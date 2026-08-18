# 중등 M1–M8 이론 강의 슬라이드 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 중등 과정 8개 모듈 각각에 워크시트 전 이론 강의용 Marp 슬라이드(`slides.md`)를 추가한다.

**Architecture:** 슬라이드는 새 이론을 발명하지 않고 각 모듈의 `teacher.md`(설명 대본·판서 지시)와 `worksheet.md`(개념 설명)에서 추출·재구성한다. 수업 구조는 "이론 강의(15–20분) → 활동지"가 되고, 워크시트 내 이론 설명은 복습 역할로 그대로 둔다. 스펙: `docs/superpowers/specs/2026-08-18-theory-slides-design.md`.

**Tech Stack:** Marp 마크다운, `npx @marp-team/marp-cli` (렌더링 검증), matplotlib + `data/seoul-temp-daily.csv` (그래프 PNG 생성).

## Global Constraints

- 덱 분량: 모듈당 12–18장, 강의 15–20분.
- **스포일러 규칙**: 슬라이드는 개념·용어·계산 절차·읽는 법까지만. worksheet의 Q번호 답(구체 수치, 해석 결론)은 싣지 않는다. 판단 기준 — 그 내용이 worksheet Q의 답이면 금지, Q를 풀기 위한 도구면 허용.
- 덱 구성 순서(모든 모듈 공통): ① 지난 모듈 연결 1장(M1은 과정 소개로 대체) → ② 오늘의 목표 1장 → ③ 그날의 이론 전체(개념 정의, 용어, 계산 방법, teacher.md의 판서 도식) → ④ 마지막 장 "이제 활동지로" 전환.
- 모든 slides.md는 아래 front-matter로 시작한다:

  ```markdown
  ---
  marp: true
  paginate: true
  theme: default
  style: |
    section { font-size: 28px; }
  ---
  ```

- 문체: worksheet.md와 같은 한국어 평서체("계산한다", "~라고 한다"). 중학생 대상 어휘.
- 범위 표기는 물결표 대신 en-dash 사용 (예: 12–18장). 한 문단에 `~` 2개가 들어가면 마크다운 취소선으로 깨진다.
- 생성된 pptx/pdf 바이너리는 커밋하지 않는다 (.gitignore 처리, Task 1).
- 그래프 이미지는 꼭 필요한 슬라이드만: `courses/middle/tools/slide_images.py` 하나에 모듈별 함수를 추가하고, 출력은 각 모듈 폴더 `img/*.png`. PNG는 커밋한다. 텍스트·마크다운 표로 충분하면 이미지 없이 간다.
- 렌더링 검증 명령(공통): `npx -y @marp-team/marp-cli <모듈>/slides.md -o /tmp/slides-check.html` — exit 0이면 통과.
- 커밋 메시지: `feat: M<N> 이론 슬라이드` 형식.

---

### Task 1: 인프라 — .gitignore, README, 렌더링 도구 확인

**Files:**
- Create: `.gitignore`
- Modify: `courses/middle/README.md` (파일 구성 표, 36–43행 부근)

**Interfaces:**
- Produces: 이후 모든 태스크가 쓰는 렌더링 검증 명령과 5파일 표준 문서화.

- [ ] **Step 1: .gitignore 작성**

```
*.pptx
*.pdf
```

- [ ] **Step 2: marp CLI 동작 확인 (스모크 테스트)**

임시 파일로 html·pptx 렌더링이 되는지 1회 확인:

```bash
printf -- '---\nmarp: true\n---\n\n# 테스트\n' > /tmp/marp-smoke.md
npx -y @marp-team/marp-cli /tmp/marp-smoke.md -o /tmp/marp-smoke.html
npx -y @marp-team/marp-cli /tmp/marp-smoke.md -o /tmp/marp-smoke.pptx
```

Expected: 두 명령 모두 exit 0. pptx 실패 시(Chrome 미탐지) 원인만 기록하고 진행 — 이후 태스크 검증은 html로 충분.

- [ ] **Step 3: 중등 README 갱신**

