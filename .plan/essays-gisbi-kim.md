# 김기섭 에세이(gisbi-kim.github.io) → 위키 반영 계획

작성: 2026-09-03, Fable 5.1 (전수조사 30편 + 판단). 실행: 이후 세션(Opus-medium).
이 파일은 `.plan/` 안에 있어 사이트에 빌드되지 않는다. 위키 본문은 아직 아무것도 수정하지 않았다.

## 0. 실행 규칙 (반드시 지킬 것)

1. **원문을 직접 읽고 쓴다.** 각 항목의 URL을 WebFetch로 끝까지 읽은 뒤 작성한다. 이 파일의 요약만 보고 쓰지 않는다. 404가 나면 그 항목은 건너뛰고 §4에 기록한다.
   - `/essays/` 목록 페이지에는 링크가 없다. 아래 URL을 직접 연다. `/vla-runtime-harnessing/`, `/spatial-experience-memory/`, `/aprl-research-vision/`, `/situated-spatial-intelligence/`는 RSS에 없는 숨은 페이지지만 실제로 존재한다.
2. **복사 금지, 재구성 + 출처 표기.** 문장을 옮기지 말고 논지를 위키의 말로 다시 쓴다. 각 삽입 단위 끝에 반드시 출처 한 줄:
   - EN: `Synthesised from Giseop Kim's essay [<title>](<URL>).`
   - KR: `김기섭의 에세이 [<제목>](<URL>)을 요약·재구성한 것이다.`
   - 그의 조어("runtime harnessing", "demo indigestion", "spatial experience" 등)는 따옴표로 묶고 "Kim's term"/"김기섭의 표현"이라고 밝힌다.
3. **논문 사실은 논문에서.** 에세이가 언급한 논문(CorrectNav, Alpamayo, Churchill & Newman, ReMEmbR 등)의 내용을 위키가 서술할 때는 arXiv 초록/원문을 확인한 것만 쓴다. 확인 못 하면 "the essay reads X as …"처럼 에세이의 해석임을 밝힌다. 숫자 창작 금지.
4. **양쪽 반(`## English` / `## 한국어`) 모두** 같은 내용으로. 기존 관례 유지: 단일행 수식, 제목에 위키링크 금지, 표 안 `\|`, 위키링크 줄바꿈 금지, `**굵게**` 뒤 조사 금지, 콜아웃 제목은 이중언어.
5. **새 페이지 없음, 절 번호 재배열 없음.** 추가는 콜아웃, 기존 절 안의 문단, 또는 §x.5 반번호 절만. 07/08/glossary(§2 예외)/study-log/templates는 손대지 않는다.
6. **분량 상한.** A등급 항목은 반쪽당 최대 ~150단어(콜아웃 1개 또는 짧은 §x.5). B등급은 1–2줄 링크. 합계로 위키가 눈에 띄게 길어지면 안 된다.
7. **포함 시험**: "논문에서 자주 나오지 않으면 넣지 않는다." 그래서 그의 조어는 glossary에 올리지 않는다(본문 콜아웃 안에서만 소개). glossary 추가는 §2에 명시한 2개만.
8. **공개 저장소.** CV·경력·소속 세부는 쓰지 않는다. 출처 표기는 "Giseop Kim (APRL)" + 링크까지만.
9. 완료 후 QA: `python3 scripts/verify_content.py`, `python3 scripts/audit_parity.py`, `python3 scripts/audit_gaps.py` 모두 통과 → `npm run site`(백그라운드, 8GB heap) → v5 push.

## 1. 전수조사 판정 (30편)

A = 본문 반영(재구성 문단/콜아웃), B = 링크만(Going deeper/Sources), C = 제외.

