# 위키를 쉽고 자세하게 만들기 — 진단과 실행 지시서

진단: Claude Fable 5, 2026-09-02. 실행: 더 낮은 모델이 이 문서만 보고 수행한다.
이 문서와 같은 폴더의 두 JSON(`terse-sections.json`, `note-worklist.json`)이 작업 목록이다.
`.plan/`은 `content/` 밖이라 사이트에 발행되지 않는다.

---

## 0. 실행 모델에게 — 먼저 읽을 규칙

**절대 규칙**
1. **숫자를 지어내지 마라.** 논문 노트에 수치를 넣을 때는 반드시 그 논문의 arXiv 초록(`curl -sL https://arxiv.org/abs/<id>`의 abstract 부분)에서 가져오고, 문장에 "per the abstract / 초록 기준"을 붙여라. 초록에 수치가 없으면 **"The abstract reports no quantitative result"**라고 쓰고 멈춰라. PDF를 뒤져 숫자를 찾지 마라.
2. **이 문서가 준 계산 예제만 써라(§3~§5).** 전부 검산돼 있다. 새 계산을 만들지 마라.
3. **양쪽 언어 반쪽에 똑같이 넣어라.** 모든 페이지는 `## English` / `## 한국어` 두 반쪽이다. 한쪽만 고치면 검사가 실패한다.
4. **새 페이지를 만들지 마라. 절 번호를 바꾸지 마라.** 기존 절 안에 문단·콜아웃을 더하는 것만 한다. 새 절이 꼭 필요하면 `### 3.5 …`처럼 반쪽 번호를 쓴다.
5. **07-research-program, 08-research-radar, glossary, study-log, templates는 건드리지 마라.**
6. **SVG를 만들거나 수정하지 마라.**

**문법 규칙 (검사기가 잡는다)**
- 위키링크는 한 줄 안에서 닫아라. 줄바꿈으로 `[[…|…]]`를 쪼개면 실패.
- 굵은 글씨 뒤에 한국어 조사가 바로 오면 실패: `**0.2%**다` ✗ → `**0.2%** 수준이다` ✓ 또는 `0.2%다`.
- 표 셀 안의 위키링크는 `\|`로 이스케이프: `[[a/b\|label]]`.
- display 수식은 한 줄: `$$ … $$`를 여러 줄로 나누지 마라.
- 제목(`###`)에 위키링크를 넣지 마라.
- 한 반쪽에 `§N` 참조를 넣으면 다른 반쪽에도 같은 참조가 있어야 한다.
- 콜아웃 종류는 기존 것만: `[!note]`, `[!tip]`, `[!warning]`, `[!example]`, `[!important]`, `[!question]`, `[!info]`.
- 콜아웃 제목은 이중언어: 영어 반쪽 `> [!example] Worked example · 계산 예제`, 한국어 반쪽 `> [!example] 계산 예제 · Worked example`.

**작업 리듬**
```bash
# 수정 뒤 매번
python3 scripts/verify_content.py && python3 scripts/audit_parity.py
# 한 묶음(페이지 3~5개) 끝날 때마다
python3 scripts/audit_gaps.py          # 느리다(2~4분). SELFCHECK·PREREQ·ARITHMETIC이 0이어야 한다
git add -A && git commit -F <메시지파일>   # 메시지에 따옴표를 쓰지 말고 파일로 넘겨라
NODE_OPTIONS=--max-old-space-size=8192 npm run site && git push origin v5
gh run list --repo jiseop-byeon/phd-wiki --limit 1    # success 확인 (약 90초)
```
`npm run build`는 깨져 있다. `npm run site`만 쓴다.

**한국어 쓰기**: 영어를 직역하지 말고 같은 내용을 짧은 문장으로 다시 써라. 위키의 기존 한국어 문체(단정적, 짧은 문장, "~다" 종결)를 따라라. 전문 용어는 기존 페이지가 쓰는 표기를 그대로 써라(예: 파지, 렌치, 여유자유도, 감쇠 최소자승, 주변화).

---

## 1. 진단 요약

