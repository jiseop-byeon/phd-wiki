# Physical AI 핵심 논문 노트 학습성 정독 감사

- 감사일: 2026-09-07
- 대상 독자: 공업수학 수강 경험은 있으나 ML·로보틱스를 처음 독학하는 공대생
- 범위: `4-vla/`, `5-world-models/`, `6-diffusion/`, `7-robotics/`, `9-navigation/`의 Markdown 58개
- 제약: `content/` 수정·배포·커밋 없음. 원 논문 전수 fact-check가 아니라 노트 자체의 학습성·내적 일관성 감사이며, 별도 확인하지 못한 니치 사실은 “추가검증 필요”로 표시한다.
- **최종 읽기 상태:** 범위의 Markdown 58개를 모두 첫 줄부터 마지막 줄까지 완독했다. 도구 출력이 한 차례 절단되었던 `act.md:176–189`, `navid.md:75–124`, `rma.md:1–45`도 별도 구간으로 끝까지 확인했다.

## 최종 결론

전체적으로는 **Literacy 달성에 강하고, 선택 영역의 Working 진입에는 조건부로 충분**하다. 특히 대부분의 노트가 (1) 한 줄 문제 정의, (2) 방법의 역할 분해, (3) 실험이 실제로 잰 것, (4) 주장 범위와 한계를 나란히 제시해 논문을 과장해 읽는 습관을 잘 교정한다. VLA의 “의미 일반화 대 운동 기술”, 월드모델의 “그럴듯함 대 물리 정확성”, 로봇공학의 “센서가 직접 재는 값 대 추론값”, 내비게이션의 “로코모션 대 내비게이션” 구분은 특히 좋다.

다만 아래 P1 세 건은 바로잡기 전에는 해당 개념을 반대로 배우거나 수식의 손잡이를 잘못 사용할 수 있다. Working 표기가 붙은 문서 중 일부는 체크리스트가 요구하는 설명이 본문에 없고, 몇몇 지도(index)는 자신의 `depth-goal`에 비해 너무 얇다.

## 발견 요약

| ID | 우선순위 | 요지 | 근거 신뢰도 |
|---|---:|---|---|
| papers-policy-001 | P1 | ACT 본문과 도식이 폐루프 재질의 여부를 서로 반대로 설명 | 본문 확인 |
| papers-policy-002 | P1 | CFG의 동일한 $w$가 두 서로 다른 관례로 정의됨 | 본문 확인 |
| papers-policy-003 | P1 | Flow Matching 도식이 스텝 수를 경로 곡률 하나로 환원 | 본문 확인(엄밀한 범위는 추가검증 필요) |
| papers-policy-004 | P2 | Dreamer 체크리스트가 본문에 설명하지 않은 RSSM 두 경로를 요구 | 본문 확인 |
| papers-policy-005 | P2 | π0 영어 독립평가 callout이 문장 중간에서 끊김 | 본문 확인 |
| papers-policy-006 | P2 | `World Models`가 분야 이름을 붙였다는 역사적 단정 | 추가검증 필요 |
| papers-policy-007 | P2 | Gervet 주택 결과를 건설 현장의 “23% 영역”으로 수치 외삽 | 본문 확인 |
| papers-policy-008 | P2 | 두 index가 읽기 지도라는 목표를 수행하지 못함 | 본문 확인 |
| papers-policy-009 | P2 | 임피던스 제어의 하드웨어 요구를 지나치게 절대화 | 추가검증 필요 |
| papers-policy-010 | P2 | BADGR 학습목표가 cost map이 못 주는 선호를 준다는 체크 질문 | 본문 확인 |

## 상세 발견

### papers-policy-001 — ACT의 핵심 실행 의미가 본문과 도식에서 모순됨 (P1)

