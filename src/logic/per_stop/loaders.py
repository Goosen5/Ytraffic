import csv
import re
from datetime import datetime
from pathlib import Path

from logic.per_stop.stops import NAME_INDEX, normalise


def stops_for_event_station(raw_station: str):
    if not raw_station or str(raw_station).strip().lower() == "nan":
        return set()

    # split event station field on common separators
    parts = re.split(r"\bou\b|/|,|\bet\b", raw_station, flags=re.IGNORECASE)
    found = set()
    for part in parts:
        norm = normalise(part)
        for key, stop_id in NAME_INDEX.items():
            if key in norm or norm in key:
                found.add(stop_id)
                break
    return found


def load_weather(path: Path):
    out = {}
    with open(path, newline="") as file_obj:
        for row in csv.DictReader(file_obj):
            dt = datetime.strptime(row["AAAAMMJJHH"], "%Y%m%d%H")
            out[dt.strftime("%Y-%m-%d %H:%M")] = {
                "rain": float(row["RR1"]) if row.get("RR1") else 0.0,
                "temp": float(row["T"]) if row.get("T") else None,
                "dt": dt,
            }
    return out


def load_events(path: Path):
    events = []
    with open(path, newline="") as file_obj:
        for row in csv.DictReader(file_obj):
            if not row.get("START DATE") or not row.get("END DATE"):
                continue
            start = datetime.strptime(row["START DATE"], "%Y-%m-%d").date()
            end = datetime.strptime(row["END DATE"], "%Y-%m-%d").date()
            stop_ids = stops_for_event_station(row.get("STATION", ""))
            events.append((start, end, stop_ids))
    return events


def load_network_rows(path: Path):
    with open(path, newline="") as file_obj:
        return list(csv.DictReader(file_obj))
