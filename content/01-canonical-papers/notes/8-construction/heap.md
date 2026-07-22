---
title: "HEAP — The Autonomous Walking Excavator (Jud et al., 2021)"
authors: Dominic Jud, Simon Kerscher, Martin Wermelinger, et al. (Marco Hutter group)
affiliation: ETH Zurich, Robotic Systems Lab
venue: Automation in Construction
year: 2021
pdf: https://doi.org/10.1016/j.autcon.2021.103783
project: https://rsl.ethz.ch/robots-media/heap.html
tags: [paper, construction, robotics]
status: to-read
---

**Jud et al., Automation in Construction 2021** — [DOI](https://doi.org/10.1016/j.autcon.2021.103783) · [Official](https://rsl.ethz.ch/robots-media/heap.html)

## English

**One-line summary**: A Menzi Muck M545 walking excavator rebuilt for autonomy — force-controllable hydraulics, full-state sensing (GNSS/IMU/LiDAR), and chassis adaptation to arbitrary terrain — the reference *system* for research-grade heavy-machine autonomy.

**What it demonstrates**: autonomous embankment digging and grading; terrain-adaptive
legged chassis; and, in follow-up work, the
[6m dry-stone wall](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)
from irregular local stones (perception + planning + force control in one loop) and
eventually [[01-canonical-papers/notes/8-construction/ext|ExT]]'s learned excavation policies.

**Why it matters for this wiki**: HEAP is what a *platform* investment buys — one
well-instrumented machine has carried a decade of research from classical control to
learning-based digging. The construction analogue of what ALOHA
([[01-canonical-papers/notes/4-vla/act|ACT]]) did for bimanual manipulation research.

## 한국어

**한 줄 요약**: 자율화를 위해 개조된 Menzi Muck M545 보행 굴착기 — 힘 제어 가능한 유압, 완전 상태 센싱(GNSS/IMU/LiDAR), 임의 지형에의 섀시 적응 — 연구급 중장비 자율성의 기준 *시스템*.

**보여준 것**: 자율 제방 굴착과 정지 작업; 지형 적응형 다리 섀시; 그리고 후속 연구에서
불규칙한 현지 돌로 쌓은 [6m 돌담](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)
(인식 + 계획 + 힘 제어가 한 루프에), 그리고 결국 [[01-canonical-papers/notes/8-construction/ext|ExT]]의
학습된 굴착 정책까지.

**이 위키에서 중요한 이유**: HEAP은 *플랫폼* 투자가 무엇을 사는지 보여준다 — 계측이 잘 된
기계 한 대가 고전 제어에서 학습 기반 굴착까지 10년의 연구를 실어 날랐다. ALOHA
([[01-canonical-papers/notes/4-vla/act|ACT]])가 양팔 조작 연구에 한 일의 건설판이다.

### 연결

- 기초: [[04-robotics/mpc|MPC]], [[02-foundations/rl-basics|RL]] · 다음: [[01-canonical-papers/notes/8-construction/ext|ExT]]
- 계보: [[05-construction-robotics/lineage|건설로봇 계보]] (4시대의 기준 시스템)

> [!question] 핵심 주장 읽는 법 · Reading the claim
> 이 논문의 주장은 "자율 보행 굴착기 시스템의 실증"이다 — 새로운 학습 방법론의 기여가 아니다. 시스템/플랫폼 논문의 기준(통합 완성도, 재사용성, 후속 연구를 가능하게 했는가)으로 평가해야 공정하고, 그 기준으로는 이 분야 최고 수준이다.

### 읽고 나면 말할 수 있어야 하는 것 · After reading

- [ ] HEAP의 가치가 개별 결과보다 "계측된 플랫폼"에 있다는 것을 설명할 수 있다
- [ ] 힘 제어 가능한 유압이 자율 굴착의 전제인 이유를 말할 수 있다
- [ ] 돌담 프로젝트의 폐루프(스캔·돌 파악 → 배치 계획 → 힘 제어 조작)를 단계별로 말할 수 있다
- [ ] ALOHA와의 유비 — 플랫폼 하나가 연구 생태계를 만든다 — 를 말할 수 있다
