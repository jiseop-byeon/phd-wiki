---
title: "24.9 Rendering in Practice: Loops, Effects & Passivity Control"
tags: [haptics, rendering, control]
study-depth: Working
wiki-support: Working
depth-goal: "On plant P3, place each computation of a haptic program in the right loop, write the one-degree-of-freedom effects as force laws with the state each keeps, and stabilize a wall stiffer than the sampling bound with a passivity observer and controller whose energy bookkeeping you can defend."
mastery-when: "Master multirate architectures, sampled-wall compensation and time-domain passivity when a rendering system is the contribution."
---

> [!note] Prerequisites · 선수 지식
> The sampled-wall bound $K<2b/T$ and why a held force leaks energy, from [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]; position quantization and velocity filtering from [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]; penalty and proxy rendering, event-based transients and friction models from [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 §2–§5]]; P3's encoder count and amplifier limit from [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]; passivity as an energy inequality at a port, from [[04-robotics/haptics-teleoperation/bilateral-teleoperation|24.5 §1]]; and, only for the comparisons in §3 and §6, the coupling and delay passivation of [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §3 and §7]]. Nothing else: every other quantity is defined on the page.
> 샘플된 벽의 경계 $K<2b/T$와 붙들린 힘이 에너지를 새게 하는 이유는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]. 위치 양자화와 속도 필터는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]. 벌점·proxy 렌더링, 사건 기반 과도 신호, 마찰 모형은 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 §2–§5]]. P3의 인코더 카운트와 앰프 한계는 [[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]. 포트에서의 에너지 부등식으로서의 수동성은 [[04-robotics/haptics-teleoperation/bilateral-teleoperation|24.5 §1]]. §3과 §6의 비교에만, 결합과 지연 수동화는 [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §3과 §7]]. 그 밖의 모든 양은 이 페이지에서 정의한다.

## English

*Stands on [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 Rendering, Sampling & Stability]] and [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 Haptic Rendering Algorithms]]: the same handle **P3**, now with the program around the force law written down — which loop computes what, what state each effect keeps, and how to keep a wall stable when its stiffness is past the bound.*

> [!note] First pass · 처음이라면
> Read the Running object and look at the picture: one wall too stiff for its sampling rate, once left alone and once watched by an energy counter that pays back what the wall produces. Then §1 and §2, which decide the period $T$ every later number depends on, and §6, which explains the solid curve. §3 is the effect library you will reach for when programming a device, §4 is 3-D geometry, and §5 is the physics of why the dashed curve rings. The Worked case runs all of it on P3.

### Running object · 이 페이지의 대상

Plant **P3** from [[02-foundations/lab-plants|0.6 Lab Plants]], pressed into its wall by a **light fingertip** — the hand's spring without its damper, which is the worst case the sampling bound of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]] assumes. The handle starts at rest $1\,\mathrm{mm}$ outside the wall, and the hand's desired position is $3\,\mathrm{mm}$ inside it, so every force on the page stays inside P3's amplifier limit.

| Symbol | Value | What it is |
|---|---:|---|
| $m,\ b$ | $0.04\,\mathrm{kg}$, $0.8\,\mathrm{N{\cdot}s/m}$ | catalog handle mass and damping |
| $\Delta x$ | $61.4\,\mathrm{\mu m}$ | one encoder count ([[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3]] Worked case, step 4) |
| $T$ | $1\,\mathrm{ms}$ | servo period: the encoder is read and a force is applied every $T$ |
| $k_h,\ b_h$ | $400\,\mathrm{N/m}$, $0$ | the fingertip: a spring, no damper |
| $x(0),\ x_d$ | $0.029\,\mathrm{m}$, $0.033\,\mathrm{m}$ | start at rest; where the fingertip wants the handle |
| $x_w$ | $0.030\,\mathrm{m}$ | wall face, $+x$ into the wall |
| $k_w$ | $400$ (catalog) or $2500\,\mathrm{N/m}$ | the second is past the bound $2b/T=1600\,\mathrm{N/m}$ |
| $F^{\max}$ | $2.0\,\mathrm{N}$ | amplifier limit ([[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3 §3]]) |
| $\alpha_{\max}$ | $0.8\,\mathrm{N{\cdot}s/m}$ | cap on the passivity controller's damping (§6), set equal to $b$ |

The fingertip values, the start and the cap are this page's frozen numbers; everything else is catalog. Two ways of breaking the wall are compared: a stiffness past the bound at $T=1\,\mathrm{ms}$, and the catalog stiffness with the force recomputed only every $5\,\mathrm{ms}$ (§2).

