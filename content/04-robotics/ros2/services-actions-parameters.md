---
title: "25.3 Services, Actions, Parameters and Lifecycle"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Choose correctly between a topic, a service and an action; configure a node with parameters from a file and the command line; and bring a node up through the managed-node state machine instead of hoping it started in order."
mastery-when: "Go deeper when you are designing the interface another team will depend on, or writing a lifecycle manager rather than using one."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to pick the right communication pattern, write both ends of it, and configure and start a node deterministically. Not enough to design a new action protocol.
> **Working** — 올바른 통신 패턴을 고르고, 양쪽 끝을 직접 작성하고, 노드를 결정론적으로 설정하고 기동할 정도. 새 액션 프로토콜을 설계할 정도는 아니다.

> [!note] Prerequisites · 선수 지식
> [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]], and through it [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], whose worked case (P6's $70\,\mathrm{ms}$ budget) and §5 (a QoS mismatch is silent) are used below; **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]]; and a working installation. Every command here assumes **ROS 2 Jazzy Jalisco on Ubuntu 24.04**, with each terminal sourced (`source /opt/ros/jazzy/setup.bash`).
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]], 그리고 그 앞의 [[04-robotics/ros2/what-ros2-is|25.1 ROS 2란 무엇인가]] — 그 계산 예제(P6의 $70\,\mathrm{ms}$ 예산)와 5절(QoS 불일치는 조용하다)을 아래에서 쓴다 — [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**, 그리고 동작하는 설치 환경. 여기의 모든 명령은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**를 전제하고, 터미널마다 `source /opt/ros/jazzy/setup.bash`가 되어 있다고 가정한다.

> [!note] First pass · 처음이라면
> Read the picture and the Worked case, then §1, whose closing table maps the four patterns to their sections. After that, read the part you need now — services §2–§3, actions §4–§5, parameters §6–§7, lifecycle §8 — because each part stands on its own. Do §10 before you write any node that calls a service, and §9 the first time you write an action. §8.3 (Nav2) is second-pass until you reach 25.9, and the C++ snippets can wait until you are reading somebody else's rclcpp.

### The picture: one P6 controller, four kinds of edge

<svg viewBox="0 0 560 464" style="max-width:100%;height:auto" role="img" aria-label="Top: the P6 graph with four kinds of edge: the topic /goal at 50 Hz from /camera to /controller, the service /controller/reset_odometry as a request and response pair with an operator, the action navigate as a lane between /controller and /planner with a goal, three feedbacks and a result, and the parameters as a table hanging off /controller. Middle: the camera's lifecycle, unconfigured, inactive, active, with the first /goal allowed only once active. Bottom: a healthy clock with 5 ms ticks running for 2 s under the action, and a broken clock with one tick and a client.call at t = 0 and then nothing, while the server answers at t = 0.">
  <defs><marker id="s3eopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="s3esol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="s3esols" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">The graph: four kinds of edge</text>
  <ellipse cx="60" cy="62" rx="40" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="60" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="330" cy="62" rx="52" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="330" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <ellipse cx="330" cy="184" rx="40" ry="14" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="330" y="188" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/planner</text>
  <line x1="100" y1="62" x2="276" y2="62" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#s3eopen)"/>
  <text x="189" y="55" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan> · 50 Hz</text>
  <rect x="470" y="48" width="80" height="28" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="510" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">operator</text>
  <line x1="466" y1="58" x2="388" y2="58" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none" marker-end="url(#s3esol)"/>
  <line x1="386" y1="66" x2="464" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none" marker-end="url(#s3esol)"/>
  <text x="548" y="38" font-size="11" text-anchor="end" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller/reset_odometry</text>
  <text x="392" y="90" font-size="11" fill-opacity="0.75" fill="currentColor">1 request, 1 response</text>
  <rect x="280" y="84" width="100" height="80" rx="6" fill="currentColor" fill-opacity="0.07" stroke="none"/>
  <rect x="280" y="84" width="100" height="80" rx="6" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="4 3" fill="none"/>
  <line x1="292" y1="89" x2="292" y2="158" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3esol)"/>
  <line x1="318" y1="159" x2="318" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <line x1="334" y1="159" x2="334" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <line x1="350" y1="159" x2="350" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <line x1="368" y1="159" x2="368" y2="90" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3esol)"/>
  <line x1="330" y1="77" x2="330" y2="84" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <line x1="330" y1="164" x2="330" y2="170" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <text x="394" y="112" font-size="11" fill-opacity="0.9" fill="currentColor">action <tspan font-family="ui-monospace,monospace">navigate</tspan></text>
  <text x="394" y="128" font-size="11" fill-opacity="0.85" fill="currentColor">goal at 0 s</text>
  <text x="394" y="144" font-size="11" fill-opacity="0.85" fill="currentColor">feedback at 0.5, 1.0, 1.5 s</text>
  <text x="394" y="160" font-size="11" fill-opacity="0.85" fill="currentColor">result at 2 s</text>
  <line x1="387" y1="120" x2="387" y2="130" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3esols)"/>
  <line x1="387" y1="146" x2="387" y2="136" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <line x1="387" y1="162" x2="387" y2="152" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3esols)"/>
  <text x="10" y="92" font-size="11" fill-opacity="0.75" fill="currentColor">parameters: a table, not an edge</text>
  <rect x="10" y="100" width="264" height="60" rx="3" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" fill="none"/>
  <line x1="10" y1="120" x2="274" y2="120" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3" fill="none"/>
  <line x1="10" y1="140" x2="274" y2="140" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3" fill="none"/>
  <text x="16" y="114" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">counts_per_metre</text>
  <text x="128" y="114" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">int64</text>
  <text x="180" y="114" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">2048</text>
  <text x="219" y="114" font-size="11" fill-opacity="0.8" font-style="italic" fill="currentColor">read-only</text>
  <text x="16" y="134" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">control_period</text>
  <text x="128" y="134" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">float64</text>
  <text x="180" y="134" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">0.005</text>
  <text x="16" y="154" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal_topic</text>
  <text x="128" y="154" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">string</text>
  <text x="180" y="154" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <line x1="309.7" y1="75.8" x2="272" y2="101" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5" fill="none"/>
  <text x="12" y="222" font-size="12" fill-opacity="0.8" fill="currentColor">The camera's lifecycle lane</text>
  <rect x="10" y="244" width="540" height="32" rx="6" fill="currentColor" fill-opacity="0.06" stroke="none"/>
  <rect x="16" y="249" width="88" height="22" rx="3" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" fill="none"/>
  <text x="60" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">unconfigured</text>
  <rect x="184" y="249" width="72" height="22" rx="3" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" fill="none"/>
  <text x="220" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">inactive</text>
  <rect x="336" y="249" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="366" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">active</text>
  <line x1="106" y1="260" x2="181" y2="260" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none" marker-end="url(#s3esol)"/>
  <text x="144" y="240" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">configure</text>
  <line x1="258" y1="260" x2="333" y2="260" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none" marker-end="url(#s3esol)"/>
  <text x="296" y="240" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">activate</text>
  <line x1="336" y1="238" x2="336" y2="282" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" stroke-dasharray="4 2" fill="none"/>
  <text x="404" y="257" font-size="11" fill-opacity="0.9" fill="currentColor">first /goal may appear here</text>
  <text x="404" y="271" font-size="11" fill-opacity="0.7" fill="currentColor">nothing publishes before it</text>
  <text x="12" y="306" font-size="12" fill-opacity="0.8" fill="currentColor">Two clocks, 0 to 2 s</text>
  <text x="12" y="328" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">healthy</text>
  <text x="102" y="340" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">action</text>
  <text x="102" y="364" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">ticks</text>
  <line x1="110" y1="336" x2="530" y2="336" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="110" y1="322" x2="110" y2="334.5" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3esol)"/>
  <text x="116" y="328" font-size="11" fill-opacity="0.8" fill="currentColor">goal accepted</text>
  <line x1="215" y1="336" x2="215" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <text x="215" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">feedback</text>
  <line x1="320" y1="336" x2="320" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <text x="320" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">feedback</text>
  <line x1="425" y1="336" x2="425" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3esols)"/>
  <text x="425" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">feedback</text>
  <line x1="530" y1="336" x2="530" y2="323" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3esol)"/>
  <text x="530" y="349" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">result</text>
  <path d="M110.00 355v10M111.05 355v10M112.10 355v10M113.15 355v10M114.20 355v10M115.25 355v10M116.30 355v10M117.35 355v10M118.40 355v10M119.45 355v10M120.50 355v10M121.55 355v10M122.60 355v10M123.65 355v10M124.70 355v10M125.75 355v10M126.80 355v10M127.85 355v10M128.90 355v10M129.95 355v10M131.00 355v10M132.05 355v10M133.10 355v10M134.15 355v10M135.20 355v10M136.25 355v10M137.30 355v10M138.35 355v10M139.40 355v10M140.45 355v10M141.50 355v10M142.55 355v10M143.60 355v10M144.65 355v10M145.70 355v10M146.75 355v10M147.80 355v10M148.85 355v10M149.90 355v10M150.95 355v10M152.00 355v10M153.05 355v10M154.10 355v10M155.15 355v10M156.20 355v10M157.25 355v10M158.30 355v10M159.35 355v10M160.40 355v10M161.45 355v10M162.50 355v10M163.55 355v10M164.60 355v10M165.65 355v10M166.70 355v10M167.75 355v10M168.80 355v10M169.85 355v10M170.90 355v10M171.95 355v10M173.00 355v10M174.05 355v10M175.10 355v10M176.15 355v10M177.20 355v10M178.25 355v10M179.30 355v10M180.35 355v10M181.40 355v10M182.45 355v10M183.50 355v10M184.55 355v10M185.60 355v10M186.65 355v10M187.70 355v10M188.75 355v10M189.80 355v10M190.85 355v10M191.90 355v10M192.95 355v10M194.00 355v10M195.05 355v10M196.10 355v10M197.15 355v10M198.20 355v10M199.25 355v10M200.30 355v10M201.35 355v10M202.40 355v10M203.45 355v10M204.50 355v10M205.55 355v10M206.60 355v10M207.65 355v10M208.70 355v10M209.75 355v10M210.80 355v10M211.85 355v10M212.90 355v10M213.95 355v10M215.00 355v10M216.05 355v10M217.10 355v10M218.15 355v10M219.20 355v10M220.25 355v10M221.30 355v10M222.35 355v10M223.40 355v10M224.45 355v10M225.50 355v10M226.55 355v10M227.60 355v10M228.65 355v10M229.70 355v10M230.75 355v10M231.80 355v10M232.85 355v10M233.90 355v10M234.95 355v10M236.00 355v10M237.05 355v10M238.10 355v10M239.15 355v10M240.20 355v10M241.25 355v10M242.30 355v10M243.35 355v10M244.40 355v10M245.45 355v10M246.50 355v10M247.55 355v10M248.60 355v10M249.65 355v10M250.70 355v10M251.75 355v10M252.80 355v10M253.85 355v10M254.90 355v10M255.95 355v10M257.00 355v10M258.05 355v10M259.10 355v10M260.15 355v10M261.20 355v10M262.25 355v10M263.30 355v10M264.35 355v10M265.40 355v10M266.45 355v10M267.50 355v10M268.55 355v10M269.60 355v10M270.65 355v10M271.70 355v10M272.75 355v10M273.80 355v10M274.85 355v10M275.90 355v10M276.95 355v10M278.00 355v10M279.05 355v10M280.10 355v10M281.15 355v10M282.20 355v10M283.25 355v10M284.30 355v10M285.35 355v10M286.40 355v10M287.45 355v10M288.50 355v10M289.55 355v10M290.60 355v10M291.65 355v10M292.70 355v10M293.75 355v10M294.80 355v10M295.85 355v10M296.90 355v10M297.95 355v10M299.00 355v10M300.05 355v10M301.10 355v10M302.15 355v10M303.20 355v10M304.25 355v10M305.30 355v10M306.35 355v10M307.40 355v10M308.45 355v10M309.50 355v10M310.55 355v10M311.60 355v10M312.65 355v10M313.70 355v10M314.75 355v10M315.80 355v10M316.85 355v10M317.90 355v10M318.95 355v10M320.00 355v10M321.05 355v10M322.10 355v10M323.15 355v10M324.20 355v10M325.25 355v10M326.30 355v10M327.35 355v10M328.40 355v10M329.45 355v10M330.50 355v10M331.55 355v10M332.60 355v10M333.65 355v10M334.70 355v10M335.75 355v10M336.80 355v10M337.85 355v10M338.90 355v10M339.95 355v10M341.00 355v10M342.05 355v10M343.10 355v10M344.15 355v10M345.20 355v10M346.25 355v10M347.30 355v10M348.35 355v10M349.40 355v10M350.45 355v10M351.50 355v10M352.55 355v10M353.60 355v10M354.65 355v10M355.70 355v10M356.75 355v10M357.80 355v10M358.85 355v10M359.90 355v10M360.95 355v10M362.00 355v10M363.05 355v10M364.10 355v10M365.15 355v10M366.20 355v10M367.25 355v10M368.30 355v10M369.35 355v10M370.40 355v10M371.45 355v10M372.50 355v10M373.55 355v10M374.60 355v10M375.65 355v10M376.70 355v10M377.75 355v10M378.80 355v10M379.85 355v10M380.90 355v10M381.95 355v10M383.00 355v10M384.05 355v10M385.10 355v10M386.15 355v10M387.20 355v10M388.25 355v10M389.30 355v10M390.35 355v10M391.40 355v10M392.45 355v10M393.50 355v10M394.55 355v10M395.60 355v10M396.65 355v10M397.70 355v10M398.75 355v10M399.80 355v10M400.85 355v10M401.90 355v10M402.95 355v10M404.00 355v10M405.05 355v10M406.10 355v10M407.15 355v10M408.20 355v10M409.25 355v10M410.30 355v10M411.35 355v10M412.40 355v10M413.45 355v10M414.50 355v10M415.55 355v10M416.60 355v10M417.65 355v10M418.70 355v10M419.75 355v10M420.80 355v10M421.85 355v10M422.90 355v10M423.95 355v10M425.00 355v10M426.05 355v10M427.10 355v10M428.15 355v10M429.20 355v10M430.25 355v10M431.30 355v10M432.35 355v10M433.40 355v10M434.45 355v10M435.50 355v10M436.55 355v10M437.60 355v10M438.65 355v10M439.70 355v10M440.75 355v10M441.80 355v10M442.85 355v10M443.90 355v10M444.95 355v10M446.00 355v10M447.05 355v10M448.10 355v10M449.15 355v10M450.20 355v10M451.25 355v10M452.30 355v10M453.35 355v10M454.40 355v10M455.45 355v10M456.50 355v10M457.55 355v10M458.60 355v10M459.65 355v10M460.70 355v10M461.75 355v10M462.80 355v10M463.85 355v10M464.90 355v10M465.95 355v10M467.00 355v10M468.05 355v10M469.10 355v10M470.15 355v10M471.20 355v10M472.25 355v10M473.30 355v10M474.35 355v10M475.40 355v10M476.45 355v10M477.50 355v10M478.55 355v10M479.60 355v10M480.65 355v10M481.70 355v10M482.75 355v10M483.80 355v10M484.85 355v10M485.90 355v10M486.95 355v10M488.00 355v10M489.05 355v10M490.10 355v10M491.15 355v10M492.20 355v10M493.25 355v10M494.30 355v10M495.35 355v10M496.40 355v10M497.45 355v10M498.50 355v10M499.55 355v10M500.60 355v10M501.65 355v10M502.70 355v10M503.75 355v10M504.80 355v10M505.85 355v10M506.90 355v10M507.95 355v10M509.00 355v10M510.05 355v10M511.10 355v10M512.15 355v10M513.20 355v10M514.25 355v10M515.30 355v10M516.35 355v10M517.40 355v10M518.45 355v10M519.50 355v10M520.55 355v10M521.60 355v10M522.65 355v10M523.70 355v10M524.75 355v10M525.80 355v10M526.85 355v10M527.90 355v10M528.95 355v10M530.00 355v10" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.6" fill="none"/>
  <text x="320" y="378" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">a 5 ms tick train: 400 periods in 2 s</text>
  <text x="12" y="394" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">broken</text>
  <text x="102" y="406" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">ticks</text>
  <text x="102" y="428" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">server</text>
  <line x1="110" y1="402" x2="530" y2="402" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="110" y1="397" x2="110" y2="407" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.95" fill="none"/>
  <text x="116" y="395" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">client.call</text>
  <text x="372.5" y="395" font-size="11" text-anchor="middle" fill-opacity="0.7" font-style="italic" fill="currentColor">nothing after t = 0: no ticks, no log lines, no error</text>
  <line x1="110" y1="424" x2="122" y2="424" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="111" y1="415" x2="111" y2="422.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none" marker-end="url(#s3esols)"/>
  <line x1="117" y1="422.5" x2="117" y2="415" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none" marker-end="url(#s3esols)"/>
  <text x="128" y="428" font-size="11" fill-opacity="0.8" fill="currentColor">answers normally at t ≈ 0</text>
  <line x1="110" y1="438" x2="530" y2="438" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35" fill="none"/>
  <line x1="110" y1="435" x2="110" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="215" y1="435" x2="215" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="320" y1="435" x2="320" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="425" y1="435" x2="425" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="530" y1="435" x2="530" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <text x="110" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="215" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0.5</text>
  <text x="320" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">1.0</text>
  <text x="425" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">1.5</text>
  <text x="530" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">2.0 s</text>
</svg>

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]] plus one node the earlier pages did not have, a `/planner` that takes up to $2\,\mathrm{s}$ to produce the next goal, with each of the four kinds of edge drawn as what it is: the topic `/goal` at $50\,\mathrm{Hz}$ as one open arrow, the service `/controller/reset_odometry` as one request and one response, the action `navigate` as a lane with a goal, feedback at $0.5$, $1.0$ and $1.5\,\mathrm{s}$ and a result at $2\,\mathrm{s}$, and the parameters as a table, not an edge. The middle lane is the camera's lifecycle, `unconfigured` → `inactive` → `active`, with nothing published before `activate`. The two clocks at the bottom share one $0$ to $2\,\mathrm{s}$ axis: in the healthy one the controller's $5\,\mathrm{ms}$ ticks, $400$ periods, run under the whole action; in the broken one a `client.call` inside the tick at $t=0$ is followed by nothing — no ticks, no log lines, no error — although the server answered at $t\approx0$.

