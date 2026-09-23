---
title: 2. Physical AI Ecosystem
tags: [reference]
study-depth: Literacy
depth-goal: "Use the map to locate a method historically and explain how neighboring research streams connect."
mastery-when: "Raise the specific downstream method pages—not the whole map—to Working or Mastery."
last_verified: 2026-09-22
---

## English

Papers tell you the *ideas*; this page tracks the *players and platforms* — who builds
what, and which hardware the papers actually run on. For exhaustive
frontier tracking see [sudoremove](https://sudoremove.com/) (Korean physical-AI knowledge hub).

> [!warning] Rosters go stale · 명단은 낡는다
> Companies, products and "who runs what" change faster than anything else in this wiki, and
> nothing on this page is load-bearing for a claim. The tables were last reviewed on
> **2026-09-09**, and the NVIDIA, AMI Labs and World Labs rows with the NVIDIA stack on
> **2026-09-22**; treat every row as a pointer to check, not as a current fact. Where a row
> matters to an argument, cite the paper note it links to rather than this page.
> 회사·제품·"누가 무엇을 돌리는가"는 이 위키에서 가장 빨리 바뀌고, 이 페이지의 어떤 항목도
> 주장의 근거가 되지 않는다. 표는 **2026-09-09**에 마지막으로 훑었고, NVIDIA·AMI Labs·World Labs 행과 NVIDIA 스택은 **2026-09-22**에 확인했다. 각 줄을 현재 사실이 아니라
> 확인할 포인터로 다뤄라. 어떤 줄이 논증에 걸린다면 이 페이지가 아니라 그 줄이 가리키는 논문
> 노트를 인용하라.

### Key players

| Player | What they do | In this wiki |
|---|---|---|
| Google DeepMind | RT series, Genie, ALOHA lineage research | [[01-canonical-papers/notes/4-vla/rt-2\|RT-2]], [[01-canonical-papers/notes/5-world-models/genie\|Genie]] |
| Physical Intelligence | robot foundation models (π series) | [[01-canonical-papers/notes/4-vla/pi0\|π0]] |
| NVIDIA | GR00T humanoid models, Cosmos world models, Isaac Sim and Isaac Lab — every layer, laid out in the next section | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| Meta AI (FAIR) | JEPA line, open vision backbones (DINOv2) | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| AMI Labs (Paris) | Yann LeCun's company, launched March 2026 to build JEPA-based world models for robotics and industry — the *planner* row of [[03-deep-learning/world-models/index\|5. World Models §6]] | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| World Labs | Fei-Fei Li's company: generated 3D worlds (Marble), real-time rendering (RTFM), an omni model (Atlas), and the renderer–simulator–planner taxonomy | [[01-canonical-papers/notes/5-world-models/world-labs\|World Labs]] |
| Tesla / Figure / 1X / Agility | humanoid hardware + in-house VLA stacks | context for humanoid papers |
| Unitree | affordable humanoids/quadrupeds — academia's default hardware | — |
| Hugging Face | LeRobot: open-source robot learning framework | practical entry point |
| Stanford / Berkeley / CMU labs | ALOHA, Octo, OpenVLA | [[01-canonical-papers/notes/4-vla/act\|ACT]], [[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/openvla\|OpenVLA]] |
| Columbia / Toyota Research Institute / MIT | Diffusion Policy — diffusion as the action head | [[01-canonical-papers/notes/4-vla/diffusion-policy\|Diffusion Policy]] |

### The NVIDIA stack, layer by layer

NVIDIA is the one player that sells every layer a robot-learning project touches, from the chip on the robot to the model that drives it, and papers increasingly cite several layers at once. Read the stack from the bottom. Each row says what a researcher actually uses and where this wiki treats it; the versions were checked on 2026-09-22 and will move.

| layer | the pieces | what a robot researcher uses it for | in this wiki |
|---|---|---|---|
| compute on the robot | **Jetson Thor**: a Blackwell GPU rated at $2{,}070$ FP4 TFLOPS (sparse), $128$ GB of memory, $40$–$130$ W, aimed at humanoids | running a VLA such as GR00T on board rather than over a network | [[04-robotics/robot-systems-deployment\|10. Robot Systems]] for the latency budget |
| scene description | **OpenUSD** scenes in **Omniverse** | one scene file shared by the simulator, the renderer and the tools | — |
| simulation | **Isaac Sim** (the simulator: PhysX physics, RTX-rendered sensors); **Isaac Lab** (the robot-learning framework on top, successor of Isaac Gym and Orbit; 3.0 in early access since 2026-09-16); **Newton** (an open GPU physics engine begun with Google DeepMind and Disney Research, MuJoCo-Warp as its main solver) | reinforcement learning at thousands of parallel environments, and simulated evaluation | [[06-research-practice/simulators-benchmarks-datasets\|Simulators, Benchmarks & Datasets §2]], with its license and version traps |
| data generation | **Isaac Lab Mimic** (about ten teleoperated demonstrations, cut into subtasks and re-posed around the objects, become about a thousand); **GR00T-Dreams** (DreamGen: a video world model fine-tuned on the robot makes new videos, and pseudo-actions are recovered from them); **Cosmos-Transfer** (turns simulator renderings into realistic video) | more demonstrations than a team can teleoperate | [[04-robotics/teleoperation-demonstration\|12. Teleoperation]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| world models | **Cosmos-Predict** (video world models, 2.5 at 2B and 14B); **Cosmos-Reason** (a vision–language model for physical reasoning) | synthetic video, policy evaluation, reasoning about a physical scene | [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]], [[03-deep-learning/world-models/index\|5. World Models §6]] |
| robot foundation model | **GR00T N1 → N1.5 → N1.6 → N1.7** (3B; Cosmos-Reason2-2B inside; relative end-effector actions shared with human video; open weights) | a pretrained policy to post-train on your own robot | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[03-deep-learning/vla/index\|4. VLA §7]] |
| deployment | **Isaac ROS** (GPU-accelerated ROS 2 packages: NITROS transport, visual SLAM, nvblox mapping, FoundationPose, cuMotion); **cuRobo** (GPU motion generation, $50$ ms on average and $60$ times faster than prior trajectory optimization in its paper) | real-time perception and motion planning on the robot | [[04-robotics/ros2/index\|25. ROS 2]], [[04-robotics/planning-decision-making\|4. Planning]] |

