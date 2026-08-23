---
title: 7. Simulators, Benchmarks & Datasets
tags: [research-practice, guide, tooling]
study-depth: Working
wiki-support: Working
depth-goal: "Choose a simulator, benchmark, or dataset for a stated experiment, and know what each one cannot give you."
mastery-when: "This is operational knowledge — keep it current rather than deep; the field replaces these tools faster than it replaces its ideas."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to pick the instrument for an experiment, and to read someone else's
> tooling section for what it quietly rules out.
> **Working** — 실험에 쓸 도구를 고르고, 남의 논문의 도구 절에서 그것이 조용히 배제하는 것을
> 읽어낼 만큼.

> [!warning] This page goes stale faster than any other · 이 페이지가 가장 빨리 낡는다
> Versions, licenses and maintenance status change constantly, and stale tooling advice
> wastes weeks. Everything here was checked against **official sources** on **2026-08-22**,
> and every scale figure is quoted from the paper's own **abstract** unless labelled
> otherwise. Three of the entries below changed status within the last two years. Re-check
> the official page before acting.
> 버전·라이선스·유지보수 상태가 끊임없이 바뀌고, 낡은 도구 조언은 몇 주를 낭비시킨다. 여기
> 있는 것은 전부 **2026-08-22**에 **공식 출처**로 확인했고, 모든 규모 수치는 따로 표시하지
> 않는 한 논문 **자신의 초록**에서 인용한 것이다. 아래 항목 중 셋은 지난 2년 안에 상태가
> 바뀌었다. 행동에 옮기기 전에 공식 페이지를 다시 확인하라.

## English

### 1. What this page is for

Three questions get asked at the start of every project and answered badly: *which
simulator, which benchmark, which data?* They are usually answered by what a labmate used.
This page answers them by what each tool can and cannot represent — which for contact-rich
construction manipulation turns out to be the deciding question.

The most useful content here is not the recommendations. It is the **absences**: things that
sound like they should exist and do not. Each one is a citable gap.

### 2. Simulators — general purpose

| Simulator | Maintainer | License | Canonical paper | The one thing it is best at |
|---|---|---|---|---|
| **MuJoCo** | Google DeepMind | Apache-2.0 | Todorov, Erez & Tassa, IROS 2012 | fast, stable articulated dynamics; analytically invertible |
| **Isaac Sim** / **Isaac Lab** | NVIDIA | see caveat below / BSD-3 | none / Orbit, RA-L 2023 | thousands of GPU-parallel envs, RTX-photoreal sensors |
| **PyBullet** | community | Zlib | **none** (cite the `@misc`) | easy, mature, CPU-friendly |
| **Gazebo** (`gz`) | Open Source Robotics Alliance | Apache-2.0 | Koenig & Howard, IROS 2004 | ROS 2 integration, sensors, headless CI |
| **Drake** | MIT origin, led by Toyota Research Institute | BSD-3 | **none** (cite the `@misc`) | **hydroelastic contact** — a contact patch with a pressure distribution |
| **SAPIEN** | UCSD SU Lab / Hillbot | see caveat | Xiang et al., CVPR 2020 | part-level articulated objects, via PartNet-Mobility |

Four things in that table need saying out loud, because each is a way to be wrong in print.

> [!warning] Four status traps
> - **Isaac Gym is deprecated.** NVIDIA's own page says: "This is legacy software. Developers
>   may download and continue to use it, but it is no longer supported." `IsaacGymEnvs` and
>   `OmniIsaacGymEnvs` were both archived read-only in April 2026. Use Isaac Lab.
> - **"Isaac Sim is Apache 2.0" is not safe to write unqualified.** The same LICENSE file
>   states that building or using it requires additional components — the Omniverse Kit SDK
>   and 3D assets — governed by a separate NVIDIA agreement.
> - **Gazebo Classic reached end of life on 2025-01-29** and its repo was archived. "Ignition"
>   should appear only as history: the rename to `gz` happened because of, in Open Robotics'
>   words, "a trademark obstacle regarding our use of the name 'Ignition'."
> - **SAPIEN's license is genuinely ambiguous**: the repo LICENSE says Apache-2.0, the PyPI
>   metadata says MIT, and GitHub's detector says NOASSERTION. State the ambiguity rather
>   than picking one.

**PyBullet, Drake, Isaac Sim and Genesis have no peer-reviewed paper.** All four officially
direct you to a `@misc` or a URL. That is fine — but write "we used Drake [software
citation]", not a fabricated venue.

### 3. The axis that actually matters: how contact is modelled

For this program the interesting difference between simulators is not speed. It is what
each one *means* by a contact.

- **MuJoCo** solves a soft convex optimisation with elliptic or pyramidal friction cones,
  and its documentation is explicit that constraint violations are permitted by design — it
  is not a complementarity solver. That is what makes it fast and stable, and it is also why
  a MuJoCo contact force is not the force a load cell would read.
- **Drake's hydroelastic contact** goes the other way: rigid bodies "penetrate slightly, as
  if the rigid body had a slightly deformable layer", producing an approximate contact
  *patch* and *pressure distribution* rather than a point force, with temporal coherence
  across non-convex geometry. Its own documented limits are equally clear — it cannot
  produce a contact surface between two rigid hydroelastic geometries, and it "cannot model
  true deformations given the model does not introduce state", so tangential compliance and
  short-timescale waves are absent.
- **PhysX**, under Isaac, is a game-engine lineage tuned for throughput.

MuJoCo 3.x has been moving toward contact-rich work in a way worth tracking: 3.0 introduced
Flex deformables, 3.3.0 made native convex collision the default, and **3.3.5 added native
SDF support plus a contact sensor and a tactile sensor** — the latter "measuring the
penetration depth between two objects at given points". For a project about
[[04-robotics/tactile-visuotactile|tactile manipulation]], that is a material change.

### 4. Terrain and earthmoving

A separate world, with separate tools, and the only part of this domain where simulation is
genuinely mature.

- **AGX Dynamics** (Algoryx) is the strongest documented option. Its `agxTerrain` module
  models a 3D voxel grid carrying mass, compaction and soil type under a height-field
  surface; a digging tool creates failure zones that convert solid terrain mass into dynamic
  mass, parameterised by **angle of internal friction and cohesion**, with solid cells
  becoming 6-DoF particles and a mass-aggregate body supplying inertial resistance through
  the failure plane. Penetration resistance and digging resistance are separate. It models
  compaction, swell factor, and angle of repose.
  - Uniquely, it has **both** vendor parameter-level documentation **and** a peer-reviewed
    open-access physics paper: Servin, Berglund and Nystedt, *A multiscale model of terrain
    dynamics for real-time earthmoving simulation*, 2021. Algoryx states the model's digging
    resistance and soil displacements "agree with the reference model up to 10-25%, and run
    more than three orders of magnitude faster".
  - Commercial, yearly subscription per seat, **price on request**. Academic single and group
    licences exist, strictly non-commercial.
- **Vortex Studio** (CM Labs) has documented deformable terrain, soil materials and soil
  particles, and is commercially proven in operator training. Two problems for research:
  no retrievable vendor theory document for its soil model — the best descriptions are
  third-party — and, in CM Labs' own words, **"An academic License is not offered anymore."**
- **Project Chrono** is the best open option (BSD-3) and the only one offering a *ladder* of
  soil fidelity in one framework: **SCM** (Bekker-Wong semi-empirical), granular **DEM**,
  **FEA**, and **CRM**, an SPH continuum model whose paper explicitly covers "digging,
  grading" and validates against a real digging robot. **Chrono DEM-Engine** is the
  high-fidelity reference to validate against rather than to run policies in.

> [!note] The honest recommendation
> **AGX if you can buy it, Chrono::CRM if you need open and citable**, with DEM-Engine as the
> reference model. And carry the caveat: both leading real-time soil models are validated
> only to roughly **10-25%** of a DEM reference. Quantitative digging forces out of any
> real-time simulator are approximate, and a paper that reports them to three significant
> figures is over-claiming.

### 5. Deformable construction materials — a gap, stated plainly

**No simulator has a documented model for construction materials as such.** Not drywall, not
rebar cages, not building membranes. What exists is generic primitives you would have to
parameterise and validate yourself:

| Material | Nearest primitive | State of the art |
|---|---|---|
| Cable, rope, hose | AGX `agxCable` | **solved at industrial grade** — lumped rigid bodies with all six DOF, so bending, twisting and stretching are tracked, plus plasticity. Documented limits: cables must be circular and homogeneous, fixed resolution |
| Rebar mesh, cages | networks of connected rods | **no dedicated model.** Nearest is DisMech (RA-L 2024), which handles arbitrary connections between rods |
| Membranes, sheets | thin shells | Chrono's `ChElementShellReissner` is the most physically appropriate documented formulation, and BSD-3 — but **no construction-material validation exists anywhere** |
| **Drywall panel** | — | **nothing.** A stiff, brittle, heavy panel that *fractures* rather than deforming elastically is not modelled by anything verifiable |

One more limit worth knowing before choosing Isaac for deformable work: its documentation
states that **"Particles and deformable body do not support contact reports"**, along with
no static friction and no friction combine mode. You cannot read contact forces off a
deformable — which is the measurement a contact-rich manipulation study exists to make.

