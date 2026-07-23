---
title: Robotic Excavation and Dry-Stone Construction Using On-Site Materials
tags: [construction, excavation, assembly]
status: note-complete
last_verified: 2026-07-23
---

**Johns et al. · Science Robotics 2023, 8(84)** — [paper](https://doi.org/10.1126/scirobotics.abp9758) · [ETH project report](https://ethz.ch/en/news-and-events/eth-news/news/2023/11/autonomous-excavator-constructs-a-six-metre-high-dry-stone-wall.html)

## English

**One-line summary:** HEAP scanned irregular on-site stones, estimated usable geometry
and mass properties, planned stable placements, and manipulated them to build a 6 m-high,
65 m-long dry-stone wall.

**Pipeline:** site/stone scanning → candidate reconstruction → structural/placement
planning → grasping and force-controlled placement → updated site model. This is a rare
closed loop joining [[05-construction-robotics/site-perception|site perception]],
[[05-construction-robotics/assembly-fabrication|assembly]], and heavy machinery.

> [!warning] Reading the claim
> The result demonstrates an integrated material-reuse workflow on one instrumented
> platform and project. It does not show unrestricted autonomous masonry, arbitrary rock
> supply, or commercial productivity against a mason.

**Impact:** The paper’s importance is system breadth: local material becomes sensed state,
planned structure, and executed contact—not merely an object-detection benchmark.

## 한국어

**한 줄:** HEAP가 현장의 불규칙 자연석을 스캔하고 형상·질량 특성을 추정해 안정적 위치를
계획한 뒤, 6 m 높이·65 m 길이의 건식 돌담으로 조작·배치했다.

현장 인식 → 구조·배치 계획 → 힘 제어 조작 → 모델 갱신의 폐루프가 핵심이다. 한 플랫폼과
프로젝트의 강한 통합 증거이지 임의 석재·현장·상업 생산성의 증명은 아니다.

### 읽고 나면 말할 수 있어야 하는 것

- 인식부터 배치까지 폐루프를 재구성한다.
- 이 논문이 굴착과 조립 스트림의 합류점인 이유를 설명한다.
- 실규모 시연이 증명한 것과 남긴 일반화 공백을 구분한다.
