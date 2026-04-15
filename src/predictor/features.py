import pandas as pd

from predictor.features_events import add_event_features
from predictor.features_time import add_time_features
from predictor.features_weather import add_weather_features


def build_features(
    traffic: pd.DataFrame,
    weather: pd.DataFrame,
    events: pd.DataFrame,
) -> pd.DataFrame:
    # build features in small clear steps
    df = add_time_features(traffic)
    df = add_event_features(df, events)
    df = add_weather_features(df, weather)
    return df
