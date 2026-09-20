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
> You need friction and contact modes ([[04-robotics/contact-force-tactile|Contact, Force & Tactile §1–2]]), the impedance/admittance distinction and the contact-transition timescales ([[04-robotics/force-compliance-control|13. §2, §5]]), and what a learned representation is ([[02-foundations/neural-network-basics|0.7]]).
> 마찰과 접촉 모드([[04-robotics/contact-force-tactile|접촉·힘·촉각 §1–2]]), 임피던스/어드미턴스 구분과 접촉 천이의 시간 규모([[04-robotics/force-compliance-control|13. §2, §5]]), 그리고 학습된 표현이 무엇인지([[02-foundations/neural-network-basics|0.7]])가 필요하다.

## English

*Group H. Stands on [[04-robotics/contact-force-tactile|9. Contact]], [[04-robotics/force-compliance-control|13. Force Control]] and [[02-foundations/neural-network-basics|0.7]].
For the tasks where the deciding variable is inside the contact, hidden by the very thing doing the manipulating.*

> [!note] First pass · 처음이라면
> Read §1 — what vision cannot see, and why that is a short and specific list — then §2 on what a sensor actually transduces, then §6. §3 and §4 are for reading a specific fusion or slip-detection paper, and §2.5 is for when you are choosing or building a sensor rather than reading about one.

### Running object · 이 페이지의 대상

No plant in [[02-foundations/lab-plants|0.6]] has a contact patch, so this page freezes its own object and never changes its numbers. **S1 — the fingertip patch**: one finger pressing a panel edge, with three candidate sensors behind the same gel and one camera watching from the wrist.

| Part of S1 | Frozen value | Source of the number |
|---|---|---|
| contact patch | circular, radius $a = 5\ \mathrm{mm}$, normal load $P = 5\ \mathrm{N}$, $\mu = 0.5$ | chosen here; a fingertip-scale patch, and $\mu$ matches [[04-robotics/grasping\|15. Grasping]] |
| **optical** sensor | pitch $p = 0.0634\ \mathrm{mm}$, $320 \times 240$ px over $18.6 \times 14.3\ \mathrm{mm}$, $30\ \mathrm{Hz}$ | GelSight Mini's own published figures, used unchanged in §2.5 below |
| **taxel** array | $4 \times 4$ over the same $18.6 \times 14.3\ \mathrm{mm}$ sensing area, $1\ \mathrm{kHz}$, holds a DC reading | chosen here; a representative coarse capacitive pad |
| **piezoelectric** element | charge amplifier with $R_f = 10\ \mathrm{G\Omega}$, $C_f = 1\ \mathrm{nF}$, $1\ \mathrm{kHz}$ | chosen here; a plain single-pole charge amplifier |
| wrist camera | $1280$ px across $1.0\ \mathrm{m}$ at $0.5\ \mathrm{m}$, $30\ \mathrm{Hz}$, depth noise $\sigma_v = 2.0\ \mathrm{mm}$ | the camera already in §2's worked example; the noise figure is chosen here |
| tactile in-hand pose | $\sigma_t = 0.2\ \mathrm{mm}$ | chosen here |
| the event | the grip holds $5\ \mathrm{N}$ for $30\ \mathrm{s}$, then a tangential load ramps up and an $80\ \mathrm{Hz}$ slip transient appears | chosen here |
| human baseline | fingertip grating-orientation threshold $0.94\ \mathrm{mm}$ | van Boven & Johnson 1994, already cited in §3 |

The three sensors watch the *same* patch and the *same* event, which is the whole point: every comparison below is a comparison of transduction and sampling, with the physics held fixed.

*Scope: this page teaches what a tactile signal can and cannot carry — what each transduction family measures, what spatial resolution a pitch actually buys, when partial slip becomes visible, and what fusing touch with vision is worth — and how to read a paper built on one. It does not teach sensor fabrication, which [[07-research-program/index|7. Research Program §7]] puts out of scope; nor contact mechanics, which [[04-robotics/contact-force-tactile|9. Contact §1–2]] carries; nor the control loops the signal might close, which belong to [[04-robotics/force-compliance-control|13]].*

### Homework diagram · 과제가 그릴 그림

Three panels, and the first two must be drawn to the same scale or they teach nothing.

**Left — the patch, sampled.** Draw the $5\ \mathrm{mm}$-radius patch as a circle. Over its left half, rule the optical sampling grid; over its right half, rule the $4 \times 4$ taxel grid. Beneath it, three horizontal bars in a row, all at the same scale: $0.1268\ \mathrm{mm}$ (what the optical sensor resolves), $0.94\ \mathrm{mm}$ (the fingertip), $9.30\ \mathrm{mm}$ (what the taxel array resolves). The third bar is wider than the patch; draw it so, and let that be the figure's punchline.

**Middle — slip, as an annulus.** The same circle with the stick zone of radius $c$ drawn inside it and the slipping annulus shaded. Draw it three times, at $Q/\mu P = 0.25$, $0.50$ and $1.00$, and write the annulus width on each. Mark which of the three bars from the left panel would first fit inside each annulus.

**Right — time.** One axis, $0$ to $30\ \mathrm{s}$. Plot the piezoelectric element's reading of a constant $5\ \mathrm{N}$ grip decaying, mark $\tau$ and the half-life, and draw the flat line a barometric element would have given. Then, on an inset with a $50\ \mathrm{ms}$ axis, draw the $80\ \mathrm{Hz}$ burst on both and show that this time they agree.

The problem set asks for the same three panels with a denser taxel array, a faster charge amplifier and a smaller patch.

### Worked case · 대상으로 한 번 끝까지

**Step 1 — pitch is not resolution.** A sampled signal needs at least two samples per cycle of the finest feature it is to represent, so the finest resolvable *period* is twice the pitch, before any blur. For the optical sensor, $2 \times 0.0634 = 0.1268\ \mathrm{mm}$; for the taxel array, whose pitch is $18.6/4 = 4.65\ \mathrm{mm}$, it is $9.30\ \mathrm{mm}$.

| | pitch | resolution $= 2\times$ pitch | vs fingertip $0.94\ \mathrm{mm}$ |
|---|---:|---:|---|
| optical | $0.0634\ \mathrm{mm}$ | $0.1268\ \mathrm{mm}$ | $7.41\times$ finer |
| taxel $4\times4$ | $4.65\ \mathrm{mm}$ | $9.30\ \mathrm{mm}$ | $9.89\times$ **coarser** |

So the optical sensor is $14.83\times$ finer than a fingertip in *pitch* and $7.41\times$ finer in *resolution* — a factor of two between the two ways of saying it, and the larger one is the one that gets quoted. Between the two sensors, over the same sensing area, the resolution gap is $9.30/0.1268 = 73\times$ while the channel count differs by $76800/16 = 4800\times$; the gap in what can be *seen* is far smaller than the gap in what is *transmitted*.

**Step 2 — what each family measures, and for how long.** The piezoelectric element's charge amplifier is a single-pole high pass with $\tau = R_f C_f = 10\ \mathrm{G\Omega}\times 1\ \mathrm{nF} = 10.0\ \mathrm{s}$, so $f_c = 1/(2\pi\tau) = 0.0159\ \mathrm{Hz}$. Its reading of a constant $5\ \mathrm{N}$ grip is $5e^{-t/\tau}$:

| $t$ | $1\ \mathrm{s}$ | $5\ \mathrm{s}$ | $6.93\ \mathrm{s}$ | $10\ \mathrm{s}$ | $30\ \mathrm{s}$ |
|---|---:|---:|---:|---:|---:|
| reading | $4.52\ \mathrm{N}$ | $3.03\ \mathrm{N}$ | $2.50\ \mathrm{N}$ | $1.84\ \mathrm{N}$ | $0.25\ \mathrm{N}$ |

Half the grip is gone after $\tau\ln 2 = 6.93\ \mathrm{s}$ and $95\%$ of it after $30\ \mathrm{s}$, with the finger never having moved. Now the $80\ \mathrm{Hz}$ slip transient: $|H(f)| = (f/f_c)/\sqrt{1+(f/f_c)^2}$ with $f/f_c = 5027$, so $|H| = 1.0000$ to four places. **The same element reports the transient perfectly and the grip not at all**, and $|H(0)| = 0$ exactly says so: this is not a calibration problem and no amount of filtering repairs it. The taxel array's $|H(0)| = 1$, and it holds the $5\ \mathrm{N}$ for as long as you like.

**Step 3 — when partial slip becomes visible.** Under a normal load $P$ and a growing tangential load $Q$, a compliant circular contact does not go from stuck to sliding at a single instant. The periphery slips first and the stick zone shrinks from the rim inwards, with radius

$$c = a\left(1 - \frac{Q}{\mu P}\right)^{1/3}$$

so at $Q/\mu P = 0.50$ the stick radius is $5 \times 0.5^{1/3} = 3.97\ \mathrm{mm}$, the slipping annulus is $1.03\ \mathrm{mm}$ wide, and $1 - 0.5^{2/3} = 37\%$ of the contact area is already sliding **while the object has not moved at all**. That is the state §1's table calls incipient slip, and this is what it looks like as a number.

Now ask each sensor when it first *sees* that annulus — when the annulus width first reaches its resolution:

| sensor | resolution | annulus reaches it at | tangential load, at $P = 5\ \mathrm{N}$, $\mu = 0.5$ |
|---|---:|---:|---:|
| optical | $0.1268\ \mathrm{mm}$ | $Q/\mu P = 0.074$ | $0.185\ \mathrm{N}$ of a $2.5\ \mathrm{N}$ budget |
| human fingertip | $0.94\ \mathrm{mm}$ | $Q/\mu P = 0.465$ | $1.16\ \mathrm{N}$ |
| taxel $4\times4$ | $9.30\ \mathrm{mm}$ | **never** | — |

The annulus can never be wider than the patch radius, $5\ \mathrm{mm}$, and the taxel array's finest resolvable feature is $9.30\ \mathrm{mm}$ — so no amount of sampling rate makes partial slip visible to it: it can report the grip force forever and can never report that the grip is about to fail. That is §1's claim for high resolution, converted from an argument into a threshold — and it is a *geometry* result, independent of the $1\ \mathrm{kHz}$ the same array runs at.

**Step 4 — the rate argument is a different argument.** At $50\ \mathrm{mm/s}$ of gross slip the object moves $1.67\ \mathrm{mm}$ between two $30\ \mathrm{Hz}$ frames and $0.05\ \mathrm{mm}$ between two $1\ \mathrm{kHz}$ samples — §2's worked example, unchanged. Note which sensor wins which: the optical sensor wins Step 3 on geometry and loses Step 4 on rate; the taxel array does the reverse. **The resolution advantage and the rate advantage belong to different transducers**, which is why "high-resolution tactile sensing gives you slip detection" is two claims wearing one coat.

**Step 5 — what fusing with vision is worth.** Vision and touch both estimate the same in-hand offset, independently, with $\sigma_v = 2.0\ \mathrm{mm}$ and $\sigma_t = 0.2\ \mathrm{mm}$. Weighting each by its precision $1/\sigma^2$:

$$w_t = \frac{\sigma_t^{-2}}{\sigma_v^{-2} + \sigma_t^{-2}} = \frac{25}{0.25 + 25} = 0.990, \qquad \sigma_{\text{fused}} = \left(\sigma_v^{-2} + \sigma_t^{-2}\right)^{-1/2} = 0.199\ \mathrm{mm}$$

because independent Gaussian precisions add. So fusion buys $10.05\times$ over vision alone and $1.005\times$ over touch alone — **half a percent**. If vision says $1.40\ \mathrm{mm}$ and touch says $0.20\ \mathrm{mm}$, the fused estimate is $0.212\ \mathrm{mm}$: touch, with a rounding error of vision. Do it unweighted instead — concatenate and average, which is what a naive architecture does — and the answer is $0.800\ \mathrm{mm}$ with $\sigma = \sqrt{(4 + 0.04)/4} = 1.005\ \mathrm{mm}$, **five times worse than touch alone**. Against a $0.5\ \mathrm{mm}$ seating tolerance that is the difference between $2.5\sigma$ and $0.50\sigma$.

