---
title: "Gemini Robotics — 1.0, 1.5 and 2: A VLA and an Embodied Reasoner on Gemini"
authors: Gemini Robotics Team (Google DeepMind)
affiliation: Google DeepMind
venue: Technical reports (2025) · announcement and model card (2026)
year: 2025
arxiv: https://arxiv.org/abs/2503.20020
project: https://arxiv.org/abs/2510.03342
tags: [paper, vla, robot-foundation-model]
status: note-complete
last_verified: 2026-09-22
study-depth: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working when the paper becomes a baseline, dependency, or implementation choice."
---

**Gemini Robotics Team, 2025–2026** — [Gemini Robotics arXiv](https://arxiv.org/abs/2503.20020) · [Gemini Robotics 1.5 arXiv](https://arxiv.org/abs/2510.03342) · [Gemini Robotics 2 announcement](https://deepmind.google/blog/gemini-robotics-2-brings-whole-body-intelligence-to-robots/)

> [!note] Math on-ramp · 수학 준비물
> [[pi0|π0]] and [[rt-2|RT-2]] first — a VLA built on a large vision–language model — and [[03-deep-learning/vla/index|4. VLA §6–§7]] for what "thinking before acting" costs and what "motion transfer" has to overcome. The reports disclose little architecture, so the reading is about claims and evaluation, not equations.
> [[pi0|π0]]와 [[rt-2|RT-2]]가 먼저다 — 큰 시각–언어 모델 위에 지은 VLA — 그리고 "행동 전에 생각하기"가 무엇을 치르는지, "모션 전이"가 무엇을 넘어야 하는지는 [[03-deep-learning/vla/index|4. VLA §6–§7]]. 보고서들이 구조를 거의 밝히지 않으므로, 읽을 것은 수식이 아니라 주장과 평가다.

## English

**One-line summary**: Google DeepMind's robot line built on Gemini — a vision–language–action model paired with an embodied-reasoning model — that added thinking and cross-robot motion transfer in 1.5 and whole-body humanoid control in 2.

### Context

[[rt-2|RT-2]] showed that a web-pretrained vision–language model can emit robot actions. Gemini Robotics asks the same of a frontier multimodal model, Gemini 2.0, and splits the work in two: an **embodied-reasoning (ER)** model that understands space, plans and tracks progress, and a **VLA** that turns vision and language into motor commands.

### Method (as disclosed)

> [!tip] Key intuition
> Keep the high-level brain and the motor policy as separate models that talk in language. The ER model decides what should happen next and whether it happened; the VLA decides how the body moves.

- **Gemini Robotics (March 2025)**: a VLA built on Gemini 2.0 that controls robots directly, with Gemini Robotics-ER for embodied reasoning. With further fine-tuning it learned long-horizon dexterous tasks, new short-horizon tasks from as few as $100$ demonstrations, and completely new embodiments.
- **Gemini Robotics 1.5 (October 2025)**: a multi-embodiment VLA with a *Motion Transfer* mechanism that lets it learn from heterogeneous data across robots; it interleaves its actions with multi-level reasoning in natural language — it reasons before acting — which the report says improves decomposition of multi-step tasks and makes behaviour easier to read. Gemini Robotics-ER 1.5 reports state-of-the-art embodied reasoning: visual and spatial understanding, task planning and progress estimation.
- **Gemini Robotics 2 (July 2026)**: whole-body control of humanoids, from the feet to the fingertips, and dexterity across end effectors including a 22-degree-of-freedom hand; **ER 2** as the high-level brain for multi-step planning, talking with people and coordinating several robots; and **On-Device 2**, a lighter VLA that adapts to a new body with a few hours of data. Tested on the Apptronik Apollo 2 humanoid, Franka, Dexmate, SO101 and Trossen platforms.

### Results (as reported)

- Gemini Robotics 2's announcement gives ranges, not a single number: $45.7$–$76.3\%$ success on general manipulation, $74.2$–$89.6\%$ on gripper dexterity, and $32$–$92\%$ on multi-finger tasks, the category it names as still hard.
- 1.5's gains are reported on the company's own task suites; the report is the place to read the definitions of success and the trial counts.

### Limitations & critique

- **Closed.** No weights; ER 2 is public through Google AI Studio, while the VLA and On-Device 2 went to early-access partners only. Every number is the company's evaluation on its own suites, so it cannot be reproduced — the same standing as [[pi0|π0]]'s first-party results.
- **Mechanisms described, not specified.** Motion Transfer is named and motivated but not given in enough detail to re-implement, so its contribution cannot be separated from data scale.
- **Reasoning is paid in rate.** Thinking before acting spends sequential decodes, the cost counted in [[03-deep-learning/vla/index|4. VLA §6]]; the reports do not make control frequency the headline.

### Impact & follow-ups

The clearest statement of the two-model pattern — an embodied reasoner above a motor VLA — that [[gr00t-n1|GR00T]]'s System 2 / System 1 split also follows, and of cross-embodiment as a learned mechanism rather than a data convention ([[03-deep-learning/vla/index|4. VLA §7]]). It also ships safety work beside the models: an agentic safety benchmark, ASIMOV-Agentic, and a separate safety report.

> [!question] Reading the claim · 핵심 주장 읽는 법
> "Whole-body intelligence" is a claim about a demonstrated range of tasks on specific humanoids, not about general competence. Read the ranges, not the best number; ask which platform each range comes from; and treat "adapts in a few hours" as a data budget to compare against a specialist trained on the same hours.

### Connections

- Previous: [[rt-2|RT-2]] (web VLM → actions), [[pi0|π0]] (VLM + action expert)
- Parallel: [[gr00t-n1|GR00T N1]] (System 2 / System 1), [[03-deep-learning/vla/index|4. VLA §6–§8]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: Gemini 위에 지은 Google DeepMind의 로봇 계열 — 체화 추론 모델과 짝을 이룬 시각–언어–행동 모델 — 로, 1.5에서 생각과 로봇 사이 모션 전이를, 2에서 휴머노이드 전신 제어를 더했다.

### 배경

[[rt-2|RT-2]]는 웹으로 사전학습한 시각–언어 모델이 로봇 행동을 낼 수 있음을 보였다. Gemini Robotics는 같은 것을 최전선 멀티모달 모델인 Gemini 2.0에 묻고, 일을 둘로 나눈다. 공간을 이해하고 계획하고 진행을 추적하는 **체화 추론**(embodied reasoning, ER) 모델, 그리고 시각과 언어를 운동 명령으로 바꾸는 **VLA**다.

### 방법 (공개된 만큼)

> [!tip] 핵심 직관
> 상위 두뇌와 운동 정책을 언어로 대화하는 따로 된 모델로 둔다. ER 모델은 다음에 무엇이 일어나야 하는지, 그리고 그것이 일어났는지를 정하고, VLA는 몸이 어떻게 움직일지를 정한다.

- **Gemini Robotics (2025년 3월)**: Gemini 2.0 위에 지은, 로봇을 직접 제어하는 VLA와 체화 추론을 맡는 Gemini Robotics-ER. 추가 미세조정으로 긴 지평의 손재주 과제, 시연 $100$개만으로 새 짧은 과제, 완전히 새로운 몸을 익혔다.
- **Gemini Robotics 1.5 (2025년 10월)**: 로봇들 사이의 이질적인 데이터로 배우게 하는 *Motion Transfer* 메커니즘을 둔 다중 몸 VLA. 행동 사이사이에 자연어로 된 여러 층의 추론을 끼워 — 행동 전에 생각한다 — 보고서는 이것이 여러 단계 과제의 분해를 낫게 하고 행동을 읽기 쉽게 만든다고 한다. Gemini Robotics-ER 1.5는 체화 추론에서 최고 수준을 보고한다. 시각·공간 이해, 과제 계획, 진행 추정.
- **Gemini Robotics 2 (2026년 7월)**: 발끝부터 손끝까지 휴머노이드의 전신 제어, 22자유도 손을 포함한 여러 말단 장치의 손재주. 여러 단계 계획, 사람과의 대화, 여러 로봇의 조율을 맡는 상위 두뇌 **ER 2**. 그리고 몇 시간의 데이터로 새 몸에 적응하는 가벼운 VLA **On-Device 2**. Apptronik Apollo 2 휴머노이드, Franka, Dexmate, SO101, Trossen 플랫폼에서 시험했다.

### 결과 (보고 기준)

- Gemini Robotics 2의 발표는 숫자 하나가 아니라 범위를 준다. 일반 조작 $45.7$–$76.3\%$, 그리퍼 손재주 $74.2$–$89.6\%$, 그리고 여전히 어렵다고 스스로 적은 다지 과제 $32$–$92\%$.
- 1.5의 이득은 회사 자신의 과제 모음에서 보고된다. 성공의 정의와 시행 수는 보고서에서 읽어야 한다.

### 한계와 비판

- **닫혀 있다.** 가중치가 없다. ER 2는 Google AI Studio로 공개됐고, VLA와 On-Device 2는 초기 파트너에게만 갔다. 모든 숫자가 회사 자신의 과제 모음에서 한 평가라 재현할 수 없다. [[pi0|π0]]의 자체 결과와 같은 처지다.
- **메커니즘을 설명할 뿐 명세하지 않는다.** Motion Transfer는 이름과 동기는 있지만 다시 구현할 만큼 자세하지 않아, 그 기여를 데이터 규모와 떼어 볼 수 없다.
- **추론은 rate로 치른다.** 행동 전의 생각은 순차 디코딩을 쓰고, 그 비용은 [[03-deep-learning/vla/index|4. VLA §6]]이 센다. 보고서들은 제어 주파수를 대표 수치로 내세우지 않는다.

### 영향과 후속 연구

운동 VLA 위에 체화 추론기를 두는 두 모델 패턴 — [[gr00t-n1|GR00T]]의 System 2 / System 1 분할도 따르는 — 과, 교차 embodiment를 데이터 규약이 아니라 학습된 메커니즘으로 보는 관점([[03-deep-learning/vla/index|4. VLA §7]])을 가장 분명히 내세운 계열이다. 모델과 함께 안전 작업도 낸다. 에이전트 안전 벤치마크 ASIMOV-Agentic과 별도의 안전 보고서다.

> [!question] 핵심 주장 읽는 법 · Reading the claim
> "전신 지능"은 특정 휴머노이드에서 시연된 과제 범위에 관한 주장이지 일반 능력에 관한 주장이 아니다. 가장 좋은 숫자가 아니라 범위를 읽고, 각 범위가 어느 플랫폼에서 왔는지 묻고, "몇 시간에 적응"은 같은 시간으로 학습한 전문 모델과 견줄 데이터 예산으로 다뤄라.

### 연결

- 이전: [[rt-2|RT-2]] (웹 VLM → 행동), [[pi0|π0]] (VLM + action expert)
- 병행: [[gr00t-n1|GR00T N1]] (System 2 / System 1), [[03-deep-learning/vla/index|4. VLA §6–§8]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] Name the two models of the family and what each decides · 계열의 두 모델과 각각이 정하는 것을 말할 수 있다
- [ ] Say what 1.5 added (Motion Transfer, thinking before acting) and what each costs · 1.5가 더한 것(Motion Transfer, 행동 전의 생각)과 각각의 대가를 말할 수 있다
- [ ] Say what 2 added and how its results are reported (ranges, platforms) · 2가 더한 것과 결과가 보고되는 방식(범위, 플랫폼)을 말할 수 있다
- [ ] State why none of the numbers can be reproduced · 어떤 숫자도 재현할 수 없는 이유를 말할 수 있다
