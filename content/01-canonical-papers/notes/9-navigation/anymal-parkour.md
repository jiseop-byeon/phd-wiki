---
title: "ANYmal Parkour — Learning Agile Navigation for Quadrupedal Robots"
authors: David Hoeller, Nikita Rudin, Dhionis Sako, Marco Hutter
affiliation: ETH Zürich, NVIDIA
venue: Science Robotics
year: 2024
journal-ref: "Science Robotics 9(88), eadi7566"
arxiv: https://arxiv.org/abs/2306.14874
tags: [paper, locomotion, legged, navigation, hierarchical]
status: note-complete
last_verified: 2026-08-22
study-depth: Literacy
wiki-support: Working
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if skill selection over a library of learned behaviours becomes part of the architecture."
---

**Hoeller, Rudin, Sako & Hutter, *Science Robotics* 9(88), eadi7566, 2024** — [arXiv:2306.14874](https://arxiv.org/abs/2306.14874)

> [!note] Math on-ramp · 수학 준비물
> Hierarchical policies: low-level skills plus a high-level selector, and what it means for the selector to be *aware of each skill's capability* ([[04-robotics/legged-locomotion|18. §5]], [[04-robotics/planning-decision-making|4. §5]]).
> 계층적 정책: 저수준 기술들과 고수준 선택기, 그리고 선택기가 *각 기술의 능력을 안다*는 것이 무슨 뜻인지([[04-robotics/legged-locomotion|18. §5]], [[04-robotics/planning-decision-making|4. §5]]).

## English

**One-line summary**: Train separate skills — walking, jumping, climbing, crouching — then train a high-level policy that knows what each skill can do and picks among them across the terrain, with a perception module that reconstructs obstacles from occluded and noisy sensing.

### Context

Locomotion papers keep the body upright; navigation papers pick a route. Agile obstacle crossing sits between them and had been handled with expert demonstrations, offline computation, prior maps, or explicit contact planning. The paper's stated contribution is doing it **without any of those four**.

### Method

Two layers plus a perception module.

- **Skills.** Advanced locomotion behaviours are trained for several obstacle types: walking, jumping, climbing, crouching.
- **A high-level policy** selects and controls those skills across the terrain. Because of the hierarchical formulation, the navigation policy is **aware of the capabilities of each skill** and adapts its behaviour to the scenario — this is the actual claim, and it is stronger than "a selector on top of skills".
- **A perception module** is trained to reconstruct obstacles from **highly occluded and noisy sensory data**, which is what gives the pipeline scene understanding when the robot's field of view is blocked by its own body mid-manoeuvre.

### Results

Trained on **simulated data only**, transferring to hardware, where the robot navigates and crosses **consecutive** challenging obstacles at speeds of **up to two metres per second**.

> [!warning] Reading the claims · 주장 읽는 법
> The one number is **2 m/s**, and it is a maximum, not an average. "Consecutive obstacles" is the load-bearing word in the results sentence — crossing obstacles one at a time from a reset is a much easier problem than chaining them, and the chaining is where a skill-selection architecture earns its keep. There is no success rate in the abstract.
> 유일한 숫자는 **2 m/s**이고, 평균이 아니라 최대다. 결과 문장에서 무게를 지는 단어는 "연속된 장애물"이다 — 초기화 후 장애물을 하나씩 넘는 것은 그것들을 이어 붙이는 것보다 훨씬 쉬운 문제이고, 기술 선택 구조가 값을 하는 곳이 바로 이어 붙이기다. 초록에 성공률은 없다.

### Limitations & critique

- **The skill library is the vocabulary.** The robot can only compose what was trained. A new obstacle class needs a new skill, not more data.
- **Simulation only, for training.** Everything the perception module learned to reconstruct is an obstacle a simulator rendered. Real occlusion statistics — dust, wet surfaces, mesh fencing — are outside that.
- **Agility is not the site bottleneck.** For construction the interesting quadruped result is robustness under load and around people, not speed over obstacles.

### Impact & follow-ups

The paper is the clearest existing demonstration that **navigation over rough terrain can be a skill-selection problem** rather than a footstep-planning problem, and the capability-aware selector is the idea most likely to transfer — it is the same structure a mobile manipulator needs when choosing between driving closer, re-grasping, and repositioning the base ([[04-robotics/navigation-mobile-manipulation|16. §4]]).

### Connections

- [[04-robotics/legged-locomotion|18. Legged Locomotion §5]] — the concept page's treatment of skill hierarchies
- [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki et al. 2022]] — the perception-robustness lineage this builds on
- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — the same selection problem with manipulation skills

