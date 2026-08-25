---
title: 1. Canonical Paper List
tags: [moc, papers]
study-depth: Literacy
depth-goal: "Use this map or guide to choose reading order, reading volume, and evidence checks."
mastery-when: "Working and Mastery are assigned on the individual concept or paper pages."
---

## English

The reading backbone of this wiki: bible-tier and milestone papers per subarea, in rough
reading order. Check off as notes are written (one note per paper in `notes/`).
Recent-trend papers get appended over time via the tracking workflow.

## 한국어

이 위키의 중심이 되는 논문 목록: 분야별로 꼭 읽어야 할 기념비적 논문들을
대략적인 읽기 순서로 정리했다. 논문 노트를 작성하면 체크 표시를 남긴다
(`notes/`에 논문 하나당 노트 하나). 최신 논문은 트렌드를 따라가며 계속 추가한다.

---

**읽기 깊이 표시** ([[01-canonical-papers/how-to-read|0. How to Read Papers]] 참고):
★ 원문 정독 (방법·실험까지) · ◐ 노트 후 원문 훑기 · ○ 노트로 충분 (계보 이해)
— 이 기호는 **권장 읽기 분량**이지 숙련 수준이 아니다: ★를 정독해도 mastery(가정 비판·변형 설계)에 도달한 것은 아니다.
(EN: ★ read the original in full · ◐ read the note, then skim the original · ○ the note is enough. These marks are the *recommended reading amount*, not a mastery level.)
— Reading depths are tuned to the **construction physical-AI profile** (2026-07): the NLP-ancestor line (BERT, GPT-3, InstructGPT) and the deep generative-image papers (Score-SDE, LDM) are one-line citations in this field's papers, so they are ○; visual perception, VLA, and diffusion-policy mathematics keep their depth.
— 깊이 배정은 **건설 physical AI 프로필** 기준으로 조정했다(2026-07): NLP 조상 계열(BERT·GPT-3·InstructGPT)과 생성 이미지 심화(Score-SDE·LDM)는 이 분야 논문에서 한 줄 인용 수준이라 ○, 시각 인식·VLA·디퓨전 정책 수학은 유지.

## 1. Deep Learning Foundations

Chronological — the CNN and RNN branches start at ImageNet 2012 and merge at the Transformer in 2017. Keep the [[03-deep-learning/lineage|lineage map]] open.
시간순 정렬 — 2012년 ImageNet에서 시작해 CNN 계열과 RNN 계열이 2017년 Transformer에서 합류하는 흐름.

- [x] ○ [[notes/1-foundations/lstm|LSTM]] — *Long Short-Term Memory* (Hochreiter & Schmidhuber, Neural Computation 1997)
- [x] ○ [[notes/1-foundations/alexnet|AlexNet]] — *ImageNet Classification with Deep CNNs* (Krizhevsky et al., NeurIPS 2012)
- [x] ○ [[notes/1-foundations/seq2seq|seq2seq]] — *Sequence to Sequence Learning* (Sutskever et al., NeurIPS 2014)
- [x] ○ [[notes/1-foundations/bahdanau-attention|Bahdanau Attention]] — *NMT by Jointly Learning to Align and Translate* (ICLR 2015)
- [x] ○ [[notes/1-foundations/vgg|VGG]] — *Very Deep Convolutional Networks* (Simonyan & Zisserman, ICLR 2015)
- [x] ◐ [[notes/1-foundations/adam|Adam]] — *A Method for Stochastic Optimization* (Kingma & Ba, ICLR 2015)
- [x] ◐ [[notes/1-foundations/batch-norm|Batch Normalization]] (Ioffe & Szegedy, ICML 2015)
- [x] ◐ [[notes/1-foundations/resnet|ResNet]] — *Deep Residual Learning* (He et al., CVPR 2016)
- [x] ★ [[notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]] (Vaswani et al., NeurIPS 2017)
- [x] ○ [[notes/1-foundations/bert|BERT]] (Devlin et al., NAACL 2019)
- [x] ○ [[notes/1-foundations/gpt-3|GPT-3]] — *Language Models are Few-Shot Learners* (Brown et al., NeurIPS 2020)
- [x] ◐ [[notes/1-foundations/scaling-laws|Scaling Laws]] (Kaplan et al., 2020) + Chinchilla (Hoffmann et al., 2022)
- [x] ◐ [[notes/1-foundations/vit|ViT]] — *An Image is Worth 16x16 Words* (Dosovitskiy et al., ICLR 2021)
- [x] ◐ [[notes/1-foundations/mae|MAE]] — *Masked Autoencoders Are Scalable Vision Learners* (He et al., CVPR 2022)
- [x] ◐ [[notes/1-foundations/lora|LoRA]] — *Low-Rank Adaptation* (Hu et al., ICLR 2022)
- [x] ○ [[notes/1-foundations/instructgpt|InstructGPT/RLHF]] — *Training LMs to Follow Instructions* (Ouyang et al., NeurIPS 2022)
*(The two below are appended as prerequisites for the robotics track — an exception to the chronological order. · 로보틱스 트랙의 선행 재료로 부록처럼 추가 — 시간순 예외)*
- [x] ◐ [[notes/1-foundations/ppo|PPO]] — *Proximal Policy Optimization Algorithms* (Schulman et al., 2017) — ExT 등 simulator-expert/RLFT 레시피
- [x] ○ [[notes/1-foundations/sac|Soft Actor-Critic]] (Haarnoja et al., ICML 2018) — 연속 제어의 off-policy 기준선

