---
title: Proximal Policy Optimization Algorithms
authors: John Schulman et al.
venue: arXiv
year: 2017
pdf: https://arxiv.org/abs/1707.06347
tags: [paper, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

## English

**One-line summary:** PPO reuses policy-gradient data for several minibatch updates while
clipping probability-ratio changes that would move the new policy too far from the data-
collecting policy.

The clipped surrogate is $L=\mathbb{E}[\min(r_tA_t,\operatorname{clip}(r_t,1-\epsilon,1+\epsilon)A_t)]$,
where $r_t=\pi_\theta(a_t|s_t)/\pi_{old}(a_t|s_t)$. Clipping limits the *incentive* for
excessive change; it is not a hard bound on parameter distance or guaranteed monotonic
improvement.

**Why here:** PPO is a common recipe for simulator experts and RL fine-tuning in locomotion
and heavy-machine policies. In ExT-like pipelines, distinguish PPO generating/finetuning
behavior from the transformer policy that is ultimately deployed.

> [!warning] Reading the claim
> “PPO-trained” does not specify observation design, reward, simulator, curriculum, safety
> constraints, or real transfer. These choices often explain more than the optimizer name.

## 한국어

**한 줄:** PPO는 행동 확률비의 과도한 변화를 유도하는 항을 clip하면서 정책경사 데이터를
여러 minibatch update에 재사용한다. Clip은 업데이트 유인을 제한할 뿐 파라미터 거리의
hard constraint나 성능 단조 향상을 보장하지 않는다. 중장비 논문에서는 PPO 자체보다 관측,
보상, 시뮬레이터, 안전 영역, 실기계 전이를 함께 읽어야 한다.

### 읽고 나면 말할 수 있어야 하는 것

- $r_t$, advantage, clip이 각각 무엇을 하는지 설명한다.
- PPO clip이 보장하지 않는 것을 말한다.
- 굴착 pretraining/finetuning 파이프라인에서 PPO의 역할을 찾는다.
