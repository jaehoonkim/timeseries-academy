"""중등 slides.md용 그래프 PNG 생성. 실행: python slide_images.py [m1 m3 ...]"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["font.family"] = "AppleGothic"
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).resolve().parents[3]
MODULES = ROOT / "courses" / "middle" / "modules"


def load():
    return pd.read_csv(
        ROOT / "data" / "seoul-temp-daily.csv",
        parse_dates=["date"], index_col="date",
    )


def m1():
    df = load()
    out = MODULES / "01-time-data" / "img"
    out.mkdir(exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4))
    df["temp_avg"].plot(ax=ax)
    ax.set_ylabel("°C")
    ax.set_title("서울 하루 평균기온")
    fig.savefig(out / "temp-line.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    for name in sys.argv[1:] or ["m1"]:
        globals()[name]()
