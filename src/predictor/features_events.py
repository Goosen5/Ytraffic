import pandas as pd


def add_event_features(df: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    # count events active on each row day
    out = df.copy()
    row_days = out["datetime"].dt.normalize()
    counts = []

    for day in row_days:
        is_active = (events["START DATE"] <= day) & (events["END DATE"] >= day)
        counts.append(int(is_active.sum()))

    # keep both count and binary flag
    out["active_events"] = counts
    out["has_event"] = (out["active_events"] > 0).astype(int)
    return out
