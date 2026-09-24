---
title: 2. Experimental Design & Reproducibility
tags: [research, experiments, reproducibility]
study-depth: Working
wiki-support: Working
depth-goal: "On RS1, work out by hand how many trials each outcome needs, check those numbers against a simulated experiment, and build the matched, reproducible design around them."
mastery-when: "Mastery means consistently producing defensible work, not memorizing the page."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/ml-practice|9. ML Practice & Evaluation]] (reading a result; the percentile bootstrap in its worked case) · [[02-foundations/probability|3. Probability §6]] (α, the p-value, power as a detection probability, the confidence-interval procedure, the test-choice table) · [[02-foundations/probability|3. Probability §3]] (the CLT behind every normal approximation) · plants P2 and P3 from [[02-foundations/lab-plants|0.6 Lab Plants]]
> [[02-foundations/ml-practice|9. ML 실무와 평가]](결과 읽기, 그 worked case의 백분위 부트스트랩) · [[02-foundations/probability|3. 확률 §6]](α, p-값, 검출 확률로서의 검정력, 신뢰구간 절차, 검정 선택 표) · [[02-foundations/probability|3. 확률 §3]](모든 정규근사 뒤에 있는 CLT) · [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 P2와 P3

## English

*Stands on [[02-foundations/ml-practice|9. ML Practice]], which reads a finished result, and [[02-foundations/probability|3. Probability §6]], which supplies the tests. Runs on RS1, the study every Research Practice page shares, and is the wiki's home for power analysis.*

An experiment should distinguish the proposed explanation from plausible alternatives. In robotics, this requires controlling not only models and datasets but scenes, hardware, calibration, operators, resets, timing, and exposure to failures.

> [!note] First pass · 처음이라면
> Read the running object — RS1 and its frozen pilot — and then the worked case, which defines α, power, effect size and the confidence interval on it and works both sample sizes by hand. Then the lab in §4, which checks those numbers by simulating the experiment. §1–§3 and §8 turn RS1 into a design; §5–§7 are what you check before the first trial.

### Running object · 이 페이지의 대상

**RS1**, the running study of every Research Practice page. It is a study, not a machine, so it is specified here in full; its hardware comes from the catalog, and every number below is fixed.

- **Question.** Does impedance control (**B**) make the planar arm's contact with a panel safer than position control with a force-threshold stop (**A**)?
- **Arm and panel.** The arm is plant **P2** from [[02-foundations/lab-plants|0.6 Lab Plants]]. The panel's stiffness is **P3**'s wall, $k_w = 400\ \mathrm{N/m}$.
- **Trial and outcome.** One trial is one approach to the panel ending in contact. It yields one number, the peak contact force $F$ in newtons, and it counts as a success when $F \le 10\ \mathrm{N}$.
- **Pilot.** Ten trials per controller. The forces are illustrative — invented for teaching, not measured — and frozen: no page changes them.

| controller | peak contact force, trials 1–10 (N) | successes | mean | sample sd | median |
|---|---|---:|---:|---:|---:|
| A — position control + force-threshold stop | 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 | 6/10 | 10.66 | 2.414 | 9.85 |
| B — impedance control | 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 | 9/10 | 7.50 | 1.356 | 7.30 |

RS1 is a study rather than a plant, so this page's lab simulates trial *outcomes*, not the arm's dynamics, and the integrators of [[02-foundations/lab-kernel|0.7 Lab Kernel]] are not used. Where a contact's dynamics are simulated instead, the integrator becomes part of the outcome: in Step 5 of the worked case of [[06-research-practice/simulators-benchmarks-datasets|7. Simulators, Benchmarks & Datasets]] one drop of P3's handle on a stiff wall peaks at an exact 6 N, a pass by RS1's rule, and at 12 N, a failure, under explicit Euler, with no controller changed.

*Scope: this page teaches how to design the experiment that answers RS1 — what to vary, hold fixed and count (§1–§3), how many trials to run, by formula and by simulation (the worked case and §4), how to budget an ablation (§5), and what to record so that the result can be repeated, reproduced and replicated (§6–§7). It does not teach how to read the finished results table, which is [[02-foundations/ml-practice|9. ML Practice & Evaluation]]; the tests themselves, which are [[02-foundations/probability|3. Probability §6]]; the two controllers, which are [[04-robotics/force-compliance-control|13. Force & Compliance Control]]; or how to diagnose the failures the trials will produce, which is [[06-research-practice/failure-analysis-system-evaluation|3. Failure Analysis & System Evaluation]].*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 640 262" style="max-width:100%;height:auto" role="img" aria-label="the two sampling distributions behind a power calculation, for RS1's success rate at 32 trials per arm and its peak force at 7">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="30" y1="172" x2="310" y2="172"/><line x1="345" y1="172" x2="625" y2="172"/></g>
  <g fill="currentColor" stroke="none"><path d="M179.9 172L179.9 100.5L183.2 93.2L186.4 86.4L189.7 80.4L192.9 75.4L196.2 71.6L199.4 69.1L202.7 68.0L205.9 68.5L209.2 70.4L212.4 73.7L215.7 78.3L218.9 83.9L222.2 90.4L225.4 97.5L228.7 104.9L231.9 112.5L235.2 120.0L238.5 127.1L241.7 133.9L245.0 140.1L248.2 145.7L251.5 150.6L254.7 154.8L258.0 158.4L261.2 161.4L264.5 163.9L267.7 165.8L271.0 167.4L274.2 168.6L277.5 169.5L280.7 170.2L284.0 170.8L287.2 171.1L290.5 171.4L293.7 171.6L297.0 171.7L300.2 171.8L303.5 171.9L306.7 171.9L310.0 172.0L310.0 172Z" opacity="0.16"/><path d="M493.0 172L493.0 112.7L496.3 105.2L499.6 97.9L502.9 90.9L506.2 84.4L509.5 78.8L512.8 74.2L516.1 70.8L519.4 68.7L522.7 68.0L526.0 68.8L529.3 71.0L532.6 74.5L535.9 79.2L539.2 84.9L542.5 91.4L545.8 98.4L549.1 105.8L552.4 113.2L555.7 120.6L559.0 127.6L562.3 134.2L565.6 140.3L568.9 145.8L572.2 150.6L575.5 154.8L578.8 158.3L582.1 161.3L585.4 163.7L588.7 165.7L592.0 167.3L595.3 168.5L598.6 169.5L601.9 170.2L605.2 170.7L608.5 171.1L611.8 171.4L615.1 171.6L618.4 171.7L621.7 171.8L625.0 171.9L625.0 172Z" opacity="0.16"/><path d="M179.9 172L179.9 157.7L183.2 160.6L186.4 163.0L189.7 165.0L192.9 166.7L196.2 168.0L199.4 169.0L202.7 169.8L205.9 170.4L209.2 170.8L212.4 171.2L215.7 171.4L218.9 171.6L222.2 171.7L225.4 171.8L228.7 171.9L231.9 171.9L235.2 171.9L238.5 172.0L241.7 172.0L245.0 172.0L248.2 172.0L251.5 172.0L254.7 172.0L258.0 172.0L261.2 172.0L264.5 172.0L267.7 172.0L271.0 172.0L274.2 172.0L277.5 172.0L280.7 172.0L284.0 172.0L287.2 172.0L290.5 172.0L293.7 172.0L297.0 172.0L300.2 172.0L303.5 172.0L306.7 172.0L310.0 172.0L310.0 172Z" opacity="0.5"/><path d="M30.0 172L30.0 171.5L30.9 171.4L31.8 171.4L32.8 171.3L33.7 171.2L34.6 171.1L35.5 171.0L36.4 170.9L37.4 170.8L38.3 170.7L39.2 170.6L40.1 170.5L41.0 170.3L41.9 170.2L42.9 170.0L43.8 169.8L44.7 169.6L45.6 169.4L46.5 169.2L47.5 168.9L48.4 168.6L49.3 168.4L50.2 168.1L51.1 167.7L52.1 167.4L53.0 167.0L53.9 166.6L54.8 166.2L55.7 165.7L56.6 165.2L57.6 164.7L58.5 164.2L59.4 163.6L60.3 163.0L61.2 162.3L62.2 161.7L63.1 161.0L64.0 160.2L64.9 159.4L65.8 158.6L66.8 157.7L66.8 172Z" opacity="0.5"/><path d="M493.0 172L493.0 156.8L496.3 160.0L499.6 162.7L502.9 164.9L506.2 166.6L509.5 168.0L512.8 169.0L516.1 169.9L519.4 170.5L522.7 170.9L526.0 171.3L529.3 171.5L532.6 171.7L535.9 171.8L539.2 171.8L542.5 171.9L545.8 171.9L549.1 172.0L552.4 172.0L555.7 172.0L559.0 172.0L562.3 172.0L565.6 172.0L568.9 172.0L572.2 172.0L575.5 172.0L578.8 172.0L582.1 172.0L585.4 172.0L588.7 172.0L592.0 172.0L595.3 172.0L598.6 172.0L601.9 172.0L605.2 172.0L608.5 172.0L611.8 172.0L615.1 172.0L618.4 172.0L621.7 172.0L625.0 172.0L625.0 172Z" opacity="0.5"/><path d="M345.0 172L345.0 171.6L346.0 171.6L346.9 171.5L347.9 171.5L348.9 171.4L349.8 171.3L350.8 171.2L351.8 171.2L352.7 171.1L353.7 171.0L354.7 170.8L355.6 170.7L356.6 170.6L357.6 170.4L358.5 170.3L359.5 170.1L360.5 169.9L361.4 169.7L362.4 169.4L363.4 169.2L364.3 168.9L365.3 168.6L366.2 168.3L367.2 168.0L368.2 167.6L369.1 167.2L370.1 166.8L371.1 166.3L372.0 165.8L373.0 165.3L374.0 164.7L374.9 164.1L375.9 163.5L376.9 162.8L377.8 162.1L378.8 161.3L379.8 160.5L380.7 159.6L381.7 158.7L382.7 157.8L383.6 156.8L383.6 172Z" opacity="0.5"/></g>
  <path d="M30.0 171.5 L33.1 171.3 L36.2 171.0 L39.3 170.6 L42.4 170.1 L45.6 169.4 L48.7 168.6 L51.8 167.5 L54.9 166.1 L58.0 164.5 L61.1 162.4 L64.2 160.0 L67.3 157.1 L70.4 153.8 L73.6 149.9 L76.7 145.6 L79.8 140.7 L82.9 135.4 L86.0 129.7 L89.1 123.7 L92.2 117.4 L95.3 111.0 L98.4 104.7 L101.6 98.6 L104.7 92.8 L107.8 87.6 L110.9 83.1 L114.0 79.4 L117.1 76.7 L120.2 75.0 L123.3 74.4 L126.4 75.0 L129.6 76.7 L132.7 79.4 L135.8 83.1 L138.9 87.6 L142.0 92.8 L145.1 98.6 L148.2 104.7 L151.3 111.0 L154.4 117.4 L157.6 123.7 L160.7 129.7 L163.8 135.4 L166.9 140.7 L170.0 145.6 L173.1 149.9 L176.2 153.8 L179.3 157.1 L182.4 160.0 L185.6 162.4 L188.7 164.5 L191.8 166.1 L194.9 167.5 L198.0 168.6 L201.1 169.4 L204.2 170.1 L207.3 170.6 L210.4 171.0 L213.6 171.3 L216.7 171.5 L219.8 171.6 L222.9 171.7 L226.0 171.8 L229.1 171.9 L232.2 171.9 L235.3 171.9 L238.4 172.0 L241.6 172.0 L244.7 172.0 L247.8 172.0 L250.9 172.0 L254.0 172.0 L257.1 172.0 L260.2 172.0 L263.3 172.0 L266.4 172.0 L269.6 172.0 L272.7 172.0 L275.8 172.0 L278.9 172.0 L282.0 172.0 L285.1 172.0 L288.2 172.0 L291.3 172.0 L294.4 172.0 L297.6 172.0 L300.7 172.0 L303.8 172.0 L306.9 172.0 L310.0 172.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4" opacity="0.75"/>
  <path d="M30.0 172.0 L33.1 172.0 L36.2 172.0 L39.3 172.0 L42.4 172.0 L45.6 172.0 L48.7 172.0 L51.8 172.0 L54.9 172.0 L58.0 172.0 L61.1 172.0 L64.2 172.0 L67.3 172.0 L70.4 172.0 L73.6 172.0 L76.7 172.0 L79.8 172.0 L82.9 172.0 L86.0 172.0 L89.1 172.0 L92.2 172.0 L95.3 172.0 L98.4 171.9 L101.6 171.9 L104.7 171.9 L107.8 171.8 L110.9 171.7 L114.0 171.5 L117.1 171.3 L120.2 171.1 L123.3 170.7 L126.4 170.2 L129.6 169.5 L132.7 168.5 L135.8 167.4 L138.9 165.9 L142.0 164.0 L145.1 161.7 L148.2 158.9 L151.3 155.5 L154.4 151.6 L157.6 147.1 L160.7 141.9 L163.8 136.2 L166.9 130.0 L170.0 123.2 L173.1 116.2 L176.2 109.0 L179.3 101.8 L182.4 94.8 L185.6 88.2 L188.7 82.2 L191.8 77.1 L194.9 72.9 L198.0 70.0 L201.1 68.3 L204.2 68.1 L207.3 69.1 L210.4 71.5 L213.6 75.2 L216.7 79.9 L219.8 85.5 L222.9 91.9 L226.0 98.7 L229.1 105.9 L232.2 113.1 L235.3 120.3 L238.4 127.1 L241.6 133.6 L244.7 139.6 L247.8 145.0 L250.9 149.7 L254.0 153.9 L257.1 157.5 L260.2 160.6 L263.3 163.1 L266.4 165.1 L269.6 166.8 L272.7 168.1 L275.8 169.1 L278.9 169.9 L282.0 170.5 L285.1 170.9 L288.2 171.2 L291.3 171.5 L294.4 171.6 L297.6 171.8 L300.7 171.8 L303.8 171.9 L306.9 171.9 L310.0 172.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M345.0 171.6 L348.1 171.4 L351.2 171.2 L354.3 170.9 L357.4 170.4 L360.6 169.9 L363.7 169.1 L366.8 168.1 L369.9 166.9 L373.0 165.3 L376.1 163.3 L379.2 161.0 L382.3 158.1 L385.4 154.7 L388.6 150.8 L391.7 146.3 L394.8 141.2 L397.9 135.6 L401.0 129.5 L404.1 123.0 L407.2 116.1 L410.3 109.1 L413.4 102.1 L416.6 95.3 L419.7 88.8 L422.8 83.0 L425.9 77.8 L429.0 73.7 L432.1 70.6 L435.2 68.6 L438.3 68.0 L441.4 68.6 L444.6 70.6 L447.7 73.7 L450.8 77.8 L453.9 83.0 L457.0 88.8 L460.1 95.3 L463.2 102.1 L466.3 109.1 L469.4 116.1 L472.6 123.0 L475.7 129.5 L478.8 135.6 L481.9 141.2 L485.0 146.3 L488.1 150.8 L491.2 154.7 L494.3 158.1 L497.4 161.0 L500.6 163.3 L503.7 165.3 L506.8 166.9 L509.9 168.1 L513.0 169.1 L516.1 169.9 L519.2 170.4 L522.3 170.9 L525.4 171.2 L528.6 171.4 L531.7 171.6 L534.8 171.7 L537.9 171.8 L541.0 171.9 L544.1 171.9 L547.2 171.9 L550.3 172.0 L553.4 172.0 L556.6 172.0 L559.7 172.0 L562.8 172.0 L565.9 172.0 L569.0 172.0 L572.1 172.0 L575.2 172.0 L578.3 172.0 L581.4 172.0 L584.6 172.0 L587.7 172.0 L590.8 172.0 L593.9 172.0 L597.0 172.0 L600.1 172.0 L603.2 172.0 L606.3 172.0 L609.4 172.0 L612.6 172.0 L615.7 172.0 L618.8 172.0 L621.9 172.0 L625.0 172.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4" opacity="0.75"/>
  <path d="M345.0 172.0 L348.1 172.0 L351.2 172.0 L354.3 172.0 L357.4 172.0 L360.6 172.0 L363.7 172.0 L366.8 172.0 L369.9 172.0 L373.0 172.0 L376.1 172.0 L379.2 172.0 L382.3 172.0 L385.4 172.0 L388.6 172.0 L391.7 172.0 L394.8 172.0 L397.9 172.0 L401.0 172.0 L404.1 172.0 L407.2 172.0 L410.3 172.0 L413.4 172.0 L416.6 171.9 L419.7 171.9 L422.8 171.8 L425.9 171.7 L429.0 171.6 L432.1 171.5 L435.2 171.2 L438.3 170.9 L441.4 170.5 L444.6 169.9 L447.7 169.2 L450.8 168.2 L453.9 167.0 L457.0 165.4 L460.1 163.5 L463.2 161.2 L466.3 158.4 L469.4 155.0 L472.6 151.2 L475.7 146.7 L478.8 141.7 L481.9 136.1 L485.0 130.0 L488.1 123.5 L491.2 116.7 L494.3 109.7 L497.4 102.7 L500.6 95.9 L503.7 89.4 L506.8 83.4 L509.9 78.2 L513.0 74.0 L516.1 70.8 L519.2 68.8 L522.3 68.0 L525.4 68.5 L528.6 70.3 L531.7 73.3 L534.8 77.4 L537.9 82.5 L541.0 88.3 L544.1 94.7 L547.2 101.5 L550.3 108.5 L553.4 115.5 L556.6 122.4 L559.7 128.9 L562.8 135.1 L565.9 140.8 L569.0 145.9 L572.1 150.4 L575.2 154.4 L578.3 157.8 L581.4 160.7 L584.6 163.2 L587.7 165.1 L590.8 166.7 L593.9 168.0 L597.0 169.0 L600.1 169.8 L603.2 170.4 L606.3 170.8 L609.4 171.2 L612.6 171.4 L615.7 171.6 L618.8 171.7 L621.9 171.8 L625.0 171.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.8"><line x1="179.9" y1="52" x2="179.9" y2="172"/><line x1="66.8" y1="112" x2="66.8" y2="172"/><line x1="493.0" y1="52" x2="493.0" y2="172"/><line x1="383.6" y1="112" x2="383.6" y2="172"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="70.0" y1="172" x2="70.0" y2="177"/><line x1="123.3" y1="172" x2="123.3" y2="177"/><line x1="176.7" y1="172" x2="176.7" y2="177"/><line x1="230.0" y1="172" x2="230.0" y2="177"/><line x1="283.3" y1="172" x2="283.3" y2="177"/><line x1="385.0" y1="172" x2="385.0" y2="177"/><line x1="438.3" y1="172" x2="438.3" y2="177"/><line x1="491.7" y1="172" x2="491.7" y2="177"/><line x1="545.0" y1="172" x2="545.0" y2="177"/><line x1="598.3" y1="172" x2="598.3" y2="177"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="70.0" y="188">-0.2</text><text x="123.3" y="188">0</text><text x="176.7" y="188">0.2</text><text x="230.0" y="188">0.4</text><text x="283.3" y="188">0.6</text><text x="385.0" y="188">-2</text><text x="438.3" y="188">0</text><text x="491.7" y="188">2</text><text x="545.0" y="188">4</text><text x="598.3" y="188">6</text></g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="170" y="20" font-weight="bold">(a) success rate, 32 trials per arm</text><text x="485" y="20" font-weight="bold">(b) peak force, 7 trials per arm</text>
    <text x="170" y="202">estimated gap in success rate</text><text x="485" y="202">estimated gap in mean peak force (N)</text>
    <text x="118.0" y="68.4">H<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="208.7" y="62.0">H<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="433.0" y="62.0">H<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="527.9" y="62.0">H<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="179.9" y="46">c = 0.212</text><text x="493.0" y="46">c = 2.05 N</text>
    <text x="211.3" y="140">power 0.81</text><text x="530.3" y="140">power 0.86</text>
    <text x="160.7" y="166" font-size="9.5">β 0.19</text><text x="474.3" y="166" font-size="9.5">β 0.14</text>
  </g>
  <g font-size="10" fill="currentColor">
    <text x="30" y="232">dashed: A and B equal (H<tspan dy="3.5">0</tspan><tspan dy="-3.5">) · solid: the pilot’s effect is real (H</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">)</tspan></text>
    <text x="30" y="250">light fill: power, under H<tspan dy="3.5">1</tspan><tspan dy="-3.5"> beyond c · dark fill: the two α/2 = 0.025 tails of H</tspan><tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text>
  </g>
</svg>

The two sampling distributions behind RS1's sample sizes — of the estimated gap if A and B are equal ($H_0$, dashed) and if the pilot's effect is real ($H_1$, solid) — for (a) the success rate at 32 trials per arm and (b) the peak force at 7. The critical value, $c = 0.212$ and $c = 2.05$ N, leaves $\alpha/2 = 0.025$ in each dashed tail, and power is the solid curve's area beyond it: 0.81 and 0.86, so $\beta$ is 0.19 and 0.14. In both panels the alternative sits about three null standard errors from zero, 2.77 and 3.02, and that ratio is all that power reads: the success rate needs 32 trials per arm to get there, the force only 7.

### Worked case · 대상으로 한 번 끝까지

The page in one calculation: what the pilot says, and then how many trials the confirmatory experiment needs for each of RS1's two outcomes, by hand. The lab in §4 checks every number here by simulation.

**Step 1 — the pilot, summarized.** From the table, A succeeds on 6 of 10 trials and B on 9 of 10. B's mean peak force is $10.66 - 7.50 = 3.16$ N lower. The sample standard deviations (divisor $n - 1$, [[02-foundations/ml-practice|9. ML Practice §4]]) are 2.414 N and 1.356 N. A's mean lies above its median, 10.66 against 9.85, because its four failures reach far (up to 14.8 N) while its successes crowd under the line: four of the six lie between 9.1 and 9.9 N. Step 5 needs that crowding.

Four quantities decide every sample size. Each is defined once here and used for the rest of the page.

> [!info] Definition — significance level α
> **What kind of thing it is:** a probability that is *chosen*, not measured — the false-alarm rate a test is allowed, which [[02-foundations/probability|3. Probability §6]] calls the type I error rate. Three conditions: (1) it is fixed **before** the data exist; (2) it is a property of the **decision rule when $H_0$ is true**, computed as if the two controllers were equal; (3) in a two-sided test it is split equally between the two tails, so the critical value is $z_{1-\alpha/2}$.
> $$\alpha = P\big(\text{reject } H_0 \mid H_0 \text{ true}\big) = P\big(|Z| > z_{1-\alpha/2}\big)$$
> where $Z$ is the test statistic standardized under $H_0$ and $z_q$ is the standard-normal quantile with $P(Z \le z_q) = q$.
> **Example.** RS1 uses $\alpha = 0.05$, two-sided, so $z_{0.975} = 1.960$.
> **Non-example.** The pilot's $p = 0.12$ for the success rates. A p-value is computed from the data and then compared with α, which was chosen before any data existed; and neither one is the probability that $H_0$ is true.
> **Why it matters.** α sets the critical value, and the critical value is the first of the two terms in every sample-size formula below.

> [!info] Definition — statistical power, 1 − β
> **What kind of thing it is:** a probability, and a property of a **design** rather than of a dataset — the chance that the planned experiment rejects $H_0$ when a stated effect is real. It is the detection probability $P_D$ of [[02-foundations/probability|3. Probability §6]], applied to a claim. Four things must be named before it has a value: (1) the **true effect** assumed under $H_1$; (2) the **test** and its α; (3) the **number of trials** per arm; (4) the **design**, independent arms or pairs. Change any one and the power changes, so "the study had 80% power" with no effect named is not a claim.
> $$1 - \beta = P\big(\text{reject } H_0 \mid H_1:\ \text{true difference} = \Delta\big)$$
> where $\beta$ is the miss (type II error) rate at that effect and $\Delta$ is the assumed true difference.
> **Example.** RS1's success rate at 32 trials per arm, α = 0.05, true rates 0.6 and 0.9: power 0.81 (step 3).
> **Non-example.** "Observed power," computed after a non-significant result by plugging the observed effect back in. It is a fixed function of the p-value and so says nothing the p-value did not (Hoenig & Heisey 2001). Nor is power the probability that $H_1$ is true.
> **Why it matters.** A study with low power usually fails to reject even when the effect is real — the pilot is one — and when it does reject, its estimate is inflated; the lab in §4 measures by how much.

> [!info] Definition — effect size
> **What kind of thing it is:** a population quantity — a parameter, which the sample only estimates — saying **how large** a difference is on a stated scale. Three conditions: (1) it belongs to the **population**, so the pilot's value is an estimate; (2) it does **not grow with $n$** — more trials sharpen its estimate but leave it unchanged; (3) its **scale** is stated, either raw (newtons, percentage points) or standardized by the spread. For the force the standardized version is **Cohen's d**:
> $$d = \frac{\mu_A - \mu_B}{\sigma}, \qquad \hat d = \frac{\bar F_A - \bar F_B}{s_p}, \qquad s_p = \sqrt{\frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}}$$
> where $\mu_A$ and $\mu_B$ are the true mean peak forces, $\sigma$ their common standard deviation and $s_p$ the pooled sample standard deviation, so $d$ is the difference measured in units of spread. For the success rate the effect size is the difference $p_B - p_A$ itself.
> **Example.** The pilot: $s_p = \sqrt{(9 \times 2.414^2 + 9 \times 1.356^2)/18} = 1.958$ N and $\hat d = 3.16/1.958 = 1.614$; for the success rate, $0.9 - 0.6 = 0.30$.
> **Non-example.** The pilot's $t = 3.61$ or its $p = 0.0028$. With equal arms $t = \hat d\sqrt{n/2}$ exactly — $1.614 \times \sqrt 5 = 3.61$ — so the same effect earns a larger $t$ and a smaller $p$ with every added trial. They measure the effect and the sample size together.
> **Why it matters.** It is the input every sample-size formula needs, and the number a reader weighs for practical importance ([[02-foundations/ml-practice|9. ML Practice §5]]).

> [!info] Definition — confidence interval, for a difference of means
> **What kind of thing it is:** a **procedure** that maps a dataset to an interval, defined in general in [[02-foundations/probability|3. Probability §6]]; here, the one RS1's analysis will print. Three conditions: (1) the endpoints are **random**, computed from the data, while the true difference is fixed; (2) over repeated experiments the interval **covers** the true difference with probability $1 - \alpha$; (3) that coverage holds only under the procedure's assumptions — here independent trials and roughly normal means.
> $$\big(\bar F_A - \bar F_B\big) \pm t_{0.975,\,\nu}\sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}$$
> where the square root is Welch's standard error of the difference and $\nu$ its Welch–Satterthwaite degrees of freedom, so neither arm is assumed to share the other's spread.
> **Example.** The pilot: $3.16 \pm 2.142 \times 0.8756 = [1.28,\ 5.04]$ N, with $\nu = 14.16$.
> **Non-example.** "B lowers the peak force by 1.28 to 5.04 N with 95% probability" — once computed, the interval either covers the truth or it does not; the 95% belongs to the procedure. And the percentile bootstrap of the same trials, $[1.58,\ 4.80]$ N in §4's lab, is narrower not because it knows more but because it ignores that both spreads were estimated from ten trials: in 4,000 simulated normal pilots of this size it covered the true difference 92% of the time, Welch's interval 95% — the thin-data failure of the bootstrap in [[02-foundations/ml-practice|9. ML Practice]]'s worked case, part 4.
> **Why it matters.** Its half-width is the precision the experiment buys, and planning for a half-width is the other way to choose the number of trials (§4).

