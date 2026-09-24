---
title: "23.5 XR for Human–Robot Collaboration: HMDs, Smart Glasses and Their Sensors"
tags: [robotics, hri, xr]
study-depth: Working
wiki-support: Working
depth-goal: "Place any headset or pair of glasses in its class and say what it shows and senses; list what a developer can read from a Meta Quest 3 and a Meta Ray-Ban Display; add up a hologram's registration error on S1 and say what AR can and cannot guide; and place an XR paper on the research map by theme and evidence rung."
mastery-when: "Raise to Mastery when an XR interface or headset-recorded data carries the thesis contribution: the robot's intent shown during S1's hold, a headset used for alignment, or egocentric demonstrations for the panel task."
---

> [!note] Prerequisites · 선수 지식
> Visual–inertial odometry and fusion from [[04-robotics/state-estimation-slam|3. State Estimation]] (§7.2, §8) · the IMU's drift terms from [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] (§2, §3) · the pinhole model, PnP and calibration from [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] (§1, §2.7, §5) · motion blur and time stamps from [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors]] (§2, §9) · frames and a latency budget from [[04-robotics/robot-systems-deployment|10. Robot Systems]] (§3, §4) · rigid transforms from [[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]] (§3) · the quintic time scaling from [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9]] (§1) · interfaces and the safety vocabulary from [[04-robotics/hri-safety|11. HRI & Safety]] (§5, §6) · the interface spectrum and retargeting from [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration]] (§3, §4, §5) · gaze from [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]] (§4) · the helmet camera E1 from [[04-robotics/egocentric-perception|22. Egocentric Perception]] (§3, §5) · the cue cascade from [[04-robotics/human-intent-prediction|23. Human Intent]] (§2) · the Tier A conventions of [[02-foundations/lab-kernel|0.7 Lab Kernel]]
> [[04-robotics/state-estimation-slam|3. 상태 추정]]의 시각–관성 주행거리계와 융합(§7.2, §8) · [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]의 IMU 드리프트 항(§2, §3) · [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정]]의 핀홀 모델, PnP, 보정(§1, §2.7, §5) · [[04-robotics/perception-sensors-rigs|3.6 인식 센서]]의 모션 블러와 타임스탬프(§2, §9) · [[04-robotics/robot-systems-deployment|10. 로봇 시스템]]의 좌표계와 지연 예산(§3, §4) · [[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]]의 강체 변환(§3) · [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장]]의 5차 시간 스케일링(§1) · [[04-robotics/hri-safety|11. HRI·안전]]의 인터페이스와 안전 어휘(§5, §6) · [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연]]의 인터페이스 스펙트럼과 리타기팅(§3, §4, §5) · [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]]의 시선(§4) · [[04-robotics/egocentric-perception|22. 1인칭 인식]]의 헬멧 카메라 E1(§3, §5) · [[04-robotics/human-intent-prediction|23. 사람 의도]]의 단서 사슬(§2) · [[02-foundations/lab-kernel|0.7 Lab Kernel]]의 Tier A 규약

## English

*Group J, after 23. Stands on [[04-robotics/state-estimation-slam|3 §7.2]], which estimates a moving camera's pose — its position and orientation — from its images and its inertial measurement unit (IMU, the gyroscopes and accelerometers of [[04-robotics/sensor-models|3.2]]), on [[04-robotics/geometric-perception-calibration|3.5 §2.7]], which turns a marker into a pose, and on [[04-robotics/perception-sensors-rigs|3.6 §9]], which turns a wrong time stamp into millimetres. First use of the page-local object **X1**; a later use of S1, the construction track's facade-panel task ([[05-construction-robotics/site-engineering|2.5]]).*

A headset on a worker's head is two things at once. It is a display that can put the robot's next move on the wall where the panel will go, and it is a sensor rig that already measures where the worker's head is, where the hands are and, on some devices, where the eyes look. **This page treats both, on one scene, and asks of every claim: at what distance, at what head speed, with what latency, and on which device.**

> [!note] Why this matters · 왜 배우는가
> This page is the human side of two layers of the physical-AI stack in [[07-research-program/index|7. Research Program §5]], perception and task completion: the interface through which a worker sees what the robot will do next and the robot sees where the worker looks and reaches. In *"Install that panel on the frame"* it serves two of the eight steps, moving the component and performing the fitting, where the robot brings the panel to the frame and a worker helps fit and fasten it (its chip sits in the perception layer of the [[physical-ai-map|Physical AI Map]], beside 21 and 22), and the task is S1 of [[05-construction-robotics/site-engineering|2.5]], a 20 kg facade panel whose two holes must land within ±5 mm. Without this page a headset is either trusted as a gauge or dismissed: on this page's scene the hole's hologram, XR's word for a rendered virtual object, is 7.40 mm off with the head still and 19.18 mm during a 90 °/s turn, so it cannot check ±5 mm, yet the same headset can show the robot's next move, record the worker's head and hands, and collect demonstrations. It leads to [[05-construction-robotics/hrc-worker-centered|6. HRC §6–§8]] (the 8 m lane along which the robot carries the panel and the hold at the wall, each with a worker beside the robot), [[04-robotics/teleoperation-demonstration|12 §4]] (the interface spectrum), [[05-construction-robotics/imitating-contact|10. Imitating Contact §1]] (whose demonstrations it can supply) and [[03-deep-learning/vla/index|4. VLA §7]] (the embodiment gap); it is off the dissertation path of [[07-research-program/index|7 §8]] and enters, as [[07-research-program/index|7 §9]] says of human perception, when the site asks for it. After it you can place any headset or pair of glasses in its class, say what a developer can read from a Quest 3 and a Ray-Ban Display, and compute on S1 what AR can and cannot guide.

> [!note] First pass · 처음이라면
> Three sittings. **Sitting 1 — the devices.** Read the Running object, find on the picture the two devices' views and the three frames, then read §1 and §2; stop at the access table of §2 and say, for each device, what a robot could log from it. **Sitting 2 — the budget.** Read §3, then work the Worked case's six steps by hand before running §10's Parts 1–3; self-check 2 closes the sitting. **Sitting 3 — what the field has done.** Read §4–§6 and the map of §9, noting each work's evidence rung. §7 and §8 come before any site study, and the problem set closes the page.

### Running object · 이 페이지의 대상

**X1 — a worker's headset beside S1.** S1 is the construction track's frozen task from [[05-construction-robotics/site-engineering|2.5 Site Robotics]]: a mobile manipulator places a $20\,\mathrm{kg}$ facade panel so that two holes $400\,\mathrm{mm}$ apart land within $\pm5\,\mathrm{mm}$, then holds it while a worker fastens it. X1 is the moment the robot brings the panel's right-hand hole onto its bracket and the worker, standing beside the robot, watches through a headset. No plant of [[02-foundations/lab-plants|0.6 Lab Plants]] fits — a plant, in control language, is the system being controlled, and that catalog freezes six of them, P1–P6 — because none of them has a head or a display, so this page freezes X1 here and never changes its numbers.

Four frames carry the scene, each a pose in the sense of [[02-foundations/se3-geometry|8 §3]] — a position and an orientation together. **W** is the headset's world frame, fixed where its tracking started; **H** is the headset on the worker's head; **B** is the robot base, which carries a printed marker; **T** is the target hole. The robot knows T in B; the headset knows H in W; the link between the two worlds, $T_{WB}$, is the anchor that §3 measures.

| quantity | symbol | value |
|---|---|---:|
| eyes to the target hole | $D$ | $1.5\,\mathrm m$ |
| marker B to the target hole | $L$ | $1.2\,\mathrm m$ |
| head angular speed | $\omega$ | $0$, $30$, $90$, $300$ °/s |
| head tracking error: position, orientation | $e_{p,H}$, $\delta\theta_H$ | $2\,\mathrm{mm}$, $0.05^\circ$ |
| anchor error: position, rotation | $e_{p,A}$, $\delta\theta_A$ | $2\,\mathrm{mm}$, $0.10^\circ$ |
| motion-to-photon latency without prediction, and left after it | $\tau$, $\tau_{\mathrm{eff}}$ | $20\,\mathrm{ms}$, $5\,\mathrm{ms}$ |
| passthrough latency of device Q | $\tau_{\mathrm{pt}}$ | $40\,\mathrm{ms}$ |
| robot state reaching the headset | $\tau_{\mathrm{net}}$ | $50\,\mathrm{ms}$ |
| a message reaching device G's display | $\tau_G$ | $0.3\,\mathrm s$ |
| panel speed: final approach, and the lane | $v$ | $0.05$, $0.5\,\mathrm{m/s}$ |
| tolerance, and a coarse guidance band | | $\pm5\,\mathrm{mm}$, $50\,\mathrm{mm}$ |

Every number in this table is a **course number**, chosen for clean arithmetic and not measured on any device. Three are borrowed: $90$ and $300$ °/s are the head rates of E1, the helmet camera frozen in [[04-robotics/egocentric-perception|22. Egocentric Perception]] — $90$ °/s is the bound Grossman et al. measured for walking and running in place, and $300$ °/s a look-around chosen on that page — and $0.5\,\mathrm{m/s}$ is the base's lane speed of [[05-construction-robotics/hrc-worker-centered|6. HRC]]. $30$ °/s is a head following the panel: $0.5\,\mathrm{m/s}$ seen from $1\,\mathrm m$ is $0.5\,\mathrm{rad/s} = 28.6$ °/s. $\tau_{\mathrm{pt}} = 40\,\mathrm{ms}$ sits at the top of an independent measurement quoted in §3. The three latencies are defined in §3; in a line each: **motion-to-photon latency** $\tau$ is the time from a head motion to the light on the display that shows it, which a runtime that predicts where the head will be when the frame appears cuts to an equivalent $\tau_{\mathrm{eff}}$; **passthrough latency** $\tau_{\mathrm{pt}}$ is how late Q's cameras show the real world, since Q shows it as video (§1).

The two featured devices are real products, and their numbers are the makers', checked on Meta's own pages (Sources):

| | **Q** — Meta Quest 3 | **G** — Meta Ray-Ban Display |
|---|---|---|
| class (§1) | video-passthrough headset | display smart glasses |
| display | $2064\times2208$ px per eye, $25$ px/deg, $110^\circ\times96^\circ$, $72$/$90$/$120\,\mathrm{Hz}$ | one full-colour panel in the right lens, $600\times600$ px, $42$ px/deg, additive |
| world cameras | 2 RGB passthrough cameras ($18$ px/deg) and a depth projector; 4 IR and 2 RGB cameras for hand tracking | one $12\,\mathrm{MP}$ camera |
| eyes, hands | no eye tracking; hand tracking | neither; a Meta Neural Band (surface EMG) for gestures |
| mass, battery | $515\,\mathrm g$ without the facial interface; up to $2.2\,\mathrm h$ on average | $69\,\mathrm g$; up to $6\,\mathrm h$ of mixed use |

The Neural Band reads surface electromyography (EMG), the electrical activity of the forearm's muscles, and turns it into gestures.

*Scope: this page teaches what XR devices are and sense, how a hologram's registration error adds up on S1, and what research has shown XR doing for collaboration, teaching and data, with a map of that research. It does not teach visual–inertial odometry ([[04-robotics/state-estimation-slam|3 §7.2]]), camera geometry and PnP ([[04-robotics/geometric-perception-calibration|3.5]]), clock synchronisation ([[04-robotics/perception-sensors-rigs|3.6 §9]]), the separation distance ([[04-robotics/hri-safety|11 §6]]), teleoperation stability ([[04-robotics/teleoperation-demonstration|12 §3]]) or the optics of displays.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="X1 in plan and to scale: the worker's eyes H 1.5 m from the target hole T on S1's panel, the marker B on the robot base 1.2 m from T, the Quest 3's 110-degree view and the Ray-Ban Display's 14.3-degree panel, which covers 0.47 m of this wall. Below, the hologram's error at T: 7.40 mm with the head still, 11.33, 19.18 and 46.67 mm at 30, 90 and 300 degrees per second with 5 ms of latency left after prediction, and 54.53 mm at 90 degrees per second without prediction, against S1's 5 mm and a 50 mm band">
  <defs><marker id="xrArr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker>
  <pattern id="xrHat" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/></pattern></defs>
  <g fill="currentColor" font-size="11">
    <text x="12" y="18" font-size="12" font-weight="600" fill-opacity="0.85">X1 in plan, to scale (1 m = 110 px)</text>
    <rect x="27" y="48" width="363" height="10" fill="url(#xrHat)" stroke="none"/>
    <line x1="27" y1="58" x2="390" y2="58" stroke="currentColor" stroke-width="1.6"/>
    <text x="27" y="43" font-size="10.5" fill-opacity="0.8">facade wall</text>
    <rect x="170" y="58" width="88" height="5.5" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
    <circle cx="192" cy="60.8" r="2.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <circle cx="236" cy="60.8" r="2.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <line x1="207.5" y1="56" x2="259.6" y2="56" stroke="currentColor" stroke-width="3.2" stroke-opacity="0.85"/>
    <text x="267.6" y="43" font-size="10.5" text-anchor="start">G covers 0.47 m of wall</text>
    <rect x="112.8" y="163.6" width="66" height="48.4" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
    <path d="M131.5 163.6 L126 113 L197.5 64.6" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.4" stroke-linejoin="round"/>
    <rect x="152.8" y="159.6" width="8" height="8" fill="currentColor" fill-opacity="0.85"/>
    <text x="163.8" y="178.6" font-size="11" font-weight="600">B</text>
    <line x1="156.8" y1="163.6" x2="236" y2="58" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
    <text x="188.4" y="114.8" font-size="11" text-anchor="end">L = 1.2 m</text>
    <line x1="335" y1="190" x2="259.6" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="335" y1="190" x2="207.5" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="335" y1="190" x2="356.2" y2="125.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <line x1="335" y1="190" x2="266.8" y2="192.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <polyline points="266.8,192.2 266.9,186.3 267.5,180.4 268.6,174.5 270.2,168.8 272.3,163.2 274.9,157.8 277.9,152.7 281.4,147.9 285.2,143.4 289.5,139.2 294.1,135.4 299,132.1 304.2,129.2 309.6,126.7 315.2,124.7 321,123.3 326.8,122.3 332.8,121.8 338.7,121.9 344.6,122.5 350.5,123.6 356.2,125.2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="328.3" y="117.9" font-size="11" font-weight="600">Q</text>
    <text x="282.3" y="108.4" font-size="11" font-weight="600">G</text>
    <line x1="335" y1="190" x2="238.5" y2="61.5" stroke="currentColor" stroke-width="1.4" marker-end="url(#xrArr)"/>
    <text x="317.3" y="156.4" font-size="11">D = 1.5 m</text>
    <circle cx="236" cy="58" r="3.2" fill="currentColor"/>
    <text x="232" y="44" font-size="11" font-weight="600" text-anchor="middle">T</text>
    <circle cx="335" cy="190" r="9" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
    <text x="322" y="205" font-size="11" font-weight="600" text-anchor="end">H</text>
    <line x1="379" y1="223" x2="401" y2="223" stroke="currentColor" stroke-width="1.2" marker-end="url(#xrArr)"/>
    <line x1="379" y1="223" x2="379" y2="201" stroke="currentColor" stroke-width="1.2" marker-end="url(#xrArr)"/>
    <text x="365" y="227" font-size="11" font-weight="600">W</text>
    <path d="M375 229 Q247 247.2 158.8 169.6" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="1.5 2.5"/>
    <text x="197.5" y="236.2" font-size="10" fill-opacity="0.85">anchor T_WB</text>
    <path d="M375 218 L343 195" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="1.5 2.5"/>
    <text x="407" y="217" font-size="10" fill-opacity="0.85">head pose T_WH</text>
    <text x="404" y="78" font-size="10.5"><tspan font-weight="600">T</tspan> target hole on S1's panel</text>
    <text x="404" y="95" font-size="10.5"><tspan font-weight="600">B</tspan> marker on the robot base</text>
    <text x="404" y="112" font-size="10.5"><tspan font-weight="600">H</tspan> worker's eyes, headset on</text>
    <text x="404" y="129" font-size="10.5"><tspan font-weight="600">W</tspan> headset's world frame</text>
    <text x="404" y="146" font-size="10.5"><tspan font-weight="600">Q</tspan> Quest 3, 110° view</text>
    <text x="404" y="163" font-size="10.5"><tspan font-weight="600">G</tspan> Ray-Ban Display, 14.3°</text>
    <line x1="8" y1="252" x2="552" y2="252" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="270" font-size="12" font-weight="600" fill-opacity="0.85">the hologram's error at T, mm (1 mm = 7 px)</text>
    <rect x="330" y="262" width="10" height="9" fill="currentColor" fill-opacity="0.75"/><text x="343" y="270" font-size="10">head</text>
    <rect x="400" y="262" width="10" height="9" fill="currentColor" fill-opacity="0.4"/><text x="413" y="270" font-size="10">anchor</text>
    <rect x="470" y="262" width="10" height="9" fill="url(#xrHat)" stroke="currentColor" stroke-width="0.6"/><text x="483" y="270" font-size="10">latency</text>
    <line x1="167" y1="284" x2="167" y2="405" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>
    <text x="171" y="281" font-size="10" text-anchor="start">S1 ±5 mm</text>
    <line x1="482" y1="284" x2="482" y2="405" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>
    <text x="478" y="281" font-size="10" text-anchor="end">50 mm band</text>
    <text x="552" y="281" font-size="10" text-anchor="end" fill-opacity="0.85">total</text>
    <text x="126" y="302" font-size="10.5" text-anchor="end">head still</text>
    <rect x="132" y="292" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="292" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="292" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="292" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <text x="552" y="302" font-size="10.5" font-weight="600" text-anchor="end">7.40</text>
    <text x="126" y="326" font-size="10.5" text-anchor="end">30 °/s</text>
    <rect x="132" y="316" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="316" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="316" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="316" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="316" width="27.5" height="13" fill="url(#xrHat)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="326" font-size="10.5" font-weight="600" text-anchor="end">11.33</text>
    <text x="126" y="350" font-size="10.5" text-anchor="end">90 °/s</text>
    <rect x="132" y="340" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="340" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="340" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="340" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="340" width="82.5" height="13" fill="url(#xrHat)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="350" font-size="10.5" font-weight="600" text-anchor="end">19.18</text>
    <text x="126" y="374" font-size="10.5" text-anchor="end">300 °/s</text>
    <rect x="132" y="364" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="364" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="364" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="364" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="364" width="274.9" height="13" fill="url(#xrHat)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="374" font-size="10.5" font-weight="600" text-anchor="end">46.67</text>
    <text x="126" y="398" font-size="10.5" text-anchor="end">90 °/s, no prediction</text>
    <rect x="132" y="388" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="388" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="388" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="388" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="388" width="329.9" height="13" fill="url(#xrHat)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="398" font-size="10.5" font-weight="600" text-anchor="end">54.53</text>
    <line x1="132" y1="411" x2="517" y2="411" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
    <line x1="132" y1="411" x2="132" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="132" y="426" font-size="10" text-anchor="middle">0</text>
    <line x1="202" y1="411" x2="202" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="202" y="426" font-size="10" text-anchor="middle">10</text>
    <line x1="272" y1="411" x2="272" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="272" y="426" font-size="10" text-anchor="middle">20</text>
    <line x1="342" y1="411" x2="342" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="342" y="426" font-size="10" text-anchor="middle">30</text>
    <line x1="412" y1="411" x2="412" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="412" y="426" font-size="10" text-anchor="middle">40</text>
    <line x1="482" y1="411" x2="482" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="482" y="426" font-size="10" text-anchor="middle">50</text>
    <text x="12" y="443" font-size="10" fill-opacity="0.8">latency left after prediction 5 ms; without prediction 20 ms</text>
  </g>
</svg>

X1 in plan and to scale: the worker's eyes H are $1.5\,\mathrm m$ from the target hole T, the marker B on the robot base $1.2\,\mathrm m$ from it; Q's view spans $110^\circ$ while G's panel spans $14.3^\circ$, $0.47\,\mathrm m$ of this wall. Below, the hologram's error at T: $7.40\,\mathrm{mm}$ with the head still, $11.33$, $19.18$ and $46.67\,\mathrm{mm}$ at $30$, $90$ and $300$ °/s with $5\,\mathrm{ms}$ of latency left after prediction, and $54.53\,\mathrm{mm}$ at $90$ °/s without prediction, against S1's $\pm5\,\mathrm{mm}$ and a $50\,\mathrm{mm}$ band.

### 1. The reality–virtuality continuum and the device classes

*In one sentence:* AR, MR, VR and XR name places on one line from the real world to a rendered one, and a device's class — how the real world reaches the eye and what the device tracks — decides what it can show before any software runs.

**The problem.** Papers write "an AR interface" for a tablet, a projector, a see-through headset and a camera-passthrough headset alike, and the four show a robot's plan through different optics, with different delays and different failures. The class is the first thing to read.

**The continuum.** Milgram and Kishino (1994) anchored one end of a line with a purely real environment, "consisting solely of real objects", and the other with a purely virtual one, and called any display that presents real and virtual objects together **mixed reality** (MR). Augmented reality (AR) is MR where the real world is augmented with virtual content; augmented virtuality (AV) is MR where most content is virtual; virtual reality (VR) is the virtual end. These words are quoted from Skarbez, Smith and Whitton (2021), who revisit the continuum; the original IEICE page sits behind a bot check and was not opened. **XR** is the umbrella: the W3C's WebXR specification uses it for the whole "spectrum of hardware, applications, and techniques" of VR, AR and related technologies, and Khronos's OpenXR, the cross-vendor interface that Meta, Microsoft, Magic Leap, HTC, Valve and PICO devices implement, defines XR as a continuum of real-and-virtual environments inclusive of VR, AR and MR.

