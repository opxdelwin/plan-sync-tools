#!/usr/bin/env python3

import csv
import json
import os
from collections import defaultdict

INPUT_CSV = "./input/input.csv"
OUTPUT_DIR = "./output"
SKIP_IF_FIRST_CELL_CONTENT = "Sem 7 | "

META = {
    "type": "norm-class",
    "revision": "Revision 1.1",
    "effective-date": "Jul 13, 2026",
    "contributor": "PlanSync Admin :)",
    "isTimetableUpdating": False,
}


def parse_cell(cell):
    """
    Cell format:
        SUBJECT
        TEACHER
        ROOM

    Returns (subject, teacher, room)
    """
    parts = [p.strip() for p in cell.split("\n") if p.strip()]
    if len(parts) < 3:
        return None

    return parts[0], parts[1], parts[2]


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timetables = defaultdict(
        lambda: {
            "meta": {},
            "data": defaultdict(list),
        }
    )

    with open(INPUT_CSV, newline="", encoding="utf-8-sig") as f:
        reader = csv.reader(f)

        header = next(reader)
        time_slots = header[2:]

        for row in reader:
            if len(row) < 2:
                continue

            # Skip rows where the first cell matches the SKIP_IF_FIRST_CELL_CONTENT
            if row[0].strip().startswith(SKIP_IF_FIRST_CELL_CONTENT):
                continue

            section = row[0].strip()
            day = row[1].strip().lower()

            if not section or not day:
                continue

            timetable = timetables[section]

            if not timetable["meta"]:
                timetable["meta"] = {
                    "section": section,
                    **META,
                }

            for time, cell in zip(time_slots, row[2:]):
                cell = cell.strip()

                if not cell:
                    continue

                parsed = parse_cell(cell)
                if parsed is None:
                    print(
                        f"Warning: malformed cell for {section} {day} {time}: {cell}"
                    )
                    continue

                subject, teacher, room = parsed

                timetable["data"][day].append(
                    {
                        "time": time,
                        "subject": subject,
                        "teacher": [teacher],
                        "room": room,
                    }
                )

    for section, timetable in timetables.items():
        timetable["data"] = dict(timetable["data"])

        out_path = os.path.join(OUTPUT_DIR, f"{section}.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(timetable, f, indent=2, ensure_ascii=False)
            f.write("\n")

        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
