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
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/se3-geometry|3D Geometry & SE(3)]] · [[02-foundations/optimization|Optimization]] (least squares)

> [!note] First pass · 처음이라면
> Read §1 (the pinhole model, with the projection written out), §5 (calibration — where most field failures actually start), §7. §2 to §4 are the machinery; read them when a paper's numbers depend on them.

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

**1. Project $L$.** In homogeneous form, with the camera frame equal to the world frame so $R = I$ and $t = 0$:

$$\tilde u = K\,[R \mid t]\,\tilde L = \begin{pmatrix}600&0&320\\0&600&240\\0&0&1\end{pmatrix}\begin{pmatrix}0.5\\0.2\\2.0\end{pmatrix} = \begin{pmatrix}940\\600\\2\end{pmatrix}$$

so dividing by the third entry gives $(u, v) = (470, 300)$ px, because the division by $Z$ that perspective performs is exactly the dehomogenization of the third coordinate.

**2. The same point in camera 2, and back to depth.** $p^{c_2} = Ip^{c_1} + t = (0.5 - 0.12,\ 0.2,\ 2.0) = (0.38, 0.2, 2.0)$, which projects to $u_2 = 600 \times 0.38/2.0 + 320 = 434$ and $v_2 = 300$. The disparity is $d = 470 - 434 = 36$ px and $Z = f b / d = 2.0$ m, then $X = (u_1 - c_x)Z/f_x = 150 \times 2/600 = 0.5$ m and $Y = (v_1 - c_y)Z/f_y = 60 \times 2/600 = 0.2$ m. The rig recovers $L$ exactly, since with $R = I$ the triangulation is algebraically the inverse of the projection.

**3. Where distortion moves it.** Normalized coordinates are $x_n = X/Z = 0.25$ and $y_n = Y/Z = 0.10$, so $r^2 = 0.0725$ and $r^4 = 0.00525625$. The radial factor is $1 + k_1r^2 + k_2r^4 = 1 - 0.0145 + 0.000263 = 0.985763$, giving $(x_d, y_d) = (0.246441, 0.098576)$ and a distorted pixel of $(467.864,\ 299.146)$. The landmark actually lands $2.30$ px from where the ideal model says, and that is at a modest $r = 0.269$; it grows as $r^2$ toward the image corners.

**4. What a sub-pixel calibration residual hides.** Suppose calibration returns $\hat f = 598$ px instead of $600$, everything else exact. Reproject the three target corners:

| Corner | true $(u,v)$ | with $\hat f = 598$ | residual |
|---|---|---|---:|
| $A=(0,0,2)$ | $(320,\ 240)$ | $(320.0,\ 240.0)$ | $0.00$ px |
| $B=(0.5,0,2)$ | $(470,\ 240)$ | $(469.5,\ 240.0)$ | $0.50$ px |
| $C=(0,0.4,2)$ | $(320,\ 360)$ | $(320.0,\ 359.6)$ | $0.40$ px |

The RMS reprojection error is $\sqrt{(0^2 + 0.5^2 + 0.4^2)/3} = 0.370$ px — comfortably "sub-pixel", and the corner at the principal point contributes nothing at all, because a focal-length error is invisible there. Now use that calibration to back-project $B$'s detection at a known $Z = 2$ m: $X = (470-320)\times 2/598 = 0.50167$ m, an error of $1.67$ mm. The relative error is $(f - \hat f)/\hat f = 0.334\%$ of the off-axis distance, so it is $1.67$ mm at $X = 0.5$ m and $10.0$ mm at $X = 3$ m. A sub-pixel residual is a statement about the fit, not about the metre.

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
a 12.5% jump at this range: depth error grows quadratically with distance. Across the optical axis the same pixel is worth only $Z/f$ metres, and turning a pixel-noise σ into the measurement variance a filter needs is [[04-robotics/sensor-models|3.2 Sensor Models & Noise §5 and §8]].



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



### 2.5 Image features: detect, describe, match