The lesson is §4's honest reading, arrived at from below. When one modality dominates in a quantity, optimal fusion of that quantity is worth almost nothing, and unweighted fusion is worth less than nothing. Whatever a fusion paper's gain is coming from, it is not this — it is coming from the modalities being good at *different* quantities, from the extra training signal, or from the representation. Which is exactly why the two ablations in §6 are the first thing to look for.

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
  you the net force and moment, not a full spatial pressure map. Under a single-contact model, the wrench can constrain a line of action; locating a unique contact needs further geometry or assumptions. Everything distal to the sensor — the gripper's own weight
  and inertia — is in the reading and must be compensated.
- **Taxel arrays** (capacitive, piezoresistive) give a coarse pressure map. Cheap,
  robust, low resolution, and they drift.
- **Optical (vision-based) tactile sensors** — GelSight, DIGIT — put a camera behind a
  deformable gel and read the gel's deformed surface as an image. This is the key point that
  papers state and readers skip: **their raw measurement is an image; geometry and force require reconstruction or calibration from gel appearance and deformation.** They give remarkable spatial detail about the shape
  pressed into the gel, at camera frame rates and camera latency.
- **Soft pin arrays** — the TacTip family — are a marker-based variant of optical tactile sensing: a camera tracks internal pins that mimic dermal papillae,
  inferring shear as well as normal information from a 3D-printable, robust structure, at camera rate.

The right question for any of them is not "how sensitive is it" but **"what does it output
at what rate, and what has to be inferred?"** The answer bounds what the paper on top of it
can claim.

> [!important] The latency point that §5 of the force-control page already made
> An optical tactile sensor runs at camera rate. A hard contact transition lasts roughly 1–15 ms depending on series compliance —
> about 14 ms for a bare tool on a real arm ([[04-robotics/force-compliance-control|13. §5]]) — and even the stiff end is well under one 33 ms camera frame, so touch is not a
> mechanism for *surviving* impact — it is a mechanism for **deciding what to do next**.
> Papers that use tactile feedback for closed-loop force regulation are making a much
> stronger hardware claim than papers that use it for state estimation and re-planning, and
> the two are easy to confuse in an abstract.

> [!example] Worked example · 계산 예제
> **Why "tactile sees what vision cannot" is an arithmetic claim.** GelSight publishes 0.0634 mm
> per pixel for the Mini, over a field of view its datasheet gives as 18.6 × 14.3 mm. A wrist camera with a 90° horizontal field of
> view at 0.5 m spans $2 \times 0.5 \times \tan 45° = 1.0$ m across 1280 pixels, i.e.
> **0.78 mm per pixel**. Over the patch that matters, the tactile sensor resolves
> $0.78/0.0634 = \mathbf{12\times}$ finer — and it does so *while the object is occluded by the
> fingers*, which is exactly when the camera has nothing.
>
> **The same argument in time.** An object slipping at 50 mm/s moves $50/30 = 1.7$ mm between
> two frames of a 30 Hz camera and $50/1000 = 0.05$ mm between two samples of a 1 kHz tactile
> signal. A 1.7 mm slip has already changed the grasp; 0.05 mm has not. Slip detection is not a
> modality preference, it is a sampling-rate result — but note that an *optical* tactile sensor runs at camera rate and gets the same 1.7 mm. The kilohertz rate needs a different transducer family (piezoelectric, taxel or acoustic), so the resolution advantage above and this rate advantage come from different sensors.
>
> **The reading this gives you.** These two ratios bound what any tactile paper can honestly
> claim. Resolution buys you contact geometry over a patch the size of a fingertip and nothing
> beyond it — a tactile sensor cannot tell you where the object is on the table. Rate buys you
> events shorter than a camera frame. A paper claiming tactile improved a task should be
> locating its gain in one of those two, and if it cannot, the gain is probably coming from
> somewhere else in the system.

### 2.5 How the signal is made — the transduction families

Section 2 grouped sensors by what comes out, because that is what bounds the claims a paper
can make. This section groups them by what physically changes, because that is what bounds
what you can *build* — and because a paper's sensor choice explains failures that look like
algorithm failures.

> **Tactile transduction, defined.** A **transduction family** is a *class of sensors sharing one physical conversion* from a mechanical contact variable to an electrical one — not a product, not a form factor and not a spatial layout. Three defining conditions, and a family is only named once all three are fixed. A named **mechanical input**: normal pressure, shear, strain, displacement, or the time derivative of one of them. A named **electrical output**: resistance, capacitance, charge, voltage, digital word. And a **passband** — the range of frequencies over which the conversion actually holds, whose lower edge is what decides whether the family reports a *state* or a *change*. The third is the one hardware sections state and method sections forget.
>
> $$\left|H(f)\right| = \frac{f/f_c}{\sqrt{1 + (f/f_c)^2}}, \qquad f_c = \frac{1}{2\pi R_f C_f}$$
>
> for a charge-coupled family read through a single-pole front end, where $f$ is the frequency of the contact variable, $f_c$ the corner set by the readout's own $R_f C_f$, and $|H|$ the fraction of the signal that survives — so $|H(0)| = 0$ says, exactly and unfixably, that this family cannot report a constant load.
>
> - **Example**: S1's piezoelectric element, $f_c = 0.0159\ \mathrm{Hz}$. It passes the $80\ \mathrm{Hz}$ slip transient at $|H| = 1.0000$ and a constant grip at $|H| = 0$. It is a *change* family.
> - **Non-example**: "piezoelectric sensors drift." Drift is a slow, unpredictable wander of a family that *can* hold DC — the piezoresistive row below. A piezoelectric element does not drift; it high-passes, with a corner you can compute from two component values and a decay you can predict to four figures. Calling both "drift" hides the fact that one is a calibration problem and the other is a passband.
> - **Why it matters**: read the passband first and half the table below is predictable. It is also the shortest honest answer to "will this sensor work for my task": a task that needs a held force needs a $|H(0)| = 1$ family, and no amount of learning recovers a quantity the transducer never transmitted.

| Family | What changes | What it measures, and for how long | How it is read | Strong at | Fails at |
|---|---|---|---|---|---|
| **Piezoresistive** | resistance of a doped elastomer or film under strain | normal pressure, as a **state** — $\left\|H(0)\right\| = 1$ in principle, degraded by drift and hysteresis in practice | Wheatstone bridge — a four-resistor circuit that turns a tiny resistance change into a measurable voltage; arrays scanned row-by-column | cheapest and fastest to get working | drift, hysteresis, and noise that grows with array size |
| **Capacitive** | capacitance of a conductor–insulator–conductor sandwich as the gap closes | normal displacement, hence pressure, as a **state** — holds DC indefinitely | a dedicated capacitance front end — a multimeter will not do it | sensitivity, and it survives being made of fabric | stray capacitance, including from the human body nearby |
| **Piezoelectric** | charge that appears when the material is stressed (PVDF, ceramics, ferroelectric crystals) | the **rate of change** of stress — a high pass at $f_c = 1/2\pi R_f C_f$, so $\left\|H(0)\right\| = 0$ | charge amplifier — its output voltage tracks the charge itself, which is tiny and would otherwise be lost to cable and input capacitance; even so the charge drains away over time, the failure at right | vibration, texture, the *onset* of slip | **static load — the charge leaks away**, so it reports change, not weight |
| **Barometric** | pressure in a sealed cavity over an off-the-shelf MEMS die | absolute pressure over one cavity, as a **state**, already calibrated in kPa | the die's own digital output | a clean calibrated signal for \$30–100, because someone else solved the hard part | spatial density; each cavity is a taxel and cavities are bulky |
| **Magnetic (Hall effect)** | position of a magnet in compliant material relative to the sensor; the Lorentz force on carriers makes a transverse voltage (see [[glossary\|Hall effect]]) | three components of a field, hence normal **and shear** displacement, as a **state** — but through a nonlinear, non-injective map | Hall element, three axes per point | no wear, no electrical contact across the compliant layer | the field-to-contact map is nonlinear and not one-to-one |
| **Acoustic** | structure-borne sound the contact itself makes | acoustic power in frequency bands — a **change** family by construction, with a passband set by the coupling | microphone or piezo element plus spectral features | events — impacts, scrapes, texture | telling you *where*, or anything about a contact that is not moving |
| **Whisker** | deflection of a compliant beam, measured at its base | root bending moment, hence one integral of the load along the beam, as a **state** — the spatial distribution is lost, not attenuated | any of the above, at the root | reaching past the body, and pre-filtering by beam geometry | resolving what it touched, as opposed to that it touched |

**The distinction that decides most of it: static or dynamic.** Half the families above
measure a *state* and half measure a *change*, and the split is not a matter of degree.
Piezoelectric charge dissipates through any real input impedance, so a piezoelectric sensor
holding a 5 N grip reads its way back to zero; it is a slip and texture sensor that cannot
tell you the grip force. Piezoresistive elements drift, so they report a fast press well and
a slow one poorly. Barometric and capacitive elements hold a DC reading and can report the
5 N indefinitely. When a paper says "with tactile feedback" and its task involves *holding*
something, this is the first question, and it is usually answered in the hardware section
rather than the method section.

**Why magnetic sensing arrived late.** The physics is old — Hall effect readout is decades
established — but the inverse problem is not friendly: a three-axis field reading at one
point is a nonlinear, non-unique function of where and how hard the compliant layer was
pressed. Fitting that by hand is unpleasant; learning it from data is routine. So this
family became practical when learned models started doing the inversion, which is a good
example of a *sensor* becoming viable because of progress in software.

**A calibration point worth carrying.** Human spatial acuity for touch runs from about
0.94 mm at the fingertip (grating orientation threshold, §3) to centimetres across the back. The optical sensors of §2 have a pixel pitch of about
0.06 mm — some fifteen times finer in pitch than the fingertip threshold, and, once the two-samples-per-feature rule of the Worked case is applied, **7.4 times** finer in resolution before any gel blur — but only over a patch the size of one
fingertip, and only where the gel is in contact. Human touch is far coarser and covers the
entire body continuously. Which of those two numbers matters depends on the task, and a
paper claiming "human-level tactile sensing" has usually compared one of them and not
the other — and has usually quoted the pitch ratio rather than the resolution ratio, which
is a free factor of two in its own favour.

**And the reason whole-body skin is a different problem.** Everything above is about a
patch. Covering a robot is a scaling question, and the arithmetic is unkind. Human skin
carries roughly 240 sensing units per cm² at the fingertip and about 60 per cm² at the palm,
over a body surface of about 1.8 m² — that is 18,000 cm², so palm density over a whole body
is $18{,}000 \times 60 \approx \mathbf{1.1}$ **million channels**, and fingertip density is
4.3 million.

Now try to reach that with the sensor of §2. A GelSight Mini is 76,800 pixels over
the datasheet's 18.6 × 14.3 mm, or 2.66 cm². That is about 29,000 channels per cm² —
**120 times denser than a human fingertip** — covering 0.015% of a body. Tiling a body with
them takes roughly **6,800 sensors**: 6,800 cameras, 0.52 gigapixels, and 16 gigasamples per
second at 30 Hz. Treat the area as approximate: 0.0634 mm per pixel across 320 pixels implies
20.3 mm, wider than the datasheet's 18.6, so GelSight's two published numbers do not quite
agree. The order of magnitude is what the argument needs.

So the two research directions here are not competing implementations of one idea, they are
answers to different halves of that calculation. **Tile cheaply**: accept a coarse
transduction — the piezoresistive or capacitive families above — and solve wiring,
addressing and per-taxel calibration at the million-channel scale, which is the line the
iCub skin started. **Probe cleverly**: keep very few transducers and recover a distributed
signal by inference, which is what acoustic and impedance-style approaches are for. A
paper's sensor count tells you which half it is working on, and its hardest problem is the
one that half implies — bandwidth and yield for the first, inverse problems for the second.

