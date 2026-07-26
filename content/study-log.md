---
title: 9. Study Log
tags: [log]
---

무엇을 읽고 공부했는지 기록하는 일지. 일주일에 한 번이라도 좋으니 꾸준히 남긴다.
나중에 다시 보면 "그때 내가 뭘 몰랐는지"가 보여서 복습 지점을 찾기 좋다.

## 2026-07

### 2026-07-26 (교차 검증 수리 + 제어 트랙 자립화 + 이중언어 완결)

전 페이지 정독 평가에서 나온 항목을 전부 반영했다.

- **개념 페이지가 자기 논문 노트를 반박하던 3건 교정** — 위키 방법론의 신뢰성 문제라 최우선:
  [[05-construction-robotics/earthmoving-heavy-machinery|토공]]의 ExT "~100시간"을 논문 검증값(과제당 15만 에피소드 ≈ 실기계 30일, RTX 3090 2시간 생성, 실기계 전이는 *사전학습* 정책)으로,
  [[05-construction-robotics/hrc-worker-centered|HRC]]의 Lasota & Shah "실제 자동차 조립 라인 배치"를 "BMW *테스트 환경*(저자가 실제 공장 배치를 대표하지 않는다고 명시)"으로,
  토공 §5의 근거 없는 운용 묘사("지오펜스·공공 통행 없음·직원 감독")를 논문이 실제로 말하는 범위로.
- **[[04-robotics/control-theory-ce397|5. 제어 이론]] 전면 재작성** — 외부 패킷 목차였던 페이지를 자체 완결 가이드로: 피드백이 사는 것/지불하는 것, 상태공간 변환, 모드와 행렬 지수, 연속·이산 안정성, 전달함수·극점과 $\zeta,\omega_n$에서 정착 시간·오버슈트 뽑기, 가제어성·가관측성 랭크 검정(가제어/불가제어 예제 각 1), 극점 배치 계산 예제, PID와 와인드업, 관측기·분리 원리, 선형화·게인 스케줄링·포화, 제어 주장 읽기 표, 자가점검 5문 + 정답. 공업수학을 한 번 본 독학자 기준으로 외부 자료 없이 통과 가능.
- **제어 서브트랙 5~8번에 선수지식 콜아웃 신설** (로보틱스·건설 22페이지 중 유일하게 없던 묶음): control→LQR→MPC→convex MPC가 서로를 명시적으로 가리키도록.
- **고아 챕터 3개 해소** — MR 6장(IK)·9장(궤적 생성)·13장(바퀴 로봇)은 코퍼스 전체에서 인바운드 링크가 0이었다. 계획·로봇 시스템·상태 추정·현장 인식·SE(3)에서 역링크를 걸어 전 페이지 인바운드 ≥ 1.
- **이중언어 완결**: foundations 6페이지에 EN 정답 추가, MR 11장 전부의 "시작 전 점검"·자가점검·정답 병기, [[03-deep-learning/lineage|DL 계보]] 영어 절 신설(홈 4번 진입 경로), [[glossary|용어집]] 전 항목 영어 병기, canonical list 서문 영어, **논문 노트 86편의 exit-test 체크리스트 전량과 claim box 전량 병기**.
- 잔여 정리: 8-construction 인덱스 frontmatter 보강, 공업수학 §8–9 → 제어 이론 본문 링크(제목 안 위키링크 금지 규약 준수).
- **완료 확인 중 추가 발견 2건** (전수 스크립트가 잡음): [[00-study-depth-guide|깊이 가이드]]와 [[08-research-radar/index|Research Radar]]의 영어 절이 `## English`로 감싸이지 않아 하위 절이 `## 한국어`의 형제로 앉아 있었고, Radar는 **영어 Methodology가 한국어 절 뒤에** 통째로 붙어 있어 한국어 독자가 번역 안 된 절로 끝나고 있었다. 둘 다 감싸고 h3로 강등, Radar에 `### 사용법`·`### 방법론` 미러 추가 → 코퍼스 전역 "한쪽 언어만 있는 페이지" 0.
- `resource` 태그 정리: 포인터 스텁이던 시절에 붙은 라벨을 [[04-robotics/lqr-lqg|LQR/LQG]]·[[04-robotics/mpc|MPC]]에서 제거(둘 다 이제 자체 완결 가이드). 실제 외부 자료 포인터인 [[04-robotics/convex-mpc-legged|convex MPC]]·[[04-robotics/modern-robotics-book|MR 책 가이드]]에는 유지. 태그를 소비하는 코드가 없음을 확인한 뒤 라벨만 수정.