**The idea in one sentence:** pick a few hundred points that can be found again in another image, give each a compact fingerprint, and pair fingerprints across images — those pairs are the correspondences every geometric step needs.

Why sparse points instead of every pixel? Stereo depth in §2 needs to know which right-image pixel shows the same point as a left-image pixel. Calibration in §5 needs target corners located to sub-pixel accuracy. Visual odometry and SLAM ([[04-robotics/state-estimation-slam|state estimation]]) track the same points across frames to constrain pose. A point is useful only if it is **repeatable** (detected again after the view changes) and **distinctive** (its neighbourhood does not resemble many others). The pipeline has three stages, and a paper can change any one of them.

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

> [!example] Worked example · 계산 예제
> Take three 5×5 patches with intensities 0 or 10. Use central differences, $I_x=(I_{x+1}-I_{x-1})/2$, on the inner 3×3 pixels, with $w=1$ and $k=0.05$.
> - **Flat** (all 10): every gradient is 0, so $M=0$, $\lambda=(0,0)$ and $R=0$.
> - **Edge** (left two columns 0, the rest 10): $I_x=5$ at 6 pixels and $I_y=0$, so $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$ and $R=0-0.05\cdot150^2=-1125$.
> - **Corner** (bright lower-right 3×3 block): $I_x=5$ at 4 pixels, $I_y=5$ at 4, both at 1, so $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$ and $R=9375-0.05\cdot200^2=7375$.
>
> The signs follow the rule — flat 0, edge negative, corner positive — and the Shi–Tomasi scores are 0, 0 and 75.
>
> **Ratio test.** A descriptor's three nearest candidates lie at distances 0.20, 0.23 and 0.61. Since $0.20/0.23=0.87>0.8$, reject the match even though 0.20 is the best: two similar candidates usually mean repeated structure. The third distance plays no role. Had the second been 0.45, $0.20/0.45=0.44$ would pass.

The same response on a synthetic image, with a check that the corner pixel scores highest:

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
img[10:, 10:] = 1.0                                  # one bright quadrant, corner at (10, 10)
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

- The **essential matrix** $E = [t]_\times R$ works in **calibrated** (normalized) coordinates, where $R, t$ are the second camera's rotation and translation relative to the first and $[t]_\times$ is the skew-symmetric matrix with $[t]_\times a = t \times a$. It has **five** degrees of freedom — three for $R$, three for $t$, minus one because scale is unrecoverable — and its singular values are $(\sigma, \sigma, 0)$, so it is rank 2.
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

### 3. Point clouds and frames

A depth image plus intrinsics back-projects to a **point cloud**:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. Every cloud lives in some frame — sensor, base,
map — and multi-sensor pipelines stand or fall on the **extrinsic calibration** between
those frames ([[04-robotics/robot-systems-deployment|the TF tree at runtime]]). A
plausible-looking cloud in the wrong frame produces systematic, learning-resistant errors.

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

In the hand–eye equation $AX=XB$ for a wrist-mounted camera, $A$ is the gripper's motion between two robot poses (known from the joint encoders), $B$ is the camera's motion between the same two poses (measured from the target), and $X$ is the unknown camera-to-gripper transform. Each pair of poses gives one equation, and several pairs with different rotation axes pin $X$ down.

The quality metric is usually **reprojection error**: project the estimated 3D points
through the estimated model and measure pixel distance to their detections. Low
reprojection error on the calibration set does **not** guarantee accuracy outside the
calibrated volume, range, or temperature, because the model was fitted only at the target positions, distances and conditions actually observed; outside them it is extrapolating, not obeying a physical law.

**Reprojection error, stated completely.** For one 3D point $X_j$ seen in one view $i$, it is a **distance in pixels** between two image points: the detected feature $\tilde u_{ij}$ and the projection of $X_j$ through the current model. Writing $\pi(\cdot)$ for the full pipeline of §1 — extrinsics, perspective division, distortion, then $K$ —