| 장 | 파일 | 페이지 중앙 단어 | 예제/천단어 | 설명표지/천단어 | 판정 |
|---|---|---|---|---|---|
| 02 기초 | 14 | 2,257 | 0.99 | 4.2 | 좋음 — 잔여 얇은 절 21개 |
| 04 로보틱스 | 36 | 1,591 | 0.73 | 4.8 | 좋음 — HRI·배포·인지군집이 열거식, 얇은 절 100개(대부분 표로 설계된 절, §6 참조) |
| **06 연구실무** | 9 | 841 | 0.21 | 2.8 | **골격 상태** — 28~60단어짜리 절이 37개. "Worked diagnosis"가 60단어, "Worked rewrite"가 60단어 |
| **01 논문 노트** | 115 | 397 | 0.15 | 0.0 | **가장 큰 기회** — 숫자 없는 노트 68, 주장읽기 없는 노트 56, 핵심직관 없는 노트 32 |
| **05 건설** | 11 | 902 | 0.00 | 2.9 | 계산 예제 0, 얇은 절 34 |
| 03 딥러닝 지도 | 3 | 195 | 0 | 0 | 지도 페이지 — 손대지 않아도 됨(선택 §7) |

"쉽고 자세하게"에서 가장 큰 이득은 **06 → 01 → 05 → 04·02 잔여** 순서다. 06은 작업량 대비 효과가 가장 크고(페이지 9개, 절이 뼈대뿐), 01은 양이 가장 많다.

---

## 2. 확장 장치 세 가지 — 절마다 하나를 골라 쓴다

위키의 좋은 절들이 이미 쓰는 장치다. 얇은 절을 만나면 아래 중 하나를 적용한다. 새 장치를 발명하지 마라.

**장치 A — "왜 → 구체 사례 → 읽을 때 달라지는 것" 3문단.** 열거식 절(불릿 목록, 용어 표)에 쓴다. 목록은 그대로 두고 그 아래에 붙인다.
- 1문단: 이 개념이 왜 존재하는가(어떤 문제가 이것 없이는 안 풀리는가).
- 2문단: 구체 사례 하나 — 실제 상황, 가능하면 이 위키가 이미 쓰는 예(균열 검출기, 굴착기, 벽 닦기, 드라이월 시트).
- 3문단: "The reading this gives you." / "여기서 얻는 독법." — 논문에서 이 개념을 만났을 때 무엇을 확인해야 하는지 한 문단.
- 모범: `04-robotics/grasping.md` §4, `02-foundations/probability.md` §2의 주사위 문단.

**장치 B — 계산 예제 콜아웃.** 숫자가 성립하는 절에 쓴다. 형식:
```
> [!example] Worked example · 계산 예제
> **한 줄 제목.** 상황 설정 두 문장. 계산 세 줄. 
> **The reading this gives you.** 그 숫자가 논문 읽기에 무엇을 바꾸는지.
```
- 모범: `04-robotics/navigation-mobile-manipulation.md` §4, `04-robotics/human-intent-prediction.md` §5.
- 이 문서 §3~§5가 준 수치만 쓴다.

**장치 C — 전/후 문장 쌍.** 06장(글쓰기·주장·실험 설계)에 쓴다. 나쁜 문장 → 무엇이 문제인가 한 줄 → 고친 문장. 두세 쌍.
- 모범: `06-research-practice/scientific-writing-peer-review.md`의 "claim inside evidence" 그림 아래 문단.

**논문 노트 장치 — 세 요소.** (§4 참조)
1. `> [!tip] Key intuition` 콜아웃 2~4문장: 이 방법이 *왜 통하는지*의 기전. 모범 `01-canonical-papers/notes/4-vla/act.md`의 콜아웃("결정 횟수를 줄이면 오차가 누적되는 지평이 100배 짧아진다").
2. **What it measured** 문단: 초록의 수치 1~3개, 조건과 함께.
3. `> [!question] Reading the claim · 핵심 주장 읽는 법` 콜아웃: 제목의 주장이 실제로 무엇을 뜻하고 무엇을 뜻하지 않는지.

---

## 3. 우선순위 1 — 06 연구실무: 골격에 살 붙이기