*Scope: this page teaches the program around a force law — the loops and what may run in each, the one-degree-of-freedom effects and the state each needs, implicit surfaces and surface detail in 3-D, the two energy leaks of a sampled wall, and the time-domain passivity observer and controller that close them. It does not re-derive the sampling bound, which is [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]; nor penalty, proxy and friction rendering, which is [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7]]; nor the same observer on a delayed teleoperation channel, which is [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §7]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="Two stacked plots for plant P3 pressed by a light fingertip into a 2500 N/m wall sampled at 1 kHz. Top: handle position over the first 0.3 s; the plain wall rings in a 34 Hz limit cycle while the wall with a passivity observer and controller settles. Bottom: the observed energy over 1.5 s falls steadily to minus 17.6 mJ for the plain wall and stays near minus 1.8 mJ with the controller.">
<rect x="52" y="30" width="446" height="130" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="52" y="21" font-size="12.5" fill="currentColor" font-weight="600">handle position x (mm), first 0.6 s</text>
<text x="46" y="164.0" font-size="11" fill="currentColor" text-anchor="end">29</text>
<text x="46" y="120.7" font-size="11" fill="currentColor" text-anchor="end">30</text>
<text x="46" y="77.3" font-size="11" fill="currentColor" text-anchor="end">31</text>
<text x="46" y="34.0" font-size="11" fill="currentColor" text-anchor="end">32</text>
<line x1="52" y1="116.7" x2="498" y2="116.7" stroke="currentColor" stroke-dasharray="2 3" stroke-opacity="0.8"/>
<text x="502" y="120.7" font-size="11" fill="currentColor">wall x<tspan dy="3.5" font-size="9.5">w</tspan><tspan dy="-3.5" dx="0"></tspan></text>
<text x="52.0" y="175" font-size="11" fill="currentColor" text-anchor="middle">0</text>
<text x="200.7" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
<text x="349.3" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
<text x="498.0" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.6</text>
<polyline points="52.7,159.1 53.5,156.5 54.2,152.3 55.0,146.6 55.7,139.4 56.5,130.8 57.2,120.9 57.9,109.9 58.7,98.1 59.4,86.1 60.2,74.8 60.9,64.8 61.7,56.4 62.4,49.6 63.1,44.5 63.9,41.0 64.6,39.2 65.4,39.1 66.1,40.6 66.9,43.7 67.6,48.3 68.4,54.3 69.1,61.7 69.8,70.3 70.6,80.1 71.3,91.0 72.1,102.3 72.8,113.5 73.6,123.7 74.3,132.4 75.0,139.5 75.8,144.9 76.5,148.7 77.3,150.8 78.0,151.2 78.8,150.0 79.5,147.2 80.2,142.9 81.0,137.1 81.7,129.9 82.5,121.5 83.2,111.9 84.0,101.3 84.7,90.3 85.5,79.7 86.2,70.2 86.9,62.2 87.7,55.8 88.4,51.0 89.2,47.7 89.9,46.1 90.7,46.0 91.4,47.5 92.1,50.5 92.9,55.0 93.6,60.8 94.4,68.0 95.1,76.3 95.9,85.8 96.6,96.0 97.3,106.4 98.1,116.3 98.8,125.0 99.6,132.1 100.3,137.6 101.1,141.5 101.8,143.9 102.5,144.6 103.3,143.7 104.0,141.3 104.8,137.5 105.5,132.2 106.3,125.5 107.0,117.7 107.8,108.6 108.5,98.8 109.2,88.7 110.0,79.1 110.7,70.7 111.5,63.8 112.2,58.4 113.0,54.6 113.7,52.3 114.4,51.5 115.2,52.3 115.9,54.5 116.7,58.2 117.4,63.2 118.2,69.5 118.9,77.0 119.6,85.6 120.4,95.1 121.1,104.8 121.9,114.2 122.6,122.5 123.4,129.2 124.1,134.4 124.8,138.1 125.6,140.2 126.3,140.7 127.1,139.7 127.8,137.2 128.6,133.2 129.3,127.9 130.1,121.3 130.8,113.5 131.5,104.7 132.3,95.3 133.0,85.9 133.8,77.3 134.5,69.9 135.3,64.0 136.0,59.6 136.7,56.7 137.5,55.3 138.2,55.3 139.0,56.9 139.7,59.9 140.5,64.2 141.2,69.8 141.9,76.7 142.7,84.6 143.4,93.4 144.2,102.6 144.9,111.5 145.7,119.4 146.4,126.0 147.1,131.1 147.9,134.6 148.6,136.7 149.4,137.1 150.1,136.1 150.9,133.7 151.6,129.8 152.4,124.6 153.1,118.1 153.8,110.5 154.6,101.9 155.3,93.0 156.1,84.3 156.8,76.5 157.6,69.9 158.3,64.9 159.0,61.3 159.8,59.2 160.5,58.6 161.3,59.4 162.0,61.6 162.8,65.2 163.5,70.0 164.2,76.1 165.0,83.4 165.7,91.6 166.5,100.3 167.2,108.9 168.0,116.9 168.7,123.6 169.4,128.7 170.2,132.4 170.9,134.6 171.7,135.2 172.4,134.4 173.2,132.1 173.9,128.4 174.7,123.4 175.4,117.2 176.1,109.8 176.9,101.4 177.6,92.7 178.4,84.3 179.1,76.6 179.9,70.4 180.6,65.5 181.3,62.1 182.1,60.2 182.8,59.7 183.6,60.7 184.3,63.0 185.1,66.7 185.8,71.7 186.5,77.9 187.3,85.2 188.0,93.3 188.8,101.9 189.5,110.1 190.3,117.6 191.0,123.8 191.7,128.5 192.5,131.7 193.2,133.4 194.0,133.7 194.7,132.4 195.5,129.8 196.2,125.8 197.0,120.5 197.7,113.9 198.4,106.3 199.2,97.9 199.9,89.3 200.7,81.2 201.4,74.2 202.2,68.7 202.9,64.6 203.6,61.9 204.4,60.7 205.1,60.9 205.9,62.6 206.6,65.6 207.4,69.9 208.1,75.4 208.8,82.1 209.6,89.8 210.3,98.1 211.1,106.5 211.8,114.3 212.6,120.9 213.3,126.0 214.0,129.7 214.8,131.9 215.5,132.6 216.3,131.8 217.0,129.6 217.8,126.1 218.5,121.2 219.3,115.1 220.0,107.9 220.7,99.9 221.5,91.7 222.2,83.8 223.0,76.9 223.7,71.3 224.5,67.1 225.2,64.4 225.9,63.0 226.7,63.1 227.4,64.6 228.2,67.4 228.9,71.5 229.7,76.9 230.4,83.4 231.1,90.8 231.9,98.8 232.6,106.8 233.4,114.2 234.1,120.4 234.9,125.2 235.6,128.5 236.3,130.4 237.1,130.7 237.8,129.7 238.6,127.3 239.3,123.5 240.1,118.4 240.8,112.2 241.6,104.9 242.3,97.0 243.0,89.1 243.8,81.7 244.5,75.5 245.3,70.7 246.0,67.3 246.8,65.2 247.5,64.6 248.2,65.4 249.0,67.5 249.7,71.0 250.5,75.6 251.2,81.5 252.0,88.4 252.7,96.1 253.4,103.9 254.2,111.4 254.9,117.9 255.7,123.0 256.4,126.7 257.2,128.9 257.9,129.7 258.6,129.0 259.4,127.0 260.1,123.6 260.9,118.9 261.6,113.0 262.4,106.1 263.1,98.4 263.9,90.6 264.6,83.1 265.3,76.6 266.1,71.4 266.8,67.6 267.6,65.2 268.3,64.2 269.1,64.7 269.8,66.5 270.5,69.6 271.3,73.9 272.0,79.5 272.8,86.2 273.5,93.7 274.3,101.6 275.0,109.3 275.7,116.2 276.5,121.8 277.2,126.0 278.0,128.8 278.7,130.1 279.5,129.9 280.2,128.3 280.9,125.4 281.7,121.1 282.4,115.6 283.2,109.0 283.9,101.4 284.7,93.4 285.4,85.7 286.2,78.7 286.9,72.9 287.6,68.5 288.4,65.5 289.1,64.0 289.9,63.8 290.6,65.1 291.4,67.7 292.1,71.6 292.8,76.7 293.6,82.9 294.3,90.2 295.1,98.0 295.8,105.8 296.6,113.1 297.3,119.4 298.0,124.4 298.8,127.9 299.5,129.9 300.3,130.5 301.0,129.6 301.8,127.3 302.5,123.7 303.2,118.9 304.0,112.8 304.7,105.6 305.5,97.9 306.2,90.0 307.0,82.6 307.7,76.1 308.5,70.8 309.2,67.1 309.9,64.7 310.7,63.7 311.4,64.2 312.2,66.0 312.9,69.1 313.7,73.6 314.4,79.2 315.1,85.9 315.9,93.5 316.6,101.4 317.4,109.1 318.1,116.1 318.9,121.8 319.6,126.0 320.3,128.8 321.1,130.1 321.8,130.0 322.6,128.5 323.3,125.6 324.1,121.4 324.8,115.9 325.5,109.3 326.3,101.7 327.0,93.8 327.8,86.0 328.5,79.0 329.3,73.3 330.0,68.9 330.8,65.9 331.5,64.4 332.2,64.2 333.0,65.5 333.7,68.1 334.5,71.9 335.2,77.0 336.0,83.3 336.7,90.5 337.4,98.3 338.2,106.0 338.9,113.2 339.7,119.3 340.4,124.1 341.2,127.4 341.9,129.3 342.6,129.7 343.4,128.7 344.1,126.3 344.9,122.5 345.6,117.5 346.4,111.3 347.1,104.1 347.8,96.3 348.6,88.5 349.3,81.2 350.1,75.1 350.8,70.4 351.6,67.0 352.3,65.1 353.1,64.6 353.8,65.5 354.5,67.7 355.3,71.2 356.0,76.0 356.8,81.9 357.5,88.9 358.3,96.6 359.0,104.5 359.7,112.0 360.5,118.6 361.2,123.7 362.0,127.4 362.7,129.7 363.5,130.5 364.2,129.8 364.9,127.8 365.7,124.4 366.4,119.7 367.2,113.7 367.9,106.8 368.7,99.1 369.4,91.2 370.1,83.7 370.9,77.1 371.6,71.9 372.4,68.0 373.1,65.6 373.9,64.5 374.6,64.9 375.4,66.6 376.1,69.6 376.8,73.9 377.6,79.4 378.3,86.0 379.1,93.5 379.8,101.4 380.6,109.0 381.3,115.8 382.0,121.4 382.8,125.6 383.5,128.3 384.3,129.6 385.0,129.4 385.8,127.8 386.5,124.8 387.2,120.5 388.0,115.0 388.7,108.4 389.5,100.9 390.2,93.1 391.0,85.5 391.7,78.7 392.4,73.1 393.2,68.9 393.9,66.1 394.7,64.7 395.4,64.7 396.2,66.0 396.9,68.8 397.7,72.7 398.4,77.9 399.1,84.3 399.9,91.6 400.6,99.4 401.4,107.3 402.1,114.5 402.9,120.6 403.6,125.2 404.3,128.4 405.1,130.1 405.8,130.3 406.6,129.1 407.3,126.6 408.1,122.7 408.8,117.5 409.5,111.1 410.3,103.8 411.0,96.1 411.8,88.3 412.5,81.0 413.3,74.9 414.0,70.2 414.7,66.9 415.5,65.0 416.2,64.5 417.0,65.4 417.7,67.6 418.5,71.2 419.2,75.9 420.0,81.9 420.7,88.9 421.4,96.7 422.2,104.6 422.9,112.1 423.7,118.7 424.4,123.9 425.2,127.6 425.9,129.9 426.6,130.7 427.4,130.0 428.1,128.0 428.9,124.6 429.6,119.9 430.4,114.0 431.1,106.9 431.8,99.1 432.6,91.0 433.3,83.3 434.1,76.6 434.8,71.2 435.6,67.2 436.3,64.6 437.0,63.5 437.8,63.8 438.5,65.4 439.3,68.4 440.0,72.6 440.8,78.1 441.5,84.6 442.2,92.1 443.0,100.0 443.7,107.9 444.5,115.2 445.2,121.3 446.0,126.0 446.7,129.2 447.5,130.9 448.2,131.1 448.9,130.0 449.7,127.4 450.4,123.5 451.2,118.3 451.9,111.9 452.7,104.5 453.4,96.5 454.1,88.5 454.9,81.1 455.6,74.7 456.4,69.8 457.1,66.3 457.9,64.3 458.6,63.6 459.3,64.3 460.1,66.4 460.8,69.8 461.6,74.5 462.3,80.4 463.1,87.3 463.8,95.0 464.6,103.0 465.3,110.7 466.0,117.7 466.8,123.3 467.5,127.5 468.3,130.3 469.0,131.5 469.8,131.3 470.5,129.7 471.2,126.7 472.0,122.3 472.7,116.7 473.5,110.0 474.2,102.3 475.0,94.2 475.7,86.3 476.4,79.2 477.2,73.2 477.9,68.7 478.7,65.6 479.4,63.9 480.2,63.7 480.9,64.8 481.6,67.2 482.4,71.0 483.1,76.0 483.9,82.2 484.6,89.3 485.4,97.1 486.1,105.1 486.8,112.7 487.6,119.2 488.3,124.5 489.1,128.2 489.8,130.5 490.6,131.3 491.3,130.6 492.1,128.6 492.8,125.2 493.5,120.5 494.3,114.5 495.0,107.4 495.8,99.5 496.5,91.5 497.3,83.8 498.0,77.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
<polyline points="52.7,159.1 53.5,156.5 54.2,152.3 55.0,146.6 55.7,139.4 56.5,130.8 57.2,120.9 57.9,109.9 58.7,98.1 59.4,86.1 60.2,74.8 60.9,64.8 61.7,56.4 62.4,49.6 63.1,44.5 63.9,41.0 64.6,39.2 65.4,39.1 66.1,40.6 66.9,43.7 67.6,48.3 68.4,54.3 69.1,61.7 69.8,70.3 70.6,80.1 71.3,91.0 72.1,102.3 72.8,113.4 73.6,123.3 74.3,131.5 75.0,137.9 75.8,142.5 76.5,145.4 77.3,146.6 78.0,146.2 78.8,144.2 79.5,140.6 80.2,135.7 81.0,129.5 81.7,122.1 82.5,113.7 83.2,104.4 84.0,94.7 84.7,85.4 85.5,76.8 86.2,69.6 86.9,63.8 87.7,59.5 88.4,56.7 89.2,55.4 89.9,55.6 90.7,57.2 91.4,60.3 92.1,64.7 92.9,70.5 93.6,77.4 94.4,85.4 95.1,94.3 95.9,103.4 96.6,111.9 97.3,119.4 98.1,125.2 98.8,129.5 99.6,132.2 100.3,133.3 101.1,132.9 101.8,131.0 102.5,127.8 103.3,123.3 104.0,117.6 104.8,110.9 105.5,103.3 106.3,95.4 107.0,87.6 107.8,80.5 108.5,74.6 109.2,70.0 110.0,66.9 110.7,65.2 111.5,64.8 112.2,65.9 113.0,68.3 113.7,71.9 114.4,76.8 115.2,82.9 115.9,89.9 116.7,97.5 117.4,105.0 118.2,111.9 118.9,117.7 119.6,122.1 120.4,124.9 121.1,126.3 121.9,126.2 122.6,124.7 123.4,121.9 124.1,117.8 124.8,112.6 125.6,106.4 126.3,99.7 127.1,92.8 127.8,86.3 128.6,80.7 129.3,76.3 130.1,73.3 130.8,71.6 131.5,71.3 132.3,72.3 133.0,74.5 133.8,78.0 134.5,82.6 135.3,88.3 136.0,94.6 136.7,101.1 137.5,107.3 138.2,112.7 139.0,117.0 139.7,119.8 140.5,121.3 141.2,121.3 141.9,120.0 142.7,117.5 143.4,113.7 144.2,108.9 144.9,103.3 145.7,97.2 146.4,91.3 147.1,85.9 147.9,81.4 148.6,78.0 149.4,76.0 150.1,75.3 150.9,75.9 151.6,77.7 152.4,80.7 153.1,84.9 153.8,89.9 154.6,95.4 155.3,100.9 156.1,106.0 156.8,110.5 157.6,113.9 158.3,116.1 159.0,117.0 159.8,116.5 160.5,114.8 161.3,111.8 162.0,107.8 162.8,103.1 163.5,98.1 164.2,93.2 165.0,88.5 165.7,84.5 166.5,81.5 167.2,79.8 168.0,79.4 168.7,80.1 169.4,82.1 170.2,85.1 170.9,89.0 171.7,93.4 172.4,98.1 173.2,102.7 173.9,106.9 174.7,110.3 175.4,112.9 176.1,114.3 176.9,114.5 177.6,113.4 178.4,111.1 179.1,108.0 179.9,104.0 180.6,99.7 181.3,95.2 182.1,90.9 182.8,87.1 183.6,84.1 184.3,82.3 185.1,81.5 185.8,81.8 186.5,83.4 187.3,86.0 188.0,89.4 188.8,93.4 189.5,97.7 190.3,102.0 191.0,105.9 191.7,109.2 192.5,111.5 193.2,112.7 194.0,112.9 194.7,111.9 195.5,109.9 196.2,107.1 197.0,103.5 197.7,99.5 198.4,95.4 199.2,91.5 199.9,88.0 200.7,85.3 201.4,83.4 202.2,82.5 202.9,82.8 203.6,84.0 204.4,86.3 205.1,89.4 205.9,93.1 206.6,97.1 207.4,101.1 208.1,104.8 208.8,107.9 209.6,110.3 210.3,111.8 211.1,112.2 211.8,111.5 212.6,109.8 213.3,107.2 214.0,103.9 214.8,100.2 215.5,96.3 216.3,92.6 217.0,89.2 217.8,86.5 218.5,84.6 219.3,83.7 220.0,83.7 220.7,84.8 221.5,86.8 222.2,89.5 223.0,92.9 223.7,96.6 224.5,100.2 225.2,103.7 225.9,106.8 226.7,109.0 227.4,110.4 228.2,110.9 228.9,110.5 229.7,109.2 230.4,107.0 231.1,104.1 231.9,100.8 232.6,97.3 233.4,93.7 234.1,90.6 234.9,87.9 235.6,85.9 236.3,84.8 237.1,84.5 237.8,85.2 238.6,86.9 239.3,89.3 240.1,92.3 240.8,95.8 241.6,99.4 242.3,102.7 243.0,105.8 243.8,108.3 244.5,110.0 245.3,110.9 246.0,110.8 246.8,109.9 247.5,108.1 248.2,105.6 249.0,102.6 249.7,99.3 250.5,96.0 251.2,92.7 252.0,89.8 252.7,87.5 253.4,86.0 254.2,85.2 254.9,85.4 255.7,86.4 256.4,88.2 257.2,90.7 257.9,93.6 258.6,96.8 259.4,99.9 260.1,103.0 260.9,105.7 261.6,107.8 262.4,109.3 263.1,109.9 263.9,109.5 264.6,108.3 265.3,106.4 266.1,103.8 266.8,100.8 267.6,97.5 268.3,94.3 269.1,91.3 269.8,88.9 270.5,87.1 271.3,86.2 272.0,86.1 272.8,86.9 273.5,88.5 274.3,90.8 275.0,93.5 275.7,96.5 276.5,99.5 277.2,102.3 278.0,104.8 278.7,106.8 279.5,108.1 280.2,108.7 280.9,108.4 281.7,107.4 282.4,105.7 283.2,103.5 283.9,100.8 284.7,97.9 285.4,94.9 286.2,92.1 286.9,89.9 287.6,88.2 288.4,87.1 289.1,86.8 289.9,87.4 290.6,88.7 291.4,90.6 292.1,93.0 292.8,95.6 293.6,98.3 294.3,100.9 295.1,103.1 295.8,105.0 296.6,106.3 297.3,107.0 298.0,107.0 298.8,106.3 299.5,104.9 300.3,103.0 301.0,100.8 301.8,98.3 302.5,95.8 303.2,93.4 304.0,91.2 304.7,89.5 305.5,88.5 306.2,88.2 307.0,88.5 307.7,89.5 308.5,91.1 309.2,93.1 309.9,95.5 310.7,97.9 311.4,100.2 312.2,102.5 312.9,104.4 313.7,105.9 314.4,106.6 315.1,106.7 315.9,106.0 316.6,104.7 317.4,102.9 318.1,100.8 318.9,98.4 319.6,95.9 320.3,93.5 321.1,91.5 321.8,89.8 322.6,88.9 323.3,88.6 324.1,89.0 324.8,90.0 325.5,91.5 326.3,93.4 327.0,95.6 327.8,97.9 328.5,100.0 329.3,102.0 330.0,103.6 330.8,104.8 331.5,105.4 332.2,105.5 333.0,105.1 333.7,104.2 334.5,102.9 335.2,101.2 336.0,99.2 336.7,97.1 337.4,95.2 338.2,93.4 338.9,92.0 339.7,91.1 340.4,90.6 341.2,90.6 341.9,91.1 342.6,92.0 343.4,93.3 344.1,95.0 344.9,96.8 345.6,98.8 346.4,100.6 347.1,102.1 347.8,103.3 348.6,104.0 349.3,104.1 350.1,103.8 350.8,103.0 351.6,101.8 352.3,100.4 353.1,98.9 353.8,97.2 354.5,95.7 355.3,94.2 356.0,93.0 356.8,92.2 357.5,91.7 358.3,91.7 359.0,92.2 359.7,93.1 360.5,94.4 361.2,95.8 362.0,97.4 362.7,98.9 363.5,100.4 364.2,101.7 364.9,102.7 365.7,103.4 366.4,103.6 367.2,103.3 367.9,102.5 368.7,101.4 369.4,100.0 370.1,98.4 370.9,96.9 371.6,95.3 372.4,94.0 373.1,92.8 373.9,92.0 374.6,91.6 375.4,91.7 376.1,92.2 376.8,93.2 377.6,94.5 378.3,95.9 379.1,97.5 379.8,99.1 380.6,100.7 381.3,101.9 382.0,102.7 382.8,103.3 383.5,103.4 384.3,102.9 385.0,102.1 385.8,101.1 386.5,99.8 387.2,98.3 388.0,96.8 388.7,95.3 389.5,94.0 390.2,92.9 391.0,92.1 391.7,91.8 392.4,91.9 393.2,92.5 393.9,93.5 394.7,94.8 395.4,96.3 396.2,98.0 396.9,99.5 397.7,100.8 398.4,101.9 399.1,102.6 399.9,103.0 400.6,103.1 401.4,102.8 402.1,102.3 402.9,101.4 403.6,100.3 404.3,99.0 405.1,97.6 405.8,96.3 406.6,95.1 407.3,94.2 408.1,93.5 408.8,93.2 409.5,93.1 410.3,93.3 411.0,93.7 411.8,94.4 412.5,95.4 413.3,96.5 414.0,97.6 414.7,98.8 415.5,99.9 416.2,100.8 417.0,101.4 417.7,101.7 418.5,101.7 419.2,101.4 420.0,100.8 420.7,100.0 421.4,98.9 422.2,97.8 422.9,96.8 423.7,95.8 424.4,95.0 425.2,94.3 425.9,94.0 426.6,94.0 427.4,94.2 428.1,94.6 428.9,95.4 429.6,96.2 430.4,97.1 431.1,98.1 431.8,98.9 432.6,99.6 433.3,100.2 434.1,100.7 434.8,100.9 435.6,100.8 436.3,100.3 437.0,99.7 437.8,99.1 438.5,98.3 439.3,97.4 440.0,96.6 440.8,95.9 441.5,95.3 442.2,94.8 443.0,94.5 443.7,94.5 444.5,94.7 445.2,95.2 446.0,95.9 446.7,96.6 447.5,97.3 448.2,98.1 448.9,98.9 449.7,99.4 450.4,99.9 451.2,100.2 451.9,100.4 452.7,100.5 453.4,100.4 454.1,100.2 454.9,99.9 455.6,99.5 456.4,99.0 457.1,98.3 457.9,97.6 458.6,96.9 459.3,96.3 460.1,95.8 460.8,95.4 461.6,95.1 462.3,95.0 463.1,95.2 463.8,95.6 464.6,96.2 465.3,96.8 466.0,97.4 466.8,98.2 467.5,98.8 468.3,99.3 469.0,99.7 469.8,100.0 470.5,100.1 471.2,100.1 472.0,100.0 472.7,99.7 473.5,99.4 474.2,98.9 475.0,98.4 475.7,97.7 476.4,97.1 477.2,96.5 477.9,96.1 478.7,95.7 479.4,95.5 480.2,95.3 480.9,95.2 481.6,95.2 482.4,95.3 483.1,95.5 483.9,95.8 484.6,96.2 485.4,96.6 486.1,97.1 486.8,97.6 487.6,98.2 488.3,98.8 489.1,99.2 489.8,99.5 490.6,99.6 491.3,99.6 492.1,99.5 492.8,99.3 493.5,99.0 494.3,98.6 495.0,98.1 495.8,97.5 496.5,96.9 497.3,96.4 498.0,96.0" fill="none" stroke="currentColor" stroke-width="1.6"/>
<text x="492" text-anchor="end" y="45" font-size="11" fill="currentColor">plain wall: 34 Hz limit cycle, 1.66 mm peak to peak</text>
<text x="492" text-anchor="end" y="152" font-size="11" fill="currentColor" font-weight="600">after 1 s: 0.08 mm</text>
<text x="275.0" y="190" font-size="11" fill="currentColor" text-anchor="middle">time (s)</text>
<rect x="52" y="251.8" width="446" height="96.2" fill="currentColor" fill-opacity="0.07"/>
<rect x="52" y="238" width="446" height="110" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="52" y="229" font-size="12.5" fill="currentColor" font-weight="600">observed energy E<tspan dy="3.5" font-size="9.5">obs</tspan><tspan dy="-3.5" dx="3">(mJ), whole 1.5 s</tspan></text>
<text x="46" y="255.8" font-size="11" fill="currentColor" text-anchor="end">0</text>
<text x="46" y="301.6" font-size="11" fill="currentColor" text-anchor="end">−10</text>
<text x="46" y="347.4" font-size="11" fill="currentColor" text-anchor="end">−20</text>
<line x1="52" y1="251.8" x2="498" y2="251.8" stroke="currentColor" stroke-dasharray="2 3" stroke-opacity="0.8"/>
<text x="52.0" y="363" font-size="11" fill="currentColor" text-anchor="middle">0</text>
<text x="200.7" y="363" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
<text x="349.3" y="363" font-size="11" fill="currentColor" text-anchor="middle">1</text>
<text x="498.0" y="363" font-size="11" fill="currentColor" text-anchor="middle">1.5</text>
<text x="275.0" y="378" font-size="11" fill="currentColor" text-anchor="middle">time (s)</text>
<polyline points="52.3,251.8 53.8,251.8 55.3,250.1 56.8,241.4 58.2,241.4 59.7,249.3 61.2,254.2 62.7,254.2 64.2,254.2 65.7,251.5 67.2,244.8 68.7,245.9 70.1,254.6 71.6,256.2 73.1,256.2 74.6,256.2 76.1,250.3 77.6,247.4 79.1,253.1 80.5,258.3 82.0,258.3 83.5,258.3 85.0,255.0 86.5,249.9 88.0,253.3 89.5,260.0 91.0,260.2 92.4,260.2 93.9,257.8 95.4,252.9 96.9,255.1 98.4,261.7 99.9,262.0 101.4,262.0 102.8,259.7 104.3,254.7 105.8,257.5 107.3,263.5 108.8,263.7 110.3,263.7 111.8,261.0 113.3,257.0 114.7,259.9 116.2,265.5 117.7,265.5 119.2,265.5 120.7,262.1 122.2,258.7 123.7,263.2 125.1,267.2 126.6,267.2 128.1,267.0 129.6,262.0 131.1,261.5 132.6,267.3 134.1,268.8 135.6,268.8 137.0,267.5 138.5,262.5 140.0,264.7 141.5,270.1 143.0,270.3 144.5,270.3 146.0,266.9 147.4,264.1 148.9,268.0 150.4,272.0 151.9,272.0 153.4,271.8 154.9,266.8 156.4,266.3 157.9,271.6 159.3,273.5 160.8,273.5 162.3,272.6 163.8,267.3 165.3,269.0 166.8,274.8 168.3,275.2 169.7,275.2 171.2,272.3 172.7,268.9 174.2,272.3 175.7,276.8 177.2,276.8 178.7,276.7 180.2,272.2 181.6,271.1 183.1,276.4 184.6,278.3 186.1,278.3 187.6,277.4 189.1,272.7 190.6,273.8 192.0,279.6 193.5,280.0 195.0,280.0 196.5,277.0 198.0,273.7 199.5,277.0 201.0,281.6 202.5,281.6 203.9,281.6 205.4,276.5 206.9,275.3 208.4,280.8 209.9,283.2 211.4,283.2 212.9,282.5 214.3,277.5 215.8,278.0 217.3,283.9 218.8,284.8 220.3,284.8 221.8,282.8 223.3,278.6 224.8,280.8 226.2,286.3 227.7,286.4 229.2,286.4 230.7,283.0 232.2,280.2 233.7,284.2 235.2,288.1 236.6,288.1 238.1,288.0 239.6,283.0 241.1,282.4 242.6,287.8 244.1,289.7 245.6,289.7 247.1,288.8 248.5,284.0 250.0,285.1 251.5,290.6 253.0,291.3 254.5,291.3 256.0,288.8 257.5,285.0 258.9,287.8 260.4,292.8 261.9,292.9 263.4,292.9 264.9,288.8 266.4,286.6 267.9,291.1 269.4,294.5 270.8,294.5 272.3,294.3 273.8,289.4 275.3,288.8 276.8,294.6 278.3,296.1 279.8,296.1 281.2,294.9 282.7,289.9 284.2,291.6 285.7,297.3 287.2,297.7 288.7,297.7 290.2,294.8 291.7,291.4 293.1,295.4 294.6,299.3 296.1,299.3 297.6,299.1 299.1,294.1 300.6,293.6 302.1,299.3 303.5,300.8 305.0,300.8 306.5,299.5 308.0,294.5 309.5,296.8 311.0,302.1 312.5,302.4 314.0,302.4 315.4,298.9 316.9,296.1 318.4,300.6 319.9,304.0 321.4,304.0 322.9,303.7 324.4,298.4 325.8,298.4 327.3,304.1 328.8,305.7 330.3,305.7 331.8,304.5 333.3,299.4 334.8,301.1 336.3,306.9 337.7,307.3 339.2,307.3 340.7,304.4 342.2,301.0 343.7,304.4 345.2,308.9 346.7,308.9 348.1,308.9 349.6,304.4 351.1,302.7 352.6,308.2 354.1,310.6 355.6,310.6 357.1,309.9 358.6,304.9 360.0,305.4 361.5,311.6 363.0,312.2 364.5,312.2 366.0,309.8 367.5,305.9 369.0,309.3 370.4,313.8 371.9,313.8 373.4,313.8 374.9,309.3 376.4,307.6 377.9,312.6 379.4,315.5 380.9,315.5 382.3,315.2 383.8,309.8 385.3,309.8 386.8,315.6 388.3,317.1 389.8,317.1 391.3,316.2 392.7,310.9 394.2,311.5 395.7,318.2 397.2,318.9 398.7,318.9 400.2,317.0 401.7,312.1 403.2,314.3 404.6,320.3 406.1,320.6 407.6,320.6 409.1,317.7 410.6,313.7 412.1,317.1 413.6,322.2 415.0,322.2 416.5,322.2 418.0,317.6 419.5,315.4 421.0,320.4 422.5,323.8 424.0,323.8 425.5,323.7 426.9,318.1 428.4,317.6 429.9,323.5 431.4,325.5 432.9,325.5 434.4,324.8 435.9,319.2 437.3,319.8 438.8,326.2 440.3,327.1 441.8,327.1 443.3,325.5 444.8,320.3 446.3,322.5 447.8,328.5 449.2,328.8 450.7,328.8 452.2,325.9 453.7,321.9 455.2,325.3 456.7,330.4 458.2,330.4 459.6,330.4 461.1,325.8 462.6,323.6 464.1,328.6 465.6,332.1 467.1,332.1 468.6,331.9 470.1,326.4 471.5,325.8 473.0,331.7 474.5,333.7 476.0,333.7 477.5,333.0 479.0,327.4 480.5,328.0 481.9,334.4 483.4,335.3 484.9,335.3 486.4,333.8 487.9,328.5 489.4,330.8 490.9,336.7 492.4,337.0 493.8,337.0 495.3,334.1 496.8,330.2" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="3 2"/>
<polyline points="52.3,251.8 53.8,251.8 55.3,250.1 56.8,241.4 58.2,241.4 59.7,249.3 61.2,253.6 62.7,253.4 64.2,253.2 65.7,249.3 67.2,244.8 68.7,247.6 70.1,254.0 71.6,253.9 73.1,253.8 74.6,250.4 76.1,247.1 77.6,251.0 79.1,254.5 80.5,254.4 82.0,253.7 83.5,249.3 85.0,250.4 86.5,254.7 88.0,254.9 89.5,254.6 91.0,250.9 92.4,251.4 93.9,255.1 95.4,255.4 96.9,254.7 98.4,251.9 99.9,253.4 101.4,255.7 102.8,255.8 104.3,254.2 105.8,252.4 107.3,255.1 108.8,256.2 110.3,255.9 111.8,253.7 113.3,253.8 114.7,256.2 116.2,256.5 117.7,255.6 119.2,253.6 120.7,255.4 122.2,256.8 123.7,256.7 125.1,255.2 126.6,254.4 128.1,256.3 129.6,257.1 131.1,256.6 132.6,255.1 134.1,255.1 135.6,256.8 137.0,257.3 138.5,256.4 140.0,254.9 141.5,256.1 143.0,257.4 144.5,257.3 146.0,256.0 147.4,255.6 148.9,257.1 150.4,257.7 151.9,257.4 153.4,255.8 154.9,256.2 156.4,257.5 157.9,257.8 159.3,257.0 160.8,255.9 162.3,257.1 163.8,257.9 165.3,257.7 166.8,256.9 168.3,256.5 169.7,257.6 171.2,258.0 172.7,257.6 174.2,256.7 175.7,257.1 177.2,258.0 178.7,258.1 180.2,257.6 181.6,256.9 183.1,257.7 184.6,258.4 186.1,258.0 187.6,257.5 189.1,257.5 190.6,258.4 192.0,258.4 193.5,257.9 195.0,257.6 196.5,258.0 198.0,258.5 199.5,258.5 201.0,258.1 202.5,257.8 203.9,258.4 205.4,258.7 206.9,258.5 208.4,257.9 209.9,258.2 211.4,258.5 212.9,258.5 214.3,258.5 215.8,258.3 217.3,258.3 218.8,258.6 220.3,258.6 221.8,258.4 223.3,258.4 224.8,258.4 226.2,258.4 227.7,258.7 229.2,258.7 230.7,258.4 232.2,258.4 233.7,258.4 235.2,258.7 236.6,258.7 238.1,258.5 239.6,258.5 241.1,258.5 242.6,258.8 244.1,258.8 245.6,258.5 247.1,258.5 248.5,258.5 250.0,258.8 251.5,258.8 253.0,258.5 254.5,258.6 256.0,258.6 257.5,258.9 258.9,258.9 260.4,258.6 261.9,258.6 263.4,258.6 264.9,258.9 266.4,258.9 267.9,258.7 269.4,258.7 270.8,258.7 272.3,259.0 273.8,259.0 275.3,258.7 276.8,258.7 278.3,259.0 279.8,259.0 281.2,258.8 282.7,258.8 284.2,258.8 285.7,259.1 287.2,259.1 288.7,258.8 290.2,258.8 291.7,258.8 293.1,259.1 294.6,259.1 296.1,258.9 297.6,258.9 299.1,258.9 300.6,259.2 302.1,259.2 303.5,258.9 305.0,258.9 306.5,258.9 308.0,259.2 309.5,259.2 311.0,258.9 312.5,258.9 314.0,259.3 315.4,259.3 316.9,259.0 318.4,259.0 319.9,259.0 321.4,259.3 322.9,259.3 324.4,259.0 325.8,259.0 327.3,259.0 328.8,259.3 330.3,259.3 331.8,259.1 333.3,259.1 334.8,259.1 336.3,259.4 337.7,259.4 339.2,259.1 340.7,259.1 342.2,259.1 343.7,259.4 345.2,259.4 346.7,259.2 348.1,259.2 349.6,259.5 351.1,259.5 352.6,259.2 354.1,259.2 355.6,259.2 357.1,259.5 358.6,259.5 360.0,259.2 361.5,259.2 363.0,259.2 364.5,259.6 366.0,259.6 367.5,259.3 369.0,259.3 370.4,259.3 371.9,259.6 373.4,259.6 374.9,259.3 376.4,259.3 377.9,259.3 379.4,259.6 380.9,259.6 382.3,259.4 383.8,259.4 385.3,259.7 386.8,259.7 388.3,259.4 389.8,259.4 391.3,259.4 392.7,259.7 394.2,259.7 395.7,259.5 397.2,259.5 398.7,259.5 400.2,259.8 401.7,259.8 403.2,259.5 404.6,259.5 406.1,259.5 407.6,259.8 409.1,259.8 410.6,259.5 412.1,259.5 413.6,259.5 415.0,259.9 416.5,259.9 418.0,259.6 419.5,259.6 421.0,259.9 422.5,259.9 424.0,259.6 425.5,259.6 426.9,259.6 428.4,259.9 429.9,259.9 431.4,259.7 432.9,259.7 434.4,259.7 435.9,260.0 437.3,260.0 438.8,259.7 440.3,259.7 441.8,259.7 443.3,260.0 444.8,260.0 446.3,259.8 447.8,259.8 449.2,259.8 450.7,260.1 452.2,260.1 453.7,259.8 455.2,259.8 456.7,260.1 458.2,260.1 459.6,259.9 461.1,259.9 462.6,259.9 464.1,260.2 465.6,260.2 467.1,259.9 468.6,259.9 470.1,259.9 471.5,260.2 473.0,260.2 474.5,259.9 476.0,259.9 477.5,259.9 479.0,260.2 480.5,260.2 481.9,260.0 483.4,260.0 484.9,260.0 486.4,260.3 487.9,260.3 489.4,260.0 490.9,260.0 492.4,260.3 493.8,260.3 495.3,260.1 496.8,260.1" fill="none" stroke="currentColor" stroke-width="1.6"/>
<text x="502" y="336.4" font-size="11" fill="currentColor">−17.6</text>
<text x="502" y="264.1" font-size="11" fill="currentColor" font-weight="600">−1.8</text>
<text x="60" y="336.5" font-size="11" fill="currentColor" fill-opacity="0.85">E<tspan dy="3.5" font-size="9.5">obs</tspan><tspan dy="-3.5" dx="3">&lt; 0: the wall has produced energy</tspan></text>
<line x1="52" y1="394" x2="78" y2="394" stroke="currentColor" stroke-width="1.6"/><text x="84" y="398" font-size="11" fill="currentColor">with observer and controller, α ≤ 0.8 N·s/m</text>
<line x1="52" y1="412" x2="78" y2="412" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="3 2"/><text x="84" y="416" font-size="11" fill="currentColor">plain sampled wall</text>
</svg>

The same $2500\,\mathrm{N/m}$ wall, sampled at $1\,\mathrm{kHz}$, under the same light fingertip. Left alone (dashed), it rings in a $34\,\mathrm{Hz}$ limit cycle and the energy counted at its port falls steadily: the wall is producing energy. With a passivity observer and controller (solid), the first impact is unchanged, but from then on every deficit the counter sees is paid back as a brief damping force, and the handle settles.

### 1. Three blocks, two loops

Salisbury, Conti and Barbagli divide every haptic rendering program into three blocks. **Collision detection** finds whether and where the device's avatar touches something. **Force response** computes the force an ideal interaction would produce. **Control** turns that ideal force into the force the device can actually produce, within its limits. One servo period runs them in order: read the joint sensors, compute the avatar's pose by forward kinematics, detect collisions, compute the response, command the actuators through $J^\top$ ([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]), and hand the same forces to the simulation so that the virtual objects react. Srinivasan and Basdogan draw the same pipeline as a second sensorimotor loop — encoders, computer, motors — meeting the human's own loop of skin and joint sensors, brain and muscles at the handle.