$$e_{ij} = \big\lVert\, \tilde u_{ij} - \pi\big(K, d, T_i, X_j\big) \,\big\rVert_2$$

Three conditions are what make it *the* metric. It is measured **in the image**, where the noise actually is, so least squares on it is the maximum-likelihood estimate under isotropic Gaussian pixel noise ([[02-foundations/optimization|4. Optimization §3]]) — an error measured in metres in 3D would be weighting a quantity the camera never observed. It is **per observation**, so every $(i,j)$ pair contributes. And it depends on **every** parameter at once: move $K$, a distortion coefficient, a pose or the point, and $e_{ij}$ moves. That is why calibration and bundle adjustment are the same optimization with different variables held fixed.

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
$\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$, and commands a twist that reduces
$\xi$. Its accuracy inherits calibration and pose-estimation errors. **IBVS** stays in the
image: for image features $s$, $\dot s=L_s v_c$, where the image Jacobian $L_s$ depends on
feature depth; a local law such as $v_c=-\lambda L_s^+(s-s^*)$ reduces pixel error. IBVS can
be less sensitive to full pose reconstruction but still needs depth estimates and a
well-conditioned feature geometry. Neither equation alone guarantees visibility, actuator
limits, global convergence, or collision avoidance. Read a "closed-loop perception" claim
by identifying the error, Jacobian, control rate, depth source, and recovery outside the
local basin.

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

### Problem set · 과제

Tier B. The wrist rig of the Running object, plus **P5** as a range to a wall ([[02-foundations/lab-plants|0.6]]) and the hand–eye offset $d_{ct}=4\,\mathrm{cm}$. No simulator. The Worked case ran the rig at the landmark $L$, $Z = 2.0$ m. This set moves it to $L' = (0.5,\ 0.2,\ 4.0)$ m and asks which errors grow, which shrink, and which stay put — that is the variant.

1. **Draw.** Both cameras, both rays to $L'$, the two image points and the disparity between them. Beside them, and to the same scale, the $\pm1$ px depth error bar at $Z = 4$ m and the one at $Z = 2$ m from the picture above. Add the distortion shift at $L'$ as a short segment on the image plane. Three errors, three different scaling laws — the drawing has to make them look different.
2. **Derive.** (a) Project $L'$ into both cameras: $u_1, v_1, u_2$, the disparity $d'$, and the check $Z = f b / d'$. (b) The depth error for $d' \pm 1$ px, exactly, and compare it with the first-order estimate $Z^2/(fb)$; say why the exact $+1$ and $-1$ errors are not equal. (c) The distortion shift at $L'$: compute $r$, the radial factor, and the shift in pixels, then explain the ratio to the $2.30$ px at $Z = 2$ using the leading term. (d) P5's scalar fusion: $K$, the fused camera-to-wall range, $P^+$, and the tip-to-wall number after $d_{ct}$.
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
> 2. (a) $u_1 = 600(0.5)/4 + 320 = 395$, $v_1 = 600(0.2)/4 + 240 = 270$; in camera 2 the point is $(0.38, 0.2, 4.0)$, so $u_2 = 377$ and $d' = 18$ px, giving $Z = 600(0.12)/18 = 4.0$ m. (b) $d' = 17 \Rightarrow Z = 4.235$ m ($+0.235$); $d' = 19 \Rightarrow Z = 3.789$ m ($-0.211$). The first-order estimate is $Z^2/(fb) = 16/72 = 0.222$ m, between the two, and the two are unequal because $Z = fb/d$ is convex in $d$ — losing disparity costs more than gaining it, so the depth error distribution is skewed *away* from the camera even when the pixel error is symmetric. (c) $x_n = 0.125$, $y_n = 0.05$, $r^2 = 0.018125$, $r = 0.1346$; the factor is $1 - 0.2(0.018125) + 0.05(0.018125)^2 = 0.996391$, so the point lands at $(394.729,\ 269.892)$ and the shift is $0.291$ px. That is $7.9$ times smaller than the $2.30$ px at $Z = 2$, because the leading radial displacement in pixels is $f\lvert k_1\rvert r^3$ and $r$ halved: $2^3 = 8$. (d) $K = 4/(4+1) = 0.8$, fused range $10 + 0.8(12-10) = 11.6\,\mathrm{cm}$, $P^+ = (1-0.8)4 = 0.8\,\mathrm{cm}^2$, tip-to-wall $11.6 - 4 = 7.6\,\mathrm{cm}$.
> 3. (a) $X$ is the unknown camera-to-gripper transform and the $4\,\mathrm{cm}$ is one translation component of it; $A$ is the gripper's motion between two robot poses, $B$ the camera's motion between the same two. A $0.37$ px residual is a *training* residual on the target views, and §5 shows a fit with exactly that residual still misplacing a point by $1.67$ mm at $0.5$ m off-axis and $10.0$ mm at $3$ m — the camera-to-gripper translation is estimated from those same views, so it inherits that extrapolation error. Only a held-out pose and a measured known length test it. (b) **The triangulated depth.** The wrong match has disparity $30$ instead of $36$, so it triangulates to $Z = 2.40$ m rather than $2.00$ m — a $40$ cm error that the epipolar residual reports as zero, because $F$ constrains a match to a line and says nothing about position *along* it. In general you add an independent constraint that is not along the epipolar line: a third view whose epipolar lines cross the first pair at an angle, a direct range measurement (the P5 sensor, or lidar), or an appearance check strong enough to tell two identical panels apart — which, on identical panels, means using their context rather than their texture.

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
> [[02-foundations/linear-algebra|선형대수]] · [[02-foundations/se3-geometry|3D 기하와 SE(3)]] · [[02-foundations/optimization|최적화]] (최소제곱)

