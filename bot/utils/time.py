from datetime import datetime, timedelta

def localize_time(iso: str, tz_str: str) -> str:
    """iso: 2025-08-26T19:00:00+00:00 → 23:00 для UTC+4"""
    offset = int(tz_str.replace("UTC", ""))
    dt = datetime.fromisoformat(iso.replace("+00:00", "")) + timedelta(hours=offset)
    return dt.strftime("%H:%M")