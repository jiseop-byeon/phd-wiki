# Robotics 학습성 정독 감사 — 최종본

- 감사일: 2026-09-07
- 범위: `content/04-robotics/**/*.md`
- 대상: 공업수학 수강 경험은 있으나 ML·로봇을 처음 독학하는 공대생
- 판정 기준: Physical AI 논문의 용어·식의 역할·방법/실험/가정을 읽는 문해력, 선택 영역에서 Working으로 넘어갈 발판
- 제한: 본문 수정·배포·커밋 없음. 원 논문 전수 검증을 주장하지 않음.
- **현재 상태:** 범위의 Markdown **36/36개 완독**. 각 파일의 영어·한국어 절을 EOF까지 읽고 핵심 주장·수식·수치·학습 경로를 대조했다.

## 현재 총평

읽은 범위에서는 “입력–출력–가정–실패 조건”을 반복해서 묻고, 같은 패널 접촉 과제를 기하·추정·계획·제어에 관통시키는 학습 설계가 좋다. 특히 접촉 페이지의 마찰원뿔 해석, 기하 인식 페이지의 프레임·보정 경고, HRI 페이지의 개입 집계 규칙은 초보자가 논문 결과를 과신하지 않게 하는 실질적 문해력을 준다.

다만 일부 대목은 강한 수사 때문에 모델의 적용 조건이 뒤로 밀리거나, 부등식에서 나오지 않는 결론을 단정한다. 영어판에만 들어간 수정·단서가 한국어판에 반영되지 않은 곳도 있어, 한국어 독자는 다른 개념을 배우게 된다. 가장 중대한 항목은 제어의 위상여유 결론(`robotics-P1-001`), 파지의 접촉 수 양언어 불일치(`robotics-P1-004`), 포인트클라우드와 extrinsic 관계(`robotics-P1-005`), AUC를 배포 임계값처럼 쓰는 의도 예측 예제(`robotics-P1-015`), 제한된 LQR 예제를 모든 가중치로 일반화한 설명(`robotics-P1-017`), 지연 안정성의 과도한 단정(`robotics-P1-020`)이다. 이들을 고치면 입문자가 논문에서 용어·식의 역할·가정·실험 경계를 읽는 데는 전반적으로 좋은 Working 발판이다.

## 발견

### robotics-P1-001 — 감도 피크에서 “45° 위상여유는 불가능”이라는 결론이 나오지 않는다

- 위치: `content/04-robotics/control-theory-ce397.md:241` — “`Then φ_m ≥ ... = 33°. A requirement of φ_m = 45° is therefore not achievable`”; 한국어 `:632` — “`φ_m ≥ ... = 33°다. 따라서 φ_m = 45°라는 요구는 ... 달성 불가능하다`”
- 문제: 바로 앞 식은 위상여유의 **하한**을 준다. 하한이 약 33°라는 사실은 45°를 배제하지 않는다. 따라서 이 예제의 핵심 결론과 “어떤 제어기로도”라는 문장이 제시된 계산으로 증명되지 않는다. 초보자는 필요조건/충분조건과 부등호 방향을 거꾸로 학습한다.
- 수정안: `:241`/`:632`의 45° 불가능 문장을 삭제하고 “이 계산은 최소 감도 피크(또는 최대 감도여유)에 대한 제약을 주지만 45° 위상여유의 불가능성을 단독으로 증명하지 않는다”로 교체한다. 불가능 예제를 유지하려면 위상여유의 상한을 실제로 주는 별도 정리와 그 가정을 제시해 다시 계산한다.
- 우선순위: P1 (사실/추론 오류)
- 근거 신뢰도: 본문 확인(부등식 방향과 결론의 논리 불일치)

### robotics-P1-002 — 안정성과 2차 응답의 설명이 적용 범위를 넘어선다

