---
title: "HIL-SERL — Precise and Dexterous Robotic Manipulation via Human-in-the-Loop Reinforcement Learning"
authors: Jianlan Luo, Charles Xu, Jeffrey Wu, Sergey Levine
affiliation: UC Berkeley
venue: Science Robotics
year: 2025
journal-ref: "Science Robotics 10(105), eads5033"
arxiv: https://arxiv.org/abs/2410.21845
project: https://hil-serl.github.io/
tags: [paper, manipulation, rl, human-in-the-loop, real-world]
status: note-complete
last_verified: 2026-08-22
study-depth: Working
wiki-support: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery when real-world RL becomes the method the thesis uses rather than cites."
---

**Luo, Xu, Wu & Levine, *Science Robotics* 10(105), eads5033, 2025** — [arXiv:2410.21845](https://arxiv.org/abs/2410.21845) · [Project](https://hil-serl.github.io/)

> [!note] Math on-ramp · 수학 준비물
> Off-policy RL and why sample efficiency is the binding constraint on real hardware ([[02-foundations/rl-basics|7. §3–§6]]), plus the interactive-versus-offline argument in [[02-foundations/rl-basics|7. §6]] — this paper is that argument's strongest evidence.
> off-policy RL과 실제 하드웨어에서 표본 효율이 왜 결정적 제약인지([[02-foundations/rl-basics|7. §3~§6]]), 그리고 [[02-foundations/rl-basics|7. §6]]의 상호작용 대 오프라인 논증 — 이 논문이 그 논증의 가장 강한 증거다.

## English

**One-line summary**: A human watches and corrects while a vision-based RL policy trains **on the real robot**, and precision assembly, dynamic manipulation and dual-arm coordination reach near-perfect success in **1 to 2.5 hours** of training.

### Context

RL had a standing promise — autonomous acquisition of complex manipulation skills — and a standing failure to deliver it outside simulation. Meanwhile imitation learning became the default because it works with a fixed dataset and no exploration. The question this paper settles is whether real-world RL was fundamentally impractical or merely badly engineered.

### Method

> [!tip] Key intuition
> The human is not a demonstrator here; the human is a **correction channel inside the training loop**. Demonstrations start the policy, and corrections keep it in the part of the state space where learning is productive — which is what turns "RL needs millions of samples" into "RL needs an afternoon".

The system integrates demonstrations, human corrections, sample-efficient RL algorithms, and a set of system-level design choices. The paper is explicit that the last category matters: it is a *system* result, not an algorithm result, and the design choices are part of the contribution rather than implementation detail.

### Results

> [!important] The numbers to remember
> Near-perfect success rates and fast cycle times within **1 to 2.5 hours** of training, across dynamic manipulation, precision assembly, and dual-arm coordination. Against baselines: an average **2× improvement in success rate** and **1.8× faster execution** compared with imitation-learning baselines and prior RL approaches.

The paper also reports that the learned policies span both **reactive and predictive** control strategies — the policy chooses its own control regime per task rather than being told.

> [!warning] Reading the claim · 핵심 주장 읽는 법
> "Near-perfect" is the abstract's own word; the exact per-task rates are in the body and should be quoted from there. The 2× and 1.8× are *averages over the task suite*, so they compress a spread — a per-task table will show tasks where the margin is much larger and tasks where it is not. And the training-time figure is per task, on a set-up already built: the hours do not include rig construction, reward design, or the operator's time in the loop.
> "거의 완벽"은 초록 자신의 표현이고, 과제별 정확한 수치는 본문에 있으니 거기서 인용해야 한다. 2배와 1.8배는 *과제 묶음 전체의 평균*이므로 분산을 압축한다 — 과제별 표를 보면 격차가 훨씬 큰 과제와 그렇지 않은 과제가 있다. 학습 시간 수치도 이미 구축된 설정 위의 과제당 시간이다: 그 시간에는 장비 구성도, 보상 설계도, 루프 안에 있는 조작자의 시간도 포함되지 않는다.

### Limitations & critique

- **A human must be present for the whole session.** That is a real cost, and it caps how many policies you can train in parallel. The method trades sample efficiency for operator time.
- **Reward specification does not disappear.** Vision-based RL still needs a success signal, and defining one for a contact-rich assembly task is its own research problem.
- **Corrections are only as good as the corrector.** The policy converges toward the operator's judgement, including their mistakes — the same auditability problem [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]] has on the navigation side.
- **Single-cell, single-task training.** Each policy is trained for its task on its rig. Generalisation across tasks is the axis [[01-canonical-papers/notes/4-vla/pi0|π0]] pursues and this method does not.

### Impact & follow-ups

HIL-SERL is the strongest existing evidence for the claim in [[02-foundations/rl-basics|7. §6]] that **interactive learning beats offline learning** on contact-rich manipulation, and it moved real-world RL from "in principle" to "this afternoon". Publication in *Science Robotics* rather than a robotics conference is itself a signal about how the community read the result.

**For construction**: an afternoon per task on the real hardware is a plausible budget for a site process that will be repeated thousands of times — bolt fastening, panel seating, connector insertion. The blocker is not training time; it is that the operator has to stand there, and that the reward signal for "the connection is sound" is not something a camera can see.

### Connections

- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets §11]] — how to read the success rates in this paper's tables: trials, initial-state distribution, seen/unseen split, and whose evaluation it is
- [[02-foundations/rl-basics|7. RL Basics §6]] — the interactive-versus-offline argument this anchors
- [[04-robotics/force-compliance-control|13. Force & Compliance Control]] — the contact regime these tasks live in
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — the imitation baseline it is measured against
- [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration Collection]] — where the demonstrations and corrections come from