> [!note] 처음이라면 · First pass
> 먼저 §1(핀홀 모델, 투영식까지), §5(보정 — 현장 실패가 실제로 시작되는 곳), §7. §2~§4는 기계장치이고, 논문의 숫자가 거기 기댈 때 읽어라.

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

**1. $L$ 을 투영한다.** 카메라 프레임을 세계 프레임과 같게 두어 $R = I$, $t = 0$ 인 동차 형태로

$$\tilde u = K\,[R \mid t]\,\tilde L = \begin{pmatrix}600&0&320\\0&600&240\\0&0&1\end{pmatrix}\begin{pmatrix}0.5\\0.2\\2.0\end{pmatrix} = \begin{pmatrix}940\\600\\2\end{pmatrix}$$

세 번째 성분으로 나누면 $(u, v) = (470, 300)$ px다. 원근이 수행하는 $Z$ 로 나누기가 정확히 세 번째 좌표의 비동차화이기 때문이다.

**2. 같은 점을 카메라 2에서, 그리고 깊이로 되돌리기.** $p^{c_2} = Ip^{c_1} + t = (0.5 - 0.12,\ 0.2,\ 2.0) = (0.38, 0.2, 2.0)$ 이므로 $u_2 = 600 \times 0.38/2.0 + 320 = 434$, $v_2 = 300$ 이다. 시차는 $d = 470 - 434 = 36$ px, $Z = f b / d = 2.0$ m이고, 이어서 $X = (u_1 - c_x)Z/f_x = 150 \times 2/600 = 0.5$ m, $Y = (v_1 - c_y)Z/f_y = 60 \times 2/600 = 0.2$ m다. 리그가 $L$ 을 정확히 복원한다. $R = I$ 일 때 삼각측량이 대수적으로 투영의 역이기 때문이다.

**3. 왜곡이 그것을 어디로 옮기는가.** 정규화 좌표는 $x_n = X/Z = 0.25$, $y_n = Y/Z = 0.10$ 이므로 $r^2 = 0.0725$, $r^4 = 0.00525625$ 다. 반경 계수는 $1 + k_1r^2 + k_2r^4 = 1 - 0.0145 + 0.000263 = 0.985763$ 이라 $(x_d, y_d) = (0.246441, 0.098576)$ 이 되고 왜곡된 픽셀은 $(467.864,\ 299.146)$ 이다. 랜드마크는 이상적 모델이 말하는 자리에서 실제로 $2.30$ px 떨어져 맺히는데, 그것도 $r = 0.269$ 라는 온건한 값에서다. 이미지 모서리로 갈수록 $r^2$ 로 자란다.