`courses/middle/README.md`의 "파일 구성 (모듈당 4개)" 표를 5개로 바꾸고 slides.md 행 추가:

```markdown
## 파일 구성 (모듈당 5개)

| 파일 | 용도 |
|---|---|
| `slides.md` | 워크시트 전에 진행하는 이론 강의 슬라이드 (Marp) |
| `teacher.md` | 강의자 노트 — 분 단위 흐름, 설명 대본, 예상 질문, 심화 |
| `worksheet.md` | 학생 배포용 활동지 (정답 없음, 인쇄 가능) |
| `practice.md` | 강의자가 수업 전에 학습자 입장으로 직접 해보는 과제 |
| `answers.md` | worksheet·practice 정답과 완성 예시 |

슬라이드 렌더링: `npx -y @marp-team/marp-cli modules/<모듈>/slides.md -o slides.pptx`
(pptx·pdf는 커밋하지 않는다)
```

- [ ] **Step 4: 커밋**

```bash
git add .gitignore courses/middle/README.md
git commit -m "chore: slides.md 표준 구성 준비 — .gitignore, 중등 README 갱신"
```

---

### Task 2: M1 시간이 담긴 데이터 — slides.md

**Files:**
- Create: `courses/middle/modules/01-time-data/slides.md`
- Create: `courses/middle/tools/slide_images.py` (m1 함수)
- Create: `courses/middle/modules/01-time-data/img/temp-line.png`

**Interfaces:**
- Consumes: Task 1의 front-matter·렌더링 명령.
- Produces: `slide_images.py`의 함수-당-모듈 패턴 (이후 태스크가 함수를 추가).

- [ ] **Step 1: 소스 읽기**

`01-time-data/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽는다. teacher.md의 설명 대본·판서 지시에서 슬라이드로 옮길 도식·비유를 추리고, answers.md에서 "슬라이드에 실으면 안 되는 답 목록"을 뽑아 둔다.

- [ ] **Step 2: 이미지 스크립트 작성 및 실행**

`courses/middle/tools/slide_images.py`를 만든다. 구조:

```python
"""중등 slides.md용 그래프 PNG 생성. 실행: python slide_images.py [m1 m3 ...]"""
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

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
```

주의: 실제 컬럼명은 `data/seoul-temp-daily.csv` 헤더를 확인해 맞춘다. 한글 제목이 깨지면 `plt.rcParams["font.family"] = "AppleGothic"`을 추가한다. 실행: `python courses/middle/tools/slide_images.py m1` → `img/temp-line.png` 생성 확인.

- [ ] **Step 3: slides.md 작성**

Global Constraints의 front-matter·덱 구성 순서를 따른다. M1 내용 뼈대 (실제 문구·도식은 Step 1에서 읽은 teacher.md 기준으로 조정):

1. 표지 — "M1. 시간이 담긴 데이터"
2. 과정 소개 — 8모듈 지도에서 오늘 위치
3. 오늘의 목표 — 시계열이 뭔지 알고, 꺾은선 그래프를 읽고 그린다
4. 데이터란 무엇인가 (teacher.md 도입 대본)
5. "시간이 담긴" 데이터 — 순서가 의미를 갖는 데이터
6. 시계열(time series) 정의
7. 시계열인 것 / 아닌 것 예시
8. 꺾은선 그래프 해부 — 축, 눈금, 점, 선 (판서 도식)
9. 그래프 읽는 법 — 오르내림, 최고·최저
10. `img/temp-line.png` — 오늘 다룰 서울 기온 데이터
11. 그래프 그리는 법 — 순서 (축 → 눈금 → 점 → 잇기)
12. 이제 활동지로 — 오늘 할 일 요약

- [ ] **Step 4: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/01-time-data/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 5: 스포일러 검증**

Step 1에서 뽑은 answers.md 답 목록(수치·결론 문장)을 slides.md와 대조 — 하나라도 슬라이드에 있으면 제거한다.

- [ ] **Step 6: 커밋**

```bash
git add courses/middle/modules/01-time-data/slides.md courses/middle/modules/01-time-data/img/ courses/middle/tools/slide_images.py
git commit -m "feat: M1 이론 슬라이드"
```

---

### Task 3: M2 평균의 힘과 함정 — slides.md

**Files:**
- Create: `courses/middle/modules/02-averages/slides.md`

**Interfaces:**
- Consumes: Task 1 front-matter, Task 2의 `slide_images.py` 패턴(이미지가 필요하다고 판단될 때만 `m2()` 함수 추가).

- [ ] **Step 1: 소스 읽기**

`02-averages/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고, 답 목록(스포일러 금지 목록)을 뽑는다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지난 시간(M1) 연결 ② 오늘의 목표 ③ 평균 정의·계산 절차 ④ 중앙값 정의·찾는 절차 ⑤ 이상치(outlier)란 ⑥ 이상치가 평균을 끄는 원리(teacher.md 판서 도식 — worksheet 문제와 **다른 예시 숫자** 사용) ⑦ 평균 vs 중앙값 언제 뭘 쓰나 ⑧ 활동지로 전환. 12–18장 범위 준수. 이상치 도식은 마크다운 표·텍스트로 충분하면 이미지 없이 간다.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/02-averages/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러 검증**