**검증 방법 메모** — 이번에 실제로 문제를 잡아낸 것은 눈이 아니라 스크립트다: ① 위키링크 in/out-degree 계산(고아 3개 발견) ② 논문 노트별 claim box·체크리스트의 언어 판정(31 + 약 300건 발견) ③ `## English`/`## 한국어` 짝 검사(위의 2건 발견). 다음 감사 때도 이 셋을 먼저 돌릴 것.

### 2026-07-24 (독학의 벽 9곳 낮추기)

교육 평가가 "외부 자료 없이는 못 넘는다"고 지목한 지점 — 주변 페이지가 유도를 기대하도록 훈련시켜 놓고 결과만 단정하던 곳 — 을 EN·KR 양쪽에서 메웠다.

- **정보이론 §5 ELBO**: 숨어 있던 대수를 노출 — $\log\frac{p(x|z)p(z)}{q}$를 재구성항 + (−KL)로 항별 분할해 우변이 허공에서 나오지 않도록
- **선형대수 §5 가제어성**: 랭크 조건을 단정 대신 직관으로 구축(입력이 $B$ 열 방향으로 밀고, 동역학이 도달 범위를 $AB$, $A^2B$로 회전)
- **공업수학 §8–9**: 가장 어려운 절에 자가점검이 0개였던 것 → ODE 안정성·극점/반평면 문제 2개와 정답 추가
- **RL 기초 §6**: 모방학습 7개 밀집 불릿을 3개 라벨 묶음으로(목적함수+covariate shift / 데이터셋 읽기 / 표현력 헤드가 존재하는 이유)
- **DDIM**: core 디퓨전 노트 중 유일하게 램프가 없던 것 → 결정론적 단계를 구체적으로(노이즈 예측 → 함의된 $x_0$ 읽기 → 낮은 수준으로 재노이즈)와 왜 허용되는지(손실이 marginal만 제약)
- **미적분·역전파**: "위의 각 단계가 곧 VJP 하나다" 연결문으로 손 계산 예제와 §2 추상 정의를 융합
- **최적화 §4**: "왜 제약을 목적함수에 더하나" — 최적점에서 $\nabla f$가 $\nabla g$와 반평행 → $\nabla(f+\lambda g)=0$
- **SE(3) §4**: 반대칭 형태 유도($R^\top R=I$ 미분 → $\dot R+\dot R^\top=0$)
- **MR 8장**: 진자 1링크로 $M/c/g$ 접지($\tau=ml^2\ddot\theta+mgl\sin\theta$), 왜 1링크는 코리올리가 0이고 2링크에서 켜지는지

### 2026-07-23 (최종 편집 3종 — 깊이 정직화·핵심 보강·정밀 교정)