**Step 2 — the pilot's own two tests.** *The force.* Welch's standard error is $\sqrt{2.414^2/10 + 1.356^2/10} = 0.8756$ N, so $t = 3.16/0.8756 = 3.61$ on $\nu = 14.16$ degrees of freedom, two-sided $p = 0.0028$, with the 95% interval $[1.28,\ 5.04]$ N: strong evidence that B lowers the peak force. *The success rate.* The pooled two-proportion $z$-test uses $\bar p = 0.75$ and $\mathrm{SE}_0 = \sqrt{0.75 \times 0.25 \times 2/10} = 0.194$, so $z = 0.30/0.194 = 1.55$ and $p = 0.12$; Fisher's exact test, the choice for a small 2×2 table in [[02-foundations/probability|3. Probability §6]], gives $p = 0.30$. The same twenty trials read as strong evidence one way and as no evidence the other. Nothing contradicts: the binary reading of a ten-trial pilot had little chance of seeing a real difference. If the true rates are 0.6 and 0.9, ten trials per arm give power 0.33 by step 3's formula — the lab finds 0.30 for the $z$-test and 0.16 for Fisher's — so "not significant" was the likely result even with B truly safer. That is misreading 3 of [[02-foundations/probability|3. Probability §6]], in numbers. What the success comparison is compatible with is an interval rather than a p-value: Newcombe's 95% interval for the difference, $-0.08$ to $+0.60$, defined and worked in [[06-research-practice/scientific-writing-peer-review|4. Scientific Writing & Peer Review]]'s worked case.

**Step 3 — trials per arm for the success rate.** Write $\hat D = \hat p_B - \hat p_A$ for the difference the experiment will estimate from $n$ trials per arm, and $q = 1 - p$. By the CLT ([[02-foundations/probability|3. Probability §3]]) each $\hat p$ is approximately normal with variance $pq/n$, and independent arms add their variances, so

- if the controllers are equal, both rates are the average $\bar p = (p_A + p_B)/2$ and $\hat D \sim \mathcal N(0,\ 2\bar p\bar q/n)$;
- if they are not, $\hat D \sim \mathcal N(\Delta,\ (p_Aq_A + p_Bq_B)/n)$, with $\Delta = p_B - p_A$.

The test rejects when $|\hat D| > c$ with $c = z_{1-\alpha/2}\sqrt{2\bar p\bar q/n}$, which gives it the false-alarm rate α. Its power is the probability under $H_1$ of landing beyond $c$; the other tail, below $-c$, holds about $2 \times 10^{-7}$ at RS1's numbers and is dropped:

$$1 - \beta = \Phi\left(\frac{\Delta\sqrt n - z_{1-\alpha/2}\sqrt{2\bar p\bar q}}{\sqrt{p_Aq_A + p_Bq_B}}\right)$$

since standardizing $P(\hat D > c)$ under $H_1$ subtracts $\Delta$ and divides by $\sqrt{(p_Aq_A + p_Bq_B)/n}$. Set this equal to the target power and solve for $n$, using $\Phi^{-1}(1 - \beta) = z_{1-\beta}$:

$$n = \frac{\Big(z_{1-\alpha/2}\sqrt{2\bar p\bar q} + z_{1-\beta}\sqrt{p_Aq_A + p_Bq_B}\Big)^2}{(p_B - p_A)^2}$$

because the numerator inside $\Phi$ must equal $z_{1-\beta}$ times its denominator. This is the normal-approximation sample size for two independent proportions (Fleiss, Levin & Paik 2003). On RS1, with $p_A = 0.6$, $p_B = 0.9$, α = 0.05 two-sided and power 0.8:

- $\bar p = 0.75$, $z_{0.975} = 1.960$, $z_{0.80} = 0.842$;
- $\sqrt{2 \times 0.75 \times 0.25} = 0.6124$ and $\sqrt{0.6 \times 0.4 + 0.9 \times 0.1} = \sqrt{0.33} = 0.5745$;
- the numerator is $(1.960 \times 0.6124 + 0.842 \times 0.5745)^2 = (1.2002 + 0.4835)^2 = 1.6837^2 = 2.8348$;
- $n = 2.8348/0.30^2 = 31.5$, so **32 trials per arm, 64 in all**, and at $n = 32$ the power formula gives 0.81.

The formula belongs to a test. Put the $H_1$ variance in both terms and it gives 28.8; add the continuity correction of the same reference, meant to track an exact test, and it gives 37.9. Plan with the test you will run: Fisher's exact test at 32 per arm has power 0.74, not 0.81 (§4).

**Step 4 — trials per arm for the force.** For a difference of two means with a common standard deviation $\sigma$, the same two-curve argument has $\mathrm{SE} = \sigma\sqrt{2/n}$ under both hypotheses, so the two terms merge:

$$n = \frac{2\big(z_{1-\alpha/2} + z_{1-\beta}\big)^2\sigma^2}{\Delta^2} = \frac{2\big(z_{1-\alpha/2} + z_{1-\beta}\big)^2}{d^2}$$

since $d = \Delta/\sigma$ is Cohen's d. With the pilot's $\hat d = 1.614$: $n = 2 \times (1.960 + 0.842)^2/1.614^2 = 2 \times 7.849/2.605 = 6.03$, so **7 per arm** after rounding up. The normal approximation treats $\sigma$ as known. The analysis will estimate it, and the $t$ critical value on $2n - 2$ degrees of freedom is larger than 1.960 at small $n$ — $t_{0.975,\,12} = 2.179$ — so the $t$-test's real power is lower: the lab measures 0.79 at 7 per arm and 0.86 at 8. The $t$-based answer is **8 per arm**.

**Step 5 — why the force needs a fifth of the trials.** 31.5 against 6.03 is a factor of 5.2; after rounding and the $t$ correction, 32 against 8 is a factor of 4. Two things multiply into it, and only one of them is the outcome's fault.

- *Cutting at 10 N throws information away.* A success at 9.9 N counts the same as one at 6.2 N, and a failure at 10.6 N the same as one at 14.8 N. Suppose the forces really were normal with the pilot's means and pooled $\sigma = 1.958$ N. The success rates would then be $\Phi\big((10 - 10.66)/1.958\big) = 0.37$ for A and $\Phi\big((10 - 7.50)/1.958\big) = 0.90$ for B, and step 3's formula at those rates asks for 11.7 per arm — about twice the 6.03 that the forces need **from the same experiment**. The lab measures this directly by analysing every simulated experiment both ways.
- *The pilot's two summaries disagree about the size of the effect.* Its observed rates, 0.6 and 0.9, are 0.30 apart; the normal model fitted to its forces implies 0.53. A's successes crowded just under the line are the reason. The remaining factor, $31.5/11.7 = 2.7$, is that disagreement, and ten trials per arm cannot settle it.

So record and analyse the force, and report the success rate beside it, since the 10 N line is what a reader of RS1 cares about. Declare which of the two is primary before the first trial (§4). The worked case of [[06-research-practice/real-world-impact|6. Real-World Impact]] prices the same two outcomes per rung of evidence: the pilot sits on the simulation rung, and repeating it on laboratory hardware costs 32 per arm on the success rate (36 for Fisher's exact test) against 8 on peak force.

**Step 6 — how sure is "7 per arm"?** The pilot's $\hat d$ is itself an estimate from ten trials per arm. Step 2's interval puts the true reduction anywhere from 1.28 to 5.04 N, and at 1.28 N step 4 asks for $2 \times 7.849 \times 1.958^2/1.28^2 = 36.7$, so 37 per arm rather than 7 (38 with the $t$ correction). Plan on the smallest reduction that would matter to someone using the arm, fixed before the experiment, not on the pilot's point estimate: at 1.5 N the answer is 26.7, so 27 per arm (28 with the $t$ correction). And a pilot taken forward *because* it looked good overstates its effect: among ten-trial binary pilots that reached significance, the lab finds an average observed gap of 0.51 where the true gap is 0.30.

### 1. Variables and units of analysis

- **Independent variable:** factor intentionally changed.
- **Dependent variable:** measured outcome.
- **Control variables:** conditions held fixed or modeled.
- **Experimental unit:** independent entity assigned to a condition—seed, scene, object, participant, robot, or site.

Repeated frames from one robot run are not thousands of independent trials.

When the experimental unit is a *person*, this page's logic still applies but the measurement procedures are their own settled subject — [[06-research-practice/psychophysics-human-measurement|8. Psychophysics & Human Measurement]] is this page's toolbox for that case.

For example, a tactile grasping study may assign surface conditions to objects while training several policy seeds. Repeated attempts on the same object help estimate performance on that object; they do not create new independent materials. Decide whether the intended claim concerns new objects, new surfaces, or training variability before choosing an aggregation. **The reading this gives you.** Look for the entity that could have been independently assigned to another condition. That entity determines which observations are clustered and what population the uncertainty can reasonably describe.

**On RS1.** The independent variable is the controller, A or B. The dependent variable is each trial's peak contact force, and success ($F \le 10$ N) is computed from it. The control variables are everything else the force could depend on: the arm (P2), the panel's stiffness ($k_w = 400$ N/m), position and mounting, the approach speed and start pose, A's threshold and B's gains, the force sensor and its filter. The experimental unit is one approach-and-contact trial. **Non-example:** the thousand samples a 1 kHz force sensor records during one contact are not a thousand trials. They share one approach, one controller state and one peak, and the peak is the one number the trial contributes.

> [!note] Verification is not validation · 검증과 타당성 확인은 다르다
> Two different questions hide under the word "testing", and a design that answers one does
> not answer the other. *Verification* asks whether the system was built the way it was
> specified: does the code match the spec, are the interlocks wired as documented, is the
> model version the one reported. *Validation* asks whether the specification is the right
> one: does the benchmark's definition of success match the behaviour a user actually wants,
> does the test environment represent the deployment environment. A robot can pass every
> verification test and still be validated against the wrong target — and the failure will
> look like a modelling problem rather than a design one.
>
> Deciding which of the two a study is producing belongs in the design, before the runs
> start. Two further consequences. The variables and units above serve verification claims
> naturally, while validation usually needs a comparison the experiment was not built for.
> And neither ends at publication: a deployed system meets changing environments and ageing
> hardware, so staying inside acceptable risk is something to keep checking, not something
> established once.

### 2. Comparisons

A strong baseline isolates the proposed contribution. Include a practical existing system, a simpler method, and when useful an **oracle** that uses unavailable information to estimate an upper bound. The oracle must be labeled; it is not a deployable competitor.

Use paired comparisons when the same scenes/tasks can be evaluated under both conditions. Randomize or counterbalance order to reduce learning, battery, wear, weather, and operator effects.

A comparison is explanatory only when the changed factors match the question. Suppose a new tactile architecture also receives additional demonstrations and a different pretrained encoder, while the baseline is trained from scratch. A higher score could come from the architecture, data, representation, or their interaction. Such an uncontrolled difference is a **confound**: something other than the proposed factor that offers an alternative explanation for the result. This is the confound identified in the self-check; putting it in the design prevents an ambiguous headline result.

For a system-level comparison, the complete packages can still be useful competitors if their resources are disclosed. For an architecture claim, add a comparison with matched data, initialization, tuning opportunity, and control interface.

**The reading this gives you.** Read the baseline description as a list of information and resources available to each method. Ask which difference the reported outcome can isolate. An oracle answers how much headroom better information might offer; it cannot establish that a deployable method actually obtains that information.

**On RS1.** A is the practical existing system, so it is the baseline. B changes one factor — the control law — only if A's threshold and B's gains received the same tuning effort on the same tuning trials; otherwise tuning is a confound. An oracle for this question would be a stop that knows the exact contact time from a separate sensor: it bounds what any threshold stop could achieve, and it must be labelled so. Pairing is available and cheap. Draw start poses and panel positions from one randomized list, run both controllers from each, and alternate the order in blocks (ABBA), so that wear, temperature and panel drift fall equally on both. The worked case's sample sizes assume independent arms; a paired analysis ([[02-foundations/probability|3. Probability §6]]) needs fewer trials when the start condition explains part of the spread, and about the same when it does not.

### 3. Variation and splits

Separate training/tuning/test data and document the unit of split. Random frames from the same trajectory leak scene, object, and temporal information. Test across relevant variation: tasks, layouts, materials, lighting/weather, hardware, operators, speed, and failure perturbations.

> [!example] Worked example · 계산 예제
> **A small reported gain needs a variability context.** In a hypothetical experiment, seed-to-seed standard deviation is 4 percentage points. With 3 independent seeds, the standard error of the mean is 4/√3 ≈ 2.3 percentage points; with 5 it is about 1.8, and with 10 about 1.3.
>
> A 3 percentage point improvement is of a similar scale to this uncertainty. Standard error is not a confidence interval, and the uncertainty of a difference also depends on the baseline and whether the design is paired. These values alone therefore establish neither significance nor its absence.
>
> **The reading this gives you.** Ask for seed count, variation, and the comparison design before interpreting a small improvement. Additional seeds measure training variability; they do not repair leakage from splitting neighboring frames across training and test, or substitute for testing genuinely new surfaces.

**On RS1.** The pilot chose A's threshold and B's gains, so its twenty trials are tuning data. They may set the design and the planning effect; they may not enter the confirmatory test, since reusing them is the test-set leak of [[02-foundations/ml-practice|9. ML Practice §1]] in experimental form. If the claim is to hold across panel positions, keep at least one position out of tuning altogether.

### 4. Trials and uncertainty

*In one sentence:* a handful of trials cannot pin down how often something works, so how many trials to run has to be decided before the experiment, and the lab checks that decision by running the whole experiment many thousands of times on a computer.

*If you need only one thing from this section:* a success rate from $n$ trials is uncertain by up to $\pm1/\sqrt{n}$ — $\pm32$ points at the pilot's $10$ per arm — and RS1's success outcome needs $32$ trials per arm for power $0.8$, which the lab below confirms by simulation ($0.82$ at $32$).

Report trial count, independent runs, failures, exclusions, aggregation, and an uncertainty measure appropriate to the design. A seed captures only software randomness; physical trials vary through calibration, wear, temperature, material, timing, and people.

Predeclare primary outcomes when many metrics and conditions make cherry-picking likely. Statistical significance and practical importance are different ([[02-foundations/ml-practice|ML Practice §5]]). Which test fits is decided by what number each trial yields and whether both methods ran on the same trials ([[02-foundations/probability|3. Probability §6]]). Two literacy-level tools for reasoning about n.

First: a success rate from $n$ trials has a 95% CI half-width of **at most** $\pm 1/\sqrt{n}$ (10 trials → ±32%p; 100 → ±10%p). It comes from the normal-approximation half-width $1.96\sqrt{p(1-p)/n}$: the product $p(1-p)$ is largest, 0.25, at $p = 0.5$, and $1.96\sqrt{0.25} = 0.98 \approx 1$. **That bound is the widest the interval ever gets, and it is reached only at $p = 0.5$** — near 0 or 1 it is far too pessimistic (at $p = 0.9$, $n = 10$, the true half-width is ±19%p), and it produces impossible bounds above 100%, so at high success rates use a Wilson or exact interval instead (both are listed in the test-choice table of [[02-foundations/probability|3. Probability §6]]).

Second: if zero failures are observed in $n$ trials, the rule of three puts the 95% **upper confidence bound** on the true failure rate at $\approx 3/n$ — an approximation that only holds for $n \gtrsim 30$; at $n = 10$ the exact bound is 26%, not 30%, and at $n = 5$ it is 45%, not 60%.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="how the uncertainty of a success rate shrinks with the number of trials">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="55" y1="24" x2="55" y2="140"/><line x1="55" y1="140" x2="415" y2="140"/><line x1="55.0" y1="140" x2="55.0" y2="146"/><line x1="100.8" y1="140" x2="100.8" y2="146"/><line x1="173.4" y1="140" x2="173.4" y2="146"/><line x1="252.9" y1="140" x2="252.9" y2="146"/><line x1="325.5" y1="140" x2="325.5" y2="146"/><line x1="405.0" y1="140" x2="405.0" y2="146"/></g>
  <path d="M55.0 90.8L58.8 92.2L62.7 93.6L66.5 94.9L70.4 96.2L74.2 97.5L78.1 98.7L81.9 99.9L85.8 101.0L89.6 102.2L93.5 103.2L97.3 104.3L101.2 105.3L105.0 106.3L108.9 107.3L112.7 108.2L116.6 109.1L120.4 110.0L124.3 110.9L128.1 111.7L132.0 112.5L135.8 113.3L139.7 114.1L143.5 114.8L147.4 115.6L151.2 116.3L155.1 116.9L158.9 117.6L162.8 118.2L166.6 118.9L170.5 119.5L174.3 120.1L178.2 120.6L182.0 121.2L185.9 121.7L189.7 122.3L193.6 122.8L197.4 123.3L201.3 123.7L205.1 124.2L209.0 124.7L212.8 125.1L216.7 125.5L220.5 125.9L224.4 126.3L228.2 126.7L232.1 127.1L235.9 127.5L239.8 127.9L243.6 128.2L247.5 128.5L251.3 128.9L255.2 129.2L259.0 129.5L262.9 129.8L266.7 130.1L270.6 130.4L274.4 130.7L278.3 130.9L282.1 131.2L286.0 131.4L289.8 131.7L293.6 131.9L297.5 132.2L301.3 132.4L305.2 132.6L309.0 132.8L312.9 133.0L316.7 133.2L320.6 133.4L324.4 133.6L328.3 133.8L332.1 134.0L336.0 134.1L339.8 134.3L343.7 134.5L347.5 134.6L351.4 134.8L355.2 134.9L359.1 135.1L362.9 135.2L366.8 135.4L370.6 135.5L374.5 135.6L378.3 135.7L382.2 135.9L386.0 136.0L389.9 136.1L393.7 136.2L397.6 136.3L401.4 136.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M55.0 74.0L58.8 77.7L62.7 81.3L66.5 84.6L70.4 87.7L74.2 90.7L78.1 93.5L81.9 96.1L85.8 98.6L89.6 100.9L93.5 103.1L97.3 105.2L101.2 107.2L105.0 109.1L108.9 110.8L112.7 112.5L116.6 114.0L120.4 115.5L124.3 116.9L128.1 118.2L132.0 119.4L135.8 120.6L139.7 121.7L143.5 122.7L147.4 123.7L151.2 124.6L155.1 125.5L158.9 126.3L162.8 127.1L166.6 127.8L170.5 128.5L174.3 129.2L178.2 129.8L182.0 130.4L185.9 130.9L189.7 131.4L193.6 131.9L197.4 132.4L201.3 132.8L205.1 133.2L209.0 133.6L212.8 133.9L216.7 134.3L220.5 134.6L224.4 134.9L228.2 135.2L232.1 135.5L235.9 135.7L239.8 136.0L243.6 136.2L247.5 136.4L251.3 136.6L255.2 136.8L259.0 137.0L262.9 137.2L266.7 137.3L270.6 137.5L274.4 137.6L278.3 137.8L282.1 137.9L286.0 138.0L289.8 138.1L293.6 138.2L297.5 138.3L301.3 138.4L305.2 138.5L309.0 138.6L312.9 138.7L316.7 138.7L320.6 138.8L324.4 138.9L328.3 138.9L332.1 139.0L336.0 139.1L339.8 139.1L343.7 139.2L347.5 139.2L351.4 139.3L355.2 139.3L359.1 139.3L362.9 139.4L366.8 139.4L370.6 139.4L374.5 139.5L378.3 139.5L382.2 139.5L386.0 139.6L389.9 139.6L393.7 139.6L397.6 139.6L401.4 139.7" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/>
  <g fill="currentColor"><circle cx="100.8" cy="105.2" r="3.5"/><circle cx="252.9" cy="129.0" r="3.5"/><circle cx="405.0" cy="136.5" r="3.5"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="55.0" y="158">5</text><text x="100.8" y="158">10</text><text x="173.4" y="158">30</text><text x="252.9" y="158">100</text><text x="325.5" y="158">300</text><text x="405.0" y="158">1000</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="10" y="34">uncertainty</text>
    <text x="106.8" y="101.2">&#177;32%p</text>
    <text x="258.9" y="125.0">&#177;10%p</text>
    <text x="365.0" y="130.5">&#177;3%p</text>
    <text x="316" y="172">number of trials n (log scale)</text>
  </g>
  <g stroke="currentColor"><line x1="55" y1="180" x2="85" y2="180" stroke-width="2"/><line x1="55" y1="196" x2="85" y2="196" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="92" y="184">maximum CI half-width, &#8776; 1/&#8730;n</text><text x="92" y="200">rule of three: 95% upper bound on failure rate after zero failures, 3/n (n &#8807; 30)</text></g>
</svg>

**On RS1.** Both tools above size an experiment around a *single* rate. RS1 compares two rates and two means, and the worked case derived those sample sizes from the four quantities defined there. Planning for precision instead of power is the same arithmetic run the other way: a 95% half-width of ±1 N on the difference of mean forces needs $n = 2(1.960 \times 1.958/1)^2 = 29.5$, so 30 per arm — more than the power calculation for the pilot's effect, because pinning a difference to ±1 N is a finer question than whether 3.16 N differs from zero. Predeclare the primary outcome (peak force) and the secondary one (success at 10 N), each with its test, because the pilot has already shown that the two can disagree.

#### Lab — power by simulation on RS1

A power formula is a claim about what would happen if the experiment were run many times, so run it many times. Each simulated experiment draws $n$ trials per arm from a stated model, applies the test the analysis will use, and records whether it rejected $H_0$. The fraction of rejections over $R = 20{,}000$ experiments estimates the power, with standard error $\sqrt{p(1-p)/R}$ — 0.003 at a power of 0.8 and never more than 0.0035 — so the tables below are good to about ±0.01. Three models:

- **success rates**: each arm's successes are Binomial($n$, $p$) with the pilot's $p_A = 0.6$ and $p_B = 0.9$, tested with step 3's pooled $z$-test and with Fisher's exact test;
- **forces**: normal, with the pilot's means and the pooled $\sigma = 1.958$ N, tested with the two-sample $t$-test on $2n - 2$ degrees of freedom (with equal arms its statistic is exactly Welch's);
- **the same forces cut at 10 N**: every simulated force experiment analysed a second time as success counts, which isolates what the cut alone costs.