## 2. Computer Vision

- [x] ◐ [[notes/2-computer-vision/u-net|U-Net]] (Ronneberger et al., MICCAI 2015)
- [x] ○ [[notes/2-computer-vision/faster-r-cnn|Faster R-CNN]] (Ren et al., NeurIPS 2015)
- [x] ◐ [[notes/2-computer-vision/yolo|YOLO]] (Redmon et al., CVPR 2016)
- [x] ○ [[notes/2-computer-vision/video-understanding|Video Understanding — I3D / SlowFast]] (2017–2019)
- [x] ◐ [[notes/2-computer-vision/detr|DETR]] — *End-to-End Object Detection with Transformers* (Carion et al., ECCV 2020)
- [x] ◐ [[notes/2-computer-vision/nerf|NeRF]] (Mildenhall et al., ECCV 2020)
- [x] ○ [[notes/2-computer-vision/swin|Swin Transformer]] (Liu et al., ICCV 2021)
- [x] ◐ [[notes/2-computer-vision/dino|DINO → DINOv2]] (Caron et al., ICCV 2021 · Oquab et al., TMLR 2024)
- [x] ◐ [[notes/2-computer-vision/sam|SAM]] — *Segment Anything* (Kirillov et al., ICCV 2023)
- [x] ◐ [[notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]] (Kerbl et al., SIGGRAPH 2023)
- [x] ◐ [[notes/2-computer-vision/depth-anything|Depth Anything]] (Yang et al., CVPR 2024)
- [x] ◐ [[notes/2-computer-vision/vggt|VGGT]] — *Visual Geometry Grounded Transformer* (Wang et al., CVPR 2025)
- [x] ○ [[notes/2-computer-vision/pointnet|PointNet / PointNet++]] (Qi et al., CVPR/NeurIPS 2017) — 건설 LiDAR·포인트 클라우드의 기초 문법

## 3. Vision-Language Models (VLM)

- [x] ★ [[notes/3-vlm/clip|CLIP]] — *Learning Transferable Visual Models From Natural Language Supervision* (Radford et al., ICML 2021)
- [x] ○ [[notes/3-vlm/flamingo|Flamingo]] (Alayrac et al., NeurIPS 2022)
- [x] ○ [[notes/3-vlm/blip-2|BLIP-2]] (Li et al., ICML 2023)
- [x] ◐ [[notes/3-vlm/llava|LLaVA]] — *Visual Instruction Tuning* (Liu et al., NeurIPS 2023)
- [x] ◐ [[notes/3-vlm/qwen-vl|Qwen-VL series]] (Qwen Team, 2023–2025) — representative open VLM line
- [x] ○ [[notes/3-vlm/paligemma|PaliGemma]] (Google, 2024) — 작은 오픈 VLM의 대표; π0의 백본

