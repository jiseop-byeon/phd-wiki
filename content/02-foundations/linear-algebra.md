---
title: 1. Linear Algebra
tags: [foundations]
study-depth: Working
depth-goal: "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments."
mastery-when: "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/engineering-math|0.5 §1]] (partial derivatives, gradient) · [[02-foundations/engineering-math|0.5 §4]] (matrix multiplication, transpose, inverse) · [[02-foundations/engineering-math|0.5 §4.5]] (linearity) · [[02-foundations/engineering-math|0.5 §10]] (Σ, argmax, norm notation) · plant **P2**, the catalog's planar two-link arm, from [[02-foundations/lab-plants|0.6 Lab Plants]] (a *plant* is the system being controlled; the catalog freezes six small ones so that every page can reuse them by name) · [[02-foundations/neural-network-basics|0.8]] for the machine-learning words the examples use (layer, token, embedding)
> [[02-foundations/engineering-math|0.5 §1]](편미분·그래디언트) · [[02-foundations/engineering-math|0.5 §4]](행렬곱·전치·역행렬) · [[02-foundations/engineering-math|0.5 §4.5]](선형성) · [[02-foundations/engineering-math|0.5 §10]](Σ·argmax·노름 표기) · [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**(카탈로그의 평면 2링크 팔. 장치(plant)는 제어되는 시스템을 뜻하고, 카탈로그는 작은 장치 여섯 개를 숫자까지 고정해 어느 페이지든 이름으로 다시 쓰게 한다) · 예제에 쓰이는 기계학습 어휘(층·토큰·임베딩)는 [[02-foundations/neural-network-basics|0.8]]
>
> Connection map · 연결 지도: [[02-foundations/overview|0. Overview]]

## English

*Stands on [[02-foundations/engineering-math|0.5]] and [[02-foundations/neural-network-basics|0.8]]. First corner of the core triangle: a matrix is a map, with a rank,
eigenvalues and an SVD (singular value decomposition). The later pages that name it as a prerequisite include calculus, probability, optimization, SE(3) and manipulator dynamics.*

Deep learning *is* linear algebra with nonlinearities between the matrix multiplies.
This page is a course-depth treatment: definitions, derivations, worked examples, and
where each concept appears in the papers of this wiki.

> [!note] Why this matters · 왜 배우는가
> On the [[physical-ai-map|Physical AI Map]], linear algebra is part of the mathematics floor under the physical-AI stack of [[07-research-program/index|7. Research Program §5]], directly beneath motion planning, manipulation and contact: in *"Install that panel on the frame"* it is how the robot identifies panel and frame from more measurements than unknowns (the least squares of §2), and how it moves the component, because the Jacobian $J$ of this page's picture turns joint rates into the panel's velocity. Near a stretched-arm pose $J$ loses rank and $J^{-1}$ demands unbounded joint speeds, so an inverse-kinematics loop lunges at the frame; §4.5's damped least squares, which at $\lambda=0.01$ turns a near-singular $1/\sigma$ of $100$ into $0.99$, is a fix you can choose only if you can read singular values. On the dissertation path ([[07-research-program/index|7. Research Program §8]]) the page is used in block 1 by [[02-foundations/manipulator-kinematics-dynamics|10. Manipulator Kinematics & Dynamics §2 and §6]], in block 2 by [[04-robotics/control-theory-ce397|5. Control Theory §2]] and [[04-robotics/system-identification|5.5 System Identification §3]], in block 3 by [[04-robotics/force-compliance-control|13. Force & Compliance Control §4]], and in block 7 by [[05-construction-robotics/imitating-contact|10. Imitating Contact §2]], whose behaviour cloning is solved by §2's normal equations. After it you can read any $y=Wx$ by rows and by columns, fit a least-squares line and check its residual, and say from a Jacobian's singular values how near a pose is to singular.

> [!note] First pass · 처음이라면
> About four 60–90-minute sessions, three to read and one to practise. **Session 1:** the picture, §1 (what a matrix does, read by rows and by columns on P2) and §2 through rank and the null space; the collapsed boxes can wait. **Session 2:** §2's least squares with its gradient derivation and worked fit, then §3 through the worked $2\times2$, its figure and the gradient-descent rate. **Session 3:** the rest of §3 (the condition number $\kappa_2$ and definiteness), §4's first two bullets and its worked $C$ (what singular values are), the shape table and P2 case of §4.5, and §6. **Session 4,** closed-book: self-check 1–4, then the problem set (Draw, Derive, Interpret), which needs exactly these pieces. Second pass: the rest of §4 (SVD) when a paper factorises something, the rest of §4.5 the first time you meet $J^\dagger$ on the robotics track, and §5 when you reach the control track.

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 218" style="max-width:100%;height:auto" role="img" aria-label="P2 at theta = (0, 90 degrees): the arm to scale, the two columns of J as arrows at the tip, (-1, 1) and (-1, 0), each perpendicular to its joint-to-tip segment; the unit circle of joint rates and the ellipse it maps to, semi-axes 1.618 and 0.618, kappa 2.618; and the straight arm, where the columns are parallel and det J = 0.">
  <defs><marker id="laHw" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="10" y="32" width="160" height="160" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="24" font-size="11" text-anchor="middle" fill="currentColor">joint-rate space (θ̇<tspan dy="3.5">1</tspan><tspan dy="-3.5">, θ̇</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">)</tspan></text>
  <polyline points="16,112 164,112" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <polyline points="90,186 90,38" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <polyline points="162,112 161.9,115.8 161.6,119.5 161.1,123.3 160.4,127 159.5,130.6 158.5,134.2 157.2,137.8 155.8,141.3 154.2,144.7 152.4,148 150.4,151.2 148.2,154.3 146,157.3 143.5,160.2 140.9,162.9 138.2,165.5 135.3,168 132.3,170.2 129.2,172.4 126,174.4 122.7,176.2 119.3,177.8 115.8,179.2 112.2,180.5 108.6,181.5 105,182.4 101.3,183.1 97.5,183.6 93.8,183.9 90,184 86.2,183.9 82.5,183.6 78.7,183.1 75,182.4 71.4,181.5 67.8,180.5 64.2,179.2 60.7,177.8 57.3,176.2 54,174.4 50.8,172.4 47.7,170.2 44.7,168 41.8,165.5 39.1,162.9 36.5,160.2 34,157.3 31.8,154.3 29.6,151.2 27.6,148 25.8,144.7 24.2,141.3 22.8,137.8 21.5,134.2 20.5,130.6 19.6,127 18.9,123.3 18.4,119.5 18.1,115.8 18,112 18.1,108.2 18.4,104.5 18.9,100.7 19.6,97 20.5,93.4 21.5,89.8 22.8,86.2 24.2,82.7 25.8,79.3 27.6,76 29.6,72.8 31.8,69.7 34,66.7 36.5,63.8 39.1,61.1 41.8,58.5 44.7,56 47.7,53.8 50.8,51.6 54,49.6 57.3,47.8 60.7,46.2 64.2,44.8 67.8,43.5 71.4,42.5 75,41.6 78.7,40.9 82.5,40.4 86.2,40.1 90,40 93.8,40.1 97.5,40.4 101.3,40.9 105,41.6 108.6,42.5 112.2,43.5 115.8,44.8 119.3,46.2 122.7,47.8 126,49.6 129.2,51.6 132.3,53.8 135.3,56 138.2,58.5 140.9,61.1 143.5,63.8 146,66.7 148.2,69.7 150.4,72.8 152.4,76 154.2,79.3 155.8,82.7 157.2,86.2 158.5,89.8 159.5,93.4 160.4,97 161.1,100.7 161.6,104.5 161.9,108.2 162,112" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="162" cy="112" r="2.6" fill="currentColor"/>
  <circle cx="90" cy="40" r="2.6" fill="currentColor"/>
  <text x="156" y="106" font-size="11" text-anchor="end" fill="currentColor">(1, 0)</text>
  <text x="95" y="60" font-size="11" fill="currentColor">(0, 1)</text>
  <text x="158" y="127" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">θ̇<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="84" y="57" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">θ̇<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="56" y="148" font-size="11" text-anchor="middle" fill="currentColor">area π</text>
  <polyline points="174,60 203,60" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#laHw)"/>
  <text x="188.5" y="53" font-size="12" text-anchor="middle" fill="currentColor">J</text>
  <polygon points="238,40 235.5,40 233.2,40.2 230.9,40.4 228.7,40.7 226.6,41.1 224.6,41.6 222.7,42.1 220.9,42.8 219.3,43.5 217.7,44.3 216.3,45.2 214.9,46.2 213.7,47.3 212.6,48.4 211.6,49.6 210.8,50.9 210,52.3 209.4,53.8 208.9,55.3 208.6,56.8 208.3,58.5 208.2,60.2 208.2,62 208.3,63.8 208.6,65.7 208.9,67.7 209.4,69.7 210,71.7 210.8,73.8 211.6,76 212.6,78.2 213.7,80.4 214.9,82.7 216.3,85 217.7,87.4 219.3,89.8 220.9,92.2 222.7,94.6 224.6,97 226.6,99.5 228.7,102 230.9,104.5 233.2,107 235.5,109.5 238,112 240.6,114.5 243.2,117 245.9,119.5 248.7,122 251.6,124.5 254.5,127 257.6,129.4 260.6,131.8 263.8,134.2 267,136.6 270.2,139 273.5,141.3 276.8,143.6 280.2,145.8 283.6,148 287.1,150.2 290.6,152.3 294.1,154.3 297.6,156.3 301.1,158.3 304.7,160.2 308.2,162 311.8,163.8 315.3,165.5 318.9,167.2 322.4,168.7 325.9,170.2 329.4,171.7 332.9,173.1 336.4,174.4 339.8,175.6 343.2,176.7 346.5,177.8 349.8,178.8 353,179.7 356.2,180.5 359.4,181.2 362.4,181.9 365.5,182.4 368.4,182.9 371.3,183.3 374.1,183.6 376.8,183.8 379.4,184 382,184 384.5,184 386.8,183.8 389.1,183.6 391.3,183.3 393.4,182.9 395.4,182.4 397.3,181.9 399.1,181.2 400.7,180.5 402.3,179.7 403.7,178.8 405.1,177.8 406.3,176.7 407.4,175.6 408.4,174.4 409.2,173.1 410,171.7 410.6,170.2 411.1,168.7 411.4,167.2 411.7,165.5 411.8,163.8 411.8,162 411.7,160.2 411.4,158.3 411.1,156.3 410.6,154.3 410,152.3 409.2,150.2 408.4,148 407.4,145.8 406.3,143.6 405.1,141.3 403.7,139 402.3,136.6 400.7,134.2 399.1,131.8 397.3,129.4 395.4,127 393.4,124.5 391.3,122 389.1,119.5 386.8,117 384.5,114.5 382,112 379.4,109.5 376.8,107 374.1,104.5 371.3,102 368.4,99.5 365.5,97 362.4,94.6 359.4,92.2 356.2,89.8 353,87.4 349.8,85 346.5,82.7 343.2,80.4 339.8,78.2 336.4,76 332.9,73.8 329.4,71.7 325.9,69.7 322.4,67.7 318.9,65.7 315.3,63.8 311.8,62 308.2,60.2 304.7,58.5 301.1,56.8 297.6,55.3 294.1,53.8 290.6,52.3 287.1,50.9 283.6,49.6 280.2,48.4 276.8,47.3 273.5,46.2 270.2,45.2 267,44.3 263.8,43.5 260.6,42.8 257.6,42.1 254.5,41.6 251.6,41.1 248.7,40.7 245.9,40.4 243.2,40.2 240.6,40 238,40" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="310,112 409.1,173.2" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="315.3,103.5 333.4,74.1" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="411.2,169.8 407,176.6" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="330,72 336.8,76.3" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="415.1" y="178.2" font-size="11" fill="currentColor">σ<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = 1.618</tspan></text>
  <text x="338.4" y="69.1" font-size="11" fill="currentColor">σ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0.618</tspan></text>
  <text transform="translate(310 112) rotate(31.7)" x="12" y="-18" font-size="11" fill="currentColor">κ<tspan dy="3.5">2</tspan><tspan dy="-3.5">(J) = σ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">/σ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text transform="translate(310 112) rotate(31.7)" x="12" y="-5" font-size="11" fill="currentColor">= 2.618</text>
  <polyline points="238,184 310,184 310,112" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
  <polyline points="310,184 333.8,184" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.8"/>
  <path d="M 325 184 A 15 15 0 0 0 310 169" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="238" cy="184" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="310" cy="184" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="310" cy="112" r="3" fill="currentColor"/>
  <text x="240" y="206" font-size="11" text-anchor="end" fill="currentColor">θ<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = 0° (from +x)</tspan></text>
  <text x="316" y="206" font-size="11" fill="currentColor">θ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90° (from link 1)</tspan></text>
  <polyline points="238,184 310,112" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.8"/>
  <polyline points="310,112 320.1,101.9" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.8"/>
  <polyline points="310,112 238,40" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHw)"/>
  <polyline points="310,112 238,112" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHw)"/>
  <polyline points="314.9,107.1 310,102.1 305.1,107.1" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="303,112 303,119 310,119" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="264" y="30" font-size="11" text-anchor="middle" fill="currentColor">θ̇ = (1, 0) → (−1, 1)</text>
  <text x="232" y="118" font-size="11" text-anchor="end" fill="currentColor">θ̇ = (0, 1)</text>
  <text x="232" y="132" font-size="11" text-anchor="end" fill="currentColor">→ (−1, 0)</text>
  <text x="372" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">P2, θ = (0°, 90°)</text>
  <text x="470" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">θ = (0°, 0°)</text>
  <line x1="496" y1="58.3" x2="496" y2="165.7" stroke="currentColor" stroke-width="8" stroke-opacity="0.22"/>
  <polyline points="448,112 472,112 496,112" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="448" cy="112" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="472" cy="112" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="496,112 496,64" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHw)"/>
  <polyline points="496,112 496,88" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHw)"/>
  <circle cx="496" cy="112" r="3" fill="currentColor"/>
  <text x="505" y="69" font-size="11" fill="currentColor">(0, 2)</text>
  <text x="505" y="93" font-size="11" fill="currentColor">(0, 1)</text>
  <text x="505" y="140" font-size="11" fill="currentColor">det J = 0</text>
  <text x="505" y="154" font-size="11" fill="currentColor">κ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = ∞</tspan></text>
  <text x="496" y="206" font-size="11" text-anchor="middle" fill="currentColor">lost direction: x</text>
  <text x="470" y="38" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">⅓ scale</text>
  <polyline points="404,80 428,80" fill="none" stroke="currentColor" stroke-width="1" marker-end="url(#laHw)"/>
  <polyline points="404,80 404,56" fill="none" stroke="currentColor" stroke-width="1" marker-end="url(#laHw)"/>
  <text x="431" y="84" font-size="11" fill="currentColor">ẋ</text>
  <text x="409" y="60" font-size="11" fill="currentColor">ẏ</text>
  <text x="388" y="96" font-size="10.5" opacity="0.85" fill="currentColor">tip velocity</text>
</svg>

Plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]] at its frozen pose $\theta=(0^\circ,90^\circ)$, drawn as what §1 means by "a matrix is a map" (§4.5 works this pose as its P2 case): the columns of $J$ are the tip velocities for one unit of each joint rate, $(-1,1)$ for the whole arm turning about the base and $(-1,0)$ for the forearm turning about the elbow, each perpendicular to its own joint-to-tip segment. Under $J$ the unit circle of joint rates becomes an ellipse in the plane of tip velocities $(\dot x,\dot y)$, drawn centred on the tip at the circle's scale, with semi-axes $\sigma_1=1.618$ and $\sigma_2=0.618$, so $\kappa_2(J)=2.618$, and its area $\pi\sigma_1\sigma_2=\pi\lvert\det J\rvert=\pi$ is the circle's own because $\det J=1$. In the right panel, drawn at a third of that scale, the arm is straight, $\theta=(0^\circ,0^\circ)$: the columns $(0,2)$ and $(0,1)$ are parallel, the ellipse has collapsed to a segment of half-length $\sqrt5=2.236$ with $\det J=0$ and $\kappa_2=\infty$, and the lost direction is $x$.

### 1. Vectors, matrices, and what multiplication means

A robot arm and a neural-network layer do the same thing to a list of numbers: P2's Jacobian takes two joint rates and returns the tip's velocity, and a layer takes features and returns features. Before either can be analysed you need to know what a matrix does to a vector and two ways to read the product; P2 then puts numbers on both readings.

- A matrix $W \in \mathbb{R}^{m\times n}$ is a **linear map** $\mathbb{R}^n \to \mathbb{R}^m$:
  it satisfies $W(ax + by) = aWx + bWy$, which is additivity and homogeneity at once (the
  complete definition, with non-examples, is [[02-foundations/engineering-math|0.5 §4.5]]).
  The converse also holds: every linear map $\mathbb{R}^n \to \mathbb{R}^m$ is a matrix, whose
  column $j$ is the image of the unit vector $e_j$, since any $x = \sum_j x_j e_j$ is then sent
  to $\sum_j x_j W e_j$. For $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$, $We_1 = (1,3)$ is the
  first column. Non-example: $x \mapsto Wx + b$ with $b \ne 0$ is affine, not linear, because it
  sends $0$ to $b$. Every linear layer (strictly, its $W$) and every embedding lookup is one, and
  so are the attention projections of the second collapsed box at the end of this section.
- Two readings of $y = Wx$:
  - **Row picture**: $y_i = \langle w_{i,:}, x\rangle$ — each output is a dot-product
    similarity between the input and a learned pattern (row).
  - **Column picture**: $y = \sum_j x_j\, w_{:,j}$ — the output is a mix of learned
    directions (columns) weighted by the input.
  - **Both readings, on P2.** At the picture's pose, $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$ sends joint rates $\dot\theta$ in rad/s to the tip velocity $v=J\dot\theta$ in m/s. By columns: column $j$ is the tip velocity for one unit of joint $j$ alone, $(-1,1)$ for the base and $(-1,0)$ for the elbow, so turning both at once, $\dot\theta=(1,1)$, gives $1\cdot(-1,1)+1\cdot(-1,0)=(-2,1)$. By rows, one output at a time: $v_x=-\dot\theta_1-\dot\theta_2=-2$ and $v_y=\dot\theta_1=1$. The same answer to two questions — what one joint does, and what one output collects.
- Shape discipline: $(m\times n)(n\times 1) = (m \times 1)$. Reading shapes is how you read
  architectures and robots alike. P2's $J$ is $(2\times2)(2\times1)=2\times1$: two joint rates in, one planar velocity out.
  The redundant arm of §4.5 has a $2\times3$ Jacobian, so it takes three joint rates for the same two outputs, and a
  mismatch such as $(2\times3)(2\times1)$ is not a smaller answer but a bug. The same bookkeeping run on a
  transformer's attention head is the second collapsed box at the end of this section.
- **Dot product and angle**: the dot (inner) product takes two vectors of the same length and
  returns one number,
  $$\langle a,b\rangle = a^\top b = \sum_{i=1}^{n} a_i b_i = \|a\|\,\|b\|\cos\theta$$
  where $\theta$ is the angle between them; the last equality is the law of cosines, so the
  product measures how much of one vector lies along the other. Example: $a = (1,2,2)$,
  $b = (2,0,1)$ give $\langle a,b\rangle = 2 + 0 + 2 = 4$, $\|a\| = 3$, $\|b\| = \sqrt5 = 2.236$,
  so $\cos\theta = 0.596$ and $\theta = 53.4°$. Two vectors are **orthogonal** when
  $\langle a,b\rangle = 0$, like $(1,0)$ and $(0,1)$. Cosine similarity
  $= \langle a,b\rangle / (\|a\|\|b\|)$ lies in $[-1, 1]$ ($1$ same direction, $0$ orthogonal,
  $-1$ opposite; $0.596$ here) and ignores lengths — the retrieval metric of
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]].
- A **norm** $\|\cdot\|$ assigns a length to each vector. It is any function satisfying three
  axioms, for all vectors $x, y$ and scalars $c$ — positive definiteness, absolute homogeneity
  and the triangle inequality:
  $$\|x\| \ge 0 \text{ with } \|x\| = 0 \iff x = 0, \qquad \|c\,x\| = |c|\,\|x\|, \qquad \|x + y\| \le \|x\| + \|y\|$$
  so lengths behave the way distances must (no detour is shorter than the direct path).
  Norms: $\|x\|_2 = \sqrt{\sum x_i^2}$ (length, energy), $\|x\|_1 = \sum |x_i|$
  (fits penalised by it come out sparse, for the reason the first collapsed box below gives), $\|x\|_\infty = \max_i |x_i|$, and for
  matrices $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$. Example: $x = (3,-4)$ has $\|x\|_2 = 5$,
  $\|x\|_1 = 7$, $\|x\|_\infty = 4$; $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$ has
  $\|A\|_F = \sqrt{30} = 5.477$; and $u = (3,0)$, $v = (0,4)$ satisfy the triangle inequality as
  $\|u+v\|_2 = 5 \le 3 + 4$. Non-example: the so-called "$L_0$ norm", the count of nonzero
  entries, is not a norm, since doubling $x$ leaves the count unchanged instead of doubling it.

**Follow one input through the map.** Before calculating, say what each axis means. In a robot velocity map, the input entries may be joint speeds and the output entries tip-velocity components. In a neural layer, they are feature coordinates. The arithmetic is the same, but units and interpretation come from the application. A row asks which combination of inputs creates one output; a column asks what happens if only one input changes. Neither view requires imagining the whole matrix at once.

> [!question] Pause and explain · 잠깐 설명해 보기
> If you double one input coordinate while holding the others fixed, which column controls the change? The corresponding column of the matrix. It describes that input's contribution; the other columns' contributions remain unchanged. Use this test whenever a matrix looks like an opaque block of numbers.

> [!note]- Deeper · 더 깊이
> **Why the L1 norm makes fitted solutions sparse.** The unit ball of $\lVert\cdot\rVert_1$, the set $\lvert x_1\rvert+\lvert x_2\rvert\le1$, is a diamond whose corners sit on the axes at $(\pm1,0)$ and $(0,\pm1)$, while the unit ball of $\lVert\cdot\rVert_2$ is a round circle. Ask for the point of each ball nearest to $(2,\ 0.5)$: the circle gives $(2,\ 0.5)/\lVert(2,\ 0.5)\rVert_2=(0.970,\ 0.243)$, both coordinates nonzero, but the diamond gives its corner $(1,\ 0)$, the small coordinate set exactly to zero. A least-squares fit penalised by the L1 norm (the *lasso*) lands on such corners in the same way, which is why it keeps a few weights and zeroes the rest, while an L2 penalty only shrinks them all.