| # | 에세이 | 판정 | 이유 |
|---|---|---|---|
| 1 | vla-runtime-harnessing (사용자가 말한 "VLA 통합 서베이 2024–2026") | **A** | 2024–26 VLA 논문을 "훈련 시 추가"와 "실행 시(runtime) 추가"로 나눠 읽는 틀. 위키에 없는 test-time compute 관점. |
| 2 | spatial-experience-memory | **A** | map vs memory 구분과 experience record 튜플. semantic-nav §7·SLAM §7의 장기/다중세션 공백을 메움. |
| 3 | slam-textbooks (SLAM back-end 자료 5개) | **A** | 무료 자료 5개 + 읽는 순서 + "왜 이 셋(회전 매개변수화·반복 최소제곱·희소성)만 알면 되는가". SLAM Going deeper에 바로 들어감. |
| 4 | slambackend-1 | **A** | SLAM back-end = 정규방정식 $A^TA\,\Delta x = A^Tb$, locality → 희소성. |
| 5 | gn-iekf-same | **A** | Gauss-Newton 한 스텝 == iterated EKF 갱신. 필터/스무더가 같은 갱신의 두 얼굴임을 보여줌. |
| 6 | slam-root, sclidarslam | **B** | "SLAM = odometry + loop closing" 한 줄 정식화. SC-PGO 모듈 분리는 구현 이야기라 링크만. |
| 7 | bayesfiltering-1, bayesfiltering-2 | **B** | 베이즈 규칙 → 가우시안 곱 → 역행렬 보조정리로 칼만 이득 유도. 한국어 유도 경로로 링크. |
| 8 | tao-ai-math-for-physical-ai | **A** | "demo indigestion"(데모 소화불량)과 Goodhart: AI가 후보 결과를 쏟아내면 병목은 검증. 06 증거 사다리에 맞음. |
| 9 | ai-verification-for-robotics | **A** | verification vs validation 구분, 배포 후 지속 보증, "AI가 제안하고 검증이 제약한다". |
| 10 | why-some-icra-papers-thrive | **A** | buildability/generativity: 남이 그 위에 쌓을 수 있는 논문이 산다. 06 real-world-impact §5와 정확히 같은 주제. |
| 11 | winning-research-design-sun-tzu | **A** | 실험 전에 주장–증거 구조를 설계하고 싸울 전장(평가 체제)을 고른다. research-questions §7 표의 사용법. |
| 12 | implementation-context-evaluation | **A** | 구현 맥락이 평가의 의미를 정한다: 같은 숫자가 맥락 따라 다른 주장. 06 simulators §10–11 읽기 지침에 맞음. |
| 13 | aprl-research-vision | **B** | 중간 지표(ATE, token accuracy) ≠ 최종 결과라는 읽기 교훈만 SLAM §9에 한 줄. 연구실 비전 자체는 07(사용자 프로그램)에 넣지 않는다. |
| 14 | situated-spatial-intelligence | **B** | task relevance(과제마다 필요한 공간정보가 다름) 예시. #2 콜아웃에 링크 한 줄. |
| 15 | from-paper-writer-to-research-system-builder | **B** | 연구를 "연결된 시스템"으로 보기. real-world-impact §5 Going deeper 묶음. |
| 16 | first-1000-citations | **B** | 재사용 가능한 자산(코드·데이터·문제정의)이 인용을 만든다. 같은 묶음. |
| 17 | ideal-research-topic-roic | **B** | 연구자본 복리 관점. 같은 묶음(수식은 옮기지 않음). |
| 18 | lab-management-designing-win-rate | **B** | "500단어 다 외우지 않는다" = 위키의 포함 시험과 같은 철학. 같은 묶음. |
| 19 | bird-in-hand-lab-management | **B** | 손안의 자산을 다음 연구로 전환. 같은 묶음. |
| 20 | inside-claude-code-boris-cherny | **B** | "하네스는 영구 지능이 아니다(scaffolding decay)" 경고 한 줄을 #1 콜아웃에 덧붙임. |
| 21 | ai-agent-era-researcher-role | C | 연구 워크플로 수필. 위키 주제 밖. |
| 22 | ai-university-redesign | C | 교육정책. 밖. |
| 23 | claude-code-field-notes | C | 도구 사용기. 밖. |
| 24 | gemini-robotics-2-dialogue-map | C | 영상 대화 지도(2차 자료). 나중에 Gemini Robotics 노트가 생기면 보조 링크로 재고. |
| 25 | atlas-enterprise-humanoid-dialogue-map | C | 휴머노이드 하드웨어 설계 대담. 조작 중심 프로그램의 범위 밖. |
| 26 | icra21-radar-ws | C | 레이더 워크숍 요약. 프로그램에 레이더 없음. |
| 27 | yeti-radar-odom-mulran1 | C | 레이더 오도메트리 구현기. 같은 이유. |
| 28 | papers-before-dgist | C | 논문 목록. 학습재료 아님(사용자 지시: CV는 여담). |
| 29 | (essays 목록 페이지) | C | 링크 없는 껍데기. |
| 30 | (Drive 폴더) | C | CV만 있음. 사용 금지. |