> [!warning] Genesis — read the history before citing it
> Genesis (now **Genesis World**, developed under the company Genesis AI) offers unusually
> broad multi-physics under one API. Its December 2024 README claimed, verbatim, "over 43
> million FPS when simulating a Franka robotic arm with a single RTX 4090 (430,000 times
> faster than real-time)". A MuJoCo maintainer questioned the comparison publicly; a
> ManiSkill developer filed an issue arguing the benchmark used the fastest physics setting,
> took one action followed by 999 no-op steps, and disabled self-collisions. The team then
> published a corrected benchmark whose script header says it is "mostly identical to" the
> critic's, and the issue was closed by the critic saying the new numbers "look more accurate
> given the right context" — while noting he had not re-verified them. **The 43-million-FPS
> claim was removed from the README in May 2026 as part of a rewrite, with no labelled
> retraction.** There is still no peer-reviewed paper; the official citation block offers a
> company blog post and a repo URL. None of this means the software is bad. It means you
> cannot cite it as a validated result, and you should say "software" when you cite it.

### 6. Benchmarks

| Benchmark | Venue | Sim / real | What it measures | Abstract-stated scale |
|---|---|---|---|---|
| **RLBench** | RA-L 2020 | simulation | task success, few-shot generalization | "100 completely unique, hand-designed tasks" |
| **Meta-World** | CoRL 2019 | simulation | multi-task and meta-RL transfer to held-out tasks | "50 distinct robotic manipulation tasks" |
| **ManiSkill 3** | RSS 2025 | simulation | throughput and task coverage | "up to 30,000+ FPS"; "12 distinct domains" |
| **CALVIN** | RA-L 2022 | simulation | long-horizon language-conditioned, zero-shot | **no numbers in the abstract** |
| **LIBERO** | NeurIPS 2023 D&B | simulation | **lifelong** transfer — forward, backward, task ordering | "four task suites (130 tasks in total)" |
| **FurnitureBench** | RSS 2023 | **both** | real-world long-horizon contact-rich **assembly** | "200+ hours of pre-collected data (5000+ demonstrations)" |
| **RoboCasa** | RSS 2024 | simulation | data-scaling behaviour for imitation learning | "over 150 object categories"; "100 tasks" |
| **NIST Assembly Task Boards** | RA-L 2020 | **real only** | time-to-complete against **tabulated** human handling times | "three task board artifacts" |
| **RAMP** | RA-L 2024 | **both** | assembly planning *and* execution, three difficulty classes | **no scale figures in the abstract** |

**The assembly line of descent is the relevant one here**: NIST task boards give physical
artifacts and a human-referenced scoring protocol (peg insertion, gear meshing, connectors,
nut threading, and in later boards cable routing and wire harnesses); FurnitureBench adds a
real-robot long-horizon benchmark with a simulator alongside; and **RAMP** is the only one
framed on construction — its Section I says the domain is *offsite* construction and that
"the assembly of beams into frames remains a manual process".

> [!important] Cite RAMP carefully
> RAMP's abstract says only "real-world industrial assembly tasks" — **the word
> construction does not appear in it**. The offsite-construction framing is in the paper
> body. If you cite RAMP as a construction benchmark, cite the section, not the abstract.

**Two verified absences.** There is **no benchmark for on-site construction manipulation** —
nothing for bricklaying, drywall, rebar tying, façade installation or overhead work. What
exists is vendor throughput figures and one-off papers with bespoke evaluations: no shared
protocol, no shared artifacts, no leaderboard. And there is **no standardised benchmark or
test-pit protocol for excavation or earthmoving**. ISO 7546, ISO 6165, ISO 10968 and the SAE
MTC1 committee standardise *machines*, not autonomy performance. NASA's Lunabotics has
published rules and a rubric, but it is regolith-simulant, student-scoped, and the rules
change annually.

### 7. Datasets — and the modality that is missing

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="three bands of dataset capability, the third of which is empty">
  <g fill="currentColor">
    <rect x="24" y="42" width="512" height="48" rx="4" fill-opacity="0.07"/>
    <rect x="24" y="112" width="512" height="48" rx="4" fill-opacity="0.16"/>
    <rect x="40" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="205" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="370" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="40" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="205" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="370" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5">
    <rect x="24" y="42" width="512" height="48" rx="4"/><rect x="24" y="112" width="512" height="48" rx="4"/>
    <rect x="40" y="52" width="150" height="28" rx="3"/><rect x="205" y="52" width="150" height="28" rx="3"/><rect x="370" y="52" width="150" height="28" rx="3"/>
    <rect x="40" y="122" width="150" height="28" rx="3"/><rect x="205" y="122" width="150" height="28" rx="3"/><rect x="370" y="122" width="150" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <rect x="24" y="182" width="512" height="48" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" font-weight="600">
    <text x="24" y="36">vision + proprioception + language</text>
    <text x="24" y="106">&#8230; and a force / torque channel</text>
    <text x="24" y="176">&#8230; and on a construction task</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="115" y="66">Open X-Embodiment</text><text x="115" y="77" font-size="9">527 skills, 160,266 tasks</text>
    <text x="280" y="66">DROID</text><text x="280" y="77" font-size="9">65,000 trajectories</text>
    <text x="445" y="66">BridgeData V2</text><text x="445" y="77" font-size="9">53,896 trajectories</text>
    <text x="115" y="136">RH20T</text><text x="115" y="147" font-size="9">110,000+ sequences</text>
    <text x="280" y="136">FMB</text><text x="280" y="147" font-size="9">functional manipulation</text>
    <text x="445" y="136">REASSEMBLE</text><text x="445" y="147" font-size="9">4,551 demonstrations</text>
    <text x="280" y="212" font-size="11" opacity="0.9">no shared real-robot force data</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="250">Every count is quoted from that paper&#8217;s own abstract. The third band is empty, and that is the finding.</text>
  </g>
</svg>

The large manipulation corpora are **vision, proprioception and language**. That is not an
oversight in any one dataset — it is baked into the shared schema. The Open X-Embodiment
overview sheet's columns run *robot, episodes, file size, morphology, gripper, action space,
RGB cameras, depth cameras, wrist cameras, language annotations, collection method,
proprioception, scene type, control frequency* — **there is no force column and no tactile
column.** The dominant data format cannot represent the modality that
[[04-robotics/force-compliance-control|contact-rich manipulation]] most depends on.

The datasets that do break the pattern:

- **RH20T** is the important one: its abstract states "over 110,000 contact-rich robot
  manipulation sequences", and its project page documents a **6-DoF force/torque channel at
  100 Hz** alongside RGB, depth, joint torque and audio. Fingertip tactile exists but only
  on **one of seven robot configurations** — do not describe the whole corpus as tactile.
- **FMB** (IJRR) exposes end-effector force and torque fields explicitly.
- **REASSEMBLE** records event cameras, force-torque, microphones and multi-view RGB, on
  NIST task boards — "4,551 demonstrations, of which 4,035 were successful".
- Inside OXE, two constituent datasets do carry force — but be precise about where.
  `iamlab_cmu_pickup_insert` puts it **in the state vector** (20-dim: 7 joint angles, gripper,
  6 joint torques, 6 end-effector force). `stanford_kuka_multimodal` (the
  [[01-canonical-papers/notes/7-robotics/vision-and-touch|Vision-and-Touch]] data) does **not**:
  its state is 8-dim proprioception only, and force lives in a sibling observation field
  (`ee_forces_continuous`). Both are small, and the pooled schema surfaces neither.

> [!warning] Two citation traps in the big datasets
> **DROID** reports different numbers in different places: the arXiv abstract says 76k
> trajectories and 84 tasks; the RSS proceedings abstract says 65,000 and 86.
> **BridgeData V2** likewise: 60,096 trajectories on arXiv, 53,896 in the PMLR proceedings.
> Quote the number that matches the version you cite.

### 8. Construction and field data

Real construction-site datasets exist, and every one of them is a **perception** corpus:

- **ConSLAM** — and note there are **two distinct papers**, not one. The ECCV 2022 Workshops
  paper announces the dataset (images, LiDAR, IMU, terrestrial-laser ground truth, collected
  periodically). The *Journal of Computing in Civil Engineering* 2023 paper is the extended
  version and adds what makes it a benchmark: it quantifies the release at "five sequences",
  **recovers a ground-truth trajectory** by registering sequential LiDAR to the reference
  scans, and documents how to score SLAM error against it automatically. The authors' own
  repository labels the journal paper a "Free Journal Extension Paper" of the workshop one —
  it is one dataset published twice, not two datasets.
- **Hilti-Oxford** (RA-L 2023) and the **Hilti SLAM Challenge** series — LiDAR, cameras,
  IMU, with millimetre-accurate ground truth in construction environments, CC BY-NC-SA.
- **Rohbau3D** (*Scientific Data*, 2025) — "504 high-resolution LiDAR scans captured with a
  terrestrial laser scanner across 14 distinct construction sites", semantically labelled,
  **CC BY 4.0**. The best-licensed construction-site 3D corpus found.
- **ConRebSeg** — "14,805 RGB images with segmentation labels for autonomous robotic
  inspection of reinforced concrete defects", CC BY 4.0.
- **SODA**, **MOCS**, **ACID**, **CIS** — construction *image* datasets for detection and
  segmentation. Note two traps: ACID is sometimes miscited as an excavation dataset when it
  is images of machines with no soil, forces or trajectories — and there is an unrelated
  robotics paper also called ACID, on deformable-object manipulation.

For earthmoving specifically, the largest trajectory corpus is a corporate release —
excavator motion data with RGB, LiDAR-derived elevation maps and joint angles, under a
non-commercial licence, **with no paper behind it**. ETH's dry-stone dataset releases 1,100
digitised stone meshes with placement-viability labels under CC BY 4.0 — geometry and
labels, no trajectories, no force. **No public dataset of measured bucket forces or
soil-tool interaction exists.**