### After reading

- [ ] Name the four things the paper claims to do without.
- [ ] Explain what "capability-aware" adds over a plain high-level selector.
- [ ] Say why the perception module has to handle occlusion specifically.
- [ ] State what the 2 m/s figure is, and what it is not.

## 한국어

**한 줄 요약**: 걷기·뛰기·오르기·웅크리기 같은 기술을 따로 학습한 뒤, 각 기술이 무엇을 할 수 있는지 아는 고수준 정책이 지형을 가로지르며 그중에서 고른다. 가려지고 잡음 많은 감지에서 장애물을 복원하는 인지 모듈이 붙는다.

### 배경

로코모션 논문은 몸을 세우고, 내비게이션 논문은 경로를 고른다. 민첩한 장애물 통과는 그 사이에 있고, 그동안 전문가 시연·오프라인 계산·사전 지도·명시적 접촉 계획으로 다뤄져 왔다. 이 논문이 내세우는 기여는 **그 넷 없이** 해낸다는 것이다.

### 방법

두 계층에 인지 모듈 하나.

- **기술.** 여러 장애물 유형에 대해 고급 로코모션 행동을 학습한다: 걷기, 뛰기, 오르기, 웅크리기.
- **고수준 정책**이 지형을 가로지르며 그 기술들을 고르고 제어한다. 계층적 정식화 덕분에 내비게이션 정책이 **각 기술의 능력을 인지**하고 상황에 따라 행동을 바꾼다 — 이것이 실제 주장이고, "기술 위에 얹은 선택기"보다 강한 말이다.
- **인지 모듈**이 **심하게 가려지고 잡음 많은 센서 데이터**에서 장애물을 복원하도록 학습된다. 동작 중 로봇 자신의 몸이 시야를 막을 때 파이프라인에 장면 이해를 주는 것이 이 부분이다.

### 결과

**시뮬레이션 데이터만으로** 학습해 하드웨어로 전이했고, 로봇이 **연속된** 험한 장애물을 **최대 초속 2미터**로 주행·통과한다.

> [!warning] 주장 읽는 법 · Reading the claim
> 유일한 숫자는 **2 m/s**이고, 평균이 아니라 최대다. 결과 문장에서 무게를 지는 단어는 "연속된 장애물"이다 — 초기화 후 장애물을 하나씩 넘는 것은 이어 붙이는 것보다 훨씬 쉬운 문제이고, 기술 선택 구조가 값을 하는 곳이 이어 붙이기다. 초록에 성공률은 없다.
> The single number is a maximum speed, and "consecutive" is the load-bearing word in the results sentence.

### 한계와 비판

- **기술 라이브러리가 곧 어휘다.** 로봇은 학습된 것만 조합할 수 있다. 새로운 장애물 종류에는 더 많은 데이터가 아니라 새 기술이 필요하다.
- **학습은 시뮬레이션뿐이다.** 인지 모듈이 복원하는 법을 배운 모든 것은 시뮬레이터가 렌더링한 장애물이다. 실제 가림의 통계 — 먼지, 젖은 표면, 그물 펜스 — 는 그 밖이다.
- **민첩성이 현장의 병목은 아니다.** 건설에서 흥미로운 4족 결과는 장애물 위 속도가 아니라 하중을 지고 사람 곁에서 유지되는 강건함이다.

### 영향과 후속 연구

이 논문은 **험지 주행이 발디딤 계획 문제가 아니라 기술 선택 문제일 수 있다**는 것을 가장 분명히 보인 사례이고, 능력을 인지하는 선택기가 가장 옮겨갈 만한 발상이다 — 모바일 매니퓰레이터가 더 다가갈지, 다시 잡을지, 베이스를 옮길지 고를 때 필요한 구조가 바로 같은 구조다([[04-robotics/navigation-mobile-manipulation|16. §4]]).

### 연결

- [[04-robotics/legged-locomotion|18. 레그드 로코모션 §5]] — 개념 페이지의 기술 계층 부분
- [[01-canonical-papers/notes/9-navigation/miki-perceptive-locomotion|Miki 등 2022]] — 이것이 딛고 선 인지 강건성 계보
- [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 매니퓰레이션]] — 조작 기술로 하는 같은 선택 문제

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 논문이 "없이" 해냈다고 주장하는 네 가지를 댄다.
- [ ] "능력 인지"가 평범한 고수준 선택기에 무엇을 더하는지 설명한다.
- [ ] 인지 모듈이 왜 하필 가림을 다뤄야 하는지 말한다.
- [ ] 2 m/s가 무엇이고 무엇이 아닌지 말한다.
