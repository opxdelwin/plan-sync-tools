#!/usr/bin/env python3

import glob
import json
import os

INPUT_DIR = "./output"
OUTPUT_FILE = "./output/sections.json"

ACADEMIC_YEAR = "2026 - 2027"
SEMESTER = "SEM3 - SCE"
COURSE = "BTech CSE"


def main():
    mapping = {
        ACADEMIC_YEAR: {
            SEMESTER: {}
        }
    }

    json_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.json")))

    for path in json_files:
        with open(path, "r", encoding="utf-8") as f:
            timetable = json.load(f)
            print(f"Processing {path}...")

        section = timetable["meta"]["section"]

        mapping[ACADEMIC_YEAR][SEMESTER][section] = (
            f"{section} - {COURSE}"
        )

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(mapping, f, indent=2, ensure_ascii=False)
        f.write("\n")

    print(f"Wrote {OUTPUT_FILE}")


if __name__ == "__main__":
    main()