**How the layers are meant to chain.** Teleoperate a few demonstrations → multiply them in Isaac Lab with Mimic, or dream new ones with a Cosmos model → make simulated ones look real with Cosmos-Transfer → post-train GR00T → run it on Jetson Thor → bring the failures back as new demonstrations. Each arrow is a claim to check in a paper, not a guarantee: the multiplication step's own documentation reports about half of generated attempts succeeding on a cube-stacking task, and a policy trained on generated data still has to be tested on the real robot.

**What to keep separate when reading.** Open weights are not open data: GR00T's code is Apache 2.0 while its weights carry the NVIDIA Open Model License, and Isaac Sim's own license points to separately licensed components. And the stack's physics is its weakest layer for contact-rich work — Isaac Sim cannot report contact forces on deformables, and neither a Cosmos video nor a generated scene carries force — which is why the manipulation track keeps measuring force on the real machine.

### Standard hardware in papers

- **Arms**: Franka Panda (research default), WidowX (low-cost eval), UR series (industrial)
- **Bimanual**: ALOHA / ALOHA 2 / Mobile ALOHA — the data-collection workhorse
- **Humanoids**: Unitree G1/H1, Fourier GR-1, Tesla Optimus, Figure, 1X NEO
- **Quadrupeds**: Unitree Go/B series, ANYmal, Boston Dynamics Spot
- **Construction-relevant**: excavator retrofits, Spot on sites, Built Robotics — see [[05-construction-robotics/index|construction robotics]]

## 한국어

