# 건설 로보틱스 정독 감사

- 감사일: 2026-09-07
- 범위: `content/05-construction-robotics/` 전체와 `content/01-canonical-papers/notes/8-construction/` 전체
- 완독: Markdown 37개, 5,350줄. 각 파일을 줄번호가 보이는 본문으로 처음부터 EOF까지 읽었다.
- 관점: 공업수학 수강 경험은 있으나 ML·로봇을 처음 독학하는 공대생이 Physical AI 논문의 용어, 식의 역할, 방법·실험·가정을 읽을 수 있는지와 선택 영역에서 Working으로 이동할 수 있는지.
- 제한: 원 논문 전수 fact-check는 하지 않았다. 사용자의 후속 지시에 따라 추가 웹 검증을 중단했다. 따라서 저장소 본문끼리 확정할 수 있는 모순은 `본문 확인`, 논문·기관 원문을 열어야 확정되는 주장은 `추가검증 필요`로 구분한다. 콘텐츠 수정·배포·커밋은 하지 않았다.

## 총평

**Literacy 목표는 대체로 달성한다.** 특히 건설 로봇 논문을 단순 알고리즘 성능이 아니라 과제 경계, 인간 개입, 현장성, 실패, 생산성으로 읽게 하는 프레임은 훌륭하다. 영어와 한국어도 대부분 의미가 맞고, HEAP/AES/ExT처럼 비슷해 보이는 결과를 시스템·배치·학습 증거로 분리하는 방식이 초보자의 과장된 해석을 잘 막는다.

**이 위키는 `study-depth`(해당 주제를 어디까지 공부할지)와 `wiki-support`(위키 자체가 제공하는 깊이)를 분리하고, 원 논문·교재·실습을 병행하는 구조이므로 위키 본문만으로 구현·변형 가능한 Working을 완결한다고 평가해서는 안 된다.** 현재 범위는 논문을 구조적으로 읽고 선택 영역을 정하는 데 강한 발판을 제공한다. 이후 구현·변형·실험설계 능력은 연결된 원 자료와 실제 실습에서 형성·검증해야 한다. 아래 construction-016의 연구 카드는 이를 대신하거나 Working을 판정하는 관문이 아니라, 다음에 필요한 원문 학습·실습을 스스로 찾는 선택적 진단 도구다.

## 우선순위별 발견

### construction-001 — Han 용접 노트의 DOI가 서로 다름

- 우선순위: **P1 사실 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/han-welding.md:5-7` — `Automation in Construction 168, 105782`, `https://doi.org/10.1016/j.autcon.2024.105782`; 같은 파일 `:17` — `https://doi.org/10.1016/j.autcon.2024.105699`.
- 문제: 같은 논문의 article number/DOI가 두 개라 독자가 다른 논문으로 이동하거나 인용을 잘못 만든다.
- 수정 제안: 출판사 원문에서 정확한 article number와 DOI를 확인한 뒤 frontmatter와 본문 링크를 하나로 통일한다. 확인 전에는 `DOI 확인 필요`로 표시한다.
- 근거 신뢰도: **본문 확인**(내부 불일치 확정), 정확한 정답은 **원 출처 확인 필요**.

### construction-002 — AES가 “단위 없음”이라고 하면서 한국어에서는 tons/hour로 바뀜

