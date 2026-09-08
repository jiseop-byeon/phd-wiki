# 부재·희소성 주장 검증 원장 (2026-09-08)

9월 7일 감사가 "검색식·DB·기간을 다시 돌린 뒤에만 갱신"으로 보류한 항목. 규식
`no published|almost no|there is no|없다시피|전무하|거의 없다|사실상 없다|보고된 바 없`으로 39줄.

## 분류

| 부류 | 건수 | 처리 |
|---|---|---|
| 수사·개념 ("선택이 없으면 0", "두 번째 기회는 없다" 등) | 20 | 문헌 주장이 아님. 무변경 |
| 특정 논문에 대한 주장 | 8 | 원문 초록으로 확인. 전부 일치 |
| 분야 전체에 대한 부재 주장 | 5 | 아래 |
| 기타 (study-log 편집 메모, 교과서 부재 등) | 6 | 저위험. 무변경 |

## 특정 논문 주장 — 확인 결과

| 위키 | 주장 | 원문 | 판정 |
|---|---|---|---|
| conceptgraphs.md:46 | 초록에 숫자 없음 | arXiv:2309.16650 초록 숫자 토큰 0 | 일치 |
| exact-2024.md:39 | 시뮬레이터 검증만 | arXiv:2405.05861 초록 "build a simulator based on captured real-world data", hardware/field 0회 | 일치 |
| apolinarska-timber.md:104 | 실로봇 *파인튜닝 단계* 없음 | 10.1016/j.autcon.2021.103569 초록 "trained entirely in simulation and successfully deployed in reality" | 일치 (실로봇 배포는 있음; 위키도 그렇게 씀) |
| liang-lfd.md:34 | 물리 로봇 결과 없음, Gazebo 78% | 10.1016/j.autcon.2020.103370 초록 Gazebo 언급, real robot 0회 | 일치 |
| simulators:313 | OpenConstruction은 시각 전용, force/tactile 행 없음 | arXiv:2508.11482 초록 51개·2005–2024·images/videos/point clouds, force/tactile 0회 | 일치 |
| simulators:189,435 / study-log:202 | RAMP 초록에 construction 없음, 오프사이트 프레이밍은 본문 | arXiv:2305.09644 초록 construction 0회, offsite 0회 | 일치 (위키가 이미 초록/본문을 구분) |
| simulators:246 | OXE 개요표에 force/tactile 열 없음 | 미확인 (스프레드시트 필요) | 저위험, 보류 |
| tactile:357 | 마모는 표준 누락, PolyTouch가 예외 | 희소성 주장, 예외 명시 | 형식 적절, 무변경 |

## 분야 부재 주장 — 재검색 결과

### A. "접촉이 많은 건설 조작에 가동 중 현장 결과가 거의 없다" (construction-manipulation §3, real-world-impact §2)
- 원 검색: 여섯 키워드(drilling, drywall, rebar, facade, timber, welding), 2026-08-21 기록(study-log §2026-08-21(4), 커밋 54068ed), 08-23 확장(53f4ab4). 예외 3편 명시, STCR 시대 제외 명시. **형식은 감사 기준을 이미 충족**했으나 검색 시점이 본문에 없었음.
- 9월 재검색(arXiv+Crossref): 후보 2 — arXiv:2509.13595(육각 커튼월; 초록상 실험실, 현장은 향후 과제), ISARC 2025/0058(드라이월; 초록 미획득). 그 밖에 arXiv:2608.22100(트러스 조립 sim-to-real, 실험실), 2309.11619(가상 시연)는 현장 아님.
- **조치**: §3에 검색 시점·DB·재검색 후보 2편과 그 상태를 양쪽 반에 추가. 집계(3편)는 변경하지 않음.

### B. "현장 건설 조작에 공유 벤치마크가 없다" (simulators §9 항목 5)
- 후보: arXiv:2512.14031(VLA vs RL 비교 평가 — 한 논문 안의 평가, 공유 실물 아님), CRC 2026 10.1061/9780784486979.004 "Benchmarking Humanoid Robot Controllers for Contact-Rich Construction Tasks"(초록 봇 차단으로 미획득; 제목만), 2608.22100("benchmark"는 동사).
- **조치**: 항목 5에 "벤치마킹 논문 ≠ 공유 벤치마크"와 확인 시점(2026-09) 추가. 주장 유지.

### C. human-pose-gaze:94/279 "배포된 거의 모든 시선 인지 시스템은 머리 자세 인지이고 거의 밝히지 않는다"
- 문헌으로 확인할 수 없는 보편 주장. **조치**: 표가 지지하는 범위(눈 영역 분해 거리)로 재서술.

### D. human-pose-gaze:151 "교과서 없음" / attention:88 "2017 블록 그대로인 모델은 거의 없다"
- 반증 어려움·저위험. 무변경.

## 얻지 못한 것
- ISARC 2025/0058 초록 (S2·랜딩 페이지 모두 없음)
- CRC 2026 벤치마크 초록 (ASCE 봇 차단)
- OXE 개요 스프레드시트 열 목록
이 셋은 위키 본문에 "미확인"으로 적어 두었거나(앞의 둘) 보류했다(OXE).

---

# 설명 없는 표시 수식 — 2026-09-08 회차

`audit_gaps.py` UNEXPLAINED 검출기 기준. 규칙: 검출기용 단어를 넣는 게 아니라 "왜 이 모양인가"를 말하는 문장을 넣는다. 검출기의 어간 뒤 `\b` 때문에 활용형(Rearranging, Substituting)은 걸리지 않으므로, 어차피 더 나은 명령형·명사형(Solve for, substitute, Expand)으로 쓴다.

| 회차 | 페이지 | 건수 변화 | 커밋 |
|---|---|---|---|
| 1 | control-theory-ce397 | 6 → 0 | 3f997d2 |
| 2 | optimization, manipulator-kinematics-dynamics, linear-algebra | 각 3 → 0 | 2adf82b |

전체: 35 → 20 (100개 중). 남은 20건 분포: state-estimation-slam·rl-basics·neural-network-basics·lqr-lqg·information-theory·human-intent-prediction·force-compliance-control 각 2, teleoperation-demonstration·se3-geometry·planning-decision-making·human-pose-gaze·egocentric-perception·contact-force-tactile 각 1.

작업 요령(재발 방지): 앵커는 반드시 repr로 확인한 원문 그대로 쓴다(줄바꿈 위치). 같은 LaTeX가 양쪽 반에 있으므로 파일을 `## 한국어`에서 갈라 각 반 안에서만 치환한다. 치환 후 검출기 로직을 해당 페이지에 재현해 0을 확인한 뒤 커밋한다.
