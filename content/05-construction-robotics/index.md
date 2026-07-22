---
title: 5. Construction
---

## English

Map of content for construction (and adjacent manufacturing) robotics — the lab's core domain.
This area spans four disciplines, so the literature is scattered across their venues:

- **Civil engineering**: Automation in Construction, Journal of Computing in Civil Engineering, ISARC
- **Computer science / robotics**: ICRA, IROS, CoRL, RSS, T-RO, RA-L
- **Mechanical engineering**: field robotics venues, Journal of Field Robotics
- **Electrical engineering**: control and systems venues

### Topic buckets (to be refined)

- Excavator / heavy-machinery automation
- Robotic construction assembly (masonry, rebar, timber, 3D printing)
- Site perception & mapping (SLAM, progress monitoring, digital twin)
- Human-robot collaboration on site
- Learning-based manipulation for construction tasks

Start with the two maps: [[05-construction-robotics/lineage|research lineage]] (four eras
→ today's physical-AI question) and [[05-construction-robotics/labs|who does this research]]
(US labs + the ETH cluster). Survey entries live in
[[01-canonical-papers/canonical-list|section 8 of the canonical list]].

## 한국어

건설로봇(그리고 인접한 제조 분야 로봇) 연구를 정리하는 공간 — 우리 랩의 핵심 연구 분야.
여러 학문 분야에 걸쳐 있어서 논문이 학회와 저널 곳곳에 흩어져 있다:

- **건설/토목**: Automation in Construction, J. of Computing in Civil Engineering, ISARC
- **컴퓨터과학/로보틱스**: ICRA, IROS, CoRL, RSS, T-RO, RA-L
- **기계공학**: Journal of Field Robotics 등 필드 로보틱스 계열
- **전기전자**: 제어·시스템 계열

### 주제 분류 (계속 다듬을 예정)

- 굴착기/중장비 자동화
- 로봇 시공·조립 (조적, 철근, 목조, 3D 프린팅)
- 현장 인식과 지도 작성 (SLAM, 공정 모니터링, 디지털 트윈)
- 현장에서의 인간-로봇 협업
- 건설 작업을 위한 학습 기반 매니퓰레이션

두 개의 지도에서 시작하라: [[05-construction-robotics/lineage|연구 계보]](네 시대 →
오늘의 physical AI 질문)와 [[05-construction-robotics/labs|이 연구를 하는 곳]](미국 랩들 +
ETH 클러스터). 서베이 항목은 [[01-canonical-papers/canonical-list|핵심 논문 리스트 8번 섹션]]에 있다.

### 건설로봇 논문 읽기 틀 · Reading frame for construction-robotics papers

딥러닝 논문처럼 구조와 벤치마크만 읽으면 이 분야 논문은 평가할 수 없다 — 현장 조건과
시스템 통합이 본질이기 때문이다. 논문마다 다음 축을 채워 가며 읽어라:

| 축 | 물어볼 것 |
|---|---|
| 작업 | 굴착·조립·점검·조작 중 무엇이고, 실제 공정의 어느 단계인가 |
| 신체 | 굴착기·팔·모바일 매니퓰레이터·드론 — 페이로드와 도달 범위는 |
| 인식 | LiDAR·비전·BIM·GNSS 중 무엇을 어떤 조건(먼지·조명·진동)에서 |
| 표현 | 지도·디지털 트윈·작업 상태 — 무엇을 어떻게 유지하나 |
| 계획·제어 | 고전(MPC 등)인가 학습인가, 주기는 얼마인가 |
| 자율 수준·인간 개입 | 완전 자율인가, 원격조작 보조인가, 리셋은 누가 하나 |
| 배포 환경·안전 | 실험실 목업인가 실제 현장인가, 안전 장치와 가정은 |
| 평가의 현실성 | 몇 회 시행, 어떤 날씨·현장 변동, 폐루프인가 |
| sim-to-real·확장성 | 시뮬레이션 격차와 기계·현장당 비용은 |

이 틀로 읽으면 "인상적인 데모"와 "배포 가능한 시스템"이 구분된다.