**4. 서브픽셀 보정 잔차가 감추는 것.** 보정이 $600$ 대신 $\hat f = 598$ px를 돌려주고 나머지는 정확하다고 하자. 타깃 코너 셋을 다시 투영하면

| 코너 | 참 $(u,v)$ | $\hat f = 598$ 로 | 잔차 |
|---|---|---|---:|
| $A=(0,0,2)$ | $(320,\ 240)$ | $(320.0,\ 240.0)$ | $0.00$ px |
| $B=(0.5,0,2)$ | $(470,\ 240)$ | $(469.5,\ 240.0)$ | $0.50$ px |
| $C=(0,0.4,2)$ | $(320,\ 360)$ | $(320.0,\ 359.6)$ | $0.40$ px |

RMS reprojection error는 $\sqrt{(0^2 + 0.5^2 + 0.4^2)/3} = 0.370$ px로 넉넉히 "서브픽셀"이고, 주점에 있는 코너는 아무 기여도 하지 않는다. 초점 거리 오차가 거기서는 보이지 않기 때문이다. 이제 그 보정으로 $Z = 2$ m를 아는 $B$ 의 검출을 역투영하면 $X = (470-320)\times 2/598 = 0.50167$ m, 곧 $1.67$ mm의 오차다. 상대 오차는 축에서 벗어난 거리의 $(f - \hat f)/\hat f = 0.334\%$ 이므로 $X = 0.5$ m에서 $1.67$ mm, $X = 3$ m에서 $10.0$ mm다. 서브픽셀 잔차는 적합에 대한 진술이지 미터에 대한 진술이 아니다.

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
튄다: 깊이 오차는 거리에 제곱으로 자란다. 광축을 가로지르는 방향에서는 같은 1픽셀이 $Z/f$미터일 뿐이고, 픽셀 잡음 σ를 필터가 쓰는 측정 분산으로 바꾸는 일은 [[04-robotics/sensor-models|3.2 센서 모델과 잡음 §5와 §8]]에 있다.

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



### 2.5 이미지 특징: 검출, 기술, 매칭

**한 문장으로:** 다른 이미지에서 다시 찾을 수 있는 점 수백 개를 고르고, 점마다 짧은 지문을 붙이고, 이미지 사이에서 지문을 짝짓는다. 그 짝이 모든 기하 단계가 필요로 하는 대응점이다.

왜 모든 픽셀이 아니라 드문드문한 점인가? §2의 스테레오 깊이는 왼쪽 이미지의 픽셀이 오른쪽 어느 픽셀과 같은 점인지 알아야 한다. §5의 보정은 타깃 모서리를 서브픽셀 정확도로 찾아야 한다. Visual odometry와 SLAM([[04-robotics/state-estimation-slam|상태 추정]])은 같은 점을 프레임마다 추적해 pose를 제약한다. 점이 쓸모 있으려면 **반복성**(시점이 바뀌어도 다시 검출됨)과 **변별성**(주변이 다른 많은 곳과 닮지 않음)을 갖춰야 한다. 파이프라인은 세 단계이고, 논문은 그중 어느 단계든 바꿀 수 있다.

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

