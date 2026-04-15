import pandas as pd


def load_weather(path: str) -> pd.DataFrame:
    # read weather then map raw column names to cleaner ones
    df = pd.read_csv(path, sep=None, engine="python")
    df["datetime"] = pd.to_datetime(df["AAAAMMJJHH"].astype(str), format="%Y%m%d%H")
    df = df.rename(columns={"RR1": "rain_mm", "T": "temp_c", "U": "humidity_pct"})

    # keep only needed columns and fill holes from neighbors
    df = df[["datetime", "rain_mm", "temp_c", "humidity_pct"]]
    df = df.set_index("datetime").sort_index().ffill().bfill().reset_index()
    return df


def load_events(path: str) -> pd.DataFrame:
    # parse event dates and drop broken rows
    df = pd.read_csv(path, sep=None, engine="python")
    df["START DATE"] = pd.to_datetime(df["START DATE"], errors="coerce")
    df["END DATE"] = pd.to_datetime(df["END DATE"], errors="coerce")
    return df.dropna(subset=["START DATE", "END DATE"])


def load_traffic(path: str) -> pd.DataFrame:
    # traffic needs valid datetime traffic value
    df = pd.read_csv(path, sep=None, engine="python")
    df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
    df = df.dropna(subset=["datetime", "traffic"])
    df = df[["datetime", "traffic"]]
    return df.sort_values("datetime").reset_index(drop=True)