> [!info] Definition — mixed reality
> A **class of displays and experiences**, not a device: those that present real and virtual objects in one view. Three conditions. The view contains **real content**, seen directly or through a camera; it contains **rendered content**; and the two are presented **together**, in one field of view, so a laptop screen beside a robot is not MR. This page reads the continuum through one number, the share of the view that is rendered:
> $$v=\frac{\Omega_{\text{rendered}}}{\Omega_{\text{view}}},\qquad \text{MR}\iff 0 < v < 1$$
> where $\Omega$ is a solid angle in steradians, [[04-robotics/egocentric-perception|22's measure of how much of the sphere a view covers]]; $v=0$ is the real environment, $v=1$ is VR, AR is MR with $v$ small and AV is MR with $v$ near one. The share is this page's teaching device, not Milgram and Kishino's.
> **Example.** G's $14.3^\circ$ square panel covers $0.0618\,\mathrm{sr}$, $2.4\%$ of the $2.618\,\mathrm{sr}$ that Q's $110^\circ\times96^\circ$ view spans: G sits near the real end. Q can render any share of its view, up to all of it.
> **Non-example.** Q showing passthrough with nothing rendered is $v=0$: the worker sees only real content, but through cameras, $\tau_{\mathrm{pt}}$ late (§3), which is not the same experience as seeing through glass.
> **Why it matters.** With the next definition, it tells you what a device can hide, what it adds, and which part of the view lags.

**How the real world reaches the eye** is the most consequential fact about a headset beside a moving robot.

> [!info] Definition — optical and video see-through
> A **property of a head-mounted display (HMD)**: the path by which light from the real world reaches the eye. **Optical see-through (OST)**: real light passes through a combiner such as a waveguide, and the display *adds* light to it. **Video see-through (VST)**: cameras capture the world and the display shows camera pixels composited with rendered ones. Conditions that separate them: whether real light reaches the eye **directly**; whether the display can **subtract** light (OST cannot, except through an added dimmer); and **which content lags**: in OST only the rendered part, in VST all of it.
> $$\text{OST: } L_{\text{eye}}(t)=L_{\text{world}}(t)+L_{\text{virt}}(t-\tau),\qquad \text{VST: } L_{\text{eye}}(t)=(1-\alpha)\,L_{\text{world}}(t-\tau_{\mathrm{pt}})+\alpha\,L_{\text{virt}}(t-\tau)$$
> where $L$ is light reaching the eye, $\tau$ the rendering latency, $\tau_{\mathrm{pt}}$ the passthrough latency and $\alpha\in[0,1]$ the opacity of the rendered layer.
> **Example.** G is OST: Meta's developer page calls its display "an additive waveguide", on which "a pixel rendered as pure black is fully transparent". Q is VST: two RGB cameras feed its displays.
> **Non-example.** A dimmer does not make OST into VST. Magic Leap 2's dimmer panel "selectively subtracts photons" to darken the world behind content, yet real light still arrives directly and without delay.
> **Why it matters.** Beside a moving robot, OST shows the robot where it is and the hologram late; VST shows both late. §3 prices both.

**The device classes.** Six classes cover what research and sites use; the examples are named only where the maker's own page was read.

| class | the world reaches the eye | tracks | can show | examples |
|---|---|---|---|---|
| VR headset | not at all | head (6-DoF), hands or controllers | a rendered world | Q in VR mode |
| video-passthrough MR headset | through cameras | head, hands, depth; eyes on some | world-locked content on video, can hide the world | **Q, Meta Quest 3**; Apple Vision Pro |
| optical see-through AR headset | directly, through a waveguide | head, hands, eyes, depth | additive world-locked holograms | Microsoft HoloLens 2 and Trimble XR10 (a HoloLens 2 in a hard hat); Magic Leap 2 |
| display smart glasses | directly | orientation; a camera | a small head-locked panel | **G, Meta Ray-Ban Display**; RealWear Navigator 520 |
| camera-only smart glasses | directly | a camera and audio | nothing but sound | Ray-Ban Meta (Gen 2) |
| research glasses | directly | head, eyes, IMUs, SLAM cameras | nothing visual; they record (Gen 2 adds audio feedback) | Project Aria Gen 1 and Gen 2 |

Here 6-DoF means six degrees of freedom, three of position and three of orientation, and a SLAM camera serves simultaneous localisation and mapping, tracking that builds its own map (§2). World-locked content keeps its place in the room while the head moves; head-locked content keeps its place on the display and moves with the head (§3 defines both). The optical see-through class is thinning: Microsoft's release notes state that as of December 2024 HoloLens devices are no longer manufactured, with security updates through December 2027, and Magic Leap's terms of sale set the end of direct sales of Magic Leap 2 at 31 March 2026. Three of the four intent studies in §4 name a Microsoft HoloLens, so part of that evidence was measured on a device that is no longer made.

**What the two featured devices can show.** Q renders world-locked content over its passthrough, so a virtual object stays on the wall while the worker walks around it, and opaque rendering hides the world behind it. G shows $600\times600$ pixels in the right lens at $42$ pixels per degree; assuming a uniform density, the panel is $600/42 = 14.3^\circ$ across and $20.2^\circ$ diagonally, $0.376\,\mathrm m$ wide seen square-on at $D=1.5\,\mathrm m$, and it moves with the head. Meta places it "off to the side, so it doesn't obstruct your view", "designed for short interactions". Q draws geometry in the scene; G shows messages about the scene.

**The trap.** "AR" in a title says nothing about the class. Read the device, then ask two questions: does the real world reach the eye directly, and is the content anchored in the world or fixed to the head?

> [!note]- Deeper · 더 깊이
> **The other classes' numbers, from the makers' pages.** Apple Vision Pro (M5): two main cameras, six world-facing tracking cameras, four eye-tracking cameras, a TrueDepth camera, a LiDAR scanner and four IMUs; "12-millisecond photon-to-photon latency"; $750$–$800\,\mathrm g$; up to $2.5\,\mathrm h$. HoloLens 2: four visible-light head-tracking cameras (the forward pair $96.1^\circ$ diagonal, $98.6\,\mathrm{mm}$ apart), two infrared eye-tracking cameras, a $1$-megapixel time-of-flight depth sensor, an IMU with magnetometer; $566\,\mathrm g$; $2$–$3\,\mathrm h$. RealWear Navigator 520, sold as "assisted reality": a $1280\times720$, $24^\circ$ display on an adjustable boom arm, a $50\,\mathrm{MP}$ camera, four noise-cancelling microphones, IP66, $270\,\mathrm g$. **Why the virtual end is unreachable**, for Skarbez et al.: a headset controls what the eyes and ears receive but not the body's senses of balance and movement, so some sensory conflict always remains — §8's cybersickness.

### 2. The HMD as a sensor rig

*In one sentence:* to keep content in place a headset must know its own pose many times per displayed frame, so it already carries cameras, an IMU and often hand and eye tracking — a sensor rig on the worker's head, from which a robot can read what the maker exposes.

**The problem.** A robot beside a worker wants to know where the head is and points, where the eyes look, and where the hands are. [[04-robotics/human-pose-gaze|21 §4]] shows that gaze is the strongest single cue to the next action and that a robot's own camera sees only head pose beyond a few metres. A headset measures all three for its own rendering. What can a developer actually read out, how fast, and under which rules?

**The idea.** An HMD estimates its pose from its own sensors; that is what makes it wearable anywhere.

> [!info] Definition — inside-out tracking
> A **pose-estimation method**: the device estimates its own 6-DoF pose from sensors it carries, by observing the environment, with no external infrastructure. Three conditions: the sensors are **on the device** (cameras, an IMU, sometimes depth); the pose is expressed in a **map the device builds** of its surroundings, its world frame W; and the estimate is **fused** from fast inertial and slow visual measurements, which is visual–inertial odometry (VIO) with a map, or SLAM ([[04-robotics/state-estimation-slam|3 §7.2]]).
> $$T_{WH}(t_k)=\arg\min_{T}\Big(\sum_j \big\lVert \tilde u_j-\pi(T^{-1}p_j)\big\rVert^2_{\Sigma_u}+\big\lVert r_{\mathrm{IMU}}(T,T_{WH}(t_{k-1}))\big\rVert^2_{\Sigma_I}\Big)$$
> where $\tilde u_j$ are the pixels at which mapped points $p_j$ are seen, $\pi$ projects a point into the camera ([[04-robotics/geometric-perception-calibration|3.5 §1]]), and $r_{\mathrm{IMU}}$ is the mismatch with the motion the IMU integrated since the last estimate, each weighted by its noise.
> **Example.** HoloLens 2 tracks the head with four visible-light cameras and an IMU; Project Aria Gen 1 with two monochrome global-shutter SLAM cameras of $150^\circ$ horizontal view and two IMUs.
> **Non-example.** Outside-in tracking, where external cameras or a motion-capture system track markers on the device, as HOT3D's ground truth was obtained (§6). Nor is an orientation from an IMU alone inside-out 6-DoF tracking: G's web apps receive heading, tilt and roll, and no head position (their location comes from the paired phone).
> **Why it matters.** It fails where VIO fails — blank walls, darkness, fast motion, a scene that moves with the camera — which lists a construction site's commonest conditions.

**Why the IMU runs so much faster than the cameras.** A head turning at $300$ °/s turns $10.0^\circ$ between two frames of a $30\,\mathrm{Hz}$ camera and $0.30^\circ$ between two samples of a $1\,\mathrm{kHz}$ IMU, while the display needs a fresh pose for every frame, $72$ to $120$ times a second on Q. Over one camera interval a gyroscope barely drifts: with the gyro of [[04-robotics/sensor-models|3.2 §3]], $1/30\,\mathrm s$ adds $0.0013^\circ$, $0.03\,\mathrm{mm}$ at $D$; left alone for ten seconds it drifts $0.104^\circ$, $2.72\,\mathrm{mm}$. So the IMU carries the pose between frames and the cameras keep correcting it. Project Aria shows the split: two IMUs at $800$ and $1000\,\mathrm{Hz}$ — different models, so that "their higher-order error behaviors are more likely to be uncorrelated" — fused with the cameras into $1\,\mathrm{kHz}$ trajectories whose open-loop drift is at most $0.4\%$ of the distance travelled.

**The trap: range as well as rate.** Aria's left IMU saturates at $500$ °/s (its right one at $1000$ °/s). Grossman et al., the source of E1's head rates, measured a group-median peak of $780$ °/s in vigorous voluntary head turns, $1.56$ times that limit. An IMU that clips during a fast glance hands the filter a wrong rotation at the very moment the view changes most.

**What the two featured devices sense, and what a developer can read.** This is the table to keep. An API (application programming interface) is the set of calls an app may make, an SDK (software development kit) packages them, and Horizon OS is the Quest's operating system. Every entry comes from Meta's product or developer pages; where the pages say nothing, the table says "not documented".

| | Q — Meta Quest 3 | G — Meta Ray-Ban Display |
|---|---|---|
| way in | apps on the headset (Meta XR SDKs, OpenXR, Android) | a phone app through the Wearables Device Access Toolkit, in developer preview; or a web app that runs on the glasses |
| head | 6-DoF pose from the runtime, predicted for each frame's display time | orientation only, through the standard DeviceMotion and DeviceOrientation web APIs (accelerometer, gyroscope, compass), with the wearer's permission; no position documented |
| eyes | none: Quest 3 has no eye tracking | not documented |
| hands | hand skeleton at $30\,\mathrm{Hz}$ by default, up to $60\,\mathrm{Hz}$ in Fast Motion Mode; Wide Motion Mode fills in "plausible" poses when the hands leave the cameras' view; Touch Plus controllers | none; touchpad and Neural Band gestures arrive as arrow-key and Enter events, and web apps get no continuous cursor |
| camera | Passthrough Camera API (Android Camera2, Horizon OS v74+): left and right RGB cameras, $1280\times960$ or $1280\times1280$, up to $60\,\mathrm{Hz}$, image capture latency $20$–$40\,\mathrm{ms}$, with intrinsics, extrinsics, timestamps and the camera's world pose; it does not cover the whole passthrough view | toolkit only: video at $720\times1280$, $504\times896$ or $360\times640$ and $2$, $7$, $15$, $24$ or $30$ frames per second over Bluetooth Classic, reduced first in resolution, then in frame rate but never below $15$, when bandwidth runs short; photos. Web apps have no camera |
| depth, scene | Depth API: real-time depth maps, unreliable closer than $0.2\,\mathrm m$; spatial anchors that persist and can be shared | location from the paired phone, to $5$–$50\,\mathrm m$ by Meta's estimate |
| sound | integrated stereo speakers | toolkit: microphones as $8\,\mathrm{kHz}$ mono over the Hands-Free Profile; speakers |
| display out | anything the app renders, world-locked or head-locked | $600\times600$ px: toolkit layouts sent from the phone over Bluetooth, each send replacing the whole display; or a web app's HTML |
| permissions | `CAMERA` or `HEADSET_CAMERA` for the cameras; a hand-tracking permission and feature flag | camera permission confirmed in the Meta AI app (always, once, deny); a sensor prompt for web apps |
| data rules | hand data "only permitted to be used for enabling hand tracking within your app"; camera images are Device User Data under Meta's Developer Data Use Policy | the capture LED blinks when content is captured for the gallery, and covering it disables the camera |

**What a robot gets from each.** From Q: the worker's head pose in 6-DoF, the hands, two calibrated camera streams with poses and time stamps, and depth. That is enough to show the robot's plan in place (§4), to teleoperate or record demonstrations (§5) and to collect first-person data (§6). There is no eye gaze, so attention stays a head-pose proxy, with every caveat of [[04-robotics/egocentric-perception|22 §3]]. From G, by two separate routes: a phone app receives the worker's first-person video at up to $30$ frames per second and audio, and a web app on the glasses reads head orientation and a coarse location; the pages read do not say whether the two can run together. Both can write to G's head-locked panel. Nothing in the documentation gives G's head position. Without it the direction from the eye to a point in the world cannot be kept: at $D=1.5\,\mathrm m$ a sideways step of $0.3\,\mathrm m$ turns the true bearing of T by $\arctan(0.3/1.5)=11.3^\circ$, while an orientation-only arrow would not move.

**The traps.** A pose from Wide Motion Mode is an estimate made when the hands were not seen; log it with its mode, or the demonstration corpus mixes measurements with guesses. The toolkit's camera frames arrive compressed to fit the Bluetooth link, and Meta warns that the image "may appear lower quality than expected, even when the resolution reports HIGH or MEDIUM". A research app that logs hand poses to train a robot should check Meta's rule that hand data is only for enabling hand tracking before the study, not after.

### 3. Registration and latency

*In one sentence:* a hologram of S1's hole is drawn through a chain — the robot base in the headset's world (the anchor), the head in that world (tracking), and the moment of display (latency) — and each link's error lands at the hole multiplied by its lever arm, so the budget is written at the hole, as S1's own is.

**The problem.** A worker will believe a mark drawn on the wall. How far from the true hole is it with the head still, how far while the head turns, and which link is worth improving?

**The chain.** The robot knows the hole in its base frame, $p_B$; the headset draws it at $p_W=T_{WB}\,p_B$ and projects it through its head pose $T_{WH}$ ([[04-robotics/robot-systems-deployment|10 §4]] names the frames, [[02-foundations/se3-geometry|8 §3]] composes them). Three things can be wrong: $T_{WB}$ (the anchor), $T_{WH}$ (tracking), and the time for which $T_{WH}$ was valid (latency). A rotation error $\delta\theta$ moves a point $\ell$ from its pivot by $\ell\,\delta\theta$, which is why S1's allocations are written at the hole ([[05-construction-robotics/site-engineering|2.5 §2]]); latency is the rotation $\omega\tau$ the head made since the pose was taken, [[04-robotics/perception-sensors-rigs|3.6 §9]]'s law $e=\omega\,\Delta t\,R$.

> [!info] Definition — registration error
> A **displacement**, in millimetres, between where a virtual object appears and where its real counterpart is, stated at a named point, for a named eye, at a named head speed. Four conditions: the **point** (here T, not the anchor); the **viewpoint** ($D$ from the eye); the **head motion** ($\omega$), because the latency term is zero only for a still head; and the **combination rule** for the terms, which, as in S1's budget, must be stated.
> $$e_{\text{reg}}=\big(e_{p,H}+D\,\delta\theta_H\big)+\big(e_{p,A}+L\,\delta\theta_A\big)+D\,\omega\,\tau_{\mathrm{eff}}$$
> where the first bracket is head tracking, the second the anchor with its lever $L$, and the last the latency term; angles are in radians in the small-angle form, which the tangent would change by at most $2.1\,\mathrm{nm}$ in the static terms and by $0.58\,\mathrm{mm}$ ($0.37\%$) in the largest latency term, $6^\circ$ at $300$ °/s and $20\,\mathrm{ms}$.
> **Example.** X1 with the head still: $3.31+4.09=7.40\,\mathrm{mm}$ (the Worked case).
> **Non-example.** A hologram's jitter while the head is held still is not its registration error; it is a stability number, and it omits both the anchor and the latency terms. Nor is the robot's own placement error part of it: the hologram is wrong or right about where T is, whatever the panel does.
> **Why it matters.** It decides what AR can guide. A gauge whose own error is $7.40\,\mathrm{mm}$ cannot check a $\pm5\,\mathrm{mm}$ tolerance.

**Latency, and why headsets predict.** Every frame is drawn from a pose measured earlier.

> [!info] Definition — motion-to-photon latency
> A **time interval**: from a motion of the head to the light, on the display, that shows the scene as seen from the new pose. Conditions: it is measured **end to end**, from sensing to photons, not as one stage of the pipeline; it is stated **with or without prediction**, since a runtime that predicts the pose for the display time hides most of it; and it is reported as a **distribution**, because spikes matter (§8).
> $$\tau=t_{\text{photon}}-t_{\text{motion}},\qquad \delta\theta_{\text{lat}}(t)=\theta(t)-\hat\theta(t)\approx\omega\,\tau\ \text{(no prediction)},\quad \approx\tfrac12\,\dot\omega\,\tau^2\ \text{(constant-rate prediction)}$$
> where $\theta$ is the head angle, $\hat\theta$ the angle the frame was drawn for, $\omega$ the rate and $\dot\omega$ the angular acceleration.
> **Example.** X1's $\tau=20\,\mathrm{ms}$ at $90$ °/s leaves the hologram $1.8^\circ$ behind the head, $47.12\,\mathrm{mm}$ at $D$; after prediction, $11.78\,\mathrm{mm}$.
> **Non-example.** Frame time is not latency: $1/90\,\mathrm s=11.1\,\mathrm{ms}$ is how often Q redraws at $90\,\mathrm{Hz}$, not how late each frame is. Passthrough (photon-to-photon) latency is a different interval too, from a change in the real scene to the display showing it.
> **Why it matters.** It is the only term of the budget that grows with head speed, and heads move fastest at the moments that matter.

OpenXR builds prediction into the interface: an app asks for its view poses at a display time, "the time for which the view poses are predicted", and the display time the runtime predicts "must refer to the midpoint of the interval during which the frame is displayed". What prediction cannot remove is the acceleration term, so a turn that starts or stops still smears (§10, Part 3).

**What $\tau_{\mathrm{eff}}$ stands for.** Constant-rate prediction of a perfectly steady turn would leave no error at all (Self-check 5). Real prediction misses a little: the rate it extrapolates is a noisy gyro estimate, the display time is itself a prediction, and a head seldom turns at one rate for long. X1 lumps those misses into one equivalent delay, $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$, a course number, so the budget charges $D\,\omega\,\tau_{\mathrm{eff}}$ with prediction on and $D\,\omega\,\tau$ with it off.

OptoFidelity, an independent test-equipment maker, measured headsets in 2024: with prediction and time warp (re-projecting a finished frame to the newest head pose just before it is shown), angular motion-to-photon medians were a few milliseconds, Quest Pro and Quest 3 best in the group and HTC's $4\,\mathrm{ms}$ "slightly higher than expected"; passthrough (photon-to-photon) minima were about $11\,\mathrm{ms}$ for Apple Vision Pro (Apple states $12$) and $35$–$40\,\mathrm{ms}$ for Quest 3, Quest Pro and HTC VIVE XR Elite. X1's $\tau_{\mathrm{pt}}=40\,\mathrm{ms}$ takes the top of that range.

**OST and VST fail differently beside a moving robot.** On G, or on any OST headset, the robot is seen where it is and only the rendered layer lags. On Q the whole view lags: a panel approaching at $0.05\,\mathrm{m/s}$ is seen $2.0\,\mathrm{mm}$ behind its true place, and at the lane's $0.5\,\mathrm{m/s}$, $20.0\,\mathrm{mm}$. A "ghost" of the robot drawn from its reported state, $\tau_{\mathrm{net}}=50\,\mathrm{ms}$ old, trails by $2.5$ and $25.0\,\mathrm{mm}$. Neither is a head-motion effect, so neither prediction nor a still head removes it.

**Aligning the headset's world to the robot's base.** $T_{WB}$ has to be measured. On Q the direct route is a marker on the robot and PnP — the pose of a known object from one image, [[04-robotics/geometric-perception-calibration|3.5 §2.7]] — on the passthrough camera, whose API supplies the intrinsics, the extrinsics, the image time stamp and the camera's pose in W at that stamp, so $T_{WB}=T_{WC}\,T_{CB}$ with $T_{CB}$ from PnP. Three cautions. A small, distant marker can flip between two nearly equal PnP solutions, and tilt is its weakest direction ($\pm2.70^\circ$ per view at $1$ pixel of noise for 3.5's $0.5\times0.4\,\mathrm m$ target at $2\,\mathrm m$), so use a large marker, several views and markers spread apart. The camera's pose must be taken at the image's own stamp, not on arrival $20$–$40\,\mathrm{ms}$ later ([[04-robotics/perception-sensors-rigs|3.6 §9]]). And the marker must be calibrated to the robot's frame ([[04-robotics/geometric-perception-calibration|3.5 §5]]).

> [!info] Definition — spatial anchor
> A **pose kept in the headset's map** so that content attached to it stays fixed in the world while tracking corrects itself. Conditions from Meta's documentation: it is **created at a point** and identified by a unique identifier (UUID); it is **re-found** by the headset's map in later sessions (persisted) and can be **shared** so that several headsets agree on one frame; it **cannot be moved** — to move content, delete the anchor and create a new one; and it is accurate **near itself**: Meta advises creating it within three metres of the object it holds, because pose errors "are amplified the further away an object is".
> $$p_W=T_{WA}\,p_A,\qquad \lVert\delta p_W\rVert\le e_{p,A}+\lVert p_A\rVert\,\delta\theta_A$$
> where $T_{WA}$ is the anchor's pose, $p_A$ the content's offset from the anchor, and $\delta\theta_A$ the anchor's rotation error.
> **Example.** X1's anchor, the marker on B, is $L=1.2\,\mathrm m$ from T, so its $0.10^\circ$ becomes $2.09\,\mathrm{mm}$ at the hole; at Meta's $3\,\mathrm m$ limit the same angle would give $5.24\,\mathrm{mm}$.
> **Non-example.** The world frame W itself is not an anchor: its origin is set by where tracking started, not by the task, and Meta's advice for a consistent mixed-reality space is to synchronise it with spatial anchors.
> **Why it matters.** It is the bridge between two worlds, the headset's and the robot's. The lever rule says to put the bridge next to the work.

> [!info] Definition — world-locked and head-locked content
> A **property of how rendered content is placed**. World-locked content holds a fixed pose in W, so its place on the display changes with every head motion. Head-locked content holds a fixed place on the display, so it moves with the head. Conditions: world-locking needs a **6-DoF head pose** and has a registration error; head-locking needs **no pose** and has none, because it claims no place in the world.
> $$\text{world-locked: } p_H(t)=T_{WH}(t)^{-1}\,p_W,\qquad \text{head-locked: } p_H(t)=\text{const}$$
> where $p_H$ is where the content sits relative to the head.
> **Example.** A target drawn on the hole by Q is world-locked. G's $600\times600$ panel is head-locked, and nothing in its documented interfaces anchors content to the world.
> **Non-example.** An arrow on G that turns with the compass heading is neither: it is locked in orientation only, and a $0.3\,\mathrm m$ step leaves it $11.3^\circ$ wrong about T.
> **Why it matters.** Only world-locked content owes the budget above; head-locked content owes a different cost, the glance away from the task (§8).

**The traps.** The latency term is a bias during a turn, always on the side the head came from, so it is added linearly, never root-sum-square (RSS) — the non-example of [[05-construction-robotics/site-engineering|2.5 §2]]. A hologram demonstrated with a still head has shown its best case. And a registration error measures the hologram, not the robot's placement.

### Worked case · 대상으로 한 번 끝까지

Six steps on X1: the budget of §3 at the hole, then what each featured device shows. They are course computations on the frozen numbers, not measurements of either device.

**Step 1 — head tracking at the hole.** The position error arrives unchanged; the orientation error arrives multiplied by $D$:

$$e_{p,H}+D\,\delta\theta_H=2+1500\times0.05\times\frac{\pi}{180}=2+1.31=3.31\,\mathrm{mm}$$

since $0.05^\circ$ is $8.73\times10^{-4}\,\mathrm{rad}$.

**Step 2 — the anchor.** The marker's rotation error acts over $L$, not $D$:

$$e_{p,A}+L\,\delta\theta_A=2+1200\times0.10\times\frac{\pi}{180}=2+2.09=4.09\,\mathrm{mm}$$

because the anchor pivots at B, $1.2\,\mathrm m$ from T. Put B at Meta's $3\,\mathrm m$ limit and the same $0.10^\circ$ gives $5.24\,\mathrm{mm}$, more than S1's whole tolerance, from the anchor alone.

**Step 3 — the head still.** Linearly, $3.31+4.09=7.40\,\mathrm{mm}$, outside $\pm5\,\mathrm{mm}$. Root-sum-square over the four sources, which assumes them independent and zero-mean, gives $\sqrt{2^2+1.31^2+2^2+2.09^2}=3.75\,\mathrm{mm}$, inside with $1.25\,\mathrm{mm}$ left. Even the kinder reading fails as a check. With $\pm3.75\,\mathrm{mm}$ of its own error, a hologram looking at a panel truly $5\,\mathrm{mm}$ off shows anything from $1.25$ to $8.75\,\mathrm{mm}$, so it cannot tell a good seat from a bad one.

**Step 4 — the head turning.** With $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$ left after prediction, the latency term $D\,\omega\,\tau_{\mathrm{eff}}$ is $3.93$, $11.78$ and $39.27\,\mathrm{mm}$ at $30$, $90$ and $300$ °/s, so the linear totals are $11.33$, $19.18$ and $46.67\,\mathrm{mm}$, all inside the $50\,\mathrm{mm}$ band. Without prediction, $\tau=20\,\mathrm{ms}$ at $90$ °/s adds $47.12\,\mathrm{mm}$ for $54.53\,\mathrm{mm}$, outside it. Solving $7.40+D\,\omega\,\tau=50$ for $\omega$:

$$\omega_{\max}=\frac{50-7.40}{D\,\tau}=\frac{42.60}{1500\times0.005}\,\mathrm{rad/s}=325^\circ/\mathrm s\quad\text{(}81^\circ/\mathrm s\text{ at }\tau=20\,\mathrm{ms})$$

because the latency term is the only one that grows with $\omega$. Prediction is what lets a walking worker keep the coarse band: $81$ °/s is just under the $90$ °/s of walking.

**Step 5 — what Q shows of the moving panel.** Passthrough shows the real panel $v\,\tau_{\mathrm{pt}}$ late: $0.05\times40=2.0\,\mathrm{mm}$ on the final approach and $20.0\,\mathrm{mm}$ on the lane. A robot ghost drawn from $50\,\mathrm{ms}$-old state trails by $2.5$ and $25.0\,\mathrm{mm}$. The resolution is not the limit. One passthrough pixel at $18$ px/deg is $1.45\,\mathrm{mm}$ at $D$, so a $5\,\mathrm{mm}$ offset spans over three pixels. The registration is.

**Step 6 — what G shows.** G's panel is $14.3^\circ$ square, $0.376\,\mathrm m$ wide square-on at $D$; on this wall, seen obliquely, it covers $0.47\,\mathrm m$. It is head-locked, and with no head position a $0.3\,\mathrm m$ step turns T's true bearing by $11.3^\circ$, so G cannot mark T at all. It can name T instead — "panel 3, bay B, right-hand hole next; robot moving" — and a message that takes $\tau_G=0.3\,\mathrm s$ to appear costs $1.6\times0.3=0.48\,\mathrm m$ of a worker walking at $1.6\,\mathrm{m/s}$, the timing arithmetic of [[04-robotics/hri-safety|11 §5]].

**The verdict.** On X1, world-locked AR guides at the coarse scale: which bracket, the approach path, the keep-out zone, the next action, all inside $50\,\mathrm{mm}$ while prediction runs. It cannot guide or check the last $\pm5\,\mathrm{mm}$. That stays with the robot's wrist camera and the release test of [[05-construction-robotics/hrc-worker-centered|6 §7]]. G guides by words and symbols, not by position.

### 4. XR for human–robot collaboration — communicating the robot's intent

*In one sentence:* showing the robot's plan where the work happens lets people read it faster and more accurately than on a screen, and the studies that show this were small, in laboratories, and mostly on headsets now leaving the market.

**The problem.** A worker beside the robot needs to know what it will do next — the path, the target, the zone it will sweep — early enough to act. [[04-robotics/hri-safety|11 §5]] puts it as timing: every second a person needs to notice and respond costs $1.6\,\mathrm m$ of floor.

**The idea.** Draw the plan in place, over the real robot, instead of on a separate screen the worker must look away to read. It runs [[04-robotics/human-intent-prediction|23 §2]]'s cue cascade in reverse: there the robot reads the person's gaze, head and hands before they act; here the person reads the robot's plan before it moves. A path shown $2\,\mathrm s$ ahead is $1.0\,\mathrm m$ of robot travel at $0.5\,\mathrm{m/s}$, and in those $2\,\mathrm s$ a worker walking at $1.6\,\mathrm{m/s}$ covers $3.2\,\mathrm m$. The display buys a decision before the crossing, not during it.

**What the studies measured.**

- **Arm motion over the real robot.** Rosen, Whitney, Phillips, Chien, Tompkin, Konidaris and Tellex (ISRR 2017; extended in IJRR 2019) drew a robot arm's planned motion in a Microsoft HoloLens, a mixed-reality headset. Thirty-two participants labelled motions as colliding or not with blocks on a table. Against a 2D display and no visualisation, the headset gave "a 16% increase in accuracy" and cut the time to complete the task by $62\%$, both against the next best system.
- **Flight paths.** Walker, Hedayati, Lee and Szafir (HRI 2018, Best Paper in Design) showed a drone's imminent path in AR, and participants were more efficient.
- **Assembly with a shared workspace.** Hietanen, Pieters, Lanz, Latokartano and Kämäräinen (*Robotics and Computer-Integrated Manufacturing* 63, 2020) monitored the workspace with a depth sensor and ran an interactive safety interface on a HoloLens and on a projector–mirror setup during a diesel-engine assembly task. Against a baseline without interaction or workspace sharing, both cut task time by $21$–$24\%$ and robot idle time by $57$–$64\%$. Subjectively, though, "HoloLens based AR is not yet suitable for industrial manufacturing", while the projector improved safety and ergonomics.
- **A team task with an industry partner.** Chan, Hanks, Sakr, Zhang, Zuo, Van der Loos and Croft (*ACM Transactions on Human-Robot Interaction* 11(3), 2022) evaluated a HoloLens interface for composite manufacturing with $26$ users. AR reduced physical demand and completion time and raised robot utilisation, while users felt a joystick was more dependable.

**The rule.** An intent display is a warning channel, not a safety function. The protective separation distance and its stop chain ([[04-robotics/hri-safety|11 §6]], [[05-construction-robotics/hrc-worker-centered|6 §6]]) must hold with the headset off, because a worker can take it off, look away, or be told the wrong thing by a stale ghost (§3). What XR can change is how early a person decides.

**The trap.** Every effect above is relative to a 2D screen or to nothing, measured in a laboratory (with $32$ and $26$ participants where the abstract gives a count), and three of the four on a HoloLens. None was measured on an active site, and the abstracts and pages read give no registration error beside the task results. Read "16% more accurate" as "on that task, at that distance, with that headset".

### 5. XR for commanding and teaching robots

*In one sentence:* a headset already tracks the head and hands in 6-DoF, so it doubles as an input device — to approve a plan in place, to teleoperate, or to collect demonstrations — and the page that owns the mapping from hand to robot is 12.

**The problem.** Programming a robot on site, correcting its plan, or recording the demonstrations a learned policy needs ([[05-construction-robotics/imitating-contact|10. Imitating Contact §1]]) all need a human's intent in 6-DoF, at a rate the robot can use.

**The idea.** Three uses, in order of how much the human does. **Approve**: the robot proposes and the human inspects the plan in place and accepts it. **Command**: the human moves and the robot follows, live. **Demonstrate without a robot**: the human performs the task and the headset records it for later learning, with AR feedback about what the robot could reproduce.

**What has been shown.**

- **Approve, in construction.** Kyjanek, Al Bahar, Vasey, Wannemacher and Menges (ISARC 2019) let a worker wearing a HoloLens plan robot trajectories, influence production sequencing and view superimposed diagnostic feedback in timber prefabrication, with a KUKA LBR iiwa on a mobile platform. Wang, Liang, Menassa and Kamat (ISARC 2020) built a process-level VR digital twin in which a human demonstrates a task plan, the robot plans its motion, and the plan comes back "for human evaluation and approval" before the robot executes it, on drywall installation over imperfect stud framing.
- **Command, with a consumer headset.** Zhang et al. (ICRA 2018) used consumer VR headsets and hand tracking to teleoperate a robot and trained visuomotor policies on the demonstrations. OPEN TEACH (Iyer et al., arXiv 2024) is built on the Meta Quest 3 and controls Franka, xArm, Jaco, Allegro and Hello Stretch robots "at up to 90Hz". It was shown on $38$ tasks; policies trained on its data reached an average success of $87\%$ on $10$ of them; and new users took $2.25$ times as long as experts, at a success rate the project page gives as $76\%$ "compared to experts". Open-TeleVision (Cheng et al., CoRL 2024) gives the operator active, stereoscopic vision of the robot's surroundings and mirrors arm and hand motion onto the robot; its code supports Apple Vision Pro and Meta Quest 3 through WebXR, and it trained policies on four long-horizon tasks for two humanoids.
- **Demonstrate without a robot.** ARCap (Chen, Wang, Nguyen, Fei-Fei and Liu, ICRA 2025) collects human demonstrations with AR visual feedback and haptic warnings when the virtual robot would violate its constraints, so that novices produce data the robot can execute.

**The rule on X1.** Getting the headset's poses into the robot's ROS 2 graph across a network is [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]'s problem, with its clocks. Q's hand skeleton arrives at $30\,\mathrm{Hz}$ by default, so a hand moving at $0.5\,\mathrm{m/s}$ travels $16.7\,\mathrm{mm}$ between samples; Fast Motion Mode's $60\,\mathrm{Hz}$ halves that to $8.3\,\mathrm{mm}$, at the price of jitter Meta warns about. A $90\,\mathrm{Hz}$ control loop therefore sees each hand sample for three ticks and must hold or interpolate it. Mapped one to one, $16.7\,\mathrm{mm}$ per sample cannot place S1's hole within $\pm5\,\mathrm{mm}$. With [[04-robotics/teleoperation-demonstration|12 §5]]'s motion scaling of $10$, the robot moves $1.67\,\mathrm{mm}$ per sample, which is why fine alignment by teleoperation scales the motion down.

**The traps.** Hand-tracked teleoperation records no force, so every item above collects position-only demonstrations — the gap between the vision interfaces and the haptic end of [[04-robotics/teleoperation-demonstration|12 §4]]'s spectrum. Wide Motion Mode's plausible poses must not be logged as measured ones (§2). And a demonstration interface's success rate depends on who used it: OPEN TEACH's novices took $2.25$ times as long as its experts.

### 6. Egocentric data from smart glasses for robot learning

*In one sentence:* glasses and headsets record what a person sees and does at a scale no robot fleet can match, and robot policies have started to learn from that data, but only where head and hand poses come with the video, logged by the device or estimated afterwards from its cameras and IMU, and never with the forces.

**The problem.** A learned policy needs many demonstrations, and robot demonstrations are slow and costly to collect ([[04-robotics/teleoperation-demonstration|12 §1]] treats teleoperation as the instrument that makes them). Humans do the tasks anyway. Can first-person recordings of people replace some robot data?

> [!info] Definition — egocentric data
> **Time-aligned recordings from sensors worn by the person doing the task**, as opposed to cameras watching them. Four conditions: the sensors are **worn**, so the viewpoint moves with the head ([[04-robotics/egocentric-perception|22 §3]]); the streams share **one clock**; the **action is recoverable**, which for robot learning means head and hand poses in 3D, not only pixels; and the people recorded — wearers and bystanders — **consented**.
> $$\mathcal E=\big\{\big(I_t,\ T_{WH}(t),\ h_t,\ g_t\big)\big\}_{t=1}^{N},\qquad a_t=\rho\big(h_t,\ T_{WH}(t)\big)$$
> where $I_t$ are images, $T_{WH}$ the head pose, $h_t$ the hand poses, $g_t$ the gaze where recorded, and $\rho$ the retargeting from a human hand to a robot's action ([[04-robotics/teleoperation-demonstration|12 §5]]).
> **Example.** EgoZero's Project Aria recordings: video with the head and hand poses that Meta's machine-perception services compute from the glasses' own cameras and IMUs, refined with a hand-pose model, from which robot-executable actions are extracted.
> **Non-example.** G's toolkit video: first-person, but at most $30$ frames per second over Bluetooth with no head or hand poses, so $a_t$ cannot be recovered from it without a separate pose estimator. Nor is a third-person video of the same task egocentric (22 §5's Ego-Exo4D records both on purpose).
> **Why it matters.** It scales, but it carries the embodiment gap: a human hand is not a gripper, and the forces of the task are not in the pictures.