- 위치: `content/04-robotics/control-theory-ce397.md:93` — “`Complex eigenvalues are ringing; real ones are monotone`”; `:110` — “`Stable only says the error eventually goes to zero`”; `:123` — “`Any second-order response is described by two numbers`”; 한국어 `:501`, `:515`, `:526`에 같은 주장
- 문제: 실수 극점만 있어도 모드 계수·영점·출력 선택에 따라 비단조 응답이 가능하다. 내부 안정은 일반적으로 기준값 추종 오차 0을 보장하지 않는다. 정착시간·오버슈트 공식은 표준적인 우세 2차, 영점 영향이 작은 계단응답 등의 조건이 필요하다. 현재 문구는 상태 안정성, 추종 성능, 출력 응답을 하나로 합친다.
- 수정안: §3 뒤에 “여기서는 단일/우세 2차 모드와 해당 상태 성분을 보는 경우”라는 적용 범위 문단을 추가한다. §4는 “자율계 상태가 원점으로 수렴”으로, §5는 “영점 영향이 작고 표준 2차 분모가 지배하는 단위 계단응답”으로 고친 뒤, 같은 극점을 갖지만 영점 때문에 오버슈트가 달라지는 한 줄 반례를 넣는다.
- 우선순위: P1 (핵심 개념 오개념)
- 근거 신뢰도: 본문 확인

### robotics-P1-003 — 위치제어/강체접촉 예제가 국소 모델을 1 cm까지 외삽해 보편 명제로 만든다

- 위치: `content/04-robotics/force-compliance-control.md:70` — “`1 cm error against 10^7 N/m asks for 10^5 N`”, `:72` — “`a position controller is never pointed at structure`”; 한국어 `:548`–`:551`
- 문제: Hertz 접촉강성은 국소·비선형이고, 실제 폐루프에는 제어기 강성, 직렬 구조 유연성, 토크 포화가 함께 있다. 뒤 `:108`/`:585`에 단서가 있지만, 앞 계산은 서로 다른 강성 정의를 섞어 1 cm까지 선형 외삽하고 “never”를 결론낸다. 실제 산업용 위치제어 로봇도 공정·툴의 수동 순응성과 힘 제한을 두고 구조물에 접촉한다.
- 수정안: 계산 **앞**에 “접촉점의 국소 선형화이며 실제 힘 예측이 아니라 위험 스케일 설명”을 둔다. 힘은 `K_e` 단독이 아니라 제어기/로봇/툴/환경 직렬 등가강성 및 포화로 제한된다고 쓰고, 결론을 “도달 불가능한 침투 위치를 높은 폐루프 강성으로 명령하면 위험하다”로 좁힌다.
- 우선순위: P1 (사실 범위/물리 모델 혼동)
- 근거 신뢰도: 본문 확인; 표의 수치 범위 자체는 추가검증 필요

### robotics-P1-004 — hard-finger 3D 접촉 수 설명이 영어와 한국어에서 다르다

- 위치: `content/04-robotics/grasping.md:113` — 영어 “`three non-collinear contacts is the 3D minimum`”, `:120` — “`Markenscoff's four ... universal bound`”; 한국어 `:469` — “`불가 — 이것이 Markenscoff의 넷`”, `:472`–`:475`에는 universal/particular 구분이 없음
- 문제: 영어는 특정 물체에서 가능한 최소와 모든 물체에 대한 보편 충분 수를 나누지만, 한국어는 hard-finger 행 자체를 “넷”으로 고정한다. 같은 문서의 자가점검도 넷을 일반 force-closure 수처럼 되풀이해 한국어 독자는 접촉 모델뿐 아니라 양화 범위까지 다르게 배운다.
- 수정안: 한국어 표를 영어 최신판과 맞춰 “특정 형상에서는 3개의 비공선 접촉이 가능할 수 있음 / Markenscoff의 4는 모든 물체에 대한 보편 bound”로 분리하고, `:652`, `:672`의 학습목표·정답도 “접촉 모델 + 특정/보편 양화”를 답하게 고친다. 원 논문 문구를 확인해 necessary/sufficient의 정확한 양화 범위를 각주로 고정한다.
- 우선순위: P1 (양언어 불일치·정리 오독 위험)
- 근거 신뢰도: 본문 확인; 정확한 원 정리 문구는 원 출처 확인 필요

### robotics-P1-005 — 포인트클라우드는 extrinsic의 중요성을 없애지 않는다

- 위치: `content/04-robotics/grasping.md:201` — “`camera extrinsics stop mattering because the points are already in a fixed frame`”; 한국어 `:541` — “`미터 기하와 시점 불변성을 거의 공짜로`”
- 문제: 점들을 로봇 고정 프레임으로 옮기려면 정확한 extrinsic이 필수다. 잘못된 extrinsic은 점군 전체를 계통적으로 틀리게 만들며, 같은 범위의 기하 인식 문서 `geometric-perception-calibration.md:140`–`:142`도 이를 정확히 설명한다. 표현 자체도 회전/시점 불변이 아니고, 가림으로 보이는 점 집합이 변한다. 영어와 한국어의 단서 수준도 다르다.
- 수정안: 표의 장점을 “보정된 깊이와 **정확한 extrinsic을 통해** 미터 좌표를 명시적으로 제공”으로 바꾸고, 비용에 “extrinsic 오차·가림·회전 불변성 없음”을 양언어 동일하게 넣는다. 기하 인식 §3으로 링크한다.
- 우선순위: P1 (시스템 프레임 오개념)
- 근거 신뢰도: 본문 상호 확인

