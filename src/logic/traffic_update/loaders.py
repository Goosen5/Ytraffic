import csv
from datetime import datetime
from pathlib import Path


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
            events.append((start, end))
    return events


def load_rows(path: Path):
    with open(path, newline="") as file_obj:
        return list(csv.DictReader(file_obj))


def write_rows(path: Path, rows):
    with open(path, "w", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
