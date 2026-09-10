# Foundations–Robotics audit: evaluation

- Date: 2026-09-09
- Commit audited: `e919cbd`
- Scope: `content/02-foundations/` (14 files), `content/04-robotics/` (44 files)
- Continues: `reviews/2026-09-09/FOUNDATIONS-ROBOTICS-HANDOFF.md`
- Nothing in `content/` was edited. `reference/` remains gitignored (191 PDFs, untracked).

## Answer to the three questions

**Can the target reader start studying now?** Yes. No blocking omission was found.

**Where must they follow an external textbook or course?** At Working level in three
places the wiki names itself: Modern Robotics summaries for calculation, the control
packet for derivation, and Oppenheim–Schafer for signal processing. These are declared
dependencies, not gaps.

**Is any missing topic serious enough to interrupt the prescribed path?** No. The one
finding that costs a reader real time is navigational, not curricular: three haptics
subpages are reachable only from the haptics index.

## 1. Blocking omissions

**None found.**

The brief's leading candidate — system identification — is not a blocking omission, and
the premise behind it needs correcting. The topic is thin *inside the audited scope*
because it lives in chapter 5. `content/05-construction-robotics/sim-to-real.md` §2 treats
it directly: identification fits simulator parameters to measured trajectories, with its
failure mode stated (overfits one machine and one operating condition) and anchored to a
real result (Egli RL's neural-network valve model carrying the M545 policy without
fine-tuning). Its §1 warning draws the parameter-error versus model-form-error line, which
is the same cut Underactuated Robotics Ch.18 makes as equation error versus simulation
error. Residual learning, domain randomization and privileged learning are covered
alongside.

Reachability from the audited tracks is real: twelve inbound links, from `rl-basics`
(which tells the reader to read it immediately after) and `legged-locomotion`.

What Underactuated Ch.18 has that the wiki does not: experiment design for identification,
online adaptation, and the kinematic-versus-inertial parameter split. Those are Working
level for someone *doing* identification, not literacy for someone reading a paper that
says it was done.

## 2. High-value improvements

Ordered by how much reader time each saves.

**2.1 Haptics reciprocal links — the one finding worth acting on.** *Actioned on 2026-09-09
with the user's explicit permission; see the closing note.* Inbound links from
outside the haptics track, as found:

| Page | Inbound from outside the track |
|---|---|
| `device-design-kinematics` | 0 |
| `experiments-readings` | 0 |
| `hapkit-lab-software` | 0 |
| `bilateral-teleoperation` | 1 — Teleoperation |
| `human-haptics-psychophysics` | 1 — Psychophysics |
| `tactile-display-design` | 1 — Contact/Force/Tactile |
| `rendering-sampling-stability` | 2 — Glossary, Contact/Force/Tactile |

The sharpest instance: `rendering-sampling-stability` is where sampled-data stability,
the virtual wall and Z-width live, and neither Signal Processing nor Control Theory points
at it. A reader who has just finished the sampling contract in Signal Processing §2 has no
route to the page where that contract becomes a stability problem. This is a missing edge,
not missing content.

**2.2 One link from dynamics to where parameters come from.**
`manipulator-kinematics-dynamics.md` says controllers carry a friction model that is
"fitted, not derived" and stops there. A pointer to `sim-to-real` §2 would close the chain
from sensor data through parameters to control without writing anything new.

**2.3 Name the law of large numbers once, if at all.** The operational content is present
and unusually good: `ml-practice` §4 separates σ from σ/√n, explains that one shrinks and
the other does not, notes they differ by a factor of two at n = 4, and tells the reader to
check the caption before comparing two papers' error bars. `experimental-design` §1 covers
the non-independence concern directly — "repeated frames from one robot run are not
thousands of independent trials" — with experimental units defined. The CLT is named once,
in Probability §3, as the reason noise models default to Gaussian. Only the name "law of
large numbers" is absent. Low value; the reasoning a paper requires is already there.

## 3. Optional specialization that should stay external

- Exact zero-order-hold discretization, Tustin, discrete PID design, sampling zeros.
- Robust/H-infinity, adaptive, sliding-mode and formal nonlinear control.
- Markov chain theory proper: transition matrices, stationary distributions, mixing. The
  Markov *property* is defined in Probability §5 and used correctly in the `rl-basics`
  Bellman derivation, which is what RL and world-model papers actually assume.
- Closed-chain kinematics. Declared optional in two places with a stated reason, which is
  the right way to omit something. Worth revisiting only if parallel mechanisms, cable
  robots or excavator boom linkages become a research target.
- Martingales and advanced random-process theory.

## 4. Independent usability

