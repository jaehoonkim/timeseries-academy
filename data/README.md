# 공유 실습 데이터

## seoul-temp-daily.csv

서울 일별 기온, 2023-08-01 ~ 2026-07-31 (1,096일, 결측 없음).

| 열 | 의미 |
|---|---|
| `date` | 날짜 (YYYY-MM-DD) |
| `temp_avg` | 일평균 기온 (°C) |
| `temp_max` | 일최고 기온 (°C) |
| `temp_min` | 일최저 기온 (°C) |

### 출처

[Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api)
(ERA5 재분석, 서울 시청 좌표 37.5665, 126.978). 회원가입·인증키 없이 받을 수 있는
실제 관측 기반 공공 데이터라 이 소스를 사용했다.

갱신(기간 변경 포함):

```bash
curl -s "https://archive-api.open-meteo.com/v1/archive?latitude=37.5665&longitude=126.978&start_date=2023-08-01&end_date=2026-07-31&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&timezone=Asia%2FSeoul&format=csv"
```

받은 파일 상단 메타 3줄을 지우고 열 이름을 `date,temp_avg,temp_max,temp_min`으로
바꾸면 같은 형식이 된다.

### 기상청 공식 데이터로 교체하려면

수업에서 "기상청 서울 관측값"이라고 말하고 싶다면
[기상자료개방포털](https://data.kma.go.kr) → 기후통계분석 → 기온분석에서
서울(108) 일자료 CSV를 내려받아 열 이름만 위 형식으로 맞춰 교체하면 된다.
(로그인 필요. 관측 지점 데이터라 값이 소수점 수준에서 다를 수 있으나 수업 내용에는 영향 없음.)