- 위치·인용: `content/01-canonical-papers/notes/4-vla/act.md:45` — “ACT explicitly does *not* run open-loop inside a chunk”; 같은 파일 `:63` — “action chunking — one decision per chunk”; `:68` — “nothing that happens mid-chunk can change the plan until the next decision.” 한국어 도식도 `:142`의 “매 스텝 질의”와 `:144`의 “다음 결정 지점까지 계획을 바꿀 수 없다”가 충돌한다.
- 문제: ACT를 이해하는 핵심은 매 시점 새 청크를 예측하고 동일 실행 시점에 대한 겹친 예측을 temporal ensemble한다는 점이다. 현재 도식은 청크를 한 번 뽑아 open-loop 실행하는 정책으로 가르쳐, 반응성·복합오차·의사결정 횟수에 관한 독자의 정신모형을 뒤집는다.
- 구체 수정안: 도식의 “one decision per chunk/5 decisions”와 “mid-chunk…” 문장을 “a new chunk prediction every tick; each executed action aggregates overlapping forecasts”로 교체한다. 한국어도 “매 틱 새 청크를 예측하고 현재 행동 하나를 앙상블해 실행”으로 맞춘다. 반응성 대 안정성의 비용은 “고정 청크 자체”가 아니라 긴 예측 지평과 시간 앙상블의 지연·평활화 효과로 정확히 설명한다.
- 근거 신뢰도: **본문 확인**(같은 노트 내부 모순만으로 확정 가능).

### papers-policy-002 — CFG의 guidance scale 관례가 한 페이지 안에서 바뀜 (P1)

- 위치·인용: `content/01-canonical-papers/notes/6-diffusion/classifier-free-guidance.md:21` — `$\hat\epsilon = \epsilon_u + w(\epsilon_c - \epsilon_u)$` 및 “$w=1$ recovers ordinary conditional sampling”; `:43` — `$\tilde\epsilon=(1+w)\epsilon_c-w\epsilon_u$`.
- 문제: 두 식은 모두 쓰이는 관례지만 같은 $w$가 아니다. 첫 식은 $w=0$이 무조건부, $w=1$이 조건부이고, 둘째 식은 $w=0$이 조건부다. 뒤의 “typical $w\sim5$–7.5”도 어느 관례인지 불명확해져 초보자가 코드를 틀리게 옮길 수 있다.
- 구체 수정안: 한 관례만 본식으로 채택한다. 예: $\epsilon_{cfg}=\epsilon_u+s(\epsilon_c-\epsilon_u)$, $s=1$ 조건부, 보통 $s>1$ 외삽. 다른 관례는 “일부 논문은 $w=s-1$로 써 $(1+w)\epsilon_c-w\epsilon_u$라 표기”라는 한 문장으로 병기한다. 영어·한국어와 전형값의 기호를 모두 `s`로 통일한다.
- 근거 신뢰도: **본문 확인**.

### papers-policy-003 — Flow Matching의 소수 스텝 설명이 필요한 조건을 지움 (P1)

- 위치·인용: `content/01-canonical-papers/notes/6-diffusion/flow-matching.md:67` — “The number of steps is not a property of the model but of the path's curvature”; `:72` — “straighter … permits far fewer inference steps.” 한국어 `:146`도 “스텝 수는 모델의 성질이 아니라 경로의 곡률이 정한다.”
- 문제: 곡률은 중요한 요인이지만 필요 스텝 수는 학습된 벡터장의 오차·매끄러움/강성, 솔버 차수, 허용 오차에도 좌우된다. 더구나 샘플별 조건부 직선 경로와 학습 후의 주변 확률 흐름이 항상 같은 직선이라는 인상을 준다. “왜 몇 스텝으로 되는가”를 Working 수준에서 진단하려는 독자에게 단일 원인 설명은 위험하다.
- 구체 수정안: 도식 마지막을 “경로 곡률이 작으면 큰 스텝이 *가능해지지만*, 실제 NFE는 벡터장 오차·강성·솔버에도 좌우된다”로 바꾼다. OT식 조건부 경로와 유도되는 주변 벡터장을 한 문장으로 구분하고, “few-step은 자동 보장이 아니라 경험적으로 확인할 항목”이라는 현재 on-ramp의 좋은 단서를 본문에도 반복한다.
- 근거 신뢰도: **본문 확인**, 단 수학적 엄밀한 표현은 **추가검증 필요**.

### papers-policy-004 — Dreamer가 RSSM 두 경로를 묻지만 설명하지 않음 (P2)

- 위치·인용: `content/01-canonical-papers/notes/5-world-models/dreamer.md:176` — “Explain why the RSSM needs both a deterministic and a stochastic path”; 정작 방법 `:44`–`:46`은 “RSSM world model”이라고만 쓴다.
- 문제: PlaNet을 읽었다는 암묵적 전제 없이는 독자가 체크 항목에 답할 수 없다. Dreamer는 Working 페이지이므로 입력·상태·학습 신호를 스스로 복원할 최소 설명이 필요하다.
- 구체 수정안: v1 항목 뒤에 “$h_t$는 GRU의 결정론적 기억, $z_t$는 관측으로 갱신되는 확률적 상태이며, 전자는 이력을 보존하고 후자는 불확실성과 다봉성을 담는다”를 영어·한국어로 2문장 추가하고 PlaNet 링크를 붙인다.
- 근거 신뢰도: **본문 확인**.

