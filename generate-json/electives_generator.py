"""
inupt csv file format:
DAY,Section,11:00 - 12:00,12:00 - 13:00,13:00 - 14:00
monday,HPC_CS-1,C25-A-001/HPC(DE),---/X,---/X
monday,HPC_CS-2,---/X,---/X,C25-A-001/HPC(DE)
...etc
"""

import csv
import json
from datetime import date


def parse_elective_string(elective_str: str):
    """Parse the room from the cell, or return None if empty/---/X"""
    if not elective_str or elective_str.strip() == "" or elective_str.strip() == "---/X":
        return None
    try:
        room, _ = elective_str.split("/")
        return room.strip()
    except Exception:
        return None


def generate_electives_json(csv_file_path, output_json_path):
    # Initialize the base structure
    electives_data = {
        "meta": {
            "type": "electives",
            "revision": "Revision 1.2",
            "effective-date": date.today().strftime("%b %d, %Y").lower(),
            "name": "Electives Configuration for SCE",
            "isTimetableUpdating": False,
        },
        "data": {},
    }

    # Read the CSV file
    with open(csv_file_path, "r", encoding="utf-8-sig") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            day = row["DAY"].lower().strip()
            if day not in electives_data["data"]:
                electives_data["data"][day] = []
            section = row["Section"].strip()
            for timeslot, value in row.items():
                if timeslot in ("DAY", "Section"):
                    continue
                room = parse_elective_string(value)
                if room is not None:
                    # Append the time to the room key
                    room_with_time = f"{room} / {timeslot}"
                    electives_data["data"][day].append({"subject": section, "room": room_with_time})

    # If any day has no entries, add a placeholder
    for day in electives_data["data"]:
        if not electives_data["data"][day]:
            electives_data["data"][day].append({"subject": "***", "room": "***"})

    # Write to JSON file
    with open(output_json_path, "w", encoding="utf-8") as jsonfile:
        json.dump(electives_data, jsonfile, indent=4)
        print(f"Electives JSON generated at: {output_json_path}")


if __name__ == "__main__":
    # Usage example
    csv_file_path = (
        "./generate-json/csv/input/electives.csv"  # Replace with your CSV file path
    )
    output_json_path = "./electives.json"  # Replace with desired output path
    generate_electives_json(csv_file_path, output_json_path)
