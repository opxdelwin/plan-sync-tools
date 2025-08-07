"""
This is only used to generate json for
available sections of an academic year.


run this only after generating all available 
sections (from [json_generator.py]).

CLEAR CSV, OUTPUT, XLS for EACH iteration.
"""

import os
import json

academic_year = "2025 - 2026"
semester = "SEM1 - SCE"
scan_dir = "output/" + academic_year + "/" + semester + "/"

modified_count = 0

# <K,V> pair as <filename, display-name>
response = {}

for section in os.listdir(scan_dir):
    response[os.path.splitext(section)[0]] = (
        os.path.splitext(section)[0] + " - BTech CSE"
    )
    modified_count += 1

with open(scan_dir + "sections.json", "w") as file:
    json.dump({academic_year: {semester: response}}, file, indent=4)
    file.close()

print("\n|------------- FOUND {} SECTIONS -------------|\n".format(modified_count))