A real program runs these blocks at two rates, because the eye and the hand need different things. The **graphics loop** redraws the scene at $30$–$60\,\mathrm{Hz}$, which is all vision needs. The **haptic loop** runs at $1\,\mathrm{kHz}$ or faster, on its own thread at high priority, because a sampled spring leaks energy in proportion to $T$ (24.4 §2) and because the skin feels transients to several hundred hertz. Open-source libraries such as CHAI3D are organized exactly this way: the main thread owns the window and the scene graph, and a haptic thread reads the device, computes the contact force for each object in the object's own frame, rotates it to the world frame and commands it, every tick. The rule that follows is the most practical sentence on this page: **nothing slow or blocking runs in the haptic loop** — no file or console output, no memory allocation, no waiting on a lock the graphics thread holds, no network call. A tick that runs late is a tick with a longer $T$, and the bound $2b/T$ does not care why.

When the geometry is too complex to query at a kilohertz, the two rates are bridged by an intermediate object.

> **Intermediate representation, defined.** An **intermediate representation** is a *local, simple stand-in for the geometry*, computed by the slow loop and rendered by the fast one (Adachi, Kumano and Ogino 1995). Three conditions define it. It is **local**: valid only near the current contact, typically a plane or a sphere tangent to the surface there. It is **computed slowly**: the collision and geometry loop updates it at tens to hundreds of hertz. And it is **rendered at the servo rate**: every tick, the haptic loop computes the force against the stand-in from the newest device position.
>
> - **Example**: a tangent plane updated at $30\,\mathrm{Hz}$ while the force is computed from it at $1\,\mathrm{kHz}$. A probe sliding at $0.1\,\mathrm{m/s}$ moves $3.3\,\mathrm{mm}$ between plane updates, so the plane is wrong by whatever the surface curves over $3.3\,\mathrm{mm}$ — but the *force* is fresh every millisecond, so the stiffness the sampling bound sees is still the $1\,\mathrm{kHz}$ one.
> - **Non-example**: the slow loop computing the force itself and passing it on. That force is held for the slow loop's whole period, which is §2's failure at a larger $T$.
> - **Why it matters**: it separates what must be fast (the force, for stability) from what may be slow (the geometry, for accuracy), which is how complex scenes and surgical simulators reach a kilohertz at all. Its cost is visible at the updates: if the probe moves far before the stand-in catches up, the force jumps (Srinivasan and Basdogan).

Ruspini, Kolarov and Khatib made the same split for the proxy of [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 §3]]: a low-level controller drives the device toward the proxy at the servo rate, and the proxy is updated separately. If the update falls behind, objects feel *sticky* — the proxy lags — rather than unstable. That is the right way for a haptic program to fail.

### 2. Where the force is computed sets $T$

The $T$ in every bound is the period at which the *force command changes*, not the period at which something is sampled. On a desktop device driven by a real-time thread they are the same. On a one-degree-of-freedom kit driven by a hobby microcontroller they often are not: a timer interrupt at $1\,\mathrm{kHz}$ reads the encoder and applies the latest motor command, while the force law itself sits in the main loop together with serial printing and a pause. The interrupt then applies the same force for as long as the main loop takes, and the effective $T$ is the main-loop period. At $5\,\mathrm{ms}$ the bound is $2b/T=2(0.8)/0.005=320\,\mathrm{N/m}$, and the catalog wall of $400\,\mathrm{N/m}$, comfortable at $1\,\mathrm{kHz}$, now rings (Worked case, run D). Compute the force in the same interrupt that reads the encoder, or at least measure how often the command actually changes — toggle a pin each time it does and look at it on an oscilloscope — before trusting any stiffness number.

Resolution sets the second limit. One count of P3 is $61.4\,\mathrm{\mu m}$, so the difference quotient $(\hat x_k-\hat x_{k-1})/T$ can only report multiples of $61.4\,\mathrm{mm/s}$ at $1\,\mathrm{kHz}$. A hand moving at $10\,\mathrm{mm/s}$ produces one count every $6.1$ ticks: the estimate reads $0$ five times and $61.4\,\mathrm{mm/s}$ once. A virtual damper $B=0.4\,\mathrm{N{\cdot}s/m}$ fed by that estimate renders force pulses of $0.025\,\mathrm{N}$ instead of a smooth $0.004\,\mathrm{N}$. The first-order filter of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]] at $f_c=20\,\mathrm{Hz}$ (coefficient $e^{-2\pi f_cT}=0.882$) smooths the pulses at the cost of a time constant of $8.0\,\mathrm{ms}$, and lag in a damper is exactly what 24.4 warns can destabilize it. There is no free choice here, only a stated one.

A third trap is units. Microcontroller code usually works in encoder counts and PWM duty, so a "stiffness" there is duty per count. It becomes $\mathrm{N/m}$ only through the motor's torque constant, the amplifier's gain and the transmission of 24.3 — and until it does, it cannot be compared with any bound.

### 3. The one-degree-of-freedom effect library

On a one-degree-of-freedom handle every effect is a force law, and the programming question is which state the law needs the loop to keep. The table is the library a lab course builds effect by effect; each row names what limits it on P3.

| Effect | Force law | State the loop keeps | What limits it on P3 |
|---|---|---|---|
| Spring (both directions) | $F=-k(x-x_0)$ | none | $k<2b/T$; one count is $k\,\Delta x$ newtons |
| Wall (one direction) | $F=-k_w(x-x_w)$ if $x>x_w$, else $0$ | none, but it switches | the same bound, plus the two leaks of §5 |
| Damper | $F=-B\hat v$ | last position, filter state | velocity quantum and filter lag (§2); $B<b$ from 24.4 §2 with $K=0$ |
| Friction with sticking | Karnopp law, [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms\|24.7 §5]] | stuck or slipping | the stick band $D_v$ cannot be finer than one count per tick, $61.4\,\mathrm{mm/s}$ |
| Bump or valley | $F=-A\,h'(x)$ for a height profile $h$ | none | force alone conveys the shape (24.7 §6); it must depend on position only, so it feels the same in both directions |
| Hard surface | wall plus an open-loop transient at contact, $F=A\,v_{\text{in}}e^{-t/\tau}\sin(2\pi ft)$ | contact latch, impact time, $v_{\text{in}}$ | amplifier limit; transients must not make the surface feel active (24.7 §4) |
| Virtual mass on a coupling | $m_v\ddot x_v=k_c(x-x_v)+b_c(\dot x-\dot x_v)+\ldots$, device feels the opposite | $x_v,\ \dot x_v$ integrated every tick | integrator step $\omega_cT$; coupling bound below |

Two rows need numbers. For a Gaussian bump $h(x)=e^{-(x-x_b)^2/2\sigma^2}$, the lateral force $-A\,h'(x)$ peaks at $x_b\pm\sigma$ with magnitude $A/(\sigma\sqrt e)$; a $0.5\,\mathrm{N}$ bump of width $\sigma=2\,\mathrm{mm}$ needs $A=0.5\cdot0.002\cdot\sqrt e=1.65\times10^{-3}\,\mathrm{J}$ — pushing uphill costs the same energy $A$ whichever side you come from, which is the "same feel in both directions" condition stated as physics. For the virtual mass, a $0.05\,\mathrm{kg}$ ball on a $1000\,\mathrm{N/m}$ coupling resonates at $\frac{1}{2\pi}\sqrt{1000/0.05}=22.5\,\mathrm{Hz}$, and the semi-implicit Euler step is stable for $\omega_cT<2$; here $\omega_cT=0.14$.

The last row is the general pattern for anything with dynamics of its own, and it has a name.

> **Virtual coupling, defined.** A **virtual coupling** is a *spring–damper $(k_c, b_c)$ placed between the device and a simulated object*, so that the device feels only the coupling and the simulation feels only the coupling's equal and opposite force (Colgate, Stanley and Brown 1995; Adams and Hannaford 1999). Three conditions define it. The environment has **its own state**, integrated by the simulation; the coupling is the **only** path from device to environment; and $(k_c, b_c)$ are chosen so that the coupling **alone** satisfies the sampled-data bound, $k_c<2(b-b_c)/T$.
>
> - **Example**: the virtual ball above with $b_c=0.2\,\mathrm{N{\cdot}s/m}$: the bound is $2(0.8-0.2)/0.001=1200\,\mathrm{N/m}$, so $k_c=1000\,\mathrm{N/m}$ passes whatever the ball collides with inside the simulation — a rigid floor included.
> - **Non-example**: a wall with entry-only damping. It has no simulated state behind it; it is an effect, and the bound applies to its own $k_w$.
> - **Why it matters**: it lets the environment be arbitrarily stiff or complex while the device renders only something it can render passively. The price is the ceiling: through a coupling the hand never feels anything stiffer than $k_c$. The PD coupling between two devices in [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §3]] is the same object, and its $Z+C$ ceiling is the same fact.

### 4. Surfaces beyond a half-space

A half-space has one normal. Everything else needs a way to find the surface point and its normal every tick.

**Implicit surfaces.** Salisbury and Tarr render a surface given as $S(p)=0$, with $S<0$ inside. Contact begins when $S(p)<0$ at the device point. The surface point is found by **seeding**: repeat the Newton step along the gradient,

$$\delta p=-\frac{S(p)\,\nabla S(p)}{\nabla S(p)\cdot\nabla S(p)},\qquad p\leftarrow p+\delta p,$$

until $\lVert\delta p\rVert$ is below a tolerance. For a sphere $S=x^2+y^2+z^2-r^2$ with $r=20\,\mathrm{mm}$ and a device point $15\,\mathrm{mm}$ from the centre, $S=-1.75\times10^{-4}\,\mathrm{m^2}$ and $\lVert\nabla S\rVert=0.030\,\mathrm{m}$, so the first step moves the point out by $5.83\,\mathrm{mm}$ to $20.83\,\mathrm{mm}$; the next two land at $20.017$ and $20.00001\,\mathrm{mm}$. Once in contact, the algorithm **tracks** instead of re-seeding from scratch: each tick it uses the tangent plane at the last surface point as a constraint for the new device point, projects onto it, and re-seeds from there, converging over a few ticks; contact ends when the device point leaves the plane's inside. Two shapes defeat it. Thin objects let the device point cross to where the nearest surface is the far one, as in 24.7 §2, and strongly concave regions can make the seed alternate between two nearby surface points — a limit cycle the hand feels as buzzing.

**Force shading.** A polygon mesh has a normal that jumps at every edge. Morgenbesser and Srinivasan interpolate the vertex normals across each face, as Phong shading does for light, so the force direction turns smoothly. Ruspini's proxy implements it in two passes: first with planes through the contact point normal to the *interpolated* normal, giving a sub-goal; then with the true planes, starting from that sub-goal. On a ten-sided polygon around a circle the unshaded force direction jumps $36^\circ$ at each edge and pulls sideways across each face; shaded, it does neither. The price is small: because the constraint planes no longer match the geometry, a shaded surface can return slightly more energy than it received.

**Texture by perturbing the normal.** Srinivasan and Basdogan adapt graphics bump mapping: keep the geometry, and tilt the force direction by the gradient of a height field $h$ on the surface,

$$M=N-\nabla h+(\nabla h\cdot N)\,N,$$

which subtracts from the unit normal $N$ the tangential part of $\nabla h$. For a grating $h=a\sin(2\pi s/\lambda)$ with $a=0.1\,\mathrm{mm}$ and $\lambda=2\,\mathrm{mm}$, the steepest slope is $2\pi a/\lambda=0.314$, so the force tilts by up to $17.4^\circ$: under a $1\,\mathrm{N}$ normal push the hand feels a $0.30\,\mathrm{N}$ lateral component alternating in sign, at $25\,\mathrm{Hz}$ when stroking at $50\,\mathrm{mm/s}$. Moving the geometry itself (displacement mapping) is more faithful and costs a collision query per bump. The height field can come from an image (grey level as height) or from a procedure — Fourier series, noise, fractals or stochastic models.

### 5. Two energy leaks at the wall

Gillespie and Cutkosky named the two mechanisms by which a sampled wall produces energy that a real wall cannot, and both are visible in the dashed curve of the picture.

**The zero-order hold.** The force computed from a sample is held for a whole period. Moving *in*, the sampled position lags behind the true one, so the held force is too small; moving *out*, the sampled position is still deeper than the true one, so the force is too large. Pressing costs less work than on a real wall, and releasing returns more. For a wall in steady contact the arithmetic is exact: with $y_k=\hat x_k-x_w$ and the held force $-k_wy_k$ acting over the step $y_{k+1}-y_k$, the energy put into the wall is

$$\sum_k k_w\,y_k\,(y_{k+1}-y_k)=\tfrac12k_w\big(y_n^2-y_0^2\big)-\tfrac12k_w\sum_k(y_{k+1}-y_k)^2,$$

the continuous spring's energy *minus* $\tfrac12k_w\sum\Delta y^2$ — a leak on every step, whether the handle moves in or out.

**Asynchronous switching.** A wall is a switch, and the switch can only change at sample times. It turns on one sample late, with the spring already compressed — stored energy that no one did work to store. And the last in-wall sample's force still pushes outward during a period in which the handle has already left.

Their test bed was a bouncing ball — a manipulandum of $0.35\,\mathrm{kg}$ and a finger of $0.006\,\mathrm{kg}$ and $500\,\mathrm{N/m}$, no damping, a $5000\,\mathrm{N/m}$ floor sampled every $10\,\mathrm{ms}$ — and the sampled ball bounced higher on every strike. They removed the hold's leak in two ways: **half-sample prediction**, which evaluates the wall law at the position predicted $T/2$ ahead using a model of hand and device; and **design in the digital domain**, which places the closed-loop poles of the discretized plant at the zero-order-hold equivalent of the continuous target. They removed the switching leak with a **watchdog and deadbeat correction**: from the samples around a crossing, compute where on-threshold switching would have left the state at the first sample outside, and choose the last two held forces to drive the second-order system exactly there.

The assumptions are the lesson. Chatter, they observed, typically runs at $10$–$50\,\mathrm{Hz}$, far above what a person commands on purpose, and people induce it not by shaking but by holding a fixed grip against the wall; the same wall may chatter under one person's fingers and not another's. So over the roughly $30\,\mathrm{ms}$ before reflexes, the finger can be modelled as a second-order linear system, identified with the same device just before rendering. The page's limit cycle sits at $34\,\mathrm{Hz}$, inside their band. Their own caution belongs with the result: the compensated walls feed back velocity as well as position, so comparing them with undamped walls flatters them, and the first experiments were qualitative.

### 6. Time-domain passivity: count the energy, then pay it back

Hannaford and Ryu replaced the model with a measurement. Whatever the reason a block produces energy — a hold, a switch, a delay, a friction compensator — the energy it has produced so far can be counted from the force and velocity at its port. Think of it as a bank balance kept for the wall. Every tick, the work the hand pushes into the wall is deposited and the work the wall pushes back is withdrawn; a real, passive wall can never be overdrawn, because it can only return what it was given. The **observer** is the balance, and the **controller** is the rule that, whenever the balance goes negative, charges exactly the overdraft back as a brief damping force.

> **Passivity observer and passivity controller, defined.** With the sign convention that power *into* a port is positive and zero initial stored energy, the **passivity observer** (PO) is the running sum
>
> $$E_{\text{obs}}(n)=T\sum_{k=0}^{n}f(k)\,v(k),$$
>
> and the port has been passive up to sample $n$ exactly when $E_{\text{obs}}(n)\ge0$; a negative value is the energy the block has produced. The **passivity controller** (PC) is an *adaptive damper* at the same port that absorbs exactly that deficit. For impedance causality (velocity in, force out) it is placed in series: with $f_e(n)$ the block's own force and $W(n)=E_{\text{obs}}(n-1)+f_e(n)v(n)T$,
>
> $$\alpha(n)=\begin{cases}-\dfrac{W(n)}{T\,v(n)^2}, & W(n)<0\\[4pt] 0, & W(n)\ge0\end{cases},\qquad f(n)=f_e(n)+\alpha(n)\,v(n).$$
>
> Admittance causality uses the dual, parallel form.
>
> - **Example**: run C of the Worked case. The PC acts on $374$ of $1500$ ticks, never above $0.20\,\mathrm{N}$, and the $1.66\,\mathrm{mm}$ limit cycle becomes $0.08\,\mathrm{mm}$.
> - **Non-example**: a virtual coupling sized for the worst case (§3). It is passive by design and costs its damping on every tick, including the many on which nothing needed dissipating.
> - **Non-example**: the same observer summing each force against the displacement *before* it was computed. It reports the wall of run B as dissipating $26.6\,\mathrm{mJ}$ when it produced $17.6$, and its controller never acts (below).
> - **Why it matters**: it needs no model of the device, the hand or the environment — only the two signals at one port — and it dissipates only when, and only as much as, the count says. The same observer on a delayed channel is [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §7]].

**Which displacement goes with which force.** The formula $f(k)v(k)T$ leaves open what $v(k)$ is, and on a sampled wall that choice decides whether the observer sees the leak at all. The force computed at sample $k$ is held over the *next* step, so the honest pairing is $f(k)\,(\hat x_{k+1}-\hat x_k)$ — the sum of §5, which shows the leak. Pair the same force with a backward-difference velocity taken at the same sample, $f(k)\,(\hat x_k-\hat x_{k-1})$, and the same algebra gives

$$\sum_k k_w\,y_k\,(y_k-y_{k-1})=\tfrac12k_w\big(y_n^2-y_0^2\big)+\tfrac12k_w\sum_k(y_k-y_{k-1})^2:$$

the leak appears with the *opposite* sign, as dissipation. Hannaford and Ryu confine their analysis to sampling fast enough that force and velocity change little from one sample to the next, and there the two pairings agree; a wall past the sampling bound is exactly where that assumption fails. The lab's observer therefore adds, at each tick, the work of the force that was *held* over the step just finished, and its controller uses that count in place of $W(n)$.

Their evidence was the Excalibur, a three-axis device running synchronously at $1\,\mathrm{kHz}$, with $0.1\,\mathrm{mm}$ position resolution, up to $200\,\mathrm{N}$ of force and a force resolution of $0.096\,\mathrm{N}$. Touching a $90\,\mathrm{kN/m}$ virtual block at about $200\,\mathrm{mm/s}$ without the PC gave sustained contact oscillation; the observer showed the first bounce passive and the later, smaller bounces active. With the PC the contact settled in about six bounces, the controller acting from the fourth, with less than $40\,\mathrm{N}$ of PC force — and limiting that force to $20\,\mathrm{N}$ changed almost nothing. Slowing the virtual environment to $66.7\,\mathrm{Hz}$ (each force held for $15$ samples) at $30\,\mathrm{kN/m}$ made contact violently unstable, with $200\,\mathrm{N}$ force pulses; with the PC it settled within one bounce. Instrumenting the device's own blocks showed that most of the active behaviour came from its Coulomb friction compensation, not from the wall.

The limitations are as specific. At low velocity, $\alpha=-W/(Tv^2)$ becomes enormous: uncapped on P3, the lab's controller asks for up to $2394\,\mathrm{N{\cdot}s/m}$ — a $147\,\mathrm{N}$ force from a $2\,\mathrm{N}$ amplifier — and velocity noise is amplified the same way. In their own slowed-environment run, the controller's output turned noise-like while the handle was nearly still, and the user felt and heard it for about half a second. So $\alpha$ or the PC force is capped, and the deficit a capped controller cannot pay is carried into later samples; in the lab, capping at $0.8$ leaves $0.08\,\mathrm{mm}$, capping at $0.4$ leaves $1.01\,\mathrm{mm}$. Dissipation accumulated in one place can mask activity in another, since the observer is a single sum; the authors propose resetting it, for example during free motion. And an observer on the wall port alone is conservative: in run A the catalog wall's port produces $0.32\,\mathrm{mJ}$ while the device's own damper dissipates more, so the loop is stable yet the controller would act. Their remedy is to credit known dissipation outside the port, replacing the zero threshold with $-b\,T\sum v^2$.

### Worked case · 대상으로 한 번 끝까지

Five runs on the Running object, each $1.5\,\mathrm{s}$; the peak is the deepest the handle goes, the tail is the peak-to-peak motion over the last $0.5\,\mathrm{s}$, and $E_{\text{obs}}$ is the observed energy at the wall port at the end. The lab code computes all of it.

| Run | Wall | Force updated every | PO/PC | Peak | Tail | $E_{\text{obs}}$ |
|---|---|---|---|---:|---:|---:|
| A | $400\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | off | $33.53\,\mathrm{mm}$ | $0.001\,\mathrm{mm}$ | $-0.32\,\mathrm{mJ}$ |
| B | $2500\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | off | $31.79\,\mathrm{mm}$ | $1.658\,\mathrm{mm}$ | $-17.6\,\mathrm{mJ}$ |
| C | $2500\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | on, $\alpha\le0.8$ | $31.79\,\mathrm{mm}$ | $0.080\,\mathrm{mm}$ | $-1.81\,\mathrm{mJ}$ |
| D | $400\,\mathrm{N/m}$ | $5\,\mathrm{ms}$ | off | $34.07\,\mathrm{mm}$ | $5.277\,\mathrm{mm}$ | $-69.7\,\mathrm{mJ}$ |
| E | $400\,\mathrm{N/m}$ | $5\,\mathrm{ms}$ | on, $\alpha\le0.8$ | $33.90\,\mathrm{mm}$ | $0.001\,\mathrm{mm}$ | $-1.44\,\mathrm{mJ}$ |

**Step 1 — the catalog wall is stable, and its port is not passive.** Run A settles at $31.52\,\mathrm{mm}$, where the fingertip spring and the wall spring balance: $x^\ast=(400\cdot0.033+400\cdot0.030)/800=0.0315\,\mathrm{m}$, a wall force of $0.60\,\mathrm{N}$. The observer still ends at $-0.32\,\mathrm{mJ}$: the hold leaks on every step, and the device's damper $b$, outside the observed port, dissipates more. Stable does not require every port to be passive — only the loop.

**Step 2 — past the bound, a limit cycle.** At $2500\,\mathrm{N/m}$ the bound $2b/T=1600\,\mathrm{N/m}$ is exceeded and, with no damping in the fingertip, nothing covers the leak. The handle bounces between $29.62$ and $31.28\,\mathrm{mm}$ at $34\,\mathrm{Hz}$ — leaving the wall by $0.38\,\mathrm{mm}$ each cycle, which is why the oscillation cannot grow without bound: outside the wall the leak stops. The wall produces $17.6\,\mathrm{mJ}$ in $1.5\,\mathrm{s}$, an average of $11.7\,\mathrm{mW}$, or about $0.35\,\mathrm{mJ}$ per cycle. §5's hold leak $\tfrac12k_w\sum\Delta y^2$, summed over the in-contact steps of the last second on which the amplifier was not clipping, gives $11.9\,\mathrm{mJ}$ against the $11.1\,\mathrm{mJ}$ the observer counts in that second: the hold accounts for nearly all of it. On $365$ of those $1000$ ticks the force sat at the $2\,\mathrm{N}$ limit, and a clipped force is constant, so holding it loses nothing.

