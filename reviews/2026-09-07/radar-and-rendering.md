# Radar 및 실제 렌더링 점검

기준: 2026-09-07, source `1824821`. 본문 수정·배포 없이 점검. 자동 QA: 210개 Markdown, 0건. QA 통과는 학술적 정확성/독학성 보증이 아니다.

읽은 범위: `content/08-research-radar/index.md` 전체, Radar compiler·JS·HTML 전체, taxonomy 및 data.json의 집계/분류 관련 필드. 화면 표본: 라이브 홈, Foundations Overview, Neural Network Basics. 전체 사이트의 화면·모바일·인쇄는 전수 확인하지 않았다.

## UX-01 · P2 · 범위 기호가 취소선으로 렌더링됨

- 근거: `content/index.md:59`의 `A~G절`과 `H~J절`. 라이브 DOM에서 두 물결표 사이가 `<del>`로 표시된다.
- `content/02-foundations/overview.md:294`의 장 범위와 `:388`의 `30~50시간 … 50~70시간`에서도 실제 취소선을 확인했다.
- 영향: 유효한 학습 안내가 삭제된 내용처럼 보인다. 자동 QA가 현재 탐지하지 않는다.
- 개선: 범위는 en dash 또는 '부터 …까지'로 통일. 의도적 삭제선은 유지하되 빌드 HTML의 `article del`을 점검 대상으로 추가한다.
- 신뢰도: source와 라이브 DOM 확인.

후속 전역 검사: 현재 로컬 `public/`의 article HTML에서는 총 8개 페이지에 `<del>`이 있다. `index`, `overview`, `ddim`, `ddpm`, `control-theory-ce397`, `force-compliance-control`, `traversability-off-road`, `study-log`이다. 범위 두 개가 만나는 문장들로 확인되며, 로컬 빌드 검사를 라이브 8페이지 전수 검사로 확대해 표현하지 않는다.

## UX-02 · P2 · 상위 섹션 번호 7 중복

- 근거: `content/glossary.md:2`와 `content/07-research-program/index.md:2`; 라이브 Explorer에 `7. Glossary`, `7. Research Program`이 함께 나타난다.
- 영향: 번호가 순서인지 분류인지 불명확해진다.
- 개선: 안정적인 URL은 유지하면서 표시 번호만 일관되게 정리하거나, 참고 도구와 학습 트랙 번호를 분리한다.
- 신뢰도: source와 라이브 DOM 확인.

## UX-03 · P2 · 절 이름 링크가 페이지 맨 위로 이동

- 근거: `content/index.md:18` gate check 링크는 `02-foundations/overview`에만 연결된다. Overview의 `0.5 공업수학 §1–3`, `§10 표기법 사전` 링크도 절 anchor 없이 페이지로만 연결된다.
- 영향: 긴 EN/KR 페이지에서 필요한 복습 부분을 다시 찾아야 한다.
- 개선: 'gate check', '§10' 등 특정 절을 명시한 링크는 해당 언어 heading anchor로 연결. 페이지 전체를 읽으라는 링크는 현 상태 유지.
- 신뢰도: source와 라이브 DOM 확인. 전역 링크 모두를 검사한 것은 아니다.

## RADAR-01 · P1(연구 주제 판단) · 선 그래프 높이와 표시 숫자의 단위가 다름

- 근거: `quartz/static/research-radar/radar.js:70–75`. 선의 높이는 `t.shares`로 계산하지만 점 라벨은 `t.counts`이다.
- 실제 데이터: Transformer 2024→2025의 편수는 603→618이지만 점유율은 33.021→28.181/1000이다. 숫자는 늘면서 선은 내려간다.
- 개선: 편수/점유율 전환을 제공하거나, 선과 라벨을 같은 단위로 맞추고 나머지는 tooltip에 표시. 축 단위와 분모를 명시한다.
- 신뢰도: source·배포용 JSON 확인. 해당 그래프의 라이브 조작은 이번 점검에서 하지 않았다.

## RADAR-02 · P2 · 해결된 온톨로지 혼합을 현재 문제로 안내

- 근거: `content/08-research-radar/index.md:47–49`와 한국어 대응. '현 데이터셋 Transformer에 Mamba가 혼입'이라고 하지만 2026-08-21 JSON은 `transformers`와 `state_space_models`를 별도로 갖는다.
- 개선: Mamba 분리는 해결된 변경 기록으로 이동. Foundation Models와 LLM 용어 혼합처럼 실제 남은 한계만 현재 경고에 남긴다.
- 신뢰도: source와 생성 JSON 대조.