- 우선순위: **P1 사실·번역 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/aes.md:49` — `It states no unit and no figure`; `:58` — `숙련 운전자에 가까운 처리량(tons/hour)`; `:81`은 다시 `단위도 수치도 제시하지 않으므로 tons/hour나 m³/h 수치가 아니라 대등성 주장`이라고 정확히 경고한다. `:97`도 다시 `숙련 운전자급 tons/hour`라고 쓴다.
- 문제: 바로 옆의 증거 경계 교육을 한국어 요약과 학습목표가 무너뜨린다. 초보자는 “시간당 처리량”과 “tons/hour라는 단위·수치”를 동일시할 가능성이 높다.
- 수정 제안: `:58`, `:86`, `:97`의 `tons/hour`를 모두 `시간당 자재 처리량의 대등성 주장(단위·수치 미제시)`으로 바꾼다. 영어 체크리스트도 같은 표현으로 맞춘다.
- 근거 신뢰도: **본문 확인**.

### construction-003 — sim-to-real 격차를 “접촉만 모델 문제, 나머지는 파라미터 문제”로 잘못 이분화

- 우선순위: **P1 개념 문제**
- 위치·인용: `content/05-construction-robotics/sim-to-real.md:39-46` — `The other four gaps are parameter problems: the physics is right and the numbers are wrong ... Contact is a model problem.` 한국어 `:212-217`도 동일하다.
- 문제: 바로 위 표에는 unseen site/task distribution, missing returns, dropped messages가 포함된다. 이는 단순히 “맞는 모델의 숫자만 틀린” 경우가 아니다. 센서 가림·미관측, 잘못된 과제 분포, 소프트웨어 구조·지연 모델 누락도 구조적/model-form gap이 될 수 있다. 이분법은 초보자가 도메인 랜덤화로 모든 비접촉 격차를 해결할 수 있다고 오해하게 한다.
- 수정 제안: 해당 경고의 첫 문단을 `모든 격차에는 parameter error와 model-form/coverage error가 있을 수 있다. 접촉은 비평활성·분포 접촉·변형 때문에 model-form error가 특히 지배적이다`로 바꾼다. 표에 `진단: 파라미터 범위 문제인가, 빠진 현상/상태/사건 문제인가?` 한 열을 추가하면 현재 예시를 그대로 살릴 수 있다.
- 근거 신뢰도: **본문 확인**(표와 경고의 논리 충돌), 세부 접촉 엔진 일반화는 **추가검증 필요**.

### construction-004 — 자세 오차 하나가 하이브리드 위치/힘 제어를 “깨뜨린다”는 단정

- 우선순위: **P1 개념 문제**
- 위치·인용: `content/05-construction-robotics/construction-manipulation.md:41-43` — `Row 1 alone breaks hybrid position/force control`; 한국어 `:293-295` — `1행 하나만으로도 하이브리드 위치/힘 제어가 깨진다`.
- 문제: 하이브리드 제어는 선택 좌표계/접촉 법선이 틀리면 성능이 나빠지지만, 자세 불확실성 자체가 아키텍처를 필연적으로 무효화하지는 않는다. 온라인 법선 추정, 접촉 탐지 후 좌표계 갱신, 임피던스/어드미턴스, 낮은 접근 강성 등으로 다룰 수 있다. 현재 문장은 실패 조건과 대응 설계를 지워 버린다.
- 수정 제안: `알려진 법선을 고정한 채 쓰는 순수 하이브리드 제어는 현장 자세 오차에 취약하다`로 한정하고, 바로 뒤에 `논문에서는 법선을 언제·어떻게 추정/갱신하며 접촉 전후 제어 모드를 어떻게 전환하는지 확인하라`를 추가한다. 자기점검 답 `:237`도 “필연적 실패”가 아니라 이 조건부 실패로 맞춘다.
- 근거 신뢰도: **본문 확인**, 제어 이론 표현은 **원 교재 확인 권장**.

### construction-005 — 힘 궤적이면 토질 모델이 불필요하고 “soil-agnostic”이라는 과장

- 우선순위: **P1 개념 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/heap.md:59-62` — `that choice is what makes a dig soil-agnostic, because the soil never has to be modelled`; 한국어 `:124-127` — `굴착을 토질에 무관하게 ... 흙을 아예 모델링하지 않아도`.
- 문제: 힘 피드백은 정확한 토질 파라미터 의존성을 줄이지만, 목표 힘·경로의 실행 가능성, 포화, 버킷 충전, 지반 붕괴와 작업 성과는 여전히 재료 상호작용에 좌우된다. 같은 페이지군의 soil-adaptive RL 소개도 토질 변화가 남은 문제임을 전제한다. “무관”은 robust/reduced model dependence를 model-free generality로 바꾼다.
- 수정 제안: `명시적 정밀 토질 모델에 대한 의존을 줄이고 측정된 상호작용에 반응하게 한다`로 교체한다. `content/05-construction-robotics/earthmoving-heavy-machinery.md:53-57, 239-243, 360-362`의 `soil-agnostic/토질 불가지론적` 표현도 같은 수준으로 제한한다.
- 근거 신뢰도: **본문 확인**(페이지군 내부 긴장), 원 논문의 정확한 제어 목표는 **원 출처 확인 권장**.