### Worked case: what a blocking callback costs P6's 200 Hz loop

The controller's period is the unit of account for everything below:

$$T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=0.005\,\mathrm{s}=5\,\mathrm{ms}$$

so on a single-threaded executor (one thread running one ready callback at a time, each to completion; §3), which is what `rclpy.spin(node)` gives you, every millisecond another callback holds is a millisecond the control timer cannot run.

**Step 1 — a short handler is not free.** A service handler that takes $1\,\mathrm{ms}$ uses $1/5=20\%$ of every period it lands in. Nothing breaks, no message appears, and you have spent a fifth of the loop on a request that was supposed to be cheap. That is the correct mental model for "services return quickly": quickly means *relative to the fastest callback in the same node*.

**Step 2 — a handler the length of one vision period.** Take $D=20\,\mathrm{ms}$, the P6 camera's period, which is a plausible length for a handler that touches a file or waits for a device. The timer cannot fire while the executor is inside the handler, so

$$\left\lfloor \frac{D}{T_{\text{ctrl}}}\right\rfloor=\left\lfloor\frac{20}{5}\right\rfloor=4$$

firings do not happen on time, and the motor holds its last command for $20\,\mathrm{ms}$ instead of $5$. Against the plant's budget that is $20/70=28.6\%$ of the whole $70\,\mathrm{ms}$, spent on one request — the same loss as running the entire loop at $50\,\mathrm{Hz}$ (the worked case of [[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]], step 3). A single handler, once, costs what a four-fold reduction in control rate costs permanently.

**Step 3 — so a $2\,\mathrm{s}$ planner cannot be a service.** Put the same arithmetic on $D=2\,\mathrm{s}$ and the numerator is 400 times the period; the problem set asks you to finish that sentence. The point is not the size of the number, it is that the number exists at all: a service occupies the caller *and* the server's executor for its whole duration, so its duration is a property of the control loop, not of the planner. An action does not — the goal is accepted, the server works, feedback arrives, and the controller's timer keeps firing between the messages, because each of those is a separate short callback. That is the entire engineering content of "long work is an action".

**Step 4 — the unbounded case, which is the one you will actually hit.** Call a service synchronously *from inside* the control timer and $D$ is not $20\,\mathrm{ms}$ or $2\,\mathrm{s}$; it is infinite, because the response can only be delivered by the executor that your callback is standing on. Ticks lost: all of them. Log lines: none. Section 10 is the diagnosis, and the tell that separates it from a QoS mismatch (two endpoints whose delivery settings are incompatible, so they never connect and nothing complains; [[04-robotics/ros2/what-ros2-is|25.1 §5]]) is timing — a deadlocked node worked until the first trigger, a mismatched one never worked at all.

**Step 5 — the parameters, and the one that is worth a set-callback.** P6's constants belong in the parameter table, not in the source: `counts_per_metre` is an `int64` of $2048$ and `control_period` a `float64` of $0.005$. Declare `counts_per_metre` read-only, because changing the encoder scale while the cart is moving rescales the state estimate mid-flight. And notice what the type system cannot do for you here. Set it to $1024$ by mistake and every value is legal — it is a perfectly good `int64` — while the estimate becomes

$$\hat p=\frac{c}{1024}=2\cdot\frac{c}{2048}=2p$$

so at a true position of $0.5\,\mathrm{m}$, where the encoder reads $c=1024$ counts, the controller believes the cart is at $1.0\,\mathrm{m}$ and drives it half a metre the wrong way, with no error anywhere in the graph. Declared types catch a string in an integer; only a set-parameters callback (a function the node registers to inspect every proposed change, with the power to reject it; §6) that refuses anything but the encoder's datasheet number catches this.

### 1. Why topics are not enough

A topic is a one-way stream with no reply and no idea who is listening. That is exactly right for a camera, a joint state, a velocity command. It is wrong for three other things a robot constantly needs to do.

**"Compute this and tell me the answer."** Spawning a second turtle, resetting a map, querying an inverse-kinematics solver. You need a reply, and you need to know it answers *your* request. That is a **service**.

**"Do this; it will take a while; keep me posted; I may change my mind."** Drive to the kitchen. Plan and execute an arm trajectory. Ten seconds to ten minutes, with progress, and with the operator able to abort. That is an **action**.

**"Come up configured this way."** Which camera device, which control gains, which frame names — none of which you want in the source. That is **parameters**, and its companion problem — starting a system in a known order, where nothing publishes until its hardware is actually open — is **managed (lifecycle) nodes**.

The distinction beginners get wrong: they reach for a service because it looks simpler than an action, then write a service handler that takes eight seconds. Section 3 is what that costs.

The rest of the page takes the four in turn, and each part can be read on its own:

| Pattern | Sections | Reach for it when | On P6, in the picture |
|---|---|---|---|
| Service | §2–§3 | you need one answer, and it comes back quickly | `/controller/reset_odometry` |
| Action | §4–§5 | the work is long, reports progress, and may be cancelled | `navigate`, between `/controller` and `/planner` |
| Parameters | §6–§7 | a value configures a node instead of flowing through it | `counts_per_metre`, `control_period`, `goal_topic` |
| Lifecycle | §8 | a node must not work until its hardware is ready | the camera's `unconfigured` → `inactive` → `active` |

§9 is one sitting at the keyboard with an action, and §10 is the failure where a service meets the executor.

### 2. Services: request and response

*Pattern 1 of 4 — services, §2–§3.*

One node sends a request and waits; another node computes an answer and sends it back. That is a service: a remote procedure call, meaning a function call whose body runs in a different process. Its contract lives in a `.srv` file: request fields, then `---`, then response fields. The one used throughout the official tutorials is `example_interfaces/srv/AddTwoInts`:

```text
int64 a
int64 b
---
int64 sum
```

There should only ever be **one service server per service name** — with several, which one receives a request is undefined. There can be any number of clients. This is the opposite of topics, where several publishers on one name is legal (and, as [[04-robotics/ros2/describing-a-robot|25.6 Describing a Robot: URDF, TF2 and RViz]] will show, a common way to break a transform tree).

A Python server. The callback receives a filled `request` and an empty `response`, fills the response in, and returns it:

```python
from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response


def main():
    rclpy.init()
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

A Python client. Note `call_async`, which returns a **future** — a handle that will eventually hold the response — rather than the response itself:

```python
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)
```

and in `main`, `rclpy.spin_until_future_complete(minimal_client, future)` before reading `future.result()`. The `wait_for_service` loop matters: unlike a publisher, a client with no server is not merely quiet, it is broken, and you would rather say so than hang.

C++ has **no synchronous `call()`** — `rclcpp` gives you `async_send_request` only. That does not make C++ safe from section 10: blocking on the returned future (`.get()` or `.wait_for()`) inside a callback deadlocks in exactly the same way (the thread waits forever for a response that only that same thread could deliver; section 10 walks through it). The server is the same shape:

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
          std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
{
  response->sum = request->a + request->b;
}

// in main, after rclcpp::init:
//   auto node = rclcpp::Node::make_shared("add_two_ints_server");
//   auto service = node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);
```

From the command line, without writing either end:

```bash
ros2 service list -t
ros2 service type /add_two_ints
ros2 service find example_interfaces/srv/AddTwoInts
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

`ros2 service echo <name>` exists too, but it depends on service introspection, which is **disabled by default** — so an empty `echo` is not evidence that no calls are happening.

### 3. Why a service must be fast

The official concept documentation is blunt: services are expected to return quickly, because the client is generally waiting, and they should *never* be used for long-running processes — especially ones that might need to be preempted (stopped partway because a newer request or a cancel arrives).

There is a mechanical reason as well as a design one. By default a node runs on a **single-threaded executor**: one thread pulls one ready callback at a time and runs it to completion. A service callback that takes eight seconds is eight seconds in which that node processes no subscriptions, no timers, and no other service requests. The control loop in the same process stops. Nothing logs a warning; the node simply goes deaf. The executor mechanism, and the callback groups that change this behaviour, are [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]].

So the rule is not a style preference: **if the work is long, or cancellable, or you want progress, it is an action.**

### 4. Actions: long-running goals

*Pattern 2 of 4 — actions, §4–§5.*

An action is a service that takes time, reports progress, and can be cancelled. Underneath it is built out of topics and services, but you use it as one thing.

Its contract is a `.action` file with three message definitions separated by `---`: goal, result, feedback. The canonical example:

```text
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

The goal is the `order` to compute, the result is the final `sequence`, the feedback is the `partial_sequence` so far. Action definitions must live in a CMake (`ament_cmake`) package — a hard constraint, though a Python node can use the generated type — and are built by passing `"action/Fibonacci.action"` to `rosidl_generate_interfaces`. The full name is then `custom_action_interfaces/action/Fibonacci`.

The goal lifecycle is the part worth memorising, because it is what distinguishes an action from "a slow service":

| Stage | Who decides | What can happen |
|---|---|---|
| Goal sent | client | — |
| Goal accepted or rejected | server | A server may refuse outright — busy, out of range, unsafe |
| Executing | server | Feedback messages stream to the client |
| Cancel requested | client | The server may accept or reject the cancellation |
| Aborted | server | The server gives up, or preempts this goal for a newer one |
| Result | server | Delivered once, with a terminal status: SUCCEEDED, CANCELED or ABORTED |

Every goal gets a unique ID, which is how a client keeps several in flight straight. And "what happens when a second goal arrives" is a **server policy, not a rule**: turtlesim's rotation server aborts the previous goal, but another server may reject the new one or queue it. Do not assume.

This is why navigation and manipulation use actions. Driving to a waypoint takes minutes, the operator must be able to stop it, and the caller needs to know how far along it is — the three things a service cannot do. [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]] is an action interface from top to bottom.

Introspection first, as always:

```bash
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
```

### 5. Writing an action server and client

Python, using the `Fibonacci` action above. The whole of the goal's execution happens inside `execute_callback`, and feedback is pushed by calling `publish_feedback` on the goal handle:

```python
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(FibonacciActionServer())


if __name__ == '__main__':
    main()
```

`goal_handle.succeed()` is not optional decoration. If the execute callback never sets the state, the goal is assumed **aborted**, and you will get a warning and a puzzled client.

The client side is callback-driven, because there are three separate moments to react to — acceptance, feedback, result:

```python
def send_goal(self, order):
    goal_msg = Fibonacci.Goal()
    goal_msg.order = order
    self._action_client.wait_for_server()
    self._send_goal_future = self._action_client.send_goal_async(
        goal_msg, feedback_callback=self.feedback_callback)
    self._send_goal_future.add_done_callback(self.goal_response_callback)

def goal_response_callback(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected :(')
        return
    self._get_result_future = goal_handle.get_result_async()
    self._get_result_future.add_done_callback(self.get_result_callback)
```

Cancellation and rejection need the fuller server form, which takes `goal_callback` (accept or reject the goal), `cancel_callback` (accept or reject a cancellation) and `handle_accepted_callback`, and inside the execution loop checks `goal_handle.is_cancel_requested` and calls `goal_handle.canceled()`.

C++ makes the hazard explicit. `rclcpp_action::create_server` requires those three callbacks, and the accepted-goal callback must return immediately, so the tutorial spawns the work onto its own thread:

```cpp
auto handle_accepted = [this](const std::shared_ptr<GoalHandleFibonacci> goal_handle)
{
  // this needs to return quickly to avoid blocking the executor,
  // so we declare a lambda function to be called inside a new thread
  auto execute_in_thread = [this, goal_handle](){return this->execute(goal_handle);};
  std::thread{execute_in_thread}.detach();
};
```

That comment is section 3, restated by the library's own authors. Python's simple `ActionServer` hides the same hazard — a long `execute_callback` on a single-threaded executor blocks everything else in the node — which is why the `rclpy` examples pair a full action server with a `MultiThreadedExecutor` and a `ReentrantCallbackGroup`.