### 3. Slip, contact state, and the things touch is uniquely for

Three problems where touch is not one option among several:

- **Incipient slip detection.** Before an object moves, the contact patch begins to slip at
  its edges while the centre still sticks. That partial-slip signature is visible in a
  dense tactile signal and in nothing else — by the time vision sees motion, the object is
  already falling. This is the single clearest case for a high-resolution sensor.
- **Contact-state estimation.** Which contact state
  (sticking, sliding or separated per [[04-robotics/contact-force-tactile|Contact §1–§2]], and task-level states such as no contact, one-point,
  two-point, line, seated) the system is in is a *classification* problem whose evidence is largely tactile.
  It is also the state a task-level planner actually needs.
- **In-hand pose.** Where the object is *relative to the fingers* after grasping, which is
  the error a vision-planned grasp leaves behind and the thing an insertion needs.

The first of the three is the one that gets used loosely, so pin it down. "Slip" is not one
thing, and the useful distinction is between a *state of the contact patch* and a *motion of
the object*.

> **Slip and incipient slip, defined.** **Gross slip** is a *relative motion*: the object moves with respect to the finger, everywhere on the patch at once. **Incipient slip** — equivalently *partial slip* — is a **state of the contact patch**, not a motion and not an event: an outer annulus of the patch is sliding while an inner stick zone is not, and the object's net displacement is zero. Three defining conditions. The patch is **divided** into a stick zone and a slip annulus, so a single contact is simultaneously in two contact modes. The **object has not moved** — any definition that mentions object velocity has defined gross slip instead. And the division is set by the *ratio* of tangential to available friction force, so it is reached at the same $Q/\mu P$ whatever the absolute load.
>
> $$c = a\left(1 - \frac{Q}{\mu P}\right)^{1/3}, \qquad \frac{A_{\text{slip}}}{A} = 1 - \left(\frac{c}{a}\right)^{2}$$
>
> where $a$ is the patch radius, $c$ the stick-zone radius, $P$ the normal load, $Q$ the tangential load and $\mu$ the friction coefficient — the Cattaneo–Mindlin result for a compliant circular contact, so the annulus opens continuously from $Q = 0$ and the stick zone vanishes exactly at $Q = \mu P$, which is where gross slip begins.
>
> - **Example**: S1 at $Q/\mu P = 0.50$. The stick radius is $3.97\ \mathrm{mm}$ of a $5\ \mathrm{mm}$ patch, the annulus is $1.03\ \mathrm{mm}$ wide, and $37\%$ of the contact area is sliding with the object stationary.
> - **Non-example**: "the tactile signal changed, so the object is slipping." A change is also what a grip-force increase, a re-grasp, or a temperature drift produces. Incipient slip has a *spatial signature* — an annulus — and detecting it means resolving that annulus, which is why the Worked case's Step 3 table is a statement about the sensor, not about the algorithm.
> - **Why it matters**: it is the one quantity in §1's table that is defined by something *not* having happened yet, which is precisely why no modality that reports motion can supply it. And because the threshold is a ratio, a sensor that first resolves the annulus at $Q/\mu P = 0.074$ gives $93\%$ of the tangential budget as warning, at any grip force — a usable margin, stated without reference to the object's weight.

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
  0.5 mm). A paper quoting a two-point number as its human baseline has quoted a contaminated
  measure, and its sensor–human comparison can be off in either direction (van Boven & Johnson 1994 give the grating thresholds: fingertip 0.94 mm, lip 0.51 mm, tongue 0.58 mm).

The **two-point limen** is defined in full and derived as a design constraint on
[[04-robotics/haptics-teleoperation/tactile-display-design|24.2 Tactile display design §3]],
where it caps the number of *locations* a tactor array can address whatever its actuator
count. It is a property of a person at a named body site under named contact conditions, and
it is not re-derived here. What this page owes is the other half of the comparison — the
number on the sensor's side of it.

> **Spatial resolution, defined.** The **spatial resolution** of a tactile sensor is a *distance*: the smallest separation of two features on the contact surface that the sensor can still report as two. It is not the pitch, not the channel count, and not the sensing area. Three defining conditions, all of which must be stated with the number. It is bounded below by **sampling** — at least two samples per feature period, so $d \ge 2p$ for a grid of pitch $p$. It is bounded below again by **blur** — the compliant layer between the contact and the transducer low-passes the pattern, and no sampling recovers what the gel has already smoothed away. And it is measured over a **stated area**, because a sensor that resolves $0.13\ \mathrm{mm}$ over $2.7\ \mathrm{cm^2}$ and one that resolves it over a whole hand are not comparable devices.
>
> $$d_{\min} = \max\left(2p,\ d_{\text{blur}}\right)$$
>
> where $p$ is the sampling pitch and $d_{\text{blur}}$ the finest separation surviving the compliant layer, so a resolution figure is a *maximum* of two independent limits and quoting only the sampling one is an upper bound on performance, never a measurement of it.
>
> - **Example**: S1's optical sensor, $2 \times 0.0634 = 0.127\ \mathrm{mm}$ from sampling alone, over $2.66\ \mathrm{cm^2}$ — $7.4\times$ finer than the fingertip's $0.94\ \mathrm{mm}$, over $0.015\%$ of a body.
> - **Non-example**: "$0.0634\ \mathrm{mm}$ resolution." That is the pitch, and it overstates the resolution by exactly a factor of two before blur is considered at all. The $4\times4$ taxel array is the same error at the other end: $16$ channels sounds like a map, and $9.30\ \mathrm{mm}$ over a $10\ \mathrm{mm}$ patch is one number with a direction.
> - **Why it matters**: the sensor's resolution and the human limen are the two ends of every "human-level touch" claim, and both are distances measured under conditions that have to be quoted. Worked case Step 3 turns the sensor end into a task threshold: whether a given sensor sees incipient slip at all is decided by this number against the annulus width, and the taxel array fails that test on geometry no matter how fast it runs.