### construction-006 — “현장 매니퓰레이터 논문 단 세 편” 집계가 재현 불가능한 상태에서 연구 공백의 핵심 근거가 됨

- 우선순위: **P1 학습·연구경로 차단**
- 위치·인용: `content/05-construction-robotics/construction-manipulation.md:94-95` — `only three papers put a manipulator on an active construction site`; `:107-114`는 `modern literature under six task keywords`라고 범위를 설명하지만 데이터베이스, 실제 검색식, 검색일, 포함/제외 기준, 중복 제거, 심사 기록이 없다. 같은 주장이 `feng-rebar.md:49-50, 96-97`에서 재사용된다.
- 문제: 이 수치가 “그 얇은 기록이 기회다”라는 박사 주제 선택을 직접 밀어 준다. 검색을 재현할 수 없으면 누락 논문 하나가 핵심 novelty 주장과 연구 경로를 바꿀 수 있다. 범위를 밝힌 것은 좋지만 검증 가능한 문헌조사로는 부족하다.
- 수정 제안: §3 바로 아래에 5~8줄짜리 `검색 장부`를 추가한다: 검색일, 데이터베이스, 여섯 과제의 정확한 검색어/동의어, active site 판정 기준, 심사논문만인지, 후보·제외 수, 결과 목록 링크. 장부를 만들기 전에는 `표적 검색에서 확인한 세 사례`라고만 쓰고 `only`를 제거한다.
- 근거 신뢰도: **본문 확인**(재현 정보 부재), “실제로 세 편뿐”인지는 **추가검증 필요**.

### construction-007 — 현장 사례 수는 셋인데 학습목표는 둘이라고 함

- 우선순위: **P2 유용 개선**
- 위치·인용: `content/05-construction-robotics/construction-manipulation.md:99-105`는 Feng, Dörfler, Yu의 `Three verified exceptions`; `:218-219` — `Name the two site-verified contact-rich results`; 한국어 `:459`도 `현장 검증된 접촉 결과 둘`.
- 문제: 독자가 어떤 두 편을 외워야 하는지, Yu를 접촉이 많은 결과에서 제외한 것인지 알 수 없다. `:227-230`의 자기점검은 세 사례를 다시 언급해 혼란이 커진다.
- 수정 제안: 세 편을 모두 학습목표로 두거나, `접촉-rich 판정 기준상 포함되는 두 편`이라면 두 편의 이름과 Yu 제외 이유를 그 문장에 명시한다.
- 근거 신뢰도: **본문 확인**.

### construction-008 — 논문 노트 인덱스가 실험실 논문을 “on-site contact papers”로 묶음

