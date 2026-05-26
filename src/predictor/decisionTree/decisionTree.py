import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor


class TrafficDecisionTreeModel:
    def __init__(self, max_depth=8):
        self.model = DecisionTreeRegressor(
            max_depth=max_depth
        )
        self.feature_columns = None

    def preprocess(self, df):
        df = df.copy()

        df["datetime"] = pd.to_datetime(df["datetime"], errors="coerce")
        df = df.dropna(subset=["datetime"])

        df["hour"] = df["datetime"].dt.hour
        df["day_of_week"] = df["datetime"].dt.dayofweek
        df["month"] = df["datetime"].dt.month

        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

        df = pd.get_dummies(df, columns=["station_code", "line"])

        return df

    def fit(self, df):
        df = self.preprocess(df)

        X = df.drop(columns=["value", "datetime", "date", "station_name"])
        y = df["value"]

        self.feature_columns = X.columns
        self.model.fit(X, y)

        return self

    def predict(self, df):
        df = self.preprocess(df)

        X = df.reindex(columns=self.feature_columns, fill_value=0)
        return self.model.predict(X)

    def clone_with_depth(self, depth):
        return TrafficDecisionTreeModel(
            max_depth=depth
        )