**What has been shown.** The datasets that make first-person video a research object are the subject of [[04-robotics/egocentric-perception|22 §5]] (Ego4D, EPIC-KITCHENS, Ego-Exo4D). The robot-learning line that followed:

- **The device.** Project Aria (Engel et al., arXiv 2023) is Meta's research glasses: in Gen 1, two SLAM cameras, one RGB camera, two eye-tracking cameras, two IMUs, a magnetometer, a barometer, satellite positioning (GNSS) and seven microphones. Gen 2 (2025) has four SLAM cameras, a PPG heart-rate sensor and a contact microphone, runs SLAM, eye tracking and hand tracking on the device, weighs about $75\,\mathrm g$ and gives audio feedback.
- **Co-training.** EgoMimic (Kareer et al., ICRA 2025) captures human data with Aria glasses paired with 3D hand tracking, uses a low-cost bimanual arm chosen to narrow the kinematic gap, and co-trains one policy on human and robot data. Adding an hour of hand data was "significantly more valuable than 1 hour of additional robot data".
- **No robot data at all.** EgoZero (Liu et al., arXiv 2025) learns from Aria recordings with zero robot data and transfers to a Franka Panda with a gripper at $70\%$ success over seven tasks, with $20$ minutes of data per task — $140$ minutes in all.
- **Scale with hand poses.** EgoDex (Hoque et al., ICLR 2026) recorded $829$ hours of egocentric video with paired 3D hand and finger tracking on Apple Vision Pro, across $194$ tabletop tasks, about $4.3$ hours per task.
- **A Quest 3 in the loop.** HOT3D (Banerjee et al., CVPR 2025) recorded $833$ minutes of hand–object interaction with Project Aria and Quest 3, with ground truth from motion capture.
- **Many labs, one protocol.** EgoVerse (Punamiya et al., arXiv 2026) pools $1{,}362$ hours ($80{,}000$ episodes, $1{,}965$ tasks, $2{,}087$ demonstrators) and replicates human-to-robot transfer across labs. It finds that performance generally improves with more human data, but that "effective scaling depends on alignment between human data and robot learning objectives".

None of these recorded on Ray-Ban-class glasses. The data came from Aria, Vision Pro and Quest 3, which log head and hand poses, and in EgoVerse also from custom head-mounted rigs and head-strapped phones, for which its pipeline estimates the head pose by visual–inertial SLAM and the hands with a $21$-keypoint model, frame by frame. Ego-Pi (Kim et al., arXiv 2026), which teleoperated a humanoid with Quest controllers on data gloves — the controllers tracking the operator's wrists relative to the headset — and fine-tuned a $\pi_{0.5}$-based policy with egocentric human data, cites the two million Ray-Ban Meta glasses sold as a reason such data is becoming practical to collect at scale.

**The rule on X1.** The recording must carry the action. Aria Gen 2 and Vision Pro track head and hands on the device, Aria Gen 1's poses come from Meta's processing, and Q's runtime gives them live; G's toolkit records only video and audio, with no documented inertial stream to estimate a head pose from, and at its fallback of $15$ frames per second a hand moving at $0.5\,\mathrm{m/s}$ travels $33.3\,\mathrm{mm}$ between frames.

**The trap.** Every dataset above is household or tabletop, bare-handed, at human scale. S1's panel weighs $20\,\mathrm{kg}$, and the forces that seat it are exactly what glasses cannot see: the embodiment gap of [[03-deep-learning/vla/index|4. VLA §7]] plus a force gap, which [[05-construction-robotics/imitating-contact|10. Imitating Contact]] meets head-on. Egocentric recording of workers is also human-subjects research with bystanders in the frame ([[04-robotics/egocentric-perception|22 §6]]).

### 7. On a construction site

*In one sentence:* a site adds sunlight on additive displays, textureless and changing surroundings for tracking, dust, gloves, noise, hard hats and bystanders — and the one AR system that met a ±5 mm tolerance on a real building did it by tracking the object, not the head.

**The problem.** Everything above was measured indoors. Which parts survive a facade in sunlight?

**The field result to know.** Mitterberger, Dörfler, Sandy, Salveridou, Hutter, Gramazio and Kohler (*Construction Robotics* 4, 2020) built a fair-faced brick facade of $13{,}596$ bricks for a winery in Greece with "augmented bricklaying". An operator carried a handheld camera and IMU that tracked each brick itself, object-aware, and arrows on a shared screen guided the bricklayer until the brick's pose was within $4\,\mathrm{mm}$ of its target. A $2\,\mathrm{mm}$ threshold was tried and made bricklayers chase the arrows too long. The wall reached "± 5 mm local precision" and $\pm1\,\mathrm{cm}$ over each $5\times5\,\mathrm m$ facade element, because the tracking also registered the concrete frame and the vertical struts as a global reference, so errors did not accumulate from brick to brick. Three details matter for S1:

- **Headsets lost to a screen.** The team compared screens, tablets and a Magic Leap headset and, for its outdoor, bright site, found a screen "the most efficient visualization platform"; it names an insufficiently accurate alignment of the digital model with the physical world as a known limit of existing AR systems.
- **Sunlight broke detection.** Direct sun cast shadow lines that disturbed brick detection, and the fix was a black textile shade.
- **Accuracy cost time.** $3$ minutes per brick after the learning period, against the $1$ minute per brick that two bricklayers take for straight brickwork without rotation.

**Why that fits §3.** Tracking the part closes the loop on the object that must meet the tolerance, so the anchor and head-tracking terms drop out of the budget. X1's hologram, drawn in the headset's world, keeps them. For S1, a headset can reach $\pm5\,\mathrm{mm}$ only by measuring the panel and the bracket, the way the robot's wrist camera does ([[04-robotics/geometric-perception-calibration|3.5 §2.7]]).

**Site conditions, device by device.**

- **Hard hats and eye protection.** Microsoft states that HoloLens 2 has been tested and conforms to the basic impact protection requirements of ANSI Z87.1, CSA Z94.3 and EN 166, and describes the Trimble XR10 as a HoloLens 2 integrated into a hard hat, "purpose-built for workers in dirty, loud, and safety-controlled environments". Being a HoloLens 2, its production follows HoloLens 2's. RealWear lists the Navigator 520 as compatible with helmets and hearing protection, rated IP66 (dust-tight, and protected against powerful water jets) and $-20$ to $45^\circ\mathrm C$. The pages read for Q and G say nothing about hard hats or other PPE (personal protective equipment).
- **Sunlight on additive displays.** On OST, black is transparent and bright scenes wash content out. G has photochromatic lenses and auto-brightness; Trimble's HoloTint for HoloLens 2 "automatically adjusts its tint level based on UV rays and ambient light".
- **Tracking.** Inside-out tracking needs texture and light, and a facade under construction offers glass, repeated panels and changing geometry ([[04-robotics/state-estimation-slam|3 §7.2]] lists VIO's failures). G's location comes from the phone at $5$–$50\,\mathrm m$, $1{,}000$ to $10{,}000$ times S1's tolerance. A compass heading near steel should be tested before it is trusted.
- **Dust, gloves and noise.** Dust coats lenses and cameras as it does any rig ([[04-robotics/perception-sensors-rigs|3.6 §7]]); gloves change hand tracking's appearance model ([[04-robotics/egocentric-perception|22 §6]]); G's and Q's inputs assume a bare hand, a touchpad or a wristband.
- **Alerts.** A visual alert competes with the task, sound competes with tools, and vibration through gloves has its own physics ([[06-research-practice/psychophysics-human-measurement|8. Psychophysics §5]]). The worker-state rules of [[05-construction-robotics/hrc-worker-centered|6 §8]] apply to anything a headset infers.
- **Privacy.** A worn camera records co-workers who did not consent. Meta's AI glasses blink a capture LED "when content is being captured for your gallery", and covering it disables the camera. Project Aria has a recording LED and a privacy switch that deletes the current recording. Quest camera images are Device User Data under Meta's policy. None of this replaces a site protocol and ethics approval ([[04-robotics/egocentric-perception|22 §6]]).

**The trap.** A laboratory result on a HoloLens is not evidence for a site. The one site result above chose a screen over a headset, a tracked object over a registered hologram, and paid three times the time per brick.

### 8. Human factors

*In one sentence:* a headset costs its wearer comfort, field of view, weight, battery and attention, and only some of those costs have numbers.

**The problem.** A device that works for twenty minutes in a study must work for a shift. What does it cost the person wearing it?

**Cybersickness.** The review of Stauffert, Niebling and Latoschik (2020) collects the evidence. Latency raises cybersickness; occasional spikes provoke it as well as constant delay; people can detect latency below $17\,\mathrm{ms}$; and a much-quoted practitioner's advice is under $20\,\mathrm{ms}$. In a count the review cites, $58$ of $76$ experiments ($76\%$) measured sickness with the Simulator Sickness Questionnaire. The first of the explanations it lists is sensory mismatch: the eyes report motion the vestibular system does not. On X1 the prediction of §3 is also a comfort measure: it keeps the rendered world steady while the head turns. A VST headset adds a mismatch no prediction removes, because the robot's own motion reaches the eye inside the camera images $\tau_{\mathrm{pt}}=40\,\mathrm{ms}$ late, behind what the worker hears and, at the hold, feels through the panel.

**Field of view.** Q replaces the whole view with displays of $110^\circ\times96^\circ$, so everything outside that is gone, including a robot approaching from the side. To see it the worker must turn the head, and head turns are exactly the moments at which §3's budget is worst. G leaves the natural view intact and adds a $14.3^\circ$ panel off to one side.

**Weight and battery, against an eight-hour shift.** Q weighs $515\,\mathrm g$ and lasts $2.2\,\mathrm h$ on average ($1.5\,\mathrm h$ for productivity use), so a shift is $3.6$ charges, or $5.3$ at the productivity figure. G weighs $69\,\mathrm g$, $7.5$ times less, and lasts up to $6\,\mathrm h$ of mixed use, $1.3$ charges. HoloLens 2 weighs $566\,\mathrm g$ for $2$–$3\,\mathrm h$, and Apple Vision Pro $750$–$800\,\mathrm g$ for $2.5\,\mathrm h$. RealWear makes its battery hot-swappable.

**Attention and trust.** A head-locked panel costs a glance; world-locked content costs a focus shift and, when wrong, the trust of §4's users, who found a joystick more dependable. The subjective verdict on HoloLens in industrial assembly (§4) and the site team's choice of a screen (§7) point the same way. These costs are stated qualitatively here because no study above measured them over a shift.

### 9. The research landscape

*In one sentence:* the field runs in five streams — intent communication, AR/VR interfaces for commanding and teaching, egocentric data for robot learning, XR on construction sites, and human factors and safety — and almost all of its evidence sits on the laboratory rung.

**How to read the map.** Each row gives authors, venue and year, what was demonstrated, and the evidence rung of [[05-construction-robotics/site-engineering|2.5 §5]] — simulation, laboratory, full-scale mock-up, active site — whose licences [[06-research-practice/real-world-impact|6. Real-World Impact §2]] states. Every work was opened at its publisher, arXiv or project page (Sources).

| stream | work | venue, year | demonstrated | rung |
|---|---|---|---|---|
| intent | Rosen, Whitney, Phillips, Chien, Tompkin, Konidaris, Tellex | ISRR 2017; IJRR 2019 | MR-headset arm-motion preview: +16% accuracy, −62% time, $n=32$ | laboratory |
| intent | Walker, Hedayati, Lee, Szafir | HRI 2018 | AR drone flight paths made users more efficient | laboratory |
| intent | Hietanen, Pieters, Lanz, Latokartano, Kämäräinen | *RCIM* 63, 2020 | HoloLens and projector UIs: −21–24% task time, −57–64% robot idle; HoloLens judged unsuitable | laboratory, industrial task |
| intent | Chan, Hanks, Sakr, Zhang, Zuo, Van der Loos, Croft | *ACM THRI* 11(3), 2022 | AR vs joystick with $n=26$: less physical demand, shorter time, more robot use | laboratory, industry task |
| command, teach | Zhang et al. | ICRA 2018 | VR teleoperation to deep imitation learning | laboratory |
| command, teach | Iyer et al. (OPEN TEACH) | arXiv 2024 | Quest 3 teleoperation at up to 90 Hz, 38 tasks, policies at 87% on 10 | laboratory |
| command, teach | Cheng et al. (Open-TeleVision) | CoRL 2024 | immersive teleoperation with active stereo vision; Vision Pro and Quest 3 | laboratory |
| command, teach | Chen, Wang, Nguyen, Fei-Fei, Liu (ARCap) | ICRA 2025 | robot-free demonstrations with AR and haptic feedback | laboratory |
| egocentric | Kareer et al. (EgoMimic) | ICRA 2025 | Aria human data co-trained with robot data | laboratory |
| egocentric | Liu et al. (EgoZero) | arXiv 2025 | zero robot data, 70% over 7 tasks | laboratory |
| egocentric | Hoque et al. (EgoDex) | ICLR 2026 | 829 h of Vision Pro video with hand poses | dataset |
| egocentric | Punamiya et al. (EgoVerse) | arXiv 2026 | 1,362 h, transfer replicated across labs | laboratory, many labs |
| construction | Mitterberger et al. | *Construction Robotics* 4, 2020 | object-aware AR bricklaying: ±5 mm local, 13,596 bricks | active site |
| construction | Kyjanek, Al Bahar, Vasey, Wannemacher, Menges | ISARC 2019 | HoloLens planning of robot trajectories in timber prefabrication | laboratory |
| construction | Wang, Liang, Menassa, Kamat | ISARC 2020 | VR digital twin: plan, approve, execute, drywall | laboratory |
| construction | Park, Menassa, Kamat | *J. Comput. Civ. Eng.* 39(1), 2025 | VR interface with a large-language-model chat, 12 construction workers | simulation (VR) |
| human factors | Stauffert, Niebling, Latoschik | *Front. Virtual Real.* 1, 2020 | latency and cybersickness: spikes matter; SSQ in 76% | review |
| human factors | OptoFidelity | benchmark, 2024 | passthrough 11 ms (Vision Pro) vs 35–40 ms (Quest 3) | bench measurement |

**Where this community publishes.** The ACM/IEEE Human-Robot Interaction conference and its workshop on Virtual, Augmented, and Mixed-Reality for Human-Robot Interactions (VAM-HRI), whose ninth edition met at HRI 2026 and which has run every year since 2018. IEEE ISMAR, whose 25th edition meets in Bari on 5–9 October 2026, and IEEE VR, whose 33rd edition, in 2026, was the first hosted in Korea, in Daegu. The HCI conference CHI and the journal *ACM Transactions on Human-Robot Interaction* (THRI), where the two surveys below and one intent study appeared, and the robot-learning venues where the teleoperation and egocentric work appears (ICRA, CoRL, ICLR, CVPR). The Joint Egocentric Vision (EgoVis) workshop, held at CVPR since 2024. For construction, ISARC, whose 43rd edition met in Singapore on 22–26 June 2026, and the journals *Construction Robotics* and the *Journal of Computing in Civil Engineering*. Two surveys map the field: Suzuki, Karim, Xia, Hedayati and Marquardt (CHI 2022) classify $460$ papers on AR and robotics, and Walker, Phung, Chakraborti, Williams and Szafir (*ACM THRI* 12(4), 2023) propose a taxonomy of virtual design elements for VAM-HRI. Before sending a paper to a workshop, read [[06-research-practice/venue-strategy|5. Venue Strategy §6]].

**Open problems a dissertation could take on.** These are this page's reading of the map above, not a verified survey of absences.

- **Registration at construction tolerance.** None of the abstracts and pages read reports a hologram's registration error beside its task result, and the one ±5 mm site result tracked the object. Can a headset measure S1's panel and bracket itself, on site, and close the budget of §3 without the anchor term?
- **Intent display beside a moving construction robot.** The intent studies of §4 were laboratory studies with arm robots and drones. A study on S1's lane or hold would measure detection and response time under dust, gloves and noise, with the safety function unchanged (§4's rule).
- **VST beside machinery.** A worker on Q sees a moving robot $40\,\mathrm{ms}$ late (course number) through passthrough. No work on this map measures what that does to a person's timing near a moving base.
- **Egocentric demonstrations with loads and PPE.** Every egocentric dataset above is bare-handed tabletop work. Gloved, heavy, two-person tasks such as S1 would need force as well as head and hand poses.
- **A low-burden channel for the hold.** G cannot register, but it can carry the next step and the robot's state with a $69\,\mathrm g$ device. Measuring glance time and response time against audio and vibration on a site is a human-factors study the owner's devices can run.

### 10. The lab

The listing runs the budget of §3 on X1, sweeps it over distance, head speed and latency, steps a head turn at $1\,\mathrm{kHz}$ with and without prediction, and prints what each featured device shows. It is deterministic and uses NumPy only.

```python
# 23.5 lab: X1's registration budget on S1, a head turn with and without prediction,
# and what each featured device can show. NumPy only; the numbers are X1's course numbers.
import numpy as np

RAD = np.pi / 180.0
# --- X1, frozen in the Running object (course numbers, not product specifications) ----------
D = 1.5                          # eye to the target hole (m)
P_H, TH_H = 2.0, 0.05            # head tracking: position error (mm), orientation error (deg)
P_A, TH_A, L = 2.0, 0.10, 1.2    # anchor: position (mm), rotation (deg), marker-to-hole lever (m)
TAU_EFF, TAU_RAW = 0.005, 0.020  # motion-to-photon after / without prediction (s)
TOL, BAND = 5.0, 50.0            # S1's +-5 mm, and a coarse 50 mm guidance band
SPEEDS = (0.0, 30.0, 90.0, 300.0)  # head speed (deg/s): still, following, walking, look-around

def static_terms(d):
    """The four static sources as displacements at the hole (mm) for an eye d metres away."""
    return np.array((P_H, d * 1e3 * TH_H * RAD, P_A, L * 1e3 * TH_A * RAD))

def totals(d, w, tau):
    """Latency term, linear total and RSS-of-static-plus-latency, all in mm."""
    s = static_terms(d)
    lat = d * 1e3 * w * RAD * tau
    return lat, s.sum() + lat, float(np.sqrt((s**2).sum())) + lat

def verdict(e):
    return "within 5" if e <= TOL else ("within 50" if e <= BAND else "outside 50")

s = static_terms(D)
print("Part 1. X1 at D = %.1f m: head %.2f + %.2f mm, anchor %.2f + %.2f mm" % (D, *s))
print("  still: linear %.2f mm, RSS %.2f mm" % (s.sum(), np.sqrt((s**2).sum())))
for tau in (TAU_EFF, TAU_RAW):
    for w in SPEEDS[1:]:
        lat, lin, rss = totals(D, w, tau)
        print("  %2.0f ms, %3.0f deg/s: latency %6.2f | linear %6.2f (%s) | RSS+latency %6.2f (%s)"
              % (tau * 1e3, w, lat, lin, verdict(lin), rss, verdict(rss)))

print("Part 2. fastest head turn (deg/s) that keeps the hologram in the band; linear, then RSS")
for d in (0.5, 1.0, 1.5, 2.0, 3.0):
    st = static_terms(d)
    row = []
    for band in (TOL, BAND):
        for tau in (TAU_EFF, TAU_RAW):
            for base in (st.sum(), np.sqrt((st**2).sum())):
                w = (band - base) / (d * 1e3 * tau) / RAD
                row.append("never" if w < 0 else "%4.0f" % w)
    print("  D %.1f m | 5 mm: %s %s at 5 ms, %s %s at 20 ms | 50 mm: %s %s at 5 ms, %s %s at 20 ms" % (d, *row))

# --- Part 3: a head turn stepped at the IMU's 1 kHz -----------------------------------------
dt, T, TH_F = 1e-3, 0.5, 60.0      # sample period (s); a rest-to-rest turn of 60 deg in 0.5 s
t = np.arange(0.0, 0.8 + dt / 2, dt)

def angle(tt):                      # the quintic rest-to-rest profile of MR ch.9 (deg)
    u = np.clip(tt / T, 0.0, 1.0)
    return TH_F * (10 * u**3 - 15 * u**4 + 6 * u**5)

def rate(tt):                       # its angular speed (deg/s)
    u = np.clip(tt / T, 0.0, 1.0)
    return TH_F / T * 30 * u**2 * (1 - u)**2

def peak_errors(tau):
    k = int(round(tau / dt))        # the pose used for a frame is tau old
    th = angle(t)
    none = th[k:] - th[:-k]                            # draw with the old pose
    cv = th[k:] - (th[:-k] + rate(t[:-k]) * tau)       # extrapolate it at its measured rate
    return none, cv

print("Part 3. %.0f deg in %.1f s: peak speed %.0f deg/s, peak acceleration %.0f deg/s^2"
      % (TH_F, T, rate(t).max(), np.abs(np.gradient(rate(t), dt)).max()))
for tau in (TAU_RAW, 0.040):
    none, cv = peak_errors(tau)
    print("  tau %2.0f ms | no prediction: lags %.3f deg = %5.1f mm | constant-rate: lags %.3f deg = %4.1f mm,"
          " leads %.3f deg = %4.1f mm"
          % (tau * 1e3, none.max(), D * 1e3 * np.tan(none.max() * RAD), cv.max(),
             D * 1e3 * np.tan(cv.max() * RAD), -cv.min(), D * 1e3 * np.tan(-cv.min() * RAD)))

# --- Part 4: the two featured devices on S1, and the sensor rates -----------------------------
TAU_PT, TAU_NET = 0.040, 0.050     # Q's passthrough latency; robot state reaching the headset (s)
print("Part 4. the two featured devices on S1")
for v in (0.05, 0.5):
    print("  panel at %.2f m/s: seen %.1f mm late through Q's passthrough; the robot ghost %.1f mm behind"
          % (v, v * TAU_PT * 1e3, v * TAU_NET * 1e3))
PX, PPD = 600, 42.0                # G's panel (px) and pixel density (px/deg), Meta's figures
fov = PX / PPD
print("  G's panel: %.1f deg across, %.1f deg diagonal, %.3f m wide at D"
      % (fov, PX * np.sqrt(2) / PPD, 2 * D * np.tan(fov / 2 * RAD)))
for step in (0.1, 0.3):
    print("  G has no head position: a %.1f m step turns the hole's true bearing by %.1f deg"
          % (step, np.degrees(np.arctan2(step, D))))
print("  Q's passthrough pixel (18 px/deg) is %.2f mm at D; a display pixel (25 px/deg) %.2f mm"
      % (D * 1e3 * np.tan(RAD / 18), D * 1e3 * np.tan(RAD / 25)))
for f in (15, 30, 60):
    print("  a hand at 0.5 m/s moves %.1f mm between samples at %d Hz" % (500.0 / f, f))
NG, BG = 1.0e-4, 1.5e-4            # 3.2's gyro: noise density (rad/s/sqrt(Hz)), bias (rad/s)
for w in (90.0, 300.0):
    print("  head at %3.0f deg/s: %.2f deg per 30 Hz camera frame, %.2f deg per 1 kHz IMU sample"
          % (w, w / 30, w / 1000))
for span in (1 / 30, 10.0):
    drift = np.degrees(NG * np.sqrt(span) + BG * span)
    print("  gyro alone for %6.3f s: %.4f deg, %.2f mm at D" % (span, drift, D * 1e3 * np.tan(drift * RAD)))
```

**What it prints.** Part 1, the budget at $D=1.5\,\mathrm m$ (mm):

| latency | head speed | latency term | linear total | RSS of static + latency |
|---|---:|---:|---:|---:|
| — | still | 0.00 | 7.40 | 3.75 |
| 5 ms | 30 °/s | 3.93 | 11.33 | 7.68 |
| 5 ms | 90 °/s | 11.78 | 19.18 | 15.54 |
| 5 ms | 300 °/s | 39.27 | 46.67 | 43.02 |
| 20 ms | 30 °/s | 15.71 | 23.11 | 19.46 |
| 20 ms | 90 °/s | 47.12 | 54.53 | 50.88 |
| 20 ms | 300 °/s | 157.08 | 164.48 | 160.83 |

Part 2, the fastest head turn (°/s) that keeps the hologram inside each band, linear reading / RSS reading:

| $D$ | ±5 mm, 5 ms | ±5 mm, 20 ms | 50 mm, 5 ms | 50 mm, 20 ms |
|---|---:|---:|---:|---:|
| 0.5 m | never / 33 | never / 8 | 996 / 1065 | 249 / 266 |
| 1.0 m | never / 16 | never / 4 | 493 / 531 | 123 / 133 |
| 1.5 m | never / 10 | never / 2 | 325 / 353 | 81 / 88 |
| 2.0 m | never / 6 | never / 2 | 242 / 264 | 60 / 66 |
| 3.0 m | never / 2 | never / 1 | 158 / 174 | 39 / 44 |

Part 3, a $60^\circ$ turn in $0.5\,\mathrm s$ on the quintic profile of [[04-robotics/modern-robotics/ch09-trajectory-generation|MR ch.9 §1]] (peak $225$ °/s, peak $1386$ °/s²): with $\tau=20\,\mathrm{ms}$, drawing the old pose lags by $4.495^\circ$, $117.9\,\mathrm{mm}$ at $D$. Constant-rate prediction lags by $0.277^\circ$, $7.2\,\mathrm{mm}$, while the head speeds up, and leads by the same while it slows down. At $\tau=40\,\mathrm{ms}$ the two become $236.5$ and $28.8\,\mathrm{mm}$. Part 4 prints the device numbers that §2, §3 and the Worked case quote, and $3.8^\circ$ for a $0.1\,\mathrm m$ step.

**What to take from it.**

- **Only a still head and a kind rule give ±5 mm.** The linear reading never reaches it at any distance; the RSS reading tolerates at most $33$ °/s, and only at $0.5\,\mathrm m$.
- **Prediction buys the coarse band.** At $1.5\,\mathrm m$ it lifts the $50\,\mathrm{mm}$ limit from $81$ to $325$ °/s.
- **Distance costs twice.** $D$ multiplies both the head-orientation term and the latency term, so stepping back from $1.0$ to $2.0\,\mathrm m$ halves the head speed the band allows.
- **Prediction fails at the ends of a turn.** The residual follows the acceleration, so the hologram swims behind as the head speeds up and ahead as it slows. Doubling the latency quadruples it, $7.2$ to $28.8\,\mathrm{mm}$.

### After reading

You should be able to:

- place a device in one of the six classes of §1 from how the real world reaches the eye and what it tracks, and say what that class can and cannot show;
- list, for Q and G, what a developer can read (head, hands, eyes, camera, depth, sound) and under which permission and rule;
- explain why an HMD's IMU runs at hundreds of hertz while its cameras run at tens;
- write the registration budget of a hologram at a named point, with each rotation's lever, and say why latency is added linearly;
- align a headset's world to a robot base with a marker and PnP, and name the three cautions;
- say, with numbers, what world-locked AR can and cannot guide on S1, and what a head-locked panel can do instead;
- summarise, for each of the five research streams, two works, their venue, what they showed and on which evidence rung.

