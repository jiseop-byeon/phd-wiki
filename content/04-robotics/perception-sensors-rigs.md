---
title: "3.6 Perception Sensors and Rigs: Cameras, Depth, LiDAR, Radar and Synchronisation"
tags: [robotics, perception, sensors]
study-depth: Working
wiki-support: Working
depth-goal: "On 3.5's wrist rig carried past S1's facade, turn each sensor's physics into an error at the panel — a pixel's SNR and the scene's dynamic range, motion blur and rolling-shutter skew, stereo σ_Z, a time-of-flight wrap, a LiDAR's footprint and spacing, a radar's range cell, an extrinsic error in pixels, and v·Δt for every wrong time stamp — and choose sensors for site conditions from those numbers."
mastery-when: "Raise to Mastery when a sensor rig's design, calibration or synchronisation carries the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> Plants **P2**, **P5** and **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] · the Tier A lab conventions of [[02-foundations/lab-kernel|0.7 Lab Kernel]] · the wrist rig of [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] (§1 the pinhole model and distortion, §2 depth from disparity, §3 frames, §5 calibration) · the noise models of [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] (§1 the measurement model, §4 quantization, §5 the range sensor and the camera) · [[04-robotics/state-estimation-slam|3. State Estimation]] (§7.2 deskewing, §8 fusion) · variances of independent errors from [[02-foundations/probability|3. Probability §2]] · quantization and the DFT's bin spacing from [[02-foundations/signal-processing|6. Signal Processing §2 and §3]] · rigid transforms from [[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §3]]
> [[02-foundations/lab-plants|0.6]]의 장치 **P2**, **P5**, **P6** · [[02-foundations/lab-kernel|0.7]]의 Tier A 실습 규약 · [[04-robotics/geometric-perception-calibration|3.5 기하 인식과 보정]]의 손목 리그(§1 핀홀 모델과 왜곡, §2 시차에서 깊이, §3 프레임, §5 보정) · [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]의 잡음 모델(§1 측정 모델, §4 양자화, §5 거리 센서와 카메라) · [[04-robotics/state-estimation-slam|3. 상태 추정]](§7.2 deskewing, §8 융합) · [[02-foundations/probability|3. 확률 §2]]의 독립 오차의 분산 · [[02-foundations/signal-processing|6. 신호처리 §2와 §3]]의 양자화와 DFT 빈 간격 · [[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §3]]의 강체 변환

## English

*Stands on [[04-robotics/geometric-perception-calibration|3.5]], which turns pixels into rays, depths and frames, and [[04-robotics/sensor-models|3.2]], which writes each sensor as $z=h(x)+b+n$. Both take the measurement as given. This page opens the sensor: how photons in a well, a pulse's flight time, a chirp's beat and a clock's reading become a measurement, and where that physics makes it fail. A later use of **P2**, **P5** and **P6**.*