파일: `content/06-research-practice/*.md`. `terse-sections.json`에서 `06-`으로 시작하는 37개 절이 대상이다. 각 절을 **140~250단어**로 키운다. 절마다 아래 지정 장치를 쓴다.

### failure-analysis-system-evaluation.md (8개 절, 전부 28~62단어 — 최우선)
- §1 First failure and downstream symptom — **장치 A**, 사례는 이것을 써라: *충돌이 t = 12.4 s에 일어났다. 로그를 거슬러 가면 t = 10.3 s에 위치 추정이 2.1초 동안 갱신되지 않았고, 계획기가 낡은 위치를 믿고 벽을 통과하는 경로를 냈으며, 제어기는 그 경로를 정확히 추종했다. 최초 실패는 추정, 증상은 충돌, 제어기는 무죄다.* 이 사례가 `04-robotics/robot-systems-deployment.md` §10과 연결됨을 링크로 말하라.
- §2 Failure taxonomy — 장치 A. 표는 유지하고, 같은 사례를 표의 행에 대응시켜라.
- §3 Instrumentation and synchronized replay — 장치 A. "동기화"가 왜 필요한지: 카메라 30 Hz, 제어 1 kHz, 위치 추정 20 Hz의 타임스탬프가 어긋나면 위 사례의 2.1초 공백을 아예 볼 수 없다.
- §4 Isolation and fault injection — 장치 A. 사례: 위치 추정을 일부러 2초 얼려 같은 충돌이 재현되면 원인이 확정된다.
- §5 Recovery, intervention, reset — 장치 A. 개입 횟수를 세는 규칙이 결과 숫자를 바꾼다는 점(개입을 실패로 세는지)을 `04-robotics/hri-safety.md` §2와 연결.
- §6 Reliability and field exposure — **장치 B**, 수치: *20회 시행 무사고면 3의 법칙으로 참 실패율 95% 상한이 3/20 = 15% — 일곱 번에 한 번 충돌해도 이 데이터와 모순되지 않는다.* (`06-research-practice/experimental-design-reproducibility.md` §4에 이미 있는 규칙을 인용하라.)
- §7 Worked diagnosis — 위 §1 사례를 **끝까지** 써라: 증상 → 로그 세 줄 → 가설 둘 → 배제 → 확정 → 수정 → 재검증. 최소 250단어.
- §8 Reporting negative results — 장치 C: 부정 결과를 숨기는 문장 → 드러내는 문장 두 쌍.

### scientific-writing-peer-review.md (8개 절)
- §2 Claim–method–evidence sentences — **장치 C**, 세 쌍. 예: ✗ "Our method robustly handles diverse objects." → ✓ "On 40 unseen household objects (Contact-GraspNet protocol), success was 91%, against 84% for the baseline; 6 of the 8 failures were transparent objects."
- §3 Related work as a taxonomy — 장치 C: 나열식 관련연구 문단 → 분류축 있는 문단.
- §4 Figures and tables — 장치 A. 사례: 같은 결과를 "성공률 막대"로 그렸을 때와 "시행 횟수·신뢰구간"으로 그렸을 때 독자가 내리는 결론이 어떻게 다른지.
- §5 Results versus discussion — 장치 C: 결과 절에 해석이 섞인 문장 → 분리한 두 문장.
- §6 Limitations — 장치 C: 형식적 한계 문장("future work will address") → 진짜 한계 문장(어떤 조건에서 어떻게 실패했는지).
- §7 Peer review — 장치 A. 사례: 리뷰어가 "novelty is unclear"라고 쓸 때 저자가 확인할 것 세 가지.
- §9 Artifact alignment — 장치 A.
- §1 Paper-level argument — 장치 A, 사례는 이 위키의 파지 페이지가 하는 논증(닫힘 → 품질 → 학습으로의 이동)을 예로.

