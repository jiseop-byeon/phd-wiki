---
title: "25.6 Describing a Robot: URDF, TF2 and RViz"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Write a robot description in Xacro, publish its frames with robot_state_publisher, read the resulting transform tree with view_frames, tf2_echo and RViz, and diagnose the two transform errors every beginner meets."
mastery-when: "Go deeper when you are writing the localisation or odometry component that owns the map and odom edges, rather than consuming the tree they produce."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to describe a robot, publish its frames correctly, and find out who is publishing a frame wrongly. Not enough to write a state estimator that owns `map`.
> **Working** — 로봇을 기술하고 프레임을 올바르게 publish하며, 어떤 프레임을 누가 잘못 내보내는지 찾아낼 정도. `map`을 소유하는 상태 추정기를 작성할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> A sourced **ROS 2 Jazzy Jalisco on Ubuntu 24.04** installation and a workspace you can build in ([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). The transient-local durability that keeps `/tf_static` alive (§6, §8) and the message timestamps every lookup asks about are [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]] and [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]] respectively. Rigid-body transforms help but are not required first: [[02-foundations/se3-geometry|3D Geometry & SE(3)]] and [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**와 빌드 가능한 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). `/tf_static`을 살려 두는 transient local durability(§6, §8)와 모든 조회가 묻는 메시지 타임스탬프는 각각 [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]]와 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에서 온다. 강체 변환은 도움이 되지만 먼저 읽을 필요는 없다: [[02-foundations/se3-geometry|3D Geometry & SE(3)]], [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].

> [!note] First pass · 처음이라면
> Read the Running object and the picture, then the Worked case; its three one-line glosses point you to §5, §8 and §10. Then §2 (links, joints and the tree rule), §7 (who owns an edge) and §8 (which time to ask for), and do the §12 exercise, which runs the Worked case on an arm you build. §1 is the motivation in one paragraph; §3–§6 and §9–§11 are reference you return to when a symptom sends you there; §13 is the failure to reproduce once the exercise runs.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], with the one thing P6 leaves open frozen here for the whole page: **the camera sits $0.10\,\mathrm{m}$ ahead of and $0.25\,\mathrm{m}$ above `base_link`, with its axes aligned to the cart's.** Every other number is P6's own: encoder $N=2048$ counts/m, control $200\,\mathrm{Hz}$, vision $50\,\mathrm{Hz}$, budget $70\,\mathrm{ms}$.

*Two objects, stated once.* The calculations are done on P6. The exercise (§12) and the failure (§13) build a **two-link arm** instead. The reason is that P6's URDF would hold only the fixed camera mount: its travel on the rail is not a URDF joint (§11), so there would be nothing to move in RViz. Each Worked-case step that can run on the arm does. Step 2's composition is `tf2_echo base_link link2` (§12, item 4); Step 3's typo is §12, item 6; Step 5's two owners are §13, at $10+20=30\,\mathrm{Hz}$ instead of $200+20$. Step 4 has no arm counterpart, because the sliders publish at $10\,\mathrm{Hz}$ and nothing on the arm carries a camera stamp.