> [!example] 계산 예제 · Worked example
> 밝기가 0 또는 10인 5×5 패치 세 개를 잡는다. 안쪽 3×3 픽셀에서 중앙 차분 $I_x=(I_{x+1}-I_{x-1})/2$를 쓰고, $w=1$, $k=0.05$로 둔다.
> - **평탄** (전부 10): 기울기가 모두 0이므로 $M=0$, $\lambda=(0,0)$, $R=0$이다.
> - **에지** (왼쪽 두 열 0, 나머지 10): $I_x=5$인 픽셀이 6개이고 $I_y=0$이므로 $M=\begin{pmatrix}150&0\\0&0\end{pmatrix}$, $\lambda=(0,150)$, $R=0-0.05\cdot150^2=-1125$다.
> - **코너** (오른쪽 아래 3×3 블록만 밝음): $I_x=5$인 픽셀 4개, $I_y=5$인 픽셀 4개, 둘 다인 픽셀 1개이므로 $M=\begin{pmatrix}100&25\\25&100\end{pmatrix}$, $\lambda=(75,125)$, $R=9375-0.05\cdot200^2=7375$다.
>
> 부호가 규칙대로다 — 평탄 0, 에지 음수, 코너 양수. Shi–Tomasi 점수는 0, 0, 75다.
>
> **비율 검사.** 어떤 기술자의 가장 가까운 후보 세 개가 거리 0.20, 0.23, 0.61에 있다. $0.20/0.23=0.87>0.8$이므로 0.20이 1등인데도 매칭을 버린다. 비슷한 후보가 둘이면 대개 반복 구조다. 세 번째 거리는 아무 역할도 하지 않는다. 두 번째가 0.45였다면 $0.20/0.45=0.44$로 통과했을 것이다.

같은 응답을 합성 이미지에 계산하고, 코너 픽셀의 점수가 가장 큰지 확인하는 코드다.

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
img[10:, 10:] = 1.0                                  # one bright quadrant, corner at (10, 10)
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

- **Essential matrix** $E = [t]_\times R$ 는 **보정된**(정규화) 좌표에서 작동한다. $R, t$ 는 첫 카메라에 대한 둘째 카메라의 회전과 평행 이동이고 $[t]_\times$ 는 $[t]_\times a = t \times a$ 인 반대칭 행렬이다. 자유도는 **다섯**이다 — $R$ 에서 셋, $t$ 에서 셋, 스케일을 복원할 수 없어 하나를 뺀다 — 특잇값은 $(\sigma, \sigma, 0)$ 이라 rank 2다.
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

### 3. 포인트 클라우드와 프레임

깊이 이미지 + intrinsics를 역투영하면 **포인트 클라우드**가 된다:
$X = (u-c_x)Z/f_x$, $Y=(v-c_y)Z/f_y$. 모든 클라우드는 어떤 프레임(센서·베이스·맵)에
산다 — 다중 센서 파이프라인은 그 프레임들 사이의 **extrinsic 보정**에 성패가 달려 있다
([[04-robotics/robot-systems-deployment|런타임에서는 TF 트리]]). 그럴듯해 보여도 틀린
프레임의 클라우드는 학습으로 잘 고쳐지지 않는 계통 오차를 만든다.

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

손목에 단 카메라의 hand–eye 방정식 $AX=XB$에서 $A$는 두 로봇 자세 사이의 그리퍼 운동(관절 엔코더로 안다), $B$는 같은 두 자세 사이의 카메라 운동(타깃으로 측정한다), $X$는 모르는 카메라–그리퍼 변환이다. 자세 한 쌍이 방정식 하나를 주고, 회전축이 서로 다른 여러 쌍이 모여야 $X$가 정해진다.

품질 지표는 대개 **reprojection error**다: 추정된 3D 점을 추정된 모델로 투영해 검출
위치와의 픽셀 거리를 잰다. 보정 세트에서 낮은 reprojection error가 보정된 부피·거리·
온도 밖에서의 정확도를 보장하지는 **않는다**. 모델은 타깃을 실제로 관측한 위치·거리·조건에서만 맞춰졌으므로, 그 밖에서는 물리 법칙을 따르는 것이 아니라 외삽하고 있을 뿐이다.