- 우선순위: **P2 분류 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/index.md:28-31` — `Construction manipulation (the on-site contact papers)` 아래 Apolinarska, Feng, Kindle를 나열한다. 그러나 `apolinarska-timber.md:100-103`은 `laboratory sim-to-real, not a construction site`, `kindle-jaibot.md:45-50`은 `not an active construction site`라고 명시한다.
- 문제: 상위 지도가 각 노트의 가장 중요한 증거 경계를 뒤집는다. 초보자가 인덱스만 보고 세 편을 현장 검증 묶음으로 기억할 수 있다.
- 수정 제안: 제목을 `Construction manipulation (contact and deployment evidence)`로 바꾸고 각 링크에 `[lab sim-to-real]`, `[active site]`, `[simulated site disturbances]` 꼬리표를 붙인다. 한국어도 동일하게 맞춘다.
- 근거 신뢰도: **본문 확인**.

### construction-009 — Lasota 결과의 “방향은 강건”과 “방향도 보장 안 됨”이 충돌

- 우선순위: **P1 사실 해석 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/lasota-shah.md:41` — `Benefits ... do not guarantee either their magnitude or direction`; `:43-44` — `what transfers to construction is the direction ... That direction is robust`. 한국어 `:63`과 `:70-71`도 같은 충돌이다.
- 문제: 한 통제 실험은 다른 현장에서 효과 방향까지 강건하다고 보장하지 않는다. 특히 바로 앞에서 현장 잡음·가림·작업 방식이 방향을 바꿀 수 있다고 인정했다. 초보자에게 외적 타당도와 반복 검증을 잘못 가르친다.
- 수정 제안: `건설이 가져갈 것은 효과의 방향이 아니라 함께 측정해야 할 가설과 지표 묶음`으로 바꾼다. 즉 “유창성과 체감 안전이 동시에 좋아질 수 있다는 가설을 현장에서 재검정”한다고 쓴다.
- 근거 신뢰도: **본문 확인**.

### construction-010 — 78% 성공률의 부족분을 공변량 이동으로 단정

- 우선순위: **P1 방법 해석 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/liang-lfd.md:36` — `the 78% ceiling is what compounding error looks like in practice`; `:40-41` — `read the gap to 100% as a miniature lecture on covariate shift`; 한국어 `:56, 66-67`도 동일하다.
- 문제: 집계 성공률만으로 실패 원인을 공변량 이동/오차 누적이라고 식별할 수 없다. 인식, 계획, 시뮬레이터, 초기조건, 과제 정의 등도 원인일 수 있다. 실패 궤적이나 ablation 없이 인과 기전을 배정하면 논문 읽기 교육의 핵심인 failure attribution과 모순된다.
- 수정 제안: `BC라면 공변량 이동이 가능한 설명이므로 실패 궤적·상태분포·ablation에서 확인하라`로 바꾼다. 실제 논문이 이를 분석했다면 그 표/절을 지목하고, 아니면 `해석 가설`로 표시한다.
- 근거 신뢰도: **본문 확인**, 논문의 실패 분석 여부는 **원 출처 확인 필요**.

### construction-011 — 순기구학의 입력을 “명령 관절각”으로 정의

- 우선순위: **P1 선수개념 문제**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/kindle-jaibot.md:32` — `Forward kinematics maps commanded joint angles to an end-effector pose`; 한국어 `:80` — `순기구학은 명령한 관절각을 말단 자세로 사상한다`.
- 문제: 순기구학은 관절 구성 (q)를 말단 자세로 사상한다. (q)가 명령값인지 엔코더 측정값인지는 별도 상태·구동 문제다. 하중 시 문제도 관절각 추종 오차뿐 아니라 링크/기구의 탄성 변형으로 rigid-link FK 자체가 실제 자세를 설명하지 못하는 데 있다. 초보자의 기구학과 제어 구분을 흐린다.
- 수정 제안: `순기구학은 주어진 관절 구성(보통 엔코더로 추정한 q)을 강체 모델의 말단 자세로 사상한다. 하중에서는 명령–실제 관절 오차와 구조 변형 때문에 이 모델 자세와 실제 공구 자세가 어긋난다`로 교체한다.
- 근거 신뢰도: **본문 확인**.

### construction-012 — worker-centered robotics를 “추정값이 로봇 행동을 바꾸는 경우”로만 정의