> [!note] Why this matters · 왜 배우는가
> This page is the first layer of the physical-AI stack in [[07-research-program/index|7. Research Program §5]], perception, beneath object and scene understanding; in *"Install that panel on the frame"* it is the sensing under identifying the panel and the frame, and under seeing the contact (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it a rig's numbers are taken on trust, and on a moving base they fail before any algorithm runs: at $0.5\,\mathrm{m/s}$ a camera stamped at the end of its readout puts the panel $8.5\,\mathrm{mm}$ off and a LiDAR cloud's single stamp $23\,\mathrm{mm}$, both past S1's $\pm5\,\mathrm{mm}$, and to a single-return LiDAR a saw's dust is a wall. The same physics returns in [[05-construction-robotics/site-perception|5. Site Perception §1]] (a scan's spacing and point error), [[04-robotics/capstone-panel-contact|26. Capstone §5]] (a delay as a staleness distance), [[04-robotics/ros2/from-simulation-to-hardware|25.11 §4–§5]] (the drivers and clocks that stamp the data) and [[05-construction-robotics/imitating-contact|10. Imitating Contact §1]], whose learned policy sees the hole only through a camera's $0.5\,\mathrm{mm}$; on the dissertation path ([[07-research-program/index|7. Research Program §8]]) it belongs to block 2, the robotics common track. After it you can turn any sensor on a moving site rig into millimetres of error at the panel, and give each sensor the job its physics allows.

> [!note] First pass · 처음이라면
> Two sittings. **Sitting 1 — the camera and time.** Read the Running object and find in the picture each error's size at the facade — the $39\,\mathrm{mm}$ stereo bar, the $16\,\mathrm{mm}$ LiDAR spots, the $5\,\mathrm{mm}$ blur, the $23\,\mathrm{mm}$ stamp error — before you know where they come from. Then read §1–§3 and §9 and work steps 1, 2 and 5 of the Worked case by hand; self-check 1, the exposure window at $1\,\mathrm{m/s}$, closes the sitting. **Sitting 2 — the LiDAR and the ledger.** Read §5, say at what range the LiDAR beats stereo and why the answer is a square root, work step 3 and the ledger, then run §10 and read its five bullets. §4 (depth cameras), §6 (radar), §7 (the site table, to carry to a site) and §8 (extrinsics) come on a second pass, or when a paper or a site uses those sensors; the problem set closes that pass.

### Running object · 이 페이지의 대상

**The rig.** Put **P2**, with 3.5's wrist rig on its tool, on the mobile base of the construction track's facade-panel task S1 ([[05-construction-robotics/site-engineering|2.5 Site Robotics]]; a forward pointer, not a prerequisite). Add a spinning LiDAR and an FMCW radar on the base's mast, and drive the base along the facade at $0.5\,\mathrm{m/s}$, $2.0\,\mathrm m$ from it, the cameras facing the facade. P2 stays parked for the whole pass, so the cameras and the mast's sensors keep one fixed geometry (§8). The landmark $L$ is a point on that facade. From other pages, unchanged:

| Object | Values | From |
|---|---|---|
| rig cameras 1 and 2 | $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, $640\times480$, $k_1=-0.20$, $k_2=+0.05$; camera 2 at $b=0.12\,\mathrm m$ along camera 1's $x$ | 3.5 |
| $L$; $A,B,C$; $d_{ct}$ | $(0.5,\ 0.2,\ 2.0)\,\mathrm m$; $(0,0,2)$, $(0.5,0,2)$, $(0,0.4,2)\,\mathrm m$; $0.04\,\mathrm m$ | 3.5 |
| P6's camera | $f_x=600$ px at $Z_c=1.0\,\mathrm m$, $\sigma_u=0.5$ px ($0.833\,\mathrm{mm}$), $50\,\mathrm{Hz}$; budget $70\,\mathrm{ms}$ from mid-exposure to force | 3.2; **P6** |
| P5's range sensor | $\sigma_r=10\,\mathrm{mm}$, offset $b_r=4\,\mathrm{mm}$; P5 reads $12\,\mathrm{cm}$ | 3.2; **P5** |

The rest is this page's own, frozen as **course numbers for clean arithmetic, not any product's datasheet**:

| Object | Values |
|---|---|
| each camera's pixel | pitch $6.0\,\mathrm{\mu m}$ (so the lens is $f=3.6\,\mathrm{mm}$) at $f/2.0$ (aperture $1.8\,\mathrm{mm}$); full well $10{,}000\ e^-$, read noise $5\ e^-$, dark current $100\ e^-/\mathrm s$; a $10$-bit converter at $10\ e^-$ per step |
| the scene at $f/2$ | photoelectrons per pixel per ms: facade in shade $200$, in sun $2{,}000$, a glint (the low sun mirrored by a glazed panel) $2\times10^6$ |
| shutter and base | rolling shutter, $25\,\mathrm{\mu s}$ per row ($480$ rows in $12\,\mathrm{ms}$), $10\,\mathrm{ms}$ indoor exposure; base at $v=0.5\,\mathrm{m/s}$, facade at $Z=2.0\,\mathrm m$ from camera 1 |
| LiDAR | $32$ channels $1.0^\circ$ apart ($\pm15.5^\circ$), columns every $0.2^\circ$, $10\,\mathrm{Hz}$; range noise $\sigma_L=20\,\mathrm{mm}$; divergence $3.0\,\mathrm{mrad}$, exit beam $10\,\mathrm{mm}$; $0.30\,\mathrm m$ above camera 1, axes forward–left–up; the sweep starts facing backwards and turns left; one stamp per cloud, at its start |
| radar | FMCW at $77\,\mathrm{GHz}$, bandwidth $B=1.0\,\mathrm{GHz}$ in $T_c=50\,\mathrm{\mu s}$, $128$ chirps per frame, $5\,\mathrm{MHz}$ IF band, $3\times4=12$ virtual channels at $\lambda/2$; below the LiDAR |
| ToF camera; worker | modulation $100$ and $80\,\mathrm{MHz}$, phase noise $0.02\,\mathrm{rad}$; a worker walking at $1.6\,\mathrm{m/s}$, the speed [[04-robotics/hri-safety\|11. HRI & Safety]] takes from ISO 13855 |

Everything later is derived from these tables. One consistency check: the LiDAR sees $L$ at $(2.0,\ -0.5,\ -0.5)\,\mathrm m$ in its own frame, $2.121\,\mathrm m$ away, and carried through the mount and 3.5's $K$ it lands on pixel $(470,\ 300)$, where camera 1 sees it (§8).

*Scope: this page teaches how cameras, stereo pairs, depth cameras, LiDARs and radars form their measurements, their dominant errors at a stated range and speed, how a rig of them is calibrated and time-stamped as one instrument, and how to choose among them for a site. It does not teach the geometry that turns their outputs into 3D ([[04-robotics/geometric-perception-calibration|3.5]]), the noise models and filters that consume them ([[04-robotics/sensor-models|3.2]], [[04-robotics/state-estimation-slam|3]]), site point clouds ([[05-construction-robotics/site-perception|5. Site Perception]]) or sensor drivers ([[04-robotics/ros2/from-simulation-to-hardware|25.11 §4]]); §11 lists the rest.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 420" style="max-width:100%;height:auto" role="img" aria-label="Left, a plan view at 1 m = 100 px: the mobile base moving at 0.5 m/s along the facade 2 m away, camera 1 and camera 2 0.12 m apart with the LiDAR above camera 1, the camera's field of view, the landmark L on the facade with the stereo depth error of plus or minus 39 mm along the ray, the radar's 15 cm by 9.5 degree cell around L, a worker 0.30 m before the facade walking toward the rig at 1.6 m/s, and the LiDAR sweeping 120 degrees across the facade. Right, the facade around L face-on at 1 mm = 2 px: camera pixel footprints of 3.3 mm, LiDAR spots of 16 mm about 7.4 mm apart on rings about 38 mm apart, S1's 5 mm tolerance circle, motion blur of 5 mm at 10 ms and 1 mm at 2 ms, and the time-stamp errors of 8.5 mm and 23 mm.">
  <text x="16" y="20" font-size="12" fill="currentColor" font-weight="600">plan: the base passing the facade</text>
  <text x="302" y="20" font-size="12" fill="currentColor" font-weight="600">the facade around L, face-on</text>
  <line x1="16" y1="72.0" x2="284" y2="72.0" stroke="currentColor" stroke-width="2.2"/>
  <line x1="20" y1="72.0" x2="28" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="32" y1="72.0" x2="40" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="44" y1="72.0" x2="52" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="56" y1="72.0" x2="64" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="68" y1="72.0" x2="76" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="80" y1="72.0" x2="88" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="92" y1="72.0" x2="100" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="104" y1="72.0" x2="112" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="116" y1="72.0" x2="124" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="128" y1="72.0" x2="136" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="140" y1="72.0" x2="148" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="152" y1="72.0" x2="160" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="164" y1="72.0" x2="172" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="176" y1="72.0" x2="184" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="188" y1="72.0" x2="196" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="200" y1="72.0" x2="208" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="212" y1="72.0" x2="220" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="224" y1="72.0" x2="232" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="236" y1="72.0" x2="244" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="248" y1="72.0" x2="256" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="260" y1="72.0" x2="268" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="272" y1="72.0" x2="280" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="18" y="60.0" font-size="11" fill="currentColor">facade (S1's panel)</text>
  <line x1="130.0" y1="272.0" x2="23.3" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="4 3"/>
  <line x1="130.0" y1="272.0" x2="236.7" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="4 3"/>
  <line x1="130.0" y1="272.0" x2="180.0" y2="72.0" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <path d="M162.0 75.9 L164.4 61.1 A213.7 213.7 0 0 1 198.9 69.8 L194.1 84.0 A198.7 198.7 0 0 0 162.0 75.9 Z" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <line x1="196.5" y1="76.9" x2="204.0" y2="96.0" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.7"/>
  <text x="206" y="100" font-size="11" fill="currentColor">radar cell</text>
  <text x="206" y="113" font-size="11" fill="currentColor">15 cm × 9.5°,</text>
  <text x="206" y="126" font-size="11" fill="currentColor" fill-opacity="0.85">0.33 m wide here</text>
  <line x1="179.0" y1="75.9" x2="181.0" y2="68.1" stroke="currentColor" stroke-width="3.6"/>
  <circle cx="180.0" cy="72.0" r="3.0" fill="currentColor" stroke="none"/>
  <text x="165.0" y="87.0" font-size="12" fill="currentColor" font-weight="600">L</text>
  <line x1="181.0" y1="78.0" x2="204.0" y2="150.0" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.7"/>
  <text x="206" y="160" font-size="11" fill="currentColor">stereo ±39 mm</text>
  <text x="206" y="173" font-size="11" fill="currentColor" fill-opacity="0.85">along the ray</text>
  <circle cx="50.0" cy="102.0" r="15" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <line x1="57.2" y1="117.4" x2="67.9" y2="140.0" stroke="currentColor" stroke-width="1.4"/>
  <path d="M70.4 145.4 L65.4 141.2 L70.3 138.9 Z" fill="currentColor" stroke="none"/>
  <text x="18.0" y="166.0" font-size="11" fill="currentColor">worker 0.30 m before</text>
  <text x="18.0" y="179.0" font-size="11" fill="currentColor">the facade, 1.6 m/s</text>
  <path d="M169.8 249.0 L168.6 246.9 L167.2 245.0 L165.7 243.1 L164.2 241.2 L162.5 239.5 L160.8 237.8 L158.9 236.3 L157.0 234.8 L155.1 233.4 L153.0 232.2 L150.9 231.0 L148.7 230.0 L146.5 229.1 L144.2 228.3 L141.9 227.6 L139.6 227.0 L137.2 226.6 L134.8 226.3 L132.4 226.1 L130.0 226.0 L127.6 226.1 L125.2 226.3 L122.8 226.6 L120.4 227.0 L118.1 227.6 L115.8 228.3 L113.5 229.1 L111.3 230.0 L109.1 231.0 L107.0 232.2 L104.9 233.4 L103.0 234.8 L101.1 236.3 L99.2 237.8 L97.5 239.5 L95.8 241.2 L94.3 243.1 L92.8 245.0 L91.4 246.9 L90.2 249.0" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <path d="M90.2 249.0 L90.8 242.5 L95.5 245.2 Z" fill="currentColor" stroke="none"/>
  <text x="16" y="214" font-size="11" fill="currentColor">LiDAR sweeps 120°: 33 ms, 17 mm</text>
  <path d="M125.0 279.0 L130.0 270.0 L135.0 279.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <text x="121.0" y="292.0" font-size="10" fill="currentColor" text-anchor="middle">C1</text>
  <path d="M137.0 279.0 L142.0 270.0 L147.0 279.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <text x="151.0" y="292.0" font-size="10" fill="currentColor" text-anchor="middle">C2</text>
  <circle cx="130.0" cy="274.0" r="9" fill="none" stroke="currentColor" stroke-width="1.0" stroke-dasharray="3 2"/>
  <text x="160" y="268" font-size="11" fill="currentColor">LiDAR, 0.30 m above C1</text>
  <rect x="95" y="298" width="70" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="316" font-size="11" fill="currentColor" text-anchor="middle">base</text>
  <line x1="172" y1="312" x2="214" y2="312" stroke="currentColor" stroke-width="1.6"/>
  <path d="M220.0 312.0 L214.0 314.7 L214.0 309.3 Z" fill="currentColor" stroke="none"/>
  <text x="226" y="309" font-size="11" fill="currentColor">v = 0.5 m/s</text>
  <text x="226" y="322" font-size="11" fill="currentColor" fill-opacity="0.85">10 ms = 5 mm</text>
  <line x1="20" y1="356" x2="120" y2="356" stroke="currentColor" stroke-width="1.6"/>
  <line x1="20" y1="352" x2="20" y2="360" stroke="currentColor" stroke-width="1.0"/>
  <line x1="120" y1="352" x2="120" y2="360" stroke="currentColor" stroke-width="1.0"/>
  <text x="70" y="349" font-size="10" fill="currentColor" text-anchor="middle">1 m</text>
  <rect x="302.0" y="30.0" width="250.0" height="226.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <circle cx="528.8" cy="223.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="222.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="221.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="220.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="219.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="218.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="217.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="216.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="215.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="214.3" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="213.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="212.5" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="211.7" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="210.8" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="210.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="146.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="145.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="144.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="143.3" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="142.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="141.5" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="140.6" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="139.7" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="138.9" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="138.0" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="137.2" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="136.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="135.6" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="134.8" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="134.0" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="69.8" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="68.9" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="68.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="67.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="66.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="65.5" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="64.7" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="63.9" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="63.1" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="62.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="61.6" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="60.8" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="60.1" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="59.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="58.7" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="223.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="222.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="221.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="220.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="219.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="218.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="217.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="216.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="215.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="214.3" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="213.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="212.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="211.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="210.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="210.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="528.8" cy="146.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="145.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="144.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="143.3" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="142.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="141.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="140.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="139.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="138.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="138.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="137.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="136.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="135.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="134.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="134.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="528.8" cy="69.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="68.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="68.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="67.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="66.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="65.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="64.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="63.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="63.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="62.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="61.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="60.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="60.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="59.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="58.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <line x1="403.7" y1="126.7" x2="403.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="126.7" x2="450.3" y2="126.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="410.3" y1="126.7" x2="410.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="133.3" x2="450.3" y2="133.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="417.0" y1="126.7" x2="417.0" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="140.0" x2="450.3" y2="140.0" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="423.7" y1="126.7" x2="423.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="146.7" x2="450.3" y2="146.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="430.3" y1="126.7" x2="430.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="153.3" x2="450.3" y2="153.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="437.0" y1="126.7" x2="437.0" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="160.0" x2="450.3" y2="160.0" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="443.7" y1="126.7" x2="443.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="166.7" x2="450.3" y2="166.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="450.3" y1="126.7" x2="450.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="173.3" x2="450.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <circle cx="427.0" cy="150.0" r="10.0" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>
  <line x1="427.0" y1="150.0" x2="417.0" y2="150.0" stroke="currentColor" stroke-width="4.0" stroke-opacity="0.45" stroke-linecap="round"/>
  <line x1="427.0" y1="150.0" x2="425.0" y2="150.0" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <circle cx="427.0" cy="150.0" r="2.4" fill="currentColor" stroke="none"/>
  <text x="439.0" y="138.0" font-size="11" fill="currentColor" font-weight="600">L</text>
  <line x1="522.0" y1="246.0" x2="542.0" y2="246.0" stroke="currentColor" stroke-width="1.6"/>
  <line x1="522.0" y1="242.0" x2="522.0" y2="250.0" stroke="currentColor" stroke-width="1.0"/>
  <line x1="542.0" y1="242.0" x2="542.0" y2="250.0" stroke="currentColor" stroke-width="1.0"/>
  <text x="532.0" y="240.0" font-size="10" fill="currentColor" text-anchor="middle">10 mm</text>
  <text x="302" y="272.0" font-size="10.5" fill="currentColor">grid: camera pixels, 3.3 mm</text>
  <text x="302" y="286.0" font-size="10.5" fill="currentColor">dashed circle: S1's ±5 mm</text>
  <text x="302" y="300.0" font-size="10.5" fill="currentColor">circles: LiDAR spots, 16 mm</text>
  <text x="302" y="314.0" font-size="10.5" fill="currentColor">bars: blur, 5 mm (10 ms), 1 mm (2 ms)</text>
  <line x1="304" y1="324.0" x2="316.0" y2="324.0" stroke="currentColor" stroke-width="1.5"/>
  <path d="M321.0 324.0 L315.0 326.7 L315.0 321.3 Z" fill="currentColor" stroke="none"/>
  <text x="358.2" y="328.0" font-size="10.5" fill="currentColor">late stamp, 17 ms: 8.5 mm</text>
  <line x1="304" y1="338.0" x2="345.2" y2="338.0" stroke="currentColor" stroke-width="1.5"/>
  <path d="M350.2 338.0 L344.2 340.7 L344.2 335.3 Z" fill="currentColor" stroke="none"/>
  <text x="358.2" y="342.0" font-size="10.5" fill="currentColor">cloud stamp, 46 ms: 23 mm</text>
  <text x="16" y="394" font-size="11" fill="currentColor" fill-opacity="0.9">Every error is drawn at the facade 2 m away. Blur, late stamps and the sweep are all v·Δt at 0.5 m/s;</text>
  <text x="16" y="410" font-size="11" fill="currentColor" fill-opacity="0.9">only the camera's pixel, at a short exposure and a true stamp, is the size of S1's ±5 mm.</text>
</svg>

The rig passing the facade, every error drawn to scale where it lands. Left, in plan: the stereo depth error at $L$ ($\pm39\,\mathrm{mm}$ along the ray), the radar's $15\,\mathrm{cm}\times9.5^\circ$ cell ($0.33\,\mathrm m$ wide there), a worker $0.30\,\mathrm m$ before the facade, and the LiDAR's $120^\circ$ sweep across it ($33\,\mathrm{ms}$, $17\,\mathrm{mm}$ of base motion). Right, the facade around $L$ at $1\,\mathrm{mm}=2$ px: $3.3\,\mathrm{mm}$ camera pixels inside S1's $\pm5\,\mathrm{mm}$, $16\,\mathrm{mm}$ LiDAR spots overlapping along each ring with $\sim22\,\mathrm{mm}$ gaps between rings, the $5\,\mathrm{mm}$ blur of a $10\,\mathrm{ms}$ exposure, and two wrong time stamps worth $8.5$ and $23\,\mathrm{mm}$.

### 1. Image formation: light, exposure and noise

*In one sentence:* a pixel counts the photoelectrons that arrive while it is exposed; the randomness of that count sets a noise floor no algorithm removes, and the finite well sets the brightest part of the scene one exposure can hold.

**The problem.** On a site at low sun the rig's camera shows either a noisy shaded panel or a white blank where a glazed one glints, never both, and the obvious fixes — a longer exposure, more gain — make other things worse. To see why, follow the light into one pixel. The idea in plain words: a pixel is a bucket that counts photoelectrons while its shutter is open. The count is random, the bucket has a rim, and everything this section derives is one of those three facts with numbers on it.

**Light into the well.** A lens of focal length $f$ and aperture diameter $D$ has the f-number $N=f/D$, which sets the light per unit area reaching the image plane ([OpenStax §26.4](https://openstax.org/books/college-physics-2e/pages/26-4-microscopes)). Think of the lens as a funnel: a wider opening catches more of the light a patch of wall sends out, and a longer focal length spreads that light over a bigger image. A patch at distance $Z$ sends light into an opening whose solid angle is proportional to $D^2/Z^2$, and its image covers $(f/Z)^2$ times its area, so

$$E_{\text{image}}\ \propto\ \frac{D^2/Z^2}{f^2/Z^2}=\frac{1}{N^2}$$

since the distance cancels: a wall's image is as bright at $10\,\mathrm m$ as at $2$ (it is smaller, not dimmer), and each $\sqrt2$ step in $N$ halves it. The rig's lens is $f=3.6\,\mathrm{mm}$ at $f/2$, an aperture of $1.8\,\mathrm{mm}$. A pixel then collects $S=\Phi\,t_{\exp}$ photoelectrons, the scene's rate times the exposure: the shaded facade, at $200$ per ms, gives $400\ e^-$ in $2\,\mathrm{ms}$.

**Four noise sources.** Why is a count noisy at all? Because photons arrive independently, like raindrops into a bucket: the same shower gives a slightly different count in each second. That count is Poisson, whose variance equals its mean, so its **shot noise** is $\sqrt S$ — $20\ e^-$ on $400$, $5\%$; heat frees **dark-current** electrons, Poisson too, $D_c t_{\exp}$ of them; the amplifier adds a fixed **read noise** $\sigma_{\text{read}}$; and the converter's step adds **quantization** noise $10/\sqrt{12}=2.89\ e^-$ ([[02-foundations/signal-processing|6. Signal Processing §2]]; when that is noise and when a bias, [[04-robotics/sensor-models|3.2 §4]]). Camera makers list the same sources for CCD and CMOS sensors alike ([Hamamatsu](https://hamamatsu.magnet.fsu.edu/articles/ccdsnr.html); [Andor](https://andor.oxinst.com/learning/view/article/sensitivity-and-noise-of-ccd-emccd-and-scmos-sensors)). Independent, their variances add ([[02-foundations/probability|3. Probability §2]]).

> **Pixel SNR, defined.** The **pixel signal-to-noise ratio** is a *ratio of a pixel's mean signal to the standard deviation of its value from frame to frame* — a property of one measurement (one pixel, exposure and brightness), not of a camera. Four conditions: the signal is a **photoelectron count** $S=\Phi t_{\exp}$; arrivals are **Poisson**, so the shot variance equals $S$; the sources are **independent**, so variances add; and the pixel is **below full well** — a saturated pixel reads the same whatever the light, so its SNR is undefined, not large.
>
> $$\mathrm{SNR}=\frac{S}{\sqrt{S+D_c\,t_{\exp}+\sigma_{\text{read}}^2+\sigma_q^2}}$$
>
> where $S$ is the signal, $D_c$ the dark current, $t_{\exp}$ the exposure, $\sigma_{\text{read}}$ and $\sigma_q$ the read and quantization noise, all in electrons — the Hamamatsu form with quantization added. For $S\gg\sigma_{\text{read}}^2$ it tends to $\sqrt S$, the shot-noise limit.
>
> - **Example**: the shaded facade at $2\,\mathrm{ms}$: $S=400\ e^-$, $\mathrm{SNR}=400/\sqrt{400+0.2+25+8.33}=19.2$, near the limit $\sqrt{400}=20$; at $10\,\mathrm{ms}$, $44.3$.
> - **Non-example**: raising the analog gain. It multiplies the collected electrons and their noise alike, adds no photons, and leaves the shot-noise limit where it was.
> - **Why it matters**: every "pixel noise" downstream — 3.2's $\sigma_u$, §3's $\sigma_d$, a matcher's success — starts here, and a longer exposure buys SNR as $\sqrt{t_{\exp}}$. §2 is what it costs.

> **Dynamic range, defined.** The **dynamic range** is a *ratio of the largest to the smallest signal a sensor records in one exposure*, to be compared with the scene's ratio of brightest to darkest. Three conditions: the top is where the pixel or converter **saturates**; the bottom is the **noise floor in the dark**, SNR $=1$; and both belong to **one exposure and one gain**.
>
> $$\mathrm{DR}=\frac{S_{\max}}{\sigma_{\text{read}}},\qquad \mathrm{DR}_{\mathrm{dB}}=20\log_{10}\mathrm{DR}$$
>
> where $S_{\max}$ is the full well and $\sigma_{\text{read}}$ the read noise (Hamamatsu's definition), so the rig has $10{,}000/5=2{,}000$, $66.0\,\mathrm{dB}$ ($10.97$ stops), and $64.8\,\mathrm{dB}$ with the converter's step in the floor.
>
> - **Example**: sun against shade is $2{,}000/200=10$, $20\,\mathrm{dB}$: at $2\,\mathrm{ms}$ the shade reads at SNR $19.2$ and the sun at $4{,}000\ e^-$, unsaturated.
> - **Non-example**: the low sun's glint against the shade, $2\times10^6/200$, is $80\,\mathrm{dB}$. No exposure holds both: the glint fills the well in $5\,\mathrm{\mu s}$, when the shade holds $1\ e^-$ (SNR $0.17$).
> - **Why it matters**: at low sun the lighting ratio, not resolution, decides what is seen; auto-exposure picks one end, and a shaded panel beside a glazed one it exposed for is simply absent.

> [!note]- Deeper · 더 깊이
> **Heat, gain and merged exposures.** Dark current roughly halves for every $5$–$9\,^\circ\mathrm C$ of cooling in the high-performance CCDs Hamamatsu describes, cooled below room temperature. If the same rule holds for the rig's sensor warming above it, a housing $30\,^\circ\mathrm C$ warmer in site sun carries $2^{30/9}=10$ to $2^{30/5}=64$ times the dark signal: at $64\times100\ e^-/\mathrm s$ and $10\,\mathrm{ms}$, $64\ e^-$ with a standard deviation of $8$, above the read noise, in the dark regions. Gain trades headroom for a finer step: at $\times4$ the converter's full scale is $2{,}558\ e^-$ and the floor $5.05\ e^-$, a dynamic range of $506$ ($54.1\,\mathrm{dB}$) instead of $1{,}732$. Sensor modes that merge exposures — alternating rows, pixels in groups of four with their own exposure times, or successive frames ([Basler, *HDR*](https://docs.baslerweb.com/hdr)) — widen the range, but on a moving base their exposures are taken at different moments, which §9 prices.

### 2. Motion blur and the rolling shutter

*In one sentence:* while a pixel is exposed the image of a moving scene slides by $f\,v\,t_{\exp}/Z$ pixels, and a rolling shutter exposes each row a little later than the last, so a moving rig smears and shears the same image through two different clocks.

**The problem.** §1 says a longer exposure buys SNR. On a moving base it also buys motion: the scene slides across the pixels while they collect, and the rig's cameras read their rows one after another, so the top and bottom of one frame are taken at different moments. The idea: the image is a record of *where things were during an interval*, not at an instant, and the rules below say how long that interval is in pixels.

**The smear.** A point at depth $Z$ moving at $v$ parallel to the image plane projects to $u(t)=f(X_0+vt)/Z+c_x$ (3.5 §1), so its image moves at $f v/Z$ pixels per second and, while the pixel integrates, draws a streak.

> **Motion blur, defined.** **Motion blur** is a *length in the image*: how far a point's image travels while the pixel is exposed. Four conditions: the motion is **relative motion during the exposure**, not the frame period; only the component **parallel to the image plane** smears to first order; the point's **depth** enters, so near things smear more under translation; and a **rotation** at rate $\omega$ smears every point by about $f\omega t_{\exp}$ near the centre, whatever its depth (the turning head of [[04-robotics/egocentric-perception|22. Egocentric Perception]]).
>
> $$b=\frac{f\,v\,t_{\exp}}{Z}$$
>
> in pixels, with $f$ in pixels, $v$ the speed, $t_{\exp}$ the exposure and $Z$ the depth — on the facade the streak is simply $v\,t_{\exp}$ long.
>
> - **Example**: the rig at $0.5\,\mathrm{m/s}$ and $2\,\mathrm m$ blurs by $1.50$ px ($5.0\,\mathrm{mm}$) at $10\,\mathrm{ms}$ and $0.30$ px at $2\,\mathrm{ms}$; P6's camera, $1.0\,\mathrm m$ from its rail, blurs a $0.5\,\mathrm{m/s}$ cart by $3.0$ px at $10\,\mathrm{ms}$, six times its $\sigma_u$.
> - **Non-example**: blur is not noise. It is the same deterministic smear in every frame at that speed, so averaging frames does not shrink it — and the streak's centre is where the point was at **mid-exposure**, which is why §9 stamps images there.
> - **Why it matters**: blur caps the exposure from above while SNR (§1) bounds it from below; between them lies the window a moving robot can use.

**The exposure window.** At $0.5\,\mathrm{m/s}$ the shade needs $t_{\exp}\ge0.632\,\mathrm{ms}$ for an SNR of $10$, half a pixel of blur allows $t_{\exp}\le0.5Z/(fv)=3.333\,\mathrm{ms}$, and the sun stays unsaturated to $5.0\,\mathrm{ms}$. The indoor $10\,\mathrm{ms}$ fails twice: $1.5$ px of blur and a saturated sunlit half. At $2\,\mathrm{m/s}$ the upper limit falls to $0.833\,\mathrm{ms}$; at dusk, with a tenth of the light, the lower limit rises about tenfold, past it. Then only light (a strobe), aperture or a slower base helps — not gain.

**The rolling shutter.** A global shutter starts and stops all pixels at once; a rolling shutter exposes row after row, each offset by the row time, and reading the frame takes that time times the rows ([Basler, *Electronic Shutter Types*](https://docs.baslerweb.com/electronic-shutter-types), whose examples include $14$ and $35\,\mathrm{\mu s}$ per row).

> **Rolling-shutter skew, defined.** **Rolling-shutter skew** is a *shift between rows of one image*, caused by rows being exposed at different times — a geometric distortion, not a blur. Three conditions: rows are exposed **sequentially with a constant row delay** $t_{\text{row}}$; there is **relative motion during the readout**; and every row's exposure has the **same length**, so rows differ in when, not how long.
>
> $$\Delta u(r)=\frac{f\,v\,r\,t_{\text{row}}}{Z}$$
>
> where $r$ is the row counted from the first and the rest is as in the blur — so a vertical edge leans while the rig moves sideways.
>
> - **Example**: $480$ rows take $12\,\mathrm{ms}$; at $0.5\,\mathrm{m/s}$ and $2\,\mathrm m$ the last row sees the facade $6.0\,\mathrm{mm}$ further along, $1.80$ px, and a vertical panel edge leans $0.21^\circ$.
> - **Non-example**: a short exposure does not remove skew. At $0.5\,\mathrm{ms}$ the blur is $0.075$ px and the skew still $1.80$ px; only a global shutter, or light that is on only while every row is open (Basler's flash window), removes it.
> - **Why it matters**: a rolling-shutter frame holds $480$ poses, not one, and a method that assigns one pose per image sees a slightly wrong geometry, which is why [[04-robotics/state-estimation-slam|3. State Estimation §8]] lists the rolling shutter among the details that can dominate an algorithm's gains.

Two rolling-shutter cameras triggered together read matching rows at the same instant, so a sideways motion shifts both images of a point alike and the disparity survives; triggered apart, it does not (§9).

### 3. Stereo depth as a sensor

*In one sentence:* a stereo pair turns pixel noise into depth noise that grows as the square of the range and falls with the baseline, and it measures nothing where the two images have nothing distinct to match.

**The problem.** 3.5 treats stereo as geometry: two rays, one point. A robot needs it as a sensor with an error bar at a working range, to compare with a LiDAR or to size a rig. The idea: depth comes from a small difference of two pixel positions, and a small difference of two noisy numbers is noisy — the farther the point, the smaller the difference and the worse the depth.

**From $Z=fb/d$ to an error bar.** 3.5 §2 gives $Z=fb/d$ and the worth of one pixel of disparity, $Z^2/(fb)$. A disparity is a difference of two positions, $d=u_1-u_2$, each located with an independent error $\sigma_u$, so variances add:

$$\sigma_d=\sqrt{\sigma_u^2+\sigma_u^2}=\sqrt2\,\sigma_u$$

because each error enters the difference with weight $\pm1$ — $0.707$ px with 3.2's $\sigma_u=0.5$ px. Linearizing $Z(d)$ with $Z'(d)=-fb/d^2=-Z^2/(fb)$ turns that into a depth error.

> **Depth precision of a triangulating sensor, defined.** It is the *standard deviation of the depth* a sensor reports by intersecting two rays over a known baseline — two cameras, or a camera and a projector (§4) — at a stated range. Four conditions: the geometry is **calibrated and rectified** (3.5's model); the correspondence is **correct** — a wrong match is a gross error, not a larger $\sigma_d$; the disparity error is **small against the disparity**, so the linear step holds; and the two images' errors are **independent**.
>
> $$\sigma_Z=\frac{Z^2\,\sigma_d}{f\,b}$$
>
> where $Z$ is the range, $b$ the baseline, and $\sigma_d$ and $f$ the disparity noise and the focal length, both in pixels — the law Keselman et al. state for the RealSense stereo cameras ([arXiv:1705.05548](https://arxiv.org/abs/1705.05548)).
>
> - **Example**: at the facade, $4\times0.707/72=39.3\,\mathrm{mm}$, about $2\%$ of the range; at $8\,\mathrm m$, $628.5\,\mathrm{mm}$, where §10's simulation gives $644.3\,\mathrm{mm}$ and a $+49.4\,\mathrm{mm}$ bias, because $\sigma_d/d=0.079$ is no longer small and $Z=fb/d$ is convex.
> - **Non-example**: a wider baseline is not free. At $b=0.24\,\mathrm m$ the error halves to $19.6\,\mathrm{mm}$, but a $128$-disparity search then sees nothing nearer than $fb/128=1.125\,\mathrm m$ instead of $0.562$ (3.5 §2's near limit), and the views differ more.
> - **Why it matters**: it says what a rig promises at a range and where another sensor takes over. The course LiDAR's $20\,\mathrm{mm}$ does not grow with range, so stereo beats it only nearer than $\sqrt{\sigma_L fb/\sigma_d}=1.43\,\mathrm m$.

Across the ray the same pixel noise is only $Z\sigma_u/f=1.67\,\mathrm{mm}$ at $2\,\mathrm m$, so a stereo point is a needle along its ray, $\sqrt2\,Z/b=23.6$ times longer than wide.

**What stereo needs from the surface.** A disparity exists only where a patch can be found again in the other image. An evenly painted panel gives every window the same content — no peak to match (3.5 §2.5's flat structure tensor). A row of identical panels gives one good match per panel, and 3.5 §2.6 shows the wrong one passing the epipolar check $40\,\mathrm{cm}$ too far. $\sigma_Z$ prices neither: it assumes the match is right.

**Active stereo.** A projector that throws an infrared pattern gives a blank panel texture; the two cameras still triangulate between themselves. Keselman et al. give the projector exactly that job — texture that makes matching unambiguous — and ask of the pattern that it be dense, photometrically consistent and free of repetition along the matching axis. Their infrared cameras work both in darkness, lit by the projector, and in broad daylight, where the sun lights the scene's own texture.

### 4. Time-of-flight and structured-light depth cameras

*In one sentence:* a time-of-flight (ToF) camera measures how long its own light takes to come back, directly as a pulse's delay or indirectly as a phase, and a structured-light camera triangulates against a pattern it throws; both bring their own light, so both work in the dark and both must outshine the sun.

**The problem.** Stereo needs texture and gets worse as $Z^2$. A camera that lights the scene itself needs no texture, and one that measures time instead of an angle escapes triangulation's $Z^2$ law. The idea: light is fast but not infinitely fast, so a round trip to the facade takes a measurable time, and that time is the range.

**Pulsed time of flight.** A pulse travels out and back, $2R$, at $c=299{,}792{,}458\,\mathrm{m/s}$, exact by definition ([NIST](https://physics.nist.gov/cgi-bin/cuu/Value?c)):

$$R=\frac{c\,\tau}{2}$$

because the delay $\tau$ covers both ways. One nanosecond is $0.1499\,\mathrm m$ of range, so a direct time-of-flight sensor is a timing instrument first. Read **P5**'s range sensor that way (3.2 does not say how it ranges; this is a reading, not a new fact): its $12\,\mathrm{cm}$ is a round trip of $0.801\,\mathrm{ns}$, its $\sigma_r=10\,\mathrm{mm}$ is $66.7\,\mathrm{ps}$ of timing jitter, and its $4\,\mathrm{mm}$ mounting offset reads like a fixed $26.7\,\mathrm{ps}$ of extra delay — a bias that calibration removes and averaging does not (3.2 §5).

**Continuous-wave time of flight.** Timing picoseconds in every pixel is hard, so many depth cameras modulate their light and measure a phase instead; the Azure Kinect's depth camera, for one, casts amplitude-modulated near-infrared light and records an indirect measurement of its travel time ([Microsoft Learn](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/depth-camera)). A delay $\tau=2R/c$ is $f_{\text{mod}}\tau$ cycles of a modulation at $f_{\text{mod}}$, so the return lags by

$$\varphi=2\pi f_{\text{mod}}\frac{2R}{c},\qquad R=\frac{c\,\varphi}{4\pi f_{\text{mod}}}$$

— the relation Baek et al. write ([arXiv:2105.11606](https://arxiv.org/abs/2105.11606)). Two facts follow. A phase error $\sigma_\varphi$ is a range error $c\sigma_\varphi/(4\pi f_{\text{mod}})$: at the course camera's $0.02\,\mathrm{rad}$, $4.77\,\mathrm{mm}$ at $100\,\mathrm{MHz}$ and $23.86\,\mathrm{mm}$ at $20$, so a high frequency is precise. And a phase is known only modulo $2\pi$ — like a clock face that shows the minutes but not the hour.

> **Ambiguity range, defined.** The **ambiguity range** of a continuous-wave time-of-flight sensor is the *largest range its phase reports uniquely* — a property of the modulation, not of the scene. Three conditions: the light is modulated **periodically** at $f_{\text{mod}}$; the phase is measured **modulo $2\pi$**; and each pixel sees **one dominant return** (a pixel mixing two paths reports neither).
>
> $$R_{\text{amb}}=\frac{c}{2f_{\text{mod}}}$$
>
> where $c$ is the speed of light and $f_{\text{mod}}$ the modulation frequency — the range at which the round trip is exactly one modulation period, so the phase is back where it started.
>
> - **Example**: at $100\,\mathrm{MHz}$, $R_{\text{amb}}=1.499\,\mathrm m$, so the facade at $2.000\,\mathrm m$ reads $0.501\,\mathrm m$; at $80\,\mathrm{MHz}$ ($1.874\,\mathrm m$) it reads $0.126\,\mathrm m$. The pair of readings repeats only when the round trip is a whole number of both periods, $10$ and $12.5\,\mathrm{ns}$ — first at $50\,\mathrm{ns}$, the period of $20\,\mathrm{MHz}$, the largest frequency dividing both — so together they read $2.000\,\mathrm m$ uniquely out to $c\times50\,\mathrm{ns}/2=7.495\,\mathrm m$, at the higher frequency's precision.
> - **Non-example**: the ambiguity range is not the working range. A dark wall inside it may return too little light to measure; the Azure Kinect documentation lists low and saturated signals among the reasons it invalidates a pixel.
> - **Why it matters**: a wrapped range is a confident wrong number, not a noisy right one; $0.501\,\mathrm m$ passes any check on one reading, and only a second frequency, a prior or another sensor catches it.

**Where depth cameras fail on a site.** Three failures, each with its cause. **Multipath**: one pixel integrates light that arrived by more than one path, the Azure Kinect documentation's common case being a corner, where light bounces off one wall onto the other — the inside corner between two panels. **Flying pixels**: at a depth edge a pixel sees foreground and background together and reports a range between them ([Zollhöfer, arXiv:1902.06835](https://arxiv.org/abs/1902.06835)). **Sunlight**: the sensor's own light is read against the ambient light at its wavelength, and Zollhöfer notes time-of-flight sensing struggles in strong sunlight.

**Structured light.** Replace one camera of a stereo pair with a projector that throws a known pattern and triangulate between the camera and the projector, which Zollhöfer calls an inverse camera ([Geng 2011](https://doi.org/10.1364/AOP.3.000128) reviews the family). The geometry is §3's with the projector–camera baseline $b_p$, so the error grows as $Z^2/(f\,b_p)$. The weakness is the light: the pattern's brightness on a surface falls as $1/R^2$ while sunlight does not fall at all, and outdoors the sun drowns it — Zollhöfer notes that the sun's infrared can saturate the sensor and leave the pattern indiscernible.

> [!note]- Deeper · 더 깊이
> **Why the pattern loses to the sun as $1/R^2$.** A projector spreads a fixed power over a pattern whose area grows as $R^2$, so its irradiance on a surface is proportional to $1/R^2$, while the sun's irradiance on that surface does not depend on $R$: the ratio falls as $1/R^2$, and doubling the range quarters the contrast the decoder works with. Zollhöfer's survey also warns that several active sensors looking at one surface can disturb each other's patterns — worth knowing before a rig carries two depth cameras.

### 5. LiDAR

*In one sentence:* a LiDAR fires short laser pulses in a fixed pattern of directions and times their echoes, so its range error hardly grows with distance while its samples spread apart, its spots grow, and its points are taken over a whole sweep rather than at one instant.

**The problem.** Stereo's error grows as $Z^2$: $39\,\mathrm{mm}$ at the facade, $628\,\mathrm{mm}$ at $8\,\mathrm m$. The idea of a LiDAR: take §4's pulsed rangefinder and sweep it through a fixed grid of directions. Each point is then good in range at any distance and coarse in where it lands.

**The measurement.** It ranges with a pulsed laser ([NOAA](https://oceanservice.noaa.gov/facts/lidar.html)) by §4's $R=c\tau/2$, mostly at $905$ or $1550\,\mathrm{nm}$ ([Li and Ibanez-Guzman 2020](https://arxiv.org/abs/2004.08467); [Dreissig et al. 2023](https://arxiv.org/abs/2304.06312)). The course LiDAR's $\sigma_L=20\,\mathrm{mm}$ is $133\,\mathrm{ps}$ of timing jitter, and a time error is the same at every range, so the range error is flat — the property stereo lacks. A spinning unit stacks its $32$ channels in elevation and turns, firing a column every $0.2^\circ$ at $10$ turns a second: $1{,}800$ columns, $576{,}000$ points per second, inside the $32$–$256$ channels and $512$–$4{,}096$ columns one manufacturer lists ([Ouster](https://ouster.com/os-overview)).

**Where the samples land.** A fixed angular step $\Delta\phi$ becomes an arc $R\,\Delta\phi$ on a surface facing the sensor, so

$$s_h=R\,\Delta\phi,\qquad s_v=R\,\Delta\varepsilon,\qquad \rho_{\text{pts}}=\frac{1}{s_h\,s_v}\ \propto\ \frac{1}{R^2}$$

with $\Delta\varepsilon$ the channel spacing and $\rho_{\text{pts}}$ the points per square metre, because each point stands for one $s_h\times s_v$ cell. At the facade's $2\,\mathrm m$: $7.0\times34.9\,\mathrm{mm}$ and $4{,}104$ points/m²; at $10\,\mathrm m$, $34.9\times174.5\,\mathrm{mm}$ and $164$. A surface turned away from the beam stretches the spacing by $1/\cos\alpha$ ([[05-construction-robotics/site-perception|5. Site Perception §1]] defines it that way for a survey scanner). Next to $L$ the beam is longer, $2.12\,\mathrm m$, and meets the facade $19.5^\circ$ off its normal, so the picture's spacing there is $7.4$ by about $38\,\mathrm{mm}$.

> **Beam footprint, defined.** The **beam footprint** is the *diameter of the spot one pulse lights on a surface* — the area one range measurement covers, not the distance between measurements. Four conditions: the beam leaves the window with a **diameter** $w_0$; it spreads with a **full divergence angle** $\theta$, small; it is evaluated at a **range** $R$; and an **incidence angle** $\alpha$ stretches it by $1/\cos\alpha$ along the tilt.
>
> $$w(R)=w_0+\theta R$$
>
> at normal incidence, the second term being the arc the divergence subtends at $R$ — so the spot and the spacing both grow in proportion to range.
>
> - **Example**: at the facade $w=10+3.0\times2=16\,\mathrm{mm}$ against a $7.0\,\mathrm{mm}$ step along the ring, so each spot overlaps two neighbours on each side, and $34.9\,\mathrm{mm}$ between rings, which leaves $18.9\,\mathrm{mm}$ of wall no pulse touches. At $10\,\mathrm m$ it is $40\,\mathrm{mm}$.
> - **Non-example**: once spots overlap, a finer column step is not a finer measurement: at $0.1^\circ$ four spots share each $16\,\mathrm{mm}$ instead of two, but each still returns one range for its whole spot, so an edge inside a spot is no sharper.
> - **Why it matters**: S1 places its hole to $\pm5\,\mathrm{mm}$ ([[05-construction-robotics/site-engineering|2.5]]). A $16\,\mathrm{mm}$ spot on rings $35$ to $38\,\mathrm{mm}$ apart cannot see that; the camera's $3.3\,\mathrm{mm}$ pixel can. At the panel the LiDAR gives the geometry around the hole, not the hole.

**When it fails on a site.** Four conditions, two of the surface and two of the air. **Dark surfaces** return less light: for a surface that fills the beam and scatters evenly, the returned power goes as $\rho/R^2$ (derived in the callout below), so a dark panel of reflectivity $0.1$ returns an eighth of what a white one of $0.8$ does at the same range, and matches it only at $1/\sqrt8=0.354$ of the range. **Glass and polished metal** mirror the pulse away: Henley et al. note such specular surfaces may be invisible to a LiDAR relying on direct single-scatter returns ([*Optics Express* 2023](https://doi.org/10.1364/OE.479900)). **Rain and fog** scatter the pulse, so some light returns early, as points in mid-air, and some never returns ([Dreissig et al. 2023](https://arxiv.org/abs/2304.06312)). **Dust** is the site's own case: Phillips, Guenther and McAree found that a LiDAR measures a dust cloud to its leading edge rather than as random noise, that dust starts to matter below about $71$–$74\%$ transmittance, and that the effect is weaker in the far field ([*Journal of Field Robotics* 2017](https://doi.org/10.1002/rob.21701)). To a single-return LiDAR, the dust from a saw is a wall.

**The sweep takes time.** A revolution takes $100\,\mathrm{ms}$, in which the base moves $50\,\mathrm{mm}$; the beam crosses $120^\circ$ of facade in $33.3\,\mathrm{ms}$, so the facade in one cloud is smeared by $16.7\,\mathrm{mm}$. [[04-robotics/state-estimation-slam|3. State Estimation §7.2]] gives the cure, deskewing: move each point to one time using the sensor's pose at its own firing time. That needs each point's time, and a ROS point cloud carries one header stamp for the whole cloud ([`sensor_msgs/PointCloud2`](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/PointCloud2.msg)); per-point times exist only if the driver adds them, as a sensor's own packets may carry a timestamp per column ([Ouster, *Sensor Data*](https://static.ouster.dev/sensor-docs/image_route1/image_route2/sensor_data/sensor-data.html)). With the course LiDAR stamping the start of each sweep, the column that sees $L$ fires $46.1\,\mathrm{ms}$ after the stamp — $23.1\,\mathrm{mm}$ of base motion if the stamp is used for it (§9).

> [!note]- Deeper · 더 깊이
> **The return from a surface.** Take a surface that fills the beam and scatters evenly in all directions (a Lambertian surface), reflectivity $\rho$, at normal incidence. It sends back a fraction $\rho$ of the pulse's power $P_t$ with an on-axis intensity of $\rho P_t/\pi$ per steradian, and a receiver of area $A_r$ at range $R$ subtends $A_r/R^2$ steradians, so $P_r=\rho P_tA_r/(\pi R^2)$: the spot's size cancels once the surface fills the beam. Manufacturers state ranges against such targets; one calibrates its reflectivity channel against Lambertian targets on a scale reaching retroreflectors $864$ times brighter than perfect white (Ouster, *Sensor Data*).
>
> **One pulse, several echoes.** A spot straddling the panel's edge and the wall $0.3\,\mathrm m$ behind returns two peaks; the USGS lidar specification calls the stored peaks discrete returns, first and last ([USGS glossary](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-glossary)), and a sensor reporting the strongest and second-strongest returns can see through rain, fog or a chain-link fence (Ouster). Phillips et al. also found the sensor still ranging through a dust cloud of $2\%$ transmittance to a retroreflective target, and of $6\%$ to a low-reflectivity one.
>
> **Spinning and solid-state.** A spinning unit turns its emitters on a motor and sees all around; solid-state designs steer with a micro-mirror (MEMS) or an optical phased array, or light the whole scene at once (flash), which Li and Ibanez-Guzman note avoids the motion compensation a scanning sensor needs, since all its ranges are measured together.

### 6. Radar

*In one sentence:* an FMCW (frequency-modulated continuous-wave) radar sweeps its frequency, so a reflector's range becomes a beat frequency, its radial speed a phase step between sweeps and its bearing a phase step across antennas, and how finely it separates two reflectors is set by what it sweeps — bandwidth, time, aperture — not by how strong the echoes are.

**The problem.** In dust, smoke or darkness the camera, the stereo pair and the LiDAR all degrade, and a person near the base is exactly what must not be missed. A radar's wavelength is millimetres, not micrometres, and it brings its own signal. The idea: instead of timing a pulse, the radar sends a tone whose pitch rises steadily; the echo is the same rising tone, a little late, and "a little late" shows up as a constant difference in pitch.

**The chirp and the beat.** The transmitted frequency rises linearly, $f(t)=f_c+St$ with slope $S=B/T_c$ over a sweep of bandwidth $B$ in time $T_c$. An echo from range $R$ is the same chirp delayed by $\tau=2R/c$; mixed with the chirp still going out, the two differ by a constant, because both ramps have the same slope:

$$f_b=S\,\tau=\frac{2SR}{c}$$

so range becomes a frequency. The course radar sweeps $1.0\,\mathrm{GHz}$ in $50\,\mathrm{\mu s}$, $S=20\,\mathrm{MHz/\mu s}$, and the facade at $2\,\mathrm m$ beats at $266.9\,\mathrm{kHz}$. The receiver passes beats only inside its $5\,\mathrm{MHz}$ intermediate-frequency (IF) band, so the range is capped at $5\,\mathrm{MHz}\times c/(2S)=37.5\,\mathrm m$. The band is real: one single-chip sensor covers $76$–$81\,\mathrm{GHz}$ with $3$ transmitters, $4$ receivers and $4\,\mathrm{GHz}$ of sweep ([TI AWR1843](https://www.ti.com/product/AWR1843)), the band Harlow et al. survey for robotics ([IEEE T-RO 2024](https://arxiv.org/abs/2305.01135)).

**Separating two ranges.** One chirp is a record $T_c$ long, and a record that long resolves frequencies $1/T_c$ apart — the DFT's bin spacing ([[02-foundations/signal-processing|6. Signal Processing §3]]). Putting $\Delta f_b=1/T_c$ into $f_b=2SR/c$ gives $\Delta R=c/(2ST_c)$, and since $ST_c=B$, only the swept bandwidth survives.

> **Range resolution, defined.** The **range resolution** of an FMCW radar is the *range separation at which two reflectors can begin to appear as two peaks in one chirp's spectrum* — the size of a range cell, not the precision of one reflector's range. Three conditions: the chirp is **linear**, bandwidth $B$ over $T_c$; the echoes are separated in the spectrum of **one chirp**, whose cells are $1/T_c$ wide; and the reflectors are of **comparable strength**, differing in range along the beam.
>
> $$\Delta R=\frac{c}{2B}$$
>
> where $c$ is the speed of light and $B$ the swept bandwidth (Harlow et al.'s statement), so it is set by bandwidth alone, not by the carrier, the chirp's length or the sampling rate.
>
> - **Example**: $1\,\mathrm{GHz}$ gives $14.99\,\mathrm{cm}$ cells. A worker $0.30\,\mathrm m$ before the facade is two cells from it, and §10 separates the two echoes for all $36$ relative phases it tries; at $0.5\,\mathrm{GHz}$ (one cell) for $13$ of $36$; at $0.25\,\mathrm{GHz}$, never. One cell is where separation becomes possible, two where it becomes dependable.
> - **Non-example**: resolution is not precision. One isolated reflector's range can be read far finer than a cell — the Doppler step below is $0.08\,\mathrm{mm}$ of range per chirp, read from phase alone. The $15\,\mathrm{cm}$ is about telling two reflectors apart.
> - **Why it matters**: whether a worker at the facade is a second object to the radar is decided by $B$; and S1's $\pm5\,\mathrm{mm}$ is a thirtieth of one cell, which is why the radar cannot place the hole.

**Speed from phase.** Between chirps, $T_c$ apart, a reflector closing at $\dot R$ moves $\dot RT_c$ — too little to change its beat frequency, but the echo's phase, $4\pi R/\lambda$ at the carrier's wavelength $\lambda=c/f_c=3.893\,\mathrm{mm}$ (a path of $2R$, at $2\pi$ per wavelength), turns by $\Delta\varphi=4\pi\dot RT_c/\lambda$. So

$$\dot R=\frac{\lambda\,\Delta\varphi}{4\pi T_c},\qquad v_{\max}=\frac{\lambda}{4T_c},\qquad v_{\text{res}}=\frac{\lambda}{2N_cT_c}$$

since the step is unambiguous while $|\Delta\varphi|<\pi$, and $N_c$ chirps form a record $N_cT_c$ long in the phase, resolved by the same bin-spacing argument (Harlow et al. give the first two). The worker walking toward the radar at $1.6\,\mathrm{m/s}$ turns the phase by $-0.2582\,\mathrm{rad}$ per chirp, which §10 reads back as $-1.600\,\mathrm{m/s}$; with $128$ chirps the velocity cell is $0.304\,\mathrm{m/s}$, so the worker sits $5.26$ cells from the static facade, and $v_{\max}=19.47\,\mathrm{m/s}$. The trap: only the component along the line of sight counts. A worker crossing straight in front of the radar, walking along the facade, has no radial speed there, so Doppler does not separate them from the facade however fast they walk; and on a moving base the static facade itself has a radial speed that changes with bearing — the pattern radar odometry reads.

**Bearing from phase across antennas.** Receivers $d$ apart see an echo from bearing $\vartheta$ with a phase step $2\pi d\sin\vartheta/\lambda$ from one to the next — $2\pi$, not $4\pi$, because the extra path $d\sin\vartheta$ is on the way back only. A DFT across $N$ elements resolves steps $2\pi/N$ apart — the bin-spacing argument a third time — so at $d=\lambda/2$ it resolves $\Delta\sin\vartheta=2/N$. The course radar's $3$ transmitters, taking turns with $4$ receivers, act as one row of $12$ receivers (a virtual array), which resolves $2/12\ \mathrm{rad}=9.55^\circ$: a cell $0.33\,\mathrm m$ wide at the facade and $1.67\,\mathrm m$ at $10\,\mathrm m$.

**Why it sees through dust, and what it cannot see.** A $3.9\,\mathrm{mm}$ wavelength is long against dust grains and fog droplets; Harlow et al. put it plainly — longer wavelengths can bypass visual clutter such as fog, dust and smoke. It brings its own signal, so darkness costs nothing. Rain is not transparent — a $77\,\mathrm{GHz}$ automotive radar has even been studied as a rain gauge ([Bertoldo et al. 2018](https://etasr.com/index.php/ETASR/article/view/1755)). What it cannot give is geometry: its returns are sparse and noisy, with multipath "ghost" objects and, without elevation channels, little height (Harlow et al.). On S1's site its job is therefore the one the others do worst: a person near the base, in dust, at night, moving.

> [!note]- Deeper · 더 깊이
> **Where radar already does this job.** Cars have carried it for driver assistance since at least 2005, and robots use it for odometry, mapping and detection in poor visibility, mining among them (Harlow et al.). Around large machines it warns of people nearby: a test on off-highway dump trucks found that it reliably detected people, small vehicles, berms and other equipment, that alarms for objects posing no danger were common, and that it should be paired with cameras so the operator can check each alarm ([Ruff 2006](https://doi.org/10.1016/j.aap.2005.07.006)) — §7's division of labour on a haul road.

### 7. Choosing sensors for site conditions

*In one sentence:* each sensor fails where its physics does — a camera with light, stereo with texture, an active depth camera with sunlight, a LiDAR with particles and glass, a radar with fine structure — so a site rig is chosen by the conditions it must survive, not by its best-day accuracy.

**The problem.** A datasheet quotes each sensor on its best day. A site offers low sun, dust, rain, darkness and rows of identical panels, often at once. The idea: go down §1–§6 and, for each condition, ask which physical step breaks. The table does that at the facade's $2\,\mathrm m$; every entry is derived on this page or taken from the source its section cites, a dash means this page has not priced it, and the cost column is a relative, qualitative class for a first choice, not a quote.

| Sensor | Dark / low sun | Dust, fog, rain | Bare, repeated, glass | Depth error at $2\,\mathrm m$ | Samples at $2\,\mathrm m$ | Reach | Cost class |
|---|---|---|---|---|---|---|---|
| camera | fails: collects light only / glint's $80\,\mathrm{dB}$ over the sensor's $66$ (§1) | visual clutter (§6) | no features, or the wrong one (3.5 §2.5–§2.6) | none from one image (3.5 §1) | $3.3\,\mathrm{mm}$ per pixel | any lit range; blur $fvt_{\exp}/Z$ (§2) | low |
| stereo pair | as the camera | as the camera | no depth on bare panels; $40\,\mathrm{cm}$ off on repeated ones (3.5 §2.6) | $39.3\,\mathrm{mm}$ (§3) | $3.3\,\mathrm{mm}$ where matched | from $0.56\,\mathrm m$; $\sigma_Z\propto Z^2$ | low |
| active stereo | works on its pattern / on sunlit texture (§3) | as the camera | the pattern supplies texture (§3) | as stereo | as stereo | as stereo | low to medium |
| ToF camera | works / struggles in strong sun (§4) | — | multipath in corners, flying pixels at edges (§4) | $4.77\,\mathrm{mm}$ at $100\,\mathrm{MHz}$, wraps past $1.5\,\mathrm m$ (§4) | a range per pixel | $7.5\,\mathrm m$ unique with two frequencies | low to medium |
| structured light | works / sun can saturate it (§4) | — | needs its pattern visible | $\propto Z^2/(fb_p)$ (§4) | a range per pixel | short: contrast $\propto1/R^2$ (§4) | low |
| spinning LiDAR | works: own pulses (§5) | early and lost returns; dust seen at its leading edge (§5) | glass may vanish; dark returns $\propto\rho$ (§5) | $20\,\mathrm{mm}$, flat with range (§5) | $7.0\times34.9\,\mathrm{mm}$, $16\,\mathrm{mm}$ spots | $164$ points/m² at $10\,\mathrm m$, $7$ at $50$ (§10) | high |
| FMCW radar | works: own signal (§6) | sees through fog, dust, smoke; rain adds loss and clutter (§6) | sparse, noisy, ghosts (§6) | $15\,\mathrm{cm}$ cells (§6) | $0.33\,\mathrm m$ angle cells | $37.5\,\mathrm m$ in the course IF band | low to medium |

**Against S1's site.** Four conditions near the panel, and what each does to the rig:
- **Low morning sun on a glazed facade.** The camera exposes for the shaded panel and treats glints as missing data (§1); the LiDAR brings its own light but may lose the glass (§5). Bracketed exposures help only with the base stopped, because on the move each sees a different place (§9).
- **Dust from cutting.** A single-return LiDAR reports the cloud as a surface at its leading edge (§5), the camera loses contrast, the radar sees through — and a person walking out of the cloud is seen first by the radar, and seen moving (§6).
- **A night shift.** The cameras need light, and a strobe that lights only during a short exposure also removes §2's blur and skew; the LiDAR and radar do not notice the dark.
- **A row of identical panels.** Stereo can match the wrong panel and pass every geometric check (3.5 §2.6); the LiDAR is not fooled by paint, but a flat facade leaves ICP free to slide along it (3.5 §4).

The trap is to pick "the best sensor". The rig divides the work by physics instead: the LiDAR maps the approach, the radar watches for people in dust and dark, and the final $\pm5\,\mathrm{mm}$ of S1's hole belongs to the camera — close, at a short exposure, with its own light, stamped at mid-exposure, with the base stopped or its motion known to a few milliseconds (§9). The Worked case prices each clause.

### 8. Rigs: extrinsics between different sensors

*In one sentence:* a rig is one instrument only once every sensor's pose in one frame is known, and a rotation error between two sensors moves every projected point by a fixed angle — a fixed number of pixels, a growing number of millimetres.

**The problem.** The LiDAR measures $L$ in its own frame, the camera in its own; fusing them — colouring points, labelling LiDAR points from an image, checking one against the other — needs the transform between the two, and an error in it looks exactly like a disagreement between sensors. The idea: calibrate the transform with a target both can see, then check it with a test whose answer changes differently for rotation, translation and time.

**Calibrating it.** [[04-robotics/geometric-perception-calibration|3.5 §5]] calibrates a camera against a camera and against the gripper. A camera and a LiDAR use a shared target too, but see it differently — the camera its corners to a fraction of a pixel, which gives the target's pose in the camera's frame by PnP ([[04-robotics/geometric-perception-calibration|3.5 §2.7]]), the LiDAR its plane and edges through $16\,\mathrm{mm}$ spots $7$ by $35\,\mathrm{mm}$ apart. One documented workflow shows a checkerboard to both in many poses, finds its corners in both frames, estimates the rigid transform aligning them, checks it by projecting LiDAR points onto images, and calibrates the camera's intrinsics first ([MathWorks](https://www.mathworks.com/help/lidar/ug/lidar-and-camera-calibration.html)). The result is an extrinsic $T_{CL}=(R_{CL},t_{CL})$ from LiDAR to camera coordinates ([[02-foundations/se3-geometry|8. SE(3) §3]]). It is one fixed transform here only because P2 stays parked: with the arm moving, it would be the chain from the mast through P2's encoders and 3.5 §5's hand–eye transform to the camera, and its error would change with the pose. For the rig, the LiDAR's axes point forward, left and up and camera 1's right, down and forward, and the LiDAR sits $0.30\,\mathrm m$ above, which is $-0.30$ in the camera's downward $y$:

$$R_{CL}=\begin{pmatrix}0&-1&0\\0&0&-1\\1&0&0\end{pmatrix},\qquad t_{CL}=\begin{pmatrix}0\\-0.30\\0\end{pmatrix}\mathrm m$$

since each row of $R_{CL}$ names the LiDAR axis a camera axis equals. Inverting it puts $L$ at $p_L=R_{CL}^\top(L-t_{CL})=(2.0,\ -0.5,\ -0.5)\,\mathrm m$, $2.121\,\mathrm m$ away at elevation $-13.6^\circ$, inside the channels' $\pm15.5^\circ$.

> **Projection of a LiDAR point into an image, defined.** It is a *map from a 3D point in the LiDAR's frame to a camera pixel* — the step that colours clouds, labels LiDAR points from images, and checks a calibration. Four conditions: the **extrinsic** $T_{CL}$ is known and points LiDAR to camera; the camera's **intrinsics and distortion** are applied in 3.5 §1's order (normalize, distort, then $K$); the point and the image refer to **the same instant**, or the motion between them is corrected (§9); and the point is **visible to the camera**, not hidden behind something the LiDAR sees past.
>
> $$\lambda\begin{pmatrix}u\\v\\1\end{pmatrix}=K\big(R_{CL}\,p_L+t_{CL}\big)$$
>
> for the undistorted pixel, with $p_L$ the point in the LiDAR frame, $K$ camera 1's intrinsic matrix and $\lambda$ the point's depth in the camera frame, because it is 3.5 §1's camera equation with the LiDAR's frame in place of the world's.
>
> - **Example**: $L$ from $(2.0,\ -0.5,\ -0.5)$ lands on $(470,\ 300)$, where camera 1 sees it; in the raw, distorted image it belongs at 3.5's $(467.86,\ 299.15)$, $2.30$ px away, so skipping the distortion step misplaces it by that much, and more toward the corners.
> - **Non-example**: projecting without a visibility check. A scaffold tube $1.0\,\mathrm m$ in front of camera 1, on its axis, hides the facade point $(0,\ 0,\ 2.0)\,\mathrm m$ from the camera; the LiDAR, $0.30\,\mathrm m$ higher, sees it over the tube (its ray passes $0.15\,\mathrm m$ above the tube's axis), and projection paints the facade's $2.0\,\mathrm m$ onto pixel $(320,\ 240)$, which shows the tube at $1.0\,\mathrm m$.
> - **Why it matters**: learned pipelines trained on image-labelled LiDAR points, or on images with LiDAR depth, inherit this map's errors as label noise that is not noise — the same offset in every frame.

**What a degree does at range.** Give $R_{CL}$ a $1^\circ$ error about the vertical: $L$ moves $11.18$ px, a point at $10\,\mathrm m$ moves $10.51$ px, both near $f\,\delta\theta=10.47$ px, because a rotation turns every ray by the same angle. In millimetres it grows with distance from the axis: $36.0\,\mathrm{mm}$ at $L$ (3.5 §3's hand–eye number) and $174.7$ at $10\,\mathrm m$. A $1\,\mathrm{cm}$ translation error does the opposite: $1\,\mathrm{cm}$ at every range, $f\delta t/Z$ pixels — $3.00$ px at $2\,\mathrm m$, $0.60$ at $10$.

**The sanity check.** Project LiDAR points of a scene with sharp depth edges — a panel's edge, a column — onto the image and measure the offset between projected and image edges at two ranges. The same pixels near and far is a rotation; an offset shrinking with range is a translation; one that changes with the base's speed is not the extrinsic but time (§9). The trap is to run the check while moving: do it with the base stopped first, so time cannot pass for geometry.

### 9. Time: timestamps, triggers and clocks

*In one sentence:* every measurement is a position at an instant, and a fused point is off by the distance the rig moved during any error in that instant, $v\,\Delta t$ — an error the fusion cannot see, because it takes the stamps as true.

**The problem.** An image is taken over an interval (§2), a LiDAR cloud over a sweep (§5), and two sensors must agree on time as well as geometry (§8). Each sensor stamps its data with some clock's reading, and the fusion of [[04-robotics/state-estimation-slam|3. State Estimation]] puts the measurement where the rig was at that stamp. The idea: a wrong stamp is a wrong position, by exactly how far the rig moved.

**The one law.** If the stamp is $\Delta t$ off, the rig was $v\Delta t$ from where the fusion thinks:

$$e=v\,\Delta t$$

because in $\Delta t$ the rig covers $v\Delta t$; a rotation at $\omega$ adds $\omega\,\Delta t\,R$ at range $R$. At $0.5\,\mathrm{m/s}$ each millisecond is $0.5\,\mathrm{mm}$: $5\,\mathrm{mm}$ at $10\,\mathrm{ms}$ and $35\,\mathrm{mm}$ at P6's $70\,\mathrm{ms}$ budget — the $35\,\mathrm{mm}$ 3.2 §5 finds for a frame acted on late. At the facade $10\,\mathrm{ms}$ is $1.5$ px, exactly the blur of a $10\,\mathrm{ms}$ exposure: blur is this law smeared over the exposure.

> **Time offset, defined.** A **time offset** is a *signed error between a measurement's stamp and the instant the measurement describes*, or between two sensors' clocks — a bias in time, not jitter. Three conditions: each sensor has a defined **reference instant** — mid-exposure for an image (a row's mid-exposure under a rolling shutter), the firing time for a LiDAR point, the chirp frame for a radar detection; the stamps are read on a **common clock**, or clocks whose relation is known; and the rig or scene **moves** during $\Delta t$ — a stationary rig makes any offset harmless, which is why a static test cannot find one.
>
> $$e=v\,\Delta t\qquad(+\ \omega\,\Delta t\,R\ \text{for a rotation})$$
>
> where $v$ is the relative speed, $\Delta t$ the offset, $\omega$ the rotation rate and $R$ the range, so it is simply the distance the rig covered while the stamp was wrong.
>
> - **Example**: a driver that stamps the rig's image at the end of readout instead of mid-exposure is late by $t_{\exp}/2$ plus the readout, counted from the first row's mid-exposure, where a rolling-shutter model starts counting rows: $5+12=17\,\mathrm{ms}$ at a $10\,\mathrm{ms}$ exposure. A camera read that way on P6's cart at $0.5\,\mathrm{m/s}$ is $8.5\,\mathrm{mm}$ off, $5.1$ px at P6's camera, ten times its $0.833\,\mathrm{mm}$ noise.
> - **Non-example**: a known, constant latency is not an offset. P6's $70\,\mathrm{ms}$ from mid-exposure to force is a delay the controller budgets and predicts across ([[04-robotics/robot-systems-deployment|10. Robot Systems §3]]); what corrupts fusion is the part the stamps get wrong.
> - **Why it matters**: a filter compares each measurement with the state at its stamp, so an offset puts $v\Delta t$ into the innovation as if it were evidence — a bias no $R$ models (3.2 §1) — and it grows with speed, so a system tuned at a walk fails at a trot.

**Which instant is the image?** §2's streak is centred where the point was at mid-exposure, so that is the instant an image's geometry belongs to, and P6's budget starts there. A ROS image message asks only for the image's acquisition time ([`sensor_msgs/Image`](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/Image.msg)) without naming the instant, so a driver's stamp must be checked, not assumed. A rolling shutter gives each row its own mid-exposure, $12\,\mathrm{ms}$ apart top to bottom, and a LiDAR cloud's single stamp puts the column that sees $L$ $23.1\,\mathrm{mm}$ ($6.92$ px) off until it is deskewed (§5).

**Hardware triggering.** The cleanest offset is none: one electrical edge starts every exposure. A machine-vision camera can start an image on the rising edge of an input line, its exposure beginning after a delay, in microseconds, fixed by the model and its settings ([Basler, *Triggered Image Acquisition*](https://docs.baslerweb.com/triggered-image-acquisition); [*Exposure Start Delay*](https://docs.baslerweb.com/exposure-start-delay)) — a constant to subtract, not an unknown. KITTI's cameras are triggered by its laser scanner as the scanner faces forward ([KITTI](https://www.cvlibs.net/datasets/kitti/setup.php)), so each image is taken as the beam sweeps the scene it shows. For the rig the payoff is exact: two free-running cameras exposed $10\,\mathrm{ms}$ apart at $0.5\,\mathrm{m/s}$ put camera 2 $5\,\mathrm{mm}$ further along, a baseline of $0.125$ instead of $0.12\,\mathrm m$, a disparity of $37.50$ instead of $36$ px, and $L$ at $1.920\,\mathrm m$ — $80\,\mathrm{mm}$ short, twice §3's noise and always on one side. A shared trigger makes it zero.

**Clocks across devices.** Sensors on different computers, or free-running, need their clocks brought together. The Precision Time Protocol (IEEE 1588) synchronizes networked devices to the best clock among them, setting each local clock to the master's time and matching its frequency ([Basler, *PTP*](https://docs.baslerweb.com/precision-time-protocol)). Its core is an exchange of four stamps: the master sends Sync at $t_1$ (its time), the slave receives it at $t_2$ (its time), sends Delay_Req at $t_3$, and the master receives it at $t_4$. With the slave ahead by $\theta$ and one-way delay $d$ each way, $t_2-t_1=d+\theta$ and $t_4-t_3=d-\theta$, so

$$\hat\theta=\frac{(t_2-t_1)-(t_4-t_3)}{2},\qquad \hat d=\frac{(t_2-t_1)+(t_4-t_3)}{2}$$

because the difference cancels the delay and the sum cancels the offset. The trap is the assumption hidden in "$d$ each way": if the two directions differ, $\hat\theta$ is wrong by half their difference ([Nokia](https://documentation.nokia.com/html/0_add-h-f/93-0267-HTML/7X50_Advanced_Configuration_Guide/ACG-%20IEEE-1588-FP-TD.html)) — $30\,\mathrm{\mu s}$ for paths of $80$ and $20\,\mathrm{\mu s}$ in §10, harmless at $0.5\,\mathrm{m/s}$. The same four-stamp exchange in NTP's form, the networks that carry it and the shell commands that check it are [[02-foundations/tools/computer-networks|12.5 Computer Networks §10]] and [[02-foundations/tools/linux-shell|12.1 §11]].

> [!note]- Deeper · 더 깊이
> **How good, and how it drifts.** Demonstrations reported at NIST's 2004 IEEE 1588 conference synchronized devices to sub-microsecond accuracy ([NIST](https://www.nist.gov/publications/standard-precision-clock-synchronization-protocol-networked-measurement-and-control)); what a given network achieves depends on its hardware and setup (Basler). The asymmetry limits NTP-style synchronization too: the chrony project notes that an offset measured stable to nanoseconds can still be off by milliseconds from asymmetric delay ([chrony FAQ](https://chrony-project.org/faq.html)). Clocks also drift: two free-running clocks $50$ parts per million apart separate by $30\,\mathrm{ms}$ in ten minutes, $15\,\mathrm{mm}$ at $0.5\,\mathrm{m/s}$, so synchronization runs continuously, not once at start-up. The ROS 2 track's advice for the robot's own computers is [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]].

**Why fusion assumes it.** [[04-robotics/state-estimation-slam|3. State Estimation §8]] lists calibration, time stamps, the rolling shutter, latency and clock offset among the details that can dominate algorithmic gains, and its filters take every stamp as true. An estimator can carry a constant offset as a state — 3.5 §5's temporal calibration correlates motion signals — but the budget comes from the task: S1 gives the base $2\,\mathrm{mm}$ ([[05-construction-robotics/site-engineering|2.5 §2]]), which at $0.5\,\mathrm{m/s}$ is $4\,\mathrm{ms}$ of unexplained time for the whole rig. Either the rig's time is known that well, or the base stops before the hole is measured.

### Worked case · 대상으로 한 번 끝까지

The base rolls along S1's facade at $v=0.5\,\mathrm{m/s}$, $Z=2.0\,\mathrm m$ from it, and every sensor on the rig looks at $L$. Five steps — one per sensor and one for time — then the ledger against S1's $\pm5\,\mathrm{mm}$. Every number is a course computation on the frozen rig, and §10 prints each one.

**Step 1 — the camera.** Blur is $b=f\,v\,t_{\exp}/Z$ (§2). At the indoor $t_{\exp}=10\,\mathrm{ms}$: $b=600\times0.5\times0.010/2=1.50$ px, a $5.0\,\mathrm{mm}$ streak; the shade collects $S=200\times10=2{,}000\ e^-$ (SNR $44.3$, §1) and the sun $20{,}000$, twice the well, so the sunlit half is white. At $t_{\exp}=2\,\mathrm{ms}$: $b=0.30$ px ($1.0\,\mathrm{mm}$), the shade $400\ e^-$ at SNR $19.2$, the sun $4{,}000\ e^-$ at SNR $63.0$. The rolling shutter shears either frame by $f\,v\,(480\,t_{\text{row}})/Z=600\times0.5\times0.012/2=1.80$ px, $6.0\,\mathrm{mm}$ top to bottom. So the short exposure buys a sharp, unsaturated facade for less than half the shade's SNR, $19.2$ against $44.3$, and the skew stays.

**Step 2 — stereo.** With $\sigma_u=0.5$ px in each image, $\sigma_d=\sqrt2\times0.5=0.707$ px and $\sigma_Z=Z^2\sigma_d/(fb)=4\times0.707/72=39.3\,\mathrm{mm}$ along the ray (§3); across it, $Z\sigma_u/f=1.67\,\mathrm{mm}$. Exposed $10\,\mathrm{ms}$ apart, the pair behaves as if $b=0.12+0.5\times0.010=0.125\,\mathrm m$, reads a disparity of $600\times0.125/2=37.50$ px, and places $L$ at $72/37.5=1.920\,\mathrm m$: $80\,\mathrm{mm}$ short, twice the noise and always on one side (§9).

**Step 3 — the LiDAR.** Spacing $R\Delta\phi=2\times0.00349=7.0\,\mathrm{mm}$ along a ring and $R\Delta\varepsilon=34.9\,\mathrm{mm}$ between rings, spots $w_0+\theta R=10+3\times2=16\,\mathrm{mm}$, $4{,}104$ points/m², $\sigma_L=20\,\mathrm{mm}$ along each beam (§5). Its range error is half the stereo pair's here and an eighth at $4\,\mathrm m$ ($20$ against $157\,\mathrm{mm}$; equal at $1.43\,\mathrm m$), but its rings are ten times farther apart than the camera's $3.3\,\mathrm{mm}$ pixels. The column that sees $L$ fires $46.1\,\mathrm{ms}$ after the cloud's stamp: fused at the stamp, $L$ is $0.5\times46.1=23.1\,\mathrm{mm}$ off, $6.92$ px in camera 1; deskewed with its own time, the error goes.

**Step 4 — the radar.** Range cell $c/(2B)=14.99\,\mathrm{cm}$, angle cell $2/12\ \mathrm{rad}=9.55^\circ$, $0.33\,\mathrm m$ wide at the facade (§6). The worker $0.30\,\mathrm m$ before the facade is two range cells from it and separates for every phase §10 tries; walking toward the rig at $1.6\,\mathrm{m/s}$, they turn the echo's phase by $4\pi\times1.6\times50\,\mathrm{\mu s}/3.893\,\mathrm{mm}=0.258\,\mathrm{rad}$ per chirp, $1.6/0.304=5.26$ velocity cells from the static facade. None of this places $L$, which is somewhere in a cell $150\,\mathrm{mm}$ deep and $333\,\mathrm{mm}$ wide.

**Step 5 — time.** At $0.5\,\mathrm{m/s}$ each millisecond of stamp error is $0.5\,\mathrm{mm}$. A camera stamped at the end of readout is $5+12=17\,\mathrm{ms}$ late, $8.5\,\mathrm{mm}$ (§9). S1 gives the base $2\,\mathrm{mm}$ of its budget: $2/0.5=4\,\mathrm{ms}$ for the whole rig.

**The ledger.** Each error at the facade, and what removes it:

| Error at the facade | Size | What removes it |
|---|---:|---|
| camera, one feature across the ray ($\sigma_u=0.5$ px) | $1.67\,\mathrm{mm}$ | a closer camera, or more pixels |
| blur at $10\,\mathrm{ms}$ / $2\,\mathrm{ms}$ | $5.0$ / $1.0\,\mathrm{mm}$ | a short exposure, a strobe (§2) |
| rolling-shutter skew over the frame | $6.0\,\mathrm{mm}$ | a global shutter or a strobe (§2) |
| stereo depth, along the ray | $39.3\,\mathrm{mm}$ | a wider baseline or a shorter range (§3) |
| stereo pair $10\,\mathrm{ms}$ apart | $80\,\mathrm{mm}$ bias | a shared trigger (§9) |
| LiDAR noise / spot / ring spacing | $20$ / $16$ / $35\,\mathrm{mm}$ | none; use it for the approach (§5) |
| LiDAR column fused at the cloud's stamp | $23.1\,\mathrm{mm}$ | deskewing with column times (§5, §9) |
| radar cell | $150\times333\,\mathrm{mm}$ | none; use it for people (§6) |
| camera stamped at the end of readout | $8.5\,\mathrm{mm}$ | a mid-exposure stamp (§9) |

Only one measurement is inside S1's tolerance on its own — the camera's position across the ray, $1.67\,\mathrm{mm}$ — and it stays inside only with the $2\,\mathrm{ms}$ exposure's $1.0\,\mathrm{mm}$ of blur, a true stamp and the $4\,\mathrm{ms}$ time budget. Every other sensor contributes what the camera cannot, and none of it is the hole's position: §7's division of labour, now with its numbers.

### 10. The lab: the rig's errors, sensor by sensor

The listing runs §1–§9 on the frozen rig, one numbered part per section, and prints every number the Worked case used. Two parts go beyond the formulas: Part 3 checks the first-order stereo law against $200{,}000$ simulated disparities, and Part 6 separates two radar echoes in one chirp's spectrum for five bandwidths, at $36$ relative phases each. Nothing is timed and the one random draw is seeded, so the output is the same on any machine.

```python
# 3.6 lab: the rig passing S1's facade, sensor by sensor. NumPy only; every number is the model's.
import numpy as np

C = 299_792_458.0                          # speed of light in m/s, exact (NIST)
# --- frozen on other pages: 3.5's wrist rig, 3.2's pixel noise and P6's camera ------------------
F, CX, CY, BASE = 600.0, 320.0, 240.0, 0.12  # focal length and principal point (px), baseline (m)
L = np.array([0.5, 0.2, 2.0])              # the landmark in camera 1's frame (m)
SIGMA_U, Z_P6 = 0.5, 1.0                   # feature noise in one image (px); P6's camera-to-rail (m)
# --- this page's course numbers (Running object) -----------------------------------------------
V, Z = 0.5, 2.0                            # base speed along the facade (m/s); facade distance (m)
FWC, READ, DARK, E_PER_DN = 10_000.0, 5.0, 100.0, 10.0   # full well, read noise (e-), dark (e-/s), e-/DN
PHI = {"shade": 200.0, "sun": 2_000.0, "glint": 2.0e6}   # photoelectrons per pixel per ms at f/2
T_ROW, ROWS = 25e-6, 480                   # rolling-shutter row delay (s) and rows
LID = dict(ch=32, d_el=1.0, d_az=0.2, rot=10.0, sigma=0.020, div=3.0e-3, w0=0.010)
RAD = dict(fc=77e9, B=1.0e9, Tc=50e-6, fs=10e6, chirps=128, virt=12)

# --- 1. the pixel: signal, noise, saturation --------------------------------------------------
SQ = E_PER_DN / np.sqrt(12)                # quantization noise of the converter, e-

def pixel(phi_per_ms, t_ms):
    """Mean signal (e-) and SNR of one pixel; SNR is None once the well is full."""
    S = phi_per_ms * t_ms
    if S >= FWC:
        return S, None
    return S, S / np.sqrt(S + DARK * t_ms * 1e-3 + READ**2 + SQ**2)

def blur_px(v, t_s, z):                    # image smear of a point moving parallel to the image plane
    return F * v * t_s / z

floor = np.hypot(READ, SQ)
print("1. DR = FWC/read = %.0f (%.1f dB, %.2f stops); with the ADC's step %.0f (%.1f dB)"
      % (FWC / READ, 20 * np.log10(FWC / READ), np.log2(FWC / READ), FWC / floor, 20 * np.log10(FWC / floor)))
for t_ms in (0.5, 1.0, 2.0, 5.0, 10.0, 20.0):
    cells = []
    for name in ("shade", "sun", "glint"):
        S, snr = pixel(PHI[name], t_ms)
        cells.append("%s %s" % (name, "saturated" if snr is None else "SNR %4.1f" % snr))
    print("   t_exp %4.1f ms | %s | blur %.2f px" % (t_ms, " | ".join(cells), blur_px(V, t_ms * 1e-3, Z)))
lo, hi = 1e-4, 20.0                        # shortest exposure giving SNR >= 10 in the shade
for _ in range(100):
    mid = (lo + hi) / 2
    lo, hi = (mid, hi) if pixel(PHI["shade"], mid)[1] < 10 else (lo, mid)
print("   window: SNR>=10 in shade from %.3f ms; blur<=0.5 px up to %.3f ms; sun unsaturated up to %.1f ms"
      % (hi, 0.5 * Z / (F * V) * 1e3, FWC / PHI["sun"]))
t_glint = FWC / PHI["glint"]
print("   glint unsaturated only below %.4f ms, where the shade holds %.1f e- (SNR %.2f)"
      % (t_glint, PHI["shade"] * t_glint, pixel(PHI["shade"], t_glint)[1]))
full4, sq4 = 1023 * E_PER_DN / 4, E_PER_DN / 4 / np.sqrt(12)
print("   gain x4: full scale %.0f e-, floor %.2f e-, DR %.0f (%.1f dB)"
      % (full4, np.hypot(READ, sq4), full4 / np.hypot(READ, sq4), 20 * np.log10(full4 / np.hypot(READ, sq4))))

# --- 2. motion blur and rolling-shutter skew --------------------------------------------------
readout = ROWS * T_ROW
for v in (0.25, 0.5, 1.0):
    print("2. v %.2f m/s | blur px at 1/2/5/10/20 ms: %s | skew over the frame %.2f px (%.1f mm)"
          % (v, " ".join("%.2f" % blur_px(v, t * 1e-3, Z) for t in (1, 2, 5, 10, 20)),
             blur_px(v, readout, Z), v * readout * 1e3))
print("   P6's camera at %.1f m, 0.5 m/s, 10 ms: blur %.1f px against sigma_u %.1f px" % (Z_P6, blur_px(V, 0.010, Z_P6), SIGMA_U))

# --- 3. stereo depth error against range and baseline -----------------------------------------
sigma_d = np.sqrt(2) * SIGMA_U             # a disparity is the difference of two pixel positions
noise = sigma_d * np.random.default_rng(36).standard_normal(200_000)
for z in (1.0, 2.0, 4.0, 8.0):
    first = ["%6.1f" % (z**2 * sigma_d / (F * b) * 1e3) for b in (0.06, 0.12, 0.24)]
    zs = F * BASE / (F * BASE / z + noise)  # simulated depths at the rig's baseline
    print("3. Z %.0f m | sigma_Z mm at b = 0.06/0.12/0.24 m: %s | simulated at 0.12: std %6.1f, bias %+5.1f mm"
          % (z, " ".join(first), zs.std() * 1e3, (zs.mean() - z) * 1e3))
print("   stereo equals the LiDAR's 20 mm at Z = %.2f m; near limit for a 128 px search: %.3f m (b 0.12), %.3f m (b 0.24)"
      % (np.sqrt(LID["sigma"] * F * BASE / sigma_d), F * 0.12 / 128, F * 0.24 / 128))
for dt in (1e-3, 10e-3):                   # a pair exposed dt apart: the baseline grows by v*dt
    d = F * (BASE + V * dt) / Z
    print("   pair %2.0f ms apart at 0.5 m/s: disparity %.2f px, depth read %.4f m (%+.1f mm)"
          % (dt * 1e3, d, F * BASE / d, (F * BASE / d - Z) * 1e3))

# --- 4. time of flight: pulse timing, phase wrapping, two frequencies -------------------------
print("4. 1 ns = %.4f m of range; P5's 12 cm = %.3f ns; sigma 10 mm = %.1f ps; offset 4 mm = %.1f ps; 20 mm = %.0f ps"
      % (C * 1e-9 / 2, 2 * 0.12 / C * 1e9, 2 * 0.010 / C * 1e12, 2 * 0.004 / C * 1e12, 2 * 0.020 / C * 1e12))
for fm in (20e6, 80e6, 100e6):
    amb = C / (2 * fm)
    print("   f_mod %3.0f MHz: unique to %.3f m, sigma %.2f mm at 0.02 rad, the facade at 2.000 m reads %.3f m"
          % (fm / 1e6, amb, C * 0.02 / (4 * np.pi * fm) * 1e3, Z % amb))
a1, a2 = C / (2 * 100e6), C / (2 * 80e6)
best = min((abs((Z % a1 + i * a1) - (Z % a2 + j * a2)), Z % a1 + i * a1) for i in range(5) for j in range(4))
print("   100 and 80 MHz together: unique to %.3f m; the two readings agree at %.3f m"
      % (C / (2 * np.gcd(100, 80) * 1e6), best[1]))

# --- 5. LiDAR: footprint, spacing, density, sweep smear ---------------------------------------
cols = 360.0 / LID["d_az"]
print("5. %d columns x %d channels at %.0f Hz = %d points/s" % (cols, LID["ch"], LID["rot"], cols * LID["ch"] * LID["rot"]))
for r in (1.0, 2.0, 5.0, 10.0, 20.0, 50.0):
    sh, sv = r * np.radians(LID["d_az"]), r * np.radians(LID["d_el"])
    w = LID["w0"] + LID["div"] * r
    print("   R %4.0f m | spacing %6.1f x %6.1f mm | footprint %5.1f mm | %6.0f points/m^2 | stereo sigma_Z %7.1f mm"
          % (r, sh * 1e3, sv * 1e3, w * 1e3, 1 / (sh * sv), r**2 * sigma_d / (F * BASE) * 1e3))
for span in (90.0, 120.0, 360.0):
    print("   sweep across %3.0f deg: %5.1f ms, facade smeared %.1f mm at 0.5 m/s"
          % (span, span / 360 / LID["rot"] * 1e3, V * span / 360 / LID["rot"] * 1e3))

# --- 6. FMCW radar: range cell, two reflectors, Doppler, angle --------------------------------
lam = C / RAD["fc"]
n = int(round(RAD["fs"] * RAD["Tc"]))      # samples per chirp
t = np.arange(n) / RAD["fs"]

def two_reflectors(sep, phi, B, r1=2.0):
    """True if reflectors at r1 and r1 - sep give two peaks, each within a quarter cell, 3 dB apart."""
    S, cell = B / RAD["Tc"], C / (2 * B)
    r2 = r1 - sep
    s = np.exp(2j * np.pi * (2 * S * r1 / C) * t) + np.exp(1j * (2 * np.pi * (2 * S * r2 / C) * t + phi))
    X = np.abs(np.fft.fft(s, 1 << 14))     # zero-padded spectrum of one chirp
    r = np.fft.fftfreq(1 << 14, 1 / RAD["fs"]) * C / (2 * S)
    keep = (r > r2 - 0.5) & (r < r1 + 0.5)
    o = np.argsort(r[keep]); r, X = r[keep][o], X[keep][o]
    pk = [i for i in range(1, len(X) - 1) if X[i] > X[i - 1] and X[i] >= X[i + 1] and X[i] > 0.5 * X.max()]
    near = [min(pk, key=lambda i: abs(r[i] - rr)) for rr in (r2, r1)]
    if near[0] == near[1] or any(abs(r[i] - rr) > cell / 4 for i, rr in zip(near, (r2, r1))):
        return False
    return bool(X[near[0]:near[1] + 1].min() < min(X[near[0]], X[near[1]]) / np.sqrt(2))

phases = np.radians(np.arange(0, 360, 10))  # 36 relative phases of the two echoes
for B in (0.25e9, 0.5e9, 1e9, 2e9, 4e9):
    S, cell = B / RAD["Tc"], C / (2 * B)
    print("6. B %.2f GHz | cell %4.1f cm | slope %2.0f MHz/us | beat at 2 m %6.1f kHz | worker 0.30 m before the"
          " facade: %.1f cells, separated for %2d of 36 phases" % (B / 1e9, cell * 100, S / 1e12, 2 * S * Z / C / 1e3,
                                                                   0.30 / cell, sum(two_reflectors(0.30, p, B) for p in phases)))
cell = C / (2 * RAD["B"])
for k in (0.5, 1.0, 1.5, 2.0):
    print("   1 GHz, echoes %.1f cells apart: separated for %2d of 36 phases"
          % (k, sum(two_reflectors(k * cell, p, RAD["B"]) for p in phases)))
S = RAD["B"] / RAD["Tc"]
echo = lambda k, v: np.exp(1j * (2 * np.pi * (2 * S * Z / C) * t + 4 * np.pi * (Z + v * k * RAD["Tc"]) / lam))
dphi = np.angle(np.vdot(np.fft.fft(echo(0, -1.6)), np.fft.fft(echo(1, -1.6))))   # worker closing at 1.6 m/s
print("   Doppler: %.4f rad per chirp -> range rate %.3f m/s | v_res %.3f m/s | v_max %.2f m/s | IF 5 MHz -> %.1f m"
      % (dphi, lam * dphi / (4 * np.pi * RAD["Tc"]), lam / (2 * RAD["chirps"] * RAD["Tc"]), lam / (4 * RAD["Tc"]),
         RAD["fs"] / 2 * C / (2 * S)))
print("   angle cell %.2f deg: %.2f m wide at 2 m, %.2f m at 10 m" % (np.degrees(2 / RAD["virt"]), 2 * 2 / RAD["virt"], 10 * 2 / RAD["virt"]))

# --- 7. time: the fused-point error, one PTP exchange, clock drift -----------------------------
for v in (0.25, 0.5, 1.0):
    print("7. v %.2f m/s | error mm at dt = 1/5/10/20/50/70 ms: %s | px at 2 m per 10 ms: %.2f"
          % (v, " ".join("%5.2f" % (v * dt) for dt in (1, 5, 10, 20, 50, 70)), F * v * 0.010 / Z))
late = 0.010 / 2 + readout                 # stamped at the end of readout instead of mid-exposure
print("   end-of-readout stamp: %.0f ms late -> %.1f mm, %.1f px on P6's camera (%.1f sigma_p)"
      % (late * 1e3, V * late * 1e3, F * V * late / Z_P6, V * late / (Z_P6 * SIGMA_U / F)))
theta = 3.000e-3                           # the slave clock's true offset (s)
for d_ms, d_sm in ((50e-6, 50e-6), (80e-6, 20e-6)):
    t1 = 0.0; t2 = t1 + d_ms + theta       # Sync: sent at master time t1, received at slave time t2
    t3 = 0.010; t4 = t3 - theta + d_sm     # Delay_Req: sent at slave time t3, received at master time t4
    off, delay = ((t2 - t1) - (t4 - t3)) / 2, ((t2 - t1) + (t4 - t3)) / 2
    print("   PTP, paths %2.0f/%2.0f us: offset %.1f us (true %.1f), mean path delay %.1f us, error %.1f us"
          % (d_ms * 1e6, d_sm * 1e6, off * 1e6, theta * 1e6, delay * 1e6, (off - theta) * 1e6))
print("   two free-running clocks 50 ppm apart: %.0f ms after 10 min -> %.0f mm at 0.5 m/s" % (50e-6 * 600 * 1e3, V * 50e-6 * 600 * 1e3))

# --- 8. LiDAR points into the image: the round trip, a 1 degree and a 1 cm extrinsic error -----
K = np.array(((F, 0, CX), (0, F, CY), (0, 0, 1.0)))
R_CL = np.array(((0, -1, 0), (0, 0, -1), (1, 0, 0)), float)   # LiDAR axes (fwd, left, up) -> camera axes
t_CL = np.array([0.0, -0.30, 0.0])                              # the LiDAR 0.30 m above camera 1

def project(p_lidar, R=R_CL, tr=t_CL):
    q = K @ (R @ p_lidar + tr)
    return q[:2] / q[2]

p_L = R_CL.T @ (L - t_CL)
print("8. L in the LiDAR frame", np.round(p_L, 3), "range %.3f m -> pixel" % np.linalg.norm(p_L), np.round(project(p_L), 2))
c1, s1 = np.cos(np.radians(1.0)), np.sin(np.radians(1.0))
yaw = np.array(((c1, 0, s1), (0, 1, 0), (-s1, 0, c1)))       # 1 degree about the camera's vertical axis
for z in (2.0, 10.0):
    p = R_CL.T @ (np.array([0.5, 0.2, z]) - t_CL)
    moved = np.linalg.norm(yaw @ R_CL @ p - R_CL @ p)
    print("   point at Z %4.1f m: 1 deg -> %5.2f px (%5.1f mm) | 1 cm -> %4.2f px (10.0 mm)"
          % (z, np.linalg.norm(project(p, yaw @ R_CL) - project(p)), moved * 1e3,
             np.linalg.norm(project(p, R_CL, t_CL + np.array([0.01, 0, 0])) - project(p))))
az = np.degrees(np.arctan2(p_L[1], p_L[0]))
t_col = ((az - 180.0) % 360.0) / 360.0 / LID["rot"]   # the sweep starts at the rear and turns left
print("   L's column fires %.1f ms after the cloud's stamp: %.1f mm, %.2f px if fused at the stamp"
      % (t_col * 1e3, V * t_col * 1e3, F * V * t_col / Z))
```

It prints, unedited:

```text
1. DR = FWC/read = 2000 (66.0 dB, 10.97 stops); with the ADC's step 1732 (64.8 dB)
   t_exp  0.5 ms | shade SNR  8.7 | sun SNR 31.1 | glint saturated | blur 0.07 px
   t_exp  1.0 ms | shade SNR 13.1 | sun SNR 44.4 | glint saturated | blur 0.15 px
   t_exp  2.0 ms | shade SNR 19.2 | sun SNR 63.0 | glint saturated | blur 0.30 px
   t_exp  5.0 ms | shade SNR 31.1 | sun saturated | glint saturated | blur 0.75 px
   t_exp 10.0 ms | shade SNR 44.3 | sun saturated | glint saturated | blur 1.50 px
   t_exp 20.0 ms | shade SNR 63.0 | sun saturated | glint saturated | blur 3.00 px
   window: SNR>=10 in shade from 0.632 ms; blur<=0.5 px up to 3.333 ms; sun unsaturated up to 5.0 ms
   glint unsaturated only below 0.0050 ms, where the shade holds 1.0 e- (SNR 0.17)
   gain x4: full scale 2558 e-, floor 5.05 e-, DR 506 (54.1 dB)
2. v 0.25 m/s | blur px at 1/2/5/10/20 ms: 0.07 0.15 0.38 0.75 1.50 | skew over the frame 0.90 px (3.0 mm)
2. v 0.50 m/s | blur px at 1/2/5/10/20 ms: 0.15 0.30 0.75 1.50 3.00 | skew over the frame 1.80 px (6.0 mm)
2. v 1.00 m/s | blur px at 1/2/5/10/20 ms: 0.30 0.60 1.50 3.00 6.00 | skew over the frame 3.60 px (12.0 mm)
   P6's camera at 1.0 m, 0.5 m/s, 10 ms: blur 3.0 px against sigma_u 0.5 px
3. Z 1 m | sigma_Z mm at b = 0.06/0.12/0.24 m:   19.6    9.8    4.9 | simulated at 0.12: std    9.8, bias  +0.1 mm
3. Z 2 m | sigma_Z mm at b = 0.06/0.12/0.24 m:   78.6   39.3   19.6 | simulated at 0.12: std   39.3, bias  +0.7 mm
3. Z 4 m | sigma_Z mm at b = 0.06/0.12/0.24 m:  314.3  157.1   78.6 | simulated at 0.12: std  158.0, bias  +6.0 mm
3. Z 8 m | sigma_Z mm at b = 0.06/0.12/0.24 m: 1257.1  628.5  314.3 | simulated at 0.12: std  644.3, bias +49.4 mm
   stereo equals the LiDAR's 20 mm at Z = 1.43 m; near limit for a 128 px search: 0.562 m (b 0.12), 1.125 m (b 0.24)
   pair  1 ms apart at 0.5 m/s: disparity 36.15 px, depth read 1.9917 m (-8.3 mm)
   pair 10 ms apart at 0.5 m/s: disparity 37.50 px, depth read 1.9200 m (-80.0 mm)
4. 1 ns = 0.1499 m of range; P5's 12 cm = 0.801 ns; sigma 10 mm = 66.7 ps; offset 4 mm = 26.7 ps; 20 mm = 133 ps
   f_mod  20 MHz: unique to 7.495 m, sigma 23.86 mm at 0.02 rad, the facade at 2.000 m reads 2.000 m
   f_mod  80 MHz: unique to 1.874 m, sigma 5.96 mm at 0.02 rad, the facade at 2.000 m reads 0.126 m
   f_mod 100 MHz: unique to 1.499 m, sigma 4.77 mm at 0.02 rad, the facade at 2.000 m reads 0.501 m
   100 and 80 MHz together: unique to 7.495 m; the two readings agree at 2.000 m
5. 1800 columns x 32 channels at 10 Hz = 576000 points/s
   R    1 m | spacing    3.5 x   17.5 mm | footprint  13.0 mm |  16414 points/m^2 | stereo sigma_Z     9.8 mm
   R    2 m | spacing    7.0 x   34.9 mm | footprint  16.0 mm |   4104 points/m^2 | stereo sigma_Z    39.3 mm
   R    5 m | spacing   17.5 x   87.3 mm | footprint  25.0 mm |    657 points/m^2 | stereo sigma_Z   245.5 mm
   R   10 m | spacing   34.9 x  174.5 mm | footprint  40.0 mm |    164 points/m^2 | stereo sigma_Z   982.1 mm
   R   20 m | spacing   69.8 x  349.1 mm | footprint  70.0 mm |     41 points/m^2 | stereo sigma_Z  3928.4 mm
   R   50 m | spacing  174.5 x  872.7 mm | footprint 160.0 mm |      7 points/m^2 | stereo sigma_Z 24552.3 mm
   sweep across  90 deg:  25.0 ms, facade smeared 12.5 mm at 0.5 m/s
   sweep across 120 deg:  33.3 ms, facade smeared 16.7 mm at 0.5 m/s
   sweep across 360 deg: 100.0 ms, facade smeared 50.0 mm at 0.5 m/s
6. B 0.25 GHz | cell 60.0 cm | slope  5 MHz/us | beat at 2 m   66.7 kHz | worker 0.30 m before the facade: 0.5 cells, separated for  0 of 36 phases
6. B 0.50 GHz | cell 30.0 cm | slope 10 MHz/us | beat at 2 m  133.4 kHz | worker 0.30 m before the facade: 1.0 cells, separated for 13 of 36 phases
6. B 1.00 GHz | cell 15.0 cm | slope 20 MHz/us | beat at 2 m  266.9 kHz | worker 0.30 m before the facade: 2.0 cells, separated for 36 of 36 phases
6. B 2.00 GHz | cell  7.5 cm | slope 40 MHz/us | beat at 2 m  533.7 kHz | worker 0.30 m before the facade: 4.0 cells, separated for 36 of 36 phases
6. B 4.00 GHz | cell  3.7 cm | slope 80 MHz/us | beat at 2 m 1067.4 kHz | worker 0.30 m before the facade: 8.0 cells, separated for 36 of 36 phases
   1 GHz, echoes 0.5 cells apart: separated for  0 of 36 phases
   1 GHz, echoes 1.0 cells apart: separated for 13 of 36 phases
   1 GHz, echoes 1.5 cells apart: separated for 31 of 36 phases
   1 GHz, echoes 2.0 cells apart: separated for 36 of 36 phases
   Doppler: -0.2582 rad per chirp -> range rate -1.600 m/s | v_res 0.304 m/s | v_max 19.47 m/s | IF 5 MHz -> 37.5 m
   angle cell 9.55 deg: 0.33 m wide at 2 m, 1.67 m at 10 m
7. v 0.25 m/s | error mm at dt = 1/5/10/20/50/70 ms:  0.25  1.25  2.50  5.00 12.50 17.50 | px at 2 m per 10 ms: 0.75
7. v 0.50 m/s | error mm at dt = 1/5/10/20/50/70 ms:  0.50  2.50  5.00 10.00 25.00 35.00 | px at 2 m per 10 ms: 1.50
7. v 1.00 m/s | error mm at dt = 1/5/10/20/50/70 ms:  1.00  5.00 10.00 20.00 50.00 70.00 | px at 2 m per 10 ms: 3.00
   end-of-readout stamp: 17 ms late -> 8.5 mm, 5.1 px on P6's camera (10.2 sigma_p)
   PTP, paths 50/50 us: offset 3000.0 us (true 3000.0), mean path delay 50.0 us, error 0.0 us
   PTP, paths 80/20 us: offset 3030.0 us (true 3000.0), mean path delay 50.0 us, error 30.0 us
   two free-running clocks 50 ppm apart: 30 ms after 10 min -> 15 mm at 0.5 m/s
8. L in the LiDAR frame [ 2.  -0.5 -0.5] range 2.121 m -> pixel [470. 300.]
   point at Z  2.0 m: 1 deg -> 11.18 px ( 36.0 mm) | 1 cm -> 3.00 px (10.0 mm)
   point at Z 10.0 m: 1 deg -> 10.51 px (174.7 mm) | 1 cm -> 0.60 px (10.0 mm)
   L's column fires 46.1 ms after the cloud's stamp: 23.1 mm, 6.92 px if fused at the stamp
```

**What the output says.**
- **Exposure is a window, and speed closes it.** The shade needs $0.632\,\mathrm{ms}$ for an SNR of $10$; half a pixel of blur allows $3.333\,\mathrm{ms}$ at $0.5\,\mathrm{m/s}$, and the $1.0\,\mathrm{m/s}$ row shows the $2\,\mathrm{ms}$ exposure already at $0.60$ px. The glint is in no window: $80\,\mathrm{dB}$ of scene against $66$ of sensor.
- **Stereo's error is a square law, the LiDAR's is flat.** They cross at $1.43\,\mathrm m$; at $8\,\mathrm m$ stereo is $31$ times worse and, being convex, biased by $+49.4\,\mathrm{mm}$ — the simulation shows the bias, the first-order law cannot.
- **A LiDAR's density falls as $1/R^2$ while its spots grow as $R$.** At $20\,\mathrm m$ the spot and the column step are both $70\,\mathrm{mm}$; at $50\,\mathrm m$ the spots no longer touch along a ring.
- **Range resolution is a threshold, not a guarantee.** Two echoes one cell apart separate for $13$ of $36$ phases, two cells apart for all; only the bandwidth moves the cell.
- **Every timing error is $v\,\Delta t$.** A late camera stamp, a cloud's single stamp, a free-running pair and a drifting clock are four causes of the same $0.5\,\mathrm{mm}$ per millisecond.

### 11. What this page does not cover

Sensors a site robot may also carry: thermal and event cameras, ultrasonic rangers, GNSS ([[04-robotics/state-estimation-slam|3 §8]]), the IMU ([[04-robotics/sensor-models|3.2]]), touch ([[04-robotics/tactile-visuotactile|14]]). Lens design beyond 3.5's distortion model, colour and demosaicing, auto-exposure algorithms, radar processing beyond one FFT, and what is done with a point cloud afterwards (3.5 §3–§4, [[05-construction-robotics/site-perception|5. Site Perception]]). Stamped transforms, drivers and the networks that carry their data belong to the ROS 2 track ([[04-robotics/ros2/describing-a-robot|25.6]] for frames and stamps, [[04-robotics/ros2/from-simulation-to-hardware|25.11]] for drivers and networks).

### After reading

You should be able to:

- turn a scene's light into photoelectrons with the f-number and the exposure, and electrons into an SNR, and say from a scene's brightness ratio in dB whether one exposure can hold it;
- compute motion blur and rolling-shutter skew, and find the exposure window of a moving rig;
- derive $\sigma_Z=Z^2\sigma_d/(fb)$ with $\sigma_d=\sqrt2\,\sigma_u$, and find where stereo and a LiDAR cross;
- convert a time-of-flight delay or phase to a range, and unwrap a phase with two frequencies;
- compute a LiDAR's spacing, footprint and density at a range, and say what dust, rain, dark and glass do to it;
- derive an FMCW radar's beat, range cell, velocity cell and angle cell, and say what it can and cannot separate;
- project a LiDAR point into an image, and tell rotation, translation and time apart by how an offset behaves;
- price any wrong stamp as $v\,\Delta t$, estimate a clock offset from four PTP stamps, and say what an asymmetric path does;
- give each sensor on a site rig the job its physics allows.

### Self-check

1. The rig's camera runs at $5\,\mathrm{ms}$ while the base moves at $1.0\,\mathrm{m/s}$. What are the shade's SNR, the blur at $2\,\mathrm m$, and the state of the sunlit half?
2. Someone doubles the analog gain to brighten a dark scene at a fixed exposure. What happens to the shot-noise-limited SNR, and to the dynamic range?
3. Why does halving the stereo baseline double the depth error, while doubling the range quadruples it?
4. A $100\,\mathrm{MHz}$ time-of-flight camera reads $0.50\,\mathrm m$ on a facade you know is about $2\,\mathrm m$ away. What happened, and how would you catch it?
5. The radar shows one object where a worker stands $10\,\mathrm{cm}$ in front of the facade. What would separate them, and what would not?
6. Projected LiDAR edges sit $10$ px right of the image edges at $3\,\mathrm m$ and at $12\,\mathrm m$. Rotation, translation or time — and how do you confirm it?

> [!tip]- Answers
> 1. The shade collects $200\times5=1{,}000\ e^-$, SNR $31.1$; the blur is $600\times1.0\times0.005/2=1.5$ px; and the sun collects $2{,}000\times5=10{,}000\ e^-$, exactly the full well, so it saturates. The window at $1.0\,\mathrm{m/s}$ runs from the shade's $0.632\,\mathrm{ms}$ (unchanged, since the SNR does not depend on speed) to half a pixel of blur at $0.5\times2/(600\times1.0)=1.67\,\mathrm{ms}$, so $5\,\mathrm{ms}$ misses it twice.
> 2. The SNR is unchanged: gain multiplies the collected electrons and their noise alike and adds no photons. The dynamic range falls, because the converter's full scale now corresponds to half as many electrons, $5{,}115$, while the floor barely moves: $983$, $59.9\,\mathrm{dB}$ instead of $64.8$ (§1's Deeper note works $\times4$: $54.1\,\mathrm{dB}$).
> 3. $\sigma_Z=Z^2\sigma_d/(fb)$: the baseline appears once, so halving it doubles the error; the range appears squared — once because the disparity itself shrinks as $1/Z$, and once because each pixel of disparity is worth more depth as $Z$ grows, $|dZ/dd|=Z^2/(fb)$.
> 4. The phase wrapped: at $100\,\mathrm{MHz}$ the range is unique only to $1.499\,\mathrm m$, and $2.0-1.499=0.501\,\mathrm m$. A second frequency catches it (at $80\,\mathrm{MHz}$ the reading is $0.126\,\mathrm m$, and only $2.000\,\mathrm m$ fits both), and so does any independent range — a prior, the stereo pair, the LiDAR.
> 5. $10\,\mathrm{cm}$ is two thirds of a $15\,\mathrm{cm}$ cell, so range does not separate them at $1\,\mathrm{GHz}$; $4\,\mathrm{GHz}$ would ($3.75\,\mathrm{cm}$ cells, nearly three apart). Walking toward the radar, Doppler separates them in one frame; standing still, it does not; and the $0.33\,\mathrm m$ angle cell at $2\,\mathrm m$ does not separate two things in the same direction.
> 6. The same pixels near and far is a rotation: $10$ px is about $f\,\delta\theta$, so $\delta\theta\approx10/600\ \mathrm{rad}=0.95^\circ$; a translation would shrink fourfold from $3$ to $12\,\mathrm m$. Confirm with the base stopped, so no time offset can contribute, and check the offset does not change with speed.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and the plant catalog. The Worked case ran the rig at $0.5\,\mathrm{m/s}$ past a facade $2\,\mathrm m$ away. This set changes seven numbers and keeps the rest: the base moves at $1.0\,\mathrm{m/s}$, the facade is $4.0\,\mathrm m$ away, the stereo baseline is $0.24\,\mathrm m$, the exposure is $2\,\mathrm{ms}$, and the LiDAR spins at $20\,\mathrm{Hz}$ with the same points per second, so its columns are $0.4^\circ$ apart; the radar sweeps $4\,\mathrm{GHz}$ with $256$ chirps.

1. **Draw.** The picture for the variant: the plan with the facade at $4\,\mathrm m$, the stereo error bar along the ray to a point on it, the radar cell there, and the LiDAR's $120^\circ$ sweep with its time and smear; and the facade patch around that point with the camera's pixels, the LiDAR's spots and rings, the $2\,\mathrm{ms}$ blur, the end-of-readout stamp's error and S1's $\pm5\,\mathrm{mm}$, all to one scale.
2. **Derive.** (a) From $Z=fb/d$ and independent errors $\sigma_u$ in each image, derive $\sigma_Z=\sqrt2\,Z^2\sigma_u/(fb)$; evaluate it at $4\,\mathrm m$ for $b=0.12$ and $0.24\,\mathrm m$, find where the wider pair equals the LiDAR's $20\,\mathrm{mm}$, and give its near limit for a $128$-px search. (b) The blur and skew at $1.0\,\mathrm{m/s}$, $4\,\mathrm m$, $2\,\mathrm{ms}$, in pixels and millimetres, and why the pixels equal the Worked case's short-exposure values. (c) The LiDAR at $20\,\mathrm{Hz}$: spacing, footprint and density at $4\,\mathrm m$, and the time and smear of a $120^\circ$ sweep. (d) The radar at $4\,\mathrm{GHz}$, $T_c=50\,\mathrm{\mu s}$: range cell, slope, beat at $4\,\mathrm m$, the reach of the $5\,\mathrm{MHz}$ IF band, and the velocity cell with $256$ chirps. (e) §4's ToF camera at $4\,\mathrm m$: each frequency's wrapped reading and the range both agree on. (f) A camera stamped at the end of readout at the $2\,\mathrm{ms}$ exposure: how late, and how far off at $1.0\,\mathrm{m/s}$, in mm and in pixels at $4\,\mathrm m$; and the PTP offset's error on paths of $90$ and $10\,\mathrm{\mu s}$.
3. **Do.** Fill the `?` blanks — each is a formula its comment names — run the variant, set each printed number beside the Worked case's, and say which errors the variant made worse, which better, and which it left unchanged in pixels.

```python
# Problem 3 (Do). The variant: base at 1.0 m/s, facade at 4.0 m, baseline 0.24 m, 2 ms exposure. Fill ?.
import numpy as np

C, F = 299_792_458.0, 600.0
V, Z, BASE, T_EXP = 1.0, 4.0, 0.24, 2e-3
SIGMA_D = np.sqrt(2) * 0.5                  # 3.2's 0.5 px in each image
T_ROW, ROWS = 25e-6, 480

def blur_px(v, t_s, z):
    return ?                                 # section 2: smear in pixels
def sigma_z(z, b, sigma_d=SIGMA_D):
    return ?                                 # section 3: first-order depth error, m
def spacing_mm(r, step_deg):
    return ?                                 # section 5: one angular step as an arc on the wall, mm
def footprint_mm(r, w0=0.010, div=3.0e-3):
    return ?                                 # section 5: spot diameter, mm
def cell_m(B):
    return ?                                 # section 6: range cell, m
def v_res(fc, chirps, Tc):
    return ?                                 # section 6: velocity cell, m/s
def ptp(t1, t2, t3, t4):
    return ?, ?                              # section 9: (offset, mean path delay), s

print("blur %.2f px, rolling skew %.2f px" % (blur_px(V, T_EXP, Z), blur_px(V, ROWS * T_ROW, Z)))
for b in (0.12, 0.24):
    print("sigma_Z at %.0f m with b = %.2f m: %.1f mm" % (Z, b, sigma_z(Z, b) * 1e3))
print("LiDAR at 20 Hz, 0.4 deg columns: spacing %.1f x %.1f mm, footprint %.1f mm; 120 deg sweep %.1f ms -> %.1f mm"
      % (spacing_mm(Z, 0.4), spacing_mm(Z, 1.0), footprint_mm(Z), 120 / 360 / 20 * 1e3, V * 120 / 360 / 20 * 1e3))
for B in (1e9, 4e9):
    print("radar B = %.0f GHz: cell %.2f cm; with 256 chirps v_res %.3f m/s" % (B / 1e9, cell_m(B) * 100, v_res(77e9, 256, 50e-6)))
late = T_EXP / 2 + ROWS * T_ROW
print("end-of-readout stamp %.0f ms late: %.1f mm, %.2f px at the facade" % (late * 1e3, V * late * 1e3, blur_px(V, late, Z)))
off, delay = ptp(0.0, 90e-6 + 3e-3, 0.010, 0.010 - 3e-3 + 10e-6)
print("PTP, paths 90/10 us: offset %.1f us, mean delay %.1f us, error %.1f us" % (off * 1e6, delay * 1e6, (off - 3e-3) * 1e6))
```

> [!note]- How to draw it · 그리는 법
> - **Two panels, each with one scale and a scale bar**: the plan in metres, the facade patch in millimetres; every length computed, none sketched.
> - **The stereo error lies along the ray**, stretched from depth to ray length, not along the facade.
> - **The radar cell is a wedge**: $c/(2B)$ deep at any range, the angle cell times the range wide — twice as wide at $4\,\mathrm m$ as at $2$, no deeper.
> - **LiDAR spots and rings from the geometry**: spots $w_0+\theta R$, columns $R\Delta\phi$ and rings $R\Delta\varepsilon$ apart; show whether spots overlap and how much wall lies between rings.
> - **Blur and every stamp error are lengths $v\,\Delta t$** on the facade, drawn along the motion with their times written on them, beside S1's $\pm5\,\mathrm{mm}$ circle.

> [!tip]- Solutions
> 1. With $b=0.24$ at $4\,\mathrm m$ the stereo bar is $\pm78.6\,\mathrm{mm}$ in depth; the radar cell is $3.75\,\mathrm{cm}$ deep and $0.67\,\mathrm m$ wide; the sweep crosses $120^\circ$ in $16.7\,\mathrm{ms}$ and smears the facade $16.7\,\mathrm{mm}$, as before — half the time at twice the speed. On the patch a camera pixel covers $6.67\,\mathrm{mm}$, so S1's circle is under two pixels across; the LiDAR's $22\,\mathrm{mm}$ spots sit $27.9\,\mathrm{mm}$ apart along a ring and $69.8\,\mathrm{mm}$ between rings, no longer overlapping; the blur is $2\,\mathrm{mm}$ and the late stamp $13\,\mathrm{mm}$.
> 2. (a) $d=u_1-u_2$ with independent errors gives $\sigma_d^2=2\sigma_u^2$; linearizing $Z=fb/d$, $|dZ/dd|=fb/d^2=Z^2/(fb)$, so $\sigma_Z=\sqrt2\,Z^2\sigma_u/(fb)$. At $4\,\mathrm m$: $157.1\,\mathrm{mm}$ at $b=0.12$, $78.6\,\mathrm{mm}$ at $0.24$; equal to $20\,\mathrm{mm}$ at $\sqrt{0.020\times600\times0.24/0.707}=2.02\,\mathrm m$; near limit $600\times0.24/128=1.125\,\mathrm m$. (b) Blur $600\times1.0\times0.002/4=0.30$ px, $2.0\,\mathrm{mm}$; skew $600\times1.0\times0.012/4=1.80$ px, $12.0\,\mathrm{mm}$. In pixels both depend only on $v/Z$, and $1.0/4=0.5/2$; in millimetres both doubled with the speed. (c) $27.9\times69.8\,\mathrm{mm}$, a $10+3\times4=22\,\mathrm{mm}$ footprint, $1/(0.0279\times0.0698)=513$ points/m²; $120^\circ$ at $20\,\mathrm{Hz}$ takes $16.7\,\mathrm{ms}$, $16.7\,\mathrm{mm}$ at $1.0\,\mathrm{m/s}$. (d) $c/(2B)=3.75\,\mathrm{cm}$; $S=80\,\mathrm{MHz/\mu s}$; $f_b=2SR/c=2.135\,\mathrm{MHz}$; reach $5\,\mathrm{MHz}\times c/(2S)=9.37\,\mathrm m$ — four times the sweep in the same time quartered the reach; $v_{\text{res}}=\lambda/(2\times256\times50\,\mathrm{\mu s})=0.152\,\mathrm{m/s}$. (e) $4.0-2\times1.499=1.002\,\mathrm m$ at $100\,\mathrm{MHz}$, $4.0-2\times1.874=0.253\,\mathrm m$ at $80$; they agree only at $4.000\,\mathrm m$ within $7.495\,\mathrm m$. (f) $1+12=13\,\mathrm{ms}$ late: $13\,\mathrm{mm}$, $600\times0.013/4=1.95$ px; the PTP offset is off by $(90-10)/2=40\,\mathrm{\mu s}$.
> 3. Blanks: `F * v * t_s / z`, `z**2 * sigma_d / (F * b)`, `r * np.radians(step_deg) * 1e3`, `(w0 + div * r) * 1e3`, `C / (2 * B)`, `C / fc / (2 * chirps * Tc)`, and `((t2 - t1) - (t4 - t3)) / 2, ((t2 - t1) + (t4 - t3)) / 2`. The filled listing prints:
>
>    ```text
>    blur 0.30 px, rolling skew 1.80 px
>    sigma_Z at 4 m with b = 0.12 m: 157.1 mm
>    sigma_Z at 4 m with b = 0.24 m: 78.6 mm
>    LiDAR at 20 Hz, 0.4 deg columns: spacing 27.9 x 69.8 mm, footprint 22.0 mm; 120 deg sweep 16.7 ms -> 16.7 mm
>    radar B = 1 GHz: cell 14.99 cm; with 256 chirps v_res 0.152 m/s
>    radar B = 4 GHz: cell 3.75 cm; with 256 chirps v_res 0.152 m/s
>    end-of-readout stamp 13 ms late: 13.0 mm, 1.95 px at the facade
>    PTP, paths 90/10 us: offset 3040.0 us, mean delay 50.0 us, error 40.0 us
>    ```
>
>    Worse: the late stamp ($8.5\to13.0\,\mathrm{mm}$), the LiDAR's spacing and spots ($7.0\times34.9\to27.9\times69.8\,\mathrm{mm}$, $16\to22\,\mathrm{mm}$), and stereo at the new range despite the doubled baseline ($39.3\to78.6\,\mathrm{mm}$). Better: the radar's range and velocity cells ($15.0\to3.75\,\mathrm{cm}$, $0.304\to0.152\,\mathrm{m/s}$), paid for in reach ($37.5\to9.37\,\mathrm m$). Unchanged in pixels: blur ($0.30$ px) and skew ($1.80$ px), because $v/Z$ is unchanged; in millimetres both doubled.

### Sources

- NIST, speed of light — [physics.nist.gov](https://physics.nist.gov/cgi-bin/cuu/Value?c) — $c$, exact by definition
- OpenStax, *College Physics 2e* §26.4 — [openstax.org](https://openstax.org/books/college-physics-2e/pages/26-4-microscopes) — the f-number sets the light per unit area on the image
- Hamamatsu Learning Center, CCD signal-to-noise ratio — [hamamatsu.magnet.fsu.edu](https://hamamatsu.magnet.fsu.edu/articles/ccdsnr.html) — the noise sources, the SNR form, full well over read noise, dark current halving per $5$–$9\,^\circ\mathrm C$
- Andor, sensitivity and noise of CCD, EMCCD and sCMOS sensors — [andor.oxinst.com](https://andor.oxinst.com/learning/view/article/sensitivity-and-noise-of-ccd-emccd-and-scmos-sensors) — the same sources for CMOS sensors
- Basler docs: shutter types, HDR, triggering, exposure start delay, PTP — [docs.baslerweb.com](https://docs.baslerweb.com/electronic-shutter-types) — row time and flash window, merged exposures, triggers and their fixed delay, PTP
- Keselman et al., "Intel RealSense Stereoscopic Depth Cameras," CCD 2017 (CVPR workshop) — [arXiv:1705.05548](https://arxiv.org/abs/1705.05548) — the $Z^2$ depth-error law, the projector's pattern, darkness and daylight
- Microsoft Learn, Azure Kinect DK depth camera — [learn.microsoft.com](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/depth-camera) — amplitude-modulated time of flight, invalidated pixels, multipath in corners
- Baek et al., "Centimeter-Wave Free-Space Time-of-Flight Imaging," preprint 2021 — [arXiv:2105.11606](https://arxiv.org/abs/2105.11606) — the phase–range relation
- Zollhöfer, "Commodity RGB-D Sensors: Data Acquisition," book chapter 2019 — [arXiv:1902.06835](https://arxiv.org/abs/1902.06835) — flying pixels, sunlight, the projector as an inverse camera, interference
- Geng, "Structured-light 3D surface imaging: a tutorial," *Adv. Opt. Photon.* 3(2), 2011 — [doi:10.1364/AOP.3.000128](https://doi.org/10.1364/AOP.3.000128) — the structured-light family
- NOAA, "What is lidar?" — [oceanservice.noaa.gov](https://oceanservice.noaa.gov/facts/lidar.html) — ranging with a pulsed laser
- Li and Ibanez-Guzman, "Lidar for Autonomous Driving," *IEEE Signal Processing Magazine* 37(4), 2020 — [doi:10.1109/MSP.2020.2973615](https://doi.org/10.1109/MSP.2020.2973615) — wavelengths; MEMS, phased-array and flash designs
- Dreissig et al., "Survey on LiDAR Perception in Adverse Weather Conditions," IEEE IV 2023 — [arXiv:2304.06312](https://arxiv.org/abs/2304.06312) — wavelengths; early and lost returns in rain and fog
- Phillips, Guenther and McAree, "When the Dust Settles," *J. Field Robotics* 34(5), 2017 — [doi:10.1002/rob.21701](https://doi.org/10.1002/rob.21701) — dust ranged at its leading edge; the $71$–$74\%$, $2\%$ and $6\%$ transmittances
- Henley et al., "Detection and mapping of specular surfaces using multibounce lidar returns," *Optics Express* 31(4), 2023 — [doi:10.1364/OE.479900](https://doi.org/10.1364/OE.479900) — specular surfaces invisible to single-scatter returns
- USGS, Lidar Base Specification glossary — [usgs.gov](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-glossary) — discrete, first and last returns
- Ouster, sensor data and OS overview — [static.ouster.dev](https://static.ouster.dev/sensor-docs/image_route1/image_route2/sensor_data/sensor-data.html), [ouster.com](https://ouster.com/os-overview) — per-column timestamps, calibrated reflectivity, dual returns; channel and column counts
- ROS 2 `sensor_msgs` Image and PointCloud2 (jazzy) — [github.com/ros2/common_interfaces](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/PointCloud2.msg) — one header stamp per message
- Texas Instruments, AWR1843 — [ti.com](https://www.ti.com/product/AWR1843) — a single-chip $76$–$81\,\mathrm{GHz}$ radar with $3$ transmitters, $4$ receivers and $4\,\mathrm{GHz}$
- Harlow et al., "A New Wave in Robotics: Survey on Recent mmWave Radar Applications in Robotics," *IEEE T-RO* 40, 2024 — [arXiv:2305.01135](https://arxiv.org/abs/2305.01135) — the FMCW resolution formulas; fog, dust and smoke; ghosts; where radar is used
- Bertoldo et al., "On the Use of a 77 GHz Automotive Radar as a Microwave Rain Gauge," *ETASR* 8(1), 2018 — [etasr.com](https://etasr.com/index.php/ETASR/article/view/1755) — rain is not transparent at $77\,\mathrm{GHz}$
- Ruff, "Evaluation of a radar-based proximity warning system for off-highway dump trucks," *Accident Analysis & Prevention* 38(1), 2006 — [doi:10.1016/j.aap.2005.07.006](https://doi.org/10.1016/j.aap.2005.07.006) — detections and false alarms around a haul truck
- MathWorks, Lidar and Camera Calibration — [mathworks.com](https://www.mathworks.com/help/lidar/ug/lidar-and-camera-calibration.html) — the checkerboard workflow
- KITTI sensor setup — [cvlibs.net](https://www.cvlibs.net/datasets/kitti/setup.php) — cameras triggered by the laser scanner
- Nokia, IEEE 1588 offset and delay — [documentation.nokia.com](https://documentation.nokia.com/html/0_add-h-f/93-0267-HTML/7X50_Advanced_Configuration_Guide/ACG-%20IEEE-1588-FP-TD.html) — the four-stamp equations and the asymmetry error
- Lee and Eidson, 2004 Conference on IEEE 1588, NIST — [nist.gov](https://www.nist.gov/publications/standard-precision-clock-synchronization-protocol-networked-measurement-and-control) — sub-microsecond synchronization demonstrated
- chrony FAQ — [chrony-project.org](https://chrony-project.org/faq.html) — asymmetric delay limits a measured offset

## 한국어

*[[04-robotics/geometric-perception-calibration|3.5]]는 픽셀을 광선·깊이·프레임으로 바꾸고, [[04-robotics/sensor-models|3.2]]는 모든 센서를 $z=h(x)+b+n$으로 적는다. 두 페이지 모두 측정값을 주어진 것으로 받는다. 이 페이지는 센서의 뚜껑을 연다. 우물에 쌓이는 광자, 펄스의 비행시간, 처프의 비트, 시계의 눈금이 어떻게 측정값이 되는지, 그리고 그 물리가 어디서 측정을 망가뜨리는지를 본다. 장치 **P2**, **P5**, **P6**을 다시 쓴다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택에서 첫 층, 물체·장면 이해 바로 아래의 인식이고, "*저 패널을 프레임에 설치해*"에서 패널과 프레임을 식별하는 단계와 접촉을 보는 단계 밑의 감지가 여기서 나온다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 이것 없이는 리그가 내놓는 숫자를 그냥 믿게 되고, 움직이는 베이스 위에서는 어떤 알고리즘이 돌기도 전에 그 숫자가 틀린다 — $0.5\,\mathrm{m/s}$에서 판독 끝에 스탬프를 찍은 카메라는 패널을 $8.5\,\mathrm{mm}$, LiDAR 클라우드의 스탬프 하나는 $23\,\mathrm{mm}$ 어긋나게 놓아 둘 다 S1의 $\pm5\,\mathrm{mm}$를 넘고, 귀환을 하나만 기록하는 LiDAR에게 톱이 일으킨 먼지는 벽이다. 같은 물리가 [[05-construction-robotics/site-perception|5. 현장 인식 §1]](스캔의 간격과 점 오차), [[04-robotics/capstone-panel-contact|26. 캡스톤 §5]](낡음 거리가 된 지연), [[04-robotics/ros2/from-simulation-to-hardware|25.11 §4–§5]](데이터에 스탬프를 찍는 드라이버와 시계), 그리고 학습된 정책이 구멍을 카메라의 $0.5\,\mathrm{mm}$로만 보는 [[05-construction-robotics/imitating-contact|10. 접촉 모방 §1]]에서 다시 나오고, 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서는 2블록, 로보틱스 공통 트랙에 속한다. 이 페이지를 마치면 움직이는 현장 리그의 어떤 센서든 패널에서의 밀리미터 오차로 바꾸고, 센서마다 제 물리가 허락하는 일을 맡길 수 있다.

> [!note] 처음이라면 · First pass
> 두 번 앉아서 끝낸다. **첫째 — 카메라와 시간.** 이 페이지의 대상을 읽고, 그림에서 파사드 위 오차의 크기를 하나씩 찾는다 — $39\,\mathrm{mm}$ 스테레오 막대, $16\,\mathrm{mm}$ LiDAR 점, $5\,\mathrm{mm}$ 블러, $23\,\mathrm{mm}$ 스탬프 오차. 어디서 왔는지는 아직 몰라도 된다. 그다음 §1–§3과 §9를 읽고 계산 절의 1, 2, 5단계를 손으로 따라간다. $1\,\mathrm{m/s}$에서의 노출 창을 묻는 스스로 점검 1로 마무리한다. **둘째 — LiDAR와 장부.** §5를 읽고, 어느 거리부터 LiDAR가 스테레오를 이기는지, 왜 그 답이 제곱근인지 말한다. 3단계와 장부를 따라간 뒤 §10을 돌리고 그 아래 다섯 항목을 읽는다. §4(깊이 카메라), §6(레이더), §7(현장에 들고 갈 표), §8(외부 파라미터)은 두 번째로 읽을 때, 또는 논문이나 현장이 그 센서를 쓸 때 연다. 과제가 그 두 번째 읽기를 마무리한다.

### 이 페이지의 대상 · Running object

**리그.** 3.5의 손목 리그를 도구에 단 **P2**를 건설 트랙의 파사드 패널 과제 S1의 모바일 베이스 위에 올린다([[05-construction-robotics/site-engineering|2.5 현장 로보틱스]]. 앞으로 가리키는 링크일 뿐 선수 지식은 아니다). 베이스의 마스트에 회전식 LiDAR와 FMCW 레이더를 더 달고, 카메라가 파사드를 보게 한 채 파사드에서 $2.0\,\mathrm m$ 떨어져 $0.5\,\mathrm{m/s}$로 파사드를 따라 달린다. P2는 지나가는 내내 멈춰 있으므로 카메라와 마스트의 센서는 하나의 고정된 기하를 유지한다(§8). 랜드마크 $L$은 그 파사드 위의 한 점이다. 다른 페이지에서 그대로 가져오는 것:

| 대상 | 값 | 출처 |
|---|---|---|
| 리그의 카메라 1과 2 | $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, $640\times480$, $k_1=-0.20$, $k_2=+0.05$. 카메라 2는 카메라 1의 $x$ 방향으로 $b=0.12\,\mathrm m$ | 3.5 |
| $L$; $A,B,C$; $d_{ct}$ | $(0.5,\ 0.2,\ 2.0)\,\mathrm m$; $(0,0,2)$, $(0.5,0,2)$, $(0,0.4,2)\,\mathrm m$; $0.04\,\mathrm m$ | 3.5 |
| P6의 카메라 | $Z_c=1.0\,\mathrm m$에서 $f_x=600$ px, $\sigma_u=0.5$ px($0.833\,\mathrm{mm}$), $50\,\mathrm{Hz}$. 노출 중간에서 힘까지의 예산 $70\,\mathrm{ms}$ | 3.2; **P6** |
| P5의 거리 센서 | $\sigma_r=10\,\mathrm{mm}$, 오프셋 $b_r=4\,\mathrm{mm}$. P5의 판독값 $12\,\mathrm{cm}$ | 3.2; **P5** |

나머지는 이 페이지가 스스로 고정한 값이다. **계산이 깔끔하도록 고른 교과 숫자이며, 어떤 제품의 데이터시트도 아니다.**

| 대상 | 값 |
|---|---|
| 각 카메라의 픽셀 | 피치 $6.0\,\mathrm{\mu m}$(그래서 렌즈는 $f=3.6\,\mathrm{mm}$), $f/2.0$(조리개 $1.8\,\mathrm{mm}$). 풀 웰 $10{,}000\ e^-$, 읽기 잡음 $5\ e^-$, 암전류 $100\ e^-/\mathrm s$. 한 단계가 $10\ e^-$인 $10$비트 변환기 |
| $f/2$에서의 장면 | 픽셀당 ms당 광전자: 그늘진 파사드 $200$, 햇빛 받는 파사드 $2{,}000$, 글린트(유리 패널이 비춘 낮은 해) $2\times10^6$ |
| 셔터와 베이스 | 롤링 셔터, 행당 $25\,\mathrm{\mu s}$($480$행을 $12\,\mathrm{ms}$에 읽음), 실내 노출 $10\,\mathrm{ms}$. 베이스 속도 $v=0.5\,\mathrm{m/s}$, 파사드는 카메라 1에서 $Z=2.0\,\mathrm m$ |
| LiDAR | $1.0^\circ$ 간격 채널 $32$개($\pm15.5^\circ$), $0.2^\circ$마다 한 열, $10\,\mathrm{Hz}$. 거리 잡음 $\sigma_L=20\,\mathrm{mm}$, 발산각 $3.0\,\mathrm{mrad}$, 출사 빔 $10\,\mathrm{mm}$. 카메라 1 위 $0.30\,\mathrm m$, 축은 앞–왼쪽–위. 훑기는 뒤를 보며 시작해 왼쪽으로 돈다. 클라우드마다 시작 시각에 스탬프 하나 |
| 레이더 | $77\,\mathrm{GHz}$ FMCW, $T_c=50\,\mathrm{\mu s}$ 동안 대역폭 $B=1.0\,\mathrm{GHz}$, 프레임당 처프 $128$개, IF 대역 $5\,\mathrm{MHz}$, $\lambda/2$ 간격 가상 채널 $3\times4=12$개. LiDAR 아래 |
| ToF 카메라; 작업자 | 변조 $100$과 $80\,\mathrm{MHz}$, 위상 잡음 $0.02\,\mathrm{rad}$. [[04-robotics/hri-safety\|11. HRI와 안전]]이 ISO 13855에서 가져온 보행 속도 $1.6\,\mathrm{m/s}$로 걷는 작업자 |

뒤의 모든 숫자는 이 두 표에서 나온다. 일관성 확인 하나: LiDAR는 제 프레임에서 $L$을 $(2.0,\ -0.5,\ -0.5)\,\mathrm m$, $2.121\,\mathrm m$ 거리에서 보고, 장착 변환과 3.5의 $K$를 거치면 카메라 1이 보는 바로 그 픽셀 $(470,\ 300)$에 떨어진다(§8).

*범위: 이 페이지는 카메라, 스테레오 쌍, 깊이 카메라, LiDAR, 레이더가 측정값을 만드는 방식, 정해진 거리와 속도에서의 지배적 오차, 이것들로 된 리그를 한 기기처럼 보정하고 타임스탬프를 맞추는 법, 현장에 맞게 고르는 법을 가르친다. 그 출력을 3D로 바꾸는 기하([[04-robotics/geometric-perception-calibration|3.5]]), 그것을 받아 쓰는 잡음 모델과 필터([[04-robotics/sensor-models|3.2]], [[04-robotics/state-estimation-slam|3]]), 현장 포인트 클라우드([[05-construction-robotics/site-perception|5. 현장 인식]]), 센서 드라이버([[04-robotics/ros2/from-simulation-to-hardware|25.11 §4]])는 가르치지 않는다. 나머지는 §11에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 420" style="max-width:100%;height:auto" role="img" aria-label="왼쪽은 1 m = 100 px의 평면도: 2 m 앞 파사드를 따라 0.5 m/s로 움직이는 모바일 베이스, 0.12 m 떨어진 카메라 1과 카메라 2와 카메라 1 위의 LiDAR, 카메라 시야, 광선을 따라 ±39 mm인 스테레오 깊이 오차가 붙은 파사드 위 랜드마크 L, L 주변의 15 cm × 9.5° 레이더 셀, 파사드 앞 0.30 m에서 1.6 m/s로 리그 쪽으로 걷는 작업자, 파사드를 120° 가로지르는 LiDAR의 훑기. 오른쪽은 1 mm = 2 px로 본 L 주변 파사드의 정면: 3.3 mm 카메라 픽셀, 약 38 mm 간격의 링 위에 약 7.4 mm 간격으로 찍힌 16 mm LiDAR 점, S1의 5 mm 허용오차 원, 10 ms에서 5 mm와 2 ms에서 1 mm의 모션 블러, 8.5 mm와 23 mm의 타임스탬프 오차.">
  <text x="16" y="20" font-size="12" fill="currentColor" font-weight="600">평면도: 파사드를 지나가는 베이스</text>
  <text x="302" y="20" font-size="12" fill="currentColor" font-weight="600">L 주변의 파사드, 정면</text>
  <line x1="16" y1="72.0" x2="284" y2="72.0" stroke="currentColor" stroke-width="2.2"/>
  <line x1="20" y1="72.0" x2="28" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="32" y1="72.0" x2="40" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="44" y1="72.0" x2="52" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="56" y1="72.0" x2="64" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="68" y1="72.0" x2="76" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="80" y1="72.0" x2="88" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="92" y1="72.0" x2="100" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="104" y1="72.0" x2="112" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="116" y1="72.0" x2="124" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="128" y1="72.0" x2="136" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="140" y1="72.0" x2="148" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="152" y1="72.0" x2="160" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="164" y1="72.0" x2="172" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="176" y1="72.0" x2="184" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="188" y1="72.0" x2="196" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="200" y1="72.0" x2="208" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="212" y1="72.0" x2="220" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="224" y1="72.0" x2="232" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="236" y1="72.0" x2="244" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="248" y1="72.0" x2="256" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="260" y1="72.0" x2="268" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <line x1="272" y1="72.0" x2="280" y2="64.0" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <text x="18" y="60.0" font-size="11" fill="currentColor">파사드 (S1의 패널)</text>
  <line x1="130.0" y1="272.0" x2="23.3" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="4 3"/>
  <line x1="130.0" y1="272.0" x2="236.7" y2="72.0" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.4" stroke-dasharray="4 3"/>
  <line x1="130.0" y1="272.0" x2="180.0" y2="72.0" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.8"/>
  <path d="M162.0 75.9 L164.4 61.1 A213.7 213.7 0 0 1 198.9 69.8 L194.1 84.0 A198.7 198.7 0 0 0 162.0 75.9 Z" fill="currentColor" fill-opacity="0.16" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.7"/>
  <line x1="196.5" y1="76.9" x2="204.0" y2="96.0" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.7"/>
  <text x="206" y="100" font-size="11" fill="currentColor">레이더 셀</text>
  <text x="206" y="113" font-size="11" fill="currentColor">15 cm × 9.5°,</text>
  <text x="206" y="126" font-size="11" fill="currentColor" fill-opacity="0.85">여기서 폭 0.33 m</text>
  <line x1="179.0" y1="75.9" x2="181.0" y2="68.1" stroke="currentColor" stroke-width="3.6"/>
  <circle cx="180.0" cy="72.0" r="3.0" fill="currentColor" stroke="none"/>
  <text x="165.0" y="87.0" font-size="12" fill="currentColor" font-weight="600">L</text>
  <line x1="181.0" y1="78.0" x2="204.0" y2="150.0" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.7"/>
  <text x="206" y="160" font-size="11" fill="currentColor">스테레오 ±39 mm</text>
  <text x="206" y="173" font-size="11" fill="currentColor" fill-opacity="0.85">광선 방향으로</text>
  <circle cx="50.0" cy="102.0" r="15" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1.2"/>
  <line x1="57.2" y1="117.4" x2="67.9" y2="140.0" stroke="currentColor" stroke-width="1.4"/>
  <path d="M70.4 145.4 L65.4 141.2 L70.3 138.9 Z" fill="currentColor" stroke="none"/>
  <text x="18.0" y="166.0" font-size="11" fill="currentColor">파사드 앞 0.30 m의</text>
  <text x="18.0" y="179.0" font-size="11" fill="currentColor">작업자, 1.6 m/s</text>
  <path d="M169.8 249.0 L168.6 246.9 L167.2 245.0 L165.7 243.1 L164.2 241.2 L162.5 239.5 L160.8 237.8 L158.9 236.3 L157.0 234.8 L155.1 233.4 L153.0 232.2 L150.9 231.0 L148.7 230.0 L146.5 229.1 L144.2 228.3 L141.9 227.6 L139.6 227.0 L137.2 226.6 L134.8 226.3 L132.4 226.1 L130.0 226.0 L127.6 226.1 L125.2 226.3 L122.8 226.6 L120.4 227.0 L118.1 227.6 L115.8 228.3 L113.5 229.1 L111.3 230.0 L109.1 231.0 L107.0 232.2 L104.9 233.4 L103.0 234.8 L101.1 236.3 L99.2 237.8 L97.5 239.5 L95.8 241.2 L94.3 243.1 L92.8 245.0 L91.4 246.9 L90.2 249.0" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8"/>
  <path d="M90.2 249.0 L90.8 242.5 L95.5 245.2 Z" fill="currentColor" stroke="none"/>
  <text x="16" y="214" font-size="11" fill="currentColor">LiDAR 120° 훑기: 33 ms, 17 mm</text>
  <path d="M125.0 279.0 L130.0 270.0 L135.0 279.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <text x="121.0" y="292.0" font-size="10" fill="currentColor" text-anchor="middle">C1</text>
  <path d="M137.0 279.0 L142.0 270.0 L147.0 279.0 Z" stroke="currentColor" stroke-width="1.2" fill="currentColor" fill-opacity="0.25"/>
  <text x="151.0" y="292.0" font-size="10" fill="currentColor" text-anchor="middle">C2</text>
  <circle cx="130.0" cy="274.0" r="9" fill="none" stroke="currentColor" stroke-width="1.0" stroke-dasharray="3 2"/>
  <text x="160" y="268" font-size="11" fill="currentColor">LiDAR, C1 위 0.30 m</text>
  <rect x="95" y="298" width="70" height="28" fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2"/>
  <text x="130" y="316" font-size="11" fill="currentColor" text-anchor="middle">베이스</text>
  <line x1="172" y1="312" x2="214" y2="312" stroke="currentColor" stroke-width="1.6"/>
  <path d="M220.0 312.0 L214.0 314.7 L214.0 309.3 Z" fill="currentColor" stroke="none"/>
  <text x="226" y="309" font-size="11" fill="currentColor">v = 0.5 m/s</text>
  <text x="226" y="322" font-size="11" fill="currentColor" fill-opacity="0.85">10 ms = 5 mm</text>
  <line x1="20" y1="356" x2="120" y2="356" stroke="currentColor" stroke-width="1.6"/>
  <line x1="20" y1="352" x2="20" y2="360" stroke="currentColor" stroke-width="1.0"/>
  <line x1="120" y1="352" x2="120" y2="360" stroke="currentColor" stroke-width="1.0"/>
  <text x="70" y="349" font-size="10" fill="currentColor" text-anchor="middle">1 m</text>
  <rect x="302.0" y="30.0" width="250.0" height="226.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <circle cx="528.8" cy="223.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="222.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="221.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="220.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="219.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="218.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="217.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="216.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="215.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="214.3" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="213.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="212.5" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="211.7" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="210.8" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="210.0" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="146.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="145.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="144.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="143.3" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="142.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="141.5" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="140.6" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="139.7" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="138.9" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="138.0" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="137.2" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="136.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="135.6" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="134.8" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="134.0" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="69.8" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="513.8" cy="68.9" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="498.8" cy="68.1" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="483.8" cy="67.2" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="468.9" cy="66.4" r="16.4" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="454.0" cy="65.5" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="439.2" cy="64.7" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="424.3" cy="63.9" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="409.5" cy="63.1" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="394.7" cy="62.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="379.9" cy="61.6" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="365.2" cy="60.8" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="350.5" cy="60.1" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="335.8" cy="59.4" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="321.1" cy="58.7" r="16.3" fill="none" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.45"/>
  <circle cx="528.8" cy="223.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="222.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="221.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="220.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="219.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="218.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="217.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="216.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="215.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="214.3" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="213.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="212.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="211.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="210.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="210.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="528.8" cy="146.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="145.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="144.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="143.3" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="142.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="141.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="140.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="139.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="138.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="138.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="137.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="136.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="135.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="134.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="134.0" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="528.8" cy="69.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="513.8" cy="68.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="498.8" cy="68.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="483.8" cy="67.2" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="468.9" cy="66.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="454.0" cy="65.5" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="439.2" cy="64.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="424.3" cy="63.9" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="409.5" cy="63.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="394.7" cy="62.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="379.9" cy="61.6" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="365.2" cy="60.8" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="350.5" cy="60.1" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="335.8" cy="59.4" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <circle cx="321.1" cy="58.7" r="1.2" fill="currentColor" fill-opacity="0.7" stroke="none"/>
  <line x1="403.7" y1="126.7" x2="403.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="126.7" x2="450.3" y2="126.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="410.3" y1="126.7" x2="410.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="133.3" x2="450.3" y2="133.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="417.0" y1="126.7" x2="417.0" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="140.0" x2="450.3" y2="140.0" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="423.7" y1="126.7" x2="423.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="146.7" x2="450.3" y2="146.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="430.3" y1="126.7" x2="430.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="153.3" x2="450.3" y2="153.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="437.0" y1="126.7" x2="437.0" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="160.0" x2="450.3" y2="160.0" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="443.7" y1="126.7" x2="443.7" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="166.7" x2="450.3" y2="166.7" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="450.3" y1="126.7" x2="450.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <line x1="403.7" y1="173.3" x2="450.3" y2="173.3" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.65"/>
  <circle cx="427.0" cy="150.0" r="10.0" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2"/>
  <line x1="427.0" y1="150.0" x2="417.0" y2="150.0" stroke="currentColor" stroke-width="4.0" stroke-opacity="0.45" stroke-linecap="round"/>
  <line x1="427.0" y1="150.0" x2="425.0" y2="150.0" stroke="currentColor" stroke-width="4.0" stroke-linecap="round"/>
  <circle cx="427.0" cy="150.0" r="2.4" fill="currentColor" stroke="none"/>
  <text x="439.0" y="138.0" font-size="11" fill="currentColor" font-weight="600">L</text>
  <line x1="522.0" y1="246.0" x2="542.0" y2="246.0" stroke="currentColor" stroke-width="1.6"/>
  <line x1="522.0" y1="242.0" x2="522.0" y2="250.0" stroke="currentColor" stroke-width="1.0"/>
  <line x1="542.0" y1="242.0" x2="542.0" y2="250.0" stroke="currentColor" stroke-width="1.0"/>
  <text x="532.0" y="240.0" font-size="10" fill="currentColor" text-anchor="middle">10 mm</text>
  <text x="302" y="272.0" font-size="10.5" fill="currentColor">격자: 카메라 픽셀, 3.3 mm</text>
  <text x="302" y="286.0" font-size="10.5" fill="currentColor">점선 원: S1의 ±5 mm</text>
  <text x="302" y="300.0" font-size="10.5" fill="currentColor">원: LiDAR 점, 폭 16 mm</text>
  <text x="302" y="314.0" font-size="10.5" fill="currentColor">막대: 블러, 5 mm(10 ms), 1 mm(2 ms)</text>
  <line x1="304" y1="324.0" x2="316.0" y2="324.0" stroke="currentColor" stroke-width="1.5"/>
  <path d="M321.0 324.0 L315.0 326.7 L315.0 321.3 Z" fill="currentColor" stroke="none"/>
  <text x="358.2" y="328.0" font-size="10.5" fill="currentColor">늦은 스탬프, 17 ms: 8.5 mm</text>
  <line x1="304" y1="338.0" x2="345.2" y2="338.0" stroke="currentColor" stroke-width="1.5"/>
  <path d="M350.2 338.0 L344.2 340.7 L344.2 335.3 Z" fill="currentColor" stroke="none"/>
  <text x="358.2" y="342.0" font-size="10.5" fill="currentColor">클라우드 스탬프, 46 ms: 23 mm</text>
  <text x="16" y="394" font-size="11" fill="currentColor" fill-opacity="0.9">모든 오차를 2 m 앞 파사드에 그렸다. 블러, 늦은 스탬프, 훑기는 0.5 m/s에서 모두 v·Δt다.</text>
  <text x="16" y="410" font-size="11" fill="currentColor" fill-opacity="0.9">S1의 ±5 mm와 같은 크기인 것은 짧은 노출과 참 스탬프를 갖춘 카메라 픽셀뿐이다.</text>
</svg>

파사드를 지나가는 리그다. 모든 오차를 떨어지는 자리에 축척대로 그렸다. 왼쪽 평면도: $L$에서의 스테레오 깊이 오차(광선 방향 $\pm39\,\mathrm{mm}$), 레이더의 $15\,\mathrm{cm}\times9.5^\circ$ 셀(그 자리에서 폭 $0.33\,\mathrm m$), 파사드 앞 $0.30\,\mathrm m$의 작업자, 파사드를 가로지르는 LiDAR의 $120^\circ$ 훑기($33\,\mathrm{ms}$ 동안 베이스가 $17\,\mathrm{mm}$ 이동). 오른쪽은 $1\,\mathrm{mm}=2$ px로 본 $L$ 주변의 파사드: S1의 $\pm5\,\mathrm{mm}$ 안에 든 $3.3\,\mathrm{mm}$ 카메라 픽셀, 링을 따라 겹치고 링 사이에 $\sim22\,\mathrm{mm}$ 틈을 남기는 $16\,\mathrm{mm}$ LiDAR 점, $10\,\mathrm{ms}$ 노출의 $5\,\mathrm{mm}$ 블러, 그리고 $8.5$와 $23\,\mathrm{mm}$짜리 잘못된 타임스탬프 둘.

### 1. 영상 형성: 빛, 노출, 잡음

*한 문장으로:* 픽셀은 노출되는 동안 도착한 광전자를 센다. 그 개수의 무작위성이 어떤 알고리즘도 없애지 못하는 잡음 바닥을 만들고, 유한한 우물이 한 번의 노출이 담을 수 있는 가장 밝은 부분을 정한다.

**문제.** 해가 낮은 현장에서 리그의 카메라는 잡음 낀 그늘 패널이나, 유리 패널이 번쩍이는 자리의 하얀 공백 중 하나만 보여 주고 둘을 함께 보여 주지 않는다. 뻔한 처방 — 노출을 늘리거나 게인을 올리기 — 은 다른 것을 망친다. 이유를 보려면 빛을 따라 픽셀 하나로 들어가 보면 된다. 쉬운 말로 하면, 픽셀은 셔터가 열린 동안 광전자를 세는 양동이다. 개수는 무작위이고, 양동이에는 테두리가 있다. 이 절이 유도하는 것은 전부 이 세 사실에 숫자를 붙인 것이다.

**우물로 들어가는 빛.** 초점 거리 $f$, 조리개 지름 $D$인 렌즈의 **F수**(f-number) $N=f/D$는 상면의 단위 면적에 닿는 빛의 양을 정한다([OpenStax §26.4](https://openstax.org/books/college-physics-2e/pages/26-4-microscopes)). 렌즈를 깔때기로 생각하자. 입구가 넓을수록 벽의 한 조각이 보내는 빛을 더 많이 받고, 초점 거리가 길수록 같은 빛을 더 큰 상에 펼친다. 거리 $Z$의 벽 조각이 보내는 빛은 $D^2/Z^2$에 비례하는 입체각의 입구로 들어오고, 그 상의 면적은 조각의 $(f/Z)^2$배다. 그래서

$$E_{\text{image}}\ \propto\ \frac{D^2/Z^2}{f^2/Z^2}=\frac{1}{N^2}$$

거리가 약분되므로 벽의 상은 $10\,\mathrm m$에서도 $2\,\mathrm m$에서처럼 밝다(작아질 뿐 어두워지지 않는다). $N$이 $\sqrt2$배가 될 때마다 밝기는 절반이 된다. 리그의 렌즈는 $f/2$에서 $f=3.6\,\mathrm{mm}$, 조리개 $1.8\,\mathrm{mm}$다. 픽셀이 모으는 광전자는 장면의 비율에 노출 시간을 곱한 $S=\Phi\,t_{\exp}$다. ms당 $200$개인 그늘진 파사드는 $2\,\mathrm{ms}$에 $400\ e^-$를 준다.

**잡음의 네 원천.** 셈이 왜 흔들리는가? 광자는 양동이에 떨어지는 빗방울처럼 서로 독립적으로 도착해서, 같은 소나기라도 초마다 개수가 조금씩 다르다. 그 개수는 푸아송 분포이고 분산이 평균과 같으므로 **샷 잡음**(shot noise)은 $\sqrt S$다. $400$에 $20\ e^-$, $5\%$다. 열이 풀어놓는 **암전류**(dark current) 전자도 푸아송이라 $D_c t_{\exp}$개만큼 분산을 더한다. 증폭기는 고정된 **읽기 잡음**(read noise) $\sigma_{\text{read}}$를 더하고, 변환기의 계단은 **양자화 잡음** $10/\sqrt{12}=2.89\ e^-$를 더한다([[02-foundations/signal-processing|6. 신호처리 §2]]. 그것이 언제 잡음이고 언제 편향인지는 [[04-robotics/sensor-models|3.2 §4]]). 카메라 제조사들은 CCD와 CMOS에 같은 원천을 든다([Hamamatsu](https://hamamatsu.magnet.fsu.edu/articles/ccdsnr.html), [Andor](https://andor.oxinst.com/learning/view/article/sensitivity-and-noise-of-ccd-emccd-and-scmos-sensors)). 서로 독립이므로 분산이 더해진다([[02-foundations/probability|3. 확률 §2]]).

> **픽셀 SNR의 정의.** **픽셀 신호 대 잡음비**(pixel SNR)는 *픽셀의 평균 신호를 프레임마다 흔들리는 값의 표준편차로 나눈 비*다. 카메라의 성질이 아니라 측정 하나(픽셀 하나, 노출 하나, 밝기 하나)의 성질이다. 조건 넷. 신호는 **광전자의 개수** $S=\Phi t_{\exp}$다. 도착이 **푸아송**이라 샷 잡음의 분산이 $S$와 같다. 원천들이 **독립**이라 분산이 더해진다. 그리고 픽셀이 **풀 웰 아래**에 있다. 포화된 픽셀은 빛이 얼마든 같은 값을 읽으므로 SNR이 큰 것이 아니라 정의되지 않는다.
>
> $$\mathrm{SNR}=\frac{S}{\sqrt{S+D_c\,t_{\exp}+\sigma_{\text{read}}^2+\sigma_q^2}}$$
>
> $S$는 신호, $D_c$는 암전류, $t_{\exp}$는 노출 시간, $\sigma_{\text{read}}$와 $\sigma_q$는 읽기 잡음과 양자화 잡음이고 모두 전자 단위다. Hamamatsu의 식에 양자화를 더한 꼴이다. $S\gg\sigma_{\text{read}}^2$이면 $\sqrt S$로 가는데, 이것이 샷 잡음 한계다.
>
> - **예**: $2\,\mathrm{ms}$의 그늘진 파사드. $S=400\ e^-$, $\mathrm{SNR}=400/\sqrt{400+0.2+25+8.33}=19.2$로 한계 $\sqrt{400}=20$에 가깝다. $10\,\mathrm{ms}$에서는 $44.3$이다.
> - **비예**: 아날로그 게인을 올리는 것. 이미 모인 전자와 그 잡음을 함께 곱할 뿐 광자를 더하지 않으니, 샷 잡음 한계는 그대로다.
> - **왜 중요한가**: 뒤에 나오는 모든 "픽셀 잡음" — 3.2의 $\sigma_u$, §3의 $\sigma_d$, 매처의 성패 — 가 여기서 시작하고, 노출을 늘리면 SNR이 $\sqrt{t_{\exp}}$로 늘어난다. 그 대가가 §2다.

> **동적 범위의 정의.** **동적 범위**(dynamic range)는 *센서가 한 번의 노출에 기록하는 가장 큰 신호와 가장 작은 신호의 비*이고, 장면의 가장 밝은 곳과 가장 어두운 곳의 비와 견주는 수다. 조건 셋. 위쪽 끝은 픽셀이나 변환기가 **포화**하는 곳이다. 아래쪽 끝은 **어둠 속의 잡음 바닥**, SNR $=1$인 곳이다. 그리고 두 끝이 **같은 노출, 같은 게인**에 속한다.
>
> $$\mathrm{DR}=\frac{S_{\max}}{\sigma_{\text{read}}},\qquad \mathrm{DR}_{\mathrm{dB}}=20\log_{10}\mathrm{DR}$$
>
> $S_{\max}$는 풀 웰, $\sigma_{\text{read}}$는 읽기 잡음이다(Hamamatsu의 정의). 리그는 $10{,}000/5=2{,}000$, $66.0\,\mathrm{dB}$($10.97$스톱)이고, 변환기의 계단을 바닥에 넣으면 $64.8\,\mathrm{dB}$다.
>
> - **예**: 햇빛 대 그늘은 $2{,}000/200=10$, $20\,\mathrm{dB}$다. $2\,\mathrm{ms}$에서 그늘은 SNR $19.2$로, 해는 $4{,}000\ e^-$로 포화 없이 읽힌다.
> - **비예**: 낮은 해의 글린트 대 그늘은 $2\times10^6/200$, $80\,\mathrm{dB}$다. 어떤 노출도 둘을 함께 담지 못한다. 글린트는 $5\,\mathrm{\mu s}$ 만에 우물을 채우는데, 그때 그늘은 $1\ e^-$(SNR $0.17$)밖에 없다.
> - **왜 중요한가**: 해가 낮을 때는 해상도가 아니라 조명의 비가 무엇이 보일지를 정한다. 자동 노출은 한쪽 끝을 고르고, 그것이 맞춘 유리 패널 옆의 그늘진 패널은 그냥 사라진다.

> [!note]- 더 깊이 · Deeper
> **열, 게인, 합친 노출.** Hamamatsu가 설명하는 고성능 CCD에서는 실온 아래로 $5$–$9\,^\circ\mathrm C$ 식힐 때마다 암전류가 대략 절반이 된다. 같은 규칙이 실온 위로 데워지는 리그의 센서에도 맞는다면, 현장 햇볕에 $30\,^\circ\mathrm C$ 더 뜨거워진 하우징은 암신호가 $2^{30/9}=10$배에서 $2^{30/5}=64$배다. $64\times100\ e^-/\mathrm s$, $10\,\mathrm{ms}$이면 $64\ e^-$, 표준편차 $8$로 읽기 잡음보다 크고, 그것도 어두운 영역에서다. 게인은 여유를 더 고운 계단과 바꾼다. $\times4$에서 변환기의 전체 눈금은 $2{,}558\ e^-$, 바닥은 $5.05\ e^-$라 동적 범위가 $1{,}732$ 대신 $506$($54.1\,\mathrm{dB}$)이 된다. 노출을 합치는 센서 모드 — 행을 번갈아, 네 픽셀씩 묶어 따로, 또는 연속 프레임으로 노출을 달리하는 것([Basler, *HDR*](https://docs.baslerweb.com/hdr)) — 는 범위를 넓히지만, 움직이는 베이스에서는 노출들이 서로 다른 순간에 찍히고, 그 값은 §9가 매긴다.

### 2. 모션 블러와 롤링 셔터

*한 문장으로:* 픽셀이 노출되는 동안 움직이는 장면의 상은 $f\,v\,t_{\exp}/Z$ 픽셀만큼 미끄러지고, 롤링 셔터는 행을 하나씩 조금씩 늦게 노출하므로, 움직이는 리그는 같은 영상을 서로 다른 두 시계로 번지게 하고 비튼다.

**문제.** §1은 노출을 늘리면 SNR이 늘어난다고 했다. 움직이는 베이스에서는 운동도 함께 늘어난다. 픽셀이 빛을 모으는 동안 장면이 픽셀 위를 미끄러지고, 리그의 카메라는 행을 차례로 읽으므로 한 프레임의 위와 아래가 서로 다른 순간에 찍힌다. 핵심은 이것이다: 영상은 한 순간이 아니라 *한 구간 동안 물체가 있던 자리*의 기록이고, 아래 규칙들은 그 구간이 픽셀로 얼마인지를 말한다.

**번짐.** 깊이 $Z$에서 상면과 나란히 $v$로 움직이는 점은 $u(t)=f(X_0+vt)/Z+c_x$로 투영되므로(3.5 §1), 그 상은 초당 $fv/Z$ 픽셀씩 움직이고, 픽셀이 적분하는 동안 줄을 긋는다.

> **모션 블러의 정의.** **모션 블러**(motion blur)는 *영상 속의 길이*, 곧 픽셀이 노출되는 동안 점의 상이 이동한 거리다. 조건 넷. 운동은 프레임 주기가 아니라 **노출 동안의 상대 운동**이다. 1차로는 **상면과 나란한** 성분만 번지게 한다. 점의 **깊이**가 들어가므로 병진에서는 가까운 것이 더 번진다. 그리고 각속도 $\omega$의 **회전**은 깊이와 상관없이 중심 근처의 모든 점을 약 $f\omega t_{\exp}$만큼 번지게 한다([[04-robotics/egocentric-perception|22. 1인칭 인식]]의 도는 머리가 이 경우다).
>
> $$b=\frac{f\,v\,t_{\exp}}{Z}$$
>
> 픽셀 단위이고 $f$는 픽셀 단위 초점 거리, $v$는 속도, $t_{\exp}$는 노출 시간, $Z$는 깊이다. 파사드 위에서 그 줄은 그냥 $v\,t_{\exp}$ 길이다.
>
> - **예**: $0.5\,\mathrm{m/s}$, $2\,\mathrm m$의 리그는 $10\,\mathrm{ms}$에서 $1.50$ px($5.0\,\mathrm{mm}$), $2\,\mathrm{ms}$에서 $0.30$ px 번진다. 레일에서 $1.0\,\mathrm m$ 떨어진 P6의 카메라는 $0.5\,\mathrm{m/s}$로 움직이는 카트를 $10\,\mathrm{ms}$에 $3.0$ px 번지게 하는데, 제 $\sigma_u$의 여섯 배다.
> - **비예**: 블러는 잡음이 아니다. 그 속도에서는 매 프레임 똑같은 결정적 번짐이라 프레임을 평균해도 줄지 않는다. 그리고 줄의 중심은 **노출 중간**에 점이 있던 자리다. §9가 영상에 노출 중간의 스탬프를 찍는 이유다.
> - **왜 중요한가**: SNR(§1)이 노출의 아래를 막고 블러가 위를 막는다. 그 사이가 움직이는 로봇이 쓸 수 있는 창이다.

**노출 창.** $0.5\,\mathrm{m/s}$에서 그늘이 SNR $10$을 내려면 $t_{\exp}\ge0.632\,\mathrm{ms}$, 블러를 반 픽셀 이하로 하려면 $t_{\exp}\le0.5Z/(fv)=3.333\,\mathrm{ms}$, 해가 포화하지 않으려면 $5.0\,\mathrm{ms}$까지다. 실내의 $10\,\mathrm{ms}$는 두 번 실패한다. $1.5$ px 블러, 그리고 포화한 햇빛 쪽 절반. $2\,\mathrm{m/s}$에서는 위쪽 한계가 $0.833\,\mathrm{ms}$로 내려오고, 빛이 열 분의 일인 해 질 녘에는 아래쪽 한계가 열 배쯤 올라가 위쪽을 넘는다. 그때는 빛(스트로브), 조리개, 느린 베이스만이 돕는다. 게인은 아니다.

**롤링 셔터.** 글로벌 셔터는 모든 픽셀을 한꺼번에 시작하고 멈춘다. 롤링 셔터는 행을 차례로 노출하고 행마다 행 시간만큼 어긋나며, 프레임 전체를 읽는 데 행 시간 곱하기 행 수가 걸린다([Basler, *Electronic Shutter Types*](https://docs.baslerweb.com/electronic-shutter-types). 예로 든 값에 행당 $14$와 $35\,\mathrm{\mu s}$가 있다).

> **롤링 셔터 스큐의 정의.** **롤링 셔터 스큐**(rolling-shutter skew)는 *한 영상의 행과 행 사이의 어긋남*이다. 행들이 서로 다른 시각에 노출되어 생기며, 블러가 아니라 기하 왜곡이다. 조건 셋. 행이 **일정한 행 지연** $t_{\text{row}}$로 **차례로** 노출된다. **판독 동안 상대 운동**이 있다. 그리고 모든 행의 노출이 **같은 길이**라, 행들은 얼마나 길게가 아니라 언제가 다르다.
>
> $$\Delta u(r)=\frac{f\,v\,r\,t_{\text{row}}}{Z}$$
>
> $r$은 첫 행부터 센 행 번호이고 나머지는 블러와 같다. 그래서 리그가 옆으로 움직이는 동안 수직 모서리가 기울어 보인다.
>
> - **예**: $480$행을 읽는 데 $12\,\mathrm{ms}$. $0.5\,\mathrm{m/s}$, $2\,\mathrm m$에서 마지막 행은 파사드를 $6.0\,\mathrm{mm}$ 더 간 자리에서 보므로 $1.80$ px이고, 수직 패널 모서리는 $0.21^\circ$ 기운다.
> - **비예**: 짧은 노출이 스큐를 없애지는 못한다. $0.5\,\mathrm{ms}$에서 블러는 $0.075$ px인데 스큐는 여전히 $1.80$ px다. 글로벌 셔터, 또는 모든 행이 열려 있을 때만 켜지는 빛(Basler의 플래시 창)만이 없앤다.
> - **왜 중요한가**: 롤링 셔터 프레임에는 자세가 하나가 아니라 $480$개 들어 있고, 영상마다 자세 하나를 주는 방법은 조금 틀린 기하를 본다. [[04-robotics/state-estimation-slam|3. 상태 추정 §8]]이 롤링 셔터를 알고리즘의 이득을 좌우할 수 있는 세부 사항으로 꼽는 이유다.

함께 트리거된 두 롤링 셔터 카메라는 짝이 맞는 행을 같은 순간에 읽으므로, 옆 방향 운동이 한 점의 두 상을 똑같이 밀어 시차가 살아남는다. 따로 트리거되면 그렇지 않다(§9).

### 3. 센서로서의 스테레오 깊이

*한 문장으로:* 스테레오 쌍은 픽셀 잡음을 거리의 제곱으로 커지고 기선으로 줄어드는 깊이 잡음으로 바꾸고, 두 영상에 맞출 만한 뚜렷한 것이 없는 곳에서는 아무것도 재지 못한다.

**문제.** 3.5는 스테레오를 기하로 다룬다. 광선 둘, 점 하나. 로봇에게는 작업 거리에서의 오차 막대를 가진 센서로 필요하다. LiDAR와 견주거나 리그의 크기를 정하려면. 핵심은 이것이다: 깊이는 두 픽셀 위치의 작은 차이에서 나오고, 잡음 낀 두 수의 작은 차이는 잡음이 크다. 점이 멀수록 차이는 작아지고 깊이는 나빠진다.

**$Z=fb/d$에서 오차 막대로.** 3.5 §2가 $Z=fb/d$와 시차 1픽셀의 값 $Z^2/(fb)$를 준다. 시차는 두 위치의 차 $d=u_1-u_2$이고, 두 위치가 각각 독립 오차 $\sigma_u$로 잡히면 분산이 더해진다.

$$\sigma_d=\sqrt{\sigma_u^2+\sigma_u^2}=\sqrt2\,\sigma_u$$

두 오차가 차에 각각 $\pm1$의 가중치로 들어가기 때문이다. 3.2의 $\sigma_u=0.5$ px이면 $0.707$ px다. $Z'(d)=-fb/d^2=-Z^2/(fb)$로 $Z(d)$를 선형화하면 이것이 깊이 오차가 된다.

> **삼각측량 센서의 깊이 정밀도의 정의.** 알려진 기선 위에서 광선 둘을 교차시켜 깊이를 내는 센서 — 카메라 둘, 또는 카메라와 프로젝터(§4) — 가 정해진 거리에서 보고하는 *깊이의 표준편차*다. 조건 넷. 기하가 **보정되고 평행화**되어 3.5의 모델이 선다. 대응이 **옳다**. 잘못된 짝은 더 큰 $\sigma_d$가 아니라 큰 오류다. 시차 오차가 **시차에 비해 작아서** 선형 근사가 선다. 그리고 두 영상의 오차가 **독립**이다.
>
> $$\sigma_Z=\frac{Z^2\,\sigma_d}{f\,b}$$
>
> $Z$는 거리, $\sigma_d$는 시차 잡음, $f$는 픽셀 단위 초점 거리, $b$는 기선이다. Keselman 등이 RealSense 스테레오 카메라에 대해 적은 법칙이다([arXiv:1705.05548](https://arxiv.org/abs/1705.05548)).
>
> - **예**: 파사드에서 $4\times0.707/72=39.3\,\mathrm{mm}$, 거리의 약 $2\%$다. $8\,\mathrm m$에서는 $628.5\,\mathrm{mm}$인데, $\sigma_d/d=0.079$가 더는 작지 않고 $Z=fb/d$가 볼록이라 §10의 시뮬레이션은 $644.3\,\mathrm{mm}$와 $+49.4\,\mathrm{mm}$ 편향을 준다.
> - **비예**: 넓은 기선은 공짜가 아니다. $b=0.24\,\mathrm m$이면 오차가 $19.6\,\mathrm{mm}$로 반이 되지만, 시차를 $128$까지 찾는 매처는 $0.562$가 아니라 $fb/128=1.125\,\mathrm m$보다 가까운 것을 보지 못하고(3.5 §2의 가까운 쪽 한계), 두 시점의 차이도 커진다.
> - **왜 중요한가**: 리그가 한 거리에서 무엇을 약속하는지, 어디서 다른 센서가 이어받는지를 말해 준다. 교과 LiDAR의 $20\,\mathrm{mm}$는 거리에 따라 자라지 않으므로, 스테레오는 $\sqrt{\sigma_L fb/\sigma_d}=1.43\,\mathrm m$보다 가까울 때만 그것을 이긴다.

광선을 가로지르는 방향으로는 같은 픽셀 잡음이 $2\,\mathrm m$에서 $Z\sigma_u/f=1.67\,\mathrm{mm}$일 뿐이다. 스테레오 점은 광선을 따라 늘어난 바늘이고, 폭보다 $\sqrt2\,Z/b=23.6$배 길다.

**스테레오가 표면에 요구하는 것.** 시차는 한 조각을 다른 영상에서 다시 찾을 수 있는 곳에만 있다. 고르게 칠한 패널은 모든 창에 같은 내용을 주어 맞출 봉우리가 없다(3.5 §2.5의 평평한 구조 텐서). 똑같은 패널이 줄지어 있으면 패널마다 좋은 짝이 하나씩 있고, 3.5 §2.6은 틀린 짝이 epipolar 검사를 통과해 $40\,\mathrm{cm}$ 멀리 떨어지는 것을 보여 준다. $\sigma_Z$는 둘 다 값을 매기지 않는다. 짝이 옳다고 가정하기 때문이다.

**능동 스테레오.** 적외선 무늬를 쏘는 프로젝터는 민무늬 패널에 무늬를 입힌다. 삼각측량은 여전히 두 카메라 사이에서 한다. Keselman 등은 프로젝터에 바로 그 일 — 매칭을 모호하지 않게 하는 무늬 — 만 맡기고, 무늬가 조밀하고, 광도가 일정하며, 매칭 축을 따라 반복하지 않기를 요구한다. 적외선만 보는 그 카메라는 프로젝터만 비추는 어둠에서도, 해가 장면 자체의 무늬를 비추는 한낮에도 작동한다.

### 4. 비행시간 카메라와 구조광 깊이 카메라

*한 문장으로:* 비행시간(ToF) 카메라는 제 빛이 돌아오는 데 걸린 시간을 펄스의 지연으로 직접, 또는 위상으로 간접 재고, 구조광 카메라는 스스로 쏜 무늬를 기준으로 삼각측량한다. 둘 다 제 빛을 가져오므로 어둠에서 작동하고, 둘 다 해보다 밝아야 한다.

**문제.** 스테레오는 무늬가 필요하고 $Z^2$로 나빠진다. 스스로 장면을 비추는 카메라는 무늬가 필요 없고, 각도 대신 시간을 재면 삼각측량의 $Z^2$ 법칙에서 벗어난다. 핵심은 이것이다: 빛은 빠르지만 무한히 빠르지는 않아서, 파사드까지 다녀오는 데 잴 수 있는 시간이 걸리고, 그 시간이 곧 거리다.

**펄스 비행시간.** 펄스는 $c=299{,}792{,}458\,\mathrm{m/s}$(정의상 정확한 값, [NIST](https://physics.nist.gov/cgi-bin/cuu/Value?c))로 갔다 오며 $2R$을 달린다.

$$R=\frac{c\,\tau}{2}$$

지연 $\tau$가 가는 길과 오는 길을 모두 담기 때문이다. $1$나노초는 거리 $0.1499\,\mathrm m$이므로, 직접 비행시간 센서는 무엇보다 먼저 시간 재는 기계다. **P5**의 거리 센서를 이렇게 읽어 보자(3.2는 어떻게 거리를 재는지 말하지 않는다. 새 사실이 아니라 해석이다). $12\,\mathrm{cm}$는 왕복 $0.801\,\mathrm{ns}$, $\sigma_r=10\,\mathrm{mm}$는 $66.7\,\mathrm{ps}$의 시간 지터이고, $4\,\mathrm{mm}$ 장착 오프셋은 고정된 $26.7\,\mathrm{ps}$의 추가 지연처럼 읽힌다. 보정은 없애고 평균은 없애지 못하는 편향이다(3.2 §5).

**연속파 비행시간.** 픽셀마다 피코초를 재기는 어려워서, 많은 깊이 카메라는 빛을 변조하고 대신 위상을 잰다. Azure Kinect의 깊이 카메라가 한 예로, 진폭 변조한 근적외선을 쏘고 그 비행시간을 간접적으로 기록한다([Microsoft Learn](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/depth-camera)). 지연 $\tau=2R/c$는 $f_{\text{mod}}$로 변조된 파형의 $f_{\text{mod}}\tau$주기이므로, 돌아온 빛은 다음만큼 뒤진다.

$$\varphi=2\pi f_{\text{mod}}\frac{2R}{c},\qquad R=\frac{c\,\varphi}{4\pi f_{\text{mod}}}$$

Baek 등이 적은 관계와 같다([arXiv:2105.11606](https://arxiv.org/abs/2105.11606)). 두 사실이 따라 나온다. 위상 오차 $\sigma_\varphi$는 거리 오차 $c\sigma_\varphi/(4\pi f_{\text{mod}})$다. 교과 카메라의 $0.02\,\mathrm{rad}$에서 $100\,\mathrm{MHz}$는 $4.77\,\mathrm{mm}$, $20\,\mathrm{MHz}$는 $23.86\,\mathrm{mm}$이니 높은 주파수가 정밀하다. 그리고 위상은 $2\pi$를 법으로만 알 수 있다. 분은 보여 주되 시는 보여 주지 않는 시계와 같다.

> **모호 거리의 정의.** 연속파 비행시간 센서의 **모호 거리**(ambiguity range)는 *위상이 하나의 값으로 보고하는 가장 큰 거리*다. 장면이 아니라 변조의 성질이다. 조건 셋. 빛이 $f_{\text{mod}}$로 **주기적으로** 변조된다. 위상은 **$2\pi$를 법으로** 잰다. 그리고 각 픽셀에 **지배적인 귀환이 하나**다(두 경로가 섞인 픽셀은 어느 쪽도 보고하지 못한다).
>
> $$R_{\text{amb}}=\frac{c}{2f_{\text{mod}}}$$
>
> $c$는 광속, $f_{\text{mod}}$는 변조 주파수다. 왕복이 정확히 변조 한 주기가 되어 위상이 제자리로 돌아오는 거리다.
>
> - **예**: $100\,\mathrm{MHz}$에서 $R_{\text{amb}}=1.499\,\mathrm m$이므로 $2.000\,\mathrm m$의 파사드는 $0.501\,\mathrm m$로 읽힌다. $80\,\mathrm{MHz}$($1.874\,\mathrm m$)에서는 $0.126\,\mathrm m$다. 두 판독의 짝은 왕복 시간이 두 주기 $10$과 $12.5\,\mathrm{ns}$의 정수배가 될 때에만 되풀이되고, 그 첫 시각은 두 주파수를 모두 나누는 가장 큰 주파수 $20\,\mathrm{MHz}$의 주기 $50\,\mathrm{ns}$다. 그래서 둘을 함께 쓰면 높은 주파수의 정밀도로 $c\times50\,\mathrm{ns}/2=7.495\,\mathrm m$까지 $2.000\,\mathrm m$를 하나로 읽는다.
> - **비예**: 모호 거리는 작업 거리가 아니다. 그 안에 있어도 어두운 벽은 잴 만큼 빛을 돌려주지 않을 수 있다. Azure Kinect 문서는 약한 신호와 포화한 신호를 픽셀을 무효로 처리하는 이유로 든다.
> - **왜 중요한가**: 감긴 거리는 잡음 낀 옳은 수가 아니라 확신에 찬 틀린 수다. $0.501\,\mathrm m$는 판독 하나에 대한 어떤 검사도 통과하고, 두 번째 주파수나 사전 정보나 다른 센서만이 잡아낸다.

**깊이 카메라가 현장에서 실패하는 곳.** 원인이 분명한 세 가지다. **다중 경로**(multipath): 픽셀 하나가 둘 이상의 경로로 온 빛을 적분한다. Azure Kinect 문서의 흔한 예는 모서리로, 빛이 한 벽에서 튕겨 다른 벽으로 간다 — 두 패널 사이의 안쪽 모서리가 그렇다. **떠다니는 픽셀**(flying pixels): 깊이 경계에서 한 픽셀이 앞과 뒤를 함께 보고 그 사이의 거리를 보고한다([Zollhöfer, arXiv:1902.06835](https://arxiv.org/abs/1902.06835)). **햇빛**: 센서 자신의 빛을 같은 파장의 주변광에 맞서 읽어야 하고, Zollhöfer는 강한 햇빛에서 비행시간 방식이 고전한다고 적는다.

**구조광.** 스테레오 쌍의 카메라 하나를 알려진 무늬를 쏘는 프로젝터로 바꾸고, 카메라와 프로젝터 사이에서 삼각측량한다. Zollhöfer는 이 프로젝터를 역카메라(inverse camera)라 부른다([Geng 2011](https://doi.org/10.1364/AOP.3.000128)이 이 계열을 정리한다). 기하는 프로젝터–카메라 기선 $b_p$를 쓴 §3과 같아서 오차가 $Z^2/(f\,b_p)$로 자란다. 약점은 빛이다. 표면 위 무늬의 밝기는 $1/R^2$로 떨어지는데 햇빛은 전혀 떨어지지 않아서, 바깥에서는 해가 무늬를 덮는다. Zollhöfer는 해의 적외선이 센서를 포화시켜 무늬를 알아볼 수 없게 만들 수 있다고 적는다.

> [!note]- 더 깊이 · Deeper
> **무늬가 $1/R^2$로 해에게 지는 이유.** 프로젝터는 고정된 출력을 면적이 $R^2$로 커지는 무늬에 펼치므로 표면의 조도가 $1/R^2$에 비례하지만, 그 표면에 떨어지는 햇빛의 조도는 $R$과 무관하다. 비가 $1/R^2$로 떨어지고, 거리를 두 배로 하면 해독기가 쓸 대비가 사분의 일이 된다. Zollhöfer의 개관은 한 표면을 여러 능동 센서가 함께 보면 서로의 무늬를 방해할 수 있다고도 경고한다. 리그에 깊이 카메라 둘을 달기 전에 알아 둘 일이다.

### 5. LiDAR

*한 문장으로:* LiDAR는 정해진 방향 격자로 짧은 레이저 펄스를 쏘고 메아리의 시간을 재므로, 거리 오차는 거리에 따라 거의 자라지 않지만 표본은 벌어지고, 점은 커지고, 점들은 한 순간이 아니라 한 번의 훑기 동안 찍힌다.

**문제.** 스테레오의 오차는 $Z^2$로 자란다. 파사드에서 $39\,\mathrm{mm}$, $8\,\mathrm m$에서 $628\,\mathrm{mm}$. LiDAR의 발상은 §4의 펄스 거리계를 정해진 방향 격자로 휘두르는 것이다. 그러면 점 하나하나는 어느 거리에서나 거리는 좋고, 떨어지는 자리는 성기다.

**측정.** 펄스 레이저로 거리를 재며([NOAA](https://oceanservice.noaa.gov/facts/lidar.html)) §4와 같은 $R=c\tau/2$를 쓰고, 대개 $905$나 $1550\,\mathrm{nm}$에서 작동한다([Li and Ibanez-Guzman 2020](https://arxiv.org/abs/2004.08467), [Dreissig et al. 2023](https://arxiv.org/abs/2304.06312)). 교과 LiDAR의 $\sigma_L=20\,\mathrm{mm}$는 $133\,\mathrm{ps}$의 시간 지터이고, 시간 오차는 어느 거리에서나 같으므로 거리 오차는 평평하다. 스테레오에 없는 성질이다. 회전식 장치는 채널 $32$개를 고도 방향으로 쌓고, 초당 $10$바퀴를 돌며 $0.2^\circ$마다 한 열을 쏜다. 한 바퀴 $1{,}800$열, 초당 $576{,}000$점으로, 한 제조사가 제시하는 $32$–$256$채널, $512$–$4{,}096$열 범위 안에 있다([Ouster](https://ouster.com/os-overview)).

**표본이 떨어지는 자리.** 고정된 각도 간격 $\Delta\phi$는 센서를 마주한 표면 위에서 호 $R\,\Delta\phi$가 된다. 그래서

$$s_h=R\,\Delta\phi,\qquad s_v=R\,\Delta\varepsilon,\qquad \rho_{\text{pts}}=\frac{1}{s_h\,s_v}\ \propto\ \frac{1}{R^2}$$

$\Delta\varepsilon$은 채널 간격, $\rho_{\text{pts}}$는 제곱미터당 점 수다. 점 하나가 $s_h\times s_v$ 칸 하나를 대표하기 때문이다. 파사드의 $2\,\mathrm m$에서 $7.0\times34.9\,\mathrm{mm}$, $4{,}104$점/m². $10\,\mathrm m$에서는 $34.9\times174.5\,\mathrm{mm}$, $164$점이다. 빔에서 비스듬히 돌아선 표면은 간격을 $1/\cos\alpha$만큼 늘린다([[05-construction-robotics/site-perception|5. 현장 인식 §1]]이 측량 스캐너에 대해 그렇게 정의한다). $L$ 옆에서는 빔이 $2.12\,\mathrm m$로 더 길고 파사드 법선에서 $19.5^\circ$ 벗어나 닿으므로, 그 자리에서 그림의 간격은 $7.4$와 약 $38\,\mathrm{mm}$다.

> **빔 풋프린트의 정의.** **빔 풋프린트**(beam footprint)는 *펄스 하나가 표면 위에 밝히는 점의 지름*, 곧 거리 측정 하나가 덮는 넓이다. 측정 사이의 거리가 아니다. 조건 넷. 빔이 창을 **지름** $w_0$로 떠난다. 작은 **전 발산각** $\theta$로 퍼진다. **거리** $R$에서 잰다. 그리고 **입사각** $\alpha$가 기운 방향으로 점을 $1/\cos\alpha$만큼 늘린다.
>
> $$w(R)=w_0+\theta R$$
>
> 수직 입사에서의 식이고, 둘째 항은 발산각이 거리 $R$에서 그리는 호다. 그래서 점의 크기와 간격이 모두 거리에 비례해 자란다.
>
> - **예**: 파사드에서 $w=10+3.0\times2=16\,\mathrm{mm}$인데 링을 따라 간격은 $7.0\,\mathrm{mm}$라 점마다 양쪽 이웃 둘씩과 겹치고, 링 사이는 $34.9\,\mathrm{mm}$라 어떤 펄스도 닿지 않는 벽이 $18.9\,\mathrm{mm}$ 남는다. $10\,\mathrm m$에서는 $40\,\mathrm{mm}$다.
> - **비예**: 점이 겹치기 시작하면 열 간격을 줄여도 측정이 고와지지 않는다. $0.1^\circ$면 $16\,\mathrm{mm}$마다 점이 둘이 아니라 넷이지만, 각자 제 점 전체에 대해 거리 하나를 돌려주므로 점 안의 모서리는 더 날카로워지지 않는다.
> - **왜 중요한가**: S1은 구멍을 $\pm5\,\mathrm{mm}$로 맞춘다([[05-construction-robotics/site-engineering|2.5]]). $35$–$38\,\mathrm{mm}$ 간격 링 위의 $16\,\mathrm{mm}$ 점은 그것을 보지 못하고, 카메라의 $3.3\,\mathrm{mm}$ 픽셀은 본다. 패널 앞에서 LiDAR가 주는 것은 구멍이 아니라 구멍 주변의 기하다.

**현장에서 실패하는 곳.** 네 조건, 표면의 것 둘과 공기의 것 둘. **어두운 표면**은 빛을 덜 돌려준다. 빔을 채우고 고르게 흩뿌리는 표면이면 돌아오는 출력이 $\rho/R^2$로 가므로(아래 더 깊이에서 유도한다), 반사율 $0.1$의 어두운 패널은 같은 거리에서 반사율 $0.8$의 흰 패널의 팔분의 일을 돌려주고, 거리의 $1/\sqrt8=0.354$에서야 그만큼을 돌려준다. **유리와 광택 금속**은 펄스를 거울처럼 다른 데로 보낸다. Henley 등은 이런 정반사 면이 직접 단일 산란 귀환에 기대는 LiDAR에 보이지 않을 수 있다고 적는다([*Optics Express* 2023](https://doi.org/10.1364/OE.479900)). **비와 안개**는 펄스를 흩어서, 일부 빛은 허공의 점으로 일찍 돌아오고 일부는 돌아오지 않는다([Dreissig et al. 2023](https://arxiv.org/abs/2304.06312)). **먼지**는 현장 고유의 경우다. Phillips, Guenther, McAree는 LiDAR가 먼지구름을 무작위 잡음이 아니라 그 앞쪽 경계로 재고, 투과율이 약 $71$–$74\%$ 아래로 내려가면 먼지가 측정에 영향을 주기 시작하며, 먼 곳에서는 효과가 약하다는 것을 보였다([*Journal of Field Robotics* 2017](https://doi.org/10.1002/rob.21701)). 귀환을 하나만 기록하는 LiDAR에게 톱이 일으킨 먼지는 벽이다.

**훑기에는 시간이 걸린다.** 한 바퀴는 $100\,\mathrm{ms}$이고 그동안 베이스는 $50\,\mathrm{mm}$ 간다. 빔이 파사드의 $120^\circ$를 가로지르는 데 $33.3\,\mathrm{ms}$가 걸리므로 클라우드 하나 속 파사드는 $16.7\,\mathrm{mm}$ 번진다. [[04-robotics/state-estimation-slam|3. 상태 추정 §7.2]]가 처방을 준다. deskewing, 곧 점마다 제가 발사된 시각의 센서 자세로 한 시각에 옮겨 놓는 것이다. 그러려면 점마다 시각이 필요한데, ROS 포인트 클라우드는 클라우드 전체에 헤더 스탬프 하나만 싣는다([`sensor_msgs/PointCloud2`](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/PointCloud2.msg)). 점별 시각은 드라이버가 필드로 넣을 때만 있고, 센서 자체의 패킷은 열마다 타임스탬프를 실을 수 있다([Ouster, *Sensor Data*](https://static.ouster.dev/sensor-docs/image_route1/image_route2/sensor_data/sensor-data.html)). 교과 LiDAR가 훑기의 시작을 스탬프로 찍으면, $L$을 보는 열은 스탬프보다 $46.1\,\mathrm{ms}$ 뒤에 쏜다. 그 스탬프를 쓰면 베이스 이동 $23.1\,\mathrm{mm}$만큼 어긋난다(§9).

> [!note]- 더 깊이 · Deeper
> **표면에서 돌아오는 출력.** 빔을 채우고 모든 방향으로 고르게 흩뿌리는 표면(람베르트 면), 반사율 $\rho$, 수직 입사를 생각하자. 펄스 출력 $P_t$의 $\rho$만큼을 축 방향 세기 $\rho P_t/\pi$(스테라디안당)로 돌려보내고, 거리 $R$의 면적 $A_r$ 수신기는 $A_r/R^2$ 스테라디안을 차지하므로 $P_r=\rho P_tA_r/(\pi R^2)$이다. 표면이 빔을 채우면 점의 크기는 약분된다. 제조사는 이런 과녁으로 거리를 말한다. 한 제조사는 반사율 채널을 람베르트 과녁으로 보정하고, 그 눈금은 완전한 흰색보다 $864$배 밝은 재귀반사체까지 이른다(Ouster, *Sensor Data*).
>
> **펄스 하나, 메아리 여럿.** 패널 모서리와 그 뒤 $0.3\,\mathrm m$의 벽에 걸친 점은 봉우리 둘을 돌려준다. USGS 라이다 규격은 저장한 봉우리들을 이산 귀환, 첫 귀환과 마지막 귀환이라 부르고([USGS glossary](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-glossary)), 가장 강한 귀환과 두 번째로 강한 귀환을 함께 보고하는 센서는 비, 안개, 철망 너머를 볼 수 있다(Ouster). Phillips 등은 투과율 $2\%$의 먼지구름 너머 재귀반사 과녁까지, $6\%$면 반사율 낮은 과녁까지 여전히 거리를 재는 것도 보였다.
>
> **회전식과 고체식.** 회전식은 발광부를 모터로 돌려 사방을 본다. 고체식은 칩 위의 작은 거울(MEMS)이나 광위상배열로 빔을 돌리거나, 장면 전체를 한꺼번에 비춘다(플래시). Li와 Ibanez-Guzman은 플래시 방식이 모든 거리를 동시에 재므로 훑는 센서가 필요로 하는 운동 보정을 피한다고 적는다.

### 6. 레이더

*한 문장으로:* FMCW(주파수 변조 연속파) 레이더는 주파수를 쓸어 올리므로 반사체의 거리는 비트 주파수가, 시선 방향 속도는 처프 사이의 위상 걸음이, 방위는 안테나 사이의 위상 걸음이 된다. 두 반사체를 얼마나 곱게 가르는지는 메아리의 세기가 아니라 쓸어 준 것 — 대역폭, 시간, 개구 — 이 정한다.

**문제.** 먼지, 연기, 어둠 속에서는 카메라도 스테레오도 LiDAR도 나빠지는데, 베이스 가까이의 사람이야말로 놓치면 안 되는 것이다. 레이더의 파장은 마이크로미터가 아니라 밀리미터이고, 제 신호를 가져온다. 발상은 이렇다: 펄스의 시간을 재는 대신 음높이가 꾸준히 올라가는 소리를 보낸다. 메아리는 조금 늦은 같은 소리이고, "조금 늦음"은 일정한 음높이 차로 나타난다.

**처프와 비트.** 송신 주파수는 선형으로 올라간다. $f(t)=f_c+St$, 기울기 $S=B/T_c$, 시간 $T_c$ 동안 대역폭 $B$를 쓴다. 거리 $R$의 메아리는 $\tau=2R/c$만큼 늦은 같은 처프이고, 아직 나가고 있는 처프와 섞으면 두 기울기가 같으므로 차이가 일정하다.

$$f_b=S\,\tau=\frac{2SR}{c}$$

거리가 주파수가 된 것이다. 교과 레이더는 $50\,\mathrm{\mu s}$에 $1.0\,\mathrm{GHz}$를 쓸어 $S=20\,\mathrm{MHz/\mu s}$이고, $2\,\mathrm m$의 파사드는 $266.9\,\mathrm{kHz}$로 맥놀이친다. 수신기는 $5\,\mathrm{MHz}$ 중간 주파수(IF) 대역 안의 비트만 통과시키므로, 거리는 $5\,\mathrm{MHz}\times c/(2S)=37.5\,\mathrm m$로 묶인다. 이 대역은 실제로 쓰인다. 단일 칩 센서 하나가 송신기 $3$개, 수신기 $4$개, $4\,\mathrm{GHz}$ 쓸기로 $76$–$81\,\mathrm{GHz}$를 덮고([TI AWR1843](https://www.ti.com/product/AWR1843)), Harlow 등이 로보틱스에 대해 개관한 대역도 이것이다([IEEE T-RO 2024](https://arxiv.org/abs/2305.01135)).

**두 거리 가르기.** 처프 하나는 길이 $T_c$인 기록이고, 그 길이의 기록은 $1/T_c$ 떨어진 주파수를 가른다. DFT의 빈 간격이다([[02-foundations/signal-processing|6. 신호처리 §3]]). $\Delta f_b=1/T_c$를 $f_b=2SR/c$에 넣으면 $\Delta R=c/(2ST_c)$이고, $ST_c=B$이므로 쓸어 준 대역폭만 남는다.

> **거리 분해능의 정의.** FMCW 레이더의 **거리 분해능**(range resolution)은 *두 반사체가 처프 하나의 스펙트럼에서 봉우리 둘로 보이기 시작하는 거리 간격*이다. 거리 셀의 크기이지, 반사체 하나의 거리를 얼마나 정밀하게 읽느냐가 아니다. 조건 셋. 처프가 $T_c$ 동안 대역폭 $B$의 **선형**이다. 메아리를 **처프 하나**의 스펙트럼에서 가르고, 그 셀은 $1/T_c$ 폭이다. 그리고 두 반사체의 **세기가 비슷**하고 빔 방향으로 거리가 다르다.
>
> $$\Delta R=\frac{c}{2B}$$
>
> $c$는 광속, $B$는 쓸어 준 대역폭이다(Harlow 등의 서술). 반송파도, 처프 길이도, 샘플링 속도도 아닌 대역폭만이 정한다.
>
> - **예**: $1\,\mathrm{GHz}$면 셀이 $14.99\,\mathrm{cm}$다. 파사드 앞 $0.30\,\mathrm m$의 작업자는 파사드에서 두 셀 떨어져 있고, §10은 시도한 상대 위상 $36$개 모두에서 두 메아리를 가른다. $0.5\,\mathrm{GHz}$(한 셀)에서는 $36$개 중 $13$개, $0.25\,\mathrm{GHz}$에서는 하나도 없다. 한 셀은 가를 수 있게 되기 시작하는 곳, 두 셀은 믿을 수 있게 되는 곳이다.
> - **비예**: 분해능은 정밀도가 아니다. 홀로 있는 반사체 하나의 거리는 셀보다 훨씬 곱게 읽을 수 있다. 아래의 도플러 걸음은 처프당 거리 $0.08\,\mathrm{mm}$를 위상만으로 읽는다. $15\,\mathrm{cm}$는 두 반사체를 가르는 문제다.
> - **왜 중요한가**: 파사드 앞 작업자가 레이더에게 두 번째 물체인지는 $B$가 정한다. 그리고 S1의 $\pm5\,\mathrm{mm}$는 셀 하나의 삼십분의 일이다. 레이더가 구멍을 맞추지 못하는 이유다.

**위상에서 속도.** $T_c$ 떨어진 처프 사이에 $\dot R$로 다가오는 반사체는 $\dot RT_c$ 움직인다. 비트 주파수를 바꾸기에는 너무 작지만, 반송파 파장 $\lambda=c/f_c=3.893\,\mathrm{mm}$에서 $4\pi R/\lambda$인 메아리의 위상(경로가 $2R$이고 파장마다 $2\pi$)은 $\Delta\varphi=4\pi\dot RT_c/\lambda$만큼 돈다. 그래서

$$\dot R=\frac{\lambda\,\Delta\varphi}{4\pi T_c},\qquad v_{\max}=\frac{\lambda}{4T_c},\qquad v_{\text{res}}=\frac{\lambda}{2N_cT_c}$$

걸음은 $|\Delta\varphi|<\pi$일 때만 하나로 정해지고, 처프 $N_c$개는 위상에서 길이 $N_cT_c$의 기록이 되어 같은 빈 간격 논리로 갈리기 때문이다(앞의 둘은 Harlow 등이 준다). $1.6\,\mathrm{m/s}$로 레이더 쪽으로 걷는 작업자는 처프마다 위상을 $-0.2582\,\mathrm{rad}$ 돌리고, §10은 이를 $-1.600\,\mathrm{m/s}$로 되읽는다. 처프 $128$개면 속도 셀이 $0.304\,\mathrm{m/s}$라 작업자는 정지한 파사드에서 $5.26$셀 떨어져 있고, $v_{\max}=19.47\,\mathrm{m/s}$다. 함정: 시선 방향 성분만 센다. 레이더 바로 앞을 파사드를 따라 가로지르는 작업자는 그 자리에서 시선 속도가 없으므로, 아무리 빨리 걸어도 도플러가 그를 파사드와 가르지 못한다. 그리고 움직이는 베이스 위에서는 정지한 파사드도 방위에 따라 변하는 시선 속도를 가진다. 레이더 오도메트리가 읽는 무늬가 그것이다.

**안테나 사이의 위상에서 방위.** $d$ 떨어진 수신기들은 방위 $\vartheta$의 메아리를 하나 건너 $2\pi d\sin\vartheta/\lambda$의 위상 걸음으로 본다. $4\pi$가 아니라 $2\pi$인 것은 더해진 경로 $d\sin\vartheta$가 돌아오는 길에만 있기 때문이다. 소자 $N$개에 걸친 DFT는 $2\pi/N$ 떨어진 걸음을 가르므로 — 빈 간격 논리의 세 번째 등장이다 — $d=\lambda/2$에서 $\Delta\sin\vartheta=2/N$을 가른다. 교과 레이더의 송신기 $3$개는 수신기 $4$개와 번갈아 짝지어져 한 줄로 늘어선 수신기 $12$개(가상 배열)처럼 동작하고, $2/12\ \mathrm{rad}=9.55^\circ$를 가른다. 파사드에서 폭 $0.33\,\mathrm m$, $10\,\mathrm m$에서 $1.67\,\mathrm m$인 셀이다.

**먼지를 꿰뚫는 이유, 그리고 보지 못하는 것.** $3.9\,\mathrm{mm}$ 파장은 먼지 알갱이나 안개 방울보다 길다. Harlow 등은 분명히 적는다. 긴 파장은 안개, 먼지, 연기 같은 시각적 방해물을 비껴갈 수 있다. 제 신호를 가져오므로 어둠도 문제가 아니다. 비는 투명하지 않다. $77\,\mathrm{GHz}$ 자동차 레이더를 강우계로 쓰는 연구까지 있다([Bertoldo et al. 2018](https://etasr.com/index.php/ETASR/article/view/1755)). 레이더가 주지 못하는 것은 기하다. 귀환이 성기고 잡음이 많으며, 다중 경로 "유령" 물체가 생기고, 고도 채널이 없으면 높이를 거의 모른다(Harlow 등). 그래서 S1 현장에서 레이더의 일은 다른 센서들이 가장 못하는 일이다. 먼지 속, 밤에, 움직이는, 베이스 근처의 사람.

> [!note]- 더 깊이 · Deeper
> **레이더가 이미 이 일을 하는 곳.** 자동차는 적어도 2005년부터 운전 보조에 레이더를 실어 왔고, 로봇은 시계가 나쁠 때 오도메트리·지도·검출에 쓰며 광산도 그중 하나다(Harlow 등). 대형 기계 주변에서는 가까운 사람을 경고한다. 오프로드 덤프트럭 시험은 레이더가 사람, 소형 차량, 둔덕, 다른 장비를 믿을 만하게 검출했지만 위험하지 않은 물체에 대한 경보도 잦았다고 보고하고, 운전자가 경보마다 원인을 확인할 수 있도록 카메라와 함께 쓰라고 권했다([Ruff 2006](https://doi.org/10.1016/j.aap.2005.07.006)). 운반로 위에서 본 §7의 분업이다.

### 7. 현장 조건에 맞는 센서 고르기

*한 문장으로:* 센서는 저마다 제 물리가 무너지는 곳에서 실패한다 — 카메라는 빛에서, 스테레오는 무늬에서, 능동 깊이 카메라는 햇빛에서, LiDAR는 입자와 유리에서, 레이더는 미세 구조에서. 그래서 현장 리그는 가장 좋은 날의 정확도가 아니라 견뎌야 할 조건으로 고른다.

**문제.** 데이터시트는 센서를 가장 좋은 날의 모습으로 적는다. 현장은 낮은 해, 먼지, 비, 어둠, 똑같은 패널의 줄을 한꺼번에 내놓는다. 발상은 §1–§6을 차례로 내려가며 조건마다 어느 물리 단계가 부러지는지 묻는 것이다. 아래 표가 파사드의 $2\,\mathrm m$에서 그 일을 한다. 칸마다 이 페이지에서 유도했거나 해당 절이 인용한 출처에서 가져왔고, 줄표는 이 페이지가 값을 매기지 않았다는 뜻이며, 비용 열은 첫 선택을 위한 상대적·정성적 등급일 뿐 견적이 아니다.

| 센서 | 어둠 / 낮은 해 | 먼지, 안개, 비 | 민무늬, 반복, 유리 | $2\,\mathrm m$의 깊이 오차 | $2\,\mathrm m$의 표본 | 도달 | 비용 등급 |
|---|---|---|---|---|---|---|---|
| 카메라 | 실패: 빛만 모은다 / 글린트 $80\,\mathrm{dB}$가 센서의 $66$을 넘는다(§1) | 시각적 방해물(§6) | 특징이 없거나 틀린 특징(3.5 §2.5–§2.6) | 영상 한 장으로는 없음(3.5 §1) | 픽셀당 $3.3\,\mathrm{mm}$ | 빛이 닿는 어디든; 블러 $fvt_{\exp}/Z$(§2) | 낮음 |
| 스테레오 쌍 | 카메라와 같음 | 카메라와 같음 | 민무늬 패널에 깊이 없음; 반복 패널에 $40\,\mathrm{cm}$ 오차(3.5 §2.6) | $39.3\,\mathrm{mm}$(§3) | 짝이 맞은 곳에서 $3.3\,\mathrm{mm}$ | $0.56\,\mathrm m$부터; $\sigma_Z\propto Z^2$ | 낮음 |
| 능동 스테레오 | 제 무늬로 작동 / 햇빛 받은 무늬로 작동(§3) | 카메라와 같음 | 무늬가 질감을 준다(§3) | 스테레오와 같음 | 스테레오와 같음 | 스테레오와 같음 | 낮음–중간 |
| ToF 카메라 | 작동 / 강한 햇빛에서 고전(§4) | — | 모서리의 다중 경로, 경계의 떠다니는 픽셀(§4) | $100\,\mathrm{MHz}$에서 $4.77\,\mathrm{mm}$, $1.5\,\mathrm m$ 넘으면 감김(§4) | 픽셀마다 거리 하나 | 두 주파수로 $7.5\,\mathrm m$까지 유일 | 낮음–중간 |
| 구조광 | 작동 / 해가 센서를 포화시킬 수 있음(§4) | — | 무늬가 보여야 함 | $\propto Z^2/(fb_p)$(§4) | 픽셀마다 거리 하나 | 짧다: 대비 $\propto1/R^2$(§4) | 낮음 |
| 회전식 LiDAR | 작동: 제 펄스(§5) | 이른 귀환과 잃은 귀환; 먼지는 앞쪽 경계에서 보임(§5) | 유리는 사라질 수 있음; 어두우면 귀환 $\propto\rho$(§5) | $20\,\mathrm{mm}$, 거리에 평평(§5) | $7.0\times34.9\,\mathrm{mm}$, $16\,\mathrm{mm}$ 점 | $10\,\mathrm m$에서 $164$점/m², $50$에서 $7$(§10) | 높음 |
| FMCW 레이더 | 작동: 제 신호(§6) | 안개, 먼지, 연기를 꿰뚫음; 비는 손실과 잡동사니를 더함(§6) | 성기고 잡음 많음, 유령(§6) | $15\,\mathrm{cm}$ 셀(§6) | $0.33\,\mathrm m$ 각도 셀 | 교과 IF 대역에서 $37.5\,\mathrm m$ | 낮음–중간 |

**S1의 현장에 대 보기.** 패널 근처의 네 조건과 그것이 리그에 하는 일:
- **유리 파사드에 낮은 아침 해.** 카메라는 그늘진 패널에 노출을 맞추고 글린트는 빠진 데이터로 다룬다(§1). LiDAR는 제 빛을 가져오지만 유리를 잃을 수 있다(§5). 노출을 여러 번 나눠 찍는 것은 베이스가 멈춰 있을 때만 돕는다. 움직이면 각 노출이 다른 자리를 보기 때문이다(§9).
- **절단 작업의 먼지.** 귀환을 하나만 기록하는 LiDAR는 구름을 그 앞쪽 경계의 표면으로 보고하고(§5), 카메라는 대비를 잃고, 레이더는 꿰뚫는다. 구름 밖으로 걸어 나오는 사람을 처음 보는 것은 레이더이고, 움직이는 것으로 본다(§6).
- **야간 작업.** 카메라는 빛이 필요한데, 짧은 노출 동안만 켜지는 스트로브는 §2의 블러와 스큐까지 없앤다. LiDAR와 레이더는 어둠을 알아채지도 못한다.
- **똑같은 패널의 줄.** 스테레오는 틀린 패널과 짝지어 모든 기하 검사를 통과할 수 있다(3.5 §2.6). LiDAR는 칠에 속지 않지만, 평평한 파사드에서는 ICP가 파사드를 따라 미끄러질 수 있다(3.5 §4).

함정은 "가장 좋은 센서"를 고르려는 것이다. 리그는 물리에 따라 일을 나눈다. LiDAR는 접근 경로의 지도를, 레이더는 먼지와 어둠 속의 사람을 맡고, S1 구멍의 마지막 $\pm5\,\mathrm{mm}$는 카메라의 몫이다 — 가까이서, 짧은 노출로, 제 빛으로, 노출 중간에 스탬프를 찍고, 베이스를 멈추거나 그 운동을 몇 밀리초 안으로 알고서(§9). 계산 절이 각 조건에 값을 매긴다.

### 8. 리그: 서로 다른 센서 사이의 외부 파라미터

*한 문장으로:* 모든 센서의 자세를 한 프레임에서 알아야 비로소 리그가 한 기기가 되고, 두 센서 사이의 회전 오차는 투영된 모든 점을 같은 각도만큼 옮긴다 — 픽셀로는 일정하고 밀리미터로는 자라는 양이다.

**문제.** LiDAR는 제 프레임에서, 카메라는 제 프레임에서 $L$을 잰다. 둘을 융합하려면 — 점에 색을 입히고, 영상으로 LiDAR 점에 라벨을 달고, 서로를 검사하려면 — 둘 사이의 변환이 필요하고, 그 변환의 오차는 센서끼리의 불일치와 똑같아 보인다. 발상은 둘 다 볼 수 있는 과녁으로 변환을 보정하고, 회전·병진·시간에 대해 답이 서로 다르게 변하는 시험으로 검사하는 것이다.

**보정하기.** [[04-robotics/geometric-perception-calibration|3.5 §5]]는 카메라를 카메라에, 그리고 그리퍼에 보정한다. 카메라와 LiDAR도 공유 과녁을 쓰지만 보는 방식이 다르다. 카메라는 모서리를 픽셀의 몇 분의 일까지 보아 PnP로 카메라 프레임에서의 과녁 자세를 얻고([[04-robotics/geometric-perception-calibration|3.5 §2.7]]), LiDAR는 $7\times35\,\mathrm{mm}$ 간격의 $16\,\mathrm{mm}$ 점으로 평면과 가장자리를 본다. 문서화된 한 작업 흐름은 체커보드를 두 센서에 여러 자세로 보여 주고, 두 프레임에서 모서리를 찾아 그것을 맞추는 강체 변환을 추정하고, LiDAR 점을 영상에 투영해 검사하며, 카메라의 내부 파라미터를 먼저 보정한다([MathWorks](https://www.mathworks.com/help/lidar/ug/lidar-and-camera-calibration.html)). 결과는 LiDAR 좌표를 카메라 좌표로 보내는 외부 파라미터 $T_{CL}=(R_{CL},t_{CL})$이다([[02-foundations/se3-geometry|8. SE(3) §3]]). 여기서 이것이 고정된 변환 하나인 것은 P2가 멈춰 있기 때문이다. 팔이 움직이면 이것은 마스트에서 P2의 엔코더와 3.5 §5의 손-눈 변환을 거쳐 카메라에 이르는 사슬이 되고, 그 오차도 자세에 따라 바뀐다. 리그에서 LiDAR의 축은 앞·왼쪽·위, 카메라 1의 축은 오른쪽·아래·앞을 가리키고, LiDAR는 $0.30\,\mathrm m$ 위에 있으므로 아래를 향한 카메라 $y$로는 $-0.30$이다.

$$R_{CL}=\begin{pmatrix}0&-1&0\\0&0&-1\\1&0&0\end{pmatrix},\qquad t_{CL}=\begin{pmatrix}0\\-0.30\\0\end{pmatrix}\mathrm m$$

$R_{CL}$의 각 행은 카메라 축이 어느 LiDAR 축과 같은지를 적은 것이기 때문이다. 이를 뒤집으면 $L$은 $p_L=R_{CL}^\top(L-t_{CL})=(2.0,\ -0.5,\ -0.5)\,\mathrm m$, $2.121\,\mathrm m$ 거리, 고도 $-13.6^\circ$로 채널의 $\pm15.5^\circ$ 안에 든다.

> **LiDAR 점의 영상 투영의 정의.** *LiDAR 프레임의 3D 점을 카메라 픽셀로 보내는 사상*이다. 클라우드에 색을 입히고, 영상으로 LiDAR 점에 라벨을 달고, 보정을 검사하는 단계다. 조건 넷. **외부 파라미터** $T_{CL}$을 알고, 그 방향은 LiDAR에서 카메라 쪽이다. 카메라의 **내부 파라미터와 왜곡**을 3.5 §1의 순서(정규화, 왜곡, 그다음 $K$)로 적용한다. 점과 영상이 **같은 순간**을 가리키거나, 그 사이의 운동을 보정한다(§9). 그리고 점이 **카메라에 보여야** 한다. LiDAR는 넘겨다보지만 카메라에게는 가리는 무언가의 뒤에 있으면 안 된다.
>
> $$\lambda\begin{pmatrix}u\\v\\1\end{pmatrix}=K\big(R_{CL}\,p_L+t_{CL}\big)$$
>
> 왜곡을 편 픽셀에 대한 식이고, $p_L$은 LiDAR 프레임의 점, $K$는 카메라 1의 내부 행렬, $\lambda$는 카메라 프레임에서 점의 깊이다. 3.5 §1의 카메라 식에서 세계 프레임 자리에 LiDAR 프레임을 넣은 것이다.
>
> - **예**: $(2.0,\ -0.5,\ -0.5)$의 $L$은 카메라 1이 보는 $(470,\ 300)$에 떨어진다. 왜곡된 원본 영상에서는 3.5의 $(467.86,\ 299.15)$, $2.30$ px 떨어진 자리에 속하므로, 왜곡 단계를 건너뛰면 그만큼, 모서리 쪽에서는 더 많이 어긋난다.
> - **비예**: 가시성 검사 없는 투영. 카메라 1 앞 $1.0\,\mathrm m$, 광축 위의 비계 파이프가 파사드 점 $(0,\ 0,\ 2.0)\,\mathrm m$를 카메라에게서 가린다. $0.30\,\mathrm m$ 위의 LiDAR는 파이프 너머로 그 점을 보고(광선이 파이프 축보다 $0.15\,\mathrm m$ 위를 지난다), 투영은 파사드의 $2.0\,\mathrm m$를 파이프가 $1.0\,\mathrm m$로 찍힌 픽셀 $(320,\ 240)$에 칠한다.
> - **왜 중요한가**: 영상으로 라벨 단 LiDAR 점이나 LiDAR 깊이를 붙인 영상으로 학습하는 파이프라인은 이 사상의 오차를 잡음 아닌 라벨 잡음, 곧 매 프레임 같은 어긋남으로 물려받는다.

**1도가 거리에서 하는 일.** $R_{CL}$에 수직축 둘레 $1^\circ$ 오차를 주면 $L$은 $11.18$ px, $10\,\mathrm m$의 점은 $10.51$ px 움직인다. 둘 다 $f\,\delta\theta=10.47$ px 근처인데, 회전은 모든 광선을 같은 각도만큼 돌리기 때문이다. 밀리미터로는 회전축에서 멀수록 자란다. $L$에서 $36.0\,\mathrm{mm}$(3.5 §3의 손-눈 수치), $10\,\mathrm m$에서 $174.7$이다. $1\,\mathrm{cm}$ 병진 오차는 그 반대다. 모든 거리에서 $1\,\mathrm{cm}$이고, 픽셀로는 $f\delta t/Z$ — $2\,\mathrm m$에서 $3.00$ px, $10$에서 $0.60$ px다.

**건전성 검사.** 날카로운 깊이 경계 — 패널 모서리, 기둥 — 가 있는 장면의 LiDAR 점을 영상에 투영하고, 투영된 경계와 영상의 경계 사이 어긋남을 두 거리에서 잰다. 가까이서나 멀리서나 픽셀 수가 같으면 회전, 거리에 따라 줄면 병진, 베이스의 속도에 따라 변하면 외부 파라미터가 아니라 시간이다(§9). 함정은 움직이면서 검사하는 것이다. 먼저 베이스를 멈추고 해야 시간이 기하로 둔갑하지 못한다.

### 9. 시간: 타임스탬프, 트리거, 시계

*한 문장으로:* 모든 측정은 어느 순간의 위치이고, 그 순간에 오차가 있으면 융합된 점은 그동안 리그가 움직인 거리 $v\,\Delta t$만큼 어긋난다. 융합은 스탬프를 참으로 받으므로 이 오차를 보지 못한다.

**문제.** 영상은 한 구간 동안 찍히고(§2), LiDAR 클라우드는 한 번의 훑기 동안 찍히며(§5), 두 센서는 기하뿐 아니라 시간에서도 맞아야 한다(§8). 센서마다 어떤 시계의 눈금으로 데이터에 스탬프를 찍고, [[04-robotics/state-estimation-slam|3. 상태 추정]]의 융합은 측정을 그 스탬프 시각에 리그가 있던 자리에 놓는다. 핵심: 틀린 스탬프는 틀린 위치이고, 그 크기는 리그가 움직인 거리와 꼭 같다.

**하나뿐인 법칙.** 스탬프가 $\Delta t$ 틀리면 리그는 융합이 생각하는 곳에서 $v\Delta t$ 떨어져 있었다.

$$e=v\,\Delta t$$

$\Delta t$ 동안 리그가 $v\Delta t$를 가기 때문이고, 각속도 $\omega$의 회전은 거리 $R$에서 $\omega\,\Delta t\,R$을 더한다. $0.5\,\mathrm{m/s}$에서 $1$밀리초는 $0.5\,\mathrm{mm}$다. $10\,\mathrm{ms}$면 $5\,\mathrm{mm}$, P6의 $70\,\mathrm{ms}$ 예산이면 $35\,\mathrm{mm}$ — 3.2 §5가 늦게 쓰인 프레임에서 찾은 바로 그 $35\,\mathrm{mm}$다. 파사드에서 $10\,\mathrm{ms}$는 $1.5$ px로, $10\,\mathrm{ms}$ 노출의 블러와 똑같다. 블러는 이 법칙을 노출 시간에 걸쳐 번지게 한 것이다.

> **시간 오프셋의 정의.** **시간 오프셋**(time offset)은 *측정의 스탬프와 그 측정이 가리키는 순간 사이의 부호 있는 오차*, 또는 두 센서 시계 사이의 오차다. 지터가 아니라 시간의 편향이다. 조건 셋. 센서마다 **기준 순간**이 정의되어 있다 — 영상은 노출 중간(롤링 셔터면 행마다의 노출 중간), LiDAR 점은 발사 시각, 레이더 검출은 처프 프레임. 스탬프를 **공통 시계**로, 또는 관계를 아는 시계들로 읽는다. 그리고 $\Delta t$ 동안 리그나 장면이 **움직인다**. 서 있는 리그에서는 어떤 오프셋도 무해하고, 그래서 정지 시험으로는 찾을 수 없다.
>
> $$e=v\,\Delta t\qquad(+\ \omega\,\Delta t\,R\ \text{for a rotation})$$
>
> $v$는 상대 속도, $\Delta t$는 오프셋, $\omega$는 각속도, $R$은 거리다. 틀린 시각에 융합된 점의 오차다.
>
> - **예**: 리그의 영상을 노출 중간이 아니라 판독 끝에 찍는 드라이버는 $t_{\exp}/2$에 판독 시간을 더한 만큼 늦다. 롤링 셔터 모델이 행을 세기 시작하는 첫 행의 노출 중간에서 센 값으로, $10\,\mathrm{ms}$ 노출이면 $5+12=17\,\mathrm{ms}$다. 그렇게 읽히는 카메라는 $0.5\,\mathrm{m/s}$로 가는 P6의 카트에서 $8.5\,\mathrm{mm}$, P6 카메라로 $5.1$ px 어긋나고, 이는 제 잡음 $0.833\,\mathrm{mm}$의 열 배다.
> - **비예**: 알려진 일정한 지연은 오프셋이 아니다. 노출 중간에서 힘까지의 P6 $70\,\mathrm{ms}$는 제어기가 예산에 넣고 예측으로 건너가는 지연이다([[04-robotics/robot-systems-deployment|10. 로봇 시스템 §3]]). 융합을 망치는 것은 스탬프가 틀리게 적는 부분이다.
> - **왜 중요한가**: 필터는 측정을 그 스탬프 시각의 상태와 비교하므로, 오프셋은 $v\Delta t$를 증거처럼 innovation에 넣는다 — 어떤 $R$도 모델링하지 못하는 편향이다(3.2 §1). 그리고 속도와 함께 자라므로, 걸음 속도로 조정한 시스템은 뛰는 속도에서 실패한다.

**영상은 어느 순간인가?** §2의 줄은 노출 중간에 점이 있던 자리를 중심으로 하므로, 영상의 기하가 속하는 순간은 노출 중간이고 P6의 예산도 거기서 시작한다. ROS 영상 메시지는 영상의 획득 시각만 요구하고([`sensor_msgs/Image`](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/Image.msg)) 어느 순간인지는 말하지 않으므로, 드라이버의 스탬프는 가정하지 말고 확인해야 한다. 롤링 셔터는 행마다 제 노출 중간을 주어 위에서 아래까지 $12\,\mathrm{ms}$ 차이가 나고, LiDAR 클라우드의 스탬프 하나는 $L$을 보는 열을 deskewing 전까지 $23.1\,\mathrm{mm}$($6.92$ px) 어긋나게 둔다(§5).

**하드웨어 트리거.** 가장 깔끔한 오프셋은 없는 것이다. 전기 신호 모서리 하나가 모든 노출을 시작시킨다. 머신비전 카메라는 입력선의 상승 모서리에서 영상을 시작할 수 있고, 노출은 기종과 설정이 정하는 마이크로초 단위 지연 뒤에 시작한다([Basler, *Triggered Image Acquisition*](https://docs.baslerweb.com/triggered-image-acquisition), [*Exposure Start Delay*](https://docs.baslerweb.com/exposure-start-delay)). 모르는 값이 아니라 빼면 되는 상수다. KITTI의 카메라는 레이저 스캐너가 앞을 볼 때 그 스캐너가 트리거하므로([KITTI](https://www.cvlibs.net/datasets/kitti/setup.php)), 영상마다 빔이 그 장면을 훑는 순간에 찍힌다. 리그에서의 보상은 정확하다. $0.5\,\mathrm{m/s}$에서 $10\,\mathrm{ms}$ 떨어져 노출되는 두 자유 구동 카메라는 카메라 2를 $5\,\mathrm{mm}$ 더 간 자리에 두어, 기선이 $0.12$가 아니라 $0.125\,\mathrm m$, 시차가 $36$이 아니라 $37.50$ px가 되고 $L$은 $1.920\,\mathrm m$에 놓인다 — $80\,\mathrm{mm}$ 짧고, §3의 잡음의 두 배이며, 늘 한쪽으로 쏠린다. 공유 트리거가 이를 0으로 만든다.

**장치 사이의 시계.** 다른 컴퓨터에 있거나 자유 구동하는 센서들은 시계를 맞춰야 한다. 정밀 시간 프로토콜(PTP, IEEE 1588)은 네트워크 장치들을 그중 가장 좋은 시계에 맞춰, 각 로컬 시계를 마스터의 시각으로 옮기고 주파수도 맞춘다([Basler, *PTP*](https://docs.baslerweb.com/precision-time-protocol)). 핵심은 스탬프 넷의 교환이다. 마스터가 $t_1$(마스터 시각)에 Sync를 보내고, 슬레이브가 $t_2$(슬레이브 시각)에 받고, $t_3$에 Delay_Req를 보내고, 마스터가 $t_4$에 받는다. 슬레이브가 $\theta$만큼 앞서고 편도 지연이 양방향 모두 $d$이면 $t_2-t_1=d+\theta$, $t_4-t_3=d-\theta$이므로

$$\hat\theta=\frac{(t_2-t_1)-(t_4-t_3)}{2},\qquad \hat d=\frac{(t_2-t_1)+(t_4-t_3)}{2}$$

차는 지연을, 합은 오프셋을 지우기 때문이다. 함정은 "양방향 모두 $d$"에 숨은 가정이다. 두 방향이 다르면 $\hat\theta$는 그 차이의 절반만큼 틀린다([Nokia](https://documentation.nokia.com/html/0_add-h-f/93-0267-HTML/7X50_Advanced_Configuration_Guide/ACG-%20IEEE-1588-FP-TD.html)). §10에서 경로가 $80$과 $20\,\mathrm{\mu s}$면 $30\,\mathrm{\mu s}$이고, $0.5\,\mathrm{m/s}$에서는 해가 없다. NTP 형태의 같은 스탬프 넷 교환, 그것을 나르는 네트워크, 그것을 확인하는 셸 명령은 [[02-foundations/tools/computer-networks|12.5 컴퓨터 네트워크 §10]]과 [[02-foundations/tools/linux-shell|12.1 §11]]이다.

> [!note]- 더 깊이 · Deeper
> **얼마나 좋은가, 어떻게 어긋나는가.** NIST의 2004년 IEEE 1588 학술대회에 보고된 시연들은 장치들을 마이크로초 미만으로 맞췄다([NIST](https://www.nist.gov/publications/standard-precision-clock-synchronization-protocol-networked-measurement-and-control)). 실제 네트워크가 얼마나 해내는지는 그 하드웨어와 구성에 달렸다(Basler). 비대칭은 NTP 방식 동기화도 제한한다. chrony 프로젝트는 나노초까지 안정되게 잰 오프셋도 비대칭 지연 때문에 밀리초만큼 틀릴 수 있다고 적는다([chrony FAQ](https://chrony-project.org/faq.html)). 시계는 흘러가기도 한다. $50$ ppm 차이 나는 두 자유 구동 시계는 10분에 $30\,\mathrm{ms}$ 벌어지고, $0.5\,\mathrm{m/s}$에서 $15\,\mathrm{mm}$다. 그래서 동기화는 시작할 때 한 번이 아니라 계속 돈다. 로봇 자신의 컴퓨터에 대한 ROS 2 트랙의 조언은 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]에 있다.

**융합이 이것을 가정하는 이유.** [[04-robotics/state-estimation-slam|3. 상태 추정 §8]]은 보정, 타임스탬프, 롤링 셔터, 지연, 시계 오프셋을 알고리즘의 이득을 좌우할 수 있는 세부 사항으로 꼽고, 그 필터들은 모든 스탬프를 참으로 받는다. 추정기는 일정한 오프셋을 상태로 들고 갈 수 있지만 — 3.5 §5의 시간 보정은 운동 신호의 상관으로 한다 — 예산은 과제에서 온다. S1은 베이스에 $2\,\mathrm{mm}$를 준다([[05-construction-robotics/site-engineering|2.5 §2]]). $0.5\,\mathrm{m/s}$에서 그것은 리그 전체에 설명되지 않은 시간 $4\,\mathrm{ms}$다. 리그의 시간을 그만큼 알든가, 구멍을 재기 전에 베이스를 멈추든가다.

### 대상으로 한 번 끝까지 · Worked case

베이스가 S1의 파사드를 따라 $v=0.5\,\mathrm{m/s}$로, 파사드에서 $Z=2.0\,\mathrm m$ 떨어져 굴러가고, 리그의 모든 센서가 $L$을 본다. 센서마다 한 단계, 시간에 한 단계, 모두 다섯 단계를 밟은 뒤 S1의 $\pm5\,\mathrm{mm}$에 대한 장부를 적는다. 모든 숫자는 고정된 리그 위의 교과 계산이고, §10이 하나하나 출력한다.

**1단계 — 카메라.** 블러는 $b=f\,v\,t_{\exp}/Z$다(§2). 실내의 $t_{\exp}=10\,\mathrm{ms}$에서 $b=600\times0.5\times0.010/2=1.50$ px, $5.0\,\mathrm{mm}$의 줄이다. 그늘은 $S=200\times10=2{,}000\ e^-$(SNR $44.3$, §1)를 모으고 햇빛 쪽은 우물의 두 배인 $20{,}000$을 모으므로 하얗게 날아간다. $t_{\exp}=2\,\mathrm{ms}$에서는 $b=0.30$ px($1.0\,\mathrm{mm}$), 그늘 $400\ e^-$에 SNR $19.2$, 해 $4{,}000\ e^-$에 SNR $63.0$이다. 롤링 셔터는 어느 노출에서나 프레임을 $f\,v\,(480\,t_{\text{row}})/Z=600\times0.5\times0.012/2=1.80$ px, 위에서 아래까지 $6.0\,\mathrm{mm}$ 비튼다. 짧은 노출은 그늘의 SNR을 절반 넘게 내주고($44.3$ 대신 $19.2$) 선명하고 포화 없는 파사드를 사며, 스큐는 그대로 남는다.

**2단계 — 스테레오.** 영상마다 $\sigma_u=0.5$ px면 $\sigma_d=\sqrt2\times0.5=0.707$ px, 광선 방향으로 $\sigma_Z=Z^2\sigma_d/(fb)=4\times0.707/72=39.3\,\mathrm{mm}$다(§3). 광선을 가로질러서는 $Z\sigma_u/f=1.67\,\mathrm{mm}$다. $10\,\mathrm{ms}$ 떨어져 노출되면 쌍은 $b=0.12+0.5\times0.010=0.125\,\mathrm m$처럼 굴어 시차를 $600\times0.125/2=37.50$ px로 읽고 $L$을 $72/37.5=1.920\,\mathrm m$에 놓는다. $80\,\mathrm{mm}$ 짧고, 잡음의 두 배이며, 늘 한쪽이다(§9).

**3단계 — LiDAR.** 링을 따라 간격 $R\Delta\phi=2\times0.00349=7.0\,\mathrm{mm}$, 링 사이 $R\Delta\varepsilon=34.9\,\mathrm{mm}$, 점 크기 $w_0+\theta R=10+3\times2=16\,\mathrm{mm}$, $4{,}104$점/m², 빔마다 $\sigma_L=20\,\mathrm{mm}$다(§5). 거리 오차는 여기서 스테레오의 절반, $4\,\mathrm m$에서는 팔분의 일이지만($157$ 대 $20\,\mathrm{mm}$. $1.43\,\mathrm m$에서 같다), 링 간격은 카메라의 $3.3\,\mathrm{mm}$ 픽셀보다 열 배 넓다. $L$을 보는 열은 클라우드 스탬프보다 $46.1\,\mathrm{ms}$ 뒤에 쏜다. 스탬프 시각으로 융합하면 $L$은 $0.5\times46.1=23.1\,\mathrm{mm}$, 카메라 1에서 $6.92$ px 어긋나고, 제 시각으로 deskewing하면 오차가 사라진다.

**4단계 — 레이더.** 거리 셀 $c/(2B)=14.99\,\mathrm{cm}$, 각도 셀 $2/12\ \mathrm{rad}=9.55^\circ$로 파사드에서 폭 $0.33\,\mathrm m$다(§6). 파사드 앞 $0.30\,\mathrm m$의 작업자는 파사드에서 거리 셀 둘 떨어져 있고 §10이 시도한 모든 위상에서 갈린다. $1.6\,\mathrm{m/s}$로 리그 쪽으로 걸으면 처프마다 메아리 위상을 $4\pi\times1.6\times50\,\mathrm{\mu s}/3.893\,\mathrm{mm}=0.258\,\mathrm{rad}$ 돌려, 정지한 파사드에서 $1.6/0.304=5.26$ 속도 셀 떨어진다. 이 중 어느 것도 $L$을 놓지 못한다. $L$은 깊이 $150\,\mathrm{mm}$, 폭 $333\,\mathrm{mm}$인 셀 어딘가에 있다.

**5단계 — 시간.** $0.5\,\mathrm{m/s}$에서 스탬프 오차 $1$밀리초는 $0.5\,\mathrm{mm}$다. 판독 끝에 찍힌 카메라는 $5+12=17\,\mathrm{ms}$ 늦어 $8.5\,\mathrm{mm}$다(§9). S1은 예산에서 베이스에 $2\,\mathrm{mm}$를 준다. 리그 전체에 $2/0.5=4\,\mathrm{ms}$다.

**장부.** 파사드에서의 오차와 그것을 없애는 것:

| 파사드에서의 오차 | 크기 | 없애는 것 |
|---|---:|---|
| 카메라, 광선을 가로지르는 특징 하나($\sigma_u=0.5$ px) | $1.67\,\mathrm{mm}$ | 더 가까운 카메라, 또는 더 많은 픽셀 |
| $10\,\mathrm{ms}$ / $2\,\mathrm{ms}$의 블러 | $5.0$ / $1.0\,\mathrm{mm}$ | 짧은 노출, 스트로브(§2) |
| 프레임 전체의 롤링 셔터 스큐 | $6.0\,\mathrm{mm}$ | 글로벌 셔터나 스트로브(§2) |
| 광선 방향 스테레오 깊이 | $39.3\,\mathrm{mm}$ | 넓은 기선이나 짧은 거리(§3) |
| $10\,\mathrm{ms}$ 떨어진 스테레오 쌍 | $80\,\mathrm{mm}$ 편향 | 공유 트리거(§9) |
| LiDAR 잡음 / 점 / 링 간격 | $20$ / $16$ / $35\,\mathrm{mm}$ | 없음. 접근에 쓴다(§5) |
| 클라우드 스탬프로 융합한 LiDAR 열 | $23.1\,\mathrm{mm}$ | 열 시각으로 deskewing(§5, §9) |
| 레이더 셀 | $150\times333\,\mathrm{mm}$ | 없음. 사람에게 쓴다(§6) |
| 판독 끝에 찍힌 카메라 스탬프 | $8.5\,\mathrm{mm}$ | 노출 중간 스탬프(§9) |

스스로 S1의 허용오차 안에 드는 측정은 하나뿐이다. 광선을 가로지르는 카메라 위치 $1.67\,\mathrm{mm}$ — 그것도 $2\,\mathrm{ms}$ 노출의 $1.0\,\mathrm{mm}$ 블러, 참 스탬프, $4\,\mathrm{ms}$ 시간 예산을 갖출 때에만 그 안에 머문다. 다른 센서들은 카메라가 못하는 것을 보태지만, 그중 어느 것도 구멍의 위치는 아니다. §7의 분업에 숫자가 붙은 것이다.

### 10. 실습: 센서별로 본 리그의 오차

영어 절의 코드는 고정된 리그 위에서 §1–§9를 절마다 번호 붙은 한 부분씩 돌리고, 계산 절이 쓴 숫자를 모두 출력한다. 식을 넘어서는 부분은 둘이다. 3부는 1차 스테레오 법칙을 $200{,}000$개 모의 시차로 검사하고, 6부는 대역폭 다섯에 대해 상대 위상 $36$개씩으로 처프 하나의 스펙트럼에서 두 레이더 메아리를 가른다. 시간을 재는 곳이 없고 무작위 추출 하나는 시드를 고정했으므로, 어느 기계에서나 출력이 같다. 출력의 핵심 값:

| 부분 | 출력 |
|---|---|
| 1. 픽셀 | 동적 범위 $2{,}000$($66.0\,\mathrm{dB}$), 변환기 포함 $1{,}732$($64.8\,\mathrm{dB}$). 그늘 SNR: $0.5$/$1$/$2$/$5$/$10$/$20\,\mathrm{ms}$에서 $8.7$/$13.1$/$19.2$/$31.1$/$44.3$/$63.0$. 해는 $5\,\mathrm{ms}$부터 포화, 글린트는 늘 포화. 창: $0.632$에서 $3.333\,\mathrm{ms}$, 해는 $5.0\,\mathrm{ms}$까지 |
| 2. 블러와 스큐 | $0.5\,\mathrm{m/s}$에서 $1$/$2$/$5$/$10$/$20\,\mathrm{ms}$에 $0.15$/$0.30$/$0.75$/$1.50$/$3.00$ px, 스큐 $1.80$ px($6.0\,\mathrm{mm}$). $1.0\,\mathrm{m/s}$에서 $2\,\mathrm{ms}$는 $0.60$ px |
| 3. 스테레오 | $b=0.12$에서 $\sigma_Z$: $1$/$2$/$4$/$8\,\mathrm m$에 $9.8$/$39.3$/$157.1$/$628.5\,\mathrm{mm}$. 모의 표준편차 $9.8$/$39.3$/$158.0$/$644.3$, 편향 $+0.1$/$+0.7$/$+6.0$/$+49.4\,\mathrm{mm}$. LiDAR와 $1.43\,\mathrm m$에서 같음. $10\,\mathrm{ms}$ 떨어진 쌍: $1.9200\,\mathrm m$($-80.0\,\mathrm{mm}$) |
| 4. 비행시간 | $1\,\mathrm{ns}=0.1499\,\mathrm m$. $100$/$80$/$20\,\mathrm{MHz}$: 유일 거리 $1.499$/$1.874$/$7.495\,\mathrm m$, 파사드 판독 $0.501$/$0.126$/$2.000\,\mathrm m$. 둘을 함께: $7.495\,\mathrm m$까지 유일, $2.000\,\mathrm m$에서 일치 |
| 5. LiDAR | $2$/$10$/$50\,\mathrm m$에서 간격 $7.0\times34.9$/$34.9\times174.5$/$174.5\times872.7\,\mathrm{mm}$, 점 $16.0$/$40.0$/$160.0\,\mathrm{mm}$, $4{,}104$/$164$/$7$점/m². $120^\circ$ 훑기 $33.3\,\mathrm{ms}$, $16.7\,\mathrm{mm}$ |
| 6. 레이더 | $0.25$/$0.5$/$1$/$2$/$4\,\mathrm{GHz}$: 셀 $60.0$/$30.0$/$15.0$/$7.5$/$3.7\,\mathrm{cm}$, 작업자와 파사드 분리 $0$/$13$/$36$/$36$/$36$(36 중). 위상 걸음 $-0.2582\,\mathrm{rad}$에서 $-1.600\,\mathrm{m/s}$, $v_{\text{res}}=0.304$, $v_{\max}=19.47\,\mathrm{m/s}$, 각도 셀 $9.55^\circ$ |
| 7. 시간 | $0.5\,\mathrm{m/s}$에서 $1$/$10$/$70\,\mathrm{ms}$에 $0.50$/$5.00$/$35.00\,\mathrm{mm}$. 판독 끝 스탬프 $17\,\mathrm{ms}$ → $8.5\,\mathrm{mm}$. PTP: 대칭 경로 오차 $0.0$, $80/20\,\mathrm{\mu s}$에서 $30.0\,\mathrm{\mu s}$. $50$ ppm 표류 10분 $30\,\mathrm{ms}$ → $15\,\mathrm{mm}$ |
| 8. LiDAR에서 영상으로 | $L$ → $(470,\ 300)$. $1^\circ$: $2\,\mathrm m$에서 $11.18$ px($36.0\,\mathrm{mm}$), $10\,\mathrm m$에서 $10.51$ px($174.7\,\mathrm{mm}$). $1\,\mathrm{cm}$: $3.00$과 $0.60$ px. $L$의 열: $46.1\,\mathrm{ms}$, $23.1\,\mathrm{mm}$, $6.92$ px |

**출력이 말하는 것.**
- **노출은 창이고, 속도가 그것을 닫는다.** 그늘이 SNR $10$을 내려면 $0.632\,\mathrm{ms}$가 필요하고, 반 픽셀 블러는 $0.5\,\mathrm{m/s}$에서 $3.333\,\mathrm{ms}$까지 허락하며, $1.0\,\mathrm{m/s}$ 행은 $2\,\mathrm{ms}$ 노출이 벌써 $0.60$ px임을 보여 준다. 글린트는 어느 창에도 없다. 장면 $80\,\mathrm{dB}$ 대 센서 $66$.
- **스테레오의 오차는 제곱 법칙이고 LiDAR는 평평하다.** $1.43\,\mathrm m$에서 교차하고, $8\,\mathrm m$에서 스테레오는 $31$배 나쁘며 볼록성 때문에 $+49.4\,\mathrm{mm}$ 치우친다. 편향은 1차 법칙이 아니라 시뮬레이션이 보여 준다.
- **LiDAR의 밀도는 $1/R^2$로 떨어지고 점은 $R$로 커진다.** $20\,\mathrm m$에서 점 크기와 열 간격이 둘 다 $70\,\mathrm{mm}$이고, $50\,\mathrm m$에서는 링을 따라 점이 더는 닿지 않는다.
- **거리 분해능은 문턱이지 보증이 아니다.** 한 셀 떨어진 두 메아리는 $36$개 위상 중 $13$개에서, 두 셀 떨어지면 모두에서 갈린다. 셀을 움직이는 것은 대역폭뿐이다.
- **모든 시간 오류는 $v\,\Delta t$다.** 늦은 카메라 스탬프, 클라우드의 스탬프 하나, 자유 구동 쌍, 흘러가는 시계는 원인은 넷이어도 같은 밀리초당 $0.5\,\mathrm{mm}$다.

### 11. 이 페이지가 다루지 않는 것

현장 로봇이 함께 실을 수 있는 센서들: 열화상 카메라와 이벤트 카메라, 초음파 거리계, GNSS([[04-robotics/state-estimation-slam|3 §8]]), IMU([[04-robotics/sensor-models|3.2]]), 촉각([[04-robotics/tactile-visuotactile|14]]). 3.5의 왜곡 모델을 넘는 렌즈 설계, 색과 디모자이킹, 자동 노출 알고리즘, FFT 하나를 넘는 레이더 처리, 포인트 클라우드를 받은 뒤의 일(3.5 §3–§4, [[05-construction-robotics/site-perception|5. 현장 인식]]). 스탬프 붙은 변환, 드라이버, 그 데이터를 나르는 네트워크는 ROS 2 트랙의 몫이다(프레임과 스탬프는 [[04-robotics/ros2/describing-a-robot|25.6]], 드라이버와 네트워크는 [[04-robotics/ros2/from-simulation-to-hardware|25.11]]).

### 읽고 나면

다음을 할 수 있어야 한다.

- 장면의 빛을 F수와 노출로 광전자로, 전자를 SNR로 바꾸고, 장면의 밝기 비를 dB로 보고 한 번의 노출이 그것을 담을 수 있는지 말한다.
- 모션 블러와 롤링 셔터 스큐를 계산하고, 움직이는 리그의 노출 창을 찾는다.
- $\sigma_d=\sqrt2\,\sigma_u$로 $\sigma_Z=Z^2\sigma_d/(fb)$를 유도하고, 스테레오와 LiDAR가 교차하는 거리를 찾는다.
- 비행시간의 지연이나 위상을 거리로 바꾸고, 두 주파수로 감긴 위상을 푼다.
- 한 거리에서 LiDAR의 간격, 점 크기, 밀도를 계산하고, 먼지·비·어두운 면·유리가 무엇을 하는지 말한다.
- FMCW 레이더의 비트, 거리 셀, 속도 셀, 각도 셀을 유도하고, 무엇을 가를 수 있고 없는지 말한다.
- LiDAR 점을 영상에 투영하고, 어긋남이 어떻게 변하는지로 회전·병진·시간을 가른다.
- 어떤 틀린 스탬프든 $v\,\Delta t$로 값을 매기고, PTP 스탬프 넷으로 시계 오프셋을 추정하고, 비대칭 경로가 무엇을 하는지 말한다.
- 현장 리그의 센서마다 제 물리가 허락하는 일을 맡긴다.

### 스스로 점검

1. 베이스가 $1.0\,\mathrm{m/s}$로 움직이는데 리그의 카메라가 $5\,\mathrm{ms}$로 돈다. 그늘의 SNR, $2\,\mathrm m$에서의 블러, 햇빛 쪽 절반의 상태는?
2. 누군가 고정된 노출에서 어두운 장면을 밝히려고 아날로그 게인을 두 배로 올린다. 샷 잡음 한계의 SNR과 동적 범위는 어떻게 되는가?
3. 스테레오 기선을 반으로 줄이면 깊이 오차가 두 배가 되는데, 거리를 두 배로 하면 왜 네 배가 되는가?
4. $100\,\mathrm{MHz}$ 비행시간 카메라가 약 $2\,\mathrm m$ 떨어진 줄 아는 파사드를 $0.50\,\mathrm m$로 읽는다. 무슨 일이 일어났고, 어떻게 잡아내겠는가?
5. 작업자가 파사드 앞 $10\,\mathrm{cm}$에 서 있는데 레이더는 물체 하나만 보여 준다. 무엇이 둘을 가르고, 무엇이 가르지 못하는가?
6. 투영된 LiDAR 경계가 $3\,\mathrm m$에서도 $12\,\mathrm m$에서도 영상 경계보다 $10$ px 오른쪽에 있다. 회전인가, 병진인가, 시간인가 — 어떻게 확인하는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. 그늘은 $200\times5=1{,}000\ e^-$로 SNR $31.1$, 블러는 $600\times1.0\times0.005/2=1.5$ px, 해는 $2{,}000\times5=10{,}000\ e^-$로 정확히 풀 웰이라 포화한다. $1.0\,\mathrm{m/s}$에서의 창은 그늘의 $0.632\,\mathrm{ms}$(SNR은 속도와 무관하므로 그대로)에서 반 픽셀 블러의 $0.5\times2/(600\times1.0)=1.67\,\mathrm{ms}$까지이므로, $5\,\mathrm{ms}$는 두 번 벗어난다.
> 2. SNR은 그대로다. 게인은 모인 전자와 그 잡음을 함께 곱할 뿐 광자를 더하지 않는다. 동적 범위는 준다. 변환기의 전체 눈금이 절반의 전자, $5{,}115$개에 해당하게 되는데 바닥은 거의 움직이지 않기 때문이다. $983$, 곧 $64.8$ 대신 $59.9\,\mathrm{dB}$다(§1 더 깊이는 $\times4$를 계산한다: $54.1\,\mathrm{dB}$).
> 3. $\sigma_Z=Z^2\sigma_d/(fb)$에서 기선은 한 번 들어가므로 반으로 줄이면 오차가 두 배다. 거리는 제곱으로 들어간다. 시차 자체가 $1/Z$로 줄어드는 것이 한 번, 시차 1픽셀의 깊이 값이 $Z$와 함께 커지는 것이 또 한 번이다. $|dZ/dd|=Z^2/(fb)$.
> 4. 위상이 감겼다. $100\,\mathrm{MHz}$에서 거리는 $1.499\,\mathrm m$까지만 유일하고 $2.0-1.499=0.501\,\mathrm m$다. 두 번째 주파수가 잡는다($80\,\mathrm{MHz}$에서는 $0.126\,\mathrm m$로 읽히고, 둘 다에 맞는 것은 $2.000\,\mathrm m$뿐이다). 사전 정보, 스테레오 쌍, LiDAR 같은 독립적인 거리도 잡는다.
> 5. $10\,\mathrm{cm}$는 $15\,\mathrm{cm}$ 셀의 삼분의 이라서 $1\,\mathrm{GHz}$의 거리로는 갈리지 않는다. $4\,\mathrm{GHz}$라면 갈린다($3.75\,\mathrm{cm}$ 셀, 거의 셋 떨어짐). 레이더 쪽으로 걸으면 도플러가 한 프레임에 가르고, 서 있으면 가르지 못하며, $2\,\mathrm m$에서 $0.33\,\mathrm m$인 각도 셀은 같은 방향의 두 물체를 가르지 못한다.
> 6. 가까이서나 멀리서나 픽셀이 같으면 회전이다. $10$ px는 대략 $f\,\delta\theta$이므로 $\delta\theta\approx10/600\ \mathrm{rad}=0.95^\circ$다. 병진이라면 $3$에서 $12\,\mathrm m$로 가며 넷으로 줄었을 것이다. 베이스를 멈춰 시간 오프셋이 끼지 못하게 하고, 어긋남이 속도에 따라 변하지 않는지 확인한다.

### 과제 · Problem set

Tier A. 이 페이지와 선수 지식, 장치 카탈로그만 쓴다. 계산 절은 $2\,\mathrm m$ 떨어진 파사드를 $0.5\,\mathrm{m/s}$로 지나가는 리그를 돌렸다. 이 과제는 숫자 일곱을 바꾸고 나머지는 그대로 둔다. 베이스는 $1.0\,\mathrm{m/s}$, 파사드는 $4.0\,\mathrm m$, 스테레오 기선은 $0.24\,\mathrm m$, 노출은 $2\,\mathrm{ms}$, LiDAR는 초당 점 수를 유지한 채 $20\,\mathrm{Hz}$로 돌아 열 간격이 $0.4^\circ$다. 레이더는 처프 $256$개로 $4\,\mathrm{GHz}$를 쓴다.

1. **그리기.** 변형의 그림. $4\,\mathrm m$의 파사드와 그 위 한 점으로 가는 광선 위의 스테레오 오차 막대, 그 자리의 레이더 셀, 시간과 번짐을 적은 LiDAR의 $120^\circ$ 훑기가 있는 평면도, 그리고 그 점 주변의 카메라 픽셀, LiDAR 점과 링, $2\,\mathrm{ms}$ 블러, 판독 끝 스탬프의 오차, S1의 $\pm5\,\mathrm{mm}$를 모두 한 축척으로 그린 파사드 조각.
2. **유도.** (a) $Z=fb/d$와 각 영상의 독립 오차 $\sigma_u$에서 $\sigma_Z=\sqrt2\,Z^2\sigma_u/(fb)$를 유도하라. $4\,\mathrm m$에서 $b=0.12$와 $0.24\,\mathrm m$로 계산하고, 넓은 쌍이 LiDAR의 $20\,\mathrm{mm}$와 같아지는 거리와 $128$ px 탐색의 가까운 쪽 한계를 구하라. (b) $1.0\,\mathrm{m/s}$, $4\,\mathrm m$, $2\,\mathrm{ms}$의 블러와 스큐를 픽셀과 밀리미터로 구하고, 픽셀 값이 계산 절의 짧은 노출 값과 같은 이유를 말하라. (c) $20\,\mathrm{Hz}$ LiDAR의 $4\,\mathrm m$ 간격, 점 크기, 밀도, 그리고 $120^\circ$ 훑기의 시간과 번짐. (d) $T_c=50\,\mathrm{\mu s}$에서 $4\,\mathrm{GHz}$ 레이더의 거리 셀, 기울기, $4\,\mathrm m$의 비트, $5\,\mathrm{MHz}$ IF 대역의 도달 거리, 처프 $256$개의 속도 셀. (e) §4의 ToF 카메라를 $4\,\mathrm m$에서: 주파수마다 감긴 판독과 둘이 동의하는 거리. (f) $2\,\mathrm{ms}$ 노출에서 판독 끝에 찍힌 카메라는 얼마나 늦고, $1.0\,\mathrm{m/s}$에서 몇 mm, $4\,\mathrm m$에서 몇 px 어긋나는가. 그리고 경로가 $90$과 $10\,\mathrm{\mu s}$일 때 PTP 오프셋의 오차.
3. **실행.** 영어 절 템플릿의 `?` — 각각 주석이 이름 붙인 식이다 — 를 채우고 변형을 돌려라. 출력된 숫자를 계산 절의 숫자 옆에 놓고, 변형이 어떤 오차를 나쁘게, 어떤 오차를 좋게, 어떤 오차를 픽셀로는 그대로 두었는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - **패널 둘, 각자 축척 하나와 축척 막대**: 평면도는 미터, 파사드 조각은 밀리미터로. 모든 길이는 계산하고, 눈대중으로 그리지 않는다.
> - **스테레오 오차는 광선 방향**이다. 깊이에서 광선 길이로 늘려 그리고, 파사드 방향으로 그리지 않는다.
> - **레이더 셀은 쐐기**다. 깊이는 어느 거리에서나 $c/(2B)$, 폭은 각도 셀 곱하기 거리 — $4\,\mathrm m$에서 $2$에서보다 두 배 넓고 깊이는 같다.
> - **LiDAR 점과 링은 기하에서**: 점은 $w_0+\theta R$, 열은 $R\Delta\phi$, 링은 $R\Delta\varepsilon$ 간격. 점이 겹치는지, 링 사이에 벽이 얼마나 남는지 보여 준다.
> - **블러와 모든 스탬프 오차는 파사드 위의 길이**, 곧 $v\,\Delta t$다. 운동 방향으로 그리고 시간을 적어, S1의 $\pm5\,\mathrm{mm}$ 원 옆에 둔다.

> [!tip]- 정답 · Solutions
> 1. $4\,\mathrm m$, $b=0.24$에서 스테레오 막대는 깊이로 $\pm78.6\,\mathrm{mm}$, 레이더 셀은 깊이 $3.75\,\mathrm{cm}$에 폭 $0.67\,\mathrm m$다. 훑기는 $120^\circ$를 $16.7\,\mathrm{ms}$에 가로질러 파사드를 $16.7\,\mathrm{mm}$ 번지게 한다. 앞과 같다 — 시간은 반, 속도는 두 배. 조각 위에서 카메라 픽셀 하나가 $6.67\,\mathrm{mm}$라 S1의 원은 지름이 두 픽셀이 안 되고, LiDAR의 $22\,\mathrm{mm}$ 점은 링을 따라 $27.9\,\mathrm{mm}$, 링 사이 $69.8\,\mathrm{mm}$ 간격이라 더는 겹치지 않는다. 블러는 $2\,\mathrm{mm}$, 늦은 스탬프는 $13\,\mathrm{mm}$다.
> 2. (a) 독립 오차의 $d=u_1-u_2$는 $\sigma_d^2=2\sigma_u^2$를 준다. $Z=fb/d$를 선형화하면 $|dZ/dd|=fb/d^2=Z^2/(fb)$이므로 $\sigma_Z=\sqrt2\,Z^2\sigma_u/(fb)$다. $4\,\mathrm m$에서 $b=0.12$는 $157.1\,\mathrm{mm}$, $0.24$는 $78.6\,\mathrm{mm}$. $20\,\mathrm{mm}$와 같은 거리는 $\sqrt{0.020\times600\times0.24/0.707}=2.02\,\mathrm m$, 가까운 쪽 한계는 $600\times0.24/128=1.125\,\mathrm m$다. (b) 블러 $600\times1.0\times0.002/4=0.30$ px, $2.0\,\mathrm{mm}$. 스큐 $600\times1.0\times0.012/4=1.80$ px, $12.0\,\mathrm{mm}$. 픽셀로는 둘 다 $v/Z$에만 달렸고 $1.0/4=0.5/2$이며, 밀리미터로는 속도와 함께 두 배가 되었다. (c) $27.9\times69.8\,\mathrm{mm}$, 점 $10+3\times4=22\,\mathrm{mm}$, $1/(0.0279\times0.0698)=513$점/m². $20\,\mathrm{Hz}$에서 $120^\circ$는 $16.7\,\mathrm{ms}$, $1.0\,\mathrm{m/s}$에서 $16.7\,\mathrm{mm}$. (d) $c/(2B)=3.75\,\mathrm{cm}$, $S=80\,\mathrm{MHz/\mu s}$, $f_b=2SR/c=2.135\,\mathrm{MHz}$, 도달 $5\,\mathrm{MHz}\times c/(2S)=9.37\,\mathrm m$ — 같은 시간에 네 배를 쓸면 도달이 사분의 일이 된다. $v_{\text{res}}=\lambda/(2\times256\times50\,\mathrm{\mu s})=0.152\,\mathrm{m/s}$. (e) $100\,\mathrm{MHz}$에서 $4.0-2\times1.499=1.002\,\mathrm m$, $80$에서 $4.0-2\times1.874=0.253\,\mathrm m$. $7.495\,\mathrm m$ 안에서는 $4.000\,\mathrm m$에서만 맞는다. (f) $1+12=13\,\mathrm{ms}$ 늦어 $13\,\mathrm{mm}$, $600\times0.013/4=1.95$ px. PTP 오프셋은 $(90-10)/2=40\,\mathrm{\mu s}$ 틀린다.
> 3. 빈칸: `F * v * t_s / z`, `z**2 * sigma_d / (F * b)`, `r * np.radians(step_deg) * 1e3`, `(w0 + div * r) * 1e3`, `C / (2 * B)`, `C / fc / (2 * chirps * Tc)`, `((t2 - t1) - (t4 - t3)) / 2, ((t2 - t1) + (t4 - t3)) / 2`. 출력은 영어 절의 정답 3과 같다. 블러 $0.30$ px와 스큐 $1.80$ px, $4\,\mathrm m$의 $\sigma_Z$가 $157.1$과 $78.6\,\mathrm{mm}$, LiDAR $27.9\times69.8\,\mathrm{mm}$에 점 $22.0\,\mathrm{mm}$와 훑기 $16.7\,\mathrm{ms}$ → $16.7\,\mathrm{mm}$, 레이더 셀 $14.99$와 $3.75\,\mathrm{cm}$에 $v_{\text{res}}$ $0.152\,\mathrm{m/s}$, 늦은 스탬프 $13\,\mathrm{ms}$ → $13.0\,\mathrm{mm}$, $1.95$ px, PTP 오프셋 $3040.0\,\mathrm{\mu s}$와 오차 $40.0\,\mathrm{\mu s}$. 나빠진 것: 늦은 스탬프($8.5\to13.0\,\mathrm{mm}$), LiDAR 간격과 점($7.0\times34.9\to27.9\times69.8\,\mathrm{mm}$, $16\to22\,\mathrm{mm}$), 기선을 두 배로 해도 새 거리의 스테레오($39.3\to78.6\,\mathrm{mm}$). 좋아진 것: 레이더의 거리 셀과 속도 셀($15.0\to3.75\,\mathrm{cm}$, $0.304\to0.152\,\mathrm{m/s}$), 도달 거리를 대가로($37.5\to9.37\,\mathrm m$). 픽셀로 그대로인 것: 블러($0.30$ px)와 스큐($1.80$ px). $v/Z$가 그대로이기 때문이고, 밀리미터로는 둘 다 두 배가 되었다.

### 출처

- NIST, 광속 — [physics.nist.gov](https://physics.nist.gov/cgi-bin/cuu/Value?c) — 정의상 정확한 $c$
- OpenStax, *College Physics 2e* §26.4 — [openstax.org](https://openstax.org/books/college-physics-2e/pages/26-4-microscopes) — F수가 상의 단위 면적에 닿는 빛을 정한다
- Hamamatsu Learning Center, CCD 신호 대 잡음비 — [hamamatsu.magnet.fsu.edu](https://hamamatsu.magnet.fsu.edu/articles/ccdsnr.html) — 잡음원, SNR 식, 풀 웰 나누기 읽기 잡음, $5$–$9\,^\circ\mathrm C$마다 절반이 되는 암전류
- Andor, CCD·EMCCD·sCMOS의 감도와 잡음 — [andor.oxinst.com](https://andor.oxinst.com/learning/view/article/sensitivity-and-noise-of-ccd-emccd-and-scmos-sensors) — CMOS에도 같은 잡음원
- Basler 문서: 셔터 종류, HDR, 트리거, 노출 시작 지연, PTP — [docs.baslerweb.com](https://docs.baslerweb.com/electronic-shutter-types) — 행 시간과 플래시 창, 합친 노출, 트리거와 그 고정 지연, PTP
- Keselman 등, "Intel RealSense Stereoscopic Depth Cameras," CCD 2017(CVPR 워크숍) — [arXiv:1705.05548](https://arxiv.org/abs/1705.05548) — $Z^2$ 깊이 오차 법칙, 프로젝터의 무늬, 어둠과 한낮
- Microsoft Learn, Azure Kinect DK 깊이 카메라 — [learn.microsoft.com](https://learn.microsoft.com/en-us/previous-versions/azure/kinect-dk/depth-camera) — 진폭 변조 비행시간, 무효 픽셀, 모서리의 다중 경로
- Baek 등, "Centimeter-Wave Free-Space Time-of-Flight Imaging," 2021 프리프린트 — [arXiv:2105.11606](https://arxiv.org/abs/2105.11606) — 위상과 거리의 관계
- Zollhöfer, "Commodity RGB-D Sensors: Data Acquisition," 2019 단행본 장 — [arXiv:1902.06835](https://arxiv.org/abs/1902.06835) — 떠다니는 픽셀, 햇빛, 역카메라인 프로젝터, 간섭
- Geng, "Structured-light 3D surface imaging: a tutorial," *Adv. Opt. Photon.* 3(2), 2011 — [doi:10.1364/AOP.3.000128](https://doi.org/10.1364/AOP.3.000128) — 구조광 계열
- NOAA, "What is lidar?" — [oceanservice.noaa.gov](https://oceanservice.noaa.gov/facts/lidar.html) — 펄스 레이저로 거리 재기
- Li와 Ibanez-Guzman, "Lidar for Autonomous Driving," *IEEE Signal Processing Magazine* 37(4), 2020 — [doi:10.1109/MSP.2020.2973615](https://doi.org/10.1109/MSP.2020.2973615) — 파장; MEMS, 광위상배열, 플래시 방식
- Dreissig 등, "Survey on LiDAR Perception in Adverse Weather Conditions," IEEE IV 2023 — [arXiv:2304.06312](https://arxiv.org/abs/2304.06312) — 파장; 비와 안개 속의 이른 귀환과 잃은 귀환
- Phillips, Guenther, McAree, "When the Dust Settles," *J. Field Robotics* 34(5), 2017 — [doi:10.1002/rob.21701](https://doi.org/10.1002/rob.21701) — 앞쪽 경계로 재는 먼지; 투과율 $71$–$74\%$, $2\%$, $6\%$
- Henley 등, "Detection and mapping of specular surfaces using multibounce lidar returns," *Optics Express* 31(4), 2023 — [doi:10.1364/OE.479900](https://doi.org/10.1364/OE.479900) — 단일 산란 귀환에 보이지 않는 정반사 면
- USGS, Lidar Base Specification 용어집 — [usgs.gov](https://www.usgs.gov/ngp-standards-and-specifications/lidar-base-specification-glossary) — 이산 귀환, 첫 귀환과 마지막 귀환
- Ouster, 센서 데이터와 OS 개요 — [static.ouster.dev](https://static.ouster.dev/sensor-docs/image_route1/image_route2/sensor_data/sensor-data.html), [ouster.com](https://ouster.com/os-overview) — 열마다의 타임스탬프, 보정된 반사율, 이중 귀환; 채널 수와 열 수
- ROS 2 `sensor_msgs`의 Image와 PointCloud2(jazzy) — [github.com/ros2/common_interfaces](https://github.com/ros2/common_interfaces/blob/jazzy/sensor_msgs/msg/PointCloud2.msg) — 메시지마다 헤더 스탬프 하나
- Texas Instruments, AWR1843 — [ti.com](https://www.ti.com/product/AWR1843) — 송신기 $3$개, 수신기 $4$개, $4\,\mathrm{GHz}$의 단일 칩 $76$–$81\,\mathrm{GHz}$ 레이더
- Harlow 등, "A New Wave in Robotics: Survey on Recent mmWave Radar Applications in Robotics," *IEEE T-RO* 40, 2024 — [arXiv:2305.01135](https://arxiv.org/abs/2305.01135) — FMCW 분해능 식; 안개, 먼지, 연기; 유령; 레이더가 쓰이는 곳
- Bertoldo 등, "On the Use of a 77 GHz Automotive Radar as a Microwave Rain Gauge," *ETASR* 8(1), 2018 — [etasr.com](https://etasr.com/index.php/ETASR/article/view/1755) — $77\,\mathrm{GHz}$에서 비는 투명하지 않다
- Ruff, "Evaluation of a radar-based proximity warning system for off-highway dump trucks," *Accident Analysis & Prevention* 38(1), 2006 — [doi:10.1016/j.aap.2005.07.006](https://doi.org/10.1016/j.aap.2005.07.006) — 운반 트럭 주변의 검출과 오경보
- MathWorks, LiDAR–카메라 보정 — [mathworks.com](https://www.mathworks.com/help/lidar/ug/lidar-and-camera-calibration.html) — 체커보드 작업 흐름
- KITTI 센서 구성 — [cvlibs.net](https://www.cvlibs.net/datasets/kitti/setup.php) — 레이저 스캐너가 트리거하는 카메라
- Nokia, IEEE 1588 오프셋과 지연 — [documentation.nokia.com](https://documentation.nokia.com/html/0_add-h-f/93-0267-HTML/7X50_Advanced_Configuration_Guide/ACG-%20IEEE-1588-FP-TD.html) — 스탬프 넷의 식과 비대칭 오차
- Lee와 Eidson, 2004년 IEEE 1588 학술대회, NIST — [nist.gov](https://www.nist.gov/publications/standard-precision-clock-synchronization-protocol-networked-measurement-and-control) — 시연된 마이크로초 미만 동기화
- chrony FAQ — [chrony-project.org](https://chrony-project.org/faq.html) — 비대칭 지연이 잰 오프셋을 제한한다
