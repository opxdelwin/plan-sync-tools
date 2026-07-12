#!/usr/bin/env python3

import json
from pathlib import Path

import pandas as pd

# ------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------

SCHEME_NAME = "sce"  # <-- Change this once if needed

INPUT_FILE = Path("./input/input.csv")
OUTPUT_DIR = Path("./output")

META = {
    "type": "electives",
    "revision": "Revision 1.1",
    "effective-date": "Jul 13, 2026",
    "name": f"Electives Configuration for {SCHEME_NAME.upper()}",
    "isTimetableUpdating": False,
}

DAY_MAP = {
    "Monday": "monday",
    "Tuesday": "tuesday",
    "Wednesday": "wednesday",
    "Thursday": "thursday",
    "Friday": "friday",
}

NON_TIME_COLUMNS = {"section", "day"}


def extract_cell(cell: str) -> tuple[list[str], str]:
    """
    Cell format: <sub> [teacher...] <room>
        AI
        Prof. XYZ
        Prof. ABC
        C25-A007

    Returns:
        (teachers, room) -> (["Prof. XYZ", "Prof. ABC"], "C25-A007")
    """
    lines = [line.strip() for line in str(cell).splitlines() if line.strip()]
    room = lines[-1] if lines else ""
    teachers = lines[1:-1] if len(lines) >= 2 else []
    return teachers, room


def main():
    df = pd.read_csv(INPUT_FILE)

    time_columns = [
        col for col in df.columns if col.strip().lower() not in NON_TIME_COLUMNS
    ]

    output = {day: [] for day in DAY_MAP.values()}

    for _, row in df.iterrows():
        day = DAY_MAP.get(str(row["Day"]).strip())
        section = str(row["Section"]).strip()

        if not day:
            continue

        for time in time_columns:
            value = row.get(time)

            if pd.isna(value):
                continue

            teachers, room = extract_cell(value)

            output[day].append(
                {
                    "subject": section,
                    "teachers": teachers,
                    "room": room,
                    "time": time,
                }
            )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = OUTPUT_DIR / f"elective-scheme-{SCHEME_NAME}.json"

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(
            {
                "meta": META,
                "data": output,
            },
            f,
            indent=2,
            ensure_ascii=False,
        )

    print(f"Generated: {output_file}")


if __name__ == "__main__":
    main()