- 우선순위: **P2 범위 개선**
- 위치·인용: `content/05-construction-robotics/hrc-worker-centered.md:33-34` — `It becomes worker-centered robotics only when the estimate changes robot behavior`; `:46-49`도 같은 필요조건을 반복한다. 반면 상위 인덱스 `content/05-construction-robotics/index.md:39-41`은 외골격과 원격조작도 같은 스트림에 포함한다.
- 문제: 이 정의는 페이지가 다루려는 폐루프 적응형 HRC에는 유용하지만 worker-centered robotics 전체의 필요조건으로는 너무 좁다. 원격조작 인터페이스, 외골격, 참여설계, 설명/경고 인터페이스는 추론 상태가 행동을 바꾸지 않아도 작업자 중심 연구가 될 수 있다.
- 수정 제안: 페이지 도입부에서 `이 페이지의 핵심 하위범위: sensed-state-adaptive HRC`라고 선언한다. 문장은 `worker sensing이 closed-loop adaptive HRC가 되려면...`으로 바꾸고, worker-centered의 다른 갈래(teleop/interface, augmentation/exoskeleton)를 3줄짜리 분기표로 남긴다.
- 근거 신뢰도: **본문 확인**.

### construction-013 — 현장 인식 선수경로가 기초보다 SAM/Depth Anything을 필수처럼 앞세움

- 우선순위: **P2 학습경로 개선**
- 위치·인용: `content/05-construction-robotics/site-perception.md:21-25`의 선수 지식에 `SAM`, `Depth Anything`이 포함된다.
- 문제: 이 페이지의 핵심 질문은 좌표계, metric scale, 보정, SLAM, point-cloud/BIM 정합이다. SAM과 단안 깊이 모델은 §3의 선택 도구이지, scan-to-BIM이나 로봇 위치추정을 이해하는 선수조건이 아니다. ML 초보가 최신 모델 노트를 먼저 따라가다 기하 기반 핵심 경로를 놓칠 수 있다.
- 수정 제안: 필수 선수는 `기하 인식·보정`, `상태추정·SLAM`으로 두고, SAM/Depth Anything은 `선택: 학습 기반 proposal/depth를 쓰는 논문을 읽을 때`로 분리한다. `강체변환/좌표계 → 보정 → 정합 → 불확실성 → 선택적으로 foundation model` 순서 한 줄을 추가한다.
- 근거 신뢰도: **본문 확인**.

### construction-014 — 디지털 트윈 4단계를 보편적 표준처럼 제시

- 우선순위: **P2 개념 경계 개선**
- 위치·인용: `content/05-construction-robotics/digital-twin-workflows.md:46-55` — `Levels often called a digital twin` 표가 digital model → shadow → closed-loop twin → process-level twin을 단일 상승 사다리로 제시한다.
- 문제: model/shadow/twin의 데이터 흐름 구분은 널리 쓰이는 유용한 프레임이지만, `process-level twin`을 그 다음 보편 단계로 놓는 것은 이 위키의 분석 루브릭인지 특정 출처의 taxonomy인지 불명확하다. 초보자가 용어 논쟁과 저자별 정의 차이를 사실상의 표준 등급으로 오인할 수 있다.
- 수정 제안: 표 위에 `이 위키의 로봇 워크플로 판독용 합성 루브릭` 또는 채택한 원 출처를 명시한다. `높은 단계가 항상 더 좋은 것은 아니며, 연구 질문에 필요한 경로만 검증하면 된다`를 덧붙인다.
- 근거 신뢰도: **본문 확인**, taxonomy의 원류는 **추가검증 필요**.

### construction-015 — `as-built`를 `준공`으로 번역해 공사 중 상태와 혼동