### papers-policy-005 — π0 영어 핵심 주장 박스가 미완 문장임 (P2)

- 위치·인용: `content/01-canonical-papers/notes/4-vla/pi0.md:96`–`:103` — “the gap is the honest”에서 끝난다. 대응 한국어 `:175`–`:179`는 “그 격차가 정직한 현재 수준이다”까지 완결된다.
- 문제: 영어 독자는 독립 평가의 결론과 callout 경계를 잃는다. 양언어 내용 일치도 깨진다.
- 구체 수정안: 영어 끝을 “the honest picture of the current capability level.”로 완결하고 callout 다음 빈 줄을 유지한다. 가능하면 제3자 연구 서지 링크도 같은 박스에 붙인다.
- 근거 신뢰도: **본문 확인**.

### papers-policy-006 — “Named the field”는 역사적 범위를 과장할 가능성이 큼 (P2)

- 위치·인용: `content/01-canonical-papers/notes/5-world-models/world-models.md:68` — “Named the field.”; 한국어 `:125` — “분야에 이름을 붙였다.”
- 문제: “world model”은 2018년 이전에도 사용된 용어이므로, 논문의 영향과 용어 창시를 혼동할 수 있다. 논문이 현대 딥러닝/RL 계보를 대중화·정형화했다는 주장과는 별개다.
- 구체 수정안: “Popularized the modern deep-learning V/M/C formulation of world-model agents” / “현대 딥러닝 기반 V/M/C 월드모델 에이전트 구성을 대중화했다”로 좁힌다.
- 근거 신뢰도: **추가검증 필요**(이번 감사에서는 역사적 원 출처 확인 생략).

### papers-policy-007 — 주택 sim-to-real 결과를 건설 현장에 같은 숫자로 외삽 (P2)

- 위치·인용: `content/01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav.md:122` — “현장 시뮬레이터에서만 검증된 정책은 반증되기 전까지 23% 영역에 있다고 가정해야 한다.”
- 문제: 23%는 특정 ObjectNav 방법·주택·프로토콜의 결과다. “현장은 더 어렵다”는 정성적 경고는 타당해도 동일 수치 영역을 prior처럼 적용하면 방법/도메인/지표가 바뀐 외삽이 된다. 앞선 `:114`–`:116`의 좋은 범위 제한과도 긴장한다.
- 구체 수정안: “실배치 성능을 미확인으로 두고, 주택 연구에서 관찰된 큰 하락을 위험 근거로 삼아 동일한 실제 현장 시험을 요구해야 한다”로 교체한다. 23%는 원 실험을 설명할 때만 유지한다.
- 근거 신뢰도: **본문 확인**.

### papers-policy-008 — World Models·Diffusion index가 ‘지도’ 역할을 못 함 (P2)

- 위치·인용: `content/01-canonical-papers/notes/5-world-models/index.md:8` — “읽기 순서는 … 핵심 논문 리스트를 따르라”; `content/01-canonical-papers/notes/6-diffusion/index.md:8`도 같은 한 문장이다. 두 파일 frontmatter `:4`는 “choose reading order, reading volume, and evidence checks”를 목표로 둔다.
- 문제: 초보자는 외부 목록으로 이동해야 할 뿐, 무엇을 위해 어떤 갈래를 읽는지 판단할 축이 없다. 반면 VLA index는 행동 표현이라는 비교축을 제공해 모범이 된다.
- 구체 수정안: 새 과목을 늘리지 말고 각 index에 5~7줄짜리 최소 경로만 추가한다. World Models: `World Models→PlaNet→Dreamer`(제어용 잠재모델), `Sora/Genie→Cosmos`(비디오/파운데이션), `JEPA`(비생성 대안). Diffusion: `VAE/GAN→DDPM→DDIM/Score-SDE→LDM/DiT→Flow Matching`, 로봇 독자는 `DDPM→Diffusion Policy→Flow Matching→π0`로 표시한다. 각 경로에 Literacy/Working 멈춤점을 한 줄씩 둔다.
- 근거 신뢰도: **본문 확인**.

