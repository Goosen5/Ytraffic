import argparse
from pathlib import Path

from logic.traffic_update.paths import DEFAULT_EVENTS, DEFAULT_OUT, DEFAULT_TRAFFIC, DEFAULT_WEATHER
from logic.traffic_update.service import update_traffic


def run_cli():
    parser = argparse.ArgumentParser(description="reapply traffic multipliers to traffic csv")
    parser.add_argument("--traffic", default=DEFAULT_TRAFFIC)
    parser.add_argument("--weather", default=DEFAULT_WEATHER)
    parser.add_argument("--events", default=DEFAULT_EVENTS)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rows_in, rows_out = update_traffic(
        traffic_path=Path(args.traffic),
        weather_path=Path(args.weather),
        events_path=Path(args.events),
        out_path=Path(args.out),
        dry_run=args.dry_run,
    )

    if args.dry_run:
        print("dry run no file written")
        changed = [
            (old, new)
            for old, new in zip(rows_in, rows_out)
            if old["traffic"] != new["traffic"]
        ][:10]
        if changed:
            print("datetime old new")
            for old, new in changed:
                print(f"{old['datetime']} {old['traffic']} {new['traffic']}")
