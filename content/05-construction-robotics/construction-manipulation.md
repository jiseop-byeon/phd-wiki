---
title: 9. Construction Manipulation
tags: [construction-robotics, manipulation]
study-depth: Mastery
wiki-support: Working
depth-goal: "Map a construction task to the manipulation primitives, sensing, and control mode it needs; place any paper on the simulation–lab–site ladder; and pick a defensible core task."
mastery-when: "This is the intersection the research program is built on — the page exists to make a task choice defensible."
---

> [!abstract] Depth target · 깊이 목표
> **Mastery** — this is where the manipulation track and the construction domain meet, and
> the choice made here decides what the rest of the dissertation is about.
> **Mastery** — 매니퓰레이션 트랙과 건설 도메인이 만나는 지점이고, 여기서의 선택이 나머지
> 학위논문이 무엇에 관한 것인지를 결정한다.

> [!note] Prerequisites · 선수 지식
> You need the manipulation primitives and their control modes ([[04-robotics/force-compliance-control|13]], [[04-robotics/grasping|15]]), what touch adds ([[04-robotics/tactile-visuotactile|14. §1]]), and the construction assembly lineages ([[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]]).
> 조작 원시동작과 그 제어 모드([[04-robotics/force-compliance-control|13]], [[04-robotics/grasping|15]]), 촉각이 더하는 것([[04-robotics/tactile-visuotactile|14. §1]]), 건설 조립 계보([[05-construction-robotics/assembly-fabrication|조립·제작]])가 필요하다.

## English

> [!note] First pass · 처음이라면
> Read the Running object and look at the picture: the same S1 panel as [[05-construction-robotics/site-engineering|2.5]] and [[05-construction-robotics/assembly-fabrication|4]], followed to the instant its hole meets a locating pin. Then §1 and §2 for why construction contact differs from factory contact and which task needs what, and the Worked case after §3 for the four numbers that decide whether the panel seats. §3–§6 are what you read when choosing a dissertation task rather than learning the mechanics.

### Running object · 이 페이지의 대상

**S1** from [[05-construction-robotics/site-engineering|2.5 Site Robotics as an Engineering System]]: the $20\,\mathrm{kg}$ facade panel with two mounting holes $400\,\mathrm{mm}$ apart, followed past transport and alignment to the moment of contact, when each hole has to drop over a locating pin on its bracket. Everything before this moment is geometry; this is where it becomes manipulation.

| Symbol | Value | What it is |
|---|---:|---|
| error budget | map $1$, base $2$, arm $1$, tool $0.5$, part $1\,\mathrm{mm}$ | S1's allocation (2.5 §2), read here as a two-sigma bound per horizontal axis for each source |
| $D,\ d$ | $18$, $16\,\mathrm{mm}$ | hole and pin diameters: a bolt-clearance fit, diametral clearance $\Delta=2\,\mathrm{mm}$ |
| $r_c$ | $4\,\mathrm{mm}$ | the radial error the pin's tapered nose can capture |
| $\mu$ | $0.3$ | friction, steel on dusty steel |
| $K_{\text{stiff}}$ | $10^5\,\mathrm{N/m}$ | a position-controlled arm pressed into steel: the series stiffness of [[04-robotics/force-compliance-control\|13]]'s running object |
| $K_d$ | $500\,\mathrm{N/m}$ | a lateral target impedance, 13's $K_d$ |
| $W$ | $196\,\mathrm{N}$ | the panel's weight, $20\times9.81$ |

Reading the allocations as two-sigma bounds is this page's choice. 2.5 leaves it open, and its §2 is exactly the warning that the reading has to be stated. The pin, the lead-in and $\mu$ are this page's frozen numbers; everything else is S1 or catalog.

*Scope: this page maps construction tasks to manipulation needs, places evidence on the simulation–lab–site ladder, and prices one contact event on S1. It does not teach impedance and admittance control ([[04-robotics/force-compliance-control|13]]), grasp quality ([[04-robotics/grasping|15]]) or base placement ([[04-robotics/navigation-mobile-manipulation|16]]); it uses their numbers.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="Left: circles centred on a mounting hole showing the 4 mm lead-in capture radius, the 95th-percentile position error of 3.29 mm in the lab and 6.51 mm on site, and the 5.5 mm linear error sum. Right: on a logarithmic force axis, the sideways push at the 95th-percentile error is 329 N for a stiff arm and 1.6 N for a laterally compliant one, against the 196 N panel weight.">
<text x="20" y="22" font-size="12.5" fill="currentColor" font-weight="600">where the pin meets the hole (mm)</text>
<circle cx="140" cy="150" r="68.0" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-opacity="0.5"/>
<circle cx="140" cy="150" r="55.9" fill="none" stroke="currentColor" stroke-width="1.6"/>
<circle cx="140" cy="150" r="93.5" fill="none" stroke="currentColor" stroke-dasharray="1.5 3" stroke-opacity="0.8"/>
<circle cx="140" cy="150" r="110.7" fill="none" stroke="currentColor" stroke-dasharray="5 3" stroke-opacity="0.75"/>
<circle cx="140" cy="150" r="2.5" fill="currentColor"/>
<line x1="38.0" y1="268" x2="38.0" y2="272" stroke="currentColor"/><text x="38.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−6</text>
<line x1="72.0" y1="268" x2="72.0" y2="272" stroke="currentColor"/><text x="72.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−4</text>
<line x1="106.0" y1="268" x2="106.0" y2="272" stroke="currentColor"/><text x="106.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−2</text>
<line x1="140.0" y1="268" x2="140.0" y2="272" stroke="currentColor"/><text x="140.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="174.0" y1="268" x2="174.0" y2="272" stroke="currentColor"/><text x="174.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<line x1="208.0" y1="268" x2="208.0" y2="272" stroke="currentColor"/><text x="208.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">4</text>
<line x1="242.0" y1="268" x2="242.0" y2="272" stroke="currentColor"/><text x="242.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">6</text>
<line x1="38.0" y1="268" x2="242.0" y2="268" stroke="currentColor" stroke-opacity="0.6"/>
<rect x="262" y="41" width="22" height="10" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-opacity="0.5"/><text x="290" y="50" font-size="11" fill="currentColor">lead-in captures r ≤ 4</text>
<line x1="262" y1="64" x2="284" y2="64" stroke="currentColor" stroke-width="1.6"/><text x="290" y="68" font-size="11" fill="currentColor">lab 95%: 3.29</text>
<line x1="262" y1="82" x2="284" y2="82" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3"/><text x="290" y="86" font-size="11" fill="currentColor">site 95%: 6.51</text>
<line x1="262" y1="100" x2="284" y2="100" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 3"/><text x="290" y="104" font-size="11" fill="currentColor">linear sum: 5.5</text>
<text x="262" y="126" font-size="11" fill="currentColor" font-weight="600">lab: 97.6% of panels seat</text>
<text x="262" y="142" font-size="11" fill="currentColor">site (base error 5 mm): 46%</text>
<text x="262" y="182" font-size="12.5" fill="currentColor" font-weight="600">sideways push at the 95th-percentile error</text>
<rect x="262" y="194" width="216.5" height="16" fill="currentColor" fill-opacity="0.55"/>
<rect x="262" y="238" width="17.6" height="16" fill="currentColor" fill-opacity="0.55"/>
<text x="262" y="226" font-size="11" fill="currentColor">stiff arm, 10<tspan dy="-4" font-size="9">5</tspan><tspan dy="4" dx="2"> N/m: 329 N</tspan></text>
<text x="262" y="270" font-size="11" fill="currentColor">lateral impedance, 500 N/m: 1.6 N</text>
<line x1="459.2" y1="190" x2="459.2" y2="278" stroke="currentColor" stroke-dasharray="2 3"/>
<text x="455.2" y="290" font-size="10.5" fill="currentColor" text-anchor="end">panel weight 196 N</text>
<line x1="262.0" y1="294" x2="262.0" y2="298" stroke="currentColor"/><text x="262.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="348.0" y1="294" x2="348.0" y2="298" stroke="currentColor"/><text x="348.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">10</text>
<line x1="434.0" y1="294" x2="434.0" y2="298" stroke="currentColor"/><text x="434.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">100</text>
<line x1="520.0" y1="294" x2="520.0" y2="298" stroke="currentColor"/><text x="520.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">1000 N</text>
<line x1="262" y1="294" x2="520" y2="294" stroke="currentColor" stroke-opacity="0.6"/>
</svg>

S1 at the instant a hole meets its pin. With the lab error budget, 95% of holes arrive within $3.29\,\mathrm{mm}$, inside the $4\,\mathrm{mm}$ the pin's lead-in captures, so $97.6\%$ of panels seat; if the base error grows to $5\,\mathrm{mm}$ on site, the 95% circle grows to $6.51\,\mathrm{mm}$ and only $46\%$ do. On the right is what the arm pushes sideways while the lead-in corrects a 95th-percentile error: a stiff arm leans on the building with more than the panel's own weight, a compliant one with about a newton and a half.

### 1. Why construction manipulation is its own problem

[[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]] now works **S1**
as a two-hole alignment course, then maps the domain's *lineages*. This page takes
the other cut: **what the robot's hand actually has to do**, task by task, and what each
task demands of the pages in the manipulation track.

The difference from factory manipulation is not that construction is harder in a vague way.
It is specific, and each item removes an assumption that factory robotics is allowed to make:

| Factory assumption | What construction supplies instead |
|---|---|
| The part is in a fixture, at a known pose | The part is where someone put it, within centimetres |
| The workpiece is rigid and dimensioned | Panels flex, bundles of rebar (steel reinforcing bars) shift, membranes drape |
| The environment is the same every cycle | Two instances of the same task differ; the building changes as it is built |
| The robot is bolted down | The base moved to get here, and its pose is part of the error budget |
| No one is inside the workspace | Trades are working alongside, and safety is regulated |
| $\mu$ (the friction coefficient, [[04-robotics/grasping\|15. §2]]), mass, and geometry are known | Dust, moisture, and tolerance make all three uncertain |

Row 1 makes pure hybrid position/force control **with a fixed, presumed contact normal**
fragile: its selection matrix depends on that frame ([[04-robotics/force-compliance-control|13. §3]]).
Check when the paper estimates or updates the normal and how it switches control modes around contact;
online frame updates, compliant control, and low approach stiffness can mitigate the error.

### 2. The task matrix

Construction tasks, decomposed into the manipulation primitives from the track. Read a row
as a specification: it says which pages a project on that task will need at depth.

| Task | Primitive | Decisive sensing | Control mode | Hardest uncertainty |
|---|---|---|---|---|
| **Anchor-bolt setting, overhead drilling** | drill, push | position + force; thrust | force along the bit axis | arm deflection under thrust; ceiling material varies |
| **Panel / curtain-wall installation** | grasp, transport, fit | vision + force | compliant fitting, low stiffness | part is large and flexible; base pose error dominates |
| **Drywall hanging** | grasp, hold, fasten | vision + force | position for hold, force for fastening | sheet flexes; overhead hold is a strength problem |
| **Drywall finishing** | sand, scrape | force / depth control | force normal to the surface | material removal depth is the spec, and it is sub-millimetre |
| **Rebar tying** | reach, wrap, cut | vision to find intersections | mostly position, light contact | mesh is non-rigid and shifts; thousands of repetitions |
| **Pipe / conduit fitting** | insert, align | force + tactile | impedance, low stiffness | wedging and jamming ([[04-robotics/force-compliance-control\|13. §5]]) |
| **Bolted steel connection** | align, insert, torque | force + torque | hybrid: position across, force along | heavy parts; the crane or base is compliant |
| **Timber joint assembly** | insert with interference | force/torque | learned or compliant insertion | tolerance and shape vary piece to piece |
| **Bricklaying, block placement** | grasp, place | vision | position | mostly a weight and cycle-time problem, not a contact problem |
| **Welding structural steel** | track a seam | vision + seam tracking | position along a tracked path | joint geometry varies; the work is hot and the standards are strict |

