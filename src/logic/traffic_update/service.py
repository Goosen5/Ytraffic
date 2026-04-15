from pathlib import Path

from logic.traffic_update.loaders import load_events, load_rows, load_weather, write_rows
from logic.traffic_update.math_tools import is_holiday, pick_band, recover_base_seed
from logic.traffic_update.rules import (
    EVENT_MULTIPLIER,
    HOLLIDAY_MULTIPLIER,
    RAIN_MULTIPLIER_BANDS,
    TEMP_MULTIPLIER_BANDS,
    WEEK_MULT_BY_HOUR,
    WEEKEND_MULT_BY_HOUR,
)


def has_event(target_date, events) -> bool:
    return any(start <= target_date <= end for start, end in events)


def update_traffic(traffic_path: Path, weather_path: Path, events_path: Path, out_path: Path, dry_run: bool = False):
    weather = load_weather(weather_path)
    events = load_events(events_path)
    rows_in = load_rows(traffic_path)

    changed = 0
    rows_out = []
    for row in rows_in:
        dt_key = row["datetime"]
        w = weather.get(dt_key)
        if w is None:
            rows_out.append(row)
            continue

        dt = w["dt"]
        is_weekend = dt.weekday() >= 5
        hour_mult = (WEEKEND_MULT_BY_HOUR if is_weekend else WEEK_MULT_BY_HOUR).get(dt.hour, 1.0)
        rain_mult = pick_band(w["rain"], RAIN_MULTIPLIER_BANDS)
        temp_mult = pick_band(w["temp"], TEMP_MULTIPLIER_BANDS) if w["temp"] is not None else 1.0
        event_mult = EVENT_MULTIPLIER if has_event(dt.date(), events) else 1.0
        holiday_mult = HOLLIDAY_MULTIPLIER if is_holiday(dt.date()) else 1.0

        old_traffic = int(row["traffic"])
        base_seed = recover_base_seed(old_traffic, hour_mult, rain_mult, temp_mult, event_mult, holiday_mult)
        new_traffic = int(base_seed * hour_mult * rain_mult * temp_mult * event_mult * holiday_mult)

        if new_traffic != old_traffic:
            changed += 1

        new_row = dict(row)
        new_row["traffic"] = new_traffic
        rows_out.append(new_row)

    print(f"rows processed {len(rows_out):,}")
    print(f"rows changed {changed:,}")
    print(f"rows unchanged {len(rows_out) - changed:,}")

    if dry_run:
        return rows_in, rows_out

    write_rows(out_path, rows_out)
    return rows_in, rows_out
