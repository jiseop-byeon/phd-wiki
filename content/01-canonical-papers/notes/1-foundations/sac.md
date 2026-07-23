---
title: Soft Actor-Critic
authors: Tuomas Haarnoja et al.
venue: ICML
year: 2018
pdf: https://arxiv.org/abs/1801.01290
tags: [paper, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

## English

**One-line summary:** SAC is an off-policy actor–critic algorithm that maximizes expected
return plus policy entropy, encouraging useful exploration while learning from replayed
experience.

The maximum-entropy objective is $\mathbb{E}[\sum_t r(s_t,a_t)+\alpha\mathcal{H}(\pi(\cdot|s_t))]$.
The actor, critic, target updates, replay buffer, and temperature $\alpha$ must be read
together. Entropy encourages stochasticity; it does not guarantee safe exploration.

**Why here:** Continuous actions and replay efficiency make SAC a recurring baseline for
hydraulic machines and manipulation. Off-policy reuse is attractive when samples are
expensive, but real machines still require simulation, constraints, or supervised data.

## 한국어

**한 줄:** SAC는 기대 보상과 정책 entropy를 함께 최대화하고 replay 경험을 쓰는 off-policy
actor–critic이다. 연속 제어와 샘플 재사용 때문에 중장비·조작의 빈번한 기준선이지만 entropy가
안전 탐색을 보장하지는 않는다.

### 읽고 나면 말할 수 있어야 하는 것

- 보상과 entropy 항의 trade-off를 설명한다.
- on-policy PPO와 off-policy SAC의 데이터 사용 차이를 말한다.
- 실제 장비에서 replay efficiency만으로 충분하지 않은 이유를 설명한다.
