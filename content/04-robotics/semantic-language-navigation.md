---
title: 19. Semantic & Language-Driven Navigation
tags: [robotics, navigation, vlm]
study-depth: Working
wiki-support: Working
depth-goal: "State the ObjectNav and VLN task definitions and metrics, explain why the nav-graph formulation was abandoned, and say what happened to the field's benchmarks."
mastery-when: "Raise to Mastery only if language-grounded navigation becomes the contribution."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to read this literature accurately, and to know why its leaderboards
> stopped being the thing to climb.
> **Working** — 이 문헌을 정확히 읽고, 그 리더보드가 왜 더 이상 오를 대상이 아니게 되었는지
> 알 만큼.

> [!note] Prerequisites · 선수 지식
> You need CLIP-style vision-language grounding ([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), frontier-based exploration and costmaps ([[04-robotics/planning-decision-making|4. Planning]]), and what a VLA is ([[01-canonical-papers/notes/4-vla/rt-2|RT-2]]).
> CLIP식 시각-언어 접지([[01-canonical-papers/notes/3-vlm/clip|CLIP]]), 프런티어 기반 탐색과 costmap([[04-robotics/planning-decision-making|4. 계획]]), 그리고 VLA가 무엇인지([[01-canonical-papers/notes/4-vla/rt-2|RT-2]])가 필요하다.

## English

*Group I. Stands on [[04-robotics/planning-decision-making|4. Planning]] and, in practice, on the VLM notes.
When the goal is a word rather than a coordinate, the hard problem stops being path-finding and becomes deciding where to look.*

> [!note] First pass · 처음이라면
> Read §1 — the shift a classically trained reader has to make — then §2, because most confusion here is people arguing about ObjectNav without agreeing on its definition, then §8. §3 to §7 are the history; read it once the definitions are solid.

### 1. The shift a classical reader has to make

Classically the goal is a **pose in a known metric space**, and planning is finding a path to
it. Here the goal is a **word** — "toilet", or "go past the kitchen and turn left at the
plant" — its location is unknown, and the hard problem is not path-finding at all. It is
**deciding where to look.**

That converts exploration from a coverage problem into an inference problem over
object-and-room co-occurrence, and it is why a vision-language model turns out to be a
navigation component.

### 2. ObjectNav — the definition, stated precisely

The agent spawns at a random pose in a **previously unseen** environment, is given only a
goal object *category*, and must navigate to **any instance** and signal completion.
Observations are RGB-D plus a noiseless GPS+Compass; no map, no scene graph, no ground-truth
semantics.

The success criterion is two-part, and the second half is what makes it a real task:

> On emitting `STOP`, the agent must be **within 1.0 m** of an instance of the target
> category **and** the object must be viewable by an oracle from that stopping position by
> turning or looking up and down.

Without the visibility clause an agent could succeed standing on the far side of a wall
0.9 m from the goal. Metrics are Success Rate and **SPL**, with the shortest path measured
to the instance nearest the agent's *start*.

> [!warning] Both defining documents are unrefereed
> SPL was introduced in *On Evaluation of Embodied Navigation Agents* (2018), which
> describes itself as a working-group report. The task definition comes from
> *ObjectNav Revisited* (2020). **Neither was ever peer-reviewed**, and between them they
> define the metrics the entire literature reports. That is worth saying out loud when you
> cite them.

> [!example] Worked example · 계산 예제
> **What an SPL of 0.47 actually says.** Success weighted by Path Length (Anderson et al. 2018)
> is $\text{SPL} = \frac{1}{N}\sum_i S_i \frac{\ell_i}{\max(p_i, \ell_i)}$, where $S_i$ is
> success, $\ell_i$ the shortest path and $p_i$ the path actually walked. Three episodes:
>
> | Episode | Success | Shortest $\ell$ | Walked $p$ | Term |
> |---|---|---|---|---|
> | 1 | yes | 10 m | 10 m | $1 \times 10/10 = 1.00$ |
> | 2 | yes | 10 m | 25 m | $1 \times 10/25 = 0.40$ |
> | 3 | no | 10 m | 8 m | $0$ |
>
> $\text{SPL} = (1.00 + 0.40 + 0)/3 = \mathbf{0.47}$, while the success rate is $2/3 = 0.67$.
>
> **The reading this gives you.** An agent that succeeds *every single time* but always walks
> twice the shortest path scores $1 \times 10/20 = 0.50$ — so 0.47 is compatible with a
> near-perfect navigator that wanders, and equally with a 47% navigator that walks straight
> lines. SPL alone cannot tell you which. This is why an SPL reported without its success rate
> is uninterpretable, and why the field now insists on both. When a paper shows only SPL and
> claims an efficiency improvement, check whether success moved at all.

### 3. The method arc, in three moves

**Move 1 — modular semantic mapping.** Active Neural SLAM established the skeleton: learned
SLAM, a global policy choosing long-term goals, an analytical planner, and a local policy.
Its thesis is that hierarchy plus classical planning beats end-to-end RL on sample
complexity. **SemExp** put a semantic map in that skeleton and let a learned global policy
pick long-term exploration goals on it. It won the 2020 challenge and its architecture is
still the backbone.

**Move 2 — replace the learned scorer with a pretrained VLM, and train nothing.**
**VLFM** builds an occupancy map, extracts frontiers, and scores each frontier by
**vision-language similarity to the goal text**, choosing where to explore next. No ObjectNav
training data at all, and it deployed on a real Spot. **ESC** does the same job with LLM
commonsense — object-and-room co-occurrence — compiled into soft logic predicates over a
frontier scorer. And **CoWs** established that zero-shot approaches match or beat trained
state of the art, while being weak at exploiting complex language.

**Move 3 — throw the modular apparatus away.** See §5.

> [!note] Cite CoWs by its real title
> The paper is *"CoWs on Pasture: Baselines and Benchmarks for Language-Driven Zero-Shot
> Object Navigation."* "CLIP on Wheels" is the *method* name. Secondary sources routinely
> miscite this.

### 4. The critique that reframes everything

Gervet et al. tested classical, modular-learning and end-to-end approaches on real robots
**across six real homes**:

| Approach | Result |
|---|---|
| **Modular learning** | **90% real-world success** |
| **End-to-end learning** | **77% in simulation → 23% in the real world** |

The load-bearing conclusion is not the gap itself but its explanation: simulators fail as
evaluation benchmarks for **two** reasons — the visual sim-to-real gap, and **misaligned
error patterns**. Simulation and reality fail in *different ways*, so **simulation ranking
does not preserve real-world ranking.** A leaderboard can be climbed without the thing it
measures improving.

### 5. VLN, and the paper that admitted the benchmark was cheating

**R2R** created the task and the Matterport3D Simulator: follow a natural-language route
instruction through a real building. But R2R is **discrete** — the agent teleports between
nodes of a pre-built navigation graph. **RxR** added multilingual instructions and
word-level temporal alignment to poses, and corrected R2R's path bias (R2R paths are all
shortest paths, which lets an agent cheat).