## 2. 항목별 실행 명세

### 2.1 VLA runtime harnessing → 두 곳 + glossary 1개
URL: https://gisbi-kim.github.io/vla-runtime-harnessing/

**(a) `content/03-deep-learning/lineage.md`**, "Robot learning: from demonstrations to foundation models" 절 끝(다이어그램 뒤)에 콜아웃 `> [!note] Reading the 2024–2026 VLA papers · 2024–2026 VLA 논문 읽기`. 담을 것(에세이 §4 이후를 읽고 재구성):
- 최근 VLA의 공통 골격: VLM backbone + action expert. 이 골격만으로 부족한 이유(모방학습이 본 데이터 분포 밖에서 멈춤).
- LLM에서 일어난 순서를 유비로: SFT → RL(GRPO, DeepSeek-R1) → 추론 시 연산(test-time compute). 에세이는 VLA가 아직 "DeepSeek 순간" 이전 단계라고 본다 — 이것은 에세이의 해석임을 명시.
- "runtime harnessing"(김기섭의 표현): 실행 중 불확실성 감지 → 더 관측 → 기억 검색 → 자기 검증 → 복구. 논문에서는 monitor/verifier/router/deliberation 같은 이름으로 나타난다.
- 논문을 읽을 때 물을 것 한 줄: "이 논문이 더한 것은 훈련 시인가, 실행 시인가? 실행 시라면 실패를 *알아채는* 것과 *고치는* 것 중 무엇인가?"
- 마지막 문장: 하네스는 영구 지능이 아니다 — 다음 모델이 나오면 걷히는 비계일 수 있다(inside-claude-code 링크, B).
- 예시 논문은 최대 2개(CorrectNav, Alpamayo). 각각 arXiv 초록을 확인하고 한 구절로만. 확인 안 되면 이름만.

**(b) `content/04-robotics/semantic-language-navigation.md` §8 "Reading a paper in this area"** 끝에 2–3문장 문단: 2025–26 VLN/VLA 논문의 "실행 시 자기교정" 계열을 읽는 법 + (a)로 위키링크 + 에세이 링크. 새 콜아웃 만들지 말고 문단으로.

**(c) `content/glossary.md`**: `test-time compute · 추론 시 연산` 1항목(정의 2문장, LLM 기원, VLA에서의 의미). "runtime harnessing"은 glossary에 올리지 않는다(규칙 7).

### 2.2 Spatial experience memory → 두 곳 + glossary 1개
URL: https://gisbi-kim.github.io/spatial-experience-memory/ (+ B: https://gisbi-kim.github.io/situated-spatial-intelligence/)

**(a) `content/04-robotics/semantic-language-navigation.md` §7** 끝에 콜아웃 `> [!note] Map or memory? · 지도인가 기억인가`:
- 지도 M은 "어디에 무엇이"의 현재 추정. 기억 H ≈ M + 색인된 경험 기록 {eᵢ}. 기록 하나 = (geometry, topology, semantics, where, when, observation, context, action, outcome, uncertainty, provenance) — 이 튜플은 에세이의 정의이므로 출처 명시.
- 왜 구분이 중요한가: 변화를 지도 갱신에 흡수하면 "왜 실패했는가"를 나중에 물을 수 없다. 언어로 질의 가능한 지도(§7 본문)는 기억 쪽으로 가는 한 걸음.
- 논문 앵커 1개: Churchill & Newman의 experience-based navigation(연도·학회는 원문에서 확인). ReMEmbR·OpenBot-Fleet는 이름만, 확인되면 한 구절.
- 마지막 줄: 과제가 바뀌면 필요한 공간정보도 바뀐다(situated-spatial-intelligence 링크).

**(b) `content/04-robotics/state-estimation-slam.md` §7** 끝에 2문장: 장기·다중세션 운영에서 "지도"가 저장하지 않는 것(시간·맥락·행동 결과) + (a)로 위키링크. 콜아웃 아님.