### robotics-P1-006 — 환경 접촉이 “공짜이고 절대 미끄러지지 않는다”는 서술은 틀리다

- 위치: `content/04-robotics/grasping.md:244`–`:245` — “`the wall's contact costs nothing, needs no actuator, and never slips out of position`”; 한국어 `:574`–`:577`
- 문제: 환경 접촉에도 법선력을 만드는 로봇 구동·중력·지지가 필요하고 마찰원뿔을 넘으면 미끄러진다. 환경이 고정돼 있어도 물체-환경 접촉점은 이동·이탈할 수 있다. 이 문장은 바로 앞에서 배운 단방향 접촉과 마찰 가정을 무효화한다.
- 수정안: “추가 손가락 구동기 없이 외부 지지·마찰을 활용할 수 있지만, 필요한 법선력·마찰·환경 강성·접촉 유지 조건을 접촉 집합에 포함해야 한다”로 교체한다. 벽 밀기 예제에 `|f_t|≤μf_n`을 한 번 적용한다.
- 우선순위: P1 (접촉 물리 사실 오류)
- 근거 신뢰도: 본문 확인

### robotics-P1-007 — PFL의 한국어 번역이 ‘역량 제한’으로 잘못되어 있다

- 위치: `content/04-robotics/hri-safety.md:409` — “`역량 제한(PFL)`” (영어 `:152`는 “`Power and force limiting`”)
- 문제: PFL은 power and force limiting으로, 로봇의 ‘역량(capability)’이 아니라 동력/힘 제한 방식이다. 안전 표준 검색·논문 독해에 직접 쓰는 핵심 용어라 오역은 학습을 막는다.
- 수정안: `:386`, `:409` 등 한국어 PFL 표기를 모두 “동력 및 힘 제한(Power and Force Limiting, PFL)”으로 통일한다.
- 우선순위: P1 (핵심 안전 용어 오역)
- 근거 신뢰도: 본문 영어-한국어 대조 확인

### robotics-P2-008 — 접촉 충격의 무감쇠 선형모델에서 보편적 제어 한계로 너무 빨리 일반화한다

- 위치: `content/04-robotics/force-compliance-control.md:258`–`:275` — “`contact is a half-sine`”, “`impulse is conserved`”, “`no control law can change Λ or K during a 1.4 ms event`”; 한국어 `:727`–`:742`
- 문제: 식은 무감쇠 선형 스프링, 일정 유효질량, 완전 에너지 저장/반환이라는 모델에서만 나온다. 실제 충돌의 감쇠·소성·반발·다중 접촉·접근 전 속도 제어를 생략한 채 “유일한 지렛대”라고 하면 독자가 계산값을 측정 예측으로 오해한다.
- 수정안: 식 직전에 가정 목록을 넣고, `v`는 접근 전 제어가 바꿀 수 있는 가장 직접적 변수임을 명시한다. 표 제목을 “무감쇠 1축 선형 충돌 모델의 예시”로 바꾸며 실제 데이터에서는 force-time trace와 식별된 등가 `Λ,K,D`를 확인하게 한다.
- 우선순위: P2 (유용한 개선)
- 근거 신뢰도: 본문 확인

### robotics-P2-009 — ε grasp quality의 단위·스케일 정규화가 빠져 있다

- 위치: `content/04-robotics/grasping.md:135`–`:152`; 한국어 `:483`–`:497`
- 문제: wrench는 힘(N)과 모멘트(N·m)를 함께 가지므로 그대로 만든 ‘공의 반지름’은 기준 길이/토크 스케일과 물체 원점, 접촉력 정규화에 따라 달라진다. 이를 빼면 서로 다른 물체·구현의 ε를 직접 비교해도 된다고 오해한다.
- 수정안: 정의 직후 “특성 길이로 모멘트를 스케일하고, 원점 및 접촉력 예산을 고정해야 수치가 의미 있다”를 추가하고, 같은 접촉에서 특성 길이만 바꾸면 ε가 달라지는 1문장 예를 넣는다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인