**Step 3 — the observer and controller.** Run C reaches the same peak, $31.79\,\mathrm{mm}$: the first impact is untouched, because the controller cannot act before the observer has seen a deficit. From then on the deficits are paid back in damping pulses of at most $0.20\,\mathrm{N}$, and the handle settles to within $0.1\,\mathrm{mm}$ of $30.47\,\mathrm{mm}$ by $0.52\,\mathrm{s}$ (the equilibrium is $30.41\,\mathrm{mm}$; one count of quantization accounts for the rest). The observer ends at $-1.81\,\mathrm{mJ}$, not $0$: the cap means some deficits are paid late, and a small remainder is never paid. With the same-sample pairing of §6 the observer reads $+26.6\,\mathrm{mJ}$, the controller never acts, and the tail stays at $1.658\,\mathrm{mm}$.

**Step 4 — the slow force loop.** Run D is the catalog wall that passed in run A, with only one change: the force is recomputed every fifth tick. The bound falls to $320\,\mathrm{N/m}$, the handle rings at $21\,\mathrm{Hz}$ between $28.8$ and $34.1\,\mathrm{mm}$, and the wall produces $69.7\,\mathrm{mJ}$ — the worst run on the page, at the stiffness that was fine. Run E adds the observer and controller, and the handle settles as fast as run A did ($0.43$ against $0.41\,\mathrm{s}$ to stay within $0.1\,\mathrm{mm}$).

**Step 5 — what the numbers license.** The controller turns an energy count into stability without any model, but it does not make the wall stiffer, it does not change the first impact, and it spends the $0.8\,\mathrm{N{\cdot}s/m}$ cap on a device whose own damping is $0.8$. Run D is the cheaper fix to know first: move the force law into the servo interrupt, and the problem the controller was solving disappears.

### After reading

- [ ] Name the three blocks of a rendering loop, say which run in the fast loop and which may run slowly, and define an intermediate representation with its cost.
- [ ] Explain why the $T$ in the sampling bound is the period of the force command, and compute the bound when the force is recomputed at $200\,\mathrm{Hz}$.
- [ ] For each effect in the library, write the force law and the state the loop must keep.
- [ ] State the virtual-coupling bound $k_c<2(b-b_c)/T$ and the ceiling a coupling puts on felt stiffness.
- [ ] Run the implicit-surface seeding step by hand for a sphere, and say which shapes defeat surface tracking.
- [ ] Derive the zero-order-hold leak $\tfrac12k_w\sum\Delta y^2$, and name the second, switching leak.
- [ ] Write the passivity observer and series controller, and explain why the pairing of force and displacement decides whether the observer sees the leak.

### Self-check

1. A haptic program logs every contact force to a file from inside its haptic loop, and a wall that was stable becomes buzzy when the disk is busy. What happened, in terms of 24.4's bound?
2. Why does a proxy whose update falls behind feel sticky rather than unstable?
3. On P3 at $1\,\mathrm{kHz}$, what is the smallest nonzero speed a difference quotient can report, and what does a virtual damper fed by it do when the hand moves at $10\,\mathrm{mm/s}$?
4. Through a virtual coupling with $k_c=1000\,\mathrm{N/m}$, a simulated ball hits a perfectly rigid simulated floor. What stiffness does the hand feel, and why is the loop stable?
5. Which of the two leaks of §5 would half-sample prediction alone leave in place, and what removes it?
6. In run C the controller's damping is capped at $0.8\,\mathrm{N{\cdot}s/m}$. Why not leave it uncapped, and what does the cap cost?

> [!tip]- Answers
> 1. File output can block for milliseconds, and during a blocked tick the last force is held, so the effective $T$ grows and $2b/T$ shrinks below the wall's stiffness. The fix is to hand the data to another thread through a buffer that never blocks the haptic thread.
> 2. The servo loop still drives the device toward the proxy every tick with a stiffness it can render; only the proxy's position is stale, so the hand is held back at an old point — a drag — rather than fed energy.
> 3. One count per tick, $61.4\,\mathrm{mm/s}$. At $10\,\mathrm{mm/s}$ a count arrives every $6.1$ ticks, so the estimate is $0$ five times and $61.4\,\mathrm{mm/s}$ once, and a damper $B=0.4$ renders $0.025\,\mathrm{N}$ pulses instead of a steady $0.004\,\mathrm{N}$.
> 4. At most $k_c=1000\,\mathrm{N/m}$: the floor and the coupling are in series, and a rigid floor leaves only the coupling. The loop is stable because the device renders only the coupling, and $1000<2(0.8-0.2)/0.001=1200\,\mathrm{N/m}$ whatever the simulation contains.
> 5. The switching leak — the wall turns on late with the spring compressed and pushes for one period after exit. Gillespie and Cutkosky remove it with a watchdog that computes the on-threshold exit state and a deadbeat choice of the last two held forces.
> 6. Uncapped, $\alpha=-W/(Tv^2)$ grows without bound as $v$ approaches one count per tick: on P3 it reaches $2394\,\mathrm{N{\cdot}s/m}$ and asks the $2\,\mathrm{N}$ amplifier for $147\,\mathrm{N}$, and it amplifies velocity noise. The cap costs completeness: deficits are paid late or not at all, so the observer ends at $-1.81\,\mathrm{mJ}$ instead of $0$, and a lower cap ($0.4$) leaves a $1.01\,\mathrm{mm}$ oscillation.

### Problem set · 과제

Tier A. Plant **P3** from [[02-foundations/lab-plants|0.6]], the fingertip, wall and cap of the Running object, and the sampling bound of [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]. The lab code simulates the continuous handle in $40$ sub-steps per servo period and holds the force between servo ticks.

1. **Draw.** The picture above for the slow force loop instead of the stiff wall — runs D and E, the catalog $400\,\mathrm{N/m}$ wall with the force recomputed every $5\,\mathrm{ms}$: in the top panel sketch $x(t)$ for the first $0.6\,\mathrm{s}$ with and without the observer and controller, marking the wall and the equilibrium; in the bottom panel sketch $E_{\text{obs}}(t)$ over $1.5\,\mathrm{s}$ for both, with the two end values written in.
2. **Derive.** (a) The identity $\sum_k y_k(y_{k+1}-y_k)=\tfrac12(y_n^2-y_0^2)-\tfrac12\sum_k(y_{k+1}-y_k)^2$. (b) The largest wall stiffness that passes 24.4's bound on P3 when the force is recomputed every $2\,\mathrm{ms}$, and every $5\,\mathrm{ms}$. (c) The first two seeding steps for the $20\,\mathrm{mm}$ sphere of §4 from a device point $12\,\mathrm{mm}$ from the centre. (d) The largest coupling damping $b_c$ that still allows $k_c=1000\,\mathrm{N/m}$ on P3 at $1\,\mathrm{kHz}$.
3. **Do.** Fill the `?` so that the script reproduces the Worked case's five runs. Then change the cap to `0.4` and to `1e9` for run C, and report the tail and $E_{\text{obs}}$.

```python
import numpy as np
m, b = 0.04, 0.8                      # P3
kh, xd, x0 = 400.0, 0.033, 0.029      # light fingertip: a spring, no damper
xw, Fmax = 0.030, 2.0                 # wall face; amplifier limit
dx = 2*np.pi*0.010/1024               # one encoder count, 61.4 um
T, sub = 1e-3, 40                     # servo period; plant substeps per period
def run(kw, hold=1, amax=0.0, t1=1.5):
    h = T/sub
    x, v = x0, 0.0
    xq_prev, F_prev, Eobs, Fw = np.floor(x0/dx)*dx, 0.0, 0.0, 0.0
    xs = []
    for k in range(int(round(t1/T))):
        xq = np.floor(x/dx)*dx                       # what the encoder reports
        Eobs += ?                                    # PO: energy into the wall over the last period
        if k % hold == 0:
            Fw = ?                                   # wall law on the reported position
        F, vq = Fw, (xq - xq_prev)/T
        if amax > 0 and Eobs < 0 and vq != 0:
            F -= ?                                   # PC: damping that pays the deficit, capped
        F = min(max(F, -Fmax), Fmax)
        for _ in range(sub):                         # continuous plant under the held force
            a = (kh*(xd - x) + F - b*v)/m
            v += h*a
            x += h*v
        F_prev, xq_prev = F, xq
        xs.append(x)
    tail = np.array(xs[int(1.0/T):])
    return round(float(max(xs))*1e3, 2), round(float(tail.max() - tail.min())*1e3, 3), round(float(Eobs)*1e3, 2)
for name, kw, hold, amax in (("A", 400, 1, 0), ("B", 2500, 1, 0), ("C", 2500, 1, 0.8),
                             ("D", 400, 5, 0), ("E", 400, 5, 0.8)):
    print(name, run(kw, hold, amax))
```

4. **Interpret.** A report says: "With time-domain passivity control, our one-degree-of-freedom kit renders a stable $5000\,\mathrm{N/m}$ wall." What three things would you ask for before believing that the wall *feels* like $5000\,\mathrm{N/m}$, and what could the result mean instead?

> [!note]- How to draw it · 그리는 법
> - Same two panels as the picture: position in millimetres over $0.6\,\mathrm{s}$ on top, observed energy in millijoules over $1.5\,\mathrm{s}$ below, the wall $x_w=30\,\mathrm{mm}$ dotted in the top panel and $E_{\text{obs}}=0$ dotted in the bottom one, with the region below zero shaded.
> - Mark the equilibrium at $31.5\,\mathrm{mm}$, not at the wall: with a $400\,\mathrm{N/m}$ wall the fingertip and wall springs share the $3\,\mathrm{mm}$ equally.
> - Without the controller (dashed): a limit cycle at about $21\,\mathrm{Hz}$ — slower than the picture's $34$ — swinging between about $28.8$ and $34.1\,\mathrm{mm}$, so the handle leaves the wall by more than a millimetre every cycle. Its energy falls roughly linearly to $-69.7\,\mathrm{mJ}$, four times the picture's.
> - With the controller (solid): a first overshoot to about $33.9\,\mathrm{mm}$, then a decay that is within $0.1\,\mathrm{mm}$ of $31.52\,\mathrm{mm}$ by about $0.43\,\mathrm{s}$; its energy drops to about $-1.5\,\mathrm{mJ}$ in the first $0.1\,\mathrm{s}$ and then stays flat, ending at $-1.44$.
> - The drawing is wrong if the dashed curve stays inside the wall: a limit cycle that never leaves the wall would never stop growing, because the leak would never switch off.

> [!tip]- Solutions
> 1. As in the How-to-draw list: dashed $x(t)$ a $21\,\mathrm{Hz}$ limit cycle between $28.8$ and $34.1\,\mathrm{mm}$ (tail $5.277\,\mathrm{mm}$), $E_{\text{obs}}\to-69.7\,\mathrm{mJ}$; solid $x(t)$ settling to $31.52\,\mathrm{mm}$ by $0.43\,\mathrm{s}$ (tail $0.001\,\mathrm{mm}$), $E_{\text{obs}}$ flat near $-1.44\,\mathrm{mJ}$ after $0.1\,\mathrm{s}$.
> 2. (a) $y_k(y_{k+1}-y_k)=\tfrac12(y_{k+1}^2-y_k^2)-\tfrac12(y_{k+1}-y_k)^2$ for each $k$ (expand the right side); summing, the first term telescopes. (b) $2b/T=2(0.8)/0.002=800\,\mathrm{N/m}$ at $2\,\mathrm{ms}$ and $320\,\mathrm{N/m}$ at $5\,\mathrm{ms}$ — the catalog wall passes the first and fails the second. (c) $S=0.012^2-0.020^2=-2.56\times10^{-4}$, $\nabla S=0.024$, step $+10.67\,\mathrm{mm}$ to $22.67\,\mathrm{mm}$; then $S=1.138\times10^{-4}$, $\nabla S=0.0453$, step $-2.51\,\mathrm{mm}$ to $20.16\,\mathrm{mm}$ (the third lands at $20.0006$). Starting deeper overshoots further, but the Newton step still converges quadratically. (d) $1000<2(0.8-b_c)/0.001$ gives $b_c<0.3\,\mathrm{N{\cdot}s/m}$.
> 3. The blanks are `-F_prev*(xq - xq_prev)`, `-kw*(xq - xw) if xq > xw else 0.0` and `min(-Eobs/(T*vq*vq), amax)*vq`. The filled script:
>
> ```python
> import numpy as np
> m, b = 0.04, 0.8
> kh, xd, x0 = 400.0, 0.033, 0.029
> xw, Fmax = 0.030, 2.0
> dx = 2*np.pi*0.010/1024
> T, sub = 1e-3, 40
> def run(kw, hold=1, amax=0.0, t1=1.5):
>     h = T/sub
>     x, v = x0, 0.0
>     xq_prev, F_prev, Eobs, Fw = np.floor(x0/dx)*dx, 0.0, 0.0, 0.0
>     xs = []
>     for k in range(int(round(t1/T))):
>         xq = np.floor(x/dx)*dx
>         Eobs += -F_prev*(xq - xq_prev)
>         if k % hold == 0:
>             Fw = -kw*(xq - xw) if xq > xw else 0.0
>         F, vq = Fw, (xq - xq_prev)/T
>         if amax > 0 and Eobs < 0 and vq != 0:
>             F -= min(-Eobs/(T*vq*vq), amax)*vq
>         F = min(max(F, -Fmax), Fmax)
>         for _ in range(sub):
>             a = (kh*(xd - x) + F - b*v)/m
>             v += h*a
>             x += h*v
>         F_prev, xq_prev = F, xq
>         xs.append(x)
>     tail = np.array(xs[int(1.0/T):])
>     return round(float(max(xs))*1e3, 2), round(float(tail.max() - tail.min())*1e3, 3), round(float(Eobs)*1e3, 2)
> for name, kw, hold, amax in (("A", 400, 1, 0), ("B", 2500, 1, 0), ("C", 2500, 1, 0.8),
>                              ("D", 400, 5, 0), ("E", 400, 5, 0.8)):
>     print(name, run(kw, hold, amax))
> ```
>
> It prints `A (33.53, 0.001, -0.32)`, `B (31.79, 1.658, -17.6)`, `C (31.79, 0.08, -1.81)`, `D (34.07, 5.277, -69.67)` and `E (33.9, 0.001, -1.44)`. With the cap at `0.4`, run C gives a tail of $1.012\,\mathrm{mm}$ and $E_{\text{obs}}=-10.45\,\mathrm{mJ}$; at `1e9` (only the amplifier limits it), $0.069\,\mathrm{mm}$ and $-8.94\,\mathrm{mJ}$ — the handle settles, but most of the dissipation the controller asked for was clipped by the $2\,\mathrm{N}$ amplifier and never delivered, so the energy count is worse than with the cap.
> 4. Ask for (i) the stiffness actually felt, measured as force over penetration during sustained contact, because a controller that damps every oscillation can make a nominal $5000\,\mathrm{N/m}$ wall feel like a stiff damper; (ii) how often, how strongly and for how long the controller acted, with the amplifier's saturation record, since a controller that is always on is a worst-case damper under another name; (iii) the force-update period and the grip used, since a stiff hold or a damped hand stabilizes walls by itself (24.4). "Stable" may mean only that the energy count was kept near zero, not that the wall was rendered.

### Sources

- K. Salisbury, F. Conti, F. Barbagli, "Haptic rendering: introductory concepts," *IEEE Computer Graphics and Applications* 24(2):24–32, 2004. DOI 10.1109/MCG.2004.1274058 — the three blocks, the loop steps and the multirate structure of §1.
- M. A. Srinivasan, C. Basdogan, "Haptics in virtual environments: taxonomy, research status, and challenges," *Computers & Graphics* 21(4):393–404, 1997. DOI 10.1016/S0097-8493(97)00030-7 — the two sensorimotor loops, the intermediate representation's discontinuity, and texture by normal perturbation.
- Y. Adachi, T. Kumano, K. Ogino, "Intermediate representation for stiff virtual objects," *Proc. IEEE VRAIS*, 1995, pp. 203–210.
- D. C. Ruspini, K. Kolarov, O. Khatib, "Haptic interaction in virtual environments," *Proc. IEEE/RSJ IROS*, 1997, pp. 128–133 — the separation of servo control from proxy update, and two-pass force shading.
- The CHAI3D documentation, [chai3d.org](https://www.chai3d.org/documentation) — an open-source library organized as the graphics and haptic threads of §1.
- K. Salisbury, C. Tarr, "Haptic rendering of surfaces defined by implicit functions," *Proc. ASME Dynamic Systems and Control Division*, DSC-Vol. 61, 1997, pp. 61–67 — seeding and surface tracking.
- H. B. Morgenbesser, M. A. Srinivasan, "Force shading for haptic shape perception," *Proc. ASME Dynamic Systems and Control Division*, DSC-Vol. 58, 1996, pp. 407–412.
- J. E. Colgate, M. C. Stanley, J. M. Brown, "Issues in the haptic display of tool use," *Proc. IEEE/RSJ IROS*, 1995, pp. 140–145; R. J. Adams, B. Hannaford, "Stable haptic interaction with virtual environments," *IEEE Transactions on Robotics and Automation* 15(3):465–474, 1999 — the virtual coupling.
- R. B. Gillespie, M. R. Cutkosky, "Stable user-specific haptic rendering of the virtual wall," *Proc. ASME IMECE*, DSC-Vol. 58, 1996, pp. 397–406 — the two energy leaks, the bouncing-ball test bed, half-sample prediction, digital-domain design and deadbeat correction of §5.
- B. Hannaford, J.-H. Ryu, "Time-domain passivity control of haptic interfaces," *IEEE Transactions on Robotics and Automation* 18(1):1–10, 2002. DOI 10.1109/70.988969 — the observer, the controller, and the experiments and limitations quoted in §6.
- The numbers on this page were computed here from the stated parameters, not quoted, except where a paper is named; recompute them with the lab code.

## 한국어

*[[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 렌더링, 샘플링과 안정성]]과 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 햅틱 렌더링 알고리즘]] 위에 선다. 같은 핸들 **P3**에, 이번에는 힘 법칙을 둘러싼 프로그램을 적어 넣는다. 어느 루프가 무엇을 계산하는지, 효과마다 어떤 상태를 들고 있는지, 강성이 경계를 넘은 벽을 어떻게 안정하게 두는지.*

> [!note] 처음이라면 · First pass
> 이 페이지의 대상을 읽고 그림을 본다. 샘플링 주기에 비해 너무 단단한 벽 하나를, 한 번은 그대로 두고 한 번은 벽이 만든 에너지를 세어 되갚는 계수기를 달아 본 것이다. 그다음 §1과 §2를 읽는다. 뒤의 모든 숫자가 기대는 주기 $T$가 여기서 정해진다. 그리고 실선을 설명하는 §6. §3은 장치를 프로그래밍할 때 꺼내 쓸 효과 목록, §4는 3차원 기하, §5는 점선이 왜 울리는지의 물리다. 계산 절이 이 모두를 P3 위에서 돌린다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P3**를 **가벼운 손끝**이 벽 안으로 누른다. 손의 스프링만 있고 댐퍼는 없는 손으로, [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]의 샘플링 경계가 가정하는 최악의 경우다. 핸들은 벽 바깥 $1\,\mathrm{mm}$에서 정지 상태로 출발하고, 손이 원하는 위치는 벽 안 $3\,\mathrm{mm}$이므로, 이 페이지의 모든 힘은 P3 앰프의 한계 안에 머문다.

| 기호 | 값 | 뜻 |
|---|---:|---|
| $m,\ b$ | $0.04\,\mathrm{kg}$, $0.8\,\mathrm{N{\cdot}s/m}$ | 카탈로그 핸들 질량과 감쇠 |
| $\Delta x$ | $61.4\,\mathrm{\mu m}$ | 인코더 한 카운트([[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3]] 계산 절 4단계) |
| $T$ | $1\,\mathrm{ms}$ | 서보 주기: $T$마다 인코더를 읽고 힘을 건다 |
| $k_h,\ b_h$ | $400\,\mathrm{N/m}$, $0$ | 손끝: 스프링만, 댐퍼 없음 |
| $x(0),\ x_d$ | $0.029\,\mathrm{m}$, $0.033\,\mathrm{m}$ | 정지 출발점, 손끝이 원하는 핸들 위치 |
| $x_w$ | $0.030\,\mathrm{m}$ | 벽 면, $+x$가 벽 안쪽 |
| $k_w$ | $400$(카탈로그) 또는 $2500\,\mathrm{N/m}$ | 뒤의 것은 경계 $2b/T=1600\,\mathrm{N/m}$를 넘는다 |
| $F^{\max}$ | $2.0\,\mathrm{N}$ | 앰프 한계([[04-robotics/haptics-teleoperation/device-design-kinematics\|24.3 §3]]) |
| $\alpha_{\max}$ | $0.8\,\mathrm{N{\cdot}s/m}$ | 수동성 제어기 감쇠의 상한(§6), $b$와 같게 둔다 |

손끝 값, 출발점, 상한은 이 페이지가 고정한 숫자이고 나머지는 카탈로그다. 벽을 망가뜨리는 두 방법을 비교한다. $T=1\,\mathrm{ms}$에서 경계를 넘는 강성, 그리고 카탈로그 강성이지만 힘을 $5\,\mathrm{ms}$마다만 다시 계산하는 경우(§2)다.