**Reprojection error의 완전한 정의.** 한 시점 $i$ 에서 보인 3D 점 $X_j$ 하나에 대해, 이것은 이미지 점 둘 사이의 **픽셀 단위 거리**다: 검출된 특징 $\tilde u_{ij}$ 와 현재 모델로 투영한 $X_j$. §1의 전체 파이프라인 — extrinsics, 원근 나눗셈, 왜곡, 그리고 $K$ — 을 $\pi(\cdot)$ 로 쓰면

$$e_{ij} = \big\lVert\, \tilde u_{ij} - \pi\big(K, d, T_i, X_j\big) \,\big\rVert_2$$

이것을 *그* 지표로 만드는 조건이 셋이다. 잡음이 실제로 있는 곳인 **이미지에서** 재므로, 이것에 대한 최소자승이 등방 가우시안 픽셀 잡음 아래의 최대우도 추정이다([[02-foundations/optimization|4. 최적화 §3]]) — 3D에서 미터로 잰 오차는 카메라가 관측한 적 없는 양에 가중치를 주는 것이다. **관측마다** 하나이므로 모든 $(i,j)$ 짝이 기여한다. 그리고 **모든** 파라미터에 동시에 의존한다: $K$, 왜곡 계수 하나, pose, 점 중 무엇을 움직여도 $e_{ij}$ 가 움직인다. 보정과 bundle adjustment가 어떤 변수를 고정하느냐만 다른 같은 최적화인 이유가 그것이다.

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
추정해 $\xi=\operatorname{Log}(T_{current}^{-1}T_{desired})^\vee$ 같은 pose error를 만들고,
$\xi$를 줄이는 twist를 명령한다. 정확도는 보정과 pose 추정 오차를 물려받는다. **IBVS**는
이미지에 남는다. 특징 $s$에 대해 $\dot s=L_s v_c$이고 image Jacobian $L_s$는 특징 깊이에
의존한다. $v_c=-\lambda L_s^+(s-s^*)$ 같은 국소 법칙이 픽셀 오차를 줄인다. IBVS는 완전한
pose 복원에 덜 민감할 수 있지만 여전히 깊이 추정과 조건이 좋은 특징 기하가 필요하다. 어느 식도
시야 유지, 구동기 한계, 전역 수렴, 충돌 회피를 혼자 보장하지 않는다. "closed-loop perception"
주장은 오차·야코비안·제어 주기·깊이 출처와 국소 수렴 영역 밖의 회복을 확인해 읽는다.

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

### 과제 · Problem set

Tier B. 계속 쓰는 대상의 손목 리그, 벽까지의 거리로서의 **P5**([[02-foundations/lab-plants|0.6]]), 그리고 손-눈 오프셋 $d_{ct}=4\,\mathrm{cm}$. 시뮬레이터 없음. 위의 계산 예제는 리그를 랜드마크 $L$, $Z = 2.0$ m에서 돌렸다. 이 과제는 그것을 $L' = (0.5,\ 0.2,\ 4.0)$ m로 옮기고 어떤 오차가 자라고 어떤 오차가 줄고 어떤 오차가 그대로인지 묻는다. 그것이 변형이다.