> [!note]- Deeper · 더 깊이
> **Reading a transformer's shapes.** One attention head, taught in full in [[03-deep-learning/foundations/attention-transformer|1.2 Attention & the Transformer]], takes $X$, the $T\times512$ matrix whose rows are the embeddings of the $T$ tokens of a sequence ($d_{model}=512$ is the width of each token's vector), and multiplies it by three learned $512\times64$ matrices: the queries $Q=XW_Q$, the keys $K=XW_K$ and the values $V=XW_V$, each $T\times64$ ($d_k=64$ is the head's width). The scores $QK^\top$ are $(T\times64)(64\times T)=T\times T$, one number per pair of tokens, and the output $\text{softmax}(QK^\top/\sqrt{64})\,V$ is $(T\times T)(T\times64)=T\times64$. Softmax turns each row of scores into probabilities ([[02-foundations/engineering-math|0.5 §10]]), and dividing by $\sqrt{d_k}=8$ keeps the scores from growing with the width ([[03-deep-learning/foundations/attention-transformer|1.2 §2]] says why). The whole [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] type-checks this way in one line.
>
> Now select one row of the score matrix: it is one query compared with every key. Softmax normalizes across those keys, and multiplying by $V$ mixes their value vectors into one output row; repeat for the other queries. That is why the scores are token-by-token while the result is token-by-feature: the operation mixes information between tokens without turning the token index into a feature coordinate. The same head worked with numbers on D2 — the deep-learning track's frozen $8\times8$ image cut into four $4\times4$ patch tokens ([[03-deep-learning/lab-objects|0. Lab Objects]]) — is in 1.2.

### 2. Linear systems, rank, column space and null space

**Separate three questions before reaching for an inverse.** Asked to solve $Ax=b$ — which joint rates give this tip velocity, which line fits these points — first ask whether the columns can produce the requested $b$ at all; if yes, whether only one input does so; and if not, what criterion chooses among approximations. These are existence, uniqueness and selection, and this section answers them in that order: the column space decides the first, the null space the second, least squares the third. A rectangular matrix is not automatically a failed problem: it may describe more measurements than unknowns, or more available controls than the task needs.

- $Ax = b$ solvable ⟺ $b \in \text{col}(A)$ — the **column space**, i.e. everything you can
  reach by scaling $A$'s columns and adding them up. ("Everything reachable from a set of
  vectors this way" is their **span**; the column space is the span of the columns.) As sets,
  $$\text{span}(v_1, \ldots, v_k) = \{c_1 v_1 + \cdots + c_k v_k : c_i \in \mathbb{R}\}, \qquad \text{col}(A) = \{Ax : x \in \mathbb{R}^n\}$$
  and the two descriptions of $\text{col}(A)$ agree because $Ax$ is exactly the combination of
  columns weighted by $x$ (§1's column picture). Example: $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$
  has $\text{col}(C)$ = the line through $(1,2)$, so $Cx = (1,2)$ is solvable and $Cx = (1,0)$
  is not.
- **Linear independence**: vectors $v_1, \ldots, v_k$ are linearly independent when the only
  combination that gives zero is the trivial one,
  $$c_1 v_1 + \cdots + c_k v_k = 0 \implies c_1 = \cdots = c_k = 0$$
  so no vector is a combination of the others and each one adds a new direction. Example:
  $(1,0,1)$ and $(0,1,1)$ are independent; adding $(1,1,2)$, their sum, makes the set dependent
  ($1\cdot v_1 + 1\cdot v_2 - 1\cdot v_3 = 0$), and the span stays a plane.

> [!note]- Deeper · 더 깊이
> **How a solver actually solves $Ax=b$: elimination and LU.** Gaussian elimination is row operations down to triangular form; LU factorization is elimination *recorded*, so that several right-hand sides cost little. Written out, $A = LU$ with $L$ lower-triangular (ones on the diagonal, the elimination multipliers below) and $U$ upper-triangular (what elimination leaves), so $Ax = b$ becomes two triangular solves, $Ly = b$ then $Ux = y$. Example: $\begin{pmatrix}2&1\\4&3\end{pmatrix} = \begin{pmatrix}1&0\\2&1\end{pmatrix}\begin{pmatrix}2&1\\0&1\end{pmatrix}$ (the multiplier is $4/2 = 2$); for $b = (3,7)$, $Ly = b$ gives $y = (3,1)$ and $Ux = y$ gives $x = (1,1)$.

- **Rank** = number of independent columns = number of independent rows = dimension of
  what the map can express, $\text{rank}(A) = \dim \text{col}(A)$, where the dimension counts
  the vectors in a largest independent set. The **null space**
  $\text{null}(A) = \{x : Ax = 0\}$ is every input the map sends to zero; it always contains
  $x = 0$, and is *nontrivial* when it contains more. The two are tied by rank–nullity, for
  $A$ with $n$ columns:
  $$\text{rank}(A) + \dim \text{null}(A) = n$$
  since every input direction is either expressed in the output or destroyed. Rank-deficient ⇒ information is destroyed
  (null space $\{x: Ax = 0\}$ is nontrivial). Example: $C$ above has rank $1$ and null space
  spanned by $(2,-1)$, dimension $1$, and $1 + 1 = 2$ ✓. The consequence for solving: if $x_0$
  solves $Ax = b$, then so does $x_0 + z$ for every $z$ in the null space, so the solution is
  unique exactly when the null space is trivial. On P2 at the stretched pose of the picture's right panel,
  $\theta=(0^\circ,0^\circ)$, the Jacobian is $J=\begin{pmatrix}0&0\\2&1\end{pmatrix}$: rank 1, its column space the vertical
  line (the tip can move only in $y$, the lost $x$ of the picture), and its null space spanned by $(1,-2)$ — turning the base at
  $+1$ rad/s and the elbow at $-2$ rad/s leaves the tip still, to first order. A structural engineer has met this object before:
  the rigid-body motions of an unsupported structure are the null space of its stiffness matrix. One bar of stiffness
  $k=400$ N/m between two nodes has $K=k\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$, rank 1, null space spanned by $(1,1)$: moving both
  nodes by 1 mm stretches nothing, $K(1,1)\,\mathrm{mm}=(0,0)$ N, so $Ku=f$ has no unique solution until a support removes that
  mode ([[02-foundations/basic-mechanics|0.6.1 Basic Mechanics §3]] has the spring itself).
- **Least squares** — the most-used derivation in applied math. Overdetermined $Ax \approx b$:
  minimize $\|Ax - b\|^2$. At the minimum the gradient ([[02-foundations/engineering-math|0.5 §1]])
  is zero, so the first job is that gradient, and it needs nothing beyond partial derivatives.
  **The gradient, derived.** *Expand.* A squared norm is a vector dotted with itself,
  $\|r\|^2 = r^\top r$, and transposes reverse products, so
  $$\|Ax-b\|^2 = (Ax-b)^\top(Ax-b) = x^\top A^\top A\,x - 2\,b^\top A x + b^\top b$$
  where the two cross terms $x^\top A^\top b$ and $b^\top A x$ merged because each is a
  $1\times1$ number and one is the other's transpose. What is left is a *quadratic form*
  $x^\top M x$ with $M = A^\top A$, a linear term $q^\top x$ with $q = -2A^\top b$, and a constant.
  *Differentiate each piece, one coordinate $x_k$ at a time.* In $q^\top x = \sum_i q_i x_i$ only
  the $i = k$ term contains $x_k$, so its partial derivative is $q_k$ and its gradient is $q$.
  The quadratic form written out is $x^\top M x = \sum_i\sum_j M_{ij}x_ix_j$ (§3 reads it term by
  term), and $x_k$ sits in the terms with $i = k$ and in those with $j = k$ (the diagonal term
  $M_{kk}x_k^2$, which is both, gives $2M_{kk}x_k$ — one $M_{kk}x_k$ to each sum), so
  $$\frac{\partial}{\partial x_k}\,x^\top M x = \sum_j M_{kj}x_j + \sum_i M_{ik}x_i = (Mx)_k + (M^\top x)_k$$
  and its gradient is $(M + M^\top)x$, which is $2Mx$ because $M = A^\top A$ is symmetric,
  $(A^\top A)^\top = A^\top A$. The constant contributes nothing. Adding the pieces,
  $$\nabla_x \|Ax-b\|^2 = 2A^\top A\,x - 2A^\top b = 2A^\top(Ax - b)$$
  the matrix version of $\frac{d}{dx}(ax-b)^2 = 2a(ax-b)$, which is exactly what it becomes when
  every matrix is $1\times1$. It is checked on numbers in the worked example below, and
  [[02-foundations/calculus-backprop|2. Calculus §2]] reaches it again in one line through the
  chain rule. Setting it to zero:
  $$2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (the **normal equations**), unique when $A$'s columns are linearly independent, because that is exactly
  when $A^\top A$ is invertible (§4.5.1 shows why in one line). Geometrically: $A\hat{x}$ is the orthogonal projection of $b$
  onto $\text{col}(A)$, and the residual is perpendicular to it. That projection is itself a
  matrix,
  $$P = A(A^\top A)^{-1}A^\top, \qquad P^2 = P, \qquad P^\top = P$$
  where $P^2 = P$ holds since projecting twice changes nothing and $P^\top = P$ since the discarded
  part is perpendicular; in the example below $Pb = (7/6,\ 8/3,\ 25/6)$. Linear regression,
  calibration, and the Kalman filter's update all live here.
  **Worked, three points and a line.** Fit $y = c + mx$ to $(1,1), (2,3), (3,4)$ — three
  equations, two unknowns, no exact solution. Stack them:
  $A = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}$, $b = (1,3,4)$. Then
  $A^\top A = \begin{pmatrix}3&6\\6&14\end{pmatrix}$ and $A^\top b = (8, 19)$, so
  $\hat x = (c, m) = (-\tfrac13, \tfrac32)$. The residual is
  $b - A\hat x = (-\tfrac16, \tfrac13, -\tfrac16)$ — and check the geometry claim directly:
  its sum is $0$ and its dot product with $(1,2,3)$ is $-\tfrac16 + \tfrac23 - \tfrac12 = 0$.
  The residual really is perpendicular to both columns of $A$, which is exactly what
  "orthogonal projection" asserts. That check costs ten seconds and catches most sign errors.
  **Check the gradient formula on the same numbers.** Written out, the loss is
  $f(c,m) = (c+m-1)^2 + (c+2m-3)^2 + (c+3m-4)^2$. At the trial point $(c,m) = (0,1)$ the
  residuals $Ax - b$ are $(0,-1,-1)$. Differentiating $f$ term by term gives
  $\partial f/\partial c = 2(0-1-1) = -4$ and $\partial f/\partial m = 2(1\cdot0 + 2(-1) + 3(-1)) = -10$;
  the formula gives $2A^\top(0,-1,-1) = 2(-2,\,-5) = (-4,\,-10)$ ✓. At $\hat x$ it gives
  $2A^\top(\tfrac16,-\tfrac13,\tfrac16) = (0,0)$ — the residual check above, read as a gradient. The same normal equations fitted to a heater's recorded input and output, with the covariance of the estimate they return, are [[04-robotics/system-identification|5.5 System Identification §3]].
<svg viewBox="0 0 560 196" style="max-width:100%;height:auto" role="img" aria-label="a vector b above the plane spanned by the columns of A, its projection inside the plane, and the residual meeting the plane at a right angle">
  <g fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.65">
    <polygon points="40,150 232,106 344,146 152,190"/>
  </g>
  <defs><marker id="laA" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#laA)">
    <line x1="112" y1="164" x2="236" y2="58"/>
    <line x1="112" y1="164" x2="238" y2="140"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" stroke-dasharray="5 4" opacity="0.85">
    <line x1="244" y1="142" x2="244" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <polyline points="232,142 232,130 244,130"/>
  </g>
  <g fill="currentColor"><circle cx="112" cy="164" r="3.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="196" y="192" opacity="0.85">col(A) &#8212; everything A can reach</text>
    <text x="200" y="48">b (the data)</text>
    <text x="184" y="158">A x&#770; (the projection)</text>
    <text x="254" y="96">residual b &#8722; A x&#770;</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="254" y="110">&#8869; to the plane</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="376" y="40">the worked example</text>
    <text x="376" y="58">b = (1, 3, 4)</text>
    <text x="376" y="74">A x&#770; = (7/6, 8/3, 25/6)</text>
    <text x="376" y="90">residual = (&#8722;1/6, 1/3, &#8722;1/6)</text>
    <text x="388" y="108">&#183; (1,1,1) = 0</text>
    <text x="388" y="124">&#183; (1,2,3) = 0</text>
  </g>
</svg>

*The worked fit as geometry: $b=(1,3,4)$ sits above the plane $\text{col}(A)$, its projection is $A\hat x=(7/6,\ 8/3,\ 25/6)$, and the residual $(-1/6,\ 1/3,\ -1/6)$ meets the plane at a right angle — its dot products with the columns $(1,1,1)$ and $(1,2,3)$ are both $0$. The normal equations $A^\top(b-A\hat x)=0$ say exactly this, and Pythagoras on that right angle is why every other point of the plane lies farther from $b$.*

- Low-rank structure recurs everywhere: [[01-canonical-papers/notes/1-foundations/lora|LoRA]] assumes weight
  *updates* have low intrinsic rank ($\Delta W = BA$ with $r \ll d$).

For the line-fitting example, the first column says how changing the intercept moves every prediction together; the second says how changing the slope moves predictions in proportion to their x-coordinate. The observed data do not lie in the plane of predictions those columns can generate. Least squares chooses a point in that plane. At the optimum, the remaining residual is perpendicular to both available directions, so neither an intercept nudge nor a slope nudge can reduce squared error to first order.

**Check your understanding.** A zero residual means the chosen model fits these observations exactly. It does not mean the data are noiseless, the parameters are unique, or future predictions are correct. Conversely, a nonzero residual may simply reflect measurement noise in an overdetermined problem. This is why rank and residual answer different questions.

### 3. Eigendecomposition — directions a map only stretches

Multiplying by a matrix usually turns a vector as well as stretching it, so repeated products — $A^kx$ in a system stepped in time, $k$ steps of gradient descent on a quadratic — are hard to predict entry by entry. They become easy along the directions a matrix only stretches, where it acts like a single number; this section finds those directions, then reads a matrix's difficulty (its conditioning) and its sign (definiteness) off those numbers.

- An **eigenvector** of a square matrix $A$ is a *nonzero* vector $v$ that $A$ only scales,
  and the scale factor $\lambda$ is its **eigenvalue**:
  $$Av = \lambda v, \qquad v \ne 0$$
  so along eigenvector $v$, the map is pure scaling by $\lambda$ ($v = 0$ is excluded because
  $A0 = \lambda 0$ for every $\lambda$). The eigenvalues are the roots of
  $\det(A - \lambda I) = 0$, since $(A - \lambda I)v = 0$ has a nonzero solution only when
  $A - \lambda I$ is singular. Non-example: the $90°$ rotation
  $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ turns every nonzero vector, so it has no real
  eigenvector; its eigenvalues are $\pm j$.
- **Eigendecomposition**: when $A$ has $n$ independent eigenvectors, stack them as the columns
  of $V$ and the eigenvalues on the diagonal of $\Lambda$; then $A = V\Lambda V^{-1}$. Example:
  $\begin{pmatrix}1&1\\0&2\end{pmatrix}$ has $\lambda = 1, 2$ with eigenvectors $(1,0)$ and
  $(1,1)$. Not every matrix has one: the shear $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ has
  $\lambda = 1$ twice but only the single eigenvector direction $(1,0)$.
- **Spectral theorem.** For
  symmetric $A$ ($A^\top = A$): real eigenvalues, orthogonal eigenvectors, $A = Q\Lambda Q^\top$
  with $Q$ orthogonal ($Q^\top Q = I$, §4), so $Q^{-1} = Q^\top$.
- **Worked $2\times2$, start to finish.** Take $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$.
  Eigenvalues solve $\det(A - \lambda I) = 0$:
  $$(2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0 \quad\Rightarrow\quad \lambda = 3,\ 1$$
  For $\lambda = 3$, solve $(A - 3I)v = 0$: the matrix
  $\begin{pmatrix}-1&1\\1&-1\end{pmatrix}$ says $v_1 = v_2$, so $v = (1,1)$.
  Check: $A(1,1) = (3,3) = 3(1,1)$ ✓. For $\lambda = 1$ the same steps give $v = (1,-1)$,
  and $A(1,-1) = (1,-1)$ ✓. The two eigenvectors came out perpendicular — that is the
  spectral theorem at work, not luck, and it happened because $A$ is symmetric. Normalized to
  length 1 they form $Q = \tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$, and
  $Q\,\text{diag}(3,1)\,Q^\top$ multiplies back to $A$ ✓.
  *Reading it aloud:* this matrix stretches everything along the $45°$ diagonal by $3\times$
  and leaves the anti-diagonal untouched. Every symmetric matrix is a version of that sentence.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="The unit circle and its image under A with rows (2,1) and (1,2): an ellipse with semi-axes 3 along (1,1) and 1 along (1,-1). The eigenvector (1,1)/sqrt2 is stretched to length 3 on its own line, (1,-1)/sqrt2 is unchanged, and (1,0) is sent to (2,1), turned 26.6 degrees.">
  <defs><marker id="laEg" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="10.8,140.0 289.2,140.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <polyline points="150.0,279.2 150.0,0.8" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <text x="292.2" y="144.0" font-size="11" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="156.0" y="6.8" font-size="11" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <polygon points="262.0,84.0 265.4,76.8 268.4,69.9 270.8,63.2 272.7,56.9 274.1,51.0 274.9,45.4 275.2,40.2 275.0,35.5 274.2,31.2 272.9,27.4 271.1,24.1 268.8,21.2 265.9,18.9 262.6,17.1 258.8,15.8 254.5,15.0 249.8,14.8 244.6,15.1 239.0,15.9 233.1,17.3 226.8,19.2 220.1,21.6 213.2,24.6 206.0,28.0 198.6,31.9 190.9,36.3 183.1,41.1 175.1,46.3 167.0,51.9 158.9,58.0 150.7,64.3 142.5,71.0 134.3,78.0 126.2,85.2 118.3,92.7 110.4,100.4 102.7,108.3 95.2,116.2 88.0,124.3 81.0,132.5 74.3,140.7 68.0,148.9 61.9,157.0 56.3,165.1 51.1,173.1 46.3,180.9 41.9,188.6 38.0,196.0 34.6,203.2 31.6,210.1 29.2,216.8 27.3,223.1 25.9,229.0 25.1,234.6 24.8,239.8 25.0,244.5 25.8,248.8 27.1,252.6 28.9,255.9 31.2,258.8 34.1,261.1 37.4,262.9 41.2,264.2 45.5,265.0 50.2,265.2 55.4,264.9 61.0,264.1 66.9,262.7 73.2,260.8 79.9,258.4 86.8,255.4 94.0,252.0 101.4,248.1 109.1,243.7 116.9,238.9 124.9,233.7 133.0,228.1 141.1,222.0 149.3,215.7 157.5,209.0 165.7,202.0 173.8,194.8 181.7,187.3 189.6,179.6 197.3,171.7 204.8,163.8 212.0,155.7 219.0,147.5 225.7,139.3 232.0,131.1 238.1,123.0 243.7,114.9 248.9,106.9 253.7,99.1 258.1,91.4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="206.0,140.0 205.9,136.3 205.5,132.7 204.9,129.1 204.1,125.5 203.0,122.0 201.7,118.6 200.2,115.2 198.5,112.0 196.6,108.9 194.4,105.9 192.1,103.1 189.6,100.4 186.9,97.9 184.1,95.6 181.1,93.4 178.0,91.5 174.8,89.8 171.4,88.3 168.0,87.0 164.5,85.9 160.9,85.1 157.3,84.5 153.7,84.1 150.0,84.0 146.3,84.1 142.7,84.5 139.1,85.1 135.5,85.9 132.0,87.0 128.6,88.3 125.2,89.8 122.0,91.5 118.9,93.4 115.9,95.6 113.1,97.9 110.4,100.4 107.9,103.1 105.6,105.9 103.4,108.9 101.5,112.0 99.8,115.2 98.3,118.6 97.0,122.0 95.9,125.5 95.1,129.1 94.5,132.7 94.1,136.3 94.0,140.0 94.1,143.7 94.5,147.3 95.1,150.9 95.9,154.5 97.0,158.0 98.3,161.4 99.8,164.8 101.5,168.0 103.4,171.1 105.6,174.1 107.9,176.9 110.4,179.6 113.1,182.1 115.9,184.4 118.9,186.6 122.0,188.5 125.2,190.2 128.6,191.7 132.0,193.0 135.5,194.1 139.1,194.9 142.7,195.5 146.3,195.9 150.0,196.0 153.7,195.9 157.3,195.5 160.9,194.9 164.5,194.1 168.0,193.0 171.4,191.7 174.8,190.2 178.0,188.5 181.1,186.6 184.1,184.4 186.9,182.1 189.6,179.6 192.1,176.9 194.4,174.1 196.6,171.1 198.5,168.0 200.2,164.8 201.7,161.4 203.0,158.0 204.1,154.5 204.9,150.9 205.5,147.3 205.9,143.7" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="150.0,140.0 206.0,140.0" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#laEg)"/>
  <polyline points="150.0,140.0 262.0,84.0" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEg)"/>
  <path d="M 218.0 140.0 A 68 68 0 0 0 210.8 109.6" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="222.1" y="132.6" font-size="10.5" fill="currentColor">26.6°</text>
  <polyline points="150.0,140.0 268.8,21.2" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEg)"/>
  <circle cx="189.6" cy="100.4" r="3.2" fill="currentColor"/>
  <polyline points="150.0,140.0 189.6,179.6" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEg)"/>
  <circle cx="189.6" cy="179.6" r="3.2" fill="currentColor"/>
  <text x="276.8" y="27.2" font-size="11" fill="currentColor">3v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="161.0" y="107.0" font-size="11" fill="currentColor">v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="197.6" y="193.6" font-size="11" fill="currentColor">v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> = Av<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="170.0" y="155.0" font-size="11" fill="currentColor">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="270.0" y="89.0" font-size="11" fill="currentColor">Ae<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="345" y="40" font-size="11.5" fill="currentColor">A: rows (2, 1) and (1, 2)</text>
  <text x="345" y="72" font-size="11" fill="currentColor">v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, 1)/√2 → 3v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="357" y="88" font-size="11" opacity="0.85" fill="currentColor">stretched ×3 on its own line, λ = 3</text>
  <text x="345" y="118" font-size="11" fill="currentColor">v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, −1)/√2 → v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="357" y="134" font-size="11" opacity="0.85" fill="currentColor">unchanged, λ = 1</text>
  <text x="345" y="164" font-size="11" fill="currentColor">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, 0) → (2, 1)</text>
  <text x="357" y="180" font-size="11" opacity="0.85" fill="currentColor">turned 26.6°: not an eigenvector</text>
  <text x="345" y="212" font-size="11" fill="currentColor">area: π → 3π = π · det A</text>
  <polyline points="345,240 367,240" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="373" y="244" font-size="10.5" fill="currentColor">image of the circle</text>
  <polyline points="345,258 367,258" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="373" y="262" font-size="10.5" fill="currentColor">unit circle</text>
</svg>

*The worked $A$ maps the unit circle (dashed) onto an ellipse whose axes lie along its eigenvectors: $(1,1)/\sqrt2$ comes out on its own line three times as long ($\lambda=3$), and $(1,-1)/\sqrt2$ comes out unchanged ($\lambda=1$). Every other direction turns — $(1,0)$ comes out as $(2,1)$, $26.6°$ off its line — so only along eigenvectors can $A$ be treated as a number; the area grows from $\pi$ to $3\pi$, the factor $\det A=3$.*

- Why you care, concretely:
  - **Powers**: $A^k = Q\Lambda^k Q^\top$ — long-run behavior is governed by the largest
    $|\lambda|$. Stability of $x_{t+1} = Ax_t$ ⟺ all $|\lambda_i| < 1$
    (continuous time $\dot x = Ax$: all $\text{Re}(\lambda_i) < 0$).
  - **Optimization landscapes**: for quadratic loss $\frac12 x^\top H x$ ($H$ = the **Hessian**,
    the matrix of second derivatives — defined properly in
    [[02-foundations/calculus-backprop|2. Calculus §1]]; here just "the curvature matrix"), gradient descent
    converges per-eigendirection at rate $(1 - \alpha\lambda_i)$. The reason takes two lines. The gradient of
    $\frac12x^\top Hx$ is $Hx$, so one step is $x \leftarrow x-\alpha Hx=(I-\alpha H)\,x$; read in the eigenvector coordinates
    $y=Q^\top x$, where $H$ becomes the diagonal $\Lambda$, that step is $y_i \leftarrow (1-\alpha\lambda_i)\,y_i$ — one number per
    direction, multiplied in at every step. So the usable step size is set by $\lambda_{max}$ (past $\alpha=2/\lambda_{max}$ that
    factor drops below $-1$ and the steep direction grows) and the slowest progress by $\lambda_{min}$. Their ratio, the
    **condition number** $\kappa=\lambda_{max}/\lambda_{min}$ of the next bullet, *is* the difficulty of the problem — and poor conditioning is one useful lens on why
    adaptive optimization ([[01-canonical-papers/notes/1-foundations/adam|Adam]]) and normalization
    ([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]) help.

    **What $\kappa$ costs you, in numbers.** Let $H = \text{diag}(10, 1)$, so
    $\lambda_{max} = 10$, $\lambda_{min} = 1$, $\kappa = 10$. Gradient descent multiplies
    coordinate $i$ by $(1 - \alpha\lambda_i)$ each step. Stability needs
    $\alpha < 2/\lambda_{max} = 0.2$, so take $\alpha = 0.18$. The steep direction then
    shrinks by $|1 - 1.8| = 0.8$ per step — fine — but the flat direction shrinks by only
    $1 - 0.18 = 0.82$ per step. Starting from $x_0 = (1,1)$, after 20 steps you are at about
    $(0.012,\ 0.019)$: the flat coordinate is what holds you back, and always will. Nor was
    $0.18$ a poor choice: the best any single $\alpha$ can do is $\alpha=2/(\lambda_{max}+\lambda_{min})=2/11=0.182$, where
    both directions shrink by the same $(\kappa-1)/(\kappa+1)=9/11=0.818$ per step. Raise $\kappa$ to 1000 and that best rate
    becomes $999/1001=0.998$, about 100 times as many steps for the same accuracy. *That* is why
    people say "the problem is ill-conditioned" rather than "the learning rate is wrong" —
    no single $\alpha$ can serve both directions, which is exactly the gap per-coordinate
    methods try to close.
<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="gradient descent bouncing across a narrow valley while creeping along its floor">
  <g stroke="currentColor" stroke-width="1" opacity="0.3" fill="none">
    <line x1="40" y1="128" x2="240" y2="128"/><line x1="138" y1="24" x2="138" y2="196"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <ellipse cx="138" cy="128" rx="19.0" ry="60.1"/>
    <ellipse cx="138" cy="128" rx="11.4" ry="36.1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" opacity="0.9">
    <polyline points="223.0,43.0 70.0,58.3 192.4,70.8 94.5,81.1 172.8,89.6 110.1,96.5 160.3,102.2 120.2,106.8 152.3,110.6"/>
  </g>
  <g fill="currentColor" opacity="0.9"><circle cx="223.0" cy="43.0" r="2.6"/><circle cx="70.0" cy="58.3" r="2.6"/><circle cx="192.4" cy="70.8" r="2.6"/><circle cx="94.5" cy="81.1" r="2.6"/><circle cx="172.8" cy="89.6" r="2.6"/><circle cx="110.1" cy="96.5" r="2.6"/><circle cx="160.3" cy="102.2" r="2.6"/><circle cx="120.2" cy="106.8" r="2.6"/><circle cx="152.3" cy="110.6" r="2.6"/></g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="230" y="36">x<tspan dy="3.5">0</tspan><tspan dy="-3.5"> = (1, 1)</tspan></text>
    <text x="256" y="120">steep direction x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="256" y="134">&#215;0.8 per step, sign flipping</text>
    <text x="256" y="158">flat direction x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="256" y="172">&#215;0.82 per step</text>
    <text x="256" y="190">after 20 steps: (0.012, 0.019)</text>
  </g>
</svg>

*Gradient descent on $\tfrac12x^\top Hx$ with $H=\text{diag}(10,1)$ and $\alpha=0.18$, just under the stability limit $0.2$, from $x_0=(1,1)$: the steep coordinate shrinks by $0.8$ a step but flips sign, so the iterates bounce across the valley, while the flat one shrinks by only $0.82$ and still holds the iterate back at step 20, at $(0.012,\ 0.019)$. Raise $\kappa$ to 1000 and the flat direction needs about 100 times as many steps — no single $\alpha$ serves both, which is what "ill-conditioned" names.*

- **Condition number**, stated completely. It is a *number attached to a matrix*, never below 1, that says how unevenly
  the matrix stretches: the ratio of its largest stretch to its smallest, because that ratio bounds how much an error can grow
  when the matrix is inverted (below),
  $$\kappa_2(A) = \frac{\sigma_{max}}{\sigma_{min}}$$
  where $\sigma_{max}$ and $\sigma_{min}$ are the largest and smallest **singular values** — the longest and shortest semi-axes of
  the ellipse the unit circle maps to, as in the picture. They are the square roots of the eigenvalues of $A^\top A$: for P2's $J$,
  $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$ has eigenvalues $2.618$ and $0.382$, so $\sigma=1.618$ and $0.618$, the picture's semi-axes (§4 says why,
  and §4.5 works it through). For a symmetric positive-definite matrix such as the
  Hessian above, the singular values are the eigenvalues, so $\kappa=\lambda_{max}/\lambda_{min}=10$ for $H=\text{diag}(10,1)$; a
  singular matrix has $\sigma_{min}=0$ and $\kappa=\infty$. Example: $\begin{pmatrix}1&2\\3&4\end{pmatrix}$ has $\sigma=5.465,\ 0.366$,
  so $\kappa_2=14.93$; P2's $J$ at the picture's pose has $\kappa_2=2.618$, and the straight arm $\infty$. Non-example: a large
  determinant does not make a matrix well conditioned — $\text{diag}(1000,1)$ has $\det=1000$ and $\kappa=1000$, while $0.01I$ has
  $\det=10^{-4}$ and $\kappa=1$. Why it matters: solving $Ax=b$ can turn a relative error in $b$ into up to $\kappa$ times that
  relative error in $x$ — for the matrix above, a 1% error in $b$ can become 14.9% in $x$ — and $\kappa$ of a Hessian is gradient
  descent's slow mode, as the numbers above showed.
- **Positive (semi-)definite**: symmetric $A$ with all $\lambda_i > 0$ ($\ge 0$);
  equivalently $x^\top A x > 0$ for all $x \ne 0$. Covariance matrices, Hessians at minima,
  and Gram/kernel matrices are PSD — "PSD" in a paper means "behaves like a squared quantity."
  A structural engineer already trusts one: the stiffness matrix $K$ of a supported structure is positive definite, because
  $\tfrac12u^\top Ku$ is the strain energy a displacement $u$ stores — the matrix form of a spring's $\tfrac12k\delta^2$
  ([[02-foundations/basic-mechanics|0.6.1 §6]]) — and it is positive for every nonzero $u$ once the supports have removed the
  rigid-body motions. The unsupported bar of §2 has $u^\top Ku=k(u_1-u_2)^2$: never negative, but zero along $(1,1)$, so only
  semidefinite.
- **Reading $x^\top A x$ — it really is $ax^2$ with more indices.** The transposes are
  bookkeeping, not content. $x$ is a column ($n\times1$), so $x^\top$ is $1\times n$, and
  $(1\times n)(n\times n)(n\times 1) = 1\times 1$: you need an $x$ on *each* side or the
  answer would not be a number. Expand the product and every term is a coefficient times two coordinates:
  $$x^\top A x = \sum_i\sum_j A_{ij}\,x_i x_j$$
  — which is exactly what "quadratic" means. In one dimension it collapses to $a x^2$, as you would hope.
  - *Diagonal $A$ = independent parabolas.* $A = \begin{pmatrix}2&0\\0&3\end{pmatrix}$ gives
    $x^\top A x = 2x_1^2 + 3x_2^2$ — a bowl, steeper along $x_2$.
  - *Off-diagonal entries are the cross-terms that tilt it.*
    $A = \begin{pmatrix}1&1\\1&1\end{pmatrix}$ gives
    $x_1^2 + 2x_1x_2 + x_2^2 = (x_1+x_2)^2$ — still never negative, but flat along the whole
    line $x_1 = -x_2$, where it is exactly zero. That is *semi*-definite: a valley with a
    flat floor rather than a single lowest point.
  - *Not PSD looks like this.* $A = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$ gives
    $x_1^2 - x_2^2$, which is $+1$ at $x=(1,0)$ and $-1$ at $x=(0,1)$ — up one way, down the
    other. A saddle, not a bowl.