논문은 *아이디어*를 알려주고, 이 페이지는 *플레이어와 플랫폼*을 추적한다 — 누가 무엇을
만들고, 논문들이 실제로 어떤 하드웨어 위에서 도는지. 가끔씩 갱신하며, 최전선의 전수
추적은 [sudoremove](https://sudoremove.com/)(한국어 physical AI 지식 허브)를 참고.

### 주요 플레이어

| 플레이어 | 하는 일 | 이 위키에서 |
|---|---|---|
| Google DeepMind | RT 시리즈, Genie, ALOHA 계열 연구 | [[01-canonical-papers/notes/4-vla/rt-2\|RT-2]], [[01-canonical-papers/notes/5-world-models/genie\|Genie]] |
| Physical Intelligence | 로봇 파운데이션 모델 (π 시리즈) | [[01-canonical-papers/notes/4-vla/pi0\|π0]] |
| NVIDIA | GR00T 휴머노이드 모델, Cosmos 월드모델, Isaac Sim과 Isaac Lab — 모든 층을 다음 절에 펼쳤다 | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| Meta AI (FAIR) | JEPA 계열, 오픈 비전 백본 (DINOv2) | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| AMI Labs (파리) | Yann LeCun이 2026년 3월 출범시킨 회사로, 로봇과 산업을 위한 JEPA 기반 월드모델을 만든다 — [[03-deep-learning/world-models/index\|5. 월드모델 §6]]의 *플래너* 행 | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| World Labs | 페이페이 리의 회사: 생성된 3D 세계(Marble), 실시간 렌더링(RTFM), 옴니 모델(Atlas), 그리고 렌더러–시뮬레이터–플래너 분류 | [[01-canonical-papers/notes/5-world-models/world-labs\|World Labs]] |
| Tesla / Figure / 1X / Agility | 휴머노이드 하드웨어 + 자체 VLA 스택 | 휴머노이드 논문의 맥락 |
| Unitree | 저가 휴머노이드/사족보행 — 학계의 기본 하드웨어 | — |
| Hugging Face | LeRobot: 오픈소스 로봇 학습 프레임워크 | 실습 진입점 |
| Stanford/Berkeley/CMU 랩들 | ALOHA, Octo, OpenVLA | [[01-canonical-papers/notes/4-vla/act\|ACT]], [[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/openvla\|OpenVLA]] |
| Columbia / Toyota Research Institute / MIT | Diffusion Policy — 확산 모델을 행동 헤드로 | [[01-canonical-papers/notes/4-vla/diffusion-policy\|Diffusion Policy]] |

### NVIDIA 스택, 층별로

NVIDIA는 로봇 학습 프로젝트가 닿는 모든 층 — 로봇에 실리는 칩부터 그것을 모는 모델까지 — 을 파는 유일한 플레이어이고, 논문들은 점점 여러 층을 한꺼번에 인용한다. 스택은 아래에서부터 읽는다. 각 행은 연구자가 실제로 무엇에 쓰는지와 이 위키가 어디서 다루는지를 적는다. 버전은 2026-09-22에 확인했고 계속 바뀐다.

| 층 | 구성 | 로봇 연구자가 쓰는 곳 | 이 위키에서 |
|---|---|---|---|
| 로봇 위 연산 | **Jetson Thor**: FP4 기준 $2{,}070$ TFLOPS(희소)의 Blackwell GPU, 메모리 $128$ GB, $40$–$130$ W, 휴머노이드를 겨냥 | GR00T 같은 VLA를 네트워크 너머가 아니라 로봇 위에서 돌리기 | 지연 예산은 [[04-robotics/robot-systems-deployment\|10. 로봇 시스템]] |
| 장면 기술 | **Omniverse**의 **OpenUSD** 장면 | 시뮬레이터·렌더러·도구가 함께 쓰는 장면 파일 하나 | — |
| 시뮬레이션 | **Isaac Sim**(시뮬레이터: PhysX 물리, RTX로 렌더링한 센서); **Isaac Lab**(그 위의 로봇 학습 프레임워크, Isaac Gym과 Orbit의 후속, 3.0은 2026-09-16부터 얼리 액세스); **Newton**(Google DeepMind·Disney Research와 시작한 오픈 GPU 물리 엔진, 주 솔버는 MuJoCo-Warp) | 병렬 환경 수천 개의 강화학습, 시뮬레이션 평가 | 라이선스와 버전 함정까지 [[06-research-practice/simulators-benchmarks-datasets\|시뮬레이터·벤치마크·데이터셋 §2]] |
| 데이터 생성 | **Isaac Lab Mimic**(원격조작 시연 약 열 개를 하위 과제로 자르고 물체 기준으로 다시 놓아 약 천 개로 늘린다); **GR00T-Dreams**(DreamGen: 로봇에 맞춰 미세조정한 비디오 월드모델이 새 영상을 만들고, 거기서 의사 행동을 복원한다); **Cosmos-Transfer**(시뮬레이터 렌더링을 실제 같은 영상으로 바꾼다) | 팀이 원격조작할 수 있는 것보다 많은 시연 | [[04-robotics/teleoperation-demonstration\|12. 원격조작]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| 월드모델 | **Cosmos-Predict**(비디오 월드모델, 2.5는 2B와 14B); **Cosmos-Reason**(물리 추론을 위한 시각–언어 모델) | 합성 비디오, 정책 평가, 물리 장면에 대한 추론 | [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]], [[03-deep-learning/world-models/index\|5. 월드모델 §6]] |
| 로봇 파운데이션 모델 | **GR00T N1 → N1.5 → N1.6 → N1.7**(3B, 안에 Cosmos-Reason2-2B, 사람 비디오와 함께 쓰는 상대 end-effector 행동, 공개 가중치) | 자기 로봇에 사후학습할 사전학습 정책 | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[03-deep-learning/vla/index\|4. VLA §7]] |
| 배치 | **Isaac ROS**(GPU 가속 ROS 2 패키지: NITROS 전송, 시각 SLAM, nvblox 지도, FoundationPose, cuMotion); **cuRobo**(GPU 동작 생성, 논문에서 평균 $50$ ms, 기존 궤적 최적화보다 $60$배 빠름) | 로봇 위의 실시간 인식과 동작 계획 | [[04-robotics/ros2/index\|25. ROS 2]], [[04-robotics/planning-decision-making\|4. 계획]] |