### The picture: P6 as two trees and one clock

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="Left: the URDF tree, base_link with a fixed joint camera_mount at xyz 0.10 0 0.25 to camera_link, each link with visual, collision and inertial elements and their readers. Right: the TF chain map, odom, base_link, camera_link, with owners, topics and rates, the static mount edge drawn doubled. Bottom: a 0 to 70 ms lookup clock where a now() lookup points past the newest odom sample into empty space and a lookup with the message stamp lands 20 ms before it.">
  <defs><marker id="d6esol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="d6eopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">URDF tree: what robot_state_publisher reads</text>
  <rect x="12" y="32" width="250" height="66" rx="4" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none"/>
  <text x="22" y="48" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">base_link</text>
  <text x="28" y="64" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;visual&gt;</text>
  <text x="114" y="64" font-size="11" fill-opacity="0.75" fill="currentColor">RViz</text>
  <text x="28" y="78" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;collision&gt;</text>
  <text x="114" y="78" font-size="11" fill-opacity="0.75" fill="currentColor">planner, physics engine</text>
  <text x="28" y="92" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;inertial&gt;</text>
  <text x="114" y="92" font-size="11" fill-opacity="0.75" fill="currentColor">physics engine only</text>
  <line x1="38" y1="98" x2="38" y2="150" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none" marker-end="url(#d6esol)"/>
  <path d="M38 118l6 6l-6 6l-6 -6z" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.25"/>
  <text x="52" y="118" font-size="11" fill-opacity="0.9" fill="currentColor">joint <tspan font-family="ui-monospace,monospace">camera_mount</tspan> (fixed)</text>
  <text x="52" y="133" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">&lt;origin xyz="0.10 0 0.25"/&gt;</text>
  <rect x="12" y="152" width="250" height="66" rx="4" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none"/>
  <text x="22" y="168" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">camera_link</text>
  <text x="28" y="184" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;visual&gt;</text>
  <text x="114" y="184" font-size="11" fill-opacity="0.75" fill="currentColor">RViz</text>
  <text x="28" y="198" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;collision&gt;</text>
  <text x="114" y="198" font-size="11" fill-opacity="0.75" fill="currentColor">planner, physics engine</text>
  <text x="28" y="212" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;inertial&gt;</text>
  <text x="114" y="212" font-size="11" fill-opacity="0.75" fill="currentColor">physics engine only</text>
  <text x="12" y="238" font-size="11" fill-opacity="0.8" fill="currentColor">Not in it: the cart's travel on the rail.</text>
  <text x="12" y="252" font-size="11" fill-opacity="0.65" fill="currentColor">A mobile base's pose is not a URDF joint (§11).</text>
  <text x="292" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">TF tree: what lookup_transform answers from</text>
  <rect x="292" y="32" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="46" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">map</text>
  <rect x="292" y="92" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="106" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">odom</text>
  <rect x="292" y="162" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="176" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">base_link</text>
  <rect x="292" y="240" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="254" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">camera_link</text>
  <line x1="334" y1="53" x2="334" y2="90" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#d6esol)"/>
  <text x="388" y="69.5" font-size="11" fill="currentColor">localisation node</text>
  <text x="388" y="82.5" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf</tspan> · when it corrects</text>
  <line x1="334" y1="113" x2="334" y2="160" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#d6esol)"/>
  <text x="388" y="128" font-size="11" fill="currentColor">encoder odometry node</text>
  <text x="388" y="141" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf</tspan> · 200 Hz</text>
  <text x="388" y="154" font-size="11" fill-opacity="0.85" fill="currentColor">Δp = 1/2048 m = 0.488 mm</text>
  <line x1="331.5" y1="183" x2="331.5" y2="233" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="none"/>
  <line x1="336.5" y1="183" x2="336.5" y2="233" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="none"/>
  <path d="M327.0 231.0L334.0 239.0L341.0 231.0" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="388" y="195.5" font-size="11" fill="currentColor">static broadcaster</text>
  <text x="388" y="208.5" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf_static</tspan> · once</text>
  <text x="388" y="221.5" font-size="11" fill-opacity="0.85" fill="currentColor">transient local</text>
  <text x="388" y="234.5" font-size="11" fill-opacity="0.85" fill="currentColor">xyz 0.10 0 0.25 m</text>
  <text x="12" y="294" font-size="12" fill-opacity="0.8" fill="currentColor">Lookup clock, 0 to 70 ms</text>
  <text x="142" y="326" font-size="11" text-anchor="end" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">odom → base_link</text>
  <text x="142" y="354" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">vision stamps</text>
  <text x="142" y="388" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">4 control lookups</text>
  <text x="142" y="414" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">budget</text>
  <line x1="150" y1="322" x2="535" y2="322" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <circle cx="150" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="177.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="205" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="232.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="260" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="287.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="315" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="342.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="370" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="397.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="425" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="452.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="480" cy="322" r="3.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="480" cy="322" r="7" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="471" y="339" font-size="11" text-anchor="end" fill-opacity="0.85" fill="currentColor">newest</text>
  <path d="M481.0 313V309H506.5V313" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="535" y="305" font-size="11" text-anchor="end" fill-opacity="0.9" font-style="italic" fill="currentColor">extrapolation into the future</text>
  <line x1="150" y1="350" x2="535" y2="350" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <path d="M150.0 344v12M260.0 344v12M370.0 344v12M480.0 344v12" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.9" fill="none"/>
  <line x1="150" y1="384" x2="535" y2="384" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <path d="M421.0 388L425.0 381L429.0 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M448.5 388L452.5 381L456.5 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M476.0 388L480.0 381L484.0 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M503.5 388L507.5 381L511.5 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <line x1="507.5" y1="379" x2="507.5" y2="326" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.95" fill="none" marker-end="url(#d6esol)"/>
  <text x="513.5" y="368" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">now()</text>
  <line x1="478" y1="379" x2="371.5" y2="326" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none" marker-end="url(#d6esol)"/>
  <text x="430.5" y="368" font-size="11" text-anchor="end" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">msg.header.stamp</tspan> (20 ms back)</text>
  <line x1="150" y1="410" x2="535" y2="410" stroke="currentColor" stroke-width="2.4" stroke-opacity="0.8" fill="none"/>
  <line x1="150" y1="405" x2="150" y2="415" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.8" fill="none"/>
  <line x1="535" y1="405" x2="535" y2="415" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.8" fill="none"/>
  <text x="342.5" y="404" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">70 ms budget</text>
  <text x="150" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">0</text>
  <text x="205" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">10</text>
  <text x="260" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">20</text>
  <text x="315" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">30</text>
  <text x="370" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">40</text>
  <text x="425" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">50</text>
  <text x="480" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">60</text>
  <text x="535" y="440" font-size="11" text-anchor="end" fill-opacity="0.75" fill="currentColor">70 ms</text>
  <path d="M150.0 420v5M177.5 420v5M205.0 420v5M232.5 420v5M260.0 420v5M287.5 420v5M315.0 420v5M342.5 420v5M370.0 420v5M397.5 420v5M425.0 420v5M452.5 420v5M480.0 420v5M507.5 420v5M535.0 420v5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45" fill="none"/>
</svg>

Left is the URDF tree `robot_state_publisher` reads: one fixed joint `camera_mount` at the frozen offset, and no joint for the cart's travel on the rail. Right is the TF chain `lookup_transform` answers from, every edge labelled with owner, topic and rate — localisation on `/tf` when it corrects, encoder odometry on `/tf` at $200\,\mathrm{Hz}$ with $\Delta p=0.488\,\mathrm{mm}$, and the mount on `/tf_static`, sent once. On the $0$ to $70\,\mathrm{ms}$ lookup clock below, a lookup at `now()` points past the newest `odom` sample into empty space, *extrapolation into the future*, while one at the message's own stamp lands $20\,\mathrm{ms}$ back, where the buffer has data.

### Worked case: a detection from `camera_link` to `odom`, and what one typo costs

Five steps on the Running object. Every number is either P6's or the frozen mount offset.

**Step 1 — where the cart is, from the encoder.** The `odom` → `base_link` edge carries the plant's own measurement, so its value and its resolution are

$$p=\frac{c}{N}=\frac{c}{2048}\,\mathrm{m},\qquad \Delta p=\frac{1}{2048}=0.488\,\mathrm{mm}$$

because a count is the smallest change the encoder can report. Take the instant where the encoder reads $c=1024$: the cart is at $p=0.5\,\mathrm{m}$, and no transform anywhere downstream can be finer than half a millimetre.

**Step 2 — compose the chain.** A detector running on the camera reports a target at $x=0.40\,\mathrm{m}$ in `camera_link`. The chain is

$$ {}_{\text{odom}}T_{\text{target}} = {}_{\text{odom}}T_{\text{base}}\cdot{}_{\text{base}}T_{\text{cam}}\cdot{}_{\text{cam}}T_{\text{target}} $$

and tf2 walks it for you across the three owners. Here every frame is axis-aligned, so the rotations are identity and the composition collapses to addition along $x$: $0.40+0.10=0.50\,\mathrm{m}$ in `base_link`, then $0.50+0.50=1.00\,\mathrm{m}$ in `odom`. Write the two additions down separately, because they come from two different places — the middle term is a fixed number in your URDF, the outer term is a live measurement from the encoder, and only one of them can be wrong quietly.

**Step 3 — and it is the fixed one.** Xacro is the macro language you write the description in, expanded to plain URDF before anything reads it, and urdfdom is the library that parses that URDF (§5). Section 5's warning is about a typo xacro cannot catch: write `xzy=` for `xyz=` and urdfdom ignores the attribute rather than failing, leaving the joint at a zero offset. The chain then yields

$$0.40+0.00+0.50=0.90\,\mathrm{m}\quad\text{instead of}\quad 1.00\,\mathrm{m}$$

so the error is exactly the lost mount offset, $0.10\,\mathrm{m}$ along $x$ (and $0.25\,\mathrm{m}$ in $z$) — which, in the units the rest of the system speaks, is $0.10\times2048=204.8$, about **205 encoder counts** of pure fiction on a cart whose encoder resolves $0.488\,\mathrm{mm}$. Nothing logs, RViz draws a robot that looks plausible, and the arm reaches ten centimetres short forever. Expand the xacro to a file and read the number whenever a result is *wrong*, not only when something is *missing*.

**Step 4 — which time to ask for.** A listener keeps a time-indexed history of every edge it hears, the buffer, and `lookup_transform`'s third argument says which instant in it to answer for; `Time()` means the newest entry (§8). The buffer holds `odom` → `base_link` samples $5\,\mathrm{ms}$ apart and `base_link` → `camera_link` once, so the three ways of calling `lookup_transform` behave very differently on P6:

| Third argument | What it means here | Cost against the $70\,\mathrm{ms}$ budget |
|---|---|---|
| `self.get_clock().now()` | a time past the newest sample, since transforms always arrive late | fails with *extrapolation into the future* |
| `Time()` | the latest available, at most one control period ($5\,\mathrm{ms}$) old | $7.1\%$ of the budget, and it answers the wrong question for a detection |
| `msg.header.stamp` | where the frames were when the image was captured, up to one vision period ($20\,\mathrm{ms}$) back | $28.6\%$ of the budget, and it is the correct answer |

The middle row is the one to argue about. `Time()` is right for "where is the cart now"; the stamp is right for "where was the cart when this pixel was exposed", which is what transforming a detection means. Interpolating between two samples $5\,\mathrm{ms}$ apart is exact to within one encoder count as long as the cart moves slower than $\Delta p/T_{\text{ctrl}}=0.488\,\mathrm{mm}/5\,\mathrm{ms}=0.0977\,\mathrm{m/s}$; above that the interpolation is smoothing real motion, which is a bound worth knowing before trusting a number to a tenth of a millimetre.

**Step 5 — one edge, two owners.** Add a state estimator that also broadcasts `odom` → `base_link`, at $20\,\mathrm{Hz}$, beside the encoder odometry node at $200\,\mathrm{Hz}$. Nothing refuses, nothing warns, and `view_frames` — the tool that draws the whole tree and labels each edge with its average rate and a Broadcaster field (§10) — reports

$$200+20=220\,\mathrm{Hz}$$

on an edge you believe is published at $200$, because tf2 keeps one buffer per *child* frame and does not record who sent a sample. The Broadcaster field will say `default_authority` and tell you nothing; the rate is the only tell. A lookup then interpolates between whichever two samples bracket the requested time regardless of authorship, so if the two publishers disagree by a centimetre the transform alternates between two answers at a rate nobody chose. Section 13 reproduces exactly this, and section 7's rule — one publisher per parent–child edge — is the thing that prevents it.

### 1. Why a robot needs a machine-readable description

Everything after this page needs to know where things are. A planner needs to know that the gripper is 0.8 m from the base when the elbow is at 1.2 rad. A collision checker needs shapes. A physics engine needs masses and inertias. A perception node that gets a point in the camera frame needs to express it in the base frame before the arm can reach for it. RViz needs to know what to draw and where.

You could hard-code all of that in every node. Then the day someone lengthens the forearm by 2 cm, six nodes are wrong and three of them fail silently.

ROS 2's answer splits the problem in two, and the split is the thing to remember:

- **URDF** is the *static* description — which links exist, how they are connected, what they look like, what they weigh. It does not change while the robot runs.
- **TF2** is the *live* answer — where every frame actually is right now, and where it was 0.3 seconds ago when that camera image was captured.

`robot_state_publisher` is the bridge: it reads the URDF once, subscribes to joint angles, and publishes the resulting frames into TF2 continuously.

### 2. URDF: a tree of links and joints

URDF (Unified Robot Description Format) is XML. It has exactly two structural elements.

A **link** is a rigid body. It carries appearance, collision shape and mass properties, and it defines a coordinate frame.

A **joint** connects exactly two links — a `parent` and a `child` — and says how the child may move relative to the parent. Its `<origin xyz="..." rpy="..."/>` (`xyz` a translation in metres, `rpy` roll, pitch and yaw: rotations about x, y and z in radians) is the fixed offset from the parent link's frame to the joint, and it is where most of the geometry of a robot actually lives.

The constraint that follows: **the links and joints must form a tree.** Every link has at most one parent joint; there is exactly one root link; no cycles. A parallel mechanism — a delta robot, a four-bar linkage — cannot be expressed as URDF, and that is a real limitation, not a beginner's misunderstanding. The common workarounds are to model the open chain and close the loop in the physics engine, or to use SDF (Simulation Description Format, the format Gazebo reads natively) instead.

Units are SI throughout, per REP 103: metres, radians, kilograms. Frames are right-handed, and the body convention is x forward, y left, z up.

Getting the tree drawn on paper before writing XML saves more time than any other habit on this page. Once it is written, check it:

```bash
sudo apt install liburdfdom-tools
check_urdf my_robot.urdf
```

`check_urdf` parses the file and prints the link tree. If it prints one root and the links you expect, the structure is right; if a link is missing from the printout, its joint is wrong.

### 3. The joint types

| Type | Motion | Needs `<axis>` | Needs `<limit>` | Appears in `joint_states` |
|---|---|---|---|---|
| `fixed` | none | no | no | no |
| `revolute` | rotation about the axis, bounded | yes | yes (`lower`, `upper` in rad, plus `effort`, `velocity`) | yes |
| `continuous` | rotation about the axis, unbounded | yes | no | yes |
| `prismatic` | translation along the axis, bounded | yes | yes (`lower`, `upper` in m, plus `effort`, `velocity`) | yes |
| `planar` | two translations plus a rotation in a plane | yes | — | not as one number |
| `floating` | unconstrained, six degrees of freedom | no | — | not as one number |

Three practical notes. A wheel is `continuous`, not `revolute`, because a bounded wheel stops rolling at its limit. A `revolute` joint without a `<limit>` tag will not parse. And `fixed` joints are not decoration — a sensor mount is a `fixed` joint, and that is what makes the sensor's data transformable into the base frame at all.

`planar` and `floating` cannot be described by a single scalar, so `joint_state_publisher` and `robot_state_publisher` do not handle them the way they handle the other three movable types; a floating base is normally published as a transform by an odometry or localisation node instead.

### 4. Visual, collision and inertial — and the mesh that wrecks your planner

A link has up to three sub-elements, and beginners conflate them:

```xml
<link name="forearm">
  <visual>
    <origin xyz="0 0 0.2"/>
    <geometry><mesh filename="package://my_robot/meshes/forearm.dae"/></geometry>
    <material name="grey"/>
  </visual>
  <collision>
    <origin xyz="0 0 0.2"/>
    <geometry><cylinder radius="0.04" length="0.4"/></geometry>
  </collision>
  <inertial>
    <mass value="1.2"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</link>
```

- `<visual>` is what a human sees. Its accuracy costs nothing but rendering.
- `<collision>` is what the collision checker and the physics engine query. Its accuracy costs *every query*.
- `<inertial>` is mass and the 3×3 rotational inertia tensor, symmetric so six numbers suffice. Only simulation and dynamics use it.

**The trap: reusing the detailed visual mesh as the collision geometry.** The official URDF tutorial states the reason plainly — collision detection between two meshes is far more computationally complex than between two primitives. A motion planner samples and checks thousands of configurations per query, and a physics engine runs a narrow-phase check every step at 1 kHz. A 50,000-triangle CAD export in `<collision>` multiplies that cost by orders of magnitude, and the symptom is not an error: it is a planner that times out, a simulation whose real-time factor sits at 0.05, and a controller that misses its period. Use primitives — box, cylinder, sphere — or a convex decomposition, and make them slightly larger than the visual rather than slightly smaller. The same element doubles as a safety envelope: a cylinder that encases a sensor head keeps planned paths away from it.

On inertia: the tutorial's guidance is that a matrix with `ixx`/`iyy`/`izz` of `1e-3` or smaller is a reasonable default for a mid-sized link, and that the identity matrix is a particularly bad choice — it corresponds to a 0.1 m box weighing 600 kg. Inertias of zero or near-zero make a simulated model collapse without warning, with every link's origin snapping to the world origin. If you ever see that in Gazebo, look at `<inertial>` first.

### 5. Xacro: properties, macros, and how it is expanded

A URDF for a real robot repeats itself relentlessly: the same cylinder written in `<visual>` and `<collision>`, the same leg written twice with a sign flipped, joint origins computed by hand from link lengths. Xacro is an XML macro language that removes that repetition. It gives you three things: **properties** (constants), **arithmetic**, and **macros**.

The file must declare the namespace; without it xacro refuses to parse the file ("unbound prefix"):

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">
  <xacro:property name="link_len" value="0.4"/>
  <cylinder radius="0.03" length="${link_len}"/>
  <origin xyz="0 0 ${link_len/2}" rpy="0 ${pi/2} 0"/>
</robot>
```

`${...}` substitutes a property or evaluates an expression; `+ - * /`, unary minus, parentheses, `sin`, `cos` and the constant `pi` are available. Substitution works inside any attribute and composes with literal text, so `<link name="${prefix}_leg"/>` is how you get two similarly named links from one macro.

Macros take parameters. In the simplest case a parameter is a value, used inside the macro with `${...}` exactly like a property:

```xml
<xacro:macro name="default_inertial" params="mass">
  <inertial>
    <mass value="${mass}"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</xacro:macro>
<xacro:default_inertial mass="10"/>
```

A second kind exists: a parameter prefixed with `*` is an XML *block* that the caller supplies and `<xacro:insert_block>` inserts. You will meet it in larger descriptions; the value form above is enough to start.

> [!warning] The silent Xacro failure
> A typo in a macro name is loud, not silent: `handle_macro_call` raises `XacroException("unknown macro name: ...")`, xacro exits non-zero and produces no output at all. Typos in property and parameter names are loud too: an undefined property in `${...}` raises "name ... is not defined", and a misspelled macro parameter raises "Invalid parameter".
>
> What *is* silent is a typo in a URDF attribute xacro does not check — `xzy=` for `xyz=` — which urdfdom ignores, leaving you with a joint at a zero offset. Expand to a file and read it whenever a number looks wrong rather than whenever something is missing.

Xacro is a preprocessor: nothing downstream understands it. Expansion happens one of two ways.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
```

That is the debugging path — run it and read the output whenever the robot is not what you expected. The production path runs xacro inside the launch file so the URDF is never stale on disk, as the official `urdf_launch` package does:

```python
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
```

The `value_type=str` matters: without it the parameter is guessed at, and a URDF that begins with a number or parses as something else will arrive at the wrong type.

### 6. What robot_state_publisher and joint_state_publisher_gui actually do

`robot_state_publisher` is the node that turns the static description plus live joint angles into live frames. Per its documentation:

- It takes the URDF through the `robot_description` **parameter**, which must be set at startup or the node fails to start.
- It subscribes to `joint_states` (`sensor_msgs/msg/JointState`).
- **Fixed** joints are published once at startup to `/tf_static`, on a transient-local topic so any later subscriber still receives them.
- **Movable** joints are published to `/tf` whenever the relevant joint appears in a `joint_states` message, rate-limited by the `publish_frequency` parameter, which defaults to 20.0 Hz.
- It also republishes the URDF itself on a transient-local `robot_description` topic, which is how RViz and `joint_state_publisher` get the model without being given the file.
- `frame_prefix` (default empty) prefixes every published frame, which is the standard way to run two identical robots in one graph.

It does *not* invent joint angles. With no `joint_states` publisher, the movable part of the tree never appears, and RViz shows the base link alone. On a real robot the joint states come from the hardware driver or from `ros2_control` ([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). With no robot at all, you supply them by hand:

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

This node reads the model — in ROS 2 it subscribes to the `/robot_description` topic — finds every non-fixed joint and its limits, and gives you one slider per joint. Moving a slider publishes a `JointState` message; `robot_state_publisher` recomputes the chain; RViz redraws. It is a stand-in for a robot, and nothing more: it is a debugging tool, not part of a running system. Leaving it in a launch file that also starts a real driver gives you two publishers of `joint_states` fighting each other.

### 7. TF2: the frame tree, and who owns an edge

TF2 is the library that answers "where is frame A relative to frame B, at time t". It is where most newcomer hours are lost, so be precise about four things.

**Frames form a tree, not a graph.** Each frame has exactly one parent and any number of children. There is one root. This is not a style rule; it is what makes a lookup a unique path.

**Direction.** Two facts, kept apart:

- *Publishing* names parent then child: `header.frame_id` is the parent, `child_frame_id` is the child.
- *Looking up* names where the data should end up, then where it starts: `lookup_transform(target_frame, source_frame, time)` returns the transform that takes data *expressed in* `source_frame` and gives it *expressed in* `target_frame`.

The trap is between them. The tf2 concept documentation warns that the published `geometry_msgs/msg/Transform` is the *frame* formulation, the inverse of the data formulation. The library inverts as needed while it walks the tree, so it does not make this sign error; you will, the first time you write a transform by hand.

Composition along the chain is what the tree buys you. For a two-link arm,

$$ {}_{\text{base}}T_{\text{tip}} = {}_{\text{base}}T_{\text{link1}} \cdot {}_{\text{link1}}T_{\text{tip}} $$

and TF2 walks that product for you across any number of edges published by any number of nodes.

**Exactly one publisher may own a given parent–child edge.** Internally tf2 keeps one time-ordered buffer per *child* frame. It is keyed by the child frame alone — not by who sent the data. Two nodes publishing the same edge therefore interleave their samples into one buffer, and a lookup interpolates between whichever neighbouring samples bracket the requested time, regardless of authorship. If the two disagree, the frame alternates between two answers. Section 13 reproduces this on purpose.

**Broadcasting is cheap and local.** Any node can broadcast any edge. Nothing checks, at any point, that the tree you intended is the tree you got. The tools in section 10 are the check.

### 8. Static and dynamic transforms, the buffer, and the time argument

A **static** transform never changes: base to laser mount, base to camera. It goes on `/tf_static`, which is published with transient-local durability, so it is sent once and every later subscriber still receives it. Publish it with the dedicated executable rather than writing code:

```bash
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id mystaticturtle
```

All arguments except `--frame-id` and `--child-frame-id` are optional and default to identity, and `--qx --qy --qz --qw` is accepted instead of roll/pitch/yaw. Every value goes after its named flag, exactly as above. (A line of six or nine bare numbers, as in older tutorials, is the older form; do not copy it.)

A **dynamic** transform changes and is stamped every time: odom to base_link, and every movable joint of your arm. It goes on `/tf` and is republished continuously.

A listener does not read those topics directly. It fills a **buffer** — a time-indexed cache, 10 seconds deep by default — and queries it:

```python
from rclpy.duration import Duration
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)

t = self.tf_buffer.lookup_transform('base_link', 'link2', Time())
```

The third argument is the part that decides whether your node works.

- `Time()` in Python (`tf2::TimePointZero` in C++) means **the latest available transform**, not "now". This is what you want for a live query, and what the official debugging tutorial gives as the correct fix.
- An actual timestamp — typically `msg.header.stamp` from the sensor message you are transforming — means "where were these frames when this image was taken". This is the whole point of a buffer, and it is what makes a transformed detection correct on a moving robot instead of 100 ms stale.
- `self.get_clock().now()` means "now", and **now has not happened yet** as far as the buffer is concerned. Transforms arrive with a delay. Section 9 is the error this produces.

Add a `timeout` to block briefly rather than fail on the first miss, which is what you want in a startup path:

```python
t = self.tf_buffer.lookup_transform('base_link', 'link2', Time(), timeout=Duration(seconds=0.05))
```

### 9. The two errors everyone meets

**A frame that does not exist.** The message is unambiguous:

```text
"turtle3" passed to lookupTransform argument target_frame does not exist
```

It means what it says. The cause is almost always a typo, a missing `frame_prefix`, or a publisher that has not started yet. Confirm it with `tf2_echo`, which reports the same thing from `canTransform`, and then look at what frames *do* exist with `view_frames`.

**A lookup that would require extrapolation into the future.**

```text
Could not transform turtle2 to turtle1: Lookup would require extrapolation into the future.
Requested time 1630223704.617054 but the latest data is at time 1630223704.616726, when
looking up transform from frame [turtle1] to frame [turtle2]
```

Read the two numbers: the request is *later* than the newest sample in the buffer, here by about 0.3 ms. The buffer will not extrapolate, by design — a made-up transform is worse than no transform. The cause is asking for `now`. The diagnostic is `tf2_monitor`, which reports the delay of the chain between two frames:

```bash
ros2 run tf2_ros tf2_monitor turtle2 turtle1
```

It prints the chain, the net average and maximum delay, and the rate of each broadcaster. If the net delay is 3 ms, then `now` will fail most of the time and `now - 0.1 s` will work — but that is a diagnosis, not a fix. The fix is `Time()` for "latest", or the message's own stamp with a timeout. Reaching for a hard-coded delay means you have papered over a question you have not answered.

The mirror-image error, `Lookup would require extrapolation into the past`, means the request is older than the buffer, which is either a stale sensor stamp or a buffer that needs to be constructed with a longer `cache_time`.

### 10. Looking at the tree: view_frames, tf2_echo and RViz

Three tools, each better at a different question.

```bash
sudo apt install ros-jazzy-tf2-tools ros-jazzy-tf2-ros graphviz
ros2 run tf2_tools view_frames
```

`view_frames` subscribes for five seconds (change it with `--wait-time`), then renders the whole tree with Graphviz. In Jazzy it writes `frames_<date>_<time>.gv` and `frames_<date>_<time>.pdf` into the current directory — not the `frames.pdf` that older tutorials mention — and `-o NAME` overrides the name. It is the only tool that answers "what is the shape of my tree", and each edge is labelled with the broadcaster, the average rate, the buffer length, and the most recent and oldest transform times. Those labels are the diagnostic content; read them, not just the arrows.

```bash
ros2 run tf2_ros tf2_echo [source_frame] [target_frame]
```

`tf2_echo` prints one edge or chain repeatedly: translation, rotation as quaternion and as RPY in radians and degrees, and the full 4×4 matrix. A quaternion is a four-number encoding of a rotation; if it is unfamiliar, read the RPY line first, and see [[02-foundations/se3-geometry|3D Geometry & SE(3)]] §2 for how the two relate. Use it to answer "is this number right", and to catch a sign or axis error that looks fine in a picture.

RViz answers "does this look like my robot". Start it, set **Fixed Frame** to a frame that actually exists (with `Fixed Frame` set to something unpublished, every display fails at once and the errors point everywhere but the cause), then add two displays:

- **RobotModel**, whose *Description Source* is `Topic` by default. The *Description Topic* field has **no default** — RViz renames the inherited topic property but sets no value — so pick `/robot_description` from its dropdown. Until you do, the display is simply empty and says nothing, which is the commonest "my robot does not show up" report. The topic is transient-local, so it needs no file path once `robot_state_publisher` is running. Its *Visual Enabled* and *Collision Enabled* checkboxes draw the two geometries separately, which is how you see that your collision shape is the 50,000-triangle mesh. *Mass* and *Inertia* draw the inertial properties.
- **TF**, which draws every frame with axes, names, and arrows from child to parent. *Frames* lists them all with checkboxes, *Tree* shows the parent–child structure, and *Frame Timeout* controls how long a frame that has stopped updating stays drawn before fading to grey and disappearing — a frame fading out in RViz means its publisher died.

### 11. REP 105: map, odom and base_link

For mobile platforms the frame names and their order are standardised by REP 105, and every navigation stack assumes it:

```text
map --> odom --> base_link
```

- `base_link` is rigidly attached to the robot base, at whatever point on the base is an obvious reference.
- `odom` is a world-fixed frame whose origin is wherever the robot started. The robot's pose in `odom` is **continuous** — it evolves smoothly, with no discrete jumps — but it **drifts without bound**, because it is computed by integrating wheel encoders, visual odometry or an IMU.
- `map` is a world-fixed frame with z up. The robot's pose in `map` does **not drift** over time, because a localisation component keeps recomputing it from sensor observations, but it is **not continuous**: it can jump discretely whenever new sensor information arrives.

That is the trade you cannot escape, and it is why both frames exist. Use `odom` for anything local and short-term — a velocity controller, obstacle avoidance over the next second, anything that would be destabilised by a pose that jumps 30 cm sideways. Use `map` for anything long-term and global — "go to the kitchen" — where drift would eventually put you in the wrong room.

On P6 the trade has sizes. `odom` → `base_link` is the encoder itself, $p=c/2048$, so it moves in $0.488\,\mathrm{mm}$ steps and never jumps. Suppose a localisation fix — the camera seeing the rail's end stop — puts the cart at $1.000\,\mathrm{m}$ while odometry says $0.990\,\mathrm{m}$ (an illustrative gap, not a catalog number). The localisation node then publishes a `map` → `odom` correction of $0.010\,\mathrm{m}$, about $20$ counts. At that instant the cart's pose in `map` jumps by $10\,\mathrm{mm}$ and its pose in `odom` does not move, so the $200\,\mathrm{Hz}$ controller, which reads `odom`, sees no jump at all.

The structure surprises people: intuition says both `map` and `odom` should be parents of `base_link`, but a frame may have only one parent, so REP 105 makes `map` the parent of `odom` instead. The consequence is that the localisation node does not publish the robot's pose directly; it publishes the `map` → `odom` correction, which is the accumulated drift of the odometry. Odometry publishes `odom` → `base_link`. Neither ever publishes the other's edge — that is section 7's rule applied to the most important edges in the system. Everything from `base_link` downward comes from `robot_state_publisher` reading your URDF.

Above `map` sits an optional `earth` frame (ECEF), present only when several robots with separate maps have to be related.

### 12. Exercise: a two-link arm in Xacro, moving in RViz

One sitting. Baseline is ROS 2 Jazzy on Ubuntu 24.04.

```bash
sudo apt install ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui ros-jazzy-robot-state-publisher ros-jazzy-rviz2 ros-jazzy-tf2-tools liburdfdom-tools graphviz
```

Write `two_link_arm.urdf.xacro`:

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">

  <material name="grey">
    <color rgba="0.6 0.6 0.6 1"/>
  </material>

  <xacro:property name="link_len" value="0.4"/>
  <xacro:property name="link_rad" value="0.03"/>

  <xacro:macro name="default_inertial" params="mass">
    <inertial>
      <mass value="${mass}"/>
      <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
    </inertial>
  </xacro:macro>

  <xacro:macro name="arm_link" params="name">
    <link name="${name}">
      <visual>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
      </collision>
      <xacro:default_inertial mass="1.0"/>
    </link>
  </xacro:macro>

  <link name="base_link"/>
  <xacro:arm_link name="link1"/>
  <xacro:arm_link name="link2"/>

  <joint name="shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  </joint>

  <joint name="elbow" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 ${link_len}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="2.0" effort="10.0" velocity="1.0"/>
  </joint>

</robot>
```

Expand it and check the structure before running anything:

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
check_urdf two_link_arm.urdf
```

Read the expanded URDF once. The two `arm_link` calls produced two full link definitions, and `${link_len/2}` became `0.2`. That is all xacro is.

Now `display.launch.py`, following the `urdf_launch` pattern from section 5:

```python
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', output='screen'),
    ])
```

```bash
ros2 launch ./display.launch.py
```

In RViz set **Fixed Frame** to `base_link`, add a **RobotModel** display and a **TF** display. Then:

1. Drag the two sliders. The cylinders move and the TF axes move with them. `shoulder` rotates about y, so the arm swings in the x–z plane.
2. `ros2 topic echo /joint_states` — two names, two positions, changing as you drag.
3. `ros2 topic echo /tf_static --once` — prints `transforms: []`. `robot_state_publisher` always publishes its static list at startup, and every joint here is movable, so the list is empty. Add a `fixed` joint for a sensor mount and an entry appears.
4. `ros2 run tf2_ros tf2_echo base_link link2` with both sliders at zero. The translation should be `[0, 0, 0.4]` — `link2`'s origin sits at the *end* of `link1`, which is what the elbow joint's `<origin>` says. Move the shoulder to 1.57 and watch x and z swap.
5. `ros2 run tf2_tools view_frames`, then open the generated PDF. Three frames, two edges, each with a rate near 10 Hz. The *Broadcaster* field reads `default_authority` on every edge: in ROS 2 a listener cannot learn which node sent a transform, so that field carries no information. That 10 is `joint_state_publisher`'s `rate` default — `robot_state_publisher` only republishes what it receives, and its own `publish_frequency` default of 20 Hz is a *maximum*, not a target.
6. **The Worked case's Step 3, on the arm.** In the xacro, change the elbow joint's `<origin xyz="0 0 ${link_len}" .../>` to `xzy=`. Expand it and run `check_urdf`: it still passes. Relaunch and repeat item 4. `tf2_echo base_link link2` now prints `[0, 0, 0]` where it printed `[0, 0, 0.4]`, so the error is exactly the lost offset, `link_len` $=0.4\,\mathrm{m}$. At zero the two cylinders lie on top of each other, and nothing logs. Put `xyz=` back.

You are done when you can predict, before looking, what `tf2_echo base_link link2` will print for a given pair of slider values.

### 13. The failure to diagnose: two publishers on one edge

Leave the exercise running and add a second owner of `base_link` → `link1` — one that publishes *different* values with its own timestamps. That last condition matters: a second `robot_state_publisher` reading the same `/joint_states` produces transforms identical in value and stamp, and tf2 silently drops exact duplicates, so nothing would happen at all.

```bash
# a SECOND robot_state_publisher, fed from its own joint-state topic
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -r __node:=robot_state_publisher_b -r joint_states:=joint_states_b \
  -p robot_description:="$(xacro two_link_arm.urdf.xacro)"
# in another terminal: hold the second publisher's shoulder at zero, 20 times a second
ros2 topic pub /joint_states_b sensor_msgs/msg/JointState \
  "{header: {stamp: now}, name: [shoulder, elbow], position: [0.0, 0.0]}" --rate 20
```

**Symptom.** Move the shoulder slider away from zero. In RViz, `link1` and everything below it — `link2`, the whole rest of the arm — jitters or snaps between the slider pose and the zero pose. A listener node computing a grasp from this tree gets a different answer each cycle, and averaging makes it worse, not better. Nothing logs an error. Both publishers are behaving exactly as told.

**Mechanism.** From section 7: tf2 stores one time-ordered buffer per child frame, keyed by the child frame alone. Both publishers' samples land in the buffer for `link1`, interleaved in time, and a lookup interpolates between whichever neighbouring samples bracket the requested time — sometimes two from the slider, sometimes one from each, sometimes two zeros. (Mixing a static and a dynamic publisher on one frame is worse still: the buffer type differs for static and dynamic frames, so alternating messages of the two kinds make tf2 reallocate the frame's cache, discarding history.)

**The command that finds it.**

```bash
ros2 run tf2_tools view_frames
```

Open the PDF and read the `base_link` → `link1` edge label:

- **Average rate** is roughly the sum of both publishers, not the rate you expect from one. Here that is about 30 Hz on an edge that should be about 10 Hz — the tell.
- **Broadcaster** is no help: in ROS 2 it reads `default_authority` for every publisher, so it can neither name nor count them.

Then confirm which nodes are actually publishing:

```bash
ros2 topic info /tf --verbose
ros2 topic info /tf_static --verbose
```

`--verbose` lists every endpoint by node name ([[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]] introduced the flag). Two publishers on `/tf` where you expected one, or a `static_transform_publisher` on `/tf_static` claiming a frame your URDF also owns, ends the investigation.

**The fix is architectural, not a tuning knob.** Decide which node owns each edge and delete the other publisher. The realistic versions of this bug are: a `static_transform_publisher` left in a launch file for a frame the URDF later gained a joint for; two launch files each starting their own `robot_state_publisher`; a localisation node and a bag playback both publishing `map` → `odom`; or a driver publishing `odom` → `base_link` while an EKF publishes the same edge. The last one is the reason robot_localization publishes `map` → `odom` and tells the wheel driver to stop broadcasting.

### 14. What this page does not cover

Driving the joints for real — controllers, hardware interfaces, and the Gazebo Harmonic side of the URDF — is [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]], which also covers the `<transmission>` and `<ros2_control>` tags this page skipped, and the SDF format Gazebo uses natively. Timestamps, the `use_sim_time` parameter and the executor that decides when your TF callback runs are [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]] — and TF2's transient-local `/tf_static` is a QoS story the moment a subscriber gets it wrong. Packaging the description properly, with `package://` mesh paths that resolve after installation, is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. The mathematics that `lookup_transform` is doing for you is [[02-foundations/se3-geometry|3D Geometry & SE(3)]] and [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]]. Everything above this sits in [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Tutorials/Intermediate/URDF: Building a movable robot model; Adding physical and collision properties; Using Xacro to clean up your code; Using URDF with `robot_state_publisher`.
- ROS 2 Jazzy documentation — Tutorials/Intermediate/Tf2: Introducing tf2; Writing a static broadcaster (Python); Debugging tf2 problems.
- ROS 2 Jazzy documentation — Concepts/Intermediate: Tf2 (transform direction and `lookupTransform` semantics).
- `robot_state_publisher` package README (jazzy) — parameters, published and subscribed topics.
- `geometry2` source (jazzy) — `tf2/src/buffer_core.cpp` and `tf2/src/cache.cpp` for per-child-frame buffering and broadcaster recording; `tf2_tools/view_frames.py` for output file naming and edge labels.
- `rviz_default_plugins` source (jazzy) — RobotModel and TF display properties.
- REP 105, Coordinate Frames for Mobile Platforms; REP 103, Standard Units of Measure and Coordinate Conventions.
- `urdf_launch` package — `description.launch.py` and `display.launch.py`.

