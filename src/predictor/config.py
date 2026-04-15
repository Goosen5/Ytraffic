from pathlib import Path

# turn this on only if xgboost is installed in your env
USE_XGBOOST = False

# keep all project paths in one place
ROOT_DIR = Path(__file__).resolve().parents[2]
PATHS = {
    "weather": str(ROOT_DIR / "assets" / "datas.csv"),
    "events": str(ROOT_DIR / "assets" / "event-toulouse.csv"),
    "traffic": str(ROOT_DIR / "returns" / "traffic.csv"),
    "model": str(ROOT_DIR / "returns" / "subway_model.pkl"),
}

# these are the exact columns used by the model
FEATURE_COLS = [
    "hour", "dayofweek", "month", "dayofmonth",
    "is_weekend", "is_rush",
    "hour_sin", "hour_cos",
    "dow_sin", "dow_cos",
    "month_sin", "month_cos",
    "rain_mm", "temp_c", "humidity_pct", "is_raining",
    "active_events", "has_event",
]
