---
title: 2. Physical AI Ecosystem
tags: [reference]
---

## English

Papers tell you the *ideas*; this page tracks the *players and platforms* — who builds
what, and which hardware the papers actually run on. Updated occasionally; for exhaustive
frontier tracking see [sudoremove](https://sudoremove.com/) (Korean physical-AI knowledge hub).

### Key players

| Player | What they do | In this wiki |
|---|---|---|
| Google DeepMind | RT series, Genie, ALOHA lineage research | [[01-canonical-papers/notes/4-vla/rt-2\|RT-2]], [[01-canonical-papers/notes/5-world-models/genie\|Genie]] |
| Physical Intelligence | robot foundation models (π series) | [[01-canonical-papers/notes/4-vla/pi0\|π0]] |
| NVIDIA | GR00T humanoid models, Cosmos world models, Isaac sim | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| Meta AI (FAIR) | JEPA line, open VLM components (DINOv2, SigLIP usage) | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| Tesla / Figure / 1X / Agility | humanoid hardware + in-house VLA stacks | context for humanoid papers |
| Unitree | affordable humanoids/quadrupeds — academia's default hardware | — |
| Hugging Face | LeRobot: open-source robot learning framework | practical entry point |
| Stanford/Berkeley/CMU labs | ALOHA, Octo, OpenVLA, Diffusion Policy | [[01-canonical-papers/notes/4-vla/act\|ACT]], [[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/openvla\|OpenVLA]], [[01-canonical-papers/notes/4-vla/diffusion-policy\|Diffusion Policy]] |

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
| NVIDIA | GR00T 휴머노이드 모델, Cosmos 월드모델, Isaac 시뮬레이션 | [[01-canonical-papers/notes/4-vla/gr00t-n1\|GR00T N1]], [[01-canonical-papers/notes/5-world-models/cosmos\|Cosmos]] |
| Meta AI (FAIR) | JEPA 계열, 오픈 VLM 구성 요소 (DINOv2 등) | [[01-canonical-papers/notes/5-world-models/jepa\|JEPA]] |
| Tesla / Figure / 1X / Agility | 휴머노이드 하드웨어 + 자체 VLA 스택 | 휴머노이드 논문의 맥락 |
| Unitree | 저가 휴머노이드/사족보행 — 학계의 기본 하드웨어 | — |
| Hugging Face | LeRobot: 오픈소스 로봇 학습 프레임워크 | 실습 진입점 |
| Stanford/Berkeley/CMU 랩들 | ALOHA, Octo, OpenVLA, Diffusion Policy | [[01-canonical-papers/notes/4-vla/act\|ACT]], [[01-canonical-papers/notes/4-vla/octo\|Octo]], [[01-canonical-papers/notes/4-vla/openvla\|OpenVLA]], [[01-canonical-papers/notes/4-vla/diffusion-policy\|Diffusion Policy]] |

### 논문에 등장하는 표준 하드웨어

- **팔**: Franka Panda(연구 기본값), WidowX(저가 평가용), UR 시리즈(산업용)
- **양팔**: ALOHA / ALOHA 2 / Mobile ALOHA — 데이터 수집의 주력 장비
- **휴머노이드**: Unitree G1/H1, Fourier GR-1, Tesla Optimus, Figure, 1X NEO
- **사족보행**: Unitree Go/B 시리즈, ANYmal, Boston Dynamics Spot
- **건설 관련**: 굴착기 개조, 현장의 Spot, Built Robotics — [[05-construction-robotics/index|건설로봇]] 참고