## 4. Vision-Language-Action (VLA) / Robot Learning

- [x] ○ [[notes/4-vla/saycan|SayCan]] — *Do As I Can, Not As I Say* (Ahn et al., CoRL 2022) — 언어 계획과 실행 가능한 skill의 접지
- [x] ◐ [[notes/4-vla/rt-1|RT-1]] — *Robotics Transformer* (Brohan et al., RSS 2023)
- [x] ★ [[notes/4-vla/rt-2|RT-2]] — *Vision-Language-Action Models* (Brohan et al., CoRL 2023)
- [x] ★ [[notes/4-vla/diffusion-policy|Diffusion Policy]] (Chi et al., RSS 2023)
- [x] ★ [[notes/4-vla/act|ACT / ALOHA]] — *Learning Fine-Grained Bimanual Manipulation* (Zhao et al., RSS 2023)
- [x] ◐ [[notes/4-vla/open-x-embodiment|Open X-Embodiment]] — the cross-embodiment dataset effort (ICRA 2024)
- [x] ◐ [[notes/4-vla/octo|Octo]] — open generalist robot policy (RSS 2024)
- [x] ◐ [[notes/4-vla/openvla|OpenVLA]] (Kim et al., CoRL 2024)
- [x] ★ [[notes/4-vla/pi0|π0]] — *A Vision-Language-Action Flow Model* (Physical Intelligence, RSS 2025)
- [x] ◐ [[notes/4-vla/gr00t-n1|GR00T N1]] — NVIDIA humanoid foundation model (2025)
- [x] ◐ [[notes/4-vla/robomimic|robomimic]] — Mandlekar et al., CoRL 2021 — 시연 데이터에서 무엇이 중요한가
- [x] ○ [[notes/4-vla/dagger|DAgger]] — Ross, Gordon & Bagnell, AISTATS 2011 — 복합 오차의 원리적 해법

## 5. World Models

- [x] ◐ [[notes/5-world-models/world-models|World Models]] (Ha & Schmidhuber, NeurIPS 2018)
- [x] ○ [[notes/5-world-models/planet|PlaNet]] (Hafner et al., ICML 2019)
- [x] ◐ [[notes/5-world-models/dreamer|Dreamer → DreamerV2 → DreamerV3]] (Hafner et al., 2020–2023, Nature 2025)
- [x] ◐ [[notes/5-world-models/jepa|JEPA line]] — LeCun 2022 position paper → I-JEPA (CVPR 2023) → V-JEPA / V-JEPA 2 (2024–2025)
- [x] ◐ [[notes/5-world-models/genie|Genie]] (Bruce et al., ICML 2024) → Genie 2 (2024)
- [x] ○ [[notes/5-world-models/sora|Sora]] — *Video Generation Models as World Simulators* (OpenAI, 2024)
- [x] ◐ [[notes/5-world-models/cosmos|Cosmos]] — world foundation models for physical AI (NVIDIA, 2025)

## 6. Diffusion & Generative Models

- [x] ◐ [[notes/6-diffusion/vae|VAE]] — *Auto-Encoding Variational Bayes* (Kingma & Welling, ICLR 2014)
- [x] ○ [[notes/6-diffusion/gan|GAN]] (Goodfellow et al., NeurIPS 2014)
- [x] ◐ [[notes/6-diffusion/ddpm|DDPM]] — *Denoising Diffusion Probabilistic Models* (Ho et al., NeurIPS 2020)
- [x] ○ [[notes/6-diffusion/score-sde|Score SDE]] — *Score-Based Generative Modeling through SDEs* (Song et al., ICLR 2021)
- [x] ◐ [[notes/6-diffusion/ddim|DDIM]] (Song et al., ICLR 2021)
- [x] ◐ [[notes/6-diffusion/classifier-free-guidance|Classifier-Free Guidance]] (Ho & Salimans, 2022)
- [x] ○ [[notes/6-diffusion/latent-diffusion|Latent Diffusion / Stable Diffusion]] (Rombach et al., CVPR 2022)
- [x] ○ [[notes/6-diffusion/controlnet|ControlNet]] (Zhang et al., ICCV 2023)
- [x] ◐ [[notes/6-diffusion/dit|DiT]] — *Scalable Diffusion Models with Transformers* (Peebles & Xie, ICCV 2023)
- [x] ◐ [[notes/6-diffusion/flow-matching|Flow Matching]] (Lipman et al., ICLR 2023)