**(c) `content/glossary.md`**: `spatial memory · 공간 기억` 1항목(지도와의 차이 한 줄).

### 2.3 SLAM back-end 자료 5개 → Going deeper 확장
URL: https://gisbi-kim.github.io/post/slam-textbooks/

`content/04-robotics/state-estimation-slam.md` Going deeper 콜아웃(EN 214행, KR 452행 부근)에 두 번째 문단 추가:
- 최적화 기반 back-end만 빠르게 잡으려면 세 가지만 알면 된다: 회전 매개변수화, 반복 최소제곱(GN/LM), 희소성.
- 자료: 1 Solà *Quaternion kinematics for the error-state KF* / 2-1 Grisetti 외 ICRA 2016 튜토리얼 *From Least-Squares to ICP* / 3 Solà *Course on SLAM* / 4 Dellaert & Kaess *Factor Graphs for Robot Perception* / 2-2 *Graph-Based SLAM and Sparsity*(ICRA 2016 튜토리얼) / 5 Triggs 외 *Bundle Adjustment — A Modern Synthesis*. 에세이가 권하는 순서 1 → 2-1 → 3 → 4 → 2-2 → 5. 각 자료의 실제 링크는 에세이에서 가져와 확인.
- 위키가 이미 Solà를 인용하는 페이지(se3-geometry 등, 17곳)와 중복되면 SLAM 페이지에만 목록을 두고 se3-geometry Going deeper에는 "읽는 순서는 SLAM 페이지" 한 줄.

### 2.4 정규방정식·희소성·GN==IEKF → SLAM §5 콜아웃 + optimization 교차링크
URL: https://gisbi-kim.github.io/post/slambackend-1/ , https://gisbi-kim.github.io/post/gn-iekf-same/ , (B) https://gisbi-kim.github.io/post/slam-root/ , https://gisbi-kim.github.io/post/sclidarslam/

**(a) `state-estimation-slam.md` §5 "Method families"** 끝에 콜아웃 `> [!tip] Filter and smoother are one update · 필터와 스무더는 같은 갱신`:
- back-end는 결국 $A^TA\,\Delta x = A^Tb$를 반복해서 푸는 일. 상태 수백만이어도 풀리는 이유는 locality → $A$가 희소.
- Gauss-Newton 한 스텝과 iterated EKF의 갱신은 같은 식(정보 형태 vs 공분산 형태)임을 에세이 gn-iekf-same이 대수로 보인다. 따라서 "필터 vs 그래프"는 문제 구조가 아니라 *어느 변수를 marginalize하고 어느 것을 남기는가*의 차이. 유도는 옮기지 말고 결론+링크.
- 반쪽 §7 첫 문단에 "SLAM = odometry + loop closing"(slam-root 링크) 한 줄이 아직 없으면 추가.

**(b) `content/02-foundations/optimization.md` §3.5**(Gauss-Newton 절) 끝에 1문장: "로봇 추정에서는 이 GN 스텝이 곧 iterated EKF 갱신이다" + SLAM §5 위키링크. 에세이 링크는 SLAM 쪽에만.

### 2.5 베이즈 필터 유도 → probability Going deeper 1줄 (B)
URL: https://gisbi-kim.github.io/post/bayesfiltering-1/ , https://gisbi-kim.github.io/post/bayesfiltering-2/
`content/02-foundations/probability.md` Going deeper(233행 부근) 끝에 1문장: 한국어로 베이즈 규칙에서 가우시안 곱, 역행렬 보조정리를 거쳐 칼만 이득까지 가는 유도 경로. 양쪽 반.

### 2.6 "demo indigestion"·Goodhart → real-world-impact §2
URL: https://gisbi-kim.github.io/tao-ai-math-for-physical-ai/
`content/06-research-practice/real-world-impact.md` §2(증거 사다리) 끝에 콜아웃 `> [!warning] Demo indigestion · 데모 소화불량`: AI가 후보 결과·데모를 싸게 대량 생산하면 병목은 생산이 아니라 검증으로 옮겨간다; 확인되지 않은 데모는 사다리의 어느 칸도 아니다; 지표가 목표가 되면 지표가 망가진다(Goodhart). Tao의 원 논지(수학에서의 AI)를 물리 AI로 옮긴 것이 에세이의 기여임을 밝힌다.