- **깊이 표시 2층 분리**: `study-depth`(권장 목표) vs `wiki-support`(페이지 자체 제공 깊이) — [[00-study-depth-guide|가이드]]에 규약 문서화, MR 8~12장·제어이론 등 격차 페이지에 `wiki-support: Literacy` 표시
- **핵심 Working 페이지 4개 심층 보강**: [[04-robotics/mpc|MPC]](QP 볼록성 조건, stacked/condensed, infeasibility·softening·warm start, 모델 불일치, 선형/NMPC/접촉), [[04-robotics/lqr-lqg|LQR/LQG]](리카티 구조 읽기, 안정화 가능성·검출 가능성, Q/R 예제, LQG 무여유), [[01-canonical-papers/notes/8-construction/heap|HEAP]](구동 개조·센싱·소프트웨어 스택·증거 성격·공백 4종), [[01-canonical-papers/notes/8-construction/ext|ExT]](시연 생성 3소스·사전학습·SFT/RLFT·전이 증거)
- **절대 표현 정밀 교정 6건**: Transformer "essentially all"→지배적+예외 명시, CLIP 개념 학습 단정→해석+경쟁 설명, FM 직선 경로→가능 조건(보장 아님), "objective of choice"→지배적 목적함수 중 하나, 고차원 직교성→검색 가능성의 한 이유(관련쌍 점수는 학습의 성질), 칼만 vs 저역통과→모델 조건부
- MR 책 가이드의 "챕터 노트 추가 예정" 잔재 제거

### 2026-07-23 (건설 트랙 완성 — 코퍼스 기반 확충 마무리)

- 5클러스터 조사(미시간·UIUC 디아스포라·GT/TAMU/CMU·유럽·로보틱스史+산업)의 잔여 작업 완료:
- **신규 논문 노트 12편**: [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]](Baidu, sim 검증), [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL 굴착]], [[01-canonical-papers/notes/8-construction/cho-slam|Cho SLAM 2018]], [[01-canonical-papers/notes/8-construction/han-welding|Han 용접]], [[01-canonical-papers/notes/8-construction/aerial-am-2022|Nature 공중 AM]], [[01-canonical-papers/notes/8-construction/liang-hrc-survey|Liang HRC 서베이]], [[01-canonical-papers/notes/8-construction/liu-jebelli-bci|BCI 원격조작]], [[01-canonical-papers/notes/8-construction/lasota-shah|Lasota & Shah]], [[01-canonical-papers/notes/8-construction/park-nl|Park NL]], [[01-canonical-papers/notes/8-construction/yu-imitation|Yu 모방학습]], [[01-canonical-papers/notes/8-construction/lundeen-2019|Lundeen]], [[01-canonical-papers/notes/8-construction/liang-lfd|Liang LfD]] — 8-construction 총 22노트
- 기존 6노트(AES·돌담·Feng·Stentz·Wang DT·휠로더) 하우스 스타일 승격: 완전 한국어 병기, 연결, 수치 심층화
- 스트림 5페이지(조립·인식·HRC·DT·sim-to-real)에 Depth target·자가 점검·KR 다이어그램 복원 + 전 스트림↔노트 양방향 링크
- 선행 노트 4편(PPO·SAC·PointNet·SayCan) 완전 통합: opener·위키링크·RL 기초 §4 on-ramp·GAE 단락
- 오류 수정: Tang DOI(2010), ext.md 구식 스트림 참조, Radar 빈 캐시 가드, iframe 높이, LDM 깊이(Literacy)


### 2026-07-23 (전역 학습 깊이 + 다중 범위 Research Radar)

- Study intent를 Radar의 임시 필터에서 제거하고 [[00-study-depth-guide|0. Study Depth Guide]]와 모든 실질 학습 페이지의 `study-depth`·`depth-goal`·`mastery-when` 속성으로 이동
- 140개 foundations·개념·논문·로보틱스·건설·research-practice 페이지에 Literacy/Working 기본 목표와 Mastery 승격 조건을 명시; 템플릿과 배포 QA에도 강제
- Radar 온톨로지를 59개 토픽·10개 겹치는 연구 관점으로 확장: Deep Learning, Computer Vision, Generative Models, Multimodal, Physical AI, World Models, VLM & VLA, Robot Learning, Robotics, Construction Physical AI
- 단일 폴더 분류를 폐기하고 Diffusion Policy처럼 여러 분야의 합류점이 복수 관점에 동시에 나타나는 multi-label 구조 채택
- 건설 신호는 `construction robotics` 검색이 아니라 작업·장비·자산·재료·현장 맥락 × 로봇·자율성·인식·계획·제어·HRI의 교차 조건으로 검출; Automation in Construction와 Construction Robotics의 Crossref 메타데이터 추가
- 2021–2025 출판 논문 58,439편, 59개 토픽으로 재집계; SLAM의 일반 `localization` 오탐과 건물 설계 RL의 embodied 오탐을 제거하고 대표 표본·필터·캐시 갱신을 브라우저에서 검증

