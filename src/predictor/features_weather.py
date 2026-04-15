import pandas as pd


def add_weather_features(df: pd.DataFrame, weather: pd.DataFrame) -> pd.DataFrame:
    # merge weather by datetime and fill blanks safely
    out = df.merge(weather, on="datetime", how="left")
    out["rain_mm"] = out["rain_mm"].fillna(0.0)
    out["temp_c"] = out["temp_c"].ffill().bfill()
    out["humidity_pct"] = out["humidity_pct"].ffill().bfill()

    # binary rainy flag is useful for tree models
    out["is_raining"] = (out["rain_mm"] > 0).astype(int)
    return out