**Foundations: passes, with the limit it states about itself.** The ordering supports two
readers at once — deep learning via engineering math to networks to linear algebra to
calculus to probability to optimization to information theory, and robotics via
engineering math to linear algebra to probability to signal processing to SE(3) to
dynamics. Mathematics is never left as theory: eigenvalues arrive at stability, Jacobians
at backpropagation and velocity kinematics, least squares at calibration and estimation,
KKT at inverse kinematics and MPC, Fourier and sampling at sensors and haptic rendering.
It is a prerequisite refresher and a paper-reading bridge, not a first mathematics
textbook, and it says so.

**Robotics: passes as a research-literacy map.** Coverage runs kinematics, dynamics,
estimation and SLAM, geometric perception and calibration, planning through TAMP, classical
control with LQR/LQG and MPC, contact, force, compliance and tactile, systems and
deployment, HRI and safety, manipulation, navigation, locomotion, and now haptics and
bilateral teleoperation. Modern Robotics summaries and parts of the control track require
the linked textbook for calculation; that dependency is declared, not hidden.

## 5. Integration quality

Strong, and the semantics hold up where I sampled them rather than only the counts.

Link structure across the 58 pages: 1,145 internal links, 363 unique edges, 35 unique
Foundations→Robotics and 65 Robotics→Foundations.

The continuous-to-digital bridge the brief worried about already exists and is better than
distributed fragments. Signal Processing §2 is titled "Sampling — the contract between
continuous and digital" and carries Nyquist, an aliasing figure worked at 170 Hz sampled at
200 Hz, the anti-alias rule, sensor-rate selection against the fastest dynamics you must
observe, and quantization at roughly 6 dB per bit. Signal Processing §5 is titled "Bridge
to control" and states that poles of H are the eigenvalues of A, with stability as left
half-plane versus inside the unit circle. Control Theory §4 gives both clocks in one table
plus the map λ ↦ e^{λT} with a numeric check, and warns that papers switch clocks without
notice. Robot Systems §3 carries the latency budget. The edges connecting these exist in
both directions.

What distinguishes this wiki from a linked personal encyclopedia is that Robotics pages do
not merely cite a Foundations page as a prerequisite; they say what the same object means
once it reaches a robot paper.

## 6. Cognitive load

The longest pages are substantial: `rl-basics` 11,751 words, `force-compliance-control`
10,878, `linear-algebra` 9,232, `tactile-visuotactile` 9,037, `control-theory-ce397` 8,610.
These counts are English and Korean combined, so the load in one language is roughly half.

Every long page I checked carries a `First pass · 처음이라면` callout naming the sections to
read and the ones to defer, plus a `study-depth` label. `rl-basics` opens by saying it is
the longest page in the track and to read §6 early. The mitigation is systematic, and I
found no page where a first-time reader is left without a route.

## 7. Two statements to correct

Confirmed at these locations. Both are wording, not content.

| File | Line | Text |
|---|---|---|
| `04-robotics/control-theory-ce397.md` | 348 | "Every real implementation has anti-windup" |
| `04-robotics/control-theory-ce397.md` | 752 | "모든 실전 구현에 anti-windup이 있다" |
| `04-robotics/modern-robotics/ch11-robot-control.md` | 25 | "hence anti-windup in every real implementation" |
| `04-robotics/modern-robotics/ch11-robot-control.md` | 54 | "모든 실전 구현에 anti-windup이 있는 이유" |
| `04-robotics/control-theory-ce397.md` | 364 | "Practice: make the observer 2–5× faster" |
| `04-robotics/control-theory-ce397.md` | 767 | "제어기보다 2~5배 빠르게 만든다" |

Anti-windup is commonly required wherever integral action and actuator saturation coexist;
it is not a property every implementation has. The surrounding reading advice — ask whether
a paper's PID baseline has it — stays valid under the weaker claim.

Observer poles 2–5× faster than the controller is a rule of thumb. Its suitability depends
on measurement noise, unmodeled high-frequency dynamics, sampling rate and sensor
bandwidth; too fast an observer can be worse. It should read as a heuristic with those
conditions named.

Do not conflate this with the separate and correct "2–5" at line 176, which is a healthy
gain-margin range.

## 8. Verification performed

At commit `e919cbd`:

- `python3 scripts/verify_content.py` — 218 files, 0 problems
- `python3 scripts/audit_parity.py` — 0 English/Korean section-reference mismatches
- Underactuated Robotics Ch.18 fetched directly and its section list read, to ground the
  system-identification comparison rather than restate the brief

## 9. Limits of this audit