### research-questions-claims.md (7개 절)
- §1 Topic → problem → question — 장치 C, 사슬 하나를 끝까지: *주제 "건설 현장 조작" → 문제 "공장용 파지 계획기는 μ를 안다고 가정하는데 현장 표면은 젖고 먼지가 묻는다" → 질문 "접촉 시 촉각으로 μ를 추정하면 μ 오추정 시 파지 성공률 저하가 얼마나 회복되는가".*
- §2 A gap is not merely "nobody has done this" — 장치 A. 사례: "아무도 굴착기에 VLA를 안 붙였다"는 갭이 아니다; 갭은 "붙였을 때 실패할 이유가 알려져 있고 그 이유가 검증 가능한 것".
- §3 Hypotheses and contributions, §4 Claim types, §7 Claim–evidence table — 장치 C 각 두 쌍.
- §5 Scope and assumptions — 장치 A.
- §6 Worked rewrite — §1의 사슬을 논문 초록 한 문단으로 다시 쓴 전/후.

### experimental-design-reproducibility.md (7개 절)
- §3 Variation and splits — **장치 B**, 수치: *시드 3개, 표준편차 4%p → 표준오차 4/√3 = 2.3%p. 3%p 개선은 이 오차 안에 있다. 시드 5개면 1.8%p, 10개면 1.3%p.* 독법: 시드 수를 안 밝힌 3%p 개선은 주장이 아니다.
- §2 Comparisons — 장치 A. 사례: 아키텍처를 바꾸면서 데이터도 바꾼 비교(`06-research-practice/experimental-design-reproducibility.md` 자가점검 답 3번의 내용을 본문으로 끌어올려라).
- §5 Ablations and budgets — 장치 A. 사례: 계산 예산이 같지 않은 절제는 절제가 아니다.
- §6, §7 — 장치 A 짧게(각 120단어).
- §8 Worked design — 최소 250단어로 한 실험을 끝까지 설계: 질문(§3의 사슬) → 단위(참가자? 물체? 시드?) → 비교 → 시행 수(§4의 규칙) → 보고할 것.
- §1 — 이미 정의 목록; 장치 A 한 문단만.

### real-world-impact.md §1, §4, §6 · simulators-benchmarks-datasets.md §1, §9, §10 · psychophysics-human-measurement.md §4
- 각각 장치 A 한 번. simulators §9·§10은 표가 본체이므로 표 아래 "읽을 때 달라지는 것" 문단만.

---

## 4. 우선순위 2 — 01 논문 노트: 숫자·직관·주장읽기

파일: `content/01-canonical-papers/notes/**/*.md`. 목록: `note-worklist.json` (각 노트의 `missing` 배열과 `arxiv` 여부).

**순서**: `tier`가 ★ → ◐ → ○. 같은 등급 안에서는 `missing` 개수가 많은 것부터. ○ 등급은 `missing`이 3개 이상인 것만.

**노트마다 할 일** (`missing`에 있는 것만):
- `numbers` (68개): 초록에서 수치를 가져와 **What it measured** 문단(영어)·**무엇을 쟀는가**(한국어)를 Results/Evidence 근처에 추가. `arxiv: true`인 49개만 초록을 가져올 수 있다. `arxiv: false`인 19개는 노트에 DOI가 있어도 초록을 가져오지 말고, "The abstract was not consulted; the note reports the paper's qualitative claim only"라고 쓰지 **말고 그냥 건너뛰어라** — 없는 숫자는 없는 대로 둔다.
- `intuition` (32개): `> [!tip] Key intuition` 콜아웃을 Method 절 맨 앞(영어) / 방법 절 맨 앞(한국어)에 추가. 2~4문장, **왜 통하는지의 기전**. 노트 본문에 이미 기전 설명이 있으면 그것을 콜아웃으로 끌어올려라. 없으면 초록의 방법 문장을 근거로 쓰되, 확신 없는 기전은 쓰지 마라.
- `claim` (56개): `> [!question] Reading the claim · 핵심 주장 읽는 법` 콜아웃을 Connections/연결 절 **앞**에 추가(이 위치가 35개 파일의 관례). 내용: 제목·초록의 주장이 뜻하는 것 / 뜻하지 않는 것 / 확인할 조건. 모범: `8-construction/wheel-loader-rl.md`의 콜아웃.
- `context`, `limits` (각 7, 6개): 템플릿 `content/templates/paper-note.md`의 해당 절을 추가.