### papers-policy-009 — 임피던스 제어의 구현 조건을 절대 명제로 제시 (P2)

- 위치·인용: `content/01-canonical-papers/notes/7-robotics/hogan-impedance.md:44` — “Impedance control **needs a torque-controlled, backdrivable arm**”; 한국어 `:83` — “요구한다.”
- 문제: 직접적·고충실도 임피던스 구현에는 매우 중요한 조건이지만, 위치/속도 인터페이스 위의 외부 루프나 내장 컴플라이언스로 제한된 임피던스 거동을 구현하는 사례까지 불가능하다고 읽힌다. 초보자는 “임피던스/어드미턴스” 구분을 하드웨어 이분법으로 외울 위험이 있다.
- 구체 수정안: “Direct, high-bandwidth impedance control generally requires torque access and suitable backdrivability; stiff position-controlled arms often use admittance or an inner-loop approximation, with a narrower renderable range”처럼 범위를 명시한다.
- 근거 신뢰도: **추가검증 필요**(니치 제어 구현 범위의 원 출처 확인 생략).

### papers-policy-010 — BADGR의 ‘선호 대 cost map’ 대비가 잘못된 질문을 만듦 (P2)

- 위치·인용: `content/01-canonical-papers/notes/9-navigation/badgr.md:72` — “what the preference channel buys you that a cost map does not”; 한국어 `:122`도 동일.
- 문제: cost map도 사용자 선호·금지 비용을 표현할 수 있다. BADGR의 차별점은 “선호를 표현할 수 있음” 자체가 아니라, 후보 행동의 학습된 사건 예측과 사용자 효용을 분리해 같은 예측 모델을 다른 목적에 재사용하는 데 있다. 현재 질문은 고전 비용 지도를 부당하게 약화해 가르친다.
- 구체 수정안: 체크 문항을 “학습된 event predictor와 user-specified cost/preference를 분리하면, 모델을 재학습하지 않고 목적을 어떻게 바꿀 수 있는가?”로 교체한다. 건설 예시는 geometry-only occupancy map과의 대비라고 명시한다.
- 근거 신뢰도: **본문 확인**.

## 잘 된 부분

- **주장과 측정의 분리:** Octo·robomimic·Cosmos·Genie·BADGR·VLFM 등에서 “초록에 있는 숫자/없는 숫자”를 명시해 숫자 재인용 오류를 강하게 예방한다.
- **양언어 구조:** 대부분 영어와 한국어가 항목·한계·체크리스트까지 대응하며, 번역도 직역보다 개념 역할을 보존한다.
- **학습 경로:** 각 노트의 Math on-ramp는 선수지식을 과도하게 확장하지 않고 실제 병목 하나나 둘로 좁힌다. DDPM의 2-step Gaussian 합성, SayCan의 점수 곱, UMI의 상대 좌표는 특히 좋은 온램프다.
- **방법/실험/가정 문해력:** Open X-Embodiment의 판본 함정, Dex-Net의 analytic label=assumption, GelSight의 geometry measured/force inferred, VLN-CE의 hidden benchmark assumptions는 연구 문해력 목표에 직접 기여한다.
- **선택 영역 Working 가능성:** DDPM, Flow Matching, Diffusion Policy, OXE, UMI, HIL-SERL, ConceptGraphs처럼 입력→표현/목표→출력→평가→실패점을 한 페이지에서 추적할 수 있는 노트는 원 논문을 펼칠 준비를 충분히 만든다. 다만 위 P1을 먼저 고치고, 실제 Working 전환 시 원 논문의 도식·방법·주요 표 한 개는 직접 확인해야 한다.

## 파일별 읽기 상태와 발견 ID

상태 `완독`은 Markdown 본문을 첫 줄부터 마지막 줄까지 읽었음을 뜻한다. `—`는 별도 발견 없이 만족한 문서다.

