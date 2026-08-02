---
title: "Open X-Embodiment — Robotic Learning Datasets and RT-X Models"
authors: Open X-Embodiment Collaboration (Google DeepMind + 30+ labs)
affiliation: Google DeepMind and 33 academic/industry labs
venue: ICRA
year: 2024
arxiv: https://arxiv.org/abs/2310.08864
pdf: https://arxiv.org/pdf/2310.08864
project: https://robotics-transformer-x.github.io
tags: [paper, vla, robot-learning, dataset]
status: note-complete
last_verified: 2026-07-22
study-depth: Working
wiki-support: Literacy
depth-goal: "Read the method and evaluation closely enough to select, adapt, or diagnose it."
mastery-when: "Raise to Mastery only when this method or its assumptions become part of the thesis contribution."
---

**Open X-Embodiment Collaboration, ICRA 2024** — [arXiv](https://arxiv.org/abs/2310.08864) · [PDF](https://arxiv.org/pdf/2310.08864) · [Official](https://robotics-transformer-x.github.io)

## English

**One-line summary**: 34 labs pooled 60 datasets — 1M+ trajectories across 22 robot embodiments — into one standardized corpus, and showed that policies trained on the mixture beat specialists on their *own* robots.

### Context

[[rt-1|RT-1]] proved robot-data scaling on one platform, but every lab's data was siloed in
incompatible formats on incompatible robots. NLP and vision scaled on shared corpora
(ImageNet, Common Crawl); robotics had nothing comparable. The bet: does experience
*transfer across robot bodies* — can a Franka arm's data help a WidowX?

### Method

> [!tip] Key intuition
> Treat different robots like different "dialects" of one manipulation language. Standardize
> the serialization (RLDS format), coarsely align camera views and end-effector action
> spaces, train one policy on everything — and let the model discover what transfers.

- **Dataset**: 60 existing datasets, 22 embodiments (single arms, bimanual, quadrupeds),
  500+ skills, 1M+ episodes, unified in RLDS.
- **RT-1-X / RT-2-X**: the [[rt-1|RT-1]] and [[rt-2|RT-2]] architectures retrained on the
  mixture — deliberately *no new method*, isolating the effect of cross-embodiment data.

### Results

- **RT-1-X beats each lab's own specialist model on that lab's robot** — ~50% mean
  improvement across partner domains: positive transfer across bodies is real.
- RT-2-X roughly triples RT-2's performance on emergent-skill evaluations involving
  objects/skills from other datasets.
- Established the shared-corpus norm: nearly every subsequent generalist policy trains on OXE.

### Limitations & critique

- Coverage is skewed (mostly single-arm tabletop pick-place; few forceful, mobile, or
  outdoor tasks — nothing construction-like).
- Coarse action-space alignment (end-effector deltas) papers over real kinematic
  differences; per-embodiment tuning still matters.
- Aggregated demos vary widely in quality and labeling — a curation problem inherited by
  every model trained on it.

### Impact & follow-ups

The ImageNet moment of robot learning: [[octo|Octo]], [[openvla|OpenVLA]], and the
pretraining mixtures of [[pi0|π0]]/[[gr00t-n1|GR00T]]-class models all build on OXE data
and its RLDS convention. For construction robotics, it is the template such a corpus
would need to follow.

### Connections

- Previous: [[rt-1|RT-1]], [[rt-2|RT-2]] · Next: [[octo|Octo]], [[openvla|OpenVLA]]
- Lineage: [[03-deep-learning/lineage|논문 계보도]]

## 한국어

**한 줄 요약**: 34개 랩이 60개 데이터셋 — 22종 로봇, 100만+ 궤적 — 을 하나의 표준 코퍼스로 모았고, 이 혼합물로 학습한 정책이 각 랩의 전문 모델을 *그 랩의 로봇에서* 이긴다는 것을 보였다.

### 배경

[[rt-1|RT-1]]이 한 플랫폼에서 로봇 데이터 스케일링을 증명했지만, 각 랩의 데이터는 호환되지
않는 로봇 위에 호환되지 않는 형식으로 고립되어 있었다. NLP와 비전은 공유 코퍼스(ImageNet,
Common Crawl)로 스케일했는데 로보틱스에는 그런 것이 없었다. 이 논문의 베팅: 경험이
*로봇 몸을 건너* 전이되는가 — Franka 팔의 데이터가 WidowX를 도울 수 있는가?

### 방법

> [!tip] 핵심 직관
> 서로 다른 로봇을 하나의 조작 언어가 가진 "방언들"로 취급하라. 직렬화를 표준화하고(RLDS
> 형식), 카메라 시점과 말단 행동 공간을 거칠게 정렬한 뒤, 전부에 대해 하나의 정책을
> 학습시켜라 — 무엇이 전이되는지는 모델이 발견하게 두라.

- **데이터셋**: 기존 60개 데이터셋, 22종 로봇(단일 팔, 양팔, 사족), 500+ 기술, 100만+
  에피소드를 RLDS로 통일.
- **RT-1-X / RT-2-X**: [[rt-1|RT-1]]과 [[rt-2|RT-2]] 구조를 혼합 데이터로 재학습 —
  의도적으로 *새 기법 없음*, 교차-신체 데이터의 효과만 분리해서 측정.

### 결과

- **RT-1-X가 각 랩의 전문 모델을 그 랩의 로봇에서 이긴다** — 파트너 도메인 평균 약 50%
  개선: 몸을 건너는 양의 전이가 실재한다.
- RT-2-X는 다른 데이터셋의 물체/기술이 관여된 창발 능력 평가에서 RT-2 성능을 약 3배로.
- 공유 코퍼스 규범을 확립: 이후 거의 모든 범용 정책이 OXE로 학습된다.

### 한계와 비판

- 커버리지 편중 (대부분 단일 팔 탁상 pick-place; 힘 쓰는 작업, 이동, 야외 과제는 거의 없음
  — 건설 유사 과제는 전무).
- 거친 행동 공간 정렬(말단 델타)은 실제 기구학 차이를 덮어버린다; 로봇별 튜닝은 여전히 중요.
- 모인 시연들의 품질·라벨 편차가 크다 — 이 위에서 학습되는 모든 모델이 물려받는 큐레이션 문제.

### 영향과 후속 연구

로봇 학습의 ImageNet 모먼트: [[octo|Octo]], [[openvla|OpenVLA]], 그리고 [[pi0|π0]]/[[gr00t-n1|GR00T]]급
모델의 사전학습 혼합물이 모두 OXE 데이터와 RLDS 규약 위에 서 있다. 건설로봇에게는
그런 코퍼스를 만들 때 따라야 할 템플릿이다.

### 연결

- 이전: [[rt-1|RT-1]], [[rt-2|RT-2]] · 다음: [[octo|Octo]], [[openvla|OpenVLA]]
- 계보: [[03-deep-learning/lineage|논문 계보도]]

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] State the problem RLDS standardization solved (format fragmentation) · RLDS 표준화가 푼 문제(형식 파편화)를 말할 수 있다
- [ ] Give the evidence for positive cross-embodiment transfer (RT-1-X beating specialist models) · 서로 다른 로봇 사이에서 양의 전이(positive transfer)가 일어난 증거(RT-1-X가 전문 모델을 이김)를 말할 수 있다
- [ ] State the coverage bias (tabletop pick-and-place heavy) and its downstream effect · 커버리지 편향(탁상 pick-place 중심)과 그 하류 효과를 말할 수 있다
- [ ] Say what template you would take from this paper if you built a construction-robotics dataset · 건설로봇 데이터셋을 만든다면 이 논문에서 가져올 템플릿을 말할 수 있다
