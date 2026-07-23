---
title: 9. Study Log
tags: [log]
---

무엇을 읽고 공부했는지 기록하는 일지. 일주일에 한 번이라도 좋으니 꾸준히 남긴다.
나중에 다시 보면 "그때 내가 뭘 몰랐는지"가 보여서 복습 지점을 찾기 좋다.

## 2026-07

### 2026-07-24 (건설 트랙 완성 — 코퍼스 기반 확충 마무리)

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