> [!important] The sharpest way to state the gap
> Two of these datasets were recorded **from real construction machines** — the Hilti SLAM
> Challenge 2023 used a drilling-robot platform drawing on the Jaibot, and **ETHcavation**
> was recorded from a Menzi Muck M545 walking excavator, releasing "502 hand-labeled sample
> images with panoptic annotations from construction sites". Neither releases an actuator,
> joint, hydraulic-pressure or force channel. **The machines were instrumented; the forces
> were not shared.**
>
> This is corroborated independently. *OpenConstruction*, a peer-reviewed catalogue of "51
> publicly available visual datasets that span the 2005-2024 period", organises them by a
> modality taxonomy of RGB, thermal, depth, LiDAR point cloud and synthetic — **there is no
> force, torque, tactile or contact row in it at all.**

> [!important] The gap this program sits in
> **No shared dataset of *real-robot, contact-rich* construction manipulation demonstrations
> exists.** Not at DROID scale, not at 10,000, not at 1,000. Be exact about what is and is
> not missing, because three papers in this wiki look like counter-examples and are not:
> [[01-canonical-papers/notes/8-construction/ext|ExT]] has 150,000 episodes per task, but
> they are generated in simulation and carry no real contact;
> [[01-canonical-papers/notes/8-construction/liang-lfd|Liang]] uses 3,000 virtual plus 85
> real demonstration *videos* and evaluates in Gazebo; and
> [[01-canonical-papers/notes/8-construction/kindle-jaibot|Kindle]] releases seven datasets,
> but they are accelerometer and pose recordings for deflection compensation, not
> manipulation demonstrations. What none of them provides is force-bearing real-robot
> demonstrations in a shared schema. The OXE `scene type` column takes values like *table top,
> kitchen, hallway, office, pantry, shelf, workshop, outdoors* — no construction, no site,
> no heavy machinery.
>
> The gap is three to four orders of magnitude, and it is a gap in **kind** as much as
> degree: no force channel, no tactile channel, no shared schema. That is what makes a
> curated dataset of a real construction task disproportionately valuable
> ([[06-research-practice/real-world-impact|6. §3]]), and it is why the demonstration-collection
> question in [[04-robotics/teleoperation-demonstration|12]] is a research question here
> rather than an engineering detail.

### 9. Choosing, for this program

| If you are doing | Use | Because |
|---|---|---|
| Contact-rich manipulation policy learning | MuJoCo, or Isaac Lab for scale | speed and stability; check whether you need real contact forces |
| Anything where the contact **force** is the result | Drake (hydroelastic), plus real hardware | a patch and a pressure distribution, not a point force |
| Excavation or terrain | AGX if funded, Chrono::CRM if not | the only documented soil models with citable physics |
| Assembly evaluation | NIST task boards → FurnitureBench → RAMP | artifacts, then real-robot, then construction-framed |
| Deformable construction materials | nothing exists — build and validate | say so in the paper; it is a contribution, not a gap in your work |
| Pretraining a manipulation policy | Open X-Embodiment, DROID, RH20T | and RH20T if you need the force channel |

### 10. Reading someone else's tooling section

| Question | What a vague answer hides |
|---|---|
| Which simulator, which version? | Isaac Gym results predate a deprecation; MuJoCo contact changed across 3.x |
| Were contact forces **simulated** or **measured**? | A simulator's contact force is a modelling choice, not a measurement |
| Sim-only, real-only, or both? | Benchmarks differ on this and the word "benchmark" hides it |
| Which dataset **version**, and which abstract's numbers? | DROID and BridgeData V2 both report two different counts |
| Does the data contain force or tactile at all? | Most does not, and most papers do not say so |
| Is the tool citable? | PyBullet, Drake, Isaac Sim and Genesis have no peer-reviewed paper |

### 11. Reading a learned-policy evaluation

The tooling section tells you what the numbers were produced *on*. This section is about the
numbers themselves — the part of a VLA, diffusion-policy or locomotion paper where a
percentage appears and has to be interpreted before it can be compared.

**What "success rate" leaves out.** A single percentage compresses four independent choices,
and two papers reporting 80% may agree on none of them:

| Choice | Why it moves the number |
|---|---|
| **How many trials** | 10 trials resolves nothing below ~10 percentage points. By the rule of three ($3/n$), zero failures in 10 trials is consistent with a true failure rate near **30%** — the exact bound is 26%, and the wiki uses $3/n$ throughout — so "10/10" is *not* evidence of reliability ([[06-research-practice/experimental-design-reproducibility\|3. Experimental Design §4]]) |
| **Initial-state distribution** | were object poses randomized, or reset to the same spot? A policy evaluated from a fixed start is being asked an easier question than one evaluated from a distribution |
| **What counts as done** | a time limit, a pose tolerance, a human judge. The tolerance is often unstated and is frequently the whole difference between two systems |
| **Whether resets and retries count** | a human straightening the object between trials is part of the system; if it is not counted, the reported autonomy is not the measured autonomy |

**Progress and partial credit.** Long-horizon and chained tasks are increasingly scored by
*how far the policy got* rather than whether it finished — stage completion, subtask counts,
or a normalized progress score. This is a reasonable response to binary success being too
coarse, and it introduces a specific failure of comparison: **a high progress score and a
zero success rate are compatible**, and they describe a policy that reliably starts a task and
reliably fails to finish it. The independent evaluation in
[[01-canonical-papers/notes/4-vla/pi0|π0]]'s claim box is exactly this shape. When a paper
leads with progress, look for the completion number; when it leads with completion, look for
whether partial credit was available to the baselines too.

**Seen versus unseen.** Nearly every generalization claim in this literature rests on a split,
and the split's *axis* is the claim: unseen object instances, unseen object categories, unseen
backgrounds, unseen lighting, unseen scenes, unseen embodiments. These are not equally hard
and papers rarely rank them. A method that generalizes across instances of a trained category
is making a much weaker claim than one that generalizes across categories — **read the split
definition before the number**, because the number is only meaningful relative to it.

**First-party versus independent numbers.** Robot-learning results are expensive to reproduce,
so most published comparisons are the authors' own reproductions of someone else's method.
That is not dishonest, and it is also not independent. Where a genuinely third-party
evaluation exists it is worth more than the headline, and the gap between the two is
frequently large — see [[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet et al.]]
(77% in simulation to 23% in six real homes) and π0's independent re-evaluation. **When you
cite a comparison, say whose evaluation it was.**

> [!warning] The three questions that settle most policy tables
> **1. How many trials, and from what initial-state distribution?** **2. Is this simulation,
> a lab testbed, or the deployment environment?** **3. Whose evaluation is it?** A results
> table that does not let you answer all three is reporting a demonstration, not a
> measurement — which is a legitimate contribution, but a different one, and it should not be
> compared against a table that does.

### After reading

- [ ] Name the four status traps in §2 and why each one produces a wrong sentence.
- [ ] Say what MuJoCo and Drake each mean by a contact, and when the difference matters.
- [ ] Give the honest recommendation for terrain simulation and the accuracy caveat attached.
- [ ] State what the OXE schema cannot represent, and why that matters here.
- [ ] Name the three verified absences on this page.

### Self-check

1. A paper reports contact forces from an Isaac Sim deformable-object experiment. What is
   the problem?
2. You need to cite the simulator you used. It is Drake. What do you write?
3. Someone quotes "43 million FPS" for Genesis. How do you respond?
4. Your related-work section says "DROID contains 76,000 trajectories". When is that wrong?
5. A reviewer asks why you did not evaluate on a standard construction manipulation
   benchmark. What is your answer?