The design consequence is that resolution is a *task* target, not a virtue. A construction
gripper handling a panel edge or seating an anchor does not need fingertip acuity across the
whole finger; it needs enough resolution to resolve the contact patch that decides the task.
Fix the patch first, then the sensor. And when quoting any sensor's own resolution figure,
apply [[01-canonical-papers/notes/7-robotics/gelsight|GelSight's]] own caution — know which
part of the paper the number came from, because that abstract states none.

### 4. Visuotactile fusion — and what it is really buying

> **Visuotactile fusion, defined.** **Fusion** is a *map from several sensor streams to one quantity or one representation that a downstream stage consumes*. It is not a concatenation, not a network architecture and not an ablation. Three defining conditions. The streams must be **about the same thing** — the same pose, the same contact state, the same instant — which is why time alignment is a training objective in the reference paper below and not a detail. Each stream must enter with a **weight that reflects its reliability**, whether that weight is computed from stated variances, learned, or gated by a mode; an unweighted combination is not fusion, it is averaging. And the output must be **one** thing: two streams kept side by side for a policy to sort out are *inputs*, not a fusion.
>
> $$\hat x = \frac{\sigma_v^{-2}x_v + \sigma_t^{-2}x_t}{\sigma_v^{-2} + \sigma_t^{-2}}, \qquad \sigma_{\text{fused}}^{-2} = \sigma_v^{-2} + \sigma_t^{-2}$$
>
> for the analytic case of two independent unbiased estimates $x_v, x_t$ of one scalar with variances $\sigma_v^2, \sigma_t^2$ — because independent *precisions* add, which is the bound any learned fusion of the same two streams is competing against.
>
> - **Example**: S1's in-hand offset. $\sigma_v = 2.0\ \mathrm{mm}$ and $\sigma_t = 0.2\ \mathrm{mm}$ give $w_t = 0.990$ and $\sigma_{\text{fused}} = 0.199\ \mathrm{mm}$ — $10.05\times$ better than vision and $1.005\times$ better than touch.
> - **Non-example**: the unweighted mean, $\sigma = \sqrt{(\sigma_v^2 + \sigma_t^2)/4} = 1.005\ \mathrm{mm}$ — **five times worse than the better sensor alone**. Adding a modality is not monotone. A fusion architecture that cannot learn to ignore a stream can be beaten by deleting that stream, which is exactly what the vision-only and touch-only ablations of §6 test for.
> - **Why it matters**: it sets the ceiling. In any quantity where one modality dominates, optimal fusion is worth a fraction of a percent, so a fusion paper reporting a large gain is *not* getting it from combining two estimates of the same quantity. It is getting it from the modalities covering different quantities, from the extra self-supervised training signal, or from the representation — and those are three different claims with three different failure modes.

The reference result here is Lee et al.'s *Making Sense of Vision and Touch*, which learns a
single compact latent representation from RGB, force/torque, and proprioception. It trains with
**self-supervised** objectives: prediction targets the recorded data already contains, so no human labels
are needed. Here there are three — action-conditional optical flow, whether contact will occur at the next control step, and whether the vision and force streams are time-aligned.

Only then is the representation used: the policy is learned by reinforcement learning (trial-and-error
reward maximisation, [[02-foundations/rl-basics|7. RL Basics]]) in that latent space rather than on raw
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
> end-to-end training "by 95.1% on average over TacBench" when every model sees only 33–50% of each task's labelled data. That is an average of relative
> improvements across six heterogeneous tasks, not a success rate and not a percentage-point
> gain — unlike [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA's "up to 90%"]], which *is* a percentage-point gain; both get misread as success rates.
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
- [ ] Turn a sensor's pitch into its resolution, and name the second thing that bounds it.
- [ ] Say what a transduction family's passband decides, and which families cannot report a held force.
- [ ] Say what incipient slip is a state *of*, and what has to be resolved before it can be detected.
- [ ] Explain why sensor latency makes touch a decision signal rather than an impact-survival mechanism.
- [ ] State what visuotactile fusion usually buys, and what it usually does not.
- [ ] List the two ablations a fusion paper needs before its claim is readable.

> [!tip] Going deeper · 더 깊이
> No textbook; the sensors are the literature. Start at the physics: Johnson & Adelson (CVPR 2009) is retrographic sensing, the optical principle, before anyone put it on a robot. Then Yuan, Dong & Adelson (*Sensors* 2017) for GelSight as a robot sensor with geometry and force, and DIGIT (*RA-L* 2020) for the cheap compact form that made the modality common. Then Lee et al. (ICRA 2019) for using touch rather than building it. For the manipulation theory the signal feeds, [[04-robotics/contact-force-tactile|9. Contact, Going deeper]] names its textbooks; this page has none of its own.

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
> 3. At 30 fps a sample arrives every 33 ms, while a hard contact transition lasts about 14 ms for a bare tool on a real arm, and about 1.4 ms in the idealised rigid case ([[04-robotics/force-compliance-control|13. §5]]) — the entire event occurs between two frames. The sensor can report what the contact *was*, which is useful for deciding the next action, but it cannot participate in regulating the impact itself. That job belongs to passive compliance and a kilohertz torque loop.
> 4. The gripper's own weight and any payload, projected into the sensor frame — which depends on the arm's orientation, since gravity is fixed in the world frame and the sensor rotates with the wrist. The same held part produces a different raw reading in every pose, so gravity compensation needs the current kinematics ([[02-foundations/manipulator-kinematics-dynamics|10. §5]]). Inertial terms matter too during acceleration.
> 5. In scope: using an existing tactile sensor to make fastening robust — the contact-state classification, the policy that acts on it, and the evaluation against real fasteners. Out of scope: designing or fabricating a new sensor, which [[07-research-program/index|§7]] excludes because it is a separate contribution with its own literature and its own failure modes.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and **S1**. Three knobs move, nothing else. The finger is smaller, so the patch radius is $a' = 3\,\mathrm{mm}$ at the same $P = 5\,\mathrm{N}$ and $\mu = 0.5$. The taxel array is rebuilt at $8\times 8$ over the same $18.6\times14.3\,\mathrm{mm}$. The charge amplifier is rebuilt with $R_f' = 1\,\mathrm{G\Omega}$ at the same $C_f$. A tangential load now ramps at $5\,\mathrm{N/s}$ from zero, and the wrist camera is recalibrated so its depth noise falls to $\sigma_v' = 0.8\,\mathrm{mm}$. No new simulator.

1. **Draw.** The three panels of the homework diagram at the new numbers: the $3\,\mathrm{mm}$ patch with both sampling grids and the three resolution bars beneath it; the stick zone and annulus at $Q/\mu P = 0.25$ and $0.50$; and the new decay curve with $\tau'$ and the half-life marked. Add a fourth, small panel: a time axis from $0$ to $0.5\,\mathrm{s}$ with the instant each sensor first resolves the annulus marked on it, and the gross-slip instant at the right-hand end.
2. **Derive.** (a) The new taxel pitch and resolution, and its ratio to the fingertip's $0.94\,\mathrm{mm}$. (b) $\tau'$, $f_c'$, the reading of a constant $5\,\mathrm{N}$ grip at $t = 1\,\mathrm{s}$ and $t = 5\,\mathrm{s}$, and $|H|$ at $80\,\mathrm{Hz}$ and at $1\,\mathrm{Hz}$. (c) For each of the optical sensor and the new taxel array, the $Q/\mu P$ at which the annulus first reaches its resolution on the $3\,\mathrm{mm}$ patch — or a statement that it never does. (d) Convert (c) into seconds under the $5\,\mathrm{N/s}$ ramp: the detection instant, the gross-slip instant, and the warning window between them, in milliseconds and in $30\,\mathrm{Hz}$ frames. (e) The fused $\sigma$ and $w_t$ at $\sigma_v' = 0.8\,\mathrm{mm}$, and the $\sigma$ of the unweighted mean.
3. **Interpret.** §2's latency box says an optical tactile sensor at $33\,\mathrm{ms}$ per frame cannot participate in a $14\,\mathrm{ms}$ contact transition. Your answer to (d) says it has many frames of warning before gross slip. Reconcile the two in one sentence. Then say which of the three knobs changed a *verdict* rather than a number, and what that implies for the sentence "we improved slip detection with a higher-rate sensor".

> [!tip]- Solutions
> 1. The $9.30\,\mathrm{mm}$ bar of the original figure becomes $4.65\,\mathrm{mm}$ and is still wider than the whole $3\,\mathrm{mm}$ patch — the punchline survives the knob.
> 2. (a) Pitch $18.6/8 = 2.325\,\mathrm{mm}$, resolution $4.65\,\mathrm{mm}$, which is $4.95\times$ coarser than the fingertip — twice as good as the $9.89\times$ of the $4\times4$ array, and still coarser than skin. (b) $\tau' = 10^9 \times 10^{-9} = 1.00\,\mathrm{s}$, $f_c' = 1/(2\pi) = 0.159\,\mathrm{Hz}$; the grip reads $5e^{-1} = 1.84\,\mathrm{N}$ at $1\,\mathrm{s}$ and $5e^{-5} = 0.034\,\mathrm{N}$ at $5\,\mathrm{s}$; $|H(80)| = 1.0000$ and $|H(1)| = 0.988$. The faster amplifier lost the grip ten times sooner and gained nothing at $80\,\mathrm{Hz}$. (c) Optical: $1 - ((3 - 0.1268)/3)^3 = 0.1215$. Taxel: resolution $4.65\,\mathrm{mm} \ge a' = 3\,\mathrm{mm}$, so its finest resolvable feature is wider than the annulus can ever become — **never**, even at $1\,\mathrm{kHz}$ and even with four times the channels. (d) $\mu P = 2.5\,\mathrm{N}$, so gross slip at $2.5/5 = 0.500\,\mathrm{s}$. The optical sensor detects at $0.1215 \times 0.500 = 0.0608\,\mathrm{s}$, a warning window of $439\,\mathrm{ms}$ = $13.2$ frames at $30\,\mathrm{Hz}$. (e) $w_t = 25/(1.5625 + 25) = 0.941$, $\sigma_{\text{fused}} = 0.194\,\mathrm{mm}$ — still only $1.031\times$ better than touch alone. The unweighted mean gives $\sqrt{(0.64 + 0.04)/4} = 0.412\,\mathrm{mm}$, $2.06\times$ worse than touch alone: halving the camera's noise made unweighted fusion less catastrophic and did not make it useful.
> 3. The two statements are about events with different durations, not about the sensor: an impact is over in $14\,\mathrm{ms}$ and incipient slip lasts $439\,\mathrm{ms}$, so the same $33\,\mathrm{ms}$ frame is far too slow for one and thirteen times faster than needed for the other. The knob that changed a verdict is the **patch radius**, which pushed the taxel array from "never resolves the annulus" to — still never, but now by a smaller margin, and would have flipped had the array gone finer than $1.5\,\mathrm{mm}$ pitch; the amplifier and the camera moved numbers only. Which is why "we improved slip detection with a higher-rate sensor" is suspicious on its face: rate is the answer to Step 4's question, and incipient slip is Step 3's, so a rate improvement that improved incipient-slip detection was probably improving something else.

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
> 먼저 §1 — 비전이 볼 수 없는 것, 그리고 그것이 왜 짧고 구체적인 목록인지 — 그다음 센서가 실제로 변환하는 것인 §2, 그다음 §6. §3·§4는 특정 융합·미끄러짐 논문을 읽을 때이고, §2.5는 센서에 관해 읽는 것이 아니라 고르거나 만들 때다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6]]의 어떤 장치에도 접촉면이 없으므로, 이 페이지는 자기 대상을 고정하고 숫자를 끝까지 바꾸지 않는다. **S1 — 손끝 접촉면**: 손가락 하나가 패널 모서리를 누르고, 같은 젤 뒤에 후보 센서 셋, 손목에서 카메라 하나가 본다.

| S1의 구성 | 고정값 | 숫자의 출처 |
|---|---|---|
| 접촉면 | 원형, 반지름 $a = 5\ \mathrm{mm}$, 법선 하중 $P = 5\ \mathrm{N}$, $\mu = 0.5$ | 여기서 고름. 손끝 규모의 접촉면이고 $\mu$는 [[04-robotics/grasping\|15. 파지]]와 같다 |
| **광학** 센서 | 피치 $p = 0.0634\ \mathrm{mm}$, $18.6 \times 14.3\ \mathrm{mm}$ 위 $320 \times 240$ px, $30\ \mathrm{Hz}$ | GelSight Mini가 공표한 값, 아래 §2.5에서 쓰는 것 그대로 |
| **택셀** 배열 | 같은 $18.6 \times 14.3\ \mathrm{mm}$ 감지 면적 위 $4 \times 4$, $1\ \mathrm{kHz}$, DC를 유지 | 여기서 고름. 대표적인 거친 정전용량 패드 |
| **압전** 소자 | $R_f = 10\ \mathrm{G\Omega}$, $C_f = 1\ \mathrm{nF}$짜리 전하 증폭기, $1\ \mathrm{kHz}$ | 여기서 고름. 평범한 단극 전하 증폭기 |
| 손목 카메라 | $0.5\ \mathrm{m}$에서 $1.0\ \mathrm{m}$를 $1280$ px에, $30\ \mathrm{Hz}$, 깊이 잡음 $\sigma_v = 2.0\ \mathrm{mm}$ | 카메라는 §2의 계산 예제에 이미 있고, 잡음 값은 여기서 고름 |
| 촉각의 손 안 자세 | $\sigma_t = 0.2\ \mathrm{mm}$ | 여기서 고름 |
| 사건 | $5\ \mathrm{N}$으로 $30\ \mathrm{s}$ 쥐고 있다가, 접선 하중이 올라가고 $80\ \mathrm{Hz}$ 미끄러짐 과도가 나타난다 | 여기서 고름 |
| 사람 기준선 | 손끝 격자 방향 역치 $0.94\ \mathrm{mm}$ | van Boven & Johnson 1994, §3에 이미 인용됨 |

센서 셋이 *같은* 접촉면의 *같은* 사건을 본다. 그것이 요점 전부다. 아래의 모든 비교가 물리를 고정한 채 변환 방식과 표집만 비교하는 것이 된다.

*범위: 이 페이지는 촉각 신호가 무엇을 실어 나르고 무엇을 못 나르는지를 가르친다 — 각 변환 계열이 무엇을 재는지, 피치가 실제로 사 주는 공간 해상도가 얼마인지, 부분 미끄러짐이 언제 보이게 되는지, 촉각과 비전을 융합하는 것이 얼마짜리인지, 그리고 그 위에 세운 논문을 어떻게 읽는지. 센서 제작은 가르치지 않는다. [[07-research-program/index|7. 연구 프로그램 §7]]이 범위 밖에 둔다. 접촉 역학도 가르치지 않는다. [[04-robotics/contact-force-tactile|9. 접촉 §1~2]]가 진다. 이 신호가 닫을 수도 있는 제어 루프도 가르치지 않는다. [[04-robotics/force-compliance-control|13]]의 몫이다.*

### 과제가 그릴 그림 · Homework diagram

패널 셋이고, 앞의 둘은 반드시 같은 축척으로 그려야 한다. 그러지 않으면 아무것도 가르치지 못한다.

**왼쪽 — 표집된 접촉면.** 반지름 $5\ \mathrm{mm}$의 접촉면을 원으로 그린다. 왼쪽 절반에 광학 표집 격자를, 오른쪽 절반에 $4 \times 4$ 택셀 격자를 긋는다. 그 아래에 같은 축척의 가로 막대 셋을 나란히: $0.1268\ \mathrm{mm}$(광학이 분해하는 것), $0.94\ \mathrm{mm}$(손끝), $9.30\ \mathrm{mm}$(택셀 배열이 분해하는 것). 세 번째 막대가 접촉면보다 넓다. 그렇게 그리고, 그것이 이 그림의 급소가 되게 두라.

**가운데 — 미끄러짐은 고리다.** 같은 원 안에 반지름 $c$의 고착 영역을 그리고 미끄러지는 고리를 칠한다. $Q/\mu P = 0.25$, $0.50$, $1.00$에서 세 번 그리고 각각에 고리 폭을 적는다. 왼쪽 패널의 막대 셋 중 어느 것이 각 고리에 처음 들어가는지 표시한다.

**오른쪽 — 시간.** 축 하나, $0$부터 $30\ \mathrm{s}$까지. 일정한 $5\ \mathrm{N}$ 쥠에 대한 압전 소자의 값이 감쇠하는 곡선을 그리고 $\tau$와 반감기를 표시하며, 기압식이었다면 주었을 평평한 선을 함께 그린다. 그다음 $50\ \mathrm{ms}$ 축의 삽입 그림에 $80\ \mathrm{Hz}$ 버스트를 둘 다 그려, 이번에는 둘이 일치함을 보인다.

과제는 택셀 배열이 조밀해지고 전하 증폭기가 빨라지고 접촉면이 작아진 같은 패널 셋을 요구한다.

### 대상으로 한 번 끝까지 · Worked case

**1단계 — 피치는 해상도가 아니다.** 표집된 신호가 어떤 특징을 표현하려면 그 특징의 한 주기당 표본이 적어도 둘 필요하므로, 분해 가능한 가장 미세한 *주기*는 번짐을 따지기 전에 이미 피치의 두 배다. 광학 센서는 $2 \times 0.0634 = 0.1268\ \mathrm{mm}$, 피치가 $18.6/4 = 4.65\ \mathrm{mm}$인 택셀 배열은 $9.30\ \mathrm{mm}$다.

| | 피치 | 해상도 $=$ 피치의 $2$배 | 손끝 $0.94\ \mathrm{mm}$ 대비 |
|---|---:|---:|---|
| 광학 | $0.0634\ \mathrm{mm}$ | $0.1268\ \mathrm{mm}$ | $7.41$배 곱다 |
| 택셀 $4\times4$ | $4.65\ \mathrm{mm}$ | $9.30\ \mathrm{mm}$ | $9.89$배 **거칠다** |

즉 광학 센서는 *피치*로는 손끝보다 $14.83$배 곱고 *해상도*로는 $7.41$배 곱다 — 같은 말의 두 방식 사이에 두 배가 있고, 인용되는 쪽은 큰 쪽이다. 두 센서 사이에서는 같은 감지 면적 위 해상도 차이가 $9.30/0.1268 = 73$배인데 채널 수 차이는 $76800/16 = 4800$배다. *볼 수 있는 것*의 격차가 *전송되는 것*의 격차보다 훨씬 작다.

**2단계 — 각 계열이 무엇을, 얼마 동안 재는가.** 압전 소자의 전하 증폭기는 $\tau = R_f C_f = 10\ \mathrm{G\Omega}\times 1\ \mathrm{nF} = 10.0\ \mathrm{s}$인 단극 고역 통과이므로 $f_c = 1/(2\pi\tau) = 0.0159\ \mathrm{Hz}$다. 일정한 $5\ \mathrm{N}$ 쥠에 대한 값은 $5e^{-t/\tau}$다:

| $t$ | $1\ \mathrm{s}$ | $5\ \mathrm{s}$ | $6.93\ \mathrm{s}$ | $10\ \mathrm{s}$ | $30\ \mathrm{s}$ |
|---|---:|---:|---:|---:|---:|
| 값 | $4.52\ \mathrm{N}$ | $3.03\ \mathrm{N}$ | $2.50\ \mathrm{N}$ | $1.84\ \mathrm{N}$ | $0.25\ \mathrm{N}$ |

$\tau\ln 2 = 6.93\ \mathrm{s}$ 뒤에 쥠의 절반이, $30\ \mathrm{s}$ 뒤에 $95\%$가 사라진다. 손가락은 전혀 움직이지 않았는데도. 이제 $80\ \mathrm{Hz}$ 미끄러짐 과도를 보자. $|H(f)| = (f/f_c)/\sqrt{1+(f/f_c)^2}$이고 $f/f_c = 5027$이므로 $|H| = 1.0000$이다, 소수 넷째 자리까지. **같은 소자가 과도는 완벽히 보고하고 쥠은 전혀 보고하지 않는다.** $|H(0)| = 0$이 정확히 그 말이다. 보정 문제가 아니고 어떤 필터링으로도 고쳐지지 않는다. 택셀 배열은 $|H(0)| = 1$이고 $5\ \mathrm{N}$을 원하는 만큼 오래 유지한다.

**3단계 — 부분 미끄러짐이 언제 보이는가.** 법선 하중 $P$ 아래 접선 하중 $Q$가 자라면, 유연한 원형 접촉은 어느 한 순간에 고착에서 활주로 넘어가지 않는다. 가장자리부터 미끄러지고 고착 영역이 테두리에서 안쪽으로 줄어들며, 그 반지름이

$$c = a\left(1 - \frac{Q}{\mu P}\right)^{1/3}$$

이다. 그래서 $Q/\mu P = 0.50$이면 고착 반지름이 $5 \times 0.5^{1/3} = 3.97\ \mathrm{mm}$, 미끄러지는 고리가 폭 $1.03\ \mathrm{mm}$, 접촉 면적의 $1 - 0.5^{2/3} = 37\%$가 이미 활주 중인데 **물체는 전혀 움직이지 않았다.** §1의 표가 초기 미끄러짐이라 부르는 상태가 그것이고, 숫자로 보면 이렇게 생겼다.

이제 각 센서가 그 고리를 언제 *보는지* 묻자. 고리 폭이 자기 해상도에 처음 도달하는 때다:

| 센서 | 해상도 | 고리가 거기 닿는 때 | $P = 5\ \mathrm{N}$, $\mu = 0.5$에서의 접선 하중 |
|---|---:|---:|---:|
| 광학 | $0.1268\ \mathrm{mm}$ | $Q/\mu P = 0.074$ | $2.5\ \mathrm{N}$ 예산 중 $0.185\ \mathrm{N}$ |
| 사람 손끝 | $0.94\ \mathrm{mm}$ | $Q/\mu P = 0.465$ | $1.16\ \mathrm{N}$ |
| 택셀 $4\times4$ | $9.30\ \mathrm{mm}$ | **결코** | — |

고리는 접촉면 반지름 $5\ \mathrm{mm}$보다 넓어질 수 없는데 택셀 배열이 분해할 수 있는 가장 미세한 특징은 $9.30\ \mathrm{mm}$다. 그래서 표집 주파수를 아무리 올려도 부분 미끄러짐이 보이지 않는다. 파지력은 영원히 보고할 수 있고 파지가 곧 실패한다는 것은 결코 보고할 수 없다. 고해상도에 대한 §1의 주장이 논증에서 문턱값으로 바뀐 것이고, 같은 배열이 도는 $1\ \mathrm{kHz}$와 무관한 *기하*의 결과다.

**4단계 — 주파수 논증은 다른 논증이다.** 총 미끄러짐 $50\ \mathrm{mm/s}$에서 물체는 $30\ \mathrm{Hz}$ 두 프레임 사이에 $1.67\ \mathrm{mm}$, $1\ \mathrm{kHz}$ 두 표본 사이에 $0.05\ \mathrm{mm}$를 간다 — §2의 계산 예제 그대로다. 어느 센서가 어느 쪽을 이기는지 보라. 광학 센서는 기하의 3단계를 이기고 주파수의 4단계를 진다. 택셀 배열은 그 반대다. **해상도 이점과 주파수 이점은 서로 다른 변환기의 것**이고, 그래서 "고해상도 촉각이 미끄러짐 감지를 준다"는 외투 하나를 걸친 주장 둘이다.

**5단계 — 비전과 융합하면 얼마인가.** 비전과 촉각이 같은 손 안 오프셋을 독립적으로, $\sigma_v = 2.0\ \mathrm{mm}$와 $\sigma_t = 0.2\ \mathrm{mm}$로 추정한다. 각각을 자기 정밀도 $1/\sigma^2$로 가중하면:

$$w_t = \frac{\sigma_t^{-2}}{\sigma_v^{-2} + \sigma_t^{-2}} = \frac{25}{0.25 + 25} = 0.990, \qquad \sigma_{\text{fused}} = \left(\sigma_v^{-2} + \sigma_t^{-2}\right)^{-1/2} = 0.199\ \mathrm{mm}$$

이다. 독립인 가우시안 정밀도가 더해지기 때문이다. 그러므로 융합은 비전만에 비해 $10.05$배, 촉각만에 비해 $1.005$배를 산다 — **0.5퍼센트**다. 비전이 $1.40\ \mathrm{mm}$, 촉각이 $0.20\ \mathrm{mm}$라고 하면 융합 추정은 $0.212\ \mathrm{mm}$, 즉 촉각에 비전의 반올림 오차가 붙은 것이다. 대신 가중 없이 하면 — 이어 붙이고 평균 내는, 소박한 구조가 하는 일 — 답이 $0.800\ \mathrm{mm}$에 $\sigma = \sqrt{(4 + 0.04)/4} = 1.005\ \mathrm{mm}$로 **촉각만보다 다섯 배 나쁘다.** $0.5\ \mathrm{mm}$ 안착 공차에 대해서는 $2.5\sigma$와 $0.50\sigma$의 차이다.

교훈은 §4의 정직한 독법을 아래에서부터 도달한 것이다. 어떤 양에서 한 모달리티가 압도적이면 그 양에 대한 최적 융합은 거의 아무 값이 없고, 가중 없는 융합은 값이 음수다. 융합 논문의 이득이 어디서 오든 여기서 오는 것은 아니다. 모달리티들이 *서로 다른* 양을 잘한다는 데서, 늘어난 학습 신호에서, 혹은 표현에서 온다. §6의 ablation 둘을 가장 먼저 찾아야 하는 이유가 정확히 그것이다.

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
  [[04-robotics/force-compliance-control|힘 제어]]의 주력이고, 합력과 합모멘트를 주지만 공간적인 압력 분포 전체는 주지 않는다. 단일 접촉 모델이면 렌치에서 힘의 작용선을 제약할 수 있다. 접촉점 하나를 특정하려면 추가 기하나 가정이 필요하다. 센서보다 말단 쪽에 있는 모든 것 — 그리퍼 자신의 무게와
  관성 — 이 측정값에 들어 있으므로 보상해야 한다.
- **택셀 배열**(정전용량식, 압저항식)은 거친 압력 지도를 준다. 싸고 튼튼하며, 해상도가 낮고
  드리프트한다.
- **광학(비전 기반) 촉각 센서** — GelSight, DIGIT — 는 변형되는 젤 뒤에 카메라를 두고 젤의
  변형된 표면을 이미지로 읽는다. 논문은 밝히지만 독자가 건너뛰는 핵심이 이것이다:
  **원시 측정은 이미지이며, 기하와 힘을 얻으려면 젤의 외관·변형에서 복원하거나 보정해야 한다.** 젤에 눌린 형상에 대해
  놀라운 공간적 세부를, 카메라의 프레임률과 카메라의 지연으로 준다.
- **연성 핀 배열** — TacTip 계열 — 은 광학 촉각의 마커 기반 변형이다: 카메라가 진피 유두를 모사한 내부 핀을 추적해, 3D 프린팅 가능하고
  튼튼한 구조에서 법선뿐 아니라 전단 정보까지 카메라 주기로 추정한다.

어느 것에 대해서든 옳은 질문은 "얼마나 민감한가"가 아니라 **"무엇을 어떤 주기로 출력하고,
무엇이 추론되어야 하는가"** 다. 그 답이 그 위에 얹힌 논문이 주장할 수 있는 범위를 정한다.

> [!important] 힘 제어 페이지 §5가 이미 한 지연 이야기
> 광학 촉각 센서는 카메라 주기로 돈다. 단단한 접촉 천이는 직렬 컴플라이언스에 따라 대략 1~15 ms — 실제 팔의 맨 공구는 약 14 ms
> ([[04-robotics/force-compliance-control|13. §5]]) — 이고, 단단한 쪽 끝도 카메라 한 프레임 33 ms보다 훨씬 짧으므로, 촉각은 충격에서 *살아남는* 기제가
> 아니라 **다음에 무엇을 할지 결정하는** 기제다. 촉각 피드백을 폐루프 힘 조절에 쓴다는
> 논문은 상태 추정과 재계획에 쓴다는 논문보다 훨씬 강한 하드웨어 주장을 하는 것이고, 초록에서
> 이 둘은 혼동하기 쉽다.

> [!example] 계산 예제 · Worked example
> **"촉각은 비전이 못 보는 것을 본다"가 산술적 주장인 이유.** GelSight는 Mini에 대해 픽셀당 0.0634 mm를 공표하고, 데이터시트의 시야는 18.6 × 14.3 mm다. 수평 화각 90°인 손목 카메라는 0.5 m에서
> $2 \times 0.5 \times \tan 45° = 1.0$ m를 1280픽셀에 담으니 **픽셀당 0.78 mm**다. 문제가 되는
> 그 패치 위에서 촉각 센서는 $0.78/0.0634 = \mathbf{12}\text{배}$ 더 곱게 분해하고, 게다가 *손가락에
> 물체가 가려진 동안* 그렇게 한다 — 카메라에 아무것도 없는 바로 그때다.
>
> **같은 논증을 시간으로.** 50 mm/s로 미끄러지는 물체는 30 Hz 카메라의 두 프레임 사이에
> $50/30 = 1.7$ mm를, 1 kHz 촉각 신호의 두 샘플 사이에 $50/1000 = 0.05$ mm를 간다. 1.7 mm
> 미끄러짐은 이미 파지를 바꿔 놓았고 0.05 mm는 그렇지 않다. 미끄러짐 감지는 모달리티 취향이
> 아니라 샘플링 주파수의 결과다 — 다만 *광학* 촉각 센서는 카메라 주기로 돌아 똑같이 1.7 mm를 얻는다. 킬로헤르츠 속도에는 다른 변환기 계열(압전, 택셀, 음향)이 필요하므로, 위의 해상도 이점과 이 속도 이점은 서로 다른 센서에서 온다.
>
> **여기서 얻는 독법.** 이 두 비율이 촉각 논문이 정직하게 주장할 수 있는 범위를 정한다.
> 분해능은 손끝만 한 패치 위의 접촉 기하를 사 줄 뿐 그 바깥은 사 주지 않는다 — 촉각 센서는
> 물체가 탁자 위 어디에 있는지 말해 주지 못한다. 주파수는 카메라 한 프레임보다 짧은 사건을
> 사 준다. 촉각으로 과제가 나아졌다고 주장하는 논문은 그 이득을 이 둘 중 하나에 위치시켜야
> 하고, 그러지 못한다면 이득은 아마 시스템의 다른 곳에서 오고 있다.

### 2.5 신호는 어떻게 만들어지는가 — 변환 방식의 계열

2절은 센서를 나오는 출력으로 묶었다. 그것이 논문이 할 수 있는 주장을 한정하기 때문이다.
이 절은 물리적으로 무엇이 변하는지로 묶는다. 그것이 당신이 *만들 수 있는 것*을 한정하기
때문이고, 논문의 센서 선택이 알고리즘 실패처럼 보이는 실패를 설명해 주기 때문이다.

> **촉각 변환의 정의.** **변환 계열**(transduction family)은 기계적 접촉 변수에서 전기적 변수로 가는 물리적 변환 하나를 공유하는 *센서들의 부류*다. 제품도, 형태도, 공간 배치도 아니다. 정의 조건이 셋이고, 셋이 모두 정해진 뒤에야 계열에 이름이 붙는다. 명시된 **기계적 입력**: 법선 압력, 전단, 변형률, 변위, 혹은 그중 하나의 시간 미분. 명시된 **전기적 출력**: 저항, 정전용량, 전하, 전압, 디지털 값. 그리고 **통과대역** — 그 변환이 실제로 성립하는 주파수 범위이고, 그 아래쪽 끝이 이 계열이 *상태*를 보고하는지 *변화*를 보고하는지를 정한다. 하드웨어 절은 밝히고 방법 절은 잊는 것이 셋째다.
>
> $$\left|H(f)\right| = \frac{f/f_c}{\sqrt{1 + (f/f_c)^2}}, \qquad f_c = \frac{1}{2\pi R_f C_f}$$
>
> 단극 프런트엔드로 읽는 전하 결합 계열에 대한 식이다. $f$는 접촉 변수의 주파수, $f_c$는 판독 회로 자신의 $R_f C_f$가 정하는 코너, $|H|$는 살아남는 신호의 비율이다. 그러므로 $|H(0)| = 0$은 이 계열이 일정한 하중을 보고할 수 없다고 정확히, 그리고 고칠 수 없게 말한다.
>
> - **예**: S1의 압전 소자, $f_c = 0.0159\ \mathrm{Hz}$. $80\ \mathrm{Hz}$ 미끄러짐 과도를 $|H| = 1.0000$으로 통과시키고 일정한 쥠을 $|H| = 0$으로 막는다. *변화* 계열이다.
> - **반례**: "압전 센서는 드리프트한다". 드리프트는 DC를 유지할 *수 있는* 계열이 느리고 예측 불가능하게 흘러가는 것이고, 아래 표의 압전저항 행이 그것이다. 압전 소자는 드리프트하지 않는다. 고역 통과를 할 뿐이고, 코너는 부품 값 둘로 계산되며 감쇠는 네 자리까지 예측된다. 둘 다 "드리프트"라고 부르면 하나가 보정 문제이고 다른 하나가 통과대역이라는 사실이 가려진다.
> - **왜 중요한가**: 통과대역부터 읽으면 아래 표의 절반이 예측된다. "이 센서가 내 과제에 맞나"에 대한 가장 짧은 정직한 답이기도 하다. 쥐고 있는 힘이 필요한 과제에는 $|H(0)| = 1$인 계열이 필요하고, 변환기가 애초에 보내지 않은 양을 학습이 되살려 주지는 않는다.

| 계열 | 무엇이 변하나 | 무엇을, 얼마나 오래 재나 | 어떻게 읽나 | 강한 곳 | 실패하는 곳 |
|---|---|---|---|---|---|
| **압전저항(piezoresistive)** | 변형을 받은 도핑 엘라스토머·필름의 저항 | 법선 압력을 **상태**로 — 원리적으로 $\left\|H(0)\right\| = 1$이지만 드리프트와 이력현상이 실제로는 깎는다 | 휘트스톤 브리지 — 저항 네 개로 된 회로로, 아주 작은 저항 변화를 잴 수 있는 전압으로 바꾼다. 배열은 행–열로 훑는다 | 가장 싸고 가장 빨리 동작시킬 수 있다 | 드리프트, 이력현상, 배열이 커질수록 자라는 잡음 |
| **정전용량(capacitive)** | 간격이 좁아질 때 도체–절연체–도체 샌드위치의 정전용량 | 법선 변위, 따라서 압력을 **상태**로 — DC를 무한정 유지 | 전용 정전용량 프런트엔드 — 멀티미터로는 안 된다 | 감도, 그리고 천으로 만들어도 살아남는다 | 부유 용량, 근처의 사람 몸까지 포함해서 |
| **압전(piezoelectric)** | 재료에 응력이 걸릴 때 생기는 전하 (PVDF, 세라믹, 강유전 결정) | 응력의 **변화율** — $f_c = 1/2\pi R_f C_f$의 고역 통과이므로 $\left\|H(0)\right\| = 0$ | 전하 증폭기 — 출력 전압이 전하 자체를 따라가게 만든 증폭기. 전하가 아주 작아 그냥 두면 케이블과 입력단 정전용량에 묻히기 때문이다. 그래도 전하는 시간이 지나며 빠져나가고, 그것이 오른쪽의 실패다 | 진동, 질감, 미끄러짐의 *시작* | **정적 하중 — 전하가 빠져나간다**. 무게가 아니라 변화를 보고한다 |
| **기압(barometric)** | 기성 MEMS 다이 위 밀폐 공동의 압력 | 공동 하나 위의 절대 압력을 **상태**로, 이미 kPa로 보정되어 | 다이 자신의 디지털 출력 | 30~100달러로 얻는 깨끗한 보정 신호. 어려운 부분은 남이 풀어 놨다 | 공간 밀도. 공동 하나가 taxel 하나인데 공동은 부피가 크다 |
| **자기(홀 효과)** | 유연 재료 속 자석의 센서 대비 위치. 전하에 걸린 로런츠 힘이 횡방향 전압을 만든다([[glossary\|홀 효과]] 참고) | 자기장 3성분, 따라서 법선 **과 전단** 변위를 **상태**로 — 다만 비선형이고 단사가 아닌 사상을 통해 | 홀 소자, 한 점당 3축 | 마모가 없고, 유연층을 가로지르는 전기적 접촉이 없다 | 자기장→접촉 사상이 비선형이고 일대일이 아니다 |
| **음향(acoustic)** | 접촉 자체가 만드는 구조 전달음 | 주파수 대역별 음향 파워 — 구조상 **변화** 계열이고, 통과대역은 결합이 정한다 | 마이크나 압전 소자 + 스펙트럼 특징 | 사건 — 충격, 긁힘, 질감 | *어디인지*, 그리고 움직이지 않는 접촉에 관한 것 전부 |
| **수염(whisker)** | 유연한 보의 휨을 뿌리에서 측정 | 뿌리의 굽힘 모멘트, 따라서 보를 따른 하중의 적분 하나를 **상태**로 — 공간 분포는 감쇠하는 것이 아니라 사라진다 | 위의 어느 방식이든, 뿌리에서 | 몸 바깥으로 뻗는 것, 그리고 보 기하가 미리 걸러 주는 것 | 닿았다는 사실이 아니라 무엇에 닿았는지를 가려내는 것 |

**대부분을 결정하는 구분: 정적인가 동적인가.** 위 계열의 절반은 *상태*를 재고 절반은
*변화*를 재는데, 그 갈림은 정도의 문제가 아니다. 압전 전하는 실재하는 어떤 입력 임피던스로도
빠져나가므로, 5 N으로 쥐고 있는 압전 센서는 스스로 0으로 되돌아 읽는다. 미끄러짐과 질감
센서일 뿐 파지력을 말해 주지 못한다. 압전저항 소자는 드리프트하므로 빠른 누름은 잘, 느린
누름은 못 보고한다. 기압식과 정전용량식은 DC 값을 유지하므로 그 5 N을 무한정 보고할 수 있다.
논문이 "촉각 피드백을 써서"라고 쓰고 그 과제가 무언가를 *들고 있는* 일이라면, 이것이 첫
질문이고, 답은 대개 방법 절이 아니라 하드웨어 절에 있다.

**자기 방식이 늦게 도착한 이유.** 물리는 오래됐다 — 홀 효과 판독은 수십 년 확립돼 있다 —
그런데 역문제가 만만치 않다. 한 점의 3축 자기장 값은 유연층이 어디를 얼마나 세게 눌렸는지에
대한 비선형이고 유일하지도 않은 함수다. 그것을 손으로 맞추는 일은 괴롭고, 데이터로 배우는
일은 일상이다. 그래서 이 계열은 학습된 모델이 역변환을 맡기 시작하면서 실용화됐다.
*센서*가 소프트웨어의 진전 덕분에 가능해진 좋은 사례다.

**들고 다닐 만한 기준점 하나.** 사람의 촉각 공간 예민도는 손끝의 약 0.94 mm(격자 방향 역치, 3절)에서 등의 수 센티미터까지다.
2절의 광학 센서는 픽셀 간격이 약 0.06 mm다 — 손끝 역치보다 간격으로 열다섯 배쯤 곱고, Worked case의 "특징당 표본 둘" 규칙을 적용하면 젤 번짐을 따지기 전에 해상도로 **7.4배** 곱다 — 그러나 손끝 하나만 한
패치 위에서만, 그것도 젤이 닿아 있는 곳에서만 그렇다. 사람의 촉각은 훨씬 거칠지만 몸 전체를
끊김 없이 덮는다. 그 두 숫자 중 어느 쪽이 중요한지는 과제가 정하고, "사람 수준의 촉각"을
주장하는 논문은 대개 둘 중 하나만 비교하고 나머지는 비교하지 않았으며, 대개 해상도 비가 아니라
피치 비를 인용했다. 자기에게 유리한 두 배를 공짜로 얻은 것이다.

**그리고 전신 스킨이 다른 문제인 이유.** 위의 이야기는 전부 패치 하나에 관한 것이다. 로봇을
덮는 것은 규모의 문제이고, 산술이 야박하다. 사람 피부는 손끝에서 cm²당 대략 240개, 손바닥에서
cm²당 약 60개의 감지 단위를 지니며 체표면적은 약 1.8 m²다 — 즉 18,000 cm²이므로, 전신을 손바닥
밀도로 덮으면 $18{,}000 \times 60 \approx \mathbf{1.1}$**백만 채널**이고 손끝 밀도로는 432만
채널이다.

이제 2절의 센서로 거기에 닿아 보자. GelSight Mini는 데이터시트의 18.6 × 14.3 mm, 즉 2.66 cm²에
76,800픽셀이니 cm²당 약 29,000채널 — **사람 손끝보다 120배 조밀하다** — 그런데 덮는 면적은
몸의 0.015%다. 이것으로 몸을 타일링하려면 약 **6,800개**가 필요하다: 카메라 6,800대,
0.52기가픽셀, 30 Hz에서 초당 16기가샘플. 면적은 근사로 다루라. 픽셀당 0.0634 mm에 320픽셀이면
20.3 mm가 되어 데이터시트의 18.6 mm와 어긋난다. GelSight가 공표한 두 숫자가 딱 맞지 않는다.
이 논증에 필요한 것은 자릿수다.

그러므로 이 분야의 두 연구 방향은 한 발상의 경쟁하는 구현이 아니라, 저 계산의 서로 다른 절반에
대한 답이다. **싸게 타일링하기**: 거친 변환 방식을 받아들이고 — 위의 압전저항이나 정전용량
계열 — 백만 채널 규모에서 배선·주소지정·taxel별 보정을 푼다. iCub 스킨이 시작한 계보다.
**영리하게 탐침하기**: 변환기를 아주 적게 두고 분포된 신호를 추론으로 복원한다. 음향이나
임피던스 계열 접근이 그것을 위해 있다. 논문의 센서 개수가 어느 절반을 붙들고 있는지 알려 주고,
가장 어려운 문제도 그 절반이 함의하는 것이다 — 앞쪽은 대역폭과 수율, 뒤쪽은 역문제.

### 3. 미끄러짐, 접촉 상태, 그리고 촉각만이 할 수 있는 일

촉각이 여러 선택지 중 하나가 아닌 세 문제:

- **초기 미끄러짐 감지.** 물체가 움직이기 전에, 접촉면은 중심이 아직 붙어 있는 동안 가장자리
  부터 미끄러지기 시작한다. 그 부분 미끄러짐의 흔적은 조밀한 촉각 신호에는 보이고 다른
  무엇에도 보이지 않는다 — 비전이 움직임을 볼 때쯤이면 물체는 이미 떨어지고 있다. 고해상도
  센서를 쓸 가장 분명한 근거다.
- **접촉 상태 추정.** 시스템이 어떤 이산 접촉 모드에
  있는가 — [[04-robotics/contact-force-tactile|접촉 §1~§2]]의 고착·미끄럼·분리, 그리고 비접촉, 1점, 2점, 선, 안착 같은 과제 수준 상태 —
  는 증거가 대체로 촉각인 *분류* 문제다. 그리고 과제 수준 계획기가 실제로 필요로 하는
  상태이기도 하다.
- **손 안 자세(in-hand pose).** 파지 이후 물체가 *손가락에 대해* 어디 있는가. 비전으로 계획한
  파지가 남기는 오차이자, 삽입이 필요로 하는 바로 그것이다.

셋 중 첫째가 느슨하게 쓰이므로 못을 박아 두자. "미끄러짐"은 한 가지가 아니고, 쓸모 있는 구분은
*접촉면의 상태*와 *물체의 운동* 사이에 있다.

> **미끄러짐과 초기 미끄러짐의 정의.** **총 미끄러짐**(gross slip)은 *상대 운동*이다. 물체가 손가락에 대해, 접촉면 전체에서 한꺼번에 움직인다. **초기 미끄러짐**(incipient slip) — 같은 말로 *부분 미끄러짐* — 은 **접촉면의 상태**이지 운동도 사건도 아니다. 접촉면의 바깥 고리가 활주하는 동안 안쪽 고착 영역은 그렇지 않고, 물체의 알짜 변위는 0이다. 정의 조건이 셋이다. 접촉면이 고착 영역과 미끄럼 고리로 **나뉘므로** 접촉 하나가 동시에 두 접촉 모드에 있다. **물체가 움직이지 않았다** — 물체 속도를 언급하는 정의는 총 미끄러짐을 정의한 것이다. 그리고 그 나눔이 접선력과 쓸 수 있는 마찰력의 *비*로 정해지므로, 절대 하중이 얼마든 같은 $Q/\mu P$에서 도달한다.
>
> $$c = a\left(1 - \frac{Q}{\mu P}\right)^{1/3}, \qquad \frac{A_{\text{slip}}}{A} = 1 - \left(\frac{c}{a}\right)^{2}$$
>
> $a$는 접촉면 반지름, $c$는 고착 영역 반지름, $P$는 법선 하중, $Q$는 접선 하중, $\mu$는 마찰계수다. 유연한 원형 접촉에 대한 Cattaneo–Mindlin 결과이므로 고리가 $Q = 0$에서부터 연속적으로 열리고 고착 영역은 정확히 $Q = \mu P$에서 사라지는데, 거기가 총 미끄러짐이 시작되는 곳이다.
>
> - **예**: $Q/\mu P = 0.50$의 S1. $5\ \mathrm{mm}$ 접촉면에서 고착 반지름이 $3.97\ \mathrm{mm}$, 고리 폭이 $1.03\ \mathrm{mm}$, 접촉 면적의 $37\%$가 활주 중인데 물체는 정지해 있다.
> - **반례**: "촉각 신호가 변했으니 물체가 미끄러지고 있다". 파지력 증가, 재파지, 온도 드리프트도 변화를 만든다. 초기 미끄러짐에는 *공간적 흔적* — 고리 — 이 있고, 그것을 감지한다는 것은 그 고리를 분해한다는 뜻이다. Worked case 3단계의 표가 알고리즘이 아니라 센서에 대한 진술인 이유가 그것이다.
> - **왜 중요한가**: §1의 표에서 아직 일어나지 *않은* 것으로 정의되는 유일한 양이고, 운동을 보고하는 어떤 모달리티도 그것을 공급할 수 없는 이유가 정확히 그것이다. 그리고 문턱값이 비이기 때문에, $Q/\mu P = 0.074$에서 고리를 처음 분해하는 센서는 파지력이 얼마든 접선 예산의 $93\%$를 경고 시간으로 준다. 물체 무게를 언급하지 않고 말할 수 있는 쓸 만한 여유다.

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
  0.5 mm 부근). 인간 기준선으로 2점 수치를 인용한 논문은 **오염된 측정을 인용한 것**이고, 센서와 인간의
  비교가 어느 쪽으로든 틀어질 수 있다(격자 역치는 van Boven & Johnson 1994: 손끝 0.94 mm, 입술 0.51 mm, 혀 0.58 mm).

