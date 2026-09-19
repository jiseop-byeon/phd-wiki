---
title: 2.5 Site Robotics as an Engineering System
tags: [construction-robotics, curriculum]
study-depth: Working
wiki-support: Working
depth-goal: "Turn one construction task into a traceable requirement, frame, uncertainty, safety, productivity, and evidence specification."
mastery-when: "Raise when the deployment workflow or field-evaluation method carries the thesis contribution."
---

> [!note] Prerequisites · 선수 지식
> [[04-robotics/robot-systems-deployment|10. Robot Systems]], [[04-robotics/hri-safety|11. HRI & Safety]], and [[06-research-practice/experimental-design-reproducibility|Experimental Design]].

## English

> [!note] First pass
> Read §§1–4 and complete the requirement ledger. Use the stream pages only after the task can be stated this precisely.

### Running project: S1 panel placement

A mobile manipulator must pick a 20 kg facade panel from a rack, move it 8 m, align two mounting holes 400 mm apart within $\pm5$ mm, hold while a worker fastens it, and clear the area. People may enter the shared site, GNSS can be blocked, and the base is repositioned between panels. This is a course object—not a proposed product—and its numbers exist to make every design claim testable.

### 1. Begin with the work package, not the robot

Write the unit of production, start and end states, tolerances, cycle-time target, predecessors, successors, and responsibility boundaries. “Install panels autonomously” hides at least five phases: acquire, transport, localize, align/hold, release/verify. Each has a different dominant failure.

| Phase | Required evidence | Dominant uncertainty | Safe fallback |
|---|---|---|---|
| acquire | stable grasp and payload margin | panel pose, suction/contact | lower and regrasp |
| transport | collision-free base motion | people, terrain, localization | controlled stop |
| align | hole residual $\le5$ mm | base/arm/frame error | retreat and rescan |
| hold/fasten | force and pose inside envelope | worker action, compliance | freeze or yield |
| verify | fastener/pose completion record | sensor observability | request inspection |

### 2. Close the frame and error budget

The tool-to-target error is not one sensor number. A first-order conservative budget can be recorded as

$$e_{\text{total}}\lesssim e_{\text{map}}+e_{\text{base}}+e_{\text{arm}}+e_{\text{tool}}+e_{\text{part}}.$$

If S1 allocates 1, 2, 1, 0.5, and 1 mm, the sum is 5.5 mm—already over tolerance. Root-sum-square would give $\sqrt{7.25}=2.69$ mm only under approximately independent zero-mean errors. The choice is an assumption to defend, not arithmetic decoration.

Every transform must name source, target, update rate, timestamp, and calibration owner. A BIM frame with no measured tie to the robot frame is not a robot command.

### 3. Safety is a system state

Separate hazard (what can cause harm), risk (severity and likelihood/exposure), safeguard, monitored variable, and safe state. An emergency stop is not the whole safety architecture: normal protective stops, speed/force limits, exclusion zones, human authority, restart conditions, and failure of the safety sensor all need ownership.

Do not infer certification from experimental success. A research paper can establish performance under stated safeguards; compliance claims require the applicable standards and an accountable assessment process.

### 4. Productivity needs a denominator

For $n$ completed units over observed time $T$, throughput is $n/T$, but deployment comparison also needs setup, calibration, supervision, resets, rework, and downtime. For S1:

$$T_{\text{effective}}=T_{\text{setup}}+\sum_i(T_{\text{cycle},i}+T_{\text{reset},i}+T_{\text{rework},i})+T_{\text{down}}.$$

If 8 panels take 160 min of cycles, 20 min setup, 15 min resets, and 5 min rework, headline cycle throughput is 3 panels/h while effective throughput is $8/200\times60=2.4$ panels/h. Both numbers are true; only the latter describes the observed work package.

### 5. Evidence ladder

Simulation tests algorithms and rare conditions; laboratory tests real sensing/contact under arranged conditions; mock-up tests scale and workflow; active site tests integration with changing work and people. A higher rung does not repair a weak protocol. At every rung define episode, success, intervention, reset, failure taxonomy, variation, and baseline.

### 6. Route into the domain

After S1 is specified, choose the matching stream: [[05-construction-robotics/earthmoving-heavy-machinery|earthmoving]], [[05-construction-robotics/assembly-fabrication|assembly]], [[05-construction-robotics/site-perception|site perception]], [[05-construction-robotics/hrc-worker-centered|HRC]], or [[05-construction-robotics/digital-twin-workflows|digital twins]]. Use [[05-construction-robotics/sim-to-real|sim-to-real]] and [[05-construction-robotics/industry-deployment|deployment]] as cross-cutting layers, not substitute topics.

### Problem set

1. **Draw.** Draw S1's phases, actors, information flows, and safe fallback from each phase.
2. **Derive.** If cycle=18 min, setup=30 min, one 12-min reset occurs every four panels, and rework is 10% at 9 min each, estimate effective time and throughput for 20 panels.
3. **Interpret.** A paper reports 95% success over 20 attempts on one indoor mock-up with manual resets. State three claims it cannot yet support.

