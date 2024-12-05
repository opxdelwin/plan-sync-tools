"""
This is used to generate placeholder schedule with
meta parameter set to true. Takes in a list of 
sections, and generates json for each.
"""

import json
import os

academic_year = "2024 - 2025"
sem = "SEM3"
output_dir = 'output/' + academic_year + '/' + sem + '/'
modified_count = 0

# make dir if doesnt exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_dict = {
    "meta": {
        "section": "a1",
        "type": "norm-class",
        "revision": "Revision 1.00",
        "effective-date": "July 15, 2024",
        "contributor": "Plan Sync Admin",
        "isTimetableUpdating": True,
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

sections = ['CSE1', 'CSE2', 'CSE3', 'CSE4', 'CSE5', 'CSE6', 'CSE7', 'CSE8', 'CSE9', 'CSE10', 
 'CSE11', 'CSE12', 'CSE13', 'CSE14', 'CSE15', 'CSE16', 'CSE17', 'CSE18', 'CSE19', 
 'CSE20', 'CSE21', 'CSE22', 'CSE23', 'CSE24', 'CSE25', 'CSE26', 'CSE27', 'CSE28', 
 'CSE29', 'CSE30', 'CSE31', 'CSE32', 'CSE33', 'CSE34', 'CSE35', 'CSE36', 'CSE37', 
 'CSE38', 'CSE39', 'CSE40', 'CSE41', 'CSE42', 'CSE43', 'CSE44', 'CSE45', 'CSE46', 
 'CSE47', 'CSE48', 'CSE49', 'CSE50', 'CSE51', 'CSE52', 'CSE53', 'CSE54', 'CSE55',
 'IT1', 'IT2', 'IT3', 'IT4', 'IT5', 'CSCE1', 'CSCE2', 'CSCE3', 'CSSE1', 'CSSE2']


for section in sections:
    print('GEN -->', section)
    temp_dict = output_dict

    temp_dict['meta']['section'] = section
            # write to file
    with open(output_dir + section+ '.json', 'w') as writeFile:
        json.dump(output_dict, writeFile, indent=4)
        writeFile.close()

    modified_count += 1


print("\n|---------- GENERATED {} JSON FILES ----------|\n".format(modified_count))
