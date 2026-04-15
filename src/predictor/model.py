import numpy as np
import pandas as pd

from predictor.config import FEATURE_COLS, USE_XGBOOST


def make_model():
    # pick one model family with the same hyperparams as before
    if USE_XGBOOST:
        import xgboost as xgb

        return xgb.XGBRegressor(
            n_estimators=600,
            learning_rate=0.05,
            max_depth=6,
            subsample=0.8,
            colsample_bytree=0.8,
            min_child_weight=5,
            reg_alpha=0.1,
            reg_lambda=1.0,
            random_state=42,
            n_jobs=-1,
            verbosity=0,
        )

    from sklearn.ensemble import GradientBoostingRegressor

    return GradientBoostingRegressor(
        n_estimators=400,
        learning_rate=0.05,
        max_depth=5,
        subsample=0.8,
        random_state=42,
    )


def train_model(df: pd.DataFrame):
    from sklearn.metrics import mean_absolute_error, mean_squared_error

    # keep time order to avoid data leakage
    x_data = df[FEATURE_COLS].values
    y_data = df["traffic"].values
    split_idx = int(len(df) * 0.8)
    x_train, x_test = x_data[:split_idx], x_data[split_idx:]
    y_train, y_test = y_data[:split_idx], y_data[split_idx:]

    model = make_model()
    model_name = "XGBoost" if USE_XGBOOST else "GradientBoosting"
    print(f"Training {model_name} on {len(x_train):,} rows ...")
    model.fit(x_train, y_train)

    # print simple metrics and feature importance
    y_pred = model.predict(x_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
    r2 = 1 - np.sum((y_test - y_pred) ** 2) / np.sum((y_test - y_test.mean()) ** 2)
    print(f"MAE: {mae:.1f} | RMSE: {rmse:.1f} | R2: {r2:.4f}")

    importances = pd.Series(model.feature_importances_, index=FEATURE_COLS)
    print("Top features:")
    print(importances.sort_values(ascending=False).head(10).to_string())
    return model