### robotics-P2-010 — 자기중심 인지 페이지가 약속한 ‘과제별 지표’를 실제로 주지 않는다

- 위치: `content/04-robotics/egocentric-perception.md:16`–`:17`, `:140`–`:148`; 한국어 `:191`–`:194`, `:316`–`:324`
- 문제: 깊이 목표와 학습 후 목표는 과제군과 “각 지표”를 말하게 하지만 §2는 과제 이름만 열거하고, recognition의 top-k/mAP, anticipation의 time-to-action, active-object detection의 mAP, gaze의 angular/pixel error, episodic retrieval의 recall 등 지표 정의가 없다.
- 수정안: §2 직후에 과제/출력/대표 지표/지표가 놓치는 것 4열 표를 추가한다. 새 과목으로 넓히지 말고 현재 열거한 여섯 과제만 한 행씩 다룬다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인

### robotics-P2-011 — 보행 주파수 제거를 주의 신호 분리의 충분한 처방처럼 제시한다

- 위치: `content/04-robotics/egocentric-perception.md:63`–`:64`, `:158`–`:161`; 한국어 `:240`–`:241`, `:334`–`:337`
- 문제: 보행 유발 head motion과 의도적 재정향은 비정상·중첩 주파수일 수 있고, 단순 주파수 제거는 실제 관심 신호도 제거할 수 있다. 자가점검 정답의 “분리 가능”은 가설/전처리 후보를 식별 가능성 보장처럼 만든다.
- 수정안: “IMU/보행 위상/영상 안정화로 보행 성분을 **모델링하거나 조건화하고**, attention label로 잔여 신호의 유효성을 검증한다”로 좁힌다. 단순 필터가 실패하는 회전·가속 보행 예를 한 문장 추가한다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인; 구체적 신호처리 권고는 추가검증 필요

### robotics-P2-012 — SSM 예제의 ‘로봇을 세워도 0.99 m’는 변수 해석이 일관되지 않다

- 위치: `content/04-robotics/hri-safety.md:182`–`:189`; 한국어 `:435`–`:442`
- 문제: `v_r=0`인 이미 정지한 로봇에 기존 반응+정지시간 0.4 s와 사람 접근거리 0.64 m를 그대로 유지한다. “감속 중 속도를 0으로 보낸 경우”인지 “위험 동작 전부터 정지 상태”인지가 다르며, 후자라면 같은 보호거리 계산을 그대로 적용할 이유가 없다. 또 `S_s=½vT_s`는 일정 감속 가정이다.
- 수정안: 1.0→0.5 m/s 비교까지만 두고, 0 m/s 행은 삭제하거나 “감지 시점에 1 m/s였다가 정지 명령을 받은 경우”와 “이미 monitored standstill인 경우”를 분리한다. 일정 감속 가정도 식 옆에 적는다.
- 우선순위: P2
- 근거 신뢰도: 본문 계산/변수 정의 확인; 표준의 정확한 적용은 최신 공식 원문 확인 필요

### robotics-P2-013 — 시차(disparity)를 각도라고 부르는 도해 문구

- 위치: `content/04-robotics/geometric-perception-calibration.md:131` — “`Disparity is that angle`”; 한국어 `:344` — “`시차가 곧 그 각도다`”
- 문제: rectified stereo에서 disparity는 대응 픽셀의 수평 좌표 차이(픽셀)이고 삼각측량 각도와 관련되지만 같은 양은 아니다. 바로 위 식은 픽셀 단위 `d`를 쓰므로 도해가 단위를 혼동시킨다.
- 수정안: “시차는 두 영상의 수평 픽셀 이동이며, 멀수록 두 관측 광선 사이 각과 함께 작아진다”로 교체한다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인

### robotics-P1-015 — AUC를 배포 가능한 결정 임계값처럼 사용한다

