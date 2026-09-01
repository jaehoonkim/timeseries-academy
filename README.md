# timeseries-academy

시계열 데이터 분석을 가르치기 위한 모듈형 커리큘럼 저장소.
강의자가 스스로 학습·실습한 자료를 그대로 강의 교안으로 사용하는 것이 목표다.

## 과정

| 과정 | 대상 | 상태 |
|---|---|---|
| [courses/middle](courses/middle/) | 중학생 | 완성 (모듈 8개) |
| [courses/high](courses/high/) | 고등학생 | 완성 (모듈 8개) |
| [courses/university](courses/university/) | 대학생 | 완성 (모듈 8개) |

## 구조

- [data/](data/) — 과정 간 공유 실습 데이터 (서울 일별 기온, 서울 지하철 일별 승하차)
- [courses/](courses/) — 대상별 과정. 각 과정은 60~90분 수업 단위의 독립 모듈로 구성
- [docs/](docs/) — 설계 문서
- [slides-pdf/](slides-pdf/) — 전 모듈 이론 슬라이드 PDF (marp-cli 렌더링 산출물)

과정별 설계 배경은 각 과정 README에 링크된 설계 문서
([docs/superpowers/specs/](docs/superpowers/specs/)) 참고.
