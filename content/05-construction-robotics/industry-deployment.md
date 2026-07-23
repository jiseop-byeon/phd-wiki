---
title: 8. Industry & Deployment Map
tags: [construction, industry, deployment]
---

## English

This page tracks **what is operationally sold or deployed**, not which demo looks most
autonomous. Company status changes quickly; entries are a verification snapshot
(2026-07), not investment advice or a permanent ranking.

### 1. Deployment archetypes

| Archetype | Examples | Typical human role | Main evidence to seek |
|---|---|---|---|
| OEM-integrated autonomy | Caterpillar Command, Komatsu/EarthBrain, Kajima A4CSEL | fleet supervision, exception handling | operating hours, fleet size, intervention rate |
| Retrofit autonomy | Gravis RACK, Built Robotics, Bedrock | setup, geofence, remote supervision/recovery | supported machines/tasks, installation and support burden |
| Teleoperation/assistance | Cat Command stations, haptic/shared-control systems | continuous or exception-based operator | latency, staffing ratio, productivity and safety |
| Task-specific robot | Canvas drywall, robotic layout/welding/bricklaying systems | material feeding, setup, finishing | complete workflow labor and throughput |
| Data/workflow platform | Smart Construction, Reconstruct | model setup and decisions remain human | whether data changes machine action or only reporting |

### 2. Research-to-industry lineages

- **CMU RI/NREC → Caterpillar**: autonomous excavation and off-road robotics became OEM
  mining autonomy; a long systems-integration lineage rather than a new AI wave.
- **ETH RSL/GKR → Gravis Robotics**: HEAP sensing/control and field deployment knowledge
  moved into retrofit autonomy and assistance.
- **UIUC D4AR → Reconstruct**: vision/BIM progress monitoring commercialized as a site
  intelligence workflow rather than a robot controller.
- **Architectural fabrication institutes → specialized production companies**: research
  prototypes often commercialize as process/design expertise before general robots.

### 3. How to read commercial claims

“Autonomous” may mean one task inside a geofence with remote operators; “deployed” may
mean a paid pilot; “AI-powered” may describe perception while motion is scripted. Ask:

1. Who specifies and validates the task?
2. How many machines, sites, customers, and continuous operating hours?
3. How many remote operators per machine and interventions per hour?
4. Who performs setup, calibration, material handling, maintenance, and recovery?
5. Is productivity compared with the complete incumbent workflow?
6. What changed after acquisition—product, team, or only ownership?

> [!warning] Evidence hierarchy
> A peer-reviewed system paper, regulator/OEM documentation, and named customer deployment
> support different claims from a funding announcement or promotional video. Preserve the
> date and source of every company-status statement.

### 4. Why commercialization does not rank research

A commercially robust system may use conservative classical methods and solve a narrow
workflow extremely well. A research paper may introduce a general learning method but
run only in simulation. These are different axes: **method novelty, system completeness,
deployment evidence, and economic value** should not be collapsed into one score.

### After reading

- Classify a product as OEM autonomy, retrofit, teleoperation, task robot, or workflow platform.
- State the hidden human labor behind an autonomy claim.
- Separate method novelty from system and commercial evidence.
- Trace at least three research-to-industry lineages in this field.

### Primary starting points

- [Caterpillar MineStar Command](https://www.cat.com/en_US/by-industry/mining/surface-mining/surface-technology/command.html)
- [Komatsu Smart Construction](https://www.komatsu.com/en/innovation/smart-construction/)
- [Gravis Robotics](https://www.gravisrobotics.com/)
- [Reconstruct](https://www.reconstructinc.com/)

## 한국어

이 페이지는 데모의 인상이 아니라 **실제로 무엇이 판매·배치되는가**를 추적한다. 기업 상태는
빠르게 변하므로 2026-07 검증 스냅샷이며 영구 순위나 투자 조언이 아니다.

### 1. 배치 유형

| 유형 | 예 | 보통의 인간 역할 | 확인할 증거 |
|---|---|---|---|
| OEM 통합 자율성 | Caterpillar Command, Komatsu/EarthBrain, Kajima A4CSEL | 선단 감독·예외 처리 | 운용 시간·선단 규모·개입률 |
| Retrofit 자율성 | Gravis RACK, Built Robotics, Bedrock | 설정·geofence·원격 감독/복구 | 지원 장비·과제, 설치·지원 부담 |
| 원격조작/보조 | Cat Command station, 햅틱·공유제어 | 지속 또는 예외 기반 운전자 | 지연, 운전자:기계 비율, 생산성·안전 |
| 과제 전용 로봇 | Canvas drywall, 레이아웃·용접·조적 | 재료 공급·준비·마감 | 전체 공정 노동과 처리량 |
| 데이터·공정 플랫폼 | Smart Construction, Reconstruct | 모델 설정·판단은 인간 | 데이터가 행동을 바꾸는지 보고만 하는지 |

### 2. 연구에서 산업으로

- **CMU RI/NREC → Caterpillar**: 자율 굴착·오프로드 로보틱스가 OEM 광산 자율화로.
- **ETH RSL/GKR → Gravis**: HEAP의 센싱·제어·필드 배치 지식이 retrofit으로.
- **UIUC D4AR → Reconstruct**: 비전+BIM 공정 모니터링이 로봇 제어가 아닌 현장 정보 공정으로.
- **건축 패브리케이션 연구소 → 전문 생산 기업**: 범용 로봇보다 공정·설계 전문성이 먼저 상품화된다.

### 3. 상업 주장 읽기

“자율”은 원격 감독이 있는 geofence 안의 한 과제일 수 있고, “배치”는 유료 pilot일 수 있으며,
“AI-powered”는 인식만 AI이고 움직임은 script일 수 있다. 과제 지정·검증 주체, 기계·현장·고객·
연속 운용 시간, 원격 운전자 비율과 개입률, 준비·보정·재료·유지·복구 노동, 전체 기존 공정과의
생산성 비교를 확인하라.

> [!warning] 증거 위계
> 동료평가 시스템 논문, 규제·OEM 문서, 실명 고객 배치는 투자 발표·홍보 영상과 다른 주장을
> 지지한다. 기업 상태 문장에는 날짜와 출처를 보존하라.

### 4. 상업화가 연구 순위는 아니다

상용 시스템은 보수적 고전 방법으로 좁은 공정을 매우 잘 풀 수 있고, 연구 논문은 일반 학습
방법을 제안하지만 시뮬레이션만 돌 수 있다. **방법 신규성, 시스템 완결성, 배치 증거, 경제성**은
서로 다른 축이다.

### 읽고 나면 말할 수 있어야 하는 것

- 제품을 OEM 자율성·retrofit·원격조작·과제 로봇·공정 플랫폼으로 분류한다.
- 자율성 주장 뒤의 인간 노동을 찾는다.
- 방법 신규성과 시스템·상업 증거를 구분한다.
- 세 개 이상의 연구→산업 계보를 설명한다.

### 1차 확인 출발점

- [Caterpillar MineStar Command](https://www.cat.com/en_US/by-industry/mining/surface-mining/surface-technology/command.html)
- [Komatsu Smart Construction](https://www.komatsu.com/en/innovation/smart-construction/)
- [Gravis Robotics](https://www.gravisrobotics.com/)
- [Reconstruct](https://www.reconstructinc.com/)