- 위치: `content/04-robotics/human-intent-prediction.md:61` — “`the largest Δ at which the predictor still clears the decision threshold`”; `:68` — “`model B holds AUC 0.78 ... Model A cannot be used at all`”; 한국어 `:318`, `:325`에 같은 결론
- 문제: AUC는 모든 분류 임계값을 훑어 순위 판별력을 요약한 지표이지, 실제 경보 임계값에서의 확률·재현율·오경보율이 아니다. 따라서 AUC 0.78이 1.5초 선행에서 제동 결정을 지지하거나 A가 “아예 쓸 수 없다”는 결론은 나오지 않는다. 또한 `max` 정의는 성능이 시간에 따라 단조라는 가정을 숨긴다. 뒤 §4가 보정을 올바르게 강조하기 때문에 내부적으로도 충돌한다.
- 수정안: §3의 `performance`를 “배포 운용점의 지표(예: 허용 FPR에서의 recall, 기대 위험, 보정된 사건확률)”로 한정하고 AUC 곡선은 판별력 진단으로 분리한다. 예제에는 두 모델의 동일 FPR에서 recall 또는 비용 행렬과 보정된 임계값을 제시해 `Δ*`를 계산한다. 비단조 곡선이면 연속 구간 또는 보수적 최초 교차로 정의한다.
- 우선순위: P1 (지표 역할 오개념)
- 근거 신뢰도: 본문 확인

### robotics-P2-016 — conformal coverage를 개별 안전확률로 읽게 한다

- 위치: `content/04-robotics/human-intent-prediction.md:117`–`:121` — “`distribution-free coverage guarantee under exchangeability`”, “`the output is exactly what a safety decision needs`”; 한국어 `:374`–`:378`
- 문제: 교환가능성 아래의 conformal 보장은 보통 표본 전체에 대한 **주변적 coverage**다. 개별 장면의 90% 사건확률이나 조건부 안전 보장이 아니며, 양 클래스가 모두 든 집합은 유용한 defer 신호일 수 있어도 곧바로 안전 결정을 주지 않는다.
- 수정안: 표 바로 뒤에 “coverage는 개별 사례 확률이 아니며 분포 이동·조건부 하위집단에서는 별도 검증이 필요하다”를 넣는다. `{'crossing','not crossing'}`이면 질문/감속으로 넘기는 짧은 정책 예를 추가해 ‘집합→행동’ 규칙을 명시한다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인; 안전 적용 범위는 추가검증 필요

### robotics-P1-017 — 특수한 LQR 가중치 결과를 ‘어떤 가중치에서도’로 일반화한다

- 위치: `content/04-robotics/lqr-lqg.md:105`–`:110` — “`ζ = 0.707 for any weights`”, “`LQR on a double integrator always`”; 한국어 `:261`–`:267`; 같은 문서 `:126`/한국어 `:279`는 “`Weights on velocity vs position shape damping`”이라고 한다
- 문제: 고정 감쇠비는 이 페이지가 계산한 특수한 `Q=diag(q,0), R=r`에서 나온다. 속도 상태에도 가중치를 주면 Riccati 해와 폐루프 감쇠가 달라진다. 문서 자체가 몇 줄 뒤 그 사실을 말해 직접 모순되고, 초보자는 LQR의 Q 설계 자유도를 잃는다.
- 수정안: “이 **특수한 위치-only Q**에서는 모든 `q/r`에 대해 0.707”로 범위를 좁힌다. 이어 `Q=diag(q_p,q_v)`에서 `q_v`를 바꾸면 감쇠가 변하는 두 행짜리 수치 예를 넣고, §7의 결론도 같은 범위로 고친다.
- 우선순위: P1 (내부 모순·일반화 오류)
- 근거 신뢰도: 본문 확인

### robotics-P2-018 — “Q/R 비만 의미”는 행렬 가중치 독법으로 부족하다

- 위치: `content/04-robotics/lqr-lqg.md:102`–`:104` — “`Only the ratio matters`”, “`papers quote Q/R ratios`”; 한국어 `:258`–`:260`
- 문제: 불변인 것은 모든 `Q`와 `R`에 같은 양의 스칼라를 곱하는 경우다. 다상태 행렬에서는 위치·속도·축 사이 상대 가중치가 핵심이며 일반적인 ‘Q/R’ 하나로 환원되지 않는다.
- 수정안: 소제목을 “공통 스칼라 배율은 의미가 없다”로 바꾸고 “행렬 내부 상대 가중치는 의미가 있다”를 바로 덧붙인다. 현재 1차원 예제를 일반 행렬의 보편 규칙으로 읽지 말라는 한 문장을 넣는다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인

### robotics-P2-019 — ALOHA의 하드웨어 생존을 임피던스 제어 하나에 귀속한다