### 2026-07-23 (Research Radar 초기판)

- 문해력 획득 이후 연구 문제를 고르는 단계의 의사결정 도구 [[08-research-radar/index|Research Radar]] 신설
- 2021–2025 NeurIPS·ICML·ICLR·CVPR·ICRA·CoRL 정식 proceedings 55,642편을 DBLP 서지 메타데이터로 수집; arXiv·워크숍 제외
- 규모×상승속도 사분면, 절대 규모/Fast Rising/Early Signals 순위, scope·학습 깊이·signal 필터, 연도별 추세, 대표 논문·근거 패널 구현
- 제목 기반 다중 태그 taxonomy, 연도별 전체 논문 수 정규화, momentum·burst·venue breadth·small-sample shrinkage 적용
- OpenAlex의 연도별 conference-source 분할이 가짜 추세를 만들 수 있어 집계 소스로 사용하지 않고, DBLP 연도별 proceedings를 로컬 캐시 후 분석하는 보수적 경로 채택
- 현재 제한: 제목에 방법명이 없는 논문은 누락될 수 있고 기관 정규화·기술적 논쟁 자동 후보는 후속 검증 대상; 화면에 audit와 confidence 공개

### 2026-07-23 (건설로봇 코퍼스·계보 재구성)

- 기술·학술·시스템의 세 계보로 분야를 재구성하고 미시간/UIUC 디아스포라, ETH 패브리케이션·굴착 나무, CMU 중장비 기원, 연구→산업 연결을 검증
- 희망적 주제 목록을 코퍼스에서 도출한 5개 연구 스트림+2개 횡단층으로 교체; 토공, 조립, 현장 인식, 작업자 중심 HRC, 디지털 트윈, sim-to-real, 산업 배치의 이중언어 개념 페이지 추가
- canonical 8번을 18편의 앵커·supporting 문헌으로 확장하고 CMU 트럭 적재, Baidu AES, 휠로더 RL, 비전 유도 조립, 돌담, BIM 디지털 트윈의 상세 노트 추가
- ExT·건설 physical AI의 누락 선행 재료 PPO, SAC, PointNet/PointNet++, SayCan을 추가

### 2026-07-23 (7종 전수 감사 + 프로필 기준 티어 조정)

- 건설로봇 제외 전 콘텐츠를 7개 영역으로 병렬 전수 감사 (탐색 계층 / foundations / 논문 노트 2조 / 로보틱스 / research practice / 커리큘럼 적합성)
- BLOCKING 2건 수정: softmax를 [[02-foundations/engineering-math|0.5 §10]]에 정의(12곳에서 정의 없이 사용되던 것), 로보틱스 한국어 인덱스에 3.5 기하 인식 추가
- 사실 교정: ViT 88.55%는 H/14(L/16은 87.8), Bahdanau는 미지단어 제외 부분집합에서만 SMT 대등, I3D 원 논문은 71–75%, Qwen2-VL은 2B/7B/72B, Genie 학습 데이터는 ~24.4만 시간 크롤 중 ~3만 시간 필터
- 탐색 수리: 섹션 인덱스 2곳이 자기 하위 페이지 링크, canonical list 영어 범례 추가·study guide를 트랙 순서로 재배열, π0→Flow Matching 직결(Score SDE 우회 제거), 전방 참조 선수지식 2건 완화
- 교육 보강: ELBO의 곱하고-나누기 단계 명시, 시행 수 가늠 도구(±1/√n, rule of three), 리뷰어 응답 예문, PaliGemma 기구·한계 보강, VGGT에 기하 인식 on-ramp
- **프로필 기준 티어 조정** (미국 상위 공대 건설 physical AI 대학원생 기준): BERT·GPT-3·InstructGPT·I3D·PlaNet·Score-SDE·LDM ◐→○, Cosmos ★→◐ — 로봇 논문에서 한 줄 조상 인용 수준인 항목들의 읽기 부담 축소
- 예정: PPO(◐)·SAC(○)·PointNet/++(○)·SayCan(○) 노트와 sim-to-real 학습 가이드를 건설로봇 확충과 함께 추가 (ExT 계열 읽기의 선행 재료)