```python
# RS1 power lab: the worked case's formulas against a simulated experiment.
# NumPy and the standard library only.
import numpy as np
from math import comb, exp, lgamma, pi, sqrt
from statistics import NormalDist

z, Phi = NormalDist().inv_cdf, NormalDist().cdf
A = np.array([8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3])   # RS1 pilot, N (frozen)
B = np.array([6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6])
s_p = sqrt((A.var(ddof=1) + B.var(ddof=1)) / 2)      # pooled sd, 1.958 N
d = (A.mean() - B.mean()) / s_p                        # Cohen's d, 1.614

def n_prop(pA, pB, alpha=0.05, power=0.8):             # step 3: trials per arm
    pbar = (pA + pB) / 2
    top = z(1 - alpha/2)*sqrt(2*pbar*(1 - pbar)) + z(power)*sqrt(pA*(1 - pA) + pB*(1 - pB))
    return (top / (pB - pA))**2

def power_prop(n, pA, pB, alpha=0.05):                 # step 3 solved for power
    pbar = (pA + pB) / 2
    return Phi((abs(pB - pA)*sqrt(n) - z(1 - alpha/2)*sqrt(2*pbar*(1 - pbar)))
               / sqrt(pA*(1 - pA) + pB*(1 - pB)))

def power_mean(n, d, alpha=0.05):                      # step 4 solved for power
    return Phi(abs(d)*sqrt(n/2) - z(1 - alpha/2))

def t_crit(df, q=0.975):                               # Student-t quantile without SciPy
    c = exp(lgamma((df + 1)/2) - lgamma(df/2)) / sqrt(df*pi)
    def cdf(x):                                        # 0.5 + trapezoid rule on the density
        u = np.linspace(0.0, x, 2001)
        f = c*(1 + u*u/df)**(-(df + 1)/2)
        return 0.5 + (f.sum() - (f[0] + f[-1])/2)*(u[1] - u[0])
    lo, hi = 0.0, 60.0
    for _ in range(60):                                # bisection
        mid = (lo + hi)/2
        lo, hi = (mid, hi) if cdf(mid) < q else (lo, mid)
    return (lo + hi)/2

def z_reject(xA, xB, n, alpha=0.05):                   # pooled two-proportion z-test
    pbar = (xA + xB) / (2*n)
    se = np.sqrt(2*pbar*(1 - pbar)/n)
    zs = np.divide(xB - xA, n*se, out=np.zeros(se.shape), where=se > 0)
    return np.abs(zs) > z(1 - alpha/2)

def fisher_table(n, alpha=0.05):                       # reject[a, b], Fisher's exact test
    rej = np.zeros((n + 1, n + 1), bool)
    for s in range(2*n + 1):                           # s = successes in both arms together
        a = np.arange(max(0, s - n), min(n, s) + 1)
        p = np.array([comb(n, i)*comb(n, s - i) for i in a], float) / comb(2*n, s)
        for i, p_i in zip(a, p):
            rej[i, s - i] = p[p <= p_i*(1 + 1e-9)].sum() <= alpha
    return rej

rng = np.random.default_rng(1)
R = 20000                                              # simulated experiments per cell

def sim_binary(n, pA, pB, fisher=False):               # returns the fraction of R that reject
    xA, xB = rng.binomial(n, pA, R), rng.binomial(n, pB, R)
    pz = z_reject(xA, xB, n).mean()
    return (pz, fisher_table(n)[xA, xB].mean()) if fisher else pz

def sim_force(n, muA=A.mean(), muB=B.mean(), sd=s_p, limit=10.0):
    FA, FB = rng.normal(muA, sd, (R, n)), rng.normal(muB, sd, (R, n))
    se = np.sqrt((FA.var(1, ddof=1) + FB.var(1, ddof=1))/n)   # Welch's se, equal arms
    t = (FA.mean(1) - FB.mean(1)) / se
    p_t = (np.abs(t) > t_crit(2*n - 2)).mean()
    p_cut = z_reject((FA <= limit).sum(1), (FB <= limit).sum(1), n).mean()
    return p_t, p_cut                                  # same forces, analysed two ways

print(f"trials per arm: binary {n_prop(0.6, 0.9):.1f}, force {2*(z(0.975) + z(0.8))**2/d**2:.2f}")
print(" n | binary 0.6 vs 0.9: formula  z-test  Fisher")
for n in (5, 10, 15, 20, 25, 32, 40, 50, 60):
    pz, pf = sim_binary(n, 0.6, 0.9, fisher=True)
    print(f"{n:2d} |                    {power_prop(n, 0.6, 0.9):.2f}    {pz:.2f}    {pf:.2f}")
print(" n | force: formula  t-test  same forces cut at 10 N")
for n in (3, 4, 5, 6, 7, 8, 10, 12, 15, 20):
    pt, pc = sim_force(n)
    print(f"{n:2d} |        {power_mean(n, d):.2f}    {pt:.2f}    {pc:.2f}")
print(" pB  | n per arm      | power at n = 32: formula  z-test | z-test at formula n")
for pB in (0.75, 0.80, 0.85, 0.90, 0.95):
    n_f = int(np.ceil(n_prop(0.6, pB)))
    print(f"{pB:.2f} | {n_prop(0.6, pB):6.1f} -> {n_f:3d} |"
          f"                  {power_prop(32, 0.6, pB):.2f}    {sim_binary(32, 0.6, pB):.2f} |   {sim_binary(n_f, 0.6, pB):.2f}")
```

The output, seed 1 (another seed moves entries by about 0.01). Success rate, true rates 0.6 and 0.9:

| trials per arm | formula | simulated $z$-test | simulated Fisher |
|---:|---:|---:|---:|
| 5 | 0.18 | 0.19 | 0.06 |
| 10 | 0.33 | 0.30 | 0.16 |
| 15 | 0.47 | 0.51 | 0.32 |
| 20 | 0.60 | 0.62 | 0.49 |
| 25 | 0.70 | 0.73 | 0.59 |
| **32** | **0.81** | **0.82** | **0.74** |
| 40 | 0.89 | 0.90 | 0.85 |
| 50 | 0.95 | 0.95 | 0.92 |
| 60 | 0.97 | 0.98 | 0.96 |

Peak force, true reduction 3.16 N with σ = 1.958 N:

| trials per arm | formula (σ known) | simulated $t$-test | same forces cut at 10 N |
|---:|---:|---:|---:|
| 3 | 0.51 | 0.33 | 0.18 |
| 4 | 0.63 | 0.48 | 0.40 |
| 5 | 0.72 | 0.61 | 0.48 |
| 6 | 0.80 | 0.71 | 0.57 |
| 7 | 0.86 | 0.79 | 0.57 |
| **8** | **0.90** | **0.86** | **0.70** |
| 10 | 0.95 | 0.93 | 0.71 |
| 12 | 0.98 | 0.96 | 0.84 |
| 15 | 0.99 | 0.99 | 0.91 |
| 20 | 1.00 | 1.00 | 0.97 |

The sweep over B's true success rate, A's held at 0.6 (a fresh random draw, hence 0.83 at 32 where the first table has 0.82):

| true $p_B$ | formula's trials per arm | power at 32, formula | power at 32, simulated | simulated at the formula's $n$ |
|---:|---:|---:|---:|---:|
| 0.75 | 151.9 → 152 | 0.25 | 0.25 | 0.80 |
| 0.80 | 81.2 → 82 | 0.41 | 0.42 | 0.81 |
| 0.85 | 48.9 → 49 | 0.61 | 0.63 | 0.81 |
| 0.90 | 31.5 → 32 | 0.81 | 0.83 | 0.83 |
| 0.95 | 21.1 → 22 | 0.94 | 0.96 | 0.86 |

What the three tables say.

1. **The formula is the $z$-test's.** It tracks the simulated $z$-test within 0.04 at every $n$ and crosses 0.80 between 25 and 32, as step 3 said. Fisher's exact test, run on the same simulated experiments, is conservative — 0.74 at 32, 0.85 at 40 — which is what step 3's continuity-corrected 37.9 anticipates.
2. **For the force, the formula is optimistic at small $n$.** It pretends σ is known; the $t$-test pays for estimating it — 0.61 against 0.72 at 5 per arm, 0.79 against 0.86 at 7 — and passes 0.80 only at 8. That is step 4's "8 per arm".
3. **Cutting at 10 N costs one and a half to two times the trials.** On the same simulated forces, the success counts pass 0.80 only at 12 per arm, where the forces needed 8; step 5's formulas said 11.7 against 6.03. The column also moves in steps — 0.57 at both 6 and 7 — because a test on counts can reject only at a few attainable tables, so one more trial need not buy any power.
4. **Across true rates** the formula's $n$ delivers 0.80–0.83, except near 1: at $p_B = 0.95$ its 22 per arm deliver 0.86, because the normal approximation is poor for a rate close to 1 and here errs on the safe side. Halving the gap from 0.30 to 0.15 multiplies $n$ by almost five, 31.5 to 151.9, because $n$ scales as $1/\Delta^2$ and the variances shift a little as well.

Two more runs, on the same random stream: a study the size of the pilot, and the bootstrap interval for the pilot's own force difference.

```python
# A pilot-sized study, and how uncertain the pilot's own effect is.
xA, xB = rng.binomial(10, 0.6, R), rng.binomial(10, 0.9, R)
sig = z_reject(xA, xB, 10)
gap = (xB - xA) / 10
print(f"10 per arm: power {sig.mean():.2f}; mean observed gap {gap.mean():.2f}, "
      f"among significant runs {gap[sig].mean():.2f} (true 0.30)")

boot = rng.choice(A, (20000, 10)).mean(1) - rng.choice(B, (20000, 10)).mean(1)
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"percentile bootstrap 95% CI for mean(A) - mean(B): [{lo:.2f}, {hi:.2f}] N")
```

```text
10 per arm: power 0.29; mean observed gap 0.30, among significant runs 0.51 (true 0.30)
percentile bootstrap 95% CI for mean(A) - mean(B): [1.58, 4.80] N
```

**A small study that reaches significance overstates its effect.** At ten trials per arm the average gap over all simulated pilots is the true 0.30, but over the 29% that reached significance it is 0.51. Gelman & Carlin (2014) call this a type M (magnitude) error; at 32 per arm the same average falls to 0.33. It is why step 6 plans on the smallest effect that matters rather than on a pilot that was taken forward because it worked.

**The bootstrap interval for the pilot's force difference** is $[1.58,\ 4.80]$ N against Welch's $[1.28,\ 5.04]$ N. It resamples each arm's ten forces with replacement — the procedure is defined in [[02-foundations/ml-practice|9. ML Practice]]'s worked case, part 4 — and at ten trials it inherits the plug-in spread, which is why the confidence-interval definition above lists it as a non-example. Its lower end is a planning number too, and the problem set asks what it costs.

### 5. Ablations and budgets

An ablation may remove or change architecture, objective, data, sensing, controller, or hyperparameter. Hold the rest constant enough to isolate interpretation. Compare data, compute, tuning effort, pretrained assets, sensors, and control interface—not architecture names alone.

Budget matching matters because removing a component may also remove resources. If the tactile model receives more optimization steps than its ablation, the comparison changes both information and training effort. Conversely, forcing an ablation to use an unsuitable inherited hyperparameter can make a useful simpler method look artificially weak.

For example, evaluate the full and reduced grasping policies with declared training budgets and comparable tuning opportunities. Keep demonstrations, test conditions, and the downstream controller fixed for the question about tactile information. If additional compute is required to exploit touch, report that trade-off explicitly rather than hiding it in the component label.

**The reading this gives you.** Ask what remained matched and what was retuned. An ablation supports a conclusion under that resource allocation. A separate equal-compute comparison may be needed to ask which system is preferable under a deployment budget. Neither comparison automatically answers the other's question.

**On RS1.** State whether B also carries A's force-threshold stop. If it does not, A against B changes two things at once — the control law and the presence of the stop — and the ablation that isolates the law is B with the same stop added. Budget the tuning too: the same number of tuning trials for A's threshold as for B's gains, declared in the paper.

### 6. Reproducibility vocabulary

Terminology differs across communities, so define it. A useful convention is:

- **Repeatability:** same team, setup, and procedure obtains compatible results.
- **Reproducibility:** independent team uses provided artifacts/procedure and obtains compatible results.
- **Replicability:** independent implementation or study tests the same claim.

The distinction is useful because a repeated number can come from very different evidence. Your own team rerunning a saved grasping configuration checks internal consistency. Another team using the released checkpoint checks whether the provided artifacts and instructions transfer. A separate implementation testing the same friction hypothesis probes dependence on the original code and engineering choices.

Report what was actually repeated: data, implementation, hardware, protocol, or the scientific claim. Do not rely on the label alone, especially when a venue defines these words differently.

**The reading this gives you.** Inspect the shared and changed ingredients behind a reproduction statement. A successful rerun on the original logs establishes less about new physical conditions than a study on independently prepared surfaces, even if both are described with the same convenient word.

Each word is defined by what it holds fixed, so here are its conditions in one row each, with the follow-up study it names on RS1:

| term | team | setup and artifacts | implementation | new trials | on RS1 |
|---|---|---|---|---|---|
| repeatability | same | same | same | yes, same rig | the team reruns the confirmatory protocol on its own rig a month later |
| reproducibility | independent | the released ones | the released one | yes, on a rig built to the specification | another lab runs the released controller code, gains, panel specification and analysis script on its own planar arm and 400 N/m panel |
| replicability | independent | its own | independent | yes | a different arm, panel and impedance implementation test whether impedance control lowers peak contact force |

**Non-example:** rerunning the released analysis script on the released force logs. No new trial is run, so under this convention it is none of the three — it checks the arithmetic, not the experiment — while the National Academies report in the Sources calls exactly this *reproducibility*. That clash is the reason the convention must be stated.

### 7. Artifact checklist

