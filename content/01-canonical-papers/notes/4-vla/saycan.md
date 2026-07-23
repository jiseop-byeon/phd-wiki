---
title: Do As I Can, Not As I Say — SayCan
authors: Michael Ahn et al.
venue: CoRL
year: 2022
pdf: https://arxiv.org/abs/2204.01691
tags: [paper, robotics, language, planning]
status: note-complete
last_verified: 2026-07-23
study-depth: Working
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

## English

**One-line summary:** SayCan combines a language model’s preference over high-level skills
with learned affordance/value estimates of what the robot can execute, selecting grounded
skill sequences without making the language model a low-level controller.

Conceptually, candidate skill $a$ is ranked by a language score “does this advance the
instruction?” times an affordance score “can this robot do it now?” The implementation
and normalization matter; this is a product-of-experts intuition, not a universal formula.

**Lineage:** SayCan bridges language planning and robot skills before RT-2 and modern VLA
models. Its action space is a library of pretrained skills; RT-2/π0 move more of perception
and action generation into one learned model.

> [!warning] Reading the claim
> Grounded language planning does not mean the LM learned new motor skills. Success is
> bounded by the skill library, affordance estimator, perception, and recovery executive.

## 한국어

**한 줄:** SayCan은 언어모델의 고수준 skill 선호와 로봇이 지금 실행할 수 있는지를 나타내는
affordance/value를 결합해 skill 순서를 고른다. 언어모델이 저수준 제어기가 되는 것은 아니다.
미리 학습된 skill library의 한계 안에서 언어 계획을 물리 실행에 접지하며 RT-2·VLA 이전의
중요한 연결점이다.

### 읽고 나면 말할 수 있어야 하는 것

- 언어 점수와 affordance 점수의 역할을 구분한다.
- skill-library planner와 end-to-end VLA의 차이를 말한다.
- SayCan의 성공이 새 운동 기술 학습을 뜻하지 않는 이유를 설명한다.