*범위: 이 페이지는 힘 법칙을 둘러싼 프로그램을 가르친다. 루프와 각 루프에서 돌려도 되는 것, 1자유도 효과와 각각에 필요한 상태, 3차원의 음함수 곡면과 표면 세부, 샘플된 벽의 두 에너지 누설, 그리고 그것을 막는 시간 영역 수동성 관측기와 제어기다. 샘플링 경계의 유도는 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]], 벌점·proxy·마찰 렌더링은 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7]], 지연된 원격조작 채널 위의 같은 관측기는 [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §7]]의 몫이다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 424" style="max-width:100%;height:auto" role="img" aria-label="가벼운 손끝이 1 kHz로 샘플되는 2500 N/m 벽에 P3를 누를 때의 두 그래프. 위: 처음 0.3초의 핸들 위치. 그냥 벽은 34 Hz 한계 순환으로 울리고, 수동성 관측기와 제어기를 단 벽은 가라앉는다. 아래: 1.5초 동안의 관측 에너지. 그냥 벽은 −17.6 mJ까지 꾸준히 내려가고, 제어기가 있으면 −1.8 mJ 근처에 머문다.">
<rect x="52" y="30" width="446" height="130" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="52" y="21" font-size="12.5" fill="currentColor" font-weight="600">핸들 위치 x (mm), 처음 0.6 s</text>
<text x="46" y="164.0" font-size="11" fill="currentColor" text-anchor="end">29</text>
<text x="46" y="120.7" font-size="11" fill="currentColor" text-anchor="end">30</text>
<text x="46" y="77.3" font-size="11" fill="currentColor" text-anchor="end">31</text>
<text x="46" y="34.0" font-size="11" fill="currentColor" text-anchor="end">32</text>
<line x1="52" y1="116.7" x2="498" y2="116.7" stroke="currentColor" stroke-dasharray="2 3" stroke-opacity="0.8"/>
<text x="502" y="120.7" font-size="11" fill="currentColor">벽 x<tspan dy="3.5" font-size="9.5">w</tspan><tspan dy="-3.5" dx="0"></tspan></text>
<text x="52.0" y="175" font-size="11" fill="currentColor" text-anchor="middle">0</text>
<text x="200.7" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.2</text>
<text x="349.3" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.4</text>
<text x="498.0" y="175" font-size="11" fill="currentColor" text-anchor="middle">0.6</text>
<polyline points="52.7,159.1 53.5,156.5 54.2,152.3 55.0,146.6 55.7,139.4 56.5,130.8 57.2,120.9 57.9,109.9 58.7,98.1 59.4,86.1 60.2,74.8 60.9,64.8 61.7,56.4 62.4,49.6 63.1,44.5 63.9,41.0 64.6,39.2 65.4,39.1 66.1,40.6 66.9,43.7 67.6,48.3 68.4,54.3 69.1,61.7 69.8,70.3 70.6,80.1 71.3,91.0 72.1,102.3 72.8,113.5 73.6,123.7 74.3,132.4 75.0,139.5 75.8,144.9 76.5,148.7 77.3,150.8 78.0,151.2 78.8,150.0 79.5,147.2 80.2,142.9 81.0,137.1 81.7,129.9 82.5,121.5 83.2,111.9 84.0,101.3 84.7,90.3 85.5,79.7 86.2,70.2 86.9,62.2 87.7,55.8 88.4,51.0 89.2,47.7 89.9,46.1 90.7,46.0 91.4,47.5 92.1,50.5 92.9,55.0 93.6,60.8 94.4,68.0 95.1,76.3 95.9,85.8 96.6,96.0 97.3,106.4 98.1,116.3 98.8,125.0 99.6,132.1 100.3,137.6 101.1,141.5 101.8,143.9 102.5,144.6 103.3,143.7 104.0,141.3 104.8,137.5 105.5,132.2 106.3,125.5 107.0,117.7 107.8,108.6 108.5,98.8 109.2,88.7 110.0,79.1 110.7,70.7 111.5,63.8 112.2,58.4 113.0,54.6 113.7,52.3 114.4,51.5 115.2,52.3 115.9,54.5 116.7,58.2 117.4,63.2 118.2,69.5 118.9,77.0 119.6,85.6 120.4,95.1 121.1,104.8 121.9,114.2 122.6,122.5 123.4,129.2 124.1,134.4 124.8,138.1 125.6,140.2 126.3,140.7 127.1,139.7 127.8,137.2 128.6,133.2 129.3,127.9 130.1,121.3 130.8,113.5 131.5,104.7 132.3,95.3 133.0,85.9 133.8,77.3 134.5,69.9 135.3,64.0 136.0,59.6 136.7,56.7 137.5,55.3 138.2,55.3 139.0,56.9 139.7,59.9 140.5,64.2 141.2,69.8 141.9,76.7 142.7,84.6 143.4,93.4 144.2,102.6 144.9,111.5 145.7,119.4 146.4,126.0 147.1,131.1 147.9,134.6 148.6,136.7 149.4,137.1 150.1,136.1 150.9,133.7 151.6,129.8 152.4,124.6 153.1,118.1 153.8,110.5 154.6,101.9 155.3,93.0 156.1,84.3 156.8,76.5 157.6,69.9 158.3,64.9 159.0,61.3 159.8,59.2 160.5,58.6 161.3,59.4 162.0,61.6 162.8,65.2 163.5,70.0 164.2,76.1 165.0,83.4 165.7,91.6 166.5,100.3 167.2,108.9 168.0,116.9 168.7,123.6 169.4,128.7 170.2,132.4 170.9,134.6 171.7,135.2 172.4,134.4 173.2,132.1 173.9,128.4 174.7,123.4 175.4,117.2 176.1,109.8 176.9,101.4 177.6,92.7 178.4,84.3 179.1,76.6 179.9,70.4 180.6,65.5 181.3,62.1 182.1,60.2 182.8,59.7 183.6,60.7 184.3,63.0 185.1,66.7 185.8,71.7 186.5,77.9 187.3,85.2 188.0,93.3 188.8,101.9 189.5,110.1 190.3,117.6 191.0,123.8 191.7,128.5 192.5,131.7 193.2,133.4 194.0,133.7 194.7,132.4 195.5,129.8 196.2,125.8 197.0,120.5 197.7,113.9 198.4,106.3 199.2,97.9 199.9,89.3 200.7,81.2 201.4,74.2 202.2,68.7 202.9,64.6 203.6,61.9 204.4,60.7 205.1,60.9 205.9,62.6 206.6,65.6 207.4,69.9 208.1,75.4 208.8,82.1 209.6,89.8 210.3,98.1 211.1,106.5 211.8,114.3 212.6,120.9 213.3,126.0 214.0,129.7 214.8,131.9 215.5,132.6 216.3,131.8 217.0,129.6 217.8,126.1 218.5,121.2 219.3,115.1 220.0,107.9 220.7,99.9 221.5,91.7 222.2,83.8 223.0,76.9 223.7,71.3 224.5,67.1 225.2,64.4 225.9,63.0 226.7,63.1 227.4,64.6 228.2,67.4 228.9,71.5 229.7,76.9 230.4,83.4 231.1,90.8 231.9,98.8 232.6,106.8 233.4,114.2 234.1,120.4 234.9,125.2 235.6,128.5 236.3,130.4 237.1,130.7 237.8,129.7 238.6,127.3 239.3,123.5 240.1,118.4 240.8,112.2 241.6,104.9 242.3,97.0 243.0,89.1 243.8,81.7 244.5,75.5 245.3,70.7 246.0,67.3 246.8,65.2 247.5,64.6 248.2,65.4 249.0,67.5 249.7,71.0 250.5,75.6 251.2,81.5 252.0,88.4 252.7,96.1 253.4,103.9 254.2,111.4 254.9,117.9 255.7,123.0 256.4,126.7 257.2,128.9 257.9,129.7 258.6,129.0 259.4,127.0 260.1,123.6 260.9,118.9 261.6,113.0 262.4,106.1 263.1,98.4 263.9,90.6 264.6,83.1 265.3,76.6 266.1,71.4 266.8,67.6 267.6,65.2 268.3,64.2 269.1,64.7 269.8,66.5 270.5,69.6 271.3,73.9 272.0,79.5 272.8,86.2 273.5,93.7 274.3,101.6 275.0,109.3 275.7,116.2 276.5,121.8 277.2,126.0 278.0,128.8 278.7,130.1 279.5,129.9 280.2,128.3 280.9,125.4 281.7,121.1 282.4,115.6 283.2,109.0 283.9,101.4 284.7,93.4 285.4,85.7 286.2,78.7 286.9,72.9 287.6,68.5 288.4,65.5 289.1,64.0 289.9,63.8 290.6,65.1 291.4,67.7 292.1,71.6 292.8,76.7 293.6,82.9 294.3,90.2 295.1,98.0 295.8,105.8 296.6,113.1 297.3,119.4 298.0,124.4 298.8,127.9 299.5,129.9 300.3,130.5 301.0,129.6 301.8,127.3 302.5,123.7 303.2,118.9 304.0,112.8 304.7,105.6 305.5,97.9 306.2,90.0 307.0,82.6 307.7,76.1 308.5,70.8 309.2,67.1 309.9,64.7 310.7,63.7 311.4,64.2 312.2,66.0 312.9,69.1 313.7,73.6 314.4,79.2 315.1,85.9 315.9,93.5 316.6,101.4 317.4,109.1 318.1,116.1 318.9,121.8 319.6,126.0 320.3,128.8 321.1,130.1 321.8,130.0 322.6,128.5 323.3,125.6 324.1,121.4 324.8,115.9 325.5,109.3 326.3,101.7 327.0,93.8 327.8,86.0 328.5,79.0 329.3,73.3 330.0,68.9 330.8,65.9 331.5,64.4 332.2,64.2 333.0,65.5 333.7,68.1 334.5,71.9 335.2,77.0 336.0,83.3 336.7,90.5 337.4,98.3 338.2,106.0 338.9,113.2 339.7,119.3 340.4,124.1 341.2,127.4 341.9,129.3 342.6,129.7 343.4,128.7 344.1,126.3 344.9,122.5 345.6,117.5 346.4,111.3 347.1,104.1 347.8,96.3 348.6,88.5 349.3,81.2 350.1,75.1 350.8,70.4 351.6,67.0 352.3,65.1 353.1,64.6 353.8,65.5 354.5,67.7 355.3,71.2 356.0,76.0 356.8,81.9 357.5,88.9 358.3,96.6 359.0,104.5 359.7,112.0 360.5,118.6 361.2,123.7 362.0,127.4 362.7,129.7 363.5,130.5 364.2,129.8 364.9,127.8 365.7,124.4 366.4,119.7 367.2,113.7 367.9,106.8 368.7,99.1 369.4,91.2 370.1,83.7 370.9,77.1 371.6,71.9 372.4,68.0 373.1,65.6 373.9,64.5 374.6,64.9 375.4,66.6 376.1,69.6 376.8,73.9 377.6,79.4 378.3,86.0 379.1,93.5 379.8,101.4 380.6,109.0 381.3,115.8 382.0,121.4 382.8,125.6 383.5,128.3 384.3,129.6 385.0,129.4 385.8,127.8 386.5,124.8 387.2,120.5 388.0,115.0 388.7,108.4 389.5,100.9 390.2,93.1 391.0,85.5 391.7,78.7 392.4,73.1 393.2,68.9 393.9,66.1 394.7,64.7 395.4,64.7 396.2,66.0 396.9,68.8 397.7,72.7 398.4,77.9 399.1,84.3 399.9,91.6 400.6,99.4 401.4,107.3 402.1,114.5 402.9,120.6 403.6,125.2 404.3,128.4 405.1,130.1 405.8,130.3 406.6,129.1 407.3,126.6 408.1,122.7 408.8,117.5 409.5,111.1 410.3,103.8 411.0,96.1 411.8,88.3 412.5,81.0 413.3,74.9 414.0,70.2 414.7,66.9 415.5,65.0 416.2,64.5 417.0,65.4 417.7,67.6 418.5,71.2 419.2,75.9 420.0,81.9 420.7,88.9 421.4,96.7 422.2,104.6 422.9,112.1 423.7,118.7 424.4,123.9 425.2,127.6 425.9,129.9 426.6,130.7 427.4,130.0 428.1,128.0 428.9,124.6 429.6,119.9 430.4,114.0 431.1,106.9 431.8,99.1 432.6,91.0 433.3,83.3 434.1,76.6 434.8,71.2 435.6,67.2 436.3,64.6 437.0,63.5 437.8,63.8 438.5,65.4 439.3,68.4 440.0,72.6 440.8,78.1 441.5,84.6 442.2,92.1 443.0,100.0 443.7,107.9 444.5,115.2 445.2,121.3 446.0,126.0 446.7,129.2 447.5,130.9 448.2,131.1 448.9,130.0 449.7,127.4 450.4,123.5 451.2,118.3 451.9,111.9 452.7,104.5 453.4,96.5 454.1,88.5 454.9,81.1 455.6,74.7 456.4,69.8 457.1,66.3 457.9,64.3 458.6,63.6 459.3,64.3 460.1,66.4 460.8,69.8 461.6,74.5 462.3,80.4 463.1,87.3 463.8,95.0 464.6,103.0 465.3,110.7 466.0,117.7 466.8,123.3 467.5,127.5 468.3,130.3 469.0,131.5 469.8,131.3 470.5,129.7 471.2,126.7 472.0,122.3 472.7,116.7 473.5,110.0 474.2,102.3 475.0,94.2 475.7,86.3 476.4,79.2 477.2,73.2 477.9,68.7 478.7,65.6 479.4,63.9 480.2,63.7 480.9,64.8 481.6,67.2 482.4,71.0 483.1,76.0 483.9,82.2 484.6,89.3 485.4,97.1 486.1,105.1 486.8,112.7 487.6,119.2 488.3,124.5 489.1,128.2 489.8,130.5 490.6,131.3 491.3,130.6 492.1,128.6 492.8,125.2 493.5,120.5 494.3,114.5 495.0,107.4 495.8,99.5 496.5,91.5 497.3,83.8 498.0,77.0" fill="none" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" stroke-dasharray="3 2"/>
<polyline points="52.7,159.1 53.5,156.5 54.2,152.3 55.0,146.6 55.7,139.4 56.5,130.8 57.2,120.9 57.9,109.9 58.7,98.1 59.4,86.1 60.2,74.8 60.9,64.8 61.7,56.4 62.4,49.6 63.1,44.5 63.9,41.0 64.6,39.2 65.4,39.1 66.1,40.6 66.9,43.7 67.6,48.3 68.4,54.3 69.1,61.7 69.8,70.3 70.6,80.1 71.3,91.0 72.1,102.3 72.8,113.4 73.6,123.3 74.3,131.5 75.0,137.9 75.8,142.5 76.5,145.4 77.3,146.6 78.0,146.2 78.8,144.2 79.5,140.6 80.2,135.7 81.0,129.5 81.7,122.1 82.5,113.7 83.2,104.4 84.0,94.7 84.7,85.4 85.5,76.8 86.2,69.6 86.9,63.8 87.7,59.5 88.4,56.7 89.2,55.4 89.9,55.6 90.7,57.2 91.4,60.3 92.1,64.7 92.9,70.5 93.6,77.4 94.4,85.4 95.1,94.3 95.9,103.4 96.6,111.9 97.3,119.4 98.1,125.2 98.8,129.5 99.6,132.2 100.3,133.3 101.1,132.9 101.8,131.0 102.5,127.8 103.3,123.3 104.0,117.6 104.8,110.9 105.5,103.3 106.3,95.4 107.0,87.6 107.8,80.5 108.5,74.6 109.2,70.0 110.0,66.9 110.7,65.2 111.5,64.8 112.2,65.9 113.0,68.3 113.7,71.9 114.4,76.8 115.2,82.9 115.9,89.9 116.7,97.5 117.4,105.0 118.2,111.9 118.9,117.7 119.6,122.1 120.4,124.9 121.1,126.3 121.9,126.2 122.6,124.7 123.4,121.9 124.1,117.8 124.8,112.6 125.6,106.4 126.3,99.7 127.1,92.8 127.8,86.3 128.6,80.7 129.3,76.3 130.1,73.3 130.8,71.6 131.5,71.3 132.3,72.3 133.0,74.5 133.8,78.0 134.5,82.6 135.3,88.3 136.0,94.6 136.7,101.1 137.5,107.3 138.2,112.7 139.0,117.0 139.7,119.8 140.5,121.3 141.2,121.3 141.9,120.0 142.7,117.5 143.4,113.7 144.2,108.9 144.9,103.3 145.7,97.2 146.4,91.3 147.1,85.9 147.9,81.4 148.6,78.0 149.4,76.0 150.1,75.3 150.9,75.9 151.6,77.7 152.4,80.7 153.1,84.9 153.8,89.9 154.6,95.4 155.3,100.9 156.1,106.0 156.8,110.5 157.6,113.9 158.3,116.1 159.0,117.0 159.8,116.5 160.5,114.8 161.3,111.8 162.0,107.8 162.8,103.1 163.5,98.1 164.2,93.2 165.0,88.5 165.7,84.5 166.5,81.5 167.2,79.8 168.0,79.4 168.7,80.1 169.4,82.1 170.2,85.1 170.9,89.0 171.7,93.4 172.4,98.1 173.2,102.7 173.9,106.9 174.7,110.3 175.4,112.9 176.1,114.3 176.9,114.5 177.6,113.4 178.4,111.1 179.1,108.0 179.9,104.0 180.6,99.7 181.3,95.2 182.1,90.9 182.8,87.1 183.6,84.1 184.3,82.3 185.1,81.5 185.8,81.8 186.5,83.4 187.3,86.0 188.0,89.4 188.8,93.4 189.5,97.7 190.3,102.0 191.0,105.9 191.7,109.2 192.5,111.5 193.2,112.7 194.0,112.9 194.7,111.9 195.5,109.9 196.2,107.1 197.0,103.5 197.7,99.5 198.4,95.4 199.2,91.5 199.9,88.0 200.7,85.3 201.4,83.4 202.2,82.5 202.9,82.8 203.6,84.0 204.4,86.3 205.1,89.4 205.9,93.1 206.6,97.1 207.4,101.1 208.1,104.8 208.8,107.9 209.6,110.3 210.3,111.8 211.1,112.2 211.8,111.5 212.6,109.8 213.3,107.2 214.0,103.9 214.8,100.2 215.5,96.3 216.3,92.6 217.0,89.2 217.8,86.5 218.5,84.6 219.3,83.7 220.0,83.7 220.7,84.8 221.5,86.8 222.2,89.5 223.0,92.9 223.7,96.6 224.5,100.2 225.2,103.7 225.9,106.8 226.7,109.0 227.4,110.4 228.2,110.9 228.9,110.5 229.7,109.2 230.4,107.0 231.1,104.1 231.9,100.8 232.6,97.3 233.4,93.7 234.1,90.6 234.9,87.9 235.6,85.9 236.3,84.8 237.1,84.5 237.8,85.2 238.6,86.9 239.3,89.3 240.1,92.3 240.8,95.8 241.6,99.4 242.3,102.7 243.0,105.8 243.8,108.3 244.5,110.0 245.3,110.9 246.0,110.8 246.8,109.9 247.5,108.1 248.2,105.6 249.0,102.6 249.7,99.3 250.5,96.0 251.2,92.7 252.0,89.8 252.7,87.5 253.4,86.0 254.2,85.2 254.9,85.4 255.7,86.4 256.4,88.2 257.2,90.7 257.9,93.6 258.6,96.8 259.4,99.9 260.1,103.0 260.9,105.7 261.6,107.8 262.4,109.3 263.1,109.9 263.9,109.5 264.6,108.3 265.3,106.4 266.1,103.8 266.8,100.8 267.6,97.5 268.3,94.3 269.1,91.3 269.8,88.9 270.5,87.1 271.3,86.2 272.0,86.1 272.8,86.9 273.5,88.5 274.3,90.8 275.0,93.5 275.7,96.5 276.5,99.5 277.2,102.3 278.0,104.8 278.7,106.8 279.5,108.1 280.2,108.7 280.9,108.4 281.7,107.4 282.4,105.7 283.2,103.5 283.9,100.8 284.7,97.9 285.4,94.9 286.2,92.1 286.9,89.9 287.6,88.2 288.4,87.1 289.1,86.8 289.9,87.4 290.6,88.7 291.4,90.6 292.1,93.0 292.8,95.6 293.6,98.3 294.3,100.9 295.1,103.1 295.8,105.0 296.6,106.3 297.3,107.0 298.0,107.0 298.8,106.3 299.5,104.9 300.3,103.0 301.0,100.8 301.8,98.3 302.5,95.8 303.2,93.4 304.0,91.2 304.7,89.5 305.5,88.5 306.2,88.2 307.0,88.5 307.7,89.5 308.5,91.1 309.2,93.1 309.9,95.5 310.7,97.9 311.4,100.2 312.2,102.5 312.9,104.4 313.7,105.9 314.4,106.6 315.1,106.7 315.9,106.0 316.6,104.7 317.4,102.9 318.1,100.8 318.9,98.4 319.6,95.9 320.3,93.5 321.1,91.5 321.8,89.8 322.6,88.9 323.3,88.6 324.1,89.0 324.8,90.0 325.5,91.5 326.3,93.4 327.0,95.6 327.8,97.9 328.5,100.0 329.3,102.0 330.0,103.6 330.8,104.8 331.5,105.4 332.2,105.5 333.0,105.1 333.7,104.2 334.5,102.9 335.2,101.2 336.0,99.2 336.7,97.1 337.4,95.2 338.2,93.4 338.9,92.0 339.7,91.1 340.4,90.6 341.2,90.6 341.9,91.1 342.6,92.0 343.4,93.3 344.1,95.0 344.9,96.8 345.6,98.8 346.4,100.6 347.1,102.1 347.8,103.3 348.6,104.0 349.3,104.1 350.1,103.8 350.8,103.0 351.6,101.8 352.3,100.4 353.1,98.9 353.8,97.2 354.5,95.7 355.3,94.2 356.0,93.0 356.8,92.2 357.5,91.7 358.3,91.7 359.0,92.2 359.7,93.1 360.5,94.4 361.2,95.8 362.0,97.4 362.7,98.9 363.5,100.4 364.2,101.7 364.9,102.7 365.7,103.4 366.4,103.6 367.2,103.3 367.9,102.5 368.7,101.4 369.4,100.0 370.1,98.4 370.9,96.9 371.6,95.3 372.4,94.0 373.1,92.8 373.9,92.0 374.6,91.6 375.4,91.7 376.1,92.2 376.8,93.2 377.6,94.5 378.3,95.9 379.1,97.5 379.8,99.1 380.6,100.7 381.3,101.9 382.0,102.7 382.8,103.3 383.5,103.4 384.3,102.9 385.0,102.1 385.8,101.1 386.5,99.8 387.2,98.3 388.0,96.8 388.7,95.3 389.5,94.0 390.2,92.9 391.0,92.1 391.7,91.8 392.4,91.9 393.2,92.5 393.9,93.5 394.7,94.8 395.4,96.3 396.2,98.0 396.9,99.5 397.7,100.8 398.4,101.9 399.1,102.6 399.9,103.0 400.6,103.1 401.4,102.8 402.1,102.3 402.9,101.4 403.6,100.3 404.3,99.0 405.1,97.6 405.8,96.3 406.6,95.1 407.3,94.2 408.1,93.5 408.8,93.2 409.5,93.1 410.3,93.3 411.0,93.7 411.8,94.4 412.5,95.4 413.3,96.5 414.0,97.6 414.7,98.8 415.5,99.9 416.2,100.8 417.0,101.4 417.7,101.7 418.5,101.7 419.2,101.4 420.0,100.8 420.7,100.0 421.4,98.9 422.2,97.8 422.9,96.8 423.7,95.8 424.4,95.0 425.2,94.3 425.9,94.0 426.6,94.0 427.4,94.2 428.1,94.6 428.9,95.4 429.6,96.2 430.4,97.1 431.1,98.1 431.8,98.9 432.6,99.6 433.3,100.2 434.1,100.7 434.8,100.9 435.6,100.8 436.3,100.3 437.0,99.7 437.8,99.1 438.5,98.3 439.3,97.4 440.0,96.6 440.8,95.9 441.5,95.3 442.2,94.8 443.0,94.5 443.7,94.5 444.5,94.7 445.2,95.2 446.0,95.9 446.7,96.6 447.5,97.3 448.2,98.1 448.9,98.9 449.7,99.4 450.4,99.9 451.2,100.2 451.9,100.4 452.7,100.5 453.4,100.4 454.1,100.2 454.9,99.9 455.6,99.5 456.4,99.0 457.1,98.3 457.9,97.6 458.6,96.9 459.3,96.3 460.1,95.8 460.8,95.4 461.6,95.1 462.3,95.0 463.1,95.2 463.8,95.6 464.6,96.2 465.3,96.8 466.0,97.4 466.8,98.2 467.5,98.8 468.3,99.3 469.0,99.7 469.8,100.0 470.5,100.1 471.2,100.1 472.0,100.0 472.7,99.7 473.5,99.4 474.2,98.9 475.0,98.4 475.7,97.7 476.4,97.1 477.2,96.5 477.9,96.1 478.7,95.7 479.4,95.5 480.2,95.3 480.9,95.2 481.6,95.2 482.4,95.3 483.1,95.5 483.9,95.8 484.6,96.2 485.4,96.6 486.1,97.1 486.8,97.6 487.6,98.2 488.3,98.8 489.1,99.2 489.8,99.5 490.6,99.6 491.3,99.6 492.1,99.5 492.8,99.3 493.5,99.0 494.3,98.6 495.0,98.1 495.8,97.5 496.5,96.9 497.3,96.4 498.0,96.0" fill="none" stroke="currentColor" stroke-width="1.6"/>
<text x="492" text-anchor="end" y="45" font-size="11" fill="currentColor">그냥 벽: 34 Hz 한계 순환, 봉우리 사이 1.66 mm</text>
<text x="492" text-anchor="end" y="152" font-size="11" fill="currentColor" font-weight="600">1 s 뒤: 0.08 mm</text>
<text x="275.0" y="190" font-size="11" fill="currentColor" text-anchor="middle">시간 (s)</text>
<rect x="52" y="251.8" width="446" height="96.2" fill="currentColor" fill-opacity="0.07"/>
<rect x="52" y="238" width="446" height="110" fill="none" stroke="currentColor" stroke-opacity="0.5"/>
<text x="52" y="229" font-size="12.5" fill="currentColor" font-weight="600">관측 에너지 E<tspan dy="3.5" font-size="9.5">obs</tspan><tspan dy="-3.5" dx="3">(mJ), 전체 1.5 s</tspan></text>
<text x="46" y="255.8" font-size="11" fill="currentColor" text-anchor="end">0</text>
<text x="46" y="301.6" font-size="11" fill="currentColor" text-anchor="end">−10</text>
<text x="46" y="347.4" font-size="11" fill="currentColor" text-anchor="end">−20</text>
<line x1="52" y1="251.8" x2="498" y2="251.8" stroke="currentColor" stroke-dasharray="2 3" stroke-opacity="0.8"/>
<text x="52.0" y="363" font-size="11" fill="currentColor" text-anchor="middle">0</text>
<text x="200.7" y="363" font-size="11" fill="currentColor" text-anchor="middle">0.5</text>
<text x="349.3" y="363" font-size="11" fill="currentColor" text-anchor="middle">1</text>
<text x="498.0" y="363" font-size="11" fill="currentColor" text-anchor="middle">1.5</text>
<text x="275.0" y="378" font-size="11" fill="currentColor" text-anchor="middle">시간 (s)</text>
<polyline points="52.3,251.8 53.8,251.8 55.3,250.1 56.8,241.4 58.2,241.4 59.7,249.3 61.2,254.2 62.7,254.2 64.2,254.2 65.7,251.5 67.2,244.8 68.7,245.9 70.1,254.6 71.6,256.2 73.1,256.2 74.6,256.2 76.1,250.3 77.6,247.4 79.1,253.1 80.5,258.3 82.0,258.3 83.5,258.3 85.0,255.0 86.5,249.9 88.0,253.3 89.5,260.0 91.0,260.2 92.4,260.2 93.9,257.8 95.4,252.9 96.9,255.1 98.4,261.7 99.9,262.0 101.4,262.0 102.8,259.7 104.3,254.7 105.8,257.5 107.3,263.5 108.8,263.7 110.3,263.7 111.8,261.0 113.3,257.0 114.7,259.9 116.2,265.5 117.7,265.5 119.2,265.5 120.7,262.1 122.2,258.7 123.7,263.2 125.1,267.2 126.6,267.2 128.1,267.0 129.6,262.0 131.1,261.5 132.6,267.3 134.1,268.8 135.6,268.8 137.0,267.5 138.5,262.5 140.0,264.7 141.5,270.1 143.0,270.3 144.5,270.3 146.0,266.9 147.4,264.1 148.9,268.0 150.4,272.0 151.9,272.0 153.4,271.8 154.9,266.8 156.4,266.3 157.9,271.6 159.3,273.5 160.8,273.5 162.3,272.6 163.8,267.3 165.3,269.0 166.8,274.8 168.3,275.2 169.7,275.2 171.2,272.3 172.7,268.9 174.2,272.3 175.7,276.8 177.2,276.8 178.7,276.7 180.2,272.2 181.6,271.1 183.1,276.4 184.6,278.3 186.1,278.3 187.6,277.4 189.1,272.7 190.6,273.8 192.0,279.6 193.5,280.0 195.0,280.0 196.5,277.0 198.0,273.7 199.5,277.0 201.0,281.6 202.5,281.6 203.9,281.6 205.4,276.5 206.9,275.3 208.4,280.8 209.9,283.2 211.4,283.2 212.9,282.5 214.3,277.5 215.8,278.0 217.3,283.9 218.8,284.8 220.3,284.8 221.8,282.8 223.3,278.6 224.8,280.8 226.2,286.3 227.7,286.4 229.2,286.4 230.7,283.0 232.2,280.2 233.7,284.2 235.2,288.1 236.6,288.1 238.1,288.0 239.6,283.0 241.1,282.4 242.6,287.8 244.1,289.7 245.6,289.7 247.1,288.8 248.5,284.0 250.0,285.1 251.5,290.6 253.0,291.3 254.5,291.3 256.0,288.8 257.5,285.0 258.9,287.8 260.4,292.8 261.9,292.9 263.4,292.9 264.9,288.8 266.4,286.6 267.9,291.1 269.4,294.5 270.8,294.5 272.3,294.3 273.8,289.4 275.3,288.8 276.8,294.6 278.3,296.1 279.8,296.1 281.2,294.9 282.7,289.9 284.2,291.6 285.7,297.3 287.2,297.7 288.7,297.7 290.2,294.8 291.7,291.4 293.1,295.4 294.6,299.3 296.1,299.3 297.6,299.1 299.1,294.1 300.6,293.6 302.1,299.3 303.5,300.8 305.0,300.8 306.5,299.5 308.0,294.5 309.5,296.8 311.0,302.1 312.5,302.4 314.0,302.4 315.4,298.9 316.9,296.1 318.4,300.6 319.9,304.0 321.4,304.0 322.9,303.7 324.4,298.4 325.8,298.4 327.3,304.1 328.8,305.7 330.3,305.7 331.8,304.5 333.3,299.4 334.8,301.1 336.3,306.9 337.7,307.3 339.2,307.3 340.7,304.4 342.2,301.0 343.7,304.4 345.2,308.9 346.7,308.9 348.1,308.9 349.6,304.4 351.1,302.7 352.6,308.2 354.1,310.6 355.6,310.6 357.1,309.9 358.6,304.9 360.0,305.4 361.5,311.6 363.0,312.2 364.5,312.2 366.0,309.8 367.5,305.9 369.0,309.3 370.4,313.8 371.9,313.8 373.4,313.8 374.9,309.3 376.4,307.6 377.9,312.6 379.4,315.5 380.9,315.5 382.3,315.2 383.8,309.8 385.3,309.8 386.8,315.6 388.3,317.1 389.8,317.1 391.3,316.2 392.7,310.9 394.2,311.5 395.7,318.2 397.2,318.9 398.7,318.9 400.2,317.0 401.7,312.1 403.2,314.3 404.6,320.3 406.1,320.6 407.6,320.6 409.1,317.7 410.6,313.7 412.1,317.1 413.6,322.2 415.0,322.2 416.5,322.2 418.0,317.6 419.5,315.4 421.0,320.4 422.5,323.8 424.0,323.8 425.5,323.7 426.9,318.1 428.4,317.6 429.9,323.5 431.4,325.5 432.9,325.5 434.4,324.8 435.9,319.2 437.3,319.8 438.8,326.2 440.3,327.1 441.8,327.1 443.3,325.5 444.8,320.3 446.3,322.5 447.8,328.5 449.2,328.8 450.7,328.8 452.2,325.9 453.7,321.9 455.2,325.3 456.7,330.4 458.2,330.4 459.6,330.4 461.1,325.8 462.6,323.6 464.1,328.6 465.6,332.1 467.1,332.1 468.6,331.9 470.1,326.4 471.5,325.8 473.0,331.7 474.5,333.7 476.0,333.7 477.5,333.0 479.0,327.4 480.5,328.0 481.9,334.4 483.4,335.3 484.9,335.3 486.4,333.8 487.9,328.5 489.4,330.8 490.9,336.7 492.4,337.0 493.8,337.0 495.3,334.1 496.8,330.2" fill="none" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="3 2"/>
<polyline points="52.3,251.8 53.8,251.8 55.3,250.1 56.8,241.4 58.2,241.4 59.7,249.3 61.2,253.6 62.7,253.4 64.2,253.2 65.7,249.3 67.2,244.8 68.7,247.6 70.1,254.0 71.6,253.9 73.1,253.8 74.6,250.4 76.1,247.1 77.6,251.0 79.1,254.5 80.5,254.4 82.0,253.7 83.5,249.3 85.0,250.4 86.5,254.7 88.0,254.9 89.5,254.6 91.0,250.9 92.4,251.4 93.9,255.1 95.4,255.4 96.9,254.7 98.4,251.9 99.9,253.4 101.4,255.7 102.8,255.8 104.3,254.2 105.8,252.4 107.3,255.1 108.8,256.2 110.3,255.9 111.8,253.7 113.3,253.8 114.7,256.2 116.2,256.5 117.7,255.6 119.2,253.6 120.7,255.4 122.2,256.8 123.7,256.7 125.1,255.2 126.6,254.4 128.1,256.3 129.6,257.1 131.1,256.6 132.6,255.1 134.1,255.1 135.6,256.8 137.0,257.3 138.5,256.4 140.0,254.9 141.5,256.1 143.0,257.4 144.5,257.3 146.0,256.0 147.4,255.6 148.9,257.1 150.4,257.7 151.9,257.4 153.4,255.8 154.9,256.2 156.4,257.5 157.9,257.8 159.3,257.0 160.8,255.9 162.3,257.1 163.8,257.9 165.3,257.7 166.8,256.9 168.3,256.5 169.7,257.6 171.2,258.0 172.7,257.6 174.2,256.7 175.7,257.1 177.2,258.0 178.7,258.1 180.2,257.6 181.6,256.9 183.1,257.7 184.6,258.4 186.1,258.0 187.6,257.5 189.1,257.5 190.6,258.4 192.0,258.4 193.5,257.9 195.0,257.6 196.5,258.0 198.0,258.5 199.5,258.5 201.0,258.1 202.5,257.8 203.9,258.4 205.4,258.7 206.9,258.5 208.4,257.9 209.9,258.2 211.4,258.5 212.9,258.5 214.3,258.5 215.8,258.3 217.3,258.3 218.8,258.6 220.3,258.6 221.8,258.4 223.3,258.4 224.8,258.4 226.2,258.4 227.7,258.7 229.2,258.7 230.7,258.4 232.2,258.4 233.7,258.4 235.2,258.7 236.6,258.7 238.1,258.5 239.6,258.5 241.1,258.5 242.6,258.8 244.1,258.8 245.6,258.5 247.1,258.5 248.5,258.5 250.0,258.8 251.5,258.8 253.0,258.5 254.5,258.6 256.0,258.6 257.5,258.9 258.9,258.9 260.4,258.6 261.9,258.6 263.4,258.6 264.9,258.9 266.4,258.9 267.9,258.7 269.4,258.7 270.8,258.7 272.3,259.0 273.8,259.0 275.3,258.7 276.8,258.7 278.3,259.0 279.8,259.0 281.2,258.8 282.7,258.8 284.2,258.8 285.7,259.1 287.2,259.1 288.7,258.8 290.2,258.8 291.7,258.8 293.1,259.1 294.6,259.1 296.1,258.9 297.6,258.9 299.1,258.9 300.6,259.2 302.1,259.2 303.5,258.9 305.0,258.9 306.5,258.9 308.0,259.2 309.5,259.2 311.0,258.9 312.5,258.9 314.0,259.3 315.4,259.3 316.9,259.0 318.4,259.0 319.9,259.0 321.4,259.3 322.9,259.3 324.4,259.0 325.8,259.0 327.3,259.0 328.8,259.3 330.3,259.3 331.8,259.1 333.3,259.1 334.8,259.1 336.3,259.4 337.7,259.4 339.2,259.1 340.7,259.1 342.2,259.1 343.7,259.4 345.2,259.4 346.7,259.2 348.1,259.2 349.6,259.5 351.1,259.5 352.6,259.2 354.1,259.2 355.6,259.2 357.1,259.5 358.6,259.5 360.0,259.2 361.5,259.2 363.0,259.2 364.5,259.6 366.0,259.6 367.5,259.3 369.0,259.3 370.4,259.3 371.9,259.6 373.4,259.6 374.9,259.3 376.4,259.3 377.9,259.3 379.4,259.6 380.9,259.6 382.3,259.4 383.8,259.4 385.3,259.7 386.8,259.7 388.3,259.4 389.8,259.4 391.3,259.4 392.7,259.7 394.2,259.7 395.7,259.5 397.2,259.5 398.7,259.5 400.2,259.8 401.7,259.8 403.2,259.5 404.6,259.5 406.1,259.5 407.6,259.8 409.1,259.8 410.6,259.5 412.1,259.5 413.6,259.5 415.0,259.9 416.5,259.9 418.0,259.6 419.5,259.6 421.0,259.9 422.5,259.9 424.0,259.6 425.5,259.6 426.9,259.6 428.4,259.9 429.9,259.9 431.4,259.7 432.9,259.7 434.4,259.7 435.9,260.0 437.3,260.0 438.8,259.7 440.3,259.7 441.8,259.7 443.3,260.0 444.8,260.0 446.3,259.8 447.8,259.8 449.2,259.8 450.7,260.1 452.2,260.1 453.7,259.8 455.2,259.8 456.7,260.1 458.2,260.1 459.6,259.9 461.1,259.9 462.6,259.9 464.1,260.2 465.6,260.2 467.1,259.9 468.6,259.9 470.1,259.9 471.5,260.2 473.0,260.2 474.5,259.9 476.0,259.9 477.5,259.9 479.0,260.2 480.5,260.2 481.9,260.0 483.4,260.0 484.9,260.0 486.4,260.3 487.9,260.3 489.4,260.0 490.9,260.0 492.4,260.3 493.8,260.3 495.3,260.1 496.8,260.1" fill="none" stroke="currentColor" stroke-width="1.6"/>
<text x="502" y="336.4" font-size="11" fill="currentColor">−17.6</text>
<text x="502" y="264.1" font-size="11" fill="currentColor" font-weight="600">−1.8</text>
<text x="60" y="336.5" font-size="11" fill="currentColor" fill-opacity="0.85">E<tspan dy="3.5" font-size="9.5">obs</tspan><tspan dy="-3.5" dx="3">&lt; 0: 벽이 에너지를 만들었다</tspan></text>
<line x1="52" y1="394" x2="78" y2="394" stroke="currentColor" stroke-width="1.6"/><text x="84" y="398" font-size="11" fill="currentColor">관측기와 제어기, α ≤ 0.8 N·s/m</text>
<line x1="52" y1="412" x2="78" y2="412" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.7" stroke-dasharray="3 2"/><text x="84" y="416" font-size="11" fill="currentColor">그냥 샘플된 벽</text>
</svg>