answers.md 답 목록과 slides.md 대조, 발견 시 제거.

- [ ] **Step 5: 커밋**

```bash
git add courses/middle/modules/02-averages/slides.md
git commit -m "feat: M2 이론 슬라이드"
```

---

### Task 4: M3 추세 찾기 — 이동평균 — slides.md

**Files:**
- Create: `courses/middle/modules/03-moving-average/slides.md`
- Modify: `courses/middle/tools/slide_images.py` (`m3()` 추가)
- Create: `courses/middle/modules/03-moving-average/img/ma-overlay.png`

**Interfaces:**
- Consumes: Task 2의 `slide_images.py` — `load()` 재사용, `m3()` 함수 추가.

- [ ] **Step 1: 소스 읽기**

`03-moving-average/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고 답 목록을 뽑는다.

- [ ] **Step 2: 이미지 생성**

`slide_images.py`에 `m3()` 추가 — 원본 기온과 이동평균(worksheet가 쓰는 창 크기와 동일)을 겹친 그래프를 `03-moving-average/img/ma-overlay.png`로 저장:

```python
def m3():
    df = load()
    out = MODULES / "03-moving-average" / "img"
    out.mkdir(exist_ok=True)
    t = df["temp_avg"]
    fig, ax = plt.subplots(figsize=(10, 4))
    t.plot(ax=ax, alpha=0.4, label="하루하루")
    t.rolling(7).mean().plot(ax=ax, label="이동평균")
    ax.set_ylabel("°C")
    ax.legend()
    fig.savefig(out / "ma-overlay.png", dpi=150, bbox_inches="tight")
```

창 크기 7은 worksheet.md가 실제로 쓰는 값으로 맞춘다. 실행: `python courses/middle/tools/slide_images.py m3`.

- [ ] **Step 3: slides.md 작성**

내용 뼈대: ① 지난 시간(M2 — 평균) 연결 ② 오늘의 목표 ③ 잡음과 추세 — 출렁임 속에 숨은 흐름 ④ 창(window) 개념 ⑤ 이동평균 계산 절차 — 창을 하루씩 밀며 평균 (worksheet와 **다른 예시 숫자**로 시연) ⑥ 창 크기가 하는 일 ⑦ `img/ma-overlay.png` — 겹쳐 보면 드러나는 추세 ⑧ 스프레드시트에서 하는 법(AVERAGE 끌어 복사) ⑨ 활동지로 전환.

- [ ] **Step 4: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/03-moving-average/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 5: 스포일러 검증**

answers.md 답 목록과 대조, 발견 시 제거.

- [ ] **Step 6: 커밋**

```bash
git add courses/middle/modules/03-moving-average/slides.md courses/middle/modules/03-moving-average/img/ courses/middle/tools/slide_images.py
git commit -m "feat: M3 이론 슬라이드"
```

---

### Task 5: M4 반복되는 패턴 — 계절성 — slides.md

**Files:**
- Create: `courses/middle/modules/04-seasonality/slides.md`
- Modify: `courses/middle/tools/slide_images.py` (`m4()` 추가)
- Create: `courses/middle/modules/04-seasonality/img/monthly-mean.png`

**Interfaces:**
- Consumes: `slide_images.py`의 `load()`.

- [ ] **Step 1: 소스 읽기**

`04-seasonality/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고 답 목록을 뽑는다.

