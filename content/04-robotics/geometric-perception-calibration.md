---
title: 3.5 Geometric Perception & Calibration
tags: [robotics, perception, calibration, geometry]
study-depth: Working
depth-goal: "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool."
mastery-when: "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution."
wiki-support: Working
---

## English

*Group B. Stands on [[02-foundations/linear-algebra|linear algebra]], optimization and [[02-foundations/se3-geometry|SE(3)]]. This is how pixels and point clouds
become 3D in the right frame — every perception claim in groups H and J passes through here.*

[[02-foundations/se3-geometry|SE(3)]] is the language for *writing down* poses; geometric
perception is how a robot *obtains* them — how pixels, depths, and point clouds become
3D structure expressed in the right coordinate frame. Deep perception
([[03-deep-learning/index|Deep Learning]]) tells you *what* something is; geometric
perception tells you *where* it is, at *what scale*, in *which frame*.

> [!info] Depth target
> Read pose-estimation, visual-odometry/SLAM-front-end, calibration, and point-cloud
> papers without stalling on projection, intrinsics/extrinsics, registration, or
> reprojection error. Deriving multiview geometry (essential/fundamental matrices,
> bundle adjustment) is a working/mastery topic.

> [!note] Prerequisites
> Plants **P2** and **P5** from [[02-foundations/lab-plants|0.6 Lab Plants]] · [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/se3-geometry|3D Geometry & SE(3)]] · [[02-foundations/optimization|Optimization]] (least squares) · [[02-foundations/probability|Probability]] (maximum likelihood, §4; the scalar Kalman update P5 uses, §5)

> [!note] First pass · 처음이라면
> Start with the picture and the Worked case: one point of the rig projected, triangulated, distorted and miscalibrated, with every number. Then read §1 (the pinhole model, with the projection written out), §5 (calibration — where most field failures actually start) and §7 (reading claims). §2 to §4 (depth, image features, two-view geometry, point clouds, ICP) are the machinery; read them when a paper's numbers depend on them. §6 and §7.5 are short bridges to learned perception and to visual servoing.

### Running object: the wrist rig on P2

No plant in [[02-foundations/lab-plants|0.6 Lab Plants]] is a camera, so this page freezes its own rig and never changes these numbers. It is mounted on **P2**, the planar 2R arm, looking along the tool axis at the panel; **P5** supplies the one scalar range the problem set fuses. Lengths in metres, pixels in pixels, and P5's range in centimetres as 0.6 freezes it.

| Symbol | Value | What it is |
|---|---:|---|
| $f_x, f_y$ | $600$ px each | focal length in pixels, equal because the pixels are square |
| $c_x, c_y$ | $320$, $240$ px | principal point, the image centre of a $640\times480$ sensor |
| $s$ | $0$ | skew, zero for every sensor you will meet |
| $k_1, k_2$ | $-0.20$, $+0.05$ | radial distortion coefficients (barrel, since $k_1<0$) |
| $p_1, p_2$ | $0$, $0$ | tangential distortion, zero for a well-seated lens |
| $b$ | $0.12$ m | stereo baseline: a second identical camera with $t = (-b, 0, 0)$, $R = I$ |
| $L$ | $(0.5,\ 0.2,\ 2.0)$ m | the landmark, in camera 1's frame |
| $A, B, C$ | $(0,0,2)$, $(0.5,0,2)$, $(0,0.4,2)$ m | three calibration-target corners on one plane |
| $d_{ct}$ | $0.04$ m | hand–eye offset: the camera sits this far behind P2's tool tip |
| P5 | $10 \pm 2$ cm prior, $12$ cm read, $R = 1\,\mathrm{cm}^2$ | the range to the panel, frozen in 0.6 |

Everything else on the page is derived from that table. $L$ lands at $(470, 300)$ px in camera 1 and $(434, 300)$ px in camera 2, so its disparity is $36$ px and $Z = f b / d = 600 \times 0.12 / 36 = 2.0$ m, which is where it started — the round trip is the check that the rig is consistent.

*Scope: this page teaches the geometry between a 3D point and a pixel and the calibrations that geometry depends on — intrinsics, extrinsics, distortion, two-view constraints, registration. It does not teach what an object is ([[03-deep-learning/index|Deep Learning]]), how the camera pose is estimated over time ([[04-robotics/state-estimation-slam|3. State Estimation & SLAM]]), or how the rig is published and time-stamped at runtime ([[04-robotics/robot-systems-deployment|10. Robot Systems]]).*

### The picture: one ray, two cameras, three error bars

<svg viewBox="0 0 560 472" style="max-width:100%;height:auto" role="img" aria-label="Stereo picture for the wrist rig: the pinhole projection of the landmark with its two similar triangles, a second camera 0.12 m to the side with rays to the landmark at 2 m and to a point at 8 m, and the two depth error bars and the distortion shift drawn to scale">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">projection, XZ plane</text>
  <text x="232" y="24" font-size="12" fill="currentColor" font-weight="600">the second camera</text>
  <text x="404" y="24" font-size="12" fill="currentColor" font-weight="600">three errors, to scale</text>
  <path d="M64 300 L64 100 L114 100 Z" fill="currentColor" fill-opacity="0.07" stroke="none"/>
  <path d="M64 300 L64 180 L94 180 Z" fill="currentColor" fill-opacity="0.24" stroke="none"/>
  <line x1="64" y1="300" x2="64" y2="50" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <path d="M64 44 L66.9 51 L61.1 51 Z" fill="currentColor" stroke="none" fill-opacity="0.7"/>
  <text x="72" y="56" font-size="11" fill="currentColor" fill-opacity="0.8">optical axis</text>
  <line x1="36" y1="180" x2="190" y2="180" stroke="currentColor" stroke-width="1.8"/>
  <text x="106" y="173" font-size="11" fill="currentColor">image plane, Z = f</text>
  <line x1="64" y1="100" x2="114" y2="100" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="114" y1="100" x2="64" y2="300" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="114" cy="100" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="94" cy="180" r="3.2" stroke="none" fill="currentColor"/>
  <circle cx="64" cy="300" r="3.6" stroke="none" fill="currentColor"/>
  <text x="64" y="318" font-size="12" fill="currentColor" text-anchor="middle">O</text>
  <text x="122" y="104" font-size="11" fill="currentColor">L (0.5, 2.0) m</text>
  <line x1="30" y1="100" x2="30" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="27" y1="100" x2="33" y2="100" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="27" y1="300" x2="33" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="46" y1="180" x2="46" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="43" y1="180" x2="49" y2="180" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="43" y1="300" x2="49" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="24" y="144" font-size="12" fill="currentColor" text-anchor="end">Z</text>
  <text x="38" y="244" font-size="12" fill="currentColor" text-anchor="middle">f</text>
  <line x1="64" y1="90" x2="114" y2="90" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="64" y1="87" x2="64" y2="93" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="114" y1="87" x2="114" y2="93" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="89" y="84" font-size="12" fill="currentColor" text-anchor="middle">X</text>
  <line x1="64" y1="187" x2="94" y2="187" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="64" y1="184" x2="64" y2="190" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="94" y1="184" x2="94" y2="190" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="104" y="198" font-size="11" fill="currentColor">u − c<tspan dy="3.1" font-size="8.6">x</tspan></text>
  <text x="16" y="340" font-size="11" fill="currentColor">(u − c<tspan dy="3.1" font-size="8.6">x</tspan><tspan dy="-3.1">) / f = X / Z</tspan></text>
  <text x="16" y="356" font-size="11" fill="currentColor">150 / 600 = 0.5 / 2.0</text>
  <text x="16" y="372" font-size="11" fill="currentColor">so u = 320 + 150 = 470 px</text>
  <line x1="250" y1="300" x2="250" y2="64" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="280" y1="300" x2="280" y2="64" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="250" y1="300" x2="287.5" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" stroke-dasharray="6 3"/>
  <line x1="280" y1="300" x2="308.5" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" stroke-dasharray="6 3"/>
  <path d="M287.5 60 L289.3 67.4 L283.5 66.5 Z" fill="currentColor" stroke="none"/>
  <path d="M308.5 60 L310.6 67.3 L304.8 66.6 Z" fill="currentColor" stroke="none"/>
  <line x1="250" y1="300" x2="375" y2="100" stroke="currentColor" stroke-width="1.6"/>
  <line x1="280" y1="300" x2="375" y2="100" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="375" cy="100" r="4.2" stroke="none" fill="currentColor"/>
  <text x="369" y="91" font-size="12" fill="currentColor" text-anchor="middle">L</text>
  <path d="M244 309 L250 300 L256 309 Z" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.25" stroke-linejoin="round"/>
  <path d="M274 309 L280 300 L286 309 Z" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.25" stroke-linejoin="round"/>
  <text x="241" y="322" font-size="11" fill="currentColor" text-anchor="middle">C<tspan dy="3.1" font-size="8.6">1</tspan></text>
  <text x="284" y="322" font-size="11" fill="currentColor">C<tspan dy="3.1" font-size="8.6">2</tspan><tspan dx="3.1" dy="-3.1">at X = +0.12 m</tspan></text>
  <text x="301.5" y="46" font-size="11" fill="currentColor">Z = 8 m: d = 9 px</text>
  <text x="360" y="112" font-size="11" fill="currentColor" text-anchor="end">d = 36 px</text>
  <text x="392" y="282" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">X drawn 2.5× Z</text>
  <line x1="234" y1="374" x2="391.5" y2="374" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="244.5" y1="371" x2="244.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="265.5" y1="371" x2="265.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="286.5" y1="371" x2="286.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="307.5" y1="371" x2="307.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="328.5" y1="371" x2="328.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="349.5" y1="371" x2="349.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="370.5" y1="371" x2="370.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="391.5" y1="371" x2="391.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="234" y="340" font-size="11" fill="currentColor" fill-opacity="0.85">both images on one u axis (px)</text>
  <line x1="343.2" y1="365" x2="343.2" y2="377" stroke="currentColor" stroke-width="1.8"/>
  <line x1="381" y1="365" x2="381" y2="377" stroke="currentColor" stroke-width="1.8"/>
  <text x="343.2" y="361" font-size="11" fill="currentColor" text-anchor="middle">434</text>
  <text x="381" y="361" font-size="11" fill="currentColor" text-anchor="middle">470</text>
  <line x1="347.6" y1="383" x2="376.6" y2="383" stroke="currentColor" stroke-width="1.1"/>
  <path d="M381 383 L375.5 385.3 L375.5 380.7 Z" fill="currentColor" stroke="none"/>
  <path d="M343.2 383 L348.7 380.7 L348.7 385.3 Z" fill="currentColor" stroke="none"/>
  <text x="362.1" y="397" font-size="11" fill="currentColor" text-anchor="middle">d = 36</text>
  <line x1="253.4" y1="365" x2="253.4" y2="377" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9"/>
  <line x1="262.9" y1="365" x2="262.9" y2="377" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9"/>
  <text x="258.1" y="361" font-size="11" fill="currentColor" text-anchor="middle">8 m</text>
  <line x1="253.4" y1="383" x2="262.9" y2="383" stroke="currentColor" stroke-width="1.1"/>
  <line x1="253.4" y1="380" x2="253.4" y2="386" stroke="currentColor" stroke-width="1.0"/>
  <line x1="262.9" y1="380" x2="262.9" y2="386" stroke="currentColor" stroke-width="1.0"/>
  <text x="258.1" y="397" font-size="11" fill="currentColor" text-anchor="middle">d = 9</text>
  <line x1="444" y1="300" x2="444" y2="39.6" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <path d="M444 32.6 L446.5 38.6 L441.5 38.6 Z" fill="currentColor" stroke="none" fill-opacity="0.8"/>
  <text x="452" y="43.6" font-size="11" fill="currentColor">Z (m)</text>
  <line x1="440" y1="300" x2="444" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="304" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="440" y1="244" x2="444" y2="244" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="248" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">2</text>
  <line x1="440" y1="188" x2="444" y2="188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="192" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">4</text>
  <line x1="440" y1="132" x2="444" y2="132" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="136" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">6</text>
  <line x1="440" y1="76" x2="444" y2="76" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="80" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">8</text>
  <rect x="450" y="242.4" width="10" height="3.1" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.35"/>
  <line x1="447" y1="242.4" x2="463" y2="242.4" stroke="currentColor" stroke-width="1.2"/>
  <line x1="447" y1="245.6" x2="463" y2="245.6" stroke="currentColor" stroke-width="1.2"/>
  <rect x="450" y="51.1" width="10" height="49.8" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.35"/>
  <line x1="447" y1="51.1" x2="463" y2="51.1" stroke="currentColor" stroke-width="1.2"/>
  <line x1="447" y1="100.9" x2="463" y2="100.9" stroke="currentColor" stroke-width="1.2"/>
  <text x="468" y="248" font-size="11" fill="currentColor">(i) ±0.056 m</text>
  <text x="468" y="76" font-size="11" fill="currentColor">(ii) ±0.89 m</text>
  <text x="468" y="90" font-size="11" fill="currentColor" fill-opacity="0.85">16× longer</text>
  <line x1="414" y1="330" x2="414" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="425" y1="330" x2="425" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="436" y1="330" x2="436" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="447" y1="330" x2="447" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="458" y1="330" x2="458" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="469" y1="330" x2="469" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="480" y1="330" x2="480" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="491" y1="330" x2="491" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="502" y1="330" x2="502" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="330" x2="502" y2="330" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="341" x2="502" y2="341" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="352" x2="502" y2="352" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="363" x2="502" y2="363" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="374" x2="502" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <circle cx="469" cy="363" r="3.4" stroke="none" fill="currentColor"/>
  <line x1="469" y1="363" x2="450" y2="355.4" stroke="currentColor" stroke-width="1.6"/>
  <path d="M445.5 353.6 L452 353.5 L450.1 358.2 Z" fill="currentColor" stroke="none"/>
  <text x="414" y="322" font-size="11" fill="currentColor">(iii) image plane</text>
  <text x="414" y="389" font-size="11" fill="currentColor">2.30 px bias</text>
  <text x="414" y="403" font-size="11" fill="currentColor" fill-opacity="0.8">1 square = 1 px</text>
  <text x="16" y="428" font-size="11" fill="currentColor" fill-opacity="0.9">At 8 m the two rays are nearly parallel (d = 9 px against 36): that angle is what depth accuracy is made of.</text>
  <text x="16" y="444" font-size="11" fill="currentColor" fill-opacity="0.9">The two depth bars share one scale, so the 8 m bar is sixteen times the 2 m bar: depth error grows as Z².</text>
  <text x="16" y="460" font-size="11" fill="currentColor" fill-opacity="0.9">The 2.30 px shift is a bias on the image plane, not noise: averaging frames does not shrink it.</text>
</svg>

The wrist rig and its landmark $L$, at $(X,Z)=(0.5,\,2.0)$ m. Left, the pinhole projection in the $XZ$ plane, whose similar triangles give $150/600=0.5/2.0$ and so $u=470$ px; middle, the second camera $0.12$ m to the side sees $L$ at $u=434$, a disparity of $36$ px, while a point at $8$ m gives only $9$ px along nearly parallel rays. Right, three errors to scale: a $\pm1$ px disparity error is $\pm0.056$ m of depth at $2$ m and $\pm0.89$ m at $8$ m, sixteen times longer because depth error grows as $Z^2$, and the $2.30$ px distortion shift at $L$ sits on the image plane as a bias, not noise.

### Worked case: from the table to a pixel, and back

**1. Project $L$.** In homogeneous form, with the camera frame equal to the world frame so $R = I$ and $t = 0$, and with $K$ the intrinsic matrix that holds the table's $f_x, f_y, c_x, c_y$ and skew $s$ (§1 defines it entry by entry):

$$\tilde u = K\,[R \mid t]\,\tilde L = \begin{pmatrix}600&0&320\\0&600&240\\0&0&1\end{pmatrix}\begin{pmatrix}0.5\\0.2\\2.0\end{pmatrix} = \begin{pmatrix}940\\600\\2\end{pmatrix}$$

so dividing by the third entry gives $(u, v) = (470, 300)$ px, because the division by $Z$ that perspective performs is exactly the dehomogenization of the third coordinate.

**2. The same point in camera 2, and back to depth.** $p^{c_2} = Ip^{c_1} + t = (0.5 - 0.12,\ 0.2,\ 2.0) = (0.38, 0.2, 2.0)$, which projects to $u_2 = 600 \times 0.38/2.0 + 320 = 434$ and $v_2 = 300$. The disparity is $d = 470 - 434 = 36$ px and $Z = f b / d = 2.0$ m, then $X = (u_1 - c_x)Z/f_x = 150 \times 2/600 = 0.5$ m and $Y = (v_1 - c_y)Z/f_y = 60 \times 2/600 = 0.2$ m. The rig recovers $L$ exactly, since with $R = I$ the triangulation is algebraically the inverse of the projection.

**3. Where distortion moves it.** Distortion acts on the normalized coordinates, before $K$, through the radial factor $1 + k_1r^2 + k_2r^4$ of the Brown–Conrady model (§1 states the model and its order). Here the normalized coordinates are $x_n = X/Z = 0.25$ and $y_n = Y/Z = 0.10$, so $r^2 = 0.0725$ and $r^4 = 0.00525625$. The radial factor is $1 + k_1r^2 + k_2r^4 = 1 - 0.0145 + 0.000263 = 0.985763$, giving $(x_d, y_d) = (0.246441, 0.098576)$ and a distorted pixel of $(467.864,\ 299.146)$. The landmark actually lands $2.30$ px from where the ideal model says, and that is at a modest $r = 0.269$; it grows as $r^2$ toward the image corners.

**4. What a sub-pixel calibration residual hides.** Suppose calibration returns $\hat f = 598$ px instead of $600$, everything else exact. Reproject the three target corners:

| Corner | true $(u,v)$ | with $\hat f = 598$ | residual |
|---|---|---|---:|
| $A=(0,0,2)$ | $(320,\ 240)$ | $(320.0,\ 240.0)$ | $0.00$ px |
| $B=(0.5,0,2)$ | $(470,\ 240)$ | $(469.5,\ 240.0)$ | $0.50$ px |
| $C=(0,0.4,2)$ | $(320,\ 360)$ | $(320.0,\ 359.6)$ | $0.40$ px |

The RMS reprojection error, the root-mean-square pixel distance between detected and reprojected corners (§5 defines it), is $\sqrt{(0^2 + 0.5^2 + 0.4^2)/3} = 0.370$ px — comfortably "sub-pixel", and the corner at the principal point contributes nothing at all, because a focal-length error is invisible there. Now use that calibration to back-project $B$'s detection at a known $Z = 2$ m: $X = (470-320)\times 2/598 = 0.50167$ m, an error of $1.67$ mm. The relative error is $(f - \hat f)/\hat f = 0.334\%$ of the off-axis distance, so it is $1.67$ mm at $X = 0.5$ m and $10.0$ mm at $X = 3$ m. A sub-pixel residual is a statement about the fit, not about the metre.

### 1. The pinhole camera model

A 3D point $p^{c}=(X,Y,Z)$ in the **camera frame** projects to pixel $(u,v)$:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

**Where that comes from — similar triangles, and nothing else.** Put the optical centre at
the origin and the image plane at distance $f$ in front of it. The ray from the 3D point
$(X, Y, Z)$ to the centre crosses that plane at height $y$, and the two triangles it forms —
one from the centre to the plane, one from the centre to the point — are similar. So
$y/f = Y/Z$, giving $y = fY/Z$. The rest is bookkeeping: divide by the physical pixel pitch
to get pixels (which is why $f_x$ and $f_y$ differ when pixels are not square, and why focal
length is quoted *in pixels* rather than millimetres), then add $c_x, c_y$ to move the origin
from the optical axis to the image corner, where array indices start.

That is the whole model, and its shape carries the two facts everything downstream inherits.
The map is **not linear** — $Z$ sits in the denominator, which is why perspective needs
homogeneous coordinates before it can be a matrix at all — and it is **not invertible**,
since every point along one ray produces the same $(u,v)$. Recovering $Z$ is therefore not a
matter of a better camera; it needs a second constraint, which is what §2 is about.

- **Intrinsics** $(f_x, f_y, c_x, c_y$, distortion$)$: properties of the camera itself —
  focal lengths in pixels and the principal point. Fixed once calibrated (until the lens
  is touched).
- **Extrinsics** $(R, t)$: the [[02-foundations/se3-geometry|SE(3)]] transform $T_{cw}$ that moves points from another frame (robot base,
  world) into the camera frame before projection, $p^c = Rp^w + t$. The camera's *pose* in that frame is its inverse, $T_{wc}$, with the camera centre at $-R^\top t$: the centre is the point with $p^c=0$, so $0=Rp^w+t$ gives $p^w=-R^\top t$ (using $R^{-1}=R^\top$). Check which one a calibration file stores.
- Division by $Z$ is the whole story of perspective: farther points move less in the
  image, and **absolute scale is lost** — a single image cannot tell a large-far object
  from a small-near one.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="pinhole projection: a small near object and a large far one land on the same pixels">
  <g stroke="currentColor" stroke-width="1.3"><line x1="150" y1="25" x2="150" y2="170"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="4 3"><line x1="60" y1="110.0" x2="440" y2="110.0"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <line x1="60" y1="110" x2="440" y2="26.4"/><line x1="60" y1="110" x2="440" y2="72.0"/>
  </g>
  <g stroke="currentColor" stroke-width="3.2">
    <line x1="150" y1="90.2" x2="150" y2="101.0"/>
    <line x1="250" y1="68.2" x2="250" y2="91.0"/>
    <line x1="420" y1="30.8" x2="420" y2="74.0"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="110" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="114">O</text>
    <text x="112" y="20">image plane</text>
    <text x="212" y="110">small and near</text>
    <text x="372" y="92">large and far</text>
    <text x="158" y="128">the same image on the sensor</text>
    <text x="25" y="192" opacity="0.85">u = f X / Z + c &#8212; dividing by Z is exactly what destroys absolute scale</text>
  </g>
</svg>



**Worked projection**: $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, point
$p^{c}=(0.5, 0.2, 2.0)$ m. Then $u = 600\cdot 0.5/2.0+320=470$,
$v = 600\cdot 0.2/2.0+240=300$. Move the point twice as far
($Z=4$): $u=395, v=270$ — it slides toward the principal point.

**The intrinsic matrix, stated completely.** $K$ is an **upper-triangular $3\times3$ matrix** that maps a point in normalized image coordinates — the ray direction $(X/Z,\ Y/Z,\ 1)$, which is what is left of a 3D point after perspective has thrown away its distance — to pixel coordinates. It has five entries, and naming all five is the definition:

$$K = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}$$

- $f_x, f_y$ — **focal length in pixels along each image axis**, that is, the physical focal length divided by the pixel pitch in that direction. They are equal exactly when the pixels are square, so $f_x \ne f_y$ is a statement about the sensor, not about the lens. The rig freezes both at $600$.
- $c_x, c_y$ — the **principal point**, where the optical axis pierces the image plane, in pixels from the array corner. It is near the image centre but not exactly at it; a calibration that returns $c_x$ far from $w/2$ is usually reporting a cropped or mis-specified image.
- $s$ — **skew**, non-zero only if the sensor's two pixel axes are not perpendicular. It is $0$ on every solid-state sensor, and the rig freezes it at $0$. It survives in the model mostly so that $K$ can absorb an affine rectification.

The whole camera is then the composition of extrinsics and intrinsics on homogeneous coordinates, which is the one equation the rest of the page differentiates, inverts and optimizes:

$$\lambda \begin{pmatrix}u\\v\\1\end{pmatrix} = K\,[R \mid t]\begin{pmatrix}X^w\\Y^w\\Z^w\\1\end{pmatrix}, \qquad \lambda = Z^c$$

The scalar $\lambda$ is the depth in the camera frame, so dividing it out *is* the perspective division, and $K$ has to be written this way because a matrix cannot divide — only the dehomogenization can. *Example:* the rig's $K$ takes $L$'s ray $(0.25, 0.10, 1)$ to $(470, 300, 1)$. *Non-example:* $K$ is **not** a change of physical units. It maps a direction to a pixel, so applying $K$ to a point in metres, as $K(0.5, 0.2, 2.0)^\top$, only accidentally works — it gives $(940, 600, 2)$, which dehomogenizes to the right answer precisely because the third row divides by $Z$ again. Feed it a ray you have already normalized and it is correct; feed it a metric point without dividing and you have relied on a coincidence.

**Extrinsics, stated completely.** $[R \mid t]$ is the $3\times4$ block of the **SE(3)** transform $T_{cw}$ that expresses a world point in the camera frame, $p^c = Rp^w + t$, with $R \in SO(3)$ and $t \in \mathbb{R}^3$ ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3)]]). Two conditions make it an extrinsic rather than a pose: it is the **world-to-camera** direction, and it carries **no** scale or shear, since $R^\top R = I$. The camera's *pose in the world* is the inverse $T_{wc}$, whose translation is the camera centre $-R^\top t$, because the centre is the point with $p^c = 0$ and $0 = Rp^w + t$ gives $p^w = -R^\top t$. *Non-example:* storing $t$ and calling it "the camera position" is the single most common calibration-file bug — $t$ equals the camera centre only when $R = I$, and then only up to sign.

**The distortion model, stated completely.** A real lens bends rays, so the pinhole map is applied in **normalized coordinates first, distortion second, and $K$ last** — that order is part of the definition, and swapping it is a silent error. With $x_n = X/Z$, $y_n = Y/Z$ and $r^2 = x_n^2 + y_n^2$, the Brown–Conrady model used by OpenCV has two radial terms and two tangential ones:

$$\begin{pmatrix}x_d\\y_d\end{pmatrix} = \underbrace{(1 + k_1r^2 + k_2r^4 + k_3r^6)}_{\text{radial}}\begin{pmatrix}x_n\\y_n\end{pmatrix} + \underbrace{\begin{pmatrix}2p_1x_ny_n + p_2(r^2+2x_n^2)\\ p_1(r^2+2y_n^2) + 2p_2x_ny_n\end{pmatrix}}_{\text{tangential}}$$

then $u = f_xx_d + c_x$ and $v = f_yy_d + c_y$. The **radial** part is even in $r$ and moves a point along its own radius — outward for $k_1>0$ (pincushion), inward for $k_1<0$ (barrel) — because a lens's deviation depends on how far off-axis a ray enters, not on which way. The **tangential** part comes from the lens not being parallel to the sensor and moves points sideways. *Example:* the rig's $L$ sits at $r = 0.269$, and $k_1 = -0.20$, $k_2 = 0.05$ pull it from $(470, 300)$ to $(467.86, 299.15)$, a shift of $2.30$ px. *Non-example:* distortion is **not** noise. It is a deterministic, repeatable bias, so averaging more frames does not reduce it by $1/\sqrt{n}$ — only estimating $k_1, k_2$ does. A feature matcher reporting "sub-pixel" repeatability on an uncorrected image is repeatably $2.3$ px wrong. *Why it matters:* every residual later on this page — reprojection error, epipolar distance, ICP — is computed against the *undistorted* model, so an unmodelled $k_1$ enters all three as a bias that no amount of least squares can absorb.

### 2. Recovering depth

| Source | How depth appears | Main caution |
|---|---|---|
| Stereo | disparity $d$ between two views: $Z = f\,b/d$ (baseline $b$) | textureless/repetitive surfaces; error grows as $Z^2$ |
| RGB-D / ToF / structured light | sensor measures $Z$ per pixel | range limits, sunlight, reflective/dark materials |
| LiDAR | direct time-of-flight ranges | sparsity, motion distortion, weather |
| Learned monocular depth | network predicts $Z$ (often only up to an unknown scale and shift, frequently in inverse depth $1/Z$, which stays bounded as points recede toward the far background) | scale ambiguity; distribution shift — check the [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]] claim scope |
| Triangulation | intersect rays from two known poses | needs baseline; degenerate for distant points and small baselines |

**Stereo worked example**: $f=600$ px, baseline $b=0.12$ m, disparity $d=9$ px
→ $Z = 600\cdot 0.12/9 = 8$ m. One pixel of disparity error ($d=8$) gives $Z=9$ m —
a 12.5% jump at this range: depth error grows quadratically with distance. Across the optical axis the same pixel is worth only $Z/f$ metres, and turning a pixel-noise σ into the measurement variance a filter needs is [[04-robotics/sensor-models|3.2 Sensor Models & Noise §5 and §8]]. The table's other rows are sensors with physics of their own — a time-of-flight camera that wraps, a LiDAR whose spots grow with range — priced on this rig in [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §3–§5]].



<svg viewBox="0 0 620 246" style="max-width:100%;height:auto" role="img" aria-label="stereo: a near point splays the two rays, a far point makes them nearly parallel">
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="60" y1="190" x2="60" y2="172"/><line x1="140" y1="190" x2="140" y2="172"/>
    <line x1="360" y1="190" x2="360" y2="172"/><line x1="440" y1="190" x2="440" y2="172"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" opacity="0.8" fill="none">
    <line x1="60" y1="190" x2="100" y2="140"/><line x1="140" y1="190" x2="100" y2="140"/>
    <line x1="360" y1="190" x2="400" y2="70"/><line x1="440" y1="190" x2="400" y2="70"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="3.5"/><circle cx="140" cy="190" r="3.5"/>
    <circle cx="360" cy="190" r="3.5"/><circle cx="440" cy="190" r="3.5"/>
    <circle cx="100" cy="140" r="4.5"/><circle cx="400" cy="70" r="4.5"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="3 3">
    <line x1="60" y1="202" x2="140" y2="202"/><line x1="360" y1="202" x2="440" y2="202"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="30">NEAR</text><text x="400" y="30">FAR</text>
    <text x="100" y="48" font-size="10.5" opacity="0.85">Z = 2 m &#183; disparity 36 px</text>
    <text x="400" y="48" font-size="10.5" opacity="0.85">Z = 8 m &#183; disparity 9 px</text>
    <text x="100" y="218" font-size="10.5">baseline b</text><text x="400" y="218" font-size="10.5">baseline b</text>
  </g>
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">Disparity is horizontal pixel displacement; it shrinks with the triangulation angle for far points.</text></g>
</svg>

**Why the error grows as $Z^2$.** Differentiate $Z=fb/d$: $dZ/dd=-fb/d^2=-Z^2/(fb)$, so a disparity error of $\Delta d$ pixels moves the depth by about $Z^2\Delta d/(fb)$. On the rig $fb=600\times0.12=72$ px·m, so one pixel is $4/72=0.056$ m at the landmark's $2$ m, which is $2.8\%$ of the range, and $64/72=0.89$ m at $8$ m: the error bars drawn in the picture. Set against the lateral $Z/f$ per pixel of the stereo example above, the ratio of the two errors is $Z/b$: $16.7$ at $2$ m and $67$ at $8$ m, which is why a stereo point's uncertainty is a needle along the ray rather than a ball. The first-order value sits between the exact errors on either side, which are unequal (at $8$ m, $+1.00$ m for $d=8$ against $-0.80$ m for $d=10$); problem 2(b) asks why.