### 6. Parameters: configuring a node

*Pattern 3 of 4 — parameters, §6–§7.*

A parameter is a node setting, owned by that node, living exactly as long as it does. Each is a key, a value, and a **descriptor** (metadata about the parameter, such as its description, allowed range and whether it is read-only). The value is one of nine types and no others: `bool`, `int64`, `float64`, `string`, `byte[]`, `bool[]`, `int64[]`, `float64[]`, `string[]`. No dictionary, no nested struct — `some_lists.some_integers` is a dotted *name*, not a nesting.

A node must **declare** every parameter it will accept, so names and types are fixed at startup rather than discovered by a typo six months later:

```python
class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_parameter', 'world')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info('Hello %s!' % my_param)
```

The type is inferred from the default, and changing a declared parameter's type at runtime **fails** by default — a bool put into an int is caught, not absorbed. (For a genuinely polymorphic parameter, declare it with a descriptor whose `dynamic_typing` is true; for a node whose parameter names are not known in advance, construct it with `allow_undeclared_parameters`.)

The descriptor carries the description, ranges and other constraints, and is where **read-only** lives:

```python
from rcl_interfaces.msg import ParameterDescriptor
my_parameter_descriptor = ParameterDescriptor(description='This parameter is mine!')
self.declare_parameter('my_parameter', 'world', my_parameter_descriptor)
```

C++ is the same idea with more type:

```cpp
auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
param_desc.description = "This parameter is mine!";
this->declare_parameter("my_parameter", "world", param_desc);
// later: std::string p = this->get_parameter("my_parameter").as_string();
```

A read-only parameter can be set at startup and not afterwards. You will meet these without meaning to: every C++ (rclcpp) node's automatically declared `qos_overrides./parameter_events.*` parameters are read-only (rclpy nodes do not declare them), which is why `ros2 param load` prints failures for them and succeeds on the rest. Not a bug — the documentation says so explicitly.

To react to changes rather than poll, a node registers a **set-parameters callback** (`add_on_set_parameters_callback`), which inspects a proposed change and may reject it; a **pre-set** callback can amend it, and a **post-set** callback runs once it is accepted. The set callback must have no side effects — several can be chained, and none of them knows whether a later one will reject the update. Do the reacting in the post-set callback.

### 7. Setting parameters from a file and from the command line

Three routes, all of them outside the source code.

From the command line at startup, with `--ros-args -p name:=value`:

```bash
ros2 run demo_nodes_cpp parameter_blackboard --ros-args -p some_int:=42 -p "a_string:=Hello world" -p "some_lists.some_integers:=[1, 2, 3, 4]"
```

From a YAML file at startup. YAML is the plain-text format ROS 2 uses for parameter files (and for one of the three launch-file formats in 25.4): indentation nests one key under another, `[1, 2, 3]` is a list, and an unquoted value takes its type from its spelling — `42` an integer, `0.005` a float, `true` or `false` a boolean, most other words a string; quotes make anything a string. The file is keyed by node name, then the literal key `ros__parameters` (two underscores):

```yaml
parameter_blackboard:
    ros__parameters:
        some_int: 42
        a_string: "Hello world"
        some_lists:
            some_integers: [1, 2, 3, 4]

/**:
  ros__parameters:
    wildcard_full: "Full wildcard for any namespaces and any node names"
```