**특히 8-construction 폴더(23개)**: 이 노트들은 "계보 위치 + 비평" 문체로 쓰였고 그 문체는 유지한다. 그 위에 세 요소를 **더한다**. 삭제하지 마라.

**하지 말 것**: 노트를 다시 쓰지 마라. 있는 문장을 고치지 마라. 초록에 없는 수치를 쓰지 마라. 노트 길이를 두 배 이상 늘리지 마라(★ 700단어 → 최대 1,100).

---

## 5. 우선순위 3 — 05 건설 로보틱스: 계산 예제 넣기

이 장에는 계산 예제가 0개다. 아래 **다섯 개는 검산된 수치**이니 그대로 장치 B 형식으로 넣는다. 그 외 `terse-sections.json`의 05 절들은 장치 A.

**earthmoving-heavy-machinery.md §6 Evaluation** (또는 §3) — 생산성 산술:
> 버킷 1.2 m³, 충전율 0.85, 사이클 25 s → 1.2 × 0.85 × 3600/25 = **146.9 m³/h**. 사이클을 10% 줄이면(22.5 s) 163.2 m³/h, 충전율을 10% 올리면(0.935) 161.6 m³/h. 독법: "자율 굴착이 생산성을 높였다"는 주장은 이 두 항 중 어느 쪽을 움직였는지 밝혀야 한다 — 학습 정책은 대개 충전율 쪽이고, 사이클 시간은 기계의 유압이 정한다.

**digital-twin-workflows.md §3 Robot-facing problems** — 오차 예산:
> 스캐너 5 mm, 정합 10 mm, 설계-시공 편차 20 mm → √(5² + 10² + 20²) = **22.9 mm**. 앵커 설치 허용오차 10 mm보다 크다. 분산의 400/525 = 76%가 설계-시공 편차다. 독법: as-designed BIM으로 로봇을 안내하는 시스템은 이 항을 통째로 지고 간다 — as-built 모델이 선택이 아닌 이유.

**sim-to-real.md §4 Reading the evidence** — 무작위화 범위:
> 파라미터 6개를 각각 실제 분포의 80%를 덮도록 무작위화하면, 독립이라 가정할 때 실제 조건이 무작위화 상자 안에 들 확률은 0.8⁶ = **26%**. 90%씩이면 0.9⁶ = 53%. 독법: "도메인 무작위화로 강건하다"는 주장은 몇 개 파라미터를 어느 범위로 흔들었는지 없이는 읽을 수 없다 — 그리고 상자 밖 74%는 시험된 적이 없다.

**site-perception.md §1 또는 §3** — 스캔 분해능:
> 각분해능 0.1°인 LiDAR는 20 m에서 점 간격 20 × tan(0.1°) = **34.9 mm**, 5 m에서 8.7 mm. 10 mm 균열은 20 m에서 점 사이로 빠진다. 독법: 검출 정확도는 거리를 명시하지 않으면 뜻이 없다.

**hrc-worker-centered.md §4 Evaluation** — 경보 정밀도: 새 계산을 하지 말고 `04-robotics/human-intent-prediction.md` §5의 기저율 예제(정밀도 26.9%, 교대당 오경보 1,411회)를 **링크로 인용**하고, 그것이 작업자 대상 인터페이스 평가에 무엇을 뜻하는지 한 문단.

**labs.md, lineage.md, industry-deployment.md**: 목록·지도 페이지다. 장치 A를 억지로 넣지 마라. `lineage.md` §4 "Reading this map as a new researcher"만 150단어로 늘려라(이 계보를 어떻게 자기 주제 선택에 쓰는지).

---

## 6. 우선순위 4 — 04·02장 잔여

`terse-sections.json`의 04(100개)·02(21개)는 **대부분 표로 설계된 절**이다(방법 계열 표, 주장 읽기 표, 용어 표). 그런 절에는 손대지 마라. 아래 열거된 것만 한다.