### Self-check

1. Your node calls `lookup_transform('odom', 'camera_link', self.get_clock().now())` and
   logs "extrapolation into the future" most cycles. What is wrong, and what are the two
   correct fixes?
2. Why can't `map` and `odom` both be parents of `base_link`, and what does the localisation
   node publish instead?
3. Your planner takes 40 seconds per query on a robot whose URDF loads fine and looks right
   in RViz. Where do you look first?
4. `view_frames` shows `default_authority` on every edge. How do you tell that an edge has
   two publishers?
5. On P6, a detector reports a target at $x=0.40\,\mathrm{m}$ in `camera_link` while the
   encoder reads $1024$ counts. Where is the target in `odom`, which two numbers did you have
   to trust, and what does a `xzy=` typo in the mount origin cost — in metres and in counts?

> [!tip]- Answers
> 1. It is asking for a time the buffer has not received data for yet; transforms always arrive with some delay. Use `Time()` (`tf2::TimePointZero`) to get the latest available transform, or — better, when transforming sensor data — use that message's own `header.stamp`, with a short `timeout` so the call waits rather than failing on the first miss. Subtracting a hard-coded 0.1 s is a diagnostic, not a fix.
> 2. A tf2 frame has exactly one parent, which is what makes a lookup a unique path. REP 105 therefore chains `map` → `odom` → `base_link`: odometry owns `odom` → `base_link`, and localisation publishes the `map` → `odom` correction, which is the accumulated odometry drift. `odom` is continuous but drifts; `map` does not drift but jumps.
> 3. The `<collision>` elements. If they reuse the detailed visual meshes, every one of the thousands of collision checks per query is mesh-versus-mesh instead of primitive-versus-primitive. Turn off *Visual Enabled* and turn on *Collision Enabled* in RViz's RobotModel display to see what the checker is actually using, then replace the meshes with primitives or a convex decomposition.
> 4. The Broadcaster field carries no information in ROS 2 — listeners cannot learn who sent a transform. Read the average rate instead: an edge you expect at 10 Hz reporting about 30 Hz has more than one owner. Confirm with `ros2 topic info /tf --verbose` and `/tf_static`. (Two publishers sending *identical* transforms with identical stamps do not show up at all, because tf2 drops exact duplicates — and they also do no harm.)
> 5. At $x=1.00\,\mathrm{m}$, at the mount height $z=0.25\,\mathrm{m}$: the frames are axis-aligned, so the chain collapses to $0.40+0.10+0.50$, where $0.10\,\mathrm{m}$ is the frozen mount offset carried on `/tf_static` from the URDF and $0.50=1024/2048$ is the live encoder measurement on `odom` → `base_link`. Those are the two numbers you trusted, and only the first can be wrong silently: urdfdom ignores an unrecognised `xzy=` attribute instead of failing, so the offset becomes zero, the answer becomes $0.90\,\mathrm{m}$, and the error is exactly $0.10\,\mathrm{m}$ along $x$ (plus $0.25\,\mathrm{m}$ in $z$) — $0.10\times2048=204.8$, about $205$ counts on an encoder that resolves $0.488\,\mathrm{mm}$. Expand the xacro and read the number; nothing else reports it.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]]. Cart frame `base_link`, camera on the cart, encoder $N=2048$ counts/m. Vision $50\,\mathrm{Hz}$, control $200\,\mathrm{Hz}$. No new simulator.