- [ ] **Step 2: 이미지 생성**

`slide_images.py`에 `m4()` 추가 — 월별 평균기온 그래프를 `04-seasonality/img/monthly-mean.png`로 저장:

```python
def m4():
    df = load()
    out = MODULES / "04-seasonality" / "img"
    out.mkdir(exist_ok=True)
    monthly = df["temp_avg"].groupby(df.index.month).mean()
    fig, ax = plt.subplots(figsize=(10, 4))
    monthly.plot(ax=ax, marker="o")
    ax.set_xlabel("월")
    ax.set_ylabel("°C")
    fig.savefig(out / "monthly-mean.png", dpi=150, bbox_inches="tight")
```

단, worksheet Q가 "월별 평균을 직접 구하라"는 문제라면 이 그래프가 답 스포일러가 된다 — 그 경우 월별 그래프 대신 "계절성이 있는 다른 데이터" 예시(예: 시간대별 그래프 개형을 손그림식 도식으로)로 대체하고 PNG는 만들지 않는다. Step 1에서 판단.

- [ ] **Step 3: slides.md 작성**

내용 뼈대: ① 지난 시간(M3 — 추세) 연결 ② 오늘의 목표 ③ 추세 말고 또 하나의 패턴 — 반복 ④ 계절성(seasonality) 정의 ⑤ 계절성인 것 / 아닌 것 예시 ⑥ 월별/요일별로 묶어 평균 내기 — 아이디어 ⑦ 피벗 테이블이란 — 묶고 요약하는 표 ⑧ 활동지로 전환.

- [ ] **Step 4: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/04-seasonality/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 5: 스포일러 검증**

answers.md 답 목록과 대조, 발견 시 제거 (Step 2의 그래프 판단 포함).

- [ ] **Step 6: 커밋**

```bash
git add courses/middle/modules/04-seasonality/slides.md courses/middle/tools/slide_images.py
git add courses/middle/modules/04-seasonality/img/ 2>/dev/null || true
git commit -m "feat: M4 이론 슬라이드"
```

---

### Task 6: M5 첫 예측 — slides.md

**Files:**
- Create: `courses/middle/modules/05-first-forecast/slides.md`

**Interfaces:**
- Consumes: Task 1 front-matter. 이미지가 필요하면 `slide_images.py`에 `m5()` 추가 (Step 1에서 판단).

- [ ] **Step 1: 소스 읽기**

`05-first-forecast/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고 답 목록을 뽑는다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지난 시간(M4 — 계절성) 연결, "이제 패턴을 알았으니 내일을 말해 보자" ② 오늘의 목표 ③ 예측이란 — 어제까지의 데이터로 내일을 말하기 ④ naive 예측 — "내일은 오늘과 같다" ⑤ 이동평균 예측 — "내일은 최근 며칠의 평균" ⑥ 오차 — 실제 빼기 예측, 부호와 크기 ⑦ 좋은 예측이란 — 오차가 작은 예측 ⑧ 활동지로 전환. 예측 시연은 worksheet와 **다른 예시 숫자** 사용.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/05-first-forecast/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러 검증**

answers.md 답 목록과 대조 — 특히 "어느 예측법의 오차가 더 작은가"류 결론은 worksheet의 핵심 발견이므로 슬라이드에 싣지 않는다.

- [ ] **Step 5: 커밋**

```bash
git add courses/middle/modules/05-first-forecast/slides.md
git commit -m "feat: M5 이론 슬라이드"
```

---

### Task 7: M6 파이썬으로 다시 보기 — slides.md

**Files:**
- Create: `courses/middle/modules/06-python-revisit/slides.md`

**Interfaces:**
- Consumes: Task 1 front-matter. 코드 블록 위주 — 이미지 불필요.

- [ ] **Step 1: 소스 읽기**

`06-python-revisit/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고 답 목록을 뽑는다. worksheet가 쓰는 실제 코드(URL, 변수명)를 그대로 슬라이드에 옮긴다 — 코드가 다르면 학생이 혼란.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지난 시간까지(1부 — 스프레드시트) 정리 ② 오늘의 목표 — 같은 일을 파이썬으로 ③ 왜 파이썬인가 — 1,000일도 한 줄 ④ Colab이란 — 설치 없는 파이썬 공책 ⑤ 셀 실행 방법 (Shift+Enter) ⑥ pandas란 ⑦ CSV 읽기 코드 — 한 줄씩 읽는 법 (worksheet 코드 그대로) ⑧ 에러를 만나면 — 에러는 정상, 읽는 법 ⑨ 활동지로 전환.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/06-python-revisit/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러 검증**

