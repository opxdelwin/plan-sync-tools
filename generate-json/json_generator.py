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

def getDayInSchema(abbr:str):
    if(abbr.upper() == 'MON'): return 'monday'
    if(abbr.upper() == 'TUE'): return 'tuesday'
    if(abbr.upper() == 'WED'): return 'wednesday'
    if(abbr.upper() == 'THU'): return 'thursday'
    if(abbr.upper() == 'FRI'): return 'friday'
    if(abbr.upper() == 'SAT'): return 'saturday'
    if(abbr.upper() == 'SUN'): return 'sunday'
    

academic_year = "2024 - 2025"
sem = "SEM3 - SCE"
output_dir = 'output/' + academic_year + '/' + sem + '/'

modified_count = 0

# make dir if doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_dict = {
    "meta": {
        "section": "a10",
        "type": "norm-class",
        "revision": "Revision 3.0",
        "effective-date": "Sep 26, 2024",
        "contributor": "PlanSync Admin :)",
        "isTimetableUpdating": False
    },

    "data": {}
}

# 2nd,3rd year
time_slots = [
    "08:00 - 09:00",
    "09:00 - 10:00",
    "10:00 - 11:00",
    "11:00 - 12:00",
    "12:00 - 13:00",
    "13:00 - 14:00",
    "14:00 - 15:00",
    "15:00 - 16:00",
    "16:00 - 17:00",
    "17:00 - 18:00"
]

# 1st year Sch B
# time_slots = [
#     "08:00 - 10:00",
# "10:00 - 11:00",
# "10:20 - 12:20",
# "10:20 - 11:20",
# "09:50 - 10:50",
# "11:20 - 12:20",
# "11:00 - 12:00",
# "12:00 - 13:00",
# "12:20 - 13:30",
# "13:50 - 14:50",
# "14:00 - 16:00",
# "14:40 - 15:40",
# "15:00 - 16:00",
# "16:00 - 18:00",
# "16:00 - 17:00",
# "16:20 - 17:20"
# ]

# # 1st Year Scheme A
# time_slots = [
#     "08:00 - 11:00",
#     "08:00 - 10:00",
#     "08:00 - 09:00",
#     "09:00 - 10:00",
#     "09:50 - 10:50",
#     "09:50 - 11:50",
#     "10:00 - 11:00",
#     "10:20 - 11:20",
#     "10:50 - 11:50",
#     "10:00 - 12:00",
#     "11:00 - 14:00",
#     "11:10 - 12:10",
#     "11:30 - 12:30",
#     "11:00 - 12:00",
#     "11:10 - 12:10",
#     "11:20 - 12:20",
#     "11:50 - 12:50",
#     "12:20 - 13:20",
#     "12:30 - 13:30",
#     "12:20 - 14:20",
#     "13:20 - 14:20",
#     "15:00 - 16:00",
#     "15:00 - 18:00",
#     "15:30 - 17:30",
#     "15:30 - 16:30",
#     "16:40 - 17:40"
# ]


for csvFile in os.listdir('./generate-json/csv/output/'):
    if not os.path.isfile('./generate-json/csv/output/' + csvFile):
        print('Not a file: ' + csvFile + '\t SKIPPING')
        continue

    # Open the CSV file for reading
    with open('./generate-json/csv/output/' + csvFile, mode='r') as file:
        print('Gen -> ' + csvFile)
        # Create a CSV reader with DictReader
        csv_reader = csv.DictReader(file, delimiter=",")
    
        # Iterate through each row in the CSV file
        for row in csv_reader:
            
            # Modify output_dict and add day-wise value
            # update keys as per csv header
            day_in_schema = getDayInSchema(row["Day"])
            periods = []
            
            for slot in time_slots:
               
                if(row[slot] == "---/X" or row[slot].endswith("/X")):
                    continue
                else:
                    print(slot)
                    sliced = row[slot].split('/')
                    periods.append({
                        "time": slot,
                        "subject": sliced[1] if sliced[1] != "X" else "***",
                        "room": sliced[0],
                    })
                
              
        
            output_dict["data"][day_in_schema] = periods

            # update output meta['section']
            output_dict["meta"]["section"] = row["Section"]

            # write to file
            with open(output_dir + str(file.name.split('/')[-1].split('.')[0]) + '.json', 'w') as writeFile:
                json.dump(output_dict, writeFile, indent=4)
                writeFile.close()

        # need not to reset output_dict content for 
        # every iteration as it'll be overwritten anyways
        file.close()
        modified_count += 1

print("\n|---------- GENERATED {} JSON FILES ----------|\n".format(modified_count))