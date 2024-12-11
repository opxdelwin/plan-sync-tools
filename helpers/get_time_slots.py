from csv import DictReader
from typing import List


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

    return [
        slot
        for slot in reader.fieldnames
        if slot not in extensionKeys
    ]
