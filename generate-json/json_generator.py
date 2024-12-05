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

def get_time_slots(reader: csv.DictReader) -> list[str]:
    header = reader.fieldnames
    return [slot for slot in header if slot not in ["DAY", "Section"]]

def getDayInSchema(abbr:str):
    if(abbr.upper() == 'MON'): return 'monday'
    if(abbr.upper() == 'TUE'): return 'tuesday'
    if(abbr.upper() == 'WED'): return 'wednesday'
    if(abbr.upper() == 'THU'): return 'thursday'
    if(abbr.upper() == 'FRI'): return 'friday'
    if(abbr.upper() == 'SAT'): return 'saturday'
    if(abbr.upper() == 'SUN'): return 'sunday'
    

academic_year = "2024 - 2025"
sem = "SEM4 - SCE"
output_dir = 'output/' + academic_year + '/' + sem + '/'

modified_count = 0

# make dir if doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_dict = {
    "meta": {
        "section": "a10",
        "type": "norm-class",
        "revision": "Revision 1.0",
        "effective-date": "Dec 4, 2024",
        "contributor": "PlanSync Admin :)",
        "isTimetableUpdating": False
    },

    "data": {}
}

time_slots = None


for csvFile in os.listdir('./generate-json/csv/input/'):
    if not os.path.isfile('./generate-json/csv/input/' + csvFile):
        print('Not a file: ' + csvFile + '\t SKIPPING')
        continue

    # Open the CSV file for reading
    with open('./generate-json/csv/input/' + csvFile, mode='r') as file:
        print('Gen -> ' + csvFile)
        # Create a CSV reader with DictReader
        csv_reader = csv.DictReader(file, delimiter=",")
        if(time_slots == None):
            time_slots = get_time_slots(csv_reader)
    
        # Iterate through each row in the CSV file
        for row in csv_reader:
            
            # Modify output_dict and add day-wise value
            # update keys as per csv header
            day_in_schema = getDayInSchema(row["DAY"])
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