- 위치: `content/04-robotics/modern-robotics/ch11-robot-control.md:40`–`:42` — “`impedance control is why ALOHA-class contact tasks don't destroy their hardware`”; 한국어 `:67`–`:69`
- 문제: 특정 플랫폼의 접촉 안전은 액추에이터·감속기·전류/토크 제한·저수준 위치/전류 루프·수동 순응성·속도와 과제 설정이 함께 정한다. 해당 문장은 ALOHA 계열이 실제로 어떤 임피던스 루프를 썼는지 근거 없이 단일 원인으로 만들며, ‘모든 VLA가 정확히 이 루프’라는 앞 문장도 인터페이스 다양성을 지운다.
- 수정안: 위키 연결을 “VLA 행동은 플랫폼별 위치·속도·토크·임피던스 인터페이스와 저수준 루프를 거친다”로 바꾼다. ALOHA는 원 논문의 명령 인터페이스와 보호장치를 확인해 구체적으로 쓰거나 이름을 빼고 일반적 임피던스 예로 교체한다.
- 우선순위: P2
- 근거 신뢰도: 본문 확인; ALOHA 실제 저수준 제어 구성은 원 출처 확인 필요

### robotics-P1-020 — 지연이 크면 ‘게인을 아무리 줄여도’ 진동한다는 단정

- 위치: `content/04-robotics/teleoperation-demonstration.md:115`–`:119` — “`for a large enough T the loop oscillates no matter how small the gains are`”; 한국어 `:529`–`:532` — “`게인을 아무리 줄여도 루프가 진동한다`”. 또한 영어 `:58`/한국어 `:473`–`:474`는 unilateral을 “`unconditionally stable`/`무조건 안정`”이라 한다.
- 문제: 시간지연이 power-variable 채널의 수동성을 깨고 안정 여유를 줄인다는 핵심은 맞지만, 그것이 모든 양의 이득에서 반드시 불안정이라는 뜻은 아니다. 충분히 낮은 대역폭·이득이나 추가 감쇠로 안정 영역을 얻을 수 있고, unilateral도 로컬 팔로워 제어까지 포함한 전체 시스템의 무조건 안정성을 보장하지 않는다. 초보자는 ‘수동성 보장 실패=필연적 불안정’을 동일시하게 된다.
- 수정안: “직접 power-variable 결합은 임의 지연에 대한 **수동성 기반 안정 보장**을 잃고, 지연이 커질수록 안정–투명성 절충이 악화된다”로 교체한다. 게인 저하는 성능을 희생해 안정화할 수 있으나 임의 지연 보장은 아니라고 구분하고, unilateral은 “원격 힘 피드백 루프가 없어 채널 유발 불안정 위험이 작다”로 좁힌다.
- 우선순위: P1 (안정성·수동성 논리 오류)
- 근거 신뢰도: 본문 확인; 정량 안정영역은 시스템 모델별 추가검증 필요

### robotics-P2-021 — “강한 현대 결과들은 아무것도 학습하지 않는다”가 같은 페이지의 학습 기반 계열까지 덮는다

- 위치: `content/04-robotics/semantic-language-navigation.md:259` — “`The strong modern results train nothing`”; 한국어 `:539` — “`강한 현대 결과들은 아무것도 학습하지 않는다`”. 같은 문서 `:197`–`:200`/한국어 `:483`–`:485`는 Uni-NaVid가 360만 샘플로 학습됐다고 설명한다.
- 문제: 무학습 주장은 VLFM·ESC·CoWs 같은 zero-shot 모듈형 계열에만 맞는다. NaVid/Uni-NaVid 같은 종단간 계열까지 포함하는 “현대 결과” 일반론으로 읽으면 방법 계보와 데이터 요구량을 거꾸로 이해한다.
- 수정안: §8 표의 답을 “강한 **zero-shot 모듈형** 결과는 ObjectNav 전용 학습 데이터를 쓰지 않는다; 종단간 비디오-VLA는 대규모 embodied 데이터를 학습한다”로 바꾸고, 질문도 “ObjectNav 전용 데이터인가, 다른 embodied 데이터인가?”로 세분한다.
- 우선순위: P2
- 근거 신뢰도: 본문 상호 확인

### robotics-P3-014 — 최신 VLA 흐름을 ‘일방향 수렴’으로 단정한다