**Two-point limen** 자체는 [[04-robotics/haptics-teleoperation/tactile-display-design|24.2 촉각 디스플레이 설계 §3]]이
완전히 정의하고 설계 제약으로 유도한다. 액추에이터 수와 무관하게 tactor 배열이 쓸 수 있는
*위치*의 수를 그것이 제한한다. 명시된 신체 부위와 명시된 접촉 조건 아래 사람에 대한 성질이고,
여기서 다시 유도하지 않는다. 이 페이지가 갚아야 할 것은 그 비교의 반대쪽 — 센서 쪽 숫자다.

> **공간 해상도의 정의.** 촉각 센서의 **공간 해상도**는 *거리*다. 접촉면 위 특징 둘을 여전히 둘로 보고할 수 있는 최소 간격. 피치도, 채널 수도, 감지 면적도 아니다. 정의 조건이 셋이고 셋 다 숫자와 함께 밝혀야 한다. **표집**이 아래에서 막는다 — 특징 주기당 표본이 적어도 둘이어야 하므로 피치 $p$의 격자에 대해 $d \ge 2p$다. **번짐**이 또 한 번 아래에서 막는다 — 접촉과 변환기 사이의 유연층이 패턴을 저역 통과시키고, 젤이 이미 뭉갠 것은 어떤 표집으로도 되살아나지 않는다. 그리고 **명시된 면적** 위에서 재야 한다. $2.7\ \mathrm{cm^2}$ 위에서 $0.13\ \mathrm{mm}$를 분해하는 센서와 손 전체에서 그것을 분해하는 센서는 비교 가능한 장치가 아니기 때문이다.
>
> $$d_{\min} = \max\left(2p,\ d_{\text{blur}}\right)$$
>
> $p$는 표집 피치, $d_{\text{blur}}$는 유연층을 통과해 살아남는 최소 간격이다. 그러므로 해상도 수치는 독립인 한계 둘의 *최댓값*이고, 표집 쪽만 인용하는 것은 성능의 상한일 뿐 결코 측정값이 아니다.
>
> - **예**: S1의 광학 센서, 표집만으로 $2 \times 0.0634 = 0.127\ \mathrm{mm}$, 면적은 $2.66\ \mathrm{cm^2}$다. 손끝의 $0.94\ \mathrm{mm}$보다 $7.4$배 곱고, 몸의 $0.015\%$ 위에서 그렇다.
> - **반례**: "해상도 $0.0634\ \mathrm{mm}$". 그것은 피치이고, 번짐을 따지기도 전에 해상도를 정확히 두 배 부풀린다. $4\times4$ 택셀 배열은 반대쪽 끝의 같은 오류다. 채널 $16$개는 지도처럼 들리고, $10\ \mathrm{mm}$ 패치 위의 $9.30\ \mathrm{mm}$는 방향이 붙은 숫자 하나다.
> - **왜 중요한가**: 센서의 해상도와 사람의 limen이 모든 "사람 수준 촉각" 주장의 양 끝이고, 둘 다 조건을 함께 인용해야 하는 거리다. Worked case 3단계가 센서 쪽 끝을 과제 문턱값으로 바꾼다. 주어진 센서가 초기 미끄러짐을 보기나 하는지는 이 숫자를 고리 폭에 견주어 정해지고, 택셀 배열은 아무리 빨리 돌아도 기하에서 그 시험에 떨어진다.

