from csv import DictReader
from typing import List

def get_time_slots(reader: DictReader) -> List[str]:
    """
    Extract time slots from CSV header excluding 'DAY' and 'Section'.
    If present, also exclude 'Academic Year', 'Program', 'Branch', 'Semester'.
    """
    return [
        slot
        for slot in reader.fieldnames
        if slot
        not in ["DAY", "Section"].extend(
            # Add optional entries (if present, for SQL csv format)
            [
                "Academic Year" if ("Academic Year" in reader.fieldnames) else None,
                "Program" if ("Program" in reader.fieldnames) else None,
                "Branch" if ("Branch" in reader.fieldnames) else None,
                "Semester" if ("Semester" in reader.fieldnames) else None,
            ]
        )
    ]