- 우선순위: **P2 번역 개선**
- 위치·인용: `content/01-canonical-papers/notes/8-construction/lundeen-2019.md:40` — `준공(as-built) 기하`; 같은 노트는 `:42-49`에서 공사 중 감지·재계획을 설명한다.
- 문제: `준공`은 공사가 완료된 시점을 강하게 뜻한다. 여기서 as-built는 설계(as-designed)와 대비되는 “실제로 시공된/현재 시공 현황” 기하이며 공정 중에도 갱신된다. 디지털 트윈·공정 모니터링 맥락에서 시간 개념을 왜곡한다.
- 수정 제안: 최초 등장에 `실제 시공(as-built) 기하` 또는 `현재 시공 현황 기하`라고 쓰고, 이후 `실제 시공 기하`로 통일한다. `준공도면`을 뜻할 때만 준공을 쓴다.
- 근거 신뢰도: **본문 확인**.

### construction-016 — 선택적 연구 카드로 다음 원문·실습 필요를 진단할 수 있음

- 우선순위: **P3 선택 개선**
- 위치·인용: 예를 들어 `content/05-construction-robotics/earthmoving-heavy-machinery.md:17-21`은 `Designing excavation controllers is a working/mastery topic`이라고 하고, `:175-190`의 자기점검은 설명형 네 문항이다. 다른 Working 스트림도 유사하다.
- 관찰: 이는 필수 결함이 아니다. frontmatter가 `study-depth`와 `wiki-support`를 분리하고 있고, 개별 페이지도 원 논문·기초 교재 링크를 전제로 한다. 따라서 설명형 자기점검이 구현 능력의 충분조건일 필요는 없다. 다만 초보자가 다음 원문·실습에서 무엇을 보충할지 스스로 진단하는 선택적 장치가 있으면 전환이 더 명확해질 수 있다.
- 선택 제안: 필요한 독자에게만 논문 한 편과 선택 과제 한 개를 대상으로 `(1) 상태/관측/행동, (2) 고전·학습 블록, (3) 깨질 가정 하나, (4) baseline, (5) 독립변수·평가지표·실패 집계, (6) 증거 사다리 목표`를 적는 1쪽 연구 카드 템플릿을 제공한다. 카드는 Working의 관문·인증·충분조건이 아니며, 빈칸을 통해 다음에 읽을 원 논문·교재와 수행할 실습을 정하는 진단용이다.
- 근거 신뢰도: **본문 확인**.

### construction-017 — 랩 지도와 계보의 최상급 표현이 증거 기준 없이 연구실 순위처럼 읽힘

- 우선순위: **P3 선택 개선**
- 위치·인용: `content/05-construction-robotics/labs.md:19-22` — `the field's faculty-producing engine`; `:33` — `the strongest robot-learning lab`; `:112-114` — `defines the ... frontier/baseline`. 한국어 `:125-127, 138, 216-218`도 같다.
- 문제: 페이지 목적은 지형도인데, 최상급은 평가 기간·코퍼스·측정축 없이 순위 주장으로 읽힌다. 계보 페이지가 연구실 순위보다 질문 선택 도구가 되라고 한 취지와도 긴장한다.
- 수정 제안: `이 조사 코퍼스에서 확인된 교수 배출 사례가 가장 조밀한 클러스터`, `이 위키의 선택 경로와 직접 겹치는 그룹`처럼 관찰축과 범위를 문장 안에 넣는다. 유지할 최상급에는 표본·날짜·판정 기준을 각주로 단다.
- 근거 신뢰도: **본문 확인**, 실제 비교 우위는 **추가검증 필요**.

## 잘된 점

