import numpy as np
import pandas as pd


def add_time_features(df: pd.DataFrame) -> pd.DataFrame:
    # extract classic time columns from datetime
    out = df.copy()
    dt = out["datetime"]
    out["hour"] = dt.dt.hour
    out["dayofweek"] = dt.dt.dayofweek
    out["month"] = dt.dt.month
    out["dayofmonth"] = dt.dt.day

    # add simple booleans for weekend and rush hours
    out["is_weekend"] = (out["dayofweek"] >= 5).astype(int)
    out["is_rush"] = out["hour"].isin([7, 8, 9, 17, 18, 19]).astype(int)

    # add cyclic encoding so model handles time wraparound
    out["hour_sin"] = np.sin(2 * np.pi * out["hour"] / 24)
    out["hour_cos"] = np.cos(2 * np.pi * out["hour"] / 24)
    out["dow_sin"] = np.sin(2 * np.pi * out["dayofweek"] / 7)
    out["dow_cos"] = np.cos(2 * np.pi * out["dayofweek"] / 7)
    out["month_sin"] = np.sin(2 * np.pi * out["month"] / 12)
    out["month_cos"] = np.cos(2 * np.pi * out["month"] / 12)
    return out