- 위치: `content/04-robotics/force-compliance-control.md:389`–`:417`; 한국어 `:845`–`:869`
- 문제: 2025 논문 한 편과 2026 프리프린트 둘을 근거로 “direction is one-way”, “every group” 및 향후 인터페이스를 단정한다. 페이지 스스로 이를 예측이라고 뒤에서 밝히지만, Mastery 학습자가 분야 합의로 받아들이기 쉽다.
- 수정안: 절 제목을 “최근 제안과 연구 가설”로 바꾸고, 관찰(각 논문이 실제 구현/보고한 것), 해석(고전 inner loop와의 연결), 예측(향후 표준 인터페이스)을 세 문단으로 분리한다. 프리프린트는 계속 명시한다.
- 우선순위: P3 (선택 개선)
- 근거 신뢰도: 본문 확인; 2025–2026 논문 세부·분야 수렴 판단은 추가검증 필요

### robotics-P3-022 — 한국어 traversability 문장에 상반된 중복어가 남아 있다

- 위치: `content/04-robotics/traversability-off-road.md:370`–`:373` — “`하드웨어를 전혀 하드웨어를 거의 개조하지 않은`”; 영어 `:100`–`:101`은 “`with little hardware modification`”
- 문제: “전혀”와 “거의”가 겹쳐 번역 문장이 깨지고, 해당 연구의 중요한 한정인 ‘little modification’을 초보자가 정확히 인용하기 어렵다.
- 수정안: “하드웨어를 **거의 개조하지 않은** 평범한 바퀴 로봇이”로 고친다. 같은 파일 `:393`의 깨진 강조표기 “`**개입 **최대** 57% 감소**`”도 “`개입 **최대 57% 감소**`”로 정리한다.
- 우선순위: P3
- 근거 신뢰도: 영어·한국어 본문 대조 확인

## 만족한 부분

- `content/04-robotics/index.md:29`–`:32`의 하나의 패널 접촉 과제와 “입력/출력/실패 조건” 체크는 파편화된 과목을 시스템으로 묶는 좋은 학습 장치다.
- `content/04-robotics/contact-force-tactile.md:41` 및 `:65`는 마찰원뿔이 운동 판정이 아니라 힘의 실행가능성 경계임을 분명히 해 흔한 오개념을 막는다. 한국어 `:196`–`:224`도 의미가 잘 맞는다.
- `content/04-robotics/geometric-perception-calibration.md:146`–`:155`의 ICP 설명은 고정 대응 SVD와 대응 선택의 국소성을 나눠, “작은 residual=올바른 pose”가 아님을 잘 가르친다.
- `content/04-robotics/hri-safety.md:215`–`:225`는 권한, 개입, 리셋, assisted completion의 집계 경계를 한 시나리오로 끝까지 따라가 연구 문해력에 직접 기여한다.
- `content/04-robotics/grasping.md:298`–`:309`의 읽기 질문은 grasp success와 task success, unseen의 종류, 재시도, 마찰 가정을 짧고 실용적으로 구분한다.
- `content/04-robotics/human-pose-gaze.md:51`–`:82`는 MPJPE를 순위 점수가 아니라 실제 과제 길이와 비교해야 하는 물리량으로 바꿔 읽게 한다. root-relative/PA-MPJPE 단서도 논문 표를 오독하지 않게 한다.
- `content/04-robotics/planning-decision-making.md:25`–`:45`는 plan/path/trajectory/policy/controller와 workspace/configuration/state/task space를 짧게 분리해 이후 모든 방법의 입출력 역할을 붙잡게 한다.
- `content/04-robotics/state-estimation-slam.md:39`–`:50`, `:65`–`:90`은 state/observation/estimate/belief를 나누고 베이즈 필터의 두 조건부 독립 가정이 어디서 쓰이는지 설명해 식 암기를 논문 가정 점검으로 연결한다.
- `content/04-robotics/video-action-understanding.md:25`–`:47`은 recognition과 anticipation을 인과적 입력 창으로 구분하고 single/shuffled-frame baseline을 요구한다. 인간 의도 논문을 읽는 데 직접적인 문해력이다.

## 파일별 정독 상태와 발견 ID

상태의 “완독”은 줄번호를 붙인 영어·한국어 본문을 처음부터 끝까지 확인한 경우만 뜻한다. 실제 완독 문서 수는 **36/36**이다.