- **Why the two definitions are the same statement.** Substitute $A = Q\Lambda Q^\top$ and
  let $y = Q^\top x$ (just $x$ read in the eigenvector coordinate system):
  $$x^\top A x = x^\top Q\Lambda Q^\top x = y^\top \Lambda y = \sum_i \lambda_i\, y_i^2$$
  A weighted sum of squares, with the eigenvalues as the weights. Squares are never negative,
  so the whole thing is $\ge 0$ for every $x$ **exactly when** every $\lambda_i \ge 0$. The
  eigenvalue test and the $x^\top A x$ test are one fact seen twice.
- **Where you will actually meet it.** Two places, and both make the abstraction concrete:
  - *Taylor's second-order term* ([[02-foundations/engineering-math|0.5 §2]]) is
    $\tfrac12\,\delta^\top H \delta$ — the curvature you feel when stepping $\delta$ away
    from a point. At a stationary point, $H \succ 0$ is sufficient for a strict local
    minimum; $H \succeq 0$ is necessary but not sufficient. For example,
    $f(x,y)=x^4-y^4$ has zero gradient and the zero (hence PSD) Hessian at the origin, but
    the origin is a saddle. See [[02-foundations/optimization|4. Optimization §3]].
  - *Variance of any linear readout*: for a random vector $x$ with covariance $\Sigma$,
    $\text{Var}(w^\top x) = w^\top \Sigma w$. A variance cannot be negative — and that,
    with no further argument, is **why every covariance matrix is PSD**. When a paper says
    "$\Sigma \succeq 0$", it is asserting nothing more exotic than that.

<svg viewBox="0 0 560 224" style="max-width:100%;height:auto" role="img" aria-label="Three quadratic forms plotted along two unit directions each, at one vertical scale: 2x1^2+3x2^2 rises along x2 (to 3) and x1 (to 2); (x1+x2)^2 rises along (1,1)/sqrt2 (to 2) and is flat along (1,-1)/sqrt2; x1^2-x2^2 rises along x1 and falls along x2.">
  <polyline points="17,120 173,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="23.0,54.0 25.4,58.3 27.8,62.5 30.2,66.5 32.6,70.4 35.0,74.2 37.4,77.8 39.8,81.2 42.2,84.5 44.6,87.7 47.0,90.7 49.4,93.5 51.8,96.2 54.2,98.8 56.6,101.2 59.0,103.5 61.4,105.6 63.8,107.6 66.2,109.4 68.6,111.1 71.0,112.7 73.4,114.1 75.8,115.3 78.2,116.4 80.6,117.4 83.0,118.2 85.4,118.8 87.8,119.3 90.2,119.7 92.6,119.9 95.0,120.0 97.4,119.9 99.8,119.7 102.2,119.3 104.6,118.8 107.0,118.2 109.4,117.4 111.8,116.4 114.2,115.3 116.6,114.1 119.0,112.7 121.4,111.1 123.8,109.4 126.2,107.6 128.6,105.6 131.0,103.5 133.4,101.2 135.8,98.8 138.2,96.2 140.6,93.5 143.0,90.7 145.4,87.7 147.8,84.5 150.2,81.2 152.6,77.8 155.0,74.2 157.4,70.4 159.8,66.5 162.2,62.5 164.6,58.3 167.0,54.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="23.0,76.0 25.4,78.9 27.8,81.7 30.2,84.4 32.6,87.0 35.0,89.4 37.4,91.8 39.8,94.1 42.2,96.3 44.6,98.4 47.0,100.4 49.4,102.4 51.8,104.2 54.2,105.9 56.6,107.5 59.0,109.0 61.4,110.4 63.8,111.7 66.2,113.0 68.6,114.1 71.0,115.1 73.4,116.0 75.8,116.9 78.2,117.6 80.6,118.2 83.0,118.8 85.4,119.2 87.8,119.6 90.2,119.8 92.6,120.0 95.0,120.0 97.4,120.0 99.8,119.8 102.2,119.6 104.6,119.2 107.0,118.8 109.4,118.2 111.8,117.6 114.2,116.9 116.6,116.0 119.0,115.1 121.4,114.1 123.8,113.0 126.2,111.7 128.6,110.4 131.0,109.0 133.4,107.5 135.8,105.9 138.2,104.2 140.6,102.4 143.0,100.4 145.4,98.4 147.8,96.3 150.2,94.1 152.6,91.8 155.0,89.4 157.4,87.0 159.8,84.4 162.2,81.7 164.6,78.9 167.0,76.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="95" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">positive definite</text>
  <text x="95" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">2x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan>² + 3x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>²</text>
  <text x="95" y="172" font-size="11" text-anchor="middle" fill="currentColor">up in every direction</text>
  <polyline points="25,192 45,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="25,210 45,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="50" y="196" font-size="10.5" fill="currentColor">along x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="50" y="214" font-size="10.5" fill="currentColor">along x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <polyline points="202,120 358,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="208.0,76.0 210.4,78.9 212.8,81.7 215.2,84.4 217.6,87.0 220.0,89.4 222.4,91.8 224.8,94.1 227.2,96.3 229.6,98.4 232.0,100.4 234.4,102.4 236.8,104.2 239.2,105.9 241.6,107.5 244.0,109.0 246.4,110.4 248.8,111.7 251.2,113.0 253.6,114.1 256.0,115.1 258.4,116.0 260.8,116.9 263.2,117.6 265.6,118.2 268.0,118.8 270.4,119.2 272.8,119.6 275.2,119.8 277.6,120.0 280.0,120.0 282.4,120.0 284.8,119.8 287.2,119.6 289.6,119.2 292.0,118.8 294.4,118.2 296.8,117.6 299.2,116.9 301.6,116.0 304.0,115.1 306.4,114.1 308.8,113.0 311.2,111.7 313.6,110.4 316.0,109.0 318.4,107.5 320.8,105.9 323.2,104.2 325.6,102.4 328.0,100.4 330.4,98.4 332.8,96.3 335.2,94.1 337.6,91.8 340.0,89.4 342.4,87.0 344.8,84.4 347.2,81.7 349.6,78.9 352.0,76.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="208.0,120.0 210.4,120.0 212.8,120.0 215.2,120.0 217.6,120.0 220.0,120.0 222.4,120.0 224.8,120.0 227.2,120.0 229.6,120.0 232.0,120.0 234.4,120.0 236.8,120.0 239.2,120.0 241.6,120.0 244.0,120.0 246.4,120.0 248.8,120.0 251.2,120.0 253.6,120.0 256.0,120.0 258.4,120.0 260.8,120.0 263.2,120.0 265.6,120.0 268.0,120.0 270.4,120.0 272.8,120.0 275.2,120.0 277.6,120.0 280.0,120.0 282.4,120.0 284.8,120.0 287.2,120.0 289.6,120.0 292.0,120.0 294.4,120.0 296.8,120.0 299.2,120.0 301.6,120.0 304.0,120.0 306.4,120.0 308.8,120.0 311.2,120.0 313.6,120.0 316.0,120.0 318.4,120.0 320.8,120.0 323.2,120.0 325.6,120.0 328.0,120.0 330.4,120.0 332.8,120.0 335.2,120.0 337.6,120.0 340.0,120.0 342.4,120.0 344.8,120.0 347.2,120.0 349.6,120.0 352.0,120.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="280" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">positive semidefinite</text>
  <text x="280" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">(x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> + x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>)²</text>
  <text x="280" y="172" font-size="11" text-anchor="middle" fill="currentColor">up, but flat along a line</text>
  <polyline points="210,192 230,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="210,210 230,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="235" y="196" font-size="10.5" fill="currentColor">along (1, 1)/√2</text>
  <text x="235" y="214" font-size="10.5" fill="currentColor">along (1, −1)/√2</text>
  <polyline points="387,120 543,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="393.0,98.0 395.4,99.4 397.8,100.8 400.2,102.2 402.6,103.5 405.0,104.7 407.4,105.9 409.8,107.1 412.2,108.2 414.6,109.2 417.0,110.2 419.4,111.2 421.8,112.1 424.2,112.9 426.6,113.7 429.0,114.5 431.4,115.2 433.8,115.9 436.2,116.5 438.6,117.0 441.0,117.6 443.4,118.0 445.8,118.4 448.2,118.8 450.6,119.1 453.0,119.4 455.4,119.6 457.8,119.8 460.2,119.9 462.6,120.0 465.0,120.0 467.4,120.0 469.8,119.9 472.2,119.8 474.6,119.6 477.0,119.4 479.4,119.1 481.8,118.8 484.2,118.4 486.6,118.0 489.0,117.6 491.4,117.0 493.8,116.5 496.2,115.9 498.6,115.2 501.0,114.5 503.4,113.7 505.8,112.9 508.2,112.1 510.6,111.2 513.0,110.2 515.4,109.2 517.8,108.2 520.2,107.1 522.6,105.9 525.0,104.7 527.4,103.5 529.8,102.2 532.2,100.8 534.6,99.4 537.0,98.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="393.0,142.0 395.4,140.6 397.8,139.2 400.2,137.8 402.6,136.5 405.0,135.3 407.4,134.1 409.8,132.9 412.2,131.8 414.6,130.8 417.0,129.8 419.4,128.8 421.8,127.9 424.2,127.1 426.6,126.3 429.0,125.5 431.4,124.8 433.8,124.1 436.2,123.5 438.6,123.0 441.0,122.4 443.4,122.0 445.8,121.6 448.2,121.2 450.6,120.9 453.0,120.6 455.4,120.4 457.8,120.2 460.2,120.1 462.6,120.0 465.0,120.0 467.4,120.0 469.8,120.1 472.2,120.2 474.6,120.4 477.0,120.6 479.4,120.9 481.8,121.2 484.2,121.6 486.6,122.0 489.0,122.4 491.4,123.0 493.8,123.5 496.2,124.1 498.6,124.8 501.0,125.5 503.4,126.3 505.8,127.1 508.2,127.9 510.6,128.8 513.0,129.8 515.4,130.8 517.8,131.8 520.2,132.9 522.6,134.1 525.0,135.3 527.4,136.5 529.8,137.8 532.2,139.2 534.6,140.6 537.0,142.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="465" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">indefinite</text>
  <text x="465" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan>² − x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>²</text>
  <text x="465" y="172" font-size="11" text-anchor="middle" fill="currentColor">one way up, one way down</text>
  <polyline points="395,192 415,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="395,210 415,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="420" y="196" font-size="10.5" fill="currentColor">along x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="420" y="214" font-size="10.5" fill="currentColor">along x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
</svg>

*Each panel plots $x^\top Ax$ along two unit directions through the origin, from $-1$ to $1$, at one vertical scale: the bowl $2x_1^2+3x_2^2$ rises along both axes (to $3$ and $2$), the valley $(x_1+x_2)^2$ rises along $(1,1)/\sqrt2$ (to $2$) but stays at $0$ along $(1,-1)/\sqrt2$, and the saddle $x_1^2-x_2^2$ rises along $x_1$ and falls along $x_2$. Positive semidefinite means no direction ever dips below the axis.*

### 4. SVD — a universal factorization, available for every matrix

Eigenvectors need a square matrix, and even a square one may have none that are real: P2's $J$ has eigenvalues $(-1\pm j\sqrt3)/2$, and the redundant arm of §4.5 is not square at all. The SVD gives *every* matrix one pair of perpendicular frames in which it only stretches, and its stretch factors, the singular values, say at once how near the matrix is to losing a direction.

*The first pass reads the first two bullets and the worked $C$ below, which say what singular values are; §3's condition number and the problem set use them. The rest of the section is second pass, for when a paper factorises something.*

- **Every** matrix (any shape, any rank): $A = U\Sigma V^\top$ with **orthogonal** $U, V$ (columns unit-length and mutually
  perpendicular, so multiplying by one is a pure rotation/reflection — it stretches nothing) and
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$. Reading: rotate (input
  basis $V$) → scale (singular values) → rotate (output basis $U$).
- **The pieces, named.** For $A \in \mathbb{R}^{m\times n}$, $U$ is $m\times m$, $\Sigma$ is
  $m\times n$ with zeros off the diagonal, and $V$ is $n\times n$. A square matrix $Q$ is
  **orthogonal** when $Q^\top Q = I$ — the same word as §1's orthogonal *vectors*, one level up:
  entry $(i,j)$ of $Q^\top Q$ is the dot product of columns $i$ and $j$, so $Q^\top Q = I$ says
  the columns are unit vectors, pairwise orthogonal in §1's sense. That is why it preserves lengths:
  $\|Qx\|^2 = x^\top Q^\top Q x = \|x\|^2$. A $30°$ rotation keeps $\|(3,4)\| = 5$; the
  non-example $\text{diag}(2,1)$ has $\text{diag}(2,1)^\top\text{diag}(2,1) = \text{diag}(4,1) \ne I$
  and stretches. Read column by column, the SVD says
  $$A v_i = \sigma_i u_i, \qquad A^\top u_i = \sigma_i v_i$$
  where the columns $v_i$ of $V$ are the **right singular vectors**, the columns $u_i$ of $U$
  the **left singular vectors**, and $\sigma_i \ge 0$ the **singular values**, so input direction
  $v_i$ goes to output direction $u_i$, stretched by $\sigma_i$.

<svg viewBox="0 0 560 150" style="max-width:100%;height:auto" role="img" aria-label="SVD as rotate, scale, rotate">
  <g transform="translate(20 0)">
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <circle cx="60" cy="75" r="38"/>
    <circle cx="205" cy="75" r="38"/>
    <ellipse cx="350" cy="75" rx="42" ry="17"/>
    <ellipse cx="475" cy="75" rx="17" ry="42" transform="rotate(-30 475 75)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.6">
    <line x1="60" y1="75" x2="87" y2="48"/><line x1="60" y1="75" x2="33" y2="48"/>
    <line x1="205" y1="75" x2="243" y2="75"/><line x1="205" y1="75" x2="205" y2="37"/>
    <line x1="350" y1="75" x2="392" y2="75"/><line x1="350" y1="75" x2="350" y2="58"/>
  </g>
  <defs><marker id="svdArrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#svdArrow)" opacity="0.8">
    <line x1="108" y1="75" x2="152" y2="75"/><line x1="253" y1="75" x2="297" y2="75"/><line x1="400" y1="75" x2="428" y2="75"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="60" y="138">unit ball</text>
    <text x="130" y="66">Vᵀ</text><text x="275" y="66">Σ</text><text x="414" y="66">U</text>
    <text x="205" y="138">rotate</text><text x="350" y="138">scale σ<tspan dy="3.5">1</tspan><tspan dy="-3.5">, σ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="475" y="138">rotate</text>
  </g>
  </g>
</svg>

*Every matrix does exactly this to a sphere: rotate, stretch along axes, rotate again. The $\sigma_i$ are the stretch factors, and a zero $\sigma_i$ is a direction the map destroys.*

- **Worked, on the singular matrix from [[02-foundations/engineering-math|0.5 §4]].** $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$.
  Compute $C^\top C = \begin{pmatrix}5&10\\10&20\end{pmatrix}$, whose eigenvalues solve
  $\lambda^2 - 25\lambda = 0$, giving $\lambda = 25, 0$. So $\sigma_1 = \sqrt{25} = 5$ and
  $\sigma_2 = 0$. Read that off: **one** nonzero singular value means rank 1, so $C$ collapses
  the plane onto a line, and $\|C\|_2 = \sigma_1 = 5$ is the most it can stretch anything. The
  direction it destroys is the right singular vector belonging to $\sigma_2 = 0$, here
  $(2,-1)/\sqrt5$ — check: $C(2,-1) = (0,0)$ ✓. That is §2's null space, found by a different
  route.
- Connections: $\sigma_i^2$ = eigenvalues of $A^\top A$; rank = number of nonzero $\sigma_i$;
  $\|A\|_2 = \sigma_1$. That last one is the definition of the **spectral norm** (the matrix
  2-norm) as the largest stretch,
  $$\|A\|_2 = \max_{x \ne 0} \frac{\|Ax\|_2}{\|x\|_2} = \sigma_1$$
  since the best input is $v_1$. For $C$ above, the input $(1,2)$ becomes $(5,10)$, stretched by
  exactly $5$.
- **Eckart–Young**: the best rank-$k$ approximation (in $\|\cdot\|_F$ or $\|\cdot\|_2$) is
  truncated SVD $A_k = \sum_{i\le k}\sigma_i u_i v_i^\top$, and its error is exactly what was
  thrown away,
  $$\|A - A_k\|_2 = \sigma_{k+1}, \qquad \|A - A_k\|_F = \sqrt{\textstyle\sum_{i>k}\sigma_i^2}$$
  so no rank-$k$ matrix can do better. Example: $A = \text{diag}(3,2,1)$ with $k = 1$ keeps
  $\text{diag}(3,0,0)$, with error $2$ in the 2-norm and $\sqrt5 = 2.236$ in Frobenius. This is the mathematical license for
  model compression and PCA. ([[01-canonical-papers/notes/1-foundations/lora|LoRA]] is related but
  different: it does not SVD-approximate a finished update — it *parameterizes* the update
  as low-rank from the start, an empirical design choice.)
- **PCA in four lines**: center data $X$; covariance $C = \frac1n X^\top X$; its top
  eigenvectors = directions of maximal variance = right singular vectors of $X$; project.
  A classical ancestor of learned representations. PCA (principal component analysis) is thus
  a linear dimensionality reduction. With $X$ holding $n$ centered samples as rows, the variance
  along a unit direction $w$ is $w^\top C w$, so the directions of maximal variance are the
  eigenvectors of $C$:
  $$C\,w_i = \lambda_i\,w_i, \qquad z = W_k^\top x$$
  where $w_i$ is the $i$-th principal direction, $\lambda_i$ the variance of the data along it,
  $W_k$ the matrix of the top $k$ directions and $z$ the $k$ new coordinates of a sample $x$; the
  share of variance kept is $\sum_{i \le k}\lambda_i / \sum_i \lambda_i$. Example: the points
  $(2,0), (0,1), (-2,0), (0,-1)$ already have mean zero, $C = \text{diag}(2,\ 0.5)$, the first
  component is $(1,0)$ with $2/2.5 = 80\%$ of the variance, and the one-number codes are
  $2, 0, -2, 0$.

**Read the multiplication from right to left.** Vᵀ first expresses an input in special input directions. Σ stretches or suppresses each of those coordinates. U then expresses the result in the output frame. The input and output spaces can have different dimensions, which is why SVD applies even when an eigenvector interpretation of A itself is unavailable.

Return to the singular example above. Its zero singular value means a component along the destroyed direction leaves no trace in the output. No inverse can recover information that never appears there. A very small nonzero singular value creates a related problem: recovering that input component requires dividing by a small number, amplifying measurement error as well as signal. This is the reason to care about conditioning before solving an inverse problem.

**Check your understanding.** When truncated SVD discards a weak direction, it accepts reconstruction error in exchange for a simpler or more stable representation. It does not prove that the discarded direction is unimportant for your task. A low-variance feature can still carry the distinction a classifier or robot needs; the matrix approximation objective and the downstream objective must be kept separate.

### 4.5 The pseudo-inverse — what $J^\dagger$ means

*Second pass, with one exception: the first pass needs only the shape table and the P2 worked case below, which the problem set uses. The rest is for the first time $J^\dagger$ appears on the robotics track.*

The symbol $A^\dagger$ appears all over the robotics track — $J^\dagger$ for inverse
kinematics, $J^\dagger$ again in operational-space control — and it is the object that
connects the SVD above to every solver in this wiki. It exists because most matrices you
meet are not square, so $A^{-1}$ is not available.

#### 4.5.1 When there is something to invert, and the two formulas

**When is there anything to invert?** $A^\top A$ is invertible exactly when $A$'s columns
are linearly independent. One line shows it: if $A^\top A x = 0$ then
$x^\top A^\top A x = \lVert Ax \rVert^2 = 0$, so $Ax = 0$, so $x = 0$ by independence.

**Two formulas, and which one you get depends on the shape.**

| Shape | Pseudo-inverse | It is a | What it computes |
|---|---|---|---|
| Tall, independent columns ($m > n$) | $A^\dagger = (A^\top A)^{-1}A^\top$ | left inverse, $A^\dagger A = I$ | the least-squares solution of an *overdetermined* system |
| Wide, independent rows ($m < n$) | $A^\dagger = A^\top (AA^\top)^{-1}$ | right inverse, $AA^\dagger = I$ | the *minimum-norm* solution of an *underdetermined* system |
| Square and invertible | both | the inverse | $A^{-1}$ — the two formulas collapse to it |

Those two rows are two different robotics situations. Tall is more measurements than
unknowns: calibration, bundle adjustment, fitting a plane to a point cloud. Wide is more
joints than task dimensions: a redundant arm, where infinitely many joint velocities produce
the tool motion you asked for and you need a rule to pick one.

#### 4.5.2 Two worked cases: a redundant arm and P2

**Worked — the minimum-norm rule, on a redundant arm.** Take a 3-link planar arm with unit
links at $\theta = (0°, 90°, 0°)$. Its Jacobian mapping joint rates to tool velocity comes from the column rule (MR ch.5) — each column is the tip velocity produced by unit rate at that joint alone — and it is
$2 \times 3$ — wide, hence redundant:

$$J = \begin{bmatrix} -2 & -2 & -1 \\ 1 & 0 & 0 \end{bmatrix}, \qquad JJ^\top = \begin{bmatrix} 9 & -2 \\ -2 & 1 \end{bmatrix}, \qquad \det JJ^\top = 5$$

The minimum-norm rule follows from minimising $\lVert\dot\theta\rVert$ subject to $J\dot\theta = v$, and the answer is the right pseudoinverse:

$$J^\dagger = J^\top (JJ^\top)^{-1} = \begin{bmatrix} 0 & 1 \\ -0.4 & -0.8 \\ -0.2 & -0.4 \end{bmatrix}$$

Ask the tool to move straight up at 1 m/s, $v = (0, 1)$. Then
$\dot\theta = J^\dagger v = (1,\, -0.8,\, -0.4)$, with $\lVert\dot\theta\rVert = 1.342$.

Now find the redundancy. $J$'s null space is spanned by $n = (0,\, 0.447,\, -0.894)$ — check
$Jn = 0$. So $\dot\theta + \alpha n$ produces **exactly the same tool velocity** for any
$\alpha$, and its norm is $\sqrt{1.8 + \alpha^2}$: at $\alpha = 1$ it is 1.673, at
$\alpha = -1$ also 1.673. Every alternative is longer. That is the whole content of
"pseudo-inverse": among the infinitely many joint motions that do the job, it returns the
shortest one, and the null space is the freedom left over — which
[[04-robotics/modern-robotics/ch06-inverse-kinematics|MR ch.6]] spends on joint limits and
obstacle avoidance.

**Worked: plant P2, the square case the problem set uses.** Catalog pose $\theta=(0^\circ,90^\circ)$ ([[02-foundations/lab-plants|0.6]]):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}.$$

Draw the columns at the tip $(1,1)$: column 1 is the tip velocity for $\dot\theta=(1,0)$, which is $(-1,1)$; column 2 is $(-1,0)$. The $2\times 2$ inverse formula with $\det J=1$ gives $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. Square and invertible, so the table's last row says $J^\dagger=J^{-1}$. Check: $J J^{-1}=I$. Its singular values come from $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$, found the way §4 found $C$'s: the eigenvalues solve $\lambda^2-3\lambda+1=0$, so $\lambda=2.618,\ 0.382$ and $\sigma=\sqrt\lambda=1.618,\ 0.618$, hence $\kappa_2(J)=1.618/0.618=2.618$ and the ellipse's area $\pi\sigma_1\sigma_2=\pi\lvert\det J\rvert=\pi$ — the picture's numbers. The problem set's Derive item runs the same steps at the other elbow of its Draw item, where the answer comes out in a surprising form. The 3-link arm above needed a pseudoinverse because it was wide; P2 does not. What P2 *does* need the SVD story for is the next sentence: send $\theta_2\to 0$ and the two columns become parallel, $\det J\to 0$, $\kappa_2(J)\to\infty$, and a sideways tip motion is lost. $J^\dagger$ then explodes in the lost direction exactly as $\Sigma^\dagger$ below predicts.

#### 4.5.3 The SVD view, singularities and damped least squares

**The SVD view, and why $J^\dagger$ explodes.** Writing $A = U\Sigma V^\top$ from §4, the
pseudo-inverse is

$$A^\dagger = V\Sigma^\dagger U^\top, \qquad \Sigma^\dagger = \operatorname{diag}(1/\sigma_1,\, \ldots,\, 1/\sigma_r,\, 0,\, \ldots)$$

— invert the nonzero singular values, leave the zeros alone. This is the definition that
works for *every* matrix, including rank-deficient ones, and the two formulas above are
special cases of it. It also explains the failure mode: near a singular configuration one
$\sigma_i \to 0$, so $1/\sigma_i \to \infty$ and the returned joint velocity grows without bound in
that one direction as the arm approaches the singularity. The arm is being asked to move in a direction it cannot move; at the singular pose itself the pseudo-inverse leaves that zero alone, so the answer jumps discontinuously when the rank actually drops.

#### 4.5.4 The Moore–Penrose definition

**The definition behind both formulas.** The (Moore–Penrose) pseudo-inverse of any
$m\times n$ matrix $A$ is the unique $n\times m$ matrix $A^\dagger$ satisfying four conditions:

$$AA^\dagger A = A, \qquad A^\dagger A A^\dagger = A^\dagger, \qquad (AA^\dagger)^\top = AA^\dagger, \qquad (A^\dagger A)^\top = A^\dagger A$$

The first two say $A^\dagger$ undoes $A$ wherever undoing is possible, and the last two say the
products $AA^\dagger$ and $A^\dagger A$ are orthogonal projections, so what cannot be undone is
discarded perpendicularly rather than arbitrarily. The SVD formula satisfies all four, which is
why it is the general definition. The $J^\dagger$ above passes all four numerically (to about
$10^{-16}$), and $J^\dagger J$ is not $I$ but the projection with rows $(1,0,0)$,
$(0, 0.8, 0.4)$, $(0, 0.4, 0.2)$: it removes exactly the null-space direction $n$, because the
arm is redundant.

The fix is to stop inverting the small singular values exactly — replace $1/\sigma$ with
$\sigma/(\sigma^2 + \lambda)$, which is bounded for every $\sigma$ and equals $1/\sigma$
when $\sigma^2 \gg \lambda$. That is **damped least squares**: instead of the exact
minimum-norm solution, it minimizes $\lVert J\dot\theta - v\rVert^2 + \lambda\lVert\dot\theta\rVert^2$,
a trade between tracking error and joint speed, whose solution is

$$J^\dagger_\lambda = J^\top (JJ^\top + \lambda I)^{-1}$$

where $\lambda > 0$ is the damping; adding $\lambda I$ keeps the matrix invertible even at a
singularity, so the inverse can never blow up. In numbers: with $\lambda = 0.01$, a healthy
$\sigma = 1$ is inverted to $0.990$ instead of $1$, but a near-singular $\sigma = 0.01$ gives
$0.990$ instead of $100$. On the arm above, the same $\lambda$ turns the command $v = (0,1)$ into
$\dot\theta = (0.982,\ -0.784,\ -0.392)$ instead of $(1,\ -0.8,\ -0.4)$ — slightly less
tracking, bounded speeds. It is the same $\lambda$
as the trust parameter you will meet on [[02-foundations/optimization|4. Optimization §3.5]] —
a forward pointer, not something this page depends on. So the chain
runs: singular values → pseudo-inverse → what happens when one of them vanishes → damping →
Levenberg–Marquardt. Four names, one idea.