**The same law, run backwards, sizes a rig.** Holding $\pm1$ cm at $2$ m with one pixel of matching error needs $fb\ge Z^2/\Delta Z=4/0.01=400$ px·m, a baseline of $0.67$ m at $f=600$ px, more than five times this rig's. Sub-pixel matching buys it back: a matcher good to $0.2$ px needs only $0.13$ m. When a paper quotes a stereo depth error, ask at what range, since the same rig's error at $4$ m is sixteen times its error at $1$ m.

**Stereo also has a near limit.** At P5's $12$ cm reading the disparity would be $72/0.12=600$ px, nearly the whole $640$-px width, so the two views barely overlap, and a matcher that searches disparities up to $128$ px sees nothing nearer than $72/128=0.56$ m. That blind zone is why the rig takes the panel's range from P5's scalar sensor rather than from stereo, and the problem set fuses it.

### 2.5 Image features: detect, describe, match

**The idea in one sentence:** pick a few hundred points that can be found again in another image, give each a compact fingerprint, and pair fingerprints across images — those pairs are the correspondences every geometric step needs.

Why sparse points instead of every pixel? Stereo depth in §2 needs to know which right-image pixel shows the same point as a left-image pixel. Calibration in §5 needs target corners, the rig's $A$, $B$ and $C$, located to sub-pixel accuracy. Visual odometry and SLAM ([[04-robotics/state-estimation-slam|state estimation]]) track the same points across frames to constrain pose. A point is useful only if it is **repeatable** (detected again after the view changes) and **distinctive** (its neighbourhood does not resemble many others). The pipeline has three stages, and a paper can change any one of them.

**Detect: where the image changes in every direction.** Shift a small window by $(u,v)$ and measure how much its content changes. A first-order Taylor step gives $I(x+u,y+v)\approx I(x,y)+I_x u+I_y v$, so each pixel's difference is $I_x u+I_y v$ and its square $I_x^2u^2+2I_xI_y\,uv+I_y^2v^2$ is quadratic in $(u,v)$. Summing over the window therefore turns the change into a quadratic form:

$$E(u,v)=\sum_{x,y} w(x,y)\,\big(I(x+u,y+v)-I(x,y)\big)^2 \approx (u,v)\,M\,(u,v)^\top$$

so the whole behaviour is governed by one 2×2 matrix, the **structure tensor**. It sums the image gradients $I_x, I_y$ over the window with weights $w$ (a box or a Gaussian):

$$M=\sum_{x,y} w(x,y)\begin{pmatrix}I_x^2 & I_xI_y\\ I_xI_y & I_y^2\end{pmatrix}$$

Its eigenvalues $\lambda_1 \le \lambda_2$ are the change along the least- and most-varying shift directions, so they classify the window:

- **Flat**: both small — no shift changes anything.
- **Edge**: one large, one near zero — sliding along the edge changes nothing, so the point cannot be located along it (the aperture problem).
- **Corner**: both large — every shift is visible, so the point is pinned in 2D.

Harris and Stephens (Alvey Vision Conference, 1988) avoid the eigen-decomposition with the response

$$R=\det M-k\,(\operatorname{tr}M)^2=\lambda_1\lambda_2-k\,(\lambda_1+\lambda_2)^2$$

which works because the determinant and trace are the product and sum of the eigenvalues: $R$ is large and positive at a corner, negative on an edge and near zero in a flat region. $k$ is an empirical constant, commonly 0.04–0.06. Shi and Tomasi ("Good Features to Track", CVPR 1994) score the window by $\min(\lambda_1,\lambda_2)$ directly, which removes $k$. Either way, keep only local maxima above a threshold (non-maximum suppression).

**Scale: SIFT.** Harris is invariant to rotation but not to scale: a corner at one zoom level is a rounded curve at another. Lowe's SIFT (IJCV 2004) also searches over scale, in three steps.

- *Detect across scale.* It blurs the image with Gaussians of increasing $\sigma$, subtracts neighbouring levels (the difference of Gaussians, a cheap approximation of the scale-normalized Laplacian — a blob detector whose response peaks when the blur width is comparable to the blob's size), and keeps points that are extrema among their 26 neighbours in space and scale.
- *Reject.* Low-contrast points and edge-like points are discarded; the edge test uses a 2×2 Hessian eigenvalue ratio, the same logic as above.
- *Describe.* Each keypoint receives a dominant gradient orientation, and the descriptor is computed in that rotated, scaled frame: a 4×4 grid of cells around the point, each holding an 8-bin histogram of gradient orientations, gives 4·4·8 = 128 numbers. The vector is normalized to reduce illumination effects and compared by Euclidean distance.

**Binary: ORB.** SIFT descriptors are floating-point and comparatively costly. ORB (Rublee et al., ICCV 2011) replaces each stage with a cheaper one.

- *Detect:* the FAST corner test (a quick comparison of pixels on a circle around the candidate), ranked by the Harris score.
- *Orient:* an angle from the patch's intensity centroid.
- *Describe:* a rotated ("steered") BRIEF descriptor, 256 pairwise intensity comparisons stored as bits.

Two descriptors are compared by **Hamming distance** — XOR, then count the set bits — which costs a few CPU instructions. ORB-SLAM (Mur-Artal et al., IEEE T-RO 2015) uses ORB for tracking, mapping, relocalization and loop closing because it can be extracted and matched at frame rate on a CPU, is rotation-invariant and tolerates moderate viewpoint change. ORB itself is not scale-invariant, so it is extracted over an image pyramid.

**Match: nearest neighbour, then filter.** For each descriptor in image A, find the nearest descriptor in image B. Raw nearest neighbours contain many wrong pairs, so three filters follow:

1. **Ratio test** (Lowe 2004): accept only if $d_1/d_2 < 0.8$, where $d_1, d_2$ are the distances to the nearest and second-nearest candidates. A distinctive point has a clear winner; a point on a repeated pattern has two near-equal candidates. On his data, Lowe reports that 0.8 removed about 90% of false matches while discarding under 5% of correct ones.
2. **Mutual check**: keep $a\leftrightarrow b$ only if $a$ is also $b$'s nearest neighbour in the reverse direction.
3. **Geometric verification**: survivors must agree with one camera motion. RANSAC (Fischler & Bolles, CACM 1981) repeatedly fits a model — a fundamental or essential matrix, a homography, or a PnP pose — to a random minimal sample and keeps the model with the most inliers; the sample-count arithmetic is worked in [[02-foundations/algorithms/robotics-ai-problems|11.8 §3 RANSAC line fitting]]. The warning from ICP in §4 carries over: least squares on wrong correspondences is confidently wrong.

**Learned features.** SuperPoint (DeTone et al., CVPR Workshops 2018) trains one network to output keypoints and descriptors. SuperGlue (Sarlin et al., CVPR 2020) replaces nearest-neighbour-plus-ratio with a graph neural network that matches the two point sets jointly. LoFTR (Sun et al., CVPR 2021) drops the detector and matches dense transformer features, aiming at low-texture regions where detectors find few points. Each paper reports stronger matching under large viewpoint and illumination change on its benchmarks. Classic features can still be the right call. Weigh the compute budget and frame rate on an embedded robot computer, and whether the training data resembled your scenes. Textureless or repetitive construction surfaces — bare drywall, formwork, rebar grids, identical façade panels — are hard for every method, so test on your own sequences rather than trusting a benchmark ranking.

**The learned family, compared.** Each member changes a different stage. SuperGlue matches with attention and an optimal-transport assignment that may leave a point unmatched, in real time on a GPU; its successor LightGlue (Lindenberger et al., ICCV 2023) spends less on easy, high-overlap pairs, for latency-sensitive uses. LoFTR's dense matching helps where detectors find nothing, as on bare formwork. The 3D foundation models change the question. DUSt3R (Wang et al., CVPR 2024) regresses a 3D point map for an image pair with no calibration or poses, and matches and relative cameras follow from it; MASt3R (Leroy et al., ECCV 2024) adds descriptors trained to match; [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]] (Wang et al., CVPR 2025) predicts cameras, depth and tracks for up to hundreds of views in one pass, reporting reconstruction in under a second. None makes the third filter optional: check their matches with RANSAC on F, E, H or PnP (§2.7) — and a façade matched one panel over still fits one motion, so it passes.

> [!example] Worked example · 계산 예제
> **Harris on the rig's calibration image.** For this example, model the calibration target as one bright plate on a dark background with $A$ as its top-left corner: camera 1 sees $A$ at the principal point $(320, 240)$, and the plate runs right toward $B$ at $(470, 240)$ and down toward $C$ at $(320, 360)$. Take three 5×5 patches from that image, with intensity 0 on the background and 10 on the plate. Use central differences, $I_x=(I_{x+1}-I_{x-1})/2$, on the inner 3×3 pixels, with $w=1$ and $k=0.05$.
> - **Flat**, inside the plate around $(395, 300)$ (all 10): every gradient is 0, so $M=0$, $\lambda=(0,0)$ and $R=0$.
> - **Edge**, on the plate's left border between $A$ and $C$, around $(320, 300)$ (left two columns 0, the rest 10): $I_x=5$ at 6 pixels and $I_y=0$, so $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$ and $R=0-0.05\cdot150^2=-1125$.
> - **Corner**, centred on $A$ (bright lower-right 3×3 block): $I_x=5$ at 4 pixels, $I_y=5$ at 4, both at 1, so $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$ and $R=9375-0.05\cdot200^2=7375$.
>
> The signs follow the rule — flat 0, edge negative, corner positive — and the Shi–Tomasi scores are 0, 0 and 75. Only the patch at $A$ can be located in both image directions, which is why a calibration detects the target's corners and not points along its edges.
>
> **Ratio test, on $L$.** In camera 1's image of the panel, $L$'s descriptor at $(470, 300)$ is compared with camera 2's candidates. The true match at $(434, 300)$ is at distance 0.20, the same feature on the next panel over, at $(440, 300)$, at 0.23, and an unrelated point at 0.61. Since $0.20/0.23=0.87>0.8$, reject the match even though the nearest candidate is the right one: two similar candidates usually mean repeated structure, and the test cannot tell which of them is true. §2.6 shows what accepting the wrong one costs: $(440, 300)$ passes the epipolar check and triangulates $40$ cm too far. The third distance plays no role. Had the second been 0.45, $0.20/0.45=0.44$ would pass.

The same response on a 20×20 crop of that calibration image around $A$, with the plate filling the crop's lower-right quadrant and a check that $A$'s pixel scores highest:

```python
import numpy as np

def harris(img, k=0.05):
    Iy, Ix = np.gradient(img.astype(float))          # axis 0 is y (rows), axis 1 is x
    def box3(a):                                     # window sum with w = 1 on a 3x3 patch
        p = np.pad(a, 1)
        return sum(p[i:i + a.shape[0], j:j + a.shape[1]] for i in range(3) for j in range(3))
    Sxx, Syy, Sxy = box3(Ix * Ix), box3(Iy * Iy), box3(Ix * Iy)
    return Sxx * Syy - Sxy**2 - k * (Sxx + Syy)**2   # det M - k (tr M)^2 at every pixel

img = np.zeros((20, 20))
img[10:, 10:] = 1.0                                  # the plate; crop pixel (10, 10) is A at (320, 240)
R = harris(img)
r, c = np.unravel_index(np.argmax(R), R.shape)
print(r, c, round(R.max(), 3), round(R[15, 10], 3), R[3, 3])   # 10 10 0.738 -0.112 0.0
assert (r, c) == (10, 10) and R[15, 10] < 0 and R[3, 3] == 0     # corner > 0, edge < 0, flat 0
```

> [!warning] Reading matching claims · 매칭 주장 읽기
> - A match count is not accuracy. Look for the inlier ratio after geometric verification and the downstream pose error.
> - Note the ratio threshold, the RANSAC pixel threshold and the model (F, E, H or PnP); results move with all of them.
> - Repeated structure can yield matches that are consistently wrong: a set shifted by one façade panel still fits a single motion and passes RANSAC. This is the §4 warning in image form.
> - Harris and FAST are not scale-invariant on their own; check how scale is handled (pyramid or scale space).
> - For learned matchers, check the training data, input resolution, GPU and whether reported timing includes detection.

### 2.6 Two views: the epipolar constraint and triangulation

§2.5 produced candidate correspondences. Two questions remain: which of them are geometrically possible at all, and what 3D point a surviving pair implies. The first is answered by a constraint that needs no 3D point, the second by solving for one.

**The epipolar constraint, stated completely.** Take one 3D point seen by two cameras. Its two optical centres and the point span a plane — the **epipolar plane** — and each image sees that plane as a line. So the match of a point in image 1 cannot be anywhere in image 2: it must lie on **one line**, the **epipolar line**. Written algebraically with homogeneous pixel coordinates $\tilde u_1, \tilde u_2$ and normalized coordinates $\hat x_i = K_i^{-1}\tilde u_i$, the constraint is a single scalar equation:

$$\hat x_2^\top E\, \hat x_1 = 0, \qquad \tilde u_2^\top F\, \tilde u_1 = 0$$

It holds because $\hat x_1$, $\hat x_2$ and the baseline $t$ are coplanar, and a triple product of coplanar vectors vanishes.

- The **essential matrix** $E = [t]_\times R$ works in **calibrated** (normalized) coordinates, where $R, t$ are the second camera's rotation and translation relative to the first and $[t]_\times$ is the skew-symmetric matrix with $[t]_\times a = t \times a$, the cross product written as a matrix ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §1]]). It has **five** degrees of freedom — three for $R$, three for $t$, minus one because scale is unrecoverable — and its singular values are $(\sigma, \sigma, 0)$, so it is rank 2.
- The **fundamental matrix** $F = K_2^{-\top} E K_1^{-1}$ works in **pixels** and therefore needs no calibration at all. It has **seven** degrees of freedom: nine entries, minus one for overall scale, minus one for $\det F = 0$. It too is rank 2.
- Both are defined **only up to scale**, since multiplying either by a constant leaves the constraint $=0$ untouched.
- The constraint is **necessary, not sufficient.** It constrains a 2D match to a 1D line, removing one degree of freedom out of two. Everything along that line still passes.

*Example, on the rig.* With $R = I$ and $t = (-0.12, 0, 0)$,

$$E = [t]_\times = \begin{pmatrix}0&0&0\\0&0&0.12\\0&-0.12&0\end{pmatrix}, \qquad 5000\,F = \begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix}$$

For $L$'s pair, $\hat x_1 = (0.25, 0.10, 1)$ and $\hat x_2 = (0.19, 0.10, 1)$: $E\hat x_1 = (0,\ 0.12,\ -0.012)$ and $\hat x_2^\top(0, 0.12, -0.012) = 0.012 - 0.012 = 0$ exactly. In pixels the epipolar line is $\ell_2 = F\tilde u_1 \propto (0,\ 1,\ -300)$, that is $v = 300$ — for a rectified rig every epipolar line is a scanline, which is the whole reason stereo rigs are rectified before matching.

*How a violation is measured.* The scalar $\tilde u_2^\top F \tilde u_1$ is an *algebraic* residual with no units, so it is converted to a **point-to-line distance in pixels** before it is thresholded:

$$d_\perp = \frac{\lvert \tilde u_2^\top F \tilde u_1 \rvert}{\sqrt{\ell_1^2 + \ell_2^2}}, \qquad \ell = F\tilde u_1$$

A candidate at $(434, 303)$ instead of $(434, 300)$ gives an algebraic residual of $6\times10^{-4}$ and $d_\perp = 3.0$ px, which is the vertical offset, as it must be for a horizontal line. That conversion is why RANSAC thresholds in these papers are quoted in pixels.

*Non-example, and it is the dangerous one.* A match at $(440, 300)$ — the same row, one repeated panel over — has an epipolar residual of **exactly zero**. It passes $F$, it passes RANSAC, and it triangulates to $(0.60, 0.24, 2.40)$ m instead of $(0.50, 0.20, 2.00)$ m: $40$ cm too far. The epipolar constraint cannot catch a correspondence error *along* the epipolar line, and on repeated structure that is precisely the error you get. This is the §2.5 warning and the §4 ICP warning in one number.

**Triangulation, stated completely.** Given two known camera matrices $P_1, P_2$ (each $3\times4$, $P_i = K_i[R_i \mid t_i]$) and a corresponding pair $\tilde u_1, \tilde u_2$, triangulation returns the 3D point $\tilde X$ that both rays pass through. Because measurement noise means they generally do **not** intersect, it is a least-squares problem, not a construction. The standard **DLT** form stacks the two cross-product constraints $\tilde u_i \times P_i\tilde X = 0$, of which two of each three rows are independent, into $A\tilde X = 0$ with

$$A = \begin{pmatrix} u_1 P_1^{3\top} - P_1^{1\top}\\ v_1 P_1^{3\top} - P_1^{2\top}\\ u_2 P_2^{3\top} - P_2^{1\top}\\ v_2 P_2^{3\top} - P_2^{2\top}\end{pmatrix}$$

where $P_i^{j\top}$ is row $j$ of $P_i$, and $\tilde X$ is the right singular vector of $A$ for its smallest singular value, since that is the unit vector minimizing $\lVert A\tilde X\rVert$. For the rectified rig the solution collapses to closed form:

$$Z = \frac{f b}{d}, \qquad X = \frac{(u_1 - c_x)Z}{f_x}, \qquad Y = \frac{(v_1 - c_y)Z}{f_y}, \qquad d = u_1 - u_2$$

*Example:* the DLT on $L$'s pair returns $(0.5, 0.2, 2.0)$ m, identical to the closed form, because the rig is noiseless and rectified. *Why the $Z^2$ law:* differentiating $Z = fb/d$ gives $\partial Z/\partial d = -fb/d^2 = -Z^2/(fb)$, so one pixel of disparity error is worth $Z^2/(fb)$ metres — $0.056$ m at $Z = 2$ and $0.889$ m at $Z = 8$, sixteen times more for four times the range. *Non-example (degeneracy):* as the baseline shrinks toward zero, or as the point recedes, $d \to 0$ and the two rays become parallel, so $A$ loses rank and $Z$ is unconstrained. "Triangulation failed" in a paper almost always means this, not a solver bug.

### 2.7 From 2D–3D matches to a pose: PnP

*In one sentence:* when every match pairs a pixel with a point already known on the object, one calibrated image gives the object's pose in metres, but three points leave several answers and four can still be weak in tilt.

**The problem.** To put a tool on a known thing — §5's target, a part, S1's facade panel — a robot needs its pose in metres from one image. §2.6 paired pixels with pixels and recovered motion only up to scale; here one side of each match is a known model point, which fixes the metres. This section adds a fourth target corner to the frozen rig, $D=(0.5,\ 0.4,\ 2)$ m, which completes the rectangle the other three imply: $B-A=(0.5,0,0)$ and $C-A=(0,0.4,0)$ are perpendicular and $A+(B-A)+(C-A)=D$. Camera 1 sees the corners at

$$A\to(320,\,240),\qquad B\to(470,\,240),\qquad C\to(320,\,360),\qquad D\to(470,\,360)\ \text{px}$$

since each is $u=600X/2+320$, $v=600Y/2+240$ by §1.

> **Perspective-n-Point (PnP), defined.** **PnP** is an *estimation problem*: find the rigid transform that places a known object in the camera's frame from one image of it. Five conditions define it, and dropping one gives a different problem. The object's **points are known in its own frame**, $X_j$, from a model or a printed target. Each point's **pixel $\tilde u_j$ is given**; finding matches is §2.5's job. The camera is **calibrated**: $K$ and distortion are known (§1). The unknown is **one pose**, $R\in SO(3)$ and $t\in\mathbb R^3$, with no free scale because the model is in metres. And there are **enough points**: three non-collinear points leave finitely many poses, and four coplanar points, no three on a line, leave one when the pixels are exact.
>
> $$(\hat R,\hat t)=\arg\min_{R\in SO(3),\ t\in\mathbb R^3}\ \sum_{j=1}^{n}\big\lVert\,\tilde u_j-\pi\big(K,\ RX_j+t\big)\big\rVert^2$$
>
> where $\pi$ takes a camera-frame point to pixels as in §1, distortion included, and each term is §5's squared reprojection error, so the minimizer is the maximum-likelihood pose under isotropic Gaussian pixel noise.
>
> - **Example**: the four corners above, with $X_j$ in a target frame at $A$ whose axes are the camera's. The minimum is $R=I$, $t=(0,0,2)$ m, residual zero: the $T_{c_1t}$ of §5's hand–eye example.
> - **Non-example**: reading $t$ as the camera's position. It is where the target sits in the camera's frame; the camera sits at $-R^\top t=(0,0,-2)$ m in the target's frame, §1's extrinsics trap.
> - **Non-example**: §2.6's two-view problem, where both sides of a match are pixels and no model fixes the metres.
> - **Why it matters**: every use at the end of this section — hand–eye calibration, grasping, S1's panel — runs this minimization.

**Three points: P3P has several answers.** Each known point lies somewhere on its pixel's ray, so three points leave three unknown distances, and the three side lengths give three equations, a law of cosines per pair of rays. Eliminating two distances leaves a quartic: up to four solutions, as Persson and Nordberg state (ECCV 2018). Geometrically, the ray through $C$ cuts the sphere of radius $|AC|$ around $A$ twice, and likewise for $B$. On the rig, P3P on $A$, $B$, $C$ returns three poses that all reproject those corners exactly: the truth; the target tilted $22.62°$ about edge $AB$ ($\tan=5/12$), with $C$ slid along its ray to $(0,\ 0.369,\ 1.846)$ m, still $0.4$ m from $A$ and $0.640$ m from $B$; and the target tilted $28.07°$ about $AC$ ($\tan=8/15$), with $B$ at $(0.441,\ 0,\ 1.765)$ m.

**The fourth point, or a prior, picks one.** P3P never used $D$, so $D$ is a free test: the truth puts it at $(470,\ 360)$, where it is seen, and the impostors at $(482.5,\ 360)$ and $(470,\ 376)$, $12.5$ and $16.0$ px away. A prior works too: the target's rough place in the base frame, through the encoders and §5's hand–eye transform, predicts its tilt within degrees and rules out both. Why three, not four? The camera lies on the cylinder through $A$, $B$, $C$ perpendicular to their plane: their circle has $BC$ as diameter, radius $0.320$ m, and passes through $A$, straight ahead of the camera. On this *danger cylinder*, long tied to P3P's instability, the true pose is a double root, leaving three solutions (Wang, Hu and Zhang, 2019). It shows here: move $A$'s detection $0.1$ px left and the true root vanishes, leaving only the impostors; $0.1$ px right and it splits into poses that put $A$ at $1.987$ and $2.013$ m. P3P proposes; it does not measure.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="P3P on the wrist rig: left, a side view in which the ray through corner C meets the 0.4 m sphere around A at C and at C prime, so a target tilted 22.6 degrees about AB fits A, B and C; right, the image, where D lands at 482.5, 360 or 470, 376 pixels under the two impostor poses instead of 470, 360">
  <text x="16" y="20" font-size="12" fill="currentColor" font-weight="600">side view of the plane X = 0, to scale</text>
  <text x="300" y="20" font-size="12" fill="currentColor" font-weight="600">the image, px, to scale</text>
  <line x1="16.0" y1="48.0" x2="270.0" y2="48.0" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <line x1="16.0" y1="168.0" x2="268.0" y2="218.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <path d="M265.4 200.2 A160.0 160.0 0 0 1 97.1 155.1" fill="none" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="216.0" y1="48.0" x2="216.0" y2="208.0" stroke="currentColor" stroke-width="2.2"/>
  <line x1="216.0" y1="48.0" x2="154.5" y2="195.7" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <path d="M216.0 88.0 A40 40 0 0 1 200.6 84.9" fill="none" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="216.0" cy="48.0" r="3.6" fill="currentColor" stroke="none"/>
  <circle cx="216.0" cy="208.0" r="3.6" fill="currentColor" stroke="none"/>
  <circle cx="154.5" cy="195.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="223.0" y="44.0" font-size="12" fill="currentColor">A</text>
  <text x="222.0" y="199.0" font-size="12" fill="currentColor">C</text>
  <text x="146.5" y="185.7" font-size="12" fill="currentColor" text-anchor="end">C′</text>
  <text x="221.0" y="84.0" font-size="11" fill="currentColor">22.6°</text>
  <text x="222.0" y="132.0" font-size="11" fill="currentColor">0.4 m</text>
  <text x="177.2" y="125.8" font-size="11" fill="currentColor" text-anchor="end">0.4 m</text>
  <text x="103.1" y="140.1" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">points 0.4 m from A</text>
  <text x="16" y="272" font-size="11" fill="currentColor" fill-opacity="0.9">solid: true target · dashed: tilted 22.6° about AB</text>
  <text x="16" y="288" font-size="11" fill="currentColor" fill-opacity="0.8">the camera is 2 m to the left, on the ray through A</text>
  <path d="M311.0 55.5 L476.0 55.5 L476.0 187.5 L311.0 187.5 Z" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="311.0" cy="55.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="476.0" cy="55.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="311.0" cy="187.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="476.0" cy="187.5" r="3.4" fill="currentColor" stroke="none"/>
  <line x1="476.0" y1="187.5" x2="489.8" y2="187.5" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="489.8" cy="187.5" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="476.0" y1="187.5" x2="476.0" y2="205.1" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="476.0" cy="205.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="317.0" y="71.5" font-size="11" fill="currentColor">A (320, 240)</text>
  <text x="470.0" y="71.5" font-size="11" fill="currentColor" text-anchor="end">B (470, 240)</text>
  <text x="317.0" y="179.5" font-size="11" fill="currentColor">C (320, 360)</text>
  <text x="470.0" y="179.5" font-size="11" fill="currentColor" text-anchor="end">D (470, 360)</text>
  <text x="495.8" y="181.5" font-size="11" fill="currentColor">12.5 px</text>
  <text x="484.0" y="215.1" font-size="11" fill="currentColor">16.0 px</text>
  <text x="300" y="240" font-size="11" fill="currentColor" fill-opacity="0.9">● where seen · ○ D under the two impostors</text>
  <text x="300" y="256" font-size="11" fill="currentColor" fill-opacity="0.9">A, B, C are the same under all three poses</text>
</svg>

Left, the plane $X=0$ seen from the side, to scale: the ray through $C$'s pixel meets the sphere of radius $0.4$ m around $A$ at $C$ and at $C'=(0,\ 0.369,\ 1.846)$ m, so a target tilted $22.6°$ about $AB$ also fits $A$, $B$ and $C$. Right, the image: under that impostor $D$ lands $12.5$ px from its detection, and $16.0$ px under the one tilted $28.1°$ about $AC$.

**Four or more points: minimize the reprojection error.** With $n\ge4$ the objective is nonlinear least squares in six unknowns with $2n$ residuals, solved by Gauss–Newton or Levenberg–Marquardt ([[02-foundations/optimization|4. Optimization §3.5]]), the rotation updated as $R\leftarrow\operatorname{Exp}(\delta\omega)R$ so it stays a rotation ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §2]]). Being local, it starts from a P3P hypothesis or, for a planar target, the homography below. The listing starts it $10.4°$ and $0.55$ m off; the RMS reprojection error falls from $49.4$ px to $18$, $1.25$, $0.0073$ and $3\times10^{-7}$ px in four steps, at $R=I$, $t=(0,0,2)$ m.

**How good is one view?** Linearized at the solution, with $J$ the $8\times6$ Jacobian of the pixels in the pose and independent pixel noise $\sigma$, the pose covariance is $\sigma^2(J^\top J)^{-1}$. At $\sigma=1$ px the listing gives the target's distance to $\pm13.2$ mm, its roll about the line of sight to $\pm0.37°$, and each tilt to only $\pm2.70°$. Each has its lever. Distance comes from apparent size: a pixel of the $150$ px width is $Z^2/(f\ell)=13.3$ mm, §6's known length. Roll comes from the edges' direction: a pixel across $150$ px is $0.38°$. Tilt comes only from how the image departs from a scaled rectangle: a $10°$ tilt makes the near edge just $5.2$ px longer than the far one, $fWH\sin\theta/Z^2$ with $fWH/Z^2=30$ px per radian. At the $0.5$ px marker noise that [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] freezes, every number halves.

The listing runs the loop, the covariance and the check on P3P's impostors:

```python
import numpy as np

f, c = 600.0, np.array([320.0, 240.0])               # the rig's focal length and principal point (px)
X = np.array([0, 0, 0, 0.5, 0, 0, 0, 0.4, 0, 0.5, 0.4, 0]).reshape(4, 3)  # A, B, C, D in a target frame at A (m)

def hat(w):                                          # the matrix of w x (.)
    return np.array([0, -w[2], w[1], w[2], 0, -w[0], -w[1], w[0], 0]).reshape(3, 3)

def exp_so3(w):                                      # rotation vector -> rotation matrix (Rodrigues)
    th = np.linalg.norm(w)
    k = hat(np.asarray(w) / th) if th > 0 else np.zeros((3, 3))
    return np.eye(3) + np.sin(th) * k + (1 - np.cos(th)) * k @ k

def project(R, t):                                   # pixels of the corners, and their camera coordinates
    p = X @ R.T + t
    return f * p[:, :2] / p[:, 2:] + c, p

def jacobian(R, t):                                  # d pixels / d (rotation, translation): 8 x 6
    _, p = project(R, t)
    rows = [f / z * np.array([1, 0, -x / z, 0, 1, -y / z]).reshape(2, 3) @ np.hstack([-hat(q), np.eye(3)])
            for (x, y, z), q in zip(p, X @ R.T)]
    return np.vstack(rows)

def pnp(uv, R, t, steps=6):                          # Gauss-Newton on the reprojection error
    for k in range(steps):
        r = (uv - project(R, t)[0]).ravel()
        print("step %d: rms %.3g px" % (k, np.sqrt(np.mean(r**2) * 2)))
        J = jacobian(R, t)
        d = np.linalg.solve(J.T @ J, J.T @ r)
        R, t = exp_so3(d[:3]) @ R, t + d[3:]
    return R, t

uv = project(np.eye(3), np.array([0, 0, 2.0]))[0]    # where camera 1 sees A, B, C, D
print(uv.tolist())
R, t = pnp(uv, exp_so3(np.radians([6, -8, 3])), np.array([0.2, -0.1, 2.5]))
print("R = I:", np.allclose(R, np.eye(3)), " t =", np.round(t, 6) + 0.0)

# 1 px of independent noise on every coordinate: pose covariance (J^T J)^-1
J = jacobian(R, t)
S = np.linalg.inv(J.T @ J)
m = R @ [0.25, 0.2, 0] + t                           # the rectangle's centre, camera frame
g = m / np.linalg.norm(m) @ np.hstack([-hat(R @ [0.25, 0.2, 0]), np.eye(3)])
print("distance %.1f mm | tilt %.2f, %.2f deg | roll %.2f deg"
      % (np.sqrt(g @ S @ g) * 1e3, *np.degrees(np.sqrt(np.diag(S)[:3]))))

# P3P's two extra poses: tilted about AB (tan 5/12) and about AC (tan 8/15)
for edge, w in (("AB", [-np.arctan2(5, 12), 0, 0]), ("AC", [0, np.arctan2(8, 15), 0])):
    q = project(exp_so3(w), np.array([0, 0, 2.0]))[0]
    print("tilted about %s: A, B, C at %s px; D at %s, %.1f px from its detection"
          % (edge, np.round(q[:3], 6).tolist(), np.round(q[3], 6).tolist(), np.linalg.norm(q[3] - uv[3])))
```