### 2026-07-23 (공통 커리큘럼 공백 보완)

- 외부 점검(달성도 ~92%)이 지목한 세 공백을 보완:
- [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] 신설 — 핀홀 모델·intrinsics/extrinsics·깊이 복원(스테레오 계산 예제)·포인트 클라우드·registration/ICP·보정 5종·reprojection error·기하+딥 인식의 역할 구분
- [[04-robotics/robot-systems-deployment|Robot Systems]] §6 행동 오케스트레이션 추가 — FSM·behavior tree·precondition/postcondition·timeout/retry/fallback·action server; "로봇이 회복했다"가 어느 계층의 일인지 읽는 법
- [[02-foundations/rl-basics|RL 기초]] §6을 모방 학습 도구 상자로 확장 — BC 목적함수, covariate shift와 오차 누적, DAgger, 시연 수집과 동기화, 행동 청킹, 다봉 시연, 데이터 큐레이션, 오프라인 RL과의 구분; VLA 노트 진입 사슬 연결
- 용어집 확충 — Intrinsics/Extrinsics·Geometric/Deep perception·State machine/Behavior tree (혼동 쌍), ICP·Reprojection error·Behavior tree (사전)

### 2026-07-23 (robot systems literacy와 research practice 확장)

- **4. Robotics & Control**을 **4. Robotics & Physical Systems**로 확장
- State Estimation/Localization/SLAM, Planning & Decision-Making, Contact/Force/Tactile Interaction, Robot Systems/Embodiment/Deployment, HRI & Safety의 다섯 literacy guide 추가
- **6. Research Practice** 신설: Research Questions & Claims, Experimental Design & Reproducibility, Failure Analysis & System Evaluation, Scientific Writing & Peer Review
- Foundations 이후 학습 구조를 AI model literacy와 robot systems literacy의 병렬 경로로 나누고 Physical AI·Construction Robotics에서 합류하도록 연결
- Probability, Optimization, Signal Processing, RL, SE(3), ML Practice, Modern Robotics, LQG, MPC에 직접 교차 링크를 추가하고 glossary를 estimation·planning·contact·systems·safety·reproducibility까지 확장
- 새 상세 페이지 9개에 English/한국어, After reading, Self-check가 유지되는지 deployment QA에서 자동 검사

### 2026-07-22 (교육 설계 개편 — research-literacy curriculum)

- 사이트 목표를 명문화: **연구 문해력**(용어 친숙 + 논문의 문장·수식·주장·실험을 과장 없이 읽기)이 목표이며, 균일한 기술 숙달이 아님 — 홈에 목표 선언 추가
- [[01-canonical-papers/how-to-read|0. How to Read Papers]] 신설: 4단계 읽기 깊이(인지/독해/실무/숙달), 논문 문장의 문법(보장하지 않는 것 표), 수식 5질문, 회의주의자 체크리스트, 퇴장 시험
- 읽기 깊이 체계 도입: 핵심 논문 리스트 전체에 ★(원문 정독)·◐(노트+훑기)·○(계보용) 표시 — 이 기호는 권장 읽기 분량이지 숙련 수준이 아님
- 전체 63개 논문 노트에 "읽고 나면 말할 수 있어야 하는 것" 점검 추가; ★ 15편에는 "핵심 주장 읽는 법" 박스(제목의 주장을 어디까지 믿을지)와 수학 on-ramp 추가
- foundations에 선수 지식 박스·접이식 정답·계산 예제 보강; [[02-foundations/ml-practice|ML 실무]]에 평가 함정 섹션(체리피킹, 개루프/폐루프, 시드 분산 등) 추가
- [[05-construction-robotics/index|건설로봇]]에 11축 논문 읽기 틀 추가 (작업·신체·인식·표현·계획제어·자율·배포안전·평가 현실성·sim-to-real·실패 분석·생산성 비교)
- 정밀 편집 패스: 용어집 정의 교정(조건수·VLM/VLA·IL·Diffusion/FM·LQR), foundations 단정 완화(atan2, MLE 범위, ResNet 완화 표현, 민감도/정확도 구분), MR 12·13장 가정 명시, 계보도 실선 의미 완화, [[01-canonical-papers/notes/3-vlm/paligemma|PaliGemma]] 노트 신설(○)