### 5. The control-theory connection

*Second pass, for when you reach the control track. Nothing else on this page depends on it.*

Before a controller is built, its designer has to know whether the system settles on its own, whether the input can steer every state, and whether the sensors can see every state; each question is a matrix computation. Linear algebra *is* the language of control ([[04-robotics/index|control track]]):

#### 5.1 The state-space model and the matrix exponential

- **State-space model** $\dot{x} = Ax + Bu$, $y = Cx$: the system is a matrix; simulating
  is repeated matrix multiplication; the matrix exponential $e^{At}$ solves the unforced system exactly, and with the convolution $x(t) = e^{At}x_0 + \int_0^t e^{A(t-s)}Bu(s)\,ds$ the forced one.
  The symbols: $x \in \mathbb{R}^n$ is the **state** (the numbers that, with future inputs,
  determine the future), $u \in \mathbb{R}^m$ the input, $y \in \mathbb{R}^p$ the measured
  output, and $A$ ($n\times n$), $B$ ($n\times m$), $C$ ($p\times n$) the internal dynamics, how
  the input enters, and what the sensor sees (full treatment in
  [[04-robotics/control-theory-ce397|5. Control Theory §2]]). The **matrix exponential** is
  defined by the same power series as $e^{at}$,
  $$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$
  so that $\frac{d}{dt}e^{At} = Ae^{At}$ and $x(t) = e^{At}x_0$ solves $\dot x = Ax$. Example: a
  unit mass pushed by a force $u$, with state (position, velocity), has
  $A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$ and $B = (0, 1)$. Here $A^2 = 0$, so the series
  stops: $e^{At} = \begin{pmatrix}1&t\\0&1\end{pmatrix}$, and starting at position $0$ with
  velocity $1$, after $t = 2$ the state is $(2, 1)$.
#### 5.2 Stability

- **Stability = eigenvalues of $A$** (poles): continuous-time stable iff all
  $\text{Re}(\lambda_i) < 0$; discrete-time iff all $|\lambda_i| < 1$.
#### 5.3 Controllability and observability

- **Controllability**: which directions can the input actually push the state? One step
  of input moves you along the columns of $B$; the dynamics then rotate that reach into
  $AB$, then $A^2B$, and so on. Stack those reachable directions —
  $[B, AB, \ldots, A^{n-1}B]$ — and if together they span all $n$ dimensions
  ($\text{rank} = n$), *every* state is reachable; if they miss a direction, no input
  sequence ever drives the state there. As a test,
  $$\mathcal{C} = [\,B \;\; AB \;\; \cdots \;\; A^{n-1}B\,], \qquad \text{controllable} \iff \text{rank}\,\mathcal{C} = n$$
  where $\mathcal{C}$ is the $n \times nm$ controllability matrix; the stack stops at
  $A^{n-1}B$ because later powers add no new direction (the Cayley–Hamilton argument in
  [[04-robotics/control-theory-ce397|5. Control Theory §6]]). Example: the pushed mass above has
  $AB = (1, 0)$, so $\mathcal{C} = \begin{pmatrix}0&1\\1&0\end{pmatrix}$ with rank 2 — a force
  alone steers both position and velocity. Non-example: $A = \text{diag}(1, 2)$ with
  $B = (1, 0)$ gives $\mathcal{C} = \begin{pmatrix}1&1\\0&0\end{pmatrix}$, rank 1, so the second,
  unstable mode can never be influenced.
<svg viewBox="0 0 560 196" style="max-width:100%;height:auto" role="img" aria-label="Controllability drawn from the page's numbers. Left, the pushed mass: B = (0, 1) points along velocity, AB = (1, 0) along position, together they span the plane, rank 2. Right, A = diag(1, 2) with B = (1, 0): AB = (1, 0) lies on B's own line, so the second state direction is never reached, rank 1.">
  <defs><marker id="cArrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="70.0,138.0 166.1,138.0" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="70.0,138.0 70.0,41.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="350.0,138.0 446.1,138.0" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="350.0,138.0 350.0,41.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polygon points="70.0,138.0 132.0,138.0 132.0,76.0 70.0,76.0" fill="currentColor" fill-opacity="0.10" stroke="none"/>
  <polyline points="70.0,138.0 70.0,76.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrow)"/>
  <polyline points="70.0,138.0 132.0,138.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrow)"/>
  <text x="77.0" y="82.0" font-size="11" fill="currentColor">B = (0, 1)</text>
  <text x="128.0" y="155.0" font-size="11" fill="currentColor">AB = (1, 0)</text>
  <text x="170.1" y="142.0" font-size="11" fill="currentColor">position</text>
  <text x="64.0" y="35.9" font-size="11" fill="currentColor">velocity</text>
  <polyline points="350.0,138.0 350.0,41.9" fill="none" stroke="currentColor" stroke-width="5" stroke-opacity="0.12"/>
  <polyline points="350.0,138.0 412.0,138.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrow)"/>
  <text x="388.0" y="155.0" font-size="11" fill="currentColor">B = AB = (1, 0)</text>
  <text x="450.1" y="142.0" font-size="11" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="344.0" y="35.9" font-size="11" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="359.0" y="82.2" font-size="10.5" opacity="0.85" fill="currentColor">never reached</text>
  <text x="20.0" y="16" font-size="11" fill="currentColor">pushed mass: A has rows (0, 1), (0, 0)</text>
  <text x="300.0" y="16" font-size="11" fill="currentColor">A = diag(1, 2), B = (1, 0)</text>
  <text x="20.0" y="184" font-size="11.5" fill="currentColor">rank 2 → every state reachable</text>
  <text x="300.0" y="184" font-size="11.5" fill="currentColor">rank 1 → x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> never reachable</text>
</svg>

*Left, the pushed mass: the force enters as a change of velocity, $B=(0,1)$, and one step of the dynamics turns that into a change of position, $AB=(1,0)$; the two span the plane, rank 2. Right, $A=\text{diag}(1,2)$ with $B=(1,0)$: $AB=(1,0)$ lies on $B$'s own line, so the second, unstable mode $x_2$ is out of reach whatever you do with $u$.*

  Observability is the transpose twin — can the
  output $y$ eventually reveal every state? — with matrix $[C^\top, A^\top C^\top, \ldots]$.
  Stacked the usual way,
  $$\mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix}, \qquad \text{observable} \iff \text{rank}\,\mathcal{O} = n$$
  which is the transpose of that matrix and has the same rank, because $y, \dot y, \ddot y, \ldots$
  equal $Cx, CAx, CA^2x, \ldots$ when $u = 0$, and $x$ can be solved for exactly when this stack
  has full rank. Example: measuring the pushed mass's position, $C = (1, 0)$, gives
  $\mathcal{O} = I$, rank 2, observable. Non-example: measuring only its velocity, $C = (0, 1)$,
  gives rows $(0,1)$ and $(0,0)$, rank 1 — no amount of speed data reveals where the mass
  started.
- LQR gains ([[04-robotics/lqr-lqg|6. LQR/LQG]]), Kalman filters ([[02-foundations/probability|3. Probability §5]]), and MPC ([[04-robotics/mpc|7. MPC]]) all reduce to structured matrix computations — Riccati recursions (one linear solve per step) for LQR and Kalman, and a dense QP (quadratic program: a quadratic cost under linear constraints) after MPC condensing (eliminating the states so only the inputs remain as variables, [[04-robotics/mpc|7. MPC §2]]) — numerical linear algebra is the control engineer's daily tool.

### 6. Geometry of high dimensions (paper-reading intuition)

Papers reason about 768-dimensional embeddings with intuitions built in two and three dimensions, and several of those intuitions fail there; this section says which, with numbers.

- Random zero-mean (isotropic) high-dim vectors are nearly orthogonal: $\cos\theta$ concentrates around 0 with standard deviation $1/\sqrt d$ (exactly, for Gaussian vectors) — $0.58$ at $d=3$, $0.125$ at $d=64$ (one attention head's width) and $0.036$ at $d=768$ (a common embedding width) — because the $d$ squared components of a random unit direction share a total of $1$ equally, so each averages $1/d$. (Its mean is already 0 in any dimension; vectors with a non-zero mean do not become orthogonal.) That is one reason
  dot-product retrieval over millions of embeddings is *possible*: unrelated items score
  near zero. (That relevant pairs score high is a property of the *learned* embedding, not
  of geometry.)
- Distances concentrate: nearest and farthest neighbors differ by little. For two random Gaussian points the distance has a relative spread (standard deviation over mean) of $0.42$ at $d=3$ but only $0.089$ at $d=64$ and $0.026$ at $d=768$, about $1/\sqrt{2d}$, so in high dimension almost every pair sits at nearly the same distance — one reason *learned* embeddings and metrics replace raw distances on raw features. (Cosine similarity does not escape concentration: for unit vectors $\|a-b\|^2 = 2 - 2\cos\theta$, so it ranks neighbours exactly as Euclidean distance does; what it adds is ignoring vector norms.)
- Manifold hypothesis: real data occupies a low-dimensional surface inside pixel space —
  the implicit justification for latent spaces ([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]]).

> [!tip] Going deeper · 더 깊이
> This page moves fast. If it moves too fast, Boyd and Vandenberghe's free [*Introduction to Applied Linear Algebra*](https://web.stanford.edu/~boyd/vmls/) (VMLS) covers §1 and the least-squares half of §2 at a gentler pace: it builds everything from linear independence and QR, states the independent-columns assumption of least squares explicitly, and never uses the words rank, column space or null space. Strang's *Introduction to Linear Algebra* is the standard first course for the eigenvalue and SVD half. Come back here for where each idea shows up in the papers.

### Self-check

1. Why do two stacked linear layers (no nonlinearity) collapse to one? What rank can the
   composition have?
2. Derive the normal equations and explain why the residual is orthogonal to $\text{col}(A)$.
3. A discrete system $x_{t+1} = Ax_t$ has eigenvalues $0.9, 1.02$. What happens, and along
   which direction?
4. Why does [[01-canonical-papers/notes/1-foundations/lora|LoRA]] initialize $B = 0$? (What map does
   $W_0 + BA$ equal at step 0?)

> [!tip]- Answers
> 1. $W_2(W_1x) = (W_2W_1)x$ — the product *is* a single linear map, so the composition collapses. Its rank is at most $\min(\text{rank}\,W_1, \text{rank}\,W_2)$: stacking cannot create expressive power that neither factor had.
> 2. Setting $\nabla\|Ax-b\|^2 = 2A^\top(Ax-b) = 0$ gives $A^\top A\hat x = A^\top b$. The residual $r = b - A\hat x$ then satisfies $A^\top r = 0$, i.e. $r$ is orthogonal to every column of $A$ — which is exactly the statement that $A\hat x$ is the orthogonal projection of $b$ onto $\text{col}(A)$.
> 3. The component along the $0.9$ eigenvector decays; the component along the $1.02$ eigenvector grows 2% per step. The state therefore diverges, asymptotically aligned with the $1.02$ eigenvector — a single unstable mode dominates the long run no matter how small it starts.
> 4. With $B = 0$ the update is $\Delta W = BA = 0$, so $W_0 + BA = W_0$ at step 0: training starts *exactly* at the pretrained model (a no-op initialization) instead of perturbing it randomly.

### Problem set · 과제

Tier B. **P2** from [[02-foundations/lab-plants|0.6]], at its catalog pose $\theta=(0^\circ,90^\circ)$ and two other poses. This page §3 (the condition number), §4 (singular values) and §4.5. No time-stepper.

1. **Draw.** The picture above for the other elbow: the same tip $(1,1)$ reached at $\theta=(90^\circ,-90^\circ)$, with the elbow at $(0,1)$. Draw $J$'s two columns as arrows at the tip (tip velocity for each unit joint rate) and the ellipse the unit circle of joint rates maps to. What is the same as in the picture above, and what changed?
2. **Derive.** At item 1's other elbow, $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$. Compute $J^{-1}$ by the $2\times 2$ formula, then $J^\dagger$ from the square-invertible row of the §4.5 table, and confirm they match. Then find the joint rates that move the tip straight up at 1 m/s, $v=(0,1)$, and compare them with the catalog pose's.
3. **Interpret.** Straighten the arm at another base angle: hold $\theta_1=90^\circ$ and send $\theta_2\to 0$, so that the arm ends pointing straight up with its tip at $(0,2)$. What happens to the two column arrows, to $\det J$ and to $\kappa_2(J)$, and which tool motion becomes impossible? Compare with the picture's right panel.

> [!note]- How to draw it · 그리는 법
> - The arm to scale: base at the origin, a unit link straight up to the elbow at $(0,1)$, a second unit link along $+x$ to the tip at $(1,1)$, both joints marked with a circle.
> - Write the angle each joint owns: $\theta_1=90^\circ$ measured from $+x$ at the base, $\theta_2=-90^\circ$ measured at the elbow *relative to link 1* — the convention the catalog freezes, and the commonest place to go wrong.
> - Put both column arrows' tails at the tip, not at the joints: column 1 is the tip velocity for $\dot\theta=(1,0)$, the whole arm turning about the base, and column 2 the tip velocity for $\dot\theta=(0,1)$, the forearm turning about the elbow. Label each arrow with the joint rate that produced it.
> - Check that each arrow is perpendicular to the segment from its own joint to the tip — a point on a rotating body moves at right angles to its radius — which catches a wrong sign faster than redoing the algebra. Column 1's segment is the same base-to-tip line as in the picture above; column 2's is not.
> - The image of the unit circle: a radius-$1$ circle in a corner box labelled joint-rate space, and at the tip the ellipse it maps to, with the singular values of §4 as semi-axes and $\kappa_2(J)=\sigma_1/\sigma_2$ written inside; its area is $\pi\lvert\det J\rvert$.
> - Draw the picture above's ellipse faintly behind yours: the two have the same semi-axes and differ only in tilt, and $\det J$ changes sign between them.
> - For item 3, a second, smaller panel with the arm straight up, $\theta=(90^\circ,0^\circ)$: the two column arrows there, the ellipse shaded down to the segment it collapses into, and $\det J$ and $\kappa_2$ beside it.

> [!tip]- Solutions
> 1. Column 1 is still $(-1,1)$: turning the whole arm about the base moves the tip at right angles to the base-to-tip line, and the tip has not moved. Column 2 is now $(0,1)$, at right angles to the forearm, which runs from $(0,1)$ to $(1,1)$ along $+x$. So $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$ and $\det J=-1$: the same size as before with the opposite sign, the sign of $\sin\theta_2$. $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$ has eigenvalues $2.618$ and $0.382$, so the singular values are again $1.618$ and $0.618$, $\kappa_2=2.618$ and the area is $\pi$. The ellipse has the same shape and a different tilt: its long axis points along $(-0.526,\ 0.851)$, at $121.7^\circ$, against $(-0.851,\ 0.526)$, at $148.3^\circ$, in the picture above. The tip is the same, the arm is not, so the map from joint rates is not.
> 2. $\det J=(-1)(1)-(0)(1)=-1$, so $J^{-1}=\frac{1}{-1}\begin{pmatrix}1&0\\-1&-1\end{pmatrix}=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$ — the same matrix as $J$, because here $J^2=I$. Square and invertible $\Rightarrow J^\dagger=J^{-1}$. For $v=(0,1)$, $\dot\theta=J^{-1}v=(0,1)$: only the elbow turns, because the forearm lies along $+x$ and its tip moves straight up. At the catalog pose the same $v$ needs $\begin{pmatrix}0&1\\-1&-1\end{pmatrix}(0,1)=(1,-1)$: base forward, elbow back. Same tip, same requested velocity, different joint rates — the map depends on the arm, not only on where the tip is.
> 3. Along the way $\det J=\sin\theta_2$ shrinks ($0.5$ at $30^\circ$, $0.017$ at $1^\circ$) and $\kappa_2$ grows ($9.4$, then $286$). At $\theta=(90^\circ,0^\circ)$, $J=\begin{pmatrix}-2&-1\\0&0\end{pmatrix}$: both columns lie along $-x$, so they are parallel, $\det J=0$ and $\kappa_2=\infty$ (the singular values are $\sqrt5$ and $0$). The lost direction is $y$, along the arm: a stretched arm cannot move its tip along its own length at finite joint speed, whichever way it points. The picture's right panel, with the arm along $+x$, lost $x$ for the same reason.

## 한국어

*[[02-foundations/engineering-math|0.5]]와 [[02-foundations/neural-network-basics|0.8]] 위에 선다. 핵심 삼각형의 첫 꼭짓점이다: 행렬은 랭크와 고윳값과 SVD(특이값 분해)를 가진
사상이다. 이 페이지를 선수로 지목하는 뒤 페이지에는 미적분, 확률, 최적화, SE(3), 매니퓰레이터 동역학이 있다.*

딥러닝은 행렬곱 사이에 비선형성을 끼운 선형대수 *그 자체*다. 이 페이지는 교재 수준의
서술이다: 정의, 유도, 계산 예시, 그리고 각 개념이 이 위키의 논문들 어디에서 나타나는지.

> [!note] 왜 배우는가 · Why this matters
> [[physical-ai-map|피지컬 AI 지도]]에서 선형대수는 [[07-research-program/index|7. 연구 프로그램 §5]]의 피지컬 AI 스택을 받치는 수학 바닥의 일부로, 모션 계획·조작·접촉 바로 아래에 놓인다. "*저 패널을 프레임에 설치해*"에서 로봇이 미지수보다 많은 측정으로 패널과 프레임의 위치를 정하는 일(§2의 최소제곱)과 부재를 옮기는 일이 여기에 기대는데, 이 페이지 그림의 야코비안 $J$가 관절 속도를 패널의 속도로 바꾸기 때문이다. 팔을 거의 다 편 자세에서는 $J$의 랭크가 떨어져 $J^{-1}$이 한없이 빠른 관절 속도를 요구하므로 역기구학 루프가 프레임 쪽으로 튀어 나가고, 이를 막는 §4.5의 감쇠 최소제곱($\lambda=0.01$이면 특이에 가까운 $1/\sigma=100$이 $0.99$가 된다)은 특이값을 읽을 줄 알아야 고를 수 있다. 학위논문 경로([[07-research-program/index|7. 연구 프로그램 §8]])에서 이 페이지를 쓰는 곳은 블록 1의 [[02-foundations/manipulator-kinematics-dynamics|10. 매니퓰레이터 기구학·동역학 §2와 §6]], 블록 2의 [[04-robotics/control-theory-ce397|5. 제어 이론 §2]]와 [[04-robotics/system-identification|5.5 시스템 식별 §3]], 블록 3의 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어 §4]], 그리고 행동 복제를 §2의 정규방정식으로 푸는 블록 7의 [[05-construction-robotics/imitating-contact|10. 접촉 모방 §2]]다. 이 페이지를 마치면 어떤 $y=Wx$든 행과 열로 읽고, 최소제곱 직선을 맞춰 잔차를 검산하고, 야코비안의 특이값으로 자세가 특이점에 얼마나 가까운지 말할 수 있다.

> [!note] 처음이라면 · First pass
> 60~90분 회차로 네 번쯤 걸린다. 셋은 읽고 하나는 푼다. **1회차:** 그림과 §1, 그리고 §2의 랭크와 영공간까지. §1에서는 행렬이 하는 일을 P2(카탈로그의 평면 2링크 팔, [[02-foundations/lab-plants|0.6 Lab Plants]]) 위에서 행과 열로 읽는다. 접힌 상자는 나중으로 미룬다. **2회차:** §2의 최소제곱을 그래디언트 유도와 직선 맞춤 계산까지 보고, 이어서 §3을 $2\times2$ 계산 예제와 그 그림, 경사 하강의 수렴 비율까지 읽는다. **3회차:** §3의 나머지(조건수 $\kappa_2$와 정부호성), §4의 처음 두 항목과 $C$ 계산(특이값이 무엇인지), §4.5의 모양별 표와 P2 계산, 그리고 §6. **4회차**에는 책을 덮고 스스로 점검 1~4를 푼 뒤 과제(그리기·유도·해석)를 한다. 과제에 필요한 조각이 정확히 이것들이다. 두 번째 읽기: §4(SVD)의 나머지는 논문이 무언가를 분해할 때, §4.5의 나머지는 로보틱스 트랙에서 $J^\dagger$를 처음 만날 때, §5는 제어 트랙에 닿았을 때 돌아오라.

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 218" style="max-width:100%;height:auto" role="img" aria-label="자세 θ = (0, 90도)의 P2: 실제 비율의 팔, 말단에 화살표로 그린 J의 두 열 (-1, 1)과 (-1, 0), 각각 자기 관절에서 말단으로 가는 선분에 수직; 관절 속도의 단위원과 그것이 옮겨 간 타원, 반축 1.618과 0.618, 조건수 2.618; 그리고 두 열이 평행하고 det J = 0인 곧게 편 팔.">
  <defs><marker id="laHwk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <rect x="10" y="32" width="160" height="160" rx="4" fill="currentColor" fill-opacity="0.04" stroke="currentColor" stroke-width="1"/>
  <text x="90" y="24" font-size="11" text-anchor="middle" fill="currentColor">관절 속도 공간 (θ̇<tspan dy="3.5">1</tspan><tspan dy="-3.5">, θ̇</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">)</tspan></text>
  <polyline points="16,112 164,112" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <polyline points="90,186 90,38" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5"/>
  <polyline points="162,112 161.9,115.8 161.6,119.5 161.1,123.3 160.4,127 159.5,130.6 158.5,134.2 157.2,137.8 155.8,141.3 154.2,144.7 152.4,148 150.4,151.2 148.2,154.3 146,157.3 143.5,160.2 140.9,162.9 138.2,165.5 135.3,168 132.3,170.2 129.2,172.4 126,174.4 122.7,176.2 119.3,177.8 115.8,179.2 112.2,180.5 108.6,181.5 105,182.4 101.3,183.1 97.5,183.6 93.8,183.9 90,184 86.2,183.9 82.5,183.6 78.7,183.1 75,182.4 71.4,181.5 67.8,180.5 64.2,179.2 60.7,177.8 57.3,176.2 54,174.4 50.8,172.4 47.7,170.2 44.7,168 41.8,165.5 39.1,162.9 36.5,160.2 34,157.3 31.8,154.3 29.6,151.2 27.6,148 25.8,144.7 24.2,141.3 22.8,137.8 21.5,134.2 20.5,130.6 19.6,127 18.9,123.3 18.4,119.5 18.1,115.8 18,112 18.1,108.2 18.4,104.5 18.9,100.7 19.6,97 20.5,93.4 21.5,89.8 22.8,86.2 24.2,82.7 25.8,79.3 27.6,76 29.6,72.8 31.8,69.7 34,66.7 36.5,63.8 39.1,61.1 41.8,58.5 44.7,56 47.7,53.8 50.8,51.6 54,49.6 57.3,47.8 60.7,46.2 64.2,44.8 67.8,43.5 71.4,42.5 75,41.6 78.7,40.9 82.5,40.4 86.2,40.1 90,40 93.8,40.1 97.5,40.4 101.3,40.9 105,41.6 108.6,42.5 112.2,43.5 115.8,44.8 119.3,46.2 122.7,47.8 126,49.6 129.2,51.6 132.3,53.8 135.3,56 138.2,58.5 140.9,61.1 143.5,63.8 146,66.7 148.2,69.7 150.4,72.8 152.4,76 154.2,79.3 155.8,82.7 157.2,86.2 158.5,89.8 159.5,93.4 160.4,97 161.1,100.7 161.6,104.5 161.9,108.2 162,112" fill="none" stroke="currentColor" stroke-width="1.5"/>
  <circle cx="162" cy="112" r="2.6" fill="currentColor"/>
  <circle cx="90" cy="40" r="2.6" fill="currentColor"/>
  <text x="156" y="106" font-size="11" text-anchor="end" fill="currentColor">(1, 0)</text>
  <text x="95" y="60" font-size="11" fill="currentColor">(0, 1)</text>
  <text x="158" y="127" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">θ̇<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="84" y="57" font-size="11" text-anchor="end" opacity="0.85" fill="currentColor">θ̇<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="56" y="148" font-size="11" text-anchor="middle" fill="currentColor">넓이 π</text>
  <polyline points="174,60 203,60" fill="none" stroke="currentColor" stroke-width="1.4" marker-end="url(#laHwk)"/>
  <text x="188.5" y="53" font-size="12" text-anchor="middle" fill="currentColor">J</text>
  <polygon points="238,40 235.5,40 233.2,40.2 230.9,40.4 228.7,40.7 226.6,41.1 224.6,41.6 222.7,42.1 220.9,42.8 219.3,43.5 217.7,44.3 216.3,45.2 214.9,46.2 213.7,47.3 212.6,48.4 211.6,49.6 210.8,50.9 210,52.3 209.4,53.8 208.9,55.3 208.6,56.8 208.3,58.5 208.2,60.2 208.2,62 208.3,63.8 208.6,65.7 208.9,67.7 209.4,69.7 210,71.7 210.8,73.8 211.6,76 212.6,78.2 213.7,80.4 214.9,82.7 216.3,85 217.7,87.4 219.3,89.8 220.9,92.2 222.7,94.6 224.6,97 226.6,99.5 228.7,102 230.9,104.5 233.2,107 235.5,109.5 238,112 240.6,114.5 243.2,117 245.9,119.5 248.7,122 251.6,124.5 254.5,127 257.6,129.4 260.6,131.8 263.8,134.2 267,136.6 270.2,139 273.5,141.3 276.8,143.6 280.2,145.8 283.6,148 287.1,150.2 290.6,152.3 294.1,154.3 297.6,156.3 301.1,158.3 304.7,160.2 308.2,162 311.8,163.8 315.3,165.5 318.9,167.2 322.4,168.7 325.9,170.2 329.4,171.7 332.9,173.1 336.4,174.4 339.8,175.6 343.2,176.7 346.5,177.8 349.8,178.8 353,179.7 356.2,180.5 359.4,181.2 362.4,181.9 365.5,182.4 368.4,182.9 371.3,183.3 374.1,183.6 376.8,183.8 379.4,184 382,184 384.5,184 386.8,183.8 389.1,183.6 391.3,183.3 393.4,182.9 395.4,182.4 397.3,181.9 399.1,181.2 400.7,180.5 402.3,179.7 403.7,178.8 405.1,177.8 406.3,176.7 407.4,175.6 408.4,174.4 409.2,173.1 410,171.7 410.6,170.2 411.1,168.7 411.4,167.2 411.7,165.5 411.8,163.8 411.8,162 411.7,160.2 411.4,158.3 411.1,156.3 410.6,154.3 410,152.3 409.2,150.2 408.4,148 407.4,145.8 406.3,143.6 405.1,141.3 403.7,139 402.3,136.6 400.7,134.2 399.1,131.8 397.3,129.4 395.4,127 393.4,124.5 391.3,122 389.1,119.5 386.8,117 384.5,114.5 382,112 379.4,109.5 376.8,107 374.1,104.5 371.3,102 368.4,99.5 365.5,97 362.4,94.6 359.4,92.2 356.2,89.8 353,87.4 349.8,85 346.5,82.7 343.2,80.4 339.8,78.2 336.4,76 332.9,73.8 329.4,71.7 325.9,69.7 322.4,67.7 318.9,65.7 315.3,63.8 311.8,62 308.2,60.2 304.7,58.5 301.1,56.8 297.6,55.3 294.1,53.8 290.6,52.3 287.1,50.9 283.6,49.6 280.2,48.4 276.8,47.3 273.5,46.2 270.2,45.2 267,44.3 263.8,43.5 260.6,42.8 257.6,42.1 254.5,41.6 251.6,41.1 248.7,40.7 245.9,40.4 243.2,40.2 240.6,40 238,40" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="310,112 409.1,173.2" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="315.3,103.5 333.4,74.1" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="411.2,169.8 407,176.6" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="330,72 336.8,76.3" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="415.1" y="178.2" font-size="11" fill="currentColor">σ<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = 1.618</tspan></text>
  <text x="338.4" y="69.1" font-size="11" fill="currentColor">σ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 0.618</tspan></text>
  <text transform="translate(310 112) rotate(31.7)" x="12" y="-18" font-size="11" fill="currentColor">κ<tspan dy="3.5">2</tspan><tspan dy="-3.5">(J) = σ</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">/σ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text transform="translate(310 112) rotate(31.7)" x="12" y="-5" font-size="11" fill="currentColor">= 2.618</text>
  <polyline points="238,184 310,184 310,112" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
  <polyline points="310,184 333.8,184" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="3 3" stroke-opacity="0.8"/>
  <path d="M 325 184 A 15 15 0 0 0 310 169" fill="none" stroke="currentColor" stroke-width="1.1"/>
  <circle cx="238" cy="184" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="310" cy="184" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="310" cy="112" r="3" fill="currentColor"/>
  <text x="240" y="206" font-size="11" text-anchor="end" fill="currentColor">θ<tspan dy="3.5">1</tspan><tspan dy="-3.5"> = 0° (+x에서)</tspan></text>
  <text x="316" y="206" font-size="11" fill="currentColor">θ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = 90° (링크 1 기준)</tspan></text>
  <polyline points="238,184 310,112" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.8"/>
  <polyline points="310,112 320.1,101.9" fill="none" stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" stroke-opacity="0.8"/>
  <polyline points="310,112 238,40" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHwk)"/>
  <polyline points="310,112 238,112" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHwk)"/>
  <polyline points="314.9,107.1 310,102.1 305.1,107.1" fill="none" stroke="currentColor" stroke-width="1"/>
  <polyline points="303,112 303,119 310,119" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="264" y="30" font-size="11" text-anchor="middle" fill="currentColor">θ̇ = (1, 0) → (−1, 1)</text>
  <text x="232" y="118" font-size="11" text-anchor="end" fill="currentColor">θ̇ = (0, 1)</text>
  <text x="232" y="132" font-size="11" text-anchor="end" fill="currentColor">→ (−1, 0)</text>
  <text x="372" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">P2, θ = (0°, 90°)</text>
  <text x="470" y="24" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">θ = (0°, 0°)</text>
  <line x1="496" y1="58.3" x2="496" y2="165.7" stroke="currentColor" stroke-width="8" stroke-opacity="0.22"/>
  <polyline points="448,112 472,112 496,112" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/>
  <circle cx="448" cy="112" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <circle cx="472" cy="112" r="5" fill="currentColor" fill-opacity="0.15" stroke="currentColor" stroke-width="1.4"/>
  <polyline points="496,112 496,64" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHwk)"/>
  <polyline points="496,112 496,88" fill="none" stroke="currentColor" stroke-width="1.9" marker-end="url(#laHwk)"/>
  <circle cx="496" cy="112" r="3" fill="currentColor"/>
  <text x="505" y="69" font-size="11" fill="currentColor">(0, 2)</text>
  <text x="505" y="93" font-size="11" fill="currentColor">(0, 1)</text>
  <text x="505" y="140" font-size="11" fill="currentColor">det J = 0</text>
  <text x="505" y="154" font-size="11" fill="currentColor">κ<tspan dy="3.5">2</tspan><tspan dy="-3.5"> = ∞</tspan></text>
  <text x="496" y="206" font-size="11" text-anchor="middle" fill="currentColor">사라진 방향: x</text>
  <text x="470" y="38" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">⅓ 축척</text>
  <polyline points="404,80 428,80" fill="none" stroke="currentColor" stroke-width="1" marker-end="url(#laHwk)"/>
  <polyline points="404,80 404,56" fill="none" stroke="currentColor" stroke-width="1" marker-end="url(#laHwk)"/>
  <text x="431" y="84" font-size="11" fill="currentColor">ẋ</text>
  <text x="409" y="60" font-size="11" fill="currentColor">ẏ</text>
  <text x="388" y="96" font-size="10.5" opacity="0.85" fill="currentColor">말단 속도</text>