## RADAR-03 · P1(연구 주제 판단) · 단일 분모와 누락 연도

- 근거: `scripts/compile_research_radar.py:251–256`; 모든 venue의 연도별 합계로 share를 계산한다. JSON에 CoRL 2025·RSS 2025가 missing이다. 현재 코퍼스 76,701편, 2021–2025, 60개 토픽.
- 개선: 동일한 venue-year가 확보된 비교 집합 또는 venue별 점유율을 함께 제공하고, 불완전 연도는 별도 표시. 원시 편수·정규화 결과를 나란히 비교한다.
- 현재 장점: 본문이 이미 이 위험을 설명한다. 따라서 학습 커리큘럼의 차단 결함은 아니며 Radar를 단독 연구 선정 근거로 쓸 때 중요한 제한이다.
- 신뢰도: 집계 구현과 JSON 확인. 현재 외부 색인에 누락 데이터가 새로 생겼는지는 재조회하지 않았다.

## RADAR-04 · P2 · 표본 규모를 분류 정확도처럼 읽힐 수 있는 confidence

- 근거: compiler `:262`의 High는 support≥30, venue≥3만 요구한다. 제목 분류의 precision/recall이나 통계적 confidence interval을 검증한 값은 아니다.
- 개선: '자료 지지량'으로 명명하고 분류 정확도와 구별. 층화 표본의 제목 매칭 검토 결과를 별도 기록한다. 현재 점수는 경험적 순위라는 점도 명시한다.
- 신뢰도: 구현 확인.

## RADAR-05 · P2 · 대표 논문 선정 기준

- 근거: compiler `:273`; 최신 연도와 venue 이름 역순으로 첫 6편을 고른다. 품질·주제 대표성 평가가 아니다.
- 개선: 라벨을 '최근 매칭 논문 예시'로 바꾸거나 venue/하위토픽을 다양하게 뽑고 선정 방식을 밝힌다. 읽기 시작할 핵심 논문은 검토된 canonical 노트와 별도 연결한다.
- 신뢰도: 구현 확인.

## RADAR-06 · P2 · 다중 매칭 합계를 고유 논문 수처럼 표시

- 근거: JS `:31`은 토픽별 recentVolume을 합산하여 `matched papers · recent`로 표시한다. 다중 라벨 구조라 한 논문이 여러 번 기여할 수 있다.
- 개선: '토픽–논문 매칭 수(중복 포함)'로 표시하거나 고유 논문 ID를 집계한다.
- 신뢰도: 구현 확인. 중복 논문 수 자체는 현재 정적 JSON만으로 재구성하지 않았다.

## RADAR-07 · P2 · 결과 0개일 때 이전 근거 패널 잔류 가능

- 근거: JS `:35–36`; 필터 결과가 없으면 selected는 undefined가 되지만 기존 timeline/detail을 지우지 않는다. JSON에는 Cooling 상태가 없어 해당 필터에서 이 경로가 발생한다.
- 개선: 결과 0개 안내와 함께 이전 그래프/근거를 초기화. 현재 필터의 결과인지 명확하게 한다.
- 신뢰도: source와 데이터 확인; 라이브 조작 재현은 미실시.

## RADAR-08 · P3 · 근거에서 실제 학습으로 돌아오는 링크

- 근거: JS `renderDetail`은 외부 매칭 논문만 제공하며, 위키 관련 foundation/개념 지도 링크는 없다. 상위 본문에는 깊이 가이드 일반 링크가 있다.
- 개선: 토픽별 위키 개념 페이지와 최소 선수 개념 1–3개를 매핑. 기술 논쟁 판단은 빈도와 구별하여 검토된 비교 자료에만 연결한다.
- 신뢰도: 구현 확인.

## 확인된 강점과 범위 제한

- Radar는 이미 IROS/RSS/RA-L/T-RO를 포함한다. 과거의 '이 venue 전체 누락' 비판은 현재에 적용하지 않는다.
- 홈→Overview→0.7 신경망 입문의 링크는 동작한다. 확인한 두 기초 페이지에서 KaTeX error 요소가 없었고, Overview의 네 Mermaid 블록은 SVG로 생성되어 있었다.
- Sources 접기 블록과 Bartos 강의 링크는 존재한다.
- 영한 연속 본문은 목차로 이동 가능하다. 언어 탭은 선택 UX 개선이지 학습 불가능의 근거가 아니다.
- PDF 내보내기·모바일·모든 외부 링크의 상태는 이번 표본 화면 검사에서 검증하지 않았다.