The table uses two construction terms worth saying plainly. *Rebar tying* joins steel reinforcing
bars into a grid by wrapping wire around each crossing, before concrete is poured around
them. A *curtain wall* is a building's non-structural outer skin of glass and metal panels
hung from the structure, so installing one means moving large, heavy modules into place.

Two rows in that table are not contact-rich, and saying so is part of the point. Bricklaying
and most placement tasks are solved geometry with a payload problem attached; they belong to
the domain but not to this dissertation's core, by the admission test in
[[07-research-program/index|7. §7]].

The matrix is useful because a task label hides the variable that determines failure. For example, pipe insertion and brick placement can both look like pick-and-place in a video, while only the former may require detecting a jam during contact. **The reading this gives you.** Choose the row by the failure mechanism and required feedback, not by the visual similarity of the arm motion. Then ask whether the proposed sensor actually observes that mechanism.

### 3. The ladder — and the finding that should shape a topic choice

This wiki insists on distinguishing **simulation**, **laboratory or mock-up**, and **active
construction site**. Applied to contact-rich construction manipulation, that distinction
produces a striking result.

<svg viewBox="0 0 560 232" style="max-width:100%;height:auto" role="img" aria-label="three rungs of evidence with most work on the lower two and almost nothing on an active site">
  <g fill="currentColor">
    <rect x="40" y="146" width="440" height="40" rx="3" fill-opacity="0.08"/>
    <rect x="88" y="98" width="392" height="40" rx="3" fill-opacity="0.16"/>
    <rect x="360" y="50" width="120" height="40" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="40" y="146" width="440" height="40" rx="3"/><rect x="88" y="98" width="392" height="40" rx="3"/><rect x="360" y="50" width="120" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="52" y="163">simulation</text>
    <text x="52" y="178" font-size="9.5" opacity="0.75">unlimited trials, chosen physics</text>
    <text x="100" y="115">laboratory or mock-up</text>
    <text x="100" y="130" font-size="9.5" opacity="0.75">real contact, arranged conditions &#8212; where nearly all of this work sits</text>
    <text x="372" y="67">active site</text>
    <text x="372" y="82" font-size="9.5" opacity="0.75">nearly empty</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="208">A targeted search of drilling, drywall, rebar, facade, timber and welding identified three papers that put</text>
    <text x="20" y="224">a manipulator on an active construction site, the oldest from 2007. Treat this as a candidate gap, not an exhaustive count.</text>
  </g>
</svg>

Three verified exceptions stand out. Feng et al. (2024) report a planar rebar-tying robot
validated first on a rebar-mesh demonstration platform and then applied in the field on the
Shenyang Hunnan Science and Technology City Phase IV project. Dörfler et al. (2019) drove
the In situ Fabricator through the Mesh Mould wall of the DFAB HOUSE at NEST — a mobile
manipulator bending and welding rebar in place, in a permitted building that is now
occupied. Yu et al. (2007) built a curtain-wall installation robot on an excavator base and
tested it on a construction site — the title says so — but it is nearly twenty years old.

**What that search excludes, so you can disagree with the scope rather than the count.** It
is a search of the *modern* literature under six task keywords, and it therefore does not
reach the Japanese **STCR era** — the dozens of single-task construction robots Shimizu,
Obayashi, Kajima and peers ran on live sites in the 1980s–90s, whose record lives in the proceedings of ISARC (the International Symposium on Automation
and Robotics in Construction) and Bock's reference volumes ([[05-construction-robotics/lineage|lineage, Era 1]]). Those machines were on real sites and are deliberately outside this count: they
are single-task automation without the contact control, force sensing or learning this page
is about. Read the finding as "three papers in the contact-rich manipulation literature",
not as "three robots ever".

Everything else that is technically strong stops at the lab or a mock-up. Do not take a
title as evidence of where the work happened: read the methods section for a sentence that
names the location. The strongest overhead-drilling result, Kindle et al., is evaluated on
datasets recorded under *simulated* site disturbances — not on a site.

