# 서울 지하철 일별 승하차 총승객수 집계 스크립트
# 사용법: uv run --with pandas,requests python build-subway-daily.py
# 출처: 서울 열린데이터광장 OA-12914 (월별 CSV 직접 다운로드, 인증키 불필요)

import io
import re

import pandas as pd
import requests

START, END = "2023-08", "2026-07"  # 집계 구간 (월)
# 관측된 기준점: seq 156 = 2026-07. 월별 파일이 한 달에 하나씩 늘므로
# seq = 156 + (해당 월 - 2026-07의 개월 차). 새 달이 올라와도 기준점은 유효하다.
BASE_SEQ, BASE_MONTH = 156, pd.Period("2026-07", "M")
URL = "https://datafile.seoul.go.kr/bigfile/iot/inf/nio_download.do?&useCache=false"

frames = []
for month in pd.period_range(START, END, freq="M"):
    seq = BASE_SEQ + (month - BASE_MONTH).n
    r = requests.post(URL, data={"infId": "OA-12914", "seq": seq, "infSeq": 3}, timeout=90)
    fname = re.search(r'filename="([^"]+)"', r.headers.get("Content-Disposition", ""))
    expected = f"CARD_SUBWAY_MONTH_{month.strftime('%Y%m')}.csv"
    assert fname and fname.group(1) == expected, f"seq {seq}: {fname} != {expected}"
    for enc in ("utf-8-sig", "cp949"):  # 월에 따라 인코딩이 섞여 있다
        try:
            df = pd.read_csv(io.BytesIO(r.content), encoding=enc,
                             index_col=False,  # 행 끝 잉여 쉼표로 인한 열 밀림 방지
                             dtype={"사용일자": str})
            break
        except UnicodeDecodeError:
            continue
    df = df[["사용일자", "승차총승객수", "하차총승객수"]]
    df.columns = ["date", "ride", "alight"]
    assert df["date"].str.fullmatch(r"\d{8}").all()
    frames.append(df)
    print(expected, len(df), "rows")

raw = pd.concat(frames)
daily = raw.groupby("date").agg(ride_total=("ride", "sum"), alight_total=("alight", "sum"))
daily.index = pd.to_datetime(daily.index, format="%Y%m%d")
daily = daily.sort_index()
daily.index.name = "date"

full = pd.date_range(f"{START}-01", pd.Period(END).end_time.date())
assert len(full.difference(daily.index)) == 0, "빠진 날짜가 있다"
daily.to_csv("seoul-subway-daily.csv")
print("saved seoul-subway-daily.csv:", len(daily), "days,",
      daily.index.min().date(), "→", daily.index.max().date())
