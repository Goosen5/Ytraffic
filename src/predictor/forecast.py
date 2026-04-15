import numpy as np
import pandas as pd

from predictor.config import FEATURE_COLS
from predictor.features import build_features


def fallback_weather(weather: pd.DataFrame, month: int) -> dict:
    # if a month is missing use a rough monthly average
    month_mask = weather["datetime"].dt.month == month
    return {
        "temp_c": float(weather.loc[month_mask, "temp_c"].mean() or 15.0),
        "humidity_pct": float(weather.loc[month_mask, "humidity_pct"].mean() or 70.0),
        "rain_mm": 0.0,
        "is_raining": 0,
    }


def predict_single(model, date_str: str, hour: int, weather: pd.DataFrame, events: pd.DataFrame) -> float:
    # build one synthetic row and run prediction
    dt_value = pd.Timestamp(date_str) + pd.Timedelta(hours=hour)
    row = pd.DataFrame({"datetime": [dt_value], "traffic": [np.nan]})
    row = build_features(row, weather, events)

    if row["temp_c"].isna().any():
        for key, value in fallback_weather(weather, dt_value.month).items():
            row[key] = value

    pred = model.predict(row[FEATURE_COLS].values)[0]
    return max(0.0, round(float(pred), 1))


def predict_day(model, date_str: str, weather: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    # predict all 24 hours one by one
    rows = []
    for hour in range(24):
        rows.append({
            "hour": hour,
            "predicted_traffic": int(predict_single(model, date_str, hour, weather, events)),
        })
    return pd.DataFrame(rows)
