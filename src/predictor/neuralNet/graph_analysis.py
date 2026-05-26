import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import imageio.v2 as imageio
from tqdm import tqdm

from neuralNet import TrafficNeuralNetModel

BASE = "graphs"
FRAMES = f"{BASE}/frames"
GIFS = f"{BASE}/gifs"

os.makedirs(FRAMES, exist_ok=True)
os.makedirs(GIFS, exist_ok=True)

metrics = [
    "real_vs_pred",
    "hourly_pattern",
    "accuracy_curve",
    "hourly_bias",
    "heatmap",
    "station_pattern"
]

for m in metrics:
    os.makedirs(f"{FRAMES}/{m}", exist_ok=True)

train_df = pd.read_csv("assets/training/traffic_per_stop.csv", low_memory=False)
test_df = pd.read_csv("assets/test/traffic_per_stop.csv", low_memory=False)

train_df.columns = test_df.columns = [
    "datetime", "date", "hour",
    "station_code", "station_name",
    "line", "value"
]

test_df["datetime"] = pd.to_datetime(test_df["datetime"], errors="coerce")

baseline_value = test_df["value"].mean()
baseline_mae = (test_df["value"] - baseline_value).abs().mean()

ref_df = test_df.copy()
ref_df["hour"] = ref_df["datetime"].dt.hour

pivot_reference = ref_df.pivot_table(
    index="hour",
    columns="station_name",
    values="value",
    aggfunc="mean"
)
station_order = pivot_reference.columns
vmin, vmax = pivot_reference.min().min(), pivot_reference.max().max()

gif_frames = {m: [] for m in metrics}
accuracy_history = []
stations_focus = "A06"

hidden_sizes = range(4, 128, 4)

for size in tqdm(hidden_sizes, desc="Training Neural Nets", unit="size"):

    model = TrafficNeuralNetModel(
        hidden_dim=size,
        num_layers=2,
    )

    model.fit(train_df)
    preds = model.predict(test_df)

    df = test_df.copy()
    df["pred"] = preds
    df["hour"] = df["datetime"].dt.hour
    df["error"] = df["value"] - df["pred"]

    # Real vs Pred
    plt.figure()
    plt.scatter(df["value"][:500], df["pred"][:500], alpha=0.4)
    plt.title(f"Real vs Pred (Hidden Size {size})")
    path = f"{FRAMES}/real_vs_pred/frame_{size}.png"
    plt.savefig(path)
    plt.close()
    gif_frames["real_vs_pred"].append(imageio.imread(path))

    # Hourly Pattern
    real = df.groupby("hour")["value"].mean()
    pred = df.groupby("hour")["pred"].mean()
    plt.figure()
    plt.plot(real.index, real.values, label="Real")
    plt.plot(pred.index, pred.values, label="Pred")
    plt.title(f"Hourly Pattern (Hidden Size {size})")
    plt.legend()
    plt.grid()
    path = f"{FRAMES}/hourly_pattern/frame_{size}.png"
    plt.savefig(path)
    plt.close()
    gif_frames["hourly_pattern"].append(imageio.imread(path))

    # Accuracy Curve
    mae = df["error"].abs().mean()
    accuracy = (1 - mae / baseline_mae) * 100
    accuracy = max(0, min(100, accuracy))
    accuracy_history.append(accuracy)

    plt.figure()
    plt.plot(list(hidden_sizes)[:len(accuracy_history)], accuracy_history)
    plt.ylim(0, 100)
    plt.title("Model Accuracy vs Baseline (%)")
    plt.xlabel("Hidden Neuron Size")
    plt.ylabel("Accuracy (%)")
    plt.grid()
    plt.scatter(size, accuracy, s=50)
    path = f"{FRAMES}/accuracy_curve/frame_{size}.png"
    plt.savefig(path)
    plt.close()
    gif_frames["accuracy_curve"].append(imageio.imread(path))

    # Hourly Bias
    bias = df.groupby("hour")["error"].mean()
    plt.figure()
    plt.plot(bias.index, bias.values)
    plt.axhline(0, linestyle="--")
    plt.title(f"Hourly Bias (Hidden Size {size})")
    plt.grid()
    path = f"{FRAMES}/hourly_bias/frame_{size}.png"
    plt.savefig(path)
    plt.close()
    gif_frames["hourly_bias"].append(imageio.imread(path))

    # Heatmap
    pivot = df.pivot_table(
        index="hour",
        columns="station_name",
        values="pred",
        aggfunc="mean"
    )
    pivot = pivot.reindex(columns=station_order)
    plt.figure(figsize=(14, 6))
    sns.heatmap(pivot, cmap="viridis", vmin=vmin, vmax=vmax)
    plt.title(f"Heatmap (Hidden Size {size})")
    plt.xticks(rotation=90)
    path = f"{FRAMES}/heatmap/frame_{size}.png"
    plt.savefig(path)
    plt.close()
    gif_frames["heatmap"].append(imageio.imread(path))

    # Station Focus
    st_df = df[df["station_code"] == stations_focus]
    if len(st_df) > 0:
        real_s = st_df.groupby("hour")["value"].mean()
        pred_s = st_df.groupby("hour")["pred"].mean()
        plt.figure()
        plt.plot(real_s.index, real_s.values, label="Real")
        plt.plot(pred_s.index, pred_s.values, label="Pred")
        plt.title(f"Station {stations_focus} (Hidden Size {size})")
        plt.legend()
        plt.grid()
        path = f"{FRAMES}/station_pattern/frame_{size}.png"
        plt.savefig(path)
        plt.close()
        gif_frames["station_pattern"].append(imageio.imread(path))

for m in metrics:
    imageio.mimsave(
        f"{GIFS}/{m}.gif",
        gif_frames[m],
        duration=0.5
    )

print("Neural network training visuals saved.")