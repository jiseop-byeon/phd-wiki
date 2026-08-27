---
title: 14. Tactile & Visuotactile Sensing
tags: [robotics, manipulation, sensing]
study-depth: Working
wiki-support: Working
depth-goal: "Say what a given tactile sensor measures and what it cannot, judge whether a task needs touch at all, and read a visuotactile paper's evaluation honestly."
mastery-when: "Raise to Mastery when tactile sensing, the fusion architecture, or a touch-conditioned policy is the contribution — but not for building sensors, which the research program keeps out of scope."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to select a sensor for a task, understand what a fusion architecture
> is doing, and see through an evaluation that credits touch for something vision did.
> **Working** — 과제에 맞는 센서를 고르고, 융합 구조가 무엇을 하는지 이해하고, 비전이 한 일을
> 촉각의 공으로 돌리는 평가를 꿰뚫어 볼 수 있을 만큼.

> [!note] Prerequisites · 선수 지식
> You need friction and contact modes ([[04-robotics/contact-force-tactile|Contact, Force & Tactile §2–3]]), the impedance/admittance distinction and the contact-transition timescales ([[04-robotics/force-compliance-control|13. §2, §5]]), and what a learned representation is ([[02-foundations/neural-network-basics|0.7]]).
> 마찰과 접촉 모드([[04-robotics/contact-force-tactile|접촉·힘·촉각 §2–3]]), 임피던스/어드미턴스 구분과 접촉 천이의 시간 규모([[04-robotics/force-compliance-control|13. §2, §5]]), 그리고 학습된 표현이 무엇인지([[02-foundations/neural-network-basics|0.7]])가 필요하다.

## English

*Group H. Stands on [[04-robotics/contact-force-tactile|9. Contact]], [[04-robotics/force-compliance-control|13. Force Control]] and [[02-foundations/neural-network-basics|0.7]].
For the tasks where the deciding variable is inside the contact, hidden by the very thing doing the manipulating.*

> [!note] First pass · 처음이라면
> Read §1 — what vision cannot see, and why that is a short and specific list — then §2 on what a sensor actually transduces, then §6. §3 and §4 are for reading a specific fusion or slip-detection paper.

### 1. What vision cannot see

The case for touch is not that it is richer than vision. It is that a handful of quantities
that decide whether a contact-rich task succeeds are, at the moment they matter, **occluded
by the very thing doing the manipulating**.

| Quantity | Why vision misses it |
|---|---|
| Whether contact has occurred at all | the gripper and the part hide the contact patch |
| Contact force and its distribution | force is not a visual quantity; you see deformation only if something visibly deforms |
| **Incipient slip** | the object has not moved yet — that is the whole point of detecting it |
| Local geometry inside the grasp | the fingers are in the way |
| Whether a part is seated, or merely touching | often a sub-millimetre distinction |

The last two are the construction case. A bolt that is started and a bolt that is
cross-threaded look identical from outside the grasp; a panel resting against a frame and a
panel seated in it differ by less than the camera's depth noise. That is the argument for
this page, and it is narrower than "touch is important": touch earns its place on the
specific tasks where the decisive variable is inside the contact.

### 2. What the sensors actually measure

Tactile sensors are usually grouped by transduction. The more useful grouping for reading
papers is by **what physical quantity comes out**, because that is what constrains the
claims a paper can make.