| 파일 | 상태 | 발견 ID |
|---|---|---|
| `4-vla/act.md` | 완독 | papers-policy-001 |
| `4-vla/dagger.md` | 완독 | — |
| `4-vla/diffusion-policy.md` | 완독 | — |
| `4-vla/gr00t-n1.md` | 완독 | — |
| `4-vla/index.md` | 완독 | — |
| `4-vla/octo.md` | 완독 | — |
| `4-vla/open-x-embodiment.md` | 완독 | — |
| `4-vla/openvla.md` | 완독 | — |
| `4-vla/pi0.md` | 완독 | papers-policy-005 |
| `4-vla/robomimic.md` | 완독 | — |
| `4-vla/rt-1.md` | 완독 | — |
| `4-vla/rt-2.md` | 완독 | — |
| `4-vla/saycan.md` | 완독 | — |
| `5-world-models/cosmos.md` | 완독 | — |
| `5-world-models/dreamer.md` | 완독 | papers-policy-004 |
| `5-world-models/genie.md` | 완독 | — |
| `5-world-models/index.md` | 완독 | papers-policy-008 |
| `5-world-models/jepa.md` | 완독 | — |
| `5-world-models/planet.md` | 완독 | — |
| `5-world-models/sora.md` | 완독 | — |
| `5-world-models/world-models.md` | 완독 | papers-policy-006 |
| `6-diffusion/classifier-free-guidance.md` | 완독 | papers-policy-002 |
| `6-diffusion/controlnet.md` | 완독 | — |
| `6-diffusion/ddim.md` | 완독 | — |
| `6-diffusion/ddpm.md` | 완독 | — |
| `6-diffusion/dit.md` | 완독 | — |
| `6-diffusion/flow-matching.md` | 완독 | papers-policy-003 |
| `6-diffusion/gan.md` | 완독 | — |
| `6-diffusion/index.md` | 완독 | papers-policy-008 |
| `6-diffusion/latent-diffusion.md` | 완독 | — |
| `6-diffusion/score-sde.md` | 완독 | — |
| `6-diffusion/vae.md` | 완독 | — |
| `7-robotics/anygrasp.md` | 완독 | — |
| `7-robotics/dex-net-2.md` | 완독 | — |
| `7-robotics/gello.md` | 완독 | — |
| `7-robotics/gelsight.md` | 완독 | — |
| `7-robotics/hil-serl.md` | 완독 | — |
| `7-robotics/hogan-impedance.md` | 완독 | papers-policy-009 |
| `7-robotics/index.md` | 완독 | — |
| `7-robotics/mobile-aloha.md` | 완독 | — |
| `7-robotics/umi.md` | 완독 | — |
| `7-robotics/vision-and-touch.md` | 완독 | — |
| `9-navigation/anymal-parkour.md` | 완독 | — |
| `9-navigation/badgr.md` | 완독 | papers-policy-010 |
| `9-navigation/clio.md` | 완독 | — |
| `9-navigation/conceptgraphs.md` | 완독 | — |
| `9-navigation/gervet-real-world-objectnav.md` | 완독 | papers-policy-007 |
| `9-navigation/index.md` | 완독 | — |
| `9-navigation/lee-quadruped-terrain.md` | 완독 | — |
| `9-navigation/miki-perceptive-locomotion.md` | 완독 | — |
| `9-navigation/navid.md` | 완독 | — |
| `9-navigation/rma.md` | 완독 | — |
| `9-navigation/semexp.md` | 완독 | — |
| `9-navigation/uni-navid.md` | 완독 | — |
| `9-navigation/vint-nomad.md` | 완독 | — |
| `9-navigation/vlfm.md` | 완독 | — |
| `9-navigation/vln-ce.md` | 완독 | — |
| `9-navigation/wild-visual-navigation.md` | 완독 | — |

## 범위와 검증 한계

- 원 논문 58편을 전수 fact-check하지 않았다. 페이지 내부 모순·교육 설계 문제는 본문 확인으로 판단했고, 역사·니치 제어 사실 두 건은 추가검증 필요로 남겼다.
- `vision-and-touch.md`의 논문 정체성과 큰 주장(자기지도 다중감각 표현, peg insertion, 시뮬레이션·실기 평가)은 공식 arXiv 초록으로 제한 확인했지만, 노트에 든 세부 pretext-task 예시는 초록만으로 검증되지 않아 별도 사실 판정에 쓰지 않았다.
- 범위 밖 페이지는 링크 문맥상 필요한 존재만 확인했으며 별도 정독 대상으로 세지 않았다.
- 문서 길이·수식 수를 깊이의 대리값으로 쓰지 않았다. 실제 판단 기준은 독자가 용어, 식의 역할, 방법의 입출력, 실험 단위, 가정과 실패 범위를 설명·선택·진단할 수 있는가였다.