**VLN-CE is the most consequential paper in this literature.** It ports R2R into Habitat with
**low-level continuous actions**, removing three assumptions at once — known topology, oracle
navigation, perfect localization — and performance drops dramatically. The conclusion the
field accepted without rebuttal: **prior nav-graph results were inflated by their own
simplifying assumptions.**

The empirical companion is Anderson et al.'s sim-to-real study: **55.9% in simulation →
46.8% real with a pre-built map → 22.5% real with no prior mapping.**

The transformer era — **HAMT** (a hierarchical ViT over the full history of past panoramas,
gaining most on long trajectories) and **DUET** (a topological map built on the fly,
combining coarse global planning including backtracking with fine local encoding) — is the
high-water mark of the discrete paradigm, and worth reading as such.

Then **NaVid** broke it: a video VLM taking **monocular RGB video only — no maps, no
odometry, no depth** — and emitting actions directly. It threw away the entire modular
apparatus HAMT and DUET depended on, and every 2025–2026 result descends from it.

> [!important] Say it precisely
> **The nav-graph action space is deprecated, not R2R.** VLN-CE *is* R2R and RxR ported into
> Habitat, so the instruction corpora remain the linguistic substrate the whole field runs
> on. "R2R is obsolete" is wrong; "the nav-graph formulation is deprecated" is right.

### 6. The two threads merged, and the benchmarks dissolved

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="two separate navigation threads from 2018 converging into one video-VLA by 2025, while the challenges end">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="34" y1="212" x2="528" y2="212"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="60" y1="212" x2="60" y2="218"/><line x1="180" y1="212" x2="180" y2="218"/><line x1="300" y1="212" x2="300" y2="218"/><line x1="380" y1="212" x2="380" y2="218"/><line x1="460" y1="212" x2="460" y2="218"/>
  </g>
  <g fill="currentColor">
    <rect x="34" y="52" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="34" y="112" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="392" y="76" width="136" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="34" y="52" width="250" height="32" rx="3"/><rect x="34" y="112" width="250" height="32" rx="3"/><rect x="392" y="76" width="136" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.8" marker-end="url(#arS)">
    <path d="M 290 68 L 340 68 L 340 92 L 386 92"/>
    <path d="M 290 128 L 340 128 L 340 106 L 386 106"/>
  </g>
  <defs><marker id="arS" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="72">ObjectNav &#8212; find a named object</text>
    <text x="46" y="132">VLN &#8212; follow a route instruction</text>
    <text x="460" y="95" text-anchor="middle" font-size="11">one video-VLA</text>
    <text x="460" y="110" text-anchor="middle" font-size="9">nav + object search + EQA + following</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="60" y="230" text-anchor="middle">2018</text><text x="180" y="230" text-anchor="middle">2020</text><text x="300" y="230" text-anchor="middle">2023</text><text x="380" y="230" text-anchor="middle">2024</text><text x="460" y="230" text-anchor="middle">2025</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" stroke-dasharray="4 3">
    <line x1="300" y1="160" x2="300" y2="206"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="306" y="170">Oct 2023: Habitat Challenge archived, read-only</text>
    <text x="306" y="184">CVPR 2026: zero navigation challenges</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="34" y="250">Navigation was not solved. It was absorbed &#8212; upward into VLAs, sideways into mobile manipulation.</text>
  </g>
</svg>

**Uni-NaVid** is the merge: one video-VLA trained on 3.6M samples spanning **VLN, object
search, embodied question answering and person-following**, reporting state of the art across
all of them at 5 Hz. In 2020 those were separate communities with separate simulators and
separate challenges.

Simultaneously the institutional scaffolding came down. The Habitat Challenge repository was
**archived read-only in October 2023** and the 2023 edition was the last. The CVPR 2025
Embodied AI Workshop ran four challenges and **none was ObjectNav**; CVPR 2026 ran three and
**all three were manipulation**.

Where the energy went is measurable: **open-vocabulary mobile manipulation**, where HomeRobot
reports ~20% real-world success and the challenge post-mortem records a baseline of **0.8%**
rising to a winning **10.8%** — a 13× improvement that still leaves the task ~90% unsolved.
That is a leaderboard worth climbing; a saturated six-category ObjectNav was not.

The successors that did appear are open-vocabulary by construction: **HM3D-OVON** (379
categories, free-form language goals) and **GOAT-Bench** (goals given as a category, a
description, *or* an image, over long horizons with memory).

### 7. The other half: maps you can query with language

Running alongside, and now more consequential than the ObjectNav leaderboard:

- **VLMaps** fuses vision-language features into a 3D reconstruction the robot builds itself,
  enabling **spatial** language goals — "between the sofa and the TV" — via LLM code
  generation, and emitting robot-specific obstacle maps shareable across embodiments.
- **ConceptFusion**'s distinctive claim is *multimodal query*: language, image, audio, and a
  click all index the same map.
- **ConceptGraphs** replaced dense feature fields with an **object-centric graph** — multi-view
  fusion into nodes, LLM-inferred edges. Cheaper and composable, which is why it became the
  default backbone.
- **Clio** asks the better question: granularity is not a fixed threshold but is **derived
  from the task list via an Information Bottleneck**. The same scene needs a coarse map for
  navigation and a fine one for manipulation, and the task should decide.
- **Hydra** is the real-time systems foundation the rest assumes, with **Khronos** extending
  it to spatio-temporal mapping in dynamic environments.

Two structural facts about 2025–2026: **Gaussian splatting displaced NeRF** as the semantic
substrate, so LERF-style radiance fields are legacy; and **scene graphs won on the robotics
side and absorbed splats** — the graph is the queryable interface, splats are the geometry
underneath.

> [!important] This is where the wiki's perception notes were heading
> [[01-canonical-papers/notes/2-computer-vision/sam|SAM]],
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]],
> [[01-canonical-papers/notes/2-computer-vision/dino|DINO]],
> [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]]
> and [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]] are the *ingredients*. This
> section is what gets built out of them — and the map is where navigation and manipulation
> meet before any controller does.

