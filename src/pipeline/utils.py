from datetime import datetime

import unidecode


def sanitize(entry: str) -> str:
    entry = unidecode.unidecode(entry)
    try:
        entry = bytes(entry, "utf-8").decode("unicode_escape").strip()
    except UnicodeDecodeError as e:
        print(f"Error decoding string: {e}")
    entry = entry.replace("Ã(", "").replace('"', "").split(".")[0]
    return entry


def convert_to_date(date_str: str):
    formats = ["%d %B %Y", "%d/%m/%Y", "%Y-%m-%d"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt).date()
        except ValueError:
            continue
    print(f"Unrecognized date format: {date_str}")
    return None