**층들이 이어지도록 설계된 방식.** 시연 몇 개를 원격조작한다 → Isaac Lab의 Mimic으로 불리거나 Cosmos 모델로 새것을 꿈꾼다 → 시뮬레이션 시연을 Cosmos-Transfer로 실제처럼 보이게 한다 → GR00T를 사후학습한다 → Jetson Thor에서 돌린다 → 실패를 새 시연으로 되가져온다. 화살표 하나하나가 논문에서 확인할 주장이지 보장이 아니다. 불리는 단계의 문서 스스로 큐브 쌓기 과제에서 생성 시도의 약 절반만 성공한다고 보고하고, 생성된 데이터로 학습한 정책도 실제 로봇에서 시험해야 한다.

**읽을 때 따로 둘 것.** 공개 가중치는 공개 데이터가 아니다. GR00T의 코드는 Apache 2.0이지만 가중치는 NVIDIA Open Model License이고, Isaac Sim의 라이선스 스스로 별도 라이선스의 구성 요소를 가리킨다. 그리고 접촉이 많은 작업에서 스택의 가장 약한 층은 물리다. Isaac Sim은 변형체의 접촉력을 보고하지 못하고, Cosmos 비디오도 생성된 장면도 힘을 싣지 않는다. 매니퓰레이션 트랙이 실제 기계에서 힘을 계속 재는 이유다.

### 논문에 등장하는 표준 하드웨어

- **팔**: Franka Panda(연구 기본값), WidowX(저가 평가용), UR 시리즈(산업용)
- **양팔**: ALOHA / ALOHA 2 / Mobile ALOHA — 데이터 수집의 주력 장비
- **휴머노이드**: Unitree G1/H1, Fourier GR-1, Tesla Optimus, Figure, 1X NEO
- **사족보행**: Unitree Go/B 시리즈, ANYmal, Boston Dynamics Spot
- **건설 관련**: 굴착기 개조, 현장의 Spot, Built Robotics — [[05-construction-robotics/index|건설로봇]] 참고