설계상의 귀결은 해상도가 미덕이 아니라 *과제* 목표라는 것이다. 패널 모서리를 다루거나 앵커를
안착시키는 건설 그리퍼는 손가락 전체에 손끝 수준의 예민도가 필요하지 않다. 과제를 가르는 접촉
패치를 분해할 만큼만 있으면 된다. **패치를 먼저 정하고 센서를 정하라.** 그리고 어떤 센서의 해상도
수치를 인용하든 [[01-canonical-papers/notes/7-robotics/gelsight|GelSight]] 노트의 경고를 적용하라 —
그 수치가 논문의 어느 부분에서 왔는지 알고 써라. 그 초록에는 수치가 하나도 없다.

### 4. 시촉각 융합 — 그리고 그것이 실제로 사는 것

> **시촉각 융합의 정의.** **융합**(fusion)은 *센서 스트림 여럿에서, 뒷단이 소비하는 양 하나 또는 표현 하나로 가는 사상*이다. 이어 붙이기도, 네트워크 구조도, ablation도 아니다. 정의 조건이 셋이다. 스트림들이 **같은 것에 관한 것**이어야 한다 — 같은 자세, 같은 접촉 상태, 같은 순간 — 그래서 아래 기준 논문에서 시간 정렬이 세부사항이 아니라 학습 목적함수다. 각 스트림이 **신뢰도를 반영한 가중치**로 들어와야 한다. 명시된 분산에서 계산하든, 학습하든, 모드로 게이팅하든 상관없다. 가중 없는 결합은 융합이 아니라 평균이다. 그리고 출력이 **하나**여야 한다. 정책이 알아서 정리하라고 나란히 둔 스트림 둘은 융합이 아니라 *입력*이다.
>
> $$\hat x = \frac{\sigma_v^{-2}x_v + \sigma_t^{-2}x_t}{\sigma_v^{-2} + \sigma_t^{-2}}, \qquad \sigma_{\text{fused}}^{-2} = \sigma_v^{-2} + \sigma_t^{-2}$$
>
> 한 스칼라에 대한 독립이고 불편인 추정 $x_v, x_t$가 분산 $\sigma_v^2, \sigma_t^2$을 가질 때의 해석적 경우다. 독립인 *정밀도*가 더해지기 때문이고, 같은 두 스트림에 대한 어떤 학습된 융합도 이것을 상대로 겨룬다.
>
> - **예**: S1의 손 안 오프셋. $\sigma_v = 2.0\ \mathrm{mm}$와 $\sigma_t = 0.2\ \mathrm{mm}$가 $w_t = 0.990$과 $\sigma_{\text{fused}} = 0.199\ \mathrm{mm}$를 준다 — 비전보다 $10.05$배, 촉각보다 $1.005$배 낫다.
> - **반례**: 가중 없는 평균, $\sigma = \sqrt{(\sigma_v^2 + \sigma_t^2)/4} = 1.005\ \mathrm{mm}$ — **더 나은 센서 하나보다 다섯 배 나쁘다.** 모달리티를 더하는 것은 단조가 아니다. 어떤 스트림을 무시하는 법을 배우지 못하는 융합 구조는 그 스트림을 지운 쪽에 질 수 있고, §6의 비전만·촉각만 ablation이 검사하는 것이 정확히 그것이다.
> - **왜 중요한가**: 천장을 정한다. 한 모달리티가 압도하는 양에서는 최적 융합이 1퍼센트의 몇 분의 일짜리이므로, 큰 이득을 보고하는 융합 논문은 같은 양의 추정 둘을 합쳐서 그 이득을 얻고 있는 것이 *아니다*. 모달리티들이 서로 다른 양을 덮어서, 자기지도 학습 신호가 늘어서, 아니면 표현 덕분에 얻고 있다 — 그리고 그 셋은 실패 모드가 셋인 서로 다른 주장이다.

