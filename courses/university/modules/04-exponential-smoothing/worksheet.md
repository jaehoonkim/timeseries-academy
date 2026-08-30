# U4. 지수평활 가족 — ETS — 활동지

이름: ____________

U3의 마지막 판독은 "직접 정보는 사실상 어제뿐 — 어제를 중심으로
**배합**하는 모형이 자연스럽다"였다. 오늘 그 생각을 정식 모형으로
만든 가족을 만난다: **지수평활**(exponential smoothing) 가족,
통칭 **ETS**다.

어려운 이름이니 먼저 풀자. **평활**은 "들쭉날쭉한 것을 평평하고
매끄럽게 고른다"는 뜻 — U2에서 rolling 평균으로 이미 해 본 그
일이다. **지수**는 배합의 기억이 과거로 갈수록 **같은 비율로
계속 옅어진다**는 뜻이다(α=0.3이면 오늘 무게 0.30, 어제 0.21,
그제 0.147 — 매일 0.7배씩, 지수함수의 모양). 합치면 "옅어지는
무게로 과거를 평균해 매끄러운 값을 만들고, **그 값을 내일의
예측으로 쓰는**" 방법이다. rolling과의 차이는 무게뿐이다 —
rolling은 창 안 며칠에게 균등, 지수평활은 모든 과거에게 멀수록
옅게.

이 가족은 수준·추세·계절이라는 **부품**을 하나씩 끼우며
조립한다.

그리고 오늘, 이 과정에서 처음으로 **미래를 예측**하고 U1에서 세운
벽과 대결한다.

준비는 지금까지와 같고, 마지막에 한 가지가 붙는다 — 읽는 법:

> `.asfreq("D")`
> = 이 시계열의 간격이 **하루**(D)라고 표에 명시하라 — 오늘 쓰는
> statsmodels 모형들이 요구하는 신고식이다 (안 하면 경고가 뜬다)

```python
!pip install -q koreanize-matplotlib
import koreanize_matplotlib
```

```python
import pandas as pd

base = "https://raw.githubusercontent.com/jaehoonkim/timeseries-academy/main/data/"
t = pd.read_csv(base + "seoul-temp-daily.csv",
                parse_dates=["date"], index_col="date")["temp_avg"].asfreq("D")
s = pd.read_csv(base + "seoul-subway-daily.csv",
                parse_dates=["date"], index_col="date")["ride_total"].asfreq("D")

train_t, test_t = t[:"2025-07-31"], t["2025-08-01":]
train_s, test_s = s[:"2025-07-31"], s["2025-08-01":]
```

## 1. 배합이라는 생각 — SES

가장 단순한 지수평활 **SES**(simple exponential smoothing)의
식은 한 줄이다:

> 내일의 예측 = **α × 오늘의 관측 + (1 − α) × 오늘의 예측**

즉 "**새 소식 α + 기억 (1 − α)**"의 **배합**이다. 배합은 요리의
그 일상어 — 재료를 비율대로 섞는 것 — 이고, 정식 용어로는
**가중 평균**(weighted average)이다: 무게의 합이 1이 되게 섞는
평균. SES는 '오늘의 관측'과 '오늘의 예측' 두 재료를 α : (1−α)로
섞는 가중 평균이다.

오늘의 예측 안에는 어제의 배합이, 그 안에는 그제의 배합이 들어
있어서 — 과거가 멀수록 기하급수로 옅어지는 기억이 된다(이름의
'지수'가 여기서 온다).

α를 얼마로 할까? **데이터가 정하게 한다** — 훈련 구간에서 오차가
가장 작아지는 α를 찾는 것이 fit이다. 읽는 법:

