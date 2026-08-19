# M6. 파이썬으로 다시 보기 — 강의자 사전 실습

## 1. 워크시트 전체 수행 (약 40분)

[worksheet.md](worksheet.md)를 학생처럼 Colab에서 순서대로 실행한다.
그리고 **일부러 에러를 내 본다** — 수업 시간의 절반은 에러 대응이다:

- import/read_csv 셀을 실행하지 않은 새 노트북에서 `df`를 실행 →
  `NameError` 메시지를 읽어 본다.
- 따옴표 하나를 지우고 실행 → `SyntaxError`의 화살표(^)가 어디를
  가리키는지 본다.
- 런타임 → 세션 다시 시작 후 마지막 셀만 실행 → 같은 NameError.
  "모두 실행"으로 복구해 본다.

## 2. 추가 실습 — 학생보다 한 발 더 (약 20분)

1. **M4 재현 — 월별 평균이 한 줄**:

   ```python
   df.groupby(df["date"].dt.month)["temp_avg"].mean()
   ```

   M4에서 피벗 테이블로 만든 월별 평균표(1월 -3.2 ~ 8월 26.7)와
   일치하는지 확인한다. `.dt.month`가 `=MONTH(A2)` 열의 역할이다.
2. **M5 재현 — 예측 대결이 네 줄**:

   ```python
   pred_naive = df["temp_avg"].shift(1)
   pred_ma7 = df["temp_avg"].rolling(window=7).mean().shift(1)
   print((pred_naive - df["temp_avg"]).abs().tail(31).mean())
   print((pred_ma7 - df["temp_avg"]).abs().tail(31).mean())
   ```

   M5의 결승전 스코어 1.02 vs 1.26이 재현되는지 확인한다.
   `shift(1)`이 "한 행 아래로 밀기" — M5에서 `=B1066`을 E1067에
   쓴 것과 같은 일이다.
3. 두 재현의 결과를 보고, 수업 중 빠른 학생에게 줄 심화 과제로
   어느 쪽이 적당할지 정해 둔다.

## 3. 셀프 체크

- [ ] Q1~Q10에 스스로 답했다
- [ ] NameError와 SyntaxError를 일부러 내고 메시지를 읽어 봤다
- [ ] 통계 4종(12.71 / 13.60 / 32.8 / -12.3)을 재현했다
- [ ] 7월 평균·중앙값이 M2와 일치(26.1 / 25.8)하는 것을 확인했다
- [ ] ma365 그래프에서 완만한 오르막을 다시 찾았다
- [ ] groupby 월별 평균이 M4 피벗과 일치하는 것을 확인했다
- [ ] shift(1) 예측 대결이 M5 결과(1.02 / 1.26)와 일치하는 것을 확인했다
- [ ] 막힌 지점을 PROGRESS.md 질문 기록에 남겼다

끝나면 [answers.md](answers.md)와 대조한다.
