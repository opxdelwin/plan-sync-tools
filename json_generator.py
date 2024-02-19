"""
Generates schedule of a section as per required
JSON schema by the application.

Generates unique JSON for all csv files 
from `csv/` dir. Make sure all sections are
available prior.

CLEAR CSV, OUTPUT, XLS for EACH iteration
"""

import csv
import json
import os

academic_year = "2024 - 2025"
sem = "SEM2"
output_dir = 'output/' + academic_year + '/' + sem + '/'

modified_count = 0

# make dir if doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_dict = {
    "meta": {
        "section": "a1",
        "type": "norm-class",
        "revision": "Revision 1.03",
        "effective-date": "Jan 15, 2024 (Satrudays' valid till Feb 17)",
        "contributor": "PlanSync Admin",
        "isTimetableUpdating": False,
        "room": {
            "monday": 102,
            "tuesday": 104,
            "wednesday": 103,
            "thursday": 103,
            "friday": 103,
            "saturday": 103
        }
    },
    "data": {}
}


for csvFile in os.listdir('csv/'):
    if not os.path.isfile('csv/' + csvFile):
        print('Not a file: ' + csvFile + '\t SKIPPING')
        continue

    # Open the CSV file for reading
    with open('csv/' + csvFile, mode='r') as file:
        print('Gen -> ' + csvFile)
        # Create a CSV reader with DictReader
        csv_reader = csv.DictReader(file, delimiter=",")
    
        # Iterate through each row in the CSV file
        for row in csv_reader:
            # Modify output_dict and add day-wise value
            # update keys as per csv header
            output_dict["data"][row["day"]] = {
                "08:00 - 09:00": row["8-9"],
                "09:00 - 10:00": row["9-10"],
                "10:00 - 11:00": row["10-11"],
                "11:00 - 12:00": row["11-12"],
                "12:00 - 13:00": row["12-1"],
                "13:00 - 14:00": row["1-2"],
                "14:00 - 15:00": row["2-3"],
                "15:00 - 16:00": row["3-4"],
                "16:00 - 17:00": row["4-5"],
                "17:00 - 18:00": row["5-6"],
            }

            # update output meta['section']
            output_dict["meta"]["section"] = row["section"]

            # write to file
            with open(output_dir + row['section'] + '.json', 'w') as writeFile:
                json.dump(output_dict, writeFile, indent=4)
                writeFile.close()

        # need not to reset output_dict content for 
        # every iteration as it'll be overwritten anyways
        file.close()
        modified_count += 1

print("\n|---------- GENERATED {} JSON FILES ----------|\n".format(modified_count))