### Self-check

1. A paper reports "an AR interface that improved accuracy by 16%". Which two facts about the device do you need before you can compare it with G?
2. X1's hologram is $7.40\,\mathrm{mm}$ off with the head still. Which single change halves the anchor's contribution to that, and what does it cost?
3. Why does a VST headset show a moving robot late even when the worker's head is perfectly still?
4. G can stream video to a phone. Why is that stream not yet a robot demonstration?
5. Constant-rate prediction leaves $7.2\,\mathrm{mm}$ at the start of a turn. Why is it zero during the middle of a steady turn?

> [!tip]- Answers
> 1. Whether the real world reaches the eye directly or through cameras (OST or VST), and whether the content was world-locked or head-locked — plus the distance and head speed at which accuracy was measured. G is OST and head-locked, so a world-locked result says nothing about it.
> 2. Moving the anchor closer to the hole. The rotation term is $L\,\delta\theta_A$: halving $L$ from $1.2$ to $0.6\,\mathrm m$ takes it from $2.09$ to $1.05\,\mathrm{mm}$. The cost is a marker near the work, where a smaller marker's weaker tilt estimate (3.5 §2.7) may raise $\delta\theta_A$, as the problem set shows.
> 3. Because the whole view is video, and every camera frame reaches the display $\tau_{\mathrm{pt}}$ after the moment it shows. The robot moves during that time: $0.5\,\mathrm{m/s}\times40\,\mathrm{ms}=20\,\mathrm{mm}$. Head prediction cannot remove it, because the lag belongs to the scene, not the head.
> 4. It has no head or hand poses, so the action cannot be recovered and retargeted ($a_t=\rho(h_t,T_{WH})$ needs both); it arrives compressed at up to $30$ frames per second; and it carries no force. It is first-person video, which becomes egocentric training data only with a pose estimator and a consent protocol.
> 5. The residual of constant-rate extrapolation is about $\tfrac12\dot\omega\tau^2$. In a steady turn $\dot\omega=0$, so extrapolating the current rate lands exactly on the true angle; the error appears only while the rate changes, at the start and end of the turn. X1 still charges $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$ at every head speed because a real head's rate keeps changing and the rate being extrapolated is itself a noisy estimate (§3).

### Problem set · 과제

Tier A. Using only this page, its prerequisites and X1. The worker steps back to watch the whole panel, so the eyes are **2.5 m** from T. The anchor is remade on a small marker on the bracket, **0.3 m** from T, with position error **1.5 mm** and, because the marker is small, rotation error **0.30°**. Head tracking is unchanged. The application is heavier, leaving **8 ms** after prediction; without prediction it is still $20\,\mathrm{ms}$. Call this **X1′**.

1. **Draw.** Redraw both panels of the picture for X1′: the plan with the new $D$ and the anchor on the bracket, G's $14.3^\circ$ panel to scale at the new distance, and the budget bars at $30$ and $90$ °/s with $8\,\mathrm{ms}$ and at $90$ °/s with $20\,\mathrm{ms}$, against $\pm5$ and $50\,\mathrm{mm}$.
2. **Derive.** For X1′: (a) the four static terms, and the linear and RSS totals; (b) the latency term and the linear total at $30$ and $90$ °/s with $8\,\mathrm{ms}$; (c) the fastest head turn that keeps the linear total inside $50\,\mathrm{mm}$, at $8$ and at $20\,\mathrm{ms}$; (d) the width of G's panel square-on at $2.5\,\mathrm m$, and the bearing shift from a $0.3\,\mathrm m$ step; (e) whether the new anchor helped, term by term.
3. **Do.** Fill the blanks, run it, and compare with the Solutions. Then say how the constant-rate and constant-acceleration residuals scale when the latency doubles, and what that implies for a pipeline that must predict $40\,\mathrm{ms}$ ahead.

```python
# Do: X1' and a constant-acceleration predictor. Fill every ?, then compare with the Solutions.
import numpy as np
RAD = np.pi / 180.0
D, TAU = 2.5, 0.008                    # X1': eyes 2.5 m from T, 8 ms left after prediction
P_H, TH_H = 2.0, 0.05                  # head tracking, as in X1
P_A, TH_A, L = 1.5, 0.30, 0.3          # the anchor, remade on a bracket marker 0.3 m from T
static = np.array((P_H, D * 1e3 * TH_H * RAD, P_A, ?))       # the anchor's rotation term (mm)
for w in (30.0, 90.0):
    lat = ?                                                  # the latency term at w deg/s (mm)
    print("w %3.0f deg/s: linear %.2f mm, RSS+latency %.2f mm"
          % (w, static.sum() + lat, np.sqrt((static**2).sum()) + lat))
print("fastest turn inside 50 mm: %.1f deg/s" % ((50.0 - static.sum()) / (D * 1e3 * TAU) / RAD))

dt, T, TH_F = 1e-3, 0.5, 60.0                  # the same quintic turn as Part 3
t = np.arange(0.0, 0.8 + dt / 2, dt)
u = np.clip(t / T, 0.0, 1.0)
th = TH_F * (10 * u**3 - 15 * u**4 + 6 * u**5)  # angle (deg)
om = TH_F / T * 30 * u**2 * (1 - u)**2          # rate (deg/s)
acc = ?                                         # angular acceleration from om (deg/s^2)
for tau in (0.020, 0.040):
    k = int(round(tau / dt))
    cv = th[k:] - (th[:-k] + om[:-k] * tau)
    ca = th[k:] - (th[:-k] + om[:-k] * tau + ?)  # add the acceleration term
    print("tau %2.0f ms: constant-rate %.4f deg, constant-acceleration %.4f deg"
          % (tau * 1e3, np.abs(cv).max(), np.abs(ca).max()))
```

> [!note]- How to draw it · 그리는 법
> - **The plan to scale**: the wall, the panel with its two holes $400\,\mathrm{mm}$ apart, T, the eyes H at the stated distance, and the marker where the anchor now is, with $D$ and $L$ written on their lines.
> - **The three frames**: W where tracking started, H on the head, B on the robot, with the anchor $T_{WB}$ and the head pose $T_{WH}$ drawn as links from W.
> - **Both devices' views from H**: Q's $110^\circ$ wedge and G's $14.3^\circ$ wedge, the latter carried to the wall so that the span it covers can be read off.
> - **The budget as stacked bars at T**, one row per head speed and latency, each bar split into head position, head orientation, anchor position, anchor rotation and latency, drawn at one scale.
> - **Two vertical lines**: S1's $\pm5\,\mathrm{mm}$ and the $50\,\mathrm{mm}$ band, so that each bar's verdict is read, not computed.
> - **The totals in a column** at the right, so that no label crosses a line.

> [!tip]- Solutions
> 1. The plan shows H $2.5\,\mathrm m$ from T and the marker on the bracket $0.3\,\mathrm m$ from it, so the anchor's lever is a quarter of X1's. G's wedge now spans $0.627\,\mathrm m$ square-on. The static part of every bar shrinks slightly, $7.25$ against $7.40\,\mathrm{mm}$, because the head term grew and the anchor term shrank; the latency parts grow by $2.5/1.5\times8/5=2.67$ times at equal head speed.
> 2. (a) Head position $2.00$, head orientation $2500\times0.05\times\pi/180=2.18$, anchor position $1.50$, anchor rotation $300\times0.30\times\pi/180=1.57\,\mathrm{mm}$; linear $7.25$, RSS $3.67\,\mathrm{mm}$. (b) $D\,\omega\,\tau=2500\times0.524\times0.008=10.47\,\mathrm{mm}$ at $30$ °/s ($0.524\,\mathrm{rad/s}$), total $17.72\,\mathrm{mm}$; $31.42\,\mathrm{mm}$ at $90$ °/s, total $38.67\,\mathrm{mm}$ — both inside $50$, both far outside $\pm5$. (c) $(50-7.25)/(2500\times0.008)=2.14\,\mathrm{rad/s}=122.5$ °/s at $8\,\mathrm{ms}$, and $49.0$ °/s at $20\,\mathrm{ms}$, less than walking. (d) $2\times2.5\times\tan7.14^\circ=0.627\,\mathrm m$; $\arctan(0.3/2.5)=6.84^\circ$, smaller than X1's $11.3^\circ$ because the same step is a smaller angle from further away — still far too large to mark a hole. (e) The anchor's rotation term fell from $2.09$ to $1.57\,\mathrm{mm}$ although its angle tripled, because the lever fell to a quarter; its position term fell by $0.5\,\mathrm{mm}$. The head-orientation term rose from $1.31$ to $2.18\,\mathrm{mm}$ with the distance.
> 3. The blanks: `L * 1e3 * TH_A * RAD`; `D * 1e3 * w * RAD * TAU`; `np.gradient(om, dt)`; `0.5 * acc[:-k] * tau**2`. The printout: linear $17.72$ and $38.67\,\mathrm{mm}$, RSS plus latency $14.14$ and $35.09\,\mathrm{mm}$; fastest turn $122.5$ °/s. At $20\,\mathrm{ms}$ the constant-rate residual is $0.2767^\circ$ and the constant-acceleration residual $0.0357^\circ$ ($7.2$ and $0.93\,\mathrm{mm}$ at $1.5\,\mathrm m$); at $40\,\mathrm{ms}$, $1.1015^\circ$ and $0.2680^\circ$. Doubling the latency multiplies the constant-rate residual by $4.0$, as $\tau^2$, and the constant-acceleration one by $7.5$, near $\tau^3$'s $8$. Predicting $40\,\mathrm{ms}$ ahead therefore needs the acceleration term, which comes from differentiating a noisy gyro — noise absent here, and the price of the higher order.

### Sources

Every page below was opened on 2026-09-23; product facts change, so re-read the maker's page before reusing a number.

**Definitions and standards**