```bash
ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

`*` matches a single slash-delimited token and `**` matches zero or more, so `/**` is the wildcard every real launch file uses to hand one setting to a whole subsystem. Partial matches such as `foo*` are not allowed. And note the asymmetry that catches people: **a parameter file used at node startup updates all parameters, including the read-only ones** — the thing `ros2 param load` cannot do later.

At runtime, through the parameter services every node creates automatically:

```bash
ros2 param list /minimal_param_node
ros2 param describe /minimal_param_node my_parameter
ros2 param get /minimal_param_node my_parameter
ros2 param set /turtlesim background_r 150
ros2 param dump /turtlesim > turtlesim.yaml
ros2 param load /turtlesim turtlesim.yaml
```

Two traps in `ros2 param set`. The value is parsed as YAML, and the YAML 1.1 rules it follows also read `on`, `off`, `yes` and `no` as booleans, so `off` becomes a boolean and will be rejected for a string parameter — write `'!!str off'`, where `!!str` is YAML's explicit tag for "this value is a string". And ROS 2 has no heterogeneous lists, so a mixed YAML list is interpreted as a string. `ros2 param dump` piped to a file is the fastest honest way to record the configuration of a run you intend to reproduce.

### 8. Managed (lifecycle) nodes

*Pattern 4 of 4 — lifecycle, §8: states in §8.1, P6's numbers in §8.2, Nav2 in §8.3.*

An ordinary node starts working the moment it is constructed. For a laser, a camera or a motor driver that is wrong: the device takes seconds to boot, and a node that publishes nonsense while it warms up — or opens hardware before the rest of the system is ready — produces failures that look like sensor faults.

#### 8.1 States, transitions and their callbacks

A **managed node** (`LifecycleNode`) adds a state machine with four steady **primary states** — `unconfigured`, `inactive`, `active`, `finalized` — and intermediate **transition states** (`configuring`, `activating`, `deactivating`, `cleaningup`, `shuttingdown`, `errorprocessing`) that report whether a transition succeeded. The transitions you invoke are `configure`, `activate`, `deactivate`, `cleanup`, `shutdown`.

Each transition runs a callback you override: `on_configure` (allocate, open the device, create publishers and timers), `on_activate` (start publishing), `on_deactivate` (stop), `on_cleanup` (release), `on_shutdown`. All default to success, so a node can be managed without overriding anything.

`on_error` is the fallback for a failed transition. It runs in the `errorprocessing` state when a transition callback returns ERROR or throws. If it returns SUCCESS — the default in both rclcpp and rclpy — the node falls back to `unconfigured`; if it returns FAILURE the node goes to `finalized`.

One documentation trap: the demos README still says the default is failure; the source says otherwise.

The payoff is that publishing is gated by state. A lifecycle publisher created in `on_configure` exists in `inactive` but transfers nothing; `publish()` is a no-op until the node is `active`. Nothing downstream sees half-initialised data.

Every managed node exposes six interfaces for free: a `<node_name>/transition_event` topic, and services `get_state`, `change_state`, `get_available_states`, `get_available_transitions`, `get_transition_graph`. The CLI wraps them:

```bash
ros2 lifecycle nodes
ros2 lifecycle list /lc_talker
ros2 lifecycle get /lc_talker
ros2 lifecycle set /lc_talker configure
ros2 lifecycle set /lc_talker activate
```

Run `ros2 launch lifecycle lifecycle_demo_launch.py`, or the executables `lifecycle_talker`, `lifecycle_listener` and `lifecycle_service_client` in three terminals. The talker prints nothing at first — it starts `unconfigured`, exactly as designed.

In Python the node subclasses `rclpy.lifecycle.Node` (an alias for `LifecycleNode`), overrides `on_configure` and friends to return `TransitionCallbackReturn.SUCCESS`, and creates its publisher with `create_lifecycle_publisher`. In C++ it derives from `rclcpp_lifecycle::LifecycleNode` and the callbacks return `LifecycleNodeInterface::CallbackReturn`.

#### 8.2 The lifecycle on P6's numbers

Make P6's camera a managed node, and suppose its sensor needs $T_{\text{warm}}=1.5\,\mathrm{s}$ from power-on to its first valid frame — an assumed figure, since P6's catalog fixes only the rates. Started as an ordinary node that publishes from construction, the camera emits a goal every $20\,\mathrm{ms}$ whatever the sensor returns, and the controller acts on the newest one every $5\,\mathrm{ms}$, so the warm-up costs

$$n_{\text{goal}}=T_{\text{warm}}\,f_{\text{vision}}=1.5\times50=75,\qquad n_{\text{tick}}=T_{\text{warm}}\,f_{\text{ctrl}}=1.5\times200=300$$

invalid goals published and controller ticks spent driving the cart towards them. As a managed node the same camera opens the device and waits for its first valid frame inside `on_configure`, returning SUCCESS only then; the manager calls `activate` after that, and the lifecycle publisher drops every `publish()` before `activate`. Both counts are $0$. What the controller meets instead is a state the ordinary node hid, *no goal yet*, and it must hold the cart still until the first goal arrives. That explicit state is what the lifecycle bought.

The second number is the case the problem set asks about: the camera dies after activation. The controller's goal store keeps the last goal and every tick re-uses it, so the goal in use ages by $T_{\text{ctrl}}=5\,\mathrm{ms}$ per tick and is older than the whole budget within $70/5=14$ ticks. A lifecycle manager holding a bond with the camera notices only when the bond times out, and at Nav2's default `bond_timeout` of $4.0\,\mathrm{s}$ (§8.3) that is

$$\frac{4.0\,\mathrm{s}}{T_{\text{ctrl}}}=\frac{4.0}{0.005}=800\ \text{ticks},\qquad \frac{4000\,\mathrm{ms}}{70\,\mathrm{ms}}\approx57\ \text{budgets}$$

on a goal that is by then about four seconds old. So the lifecycle takes the stack down cleanly, but it is not the guard on the $70\,\mathrm{ms}$ budget. That guard is one comparison in `on_tick` — the goal's stamp against the node's clock, holding the cart once the difference passes $70\,\mathrm{ms}$ — and the bond is how the rest of the system finds out.

#### 8.3 Where you will meet it: Nav2

This is not academic: **Nav2 is built on it**, and you will meet it in [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]]. Its `map_server`, `planner_server` and `controller_server` are lifecycle-enabled, and `nav2_lifecycle_manager` drives them through `configure` and `activate` in ordered groups on startup, and in reverse on shutdown, via its `<manager_name>/manage_nodes` service (e.g. `lifecycle_manager_navigation/manage_nodes`). It also holds a **bond** (a periodic heartbeat exchanged between the manager and a server) with each server, so a node that crashes after activation is noticed and the stack is brought down rather than left half-running; `bond_timeout` (default 4.0 s) is how long it waits. When Nav2 "does nothing" on startup, ask which state its servers are in — `ros2 lifecycle get` answers in one line.

### 9. Exercise: an action server that reports feedback

One sitting. Work in the `ros2_ws` from 25.2; building and sourcing workspaces is [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]] if this is unfamiliar.

1. Create the interface package and the action:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces
mkdir custom_action_interfaces/action
```

Put the section 4 definition in `action/Fibonacci.action`; add `find_package(rosidl_default_generators REQUIRED)` and the `rosidl_generate_interfaces` block to `CMakeLists.txt` before `ament_package()`; add `<buildtool_depend>rosidl_default_generators</buildtool_depend>` and `<member_of_group>rosidl_interface_packages</member_of_group>` to `package.xml`; then `colcon build` from `~/ros2_ws` and `source install/local_setup.bash`.

2. Confirm the contract exists before writing code against it:

```bash
ros2 interface show custom_action_interfaces/action/Fibonacci
```

3. Save the section 5 server as `fibonacci_action_server.py` and run it with `python3 fibonacci_action_server.py`.

4. In a second terminal, send a goal *without* feedback, then with it:

```bash
ros2 action send_goal fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
```

The first prints the goal ID, waits about four seconds in silence, then prints the result and `SUCCEEDED`. The loop is `range(1, order)`, so `order: 5` gives four iterations of one second each. The second prints one `Feedback:` block per iteration — four of them — as `partial_sequence` grows. That difference *is* the argument for actions: same computation, but the caller can see inside it.

5. In a third terminal, watch the graph while a goal runs: `ros2 action list -t`, then `ros2 action info /fibonacci`.

6. Raise `order` to 30 and press Ctrl+C in the client mid-goal. The CLI sends a cancel request (`Canceling goal...`), but this server cannot service it while `execute_callback` blocks its only thread, and its default cancel callback would reject it anyway — so the client waits for the goal to finish and then reports `Failed to cancel goal`. Cancellation is a request the *server* must handle, not something a client can impose — which is why the full server form in section 5 exists.

You are done when you can say what each of the three parts of the `.action` file does, and why `--feedback` changes nothing on the server side.

### 10. The failure to diagnose: a service call inside a callback

A node subscribes to a trigger topic and, on each message, calls a service. In Python you used the synchronous `call()` because it reads better. The first message arrives and the node stops. Forever.

The symptom is the worst kind: **no error**. The official documentation states it plainly — no warning, no exception, nothing in a stack trace, and the call does not fail. The process is alive, the node is in the graph, and nothing happens.

```python
def trigger_request(msg):
    response = minimal_client.cli.call(minimal_client.req)  # synchronous call inside a callback: deadlock
```

The mechanism: `call()` blocks the thread until the response arrives, but the response can only be delivered by the executor spinning on *that same thread* — and that thread is inside your callback. The executor cannot preempt a running callback. The client waits for a response that only the waiter could deliver.

What finds it:

```bash
ros2 node list                  # the node is there
ros2 node info /your_node       # its subscriptions and service clients are all present
ros2 topic hz /its_output       # nothing — no messages arriving
ros2 service list | grep add_two_ints   # the server exists and is fine
```

Alive in the graph, producing nothing, with a healthy server on the other end — that combination is the signature. Distinguish it from a QoS mismatch (also silent) by checking whether the node produced output *before* the trigger arrived: a deadlocked node worked until the first trigger, a mismatched one never worked at all.

Three fixes, in order of preference. Use `call_async` and handle the future in a callback, which is safe from anywhere. Keep the call synchronous but put the *client* in a different **callback group** from the calling callback (or use a reentrant group) and run a multi-threaded executor. Or follow the documented pattern: spin in a separate thread and call from `main`, never from a callback. The executor and callback-group machinery behind all three is [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]]. C++ is not exempt: blocking on the future from `async_send_request` inside a callback deadlocks the same way, and the official callback-groups guide uses exactly that as its example.

### 11. What this page does not cover

Custom `.srv` and `.action` packages appear here only far enough to build one; the general interface-definition rules, and starting all of this from a launch file with parameters attached instead of six terminals, are [[04-robotics/ros2/workspaces-packages-launch|25.4 Workspaces, Packages, Builds and Launch]]. Executors, callback groups and the QoS settings that make services and actions connect at all are [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executors, Callback Groups and Time]] and [[04-robotics/ros2/qos-executors-time|25.5 Quality of Service]]. Actions as a system interface — a behaviour tree calling them, a lifecycle manager sequencing the servers — arrive in [[04-robotics/ros2/navigation-nav2|25.9 Navigation with Nav2]]. The rest of the track is [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Concepts: Services; Actions; Parameters.
- ROS 2 Jazzy documentation — Tutorials: Understanding services; Understanding parameters; Understanding actions; Writing a simple service and client (Python and C++); Creating an action; Writing an action server and client (Python and C++); Using parameters in a class (Python and C++); Managing node lifecycles.
- ROS 2 Jazzy documentation — How-to guides: Synchronous vs. asynchronous service clients; Using the `ros2 param` command-line tool; Passing ROS arguments to nodes via the command-line.
- ros2/demos — `lifecycle` package README (primary and transition states, transition callbacks, the lifecycle interfaces — the README says five, the source creates six); `lifecycle_py/lifecycle_py/talker.py`.
- ros2/examples — `rclpy/actions/minimal_action_server` (goal, cancel and accepted callbacks).
- ros2/ros2cli — `ros2lifecycle` verbs (`nodes`, `list`, `get`, `set`).
- ros-navigation/navigation2 — `nav2_lifecycle_manager` README and `lifecycle_manager.cpp` (ordered bringup, `manage_nodes` service, `bond_timeout` default).

### Self-check

1. You need a node to run a 30-second global plan on request. Service or action, and why?
2. `ros2 param load /my_node params.yaml` reports "successful" for some parameters and
   "cannot be set because it is read-only" for others. Is something broken?
3. A node you wrote is in `ros2 node list`, its service client and subscription show in
   `ros2 node info`, the server it calls is running, and it emits nothing after the first
   input. What is your first hypothesis?
4. Why does Nav2 use lifecycle nodes instead of ordinary ones?
5. A service handler on P6's controller node takes $20\,\mathrm{ms}$ on a single-threaded
   executor. How many $200\,\mathrm{Hz}$ firings does it cost, what does the motor do, and
   how does that compare with P6's $70\,\mathrm{ms}$ budget?

> [!tip]- Answers
> 1. Action. A service blocks the caller and cannot be preempted, and on a single-threaded executor a 30-second service callback stops every other callback in that node — timers, subscriptions, other services. Official guidance is that services return quickly and long work belongs in an action, which also gives you feedback and a cancellation path.
> 2. No. Read-only parameters can only be set at startup, and every C++ node declares read-only `qos_overrides./parameter_events.*` parameters, so a dump-then-load round trip on an rclcpp node prints those failures. To apply them, pass the same file at startup with `--ros-args --params-file`, which does update read-only parameters.
> 3. A synchronous service call from inside a callback. The executor cannot preempt the running callback to deliver the response, so the call waits forever — no exception, no warning, no failure. Confirm by checking that the node produced output before the first trigger; fix with `call_async`, or a separate callback group plus a multi-threaded executor.
> 4. Because bringup order matters and partial startup is dangerous. The lifecycle manager transitions the servers through `configure` and `activate` in ordered groups (reverse on shutdown), so nothing publishes or accepts goals before its resources exist, then holds a bond with each so a crash after activation brings the stack down deterministically. `ros2 lifecycle get <node>` is the one-line answer to "why is Nav2 doing nothing".
> 5. Four: $\lfloor 20/5\rfloor=4$ firings cannot happen while the executor is inside the handler, because a single-threaded executor runs one callback to completion at a time. The motor holds its last command for $20\,\mathrm{ms}$ instead of $5$, and $20\,\mathrm{ms}$ is $28.6\%$ of the $70\,\mathrm{ms}$ budget — one request costing what a permanent drop to a $50\,\mathrm{Hz}$ loop would cost. If the handler instead makes a synchronous service call from inside that timer callback, the duration is not $20\,\mathrm{ms}$ but unbounded, which is section 10.

### Problem set · 과제

Tier B. Using **P6** from [[02-foundations/lab-plants|0.6]]. The controller loop is $200\,\mathrm{Hz}$. A planner may take $2\,\mathrm{s}$ to produce the next goal. No new simulator.

1. **Draw.** P6 nodes: `planner` (long goal), `controller` ($5\,\mathrm{ms}$ timer + encoder), `camera` ($50\,\mathrm{Hz}$). Mark the planner–controller link as an *action*, not a topic or a service. Five-line timeline: goal sent, feedback at $0.5\,\mathrm{s}$, result at $2\,\mathrm{s}$, controller ticks throughout.
2. **Derive.** (a) How many control samples does a $2\,\mathrm{s}$ *service* callback block? (b) Encoder $\Delta p$ for one count. (c) Silent case: inside the $200\,\mathrm{Hz}$ timer the controller logs `calling`, then calls the planner with `client.call`. What does the log show from the first tick on, and why is there no error?
3. **Interpret.** Why is a P6 goal an action, and what does lifecycle buy you when the camera driver dies after the controller is already at $200\,\mathrm{Hz}$?

> [!note]- How to draw it · 그리는 법
> - Each kind of edge gets its own pen stroke, and no two may look alike: the whole of this page is the distinction.
> - A topic is one open arrow: `/goal`, $50\,\mathrm{Hz}$, `/camera` → `/controller`.
> - A service is a matched pair of short arrows in both directions, drawn tight together: one request, one response, nothing in between.
> - An action is a lane with three kinds of arrow — the goal down, several feedback arrows up along its length, one result arrow up at the end — with `/planner` and `/controller` at its two ends.
> - Parameters are not an edge at all: draw them as a small table hanging off `/controller` (name, type, value, and read-only where declared so), never as an arrow.
> - On the timeline the controller's $5\,\mathrm{ms}$ ticks run unbroken under the whole action, from the goal to the result.
> - A clock with one tick holding a `client.call` and nothing after it — no ticks, no log lines, no error, while the server answered at once — is §10's failure, not an action.

> [!tip]- Solutions
> 1. Action `navigate` from planner to controller; camera on `/goal` is a separate stream. Timeline: $t=0$ goal; ticks every $5\,\mathrm{ms}$; feedback; result at $2\,\mathrm{s}$.
> 2. (a) $2/0.005=400$ samples. (b) $0.488\,\mathrm{mm}$. (c) The timer holds the executor; the response callback cannot run; one `calling` and silence. No exception.
> 3. $2\,\mathrm{s}$ is not "return quickly"; the action keeps the $200\,\mathrm{Hz}$ loop alive and is cancellable. Lifecycle + a bond tears the stack down when the camera dies, instead of letting the controller track a stale $70\,\mathrm{ms}$ budget — but only once the bond times out, $4.0/0.005=800$ ticks at Nav2's default. The guard on the budget itself is a stamp check in `on_tick` (§8.2).

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 올바른 통신 패턴을 고르고, 양쪽 끝을 직접 작성하고, 노드를 결정론적으로 설정하고 기동할 정도. 새 액션 프로토콜을 설계할 정도는 아니다.
> **Working** — enough to pick the right pattern, write both ends, and start a node deterministically.

> [!note] 선수 지식 · Prerequisites
> [[04-robotics/ros2/nodes-topics-messages|25.2 노드, 토픽, 메시지]], 그리고 그 앞의 [[04-robotics/ros2/what-ros2-is|25.1 ROS 2란 무엇인가]] — 그 계산 예제(P6의 $70\,\mathrm{ms}$ 예산)와 5절(QoS 불일치는 조용하다)을 아래에서 쓴다 — [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**, 그리고 동작하는 설치 환경. 여기의 모든 명령은 **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco**를 전제하고, 터미널마다 `source /opt/ros/jazzy/setup.bash`가 되어 있다고 가정한다.
> 25.2 and, through it, 25.1 (its worked case and §5); **P6** from 0.6 Lab Plants; a working install. All commands assume ROS 2 Jazzy on Ubuntu 24.04, each terminal sourced.

> [!note] 처음이라면 · First pass
> 그림과 계산 절을 읽고, 이어서 1절을 읽어라. 1절 끝의 표가 네 패턴을 각자의 절에 짝지어 준다. 그다음은 지금 필요한 부분만 읽으면 된다 — 서비스 2–3절, 액션 4–5절, 파라미터 6–7절, 라이프사이클 8절 — 부분마다 따로 선다. 서비스를 호출하는 노드를 쓰기 전에 10절을, 액션을 처음 쓸 때 9절을 한다. 8.3절(Nav2)은 25.9에 닿기 전까지 두 번째 읽기이고, C++ 조각은 남의 rclcpp를 읽게 될 때까지 미뤄도 된다.

### 그림으로 먼저 보기: P6 제어기 하나와 네 종류의 간선 · The picture

<svg viewBox="0 0 560 464" style="max-width:100%;height:auto" role="img" aria-label="위: 간선 네 종류로 그린 P6 그래프. /camera에서 /controller로 가는 50 Hz 토픽 /goal, 조작자와 주고받는 요청·응답 한 쌍인 서비스 /controller/reset_odometry, /controller와 /planner 사이의 레인으로 그린 액션 navigate(목표, 피드백 셋, 결과), /controller에 매달린 표로 그린 파라미터. 가운데: 카메라의 라이프사이클 unconfigured, inactive, active와 active 이후에만 허용되는 첫 /goal. 아래: 액션 아래로 5 ms 틱이 2 s 내내 이어지는 정상 시계, 그리고 t = 0의 틱 하나와 client.call 뒤로 아무것도 없는 고장 시계, 그동안 서버는 t = 0에 응답한다.">
  <defs><marker id="s3kopen" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 1 1 L 9 5 L 1 9" fill="none" stroke="currentColor" stroke-width="1.6"/></marker><marker id="s3ksol" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker><marker id="s3ksols" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="20" font-size="12" fill-opacity="0.8" fill="currentColor">그래프: 간선 네 종류</text>
  <ellipse cx="60" cy="62" rx="40" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="60" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/camera</text>
  <ellipse cx="330" cy="62" rx="52" ry="15" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="330" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller</text>
  <ellipse cx="330" cy="184" rx="40" ry="14" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none"/>
  <text x="330" y="188" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/planner</text>
  <line x1="100" y1="62" x2="276" y2="62" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85" fill="none" marker-end="url(#s3kopen)"/>
  <text x="189" y="55" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor"><tspan font-family="ui-monospace,monospace">/goal</tspan> · 50 Hz</text>
  <rect x="470" y="48" width="80" height="28" rx="3" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none"/>
  <text x="510" y="66" font-size="11" text-anchor="middle" fill-opacity="0.9" fill="currentColor">조작자</text>
  <line x1="466" y1="58" x2="388" y2="58" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none" marker-end="url(#s3ksol)"/>
  <line x1="386" y1="66" x2="464" y2="66" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none" marker-end="url(#s3ksol)"/>
  <text x="548" y="38" font-size="11" text-anchor="end" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">/controller/reset_odometry</text>
  <text x="392" y="90" font-size="11" fill-opacity="0.75" fill="currentColor">요청 1, 응답 1</text>
  <rect x="280" y="84" width="100" height="80" rx="6" fill="currentColor" fill-opacity="0.07" stroke="none"/>
  <rect x="280" y="84" width="100" height="80" rx="6" stroke="currentColor" stroke-width="1" stroke-opacity="0.45" stroke-dasharray="4 3" fill="none"/>
  <line x1="292" y1="89" x2="292" y2="158" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3ksol)"/>
  <line x1="318" y1="159" x2="318" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="334" y1="159" x2="334" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="350" y1="159" x2="350" y2="91" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="368" y1="159" x2="368" y2="90" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3ksol)"/>
  <line x1="330" y1="77" x2="330" y2="84" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <line x1="330" y1="164" x2="330" y2="170" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.35" fill="none"/>
  <text x="394" y="112" font-size="11" fill-opacity="0.9" fill="currentColor">액션 <tspan font-family="ui-monospace,monospace">navigate</tspan></text>
  <text x="394" y="128" font-size="11" fill-opacity="0.85" fill="currentColor">목표 0 s</text>
  <text x="394" y="144" font-size="11" fill-opacity="0.85" fill="currentColor">피드백 0.5, 1.0, 1.5 s</text>
  <text x="394" y="160" font-size="11" fill-opacity="0.85" fill="currentColor">결과 2 s</text>
  <line x1="387" y1="120" x2="387" y2="130" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="387" y1="146" x2="387" y2="136" stroke="currentColor" stroke-width="1" stroke-opacity="0.7" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="387" y1="162" x2="387" y2="152" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3ksols)"/>
  <text x="10" y="92" font-size="11" fill-opacity="0.75" fill="currentColor">파라미터: 간선이 아니라 표</text>
  <rect x="10" y="100" width="264" height="60" rx="3" stroke="currentColor" stroke-width="1" stroke-opacity="0.6" fill="none"/>
  <line x1="10" y1="120" x2="274" y2="120" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3" fill="none"/>
  <line x1="10" y1="140" x2="274" y2="140" stroke="currentColor" stroke-width="0.6" stroke-opacity="0.3" fill="none"/>
  <text x="16" y="114" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">counts_per_metre</text>
  <text x="128" y="114" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">int64</text>
  <text x="180" y="114" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">2048</text>
  <text x="219" y="114" font-size="11" fill-opacity="0.8" font-style="italic" fill="currentColor">read-only</text>
  <text x="16" y="134" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">control_period</text>
  <text x="128" y="134" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">float64</text>
  <text x="180" y="134" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">0.005</text>
  <text x="16" y="154" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal_topic</text>
  <text x="128" y="154" font-size="11" fill-opacity="0.75" font-family="ui-monospace,monospace" fill="currentColor">string</text>
  <text x="180" y="154" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">goal</text>
  <line x1="309.7" y1="75.8" x2="272" y2="101" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.5" fill="none"/>
  <text x="12" y="222" font-size="12" fill-opacity="0.8" fill="currentColor">카메라의 라이프사이클 레인</text>
  <rect x="10" y="244" width="540" height="32" rx="6" fill="currentColor" fill-opacity="0.06" stroke="none"/>
  <rect x="16" y="249" width="88" height="22" rx="3" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" fill="none"/>
  <text x="60" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">unconfigured</text>
  <rect x="184" y="249" width="72" height="22" rx="3" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.8" fill="none"/>
  <text x="220" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">inactive</text>
  <rect x="336" y="249" width="60" height="22" rx="3" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.9" fill="none"/>
  <text x="366" y="264" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">active</text>
  <line x1="106" y1="260" x2="181" y2="260" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none" marker-end="url(#s3ksol)"/>
  <text x="144" y="240" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">configure</text>
  <line x1="258" y1="260" x2="333" y2="260" stroke="currentColor" stroke-width="1.2" stroke-opacity="0.8" fill="none" marker-end="url(#s3ksol)"/>
  <text x="296" y="240" font-size="11" text-anchor="middle" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">activate</text>
  <line x1="336" y1="238" x2="336" y2="282" stroke="currentColor" stroke-width="1.6" stroke-opacity="0.9" stroke-dasharray="4 2" fill="none"/>
  <text x="404" y="257" font-size="11" fill-opacity="0.9" fill="currentColor">여기서부터 첫 /goal 가능</text>
  <text x="404" y="271" font-size="11" fill-opacity="0.7" fill="currentColor">그 전엔 아무것도 publish 없음</text>
  <text x="12" y="306" font-size="12" fill-opacity="0.8" fill="currentColor">시계 둘, 0에서 2 s</text>
  <text x="12" y="328" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">정상</text>
  <text x="102" y="340" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">액션</text>
  <text x="102" y="364" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">틱</text>
  <line x1="110" y1="336" x2="530" y2="336" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="110" y1="322" x2="110" y2="334.5" stroke="currentColor" stroke-width="1.4" stroke-opacity="0.9" fill="none" marker-end="url(#s3ksol)"/>
  <text x="116" y="328" font-size="11" fill-opacity="0.8" fill="currentColor">목표 수락</text>
  <line x1="215" y1="336" x2="215" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <text x="215" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">피드백</text>
  <line x1="320" y1="336" x2="320" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <text x="320" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">피드백</text>
  <line x1="425" y1="336" x2="425" y2="324" stroke="currentColor" stroke-width="1" stroke-opacity="0.75" stroke-dasharray="3 2" fill="none" marker-end="url(#s3ksols)"/>
  <text x="425" y="349" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">피드백</text>
  <line x1="530" y1="336" x2="530" y2="323" stroke="currentColor" stroke-width="2.2" stroke-opacity="0.95" fill="none" marker-end="url(#s3ksol)"/>
  <text x="530" y="349" font-size="11" text-anchor="middle" fill-opacity="0.85" fill="currentColor">결과</text>
  <path d="M110.00 355v10M111.05 355v10M112.10 355v10M113.15 355v10M114.20 355v10M115.25 355v10M116.30 355v10M117.35 355v10M118.40 355v10M119.45 355v10M120.50 355v10M121.55 355v10M122.60 355v10M123.65 355v10M124.70 355v10M125.75 355v10M126.80 355v10M127.85 355v10M128.90 355v10M129.95 355v10M131.00 355v10M132.05 355v10M133.10 355v10M134.15 355v10M135.20 355v10M136.25 355v10M137.30 355v10M138.35 355v10M139.40 355v10M140.45 355v10M141.50 355v10M142.55 355v10M143.60 355v10M144.65 355v10M145.70 355v10M146.75 355v10M147.80 355v10M148.85 355v10M149.90 355v10M150.95 355v10M152.00 355v10M153.05 355v10M154.10 355v10M155.15 355v10M156.20 355v10M157.25 355v10M158.30 355v10M159.35 355v10M160.40 355v10M161.45 355v10M162.50 355v10M163.55 355v10M164.60 355v10M165.65 355v10M166.70 355v10M167.75 355v10M168.80 355v10M169.85 355v10M170.90 355v10M171.95 355v10M173.00 355v10M174.05 355v10M175.10 355v10M176.15 355v10M177.20 355v10M178.25 355v10M179.30 355v10M180.35 355v10M181.40 355v10M182.45 355v10M183.50 355v10M184.55 355v10M185.60 355v10M186.65 355v10M187.70 355v10M188.75 355v10M189.80 355v10M190.85 355v10M191.90 355v10M192.95 355v10M194.00 355v10M195.05 355v10M196.10 355v10M197.15 355v10M198.20 355v10M199.25 355v10M200.30 355v10M201.35 355v10M202.40 355v10M203.45 355v10M204.50 355v10M205.55 355v10M206.60 355v10M207.65 355v10M208.70 355v10M209.75 355v10M210.80 355v10M211.85 355v10M212.90 355v10M213.95 355v10M215.00 355v10M216.05 355v10M217.10 355v10M218.15 355v10M219.20 355v10M220.25 355v10M221.30 355v10M222.35 355v10M223.40 355v10M224.45 355v10M225.50 355v10M226.55 355v10M227.60 355v10M228.65 355v10M229.70 355v10M230.75 355v10M231.80 355v10M232.85 355v10M233.90 355v10M234.95 355v10M236.00 355v10M237.05 355v10M238.10 355v10M239.15 355v10M240.20 355v10M241.25 355v10M242.30 355v10M243.35 355v10M244.40 355v10M245.45 355v10M246.50 355v10M247.55 355v10M248.60 355v10M249.65 355v10M250.70 355v10M251.75 355v10M252.80 355v10M253.85 355v10M254.90 355v10M255.95 355v10M257.00 355v10M258.05 355v10M259.10 355v10M260.15 355v10M261.20 355v10M262.25 355v10M263.30 355v10M264.35 355v10M265.40 355v10M266.45 355v10M267.50 355v10M268.55 355v10M269.60 355v10M270.65 355v10M271.70 355v10M272.75 355v10M273.80 355v10M274.85 355v10M275.90 355v10M276.95 355v10M278.00 355v10M279.05 355v10M280.10 355v10M281.15 355v10M282.20 355v10M283.25 355v10M284.30 355v10M285.35 355v10M286.40 355v10M287.45 355v10M288.50 355v10M289.55 355v10M290.60 355v10M291.65 355v10M292.70 355v10M293.75 355v10M294.80 355v10M295.85 355v10M296.90 355v10M297.95 355v10M299.00 355v10M300.05 355v10M301.10 355v10M302.15 355v10M303.20 355v10M304.25 355v10M305.30 355v10M306.35 355v10M307.40 355v10M308.45 355v10M309.50 355v10M310.55 355v10M311.60 355v10M312.65 355v10M313.70 355v10M314.75 355v10M315.80 355v10M316.85 355v10M317.90 355v10M318.95 355v10M320.00 355v10M321.05 355v10M322.10 355v10M323.15 355v10M324.20 355v10M325.25 355v10M326.30 355v10M327.35 355v10M328.40 355v10M329.45 355v10M330.50 355v10M331.55 355v10M332.60 355v10M333.65 355v10M334.70 355v10M335.75 355v10M336.80 355v10M337.85 355v10M338.90 355v10M339.95 355v10M341.00 355v10M342.05 355v10M343.10 355v10M344.15 355v10M345.20 355v10M346.25 355v10M347.30 355v10M348.35 355v10M349.40 355v10M350.45 355v10M351.50 355v10M352.55 355v10M353.60 355v10M354.65 355v10M355.70 355v10M356.75 355v10M357.80 355v10M358.85 355v10M359.90 355v10M360.95 355v10M362.00 355v10M363.05 355v10M364.10 355v10M365.15 355v10M366.20 355v10M367.25 355v10M368.30 355v10M369.35 355v10M370.40 355v10M371.45 355v10M372.50 355v10M373.55 355v10M374.60 355v10M375.65 355v10M376.70 355v10M377.75 355v10M378.80 355v10M379.85 355v10M380.90 355v10M381.95 355v10M383.00 355v10M384.05 355v10M385.10 355v10M386.15 355v10M387.20 355v10M388.25 355v10M389.30 355v10M390.35 355v10M391.40 355v10M392.45 355v10M393.50 355v10M394.55 355v10M395.60 355v10M396.65 355v10M397.70 355v10M398.75 355v10M399.80 355v10M400.85 355v10M401.90 355v10M402.95 355v10M404.00 355v10M405.05 355v10M406.10 355v10M407.15 355v10M408.20 355v10M409.25 355v10M410.30 355v10M411.35 355v10M412.40 355v10M413.45 355v10M414.50 355v10M415.55 355v10M416.60 355v10M417.65 355v10M418.70 355v10M419.75 355v10M420.80 355v10M421.85 355v10M422.90 355v10M423.95 355v10M425.00 355v10M426.05 355v10M427.10 355v10M428.15 355v10M429.20 355v10M430.25 355v10M431.30 355v10M432.35 355v10M433.40 355v10M434.45 355v10M435.50 355v10M436.55 355v10M437.60 355v10M438.65 355v10M439.70 355v10M440.75 355v10M441.80 355v10M442.85 355v10M443.90 355v10M444.95 355v10M446.00 355v10M447.05 355v10M448.10 355v10M449.15 355v10M450.20 355v10M451.25 355v10M452.30 355v10M453.35 355v10M454.40 355v10M455.45 355v10M456.50 355v10M457.55 355v10M458.60 355v10M459.65 355v10M460.70 355v10M461.75 355v10M462.80 355v10M463.85 355v10M464.90 355v10M465.95 355v10M467.00 355v10M468.05 355v10M469.10 355v10M470.15 355v10M471.20 355v10M472.25 355v10M473.30 355v10M474.35 355v10M475.40 355v10M476.45 355v10M477.50 355v10M478.55 355v10M479.60 355v10M480.65 355v10M481.70 355v10M482.75 355v10M483.80 355v10M484.85 355v10M485.90 355v10M486.95 355v10M488.00 355v10M489.05 355v10M490.10 355v10M491.15 355v10M492.20 355v10M493.25 355v10M494.30 355v10M495.35 355v10M496.40 355v10M497.45 355v10M498.50 355v10M499.55 355v10M500.60 355v10M501.65 355v10M502.70 355v10M503.75 355v10M504.80 355v10M505.85 355v10M506.90 355v10M507.95 355v10M509.00 355v10M510.05 355v10M511.10 355v10M512.15 355v10M513.20 355v10M514.25 355v10M515.30 355v10M516.35 355v10M517.40 355v10M518.45 355v10M519.50 355v10M520.55 355v10M521.60 355v10M522.65 355v10M523.70 355v10M524.75 355v10M525.80 355v10M526.85 355v10M527.90 355v10M528.95 355v10M530.00 355v10" stroke="currentColor" stroke-width="0.5" stroke-opacity="0.6" fill="none"/>
  <text x="320" y="378" font-size="11" text-anchor="middle" fill-opacity="0.7" fill="currentColor">5 ms 틱의 연속: 2 s에 주기 400개</text>
  <text x="12" y="394" font-size="11" fill-opacity="0.85" font-weight="bold" fill="currentColor">고장</text>
  <text x="102" y="406" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">틱</text>
  <text x="102" y="428" font-size="11" text-anchor="end" fill-opacity="0.8" fill="currentColor">서버</text>
  <line x1="110" y1="402" x2="530" y2="402" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="110" y1="397" x2="110" y2="407" stroke="currentColor" stroke-width="1.8" stroke-opacity="0.95" fill="none"/>
  <text x="116" y="395" font-size="11" fill-opacity="0.9" font-family="ui-monospace,monospace" fill="currentColor">client.call</text>
  <text x="372.5" y="395" font-size="11" text-anchor="middle" fill-opacity="0.7" font-style="italic" fill="currentColor">t = 0 이후 아무것도 없음: 틱도, 로그도, 오류도 없음</text>
  <line x1="110" y1="424" x2="122" y2="424" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.4" fill="none"/>
  <line x1="111" y1="415" x2="111" y2="422.5" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none" marker-end="url(#s3ksols)"/>
  <line x1="117" y1="422.5" x2="117" y2="415" stroke="currentColor" stroke-width="1.1" stroke-opacity="0.85" fill="none" marker-end="url(#s3ksols)"/>
  <text x="128" y="428" font-size="11" fill-opacity="0.8" fill="currentColor">t ≈ 0에 정상 응답</text>
  <line x1="110" y1="438" x2="530" y2="438" stroke="currentColor" stroke-width="0.7" stroke-opacity="0.35" fill="none"/>
  <line x1="110" y1="435" x2="110" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="215" y1="435" x2="215" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="320" y1="435" x2="320" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="425" y1="435" x2="425" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <line x1="530" y1="435" x2="530" y2="441" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.5" fill="none"/>
  <text x="110" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0</text>
  <text x="215" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">0.5</text>
  <text x="320" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">1.0</text>
  <text x="425" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">1.5</text>
  <text x="530" y="452" font-size="11" text-anchor="middle" fill-opacity="0.8" fill="currentColor">2.0 s</text>
</svg>

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6** 카트에 앞 페이지들에 없던 노드 하나, 다음 목표를 만드는 데 최대 $2\,\mathrm{s}$가 걸리는 `/planner`를 더하고, 네 종류의 간선을 각각 그 정체대로 그렸다: $50\,\mathrm{Hz}$ 토픽 `/goal`은 열린 화살표 하나, 서비스 `/controller/reset_odometry`는 요청 하나와 응답 하나, 액션 `navigate`는 목표와 $0.5$, $1.0$, $1.5\,\mathrm{s}$의 피드백과 $2\,\mathrm{s}$의 결과가 있는 레인, 파라미터는 간선이 아니라 표. 가운데 레인은 카메라의 라이프사이클 `unconfigured` → `inactive` → `active`이고, `activate` 이전에는 아무것도 발행되지 않는다. 아래 두 시계는 같은 $0$에서 $2\,\mathrm{s}$ 축 위에 있다 — 정상 쪽에서는 제어기의 $5\,\mathrm{ms}$ 틱 $400$ 주기가 액션 내내 이어지고, 고장 쪽에서는 서버가 $t\approx0$에 응답했는데도 $t=0$ 틱 안의 `client.call` 뒤로 틱도 로그도 오류도 없다.

### 대상으로 한 번 끝까지: 블로킹 콜백이 P6의 200 Hz 루프에 물리는 값 · Worked case

아래 모든 것의 계산 단위는 제어기의 주기다.

$$T_{\text{ctrl}}=\frac{1}{200\,\mathrm{Hz}}=0.005\,\mathrm{s}=5\,\mathrm{ms}$$

`rclpy.spin(node)`가 주는 단일 스레드 executor(스레드 하나가 준비된 콜백을 한 번에 하나씩, 끝까지 돌리는 것. 3절)에서는 다른 콜백이 붙들고 있는 1밀리초가 곧 제어 타이머가 돌지 못하는 1밀리초이기 때문이다.

**1단계 — 짧은 핸들러도 공짜가 아니다**. $1\,\mathrm{ms}$ 걸리는 서비스 핸들러는 자기가 떨어진 주기의 $1/5=20\%$를 쓴다. 깨지는 것도 없고 메시지도 안 나오는데, 싸야 했던 요청 하나에 루프의 5분의 1을 쓴 것이다. "서비스는 빨리 반환한다"의 올바른 심상이 이것이다. 빠르다는 것은 *같은 노드에서 가장 빠른 콜백에 견주어* 빠르다는 뜻이다.

**2단계 — 비전 주기 하나만큼 걸리는 핸들러**. $D=20\,\mathrm{ms}$로 두자. P6 카메라의 주기이고, 파일을 건드리거나 장치를 기다리는 핸들러라면 그럴듯한 길이다. executor가 핸들러 안에 있는 동안 타이머는 돌 수 없으므로

$$\left\lfloor \frac{D}{T_{\text{ctrl}}}\right\rfloor=\left\lfloor\frac{20}{5}\right\rfloor=4$$

번의 발화가 제때 일어나지 못하고, 모터는 $5$가 아니라 $20\,\mathrm{ms}$ 동안 마지막 명령을 붙든다. 장치의 예산에 대면 $20/70=28.6\%$, 요청 하나에 $70\,\mathrm{ms}$의 4분의 1이 넘게 나간 것이다([[04-robotics/ros2/what-ros2-is|25.1 What ROS 2 Is]] 계산 예제 3단계). 핸들러 하나가 한 번 걸리는 값이 제어 주기를 영구히 네 배 늦추는 값과 같다.

**3단계 — 그래서 $2\,\mathrm{s}$짜리 플래너는 서비스일 수 없다**. 같은 산수를 $D=2\,\mathrm{s}$에 대면 분자가 주기의 400배가 된다. 그 문장을 끝내는 것이 과제다. 요점은 숫자의 크기가 아니라 그 숫자가 존재한다는 사실이다. 서비스는 그 시간 내내 호출자와 서버의 executor를 함께 점유하므로, 그 소요 시간이 플래너의 성질이 아니라 제어 루프의 성질이 된다. 액션은 그렇지 않다. 목표가 수락되고, 서버가 일하고, 피드백이 오고, 그 메시지들 사이에서 제어기의 타이머는 계속 발화한다. 각각이 짧은 콜백 하나씩이기 때문이다. "긴 작업은 액션"이라는 말의 공학적 내용이 전부 이것이다.

**4단계 — 그리고 실제로 당신이 맞을 무한대**. 제어 타이머 *안에서* 서비스를 동기 호출하면 $D$는 $20\,\mathrm{ms}$도 $2\,\mathrm{s}$도 아니고 무한이다. 응답을 전달할 수 있는 executor 위에 당신 콜백이 올라서 있기 때문이다. 잃는 틱: 전부. 로그 줄: 없음. 진단은 10절이고, QoS 불일치(전달 설정이 호환되지 않아 두 엔드포인트가 연결되지 않고 아무도 불평하지 않는 것. [[04-robotics/ros2/what-ros2-is|25.1 §5]])와 가르는 단서는 시간이다. 교착된 노드는 첫 트리거 전까지는 동작했고, 불일치한 노드는 처음부터 한 번도 동작하지 않았다.

**5단계 — 파라미터, 그리고 set 콜백을 붙일 값어치가 있는 하나**. P6의 상수는 소스가 아니라 파라미터 표에 산다. `counts_per_metre`는 $2048$인 `int64`, `control_period`는 $0.005$인 `float64`. `counts_per_metre`는 read-only로 선언한다. 카트가 움직이는 중에 엔코더 축척이 바뀌면 상태 추정이 통째로 다시 스케일되기 때문이다. 그리고 여기서 타입 체계가 해 주지 못하는 일을 보라. 실수로 $1024$를 넣어도 모든 값이 합법이다. 훌륭한 `int64`이기 때문이다. 그동안 추정치는

$$\hat p=\frac{c}{1024}=2\cdot\frac{c}{2048}=2p$$

가 되므로, 엔코더가 $c=1024$ 카운트를 읽는 실제 위치 $0.5\,\mathrm{m}$에서 제어기는 카트가 $1.0\,\mathrm{m}$에 있다고 믿고 반대 방향으로 반 미터를 몬다. 그래프 어디에도 오류는 없다. 선언된 타입은 정수 자리의 문자열을 잡지만, 이것을 잡는 것은 엔코더 데이터시트의 숫자 외에는 거부하는 set-parameters 콜백(노드가 등록해 두고 제안된 변경마다 검사해 거부할 수 있는 함수. 6절)뿐이다.

### 1. 토픽만으로 부족한 이유

토픽은 응답이 없고 누가 듣는지도 모르는 단방향 스트림이다. 카메라, 관절 상태, 속도 명령에는 정확히 맞다. 로봇이 늘 해야 하는 다른 세 가지에는 맞지 않는다.

**"이걸 계산해서 답을 달라."** 거북이 하나 더 띄우기, 지도 초기화, 역기구학 솔버 질의. 응답이 필요하고, 그 응답이 남의 요청이 아니라 *내* 요청의 것임을 알아야 한다. 이것이 **서비스**다.

**"이걸 해라. 오래 걸린다. 진행 상황을 알려 달라. 중간에 마음이 바뀔 수도 있다."** 주방까지 주행. 팔 궤적 계획과 실행. 10초에서 10분, 진행 보고가 있고, 조작자가 중단할 수 있어야 한다. 이것이 **액션**이다.

**"이런 설정으로 떠라."** 어느 카메라 장치, 어느 제어 게인, 어느 프레임 이름. 소스에 박고 싶지 않다. 이것이 **파라미터**이고, 그 짝이 되는 문제 — 하드웨어가 실제로 열리기 전에는 아무것도 발행하지 않는 상태로, 알려진 순서대로 시스템을 띄우는 일 — 이 **관리형(라이프사이클) 노드**다.

초심자가 틀리는 구분: 액션보다 간단해 보인다는 이유로 서비스를 고르고, 8초 걸리는 서비스 핸들러를 쓴다. 그 대가가 3절이다.

나머지 페이지는 넷을 차례로 다루고, 각 부분은 따로 읽어도 된다.

| 패턴 | 절 | 이럴 때 쓴다 | 그림 속 P6에서 |
|---|---|---|---|
| 서비스 | 2–3절 | 답 하나가 필요하고, 그 답이 빨리 돌아온다 | `/controller/reset_odometry` |
| 액션 | 4–5절 | 작업이 길고, 진행을 보고하고, 취소될 수 있다 | `/controller`와 `/planner` 사이의 `navigate` |
| 파라미터 | 6–7절 | 값이 노드를 지나가는 것이 아니라 노드를 설정한다 | `counts_per_metre`, `control_period`, `goal_topic` |
| 라이프사이클 | 8절 | 하드웨어가 준비되기 전에는 노드가 일하면 안 된다 | 카메라의 `unconfigured` → `inactive` → `active` |

9절은 키보드 앞에서 액션을 다루는 한 자리이고, 10절은 서비스가 executor와 만나는 고장이다.

### 2. 서비스: 요청과 응답

*네 패턴 중 첫째 — 서비스, 2–3절.*

한 노드가 요청을 보내고 기다리면, 다른 노드가 답을 계산해 돌려보낸다. 이것이 서비스다. 원격 프로시저 호출, 즉 몸체가 다른 프로세스에서 실행되는 함수 호출이다. 계약은 `.srv` 파일에 있다. 요청 필드, `---`, 응답 필드. 공식 튜토리얼 전체가 쓰는 `example_interfaces/srv/AddTwoInts`:

```text
int64 a
int64 b
---
int64 sum
```

한 서비스 이름당 **서버는 단 하나**여야 한다. 여럿이면 어느 서버가 요청을 받을지 정의되어 있지 않다. 클라이언트는 몇 개든 된다. 토픽과 정반대다. 토픽은 한 이름에 퍼블리셔가 여럿이어도 합법이고, [[04-robotics/ros2/describing-a-robot|25.6 로봇 기술하기: URDF, TF2, RViz]]에서 보듯 그것이 변환 트리를 깨는 흔한 방법이다.

Python 서버. 콜백은 채워진 `request`와 빈 `response`를 받아, 응답을 채우고 반환한다.

```python
from example_interfaces.srv import AddTwoInts

import rclpy
from rclpy.node import Node


class MinimalService(Node):

    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))

        return response


def main():
    rclpy.init()
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
```

Python 클라이언트. `call_async`는 응답 자체가 아니라 **future**(언젠가 응답을 담을 손잡이)를 돌려준다.

```python
class MinimalClientAsync(Node):

    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('service not available, waiting again...')
        self.req = AddTwoInts.Request()

    def send_request(self, a, b):
        self.req.a = a
        self.req.b = b
        return self.cli.call_async(self.req)
```

`main`에서는 `future.result()`를 읽기 전에 `rclpy.spin_until_future_complete(minimal_client, future)`를 호출한다. `wait_for_service` 루프가 중요하다. 퍼블리셔와 달리 서버 없는 클라이언트는 조용한 것이 아니라 고장 난 것이고, 매달리는 것보다 그렇게 말하는 편이 낫다.

C++에는 **동기 `call()`이 없다.** `rclcpp`는 `async_send_request`만 준다. 그렇다고 C++가 10절의 문제에서 안전한 것은 아니다. 콜백 안에서 돌려받은 future를 기다리면(`.get()`이나 `.wait_for()`) 똑같이 교착된다(스레드가 바로 그 스레드만 전달할 수 있는 응답을 영원히 기다린다. 10절에서 자세히 본다). C++ 서버는 모양이 같다.

```cpp
#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

void add(const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
          std::shared_ptr<example_interfaces::srv::AddTwoInts::Response>      response)
{
  response->sum = request->a + request->b;
}

// main에서 rclcpp::init 뒤에:
//   auto node = rclcpp::Node::make_shared("add_two_ints_server");
//   auto service = node->create_service<example_interfaces::srv::AddTwoInts>("add_two_ints", &add);
```

양쪽 다 안 쓰고 커맨드라인에서:

```bash
ros2 service list -t
ros2 service type /add_two_ints
ros2 service find example_interfaces/srv/AddTwoInts
ros2 service call /add_two_ints example_interfaces/srv/AddTwoInts "{a: 2, b: 3}"
```

`ros2 service echo <name>`도 있지만 서비스 introspection에 의존하고 그것은 **기본적으로 꺼져 있다.** 즉 `echo`가 비어 있다고 호출이 없다는 증거가 되지 않는다.

### 3. 서비스가 빨라야 하는 이유

공식 개념 문서는 단호하다. 클라이언트가 대개 기다리고 있으므로 서비스는 빨리 반환해야 하고, 장시간 프로세스에는 *절대* 쓰지 말아야 한다. 특히 선점(새 요청이나 취소가 와서 도중에 멈추는 것)이 필요할 수 있는 작업에는 그렇다.

설계상의 이유만이 아니라 기계적인 이유도 있다. 기본적으로 노드는 **단일 스레드 executor** 위에서 돈다. 스레드 하나가 준비된 콜백을 하나씩 꺼내 끝까지 실행한다. 8초 걸리는 서비스 콜백은 그 노드가 구독도, 타이머도, 다른 서비스 요청도 처리하지 않는 8초다. 같은 프로세스의 제어 루프가 멈춘다. 경고 로그는 없다. 노드가 그냥 귀를 닫는다. executor 기전과 이 동작을 바꾸는 콜백 그룹은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에 있다.

그러니 이 규칙은 취향이 아니다. **오래 걸리거나, 취소 가능해야 하거나, 진행 상황이 필요하면 액션이다.**

### 4. 액션: 장시간 목표

*네 패턴 중 둘째 — 액션, 4–5절.*

액션은 시간이 걸리고, 진행을 보고하고, 취소할 수 있는 서비스다. 내부는 토픽과 서비스로 만들어져 있지만, 쓸 때는 하나로 쓴다.

계약은 `---`로 구분된 메시지 정의 세 개가 든 `.action` 파일이다. 목표(goal), 결과(result), 피드백(feedback). 표준 예제:

```text
int32 order
---
int32[] sequence
---
int32[] partial_sequence
```

목표는 계산할 `order`, 결과는 최종 `sequence`, 피드백은 지금까지의 `partial_sequence`다. 액션 정의는 CMake(`ament_cmake`) 패키지에 있어야 한다. 이것은 강한 제약이지만 Python 노드가 그 결과물을 쓰는 것은 된다. 빌드는 `rosidl_generate_interfaces`에 `"action/Fibonacci.action"`을 넘겨서 한다. 전체 이름은 `custom_action_interfaces/action/Fibonacci`가 된다.

목표의 생애주기는 외워 둘 만하다. 액션을 "느린 서비스"와 구별해 주는 것이 바로 이것이다.

| 단계 | 결정 주체 | 일어날 수 있는 일 |
|---|---|---|
| 목표 전송 | 클라이언트 | — |
| 목표 수락 또는 거부 | 서버 | 서버는 거절할 수 있다 — 바쁨, 범위 밖, 위험 |
| 실행 중 | 서버 | 피드백 메시지가 클라이언트로 흐른다 |
| 취소 요청 | 클라이언트 | 서버가 취소를 수락하거나 거부한다 |
| 중단(abort) | 서버 | 서버가 포기하거나, 새 목표를 위해 이 목표를 선점한다 |
| 결과 | 서버 | 한 번 전달되며 종단 상태가 붙는다: SUCCEEDED, CANCELED, ABORTED |

모든 목표에는 고유 ID가 붙고, 클라이언트는 그것으로 여러 목표를 구분한다. 그리고 "두 번째 목표가 오면 어떻게 되는가"는 **규칙이 아니라 서버 정책이다.** turtlesim의 회전 서버는 이전 목표를 중단하지만, 다른 서버는 새 목표를 거부하거나 대기시킬 수 있다. 가정하지 마라.

내비게이션과 매니퓰레이션이 액션을 쓰는 이유가 이것이다. 경유점까지 주행은 몇 분이 걸리고, 조작자가 멈출 수 있어야 하고, 호출자는 얼마나 진행됐는지 알아야 한다. 셋 다 정확히 서비스가 못 하는 것이다. [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]은 위에서 아래까지 액션 인터페이스다.

늘 그렇듯 내성 먼저:

```bash
ros2 action list -t
ros2 action info /turtle1/rotate_absolute
ros2 interface show turtlesim/action/RotateAbsolute
ros2 action send_goal /turtle1/rotate_absolute turtlesim/action/RotateAbsolute "{theta: 1.57}"
```

### 5. 액션 서버와 클라이언트 작성

Python, 위의 `Fibonacci` 액션으로. 목표 실행 전체가 `execute_callback` 안에서 일어나고, 피드백은 goal handle의 `publish_feedback`으로 내보낸다.

```python
import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from custom_action_interfaces.action import Fibonacci


class FibonacciActionServer(Node):

    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')

        feedback_msg = Fibonacci.Feedback()
        feedback_msg.partial_sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            feedback_msg.partial_sequence.append(
                feedback_msg.partial_sequence[i] + feedback_msg.partial_sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)
            time.sleep(1)

        goal_handle.succeed()

        result = Fibonacci.Result()
        result.sequence = feedback_msg.partial_sequence
        return result


def main(args=None):
    rclpy.init(args=args)
    rclpy.spin(FibonacciActionServer())


if __name__ == '__main__':
    main()
```

`goal_handle.succeed()`는 장식이 아니다. execute 콜백이 상태를 설정하지 않으면 목표는 **중단(aborted)** 으로 간주되고, 경고와 어리둥절한 클라이언트를 얻는다.

클라이언트 쪽은 콜백 구동이다. 반응해야 할 순간이 수락, 피드백, 결과로 셋이기 때문이다.

```python
def send_goal(self, order):
    goal_msg = Fibonacci.Goal()
    goal_msg.order = order
    self._action_client.wait_for_server()
    self._send_goal_future = self._action_client.send_goal_async(
        goal_msg, feedback_callback=self.feedback_callback)
    self._send_goal_future.add_done_callback(self.goal_response_callback)

def goal_response_callback(self, future):
    goal_handle = future.result()
    if not goal_handle.accepted:
        self.get_logger().info('Goal rejected :(')
        return
    self._get_result_future = goal_handle.get_result_async()
    self._get_result_future.add_done_callback(self.get_result_callback)
```

취소와 거부에는 더 완전한 서버 형태가 필요하다. `goal_callback`(수락/거부), `cancel_callback`(취소 수락/거부), `handle_accepted_callback`을 받고, 실행 루프 안에서 `goal_handle.is_cancel_requested`를 검사해 `goal_handle.canceled()`를 부른다.

C++ 쪽이 교훈적이다. `rclcpp_action::create_server`는 그 세 콜백을 명시적으로 받고, 수락된 목표 콜백은 즉시 반환해야 하므로 튜토리얼은 작업을 별도 스레드로 던진다.

```cpp
auto handle_accepted = [this](const std::shared_ptr<GoalHandleFibonacci> goal_handle)
{
  // this needs to return quickly to avoid blocking the executor,
  // so we declare a lambda function to be called inside a new thread
  auto execute_in_thread = [this, goal_handle](){return this->execute(goal_handle);};
  std::thread{execute_in_thread}.detach();
};
```

저 주석은 라이브러리를 쓴 사람들이 3절을 다시 말한 것이다. Python의 간단한 `ActionServer` 형태는 같은 위험을 감춘다. 단일 스레드 executor에서 긴 `execute_callback`은 그 노드의 나머지 전부를 막는다. `rclpy` 예제가 완전한 액션 서버에 `MultiThreadedExecutor`와 `ReentrantCallbackGroup`을 짝지어 두는 이유다.

### 6. 파라미터: 노드 설정하기

*네 패턴 중 셋째 — 파라미터, 6–7절.*

파라미터는 노드의 설정값이고, 그 노드가 소유하며, 정확히 그 노드만큼 산다. 각각은 키, 값, **디스크립터**(설명, 허용 범위, 읽기 전용 여부 같은 파라미터 메타데이터)로 이루어진다. 값의 타입은 아홉 가지뿐이다. `bool`, `int64`, `float64`, `string`, `byte[]`, `bool[]`, `int64[]`, `float64[]`, `string[]`. 사전도 중첩 구조체도 없다. `some_lists.some_integers`는 점이 들어간 *이름*이지 중첩이 아니다.

노드는 받아들일 모든 파라미터를 **선언(declare)** 해야 한다. 그래야 이름과 타입이 반년 뒤 오타로 발견되지 않고 기동 시점에 고정된다.

```python
class MinimalParam(Node):
    def __init__(self):
        super().__init__('minimal_param_node')
        self.declare_parameter('my_parameter', 'world')
        self.timer = self.create_timer(1, self.timer_callback)

    def timer_callback(self):
        my_param = self.get_parameter('my_parameter').get_parameter_value().string_value
        self.get_logger().info('Hello %s!' % my_param)
```

타입은 기본값에서 추론되고, 선언된 파라미터의 타입을 런타임에 바꾸려는 시도는 기본적으로 **실패한다.** 불리언을 정수에 넣는 실수가 흡수되지 않고 잡힌다. (정말로 다형적 파라미터가 필요하면 `dynamic_typing`이 참인 디스크립터로 선언하고, 이름을 미리 알 수 없는 노드는 `allow_undeclared_parameters`로 생성한다.)

디스크립터는 설명, 범위, 그 밖의 제약을 담고, **읽기 전용**이 사는 곳이다.

```python
from rcl_interfaces.msg import ParameterDescriptor
my_parameter_descriptor = ParameterDescriptor(description='This parameter is mine!')
self.declare_parameter('my_parameter', 'world', my_parameter_descriptor)
```

C++은 같은 생각에 타입이 더 붙는다.

```cpp
auto param_desc = rcl_interfaces::msg::ParameterDescriptor{};
param_desc.description = "This parameter is mine!";
this->declare_parameter("my_parameter", "world", param_desc);
// 나중에: std::string p = this->get_parameter("my_parameter").as_string();
```

읽기 전용 파라미터는 기동 시에만 설정할 수 있고 그 뒤에는 안 된다. 의도하지 않아도 만나게 된다. 모든 C++(rclcpp) 노드가 자동으로 선언하는 `qos_overrides./parameter_events.*` 파라미터가 읽기 전용이고(rclpy 노드는 선언하지 않는다), 그래서 `ros2 param load`가 그것들에 대해 실패를 찍고 나머지는 성공한다. 버그가 아니며 문서에 그렇게 적혀 있다.

폴링 대신 변경에 반응하려면, 제안된 변경을 검사하고 거부할 수 있는 **set-parameters 콜백**(`add_on_set_parameters_callback`), 변경을 수정할 수 있는 **pre-set** 콜백, 변경이 수락된 *뒤에* 도는 **post-set** 콜백을 등록할 수 있다. set 콜백에는 부작용이 없어야 한다. 여러 개가 사슬로 이어질 수 있고, 개별 콜백은 뒤의 콜백이 갱신을 거부할지 알 수 없다. 반응은 post-set 콜백에서 하라.

### 7. 파일과 커맨드라인으로 파라미터 설정하기

세 가지 경로, 모두 소스 코드 바깥이다.

기동 시 커맨드라인에서 `--ros-args -p 이름:=값`으로:

```bash
ros2 run demo_nodes_cpp parameter_blackboard --ros-args -p some_int:=42 -p "a_string:=Hello world" -p "some_lists.some_integers:=[1, 2, 3, 4]"
```

기동 시 YAML 파일로. YAML은 ROS 2가 파라미터 파일(그리고 25.4의 launch 파일 세 형식 중 하나)에 쓰는 평문 형식이다. 들여쓰기가 키 아래에 키를 중첩하고, `[1, 2, 3]`은 리스트이며, 따옴표 없는 값은 철자로 타입이 정해진다 — `42`는 정수, `0.005`는 실수, `true`나 `false`는 불리언, 그 밖의 낱말은 대개 문자열. 따옴표를 치면 무엇이든 문자열이다. 파일은 노드 이름, 그다음 리터럴 키 `ros__parameters`(밑줄 두 개)로 키를 잡는다.

```yaml
parameter_blackboard:
    ros__parameters:
        some_int: 42
        a_string: "Hello world"
        some_lists:
            some_integers: [1, 2, 3, 4]

/**:
  ros__parameters:
    wildcard_full: "Full wildcard for any namespaces and any node names"
```

```bash
ros2 run <package_name> <executable_name> --ros-args --params-file <file_name>
```

`*`는 슬래시로 구분된 토큰 하나에, `**`는 0개 이상의 토큰에 대응한다. 그래서 실제 런치 파일은 하위 시스템 전체에 설정 하나를 주려고 `/**`를 쓴다. `foo*` 같은 부분 일치는 허용되지 않는다. 그리고 사람들이 걸리는 비대칭: **기동 시에 쓰는 파라미터 파일은 읽기 전용 파라미터를 포함해 모든 파라미터를 갱신한다.** 나중에 `ros2 param load`로는 못 하는 일이다.

런타임에는 모든 노드가 자동으로 만드는 파라미터 서비스를 통해:

```bash
ros2 param list /minimal_param_node
ros2 param describe /minimal_param_node my_parameter
ros2 param get /minimal_param_node my_parameter
ros2 param set /turtlesim background_r 150
ros2 param dump /turtlesim > turtlesim.yaml
ros2 param load /turtlesim turtlesim.yaml
```

`ros2 param set`의 함정 둘. 값은 YAML로 파싱되고, 그것이 따르는 YAML 1.1 규칙은 `on`, `off`, `yes`, `no`도 불리언으로 읽는다. 그래서 `off`는 불리언이 되고 문자열 파라미터에는 거부된다. `'!!str off'`라고 써라. `!!str`은 "이 값은 문자열"이라고 못 박는 YAML의 명시적 태그다. 그리고 ROS 2에는 이종(heterogeneous) 리스트가 없어서, 타입이 섞인 YAML 리스트는 문자열로 해석된다. `ros2 param dump`를 파일로 보내는 것은 재현할 실행의 설정을 기록하는 가장 빠르고 정직한 방법이다.

### 8. 관리형(라이프사이클) 노드

*네 패턴 중 넷째 — 라이프사이클, 8절. 상태는 8.1절, P6 숫자는 8.2절, Nav2는 8.3절.*

보통 노드는 생성되는 순간부터 제 일을 시작한다. 레이저, 카메라, 모터 드라이버에는 그것이 틀렸다. 장치는 부팅에 몇 초가 걸리고, 예열 중에 헛소리를 발행하거나 시스템의 나머지가 준비되기 전에 하드웨어를 여는 노드는 센서 고장처럼 보이는 실패를 만든다.

#### 8.1 상태, 전이, 그리고 그 콜백

**관리형 노드**(`LifecycleNode`)는 상태 기계를 더한다. 네 개의 안정적인 **주 상태** — `unconfigured`, `inactive`, `active`, `finalized` — 와, 전이 성공 여부를 알리는 **전이 상태**(`configuring`, `activating`, `deactivating`, `cleaningup`, `shuttingdown`, `errorprocessing`). 호출하는 전이는 `configure`, `activate`, `deactivate`, `cleanup`, `shutdown`이다.

전이마다 재정의할 콜백이 돈다. `on_configure`(할당, 장치 열기, 퍼블리셔와 타이머 생성), `on_activate`(발행 시작), `on_deactivate`(중지), `on_cleanup`(해제), `on_shutdown`. 전부 기본 반환이 성공이라, 아무것도 재정의하지 않아도 관리형 노드가 된다.

`on_error`는 실패한 전이의 뒤처리다. 이 콜백은 전이 콜백이 ERROR를 반환하거나 예외를 던질 때 `errorprocessing` 상태에서 호출된다. SUCCESS를 반환하면 — rclcpp와 rclpy 모두 기본값 — 노드는 `unconfigured`로 돌아가고, FAILURE를 반환하면 `finalized`로 간다.

문서 함정 하나: demos README는 아직 기본값이 실패라고 적지만, 소스는 그렇지 않다.

이득은 발행이 상태로 게이팅된다는 것이다. `on_configure`에서 만든 라이프사이클 퍼블리셔는 `inactive`에 존재하지만 아무것도 전달하지 않는다. 노드가 `active`가 되기 전까지 `publish()`는 아무 일도 하지 않는다. 하류의 누구도 반쯤 초기화된 데이터를 보지 않는다.

모든 관리형 노드는 여섯 가지 인터페이스를 공짜로 노출한다. `<node_name>/transition_event` 토픽, 그리고 `get_state`, `change_state`, `get_available_states`, `get_available_transitions`, `get_transition_graph` 서비스. CLI가 그것을 감싼다.

```bash
ros2 lifecycle nodes
ros2 lifecycle list /lc_talker
ros2 lifecycle get /lc_talker
ros2 lifecycle set /lc_talker configure
ros2 lifecycle set /lc_talker activate
```

돌려 볼 데모는 `ros2 launch lifecycle lifecycle_demo_launch.py`, 또는 터미널 셋에 `lifecycle_talker`, `lifecycle_listener`, `lifecycle_service_client`. talker는 처음에 아무것도 찍지 않는다. 설계대로 `unconfigured`로 시작하기 때문이다.

Python에서는 `rclpy.lifecycle.Node`(`LifecycleNode`의 별칭)를 상속하고, `on_configure` 등을 재정의해 `TransitionCallbackReturn.SUCCESS`를 반환하고, 퍼블리셔를 `create_lifecycle_publisher`로 만든다. C++에서는 `rclcpp_lifecycle::LifecycleNode`를 상속하고 콜백은 `LifecycleNodeInterface::CallbackReturn`을 반환한다.

#### 8.2 P6 숫자로 보는 라이프사이클

P6의 카메라를 관리형 노드로 만들고, 센서가 전원을 켠 뒤 첫 유효 프레임까지 $T_{\text{warm}}=1.5\,\mathrm{s}$가 걸린다고 하자. P6 카탈로그는 주기만 정하므로 가정한 값이다. 생성 직후부터 발행하는 평범한 노드로 띄우면 카메라는 센서가 무엇을 돌려주든 $20\,\mathrm{ms}$마다 목표를 내고, 제어기는 $5\,\mathrm{ms}$마다 가장 새 목표대로 움직이므로 워밍업의 대가는

$$n_{\text{goal}}=T_{\text{warm}}\,f_{\text{vision}}=1.5\times50=75,\qquad n_{\text{tick}}=T_{\text{warm}}\,f_{\text{ctrl}}=1.5\times200=300$$

이다. 무효 목표 75개가 발행되고, 제어 틱 300번이 카트를 그쪽으로 모는 데 쓰인다. 관리형 노드라면 같은 카메라가 `on_configure` 안에서 장치를 열고 첫 유효 프레임을 기다렸다가 그때에야 SUCCESS를 반환하고, 관리자는 그 뒤에 `activate`를 부르며, 라이프사이클 퍼블리셔는 `activate` 전의 `publish()`를 모두 버린다. 두 수 모두 $0$이다. 대신 제어기는 평범한 노드가 숨기던 상태, *아직 목표 없음*을 만나고, 첫 목표가 올 때까지 카트를 세워 두어야 한다. 라이프사이클이 사 준 것은 그 명시적인 상태다.

두 번째 숫자는 과제가 묻는 경우, 활성화 뒤에 카메라가 죽는 경우다. 제어기의 목표 저장소는 마지막 목표를 쥐고 있고 틱마다 그것을 재사용하므로, 쓰이는 목표는 틱마다 $T_{\text{ctrl}}=5\,\mathrm{ms}$씩 늙어 $70/5=14$틱 안에 예산 전체보다 오래된다. 카메라와 bond를 맺은 라이프사이클 관리자는 bond가 시간 초과될 때에야 알아채고, Nav2의 기본 `bond_timeout` $4.0\,\mathrm{s}$(8.3절)라면 그것은

$$\frac{4.0\,\mathrm{s}}{T_{\text{ctrl}}}=\frac{4.0}{0.005}=800\ \text{틱},\qquad \frac{4000\,\mathrm{ms}}{70\,\mathrm{ms}}\approx57\ \text{예산}$$

이고, 그 무렵 목표는 4초 가까이 묵어 있다. 그러니 라이프사이클은 스택을 깔끔하게 내려 주지만 $70\,\mathrm{ms}$ 예산의 파수꾼은 아니다. 그 파수꾼은 `on_tick` 안의 비교 한 줄 — 목표의 스탬프를 노드의 시계와 견주어, 차이가 $70\,\mathrm{ms}$를 넘으면 카트를 세우는 것 — 이고, bond는 나머지 시스템이 그 사실을 알게 되는 경로다.

#### 8.3 만나게 될 곳: Nav2

학술적인 이야기가 아니다. **Nav2가 이 위에 세워져 있고**, [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]에서 만나게 된다. `map_server`, `planner_server`, `controller_server`가 라이프사이클 노드이고, `nav2_lifecycle_manager`가 자기 `<manager_name>/manage_nodes` 서비스(예: `lifecycle_manager_navigation/manage_nodes`)를 통해 기동 시 순서 지어진 그룹으로 `configure`와 `activate`를, 종료 시에는 역순으로 몰아간다. 또 각 서버와 **bond**(관리자와 서버가 주기적으로 주고받는 heartbeat)를 유지해서, 활성화 뒤에 죽은 노드를 알아채고 반쯤 돌아가는 상태로 두는 대신 스택 전체를 내린다. `bond_timeout`(기본 4.0초)이 판단까지 기다리는 시간이다. Nav2가 기동 후 "아무것도 안 할" 때 첫 질문은 서버들이 어느 상태인가이고, `ros2 lifecycle get`이 한 줄로 답한다.

### 9. 실습: 피드백을 보고하는 액션 서버

한 번에 앉아서. 25.2의 `ros2_ws`에서 작업한다. 워크스페이스 빌드와 source가 낯설면 [[04-robotics/ros2/workspaces-packages-launch|25.4 워크스페이스, 패키지, 빌드, 런치]]를 보라.

1. 인터페이스 패키지와 액션을 만든다.

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_cmake --license Apache-2.0 custom_action_interfaces
mkdir custom_action_interfaces/action
```

4절의 3부 정의를 `action/Fibonacci.action`에 넣고, `CMakeLists.txt`의 `ament_package()` 앞에 `find_package(rosidl_default_generators REQUIRED)`와 `rosidl_generate_interfaces` 블록을 추가하고, `package.xml`에 `<buildtool_depend>rosidl_default_generators</buildtool_depend>`와 `<member_of_group>rosidl_interface_packages</member_of_group>`를 추가한 뒤, `~/ros2_ws`에서 `colcon build`하고 `source install/local_setup.bash`.

2. 코드를 쓰기 전에 계약이 존재하는지 확인한다.

```bash
ros2 interface show custom_action_interfaces/action/Fibonacci
```

3. 5절의 서버를 `fibonacci_action_server.py`로 저장하고 `python3 fibonacci_action_server.py`로 실행한다.

4. 두 번째 터미널에서 피드백 *없이* 목표를 보내고, 그다음 피드백과 함께 보낸다.

```bash
ros2 action send_goal fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
ros2 action send_goal --feedback fibonacci custom_action_interfaces/action/Fibonacci "{order: 5}"
```

첫 번째는 목표 ID를 찍고, 약 4초간 조용히 기다리다가, 결과와 `SUCCEEDED`를 찍는다. 루프가 `range(1, order)`라서 `order: 5`면 1초짜리 반복이 네 번이다. 두 번째는 반복마다 `Feedback:` 블록을 하나씩, 그러니까 넷을 찍는다. 그 차이가 액션을 쓰는 논거 자체다. 계산은 같은데, 호출자가 이제 그 안을 볼 수 있다.

5. 세 번째 터미널에서 목표가 도는 동안 그래프를 본다. `ros2 action list -t`, 그다음 `ros2 action info /fibonacci`.

6. `order`를 30으로 올리고 목표 중간에 클라이언트에서 Ctrl+C를 누른다. CLI는 취소 요청을 보내지만(`Canceling goal...`), 이 서버는 `execute_callback`이 유일한 스레드를 막고 있어 처리할 수 없고, 기본 취소 콜백은 어차피 거부한다 — 그래서 클라이언트는 목표가 끝날 때까지 기다린 뒤 `Failed to cancel goal`을 보고한다. 취소는 *서버가* 처리해야 하는 요청이지 클라이언트가 강제할 수 있는 것이 아니다. 5절의 완전한 서버 형태가 존재하는 이유다.

`.action` 파일의 세 부분이 각각 무엇을 하는지, 그리고 `--feedback`이 서버 쪽에서는 왜 아무것도 바꾸지 않는지 말할 수 있으면 끝난 것이다.

### 10. 진단할 실패: 콜백 안에서 한 서비스 호출

트리거 토픽을 구독하다가 메시지마다 서비스를 호출하는 노드가 있다. Python에서 읽기 좋다는 이유로 동기 `call()`을 쓴다. 첫 메시지가 도착하고 노드가 멈춘다. 영원히.

증상이 최악의 종류다. **오류가 없다.** 공식 문서가 그대로 적어 두었다. 경고도, 예외도, 스택 트레이스에 남는 것도 없고, 호출이 실패하지도 않는다. 프로세스는 살아 있고, 노드는 그래프에 있고, 아무 일도 일어나지 않는다.

```python
def trigger_request(msg):
    response = minimal_client.cli.call(minimal_client.req)  # synchronous call inside a callback: deadlock
```

기전은 이렇다. `call()`은 응답이 올 때까지 스레드를 막는데, 응답을 전달할 수 있는 것은 *바로 그 스레드* 위에서 도는 executor뿐이고, 그 스레드는 지금 당신의 콜백 안에 있다. executor는 실행 중인 콜백을 선점하지 못한다. 클라이언트는 기다리는 자만이 전달할 수 있는 응답을 기다린다.

무엇이 찾아내는가:

```bash
ros2 node list                  # 노드는 있다
ros2 node info /your_node       # 구독과 서비스 클라이언트가 다 보인다
ros2 topic hz /its_output       # 아무것도 없음 — 메시지가 오지 않는다
ros2 service list | grep add_two_ints   # 서버는 멀쩡히 있다
```

그래프에 살아 있고, 아무것도 생산하지 않고, 반대편 서버는 건강하다. 이 조합이 서명이다. 역시 조용한 QoS 불일치와 구별하려면 트리거가 오기 *전에* 노드가 출력을 냈는지 보라. 데드락 난 노드는 첫 트리거까지는 동작했고, 불일치 난 노드는 처음부터 한 번도 동작하지 않았다.

고치는 방법 셋, 선호 순서대로. `call_async`를 쓰고 future를 콜백에서 처리한다. 어디서 불러도 안전하다. 호출을 동기로 두되 *클라이언트*를 호출하는 콜백과 다른 **콜백 그룹**에 넣고(또는 재진입 그룹을 쓰고) 다중 스레드 executor를 돌린다. 정 필요하면 문서화된 패턴을 따른다. 별도 스레드에서 spin하고 `main`에서 호출하되, 콜백에서는 절대 부르지 않는다. 셋 모두의 바탕인 executor와 콜백 그룹 기계는 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]에 있다. C++도 예외가 아니다. 콜백 안에서 `async_send_request`의 future를 기다리면 똑같이 교착되고, 공식 콜백 그룹 안내서가 바로 그것을 예로 든다.

### 11. 이 페이지가 다루지 않는 것

커스텀 `.srv`와 `.action` 패키지는 여기서 하나를 빌드할 만큼만 보였다. 일반적인 인터페이스 정의 규칙과 패키지가 그것을 선언하는 방법은 [[04-robotics/ros2/workspaces-packages-launch|25.4 워크스페이스, 패키지, 빌드, 런치]]의 몫이고, 터미널 여섯 개 대신 파라미터를 붙인 런치 파일로 이 전부를 띄우는 법도 거기에 있다. Executor, 콜백 그룹, 그리고 애초에 서비스와 액션이 연결되게 만드는 QoS 설정은 [[04-robotics/ros2/executors-callbacks-time|25.5.1 Executor, 콜백 그룹, 시간]]와 [[04-robotics/ros2/qos-executors-time|25.5 서비스 품질(QoS)]]. 시스템 인터페이스로서의 액션 — 행동 트리가 액션을 부르고, 라이프사이클 관리자가 서버들을 순서 짓는 모습 — 은 [[04-robotics/ros2/navigation-nav2|25.9 Nav2로 하는 내비게이션]]에서 나온다. 트랙 전체는 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- ROS 2 Jazzy 문서 — Concepts: Services; Actions; Parameters.
- ROS 2 Jazzy 문서 — Tutorials: Understanding services; Understanding parameters; Understanding actions; Writing a simple service and client (Python, C++); Creating an action; Writing an action server and client (Python, C++); Using parameters in a class (Python, C++); Managing node lifecycles.
- ROS 2 Jazzy 문서 — How-to guides: Synchronous vs. asynchronous service clients; `ros2 param` 커맨드라인 도구 사용; 커맨드라인으로 노드에 ROS 인자 넘기기.
- ros2/demos — `lifecycle` 패키지 README(주 상태와 전이 상태, 전이 콜백, 라이프사이클 인터페이스 — README는 다섯이라 하지만 소스는 여섯을 만든다); `lifecycle_py/lifecycle_py/talker.py`.
- ros2/examples — `rclpy/actions/minimal_action_server`(goal, cancel, accepted 콜백).
- ros2/ros2cli — `ros2lifecycle` 동사(`nodes`, `list`, `get`, `set`).
- ros-navigation/navigation2 — `nav2_lifecycle_manager` README와 `lifecycle_manager.cpp`(순서 지어진 기동, `manage_nodes` 서비스, `bond_timeout` 기본값).

### 스스로 점검

1. 요청을 받아 30초짜리 전역 계획을 도는 노드가 필요하다. 서비스인가 액션인가, 왜인가?
2. `ros2 param load /my_node params.yaml`이 일부는 "successful", 일부는 "cannot be set
   because it is read-only"를 찍는다. 뭔가 고장 났나?
3. 직접 쓴 노드가 `ros2 node list`에 있고, `ros2 node info`에 서비스 클라이언트와 구독이 다
   보이고, 호출하는 서버도 돌고 있는데, 첫 입력 이후 아무것도 내보내지 않는다. 첫 가설은?
4. Nav2는 왜 보통 노드 대신 라이프사이클 노드를 쓰는가?
5. P6 제어기 노드의 서비스 핸들러가 단일 스레드 executor에서 $20\,\mathrm{ms}$ 걸린다.
   $200\,\mathrm{Hz}$ 발화를 몇 번 잃고, 모터는 무엇을 하며, P6의 $70\,\mathrm{ms}$
   예산에 견주면 얼마인가?

> [!tip]- 정답 · Answers
> 1. 액션이다. 서비스는 호출자를 막고 선점할 수 없으며, 단일 스레드 executor에서 30초짜리 서비스 콜백은 그 노드의 다른 모든 콜백 — 타이머, 구독, 다른 서비스 — 도 함께 멈춘다. 공식 지침은 서비스가 빨리 반환해야 하고 장시간 작업은 액션의 몫이라는 것이다. 액션은 덤으로 피드백과 취소 경로를 준다.
> 2. 아니다. 읽기 전용 파라미터는 기동 시에만 설정된다. 모든 C++ 노드가 읽기 전용 `qos_overrides./parameter_events.*`를 선언하므로, rclcpp 노드에서 dump 후 load를 왕복하면 그 실패가 찍힌다. 꼭 적용해야 하면 같은 파일을 기동 시 `--ros-args --params-file`로 넘겨라. 그쪽은 읽기 전용 파라미터도 갱신한다.
> 3. 콜백 안에서 한 동기 서비스 호출. executor가 실행 중인 콜백을 선점해 응답을 전달할 수 없어서 호출이 영원히 기다린다. 예외도, 경고도, 실패도 없다. 첫 트리거 이전에는 출력이 있었는지 확인해 확증하고, `call_async`나 별도 콜백 그룹 + 다중 스레드 executor로 고친다.
> 4. 기동 순서가 중요하고 부분 기동이 위험하기 때문이다. 라이프사이클 관리자가 서버들을 순서 지어진 그룹으로 `configure`와 `activate`를 거치게(종료 시에는 역순으로) 하므로, 자원이 생기기 전에는 무엇도 발행하거나 목표를 받지 않는다. 그다음 각 서버와 bond를 유지해서, 활성화 이후의 충돌이 스택을 반쯤 살아 있는 상태로 남기지 않고 결정론적으로 내리게 한다. "Nav2가 왜 아무것도 안 하지"에 대한 한 줄 답은 `ros2 lifecycle get <node>`다.
> 5. 넷이다. executor가 핸들러 안에 있는 동안에는 타이머가 돌 수 없으므로 $\lfloor 20/5\rfloor=4$번의 발화를 잃는다. 단일 스레드 executor는 콜백 하나를 끝까지 돌린 다음에야 다음 것을 집기 때문이다. 모터는 $5$가 아니라 $20\,\mathrm{ms}$ 동안 마지막 명령을 붙들고, $20\,\mathrm{ms}$는 $70\,\mathrm{ms}$ 예산의 $28.6\%$다. 요청 하나가 루프를 영구히 $50\,\mathrm{Hz}$로 떨어뜨리는 것과 같은 값을 문 셈이다. 그 핸들러가 타이머 콜백 안에서 동기 서비스 호출을 한다면 소요는 $20\,\mathrm{ms}$가 아니라 무한이고, 그것이 10절이다.

### 과제 · Problem set

Tier B. [[02-foundations/lab-plants|0.6]]의 **P6**. 제어 루프는 $200\,\mathrm{Hz}$. 계획기는 다음 목표를 만드는 데 $2\,\mathrm{s}$가 걸릴 수 있다. 시뮬레이터를 새로 만들지 마라.

1. **그리기.** P6 노드: `planner`(긴 목표), `controller`($5\,\mathrm{ms}$ 타이머 + 엔코더), `camera`($50\,\mathrm{Hz}$). 계획기–제어기 링크는 토픽이나 서비스가 아니라 *액션*. 다섯 줄 타임라인: 목표 전송, $0.5\,\mathrm{s}$ 피드백, $2\,\mathrm{s}$ 결과, 그동안의 제어 틱.
2. **유도.** (a) $2\,\mathrm{s}$ *서비스* 콜백이 막는 제어 샘플 수. (b) 엔코더 한 카운트의 $\Delta p$. (c) 조용한 고장: 제어기가 $200\,\mathrm{Hz}$ 타이머 안에서 `calling`을 로그로 찍은 뒤 `client.call`로 계획기를 부른다. 첫 틱부터 로그에는 무엇이 보이고, 왜 에러가 없는가?
3. **해석.** P6 목표가 액션인 이유, 그리고 제어기가 이미 $200\,\mathrm{Hz}$인데 카메라 드라이버가 죽으면 라이프사이클이 사 주는 것은?

> [!note]- 그리는 법 · How to draw it
> - 간선의 종류마다 펜 자국이 따로 있고, 어느 둘도 닮아 보이면 안 된다. 이 페이지 전체가 그 구분이다.
> - 토픽은 열린 화살표 하나. `/goal`, $50\,\mathrm{Hz}$, `/camera` → `/controller`.
> - 서비스는 양방향 짧은 화살표 한 쌍을 바짝 붙여 그린다. 요청 하나, 응답 하나, 그 사이에는 아무것도 없다.
> - 액션은 화살표 세 종류가 있는 레인이다. 목표가 내려가고, 레인을 따라 피드백이 여러 번 올라오고, 끝에서 결과가 한 번 올라온다. 양 끝이 `/planner`와 `/controller`다.
> - 파라미터는 간선이 아니다. `/controller`에 매달린 작은 표(이름, 타입, 값, 그렇게 선언했다면 read-only)로 그리고, 화살표로는 그리지 않는다.
> - 타임라인에서 제어기의 $5\,\mathrm{ms}$ 틱은 목표부터 결과까지 액션 내내 끊김 없이 이어진다.
> - 틱 하나가 `client.call`을 쥔 뒤로 아무것도 없는 시계 — 틱도, 로그도, 오류도 없고 서버는 곧바로 응답한 — 는 액션이 아니라 10절의 고장이다.

> [!tip]- 정답 · Solutions
> 1. 계획기에서 제어기로 액션 `navigate`; 카메라 `/goal`은 별 스트림. 타임라인: $t=0$ 목표; $5\,\mathrm{ms}$마다 틱; 피드백; $2\,\mathrm{s}$에 결과.
> 2. (a) $2/0.005=400$ 샘플. (b) $0.488\,\mathrm{mm}$. (c) 타이머가 executor를 붙들고 응답 콜백이 못 돈다. `calling` 한 줄 후 침묵. 예외 없음.
> 3. $2\,\mathrm{s}$는 "빨리 반환"이 아니다. 액션은 $200\,\mathrm{Hz}$ 루프를 살려 두고 취소할 수 있다. 라이프사이클 + bond는 카메라가 죽으면 스택을 내리지, 제어기가 낡은 $70\,\mathrm{ms}$ 예산을 추적하게 두지 않는다. 다만 bond가 시간 초과된 뒤에야 그렇고, Nav2 기본값이면 $4.0/0.005=800$틱 뒤다. 예산 자체의 파수꾼은 `on_tick` 안의 스탬프 검사다(8.2절).
