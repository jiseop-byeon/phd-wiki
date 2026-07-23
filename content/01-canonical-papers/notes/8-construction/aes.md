---
title: An Autonomous Excavator System for Material Loading Tasks
tags: [construction, excavation, deployment]
status: note-complete
last_verified: 2026-07-23
---

**Zhang et al. · Science Robotics 2021** — [paper](https://doi.org/10.1126/scirobotics.abc3164) · [PubMed record](https://pubmed.ncbi.nlm.nih.gov/34193561/)

## English

**One-line summary:** Baidu’s AES integrated perception, task/motion planning, and control
on multiple excavator sizes, reporting 24 hours per human intervention and material
throughput close to an experienced operator in deployed loading work.

**Method:** LiDAR/camera perception reconstructs terrain and work zones; planning selects
loading actions and trajectories; robust low-level control executes them. The lesson is
system engineering and operational robustness, not a single foundation-model component.

> [!warning] Reading the claim
> Continuous operation in a constrained material-handling site is strong deployment
> evidence, but not proof of general excavation autonomy. Separate machine-size transfer,
> site/task variation, and hours accumulated in the production setting.

**Why it matters:** AES is a rare paper that reports industrial-duration autonomy and a
human productivity comparison. It is the deployment counterweight to simulation-heavy
learning papers.

## 한국어

**한 줄:** Baidu AES는 여러 크기의 굴착기에 인식·과제/모션 계획·제어를 통합해 실제 적재
작업에서 인간 개입당 24시간 운용과 숙련 운전자에 가까운 처리량을 보고했다.

강점은 단일 AI 모듈이 아니라 운용 강건성이다. 다만 제한된 재료 처리 현장의 연속 운용이
모든 굴착·토질·현장으로의 일반성을 증명하지는 않는다.

### 읽고 나면 말할 수 있어야 하는 것

- AES의 모듈형 스택과 배치 증거를 설명한다.
- 24시간 지표의 정확한 의미를 말한다.
- 학습 신규성과 시스템 완결성을 구분한다.