</svg>

고정 자세 $\theta=(0^\circ,90^\circ)$의 장치 P2([[02-foundations/lab-plants|0.6 Lab Plants]])로 §1이 말하는 "행렬은 사상이다"를 그린 것으로(§4.5가 이 자세를 P2 계산으로 푼다), $J$의 두 열은 관절 속도 하나를 단위만큼 줄 때의 말단 속도, 곧 팔 전체가 베이스를 중심으로 돌 때의 $(-1,1)$과 전완이 엘보를 중심으로 돌 때의 $(-1,0)$이며 각각 자기 관절에서 말단으로 가는 선분에 수직이다. $J$는 관절 속도의 단위원을 말단 속도 $(\dot x,\dot y)$의 평면 위 타원, 곧 말단을 중심으로 원과 같은 축척으로 그린 반축 $\sigma_1=1.618$, $\sigma_2=0.618$의 타원으로 옮기므로 $\kappa_2(J)=2.618$이고, $\det J=1$이라 타원의 넓이 $\pi\sigma_1\sigma_2=\pi\lvert\det J\rvert=\pi$는 원의 넓이 그대로다. 그 축척의 3분의 1로 그린 오른쪽 칸은 곧게 편 팔 $\theta=(0^\circ,0^\circ)$로, 두 열 $(0,2)$와 $(0,1)$이 평행하고 타원이 반길이 $\sqrt5=2.236$의 선분으로 주저앉아 $\det J=0$, $\kappa_2=\infty$이며 사라진 방향은 $x$다.

### 1. 벡터, 행렬, 그리고 곱셈의 의미

로봇 팔과 신경망 층은 숫자 목록에 같은 일을 한다. P2의 야코비안은 관절 속도 둘을 받아 말단 속도를 돌려주고, 층은 특징을 받아 특징을 돌려준다. 어느 쪽이든 분석하려면 행렬이 벡터에 무엇을 하는지, 그리고 그 곱을 읽는 두 방법을 먼저 알아야 한다. 아래에서 P2가 두 읽기 모두에 숫자를 붙인다.

- 행렬 $W \in \mathbb{R}^{m\times n}$은 **선형 사상** $\mathbb{R}^n \to \mathbb{R}^m$이다:
  $W(ax + by) = aWx + bWy$를 만족한다. 가법성과 동차성을 한꺼번에 쓴 것이다(비예시까지 담은
  완전한 정의는 [[02-foundations/engineering-math|0.5 §4.5]]). 역도 성립한다. $\mathbb{R}^n \to \mathbb{R}^m$인
  모든 선형 사상은 행렬이고, 그 $j$번째 열은 단위벡터 $e_j$의 상이다. 임의의 $x = \sum_j x_j e_j$가
  $\sum_j x_j W e_j$로 가기 때문이다. $W = \begin{pmatrix}1&2\\3&4\end{pmatrix}$라면
  $We_1 = (1,3)$이 첫 열이다. 비예시: $b \ne 0$인 $x \mapsto Wx + b$는 $0$을 $b$로 보내므로
  선형이 아니라 아핀이다. 모든 선형층(엄밀히는 그 $W$)과 모든 임베딩 조회가 이것이고, 이 절 끝의
  두 번째 접힌 상자에 나오는 어텐션 투영도 그렇다.
- $y = Wx$의 두 가지 독해:
  - **행 관점**: $y_i = \langle w_{i,:}, x\rangle$ — 각 출력은 입력과 학습된 패턴(행)
    사이의 내적 유사도다.
  - **열 관점**: $y = \sum_j x_j\, w_{:,j}$ — 출력은 학습된 방향들(열)을 입력이 가중한
    혼합이다.
  - **두 읽기를 P2에서.** 그림의 자세에서 $J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}$는 rad/s 단위의 관절 속도 $\dot\theta$를 m/s 단위의 말단 속도 $v=J\dot\theta$로 보낸다. 열로 읽으면, $j$번째 열은 관절 $j$ 하나만 단위 속도로 돌릴 때의 말단 속도로 베이스는 $(-1,1)$, 엘보는 $(-1,0)$이다. 그래서 둘을 함께 $\dot\theta=(1,1)$로 돌리면 $1\cdot(-1,1)+1\cdot(-1,0)=(-2,1)$이다. 행으로 읽으면 출력을 하나씩 모은다. $v_x=-\dot\theta_1-\dot\theta_2=-2$, $v_y=\dot\theta_1=1$. 답은 같고 질문이 다르다. 관절 하나가 무엇을 하는가, 그리고 출력 하나가 무엇을 모으는가.
- 모양의 규율: $(m\times n)(n\times 1) = (m \times 1)$. 모양 읽기가 신경망 구조를 읽는 법이고 로봇을 읽는
  법이기도 하다. P2의 $J$는 $(2\times2)(2\times1)=2\times1$, 곧 관절 속도 둘이 들어가 평면 속도 하나가 나온다.
  §4.5의 여유자유도 팔은 야코비안이 $2\times3$이라 같은 출력 둘에 관절 속도 셋을 받는다. $(2\times3)(2\times1)$처럼
  모양이 어긋나면 작은 답이 나오는 것이 아니라 버그다. 같은 장부를 트랜스포머의 어텐션 헤드에 적용한 것이
  이 절 끝의 두 번째 접힌 상자다.
- **내적과 각도**: 내적은 길이가 같은 두 벡터를 받아 숫자 하나를 돌려준다.
  $$\langle a,b\rangle = a^\top b = \sum_{i=1}^{n} a_i b_i = \|a\|\,\|b\|\cos\theta$$
  $\theta$는 두 벡터 사이의 각이다. 마지막 등식은 코사인 법칙이고, 그래서 내적은 한 벡터가 다른
  벡터 방향으로 얼마나 누워 있는지를 잰다. 예: $a = (1,2,2)$, $b = (2,0,1)$이면
  $\langle a,b\rangle = 2 + 0 + 2 = 4$, $\|a\| = 3$, $\|b\| = \sqrt5 = 2.236$이므로
  $\cos\theta = 0.596$, $\theta = 53.4°$다. $\langle a,b\rangle = 0$이면 두 벡터가 **직교**한다.
  $(1,0)$과 $(0,1)$이 그렇다. 코사인 유사도 $= \langle a,b\rangle / (\|a\|\|b\|)$는 $[-1, 1]$에
  있고($1$은 같은 방향, $0$은 직교, $-1$은 반대 방향, 여기서는 $0.596$) 길이를 무시한다 —
  [[01-canonical-papers/notes/3-vlm/clip|CLIP]]의 검색 지표.
- **노름** $\|\cdot\|$은 각 벡터에 길이를 준다. 모든 벡터 $x, y$와 스칼라 $c$에 대해 세 공리
  — 양의 정부호성, 절대 동차성, 삼각 부등식 — 를 만족하는 함수면 무엇이든 노름이다.
  $$\|x\| \ge 0 \text{ with } \|x\| = 0 \iff x = 0, \qquad \|c\,x\| = |c|\,\|x\|, \qquad \|x + y\| \le \|x\| + \|y\|$$
  그래서 길이가 거리처럼 행동한다(돌아가는 길이 곧은 길보다 짧을 수 없다).
  노름: $\|x\|_2 = \sqrt{\sum x_i^2}$(길이, 에너지), $\|x\|_1 = \sum |x_i|$(이것으로 벌점을 준 적합은
  희소하게 나온다. 이유는 아래 첫 번째 접힌 상자), $\|x\|_\infty = \max_i |x_i|$, 행렬에는
  $\|A\|_F = \sqrt{\sum_{ij} a_{ij}^2}$. 예: $x = (3,-4)$는 $\|x\|_2 = 5$, $\|x\|_1 = 7$,
  $\|x\|_\infty = 4$이고, $A = \begin{pmatrix}1&2\\3&4\end{pmatrix}$는
  $\|A\|_F = \sqrt{30} = 5.477$이며, $u = (3,0)$, $v = (0,4)$는 $\|u+v\|_2 = 5 \le 3 + 4$로
  삼각 부등식을 만족한다. 비예시: 0이 아닌 성분의 개수인 이른바 "$L_0$ 노름"은 노름이 아니다.
  $x$를 두 배로 해도 개수가 두 배가 되지 않고 그대로이기 때문이다.

**입력 하나를 사상 끝까지 따라간다.** 계산 전에 각 축의 뜻을 말해 본다. 로봇 속도 사상에서는 입력이 관절 속도이고 출력이 말단 속도 성분일 수 있다. 신경망 층에서는 특징 좌표다. 계산은 같지만 단위와 해석은 응용이 정한다. 행은 한 출력을 만드는 입력 조합을 묻는다. 열은 입력 하나만 바뀌면 무슨 일이 생기는지 묻는다. 행렬 전체를 한꺼번에 상상할 필요가 없다.

> [!question] 잠깐 설명해 보기 · Pause and explain
> 다른 입력을 고정하고 입력 좌표 하나를 두 배로 만들면 어느 열이 변화를 결정하는가? 그 좌표에 대응하는 열이다. 그 입력의 기여가 바뀌고 다른 열의 기여는 그대로다. 행렬이 불투명한 숫자 덩어리처럼 보이면 이 질문부터 한다.

> [!note]- 더 깊이 · Deeper
> **L1 노름이 적합을 희소하게 만드는 이유.** $\lVert\cdot\rVert_1$의 단위공, 곧 $\lvert x_1\rvert+\lvert x_2\rvert\le1$인 집합은 모서리가 축 위의 $(\pm1,0)$과 $(0,\pm1)$에 있는 마름모이고, $\lVert\cdot\rVert_2$의 단위공은 둥근 원이다. 각 공에서 $(2,\ 0.5)$에 가장 가까운 점을 찾아 보자. 원은 $(2,\ 0.5)/\lVert(2,\ 0.5)\rVert_2=(0.970,\ 0.243)$을 주어 두 좌표가 모두 0이 아니지만, 마름모는 모서리 $(1,\ 0)$을 주어 작은 좌표가 정확히 0이 된다. L1 노름으로 벌점을 준 최소제곱 적합(*라소*, lasso)도 같은 식으로 이런 모서리에 내려앉기 때문에 가중치 몇 개만 남기고 나머지를 0으로 만들고, L2 벌점은 모두를 조금씩 줄이기만 한다.

> [!note]- 더 깊이 · Deeper
> **트랜스포머의 모양 읽기.** 어텐션 헤드 하나([[03-deep-learning/foundations/attention-transformer|1.2 어텐션과 Transformer]]가 전부 가르친다)는 $X$, 곧 시퀀스의 토큰 $T$개의 임베딩을 행으로 쌓은 $T\times512$ 행렬($d_{model}=512$는 토큰 벡터 하나의 폭)을 받아, 학습된 $512\times64$ 행렬 셋을 곱한다. 쿼리 $Q=XW_Q$, 키 $K=XW_K$, 값 $V=XW_V$이고 각각 $T\times64$다($d_k=64$는 헤드의 폭). 점수 $QK^\top$는 $(T\times64)(64\times T)=T\times T$로 토큰 쌍마다 숫자 하나이고, 출력 $\text{softmax}(QK^\top/\sqrt{64})\,V$는 $(T\times T)(T\times64)=T\times64$다. softmax는 점수의 각 행을 확률로 바꾸고([[02-foundations/engineering-math|0.5 §10]]), $\sqrt{d_k}=8$로 나누는 것은 폭이 커져도 점수가 따라 커지지 않게 하려는 것이다(이유는 [[03-deep-learning/foundations/attention-transformer|1.2 §2]]). [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Transformer]] 전체가 이렇게 한 줄로 타입 검사된다.
>
> 이제 점수 행렬의 행 하나를 고른다. 한 쿼리를 모든 키와 비교한 값이다. softmax는 그 키들에 걸쳐 정규화하고, $V$를 곱하면 그 키들의 값 벡터가 섞여 출력 행 하나가 된다. 나머지 쿼리에서도 반복한다. 그래서 점수는 토큰×토큰이지만 결과는 토큰×특징이다. 토큰 사이의 정보를 섞을 뿐, 토큰 번호를 특징 좌표로 바꾸는 것이 아니다. 같은 헤드를 D2(딥러닝 트랙이 고정해 둔 $8\times8$ 영상을 $4\times4$ 패치 토큰 넷으로 자른 것, [[03-deep-learning/lab-objects|0. Lab Objects]]) 위에서 숫자로 끝까지 계산한 것이 1.2에 있다.

### 2. 선형계, 랭크, 열공간과 영공간

**역행렬을 찾기 전에 세 질문을 나눈다.** $Ax=b$를 풀라는 요청 — 어떤 관절 속도가 이 말단 속도를 내는가, 어떤 직선이 이 점들에 맞는가 — 을 받으면, 먼저 열들로 요청한 $b$를 만들 수 있는지, 만들 수 있다면 그런 입력이 하나뿐인지, 만들 수 없다면 어떤 기준으로 근사를 고를지를 묻는다. 존재성, 유일성, 선택의 문제이고, 이 절은 그 순서로 답한다. 첫째는 열공간이, 둘째는 영공간이, 셋째는 최소제곱이 정한다. 직사각 행렬이라고 문제가 실패한 것은 아니다. 미지수보다 측정이 많거나, 과제가 요구하는 것보다 제어 수단이 많을 수 있다.

