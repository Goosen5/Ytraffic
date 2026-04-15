import argparse
from pathlib import Path

from logic.per_stop.paths import DEFAULT_EVENTS, DEFAULT_OUT, DEFAULT_TRAFFIC, DEFAULT_WEATHER
from logic.per_stop.service import generate_per_stop


def run_cli():
    parser = argparse.ArgumentParser(description="generate per stop traffic csv")
    parser.add_argument("--traffic", default=DEFAULT_TRAFFIC)
    parser.add_argument("--weather", default=DEFAULT_WEATHER)
    parser.add_argument("--events", default=DEFAULT_EVENTS)
    parser.add_argument("--out", default=DEFAULT_OUT)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    generate_per_stop(
        traffic_path=Path(args.traffic),
        weather_path=Path(args.weather),
        events_path=Path(args.events),
        out_path=Path(args.out),
        dry_run=args.dry_run,
    )