같은 $2500\,\mathrm{N/m}$ 벽을 $1\,\mathrm{kHz}$로 샘플하고 같은 가벼운 손끝이 누른다. 그대로 두면(점선) $34\,\mathrm{Hz}$ 한계 순환으로 울리고, 벽의 포트에서 센 에너지가 꾸준히 내려간다. 벽이 에너지를 만들고 있다. 수동성 관측기와 제어기를 달면(실선) 첫 충돌은 그대로지만, 그 뒤로 계수기가 보는 부족분이 짧은 감쇠 힘으로 되갚아지고 핸들이 가라앉는다.

### 1. 세 블록, 두 루프

Salisbury, Conti, Barbagli는 모든 햅틱 렌더링 프로그램을 세 블록으로 나눈다. **충돌 검출**은 장치의 아바타가 무엇에, 어디서 닿는지를 찾는다. **힘 응답**은 이상적인 상호작용이 낼 힘을 계산한다. **제어**는 그 이상적인 힘을, 한계 안에서 장치가 실제로 낼 수 있는 힘으로 바꾼다. 한 서보 주기가 이들을 순서대로 돌린다. 관절 센서를 읽고, 순기구학으로 아바타 자세를 구하고, 충돌을 검출하고, 응답을 계산하고, $J^\top$로 구동기에 명령하고([[04-robotics/haptics-teleoperation/device-design-kinematics|24.3]]), 같은 힘을 시뮬레이션에 넘겨 가상 물체가 반응하게 한다. Srinivasan과 Basdogan은 같은 파이프라인을 두 번째 감각운동 루프 — 인코더, 컴퓨터, 모터 — 로 그리고, 그것이 피부와 관절 센서, 뇌, 근육으로 이뤄진 사람의 루프와 핸들에서 만난다고 본다.

실제 프로그램은 이 블록들을 두 주기로 돌린다. 눈과 손이 필요로 하는 것이 다르기 때문이다. **그래픽 루프**는 $30$–$60\,\mathrm{Hz}$로 장면을 다시 그리고, 시각에는 그것으로 충분하다. **햅틱 루프**는 $1\,\mathrm{kHz}$ 이상으로, 자기 스레드에서 높은 우선순위로 돈다. 샘플된 스프링은 $T$에 비례해 에너지를 새게 하고(24.4 §2), 피부는 수백 헤르츠까지의 과도 신호를 느끼기 때문이다. CHAI3D 같은 오픈소스 라이브러리가 정확히 이렇게 짜여 있다. 메인 스레드가 창과 장면 그래프를 맡고, 햅틱 스레드가 매 틱 장치를 읽고, 물체마다 그 물체의 좌표계에서 접촉력을 계산해 월드 좌표계로 돌려 명령한다. 여기서 나오는 규칙이 이 페이지에서 가장 실용적인 문장이다. **햅틱 루프에서는 느리거나 막히는 일을 하나도 하지 않는다.** 파일이나 콘솔 출력, 메모리 할당, 그래픽 스레드가 쥔 잠금 기다리기, 네트워크 호출 모두 안 된다. 늦게 끝난 틱은 $T$가 길어진 틱이고, 경계 $2b/T$는 그 이유를 묻지 않는다.

기하가 너무 복잡해 킬로헤르츠로 질의할 수 없으면, 두 주기를 중간 대상 하나로 잇는다.

> **중간 표현, 정의.** **중간 표현**(intermediate representation)은 *기하를 대신하는 국소적이고 단순한 대리물*이며, 느린 루프가 계산하고 빠른 루프가 렌더링한다(Adachi, Kumano, Ogino 1995). 세 조건이 정의한다. **국소적**이다. 현재 접촉 근처에서만 유효하며, 대개 그곳 표면에 접하는 평면이나 구다. **느리게 계산**된다. 충돌·기하 루프가 수십에서 수백 헤르츠로 갱신한다. 그리고 **서보 주기로 렌더링**된다. 매 틱 햅틱 루프가 가장 새 장치 위치로 대리물에 대한 힘을 계산한다.
>
> - **예**: $30\,\mathrm{Hz}$로 갱신되는 접평면에서 $1\,\mathrm{kHz}$로 힘을 계산한다. $0.1\,\mathrm{m/s}$로 미끄러지는 탐침은 평면 갱신 사이에 $3.3\,\mathrm{mm}$를 움직이므로, 평면은 표면이 $3.3\,\mathrm{mm}$에 걸쳐 휘는 만큼 틀린다. 그러나 *힘*은 매 밀리초 새로우므로, 샘플링 경계가 보는 강성은 여전히 $1\,\mathrm{kHz}$의 것이다.
> - **비예**: 느린 루프가 힘까지 계산해 넘기는 것. 그 힘은 느린 루프의 한 주기 내내 붙들리므로, 더 큰 $T$에서의 §2의 실패다.
> - **왜 중요한가**: 빨라야 하는 것(안정성을 위한 힘)과 느려도 되는 것(정확도를 위한 기하)을 가르고, 복잡한 장면과 수술 시뮬레이터가 킬로헤르츠에 닿는 방법이 이것이다. 대가는 갱신 순간에 보인다. 대리물이 따라잡기 전에 탐침이 멀리 가면 힘이 튄다(Srinivasan과 Basdogan).

Ruspini, Kolarov, Khatib는 [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms|24.7 §3]]의 proxy에 같은 분리를 했다. 저수준 제어기가 서보 주기로 장치를 proxy 쪽으로 몰고, proxy는 따로 갱신된다. 갱신이 뒤처지면 물체는 불안정해지는 대신 *끈적하게* 느껴진다 — proxy가 늦는 것이다. 햅틱 프로그램이 실패한다면 이렇게 실패해야 한다.

### 2. 힘을 어디서 계산하느냐가 $T$를 정한다

