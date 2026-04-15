import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.append(str(SRC_DIR))

from predictor.cli import run_cli


if __name__ == "__main__":
    # keep this file tiny all logic now lives in predictor package
    run_cli()