answers.md 답 목록과 대조, 발견 시 제거.

- [ ] **Step 5: 커밋**

```bash
git add courses/middle/modules/06-python-revisit/slides.md
git commit -m "feat: M6 이론 슬라이드"
```

---

### Task 8: M7 pandas 시계열 도구 — slides.md

**Files:**
- Create: `courses/middle/modules/07-pandas-tools/slides.md`

**Interfaces:**
- Consumes: Task 1 front-matter. 코드 블록 위주 — 이미지 불필요.

- [ ] **Step 1: 소스 읽기**

`07-pandas-tools/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽고 답 목록을 뽑는다. worksheet의 실제 코드·인자값을 그대로 사용한다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지난 시간(M6) 연결 ② 오늘의 목표 ③ 날짜 인덱스 — 날짜가 이름표가 되면 생기는 힘 ④ 날짜로 잘라 보기(슬라이싱) 읽는 법 ⑤ resample — 하루를 월로 묶기, 읽는 법 ⑥ rolling — M3의 이동평균을 한 줄로, 읽는 법 ⑦ NaN — 값 없음은 에러가 아니라 표시 ⑧ 결측치 다루는 선택지 ⑨ 활동지로 전환.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/07-pandas-tools/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러 검증**

answers.md 답 목록과 대조, 발견 시 제거.

- [ ] **Step 5: 커밋**

```bash
git add courses/middle/modules/07-pandas-tools/slides.md
git commit -m "feat: M7 이론 슬라이드"
```

---

### Task 9: M8 미니 프로젝트 — slides.md

**Files:**
- Create: `courses/middle/modules/08-mini-project/slides.md`

**Interfaces:**
- Consumes: Task 1 front-matter. 이미지 불필요.

- [ ] **Step 1: 소스 읽기**

`08-mini-project/`의 `teacher.md`, `worksheet.md`, `answers.md`를 읽는다. 프로젝트 모듈이라 "답"보다 절차·기준이 중심 — 스포일러 목록은 짧을 수 있다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지금까지 배운 것 한 장 정리 (M1–M7 지도) ② 오늘의 목표 — 내 데이터로 처음부터 끝까지 ③ 프로젝트 절차 — 수집 → 분석 → 예측 → 발표 ④ 데이터 고르는 기준 ⑤ 데이터 후보 (README의 후보 목록) ⑥ 분석에서 할 일 체크리스트 (M1–M5 도구 대응) ⑦ 발표 틀 — 무엇을 말하면 되나 ⑧ 활동지로 전환.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/middle/modules/08-mini-project/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러 검증**

answers.md 답 목록과 대조, 발견 시 제거.

- [ ] **Step 5: 커밋**

```bash
git add courses/middle/modules/08-mini-project/slides.md
git commit -m "feat: M8 이론 슬라이드"
```

---

## 완료 기준

- 8개 모듈 모두 `slides.md` 존재, marp 렌더링 exit 0.
- 각 slides.md 12–18장, 덱 구성 순서 준수.
- answers.md 대조에서 스포일러 0건.
- `courses/middle/README.md`가 5파일 구성과 렌더링 명령을 안내.
