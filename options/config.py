from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
OPTIONS_DIR = ROOT_DIR / "options"
if str(OPTIONS_DIR) not in sys.path:
    sys.path.append(str(OPTIONS_DIR))
DATA_DIR = ROOT_DIR / "data"
