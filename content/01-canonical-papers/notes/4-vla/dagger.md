---
title: "A Reduction of Imitation Learning and Structured Prediction to No-Regret Online Learning (DAgger)"
authors: Stéphane Ross, Geoffrey J. Gordon, J. Andrew Bagnell
affiliation: Carnegie Mellon University
venue: AISTATS
year: 2011
arxiv: https://arxiv.org/abs/1011.0686
tags: [paper, imitation-learning, theory]
status: note-complete
last_verified: 2026-08-21
study-depth: Literacy
wiki-support: Literacy
depth-goal: "Explain the problem, inputs and outputs, central claim, evidence, and one limitation."
mastery-when: "Raise to Working if data collection under the learner's own distribution becomes part of the method."
---

**Ross, Gordon & Bagnell, AISTATS 2011, PMLR vol. 15, pp. 627–635** — [arXiv](https://arxiv.org/abs/1011.0686). DBLP files it under JMLR W&CP vol. 15; citing it as AISTATS 2011 is correct.

> [!note] Math on-ramp · 수학 준비물
> The one thing to hold is the difference between the distribution a policy was *trained* on and the one it *runs* on ([[02-foundations/rl-basics|7. RL Basics §6]] — the horizon figure there is this paper's argument in picture form). Big-O notation is enough for the bound.
> 붙잡을 것 하나: 정책이 *학습된* 분포와 *실행되는* 분포의 차이([[02-foundations/rl-basics|7. RL 기초 §6]] — 거기 있는 지평 그림이 이 논문의 논증을 그림으로 옮긴 것이다). 경계에는 빅오 표기면 충분하다.

## English

**One-line summary**: Recast imitation learning as no-regret online learning, then collect expert labels on the states the *learner* actually visits — turning behaviour cloning's quadratic-in-horizon error growth into a linear one.

### Context

Behaviour cloning trains on the expert's state distribution but runs on its own. Small errors take the policy somewhere the expert never demonstrated, where it has no idea what to do, so it errs further — the compounding-error failure mode. Every subsequent trick in imitation learning is a response to this one problem.

### Method

> [!tip] Key intuition
> The training data is collected from the wrong distribution. So fix the distribution: run the learner, let the expert label the states it actually visited, add those to the dataset, retrain, repeat. The dataset converges to the distribution the policy will face rather than the one the expert preferred.

### Results

The theoretical result is the one to carry: plain behaviour cloning accumulates cost as
$O(\epsilon T^2)$ in the horizon $T$ with per-step error $\epsilon$, while a no-regret method such as DAgger reaches $O(\epsilon T)$ — the difference between a horizon you can grow and one you cannot.

### Limitations & critique

- **It needs an expert that can be queried on demand**, at states the learner chose. For a human demonstrator this is expensive and awkward; for a robot it can also be unsafe, since the states in question are by definition ones the policy reached by erring.
- Interactive data collection does not fit the "collect a dataset, then train" workflow that most robot-learning pipelines are built around.
- The alternative that the field mostly took — action chunking, which shortens the effective horizon rather than fixing the distribution — is cheaper and is why [[01-canonical-papers/notes/4-vla/act|ACT]] exists.

### Connections

- [[04-robotics/legged-locomotion|18. Legged Locomotion §2]] — where this algorithm does its most consequential work: distilling a privileged teacher into a proprioception-only student
- [[02-foundations/rl-basics|7. RL Basics §6]] — where the compounding-error argument and its arithmetic live
- [[01-canonical-papers/notes/4-vla/act|ACT]] — the cheap alternative to the same problem
- [[04-robotics/teleoperation-demonstration|12. §6]] — why demonstrations rarely contain recoveries

### After reading

- [ ] State the distribution mismatch in one sentence.
- [ ] Give the two error rates and say what the difference means practically.
- [ ] Name why DAgger is not the default in robot manipulation despite being the principled fix.

## 한국어

**한 줄 요약**: 모방학습을 no-regret 온라인 학습으로 환원한 뒤, *학습자*가 실제로 방문하는 상태에서 전문가 라벨을 모은다 — 행동 복제의 지평에 대한 이차 오차 증가를 일차로 바꾼다.

### 배경

행동 복제는 전문가의 상태 분포에서 학습되지만 자기 자신의 분포에서 실행된다. 작은 오차가 정책을 전문가가 시연한 적 없는 곳으로 데려가고, 거기서는 무엇을 해야 할지 모르므로 더 크게 틀린다 — 복합 오차 실패 모드다. 모방학습의 이후 모든 요령이 이 하나의 문제에 대한 대응이다.

### 방법

> [!tip] 핵심 직관
> 학습 데이터가 틀린 분포에서 모였다. 그러면 분포를 고쳐라: 학습자를 실행시키고, 실제로 방문한 상태를 전문가가 라벨하고, 데이터셋에 더하고, 재학습하고, 반복한다. 데이터셋이 전문가가 선호한 분포가 아니라 정책이 마주할 분포로 수렴한다.

### 결과

가져갈 것은 이론적 결과다: 순수 행동 복제는 스텝당 오차 $\epsilon$, 지평 $T$에 대해 $O(\epsilon T^2)$로 비용을 누적하는 반면, DAgger 같은 no-regret 방법은 $O(\epsilon T)$에 도달한다 — 늘릴 수 있는 지평과 늘릴 수 없는 지평의 차이다.

### 한계와 비판

- **필요할 때 질의할 수 있는 전문가가 필요하다**, 그것도 학습자가 고른 상태에서. 사람 시연자에게는 비싸고 어색하며, 로봇에서는 안전하지 않을 수도 있다. 문제의 그 상태들은 정의상 정책이 틀려서 도달한 곳이기 때문이다.
- 상호작용적 데이터 수집이 "데이터셋을 모으고 나서 학습한다"는, 대부분의 로봇 학습 파이프라인이 딛고 선 작업 흐름에 맞지 않는다.
- 분야가 대체로 택한 대안 — 분포를 고치는 대신 유효 지평을 줄이는 행동 청킹 — 이 더 싸고, 그것이 [[01-canonical-papers/notes/4-vla/act|ACT]]가 존재하는 이유다.

### 연결

- [[04-robotics/legged-locomotion|18. 레그드 로코모션 §2]] — 이 알고리즘이 가장 큰 일을 하는 곳: 특권 교사를 고유수용 감각만 쓰는 학생으로 증류하기
- [[02-foundations/rl-basics|7. RL 기초 §6]] — 복합 오차 논증과 그 산수가 있는 곳
- [[01-canonical-papers/notes/4-vla/act|ACT]] — 같은 문제에 대한 싼 대안
- [[04-robotics/teleoperation-demonstration|12. §6]] — 시연에 복구가 좀처럼 없는 이유

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 분포 불일치를 한 문장으로 말한다.
- [ ] 두 오차율을 대고 그 차이가 실전에서 무엇을 뜻하는지 말한다.
- [ ] 원리적 해법인데도 DAgger가 로봇 조작의 기본값이 아닌 이유를 댄다.
