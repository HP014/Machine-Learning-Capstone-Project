"""Where everything lives, found from this file's own location so the code runs from any clone."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RESULTS = ROOT / "results"
FIGURES = RESULTS / "figures"


def latest_week():
    """The highest Week_N folder in data/."""
    return max(int(p.name.split("_")[1]) for p in DATA.glob("Week_*"))