> [!tip]- Answers
> 1. Isaac Sim's own documentation states that particles and deformable bodies **do not support contact reports** — so contact forces cannot be read off a deformable there at all. Either the forces came from somewhere else (a rigid proxy, an inferred estimate) and the paper should say so, or the number is not what it appears to be. Static friction and friction combine mode are also unsupported for deformables, which compounds it.
> 2. The software citation Drake itself provides — a `@misc` with the project name, the development team, and the URL. **There is no peer-reviewed Drake paper**, so inventing a venue would be a fabricated citation. If you used hydroelastic contact specifically, cite the contact-model papers the documentation points to (Castro et al.) alongside the software.
> 3. That the figure came from the December 2024 README, was publicly disputed on methodology — fastest physics setting, one action then 999 no-op steps, self-collisions disabled — that the team published a corrected benchmark adopting the critic's own harness, and that **the claim was removed from the README in May 2026 without a labelled retraction**. The current official materials make no such claim. It should not be quoted as a live number.
> 4. When you are citing the RSS proceedings version, whose abstract says **65,000** trajectories and 86 tasks. 76k/84 is the arXiv abstract's figure. Neither is wrong; quoting one against the other version's citation is. The same trap exists for BridgeData V2 — 60,096 on arXiv, 53,896 in PMLR.
> 5. That none exists, and say it plainly: there is no shared benchmark for on-site construction manipulation — no shared protocol, no shared artifacts, no leaderboard — and the nearest thing, RAMP, is framed on *offsite* construction. The defensible move is to state the absence, borrow the closest evaluation apparatus (NIST task boards for assembly scoring, or RAMP's protocol), and define your own protocol explicitly enough that someone else could rerun it — which is itself an artifact worth releasing.

### Sources

Checked against official sources on **2026-08-22**. Scale figures are from each paper's own
abstract unless marked otherwise; claims resting on absence mean the official pages were
checked and contained nothing.

**Simulators** — [MuJoCo](https://mujoco.readthedocs.io/) (Todorov, Erez & Tassa, IROS 2012, pp. 5026–5033, DOI 10.1109/IROS.2012.6386109); [Isaac Sim](https://developer.nvidia.com/isaac/sim) and [Isaac Lab](https://isaac-sim.github.io/IsaacLab/) (predecessor Orbit: Mittal et al., *RA-L* 8(6), 2023, DOI 10.1109/LRA.2023.3270034); [the Isaac Gym legacy notice](https://developer.nvidia.com/isaac-gym); [Bullet](https://github.com/bulletphysics/bullet3); [Gazebo](https://gazebosim.org/docs/latest/releases/) and the [Classic end-of-life notice](https://classic.gazebosim.org/) (Koenig & Howard, IROS 2004, pp. 2149–2154); [Drake](https://drake.mit.edu/) and its [hydroelastic contact guide](https://drake.mit.edu/doxygen_cxx/group__hydroelastic__user__guide.html); [SAPIEN](https://github.com/haosulab/SAPIEN) (Xiang et al., CVPR 2020, pp. 11094–11104); [Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world), [the benchmark issue](https://github.com/Genesis-Embodied-AI/genesis-world/issues/181) and [the MuJoCo discussion](https://github.com/google-deepmind/mujoco/discussions/2303).

**Terrain** — [agxTerrain user manual](https://www.algoryx.se/documentation/complete/agx/tags/latest/doc/UserManual/source/agxTerrain.html); M. Servin, T. Berglund, S. Nystedt, "A multiscale model of terrain dynamics for real-time earthmoving simulation," *Advanced Modeling and Simulation in Engineering Sciences* 8:11, 2021, DOI 10.1186/s40323-021-00196-3; [Vortex Studio licensing](https://vortexstudio.atlassian.net/wiki/spaces/VSD2511/pages/4607410452); [Project Chrono terrain models](https://api.projectchrono.org/vehicle_terrain.html) and Unjhawala et al., [arXiv:2507.05643](https://arxiv.org/abs/2507.05643) for CRM.

**Benchmarks** — RLBench ([arXiv:1909.12271](https://arxiv.org/abs/1909.12271)); Meta-World (CoRL 2019, PMLR v100); ManiSkill 3 ([arXiv:2410.00425](https://arxiv.org/abs/2410.00425) — the RSS proceedings title differs from the arXiv title); CALVIN ([arXiv:2112.03227](https://arxiv.org/abs/2112.03227)); LIBERO ([arXiv:2306.03310](https://arxiv.org/abs/2306.03310)); FurnitureBench (RSS 2023, DOI 10.15607/RSS.2023.XIX.041); RoboCasa (RSS 2024, DOI 10.15607/RSS.2024.XX.050 — the proceedings title says "Household", arXiv says "Everyday"); [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly) (Kimble et al., *RA-L* 2020, DOI 10.1109/LRA.2020.2965869; deformables: Kimble et al., *Frontiers in Robotics and AI* 9, 2022, DOI 10.3389/frobt.2022.999348); RAMP (*RA-L* 9(1):9–16, 2024, DOI 10.1109/LRA.2023.3330611).

**Datasets** — [Open X-Embodiment](https://robotics-transformer-x.github.io/) (ICRA 2024, [arXiv:2310.08864](https://arxiv.org/abs/2310.08864), CC BY 4.0); DROID (RSS 2024, DOI 10.15607/RSS.2024.XX.120, [arXiv:2403.12945](https://arxiv.org/abs/2403.12945)); BridgeData V2 (CoRL 2023, PMLR v229:1723–1736); [RH20T](https://rh20t.github.io/) (ICRA 2024, [arXiv:2307.00595](https://arxiv.org/abs/2307.00595)); FMB (*IJRR*, DOI 10.1177/02783649241276017); REASSEMBLE ([arXiv:2502.05086](https://arxiv.org/abs/2502.05086)); Rohbau3D (*Scientific Data*, 2025, DOI 10.1038/s41597-025-05827-7, CC BY 4.0); ConRebSeg ([arXiv:2407.09372](https://arxiv.org/abs/2407.09372)); ETHcavation ([arXiv:2410.04250](https://arxiv.org/abs/2410.04250)); the Hilti SLAM Challenge 2023 ([arXiv:2404.09765](https://arxiv.org/abs/2404.09765)); the *OpenConstruction* catalogue ([arXiv:2508.11482](https://arxiv.org/abs/2508.11482)); ConSLAM — ECCV 2022 Workshops, DOI 10.1007/978-3-031-25082-8_21, **and** *J. Comput. Civ. Eng.* 37(3):04023009, 2023, DOI 10.1061/JCCEE5.CPENG-5212.

**Within this wiki**

- [[05-construction-robotics/sim-to-real|Sim-to-Real for Field Robots]] — the reality gap these tools sit inside
- [[06-research-practice/experimental-design-reproducibility|Experimental Design & Reproducibility]] — what an evaluation has to hold fixed
- [[06-research-practice/real-world-impact|6. Real-World Impact]] — why a released dataset is worth more here than elsewhere
- [[05-construction-robotics/construction-manipulation|9. Construction Manipulation]] — the tasks these absences are absent for

## 한국어

### 1. 이 페이지의 용도

모든 프로젝트 초반에 나오고 대개 엉성하게 답해지는 질문 셋: *어느 시뮬레이터, 어느 벤치마크,
어느 데이터?* 보통은 옆자리 사람이 쓰던 것으로 답한다. 이 페이지는 각 도구가 무엇을 표현할 수
있고 없는가로 답한다 — 접촉이 많은 건설 조작에서는 그것이 결정적인 질문이기 때문이다.

여기서 가장 쓸모 있는 내용은 추천이 아니다. **부재**들이다: 있을 법한데 없는 것들. 각각이
인용 가능한 공백이다.

### 2. 시뮬레이터 — 범용

| 시뮬레이터 | 유지 주체 | 라이선스 | 정본 논문 | 가장 잘하는 한 가지 |
|---|---|---|---|---|
| **MuJoCo** | Google DeepMind | Apache-2.0 | Todorov, Erez & Tassa, IROS 2012 | 빠르고 안정적인 관절 동역학, 해석적으로 역산 가능 |
| **Isaac Sim** / **Isaac Lab** | NVIDIA | 아래 단서 참고 / BSD-3 | 없음 / Orbit, RA-L 2023 | GPU 병렬 수천 환경, RTX 실사 센서 |
| **PyBullet** | 커뮤니티 | Zlib | **없음** (`@misc`를 인용) | 쉽고 성숙하며 CPU 친화적 |
| **Gazebo** (`gz`) | Open Source Robotics Alliance | Apache-2.0 | Koenig & Howard, IROS 2004 | ROS 2 통합, 센서, 헤드리스 CI |
| **Drake** | MIT 출발, Toyota Research Institute 주도 | BSD-3 | **없음** (`@misc`를 인용) | **하이드로일래스틱 접촉** — 압력 분포를 가진 접촉면 |
| **SAPIEN** | UCSD SU Lab / Hillbot | 아래 단서 참고 | Xiang et al., CVPR 2020 | PartNet-Mobility 기반 부품 수준 관절 물체 |

이 표에서 소리 내어 말해야 할 것이 넷 있다. 각각이 활자로 틀리는 방법이기 때문이다.

> [!warning] 상태에 관한 함정 넷
> - **Isaac Gym은 지원 종료되었다.** NVIDIA 자신의 페이지가 말한다: "This is legacy software.
>   Developers may download and continue to use it, but it is no longer supported."
>   `IsaacGymEnvs`와 `OmniIsaacGymEnvs`는 2026년 4월 읽기 전용으로 보관 처리되었다. Isaac Lab을 쓰라.
> - **"Isaac Sim은 Apache 2.0"이라고 단서 없이 쓰면 안 된다.** 같은 LICENSE 파일이, 빌드하거나
>   사용하려면 별도의 NVIDIA 계약이 적용되는 추가 구성 요소 — Omniverse Kit SDK와 3D 자산 —
>   가 필요하다고 밝힌다.
> - **Gazebo Classic은 2025-01-29에 수명이 끝났고** 저장소는 보관 처리되었다. "Ignition"은
>   역사로만 등장해야 한다: `gz`로의 개명은 Open Robotics의 표현으로 "'Ignition'이라는 이름
>   사용에 관한 상표 문제" 때문이었다.
> - **SAPIEN의 라이선스는 실제로 모호하다**: 저장소 LICENSE는 Apache-2.0, PyPI 메타데이터는
>   MIT, GitHub 탐지기는 NOASSERTION이라고 한다. 하나를 고르지 말고 모호함을 진술하라.

**PyBullet·Drake·Isaac Sim·Genesis에는 심사받은 논문이 없다.** 넷 다 공식적으로 `@misc`나 URL을
인용하라고 안내한다. 그래도 괜찮다 — 다만 "Drake [소프트웨어 인용]을 사용했다"라고 쓰고,
없는 venue를 지어내지 마라.

### 3. 실제로 중요한 축: 접촉을 어떻게 모델링하는가

이 프로그램에서 시뮬레이터 사이의 흥미로운 차이는 속도가 아니다. 각각이 접촉을 *무엇으로
여기는가*다.

- **MuJoCo**는 타원 또는 각뿔 마찰 원뿔로 부드러운 볼록 최적화를 푼다. 그리고 문서가 명시적으로
  제약 위반이 설계상 허용된다고 밝힌다 — 상보성 해법(complementarity solver)이 아니다. 그것이
  빠르고 안정적인 이유이자, MuJoCo의 접촉력이 로드셀이 읽을 힘이 아닌 이유다.
- **Drake의 하이드로일래스틱 접촉**은 반대로 간다: 강체가 "약간의 변형 가능한 층을 가진 것처럼
  살짝 파고들어", 점 힘이 아니라 근사적인 접촉 *면*과 *압력 분포*를 만들고, 비볼록 기하에서도
  시간적으로 일관된 힘을 준다. 문서화된 한계도 그만큼 분명하다 — 두 강체 하이드로일래스틱 기하
  사이에는 접촉면을 만들 수 없고, "모델이 상태를 도입하지 않으므로 진짜 변형을 모델링할 수
  없어" 접선 방향 컴플라이언스와 짧은 시간 규모의 파동이 빠진다.
- **PhysX**는 Isaac 아래에서, 처리량에 맞춰 조율된 게임 엔진 계보다.

MuJoCo 3.x가 접촉 다량 작업 쪽으로 움직이고 있는 것은 추적할 가치가 있다: 3.0이 Flex 변형체를
도입했고, 3.3.0이 네이티브 볼록 충돌을 기본값으로 만들었으며, **3.3.5가 네이티브 SDF 지원과
함께 접촉 센서와 촉각 센서를 추가했다** — 뒤의 것은 "주어진 점들에서 두 물체 사이의 침투
깊이를 측정"한다. [[04-robotics/tactile-visuotactile|촉각 조작]] 프로젝트에는 실질적인 변화다.

### 4. 지형과 토공

별도의 세계이고, 별도의 도구를 쓰며, 이 도메인에서 시뮬레이션이 진짜로 성숙한 유일한 부분이다.

- **AGX Dynamics**(Algoryx)가 가장 잘 문서화된 선택지다. `agxTerrain` 모듈은 높이장 표면 아래에
  질량·다짐도·토질을 담은 3D 복셀 격자를 모델링한다. 굴착 도구가 실패 영역(failure zone)을
  만들어 고체 지형 질량을 동적 질량으로 바꾸고, **내부 마찰각과 점착력**으로 매개변수화되며,
  고체 셀이 6자유도 입자가 되고, 질량 집합체가 실패면을 통해 관성 저항을 공급한다. 관입 저항과
  굴착 저항이 분리되어 있다. 다짐, 팽창률(swell factor), 안식각도 모델링한다.
  - 독특하게도 벤더의 매개변수 수준 문서 **와** 심사받은 오픈 액세스 물리 논문을 **둘 다**
    가지고 있다: Servin, Berglund, Nystedt, *A multiscale model of terrain dynamics for
    real-time earthmoving simulation*, 2021. Algoryx는 이 모델의 굴착 저항과 토사 변위가
    "기준 모델과 10~25%까지 일치하며, 3자릿수 이상 빠르게 돈다"고 밝힌다.
  - 상용, 좌석당 연간 구독, **가격은 문의**. 학술 단일/그룹 라이선스가 있으며 엄격히 비상업용이다.
- **Vortex Studio**(CM Labs)는 변형 지형·토질 재료·토사 입자를 문서화하고 있고 운전 교육에서
  상업적으로 검증되었다. 연구에는 문제가 둘이다: 자기 토질 모델에 대해 가져올 수 있는 벤더
  이론 문서가 없어 최선의 서술이 제3자의 것이고, CM Labs 자신의 표현으로
  **"An academic License is not offered anymore."**
- **Project Chrono**가 최선의 오픈 선택지(BSD-3)이며, 하나의 프레임워크에 토질 충실도의
  *사다리*를 제공하는 유일한 것이다: **SCM**(Bekker-Wong 준경험적), 입상 **DEM**, **FEA**,
  그리고 논문이 "digging, grading"을 명시적으로 다루고 실제 굴착 로봇에 대해 검증한 SPH 연속체
  모델 **CRM**. **Chrono DEM-Engine**은 정책을 돌릴 곳이 아니라 검증의 기준으로 쓸 고충실도 모델이다.

> [!note] 정직한 권고
> **살 수 있으면 AGX, 열려 있고 인용 가능해야 하면 Chrono::CRM**, 그리고 DEM-Engine을 기준
> 모델로. 단서도 함께 가져가라: 두 선도적 실시간 토질 모델 모두 DEM 기준의 **10~25%** 수준
> 까지만 검증되었다. 어떤 실시간 시뮬레이터에서 나온 정량적 굴착력도 근사값이고, 그것을 유효
> 숫자 세 자리로 보고하는 논문은 과잉 주장이다.

### 5. 변형되는 건설 자재 — 공백을 분명히 말한다

**어떤 시뮬레이터도 건설 자재를 자재로서 모델링하지 않는다.** 드라이월도, 철근 케이지도,
건축 멤브레인도. 있는 것은 직접 매개변수화하고 직접 검증해야 하는 범용 원시 요소들이다:

| 자재 | 가장 가까운 원시 요소 | 현황 |
|---|---|---|
| 케이블·로프·호스 | AGX `agxCable` | **산업 수준으로 해결됨** — 6자유도 전부를 가진 집중 강체들이라 굽힘·비틀림·신장이 추적되고, 소성도 있다. 문서화된 한계: 케이블은 원형이고 크기·물성이 균질해야 하며, 해상도가 고정이다 |
| 철근 메시·케이지 | 연결된 로드의 네트워크 | **전용 모델 없음.** 가장 가까운 것은 로드 사이의 임의 연결을 다루는 DisMech(RA-L 2024) |
| 멤브레인·판재 | 박판 셸 | Chrono의 `ChElementShellReissner`가 물리적으로 가장 적절한 문서화된 정식화이고 BSD-3다 — 그러나 **건설 자재로 검증된 사례가 어디에도 없다** |
| **드라이월 패널** | — | **없음.** 탄성 변형이 아니라 *파단*하는 뻣뻣하고 취성이며 무거운 판재는 확인 가능한 어떤 것으로도 모델링되지 않는다 |

변형체 작업에 Isaac을 고르기 전에 알아 둘 한계가 하나 더 있다. 문서가
**"Particles and deformable body do not support contact reports"** 라고 밝히며, 정적 마찰도
마찰 결합 모드도 지원하지 않는다. 변형체에서 접촉력을 읽어낼 수 없다 — 접촉 다량 조작 연구가
하려는 측정이 바로 그것인데.

> [!warning] Genesis — 인용하기 전에 이력을 읽어라
> Genesis(현재 **Genesis World**, 회사 Genesis AI 아래에서 개발)는 하나의 API 아래 이례적으로
> 넓은 멀티피직스를 제공한다. 2024년 12월 README는 이렇게 주장했다: "over 43 million FPS when
> simulating a Franka robotic arm with a single RTX 4090 (430,000 times faster than
> real-time)". MuJoCo 유지보수자가 그 비교를 공개적으로 문제 삼았고, ManiSkill 개발자가 그
> 벤치마크가 가장 빠른(가장 부정확한) 물리 설정을 썼고, 행동 1회 뒤 999스텝을 무행동으로
> 돌렸으며, 자기 충돌을 껐다고 주장하는 이슈를 냈다. 이후 팀은 스크립트 헤더에 비판자의 것과
> "거의 동일하다"고 적힌 수정 벤치마크를 공개했고, 이슈는 비판자가 새 숫자들이 "맥락을 제대로
> 주면 더 정확해 보인다"며 — 다만 자신이 재검증하지는 않았다고 밝히며 — 닫았다.
> **43M FPS 주장은 2026년 5월 재작성 과정에서 철회 표시 없이 README에서 삭제되었다.**
> 여전히 심사받은 논문은 없고, 공식 인용 블록은 회사 블로그 글과 저장소 URL을 제시한다.
> 이 중 무엇도 소프트웨어가 나쁘다는 뜻이 아니다. 검증된 결과로 인용할 수 없다는 뜻이고,
> 인용할 때 "소프트웨어"라고 말해야 한다는 뜻이다.

### 6. 벤치마크

| 벤치마크 | Venue | 시뮬/실제 | 무엇을 재는가 | 초록이 밝힌 규모 |
|---|---|---|---|---|
| **RLBench** | RA-L 2020 | 시뮬레이션 | 과제 성공, few-shot 일반화 | "100 completely unique, hand-designed tasks" |
| **Meta-World** | CoRL 2019 | 시뮬레이션 | 멀티태스크·메타RL의 미본 과제 전이 | "50 distinct robotic manipulation tasks" |
| **ManiSkill 3** | RSS 2025 | 시뮬레이션 | 처리량과 과제 범위 | "up to 30,000+ FPS"; "12 distinct domains" |
| **CALVIN** | RA-L 2022 | 시뮬레이션 | 긴 지평 언어 조건부, zero-shot | **초록에 숫자 없음** |
| **LIBERO** | NeurIPS 2023 D&B | 시뮬레이션 | **평생 학습** 전이 — 순방향·역방향·과제 순서 | "four task suites (130 tasks in total)" |
| **FurnitureBench** | RSS 2023 | **둘 다** | 실세계 긴 지평 접촉 다량 **조립** | "200+ hours of pre-collected data (5000+ demonstrations)" |
| **RoboCasa** | RSS 2024 | 시뮬레이션 | 모방학습의 데이터 스케일링 거동 | "over 150 object categories"; "100 tasks" |
| **NIST Assembly Task Boards** | RA-L 2020 | **실제만** | **사람 기준선** 대비 완료 시간 | "three task board artifacts" |
| **RAMP** | RA-L 2024 | **둘 다** | 조립 계획 *과* 실행, 난이도 3등급 | **초록에 숫자 없음** |

**여기서 관련 있는 것은 조립 계보다**: NIST 태스크 보드가 물리적 실물과 사람 기준 채점
프로토콜을 준다(peg 삽입, 기어 맞물림, 커넥터, 너트 체결, 그리고 후속 보드에서 케이블 배선과
와이어 하니스). FurnitureBench가 시뮬레이터를 곁들인 실기계 긴 지평 벤치마크를 더한다. 그리고
**RAMP**가 건설을 틀로 삼은 유일한 것이다 — Section I이 도메인을 *오프사이트* 건설이라고
밝히며 "빔을 프레임으로 조립하는 일은 여전히 수작업으로 남아 있다"고 말한다.

> [!important] RAMP는 조심해서 인용하라
> RAMP의 초록은 "real-world industrial assembly tasks"라고만 말한다 — **construction이라는
> 단어가 초록에 나오지 않는다.** 오프사이트 건설 프레이밍은 본문에 있다. RAMP를 건설
> 벤치마크로 인용한다면 초록이 아니라 절을 인용하라.

**검증된 부재 둘.** **현장 건설 조작 벤치마크는 없다** — 조적, 드라이월, 철근 결속, 파사드
설치, 머리 위 작업 어느 것에도. 있는 것은 벤더의 처리량 수치와 각자의 평가를 쓰는 일회성
논문들이다: 공유 프로토콜도, 공유 실물도, 리더보드도 없다. 그리고 **굴착·토공에 대한 표준
벤치마크나 시험 피트 프로토콜도 없다.** ISO 7546, ISO 6165, ISO 10968과 SAE MTC1 위원회는
자율성 성능이 아니라 *기계*를 표준화한다. NASA의 Lunabotics는 규칙과 채점표를 공개하지만
레골리스 시뮬런트이고 학생 대회 범위이며 규칙이 해마다 바뀐다.

### 7. 데이터셋 — 그리고 빠져 있는 모달리티

<svg viewBox="0 0 560 258" style="max-width:100%;height:auto" role="img" aria-label="데이터셋 역량의 세 띠, 그중 세 번째가 비어 있다">
  <g fill="currentColor">
    <rect x="24" y="42" width="512" height="48" rx="4" fill-opacity="0.07"/>
    <rect x="24" y="112" width="512" height="48" rx="4" fill-opacity="0.16"/>
    <rect x="40" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="205" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="370" y="52" width="150" height="28" rx="3" fill-opacity="0.24"/>
    <rect x="40" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="205" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
    <rect x="370" y="122" width="150" height="28" rx="3" fill-opacity="0.30"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.5">
    <rect x="24" y="42" width="512" height="48" rx="4"/><rect x="24" y="112" width="512" height="48" rx="4"/>
    <rect x="40" y="52" width="150" height="28" rx="3"/><rect x="205" y="52" width="150" height="28" rx="3"/><rect x="370" y="52" width="150" height="28" rx="3"/>
    <rect x="40" y="122" width="150" height="28" rx="3"/><rect x="205" y="122" width="150" height="28" rx="3"/><rect x="370" y="122" width="150" height="28" rx="3"/>
  </g>
  <g stroke="currentColor" stroke-width="1.3" fill="none" opacity="0.75" stroke-dasharray="6 4">
    <rect x="24" y="182" width="512" height="48" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" font-weight="600">
    <text x="24" y="36">비전 + 고유수용감각 + 언어</text>
    <text x="24" y="106">&#8230; 그리고 힘/토크 채널</text>
    <text x="24" y="176">&#8230; 그리고 건설 작업에서</text>
  </g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="115" y="66">Open X-Embodiment</text><text x="115" y="77" font-size="9">스킬 527, 과제 160,266</text>
    <text x="280" y="66">DROID</text><text x="280" y="77" font-size="9">궤적 65,000</text>
    <text x="445" y="66">BridgeData V2</text><text x="445" y="77" font-size="9">궤적 53,896</text>
    <text x="115" y="136">RH20T</text><text x="115" y="147" font-size="9">시퀀스 110,000+</text>
    <text x="280" y="136">FMB</text><text x="280" y="147" font-size="9">기능적 조작</text>
    <text x="445" y="136">REASSEMBLE</text><text x="445" y="147" font-size="9">시연 4,551</text>
    <text x="280" y="212" font-size="11" opacity="0.9">공유된 실기계 힘 데이터가 없다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="250">모든 수치는 그 논문 자신의 초록에서 인용했다. 세 번째 띠가 비어 있고, 그것이 발견이다.</text>
  </g>
</svg>

큰 조작 코퍼스들은 **비전·고유수용감각·언어**다. 어느 한 데이터셋의 실수가 아니라 공유 스키마에
박혀 있는 것이다. Open X-Embodiment 개요 시트의 열은 *로봇, 에피소드, 파일 크기, 형태, 그리퍼,
행동 공간, RGB 카메라, 깊이 카메라, 손목 카메라, 언어 주석, 수집 방법, 고유수용감각, 장면 유형,
제어 주파수* 로 이어진다 — **force 열도 tactile 열도 없다.** 지배적인 데이터 형식이
[[04-robotics/force-compliance-control|접촉 다량 조작]]이 가장 의존하는 모달리티를 표현하지 못한다.

이 패턴을 깨는 데이터셋들:

- **RH20T**가 중요한 것이다: 초록이 "over 110,000 contact-rich robot manipulation sequences"라
  말하고, 프로젝트 페이지가 RGB·깊이·관절 토크·오디오와 함께 **100 Hz의 6자유도 힘/토크
  채널**을 문서화한다. 손끝 촉각도 있지만 **로봇 구성 일곱 중 하나에만** 있다 — 코퍼스 전체를
  촉각이라고 서술하지 마라.
- **FMB**(IJRR)는 말단 힘과 토크 필드를 명시적으로 노출한다.
- **REASSEMBLE**은 NIST 태스크 보드 위에서 이벤트 카메라·힘토크·마이크·다시점 RGB를 기록한다 —
  "4,551 demonstrations, of which 4,035 were successful".
- OXE 안에서도 구성 데이터셋 둘이 힘을 담고 있다 — 다만 *어디에* 담기는지를 정확히 하라.
  `iamlab_cmu_pickup_insert`는 **상태 벡터 안에** 넣는다(20차원: 관절각 7, 그리퍼 1, 관절
  토크 6, 말단 힘 6). `stanford_kuka_multimodal`([[01-canonical-papers/notes/7-robotics/vision-and-touch|Vision-and-Touch]]
  데이터)은 **그렇지 않다**: 상태는 8차원 고유수용뿐이고, 힘은 형제 관측 필드
  (`ee_forces_continuous`)에 있다. 둘 다 작고, 통합 스키마는 어느 쪽도 드러내지 않는다.

> [!warning] 큰 데이터셋의 인용 함정 둘
> **DROID**는 곳에 따라 다른 숫자를 보고한다: arXiv 초록은 궤적 76k에 과제 84개, RSS 프로시딩
> 초록은 65,000에 86개다. **BridgeData V2**도 마찬가지다: arXiv 60,096, PMLR 프로시딩 53,896.
> 인용하는 판본에 맞는 숫자를 쓰라.

### 8. 건설·현장 데이터

실제 건설 현장 데이터셋은 존재하고, 그 전부가 **인식** 코퍼스다:

- **ConSLAM** — 그리고 이것은 하나가 아니라 **두 편의 별개 논문**이다. ECCV 2022 Workshops
  논문이 데이터셋을 발표한다(이미지·LiDAR·IMU·지상 레이저 기준 스캔, 주기적으로 수집).
  *Journal of Computing in Civil Engineering* 2023 논문이 확장판이며 그것을 벤치마크로 만드는
  것을 더한다: 공개 규모를 "five sequences"로 명시하고, 순차 LiDAR를 기준 스캔에 정합해
  **기준 궤적을 복원**하며, 그에 대해 SLAM 오차를 자동으로 채점하는 방법을 문서화한다.
  저자들의 저장소가 저널 논문을 워크숍 논문의 "Free Journal Extension Paper"라고 스스로
  이름 붙인다 — 두 데이터셋이 아니라 두 번 발표된 하나의 데이터셋이다.
- **Hilti-Oxford**(RA-L 2023)와 **Hilti SLAM Challenge** 시리즈 — 건설 환경에서의
  LiDAR·카메라·IMU, 밀리미터 정확도 기준값, CC BY-NC-SA.
- **Rohbau3D**(*Scientific Data*, 2025) — "504 high-resolution LiDAR scans captured with a
  terrestrial laser scanner across 14 distinct construction sites", 의미 라벨 포함,
  **CC BY 4.0**. 확인한 것 중 라이선스가 가장 좋은 건설 현장 3D 코퍼스다.
- **ConRebSeg** — "14,805 RGB images with segmentation labels for autonomous robotic
  inspection of reinforced concrete defects", CC BY 4.0.
- **SODA**, **MOCS**, **ACID**, **CIS** — 검출과 분할을 위한 건설 *이미지* 데이터셋. 함정이
  둘 있다: ACID는 때때로 굴착 데이터셋으로 잘못 인용되지만 기계의 이미지일 뿐 토사도 힘도
  궤적도 없고 — 변형체 조작을 다루는 무관한 로보틱스 논문에도 ACID라는 이름이 있다.

토공에 한정하면 가장 큰 궤적 코퍼스는 기업 공개물이다 — RGB, LiDAR 유래 표고 지도, 관절각을
담은 굴착기 동작 데이터로, 비상업 라이선스이며 **뒤에 논문이 없다.** ETH의 건식 석벽 데이터셋은
배치 가능성 라벨이 붙은 디지털화된 돌 메시 1,100개를 CC BY 4.0으로 공개한다 — 기하와 라벨이지
궤적도 힘도 아니다. **측정된 버킷 힘이나 토사-도구 상호작용의 공개 데이터셋은 존재하지 않는다.**

> [!important] 공백을 가장 날카롭게 진술하는 법
> 이 데이터셋 중 둘은 **실제 건설 기계에서** 기록되었다 — Hilti SLAM Challenge 2023은 Jaibot을
> 참조한 드릴링 로봇 플랫폼을 썼고, **ETHcavation**은 Menzi Muck M545 보행 굴착기에서 기록해
> "502 hand-labeled sample images with panoptic annotations from construction sites"를 공개한다.
> **어느 쪽도 액추에이터·관절·유압·힘 채널을 공개하지 않는다. 기계는 계측되어 있었고, 힘은
> 공유되지 않았다.**
>
> 이것은 독립적으로 뒷받침된다. "51 publicly available visual datasets that span the
> 2005-2024 period"를 정리한 심사 논문 *OpenConstruction*은 그것들을 RGB·열화상·깊이·LiDAR
> 포인트 클라우드·합성이라는 모달리티 분류로 조직한다 — **거기에 force, torque, tactile,
> contact 행이 아예 없다.**

> [!important] 이 프로그램이 놓인 공백
> **실기계의 *접촉 다량* 건설 조작 시연을 담은 공유 데이터셋은 존재하지 않는다.** DROID
> 규모도, 10,000도, 1,000도 아니다. 무엇이 없고 무엇이 있는지를 정확히 말해야 한다. 이 위키
> 안의 논문 셋이 반례처럼 보이지만 아니기 때문이다:
> [[01-canonical-papers/notes/8-construction/ext|ExT]]는 과제당 15만 에피소드를 갖지만
> 시뮬레이션에서 생성되어 실제 접촉이 없고,
> [[01-canonical-papers/notes/8-construction/liang-lfd|Liang]]은 가상 3,000 + 실제 85개의
> 시연 *영상*을 쓰고 Gazebo에서 평가하며,
> [[01-canonical-papers/notes/8-construction/kindle-jaibot|Kindle]]은 데이터셋 일곱 개를
> 공개하지만 그것은 변형 보상용 가속도계·자세 기록이지 조작 시연이 아니다. 셋 중 어느
> 것도 공유 스키마의 힘을 동반한 실기계 시연을 제공하지 않는다. OXE의 `scene type` 열은 *table top,
> kitchen, hallway, office, pantry, shelf, workshop, outdoors* 같은 값을 갖는다 — 건설도,
> 현장도, 중장비도 없다.
>
> 공백은 3~4자릿수이고, 정도만이 아니라 **종류**의 공백이다: 힘 채널도, 촉각 채널도, 공유
> 스키마도 없다. 실제 건설 작업의 잘 큐레이션된 데이터셋이 불균형하게 값어치 있는 이유가
> 그것이고([[06-research-practice/real-world-impact|6. §3]]),
> [[04-robotics/teleoperation-demonstration|12번]]의 시연 수집 문제가 여기서는 공학적 세부가
> 아니라 연구 질문인 이유도 그것이다.

### 9. 이 프로그램을 위한 선택

| 하려는 일 | 쓸 것 | 이유 |
|---|---|---|
| 접촉 다량 조작 정책 학습 | MuJoCo, 규모가 필요하면 Isaac Lab | 속도와 안정성. 진짜 접촉력이 필요한지 먼저 확인할 것 |
| 접촉 **힘**이 곧 결과인 연구 | Drake(하이드로일래스틱) + 실기계 | 점 힘이 아니라 접촉면과 압력 분포 |
| 굴착·지형 | 예산이 되면 AGX, 아니면 Chrono::CRM | 인용 가능한 물리를 갖춘 유일한 문서화된 토질 모델들 |
| 조립 평가 | NIST 태스크 보드 → FurnitureBench → RAMP | 실물, 그다음 실기계, 그다음 건설 프레이밍 |
| 변형되는 건설 자재 | 없다 — 만들고 검증하라 | 논문에 그렇게 쓰라. 당신 연구의 결함이 아니라 기여다 |
| 조작 정책 사전학습 | Open X-Embodiment, DROID, RH20T | 힘 채널이 필요하면 RH20T |

### 10. 남의 논문의 도구 절 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 어느 시뮬레이터, 어느 버전인가? | Isaac Gym 결과는 지원 종료 이전의 것이고, MuJoCo 접촉은 3.x에서 바뀌었다 |
| 접촉력은 **시뮬레이션**인가 **측정**인가? | 시뮬레이터의 접촉력은 측정이 아니라 모델링 선택이다 |
| 시뮬만인가, 실제만인가, 둘 다인가? | 벤치마크마다 다른데 "벤치마크"라는 말이 그것을 감춘다 |
| 어느 데이터셋 **판본**이며, 어느 초록의 숫자인가? | DROID와 BridgeData V2 둘 다 서로 다른 수치를 보고한다 |
| 데이터에 힘이나 촉각이 있기는 한가? | 대개 없고, 대개 논문이 그렇다고 말하지 않는다 |
| 그 도구는 인용 가능한가? | PyBullet·Drake·Isaac Sim·Genesis에는 심사받은 논문이 없다 |

### 11. 학습된 정책의 평가 읽기

도구 절은 그 숫자들이 *무엇 위에서* 나왔는지를 알려준다. 이 절은 숫자 자체에 관한 것이다 —
VLA·확산 정책·로코모션 논문에서 백분율이 등장하고, 비교되기 전에 해석되어야 하는 그 부분.

**"성공률"이 빠뜨리는 것.** 백분율 하나가 독립적인 선택 네 개를 압축하고 있고, 80%를 보고한
두 논문이 그중 어느 것에서도 일치하지 않을 수 있다:

| 선택 | 숫자를 움직이는 이유 |
|---|---|
| **시행 횟수** | 10회로는 약 10퍼센트포인트 아래를 분간할 수 없다. 3의 법칙($3/n$)으로, 10회 중 실패 0회는 참 실패율 **30%** 근처까지와 양립한다(정확한 상한은 26%이고, 위키는 전체에서 $3/n$을 쓴다) — 그러니 "10/10"은 신뢰성의 증거가 *아니다*([[06-research-practice/experimental-design-reproducibility\|3. 실험 설계 §4]]) |
| **초기 상태 분포** | 물체 자세를 무작위화했는가, 같은 자리로 리셋했는가? 고정된 시작에서 평가된 정책은 분포에서 평가된 정책보다 쉬운 질문을 받고 있다 |
| **무엇을 완료로 세는가** | 시간 제한, 자세 허용오차, 사람 판정. 허용오차는 자주 명시되지 않고, 두 시스템의 차이 전체가 거기인 경우가 흔하다 |
| **리셋과 재시도를 세는가** | 시행 사이에 사람이 물체를 바로 세워 준다면 그 사람도 시스템의 일부다. 그것을 세지 않으면 보고된 자율성은 측정된 자율성이 아니다 |

**진행도와 부분 점수.** 긴 지평 과제와 연쇄 과제는 완료 여부가 아니라 *정책이 얼마나 갔는지*로
채점되는 일이 늘고 있다 — 단계 완료 수, 하위 과제 수, 정규화된 진행 점수. 이진 성공이 너무
거칠다는 데 대한 합당한 대응이고, 동시에 특정한 비교 실패를 들여온다: **높은 진행 점수와 0%
성공률은 양립한다.** 그리고 그것은 과제를 안정적으로 시작하고 안정적으로 끝내지 못하는 정책을
기술한다. [[01-canonical-papers/notes/4-vla/pi0|π0]] 주장 상자의 독립 평가가 정확히 이 모양이다.
논문이 진행도를 앞세우면 완료 숫자를 찾아보고, 완료를 앞세우면 베이스라인에도 부분 점수가
주어졌는지를 확인하라.

**Seen 대 unseen.** 이 문헌의 거의 모든 일반화 주장이 분할 위에 서 있고, 그 분할의 *축*이 곧
주장이다: 본 적 없는 물체 개체, 본 적 없는 물체 범주, 본 적 없는 배경, 조명, 장면, 신체.
이것들은 난이도가 같지 않은데 논문은 좀처럼 서열을 밝히지 않는다. 학습한 범주의 다른 개체로
일반화하는 방법은 범주를 가로질러 일반화하는 방법보다 훨씬 약한 주장을 하고 있다 — **숫자보다
분할의 정의를 먼저 읽어라.** 숫자는 그것에 상대적으로만 의미가 있다.

**1차 평가 대 독립 평가.** 로봇 학습 결과는 재현 비용이 커서, 출판된 비교 대부분은 저자들이
남의 방법을 직접 재현한 것이다. 부정직한 것은 아니지만 독립적인 것도 아니다. 진짜 제3자
평가가 존재한다면 그것이 헤드라인보다 값어치가 있고, 둘 사이의 격차는 자주 크다 —
[[01-canonical-papers/notes/9-navigation/gervet-real-world-objectnav|Gervet 등]](시뮬 77% →
실제 주택 여섯 곳 23%)과 π0의 독립 재평가를 보라. **비교를 인용할 때는 누구의 평가인지 밝혀라.**

> [!warning] 정책 표 대부분을 결판내는 세 질문
> **1. 시행 몇 회이고, 어떤 초기 상태 분포에서인가?** **2. 이것은 시뮬레이션인가, 실험실
> 테스트베드인가, 배포 환경인가?** **3. 누구의 평가인가?** 이 셋에 답할 수 없게 만드는 결과
> 표는 측정이 아니라 실증을 보고하고 있는 것이다 — 그것도 정당한 기여이지만 다른 종류의
> 기여이고, 답할 수 있는 표와 나란히 비교되어서는 안 된다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] §2의 상태 함정 넷을 대고, 각각이 어떤 틀린 문장을 만드는지 말한다.
- [ ] MuJoCo와 Drake가 각각 접촉을 무엇으로 여기는지, 그 차이가 언제 중요한지 말한다.
- [ ] 지형 시뮬레이션의 정직한 권고와 거기 붙는 정확도 단서를 댄다.
- [ ] OXE 스키마가 표현할 수 없는 것과, 그것이 여기서 왜 중요한지 말한다.
- [ ] 이 페이지의 검증된 부재 셋을 댄다.

### 스스로 점검

1. 어떤 논문이 Isaac Sim의 변형체 실험에서 얻은 접촉력을 보고한다. 무엇이 문제인가?
2. 사용한 시뮬레이터를 인용해야 한다. Drake다. 무엇이라고 쓰겠는가?
3. 누군가 Genesis에 대해 "4,300만 FPS"를 인용한다. 어떻게 답하겠는가?
4. 관련 연구 절에 "DROID는 궤적 76,000개를 담고 있다"고 썼다. 언제 이것이 틀리는가?
5. 심사자가 왜 표준 건설 조작 벤치마크로 평가하지 않았느냐고 묻는다. 답은?

> [!tip]- 정답 · Answers
> 1. Isaac Sim 자신의 문서가 입자와 변형체는 **contact report를 지원하지 않는다**고 밝힌다 — 거기서는 변형체에서 접촉력을 읽어낼 수 없다. 힘이 다른 데서 왔거나(강체 프록시, 추정값) 논문이 그렇게 밝혔어야 하거나, 아니면 그 숫자가 보이는 것과 다르다. 변형체에는 정적 마찰과 마찰 결합 모드도 지원되지 않아 문제가 겹친다.
> 2. Drake가 스스로 제시하는 소프트웨어 인용 — 프로젝트 이름, 개발팀, URL을 담은 `@misc`. **심사받은 Drake 논문은 없으므로** venue를 지어내면 조작된 인용이 된다. 하이드로일래스틱 접촉을 썼다면 문서가 가리키는 접촉 모델 논문들(Castro 등)을 소프트웨어와 함께 인용하라.
> 3. 그 수치가 2024년 12월 README에서 나왔고, 방법론이 공개적으로 문제 제기되었으며 — 가장 빠른 물리 설정, 행동 1회 뒤 999스텝 무행동, 자기 충돌 해제 — 팀이 비판자의 하네스를 채택한 수정 벤치마크를 공개했고, **그 주장이 2026년 5월 철회 표시 없이 README에서 삭제되었다**고 답한다. 현재 공식 자료는 그런 주장을 하지 않는다. 살아 있는 수치로 인용해서는 안 된다.
> 4. RSS 프로시딩 판본을 인용할 때. 그 초록은 궤적 **65,000**개에 과제 86개라고 말한다. 76k/84는 arXiv 초록의 수치다. 둘 다 틀린 것이 아니고, 한쪽 인용에 다른 쪽 숫자를 붙이는 것이 틀린 것이다. BridgeData V2에도 같은 함정이 있다 — arXiv 60,096, PMLR 53,896.
> 5. 그런 것이 없다고, 분명히 말한다: 현장 건설 조작에는 공유 벤치마크가 없다 — 공유 프로토콜도, 공유 실물도, 리더보드도 없다 — 그리고 가장 가까운 RAMP는 *오프사이트* 건설을 틀로 삼는다. 방어 가능한 수는 부재를 진술하고, 가장 가까운 평가 장치를 빌려 오고(조립 채점은 NIST 태스크 보드, 또는 RAMP의 프로토콜), 남이 다시 돌릴 수 있을 만큼 명시적으로 자기 프로토콜을 정의하는 것이다 — 그리고 그것 자체가 공개할 가치가 있는 산출물이다.

### 출처

**2026-08-22**에 공식 출처로 확인했다. 규모 수치는 따로 표시하지 않는 한 각 논문 자신의
초록에서 인용한 것이고, 부재에 근거한 주장은 공식 페이지를 확인했으나 아무것도 없었다는 뜻이다.

**시뮬레이터** — [MuJoCo](https://mujoco.readthedocs.io/)(Todorov, Erez & Tassa, IROS 2012, pp. 5026–5033, DOI 10.1109/IROS.2012.6386109); [Isaac Sim](https://developer.nvidia.com/isaac/sim)과 [Isaac Lab](https://isaac-sim.github.io/IsaacLab/)(선행 Orbit: Mittal et al., *RA-L* 8(6), 2023, DOI 10.1109/LRA.2023.3270034); [Isaac Gym 레거시 고지](https://developer.nvidia.com/isaac-gym); [Bullet](https://github.com/bulletphysics/bullet3); [Gazebo](https://gazebosim.org/docs/latest/releases/)와 [Classic 수명 종료 고지](https://classic.gazebosim.org/)(Koenig & Howard, IROS 2004, pp. 2149–2154); [Drake](https://drake.mit.edu/)와 [하이드로일래스틱 접촉 가이드](https://drake.mit.edu/doxygen_cxx/group__hydroelastic__user__guide.html); [SAPIEN](https://github.com/haosulab/SAPIEN)(Xiang et al., CVPR 2020, pp. 11094–11104); [Genesis World](https://github.com/Genesis-Embodied-AI/genesis-world), [벤치마크 이슈](https://github.com/Genesis-Embodied-AI/genesis-world/issues/181), [MuJoCo 논의](https://github.com/google-deepmind/mujoco/discussions/2303).

**지형** — [agxTerrain 사용자 매뉴얼](https://www.algoryx.se/documentation/complete/agx/tags/latest/doc/UserManual/source/agxTerrain.html); M. Servin, T. Berglund, S. Nystedt, "A multiscale model of terrain dynamics for real-time earthmoving simulation," *Advanced Modeling and Simulation in Engineering Sciences* 8:11, 2021, DOI 10.1186/s40323-021-00196-3; [Vortex Studio 라이선싱](https://vortexstudio.atlassian.net/wiki/spaces/VSD2511/pages/4607410452); [Project Chrono 지형 모델](https://api.projectchrono.org/vehicle_terrain.html)과 CRM은 Unjhawala et al., [arXiv:2507.05643](https://arxiv.org/abs/2507.05643).

**벤치마크** — RLBench([arXiv:1909.12271](https://arxiv.org/abs/1909.12271)); Meta-World(CoRL 2019, PMLR v100); ManiSkill 3([arXiv:2410.00425](https://arxiv.org/abs/2410.00425) — RSS 프로시딩 제목이 arXiv 제목과 다르다); CALVIN([arXiv:2112.03227](https://arxiv.org/abs/2112.03227)); LIBERO([arXiv:2306.03310](https://arxiv.org/abs/2306.03310)); FurnitureBench(RSS 2023, DOI 10.15607/RSS.2023.XIX.041); RoboCasa(RSS 2024, DOI 10.15607/RSS.2024.XX.050 — 프로시딩 제목은 "Household", arXiv는 "Everyday"); [NIST Assembly Task Boards](https://www.nist.gov/el/intelligent-systems-division-73500/robotic-grasping-and-manipulation-assembly/assembly)(Kimble et al., *RA-L* 2020, DOI 10.1109/LRA.2020.2965869; 변형체는 Kimble et al., *Frontiers in Robotics and AI* 9, 2022, DOI 10.3389/frobt.2022.999348); RAMP(*RA-L* 9(1):9–16, 2024, DOI 10.1109/LRA.2023.3330611).

**데이터셋** — [Open X-Embodiment](https://robotics-transformer-x.github.io/)(ICRA 2024, [arXiv:2310.08864](https://arxiv.org/abs/2310.08864), CC BY 4.0); DROID(RSS 2024, DOI 10.15607/RSS.2024.XX.120, [arXiv:2403.12945](https://arxiv.org/abs/2403.12945)); BridgeData V2(CoRL 2023, PMLR v229:1723–1736); [RH20T](https://rh20t.github.io/)(ICRA 2024, [arXiv:2307.00595](https://arxiv.org/abs/2307.00595)); FMB(*IJRR*, DOI 10.1177/02783649241276017); REASSEMBLE([arXiv:2502.05086](https://arxiv.org/abs/2502.05086)); Rohbau3D(*Scientific Data*, 2025, DOI 10.1038/s41597-025-05827-7, CC BY 4.0); ConRebSeg([arXiv:2407.09372](https://arxiv.org/abs/2407.09372)); ETHcavation([arXiv:2410.04250](https://arxiv.org/abs/2410.04250)); Hilti SLAM Challenge 2023([arXiv:2404.09765](https://arxiv.org/abs/2404.09765)); *OpenConstruction* 카탈로그([arXiv:2508.11482](https://arxiv.org/abs/2508.11482)); ConSLAM — ECCV 2022 Workshops, DOI 10.1007/978-3-031-25082-8_21, **그리고** *J. Comput. Civ. Eng.* 37(3):04023009, 2023, DOI 10.1061/JCCEE5.CPENG-5212.

**이 위키 안에서**

- [[05-construction-robotics/sim-to-real|필드 로봇 Sim-to-Real]] — 이 도구들이 놓인 reality gap
- [[06-research-practice/experimental-design-reproducibility|실험 설계와 재현성]] — 평가가 무엇을 고정해야 하는가
- [[06-research-practice/real-world-impact|6. 실세계 임팩트]] — 여기서 공개 데이터셋이 다른 곳보다 값어치 있는 이유
- [[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]] — 이 부재들이 부재인 대상 작업들