**PnP inside RANSAC.** Matches from §2.5 between an image and a 3D model — mapped landmarks, a part's features — contain outliers. So PnP runs inside RANSAC: draw three matches, solve P3P, score each pose by the matches it reprojects within a pixel threshold, and refine the best on its inliers. The minimal sample keeps it cheap: at half the matches inliers and $99\%$ confidence, [[02-foundations/algorithms/robotics-ai-problems|11.8 §3]]'s count is $35$ samples of three, $72$ of four, and $293$ of the six a linear solve for a general $3\times4$ camera matrix needs (eleven unknowns, two equations per point).

**Planar targets: the homography route.** When every point lies on one plane, put the target frame on it, so $Z_t=0$ and the third column of $R$ drops out:

$$\lambda\begin{pmatrix}u\\v\\1\end{pmatrix}=K\,[\,r_1\ \ r_2\ \ t\,]\begin{pmatrix}X_t\\Y_t\\1\end{pmatrix}=H\begin{pmatrix}X_t\\Y_t\\1\end{pmatrix}$$

so the plane maps to the image by a $3\times3$ homography $H$, which four points with no three on a line fix (eight unknowns after scale, two equations each). Then $[\,r_1\ r_2\ t\,]=\lambda K^{-1}H$ with $\lambda=1/\lVert K^{-1}h_1\rVert$, because $r_1$ is a unit vector, and $r_3=r_1\times r_2$. On the rig $H=\begin{pmatrix}300&0&320\\0&300&240\\0&0&1\end{pmatrix}$ and $K^{-1}H=\operatorname{diag}(0.5,\ 0.5,\ 1)$, so $\lambda=2$, $r_1=(1,0,0)$, $r_2=(0,1,0)$, $t=(0,0,2)$ m: the same pose in closed form. With noisy corners, $r_1$ and $r_2$ come out slightly non-orthonormal, so the rotation is projected onto $SO(3)$ and used to start the refinement.

**Small, distant markers flip.** The tilt lever shrinks faster than the marker. A $0.1$ m square at the target's centre spans $30$ px, and a $10°$ tilt changes its edges by $0.26$ px. Its reprojection error has two distinct local minima (Schweighofer and Pinz, 2006). Tilted $20°$ about its vertical axis, the marker faces the camera $14.0°$ off its line of sight; a second pose $13.5°$ off on the other side, $27.5°$ from the truth, reprojects its corners to $0.18$ px RMS. A pixel of noise can pick either, so the answer can jump between frames. The cures are geometric: a larger target, a closer camera, markers spread apart, or a prior that excludes one side.

**Fiducial markers: AprilTag.** A fiducial solves correspondence by design. AprilTag (Olson, ICRA 2011; AprilTag 2, Wang and Olson, IROS 2016) prints a black-and-white square encoding only 4 to 12 bits; its project page credits that small payload with detection more robust and longer-range than a QR code's, and its output — the tag's precise 3D position, orientation and identity relative to the camera — is PnP on the four corners, with the printed side length as the model, so a wrong size scales the distance by the same factor. It also inherits the flip. The anchor paper of the wiki's construction-assembly lineage put two tags on every block ([[01-canonical-papers/notes/8-construction/vision-guided-assembly|Feng et al. 2015]]).

**Where PnP is used.** Hand–eye calibration measures $T_{c_it}$ at every robot pose by PnP (§5), so the $\pm2.70°$ tilt noise enters $B$ in $AX=XB$, one reason that solve averages many poses. Grasping a known part is PnP between its model's points and their detections, then §3's frame chain. Aligning the tool to S1's facade panel ([[05-construction-robotics/site-engineering|2.5]]) is the same problem with the panel as the target; for a target the rig's size at $2$ m and $1$ px of corner noise, one camera promises $\pm2.2$ mm across the line of sight and $\pm13$ mm along it, against S1's $\pm5$ mm.

### 3. Point clouds and frames

A depth image plus intrinsics back-projects to a **point cloud**:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. Every cloud lives in some frame — sensor, base,
map — and multi-sensor pipelines stand or fall on the **extrinsic calibration** between
those frames ([[04-robotics/robot-systems-deployment|the TF tree at runtime]]). A
plausible-looking cloud in the wrong frame produces systematic, learning-resistant errors.

**How dense, and why the grid is worth keeping.** One $640\times480$ depth image gives at most $307{,}200$ points, one per pixel with a valid depth. Neighbouring pixels land $Z/f$ apart on a surface facing the camera, $3.3$ mm at the landmark's $2$ m and $13.3$ mm at $8$ m, so the same scene is sampled four times more coarsely at four times the range, and ICP (§4) finds fewer and noisier correspondences on far surfaces. A cloud that keeps the image grid is called **organized**: a point's neighbours are found by pixel index rather than by a spatial search, which makes the normals that point-to-plane ICP needs cheap to estimate.

**The frame, worked on the rig.** $L=(0.5,\ 0.2,\ 2.0)$ m is a camera-frame coordinate. The arm plans in the tool frame, and §5's hand–eye transform for this rig, $X=\big(I,\ (0,0,-0.04)\big)$, moves it there: $p^{g}=R_Xp^{c}+t_X=(0.5,\ 0.2,\ 1.96)$ m. One link further, the base frame is $p^{b}=T_{bg}\,X\,p^{c}$, with $T_{bg}$ from P2's joint encoders, the same chain §5 writes for the target. Two kinds of frame error follow, and they behave differently. Skip $X$, treating camera coordinates as tool coordinates, and every point in the cloud is off by the same $4$ cm along the tool axis at every range: a bias that no amount of training data averages away, which is what "learning-resistant" means in practice. Get the rotation of $X$ wrong by $1^\circ$ instead, and a point moves by $2\sin(0.5^\circ)=1.75$ cm per metre of its distance from the rotation axis: $L$, $2.06$ m from the camera's $y$ axis, moves $3.6$ cm, and a point $0.5$ m from it moves under $1$ cm. A translation error is constant; a rotation error grows with range.

**A frame is also a time.** A cloud captured while the arm moves belongs to the camera pose at the instant of capture. Pair it with the arm's pose from another instant and the whole cloud lands in the wrong frame by the distance the camera moved in between, $3$ mm for a camera moving at $0.10$ m/s and a $30$ ms mismatch. Which transform is looked up for which time stamp is the TF tree of [[04-robotics/robot-systems-deployment|10. Robot Systems §4]]; which calibration fixes $X$ is §5. When a point-cloud paper quotes millimetres, ask in which frame, and whether the extrinsic and the time stamp that put the cloud there were estimated or assumed. On a moving base every millisecond of a wrong stamp is a distance, $v\,\Delta t$, and [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §9]] prices it for each sensor of the rig.

### 4. Registration and ICP

**Registration** aligns two geometries: a scan with another scan, a point cloud with a part model, or a site scan with BIM. The unknown is a rigid transform $T\in SE(3)$. Before optimizing it, ask which points are supposed to represent the same surface.

**ICP** (iterative closest point) alternates two problems: match points under the current transform, then update the transform while holding those matches fixed. For ordinary rigid **point-to-point** least squares, the fixed-correspondence update has a closed-form SVD solution. **Point-to-plane** variants commonly use linearized least squares. Gauss–Newton or Levenberg–Marquardt is therefore not a defining requirement of every ICP update ([[02-foundations/optimization|4. Optimization §3.5]]).

Imagine aligning a scan of one wall panel to a model containing several similar panels. A bad initial transform may match the scan to the neighboring panel. Even an exact least-squares solution for those matches can reinforce the wrong alignment. **This is why ICP is local:** correspondence selection and pose depend on each other, and alternating improvements do not search every assignment. Use an initial estimate from odometry or global matching and inspect overlap and outliers. See the [MIT geometric pose-estimation derivation](https://manipulation.mit.edu/pose.html).

**The ICP objective, stated completely.** ICP is an **alternating minimization** of one cost over two unknowns: a rigid transform $T = (R, t)$ with $R \in SO(3)$, and a correspondence map $c$ that sends each source point to a target point. Given source points $\{p_i\}$ and target points $\{q_j\}$, the two half-steps are

$$c(i) \leftarrow \arg\min_j \lVert Rp_i + t - q_j \rVert \quad\text{(match)}, \qquad (R,t) \leftarrow \arg\min_{R,t} \sum_i \lVert Rp_i + t - q_{c(i)} \rVert^2 \quad\text{(solve)}$$

Each half-step can only lower the cost, so the loop converges — but it converges to a **local** minimum, because the match step is a discrete choice that the solve step never revisits. That is the precise content of "ICP is local". The solve step has a closed form: centre both sets, take the SVD of the cross-covariance $H = \sum_i (p_i - \bar p)(q_{c(i)} - \bar q)^\top$, set $R = V\operatorname{diag}(1,1,\det(VU^\top))U^\top$ and $t = \bar q - R\bar p$, where the $\det$ term forces a rotation rather than a reflection.

**The point-to-plane variant, stated completely.** When the target is a sampled *surface*, the nearest target point is almost never the true corresponding point — it is just the nearest sample. Point-to-plane therefore measures the residual **along the target's surface normal** $n_{c(i)}$ only, so a source point is free to slide within the tangent plane at no cost:

$$\min_{R,t} \sum_i \big((Rp_i + t - q_{c(i)})^\top n_{c(i)}\big)^2$$

It converges in far fewer iterations on smooth surfaces, because sliding is exactly the motion the point-to-point cost wrongly penalizes. The price is that the freedom is real: if the normals do not span, the cost has a flat direction.

> [!example] Worked example · 계산 예제 — the degeneracy in numbers
> **A wall.** Target plane $y = 0$ with normal $n = (0,1)$; three scan points at $(0,\ 0.05)$, $(1,\ 0.05)$, $(2,\ 0.05)$, so the scan sits $5$ cm off the model. For a pure translation $t = (t_x, t_y)$ the point-to-plane residual of every point is $(t_y + 0.05)$, and the cost is $3(t_y + 0.05)^2$. It is **zero for $t = (0, -0.05)$, for $t = (-0.30, -0.05)$ and for $t = (+0.75, -0.05)$ alike** — $t_x$ does not appear in the cost at all. A $30$ cm along-wall error therefore has an exactly zero residual, which is what "a small residual does not prove the pose" means arithmetically.
>
> **A corner fixes it.** Add a second face, $x = 0$ with normal $(1,0)$, and two scan points at $(0.05,\ 0)$ and $(0.05,\ 1)$. Now the cost at $t = (0, -0.05)$ is $2(0.05)^2 = 0.005$, at $t = (-0.05, -0.05)$ it is $0$, and at $t = (-0.30, -0.05)$ it is $2(0.05-0.30)^2 = 0.125$. Two non-parallel normals are enough to pin a planar translation, so **degeneracy is a property of the normals the scan contains**, not of walls.
>
> **Point-to-point on the same wall, with correct correspondences,** recovers the full transform: with $q_i = p_i + (0.30, 0.05)$ the SVD solve returns $R = I$ and $t = (0.30, 0.05)$ exactly. The catch is that ICP does not *have* the correct correspondences — nearest-point matching on a featureless plane returns the foot of the perpendicular, which slides with $t_x$ and reproduces the same degeneracy.

Degeneracy depends on the measured geometry and objective. Point-to-plane residuals on a featureless planar patch cannot constrain translation along the plane or rotation about its normal. Distinct boundaries or point correspondences can supply additional information. Thus “a wall is degenerate” is shorthand for an insufficient measurement model, not a universal statement about every wall scan.

> [!question] Check the correspondence · 대응점 확인
> Does a small ICP residual prove the pose is correct? **Answer:** no. Repeated panels may fit well at the wrong location. Check initialization, independent landmarks and the unconstrained directions, not only the final residual.

### 5. Calibration

| Calibration | What it estimates | Typical method |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, distortion | checkerboard/target views |
| Camera–camera (stereo) | relative $SE(3)$ + rectification | shared target views |
| Camera–LiDAR | extrinsic $SE(3)$ | target or mutual-feature alignment |
| Hand–eye (camera–robot) | sensor-to-end-effector or base transform | robot motion + target ($AX=XB$) |
| Temporal | clock offset / latency between sensors | correlation of motion signals |

The camera–LiDAR row, worked on this rig with a LiDAR on the mast — its extrinsic, what a $1^\circ$ error does in pixels and in millimetres, and the check that tells rotation, translation and time apart — is [[04-robotics/perception-sensors-rigs|3.6 Perception Sensors §8]]. Every row assumes the mount does not move between calibration and use; a bracket that bends or rings breaks that, and sizing one by its tilt at the target is [[02-foundations/tools/mechanical-design-fabrication|12.9 Mechanical Design and Fabrication §6]].

**The hand–eye equation, derived.** A wrist-mounted camera looks at a calibration target that stays put while the arm moves. Write $T_{ab}$ for the transform that takes coordinates in frame $b$ to frame $a$, $p^a = T_{ab}p^b$, as §1's $T_{cw}$ does ([[02-foundations/se3-geometry|8. 3D Geometry & SE(3) §3]]), with $b$ the robot base, $g$ the gripper, $c$ the camera and $t$ the target. At robot pose $i$, one chain of three transforms reaches the target from the base: the gripper pose $T_{bg_i}$ from the joint encoders, the unknown camera-to-gripper mount $X = T_{gc}$, which never changes, and the target pose $T_{c_it}$ that the camera measures (by PnP, from the target's known corners and their pixels). The target has not moved, so the chains at two robot poses $1$ and $2$ end at the same transform:
$$T_{bg_1}\,X\,T_{c_1t} = T_{bt} = T_{bg_2}\,X\,T_{c_2t}$$
Multiply on the left by $T_{bg_2}^{-1}$ and on the right by $T_{c_1t}^{-1}$, and the unknown target pose drops out:
$$AX = XB, \qquad A = T_{bg_2}^{-1}T_{bg_1}, \qquad B = T_{c_2t}\,T_{c_1t}^{-1}$$
$A$ is the gripper's motion between the two poses, known from the encoders, and $B$ is the camera's motion between the same poses, measured from the target. Both sides are one transform, the camera at pose 1 seen from the gripper at pose 2, reached along two routes: move the gripper and then step to the camera, or step to the camera and then move it. Splitting $AX = XB$ into its rotation and translation blocks shows what one motion can and cannot tell you:
$$R_AR_X = R_XR_B, \qquad (R_A - I)\,t_X = R_Xt_B - t_A$$
The mount's translation $t_X$, the block that holds $d_{ct}$, enters only through $R_A - I$. A motion without rotation leaves it out entirely, and a rotation about one axis leaves out its component along that axis, because $R_A - I$ sends the rotation axis to zero. So several motions with different rotation axes are needed to pin $X$ down.

*Example, on the rig.* Write a transform as (rotation, translation). Put the gripper frame at P2's tool tip with its axes parallel to the camera's, so $X = \big(I,\ (0, 0, -0.04)\big)$: the camera sits $d_{ct}$ behind the tip on the tool axis. Put the target frame at the target corner $(0, 0, 2)$, so $T_{c_1t} = \big(I,\ (0, 0, 2)\big)$. P2 turns its gripper through the tool tip about the camera's $y$ axis, which is the joint-axis direction since P2 is planar, by the angle with $\cos\theta = 0.96$ and $\sin\theta = 0.28$ ($16.26°$). The encoders give $A = \big(R_y(-\theta),\ 0\big)$, with $R_y$ the rotation about $y$ and a minus sign because $A$ re-expresses the old gripper frame in the new one. The camera, $4$ cm behind the pivot, swings: the target now measures $T_{c_2t} = \big(R_y(-\theta),\ (-0.5488, 0, 1.9216)\big)$, so the three target corners appear at $(148.6, 240)$, $(300.0, 240)$ and $(148.6, 364.9)$ px, all still in the image. Then the camera's motion is $B = \big(R_y(-\theta),\ (0.0112, 0, 0.0016)\big)$, and the two routes agree:
$$AX = XB = \big(R_y(-\theta),\ (0.0112,\ 0,\ -0.0384)\big)$$
because $R_y(-\theta)(0, 0, -0.04) = (0.0112, 0, -0.0384)$ on the left and $(0, 0, -0.04) + (0.0112, 0, 0.0016)$ is the same vector on the right. *Non-example:* assume the camera sits at the tip, $X = I$. Then $AX$ has no translation while $XB$ keeps $(0.0112, 0, 0.0016)$, a mismatch of $11.3$ mm, the chord $2d_{ct}\sin(\theta/2)$ the camera swept. That is how one rotation exposes the $4$ cm. An offset of the same size along the joint axis, $(0, 0.04, 0)$, would leave $AX = XB$ satisfied by $X = I$ as well: a planar arm like P2, whose every rotation is about that one axis, cannot calibrate the component of the mount along it.

The quality metric is usually **reprojection error**: project the estimated 3D points
through the estimated model and measure pixel distance to their detections. Low
reprojection error on the calibration set does **not** guarantee accuracy outside the
calibrated volume, range, or temperature, because the model was fitted only at the target positions, distances and conditions actually observed; outside them it is extrapolating, not obeying a physical law.

**Reprojection error, stated completely.** For one 3D point $X_j$ seen in one view $i$, it is a **distance in pixels** between two image points: the detected feature $\tilde u_{ij}$ and the projection of $X_j$ through the current model. Writing $\pi(\cdot)$ for the full pipeline of §1 — extrinsics, perspective division, distortion, then $K$ —

$$e_{ij} = \big\lVert\, \tilde u_{ij} - \pi\big(K, d, T_i, X_j\big) \,\big\rVert_2$$

Three conditions are what make it *the* metric. It is measured **in the image**, where the noise actually is, so least squares on it is the maximum-likelihood estimate under isotropic Gaussian pixel noise ([[02-foundations/probability|3. Probability §4]] for why a Gaussian likelihood becomes squared error, [[02-foundations/optimization|4. Optimization §3]] for the solver) — an error measured in metres in 3D would be weighting a quantity the camera never observed. It is **per observation**, so every $(i,j)$ pair contributes. And it depends on **every** parameter at once: move $K$, a distortion coefficient, a pose or the point, and $e_{ij}$ moves. That is why calibration and bundle adjustment are the same optimization with different variables held fixed.

**The calibration residual, stated completely.** What a calibration tool prints is the **RMS reprojection error** over all corners in all views — one number summarizing $NM$ of the above, with $N$ views and $M$ target corners:

$$e_{\text{RMS}} = \sqrt{\frac{1}{NM}\sum_{i=1}^{N}\sum_{j=1}^{M} \big\lVert \tilde u_{ij} - \pi(K, d, T_i, X_j)\big\rVert_2^2}$$

*Example:* the three rig corners with $\hat f = 598$ give residuals $0.00$, $0.50$ and $0.40$ px, so $e_{\text{RMS}} = \sqrt{0.41/3} = 0.370$ px, and that calibration still misplaces a point $0.5$ m off-axis by $1.67$ mm, or $10.0$ mm at $3$ m off-axis. *Non-example, and the one to remember:* $e_{\text{RMS}}$ is a **training** residual. Adding $k_3$, $p_1$ and $p_2$ to a model fitted on twenty views of a target at one distance will lower it while making the extrapolation worse, exactly as an over-parameterized regression does ([[02-foundations/ml-practice|9. ML Practice §2]]). The honest checks are a held-out set of views the fit never saw, residuals plotted *by image position* (a focal error leaves nothing at the principal point and grows radially, as the table above shows), and a measurement of a known length at the working distance.

### 6. Geometric + deep perception

Modern pipelines mix the two: a network detects or segments
([[01-canonical-papers/notes/2-computer-vision/sam|SAM]]), matches features, or predicts
depth/pose; geometry turns those into metric structure and enforces consistency
(triangulation, [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]-style feed-forward
geometry, [[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3DGS]] rendering losses).
When reading, ask: *which stage is learned, which is geometric, and where does metric
scale enter?* (calibrated stereo/LiDAR, known object size, or not at all).

**Where scale enters, on the rig.** There are three places, and all three obey the same $Z^2$ law with a different baseline $B$: a measurement error $\delta$ moves the depth by about $Z^2\delta/B$, with $B=fb=72$ px·m for stereo, $B=f\ell=300$ px·m for the $0.5$ m known length, and $B=s$ for the anchors.

*Calibrated stereo* is §2's: $fb=72$ px·m gives $5.6$ cm per pixel of disparity at $2$ m.

*A known length* works the same way, with the object as the baseline. The target corners $A$ and $B$ are $0.5$ m apart and $150$ px apart in the image, so $Z=f\ell/\Delta u=600\times0.5/150=2.0$ m with $\ell=0.5$ m the known length, and one pixel of error in that separation moves the depth by $Z^2/(f\ell)=4/300=1.3$ cm, four times better than the stereo pair, because the target is a longer baseline than $b=0.12$ m.

*Alignment to anchors* is how a learned relative depth becomes metric. A network that predicts inverse depth up to scale and shift outputs $r=s/Z+t$ with $s$ and $t$ unknown, so it needs at least two pixels of known depth at different ranges. Suppose it outputs $r=0.80$ at $L$ (stereo: $Z=2.0$ m) and $r=0.35$ at the $8$ m point of §2; then $s=1.2$ and $t=0.2$, and a third pixel with $r=0.50$ is at $Z=4.0$ m. An output error of $\pm0.01$ moves that pixel between $3.87$ and $4.14$ m, and a pixel at $8$ m between $7.50$ and $8.57$ m: inverse depth stays bounded, but its errors grow with range just as stereo's do. Two anchors at the same depth fix nothing, since they give one equation in two unknowns.

**The same question for reconstructions.** A single moving camera recovers a scene only up to a similarity transform, seven numbers of which one is the scale, so a NeRF or 3DGS model fitted to poses from monocular structure-from-motion is in arbitrary units until one known length fixes it. That length can be the $0.5$ m target edge, or the arm's own motion: P2's encoders, through the hand–eye $X$ of §5, say how far the camera moved, so two images of a static scene taken before and after a sideways move of $0.12$ m are §2's stereo pair in time. The canonical notes make the same point for learned depth: [[01-canonical-papers/notes/2-computer-vision/depth-anything|Depth Anything]]'s robust relative depth still needs a metric head and scale calibration on a new site.

### 7. Reading claims and evaluations

| Paper phrase | Check before accepting it |
|---|---|
| "accurate 6-DoF pose" | error metric (ADD? rotation/translation split?), object symmetry handling, occlusion levels |
| "metric depth" | where scale comes from; evaluation range; indoor-vs-outdoor shift |
| "robust registration" | initialization protocol, degenerate-scene fraction, outlier rates |
| "calibration-free" | what is actually assumed (often: intrinsics still known) |
| "real-time reconstruction" | hardware, resolution, drift over long sequences |

> [!warning] Reading the claim · 핵심 주장 읽는 법
> Sub-pixel reprojection error and beautiful reconstructions do not by themselves mean
> the *pose is right in the robot's base frame* — that also requires correct extrinsics
> and time synchronization, which many papers hold fixed and out of scope.

### 7.5 From seeing an error to correcting it: visual servoing

Perception does not close a robot loop until an image or pose error becomes a velocity
command. **PBVS** estimates two poses, forms a pose error such as
$\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$, where $\operatorname{Log}$ is the pose logarithm of
[[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §5]] and $^\vee$ stacks its result as six numbers,
and commands a twist ([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR ch.3 §3]]) that reduces $\xi$. Its accuracy inherits calibration and pose-estimation errors. **IBVS** stays in the
image: for image features $s$, $\dot s=L_s v_c$, where the image Jacobian $L_s$ depends on
feature depth; a local law such as $v_c=-\lambda L_s^+(s-s^*)$ reduces pixel error. IBVS can
be less sensitive to full pose reconstruction but still needs depth estimates and a
well-conditioned feature geometry. Neither equation alone guarantees visibility, actuator
limits, global convergence, or collision avoidance. Read a "closed-loop perception" claim
by identifying the error, Jacobian, control rate, depth source, and recovery outside the
local basin.

**Worked on the rig: IBVS on one point.** Take the landmark's pixel $(470,300)$ as the current feature and the principal point as the goal, so the error in normalized coordinates is $e=(0.25,\ 0.10)$. For a camera that only translates parallel to the image, the two relevant columns of $L_s$ carry $-1/Z$ on the diagonal, and the law $v_c=-\lambda L_s^+e$ becomes $v_c=\lambda\hat Z e$: with $\lambda=0.5\ \mathrm{s^{-1}}$ and $\hat Z=2.0$ m it commands $(0.25,\ 0.10)$ m/s, and the error decays as $e^{-\lambda t}$, to $5\%$ after $6$ s. A depth estimate of $1.0$ m instead of $2.0$ m halves the rate to $0.25\ \mathrm{s^{-1}}$ without breaking convergence. In the full six-column matrix depth appears only in the translation columns, so a wrong $\hat Z$ also shifts the split between translating and rotating, and the path bends.

**Why IBVS is called robust to calibration.** If the goal image $s^*$ was recorded with the camera at the goal, IBVS converges to that image, and to that pose when the features pin the pose down: four or more points in general position do, three allow up to four poses, and the single point of the example above leaves four of the six degrees of freedom free. Focal-length and hand–eye errors change the path and the speed, as long as the loop still converges, but not the end point. PBVS computes its error through the calibrated model, so the error survives convergence. With the Worked case's $\hat f=598$ px, a PBVS loop told to hold the $0.5$ m target edge at $2.0$ m reads that depth as $\hat f\cdot0.5/\Delta u$, stops where $\Delta u=149.5$ px, and is then truly at $2.0067$ m, $6.7$ mm too far even after it has converged. Assume $X=I$ instead of the $4$ cm offset, and a PBVS tool goal lands $4$ cm off along the tool axis.

**The gain is a bandwidth, so delay bounds it.** The closed loop $\dot e=-\lambda e$ comes from the open loop $L(s)=\lambda/s$, an integrator with crossover at $\lambda$ and a $90^\circ$ phase margin, and a delay $\tau$ spends $\lambda\tau$ radians of that margin. At the $70$ ms camera-to-force budget of **P6** ([[02-foundations/lab-plants|0.6]]) that is $2^\circ$ at $\lambda=0.5\ \mathrm{s^{-1}}$ and $40^\circ$ at $\lambda=10\ \mathrm{s^{-1}}$, leaving $50^\circ$, and the loop goes unstable near $\lambda=\pi/(2\tau)=22.4\ \mathrm{s^{-1}}$. The general form is the delay budget of [[04-robotics/control-theory-ce397|5. Control Theory §5.5]].

### After reading

- Project a 3D point through a pinhole model by hand.
- Distinguish intrinsics from extrinsics and say when each changes.
- Explain why monocular vision loses scale and where scale re-enters.
- Explain ICP's loop and why it needs initialization.
- Name the calibrations a camera+LiDAR+arm system needs.
- Interpret reprojection error without over-trusting it.
- Distinguish PBVS from IBVS and identify where pose, calibration, depth and the image Jacobian enter the loop.
- Explain why corners, not edges, are matched, and filter matches with the ratio test, a mutual check and RANSAC.
- Name all five entries of $K$, say which are properties of the sensor and which of the lens, and apply distortion in the right order.
- Write the epipolar constraint with $E$ and with $F$, convert an algebraic residual to a pixel distance, and say what the constraint cannot catch.
- Triangulate a rectified pair, and state the range at which its $Z^2$ error law makes the answer useless.
- Recover a pose from four known corners by PnP, say why three corners can leave up to four poses and what picks one, and explain why a small marker's tilt is its weakest number.
- Write the point-to-point and point-to-plane ICP objectives and show a case where the second has a flat direction.
- Read an RMS reprojection error as a training residual rather than an accuracy.

> [!tip] Going deeper · 더 깊이
> Szeliski's [*Computer Vision: Algorithms and Applications*](https://szeliski.org/Book/) is free and covers this page's whole span; when you need multi-view geometry stated as theorems — essential and fundamental matrices, triangulation, bundle adjustment — Hartley and Zisserman's *Multiple View Geometry in Computer Vision* is the reference the field cites.

### Self-check

1. With the worked intrinsics, where does $p^{c}=(-0.3, 0.1, 1.5)$ project?
2. Stereo at $f=600$, $b=0.12$: what disparity corresponds to $Z=24$ m, and why is that a problem?
3. Why can ICP fail in a long empty corridor even with perfect data?
4. A paper fuses LiDAR and camera "without calibration" — what is it most likely still assuming?
5. A window has $\sum I_x^2=40$, $\sum I_y^2=2$ and $\sum I_xI_y=0$. With $k=0.05$, what are the Harris response and the Shi–Tomasi score, and what kind of point is it?
6. On a wall of identical panels, an ORB descriptor's nearest candidate is 32 bits away and the second is 36. Does it pass a 0.8 ratio test, and what must catch a wrong match that survives the filters?
7. A calibration file reports $f_x = 600$, $f_y = 604$, $c_x = 318$, $c_y = 241$, $s = 0$ for the rig's $640\times480$ sensor. Which of these tells you something about the *sensor* rather than the lens, and which single value would make you suspect the image was cropped?
8. Using the rig's $F$, a candidate match for $\tilde u_1 = (470, 300)$ sits at $(434, 306)$. Compute the algebraic residual and the point-to-line distance in pixels. Would a match at $(452, 300)$ be rejected by the same test?
9. A calibration is refitted with $k_3$, $p_1$ and $p_2$ added, and $e_{\text{RMS}}$ drops from $0.37$ px to $0.21$ px on the same twenty views. What has been demonstrated, and what two checks would settle whether the new model is better?
10. PnP on the four corners returns $R=I$, $t=(0,0,2)$ m. Where is the camera in the target's frame? With $1$ px of noise on every corner, which does the fit recover worse, the target's distance or its tilt, and why? What changes if the target is a $0.1$ m tag at the same place?