1. **그리기.** 두 카메라, $L'$ 로 가는 두 광선, 두 상점과 그 사이의 시차. 그 옆에 같은 축척으로 $Z = 4$ m에서의 $\pm1$ px 깊이 오차 막대와 위의 그림에 있던 $Z = 2$ m의 것을 함께. 이미지 평면 위에는 $L'$ 에서의 왜곡 변위를 짧은 선분으로 더한다. 오차 셋, 서로 다른 축척 법칙 셋 — 그림이 셋을 달라 보이게 해야 한다.
2. **유도.** (a) $L'$ 을 두 카메라에 투영하라: $u_1, v_1, u_2$, 시차 $d'$, 그리고 확인 $Z = f b / d'$. (b) $d' \pm 1$ px의 깊이 오차를 정확히 구하고 1차 추정 $Z^2/(fb)$ 와 비교한 뒤, $+1$ 과 $-1$ 의 정확한 오차가 왜 같지 않은지 말하라. (c) $L'$ 에서의 왜곡 변위: $r$, 반경 계수, 픽셀 변위를 구하고, $Z = 2$ 에서의 $2.30$ px과의 비를 주도항으로 설명하라. (d) P5의 스칼라 융합: $K$, 융합한 카메라–벽 거리, $P^+$, 그리고 $d_{ct}$ 를 뺀 말단–벽 값.
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
> 2. (a) $u_1 = 600(0.5)/4 + 320 = 395$, $v_1 = 600(0.2)/4 + 240 = 270$; 카메라 2에서 점은 $(0.38, 0.2, 4.0)$ 이므로 $u_2 = 377$, $d' = 18$ px이고 $Z = 600(0.12)/18 = 4.0$ m다. (b) $d' = 17 \Rightarrow Z = 4.235$ m($+0.235$); $d' = 19 \Rightarrow Z = 3.789$ m($-0.211$). 1차 추정은 $Z^2/(fb) = 16/72 = 0.222$ m로 둘 사이에 있고, 둘이 같지 않은 것은 $Z = fb/d$ 가 $d$ 에 대해 볼록하기 때문이다 — 시차를 잃는 쪽이 얻는 쪽보다 비싸므로, 픽셀 오차가 대칭이어도 깊이 오차 분포는 카메라에서 *멀어지는* 쪽으로 기운다. (c) $x_n = 0.125$, $y_n = 0.05$, $r^2 = 0.018125$, $r = 0.1346$; 계수는 $1 - 0.2(0.018125) + 0.05(0.018125)^2 = 0.996391$ 이라 점은 $(394.729,\ 269.892)$ 에 맺히고 변위는 $0.291$ px다. $Z = 2$ 에서의 $2.30$ px보다 $7.9$ 배 작은데, 픽셀 단위 주도 반경 변위가 $f\lvert k_1\rvert r^3$ 이고 $r$ 이 절반이 되었기 때문이다: $2^3 = 8$. (d) $K = 4/(4+1) = 0.8$, 융합 거리 $10 + 0.8(12-10) = 11.6\,\mathrm{cm}$, $P^+ = (1-0.8)4 = 0.8\,\mathrm{cm}^2$, 말단–벽 $11.6 - 4 = 7.6\,\mathrm{cm}$.
> 3. (a) $X$ 가 모르는 카메라–그리퍼 변환이고 $4\,\mathrm{cm}$ 는 그 평행 이동 성분 하나다. $A$ 는 두 로봇 자세 사이의 그리퍼 운동, $B$ 는 같은 두 자세 사이의 카메라 운동이다. $0.37$ px 잔차는 타깃 시점들 위의 *훈련* 잔차이고, §5는 바로 그 잔차를 가진 적합이 축에서 $0.5$ m 벗어난 점을 $1.67$ mm, $3$ m 벗어난 점을 $10.0$ mm 틀리게 놓는 것을 보인다 — 카메라–그리퍼 평행 이동도 같은 시점들에서 추정되므로 그 외삽 오차를 물려받는다. 홀드아웃 자세와 알려진 길이 측정만이 그것을 검사한다. (b) **삼각측량한 깊이.** 틀린 매칭은 시차가 $36$ 이 아니라 $30$ 이므로 $Z = 2.00$ m가 아니라 $2.40$ m로 삼각측량된다 — epipolar 잔차가 0이라고 보고하는 $40$ cm 오차다. $F$ 는 매칭을 선 위로 구속할 뿐 그 선을 *따라간* 위치에 대해서는 아무 말도 하지 않기 때문이다. 일반적으로는 epipolar 선을 따르지 않는 독립 제약을 더한다: 첫 짝의 epipolar 선과 각을 이루는 세 번째 시점, 직접 거리 측정(P5 센서나 라이다), 또는 똑같은 패널 둘을 구별할 만큼 강한 외양 검사 — 그런데 똑같은 패널에서는 그것이 질감이 아니라 맥락을 쓴다는 뜻이다.

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
