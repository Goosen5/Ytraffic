import pandas as pd
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler


class TrafficNeuralNetModel:
    def __init__(self, hidden_dim=64, num_layers=3, max_iter=20):
        hidden_layer_sizes = tuple([hidden_dim] * num_layers)

        self.model = MLPRegressor(
            hidden_layer_sizes=hidden_layer_sizes,
            activation="relu",
            solver="adam",
            max_iter=max_iter,
            random_state=42,
            early_stopping=False,
            verbose=False
        )
        self.feature_columns = None
        self.scaler = StandardScaler()

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

        X_scaled = self.scaler.fit_transform(X)

        self.model.fit(X_scaled, y)

        return self

    def predict(self, df):
        df = self.preprocess(df)

        X = df.reindex(columns=self.feature_columns, fill_value=0)

        X_scaled = self.scaler.transform(X)

        return self.model.predict(X_scaled)

    def clone_with_complexity(self, hidden_dim, num_layers):
        return TrafficNeuralNetModel(
            hidden_dim=hidden_dim,
            num_layers=num_layers,
            max_iter=self.model.max_iter
        )