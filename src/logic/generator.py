import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1]
if str(SRC_DIR) not in sys.path:
	sys.path.append(str(SRC_DIR))

from logic.traffic_generator.generate import generate_traffic


if __name__ == "__main__":
    # keep this entry file tiny and easy to read
    print(f"Traffic file generated at: {generate_traffic()}")
