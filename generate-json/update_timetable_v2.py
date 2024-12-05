# convert the old timetable schema to the latest one
# the new one adds functionality of period wise room
# number and timing.

import json
import os
from collections import OrderedDict

def convert_timetable(old_data):
    new_data = {
        "meta": {
            "section": old_data["meta"]["section"],
            "type": old_data["meta"]["type"],
            "revision": old_data["meta"]["revision"],
            "effective-date": old_data["meta"]["effective-date"],
            "contributor": old_data["meta"]["contributor"],
            "isTimetableUpdating": False ,
        },
        "data": {}
    }

    for day, schedule in old_data["data"].items():
        new_data["data"][day] = []
        for time, subject in schedule.items():
            new_entry = {
                "time": time,
                "subject": subject,
                "room": str(old_data["meta"]["room"].get(day, ""))
            }
            new_data["data"][day].append(new_entry)

    return new_data

def save_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)



for dir in os.listdir('./generate-json/data/sem1'):
    if not dir.endswith('.json'):
        print('Not json file', dir, 'Skipping')
        continue

    # Read the old format JSON file
    with open('./generate-json/data/sem1/'+dir, 'r') as f:
        old_data = json.load(f)

    # Convert the data
    new_data = convert_timetable(old_data)

    # Save the new format JSON file
    save_json(new_data, './output/sem1/'+dir)

    print("Conversion complete. New timetable saved as ", dir)