### 8. Reading a paper in this area

| Question | What a vague answer hides |
|---|---|
| Nav-graph or continuous? | Nav-graph numbers are not comparable to VLN-CE numbers |
| Simulation or real robot? | Sim ranking does not preserve real ranking |
| Was any ObjectNav training data used? | The strong modern results train nothing |
| Which HM3D/MP3D split, and how many categories? | 6-category ObjectNav is saturated; 379-category is not |
| Is the language actually load-bearing? | Rephrase-sensitivity is the standard failure |
| SPL or bare success rate? | Success alone rewards inefficient wandering |

### After reading

- [ ] State the ObjectNav success criterion, including the visibility clause, and why it exists.
- [ ] Explain what VLN-CE removed and what it showed.
- [ ] Give the modular-versus-end-to-end real-world numbers and the reason behind them.
- [ ] Say what happened to the Habitat Challenge and where the field went.
- [ ] Name the map representation that became the default backbone, and Clio's better question.

### Self-check

1. Why does the ObjectNav success criterion have two parts?
2. A 2026 paper reports 68% success on nav-graph R2R. What do you conclude?
3. A method scores well on a simulated navigation benchmark. What does Gervet et al. say you
   may *not* infer?
4. ObjectNav challenges stopped running. Does that mean object-goal navigation is solved?
5. You want a map that supports both navigating to a room and grasping something in it. What
   does the current literature suggest?

> [!tip]- Answers
> 1. Because proximity alone is not the task. Without the oracle-visibility clause an agent could stop 0.9 m from the target with a wall between them and be scored correct — which would reward reaching a *coordinate* rather than finding an *object*. The two-part criterion is what makes ObjectNav a perception problem rather than a metric-navigation problem in disguise.
> 2. That the number is not comparable to anything current, and that the paper is reporting on a formulation the field deprecated. VLN-CE showed nav-graph results are inflated by known topology, oracle navigation and perfect localization; every 2024–2026 result reports R2R-CE instead. The R2R *instructions* are still the substrate — it is the teleporting action space that is obsolete.
> 3. That its real-world ranking will follow. Their finding is not merely that performance drops but that **simulation and reality fail in different ways**, so the ordering between methods is not preserved. End-to-end went 77% sim → 23% real while modular learning reached 90% real — a reversal, not a uniform discount. Sim results are evidence about sim.
> 4. No — it means the benchmark stopped measuring something worth measuring, at six categories in simulation. The task moved to open-vocabulary form (HM3D-OVON's 379 categories, GOAT-Bench's multi-modal lifelong goals) and got absorbed into video-VLAs that do navigation alongside object search and question answering. Meanwhile the real-world version, inside open-vocabulary mobile manipulation, sits around 10–20%.
> 5. That granularity should be **task-derived rather than fixed** — Clio's Information Bottleneck formulation exists precisely because navigation wants a coarse map and manipulation wants a fine one of the same scene. Architecturally, build an object-centric scene graph (the ConceptGraphs lineage) as the queryable interface, over whatever geometric substrate you use, and let the task list set the level of detail.

### Sources

