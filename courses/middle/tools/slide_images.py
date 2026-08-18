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
    # ponytail: 14일 미리보기만 표시 — 전체 3년을 그리면 계절 파형이 보여
    # worksheet Q5(반복되는 물결 모양)의 답을 미리 스포일링한다.
    df["temp_avg"].head(14).plot(ax=ax, marker="o")
    ax.set_ylabel("°C")
    ax.set_title("서울 하루 평균기온 (14일 미리보기)")
    fig.savefig(out / "temp-line.png", dpi=150, bbox_inches="tight")


def m3():
    df = load()
    out = MODULES / "03-moving-average" / "img"
    out.mkdir(exist_ok=True)
    # ponytail: 2024년 봄 90일만 크롭 — 전체 3년을 그리면 7일 창으로도
    # 계절 물결이 보여 Q6~Q8(창 크기 실험) 방향을 암시하고, 2023년 8월
    # (태풍 카눈, Q5)·10월(손 계산 주간, Q1~Q3)을 포함하면 그래프에서
    # 답을 읽어낼 수 있어 두 구간을 모두 피한 다른 시기를 쓴다.
    t = df.loc["2024-02-01":"2024-04-30", "temp_avg"]
    fig, ax = plt.subplots(figsize=(10, 4))
    t.plot(ax=ax, alpha=0.4, label="하루하루")
    t.rolling(7).mean().plot(ax=ax, label="7일 이동평균")
    ax.set_ylabel("°C")
    ax.set_title("서울 하루 평균기온 — 2024년 봄 90일")
    ax.legend()
    fig.savefig(out / "ma-overlay.png", dpi=150, bbox_inches="tight")


if __name__ == "__main__":
    for name in sys.argv[1:] or ["m1"]:
        globals()[name]()
