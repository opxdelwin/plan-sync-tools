"""
Generates schedule of a section as JSON according to required schema.

Processes all CSV files from `csv/` directory to generate unique JSON files.
Note: Clear CSV, OUTPUT, XLS directories before each iteration.
"""

import csv
from typing import List, Dict
import os
import json

def get_time_slots(reader: csv.DictReader) -> List[str]:
    """Extract time slots from CSV header excluding 'DAY' and 'Section'."""
    return [slot for slot in reader.fieldnames if slot not in ["DAY", "Section"]]

def get_day_in_schema(abbr: str) -> str:
    """Convert day abbreviation to full day name."""
    day_mapping = {
        'MON': 'monday',
        'MONDAY': 'monday',
        'TUE': 'tuesday',
        'TUESDAY': 'tuesday',
        'WED': 'wednesday',
        'WEDNESDAY': 'wednesday',
        'THU': 'thursday',
        'THURSDAY': 'thursday',
        'FRI': 'friday',
        'FRIDAY': 'friday',
        'SAT': 'saturday',
        'SATURDAY': 'saturday',
        'SUN': 'sunday',
        'SUNNDAY': 'sunday'
    }
    return day_mapping.get(abbr.upper(), '')

def create_period(slot: str, value: str) -> Dict:
    """Create a period dictionary from slot and value."""
    if value == "---/X" or value.endswith("/X"):
        return None
    
    sliced = value.split('/')
    return {
        "time": slot,
        "subject": "***" if sliced[1] == "X" else sliced[1],
        "room": sliced[0]
    }

def main():
    ACADEMIC_YEAR = "2024 - 2025"
    SEMESTER = "SEM4 - ECS"
    INPUT_DIR = './generate-json/csv/input/'
    OUTPUT_DIR = f'output/{ACADEMIC_YEAR}/{SEMESTER}/'

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_template = {
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

    modified_count = 0

    for csv_file in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, csv_file)
        if not os.path.isfile(file_path):
            print(f'Not a file: {csv_file}\t SKIPPING')
            continue

        print(f'Processing -> {csv_file}')
        with open(file_path, mode='r') as file:
            csv_reader = csv.DictReader(file)
            time_slots = get_time_slots(csv_reader)
            output_dict = json.loads(json.dumps(output_template))
            
            for row in csv_reader:
                day_in_schema = get_day_in_schema(row["DAY"])
                periods = []
                
                for slot in time_slots:
                    period = create_period(slot, row[slot])
                    if period:
                        periods.append(period)
                
                if periods:  # Only add the day if there are periods
                    output_dict["data"][day_in_schema] = periods
                output_dict["meta"]["section"] = row["Section"]

                output_file = os.path.join(OUTPUT_DIR, f"{os.path.splitext(csv_file)[0]}.json")
                with open(output_file, 'w') as write_file:
                    json.dump(output_dict, write_file, indent=4)

            modified_count += 1

    print(f"\n|---------- GENERATED {modified_count} JSON FILES ----------|\n")

if __name__ == "__main__":
    main()
