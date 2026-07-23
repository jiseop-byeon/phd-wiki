---
title: Automatic Loading of Unknown Material with a Wheel Loader Using RL
tags: [construction, wheel-loader, reinforcement-learning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Eriksson, Ghabcheloo & Geimer · ICRA 2024** — [open PDF](https://researchportal.tuni.fi/files/126570241/icra2024.pdf)

## English

**One-line summary:** A reinforcement-learning controller performs wheel-loader bucket
filling against previously unknown material, bringing learned contact control onto a real
heavy-machine task.

Read the observation/action space, simulator material model, safety envelope, and real-
machine test protocol. The key contribution is not “RL beats control everywhere,” but
that a policy can coordinate vehicle and bucket motion during uncertain pile interaction.

> [!warning] Reading the claim
> “Unknown material” means material not directly parameterized for the policy in the
> reported evaluation; it does not imply all granular materials, pile geometries, weather,
> or machines. Inspect the variation actually tested.

## 한국어

**한 줄:** RL 제어기가 알려지지 않은 재료 더미에서 휠로더의 주행과 버킷 운동을 조정해 실제
중장비 적재를 수행한다. 관측·행동, 재료 시뮬레이션, 안전 영역, 실기계 시험을 함께 읽어야
한다. “unknown”은 평가된 변동 범위 밖 모든 재료를 뜻하지 않는다.

### 읽고 나면 말할 수 있어야 하는 것

- 휠로더 적재에서 RL이 담당하는 제어 범위를 말한다.
- sim-to-real 증거와 안전 장치를 찾는다.
- unknown-material 주장의 실제 시험 분포를 설명한다.
