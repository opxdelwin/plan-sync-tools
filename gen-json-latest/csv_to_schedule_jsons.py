#!/usr/bin/env python3

import csv
import json
import os
import re
from collections import defaultdict

INPUT_CSV = "./input/input.csv"
OUTPUT_DIR = "./output"
# Group-header rows look like "Sem 7 | DL-S7-PE4 | CS21" (older CSVs: "Sem 5 | ...")
GROUP_HEADER_RE = re.compile(r"^Sem\s*\d+\s*\|")

META = {
    "type": "norm-class",
    "revision": "Revision 1.4",
    "effective-date": "Jul 20, 2026",
    "contributor": "PlanSync Admin :)",
    "isTimetableUpdating": False,
}


def parse_cell(cell):
    """
    Cell format:
        SUBJECT
        TEACHER
        ROOM
    or (no teacher):
        SUBJECT
        ROOM

    Returns (subject, teacher, room); teacher is None if absent
    """
    parts = [p.strip() for p in cell.split("\n") if p.strip()]
    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    if len(parts) == 2:
        return parts[0], None, parts[1]

    return None


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

            # Skip group-header rows; the section rows that follow carry the
            # section name themselves, so blocks for the same section (e.g.
            # core + elective course groups) merge into one timetable
            if GROUP_HEADER_RE.match(row[0].strip()):
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
                        "teacher": [teacher] if teacher else [],
                        "room": room,
                    }
                )

    slot_order = {t: i for i, t in enumerate(time_slots)}

    for section, timetable in timetables.items():
        data = {}
        for day, entries in timetable["data"].items():
            entries.sort(key=lambda e: slot_order.get(e["time"], len(slot_order)))

            merged = []
            seen = set()
            for entry in entries:
                key = (entry["time"], entry["subject"], tuple(entry["teacher"]), entry["room"])
                if key in seen:
                    continue
                seen.add(key)
                if any(e["time"] == entry["time"] for e in merged):
                    print(
                        f"Warning: conflicting entries for {section} {day} {entry['time']}"
                    )
                merged.append(entry)
            data[day] = merged

        timetable["data"] = data

        out_path = os.path.join(OUTPUT_DIR, f"{section}.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(timetable, f, indent=2, ensure_ascii=False)
            f.write("\n")

        print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
