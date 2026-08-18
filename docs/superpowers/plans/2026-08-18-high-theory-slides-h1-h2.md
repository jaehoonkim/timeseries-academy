# 고등 H1–H2 이론 강의 슬라이드 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 고등 과정의 소화 완료된 두 모듈 H1·H2에 워크시트 전 이론 강의용 Marp 슬라이드(`slides.md`)를 추가한다.

**Architecture:** 중등 M1–M8과 동일한 표준(스펙 `docs/superpowers/specs/2026-08-18-theory-slides-design.md`)을 따른다. 슬라이드는 각 모듈의 `teacher.md`·`worksheet.md`에서 추출·재구성하며, `courses/high/PROGRESS.md`의 질문 기록(강의자가 실제로 막힌 지점)을 해당 모듈 슬라이드에 반영한다. H3 이후는 강의자 소화 완료 후 별도 진행.

**Tech Stack:** Marp 마크다운, `npx @marp-team/marp-cli` (렌더링 검증).

## Global Constraints

- 덱 분량: 모듈당 12–18장, 강의 15–20분 (수업은 75분).
- **스포일러 규칙**: 슬라이드는 개념·용어·계산 절차·코드 읽는 법까지만. worksheet Q의 답(구체 수치, 해석 결론)은 싣지 않는다. 계산 시연은 워크시트와 **다른 예시 숫자** 사용.
- **코드 충실성**: 덱에 싣는 코드(URL, 변수명, 인자)는 해당 모듈 worksheet.md에서 그대로 복사하고, 워크시트의 셀 경계를 유지한다(셀 병합 금지 — 중등 M6에서 수정 라운드 발생한 전례).
- 덱 구성 순서: ① 지난 모듈 연결 1장(H1은 과정 소개로 대체) → ② 오늘의 목표 1장 → ③ 이론 전체 → ④ 마지막 장 "이제 활동지로".
- front-matter는 `courses/middle/modules/01-time-data/slides.md`의 첫 7행과 바이트 동일.
- 문체: 해당 worksheet.md와 같은 한국어 평서체, 고등학생 대상.
- 범위 표기는 en-dash. 한 문단에 `~` 2개 금지 (취소선 깨짐 — H2 질문 기록에도 있는 교훈).
- 이미지: 꼭 필요할 때만. H1·H2 모두 코드 중심이라 불필요 예상 — 특히 H2의 히스토그램·상자그림 이미지는 워크시트 발견을 스포일하므로 금지. 만들 경우 `courses/high/tools/slide_images.py` 신설.
- 렌더링 검증(공통): `npx -y @marp-team/marp-cli <모듈>/slides.md -o /tmp/slides-check.html` — exit 0.
- 커밋 메시지: `feat: H<N> 이론 슬라이드`.

---

### Task 1: 고등 README 갱신

**Files:**
- Modify: `courses/high/README.md` ("파일 구성 (모듈당 4개)" 표 부근)

**Interfaces:**
- Produces: 고등 과정 5파일 표준 문서화 (H3+는 소화 후 작성 원칙 명시).

- [ ] **Step 1: README 파일 구성 표 갱신**

"파일 구성 (모듈당 4개)"를 5개로 바꾸고 slides.md 행을 첫 행으로 추가:

```markdown
## 파일 구성 (모듈당 5개)

| 파일 | 용도 |
|---|---|
| `slides.md` | 워크시트 전에 진행하는 이론 강의 슬라이드 (Marp) — 강의자가 practice 소화를 마친 모듈부터 작성 |
| `teacher.md` | 강의자 노트 — 분 단위 흐름, 설명 대본, 토론 가이드, 예상 질문, 심화 |
| `worksheet.md` | 학생 배포용 활동지 (정답 없음, 인쇄 가능) |
| `practice.md` | 강의자가 수업 전에 학습자 입장으로 직접 해보는 과제 |
| `answers.md` | worksheet·practice 정답과 완성 예시 |

슬라이드 렌더링: `npx -y @marp-team/marp-cli modules/<모듈>/slides.md -o slides.pptx`
(pptx·pdf는 커밋하지 않는다)
```

- [ ] **Step 2: 커밋**

```bash
git add courses/high/README.md
git commit -m "docs: 고등 README 파일 구성 5개로 갱신 — slides.md 추가"
```

---

### Task 2: H1 시계열과 파이썬 — slides.md

**Files:**
- Create: `courses/high/modules/01-python-timeseries/slides.md`

**Interfaces:**
- Consumes: Global Constraints의 front-matter·렌더링 명령. 스타일 전례: `courses/middle/modules/06-python-revisit/slides.md` (코드 중심 덱).