1. **Draw.** TF tree `map` → `odom` → `base_link` → `camera_link`. Who owns each edge? Mark encoder counts on `odom` → `base_link` and vision on `camera_link`. Five-line timeline: the $200\,\mathrm{Hz}$ `odom` → `base_link` TF updates and four $200\,\mathrm{Hz}$ lookups, one of them with `now()`.
2. **Derive.** (a) Encoder $\Delta p$ for one count — the resolution of `odom` → `base_link`. (b) Why `lookup_transform(..., now())` from the controller logs "extrapolation into the future". (c) Two publishers on `odom` → `base_link` at $50\,\mathrm{Hz}$ and $200\,\mathrm{Hz}$. What rate does `view_frames` report?
3. **Interpret.** The controller must transform a detection whose camera stamp is $200\,\mathrm{ms}$ old, inside a $70\,\mathrm{ms}$ budget. Which two fixes does §9 give for *extrapolation into the future*, which one is wrong for P6's force loop, and what should the loop do with the detection?

> [!note]- How to draw it · 그리는 법
> - Four frames in one chain, `map` → `odom` → `base_link` → `camera_link`, with three labels on every edge: owner, topic, rate.
> - `map` → `odom`: the localisation node, `/tf`, published when it corrects. `odom` → `base_link`: the encoder odometry node, `/tf`, $200\,\mathrm{Hz}$ — write the encoder resolution on this edge.
> - `base_link` → `camera_link`: a static broadcaster, `/tf_static`, published once, transient local — write the frozen mount offset on this edge.
> - Draw the two `/tf` edges as solid arrows and the `/tf_static` edge as a doubled one: "republished forever" against "sent once and kept for late joiners" is the difference between a working RViz and an empty one.
> - Write beside the chain what is deliberately not in the URDF: the cart's travel on the rail. A mobile base's pose is not a URDF joint (§11); its edge belongs to the odometry node.
> - On the clock: `odom` → `base_link` samples every $5\,\mathrm{ms}$ with the newest one marked, vision stamps at $0, 20, 40, 60\,\mathrm{ms}$, the four control lookups, and the $70\,\mathrm{ms}$ budget.
> - Draw the `now()` lookup landing right of the newest sample and label the gap *extrapolation into the future*; draw a lookup at the message's own stamp landing back at that stamp ($20\,\mathrm{ms}$ left of the newest sample in the picture above).
> - The drawing is right when the `now()` arrow visibly points into empty space.

> [!tip]- Solutions
> 1. Localisation owns `map` → `odom`; odometry (encoder) owns `odom` → `base_link`; a static broadcaster owns `base_link` → `camera_link`. Timeline: `odom` → `base_link` TF every $5\,\mathrm{ms}$ (the camera mount is static and never updates); lookups at $0,5,10,15$; the `now()` lookup sits in the future of the buffer.
> 2. (a) $0.488\,\mathrm{mm}$. (b) Transforms arrive late; `now()` is a time the buffer has not seen. Use `Time()` or the message stamp. (c) About $250\,\mathrm{Hz}$ — two owners.
> 3. Latest available (`Time()`), or the *message* stamp with a short timeout. Subtracting a hard-coded $0.1\,\mathrm{s}$ is a diagnostic. `Time()` is the wrong one here: it composes the $200\,\mathrm{ms}$-old detection with a pose at most $5\,\mathrm{ms}$ old, so the target is placed as if the image had been taken from where the cart is now, and nothing in the result shows the age. The message stamp gives the correct transform and keeps the age in view: $200\,\mathrm{ms}$ is already $130\,\mathrm{ms}$ over the $70\,\mathrm{ms}$ budget — drop the detection, do not extrapolate it.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 로봇을 기술하고 프레임을 올바르게 publish하며, 어떤 프레임을 누가 잘못 내보내는지 찾아낼 정도. `map`을 소유하는 상태 추정기를 작성할 정도는 아니다.
> **Working** — enough to describe a robot, publish its frames correctly, and find who publishes a frame wrongly.

> [!note] 선수 지식 · Prerequisites
> source된 **Ubuntu 24.04 위 ROS 2 Jazzy Jalisco**와 빌드할 수 있는 워크스페이스([[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]). `/tf_static`을 살려 두는 transient local durability(§6, §8)와 모든 조회가 묻는 메시지 타임스탬프는 각각 [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]]와 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에서 온다. 강체 변환은 도움이 되지만 선행 조건은 아니다: [[02-foundations/se3-geometry|3D Geometry & SE(3)]], [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]].
> A sourced ROS 2 Jazzy on Ubuntu 24.04 and a buildable workspace; transient-local durability and timestamps from 25.5; rigid-body transforms help but are not required.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상과 그림을 보고 Worked case로 가라. 그 안의 한 줄 설명 셋이 §5, §8, §10을 가리킨다. 그다음 §2(링크, 조인트, 트리 규칙), §7(간선의 소유자), §8(어느 시각을 물을지)을 읽고 §12 실습을 하라. 실습은 Worked case를 직접 만든 팔 위에서 돌린다. §1은 한 문단짜리 동기이고, §3–§6과 §9–§11은 증상이 그리로 보낼 때 돌아와 찾는 참고 자료이며, §13은 실습이 돌아간 뒤 재현할 고장이다.

### 이 페이지의 대상 · Running object

