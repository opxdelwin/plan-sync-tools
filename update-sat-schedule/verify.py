"""
Generates schedule of a section as per required
JSON schema by the application.

Generates unique JSON for all csv files 
from `csv/` dir. Make sure all sections are
available prior.

CLEAR CSV, OUTPUT, XLS for EACH iteration
"""

import json
import os

academic_year = "2023 - 2024"
sem = "SEM2"
output_dir = 'update-sat-schedule/output/' + academic_year + '/' + sem + '/'

verified_count = 0


for jsonFile in os.listdir('update-sat-schedule/data/'):
    if not os.path.isfile('update-sat-schedule/data/' + jsonFile):
        print('Not a file: ' + jsonFile + '\t SKIPPING')
        continue

    with open(output_dir + jsonFile, mode='r') as file:
        print('Verifying -> ' + jsonFile)
        original = json.load(file)

        print('\t eff-date: ', original['meta']['effective-date'] == "Jan 15, 2024 (Satrudays' valid till Apr 13)")
        if(not jsonFile.startswith('electives')) :
             print('\t room: ', original['meta']['room']['saturday'] == original['meta']['room']['monday'] )
        print('\t schedule: ', original['data']['saturday'] == original['data']['monday'])


        verified_count+=1


print("\n|---------- Verified {} JSON FILES ----------|\n".format(verified_count))