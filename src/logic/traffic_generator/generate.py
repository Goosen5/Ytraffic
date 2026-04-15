import csv
import random

from logic.globales import (
    EVENT_MULTIPLIER,
    HOLLIDAY_MULTIPLIER,
    RAIN_MULTIPLIER_BANDS,
    TEMP_MULTIPLIER_BANDS,
    WEEKEND_RANGE,
    WEEK_MULT_BY_HOUR,
    WEEK_RANGE,
)
from logic.traffic_generator.helpers import has_event, is_holiday, load_events, pick_band
from logic.traffic_generator.paths import get_paths


def generate_traffic():
    # resolve file paths and ensure output folder exists
    paths = get_paths()
    weather_path = paths["weather"]
    events_path = paths["events"]
    output_path = paths["output"]
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # load events once before looping weather rows
    events = load_events(events_path)
    with open(weather_path, newline="") as weather_file, open(output_path, "w", newline="") as out_csv:
        reader = csv.DictReader(weather_file)
        writer = csv.DictWriter(out_csv, fieldnames=["datetime", "date", "hour", "traffic"])
        writer.writeheader()

        # build one traffic value per weather row
        for row in reader:
            dt = __import__("datetime").datetime.strptime(row["AAAAMMJJHH"], "%Y%m%d%H")
            is_weekend = dt.weekday() >= 5
            base_min, base_max = WEEKEND_RANGE if is_weekend else WEEK_RANGE
            base_seed = random.randint(base_min, base_max)
            hour_mult = WEEK_MULT_BY_HOUR.get(dt.hour, 1.0)

            rain_val = float(row["RR1"]) if row.get("RR1") else 0.0
            temp_val = float(row["T"]) if row.get("T") not in (None, "") else None
            rain_mult = pick_band(rain_val, RAIN_MULTIPLIER_BANDS)
            temp_mult = pick_band(temp_val, TEMP_MULTIPLIER_BANDS) if temp_val is not None else 1.0

            event_mult = EVENT_MULTIPLIER if has_event(dt.date(), events) else 1.0
            holiday_mult = HOLLIDAY_MULTIPLIER if is_holiday(dt.date()) else 1.0
            traffic = int(base_seed * hour_mult * rain_mult * temp_mult * event_mult * holiday_mult)

            writer.writerow({
                "datetime": dt.strftime("%Y-%m-%d %H:%M"),
                "date": dt.date().isoformat(),
                "hour": dt.hour,
                "traffic": traffic,
            })

    return output_path