## 7. Robotics & Physical Systems

**Core textbook and papers** (★◐○ = recommended reading amount · 읽기 분량)

- [x] ★ [[04-robotics/modern-robotics-book|Modern Robotics]] (Lynch & Park) — textbook with free official PDF & course links
- [x] ◐ [[04-robotics/mpc|MPC]] — Mayne et al., *Constrained MPC* (Automatica 2000) + study guide
- [x] ○ [[04-robotics/convex-mpc-legged|Convex MPC for legged robots]] — MIT Cheetah (IROS 2018 + open-access follow-up)

**Field surveys** (분야 서베이)

- ◐ **Trends and challenges in robot manipulation** — Billard & Kragic, *Science* 364(6446), eaat8414, 2019 — 매니퓰레이션 논문 서론이 상대해야 하는 분야 수준 진술 (노트 없음, [[04-robotics/index|4 §H]])
- ○ **An overview of dexterous manipulation** — Okamura, Smaby & Cutkosky, ICRA 2000, pp. 255–262 — 구르기·미끄러짐·finger gaiting·재파지의 분류 체계 (노트 없음, [[04-robotics/grasping|15 §8]])

**Force control classics** (힘 제어 고전)

- [x] ◐ [[notes/7-robotics/hogan-impedance|Impedance Control]] — Hogan, ASME JDSMC 107(1), 1985 (3부작)
- ◐ **Variable Impedance Control in End-Effector Space** — Martín-Martín et al., IROS 2019 — 임피던스 파라미터를 RL 행동 공간으로 (노트 없음, [[04-robotics/force-compliance-control|13 §6]]에서 다룸)
- ○ **Learning Variable Impedance Control for Contact Sensitive Tasks** — Bogdanovic, Khadiv & Righetti, RA-L 5(4), 2020 — 같은 질문을 관절 공간에서, 접촉 불확실성 축으로 (노트 없음, [[04-robotics/force-compliance-control|13 §6]])

**Grasping** (파지)

- [x] ◐ [[notes/7-robotics/dex-net-2|Dex-Net 2.0]] — Mahler et al., RSS 2017 — 해석 지표가 라벨 생성기가 되다
- [x] ◐ [[notes/7-robotics/anygrasp|AnyGrasp]] — Fang et al., T-RO 2023 — 조밀·시간적으로 매끄러운 7-DoF 파지

**Tactile & visuotactile** (촉각·시촉각)

- [x] ◐ [[notes/7-robotics/gelsight|GelSight]] — Yuan, Dong & Adelson, Sensors 2017 — 기하를 재고 힘은 추론한다
- [x] ★ [[notes/7-robotics/vision-and-touch|Making Sense of Vision and Touch]] — Lee et al., ICRA 2019 — 자기지도 시촉각 표현
- ◐ **Coding and use of tactile signals from the fingertips** — Johansson & Flanagan, *Nature Reviews Neuroscience* 10, 2009 — SA/FA 수용기 네 종류, 촉각 신호처리가 두 갈래인 이유 (노트 없음, [[04-robotics/tactile-visuotactile|14 §3]])
- ◐ **Sparsh** — Higuera et al., CoRL 2024 — 촉각 백본과 TacBench; DINO·I-JEPA 위에 선다 (노트 없음, [[04-robotics/tactile-visuotactile|14 §4]])
- ○ **PolyTouch** — Zhao et al., ICRA 2025 — 내구성을 실제로 시험한 드문 촉각 논문 (노트 없음, [[04-robotics/tactile-visuotactile|14 §6]])