**When and where that count was made, so it can be rerun.** The six-keyword search was run in
August 2026 against arXiv and Crossref, and rerun in September 2026. The rerun surfaced two
2025 papers under the same keywords that are not in the count and should not be added until
the location test above is applied to them: a hexapod curtain-wall installation robot
([arXiv:2509.13595](https://arxiv.org/abs/2509.13595)), whose abstract describes experiments
on the robot and names site deployment as future work, so it reads as a laboratory result; and
an ISARC 2025 drywall-panel installation robot (doi:10.22260/isarc2025/0058), whose abstract
could not be retrieved, so where its experiments happened is unverified. A count that is not
dated cannot be disagreed with, and this one is meant to be.

> [!important] What to do with that finding
> Read it as a research opportunity, not as permission to skip the rung. The reason the top
> rung is empty is that it is genuinely hard — access, safety, schedule, and a building that
> will not wait. A dissertation that reaches an active site with a contact-rich task is
> making a claim almost nobody else can make. A dissertation that *says* "on-site" about
> mock-up work is joining the pattern this page exists to name.

### Worked case · 대상으로 한 번 끝까지

Five steps on S1 at the pin, then what changes on site. The lab code in the problem set reproduces every number by sampling.

**Step 1 — the budget, read two ways.** Added linearly, the five allocations come to $5.5\,\mathrm{mm}$, more than the $4\,\mathrm{mm}$ the lead-in captures, so a worst-case reading says the panel never seats reliably. Read as independent two-sigma bounds, they combine by root-sum-square to $\sqrt{1+4+1+0.25+1}=2.69\,\mathrm{mm}$ per axis, a per-axis standard deviation $\sigma=1.35\,\mathrm{mm}$. Neither reading is mere arithmetic; each is a claim about the errors (2.5 §2), and the rest of the case uses the second.

**Step 2 — will the hole be captured?** With independent, equal errors in the two horizontal axes, the radial distance $r$ of a hole from its pin follows a Rayleigh distribution, so the probability that it lands inside the lead-in is

$$P(r\le r_c)=1-e^{-r_c^2/2\sigma^2}=1-e^{-16/3.62}=0.988$$

per hole, and $0.988^2=0.976$ for a panel whose two holes err independently. Ninety-five percent of holes arrive within $3.29\,\mathrm{mm}$, which is $2.45\sigma$. About one panel in forty misses a pin: often enough that the system needs a detected, recoverable miss (S1's *retreat and rescan*), not an assumption that it never happens.

**Step 3 — how hard does the arm push while the lead-in corrects?** The taper turns the error into a sideways displacement the arm must allow. Held by a stiff position loop, the arm resists with the series stiffness of the structure: at the 95th-percentile error of $3.29\,\mathrm{mm}$, $F=K_{\text{stiff}}\,r=10^5\times0.00329=329\,\mathrm{N}$, **1.7 times the panel's own weight**, pushed sideways into a bracket bolted to the building. With a lateral target impedance $K_d=500\,\mathrm{N/m}$ the same correction costs $1.6\,\mathrm{N}$. This is why the task matrix of §2 lists *compliant fitting, low stiffness* for panel installation: the lead-in does the aligning only if the arm lets it.

**Step 4 — but not compliant everywhere.** The same $500\,\mathrm{N/m}$ vertically would let a $5\%$ error in the payload estimate, $9.81\,\mathrm{N}$, sag the panel $9.81/500=19.6\,\mathrm{mm}$, four times the tolerance. Holding $1\,\mathrm{mm}$ against that error needs $9.81/0.001=9{,}810\,\mathrm{N/m}$ vertically. The target impedance has to be anisotropic, stiff along gravity and soft across the pin. That is 13's selection-matrix idea applied to a panel rather than a peg, and it is why the contact frame must be known (§1).

**Step 5 — wedging needs a tight fit.** Once the pin is in, a tilted panel can still lock. Wedging ([[04-robotics/force-compliance-control|13 §5.2]]) is possible when two-point contact forms at an insertion depth $l<\mu D$, and for a small tilt $\theta$ two-point contact forms at $l\approx\Delta/\theta$, so the danger begins near $\theta=\Delta/(\mu D)$. With the $2\,\mathrm{mm}$ bolt clearance that is $2/(0.3\times18)=0.37\,\mathrm{rad}$, or $21^\circ$, and no panel is hung that crooked. With a $0.2\,\mathrm{mm}$ dowel fit it is $0.037\,\mathrm{rad}$, or $2.1^\circ$, which a flexing panel or an uneven bracket reaches easily. On S1, capture and sideways force are the problems; wedging becomes one only when the fit is precise.

**What moves on site.** Step 2 assumed the lab's $2\,\mathrm{mm}$ base term. On a site where the base re-localizes against a structure that keeps changing, it may be $5\,\mathrm{mm}$. The per-axis $\sigma$ becomes $2.66\,\mathrm{mm}$, the 95% circle $6.51\,\mathrm{mm}$, and the panel capture rate falls from $97.6\%$ to $46\%$; keeping $99\%$ per hole would need a lead-in of $8.1\,\mathrm{mm}$ instead of $4.1$. Nothing about the arm changed, only the rung of §3. This is the quantitative form of why a mock-up result does not transfer to a site, and why the base term of the budget, owned by [[04-robotics/navigation-mobile-manipulation|16]], is a manipulation problem.

### 4. Anchor papers, by what they actually demonstrate

Sorted by rung rather than by fame, because that is the ordering that matters here.

**On an active site**

- **Feng et al. (2024)**, rebar-tying robot with two-stage recognition (depth camera plus
  industrial camera), driving on the rebar mesh. Verified on a demonstration platform and
  then in the field.
- **Dörfler et al. (2019)**, In situ Fabricator building the Mesh Mould wall of the DFAB
  HOUSE — rebar bent and welded in place in a real, permitted, now-occupied building.
- **Yu et al. (2007)**, curtain-wall installation robot on an excavator base, tested on site.

**Real contact, laboratory or full-scale mock-up**

- **Apolinarska et al. (2021)** — timber joint assembly where a policy trained entirely in
  simulation is deployed on hardware, guided by force/torque and pose, and generalises to
  tolerances and shape variations not seen in training. This is construction-scale
  peg-in-hole, and it is the closest thing the field has to a contact-rich learning result.
- **Kindle et al. (RA-L 2025)** — deflection and backlash compensation on a 700 kg tracked
  drilling robot (widely identified as the Hilti Jaibot; the paper itself describes only a
  ~700 kg tracked base with a lifting column, a Doosan manipulator and a drilling end
  effector), evaluated on seven datasets recorded under
  simulated site disturbances. The compliance problem of
  [[04-robotics/force-compliance-control|13]] stated in construction terms.
- **Iturralde et al. (2022)** — a cable-driven parallel robot installing curtain-wall
  modules, tested in two close-to-real demonstration buildings.
- **Chu, Jung et al. (2013)** — the two-part steel-beam bolting system; older, and the
  canonical academic reference for bolted connections.

**Read for framing, not as a manipulation result**

- **Brosque et al. (2023)** compares on-site and off-site drywall solutions on a real
  project — an economics and process evaluation, which is exactly what a manipulation paper
  cannot tell you.
- **Melenbrink, Werfel and Menges (2020)** is the survey to read first: organised by
  construction task rather than by technology, scoped to on-site autonomy, and its gap
  analysis still holds.

> [!warning] Two traps in this literature
> **Press demonstrations get cited as results.** The humanoid widely described as installing
> drywall has a peer-reviewed paper about its *joint design*; the drywall demonstration
> itself is a press video. **And commercial systems have no papers *of their own*.** Jaibot, TyBot,
> Canvas and Okibo are products; their productivity figures are vendor marketing that has
> not been reviewed. Say "of their own" and mean it — the platform in Kindle et al. above is
> widely identified as the Jaibot, so a peer-reviewed paper *about* one of these machines can
> exist while the vendor's own numbers remain unreviewed. Cite the product as a product and
> the paper as a paper — see [[05-construction-robotics/industry-deployment|Industry Deployment]].

### 5. Choosing a task, concretely

Apply the five criteria from [[07-research-program/paper-arc|7.1 §4]] to the matrix in §2.

| Task | Contact essential? | Real tolerance? | Done at scale by hand? | Lab-repeatable? | Failure survivable? |
|---|---|---|---|---|---|
| Anchor-bolt setting | yes | yes, mm | yes | yes | overhead work — needs care |
| Panel fitting | yes | yes, mm | yes | yes | yes |
| Drywall finishing | yes | yes, sub-mm depth | yes | yes | yes |
| Rebar tying | partly | loose | yes, enormously | yes | yes |
| Pipe insertion | yes | yes | yes | yes | yes |
| Bricklaying | no | loose | yes | yes | yes |
| Overhead drilling | yes | yes | yes | yes | dust and falling debris |

Panel fitting, drywall finishing, and pipe insertion clear all five. Rebar tying clears the
scale criterion by a wide margin but is only lightly contact-rich, which makes it a superb
*deployment* target and a weak *contact-manipulation* contribution — and note that it is
also the one task with a site-verified result, which is not a coincidence.

A good starting task exposes the uncertainty you want to study while keeping repeated evaluation feasible. For example, a pipe-fitting setup can deliberately vary alignment while preserving a recoverable failed attempt. **The reading this gives you.** Write the failure you need to reproduce before selecting hardware. If the available setup makes that failure impossible, it may be convenient but cannot test the intended contact-adaptation claim.

### 6. What this domain gives back to the manipulation literature

The relationship runs both ways, and this is the part to say in an introduction. Construction
supplies problems that general manipulation research has no clean way to pose:

- **Unknown, drifting friction** — the $\mu$ that every grasp result in
  [[04-robotics/grasping|15. §2–§4]] takes as given.
- **Non-rigid parts at structural scale** — form and force closure
  ([[04-robotics/grasping|15. §3]]) are defined for a rigid body, whose contact points keep
  fixed positions relative to each other; a 2.4 m sheet is not a rigid body, since it flexes
  and its contact geometry changes under load, so closure is not even defined on it.
- **A workspace that changes because the robot changed it** — the building is the workpiece.
- **Tolerance stacks that no fixture absorbs** — base pose error, part placement error, and
  as-built deviation all land on the same contact.

Each is a defensible robustness claim rather than a domain excuse. That is the difference
the [[07-research-program/index|research program]] is built on.

### After reading

- [ ] Map a named construction task to its primitive, sensing, and control mode.
- [ ] Place any paper in this area on the simulation–lab–site ladder, and say what evidence put it there.
- [ ] Name the three site-verified manipulation cases and distinguish their contact and deployment evidence.
- [ ] Apply the five task-selection criteria and reject at least one tempting task.
- [ ] State two things construction gives back to general manipulation research.

Next, [[05-construction-robotics/imitating-contact|10. Imitating Contact]] keeps this page's pin and lead-in and asks what a policy learned from demonstrations does in S1's last 40 mm: how behaviour cloning's per-step errors compound into millimetres at the pin, and which fix keeps the policy inside the lead-in.

### Self-check

1. Why does hybrid position/force control fail on a construction panel-fitting task that it
   would handle in a factory?
2. A paper's title contains "on-site". What do you check before believing it?
3. Rebar tying carries the strongest site-verified evidence of any §2 task — Feng et al.
   (2024) in the field and Dörfler et al. (2019) welding rebar in place in a permitted
   building. (Panel / curtain-wall installation has one too, Yu et al. 2007, but it is
   nearly twenty years old.) Why is rebar tying *still* a weak choice for this
   dissertation's core contribution?
4. A vendor reports 300 holes per day for a drilling robot. How should that appear in a
   literature review?
5. Which two rows of §2 would you cut first if the dissertation needed narrowing, and why?

> [!tip]- Answers
> 1. A controller that keeps a model-derived contact normal fixed can assign force partly along the surface and position partly into it when the on-site pose differs from the model. The architecture is therefore vulnerable unless the system estimates or updates the contact frame, switches modes around contact, or adds compliance ([[04-robotics/force-compliance-control|13. §3]]).
> 2. The methods and experiments sections, for a sentence naming where the work actually happened. Several papers in this area carry "on-site" in the title and state in their own text that the development and validation were done in a controlled laboratory. The title describes the ambition; the experimental section describes the evidence.
> 3. Because the contact is light. The hard parts of rebar tying are perception (finding intersections on a shifting non-rigid mesh), coverage planning, and doing it thousands of times reliably — which makes it an excellent deployment and autonomy result, but the contribution would not be about contact. Under the admission test it serves the program's *navigation and deployment* pillars more than its manipulation core.
> 4. As a product claim with its source named, never as a result. Jaibot, TyBot, Canvas and Okibo have no peer-reviewed papers of their own, so their productivity figures are marketing that has not been through review. They are legitimate evidence that a market exists and that the task is worth automating — which is a different claim from a measured one.
> 5. Bricklaying and block placement, because they fail the contact-essential criterion — they are solved geometry with a payload attached — and welding, because its standards, heat, and qualification requirements add an entire regulatory apparatus orthogonal to the manipulation contribution. Cutting them costs the dissertation no core claim.

### Problem set · 과제

Tier A. S1 at the pin, with [[04-robotics/force-compliance-control|13]] and [[04-robotics/navigation-mobile-manipulation|16]] behind it. The lab code samples the five error sources; there is no simulator.

1. **Draw.** The picture above for the site case, base term $5\,\mathrm{mm}$, with the lead-in enlarged until $99\%$ of holes are captured: the new 95% circle, the new lead-in, the new linear sum, and on the right the stiff and compliant sideways pushes at the new 95th-percentile error, against the panel's weight.
2. **Derive.** (a) The root-sum-square budget and per-axis $\sigma$ when the base term is $3\,\mathrm{mm}$. (b) The lead-in radius that captures $99\%$ of holes at that $\sigma$. (c) The vertical stiffness that keeps the sag under $1\,\mathrm{mm}$ if the payload estimate is off by $10\%$. (d) The tilt at which wedging becomes possible for a $1\,\mathrm{mm}$ clearance in the same $18\,\mathrm{mm}$ hole, $\mu=0.3$.
3. **Do.** Fill the `?` so that the script samples the five error sources and reproduces the Worked case: capture per hole and per panel, the 95th-percentile error, the two sideways forces, the vertical stiffness, and the site sweep of the base term. Then read the sweep: at what base error does panel capture first fall below $90\%$, and how fast must the lead-in grow to keep $99\%$ per hole?

```python
import numpy as np
ALLOC = {"map": 1.0, "base": 2.0, "arm": 1.0, "tool": 0.5, "part": 1.0}   # S1 budget (mm), read as 2-sigma per axis
rc, W = 4.0, 20*9.81                   # lead-in capture radius (mm), panel weight (N)
rng = np.random.default_rng(0)
def radial_error(alloc, n=200_000):
    sig = ?                                                       # per-axis sigma of each source
    e = rng.normal(0.0, sig, size=(n, 2, len(sig))).sum(axis=2)   # x and y error, sources summed
    return np.hypot(e[:, 0], e[:, 1])
r = radial_error(ALLOC)
p_hole = ?                                                       # fraction of holes the lead-in captures
r95 = float(np.percentile(r, 95))
print("linear", sum(ALLOC.values()), "rss", round(float(np.sqrt(sum(v*v for v in ALLOC.values()))), 2),
      "p_hole", round(p_hole, 3), "p_panel", round(p_hole*p_hole, 3), "r95", round(r95, 2))
for K in (1e5, 500.0):                                           # stiff position control vs lateral impedance
    print("K", K, "lateral force at r95 (N)", round(?, 1))
print("vertical K for 1 mm sag at 5% payload error", round(?))
for base in (2.0, 3.0, 4.0, 5.0):                                # the base term grows from lab to site
    rb = radial_error(dict(ALLOC, base=base))
    pb = float((rb <= rc).mean())
    print("base", base, "p_panel", round(pb*pb, 3), "r95", round(float(np.percentile(rb, 95)), 2),
          "rc for 99% per hole", round(float(np.percentile(rb, 99)), 2))
```

4. **Interpret.** A paper reports "$100\%$ insertion success in $30$ trials" for a panel-installation robot in a full-scale mock-up. Using Step 2 and the site paragraph, what would you need to know before expecting the same on a site, and how many consecutive successes would it take to rule out, at $95\%$ confidence, the $2.4\%$ panel miss rate of the lab budget?

> [!note]- How to draw it · 그리는 법
> - **Left, circles centred on the hole, to scale in millimetres**: the lead-in as a shaded disk of radius $8.1\,\mathrm{mm}$, the site 95% circle at $6.51\,\mathrm{mm}$ solid, and the linear sum, now $1+5+1+0.5+1=8.5\,\mathrm{mm}$, dotted, just outside the lead-in.
> - **Beside it, the lab's $4\,\mathrm{mm}$ lead-in as a faint outline**, so the doubling is visible: the lead-in had to grow about $1.3\,\mathrm{mm}$ for every millimetre the base term grew.
> - **Right, the two sideways pushes on a log axis at the new 95th-percentile error**: stiff $10^5\times0.00651=651\,\mathrm{N}$, now $3.3$ times the panel's weight, and compliant $500\times0.00651=3.3\,\mathrm{N}$. Draw the $196\,\mathrm{N}$ weight line.
> - **Write under the left panel what the enlarged lead-in costs**: a pin nose twice as long and a bracket that must leave room for it. Geometry bought back what localization lost.
> - The drawing is wrong if the 95% circle is inside the lead-in by the old margin: at $99\%$ capture the lead-in sits only $1.6\,\mathrm{mm}$ outside the 95% circle, because the Rayleigh tail between the 95th and 99th percentiles is short.

> [!tip]- Solutions
> 1. As in the How-to-draw list: lead-in $8.1\,\mathrm{mm}$, 95% circle $6.51\,\mathrm{mm}$, linear sum $8.5\,\mathrm{mm}$; pushes $651$ and $3.3\,\mathrm{N}$ against $196\,\mathrm{N}$.
> 2. (a) $\sqrt{1+9+1+0.25+1}=\sqrt{12.25}=3.50\,\mathrm{mm}$, so $\sigma=1.75\,\mathrm{mm}$. (b) $r_c=\sigma\sqrt{-2\ln0.01}=1.75\times3.035=5.31\,\mathrm{mm}$. (c) $10\%$ of $196.2\,\mathrm{N}$ is $19.62\,\mathrm{N}$, so $K\ge19{,}620\,\mathrm{N/m}$. (d) $\theta=\Delta/(\mu D)=1/(0.3\times18)=0.185\,\mathrm{rad}$, $10.6^\circ$.
> 3. The blanks are `np.array(list(alloc.values()))/2`, `float((r <= rc).mean())`, `K*r95/1000` and `0.05*W/0.001`. The filled script:
>
> ```python
> import numpy as np
> ALLOC = {"map": 1.0, "base": 2.0, "arm": 1.0, "tool": 0.5, "part": 1.0}   # S1 budget (mm), read as 2-sigma per axis
> rc, W = 4.0, 20*9.81                   # lead-in capture radius (mm), panel weight (N)
> rng = np.random.default_rng(0)
> def radial_error(alloc, n=200_000):
>     sig = np.array(list(alloc.values()))/2                        # per-axis sigma of each source
>     e = rng.normal(0.0, sig, size=(n, 2, len(sig))).sum(axis=2)   # x and y error, sources summed
>     return np.hypot(e[:, 0], e[:, 1])
> r = radial_error(ALLOC)
> p_hole = float((r <= rc).mean())                                 # fraction of holes the lead-in captures
> r95 = float(np.percentile(r, 95))
> print("linear", sum(ALLOC.values()), "rss", round(float(np.sqrt(sum(v*v for v in ALLOC.values()))), 2),
>       "p_hole", round(p_hole, 3), "p_panel", round(p_hole*p_hole, 3), "r95", round(r95, 2))
> for K in (1e5, 500.0):                                           # stiff position control vs lateral impedance
>     print("K", K, "lateral force at r95 (N)", round(K*r95/1000, 1))
> print("vertical K for 1 mm sag at 5% payload error", round(0.05*W/0.001))
> for base in (2.0, 3.0, 4.0, 5.0):                                # the base term grows from lab to site
>     rb = radial_error(dict(ALLOC, base=base))
>     pb = float((rb <= rc).mean())
>     print("base", base, "p_panel", round(pb*pb, 3), "r95", round(float(np.percentile(rb, 95)), 2),
>           "rc for 99% per hole", round(float(np.percentile(rb, 99)), 2))
> ```
>
> It prints `linear 5.5 rss 2.69 p_hole 0.988 p_panel 0.976 r95 3.29`, the forces `329.3` and `1.6`, the stiffness `9810`, and the sweep: base $2$, $3$, $4$, $5\,\mathrm{mm}$ give panel capture $0.976$, $0.860$, $0.657$, $0.461$, 95th-percentile error $3.29$, $4.28$, $5.37$, $6.51\,\mathrm{mm}$, and a $99\%$ lead-in of $4.08$, $5.30$, $6.65$, $8.10\,\mathrm{mm}$. Panel capture first falls below $90\%$ at a base error of $3\,\mathrm{mm}$, one millimetre above the lab's, and the lead-in has to grow about $1.3\,\mathrm{mm}$ per millimetre of base error.
> 4. You would need the error budget the mock-up actually produced (in particular the base term, and whether the base was re-localized against the same fixed targets every trial), whether trials were reset by hand, and how misses would have been detected. With zero failures in $n$ trials, a failure rate $p$ is ruled out at $95\%$ when $(1-p)^n\le0.05$: for $p=0.024$ that needs $n\ge\ln0.05/\ln0.976=123.3$, so $124$ consecutive successes (the rule of three, $3/p$, gives $125$). Thirty successes rule out only rates above about $10\%$.

### Sources

**Site-verified**

- R. Feng, Y. Jia, T. Wang, H. Gan, "Research on the System Design and Target Recognition Method of the Rebar-Tying Robot," *Buildings*, vol. 14, no. 3, art. 838, 2024. DOI 10.3390/buildings14030838. Open access. Its abstract states validation on a rebar-mesh demonstration platform followed by application on the Shenyang Hunnan Science and Technology City Phase IV project.
- K. Dörfler, T. Hack, T. Sandy, M. Giftthaler, M. Lussi, A. R. Walzer, J. Buchli, F. Gramazio, M. Kohler, "Mobile robotic fabrication beyond factory conditions: case study Mesh Mould wall of the DFAB HOUSE," *Construction Robotics*, vol. 3, no. 1–4, pp. 53–67, 2019. DOI 10.1007/s41693-019-00020-w
- S. N. Yu, S. Y. Lee, C. S. Han, K. Y. Lee, S. H. Lee, "Development of the curtain wall installation robot: Performance and efficiency tests at a construction site," *Autonomous Robots*, vol. 22, no. 3, pp. 281–291, 2007. DOI 10.1007/s10514-006-9019-2.

**Laboratory or mock-up**

- A. A. Apolinarska, M. Pacher, H. Li, et al., "Robotic assembly of timber joints using reinforcement learning," *Automation in Construction*, vol. 125, art. 103569, 2021. DOI 10.1016/j.autcon.2021.103569. Sim-to-real, force/torque-guided insertion.
- J. Kindle, M. Loetscher, A. Alessandretti, C. Cadena, M. Hutter, "Enhancing Robotic Precision in Construction: A Modular Factor Graph-Based Framework to Deflection and Backlash Compensation Using High-Accuracy Accelerometers," [arXiv:2501.14280](https://arxiv.org/abs/2501.14280); accepted to IEEE RA-L, November 2024. Uses a 700 kg tracked drilling robot identified as the Hilti Jaibot.
- K. Iturralde, M. Feucht, D. Illner, et al., "Cable-driven parallel robot for curtain wall module installation," *Automation in Construction*, vol. 138, art. 104235, 2022. DOI 10.1016/j.autcon.2022.104235. Tested in two close-to-real demonstration buildings.
- B. Chu, K. Jung, M.-T. Lim, D. Hong, "Robot-based construction automation: An application to steel beam assembly (Part I)," *Automation in Construction*, vol. 32, pp. 46–61, 2013, with Part II by K. Jung, B. Chu, D. Hong, pp. 62–79.
- P. D'Amours, S. Faucher, F. Ferland, A. Girard, "Drywall finishing with collaborative robot arm in off-site construction," *Proc. 42nd ISARC*, 2025, pp. 1567–1570. DOI 10.22260/ISARC2025/0204.

**Framing and surveys**

- N. Melenbrink, J. Werfel, A. Menges, "On-site autonomous construction robots: Towards unsupervised building," *Automation in Construction*, vol. 119, art. 103312, 2020. DOI 10.1016/j.autcon.2020.103312 — the survey to read first.
- C. Brosque, J. T. Hawkins, T. Dong, J. Örn, M. Fischer, "Comparison of on-site and off-site robot solutions to the traditional framing and drywall installation tasks," *Construction Robotics*, vol. 7, no. 1, pp. 19–39, 2023. DOI 10.1007/s41693-023-00093-8 — a process and economics evaluation on a real project.
- Z. Ren, J. I. Kim, "The Role of AI in On-Site Construction Robotics: A State-of-the-Art Review Using the Sense–Think–Act Framework," *Buildings*, vol. 15, no. 13, art. 2374, 2025 — the most recent learning-centric review.

**Contact mechanics used in the Worked case**

- D. E. Whitney, "Quasi-static assembly of compliantly supported rigid parts," *ASME Journal of Dynamic Systems, Measurement, and Control* 104(1):65–77, 1982 — the wedging condition of Step 5.

**Within this wiki**

- [[05-construction-robotics/assembly-fabrication|Assembly & Fabrication]] — the lineages behind these systems.
- [[05-construction-robotics/industry-deployment|Industry Deployment]] — the commercial systems that have no papers.
- [[07-research-program/paper-arc|7.1 Paper Arc §4]] — the five criteria applied in §5.
- [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] — the tools these tasks would be studied with, and the benchmark and dataset absences that go with them.

## 한국어

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고 그림을 본다. [[05-construction-robotics/site-engineering|2.5]]와 [[05-construction-robotics/assembly-fabrication|4]]의 같은 S1 패널을, 구멍이 위치 결정 핀을 만나는 순간까지 따라간 것이다. 그다음 §1과 §2에서 건설의 접촉이 공장의 접촉과 왜 다르고 어떤 작업이 무엇을 요구하는지 읽고, §3 뒤의 계산 절에서 패널이 앉을지를 정하는 네 숫자를 본다. §3–§6은 역학을 배울 때가 아니라 학위논문 작업을 고를 때 읽는 부분이다.

### 이 페이지의 대상 · Running object

[[05-construction-robotics/site-engineering|2.5 현장 로보틱스를 공학 시스템으로]]의 **S1**이다. 설치 구멍 두 개가 $400\,\mathrm{mm}$ 떨어진 $20\,\mathrm{kg}$ 외장 패널을 운반과 정렬 너머 접촉하는 순간까지 따라간다. 이때 구멍마다 브래킷의 위치 결정 핀 위로 내려앉아야 한다. 이 순간 전까지는 기하이고, 여기서부터 조작이 된다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| 오차 예산 | 지도 $1$, 베이스 $2$, 팔 $1$, 공구 $0.5$, 부품 $1\,\mathrm{mm}$ | S1의 할당(2.5 §2). 여기서는 각 원천의 수평 축별 2시그마 경계로 읽는다 |
| $D,\ d$ | $18$, $16\,\mathrm{mm}$ | 구멍과 핀의 지름. 볼트 여유 끼워맞춤, 지름 틈새 $\Delta=2\,\mathrm{mm}$ |
| $r_c$ | $4\,\mathrm{mm}$ | 핀의 뾰족한 끝이 붙잡을 수 있는 반지름 방향 오차 |
| $\mu$ | $0.3$ | 먼지 묻은 강철끼리의 마찰 |
| $K_{\text{stiff}}$ | $10^5\,\mathrm{N/m}$ | 강철에 눌린 위치 제어 팔. [[04-robotics/force-compliance-control\|13]] 대상의 직렬 강성 |
| $K_d$ | $500\,\mathrm{N/m}$ | 옆 방향 목표 임피던스, 13의 $K_d$ |
| $W$ | $196\,\mathrm{N}$ | 패널 무게, $20\times9.81$ |

할당을 2시그마 경계로 읽는 것은 이 페이지의 선택이다. 2.5는 그것을 열어 두었고, 그 페이지의 §2가 바로 그 읽기를 밝혀야 한다는 경고다. 핀, 리드인, $\mu$는 이 페이지가 고정한 숫자이고 나머지는 S1이나 카탈로그다.

*범위: 이 페이지는 건설 작업을 조작의 요구에 대응시키고, 증거를 시뮬레이션–실험실–현장 사다리에 놓고, S1의 접촉 사건 하나에 값을 매긴다. 임피던스·어드미턴스 제어([[04-robotics/force-compliance-control|13]]), 파지 품질([[04-robotics/grasping|15]]), 베이스 배치([[04-robotics/navigation-mobile-manipulation|16]])는 가르치지 않고, 그 숫자를 쓴다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 318" style="max-width:100%;height:auto" role="img" aria-label="왼쪽: 설치 구멍을 중심으로 한 원들. 4 mm 리드인 포착 반지름, 실험실의 95번째 백분위 위치 오차 3.29 mm와 현장의 6.51 mm, 5.5 mm 선형 오차 합. 오른쪽: 로그 힘 축 위에서 95번째 백분위 오차의 옆 힘은 단단한 팔 329 N, 옆으로 유연한 팔 1.6 N이고, 패널 무게 196 N과 비교된다.">
<text x="20" y="22" font-size="12.5" fill="currentColor" font-weight="600">핀이 구멍을 만나는 곳 (mm)</text>
<circle cx="140" cy="150" r="68.0" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-opacity="0.5"/>
<circle cx="140" cy="150" r="55.9" fill="none" stroke="currentColor" stroke-width="1.6"/>
<circle cx="140" cy="150" r="93.5" fill="none" stroke="currentColor" stroke-dasharray="1.5 3" stroke-opacity="0.8"/>
<circle cx="140" cy="150" r="110.7" fill="none" stroke="currentColor" stroke-dasharray="5 3" stroke-opacity="0.75"/>
<circle cx="140" cy="150" r="2.5" fill="currentColor"/>
<line x1="38.0" y1="268" x2="38.0" y2="272" stroke="currentColor"/><text x="38.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−6</text>
<line x1="72.0" y1="268" x2="72.0" y2="272" stroke="currentColor"/><text x="72.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−4</text>
<line x1="106.0" y1="268" x2="106.0" y2="272" stroke="currentColor"/><text x="106.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">−2</text>
<line x1="140.0" y1="268" x2="140.0" y2="272" stroke="currentColor"/><text x="140.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">0</text>
<line x1="174.0" y1="268" x2="174.0" y2="272" stroke="currentColor"/><text x="174.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">2</text>
<line x1="208.0" y1="268" x2="208.0" y2="272" stroke="currentColor"/><text x="208.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">4</text>
<line x1="242.0" y1="268" x2="242.0" y2="272" stroke="currentColor"/><text x="242.0" y="284" font-size="10.5" fill="currentColor" text-anchor="middle">6</text>
<line x1="38.0" y1="268" x2="242.0" y2="268" stroke="currentColor" stroke-opacity="0.6"/>
<rect x="262" y="41" width="22" height="10" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-opacity="0.5"/><text x="290" y="50" font-size="11" fill="currentColor">리드인 포착 r ≤ 4</text>
<line x1="262" y1="64" x2="284" y2="64" stroke="currentColor" stroke-width="1.6"/><text x="290" y="68" font-size="11" fill="currentColor">실험실 95%: 3.29</text>
<line x1="262" y1="82" x2="284" y2="82" stroke="currentColor" stroke-width="1.2" stroke-dasharray="5 3"/><text x="290" y="86" font-size="11" fill="currentColor">현장 95%: 6.51</text>
<line x1="262" y1="100" x2="284" y2="100" stroke="currentColor" stroke-width="1.2" stroke-dasharray="1.5 3"/><text x="290" y="104" font-size="11" fill="currentColor">선형 합: 5.5</text>
<text x="262" y="126" font-size="11" fill="currentColor" font-weight="600">실험실: 패널의 97.6%가 앉는다</text>
<text x="262" y="142" font-size="11" fill="currentColor">현장(베이스 오차 5 mm): 46%</text>
<text x="262" y="182" font-size="12.5" fill="currentColor" font-weight="600">95번째 백분위 오차에서의 옆 힘</text>
<rect x="262" y="194" width="216.5" height="16" fill="currentColor" fill-opacity="0.55"/>
<rect x="262" y="238" width="17.6" height="16" fill="currentColor" fill-opacity="0.55"/>
<text x="262" y="226" font-size="11" fill="currentColor">단단한 팔, 10<tspan dy="-4" font-size="9">5</tspan><tspan dy="4" dx="2"> N/m: 329 N</tspan></text>
<text x="262" y="270" font-size="11" fill="currentColor">옆 방향 임피던스 500 N/m: 1.6 N</text>
<line x1="459.2" y1="190" x2="459.2" y2="278" stroke="currentColor" stroke-dasharray="2 3"/>
<text x="455.2" y="290" font-size="10.5" fill="currentColor" text-anchor="end">패널 무게 196 N</text>
<line x1="262.0" y1="294" x2="262.0" y2="298" stroke="currentColor"/><text x="262.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">1</text>
<line x1="348.0" y1="294" x2="348.0" y2="298" stroke="currentColor"/><text x="348.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">10</text>
<line x1="434.0" y1="294" x2="434.0" y2="298" stroke="currentColor"/><text x="434.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">100</text>
<line x1="520.0" y1="294" x2="520.0" y2="298" stroke="currentColor"/><text x="520.0" y="310" font-size="10.5" fill="currentColor" text-anchor="middle">1000 N</text>
<line x1="262" y1="294" x2="520" y2="294" stroke="currentColor" stroke-opacity="0.6"/>
</svg>

구멍이 핀을 만나는 순간의 S1이다. 실험실 오차 예산이면 구멍의 95%가 $3.29\,\mathrm{mm}$ 안에 도착해 핀의 리드인이 붙잡는 $4\,\mathrm{mm}$ 안에 들어오므로 패널의 $97.6\%$가 앉는다. 현장에서 베이스 오차가 $5\,\mathrm{mm}$로 커지면 95% 원은 $6.51\,\mathrm{mm}$로 커지고 $46\%$만 앉는다. 오른쪽은 리드인이 95번째 백분위 오차를 바로잡는 동안 팔이 옆으로 미는 힘이다. 단단한 팔은 패널 자신의 무게보다 큰 힘으로 건물에 기대고, 유연한 팔은 1.5뉴턴 남짓으로 민다.

### 1. 건설 조작이 자기만의 문제인 이유

[[05-construction-robotics/assembly-fabrication|조립·제작]]은 이제 **S1**을 두 구멍 정렬 교과로 푼 뒤 도메인의 *계보*를 지도로 둔다. 이 페이지는 다른 단면을 자른다:
**로봇의 손이 실제로 무엇을 해야 하는가**를 작업별로, 그리고 각 작업이 매니퓰레이션 트랙의
페이지들에 무엇을 요구하는지를.

공장 조작과의 차이는 건설이 막연히 더 어렵다는 것이 아니다. 구체적이며, 각 항목이 공장
로보틱스에게는 허용된 가정을 하나씩 없앤다:

| 공장의 가정 | 건설이 대신 주는 것 |
|---|---|
| 부재가 지그에 알려진 자세로 있다 | 부재는 누군가 놓은 자리에, 센티미터 오차로 있다 |
| 작업물은 강체이고 치수가 정해져 있다 | 패널은 휘고, 철근(콘크리트 속에 넣는 보강용 강봉) 다발은 어긋나고, 멤브레인은 늘어진다 |
| 환경이 매 사이클 같다 | 같은 작업의 두 사례가 다르고, 건물은 지어지면서 변한다 |
| 로봇이 바닥에 볼트로 고정되어 있다 | 베이스가 여기까지 이동해 왔고, 그 자세가 오차 예산의 일부다 |
| 작업 구역 안에 아무도 없다 | 다른 공종이 옆에서 일하고, 안전이 규제된다 |
| $\mu$(마찰 계수, [[04-robotics/grasping\|15. §2]]), 질량, 기하를 안다 | 분진·습기·공차가 셋 다 불확실하게 만든다 |

1행은 **접촉 법선을 고정해 둔 순수 하이브리드 위치/힘 제어**를 취약하게 만든다. 선택 행렬이
그 좌표계에 의존하기 때문이다([[04-robotics/force-compliance-control|13. §3]]). 논문이 법선을 언제
추정·갱신하고 접촉 전후 제어 모드를 어떻게 전환하는지 확인하라. 온라인 좌표계 갱신,
컴플라이언스, 낮은 접근 강성은 이 오차를 완화할 수 있다.

### 2. 작업 매트릭스

건설 작업을 트랙의 조작 원시동작으로 분해한 것. 각 행을 명세로 읽어라 — 그 작업을 하는
프로젝트가 어느 페이지들을 깊이 필요로 할지를 말해 준다.

| 작업 | 원시동작 | 결정적 센싱 | 제어 모드 | 가장 어려운 불확실성 |
|---|---|---|---|---|
| **앵커 볼트 설치, 천장 드릴링** | 드릴, 밀기 | 위치 + 힘, 추력 | 비트 축 방향의 힘 | 추력에 의한 팔 변형, 천장 재료의 편차 |
| **패널·커튼월 설치** | 파지, 운반, 끼움 | 비전 + 힘 | 낮은 강성의 유연 끼움 | 부재가 크고 휜다, 베이스 자세 오차가 지배적 |
| **드라이월 시공** | 파지, 지지, 체결 | 비전 + 힘 | 지지는 위치, 체결은 힘 | 시트가 휜다, 머리 위 지지는 힘의 문제 |
| **드라이월 마감** | 샌딩, 긁기 | 힘 / 깊이 제어 | 표면 법선 방향의 힘 | 제거 깊이가 명세인데 밀리미터 이하다 |
| **철근 결속** | 도달, 감기, 절단 | 교차점을 찾는 비전 | 대체로 위치, 가벼운 접촉 | 메시가 비강체이고 어긋난다, 수천 번의 반복 |
| **배관·전선관 끼움** | 삽입, 정렬 | 힘 + 촉각 | 낮은 강성 임피던스 | wedging과 jamming([[04-robotics/force-compliance-control\|13. §5]]) |
| **볼트 강접합** | 정렬, 삽입, 조임 | 힘 + 토크 | 하이브리드: 가로는 위치, 축은 힘 | 부재가 무겁고, 크레인이나 베이스가 유연하다 |
| **목재 접합 조립** | 억지 끼움 삽입 | 힘/토크 | 학습 또는 유연 삽입 | 공차와 형상이 부재마다 다르다 |
| **조적, 블록 쌓기** | 파지, 놓기 | 비전 | 위치 | 접촉 문제라기보다 무게와 사이클 타임 문제 |
| **강구조 용접** | 이음선 추적 | 비전 + seam tracking | 추적된 경로를 따르는 위치 | 이음 기하가 변하고, 뜨겁고, 기준이 엄격하다 |

표의 건설 용어 둘을 쉬운 말로 풀면 이렇다. *철근 결속*은 콘크리트를 붓기 전에 철근이 교차하는
점마다 철사를 감아 격자로 묶는 일이다. *커튼월*은 구조체에 매다는, 하중을 받지 않는 유리·금속
패널 외피이므로, 설치란 크고 무거운 모듈을 제자리로 옮겨 맞추는 일이다.

그 표의 두 행은 접촉이 많지 않고, 그렇게 말하는 것 자체가 요점의 일부다. 조적과 대부분의
놓기 작업은 페이로드 문제가 붙은 풀린 기하다. 도메인에는 속하지만 [[07-research-program/index|7. §7]]의
입장 시험에 따르면 이 학위논문의 핵심에는 속하지 않는다.

과제 이름에 실패를 결정하는 변수가 숨기 때문에 행렬이 필요하다. 예를 들어 파이프 삽입과 벽돌 배치는 영상에서 모두 집어 놓기로 보이지만 전자는 접촉 중 끼임 감지가 필요할 수 있다. **여기서 얻는 독법.** 팔 동작의 시각적 유사성보다 실패 기전과 필요한 피드백으로 행을 고른다. 제안 센서가 그 기전을 실제 관측하는지도 묻는다.

### 3. 사다리 — 그리고 주제 선택을 바꿔야 할 발견

이 위키는 **시뮬레이션**, **실험실 또는 목업**, **가동 중인 건설 현장**을 구분할 것을 고수한다.
접촉이 많은 건설 조작에 그 구분을 적용하면 눈에 띄는 결과가 나온다.

<svg viewBox="0 0 560 232" style="max-width:100%;height:auto" role="img" aria-label="증거의 세 단계, 아래 두 칸에 대부분이 몰려 있고 가동 중 현장은 거의 비어 있다">
  <g fill="currentColor">
    <rect x="40" y="146" width="440" height="40" rx="3" fill-opacity="0.08"/>
    <rect x="88" y="98" width="392" height="40" rx="3" fill-opacity="0.16"/>
    <rect x="360" y="50" width="120" height="40" rx="3" fill-opacity="0.32"/>
  </g>
  <g stroke="currentColor" stroke-width="1" fill="none" opacity="0.6">
    <rect x="40" y="146" width="440" height="40" rx="3"/><rect x="88" y="98" width="392" height="40" rx="3"/><rect x="360" y="50" width="120" height="40" rx="3"/>
  </g>
  <g font-size="11" fill="currentColor">
    <text x="52" y="163">시뮬레이션</text>
    <text x="52" y="178" font-size="9.5" opacity="0.75">무한한 시행, 고른 물리</text>
    <text x="100" y="115">실험실 또는 목업</text>
    <text x="100" y="130" font-size="9.5" opacity="0.75">실제 접촉, 마련된 조건 &#8212; 이 연구의 거의 전부가 여기 있다</text>
    <text x="372" y="67">가동 중 현장</text>
    <text x="372" y="82" font-size="9.5" opacity="0.75">거의 비어 있다</text>
  </g>
  <g font-size="11" fill="currentColor" opacity="0.9">
    <text x="20" y="208">드릴링·드라이월·철근·파사드·목재·용접을 겨냥해 찾아본 결과, 가동 중인 건설 현장에 매니퓰레이터를</text>
    <text x="20" y="224">올린 논문은 셋뿐이고 가장 오래된 것은 2007년이다. 전수 집계가 아니라 후보 공백으로 다룰 것.</text>
  </g>
</svg>

검증된 예외 셋이 두드러진다. Feng 등(2024)은 평면형 철근 결속 로봇을 철근 메시 실증
플랫폼에서 먼저 검증한 뒤 선양 훈난 과학기술도시 4기 현장에 적용했다고 보고한다.
Dörfler 등(2019)은 In situ Fabricator로 NEST의 DFAB HOUSE Mesh Mould 벽을 지었다 —
모바일 매니퓰레이터가 철근을 현장에서 구부리고 용접했고, 허가받아 지금은 사람이 사는
건물이다. Yu 등(2007)은 굴착기 베이스 위에 커튼월 설치 로봇을 만들어 건설 현장에서
시험했다 — 제목이 그렇게 말한다 — 그러나 스무 해 가까이 된 연구다.

**그 검색이 무엇을 제외하는지 — 개수가 아니라 범위에 반대할 수 있도록.** 이것은 여섯 개 과제
키워드로 *현대* 문헌을 훑은 것이라, 일본의 **STCR 시대**에는 닿지 않는다 — Shimizu, Obayashi,
Kajima 등이 1980~90년대에 실제 현장에서 돌린 수십 대의 단일 작업 건설 로봇이고, 그 기록은
ISARC(International Symposium on Automation and Robotics in Construction) 회보와 Bock의 참고서에 있다([[05-construction-robotics/lineage|계보, 1시대]]). 그 기계들은
실제 현장에 있었고 의도적으로 이 집계 밖이다 — 이 페이지가 다루는 접촉 제어·힘 센싱·학습이
없는 단일 작업 자동화이기 때문이다. 이 발견은 "접촉이 많은 조작 문헌에서 세 편"으로 읽어야지
"역사상 세 대"로 읽으면 안 된다.

기술적으로 강한 나머지는 전부 실험실이나 목업에서 멈춘다. 제목을 작업 장소의 증거로
삼지 마라. 방법 절에서 장소를 지명한 문장을 읽어라. 가장 강한
천장 드릴링 결과인 Kindle 등은 *모사된* 현장 교란 조건에서 기록한 데이터셋으로 평가된다 —
현장이 아니다.

**이 집계를 언제 어디서 했는지 — 다시 돌릴 수 있도록.** 여섯 키워드 검색은 2026년 8월에
arXiv와 Crossref에서 했고, 2026년 9월에 다시 돌렸다. 재검색에서 같은 키워드 아래 집계에 없는
2025년 논문 둘이 나왔는데, 위의 장소 시험을 적용하기 전에는 더하면 안 된다. 육각보행
커튼월 설치 로봇([arXiv:2509.13595](https://arxiv.org/abs/2509.13595))은 초록이 로봇 위의 실험을
서술하고 현장 배치는 향후 과제로 두므로 실험실 결과로 읽힌다. ISARC 2025의 드라이월 패널 설치
로봇(doi:10.22260/isarc2025/0058)은 초록을 구하지 못해 실험 장소가 미확인이다. 날짜 없는
집계에는 반대할 수 없고, 이 집계는 반대받으려고 있는 것이다.

> [!important] 이 발견을 어떻게 쓸 것인가
> 연구 기회로 읽되, 단계를 건너뛰어도 된다는 허가로 읽지 마라. 맨 위 칸이 비어 있는 이유는
> 그것이 정말로 어렵기 때문이다 — 출입, 안전, 공정, 그리고 기다려 주지 않는 건물. 접촉이 많은
> 작업으로 가동 중인 현장에 도달한 학위논문은 거의 아무도 할 수 없는 주장을 하는 것이다.
> 목업 작업을 두고 "on-site"라고 *말하는* 학위논문은, 이 페이지가 지목하려고 존재하는 그
> 패턴에 합류하는 것이다.

### 대상으로 한 번 끝까지 · Worked case

핀 앞의 S1에서 다섯 단계, 그다음 현장에서 무엇이 바뀌는지. 과제의 실습 코드가 표본 추출로 모든 숫자를 다시 낸다.

**1단계 — 예산을 두 가지로 읽기.** 다섯 할당을 선형으로 더하면 $5.5\,\mathrm{mm}$로 리드인이 붙잡는 $4\,\mathrm{mm}$보다 크므로, 최악의 경우로 읽으면 패널은 결코 믿을 만하게 앉지 않는다. 독립인 2시그마 경계로 읽으면 제곱합의 제곱근으로 축마다 $\sqrt{1+4+1+0.25+1}=2.69\,\mathrm{mm}$, 축별 표준편차 $\sigma=1.35\,\mathrm{mm}$가 된다. 어느 읽기도 단순한 산수가 아니라 오차에 대한 주장이고(2.5 §2), 이 계산은 뒤의 것을 쓴다.

**2단계 — 구멍이 붙잡히는가?** 두 수평 축의 오차가 독립이고 크기가 같으면, 구멍이 핀에서 떨어진 반지름 거리 $r$는 레일리 분포를 따른다. 그래서 리드인 안에 떨어질 확률은

$$P(r\le r_c)=1-e^{-r_c^2/2\sigma^2}=1-e^{-16/3.62}=0.988$$

로 구멍 하나에 $0.988$, 두 구멍이 독립으로 어긋나는 패널에 $0.988^2=0.976$이다. 구멍의 95%는 $3.29\,\mathrm{mm}$, 곧 $2.45\sigma$ 안에 도착한다. 패널 마흔 개에 하나꼴로 핀을 놓친다. 그런 일이 없다고 가정할 것이 아니라, 놓침을 검출하고 되돌릴 수 있어야 할 만큼(S1의 *후퇴 후 재스캔*) 잦다.

**3단계 — 리드인이 바로잡는 동안 팔은 얼마나 세게 미는가?** 테이퍼는 오차를 팔이 허용해야 할 옆 방향 변위로 바꾼다. 단단한 위치 루프가 팔을 붙들면 팔은 구조의 직렬 강성으로 버틴다. 95번째 백분위 오차 $3.29\,\mathrm{mm}$에서 $F=K_{\text{stiff}}\,r=10^5\times0.00329=329\,\mathrm{N}$으로, **패널 자신의 무게의 1.7배**를 건물에 볼트로 고정된 브래킷 쪽으로 옆으로 민다. 옆 방향 목표 임피던스 $K_d=500\,\mathrm{N/m}$이면 같은 교정에 $1.6\,\mathrm{N}$이 든다. §2의 작업 매트릭스가 패널 설치에 *유연한 맞춤, 낮은 강성*을 적는 이유다. 리드인은 팔이 허락할 때만 정렬을 해 준다.

**4단계 — 그러나 모든 방향으로 유연하면 안 된다.** 같은 $500\,\mathrm{N/m}$를 수직으로 쓰면, 탑재물 추정의 $5\%$ 오차 $9.81\,\mathrm{N}$이 패널을 $9.81/500=19.6\,\mathrm{mm}$ 처지게 한다. 허용 오차의 네 배다. 그 오차에 맞서 $1\,\mathrm{mm}$를 지키려면 수직으로 $9.81/0.001=9{,}810\,\mathrm{N/m}$가 필요하다. 목표 임피던스는 비등방이어야 한다. 중력 방향으로 단단하고 핀을 가로질러 무르게. 13의 선택 행렬 발상을 못 대신 패널에 쓴 것이고, 접촉 좌표계를 알아야 하는 이유다(§1).

**5단계 — 쐐기 걸림에는 빡빡한 끼워맞춤이 필요하다.** 핀이 들어간 뒤에도 기운 패널은 잠길 수 있다. 쐐기 걸림([[04-robotics/force-compliance-control|13 §5.2]])은 삽입 깊이 $l<\mu D$에서 두 점 접촉이 생길 때 가능하고, 작은 기울기 $\theta$에서 두 점 접촉은 $l\approx\Delta/\theta$에서 생긴다. 그래서 위험은 $\theta=\Delta/(\mu D)$ 근처에서 시작한다. $2\,\mathrm{mm}$ 볼트 틈새면 $2/(0.3\times18)=0.37\,\mathrm{rad}$, 곧 $21^\circ$이고, 그렇게 삐뚤게 거는 패널은 없다. $0.2\,\mathrm{mm}$ 다월 끼워맞춤이면 $0.037\,\mathrm{rad}$, 곧 $2.1^\circ$로, 휘는 패널이나 고르지 않은 브래킷이 쉽게 닿는다. S1에서는 포착과 옆 힘이 문제이고, 쐐기 걸림은 끼워맞춤이 정밀할 때만 문제가 된다.

**현장에서 무엇이 움직이는가.** 2단계는 실험실의 베이스 항 $2\,\mathrm{mm}$를 가정했다. 계속 바뀌는 구조물에 대고 베이스를 다시 위치 추정하는 현장에서는 $5\,\mathrm{mm}$일 수 있다. 축별 $\sigma$는 $2.66\,\mathrm{mm}$, 95% 원은 $6.51\,\mathrm{mm}$가 되고, 패널 포착률은 $97.6\%$에서 $46\%$로 떨어진다. 구멍당 $99\%$를 지키려면 리드인이 $4.1$이 아니라 $8.1\,\mathrm{mm}$여야 한다. 팔은 하나도 바뀌지 않았고 §3의 단만 바뀌었다. 목업 결과가 현장으로 옮겨지지 않는 이유의 정량적 형태이고, [[04-robotics/navigation-mobile-manipulation|16]]이 맡는 예산의 베이스 항이 곧 조작의 문제인 이유다.

### 4. 앵커 논문 — 실제로 무엇을 실증했는가로 정렬

명성이 아니라 사다리 단계로 정렬한다. 여기서는 그 순서가 중요하기 때문이다.

**가동 중인 현장에서**

- **Feng 등(2024)** — 깊이 카메라와 산업용 카메라를 결합한 2단 인식으로 철근 메시 위를 주행하는
  철근 결속 로봇. 실증 플랫폼에서 검증한 뒤 현장에 적용.
- **Dörfler 등(2019)** — NEST DFAB HOUSE의 Mesh Mould 벽을 지은 In situ Fabricator.
  실제로 허가받아 지금 사람이 사는 건물에서 철근을 현장 성형·용접했다.
- **Yu 등(2007)** — 굴착기 베이스 위의 커튼월 설치 로봇. 현장에서 시험.

**실제 접촉, 실험실 또는 실물 크기 목업**

- **Apolinarska 등(2021)** — 목재 접합 조립. 전적으로 시뮬레이션에서 학습한 정책을 힘/토크와
  자세를 안내 삼아 실기계에 배치하고, 학습에서 보지 못한 공차와 형상 변동에도 일반화한다.
  건설 규모의 peg-in-hole이며, 이 분야가 가진 접촉이 많은 학습 결과에 가장 가까운 것이다.
- **Kindle 등(RA-L 2025)** — 700 kg 궤도형 드릴링 로봇(널리 Hilti Jaibot으로 지목되지만,
  논문 자체는 리프팅 칼럼·Doosan 매니퓰레이터·드릴링 엔드이펙터를 갖춘 약 700 kg 궤도
  베이스라고만 기술한다)에서의 변형·백래시 보상.
  현장 교란을 모사한 조건에서 기록한 데이터셋 일곱 개로 평가했다.
  [[04-robotics/force-compliance-control|13번]]의 컴플라이언스 문제를 건설의 언어로 진술한 것.
- **Iturralde 등(2022)** — 커튼월 모듈을 설치하는 케이블 구동 병렬 로봇. 실물에 가까운 실증
  건물 두 곳에서 시험.
- **Chu, Jung 등(2013)** — 2부작 강재 보 볼팅 시스템. 오래됐지만 볼트 접합의 정본 학술 참고다.

**결과가 아니라 틀로 읽을 것**

- **Brosque 등(2023)** 은 실제 프로젝트에서 현장 방식과 오프사이트 방식을 비교한다 — 경제성·공정
  평가이며, 조작 논문이 결코 말해 줄 수 없는 바로 그것이다.
- **Melenbrink, Werfel, Menges(2020)** 가 먼저 읽을 서베이다: 기술이 아니라 건설 작업으로
  구성되어 있고, 오프사이트가 아니라 현장 자율성으로 범위가 정해져 있으며, 그 공백 분석은
  여전히 유효하다.

> [!warning] 이 문헌의 두 가지 함정
> **보도용 시연이 결과로 인용된다.** 드라이월을 시공한다고 널리 소개된 휴머노이드는
> *관절 설계*에 관한 심사 논문을 가지고 있고, 드라이월 시연 자체는 보도 영상이다.
> **그리고 상용 시스템에는 *자기* 논문이 없다.** Jaibot, TyBot, Canvas, Okibo는 제품이고, 위
> Kindle 등의 플랫폼이 널리 Jaibot으로 지목된다는 점에서 보듯 **그 기계를 *다룬* 심사 논문은
> 존재할 수 있다** — 없는 것은 업체 자신의 심사된 발표다. 제품은 제품으로, 논문은 논문으로
> 인용하라. 그 생산성
> 수치는 마케팅이다. 제품으로 인용하고 그렇다고 밝혀라 —
> [[05-construction-robotics/industry-deployment|산업 배치]]를 보라.

### 5. 작업 고르기, 구체적으로

[[07-research-program/paper-arc|7.1 §4]]의 다섯 기준을 §2의 매트릭스에 적용한다.

| 작업 | 접촉이 본질적? | 실재하는 공차? | 사람이 대규모로? | 실험실 반복 가능? | 실패가 견딜 만한가? |
|---|---|---|---|---|---|
| 앵커 볼트 설치 | 예 | 예, mm | 예 | 예 | 머리 위 작업 — 주의 필요 |
| 패널 끼움 | 예 | 예, mm | 예 | 예 | 예 |
| 드라이월 마감 | 예 | 예, mm 이하 깊이 | 예 | 예 | 예 |
| 철근 결속 | 부분적 | 느슨 | 예, 엄청나게 | 예 | 예 |
| 배관 삽입 | 예 | 예 | 예 | 예 | 예 |
| 조적 | 아니오 | 느슨 | 예 | 예 | 예 |
| 천장 드릴링 | 예 | 예 | 예 | 예 | 분진과 낙하물 |

패널 끼움, 드라이월 마감, 배관 삽입이 다섯 기준을 모두 통과한다. 철근 결속은 규모 기준을
압도적으로 통과하지만 접촉이 가벼워서, 훌륭한 *배치* 목표이자 약한 *접촉 조작* 기여가 된다 —
그리고 그것이 현장 검증 결과를 가진 유일한 작업이라는 점은 우연이 아니다.

좋은 출발 과제는 연구할 불확실성을 드러내면서 반복 평가가 가능하다. 파이프 맞춤 장치는 정렬을 의도적으로 바꾸면서 실패를 회복 가능하게 만들 수 있다. **여기서 얻는 독법.** 장비를 고르기 전에 재현할 실패를 적는다. 장치가 그 실패를 불가능하게 만든다면 편리해도 의도한 접촉 적응 주장은 시험하지 못한다.

### 6. 이 도메인이 매니퓰레이션 문헌에 되돌려주는 것

관계는 양방향이고, 이것이 서론에 쓸 부분이다. 건설은 일반 조작 연구가 깔끔하게 제기할 방법이
없는 문제들을 공급한다:

- **알 수 없고 변하는 마찰** — [[04-robotics/grasping|15. §2~§4]]의 모든 파지 결과가 주어진
  것으로 놓는 그 $\mu$.
- **구조 규모의 비강체 부재** — form closure와 force closure([[04-robotics/grasping|15. §3]])는
  접촉점끼리의 상대 위치가 고정된 강체에 대해 정의된다. 2.4 m 시트는 휘어서 하중을 받으면 접촉
  기하가 바뀌므로 강체가 아니고, 따라서 closure가 정의조차 되지 않는다.
- **로봇이 바꿔 놓아서 변한 작업 구역** — 건물이 곧 작업물이다.
- **어떤 지그도 흡수하지 않는 공차 누적** — 베이스 자세 오차, 부재 배치 오차, 시공 편차가
  모두 같은 접촉 위에 떨어진다.

각각은 도메인을 핑계 삼는 것이 아니라 방어 가능한 견고성 주장이다. [[07-research-program/index|연구 프로그램]]이
딛고 선 차이가 그것이다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 지명된 건설 작업을 원시동작·센싱·제어 모드로 대응시킨다.
- [ ] 이 분야의 논문을 시뮬레이션–실험실–현장 사다리에 놓고, 어떤 근거로 거기 놓았는지 말한다.
- [ ] 현장 검증된 매니퓰레이션 사례 셋을 대고 접촉·배치 증거의 차이를 말한다.
- [ ] 작업 선정 다섯 기준을 적용해, 끌리는 작업 하나를 최소한 탈락시킨다.
- [ ] 건설이 일반 조작 연구에 되돌려주는 것 둘을 말한다.

다음 [[05-construction-robotics/imitating-contact|10. 접촉 모방]]은 이 페이지의 핀과 리드인을 그대로 두고, 시연에서 배운 정책이 S1의 마지막 40 mm에서 무엇을 하는지 묻는다. 행동 복제의 스텝당 오류가 핀에서 몇 밀리미터로 불어나는지, 어떤 해법이 정책을 리드인 안에 붙잡아 두는지다.

### 스스로 점검

1. 공장에서라면 처리했을 패널 끼움 작업에서 하이브리드 위치/힘 제어가 왜 건설에서는 실패하는가?
2. 어떤 논문의 제목에 "on-site"가 들어 있다. 믿기 전에 무엇을 확인하는가?
3. 철근 결속은 §2의 어느 작업보다 현장 검증 근거가 강하다 — Feng 등(2024)의 현장 적용과
   Dörfler 등(2019)의 허가받은 건물에서의 현장 철근 용접. (패널/커튼월 설치에도 하나 있지만
   Yu 등 2007로 스무 해 가까이 됐다.) 그런데도 왜 이 학위논문의 핵심 기여로는 약한 선택인가?
4. 어떤 업체가 드릴링 로봇의 하루 300공을 보고한다. 문헌 검토에 어떻게 실려야 하는가?
5. 학위논문을 좁혀야 한다면 §2의 어느 두 행을 먼저 잘라내겠는가, 그리고 왜인가?

> [!tip]- 정답 · Answers
> 1. 선택 행렬이 표면에 수직이라고 *믿는* 방향에 힘 제어를 배정하는데 그 믿음이 모델에서 오기 때문이다. 지그에서는 부재가 모델이 말하는 자리에 있지만 현장에서는 1~2 cm 안쪽 어딘가에 있으므로, 힘 제어가 부분적으로 표면을 따라, 위치 제어가 부분적으로 표면 안으로 작용하게 된다 — 그 아키텍처가 막으려고 존재하는 바로 그 싸움이다. 시스템이 접촉 프레임을 추정하거나 갱신하지 않고, 접촉 전후로 모드를 전환하지 않고, 컴플라이언스를 더하지 않는 한 이 아키텍처는 취약하다([[04-robotics/force-compliance-control|13. §3]]).
> 2. 방법과 실험 절에서 작업이 실제로 어디서 이루어졌는지를 지명한 문장을 확인한다. 이 분야의 여러 논문이 제목에 "on-site"를 달고 본문에서는 개발과 검증을 통제된 실험실에서 했다고 밝힌다. 제목은 포부를 말하고, 실험 절이 증거를 말한다.
> 3. 접촉이 가볍기 때문이다. 철근 결속의 어려운 부분은 인식(어긋나는 비강체 메시 위에서 교차점 찾기), 커버리지 계획, 그리고 수천 번을 신뢰성 있게 해내는 것이다 — 훌륭한 배치·자율성 결과가 되지만 기여가 접촉에 관한 것이 되지 않는다. 입장 시험에 따르면 이 프로그램의 매니퓰레이션 핵심보다 *내비게이션·배치* 기둥에 더 기여한다.
> 4. 결과가 아니라 출처를 밝힌 제품 주장으로. Jaibot, TyBot, Canvas, Okibo는 자기 심사 논문이 없으므로 그 생산성 수치는 심사를 거치지 않은 마케팅이다. 시장이 존재하고 그 작업이 자동화할 가치가 있다는 정당한 증거이긴 하다 — 측정된 주장과는 다른 주장이다.
> 5. 조적·블록 쌓기는 접촉 본질성 기준에서 탈락하기 때문이고(페이로드가 붙은 풀린 기하다), 용접은 기준·열·자격 요건이 조작 기여와 직교하는 규제 장치 전체를 끌고 오기 때문이다. 둘을 잘라도 학위논문은 어떤 핵심 주장도 잃지 않는다.

### 과제 · Problem set

Tier A. 핀 앞의 S1, 그 뒤에 [[04-robotics/force-compliance-control|13]]과 [[04-robotics/navigation-mobile-manipulation|16]]. 실습 코드는 다섯 오차 원천을 표본 추출하고, 시뮬레이터는 없다.

1. **그리기.** 현장의 경우, 베이스 항 $5\,\mathrm{mm}$에서 구멍의 $99\%$를 붙잡을 때까지 리드인을 키운 위의 그림: 새 95% 원, 새 리드인, 새 선형 합, 그리고 오른쪽에 새 95번째 백분위 오차에서 단단한 팔과 유연한 팔이 옆으로 미는 힘을 패널 무게와 함께.
2. **유도.** (a) 베이스 항이 $3\,\mathrm{mm}$일 때의 제곱합 제곱근 예산과 축별 $\sigma$. (b) 그 $\sigma$에서 구멍의 $99\%$를 붙잡는 리드인 반지름. (c) 탑재물 추정이 $10\%$ 틀릴 때 처짐을 $1\,\mathrm{mm}$ 아래로 지키는 수직 강성. (d) 같은 $18\,\mathrm{mm}$ 구멍에서 틈새가 $1\,\mathrm{mm}$일 때 쐐기 걸림이 가능해지는 기울기, $\mu=0.3$.
3. **실행.** 영어 절 템플릿의 `?`를 채워, 스크립트가 다섯 오차 원천을 표본 추출해 계산 절을 다시 내게 하라. 구멍당과 패널당 포착, 95번째 백분위 오차, 두 옆 힘, 수직 강성, 그리고 베이스 항의 현장 훑기. 그다음 훑기를 읽어라. 베이스 오차가 얼마일 때 패널 포착이 처음 $90\%$ 아래로 떨어지는가, 그리고 구멍당 $99\%$를 지키려면 리드인이 얼마나 빨리 커져야 하는가?
4. **해석.** 어떤 논문이 실물 크기 목업에서 패널 설치 로봇이 "$30$회 시행에서 삽입 성공 $100\%$"라고 보고한다. 2단계와 현장 문단을 써서, 현장에서도 같기를 기대하기 전에 알아야 할 것은 무엇인가? 그리고 실험실 예산의 패널 놓침 비율 $2.4\%$를 $95\%$ 신뢰로 배제하려면 몇 번 연속 성공해야 하는가?

> [!note]- 그리는 법 · How to draw it
> - **왼쪽, 구멍을 중심으로 한 원들을 밀리미터 축척으로**: 반지름 $8.1\,\mathrm{mm}$의 리드인을 칠한 원판으로, 현장 95% 원 $6.51\,\mathrm{mm}$를 실선으로, 이제 $1+5+1+0.5+1=8.5\,\mathrm{mm}$인 선형 합을 리드인 바로 바깥의 점선으로.
> - **그 옆에 실험실의 $4\,\mathrm{mm}$ 리드인을 흐린 윤곽선으로** 그려 두 배가 된 것이 보이게 한다. 베이스 항이 1밀리미터 커질 때마다 리드인은 약 $1.3\,\mathrm{mm}$ 커져야 했다.
> - **오른쪽, 새 95번째 백분위 오차에서의 두 옆 힘을 로그 축에**: 단단한 팔 $10^5\times0.00651=651\,\mathrm{N}$으로 이제 패널 무게의 $3.3$배, 유연한 팔 $500\times0.00651=3.3\,\mathrm{N}$. $196\,\mathrm{N}$ 무게 선을 긋는다.
> - **왼쪽 칸 아래에 키운 리드인의 대가를 적는다**: 두 배 긴 핀 끝과 그것이 들어갈 자리를 남겨야 하는 브래킷. 위치 추정이 잃은 것을 기하가 되사 온 것이다.
> - 95% 원이 옛 여유만큼 리드인 안에 있으면 그림이 틀린 것이다. $99\%$ 포착에서 리드인은 95% 원보다 겨우 $1.6\,\mathrm{mm}$ 바깥에 있다. 95번째와 99번째 백분위 사이의 레일리 꼬리가 짧기 때문이다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법 목록과 같다. 리드인 $8.1\,\mathrm{mm}$, 95% 원 $6.51\,\mathrm{mm}$, 선형 합 $8.5\,\mathrm{mm}$. 옆 힘 $651$과 $3.3\,\mathrm{N}$, 무게 $196\,\mathrm{N}$.
> 2. (a) $\sqrt{1+9+1+0.25+1}=\sqrt{12.25}=3.50\,\mathrm{mm}$이므로 $\sigma=1.75\,\mathrm{mm}$. (b) $r_c=\sigma\sqrt{-2\ln0.01}=1.75\times3.035=5.31\,\mathrm{mm}$. (c) $196.2\,\mathrm{N}$의 $10\%$는 $19.62\,\mathrm{N}$이므로 $K\ge19{,}620\,\mathrm{N/m}$. (d) $\theta=\Delta/(\mu D)=1/(0.3\times18)=0.185\,\mathrm{rad}$, $10.6^\circ$.
> 3. 빈칸은 영어 절 정답과 같다. 스크립트는 `linear 5.5 rss 2.69 p_hole 0.988 p_panel 0.976 r95 3.29`, 힘 `329.3`과 `1.6`, 강성 `9810`, 그리고 훑기를 찍는다. 베이스 $2$, $3$, $4$, $5\,\mathrm{mm}$에서 패널 포착은 $0.976$, $0.860$, $0.657$, $0.461$, 95번째 백분위 오차는 $3.29$, $4.28$, $5.37$, $6.51\,\mathrm{mm}$, $99\%$ 리드인은 $4.08$, $5.30$, $6.65$, $8.10\,\mathrm{mm}$다. 패널 포착은 실험실보다 1밀리미터 큰 베이스 오차 $3\,\mathrm{mm}$에서 처음 $90\%$ 아래로 떨어지고, 리드인은 베이스 오차 1밀리미터마다 약 $1.3\,\mathrm{mm}$ 커져야 한다.
> 4. 목업이 실제로 만든 오차 예산(특히 베이스 항, 그리고 매 시행 같은 고정 표적에 대고 베이스를 다시 위치 추정했는지), 시행을 손으로 되돌렸는지, 놓침을 어떻게 검출했을지를 알아야 한다. $n$번 시행에 실패가 없으면 $(1-p)^n\le0.05$일 때 실패율 $p$가 $95\%$로 배제된다. $p=0.024$에는 $n\ge\ln0.05/\ln0.976=123.3$, 곧 $124$번 연속 성공이 필요하다(3의 규칙 $3/p$은 $125$). $30$번 성공은 약 $10\%$ 넘는 비율만 배제한다.

### 출처

**현장 검증**

- R. Feng, Y. Jia, T. Wang, H. Gan, "Research on the System Design and Target Recognition Method of the Rebar-Tying Robot," *Buildings*, vol. 14, no. 3, art. 838, 2024. DOI 10.3390/buildings14030838. 오픈 액세스. 초록이 철근 메시 실증 플랫폼 검증과 이어진 선양 훈난 과학기술도시 4기 현장 적용을 명시한다.
- K. Dörfler, T. Hack, T. Sandy, M. Giftthaler, M. Lussi, A. R. Walzer, J. Buchli, F. Gramazio, M. Kohler, "Mobile robotic fabrication beyond factory conditions: case study Mesh Mould wall of the DFAB HOUSE," *Construction Robotics*, vol. 3, no. 1–4, pp. 53–67, 2019. DOI 10.1007/s41693-019-00020-w
- S. N. Yu, S. Y. Lee, C. S. Han, K. Y. Lee, S. H. Lee, "Development of the curtain wall installation robot: Performance and efficiency tests at a construction site," *Autonomous Robots*, vol. 22, no. 3, pp. 281–291, 2007. DOI 10.1007/s10514-006-9019-2.

**실험실 또는 목업**

- A. A. Apolinarska, M. Pacher, H. Li, et al., "Robotic assembly of timber joints using reinforcement learning," *Automation in Construction*, vol. 125, art. 103569, 2021. DOI 10.1016/j.autcon.2021.103569. Sim-to-real, 힘/토크 유도 삽입.
- J. Kindle, M. Loetscher, A. Alessandretti, C. Cadena, M. Hutter, "Enhancing Robotic Precision in Construction: A Modular Factor Graph-Based Framework to Deflection and Backlash Compensation Using High-Accuracy Accelerometers," [arXiv:2501.14280](https://arxiv.org/abs/2501.14280); 2024년 11월 IEEE RA-L 게재 확정. Hilti Jaibot으로 식별되는 700 kg 궤도형 드릴링 로봇을 사용한다.
- K. Iturralde, M. Feucht, D. Illner, et al., "Cable-driven parallel robot for curtain wall module installation," *Automation in Construction*, vol. 138, art. 104235, 2022. DOI 10.1016/j.autcon.2022.104235. 실물에 가까운 실증 건물 두 곳에서 시험.
- B. Chu, K. Jung, M.-T. Lim, D. Hong, "Robot-based construction automation: An application to steel beam assembly (Part I)," *Automation in Construction*, vol. 32, pp. 46–61, 2013. Part II는 K. Jung, B. Chu, D. Hong, pp. 62–79.
- P. D'Amours, S. Faucher, F. Ferland, A. Girard, "Drywall finishing with collaborative robot arm in off-site construction," *Proc. 42nd ISARC*, 2025, pp. 1567–1570. DOI 10.22260/ISARC2025/0204.

**틀과 서베이**

- N. Melenbrink, J. Werfel, A. Menges, "On-site autonomous construction robots: Towards unsupervised building," *Automation in Construction*, vol. 119, art. 103312, 2020. DOI 10.1016/j.autcon.2020.103312 — 먼저 읽을 서베이.
- C. Brosque, J. T. Hawkins, T. Dong, J. Örn, M. Fischer, "Comparison of on-site and off-site robot solutions to the traditional framing and drywall installation tasks," *Construction Robotics*, vol. 7, no. 1, pp. 19–39, 2023. DOI 10.1007/s41693-023-00093-8 — 실제 프로젝트에서의 공정·경제성 평가.
- Z. Ren, J. I. Kim, "The Role of AI in On-Site Construction Robotics: A State-of-the-Art Review Using the Sense–Think–Act Framework," *Buildings*, vol. 15, no. 13, art. 2374, 2025 — 가장 최근의 학습 중심 리뷰.


**계산 절에 쓴 접촉 역학**

- D. E. Whitney, "Quasi-static assembly of compliantly supported rigid parts," *ASME Journal of Dynamic Systems, Measurement, and Control* 104(1):65–77, 1982 — 5단계의 쐐기 걸림 조건.

**이 위키 안에서**

- [[05-construction-robotics/assembly-fabrication|조립·제작]] — 이 시스템들 뒤의 계보.
- [[05-construction-robotics/industry-deployment|산업 배치]] — 논문이 없는 상용 시스템들.
- [[07-research-program/paper-arc|7.1 논문 arc §4]] — §5에서 적용한 다섯 기준.
- [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] — 이 작업들을 연구할 도구와, 그에 딸린 벤치마크·데이터셋의 부재.
