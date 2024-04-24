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

modified_count = 0

# make dir if doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)


for jsonFile in os.listdir('update-sat-schedule/data/'):
    if not os.path.isfile('update-sat-schedule/data/' + jsonFile):
        print('Not a file: ' + jsonFile + '\t SKIPPING')
        continue

    with open('update-sat-schedule/data/' + jsonFile, mode='r+') as file:
        print('Gen -> ' + jsonFile)
        original = json.load(file)

        original['meta']['effective-date'] = "Jan 15, 2024 (Satrudays' valid till Apr 13)"
        
        if(not jsonFile.startswith('electives')) :
             original['meta']['room']['saturday'] = original['meta']['room']['monday']

        original['data']['saturday'] = original['data']['monday']

        modified = original
        
        with open(output_dir + jsonFile, 'w') as writeFile:
                json.dump(modified, writeFile, indent=4)
                writeFile.close()

        modified_count+=1


print("\n|---------- GENERATED {} JSON FILES ----------|\n".format(modified_count))