모든 경계의 $T$는 무엇을 샘플하는 주기가 아니라 *힘 명령이 바뀌는* 주기다. 실시간 스레드로 도는 데스크톱 장치에서는 둘이 같다. 취미용 마이크로컨트롤러로 도는 1자유도 키트에서는 흔히 다르다. $1\,\mathrm{kHz}$ 타이머 인터럽트가 인코더를 읽고 가장 최근 모터 명령을 거는데, 힘 법칙 자체는 시리얼 출력과 대기와 함께 메인 루프에 있다. 그러면 인터럽트는 메인 루프가 걸리는 동안 같은 힘을 걸고, 실효 $T$는 메인 루프의 주기다. $5\,\mathrm{ms}$에서 경계는 $2b/T=2(0.8)/0.005=320\,\mathrm{N/m}$이고, $1\,\mathrm{kHz}$에서 넉넉하던 카탈로그 $400\,\mathrm{N/m}$ 벽이 이제 울린다(계산 절 D). 인코더를 읽는 바로 그 인터럽트 안에서 힘을 계산하거나, 적어도 명령이 실제로 얼마나 자주 바뀌는지 — 바뀔 때마다 핀 하나를 토글해 오실로스코프로 본다 — 재고 나서 강성 숫자를 믿는다.

분해능이 두 번째 한계다. P3의 한 카운트는 $61.4\,\mathrm{\mu m}$이므로, 차분 $(\hat x_k-\hat x_{k-1})/T$는 $1\,\mathrm{kHz}$에서 $61.4\,\mathrm{mm/s}$의 배수만 보고할 수 있다. $10\,\mathrm{mm/s}$로 움직이는 손은 $6.1$틱마다 한 카운트를 만든다. 추정값은 다섯 번 $0$이고 한 번 $61.4\,\mathrm{mm/s}$다. 그 추정값을 받는 가상 댐퍼 $B=0.4\,\mathrm{N{\cdot}s/m}$는 매끈한 $0.004\,\mathrm{N}$ 대신 $0.025\,\mathrm{N}$짜리 힘 펄스를 낸다. [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §3]]의 1차 필터를 $f_c=20\,\mathrm{Hz}$(계수 $e^{-2\pi f_cT}=0.882$)로 걸면 펄스는 매끈해지지만 시정수 $8.0\,\mathrm{ms}$를 치르고, 댐퍼의 지연은 24.4가 불안정을 부를 수 있다고 경고한 바로 그것이다. 공짜 선택은 없고, 밝혀 둔 선택만 있다.

세 번째 함정은 단위다. 마이크로컨트롤러 코드는 대개 인코더 카운트와 PWM 듀티로 일하므로, 거기서의 "강성"은 카운트당 듀티다. 모터 토크 상수, 앰프 이득, 24.3의 전동을 거쳐야 비로소 $\mathrm{N/m}$가 되고, 그 전에는 어떤 경계와도 비교할 수 없다.

### 3. 1자유도 효과 목록

1자유도 핸들에서 모든 효과는 힘 법칙이고, 프로그래밍의 질문은 그 법칙이 루프에 어떤 상태를 들고 있으라고 요구하느냐다. 표는 실습 과정이 효과 하나씩 쌓아 올리는 목록이고, 행마다 P3에서 무엇이 한계를 정하는지 적었다.

| 효과 | 힘 법칙 | 루프가 들고 있는 상태 | P3에서의 한계 |
|---|---|---|---|
| 스프링(양방향) | $F=-k(x-x_0)$ | 없음 | $k<2b/T$. 한 카운트가 $k\,\Delta x$ 뉴턴 |
| 벽(한 방향) | $x>x_w$이면 $F=-k_w(x-x_w)$, 아니면 $0$ | 없음, 대신 스위치 | 같은 경계, 그리고 §5의 두 누설 |
| 댐퍼 | $F=-B\hat v$ | 직전 위치, 필터 상태 | 속도 양자와 필터 지연(§2). $K=0$인 24.4 §2에서 $B<b$ |
| 달라붙는 마찰 | Karnopp 법칙, [[04-robotics/haptics-teleoperation/haptic-rendering-algorithms\|24.7 §5]] | 붙음 또는 미끄러짐 | 붙음 대역 $D_v$는 틱당 한 카운트, $61.4\,\mathrm{mm/s}$보다 촘촘할 수 없다 |
| 돌기나 골 | 높이 곡선 $h$에 대해 $F=-A\,h'(x)$ | 없음 | 힘만으로 모양이 전달된다(24.7 §6). 위치에만 의존해야 양방향에서 같은 느낌 |
| 단단한 표면 | 벽에, 접촉 순간 개루프 과도 신호 $F=A\,v_{\text{in}}e^{-t/\tau}\sin(2\pi ft)$ | 접촉 래치, 충돌 시각, $v_{\text{in}}$ | 앰프 한계. 과도 신호가 표면을 능동적으로 느끼게 하면 안 된다(24.7 §4) |
| 결합에 매단 가상 질량 | $m_v\ddot x_v=k_c(x-x_v)+b_c(\dot x-\dot x_v)+\ldots$, 장치는 반대 힘을 느낀다 | 매 틱 적분하는 $x_v,\ \dot x_v$ | 적분 스텝 $\omega_cT$. 아래의 결합 경계 |

두 행에는 숫자가 필요하다. 가우스 돌기 $h(x)=e^{-(x-x_b)^2/2\sigma^2}$에서 옆 힘 $-A\,h'(x)$는 $x_b\pm\sigma$에서 크기 $A/(\sigma\sqrt e)$로 최대다. 폭 $\sigma=2\,\mathrm{mm}$, $0.5\,\mathrm{N}$짜리 돌기는 $A=0.5\cdot0.002\cdot\sqrt e=1.65\times10^{-3}\,\mathrm{J}$가 필요하다. 오르막을 미는 데 드는 에너지는 어느 쪽에서 오든 똑같이 $A$이고, 이것이 "양방향에서 같은 느낌"을 물리로 쓴 조건이다. 가상 질량에서는 $1000\,\mathrm{N/m}$ 결합에 매단 $0.05\,\mathrm{kg}$ 공이 $\frac{1}{2\pi}\sqrt{1000/0.05}=22.5\,\mathrm{Hz}$로 공진하고, 반암시적 오일러 스텝은 $\omega_cT<2$에서 안정하다. 여기서 $\omega_cT=0.14$다.

마지막 행은 스스로 동역학을 가진 모든 것의 일반 형태이고, 이름이 있다.

> **가상 결합, 정의.** **가상 결합**(virtual coupling)은 *장치와 시뮬레이션 물체 사이에 둔 스프링–댐퍼 $(k_c, b_c)$*이며, 장치는 결합만 느끼고 시뮬레이션은 결합의 크기가 같고 방향이 반대인 힘만 느낀다(Colgate, Stanley, Brown 1995; Adams와 Hannaford 1999). 세 조건이 정의한다. 환경은 시뮬레이션이 적분하는 **자기 상태**를 가진다. 결합이 장치에서 환경으로 가는 **유일한** 경로다. 그리고 $(k_c, b_c)$는 결합 **혼자서** 샘플링 경계 $k_c<2(b-b_c)/T$를 만족하도록 고른다.
>
> - **예**: 위의 가상 공에 $b_c=0.2\,\mathrm{N{\cdot}s/m}$. 경계는 $2(0.8-0.2)/0.001=1200\,\mathrm{N/m}$이므로, 공이 시뮬레이션 안에서 무엇과 부딪치든 — 강체 바닥까지 — $k_c=1000\,\mathrm{N/m}$는 통과한다.
> - **비예**: 들어갈 때만 감쇠를 거는 벽. 뒤에 시뮬레이션 상태가 없다. 그것은 효과이고, 경계는 그 자신의 $k_w$에 걸린다.
> - **왜 중요한가**: 환경은 얼마든지 단단하고 복잡해도 되고, 장치는 수동적으로 렌더링할 수 있는 것만 렌더링한다. 대가는 천장이다. 결합을 통해 손은 $k_c$보다 단단한 것을 결코 느끼지 못한다. [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §3]]의 장치 두 대 사이 PD 결합이 같은 대상이고, 그 $Z+C$ 천장이 같은 사실이다.

### 4. 반공간 너머의 곡면

반공간에는 법선이 하나뿐이다. 그 밖의 모든 것은 매 틱 표면 점과 그 법선을 찾을 방법이 필요하다.

**음함수 곡면.** Salisbury와 Tarr는 $S(p)=0$으로 주어지고 안쪽이 $S<0$인 곡면을 렌더링한다. 장치 점에서 $S(p)<0$이 되면 접촉이 시작된다. 표면 점은 **시딩**(seeding)으로 찾는다. 기울기를 따라 뉴턴 스텝을

$$\delta p=-\frac{S(p)\,\nabla S(p)}{\nabla S(p)\cdot\nabla S(p)},\qquad p\leftarrow p+\delta p$$

$\lVert\delta p\rVert$가 허용치보다 작아질 때까지 반복한다. 반지름 $r=20\,\mathrm{mm}$인 구 $S=x^2+y^2+z^2-r^2$와 중심에서 $15\,\mathrm{mm}$인 장치 점이면 $S=-1.75\times10^{-4}\,\mathrm{m^2}$, $\lVert\nabla S\rVert=0.030\,\mathrm{m}$이므로 첫 스텝이 점을 $5.83\,\mathrm{mm}$ 밖으로, $20.83\,\mathrm{mm}$로 옮긴다. 다음 두 스텝은 $20.017$과 $20.00001\,\mathrm{mm}$에 닿는다. 접촉 중에는 처음부터 다시 시딩하지 않고 **추적**한다. 매 틱 직전 표면 점의 접평면을 새 장치 점의 제약으로 쓰고, 그 위로 사영하고, 거기서 다시 시딩해 몇 틱에 걸쳐 수렴한다. 장치 점이 평면 안쪽을 벗어나면 접촉이 끝난다. 두 모양이 이것을 무너뜨린다. 얇은 물체는 24.7 §2에서처럼 가장 가까운 면이 반대쪽 면이 되는 곳까지 장치 점을 넘어가게 하고, 강하게 오목한 곳은 시드가 가까운 두 표면 점 사이를 오가게 만든다 — 손이 윙윙거림으로 느끼는 한계 순환이다.

**힘 셰이딩.** 다각형 메시는 모서리마다 법선이 튄다. Morgenbesser와 Srinivasan은 Phong 셰이딩이 빛에 하듯 꼭짓점 법선을 각 면에 걸쳐 보간해, 힘 방향이 매끄럽게 돌게 한다. Ruspini의 proxy는 이것을 두 번에 나눠 구현한다. 먼저 *보간된* 법선에 수직이고 접촉점을 지나는 평면들로 부분 목표를 얻고, 그다음 그 부분 목표에서 출발해 진짜 평면들로 푼다. 원을 두른 십각형에서 셰이딩이 없으면 힘 방향이 모서리마다 $36^\circ$ 튀고 면마다 옆으로 끌지만, 셰이딩하면 둘 다 없다. 대가는 작다. 제약 평면이 더는 기하와 맞지 않으므로, 셰이딩한 표면은 받은 것보다 조금 많은 에너지를 돌려줄 수 있다.

**법선을 흔드는 질감.** Srinivasan과 Basdogan은 그래픽의 범프 매핑을 가져온다. 기하는 그대로 두고, 표면 위 높이장 $h$의 기울기로 힘 방향을 기울인다.

$$M=N-\nabla h+(\nabla h\cdot N)\,N$$

단위 법선 $N$에서 $\nabla h$의 접선 성분을 빼는 식이다. $a=0.1\,\mathrm{mm}$, $\lambda=2\,\mathrm{mm}$인 격자 $h=a\sin(2\pi s/\lambda)$에서 가장 가파른 기울기는 $2\pi a/\lambda=0.314$이므로 힘은 최대 $17.4^\circ$ 기운다. $1\,\mathrm{N}$으로 수직으로 누르면 손은 부호가 번갈아 바뀌는 $0.30\,\mathrm{N}$의 옆 성분을 느끼고, $50\,\mathrm{mm/s}$로 쓸면 그것이 $25\,\mathrm{Hz}$다. 기하 자체를 움직이는 것(변위 매핑)은 더 충실하지만 돌기마다 충돌 질의를 치른다. 높이장은 이미지(회색 값을 높이로)에서 오거나 절차 — 푸리에 급수, 노이즈, 프랙탈, 확률 모형 — 에서 온다.

### 5. 벽의 두 에너지 누설

Gillespie와 Cutkosky는 샘플된 벽이 진짜 벽은 만들 수 없는 에너지를 만드는 두 기구에 이름을 붙였고, 둘 다 그림의 점선에서 보인다.

**영차 홀드.** 한 샘플에서 계산한 힘이 한 주기 내내 붙들린다. *들어갈* 때는 샘플된 위치가 실제보다 뒤처지므로 붙들린 힘이 너무 작고, *나올* 때는 샘플된 위치가 여전히 실제보다 깊으므로 힘이 너무 크다. 누르는 데 진짜 벽보다 일이 덜 들고, 놓을 때 더 돌려받는다. 지속 접촉하는 벽이면 계산이 정확하다. $y_k=\hat x_k-x_w$로 두고 붙들린 힘 $-k_wy_k$가 스텝 $y_{k+1}-y_k$ 동안 작용하면, 벽에 들어간 에너지는

$$\sum_k k_w\,y_k\,(y_{k+1}-y_k)=\tfrac12k_w\big(y_n^2-y_0^2\big)-\tfrac12k_w\sum_k(y_{k+1}-y_k)^2$$

로, 연속 스프링의 에너지에서 $\tfrac12k_w\sum\Delta y^2$를 *뺀* 것이다. 들어가든 나오든 스텝마다 샌다.

**비동기 전환.** 벽은 스위치이고, 스위치는 샘플 시각에만 바뀐다. 한 샘플 늦게 켜지므로 스프링은 이미 눌린 채다 — 아무도 일을 하지 않았는데 저장된 에너지다. 그리고 벽 안의 마지막 샘플의 힘은 핸들이 이미 벗어난 주기 동안에도 밖으로 민다.

그들의 시험대는 튀는 공이었다. $0.35\,\mathrm{kg}$의 조작 핸들과 $0.006\,\mathrm{kg}$, $500\,\mathrm{N/m}$의 손가락, 감쇠 없음, $10\,\mathrm{ms}$마다 샘플되는 $5000\,\mathrm{N/m}$ 바닥이다. 샘플된 공은 튈 때마다 더 높이 올라갔다. 홀드의 누설은 두 방법으로 없앴다. 손과 장치의 모형으로 $T/2$ 앞을 예측한 위치에서 벽 법칙을 계산하는 **반 샘플 예측**, 그리고 이산화한 플랜트의 폐루프 극을 연속 목표의 영차 홀드 등가에 두는 **디지털 영역 설계**다. 전환의 누설은 **감시와 데드비트 보정**으로 없앴다. 교차 전후의 샘플로부터, 문턱에서 정확히 전환했다면 벽 밖 첫 샘플에서 상태가 어디 있었을지 계산하고, 벽 안 마지막 두 붙들린 힘을 골라 2차 계를 정확히 거기로 보낸다.

교훈은 가정에 있다. 그들이 본 채터는 대개 $10$–$50\,\mathrm{Hz}$로, 사람이 의도해서 명령하는 것보다 훨씬 높고, 사람은 흔드는 것이 아니라 일정한 쥠새로 벽을 누른 채 채터를 일으킨다. 같은 벽이 한 사람의 손가락 아래서는 떨고 다른 사람 아래서는 떨지 않을 수 있다. 그래서 반사가 개입하기 전 약 $30\,\mathrm{ms}$ 동안 손가락을 2차 선형계로 모형화할 수 있고, 렌더링 직전에 같은 장치로 그 모형을 식별한다. 이 페이지의 한계 순환은 $34\,\mathrm{Hz}$로 그들의 대역 안에 있다. 결과와 함께 가져가야 할 그들 자신의 단서도 있다. 보정한 벽은 위치뿐 아니라 속도도 되먹임하므로 감쇠 없는 벽과 비교하면 후하게 보이고, 첫 실험은 정성적이었다.

### 6. 시간 영역 수동성: 에너지를 세고, 되갚는다

Hannaford와 Ryu는 모형을 측정으로 바꿨다. 한 블록이 에너지를 만드는 이유가 무엇이든 — 홀드, 스위치, 지연, 마찰 보상기 — 지금까지 만든 에너지는 그 포트의 힘과 속도로 셀 수 있다. 벽 하나에 통장을 만들어 준다고 생각하면 된다. 매 틱, 손이 벽에 밀어 넣은 일은 입금되고 벽이 되민 일은 출금된다. 진짜 수동적인 벽은 받은 것만 돌려줄 수 있으므로 결코 마이너스가 되지 않는다. **관측기**가 그 잔고이고, **제어기**는 잔고가 마이너스가 될 때마다 정확히 그 초과분을 짧은 감쇠 힘으로 되받아 내는 규칙이다.

> **수동성 관측기와 수동성 제어기, 정의.** 포트로 *들어가는* 파워를 양으로 하고 초기 저장 에너지를 0으로 두면, **수동성 관측기**(PO)는 누적합
>
> $$E_{\text{obs}}(n)=T\sum_{k=0}^{n}f(k)\,v(k)$$
>
> 이고, 포트는 $E_{\text{obs}}(n)\ge0$일 때 정확히 샘플 $n$까지 수동적이었다. 음수 값은 블록이 만든 에너지다. **수동성 제어기**(PC)는 같은 포트에 둔 *적응 댐퍼*로, 그 부족분을 정확히 흡수한다. 임피던스 인과성(속도 입력, 힘 출력)에서는 직렬로 둔다. 블록 자신의 힘을 $f_e(n)$, $W(n)=E_{\text{obs}}(n-1)+f_e(n)v(n)T$로 두면
>
> $$\alpha(n)=\begin{cases}-\dfrac{W(n)}{T\,v(n)^2}, & W(n)<0\\[4pt] 0, & W(n)\ge0\end{cases},\qquad f(n)=f_e(n)+\alpha(n)\,v(n)$$
>
> 이다. 어드미턴스 인과성은 쌍대인 병렬 형태를 쓴다.
>
> - **예**: 계산 절의 C. PC는 $1500$틱 중 $374$틱에서, 결코 $0.20\,\mathrm{N}$을 넘지 않게 작동하고, $1.66\,\mathrm{mm}$ 한계 순환이 $0.08\,\mathrm{mm}$가 된다.
> - **비예**: 최악의 경우에 맞춰 크기를 정한 가상 결합(§3). 설계로 수동적이고, 아무것도 소산할 필요가 없던 대부분의 틱까지 포함해 매 틱 감쇠를 치른다.
> - **비예**: 각 힘을 *그 힘을 계산하기 전의* 변위와 곱해 더하는 같은 관측기. B의 벽이 $17.6\,\mathrm{mJ}$를 만들었는데 $26.6\,\mathrm{mJ}$를 소산했다고 보고하고, 그 제어기는 한 번도 작동하지 않는다(아래).
> - **왜 중요한가**: 장치, 손, 환경의 모형이 필요 없다. 한 포트의 두 신호만 있으면 되고, 계수가 말할 때만, 말하는 만큼만 소산한다. 지연된 채널 위의 같은 관측기가 [[04-robotics/haptics-teleoperation/teleoperation-architectures-delay|24.8 §7]]이다.

**어느 변위를 어느 힘과 짝짓는가.** 식 $f(k)v(k)T$는 $v(k)$가 무엇인지 열어 두고, 샘플된 벽에서는 그 선택이 관측기가 누설을 보느냐 마느냐를 정한다. 샘플 $k$에서 계산한 힘은 *다음* 스텝 동안 붙들리므로, 정직한 짝은 $f(k)\,(\hat x_{k+1}-\hat x_k)$ — 누설을 보여 주는 §5의 합이다. 같은 힘을 같은 샘플에서 잰 후진 차분 속도와 짝지으면, $f(k)\,(\hat x_k-\hat x_{k-1})$, 같은 대수가

$$\sum_k k_w\,y_k\,(y_k-y_{k-1})=\tfrac12k_w\big(y_n^2-y_0^2\big)+\tfrac12k_w\sum_k(y_k-y_{k-1})^2$$

를 준다. 누설이 *반대* 부호, 곧 소산으로 나타난다. Hannaford와 Ryu는 샘플 사이에 힘과 속도가 거의 변하지 않을 만큼 샘플링이 빠른 경우로 분석을 한정했고, 거기서는 두 짝짓기가 일치한다. 샘플링 경계를 넘은 벽은 정확히 그 가정이 깨지는 곳이다. 그래서 실습의 관측기는 매 틱, 방금 끝난 스텝 동안 *붙들렸던* 힘의 일을 더하고, 제어기는 $W(n)$ 대신 그 계수를 쓴다.

그들의 근거는 Excalibur라는 3축 장치였다. $1\,\mathrm{kHz}$로 동기화되어 돌고, 위치 분해능 $0.1\,\mathrm{mm}$, 최대 $200\,\mathrm{N}$의 힘, 힘 분해능 $0.096\,\mathrm{N}$이다. $90\,\mathrm{kN/m}$ 가상 블록을 약 $200\,\mathrm{mm/s}$로 건드리면 PC 없이 접촉 진동이 지속됐다. 관측기는 첫 튐이 수동적이고 그 뒤의 더 작은 튐들이 능동적임을 보여 줬다. PC를 켜면 약 여섯 번 튄 뒤 접촉이 안정됐고, 제어기는 네 번째부터 작동했으며, PC 힘은 $40\,\mathrm{N}$ 미만이었다. 그 힘을 $20\,\mathrm{N}$으로 제한해도 거의 달라지지 않았다. 가상 환경을 $66.7\,\mathrm{Hz}$로 늦추고(힘 하나를 $15$샘플 동안 붙듦) $30\,\mathrm{kN/m}$로 두면 접촉이 격렬하게 불안정해져 $200\,\mathrm{N}$짜리 힘 펄스가 나왔고, PC를 켜면 한 번 튄 뒤 안정됐다. 장치 자신의 블록들에 관측기를 달아 보니, 능동적 거동의 대부분은 벽이 아니라 장치의 Coulomb 마찰 보상에서 왔다.

한계도 그만큼 구체적이다. 저속에서 $\alpha=-W/(Tv^2)$는 엄청나게 커진다. P3에서 상한 없이 두면 실습의 제어기는 최대 $2394\,\mathrm{N{\cdot}s/m}$를 요구한다 — $2\,\mathrm{N}$ 앰프에 $147\,\mathrm{N}$을 내라는 것이다 — 그리고 속도 잡음도 같은 식으로 키운다. 그들 자신의 느린 환경 실험에서도 핸들이 거의 멈춰 있는 동안 제어기 출력이 잡음처럼 되었고, 사용자는 약 반 초 동안 그것을 느끼고 들었다. 그래서 $\alpha$나 PC 힘에 상한을 두고, 상한이 걸린 제어기가 다 갚지 못한 부족분은 뒤의 샘플로 넘어간다. 실습에서 상한 $0.8$이면 $0.08\,\mathrm{mm}$, $0.4$면 $1.01\,\mathrm{mm}$가 남는다. 관측기는 합 하나이므로 한 곳에 쌓인 소산이 다른 곳의 능동성을 가릴 수 있고, 저자들은 이를테면 자유 운동 중에 계수를 초기화하자고 제안한다. 그리고 벽 포트에만 단 관측기는 보수적이다. A에서 카탈로그 벽의 포트는 $0.32\,\mathrm{mJ}$를 만들지만 장치 자신의 댐퍼가 더 많이 소산하므로 루프는 안정한데도 제어기는 작동할 것이다. 그들의 처방은 포트 밖의 알려진 소산을 셈에 넣어, 문턱 0을 $-b\,T\sum v^2$로 바꾸는 것이다.

