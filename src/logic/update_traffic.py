import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from logic.traffic_update.cli import run_cli


if __name__ == "__main__":
    run_cli()