**Definitions and evaluation** — P. Anderson, A. Chang, D. S. Chaplot, et al., "On Evaluation of Embodied Navigation Agents," [arXiv:1807.06757](https://arxiv.org/abs/1807.06757), 2018 (introduces SPL; **unrefereed**); D. Batra, A. Gokaslan, A. Kembhavi, et al., "ObjectNav Revisited," [arXiv:2006.13171](https://arxiv.org/abs/2006.13171), 2020 (**unrefereed**).

**Simulators and datasets** — Habitat (ICCV 2019, [arXiv:1904.01201](https://arxiv.org/abs/1904.01201)); Habitat 2.0 (NeurIPS 2021); Habitat 3.0 (ICLR 2024); HM3D (NeurIPS 2021 D&B); HM3D-Semantics (CVPR 2023); HM3D-OVON ([arXiv:2409.14296](https://arxiv.org/abs/2409.14296)); GOAT-Bench ([arXiv:2404.06609](https://arxiv.org/abs/2404.06609)).

**ObjectNav methods** — Active Neural SLAM (ICLR 2020, [arXiv:2004.05155](https://arxiv.org/abs/2004.05155)); SemExp ([arXiv:2007.00643](https://arxiv.org/abs/2007.00643), CVPR 2020 challenge winner); "CoWs on Pasture" (CVPR 2023, [arXiv:2203.10421](https://arxiv.org/abs/2203.10421)); VLFM (ICRA 2024, [arXiv:2312.03275](https://arxiv.org/abs/2312.03275)); ESC (ICML 2023, [arXiv:2301.13166](https://arxiv.org/abs/2301.13166)).

**The critique** — T. Gervet, S. Chintala, D. Batra, J. Malik, D. S. Chaplot, "Navigating to Objects in the Real World," *Science Robotics*, 2023 ([arXiv:2212.00922](https://arxiv.org/abs/2212.00922)).

**VLN** — R2R (CVPR 2018 Spotlight, [arXiv:1711.07280](https://arxiv.org/abs/1711.07280)); RxR (EMNLP 2020, [arXiv:2010.07954](https://arxiv.org/abs/2010.07954)); VLN-CE (ECCV 2020, [arXiv:2004.02857](https://arxiv.org/abs/2004.02857)); HAMT (NeurIPS 2021, [arXiv:2110.13309](https://arxiv.org/abs/2110.13309)); DUET (CVPR 2022, [arXiv:2202.11742](https://arxiv.org/abs/2202.11742)); sim-to-real: P. Anderson et al., CoRL 2020 ([arXiv:2011.03807](https://arxiv.org/abs/2011.03807)); NaVid (RSS 2024, [arXiv:2402.15852](https://arxiv.org/abs/2402.15852)); Uni-NaVid (RSS 2025, [arXiv:2412.06224](https://arxiv.org/abs/2412.06224)); NaVILA (RSS 2025, [arXiv:2412.04453](https://arxiv.org/abs/2412.04453)).

**Language-queryable maps** — Hydra (RSS 2022, [arXiv:2201.13360](https://arxiv.org/abs/2201.13360)); Khronos (RSS 2024); CLIP-Fields (RSS 2023); ConceptFusion (RSS 2023, [arXiv:2302.07241](https://arxiv.org/abs/2302.07241)); VLMaps (ICRA 2023, [arXiv:2210.05714](https://arxiv.org/abs/2210.05714)); ConceptGraphs (ICRA 2024, [arXiv:2309.16650](https://arxiv.org/abs/2309.16650)); HOV-SG (RSS 2024); Clio (*IEEE RA-L* 9(10):8921–8928, 2024, [arXiv:2404.13696](https://arxiv.org/abs/2404.13696)).

**Where the energy went** — HomeRobot (CoRL 2023, [arXiv:2306.11565](https://arxiv.org/abs/2306.11565)); the OVMM challenge post-mortem ([arXiv:2407.06939](https://arxiv.org/abs/2407.06939)).

**Within this wiki**

- **Paper notes** — [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] · [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] · [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] · [[01-canonical-papers/notes/9-navigation/navid|NaVid]] · [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] · [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] · [[01-canonical-papers/notes/9-navigation/clio|Clio]] · [[01-canonical-papers/notes/9-navigation/vint-nomad|ViNT / NoMaD]] · [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al. 2023]]
- [[04-robotics/navigation-mobile-manipulation|16. Navigation & Mobile Manipulation]] — the geometric half of the same problem
- [[04-robotics/traversability-off-road|17. Traversability & Off-Road Autonomy]] — the outdoor counterpart
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]] and [[01-canonical-papers/notes/2-computer-vision/sam|SAM]] — the ingredients §7 assembles

## 한국어

*I군이다. [[04-robotics/planning-decision-making|4. 계획]] 위에 서고, 실질적으로는 VLM 노트에도 기댄다.
목표가 좌표가 아니라 단어일 때 어려운 문제는 경로 찾기가 아니라 어디를 볼지 정하는 것이 된다.*

> [!note] 처음이라면 · First pass
> 먼저 §1 — 고전적 독자가 해야 하는 전환 — 그다음 §2, 이 분야 혼란 대부분이 ObjectNav의 정의에 합의하지 않은 채 논쟁하는 데서 오기 때문이다 — 그다음 §8. §3~§7은 역사이니 정의가 단단해진 뒤에 읽어라.

### 1. 고전적 독자가 해야 하는 전환

고전적으로 목표는 **알려진 계량 공간의 자세**이고, 계획은 거기로 가는 경로를 찾는 것이다. 여기서
목표는 **단어**다 — "변기", 또는 "주방을 지나 화분에서 왼쪽" — 그 위치는 알려져 있지 않고,
어려운 문제는 경로 찾기가 전혀 아니다. **어디를 볼지 정하는 것**이다.

그것이 탐색을 커버리지 문제에서 물체-방 동시 출현에 대한 추론 문제로 바꾸고, 시각-언어 모델이
내비게이션 구성 요소가 되는 이유다.

### 2. ObjectNav — 정의를 정확히

에이전트가 **처음 보는** 환경의 임의 자세에서 시작해, 목표 물체의 *범주*만 받고, **아무 인스턴스**
로든 이동해 완료를 알려야 한다. 관측은 RGB-D와 잡음 없는 GPS+Compass이고, 지도도, 장면 그래프도,
정답 의미 라벨도 없다.

성공 기준은 두 부분이며, 두 번째 절반이 이것을 진짜 과제로 만든다:

> `STOP`을 낼 때, 에이전트는 목표 범주 인스턴스로부터 **1.0 m 이내**에 있어야 **하고**, 그 정지
> 위치에서 회전하거나 위아래를 봄으로써 오라클이 그 물체를 볼 수 있어야 한다.

가시성 조항이 없으면 에이전트가 목표에서 0.9 m 떨어진 벽 반대편에 서서 성공할 수 있다. 지표는
성공률과 **SPL**이고, 최단 경로는 에이전트의 *출발점*에 가장 가까운 인스턴스까지로 잰다.

> [!warning] 정의하는 두 문서 모두 심사를 거치지 않았다
> SPL은 *On Evaluation of Embodied Navigation Agents*(2018)에서 도입되었고, 그 문서는 스스로를
> 워킹 그룹 보고서라고 서술한다. 과제 정의는 *ObjectNav Revisited*(2020)에서 온다. **둘 다 심사를
> 거친 적이 없고**, 그 둘이 문헌 전체가 보고하는 지표를 정의한다. 인용할 때 소리 내어 말할
> 가치가 있다.

> [!example] 계산 예제 · Worked example
> **SPL 0.47이 실제로 하는 말.** 경로 길이로 가중한 성공률(Anderson 외 2018)은
> $\text{SPL} = \frac{1}{N}\sum_i S_i \frac{\ell_i}{\max(p_i, \ell_i)}$이다. $S_i$는 성공 여부,
> $\ell_i$는 최단 경로, $p_i$는 실제로 걸은 경로다. 에피소드 셋:
>
> | 에피소드 | 성공 | 최단 $\ell$ | 실제 $p$ | 항 |
> |---|---|---|---|---|
> | 1 | O | 10 m | 10 m | $1 \times 10/10 = 1.00$ |
> | 2 | O | 10 m | 25 m | $1 \times 10/25 = 0.40$ |
> | 3 | X | 10 m | 8 m | $0$ |
>
> $\text{SPL} = (1.00 + 0.40 + 0)/3 = \mathbf{0.47}$이고, 성공률은 $2/3 = 0.67$이다.
>
> **여기서 얻는 독법.** *매번* 성공하지만 늘 최단 경로의 두 배를 걷는 에이전트는
> $1 \times 10/20 = 0.50$을 받는다. 즉 0.47은 헤매는 거의 완벽한 내비게이터와도, 직선으로
> 걷는 47%짜리 내비게이터와도 똑같이 들어맞는다. SPL만으로는 둘을 구분할 수 없다. 성공률
> 없이 보고된 SPL이 해석 불가능한 이유이자, 이 분야가 이제 둘을 함께 요구하는 이유다. SPL만
> 보이면서 효율 개선을 주장하는 논문이라면, 성공률이 움직이기는 했는지부터 확인하라.

### 3. 방법의 궤적, 세 수

**1수 — 모듈형 의미 지도.** Active Neural SLAM이 골격을 세웠다: 학습된 SLAM, 장기 목표를 고르는
전역 정책, 해석적 계획기, 지역 정책. 그 주장은 계층 구조와 고전 계획이 샘플 복잡도에서 종단간
RL을 이긴다는 것이다. **SemExp**가 그 골격에 의미 지도를 넣고, 학습된 전역 정책이 그 위에서
장기 탐색 목표를 고르게 했다. 2020년 챌린지를 우승했고 그 아키텍처가 여전히 중추다.

**2수 — 학습된 채점기를 사전학습 VLM으로 갈고, 아무것도 학습하지 않기.** **VLFM**은 점유 지도를
만들고 프런티어를 뽑은 뒤, 각 프런티어를 **목표 텍스트와의 시각-언어 유사도**로 채점해 다음에
어디를 탐색할지 고른다. ObjectNav 학습 데이터가 하나도 없고, 실제 Spot에 배치되었다. **ESC**는
같은 일을 LLM 상식 — 물체-방 동시 출현 — 을 프런티어 채점기 위의 소프트 논리 술어로 컴파일해
한다. 그리고 **CoWs**가, zero-shot 접근이 학습된 SOTA와 대등하거나 낫되 복잡한 언어를 활용하는
데는 약하다는 것을 확립했다.

**3수 — 모듈형 장치를 통째로 버리기.** §5를 보라.

> [!note] CoWs는 진짜 제목으로 인용하라
> 논문은 *"CoWs on Pasture: Baselines and Benchmarks for Language-Driven Zero-Shot Object
> Navigation"* 이다. "CLIP on Wheels"는 *방법* 이름이다. 2차 출처가 어김없이 잘못 인용한다.

### 4. 모든 것을 재구성하는 비판

Gervet 등이 고전·모듈형 학습·종단간 접근을 **실제 가정 여섯 곳**의 실기계에서 시험했다:

| 접근 | 결과 |
|---|---|
| **모듈형 학습** | **실세계 성공률 90%** |
| **종단간 학습** | **시뮬레이션 77% → 실세계 23%** |

부하를 지는 결론은 격차 자체가 아니라 그 설명이다: 시뮬레이터가 평가 벤치마크로서 실패하는
이유가 **둘**이라는 것 — 시각적 sim-to-real 격차, 그리고 **어긋난 실패 패턴**. 시뮬레이션과
현실이 *다른 방식으로* 실패하므로 **시뮬레이션 순위가 실세계 순위를 보존하지 않는다.** 재는
대상이 나아지지 않은 채로 리더보드를 오를 수 있다.

### 5. VLN, 그리고 벤치마크가 부정행위였음을 인정한 논문

**R2R**이 과제와 Matterport3D 시뮬레이터를 만들었다: 실제 건물에서 자연어 경로 지시를 따르기.
그러나 R2R은 **이산적**이다 — 에이전트가 미리 만든 내비게이션 그래프의 노드 사이를 순간이동한다.
**RxR**이 다국어 지시와 자세에 대한 단어 수준 시간 정렬을 더하고, R2R의 경로 편향(R2R 경로가
전부 최단 경로여서 에이전트가 부정행위를 할 수 있다)을 교정했다.

**VLN-CE가 이 문헌에서 가장 중대한 논문이다.** R2R을 **저수준 연속 행동**과 함께 Habitat으로
옮겨, 세 가정을 한 번에 제거한다 — 알려진 위상, 오라클 내비게이션, 완벽한 위치추정 — 그리고
성능이 급격히 떨어진다. 분야가 반박 없이 받아들인 결론: **이전의 내비 그래프 결과들은 자기
단순화 가정에 의해 부풀려져 있었다.**

그 경험적 짝이 Anderson 등의 sim-to-real 연구다: **시뮬레이션 55.9% → 사전 지도가 있는 실제
46.8% → 사전 지도 없는 실제 22.5%.**

트랜스포머 시대 — **HAMT**(지난 파노라마 전체 이력에 대한 계층적 ViT, 긴 궤적에서 가장 크게
이득)와 **DUET**(즉석에서 만드는 위상 지도, 되돌아가기를 포함한 거친 전역 계획과 미세 지역
인코딩의 결합) — 는 이산 패러다임의 정점이고, 그렇게 읽을 가치가 있다.

그다음 **NaVid**가 그것을 깼다: **단안 RGB 비디오만 — 지도도, 오도메트리도, 깊이도 없이** — 받아
행동을 직접 내는 비디오 VLM. HAMT와 DUET이 의존하던 모듈형 장치 전체를 버렸고, 2025~26년의 모든
결과가 그 후손이다.

> [!important] 정확히 말하라
> **폐기된 것은 내비 그래프 행동 공간이지 R2R이 아니다.** VLN-CE가 *바로* R2R과 RxR을 Habitat으로
> 옮긴 것이므로, 지시 코퍼스는 분야 전체가 딛고 선 언어적 기반으로 남아 있다. "R2R은 낡았다"는
> 틀렸고, "내비 그래프 정식화가 폐기되었다"가 맞다.

### 6. 두 갈래가 합쳐졌고, 벤치마크는 해체되었다

<svg viewBox="0 0 560 254" style="max-width:100%;height:auto" role="img" aria-label="2018년의 두 별개 내비게이션 갈래가 2025년까지 하나의 비디오 VLA로 수렴하고, 그동안 챌린지들이 끝난다">
  <g stroke="currentColor" stroke-width="1.1" fill="none" opacity="0.55">
    <line x1="34" y1="212" x2="528" y2="212"/>
  </g>
  <g stroke="currentColor" stroke-width="0.9" opacity="0.5">
    <line x1="60" y1="212" x2="60" y2="218"/><line x1="180" y1="212" x2="180" y2="218"/><line x1="300" y1="212" x2="300" y2="218"/><line x1="380" y1="212" x2="380" y2="218"/><line x1="460" y1="212" x2="460" y2="218"/>
  </g>
  <g fill="currentColor">
    <rect x="34" y="52" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="34" y="112" width="250" height="32" rx="3" fill-opacity="0.12"/>
    <rect x="392" y="76" width="136" height="46" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="34" y="52" width="250" height="32" rx="3"/><rect x="34" y="112" width="250" height="32" rx="3"/><rect x="392" y="76" width="136" height="46" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.5" fill="none" opacity="0.8" marker-end="url(#arSk)">
    <path d="M 290 68 L 340 68 L 340 92 L 386 92"/>
    <path d="M 290 128 L 340 128 L 340 106 L 386 106"/>
  </g>
  <defs><marker id="arSk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10.5" fill="currentColor">
    <text x="46" y="72">ObjectNav &#8212; 지명된 물체 찾기</text>
    <text x="46" y="132">VLN &#8212; 경로 지시 따르기</text>
    <text x="460" y="95" text-anchor="middle" font-size="11">하나의 비디오 VLA</text>
    <text x="460" y="110" text-anchor="middle" font-size="9">내비 + 물체 탐색 + EQA + 사람 추종</text>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.85">
    <text x="60" y="230" text-anchor="middle">2018</text><text x="180" y="230" text-anchor="middle">2020</text><text x="300" y="230" text-anchor="middle">2023</text><text x="380" y="230" text-anchor="middle">2024</text><text x="460" y="230" text-anchor="middle">2025</text>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.7" stroke-dasharray="4 3">
    <line x1="300" y1="160" x2="300" y2="206"/>
  </g>
  <g font-size="9.5" fill="currentColor" opacity="0.9">
    <text x="306" y="170">2023년 10월: Habitat 챌린지 저장소 보관</text>
    <text x="306" y="184">CVPR 2026: 내비게이션 챌린지 0개</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="34" y="250">내비게이션은 풀린 것이 아니라 흡수되었다 &#8212; 위로는 VLA로, 옆으로는 모바일 조작으로.</text>
  </g>
</svg>

**Uni-NaVid**가 그 합류다: **VLN, 물체 탐색, embodied QA, 사람 추종**에 걸친 360만 샘플로 학습한
하나의 비디오 VLA가 그 전부에서 SOTA를 5 Hz로 보고한다. 2020년에 저것들은 별도의 시뮬레이터와
별도의 챌린지를 가진 별도의 공동체였다.

동시에 제도적 발판이 내려앉았다. Habitat 챌린지 저장소가 **2023년 10월 읽기 전용으로 보관**
되었고 2023년판이 마지막이었다. CVPR 2025 Embodied AI 워크숍은 챌린지 넷을 돌렸고 **그중 ObjectNav는
없었다.** CVPR 2026은 셋을 돌렸고 **셋 다 매니퓰레이션이었다.**

에너지가 간 곳은 측정 가능하다: **open-vocabulary 모바일 조작**이다. HomeRobot이 실세계 성공률
약 20%를 보고하고, 챌린지 사후 보고가 기준선 **0.8%**, 우승 **10.8%** 를 기록한다 — 13배
개선인데도 과제는 여전히 약 90% 미해결이다. 그것이 오를 가치가 있는 리더보드이고, 포화된 6범주
ObjectNav는 아니었다.

실제로 나온 후속들은 구조적으로 open-vocabulary다: **HM3D-OVON**(379범주, 자유 형식 언어 목표)과
**GOAT-Bench**(범주·서술·이미지 중 무엇으로든 주어지는 목표, 기억을 요구하는 긴 지평).

### 7. 나머지 절반: 언어로 질의할 수 있는 지도

나란히 굴러왔고, 이제는 ObjectNav 리더보드보다 중대하다:

- **VLMaps**는 로봇이 스스로 만든 3D 재구성에 시각-언어 특징을 융합해 **공간적** 언어 목표 —
  "소파와 TV 사이" — 를 LLM 코드 생성으로 가능하게 하고, embodiment를 가로질러 공유 가능한 로봇별
  장애물 지도를 내놓는다.
- **ConceptFusion**의 독특한 주장은 *멀티모달 질의*다: 언어·이미지·오디오·클릭이 모두 같은 지도를
  색인한다.
- **ConceptGraphs**가 조밀한 특징 필드를 **물체 중심 그래프**로 대체했다 — 다시점 융합으로 노드를,
  LLM 추론으로 간선을. 더 싸고 조합 가능해서 기본 중추가 되었다.
- **Clio**가 더 나은 질문을 한다: granularity는 고정 임계값이 아니라 **정보 병목을 통해 과제
  목록에서 유도된다.** 같은 장면이 내비게이션에는 거친 지도를, 조작에는 세밀한 지도를 필요로 하고,
  그것을 과제가 정해야 한다.
- **Hydra**가 나머지가 가정하는 실시간 시스템 기반이고, **Khronos**가 그것을 동적 환경의 시공간
  매핑으로 확장한다.

2025~26년의 구조적 사실 둘: **가우시안 스플래팅이 NeRF를 의미 기반 substrate에서 밀어냈고**, 그래서
LERF식 방사 필드는 레거시다. 그리고 **로보틱스 쪽에서는 장면 그래프가 이겼고 스플랫을 흡수했다** —
그래프가 질의 가능한 인터페이스이고 스플랫이 그 밑의 기하다.

> [!important] 위키의 인식 노트들이 향하던 곳이 여기다
> [[01-canonical-papers/notes/2-computer-vision/sam|SAM]],
> [[01-canonical-papers/notes/3-vlm/clip|CLIP]],
> [[01-canonical-papers/notes/2-computer-vision/dino|DINO]],
> [[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3D Gaussian Splatting]],
> [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]가 *재료*다. 이 절이 그것들로 만들어지는
> 것이고 — 지도야말로 어떤 제어기보다 먼저 내비게이션과 매니퓰레이션이 만나는 곳이다.

### 8. 이 분야의 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 내비 그래프인가 연속인가? | 내비 그래프 수치는 VLN-CE 수치와 비교 불가다 |
| 시뮬레이션인가 실기계인가? | 시뮬 순위는 실제 순위를 보존하지 않는다 |
| ObjectNav 학습 데이터를 썼는가? | 강한 현대 결과들은 아무것도 학습하지 않는다 |
| 어느 HM3D/MP3D 분할이며 범주가 몇 개인가? | 6범주 ObjectNav는 포화, 379범주는 아니다 |
| 언어가 실제로 부하를 지고 있는가? | 재구성 문장에 대한 민감성이 표준적 실패다 |
| SPL인가 맨 성공률인가? | 성공률만으로는 비효율적 배회가 보상된다 |

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 가시성 조항을 포함한 ObjectNav 성공 기준과 그것이 존재하는 이유를 말한다.
- [ ] VLN-CE가 무엇을 제거했고 무엇을 보였는지 설명한다.
- [ ] 모듈형 대 종단간의 실세계 수치와 그 이유를 댄다.
- [ ] Habitat 챌린지에 무슨 일이 있었고 분야가 어디로 갔는지 말한다.
- [ ] 기본 중추가 된 지도 표현과, Clio가 던진 더 나은 질문을 댄다.

### 스스로 점검

1. ObjectNav 성공 기준이 왜 두 부분인가?
2. 2026년 논문이 내비 그래프 R2R에서 68% 성공을 보고한다. 무엇을 결론짓겠는가?
3. 어떤 방법이 시뮬레이션 내비게이션 벤치마크에서 좋은 점수를 낸다. Gervet 등에 따르면 무엇을
   추론하면 *안 되는가*?
4. ObjectNav 챌린지가 중단되었다. 물체 목표 내비게이션이 풀렸다는 뜻인가?
5. 방으로 이동하는 것과 그 안의 무언가를 파지하는 것을 모두 지원하는 지도가 필요하다. 현재 문헌은
   무엇을 시사하는가?

> [!tip]- 정답 · Answers
> 1. 근접만으로는 과제가 아니기 때문이다. 오라클 가시성 조항이 없으면 에이전트가 목표에서 0.9 m 떨어진, 그 사이에 벽이 있는 곳에 멈춰서 정답 처리를 받을 수 있고, 그것은 *물체*를 찾은 것이 아니라 *좌표*에 도달한 것을 보상하는 셈이다. 두 부분 기준이 ObjectNav를 변장한 계량 내비게이션 문제가 아니라 인식 문제로 만든다.
> 2. 그 숫자가 현재의 무엇과도 비교 불가이며, 논문이 분야가 폐기한 정식화에 대해 보고하고 있다는 것. VLN-CE가 내비 그래프 결과는 알려진 위상·오라클 내비게이션·완벽한 위치추정으로 부풀려져 있음을 보였고, 2024~26년의 모든 결과는 R2R-CE로 보고한다. R2R의 *지시*는 여전히 기반이다 — 낡은 것은 순간이동하는 행동 공간이다.
> 3. 실세계 순위가 따라올 것이라는 점. 그들의 발견은 성능이 떨어진다는 것만이 아니라 **시뮬레이션과 현실이 다른 방식으로 실패한다**는 것이고, 그래서 방법 사이의 순서가 보존되지 않는다. 종단간이 시뮬 77% → 실제 23%인 동안 모듈형 학습은 실제 90%에 도달했다 — 균일한 할인이 아니라 역전이다. 시뮬 결과는 시뮬에 관한 증거다.
> 4. 아니다 — 그 벤치마크가, 시뮬레이션의 6범주에서, 잴 가치가 있는 것을 재기를 멈췄다는 뜻이다. 과제는 open-vocabulary 형태(HM3D-OVON의 379범주, GOAT-Bench의 멀티모달 평생 목표)로 옮겨 갔고, 물체 탐색·질의응답과 나란히 내비게이션을 하는 비디오 VLA로 흡수되었다. 한편 open-vocabulary 모바일 조작 안의 실세계 판본은 10~20%대에 있다.
> 5. Granularity가 **고정이 아니라 과제에서 유도되어야 한다**는 것 — Clio의 정보 병목 정식화가 존재하는 이유가 정확히, 같은 장면에 대해 내비게이션은 거친 지도를 원하고 조작은 세밀한 지도를 원하기 때문이다. 아키텍처로는, 어떤 기하 substrate를 쓰든 그 위에 물체 중심 장면 그래프(ConceptGraphs 계보)를 질의 가능한 인터페이스로 세우고, 상세도는 과제 목록이 정하게 하라.

### 출처

**정의와 평가** — P. Anderson, A. Chang, D. S. Chaplot, et al., "On Evaluation of Embodied Navigation Agents," [arXiv:1807.06757](https://arxiv.org/abs/1807.06757), 2018 (SPL 도입, **미심사**); D. Batra, A. Gokaslan, A. Kembhavi, et al., "ObjectNav Revisited," [arXiv:2006.13171](https://arxiv.org/abs/2006.13171), 2020 (**미심사**).

**시뮬레이터와 데이터셋** — Habitat (ICCV 2019, [arXiv:1904.01201](https://arxiv.org/abs/1904.01201)); Habitat 2.0 (NeurIPS 2021); Habitat 3.0 (ICLR 2024); HM3D (NeurIPS 2021 D&B); HM3D-Semantics (CVPR 2023); HM3D-OVON ([arXiv:2409.14296](https://arxiv.org/abs/2409.14296)); GOAT-Bench ([arXiv:2404.06609](https://arxiv.org/abs/2404.06609)).

**ObjectNav 방법** — Active Neural SLAM (ICLR 2020, [arXiv:2004.05155](https://arxiv.org/abs/2004.05155)); SemExp ([arXiv:2007.00643](https://arxiv.org/abs/2007.00643)); "CoWs on Pasture" (CVPR 2023, [arXiv:2203.10421](https://arxiv.org/abs/2203.10421)); VLFM (ICRA 2024, [arXiv:2312.03275](https://arxiv.org/abs/2312.03275)); ESC (ICML 2023, [arXiv:2301.13166](https://arxiv.org/abs/2301.13166)).

**비판** — T. Gervet, S. Chintala, D. Batra, J. Malik, D. S. Chaplot, "Navigating to Objects in the Real World," *Science Robotics*, 2023 ([arXiv:2212.00922](https://arxiv.org/abs/2212.00922)).

**VLN** — R2R (CVPR 2018 Spotlight, [arXiv:1711.07280](https://arxiv.org/abs/1711.07280)); RxR (EMNLP 2020, [arXiv:2010.07954](https://arxiv.org/abs/2010.07954)); VLN-CE (ECCV 2020, [arXiv:2004.02857](https://arxiv.org/abs/2004.02857)); HAMT (NeurIPS 2021, [arXiv:2110.13309](https://arxiv.org/abs/2110.13309)); DUET (CVPR 2022, [arXiv:2202.11742](https://arxiv.org/abs/2202.11742)); sim-to-real: P. Anderson et al., CoRL 2020 ([arXiv:2011.03807](https://arxiv.org/abs/2011.03807)); NaVid (RSS 2024, [arXiv:2402.15852](https://arxiv.org/abs/2402.15852)); Uni-NaVid (RSS 2025, [arXiv:2412.06224](https://arxiv.org/abs/2412.06224)); NaVILA (RSS 2025, [arXiv:2412.04453](https://arxiv.org/abs/2412.04453)).

**언어로 질의하는 지도** — Hydra (RSS 2022, [arXiv:2201.13360](https://arxiv.org/abs/2201.13360)); Khronos (RSS 2024); CLIP-Fields (RSS 2023); ConceptFusion (RSS 2023, [arXiv:2302.07241](https://arxiv.org/abs/2302.07241)); VLMaps (ICRA 2023, [arXiv:2210.05714](https://arxiv.org/abs/2210.05714)); ConceptGraphs (ICRA 2024, [arXiv:2309.16650](https://arxiv.org/abs/2309.16650)); HOV-SG (RSS 2024); Clio (*IEEE RA-L* 9(10):8921–8928, 2024, [arXiv:2404.13696](https://arxiv.org/abs/2404.13696)).

**에너지가 간 곳** — HomeRobot (CoRL 2023, [arXiv:2306.11565](https://arxiv.org/abs/2306.11565)); OVMM 챌린지 사후 보고 ([arXiv:2407.06939](https://arxiv.org/abs/2407.06939)).

**이 위키 안에서**

- **논문 노트** — [[01-canonical-papers/notes/9-navigation/semexp|SemExp]] · [[01-canonical-papers/notes/9-navigation/vlfm|VLFM]] · [[01-canonical-papers/notes/9-navigation/vln-ce|VLN-CE]] · [[01-canonical-papers/notes/9-navigation/navid|NaVid]] · [[01-canonical-papers/notes/9-navigation/uni-navid|Uni-NaVid]] · [[01-canonical-papers/notes/9-navigation/conceptgraphs|ConceptGraphs]] · [[01-canonical-papers/notes/9-navigation/clio|Clio]] · [[01-canonical-papers/notes/9-navigation/vint-nomad|ViNT / NoMaD]] · [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등 2023]]
- [[04-robotics/navigation-mobile-manipulation|16. 내비게이션과 모바일 조작]] — 같은 문제의 기하학적 절반
- [[04-robotics/traversability-off-road|17. Traversability와 오프로드 자율성]] — 실외 대응물
- [[01-canonical-papers/notes/3-vlm/clip|CLIP]]과 [[01-canonical-papers/notes/2-computer-vision/sam|SAM]] — §7이 조립하는 재료들
