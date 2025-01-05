"""
inupt csv file format:
DAY,ELECTIVE
Monday,Room 1/Subject 1
Monday,Room 2/Subject 2
Tuesday,Room 3/Subject 3
..
"""

import csv
import json
from datetime import date


def parse_elective_string(elective_str: str):
    """Parse the room/elective string into separate components"""
    if not elective_str or elective_str.strip() == "":
        return {"subject": "***", "room": "***"}

    room, subject = elective_str.split("/")
    return {"subject": subject.strip(), "room": room.strip()}


def generate_electives_json(csv_file_path, output_json_path):
    # Initialize the base structure
    electives_data = {
        "meta": {
            "type": "electives",
            "revision": "Revision 1.0",
            "effective-date": date.today().strftime("%b %d, %Y"),
            "name": "Electives Configuration for B1 - B35",
            "isTimetableUpdating": False,
        },
        "data": {
            "monday": [],
            "tuesday": [],
            "wednesday": [],
            "thursday": [],
            "friday": [],
        },
    }

    # Read the CSV file
    with open(csv_file_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row["DAY"].lower().strip()
            if day in electives_data["data"]:
                elective_info = parse_elective_string(row["ELECTIVE"])
                electives_data["data"][day].append(elective_info)

    # If any day has no entries, add a placeholder
    for day in electives_data["data"]:
        if not electives_data["data"][day]:
            electives_data["data"][day].append({"subject": "***", "room": "***"})

    # Write to JSON file
    with open(output_json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(electives_data, jsonfile, indent=4)


if __name__ == "__main__":
    # Usage example
    csv_file_path = (
        "./generate-json/csv/input/electives.csv"  # Replace with your CSV file path
    )
    output_json_path = "./electives.json"  # Replace with desired output path
    generate_electives_json(csv_file_path, output_json_path)