### 대상으로 한 번 끝까지 · Worked case

이 페이지의 대상 위에서 $1.5\,\mathrm{s}$씩 다섯 번 돌린다. 최고점은 핸들이 가장 깊이 간 곳, 꼬리는 마지막 $0.5\,\mathrm{s}$의 봉우리 사이 운동, $E_{\text{obs}}$는 끝에서 벽 포트의 관측 에너지다. 실습 코드가 모두 계산한다.

| 실행 | 벽 | 힘 갱신 주기 | PO/PC | 최고점 | 꼬리 | $E_{\text{obs}}$ |
|---|---|---|---|---:|---:|---:|
| A | $400\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | 끔 | $33.53\,\mathrm{mm}$ | $0.001\,\mathrm{mm}$ | $-0.32\,\mathrm{mJ}$ |
| B | $2500\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | 끔 | $31.79\,\mathrm{mm}$ | $1.658\,\mathrm{mm}$ | $-17.6\,\mathrm{mJ}$ |
| C | $2500\,\mathrm{N/m}$ | $1\,\mathrm{ms}$ | 켬, $\alpha\le0.8$ | $31.79\,\mathrm{mm}$ | $0.080\,\mathrm{mm}$ | $-1.81\,\mathrm{mJ}$ |
| D | $400\,\mathrm{N/m}$ | $5\,\mathrm{ms}$ | 끔 | $34.07\,\mathrm{mm}$ | $5.277\,\mathrm{mm}$ | $-69.7\,\mathrm{mJ}$ |
| E | $400\,\mathrm{N/m}$ | $5\,\mathrm{ms}$ | 켬, $\alpha\le0.8$ | $33.90\,\mathrm{mm}$ | $0.001\,\mathrm{mm}$ | $-1.44\,\mathrm{mJ}$ |

**1단계 — 카탈로그 벽은 안정하고, 그 포트는 수동적이지 않다.** A는 손끝 스프링과 벽 스프링이 균형을 이루는 $31.52\,\mathrm{mm}$에 가라앉는다. $x^\ast=(400\cdot0.033+400\cdot0.030)/800=0.0315\,\mathrm{m}$, 벽 힘 $0.60\,\mathrm{N}$이다. 그래도 관측기는 $-0.32\,\mathrm{mJ}$로 끝난다. 홀드가 스텝마다 새고, 관측한 포트 밖의 장치 댐퍼 $b$가 그보다 많이 소산한다. 안정은 모든 포트가 수동적일 것을 요구하지 않는다. 루프만 그러면 된다.

**2단계 — 경계를 넘으면 한계 순환.** $2500\,\mathrm{N/m}$에서는 경계 $2b/T=1600\,\mathrm{N/m}$를 넘고, 손끝에 감쇠가 없으니 누설을 덮어 줄 것이 없다. 핸들은 $29.62$와 $31.28\,\mathrm{mm}$ 사이를 $34\,\mathrm{Hz}$로 튄다. 매 주기 벽 밖으로 $0.38\,\mathrm{mm}$ 나가고, 그래서 진동이 한없이 커지지 못한다. 벽 밖에서는 누설이 멈춘다. 벽은 $1.5\,\mathrm{s}$ 동안 $17.6\,\mathrm{mJ}$를 만든다. 평균 $11.7\,\mathrm{mW}$, 주기당 약 $0.35\,\mathrm{mJ}$다. §5의 홀드 누설 $\tfrac12k_w\sum\Delta y^2$를 마지막 1초 동안 앰프가 잘리지 않은 접촉 스텝에 걸쳐 더하면 $11.9\,\mathrm{mJ}$이고, 관측기가 그 1초에 센 것은 $11.1\,\mathrm{mJ}$다. 거의 전부가 홀드의 몫이다. 그 $1000$틱 가운데 $365$틱에서 힘은 $2\,\mathrm{N}$ 한계에 붙어 있었고, 잘린 힘은 상수이므로 붙들어도 잃는 것이 없다.

**3단계 — 관측기와 제어기.** C는 같은 최고점 $31.79\,\mathrm{mm}$에 닿는다. 첫 충돌은 그대로다. 관측기가 부족분을 보기 전에는 제어기가 작동할 수 없기 때문이다. 그 뒤로 부족분은 최대 $0.20\,\mathrm{N}$의 감쇠 펄스로 되갚아지고, 핸들은 $0.52\,\mathrm{s}$까지 $30.47\,\mathrm{mm}$의 $0.1\,\mathrm{mm}$ 안으로 가라앉는다(평형은 $30.41\,\mathrm{mm}$이고, 나머지는 한 카운트의 양자화 몫이다). 관측기는 $0$이 아니라 $-1.81\,\mathrm{mJ}$로 끝난다. 상한 때문에 일부 부족분은 늦게 갚아지고, 작은 나머지는 끝내 갚지 못한다. §6의 같은 샘플 짝짓기로 하면 관측기는 $+26.6\,\mathrm{mJ}$를 읽고, 제어기는 한 번도 작동하지 않으며, 꼬리는 $1.658\,\mathrm{mm}$에 머문다.

**4단계 — 느린 힘 루프.** D는 A에서 통과한 카탈로그 벽에 변경 하나만 준 것이다. 힘을 다섯 틱마다 다시 계산한다. 경계가 $320\,\mathrm{N/m}$로 떨어지고, 핸들은 $28.8$과 $34.1\,\mathrm{mm}$ 사이를 $21\,\mathrm{Hz}$로 울리며, 벽은 $69.7\,\mathrm{mJ}$를 만든다. 멀쩡하던 강성에서 이 페이지 최악의 실행이 나온다. E는 관측기와 제어기를 더하고, 핸들은 A만큼 빨리 가라앉는다($0.1\,\mathrm{mm}$ 안에 머물기까지 $0.43$ 대 $0.41\,\mathrm{s}$).

**5단계 — 숫자가 허락하는 것.** 제어기는 모형 없이 에너지 계수를 안정성으로 바꾸지만, 벽을 더 단단하게 만들지 않고, 첫 충돌을 바꾸지 않으며, 자기 감쇠가 $0.8$인 장치에 $0.8\,\mathrm{N{\cdot}s/m}$의 상한을 쓴다. 먼저 알아야 할 더 싼 처방은 D다. 힘 법칙을 서보 인터럽트로 옮기면 제어기가 풀던 문제가 사라진다.

### 읽고 나서

- [ ] 렌더링 루프의 세 블록을 말하고, 어느 것이 빠른 루프에서 돌고 어느 것이 느리게 돌아도 되는지, 그리고 중간 표현과 그 대가를 정의할 수 있다.
- [ ] 샘플링 경계의 $T$가 왜 힘 명령의 주기인지 설명하고, 힘을 $200\,\mathrm{Hz}$로 다시 계산할 때의 경계를 계산할 수 있다.
- [ ] 효과 목록의 각 효과에 대해 힘 법칙과 루프가 들고 있어야 할 상태를 쓸 수 있다.
- [ ] 가상 결합 경계 $k_c<2(b-b_c)/T$와, 결합이 느껴지는 강성에 거는 천장을 말할 수 있다.
- [ ] 구에 대해 음함수 곡면 시딩 스텝을 손으로 돌리고, 어떤 모양이 표면 추적을 무너뜨리는지 말할 수 있다.
- [ ] 영차 홀드 누설 $\tfrac12k_w\sum\Delta y^2$를 유도하고, 두 번째인 전환 누설을 말할 수 있다.
- [ ] 수동성 관측기와 직렬 제어기를 쓰고, 힘과 변위의 짝짓기가 왜 관측기가 누설을 보느냐를 정하는지 설명할 수 있다.

### 스스로 점검

1. 어떤 햅틱 프로그램이 햅틱 루프 안에서 모든 접촉력을 파일에 기록하고, 디스크가 바쁠 때 안정하던 벽이 윙윙거리기 시작한다. 24.4의 경계로 말하면 무슨 일이 일어났는가?
2. 갱신이 뒤처진 proxy는 왜 불안정하지 않고 끈적하게 느껴지는가?
3. $1\,\mathrm{kHz}$의 P3에서 차분이 보고할 수 있는 가장 작은 0 아닌 속도는 얼마이고, 손이 $10\,\mathrm{mm/s}$로 움직일 때 그것을 받는 가상 댐퍼는 무엇을 하는가?
4. $k_c=1000\,\mathrm{N/m}$인 가상 결합을 통해, 시뮬레이션 공이 완전히 단단한 시뮬레이션 바닥에 부딪친다. 손은 어떤 강성을 느끼고, 루프는 왜 안정한가?
5. §5의 두 누설 가운데 반 샘플 예측만으로는 남는 것은 무엇이고, 무엇이 그것을 없애는가?
6. C에서 제어기 감쇠의 상한은 $0.8\,\mathrm{N{\cdot}s/m}$다. 왜 상한 없이 두지 않으며, 상한은 무엇을 치르는가?

> [!tip]- 정답 · Answers
> 1. 파일 출력은 몇 밀리초씩 막힐 수 있고, 막힌 틱 동안 마지막 힘이 붙들리므로 실효 $T$가 커지고 $2b/T$가 벽의 강성 아래로 줄어든다. 처방은 햅틱 스레드를 결코 막지 않는 버퍼를 통해 데이터를 다른 스레드로 넘기는 것이다.
> 2. 서보 루프는 여전히 매 틱, 렌더링할 수 있는 강성으로 장치를 proxy 쪽으로 몬다. 낡은 것은 proxy의 위치뿐이므로, 손은 에너지를 받는 대신 옛 점에 붙잡힌다 — 끌림이다.
> 3. 틱당 한 카운트, $61.4\,\mathrm{mm/s}$다. $10\,\mathrm{mm/s}$에서는 $6.1$틱마다 카운트가 오므로 추정값은 다섯 번 $0$, 한 번 $61.4\,\mathrm{mm/s}$이고, 댐퍼 $B=0.4$는 꾸준한 $0.004\,\mathrm{N}$ 대신 $0.025\,\mathrm{N}$ 펄스를 낸다.
> 4. 많아야 $k_c=1000\,\mathrm{N/m}$. 바닥과 결합이 직렬이고, 강체 바닥이면 결합만 남는다. 장치는 결합만 렌더링하고, 시뮬레이션에 무엇이 있든 $1000<2(0.8-0.2)/0.001=1200\,\mathrm{N/m}$이므로 루프는 안정하다.
> 5. 전환 누설 — 벽이 스프링이 눌린 채 늦게 켜지고, 나간 뒤 한 주기 동안 민다. Gillespie와 Cutkosky는 문턱에서의 탈출 상태를 계산하는 감시와, 마지막 두 붙들린 힘을 데드비트로 고르는 것으로 그것을 없앤다.
> 6. 상한이 없으면 $v$가 틱당 한 카운트에 다가갈 때 $\alpha=-W/(Tv^2)$가 한없이 커진다. P3에서는 $2394\,\mathrm{N{\cdot}s/m}$에 이르러 $2\,\mathrm{N}$ 앰프에 $147\,\mathrm{N}$을 요구하고, 속도 잡음도 키운다. 상한의 대가는 완전성이다. 부족분이 늦게 갚아지거나 끝내 갚아지지 않으므로 관측기는 $0$ 대신 $-1.81\,\mathrm{mJ}$로 끝나고, 더 낮은 상한($0.4$)은 $1.01\,\mathrm{mm}$ 진동을 남긴다.

### 과제 · Problem set

Tier A. [[02-foundations/lab-plants|0.6]]의 **P3**, 이 페이지 대상의 손끝·벽·상한, 그리고 [[04-robotics/haptics-teleoperation/rendering-sampling-stability|24.4 §2]]의 샘플링 경계. 실습 코드는 연속 핸들을 서보 주기당 $40$개의 부분 스텝으로 시뮬레이션하고, 서보 틱 사이에는 힘을 붙든다.

1. **그리기.** 단단한 벽 대신 느린 힘 루프에 대한 위의 그림 — D와 E, 힘을 $5\,\mathrm{ms}$마다 다시 계산하는 카탈로그 $400\,\mathrm{N/m}$ 벽: 위 칸에는 관측기와 제어기가 있을 때와 없을 때의 처음 $0.6\,\mathrm{s}$의 $x(t)$를 벽과 평형을 표시해 그리고, 아래 칸에는 둘의 $1.5\,\mathrm{s}$ 동안의 $E_{\text{obs}}(t)$를 두 끝값을 적어 그려라.
2. **유도.** (a) 항등식 $\sum_k y_k(y_{k+1}-y_k)=\tfrac12(y_n^2-y_0^2)-\tfrac12\sum_k(y_{k+1}-y_k)^2$. (b) 힘을 $2\,\mathrm{ms}$마다, 그리고 $5\,\mathrm{ms}$마다 다시 계산할 때 P3에서 24.4의 경계를 통과하는 가장 큰 벽 강성. (c) 중심에서 $12\,\mathrm{mm}$인 장치 점에서 출발한, §4의 $20\,\mathrm{mm}$ 구에 대한 처음 두 시딩 스텝. (d) $1\,\mathrm{kHz}$의 P3에서 $k_c=1000\,\mathrm{N/m}$를 여전히 허락하는 가장 큰 결합 감쇠 $b_c$.
3. **실행.** 영어 절 템플릿의 `?`를 채워 계산 절의 다섯 실행을 재현하라. 그다음 C의 상한을 `0.4`와 `1e9`로 바꿔 꼬리와 $E_{\text{obs}}$를 보고하라.
4. **해석.** 어떤 보고서가 이렇게 말한다: "시간 영역 수동성 제어로, 우리의 1자유도 키트는 안정한 $5000\,\mathrm{N/m}$ 벽을 렌더링한다." 그 벽이 $5000\,\mathrm{N/m}$처럼 *느껴진다*고 믿기 전에 무엇 세 가지를 요구하겠는가? 그리고 그 결과는 대신 무엇을 뜻할 수 있는가?

> [!note]- 그리는 법 · How to draw it
> - 그림과 같은 두 칸이다. 위는 $0.6\,\mathrm{s}$ 동안의 밀리미터 단위 위치, 아래는 $1.5\,\mathrm{s}$ 동안의 밀리줄 단위 관측 에너지. 위 칸에는 벽 $x_w=30\,\mathrm{mm}$를, 아래 칸에는 $E_{\text{obs}}=0$을 점선으로 두고, 0 아래를 음영으로 칠한다.
> - 평형은 벽이 아니라 $31.5\,\mathrm{mm}$에 표시한다. $400\,\mathrm{N/m}$ 벽이면 손끝 스프링과 벽 스프링이 $3\,\mathrm{mm}$를 똑같이 나눈다.
> - 제어기 없이(점선): 약 $21\,\mathrm{Hz}$의 한계 순환 — 그림의 $34$보다 느리다 — 으로 약 $28.8$과 $34.1\,\mathrm{mm}$ 사이를 오가므로, 핸들은 매 주기 벽 밖으로 1밀리미터 넘게 나간다. 에너지는 거의 직선으로 $-69.7\,\mathrm{mJ}$까지, 그림의 네 배로 떨어진다.
> - 제어기와 함께(실선): 처음 약 $33.9\,\mathrm{mm}$까지 넘쳤다가, 약 $0.43\,\mathrm{s}$까지 $31.52\,\mathrm{mm}$의 $0.1\,\mathrm{mm}$ 안으로 줄어든다. 에너지는 처음 $0.1\,\mathrm{s}$에 약 $-1.5\,\mathrm{mJ}$로 떨어진 뒤 평평하게 머물러 $-1.44$로 끝난다.
> - 점선 곡선이 벽 안에만 머물면 그림이 틀린 것이다. 벽을 떠나지 않는 한계 순환은 누설이 결코 꺼지지 않으므로 끝없이 커질 것이다.

> [!tip]- 정답 · Solutions
> 1. 그리는 법 목록과 같다. 점선 $x(t)$는 $28.8$과 $34.1\,\mathrm{mm}$ 사이의 $21\,\mathrm{Hz}$ 한계 순환(꼬리 $5.277\,\mathrm{mm}$), $E_{\text{obs}}\to-69.7\,\mathrm{mJ}$. 실선 $x(t)$는 $0.43\,\mathrm{s}$까지 $31.52\,\mathrm{mm}$로 가라앉고(꼬리 $0.001\,\mathrm{mm}$), $E_{\text{obs}}$는 $0.1\,\mathrm{s}$ 뒤 $-1.44\,\mathrm{mJ}$ 근처에서 평평하다.
> 2. (a) 각 $k$에서 $y_k(y_{k+1}-y_k)=\tfrac12(y_{k+1}^2-y_k^2)-\tfrac12(y_{k+1}-y_k)^2$(우변을 전개한다). 더하면 첫 항이 망원급수로 줄어든다. (b) $2\,\mathrm{ms}$에서 $2b/T=2(0.8)/0.002=800\,\mathrm{N/m}$, $5\,\mathrm{ms}$에서 $320\,\mathrm{N/m}$. 카탈로그 벽은 앞의 것은 통과하고 뒤의 것은 실패한다. (c) $S=0.012^2-0.020^2=-2.56\times10^{-4}$, $\nabla S=0.024$, 스텝 $+10.67\,\mathrm{mm}$로 $22.67\,\mathrm{mm}$. 다음은 $S=1.138\times10^{-4}$, $\nabla S=0.0453$, 스텝 $-2.51\,\mathrm{mm}$로 $20.16\,\mathrm{mm}$(세 번째는 $20.0006$). 더 깊이서 출발하면 더 멀리 넘치지만, 뉴턴 스텝은 여전히 이차로 수렴한다. (d) $1000<2(0.8-b_c)/0.001$에서 $b_c<0.3\,\mathrm{N{\cdot}s/m}$.
> 3. 빈칸은 영어 절 정답과 같다. 채운 스크립트는 `A (33.53, 0.001, -0.32)`, `B (31.79, 1.658, -17.6)`, `C (31.79, 0.08, -1.81)`, `D (34.07, 5.277, -69.67)`, `E (33.9, 0.001, -1.44)`를 찍는다. 상한을 `0.4`로 하면 C는 꼬리 $1.012\,\mathrm{mm}$, $E_{\text{obs}}=-10.45\,\mathrm{mJ}$. `1e9`(앰프만 제한)이면 $0.069\,\mathrm{mm}$와 $-8.94\,\mathrm{mJ}$다. 핸들은 가라앉지만, 제어기가 요구한 소산의 대부분이 $2\,\mathrm{N}$ 앰프에 잘려 전달되지 않았으므로 에너지 계수는 상한이 있을 때보다 나쁘다.
> 4. (i) 실제로 느껴지는 강성, 곧 지속 접촉 중 힘을 침투로 나눈 값을 요구한다. 모든 진동을 감쇠하는 제어기는 명목상 $5000\,\mathrm{N/m}$ 벽을 단단한 댐퍼처럼 느끼게 만들 수 있다. (ii) 제어기가 얼마나 자주, 얼마나 세게, 얼마나 오래 작동했는지와 앰프의 포화 기록. 늘 켜진 제어기는 이름만 다른 최악의 경우 댐퍼다. (iii) 힘 갱신 주기와 사용한 쥠새. 단단한 쥠이나 감쇠가 있는 손은 그 자체로 벽을 안정시킨다(24.4). "안정"은 에너지 계수를 0 근처로 지켰다는 뜻일 뿐, 벽을 렌더링했다는 뜻이 아닐 수 있다.

### 출처

- K. Salisbury, F. Conti, F. Barbagli, "Haptic rendering: introductory concepts," *IEEE Computer Graphics and Applications* 24(2):24–32, 2004. DOI 10.1109/MCG.2004.1274058 — §1의 세 블록, 루프 단계, 다중 주기 구조.
- M. A. Srinivasan, C. Basdogan, "Haptics in virtual environments: taxonomy, research status, and challenges," *Computers & Graphics* 21(4):393–404, 1997. DOI 10.1016/S0097-8493(97)00030-7 — 두 감각운동 루프, 중간 표현의 불연속, 법선 흔들기로 만든 질감.
- Y. Adachi, T. Kumano, K. Ogino, "Intermediate representation for stiff virtual objects," *Proc. IEEE VRAIS*, 1995, pp. 203–210.
- D. C. Ruspini, K. Kolarov, O. Khatib, "Haptic interaction in virtual environments," *Proc. IEEE/RSJ IROS*, 1997, pp. 128–133 — 서보 제어와 proxy 갱신의 분리, 두 번에 나눈 힘 셰이딩.
- CHAI3D 문서, [chai3d.org](https://www.chai3d.org/documentation) — §1의 그래픽 스레드와 햅틱 스레드로 짜인 오픈소스 라이브러리.
- K. Salisbury, C. Tarr, "Haptic rendering of surfaces defined by implicit functions," *Proc. ASME Dynamic Systems and Control Division*, DSC-Vol. 61, 1997, pp. 61–67 — 시딩과 표면 추적.
- H. B. Morgenbesser, M. A. Srinivasan, "Force shading for haptic shape perception," *Proc. ASME Dynamic Systems and Control Division*, DSC-Vol. 58, 1996, pp. 407–412.
- J. E. Colgate, M. C. Stanley, J. M. Brown, "Issues in the haptic display of tool use," *Proc. IEEE/RSJ IROS*, 1995, pp. 140–145; R. J. Adams, B. Hannaford, "Stable haptic interaction with virtual environments," *IEEE Transactions on Robotics and Automation* 15(3):465–474, 1999 — 가상 결합.
- R. B. Gillespie, M. R. Cutkosky, "Stable user-specific haptic rendering of the virtual wall," *Proc. ASME IMECE*, DSC-Vol. 58, 1996, pp. 397–406 — §5의 두 에너지 누설, 튀는 공 시험대, 반 샘플 예측, 디지털 영역 설계, 데드비트 보정.
- B. Hannaford, J.-H. Ryu, "Time-domain passivity control of haptic interfaces," *IEEE Transactions on Robotics and Automation* 18(1):1–10, 2002. DOI 10.1109/70.988969 — §6의 관측기, 제어기, 인용한 실험과 한계.
- 이 페이지의 숫자는 논문 이름을 댄 곳을 빼면 인용이 아니라 적힌 매개변수로 여기서 계산한 것이다. 실습 코드로 다시 계산하라.