> [!tip]- Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — a ±1 px error spans 18–36 m; long-range stereo depth is fragile.
> 3. Translation along the corridor axis barely changes point-to-nearest-point distances — a degenerate (unobservable) direction.
> 4. Known intrinsics, and usually a rough extrinsic initialization or joint optimization that still needs overlap and synchronized timestamps.
> 5. The eigenvalues are 40 and 2, so $R=80-0.05\cdot42^2=-8.2<0$ and $\min\lambda=2$. It is an edge: intensity changes along $x$ only, so the point is poorly located along the edge direction $y$.
> 6. No: $32/36=0.89>0.8$, so reject it — near-equal candidates suggest the neighbouring panel. A wrong match that survives must be caught by geometric verification (RANSAC), and a set shifted by one whole panel can pass even that, so check against odometry or independent landmarks.
> 7. $f_x \ne f_y$ and $s$ are sensor facts: unequal focal lengths in pixels mean non-square pixels, and $s=0$ means the pixel axes are perpendicular. The focal length itself is the lens. $c_x = 318$ is unremarkable, but $c_y = 241$ against an image height of 480 means the principal point sits $1$ px *below* centre while $c_x$ sits $2$ px left of $320$ — both normal. The value that would signal a crop is a principal point far from $(w/2, h/2)$, for instance $c_x = 240$ on a $640$-wide image, which says the array you calibrated is not the array you are now projecting into.
> 8. $\ell = F\tilde u_1 \propto (0,\ 0.0002,\ -0.06)$. The algebraic residual is $0.0002(306) - 0.06 = 1.2\times10^{-3}$ and $\sqrt{\ell_1^2+\ell_2^2} = 0.0002$, so $d_\perp = 6.0$ px — the vertical offset, as it must be for a horizontal epipolar line. A match at $(452, 300)$ gives an algebraic residual of exactly $0$ and $d_\perp = 0$: it is *on* the line, so the epipolar test passes it. It is still wrong — it triangulates to $Z = 600(0.12)/18 = 4.0$ m instead of $2.0$ m. Moving along the epipolar line is invisible to $F$ and visible only in depth.
> 9. Only that a model with more free parameters fits the same data better, which is guaranteed and therefore demonstrates nothing about accuracy ([[02-foundations/ml-practice|9. ML Practice §2]]). Two checks settle it: (i) hold out views the fit never saw — ideally at a different distance and tilt — and compare $e_{\text{RMS}}$ there, not on the training views; (ii) measure a known length, or a known target-to-target distance, at the actual working range, since that is the metre the calibration is for. A third useful look is the residual map by image position: genuine distortion structure appears as a radial pattern, while noise-fitting appears as speckle.
> 10. At $-R^\top t=(0,0,-2)$ m; $t$ is where the target sits in the camera's frame, not where the camera is (§1). The distance comes out to $\pm13.2$ mm because it is read from the target's apparent size, $13.3$ mm per pixel of its $150$ px width. Each tilt comes out only to $\pm2.70°$, because tilt shows only as the image's departure from a scaled rectangle, $5.2$ px for $10°$. A $0.1$ m tag spans $30$ px and a $10°$ tilt changes its edges by $0.26$ px; worse, its reprojection error has a second minimum, and at $20°$ a pose $27.5°$ away fits its corners to $0.18$ px, so the tilt is ambiguous, not merely noisy (§2.7). A larger target, several tags spread apart, or a prior fixes it.

### Problem set · 과제

Tier B. The wrist rig of the Running object, plus **P5** as a range to a wall ([[02-foundations/lab-plants|0.6]]) and the hand–eye offset $d_{ct}=4\,\mathrm{cm}$. No simulator. The Worked case ran the rig at the landmark $L$, $Z = 2.0$ m. This set moves it to $L' = (0.5,\ 0.2,\ 4.0)$ m and asks which errors grow, which shrink, and which stay put — that is the variant.

1. **Draw.** Both cameras, both rays to $L'$, the two image points and the disparity between them. Beside them, and to the same scale, the $\pm1$ px depth error bar at $Z = 4$ m and the one at $Z = 2$ m from the picture above. Add the distortion shift at $L'$ as a short segment on the image plane. Three errors, three different scaling laws — the drawing has to make them look different.
2. **Derive.** (a) Project $L'$ into both cameras: $u_1, v_1, u_2$, the disparity $d'$, and the check $Z = f b / d'$. (b) The depth error for $d' \pm 1$ px, exactly, and compare it with the first-order estimate $Z^2/(fb)$; say why the exact $+1$ and $-1$ errors are not equal. (c) The distortion shift at $L'$: compute $r$, the radial factor, and the shift in pixels, then explain the ratio to the $2.30$ px at $Z = 2$ using the leading term. (d) P5's scalar fusion: $K$, the fused camera-to-wall range, $P^+$, and the tip-to-wall number after $d_{ct}$. (e) PnP at $Z = 4$ m: move the four target corners to $(0,0,4)$, $(0.5,0,4)$, $(0,0.4,4)$ and $(0.5,0.4,4)$ m. Project them, then use §2.7's three levers to predict how the $1$ px spreads of the target's distance, roll and tilt change from $Z=2$ m.
3. **Interpret.** (a) In $AX = XB$, which of $A$, $B$, $X$ contains the $4\,\mathrm{cm}$, and why a $0.37$ px calibration residual does not certify it. (b) A match on the repeated panel at $(440, 300)$ has an epipolar residual of exactly zero. Name the one number in part 2 that would have caught it, and say what you would add to the rig to catch it in general.

> [!note]- How to draw it · 그리는 법
> - **Left, the projection in the $XZ$ plane**: optical centre $O$ at the origin, the optical axis along $+Z$, the image plane at $Z = f$, the landmark, and the ray from it through $O$ crossing the image plane.
> - **Mark the similar triangles** that give $u - c_x = f_x X / Z$: they are the derivation, so the drawing has to show both.
> - **Middle, the second camera**: an identical centre at $X = +0.12$ with its own ray to the same point; label the two image points and the disparity between them.
> - **Draw the same pair of rays for a farther point** and show them nearly parallel: the angle between the rays is what depth accuracy is actually made of.
> - **Right, the depth error bars share one axis and one scale**: a $\pm1$ px disparity error grows as $Z^2$, and the bars must be drawn that way — in the picture, $\pm0.056$ m at $2$ m and $\pm0.89$ m at $8$ m, sixteen times longer.
> - **The distortion shift goes on the image plane, not on the depth axis**, because it is a different kind of error: a bias, not a noise.

> [!tip]- Solutions
> 1. The two rays to $L'$ are visibly closer to parallel than the pair at $Z = 2$; the $Z=4$ error bar must be drawn about four times the $Z=2$ one, and the distortion segment about eight times *shorter* than the one in the picture at the top of the page.
> 2. (a) $u_1 = 600(0.5)/4 + 320 = 395$, $v_1 = 600(0.2)/4 + 240 = 270$; in camera 2 the point is $(0.38, 0.2, 4.0)$, so $u_2 = 377$ and $d' = 18$ px, giving $Z = 600(0.12)/18 = 4.0$ m. (b) $d' = 17 \Rightarrow Z = 4.235$ m ($+0.235$); $d' = 19 \Rightarrow Z = 3.789$ m ($-0.211$). The first-order estimate is $Z^2/(fb) = 16/72 = 0.222$ m, between the two, and the two are unequal because $Z = fb/d$ is convex in $d$ — losing disparity costs more than gaining it, so the depth error distribution is skewed *away* from the camera even when the pixel error is symmetric. (c) $x_n = 0.125$, $y_n = 0.05$, $r^2 = 0.018125$, $r = 0.1346$; the factor is $1 - 0.2(0.018125) + 0.05(0.018125)^2 = 0.996391$, so the point lands at $(394.729,\ 269.892)$ and the shift is $0.291$ px. That is $7.9$ times smaller than the $2.30$ px at $Z = 2$, because the leading radial displacement in pixels is $f\lvert k_1\rvert r^3$ and $r$ halved: $2^3 = 8$. (d) $K = 4/(4+1) = 0.8$, fused range $10 + 0.8(12-10) = 11.6\,\mathrm{cm}$, $P^+ = (1-0.8)4 = 0.8\,\mathrm{cm}^2$, tip-to-wall $11.6 - 4 = 7.6\,\mathrm{cm}$. (e) The corners land at $(320, 240)$, $(395, 240)$, $(320, 300)$ and $(395, 300)$ px, a $75\times60$ px rectangle. Distance: $Z^2/(f\ell)=16/300=53.3$ mm per pixel, four times $13.3$, since the lever carries $Z^2$. Roll: one pixel across $75$ px is $0.76°$, twice $0.38°$, since it carries $Z$. Tilt: $fWH/Z^2=7.5$ px per radian, a quarter of $30$, so its spread quadruples. The listing's covariance at $t=(0,0,4)$ gives $\pm52.7$ mm, $\pm0.73°$ and $\pm10.80°$: distance and tilt grow as $Z^2$, roll as $Z$.
> 3. (a) $X$ is the unknown camera-to-gripper transform and the $4\,\mathrm{cm}$ is one translation component of it; $A$ is the gripper's motion between two robot poses, $B$ the camera's motion between the same two. It enters the equation only through $(R_A - I)t_X$, so §5's one rotation of P2 shows it as an $11.3$ mm mismatch, and a motion without rotation would not show it at all. A $0.37$ px residual is a *training* residual on the target views, and §5 shows a fit with exactly that residual still misplacing a point by $1.67$ mm at $0.5$ m off-axis and $10.0$ mm at $3$ m — the camera-to-gripper translation is estimated from those same views, so it inherits that extrapolation error. Only a held-out pose and a measured known length test it. (b) **The triangulated depth.** The wrong match has disparity $30$ instead of $36$, so it triangulates to $Z = 2.40$ m rather than $2.00$ m — a $40$ cm error that the epipolar residual reports as zero, because $F$ constrains a match to a line and says nothing about position *along* it. In general you add an independent constraint that is not along the epipolar line: a third view whose epipolar lines cross the first pair at an angle, a direct range measurement (the P5 sensor, or lidar), or an appearance check strong enough to tell two identical panels apart — which, on identical panels, means using their context rather than their texture.

### Sources