1. `content/05-construction-robotics/index.md:57-80, 125-147`의 논문 읽기 틀은 과제·신체·인식·표현·제어·인간·배치·실패·생산성을 한 장에 묶는다. 초보자가 “모델 이름과 성공률”만 읽는 습관을 교정하는 데 매우 효과적이다.
2. `earthmoving-heavy-machinery.md`, `assembly-fabrication.md`, `site-perception.md`, `digital-twin-workflows.md`는 각각 센스–플랜–컨트롤 또는 설계–실행–검증의 폐루프를 먼저 보여 주고, 학습이 어느 블록에 들어가는지 묻는다. 식을 장식으로 쓰지 않고 역할과 가정을 연결한다.
3. 생산성 계산(`earthmoving-heavy-machinery.md:161-164`), 오차 예산(`digital-twin-workflows.md:92-95`), LiDAR 각분해능(`site-perception.md:40-43`), 결합 포함률(`sim-to-real.md:144-147`)은 계산 결과보다 “무엇을 고정했고 무엇을 분모에 넣었는가”를 읽게 한다. 공업수학 배경의 초보자에게 적절한 수준이다.
4. 거의 모든 논문 노트가 testbed/site, 인간 역할, 수치의 범위, 후속 논문의 증거를 분리한다. 특히 ExACT와 ExT, HEAP과 AES를 같은 자율성으로 뭉개지 않는 점이 좋다.
5. 영문/국문은 대체로 동일한 주장과 경계를 유지한다. construction-002, construction-015처럼 명확한 예외는 있지만 구조적 번역 누락은 드물었다.
6. `construction-manipulation.md`의 과제–원시동작–센싱–제어–불확실성 표와 실험 사다리는 주제 선택을 기술 유행이 아니라 실패 기전과 증거 수준으로 바꾸는 강한 장치다. 다만 construction-004/006/007을 고쳐야 그 장치가 안전하게 작동한다.

## 권장 학습 경로(기존 범위 안에서)

새 과목을 늘리지 않고 다음 순서가 가장 자연스럽다.

1. `05-construction-robotics/index.md`의 읽기 틀과 `industry-deployment.md`로 주장·증거 어휘를 익힌다.
2. `lineage.md`는 역사적 위치만 잡고, 관심 스트림 하나를 선택한다. 랩 순위가 아니라 과제 실패를 기준으로 고른다.
3. 선택 스트림의 prerequisite 중 **필수 기초만** 먼저 읽는다. 현장 인식에서는 foundation model을 선택 사항으로 둔다(construction-013).
4. 앵커 노트 2~3개를 오래된 시스템 → 최신 학습 논문 순으로 읽으며 같은 읽기 틀을 채운다. 토공이면 Stentz → HEAP/AES → Egli/ExT, 조작이면 Feng → Lundeen → Apolinarska 또는 Liang/Yu가 적절하다.
5. 필요하면 construction-016의 1쪽 연구 카드를 선택적으로 작성해 부족한 원문 이해·구현·실험 항목을 찾는다. 카드 완성은 Working 판정이 아니며, 실제 도달 여부는 연결된 원 논문·교재 학습과 구현·변형·실험 수행으로 확인한다.

## 파일별 완독 장부

상태의 `양호`는 중대한 신규 발견이 없다는 뜻이며 원 논문 fact-check 완료를 뜻하지 않는다.

