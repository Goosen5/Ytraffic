import csv
from datetime import datetime
from pathlib import Path

from logic.per_stop.loaders import load_events, load_network_rows, load_weather
from logic.per_stop.math_tools import is_holiday, pick_band
from logic.per_stop.rules import (
    EVENT_MULTIPLIER,
    HOLLIDAY_MULTIPLIER,
    RAIN_MULTIPLIER_BANDS,
    TEMP_MULTIPLIER_BANDS,
    WEEK_MULT_BY_HOUR,
    WEEKEND_MULT_BY_HOUR,
)
from logic.per_stop.stops import STOPS


FIELDNAMES = ["datetime", "date", "hour", "stop_id", "stop_name", "line", "traffic"]


def active_stop_events(target_date, events):
    active = set()
    for start, end, stop_ids in events:
        if start <= target_date <= end:
            active |= stop_ids
    return active


def _iter_output_rows(network_rows, weather, events):
    prev_date = None
    active_evts = set()

    for net_row in network_rows:
        dt_key = net_row["datetime"]
        w = weather.get(dt_key)
        dt = datetime.strptime(dt_key, "%Y-%m-%d %H:%M")
        today = dt.date()

        if today != prev_date:
            active_evts = active_stop_events(today, events)
            prev_date = today

        is_weekend = dt.weekday() >= 5
        hour_table = WEEKEND_MULT_BY_HOUR if is_weekend else WEEK_MULT_BY_HOUR
        hour_mult = hour_table.get(dt.hour, 1.0)
        rain_mult = pick_band(w["rain"], RAIN_MULTIPLIER_BANDS) if w else 1.0
        temp_mult = pick_band(w["temp"], TEMP_MULTIPLIER_BANDS) if (w and w["temp"] is not None) else 1.0
        holiday_mult = HOLLIDAY_MULTIPLIER if is_holiday(today) else 1.0

        shared_mult = hour_mult * rain_mult * temp_mult * holiday_mult
        base_seed = int(net_row["traffic"]) / shared_mult if shared_mult else int(net_row["traffic"])

        for stop in STOPS:
            event_mult = EVENT_MULTIPLIER if stop["stop_id"] in active_evts else 1.0
            stop_traffic = int(base_seed * stop["base_multiplier"] * hour_mult * rain_mult * temp_mult * event_mult * holiday_mult)
            yield {
                "datetime": dt_key,
                "date": net_row["date"],
                "hour": net_row["hour"],
                "stop_id": stop["stop_id"],
                "stop_name": stop["stop_name"],
                "line": stop["line"],
                "traffic": stop_traffic,
            }


def generate_per_stop(traffic_path: Path, weather_path: Path, events_path: Path, out_path: Path, dry_run: bool = False):
    weather = load_weather(weather_path)
    events = load_events(events_path)
    network_rows = load_network_rows(traffic_path)

    print(f"input rows {len(network_rows):,}")
    print(f"stops {len(STOPS)}")
    print(f"output rows {len(network_rows) * len(STOPS):,}")
    print(f"output file {out_path}")

    rows = _iter_output_rows(network_rows, weather, events)
    if dry_run:
        print("datetime,date,hour,stop_id,stop_name,line,traffic")
        for index, row in enumerate(rows):
            if index >= len(STOPS) * 2:
                break
            print(",".join(str(row[k]) for k in FIELDNAMES))
        return

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w", newline="") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)