- [ ] **Step 1: 소스 읽기**

`01-python-timeseries/`의 `teacher.md`, `worksheet.md`, `answers.md`와 `courses/high/PROGRESS.md`의 H1 질문 기록을 읽는다. answers.md에서 스포일러 금지 목록을 뽑고, worksheet의 코드 셀(URL·변수명·경계)을 그대로 추린다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대 (실제 문구는 teacher.md 기준으로 조정): ① 과정 소개 — 8모듈 지도(고등 README 표 제목 그대로)와 서사 축 ② 오늘의 목표 ③ 시계열이란 — 정의, 순서가 의미를 갖는 데이터 ④ 시계열인 것/아닌 것 ⑤ Colab이란 — 설치 없는 파이썬, 셀 실행 ⑥ pandas와 CSV 읽기 코드 — 한 줄씩 읽는 법 (worksheet 코드 그대로) ⑦ 날짜 인덱스 — 날짜가 이름표가 되는 것, **loc 읽는 법(질문 기록 반영: 이름표로 행 찾기, 열 선택과 대비, 부분 날짜)** ⑧ 그래프 그리기 코드 읽는 법 ⑨ 에러를 만나면 ⑩ 활동지로 전환.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/high/modules/01-python-timeseries/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러·코드 충실성 검증**

answers.md 답 목록과 대조해 제거. 덱의 코드 블록을 worksheet와 문자 단위로 대조.

- [ ] **Step 5: 커밋**

```bash
git add courses/high/modules/01-python-timeseries/slides.md
git commit -m "feat: H1 이론 슬라이드"
```

---

### Task 3: H2 분포로 보는 시계열 — slides.md

**Files:**
- Create: `courses/high/modules/02-distribution/slides.md`

**Interfaces:**
- Consumes: Task 2와 동일 전례. H1 슬라이드가 이미 존재(지난 모듈 연결 장에서 참조).

- [ ] **Step 1: 소스 읽기**

`02-distribution/`의 `teacher.md`, `worksheet.md`, `answers.md`와 `courses/high/PROGRESS.md`의 H2 질문 기록 3건(히스토그램 봉우리, z-점수 비유, 물결표)을 읽는다. 스포일러 금지 목록과 worksheet 코드 셀을 추린다.

- [ ] **Step 2: slides.md 작성**

내용 뼈대: ① 지난 모듈(H1) 연결 ② 오늘의 목표 ③ 분포로 본다는 것 — 시간축을 접고 값의 퍼짐을 보기 ④ 평균 복습과 표준편차 — 정의·계산 절차 (워크시트와 다른 예시 숫자) ⑤ 히스토그램 읽는 법 — bins 개념, **bins 나누기에 따라 잔봉우리가 생길 수 있음(질문 기록 반영, 단 워크시트의 "봉우리 2개" 답 자체는 금지)** ⑥ 상자그림 읽는 법 — 다섯 숫자 요약 ⑦ z-점수 — **"거리 ÷ 보폭 = 걸음 수" 비유(질문 기록 반영)**, 빼기→나누기 두 단계 손 계산(다른 예시 숫자) ⑧ z-점수로 이상치 탐지 아이디어 ⑨ 관련 코드 읽는 법 (worksheet 코드 그대로, 셀 경계 유지) ⑩ 활동지로 전환. 히스토그램·상자그림 그림(이미지)은 넣지 않는다 — 모양 자체가 워크시트의 발견.

- [ ] **Step 3: 렌더링 검증**

```bash
npx -y @marp-team/marp-cli courses/high/modules/02-distribution/slides.md -o /tmp/slides-check.html
```

Expected: exit 0.

- [ ] **Step 4: 스포일러·코드 충실성 검증**

answers.md 답 목록과 대조해 제거. 코드 블록을 worksheet와 문자 단위로 대조. `~` 2개 이상인 문단이 없는지 확인.

- [ ] **Step 5: 커밋**

```bash
git add courses/high/modules/02-distribution/slides.md
git commit -m "feat: H2 이론 슬라이드"
```

---

## 완료 기준

- H1·H2 `slides.md` 존재, marp 렌더링 exit 0, 각 12–18장, 덱 구성 순서 준수.
- answers.md 대조 스포일러 0건, 코드 블록 워크시트와 일치(셀 경계 포함).
- PROGRESS.md 질문 기록이 해당 슬라이드에 반영됨.
- `courses/high/README.md`가 5파일 구성과 작성 시점 원칙을 안내.