Record code commit, dependencies/container, model and data versions, splits, seeds, training commands, configurations, calibration, frame conventions, controller gains, firmware, hardware revision, trial protocol, raw logs, exclusions, and analysis scripts. Provide enough detail to reconstruct what physically happened.

A checklist becomes useful when its entries reconstruct a specific attempt. For example, a tactile grasp can fail because the saved sensor calibration no longer matches the mounted pad. Releasing training code does not reveal that discrepancy. The trial record must connect the calibration and hardware state to the checkpoint and command stream used that day.

Link each reported run to a configuration snapshot and a raw log, and preserve the analysis command that produced its result. Record exclusions with reasons so another reader can recover the denominator. Also document the reset procedure: a carefully prepared starting pose may be an essential experimental condition.

**The reading this gives you.** Choose one result and ask whether its complete path back to a physical attempt is recoverable. Missing entries identify a reproducibility limitation more precisely than a general statement that the code is available.

**On RS1**, the entries that decide the peak force and are the easiest to lose: the force sensor's calibration and its low-pass cut-off (a filter lowers a recorded peak), the sensor rate, A's threshold and B's gains, the panel's measured stiffness and mounting, the approach speed and start poses, and the script that turns a force trace into a peak. Record each excluded trial with its reason, so that a reader can recover both denominators.

**Where each entry is taught.** The code commit and a tag per experiment are [[02-foundations/tools/git-research-code|12.2 Git for Research Code §7]]; the pinned environment and the seeds are [[02-foundations/tools/python-research-code|12.3 Python for Research Code §1 and §7]]; the configuration snapshot and the sidecar that travels beside a log are [[02-foundations/tools/config-data-formats|12.4 Config and Data Formats §3–§4]]; the hardware revision, and a fixture that puts the part back in the same place every trial, are [[02-foundations/tools/mechanical-design-fabrication|12.9 Mechanical Design and Fabrication §1 and §7]]; the checkpoint a training run needs to survive a cluster's time limit is [[02-foundations/tools/gpu-clusters|12.7 GPU Clusters §6]]; and a paper whose figures are rebuilt from the same repository is [[02-foundations/tools/latex-figures-references|12.6 Writing Tools §10]].

### 8. Worked design

Claim: tactile sensing improves insertion recovery. Use the same robot, controller, demonstrations, objects, initial offsets, and failure perturbations. Compare vision-only and vision+tactile in randomized paired trials. Report insertion success, peak force, recovery time, damage, interventions, latency, and failure taxonomy across held-out clearances/materials.

Which of these choices to make is settled by the claim–evidence table in [[06-research-practice/research-questions-claims|Research Questions §7]], filled before any run. For a complete design of the friction question in [[06-research-practice/research-questions-claims|Research Questions §1]], start with the uncertainty: does contact-time estimation of μ recover grasp success lost when the planner assumes incorrect friction? This is a proposed experiment, not a report of an advantage already observed.

Define the intervention as enabling friction updates from the available tactile stream. Use the same planner with fixed μ as the comparator, and keep grasp candidates, demonstrations, control interface, and sensing opportunities comparable. A reference-friction condition can diagnose headroom if its privileged information is labeled. It must not be presented as an equally deployable policy.

Define units before counting trials. Objects and independently prepared surface conditions support claims about physical variation; training seeds support claims about optimization variability. Attempts within one object-condition group are repeated observations. Record their grouping rather than treating every sensor frame as independent evidence. Hold out the surface conditions needed for the transfer claim and keep them out of tuning.

Randomize or counterbalance method order within matched conditions. Record surface preparation, contact timing, failed grasps, operator stops, and resets. Predeclare whether an intervention ends the autonomous attempt. Otherwise one method can receive more rescue and appear better without making better decisions.

Choose the sample size from the required precision and the claim, using §4's uncertainty tools as planning guides. Do not select a convenient count and declare reliability afterward; a rare-failure claim needs a different exposure argument from an average-performance comparison. Use appropriate intervals and preserve clustering in the analysis.

Report success with uncertainty, recovery behavior, estimation timing, and failure categories for each condition. Include the cost of unnecessary corrections and the effect of compute latency. A finding that updates arrive after the decisive contact would locate a useful sensing boundary even without a success-rate gain. The final claim should distinguish this mechanistic evidence from the broader question of transfer across construction tasks; writing that split into separate results and discussion sentences is [[06-research-practice/scientific-writing-peer-review|Scientific Writing §5]].