**hri-safety.md** — §3 Shared control(장치 A, 사례: 블렌딩 α = 0.5에서 사람은 왼쪽, 자율성은 오른쪽으로 장애물을 피하려 하면 합은 정면충돌), §4 Human performance(장치 A, 사례: 신뢰가 높아서 개입이 줄었는데 그게 나쁜 경우), §7 Human-study design(장치 A, 사례: 순서 효과가 결과를 뒤집는 within-subject 연구 하나 — 조건 A를 항상 먼저 하면 A가 연습 효과를 못 받는다), §8 Evaluation(장치 A), §10 Worked interpretation(**최소 250단어**로 굴착기 사례를 끝까지: 자율성 수준 판정 → 개입 집계 규칙 → 보고할 지표 → 이 논문이 할 수 있는 최강 주장).

**robot-systems-deployment.md** — §4 Frames(장치 A, 사례: map 프레임이 루프 폐쇄로 30 cm 점프하면 odom 기준 경로는 멀쩡한데 map 기준 목표가 튄다), §7 Reliability(장치 A, 사례: 하트비트 없는 노드가 죽은 채 마지막 명령을 남기는 상황), §10 Failure taxonomy(§3 절의 06 failure-analysis 사례와 링크). §5·§8·§11은 참고표 — 두어라.

**perception 군집(20~23)** — 각 페이지에 "기전 한 문단"을 §3(백본) 또는 그에 해당하는 절에 추가: video-action §3에 "시공간 어텐션이 실제로 하는 일"(토큰 = 패치×시간, 어텐션은 모든 쌍의 유사도 — `02-foundations/linear-algebra.md` §1의 어텐션 계산 예제로 링크), human-pose-gaze §2에 "히트맵 회귀가 왜 좌표 회귀보다 잘 되는지"(공간적 불확실성을 표현), egocentric §3은 이미 예제 있음 — 생략.

**얇은 불릿 절** — contact-force-tactile §2·§3, state-estimation-slam §2·§3, signal-processing §1·§3: 장치 A 한 문단씩(불릿은 두고 아래에 붙인다).

**02장 잔여**: `terse-sections.json`의 02 항목 21개 중 `words < 100`인 것만 장치 A.

---

## 7. 선택 — 03 딥러닝 지도

`03-deep-learning/lineage.md`의 각 mermaid 블록 아래에 "이 시대가 바꾼 것" 3문장. 낮은 우선순위. 시간이 남으면.

---

## 8. 검증과 완료 기준

- 각 우선순위 묶음 뒤 `python3 scripts/audit_gaps.py` 실행: ARITHMETIC·PREREQ·SELFCHECK 0 유지. UNEXPLAINED는 줄어야 하지만 0이 목표가 아니다.
- 완료 기준(다시 재라):
  - 06장: `terse-sections.json`의 06 항목 중 140단어 미만 절 0개.
  - 01장: `note-worklist.json`에서 ★·◐ 노트의 `missing`에 `intuition`·`claim`이 남지 않음; `numbers`는 `arxiv: true`인 것만.
  - 05장: 계산 예제 5개 존재.
  - 04장: 위 §6에 열거한 절 전부 처리.
- 재측정 스크립트는 이 문서를 만든 스캔과 같다 — `terse-sections.json`을 다시 만들려면 `.plan/rescan.py`를 실행하라.

## 9. 진단자가 남기는 판단 근거 (실행 모델은 읽지 않아도 된다)

- 02·04는 이미 교과서급이라 판정됐고(2026-09-02 평가), 남은 것은 국소적 열거 절이다.
- 06이 골격인 이유: 수학이 없어 위키의 주무기(계산 예제)를 못 썼고, 대체 장치(사례 서사·전/후 문장)를 쓰지 않았다. 이 문서의 장치 A·C가 그 대체 무기다.
- 01의 숫자 결손은 초록 기반으로만 메워야 한다. 이 위키의 인용 위생("초록에서 가져온 수치"를 명시)이 신뢰의 근거이기 때문이다.
- 05는 연구 프로그램의 본진이지만 정량 예제가 0인 유일한 장이었다. 다섯 개 수치는 전부 위키 안의 다른 페이지가 이미 쓰는 종류의 산술이다.