**Real-world reinforcement learning** (실제 환경 RL)

- [x] ★ [[notes/7-robotics/hil-serl|HIL-SERL]] — Luo, Xu, Wu & Levine, Science Robotics 2025 — 실제 로봇 위에서 1~2.5시간, 사람이 루프 안의 교정 채널

**Teleoperation & demonstration data** (원격조작·시연 데이터)

- [x] ★ [[notes/7-robotics/umi|UMI]] — Chi et al., RSS 2024 — 로봇 없이 야생에서 시연 수집
- [x] ○ [[notes/7-robotics/gello|GELLO]] — Wu et al., IROS 2024 — 기구학이 같은 저가 리더 암
- [x] ◐ [[notes/7-robotics/mobile-aloha|Mobile ALOHA]] — Fu, Zhao & Finn, CoRL 2024 — 전신 원격조작과 co-training

**Study guides** — concept guides rather than papers, so they carry no ★◐○ mark; read them in track order.
**Study guides** (논문이 아닌 개념 가이드 — 읽기 기호 대신 트랙 순서로 읽는다)

- [[04-robotics/modern-robotics/index|Modern Robotics Summary]] — 2–6장·8–13장 챕터 요약 (트랙 2번)
- [[04-robotics/state-estimation-slam|State Estimation, Localization & SLAM]] — Probabilistic Robotics 기반 (3)
- [[04-robotics/geometric-perception-calibration|Geometric Perception & Calibration]] — 카메라 모델·registration·보정 (3.5)
- [[04-robotics/planning-decision-making|Planning & Decision-Making]] — search·sampling·trajectory optimization·TAMP (4)
- [[04-robotics/control-theory-ce397|Control Theory]] — 상태공간·안정성·극점·가제어성/가관측성·극점 배치·PID·관측기 (5)
- [[04-robotics/lqr-lqg|LQR/LQG]] — Underactuated Robotics, Stanford EE363 기반 (6)
- [[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] — MR 12장의 연장 (9)
- [[04-robotics/robot-systems-deployment|Robot Systems, Embodiment & Deployment]] — timing·frames·middleware·failure (10)
- [[04-robotics/hri-safety|Human–Robot Interaction & Safety]] — autonomy levels·human studies·hazard/risk (11)
- [[04-robotics/teleoperation-demonstration|Teleoperation & Demonstration Collection]] — 양방향 제어·지연과 수동성·인터페이스·시연 데이터 품질 (12, 매니퓰레이션 전문화)
- [[04-robotics/force-compliance-control|Force & Compliance Control]] — 임피던스/어드미턴스·하이브리드·작업 공간 제어·접촉 천이 (13, 매니퓰레이션 전문화)
- [[04-robotics/tactile-visuotactile|Tactile & Visuotactile Sensing]] — 센서 계열·미끄러짐·접촉 상태·시촉각 융합 (14, 매니퓰레이션 전문화)
- [[04-robotics/grasping|Grasping]] — 마찰 원뿔·form/force closure·엡실론 지표·학습 파지 (15, 매니퓰레이션 전문화)
- [[04-robotics/navigation-mobile-manipulation|Navigation & Mobile Manipulation]] — 조작 가능한 자세·도달성/능력 지도·base placement·오차 예산 (16, 매니퓰레이션 전문화)
- [[04-robotics/traversability-off-road|Traversability & Off-Road Autonomy]] — 학습된 어포던스로서의 traversability·지도 신호·SubT/RACER (17, 내비게이션)
- [[04-robotics/legged-locomotion|Legged Locomotion]] — privileged teacher-student 증류·정본의 실제 주장·파쿠르 대조 (18, 내비게이션)
- [[04-robotics/semantic-language-navigation|Semantic & Language-Driven Navigation]] — ObjectNav/VLN 정의와 지표·언어로 질의하는 지도·벤치마크의 해체 (19, 내비게이션)
- [[04-robotics/video-action-understanding|Video Representation & Action Understanding]] — 인식/위치추정/예측의 구분·장면 편향·백본 계보 (20, 사람 인지)
- [[04-robotics/human-pose-gaze|Human Pose, Hands & Gaze]] — 표현의 사다리·MPJPE의 물리적 의미·머리 자세를 시선으로 대체하는 문제 (21, 사람 인지)
- [[04-robotics/egocentric-perception|Egocentric & First-Person Perception]] — 1인칭 시점이 관측 가능성을 바꾸는 방식·시선→머리→손→접촉 단서 사슬 (22, 사람 인지)
- [[04-robotics/human-intent-prediction|Human Intent & Trajectory Prediction]] — 의도 대 궤적·가용 지평 Δ*와 필요 선행 시간·보정과 base rate (23, 사람 인지)


## 8. Construction Robotics

Maps: [[05-construction-robotics/lineage|Construction Robotics Lineage]] · [[05-construction-robotics/labs|Labs]]. The 26 entries below were selected in the 2026-07 lab/lineage corpus audit and extended in 2026-08 with the three construction-manipulation papers. **Core** papers changed the technical or system trajectory of construction physical AI; **Supporting** papers represent the key perception, HRC, and workflow connections. Papers from famous labs were still excluded when purely construction-management.

계보와 랩 지도: [[05-construction-robotics/lineage|Construction Robotics Lineage]] · [[05-construction-robotics/labs|Labs]]. 아래 26편은 2026-07 랩·계보 코퍼스 감사에서 선별하고, 2026-08에 건설 매니퓰레이션 3편을 더했다. **Core**는 건설 physical AI의 기술·시스템 흐름을 바꾼 논문, **Supporting**은 핵심 인식·HRC·공정 연결을 대표하는 논문이다. 유명 랩의 논문이라도 순수 건설관리이면 제외했다.

### Field overview

- [x] ◐ [[notes/8-construction/bock-2015|Bock — *The future of construction automation*]] (Automation in Construction, 2015) — STCR에서 통합 자동화까지의 조감
- [x] ◐ [[notes/8-construction/davila-delgado-2019|Davila Delgado et al. — adoption barriers]] (J. Building Engineering, 2019) — 기술 외 도입 조건

### Earthmoving & heavy machines

- [x] ◐ [[notes/8-construction/stentz-excavator|Stentz et al. — autonomous truck loading]] (IROS 1998 / Autonomous Robots 1999) — 30년 중장비 자율화 계보의 출발점
- [x] ★ [[notes/8-construction/heap|HEAP — the autonomous walking excavator]] (Jud et al., Automation in Construction 2021) — 계측·힘 제어 플랫폼
- [x] ◐ [[notes/8-construction/aes|AES — autonomous material loading]] (Zhang et al., Science Robotics 2021) — 24시간/개입의 산업 규모 시스템
- [x] ◐ [[notes/8-construction/egli-rl|Egli et al. — RL for hydraulic excavator arms + soil-adaptive excavation]] (RA-L 2022) — 실기계 토질 적응 RL
- [x] ◐ [[notes/8-construction/wheel-loader-rl|Eriksson et al. — wheel-loader RL]] (ICRA 2024) — 북유럽 실기계 적재 학습
- [x] ○ [[notes/8-construction/exact-2024|ExACT — ACT for an excavator]] (Chen et al., Baidu, ICRA 2024 **Workshop**) — end-to-end 모방학습, 시뮬레이터 검증
- [x] ★ [[notes/8-construction/ext|ExT — excavation pretrain→fine-tune]] (Zhai, Terenzi et al., ETH RSL 2025) — 멀티태스크 physical-AI 신호

### Assembly & fabrication

- [x] ★ [[notes/8-construction/vision-guided-assembly|Feng et al. — vision-guided assembly and as-built scanning]] (Automation in Construction 2015) — 미시간 조작 계보의 앵커
- [x] ★ [[notes/8-construction/apolinarska-timber|Apolinarska et al. — 목재 접합의 힘 유도 삽입]] (Automation in Construction 2021) — 전적으로 시뮬에서 학습해 실기계로 전이
- [x] ◐ [[notes/8-construction/feng-rebar|Feng et al. — 철근 결속 로봇]] (Buildings 2024) — 현장 검증된 드문 사례
- [x] ◐ [[notes/8-construction/kindle-jaibot|Kindle et al. — 드릴링 로봇의 변형·백래시 보상]] (RA-L 2025)
- [x] ★ [[notes/8-construction/dry-stone-wall|Johns et al. — excavation and dry-stone construction]] (Science Robotics 2023) — 인식·계획·중장비 조작의 실규모 폐루프
- [x] ○ [[notes/8-construction/aerial-am-2022|Zhang et al. — aerial additive manufacturing]] (Nature 2022) — 공중 적층 제조
- [x] ◐ [[notes/8-construction/yu-imitation|Yu et al. — cloud-based hierarchical imitation learning]] (JCCE 2024) — 작업자 기술의 시연 학습
- [x] ○ [[notes/8-construction/lundeen-2019|Lundeen et al. — geometrically adaptive robotized construction]] (Automation in Construction 2019) — as-built 변동 적응
- [x] ◐ [[notes/8-construction/liang-lfd|Liang et al. — LfD for quasi-repetitive construction tasks]] (Automation in Construction 2020) — 건설 모방학습의 입구
- [x] ○ [[notes/8-construction/han-welding|Lee & Han — mobile robotic welding with HRI]] (Automation in Construction 2024) — UGV+팔 용접 시스템

### Site perception, HRC & workflow layers

- [ ] ○ [Tang et al. — automatic reconstruction of as-built BIM from laser scans](https://doi.org/10.1016/j.autcon.2010.06.007) (Automation in Construction 2010) — scan-to-BIM 기준 서베이
- [x] ◐ [[notes/8-construction/cho-slam|Kim, Chen & Cho — SLAM-driven robotic site mapping]] (Automation in Construction 2018) — RICAL 자율 스캔 계보의 앵커 (2019 UAV+UGV, 2025 view planning으로 이어짐)
- [x] ◐ [[notes/8-construction/liu-jebelli-bci|Liu & Jebelli — BCI teleoperation → intention-aware planning]] (AutCon 2021 / CACAIE 2024) — 생리 신호를 로봇 루프에 연결한 계보
- [x] ○ [[notes/8-construction/park-nl|Park et al. — natural-language robot instructions]] (Automation in Construction 2024) — 언어 기반 HRC 인터페이스
- [x] ◐ [[notes/8-construction/bim-digital-twin|Wang et al. — BIM-driven closed-loop digital twins]] (Computers in Industry 2024) — 공정 수준 인터페이스
- [x] ◐ [[notes/8-construction/lasota-shah|Lasota & Shah — human-aware motion planning]] (Human Factors 2015 / RA-L 2018) — 건설이 수입하는 제조 HRC 증거
- [x] ○ [[notes/8-construction/liang-hrc-survey|Liang et al. — HRC in construction: classification & trends]] (JCEM 2021) — 스트림 6의 방향 잡는 분류 체계

Concept pages · 개념 페이지: [[05-construction-robotics/earthmoving-heavy-machinery|Earthmoving]] · [[05-construction-robotics/assembly-fabrication|Assembly]] · [[05-construction-robotics/site-perception|Site Perception]] · [[05-construction-robotics/hrc-worker-centered|HRC]] · [[05-construction-robotics/digital-twin-workflows|Digital Twins]] · [[05-construction-robotics/sim-to-real|Sim-to-Real]] · [[05-construction-robotics/industry-deployment|Industry Map]] · [[05-construction-robotics/construction-manipulation|Construction Manipulation]]. 커뮤니티 추적: [ICRA Construction Robotics Workshop](https://construction-robots.github.io/index2024.html).

## 9. Navigation & Locomotion

Notes: [[01-canonical-papers/notes/9-navigation/index|9. Navigation & Locomotion]]. Concept guides: section I of [[04-robotics/index|Robotics & Physical Systems]] — pages 17, 18, 19. These fifteen papers are the navigation pillar of [[07-research-program/index|the research program]]: enough to know what a site robot's base can already do, and where the literature stops.

노트: [[01-canonical-papers/notes/9-navigation/index|9. Navigation & Locomotion]]. 개념 가이드는 [[04-robotics/index|Robotics & Physical Systems]] I절 — 17·18·19번. 아래 15편이 [[07-research-program/index|연구 프로그램]]의 내비게이션 기둥이다: 현장 로봇의 베이스가 이미 무엇을 할 수 있고 문헌이 어디서 멈추는지를 알기에 충분한 만큼.

### Traversability — the learned affordance

- [x] ◐ [[notes/9-navigation/badgr|BADGR]] — Kahn, Abbeel & Levine, RA-L 2021 — 기하가 아니라 주행 사건을 예측한다
- [x] ★ [[notes/9-navigation/wild-visual-navigation|WVN]] — Frey, Mattamala et al., RSS 2023 — 현장에서 5분 만에 학습하는 traversability

### Legged locomotion

- [x] ★ [[notes/9-navigation/lee-quadruped-terrain|Lee et al. — 험지 4족 로코모션]] (Science Robotics 2020) — 특권 정보 teacher–student 증류의 정본
- [x] ◐ [[notes/9-navigation/miki-perceptive-locomotion|Miki et al. — 야생의 지각적 로코모션]] (Science Robotics 2022) — 센서를 *언제* 믿을지 학습한다
- [x] ◐ [[notes/9-navigation/rma|RMA]] — Kumar, Fu, Pathak & Malik, RSS 2021 — 증류 대신 온라인 시스템 식별
- [x] ○ [[notes/9-navigation/anymal-parkour|ANYmal Parkour]] — Hoeller et al., Science Robotics 2024 — 발디딤 계획이 아니라 기술 선택

### Object-goal and language navigation

- [x] ◐ [[notes/9-navigation/semexp|SemExp]] — Chaplot et al., NeurIPS 2020 — 목표 범주에 조건부인 탐색, Habitat 챌린지 우승
- [x] ◐ [[notes/9-navigation/vln-ce|VLN-CE]] — Krantz et al., ECCV 2020 — nav-graph 벤치마크의 세 가정을 해체한다
- [x] ◐ [[notes/9-navigation/vlfm|VLFM]] — Yokoyama et al., ICRA 2024 — 사전학습 VLM이 frontier에 점수를 매긴다 (zero-shot)
- [x] ◐ [[notes/9-navigation/navid|NaVid]] — Zhang et al., RSS 2024 — 지도·오도메트리·깊이 없이 비디오 VLM만으로
- [x] ○ [[notes/9-navigation/uni-navid|Uni-NaVid]] — Zhang et al., RSS 2025 — 네 내비게이션 과제를 한 VLA로

### Language-queryable maps

- [x] ◐ [[notes/9-navigation/conceptgraphs|ConceptGraphs]] — Gu, Kuwajerwala et al., ICRA 2024 — 점별 특징장이 아니라 물체 그래프
- [x] ○ [[notes/9-navigation/clio|Clio]] — Maggio et al., RA-L 2024 — 입도는 물체의 성질이 아니라 과제의 성질이다

### Navigation foundation models, and the reality check

- [x] ◐ [[notes/9-navigation/vint-nomad|ViNT / NoMaD]] — Shah et al., CoRL 2023 · Sridhar et al., ICRA 2024 — 신체 교차 사전학습과 목표 가리기
- [x] ★ [[notes/9-navigation/gervet-real-world-objectnav|Gervet et al. — 실제 환경의 물체 내비게이션]] (Science Robotics 2023) — end-to-end가 시뮬 77%에서 현실 23%로 무너진다

**Study guides** — the concept pages these papers depend on · 이 논문들이 딛고 선 개념 페이지

- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]]
- [[04-robotics/legged-locomotion|18. Legged Locomotion]]
- [[04-robotics/semantic-language-navigation|19. Semantic & Language-Driven Navigation]]
- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — 조작과 만나는 지점