### 2026-07-22 (초기 구축)

- 위키 개설: Obsidian + Quartz + GitHub Pages 구축
- 첫 논문 노트 작성: [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]]
- 기초 1차 배치 (2012→2016 연대순): [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/vgg|VGG]], [[01-canonical-papers/notes/1-foundations/bahdanau-attention|Bahdanau Attention]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]
- 계보도에 2012–2017 구간 추가 (CNN 갈래 + RNN 갈래 → Transformer 합류)
- 다음 읽을 것: Adam, BatchNorm, seq2seq, LSTM 또는 바로 ViT/CLIP
- 기초 섹션 완주 + Transformer 이후 진출 (총 12편 추가):
  기초 마무리 — [[01-canonical-papers/notes/1-foundations/lstm|LSTM]], [[01-canonical-papers/notes/1-foundations/seq2seq|seq2seq]], [[01-canonical-papers/notes/1-foundations/adam|Adam]], [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]
  Transformer 이후 — [[01-canonical-papers/notes/1-foundations/bert|BERT]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]], [[01-canonical-papers/notes/1-foundations/scaling-laws|Scaling Laws+Chinchilla]], [[01-canonical-papers/notes/1-foundations/vit|ViT]], [[01-canonical-papers/notes/1-foundations/mae|MAE]], [[01-canonical-papers/notes/1-foundations/lora|LoRA]], [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]], [[01-canonical-papers/notes/3-vlm/clip|CLIP]]