대상은 [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** 카트이고, P6이 정하지 않는 것 하나를 여기서 페이지 끝까지 고정한다: **카메라는 `base_link`보다 $0.10\,\mathrm{m}$ 앞, $0.25\,\mathrm{m}$ 위에 있고 축은 카트와 정렬되어 있다.** 나머지 숫자는 모두 P6의 것이다: 엔코더 $N=2048$ counts/m, 제어 $200\,\mathrm{Hz}$, 비전 $50\,\mathrm{Hz}$, 예산 $70\,\mathrm{ms}$.

*대상이 둘이라는 것을 한 번 밝혀 둔다.* 계산은 P6 위에서 한다. 실습(§12)과 고장(§13)은 대신 **2링크 팔** 하나를 만든다. P6의 URDF에는 고정된 카메라 장착 하나만 들어가기 때문이다. 레일 위 카트의 이동은 URDF 조인트가 아니므로(§11) RViz에서 움직일 것이 없다. Worked case의 단계 중 팔에서 돌릴 수 있는 것은 팔에서 돌린다. 2단계의 합성은 `tf2_echo base_link link2`(§12의 4번), 3단계의 오타는 §12의 6번, 5단계의 소유자 둘은 §13이며 주기는 $200+20$이 아니라 $10+20=30\,\mathrm{Hz}$다. 4단계에는 팔 쪽 짝이 없다. 슬라이더는 $10\,\mathrm{Hz}$로 publish하고 팔에는 카메라 스탬프를 단 것이 없기 때문이다.

### 그림으로 먼저 보기: 트리 둘과 시계 하나로 본 P6 · The picture

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="왼쪽: URDF 트리. base_link에서 xyz 0.10 0 0.25의 fixed 조인트 camera_mount를 지나 camera_link로, 링크마다 visual, collision, inertial 요소와 그것을 읽는 쪽. 오른쪽: map, odom, base_link, camera_link의 TF 사슬과 소유자·토픽·주기, 정적 장착 간선은 겹친 화살표. 아래: 0에서 70 ms 조회 시계. now() 조회는 가장 새 odom 샘플을 지나 빈 공간을 가리키고, 메시지 스탬프 조회는 그보다 20 ms 앞에 떨어진다.">
  <defs><marker id="d6ksol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="d6kopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">URDF 트리: robot_state_publisher가 읽는 것</text>
  <rect x="12" y="32" width="250" height="66" rx="4" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none"/>
  <text x="22" y="48" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">base_link</text>
  <text x="28" y="64" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;visual&gt;</text>
  <text x="114" y="64" font-size="11" fill-opacity="0.75" fill="currentColor">RViz</text>
  <text x="28" y="78" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;collision&gt;</text>
  <text x="114" y="78" font-size="11" fill-opacity="0.75" fill="currentColor">플래너, 물리 엔진</text>
  <text x="28" y="92" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;inertial&gt;</text>
  <text x="114" y="92" font-size="11" fill-opacity="0.75" fill="currentColor">물리 엔진만</text>
  <line x1="38" y1="98" x2="38" y2="150" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none" marker-end="url(#d6ksol)"/>
  <path d="M38 118l6 6l-6 6l-6 -6z" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.25"/>
  <text x="52" y="118" font-size="11" fill-opacity="0.9" fill="currentColor">조인트 <tspan font-family="ui-monospace,monospace">camera_mount</tspan> (fixed)</text>
  <text x="52" y="133" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">&lt;origin xyz="0.10 0 0.25"/&gt;</text>
  <rect x="12" y="152" width="250" height="66" rx="4" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none"/>
  <text x="22" y="168" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" font-weight="bold" fill="currentColor">camera_link</text>
  <text x="28" y="184" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;visual&gt;</text>
  <text x="114" y="184" font-size="11" fill-opacity="0.75" fill="currentColor">RViz</text>
  <text x="28" y="198" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;collision&gt;</text>
  <text x="114" y="198" font-size="11" fill-opacity="0.75" fill="currentColor">플래너, 물리 엔진</text>
  <text x="28" y="212" font-size="11" fill-opacity="0.85" font-family="ui-monospace,monospace" fill="currentColor">&lt;inertial&gt;</text>
  <text x="114" y="212" font-size="11" fill-opacity="0.75" fill="currentColor">물리 엔진만</text>
  <text x="12" y="238" font-size="11" fill-opacity="0.8" fill="currentColor">여기 없는 것: 레일 위의 카트 이동.</text>
  <text x="12" y="252" font-size="11" fill-opacity="0.65" fill="currentColor">이동 베이스의 자세는 URDF 조인트가 아니다(11절).</text>
  <text x="292" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">TF 트리: lookup_transform이 답하는 근거</text>
  <rect x="292" y="32" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="46" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">map</text>
  <rect x="292" y="92" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="106" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">odom</text>
  <rect x="292" y="162" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="176" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">base_link</text>
  <rect x="292" y="240" width="84" height="20" rx="8" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="334" y="254" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">camera_link</text>
  <line x1="334" y1="53" x2="334" y2="90" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#d6ksol)"/>
  <text x="388" y="69.5" font-size="11" fill="currentColor">위치추정 노드</text>
  <text x="388" y="82.5" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf</tspan> · 보정할 때마다</text>
  <line x1="334" y1="113" x2="334" y2="160" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#d6ksol)"/>
  <text x="388" y="128" font-size="11" fill="currentColor">엔코더 오도메트리 노드</text>
  <text x="388" y="141" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf</tspan> · 200 Hz</text>
  <text x="388" y="154" font-size="11" fill-opacity="0.85" fill="currentColor">Δp = 1/2048 m = 0.488 mm</text>
  <line x1="331.5" y1="183" x2="331.5" y2="233" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="none"/>
  <line x1="336.5" y1="183" x2="336.5" y2="233" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.9" fill="none"/>
  <path d="M327.0 231.0L334.0 239.0L341.0 231.0" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="388" y="195.5" font-size="11" fill="currentColor">정적 브로드캐스터</text>
  <text x="388" y="208.5" font-size="11" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/tf_static</tspan> · 한 번</text>
  <text x="388" y="221.5" font-size="11" fill-opacity="0.85" fill="currentColor">transient local</text>
  <text x="388" y="234.5" font-size="11" fill-opacity="0.85" fill="currentColor">xyz 0.10 0 0.25 m</text>
  <text x="12" y="294" font-size="12" fill-opacity="0.8" fill="currentColor">조회 시계, 0에서 70 ms</text>
  <text x="142" y="326" font-size="11" text-anchor="end" fill-opacity="0.8" font-family="ui-monospace,monospace" fill="currentColor">odom → base_link</text>
  <text x="142" y="354" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">비전 스탬프</text>
  <text x="142" y="388" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">제어 조회 넷</text>
  <text x="142" y="414" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">예산</text>
  <line x1="150" y1="322" x2="535" y2="322" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <circle cx="150" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="177.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="205" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="232.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="260" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="287.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="315" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="342.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="370" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="397.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="425" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="452.5" cy="322" r="2.6" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="480" cy="322" r="3.4" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.9"/>
  <circle cx="480" cy="322" r="7" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="471" y="339" font-size="11" text-anchor="end" fill-opacity="0.85" fill="currentColor">가장 새 샘플</text>
  <path d="M481.0 313V309H506.5V313" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="535" y="305" font-size="11" text-anchor="end" fill-opacity="0.9" font-style="italic" fill="currentColor">extrapolation into the future</text>
  <line x1="150" y1="350" x2="535" y2="350" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <path d="M150.0 344v12M260.0 344v12M370.0 344v12M480.0 344v12" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.9" fill="none"/>
  <line x1="150" y1="384" x2="535" y2="384" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.3" fill="none"/>
  <path d="M421.0 388L425.0 381L429.0 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M448.5 388L452.5 381L456.5 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M476.0 388L480.0 381L484.0 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <path d="M503.5 388L507.5 381L511.5 388z" stroke="currentColor" stroke-width="1" stroke-opacity="0.9" fill="currentColor" fill-opacity="0.6"/>
  <line x1="507.5" y1="379" x2="507.5" y2="326" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.95" fill="none" marker-end="url(#d6ksol)"/>
  <text x="513.5" y="368" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">now()</text>
  <line x1="478" y1="379" x2="371.5" y2="326" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.85" fill="none" marker-end="url(#d6ksol)"/>
  <text x="430.5" y="368" font-size="11" text-anchor="end" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">msg.header.stamp</tspan> (20 ms 전)</text>
  <line x1="150" y1="410" x2="535" y2="410" stroke="currentColor" stroke-width="2.4" stroke-opacity="0.8" fill="none"/>
  <line x1="150" y1="405" x2="150" y2="415" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.8" fill="none"/>
  <line x1="535" y1="405" x2="535" y2="415" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.8" fill="none"/>
  <text x="342.5" y="404" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">70 ms 예산</text>
  <text x="150" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">0</text>
  <text x="205" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">10</text>
  <text x="260" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">20</text>
  <text x="315" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">30</text>
  <text x="370" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">40</text>
  <text x="425" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">50</text>
  <text x="480" y="440" font-size="11" text-anchor="middle" fill-opacity="0.75" fill="currentColor">60</text>
  <text x="535" y="440" font-size="11" text-anchor="end" fill-opacity="0.75" fill="currentColor">70 ms</text>
  <path d="M150.0 420v5M177.5 420v5M205.0 420v5M232.5 420v5M260.0 420v5M287.5 420v5M315.0 420v5M342.5 420v5M370.0 420v5M397.5 420v5M425.0 420v5M452.5 420v5M480.0 420v5M507.5 420v5M535.0 420v5" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45" fill="none"/>
</svg>

왼쪽은 `robot_state_publisher`가 읽는 URDF 트리로, 고정된 오프셋의 fixed 조인트 `camera_mount` 하나뿐이고 레일 위 카트의 이동에 해당하는 조인트는 없다. 오른쪽은 `lookup_transform`이 답하는 근거인 TF 사슬로 간선마다 소유자·토픽·주기를 적었다 — 위치추정은 보정할 때마다 `/tf`로, 엔코더 오도메트리는 $200\,\mathrm{Hz}$ `/tf`로(해상도 $\Delta p=0.488\,\mathrm{mm}$), 장착은 `/tf_static`으로 한 번. 아래 $0$에서 $70\,\mathrm{ms}$ 조회 시계에서 `now()`로 한 조회는 가장 새 `odom` 샘플을 지나 빈 공간을 가리키고(*extrapolation into the future*), 메시지 자신의 스탬프로 한 조회는 버퍼에 데이터가 있는 $20\,\mathrm{ms}$ 전에 떨어진다.

### 대상으로 한 번 끝까지: `camera_link`의 검출을 `odom`으로, 그리고 오타 하나의 값 · Worked case

이 페이지의 대상 위에서 다섯 단계. 모든 숫자는 P6의 것이거나 고정한 장착 오프셋이다.

**1단계 — 엔코더가 말하는 카트의 위치**. `odom` → `base_link` 간선이 장치 자신의 측정값을 나르므로 그 값과 해상도는

$$p=\frac{c}{N}=\frac{c}{2048}\,\mathrm{m},\qquad \Delta p=\frac{1}{2048}=0.488\,\mathrm{mm}$$

한 카운트가 엔코더가 보고할 수 있는 최소 변화이기 때문이다. 엔코더가 $c=1024$를 읽는 순간을 잡으면 카트는 $p=0.5\,\mathrm{m}$에 있고, 하류의 어떤 변환도 $0.5\,\mathrm{mm}$보다 정밀할 수 없다.

**2단계 — 사슬을 합성한다**. 카메라 위에서 도는 검출기가 `camera_link` 기준 $x=0.40\,\mathrm{m}$에 표적을 보고한다. 사슬은

$$ {}_{\text{odom}}T_{\text{target}} = {}_{\text{odom}}T_{\text{base}}\cdot{}_{\text{base}}T_{\text{cam}}\cdot{}_{\text{cam}}T_{\text{target}} $$

이고 tf2가 소유자 셋을 가로질러 대신 걸어 준다. 여기서는 모든 프레임의 축이 정렬되어 회전이 항등이므로 합성이 $x$ 방향 덧셈으로 무너진다. `base_link`에서 $0.40+0.10=0.50\,\mathrm{m}$, 그다음 `odom`에서 $0.50+0.50=1.00\,\mathrm{m}$. 두 덧셈을 따로 적어라. 출처가 다르기 때문이다. 가운데 항은 URDF에 박힌 고정 숫자이고 바깥 항은 엔코더의 살아 있는 측정값인데, 조용히 틀릴 수 있는 쪽은 하나뿐이다.

**3단계 — 그리고 그 하나는 고정된 쪽이다**. xacro는 로봇 기술을 쓰는 매크로 언어로, 누가 읽기 전에 평범한 URDF로 전개된다. urdfdom은 그 URDF를 파싱하는 라이브러리다(§5). 5절의 경고가 xacro가 잡지 못하는 오타 이야기였다. `xyz=`를 `xzy=`로 쓰면 urdfdom은 실패하는 대신 그 속성을 무시하고, 조인트 오프셋은 0이 된다. 그러면 사슬은

$$0.40+0.00+0.50=0.90\,\mathrm{m}$$

를 내놓는다. 원래 답은 $1.00\,\mathrm{m}$였으므로 오차는 정확히 잃어버린 장착 오프셋, $x$로 $0.10\,\mathrm{m}$(그리고 $z$로 $0.25\,\mathrm{m}$)이다. 시스템 나머지가 쓰는 단위로 옮기면 $0.10\times2048=204.8$, 곧 $0.488\,\mathrm{mm}$를 분해하는 카트 위의 **엔코더 205 카운트짜리 허구**다. 로그는 조용하고, RViz는 그럴듯한 로봇을 그리고, 팔은 영원히 10센티미터 못 미쳐 닿는다. 무언가 *빠졌을* 때만이 아니라 결과가 *틀렸을* 때 xacro를 파일로 전개해 숫자를 읽어라.

**4단계 — 어느 시각을 물을 것인가**. 리스너는 들은 간선마다 시간으로 색인한 이력, 곧 버퍼를 쌓고, `lookup_transform`의 세 번째 인자는 그 안의 어느 순간에 대해 답할지를 정한다. `Time()`은 가장 새 항목을 뜻한다(§8). 버퍼에는 `odom` → `base_link` 샘플이 $5\,\mathrm{ms}$ 간격으로, `base_link` → `camera_link`는 한 번 들어 있다. 그래서 `lookup_transform`의 세 가지 호출이 P6에서는 아주 다르게 굴러간다.

| 세 번째 인자 | 여기서의 뜻 | $70\,\mathrm{ms}$ 예산에 대한 값 |
|---|---|---|
| `self.get_clock().now()` | 변환은 언제나 늦게 오므로 가장 새 샘플보다 뒤의 시각 | *extrapolation into the future*로 실패 |
| `Time()` | 가장 최근 값, 최대 제어 주기 하나($5\,\mathrm{ms}$)만큼 낡음 | 예산의 $7.1\%$. 다만 검출에는 틀린 질문 |
| `msg.header.stamp` | 이미지가 잡힌 순간의 프레임 배치, 최대 비전 주기 하나($20\,\mathrm{ms}$) 이전 | 예산의 $28.6\%$. 그리고 이것이 맞는 답 |

다툴 만한 것은 가운데 행이다. "카트가 지금 어디인가"에는 `Time()`이 맞고, "이 픽셀이 노출된 순간 카트가 어디였나"에는 스탬프가 맞는데, 검출을 변환한다는 것은 후자를 뜻한다. $5\,\mathrm{ms}$ 떨어진 두 샘플 사이의 보간은 카트가 $\Delta p/T_{\text{ctrl}}=0.488\,\mathrm{mm}/5\,\mathrm{ms}=0.0977\,\mathrm{m/s}$보다 느리게 움직이는 한 엔코더 한 카운트 안에서 정확하다. 그보다 빠르면 보간이 실제 운동을 뭉개는 것이고, 어떤 숫자를 $0.1\,\mathrm{mm}$ 단위까지 믿기 전에 알아 둘 만한 한계다.

**5단계 — 간선 하나에 소유자 둘**. $200\,\mathrm{Hz}$의 엔코더 오도메트리 노드 옆에, `odom` → `base_link`를 $20\,\mathrm{Hz}$로 함께 내보내는 상태 추정기를 붙여 보자. 아무도 거부하지 않고 아무도 경고하지 않으며, 트리 전체를 그리고 간선마다 평균 주기와 Broadcaster 칸을 적어 주는 도구인 `view_frames`(§10)는

$$200+20=220\,\mathrm{Hz}$$

를 보고한다. $200$으로 알고 있던 간선에 대해서다. tf2는 *자식* 프레임마다 버퍼 하나를 두고 누가 보냈는지는 기록하지 않기 때문이다. Broadcaster 칸은 `default_authority`라고만 적히고 아무것도 알려 주지 않는다. 단서는 주기뿐이다. 그리고 조회는 요청 시각을 끼고 있는 두 샘플 사이를 저자와 무관하게 보간하므로, 두 퍼블리셔가 1센티미터쯤 어긋나 있으면 변환은 아무도 고르지 않은 주기로 두 답을 오간다. 13절이 바로 이것을 재현하고, 7절의 규칙 — 부모-자식 간선마다 퍼블리셔 하나 — 이 그것을 막는 장치다.

### 1. 로봇에 기계가 읽을 수 있는 기술(description)이 필요한 이유

이 페이지 이후의 모든 것은 물건이 어디에 있는지를 알아야 한다. 플래너는 팔꿈치가 1.2 rad일 때 그리퍼가 베이스에서 0.8 m라는 것을 알아야 하고, 충돌 검사기는 형상을, 물리 엔진은 질량과 관성을 필요로 한다. 카메라 프레임의 점을 받은 인식 노드는 팔이 뻗기 전에 그것을 base 프레임으로 옮겨야 한다. RViz는 무엇을 어디에 그릴지 알아야 한다.

이걸 노드마다 하드코딩할 수는 있다. 그러면 누군가 전완 길이를 2 cm 늘린 날 여섯 개 노드가 틀리고 그중 셋은 조용히 실패한다.

ROS 2의 답은 문제를 둘로 나눈다. 그 분할이 기억할 대상이다.

- **URDF**는 *정적* 기술이다 — 어떤 링크가 있고, 어떻게 연결되고, 어떻게 생겼고, 무게가 얼마인지. 로봇이 도는 동안 바뀌지 않는다.
- **TF2**는 *실시간* 답이다 — 지금 모든 프레임이 실제로 어디에 있는지, 그리고 저 카메라 이미지가 찍힌 0.3초 전에는 어디에 있었는지.

`robot_state_publisher`가 다리다. URDF를 한 번 읽고, 조인트 각도를 구독하고, 그 결과 프레임을 TF2로 계속 내보낸다.

### 2. URDF: 링크와 조인트의 트리

URDF(Unified Robot Description Format)는 XML이다. 구조 요소는 정확히 둘이다.

**링크(link)** 는 강체다. 외형, 충돌 형상, 질량 특성을 담고, 좌표 프레임을 정의한다.

**조인트(joint)** 는 정확히 두 링크 — `parent`와 `child` — 를 잇고, 자식이 부모에 대해 어떻게 움직일 수 있는지 말한다. `<origin xyz="..." rpy="..."/>`(`xyz`는 미터 단위 병진, `rpy`는 roll·pitch·yaw, 즉 x·y·z축에 대한 라디안 단위 회전)는 부모 링크 프레임에서 조인트까지의 고정 오프셋이며, 로봇 기하의 대부분이 실제로 여기에 들어 있다.

여기서 따라오는 제약: **링크와 조인트는 트리를 이루어야 한다.** 모든 링크는 부모 조인트를 최대 하나 갖고, 루트 링크는 정확히 하나이며, 순환은 없다. 델타 로봇이나 4절 링크 같은 병렬 기구는 URDF로 표현할 수 없다. 이것은 초심자의 오해가 아니라 실제 한계다. 흔한 우회는 열린 사슬로 모델링하고 물리 엔진에서 루프를 닫거나, SDF(Simulation Description Format, Gazebo가 기본으로 읽는 형식)를 쓰는 것이다.

단위는 REP 103에 따라 전부 SI다: 미터, 라디안, 킬로그램. 프레임은 오른손 좌표계이고, 본체 관례는 x 전방, y 좌측, z 상방이다.

XML을 쓰기 전에 트리를 종이에 그려 두는 습관이 이 페이지의 어떤 것보다 시간을 아껴 준다. 다 썼으면 확인한다.

```bash
sudo apt install liburdfdom-tools
check_urdf my_robot.urdf
```

`check_urdf`는 파일을 파싱하고 링크 트리를 찍는다. 루트 하나와 기대한 링크들이 나오면 구조는 맞다. 출력에서 링크가 빠져 있으면 그 조인트가 틀린 것이다.

### 3. 조인트 타입

| 타입 | 운동 | `<axis>` 필요 | `<limit>` 필요 | `joint_states`에 등장 |
|---|---|---|---|---|
| `fixed` | 없음 | 아니오 | 아니오 | 아니오 |
| `revolute` | 축 둘레 회전, 제한 있음 | 예 | 예 (`lower`, `upper`는 rad, 그리고 `effort`, `velocity`) | 예 |
| `continuous` | 축 둘레 회전, 무제한 | 예 | 아니오 | 예 |
| `prismatic` | 축 방향 병진, 제한 있음 | 예 | 예 (`lower`, `upper`는 m, 그리고 `effort`, `velocity`) | 예 |
| `planar` | 평면 안에서 병진 둘 + 회전 하나 | 예 | — | 숫자 하나로는 아님 |
| `floating` | 구속 없음, 6자유도 | 아니오 | — | 숫자 하나로는 아님 |

실무 메모 셋. 바퀴는 `revolute`가 아니라 `continuous`다. 제한이 걸린 바퀴는 한계에서 구르기를 멈춘다. `<limit>` 태그 없는 `revolute`는 파싱되지 않는다. 그리고 `fixed`는 장식이 아니다. 센서 마운트가 `fixed` 조인트이고, 그것이 있어야 센서 데이터를 base 프레임으로 옮길 수 있다.

`planar`와 `floating`은 스칼라 하나로 기술할 수 없어서, `joint_state_publisher`와 `robot_state_publisher`가 나머지 가동 타입처럼 다루지 않는다. 부유 베이스는 보통 오도메트리나 위치추정 노드가 변환으로 publish한다.

### 4. visual, collision, inertial — 그리고 플래너를 망치는 메시

링크는 하위 요소를 최대 셋 갖는다. 초심자는 이 셋을 뭉뚱그린다.

```xml
<link name="forearm">
  <visual>
    <origin xyz="0 0 0.2"/>
    <geometry><mesh filename="package://my_robot/meshes/forearm.dae"/></geometry>
    <material name="grey"/>
  </visual>
  <collision>
    <origin xyz="0 0 0.2"/>
    <geometry><cylinder radius="0.04" length="0.4"/></geometry>
  </collision>
  <inertial>
    <mass value="1.2"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</link>
```

- `<visual>`은 사람이 보는 것이다. 정밀해도 렌더링 비용뿐이다.
- `<collision>`은 충돌 검사기와 물리 엔진이 질의하는 것이다. 정밀함의 대가를 *질의마다* 치른다.
- `<inertial>`은 질량과 3×3 회전 관성 텐서다. 대칭이라 여섯 수면 충분하다. 시뮬레이션과 동역학만 쓴다.

**함정: 정밀한 visual 메시를 collision 형상으로 재사용하는 것.** 공식 URDF 튜토리얼이 이유를 분명히 적는다 — 메시 대 메시 충돌 검사는 원시 도형 둘 사이보다 계산 복잡도가 훨씬 크다. 모션 플래너는 질의마다 수천 개 구성을 샘플링해 검사하고, 물리 엔진은 매 스텝 1 kHz로 좁은 단계 검사를 돈다. 삼각형 5만 개짜리 CAD 출력이 `<collision>`에 들어가면 그 비용이 자릿수 단위로 뛰고, 증상은 에러가 아니다. 시간 초과하는 플래너, 실시간 계수 0.05에 머무는 시뮬레이션, 주기를 놓치는 제어기다. 원시 도형(상자, 원기둥, 구)이나 볼록 분해를 쓰고, visual보다 약간 작게가 아니라 약간 크게 잡아라. 같은 요소가 안전 여유로도 쓰인다. 센서 헤드를 감싸는 원기둥은 계획 경로를 그 근처에서 떼어 놓는다.

관성에 대해: 튜토리얼의 지침은 중간 크기 링크에 `ixx`/`iyy`/`izz`를 `1e-3` 이하로 두는 것이 합리적 기본값이고, 단위 행렬은 특히 나쁜 선택이라는 것이다. 단위 행렬은 한 변 0.1 m에 600 kg인 상자에 해당한다. 관성이 0이거나 0에 가까우면 시뮬레이션 모델이 경고 없이 붕괴하고 모든 링크 원점이 월드 원점으로 몰린다. Gazebo에서 그 광경을 보면 `<inertial>`부터 보라.

### 5. Xacro: property, macro, 그리고 전개 방식

실제 로봇의 URDF는 지독하게 반복된다. 같은 원기둥이 `<visual>`과 `<collision>`에 두 번, 같은 다리가 부호만 바뀌어 두 번, 조인트 원점은 링크 길이로 손계산. Xacro는 그 반복을 없애는 XML 매크로 언어다. **property**(상수), **산술**, **macro** 셋을 준다.

네임스페이스를 선언해야 한다. 선언이 없으면 xacro가 파일 파싱을 거부한다("unbound prefix").

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">
  <xacro:property name="link_len" value="0.4"/>
  <cylinder radius="0.03" length="${link_len}"/>
  <origin xyz="0 0 ${link_len/2}" rpy="0 ${pi/2} 0"/>
</robot>
```

`${...}`는 property를 치환하거나 식을 계산한다. `+ - * /`, 단항 마이너스, 괄호, `sin`, `cos`, 상수 `pi`를 쓸 수 있다. 치환은 어떤 속성 안에서든 되고 리터럴 문자열과 합쳐지므로, `<link name="${prefix}_leg"/>`가 매크로 하나로 비슷한 이름의 링크 둘을 얻는 방법이다.

매크로는 파라미터를 받는다. 가장 단순한 경우 파라미터는 값이고, 매크로 안에서 property와 똑같이 `${...}`로 쓴다.

```xml
<xacro:macro name="default_inertial" params="mass">
  <inertial>
    <mass value="${mass}"/>
    <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
  </inertial>
</xacro:macro>
<xacro:default_inertial mass="10"/>
```

두 번째 종류도 있다. 이름 앞에 `*`를 붙인 파라미터는 호출자가 넘기는 XML *블록*이며 `<xacro:insert_block>`이 삽입한다. 큰 로봇 기술에서 만나게 되며, 시작할 때는 위의 값 형태로 충분하다.

> [!warning] 조용한 Xacro 실패
> 매크로 이름 오타는 조용하지 않고 시끄럽다. `handle_macro_call`이 `XacroException("unknown macro name: ...")`을 던지고, xacro는 0이 아닌 값으로 종료하며 출력물을 아예 내지 않는다. property나 파라미터 이름의 오타도 시끄럽다. `${...}` 안의 정의되지 않은 property는 "name ... is not defined"를, 틀린 매크로 파라미터 이름은 "Invalid parameter"를 낸다.
>
> 정작 조용한 것은 xacro가 검사하지 않는 URDF 속성의 오타다 — `xyz=` 대신 `xzy=` — urdfdom이 무시하므로 오프셋이 0인 조인트가 남는다. 무언가 없을 때가 아니라 숫자가 이상할 때 파일로 전개해서 읽어라.

Xacro는 전처리기다. 하류의 어떤 것도 이해하지 못한다. 전개는 두 방식 중 하나다.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
```

이쪽이 디버깅 경로다. 로봇이 기대와 다를 때마다 실행해서 출력을 읽어라. 운영 경로는 launch 파일 안에서 xacro를 돌려 디스크의 URDF가 낡지 않게 한다. 공식 `urdf_launch` 패키지가 하는 방식이다.

```python
from launch.substitutions import Command
from launch_ros.parameter_descriptions import ParameterValue

robot_description = ParameterValue(Command(['xacro ', urdf_path]), value_type=str)
```

`value_type=str`이 중요하다. 없으면 파라미터 타입이 추정되고, 숫자로 시작하거나 다른 것으로 파싱되는 URDF는 엉뚱한 타입으로 도착한다.

### 6. robot_state_publisher와 joint_state_publisher_gui가 실제로 하는 일

`robot_state_publisher`는 정적 기술과 실시간 조인트 각도를 실시간 프레임으로 바꾸는 노드다. 문서에 따르면,

- URDF를 `robot_description` **파라미터**로 받는다. 시작 시점에 설정되어 있지 않으면 노드가 뜨지 않는다.
- `joint_states`(`sensor_msgs/msg/JointState`)를 구독한다.
- **fixed** 조인트는 시작 시 한 번 `/tf_static`으로 나간다. transient local 토픽이라 나중에 붙은 구독자도 받는다.
- **가동** 조인트는 해당 조인트가 `joint_states`에 들어올 때마다 `/tf`로 나가고, `publish_frequency` 파라미터가 상한을 정한다. 기본값은 20.0 Hz.
- URDF 자체도 transient local인 `robot_description` 토픽으로 다시 내보낸다. RViz와 `joint_state_publisher`가 파일 경로 없이 모델을 얻는 경로가 이것이다.
- `frame_prefix`(기본값 빈 문자열)는 publish되는 모든 프레임에 접두사를 붙인다. 동일한 로봇 둘을 한 그래프에 띄우는 표준 방법이다.

조인트 각도를 지어내지는 *않는다*. `joint_states`를 내는 쪽이 없으면 트리의 가동 부분은 아예 나타나지 않고 RViz는 베이스 링크만 보여 준다. 실제 로봇에서는 하드웨어 드라이버나 `ros2_control`이 조인트 상태를 준다([[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]). 로봇이 아예 없으면 손으로 준다.

```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

이 노드는 모델을 읽고 — ROS 2에서는 `/robot_description` 토픽을 구독한다 — 고정이 아닌 모든 조인트와 그 한계를 찾아 조인트마다 슬라이더를 하나씩 준다. 슬라이더를 움직이면 `JointState`가 나가고, `robot_state_publisher`가 사슬을 다시 계산하고, RViz가 다시 그린다. 로봇 대역품일 뿐 그 이상이 아니다. 디버깅 도구이지 운영 시스템의 일부가 아니다. 실제 드라이버를 띄우는 launch 파일에 이것을 남겨 두면 `joint_states` 퍼블리셔 둘이 서로 싸운다.

### 7. TF2: 프레임 트리, 그리고 간선의 소유자

TF2는 "시각 t에 프레임 A가 B에 대해 어디 있는가"에 답하는 라이브러리다. 초심자가 가장 많은 시간을 잃는 곳이므로 네 가지를 정확히 하자.

**프레임은 그래프가 아니라 트리다.** 각 프레임은 부모가 정확히 하나, 자식은 몇이든 가진다. 루트는 하나다. 취향 규칙이 아니라, 조회 경로가 유일해지는 근거다.

**방향.** 두 사실을 떼어 놓자.

- *publish*는 부모, 자식 순으로 이름을 댄다. `header.frame_id`가 부모, `child_frame_id`가 자식이다.
- *조회*는 데이터가 도착할 곳, 출발한 곳 순으로 이름을 댄다. `lookup_transform(target_frame, source_frame, time)`은 `source_frame`에 *표현된* 데이터를 `target_frame`에 표현된 것으로 바꾸는 변환을 돌려준다.

함정은 그 둘 사이에 있다. tf2 개념 문서는 publish되는 `geometry_msgs/msg/Transform`이 *프레임* 형식이고 이는 데이터 형식의 역이라고 경고한다. 라이브러리는 트리를 걸으며 알아서 역을 취하므로 이 부호 오류를 저지르지 않는다. 저지르는 쪽은 변환을 처음 손으로 적는 당신이다.

사슬을 따라 합성하는 것이 트리의 이득이다. 2링크 팔이라면

$$ {}_{\text{base}}T_{\text{tip}} = {}_{\text{base}}T_{\text{link1}} \cdot {}_{\text{link1}}T_{\text{tip}} $$

이고, TF2가 몇 개 노드가 내보낸 몇 개 간선이든 이 곱을 대신 계산한다.

**주어진 부모–자식 간선은 퍼블리셔가 정확히 하나여야 한다.** 내부적으로 tf2는 *자식* 프레임마다 시간순 버퍼를 하나씩 둔다. 키는 자식 프레임뿐이고, 누가 보냈는지는 키가 아니다. 같은 간선을 내보내는 두 노드의 샘플은 한 버퍼에 섞여 들어가고, 조회는 요청 시각을 감싸는 이웃 샘플 사이를 저자와 무관하게 보간한다. 둘이 어긋나면 프레임은 두 답 사이를 오간다. 13절에서 일부러 재현한다.

**브로드캐스트는 싸고 국소적이다.** 어느 노드든 어느 간선이든 내보낼 수 있다. 의도한 트리가 실제 트리인지 검사하는 장치는 어디에도 없다. 10절의 도구가 그 검사다.

### 8. 정적 변환과 동적 변환, 버퍼, 그리고 조회의 시간 인자

**정적** 변환은 변하지 않는다. base에서 라이다 마운트, base에서 카메라. `/tf_static`으로 나가고 transient local durability로 publish되므로 한 번 보내면 이후 구독자도 받는다. 코드를 쓰지 말고 전용 실행 파일로 내보내라.

```bash
ros2 run tf2_ros static_transform_publisher --x 0 --y 0 --z 1 --roll 0 --pitch 0 --yaw 0 --frame-id world --child-frame-id mystaticturtle
```

`--frame-id`와 `--child-frame-id`를 뺀 모든 인자는 선택이고 생략하면 항등이며, roll/pitch/yaw 대신 `--qx --qy --qz --qw`도 받는다. 값은 모두 위처럼 이름 붙은 플래그 뒤에 쓴다. (오래된 튜토리얼에 나오는, 숫자 여섯 개나 아홉 개를 맨몸으로 늘어놓은 줄은 옛 형식이니 복사하지 말 것.)

**동적** 변환은 변하고 매번 타임스탬프가 찍힌다. odom에서 base_link, 그리고 팔의 모든 가동 조인트. `/tf`로 계속 나간다.

리스너는 그 토픽을 직접 읽지 않는다. **버퍼** — 기본 10초 깊이의 시간 색인 캐시 — 를 채우고 거기에 질의한다.

```python
from rclpy.duration import Duration
from rclpy.time import Time
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

self.tf_buffer = Buffer()
self.tf_listener = TransformListener(self.tf_buffer, self)

t = self.tf_buffer.lookup_transform('base_link', 'link2', Time())
```

세 번째 인자가 노드의 동작 여부를 가른다.

- Python의 `Time()`(C++의 `tf2::TimePointZero`)은 "지금"이 아니라 **가장 최근에 쓸 수 있는 변환**을 뜻한다. 실시간 질의에 원하는 값이고, 공식 디버깅 튜토리얼이 제시하는 올바른 수정이다.
- 실제 타임스탬프 — 보통 변환하려는 센서 메시지의 `msg.header.stamp` — 는 "이 이미지가 찍혔을 때 프레임들이 어디 있었나"를 뜻한다. 버퍼가 존재하는 이유 전부이고, 움직이는 로봇에서 검출 결과가 100 ms 낡지 않고 맞게 만드는 것이 이것이다.
- `self.get_clock().now()`는 "지금"이고, 버퍼 입장에서 **지금은 아직 오지 않았다**. 변환은 지연을 두고 도착한다. 9절이 이 오류다.

첫 실패에 바로 죽는 대신 잠깐 기다리려면 `timeout`을 준다. 기동 경로에서 원하는 동작이다.

```python
t = self.tf_buffer.lookup_transform('base_link', 'link2', Time(), timeout=Duration(seconds=0.05))
```

### 9. 누구나 만나는 오류 둘

**존재하지 않는 프레임.** 메시지가 명확하다.

```text
"turtle3" passed to lookupTransform argument target_frame does not exist
```

말 그대로다. 원인은 거의 항상 오타, 빠진 `frame_prefix`, 아직 뜨지 않은 퍼블리셔다. `tf2_echo`로 확인하면 `canTransform` 쪽에서 같은 말을 하고, 그다음 `view_frames`로 *존재하는* 프레임을 본다.

**미래로의 외삽을 요구하는 조회.**

```text
Could not transform turtle2 to turtle1: Lookup would require extrapolation into the future.
Requested time 1630223704.617054 but the latest data is at time 1630223704.616726, when
looking up transform from frame [turtle1] to frame [turtle2]
```

두 수를 읽어라. 요청 시각이 버퍼의 최신 샘플보다 *뒤*이고, 여기서는 약 0.3 ms 차이다. 버퍼는 설계상 외삽하지 않는다. 지어낸 변환은 변환이 없는 것보다 나쁘다. 원인은 `now`를 물은 것이다. 진단 도구는 두 프레임 사이 사슬의 지연을 보고하는 `tf2_monitor`다.

```bash
ros2 run tf2_ros tf2_monitor turtle2 turtle1
```

사슬, 평균과 최대 지연, 브로드캐스터별 주기를 찍는다. 순 지연이 3 ms라면 `now`는 대개 실패하고 `now - 0.1초`는 동작한다 — 그러나 그것은 진단이지 해법이 아니다. 해법은 "최신"을 뜻하는 `Time()`이거나, 메시지 자신의 타임스탬프에 timeout을 붙이는 것이다. 하드코딩한 지연에 손을 뻗었다면 답하지 않은 질문을 덮은 것이다.

거울상인 `Lookup would require extrapolation into the past`는 요청이 버퍼보다 오래됐다는 뜻이고, 센서 타임스탬프가 낡았거나 버퍼를 더 긴 `cache_time`으로 만들어야 한다는 신호다.

### 10. 트리 들여다보기: view_frames, tf2_echo, RViz

도구 셋, 각각 잘 답하는 질문이 다르다.

```bash
sudo apt install ros-jazzy-tf2-tools ros-jazzy-tf2-ros graphviz
ros2 run tf2_tools view_frames
```

`view_frames`는 5초 동안 구독하고(`--wait-time`으로 변경), 트리 전체를 Graphviz로 그린다. Jazzy에서는 현재 디렉터리에 `frames_<날짜>_<시각>.gv`와 `frames_<날짜>_<시각>.pdf`를 쓴다. 옛 튜토리얼이 말하는 `frames.pdf`가 아니다. `-o NAME`으로 이름을 바꾼다. "내 트리의 모양은 무엇인가"에 답하는 유일한 도구이고, 간선마다 브로드캐스터, 평균 주기, 버퍼 길이, 가장 최근과 가장 오래된 변환 시각이 라벨로 붙는다. 그 라벨이 진단 내용이다. 화살표만 보지 말고 라벨을 읽어라.

```bash
ros2 run tf2_ros tf2_echo [source_frame] [target_frame]
```

`tf2_echo`는 간선 하나 또는 사슬을 반복 출력한다. 병진, 쿼터니언과 RPY(라디안·도) 회전, 그리고 4×4 행렬 전체. 쿼터니언은 회전을 숫자 네 개로 표현한 것이다. 낯설다면 RPY 줄부터 읽고, 둘의 관계는 [[02-foundations/se3-geometry|3D Geometry & SE(3)]] §2를 보라. "이 숫자가 맞나"에 답하고, 그림으로는 멀쩡해 보이는 부호·축 오류를 잡는 데 쓴다.

RViz는 "이게 내 로봇처럼 보이나"에 답한다. 띄우고 **Fixed Frame**을 실제로 존재하는 프레임으로 맞춘 뒤(존재하지 않는 프레임을 넣으면 모든 display가 한꺼번에 실패하고 에러가 원인 아닌 곳을 가리킨다) display 둘을 추가한다.

- **RobotModel**. *Description Source*는 기본이 `Topic`이다. 다만 *Description Topic* 필드에는 **기본값이 없다.** RViz가 상속받은 토픽 속성의 이름만 바꿀 뿐 값을 넣지 않는다. 그러니 드롭다운에서 `/robot_description`을 직접 고르라. 고르기 전까지 디스플레이는 그냥 비어 있고 아무 말도 하지 않는데, "로봇이 안 보인다"는 신고의 가장 흔한 원인이 이것이다. 그 토픽은 transient local이라 `robot_state_publisher`만 돌고 있으면 파일 경로는 필요 없다. *Visual Enabled*와 *Collision Enabled* 체크박스가 두 형상을 따로 그리며, 충돌 형상이 삼각형 5만 개짜리 메시라는 사실을 이걸로 본다. *Mass*와 *Inertia*는 관성 특성을 그린다.
- **TF**. 모든 프레임을 축, 이름, 자식에서 부모로 가는 화살표로 그린다. *Frames*가 전체를 체크박스로 나열하고, *Tree*가 부모–자식 구조를 보여 주며, *Frame Timeout*은 갱신이 멈춘 프레임이 회색으로 바랬다가 사라지기까지의 시간을 정한다. RViz에서 프레임이 바래면 그 퍼블리셔가 죽은 것이다.

### 11. REP 105: map, odom, base_link

이동 플랫폼의 프레임 이름과 순서는 REP 105로 표준화되어 있고, 모든 내비게이션 스택이 이를 전제한다.

```text
map --> odom --> base_link
```

- `base_link`는 로봇 베이스에 강체로 붙어 있고, 베이스에서 기준으로 삼기 자연스러운 지점에 둔다.
- `odom`은 월드 고정 프레임이고 원점은 로봇이 출발한 자리다. `odom`에서의 로봇 자세는 **연속**이다. 불연속 도약 없이 매끄럽게 변한다. 그러나 휠 엔코더, 시각 오도메트리, IMU를 적분해 얻으므로 **한계 없이 표류**한다.
- `map`은 z가 위인 월드 고정 프레임이다. `map`에서의 자세는 위치추정 요소가 센서 관측으로 계속 다시 계산하므로 **표류하지 않는다**. 대신 **연속이 아니다**. 새 센서 정보가 들어올 때마다 불연속으로 도약할 수 있다.

피할 수 없는 맞교환이고, 두 프레임이 모두 존재하는 이유다. 국소적이고 단기적인 것 — 속도 제어기, 1초 앞 장애물 회피, 자세가 옆으로 30 cm 튀면 불안정해지는 모든 것 — 에는 `odom`을 쓴다. 장기적이고 전역적인 것 — "부엌으로 가라" — 에는 `map`을 쓴다. 표류하면 결국 엉뚱한 방에 도착하기 때문이다.

P6에서는 이 맞교환에 크기가 붙는다. `odom` → `base_link`는 엔코더 그 자체, $p=c/2048$이므로 $0.488\,\mathrm{mm}$ 단위로 움직이고 도약하지 않는다. 위치추정 한 번 — 카메라가 레일 끝 멈춤쇠를 본 것 — 이 카트를 $1.000\,\mathrm{m}$에 두는데 오도메트리는 $0.990\,\mathrm{m}$라고 한다고 하자(예시용 차이이지 카탈로그 숫자가 아니다). 그러면 위치추정 노드는 $0.010\,\mathrm{m}$, 약 $20$ 카운트짜리 `map` → `odom` 보정을 publish한다. 그 순간 `map`에서의 카트 자세는 $10\,\mathrm{mm}$ 도약하고 `odom`에서의 자세는 움직이지 않으므로, `odom`을 읽는 $200\,\mathrm{Hz}$ 제어기는 아무 도약도 보지 않는다.

구조가 사람을 놀라게 한다. 직관은 `map`과 `odom`이 둘 다 `base_link`의 부모여야 한다고 말하지만, 프레임은 부모를 하나만 가질 수 있으므로 REP 105는 `map`을 `odom`의 부모로 둔다. 그 귀결로, 위치추정 노드는 로봇 자세를 직접 내보내지 않는다. `map` → `odom` 보정 — 곧 누적된 오도메트리 표류 — 을 내보낸다. 오도메트리는 `odom` → `base_link`를 낸다. 어느 쪽도 상대의 간선을 내지 않는다. 7절의 규칙을 시스템에서 가장 중요한 간선들에 적용한 것이다. `base_link` 아래는 전부 `robot_state_publisher`가 당신의 URDF를 읽어서 만든다.

`map` 위에는 선택적인 `earth` 프레임(ECEF)이 있고, 서로 다른 지도를 가진 여러 로봇을 엮어야 할 때만 등장한다.

### 12. 실습: Xacro로 쓴 2링크 팔을 RViz에서 움직이기

한 자리에서 끝난다. 기준 환경은 Ubuntu 24.04 위 ROS 2 Jazzy.

```bash
sudo apt install ros-jazzy-xacro ros-jazzy-joint-state-publisher-gui ros-jazzy-robot-state-publisher ros-jazzy-rviz2 ros-jazzy-tf2-tools liburdfdom-tools graphviz
```

`two_link_arm.urdf.xacro`를 쓴다.

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="two_link_arm">

  <material name="grey">
    <color rgba="0.6 0.6 0.6 1"/>
  </material>

  <xacro:property name="link_len" value="0.4"/>
  <xacro:property name="link_rad" value="0.03"/>

  <xacro:macro name="default_inertial" params="mass">
    <inertial>
      <mass value="${mass}"/>
      <inertia ixx="1e-3" ixy="0.0" ixz="0.0" iyy="1e-3" iyz="0.0" izz="1e-3"/>
    </inertial>
  </xacro:macro>

  <xacro:macro name="arm_link" params="name">
    <link name="${name}">
      <visual>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
        <material name="grey"/>
      </visual>
      <collision>
        <origin xyz="0 0 ${link_len/2}" rpy="0 0 0"/>
        <geometry>
          <cylinder radius="${link_rad}" length="${link_len}"/>
        </geometry>
      </collision>
      <xacro:default_inertial mass="1.0"/>
    </link>
  </xacro:macro>

  <link name="base_link"/>
  <xacro:arm_link name="link1"/>
  <xacro:arm_link name="link2"/>

  <joint name="shoulder" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-1.57" upper="1.57" effort="10.0" velocity="1.0"/>
  </joint>

  <joint name="elbow" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0 0 ${link_len}" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-2.0" upper="2.0" effort="10.0" velocity="1.0"/>
  </joint>

</robot>
```

무엇을 실행하기 전에 전개해서 구조를 확인한다.

```bash
xacro two_link_arm.urdf.xacro > two_link_arm.urdf
check_urdf two_link_arm.urdf
```

전개된 URDF를 한 번 읽어라. `arm_link` 호출 둘이 완전한 링크 정의 둘을 만들었고 `${link_len/2}`는 `0.2`가 됐다. xacro는 그게 전부다.

이제 5절의 `urdf_launch` 방식을 따른 `display.launch.py`.

```python
from launch import LaunchDescription
from launch.substitutions import Command
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

URDF = '/absolute/path/to/two_link_arm.urdf.xacro'


def generate_launch_description():
    robot_description = ParameterValue(Command(['xacro ', URDF]), value_type=str)
    return LaunchDescription([
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             parameters=[{'robot_description': robot_description}]),
        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui'),
        Node(package='rviz2', executable='rviz2', output='screen'),
    ])
```

```bash
ros2 launch ./display.launch.py
```

RViz에서 **Fixed Frame**을 `base_link`로 두고 **RobotModel**과 **TF** display를 추가한다. 그다음:

1. 슬라이더 둘을 끌어 보라. 원기둥이 움직이고 TF 축이 따라 움직인다. `shoulder`는 y 둘레로 돌므로 팔은 x–z 평면에서 흔들린다.
2. `ros2 topic echo /joint_states` — 이름 둘, 위치 둘, 끌 때마다 변한다.
3. `ros2 topic echo /tf_static --once` — `transforms: []`가 찍힌다. `robot_state_publisher`는 기동할 때 정적 목록을 항상 발행하는데, 여기 조인트는 전부 가동이라 목록이 비어 있다. 센서 마운트용 `fixed` 조인트를 하나 넣으면 항목이 나타난다.
4. 슬라이더 둘을 0에 두고 `ros2 run tf2_ros tf2_echo base_link link2`. 병진이 `[0, 0, 0.4]`여야 한다. `link2`의 원점은 `link1`의 *끝*에 있고, 이는 elbow 조인트의 `<origin>`이 말하는 바다. shoulder를 1.57로 옮기고 x와 z가 뒤바뀌는 것을 보라.
5. `ros2 run tf2_tools view_frames` 후 생성된 PDF를 연다. 프레임 셋, 간선 둘, 각 간선의 주기는 10 Hz 근처다. *Broadcaster* 칸은 모든 간선에서 `default_authority`다. ROS 2에서는 리스너가 어느 노드가 변환을 보냈는지 알 수 없으므로 그 칸에는 정보가 없다. 그 10은 `joint_state_publisher`의 `rate` 기본값이다. `robot_state_publisher`는 받은 것을 다시 낼 뿐이고, 자기 `publish_frequency` 기본값 20 Hz는 목표치가 아니라 *상한*이다.
6. **Worked case의 3단계를 팔에서.** xacro에서 elbow 조인트의 `<origin xyz="0 0 ${link_len}" .../>`을 `xzy=`로 바꾼다. 전개해서 `check_urdf`를 돌리면 여전히 통과한다. 다시 띄우고 4번을 반복하라. `tf2_echo base_link link2`는 `[0, 0, 0.4]`를 찍던 자리에서 이제 `[0, 0, 0]`을 찍으므로, 오차는 정확히 잃어버린 오프셋 `link_len` $=0.4\,\mathrm{m}$다. 0에서는 두 원기둥이 겹쳐 그려지고, 로그는 아무것도 남기지 않는다. `xyz=`로 되돌려 놓아라.

주어진 슬라이더 값에 대해 `tf2_echo base_link link2`가 무엇을 찍을지 보기 전에 예측할 수 있으면 끝이다.

### 13. 진단할 고장: 한 간선에 퍼블리셔 둘

실습을 띄워 둔 채 `base_link` → `link1`의 두 번째 소유자를 추가한다 — 자기 타임스탬프로 *다른* 값을 내보내는 소유자여야 한다. 이 조건이 중요하다. 같은 `/joint_states`를 읽는 두 번째 `robot_state_publisher`는 값도 스탬프도 똑같은 변환을 만들고, tf2는 완전히 같은 샘플을 조용히 버리므로 아무 일도 일어나지 않는다.

```bash
# a SECOND robot_state_publisher, fed from its own joint-state topic
ros2 run robot_state_publisher robot_state_publisher --ros-args \
  -r __node:=robot_state_publisher_b -r joint_states:=joint_states_b \
  -p robot_description:="$(xacro two_link_arm.urdf.xacro)"
# in another terminal: hold the second publisher's shoulder at zero, 20 times a second
ros2 topic pub /joint_states_b sensor_msgs/msg/JointState \
  "{header: {stamp: now}, name: [shoulder, elbow], position: [0.0, 0.0]}" --rate 20
```

**증상.** shoulder 슬라이더를 0에서 멀리 옮겨라. RViz에서 `link1`과 그 아래 전부 — `link2`, 팔의 나머지 — 가 슬라이더 자세와 0 자세 사이에서 떨거나 튄다. 이 트리로 파지 자세를 계산하는 리스너 노드는 주기마다 다른 답을 받고, 평균을 내면 나아지는 게 아니라 나빠진다. 에러 로그는 없다. 두 퍼블리셔 모두 시킨 대로 정확히 동작하고 있다.

**기전.** 7절에서: tf2는 자식 프레임마다 시간순 버퍼 하나를 두고, 키는 자식 프레임뿐이다. 두 퍼블리셔의 샘플이 시간순으로 뒤섞여 `link1`의 버퍼에 들어가고, 조회는 요청 시각을 감싸는 이웃 샘플 사이를 보간한다 — 그 쌍이 어떤 때는 슬라이더 쪽 둘, 어떤 때는 하나씩, 어떤 때는 0 자세 둘이다. (한 프레임에 정적 퍼블리셔와 동적 퍼블리셔를 섞으면 더 나쁘다. 정적 프레임과 동적 프레임은 버퍼 타입이 달라서, 두 종류가 번갈아 들어오면 tf2가 그 프레임의 캐시를 재할당하며 이력을 버린다.)

**그것을 찾는 명령.**

```bash
ros2 run tf2_tools view_frames
```

PDF를 열어 `base_link` → `link1` 간선의 라벨을 읽는다.

- **Average rate**가 하나가 아니라 대략 둘의 합이다. 여기서는 10 Hz 근처여야 할 간선이 30 Hz 근처로 찍힌다 — 그것이 단서다.
- **Broadcaster**는 도움이 안 된다. ROS 2에서는 어떤 퍼블리셔든 `default_authority`로 찍히므로 이름도 개수도 알려 주지 못한다.

그다음 실제로 어떤 노드가 내보내는지 확인한다.

```bash
ros2 topic info /tf --verbose
ros2 topic info /tf_static --verbose
```

`--verbose`는 모든 엔드포인트를 노드 이름으로 나열한다([[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]]에서 이 플래그를 소개했다). 하나를 기대한 `/tf`에 퍼블리셔가 둘이거나, URDF가 이미 소유한 프레임을 `/tf_static`의 `static_transform_publisher`가 주장하고 있으면 조사는 끝난다.

**해법은 조정 손잡이가 아니라 구조다.** 각 간선의 소유자를 정하고 나머지 퍼블리셔를 지운다. 이 버그의 현실적 형태는 이렇다. URDF가 나중에 조인트를 갖게 된 프레임에 대해 launch 파일에 남아 있는 `static_transform_publisher`. 각자 `robot_state_publisher`를 띄우는 launch 파일 둘. `map` → `odom`을 동시에 내보내는 위치추정 노드와 bag 재생. 그리고 드라이버가 `odom` → `base_link`를 내보내는데 EKF가 같은 간선을 내보내는 경우. 마지막 것이 robot_localization이 `map` → `odom`을 내보내고 휠 드라이버에게 브로드캐스트를 끄라고 하는 이유다.

### 14. 이 페이지가 다루지 않는 것

조인트를 실제로 구동하는 것 — 제어기, 하드웨어 인터페이스, URDF의 Gazebo Harmonic 쪽 — 은 [[04-robotics/ros2/simulation-and-control|25.7 Simulation and ros2_control]]이고, 여기서 건너뛴 `<transmission>`과 `<ros2_control>` 태그, Gazebo가 기본으로 쓰는 SDF 형식도 거기 있다. 타임스탬프, `use_sim_time` 파라미터, TF 콜백이 언제 도는지 정하는 executor는 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]이다. TF2의 transient local `/tf_static`도 구독자가 QoS를 틀리는 순간 QoS 이야기가 된다. 설치 후에도 `package://` 메시 경로가 풀리도록 기술을 제대로 패키징하는 것은 [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. `lookup_transform`이 대신 해 주는 수학은 [[02-foundations/se3-geometry|3D Geometry & SE(3)]]와 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3]]. 이 모든 것의 위층은 [[04-robotics/ros2/index|25. ROS 2]]에 있다.

### 출처

- ROS 2 Jazzy 문서 — Tutorials/Intermediate/URDF: Building a movable robot model; Adding physical and collision properties; Using Xacro to clean up your code; Using URDF with `robot_state_publisher`.
- ROS 2 Jazzy 문서 — Tutorials/Intermediate/Tf2: Introducing tf2; Writing a static broadcaster (Python); Debugging tf2 problems.
- ROS 2 Jazzy 문서 — Concepts/Intermediate: Tf2(변환 방향과 `lookupTransform` 의미).
- `robot_state_publisher` 패키지 README(jazzy) — 파라미터, publish/subscribe 토픽.
- `geometry2` 소스(jazzy) — 자식 프레임 단위 버퍼와 브로드캐스터 기록은 `tf2/src/buffer_core.cpp`, `tf2/src/cache.cpp`; 출력 파일 이름과 간선 라벨은 `tf2_tools/view_frames.py`.
- `rviz_default_plugins` 소스(jazzy) — RobotModel과 TF display 속성.
- REP 105, Coordinate Frames for Mobile Platforms; REP 103, Standard Units of Measure and Coordinate Conventions.
- `urdf_launch` 패키지 — `description.launch.py`, `display.launch.py`.

### 스스로 점검

1. 노드가 `lookup_transform('odom', 'camera_link', self.get_clock().now())`을 호출하는데
   주기마다 "extrapolation into the future"가 찍힌다. 무엇이 잘못됐고 올바른 수정 둘은?
2. `map`과 `odom`이 둘 다 `base_link`의 부모가 될 수 없는 이유는 무엇이고, 위치추정 노드는
   대신 무엇을 내보내나?
3. URDF는 잘 로드되고 RViz에서도 멀쩡한데 플래너가 질의당 40초를 쓴다. 어디부터 보나?
4. `view_frames`는 모든 간선에 `default_authority`를 보여 준다. 한 간선에 퍼블리셔가 둘인지
   어떻게 알아내나?
5. P6에서 엔코더가 $1024$ 카운트를 읽는 동안 검출기가 `camera_link` 기준 $x=0.40\,\mathrm{m}$에
   표적을 보고한다. `odom`에서 표적은 어디이고, 믿어야 했던 숫자 둘은 무엇이며, 장착
   origin의 `xzy=` 오타는 미터와 카운트로 얼마를 물리는가?

> [!tip]- 정답 · Answers
> 1. 버퍼가 아직 데이터를 받지 못한 시각을 묻고 있다. 변환은 항상 얼마간 지연을 두고 도착한다. 가장 최근 변환을 원하면 `Time()`(`tf2::TimePointZero`)을 쓰고, 센서 데이터를 변환하는 경우라면 그 메시지의 `header.stamp`를 쓰되 짧은 `timeout`을 붙여 첫 실패에 죽지 않고 기다리게 한다. 0.1초를 하드코딩해 빼는 것은 진단이지 수정이 아니다.
> 2. tf2 프레임은 부모가 정확히 하나이고, 그것이 조회 경로를 유일하게 만든다. 그래서 REP 105는 `map` → `odom` → `base_link`로 잇는다. 오도메트리가 `odom` → `base_link`를 소유하고, 위치추정은 누적된 오도메트리 표류인 `map` → `odom` 보정을 내보낸다. `odom`은 연속이지만 표류하고, `map`은 표류하지 않지만 도약한다.
> 3. `<collision>` 요소. 정밀한 visual 메시를 재사용하고 있다면 질의당 수천 번의 충돌 검사가 원시 도형 대신 메시 대 메시로 돈다. RViz의 RobotModel display에서 *Visual Enabled*를 끄고 *Collision Enabled*를 켜서 검사기가 실제로 쓰는 형상을 보고, 원시 도형이나 볼록 분해로 바꾼다.
> 4. ROS 2에서 Broadcaster 칸에는 정보가 없다 — 리스너는 누가 변환을 보냈는지 알 수 없다. 대신 평균 주기를 읽는다. 10 Hz로 예상한 간선이 약 30 Hz로 보고되면 소유자가 둘 이상이다. `ros2 topic info /tf --verbose`와 `/tf_static`으로 확인한다. (값과 스탬프가 *똑같은* 변환을 보내는 두 퍼블리셔는 tf2가 완전 중복을 버리므로 아예 드러나지 않고, 해를 끼치지도 않는다.)
> 5. $x=1.00\,\mathrm{m}$, 장착 높이인 $z=0.25\,\mathrm{m}$이다. 프레임 축이 정렬되어 있어 사슬이 $0.40+0.10+0.50$으로 무너진다. $0.10\,\mathrm{m}$은 URDF에서 나와 `/tf_static`에 실린 고정 장착 오프셋이고 $0.50=1024/2048$은 `odom` → `base_link` 위의 살아 있는 엔코더 측정값이다. 믿은 숫자가 그 둘이고, 조용히 틀릴 수 있는 것은 앞의 것뿐이다. urdfdom은 알 수 없는 `xzy=` 속성을 실패시키지 않고 무시하므로 오프셋이 0이 되고 답이 $0.90\,\mathrm{m}$이 되며 오차는 $x$로 정확히 $0.10\,\mathrm{m}$($z$로는 $0.25\,\mathrm{m}$), 곧 $0.10\times2048=204.8$로 $0.488\,\mathrm{mm}$를 분해하는 엔코더의 약 $205$ 카운트다. xacro를 전개해 숫자를 읽어라. 다른 무엇도 이것을 알려 주지 않는다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**. 카트 프레임 `base_link`, 카메라가 카트 위, 엔코더 $N=2048$ counts/m. 비전 $50\,\mathrm{Hz}$, 제어 $200\,\mathrm{Hz}$. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** TF 트리 `map` → `odom` → `base_link` → `camera_link`. 각 간선의 소유자. `odom` → `base_link`에 엔코더 카운트, `camera_link`에 비전. 다섯 줄 타임라인: $200\,\mathrm{Hz}$ `odom` → `base_link` TF 갱신과 $200\,\mathrm{Hz}$ 조회 넷, 그중 하나가 `now()`.
2. **유도.** (a) 엔코더 한 카운트의 $\Delta p$ — `odom` → `base_link`의 해상도. (b) 제어기의 `lookup_transform(..., now())`가 "extrapolation into the future"를 찍는 이유. (c) `odom` → `base_link`에 $50\,\mathrm{Hz}$와 $200\,\mathrm{Hz}$ 퍼블리셔 둘. `view_frames`가 보고하는 주기는?
3. **해석.** 제어기가 $70\,\mathrm{ms}$ 예산 안에서 카메라 스탬프가 $200\,\mathrm{ms}$ 된 검출을 변환해야 한다. §9가 *extrapolation into the future*에 주는 수정 둘은 무엇이고, 그중 P6 힘 루프에 틀린 것은 어느 것이며, 루프는 그 검출을 어떻게 해야 하는가?

> [!note]- 그리는 법 · How to draw it
> - 프레임 넷이 한 사슬 `map` → `odom` → `base_link` → `camera_link`를 이루고, 모든 간선에 소유자·토픽·주기 셋을 적는다.
> - `map` → `odom`: 위치추정 노드, `/tf`, 보정할 때마다. `odom` → `base_link`: 엔코더 오도메트리 노드, `/tf`, $200\,\mathrm{Hz}$ — 이 간선에 엔코더 해상도를 적는다.
> - `base_link` → `camera_link`: 정적 브로드캐스터, `/tf_static`, 한 번, transient local — 이 간선에 고정한 장착 오프셋을 적는다.
> - `/tf` 간선 둘은 실선 화살표로, `/tf_static` 간선은 겹친 화살표로 그린다. "계속 다시 보낸다"와 "한 번 보내고 늦게 온 쪽을 위해 보존한다"의 차이가 곧 동작하는 RViz와 빈 RViz의 차이다.
> - URDF에 일부러 넣지 않은 것을 사슬 옆에 말로 적는다. 레일 위의 카트 이동이다. 이동 베이스의 자세는 URDF 조인트가 아니고(11절), 그 간선은 오도메트리 노드의 것이다.
> - 시계에는 `odom` → `base_link` 샘플을 $5\,\mathrm{ms}$ 간격으로 찍고 가장 새 것에 표시, 비전 스탬프 $0, 20, 40, 60\,\mathrm{ms}$, 제어 조회 넷, 그리고 $70\,\mathrm{ms}$ 예산.
> - `now()` 조회는 가장 새 샘플의 오른쪽에 떨어뜨리고 그 간격에 *extrapolation into the future*라고 적는다. 메시지 자신의 스탬프로 한 조회는 그 스탬프 자리로 돌아간다(위의 그림에서는 가장 새 샘플의 $20\,\mathrm{ms}$ 왼쪽).
> - `now()` 화살표가 눈에 띄게 빈 공간을 가리키면 제대로 그린 것이다.

> [!tip]- 정답 · Solutions
> 1. 위치추정이 `map` → `odom`을, 오도메트리(엔코더)가 `odom` → `base_link`를, 정적 브로드캐스터가 `base_link` → `camera_link`를 소유. 타임라인: `odom` → `base_link` TF $5\,\mathrm{ms}$마다(카메라 장착은 정적이라 갱신되지 않음); 조회 $0,5,10,15$; `now()` 조회는 버퍼의 미래.
> 2. (a) $0.488\,\mathrm{mm}$. (b) 변환은 늦게 도착하고 `now()`는 버퍼가 아직 못 본 시각. `Time()` 또는 메시지 스탬프. (c) 약 $250\,\mathrm{Hz}$ — 소유자 둘.
> 3. 최신값(`Time()`), 또는 짧은 timeout을 붙인 *메시지* 스탬프. $0.1\,\mathrm{s}$를 빼는 것은 진단이다. 여기서 틀린 것은 `Time()`이다. $200\,\mathrm{ms}$ 된 검출을 길어야 $5\,\mathrm{ms}$ 된 자세와 합성하므로, 표적이 지금 카트가 있는 자리에서 찍은 것처럼 놓이고 결과 어디에도 그 나이가 드러나지 않는다. 메시지 스탬프는 올바른 변환을 주고 나이도 그대로 보여 준다. $200\,\mathrm{ms}$는 이미 $70\,\mathrm{ms}$ 예산을 $130\,\mathrm{ms}$ 넘으니 — 외삽하지 말고 버려라.