- $Ax = b$가 풀린다 ⟺ $b \in \text{col}(A)$ — **열공간(column space)**, 즉 $A$의 열들을
  스칼라배해 더해서 도달할 수 있는 점 전체다. ("어떤 벡터 집합에서 이렇게 도달할 수 있는
  것 전체"를 그 집합의 **span**(생성)이라 하고, 열공간은 열들의 span이다.) 집합으로 쓰면
  $$\text{span}(v_1, \ldots, v_k) = \{c_1 v_1 + \cdots + c_k v_k : c_i \in \mathbb{R}\}, \qquad \text{col}(A) = \{Ax : x \in \mathbb{R}^n\}$$
  이고, $Ax$가 정확히 $x$로 가중한 열들의 조합이므로(§1의 열 관점) $\text{col}(A)$의 두 설명이
  일치한다. 예: $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$의 $\text{col}(C)$는 $(1,2)$를 지나는
  직선이므로 $Cx = (1,2)$는 풀리고 $Cx = (1,0)$은 풀리지 않는다.
- **일차독립**: 영벡터를 만드는 조합이 자명한 것뿐이면 벡터 $v_1, \ldots, v_k$가 일차독립이다.
  $$c_1 v_1 + \cdots + c_k v_k = 0 \implies c_1 = \cdots = c_k = 0$$
  그래서 어떤 벡터도 나머지의 조합이 아니고, 하나하나가 새 방향을 더한다. 예: $(1,0,1)$과
  $(0,1,1)$은 독립이다. 둘의 합 $(1,1,2)$를 보태면 종속이 되고
  ($1\cdot v_1 + 1\cdot v_2 - 1\cdot v_3 = 0$), span은 여전히 평면이다.

> [!note]- 더 깊이 · Deeper
> **솔버가 실제로 $Ax=b$를 푸는 법: 소거와 LU.** 가우스 소거는 삼각형 꼴이 될 때까지 행 연산을 하는 것이고, LU 분해는 소거 과정을 *기록*해 두어 우변이 여러 개여도 적은 비용으로 풀게 한 것이다. 풀어 쓰면 $A = LU$이고, $L$은 하삼각(대각선이 1, 그 아래가 소거 승수), $U$는 상삼각(소거가 남긴 것)이다. 그래서 $Ax = b$가 삼각 풀이 두 번, $Ly = b$와 $Ux = y$가 된다. 예: $\begin{pmatrix}2&1\\4&3\end{pmatrix} = \begin{pmatrix}1&0\\2&1\end{pmatrix}\begin{pmatrix}2&1\\0&1\end{pmatrix}$(승수는 $4/2 = 2$)이고, $b = (3,7)$이면 $Ly = b$에서 $y = (3,1)$, $Ux = y$에서 $x = (1,1)$이다.

- **랭크** = 독립인 열의 수 = 독립인 행의 수 = 사상이 표현할 수 있는 것의 차원,
  $\text{rank}(A) = \dim \text{col}(A)$이다. 차원은 가장 큰 독립 집합의 벡터 수다. **영공간**
  $\text{null}(A) = \{x : Ax = 0\}$은 사상이 0으로 보내는 입력 전체다. 항상 $x = 0$을 포함하고,
  그보다 많이 포함하면 *자명하지 않다*고 한다. 열이 $n$개인 $A$에서 둘은 랭크–퇴화차수 정리로
  묶인다.
  $$\text{rank}(A) + \dim \text{null}(A) = n$$
  모든 입력 방향은 출력에 표현되거나 파괴되거나 둘 중 하나이기 때문이다.
  랭크 부족 ⇒ 정보가 파괴된다 (영공간 $\{x: Ax = 0\}$이 자명하지 않다). 예: 위의 $C$는 랭크
  $1$이고 영공간은 $(2,-1)$이 생성하는 1차원이며 $1 + 1 = 2$다 ✓. 풀이에 대한 결과: $x_0$가
  $Ax = b$의 해이면 영공간의 모든 $z$에 대해 $x_0 + z$도 해이므로, 해는 영공간이 자명할 때만
  유일하다. 곧게 편 P2, 곧 그림 오른쪽 칸의 $\theta=(0^\circ,0^\circ)$에서 야코비안은 $J=\begin{pmatrix}0&0\\2&1\end{pmatrix}$이다.
  랭크 1이고, 열공간은 세로 직선(말단은 $y$ 방향으로만 움직일 수 있다. 그림에서 사라진 $x$다)이며, 영공간은 $(1,-2)$가
  생성한다. 베이스를 $+1$ rad/s, 엘보를 $-2$ rad/s로 돌리면 말단이 1차까지 그대로 있다는 뜻이다. 구조 공학자는 이
  대상을 이미 만났다. 지지되지 않은 구조물의 강체 운동이 곧 강성 행렬의 영공간이다. 두 절점 사이에 강성
  $k=400$ N/m인 봉 하나를 두면 $K=k\begin{pmatrix}1&-1\\-1&1\end{pmatrix}$이고, 랭크 1, 영공간은 $(1,1)$이 생성한다. 두 절점을
  함께 1 mm 옮기면 아무것도 늘어나지 않아 $K(1,1)\,\mathrm{mm}=(0,0)$ N이고, 지점이 그 모드를 없애기 전에는 $Ku=f$의
  해가 유일하지 않다(스프링 자체는 [[02-foundations/basic-mechanics|0.6.1 기초 역학 §3]]).
- **최소제곱** — 응용수학에서 가장 많이 쓰는 유도. 과결정 $Ax \approx b$:
  $\|Ax - b\|^2$ 최소화. 최솟점에서는 그래디언트([[02-foundations/engineering-math|0.5 §1]])가
  0이므로, 먼저 할 일은 그 그래디언트를 구하는 것이고 편미분만 있으면 된다.
  **그래디언트 유도.** *전개한다.* 노름의 제곱은 벡터를 자기 자신과 내적한 것,
  $\|r\|^2 = r^\top r$이고 전치는 곱의 순서를 뒤집으므로
  $$\|Ax-b\|^2 = (Ax-b)^\top(Ax-b) = x^\top A^\top A\,x - 2\,b^\top A x + b^\top b$$
  이다. 두 교차항 $x^\top A^\top b$와 $b^\top A x$는 각각 $1\times1$ 숫자이고 하나가 다른 하나의
  전치이므로 합쳐졌다. 남은 것은 $M = A^\top A$인 *이차형식* $x^\top M x$, $q = -2A^\top b$인
  일차항 $q^\top x$, 그리고 상수다.
  *조각마다, 좌표 $x_k$ 하나씩 미분한다.* $q^\top x = \sum_i q_i x_i$에서 $x_k$를 담은 항은
  $i = k$ 하나뿐이므로 편미분은 $q_k$, 그래디언트는 $q$다. 이차형식을 풀어 쓰면
  $x^\top M x = \sum_i\sum_j M_{ij}x_ix_j$(§3이 항별로 읽는다)이고, $x_k$는 $i = k$인 항들과
  $j = k$인 항들에 들어 있다(둘 다인 대각항 $M_{kk}x_k^2$는 $2M_{kk}x_k$를 내어 두 합에
  $M_{kk}x_k$씩 들어간다). 그래서
  $$\frac{\partial}{\partial x_k}\,x^\top M x = \sum_j M_{kj}x_j + \sum_i M_{ik}x_i = (Mx)_k + (M^\top x)_k$$
  이고 그래디언트는 $(M + M^\top)x$다. $M = A^\top A$는 $(A^\top A)^\top = A^\top A$로 대칭이므로
  이것은 $2Mx$다. 상수는 아무것도 보태지 않는다. 조각들을 더하면
  $$\nabla_x \|Ax-b\|^2 = 2A^\top A\,x - 2A^\top b = 2A^\top(Ax - b)$$
  이다. $\frac{d}{dx}(ax-b)^2 = 2a(ax-b)$의 행렬판이고, 모든 행렬이 $1\times1$이면 정확히 그것이
  된다. 아래 계산 예제에서 숫자로 검산하고,
  [[02-foundations/calculus-backprop|2. 미적분 §2]]는 연쇄 법칙 한 줄로 같은 식에 다시 닿는다.
  0으로 놓으면
  $$2A^\top(Ax - b) = 0 \;\Rightarrow\; A^\top A\, \hat{x} = A^\top b$$
  (**정규방정식**). $A$의 열이 일차독립일 때 유일하다. 정확히 그때 $A^\top A$가 가역이기 때문이다(§4.5.1이 한 줄로 보인다). 기하적으로: $A\hat{x}$는 $b$를 $\text{col}(A)$에 직교 투영한 것이고,
  잔차는 거기에 수직이다. 그 투영 자체가 행렬이다.
  $$P = A(A^\top A)^{-1}A^\top, \qquad P^2 = P, \qquad P^\top = P$$
  $P^2 = P$는 두 번 투영해도 달라지지 않는다는 뜻이고, $P^\top = P$는 버려지는 부분이 수직이라는
  뜻이다. 아래 예제에서 $Pb = (7/6,\ 8/3,\ 25/6)$이다.
  선형 회귀, 캘리브레이션, 칼만 필터의 갱신이 모두 여기 산다.
  **계산 예제 — 점 셋에 직선 하나.** $(1,1), (2,3), (3,4)$에 $y = c + mx$를 맞춰 보자 —
  식 셋, 미지수 둘, 정확한 해는 없다. 쌓으면
  $A = \begin{pmatrix}1&1\\1&2\\1&3\end{pmatrix}$, $b = (1,3,4)$. 그러면
  $A^\top A = \begin{pmatrix}3&6\\6&14\end{pmatrix}$, $A^\top b = (8, 19)$이므로
  $\hat x = (c, m) = (-\tfrac13, \tfrac32)$. 잔차는 $b - A\hat x = (-\tfrac16, \tfrac13, -\tfrac16)$이고,
  기하 주장을 직접 검산해 보라: 합이 $0$이고 $(1,2,3)$과의 내적이
  $-\tfrac16 + \tfrac23 - \tfrac12 = 0$이다. 잔차가 정말로 $A$의 두 열 모두에 수직이고,
  그것이 "직교 투영"이 주장하는 바로 그것이다. 이 검산은 10초면 되고 부호 실수의 대부분을
  잡아낸다.
  **같은 숫자로 그래디언트 공식도 검산한다.** 풀어 쓰면 손실은
  $f(c,m) = (c+m-1)^2 + (c+2m-3)^2 + (c+3m-4)^2$이다. 시험점 $(c,m) = (0,1)$에서 잔차
  $Ax - b$는 $(0,-1,-1)$이다. $f$를 항별로 미분하면 $\partial f/\partial c = 2(0-1-1) = -4$,
  $\partial f/\partial m = 2(1\cdot0 + 2(-1) + 3(-1)) = -10$이고, 공식은
  $2A^\top(0,-1,-1) = 2(-2,\,-5) = (-4,\,-10)$ ✓을 준다. $\hat x$에서는
  $2A^\top(\tfrac16,-\tfrac13,\tfrac16) = (0,0)$ — 위의 잔차 검산을 그래디언트로 읽은 것이다. 같은 정규방정식을 히터의 입출력 기록에 맞추고 추정의 공분산까지 구하는 것이 [[04-robotics/system-identification|5.5 시스템 식별 §3]]이다.
<svg viewBox="0 0 560 196" style="max-width:100%;height:auto" role="img" aria-label="A의 열들이 만드는 평면 위로 벡터 b가 떠 있고 그 투영이 평면 안에 있으며 잔차가 평면과 직각으로 만난다">
  <g fill="currentColor" fill-opacity="0.08" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.65">
    <polygon points="40,150 232,106 344,146 152,190"/>
  </g>
  <defs><marker id="laAk" markerWidth="8" markerHeight="8" refX="7" refY="3.2" orient="auto"><path d="M0,0 L8,3.2 L0,6.4 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="2" fill="none" marker-end="url(#laAk)">
    <line x1="112" y1="164" x2="236" y2="58"/>
    <line x1="112" y1="164" x2="238" y2="140"/>
  </g>
  <g stroke="currentColor" stroke-width="1.6" fill="none" stroke-dasharray="5 4" opacity="0.85">
    <line x1="244" y1="142" x2="244" y2="62"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.8">
    <polyline points="232,142 232,130 244,130"/>
  </g>
  <g fill="currentColor"><circle cx="112" cy="164" r="3.5"/></g>
  <g font-size="10.5" fill="currentColor">
    <text x="196" y="192" opacity="0.85">col(A) &#8212; A가 도달할 수 있는 전부</text>
    <text x="200" y="48">b (데이터)</text>
    <text x="184" y="158">A x&#770; (투영)</text>
    <text x="254" y="96">잔차 b &#8722; A x&#770;</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.8">
    <text x="254" y="110">평면에 &#8869;</text>
  </g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="376" y="40">예제의 숫자</text>
    <text x="376" y="58">b = (1, 3, 4)</text>
    <text x="376" y="74">A x&#770; = (7/6, 8/3, 25/6)</text>
    <text x="376" y="90">잔차 = (&#8722;1/6, 1/3, &#8722;1/6)</text>
    <text x="388" y="108">&#183; (1,1,1) = 0</text>
    <text x="388" y="124">&#183; (1,2,3) = 0</text>
  </g>
</svg>

*계산 예제를 기하로 그린 것이다. $b=(1,3,4)$가 평면 $\text{col}(A)$ 위에 떠 있고, 그 투영은 $A\hat x=(7/6,\ 8/3,\ 25/6)$이며, 잔차 $(-1/6,\ 1/3,\ -1/6)$은 평면과 직각으로 만난다. 두 열 $(1,1,1)$, $(1,2,3)$과의 내적이 모두 $0$이다. 정규방정식 $A^\top(b-A\hat x)=0$이 말하는 것이 정확히 이것이고, 그 직각에 피타고라스를 적용하면 평면 위의 다른 어떤 점도 $b$에서 더 멀다.*

- 저랭크 구조는 도처에서 반복된다: [[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 가중치
  *업데이트*의 내재 랭크가 낮다고 가정한다($r \ll d$인 $\Delta W = BA$).

직선 적합 예제의 첫 열은 절편을 바꾸면 모든 예측이 함께 움직인다는 뜻이다. 둘째 열은 기울기를 바꾸면 x좌표에 비례해 움직인다는 뜻이다. 관측 자료는 두 열이 만드는 예측의 평면 안에 없다. 최소제곱은 그 평면 위의 점을 고른다. 최적점에서는 남은 잔차가 두 방향 모두에 수직이므로 절편이나 기울기를 조금 바꿔도 제곱 오차를 일차적으로 줄이지 못한다.

**이해 확인.** 잔차가 0이면 선택한 모델이 이 관측을 정확히 맞춘다는 뜻이다. 잡음이 없거나 파라미터가 유일하거나 미래 예측이 맞는다는 뜻은 아니다. 반대로 과결정 문제의 0이 아닌 잔차는 측정 잡음 때문일 수 있다. 랭크와 잔차가 다른 질문에 답하는 이유다.

### 3. 고유분해 — 사상이 늘이기만 하는 방향

행렬을 곱하면 보통 벡터가 늘어나면서 돌기도 한다. 그래서 거듭된 곱 — 시간을 따라 전진하는 시스템의 $A^kx$, 이차 함수 위에서 경사 하강 $k$스텝 — 은 성분별로 따라가서는 예측하기 어렵다. 행렬이 늘이기만 하는 방향에서는 행렬이 숫자 하나처럼 행동하므로 쉬워진다. 이 절은 그 방향을 찾고, 그 숫자들로 행렬의 난이도(조건수)와 부호(정부호성)를 읽는다.

- 정방 행렬 $A$의 **고유벡터**는 $A$가 늘이거나 줄이기만 하는 *영이 아닌* 벡터 $v$이고, 그
  배율 $\lambda$가 **고유값**이다.
  $$Av = \lambda v, \qquad v \ne 0$$
  그래서 고유벡터 $v$ 방향에서 사상은 $\lambda$배 순수 스케일링이다(모든 $\lambda$에 대해
  $A0 = \lambda 0$이므로 $v = 0$은 뺀다). $(A - \lambda I)v = 0$이 영이 아닌 해를 가지려면
  $A - \lambda I$가 특이해야 하므로, 고유값은 $\det(A - \lambda I) = 0$의 근이다. 비예시:
  $90°$ 회전 $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$은 영이 아닌 모든 벡터를 돌려 버리므로 실수
  고유벡터가 없고, 고유값은 $\pm j$다.
- **고유분해**: $A$가 독립인 고유벡터 $n$개를 가지면 그것들을 $V$의 열로, 고유값을 $\Lambda$의
  대각선에 놓아 $A = V\Lambda V^{-1}$로 쓴다. 예: $\begin{pmatrix}1&1\\0&2\end{pmatrix}$는
  고유값 $1, 2$와 고유벡터 $(1,0)$, $(1,1)$을 가진다. 모든 행렬이 되는 것은 아니다. 층밀림
  $\begin{pmatrix}1&1\\0&1\end{pmatrix}$은 고유값 $1$이 두 번이지만 고유벡터 방향은 $(1,0)$
  하나뿐이다.
- **스펙트럼 정리.** 대칭 $A$($A^\top = A$): 실수 고유값, 직교 고유벡터, $A = Q\Lambda Q^\top$.
  $Q$는 직교행렬($Q^\top Q = I$, §4)이므로 $Q^{-1} = Q^\top$이다.
- **$2\times2$ 계산 예제, 처음부터 끝까지.** $A = \begin{pmatrix}2&1\\1&2\end{pmatrix}$를 보자.
  고유값은 $\det(A - \lambda I) = 0$을 푼다:
  $$(2-\lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = 0 \quad\Rightarrow\quad \lambda = 3,\ 1$$
  $\lambda = 3$이면 $(A - 3I)v = 0$을 푼다: 행렬
  $\begin{pmatrix}-1&1\\1&-1\end{pmatrix}$이 $v_1 = v_2$를 말하므로 $v = (1,1)$.
  검산: $A(1,1) = (3,3) = 3(1,1)$ ✓. $\lambda = 1$도 같은 절차로 $v = (1,-1)$,
  $A(1,-1) = (1,-1)$ ✓. 두 고유벡터가 서로 수직으로 나온 것은 운이 아니라 스펙트럼 정리가
  작동한 것이고, $A$가 대칭이기 때문이다. 길이 1로 정규화하면
  $Q = \tfrac{1}{\sqrt2}\begin{pmatrix}1&1\\1&-1\end{pmatrix}$이고, $Q\,\text{diag}(3,1)\,Q^\top$를
  곱하면 다시 $A$가 된다 ✓.
  *소리 내어 읽으면:* 이 행렬은 $45°$ 대각선 방향으로 모든 것을 $3$배 늘이고 반대 대각선은
  건드리지 않는다. 모든 대칭 행렬이 이 문장의 어떤 판본이다.

<svg viewBox="0 0 560 280" style="max-width:100%;height:auto" role="img" aria-label="단위원과, 행이 (2,1), (1,2)인 A가 그것을 옮긴 상: (1,1) 방향 반축 3, (1,-1) 방향 반축 1인 타원. 고유벡터 (1,1)/√2는 제 직선 위에서 길이 3으로 늘어나고, (1,-1)/√2는 그대로이며, (1,0)은 26.6도 돌아간 (2,1)로 간다.">
  <defs><marker id="laEgk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="10.8,140.0 289.2,140.0" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <polyline points="150.0,279.2 150.0,0.8" fill="none" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.45"/>
  <text x="292.2" y="144.0" font-size="11" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="156.0" y="6.8" font-size="11" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <polygon points="262.0,84.0 265.4,76.8 268.4,69.9 270.8,63.2 272.7,56.9 274.1,51.0 274.9,45.4 275.2,40.2 275.0,35.5 274.2,31.2 272.9,27.4 271.1,24.1 268.8,21.2 265.9,18.9 262.6,17.1 258.8,15.8 254.5,15.0 249.8,14.8 244.6,15.1 239.0,15.9 233.1,17.3 226.8,19.2 220.1,21.6 213.2,24.6 206.0,28.0 198.6,31.9 190.9,36.3 183.1,41.1 175.1,46.3 167.0,51.9 158.9,58.0 150.7,64.3 142.5,71.0 134.3,78.0 126.2,85.2 118.3,92.7 110.4,100.4 102.7,108.3 95.2,116.2 88.0,124.3 81.0,132.5 74.3,140.7 68.0,148.9 61.9,157.0 56.3,165.1 51.1,173.1 46.3,180.9 41.9,188.6 38.0,196.0 34.6,203.2 31.6,210.1 29.2,216.8 27.3,223.1 25.9,229.0 25.1,234.6 24.8,239.8 25.0,244.5 25.8,248.8 27.1,252.6 28.9,255.9 31.2,258.8 34.1,261.1 37.4,262.9 41.2,264.2 45.5,265.0 50.2,265.2 55.4,264.9 61.0,264.1 66.9,262.7 73.2,260.8 79.9,258.4 86.8,255.4 94.0,252.0 101.4,248.1 109.1,243.7 116.9,238.9 124.9,233.7 133.0,228.1 141.1,222.0 149.3,215.7 157.5,209.0 165.7,202.0 173.8,194.8 181.7,187.3 189.6,179.6 197.3,171.7 204.8,163.8 212.0,155.7 219.0,147.5 225.7,139.3 232.0,131.1 238.1,123.0 243.7,114.9 248.9,106.9 253.7,99.1 258.1,91.4" fill="currentColor" fill-opacity="0.06" stroke="currentColor" stroke-width="1.4"/>
  <polygon points="206.0,140.0 205.9,136.3 205.5,132.7 204.9,129.1 204.1,125.5 203.0,122.0 201.7,118.6 200.2,115.2 198.5,112.0 196.6,108.9 194.4,105.9 192.1,103.1 189.6,100.4 186.9,97.9 184.1,95.6 181.1,93.4 178.0,91.5 174.8,89.8 171.4,88.3 168.0,87.0 164.5,85.9 160.9,85.1 157.3,84.5 153.7,84.1 150.0,84.0 146.3,84.1 142.7,84.5 139.1,85.1 135.5,85.9 132.0,87.0 128.6,88.3 125.2,89.8 122.0,91.5 118.9,93.4 115.9,95.6 113.1,97.9 110.4,100.4 107.9,103.1 105.6,105.9 103.4,108.9 101.5,112.0 99.8,115.2 98.3,118.6 97.0,122.0 95.9,125.5 95.1,129.1 94.5,132.7 94.1,136.3 94.0,140.0 94.1,143.7 94.5,147.3 95.1,150.9 95.9,154.5 97.0,158.0 98.3,161.4 99.8,164.8 101.5,168.0 103.4,171.1 105.6,174.1 107.9,176.9 110.4,179.6 113.1,182.1 115.9,184.4 118.9,186.6 122.0,188.5 125.2,190.2 128.6,191.7 132.0,193.0 135.5,194.1 139.1,194.9 142.7,195.5 146.3,195.9 150.0,196.0 153.7,195.9 157.3,195.5 160.9,194.9 164.5,194.1 168.0,193.0 171.4,191.7 174.8,190.2 178.0,188.5 181.1,186.6 184.1,184.4 186.9,182.1 189.6,179.6 192.1,176.9 194.4,174.1 196.6,171.1 198.5,168.0 200.2,164.8 201.7,161.4 203.0,158.0 204.1,154.5 204.9,150.9 205.5,147.3 205.9,143.7" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <polyline points="150.0,140.0 206.0,140.0" fill="none" stroke="currentColor" stroke-width="1.3" stroke-dasharray="3 2" marker-end="url(#laEgk)"/>
  <polyline points="150.0,140.0 262.0,84.0" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEgk)"/>
  <path d="M 218.0 140.0 A 68 68 0 0 0 210.8 109.6" fill="none" stroke="currentColor" stroke-width="1"/>
  <text x="222.1" y="132.6" font-size="10.5" fill="currentColor">26.6°</text>
  <polyline points="150.0,140.0 268.8,21.2" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEgk)"/>
  <circle cx="189.6" cy="100.4" r="3.2" fill="currentColor"/>
  <polyline points="150.0,140.0 189.6,179.6" fill="none" stroke="currentColor" stroke-width="2.1" marker-end="url(#laEgk)"/>
  <circle cx="189.6" cy="179.6" r="3.2" fill="currentColor"/>
  <text x="276.8" y="27.2" font-size="11" fill="currentColor">3v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="161.0" y="107.0" font-size="11" fill="currentColor">v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="197.6" y="193.6" font-size="11" fill="currentColor">v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> = Av<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="170.0" y="155.0" font-size="11" fill="currentColor">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="270.0" y="89.0" font-size="11" fill="currentColor">Ae<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="345" y="40" font-size="11.5" fill="currentColor">A: 행 (2, 1)과 (1, 2)</text>
  <text x="345" y="72" font-size="11" fill="currentColor">v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, 1)/√2 → 3v<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="357" y="88" font-size="11" opacity="0.85" fill="currentColor">제 직선 위에서 3배로, λ = 3</text>
  <text x="345" y="118" font-size="11" fill="currentColor">v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, −1)/√2 → v<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="357" y="134" font-size="11" opacity="0.85" fill="currentColor">그대로, λ = 1</text>
  <text x="345" y="164" font-size="11" fill="currentColor">e<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> = (1, 0) → (2, 1)</text>
  <text x="357" y="180" font-size="11" opacity="0.85" fill="currentColor">26.6° 돌아감: 고유벡터가 아니다</text>
  <text x="345" y="212" font-size="11" fill="currentColor">넓이: π → 3π = π · det A</text>
  <polyline points="345,240 367,240" fill="none" stroke="currentColor" stroke-width="1.4"/>
  <text x="373" y="244" font-size="10.5" fill="currentColor">원이 옮겨 간 타원</text>
  <polyline points="345,258 367,258" fill="none" stroke="currentColor" stroke-width="1.2" stroke-dasharray="4 3"/>
  <text x="373" y="262" font-size="10.5" fill="currentColor">단위원</text>
</svg>

*계산 예제의 $A$는 단위원(점선)을 고유벡터 방향에 축을 둔 타원으로 옮긴다. $(1,1)/\sqrt2$는 제 직선 위에서 세 배 길어져 나오고($\lambda=3$), $(1,-1)/\sqrt2$는 그대로 나온다($\lambda=1$). 다른 방향은 모두 돈다. $(1,0)$은 제 직선에서 $26.6°$ 벗어난 $(2,1)$로 나오므로, $A$를 숫자 하나처럼 다룰 수 있는 것은 고유벡터 방향뿐이다. 넓이는 $\pi$에서 $3\pi$로, $\det A=3$배가 된다.*

- 구체적으로 왜 중요한가:
  - **거듭제곱**: $A^k = Q\Lambda^k Q^\top$ — 장기 거동은 가장 큰 $|\lambda|$가 지배한다.
    $x_{t+1} = Ax_t$의 안정성 ⟺ 모든 $|\lambda_i| < 1$
    (연속 시간 $\dot x = Ax$: 모든 $\text{Re}(\lambda_i) < 0$).
  - **최적화 지형**: 이차 손실 $\frac12 x^\top H x$($H$ = **헤시안**, 2차 도함수의 행렬 —
    정식 정의는 [[02-foundations/calculus-backprop|2. 미적분 §1]]; 여기서는 "곡률 행렬"로
    읽으면 된다)에서 경사 하강은 고유방향별로
    $(1 - \alpha\lambda_i)$ 비율로 수렴한다. 이유는 두 줄이다. $\frac12x^\top Hx$의 그래디언트가 $Hx$이므로 한 스텝은
    $x \leftarrow x-\alpha Hx=(I-\alpha H)\,x$이고, $H$가 대각 $\Lambda$가 되는 고유벡터 좌표 $y=Q^\top x$에서 읽으면 이 스텝은
    $y_i \leftarrow (1-\alpha\lambda_i)\,y_i$, 곧 방향마다 숫자 하나를 매 스텝 곱하는 것이다. 그래서 쓸 수 있는 스텝 크기는
    $\lambda_{max}$가 정하고($\alpha=2/\lambda_{max}$를 넘으면 그 인수가 $-1$ 아래로 내려가 가파른 방향이 커진다), 가장 느린
    진전은 $\lambda_{min}$이 정한다. 둘의 비, 곧 다음 항목에서 정의하는 **조건수** $\kappa=\lambda_{max}/\lambda_{min}$가 문제의 난이도 *그 자체*다 —
    나쁜 조건수는 적응형 최적화([[01-canonical-papers/notes/1-foundations/adam|Adam]])와
    정규화([[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]])가 왜 돕는지 이해하는
    유용한 관점 중 하나다.

    **$\kappa$가 치르게 하는 대가, 숫자로.** $H = \text{diag}(10, 1)$이면 $\lambda_{max} = 10$,
    $\lambda_{min} = 1$, $\kappa = 10$이다. 경사 하강은 매 스텝 좌표 $i$에
    $(1 - \alpha\lambda_i)$를 곱한다. 안정하려면 $\alpha < 2/\lambda_{max} = 0.2$여야 하니
    $\alpha = 0.18$로 두자. 그러면 가파른 방향은 스텝당 $|1 - 1.8| = 0.8$배로 줄어 괜찮지만,
    평평한 방향은 스텝당 $1 - 0.18 = 0.82$배밖에 줄지 않는다. $x_0 = (1,1)$에서 시작하면 20
    스텝 뒤 대략 $(0.012,\ 0.019)$ — 발목을 잡는 것은 평평한 좌표이고 앞으로도 계속 그렇다.
    $0.18$이 나쁜 선택이었던 것도 아니다. 단일 $\alpha$로 할 수 있는 최선은 $\alpha=2/(\lambda_{max}+\lambda_{min})=2/11=0.182$이고,
    거기서 두 방향이 스텝당 똑같이 $(\kappa-1)/(\kappa+1)=9/11=0.818$배로 준다. $\kappa$를 1000으로 올리면 그 최선의 비율이
    $999/1001=0.998$이 되어, 같은 정확도에 약 100배의 스텝이 필요하다. "학습률이
    잘못됐다"가 아니라 *"문제의 조건이 나쁘다"*고 말하는 이유가 이것이다 — 어떤 단일 $\alpha$도
    두 방향을 동시에 만족시킬 수 없고, 좌표별 방법들이 메우려는 격차가 정확히 이것이다.

<svg viewBox="0 0 560 200" style="max-width:100%;height:auto" role="img" aria-label="좁은 골짜기를 가로질러 튀면서 바닥을 따라 천천히 나아가는 경사 하강">
  <g stroke="currentColor" stroke-width="1" opacity="0.3" fill="none">
    <line x1="40" y1="128" x2="240" y2="128"/><line x1="138" y1="24" x2="138" y2="196"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" fill="none" opacity="0.45">
    <ellipse cx="138" cy="128" rx="19.0" ry="60.1"/>
    <ellipse cx="138" cy="128" rx="11.4" ry="36.1"/>
  </g>
  <g stroke="currentColor" stroke-width="1.7" fill="none" opacity="0.9">
    <polyline points="223.0,43.0 70.0,58.3 192.4,70.8 94.5,81.1 172.8,89.6 110.1,96.5 160.3,102.2 120.2,106.8 152.3,110.6"/>
  </g>
  <g fill="currentColor" opacity="0.9"><circle cx="223.0" cy="43.0" r="2.6"/><circle cx="70.0" cy="58.3" r="2.6"/><circle cx="192.4" cy="70.8" r="2.6"/><circle cx="94.5" cy="81.1" r="2.6"/><circle cx="172.8" cy="89.6" r="2.6"/><circle cx="110.1" cy="96.5" r="2.6"/><circle cx="160.3" cy="102.2" r="2.6"/><circle cx="120.2" cy="106.8" r="2.6"/><circle cx="152.3" cy="110.6" r="2.6"/></g>
  <g font-size="10.5" fill="currentColor" opacity="0.85">
    <text x="230" y="36">x<tspan dy="3.5">0</tspan><tspan dy="-3.5"> = (1, 1)</tspan></text>
    <text x="256" y="120">가파른 방향 x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="256" y="134">스텝당 &#215;0.8, 부호가 뒤집힌다</text>
    <text x="256" y="158">평평한 방향 x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="256" y="172">스텝당 &#215;0.82</text>
    <text x="256" y="190">20 스텝 뒤: (0.012, 0.019)</text>
  </g>
</svg>

*$H=\text{diag}(10,1)$인 $\tfrac12x^\top Hx$에서 안정 한계 $0.2$ 바로 아래인 $\alpha=0.18$로 $x_0=(1,1)$부터 내려간 경사 하강이다. 가파른 좌표는 스텝마다 $0.8$배로 줄지만 부호가 뒤집혀 반복점이 골짜기를 가로질러 튀고, 평평한 좌표는 $0.82$배밖에 줄지 않아 20스텝째 $(0.012,\ 0.019)$에서도 발목을 잡는다. $\kappa$를 1000으로 올리면 평평한 방향에 약 100배의 스텝이 필요하다. 어떤 단일 $\alpha$도 두 방향을 함께 만족시키지 못한다는 것, 그것이 "조건이 나쁘다"는 말의 뜻이다.*

- **조건수**의 완전한 정의. *행렬에 붙는 숫자*로 1보다 작아지지 않으며, 행렬이 얼마나 고르지 않게 늘이는지를
  말한다. 가장 크게 늘이는 배율과 가장 작게 늘이는 배율의 비이고, 그 비가 행렬을 뒤집을 때 오차가 얼마나
  커질 수 있는지를 묶기 때문에(아래) 이렇게 정의한다.
  $$\kappa_2(A) = \frac{\sigma_{max}}{\sigma_{min}}$$
  $\sigma_{max}$와 $\sigma_{min}$은 가장 큰 **특이값**과 가장 작은 특이값, 곧 단위원이 옮겨 간 타원의 가장 긴 반축과
  가장 짧은 반축이다(그림에서처럼). 특이값은 $A^\top A$ 고유값의 제곱근이다. P2의 $J$라면 $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$의 고유값이 $2.618$과
  $0.382$이므로 $\sigma=1.618$과 $0.618$, 곧 그림의 반축이다(이유는 §4, 끝까지 계산은 §4.5). 위의 헤시안 같은 대칭 양정부호 행렬에서는 특이값이 고유값과
  같으므로 $H=\text{diag}(10,1)$이면 $\kappa=\lambda_{max}/\lambda_{min}=10$이다. 특이 행렬은 $\sigma_{min}=0$이라
  $\kappa=\infty$다. 예: $\begin{pmatrix}1&2\\3&4\end{pmatrix}$는 $\sigma=5.465,\ 0.366$이므로 $\kappa_2=14.93$이고, 그림
  자세의 P2 $J$는 $\kappa_2=2.618$, 곧게 편 팔은 $\infty$다. 비예시: 행렬식이 크다고 조건이 좋은 것이 아니다.
  $\text{diag}(1000,1)$은 $\det=1000$이지만 $\kappa=1000$이고, $0.01I$는 $\det=10^{-4}$이지만 $\kappa=1$이다. 중요한 이유:
  $Ax=b$를 풀면 $b$의 상대 오차가 $x$에서 최대 $\kappa$배의 상대 오차가 될 수 있고 — 위의 행렬이라면 $b$의 1% 오차가
  $x$에서 14.9%가 될 수 있다 — 헤시안의 $\kappa$는 위의 숫자가 보인 대로 경사 하강의 느린 모드다.
- **양(준)정부호**: 모든 $\lambda_i > 0$($\ge 0$)인 대칭 $A$; 동치로 모든 $x \ne 0$에서
  $x^\top A x > 0$. 공분산 행렬, 최솟값에서의 헤시안, 그람/커널 행렬이 PSD다 —
  논문의 "PSD"는 "제곱량처럼 행동한다"는 뜻. 구조 공학자는 이미 하나를 믿고 있다. 지지된 구조물의 강성 행렬 $K$는
  양정부호다. $\tfrac12u^\top Ku$가 변위 $u$가 저장하는 변형 에너지, 곧 스프링의 $\tfrac12k\delta^2$를 행렬로 쓴 것이고
  ([[02-foundations/basic-mechanics|0.6.1 §6]]), 지점이 강체 운동을 없애고 나면 0이 아닌 모든 $u$에서 양수이기 때문이다.
  §2의 지지되지 않은 봉은 $u^\top Ku=k(u_1-u_2)^2$이라 음수가 되지는 않지만 $(1,1)$ 방향에서 0이므로 준정부호일 뿐이다.
- **$x^\top A x$ 읽는 법 — 정말로 인덱스가 늘어난 $ax^2$이다.** 전치는 내용이 아니라 부기다.
  $x$가 열벡터($n\times1$)이므로 $x^\top$은 $1\times n$이고,
  $(1\times n)(n\times n)(n\times 1) = 1\times 1$ — 즉 답이 숫자가 되려면 $x$가 *양쪽에*
  하나씩 있어야 한다. 곱을 전개하면 모든 항이 계수 곱하기 좌표 둘이다:
  $$x^\top A x = \sum_i\sum_j A_{ij}\,x_i x_j$$
  — 그것이 정확히 "이차"의 뜻이다. 1차원으로 줄이면
  기대대로 $a x^2$가 된다.
  - *대각 $A$ = 서로 독립인 포물선들.* $A = \begin{pmatrix}2&0\\0&3\end{pmatrix}$이면
    $x^\top A x = 2x_1^2 + 3x_2^2$ — 그릇 모양이고 $x_2$ 방향이 더 가파르다.
  - *비대각 성분이 그릇을 기울이는 교차항이다.*
    $A = \begin{pmatrix}1&1\\1&1\end{pmatrix}$이면
    $x_1^2 + 2x_1x_2 + x_2^2 = (x_1+x_2)^2$ — 여전히 음수가 되지 않지만, 직선 $x_1 = -x_2$
    전체에서 정확히 0으로 평평하다. 이것이 *준*정부호다: 최저점 하나가 아니라 바닥이 평평한
    골짜기.
  - *PSD가 아닌 경우는 이렇게 생겼다.* $A = \begin{pmatrix}1&0\\0&-1\end{pmatrix}$이면
    $x_1^2 - x_2^2$이고, $x=(1,0)$에서 $+1$, $x=(0,1)$에서 $-1$ — 한 방향은 올라가고 다른
    방향은 내려간다. 그릇이 아니라 안장이다.
- **두 정의가 왜 같은 말인가.** $A = Q\Lambda Q^\top$을 대입하고 $y = Q^\top x$로 두면
  (그저 $x$를 고유벡터 좌표계에서 읽은 것):
  $$x^\top A x = x^\top Q\Lambda Q^\top x = y^\top \Lambda y = \sum_i \lambda_i\, y_i^2$$
  고유값을 가중치로 쓴 제곱들의 가중합이다. 제곱은 결코 음수가 아니므로, 이 전체가 모든 $x$에
  대해 $\ge 0$일 **필요충분조건**이 모든 $\lambda_i \ge 0$이다. 고유값 판정과 $x^\top A x$
  판정은 하나의 사실을 두 번 본 것이다.
- **실제로 만나게 되는 자리.** 두 곳이고, 둘 다 이 추상을 구체로 만든다:
  - *테일러의 2차 항*([[02-foundations/engineering-math|0.5 §2]])이
    $\tfrac12\,\delta^\top H \delta$다 — 어떤 점에서 $\delta$만큼 움직일 때 느끼는 곡률.
    정상점에서 $H \succ 0$이면 엄격한 지역 최솟값이라는 충분조건이고, $H \succeq 0$은
    필요하지만 충분하지 않다. 예를 들어 $f(x,y)=x^4-y^4$는 원점에서 그래디언트와 헤시안이
    모두 0(따라서 PSD)이지만 원점은 안장점이다
    ([[02-foundations/optimization|4. 최적화 §3]]).
  - *임의의 선형 판독값의 분산*: 공분산이 $\Sigma$인 확률벡터 $x$에 대해
    $\text{Var}(w^\top x) = w^\top \Sigma w$. 분산은 음수가 될 수 없고 — 더 이상의 논증 없이
    이것이 **모든 공분산 행렬이 PSD인 이유**다. 논문의 "$\Sigma \succeq 0$"은 그 이상 별난
    것을 주장하지 않는다.

<svg viewBox="0 0 560 224" style="max-width:100%;height:auto" role="img" aria-label="세 이차형식을 각각 두 단위 방향을 따라 같은 세로 축척으로 그린 것: 2x1^2+3x2^2는 x2 방향(3까지)과 x1 방향(2까지)으로 오르고, (x1+x2)^2는 (1,1)/√2 방향으로 2까지 오르지만 (1,-1)/√2 방향으로는 평평하며, x1^2-x2^2는 x1 방향으로 오르고 x2 방향으로 내려간다.">
  <polyline points="17,120 173,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="23.0,54.0 25.4,58.3 27.8,62.5 30.2,66.5 32.6,70.4 35.0,74.2 37.4,77.8 39.8,81.2 42.2,84.5 44.6,87.7 47.0,90.7 49.4,93.5 51.8,96.2 54.2,98.8 56.6,101.2 59.0,103.5 61.4,105.6 63.8,107.6 66.2,109.4 68.6,111.1 71.0,112.7 73.4,114.1 75.8,115.3 78.2,116.4 80.6,117.4 83.0,118.2 85.4,118.8 87.8,119.3 90.2,119.7 92.6,119.9 95.0,120.0 97.4,119.9 99.8,119.7 102.2,119.3 104.6,118.8 107.0,118.2 109.4,117.4 111.8,116.4 114.2,115.3 116.6,114.1 119.0,112.7 121.4,111.1 123.8,109.4 126.2,107.6 128.6,105.6 131.0,103.5 133.4,101.2 135.8,98.8 138.2,96.2 140.6,93.5 143.0,90.7 145.4,87.7 147.8,84.5 150.2,81.2 152.6,77.8 155.0,74.2 157.4,70.4 159.8,66.5 162.2,62.5 164.6,58.3 167.0,54.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="23.0,76.0 25.4,78.9 27.8,81.7 30.2,84.4 32.6,87.0 35.0,89.4 37.4,91.8 39.8,94.1 42.2,96.3 44.6,98.4 47.0,100.4 49.4,102.4 51.8,104.2 54.2,105.9 56.6,107.5 59.0,109.0 61.4,110.4 63.8,111.7 66.2,113.0 68.6,114.1 71.0,115.1 73.4,116.0 75.8,116.9 78.2,117.6 80.6,118.2 83.0,118.8 85.4,119.2 87.8,119.6 90.2,119.8 92.6,120.0 95.0,120.0 97.4,120.0 99.8,119.8 102.2,119.6 104.6,119.2 107.0,118.8 109.4,118.2 111.8,117.6 114.2,116.9 116.6,116.0 119.0,115.1 121.4,114.1 123.8,113.0 126.2,111.7 128.6,110.4 131.0,109.0 133.4,107.5 135.8,105.9 138.2,104.2 140.6,102.4 143.0,100.4 145.4,98.4 147.8,96.3 150.2,94.1 152.6,91.8 155.0,89.4 157.4,87.0 159.8,84.4 162.2,81.7 164.6,78.9 167.0,76.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="95" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">양정부호</text>
  <text x="95" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">2x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan>² + 3x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>²</text>
  <text x="95" y="172" font-size="11" text-anchor="middle" fill="currentColor">모든 방향에서 위로</text>
  <polyline points="25,192 45,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="25,210 45,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="50" y="196" font-size="10.5" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> 방향</text>
  <text x="50" y="214" font-size="10.5" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> 방향</text>
  <polyline points="202,120 358,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="208.0,76.0 210.4,78.9 212.8,81.7 215.2,84.4 217.6,87.0 220.0,89.4 222.4,91.8 224.8,94.1 227.2,96.3 229.6,98.4 232.0,100.4 234.4,102.4 236.8,104.2 239.2,105.9 241.6,107.5 244.0,109.0 246.4,110.4 248.8,111.7 251.2,113.0 253.6,114.1 256.0,115.1 258.4,116.0 260.8,116.9 263.2,117.6 265.6,118.2 268.0,118.8 270.4,119.2 272.8,119.6 275.2,119.8 277.6,120.0 280.0,120.0 282.4,120.0 284.8,119.8 287.2,119.6 289.6,119.2 292.0,118.8 294.4,118.2 296.8,117.6 299.2,116.9 301.6,116.0 304.0,115.1 306.4,114.1 308.8,113.0 311.2,111.7 313.6,110.4 316.0,109.0 318.4,107.5 320.8,105.9 323.2,104.2 325.6,102.4 328.0,100.4 330.4,98.4 332.8,96.3 335.2,94.1 337.6,91.8 340.0,89.4 342.4,87.0 344.8,84.4 347.2,81.7 349.6,78.9 352.0,76.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="208.0,120.0 210.4,120.0 212.8,120.0 215.2,120.0 217.6,120.0 220.0,120.0 222.4,120.0 224.8,120.0 227.2,120.0 229.6,120.0 232.0,120.0 234.4,120.0 236.8,120.0 239.2,120.0 241.6,120.0 244.0,120.0 246.4,120.0 248.8,120.0 251.2,120.0 253.6,120.0 256.0,120.0 258.4,120.0 260.8,120.0 263.2,120.0 265.6,120.0 268.0,120.0 270.4,120.0 272.8,120.0 275.2,120.0 277.6,120.0 280.0,120.0 282.4,120.0 284.8,120.0 287.2,120.0 289.6,120.0 292.0,120.0 294.4,120.0 296.8,120.0 299.2,120.0 301.6,120.0 304.0,120.0 306.4,120.0 308.8,120.0 311.2,120.0 313.6,120.0 316.0,120.0 318.4,120.0 320.8,120.0 323.2,120.0 325.6,120.0 328.0,120.0 330.4,120.0 332.8,120.0 335.2,120.0 337.6,120.0 340.0,120.0 342.4,120.0 344.8,120.0 347.2,120.0 349.6,120.0 352.0,120.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="280" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">양준정부호</text>
  <text x="280" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">(x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> + x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>)²</text>
  <text x="280" y="172" font-size="11" text-anchor="middle" fill="currentColor">위로, 다만 한 직선에서 평평</text>
  <polyline points="210,192 230,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="210,210 230,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="235" y="196" font-size="10.5" fill="currentColor">(1, 1)/√2 방향</text>
  <text x="235" y="214" font-size="10.5" fill="currentColor">(1, −1)/√2 방향</text>
  <polyline points="387,120 543,120" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.35"/>
  <polyline points="393.0,98.0 395.4,99.4 397.8,100.8 400.2,102.2 402.6,103.5 405.0,104.7 407.4,105.9 409.8,107.1 412.2,108.2 414.6,109.2 417.0,110.2 419.4,111.2 421.8,112.1 424.2,112.9 426.6,113.7 429.0,114.5 431.4,115.2 433.8,115.9 436.2,116.5 438.6,117.0 441.0,117.6 443.4,118.0 445.8,118.4 448.2,118.8 450.6,119.1 453.0,119.4 455.4,119.6 457.8,119.8 460.2,119.9 462.6,120.0 465.0,120.0 467.4,120.0 469.8,119.9 472.2,119.8 474.6,119.6 477.0,119.4 479.4,119.1 481.8,118.8 484.2,118.4 486.6,118.0 489.0,117.6 491.4,117.0 493.8,116.5 496.2,115.9 498.6,115.2 501.0,114.5 503.4,113.7 505.8,112.9 508.2,112.1 510.6,111.2 513.0,110.2 515.4,109.2 517.8,108.2 520.2,107.1 522.6,105.9 525.0,104.7 527.4,103.5 529.8,102.2 532.2,100.8 534.6,99.4 537.0,98.0" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="393.0,142.0 395.4,140.6 397.8,139.2 400.2,137.8 402.6,136.5 405.0,135.3 407.4,134.1 409.8,132.9 412.2,131.8 414.6,130.8 417.0,129.8 419.4,128.8 421.8,127.9 424.2,127.1 426.6,126.3 429.0,125.5 431.4,124.8 433.8,124.1 436.2,123.5 438.6,123.0 441.0,122.4 443.4,122.0 445.8,121.6 448.2,121.2 450.6,120.9 453.0,120.6 455.4,120.4 457.8,120.2 460.2,120.1 462.6,120.0 465.0,120.0 467.4,120.0 469.8,120.1 472.2,120.2 474.6,120.4 477.0,120.6 479.4,120.9 481.8,121.2 484.2,121.6 486.6,122.0 489.0,122.4 491.4,123.0 493.8,123.5 496.2,124.1 498.6,124.8 501.0,125.5 503.4,126.3 505.8,127.1 508.2,127.9 510.6,128.8 513.0,129.8 515.4,130.8 517.8,131.8 520.2,132.9 522.6,134.1 525.0,135.3 527.4,136.5 529.8,137.8 532.2,139.2 534.6,140.6 537.0,142.0" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="465" y="20" font-size="11.5" text-anchor="middle" fill="currentColor">부정부호</text>
  <text x="465" y="37" font-size="11" text-anchor="middle" opacity="0.85" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan>² − x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>²</text>
  <text x="465" y="172" font-size="11" text-anchor="middle" fill="currentColor">한쪽은 위, 다른 쪽은 아래</text>
  <polyline points="395,192 415,192" fill="none" stroke="currentColor" stroke-width="1.9"/>
  <polyline points="395,210 415,210" fill="none" stroke="currentColor" stroke-width="1.9" stroke-opacity="0.6" stroke-dasharray="5 3"/>
  <text x="420" y="196" font-size="10.5" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan> 방향</text>
  <text x="420" y="214" font-size="10.5" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan> 방향</text>
</svg>

*각 패널은 원점을 지나는 두 단위 방향을 따라 $-1$부터 $1$까지 $x^\top Ax$를 같은 세로 축척으로 그린 것이다. 그릇 $2x_1^2+3x_2^2$는 두 축 방향 모두로 오르고($3$과 $2$까지), 골짜기 $(x_1+x_2)^2$는 $(1,1)/\sqrt2$ 방향으로 $2$까지 오르지만 $(1,-1)/\sqrt2$ 방향으로는 $0$에 머물며, 안장 $x_1^2-x_2^2$는 $x_1$ 방향으로 오르고 $x_2$ 방향으로 내려간다. 양준정부호란 어느 방향으로도 축 아래로 내려가지 않는다는 뜻이다.*

### 4. SVD — 모든 행렬에 존재하는 보편적 분해

고유벡터는 정방 행렬에만 있고, 정방 행렬이라도 실수 고유벡터가 하나도 없을 수 있다. P2의 $J$는 고유값이 $(-1\pm j\sqrt3)/2$이고, §4.5의 여유자유도 팔은 아예 정방이 아니다. SVD는 *모든* 행렬에 늘이기만 하는 한 쌍의 직교 좌표계를 주고, 그 늘임 배율인 특이값이 행렬이 한 방향을 잃기까지 얼마나 가까운지를 곧바로 말한다.

*처음에는 처음 두 항목과 아래의 $C$ 계산만 읽는다. 특이값이 무엇인지를 말해 주고, §3의 조건수와 과제가 그것을 쓴다. 나머지는 두 번째 읽기로, 논문이 무언가를 분해할 때 돌아오라.*

- **모든** 행렬(모양·랭크 불문): $A = U\Sigma V^\top$, $U, V$는 **직교행렬**(열들이 길이 1이고 서로 수직 — 그래서 곱하는
  것은 순수한 회전/반사이고 아무것도 늘이지 않는다),
  $\Sigma = \text{diag}(\sigma_1 \ge \sigma_2 \ge \cdots \ge 0)$.
  독해: 회전(입력 기저 $V$) → 스케일(특이값) → 회전(출력 기저 $U$).
- **조각들의 이름.** $A \in \mathbb{R}^{m\times n}$이면 $U$는 $m\times m$, $\Sigma$는 대각선
  밖이 0인 $m\times n$, $V$는 $n\times n$이다. 정방 행렬 $Q$가 $Q^\top Q = I$를 만족하면
  **직교행렬**(orthogonal matrix)이다 — §1의 직교하는 *벡터*와 같은 말을 한 단계 위에서 쓴 것이다: $Q^\top Q$의
  $(i,j)$ 성분은 열 $i$와 열 $j$의 내적이므로, $Q^\top Q = I$는 열들이 길이 1이고 §1의 뜻으로
  서로 직교한다는 말이다. 그래서 길이를 보존한다: $\|Qx\|^2 = x^\top Q^\top Q x = \|x\|^2$. $30°$ 회전은
  $\|(3,4)\| = 5$를 그대로 두고, 비예시 $\text{diag}(2,1)$은
  $\text{diag}(2,1)^\top\text{diag}(2,1) = \text{diag}(4,1) \ne I$라서 늘인다. 열 하나씩 읽으면
  SVD는 이렇게 말한다.
  $$A v_i = \sigma_i u_i, \qquad A^\top u_i = \sigma_i v_i$$
  $V$의 열 $v_i$가 **오른쪽 특이벡터**, $U$의 열 $u_i$가 **왼쪽 특이벡터**, $\sigma_i \ge 0$이
  **특이값**이다. 입력 방향 $v_i$가 $\sigma_i$배 늘어나 출력 방향 $u_i$로 간다.

<svg viewBox="0 0 560 150" style="max-width:100%;height:auto" role="img" aria-label="SVD = 회전 → 스케일 → 회전">
  <g transform="translate(20 0)">
  <g fill="none" stroke="currentColor" stroke-width="1.5">
    <circle cx="60" cy="75" r="38"/>
    <circle cx="205" cy="75" r="38"/>
    <ellipse cx="350" cy="75" rx="42" ry="17"/>
    <ellipse cx="475" cy="75" rx="17" ry="42" transform="rotate(-30 475 75)"/>
  </g>
  <g stroke="currentColor" stroke-width="1.2" opacity="0.6">
    <line x1="60" y1="75" x2="87" y2="48"/><line x1="60" y1="75" x2="33" y2="48"/>
    <line x1="205" y1="75" x2="243" y2="75"/><line x1="205" y1="75" x2="205" y2="37"/>
    <line x1="350" y1="75" x2="392" y2="75"/><line x1="350" y1="75" x2="350" y2="58"/>
  </g>
  <defs><marker id="svdArrowk" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
    <path d="M0,0 L7,3 L0,6 z" fill="currentColor"/></marker></defs>
  <g stroke="currentColor" stroke-width="1.4" marker-end="url(#svdArrowk)" opacity="0.8">
    <line x1="108" y1="75" x2="152" y2="75"/><line x1="253" y1="75" x2="297" y2="75"/><line x1="400" y1="75" x2="428" y2="75"/>
  </g>
  <g font-size="12" fill="currentColor" text-anchor="middle">
    <text x="60" y="138">단위 원</text>
    <text x="130" y="66">Vᵀ</text><text x="275" y="66">Σ</text><text x="414" y="66">U</text>
    <text x="205" y="138">회전</text><text x="350" y="138">σ<tspan dy="3.5">1</tspan><tspan dy="-3.5">, σ</tspan><tspan dy="3.5">2</tspan><tspan dy="-3.5"> 배로 늘리기</tspan></text><text x="475" y="138">회전</text>
  </g>
  </g>
</svg>

*모든 행렬이 구에 하는 일이 정확히 이것이다: 회전 → 축 방향으로 늘이기 → 다시 회전. $\sigma_i$가 늘이는 배율이고, $\sigma_i = 0$인 방향은 사상이 파괴하는 방향이다.*

- **[[02-foundations/engineering-math|0.5 §4]]의 특이 행렬로 계산해 보면.** $C = \begin{pmatrix}1&2\\2&4\end{pmatrix}$.
  $C^\top C = \begin{pmatrix}5&10\\10&20\end{pmatrix}$이고 그 고유값은
  $\lambda^2 - 25\lambda = 0$에서 $\lambda = 25, 0$. 따라서 $\sigma_1 = \sqrt{25} = 5$,
  $\sigma_2 = 0$이다. 그대로 읽으면: 0이 아닌 특이값이 **하나**이므로 랭크 1, 즉 $C$는 평면을
  직선 하나로 뭉갠다. 그리고 $\|C\|_2 = \sigma_1 = 5$가 이 행렬이 무언가를 늘일 수 있는
  최대치다. 파괴되는 방향은 $\sigma_2 = 0$에 대응하는 우특이벡터, 여기서는 $(2,-1)/\sqrt5$ —
  검산: $C(2,-1) = (0,0)$ ✓. 2절의 영공간을 다른 길로 찾은 것이다.
- 연결: $\sigma_i^2$ = $A^\top A$의 고유값; 랭크 = 0이 아닌 $\sigma_i$의 수;
  $\|A\|_2 = \sigma_1$. 마지막 것이 **스펙트럼 노름**(행렬 2-노름)을 가장 큰 늘임으로 정의한
  것이다.
  $$\|A\|_2 = \max_{x \ne 0} \frac{\|Ax\|_2}{\|x\|_2} = \sigma_1$$
  가장 좋은 입력이 $v_1$이기 때문이다. 위의 $C$에서 입력 $(1,2)$는 $(5,10)$이 되어 정확히 $5$배
  늘어난다.
- **Eckart–Young**: 최적 랭크-$k$ 근사($\|\cdot\|_F$·$\|\cdot\|_2$ 기준)는 절단 SVD
  $A_k = \sum_{i\le k}\sigma_i u_i v_i^\top$이고, 그 오차는 정확히 버린 것만큼이다.
  $$\|A - A_k\|_2 = \sigma_{k+1}, \qquad \|A - A_k\|_F = \sqrt{\textstyle\sum_{i>k}\sigma_i^2}$$
  그래서 어떤 랭크-$k$ 행렬도 더 잘할 수 없다. 예: $A = \text{diag}(3,2,1)$, $k = 1$이면
  $\text{diag}(3,0,0)$을 남기고 오차는 2-노름으로 $2$, 프로베니우스로 $\sqrt5 = 2.236$이다.
  모델 압축과 PCA의 수학적 면허장.
  ([[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 관련되지만 다르다: 완성된 업데이트를
  SVD로 근사하는 게 아니라 업데이트 자체를 처음부터 저랭크로 *매개화*하는 경험적 설계다.)
- **PCA 네 줄 요약**: 데이터 $X$를 중심화; 공분산 $C = \frac1n X^\top X$; 그 상위
  고유벡터들 = 분산 최대 방향 = $X$의 오른쪽 특이벡터; 투영. 학습된 표현의 고전적
  조상이다. 즉 PCA(주성분 분석)는 선형 차원 축소다. 중심화한 샘플 $n$개를 행으로 담은 $X$에서
  주성분은
  $$C\,w_i = \lambda_i\,w_i, \qquad z = W_k^\top x$$
  를 푼다. $w_i$는 $i$번째 주방향, $\lambda_i$는 그 방향의 데이터 분산, $W_k$는 상위 $k$개 방향을
  모은 행렬, $z$는 샘플 $x$의 새 좌표 $k$개다. 단위 방향 $w$를 따른 분산이 $w^\top C w$이므로 분산이 최대인 방향이 곧 $C$의 고유벡터다. 남기는 분산 비율은
  $\sum_{i \le k}\lambda_i / \sum_i \lambda_i$다. 예: 점 $(2,0), (0,1), (-2,0), (0,-1)$은 이미
  평균이 0이고 $C = \text{diag}(2,\ 0.5)$이므로, 첫 주성분은 $(1,0)$으로 분산의
  $2/2.5 = 80\%$를 담고, 숫자 하나짜리 코드는 $2, 0, -2, 0$이다.

**곱은 오른쪽에서 왼쪽으로 읽는다.** Vᵀ가 입력을 특별한 입력 방향들의 성분으로 바꾼다. Σ가 각 성분을 늘이거나 지운다. U가 결과를 출력 좌표로 표현한다. 입력·출력 공간의 차원이 달라도 된다. A 자체의 고유벡터 해석을 쓸 수 없는 경우에도 SVD가 가능한 이유다.

위 특이 행렬의 0인 특이값은 사라지는 방향의 성분이 출력에 흔적을 남기지 않는다는 뜻이다. 출력에 없는 정보는 역행렬로 복원할 수 없다. 0은 아니지만 아주 작은 특이값도 관련 문제를 만든다. 입력 성분을 복원하려면 작은 수로 나눠야 하므로 신호와 함께 측정 오차도 증폭한다. 역문제를 풀기 전에 조건수를 보는 이유다.

**이해 확인.** 절단 SVD가 약한 방향을 버리면 복원 오차를 받아들이는 대신 더 단순하거나 안정적인 표현을 얻는다. 버린 방향이 내 과제에 중요하지 않다는 증거는 아니다. 분산이 작은 특징도 분류기나 로봇이 필요한 구분을 담을 수 있다. 행렬 근사 목적과 후속 과제 목적을 나눠야 한다.

### 4.5 유사역행렬 — $J^\dagger$가 무슨 뜻인가

*두 번째 읽기이되 한 가지는 예외다: 처음에는 아래의 모양별 표와 과제가 쓰는 P2 계산만 필요하다. 나머지는 로보틱스 트랙에서 $J^\dagger$가 처음 나올 때를 위한 것이다.*

기호 $A^\dagger$는 로보틱스 트랙 곳곳에 나온다 — 역기구학의 $J^\dagger$, 작업공간 제어의
$J^\dagger$ — 그리고 위의 SVD와 이 위키의 모든 솔버를 잇는 대상이다. 마주치는 행렬 대부분이
정사각이 아니어서 $A^{-1}$을 쓸 수 없기 때문에 존재한다.

#### 4.5.1 뒤집을 것이 있을 때, 그리고 두 공식

**애초에 뒤집을 것이 있기는 한가?** $A^\top A$는 정확히 $A$의 열이 선형독립일 때 역을 갖는다.
한 줄이면 보인다. $A^\top A x = 0$이면 $x^\top A^\top A x = \lVert Ax \rVert^2 = 0$이므로
$Ax = 0$이고, 독립성에 의해 $x = 0$이다.

**공식이 둘이고, 어느 쪽을 얻는지는 모양이 정한다.**

| 모양 | 유사역행렬 | 정체 | 무엇을 계산하는가 |
|---|---|---|---|
| 키 크고 열이 독립 ($m > n$) | $A^\dagger = (A^\top A)^{-1}A^\top$ | 왼쪽 역원, $A^\dagger A = I$ | *과결정* 계의 최소제곱 해 |
| 넓고 행이 독립 ($m < n$) | $A^\dagger = A^\top (AA^\top)^{-1}$ | 오른쪽 역원, $AA^\dagger = I$ | *부족결정* 계의 *최소 노름* 해 |
| 정사각이고 가역 | 둘 다 | 역행렬 | $A^{-1}$ — 두 공식이 여기로 무너진다 |

그 두 행이 서로 다른 두 로보틱스 상황이다. 키 큰 쪽은 미지수보다 측정이 많은 경우 — 보정,
번들 조정, 점군에 평면 맞추기. 넓은 쪽은 과제 차원보다 관절이 많은 경우 — 여유자유도 팔이고,
요청한 도구 운동을 만드는 관절 속도가 무한히 많으므로 하나를 고르는 규칙이 필요하다.

#### 4.5.2 두 계산: 여유자유도 팔과 P2

**계산 — 여유자유도 팔에서의 최소 노름 규칙.** 단위 길이 링크 셋짜리 평면 팔을
$\theta = (0°, 90°, 0°)$에 두자. 관절 속도를 도구 속도로 보내는 야코비는 열 규칙(MR 5장)에서 나온다 — 각 열은 그 관절만 단위 속도로 돌릴 때 생기는 말단 속도다 — 그리고 $2 \times 3$이다 —
넓고, 따라서 여유자유도가 있다.

$$J = \begin{bmatrix} -2 & -2 & -1 \\ 1 & 0 & 0 \end{bmatrix}, \qquad JJ^\top = \begin{bmatrix} 9 & -2 \\ -2 & 1 \end{bmatrix}, \qquad \det JJ^\top = 5$$

최소 노름 규칙은 $J\dot\theta = v$를 만족하면서 $\lVert\dot\theta\rVert$를 최소화하는 데서 따라 나온다. 답이 오른쪽 유사역행렬이다:

$$J^\dagger = J^\top (JJ^\top)^{-1} = \begin{bmatrix} 0 & 1 \\ -0.4 & -0.8 \\ -0.2 & -0.4 \end{bmatrix}$$

도구를 위로 1 m/s로 올리라고 하자, 즉 $v = (0, 1)$. 그러면
$\dot\theta = J^\dagger v = (1,\, -0.8,\, -0.4)$이고 $\lVert\dot\theta\rVert = 1.342$다.

이제 여유자유도를 찾자. $J$의 영공간은 $n = (0,\, 0.447,\, -0.894)$가 친다 — $Jn = 0$을
확인하라. 그러므로 $\dot\theta + \alpha n$은 어떤 $\alpha$에 대해서도 **정확히 같은 도구
속도**를 만들고, 그 노름은 $\sqrt{1.8 + \alpha^2}$다. $\alpha = 1$이면 1.673, $\alpha = -1$
이어도 1.673. 모든 대안이 더 길다. "유사역행렬"의 내용이 그것으로 전부다. 일을 해내는 무한히
많은 관절 운동 중 가장 짧은 것을 돌려주고, 영공간은 남은 자유다 —
[[04-robotics/modern-robotics/ch06-inverse-kinematics|MR 6장]]이 그것을 관절 한계와 장애물
회피에 쓴다.

**계산: 장치 P2, 과제가 쓰는 정방 경우.** 카탈로그 자세 $\theta=(0^\circ,90^\circ)$([[02-foundations/lab-plants|0.6]]):

$$J=\begin{pmatrix}-1&-1\\1&0\end{pmatrix}.$$

말단 $(1,1)$에서 열을 그려라. 열 1은 $\dot\theta=(1,0)$의 말단 속도 $(-1,1)$, 열 2는 $(-1,0)$. $\det J=1$인 $2\times 2$ 역행렬 공식은 $J^{-1}=\begin{pmatrix}0&1\\-1&-1\end{pmatrix}$. 정방·가역이므로 표의 마지막 행이 $J^\dagger=J^{-1}$이라고 말한다. $J J^{-1}=I$. 특이값은 §4가 $C$의 것을 구한 방식대로 $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$에서 나온다. 고유값이 $\lambda^2-3\lambda+1=0$을 풀어 $\lambda=2.618,\ 0.382$이므로 $\sigma=\sqrt\lambda=1.618,\ 0.618$, 따라서 $\kappa_2(J)=1.618/0.618=2.618$이고 타원의 넓이는 $\pi\sigma_1\sigma_2=\pi\lvert\det J\rvert=\pi$다. 그림의 숫자 그대로다. 과제의 유도 문항은 같은 절차를 그리기 문항의 반대쪽 엘보에서 되풀이하는데, 거기서는 답이 뜻밖의 모양으로 나온다. 위의 3링크는 가로로 넓어서 유사역행렬이 필요했고, P2는 아니다. P2가 SVD 이야기를 필요로 하는 것은 다음 문장이다. $\theta_2\to 0$이면 두 열이 평행해지고 $\det J\to 0$, $\kappa_2(J)\to\infty$, 옆방향 말단 운동이 사라진다. $J^\dagger$는 잃어버린 방향에서 아래 $\Sigma^\dagger$가 예측하는 대로 폭발한다.

#### 4.5.3 SVD의 관점, 특이점, 감쇠 최소제곱

**SVD의 관점, 그리고 $J^\dagger$가 폭발하는 이유.** §4에서 $A = U\Sigma V^\top$로 쓰면
유사역행렬은

$$A^\dagger = V\Sigma^\dagger U^\top, \qquad \Sigma^\dagger = \operatorname{diag}(1/\sigma_1,\, \ldots,\, 1/\sigma_r,\, 0,\, \ldots)$$

이다 — 0이 아닌 특이값만 뒤집고 0은 그대로 둔다. 이것이 랭크가 모자란 것을 포함해 *모든*
행렬에서 통하는 정의이고, 위의 두 공식은 그 특수한 경우다. 그리고 실패 방식도 설명한다.
특이 자세 근처에서는 어떤 $\sigma_i \to 0$이므로 $1/\sigma_i \to \infty$가 되고 돌려받는
관절 속도가 특이 자세에 다가갈수록 그 한 방향으로 한없이 커진다. 팔에게 움직일 수 없는 방향으로 움직이라고 요구한 것이다. 특이 자세 그 자체에서는 유사역행렬이 그 0을 건드리지 않으므로, 랭크가 실제로 떨어지는 순간 답이 불연속으로 뛴다.

#### 4.5.4 무어–펜로즈 정의

**두 공식 뒤에 있는 정의.** 임의의 $m\times n$ 행렬 $A$의 (무어–펜로즈) 유사역행렬은 네 조건을
만족하는 유일한 $n\times m$ 행렬 $A^\dagger$다.

$$AA^\dagger A = A, \qquad A^\dagger A A^\dagger = A^\dagger, \qquad (AA^\dagger)^\top = AA^\dagger, \qquad (A^\dagger A)^\top = A^\dagger A$$

앞의 둘은 되돌릴 수 있는 곳에서는 $A^\dagger$가 $A$를 되돌린다는 뜻이고, 뒤의 둘은 곱
$AA^\dagger$와 $A^\dagger A$가 직교 투영이라는 뜻이다. 그래서 되돌릴 수 없는 부분은 제멋대로가
아니라 수직으로 버려진다. SVD 공식이 넷을 모두 만족하므로 그것이 일반 정의다. 위의 $J^\dagger$도
넷을 수치적으로(약 $10^{-16}$까지) 통과하고, $J^\dagger J$는 $I$가 아니라 행이 $(1,0,0)$,
$(0, 0.8, 0.4)$, $(0, 0.4, 0.2)$인 투영이다. 팔이 여유자유도를 가지므로 영공간 방향 $n$을 정확히
지우는 것이다.

해법은 작은 특이값을 정확히 뒤집는 일을 그만두는 것이다 — $1/\sigma$를
$\sigma/(\sigma^2 + \lambda)$로 바꾸면 모든 $\sigma$에 대해 유계이고 $\sigma^2 \gg \lambda$일
때는 $1/\sigma$와 같다. 그것이 **감쇠 최소제곱**이다. 정확한 최소 노름 해 대신
$\lVert J\dot\theta - v\rVert^2 + \lambda\lVert\dot\theta\rVert^2$, 즉 추종 오차와 관절 속도의
절충을 최소화하며, 그 해는

$$J^\dagger_\lambda = J^\top (JJ^\top + \lambda I)^{-1}$$

이다. $\lambda > 0$이 감쇠다. $\lambda I$를 더하면 특이 자세에서도 행렬이 가역으로 남으므로 역이
폭발할 수 없다. 숫자로: $\lambda = 0.01$일 때 멀쩡한 $\sigma = 1$은 $1$ 대신 $0.990$으로, 특이에
가까운 $\sigma = 0.01$은 $100$ 대신 $0.990$으로 뒤집힌다. 위의 팔에서 같은 $\lambda$는 명령
$v = (0,1)$을 $(1,\ -0.8,\ -0.4)$ 대신 $\dot\theta = (0.982,\ -0.784,\ -0.392)$로 바꾼다 — 추종은
조금 덜하고 속도는 유계다. 그리고 이것은
[[02-foundations/optimization|4. 최적화 §3.5]]에서 만나게 될 신뢰 파라미터와 같은 $\lambda$다 —
이 페이지가 기대는 것이 아니라 앞을 가리키는 표지다. 그러니 사슬은 이렇게 이어진다: 특이값 → 유사역행렬
→ 그중 하나가 사라지면 벌어지는 일 → 감쇠 → Levenberg–Marquardt. 이름 넷, 발상 하나.

### 5. 제어이론과의 연결

*두 번째 읽기 — 제어 트랙에 닿았을 때를 위한 절이다. 이 페이지의 다른 부분은 이 절에 기대지 않는다.*

제어기를 만들기 전에 설계자는 시스템이 스스로 가라앉는지, 입력이 모든 상태를 몰 수 있는지, 센서가 모든 상태를 볼 수 있는지를 알아야 하고, 그 질문 하나하나가 행렬 계산이다. 선형대수는 제어의 언어 *그 자체*다 ([[04-robotics/index|제어 트랙]]):

#### 5.1 상태공간 모델과 행렬 지수

- **상태공간 모델** $\dot{x} = Ax + Bu$, $y = Cx$: 시스템이 곧 행렬이다; 시뮬레이션은
  반복된 행렬곱이고, 행렬 지수 $e^{At}$가 입력이 없는 시스템의 정확한 해를 주고, 입력이 있으면 합성곱 $x(t) = e^{At}x_0 + \int_0^t e^{A(t-s)}Bu(s)\,ds$가 해다.
  기호: $x \in \mathbb{R}^n$은 **상태**(미래 입력과 함께 미래를 결정하는 숫자들),
  $u \in \mathbb{R}^m$은 입력, $y \in \mathbb{R}^p$는 측정 출력이고, $A$($n\times n$), $B$($n\times m$),
  $C$($p\times n$)는 각각 내부 동역학, 입력이 들어오는 방식, 센서가 보는 것이다(자세한 서술은
  [[04-robotics/control-theory-ce397|5. 제어 이론 §2]]). **행렬 지수**는 $e^{at}$와 같은 거듭제곱
  급수로 정의한다.
  $$e^{At} = I + At + \frac{(At)^2}{2!} + \frac{(At)^3}{3!} + \cdots$$
  그래서 $\frac{d}{dt}e^{At} = Ae^{At}$이고 $x(t) = e^{At}x_0$가 $\dot x = Ax$를 푼다. 예: 힘
  $u$로 미는 단위 질량의 상태를 (위치, 속도)로 두면 $A = \begin{pmatrix}0&1\\0&0\end{pmatrix}$,
  $B = (0, 1)$이다. $A^2 = 0$이라 급수가 멈추고 $e^{At} = \begin{pmatrix}1&t\\0&1\end{pmatrix}$이며,
  위치 $0$, 속도 $1$에서 출발하면 $t = 2$ 뒤 상태는 $(2, 1)$이다.
#### 5.2 안정성

- **안정성 = $A$의 고유값** (극점): 연속 시간은 모든 $\text{Re}(\lambda_i) < 0$일 때,
  이산 시간은 모든 $|\lambda_i| < 1$일 때 안정.
#### 5.3 가제어성과 가관측성

- **가제어성**: 입력이 상태를 실제로 어느 방향으로 밀 수 있나? 입력 한 스텝은 $B$의 열
  방향으로 움직이고, 동역학이 그 도달 범위를 $AB$로, 다시 $A^2B$로 회전시킨다. 그 도달
  방향들을 쌓아 —$[B, AB, \ldots, A^{n-1}B]$— 함께 $n$차원 전체를 생성하면($\text{rank}=n$)
  *모든* 상태에 도달 가능하고, 한 방향이라도 빠지면 어떤 입력 시퀀스도 상태를 그리로
  몰지 못한다. 판정식으로 쓰면
  $$\mathcal{C} = [\,B \;\; AB \;\; \cdots \;\; A^{n-1}B\,], \qquad \text{controllable} \iff \text{rank}\,\mathcal{C} = n$$
  이고 $\mathcal{C}$는 $n \times nm$ 가제어성 행렬이다. 그 뒤의 거듭제곱은 새 방향을 더하지
  못하므로 $A^{n-1}B$에서 멈춘다(케일리–해밀턴 논증은 [[04-robotics/control-theory-ce397|5. 제어 이론 §6]]).
  예: 위의 밀리는 질량은 $AB = (1, 0)$이라 $\mathcal{C} = \begin{pmatrix}0&1\\1&0\end{pmatrix}$,
  랭크 2다 — 힘 하나로 위치와 속도를 모두 몬다. 비예시: $A = \text{diag}(1, 2)$,
  $B = (1, 0)$이면 $\mathcal{C} = \begin{pmatrix}1&1\\0&0\end{pmatrix}$, 랭크 1이라 둘째 모드,
  그것도 불안정한 모드에 결코 영향을 줄 수 없다.
<svg viewBox="0 0 560 196" style="max-width:100%;height:auto" role="img" aria-label="페이지의 숫자로 그린 가제어성. 왼쪽, 밀리는 질량: B = (0, 1)은 속도 방향, AB = (1, 0)은 위치 방향이라 둘이 평면을 생성한다, 랭크 2. 오른쪽, A = diag(1, 2), B = (1, 0): AB = (1, 0)이 B와 같은 직선 위에 있어 둘째 상태 방향에는 결코 닿지 못한다, 랭크 1.">
  <defs><marker id="cArrowk" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <polyline points="70.0,138.0 166.1,138.0" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="70.0,138.0 70.0,41.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="350.0,138.0 446.1,138.0" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polyline points="350.0,138.0 350.0,41.9" fill="none" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5"/>
  <polygon points="70.0,138.0 132.0,138.0 132.0,76.0 70.0,76.0" fill="currentColor" fill-opacity="0.10" stroke="none"/>
  <polyline points="70.0,138.0 70.0,76.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrowk)"/>
  <polyline points="70.0,138.0 132.0,138.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrowk)"/>
  <text x="77.0" y="82.0" font-size="11" fill="currentColor">B = (0, 1)</text>
  <text x="128.0" y="155.0" font-size="11" fill="currentColor">AB = (1, 0)</text>
  <text x="170.1" y="142.0" font-size="11" fill="currentColor">위치</text>
  <text x="64.0" y="35.9" font-size="11" fill="currentColor">속도</text>
  <polyline points="350.0,138.0 350.0,41.9" fill="none" stroke="currentColor" stroke-width="5" stroke-opacity="0.12"/>
  <polyline points="350.0,138.0 412.0,138.0" fill="none" stroke="currentColor" stroke-width="2" marker-end="url(#cArrowk)"/>
  <text x="388.0" y="155.0" font-size="11" fill="currentColor">B = AB = (1, 0)</text>
  <text x="450.1" y="142.0" font-size="11" fill="currentColor">x<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="344.0" y="35.9" font-size="11" fill="currentColor">x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  <text x="359.0" y="82.2" font-size="10.5" opacity="0.85" fill="currentColor">닿지 못함</text>
  <text x="20.0" y="16" font-size="11" fill="currentColor">밀리는 질량: A의 행 (0, 1), (0, 0)</text>
  <text x="300.0" y="16" font-size="11" fill="currentColor">A = diag(1, 2), B = (1, 0)</text>
  <text x="20.0" y="184" font-size="11.5" fill="currentColor">랭크 2 → 모든 상태에 도달</text>
  <text x="300.0" y="184" font-size="11.5" fill="currentColor">랭크 1 → x<tspan dy="3.5">2</tspan><tspan dy="-3.5">&#8203;</tspan>에 결코 도달 못함</text>
</svg>

*왼쪽, 밀리는 질량: 힘은 속도의 변화 $B=(0,1)$로 들어오고, 동역학의 한 스텝이 그것을 위치의 변화 $AB=(1,0)$로 바꾼다. 둘이 평면을 생성하므로 랭크 2다. 오른쪽, $A=\text{diag}(1,2)$, $B=(1,0)$: $AB=(1,0)$이 $B$와 같은 직선 위에 있어, $u$를 어떻게 써도 둘째 모드, 그것도 불안정한 모드 $x_2$에 닿지 못한다.*

  가관측성은 전치 쌍둥이다 — 출력 $y$가 결국 모든 상태를 드러낼 수 있는가? — 행렬은 $[C^\top, A^\top C^\top, \ldots]$이다.
  보통 방식으로 쌓으면
  $$\mathcal{O} = \begin{bmatrix} C \\ CA \\ \vdots \\ CA^{n-1} \end{bmatrix}, \qquad \text{observable} \iff \text{rank}\,\mathcal{O} = n$$
  이고, 앞의 행렬의 전치라 랭크가 같다. $u = 0$일 때 $y, \dot y, \ddot y, \ldots$가
  $Cx, CAx, CA^2x, \ldots$와 같으므로, 이 묶음이 풀랭크일 때 정확히 $x$를 풀어낼 수 있기
  때문이다. 예: 밀리는 질량의 위치를 재면 $C = (1, 0)$, $\mathcal{O} = I$, 랭크 2로 가관측이다.
  비예시: 속도만 재면 $C = (0, 1)$, 행이 $(0,1)$과 $(0,0)$이라 랭크 1 — 속도 자료를 아무리 모아도
  질량이 어디서 출발했는지 알 수 없다.
- LQR 이득([[04-robotics/lqr-lqg|6. LQR/LQG]]), 칼만 필터([[02-foundations/probability|3. 확률 §5]]), MPC([[04-robotics/mpc|7. MPC]])가 전부 구조화된 행렬 계산으로 환원된다 — LQR과 칼만은 리카티 재귀(단계마다 선형 풀이 한 번), MPC는 응축(condensing: 상태를 소거해 입력만 변수로 남기는 것, [[04-robotics/mpc|7. MPC §2]]) 뒤의 조밀한 QP(이차 계획: 선형 제약 아래 이차 비용 최소화) — 수치 선형대수가 제어 엔지니어의 일상 도구인 이유.

### 6. 고차원의 기하 (논문 읽기용 직관)

논문은 768차원 임베딩을 2차원과 3차원에서 쌓은 직관으로 다루는데, 그 직관 몇 가지가 거기서는 틀린다. 이 절은 어느 것이 틀리는지 숫자로 말한다.

- 평균이 0인(등방) 무작위 고차원 벡터들은 거의 직교한다: $\cos\theta$가 표준편차 $1/\sqrt d$(가우스 벡터라면 정확히)로 0 근처에 모인다. $d=3$이면 $0.58$, $d=64$(어텐션 헤드 하나의 폭)이면 $0.125$, $d=768$(흔한 임베딩 폭)이면 $0.036$이다. 무작위 단위 방향의 성분 $d$개의 제곱이 합 $1$을 고르게 나눠 가지므로 하나가 평균 $1/d$이기 때문이다. (평균은 어느 차원에서나 이미 0이고, 평균이 0이 아닌 벡터들은 직교해지지 않는다.) 이것이 수백만 임베딩에 대한
  내적 검색이 *가능한* 이유 중 하나다: 무관한 항목의 점수가 0 근처로 깔린다. (관련 쌍의
  점수가 높은 것은 기하가 아니라 *학습된* 임베딩의 성질이다.)
- 거리가 집중된다: 가장 가까운 이웃과 가장 먼 이웃의 차이가 작다. 무작위 가우스 점 두 개 사이의 거리는 상대 퍼짐(표준편차를 평균으로 나눈 값)이 $d=3$에서 $0.42$이지만 $d=64$에서 $0.089$, $d=768$에서 $0.026$으로 대략 $1/\sqrt{2d}$이고, 고차원에서는 거의 모든 쌍이 거의 같은 거리에 있다는 뜻이다 — 원시 특징 위의 거리 대신 *학습된* 임베딩과 거리를 쓰는 이유 중 하나다. (코사인 유사도도 집중을 피하지 못한다: 단위 벡터에서 $\|a-b\|^2 = 2 - 2\cos\theta$이므로 이웃 순위는 유클리드 거리와 똑같다. 코사인이 더하는 것은 벡터 크기를 무시하는 것이다.)
- 다양체 가설: 실제 데이터는 픽셀 공간 속 저차원 곡면 위에 산다 —
  잠재 공간([[01-canonical-papers/notes/6-diffusion/vae|VAE]],
  [[01-canonical-papers/notes/6-diffusion/latent-diffusion|latent diffusion]])의 암묵적 정당화.

> [!tip] 더 깊이 · Going deeper
> 이 페이지는 빠르게 나아간다. 너무 빠르면 Boyd·Vandenberghe의 무료 교재 [*Introduction to Applied Linear Algebra*](https://web.stanford.edu/~boyd/vmls/)(VMLS)가 §1과 §2의 최소제곱 쪽을 더 천천히 간다. 그 책은 모든 것을 일차독립과 QR로 세우고, 최소제곱의 열 독립 가정을 명시하며, 랭크·열공간·영공간이라는 말은 쓰지 않는다. 고윳값·SVD 쪽은 Strang의 *Introduction to Linear Algebra*가 표준 첫 강의다. 각 개념이 논문 어디에 나타나는지는 이 페이지로 돌아와 보라.

### 스스로 점검

1. 비선형성 없는 선형층 두 개는 왜 하나로 접히는가? 그 합성의 랭크는 최대 얼마인가?
2. 정규방정식을 유도하고, 잔차가 $\text{col}(A)$에 직교하는 이유를 설명하라.
3. 이산 시스템 $x_{t+1} = Ax_t$의 고유값이 $0.9, 1.02$다. 무슨 일이, 어느 방향으로
   일어나는가?
4. [[01-canonical-papers/notes/1-foundations/lora|LoRA]]는 왜 $B = 0$으로 초기화하는가? (0스텝에서
   $W_0 + BA$는 어떤 사상과 같은가?)

> [!tip]- 스스로 점검 정답 · Answers
> 1. $W_2(W_1 x) = (W_2 W_1)x$ — 곱이 곧 하나의 선형 사상이라 접힌다; 랭크는 $\min(\text{rank}\,W_1, \text{rank}\,W_2)$ 이하.
> 2. $\nabla\|Ax-b\|^2 = 2A^\top(Ax-b) = 0 \Rightarrow A^\top A\hat{x} = A^\top b$; 잔차 $r = b - A\hat{x}$는 $A^\top r = 0$ — $A$의 모든 열과 직교한다.
> 3. 0.9 고유방향 성분은 감쇠하고 1.02 방향 성분은 매 스텝 2%씩 지수 성장 — 상태는 결국 1.02의 고유벡터 방향으로 발산한다.
> 4. $B=0$이면 $\Delta W = BA = 0$이라 시작 시점에 $W_0 + BA = W_0$ — 학습이 정확히 사전학습 모델에서 출발한다(no-op 초기화).

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P2**, 카탈로그 자세 $\theta=(0^\circ,90^\circ)$와 다른 자세 둘. 이 페이지 §3(조건수), §4(특이값), §4.5. 시간 스테퍼 없음.

1. **그리기.** 반대쪽 엘보에 대한 위의 그림: 같은 말단 $(1,1)$에 $\theta=(90^\circ,-90^\circ)$로 닿고 엘보는 $(0,1)$에 있다. $J$의 두 열을 말단의 화살로(각 관절 단위속도가 만드는 말단 속도), 그리고 관절 속도의 단위원이 옮겨 간 타원을 그려라. 위의 그림과 무엇이 같고 무엇이 바뀌었는가?
2. **유도.** 1번의 반대쪽 엘보에서 $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$다. $2\times 2$ 공식으로 $J^{-1}$을, 이어서 §4.5 표의 정방·가역 행으로 $J^\dagger$를 구하고 둘이 같은지 확인하라. 그다음 말단을 1 m/s로 곧장 위로 올리는, 곧 $v=(0,1)$을 내는 관절 속도를 구해 카탈로그 자세의 것과 비교하라.
3. **해석.** 다른 베이스 각에서 팔을 편다. $\theta_1=90^\circ$로 두고 $\theta_2\to 0$으로 보내면 팔은 말단이 $(0,2)$에 오도록 곧장 위를 향한다. 두 열 화살, $\det J$, $\kappa_2(J)$는 어떻게 되고, 어떤 말단 운동이 불가능해지는가? 그림 오른쪽 칸과 비교하라.

> [!note]- 그리는 법 · How to draw it
> - 팔은 실제 비율로 그린다. 베이스는 원점, 단위 링크가 곧장 위로 엘보 $(0,1)$까지, 둘째 단위 링크가 $+x$를 따라 말단 $(1,1)$까지 가고, 관절 둘은 동그라미로 표시한다.
> - 관절마다 자기 각을 적는다. $\theta_1=90^\circ$은 베이스에서 $+x$로부터, $\theta_2=-90^\circ$은 엘보에서 링크 1에 *대한 상대각*이다. 카탈로그가 고정한 규약이고 가장 흔히 틀리는 자리다.
> - 두 열 화살표의 꼬리는 관절이 아니라 말단에 둔다. 열 1은 $\dot\theta=(1,0)$, 곧 팔 전체가 베이스를 중심으로 돌 때의 말단 속도이고, 열 2는 $\dot\theta=(0,1)$, 곧 전완이 엘보를 중심으로 돌 때의 말단 속도다. 화살표마다 그것을 만든 관절 속도를 적는다.
> - 각 화살표가 자기 관절에서 말단으로 가는 선분과 수직인지 확인한다. 회전하는 강체 위의 점은 반지름에 직각으로 움직이기 때문이고, 이 확인이 대수를 다시 푸는 것보다 부호 실수를 빨리 잡는다. 열 1의 선분은 위 그림과 같은 베이스-말단 선이고, 열 2의 선분은 다르다.
> - 단위원의 상: 한쪽 구석 상자에 관절 속도 공간의 반지름 $1$짜리 원을 그리고 말단 자리에 그 원이 옮겨 간 타원을 그린다. 반축은 §4의 특이값이고 타원 안에 $\kappa_2(J)=\sigma_1/\sigma_2$를 쓴다. 넓이는 $\pi\lvert\det J\rvert$다.
> - 위 그림의 타원을 뒤에 흐리게 겹쳐 그린다. 둘은 반축이 같고 기울기만 다르며, 둘 사이에서 $\det J$의 부호가 바뀐다.
> - 3번을 위해 더 작은 둘째 칸에 팔을 곧게 위로 편 자세 $\theta=(90^\circ,0^\circ)$를 그리고, 거기서 두 열 화살표, 타원이 주저앉은 선분, 그리고 옆에 $\det J$와 $\kappa_2$를 쓴다.

> [!tip]- 정답 · Solutions
> 1. 열 1은 그대로 $(-1,1)$이다. 팔 전체가 베이스를 중심으로 돌면 말단은 베이스-말단 선에 직각으로 움직이고, 말단은 움직이지 않았다. 열 2는 이제 $(0,1)$로, $(0,1)$에서 $(1,1)$까지 $+x$를 따라 놓인 전완에 직각이다. 그러므로 $J=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$, $\det J=-1$이다. 크기는 같고 부호는 반대이며, 그 부호는 $\sin\theta_2$의 부호다. $J^\top J=\begin{pmatrix}2&1\\1&1\end{pmatrix}$의 고윳값은 $2.618$과 $0.382$이므로 특이값은 다시 $1.618$과 $0.618$, $\kappa_2=2.618$, 넓이 $\pi$다. 타원은 모양이 같고 기울기가 다르다. 긴 축이 여기서는 $(-0.526,\ 0.851)$, 곧 $121.7^\circ$ 방향이고, 위 그림에서는 $(-0.851,\ 0.526)$, 곧 $148.3^\circ$ 방향이다. 말단은 같아도 팔이 다르니 관절 속도에서 오는 사상도 다르다.
> 2. $\det J=(-1)(1)-(0)(1)=-1$이므로 $J^{-1}=\frac{1}{-1}\begin{pmatrix}1&0\\-1&-1\end{pmatrix}=\begin{pmatrix}-1&0\\1&1\end{pmatrix}$로, $J$와 같은 행렬이다. 여기서는 $J^2=I$이기 때문이다. 정방·가역 $\Rightarrow J^\dagger=J^{-1}$. $v=(0,1)$이면 $\dot\theta=J^{-1}v=(0,1)$, 곧 엘보만 돈다. 전완이 $+x$를 따라 놓여 있어 그 끝이 곧장 위로 움직이기 때문이다. 카탈로그 자세에서는 같은 $v$에 $\begin{pmatrix}0&1\\-1&-1\end{pmatrix}(0,1)=(1,-1)$, 곧 베이스는 앞으로, 엘보는 뒤로 돌려야 한다. 말단도 요청한 속도도 같은데 관절 속도가 다르다. 사상은 말단의 위치만이 아니라 팔 전체에 달려 있다.
> 3. 가는 동안 $\det J=\sin\theta_2$가 줄고($30^\circ$에서 $0.5$, $1^\circ$에서 $0.017$) $\kappa_2$가 커진다($9.4$, 그다음 $286$). $\theta=(90^\circ,0^\circ)$에서 $J=\begin{pmatrix}-2&-1\\0&0\end{pmatrix}$이라 두 열이 모두 $-x$ 방향이므로 평행하고, $\det J=0$, $\kappa_2=\infty$다(특이값은 $\sqrt5$와 $0$). 사라진 방향은 팔을 따라가는 $y$다. 곧게 뻗은 팔은 어느 쪽을 가리키든 말단을 자기 길이 방향으로는 유한 관절 속도로 움직이지 못한다. 팔이 $+x$를 따라 놓인 그림 오른쪽 칸이 $x$를 잃은 것도 같은 이유다.
