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