### 2.7 verification vs validation → experimental-design §1 + failure-analysis 1문단
URL: https://gisbi-kim.github.io/ai-verification-for-robotics/
- `content/06-research-practice/experimental-design-reproducibility.md` §1 끝 콜아웃 `> [!note] Verification is not validation · 검증과 타당성 확인은 다르다`: verification = "만든 대로 동작하는가", validation = "만든 것이 옳은 것인가"; 모델이 제안하는 시대에는 둘 다 사람이 설계해야 하며 배포 후에도 계속(continuous assurance). 실험 설계 단계에서 어느 쪽 증거를 만드는지 미리 정하라.
- `content/06-research-practice/failure-analysis-system-evaluation.md`: 배포 후 평가/모니터링을 다루는 절 끝에 2문장 + 위 콜아웃으로 위키링크(절 번호는 실행 시 확인).

### 2.8 buildability/generativity → real-world-impact §5 + §3
URL: https://gisbi-kim.github.io/why-some-icra-papers-thrive/
`real-world-impact.md` §5 "Designing so the outputs compound" 끝에 문단(콜아웃 아님): 오래 사는 논문의 공통점은 남이 *그 위에 쌓을 수 있음*(buildability)과 *새 질문을 낳음*(generativity); 실용적으로는 코드+데이터+평가 프로토콜을 한 묶음으로 내는 것. §3(artifact 비용 표) 끝에 이 문단으로 위키링크 1줄. 같은 §5 끝에 `> [!tip]- Going deeper · 더 깊이` 접힌 콜아웃 하나로 #15–19 다섯 편을 각 한 줄 설명과 함께 링크(B 묶음). ROIC 수식은 옮기지 않는다.

### 2.9 "이기고 나서 싸운다" → research-questions §7
URL: https://gisbi-kim.github.io/winning-research-design-sun-tzu/
`content/06-research-practice/research-questions-claims.md` §7 claim–evidence 표 아래 콜아웃 `> [!tip] Fill the table before the experiments · 실험 전에 표를 채워라`: 표의 오른쪽(증거)을 실험 *전에* 설계한다; 반박하기 어려운 실험 하나가 실험 열 개보다 낫다; 전장을 고른다 = 우리 방법의 장점이 결정적으로 드러나는 평가 체제를 선택하되 그 선택을 논문에 정직하게 쓴다. experimental-design §1에서 이 콜아웃으로 위키링크 1줄.

### 2.10 구현 맥락이 평가를 정한다 → simulators-benchmarks §11
URL: https://gisbi-kim.github.io/implementation-context-evaluation/
`content/06-research-practice/simulators-benchmarks-datasets.md` §11 "Reading a learned-policy evaluation" 끝에 콜아웃 `> [!note] The implementation context is part of the result · 구현 맥락도 결과의 일부다`: 같은 성공률도 로봇·센서·재시도 규칙·정지 조건·실패 집계 방식이 다르면 다른 주장; 표를 읽기 전에 그 맥락을 먼저 찾아라; 저자로서는 맥락을 바꾸는 것 자체가 기여가 될 수 있다(평가 체제의 제안).

### 2.11 중간 지표 ≠ 최종 결과 → SLAM §9 1문장 (B)
URL: https://gisbi-kim.github.io/aprl-research-vision/
`state-estimation-slam.md` §9 "Reading claims and evaluations" 끝: "ATE를 낮추는 목적은 숫자가 아니라 로봇이 길을 잃지 않게 하는 것 — 논문의 지표가 그 목적에 닿는지 물어라" 취지 1문장 + 링크. 연구실 비전·폐루프 도식은 옮기지 않는다.

## 3. 실행 순서 (권장)
2.3 → 2.4 → 2.5 (SLAM 묶음, 가장 기계적) → 2.1 → 2.2 (VLA/기억, 논문 확인 필요) → 2.6 → 2.10 (06 묶음) → QA → 빌드 → push → 커밋 메시지는 `git commit -F` 파일로.

## 4. 실행 기록 (실행 세션이 채움)
- 404/생략 항목:
- 논문 사실 확인 못 해 "에세이의 해석"으로 표기한 곳:
