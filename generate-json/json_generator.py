"""
Generates schedule of a section as JSON according to required schema.

Processes all CSV files from `csv/input/` directory to generate unique JSON files.
Note: Clear CSV, OUTPUT, XLS directories before each iteration.
"""

import csv
from typing import Dict
import os
import json

# from helpers.get_time_slots import get_time_slots
# from helpers.day_from_abbr import day_from_abbr

from csv import DictReader
from typing import List


def day_from_abbr(abbr: str, capitalize: bool = False) -> str:
    """Convert day abbreviation to full day name."""
    day_mapping = {
        "MON": "monday",
        "MONDAY": "monday",
        "TUE": "tuesday",
        "TUESDAY": "tuesday",
        "WED": "wednesday",
        "WEDNESDAY": "wednesday",
        "THU": "thursday",
        "THURSDAY": "thursday",
        "FRI": "friday",
        "FRIDAY": "friday",
        "SAT": "saturday",
        "SATURDAY": "saturday",
        "SUN": "sunday",
        "SUNDAY": "sunday",
    }
    day = day_mapping.get(abbr.upper(), "")
    return day if not capitalize else day.upper()


def get_time_slots(reader: DictReader) -> List[str]:
    """
    Extract time slots from CSV header excluding 'DAY' and 'Section'.
    If present, also exclude 'Academic Year', 'Program', 'Branch', 'Semester'.
    """
    extensionKeys = ["DAY", "Section"]
    if "Academic Year" in reader.fieldnames:
        extensionKeys.append("Academic Year")
    if "Program" in reader.fieldnames:
        extensionKeys.append("Program")
    if "Branch" in reader.fieldnames:
        extensionKeys.append("Branch")
    if "Semester" in reader.fieldnames:
        extensionKeys.append("Semester")

    return [slot for slot in reader.fieldnames if slot not in extensionKeys]


def create_period(slot: str, value: str) -> Dict:
    """Create a period dictionary from slot and value."""
    if value == "---/X" or value.endswith("/X") or value == "":
        return None

    sliced = value.split("/")
    return {
        "time": slot,
        "subject": "***" if sliced[1] == "X" else sliced[1],
        "room": sliced[0],
    }


def main():
    ACADEMIC_YEAR = "2025 - 2026"
    SEMESTER = "SEM3 - SCE"
    INPUT_DIR = "./generate-json/csv/input/"
    OUTPUT_DIR = f"output/{ACADEMIC_YEAR}/{SEMESTER}/"

    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    output_template = {
        "meta": {
            "section": "a10",
            "type": "norm-class",
            "revision": "Revision 1.0",
            "effective-date": "Jul 17, 2025",
            "contributor": "PlanSync Admin :)",
            "isTimetableUpdating": False,
        },
        "data": {},
    }

    modified_count = 0

    for csv_file in os.listdir(INPUT_DIR):
        file_path = os.path.join(INPUT_DIR, csv_file)
        if not os.path.isfile(file_path):
            print(f"Not a file: {csv_file}\t SKIPPING")
            continue

        print(f"Processing -> {csv_file}")
        with open(file_path, mode="r", encoding="utf-8-sig") as file:
            csv_reader = csv.DictReader(file)
            time_slots = get_time_slots(csv_reader)
            # Group rows by section
            section_data = {}
            for row in csv_reader:
                section = row["Section"]
                day_in_schema = day_from_abbr(row["DAY"])
                periods = []
                for slot in time_slots:
                    period = create_period(slot, row[slot])
                    if period:
                        periods.append(period)
                if section not in section_data:
                    section_data[section] = {}
                if periods:
                    section_data[section][day_in_schema] = periods
            # Write one JSON per section
            for section, days in section_data.items():
                output_dict = json.loads(json.dumps(output_template))
                output_dict["meta"]["section"] = section
                output_dict["data"] = days
                output_file = os.path.join(OUTPUT_DIR, f"{section}.json")
                with open(output_file, "w", encoding="utf-8") as write_file:
                    json.dump(output_dict, write_file, indent=4)
                modified_count += 1

    print(f"\n|---------- GENERATED {modified_count} JSON FILES ----------|\n")


if __name__ == "__main__":
    main()
