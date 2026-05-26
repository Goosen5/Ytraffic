from datetime import date as Date
from datetime import datetime, time, timedelta
from pathlib import Path
import sys
from threading import Lock

import pandas as pd
from flask import Flask, jsonify, request
from flask_cors import CORS

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from logic.per_stop.stops import STOPS
from predictor.decisionTree.decisionTree import TrafficDecisionTreeModel


TRAINING_DATA_PATH = BASE_DIR / "assets" / "training" / "traffic_per_stop.csv"

STOPS_BY_ID = {stop["stop_id"]: stop for stop in STOPS}
VALID_GRANULARITIES = {"week", "month", "year"}
VALID_PERIODS = {"morning", "afternoon", "evening"}

PERIOD_HOURS = {
    "morning": range(6, 12),
    "afternoon": range(12, 18),
    "evening": range(18, 24),
}

WEEK_LABELS = ["Lun", "Mar", "Mer", "Jeu", "Ven", "Sam", "Dim"]
MONTH_LABELS = ["Jan", "Fev", "Mar", "Avr", "Mai", "Juin", "Juil", "Aou", "Sep", "Oct", "Nov", "Dec"]

decision_tree_model = None
model_lock = Lock()


def load_training_data():
    df = pd.read_csv(TRAINING_DATA_PATH, low_memory=False)
    return df.rename(
        columns={
            "stop_id": "station_code",
            "stop_name": "station_name",
            "traffic": "value",
        }
    )


def initialize_decision_tree_model():
    model = TrafficDecisionTreeModel(max_depth=50)
    model.fit(load_training_data())
    return model


def create_app():
    app = Flask(__name__)

    global decision_tree_model
    decision_tree_model = initialize_decision_tree_model()

    if CORS is not None:
        CORS(app, resources={r"/api/*": {"origins": "*"}})
    else:
        @app.after_request
        def add_cors_headers(response):
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers["Access-Control-Allow-Headers"] = "Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, OPTIONS"
            return response

    @app.get("/api/affluence")
    def get_affluence():
        validation_error, params = validate_affluence_params(request.args)
        if validation_error is not None:
            return jsonify({"error": validation_error}), 400

        stop = params["stop"]
        granularity = params["granularity"]
        period = params["period"]
        selected_date = params["date"]

        prediction_df = build_prediction_frame(stop, granularity, period, selected_date)

        with model_lock:
            predictions = decision_tree_model.predict(prediction_df)

        response = aggregate_predictions(prediction_df, predictions, granularity)
        return jsonify(response)

    return app


def validate_affluence_params(args):
    stop_id = args.get("stop_id")
    granularity = args.get("granularity")
    period = args.get("period")
    raw_date = args.get("date")

    if stop_id is None:
        return "Query parameter 'stop_id' is required.", None

    if stop_id not in STOPS_BY_ID:
        valid_stop_ids = ", ".join(STOPS_BY_ID.keys())
        return f"Query parameter 'stop_id' must be one of: {valid_stop_ids}.", None

    if granularity not in VALID_GRANULARITIES:
        return "Query parameter 'granularity' must be one of: week, month, year.", None

    if period not in VALID_PERIODS:
        return "Query parameter 'period' must be one of: morning, afternoon, evening.", None

    if raw_date is None:
        return "Query parameter 'date' is required in YYYY-MM-DD format.", None

    try:
        parsed_date = datetime.strptime(raw_date, "%Y-%m-%d").date()
    except ValueError:
        return "Query parameter 'date' must be a valid date in YYYY-MM-DD format.", None

    return None, {
        "stop": STOPS_BY_ID[stop_id],
        "granularity": granularity,
        "period": period,
        "date": parsed_date,
    }


def build_prediction_frame(stop, granularity, period, selected_date):
    hours = PERIOD_HOURS[period]
    rows = []

    for chart_point_date, chart_point_label in get_chart_points_dates(granularity, selected_date):
        for hour in hours:
            dt = datetime.combine(chart_point_date, time(hour=hour))
            rows.append(
                {
                    "datetime": dt,
                    "date": chart_point_date.isoformat(),
                    "hour": hour,
                    "station_code": stop["stop_id"],
                    "station_name": stop["stop_name"],
                    "line": stop["line"],
                    "label": chart_point_label,
                }
            )

    return pd.DataFrame(rows)


def get_chart_points_dates(granularity, selected_date):
    if granularity == "week":
        start = selected_date - timedelta(days=selected_date.weekday())
        chart_points_dates = []

        for offset, label in enumerate(WEEK_LABELS):
            chart_point_date = start + timedelta(days=offset)
            chart_points_dates.append((chart_point_date, label))

        return chart_points_dates

    if granularity == "month":
        current = selected_date.replace(day=1)
        chart_points_dates = []

        while current.month == selected_date.month:
            label = f"{current.day:02d}"
            chart_points_dates.append((current, label))
            current += timedelta(days=1)

        return chart_points_dates

    chart_points_dates = []

    for month in range(1, 13):
        chart_point_date = Date(selected_date.year, month, 15)
        label = MONTH_LABELS[month - 1]
        chart_points_dates.append((chart_point_date, label))

    return chart_points_dates


def aggregate_predictions(prediction_df, predictions, granularity):
    df = prediction_df[["label"]].copy()
    df["affluence"] = predictions

    grouped = df.groupby("label", sort=False)["affluence"].mean()

    return [
        {"label": label, "affluence": int(round(float(affluence)))}
        for label, affluence in grouped.items()
    ]


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