### After reading

- [ ] State what role the human plays, and why it is not the demonstrator's role.
- [ ] Explain why "1 to 2.5 hours" is the headline rather than a success rate.
- [ ] Say what the 2× and 1.8× figures average over.
- [ ] Name what the training-time number excludes.

## 한국어

**한 줄 요약**: 사람이 지켜보며 교정하는 동안 비전 기반 RL 정책이 **실제 로봇 위에서** 학습하고, 정밀 조립·동적 조작·양팔 협응이 **1~2.5시간** 학습 만에 거의 완벽한 성공률에 도달한다.

### 배경

RL에는 오래된 약속 — 복잡한 조작 기술의 자율적 습득 — 이 있었고, 시뮬레이션 밖에서 그것을 지키지 못한 오랜 실패가 있었다. 그동안 모방학습이 기본값이 되었는데, 고정된 데이터셋으로 탐색 없이 작동하기 때문이다. 이 논문이 결판내는 질문은 실제 환경 RL이 근본적으로 비현실적이었는가, 아니면 그저 공학이 부실했는가다.

### 방법

> [!tip] 핵심 직관
> 여기서 사람은 시연자가 아니다. 사람은 **학습 루프 안의 교정 채널**이다. 시연이 정책을 출발시키고, 교정이 정책을 학습이 생산적인 상태 공간 영역 안에 붙들어 둔다 — 그것이 "RL에는 수백만 표본이 필요하다"를 "RL에는 오후 한나절이 필요하다"로 바꾼다.

시스템은 시연, 사람의 교정, 표본 효율적 RL 알고리즘, 그리고 시스템 수준 설계 선택들을 통합한다. 논문은 마지막 범주가 중요하다고 명시한다: 알고리즘 결과가 아니라 *시스템* 결과이고, 설계 선택은 구현 세부가 아니라 기여의 일부다.

### 결과

> [!important] 기억할 숫자
> 동적 조작·정밀 조립·양팔 협응에 걸쳐, **1~2.5시간** 학습 안에 거의 완벽한 성공률과 빠른 사이클 타임. 베이스라인 대비: 모방학습 베이스라인과 기존 RL 방법 대비 성공률 평균 **2배 향상**, 실행 속도 **1.8배**.

