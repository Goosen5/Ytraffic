from pathlib import Path


def project_root() -> Path:
    # compute root from current file location
    return Path(__file__).resolve().parents[3]


def get_paths() -> dict:
    # keep all path values grouped together
    root = project_root()
    return {
        "weather": root / "assets" / "datas.csv",
        "events": root / "assets" / "event-toulouse.csv",
        "output": root / "returns" / "traffic.csv",
    }