- R. Skarbez, M. Smith, M. C. Whitton, "Revisiting Milgram and Kishino's Reality-Virtuality Continuum," *Frontiers in Virtual Reality* 2:647997, 2021. [frontiersin.org](https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2021.647997/full) — quotes Milgram and Kishino (*IEICE Trans. Inf. & Syst.* E77-D, 1994) and Milgram et al. (*Proc. SPIE* 2351), whose own pages sit behind bot checks and were not opened.
- W3C, *WebXR Device API*, Candidate Recommendation Draft, 9 June 2026. [w3.org](https://www.w3.org/TR/webxr/) — "XR" as a spectrum.
- The Khronos Group, *The OpenXR Specification*. [registry.khronos.org](https://registry.khronos.org/OpenXR/specs/1.0/html/xrspec.html) — XR as a continuum; [XrViewLocateInfo](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XrViewLocateInfo.html) and [XrFrameState](https://registry.khronos.org/OpenXR/specs/1.0/man/html/XrFrameState.html) — the two quoted sentences on predicted display time. [OpenXR overview](https://www.khronos.org/openxr/) — conformant runtimes.

**The featured devices (Meta's pages)**

- Meta Quest 3 tech specs, [meta.com](https://www.meta.com/quest/quest-3/) and [the comparison page](https://www.meta.com/quest/compare/) — display, pixels per degree, 4 MP passthrough at 18 PPD, field of view, refresh rates, the 2.2 h battery; the weight, camera and eye-tracking rows load by script and were checked only through search results.
- Meta, "Build the Next Generation of VR & MR with Meta Quest 3," 1 June 2023. [developers.meta.com](https://developers.meta.com/horizon/blog/build-the-next-generation-of-vr-mr-with-meta-quest-3/) — dual 4 MP RGB cameras and a depth sensor.
- Meta, Passthrough Camera API overview (updated 21 April 2026) [developers.meta.com](https://developers.meta.com/horizon/documentation/spatial-sdk/spatial-sdk-pca-overview/) and Getting Started with Passthrough Camera API in Unity (9 December 2025) [developers.meta.com](https://developers.meta.com/horizon/documentation/unity/unity-pca-documentation/) — cameras, resolutions, 60 Hz, 20–40 ms, intrinsics, extrinsics, timestamps, camera pose, permissions, data policy.
- Meta, Hands Technology (17 August 2026) [developers.meta.com](https://developers.meta.com/horizon/design/hands-technology/), Hand Tracking Overview in Unity (14 September 2026) [developers.meta.com](https://developers.meta.com/horizon/documentation/unity/unity-handtracking-overview/) and Enable Hand Tracking [developers.meta.com](https://developers.meta.com/horizon/documentation/native/android/mobile-hand-tracking/) — 30 and 60 Hz modes, Wide Motion Mode, the data-usage rule.
- Meta, Depth API Overview (29 April 2026) [developers.meta.com](https://developers.meta.com/horizon/documentation/unity/unity-depthapi-overview/) and Spatial Anchors Best Practices (2 August 2024) [developers.meta.com](https://developers.meta.com/horizon/documentation/unity/unity-spatial-anchors-best-practices/).
- Meta, "Meta Ray-Ban Display: Breakthrough AI Glasses Available Now," 17 and 30 September 2025. [meta.com](https://www.meta.com/blog/meta-ray-ban-display-ai-glasses-connect-2025/) — monocular geometric waveguide, 42 pixels per degree, 2% light leakage, 69 g, six hours.
- Meta Newsroom, "Meta Ray-Ban Display: AI Glasses With an EMG Wristband," 17 September 2025. [about.fb.com](https://about.fb.com/news/2025/09/meta-ray-ban-display-ai-glasses-emg-wristband/); product page [meta.com](https://www.meta.com/ai-glasses/meta-ray-ban-display/) — 12 MP camera, right-lens display.
- Meta Wearables Developer Center: [Device Access Toolkit](https://wearables.developer.meta.com/docs/develop/dat/), [Integration overview](https://wearables.developer.meta.com/docs/develop/dat/build-overview/) (16 September 2026), [Display access overview](https://wearables.developer.meta.com/docs/develop/dat/display-overview/) (19 September 2026), [Android integration](https://wearables.developer.meta.com/docs/develop/dat/build-integration-android/) (18 September 2026), [Version dependencies](https://wearables.developer.meta.com/docs/develop/dat/version-dependencies/) (23 September 2026), [Web Apps](https://wearables.developer.meta.com/docs/develop/webapps/) and [Build](https://wearables.developer.meta.com/docs/develop/webapps/build/) (19 September 2026).
- Meta Newsroom, Ray-Ban Meta (Gen 2), September 2025 [about.fb.com](https://about.fb.com/news/2025/09/ray-ban-meta-gen-2-better-battery-life-video-capture/), and "Meta's AI Glasses: Your Questions Answered," July 2026 [about.fb.com](https://about.fb.com/news/2026/07/metas-ai-glasses-your-questions-answered/) — the capture LED.

**Other devices (makers' pages)**

- Apple, Apple Vision Pro technical specifications. [apple.com](https://www.apple.com/apple-vision-pro/specs/)
- Microsoft Learn: [HoloLens 2 hardware](https://learn.microsoft.com/en-us/hololens/hololens2-hardware), [HoloLens 2 release notes](https://learn.microsoft.com/en-us/hololens/hololens-release-notes) (production ended December 2024), [Trimble XR10 with HoloLens 2](https://learn.microsoft.com/en-us/hololens/hololens2-options-trimble-xr10-edition).
- Magic Leap, [Terms of Sale](https://www.magicleap.com/legal/terms-of-sale) (revised 19 February 2026) and [Global/Segmented Dimmer](https://developer-docs.magicleap.cloud/docs/guides/features/dimmer-feature/).
- RealWear, [Navigator 520 specifications](https://shop.realwear.com/pages/realwear-navigator-520-specifications) and [press release, 3 January 2023](https://www.realwear.com/press-releases/realwear-unveils-next-generation-assisted-reality-headset-for-modern-frontline-professional-with-all-new-hyperdisplay).
- Project Aria: [glasses](https://www.projectaria.com/glasses/) and Meta's blog, [Introducing Aria Gen 2](https://www.meta.com/blog/project-aria-gen-2-next-generation-egocentric-research-glasses-reality-labs-ai-robotics/).

**Measurements and human factors**

- OptoFidelity, [See-Through Latency, Photon-to-Photon](https://www.optofidelity.com/insights/blogs/apple-vision-pro-benchmark-test-1-see-through-latency-photon-to-photon) (14 February 2024) and [Angular Motion-to-Photon Latency](https://www.optofidelity.com/insights/blogs/apple-vision-pro-bencmark-test-2.-angular-motion-to-photon-latency-in-vr) (15 February 2024).
- J.-P. Stauffert, F. Niebling, M. E. Latoschik, "Latency and Cybersickness: Impact, Causes, and Measures. A Review," *Frontiers in Virtual Reality* 1:582204, 2020. [frontiersin.org](https://www.frontiersin.org/journals/virtual-reality/articles/10.3389/frvir.2020.582204/full)

**Intent communication**

- E. Rosen, D. Whitney, E. Phillips, G. Chien, J. Tompkin, G. Konidaris, S. Tellex, "Communicating Robot Arm Motion Intent Through Mixed Reality Head-mounted Displays," ISRR 2017. [arXiv:1708.03655](https://arxiv.org/abs/1708.03655); extended in *IJRR* 38(12–13), 2019, [doi:10.1177/0278364919842925](https://doi.org/10.1177/0278364919842925), whose abstract names the HoloLens; venues from the [first author's page](https://cs.brown.edu/people/er35/publications.html).
- M. Walker, H. Hedayati, J. Lee, D. Szafir, "Communicating Robot Motion Intent with Augmented Reality," HRI 2018, [doi:10.1145/3171221.3171253](https://doi.org/10.1145/3171221.3171253) — read on the [authors' institute page](https://www.colorado.edu/atlas/2018/03/15/augmented-reality-enhances-robot-collaboration); the ACM page sits behind a bot check.
- A. Hietanen, R. Pieters, M. Lanz, J. Latokartano, J.-K. Kämäräinen, "AR-based interaction for human-robot collaborative manufacturing," *Robotics and Computer-Integrated Manufacturing* 63:101891, 2020, [doi:10.1016/j.rcim.2019.101891](https://doi.org/10.1016/j.rcim.2019.101891); [arXiv:1909.02933](https://arxiv.org/abs/1909.02933); [university record](https://researchportal.tuni.fi/en/publications/ar-based-interaction-for-human-robot-collaborative-manufacturing/).
- W. P. Chan, G. Hanks, M. Sakr, H. Zhang, T. Zuo, H. F. M. Van der Loos, E. Croft, "Design and Evaluation of an Augmented Reality Head-Mounted Display Interface for Human Robot Teams Collaborating in Physically Shared Manufacturing Tasks," *ACM Transactions on Human-Robot Interaction* 11(3), 2022, [doi:10.1145/3524082](https://doi.org/10.1145/3524082); [arXiv:2203.08343](https://arxiv.org/abs/2203.08343), whose [HTML version](https://arxiv.org/html/2203.08343) names the HoloLens.

**Commanding and teaching**

- T. Zhang, Z. McCarthy, O. Jow, D. Lee, X. Chen, K. Goldberg, P. Abbeel, "Deep Imitation Learning for Complex Manipulation Tasks from Virtual Reality Teleoperation," ICRA 2018, [doi:10.1109/ICRA.2018.8461249](https://doi.org/10.1109/ICRA.2018.8461249); [arXiv:1710.04615](https://arxiv.org/abs/1710.04615)
- A. Iyer et al., "OPEN TEACH: A Versatile Teleoperation System for Robotic Manipulation," 2024. [arXiv:2403.07870](https://arxiv.org/abs/2403.07870); [project page](https://open-teach.github.io/) — robots, 38 tasks, 87% on 10 tasks, the novice–expert study.
- X. Cheng, J. Li, S. Yang, G. Yang, X. Wang, "Open-TeleVision: Teleoperation with Immersive Active Visual Feedback," CoRL 2024. [arXiv:2407.01512](https://arxiv.org/abs/2407.01512); [project page](https://robot-tv.github.io/); [code](https://github.com/OpenTeleVision/TeleVision).
- S. Chen, C. Wang, K. Nguyen, L. Fei-Fei, C. K. Liu, "ARCap: Collecting High-quality Human Demonstrations for Robot Learning with Augmented Reality Feedback," ICRA 2025, [doi:10.1109/ICRA55743.2025.11128717](https://doi.org/10.1109/ICRA55743.2025.11128717); [arXiv:2410.08464](https://arxiv.org/abs/2410.08464)
- O. Kyjanek, B. Al Bahar, L. Vasey, B. Wannemacher, A. Menges, "Implementation of an Augmented Reality AR Workflow for Human Robot Collaboration in Timber Prefabrication," ISARC 2019, pp. 1223–1230. [iaarc.org](http://www.iaarc.org/publications/2019_proceedings_of_the_36th_isarc/implementation_of_an_augmented_reality_ar_workflow_for_human_robot_collaboration_in_timber_prefabrication.html)
- X. Wang, C.-J. Liang, C. Menassa, V. Kamat, "Real-Time Process-Level Digital Twin for Collaborative Human-Robot Construction Work," ISARC 2020, pp. 1528–1535. [iaarc.org](http://www.iaarc.org/publications/2020_proceedings_of_the_37th_isarc/real_time_process_level_digital_twin_for_collaborative_human_robot_construction_work.html)
- S. Park, C. C. Menassa, V. R. Kamat, "Integrating Large Language Models with Multimodal Virtual Reality Interfaces to Support Collaborative Human-Robot Construction Work," *Journal of Computing in Civil Engineering* 39(1), 2025, [doi:10.1061/JCCEE5.CPENG-6106](https://doi.org/10.1061/JCCEE5.CPENG-6106), also cited on [[05-construction-robotics/hrc-worker-centered|6. HRC]]; [arXiv:2404.03498](https://arxiv.org/abs/2404.03498).

**Egocentric data**

- J. Engel et al., "Project Aria: A New Tool for Egocentric Multi-Modal AI Research," 2023. [arXiv:2308.13561](https://arxiv.org/abs/2308.13561) — sensor suite, IMU rates, 1 kHz trajectories, privacy features.
- S. Kareer et al., "EgoMimic: Scaling Imitation Learning via Egocentric Video," ICRA 2025, [doi:10.1109/ICRA55743.2025.11127989](https://doi.org/10.1109/ICRA55743.2025.11127989); [arXiv:2410.24221](https://arxiv.org/abs/2410.24221)
- V. Liu et al., "EgoZero: Robot Learning from Smart Glasses," 2025. [arXiv:2505.20290](https://arxiv.org/abs/2505.20290); [HTML](https://arxiv.org/html/2505.20290) — poses from Meta's Machine Perception Services, refined with a hand-pose model.
- R. Hoque, P. Huang, D. J. Yoon, M. Sivapurapu, J. Zhang, "EgoDex: Learning Dexterous Manipulation from Large-Scale Egocentric Video," ICLR 2026. [arXiv:2505.11709](https://arxiv.org/abs/2505.11709)
- P. Banerjee et al., "HOT3D: Hand and Object Tracking in 3D from Egocentric Multi-View Videos," CVPR 2025. [arXiv:2411.19167](https://arxiv.org/abs/2411.19167)
- R. Punamiya et al., "EgoVerse: An Egocentric Human Dataset for Robot Learning from Around the World," 2026. [arXiv:2604.07607](https://arxiv.org/abs/2604.07607); [HTML](https://arxiv.org/html/2604.07607) — devices: Aria Gen 1, custom head-mounted rigs, head-strapped phones.
- J. W. Kim, K. Wang, Z. Fu, S. Chen, C. Zhao, J. Lai, C. Finn, "Ego-Pi: VLA Fine-Tuning for Ego-Centric Human and Robot Data," 2026. [arXiv:2606.08107](https://arxiv.org/abs/2606.08107) — Quest controllers on data gloves for teleoperation; Ray-Ban Meta's sales as motivation.

**Construction**

- D. Mitterberger, K. Dörfler, T. Sandy, F. Salveridou, M. Hutter, F. Gramazio, M. Kohler, "Augmented bricklaying: Human–machine interaction for in situ assembly of complex brickwork using object-aware augmented reality," *Construction Robotics* 4:151–161, 2020 (open access). [link.springer.com](https://link.springer.com/article/10.1007/s41693-020-00035-8)

**Surveys and venues**

- R. Suzuki, A. Karim, T. Xia, H. Hedayati, N. Marquardt, "Augmented Reality and Robotics: A Survey and Taxonomy for AR-enhanced Human-Robot Interaction and Robotic Interfaces," CHI 2022. [arXiv:2203.03254](https://arxiv.org/abs/2203.03254)
- M. Walker, T. Phung, T. Chakraborti, T. Williams, D. Szafir, "Virtual, Augmented, and Mixed Reality for Human-Robot Interaction: A Survey and Virtual Design Element Taxonomy," *ACM Transactions on Human-Robot Interaction* 12(4), 2023, [doi:10.1145/3597623](https://doi.org/10.1145/3597623); [arXiv:2202.11249](https://arxiv.org/abs/2202.11249)
- [VAM-HRI 2026](https://vam-hri.github.io/) · [IEEE ISMAR 2026](https://www.ieeeismar.net/2026/) · [IEEE VR 2026](https://ieeevr.org/2026/) · [EgoVis](https://egovis.github.io/) · [ISARC 2026](https://www.iaarc.org/isarc-2026)

**Within this wiki:** [[04-robotics/egocentric-perception|22. Egocentric Perception]] (E1, and Grossman et al. 1988 for the head rates) · [[04-robotics/human-pose-gaze|21. Human Pose, Hands & Gaze]] · [[04-robotics/human-intent-prediction|23. Human Intent]] · [[04-robotics/hri-safety|11. HRI & Safety]] · [[04-robotics/teleoperation-demonstration|12. Teleoperation & Demonstration]] · [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors]] · [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception]] · [[05-construction-robotics/site-engineering|2.5 Site Robotics]] (S1) · [[05-construction-robotics/hrc-worker-centered|6. HRC]] · [[05-construction-robotics/imitating-contact|10. Imitating Contact]] · [[03-deep-learning/vla/index|4. VLA]]

## 한국어

*J 그룹, 23 다음. 움직이는 카메라의 자세 — 위치와 방향 — 를 영상과 관성 측정 장치(IMU, [[04-robotics/sensor-models|3.2]]의 자이로와 가속도계)로 추정하는 [[04-robotics/state-estimation-slam|3 §7.2]], 마커 하나를 자세로 바꾸는 [[04-robotics/geometric-perception-calibration|3.5 §2.7]], 잘못 찍힌 타임스탬프를 밀리미터로 바꾸는 [[04-robotics/perception-sensors-rigs|3.6 §9]] 위에 선다. 이 페이지 고유의 대상 **X1**을 처음 쓰고, 건설 트랙의 파사드 패널 과제 S1([[05-construction-robotics/site-engineering|2.5]])을 다시 쓴다.*

작업자의 머리 위 헤드셋은 두 가지를 동시에 한다. 패널이 들어갈 벽 위에 로봇의 다음 동작을 그려 보이는 디스플레이이고, 작업자의 머리가 어디 있는지, 손이 어디 있는지, 기기에 따라서는 눈이 어디를 보는지까지 이미 재고 있는 센서 리그다. **이 페이지는 둘을 한 장면에서 함께 다루고, 모든 주장에 같은 질문을 던진다 — 어느 거리에서, 어느 머리 속도에서, 어느 지연으로, 어느 기기에서인가.**

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 두 층, 인식과 작업 완료의 사람 쪽을 맡는다. 작업자가 로봇이 다음에 무엇을 할지 보고, 로봇이 작업자가 어디를 보고 어디로 손을 뻗는지 보는 인터페이스다. "*저 패널을 프레임에 설치해*"의 여덟 단계 가운데 부품을 옮기는 단계와 맞춰 끼우는 단계, 곧 로봇이 패널을 프레임까지 가져가고 작업자가 맞추고 체결을 돕는 단계를 맡으며(그 칩은 [[physical-ai-map|피지컬 AI 지도]]의 인식 층, 21과 22 옆에 있다), 과제는 [[05-construction-robotics/site-engineering|2.5]]의 S1, 두 구멍을 ±5 mm 안에 맞춰야 하는 20 kg 파사드 패널이다. 이 페이지 없이는 헤드셋을 게이지처럼 믿거나 통째로 버리게 된다 — 이 페이지의 장면에서 구멍의 홀로그램(XR에서 렌더링된 가상 물체를 부르는 말)은 머리가 멈춰 있어도 7.40 mm, 90 °/s로 돌 때 19.18 mm 어긋나 ±5 mm를 검사할 수 없지만, 같은 헤드셋이 로봇의 다음 동작을 보여 주고 작업자의 머리와 손을 기록하고 시연을 모을 수 있다. 이 페이지는 [[05-construction-robotics/hrc-worker-centered|6. HRC §6–§8]](로봇이 패널을 싣고 가는 8 m 통로와 벽에서의 지지, 둘 다 곁에 작업자가 있다), [[04-robotics/teleoperation-demonstration|12 §4]](인터페이스 스펙트럼), [[05-construction-robotics/imitating-contact|10. 접촉 모방 §1]](이 페이지가 공급할 수 있는 시연), [[03-deep-learning/vla/index|4. VLA §7]](embodiment 격차)로 이어진다. [[07-research-program/index|7 §8]]의 학위논문 경로 밖에 있고, [[07-research-program/index|7 §9]]가 사람 인지에 대해 말하듯 현장이 요구할 때 들어온다. 이 페이지를 마치면 어떤 헤드셋이나 안경이든 분류에 넣고, Quest 3와 Ray-Ban Display에서 개발자가 무엇을 읽을 수 있는지 말하고, AR이 S1에서 무엇을 안내할 수 있고 무엇을 못 하는지 계산할 수 있다.

> [!note] 처음이라면 · First pass
> 세 번 앉아서 끝낸다. **첫째 — 기기.** 이 페이지의 대상을 읽고 그림에서 두 기기의 시야와 세 좌표계를 찾은 뒤 §1과 §2를 읽는다. §2의 접근 표에서 멈추고, 기기마다 로봇이 무엇을 기록할 수 있는지 말해 본다. **둘째 — 예산.** §3을 읽고, 계산 절의 여섯 단계를 손으로 따라간 다음 §10의 Part 1–3을 돌린다. 스스로 점검 2로 마무리한다. **셋째 — 이 분야가 해 온 일.** §4–§6과 §9의 지도를 읽으며 각 연구의 증거 단을 적는다. §7과 §8은 현장 연구를 하기 전에, 과제는 마지막에 푼다.

### 이 페이지의 대상 · Running object

**X1 — S1 옆 작업자의 헤드셋.** S1은 [[05-construction-robotics/site-engineering|2.5 현장 로보틱스]]가 고정한 건설 트랙의 과제다. 모바일 매니퓰레이터가 $20\,\mathrm{kg}$ 파사드 패널을 놓아 $400\,\mathrm{mm}$ 떨어진 두 구멍을 $\pm5\,\mathrm{mm}$ 안에 맞추고, 작업자가 체결하는 동안 붙잡고 있는다. X1은 로봇이 패널의 오른쪽 구멍을 브래킷에 가져가는 순간이고, 작업자는 로봇 옆에 서서 헤드셋을 쓰고 이를 본다. [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치는 맞지 않는다 — 장치(plant)는 제어 용어로 제어되는 시스템을 뜻하고 그 목록은 여섯 개(P1–P6)를 고정해 두는데, 그중 머리나 디스플레이를 가진 것은 없다. 그래서 이 페이지가 X1을 여기서 고정하고 숫자를 다시 바꾸지 않는다.

장면은 네 좌표계로 기술한다. 각각은 [[02-foundations/se3-geometry|8 §3]]의 뜻에서 자세, 곧 위치와 방향을 함께 가진 것이다. **W**는 추적이 시작된 곳에 고정된 헤드셋의 월드 좌표계, **H**는 작업자 머리 위의 헤드셋, **B**는 인쇄된 마커를 단 로봇 베이스, **T**는 목표 구멍이다. 로봇은 B에서 T를 알고, 헤드셋은 W에서 H를 안다. 두 세계를 잇는 $T_{WB}$가 §3에서 재는 앵커다.

| 양 | 기호 | 값 |
|---|---|---:|
| 눈에서 목표 구멍까지 | $D$ | $1.5\,\mathrm m$ |
| 마커 B에서 목표 구멍까지 | $L$ | $1.2\,\mathrm m$ |
| 머리 각속도 | $\omega$ | $0$, $30$, $90$, $300$ °/s |
| 머리 추적 오차: 위치, 방향 | $e_{p,H}$, $\delta\theta_H$ | $2\,\mathrm{mm}$, $0.05^\circ$ |
| 앵커 오차: 위치, 회전 | $e_{p,A}$, $\delta\theta_A$ | $2\,\mathrm{mm}$, $0.10^\circ$ |
| 예측 없는 모션-투-포톤 지연, 예측 뒤 남는 지연 | $\tau$, $\tau_{\mathrm{eff}}$ | $20\,\mathrm{ms}$, $5\,\mathrm{ms}$ |
| 기기 Q의 패스스루 지연 | $\tau_{\mathrm{pt}}$ | $40\,\mathrm{ms}$ |
| 로봇 상태가 헤드셋에 닿는 시간 | $\tau_{\mathrm{net}}$ | $50\,\mathrm{ms}$ |
| 메시지가 기기 G의 화면에 뜨는 시간 | $\tau_G$ | $0.3\,\mathrm s$ |
| 패널 속도: 마지막 접근, 통로 | $v$ | $0.05$, $0.5\,\mathrm{m/s}$ |
| 공차, 거친 안내 대역 | | $\pm5\,\mathrm{mm}$, $50\,\mathrm{mm}$ |

이 표의 숫자는 모두 **강의용 숫자**다. 계산이 깔끔하도록 고른 값이고 어떤 기기에서도 잰 값이 아니다. 세 개는 빌려 왔다. $90$ °/s와 $300$ °/s는 [[04-robotics/egocentric-perception|22. 1인칭 인식]]이 고정한 헬멧 카메라 E1의 머리 속도로, $90$ °/s는 Grossman 등이 제자리 걷기와 달리기에서 잰 상한, $300$ °/s는 그 페이지가 고른 둘러보기다. $0.5\,\mathrm{m/s}$는 [[05-construction-robotics/hrc-worker-centered|6. HRC]]의 베이스 통로 속도다. $30$ °/s는 패널을 눈으로 따라가는 머리다. $1\,\mathrm m$ 떨어진 곳에서 본 $0.5\,\mathrm{m/s}$는 $0.5\,\mathrm{rad/s} = 28.6$ °/s다. $\tau_{\mathrm{pt}} = 40\,\mathrm{ms}$는 §3이 인용하는 독립 측정값 범위의 위쪽 끝이다. 세 지연은 §3이 정의하는데, 한 줄씩 말하면 이렇다. **모션-투-포톤 지연**(motion-to-photon latency) $\tau$는 머리가 움직인 순간부터 그것을 보여 주는 빛이 디스플레이에 나올 때까지의 시간이고, 화면이 뜰 때 머리가 어디 있을지 예측하는 런타임은 이를 등가 지연 $\tau_{\mathrm{eff}}$로 줄인다. **패스스루 지연**(passthrough latency) $\tau_{\mathrm{pt}}$는 Q가 현실 세계를 영상으로 보여 주므로(§1) 그 카메라가 현실을 얼마나 늦게 보여 주는지다.

주인공인 두 기기는 실제 제품이고, 숫자는 제조사의 것을 Meta의 페이지에서 확인했다(출처).

| | **Q** — Meta Quest 3 | **G** — Meta Ray-Ban Display |
|---|---|---|
| 분류(§1) | 비디오 패스스루 헤드셋 | 디스플레이 스마트 글라스 |
| 디스플레이 | 눈마다 $2064\times2208$ px, $25$ px/deg, $110^\circ\times96^\circ$, $72$/$90$/$120\,\mathrm{Hz}$ | 오른쪽 렌즈의 풀컬러 패널 하나, $600\times600$ px, $42$ px/deg, 더하기식 |
| 바깥 카메라 | RGB 패스스루 카메라 2대($18$ px/deg)와 깊이 프로젝터, 손 추적용 IR 카메라 4대와 RGB 카메라 2대 | $12\,\mathrm{MP}$ 카메라 1대 |
| 눈, 손 | 눈 추적 없음, 손 추적 | 둘 다 없음, 제스처용 Meta Neural Band(표면 근전도) |
| 무게, 배터리 | 얼굴 패드를 뺀 $515\,\mathrm g$, 평균 최대 $2.2\,\mathrm h$ | $69\,\mathrm g$, 혼합 사용 최대 $6\,\mathrm h$ |

Neural Band는 **표면 근전도**(surface electromyography, EMG), 곧 팔뚝 근육의 전기 활동을 읽어 제스처로 바꾼다.

*범위: 이 페이지는 XR 기기가 무엇이고 무엇을 감지하는지, 홀로그램의 정합 오차가 S1에서 어떻게 쌓이는지, 협업·교시·데이터에서 XR이 무엇을 보였는지를 연구 지도와 함께 가르친다. 시각–관성 주행거리계([[04-robotics/state-estimation-slam|3 §7.2]]), 카메라 기하와 PnP([[04-robotics/geometric-perception-calibration|3.5]]), 시계 동기화([[04-robotics/perception-sensors-rigs|3.6 §9]]), 이격 거리([[04-robotics/hri-safety|11 §6]]), 원격조작의 안정성([[04-robotics/teleoperation-demonstration|12 §3]]), 디스플레이 광학은 가르치지 않는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 452" style="max-width:100%;height:auto" role="img" aria-label="축척 그대로 그린 X1 평면도: 작업자의 눈 H는 S1 패널의 목표 구멍 T에서 1.5 m, 로봇 베이스의 마커 B는 T에서 1.2 m, Quest 3의 110도 시야, 이 벽을 0.47 m 덮는 Ray-Ban Display의 14.3도 패널. 아래는 T에서 홀로그램의 오차: 머리 정지 7.40 mm, 예측 뒤 5 ms 지연에서 초당 30, 90, 300도일 때 11.33, 19.18, 46.67 mm, 예측 없이 초당 90도에서 54.53 mm, S1의 5 mm와 50 mm 대역과 함께">
  <defs><marker id="xrArrk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0 0L10 5L0 10z" fill="currentColor"/></marker>
  <pattern id="xrHatk" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="currentColor" stroke-width="1" stroke-opacity="0.45"/></pattern></defs>
  <g fill="currentColor" font-size="11">
    <text x="12" y="18" font-size="12" font-weight="600" fill-opacity="0.85">X1 평면도, 축척 그대로 (1 m = 110 px)</text>
    <rect x="27" y="48" width="363" height="10" fill="url(#xrHatk)" stroke="none"/>
    <line x1="27" y1="58" x2="390" y2="58" stroke="currentColor" stroke-width="1.6"/>
    <text x="27" y="43" font-size="10.5" fill-opacity="0.8">파사드 벽</text>
    <rect x="170" y="58" width="88" height="5.5" fill="currentColor" fill-opacity="0.22" stroke="currentColor" stroke-width="1"/>
    <circle cx="192" cy="60.8" r="2.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <circle cx="236" cy="60.8" r="2.6" fill="none" stroke="currentColor" stroke-width="1.2"/>
    <line x1="207.5" y1="56" x2="259.6" y2="56" stroke="currentColor" stroke-width="3.2" stroke-opacity="0.85"/>
    <text x="267.6" y="43" font-size="10.5" text-anchor="start">G가 벽 0.47 m를 덮는다</text>
    <rect x="112.8" y="163.6" width="66" height="48.4" rx="4" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
    <path d="M131.5 163.6 L126 113 L197.5 64.6" fill="none" stroke="currentColor" stroke-width="3" stroke-opacity="0.4" stroke-linejoin="round"/>
    <rect x="152.8" y="159.6" width="8" height="8" fill="currentColor" fill-opacity="0.85"/>
    <text x="163.8" y="178.6" font-size="11" font-weight="600">B</text>
    <line x1="156.8" y1="163.6" x2="236" y2="58" stroke="currentColor" stroke-width="1.1" stroke-dasharray="5 3"/>
    <text x="188.4" y="114.8" font-size="11" text-anchor="end">L = 1.2 m</text>
    <line x1="335" y1="190" x2="259.6" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="335" y1="190" x2="207.5" y2="58" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.8"/>
    <line x1="335" y1="190" x2="356.2" y2="125.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <line x1="335" y1="190" x2="266.8" y2="192.2" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="2 2"/>
    <polyline points="266.8,192.2 266.9,186.3 267.5,180.4 268.6,174.5 270.2,168.8 272.3,163.2 274.9,157.8 277.9,152.7 281.4,147.9 285.2,143.4 289.5,139.2 294.1,135.4 299,132.1 304.2,129.2 309.6,126.7 315.2,124.7 321,123.3 326.8,122.3 332.8,121.8 338.7,121.9 344.6,122.5 350.5,123.6 356.2,125.2" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6"/>
    <text x="328.3" y="117.9" font-size="11" font-weight="600">Q</text>
    <text x="282.3" y="108.4" font-size="11" font-weight="600">G</text>
    <line x1="335" y1="190" x2="238.5" y2="61.5" stroke="currentColor" stroke-width="1.4" marker-end="url(#xrArrk)"/>
    <text x="317.3" y="156.4" font-size="11">D = 1.5 m</text>
    <circle cx="236" cy="58" r="3.2" fill="currentColor"/>
    <text x="232" y="44" font-size="11" font-weight="600" text-anchor="middle">T</text>
    <circle cx="335" cy="190" r="9" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.4"/>
    <text x="322" y="205" font-size="11" font-weight="600" text-anchor="end">H</text>
    <line x1="379" y1="223" x2="401" y2="223" stroke="currentColor" stroke-width="1.2" marker-end="url(#xrArrk)"/>
    <line x1="379" y1="223" x2="379" y2="201" stroke="currentColor" stroke-width="1.2" marker-end="url(#xrArrk)"/>
    <text x="365" y="227" font-size="11" font-weight="600">W</text>
    <path d="M375 229 Q247 247.2 158.8 169.6" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="1.5 2.5"/>
    <text x="197.5" y="236.2" font-size="10" fill-opacity="0.85">앵커 T_WB</text>
    <path d="M375 218 L343 195" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.55" stroke-dasharray="1.5 2.5"/>
    <text x="407" y="217" font-size="10" fill-opacity="0.85">머리 자세 T_WH</text>
    <text x="404" y="78" font-size="10.5"><tspan font-weight="600">T</tspan> S1 패널의 목표 구멍</text>
    <text x="404" y="95" font-size="10.5"><tspan font-weight="600">B</tspan> 로봇 베이스의 마커</text>
    <text x="404" y="112" font-size="10.5"><tspan font-weight="600">H</tspan> 헤드셋을 쓴 작업자의 눈</text>
    <text x="404" y="129" font-size="10.5"><tspan font-weight="600">W</tspan> 헤드셋의 월드 좌표계</text>
    <text x="404" y="146" font-size="10.5"><tspan font-weight="600">Q</tspan> Quest 3, 110° 시야</text>
    <text x="404" y="163" font-size="10.5"><tspan font-weight="600">G</tspan> Ray-Ban Display, 14.3°</text>
    <line x1="8" y1="252" x2="552" y2="252" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3"/>
    <text x="12" y="270" font-size="12" font-weight="600" fill-opacity="0.85">T에서 홀로그램의 오차, mm (1 mm = 7 px)</text>
    <rect x="330" y="262" width="10" height="9" fill="currentColor" fill-opacity="0.75"/><text x="343" y="270" font-size="10">머리 추적</text>
    <rect x="400" y="262" width="10" height="9" fill="currentColor" fill-opacity="0.4"/><text x="413" y="270" font-size="10">앵커</text>
    <rect x="470" y="262" width="10" height="9" fill="url(#xrHatk)" stroke="currentColor" stroke-width="0.6"/><text x="483" y="270" font-size="10">지연</text>
    <line x1="167" y1="284" x2="167" y2="405" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>
    <text x="171" y="281" font-size="10" text-anchor="start">S1 ±5 mm</text>
    <line x1="482" y1="284" x2="482" y2="405" stroke="currentColor" stroke-width="1.1" stroke-dasharray="4 3"/>
    <text x="478" y="281" font-size="10" text-anchor="end">50 mm 대역</text>
    <text x="552" y="281" font-size="10" text-anchor="end" fill-opacity="0.85">합계</text>
    <text x="126" y="302" font-size="10.5" text-anchor="end">머리 정지</text>
    <rect x="132" y="292" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="292" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="292" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="292" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <text x="552" y="302" font-size="10.5" font-weight="600" text-anchor="end">7.40</text>
    <text x="126" y="326" font-size="10.5" text-anchor="end">30 °/s</text>
    <rect x="132" y="316" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="316" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="316" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="316" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="316" width="27.5" height="13" fill="url(#xrHatk)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="326" font-size="10.5" font-weight="600" text-anchor="end">11.33</text>
    <text x="126" y="350" font-size="10.5" text-anchor="end">90 °/s</text>
    <rect x="132" y="340" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="340" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="340" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="340" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="340" width="82.5" height="13" fill="url(#xrHatk)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="350" font-size="10.5" font-weight="600" text-anchor="end">19.18</text>
    <text x="126" y="374" font-size="10.5" text-anchor="end">300 °/s</text>
    <rect x="132" y="364" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="364" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="364" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="364" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="364" width="274.9" height="13" fill="url(#xrHatk)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="374" font-size="10.5" font-weight="600" text-anchor="end">46.67</text>
    <text x="126" y="398" font-size="10.5" text-anchor="end">90 °/s, 예측 없음</text>
    <rect x="132" y="388" width="14" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="146" y="388" width="9.2" height="13" fill="currentColor" fill-opacity="0.75" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="155.2" y="388" width="14" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="169.2" y="388" width="14.7" height="13" fill="currentColor" fill-opacity="0.4" stroke="currentColor" stroke-width="0.4" stroke-opacity="0.6"/>
    <rect x="183.8" y="388" width="329.9" height="13" fill="url(#xrHatk)" stroke="currentColor" stroke-width="0.7"/>
    <text x="552" y="398" font-size="10.5" font-weight="600" text-anchor="end">54.53</text>
    <line x1="132" y1="411" x2="517" y2="411" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
    <line x1="132" y1="411" x2="132" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="132" y="426" font-size="10" text-anchor="middle">0</text>
    <line x1="202" y1="411" x2="202" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="202" y="426" font-size="10" text-anchor="middle">10</text>
    <line x1="272" y1="411" x2="272" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="272" y="426" font-size="10" text-anchor="middle">20</text>
    <line x1="342" y1="411" x2="342" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="342" y="426" font-size="10" text-anchor="middle">30</text>
    <line x1="412" y1="411" x2="412" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="412" y="426" font-size="10" text-anchor="middle">40</text>
    <line x1="482" y1="411" x2="482" y2="415" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/><text x="482" y="426" font-size="10" text-anchor="middle">50</text>
    <text x="12" y="443" font-size="10" fill-opacity="0.8">예측 뒤 남는 지연 5 ms, 예측 없이 20 ms</text>
  </g>
</svg>

축척 그대로 그린 X1의 평면도다. 작업자의 눈 H는 목표 구멍 T에서 $1.5\,\mathrm m$, 로봇 베이스의 마커 B는 T에서 $1.2\,\mathrm m$ 떨어져 있고, Q의 시야는 $110^\circ$, G의 패널은 $14.3^\circ$로 이 벽을 $0.47\,\mathrm m$ 덮는다. 아래는 T에서 홀로그램의 오차로, 머리가 멈추면 $7.40\,\mathrm{mm}$, 예측 뒤 $5\,\mathrm{ms}$ 지연에서 $30$, $90$, $300$ °/s일 때 $11.33$, $19.18$, $46.67\,\mathrm{mm}$, 예측 없이 $90$ °/s에서 $54.53\,\mathrm{mm}$이며, S1의 $\pm5\,\mathrm{mm}$와 $50\,\mathrm{mm}$ 대역과 함께 그렸다.

### 1. 현실–가상 연속체와 기기 분류

*한 문장으로:* AR, MR, VR, XR은 현실 세계에서 렌더링된 세계까지 이어진 한 줄 위의 위치를 가리키고, 기기의 분류 — 현실 세계가 눈에 어떻게 닿는지, 기기가 무엇을 추적하는지 — 가 소프트웨어가 돌기도 전에 무엇을 보여 줄 수 있는지를 정한다.

**문제.** 논문은 태블릿, 프로젝터, 투과형 헤드셋, 카메라 패스스루 헤드셋을 모두 "AR 인터페이스"라 부르지만, 넷은 서로 다른 광학과 다른 지연, 다른 실패 방식으로 로봇의 계획을 보여 준다. 분류가 가장 먼저 읽어야 할 것이다.

**연속체.** Milgram과 Kishino(1994)는 한 줄의 한쪽 끝을 "실제 물체로만 이루어진" 순수한 현실 환경으로, 다른 끝을 순수한 가상 환경으로 두고, 현실과 가상의 물체를 함께 보여 주는 모든 디스플레이를 **혼합현실**(mixed reality, MR)이라 불렀다. 증강현실(AR)은 현실 세계에 가상 콘텐츠를 더한 MR, 증강가상(AV)은 콘텐츠 대부분이 가상인 MR이고, 가상현실(VR)은 가상 쪽 끝이다. 이 표현은 연속체를 다시 검토한 Skarbez, Smith, Whitton(2021)의 인용에서 가져왔다. 원래의 IEICE 페이지는 봇 확인 뒤에 있어 열지 않았다. **XR**은 이 모두를 덮는 우산이다. W3C의 WebXR 명세는 이 약어를 VR, AR과 관련 기술의 하드웨어·응용·기법 스펙트럼 전체에 쓰고, Meta, Microsoft, Magic Leap, HTC, Valve, PICO 기기가 구현하는 제조사 공통 인터페이스 Khronos OpenXR은 XR을 VR, AR, MR을 아우르는 현실–가상 결합 환경의 연속체로 정의한다.

> [!info] 정의 — 혼합현실(mixed reality)
> 기기가 아니라 **디스플레이와 경험의 한 부류**다. 한 시야 안에 현실과 가상의 물체를 함께 보여 주는 것들이다. 조건은 셋이다. 시야에 **현실 콘텐츠**가 있고(직접 보든 카메라로 보든), **렌더링된 콘텐츠**가 있으며, 둘이 한 시야 안에서 **함께** 보인다. 그래서 로봇 옆의 노트북 화면은 MR이 아니다. 이 페이지는 연속체를 숫자 하나, 시야 가운데 렌더링된 몫으로 읽는다.
> $$v=\frac{\Omega_{\text{rendered}}}{\Omega_{\text{view}}},\qquad \text{MR}\iff 0 < v < 1$$
> 여기서 $\Omega$는 입체각(sr)으로, 시야가 구의 얼마를 덮는지 재는 [[04-robotics/egocentric-perception|22의 척도]]다. $v=0$은 현실 환경, $v=1$은 VR이고, AR은 $v$가 작은 MR, AV는 $v$가 1에 가까운 MR이다. 이 몫은 이 페이지의 교육용 장치이지 Milgram과 Kishino의 것이 아니다.
> **예.** G의 $14.3^\circ$ 정사각 패널은 $0.0618\,\mathrm{sr}$로, Q의 $110^\circ\times96^\circ$ 시야가 차지하는 $2.618\,\mathrm{sr}$의 $2.4\%$다. G는 현실 쪽 끝 가까이 있다. Q는 시야의 어떤 몫이든, 전부라도 렌더링할 수 있다.
> **반례.** 아무것도 렌더링하지 않고 패스스루만 보여 주는 Q는 $v=0$이다. 작업자는 현실 콘텐츠만 보지만 카메라를 거쳐 $\tau_{\mathrm{pt}}$ 늦게 본다(§3). 유리를 통해 보는 것과 같은 경험이 아니다.
> **왜 중요한가.** 다음 정의와 함께, 기기가 무엇을 가릴 수 있고 무엇을 더하며 시야의 어느 부분이 늦는지 알려 준다.

**현실 세계가 눈에 닿는 방식**이 움직이는 로봇 옆 헤드셋에 대해 가장 결정적인 사실이다.

> [!info] 정의 — 광학 투과와 비디오 투과(optical and video see-through)
> **헤드 마운트 디스플레이**(head-mounted display, HMD)의 성질, 곧 현실 세계의 빛이 눈에 닿는 경로다. **광학 투과**(OST): 현실의 빛이 웨이브가이드 같은 결합기를 지나 그대로 들어오고 디스플레이가 빛을 *더한다*. **비디오 투과**(VST): 카메라가 세계를 찍고 디스플레이가 카메라 픽셀과 렌더링 픽셀을 합성해 보여 준다. 둘을 가르는 조건은 셋이다 — 현실의 빛이 **직접** 눈에 닿는가, 디스플레이가 빛을 **뺄** 수 있는가(OST는 덧붙인 디머 없이는 못 한다), **어느 콘텐츠가 늦는가**(OST는 렌더링된 부분만, VST는 전부).
> $$\text{OST: } L_{\text{eye}}(t)=L_{\text{world}}(t)+L_{\text{virt}}(t-\tau),\qquad \text{VST: } L_{\text{eye}}(t)=(1-\alpha)\,L_{\text{world}}(t-\tau_{\mathrm{pt}})+\alpha\,L_{\text{virt}}(t-\tau)$$
> 여기서 $L$은 눈에 닿는 빛, $\tau$는 렌더링 지연, $\tau_{\mathrm{pt}}$는 패스스루 지연, $\alpha\in[0,1]$은 렌더링 층의 불투명도다.
> **예.** G는 OST다. Meta의 개발자 페이지는 그 디스플레이를 "더하기식 웨이브가이드"라 부르고, 그 위에서 "순수한 검정으로 렌더링한 픽셀은 완전히 투명하다"고 쓴다. Q는 VST다. RGB 카메라 두 대가 디스플레이에 영상을 보낸다.
> **반례.** 디머가 OST를 VST로 바꾸지는 않는다. Magic Leap 2의 디머 패널은 콘텐츠 뒤의 세계를 어둡게 하려고 "광자를 선택적으로 빼지만", 현실의 빛은 여전히 지연 없이 직접 들어온다.
> **왜 중요한가.** 움직이는 로봇 옆에서 OST는 로봇을 제자리에, 홀로그램을 늦게 보여 주고, VST는 둘 다 늦게 보여 준다. §3이 둘의 값을 매긴다.

**기기 분류.** 연구와 현장이 쓰는 것은 여섯 부류로 덮인다. 예시는 제조사 자신의 페이지를 읽은 것만 적었다.

| 분류 | 세계가 눈에 닿는 길 | 추적 | 보여 줄 수 있는 것 | 예 |
|---|---|---|---|---|
| VR 헤드셋 | 닿지 않음 | 머리(6-DoF), 손 또는 컨트롤러 | 렌더링된 세계 | VR 모드의 Q |
| 비디오 패스스루 MR 헤드셋 | 카메라를 거쳐 | 머리, 손, 깊이, 일부는 눈 | 영상 위의 월드 고정 콘텐츠, 세계를 가릴 수 있음 | **Q, Meta Quest 3**, Apple Vision Pro |
| 광학 투과 AR 헤드셋 | 웨이브가이드를 지나 직접 | 머리, 손, 눈, 깊이 | 더하기식 월드 고정 홀로그램 | Microsoft HoloLens 2와 Trimble XR10(안전모에 넣은 HoloLens 2), Magic Leap 2 |
| 디스플레이 스마트 글라스 | 직접 | 방향, 카메라 | 머리에 고정된 작은 패널 | **G, Meta Ray-Ban Display**, RealWear Navigator 520 |
| 카메라만 있는 스마트 글라스 | 직접 | 카메라와 소리 | 소리 말고는 없음 | Ray-Ban Meta(Gen 2) |
| 연구용 안경 | 직접 | 머리, 눈, IMU, SLAM 카메라 | 시각적으로는 없음, 기록만 함(Gen 2는 소리 피드백) | Project Aria Gen 1, Gen 2 |

6-DoF는 위치 셋, 방향 셋의 여섯 자유도이고, SLAM 카메라는 스스로 지도를 만들며 위치를 추적하는 **동시적 위치 추정과 지도 작성**(simultaneous localisation and mapping)에 쓰인다(§2). 월드 고정 콘텐츠는 머리가 움직여도 방 안의 제자리를 지키고, 머리 고정 콘텐츠는 화면 위의 제자리를 지켜 머리와 함께 움직인다(둘 다 §3이 정의한다). 광학 투과 부류는 줄어들고 있다. Microsoft의 릴리스 노트는 2024년 12월부로 HoloLens 기기를 더 이상 생산하지 않으며 보안 업데이트는 2027년 12월까지라고 적고, Magic Leap의 판매 약관은 Magic Leap 2의 직접 판매 종료일을 2026년 3월 31일로 정했다. §4의 의도 연구 네 편 가운데 세 편이 Microsoft HoloLens를 명시하므로, 그 증거의 일부는 이제 만들지 않는 기기에서 잰 것이다.

**두 주인공 기기가 보여 줄 수 있는 것.** Q는 패스스루 위에 월드 고정 콘텐츠를 렌더링하므로 작업자가 주위를 걸어도 가상 물체가 벽 위에 그대로 있고, 불투명하게 렌더링한 부분은 뒤의 세계를 가린다. G는 오른쪽 렌즈에 $600\times600$ 픽셀을 $42$ px/deg로 보여 준다. 픽셀 밀도가 고르다고 두면 패널은 $600/42 = 14.3^\circ$ 너비, 대각선 $20.2^\circ$이고, $D=1.5\,\mathrm m$에서 정면으로 보면 $0.376\,\mathrm m$ 너비이며, 머리와 함께 움직인다. Meta는 이 화면을 "시야를 가리지 않도록 옆으로 비켜" 두었고 "짧은 상호작용을 위해 설계"했다고 쓴다. Q는 장면 안에 기하를 그리고, G는 장면에 대한 메시지를 보여 준다.

**함정.** 제목의 "AR"은 분류에 대해 아무것도 말하지 않는다. 기기를 읽고 두 가지를 물어라 — 현실 세계가 눈에 직접 닿는가, 콘텐츠가 세계에 고정되는가 머리에 고정되는가.

> [!note]- 더 깊이 · Deeper
> **다른 부류의 숫자, 제조사 페이지에서.** Apple Vision Pro(M5): 메인 카메라 2대, 바깥을 향한 추적 카메라 6대, 눈 추적 카메라 4대, TrueDepth 카메라, LiDAR 스캐너, IMU 4개, "12밀리초 photon-to-photon 지연", $750$–$800\,\mathrm g$, 최대 $2.5\,\mathrm h$. HoloLens 2: 가시광 머리 추적 카메라 4대(앞쪽 두 대는 대각선 $96.1^\circ$, 간격 $98.6\,\mathrm{mm}$), 적외선 눈 추적 카메라 2대, $1$메가픽셀 ToF 깊이 센서, 자력계가 들어간 IMU, $566\,\mathrm g$, $2$–$3\,\mathrm h$. "보조 현실"(assisted reality)로 팔리는 RealWear Navigator 520: 조절식 붐 암 위의 $1280\times720$, $24^\circ$ 디스플레이, $50\,\mathrm{MP}$ 카메라, 소음 제거 마이크 4개, IP66, $270\,\mathrm g$. **가상 쪽 끝에 닿을 수 없는 이유**는 Skarbez 등에 따르면 이렇다. 헤드셋은 눈과 귀에 들어가는 것은 다스리지만 몸의 균형 감각과 운동 감각은 다스리지 못해 감각 충돌이 늘 남는다 — §8의 사이버멀미다.

### 2. 센서 리그로서의 HMD

*한 문장으로:* 콘텐츠를 제자리에 두려면 헤드셋은 화면 한 장마다 여러 번 자기 자세를 알아야 하므로 이미 카메라, IMU, 흔히 손과 눈 추적까지 싣고 있다. 작업자 머리 위의 센서 리그이고, 로봇은 제조사가 열어 준 만큼 그것을 읽을 수 있다.

**문제.** 작업자 옆의 로봇은 세 가지를 알고 싶다. 머리가 어디 있고 어디를 향하는지, 눈이 어디를 보는지, 손이 어디 있는지. [[04-robotics/human-pose-gaze|21 §4]]는 시선이 다음 행동의 가장 강한 단일 단서이고, 로봇 자신의 카메라는 몇 미터를 넘으면 머리 자세밖에 보지 못한다는 것을 보였다. 헤드셋은 렌더링을 위해 셋을 모두 잰다. 개발자가 실제로 무엇을, 얼마나 빨리, 어떤 규칙 아래서 읽어 낼 수 있는가?

**생각.** HMD는 자기 센서로 자기 자세를 추정한다. 그래서 어디서든 쓸 수 있다.

> [!info] 정의 — 인사이드아웃 추적(inside-out tracking)
> **자세 추정 방법**이다. 기기가 싣고 다니는 센서로 주변을 관찰해 외부 설비 없이 자기의 6-DoF 자세를 추정한다. 조건은 셋이다. 센서가 **기기 위에** 있고(카메라, IMU, 때로 깊이), 자세가 기기가 **스스로 만든 주변 지도**, 곧 월드 좌표계 W로 표현되며, 추정이 빠른 관성 측정과 느린 시각 측정의 **융합**이다. 지도를 곁들인 시각–관성 주행거리계(VIO), 곧 SLAM이다([[04-robotics/state-estimation-slam|3 §7.2]]).
> $$T_{WH}(t_k)=\arg\min_{T}\Big(\sum_j \big\lVert \tilde u_j-\pi(T^{-1}p_j)\big\rVert^2_{\Sigma_u}+\big\lVert r_{\mathrm{IMU}}(T,T_{WH}(t_{k-1}))\big\rVert^2_{\Sigma_I}\Big)$$
> 여기서 $\tilde u_j$는 지도의 점 $p_j$가 보인 픽셀, $\pi$는 점을 카메라에 투영하는 사상([[04-robotics/geometric-perception-calibration|3.5 §1]]), $r_{\mathrm{IMU}}$는 지난 추정 이후 IMU가 적분한 움직임과의 불일치이며, 각 항은 제 잡음으로 가중된다.
> **예.** HoloLens 2는 가시광 카메라 4대와 IMU로 머리를 추적하고, Project Aria Gen 1은 수평 시야 $150^\circ$의 흑백 글로벌 셔터 SLAM 카메라 2대와 IMU 2개로 추적한다.
> **반례.** 외부 카메라나 모션 캡처가 기기의 마커를 추적하는 아웃사이드인 추적. HOT3D의 정답 자세가 이렇게 얻어졌다(§6). IMU 하나로 얻은 방향도 인사이드아웃 6-DoF 추적이 아니다. G의 웹 앱은 방위, 기울기, 롤을 받을 뿐 머리 위치는 받지 못한다(위치는 짝지은 폰에서 온다).
> **왜 중요한가.** VIO가 실패하는 곳 — 무늬 없는 벽, 어둠, 빠른 움직임, 카메라와 함께 움직이는 장면 — 에서 실패하는데, 이는 건설 현장의 가장 흔한 조건 목록이다.

**IMU가 카메라보다 훨씬 자주 재는 이유.** $300$ °/s로 도는 머리는 $30\,\mathrm{Hz}$ 카메라의 두 프레임 사이에 $10.0^\circ$, $1\,\mathrm{kHz}$ IMU의 두 샘플 사이에 $0.30^\circ$ 돈다. 그런데 디스플레이는 화면마다, Q에서는 초당 $72$–$120$번 새 자세가 필요하다. 카메라 한 간격 동안 자이로는 거의 떠내려가지 않는다. [[04-robotics/sensor-models|3.2 §3]]의 자이로로 $1/30\,\mathrm s$를 적분하면 $0.0013^\circ$, $D$에서 $0.03\,\mathrm{mm}$이지만, 10초를 혼자 두면 $0.104^\circ$, $2.72\,\mathrm{mm}$ 떠내려간다. 그래서 IMU가 프레임 사이의 자세를 나르고 카메라가 계속 고친다. Project Aria가 이 분업을 보여 준다. IMU 두 개가 $800$과 $1000\,\mathrm{Hz}$로 표본을 뜨고 — "고차 오차 거동이 서로 상관되지 않을 가능성을 높이려고" 일부러 다른 모델을 골랐다 — 카메라와 융합되어 열린 루프 표류가 이동 거리의 $0.4\%$ 이하인 $1\,\mathrm{kHz}$ 궤적이 된다.

**함정: 속도뿐 아니라 범위.** Aria의 왼쪽 IMU는 $500$ °/s에서 포화된다(오른쪽 IMU는 $1000$ °/s). E1의 머리 속도 출처인 Grossman 등은 의도적으로 세게 돌린 머리에서 집단 중앙값 최고 $780$ °/s를 쟀는데, 이는 그 한계의 $1.56$배다. 빠른 흘끗 보기 때 잘리는 IMU는 시야가 가장 크게 바뀌는 바로 그 순간에 필터에 틀린 회전을 넘긴다.

**두 주인공 기기가 감지하는 것, 그리고 개발자가 읽을 수 있는 것.** 간직할 표다. API(application programming interface)는 앱이 부를 수 있는 호출의 집합이고, SDK(software development kit)는 그것을 묶은 꾸러미이며, Horizon OS는 Quest의 운영체제다. 모든 칸은 Meta의 제품·개발자 페이지에서 왔고, 페이지가 말하지 않는 것은 "문서에 없음"이라 적었다.

| | Q — Meta Quest 3 | G — Meta Ray-Ban Display |
|---|---|---|
| 들어가는 길 | 헤드셋 위의 앱(Meta XR SDK, OpenXR, Android) | 개발자 프리뷰 단계의 Wearables Device Access Toolkit을 쓰는 폰 앱, 또는 안경 위에서 도는 웹 앱 |
| 머리 | 런타임이 주는 6-DoF 자세, 각 화면의 표시 시각에 맞춰 예측됨 | 방향만: 표준 DeviceMotion·DeviceOrientation 웹 API(가속도계, 자이로, 나침반), 착용자 허락 필요. 위치는 문서에 없음 |
| 눈 | 없음: Quest 3에는 눈 추적이 없다 | 문서에 없음 |
| 손 | 손 골격, 기본 $30\,\mathrm{Hz}$, Fast Motion Mode에서 최대 $60\,\mathrm{Hz}$. 손이 카메라 시야를 벗어나면 Wide Motion Mode가 "그럴듯한" 자세를 채움. Touch Plus 컨트롤러 | 없음. 터치패드와 Neural Band 제스처는 화살표 키와 Enter 이벤트로 오고, 웹 앱에는 연속 커서가 없음 |
| 카메라 | Passthrough Camera API(Android Camera2, Horizon OS v74 이상): 좌우 RGB 카메라, $1280\times960$ 또는 $1280\times1280$, 최대 $60\,\mathrm{Hz}$, 영상 포착 지연 $20$–$40\,\mathrm{ms}$, 내부·외부 파라미터, 타임스탬프, 카메라의 월드 자세 제공. 패스스루 시야 전체를 덮지는 않음 | 툴킷만: $720\times1280$, $504\times896$, $360\times640$ 영상, 초당 $2$, $7$, $15$, $24$, $30$ 프레임, Bluetooth Classic으로 전송. 대역폭이 모자라면 해상도부터, 다음 프레임률을 낮추되 $15$ 아래로는 내리지 않음. 사진. 웹 앱은 카메라 없음 |
| 깊이, 장면 | Depth API: 실시간 깊이 지도, $0.2\,\mathrm m$보다 가까우면 믿을 수 없음. 저장·공유되는 공간 앵커 | 짝지은 폰에서 오는 위치, Meta 추정으로 $5$–$50\,\mathrm m$ 정확도 |
| 소리 | 내장 스테레오 스피커 | 툴킷: Hands-Free Profile로 $8\,\mathrm{kHz}$ 모노 마이크, 스피커 |
| 화면 출력 | 앱이 렌더링하는 무엇이든, 월드 고정이든 머리 고정이든 | $600\times600$ px: 폰이 Bluetooth로 보내는 툴킷 레이아웃(보낼 때마다 화면 전체를 교체), 또는 웹 앱의 HTML |
| 권한 | 카메라에 `CAMERA` 또는 `HEADSET_CAMERA`, 손 추적 권한과 기능 플래그 | Meta AI 앱에서 확인하는 카메라 권한(항상, 한 번, 거부), 웹 앱은 센서 허락 창 |
| 데이터 규칙 | 손 데이터는 "앱 안에서 손 추적을 가능하게 하는 데에만" 쓸 수 있음. 카메라 영상은 Meta 개발자 데이터 사용 정책의 Device User Data | 갤러리용으로 촬영하면 캡처 LED가 깜박이고, 가리면 카메라가 꺼짐 |

**로봇이 각각에서 얻는 것.** Q에서는 작업자 머리의 6-DoF 자세, 손, 자세와 타임스탬프가 붙은 보정된 카메라 두 대의 영상, 깊이를 얻는다. 로봇의 계획을 제자리에 보여 주고(§4), 원격조작하거나 시연을 기록하고(§5), 1인칭 데이터를 모으기(§6)에 충분하다. 눈 시선은 없으니 주의는 여전히 머리 자세 대용이고, [[04-robotics/egocentric-perception|22 §3]]의 경고가 모두 따라온다. G에서는 두 갈래 길로 얻는다. 폰 앱은 작업자의 1인칭 영상(초당 최대 $30$ 프레임)과 소리를 받고, 안경 위의 웹 앱은 머리 방향과 거친 위치를 읽는다. 읽은 페이지들은 둘이 함께 돌 수 있는지 말하지 않는다. 두 길 모두 G의 머리 고정 패널에 쓸 수 있다. G의 머리 위치를 주는 문서는 없다. 위치 없이는 눈에서 세계의 한 점으로 가는 방향을 유지할 수 없다. $D=1.5\,\mathrm m$에서 옆으로 $0.3\,\mathrm m$ 걸으면 T의 참 방위가 $\arctan(0.3/1.5)=11.3^\circ$ 도는데, 방향만 쓰는 화살표는 움직이지 않는다.

**함정.** Wide Motion Mode의 자세는 손을 보지 못한 동안의 추정이다. 모드와 함께 기록하지 않으면 시연 말뭉치에 측정과 짐작이 섞인다. 툴킷의 카메라 프레임은 Bluetooth 링크에 맞게 압축되어 오고, Meta는 영상이 "해상도가 HIGH나 MEDIUM으로 보고되어도 기대보다 낮은 품질로 보일 수 있다"고 경고한다. 로봇 학습을 위해 손 자세를 기록하는 연구 앱은 손 데이터가 손 추적을 가능하게 하는 데에만 쓰인다는 Meta의 규칙을 연구 전에 확인해야 한다.

### 3. 정합과 지연

*한 문장으로:* S1 구멍의 홀로그램은 사슬을 거쳐 그려진다 — 헤드셋 세계 속 로봇 베이스(앵커), 그 세계 속 머리(추적), 그리고 표시되는 순간(지연). 각 고리의 오차는 제 지렛대 팔을 곱해 구멍에 떨어지므로, 예산은 S1 자신의 예산처럼 구멍에서 적는다.

**문제.** 작업자는 벽에 그려진 표시를 믿을 것이다. 머리가 멈춰 있을 때 그것은 참 구멍에서 얼마나 떨어져 있고, 머리가 돌 때는 얼마나이며, 어느 고리를 고칠 가치가 있는가?

**사슬.** 로봇은 베이스 좌표계에서 구멍 $p_B$를 안다. 헤드셋은 그것을 $p_W=T_{WB}\,p_B$에 그리고 머리 자세 $T_{WH}$로 투영한다([[04-robotics/robot-systems-deployment|10 §4]]가 좌표계를 이름 짓고, [[02-foundations/se3-geometry|8 §3]]이 합성한다). 틀릴 수 있는 것은 셋이다 — $T_{WB}$(앵커), $T_{WH}$(추적), 그리고 $T_{WH}$가 유효했던 시각(지연). 회전 오차 $\delta\theta$는 회전축에서 $\ell$ 떨어진 점을 $\ell\,\delta\theta$만큼 옮긴다. 그래서 S1의 배분도 구멍에서 적는다([[05-construction-robotics/site-engineering|2.5 §2]]). 지연은 자세를 잰 뒤 머리가 돈 각 $\omega\tau$이고, [[04-robotics/perception-sensors-rigs|3.6 §9]]의 법칙 $e=\omega\,\Delta t\,R$이다.

> [!info] 정의 — 정합 오차(registration error)
> 가상 물체가 보이는 곳과 그 실제 짝이 있는 곳 사이의 **변위**(mm)이며, 이름 붙인 점에서, 이름 붙인 눈에 대해, 이름 붙인 머리 속도에서 말한다. 조건은 넷이다. **점**(여기서는 앵커가 아니라 T), **시점**(눈에서 $D$), **머리 움직임**($\omega$ — 지연 항은 머리가 멈춰 있을 때만 0이다), 그리고 항들을 합치는 **결합 규칙**이다. S1의 예산처럼 규칙을 밝혀야 한다.
> $$e_{\text{reg}}=\big(e_{p,H}+D\,\delta\theta_H\big)+\big(e_{p,A}+L\,\delta\theta_A\big)+D\,\omega\,\tau_{\mathrm{eff}}$$
> 첫 괄호는 머리 추적, 둘째는 지렛대 $L$을 가진 앵커, 마지막은 지연 항이다. 각은 라디안이고 작은 각 근사를 쓴다. 탄젠트로 바꾸면 정적 항은 많아야 $2.1\,\mathrm{nm}$ 바뀌고, 가장 큰 지연 항($300$ °/s, $20\,\mathrm{ms}$의 $6^\circ$)은 $0.58\,\mathrm{mm}$($0.37\%$) 바뀐다.
> **예.** 머리가 멈춘 X1: $3.31+4.09=7.40\,\mathrm{mm}$(계산 절).
> **반례.** 머리를 고정했을 때 홀로그램의 떨림은 정합 오차가 아니라 안정성 수치이고, 앵커 항도 지연 항도 빠져 있다. 로봇 자신의 배치 오차도 여기에 들어가지 않는다. 패널이 어떻든, 홀로그램은 T가 어디 있는지에 대해 맞거나 틀릴 뿐이다.
> **왜 중요한가.** AR이 무엇을 안내할 수 있는지를 정한다. 자기 오차가 $7.40\,\mathrm{mm}$인 게이지는 $\pm5\,\mathrm{mm}$ 공차를 검사할 수 없다.

**지연, 그리고 헤드셋이 예측하는 이유.** 모든 화면은 그보다 먼저 잰 자세로 그려진다.

> [!info] 정의 — 모션-투-포톤 지연(motion-to-photon latency)
> **시간 간격**이다. 머리가 움직인 순간부터, 새 자세에서 본 장면을 보여 주는 빛이 디스플레이에 나올 때까지. 조건: 파이프라인의 한 단계가 아니라 감지에서 광자까지 **끝에서 끝으로** 재고, 표시 시각의 자세를 예측하는 런타임은 대부분을 숨기므로 **예측이 있는지 없는지** 밝히며, 튀는 값이 중요하므로 **분포**로 보고한다(§8).
> $$\tau=t_{\text{photon}}-t_{\text{motion}},\qquad \delta\theta_{\text{lat}}(t)=\theta(t)-\hat\theta(t)\approx\omega\,\tau\ \text{(no prediction)},\quad \approx\tfrac12\,\dot\omega\,\tau^2\ \text{(constant-rate prediction)}$$
> 여기서 $\theta$는 머리 각, $\hat\theta$는 화면이 그려진 기준 각, $\omega$는 각속도, $\dot\omega$는 각가속도다.
> **예.** X1의 $\tau=20\,\mathrm{ms}$는 $90$ °/s에서 홀로그램을 머리보다 $1.8^\circ$ 뒤처지게 해 $D$에서 $47.12\,\mathrm{mm}$가 되고, 예측 뒤에는 $11.78\,\mathrm{mm}$다.
> **반례.** 프레임 시간은 지연이 아니다. $1/90\,\mathrm s=11.1\,\mathrm{ms}$는 $90\,\mathrm{Hz}$의 Q가 얼마나 자주 다시 그리는지이지 각 화면이 얼마나 늦는지가 아니다. 패스스루(photon-to-photon) 지연도 다른 간격으로, 현실 장면의 변화에서 디스플레이가 그것을 보여 줄 때까지다.
> **왜 중요한가.** 예산 가운데 머리 속도와 함께 커지는 유일한 항이고, 머리는 중요한 순간에 가장 빨리 움직인다.

OpenXR은 예측을 인터페이스에 넣어 두었다. 앱은 시야 자세를 표시 시각, 곧 "시야 자세가 예측되는 시각"에 대해 요청하고, 런타임이 예측하는 표시 시각은 "화면이 표시되는 구간의 한가운데를 가리켜야 한다". 예측으로도 없앨 수 없는 것은 가속도 항이어서, 시작하거나 멈추는 회전은 여전히 번진다(§10, Part 3).

**$\tau_{\mathrm{eff}}$가 뜻하는 것.** 완벽하게 일정한 회전을 일정 속도로 예측하면 오차가 전혀 남지 않는다(스스로 점검 5). 실제 예측은 조금씩 빗나간다. 외삽하는 각속도는 잡음 섞인 자이로 추정값이고, 표시 시각 자체도 예측이며, 머리는 한 속도로 오래 돌지 않는다. X1은 이 빗나감을 하나의 등가 지연 $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$(강의용 숫자)로 묶는다. 그래서 예산은 예측이 켜져 있으면 $D\,\omega\,\tau_{\mathrm{eff}}$를, 꺼져 있으면 $D\,\omega\,\tau$를 매긴다.

독립 시험장비 업체 OptoFidelity는 2024년에 헤드셋들을 쟀다. 예측과 time warp(완성된 화면을 표시 직전에 가장 새로운 머리 자세로 다시 투영하는 것)를 켠 각 모션-투-포톤의 중앙값은 몇 밀리초였고, Quest Pro와 Quest 3가 무리에서 가장 좋았으며 HTC의 $4\,\mathrm{ms}$는 "기대보다 조금 높다"고 했다. 패스스루(photon-to-photon) 최솟값은 Apple Vision Pro가 약 $11\,\mathrm{ms}$(Apple의 발표는 $12$), Quest 3, Quest Pro, HTC VIVE XR Elite가 $35$–$40\,\mathrm{ms}$였다. X1의 $\tau_{\mathrm{pt}}=40\,\mathrm{ms}$는 그 범위의 위쪽 끝이다.

**움직이는 로봇 옆에서 OST와 VST는 다르게 실패한다.** G나 다른 OST 헤드셋에서는 로봇이 제자리에 보이고 렌더링 층만 늦는다. Q에서는 시야 전체가 늦는다. $0.05\,\mathrm{m/s}$로 다가오는 패널은 실제 위치보다 $2.0\,\mathrm{mm}$ 뒤에, 통로의 $0.5\,\mathrm{m/s}$에서는 $20.0\,\mathrm{mm}$ 뒤에 보인다. $\tau_{\mathrm{net}}=50\,\mathrm{ms}$ 묵은 보고 상태로 그린 로봇의 "유령"은 $2.5$와 $25.0\,\mathrm{mm}$ 뒤처진다. 둘 다 머리 움직임의 효과가 아니므로, 예측도 멈춘 머리도 없애지 못한다.

**헤드셋의 세계를 로봇 베이스에 맞추기.** $T_{WB}$는 재야 한다. Q에서 가장 곧은 길은 로봇에 붙인 마커와 PnP — 한 장의 영상에서 알려진 물체의 자세를 구하는 것, [[04-robotics/geometric-perception-calibration|3.5 §2.7]] — 를 패스스루 카메라로 푸는 것이다. 그 API가 내부 파라미터, 외부 파라미터, 영상 타임스탬프, 그 순간 W에서의 카메라 자세를 주므로 $T_{WB}=T_{WC}\,T_{CB}$이고 $T_{CB}$는 PnP에서 온다. 조심할 것 셋. 작고 먼 마커는 거의 같은 두 PnP 해 사이를 오갈 수 있고 기울기가 가장 약한 방향이다(3.5의 $2\,\mathrm m$ 거리 $0.5\times0.4\,\mathrm m$ 표적에서 $1$픽셀 잡음이면 한 장당 $\pm2.70^\circ$). 그러니 큰 마커, 여러 장의 영상, 서로 떨어진 마커를 쓴다. 카메라 자세는 도착한 때가 아니라 영상 자신의 타임스탬프에서, 곧 $20$–$40\,\mathrm{ms}$ 전의 것을 써야 한다([[04-robotics/perception-sensors-rigs|3.6 §9]]). 그리고 마커를 로봇 좌표계에 보정해야 한다([[04-robotics/geometric-perception-calibration|3.5 §5]]).

> [!info] 정의 — 공간 앵커(spatial anchor)
> 추적이 스스로를 고치는 동안에도 거기 붙인 콘텐츠가 세계에 고정되도록 **헤드셋의 지도 안에 유지되는 자세**다. Meta 문서가 주는 조건: **한 점에서 만들어지고** 고유 식별자(UUID)로 불린다. 뒤의 세션에서 헤드셋의 지도가 **다시 찾으며**(저장), 여러 헤드셋이 한 좌표계에 합의하도록 **공유**할 수 있다. **옮길 수 없다** — 콘텐츠를 옮기려면 앵커를 지우고 새로 만든다. 그리고 **자기 근처에서** 정확하다 — Meta는 붙잡을 물체에서 3미터 안에 앵커를 만들라고 권하는데, 물체가 앵커에서 멀수록 자세 오차가 증폭되기 때문이다.
> $$p_W=T_{WA}\,p_A,\qquad \lVert\delta p_W\rVert\le e_{p,A}+\lVert p_A\rVert\,\delta\theta_A$$
> 여기서 $T_{WA}$는 앵커의 자세, $p_A$는 앵커에서 콘텐츠까지의 오프셋, $\delta\theta_A$는 앵커의 회전 오차다.
> **예.** X1의 앵커인 B의 마커는 T에서 $L=1.2\,\mathrm m$라, $0.10^\circ$가 구멍에서 $2.09\,\mathrm{mm}$가 된다. Meta의 한계인 $3\,\mathrm m$에서는 같은 각이 $5.24\,\mathrm{mm}$를 만든다.
> **반례.** 월드 좌표계 W 자체는 앵커가 아니다. 그 원점은 과제가 아니라 추적이 시작된 곳이 정하고, 일관된 혼합현실 공간을 위한 Meta의 권고도 공간 앵커로 추적 공간을 맞추라는 것이다.
> **왜 중요한가.** 헤드셋의 세계와 로봇의 세계를 잇는 다리다. 지렛대 규칙은 다리를 작업 옆에 놓으라고 말한다.

> [!info] 정의 — 월드 고정과 머리 고정 콘텐츠(world-locked, head-locked)
> **렌더링 콘텐츠를 두는 방식의 성질**이다. 월드 고정 콘텐츠는 W에서 자세가 고정되어 머리가 움직일 때마다 화면 위 자리가 바뀌고, 머리 고정 콘텐츠는 화면 위 자리가 고정되어 머리와 함께 움직인다. 조건: 월드 고정에는 **6-DoF 머리 자세**가 필요하고 정합 오차가 생긴다. 머리 고정에는 **자세가 필요 없고** 세계의 어느 자리도 주장하지 않으므로 정합 오차도 없다.
> $$\text{world-locked: } p_H(t)=T_{WH}(t)^{-1}\,p_W,\qquad \text{head-locked: } p_H(t)=\text{const}$$
> 여기서 $p_H$는 머리에 대해 콘텐츠가 놓인 자리다.
> **예.** Q가 구멍 위에 그린 표적은 월드 고정이다. G의 $600\times600$ 패널은 머리 고정이고, 문서화된 인터페이스 어디에도 콘텐츠를 세계에 고정하는 기능은 없다.
> **반례.** 나침반 방위를 따라 도는 G의 화살표는 어느 쪽도 아니다. 방향만 고정되어 있어 $0.3\,\mathrm m$ 걸음 하나로 T에 대해 $11.3^\circ$ 틀린다.
> **왜 중요한가.** 위의 예산을 치러야 하는 것은 월드 고정 콘텐츠뿐이다. 머리 고정 콘텐츠는 다른 비용, 작업에서 눈을 돌리는 흘끗 보기를 치른다(§8).

**함정.** 지연 항은 회전하는 동안 늘 머리가 온 쪽으로 치우친 편향이므로 선형으로 더하고, 절대 제곱합 제곱근(RSS)으로 합치지 않는다 — [[05-construction-robotics/site-engineering|2.5 §2]]의 반례다. 머리를 멈춘 채 시연한 홀로그램은 가장 좋은 경우를 보여 준 것이다. 그리고 정합 오차는 로봇의 배치가 아니라 홀로그램을 잰다.

### 대상으로 한 번 끝까지 · Worked case

X1 위의 여섯 단계다. 먼저 §3의 예산을 구멍에서 세우고, 다음에 각 주인공 기기가 무엇을 보여 주는지 본다. 고정된 숫자 위의 강의용 계산이지 어느 기기를 잰 것이 아니다.

**1단계 — 구멍에서의 머리 추적.** 위치 오차는 그대로 오고, 방향 오차는 $D$가 곱해져 온다.

$$e_{p,H}+D\,\delta\theta_H=2+1500\times0.05\times\frac{\pi}{180}=2+1.31=3.31\,\mathrm{mm}$$

$0.05^\circ$가 $8.73\times10^{-4}\,\mathrm{rad}$이기 때문이다.

**2단계 — 앵커.** 마커의 회전 오차는 $D$가 아니라 $L$을 지렛대로 삼는다.

$$e_{p,A}+L\,\delta\theta_A=2+1200\times0.10\times\frac{\pi}{180}=2+2.09=4.09\,\mathrm{mm}$$

앵커가 T에서 $1.2\,\mathrm m$ 떨어진 B를 축으로 돌기 때문이다. B를 Meta의 $3\,\mathrm m$ 한계에 두면 같은 $0.10^\circ$가 앵커 하나만으로 S1의 공차 전체보다 큰 $5.24\,\mathrm{mm}$를 만든다.

**3단계 — 머리가 멈췄을 때.** 선형으로 $3.31+4.09=7.40\,\mathrm{mm}$로 $\pm5\,\mathrm{mm}$ 밖이다. 네 원천이 독립이고 평균이 0이라 가정하는 제곱합 제곱근은 $\sqrt{2^2+1.31^2+2^2+2.09^2}=3.75\,\mathrm{mm}$로 $1.25\,\mathrm{mm}$를 남기고 안에 든다. 그런데 너그러운 읽기로도 검사 도구로는 실패한다. 자기 오차가 $\pm3.75\,\mathrm{mm}$인 홀로그램은 실제로 $5\,\mathrm{mm}$ 어긋난 패널을 $1.25$에서 $8.75\,\mathrm{mm}$ 사이 어디로든 보여 주므로, 잘 앉은 것과 잘못 앉은 것을 가르지 못한다.

**4단계 — 머리가 돌 때.** 예측 뒤 남는 $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$에서 지연 항 $D\,\omega\,\tau_{\mathrm{eff}}$는 $30$, $90$, $300$ °/s에서 $3.93$, $11.78$, $39.27\,\mathrm{mm}$이고, 선형 합은 $11.33$, $19.18$, $46.67\,\mathrm{mm}$로 모두 $50\,\mathrm{mm}$ 대역 안이다. 예측이 없으면 $90$ °/s에서 $\tau=20\,\mathrm{ms}$가 $47.12\,\mathrm{mm}$를 더해 $54.53\,\mathrm{mm}$로 대역 밖이다. $7.40+D\,\omega\,\tau=50$을 $\omega$에 대해 풀면

$$\omega_{\max}=\frac{50-7.40}{D\,\tau}=\frac{42.60}{1500\times0.005}\,\mathrm{rad/s}=325^\circ/\mathrm s\quad\text{(}81^\circ/\mathrm s\text{ at }\tau=20\,\mathrm{ms})$$

인데, $\omega$와 함께 커지는 항이 지연 항 하나뿐이기 때문이다. 걸어 다니는 작업자가 거친 대역을 지키게 해 주는 것이 예측이다. $81$ °/s는 걷기의 $90$ °/s 바로 아래다.

**5단계 — Q가 움직이는 패널을 보여 주는 방식.** 패스스루는 실제 패널을 $v\,\tau_{\mathrm{pt}}$ 늦게 보여 준다. 마지막 접근에서 $0.05\times40=2.0\,\mathrm{mm}$, 통로에서 $20.0\,\mathrm{mm}$다. $50\,\mathrm{ms}$ 묵은 상태로 그린 로봇 유령은 $2.5$와 $25.0\,\mathrm{mm}$ 뒤처진다. 해상도는 한계가 아니다. $18$ px/deg의 패스스루 픽셀 하나는 $D$에서 $1.45\,\mathrm{mm}$이니 $5\,\mathrm{mm}$ 어긋남은 세 픽셀이 넘는다. 한계는 정합이다.

**6단계 — G가 보여 주는 것.** G의 패널은 $14.3^\circ$ 정사각형으로 $D$에서 정면으로 보면 $0.376\,\mathrm m$ 너비이고, 이 벽을 비스듬히 보면 $0.47\,\mathrm m$를 덮는다. 머리 고정이고 머리 위치가 없으므로 $0.3\,\mathrm m$ 걸음이 T의 참 방위를 $11.3^\circ$ 돌려 놓아, G는 T를 표시할 수 없다. 대신 T를 이름으로 부를 수 있다 — "3번 패널, B 구역, 다음은 오른쪽 구멍, 로봇 이동 중". 나타나는 데 $\tau_G=0.3\,\mathrm s$가 걸리는 메시지는 $1.6\,\mathrm{m/s}$로 걷는 작업자에게 $1.6\times0.3=0.48\,\mathrm m$의 바닥을 치르게 한다. [[04-robotics/hri-safety|11 §5]]의 시간 계산이다.

**판정.** X1에서 월드 고정 AR은 거친 규모에서 안내한다 — 어느 브래킷인지, 접근 경로, 출입 금지 구역, 다음 행동. 예측이 도는 동안 모두 $50\,\mathrm{mm}$ 안이다. 마지막 $\pm5\,\mathrm{mm}$는 안내하지도 검사하지도 못한다. 그것은 로봇의 손목 카메라와 [[05-construction-robotics/hrc-worker-centered|6 §7]]의 해제 시험에 남는다. G는 위치가 아니라 말과 기호로 안내한다.

### 4. 사람–로봇 협업을 위한 XR — 로봇의 의도 전달

*한 문장으로:* 로봇의 계획을 작업이 일어나는 자리에 보여 주면 화면보다 빠르고 정확하게 읽히지만, 그렇게 보인 연구들은 작고, 실험실에서, 대부분 지금 시장을 떠나는 헤드셋으로 이루어졌다.

**문제.** 로봇 옆의 작업자는 로봇이 다음에 무엇을 할지 — 경로, 목표, 쓸고 지나갈 구역 — 를 대응할 만큼 일찍 알아야 한다. [[04-robotics/hri-safety|11 §5]]는 이를 시간으로 말한다. 사람이 알아채고 반응하는 데 드는 1초마다 바닥 $1.6\,\mathrm m$가 든다.

**생각.** 작업자가 고개를 돌려 읽어야 하는 별도 화면 대신, 실제 로봇 위 제자리에 계획을 그린다. 이것은 [[04-robotics/human-intent-prediction|23 §2]]의 단서 사슬을 거꾸로 돌리는 것이다. 거기서는 로봇이 사람이 움직이기 전에 시선, 머리, 손을 읽고, 여기서는 사람이 로봇이 움직이기 전에 계획을 읽는다. $2\,\mathrm s$ 앞의 경로를 보여 주면 $0.5\,\mathrm{m/s}$ 로봇의 $1.0\,\mathrm m$이고, 그 $2\,\mathrm s$ 동안 $1.6\,\mathrm{m/s}$로 걷는 작업자는 $3.2\,\mathrm m$를 간다. 디스플레이는 교차 중이 아니라 교차 전의 결정을 산다.

**연구들이 잰 것.**

- **실제 로봇 위의 팔 동작.** Rosen, Whitney, Phillips, Chien, Tompkin, Konidaris, Tellex(ISRR 2017, IJRR 2019에서 확장)는 로봇 팔의 계획된 동작을 혼합현실 헤드셋인 Microsoft HoloLens에 그렸다. 참가자 32명이 동작마다 탁자 위 블록과 부딪히는지 판정했다. 2D 디스플레이, 시각화 없음과 비교해 헤드셋은 다음으로 좋은 시스템보다 정확도를 $16\%$ 높이고 과제 시간을 $62\%$ 줄였다.
- **비행 경로.** Walker, Hedayati, Lee, Szafir(HRI 2018, 디자인 부문 최우수 논문)는 드론의 임박한 경로를 AR로 보여 주었고, 참가자는 더 효율적이었다.
- **작업 영역을 나누는 조립.** Hietanen, Pieters, Lanz, Latokartano, Kämäräinen(*Robotics and Computer-Integrated Manufacturing* 63, 2020)은 깊이 센서로 작업 영역을 감시하고, 디젤 엔진 조립 과제에서 HoloLens와 프로젝터–거울 장치에 대화형 안전 인터페이스를 띄웠다. 상호작용과 공간 공유가 없는 기준선과 비교해 둘 다 과제 시간을 $21$–$24\%$, 로봇 유휴 시간을 $57$–$64\%$ 줄였다. 그러나 주관 평가에서는 "HoloLens 기반 AR은 아직 산업 제조에 적합하지 않다"였고, 프로젝터는 안전과 작업 인간공학을 개선했다.
- **산업 파트너와의 팀 과제.** Chan, Hanks, Sakr, Zhang, Zuo, Van der Loos, Croft(*ACM Transactions on Human-Robot Interaction* 11(3), 2022)는 복합재 제조를 위한 HoloLens 인터페이스를 사용자 $26$명으로 평가했다. AR은 신체 부담과 완료 시간을 줄이고 로봇 활용을 높였지만, 사용자는 조이스틱을 더 믿을 만하다고 느꼈다.

**규칙.** 의도 디스플레이는 경고 채널이지 안전 기능이 아니다. 보호 이격 거리와 그 정지 사슬([[04-robotics/hri-safety|11 §6]], [[05-construction-robotics/hrc-worker-centered|6 §6]])은 헤드셋을 벗어도 성립해야 한다. 작업자는 벗을 수도, 딴 데를 볼 수도, 묵은 유령에게 틀린 정보를 받을 수도 있기 때문이다(§3). XR이 바꿀 수 있는 것은 사람이 얼마나 일찍 결정하느냐다.

**함정.** 위의 모든 효과는 2D 화면이나 아무것도 없는 것과 비교한 것이고, 실험실에서 재었으며(초록이 인원을 밝힌 경우 $32$명과 $26$명), 넷 중 셋이 HoloLens였다. 현장에서 잰 것은 없고, 읽은 초록과 페이지들은 과제 결과 옆에 정합 오차를 적지 않는다. "16% 더 정확"은 "그 과제에서, 그 거리에서, 그 헤드셋으로"라고 읽어라.

### 5. 로봇에게 명령하고 가르치는 XR

*한 문장으로:* 헤드셋은 이미 머리와 손을 6-DoF로 추적하므로 입력 장치를 겸한다 — 제자리에서 계획을 승인하고, 원격조작하고, 시연을 모은다 — 그리고 손에서 로봇으로의 사상을 맡은 페이지는 12다.

**문제.** 현장에서 로봇을 프로그래밍하고 계획을 고치거나, 학습된 정책에 필요한 시연을 기록하려면([[05-construction-robotics/imitating-contact|10. 접촉 모방 §1]]) 사람의 의도가 6-DoF로, 로봇이 쓸 수 있는 속도로 필요하다.

**생각.** 사람이 하는 몫에 따라 세 가지다. **승인**: 로봇이 제안하고 사람이 제자리에서 계획을 살펴 받아들인다. **명령**: 사람이 움직이면 로봇이 실시간으로 따른다. **로봇 없이 시연**: 사람이 과제를 하고 헤드셋이 나중의 학습을 위해 기록하며, 로봇이 재현할 수 있는지를 AR로 알려 준다.

**보여진 것.**

- **건설에서의 승인.** Kyjanek, Al Bahar, Vasey, Wannemacher, Menges(ISARC 2019)는 목조 프리패브에서 HoloLens를 쓴 작업자가 로봇 궤적을 계획하고, 생산 순서에 개입하고, 겹쳐 보이는 진단 피드백을 보게 했다. 로봇은 모바일 플랫폼 위의 KUKA LBR iiwa였다. Wang, Liang, Menassa, Kamat(ISARC 2020)는 공정 수준의 VR 디지털 트윈을 만들었다. 사람이 과제 계획을 시연하면 로봇이 동작을 계획하고, 그 계획이 사람의 평가와 승인을 위해 돌아온 뒤에야 실행한다. 사례는 불완전한 스터드 골조 위의 석고보드 설치였다.
- **소비자용 헤드셋으로 명령.** Zhang 등(ICRA 2018)은 소비자용 VR 헤드셋과 손 추적으로 로봇을 원격조작하고 그 시연으로 시각운동 정책을 학습했다. OPEN TEACH(Iyer 등, arXiv 2024)는 Meta Quest 3 위에 만들어져 Franka, xArm, Jaco, Allegro, Hello Stretch 로봇을 "최대 90Hz로" 조종한다. 과제 $38$개에서 보였고, 그 데이터로 학습한 정책은 그중 $10$개에서 평균 $87\%$ 성공했으며, 새 사용자는 전문가보다 $2.25$배 오래 걸렸고 성공률은 프로젝트 페이지의 말로 "전문가와 비교해" $76\%$였다. Open-TeleVision(Cheng 등, CoRL 2024)은 조작자에게 로봇 주변의 능동적 입체 시각을 주고 팔과 손 동작을 로봇에 옮긴다. 코드는 WebXR로 Apple Vision Pro와 Meta Quest 3를 지원하고, 휴머노이드 두 대로 긴 과제 네 개의 정책을 학습했다.
- **로봇 없이 시연.** ARCap(Chen, Wang, Nguyen, Fei-Fei, Liu, ICRA 2025)은 가상 로봇이 제약을 어길 때 AR 시각 피드백과 햅틱 경고를 주며 사람의 시연을 모아, 초보자도 로봇이 실행할 수 있는 데이터를 만들게 한다.

**X1에서의 규칙.** 헤드셋의 자세를 네트워크를 건너 로봇의 ROS 2 그래프에 넣는 일은 시계 문제와 함께 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]의 몫이다. Q의 손 골격은 기본 $30\,\mathrm{Hz}$로 오므로 $0.5\,\mathrm{m/s}$로 움직이는 손은 표본 사이에 $16.7\,\mathrm{mm}$ 간다. Fast Motion Mode의 $60\,\mathrm{Hz}$는 이를 $8.3\,\mathrm{mm}$로 반으로 줄이지만, Meta가 경고하는 떨림을 대가로 치른다. $90\,\mathrm{Hz}$ 제어 루프는 손 표본 하나를 세 틱 동안 보므로 붙잡아 두거나 보간해야 한다. 일대일로 옮기면 표본당 $16.7\,\mathrm{mm}$로는 S1의 구멍을 $\pm5\,\mathrm{mm}$ 안에 놓을 수 없다. [[04-robotics/teleoperation-demonstration|12 §5]]의 동작 스케일 $10$을 쓰면 로봇은 표본당 $1.67\,\mathrm{mm}$ 움직인다. 원격조작의 미세 정렬이 동작을 줄여 옮기는 이유다.

**함정.** 손 추적 원격조작은 힘을 기록하지 않으므로 위의 모든 것은 위치만의 시연을 모은다 — [[04-robotics/teleoperation-demonstration|12 §4]] 스펙트럼의 시각 인터페이스와 햅틱 끝 사이의 간극이다. Wide Motion Mode의 그럴듯한 자세를 측정값으로 기록하면 안 된다(§2). 그리고 시연 인터페이스의 성공률은 누가 썼느냐에 달렸다. OPEN TEACH의 초보자는 전문가보다 $2.25$배 오래 걸렸다.

### 6. 스마트 글라스의 1인칭 데이터와 로봇 학습

*한 문장으로:* 안경과 헤드셋은 사람이 보고 하는 것을 어떤 로봇 무리도 따라올 수 없는 규모로 기록하고, 로봇 정책이 그 데이터로 배우기 시작했지만, 영상과 함께 머리와 손의 자세가 — 기기가 기록했든 그 카메라와 IMU로 나중에 추정했든 — 주어진 곳에서만 그렇고, 힘은 어디에도 없다.

**문제.** 학습된 정책은 시연이 많이 필요하고, 로봇 시연은 모으기 느리고 비싸다([[04-robotics/teleoperation-demonstration|12 §1]]은 원격조작을 그것을 만드는 도구로 다룬다). 사람은 어차피 과제를 한다. 사람의 1인칭 기록이 로봇 데이터의 일부를 대신할 수 있을까?

> [!info] 정의 — 1인칭 데이터(egocentric data)
> 과제를 하는 사람을 지켜보는 카메라가 아니라, **그 사람이 착용한 센서의 시간 정렬된 기록**이다. 조건은 넷이다. 센서가 **착용되어** 시점이 머리와 함께 움직이고([[04-robotics/egocentric-perception|22 §3]]), 스트림들이 **한 시계**를 공유하며, **행동을 복원할 수 있어야** 하고 — 로봇 학습에서는 픽셀만이 아니라 3D의 머리와 손 자세를 뜻한다 — 기록된 사람들, 착용자와 주변 사람이 **동의**했어야 한다.
> $$\mathcal E=\big\{\big(I_t,\ T_{WH}(t),\ h_t,\ g_t\big)\big\}_{t=1}^{N},\qquad a_t=\rho\big(h_t,\ T_{WH}(t)\big)$$
> 여기서 $I_t$는 영상, $T_{WH}$는 머리 자세, $h_t$는 손 자세, $g_t$는 기록된 경우의 시선, $\rho$는 사람 손에서 로봇 행동으로의 리타기팅이다([[04-robotics/teleoperation-demonstration|12 §5]]).
> **예.** EgoZero의 Project Aria 기록: Meta의 기계 인식 서비스가 안경 자신의 카메라와 IMU로 계산하고 손 자세 모델로 다듬은 머리와 손 자세가 붙은 영상으로, 여기서 로봇이 실행할 수 있는 행동을 뽑는다.
> **반례.** G의 툴킷 영상은 1인칭이지만 Bluetooth로 초당 최대 $30$ 프레임이고 머리나 손의 자세가 없어, 별도의 자세 추정기 없이는 $a_t$를 복원할 수 없다. 같은 과제의 3인칭 영상도 1인칭이 아니다(22 §5의 Ego-Exo4D는 일부러 둘을 함께 기록한다).
> **왜 중요한가.** 규모는 커지지만 embodiment 격차를 안고 온다. 사람 손은 그리퍼가 아니고, 과제의 힘은 그림에 없다.

**보여진 것.** 1인칭 영상을 연구 대상으로 만든 데이터셋들(Ego4D, EPIC-KITCHENS, Ego-Exo4D)은 [[04-robotics/egocentric-perception|22 §5]]의 주제다. 그 뒤를 이은 로봇 학습 계열:

- **기기.** Project Aria(Engel 등, arXiv 2023)는 Meta의 연구용 안경이다. Gen 1에는 SLAM 카메라 2대, RGB 카메라 1대, 눈 추적 카메라 2대, IMU 2개, 자력계, 기압계, 위성 측위(GNSS), 마이크 7개가 있다. Gen 2(2025)는 SLAM 카메라 4대, PPG 심박 센서, 접촉 마이크를 더하고, SLAM, 눈 추적, 손 추적을 기기에서 처리하며, 무게는 약 $75\,\mathrm g$이고 소리 피드백을 준다.
- **함께 학습.** EgoMimic(Kareer 등, ICRA 2025)은 3D 손 추적이 붙은 사람 데이터를 Aria 안경으로 모으고, 기구학적 격차를 줄이려고 고른 저가 양팔 로봇을 쓰며, 사람과 로봇 데이터로 한 정책을 함께 학습한다. 손 데이터 1시간을 더하는 것이 "로봇 데이터 1시간을 더하는 것보다 훨씬 가치 있었다".
- **로봇 데이터 없이.** EgoZero(Liu 등, arXiv 2025)는 로봇 데이터 없이 Aria 기록만으로 배우고, 그리퍼를 단 Franka Panda에 옮겨 과제 7개에서 $70\%$ 성공했다. 과제당 데이터는 $20$분, 모두 $140$분이다.
- **손 자세와 함께 규모를.** EgoDex(Hoque 등, ICLR 2026)는 Apple Vision Pro로 3D 손과 손가락 추적이 짝지어진 1인칭 영상 $829$시간을 탁상 과제 $194$개에 걸쳐 기록했다. 과제당 약 $4.3$시간이다.
- **고리 안의 Quest 3.** HOT3D(Banerjee 등, CVPR 2025)는 Project Aria와 Quest 3로 손–물체 상호작용 $833$분을 기록했고, 정답은 모션 캡처로 얻었다.
- **여러 실험실, 한 규약.** EgoVerse(Punamiya 등, arXiv 2026)는 $1{,}362$시간(에피소드 $80{,}000$개, 과제 $1{,}965$개, 시연자 $2{,}087$명)을 모으고 사람에서 로봇으로의 전이를 여러 실험실에서 재현한다. 사람 데이터가 많을수록 대체로 성능이 오르지만 "효과적인 확장은 사람 데이터와 로봇 학습 목표 사이의 정렬에 달려 있다"고 결론짓는다.

이 가운데 Ray-Ban급 안경으로 기록한 것은 없다. 데이터는 머리와 손 자세를 기록하는 Aria, Vision Pro, Quest 3에서 왔고, EgoVerse에서는 직접 만든 머리 착용 장치와 머리띠에 단 폰에서도 왔는데, 그 파이프라인이 머리 자세는 시각–관성 SLAM으로, 손은 $21$개 키포인트 모델로 프레임마다 추정한다. 데이터 장갑에 단 Quest 컨트롤러로 — 컨트롤러가 헤드셋에 대한 조작자 손목을 추적한다 — 휴머노이드를 원격조작하고 1인칭 사람 데이터로 $\pi_{0.5}$ 기반 정책을 미세 조정한 Ego-Pi(Kim 등, arXiv 2026)는, 이런 데이터를 대규모로 모으는 일이 현실적이 되는 이유로 200만 대 팔린 Ray-Ban Meta 안경을 든다.

**X1에서의 규칙.** 기록은 행동을 실어야 한다. Aria Gen 2와 Vision Pro는 기기에서 머리와 손을 추적하고, Aria Gen 1의 자세는 Meta의 처리에서 오며, Q의 런타임은 실시간으로 준다. G의 툴킷은 영상과 소리만 기록하고 머리 자세를 추정할 관성 스트림은 문서에 없으며, 대체 하한인 초당 $15$ 프레임에서는 $0.5\,\mathrm{m/s}$로 움직이는 손이 프레임 사이에 $33.3\,\mathrm{mm}$ 간다.

**함정.** 위의 데이터셋은 모두 가정이나 탁상, 맨손, 사람 크기의 과제다. S1의 패널은 $20\,\mathrm{kg}$이고, 그것을 앉히는 힘이야말로 안경이 볼 수 없는 것이다. [[03-deep-learning/vla/index|4. VLA §7]]의 embodiment 격차에 힘의 격차가 더해지고, [[05-construction-robotics/imitating-contact|10. 접촉 모방]]이 이를 정면으로 다룬다. 작업자의 1인칭 기록은 화면 안에 주변 사람이 있는 인간 대상 연구이기도 하다([[04-robotics/egocentric-perception|22 §6]]).

### 7. 건설 현장에서

*한 문장으로:* 현장은 더하기식 디스플레이 위의 햇빛, 추적에 불리한 무늬 없고 변하는 주변, 먼지, 장갑, 소음, 안전모, 주변 사람을 더한다. 그리고 실제 건물에서 ±5 mm 공차를 맞춘 유일한 AR 시스템은 머리가 아니라 물체를 추적해서 그렇게 했다.

**문제.** 위의 모든 것은 실내에서 잰 것이다. 햇빛 아래 파사드에서는 어느 부분이 살아남는가?

**알아야 할 현장 결과.** Mitterberger, Dörfler, Sandy, Salveridou, Hutter, Gramazio, Kohler(*Construction Robotics* 4, 2020)는 "증강 벽돌 쌓기"로 그리스의 와이너리에 벽돌 $13{,}596$장의 치장 벽돌 파사드를 지었다. 조작자가 벽돌 자체를 추적하는 손에 든 카메라와 IMU를 들었고(물체 인식형), 공유 화면의 화살표가 벽돌의 자세가 목표에서 $4\,\mathrm{mm}$ 안에 들 때까지 벽돌공을 안내했다. $2\,\mathrm{mm}$ 문턱도 시험했으나 벽돌공이 화살표를 너무 오래 쫓았다. 벽은 국부 정밀도 $\pm5\,\mathrm{mm}$, 파사드 요소 $5\times5\,\mathrm m$ 전체에서 $\pm1\,\mathrm{cm}$에 이르렀다. 추적이 콘크리트 골조와 세로 지주도 전역 기준으로 함께 잡아, 오차가 벽돌에서 벽돌로 쌓이지 않았기 때문이다. S1에 중요한 세부가 셋이다.

- **헤드셋이 화면에 졌다.** 팀은 화면, 태블릿, Magic Leap 헤드셋을 비교해, 야외의 밝은 현장에서는 화면이 가장 효율적인 시각화 플랫폼이라는 결론을 내렸다. 디지털 모델을 물리 세계에 충분히 정확하게 맞추지 못하는 것을 기존 AR 시스템의 알려진 한계로 든다.
- **햇빛이 검출을 깨뜨렸다.** 직사광이 그림자 선을 만들어 벽돌 검출을 방해했고, 해법은 검은 천 가림막이었다.
- **정확도는 시간을 치렀다.** 익숙해진 뒤 벽돌 한 장에 $3$분으로, 벽돌공 두 명이 회전 없는 일자 쌓기에 드는 한 장당 $1$분과 비교된다.

**왜 이것이 §3과 맞는가.** 부품을 추적하면 공차를 맞춰야 하는 바로 그 물체에서 고리가 닫혀, 앵커 항과 머리 추적 항이 예산에서 빠진다. 헤드셋의 세계에 그린 X1의 홀로그램은 그 항들을 그대로 안고 있다. S1에서 헤드셋이 $\pm5\,\mathrm{mm}$에 이르려면 로봇의 손목 카메라처럼 패널과 브래킷을 직접 재야 한다([[04-robotics/geometric-perception-calibration|3.5 §2.7]]).

**기기별 현장 조건.**

- **안전모와 보안경.** Microsoft는 HoloLens 2가 시험을 거쳐 ANSI Z87.1, CSA Z94.3, EN 166의 기본 충격 보호 요구에 부합한다고 적고, Trimble XR10을 "먼지 많고 시끄럽고 안전 관리가 필요한 환경의 작업자를 위해 만든", 안전모에 HoloLens 2를 넣은 기기로 소개한다. HoloLens 2이므로 생산도 HoloLens 2를 따른다. RealWear는 Navigator 520이 헬멧, 청력 보호구와 함께 쓸 수 있고 IP66(먼지가 들어가지 않고 강한 물줄기에도 견딘다는 등급), $-20$–$45^\circ\mathrm C$라고 적는다. Q와 G에 대해 읽은 페이지들은 안전모나 다른 개인 보호구(PPE)에 대해 아무 말도 하지 않는다.
- **더하기식 디스플레이 위의 햇빛.** OST에서 검정은 투명하고, 밝은 장면은 콘텐츠를 씻어 낸다. G에는 광변색 렌즈와 자동 밝기가 있고, HoloLens 2용 Trimble HoloTint는 "자외선과 주변광에 따라 색조를 자동으로 조절한다".
- **추적.** 인사이드아웃 추적에는 무늬와 빛이 필요한데, 짓고 있는 파사드는 유리, 반복되는 패널, 바뀌는 기하를 내놓는다([[04-robotics/state-estimation-slam|3 §7.2]]가 VIO의 실패를 나열한다). G의 위치는 폰에서 오는 $5$–$50\,\mathrm m$로, S1 공차의 천 배에서 만 배다. 철골 근처의 나침반 방위는 믿기 전에 시험해야 한다.
- **먼지, 장갑, 소음.** 먼지는 다른 리그처럼 렌즈와 카메라를 덮고([[04-robotics/perception-sensors-rigs|3.6 §7]]), 장갑은 손 추적의 외형 모델을 바꾸며([[04-robotics/egocentric-perception|22 §6]]), G와 Q의 입력은 맨손, 터치패드, 손목 밴드를 가정한다.
- **경보.** 시각 경보는 작업과 경쟁하고, 소리는 공구와 경쟁하며, 장갑을 통한 진동은 제 물리를 가진다([[06-research-practice/psychophysics-human-measurement|8. 심리물리 §5]]). 헤드셋이 추정하는 무엇에든 [[05-construction-robotics/hrc-worker-centered|6 §8]]의 작업자 상태 규칙이 적용된다.
- **사생활.** 착용형 카메라는 동의하지 않은 동료를 기록한다. Meta의 AI 안경은 "갤러리용으로 콘텐츠를 촬영할 때" 캡처 LED가 깜박이고, 가리면 카메라가 꺼진다. Project Aria에는 녹화 LED와 현재 녹화를 지우는 사생활 스위치가 있다. Quest의 카메라 영상은 Meta 정책상 Device User Data다. 어느 것도 현장 규약과 윤리 승인을 대신하지 않는다([[04-robotics/egocentric-perception|22 §6]]).

**함정.** HoloLens 위의 실험실 결과는 현장의 증거가 아니다. 위의 유일한 현장 결과는 헤드셋 대신 화면을, 정합된 홀로그램 대신 추적된 물체를 골랐고, 벽돌 한 장에 세 배의 시간을 치렀다.

### 8. 인간 요인

*한 문장으로:* 헤드셋은 착용자에게 편안함, 시야, 무게, 배터리, 주의를 치르게 하고, 그 가운데 일부에만 숫자가 있다.

**문제.** 연구에서 20분 도는 기기는 한 교대 내내 돌아야 한다. 쓰는 사람은 무엇을 치르는가?

**사이버멀미.** Stauffert, Niebling, Latoschik(2020)의 리뷰가 증거를 모은다. 지연은 사이버멀미를 키우고, 일정한 지연뿐 아니라 가끔 튀는 값도 그것을 일으키며, 사람은 $17\,\mathrm{ms}$ 아래의 지연도 알아챈다. 자주 인용되는 실무자의 권고는 $20\,\mathrm{ms}$ 아래다. 리뷰가 인용하는 집계에서 실험 $76$개 가운데 $58$개($76\%$)가 멀미를 Simulator Sickness Questionnaire로 쟀다. 리뷰가 나열하는 설명 가운데 첫째는 감각 불일치다. 눈은 움직임을 알리는데 전정계는 그렇지 않다. X1에서 §3의 예측은 편안함을 위한 조치이기도 하다. 머리가 도는 동안 렌더링된 세계를 붙잡아 두기 때문이다. VST 헤드셋은 예측으로 없앨 수 없는 불일치를 더한다. 로봇 자신의 움직임은 카메라 영상 안에서 $\tau_{\mathrm{pt}}=40\,\mathrm{ms}$ 늦게 눈에 닿아, 작업자가 듣는 것보다, 지지 단계에서는 패널을 통해 손으로 느끼는 것보다 뒤처진다.

**시야.** Q는 시야 전체를 $110^\circ\times96^\circ$ 디스플레이로 바꾸므로 그 밖의 모든 것, 옆에서 다가오는 로봇까지 사라진다. 그것을 보려면 작업자는 고개를 돌려야 하는데, 고개를 돌리는 순간이 바로 §3의 예산이 가장 나쁜 때다. G는 자연 시야를 그대로 두고 한쪽에 $14.3^\circ$ 패널을 더한다.

**8시간 교대에 맞선 무게와 배터리.** Q는 $515\,\mathrm g$에 평균 $2.2\,\mathrm h$(생산성 용도는 $1.5\,\mathrm h$)라 한 교대가 $3.6$번, 생산성 기준으로는 $5.3$번의 충전이다. G는 $69\,\mathrm g$로 $7.5$배 가볍고 혼합 사용 최대 $6\,\mathrm h$, $1.3$번이다. HoloLens 2는 $566\,\mathrm g$에 $2$–$3\,\mathrm h$, Apple Vision Pro는 $750$–$800\,\mathrm g$에 $2.5\,\mathrm h$다. RealWear는 배터리를 켠 채 바꿀 수 있게 했다.

**주의와 신뢰.** 머리 고정 패널은 흘끗 보기를 치르고, 월드 고정 콘텐츠는 초점 이동을, 틀렸을 때는 신뢰를 치른다 — §4의 사용자들은 조이스틱을 더 믿을 만하다고 느꼈다. 산업 조립에서 HoloLens에 대한 주관 평가(§4)와 현장 팀의 화면 선택(§7)이 같은 쪽을 가리킨다. 위의 어느 연구도 이 비용을 한 교대에 걸쳐 재지 않았으므로 여기서는 정성적으로만 말한다.

### 9. 연구 지형

*한 문장으로:* 이 분야는 다섯 흐름으로 흐른다 — 의도 전달, 명령·교시용 AR/VR 인터페이스, 로봇 학습용 1인칭 데이터, 건설 현장의 XR, 인간 요인과 안전 — 그리고 증거는 거의 모두 실험실 단에 있다.

**지도 읽는 법.** 각 행은 저자, 발표처와 연도, 보인 것, 그리고 [[05-construction-robotics/site-engineering|2.5 §5]]의 증거 단 — 시뮬레이션, 실험실, 실물 크기 목업, 가동 중인 현장 — 을 적었고, 각 단이 허락하는 말은 [[06-research-practice/real-world-impact|6. 실세계 임팩트 §2]]가 말한다. 모든 연구는 출판사, arXiv, 프로젝트 페이지에서 열어 확인했다(출처).

| 흐름 | 연구 | 발표처, 연도 | 보인 것 | 증거 단 |
|---|---|---|---|---|
| 의도 | Rosen, Whitney, Phillips, Chien, Tompkin, Konidaris, Tellex | ISRR 2017, IJRR 2019 | MR 헤드셋 팔 동작 미리 보기: 정확도 +16%, 시간 −62%, $n=32$ | 실험실 |
| 의도 | Walker, Hedayati, Lee, Szafir | HRI 2018 | AR 드론 비행 경로가 사용자를 더 효율적으로 | 실험실 |
| 의도 | Hietanen, Pieters, Lanz, Latokartano, Kämäräinen | *RCIM* 63, 2020 | HoloLens와 프로젝터 UI: 과제 시간 −21–24%, 로봇 유휴 −57–64%, HoloLens는 부적합 판정 | 실험실, 산업 과제 |
| 의도 | Chan, Hanks, Sakr, Zhang, Zuo, Van der Loos, Croft | *ACM THRI* 11(3), 2022 | $n=26$에서 AR 대 조이스틱: 신체 부담 감소, 시간 단축, 로봇 활용 증가 | 실험실, 산업 과제 |
| 명령·교시 | Zhang 등 | ICRA 2018 | VR 원격조작에서 심층 모방 학습으로 | 실험실 |
| 명령·교시 | Iyer 등(OPEN TEACH) | arXiv 2024 | Quest 3 원격조작 최대 90 Hz, 과제 38개, 정책 87%(과제 10개) | 실험실 |
| 명령·교시 | Cheng 등(Open-TeleVision) | CoRL 2024 | 능동적 입체 시각을 갖춘 몰입형 원격조작, Vision Pro와 Quest 3 | 실험실 |
| 명령·교시 | Chen, Wang, Nguyen, Fei-Fei, Liu(ARCap) | ICRA 2025 | AR·햅틱 피드백이 있는 로봇 없는 시연 | 실험실 |
| 1인칭 | Kareer 등(EgoMimic) | ICRA 2025 | Aria 사람 데이터와 로봇 데이터 공동 학습 | 실험실 |
| 1인칭 | Liu 등(EgoZero) | arXiv 2025 | 로봇 데이터 0, 과제 7개에서 70% | 실험실 |
| 1인칭 | Hoque 등(EgoDex) | ICLR 2026 | 손 자세가 붙은 Vision Pro 영상 829 h | 데이터셋 |
| 1인칭 | Punamiya 등(EgoVerse) | arXiv 2026 | 1,362 h, 여러 실험실에서 전이 재현 | 실험실, 여러 곳 |
| 건설 | Mitterberger 등 | *Construction Robotics* 4, 2020 | 물체 인식형 AR 벽돌 쌓기: 국부 ±5 mm, 벽돌 13,596장 | 가동 중인 현장 |
| 건설 | Kyjanek, Al Bahar, Vasey, Wannemacher, Menges | ISARC 2019 | 목조 프리패브에서 HoloLens로 로봇 궤적 계획 | 실험실 |
| 건설 | Wang, Liang, Menassa, Kamat | ISARC 2020 | VR 디지털 트윈: 계획, 승인, 실행, 석고보드 | 실험실 |
| 건설 | Park, Menassa, Kamat | *J. Comput. Civ. Eng.* 39(1), 2025 | 대형 언어 모델 대화가 붙은 VR 인터페이스, 건설 작업자 12명 | 시뮬레이션(VR) |
| 인간 요인 | Stauffert, Niebling, Latoschik | *Front. Virtual Real.* 1, 2020 | 지연과 사이버멀미: 튀는 값이 중요, SSQ가 76% | 리뷰 |
| 인간 요인 | OptoFidelity | 벤치마크, 2024 | 패스스루 11 ms(Vision Pro) 대 35–40 ms(Quest 3) | 벤치 측정 |

**이 공동체가 발표하는 곳.** ACM/IEEE Human-Robot Interaction 학회와 그 워크숍인 Virtual, Augmented, and Mixed-Reality for Human-Robot Interactions(VAM-HRI) — 아홉 번째가 HRI 2026에서 열렸고 2018년부터 해마다 열렸다. 25회가 2026년 10월 5–9일 바리에서 열리는 IEEE ISMAR, 33회인 2026년 대회가 처음 한국 대구에서 열린 IEEE VR. HCI 학회 CHI와 저널 *ACM Transactions on Human-Robot Interaction*(THRI) — 아래 두 서베이와 의도 연구 한 편이 여기 실렸다 — 그리고 원격조작·1인칭 연구가 실리는 로봇 학습 학회들(ICRA, CoRL, ICLR, CVPR). 2024년부터 CVPR에서 열리는 Joint Egocentric Vision(EgoVis) 워크숍. 건설 쪽은 43회가 2026년 6월 22–26일 싱가포르에서 열린 ISARC와, 저널 *Construction Robotics*, *Journal of Computing in Civil Engineering*. 두 서베이가 분야를 지도로 그린다. Suzuki, Karim, Xia, Hedayati, Marquardt(CHI 2022)는 AR과 로보틱스 논문 $460$편을 분류하고, Walker, Phung, Chakraborti, Williams, Szafir(*ACM THRI* 12(4), 2023)는 VAM-HRI의 가상 디자인 요소 분류 체계를 제안한다. 워크숍에 논문을 보내기 전에 [[06-research-practice/venue-strategy|5. 발표처 전략 §6]]을 읽어라.

**학위논문이 맡을 수 있는 열린 문제.** 위 지도에 대한 이 페이지의 읽기이지, 부재를 검증한 서베이가 아니다.

- **건설 공차에서의 정합.** 읽은 초록과 페이지 가운데 과제 결과 옆에 홀로그램의 정합 오차를 적은 것은 없고, 유일한 ±5 mm 현장 결과는 물체를 추적했다. 헤드셋이 현장에서 S1의 패널과 브래킷을 직접 재어, 앵커 항 없이 §3의 예산을 닫을 수 있는가?
- **움직이는 건설 로봇 옆의 의도 디스플레이.** §4의 의도 연구는 팔 로봇과 드론으로 한 실험실 연구다. S1의 통로나 지지에서의 연구라면 먼지, 장갑, 소음 아래에서 알아챔과 반응 시간을 재고, 안전 기능은 그대로 둔다(§4의 규칙).
- **기계 옆의 VST.** Q를 쓴 작업자는 움직이는 로봇을 패스스루로 $40\,\mathrm{ms}$(강의용 숫자) 늦게 본다. 그것이 움직이는 베이스 옆 사람의 타이밍에 무엇을 하는지 잰 연구는 이 지도에 없다.
- **하중과 보호구가 있는 1인칭 시연.** 위의 1인칭 데이터셋은 모두 맨손 탁상 작업이다. S1처럼 장갑을 끼고, 무겁고, 두 사람이 하는 과제라면 머리와 손 자세에 더해 힘이 필요하다.
- **지지 단계를 위한 부담 낮은 채널.** G는 정합할 수 없지만, $69\,\mathrm g$ 기기로 다음 단계와 로봇 상태를 전할 수 있다. 현장에서 소리, 진동과 비교해 흘끗 보는 시간과 반응 시간을 재는 것은 이 주인의 기기로 할 수 있는 인간 요인 연구다.

### 10. 실습

영어 절의 목록은 §3의 예산을 X1에서 돌리고, 거리·머리 속도·지연에 대해 쓸어 보고, 머리 회전을 $1\,\mathrm{kHz}$로 예측 있이·없이 한 걸음씩 밟고, 각 주인공 기기가 무엇을 보여 주는지 출력한다. 결정론적이고 NumPy만 쓴다. 코드는 영어 절에 한 번만 싣는다.

**출력.** Part 1, $D=1.5\,\mathrm m$에서의 예산(mm):

| 지연 | 머리 속도 | 지연 항 | 선형 합 | 정적 항의 RSS + 지연 |
|---|---:|---:|---:|---:|
| — | 정지 | 0.00 | 7.40 | 3.75 |
| 5 ms | 30 °/s | 3.93 | 11.33 | 7.68 |
| 5 ms | 90 °/s | 11.78 | 19.18 | 15.54 |
| 5 ms | 300 °/s | 39.27 | 46.67 | 43.02 |
| 20 ms | 30 °/s | 15.71 | 23.11 | 19.46 |
| 20 ms | 90 °/s | 47.12 | 54.53 | 50.88 |
| 20 ms | 300 °/s | 157.08 | 164.48 | 160.83 |

Part 2, 홀로그램을 각 대역 안에 두는 가장 빠른 머리 회전(°/s), 선형 읽기 / RSS 읽기:

| $D$ | ±5 mm, 5 ms | ±5 mm, 20 ms | 50 mm, 5 ms | 50 mm, 20 ms |
|---|---:|---:|---:|---:|
| 0.5 m | never / 33 | never / 8 | 996 / 1065 | 249 / 266 |
| 1.0 m | never / 16 | never / 4 | 493 / 531 | 123 / 133 |
| 1.5 m | never / 10 | never / 2 | 325 / 353 | 81 / 88 |
| 2.0 m | never / 6 | never / 2 | 242 / 264 | 60 / 66 |
| 3.0 m | never / 2 | never / 1 | 158 / 174 | 39 / 44 |

Part 3, [[04-robotics/modern-robotics/ch09-trajectory-generation|MR 9장 §1]]의 5차 곡선으로 $0.5\,\mathrm s$에 $60^\circ$ 도는 회전(최고 $225$ °/s, 최고 $1386$ °/s²): $\tau=20\,\mathrm{ms}$에서 옛 자세로 그리면 $4.495^\circ$, $D$에서 $117.9\,\mathrm{mm}$ 뒤처진다. 일정 속도 예측은 머리가 빨라지는 동안 $0.277^\circ$, $7.2\,\mathrm{mm}$ 뒤처지고, 느려지는 동안 같은 만큼 앞선다. $\tau=40\,\mathrm{ms}$에서는 둘이 $236.5$와 $28.8\,\mathrm{mm}$가 된다. Part 4는 §2, §3, 계산 절이 인용한 기기 숫자들과, $0.1\,\mathrm m$ 걸음에 대한 $3.8^\circ$를 출력한다.

**가져갈 것.**

- **±5 mm는 멈춘 머리와 너그러운 규칙에서만 나온다.** 선형 읽기로는 어느 거리에서도 닿지 않고, RSS 읽기로도 $0.5\,\mathrm m$에서 최대 $33$ °/s까지만 견딘다.
- **예측이 거친 대역을 산다.** $1.5\,\mathrm m$에서 $50\,\mathrm{mm}$ 한계를 $81$에서 $325$ °/s로 올린다.
- **거리는 두 번 치른다.** $D$가 머리 방향 항과 지연 항을 모두 곱하므로, $1.0$에서 $2.0\,\mathrm m$로 물러서면 대역이 허락하는 머리 속도가 반이 된다.
- **예측은 회전의 양 끝에서 실패한다.** 남는 오차가 가속도를 따르므로 홀로그램은 머리가 빨라질 때 뒤로, 느려질 때 앞으로 헤엄친다. 지연을 두 배로 하면 네 배, $7.2$에서 $28.8\,\mathrm{mm}$가 된다.

### 읽고 나면 말할 수 있어야 하는 것

다음을 할 수 있어야 한다.

- 현실 세계가 눈에 닿는 방식과 추적하는 것으로 기기를 §1의 여섯 부류 가운데 하나에 넣고, 그 부류가 무엇을 보여 줄 수 있고 없는지 말하기;
- Q와 G에 대해 개발자가 무엇을(머리, 손, 눈, 카메라, 깊이, 소리) 어떤 권한과 규칙 아래 읽을 수 있는지 나열하기;
- HMD의 IMU는 수백 헤르츠로, 카메라는 수십 헤르츠로 재는 이유 설명하기;
- 이름 붙인 점에서 홀로그램의 정합 예산을 각 회전의 지렛대와 함께 쓰고, 지연을 왜 선형으로 더하는지 말하기;
- 마커와 PnP로 헤드셋의 세계를 로봇 베이스에 맞추고, 조심할 것 세 가지를 들기;
- 월드 고정 AR이 S1에서 무엇을 안내할 수 있고 없는지, 그리고 머리 고정 패널이 대신 무엇을 할 수 있는지 숫자로 말하기;
- 다섯 연구 흐름마다 두 연구의 발표처, 보인 것, 증거 단을 요약하기.

### 스스로 점검

1. 한 논문이 "정확도를 16% 높인 AR 인터페이스"를 보고한다. G와 비교하기 전에 기기에 대해 알아야 할 두 가지는?
2. X1의 홀로그램은 머리가 멈춰도 $7.40\,\mathrm{mm}$ 어긋난다. 그 가운데 앵커의 몫을 반으로 줄이는 변화 하나는 무엇이고, 그 대가는?
3. 작업자의 머리가 완전히 멈춰 있어도 VST 헤드셋이 움직이는 로봇을 늦게 보여 주는 이유는?
4. G는 영상을 폰으로 보낼 수 있다. 그 영상이 아직 로봇 시연이 아닌 이유는?
5. 일정 속도 예측은 회전의 시작에서 $7.2\,\mathrm{mm}$를 남긴다. 일정한 회전의 한가운데서 0이 되는 이유는?

> [!tip]- 정답
> 1. 현실 세계가 눈에 직접 닿는가 카메라를 거치는가(OST인가 VST인가), 그리고 콘텐츠가 월드 고정이었나 머리 고정이었나 — 더해 정확도를 잰 거리와 머리 속도. G는 OST이고 머리 고정이므로 월드 고정 결과는 G에 대해 아무것도 말하지 않는다.
> 2. 앵커를 구멍 가까이 옮긴다. 회전 항은 $L\,\delta\theta_A$이니 $L$을 $1.2$에서 $0.6\,\mathrm m$로 반으로 줄이면 $2.09$에서 $1.05\,\mathrm{mm}$가 된다. 대가는 작업 옆의 마커인데, 작은 마커는 기울기 추정이 약해(3.5 §2.7) $\delta\theta_A$가 커질 수 있다. 과제가 이를 보여 준다.
> 3. 시야 전체가 영상이고, 카메라 프레임마다 그것이 보여 주는 순간보다 $\tau_{\mathrm{pt}}$ 뒤에 디스플레이에 닿기 때문이다. 그동안 로봇은 움직인다. $0.5\,\mathrm{m/s}\times40\,\mathrm{ms}=20\,\mathrm{mm}$. 지연이 머리가 아니라 장면의 것이므로 머리 예측으로 없앨 수 없다.
> 4. 머리나 손의 자세가 없어 행동을 복원·리타기팅할 수 없고($a_t=\rho(h_t,T_{WH})$에는 둘 다 필요), 초당 최대 $30$ 프레임으로 압축되어 오며, 힘을 싣지 않는다. 1인칭 영상일 뿐이고, 자세 추정기와 동의 규약을 갖춰야 1인칭 학습 데이터가 된다.
> 5. 일정 속도 외삽의 남는 오차는 약 $\tfrac12\dot\omega\tau^2$다. 일정한 회전에서는 $\dot\omega=0$이라 현재 속도로 외삽하면 참 각에 정확히 닿는다. 오차는 속도가 바뀌는 동안, 곧 회전의 시작과 끝에서만 나타난다. 그런데도 X1이 모든 머리 속도에 $\tau_{\mathrm{eff}}=5\,\mathrm{ms}$를 매기는 것은, 실제 머리의 속도는 계속 바뀌고 외삽하는 속도 자체가 잡음 섞인 추정값이기 때문이다(§3).

### 과제 · Problem set

Tier A. 이 페이지, 선수 페이지, X1만 쓴다. 작업자가 패널 전체를 보려고 물러서서 눈이 T에서 **2.5 m**에 있다. 앵커는 T에서 **0.3 m** 떨어진 브래킷의 작은 마커로 다시 만들었고, 위치 오차는 **1.5 mm**이고, 회전 오차는 마커가 작아서 크다: **0.30°**. 머리 추적은 그대로다. 앱이 무거워져 예측 뒤 **8 ms**가 남고, 예측이 없으면 여전히 $20\,\mathrm{ms}$다. 이것을 **X1′**(X1 프라임)이라 부른다.

1. **그리기(Draw).** X1′에 대해 그림의 두 판을 다시 그린다 — 새 $D$와 브래킷의 앵커를 넣은 평면도, 새 거리에서 축척대로 그린 G의 $14.3^\circ$ 패널, 그리고 $8\,\mathrm{ms}$에서 $30$과 $90$ °/s, $20\,\mathrm{ms}$에서 $90$ °/s의 예산 막대를 $\pm5$와 $50\,\mathrm{mm}$ 선과 함께.
2. **유도(Derive).** X1′에 대해: (a) 네 정적 항과 선형·RSS 합, (b) $8\,\mathrm{ms}$에서 $30$과 $90$ °/s의 지연 항과 선형 합, (c) 선형 합을 $50\,\mathrm{mm}$ 안에 두는 가장 빠른 머리 회전을 $8$과 $20\,\mathrm{ms}$에서, (d) $2.5\,\mathrm m$에서 정면으로 본 G 패널의 너비와 $0.3\,\mathrm m$ 걸음의 방위 변화, (e) 새 앵커가 항별로 도움이 되었는지.
3. **실행(Do).** 영어 절의 템플릿에서 빈칸을 채워 돌리고 정답과 비교한다. 그다음 지연이 두 배가 될 때 일정 속도·일정 가속도 예측의 남는 오차가 어떻게 커지는지, 그것이 $40\,\mathrm{ms}$ 앞을 예측해야 하는 파이프라인에 무엇을 뜻하는지 말한다.

> [!note]- 그리는 법 · How to draw it
> - **축척대로 그린 평면도**: 벽, $400\,\mathrm{mm}$ 떨어진 두 구멍이 있는 패널, T, 주어진 거리의 눈 H, 지금 앵커가 있는 곳의 마커를 그리고, 선 위에 $D$와 $L$을 적는다.
> - **세 좌표계**: 추적이 시작된 곳의 W, 머리의 H, 로봇의 B, 그리고 W에서 나가는 연결로 그린 앵커 $T_{WB}$와 머리 자세 $T_{WH}$.
> - **H에서 본 두 기기의 시야**: Q의 $110^\circ$ 쐐기와 G의 $14.3^\circ$ 쐐기. G의 쐐기는 벽까지 이어 덮는 폭을 읽을 수 있게 한다.
> - **T에서의 예산을 쌓은 막대**로, 머리 속도와 지연마다 한 줄, 막대마다 머리 위치, 머리 방향, 앵커 위치, 앵커 회전, 지연으로 나누어 한 축척으로 그린다.
> - **세로선 둘**: S1의 $\pm5\,\mathrm{mm}$와 $50\,\mathrm{mm}$ 대역. 막대마다 판정을 계산하지 않고 읽을 수 있게.
> - **합계는 오른쪽 한 열에**, 어느 글자도 선을 가로지르지 않게.

> [!tip]- 정답 · Solutions
> 1. 평면도에서 H는 T에서 $2.5\,\mathrm m$, 마커는 브래킷 위 T에서 $0.3\,\mathrm m$에 있어 앵커의 지렛대가 X1의 4분의 1이다. G의 쐐기는 이제 정면 $0.627\,\mathrm m$를 덮는다. 모든 막대의 정적 부분은 $7.40$에서 $7.25\,\mathrm{mm}$로 조금 줄어드는데, 머리 항은 커지고 앵커 항은 작아졌기 때문이다. 지연 부분은 같은 머리 속도에서 $2.5/1.5\times8/5=2.67$배 커진다.
> 2. (a) 머리 위치 $2.00$, 머리 방향 $2500\times0.05\times\pi/180=2.18$, 앵커 위치 $1.50$, 앵커 회전 $300\times0.30\times\pi/180=1.57\,\mathrm{mm}$. 선형 $7.25$, RSS $3.67\,\mathrm{mm}$. (b) $D\,\omega\,\tau=2500\times0.524\times0.008=10.47\,\mathrm{mm}$($30$ °/s, 곧 $0.524\,\mathrm{rad/s}$), 합 $17.72\,\mathrm{mm}$. $90$ °/s에서 $31.42\,\mathrm{mm}$, 합 $38.67\,\mathrm{mm}$ — 둘 다 $50$ 안, $\pm5$에서는 한참 밖. (c) $(50-7.25)/(2500\times0.008)=2.14\,\mathrm{rad/s}=122.5$ °/s($8\,\mathrm{ms}$), $20\,\mathrm{ms}$에서는 걷기보다 느린 $49.0$ °/s. (d) $2\times2.5\times\tan7.14^\circ=0.627\,\mathrm m$. $\arctan(0.3/2.5)=6.84^\circ$로 X1의 $11.3^\circ$보다 작은데, 같은 걸음이 먼 곳에서는 작은 각이기 때문이다. 그래도 구멍을 표시하기에는 턱없이 크다. (e) 앵커 회전 항은 각이 세 배가 되었는데도 지렛대가 4분의 1로 줄어 $2.09$에서 $1.57\,\mathrm{mm}$로 줄었고, 위치 항은 $0.5\,\mathrm{mm}$ 줄었다. 머리 방향 항은 거리와 함께 $1.31$에서 $2.18\,\mathrm{mm}$로 커졌다.
> 3. 빈칸: `L * 1e3 * TH_A * RAD`, `D * 1e3 * w * RAD * TAU`, `np.gradient(om, dt)`, `0.5 * acc[:-k] * tau**2`. 출력: 선형 $17.72$와 $38.67\,\mathrm{mm}$, RSS와 지연 $14.14$와 $35.09\,\mathrm{mm}$, 가장 빠른 회전 $122.5$ °/s. $20\,\mathrm{ms}$에서 일정 속도 예측의 남는 오차는 $0.2767^\circ$, 일정 가속도는 $0.0357^\circ$($1.5\,\mathrm m$에서 $7.2$와 $0.93\,\mathrm{mm}$), $40\,\mathrm{ms}$에서는 $1.1015^\circ$와 $0.2680^\circ$다. 지연을 두 배로 하면 일정 속도 오차는 $\tau^2$처럼 $4.0$배, 일정 가속도 오차는 $\tau^3$의 $8$에 가까운 $7.5$배가 된다. $40\,\mathrm{ms}$ 앞을 예측하려면 가속도 항이 필요하고, 그 가속도는 잡음 많은 자이로를 미분해서 얻는다 — 여기에는 없는 그 잡음이 고차 예측의 대가다.

### 출처

모든 페이지는 2026-09-23에 열었다. 제품 정보는 바뀌므로 숫자를 다시 쓰기 전에 제조사 페이지를 다시 읽어라. 전체 목록과 링크는 영어 절의 Sources에 있다.

- **정의와 표준**: Skarbez, Smith, Whitton 2021(Milgram과 Kishino 1994의 인용; 원 페이지는 봇 확인 뒤에 있어 열지 않음), W3C WebXR Device API(2026년 6월 9일 CR 초안), Khronos OpenXR 명세와 개요.
- **주인공 기기(Meta 페이지)**: Meta Quest 3 기술 사양, Meta 개발자 블로그(2023년 6월 1일), Passthrough Camera API 개요와 Unity 안내, 손 추적 세 페이지, Depth API 개요, 공간 앵커 모범 사례, Meta Ray-Ban Display 블로그·뉴스룸·제품 페이지, Wearables Developer Center(툴킷 개요, 통합 개요, 디스플레이 접근, Android 통합, 버전 의존성, 웹 앱과 Build), Ray-Ban Meta(Gen 2) 뉴스룸, AI 안경 질의응답(캡처 LED).
- **다른 기기**: Apple Vision Pro 사양, Microsoft Learn(HoloLens 2 하드웨어, 릴리스 노트, Trimble XR10), Magic Leap 판매 약관과 디머 문서, RealWear Navigator 520 사양과 보도자료, Project Aria 안경 페이지와 Aria Gen 2 블로그.
- **측정과 인간 요인**: OptoFidelity 벤치마크 두 편(2024년 2월), Stauffert, Niebling, Latoschik 2020.
- **연구**: 의도 전달(Rosen 등, Walker 등, Hietanen 등, Chan 등), 명령과 교시(Zhang 등, OPEN TEACH, Open-TeleVision, ARCap, Kyjanek 등, Wang 등, Park 등), 1인칭 데이터(Project Aria, EgoMimic, EgoZero, EgoDex, HOT3D, EgoVerse, Ego-Pi), 건설(Mitterberger 등), 서베이(Suzuki 등, Walker 등), 발표처(VAM-HRI, ISMAR, IEEE VR, EgoVis, ISARC).
- **이 위키 안**: [[04-robotics/egocentric-perception|22. 1인칭 인식]](E1, 머리 속도의 출처 Grossman 등 1988) · [[04-robotics/human-pose-gaze|21. 사람 자세·손·시선]] · [[04-robotics/human-intent-prediction|23. 사람 의도]] · [[04-robotics/hri-safety|11. HRI·안전]] · [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연]] · [[04-robotics/perception-sensors-rigs|3.6 인식 센서]] · [[04-robotics/geometric-perception-calibration|3.5 기하 인식]] · [[05-construction-robotics/site-engineering|2.5 현장 로보틱스]](S1) · [[05-construction-robotics/hrc-worker-centered|6. HRC]] · [[05-construction-robotics/imitating-contact|10. 접촉 모방]] · [[03-deep-learning/vla/index|4. VLA]]