학습된 정책이 **반응적 제어와 예측적 제어 전략을 모두** 아우른다고도 보고한다 — 정책이 지시받는 대신 과제마다 자기 제어 방식을 고른다.

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> "거의 완벽"은 초록 자신의 표현이고, 과제별 정확한 수치는 본문에 있으니 거기서 인용해야 한다. 2배와 1.8배는 *과제 묶음 전체의 평균*이므로 분산을 압축한다 — 과제별 표를 보면 격차가 훨씬 큰 과제와 그렇지 않은 과제가 있다. 학습 시간 수치도 이미 구축된 설정 위의 과제당 시간이다: 그 시간에는 장비 구성도, 보상 설계도, 루프 안에 있는 조작자의 시간도 포함되지 않는다.
> The 2x and 1.8x figures are averages over the task suite, and the training-time number excludes rig construction, reward design, and operator time.

### 한계와 비판

- **세션 내내 사람이 있어야 한다.** 실제 비용이고, 병렬로 학습시킬 수 있는 정책 수의 상한이 된다. 이 방법은 표본 효율을 조작자 시간과 맞바꾼다.
- **보상 설계가 사라지지는 않는다.** 비전 기반 RL에도 성공 신호가 필요하고, 접촉 많은 조립 과제에서 그것을 정의하는 일 자체가 별도의 연구 문제다.
- **교정은 교정하는 사람만큼만 좋다.** 정책은 조작자의 판단으로 수렴하고, 그 실수까지 함께 수렴한다 — 내비게이션 쪽에서 [[01-canonical-papers/notes/9-navigation/wild-visual-navigation|WVN]]이 갖는 것과 같은 감사 불가능성 문제다.
- **셀 하나, 과제 하나 단위 학습이다.** 각 정책은 자기 장비 위에서 자기 과제를 위해 학습된다. 과제를 가로지르는 일반화는 [[01-canonical-papers/notes/4-vla/pi0|π0]]가 쫓는 축이고 이 방법이 쫓지 않는 축이다.

### 영향과 후속 연구

HIL-SERL은 접촉이 많은 조작에서 **상호작용적 학습이 오프라인 학습을 이긴다**는 [[02-foundations/rl-basics|7. §6]]의 주장을 뒷받침하는 현존하는 가장 강한 증거이고, 실제 환경 RL을 "원리적으로는"에서 "오늘 오후에"로 옮겼다. 로보틱스 학회가 아니라 *Science Robotics*에 실렸다는 사실 자체가 커뮤니티가 이 결과를 어떻게 읽었는지에 대한 신호다.

**건설의 경우**: 수천 번 반복될 현장 공정 — 볼트 체결, 패널 안착, 커넥터 삽입 — 에 대해 실제 하드웨어에서 과제당 오후 한나절은 그럴듯한 예산이다. 병목은 학습 시간이 아니다. 조작자가 거기 서 있어야 한다는 것, 그리고 "접합이 제대로 되었다"는 보상 신호가 카메라로 볼 수 있는 것이 아니라는 것이 병목이다.

### 연결

- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋 §11]] — 이 논문 표의 성공률을 읽는 법: 시행 횟수, 초기 상태 분포, seen/unseen 분할, 그리고 누구의 평가인가
- [[02-foundations/rl-basics|7. RL 기초 §6]] — 이것이 정박하는 상호작용 대 오프라인 논증
- [[04-robotics/force-compliance-control|13. 힘과 컴플라이언스 제어]] — 이 과제들이 사는 접촉 영역
- [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]] — 비교 대상이 되는 모방학습 베이스라인
- [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]] — 시연과 교정이 오는 곳

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 사람이 맡는 역할과, 그것이 왜 시연자의 역할이 아닌지 말한다.
- [ ] 성공률이 아니라 "1~2.5시간"이 왜 헤드라인인지 설명한다.
- [ ] 2배·1.8배 수치가 무엇에 대한 평균인지 말한다.
- [ ] 학습 시간 숫자가 무엇을 제외하는지 댄다.
