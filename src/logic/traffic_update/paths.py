from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_TRAFFIC = str(PROJECT_ROOT / "returns" / "traffic.csv")
DEFAULT_WEATHER = str(PROJECT_ROOT / "assets" / "datas.csv")
DEFAULT_EVENTS = str(PROJECT_ROOT / "assets" / "event-toulouse.csv")
DEFAULT_OUT = str(PROJECT_ROOT / "returns" / "traffic.csv")