> [!tip]- Solutions
> 1. The drawing must include worker, supervisor, robot, target/BIM, perception, controller, and stop/recovery paths—not only the nominal robot arrows.
> 2. Cycles 360 min + setup 30 + resets $5\times12=60$ + expected rework $2\times9=18$: 468 min, so $20/(468/60)=2.56$ panels/h.
> 3. Examples: active-site robustness, low-intervention autonomy, cross-site generalization, weather tolerance, or competitive productivity.

### Exit check

For a construction-robotics claim, produce a one-page ledger of work unit, tolerances, frames, uncertainty, people/authority, safety state, time denominator, intervention/reset, evidence rung, and failure taxonomy.

## 한국어

> [!note] 처음이라면
> §1–4와 요구사항 장부를 먼저 한다. 작업을 이 정밀도로 말한 뒤에만 스트림 페이지를 연다.

### 계속 쓰는 프로젝트: S1 패널 설치

모바일 매니퓰레이터가 20 kg 외장 패널을 rack에서 집어 8 m 이동하고, 400 mm 떨어진 두 mounting hole을 $\pm5$ mm 안에 맞추고, 작업자가 체결하는 동안 들고 있다가 구역을 비운다. 사람은 공유 현장에 들어오고 GNSS는 가려질 수 있으며 panel마다 base가 이동한다. 실제 제품 제안이 아니라 모든 설계 주장을 검사하기 위한 교과 대상이다.

### 1. 로봇보다 작업 package부터

생산 단위, 시작·끝 상태, 허용오차, cycle 목표, 선행·후속 공정, 책임 경계를 쓴다. panel 설치는 acquire·transport·localize·align/hold·release/verify로 나뉘며 지배적 실패가 다르다.

| 단계 | 필요한 증거 | 지배적 불확실성 | 안전 fallback |
|---|---|---|---|
| acquire | 안정 grasp와 payload 여유 | panel pose, suction/contact | 내려놓고 재파지 |
| transport | 충돌 없는 base 운동 | 사람, 지형, 위치추정 | 제어된 정지 |
| align | hole 잔차 $\le5$ mm | base/arm/frame 오차 | 후퇴 후 재스캔 |
| hold/fasten | 힘과 pose가 envelope 안 | 작업자 행동, compliance | freeze 또는 yield |
| verify | 체결/pose 완료 기록 | 센서 관측 가능성 | 검사 요청 |

### 2. Frame과 오차 budget 닫기

$e_{total}\lesssim e_{map}+e_{base}+e_{arm}+e_{tool}+e_{part}$. 각각 1, 2, 1, 0.5, 1 mm면 보수 합은 5.5 mm라 허용치를 넘는다. 독립 zero-mean을 가정한 RSS는 2.69 mm다. 어떤 합을 쓰는지는 방어할 가정이다. 모든 transform에는 source·target·rate·timestamp·calibration 책임자가 필요하다.

### 3. 안전은 시스템 상태다

hazard, risk, safeguard, monitored variable, safe state를 구분한다. emergency stop만으로 끝나지 않는다. 정상 protective stop, 속도/힘 제한, exclusion zone, human authority, restart 조건, safety sensor failure를 정해야 한다. 실험 성공은 인증이 아니다.

### 4. 생산성에는 분모가 필요하다

$T_{effective}=T_{setup}+\sum_i(T_{cycle,i}+T_{reset,i}+T_{rework,i})+T_{down}$. 8 panel의 순수 cycle 160분, setup 20분, reset 15분, rework 5분이면 headline은 3 panels/h, 실제 관측 package는 2.4 panels/h다.

### 5. 증거 사다리

simulation은 알고리즘·희귀 조건, lab은 real sensing/contact, mock-up은 scale·workflow, active site는 변화하는 공정·사람과의 통합을 검사한다. 모든 rung에서 episode·success·intervention·reset·failure taxonomy·variation·baseline을 정의한다.

### 6. 도메인 진입

S1을 명세한 뒤 earthmoving·assembly·site perception·HRC·digital twin 중 stream을 고른다. sim-to-real과 deployment는 모든 stream을 가로지르는 층이다.

### 과제

1. S1의 단계·actor·정보 흐름·단계별 safe fallback을 그린다.
2. cycle 18분, setup 30분, panel 4개마다 reset 12분, 10% rework에 9분이면 20개의 시간과 throughput을 구한다.
3. 한 실내 mock-up, 20회, 수동 reset에서 95% 성공이 지지하지 못하는 주장 세 개를 말한다.

> [!tip]- 정답
> 1. worker·supervisor·robot·target/BIM·perception·controller와 stop/recovery path가 모두 있어야 한다.
> 2. $360+30+60+18=468$분, $2.56$ panels/h.
> 3. active-site robustness, 저개입 자율성, cross-site 일반화, 날씨 내성, 경쟁 생산성 등.

### 통과 기준

건설로봇 주장 하나를 작업 단위·허용오차·frame·불확실성·사람/권한·안전 상태·시간 분모·개입/reset·증거 rung·failure taxonomy 한 장으로 명세할 수 있다.
