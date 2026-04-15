import argparse
from pathlib import Path

from predictor.config import PATHS
from predictor.features import build_features
from predictor.forecast import predict_day, predict_single
from predictor.loaders import load_events, load_traffic, load_weather
from predictor.model import train_model
from predictor.persistence import load_model, save_model


def run_cli() -> None:
    # parse main commandline options
    parser = argparse.ArgumentParser(description="Toulouse Subway Traffic Predictor")
    parser.add_argument("--predict", action="store_true")
    parser.add_argument("--date", default=None, metavar="YYYY-MM-DD")
    parser.add_argument("--hour", type=int, default=None, metavar="0-23")
    parser.add_argument("--retrain", action="store_true")
    args = parser.parse_args()

    # load source data files
    print("Loading data ...")
    weather = load_weather(PATHS["weather"])
    events = load_events(PATHS["events"])
    traffic = load_traffic(PATHS["traffic"])
    print(f"Weather rows: {len(weather):,}")
    print(f"Events rows: {len(events):,}")
    print(f"Traffic rows: {len(traffic):,}")

    # either load model or retrain from scratch
    model_path = Path(PATHS["model"])
    if args.predict and model_path.exists() and not args.retrain:
        print(f"Loading model from {model_path}")
        model = load_model(str(model_path))
    else:
        print("Building features and training model ...")
        features_df = build_features(traffic, weather, events)
        model = train_model(features_df)
        save_model(model, str(model_path))

    # if in predict mode output one hour or a full day
    if not args.predict:
        return
    if not args.date:
        parser.error("--predict requires --date YYYY-MM-DD")

    if args.hour is not None:
        value = predict_single(model, args.date, args.hour, weather, events)
        print(f"Predicted traffic on {args.date} {args.hour:02d}:00 = {value:.0f}")
        return

    day_df = predict_day(model, args.date, weather, events)
    print(day_df.to_string(index=False))
    print(f"Daily total: {day_df['predicted_traffic'].sum():,}")