여기서의 기준 결과는 Lee 등의 *Making Sense of Vision and Touch*다. RGB, 힘/토크, 고유수용
감각으로부터 하나의 압축된 잠재 표현을 학습한다. 학습에는 **자기지도** 목적함수를 쓴다: 기록된 데이터에
이미 들어 있는 것을 예측 대상으로 삼으므로 사람의 라벨이 필요 없다. 여기서는 세 가지 — 행동 조건부 광학 흐름, 다음 제어 단계의 접촉 여부, 그리고 시각과 힘 스트림의 시간 정렬 여부 — 를 예측한다.

그다음에야 표현을 쓴다: 원 입력이 아니라 그 잠재 공간에서 강화학습(시행착오로 보상을 최대화하는 학습,
[[02-foundations/rl-basics|7. 강화학습 기초]])으로 정책을 학습한다. 주장의 구조를
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
> 앞선다고 보고하며, 이는 모든 모델이 과제별 라벨 데이터의 33~50%만 볼 때의 결과다. 이질적인 6개 과제에 걸친 **상대 개선의 평균**이지 성공률도 퍼센트 포인트
> 상승도 아니다 — 퍼센트 포인트 상승*인* [[01-canonical-papers/notes/7-robotics/mobile-aloha|Mobile ALOHA의 "최대 90%"]]와는 다르고,
> 둘 다 성공률로 오독되기 쉽다. 인용 전에 과제별 표로 가라.

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
- [ ] 센서의 피치를 해상도로 바꾸고, 해상도를 막는 두 번째 것을 댄다.
- [ ] 변환 계열의 통과대역이 무엇을 정하는지, 그리고 어느 계열이 쥐고 있는 힘을 보고할 수 없는지 말한다.
- [ ] 초기 미끄러짐이 무엇*의* 상태인지, 그리고 그것을 감지하려면 무엇을 분해해야 하는지 말한다.
- [ ] 센서 지연 때문에 촉각이 충격 생존 기제가 아니라 결정 신호인 이유를 설명한다.
- [ ] 시촉각 융합이 보통 사는 것과 사지 못하는 것을 말한다.
- [ ] 융합 논문의 주장이 읽히려면 필요한 두 ablation을 댄다.