- VGGT(CVPR 2025 Best Paper) 확인 후 CV 섹션에 추가
- 다음: VLM 계열 (Flamingo, BLIP-2, LLaVA) 또는 디퓨전 계열 (VAE, GAN, DDPM)
- 노트 형식 개선: 모든 노트 첫 줄에 "저자, 학회 연도 — arXiv·PDF·Code" 표기; 폴더명 `01-canonical-papers`로 변경
- VLM 배치 완료: [[01-canonical-papers/notes/3-vlm/flamingo|Flamingo]], [[01-canonical-papers/notes/3-vlm/blip-2|BLIP-2]], [[01-canonical-papers/notes/3-vlm/llava|LLaVA]] — CLIP→연결자 설계 경쟁→지시 튜닝의 흐름; 다음은 VLA로 가는 관문 통과
- 다음: 디퓨전 계열 (VAE, GAN, DDPM, Score SDE) 또는 바로 VLA (RT-1, RT-2, Diffusion Policy)
- 기초 정리 페이지 3편 (reference 자료를 내 언어로 재구성): [[02-foundations/optimization|최적화]], [[02-foundations/probability|확률과 랜덤 프로세스]], [[02-foundations/signal-processing|신호처리]]
- 디퓨전 기초 배치: [[01-canonical-papers/notes/6-diffusion/vae|VAE]], [[01-canonical-papers/notes/6-diffusion/gan|GAN]], [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]], [[01-canonical-papers/notes/6-diffusion/score-sde|Score SDE]] — VAE(안정·흐릿) vs GAN(선명·불안정)의 긴장을 DDPM이 해소하고 Score SDE가 이론으로 통합
- 다음: VLA 진입 (RT-1, RT-2, Diffusion Policy, ACT) — 디퓨전 수학 준비 완료
- VLA 1차 배치: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]], [[01-canonical-papers/notes/4-vla/act|ACT/ALOHA]] — 로봇 데이터 스케일링(RT-1) → 웹 지식 전이(RT-2) → 다봉 행동 분포(DP) → 행동 청킹(ACT)
- 다음: VLA 2차 (Open X-Embodiment, Octo, OpenVLA, π0, GR00T N1)로 VLA 섹션 완주
- 기초 섹션 확장 (4편 추가, 총 7편 체계 완성): [[02-foundations/linear-algebra|선형대수]], [[02-foundations/calculus-backprop|미적분과 역전파]], [[02-foundations/information-theory|정보이론]], [[02-foundations/rl-basics|강화학습 기초]] — 위키의 모든 논문을 읽기에 충분한 배경 세트
- VLA 섹션 완주 (5편): [[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]], [[01-canonical-papers/notes/4-vla/octo|Octo]], [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]], [[01-canonical-papers/notes/4-vla/pi0|π0]], [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] — 데이터 풀링 → 오픈 모듈식 정책 → 오픈 VLA → flow matching 융합 → 휴머노이드 데이터 피라미드
- 다음: 월드모델 섹션 (World Models, PlaNet, Dreamer, JEPA, Genie, Sora, Cosmos)
- sudoremove.com 점검: 내용 상충 없음 확인; 배울 점으로 생태계 카탈로그 채택 → [[03-deep-learning/physical-ai-ecosystem|Physical AI Ecosystem]] 페이지 신설
- 선형대수 페이지에 제어이론 연결 섹션 추가 (상태공간, 고유값=안정성, 가제어성 랭크 조건)
- 월드모델 섹션 완주 (7편): [[01-canonical-papers/notes/5-world-models/world-models|World Models]], [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer v1–3]], [[01-canonical-papers/notes/5-world-models/jepa|JEPA 계열]], [[01-canonical-papers/notes/5-world-models/genie|Genie]], [[01-canonical-papers/notes/5-world-models/sora|Sora]], [[01-canonical-papers/notes/5-world-models/cosmos|Cosmos]] — 꿈속 훈련 → RSSM → 상상 속 actor-critic → 표현 공간 예측(반대 진영) → 인터넷 비디오에서 행동 발견 → 시뮬레이터 가설 → 인프라화
- 다음 후보: CV 나머지 (U-Net~VGGT) 또는 디퓨전 나머지 (DDIM, CFG, LDM, ControlNet, DiT, Flow Matching) 또는 건설로봇 서베이 수집
- CV 섹션 완주 (12편): U-Net, Faster R-CNN, YOLO, I3D/SlowFast, DETR, NeRF, Swin, DINO/DINOv2, SAM, 3DGS, Depth Anything, VGGT
- 디퓨전 섹션 완주 (6편): DDIM, CFG, Latent Diffusion, ControlNet, DiT, Flow Matching — 딥러닝 파트(섹션 1~6) 논문 노트 전부 완료 (총 58편)
- 방침: foundations 페이지들을 제어이론 교재 수준의 깊이로 증보하기로 함 (다음 작업)
- 남은 큰 덩어리: ① foundations 심화 증보 ② 건설로봇 서베이 수집(섹션 8) ③ 로보틱스/제어 노트(섹션 7)
- foundations 심화 증보 완료: 7개 페이지 전부 교재 수준으로 — 유도(정규방정식, KL 비음수성, 벨만, 정책 그래디언트), 계산 예제(2층 역전파, 합성곱, 베이즈 진단, KKT 투영, MPC-QP 정식화), 스스로 점검 문제 추가
- 남은 큰 덩어리: ① 건설로봇 서베이 수집(섹션 8) ② 로보틱스/제어 노트(섹션 7: Modern Robotics 챕터, LQR, MPC)