| 파일 | 상태 | 발견 ID |
|---|---|---|
| `content/05-construction-robotics/index.md` | 양호; 읽기 틀 우수 | construction-016(선택적 진단 보조) |
| `content/05-construction-robotics/assembly-fabrication.md` | 양호 | 없음 |
| `content/05-construction-robotics/construction-manipulation.md` | 개선 필요 | construction-004, 006, 007 |
| `content/05-construction-robotics/digital-twin-workflows.md` | 개선 권장 | construction-014 |
| `content/05-construction-robotics/earthmoving-heavy-machinery.md` | 개선 필요 | construction-005 |
| `content/05-construction-robotics/hrc-worker-centered.md` | 개선 권장 | construction-012 |
| `content/05-construction-robotics/industry-deployment.md` | 양호; 상업 주장 판독이 특히 좋음 | 없음 |
| `content/05-construction-robotics/labs.md` | 선택 개선 | construction-017 |
| `content/05-construction-robotics/lineage.md` | 대체로 양호; 연구기회 단정은 랩 지도와 함께 범위 표시 필요 | construction-017 |
| `content/05-construction-robotics/sim-to-real.md` | 개선 필요 | construction-003 |
| `content/05-construction-robotics/site-perception.md` | 개선 권장 | construction-013 |
| `content/01-canonical-papers/notes/8-construction/index.md` | 개선 권장 | construction-008 |
| `content/01-canonical-papers/notes/8-construction/aerial-am-2022.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/aes.md` | 개선 필요 | construction-002 |
| `content/01-canonical-papers/notes/8-construction/apolinarska-timber.md` | 양호; 전이와 현장 증거 구분 우수 | 없음 |
| `content/01-canonical-papers/notes/8-construction/bim-digital-twin.md` | 양호 | construction-014(상위 루브릭 의존) |
| `content/01-canonical-papers/notes/8-construction/bock-2015.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/cho-slam.md` | 양호; 페이월 한계를 정직하게 표시 | 없음 |
| `content/01-canonical-papers/notes/8-construction/davila-delgado-2019.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/dry-stone-wall.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/egli-rl.md` | 대체로 양호; all-soil 일반화를 제한함 | construction-005(상위 페이지 표현과 함께 정리) |
| `content/01-canonical-papers/notes/8-construction/exact-2024.md` | 양호; simulation-only 경계 명확 | 없음 |
| `content/01-canonical-papers/notes/8-construction/ext.md` | 양호; pretrained hardware와 fine-tuning simulation을 잘 분리 | 없음 |
| `content/01-canonical-papers/notes/8-construction/feng-rebar.md` | 개선 필요 | construction-006 |
| `content/01-canonical-papers/notes/8-construction/han-welding.md` | 개선 필요 | construction-001 |
| `content/01-canonical-papers/notes/8-construction/heap.md` | 개선 필요 | construction-005 |
| `content/01-canonical-papers/notes/8-construction/kindle-jaibot.md` | 개선 필요 | construction-011 |
| `content/01-canonical-papers/notes/8-construction/lasota-shah.md` | 개선 필요 | construction-009 |
| `content/01-canonical-papers/notes/8-construction/liang-hrc-survey.md` | 양호; 빈 범주를 공백 증명으로 보지 말라는 경고 우수 | 없음 |
| `content/01-canonical-papers/notes/8-construction/liang-lfd.md` | 개선 필요 | construction-010 |
| `content/01-canonical-papers/notes/8-construction/liu-jebelli-bci.md` | 양호 | construction-012(상위 범위 정의와 조화 필요) |
| `content/01-canonical-papers/notes/8-construction/lundeen-2019.md` | 번역 개선 | construction-015 |
| `content/01-canonical-papers/notes/8-construction/park-nl.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/stentz-excavator.md` | 양호 | 없음 |
| `content/01-canonical-papers/notes/8-construction/vision-guided-assembly.md` | 양호; 마커 가정을 명시함 | 없음 |
| `content/01-canonical-papers/notes/8-construction/wheel-loader-rl.md` | 양호; unknown material 범위를 잘 제한 | 없음 |
| `content/01-canonical-papers/notes/8-construction/yu-imitation.md` | 대체로 양호; VR–현실 간극 명확 | 없음 |

## 결론

이 범위는 초보자에게 **건설 Physical AI 연구 문해력**을 주는 데 성공적이다. 가장 강한 부분은 시스템 경계와 증거 사다리다. P1인 construction-001~006, 009~011을 먼저 고치면 사실·개념 오염을 막을 수 있다. 선택 스트림의 Working은 위키의 `study-depth` 목표와 `wiki-support` 범위를 구분한 채 원 논문·교재·실습을 병행해 도달해야 한다. construction-016의 연구 카드는 그 과정을 대체하거나 충분성을 판정하지 않고, 다음 학습·실습 필요를 찾는 선택적 보조로만 권한다.