- The 13,171 reference pages were searched and compared by topic, not read
  sentence by sentence. No claim here rests on an unread page.
- The undefined-term detector in `audit_gaps.py` was not run; its n-gram pass is expensive
  and the brief records it as interrupted. That detector's result is unknown, not clean.
- Of the external benchmarks, only Underactuated Ch.18 was fetched in this session. The
  others are carried over from the brief's earlier checks.
- Link *counts* were computed mechanically; link *semantics* were sampled, concentrated on
  the continuous-to-digital chain and the haptics boundary, not exhaustively read.
- No numerical score is given, because no rubric defines one.

## 10. Change made after this evaluation

The user authorised acting on finding 2.1 only. Six reciprocal links were added, each in
both language halves, placed where the canonical page already owns the principle:

| From | To |
|---|---|
| Signal Processing §2 (sampling contract) | 24.4 Rendering, Sampling & Stability |
| Control Theory §4 (the two clocks) | 24.4 |
| Robot Systems §3 (latency budget) | 24.4 |
| Robot Systems §9 (staged deployment) | 24.6 Hapkit Lab & Real-Time Software |
| Force & Compliance §2 (impedance/admittance causality) | 24.3 Haptic Device Design & Kinematics |
| HRI & Safety §7 (human-study design) | 24.7 Experiments & Reading Map |

Every haptics subpage now has at least one inbound link from outside the track; the three
that had none no longer do, and `rendering-sampling-stability` went from two to five.
No other finding in this report was acted on. Verified after the edit: `verify_content.py`
218 files 0 problems, `audit_parity.py` 0 mismatches.

## 11. Second change: the Hapkit lab page removed

The user asked whether the Hapkit lab belonged in a research-literacy wiki and then ruled that
the lab material was not needed. Assessment and action:

- Measured against the wiki's stated purpose, `24.6 Hapkit Lab & Real-Time Software` was the
  only page whose centre of gravity was building rather than reading — the sole page using
  `Arduino`, and about half of it (kit parts list, board revision, an H-bridge pin conflict
  between two supplied documents, a CHAI3D/ROS 2 onboarding route) was semester-bound lab
  manual. Hapkit does not appear in papers, so it failed the wiki's own inclusion rule.
- Most of the rest was already in `24.4`, which carries the hard-real-time loop path in §1 and
  a debugging order in §6 that subsumes the bring-up ladder and the diagnostic table.
- Two items were genuinely orphaned and were rehomed rather than lost: the low-pass filter
  α-convention trap went to `02-foundations/signal-processing` §4, where filters live and
  where it serves paper reading directly; the explicit-versus-semi-implicit Euler point went
  to `24.4` §2 alongside the sampled-spring energy argument.
- The track is now six steps; Experiments & Reading Map moved from 24.7 to 24.6 and the fast
  route is 24.1 → 24.3 → 24.4. The `robot-systems` §9 link added earlier was repointed to
  `24.4` §6. Residual Hapkit mentions in the two index pages, the teleoperation scope note and
  the provenance table were corrected. The study log was appended to, not rewritten, because
  it is a dated historical record.
- Course originals remain in `reference/`, untracked.

Verified after the change: `verify_content.py` 217 files 0 problems, `audit_parity.py` 0
mismatches.

## 12. Third change: the last two recommendations applied

**Finding 2.2 — the dynamics page now says where its parameters come from.** Item 2 of the
parameter-honesty list said that real controllers carry a friction model that is "fitted, not
derived" and stopped there. It now names the fitting and its failure mode, with a link to
`05-construction-robotics/sim-to-real` §2. This closes the chain from sensor data through
identified parameters to control and sim-to-real, which §1 of this report argued was the only
thing missing about system identification — a link, not a chapter.

**Finding 7 — the two over-absolute control statements corrected, in all six places.**

| Statement | Now reads |
|---|---|
| "Every real implementation has anti-windup" | "Wherever integral action and actuator saturation coexist, anti-windup is needed" |
| "anti-windup in every real implementation" (MR ch.11) | "anti-windup wherever the actuator can saturate" |
| observer "2–5× faster" as practice | "a common rule of thumb", qualified by noise, unmodelled high-frequency dynamics, sampling rate and sensor bandwidth, and the note that past that bound a faster observer amplifies noise instead of settling sooner |

The surrounding reading advice was kept: a PID baseline without anti-windup is still called
unfairly weak, which holds under the weaker claim. The separate and correct "2–5" gain-margin
range at line 176 was not touched.

Verified: `verify_content.py` 217 files 0 problems, `audit_parity.py` 0 mismatches.

Every finding in this report has now been either acted on or explicitly left as optional
specialization. Nothing remains open.