<svg viewBox="0 0 560 264" style="max-width:100%;height:auto" role="img" aria-label="four sensor families arranged by what they output, from a single six-axis wrench to a dense image of the contact surface">
  <g fill="currentColor">
    <rect x="24" y="46" width="122" height="96" rx="4" fill-opacity="0.10"/>
    <rect x="160" y="46" width="122" height="96" rx="4" fill-opacity="0.14"/>
    <rect x="296" y="46" width="122" height="96" rx="4" fill-opacity="0.20"/>
    <rect x="432" y="46" width="104" height="96" rx="4" fill-opacity="0.28"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="46" width="122" height="96" rx="4"/><rect x="160" y="46" width="122" height="96" rx="4"/><rect x="296" y="46" width="122" height="96" rx="4"/><rect x="432" y="46" width="104" height="96" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="85" y="68" font-size="11">wrist force/torque</text>
    <text x="221" y="68" font-size="11">taxel array</text>
    <text x="357" y="68" font-size="11">optical tactile</text>
    <text x="484" y="68" font-size="11">soft pin array</text>
    <text x="85" y="90" font-size="9.5" opacity="0.85">6 numbers</text>
    <text x="221" y="90" font-size="9.5" opacity="0.85">a coarse pressure map</text>
    <text x="357" y="90" font-size="9.5" opacity="0.85">an image of the</text>
    <text x="357" y="102" font-size="9.5" opacity="0.85">deformed surface</text>
    <text x="484" y="90" font-size="9.5" opacity="0.85">pin displacements</text>
    <text x="85" y="118" font-size="9.5" opacity="0.7">total wrench only</text>
    <text x="221" y="118" font-size="9.5" opacity="0.7">where, roughly</text>
    <text x="357" y="120" font-size="9.5" opacity="0.7">shape, not force</text>
    <text x="484" y="118" font-size="9.5" opacity="0.7">shear and normal</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.7" marker-end="url(#arTc)">
    <line x1="24" y1="170" x2="530" y2="170"/>
  </g>
  <defs><marker id="arTc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="24" y="188">one contact, integrated</text>
    <text x="530" y="188" text-anchor="end">the contact patch, resolved</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="218">Moving right buys spatial detail and costs you a direct force reading: an optical tactile sensor</text>
    <text x="20" y="234">measures the gel&#8217;s geometry, and force is inferred from it rather than transduced.</text>
    <text x="20" y="250">A wrist sensor is the opposite &#8212; honest newtons, no idea where they came from.</text>
  </g>
</svg>

- **Wrist force/torque sensors** give one six-axis wrench, calibrated, at high rate. They
  are the workhorse of [[04-robotics/force-compliance-control|force control]] and they tell
  you *how hard*, never *where*. Everything distal to the sensor — the gripper's own weight
  and inertia — is in the reading and must be compensated.
- **Taxel arrays** (capacitive, piezoresistive) give a coarse pressure map. Cheap,
  robust, low resolution, and they drift.
- **Optical (vision-based) tactile sensors** — GelSight, DIGIT — put a camera behind a
  deformable gel and read the gel's deformed surface as an image. This is the key point that
  papers state and readers skip: **they measure geometry, and force is inferred from
  deformation rather than transduced.** They give remarkable spatial detail about the shape
  pressed into the gel, at camera frame rates and camera latency.
- **Soft pin arrays** — the TacTip family — track internal pins that mimic dermal papillae,
  giving shear as well as normal information from a 3D-printable, robust structure.

The right question for any of them is not "how sensitive is it" but **"what does it output
at what rate, and what has to be inferred?"** The answer bounds what the paper on top of it
can claim.

> [!important] The latency point that §5 of the force-control page already made
> An optical tactile sensor runs at camera rate. A hard contact transition is over in a
> millisecond or two ([[04-robotics/force-compliance-control|13. §5]]), so touch is not a
> mechanism for *surviving* impact — it is a mechanism for **deciding what to do next**.
> Papers that use tactile feedback for closed-loop force regulation are making a much
> stronger hardware claim than papers that use it for state estimation and re-planning, and
> the two are easy to confuse in an abstract.

> [!example] Worked example · 계산 예제
> **Why "tactile sees what vision cannot" is an arithmetic claim.** GelSight publishes 0.0634 mm
> per pixel over an 18 × 24 mm pad for the Mini. A wrist camera with a 90° horizontal field of
> view at 0.5 m spans $2 \times 0.5 \times \tan 45° = 1.0$ m across 1280 pixels, i.e.
> **0.78 mm per pixel**. Over the patch that matters, the tactile sensor resolves
> $0.78/0.0634 = \mathbf{12\times}$ finer — and it does so *while the object is occluded by the
> fingers*, which is exactly when the camera has nothing.
>
> **The same argument in time.** An object slipping at 50 mm/s moves $50/30 = 1.7$ mm between
> two frames of a 30 Hz camera and $50/1000 = 0.05$ mm between two frames of a 1 kHz tactile
> signal. A 1.7 mm slip has already changed the grasp; 0.05 mm has not. Slip detection is not a
> modality preference, it is a sampling-rate result.
>
> **The reading this gives you.** These two ratios bound what any tactile paper can honestly
> claim. Resolution buys you contact geometry over a patch the size of a fingertip and nothing
> beyond it — a tactile sensor cannot tell you where the object is on the table. Rate buys you
> events shorter than a camera frame. A paper claiming tactile improved a task should be
> locating its gain in one of those two, and if it cannot, the gain is probably coming from
> somewhere else in the system.

### 3. Slip, contact state, and the things touch is uniquely for

Three problems where touch is not one option among several:

- **Incipient slip detection.** Before an object moves, the contact patch begins to slip at
  its edges while the centre still sticks. That partial-slip signature is visible in a
  dense tactile signal and in nothing else — by the time vision sees motion, the object is
  already falling. This is the single clearest case for a high-resolution sensor.
- **Contact-state estimation.** Which of the discrete contact modes
  ([[04-robotics/contact-force-tactile|Contact §3]]) the system is in — no contact, one-point,
  two-point, line, seated — is a *classification* problem whose evidence is largely tactile.
  It is also the state a task-level planner actually needs.
- **In-hand pose.** Where the object is *relative to the fingers* after grasping, which is
  the error a vision-planned grasp leaves behind and the thing an insertion needs.

#### Why the signal splits into two channels

Human skin does not have one touch sense, it has four receptor types, and the split is the
reason tactile signal processing has two halves. Johansson and Flanagan's review is the
canonical source:

| Receptor | Adapts | Carries |
|---|---|---|
| **SA I** (Merkel) | slowly | sustained pressure, fine spatial detail |
| **SA II** (Ruffini) | slowly | skin stretch — hand shape, force direction |
| **FA I** (Meissner) | fast | flutter, low-frequency vibration (~5–50 Hz), **slip onset** |
| **FA II** (Pacinian) | fast | high-frequency vibration transmitted through a grasped tool |

The engineering consequence is direct, and it is the part most often skipped. **Slowly
varying quantities and transient events need different signal processing.** Force magnitude
is a slow signal: baseline-zero it, median-filter the noise, then regress. Slip is a
*transient*: it lives in the frequency content, so it is found with spectral features — a
short-time Fourier transform over the tactile stream — not by smoothing. A pipeline that
only low-pass filters has, by construction, deleted the evidence for the one thing touch is
uniquely good at.

The same split explains why tool use works at all: FA II carries vibration through a rigid
tool, which is why a person can feel a drill bit catch — a fact with obvious weight for
[[05-construction-robotics/construction-manipulation|construction manipulation]], where the
contact of interest is usually at the tip of a tool rather than at the skin.

#### "High-resolution" is measured against a number, and the number has a trap in it

Every tactile sensor that calls itself high-resolution is implicitly compared to human skin,
so it is worth knowing what human skin actually does. Two things matter:

- **It depends entirely on the body site.** Spatial acuity runs from roughly a millimetre at
  the fingertip to centimetres on the back or thigh. "Human-level tactile resolution" without
  a named body site is not a claim.
- **The two measurements disagree, and the popular one is the wrong one.** The traditional
  **two-point discrimination** test leaks a non-spatial cue, so subjects score better than
  their actual spatial resolution allows. The rigorous measure is the **grating orientation
  threshold**, which puts the fingertip near **0.94 mm** (the lip and tongue are finer, near
  0.5 mm). A paper quoting a two-point number as its human baseline has quoted the inflated
  one — and it will make the sensor look closer to human than it is.

The design consequence is that resolution is a *task* target, not a virtue. A construction
gripper handling a panel edge or seating an anchor does not need fingertip acuity across the
whole finger; it needs enough resolution to resolve the contact patch that decides the task.
Fix the patch first, then the sensor. And when quoting any sensor's own resolution figure,
apply [[01-canonical-papers/notes/7-robotics/gelsight|GelSight's]] own caution — know which
part of the paper the number came from, because that abstract states none.

### 4. Visuotactile fusion — and what it is really buying

The reference result here is Lee et al.'s *Making Sense of Vision and Touch*, which learns a
single compact latent representation from RGB, force/torque, and proprioception using
**self-supervised** objectives — predicting optical flow and predicting whether contact
occurs — and then does reinforcement learning in that latent space rather than on raw
inputs. The claim structure is worth internalising because it recurs:

1. Raw multimodal input is high-dimensional and badly conditioned for policy learning.
2. Self-supervision provides training signal without extra labels, because the modalities
   predict each other.
3. The compact fused representation is what makes learning on a real robot tractable.

The honest reading of fusion work in general: it usually buys **sample efficiency and
robustness**, not a capability that vision alone could never reach on infinite data. That is
still a large win on a real robot, where data is the binding constraint — but it is a
different claim from "the task is impossible without touch", and abstracts blur them.

Calandra et al.'s regrasping work is the other archetype: rather than fusing for
representation, it learns an **action-conditional outcome predictor** — given the current
visuotactile reading and a candidate grasp adjustment, will the grasp succeed? — and then
selects adjustments by search. No analytic contact model, no tactile calibration.

#### From per-task fusion to a touch backbone

The 2019 fusion papers train one representation per task and per sensor. The line since then
runs the same way vision did: pre-train a general encoder, then attach small task heads.
**Sparsh** (CoRL 2024) is the reference point — self-supervised pre-training on 460k+ tactile
images with masking and self-distillation, deliberately built to serve *several* vision-based
tactile sensors rather than one, and released with **TacBench**, a six-task benchmark so that
sensors and models can be compared at all.

Two things make it worth reading here rather than filing under "another SSL paper":

- **The backbones are ones this wiki already covers.** Its strongest variants are built on
  [[01-canonical-papers/notes/2-computer-vision/dino|DINO]] and
  [[01-canonical-papers/notes/5-world-models/jepa|I-JEPA]] — so the touch story is not a
  separate lineage, it is the vision self-supervision lineage pointed at a gel.
- **It attacks the standardisation problem directly.** The reason tactile has no equivalent
  of the camera is that every lab builds its own sensor; a representation that transfers
  across sensors is a partial answer to that, and is why the paper ships a benchmark.

> [!warning] Read its headline number carefully
> The paper reports that self-supervised pre-training beats task- and sensor-specific
> end-to-end training "by 95.1% on average over TacBench". That is an average of relative
> improvements across six heterogeneous tasks, not a success rate and not a percentage-point
> gain — the same reading error that [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA's "up to 90%"]] invites.
> Go to the per-task table before quoting it.

This is the layer this page's own scope rule admits: a touch-conditioned policy or a fusion
architecture is in scope, building the sensor is not.

### 5. Construction framings

The research program's use for this page is narrow and specific. Four framings where the
decisive variable sits inside the contact:

| Framing | The tactile question |
|---|---|
| **Tactile-guided fastening** | is the bolt started straight, or cross-threading? |
| **Visuotactile insertion** | is the part seated, or merely touching? |
| **Force-aware fitting** | is resistance the correct interference fit, or an obstruction? |
| **Tool use** | has the tool engaged the workpiece, and is it slipping in the grip? |

Each is a *classification* framed at the contact, feeding a planner — which is exactly what
§2's latency note says touch is good for, and not the closed-loop force regulation that
belongs to [[04-robotics/force-compliance-control|13]].

> [!warning] Scope, from the research program
> [[07-research-program/index|7. Research Program §7]] keeps **tactile sensor hardware** out
> of the contribution. Building a new sensor is a different dissertation. Using an existing
> sensor to make construction fastening or insertion robust is this one.

### 6. Reading a tactile paper

| Question | What a vague answer hides |
|---|---|
| What does the sensor output, at what rate and latency? | An optical sensor at camera rate cannot close a contact-transition loop |
| Is touch used for **control** or for **decision-making**? | The former is a much stronger hardware claim |
| Is there a **vision-only** ablation, on the same tasks? | Without it, the fusion result may be an architecture result |
| Is there a **touch-only** ablation? | Tells you which modality is actually carrying the task |
| How many objects, and were the test objects seen in training? | Tactile generalization across materials is genuinely hard |
| Sensor wear and recalibration over the experiment? | Gels abrade and taxels drift; long runs are where this shows |

> [!note] A reading habit these four papers teach
> **GelSight (2017), DIGIT (2020), and Making Sense of Vision and Touch (2019/2020) state no
> numbers at all in their abstracts** — their abstracts are entirely qualitative. The
> resolution figures, success rates, and sample-efficiency multipliers that circulate for
> them all come from the bodies or from secondary write-ups. Calandra et al. is the
> exception, stating "about 6,450 grasping trials" in its abstract. When you quote a number
> for any of these, know which part of the paper you took it from.

> [!tip] The wear row is the one almost nobody answers — and there is now a paper that does
> Durability is the standard omission in optical tactile work: a gel that images beautifully
> for a demo abrades in an afternoon of real contact, and abstracts do not say so.
> **PolyTouch** (Zhao, Kuppuswamy, Feng, Burchfiel & Adelson, ICRA 2025) is the exception
> worth citing, because it runs an explicit elastomer durability test — a Franka rubbing and
> chafing against a fixed tool handle, with a commercial GelSight Mini and a PolyTouch finger
> mounted opposing each other — rather than asserting robustness. For a research programme
> aimed at a **construction** task, where the contact is abrasive by nature and a session is
> measured in hours, this row is not a detail; it decides whether a demonstration corpus can
> be collected at all.

### After reading

- [ ] Name three quantities vision cannot supply at the moment they matter.
- [ ] Say what an optical tactile sensor physically measures, and what is inferred.
- [ ] Explain why sensor latency makes touch a decision signal rather than an impact-survival mechanism.
- [ ] State what visuotactile fusion usually buys, and what it usually does not.
- [ ] List the two ablations a fusion paper needs before its claim is readable.

> [!tip] Going deeper · 더 깊이
> No textbook; the sensors are the literature. Start at the physics: Johnson & Adelson (CVPR 2009) is retrographic sensing, the optical principle, before anyone put it on a robot. Then Yuan, Dong & Adelson (*Sensors* 2017) for GelSight as a robot sensor with geometry and force, and DIGIT (*RA-L* 2020) for the cheap compact form that made the modality common. Then Lee et al. (ICRA 2019) for using touch rather than building it. For the manipulation theory the signal feeds, [[04-robotics/contact-force-tactile|9. Contact §2–§4]] names its textbooks; this page has none of its own.

### Self-check

1. A paper reports that adding tactile input raised insertion success from 62% to 89%. What
   two experiments do you need before you believe touch caused that?
2. Why is incipient slip the cleanest argument for a high-resolution tactile sensor?
3. A team wants tactile feedback to regulate contact force during a hard impact, using a
   GelSight-class sensor at 30 fps. What is wrong?
4. A wrist force/torque sensor reads 12 N while the gripper holds a 1 kg part. What must be
   subtracted, and why does the arm's pose matter?
5. Your dissertation involves tactile-guided fastening. Per the research program, what is in
   scope and what is not?

> [!tip]- Answers
> 1. A vision-only ablation and a touch-only ablation, on the same tasks and the same policy architecture. Without the first, the gain may come from the extra network capacity or the extra training signal rather than from touch; without the second, you do not know whether touch is carrying the task or merely trimming its tail. A change in success rate between two differently-shaped models is an architecture comparison until those are run.
> 2. Because incipient slip is defined by the object *not having moved yet* — the contact patch is partially slipping at its edges while its centre still sticks. Any sensor that reports object motion is by construction too late, so this is a case where a dense contact signal supplies information no other modality has, rather than supplying the same information more conveniently.
> 3. At 30 fps a sample arrives every 33 ms, while a hard contact transition is complete in one or two milliseconds ([[04-robotics/force-compliance-control|13. §5]]) — the entire event occurs between two frames. The sensor can report what the contact *was*, which is useful for deciding the next action, but it cannot participate in regulating the impact itself. That job belongs to passive compliance and a kilohertz torque loop.
> 4. The gripper's own weight and any payload, projected into the sensor frame — which depends on the arm's orientation, since gravity is fixed in the world frame and the sensor rotates with the wrist. The same held part produces a different raw reading in every pose, so gravity compensation needs the current kinematics ([[02-foundations/manipulator-kinematics-dynamics|10. §5]]). Inertial terms matter too during acceleration.
> 5. In scope: using an existing tactile sensor to make fastening robust — the contact-state classification, the policy that acts on it, and the evaluation against real fasteners. Out of scope: designing or fabricating a new sensor, which [[07-research-program/index|§7]] excludes because it is a separate contribution with its own literature and its own failure modes.

### Sources

**Sensors**

- W. Yuan, S. Dong, E. H. Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force," *Sensors*, vol. 17, no. 12, art. 2762, 2017. The optical principle comes from M. K. Johnson and E. H. Adelson, "Retrographic sensing for the measurement of surface texture and shape," CVPR 2009, pp. 1070–1077.
- M. Lambeta et al., "DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor With Application to In-Hand Manipulation," *IEEE RA-L*, vol. 5, no. 3, pp. 3838–3845, 2020 ([arXiv:2005.14679](https://arxiv.org/abs/2005.14679)).
- B. Ward-Cherrier et al., "The TacTip Family: Soft Optical Tactile Sensors with 3D-Printed Biomimetic Morphologies," *Soft Robotics*, vol. 5, no. 2, pp. 216–227, 2018.

**Using touch**

- M. A. Lee, Y. Zhu, K. Srinivasan, et al., "Making Sense of Vision and Touch: Self-Supervised Learning of Multimodal Representations for Contact-Rich Tasks," ICRA 2019, pp. 8943–8950 ([arXiv:1810.10191](https://arxiv.org/abs/1810.10191)). The extended journal version has a **different title and author list**: M. A. Lee, Y. Zhu, P. Zachares, et al., "Making Sense of Vision and Touch: Learning Multimodal Representations for Contact-Rich Tasks," *IEEE T-RO*, vol. 36, no. 3, pp. 582–596, 2020 — cite them separately.
- R. Calandra et al., "More Than a Feeling: Learning to Grasp and Regrasp Using Vision and Touch," *IEEE RA-L*, vol. 3, no. 4, pp. 3300–3307, 2018 ([arXiv:1805.11085](https://arxiv.org/abs/1805.11085)).
- R. S. Johansson, J. R. Flanagan, "Coding and use of tactile signals from the fingertips in object manipulation tasks," *Nature Reviews Neuroscience* 10, pp. 345–359, 2009. DOI 10.1038/nrn2621 — the canonical account of the four mechanoreceptor types and what each carries.
- J. Tong, O. Mao, D. Goldreich, "Two-Point Orientation Discrimination Versus the Traditional Two-Point Test for Tactile Spatial Acuity Assessment," *Frontiers in Human Neuroscience* 7:579, 2013. DOI 10.3389/fnhum.2013.00579 — why the traditional two-point test overstates acuity, and what to use instead. Fingertip grating-orientation thresholds near 0.94 mm (lip and tongue nearer 0.5 mm) come from the grating-orientation literature this paper sits in.
- C. Higuera, A. Sharma, C. K. Bodduluri, et al., "Sparsh: Self-supervised touch representations for vision-based tactile sensing," *CoRL 2024* ([arXiv:2410.24090](https://arxiv.org/abs/2410.24090)) · [code](https://github.com/facebookresearch/sparsh) — touch backbones plus the TacBench benchmark.
- J. Zhao, N. Kuppuswamy, S. Feng, B. Burchfiel, E. Adelson, "PolyTouch: A Robust Multi-Modal Tactile Sensor for Contact-rich Manipulation Using Tactile-Diffusion Policies," *ICRA 2025* ([arXiv:2504.19341](https://arxiv.org/abs/2504.19341)) — includes an explicit elastomer durability comparison against a commercial GelSight Mini.

**Surveys**

- Q. Li, O. Kroemer, Z. Su, et al., "A Review of Tactile Information: Perception and Action Through Touch," *IEEE T-RO*, vol. 36, no. 6, pp. 1619–1634, 2020 — organised around the perception-to-action loop rather than around transducers, which is the right orientation for manipulation research.
- R. S. Dahiya, G. Metta, M. Valle, G. Sandini, "Tactile Sensing—From Humans to Humanoids," *IEEE T-RO*, vol. 26, no. 1, pp. 1–20, 2010 — the transduction-first background, predating the vision-based and learned era.

**Within this wiki**

- [[04-robotics/contact-force-tactile|Contact, Force & Tactile Interaction]] — friction, contact modes, and the material-state material this page builds on.
- [[04-robotics/force-compliance-control|13. Force & Compliance Control]] — the timescales that decide what touch can and cannot be used for.

## 한국어

*H군이다. [[04-robotics/contact-force-tactile|9. 접촉]]·[[04-robotics/force-compliance-control|13. 힘 제어]]와 [[02-foundations/neural-network-basics|0.7]] 위에 선다.
결정적 변수가 접촉 안에 있고, 하필 조작을 하고 있는 그것에 가려지는 과제들을 위한 페이지다.*

> [!note] 처음이라면 · First pass
> 먼저 §1 — 비전이 볼 수 없는 것, 그리고 그것이 왜 짧고 구체적인 목록인지 — 그다음 센서가 실제로 변환하는 것인 §2, 그다음 §6. §3·§4는 특정 융합·미끄러짐 논문을 읽을 때다.

### 1. 비전이 볼 수 없는 것

촉각을 쓰는 근거는 그것이 비전보다 풍부해서가 아니다. 접촉이 많은 작업의 성패를 가르는 몇
가지 양이, 하필 그것들이 중요해지는 순간에 **조작을 하고 있는 바로 그것에 가려진다**는 데
있다.

| 양 | 비전이 놓치는 이유 |
|---|---|
| 접촉이 일어났는지 여부 자체 | 그리퍼와 부재가 접촉면을 가린다 |
| 접촉력과 그 분포 | 힘은 시각적인 양이 아니다. 눈에 띄게 변형되는 것이 있을 때만 보인다 |
| **초기 미끄러짐**(incipient slip) | 물체가 아직 움직이지 않았다 — 그것을 감지하려는 이유가 바로 그것이다 |
| 파지 안쪽의 국소 기하 | 손가락이 가로막고 있다 |
| 부재가 안착했는가, 그냥 닿아만 있는가 | 흔히 밀리미터 이하의 차이다 |

마지막 둘이 건설의 경우다. 제대로 물린 볼트와 나사산이 어긋난 볼트는 파지 바깥에서 똑같아
보인다. 프레임에 기대어 있는 패널과 프레임에 안착한 패널은 카메라의 깊이 잡음보다 작은
차이다. 이것이 이 페이지의 논거이고, "촉각은 중요하다"보다 좁다: 촉각은 **결정적 변수가
접촉 안에 있는** 특정 작업에서 자기 자리를 번다.

### 2. 센서가 실제로 재는 것

촉각 센서는 보통 변환 원리로 묶인다. 논문을 읽을 때 더 쓸모 있는 묶음은 **무슨 물리량이
나오는가**다. 그것이 그 위에 얹힌 논문이 할 수 있는 주장을 제약하기 때문이다.

<svg viewBox="0 0 560 264" style="max-width:100%;height:auto" role="img" aria-label="여섯 개 숫자짜리 렌치에서 접촉면을 해상하는 이미지까지, 출력하는 것으로 배열한 네 가지 센서 계열">
  <g fill="currentColor">
    <rect x="24" y="46" width="122" height="96" rx="4" fill-opacity="0.10"/>
    <rect x="160" y="46" width="122" height="96" rx="4" fill-opacity="0.14"/>
    <rect x="296" y="46" width="122" height="96" rx="4" fill-opacity="0.20"/>
    <rect x="432" y="46" width="104" height="96" rx="4" fill-opacity="0.28"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="24" y="46" width="122" height="96" rx="4"/><rect x="160" y="46" width="122" height="96" rx="4"/><rect x="296" y="46" width="122" height="96" rx="4"/><rect x="432" y="46" width="104" height="96" rx="4"/>
  </g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="85" y="68" font-size="11">손목 힘/토크</text>
    <text x="221" y="68" font-size="11">택셀 배열</text>
    <text x="357" y="68" font-size="11">광학 촉각</text>
    <text x="484" y="68" font-size="11">연성 핀 배열</text>
    <text x="85" y="90" font-size="9.5" opacity="0.85">숫자 6개</text>
    <text x="221" y="90" font-size="9.5" opacity="0.85">거친 압력 지도</text>
    <text x="357" y="90" font-size="9.5" opacity="0.85">변형된 표면의</text>
    <text x="357" y="102" font-size="9.5" opacity="0.85">이미지</text>
    <text x="484" y="90" font-size="9.5" opacity="0.85">핀의 변위</text>
    <text x="85" y="118" font-size="9.5" opacity="0.7">합력만</text>
    <text x="221" y="118" font-size="9.5" opacity="0.7">어디인지 대략</text>
    <text x="357" y="120" font-size="9.5" opacity="0.7">힘이 아니라 형상</text>
    <text x="484" y="118" font-size="9.5" opacity="0.7">전단과 법선</text>
  </g>
  <g stroke="currentColor" stroke-width="1.4" fill="none" opacity="0.7" marker-end="url(#arTck)">
    <line x1="24" y1="170" x2="530" y2="170"/>
  </g>
  <defs><marker id="arTck" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <g font-size="10" fill="currentColor" opacity="0.85">
    <text x="24" y="188">접촉 하나로 적분됨</text>
    <text x="530" y="188" text-anchor="end">접촉면이 해상됨</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="218">오른쪽으로 갈수록 공간적 세부를 사고 직접적인 힘 측정값을 잃는다: 광학 촉각 센서는 젤의</text>
    <text x="20" y="234">기하를 재고, 힘은 변환되는 것이 아니라 그로부터 추론된다.</text>
    <text x="20" y="250">손목 센서는 정반대다 &#8212; 정직한 뉴턴, 그러나 어디서 왔는지는 모른다.</text>
  </g>
</svg>

- **손목 힘/토크 센서**는 보정된 6축 렌치 하나를 높은 주기로 준다.
  [[04-robotics/force-compliance-control|힘 제어]]의 주력이고, *얼마나 세게*는 말해 주되
  *어디서*는 결코 말해 주지 않는다. 센서보다 말단 쪽에 있는 모든 것 — 그리퍼 자신의 무게와
  관성 — 이 측정값에 들어 있으므로 보상해야 한다.
- **택셀 배열**(정전용량식, 압저항식)은 거친 압력 지도를 준다. 싸고 튼튼하며, 해상도가 낮고
  드리프트한다.
- **광학(비전 기반) 촉각 센서** — GelSight, DIGIT — 는 변형되는 젤 뒤에 카메라를 두고 젤의
  변형된 표면을 이미지로 읽는다. 논문은 밝히지만 독자가 건너뛰는 핵심이 이것이다:
  **이들은 기하를 재고, 힘은 변환되는 것이 아니라 변형에서 추론된다.** 젤에 눌린 형상에 대해
  놀라운 공간적 세부를, 카메라의 프레임률과 카메라의 지연으로 준다.
- **연성 핀 배열** — TacTip 계열 — 은 진피 유두를 모사한 내부 핀을 추적해, 3D 프린팅 가능하고
  튼튼한 구조에서 법선뿐 아니라 전단 정보까지 준다.

어느 것에 대해서든 옳은 질문은 "얼마나 민감한가"가 아니라 **"무엇을 어떤 주기로 출력하고,
무엇이 추론되어야 하는가"** 다. 그 답이 그 위에 얹힌 논문이 주장할 수 있는 범위를 정한다.

> [!important] 힘 제어 페이지 §5가 이미 한 지연 이야기
> 광학 촉각 센서는 카메라 주기로 돈다. 단단한 접촉 천이는 1~2 밀리초에 끝나므로
> ([[04-robotics/force-compliance-control|13. §5]]), 촉각은 충격에서 *살아남는* 기제가
> 아니라 **다음에 무엇을 할지 결정하는** 기제다. 촉각 피드백을 폐루프 힘 조절에 쓴다는
> 논문은 상태 추정과 재계획에 쓴다는 논문보다 훨씬 강한 하드웨어 주장을 하는 것이고, 초록에서
> 이 둘은 혼동하기 쉽다.

> [!example] 계산 예제 · Worked example
> **"촉각은 비전이 못 보는 것을 본다"가 산술적 주장인 이유.** GelSight는 Mini의 18 × 24 mm
> 패드에서 픽셀당 0.0634 mm를 공표한다. 수평 화각 90°인 손목 카메라는 0.5 m에서
> $2 \times 0.5 \times \tan 45° = 1.0$ m를 1280픽셀에 담으니 **픽셀당 0.78 mm**다. 문제가 되는
> 그 패치 위에서 촉각 센서는 $0.78/0.0634 = \mathbf{12배}$ 더 곱게 분해하고, 게다가 *손가락에
> 물체가 가려진 동안* 그렇게 한다 — 카메라에 아무것도 없는 바로 그때다.
>
> **같은 논증을 시간으로.** 50 mm/s로 미끄러지는 물체는 30 Hz 카메라의 두 프레임 사이에
> $50/30 = 1.7$ mm를, 1 kHz 촉각 신호의 두 프레임 사이에 $50/1000 = 0.05$ mm를 간다. 1.7 mm
> 미끄러짐은 이미 파지를 바꿔 놓았고 0.05 mm는 그렇지 않다. 미끄러짐 감지는 모달리티 취향이
> 아니라 샘플링 주파수의 결과다.
>
> **여기서 얻는 독법.** 이 두 비율이 촉각 논문이 정직하게 주장할 수 있는 범위를 정한다.
> 분해능은 손끝만 한 패치 위의 접촉 기하를 사 줄 뿐 그 바깥은 사 주지 않는다 — 촉각 센서는
> 물체가 탁자 위 어디에 있는지 말해 주지 못한다. 주파수는 카메라 한 프레임보다 짧은 사건을
> 사 준다. 촉각으로 과제가 나아졌다고 주장하는 논문은 그 이득을 이 둘 중 하나에 위치시켜야
> 하고, 그러지 못한다면 이득은 아마 시스템의 다른 곳에서 오고 있다.

### 3. 미끄러짐, 접촉 상태, 그리고 촉각만이 할 수 있는 일

촉각이 여러 선택지 중 하나가 아닌 세 문제:

- **초기 미끄러짐 감지.** 물체가 움직이기 전에, 접촉면은 중심이 아직 붙어 있는 동안 가장자리
  부터 미끄러지기 시작한다. 그 부분 미끄러짐의 흔적은 조밀한 촉각 신호에는 보이고 다른
  무엇에도 보이지 않는다 — 비전이 움직임을 볼 때쯤이면 물체는 이미 떨어지고 있다. 고해상도
  센서를 쓸 가장 분명한 근거다.
- **접촉 상태 추정.** 시스템이 어떤 이산 접촉 모드에
  ([[04-robotics/contact-force-tactile|접촉 §3]]) 있는가 — 비접촉, 1점, 2점, 선, 안착 —
  는 증거가 대체로 촉각인 *분류* 문제다. 그리고 과제 수준 계획기가 실제로 필요로 하는
  상태이기도 하다.
- **손 안 자세(in-hand pose).** 파지 이후 물체가 *손가락에 대해* 어디 있는가. 비전으로 계획한
  파지가 남기는 오차이자, 삽입이 필요로 하는 바로 그것이다.

#### 신호가 두 채널로 갈리는 이유

사람 피부에는 촉각이 하나가 아니라 수용기 네 종류가 있고, 그 구분이 촉각 신호처리가 두 갈래인
이유다. Johansson과 Flanagan의 리뷰가 정본이다:

| 수용기 | 적응 | 실어 나르는 것 |
|---|---|---|
| **SA I**(Merkel) | 느림 | 지속 압력, 미세한 공간 해상 |
| **SA II**(Ruffini) | 느림 | 피부 신장 — 손 모양, 힘의 방향 |
| **FA I**(Meissner) | 빠름 | 플러터, 저주파 진동(약 5~50 Hz), **미끄러짐 개시** |
| **FA II**(Pacinian) | 빠름 | 쥔 도구를 타고 전달되는 고주파 진동 |

공학적 귀결이 곧바로 나오고, 가장 자주 건너뛰는 대목이다. **천천히 변하는 양과 순간적 사건은
서로 다른 신호처리를 요구한다.** 힘의 크기는 느린 신호다 — 베이스라인을 0으로 맞추고, median
필터로 잡음을 걷어낸 뒤 회귀한다. 미끄러짐은 *과도 현상*이다 — 주파수 성분에 살기 때문에 평활화가
아니라 스펙트럼 특징(촉각 스트림의 단시간 푸리에 변환)으로 찾는다. 저역 통과만 하는 파이프라인은
구조적으로 **촉각이 유일하게 잘하는 그 하나의 증거를 지워 버린 것**이다.

같은 구분이 도구 사용이 왜 성립하는지도 설명한다. FA II가 단단한 도구를 통해 진동을 실어 나르기
때문에 사람은 드릴 비트가 걸리는 것을 느낄 수 있다 —
[[05-construction-robotics/construction-manipulation|건설 매니퓰레이션]]에서 관심 있는 접촉이
대개 피부가 아니라 **도구 끝**에 있다는 점을 생각하면 무게가 분명한 사실이다.

#### "고해상도"는 어떤 수치에 견주는 말이고, 그 수치에 함정이 있다

고해상도를 자처하는 촉각 센서는 전부 암묵적으로 사람 피부에 견주고 있으므로, 사람 피부가 실제로
어떤지를 알아둘 값이 있다. 둘이 중요하다:

- **몸의 어느 부위냐에 전적으로 달렸다.** 공간 예민도는 손끝의 약 1 mm에서 등이나 허벅지의 수
  센티미터까지 걸쳐 있다. 부위를 지목하지 않은 "인간 수준의 촉각 해상도"는 주장이 아니다.
- **두 측정이 서로 다르고, 널리 쓰이는 쪽이 틀린 쪽이다.** 전통적인 **2점 식별** 검사는 공간
  정보가 아닌 단서가 새어 들어가서, 피험자가 실제 공간 해상도보다 좋은 점수를 낸다. 엄밀한
  측정은 **격자 방향 판별 역치**이고, 손끝을 **약 0.94 mm**에 놓는다(입술과 혀는 더 미세해서
  0.5 mm 부근). 인간 기준선으로 2점 수치를 인용한 논문은 **부풀려진 쪽을 인용한 것**이고, 센서를
  실제보다 인간에 가깝게 보이게 만든다.

설계상의 귀결은 해상도가 미덕이 아니라 *과제* 목표라는 것이다. 패널 모서리를 다루거나 앵커를
안착시키는 건설 그리퍼는 손가락 전체에 손끝 수준의 예민도가 필요하지 않다. 과제를 가르는 접촉
패치를 분해할 만큼만 있으면 된다. **패치를 먼저 정하고 센서를 정하라.** 그리고 어떤 센서의 해상도
수치를 인용하든 [[01-canonical-papers/notes/7-robotics/gelsight|GelSight]] 노트의 경고를 적용하라 —
그 수치가 논문의 어느 부분에서 왔는지 알고 써라. 그 초록에는 수치가 하나도 없다.

### 4. 시촉각 융합 — 그리고 그것이 실제로 사는 것

여기서의 기준 결과는 Lee 등의 *Making Sense of Vision and Touch*다. RGB, 힘/토크, 고유수용
감각으로부터 하나의 압축된 잠재 표현을 **자기지도** 목적함수 — 광학 흐름 예측과 접촉 발생
여부 예측 — 로 학습하고, 원 입력이 아니라 그 잠재 공간에서 강화학습을 돌린다. 주장의 구조를
몸에 새겨 둘 가치가 있다. 반복해서 나오기 때문이다:

1. 원 멀티모달 입력은 고차원이고 정책 학습에 조건이 나쁘다.
2. 자기지도가 추가 라벨 없이 학습 신호를 준다. 모달리티들이 서로를 예측하기 때문이다.
3. 압축된 융합 표현이 실기계에서의 학습을 감당 가능하게 만든다.

융합 연구 일반에 대한 정직한 독법: 대개 사는 것은 **샘플 효율과 견고성**이지, 비전만으로는
무한한 데이터로도 결코 도달할 수 없는 능력이 아니다. 데이터가 제약인 실기계에서는 여전히 큰
승리다 — 그러나 "촉각 없이는 그 과제가 불가능하다"와는 다른 주장이고, 초록은 둘을 흐린다.

Calandra 등의 재파지 연구가 다른 원형이다: 표현을 위한 융합이 아니라 **행동 조건부 결과
예측기**를 학습한다 — 현재 시촉각 관측과 후보 파지 조정이 주어졌을 때 그 파지가 성공할
것인가? — 그리고 탐색으로 조정을 고른다. 해석적 접촉 모델도, 촉각 보정도 없이.

#### 과제별 융합에서 촉각 백본으로

2019년의 융합 논문들은 과제마다, 센서마다 표현을 따로 학습한다. 이후의 흐름은 비전이 갔던 길과
같다 — 범용 인코더를 사전학습하고 작은 과제 헤드를 붙인다. **Sparsh**(CoRL 2024)가 기준점이다.
촉각 이미지 46만 장 이상에 마스킹과 자기 증류로 자기지도 사전학습을 하되, 하나가 아니라 *여러*
카메라 기반 촉각 센서를 겨냥해 만들었고, 센서와 모델을 비교할 수 있도록 6개 과제 벤치마크
**TacBench**를 함께 공개했다.

"또 하나의 SSL 논문"으로 분류하지 않고 여기서 읽어야 하는 이유가 둘이다:

- **백본이 이 위키가 이미 다루는 것들이다.** 가장 강한 변형이
  [[01-canonical-papers/notes/2-computer-vision/dino|DINO]]와
  [[01-canonical-papers/notes/5-world-models/jepa|I-JEPA]] 위에 서 있다 — 촉각 이야기가 별개
  계보가 아니라 **비전 자기지도 계보를 젤에 겨눈 것**이다.
- **표준화 문제를 정면으로 친다.** 촉각에 카메라에 해당하는 물건이 없는 이유는 랩마다 자기 센서를
  만들기 때문이고, 센서를 가로질러 전이되는 표현은 그에 대한 부분적 답이다. 벤치마크를 같이 낸
  이유이기도 하다.

> [!warning] 헤드라인 수치를 조심해서 읽어라
> 논문은 자기지도 사전학습이 과제·센서 특화 end-to-end 학습을 "TacBench 전체 평균 95.1%"만큼
> 앞선다고 보고한다. 이질적인 6개 과제에 걸친 **상대 개선의 평균**이지 성공률도 퍼센트 포인트
> 상승도 아니다 — [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA의 "최대 90%"]]가
> 유발하는 것과 같은 종류의 오독이다. 인용 전에 과제별 표로 가라.

이것이 이 페이지의 범위 규칙이 허용하는 층이다 — 촉각 조건 정책이나 융합 구조는 범위 안이고,
센서를 만드는 것은 범위 밖이다.

### 5. 건설에서의 프레이밍

연구 프로그램이 이 페이지를 쓰는 용도는 좁고 구체적이다. 결정적 변수가 접촉 안에 있는 네
가지 프레이밍:

| 프레이밍 | 촉각의 질문 |
|---|---|
| **촉각 유도 체결** | 볼트가 똑바로 물렸는가, 나사산이 어긋나고 있는가? |
| **시촉각 삽입** | 부재가 안착했는가, 그냥 닿아만 있는가? |
| **힘 인지 끼움** | 저항이 올바른 억지 끼워맞춤인가, 아니면 걸림인가? |
| **공구 사용** | 공구가 작업물에 물렸는가, 그리고 손 안에서 미끄러지고 있는가? |

각각은 접촉에서 정의된 *분류*이고, 계획기에 먹인다 — §2의 지연 이야기가 촉각이 잘하는 일이라고
말한 바로 그것이며, [[04-robotics/force-compliance-control|13번]]에 속하는 폐루프 힘 조절이
아니다.

> [!warning] 연구 프로그램이 정한 범위
> [[07-research-program/index|7. 연구 프로그램 §7]]은 **촉각 센서 하드웨어**를 기여 범위 밖에
> 둔다. 새 센서를 만드는 것은 다른 학위논문이다. 기존 센서를 *써서* 건설 체결이나 삽입을
> 견고하게 만드는 것이 이 학위논문이다.

### 6. 촉각 논문 읽기

| 질문 | 모호한 답이 감추는 것 |
|---|---|
| 센서가 무엇을, 어떤 주기와 지연으로 출력하는가? | 카메라 주기의 광학 센서는 접촉 천이 루프를 닫을 수 없다 |
| 촉각을 **제어**에 쓰는가, **의사결정**에 쓰는가? | 전자가 훨씬 강한 하드웨어 주장이다 |
| 같은 과제에서 **비전만**의 ablation이 있는가? | 없으면 융합 결과가 구조(architecture) 결과일 수 있다 |
| **촉각만**의 ablation이 있는가? | 어느 모달리티가 실제로 과제를 지고 있는지 알려준다 |
| 물체 몇 개이며, 시험 물체를 학습에서 보았는가? | 재료를 가로지르는 촉각 일반화는 정말로 어렵다 |
| 실험 동안 센서 마모와 재보정은? | 젤은 마모되고 택셀은 드리프트한다. 긴 실험에서 드러난다 |

> [!note] 이 네 논문이 가르쳐 주는 독서 습관
> **GelSight(2017), DIGIT(2020), Making Sense of Vision and Touch(2019/2020)는 초록에 숫자를
> 하나도 적지 않는다** — 초록이 전부 정성적이다. 이들에 대해 떠도는 해상도 수치, 성공률,
> 샘플 효율 배수는 전부 본문이나 2차 요약에서 온 것이다. Calandra 등이 예외로, 초록에
> "약 6,450회의 파지 시행"을 적는다. 이들 중 어느 것에 대해 숫자를 인용할 때는, 그것을 논문의
> 어느 부분에서 가져왔는지 알고 있어야 한다.

> [!tip] 마모 항목은 거의 아무도 답하지 않는다 — 그런데 답한 논문이 생겼다
> 내구성은 광학 촉각 연구의 표준적 누락이다. 데모에서는 아름답게 찍히는 젤이 실제 접촉 반나절에
> 마모되는데, 초록은 그 말을 하지 않는다. **PolyTouch**(Zhao, Kuppuswamy, Feng, Burchfiel &
> Adelson, ICRA 2025)가 인용할 만한 예외다. 강건하다고 주장하는 대신 **명시적인 엘라스토머
> 내구 시험**을 돌린다 — Franka가 고정된 도구 손잡이에 계속 문지르고 쓸게 하고, 상용 GelSight
> Mini와 PolyTouch 손가락을 마주 보게 달아 비교한다. **건설** 과제를 겨냥한 연구 프로그램에서는
> 접촉이 본래 마모성이고 한 세션이 시간 단위이므로, 이 항목은 세부사항이 아니라 **시연 코퍼스를
> 애초에 모을 수 있느냐를 정하는 조건**이다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 중요해지는 순간에 비전이 줄 수 없는 양 셋을 댄다.
- [ ] 광학 촉각 센서가 물리적으로 무엇을 재고 무엇이 추론되는지 말한다.
- [ ] 센서 지연 때문에 촉각이 충격 생존 기제가 아니라 결정 신호인 이유를 설명한다.
- [ ] 시촉각 융합이 보통 사는 것과 사지 못하는 것을 말한다.
- [ ] 융합 논문의 주장이 읽히려면 필요한 두 ablation을 댄다.

> [!tip] 더 깊이 · Going deeper
> 교과서는 없고, 센서가 곧 문헌이다. 물리에서 시작하라: Johnson & Adelson(CVPR 2009)의 retrographic sensing이 광학 원리이고, 아직 아무도 로봇에 붙이기 전이다. 그다음 Yuan, Dong, Adelson(*Sensors* 2017)으로 기하와 힘을 재는 로봇 센서로서의 GelSight를, DIGIT(*RA-L* 2020)으로 이 모달리티를 흔하게 만든 값싸고 작은 형태를. 그다음 Lee 외(ICRA 2019)로 촉각을 만드는 것이 아니라 쓰는 쪽을. 이 신호가 먹여 주는 조작 이론 쪽은 [[04-robotics/contact-force-tactile|9. 접촉 §2~§4]]가 자기 교재를 지목한다. 이 페이지에는 자기 것이 없다.

### 스스로 점검

1. 어떤 논문이 촉각 입력을 더해 삽입 성공률이 62%에서 89%로 올랐다고 보고한다. 촉각이 그
   변화를 일으켰다고 믿기 전에 어떤 실험 둘이 필요한가?
2. 초기 미끄러짐이 고해상도 촉각 센서를 쓸 가장 깨끗한 근거인 이유는?
3. 어떤 팀이 30 fps의 GelSight급 센서로 단단한 충돌 중 접촉력을 조절하려 한다. 무엇이
   잘못되었는가?
4. 그리퍼가 1 kg 부재를 잡고 있을 때 손목 힘/토크 센서가 12 N을 읽는다. 무엇을 빼야 하고,
   팔의 자세가 왜 중요한가?
5. 학위논문이 촉각 유도 체결을 다룬다. 연구 프로그램에 따르면 무엇이 범위 안이고 무엇이
   범위 밖인가?

> [!tip]- 정답 · Answers
> 1. 같은 과제·같은 정책 구조에서의 비전만 ablation과 촉각만 ablation. 앞의 것이 없으면 이득이 촉각이 아니라 늘어난 네트워크 용량이나 늘어난 학습 신호에서 왔을 수 있고, 뒤의 것이 없으면 촉각이 과제를 지고 있는지 아니면 꼬리만 다듬고 있는지 알 수 없다. 모양이 다른 두 모델 사이의 성공률 차이는, 그 둘을 돌리기 전까지는 구조 비교다.
> 2. 초기 미끄러짐은 물체가 *아직 움직이지 않았다*는 것으로 정의되기 때문이다 — 접촉면의 중심은 아직 붙어 있고 가장자리만 부분적으로 미끄러진다. 물체의 운동을 보고하는 센서는 구조적으로 이미 늦었으므로, 조밀한 접촉 신호가 다른 모달리티에는 없는 정보를 주는 경우다. 같은 정보를 더 편하게 주는 것이 아니다.
> 3. 30 fps면 샘플이 33 ms마다 오는데, 단단한 접촉 천이는 1~2 밀리초에 끝난다([[04-robotics/force-compliance-control|13. §5]]) — 사건 전체가 두 프레임 사이에서 일어난다. 센서는 접촉이 *어땠는지*를 보고할 수 있고 그것은 다음 행동을 정하는 데 유용하지만, 충격 자체를 조절하는 데 참여할 수는 없다. 그 일은 수동 컴플라이언스와 킬로헤르츠 토크 루프의 몫이다.
> 4. 그리퍼 자신의 무게와 페이로드를 센서 프레임으로 사영해서 빼야 한다 — 그리고 그것은 팔의 방향에 의존한다. 중력은 월드 프레임에 고정되어 있고 센서는 손목과 함께 회전하기 때문이다. 같은 부재를 잡아도 자세마다 원 측정값이 다르므로, 중력 보상에는 현재 기구학이 필요하다([[02-foundations/manipulator-kinematics-dynamics|10. §5]]). 가속 중에는 관성 항도 들어온다.
> 5. 범위 안: 기존 촉각 센서를 써서 체결을 견고하게 만드는 것 — 접촉 상태 분류, 그것에 따라 행동하는 정책, 실제 체결구에 대한 평가. 범위 밖: 새 센서를 설계하거나 제작하는 것. [[07-research-program/index|§7]]이 이를 제외하는 이유는 그것이 자기 문헌과 자기 실패 모드를 가진 별개의 기여이기 때문이다.

### 출처

**센서**

- W. Yuan, S. Dong, E. H. Adelson, "GelSight: High-Resolution Robot Tactile Sensors for Estimating Geometry and Force," *Sensors*, vol. 17, no. 12, art. 2762, 2017. 광학 원리의 출처는 M. K. Johnson and E. H. Adelson, "Retrographic sensing for the measurement of surface texture and shape," CVPR 2009, pp. 1070–1077.
- M. Lambeta et al., "DIGIT: A Novel Design for a Low-Cost Compact High-Resolution Tactile Sensor With Application to In-Hand Manipulation," *IEEE RA-L*, vol. 5, no. 3, pp. 3838–3845, 2020 ([arXiv:2005.14679](https://arxiv.org/abs/2005.14679)).
- B. Ward-Cherrier et al., "The TacTip Family: Soft Optical Tactile Sensors with 3D-Printed Biomimetic Morphologies," *Soft Robotics*, vol. 5, no. 2, pp. 216–227, 2018.

**촉각을 쓰는 법**

- M. A. Lee, Y. Zhu, K. Srinivasan, et al., "Making Sense of Vision and Touch: Self-Supervised Learning of Multimodal Representations for Contact-Rich Tasks," ICRA 2019, pp. 8943–8950 ([arXiv:1810.10191](https://arxiv.org/abs/1810.10191)). 확장된 저널판은 **제목과 저자 목록이 다르다**: M. A. Lee, Y. Zhu, P. Zachares, et al., "Making Sense of Vision and Touch: Learning Multimodal Representations for Contact-Rich Tasks," *IEEE T-RO*, vol. 36, no. 3, pp. 582–596, 2020 — 따로 인용하라.
- R. Calandra et al., "More Than a Feeling: Learning to Grasp and Regrasp Using Vision and Touch," *IEEE RA-L*, vol. 3, no. 4, pp. 3300–3307, 2018 ([arXiv:1805.11085](https://arxiv.org/abs/1805.11085)).
- R. S. Johansson, J. R. Flanagan, "Coding and use of tactile signals from the fingertips in object manipulation tasks," *Nature Reviews Neuroscience* 10, pp. 345–359, 2009. DOI 10.1038/nrn2621 — the canonical account of the four mechanoreceptor types and what each carries.
- J. Tong, O. Mao, D. Goldreich, "Two-Point Orientation Discrimination Versus the Traditional Two-Point Test for Tactile Spatial Acuity Assessment," *Frontiers in Human Neuroscience* 7:579, 2013. DOI 10.3389/fnhum.2013.00579 — why the traditional two-point test overstates acuity, and what to use instead. Fingertip grating-orientation thresholds near 0.94 mm (lip and tongue nearer 0.5 mm) come from the grating-orientation literature this paper sits in.
- C. Higuera, A. Sharma, C. K. Bodduluri, et al., "Sparsh: Self-supervised touch representations for vision-based tactile sensing," *CoRL 2024* ([arXiv:2410.24090](https://arxiv.org/abs/2410.24090)) · [code](https://github.com/facebookresearch/sparsh) — touch backbones plus the TacBench benchmark.
- J. Zhao, N. Kuppuswamy, S. Feng, B. Burchfiel, E. Adelson, "PolyTouch: A Robust Multi-Modal Tactile Sensor for Contact-rich Manipulation Using Tactile-Diffusion Policies," *ICRA 2025* ([arXiv:2504.19341](https://arxiv.org/abs/2504.19341)) — includes an explicit elastomer durability comparison against a commercial GelSight Mini.

**서베이**

- Q. Li, O. Kroemer, Z. Su, et al., "A Review of Tactile Information: Perception and Action Through Touch," *IEEE T-RO*, vol. 36, no. 6, pp. 1619–1634, 2020 — 변환기가 아니라 인식-행동 루프를 축으로 구성되어 있어, 조작 연구에 들어오는 사람에게 맞는 방향이다.
- R. S. Dahiya, G. Metta, M. Valle, G. Sandini, "Tactile Sensing—From Humans to Humanoids," *IEEE T-RO*, vol. 26, no. 1, pp. 1–20, 2010 — 비전 기반·학습 시대 이전의, 변환 원리 중심 배경.

**이 위키 안에서**

- [[04-robotics/contact-force-tactile|접촉·힘·촉각 상호작용]] — 이 페이지가 딛고 선 마찰, 접촉 모드, 재료 상태.
- [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]] — 촉각을 무엇에 쓸 수 있고 없는지를 결정하는 시간 규모.