**RS1, designed with this page.** *Claim:* impedance control lowers peak contact force relative to a force-threshold stop, on P2 against a 400 N/m panel. *Comparison:* A as the baseline against B, plus B with A's stop if B runs without one (§5). *Unit and order:* one approach-and-contact trial; start poses and panel positions from one randomized list, used by both controllers in alternating blocks (§2). *Outcomes, declared before the first trial:* peak force as primary, with Welch's test and its interval on the difference; success at 10 N as secondary, with Fisher's exact test (§4). *Number of trials:* 8 per arm detects the pilot's effect with power 0.8; 28 per arm detects a 1.5 N reduction, taken here as the smallest that would matter (the worked case's step 6, with the $t$ correction). *Tuning:* the pilot's twenty trials chose the gains and stay out of the test (§3). *Record:* the §7 entries, and every exclusion with its reason. *Publication:* pilot and confirmatory run are one claim, so the pilot does not go to an archival venue on its own — the trap the worked case of [[06-research-practice/venue-strategy|5. Venue Strategy]] traces through the journal rules.

### After reading

- Identify variables and the true experimental unit.
- Design a matched baseline and label oracle information.
- Detect temporal/scene leakage in robot datasets.
- Choose trials and uncertainty appropriate to physical variation.
- Specify artifacts needed to reconstruct hardware and software conditions.
- Define α, power, effect size and a confidence interval, and name the four things power depends on.
- Derive the two-proportion sample size and reproduce RS1's 32 trials per arm; derive the force's 7, and say why the $t$-test asks for 8.
- Estimate power by simulation, and check the simulation by running it under $H_0$ first.

### Self-check

1. Why are 10,000 video frames from one run not 10,000 trials?
2. When is a paired design useful?
3. What is unfair about comparing a pretrained model with extra data to a scratch baseline without disclosure?
4. Why does sharing code alone not reproduce a robot experiment?
5. The pilot's success-rate test gives $p = 0.12$. Is that evidence that B is no safer than A?
6. Planning the force experiment on the pilot's $\hat d = 1.614$ is optimistic in two separate ways. Name both.
7. A paper says its study "had 80% power." What four things must it also state for that sentence to mean anything?

> [!tip]- Answers
> 1. Frames share the same scene, state trajectory, calibration, and failure event.
> 2. When both methods can face the same task/scene/participant, reducing nuisance variation.
> 3. The comparison confounds architecture with data and pretraining.
> 4. Hardware, calibration, timing, control, materials, configuration, and procedures also determine outcomes.
> 5. No. At ten trials per arm and true rates 0.6 and 0.9 the test's power is about 0.3, so a non-significant result was the likely outcome even if B is safer, and a large p is not evidence of no difference ([[02-foundations/probability|3. Probability §6]], misreading 3). The force reading of the same trials gives $p = 0.003$.
> 6. First, $\hat d$ is an estimate from ten trials per arm: the interval for the reduction runs from 1.28 to 5.04 N, and at its low end the force needs 37 per arm instead of 7. Second, selection: a pilot taken forward because it looked good tends to be one whose estimate came out high — in the lab, significant ten-trial pilots show a gap of 0.51 where the truth is 0.30.
> 7. The true effect it assumed, the test and its α, the number of trials per arm, and the design (independent arms or pairs). Power is a function of all four, so leaving any one out leaves the number without a meaning.

### Problem set · 과제

Tier A. Using only this page, its prerequisites and RS1. The variant is a smaller improvement — B's true success rate is 0.8, not 0.9 — together with the uncertainty of the pilot's force effect.

1. **Draw.** Panel (a) of the picture above, at 32 trials per arm with true rates 0.6 and 0.8. Write $\mathrm{SE}_0$, $\mathrm{SE}_1$ and $c$ on it, shade the power and read off its value. Where does the centre of the solid curve sit relative to $c$, and what does that tell you about the power before you compute it?
2. **Derive.** (a) Trials per arm for true rates 0.6 and 0.8, at α = 0.05 two-sided and power 0.8. (b) The lab's bootstrap interval puts the pilot's force reduction as low as 1.58 N. With σ = 1.958 N, how many trials per arm would the force need if that were the true reduction? (c) Redo RS1's two sample sizes (rates 0.6 and 0.9; $\hat d = 1.614$) at α = 0.01, where $z_{0.995} = 2.576$. Does the factor between them change?
3. **Do.** Fill the `?` in the template and run it. (a) Print the formula's and the simulation's power at 32, 50, 70, 82 and 100 trials per arm for rates 0.6 and 0.8. Where does each cross 0.80? (b) Set `alpha = 0.01` and step $n$ from 100 to 140 by 5: where does the simulation cross 0.80, and what does the formula say? (c) Set both rates to 0.6. What should the simulated column show, and why does the formula column print 0.03?

```python
# RS1 variant: true success rates 0.6 and 0.8. Fill each ?; runs in a second.
import numpy as np
from math import sqrt
from statistics import NormalDist

z, Phi = NormalDist().inv_cdf, NormalDist().cdf
rng = np.random.default_rng(2)
R = 20000                                      # simulated experiments per n

def power_formula(n, pA, pB, alpha):           # the worked case, step 3
    pbar = (pA + pB) / 2
    return Phi((abs(pB - pA)*sqrt(n) - z(1 - alpha/2)*sqrt(2*pbar*(1 - pbar)))
               / sqrt(pA*(1 - pA) + pB*(1 - pB)))

def power_sim(n, pA, pB, alpha):
    xA = ?                                     # successes of A in each of R experiments
    xB = ?
    pbar = (xA + xB) / (2*n)
    se = ?                                     # standard error of pB_hat - pA_hat under H0
    zs = np.divide(xB - xA, n*se, out=np.zeros(R), where=se > 0)
    return (np.abs(zs) > ?).mean()             # two-sided test at level alpha

pA, pB, alpha = 0.6, 0.8, 0.05                 # (b): alpha = 0.01   (c): pB = 0.6
for n in (32, 50, 70, 82, 100):                # (b): range(100, 141, 5)
    print(f"{n:3d}   formula {power_formula(n, pA, pB, alpha):.2f}   simulated {power_sim(n, pA, pB, alpha):.2f}")
```

> [!note]- How to draw it · 그리는 법
> - **One axis, and it is the estimate, not the data:** the gap $\hat p_B - \hat p_A$ that the experiment will estimate from its trials.
> - **Two curves over it:** dashed, the estimate's sampling distribution if the two controllers are equal ($H_0$); solid, its sampling distribution if the assumed rates are true ($H_1$), centred at their gap.
> - **The critical value, fixed before any trial:** mark $\pm c$ with $c = z_{1-\alpha/2}\,\mathrm{SE}_0$, where $\mathrm{SE}_0$ is the standard error under $H_0$ (the worked case, step 3), not $\mathrm{SE}_1$.
> - **The false-alarm rate is the two dashed tails** beyond $\pm c$, $\alpha/2 = 0.025$ each.
> - **Power is an area under the other curve:** shade the solid curve beyond $c$ and write its value; the unshaded rest of the solid curve is $\beta$.
> - **Write the widths on:** $\mathrm{SE}_0$, $\mathrm{SE}_1$ and $c$ — in the worked case's panel, 0.108, 0.102 and 0.212, with power 0.81.
> - **Power reads one ratio:** how many null standard errors the alternative sits from zero — 2.77 in the worked case's panel.

> [!tip]- Solutions
> 1. $\bar p = 0.7$, so $\mathrm{SE}_0 = \sqrt{2 \times 0.7 \times 0.3/32} = 0.1146$ and $c = 1.960 \times 0.1146 = 0.2245$, while $\mathrm{SE}_1 = \sqrt{(0.24 + 0.16)/32} = 0.1118$. The solid curve is centred at 0.20, to the *left* of $c$, so less than half of it lies beyond $c$ and the power must be below 0.5 before any arithmetic: $\Phi\big((0.20 - 0.2245)/0.1118\big) = 0.41$, with $\beta = 0.59$. The two curves overlap almost entirely. Thirty-two trials per arm, enough for a gap of 0.30, cannot reliably see a gap of 0.20.
> 2. (a) With $\bar p = 0.7$: $(1.960\sqrt{0.42} + 0.842\sqrt{0.40})^2/0.2^2 = (1.2702 + 0.5323)^2/0.04 = 81.2$, so 82 per arm and 164 trials — 2.6 times RS1's 32 for two-thirds of the gap, because $n$ scales as $1/\Delta^2$. (b) $n = 2 \times 7.849 \times (1.958/1.58)^2 = 24.1$, so 25 per arm (26 with the $t$ correction): replacing the pilot's effect by the low end of its own interval moves the force's plan from 7 per arm to 25. (c) $(z_{0.995} + z_{0.80})^2 = (2.576 + 0.842)^2 = 11.68$. Success rate: $(2.576 \times 0.6124 + 0.842 \times 0.5745)^2/0.09 = (1.5775 + 0.4835)^2/0.09 = 47.2$, so 48 per arm. Force: $2 \times 11.68/2.605 = 8.97$, so 9 per arm. The factor is $47.2/8.97 = 5.3$ against 5.2 at α = 0.05: a stricter α raises both and leaves the cost of cutting at 10 N almost unchanged.
> 3. Blanks: `xA = rng.binomial(n, pA, R)`, `xB = rng.binomial(n, pB, R)`, `se = np.sqrt(2*pbar*(1 - pbar)/n)`, and the threshold `z(1 - alpha/2)`. (a) Formula against simulation: 0.41 and 0.43 at 32, 0.59 and 0.59 at 50, 0.74 and 0.75 at 70, 0.80 and 0.81 at 82, 0.88 and 0.88 at 100 — both cross 0.80 at about 82, as Derive (a) said. (b) Both columns read 0.80 at 120 and 0.81–0.82 at 125; the formula's $n$ is 121.2, so 122 per arm, half again as many as at α = 0.05. (c) With equal rates every rejection is a false alarm, so the simulated column is the test's real false-alarm rate. It should sit near α = 0.05, and it prints 0.04–0.06, wobbling because a count test's attainable levels change with $n$. The formula prints 0.03 because it keeps only the tail beyond $+c$: $\Phi(-1.960) = 0.025$. With an effect, the dropped tail is negligible; with none, it is exactly half the answer. A simulation that does not return about α under $H_0$ has a bug, so run this check first whenever you write one.

### Sources

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — the landmark report; note it splits the terms differently (reproducibility = same data + same computation, replicability = new data) than the ACM-style convention presented above
- [Artifact Evaluation (artifact-eval.org)](https://www.artifact-eval.org/) — what independent artifact reviewers actually check
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS Comp Biol 2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
- Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2nd ed. (Lawrence Erlbaum, 1988) — the effect size $d$ and the power tables built on it
- Fleiss, Levin & Paik, *Statistical Methods for Rates and Proportions*, 3rd ed. (Wiley, 2003) — the sample size for two independent proportions, with and without the continuity correction
- Welch, "The generalization of 'Student's' problem when several different population variances are involved," *Biometrika* 34 (1947) — the unequal-variance $t$-test and its degrees of freedom
- Efron & Tibshirani, *An Introduction to the Bootstrap* (Chapman & Hall, 1993) — the percentile interval
- Hoenig & Heisey, "The abuse of power: the pervasive fallacy of power calculations for data analysis," *The American Statistician* 55 (2001) — why "observed power" adds nothing to a p-value
- Gelman & Carlin, "Beyond power calculations: assessing type S (sign) and type M (magnitude) errors," *Perspectives on Psychological Science* 9 (2014) — why significant estimates from small studies run large

## 한국어

*[[02-foundations/ml-practice|9. ML 실무]](완성된 결과를 읽는 법)와 [[02-foundations/probability|3. 확률 §6]](검정) 위에 선다. 모든 연구 실무 페이지가 공유하는 연구 RS1 위에서 진행하며, 위키에서 검정력 분석을 가르치는 자리다.*

실험은 제안한 설명을 그럴듯한 대안들과 구분해야 한다. 로보틱스에서는 모델·데이터셋만이
아니라 장면, 하드웨어, 보정, 운용자, 리셋, 타이밍, 실패 노출까지 통제 대상이다.

> [!note] 처음이라면 · First pass
> 이 페이지의 대상인 RS1과 고정된 파일럿을 읽고, 이어서 worked case를 따라가라. 그 위에서 α, 검정력, 효과 크기, 신뢰구간을 정의하고 두 표본 크기를 손으로 구한다. 그다음 §4의 랩이 실험을 시뮬레이션해 그 숫자들을 확인한다. §1–§3과 §8은 RS1을 설계로 바꾸고, §5–§7은 첫 시행 전에 점검할 것들이다.

### 이 페이지의 대상 · Running object

모든 연구 실무 페이지의 관통 연구 **RS1**. 기계가 아니라 연구이므로 여기서 전부 규정한다. 하드웨어는 카탈로그에서 가져오고, 아래 숫자는 모두 고정이다.

- **질문.** 임피던스 제어(**B**)가 힘 문턱 정지를 단 위치 제어(**A**)보다 평면 팔과 패널의 접촉을 더 안전하게 만드는가?
- **팔과 패널.** 팔: [[02-foundations/lab-plants|0.6 Lab Plants]]의 장치 **P2**. 패널 강성: $k_w = 400\ \mathrm{N/m}$ — **P3** 가상 벽과 같은 값.
- **시행과 결과.** 시행 하나는 패널에 다가가 접촉으로 끝나는 한 번의 동작이다. 시행마다 숫자 하나, 곧 뉴턴 단위의 최대 접촉력 $F$가 나오며, $F \le 10\ \mathrm{N}$인 시행을 성공으로 센다.
- **파일럿.** 제어기당 10회. 힘 값은 교육용으로 지어낸 예시로 측정값이 아니며, 고정되어 어떤 페이지도 바꾸지 않는다.

| 제어기 | 최대 접촉력, 시행 1–10 (N) | 성공 | 평균 | 표본 표준편차 | 중앙값 |
|---|---|---:|---:|---:|---:|
| A — 위치 제어 + 힘 문턱 정지 | 8.1, 9.4, 12.6, 9.8, 13.9, 7.7, 9.9, 9.1, 14.8, 11.3 | 6/10 | 10.66 | 2.414 | 9.85 |
| B — 임피던스 제어 | 6.2, 7.9, 8.4, 5.9, 7.1, 10.6, 6.8, 7.5, 8.0, 6.6 | 9/10 | 7.50 | 1.356 | 7.30 |

RS1은 장치가 아니라 연구이므로 이 페이지의 랩은 팔의 동역학이 아니라 시행의 *결과*를 시뮬레이션하며, [[02-foundations/lab-kernel|0.7 Lab Kernel]]의 적분기는 쓰지 않는다. 접촉의 동역학을 시뮬레이션한다면 적분기가 결과의 일부가 된다. [[06-research-practice/simulators-benchmarks-datasets|7. 시뮬레이터·벤치마크·데이터셋]] worked case의 5단계에서 단단한 벽에 떨어지는 P3 핸들의 같은 낙하가 정확히는 6 N으로 RS1의 규칙상 성공이고, 명시적 오일러로는 12 N으로 실패다. 제어기는 바뀌지 않았다.

*범위: 이 페이지는 RS1에 답할 실험을 설계하는 법을 가르친다 — 무엇을 바꾸고 무엇을 고정하고 무엇을 셀지(§1–§3), 시행을 몇 번 할지를 공식과 시뮬레이션으로(worked case와 §4), 절제의 예산을 어떻게 맞출지(§5), 결과를 반복·재현·재연할 수 있도록 무엇을 기록할지(§6–§7). 완성된 결과 표를 읽는 법은 가르치지 않는다. 그것은 [[02-foundations/ml-practice|9. ML 실무와 평가]]다. 검정 자체는 [[02-foundations/probability|3. 확률 §6]], 두 제어기는 [[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]], 시행이 낳을 실패의 진단은 [[06-research-practice/failure-analysis-system-evaluation|3. 실패 분석과 시스템 평가]]에 있다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 640 262" style="max-width:100%;height:auto" role="img" aria-label="검정력 계산 뒤의 두 표본분포. RS1의 성공률(제어기당 32회)과 최대 힘(제어기당 7회)">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="30" y1="172" x2="310" y2="172"/><line x1="345" y1="172" x2="625" y2="172"/></g>
  <g fill="currentColor" stroke="none"><path d="M179.9 172L179.9 100.5L183.2 93.2L186.4 86.4L189.7 80.4L192.9 75.4L196.2 71.6L199.4 69.1L202.7 68.0L205.9 68.5L209.2 70.4L212.4 73.7L215.7 78.3L218.9 83.9L222.2 90.4L225.4 97.5L228.7 104.9L231.9 112.5L235.2 120.0L238.5 127.1L241.7 133.9L245.0 140.1L248.2 145.7L251.5 150.6L254.7 154.8L258.0 158.4L261.2 161.4L264.5 163.9L267.7 165.8L271.0 167.4L274.2 168.6L277.5 169.5L280.7 170.2L284.0 170.8L287.2 171.1L290.5 171.4L293.7 171.6L297.0 171.7L300.2 171.8L303.5 171.9L306.7 171.9L310.0 172.0L310.0 172Z" opacity="0.16"/><path d="M493.0 172L493.0 112.7L496.3 105.2L499.6 97.9L502.9 90.9L506.2 84.4L509.5 78.8L512.8 74.2L516.1 70.8L519.4 68.7L522.7 68.0L526.0 68.8L529.3 71.0L532.6 74.5L535.9 79.2L539.2 84.9L542.5 91.4L545.8 98.4L549.1 105.8L552.4 113.2L555.7 120.6L559.0 127.6L562.3 134.2L565.6 140.3L568.9 145.8L572.2 150.6L575.5 154.8L578.8 158.3L582.1 161.3L585.4 163.7L588.7 165.7L592.0 167.3L595.3 168.5L598.6 169.5L601.9 170.2L605.2 170.7L608.5 171.1L611.8 171.4L615.1 171.6L618.4 171.7L621.7 171.8L625.0 171.9L625.0 172Z" opacity="0.16"/><path d="M179.9 172L179.9 157.7L183.2 160.6L186.4 163.0L189.7 165.0L192.9 166.7L196.2 168.0L199.4 169.0L202.7 169.8L205.9 170.4L209.2 170.8L212.4 171.2L215.7 171.4L218.9 171.6L222.2 171.7L225.4 171.8L228.7 171.9L231.9 171.9L235.2 171.9L238.5 172.0L241.7 172.0L245.0 172.0L248.2 172.0L251.5 172.0L254.7 172.0L258.0 172.0L261.2 172.0L264.5 172.0L267.7 172.0L271.0 172.0L274.2 172.0L277.5 172.0L280.7 172.0L284.0 172.0L287.2 172.0L290.5 172.0L293.7 172.0L297.0 172.0L300.2 172.0L303.5 172.0L306.7 172.0L310.0 172.0L310.0 172Z" opacity="0.5"/><path d="M30.0 172L30.0 171.5L30.9 171.4L31.8 171.4L32.8 171.3L33.7 171.2L34.6 171.1L35.5 171.0L36.4 170.9L37.4 170.8L38.3 170.7L39.2 170.6L40.1 170.5L41.0 170.3L41.9 170.2L42.9 170.0L43.8 169.8L44.7 169.6L45.6 169.4L46.5 169.2L47.5 168.9L48.4 168.6L49.3 168.4L50.2 168.1L51.1 167.7L52.1 167.4L53.0 167.0L53.9 166.6L54.8 166.2L55.7 165.7L56.6 165.2L57.6 164.7L58.5 164.2L59.4 163.6L60.3 163.0L61.2 162.3L62.2 161.7L63.1 161.0L64.0 160.2L64.9 159.4L65.8 158.6L66.8 157.7L66.8 172Z" opacity="0.5"/><path d="M493.0 172L493.0 156.8L496.3 160.0L499.6 162.7L502.9 164.9L506.2 166.6L509.5 168.0L512.8 169.0L516.1 169.9L519.4 170.5L522.7 170.9L526.0 171.3L529.3 171.5L532.6 171.7L535.9 171.8L539.2 171.8L542.5 171.9L545.8 171.9L549.1 172.0L552.4 172.0L555.7 172.0L559.0 172.0L562.3 172.0L565.6 172.0L568.9 172.0L572.2 172.0L575.5 172.0L578.8 172.0L582.1 172.0L585.4 172.0L588.7 172.0L592.0 172.0L595.3 172.0L598.6 172.0L601.9 172.0L605.2 172.0L608.5 172.0L611.8 172.0L615.1 172.0L618.4 172.0L621.7 172.0L625.0 172.0L625.0 172Z" opacity="0.5"/><path d="M345.0 172L345.0 171.6L346.0 171.6L346.9 171.5L347.9 171.5L348.9 171.4L349.8 171.3L350.8 171.2L351.8 171.2L352.7 171.1L353.7 171.0L354.7 170.8L355.6 170.7L356.6 170.6L357.6 170.4L358.5 170.3L359.5 170.1L360.5 169.9L361.4 169.7L362.4 169.4L363.4 169.2L364.3 168.9L365.3 168.6L366.2 168.3L367.2 168.0L368.2 167.6L369.1 167.2L370.1 166.8L371.1 166.3L372.0 165.8L373.0 165.3L374.0 164.7L374.9 164.1L375.9 163.5L376.9 162.8L377.8 162.1L378.8 161.3L379.8 160.5L380.7 159.6L381.7 158.7L382.7 157.8L383.6 156.8L383.6 172Z" opacity="0.5"/></g>
  <path d="M30.0 171.5 L33.1 171.3 L36.2 171.0 L39.3 170.6 L42.4 170.1 L45.6 169.4 L48.7 168.6 L51.8 167.5 L54.9 166.1 L58.0 164.5 L61.1 162.4 L64.2 160.0 L67.3 157.1 L70.4 153.8 L73.6 149.9 L76.7 145.6 L79.8 140.7 L82.9 135.4 L86.0 129.7 L89.1 123.7 L92.2 117.4 L95.3 111.0 L98.4 104.7 L101.6 98.6 L104.7 92.8 L107.8 87.6 L110.9 83.1 L114.0 79.4 L117.1 76.7 L120.2 75.0 L123.3 74.4 L126.4 75.0 L129.6 76.7 L132.7 79.4 L135.8 83.1 L138.9 87.6 L142.0 92.8 L145.1 98.6 L148.2 104.7 L151.3 111.0 L154.4 117.4 L157.6 123.7 L160.7 129.7 L163.8 135.4 L166.9 140.7 L170.0 145.6 L173.1 149.9 L176.2 153.8 L179.3 157.1 L182.4 160.0 L185.6 162.4 L188.7 164.5 L191.8 166.1 L194.9 167.5 L198.0 168.6 L201.1 169.4 L204.2 170.1 L207.3 170.6 L210.4 171.0 L213.6 171.3 L216.7 171.5 L219.8 171.6 L222.9 171.7 L226.0 171.8 L229.1 171.9 L232.2 171.9 L235.3 171.9 L238.4 172.0 L241.6 172.0 L244.7 172.0 L247.8 172.0 L250.9 172.0 L254.0 172.0 L257.1 172.0 L260.2 172.0 L263.3 172.0 L266.4 172.0 L269.6 172.0 L272.7 172.0 L275.8 172.0 L278.9 172.0 L282.0 172.0 L285.1 172.0 L288.2 172.0 L291.3 172.0 L294.4 172.0 L297.6 172.0 L300.7 172.0 L303.8 172.0 L306.9 172.0 L310.0 172.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4" opacity="0.75"/>
  <path d="M30.0 172.0 L33.1 172.0 L36.2 172.0 L39.3 172.0 L42.4 172.0 L45.6 172.0 L48.7 172.0 L51.8 172.0 L54.9 172.0 L58.0 172.0 L61.1 172.0 L64.2 172.0 L67.3 172.0 L70.4 172.0 L73.6 172.0 L76.7 172.0 L79.8 172.0 L82.9 172.0 L86.0 172.0 L89.1 172.0 L92.2 172.0 L95.3 172.0 L98.4 171.9 L101.6 171.9 L104.7 171.9 L107.8 171.8 L110.9 171.7 L114.0 171.5 L117.1 171.3 L120.2 171.1 L123.3 170.7 L126.4 170.2 L129.6 169.5 L132.7 168.5 L135.8 167.4 L138.9 165.9 L142.0 164.0 L145.1 161.7 L148.2 158.9 L151.3 155.5 L154.4 151.6 L157.6 147.1 L160.7 141.9 L163.8 136.2 L166.9 130.0 L170.0 123.2 L173.1 116.2 L176.2 109.0 L179.3 101.8 L182.4 94.8 L185.6 88.2 L188.7 82.2 L191.8 77.1 L194.9 72.9 L198.0 70.0 L201.1 68.3 L204.2 68.1 L207.3 69.1 L210.4 71.5 L213.6 75.2 L216.7 79.9 L219.8 85.5 L222.9 91.9 L226.0 98.7 L229.1 105.9 L232.2 113.1 L235.3 120.3 L238.4 127.1 L241.6 133.6 L244.7 139.6 L247.8 145.0 L250.9 149.7 L254.0 153.9 L257.1 157.5 L260.2 160.6 L263.3 163.1 L266.4 165.1 L269.6 166.8 L272.7 168.1 L275.8 169.1 L278.9 169.9 L282.0 170.5 L285.1 170.9 L288.2 171.2 L291.3 171.5 L294.4 171.6 L297.6 171.8 L300.7 171.8 L303.8 171.9 L306.9 171.9 L310.0 172.0" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M345.0 171.6 L348.1 171.4 L351.2 171.2 L354.3 170.9 L357.4 170.4 L360.6 169.9 L363.7 169.1 L366.8 168.1 L369.9 166.9 L373.0 165.3 L376.1 163.3 L379.2 161.0 L382.3 158.1 L385.4 154.7 L388.6 150.8 L391.7 146.3 L394.8 141.2 L397.9 135.6 L401.0 129.5 L404.1 123.0 L407.2 116.1 L410.3 109.1 L413.4 102.1 L416.6 95.3 L419.7 88.8 L422.8 83.0 L425.9 77.8 L429.0 73.7 L432.1 70.6 L435.2 68.6 L438.3 68.0 L441.4 68.6 L444.6 70.6 L447.7 73.7 L450.8 77.8 L453.9 83.0 L457.0 88.8 L460.1 95.3 L463.2 102.1 L466.3 109.1 L469.4 116.1 L472.6 123.0 L475.7 129.5 L478.8 135.6 L481.9 141.2 L485.0 146.3 L488.1 150.8 L491.2 154.7 L494.3 158.1 L497.4 161.0 L500.6 163.3 L503.7 165.3 L506.8 166.9 L509.9 168.1 L513.0 169.1 L516.1 169.9 L519.2 170.4 L522.3 170.9 L525.4 171.2 L528.6 171.4 L531.7 171.6 L534.8 171.7 L537.9 171.8 L541.0 171.9 L544.1 171.9 L547.2 171.9 L550.3 172.0 L553.4 172.0 L556.6 172.0 L559.7 172.0 L562.8 172.0 L565.9 172.0 L569.0 172.0 L572.1 172.0 L575.2 172.0 L578.3 172.0 L581.4 172.0 L584.6 172.0 L587.7 172.0 L590.8 172.0 L593.9 172.0 L597.0 172.0 L600.1 172.0 L603.2 172.0 L606.3 172.0 L609.4 172.0 L612.6 172.0 L615.7 172.0 L618.8 172.0 L621.9 172.0 L625.0 172.0" fill="none" stroke="currentColor" stroke-width="1.6" stroke-dasharray="5 4" opacity="0.75"/>
  <path d="M345.0 172.0 L348.1 172.0 L351.2 172.0 L354.3 172.0 L357.4 172.0 L360.6 172.0 L363.7 172.0 L366.8 172.0 L369.9 172.0 L373.0 172.0 L376.1 172.0 L379.2 172.0 L382.3 172.0 L385.4 172.0 L388.6 172.0 L391.7 172.0 L394.8 172.0 L397.9 172.0 L401.0 172.0 L404.1 172.0 L407.2 172.0 L410.3 172.0 L413.4 172.0 L416.6 171.9 L419.7 171.9 L422.8 171.8 L425.9 171.7 L429.0 171.6 L432.1 171.5 L435.2 171.2 L438.3 170.9 L441.4 170.5 L444.6 169.9 L447.7 169.2 L450.8 168.2 L453.9 167.0 L457.0 165.4 L460.1 163.5 L463.2 161.2 L466.3 158.4 L469.4 155.0 L472.6 151.2 L475.7 146.7 L478.8 141.7 L481.9 136.1 L485.0 130.0 L488.1 123.5 L491.2 116.7 L494.3 109.7 L497.4 102.7 L500.6 95.9 L503.7 89.4 L506.8 83.4 L509.9 78.2 L513.0 74.0 L516.1 70.8 L519.2 68.8 L522.3 68.0 L525.4 68.5 L528.6 70.3 L531.7 73.3 L534.8 77.4 L537.9 82.5 L541.0 88.3 L544.1 94.7 L547.2 101.5 L550.3 108.5 L553.4 115.5 L556.6 122.4 L559.7 128.9 L562.8 135.1 L565.9 140.8 L569.0 145.9 L572.1 150.4 L575.2 154.4 L578.3 157.8 L581.4 160.7 L584.6 163.2 L587.7 165.1 L590.8 166.7 L593.9 168.0 L597.0 169.0 L600.1 169.8 L603.2 170.4 L606.3 170.8 L609.4 171.2 L612.6 171.4 L615.7 171.6 L618.8 171.7 L621.9 171.8 L625.0 171.9" fill="none" stroke="currentColor" stroke-width="2"/>
  <g stroke="currentColor" stroke-width="1" stroke-dasharray="2 3" opacity="0.8"><line x1="179.9" y1="52" x2="179.9" y2="172"/><line x1="66.8" y1="112" x2="66.8" y2="172"/><line x1="493.0" y1="52" x2="493.0" y2="172"/><line x1="383.6" y1="112" x2="383.6" y2="172"/></g>
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="70.0" y1="172" x2="70.0" y2="177"/><line x1="123.3" y1="172" x2="123.3" y2="177"/><line x1="176.7" y1="172" x2="176.7" y2="177"/><line x1="230.0" y1="172" x2="230.0" y2="177"/><line x1="283.3" y1="172" x2="283.3" y2="177"/><line x1="385.0" y1="172" x2="385.0" y2="177"/><line x1="438.3" y1="172" x2="438.3" y2="177"/><line x1="491.7" y1="172" x2="491.7" y2="177"/><line x1="545.0" y1="172" x2="545.0" y2="177"/><line x1="598.3" y1="172" x2="598.3" y2="177"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle"><text x="70.0" y="188">-0.2</text><text x="123.3" y="188">0</text><text x="176.7" y="188">0.2</text><text x="230.0" y="188">0.4</text><text x="283.3" y="188">0.6</text><text x="385.0" y="188">-2</text><text x="438.3" y="188">0</text><text x="491.7" y="188">2</text><text x="545.0" y="188">4</text><text x="598.3" y="188">6</text></g>
  <g font-size="10.5" fill="currentColor" text-anchor="middle">
    <text x="170" y="20" font-weight="bold">(a) 성공률, 제어기당 32회</text><text x="485" y="20" font-weight="bold">(b) 최대 힘, 제어기당 7회</text>
    <text x="170" y="202">추정한 성공률 차이</text><text x="485" y="202">추정한 평균 최대 힘 차이 (N)</text>
    <text x="118.0" y="68.4">H<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="208.7" y="62.0">H<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="433.0" y="62.0">H<tspan dy="3.5">0</tspan><tspan dy="-3.5">&#8203;</tspan></text><text x="527.9" y="62.0">H<tspan dy="3.5">1</tspan><tspan dy="-3.5">&#8203;</tspan></text>
    <text x="179.9" y="46">c = 0.212</text><text x="493.0" y="46">c = 2.05 N</text>
    <text x="211.3" y="140">검정력 0.81</text><text x="530.3" y="140">검정력 0.86</text>
    <text x="160.7" y="166" font-size="9.5">β 0.19</text><text x="474.3" y="166" font-size="9.5">β 0.14</text>
  </g>
  <g font-size="10" fill="currentColor">
    <text x="30" y="232">점선: A와 B가 같다(H<tspan dy="3.5">0</tspan><tspan dy="-3.5">) · 실선: 파일럿의 효과가 실제다(H</tspan><tspan dy="3.5">1</tspan><tspan dy="-3.5">)</tspan></text>
    <text x="30" y="250">옅은 채움: 검정력, c 너머의 H<tspan dy="3.5">1</tspan><tspan dy="-3.5"> 넓이 · 짙은 채움: H</tspan><tspan dy="3.5">0</tspan><tspan dy="-3.5">의 두 꼬리 α/2 = 0.025</tspan></text>
  </g>
</svg>

RS1의 표본 크기 뒤에 있는 두 표본분포로, 추정한 차이가 A와 B가 같을 때($H_0$, 점선)와 파일럿의 효과가 실제일 때($H_1$, 실선) 따르는 분포를 (a) 제어기당 32회의 성공률과 (b) 7회의 최대 힘에 대해 그렸다. 임계값 $c = 0.212$와 $c = 2.05$ N은 점선의 두 꼬리에 각각 $\alpha/2 = 0.025$를 남기고, 검정력은 그 너머의 실선 넓이로 0.81과 0.86이며 $\beta$는 0.19와 0.14다. 두 칸 모두 대립가설이 0에서 귀무 표준오차의 약 세 배, 2.77과 3.02만큼 떨어져 있고 검정력이 읽는 것은 그 비율뿐이다 — 성공률은 거기까지 가는 데 제어기당 32회가 들고, 힘은 7회면 된다.

### 대상으로 한 번 끝까지 · Worked case

계산 하나로 본 이 페이지 전체다. 파일럿이 무엇을 말하는지, 그리고 확증 실험이 RS1의 두 결과 각각에 시행을 몇 번 필요로 하는지를 손으로 구한다. §4의 랩이 여기 나온 모든 숫자를 시뮬레이션으로 확인한다.

**1단계 — 파일럿 요약.** 표에서 A는 10회 중 6회, B는 10회 중 9회 성공한다. B의 평균 최대 힘은 $10.66 - 7.50 = 3.16$ N 낮다. 표본 표준편차(분모 $n - 1$, [[02-foundations/ml-practice|9. ML 실무 §4]])는 2.414 N과 1.356 N이다. A의 평균이 중앙값보다 큰 것(10.66 대 9.85)은 네 번의 실패가 멀리까지(최대 14.8 N) 뻗은 반면 성공은 선 바로 아래에 몰려 있기 때문이다. 여섯 번의 성공 중 넷이 9.1–9.9 N 사이에 있다. 5단계에서 이 몰림이 필요하다.

모든 표본 크기는 네 가지 양으로 정해진다. 각각을 여기서 한 번 정의하고 페이지 끝까지 쓴다.

> [!info] 정의 — 유의수준 α
> **어떤 종류의 것인가:** 측정하는 것이 아니라 *고르는* 확률이다. 검정에 허용하는 오경보율이며, [[02-foundations/probability|3. 확률 §6]]은 이를 제1종 오류율이라 부른다. 세 조건: (1) 데이터가 생기기 전에 고정한다; (2) $H_0$가 참일 때 결정 규칙이 갖는 성질로, 두 제어기가 같다고 보고 계산한다; (3) 양측 검정에서는 두 꼬리에 똑같이 나누므로 임계값이 $z_{1-\alpha/2}$다.
> $$\alpha = P\big(\text{reject } H_0 \mid H_0 \text{ true}\big) = P\big(|Z| > z_{1-\alpha/2}\big)$$
> 여기서 $Z$는 $H_0$ 아래에서 표준화한 검정 통계량이고, $z_q$는 $P(Z \le z_q) = q$인 표준정규 분위수다.
> **예.** RS1은 양측 α = 0.05를 쓰므로 $z_{0.975} = 1.960$이다.
> **반례.** 성공률에 대한 파일럿의 $p = 0.12$. p-값은 데이터로 계산한 뒤 α와 비교하는 값이고, α는 데이터가 생기기 전에 고른 값이다. 그리고 둘 다 $H_0$가 참일 확률이 아니다.
> **왜 중요한가.** α가 임계값을 정하고, 임계값은 아래 모든 표본 크기 공식의 두 항 중 첫째다.

> [!info] 정의 — 통계적 검정력, 1 − β
> **어떤 종류의 것인가:** 확률이며, 데이터셋이 아니라 설계의 성질이다. 명시한 효과가 실제일 때 계획한 실험이 $H_0$를 기각할 확률이다. [[02-foundations/probability|3. 확률 §6]]의 검출 확률 $P_D$를 주장에 적용한 것이다. 값을 가지려면 네 가지를 먼저 정해야 한다: (1) $H_1$ 아래에서 가정한 참 효과; (2) 검정과 그 α; (3) 제어기당 시행 수; (4) 설계, 곧 독립된 두 군인지 짝인지. 하나만 바꿔도 검정력이 바뀌므로, 효과를 밝히지 않은 "검정력 80%의 연구"는 주장이 아니다.
> $$1 - \beta = P\big(\text{reject } H_0 \mid H_1:\ \text{true difference} = \Delta\big)$$
> 여기서 $\beta$는 그 효과에서의 놓침(제2종 오류)율이고 $\Delta$는 가정한 참 차이다.
> **예.** RS1의 성공률, 제어기당 32회, α = 0.05, 참 성공률 0.6과 0.9: 검정력 0.81(3단계).
> **반례.** 유의하지 않은 결과가 나온 뒤 관측된 효과를 다시 넣어 계산한 "관측 검정력". p-값의 고정된 함수이므로 p-값이 말하지 않은 것을 아무것도 말하지 않는다(Hoenig & Heisey 2001). 검정력은 $H_1$이 참일 확률도 아니다.
> **왜 중요한가.** 검정력이 낮은 연구는 효과가 실제여도 대개 기각하지 못하고 — 파일럿이 그 예다 — 기각하더라도 추정값이 부풀려진다. 얼마나 부풀려지는지는 §4의 랩이 잰다.

> [!info] 정의 — 효과 크기
> **어떤 종류의 것인가:** 모집단의 양, 곧 표본은 추정할 뿐인 모수이며, 차이가 얼마나 큰지를 밝힌 척도로 말한다. 세 조건: (1) 모집단에 속하므로 파일럿의 값은 추정값이다; (2) $n$이 늘어도 커지지 않는다 — 시행을 늘리면 추정이 정밀해질 뿐 값은 그대로다; (3) 척도를 밝힌다 — 원척도(뉴턴, 퍼센트포인트)이거나 퍼짐으로 표준화한 것이다. 힘의 표준화 효과 크기가 Cohen의 d다.
> $$d = \frac{\mu_A - \mu_B}{\sigma}, \qquad \hat d = \frac{\bar F_A - \bar F_B}{s_p}, \qquad s_p = \sqrt{\frac{(n_A - 1)s_A^2 + (n_B - 1)s_B^2}{n_A + n_B - 2}}$$
> 여기서 $\mu_A$, $\mu_B$는 참 평균 최대 힘, $\sigma$는 둘의 공통 표준편차, $s_p$는 합동 표본 표준편차이므로, $d$는 퍼짐을 단위로 잰 차이다. 성공률의 효과 크기는 차이 $p_B - p_A$ 자체다.
> **예.** 파일럿: $s_p = \sqrt{(9 \times 2.414^2 + 9 \times 1.356^2)/18} = 1.958$ N, $\hat d = 3.16/1.958 = 1.614$. 성공률은 $0.9 - 0.6 = 0.30$.
> **반례.** 파일럿의 $t = 3.61$이나 $p = 0.0028$. 두 군의 크기가 같으면 정확히 $t = \hat d\sqrt{n/2}$이다 — $1.614 \times \sqrt 5 = 3.61$ — 그래서 같은 효과라도 시행을 더할 때마다 $t$는 커지고 $p$는 작아진다. 둘은 효과와 표본 크기를 함께 잰다.
> **왜 중요한가.** 모든 표본 크기 공식이 요구하는 입력이며, 독자가 실질적 중요성을 따질 때 보는 숫자다([[02-foundations/ml-practice|9. ML 실무 §5]]).

> [!info] 정의 — 평균 차이의 신뢰구간
> **어떤 종류의 것인가:** 데이터셋을 구간으로 보내는 절차이며, 일반적인 정의는 [[02-foundations/probability|3. 확률 §6]]에 있다. 여기서는 RS1의 분석이 출력할 그 구간이다. 세 조건: (1) 끝점은 데이터로 계산하므로 확률적이고, 참 차이는 고정되어 있다; (2) 실험을 반복하면 구간이 참 차이를 확률 $1 - \alpha$로 덮는다; (3) 그 포함 확률은 절차의 가정 아래에서만 성립한다 — 여기서는 독립 시행과 대략 정규인 평균.
> $$\big(\bar F_A - \bar F_B\big) \pm t_{0.975,\,\nu}\sqrt{\frac{s_A^2}{n_A} + \frac{s_B^2}{n_B}}$$
> 제곱근은 차이에 대한 Welch 표준오차이고 $\nu$는 Welch–Satterthwaite 자유도다. 그래서 두 군이 같은 퍼짐을 가진다고 가정하지 않는다.
> **예.** 파일럿: $3.16 \pm 2.142 \times 0.8756 = [1.28,\ 5.04]$ N, $\nu = 14.16$.
> **반례.** "B는 95% 확률로 최대 힘을 1.28–5.04 N 낮춘다." 한 번 계산된 구간은 참값을 덮거나 덮지 않거나 둘 중 하나이고, 95%는 절차의 성질이다. 그리고 같은 시행의 백분위 부트스트랩 구간, §4 랩의 $[1.58,\ 4.80]$ N이 더 좁은 것은 더 많이 알아서가 아니라 두 퍼짐을 10회 시행에서 추정했다는 사실을 무시하기 때문이다. 이 크기의 정규 파일럿 4,000개를 시뮬레이션하면 부트스트랩 구간은 참 차이를 92%, Welch 구간은 95% 덮었다. [[02-foundations/ml-practice|9. ML 실무]] worked case 4번이 말한, 데이터가 얇을 때의 부트스트랩 실패다.
> **왜 중요한가.** 반폭은 실험이 사는 정밀도이고, 반폭을 목표로 계획하는 것이 시행 수를 고르는 또 하나의 방법이다(§4).

**2단계 — 파일럿 자신의 두 검정.** *힘.* Welch 표준오차는 $\sqrt{2.414^2/10 + 1.356^2/10} = 0.8756$ N이므로 자유도 $\nu = 14.16$에서 $t = 3.16/0.8756 = 3.61$, 양측 $p = 0.0028$, 95% 구간 $[1.28,\ 5.04]$ N이다. B가 최대 힘을 낮춘다는 강한 증거다. *성공률.* 합동 두 비율 $z$-검정은 $\bar p = 0.75$, $\mathrm{SE}_0 = \sqrt{0.75 \times 0.25 \times 2/10} = 0.194$를 써서 $z = 0.30/0.194 = 1.55$, $p = 0.12$를 준다. [[02-foundations/probability|3. 확률 §6]]의 표가 작은 2×2 표에 고르는 Fisher 정확 검정은 $p = 0.30$이다. 같은 스무 번의 시행이 한 방식으로는 강한 증거로, 다른 방식으로는 증거 없음으로 읽힌다. 모순은 없다. 10회 파일럿의 이분 판독은 실제 차이를 볼 기회가 거의 없었다. 참 성공률이 0.6과 0.9라면 제어기당 10회의 검정력은 3단계 공식으로 0.33이고 — 랩은 $z$-검정 0.30, Fisher 0.16을 얻는다 — 그러니 B가 정말 더 안전해도 "유의하지 않음"이 가장 그럴듯한 결과였다. [[02-foundations/probability|3. 확률 §6]]의 오독 3을 숫자로 본 것이다. 성공 비교가 무엇과 양립하는지는 p-값이 아니라 구간이 말한다. 차이에 대한 Newcombe 95% 구간 $-0.08$–$+0.60$이고, [[06-research-practice/scientific-writing-peer-review|4. 과학 글쓰기와 peer review]]의 worked case가 정의하고 계산한다.

**3단계 — 성공률에 필요한 제어기당 시행 수.** 실험이 제어기당 $n$회에서 추정할 차이를 $\hat D = \hat p_B - \hat p_A$로, $q = 1 - p$로 쓴다. CLT([[02-foundations/probability|3. 확률 §3]])에 의해 각 $\hat p$는 분산 $pq/n$인 정규분포에 가깝고, 독립된 두 군의 분산은 더해진다. 따라서

- 두 제어기가 같으면 두 성공률은 평균 $\bar p = (p_A + p_B)/2$이고 $\hat D \sim \mathcal N(0,\ 2\bar p\bar q/n)$;
- 다르면 $\hat D \sim \mathcal N(\Delta,\ (p_Aq_A + p_Bq_B)/n)$, 단 $\Delta = p_B - p_A$.

검정은 $|\hat D| > c$일 때 기각하며, $c = z_{1-\alpha/2}\sqrt{2\bar p\bar q/n}$로 두면 오경보율이 α가 된다. 검정력은 $H_1$ 아래에서 $c$ 너머에 떨어질 확률이다. 반대쪽 꼬리($-c$ 아래)는 RS1의 숫자에서 약 $2 \times 10^{-7}$이므로 버린다.

$$1 - \beta = \Phi\left(\frac{\Delta\sqrt n - z_{1-\alpha/2}\sqrt{2\bar p\bar q}}{\sqrt{p_Aq_A + p_Bq_B}}\right)$$

$H_1$ 아래에서 $P(\hat D > c)$를 표준화하면 $\Delta$를 빼고 $\sqrt{(p_Aq_A + p_Bq_B)/n}$로 나누기 때문이다. 이것을 목표 검정력과 같게 놓고 $\Phi^{-1}(1 - \beta) = z_{1-\beta}$를 써서 $n$에 대해 풀면

$$n = \frac{\Big(z_{1-\alpha/2}\sqrt{2\bar p\bar q} + z_{1-\beta}\sqrt{p_Aq_A + p_Bq_B}\Big)^2}{(p_B - p_A)^2}$$

$\Phi$ 안의 분자가 분모의 $z_{1-\beta}$배여야 하기 때문이다. 독립된 두 비율의 정규근사 표본 크기 공식이다(Fleiss, Levin & Paik 2003). RS1에서 $p_A = 0.6$, $p_B = 0.9$, 양측 α = 0.05, 검정력 0.8이면

- $\bar p = 0.75$, $z_{0.975} = 1.960$, $z_{0.80} = 0.842$;
- $\sqrt{2 \times 0.75 \times 0.25} = 0.6124$, $\sqrt{0.6 \times 0.4 + 0.9 \times 0.1} = \sqrt{0.33} = 0.5745$;
- 분자는 $(1.960 \times 0.6124 + 0.842 \times 0.5745)^2 = (1.2002 + 0.4835)^2 = 1.6837^2 = 2.8348$;
- $n = 2.8348/0.30^2 = 31.5$. 따라서 **제어기당 32회, 모두 64회**. $n = 32$에서 검정력 공식은 0.81을 준다.

공식은 검정에 속한다. 두 항 모두에 $H_1$ 분산을 넣으면 28.8이 나오고, 같은 참고문헌의 연속성 보정 — 정확 검정을 따라가도록 만든 것 — 을 더하면 37.9가 나온다. 실제로 돌릴 검정으로 계획하라. 제어기당 32회에서 Fisher 정확 검정의 검정력은 0.81이 아니라 0.74다(§4).

**4단계 — 힘에 필요한 제어기당 시행 수.** 공통 표준편차 $\sigma$를 가진 두 평균의 차이라면, 같은 두 곡선 논증에서 두 가설 모두 $\mathrm{SE} = \sigma\sqrt{2/n}$이므로 두 항이 합쳐진다.

$$n = \frac{2\big(z_{1-\alpha/2} + z_{1-\beta}\big)^2\sigma^2}{\Delta^2} = \frac{2\big(z_{1-\alpha/2} + z_{1-\beta}\big)^2}{d^2}$$

$d = \Delta/\sigma$가 Cohen의 d이기 때문이다. 파일럿의 $\hat d = 1.614$를 넣으면 $n = 2 \times (1.960 + 0.842)^2/1.614^2 = 2 \times 7.849/2.605 = 6.03$, 올림하면 **제어기당 7회**. 정규근사는 $\sigma$를 안다고 가정한다. 실제 분석은 $\sigma$를 추정하고, 자유도 $2n - 2$의 $t$ 임계값은 작은 $n$에서 1.960보다 크다 — $t_{0.975,\,12} = 2.179$ — 그래서 $t$-검정의 실제 검정력은 더 낮다. 랩은 제어기당 7회에서 0.79, 8회에서 0.86을 잰다. $t$ 기반의 답은 **제어기당 8회**.

**5단계 — 힘은 왜 시행의 5분의 1이면 되는가.** 31.5 대 6.03은 5.2배이고, 올림과 $t$ 보정을 거친 32 대 8은 4배다. 두 가지가 곱해진 결과이며, 그중 결과 변수 탓은 하나뿐이다.

- *10 N에서 자르면 정보를 버린다.* 9.9 N의 성공과 6.2 N의 성공이 같게 세어지고, 10.6 N의 실패와 14.8 N의 실패가 같게 세어진다. 힘이 정말 파일럿의 평균과 합동 $\sigma = 1.958$ N을 가진 정규분포라고 하자. 그러면 성공률은 A가 $\Phi\big((10 - 10.66)/1.958\big) = 0.37$, B가 $\Phi\big((10 - 7.50)/1.958\big) = 0.90$이고, 그 성공률에서 3단계 공식은 제어기당 11.7회를 요구한다. **같은 실험에서** 힘이 필요로 하는 6.03회의 약 두 배다. 랩은 시뮬레이션한 실험마다 두 방식으로 분석해 이를 직접 잰다.
- *파일럿의 두 요약이 효과의 크기에 대해 서로 다르게 말한다.* 관측된 성공률 0.6과 0.9는 0.30 떨어져 있지만, 힘에 맞춘 정규 모형은 0.53을 함의한다. 선 바로 아래에 몰린 A의 성공들이 그 이유다. 나머지 배수 $31.5/11.7 = 2.7$이 그 불일치이고, 제어기당 10회로는 가릴 수 없다.

그러니 힘을 기록하고 힘으로 분석하되, 성공률을 옆에 함께 보고하라. RS1의 독자가 신경 쓰는 것은 10 N 선이기 때문이다. 둘 중 무엇이 주요 결과인지는 첫 시행 전에 선언한다(§4). [[06-research-practice/real-world-impact|6. 실세계 임팩트]]의 worked case는 같은 두 결과의 값을 증거의 단마다 매긴다. 파일럿은 시뮬레이션 단에 있고, 그것을 실험실 하드웨어에서 다시 하는 값은 성공률로 제어기당 32회(Fisher 정확 검정으로 36회), 최대 힘으로 8회다.

**6단계 — "제어기당 7회"는 얼마나 확실한가.** 파일럿의 $\hat d$ 자체가 제어기당 10회에서 나온 추정값이다. 2단계의 구간은 참 감소량을 1.28–5.04 N 어디에나 둘 수 있고, 1.28 N이라면 4단계는 $2 \times 7.849 \times 1.958^2/1.28^2 = 36.7$, 곧 7회가 아니라 37회를 요구한다($t$ 보정으로 38회). 파일럿의 점추정값이 아니라, 팔을 쓰는 사람에게 의미가 있을 가장 작은 감소량을 실험 전에 정해 그것으로 계획하라. 1.5 N이라면 답은 26.7, 곧 제어기당 27회다($t$ 보정으로 28회). 그리고 좋아 보였기 *때문에* 다음 단계로 간 파일럿은 효과를 과장한다. 유의에 도달한 10회 이분 파일럿들만 모으면, 참 차이가 0.30일 때 랩이 찾는 평균 관측 차이는 0.51이다.

### 1. 변수와 분석 단위

- **독립 변수:** 의도적으로 바꾸는 요인.
- **종속 변수:** 측정되는 결과.
- **통제 변수:** 고정하거나 모델링하는 조건.
- **실험 단위:** 조건에 배정되는 독립적 개체 — 시드, 장면, 물체, 참가자, 로봇, 현장.

한 로봇 실행의 반복 프레임들은 수천 개의 독립 시행이 아니다.

실험 단위가 *사람*일 때도 이 페이지의 논리는 그대로 적용되지만, 측정 절차는 그 자체로 정착된 별도 주제다 — [[06-research-practice/psychophysics-human-measurement|8. 심리물리와 인간 측정]]이 그 경우를 위한 이 페이지의 공구함이다.

예를 들어 촉각 파지 연구는 물체별 표면 조건을 배정하고 여러 정책 시드를 학습할 수 있다. 같은 물체의 반복 시도는 그 물체의 성능 추정을 돕지만 새로운 독립 재료를 만들지는 않는다. 새 물체, 새 표면, 학습 변동 중 무엇을 주장할지 먼저 정하고 집계한다. **여기서 얻는 독법.** 독립적으로 다른 조건에 배정될 수 있었던 대상을 찾는다. 그 대상에 따라 관측의 군집과 불확실성이 설명할 모집단이 정해진다.

**RS1에서는.** 독립 변수는 제어기, A 또는 B다. 종속 변수는 각 시행의 최대 접촉력이고, 성공($F \le 10$ N)은 거기서 계산한다. 통제 변수는 힘이 의존할 수 있는 나머지 전부다: 팔(P2), 패널의 강성($k_w = 400$ N/m)·위치·고정, 접근 속도와 시작 자세, A의 문턱과 B의 이득, 힘 센서와 그 필터. 실험 단위는 접근과 접촉 한 번으로 이루어진 시행 하나다. **반례:** 1 kHz 힘 센서가 접촉 한 번 동안 기록한 표본 천 개는 시행 천 개가 아니다. 한 번의 접근, 하나의 제어기 상태, 하나의 최댓값을 공유하며, 그 최댓값이 시행이 내놓는 유일한 숫자다.

> [!note] 검증과 타당성 확인은 다르다 · Verification is not validation
> "테스트"라는 한 단어 아래 서로 다른 두 질문이 숨어 있고, 한쪽에 답하는 설계가 다른 쪽에는
> 답하지 못한다. *Verification*(검증)은 시스템이 명세대로 만들어졌는지 묻는다. 코드가 명세와
> 맞는가, 인터록이 문서대로 배선됐는가, 모델 버전이 보고된 그것인가. *Validation*(타당성 확인)은
> 그 명세 자체가 옳은지 묻는다. 벤치마크의 성공 정의가 사용자가 실제로 원하는 행동과 같은가,
> 시험 환경이 배치 환경을 대표하는가. 로봇은 모든 verification 시험을 통과하고도 틀린 목표에
> validation될 수 있다. 그리고 그 실패는 설계 문제가 아니라 모델링 문제처럼 보인다.
>
> 이 연구가 둘 중 무엇을 생산하는지 정하는 일은 실행 전 설계 단계에 속한다. 귀결이 둘 더 있다.
> 위의 변수와 단위는 verification 주장을 자연스럽게 받쳐 주지만, validation은 대개 그 실험이
> 만들어지지 않은 비교를 요구한다. 그리고 둘 다 출판에서 끝나지 않는다. 배치된 시스템은 변하는
> 환경과 늙어 가는 하드웨어를 만나므로, 허용 가능한 위험 안에 머무는지는 한 번 확립하는 것이
> 아니라 계속 확인하는 일이다.

### 2. 비교

강한 베이스라인은 제안된 기여를 분리한다. 실용적인 기존 시스템, 더 단순한 방법,
필요하면 사용할 수 없는 정보로 상한을 추정하는 **oracle**을 포함하라. Oracle은 표시돼야
하며 배포 가능한 경쟁자가 아니다.

같은 장면/과제를 두 조건에서 평가할 수 있으면 짝지은 비교를 써라. 학습·배터리·마모·
날씨·운용자 효과를 줄이도록 순서를 무작위화하거나 counterbalance하라.

바꾼 요인이 질문과 맞아야 설명력 있는 비교가 된다. 새 촉각 구조에 시연과 사전학습 인코더도 추가하고 베이스라인은 처음부터 학습했다고 하자. 점수 차이는 구조, 데이터, 표현 또는 상호작용에서 올 수 있다. 이렇게 통제되지 않은 차이를 **혼입**(confound)이라 한다. 제안한 요인이 아닌데 결과를 달리 설명할 수 있는 차이라는 뜻이다. 자가점검에서 지적한 혼입을 설계 단계에서 막아야 대표 결과의 의미가 흐려지지 않는다.

시스템 수준 비교라면 자원을 공개한 전체 패키지끼리의 경쟁도 유익하다. 구조에 대한 주장이면 데이터, 초기화, 튜닝 기회, 제어 인터페이스를 맞춘 비교를 추가한다.

**여기서 얻는 독법.** 베이스라인 설명을 각 방법이 가진 정보와 자원 목록으로 읽는다. 결과가 어느 차이를 분리할 수 있는지 묻는다. 오라클은 더 좋은 정보가 줄 여지를 보여 준다. 배포 가능한 방법이 그 정보를 실제 얻는다는 증거는 아니다.

**RS1에서는.** A는 실용적인 기존 시스템이므로 베이스라인이다. B가 바꾸는 요인이 제어 법칙 하나가 되려면 A의 문턱과 B의 이득이 같은 튜닝 시행에서 같은 튜닝 노력을 받아야 한다. 그렇지 않으면 튜닝이 혼입이 된다. 이 질문의 oracle은 별도 센서로 정확한 접촉 시각을 아는 정지일 것이다. 어떤 문턱 정지든 도달할 수 있는 상한을 알려 주며, 그렇다고 표시해야 한다. 짝짓기는 가능하고 비용도 적다. 시작 자세와 패널 위치를 하나의 무작위 목록에서 뽑아 두 제어기를 각각에서 돌리고, 순서를 블록 단위로 번갈아(ABBA) 마모·온도·패널 드리프트가 양쪽에 고르게 떨어지게 한다. worked case의 표본 크기는 독립된 두 군을 가정한다. 짝지은 분석([[02-foundations/probability|3. 확률 §6]])은 시작 조건이 퍼짐의 일부를 설명하면 시행이 덜 들고, 그렇지 않으면 비슷하게 든다.

### 3. 변동과 분할

학습/튜닝/시험 데이터를 분리하고 분할의 단위를 문서화하라. 같은 궤적의 무작위 프레임은
장면·물체·시간 정보를 누출한다. 관련 변동 전반 — 과제, 배치, 재료, 조명/날씨, 하드웨어,
운용자, 속도, 실패 교란 — 에 걸쳐 시험하라.

> [!example] 계산 예제 · Worked example
> **작은 개선에는 변동 정보가 필요하다.** 가상 실험에서 시드 간 표준편차가 4%p다. 독립 시드 3개면 평균의 표준오차는 4/√3 ≈ 2.3%p다. 5개면 약 1.8%p, 10개면 약 1.3%p다.
>
> 3%p 개선은 이 불확실성과 비슷한 규모다. 표준오차는 신뢰구간이 아니다. 차이의 불확실성은 베이스라인의 변동과 짝지은 설계 여부에도 달려 있다. 이 값만으로 유의하거나 유의하지 않다고 판정할 수 없다.
>
> **여기서 얻는 독법.** 작은 개선을 읽기 전에 시드 수, 변동, 비교 설계를 확인한다. 시드를 늘리면 학습 변동을 측정한다. 이웃 프레임을 학습과 시험으로 나눈 누수를 고치거나 새로운 표면의 시험을 대신하지는 못한다.

**RS1에서는.** 파일럿이 A의 문턱과 B의 이득을 골랐으므로 그 스무 번의 시행은 튜닝 데이터다. 설계와 계획용 효과를 정하는 데는 써도 되지만 확증 검정에 들어가서는 안 된다. 다시 쓰는 것은 [[02-foundations/ml-practice|9. ML 실무 §1]]의 시험 집합 누수를 실험의 형태로 저지르는 일이다. 주장이 여러 패널 위치에서 성립해야 한다면 적어도 한 위치는 튜닝에서 완전히 빼 둔다.

### 4. 시행 수와 불확실성

*한 문장으로:* 시행 몇 번으로는 무언가가 얼마나 자주 되는지 못 박을 수 없으므로 시행 수는 실험 전에 정해야 하고, 랩은 실험 전체를 컴퓨터에서 만 번 넘게 돌려 그 결정을 확인한다.

*이 절에서 하나만 가져간다면:* $n$회 시행에서 얻은 성공률의 불확실성은 최대 $\pm1/\sqrt{n}$ — 파일럿의 팔당 $10$회에서 $\pm32$%p — 이고, RS1의 성공 결과는 검정력 $0.8$을 위해 팔당 $32$회가 필요하며, 아래 랩이 시뮬레이션으로 그것을 확인한다($32$에서 $0.82$).

시행 수, 독립 실행, 실패, 제외, 집계 방식, 설계에 맞는 불확실성 지표를 보고하라. 시드는
소프트웨어 무작위성만 잡는다; 물리 시행은 보정, 마모, 온도, 재료, 타이밍, 사람을 통해
변한다.

지표와 조건이 많아 체리피킹이 쉬울 때는 주요 결과(primary outcome)를 미리 선언하라.
통계적 유의성과 실질적 중요성은 다르다([[02-foundations/ml-practice|ML 실무 §5]]).
어떤 검정이 맞는지는 시행마다 어떤 수가 나오는지와 두 방법이 같은 시행에서 돌았는지로 정해진다([[02-foundations/probability|3. 확률 §6]]).
시행 수를 가늠하는 문해력 수준의 도구 둘.

첫째, $n$회 시행의 성공률 신뢰구간은 대략
**최대** $\pm 1/\sqrt{n}$이다(10회 → ±32%p; 100회 → ±10%p). 이 값은 정규근사 반폭 $1.96\sqrt{p(1-p)/n}$에서 나온다. 곱 $p(1-p)$는 $p = 0.5$에서 최대 0.25이고, $1.96\sqrt{0.25} = 0.98 \approx 1$이기 때문이다. **이 값은 구간이 가장 넓어질 때의 크기이고 $p = 0.5$에서만 도달한다** — 0이나 1 근처에서는 지나치게 비관적이고($p = 0.9$, $n = 10$이면 실제 반폭은 ±19%p), 100%를 넘는 불가능한 상한을 만든다. 그러니 성공률이 높을 때는 Wilson이나 정확 구간을 써라(두 구간 모두 [[02-foundations/probability|3. 확률 §6]]의 검정 선택 표에 있다).

둘째, $n$회에서 실패 0이면 3의
법칙(rule of three)은 참 실패율의 95% **상한**을 $\approx 3/n$으로 준다 — $n \gtrsim 30$에서만 성립하는 근사이고, $n = 10$이면 정확한 상한이 30%가 아니라 26%, $n = 5$면 60%가 아니라 45%다.

<svg viewBox="0 0 470 214" style="max-width:100%;height:auto" role="img" aria-label="시행 횟수에 따라 성공률의 불확실성이 줄어드는 방식">
  <g stroke="currentColor" stroke-width="1" opacity="0.35"><line x1="55" y1="24" x2="55" y2="140"/><line x1="55" y1="140" x2="415" y2="140"/><line x1="55.0" y1="140" x2="55.0" y2="146"/><line x1="100.8" y1="140" x2="100.8" y2="146"/><line x1="173.4" y1="140" x2="173.4" y2="146"/><line x1="252.9" y1="140" x2="252.9" y2="146"/><line x1="325.5" y1="140" x2="325.5" y2="146"/><line x1="405.0" y1="140" x2="405.0" y2="146"/></g>
  <path d="M55.0 90.8L58.8 92.2L62.7 93.6L66.5 94.9L70.4 96.2L74.2 97.5L78.1 98.7L81.9 99.9L85.8 101.0L89.6 102.2L93.5 103.2L97.3 104.3L101.2 105.3L105.0 106.3L108.9 107.3L112.7 108.2L116.6 109.1L120.4 110.0L124.3 110.9L128.1 111.7L132.0 112.5L135.8 113.3L139.7 114.1L143.5 114.8L147.4 115.6L151.2 116.3L155.1 116.9L158.9 117.6L162.8 118.2L166.6 118.9L170.5 119.5L174.3 120.1L178.2 120.6L182.0 121.2L185.9 121.7L189.7 122.3L193.6 122.8L197.4 123.3L201.3 123.7L205.1 124.2L209.0 124.7L212.8 125.1L216.7 125.5L220.5 125.9L224.4 126.3L228.2 126.7L232.1 127.1L235.9 127.5L239.8 127.9L243.6 128.2L247.5 128.5L251.3 128.9L255.2 129.2L259.0 129.5L262.9 129.8L266.7 130.1L270.6 130.4L274.4 130.7L278.3 130.9L282.1 131.2L286.0 131.4L289.8 131.7L293.6 131.9L297.5 132.2L301.3 132.4L305.2 132.6L309.0 132.8L312.9 133.0L316.7 133.2L320.6 133.4L324.4 133.6L328.3 133.8L332.1 134.0L336.0 134.1L339.8 134.3L343.7 134.5L347.5 134.6L351.4 134.8L355.2 134.9L359.1 135.1L362.9 135.2L366.8 135.4L370.6 135.5L374.5 135.6L378.3 135.7L382.2 135.9L386.0 136.0L389.9 136.1L393.7 136.2L397.6 136.3L401.4 136.4" fill="none" stroke="currentColor" stroke-width="2"/>
  <path d="M55.0 74.0L58.8 77.7L62.7 81.3L66.5 84.6L70.4 87.7L74.2 90.7L78.1 93.5L81.9 96.1L85.8 98.6L89.6 100.9L93.5 103.1L97.3 105.2L101.2 107.2L105.0 109.1L108.9 110.8L112.7 112.5L116.6 114.0L120.4 115.5L124.3 116.9L128.1 118.2L132.0 119.4L135.8 120.6L139.7 121.7L143.5 122.7L147.4 123.7L151.2 124.6L155.1 125.5L158.9 126.3L162.8 127.1L166.6 127.8L170.5 128.5L174.3 129.2L178.2 129.8L182.0 130.4L185.9 130.9L189.7 131.4L193.6 131.9L197.4 132.4L201.3 132.8L205.1 133.2L209.0 133.6L212.8 133.9L216.7 134.3L220.5 134.6L224.4 134.9L228.2 135.2L232.1 135.5L235.9 135.7L239.8 136.0L243.6 136.2L247.5 136.4L251.3 136.6L255.2 136.8L259.0 137.0L262.9 137.2L266.7 137.3L270.6 137.5L274.4 137.6L278.3 137.8L282.1 137.9L286.0 138.0L289.8 138.1L293.6 138.2L297.5 138.3L301.3 138.4L305.2 138.5L309.0 138.6L312.9 138.7L316.7 138.7L320.6 138.8L324.4 138.9L328.3 138.9L332.1 139.0L336.0 139.1L339.8 139.1L343.7 139.2L347.5 139.2L351.4 139.3L355.2 139.3L359.1 139.3L362.9 139.4L366.8 139.4L370.6 139.4L374.5 139.5L378.3 139.5L382.2 139.5L386.0 139.6L389.9 139.6L393.7 139.6L397.6 139.6L401.4 139.7" fill="none" stroke="currentColor" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/>
  <g fill="currentColor"><circle cx="100.8" cy="105.2" r="3.5"/><circle cx="252.9" cy="129.0" r="3.5"/><circle cx="405.0" cy="136.5" r="3.5"/></g>
  <g font-size="10" fill="currentColor" text-anchor="middle">
    <text x="55.0" y="158">5</text><text x="100.8" y="158">10</text><text x="173.4" y="158">30</text><text x="252.9" y="158">100</text><text x="325.5" y="158">300</text><text x="405.0" y="158">1000</text>
  </g>
  <g font-size="10.5" fill="currentColor">
    <text x="10" y="34">불확실성</text>
    <text x="106.8" y="101.2">&#177;32%p</text>
    <text x="258.9" y="125.0">&#177;10%p</text>
    <text x="365.0" y="130.5">&#177;3%p</text>
    <text x="316" y="172">시행 횟수 n (로그 축)</text>
  </g>
  <g stroke="currentColor"><line x1="55" y1="180" x2="85" y2="180" stroke-width="2"/><line x1="55" y1="196" x2="85" y2="196" stroke-width="1.7" opacity="0.6" stroke-dasharray="6 4"/></g>
  <g font-size="10.5" fill="currentColor"><text x="92" y="184">신뢰구간 반폭의 최대치, &#8776; 1/&#8730;n</text><text x="92" y="200">3의 법칙: 실패 0회 뒤 실패율의 95% 상한, 3/n (n &#8807; 30)</text></g>
</svg>

**RS1에서는.** 위의 두 도구는 *하나의* 비율을 중심으로 실험의 크기를 정한다. RS1은 두 비율과 두 평균을 비교하며, worked case는 거기서 정의한 네 양으로 그 표본 크기를 유도했다. 검정력 대신 정밀도로 계획하는 것은 같은 산수를 거꾸로 돌리는 일이다. 평균 힘 차이의 95% 반폭을 ±1 N으로 하려면 $n = 2(1.960 \times 1.958/1)^2 = 29.5$, 곧 제어기당 30회가 필요하다. 파일럿의 효과에 대한 검정력 계산보다 많은데, 차이를 ±1 N까지 좁히는 것은 3.16 N이 0과 다른지보다 더 세밀한 질문이기 때문이다. 주요 결과(최대 힘)와 부차 결과(10 N 기준 성공)를 각각의 검정과 함께 미리 선언하라. 파일럿이 이미 둘이 어긋날 수 있음을 보여 주었다.

#### 랩 — RS1의 검정력을 시뮬레이션으로

검정력 공식은 실험을 여러 번 돌리면 무슨 일이 일어날지에 대한 주장이다. 그러니 여러 번 돌려 본다. 시뮬레이션한 실험 하나는 명시한 모형에서 제어기당 $n$회를 뽑고, 분석에 쓸 검정을 적용해 $H_0$를 기각했는지 기록한다. $R = 20{,}000$개 실험 중 기각한 비율이 검정력의 추정값이고, 그 표준오차는 $\sqrt{p(1-p)/R}$이다 — 검정력 0.8에서 0.003, 가장 커도 0.0035 — 그래서 아래 표는 약 ±0.01까지 믿을 수 있다. 모형은 셋이며, 코드는 영어 절의 두 목록을 그대로 쓴다.

- **성공률**: 각 군의 성공 수가 파일럿의 $p_A = 0.6$, $p_B = 0.9$를 쓴 Binomial($n$, $p$)이고, 3단계의 합동 $z$-검정과 Fisher 정확 검정으로 검정한다;
- **힘**: 파일럿의 평균과 합동 $\sigma = 1.958$ N을 가진 정규분포이고, 자유도 $2n - 2$의 두 표본 $t$-검정으로 검정한다(두 군의 크기가 같으면 그 통계량은 Welch의 것과 정확히 같다);
- **같은 힘을 10 N에서 자른 것**: 시뮬레이션한 힘 실험 하나하나를 성공 수로 한 번 더 분석해, 자르는 일 자체의 비용만 떼어 낸다.

출력, 시드 1(다른 시드는 항목을 약 0.01 움직인다). 성공률, 참 성공률 0.6과 0.9:

| 제어기당 시행 | 공식 | 시뮬레이션 $z$-검정 | 시뮬레이션 Fisher |
|---:|---:|---:|---:|
| 5 | 0.18 | 0.19 | 0.06 |
| 10 | 0.33 | 0.30 | 0.16 |
| 15 | 0.47 | 0.51 | 0.32 |
| 20 | 0.60 | 0.62 | 0.49 |
| 25 | 0.70 | 0.73 | 0.59 |
| **32** | **0.81** | **0.82** | **0.74** |
| 40 | 0.89 | 0.90 | 0.85 |
| 50 | 0.95 | 0.95 | 0.92 |
| 60 | 0.97 | 0.98 | 0.96 |

최대 힘, 참 감소량 3.16 N, σ = 1.958 N:

| 제어기당 시행 | 공식(σ를 앎) | 시뮬레이션 $t$-검정 | 같은 힘을 10 N에서 자름 |
|---:|---:|---:|---:|
| 3 | 0.51 | 0.33 | 0.18 |
| 4 | 0.63 | 0.48 | 0.40 |
| 5 | 0.72 | 0.61 | 0.48 |
| 6 | 0.80 | 0.71 | 0.57 |
| 7 | 0.86 | 0.79 | 0.57 |
| **8** | **0.90** | **0.86** | **0.70** |
| 10 | 0.95 | 0.93 | 0.71 |
| 12 | 0.98 | 0.96 | 0.84 |
| 15 | 0.99 | 0.99 | 0.91 |
| 20 | 1.00 | 1.00 | 0.97 |

B의 참 성공률을 훑고 A는 0.6에 고정했다(새로 뽑은 난수라서 32회에서 첫 표의 0.82 대신 0.83이 나온다):

| 참 $p_B$ | 공식의 제어기당 시행 | 32회 검정력, 공식 | 32회 검정력, 시뮬레이션 | 공식의 $n$에서 시뮬레이션 |
|---:|---:|---:|---:|---:|
| 0.75 | 151.9 → 152 | 0.25 | 0.25 | 0.80 |
| 0.80 | 81.2 → 82 | 0.41 | 0.42 | 0.81 |
| 0.85 | 48.9 → 49 | 0.61 | 0.63 | 0.81 |
| 0.90 | 31.5 → 32 | 0.81 | 0.83 | 0.83 |
| 0.95 | 21.1 → 22 | 0.94 | 0.96 | 0.86 |

세 표가 말하는 것.

1. **공식은 $z$-검정의 것이다.** 모든 $n$에서 시뮬레이션한 $z$-검정과 0.04 안에서 맞고, 3단계가 말한 대로 25와 32 사이에서 0.80을 넘는다. 같은 시뮬레이션 실험에 돌린 Fisher 정확 검정은 보수적이다 — 32에서 0.74, 40에서 0.85 — 3단계의 연속성 보정값 37.9가 내다본 그대로다.
2. **힘에서는 작은 $n$에서 공식이 낙관적이다.** 공식은 σ를 안다고 가정하지만 $t$-검정은 그것을 추정하는 값을 치른다 — 제어기당 5회에서 0.72 대신 0.61, 7회에서 0.86 대신 0.79 — 그리고 8회에서야 0.80을 넘는다. 4단계의 "제어기당 8회"다.
3. **10 N에서 자르면 시행이 1.5–2배 든다.** 같은 시뮬레이션 힘에서 성공 수는 제어기당 12회에서야 0.80을 넘는데, 힘은 8회면 되었다. 5단계의 공식은 11.7 대 6.03이라고 했다. 이 열은 계단식으로도 움직인다 — 6회와 7회 모두 0.57 — 개수에 대한 검정은 몇 안 되는 도달 가능한 표에서만 기각할 수 있어서, 시행 하나를 더해도 검정력이 늘지 않을 수 있기 때문이다.
4. **참 성공률 전반에서** 공식의 $n$은 0.80–0.83을 내지만, 1 근처는 예외다. $p_B = 0.95$에서 제어기당 22회는 0.86을 낸다. 성공률이 1에 가까우면 정규근사가 나쁘고, 여기서는 안전한 쪽으로 틀린다. 차이를 0.30에서 0.15로 반으로 줄이면 $n$은 거의 다섯 배, 31.5에서 151.9가 된다. $n$은 $1/\Delta^2$에 비례하고 분산도 조금 바뀌기 때문이다.

같은 난수 흐름으로 두 번 더 돌린다. 파일럿 크기의 연구, 그리고 파일럿 자신의 힘 차이에 대한 부트스트랩 구간이다.

```text
10 per arm: power 0.29; mean observed gap 0.30, among significant runs 0.51 (true 0.30)
percentile bootstrap 95% CI for mean(A) - mean(B): [1.58, 4.80] N
```

**유의에 도달한 작은 연구는 효과를 과장한다.** 제어기당 10회에서 시뮬레이션한 모든 파일럿의 평균 차이는 참값 0.30이지만, 유의에 도달한 29%만 모으면 0.51이다. Gelman & Carlin(2014)은 이것을 M형(크기) 오류라 부른다. 제어기당 32회에서는 같은 평균이 0.33으로 내려간다. 6단계가, 효과가 있어 보여서 다음 단계로 넘어온 파일럿이 아니라 의미 있는 가장 작은 효과로 계획하는 이유다.

**파일럿 힘 차이의 부트스트랩 구간.** Welch의 $[1.28,\ 5.04]$ N에 비해 $[1.58,\ 4.80]$ N이다. 각 군의 힘 열 개를 복원추출로 다시 뽑는다 — 절차는 [[02-foundations/ml-practice|9. ML 실무]] worked case 4번에 정의되어 있다 — 그리고 10회에서는 대입(plug-in) 퍼짐을 물려받는다. 위의 신뢰구간 정의가 이것을 반례로 든 이유다. 그 하한도 계획용 숫자이고, 과제가 그 비용을 묻는다.

### 5. 절제와 예산

절제는 구조, 목적함수, 데이터, 센싱, 제어기, 하이퍼파라미터를 제거하거나 바꿀 수 있다.
해석을 분리할 만큼 나머지를 고정하라. 구조 이름만이 아니라 데이터, 컴퓨트, 튜닝 노력,
사전학습 자산, 센서, 제어 인터페이스를 비교하라.

구성요소를 빼면서 자원도 뺄 수 있으므로 예산 정렬이 중요하다. 촉각 모델을 절제 모델보다 더 오래 학습하면 정보와 학습 노력이 함께 바뀐다. 반대로 절제 모델에 맞지 않는 하이퍼파라미터를 그대로 강요해도 단순한 방법을 부당하게 약화할 수 있다.

전체·축소 파지 정책에 학습 예산과 대등한 튜닝 기회를 명시한다. 촉각 정보의 가치를 묻는 비교에서는 시연, 시험 조건, 하류 제어기를 고정한다. 촉각을 활용하려면 연산이 더 필요할 경우 그 교환 관계를 드러낸다. 부품 이름 안에 숨기지 않는다.

**여기서 얻는 독법.** 무엇을 맞추고 무엇을 재튜닝했는지 묻는다. 절제는 해당 자원 배분 아래의 결론을 지지한다. 배포 예산에서 어느 시스템이 더 나은지는 별도의 동일 연산 비교가 필요할 수 있다. 두 비교가 서로의 질문에 자동으로 답하지는 않는다.

**RS1에서는.** B에도 A의 힘 문턱 정지가 달려 있는지 밝혀라. 달려 있지 않다면 A 대 B는 제어 법칙과 정지의 유무, 두 가지를 한꺼번에 바꾸며, 법칙만 떼어 내는 절제는 같은 정지를 단 B다. 튜닝 예산도 맞춘다. A의 문턱에도 B의 이득에도 같은 수의 튜닝 시행을 쓰고 논문에 밝힌다.

### 6. 재현성 어휘

용어가 커뮤니티마다 다르므로 정의하고 써라. 유용한 관례:

- **Repeatability:** 같은 팀·장비·절차로 양립 가능한 결과를 얻는다.
- **Reproducibility:** 독립 팀이 제공된 산출물·절차로 양립 가능한 결과를 얻는다.
- **Replicability:** 독립 구현·연구가 같은 주장을 시험한다.

같은 숫자의 반복도 서로 다른 증거에서 올 수 있어 이 구분이 유용하다. 자기 팀이 저장한 파지 설정을 다시 돌리면 내부 일관성을 확인한다. 다른 팀이 공개 체크포인트를 쓰면 산출물과 설명의 이전 가능성을 확인한다. 별도 구현으로 같은 마찰 가설을 시험하면 원래 코드와 공학적 선택에 대한 의존성을 살핀다.

데이터, 구현, 하드웨어, 절차, 과학적 주장 중 무엇을 반복했는지 적는다. 학회마다 용어 정의가 다를 수 있으므로 명칭에만 기대지 않는다.

**여기서 얻는 독법.** 재현 주장 뒤에서 공유한 것과 바꾼 것을 본다. 원래 로그의 재실행은 독립적으로 준비한 표면에서의 연구보다 새 물리 조건에 대해 적은 것을 말한다. 편의상 같은 단어를 쓰더라도 그렇다.

각 용어는 무엇을 고정하느냐로 정의되므로, 정의 조건을 한 줄씩 적고 RS1에서 그 용어가 가리키는 후속 연구를 붙인다.

| 용어 | 팀 | 설정과 산출물 | 구현 | 새 시행 | RS1에서 |
|---|---|---|---|---|---|
| repeatability(반복성) | 같음 | 같음 | 같음 | 있음, 같은 장치 | 한 달 뒤 같은 팀이 자기 장치로 확증 프로토콜을 다시 돌린다 |
| reproducibility(재현성) | 독립 | 공개된 것 | 공개된 것 | 있음, 명세대로 만든 장치 | 다른 연구실이 공개된 제어기 코드·이득·패널 명세·분석 스크립트를 자기 평면 팔과 400 N/m 패널에서 돌린다 |
| replicability(재연성) | 독립 | 자체 | 독립 | 있음 | 다른 팔, 다른 패널, 독립된 임피던스 구현으로 임피던스 제어가 최대 접촉력을 낮추는지 시험한다 |

**반례:** 공개된 분석 스크립트를 공개된 힘 로그에 다시 돌리는 것. 새 시행이 없으므로 이 관례에서는 셋 중 어느 것도 아니다 — 실험이 아니라 산수를 확인한다 — 반면 출처의 National Academies 보고서는 바로 이것을 *reproducibility*라 부른다. 이 충돌이 관례를 밝혀야 하는 이유다.

### 7. 산출물 체크리스트

코드 커밋, 의존성/컨테이너, 모델·데이터 버전, 분할, 시드, 학습 명령, 설정, 보정, 프레임
관례, 제어기 이득, 펌웨어, 하드웨어 리비전, 시행 프로토콜, 원시 로그, 제외, 분석
스크립트를 기록하라. 물리적으로 무슨 일이 있었는지 재구성할 수 있을 만큼 상세해야 한다.

목록은 특정 시도를 재구성할 때 유용해진다. 예를 들어 저장된 센서 보정이 장착한 패드와 맞지 않아 촉각 파지가 실패할 수 있다. 학습 코드 공개만으로는 이 차이를 알 수 없다. 시행 기록이 그날의 보정·하드웨어 상태를 체크포인트와 명령 스트림으로 연결해야 한다.

보고한 시행마다 설정 스냅샷과 원본 로그를 연결하고 결과를 만든 분석 명령을 보존한다. 제외 이유도 남겨 다른 독자가 분모를 복원하게 한다. 리셋 절차도 기록한다. 정성껏 준비한 시작 자세가 핵심 실험 조건일 수 있다.

**여기서 얻는 독법.** 결과 하나를 골라 실제 시도까지의 전체 경로를 복원할 수 있는지 묻는다. 빠진 항목은 코드가 공개됐다는 일반 문구보다 재현성 한계를 정확히 알려 준다.

**RS1에서**, 최대 힘을 좌우하면서 가장 잃어버리기 쉬운 항목: 힘 센서의 보정과 저역 통과 차단 주파수(필터는 기록된 최댓값을 낮춘다), 센서 속도, A의 문턱과 B의 이득, 패널의 측정 강성과 고정 방식, 접근 속도와 시작 자세, 힘 궤적을 최댓값으로 바꾸는 스크립트. 제외한 시행은 이유와 함께 기록해 독자가 두 분모를 모두 복원할 수 있게 한다.

**항목마다 가르치는 곳.** 코드 커밋과 실험마다의 태그는 [[02-foundations/tools/git-research-code|12.2 연구 코드를 위한 Git §7]], 고정한 환경과 시드는 [[02-foundations/tools/python-research-code|12.3 연구 코드를 위한 Python §1, §7]], 설정 스냅샷과 로그 곁을 따라다니는 사이드카 파일은 [[02-foundations/tools/config-data-formats|12.4 설정과 데이터 형식 §3–§4]], 하드웨어 리비전과 부품을 매 시행 같은 자리에 돌려놓는 고정구는 [[02-foundations/tools/mechanical-design-fabrication|12.9 실험을 위한 기계 설계와 제작 §1, §7]], 학습이 클러스터의 시간 한도를 넘어 살아남는 데 필요한 체크포인트는 [[02-foundations/tools/gpu-clusters|12.7 GPU 클러스터 §6]], 그림을 같은 저장소에서 다시 만드는 논문은 [[02-foundations/tools/latex-figures-references|12.6 글쓰기 도구 §10]]이다.

### 8. 설계 예제

주장: 촉각 센싱이 삽입 회복을 개선한다. 같은 로봇, 제어기, 시연, 물체, 초기 오프셋,
실패 교란을 쓰라. vision-only와 vision+tactile을 무작위 짝지은 시행으로 비교하라. 삽입
성공, 최대 힘, 회복 시간, 손상, 개입, 지연, 실패 분류를 held-out 공차/재료에 걸쳐
보고하라.

이 선택들 중 무엇을 할지는 [[06-research-practice/research-questions-claims|연구 질문 §7]]의 주장–증거 표가 결판내며, 그 표는 어떤 실행보다 먼저 채운다. [[06-research-practice/research-questions-claims|연구 질문 §1]]의 마찰 질문을 끝까지 설계하자. 불확실성은 접촉 중 μ 추정이 잘못된 마찰 가정 때문에 잃은 파지 성공을 회복하는가다. 이점이 이미 관찰됐다는 보고가 아니라 제안 실험이다.

개입은 주어진 촉각 스트림으로 마찰 갱신을 켜는 것이다. 비교 대상은 고정 μ를 쓰는 같은 계획기다. 파지 후보, 시연, 제어 인터페이스, 센싱 기회를 대등하게 유지한다. 기준 마찰을 아는 조건은 특권 정보를 표시하면 개선 여지를 진단할 수 있다. 똑같이 배포 가능한 정책으로 제시하지 않는다.

시행을 세기 전에 단위를 정한다. 물체와 독립적으로 준비한 표면 조건은 물리적 변동의 주장을 지지한다. 학습 시드는 최적화 변동을 다룬다. 같은 물체·조건의 시도는 반복 관측이다. 센서 프레임을 독립 증거로 세지 말고 군집을 남긴다. 전이 주장에 필요한 표면 조건은 튜닝에서 제외한다.

짝지은 조건 안에서 방법 순서를 무작위화하거나 균형 배치한다. 표면 준비, 접촉 시점, 파지 실패, 운전자 정지, 리셋을 기록한다. 개입이 자율 시도를 끝내는지 미리 선언한다. 그렇지 않으면 한 방법이 더 많은 구조를 받고도 더 좋은 결정을 한 것처럼 보인다.

표본 수는 필요한 정밀도와 주장에 맞춰 정하고 §4의 도구를 계획 지침으로 쓴다. 편한 시행 수를 고른 뒤 신뢰성을 선언하지 않는다. 희귀 실패의 노출 논증은 평균 성능 비교와 다르다. 적절한 구간을 쓰고 분석에서 군집 구조를 보존한다.

조건별 성공과 불확실성, 회복 행동, 추정 시점, 실패 분류를 보고한다. 불필요한 보정의 비용과 연산 지연도 포함한다. 갱신이 결정적 접촉 뒤에 도착한다는 결과는 성공률 개선이 없어도 유용한 센싱 경계다. 최종 주장은 이 기전 증거와 건설 과제 전반의 전이 질문을 구분해야 한다. 그 구분을 Results 문장과 Discussion 문장으로 나눠 쓰는 법은 [[06-research-practice/scientific-writing-peer-review|과학 글쓰기 §5]]에 있다.

**이 페이지로 설계한 RS1.** *주장:* P2가 400 N/m 패널에 닿을 때, 임피던스 제어가 힘 문턱 정지보다 최대 접촉력을 낮춘다. *비교:* 베이스라인 A 대 B, 그리고 B에 정지가 없다면 A의 정지를 단 B(§5). *단위와 순서:* 접근과 접촉 한 번이 시행 하나; 시작 자세와 패널 위치는 하나의 무작위 목록에서 뽑아 두 제어기가 번갈아 드는 블록으로 쓴다(§2). *첫 시행 전에 선언한 결과:* 주요 결과는 최대 힘으로, Welch 검정과 차이의 구간으로 분석한다; 부차 결과는 10 N 기준 성공으로, Fisher 정확 검정을 쓴다(§4). *시행 수:* 제어기당 8회면 파일럿의 효과를 검정력 0.8로 잡는다. 여기서 의미 있는 최소 감소량으로 삼은 1.5 N을 잡으려면 제어기당 28회다(worked case 6단계, $t$ 보정 포함). *튜닝:* 파일럿의 스무 번이 이득을 골랐고 검정에서 빠진다(§3). *기록:* §7의 항목들과, 모든 제외와 그 이유. *출판:* 파일럿과 확인 실험은 주장 하나이므로 파일럿은 혼자 아카이브 venue로 가지 않는다. [[06-research-practice/venue-strategy|5. Venue 전략]]의 worked case가 저널 규칙을 따라가며 짚는 함정이다.

### 읽고 나면 말할 수 있어야 하는 것

- 변수와 진짜 실험 단위를 식별할 수 있다
- 짝지은 베이스라인을 설계하고 oracle 정보를 표시할 수 있다
- 로봇 데이터셋의 시간·장면 누출을 탐지할 수 있다
- 물리적 변동에 맞는 시행 수와 불확실성을 고를 수 있다
- 하드웨어·소프트웨어 조건을 재구성하는 데 필요한 산출물을 명시할 수 있다
- α, 검정력, 효과 크기, 신뢰구간을 정의하고 검정력이 의존하는 네 가지를 댈 수 있다
- 두 비율 표본 크기를 유도해 RS1의 제어기당 32회를 재현하고, 힘의 7회를 유도하며 $t$-검정이 8회를 요구하는 이유를 말할 수 있다
- 검정력을 시뮬레이션으로 추정하고, 그 시뮬레이션을 먼저 $H_0$ 아래에서 돌려 점검할 수 있다

### 스스로 점검

1. 한 실행의 비디오 프레임 10,000장이 10,000 시행이 아닌 이유는?
2. 짝지은 설계는 언제 유용한가?
3. 추가 데이터로 사전학습된 모델을 공개 없이 scratch 베이스라인과 비교하면 무엇이 불공정한가?
4. 코드 공유만으로 로봇 실험이 재현되지 않는 이유는?
5. 파일럿의 성공률 검정은 $p = 0.12$를 준다. 이것이 B가 A보다 안전하지 않다는 증거인가?
6. 파일럿의 $\hat d = 1.614$로 힘 실험을 계획하는 것은 서로 다른 두 방식으로 낙관적이다. 둘을 말하라.
7. 어떤 논문이 자기 연구가 "검정력 80%였다"고 쓴다. 이 문장이 뜻을 가지려면 무엇 넷을 함께 밝혀야 하는가?

> [!tip]- 정답 · Answers
> 1. 프레임들이 같은 장면, 상태 궤적, 보정, 실패 사건을 공유한다.
> 2. 두 방법이 같은 과제/장면/참가자를 마주할 수 있어 방해 변동이 줄어들 때.
> 3. 구조와 데이터·사전학습이 교란(confound)된다.
> 4. 하드웨어, 보정, 타이밍, 제어, 재료, 설정, 절차도 결과를 결정한다.
> 5. 아니다. 제어기당 10회, 참 성공률 0.6과 0.9에서 검정의 검정력은 약 0.3이므로 B가 더 안전해도 유의하지 않은 결과가 가장 그럴듯했고, 큰 p는 차이가 없다는 증거가 아니다([[02-foundations/probability|3. 확률 §6]], 오독 3). 같은 시행의 힘 판독은 $p = 0.003$을 준다.
> 6. 첫째, $\hat d$는 제어기당 10회에서 나온 추정값이다. 감소량의 구간은 1.28–5.04 N이고, 그 하한이라면 힘에 7회가 아니라 37회가 든다. 둘째, 선택: 좋아 보여서 다음으로 넘어온 파일럿은 대개 추정값이 높게 나온 파일럿이다 — 랩에서 유의에 도달한 10회 파일럿들은 참값 0.30에 대해 0.51의 차이를 보인다.
> 7. 가정한 참 효과, 검정과 그 α, 제어기당 시행 수, 설계(독립된 두 군인지 짝인지). 검정력은 넷 모두의 함수라서, 하나라도 빠지면 그 숫자는 뜻이 없다.

### 과제 · Problem set

Tier A. 이 페이지, 선수 지식, RS1만 쓴다. 변형은 더 작은 개선 — B의 참 성공률이 0.9가 아니라 0.8 — 과 파일럿 힘 효과의 불확실성이다.

1. **Draw.** 참 성공률 0.6과 0.8, 제어기당 32회에서 위 그림의 (a) 칸. $\mathrm{SE}_0$, $\mathrm{SE}_1$, $c$를 적고 검정력을 칠해 그 값을 읽어라. 실선의 중심은 $c$에 대해 어디에 있으며, 계산하기 전에 그것이 검정력에 대해 무엇을 말해 주는가?
2. **Derive.** (a) 참 성공률 0.6과 0.8, 양측 α = 0.05, 검정력 0.8에서 제어기당 시행 수. (b) 랩의 부트스트랩 구간은 파일럿의 힘 감소량을 1.58 N까지 낮게 둔다. σ = 1.958 N일 때 그것이 참 감소량이라면 힘에는 제어기당 몇 회가 필요한가? (c) RS1의 두 표본 크기(성공률 0.6과 0.9; $\hat d = 1.614$)를 α = 0.01에서 다시 구하라. $z_{0.995} = 2.576$이다. 둘 사이의 배수가 바뀌는가?
3. **Do.** 영어 절 템플릿의 `?`를 채워 돌려라. (a) 성공률 0.6과 0.8에서 제어기당 32, 50, 70, 82, 100회일 때 공식과 시뮬레이션의 검정력을 출력하라. 각각 어디서 0.80을 넘는가? (b) `alpha = 0.01`로 두고 $n$을 100에서 140까지 5씩 올려라. 시뮬레이션은 어디서 0.80을 넘고, 공식은 무엇이라 하는가? (c) 두 성공률을 모두 0.6으로 두어라. 시뮬레이션 열은 무엇을 보여야 하며, 공식 열은 왜 0.03을 출력하는가?

> [!note]- 그리는 법 · How to draw it
> - **축은 하나, 그 축은 데이터가 아니라 추정량이다:** 실험이 시행들로부터 추정할 차이 $\hat p_B - \hat p_A$.
> - **그 위의 두 곡선:** 점선은 두 제어기가 같을 때($H_0$) 추정량의 표본분포, 실선은 가정한 성공률이 참일 때($H_1$)의 표본분포로 두 성공률의 차이에 중심이 있다.
> - **임계값은 어떤 시행보다 먼저 정해진다:** $c = z_{1-\alpha/2}\,\mathrm{SE}_0$로 $\pm c$를 표시하라. $\mathrm{SE}_0$는 $H_0$ 아래의 표준오차(worked case 3단계)이며, $\mathrm{SE}_1$이 아니다.
> - **오경보율은 점선의 두 꼬리다:** $\pm c$ 바깥, 각각 $\alpha/2 = 0.025$.
> - **검정력은 다른 곡선 아래의 넓이다:** $c$ 너머의 실선 아래를 칠하고 그 값을 적어라. 칠하지 않은 나머지 실선 넓이가 $\beta$다.
> - **폭을 그림에 적어라:** $\mathrm{SE}_0$, $\mathrm{SE}_1$, $c$ — worked case의 칸에서는 0.108, 0.102, 0.212이고 검정력은 0.81이다.
> - **검정력이 읽는 것은 비율 하나다:** 대립가설이 0에서 귀무 표준오차 몇 개만큼 떨어져 있는가 — worked case의 칸에서는 2.77.

> [!tip]- 풀이 · Solutions
> 1. $\bar p = 0.7$이므로 $\mathrm{SE}_0 = \sqrt{2 \times 0.7 \times 0.3/32} = 0.1146$, $c = 1.960 \times 0.1146 = 0.2245$이고 $\mathrm{SE}_1 = \sqrt{(0.24 + 0.16)/32} = 0.1118$이다. 실선의 중심은 0.20으로 $c$의 *왼쪽*에 있으므로 절반도 $c$ 너머에 있지 않고, 계산 전에 이미 검정력은 0.5 미만이다. $\Phi\big((0.20 - 0.2245)/0.1118\big) = 0.41$, $\beta = 0.59$. 두 곡선이 거의 전부 겹친다. 차이 0.30에 충분한 제어기당 32회로는 차이 0.20을 믿을 만하게 보지 못한다.
> 2. (a) $\bar p = 0.7$이면 $(1.960\sqrt{0.42} + 0.842\sqrt{0.40})^2/0.2^2 = (1.2702 + 0.5323)^2/0.04 = 81.2$, 곧 제어기당 82회, 모두 164회다. 차이가 3분의 2로 줄었는데 RS1의 32회의 2.6배인 것은 $n$이 $1/\Delta^2$에 비례하기 때문이다. (b) $n = 2 \times 7.849 \times (1.958/1.58)^2 = 24.1$, 곧 제어기당 25회($t$ 보정으로 26회). 파일럿의 효과를 그 자신의 구간 하한으로 바꾸면 힘의 계획이 제어기당 7회에서 25회로 옮겨 간다. (c) $(z_{0.995} + z_{0.80})^2 = (2.576 + 0.842)^2 = 11.68$. 성공률: $(2.576 \times 0.6124 + 0.842 \times 0.5745)^2/0.09 = (1.5775 + 0.4835)^2/0.09 = 47.2$, 곧 제어기당 48회. 힘: $2 \times 11.68/2.605 = 8.97$, 곧 제어기당 9회. 배수는 $47.2/8.97 = 5.3$으로 α = 0.05의 5.2와 거의 같다. 더 엄격한 α는 둘을 함께 올릴 뿐, 10 N에서 자르는 비용은 거의 그대로 둔다.
> 3. 빈칸: `xA = rng.binomial(n, pA, R)`, `xB = rng.binomial(n, pB, R)`, `se = np.sqrt(2*pbar*(1 - pbar)/n)`, 문턱 `z(1 - alpha/2)`. (a) 공식 대 시뮬레이션: 32에서 0.41과 0.43, 50에서 0.59와 0.59, 70에서 0.74와 0.75, 82에서 0.80과 0.81, 100에서 0.88과 0.88 — Derive (a)대로 둘 다 약 82에서 0.80을 넘는다. (b) 두 열 모두 120에서 0.80, 125에서 0.81–0.82다. 공식의 $n$은 121.2, 곧 제어기당 122회로 α = 0.05일 때의 1.5배다. (c) 두 성공률이 같으면 모든 기각이 오경보이므로 시뮬레이션 열은 검정의 실제 오경보율이다. α = 0.05 근처여야 하고, 0.04–0.06이 나온다. 개수 검정의 도달 가능한 수준이 $n$에 따라 바뀌어 흔들린다. 공식이 0.03을 출력하는 것은 $+c$ 너머의 꼬리만 남기기 때문이다: $\Phi(-1.960) = 0.025$. 효과가 있으면 버린 꼬리는 무시할 만하지만, 효과가 없으면 답의 정확히 절반이다. $H_0$ 아래에서 약 α를 돌려주지 않는 시뮬레이션에는 버그가 있으니, 시뮬레이션을 쓸 때마다 이 점검을 먼저 하라.

### 출처

- [National Academies — *Reproducibility and Replicability in Science* (2019)](https://nap.nationalacademies.org/catalog/25303/reproducibility-and-replicability-in-science) — 기념비적 보고서; 단 본문에 제시한 ACM식 관례와 용어 구분이 다르다(reproducibility = 같은 데이터·같은 계산, replicability = 새 데이터)
- [Artifact Evaluation (artifact-eval.org)](https://www.artifact-eval.org/) — 독립 artifact 리뷰어가 실제로 확인하는 것
- [Sandve et al., *Ten Simple Rules for Reproducible Computational Research* (PLOS Comp Biol 2013)](https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285)
- Cohen, *Statistical Power Analysis for the Behavioral Sciences*, 2판 (Lawrence Erlbaum, 1988) — 효과 크기 $d$와 그 위에 세운 검정력 표
- Fleiss, Levin & Paik, *Statistical Methods for Rates and Proportions*, 3판 (Wiley, 2003) — 독립된 두 비율의 표본 크기, 연속성 보정 유무 모두
- Welch, "The generalization of 'Student's' problem when several different population variances are involved," *Biometrika* 34 (1947) — 분산이 다른 $t$-검정과 그 자유도
- Efron & Tibshirani, *An Introduction to the Bootstrap* (Chapman & Hall, 1993) — 백분위 구간
- Hoenig & Heisey, "The abuse of power: the pervasive fallacy of power calculations for data analysis," *The American Statistician* 55 (2001) — "관측 검정력"이 p-값에 아무것도 더하지 않는 이유
- Gelman & Carlin, "Beyond power calculations: assessing type S (sign) and type M (magnitude) errors," *Perspectives on Psychological Science* 9 (2014) — 작은 연구의 유의한 추정값이 큰 쪽으로 치우치는 이유