- [Szeliski, *Computer Vision: Algorithms and Applications* (free official PDF)](https://szeliski.org/Book/)
- [OpenCV camera calibration tutorial](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI sensor setup — a real calibrated multi-sensor rig](https://www.cvlibs.net/datasets/kitti/setup.php)
- Harris, C. & Stephens, M. "A combined corner and edge detector." *Proceedings of the 4th Alvey Vision Conference*, 1988.
- Shi, J. & Tomasi, C. "Good features to track." *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 1994.
- Lowe, D. G. "Distinctive image features from scale-invariant keypoints." *International Journal of Computer Vision* 60(2), 2004. doi:10.1023/B:VISI.0000029664.99615.94
- Rublee, E., Rabaud, V., Konolige, K. & Bradski, G. "ORB: An efficient alternative to SIFT or SURF." *IEEE International Conference on Computer Vision (ICCV)*, 2011.
- Mur-Artal, R., Montiel, J. M. M. & Tardós, J. D. "ORB-SLAM: A versatile and accurate monocular SLAM system." *IEEE Transactions on Robotics* 31(5), 2015. doi:10.1109/TRO.2015.2463671
- Fischler, M. A. & Bolles, R. C. "Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography." *Communications of the ACM* 24(6), 1981. doi:10.1145/358669.358692
- DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperPoint: Self-supervised interest point detection and description." *CVPR Workshops*, 2018.
- Sarlin, P.-E., DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperGlue: Learning feature matching with graph neural networks." *CVPR*, 2020.
- Sun, J., Shen, Z., Wang, Y., Bao, H. & Zhou, X. "LoFTR: Detector-free local feature matching with transformers." *CVPR*, 2021.
- Persson, M. & Nordberg, K. "Lambda Twist: An accurate fast robust perspective three point (P3P) solver." *European Conference on Computer Vision (ECCV)*, 2018. [ECVA page](https://www.ecva.net/papers/eccv_2018/papers_ECCV/html/Mikael_Persson_Lambda_Twist_An_ECCV_2018_paper.php); its abstract states the up-to-four P3P solutions.
- Wang, B., Hu, H. & Zhang, C. "Companion surface of danger cylinder and its role in solution variation of P3P problem." arXiv:1906.08598, 2019, preprint. [arXiv](https://arxiv.org/abs/1906.08598); the danger cylinder, the double solution on it, and its instability.
- Schweighofer, G. & Pinz, A. "Robust pose estimation from a planar target." *IEEE Transactions on Pattern Analysis and Machine Intelligence* 28(12), 2024–2030, 2006. [Publication record](https://tugraz.elsevierpure.com/en/publications/robust-pose-estimation-from-a-planar-target-2/); a unique pose from four coplanar points in theory, two local minima in practice.
- Olson, E. "AprilTag: A robust and flexible visual fiducial system." *ICRA*, 2011; Wang, J. & Olson, E. "AprilTag 2: Efficient and robust fiducial detection." *IROS*, 2016. [AprilTag project page](https://april.eecs.umich.edu/software/apriltag)
- Lindenberger, P., Sarlin, P.-E. & Pollefeys, M. "LightGlue: Local feature matching at light speed." *ICCV*, 2023. [arXiv:2306.13643](https://arxiv.org/abs/2306.13643)
- Wang, S., Leroy, V., Cabon, Y., Chidlovskii, B. & Revaud, J. "DUSt3R: Geometric 3D vision made easy." *CVPR*, 2024. [arXiv:2312.14132](https://arxiv.org/abs/2312.14132)
- Leroy, V., Cabon, Y. & Revaud, J. "Grounding image matching in 3D with MASt3R." *ECCV*, 2024. [arXiv:2406.09756](https://arxiv.org/abs/2406.09756)
- Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C. & Novotny, D. "VGGT: Visual geometry grounded transformer." *CVPR*, 2025. [arXiv:2503.11651](https://arxiv.org/abs/2503.11651)

## 한국어

*B군이다. [[02-foundations/linear-algebra|선형대수]]·최적화와 [[02-foundations/se3-geometry|SE(3)]] 위에 선다. 픽셀과 점군이 올바른 좌표계의
3D가 되는 과정이고, H군과 J군의 인식 주장이 전부 여기를 통과한다.*

[[02-foundations/se3-geometry|SE(3)]]가 pose를 *적는* 언어라면, 기하학적 인식은 로봇이
pose를 *얻는* 방법이다 — 픽셀, 깊이, 포인트 클라우드가 올바른 좌표계의 3D 구조가 되는
과정. 딥 인식([[03-deep-learning/index|딥러닝]])이 무엇*인지*를 알려준다면, 기하학적
인식은 그것이 *어디에*, *어떤 스케일로*, *어느 프레임에* 있는지를 알려준다.

> [!info] 깊이 목표
> Pose 추정, visual odometry/SLAM front end, 보정, 포인트 클라우드 논문을 projection,
> intrinsics/extrinsics, registration, reprojection error에서 막히지 않고 읽는다.
> 다시점 기하의 유도(essential/fundamental matrix, bundle adjustment)는 실무/숙달
> 단계의 주제다.

> [!note] 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**, **P5** · [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/se3-geometry|3D 기하와 SE(3)]] · [[02-foundations/optimization|최적화]] (최소제곱) · [[02-foundations/probability|확률]] (§4의 최대우도, P5가 쓰는 §5의 스칼라 칼만 갱신)

> [!note] 처음이라면 · First pass
> 그림과 계산 절부터 본다. 리그의 점 하나를 투영하고, 삼각측량하고, 왜곡하고, 잘못 보정해 보는 것을 숫자 전부와 함께 한다. 그다음 §1(핀홀 모델, 투영식까지), §5(보정 — 현장 실패가 실제로 시작되는 곳), §7(주장 읽기)을 읽는다. §2~§4(깊이, 이미지 특징, 두 시점 기하, 포인트 클라우드, ICP)는 기계장치이고, 논문의 숫자가 거기 기댈 때 읽어라. §6과 §7.5는 학습 기반 인식과 visual servoing으로 넘어가는 짧은 다리다.

### 계속 쓰는 대상: P2의 손목 리그

[[02-foundations/lab-plants|0.6 Lab Plants]]에는 카메라인 장치가 없다. 그래서 이 페이지는 자기 리그를 고정하고 아래 숫자를 다시는 바꾸지 않는다. 평면 2R 팔 **P2** 에 달려 도구 축을 따라 패널을 보고, 과제가 융합하는 스칼라 거리 하나는 **P5** 가 준다. 길이는 미터, 픽셀은 픽셀, P5의 거리는 0.6이 고정한 대로 센티미터다.

| 기호 | 값 | 무엇인가 |
|---|---:|---|
| $f_x, f_y$ | 각각 $600$ px | 픽셀 단위 초점 거리, 픽셀이 정사각이라 둘이 같다 |
| $c_x, c_y$ | $320$, $240$ px | 주점, $640\times480$ 센서의 이미지 중심 |
| $s$ | $0$ | skew, 실제로 만날 모든 센서에서 0 |
| $k_1, k_2$ | $-0.20$, $+0.05$ | 반경 방향 왜곡 계수($k_1<0$ 이므로 배럴) |
| $p_1, p_2$ | $0$, $0$ | 접선 방향 왜곡, 렌즈가 제대로 앉았으면 0 |
| $b$ | $0.12$ m | 스테레오 기선: $t = (-b, 0, 0)$, $R = I$ 의 동일한 두 번째 카메라 |
| $L$ | $(0.5,\ 0.2,\ 2.0)$ m | 랜드마크, 카메라 1의 프레임에서 |
| $A, B, C$ | $(0,0,2)$, $(0.5,0,2)$, $(0,0.4,2)$ m | 한 평면 위의 보정 타깃 코너 셋 |
| $d_{ct}$ | $0.04$ m | 손-눈 오프셋: 카메라가 P2 도구 끝에서 이만큼 뒤에 있다 |
| P5 | 사전 $10 \pm 2$ cm, 측정 $12$ cm, $R = 1\,\mathrm{cm}^2$ | 0.6이 고정한 패널까지의 거리 |

페이지의 나머지는 전부 저 표에서 나온다. $L$ 은 카메라 1에서 $(470, 300)$ px, 카메라 2에서 $(434, 300)$ px에 맺히므로 시차가 $36$ px이고 $Z = f b / d = 600 \times 0.12 / 36 = 2.0$ m — 출발한 자리다. 이 왕복이 리그가 일관되다는 확인이다.

*범위: 이 페이지는 3D 점과 픽셀 사이의 기하, 그리고 그 기하가 의존하는 보정을 가르친다 — intrinsics, extrinsics, 왜곡, 두 시점 제약, registration. 물체가 무엇인지([[03-deep-learning/index|딥러닝]]), 카메라 pose가 시간에 걸쳐 어떻게 추정되는지([[04-robotics/state-estimation-slam|3. 상태 추정과 SLAM]]), 리그가 런타임에 어떻게 발행되고 타임스탬프가 찍히는지([[04-robotics/robot-systems-deployment|10. 로봇 시스템]])는 가르치지 않는다.*

### 그림으로 먼저 보기: 광선 하나, 카메라 둘, 오차 막대 셋

<svg viewBox="0 0 560 472" style="max-width:100%;height:auto" role="img" aria-label="손목 리그의 스테레오 그림: 닮은꼴 삼각형 둘로 본 랜드마크의 핀홀 투영, 옆으로 0.12 m 떨어진 두 번째 카메라와 2 m의 랜드마크 및 8 m의 점으로 가는 광선, 그리고 축척대로 그린 깊이 오차 막대 둘과 왜곡 이동">
  <text x="16" y="24" font-size="12" fill="currentColor" font-weight="600">XZ 평면의 투영</text>
  <text x="232" y="24" font-size="12" fill="currentColor" font-weight="600">두 번째 카메라</text>
  <text x="404" y="24" font-size="12" fill="currentColor" font-weight="600">오차 셋, 축척대로</text>
  <path d="M64 300 L64 100 L114 100 Z" fill="currentColor" fill-opacity="0.07" stroke="none"/>
  <path d="M64 300 L64 180 L94 180 Z" fill="currentColor" fill-opacity="0.24" stroke="none"/>
  <line x1="64" y1="300" x2="64" y2="50" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <path d="M64 44 L66.9 51 L61.1 51 Z" fill="currentColor" stroke="none" fill-opacity="0.7"/>
  <text x="72" y="56" font-size="11" fill="currentColor" fill-opacity="0.8">광축</text>
  <line x1="36" y1="180" x2="190" y2="180" stroke="currentColor" stroke-width="1.8"/>
  <text x="106" y="173" font-size="11" fill="currentColor">이미지 평면, Z = f</text>
  <line x1="64" y1="100" x2="114" y2="100" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="114" y1="100" x2="64" y2="300" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="114" cy="100" r="4.2" stroke="none" fill="currentColor"/>
  <circle cx="94" cy="180" r="3.2" stroke="none" fill="currentColor"/>
  <circle cx="64" cy="300" r="3.6" stroke="none" fill="currentColor"/>
  <text x="64" y="318" font-size="12" fill="currentColor" text-anchor="middle">O</text>
  <text x="122" y="104" font-size="11" fill="currentColor">L (0.5, 2.0) m</text>
  <line x1="30" y1="100" x2="30" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="27" y1="100" x2="33" y2="100" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="27" y1="300" x2="33" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="46" y1="180" x2="46" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="43" y1="180" x2="49" y2="180" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="43" y1="300" x2="49" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="24" y="144" font-size="12" fill="currentColor" text-anchor="end">Z</text>
  <text x="38" y="244" font-size="12" fill="currentColor" text-anchor="middle">f</text>
  <line x1="64" y1="90" x2="114" y2="90" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="64" y1="87" x2="64" y2="93" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="114" y1="87" x2="114" y2="93" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="89" y="84" font-size="12" fill="currentColor" text-anchor="middle">X</text>
  <line x1="64" y1="187" x2="94" y2="187" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="64" y1="184" x2="64" y2="190" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <line x1="94" y1="184" x2="94" y2="190" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="104" y="198" font-size="11" fill="currentColor">u − c<tspan dy="3.1" font-size="8.6">x</tspan></text>
  <text x="16" y="340" font-size="11" fill="currentColor">(u − c<tspan dy="3.1" font-size="8.6">x</tspan><tspan dy="-3.1">) / f = X / Z</tspan></text>
  <text x="16" y="356" font-size="11" fill="currentColor">150 / 600 = 0.5 / 2.0</text>
  <text x="16" y="372" font-size="11" fill="currentColor">그래서 u = 320 + 150 = 470 px</text>
  <line x1="250" y1="300" x2="250" y2="64" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="280" y1="300" x2="280" y2="64" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.35" stroke-dasharray="4 3"/>
  <line x1="250" y1="300" x2="287.5" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" stroke-dasharray="6 3"/>
  <line x1="280" y1="300" x2="308.5" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" stroke-dasharray="6 3"/>
  <path d="M287.5 60 L289.3 67.4 L283.5 66.5 Z" fill="currentColor" stroke="none"/>
  <path d="M308.5 60 L310.6 67.3 L304.8 66.6 Z" fill="currentColor" stroke="none"/>
  <line x1="250" y1="300" x2="375" y2="100" stroke="currentColor" stroke-width="1.6"/>
  <line x1="280" y1="300" x2="375" y2="100" stroke="currentColor" stroke-width="1.6"/>
  <circle cx="375" cy="100" r="4.2" stroke="none" fill="currentColor"/>
  <text x="369" y="91" font-size="12" fill="currentColor" text-anchor="middle">L</text>
  <path d="M244 309 L250 300 L256 309 Z" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.25" stroke-linejoin="round"/>
  <path d="M274 309 L280 300 L286 309 Z" stroke="currentColor" stroke-width="1.4" fill="currentColor" fill-opacity="0.25" stroke-linejoin="round"/>
  <text x="241" y="322" font-size="11" fill="currentColor" text-anchor="middle">C<tspan dy="3.1" font-size="8.6">1</tspan></text>
  <text x="284" y="322" font-size="11" fill="currentColor">C<tspan dy="3.1" font-size="8.6">2</tspan><tspan dy="-3.1">: X = +0.12 m</tspan></text>
  <text x="301.5" y="46" font-size="11" fill="currentColor">Z = 8 m: d = 9 px</text>
  <text x="360" y="112" font-size="11" fill="currentColor" text-anchor="end">d = 36 px</text>
  <text x="392" y="282" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.8">X를 Z의 2.5배로 그림</text>
  <line x1="234" y1="374" x2="391.5" y2="374" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <line x1="244.5" y1="371" x2="244.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="265.5" y1="371" x2="265.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="286.5" y1="371" x2="286.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="307.5" y1="371" x2="307.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="328.5" y1="371" x2="328.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="349.5" y1="371" x2="349.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="370.5" y1="371" x2="370.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <line x1="391.5" y1="371" x2="391.5" y2="377" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.45"/>
  <text x="234" y="340" font-size="11" fill="currentColor" fill-opacity="0.85">두 이미지를 한 u축에 (px)</text>
  <line x1="343.2" y1="365" x2="343.2" y2="377" stroke="currentColor" stroke-width="1.8"/>
  <line x1="381" y1="365" x2="381" y2="377" stroke="currentColor" stroke-width="1.8"/>
  <text x="343.2" y="361" font-size="11" fill="currentColor" text-anchor="middle">434</text>
  <text x="381" y="361" font-size="11" fill="currentColor" text-anchor="middle">470</text>
  <line x1="347.6" y1="383" x2="376.6" y2="383" stroke="currentColor" stroke-width="1.1"/>
  <path d="M381 383 L375.5 385.3 L375.5 380.7 Z" fill="currentColor" stroke="none"/>
  <path d="M343.2 383 L348.7 380.7 L348.7 385.3 Z" fill="currentColor" stroke="none"/>
  <text x="362.1" y="397" font-size="11" fill="currentColor" text-anchor="middle">d = 36</text>
  <line x1="253.4" y1="365" x2="253.4" y2="377" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9"/>
  <line x1="262.9" y1="365" x2="262.9" y2="377" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.9"/>
  <text x="258.1" y="361" font-size="11" fill="currentColor" text-anchor="middle">8 m</text>
  <line x1="253.4" y1="383" x2="262.9" y2="383" stroke="currentColor" stroke-width="1.1"/>
  <line x1="253.4" y1="380" x2="253.4" y2="386" stroke="currentColor" stroke-width="1.0"/>
  <line x1="262.9" y1="380" x2="262.9" y2="386" stroke="currentColor" stroke-width="1.0"/>
  <text x="258.1" y="397" font-size="11" fill="currentColor" text-anchor="middle">d = 9</text>
  <line x1="444" y1="300" x2="444" y2="39.6" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7"/>
  <path d="M444 32.6 L446.5 38.6 L441.5 38.6 Z" fill="currentColor" stroke="none" fill-opacity="0.8"/>
  <text x="452" y="43.6" font-size="11" fill="currentColor">Z (m)</text>
  <line x1="440" y1="300" x2="444" y2="300" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="304" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">0</text>
  <line x1="440" y1="244" x2="444" y2="244" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="248" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">2</text>
  <line x1="440" y1="188" x2="444" y2="188" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="192" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">4</text>
  <line x1="440" y1="132" x2="444" y2="132" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="136" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">6</text>
  <line x1="440" y1="76" x2="444" y2="76" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.7"/>
  <text x="437" y="80" font-size="11" fill="currentColor" text-anchor="end" fill-opacity="0.85">8</text>
  <rect x="450" y="242.4" width="10" height="3.1" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.35"/>
  <line x1="447" y1="242.4" x2="463" y2="242.4" stroke="currentColor" stroke-width="1.2"/>
  <line x1="447" y1="245.6" x2="463" y2="245.6" stroke="currentColor" stroke-width="1.2"/>
  <rect x="450" y="51.1" width="10" height="49.8" stroke="currentColor" stroke-width="1.0" fill="currentColor" fill-opacity="0.35"/>
  <line x1="447" y1="51.1" x2="463" y2="51.1" stroke="currentColor" stroke-width="1.2"/>
  <line x1="447" y1="100.9" x2="463" y2="100.9" stroke="currentColor" stroke-width="1.2"/>
  <text x="468" y="248" font-size="11" fill="currentColor">(i) ±0.056 m</text>
  <text x="468" y="76" font-size="11" fill="currentColor">(ii) ±0.89 m</text>
  <text x="468" y="90" font-size="11" fill="currentColor" fill-opacity="0.85">16배 길다</text>
  <line x1="414" y1="330" x2="414" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="425" y1="330" x2="425" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="436" y1="330" x2="436" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="447" y1="330" x2="447" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="458" y1="330" x2="458" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="469" y1="330" x2="469" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="480" y1="330" x2="480" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="491" y1="330" x2="491" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="502" y1="330" x2="502" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="330" x2="502" y2="330" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="341" x2="502" y2="341" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="352" x2="502" y2="352" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="363" x2="502" y2="363" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <line x1="414" y1="374" x2="502" y2="374" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35"/>
  <circle cx="469" cy="363" r="3.4" stroke="none" fill="currentColor"/>
  <line x1="469" y1="363" x2="450" y2="355.4" stroke="currentColor" stroke-width="1.6"/>
  <path d="M445.5 353.6 L452 353.5 L450.1 358.2 Z" fill="currentColor" stroke="none"/>
  <text x="414" y="322" font-size="11" fill="currentColor">(iii) 이미지 평면</text>
  <text x="414" y="389" font-size="11" fill="currentColor">2.30 px 편향</text>
  <text x="414" y="403" font-size="11" fill="currentColor" fill-opacity="0.8">한 칸 = 1 px</text>
  <text x="16" y="428" font-size="11" fill="currentColor" fill-opacity="0.9">8 m에서는 두 광선이 거의 나란하다(시차 36이 아니라 9 px). 깊이 정확도의 실체가 그 각도다.</text>
  <text x="16" y="444" font-size="11" fill="currentColor" fill-opacity="0.9">두 깊이 막대는 같은 축척이라 8 m 막대가 2 m 막대의 열여섯 배다. 깊이 오차는 Z²로 자란다.</text>
  <text x="16" y="460" font-size="11" fill="currentColor" fill-opacity="0.9">2.30 px 이동은 이미지 평면 위의 편향이지 잡음이 아니다. 프레임을 평균해도 줄지 않는다.</text>
</svg>

손목 리그와 $(X,Z)=(0.5,\,2.0)$ m의 랜드마크 $L$ 이다. 왼쪽은 $XZ$ 평면의 핀홀 투영으로 닮은꼴 삼각형이 $150/600=0.5/2.0$, 곧 $u=470$ px를 주고, 가운데에서는 옆으로 $0.12$ m 떨어진 두 번째 카메라가 $L$ 을 $u=434$ 에서 보아 시차가 $36$ px인 반면 $8$ m의 점은 거의 평행한 광선으로 $9$ px만 준다. 오른쪽은 같은 축척으로 그린 오차 셋이다: $\pm1$ px 시차 오차는 깊이로 $2$ m에서 $\pm0.056$ m, $8$ m에서 $\pm0.89$ m이고 깊이 오차가 $Z^2$ 로 자라므로 열여섯 배 길며, $L$ 에서의 $2.30$ px 왜곡 이동은 잡음이 아니라 편향으로 이미지 평면 위에 놓인다.

### 대상으로 한 번 끝까지: 표에서 픽셀로, 그리고 되돌아

**1. $L$ 을 투영한다.** 카메라 프레임을 세계 프레임과 같게 두어 $R = I$, $t = 0$ 이고, $K$ 가 표의 $f_x, f_y, c_x, c_y$ 와 skew $s$ 를 담은 내부 파라미터 행렬(§1이 성분 하나하나를 정의한다)인 동차 형태로

$$\tilde u = K\,[R \mid t]\,\tilde L = \begin{pmatrix}600&0&320\\0&600&240\\0&0&1\end{pmatrix}\begin{pmatrix}0.5\\0.2\\2.0\end{pmatrix} = \begin{pmatrix}940\\600\\2\end{pmatrix}$$

세 번째 성분으로 나누면 $(u, v) = (470, 300)$ px다. 원근이 수행하는 $Z$ 로 나누기가 정확히 세 번째 좌표의 비동차화이기 때문이다.

**2. 같은 점을 카메라 2에서, 그리고 깊이로 되돌리기.** $p^{c_2} = Ip^{c_1} + t = (0.5 - 0.12,\ 0.2,\ 2.0) = (0.38, 0.2, 2.0)$ 이므로 $u_2 = 600 \times 0.38/2.0 + 320 = 434$, $v_2 = 300$ 이다. 시차는 $d = 470 - 434 = 36$ px, $Z = f b / d = 2.0$ m이고, 이어서 $X = (u_1 - c_x)Z/f_x = 150 \times 2/600 = 0.5$ m, $Y = (v_1 - c_y)Z/f_y = 60 \times 2/600 = 0.2$ m다. 리그가 $L$ 을 정확히 복원한다. $R = I$ 일 때 삼각측량이 대수적으로 투영의 역이기 때문이다.

**3. 왜곡이 그것을 어디로 옮기는가.** 왜곡은 $K$ 보다 먼저 정규화 좌표에 Brown–Conrady 모델의 반경 계수 $1 + k_1r^2 + k_2r^4$ 로 작용한다(§1이 모델과 그 순서를 적는다). 여기서 정규화 좌표는 $x_n = X/Z = 0.25$, $y_n = Y/Z = 0.10$ 이므로 $r^2 = 0.0725$, $r^4 = 0.00525625$ 다. 반경 계수는 $1 + k_1r^2 + k_2r^4 = 1 - 0.0145 + 0.000263 = 0.985763$ 이라 $(x_d, y_d) = (0.246441, 0.098576)$ 이 되고 왜곡된 픽셀은 $(467.864,\ 299.146)$ 이다. 랜드마크는 이상적 모델이 말하는 자리에서 실제로 $2.30$ px 떨어져 맺히는데, 그것도 $r = 0.269$ 라는 온건한 값에서다. 이미지 모서리로 갈수록 $r^2$ 로 자란다.

**4. 서브픽셀 보정 잔차가 감추는 것.** 보정이 $600$ 대신 $\hat f = 598$ px를 돌려주고 나머지는 정확하다고 하자. 타깃 코너 셋을 다시 투영하면

| 코너 | 참 $(u,v)$ | $\hat f = 598$ 로 | 잔차 |
|---|---|---|---:|
| $A=(0,0,2)$ | $(320,\ 240)$ | $(320.0,\ 240.0)$ | $0.00$ px |
| $B=(0.5,0,2)$ | $(470,\ 240)$ | $(469.5,\ 240.0)$ | $0.50$ px |
| $C=(0,0.4,2)$ | $(320,\ 360)$ | $(320.0,\ 359.6)$ | $0.40$ px |

검출된 코너와 재투영된 코너 사이 픽셀 거리의 제곱평균제곱근인 RMS reprojection error(§5가 정의한다)는 $\sqrt{(0^2 + 0.5^2 + 0.4^2)/3} = 0.370$ px로 넉넉히 "서브픽셀"이고, 주점에 있는 코너는 아무 기여도 하지 않는다. 초점 거리 오차가 거기서는 보이지 않기 때문이다. 이제 그 보정으로 $Z = 2$ m를 아는 $B$ 의 검출을 역투영하면 $X = (470-320)\times 2/598 = 0.50167$ m, 곧 $1.67$ mm의 오차다. 상대 오차는 축에서 벗어난 거리의 $(f - \hat f)/\hat f = 0.334\%$ 이므로 $X = 0.5$ m에서 $1.67$ mm, $X = 3$ m에서 $10.0$ mm다. 서브픽셀 잔차는 적합에 대한 진술이지 미터에 대한 진술이 아니다.

### 1. 핀홀 카메라 모델

**카메라 프레임**의 3D 점 $p^{c}=(X,Y,Z)$는 픽셀 $(u,v)$로 투영된다:

$$u = f_x\frac{X}{Z}+c_x, \qquad v = f_y\frac{Y}{Z}+c_y$$

**이것이 어디서 오는가 — 닮은꼴 삼각형, 그게 전부다.** 광학 중심을 원점에 두고 이미지 평면을
그 앞 거리 $f$에 둔다. 3D 점 $(X, Y, Z)$에서 중심으로 가는 광선이 그 평면을 높이 $y$에서
지나는데, 그 광선이 만드는 두 삼각형 — 중심에서 평면까지, 중심에서 점까지 — 이 닮은꼴이다.
그래서 $y/f = Y/Z$, 즉 $y = fY/Z$다. 나머지는 장부 정리다. 물리적 픽셀 피치로 나눠 픽셀 단위로
바꾸고(픽셀이 정사각이 아니면 $f_x$와 $f_y$가 달라지는 이유이고, 초점 거리를 밀리미터가 아니라
*픽셀 단위*로 적는 이유다), $c_x, c_y$를 더해 원점을 광축에서 배열 인덱스가 시작하는 이미지
모서리로 옮긴다.

모델은 그게 전부이고, 그 모양이 뒤따르는 전부가 물려받는 두 사실을 지고 있다. 이 사상은
**선형이 아니다** — $Z$가 분모에 있고, 그래서 원근이 행렬이 되려면 먼저 동차 좌표가 필요하다 —
그리고 **가역이 아니다**. 한 광선 위의 모든 점이 같은 $(u,v)$를 주기 때문이다. 그러므로 $Z$를
되찾는 것은 더 좋은 카메라의 문제가 아니라 두 번째 제약이 필요한 문제이고, §2가 그것에 관한
것이다.

- **Intrinsics** $(f_x, f_y, c_x, c_y$, 왜곡$)$: 카메라 자체의 성질 — 픽셀 단위 초점
  거리와 주점. 한 번 보정하면 (렌즈를 건드리기 전까지) 고정.
- **Extrinsics** $(R, t)$: 투영 전에 다른 프레임(로봇 베이스, 월드)의 점을 카메라 프레임으로 옮기는 [[02-foundations/se3-geometry|SE(3)]] 변환 $T_{cw}$, $p^c = Rp^w + t$다.
  그 프레임에서의 카메라 *pose*는 그 역 $T_{wc}$이고 카메라 중심은 $-R^\top t$다. 중심은 $p^c=0$인 점이므로 $0=Rp^w+t$에서 $p^w=-R^\top t$가 나온다($R^{-1}=R^\top$ 사용). 보정 파일이 어느 쪽을 저장하는지 확인하라.
- $Z$로 나누는 것이 원근의 전부다: 먼 점일수록 이미지에서 덜 움직이고, **절대
  스케일이 사라진다** — 이미지 한 장으로는 크고 먼 물체와 작고 가까운 물체를 구분할
  수 없다.

<svg viewBox="0 0 460 200" style="max-width:100%;height:auto" role="img" aria-label="핀홀 투영: 작고 가까운 물체와 크고 먼 물체가 같은 픽셀에 맺힌다">
  <g stroke="currentColor" stroke-width="1.3"><line x1="150" y1="25" x2="150" y2="170"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="4 3"><line x1="60" y1="110.0" x2="440" y2="110.0"/></g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <line x1="60" y1="110" x2="440" y2="26.4"/><line x1="60" y1="110" x2="440" y2="72.0"/>
  </g>
  <g stroke="currentColor" stroke-width="3.2">
    <line x1="150" y1="90.2" x2="150" y2="101.0"/>
    <line x1="250" y1="68.2" x2="250" y2="91.0"/>
    <line x1="420" y1="30.8" x2="420" y2="74.0"/>
  </g>
  <g fill="currentColor"><circle cx="60" cy="110" r="3.5"/></g>
  <g font-size="11.5" fill="currentColor">
    <text x="30" y="114">O</text>
    <text x="112" y="20">이미지 평면</text>
    <text x="212" y="110">작고 가깝다</text>
    <text x="372" y="92">크고 멀다</text>
    <text x="158" y="128">센서 위에서는 같은 상</text>
    <text x="25" y="192" opacity="0.85">u = f X / Z + c &#8212; Z로 나누는 그 한 번이 절대 스케일을 지운다</text>
  </g>
</svg>



**투영 계산 예제**: $f_x=f_y=600$ px, $(c_x,c_y)=(320,240)$, 점
$p^{c}=(0.5, 0.2, 2.0)$ m이면 $u = 600\cdot 0.5/2.0+320=470$,
$v = 600\cdot 0.2/2.0+240=300$. 점을 두 배 멀리 보내면($Z=4$): $u=395, v=270$ —
주점 쪽으로 미끄러진다.

**내부 행렬의 완전한 정의.** $K$ 는 정규화 이미지 좌표 — 광선 방향 $(X/Z,\ Y/Z,\ 1)$, 곧 원근이 거리를 버리고 3D 점에서 남긴 것 — 를 픽셀 좌표로 보내는 **상삼각 $3\times3$ 행렬**이다. 성분이 다섯이고, 다섯을 다 이름 붙이는 것이 정의다.

$$K = \begin{pmatrix} f_x & s & c_x \\ 0 & f_y & c_y \\ 0 & 0 & 1 \end{pmatrix}$$

- $f_x, f_y$ — 각 이미지 축을 따른 **픽셀 단위 초점 거리**, 곧 물리적 초점 거리를 그 방향의 픽셀 피치로 나눈 값이다. 픽셀이 정사각일 때만 둘이 같으므로 $f_x \ne f_y$ 는 렌즈가 아니라 센서에 대한 진술이다. 이 리그는 둘 다 $600$ 으로 고정한다.
- $c_x, c_y$ — **주점**, 광축이 이미지 평면을 뚫는 자리를 배열 모서리에서부터 픽셀로 잰 값이다. 이미지 중심 근처지만 정확히 중심은 아니다. $c_x$ 가 $w/2$ 에서 크게 벗어난 보정 결과는 대개 잘렸거나 잘못 지정된 이미지를 보고하는 것이다.
- $s$ — **skew**, 센서의 두 픽셀 축이 직교하지 않을 때만 0이 아니다. 모든 고체 촬상 소자에서 $0$ 이고 이 리그도 $0$ 으로 고정한다. 모델에 남아 있는 이유는 주로 $K$ 가 아핀 rectification을 흡수할 수 있게 하기 위해서다.

그러면 카메라 전체는 동차 좌표 위에서 extrinsics와 intrinsics를 합성한 것이고, 이것이 페이지의 나머지가 미분하고 역으로 풀고 최적화하는 단 하나의 식이다.

$$\lambda \begin{pmatrix}u\\v\\1\end{pmatrix} = K\,[R \mid t]\begin{pmatrix}X^w\\Y^w\\Z^w\\1\end{pmatrix}, \qquad \lambda = Z^c$$

스칼라 $\lambda$ 는 카메라 프레임에서의 깊이이므로 그것을 나눠 없애는 것이 *곧* 원근 나눗셈이고, 행렬은 나눌 수 없으므로 — 나눌 수 있는 것은 비동차화뿐이므로 — $K$ 를 이렇게 써야 한다. *예:* 리그의 $K$ 는 $L$ 의 광선 $(0.25, 0.10, 1)$ 을 $(470, 300, 1)$ 로 보낸다. *반례:* $K$ 는 물리 단위의 변환이 **아니다**. 방향을 픽셀로 보내므로 미터 단위 점에 $K(0.5, 0.2, 2.0)^\top$ 처럼 적용하면 우연히 맞는 것이다 — $(940, 600, 2)$ 가 나오고 비동차화하면 정답이 되는데, 세 번째 행이 $Z$ 로 또 나누기 때문일 뿐이다. 이미 정규화한 광선을 넣으면 옳고, 나누지 않은 미터 점을 넣으면 우연에 기댄 것이다.

**외부 파라미터의 완전한 정의.** $[R \mid t]$ 는 세계 점을 카메라 프레임으로 쓰는 **SE(3)** 변환 $T_{cw}$ 의 $3\times4$ 블록이다. $p^c = Rp^w + t$ 이고 $R \in SO(3)$, $t \in \mathbb{R}^3$ 이다([[02-foundations/se3-geometry|8. 3D 기하와 SE(3)]]). 이것을 pose가 아니라 extrinsic으로 만드는 조건이 둘이다: 방향이 **세계에서 카메라로**이고, $R^\top R = I$ 이므로 스케일도 전단도 **없다**. 카메라의 *세계 안 pose*는 역변환 $T_{wc}$ 이고 그 평행 이동이 카메라 중심 $-R^\top t$ 다. 중심은 $p^c = 0$ 인 점이고 $0 = Rp^w + t$ 에서 $p^w = -R^\top t$ 가 나오기 때문이다. *반례:* $t$ 를 저장해 놓고 "카메라 위치"라 부르는 것이 보정 파일에서 가장 흔한 버그다. $t$ 가 카메라 중심과 같은 것은 $R = I$ 일 때뿐이고, 그때도 부호를 빼고서다.

**왜곡 모델의 완전한 정의.** 실제 렌즈는 광선을 휘게 하므로 핀홀 사상은 **정규화 좌표에서 먼저, 왜곡이 다음, $K$ 가 마지막** 순서로 적용된다. 그 순서가 정의의 일부이고 바꾸면 조용한 오류가 된다. $x_n = X/Z$, $y_n = Y/Z$, $r^2 = x_n^2 + y_n^2$ 로 두면 OpenCV가 쓰는 Brown–Conrady 모델은 반경 항 둘과 접선 항 둘을 갖는다.

$$\begin{pmatrix}x_d\\y_d\end{pmatrix} = \underbrace{(1 + k_1r^2 + k_2r^4 + k_3r^6)}_{\text{반경}}\begin{pmatrix}x_n\\y_n\end{pmatrix} + \underbrace{\begin{pmatrix}2p_1x_ny_n + p_2(r^2+2x_n^2)\\ p_1(r^2+2y_n^2) + 2p_2x_ny_n\end{pmatrix}}_{\text{접선}}$$

그다음 $u = f_xx_d + c_x$, $v = f_yy_d + c_y$ 다. **반경** 부분은 $r$ 의 짝함수이고 점을 자기 반경을 따라 움직인다 — $k_1>0$ 이면 바깥으로(핀쿠션), $k_1<0$ 이면 안으로(배럴). 렌즈의 어긋남이 광선이 어느 쪽으로 들어오느냐가 아니라 축에서 얼마나 벗어나 들어오느냐에 달렸기 때문이다. **접선** 부분은 렌즈가 센서와 평행하지 않아 생기고 점을 옆으로 민다. *예:* 리그의 $L$ 은 $r = 0.269$ 에 있고 $k_1 = -0.20$, $k_2 = 0.05$ 가 그것을 $(470, 300)$ 에서 $(467.86, 299.15)$ 로, 곧 $2.30$ px 끌어당긴다. *반례:* 왜곡은 잡음이 **아니다**. 결정적이고 재현되는 편향이므로 프레임을 더 평균해도 $1/\sqrt{n}$ 로 줄지 않는다. 줄이는 것은 $k_1, k_2$ 를 추정하는 것뿐이다. 보정하지 않은 이미지에서 "서브픽셀" 재현성을 보고하는 특징 매처는 재현성 있게 $2.3$ px 틀린 것이다. *왜 중요한가:* 이 페이지 뒤쪽의 모든 잔차 — reprojection error, epipolar 거리, ICP — 는 *왜곡을 편 뒤의* 모델에 대해 계산되므로, 모델에 없는 $k_1$ 은 셋 모두에 최소자승이 아무리 해도 흡수하지 못하는 편향으로 들어간다.

### 2. 깊이 복원

| 방법 | 깊이가 나타나는 방식 | 주된 주의점 |
|---|---|---|
| 스테레오 | 두 시점 간 시차 $d$: $Z = f\,b/d$ (기선 $b$) | 무늬 없는/반복 표면; 오차가 $Z^2$로 증가 |
| RGB-D / ToF / 구조광 | 센서가 픽셀별 $Z$ 측정 | 거리 한계, 햇빛, 반사/어두운 재질 |
| LiDAR | 직접 time-of-flight 거리 | 희소성, 운동 왜곡, 날씨 |
| 학습된 단안 깊이 | 네트워크가 $Z$ 예측 (대개 스케일과 오프셋이 미정, 흔히 역깊이 $1/Z$ 공간. 먼 배경으로 갈수록 $1/Z$는 0 근처에 머물러 유계다) | 스케일 모호성; 분포 이동 — [[01-canonical-papers/notes/2-computer-vision/depth-anything\|Depth Anything]]의 주장 범위 확인 |
| 삼각측량 | 알려진 두 pose에서 광선 교차 | 기선 필요; 먼 점·짧은 기선에서 퇴화 |

**스테레오 계산 예제**: $f=600$ px, 기선 $b=0.12$ m, 시차 $d=9$ px
→ $Z = 600\cdot 0.12/9 = 8$ m. 시차 1픽셀 오차($d=8$)면 $Z=9$ m — 이 거리에서 12.5%
튄다: 깊이 오차는 거리에 제곱으로 자란다. 광축을 가로지르는 방향에서는 같은 1픽셀이 $Z/f$미터일 뿐이고, 픽셀 잡음 σ를 필터가 쓰는 측정 분산으로 바꾸는 일은 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §5와 §8]]에 있다. 표의 다른 행은 제 물리를 가진 센서다 — 위상이 감기는 ToF 카메라, 거리와 함께 점이 커지는 LiDAR — 그 값을 이 리그 위에서 매기는 곳이 [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §3–§5]]다.

<svg viewBox="0 0 620 246" style="max-width:100%;height:auto" role="img" aria-label="스테레오: 가까운 점은 두 광선을 크게 벌리고, 먼 점은 거의 나란하게 만든다">
  <g stroke="currentColor" stroke-width="1.4" fill="none">
    <line x1="60" y1="190" x2="60" y2="172"/><line x1="140" y1="190" x2="140" y2="172"/>
    <line x1="360" y1="190" x2="360" y2="172"/><line x1="440" y1="190" x2="440" y2="172"/>
  </g>
  <g stroke="currentColor" stroke-width="1.4" opacity="0.8" fill="none">
    <line x1="60" y1="190" x2="100" y2="140"/><line x1="140" y1="190" x2="100" y2="140"/>
    <line x1="360" y1="190" x2="400" y2="70"/><line x1="440" y1="190" x2="400" y2="70"/>
  </g>
  <g fill="currentColor">
    <circle cx="60" cy="190" r="3.5"/><circle cx="140" cy="190" r="3.5"/>
    <circle cx="360" cy="190" r="3.5"/><circle cx="440" cy="190" r="3.5"/>
    <circle cx="100" cy="140" r="4.5"/><circle cx="400" cy="70" r="4.5"/>
  </g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35" stroke-dasharray="3 3">
    <line x1="60" y1="202" x2="140" y2="202"/><line x1="360" y1="202" x2="440" y2="202"/>
  </g>
  <g font-size="11" fill="currentColor" text-anchor="middle">
    <text x="100" y="30">가깝다</text><text x="400" y="30">멀다</text>
    <text x="100" y="48" font-size="10.5" opacity="0.85">Z = 2 m &#183; 시차 36 px</text>
    <text x="400" y="48" font-size="10.5" opacity="0.85">Z = 8 m &#183; 시차 9 px</text>
    <text x="100" y="218" font-size="10.5">베이스라인 b</text><text x="400" y="218" font-size="10.5">베이스라인 b</text>
  </g>
  <g font-size="11" fill="currentColor"><text x="30" y="240" opacity="0.9">시차는 수평 픽셀 이동량이며, 먼 점에서는 삼각측량 각도와 함께 작아진다.</text></g>
</svg>

**오차가 $Z^2$로 자라는 이유.** $Z=fb/d$를 미분하면 $dZ/dd=-fb/d^2=-Z^2/(fb)$이므로, 시차 오차 $\Delta d$ 픽셀은 깊이를 약 $Z^2\Delta d/(fb)$만큼 옮긴다. 이 리그에서는 $fb=600\times0.12=72$ px·m이므로 1픽셀이 랜드마크의 $2$ m에서 $4/72=0.056$ m, 곧 거리의 $2.8\%$이고, $8$ m에서는 $64/72=0.89$ m다. 그림에 그린 오차 막대가 그것이다. 위 스테레오 예제의 가로 방향 1픽셀 $Z/f$와 견주면 두 오차의 비는 $Z/b$다. $2$ m에서 $16.7$, $8$ m에서 $67$이고, 스테레오 점의 불확실성이 공이 아니라 광선을 따라 늘어난 바늘인 이유가 그것이다. 1차 값은 양쪽의 정확한 오차 사이에 있고, 두 정확한 오차는 같지 않다($8$ m에서 $d=8$이면 $+1.00$ m, $d=10$이면 $-0.80$ m). 왜 그런지는 과제 2(b)가 묻는다.

**같은 법칙을 거꾸로 돌리면 리그의 크기가 정해진다.** $2$ m에서 매칭 오차 1픽셀로 $\pm1$ cm를 지키려면 $fb\ge Z^2/\Delta Z=4/0.01=400$ px·m, 곧 $f=600$ px에서 기선 $0.67$ m가 필요하다. 이 리그의 다섯 배가 넘는다. 서브픽셀 매칭이 그것을 되사 준다. $0.2$ px까지 맞추는 매처라면 $0.13$ m면 된다. 논문이 스테레오 깊이 오차를 인용하면 어느 거리에서인지 물어라. 같은 리그의 $4$ m 오차는 $1$ m 오차의 열여섯 배다.

**스테레오에는 가까운 쪽 한계도 있다.** P5의 판독값 $12$ cm에서는 시차가 $72/0.12=600$ px로 $640$ px 폭을 거의 다 차지하므로 두 시점이 거의 겹치지 않고, 시차를 $128$ px까지만 찾는 매처는 $72/128=0.56$ m보다 가까운 것을 아무것도 보지 못한다. 리그가 패널까지의 거리를 스테레오가 아니라 P5의 스칼라 센서에서 받는 이유가 그 사각지대이고, 과제가 그것을 융합한다.

### 2.5 이미지 특징: 검출, 기술, 매칭

**한 문장으로:** 다른 이미지에서 다시 찾을 수 있는 점 수백 개를 고르고, 점마다 짧은 지문을 붙이고, 이미지 사이에서 지문을 짝짓는다. 그 짝이 모든 기하 단계가 필요로 하는 대응점이다.

왜 모든 픽셀이 아니라 드문드문한 점인가? §2의 스테레오 깊이는 왼쪽 이미지의 픽셀이 오른쪽 어느 픽셀과 같은 점인지 알아야 한다. §5의 보정은 타깃 모서리, 곧 리그의 $A$, $B$, $C$를 서브픽셀 정확도로 찾아야 한다. Visual odometry와 SLAM([[04-robotics/state-estimation-slam|상태 추정]])은 같은 점을 프레임마다 추적해 pose를 제약한다. 점이 쓸모 있으려면 **반복성**(시점이 바뀌어도 다시 검출됨)과 **변별성**(주변이 다른 많은 곳과 닮지 않음)을 갖춰야 한다. 파이프라인은 세 단계이고, 논문은 그중 어느 단계든 바꿀 수 있다.

**검출: 모든 방향으로 변하는 곳.** 작은 창을 $(u,v)$만큼 옮기고 내용이 얼마나 바뀌는지 잰다. 1차 테일러 전개로 $I(x+u,y+v)\approx I(x,y)+I_x u+I_y v$이므로 픽셀마다 차이는 $I_x u+I_y v$이고, 그 제곱 $I_x^2u^2+2I_xI_y\,uv+I_y^2v^2$은 $(u,v)$의 이차식이다. 따라서 창 전체에서 더하면 변화가 이차 형식이 된다.

$$E(u,v)=\sum_{x,y} w(x,y)\,\big(I(x+u,y+v)-I(x,y)\big)^2 \approx (u,v)\,M\,(u,v)^\top$$

그래서 전체 거동은 2×2 행렬 하나, 곧 **구조 텐서** 하나가 정한다. 창 안의 영상 기울기 $I_x, I_y$를 가중치 $w$(상자 또는 가우시안)로 더한 것이다.

$$M=\sum_{x,y} w(x,y)\begin{pmatrix}I_x^2 & I_xI_y\\ I_xI_y & I_y^2\end{pmatrix}$$

고윳값 $\lambda_1 \le \lambda_2$는 가장 덜 변하는 이동 방향과 가장 많이 변하는 이동 방향의 변화량이므로, 창을 이렇게 분류한다.

- **평탄**: 둘 다 작다 — 어느 쪽으로 옮겨도 변화가 없다.
- **에지**: 하나는 크고 하나는 거의 0이다 — 에지를 따라 미끄러지면 변화가 없으므로 그 방향으로는 위치를 정할 수 없다(aperture 문제).
- **코너**: 둘 다 크다 — 어떤 이동도 드러나므로 점이 2D로 고정된다.

Harris와 Stephens(Alvey Vision Conference, 1988)는 고윳값 분해 없이 다음 응답을 쓴다.

$$R=\det M-k\,(\operatorname{tr}M)^2=\lambda_1\lambda_2-k\,(\lambda_1+\lambda_2)^2$$

행렬식과 대각합이 고윳값의 곱과 합이기 때문에 이 식이 통한다. $R$은 코너에서 크고 양수, 에지에서 음수, 평탄한 영역에서 0 근처다. $k$는 경험적 상수로 흔히 0.04–0.06을 쓴다. Shi와 Tomasi("Good Features to Track", CVPR 1994)는 $\min(\lambda_1,\lambda_2)$를 직접 점수로 써서 $k$를 없앤다. 어느 쪽이든 문턱값을 넘는 국소 최댓값만 남긴다(non-maximum suppression).

**스케일: SIFT.** Harris는 회전에는 불변이지만 스케일에는 불변이 아니다. 한 배율의 코너가 다른 배율에서는 둥근 곡선이다. Lowe의 SIFT(IJCV 2004)는 스케일 방향으로도 탐색하며, 세 단계로 이루어진다.

- *스케일에 걸쳐 검출.* $\sigma$를 키워 가며 가우시안으로 흐리게 한 뒤 이웃 단계끼리 빼고(difference of Gaussians, 스케일 정규화 라플라시안의 값싼 근사 — 흐림 폭이 덩어리 크기와 비슷할 때 응답이 가장 커지는 blob 검출기), 공간과 스케일의 이웃 26개 가운데 극값인 점을 남긴다.
- *버리기.* 대비가 낮은 점과 에지 같은 점은 버리는데, 에지 판정은 위와 같은 논리로 2×2 헤시안의 고윳값 비를 쓴다.
- *기술.* 키포인트마다 지배적인 기울기 방향을 붙이고, 그 회전·스케일 좌표계에서 기술자를 계산한다. 점 주위를 4×4 칸으로 나누고 칸마다 기울기 방향의 8구간 히스토그램을 만들면 4·4·8 = 128개의 수가 된다. 조명 영향을 줄이도록 정규화하고 유클리드 거리로 비교한다.

**이진: ORB.** SIFT 기술자는 실수 벡터이고 계산이 비교적 무겁다. ORB(Rublee 외, ICCV 2011)는 각 단계를 더 값싼 것으로 바꾼다.

- *검출:* FAST 코너 검사(후보 주위 원 위의 픽셀을 빠르게 비교)를 Harris 점수로 순위를 매겨 쓴다.
- *방향:* 패치의 밝기 중심(intensity centroid)으로 각도를 정한다.
- *기술:* 회전시킨(steered) BRIEF 기술자, 곧 픽셀 쌍의 밝기 비교 256개를 비트로 저장한 것이다.

두 기술자는 **해밍 거리**, 곧 XOR 후 켜진 비트 수로 비교하며 CPU 명령 몇 개면 계산된다. ORB-SLAM(Mur-Artal 외, IEEE T-RO 2015)이 추적·지도 작성·재위치 추정·루프 닫기에 모두 ORB를 쓰는 이유는 CPU에서 프레임 속도로 추출·매칭할 수 있고, 회전에 불변이며, 적당한 시점 변화를 견디기 때문이다. ORB 자체는 스케일 불변이 아니어서 이미지 피라미드 위에서 추출한다.

**매칭: 최근접 이웃, 그다음 거르기.** 이미지 A의 기술자마다 이미지 B에서 가장 가까운 기술자를 찾는다. 날것의 최근접 짝에는 틀린 쌍이 많아서 세 가지 거르기가 뒤따른다.

1. **비율 검사**(Lowe 2004): 가장 가까운 후보와 두 번째 후보까지의 거리를 $d_1, d_2$라 할 때 $d_1/d_2 < 0.8$일 때만 받아들인다. 변별력 있는 점에는 확실한 1등이 있고, 반복 패턴 위의 점에는 거의 같은 후보가 둘 있다. Lowe는 자신의 데이터에서 0.8이 틀린 매칭의 약 90%를 없애면서 맞는 매칭은 5% 미만만 버렸다고 보고한다.
2. **상호 검사**: 역방향으로도 $a$가 $b$의 최근접 이웃일 때만 $a\leftrightarrow b$를 남긴다.
3. **기하 검증**: 남은 짝은 하나의 카메라 운동과 맞아야 한다. RANSAC(Fischler & Bolles, CACM 1981)은 무작위 최소 표본에 모델 — fundamental 또는 essential 행렬, homography, PnP pose — 을 맞추기를 반복하고 인라이어가 가장 많은 모델을 남긴다. 표본 수 계산은 [[02-foundations/algorithms/robotics-ai-problems|11.8 §3 RANSAC 직선 맞춤]]에서 직접 해 본다. §4의 ICP 경고가 그대로 적용된다. 틀린 대응에 대한 최소제곱은 자신 있게 틀린다.

**학습된 특징.** SuperPoint(DeTone 외, CVPR Workshops 2018)는 한 네트워크가 키포인트와 기술자를 함께 출력하도록 학습한다. SuperGlue(Sarlin 외, CVPR 2020)는 최근접 이웃과 비율 검사를 두 점 집합을 한꺼번에 짝짓는 그래프 신경망으로 바꾼다. LoFTR(Sun 외, CVPR 2021)은 검출기를 없애고 트랜스포머 특징을 조밀하게 매칭해, 검출기가 점을 거의 찾지 못하는 저텍스처 영역을 겨냥한다. 각 논문은 자기 벤치마크의 큰 시점·조명 변화에서 더 강한 매칭을 보고한다. 그래도 고전 특징이 맞는 선택일 수 있다. 임베디드 로봇 컴퓨터의 연산 예산과 프레임 속도, 학습 데이터가 내 장면과 닮았는지를 따져라. 맨 석고보드, 거푸집, 철근 격자, 똑같은 외벽 패널처럼 무늬가 없거나 반복되는 건설 현장 표면은 어떤 방법에도 어렵다. 벤치마크 순위를 믿기보다 자기 시퀀스에서 시험하라.

**학습된 계열, 나란히 놓고 보기.** 계열의 방법마다 바꾸는 단계가 다르다. SuperGlue는 attention과, 짝이 없는 점을 남겨 둘 수 있는 최적 수송 배정으로 매칭하며 GPU에서 실시간으로 돈다. 그 후속인 LightGlue(Lindenberger 외, ICCV 2023)는 겹침이 큰 쉬운 쌍에 계산을 덜 써서 지연에 민감한 용도를 겨냥한다. LoFTR의 조밀 매칭은 맨 거푸집처럼 검출기가 아무것도 찾지 못하는 곳에서 돕는다. 3D 기반 모델(foundation model)은 질문 자체를 바꾼다. DUSt3R(Wang 외, CVPR 2024)는 보정도 자세도 없이 이미지 쌍의 3D point map을 회귀하고, 매칭과 상대 카메라가 거기서 따라 나온다. MASt3R(Leroy 외, ECCV 2024)는 매칭하도록 학습한 기술자를 더한다. [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]](Wang 외, CVPR 2025)는 수백 장까지의 시점에 대해 카메라, 깊이, 트랙을 한 번의 순전파로 예측하며, 복원이 1초 안에 끝난다고 보고한다. 어느 것도 세 번째 거르기를 생략하게 해 주지 않는다. 그 매칭도 F, E, H, PnP(§2.7)로 하는 RANSAC으로 검사해야 하고, 패널 한 칸 밀려 매칭된 외벽은 여전히 운동 하나에 맞으므로 그 검사도 통과한다.

> [!example] 계산 예제 · Worked example
> **리그의 보정 이미지 위의 Harris.** 이 예제에서는 보정 타깃을 어두운 배경 위의 밝은 판 하나로, $A$를 그 왼쪽 위 코너로 모델링한다. 카메라 1은 $A$를 주점 $(320, 240)$에서 보고, 판은 오른쪽으로 $(470, 240)$의 $B$까지, 아래로 $(320, 360)$의 $C$까지 뻗는다. 그 이미지에서 배경은 밝기 0, 판은 10인 5×5 패치 세 개를 잡는다. 안쪽 3×3 픽셀에서 중앙 차분 $I_x=(I_{x+1}-I_{x-1})/2$를 쓰고, $w=1$, $k=0.05$로 둔다.
> - **평탄**, 판 안쪽 $(395, 300)$ 근처 (전부 10): 기울기가 모두 0이므로 $M=0$, $\lambda=(0,0)$, $R=0$이다.
> - **에지**, $A$와 $C$ 사이 판의 왼쪽 경계 $(320, 300)$ 근처 (왼쪽 두 열 0, 나머지 10): $I_x=5$인 픽셀이 6개이고 $I_y=0$이므로 $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$, $R=0-0.05\cdot150^2=-1125$다.
> - **코너**, $A$를 중심으로 (오른쪽 아래 3×3 블록만 밝음): $I_x=5$인 픽셀 4개, $I_y=5$인 픽셀 4개, 둘 다인 픽셀 1개이므로 $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$, $R=9375-0.05\cdot200^2=7375$다.
>
> 부호가 규칙대로다 — 평탄 0, 에지 음수, 코너 양수. Shi–Tomasi 점수는 0, 0, 75다. 두 이미지 방향 모두에서 위치를 잡을 수 있는 것은 $A$의 패치뿐이고, 보정이 타깃의 경계 위 점이 아니라 코너를 검출하는 이유가 그것이다.
>
> **$L$ 위의 비율 검사.** 카메라 1이 패널을 찍은 이미지에서 $(470, 300)$에 있는 $L$의 기술자를 카메라 2의 후보들과 비교한다. $(434, 300)$의 참 짝은 거리 0.20, 옆 패널의 같은 특징인 $(440, 300)$은 0.23, 무관한 점 하나는 0.61에 있다. $0.20/0.23=0.87>0.8$이므로 가장 가까운 후보가 옳은 짝인데도 매칭을 버린다. 비슷한 후보가 둘이면 대개 반복 구조이고, 검사는 둘 중 어느 쪽이 참인지 가리지 못한다. 틀린 쪽을 받아들이면 무엇을 치르는지는 §2.6이 보여 준다. $(440, 300)$은 epipolar 검사를 통과하고 $40$ cm 멀리 삼각측량된다. 세 번째 거리는 아무 역할도 하지 않는다. 두 번째가 0.45였다면 $0.20/0.45=0.44$로 통과했을 것이다.

같은 응답을 그 보정 이미지에서 $A$ 둘레를 잘라 낸 20×20 조각에 계산하는 코드다. 판이 조각의 오른쪽 아래 사분면을 채우고, $A$의 픽셀 점수가 가장 큰지 확인한다.

```python
import numpy as np

def harris(img, k=0.05):
    Iy, Ix = np.gradient(img.astype(float))          # axis 0 is y (rows), axis 1 is x
    def box3(a):                                     # window sum with w = 1 on a 3x3 patch
        p = np.pad(a, 1)
        return sum(p[i:i + a.shape[0], j:j + a.shape[1]] for i in range(3) for j in range(3))
    Sxx, Syy, Sxy = box3(Ix * Ix), box3(Iy * Iy), box3(Ix * Iy)
    return Sxx * Syy - Sxy**2 - k * (Sxx + Syy)**2   # det M - k (tr M)^2 at every pixel

img = np.zeros((20, 20))
img[10:, 10:] = 1.0                                  # the plate; crop pixel (10, 10) is A at (320, 240)
R = harris(img)
r, c = np.unravel_index(np.argmax(R), R.shape)
print(r, c, round(R.max(), 3), round(R[15, 10], 3), R[3, 3])   # 10 10 0.738 -0.112 0.0
assert (r, c) == (10, 10) and R[15, 10] < 0 and R[3, 3] == 0     # corner > 0, edge < 0, flat 0
```

> [!warning] 매칭 주장 읽기 · Reading matching claims
> - 매칭 개수는 정확도가 아니다. 기하 검증 뒤의 인라이어 비율과 그다음 단계의 pose 오차를 찾아라.
> - 비율 문턱값, RANSAC 픽셀 문턱값, 모델(F, E, H, PnP)을 적어 두라. 결과가 이 모두에 따라 움직인다.
> - 반복 구조는 일관되게 틀린 매칭을 만들 수 있다. 외벽 패널 한 칸만큼 밀린 매칭 집합도 하나의 운동에 맞아 RANSAC을 통과한다. 이미지 버전의 §4 경고다.
> - Harris와 FAST는 그 자체로 스케일 불변이 아니다. 스케일을 어떻게 다루는지(피라미드인지 스케일 공간인지) 확인하라.
> - 학습된 매처라면 학습 데이터, 입력 해상도, GPU, 보고된 시간에 검출이 포함되는지 확인하라.

### 2.6 두 시점: epipolar 제약과 삼각측량

§2.5는 후보 대응점을 만들었다. 남은 질문이 둘이다. 그중 어느 것이 기하적으로 가능하기나 한가, 그리고 살아남은 짝이 어떤 3D 점을 뜻하는가. 첫째는 3D 점이 필요 없는 제약이 답하고, 둘째는 그 점을 푸는 것이 답한다.

**Epipolar 제약의 완전한 정의.** 두 카메라가 보는 3D 점 하나를 잡는다. 두 광학 중심과 그 점이 평면 하나를 — **epipolar 평면** — 펼치고, 각 이미지는 그 평면을 선 하나로 본다. 그래서 이미지 1의 한 점에 대응하는 짝은 이미지 2의 아무 데나 있을 수 없고 **선 하나**, 곧 **epipolar 선** 위에 있어야 한다. 동차 픽셀 좌표 $\tilde u_1, \tilde u_2$ 와 정규화 좌표 $\hat x_i = K_i^{-1}\tilde u_i$ 로 대수적으로 쓰면 제약은 스칼라 방정식 하나다.

$$\hat x_2^\top E\, \hat x_1 = 0, \qquad \tilde u_2^\top F\, \tilde u_1 = 0$$

$\hat x_1$, $\hat x_2$, 기선 $t$ 가 같은 평면에 있고, 공면인 벡터들의 삼중곱이 0이기 때문에 성립한다.

- **Essential matrix** $E = [t]_\times R$ 는 **보정된**(정규화) 좌표에서 작동한다. $R, t$ 는 첫 카메라에 대한 둘째 카메라의 회전과 평행 이동이고 $[t]_\times$ 는 $[t]_\times a = t \times a$ 인 반대칭 행렬, 곧 행렬로 쓴 외적이다([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §1]]). 자유도는 **다섯**이다 — $R$ 에서 셋, $t$ 에서 셋, 스케일을 복원할 수 없어 하나를 뺀다 — 특잇값은 $(\sigma, \sigma, 0)$ 이라 rank 2다.
- **Fundamental matrix** $F = K_2^{-\top} E K_1^{-1}$ 는 **픽셀**에서 작동하므로 보정이 전혀 필요 없다. 자유도는 **일곱**이다: 성분 아홉에서 전체 스케일로 하나, $\det F = 0$ 으로 하나를 뺀다. 이것도 rank 2다.
- 둘 다 **스케일을 빼고서만** 정의된다. 어느 쪽에 상수를 곱해도 제약 $=0$ 은 그대로이기 때문이다.
- 이 제약은 **필요조건이지 충분조건이 아니다.** 2차원 짝을 1차원 선으로 줄여 자유도 둘 중 하나를 없앨 뿐이다. 그 선 위의 모든 것이 여전히 통과한다.

*리그에서의 예.* $R = I$, $t = (-0.12, 0, 0)$ 이므로

$$E = [t]_\times = \begin{pmatrix}0&0&0\\0&0&0.12\\0&-0.12&0\end{pmatrix}, \qquad 5000\,F = \begin{pmatrix}0&0&0\\0&0&1\\0&-1&0\end{pmatrix}$$

$L$ 의 짝은 $\hat x_1 = (0.25, 0.10, 1)$, $\hat x_2 = (0.19, 0.10, 1)$ 이고 $E\hat x_1 = (0,\ 0.12,\ -0.012)$, $\hat x_2^\top(0, 0.12, -0.012) = 0.012 - 0.012 = 0$ 으로 정확히 0이다. 픽셀에서 epipolar 선은 $\ell_2 = F\tilde u_1 \propto (0,\ 1,\ -300)$, 곧 $v = 300$ 이다. Rectify된 리그에서는 모든 epipolar 선이 스캔라인이고, 매칭 전에 스테레오 리그를 rectify하는 이유가 전부 그것이다.

*위반을 어떻게 재는가.* 스칼라 $\tilde u_2^\top F \tilde u_1$ 은 단위가 없는 *대수적* 잔차이므로, 문턱을 걸기 전에 **픽셀 단위 점-선 거리**로 바꾼다.

$$d_\perp = \frac{\lvert \tilde u_2^\top F \tilde u_1 \rvert}{\sqrt{\ell_1^2 + \ell_2^2}}, \qquad \ell = F\tilde u_1$$

$(434, 300)$ 대신 $(434, 303)$ 인 후보는 대수적 잔차가 $6\times10^{-4}$, $d_\perp = 3.0$ px다. 수평 epipolar 선에서는 당연히 수직 어긋남 그대로다. 이 논문들의 RANSAC 문턱이 픽셀로 인용되는 이유가 그 변환이다.

*반례, 그리고 이것이 위험한 쪽이다.* 같은 행에서 반복 패널 하나 옆인 $(440, 300)$ 의 짝은 epipolar 잔차가 **정확히 0**이다. $F$ 를 통과하고, RANSAC을 통과하고, $(0.50, 0.20, 2.00)$ m가 아니라 $(0.60, 0.24, 2.40)$ m로 삼각측량된다 — $40$ cm 멀다. Epipolar 제약은 epipolar 선을 *따라가는* 대응점 오류를 잡지 못하고, 반복 구조에서는 바로 그 오류가 난다. §2.5의 경고와 §4 ICP의 경고를 숫자 하나로 합친 것이다.

**삼각측량의 완전한 정의.** 알려진 카메라 행렬 둘 $P_1, P_2$(각각 $3\times4$, $P_i = K_i[R_i \mid t_i]$)와 대응 짝 $\tilde u_1, \tilde u_2$ 가 주어지면, 삼각측량은 두 광선이 함께 지나는 3D 점 $\tilde X$ 를 돌려준다. 측정 잡음 때문에 두 광선은 대개 **만나지 않으므로**, 이것은 작도가 아니라 최소자승 문제다. 표준 **DLT** 형태는 외적 제약 $\tilde u_i \times P_i\tilde X = 0$ 의 세 행 중 독립인 두 행씩을 쌓아 $A\tilde X = 0$ 을 만든다.

$$A = \begin{pmatrix} u_1 P_1^{3\top} - P_1^{1\top}\\ v_1 P_1^{3\top} - P_1^{2\top}\\ u_2 P_2^{3\top} - P_2^{1\top}\\ v_2 P_2^{3\top} - P_2^{2\top}\end{pmatrix}$$

$P_i^{j\top}$ 는 $P_i$ 의 $j$ 번째 행이고, $\tilde X$ 는 $A$ 의 가장 작은 특잇값에 대응하는 오른쪽 특이벡터다. 그것이 $\lVert A\tilde X\rVert$ 를 최소화하는 단위 벡터이기 때문이다. Rectify된 리그에서는 해가 닫힌 형태로 주저앉는다.

$$Z = \frac{f b}{d}, \qquad X = \frac{(u_1 - c_x)Z}{f_x}, \qquad Y = \frac{(v_1 - c_y)Z}{f_y}, \qquad d = u_1 - u_2$$

*예:* $L$ 의 짝에 DLT를 돌리면 닫힌 형태와 똑같이 $(0.5, 0.2, 2.0)$ m가 나온다. 리그에 잡음이 없고 rectify되어 있기 때문이다. *$Z^2$ 법칙이 나오는 곳:* $Z = fb/d$ 를 미분하면 $\partial Z/\partial d = -fb/d^2 = -Z^2/(fb)$ 이므로 시차 1픽셀 오차는 $Z^2/(fb)$ 미터의 값이다 — $Z = 2$ 에서 $0.056$ m, $Z = 8$ 에서 $0.889$ m로, 거리 4배에 열여섯 배다. *반례(퇴화):* 기선이 0으로 줄거나 점이 멀어지면 $d \to 0$ 이고 두 광선이 평행해지므로 $A$ 가 rank를 잃고 $Z$ 가 구속되지 않는다. 논문의 "삼각측량 실패"는 solver 버그가 아니라 거의 항상 이것이다.

### 2.7 2D–3D 대응에서 자세로: PnP

*한 문장으로:* 대응마다 픽셀이 물체 위에서 이미 아는 점과 짝지어져 있으면 보정된 이미지 한 장이 물체의 자세를 미터 단위로 주지만, 점 셋은 답을 여럿 남기고 점 넷도 기울기에서는 약할 수 있다.

**문제.** 공구를 이미 아는 물체, 곧 §5의 타깃이나 부품이나 S1의 외장 패널에 가져다 대려면 로봇은 이미지 한 장에서 그 물체의 자세를 미터 단위로 알아야 한다. §2.6은 픽셀을 픽셀과 짝지었고 운동을 스케일을 빼고서만 복원했다. 여기서는 대응의 한쪽이 이미 아는 모델의 점이고, 그 모델이 미터를 정한다. 이 절은 고정된 리그에 네 번째 타깃 코너 $D=(0.5,\ 0.4,\ 2)$ m를 더한다. 나머지 세 코너가 암시하는 직사각형을 완성하는 점이다. $B-A=(0.5,0,0)$ 와 $C-A=(0,0.4,0)$ 가 수직이고 $A+(B-A)+(C-A)=D$ 다. 카메라 1은 네 코너를 다음 자리에서 본다.

$$A\to(320,\,240),\qquad B\to(470,\,240),\qquad C\to(320,\,360),\qquad D\to(470,\,360)\ \text{px}$$

§1에 따라 각각 $u=600X/2+320$, $v=600Y/2+240$ 이기 때문이다.

> **Perspective-n-Point(PnP)의 정의.** **PnP**는 *추정 문제*다. 알고 있는 물체를 카메라 프레임에 놓는 강체 변환을, 그 물체를 찍은 이미지 한 장에서 찾는다. 정의 조건이 다섯이고, 하나를 빼면 다른 문제가 된다. 물체의 **점들은 물체 자신의 프레임에서 알려져** 있다. $X_j$ 는 모델이나 인쇄된 타깃에서 온다. 점마다 **픽셀 $\tilde u_j$ 가 주어진다**. 대응을 찾는 일은 §2.5의 몫이다. 카메라는 **보정되어** 있다. $K$ 와 왜곡을 안다(§1). 미지수는 **자세 하나**, 곧 $R\in SO(3)$ 와 $t\in\mathbb R^3$ 이고, 모델이 미터 단위이므로 남는 스케일이 없다. 그리고 **점이 충분하다**. 한 직선 위에 있지 않은 점 셋은 유한 개의 자세를 남기고, 한 평면 위에 있으면서 어느 셋도 한 직선 위에 있지 않은 점 넷은 픽셀이 정확할 때 자세 하나를 남긴다.
>
> $$(\hat R,\hat t)=\arg\min_{R\in SO(3),\ t\in\mathbb R^3}\ \sum_{j=1}^{n}\big\lVert\,\tilde u_j-\pi\big(K,\ RX_j+t\big)\big\rVert^2$$
>
> 여기서 $\pi$ 는 카메라 프레임의 점을 §1처럼 왜곡까지 넣어 픽셀로 보내고, 각 항은 §5의 재투영 오차 제곱이다. 그래서 최소점은 등방 가우시안 픽셀 잡음 아래의 최대우도 자세다.
>
> - **예**: 위의 네 코너이고, $X_j$ 는 $A$ 에 원점을 두고 축이 카메라 축과 같은 타깃 프레임에서 쓴다. 최소점은 $R=I$, $t=(0,0,2)$ m이고 잔차는 0이다. §5 hand–eye 예의 $T_{c_1t}$ 가 바로 이것이다.
> - **비예**: $t$ 를 카메라의 위치로 읽는 것. $t$ 는 카메라 프레임에서 타깃이 놓인 자리이고, 카메라는 타깃 프레임에서 $-R^\top t=(0,0,-2)$ m에 있다. §1의 extrinsics 함정이다.
> - **비예**: §2.6의 두 시점 문제. 대응의 양쪽이 모두 픽셀이고, 미터를 정해 줄 모델이 없다.
> - **왜 중요한가**: 이 절 끝에 모은 쓰임 — hand–eye 보정, 파지, S1의 패널 — 이 모두 이 최소화를 돌린다.

**점 셋: P3P의 답은 여럿이다.** 알려진 점은 저마다 자기 픽셀의 광선 위 어딘가에 있으므로 점 셋은 모르는 거리 셋을 남기고, 세 변의 길이가 광선 쌍마다 코사인 법칙 하나씩, 식 셋을 준다. 거리 둘을 소거하면 4차식이 남는다. 해는 최대 넷이고, Persson과 Nordberg(ECCV 2018)도 그렇게 적는다. 기하로 보면 $C$ 를 지나는 광선이 $A$ 둘레 반지름 $|AC|$ 의 구를 두 번 자르고, $B$ 도 마찬가지다. 리그의 $A$, $B$, $C$ 로 P3P를 풀면 세 코너를 정확히 재투영하는 자세 셋이 나온다. 참 자세, 모서리 $AB$ 둘레로 $22.62°$ 기운 타깃($\tan=5/12$), 그리고 $AC$ 둘레로 $28.07°$ 기운 타깃($\tan=8/15$)이다. 둘째에서는 $C$ 가 자기 광선을 따라 $(0,\ 0.369,\ 1.846)$ m로 미끄러졌는데도 여전히 $A$ 에서 $0.4$ m, $B$ 에서 $0.640$ m 떨어져 있고, 셋째에서는 $B$ 가 $(0.441,\ 0,\ 1.765)$ m에 있다.

**네 번째 점이나 사전 정보가 하나를 고른다.** P3P는 $D$ 를 쓰지 않았으므로 $D$ 는 공짜 검사다. 참 자세는 $D$ 를 보이는 자리 $(470,\ 360)$ 에 놓고, 가짜 둘은 $(482.5,\ 360)$ 과 $(470,\ 376)$ 에 놓아 $12.5$ px와 $16.0$ px 어긋난다. 사전 정보도 같은 일을 한다. 베이스 프레임에서 타깃이 대략 어디 있는지 알면 엔코더와 §5의 hand–eye 변환이 그 기울기를 몇 도 안으로 예측하고, 그것만으로 가짜 둘이 배제된다. 왜 넷이 아니라 셋인가? 카메라가 $A$, $B$, $C$ 를 지나고 그 평면에 수직인 원기둥 위에 있기 때문이다. 세 점의 원은 $BC$ 를 지름으로 하는 반지름 $0.320$ m의 원이고, 카메라 바로 앞의 점 $A$ 를 지난다. 오래전부터 P3P의 불안정성과 이어져 온 이 *위험 원기둥*(danger cylinder) 위에서는 참 자세가 중근이 되어 해가 셋만 남는다(Wang, Hu, Zhang, 2019). 이 리그의 숫자에서도 그대로 드러난다. $A$ 의 검출을 왼쪽으로 $0.1$ px 옮기면 참 근이 사라져 가짜 둘만 남고, 오른쪽으로 $0.1$ px 옮기면 참 근이 $A$ 를 $1.987$ m와 $2.013$ m에 놓는 두 자세로 갈라진다. P3P는 후보를 낼 뿐 측정하지 않는다.

<svg viewBox="0 0 560 300" style="max-width:100%;height:auto" role="img" aria-label="손목 리그의 P3P: 왼쪽은 옆에서 본 그림으로, 코너 C를 지나는 광선이 A 둘레 0.4 m 구를 C와 C′에서 만나므로 AB 둘레로 22.6도 기운 타깃도 A, B, C에 맞는다. 오른쪽은 이미지로, 가짜 자세 둘에서 D는 470, 360 픽셀이 아니라 482.5, 360과 470, 376 픽셀에 떨어진다">
  <text x="16" y="20" font-size="12" fill="currentColor" font-weight="600">X = 0 평면을 옆에서, 축척대로</text>
  <text x="300" y="20" font-size="12" fill="currentColor" font-weight="600">이미지, px, 축척대로</text>
  <line x1="16.0" y1="48.0" x2="270.0" y2="48.0" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <line x1="16.0" y1="168.0" x2="268.0" y2="218.4" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.55" stroke-dasharray="4 3"/>
  <path d="M265.4 200.2 A160.0 160.0 0 0 1 97.1 155.1" fill="none" stroke="currentColor" stroke-width="1.0" stroke-opacity="0.6"/>
  <line x1="216.0" y1="48.0" x2="216.0" y2="208.0" stroke="currentColor" stroke-width="2.2"/>
  <line x1="216.0" y1="48.0" x2="154.5" y2="195.7" stroke="currentColor" stroke-width="2.2" stroke-dasharray="6 3"/>
  <path d="M216.0 88.0 A40 40 0 0 1 200.6 84.9" fill="none" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="216.0" cy="48.0" r="3.6" fill="currentColor" stroke="none"/>
  <circle cx="216.0" cy="208.0" r="3.6" fill="currentColor" stroke="none"/>
  <circle cx="154.5" cy="195.7" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="223.0" y="44.0" font-size="12" fill="currentColor">A</text>
  <text x="222.0" y="199.0" font-size="12" fill="currentColor">C</text>
  <text x="146.5" y="185.7" font-size="12" fill="currentColor" text-anchor="end">C′</text>
  <text x="221.0" y="84.0" font-size="11" fill="currentColor">22.6°</text>
  <text x="222.0" y="132.0" font-size="11" fill="currentColor">0.4 m</text>
  <text x="177.2" y="125.8" font-size="11" fill="currentColor" text-anchor="end">0.4 m</text>
  <text x="103.1" y="140.1" font-size="11" fill="currentColor" fill-opacity="0.85" text-anchor="middle">A에서 0.4 m인 점들</text>
  <text x="16" y="272" font-size="11" fill="currentColor" fill-opacity="0.9">실선: 참 타깃 · 점선: AB 둘레로 22.6° 기운 것</text>
  <text x="16" y="288" font-size="11" fill="currentColor" fill-opacity="0.8">카메라는 2 m 왼쪽, A를 지나는 광선 위에 있다</text>
  <path d="M311.0 55.5 L476.0 55.5 L476.0 187.5 L311.0 187.5 Z" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="311.0" cy="55.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="476.0" cy="55.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="311.0" cy="187.5" r="3.4" fill="currentColor" stroke="none"/>
  <circle cx="476.0" cy="187.5" r="3.4" fill="currentColor" stroke="none"/>
  <line x1="476.0" y1="187.5" x2="489.8" y2="187.5" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="489.8" cy="187.5" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <line x1="476.0" y1="187.5" x2="476.0" y2="205.1" stroke="currentColor" stroke-width="1.0"/>
  <circle cx="476.0" cy="205.1" r="3.6" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="317.0" y="71.5" font-size="11" fill="currentColor">A (320, 240)</text>
  <text x="470.0" y="71.5" font-size="11" fill="currentColor" text-anchor="end">B (470, 240)</text>
  <text x="317.0" y="179.5" font-size="11" fill="currentColor">C (320, 360)</text>
  <text x="470.0" y="179.5" font-size="11" fill="currentColor" text-anchor="end">D (470, 360)</text>
  <text x="495.8" y="181.5" font-size="11" fill="currentColor">12.5 px</text>
  <text x="484.0" y="215.1" font-size="11" fill="currentColor">16.0 px</text>
  <text x="300" y="240" font-size="11" fill="currentColor" fill-opacity="0.9">● 보이는 자리 · ○ 가짜 자세 둘에서의 D</text>
  <text x="300" y="256" font-size="11" fill="currentColor" fill-opacity="0.9">A, B, C는 세 자세 모두에서 같다</text>
</svg>

왼쪽은 $X=0$ 평면을 옆에서 축척대로 본 것이다. $C$ 의 픽셀을 지나는 광선이 $A$ 둘레 반지름 $0.4$ m의 구를 $C$ 와 $C'=(0,\ 0.369,\ 1.846)$ m에서 만나므로, $AB$ 둘레로 $22.6°$ 기운 타깃도 $A$, $B$, $C$ 에 맞는다. 오른쪽은 이미지로, 그 가짜 자세에서 $D$ 는 검출된 자리에서 $12.5$ px, $AC$ 둘레로 $28.1°$ 기운 가짜 자세에서는 $16.0$ px 떨어진 곳에 맺힌다.

**점 넷 이상: 재투영 오차를 최소화한다.** $n\ge4$ 이면 목적함수는 미지수 여섯, 잔차 $2n$ 개의 비선형 최소자승이고, Gauss–Newton이나 Levenberg–Marquardt로 푼다([[02-foundations/optimization|4. 최적화 §3.5]]). 회전은 $R\leftarrow\operatorname{Exp}(\delta\omega)R$ 로 갱신해 계속 회전으로 남게 한다([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §2]]). 국소적인 방법이므로 P3P 후보에서, 평면 타깃이라면 아래의 homography에서 출발한다. 영어 절반의 코드는 $10.4°$, $0.55$ m 어긋난 곳에서 출발하고, RMS 재투영 오차가 $49.4$ px에서 $18$, $1.25$, $0.0073$, $3\times10^{-7}$ px로 네 스텝 만에 떨어져 $R=I$, $t=(0,0,2)$ m에 닿는다.

**한 장의 이미지는 얼마나 좋은가?** 해에서 선형화하고, $J$ 를 자세에 대한 픽셀의 $8\times6$ 야코비안, 픽셀 잡음을 서로 독립인 $\sigma$ 로 두면 자세의 공분산은 $\sigma^2(J^\top J)^{-1}$ 이다. $\sigma=1$ px에서 코드는 타깃까지의 거리를 $\pm13.2$ mm, 시선 둘레의 roll을 $\pm0.37°$ 로 주지만, 두 기울기는 각각 $\pm2.70°$ 로밖에 주지 못한다. 셋은 저마다 지렛대가 다르다. 거리는 겉보기 크기에서 온다. $150$ px 폭에서 1픽셀은 $Z^2/(f\ell)=13.3$ mm, §6의 알려진 길이다. Roll은 모서리 방향에서 온다. $150$ px에 걸친 1픽셀은 $0.38°$ 다. 기울기는 이미지가 크기만 바뀐 직사각형에서 얼마나 벗어나느냐에서만 온다. $10°$ 를 기울여도 가까운 모서리가 먼 모서리보다 $5.2$ px 길어질 뿐이다. $fWH\sin\theta/Z^2$ 이고 $fWH/Z^2=30$ px/rad다. [[04-robotics/sensor-models|3.2 센서 모델과 잡음]]이 고정한 마커 잡음 $0.5$ px에서는 모든 숫자가 절반이 된다.

영어 절반의 코드가 이 루프와 공분산, 그리고 P3P 가짜 자세의 확인을 돌린다. 출력은 네 코너의 픽셀, Gauss–Newton 스텝마다의 RMS($49.4$, $18$, $1.25$, $0.00733$ px, …), $R=I$ 와 $t=(0,0,2)$ m, 거리 $13.2$ mm·기울기 $2.70°$·roll $0.37°$, 그리고 가짜 자세 둘이 $A$, $B$, $C$ 의 픽셀은 그대로 두면서 $D$ 를 $(482.5,\ 360)$ 과 $(470,\ 376)$ 에 놓는다는 두 줄이다.

**RANSAC 안의 PnP.** §2.5에서 이미지와 3D 모델 — 지도의 랜드마크, 부품의 특징 — 사이에 만든 대응에는 이상점이 섞여 있다. 그래서 PnP는 RANSAC 안에서 돈다. 대응 셋을 뽑아 P3P를 풀고, 각 자세를 픽셀 문턱 안으로 재투영되는 대응의 수로 채점하고, 가장 좋은 자세를 그 인라이어 전부로 다듬는다. 최소 표본이 비용을 낮춘다. 대응의 절반이 인라이어이고 신뢰도가 $99\%$ 이면 [[02-foundations/algorithms/robotics-ai-problems|11.8 §3]]의 횟수는 셋짜리 표본 $35$ 번, 넷짜리 $72$ 번, 일반 $3\times4$ 카메라 행렬을 선형으로 풀 때 필요한 여섯짜리 $293$ 번이다(미지수 열한 개, 점 하나에 식 둘).

**평면 타깃: homography로 가는 길.** 모든 점이 한 평면 위에 있으면 타깃 프레임을 그 평면에 둔다. 그러면 $Z_t=0$ 이고 $R$ 의 세 번째 열이 빠진다.

$$\lambda\begin{pmatrix}u\\v\\1\end{pmatrix}=K\,[\,r_1\ \ r_2\ \ t\,]\begin{pmatrix}X_t\\Y_t\\1\end{pmatrix}=H\begin{pmatrix}X_t\\Y_t\\1\end{pmatrix}$$

그래서 평면은 $3\times3$ homography $H$ 로 이미지에 옮겨지고, 어느 셋도 한 직선 위에 있지 않은 점 넷이 $H$ 를 정한다(스케일을 빼면 미지수 여덟, 점마다 식 둘). 그다음 $[\,r_1\ r_2\ t\,]=\lambda K^{-1}H$ 이고, $r_1$ 이 단위 벡터이므로 $\lambda=1/\lVert K^{-1}h_1\rVert$, 그리고 $r_3=r_1\times r_2$ 다. 리그에서는 $H=\begin{pmatrix}300&0&320\\0&300&240\\0&0&1\end{pmatrix}$, $K^{-1}H=\operatorname{diag}(0.5,\ 0.5,\ 1)$ 이므로 $\lambda=2$, $r_1=(1,0,0)$, $r_2=(0,1,0)$, $t=(0,0,2)$ m다. 같은 자세가 닫힌 형태로 나온다. 코너에 잡음이 있으면 $r_1$ 과 $r_2$ 가 정확히 정규직교가 아니므로, 회전을 $SO(3)$ 에 사영해 다듬기의 출발점으로 쓴다.

**작고 먼 마커는 뒤집힌다.** 기울기 지렛대는 마커보다 빨리 줄어든다. 타깃 중심에 놓인 $0.1$ m 정사각형은 $30$ px에 걸치고, $10°$ 를 기울여도 모서리가 $0.26$ px 바뀐다. 그 재투영 오차에는 서로 다른 국소 최소점이 둘 있다(Schweighofer, Pinz, 2006). 수직축 둘레로 $20°$ 기운 마커는 시선에서 $14.0°$ 벗어난 쪽을 향하는데, 반대쪽으로 $13.5°$ 벗어나 참 자세에서 $27.5°$ 떨어진 두 번째 자세가 코너를 RMS $0.18$ px로 재투영한다. 1픽셀 잡음이 어느 쪽이든 고를 수 있으므로 답이 프레임마다 둘 사이를 오갈 수 있다. 처방은 기하다. 더 큰 타깃, 더 가까운 카메라, 멀리 떨어뜨린 여러 마커, 또는 한쪽을 배제하는 사전 정보다.

**피두셜 마커: AprilTag.** 피두셜은 대응 문제를 설계로 푼다. AprilTag(Olson, ICRA 2011; AprilTag 2, Wang과 Olson, IROS 2016)는 4~12비트만 담는 흑백 정사각형을 인쇄한다. 프로젝트 페이지는 그 작은 payload를 QR 코드보다 강건하고 더 먼 거리에서 되는 검출과 맞바꾼 것으로 설명한다. 출력은 카메라에 대한 태그의 정밀한 3D 위치, 방향, ID다. 그것이 네 코너에 대한 PnP이고, 인쇄된 한 변의 길이가 모델이므로 크기를 잘못 넣으면 거리가 같은 비율로 틀린다. 뒤집힘도 물려받는다. 위키의 건설 조립 계보에서 앵커 논문은 블록마다 태그를 둘씩 붙였다([[01-canonical-papers/notes/8-construction/vision-guided-assembly|Feng 외 2015]]).

**PnP가 쓰이는 곳.** Hand–eye 보정은 로봇 자세마다 $T_{c_it}$ 를 PnP로 잰다(§5). 그래서 $\pm2.70°$ 의 기울기 잡음이 $AX=XB$ 의 $B$ 에 들어가고, 그 풀이가 여러 자세를 평균하는 이유 하나가 이것이다. 알고 있는 부품을 잡는 일은 부품 모델의 점과 그 검출 사이의 PnP에 §3의 프레임 사슬을 이은 것이다. 공구를 S1의 외장 패널에 맞추는 일([[05-construction-robotics/site-engineering|2.5]])은 패널을 타깃으로 한 같은 문제다. 리그 크기의 타깃이 $2$ m에 있고 코너 잡음이 $1$ px일 때 카메라 하나가 S1의 $\pm5$ mm에 대해 약속하는 것은 시선을 가로질러 $\pm2.2$ mm, 시선을 따라 $\pm13$ mm다.

### 3. 포인트 클라우드와 프레임

깊이 이미지 + intrinsics를 역투영하면 **포인트 클라우드**가 된다:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. 모든 클라우드는 어떤 프레임(센서·베이스·맵)에
산다 — 다중 센서 파이프라인은 그 프레임들 사이의 **extrinsic 보정**에 성패가 달려 있다
([[04-robotics/robot-systems-deployment|런타임에서는 TF 트리]]). 그럴듯해 보여도 틀린
프레임의 클라우드는 학습으로 잘 고쳐지지 않는 계통 오차를 만든다.

**얼마나 촘촘한가, 그리고 격자를 남겨 둘 이유.** $640\times480$ 깊이 이미지 한 장은 유효한 깊이를 가진 픽셀마다 점 하나씩, 많아야 $307{,}200$개의 점을 준다. 카메라를 마주 보는 면에서 이웃 픽셀은 $Z/f$만큼 떨어져 찍힌다. 랜드마크의 $2$ m에서 $3.3$ mm, $8$ m에서 $13.3$ mm이므로, 같은 장면이 네 배 먼 곳에서는 네 배 성기게 표본화되고, ICP(§4)는 먼 면에서 더 적고 더 시끄러운 대응점을 얻는다. 이미지 격자를 유지한 클라우드를 **격자형**(organized) 클라우드라 한다. 점의 이웃을 공간 탐색이 아니라 픽셀 인덱스로 찾으므로, point-to-plane ICP에 필요한 법선을 싸게 추정할 수 있다.

**리그로 계산한 프레임.** $L=(0.5,\ 0.2,\ 2.0)$ m는 카메라 프레임 좌표다. 팔은 공구 프레임에서 계획하고, 이 리그에 대한 §5의 손–눈 변환 $X=\big(I,\ (0,0,-0.04)\big)$가 그것을 옮긴다: $p^{g}=R_Xp^{c}+t_X=(0.5,\ 0.2,\ 1.96)$ m. 한 고리 더 가면 베이스 프레임은 $p^{b}=T_{bg}\,X\,p^{c}$이고, $T_{bg}$는 P2의 관절 엔코더에서 온다. §5가 표적에 대해 쓰는 것과 같은 사슬이다. 여기서 두 종류의 프레임 오차가 나오고, 둘은 다르게 행동한다. $X$를 빼먹고 카메라 좌표를 공구 좌표로 쓰면 클라우드의 모든 점이 거리와 상관없이 공구 축을 따라 똑같이 $4$ cm 어긋난다. 학습 데이터를 아무리 모아도 평균으로 지워지지 않는 편향이고, "학습으로 잘 고쳐지지 않는다"는 말의 실제 뜻이 그것이다. 대신 $X$의 회전을 $1^\circ$ 틀리면 점은 회전축에서의 거리 1미터마다 $2\sin(0.5^\circ)=1.75$ cm씩 움직인다. 카메라 $y$축에서 $2.06$ m 떨어진 $L$은 $3.6$ cm, $0.5$ m 떨어진 점은 $1$ cm 미만이다. 병진 오차는 일정하고, 회전 오차는 거리와 함께 자란다.

**프레임은 시각이기도 하다.** 팔이 움직이는 동안 찍은 클라우드는 찍힌 순간의 카메라 자세에 속한다. 그것을 다른 순간의 팔 자세와 짝지으면 클라우드 전체가 그 사이 카메라가 움직인 거리만큼 틀린 프레임에 놓인다. $0.10$ m/s로 움직이는 카메라와 $30$ ms의 어긋남이면 $3$ mm다. 어느 타임스탬프에 어느 변환을 조회하는지는 [[04-robotics/robot-systems-deployment|10. 로봇 시스템 §4]]의 TF 트리이고, $X$를 정하는 보정은 §5다. 포인트 클라우드 논문이 밀리미터를 인용하면 어느 프레임에서인지, 그리고 클라우드를 거기 놓은 extrinsic과 타임스탬프가 추정한 것인지 가정한 것인지 물어라. 움직이는 베이스에서 틀린 스탬프의 1밀리초는 모두 거리 $v\,\Delta t$이고, [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §9]]가 리그의 센서마다 그 값을 매긴다.

### 4. Registration과 ICP

**Registration**은 두 기하를 정렬한다. 스캔끼리, 점군과 부품 모델, 현장 스캔과 BIM이 대상이다. 미지수는 강체 변환 $T\in SE(3)$다. 최적화하기 전에 어떤 점끼리 같은 표면을 나타내는지부터 물어야 한다.

**ICP**(iterative closest point)는 현재 변환으로 대응점을 고른 뒤, 그 대응을 고정하고 변환을 갱신한다. 일반적인 강체 **점대점** 최소제곱의 고정 대응 갱신은 SVD로 닫힌 형태의 해를 구한다. **점대평면** 방식은 흔히 선형화한 최소제곱을 쓴다. 따라서 모든 ICP 갱신에 Gauss–Newton이나 Levenberg–Marquardt가 필수인 것은 아니다([[02-foundations/optimization|4. 최적화 §3.5]]).

비슷한 패널이 반복되는 벽 모델에 스캔을 맞춘다고 하자. 초기 변환이 틀리면 옆 패널의 점과 짝지을 수 있다. 그 대응에 대해 최소제곱을 정확히 풀어도 잘못된 정렬을 강화할 수 있다. **ICP가 국소적인 이유**는 대응 선택과 자세가 서로 의존하며, 번갈아 개선한다고 모든 대응을 탐색하지는 않기 때문이다. odometry나 전역 매칭으로 초기값을 얻고 겹치는 영역과 이상점을 확인한다. [MIT 기하 자세 추정 유도](https://manipulation.mit.edu/pose.html)를 함께 보라.

**ICP 목적함수의 완전한 정의.** ICP는 미지수 둘 위에서 비용 하나를 **번갈아 최소화**한다. $R \in SO(3)$ 인 강체 변환 $T = (R, t)$, 그리고 각 원본 점을 대상 점으로 보내는 대응 사상 $c$ 다. 원본 점 $\{p_i\}$ 와 대상 점 $\{q_j\}$ 에 대해 두 반쪽 스텝은

$$c(i) \leftarrow \arg\min_j \lVert Rp_i + t - q_j \rVert \quad\text{(대응)}, \qquad (R,t) \leftarrow \arg\min_{R,t} \sum_i \lVert Rp_i + t - q_{c(i)} \rVert^2 \quad\text{(풀이)}$$

각 반쪽 스텝이 비용을 낮추기만 하므로 루프는 수렴한다 — 다만 **국소** 최소점으로 수렴한다. 대응 스텝이 이산 선택이고 풀이 스텝이 그것을 다시 들여다보지 않기 때문이다. 그것이 "ICP는 국소적이다"의 정확한 내용이다. 풀이 스텝은 닫힌 형태다: 두 집합을 중심화하고 교차 공분산 $H = \sum_i (p_i - \bar p)(q_{c(i)} - \bar q)^\top$ 의 SVD를 취해 $R = V\operatorname{diag}(1,1,\det(VU^\top))U^\top$, $t = \bar q - R\bar p$ 로 둔다. $\det$ 항은 반사가 아니라 회전이 되도록 강제한다.

**점대평면 방식의 완전한 정의.** 대상이 표본으로 찍힌 *표면*일 때, 가장 가까운 대상 점은 참된 대응점인 경우가 거의 없다 — 그냥 가장 가까운 표본일 뿐이다. 그래서 점대평면은 잔차를 대상의 표면 법선 $n_{c(i)}$ **방향으로만** 재고, 원본 점은 접평면 안에서 비용 없이 미끄러질 수 있다.

$$\min_{R,t} \sum_i \big((Rp_i + t - q_{c(i)})^\top n_{c(i)}\big)^2$$

매끄러운 표면에서 훨씬 적은 반복으로 수렴한다. 미끄러짐이야말로 점대점 비용이 잘못 벌주는 운동이기 때문이다. 대가는 그 자유가 진짜라는 것이다. 법선들이 공간을 펼치지 못하면 비용에 평평한 방향이 남는다.

> [!example] 계산 예제 · Worked example — 퇴화를 숫자로
> **벽 하나.** 대상 평면은 $y = 0$, 법선 $n = (0,1)$; 스캔 점 셋은 $(0,\ 0.05)$, $(1,\ 0.05)$, $(2,\ 0.05)$ 라 스캔이 모델에서 $5$ cm 떠 있다. 순수 평행 이동 $t = (t_x, t_y)$ 에 대해 모든 점의 점대평면 잔차는 $(t_y + 0.05)$ 이고 비용은 $3(t_y + 0.05)^2$ 이다. $t = (0, -0.05)$ 에서도, $t = (-0.30, -0.05)$ 에서도, $t = (+0.75, -0.05)$ 에서도 똑같이 **0**이다 — $t_x$ 는 비용에 아예 나타나지 않는다. 벽을 따라 $30$ cm 틀려도 잔차가 정확히 0이라는 것, 그것이 "잔차가 작다고 pose가 맞는 것은 아니다"를 산수로 쓴 것이다.
>
> **모서리가 그것을 고친다.** 법선 $(1,0)$ 의 두 번째 면 $x = 0$ 과 그 위의 스캔 점 $(0.05,\ 0)$, $(0.05,\ 1)$ 을 더한다. 이제 $t = (0, -0.05)$ 의 비용은 $2(0.05)^2 = 0.005$, $t = (-0.05, -0.05)$ 에서 $0$, $t = (-0.30, -0.05)$ 에서 $2(0.05-0.30)^2 = 0.125$ 다. 평행하지 않은 법선 둘이면 평면 위 평행 이동을 고정하기에 충분하므로, **퇴화는 벽의 성질이 아니라 스캔이 담은 법선들의 성질**이다.
>
> **같은 벽에 올바른 대응점으로 점대점을** 풀면 변환 전체가 복원된다: $q_i = p_i + (0.30, 0.05)$ 이면 SVD 풀이가 정확히 $R = I$, $t = (0.30, 0.05)$ 를 돌려준다. 함정은 ICP가 올바른 대응점을 *갖고 있지 않다*는 것이다. 특징 없는 평면에서 최근접 점 매칭은 수선의 발을 돌려주고, 그것은 $t_x$ 와 함께 미끄러지므로 같은 퇴화를 그대로 재현한다.

퇴화는 기하와 목적함수에 달렸다. 특징 없는 평면의 점대평면 잔차로는 평면을 따르는 병진과 법선 둘레 회전을 제약할 수 없다. 뚜렷한 경계나 점 대응은 추가 정보를 줄 수 있다. “벽은 퇴화한다”는 말은 측정 모델의 정보 부족을 줄여 부르는 것이지, 모든 벽 스캔의 보편적 성질은 아니다.

> [!question] 대응점 확인 · Check the correspondence
> ICP 잔차가 작으면 자세도 맞는가? **답:** 아니다. 반복 패널은 틀린 위치에서도 잘 맞는다. 최종 잔차뿐 아니라 초기값, 독립 랜드마크, 제약되지 않는 방향을 확인한다.

### 5. 보정

| 보정 | 추정 대상 | 전형적 방법 |
|---|---|---|
| Intrinsic | $f_x,f_y,c_x,c_y$, 왜곡 | 체커보드/타깃 촬영 |
| 카메라–카메라 (스테레오) | 상대 $SE(3)$ + 정렬(rectification) | 공유 타깃 촬영 |
| 카메라–LiDAR | extrinsic $SE(3)$ | 타깃 또는 상호 특징 정렬 |
| Hand–eye (카메라–로봇) | 센서–말단 또는 베이스 변환 | 로봇 운동 + 타깃 ($AX=XB$) |
| 시간 | 센서 간 클럭 오프셋/지연 | 운동 신호의 상관 |

카메라–LiDAR 행을 마스트에 LiDAR를 단 이 리그 위에서 계산한 것 — 외부 파라미터, $1^\circ$ 오차가 픽셀과 밀리미터로 하는 일, 그리고 회전·평행이동·시간을 가르는 검사 — 이 [[04-robotics/perception-sensors-rigs|3.6 인식 센서 §8]]이다. 모든 행은 보정과 사용 사이에 마운트가 움직이지 않는다고 가정한다. 휘거나 떠는 브래킷은 그 가정을 깨고, 그것을 목표에서의 기울기로 설계하는 법은 [[02-foundations/tools/mechanical-design-fabrication|12.9 실험을 위한 기계 설계와 제작 §6]]이다.

**Hand–eye 방정식의 유도.** 손목에 단 카메라가, 팔이 움직이는 동안 제자리에 있는 보정 타깃을 본다. 프레임 $b$ 의 좌표를 프레임 $a$ 로 옮기는 변환을 $T_{ab}$ 로 쓴다. $p^a = T_{ab}p^b$ 이고, §1의 $T_{cw}$ 와 같은 방향이다([[02-foundations/se3-geometry|8. 3D 기하와 SE(3) §3]]). $b$ 는 로봇 베이스, $g$ 는 그리퍼, $c$ 는 카메라, $t$ 는 타깃이다. 로봇 자세 $i$ 에서는 변환 세 개의 사슬 하나가 베이스에서 타깃까지 닿는다. 관절 엔코더가 주는 그리퍼 자세 $T_{bg_i}$, 변하지 않는 모르는 카메라–그리퍼 장착 $X = T_{gc}$, 그리고 카메라가 재는 타깃 자세 $T_{c_it}$(PnP, 곧 타깃의 알려진 코너와 그 픽셀로 구한다)다. 타깃은 움직이지 않았으므로 두 로봇 자세 $1$ 과 $2$ 의 사슬은 같은 변환에서 끝난다.
$$T_{bg_1}\,X\,T_{c_1t} = T_{bt} = T_{bg_2}\,X\,T_{c_2t}$$
왼쪽에 $T_{bg_2}^{-1}$, 오른쪽에 $T_{c_1t}^{-1}$ 를 곱하면 모르는 타깃 자세가 빠진다.
$$AX = XB, \qquad A = T_{bg_2}^{-1}T_{bg_1}, \qquad B = T_{c_2t}\,T_{c_1t}^{-1}$$
$A$ 는 두 자세 사이의 그리퍼 운동으로 엔코더로 알고, $B$ 는 같은 두 자세 사이의 카메라 운동으로 타깃에서 잰다. 양변은 하나의 변환, 곧 자세 2의 그리퍼에서 본 자세 1의 카메라이고, 두 경로로 닿은 것이다. 그리퍼를 움직인 다음 카메라로 건너가거나, 카메라로 건너간 다음 그것을 움직이거나. $AX = XB$ 를 회전 블록과 평행 이동 블록으로 나누면 운동 하나가 무엇을 알려 주고 무엇을 못 알려 주는지 보인다.
$$R_AR_X = R_XR_B, \qquad (R_A - I)\,t_X = R_Xt_B - t_A$$
장착의 평행 이동 $t_X$, 곧 $d_{ct}$ 를 담은 블록은 $R_A - I$ 를 거쳐서만 들어온다. 회전 없는 운동은 그것을 통째로 빼고, 한 축에 대한 회전은 그 축 방향 성분을 뺀다. $R_A - I$ 가 회전축을 0으로 보내기 때문이다. 그래서 $X$ 를 정하려면 회전축이 서로 다른 운동이 여럿 필요하다.

*예, 리그 위에서.* 변환을 (회전, 평행 이동)으로 쓴다. 그리퍼 프레임을 P2의 도구 끝에 두고 축을 카메라 축과 평행하게 잡으면 $X = \big(I,\ (0, 0, -0.04)\big)$ 다. 카메라가 도구 축 위에서 끝보다 $d_{ct}$ 뒤에 있다. 타깃 프레임을 타깃 코너 $(0, 0, 2)$ 에 두면 $T_{c_1t} = \big(I,\ (0, 0, 2)\big)$ 다. P2가 도구 끝을 축으로 그리퍼를 카메라의 $y$ 축 둘레로 돌린다. P2가 평면 팔이므로 이것이 관절축 방향이다. 각은 $\cos\theta = 0.96$, $\sin\theta = 0.28$ ($16.26°$)이다. 엔코더는 $A = \big(R_y(-\theta),\ 0\big)$ 를 준다. $R_y$ 는 $y$ 축 둘레 회전이고, $A$ 가 옛 그리퍼 프레임을 새 그리퍼 프레임에서 다시 쓰는 것이라 부호가 음이다. 회전 중심보다 $4$ cm 뒤에 있는 카메라는 휘둘린다. 이제 타깃은 $T_{c_2t} = \big(R_y(-\theta),\ (-0.5488, 0, 1.9216)\big)$ 로 재지므로 타깃 코너 셋은 $(148.6, 240)$, $(300.0, 240)$, $(148.6, 364.9)$ px에 보이고, 모두 여전히 이미지 안이다. 그러면 카메라 운동은 $B = \big(R_y(-\theta),\ (0.0112, 0, 0.0016)\big)$ 이고, 두 경로가 일치한다.
$$AX = XB = \big(R_y(-\theta),\ (0.0112,\ 0,\ -0.0384)\big)$$
왼쪽에서는 $R_y(-\theta)(0, 0, -0.04) = (0.0112, 0, -0.0384)$ 이고, 오른쪽의 $(0, 0, -0.04) + (0.0112, 0, 0.0016)$ 도 같은 벡터이기 때문이다. *반례:* 카메라가 도구 끝에 있다고, 곧 $X = I$ 라고 가정하자. 그러면 $AX$ 에는 평행 이동이 없는데 $XB$ 는 $(0.0112, 0, 0.0016)$ 을 그대로 가져 $11.3$ mm가 어긋난다. 카메라가 쓸고 간 현의 길이 $2d_{ct}\sin(\theta/2)$ 다. 회전 한 번이 $4$ cm를 드러내는 방식이 이것이다. 같은 크기의 오프셋이 관절축 방향 $(0, 0.04, 0)$ 에 있었다면 $X = I$ 도 $AX = XB$ 를 만족했을 것이다. 모든 회전이 그 한 축에 대한 것인 P2 같은 평면 팔은 장착의 그 축 방향 성분을 보정할 수 없다.

품질 지표는 대개 **reprojection error**다: 추정된 3D 점을 추정된 모델로 투영해 검출
위치와의 픽셀 거리를 잰다. 보정 세트에서 낮은 reprojection error가 보정된 부피·거리·
온도 밖에서의 정확도를 보장하지는 **않는다**. 모델은 타깃을 실제로 관측한 위치·거리·조건에서만 맞춰졌으므로, 그 밖에서는 물리 법칙을 따르는 것이 아니라 외삽하고 있을 뿐이다.

**Reprojection error의 완전한 정의.** 한 시점 $i$ 에서 보인 3D 점 $X_j$ 하나에 대해, 이것은 이미지 점 둘 사이의 **픽셀 단위 거리**다: 검출된 특징 $\tilde u_{ij}$ 와 현재 모델로 투영한 $X_j$. §1의 전체 파이프라인 — extrinsics, 원근 나눗셈, 왜곡, 그리고 $K$ — 을 $\pi(\cdot)$ 로 쓰면

$$e_{ij} = \big\lVert\, \tilde u_{ij} - \pi\big(K, d, T_i, X_j\big) \,\big\rVert_2$$

이것을 *그* 지표로 만드는 조건이 셋이다. 잡음이 실제로 있는 곳인 **이미지에서** 재므로, 이것에 대한 최소자승이 등방 가우시안 픽셀 잡음 아래의 최대우도 추정이다(가우시안 우도가 왜 제곱 오차가 되는지는 [[02-foundations/probability|3. 확률 §4]], 푸는 법은 [[02-foundations/optimization|4. 최적화 §3]]) — 3D에서 미터로 잰 오차는 카메라가 관측한 적 없는 양에 가중치를 주는 것이다. **관측마다** 하나이므로 모든 $(i,j)$ 짝이 기여한다. 그리고 **모든** 파라미터에 동시에 의존한다: $K$, 왜곡 계수 하나, pose, 점 중 무엇을 움직여도 $e_{ij}$ 가 움직인다. 보정과 bundle adjustment가 어떤 변수를 고정하느냐만 다른 같은 최적화인 이유가 그것이다.

**보정 잔차의 완전한 정의.** 보정 도구가 찍어 주는 값은 모든 시점의 모든 코너에 걸친 **RMS reprojection error**, 곧 시점 $N$ 개와 타깃 코너 $M$ 개에 대한 위 값 $NM$ 개를 요약한 숫자 하나다.

$$e_{\text{RMS}} = \sqrt{\frac{1}{NM}\sum_{i=1}^{N}\sum_{j=1}^{M} \big\lVert \tilde u_{ij} - \pi(K, d, T_i, X_j)\big\rVert_2^2}$$

*예:* $\hat f = 598$ 인 리그의 코너 셋은 잔차 $0.00$, $0.50$, $0.40$ px를 주므로 $e_{\text{RMS}} = \sqrt{0.41/3} = 0.370$ px이고, 그 보정은 축에서 $0.5$ m 벗어난 점을 여전히 $1.67$ mm, $3$ m 벗어난 점을 $10.0$ mm 틀리게 놓는다. *반례, 그리고 기억할 쪽:* $e_{\text{RMS}}$ 는 **훈련** 잔차다. 한 거리에서 찍은 타깃 스무 장에 맞춘 모델에 $k_3$, $p_1$, $p_2$ 를 더하면 이 값은 내려가면서 외삽은 나빠진다. 과대 매개변수화된 회귀와 정확히 같다([[02-foundations/ml-practice|9. ML 실무 §2]]). 정직한 확인은 셋이다: 적합이 본 적 없는 시점으로 만든 홀드아웃 세트, *이미지 위치별로* 그린 잔차(초점 거리 오차는 위 표처럼 주점에서 아무것도 남기지 않고 반경 방향으로 자란다), 그리고 실제 작업 거리에서 잰 알려진 길이.

### 6. 기하학적 인식 + 딥 인식

현대 파이프라인은 둘을 섞는다: 네트워크가 검출·분할
([[01-canonical-papers/notes/2-computer-vision/sam|SAM]])하거나, 특징을 매칭하거나,
깊이/pose를 예측하고; 기하가 그것을 미터법 구조로 바꾸고 일관성을 강제한다
(삼각측량, [[01-canonical-papers/notes/2-computer-vision/vggt|VGGT]]식 feed-forward 기하,
[[01-canonical-papers/notes/2-computer-vision/nerf|NeRF]]/[[01-canonical-papers/notes/2-computer-vision/3d-gaussian-splatting|3DGS]] 렌더링 손실).
읽을 때 물어라: *어느 단계가 학습이고 어느 단계가 기하이며, 미터 스케일은 어디서
들어오는가?* (보정된 스테레오/LiDAR, 알려진 물체 크기, 또는 아예 없음).

**리그에서 스케일이 들어오는 곳.** 세 곳이 있고, 셋 모두 기선 $B$만 다른 같은 $Z^2$ 법칙을 따른다. 측정 오차 $\delta$는 깊이를 약 $Z^2\delta/B$만큼 옮기며, 스테레오는 $B=fb=72$ px·m, $0.5$ m 알려진 길이는 $B=f\ell=300$ px·m, 기준점 맞추기는 $B=s$다.

*보정된 스테레오*는 §2의 것이다. $fb=72$ px·m이므로 $2$ m에서 시차 1픽셀이 $5.6$ cm다.

*알려진 길이*는 물체를 기선으로 삼아 같은 방식으로 작동한다. 표적 모서리 $A$와 $B$는 $0.5$ m 떨어져 있고 영상에서 $150$ px 떨어져 있으므로 알려진 길이 $\ell=0.5$ m로 $Z=f\ell/\Delta u=600\times0.5/150=2.0$ m이며, 그 간격을 1픽셀 틀리면 깊이가 $Z^2/(f\ell)=4/300=1.3$ cm 움직인다. 표적이 $b=0.12$ m보다 긴 기선이므로 스테레오 쌍보다 네 배 좋다.

*기준점에 맞추기*는 학습된 상대 깊이가 미터가 되는 방법이다. 스케일과 오프셋을 모른 채 역깊이를 예측하는 네트워크는 $s$와 $t$를 모르는 $r=s/Z+t$를 내놓으므로, 서로 다른 거리에 깊이를 아는 픽셀이 적어도 둘 필요하다. 네트워크가 $L$(스테레오: $Z=2.0$ m)에서 $r=0.80$, §2의 $8$ m 점에서 $r=0.35$를 낸다고 하자. 그러면 $s=1.2$, $t=0.2$이고, $r=0.50$인 세 번째 픽셀은 $Z=4.0$ m에 있다. 출력 오차 $\pm0.01$은 그 픽셀을 $3.87$에서 $4.14$ m 사이로, $8$ m에 있는 픽셀을 $7.50$에서 $8.57$ m 사이로 옮긴다. 역깊이는 유계로 남지만, 그 오차는 스테레오와 똑같이 거리와 함께 자란다. 같은 깊이에 있는 기준점 둘은 아무것도 정하지 못한다. 미지수 둘에 식 하나이기 때문이다.

**복원에도 같은 질문을.** 움직이는 카메라 하나는 장면을 닮음 변환까지만 복원한다. 숫자 일곱 개이고 그중 하나가 스케일이다. 그래서 단안 structure-from-motion의 자세로 맞춘 NeRF나 3DGS 모델은 알려진 길이 하나가 정해 주기 전까지 임의 단위에 있다. 그 길이는 $0.5$ m 표적 모서리일 수도 있고, 팔 자신의 움직임일 수도 있다. P2의 엔코더가 §5의 손–눈 $X$를 거쳐 카메라가 얼마나 움직였는지 말해 주므로, 정지한 장면을 옆으로 $0.12$ m 옮기기 전과 후에 찍은 영상 두 장은 시간 속의 §2 스테레오 쌍이다. 정본 노트도 학습된 깊이에 대해 같은 말을 한다. [[01-canonical-papers/notes/2-computer-vision/depth-anything|Depth Anything]]의 강건한 상대 깊이도 새 현장에서는 미터 헤드와 스케일 보정이 여전히 필요하다.

### 7. 주장과 평가 읽기

| 논문 표현 | 받아들이기 전에 확인할 것 |
|---|---|
| "accurate 6-DoF pose" | 오차 지표(ADD? 회전/병진 분리?), 대칭 처리, 가림 수준 |
| "metric depth" | 스케일의 출처; 평가 거리 범위; 실내-실외 이동 |
| "robust registration" | 초기화 프로토콜, 퇴화 장면 비율, outlier 비율 |
| "calibration-free" | 실제로 가정하는 것 (대개: intrinsics는 여전히 앎) |
| "real-time reconstruction" | 하드웨어, 해상도, 긴 시퀀스에서의 drift |

> [!warning] 핵심 주장 읽는 법 · Reading the claim
> 서브픽셀 reprojection error와 아름다운 복원이 그 자체로 *로봇 베이스 프레임에서
> pose가 맞다*는 뜻은 아니다 — 그러려면 올바른 extrinsics와 시간 동기화도 필요한데,
> 많은 논문이 이를 고정된 범위 밖 가정으로 둔다.

### 7.5 오차를 보고 고치는 명령으로: visual servoing

이미지나 pose 오차가 속도 명령이 되어야 인식이 로봇 루프를 닫는다. **PBVS**는 두 자세를
추정해 $\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$ 같은 pose error를 만들고
($\operatorname{Log}$는 [[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §5]]의 자세 로그, $^\vee$는 그 결과를 숫자 여섯으로 쌓는 것),
$\xi$를 줄이는 twist([[04-robotics/modern-robotics/ch03-rigid-body-motions|MR 3장 §3]])를 명령한다. 정확도는 보정과 pose 추정 오차를 물려받는다. **IBVS**는
이미지에 남는다. 특징 $s$에 대해 $\dot s=L_s v_c$이고 image Jacobian $L_s$는 특징 깊이에
의존한다. $v_c=-\lambda L_s^+(s-s^*)$ 같은 국소 법칙이 픽셀 오차를 줄인다. IBVS는 완전한
pose 복원에 덜 민감할 수 있지만 여전히 깊이 추정과 조건이 좋은 특징 기하가 필요하다. 어느 식도
시야 유지, 구동기 한계, 전역 수렴, 충돌 회피를 혼자 보장하지 않는다. "closed-loop perception"
주장은 오차·야코비안·제어 주기·깊이 출처와 국소 수렴 영역 밖의 회복을 확인해 읽는다.

**리그로 계산: 점 하나에 대한 IBVS.** 랜드마크의 픽셀 $(470,300)$을 현재 특징으로, 주점을 목표로 두면 정규화 좌표에서 오차는 $e=(0.25,\ 0.10)$이다. 영상면에 평행하게 병진만 하는 카메라라면 $L_s$의 관련된 두 열은 대각선에 $-1/Z$를 가지므로, 법칙 $v_c=-\lambda L_s^+e$는 $v_c=\lambda\hat Z e$가 된다. $\lambda=0.5\ \mathrm{s^{-1}}$, $\hat Z=2.0$ m이면 $(0.25,\ 0.10)$ m/s를 명령하고, 오차는 $e^{-\lambda t}$로 줄어 $6$ s 뒤에는 $5\%$가 남는다. 깊이 추정이 $2.0$ m가 아니라 $1.0$ m이면 수렴은 깨지지 않고 속도만 $0.25\ \mathrm{s^{-1}}$로 반이 된다. 여섯 열 전체에서 깊이는 병진 열에만 나타나므로, 틀린 $\hat Z$는 병진과 회전 사이의 몫도 바꾸고 경로가 휜다.

**IBVS가 보정에 강건하다고 불리는 이유.** 목표 영상 $s^*$를 카메라가 목표에 있을 때 기록했다면, IBVS는 그 영상으로 수렴하고, 특징이 자세를 못 박아 줄 때 그 자세로도 수렴한다. 일반 위치의 점 넷 이상이면 그렇고, 점 셋은 자세를 최대 네 개까지 허용하며, 위 예제의 점 하나는 자유도 여섯 중 넷을 풀어 둔다. 초점 거리와 손–눈 오차는 루프가 수렴하는 한 경로와 속도를 바꿀 뿐 끝점은 바꾸지 않는다. PBVS는 보정된 모델을 거쳐 오차를 계산하므로 그 오차가 수렴 뒤에도 남는다. 대상으로 한 번 끝까지의 $\hat f=598$ px로, $0.5$ m 표적 모서리를 $2.0$ m에 두라는 PBVS 루프는 그 깊이를 $\hat f\cdot0.5/\Delta u$로 읽어 $\Delta u=149.5$ px에서 멈추고, 그때 실제로는 $2.0067$ m에 있다. 수렴한 뒤에도 $6.7$ mm 멀다. $4$ cm 오프셋 대신 $X=I$를 가정하면 PBVS의 공구 목표가 공구 축을 따라 $4$ cm 어긋난다.

**게인은 대역폭이므로 지연이 그것을 묶는다.** 폐루프 $\dot e=-\lambda e$는 개루프 $L(s)=\lambda/s$에서 나오는데, 이것은 $\lambda$에서 교차하고 위상 여유가 $90^\circ$인 적분기이며, 지연 $\tau$가 그 여유에서 $\lambda\tau$ 라디안을 쓴다. **P6**([[02-foundations/lab-plants|0.6]])의 카메라–힘 예산 $70$ ms라면 $\lambda=0.5\ \mathrm{s^{-1}}$에서 $2^\circ$, $\lambda=10\ \mathrm{s^{-1}}$에서 $40^\circ$를 써 $50^\circ$가 남고, $\lambda=\pi/(2\tau)=22.4\ \mathrm{s^{-1}}$ 근처에서 루프가 불안정해진다. 일반형은 [[04-robotics/control-theory-ce397|5. 제어 이론 §5.5]]의 지연 예산이다.

### 읽고 나면 말할 수 있어야 하는 것

- 핀홀 모델로 3D 점을 손으로 투영할 수 있다
- intrinsics와 extrinsics를 구분하고 각각 언제 바뀌는지 말할 수 있다
- 단안 비전이 스케일을 잃는 이유와 스케일이 다시 들어오는 지점을 설명할 수 있다
- ICP의 루프와 초기화가 필요한 이유를 설명할 수 있다
- 카메라+LiDAR+로봇팔 시스템에 필요한 보정들을 나열할 수 있다
- reprojection error를 과신하지 않고 해석할 수 있다
- PBVS와 IBVS를 구분하고 pose·보정·깊이·image Jacobian이 루프 어디에 들어가는지 말할 수 있다
- 에지가 아니라 코너를 매칭하는 이유를 설명하고, 비율 검사·상호 검사·RANSAC으로 매칭을 거를 수 있다
- $K$ 의 다섯 성분을 모두 이름 붙이고, 어느 것이 센서의 성질이고 어느 것이 렌즈의 성질인지 말하고, 왜곡을 올바른 순서로 적용할 수 있다
- Epipolar 제약을 $E$ 로도 $F$ 로도 쓰고, 대수적 잔차를 픽셀 거리로 바꾸고, 그 제약이 잡지 못하는 것을 말할 수 있다
- Rectify된 짝을 삼각측량하고, $Z^2$ 오차 법칙 때문에 답이 쓸모없어지는 거리를 말할 수 있다
- 알려진 코너 넷에서 PnP로 자세를 구하고, 코너 셋이 왜 자세를 최대 넷까지 남기는지와 무엇이 하나를 고르는지 말하고, 작은 마커에서 왜 기울기가 가장 약한 숫자인지 설명할 수 있다
- 점대점과 점대평면 ICP 목적함수를 쓰고, 후자에 평평한 방향이 생기는 경우를 보일 수 있다
- RMS reprojection error를 정확도가 아니라 훈련 잔차로 읽을 수 있다

> [!tip] 더 깊이 · Going deeper
> Szeliski의 [*Computer Vision: Algorithms and Applications*](https://szeliski.org/Book/)이 무료이고 이 페이지의 범위를 전부 덮는다. 다시점 기하를 정리로 봐야 할 때 — essential·fundamental 행렬, 삼각측량, 번들 조정 — 는 Hartley·Zisserman의 *Multiple View Geometry in Computer Vision*이 이 분야가 인용하는 참고서다.

### 스스로 점검

1. 위의 intrinsics로 $p^{c}=(-0.3, 0.1, 1.5)$는 어디에 투영되는가?
2. $f=600$, $b=0.12$의 스테레오에서 $Z=24$ m에 해당하는 시차는? 그것이 왜 문제인가?
3. 데이터가 완벽해도 길고 빈 복도에서 ICP가 실패할 수 있는 이유는?
4. "보정 없이" LiDAR와 카메라를 융합한다는 논문이 여전히 가정하고 있을 가능성이 큰 것은?
5. 어떤 창에서 $\sum I_x^2=40$, $\sum I_y^2=2$, $\sum I_xI_y=0$이다. $k=0.05$일 때 Harris 응답과 Shi–Tomasi 점수는 얼마이고, 어떤 종류의 점인가?
6. 똑같은 패널이 반복되는 벽에서 ORB 기술자의 가장 가까운 후보가 32비트, 두 번째가 36비트 떨어져 있다. 0.8 비율 검사를 통과하는가? 거르기를 통과한 틀린 매칭은 무엇이 잡아야 하는가?
7. 어떤 보정 파일이 리그의 $640\times480$ 센서에 대해 $f_x = 600$, $f_y = 604$, $c_x = 318$, $c_y = 241$, $s = 0$ 을 보고한다. 이 중 렌즈가 아니라 *센서*에 대해 말해 주는 것은 무엇이고, 이미지가 잘렸다고 의심하게 만들 값은 어느 하나인가?
8. 리그의 $F$ 로, $\tilde u_1 = (470, 300)$ 의 후보 짝이 $(434, 306)$ 에 있다. 대수적 잔차와 픽셀 단위 점-선 거리를 계산하라. $(452, 300)$ 의 짝은 같은 검사에서 기각되는가?
9. 같은 시점 스무 장에 $k_3$, $p_1$, $p_2$ 를 더해 보정을 다시 맞추니 $e_{\text{RMS}}$ 가 $0.37$ px에서 $0.21$ px로 내려갔다. 무엇이 입증되었으며, 새 모델이 더 나은지를 가리려면 어떤 확인 둘이 필요한가?
10. 네 코너에 PnP를 풀어 $R=I$, $t=(0,0,2)$ m를 얻었다. 타깃 프레임에서 카메라는 어디 있는가? 코너마다 $1$ px의 잡음이 있을 때 적합은 타깃의 거리와 기울기 중 무엇을 더 나쁘게 복원하며, 왜 그런가? 타깃이 같은 자리의 $0.1$ m 태그라면 무엇이 바뀌는가?

> [!tip]- 정답 · Answers
> 1. $u = 600(-0.3)/1.5+320 = 200$, $v = 600(0.1)/1.5+240 = 280$.
> 2. $d = fb/Z = 600\cdot0.12/24 = 3$ px — ±1 px 오차가 18–36 m를 오간다; 원거리 스테레오 깊이는 취약하다.
> 3. 복도 축 방향의 병진은 점-최근접점 거리를 거의 바꾸지 않는다 — 퇴화된(관측 불가능한) 방향.
> 4. 알려진 intrinsics, 그리고 대개 대략적인 extrinsic 초기화 또는 겹침과 동기화된 타임스탬프를 여전히 요구하는 공동 최적화.
> 5. 고윳값이 40과 2이므로 $R=80-0.05\cdot42^2=-8.2<0$이고 $\min\lambda=2$다. 에지다. 밝기가 $x$ 방향으로만 바뀌므로 에지 방향인 $y$로는 위치가 잘 정해지지 않는다.
> 6. 통과하지 못한다. $32/36=0.89>0.8$이므로 버린다 — 거의 같은 후보는 옆 패널일 가능성을 뜻한다. 거르기를 통과한 틀린 매칭은 기하 검증(RANSAC)이 잡아야 하는데, 패널 한 칸만큼 통째로 밀린 집합은 그것마저 통과할 수 있으니 odometry나 독립 랜드마크와 대조하라.
> 7. $f_x \ne f_y$ 와 $s$ 가 센서의 사실이다. 픽셀 단위 초점 거리가 다르다는 것은 픽셀이 정사각이 아니라는 뜻이고, $s=0$ 은 픽셀 축이 직교한다는 뜻이다. 초점 거리 자체는 렌즈다. $c_x = 318$ 은 특별할 것이 없고, 높이 480에 대한 $c_y = 241$ 은 주점이 중심보다 $1$ px *아래*, $c_x$ 는 $320$ 보다 $2$ px 왼쪽에 있다는 뜻으로 둘 다 정상이다. 자르기를 알리는 값은 $(w/2, h/2)$ 에서 크게 벗어난 주점이다. 예를 들어 폭 $640$ 이미지에서 $c_x = 240$ 이라면, 보정한 배열과 지금 투영해 넣는 배열이 다르다는 말이다.
> 8. $\ell = F\tilde u_1 \propto (0,\ 0.0002,\ -0.06)$ 이다. 대수적 잔차는 $0.0002(306) - 0.06 = 1.2\times10^{-3}$, $\sqrt{\ell_1^2+\ell_2^2} = 0.0002$ 이므로 $d_\perp = 6.0$ px — 수평 epipolar 선이니 당연히 수직 어긋남 그대로다. $(452, 300)$ 의 짝은 대수적 잔차가 정확히 $0$ 이고 $d_\perp = 0$ 이다. 선 *위에* 있으므로 epipolar 검사를 통과한다. 그래도 틀렸다. $Z = 600(0.12)/18 = 4.0$ m로 삼각측량되어 $2.0$ m가 아니다. Epipolar 선을 따라 움직이는 것은 $F$ 에 보이지 않고 깊이에만 보인다.
> 9. 자유 파라미터가 많은 모델이 같은 데이터에 더 잘 맞았다는 것뿐이고, 그것은 보장된 일이므로 정확도에 대해서는 아무것도 입증하지 않는다([[02-foundations/ml-practice|9. ML 실무 §2]]). 가리는 확인이 둘이다: (i) 적합이 본 적 없는 시점 — 되도록 다른 거리와 기울기 — 을 홀드아웃으로 두고 훈련 시점이 아니라 거기서 $e_{\text{RMS}}$ 를 비교한다; (ii) 실제 작업 거리에서 알려진 길이나 타깃 간 거리를 잰다. 그것이 보정이 봉사할 미터이기 때문이다. 셋째로 이미지 위치별 잔차 지도가 유용하다. 진짜 왜곡 구조는 반경 방향 무늬로 나타나고, 잡음 적합은 얼룩으로 나타난다.
> 10. $-R^\top t=(0,0,-2)$ m에 있다. $t$ 는 카메라 프레임에서 타깃이 놓인 자리이지 카메라의 위치가 아니다(§1). 거리는 $\pm13.2$ mm로 나온다. 타깃의 겉보기 크기에서 읽으므로 $150$ px 폭에서 1픽셀이 $13.3$ mm다. 기울기는 각각 $\pm2.70°$ 로밖에 나오지 않는다. 기울기는 이미지가 크기만 바뀐 직사각형에서 벗어나는 정도로만 드러나고, 그것이 $10°$ 에 $5.2$ px이기 때문이다. $0.1$ m 태그는 $30$ px에 걸치고 $10°$ 를 기울여도 모서리가 $0.26$ px 바뀐다. 더 나쁘게는 재투영 오차에 두 번째 최소점이 있어서, $20°$ 에서 $27.5°$ 떨어진 자세가 코너를 $0.18$ px로 맞춘다. 기울기가 그저 시끄러운 것이 아니라 모호하다(§2.7). 더 큰 타깃, 멀리 떨어뜨린 여러 태그, 또는 사전 정보가 그것을 고친다.

### 과제 · Problem set

Tier B. 계속 쓰는 대상의 손목 리그, 벽까지의 거리로서의 **P5**([[02-foundations/lab-plants|0.6]]), 그리고 손-눈 오프셋 $d_{ct}=4\,\mathrm{cm}$. 시뮬레이터 없음. 위의 계산 예제는 리그를 랜드마크 $L$, $Z = 2.0$ m에서 돌렸다. 이 과제는 그것을 $L' = (0.5,\ 0.2,\ 4.0)$ m로 옮기고 어떤 오차가 자라고 어떤 오차가 줄고 어떤 오차가 그대로인지 묻는다. 그것이 변형이다.

1. **그리기.** 두 카메라, $L'$ 로 가는 두 광선, 두 상점과 그 사이의 시차. 그 옆에 같은 축척으로 $Z = 4$ m에서의 $\pm1$ px 깊이 오차 막대와 위의 그림에 있던 $Z = 2$ m의 것을 함께. 이미지 평면 위에는 $L'$ 에서의 왜곡 변위를 짧은 선분으로 더한다. 오차 셋, 서로 다른 축척 법칙 셋 — 그림이 셋을 달라 보이게 해야 한다.
2. **유도.** (a) $L'$ 을 두 카메라에 투영하라: $u_1, v_1, u_2$, 시차 $d'$, 그리고 확인 $Z = f b / d'$. (b) $d' \pm 1$ px의 깊이 오차를 정확히 구하고 1차 추정 $Z^2/(fb)$ 와 비교한 뒤, $+1$ 과 $-1$ 의 정확한 오차가 왜 같지 않은지 말하라. (c) $L'$ 에서의 왜곡 변위: $r$, 반경 계수, 픽셀 변위를 구하고, $Z = 2$ 에서의 $2.30$ px과의 비를 주도항으로 설명하라. (d) P5의 스칼라 융합: $K$, 융합한 카메라–벽 거리, $P^+$, 그리고 $d_{ct}$ 를 뺀 말단–벽 값. (e) $Z = 4$ m의 PnP: 네 타깃 코너를 $(0,0,4)$, $(0.5,0,4)$, $(0,0.4,4)$, $(0.5,0.4,4)$ m로 옮긴다. 투영한 뒤, §2.7의 지렛대 셋으로 타깃의 거리, roll, 기울기의 $1$ px 퍼짐이 $Z=2$ m에서 어떻게 바뀌는지 예측하라.
3. **해석.** (a) $AX = XB$ 에서 $A$, $B$, $X$ 중 무엇이 $4\,\mathrm{cm}$ 를 담고 있으며, $0.37$ px 보정 잔차가 그것을 보증하지 못하는 이유는? (b) 반복 패널 위 $(440, 300)$ 의 매칭은 epipolar 잔차가 정확히 0이다. 2번의 어느 숫자 하나가 그것을 잡았을지 말하고, 일반적으로 잡으려면 리그에 무엇을 더해야 하는지 말하라.

> [!note]- 그리는 법 · How to draw it
> - **왼쪽, $XZ$ 평면에서의 투영.** 원점에 광학 중심 $O$, $+Z$ 를 따라 광축, $Z = f$ 에 이미지 평면, 랜드마크, 그리고 랜드마크에서 $O$ 를 지나 이미지 평면을 가로지르는 광선.
> - **$u - c_x = f_x X / Z$ 를 주는 닮은꼴 삼각형을 표시한다.** 그것이 유도 자체이므로 그림이 둘 다 보여야 한다.
> - **가운데, 두 번째 카메라.** $X = +0.12$ 에 동일한 중심과 같은 점으로 가는 자기 광선. 두 상점과 그 사이의 시차를 적는다.
> - **더 먼 점에 대해 같은 광선 쌍을 그려 거의 평행함을 보인다.** 두 광선 사이의 각도가 깊이 정확도의 실체다.
> - **오른쪽, 깊이 오차 막대는 한 축과 한 축척을 쓴다.** $\pm1$ px 시차 오차는 $Z^2$ 로 자라고 막대도 그렇게 그려야 한다 — 위의 그림에서는 $2$ m의 $\pm0.056$ m와 $8$ m의 $\pm0.89$ m, 열여섯 배 길다.
> - **왜곡 이동은 깊이 축이 아니라 이미지 평면 위에 그린다.** 종류가 다른 오차, 잡음이 아니라 편향이기 때문이다.

> [!tip]- 정답 · Solutions
> 1. $L'$ 로 가는 두 광선은 $Z = 2$ 의 짝보다 눈에 띄게 평행에 가깝다. $Z=4$ 의 오차 막대는 $Z=2$ 것의 약 네 배로, 왜곡 선분은 맨 위 그림의 것보다 약 여덟 배 *짧게* 그려야 한다.
> 2. (a) $u_1 = 600(0.5)/4 + 320 = 395$, $v_1 = 600(0.2)/4 + 240 = 270$; 카메라 2에서 점은 $(0.38, 0.2, 4.0)$ 이므로 $u_2 = 377$, $d' = 18$ px이고 $Z = 600(0.12)/18 = 4.0$ m다. (b) $d' = 17 \Rightarrow Z = 4.235$ m($+0.235$); $d' = 19 \Rightarrow Z = 3.789$ m($-0.211$). 1차 추정은 $Z^2/(fb) = 16/72 = 0.222$ m로 둘 사이에 있고, 둘이 같지 않은 것은 $Z = fb/d$ 가 $d$ 에 대해 볼록하기 때문이다 — 시차를 잃는 쪽이 얻는 쪽보다 비싸므로, 픽셀 오차가 대칭이어도 깊이 오차 분포는 카메라에서 *멀어지는* 쪽으로 기운다. (c) $x_n = 0.125$, $y_n = 0.05$, $r^2 = 0.018125$, $r = 0.1346$; 계수는 $1 - 0.2(0.018125) + 0.05(0.018125)^2 = 0.996391$ 이라 점은 $(394.729,\ 269.892)$ 에 맺히고 변위는 $0.291$ px다. $Z = 2$ 에서의 $2.30$ px보다 $7.9$ 배 작은데, 픽셀 단위 주도 반경 변위가 $f\lvert k_1\rvert r^3$ 이고 $r$ 이 절반이 되었기 때문이다: $2^3 = 8$. (d) $K = 4/(4+1) = 0.8$, 융합 거리 $10 + 0.8(12-10) = 11.6\,\mathrm{cm}$, $P^+ = (1-0.8)4 = 0.8\,\mathrm{cm}^2$, 말단–벽 $11.6 - 4 = 7.6\,\mathrm{cm}$. (e) 코너는 $(320, 240)$, $(395, 240)$, $(320, 300)$, $(395, 300)$ px에 맺혀 $75\times60$ px 직사각형이 된다. 거리: $Z^2/(f\ell)=16/300=53.3$ mm/px로 $13.3$ 의 네 배다. 지렛대에 $Z^2$ 이 들어 있기 때문이다. Roll: $75$ px에 걸친 1픽셀은 $0.76°$ 로 $0.38°$ 의 두 배다. $Z$ 가 들어 있기 때문이다. 기울기: $fWH/Z^2=7.5$ px/rad로 $30$ 의 4분의 1이므로 퍼짐이 네 배가 된다. 코드의 공분산을 $t=(0,0,4)$ 에서 계산하면 $\pm52.7$ mm, $\pm0.73°$, $\pm10.80°$ 다. 거리와 기울기는 $Z^2$ 으로, roll은 $Z$ 로 자란다.
> 3. (a) $X$ 가 모르는 카메라–그리퍼 변환이고 $4\,\mathrm{cm}$ 는 그 평행 이동 성분 하나다. $A$ 는 두 로봇 자세 사이의 그리퍼 운동, $B$ 는 같은 두 자세 사이의 카메라 운동이다. 그것은 $(R_A - I)t_X$ 를 거쳐서만 방정식에 들어오므로, §5의 P2 회전 한 번은 그것을 $11.3$ mm의 어긋남으로 보여 주고, 회전 없는 운동은 전혀 보여 주지 못한다. $0.37$ px 잔차는 타깃 시점들 위의 *훈련* 잔차이고, §5는 바로 그 잔차를 가진 적합이 축에서 $0.5$ m 벗어난 점을 $1.67$ mm, $3$ m 벗어난 점을 $10.0$ mm 틀리게 놓는 것을 보인다 — 카메라–그리퍼 평행 이동도 같은 시점들에서 추정되므로 그 외삽 오차를 물려받는다. 홀드아웃 자세와 알려진 길이 측정만이 그것을 검사한다. (b) **삼각측량한 깊이.** 틀린 매칭은 시차가 $36$ 이 아니라 $30$ 이므로 $Z = 2.00$ m가 아니라 $2.40$ m로 삼각측량된다 — epipolar 잔차가 0이라고 보고하는 $40$ cm 오차다. $F$ 는 매칭을 선 위로 구속할 뿐 그 선을 *따라간* 위치에 대해서는 아무 말도 하지 않기 때문이다. 일반적으로는 epipolar 선을 따르지 않는 독립 제약을 더한다: 첫 짝의 epipolar 선과 각을 이루는 세 번째 시점, 직접 거리 측정(P5 센서나 라이다), 또는 똑같은 패널 둘을 구별할 만큼 강한 외양 검사 — 그런데 똑같은 패널에서는 그것이 질감이 아니라 맥락을 쓴다는 뜻이다.

### 출처

- [Szeliski, *Computer Vision: Algorithms and Applications* (공식 무료 PDF)](https://szeliski.org/Book/)
- [OpenCV 카메라 보정 튜토리얼](https://docs.opencv.org/4.x/dc/dbb/tutorial_py_calibration.html)
- [KITTI 센서 구성 — 실제 보정된 다중 센서 리그](https://www.cvlibs.net/datasets/kitti/setup.php)
- Harris, C. & Stephens, M. "A combined corner and edge detector." *Proceedings of the 4th Alvey Vision Conference*, 1988.
- Shi, J. & Tomasi, C. "Good features to track." *IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 1994.
- Lowe, D. G. "Distinctive image features from scale-invariant keypoints." *International Journal of Computer Vision* 60(2), 2004. doi:10.1023/B:VISI.0000029664.99615.94
- Rublee, E., Rabaud, V., Konolige, K. & Bradski, G. "ORB: An efficient alternative to SIFT or SURF." *IEEE International Conference on Computer Vision (ICCV)*, 2011.
- Mur-Artal, R., Montiel, J. M. M. & Tardós, J. D. "ORB-SLAM: A versatile and accurate monocular SLAM system." *IEEE Transactions on Robotics* 31(5), 2015. doi:10.1109/TRO.2015.2463671
- Fischler, M. A. & Bolles, R. C. "Random sample consensus: a paradigm for model fitting with applications to image analysis and automated cartography." *Communications of the ACM* 24(6), 1981. doi:10.1145/358669.358692
- DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperPoint: Self-supervised interest point detection and description." *CVPR Workshops*, 2018.
- Sarlin, P.-E., DeTone, D., Malisiewicz, T. & Rabinovich, A. "SuperGlue: Learning feature matching with graph neural networks." *CVPR*, 2020.
- Sun, J., Shen, Z., Wang, Y., Bao, H. & Zhou, X. "LoFTR: Detector-free local feature matching with transformers." *CVPR*, 2021.
- Persson, M. & Nordberg, K. "Lambda Twist: An accurate fast robust perspective three point (P3P) solver." *European Conference on Computer Vision (ECCV)*, 2018. [ECVA 페이지](https://www.ecva.net/papers/eccv_2018/papers_ECCV/html/Mikael_Persson_Lambda_Twist_An_ECCV_2018_paper.php). 초록이 P3P 해가 최대 넷임을 밝힌다.
- Wang, B., Hu, H. & Zhang, C. "Companion surface of danger cylinder and its role in solution variation of P3P problem." arXiv:1906.08598, 2019, preprint. [arXiv](https://arxiv.org/abs/1906.08598). 위험 원기둥, 그 위의 중근, 그리고 불안정성.
- Schweighofer, G. & Pinz, A. "Robust pose estimation from a planar target." *IEEE Transactions on Pattern Analysis and Machine Intelligence* 28(12), 2024–2030, 2006. [출판 기록](https://tugraz.elsevierpure.com/en/publications/robust-pose-estimation-from-a-planar-target-2/). 이론상 동일 평면의 점 넷이면 자세가 하나이고, 실제로는 국소 최소점이 둘이다.
- Olson, E. "AprilTag: A robust and flexible visual fiducial system." *ICRA*, 2011; Wang, J. & Olson, E. "AprilTag 2: Efficient and robust fiducial detection." *IROS*, 2016. [AprilTag 프로젝트 페이지](https://april.eecs.umich.edu/software/apriltag)
- Lindenberger, P., Sarlin, P.-E. & Pollefeys, M. "LightGlue: Local feature matching at light speed." *ICCV*, 2023. [arXiv:2306.13643](https://arxiv.org/abs/2306.13643)
- Wang, S., Leroy, V., Cabon, Y., Chidlovskii, B. & Revaud, J. "DUSt3R: Geometric 3D vision made easy." *CVPR*, 2024. [arXiv:2312.14132](https://arxiv.org/abs/2312.14132)
- Leroy, V., Cabon, Y. & Revaud, J. "Grounding image matching in 3D with MASt3R." *ECCV*, 2024. [arXiv:2406.09756](https://arxiv.org/abs/2406.09756)
- Wang, J., Chen, M., Karaev, N., Vedaldi, A., Rupprecht, C. & Novotny, D. "VGGT: Visual geometry grounded transformer." *CVPR*, 2025. [arXiv:2503.11651](https://arxiv.org/abs/2503.11651)