> `SimpleExpSmoothing(train_t, initialization_method="estimated")`
> = 훈련 데이터로 SES를 준비하라 (initialization_method는 "시작
> 값도 데이터에서 추정하라" — 버전에 따라 요구되는 신고식)
>
> `.fit()`
> = 최선의 배합 α를 찾아라
>
> `.params["smoothing_level"]`
> = 찾은 α를 보여 달라

```python
from statsmodels.tsa.holtwinters import SimpleExpSmoothing

ses = SimpleExpSmoothing(train_t, initialization_method="estimated").fit()
alpha = ses.params["smoothing_level"]
round(alpha, 3)
```

**Q1.** 기온의 최적 α = ______. 식에 넣어 보자 — α가 이 값이면
SES의 예측은 정확히 무엇이 되는가? U1에서 만난 어떤 선수인가?

답: ____________

fit이 훈련 구간(앞 2년)의 데이터만 보고 찾아낸 최선의 배합이
이것이다 — **사람이 아니라 데이터가 고른 답이 naive**라는 뜻이다.
U1의 벽이 왜 그리 높았는지, U3의 "직접 정보는 어제뿐"이 왜 그
그림이었는지가 모형의 언어로 한 번에 설명된다.

## 2. 하루 앞 채점 — 배운 배합으로 시험을

U1의 벽과 공정하게 겨루려면 같은 시험이어야 한다: **시험 구간을
하루 앞씩** 예측한다. 요령은 회귀의 fit/predict와 같은 생각이다 —
배합은 훈련에서만 배우고, 그 배합을 그대로 들고 시험을 친다:

> `SimpleExpSmoothing(t, ...).fit(smoothing_level=alpha, optimized=False)`
> = 전체 기간에 SES를 놓되, **배합은 새로 배우지 말고**(optimized
> =False) 훈련이 배운 α를 그대로 써라
>
> `.fittedvalues`
> = 각 날짜에 대한 **하루 앞 예측**들 — 시험 구간만 잘라 채점한다

```python
ses_all = SimpleExpSmoothing(t, initialization_method="estimated").fit(
    smoothing_level=alpha, optimized=False)
e = test_t - ses_all.fittedvalues["2025-08-01":]
round(e.abs().mean(), 2), round((e**2).mean() ** 0.5, 2)
```

train_t가 아니라 **전체 t를 주는 이유**: 하루 앞 예측은 배합의
재귀라서, 시험 기간에도 모형이 매일 "어제까지의 관측"을 받아야
다음 날 예측을 만들 수 있다. 이것은 반칙이 아니다 — naive도 시험
기간 내내 어제의 실제값을 보고 예측한다(같은 조건). 반칙은
미래를 보거나 **시험 구간으로 배합을 배우는 것**이고, 후자를
막는 자물쇠가 optimized=False다.

**Q2.** SES의 성적: MAE ______ / RMSE ______ — U1의 naive
(1.63 / 2.26)와 비교하면? Q1의 답과 앞뒤가 맞는가?

답: ____________

## 3. 부품 하나 추가 — 추세 (Holt)

Holt는 사람 이름이다 — 1950년대에 이 방법을 만든 통계학자 찰스
홀트(Charles Holt).

홀트의 모형은 부품 두 개를 각자의 배합으로 굴린다:

- **수준**(level) — "이 시계열이 **지금 어디쯤 있나**"의 매끄러운
  현재값. SES가 배합으로 굴려 온 그 값, 곧 1절의 "오늘의 예측"
  이다. 갱신 비율은 α.
- **변화량** — "하루에 얼마나 오르내리는 **중인가**"(기울기).
  홀트가 새로 끼운 부품이다. 갱신 비율은 β.

예측은 "**수준 + 변화량**" — 지금 있는 곳에서 하루치만큼 더 간
곳이다. 수준이 20도이고 요즘 하루 +0.3도씩 오르는 중이면 내일
예측은 20.3도 — naive(20도)가 못 하는 방향 반영이다.

코드는 옵션 하나 차이다. statsmodels의 이름표는 그리스 문자가
아니라서 대응만 적어 두자: α는 `"smoothing_level"`, β는
`"smoothing_trend"` — 아래 셀의 출력 (첫째, 둘째)가 곧 (α, β)다.

```python
from statsmodels.tsa.holtwinters import ExponentialSmoothing

holt = ExponentialSmoothing(train_t, trend="add",
                            initialization_method="estimated").fit()
round(holt.params["smoothing_level"], 3), round(holt.params["smoothing_trend"], 4)
```

```python
holt_all = ExponentialSmoothing(t, trend="add",
                                initialization_method="estimated").fit(
    smoothing_level=holt.params["smoothing_level"],
    smoothing_trend=holt.params["smoothing_trend"], optimized=False)
e = test_t - holt_all.fittedvalues["2025-08-01":]
round(e.abs().mean(), 2), round((e**2).mean() ** 0.5, 2)
```

**Q3.** β = ______ — 추세 부품을 얼마나 쓰는가? 성적은 ______ /
______ 로 SES보다 어떤가? U2에서 잰 기온의 추세(표준편차 0.3도,
계절의 1/36)를 떠올려 이유를 쓰자.

답: ____________ (β = 0은 fit이 추세 부품의 배합 비율을 0으로
**꺼 버렸다**는 뜻이다 — 데이터에 담을 추세가 없어서. 이런
부품을 **죽은 부품**이라 부르자. 그리고 죽은 부품은 공짜가
아니다 — 끼워 두는 것만으로 성적을 갉아먹는다)

## 4. 계절 부품 — Holt-Winters, 그리고 첫 승리

세 번째 부품은 **계절**이다 — 주기 안의 각 자리마다(요일이
주기면 월요일부터 일요일까지 일곱 칸) "**보통과 얼마나
다른가**"의 보정값을 기억하는 부품. U1에서 만든 요일 프로필의
배합 버전이라 보면 되고, 갱신 비율은 γ다.

예측은 "수준 + 변화량 + **내일 자리의 계절 보정**"이 된다.
수준이 700만인데 내일이 일요일이고 일요일 보정이 -250만이면,
내일 예측은 450만.

이 부품까지 끼우면 **Holt-Winters**다 — Winters도 사람으로,
홀트의 **제자**다. 스승의 모형에 계절 부품을 더해 이름이 나란히
붙었다. 오늘 우리가 부품을 하나씩 끼우는 순서가 실제 역사의
순서이기도 하다. 지하철에 주기 7로 조립하자:

```python
hw = ExponentialSmoothing(train_s, trend="add", seasonal="add",
                          seasonal_periods=7,
                          initialization_method="estimated").fit()
(round(hw.params["smoothing_level"], 3),
 round(hw.params["smoothing_trend"], 4),
 round(hw.params["smoothing_seasonal"], 3))
```

(출력은 순서대로 α, β, γ — 계절의 γ는 `"smoothing_seasonal"`이다)

**Q4.** 배합 세 개를 읽자 — α(수준) ______, β(추세) ______,
γ(계절) ______.

지하철은 어제를 얼마나 믿는가(α)? 기온의 α=1과 왜 다른가?
(힌트: U1 성격표의 시차 1 자기상관 — 0.98 vs 0.35)

답: ____________

γ가 0.035라는 것은 "요일 파형을 하루에 3.5%씩만 갱신한다"는 뜻 —
파형은 안정적이니 천천히만 고친다.

채점은 2절과 같은 요령이다(배합 세 개를 그대로 들고):

```python
hw_all = ExponentialSmoothing(s, trend="add", seasonal="add",
                              seasonal_periods=7,
                              initialization_method="estimated").fit(
    smoothing_level=hw.params["smoothing_level"],
    smoothing_trend=hw.params["smoothing_trend"],
    smoothing_seasonal=hw.params["smoothing_seasonal"],
    optimized=False)
e_hw = test_s - hw_all.fittedvalues["2025-08-01":]
round(e_hw.abs().mean() / 1e4, 1), round((e_hw**2).mean() ** 0.5 / 1e4, 1)
```

**Q5.** Holt-Winters의 성적 (만 명): MAE ______ / RMSE ______.
U1의 벽들(주간 naive 55.5 / 119.1, naive 118.0 / 166.5)과
비교하면?

답: ____________ — 이 과정의 **첫 벽 돌파**다.

**Q6.** 어디서 벌었고, 어디가 여전히 아픈가:

```python
e_w7 = test_s - s.shift(7)["2025-08-01":]
(pd.DataFrame({"주간naive": e_w7.abs().groupby(e_w7.index.month).mean(),
               "HW": e_hw.abs().groupby(e_hw.index.month).mean()}) / 1e4).round(0)
```

```python
e_hw.abs().nlargest(5) / 1e4
```

크게 번 달: ______ 월(161만 → 77만), ______ 월(123만 → 87만) —
공통점은? 그리고 최악의 날 다섯은 여전히 어떤 날들인가?

답: ____________ (남은 숙제의 이름은 달력이다 — U7에서 정면으로)

## 5. 기온에도 계절 부품 — 벽이 둘 다 무너진다

기온의 주기는 365다:

```python
hw_t = ExponentialSmoothing(train_t, trend="add", seasonal="add",
                            seasonal_periods=365,
                            initialization_method="estimated").fit()
hw_t_all = ExponentialSmoothing(t, trend="add", seasonal="add",
                                seasonal_periods=365,
                                initialization_method="estimated").fit(
    smoothing_level=hw_t.params["smoothing_level"],
    smoothing_trend=hw_t.params["smoothing_trend"],
    smoothing_seasonal=hw_t.params["smoothing_seasonal"],
    optimized=False)
e = test_t - hw_t_all.fittedvalues["2025-08-01":]
round(e.abs().mean(), 2), round((e**2).mean() ** 0.5, 2)
```

**Q7.** 성적: ______ / ______ — naive의 벽(1.63 / 2.26)을
넘었는가? 그런데 α를 확인하면 여전히 1.0이다. 어제를 100% 믿는
건 그대로인데 무엇이 성적을 끌어올렸을까?

답: ____________ (힌트: 계절 부품은 "내일은 오늘보다 계절적으로
이만큼 다르다"를 보태 준다 — naive가 전환점에서 하루 늦는 몫의
일부를 미리 당겨 주는 것)

## 6. 여러 걸음 — 예측에는 두 종류가 있다

지금까지는 **하루 앞**(one-step) 예측이었다 — 매일 저녁 내일
하나를 맞히는 시험. 다른 시험도 있다: 오늘 시점에서 **1년치를
한 번에** 그리는 여러 걸음(multi-step) 예측이다. `forecast`가
그 일을 한다:

```python
test_t.plot(figsize=(10, 3), label="실제", legend=True)
ses.forecast(365).plot(label="SES의 1년 예측", legend=True)
hw_t.forecast(365).plot(label="Holt-Winters의 1년 예측", legend=True);
```

**Q8.** SES의 1년 예측은 ______ 도짜리 **수평선**이다(훈련 마지막
날은 한여름이었다). 왜 얼어붙는가 — SES의 기억에는 무엇이 없나?

답: ____________

(채점까지 하면 SES의 1년 예측은 MAE 18.7도 — 하루 앞의 1.63과
같은 모형이 맞나 싶은 참사다. 같은 모형도 **시험의 종류**에 따라
성적이 전혀 다르다. Holt-Winters는 리듬을 그려서 1년 앞에서도
MAE 4.1도.)

지하철도 한 장:

```python
test_s.plot(figsize=(10, 3), label="실제", legend=True)
hw.forecast(365).plot(label="HW의 1년 예측", legend=True);
```

Holt-Winters의 1년 예측은 MAE 54.1만 — **1년 앞**인데 주간
naive의 **하루 앞** 성적(55.5만)과 맞먹는다. 계절 부품이 미래로
보낼 수 있는 리듬을 기억하고 있기 때문이다.

## 7. 생각해 보기

**Q9.** SES(=naive)의 하루 앞 오차는 U3의 언어로 **차분**이다.
U3에서 기온의 차분에 구조가 남아 있었다(시차 2의 -0.26 등) —
ETS 가족은 이 구조를 잡는 부품이 없다. "오차 자체의 무늬"를
모형 안에 넣으려면 무엇이 필요할까?

답: ____________ (다음 모듈의 주인공 — ARIMA — 이 정확히 그
부품이다)

**Q10.** 오늘 조립한 부품 세 개(수준·추세·계절)에 오차(Error)를
더한 네 글자가 이 가족의 정식 이름 **ETS**(Error·Trend·Seasonal)
다. 두 데이터에 어떤 부품 조합이 최선이었는지 표로 정리하자:

| | 수준(α) | 추세(β) | 계절(γ) | 하루 앞 성적 |
|---|---|---|---|---|
| 기온 | | | | |
| 지하철 | | | | |

오늘의 세 문장:

1. **지수평활은 배합이다** — 새 소식 α + 기억 (1−α), 그리고
   기온이 고른 최선의 배합은 α=1, naive였다.
2. **부품은 데이터가 정한다** — 죽은 부품(기온의 추세)은 비용만
   내고, 산 부품(계절)은 벽을 무너뜨린다.
3. **예측에는 두 종류가 있다** — 하루 앞과 여러 걸음. 계절 부품
   없는 모형은 먼 미래에서 얼어붙는다.
