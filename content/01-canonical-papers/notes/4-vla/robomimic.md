---
title: "What Matters in Learning from Offline Human Demonstrations for Robot Manipulation (robomimic)"
authors: Ajay Mandlekar, Danfei Xu, Josiah Wong, et al.
affiliation: Stanford University, UT Austin, NVIDIA
venue: CoRL
year: 2021
arxiv: https://arxiv.org/abs/2108.03298
project: https://robomimic.github.io
tags: [paper, robot-learning, imitation-learning, benchmark]
status: note-complete
last_verified: 2026-08-21
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when demonstration-data design is part of the thesis contribution."
---

**Mandlekar et al., CoRL 2021, PMLR vol. 164, pp. 1678–1690** — [arXiv](https://arxiv.org/abs/2108.03298) · [Official](https://robomimic.github.io). Cite as CoRL 2021 although the PMLR volume is stamped 2022.

> [!note] Math on-ramp · 수학 준비물
> Behaviour cloning and its failure mode ([[02-foundations/rl-basics|7. RL Basics §6]]), plus the experimental-design vocabulary for reading a controlled comparison — what is held fixed, what varies, and what a difference between two numbers can and cannot mean ([[02-foundations/ml-practice|9. ML Practice]]).
> 행동 복제와 그 실패 모드([[02-foundations/rl-basics|7. RL 기초 §6]]), 그리고 통제된 비교를 읽는 실험 설계 어휘 — 무엇이 고정되고 무엇이 변하며, 두 숫자의 차이가 무엇을 뜻할 수 있고 없는지([[02-foundations/ml-practice|9. ML 실무]]).

## English

**One-line summary**: A large controlled study isolating what actually drives offline learning performance from human manipulation data — dataset quality, algorithmic choices, observation space, stopping criteria — released with the open-source robomimic benchmark and datasets.

### Context

The area had a reproducibility problem hiding inside a progress narrative: papers reported success rates on different datasets, with different observation spaces, different stopping criteria and different demonstration sources, and the field had no way to tell which of those differences produced the numbers.

### Method

> [!tip] Key intuition
> Before asking which algorithm is best, ask what the comparison is even holding fixed. Most of the apparent difference between manipulation-learning methods is a difference in what they were fed and when they were stopped.

A controlled sweep across algorithms, datasets and design choices, with the whole apparatus released so others can run the same comparison.

### Results

From the **abstract**: "an extensive study of **six** offline learning algorithms for robot manipulation on **five** simulated and **three** real-world multi-stage manipulation tasks of varying complexity."

> [!warning] Reading the claims · 주장 읽는 법
> **The abstract reports no success rates** — only the scale of the study. The specific findings people cite from this paper (which choices matter most, what operator variation costs) are in the body. That is appropriate for a study paper, but it means every "robomimic showed that…" claim needs a section number attached.
> **초록에는 성공률이 없다** — 연구의 규모만 있다. 이 논문에서 사람들이 인용하는 구체적 발견(어떤 선택이 가장 중요한가, 조작자 변동이 얼마나 비싼가)은 본문에 있다. 연구 논문으로서 적절하지만, "robomimic이 보였듯…"이라는 모든 주장에 절 번호를 붙여야 한다는 뜻이다.

### Limitations & critique

- **A study inherits the scope of its sweep.** Six algorithms and eight tasks is large, but conclusions are about that space, and manipulation-learning has moved since 2021.
- Simulation-heavy: five simulated tasks against three real ones.
- The benchmark's own existence shapes the field it measures — a common and largely benign effect, but worth naming when a later paper reports "state of the art on robomimic".

### Connections

- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection §6]] — the data-quality axes this study is the evidence for
- [[02-foundations/rl-basics|7. RL Basics §6]] — the imitation toolbox it evaluates
- [[06-research-practice/experimental-design-reproducibility|Experimental Design & Reproducibility]] — the methodology this paper exemplifies

### After reading

- [ ] Say what question this paper asks that a method paper does not.
- [ ] State what its abstract does and does not report.
- [ ] Name two data properties a count of demonstrations does not capture.

## 한국어

**한 줄 요약**: 사람의 조작 데이터로부터의 오프라인 학습 성능을 실제로 좌우하는 것 — 데이터셋 품질, 알고리즘 선택, 관측 공간, 중단 기준 — 을 분리해 낸 대규모 통제 연구. 오픈소스 robomimic 벤치마크와 데이터셋과 함께 공개되었다.

### 배경

이 분야에는 진보의 서사 안에 숨은 재현성 문제가 있었다: 논문마다 다른 데이터셋, 다른 관측 공간, 다른 중단 기준, 다른 시연 출처에서 성공률을 보고했고, 그중 무엇이 그 숫자를 만들었는지 분야가 판별할 방법이 없었다.

### 방법

> [!tip] 핵심 직관
> 어느 알고리즘이 최고인지 묻기 전에, 그 비교가 도대체 무엇을 고정하고 있는지 물어라. 조작 학습 방법들 사이의 겉보기 차이 대부분은 무엇을 먹였고 언제 멈췄는지의 차이다.

알고리즘·데이터셋·설계 선택을 가로지르는 통제된 스윕. 다른 사람들이 같은 비교를 돌릴 수 있도록 전체 장치를 공개했다.

### 결과

**초록**에서: "복잡도가 다양한 시뮬레이션 과제 **다섯** 개와 실세계 다단계 조작 과제 **세** 개에 대한 로봇 조작용 오프라인 학습 알고리즘 **여섯** 개의 광범위한 연구."

> [!warning] 주장 읽는 법 · Reading the claim
> **초록에는 성공률이 없다** — 연구의 규모만 있다. 사람들이 인용하는 구체적 발견은 본문에 있다. "robomimic이 보였듯…"이라는 모든 주장에 절 번호를 붙여야 한다는 뜻이다.
> The abstract reports only the study's scale, no success rates.

### 한계와 비판

- **연구는 자기 스윕의 범위를 물려받는다.** 알고리즘 여섯에 과제 여덟은 크지만 결론은 그 공간에 관한 것이고, 조작 학습은 2021년 이후 움직였다.
- 시뮬레이션 비중이 크다: 시뮬 다섯 대 실제 셋.
- 벤치마크의 존재 자체가 그것이 재는 분야를 형성한다 — 흔하고 대체로 무해한 효과이지만, 후속 논문이 "robomimic에서 state of the art"를 보고할 때 지목해 둘 가치가 있다.

### 연결

- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집 §6]] — 이 연구가 근거가 되는 데이터 품질 축들
- [[02-foundations/rl-basics|7. RL 기초 §6]] — 이 논문이 평가하는 모방학습 도구상자
- [[06-research-practice/experimental-design-reproducibility|실험 설계와 재현성]] — 이 논문이 예시하는 방법론

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 이 논문이 방법 논문은 하지 않는 어떤 질문을 하는지 말한다.
- [ ] 초록이 보고하는 것과 보고하지 않는 것을 말한다.
- [ ] 시연 개수가 담지 못하는 데이터 성질 둘을 댄다.