> [!tip] 더 깊이 · Going deeper
> 교과서는 없고, 센서가 곧 문헌이다. 물리에서 시작하라: Johnson & Adelson(CVPR 2009)의 retrographic sensing이 광학 원리이고, 아직 아무도 로봇에 붙이기 전이다. 그다음 Yuan, Dong, Adelson(*Sensors* 2017)으로 기하와 힘을 재는 로봇 센서로서의 GelSight를, DIGIT(*RA-L* 2020)으로 이 모달리티를 흔하게 만든 값싸고 작은 형태를. 그다음 Lee 외(ICRA 2019)로 촉각을 만드는 것이 아니라 쓰는 쪽을. 이 신호가 먹여 주는 조작 이론 쪽은 [[04-robotics/contact-force-tactile|9. 접촉의 '더 깊이']]가 자기 교재를 지목한다. 이 페이지에는 자기 것이 없다.

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
> 3. 30 fps면 샘플이 33 ms마다 오는데, 단단한 접촉 천이는 실제 팔의 맨 공구에서 약 14 ms, 이상화한 강체 경우 약 1.4 ms에 끝난다([[04-robotics/force-compliance-control|13. §5]]) — 사건 전체가 두 프레임 사이에서 일어난다. 센서는 접촉이 *어땠는지*를 보고할 수 있고 그것은 다음 행동을 정하는 데 유용하지만, 충격 자체를 조절하는 데 참여할 수는 없다. 그 일은 수동 컴플라이언스와 킬로헤르츠 토크 루프의 몫이다.
> 4. 그리퍼 자신의 무게와 페이로드를 센서 프레임으로 사영해서 빼야 한다 — 그리고 그것은 팔의 방향에 의존한다. 중력은 월드 프레임에 고정되어 있고 센서는 손목과 함께 회전하기 때문이다. 같은 부재를 잡아도 자세마다 원 측정값이 다르므로, 중력 보상에는 현재 기구학이 필요하다([[02-foundations/manipulator-kinematics-dynamics|10. §5]]). 가속 중에는 관성 항도 들어온다.
> 5. 범위 안: 기존 촉각 센서를 써서 체결을 견고하게 만드는 것 — 접촉 상태 분류, 그것에 따라 행동하는 정책, 실제 체결구에 대한 평가. 범위 밖: 새 센서를 설계하거나 제작하는 것. [[07-research-program/index|§7]]이 이를 제외하는 이유는 그것이 자기 문헌과 자기 실패 모드를 가진 별개의 기여이기 때문이다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, **S1**만 쓴다. 손잡이 셋만 움직이고 나머지는 그대로다. 손가락이 작아져 접촉면 반지름이 $a' = 3\,\mathrm{mm}$이고 $P = 5\,\mathrm{N}$, $\mu = 0.5$는 같다. 택셀 배열을 같은 $18.6\times14.3\,\mathrm{mm}$ 위에 $8\times 8$로 다시 만든다. 전하 증폭기를 같은 $C_f$에 $R_f' = 1\,\mathrm{G\Omega}$으로 다시 만든다. 접선 하중이 이제 0에서 $5\,\mathrm{N/s}$로 올라가고, 손목 카메라를 재보정해 깊이 잡음이 $\sigma_v' = 0.8\,\mathrm{mm}$로 떨어진다. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** 과제 그림의 패널 셋을 새 숫자로. $3\,\mathrm{mm}$ 접촉면에 표집 격자 둘과 그 아래 해상도 막대 셋, $Q/\mu P = 0.25$와 $0.50$에서의 고착 영역과 고리, 그리고 $\tau'$와 반감기를 표시한 새 감쇠 곡선. 작은 네 번째 패널을 더한다. $0$부터 $0.5\,\mathrm{s}$까지의 시간 축에 각 센서가 고리를 처음 분해하는 순간을 찍고, 오른쪽 끝에 총 미끄러짐 순간을 찍는다.
2. **유도.** (a) 새 택셀 피치와 해상도, 그리고 손끝 $0.94\,\mathrm{mm}$에 대한 비. (b) $\tau'$, $f_c'$, $t = 1\,\mathrm{s}$와 $t = 5\,\mathrm{s}$에서 일정한 $5\,\mathrm{N}$ 쥠의 값, 그리고 $80\,\mathrm{Hz}$와 $1\,\mathrm{Hz}$에서의 $|H|$. (c) 광학 센서와 새 택셀 배열 각각에 대해, $3\,\mathrm{mm}$ 접촉면에서 고리가 자기 해상도에 처음 닿는 $Q/\mu P$ — 또는 결코 닿지 않는다는 진술. (d) (c)를 $5\,\mathrm{N/s}$ 램프 아래 초로 바꾼다. 감지 순간, 총 미끄러짐 순간, 그 사이 경고 시간을 밀리초와 $30\,\mathrm{Hz}$ 프레임 수로. (e) $\sigma_v' = 0.8\,\mathrm{mm}$에서의 융합 $\sigma$와 $w_t$, 그리고 가중 없는 평균의 $\sigma$.
3. **해석.** §2의 지연 상자는 프레임당 $33\,\mathrm{ms}$인 광학 촉각 센서가 $14\,\mathrm{ms}$ 접촉 천이에 참여할 수 없다고 말한다. (d)의 답은 총 미끄러짐 전에 여러 프레임의 경고가 있다고 말한다. 둘을 한 문장으로 조정하라. 그다음 손잡이 셋 중 숫자가 아니라 *판정*을 바꾼 것이 무엇인지, 그리고 그것이 "더 빠른 센서로 미끄러짐 감지를 개선했다"는 문장에 무엇을 함의하는지 말하라.

> [!tip]- 정답 · Solutions
> 1. 원래 그림의 $9.30\,\mathrm{mm}$ 막대가 $4.65\,\mathrm{mm}$가 되는데 그래도 $3\,\mathrm{mm}$ 접촉면 전체보다 넓다 — 급소가 손잡이를 견디고 살아남는다.
> 2. (a) 피치 $18.6/8 = 2.325\,\mathrm{mm}$, 해상도 $4.65\,\mathrm{mm}$로 손끝보다 $4.95$배 거칠다. $4\times4$ 배열의 $9.89$배보다 두 배 낫고, 여전히 피부보다 거칠다. (b) $\tau' = 10^9 \times 10^{-9} = 1.00\,\mathrm{s}$, $f_c' = 1/(2\pi) = 0.159\,\mathrm{Hz}$. 쥠이 $1\,\mathrm{s}$에 $5e^{-1} = 1.84\,\mathrm{N}$, $5\,\mathrm{s}$에 $5e^{-5} = 0.034\,\mathrm{N}$. $|H(80)| = 1.0000$, $|H(1)| = 0.988$. 빨라진 증폭기는 쥠을 열 배 일찍 잃고 $80\,\mathrm{Hz}$에서는 아무것도 얻지 못했다. (c) 광학은 $1 - ((3 - 0.1268)/3)^3 = 0.1215$. 택셀은 해상도 $4.65\,\mathrm{mm} \ge a' = 3\,\mathrm{mm}$이므로 분해 가능한 가장 미세한 특징이 고리가 도달할 수 있는 최대 폭보다 넓다 — **결코**, $1\,\mathrm{kHz}$에서도, 채널이 네 배가 되어도. (d) $\mu P = 2.5\,\mathrm{N}$이므로 총 미끄러짐이 $2.5/5 = 0.500\,\mathrm{s}$. 광학은 $0.1215 \times 0.500 = 0.0608\,\mathrm{s}$에 감지하므로 경고 시간이 $439\,\mathrm{ms}$, $30\,\mathrm{Hz}$에서 $13.2$ 프레임이다. (e) $w_t = 25/(1.5625 + 25) = 0.941$, $\sigma_{\text{fused}} = 0.194\,\mathrm{mm}$ — 여전히 촉각만보다 $1.031$배 나을 뿐이다. 가중 없는 평균은 $\sqrt{(0.64 + 0.04)/4} = 0.412\,\mathrm{mm}$로 촉각만보다 $2.06$배 나쁘다. 카메라 잡음을 반으로 줄인 것은 가중 없는 융합을 덜 파국적으로 만들었을 뿐 쓸모 있게 만들지 못했다.
> 3. 두 진술은 센서가 아니라 지속 시간이 다른 사건들에 관한 것이다. 충격은 $14\,\mathrm{ms}$에 끝나고 초기 미끄러짐은 $439\,\mathrm{ms}$ 동안 이어지므로, 같은 $33\,\mathrm{ms}$ 프레임이 하나에는 한참 느리고 다른 하나에는 필요보다 열세 배 빠르다. 판정을 바꾼 손잡이는 **접촉면 반지름**이다. 택셀 배열을 "고리를 결코 분해하지 못함"에서 — 여전히 못하지만 이제 더 작은 차이로 — 밀었고, 배열이 피치 $1.5\,\mathrm{mm}$보다 곱게 갔다면 뒤집혔을 것이다. 증폭기와 카메라는 숫자만 움직였다. 그래서 "더 빠른 센서로 미끄러짐 감지를 개선했다"는 문장이 그 자체로 의심스럽다. 주파수는 4단계 질문의 답이고 초기 미끄러짐은 3단계의 질문이므로, 초기 미끄러짐 감지를 개선한 주파수 개선은 아마 다른 무언가를 개선하고 있었다.

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
