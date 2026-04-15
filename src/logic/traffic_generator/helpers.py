import csv
from datetime import datetime
from pathlib import Path

from logic.globales import HOLIDAYS


def pick_band(value: float, bands) -> float:
    # return first matching multiplier interval
    for low, high, mult in bands:
        if low <= value <= high:
            return mult
    return 1.0


def load_events(events_path: Path):
    # read date ranges from events csv
    events = []
    with open(events_path, newline="") as csvfile:
        for row in csv.DictReader(csvfile):
            if not row.get("START DATE") or not row.get("END DATE"):
                continue
            start_date = datetime.strptime(row["START DATE"], "%Y-%m-%d").date()
            end_date = datetime.strptime(row["END DATE"], "%Y-%m-%d").date()
            events.append((start_date, end_date))
    return events


def has_event(target_date, events) -> bool:
    # at least one event active on this date
    return any(start <= target_date <= end for start, end in events)


def is_holiday(target_date) -> bool:
    # handle both normal and yearwrapping ranges
    for start, end in HOLIDAYS:
        start_date = datetime.strptime(f"{target_date.year}-{start}", "%Y-%m-%d").date()
        end_date = datetime.strptime(f"{target_date.year}-{end}", "%Y-%m-%d").date()
        if start > end:
            end_date = datetime.strptime(f"{target_date.year + 1}-{end}", "%Y-%m-%d").date()
        if start_date <= target_date <= end_date:
            return True
    return False