| 파일 | 줄 | 상태 | 발견 ID |
|---|---:|---|---|
| `content/04-robotics/contact-force-tactile.md` | 342 | 완독 | — |
| `content/04-robotics/control-theory-ce397.md` | 790 | 완독 | robotics-P1-001, robotics-P1-002 |
| `content/04-robotics/convex-mpc-legged.md` | 72 | 완독 | — |
| `content/04-robotics/egocentric-perception.md` | 357 | 완독 | robotics-P2-010, robotics-P2-011 |
| `content/04-robotics/force-compliance-control.md` | 951 | 완독 | robotics-P1-003, robotics-P2-008, robotics-P3-014 |
| `content/04-robotics/geometric-perception-calibration.md` | 438 | 완독 | robotics-P2-013 |
| `content/04-robotics/grasping.md` | 704 | 완독 | robotics-P1-004, robotics-P1-005, robotics-P1-006, robotics-P2-009 |
| `content/04-robotics/hri-safety.md` | 524 | 완독 | robotics-P1-007, robotics-P2-012 |
| `content/04-robotics/index.md` | 204 | 완독 | — |
| `content/04-robotics/modern-robotics-book.md` | 74 | 완독 | — |
| `content/04-robotics/modern-robotics/index.md` | 15 | 완독 | — |
| `content/04-robotics/modern-robotics/ch02-configuration-space.md` | 73 | 완독 | — |
| `content/04-robotics/modern-robotics/ch03-rigid-body-motions.md` | 226 | 완독 | — |
| `content/04-robotics/modern-robotics/ch04-forward-kinematics.md` | 190 | 완독 | — |
| `content/04-robotics/modern-robotics/ch05-velocity-kinematics.md` | 194 | 완독 | — |
| `content/04-robotics/modern-robotics/ch06-inverse-kinematics.md` | 261 | 완독 | — |
| `content/04-robotics/modern-robotics/ch08-dynamics.md` | 85 | 완독 | — |
| `content/04-robotics/modern-robotics/ch09-trajectory-generation.md` | 71 | 완독 | — |
| `content/04-robotics/modern-robotics/ch10-motion-planning.md` | 76 | 완독 | — |
| `content/04-robotics/modern-robotics/ch11-robot-control.md` | 80 | 완독 | robotics-P2-019 |
| `content/04-robotics/modern-robotics/ch12-grasping.md` | 89 | 완독 | — |
| `content/04-robotics/modern-robotics/ch13-wheeled-mobile-robots.md` | 101 | 완독 | — |
| `content/04-robotics/human-intent-prediction.md` | 517 | 완독 | robotics-P1-015, robotics-P2-016 |
| `content/04-robotics/human-pose-gaze.md` | 373 | 완독 | — |
| `content/04-robotics/legged-locomotion.md` | 660 | 완독 | — |
| `content/04-robotics/lqr-lqg.md` | 336 | 완독 | robotics-P1-017, robotics-P2-018 |
| `content/04-robotics/mpc.md` | 333 | 완독 | — |
| `content/04-robotics/navigation-mobile-manipulation.md` | 445 | 완독 | — |
| `content/04-robotics/planning-decision-making.md` | 512 | 완독 | — |
| `content/04-robotics/robot-systems-deployment.md` | 495 | 완독 | — |
| `content/04-robotics/semantic-language-navigation.md` | 599 | 완독 | robotics-P2-021 |
| `content/04-robotics/state-estimation-slam.md` | 497 | 완독 | — |
| `content/04-robotics/tactile-visuotactile.md` | 797 | 완독 | — |
| `content/04-robotics/teleoperation-demonstration.md` | 824 | 완독 | robotics-P1-020 |
| `content/04-robotics/traversability-off-road.md` | 545 | 완독 | robotics-P3-022 |
| `content/04-robotics/video-action-understanding.md` | 314 | 완독 | — |

## 검증 범위와 제한

- 새 웹 조사는 사용량 제한 요청에 따라 중단했다. 최신 표준·2025–2026 논문·도구 버전은 본문이 인용한 주장으로만 읽었고, 원 출처를 확인하지 않은 니치 판단은 발견별로 “원 출처 확인/추가검증 필요”라고 표시했다.
- 원 논문 전수 fact-check는 하지 않았다. 이 보고서의 “본문 확인”은 위키 내부의 식·논리·양언어 대조로 확정 가능한 판단을 뜻하며, 최신 사실이나 특정 시스템 구현은 원 출처 확인 전까지 제한적으로 읽어야 한다.
- 콘텐츠 파일, 배포 상태, Git 기록은 변경하지 않았다.
