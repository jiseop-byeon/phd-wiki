# Foundations · Research Practice · Research Program 학습성 정독 감사

- 감사일: 2026-09-07
- 독자 가정: 공업수학 수강 경험은 있으나 ML/로봇 독학은 처음인 공대생
- 상태: **완료 — 범위 내 Markdown 25개 전부 처음부터 끝까지 정독. 콘텐츠 수정·배포·커밋 없음.**
- 판정 기준: P1 학습 차단/사실 문제, P2 유용한 개선, P3 선택 개선. 본문 내 수식·예제와 영문/국문을 함께 대조했다. 원 논문 전수 사실검증은 하지 않았으며, 니치한 최신 주장은 별도로 표시한다.

## 최종 판정

**Physical AI 연구 문해력에는 전반적으로 도달 가능하다.** 진입부의 “입력·출력 의미, 단위/shape, 가정 하나를 말하라”는 규칙, 선형대수의 사상 관점, 역전파의 VJP/shape 점검, 베이즈 기저율, 신호 처리 이력, 실험 단위·주장–증거 표·최초 실패 로그는 초보자가 용어를 외우는 대신 식과 실험의 역할을 묻게 만든다. 특히 선형대수, 공업수학, 연구 질문, 실험 설계, 실패 분석은 이 독자층에 맞는 강한 다리다.

**선택 영역의 Working은 조건부로 가능하다.** 페이지 자체가 Working을 실제로 제공하는 경우(ML 평가, 실험 설계, 실패 분석)와 어휘만 주거나 외부 교재·시뮬레이터를 요구하는 경우(0.7 신경망, 10 동역학)가 메타데이터에서 섞여 있다. 각 페이지의 `study-depth`와 `wiki-support` 계약을 맞추고, 선택 트랙별 prerequisite를 명시하면 경로가 성립한다. 지금 상태에서는 아래 P1, 특히 게이트 분모·DDPM 조건부성·LM/솔버·PPO·JND 해석을 교정하기 전에는 초보자가 잘못된 확신을 Working으로 가져갈 위험이 있다.

길이·수식 수는 깊이 판정 기준으로 쓰지 않았다. 원 논문 전수 검증도 하지 않았다. 본문 수식/언어판/내부 링크로 판정 가능한 것은 `본문 확인`, 사용자가 제공한 PPO 원문 근거는 `원 출처 확인`, 최신 도구·분야 부재·니치한 정리는 `추가검증 필요`로 구분했다.

## 발견

### foundations-001 — P1 · 전문화 안내가 현재 MR 요약 구조와 정면 충돌

- 위치/인용: `content/02-foundations/index.md:59-63` — “*Modern Robotics* chapter summaries stop at kinematics”; 한국어 `:118-121` — “*Modern Robotics* 챕터 요약이 기구학에서 멈추는 반면”.
- 문제: 실제 `content/04-robotics/modern-robotics/index.md:8-11`은 ch.2–6과 **8–13**을 다룬다고 명시하고, `ch08-dynamics.md:18-41`에는 운동방정식·순/역동역학·작업공간 버전까지 있다. 현재 문구는 10번 페이지의 존재 이유와 학습 경로를 구식 사실 위에 세운다.
- 제안: 해당 두 문장을 “MR 요약에도 ch.8 동역학은 있으나, 페이지 10은 조작 독자를 위해 ch.5·8·11의 핵심을 작업공간 관성/힘 제어까지 한 흐름으로 재구성한다”로 교체하고 실제 MR8·MR11 링크를 붙인다.
- 근거 신뢰도: **본문 확인**(연관 페이지의 실제 목차와 MR8 본문 확인).

### foundations-002 — P1 · “0–9가 모든 논문의 전체 선수지식”은 선택 트랙과 모순되고 범위가 과도함

- 위치/인용: `content/02-foundations/index.md:59-60` — “pages 0–9 remain the whole prerequisite for reading every paper in this wiki”; 한국어 `:118-119` — “모든 논문을 읽기 위한 선수 지식은 여전히 0~9번 전부”.
- 문제: 같은 절은 조작/힘 제어 독자에게 10번을 요구하고(`:65-68`), Overview의 누적 게이트도 10번 내용을 15번 문항으로 검사한다(`content/02-foundations/overview.md:207-209`). “모든 논문”은 개별 논문의 제어·역학·통계 선수지식을 보장하는 것으로 오독된다.
- 제안: “공통 **입문 지도**는 0–9이며, 개별 논문과 선택 경로는 각 페이지의 prerequisite box를 따른다. 조작/힘 제어 경로는 10번을 추가한다”로 한정한다.
- 근거 신뢰도: **본문 확인**.

### foundations-003 — P1 · 누적 게이트가 12문항이라면서 실제로는 15문항

- 위치/인용: `content/02-foundations/overview.md:164-168` — “Twelve questions… Nine or more means go”; 실제 목록은 `:170-209`의 1–15. 한국어도 `:400-438`에서 “열두 문항” 뒤 15개를 제시한다.
- 문제: 9/12(75%)인지 9/15(60%)인지 통과 기준이 달라지고, 13–15는 최적화·SE(3)·선택 10번을 추가해 공통 게이트의 범위 자체를 바꾼다.
- 제안: 공통 게이트 1–14와 선택 조작 문항 15를 분리하고 통과 기준을 분모와 함께 명시하거나, 15문항/예: 11개 이상으로 일관되게 재설계한다. 단순 숫자 교체 전 어떤 역량을 필수로 볼지 먼저 결정해야 한다.
- 근거 신뢰도: **본문 확인**.

### foundations-004 — P1 · DDPM 자가점검 해설이 조건부 분포의 전제를 잘못 설명

- 위치/인용: `content/02-foundations/probability.md:241-248` — “$\sqrt{\bar\alpha_t}x_0$ is an affine map of $x_0$ … By affine closure the first is Gaussian”; 한국어 `:475-482`도 동일.
- 문제: 일반 데이터 $x_0$는 가우시안이 아니다. 표준 DDPM의 주장은 **$x_0$를 고정한 조건부** $q(x_t\mid x_0)=\mathcal N(\sqrt{\bar\alpha_t}x_0,(1-\bar\alpha_t)I)$이다. 현재 해설은 데이터 분포의 아핀상이 가우시안이라고 가르친다.
- 제안: 질문에 “$x_0$에 조건부로”를 넣고, 해설을 “첫 항은 고정된 평균(결정론적 이동), 둘째만 가우시안 잡음이므로 조건부 합이 가우시안”으로 교체한다. 주변 §3에도 비특이 공분산일 때만 표시된 밀도식의 역행렬/행렬식이 유효하다는 한 문장을 추가하면 좋다.
- 근거 신뢰도: **본문 확인**(수식 자체로 판정).

### foundations-005 — P1 · LM이 ‘두 실패를 한 원인으로 동시에 고친다’는 설명이 랭크 결손과 모델 오차를 혼동

- 위치/인용: `content/02-foundations/optimization.md:121-156` — “exactly two failure modes”, “Both failures have one cause”, “$\lambda I$ fixes both failures at once”; 한국어 `:422-455` 동일.
- 문제: 랭크 결손은 식별 불가능/기하적 퇴화일 수 있어 “스텝이 아핀 모델 밖으로 감”과 같은 원인이 아니다. 감쇠는 선형계를 가역·안정하게 만들고 스텝을 줄이지만, 관측되지 않는 방향의 정보를 복원하거나 발산/지역최소를 일반적으로 해결하지 않는다.
- 제안: “두 대표 실패”로 낮추고, (a) 나쁜 국소모델에는 trust-region식 accept/reject가, (b) 작은 특이값에는 감쇠가 수치 폭발을 제한하지만 bias를 도입하며 관측가능성을 만들지는 않는다고 분리한다.
- 근거 신뢰도: **본문 확인**.

### foundations-006 — P1 · 솔버 이름만으로 LM 실행을 단정

- 위치/인용: `content/02-foundations/optimization.md:185-190` — “Ceres / g2o / GTSAM … told you it ran this algorithm”; 한국어 `:482-486` 동일.
- 문제: 이들은 최적화 프레임워크/라이브러리이며 Gauss–Newton, LM, Dogleg 등 설정이 가능하다. 초보자가 라이브러리와 알고리즘을 같은 것으로 학습하게 된다.
- 제안: “비선형 최소자승 계열을 썼다는 단서일 뿐, 실제 선형화·trust-region/line-search·선형 솔버·강건 손실 설정을 확인해야 한다”로 교체한다.
- 근거 신뢰도: **추가검증 필요**(공식 문서 확인 없이 라이브러리의 알려진 다중 알고리즘 성격으로 판정).

### foundations-007 — P1 · deadly triad의 ‘어떤 둘도 안전’은 보장으로 과장

- 위치/인용: `content/02-foundations/rl-basics.md:121-124` — “Any two of the three is safe”; 한국어 `:685-687` — “셋 중 둘까지는 안전하다.”
- 문제: deadly triad는 세 요소의 조합이 발산 위험의 대표 조건이라는 경고이지, 임의의 비선형 함수근사·옵티마이저에서 둘만 있으면 수렴한다는 정리가 아니다. 뒤의 “신경망 Sarsa도 안전”도 조건 없는 보장처럼 읽힌다.
- 제안: “고전적 표형/선형 근사와 정리의 조건 아래 특정 조합은 수렴 결과가 있지만, 신경망에서는 둘만으로 일반 안전 보장이 생기지 않는다”를 넣고 예시를 ‘triad 한 다리를 제거한 대표 완화’로 표현한다.
- 근거 신뢰도: **추가검증 필요**(정확한 수렴 정리의 가정은 원 교재/논문 확인 권장).

### foundations-008 — P1 · PPO가 배치를 ‘한 번 갱신 후 버린다’는 설명은 표준 PPO 절차와 불일치

- 위치/인용: `content/02-foundations/rl-basics.md:165-169` — “must throw away every batch after one update”; 한국어 `:723-726` 동일.
- 문제: PPO는 같은 rollout batch를 여러 minibatch epoch 동안 재사용하는 것이 핵심 실무다. 다만 새 정책으로 넘어간 뒤 오래된 rollout을 replay buffer처럼 지속 재사용하지 않는다는 뜻이어야 한다.
- 제안: “수집한 on-policy rollout을 보통 여러 epoch 재사용하되, 정책이 충분히 바뀌면 폐기하고 새 rollout을 수집한다; 장기 replay는 importance-ratio/신뢰영역 가정을 깨뜨린다”로 수정한다.
- 근거 신뢰도: **원 출처 확인**(PPO 공식 원 논문 초록이 수집 데이터에 대한 여러 epoch의 minibatch update를 명시함: https://arxiv.org/abs/1707.06347).

### foundations-009 — P2 · LoRA가 다른 adapter를 ‘밀어냈고 추론 비용이 없다’는 단정

- 위치/인용: `content/02-foundations/neural-network-basics.md:173` — “adds no inference cost, which is why it displaced the others”; 한국어 `:363` 동일.
- 문제: LoRA는 가중치 병합 시 추가 지연을 없앨 수 있지만, 동적 adapter 전환·양자화·서빙 방식에 따라 비용이 남을 수 있고 다른 adapter 계열도 사용된다.
- 제안: “추론 전에 병합 가능한 경우 추가 행렬곱 비용을 없앨 수 있어 널리 쓰인다”로 조건화한다.
- 근거 신뢰도: **추가검증 필요**.

### foundations-010 — P2 · 볼록 최적화와 실시간 MPC의 계산 보장이 너무 넓음

- 위치/인용: `content/02-foundations/optimization.md:45-46` — “polynomial-time reliable solvers exist”; `:288-290` — “solved in milliseconds… a thousand times a second”; 한국어 `:352-353`, `:579-581` 동일.
- 문제: 다항시간 주장은 표현/오라클·정확도·regularity 조건이 필요하고, MPC 시간은 문제 크기·희소성·하드웨어·solver/warm start에 따라 달라진다. 초보자가 convex=항상 빠름으로 오해할 수 있다.
- 제안: “많은 표준 유한차원 볼록 문제에는 전역해 보장과 효율적 솔버가 있다” 및 “작고 구조화된 QP는 적절한 구현에서 ms급도 가능하므로 deadline과 worst-case 시간을 보고한다”로 고친다.
- 근거 신뢰도: **본문 확인**.

### foundations-011 — P2 · 신호처리의 최적성/지연 문구에 적용 조건이 빠짐

- 위치/인용: `content/02-foundations/signal-processing.md:132-136` — “every causal low-pass delays… Kalman filter is the optimal time-varying filter”; 한국어 `:291-294` 동일.
- 문제: ‘지연’은 위상/군지연의 의미와 필터 부류를 밝혀야 하고, 칼만 최적성은 선형 모델·백색 잡음·정확한 공분산(가우시안이면 조건부 분포까지)에 의존한다.
- 제안: 해당 문장 뒤에 “선형-가우시안/정확한 모델에서 최소 MSE이며, 모델 불일치 시 보장되지 않는다”를 붙이고 causal smoothing의 위상 지연을 통과대역 기준으로 설명한다.
- 근거 신뢰도: **본문 확인**.

### foundations-012 — P2 · 최신 RL 대 모방 결론은 좁은 결과에서 분야 전체로 확대됨

- 위치/인용: `content/02-foundations/rl-basics.md:366-389` — “every one… human correcting”, “nobody has shown RL producing a generalist”, “RL is currently a finishing process”; 한국어 `:912-932` 동일.
- 문제: 특정 논문들의 과제·데이터 수집 규약을 유용하게 경고하지만, 보편 부정과 2024–26 분야 총평은 빠르게 변하고 정의(일반가, RL, 상호작용)가 불명확하다.
- 제안: 각 결과를 논문별 표(과제 수, 실기계 시간, 사람 개입, 보상 구성, baseline 조건)로 제한하고, 마지막을 “이 페이지가 다루는 접촉 정밀 사례들에서는…”로 좁힌다.
- 근거 신뢰도: **추가검증 필요**(사용자 요청에 따라 웹 검증 중단; 원 논문 대조 대상).

### foundations-013 — P1 · 0.7의 `Working` 계약과 본문의 읽기 전용 목표가 맞지 않음

- 위치/인용: `content/02-foundations/neural-network-basics.md:4-5` — `study-depth: Working`, “Use the notation, equations, and diagnostic ideas while reading methods and designing experiments”; 같은 파일 `:14-16` — “Read the words … Training your own models is not the goal here.”
- 문제: 본문은 20분짜리 어휘 입문으로 스스로 범위를 제한하는데, 메타데이터는 방법을 사용하고 실험을 설계하는 `Working`을 약속한다. `wiki-support`도 표시되지 않아 이 페이지 단독으로 Working을 제공하는지, 다른 실습 페이지가 보충하는지 알 수 없다. 문제는 코딩 과제를 강제하지 않았다는 데 있지 않고, 독자가 목표 달성 여부를 판단할 계약이 서로 다르다는 데 있다.
- 제안: 이 페이지의 `study-depth`를 `Literacy`로 낮추거나, `study-depth: Working`을 유지한다면 `wiki-support: Literacy`를 명시하고 depth-goal을 “ML 용어와 순전파/손실/역전파의 역할을 논문에서 식별한다”로 맞춘다. Working은 `ml-practice.md` 또는 선택한 모델의 기존 실습 경로에서 얻는다고 마지막 depth 안내에 한 문장으로 연결한다. 새 필수 코딩 과제를 추가할 필요는 없다.
- 근거 신뢰도: **본문 확인**.

### foundations-014 — P2 · SE(3)의 “모든 3·4수 표현은 불연속”은 필요한 위상적 조건이 생략됨

- 위치/인용: `content/02-foundations/se3-geometry.md:109-111` — “all 3- and 4-number representations are *discontinuous* as targets for neural networks”.
- 문제: 학습용 회전 표현의 연속성 결과는 표현/역표현의 연속성, 유클리드 출력공간, 전역 단일표현 같은 정의에 의존한다. 현재 문장은 axis–angle·quaternion의 제약과 double cover 설명을 바로 앞 표와도 구별하지 않아, 숫자 개수만으로 불연속이 결정된다고 오독하게 한다.
- 제안: “전역적으로 단일값이고 유클리드 공간에서 연속인 회귀 표적을 요구하면, SO(3)는 4차원 이하 표현에 위상적 장애가 있다”처럼 조건을 쓰고 6D가 그 회귀 문제를 피하는 방식임을 명시한다.
- 근거 신뢰도: **추가검증 필요**(연속 회전 표현 원 논문의 정확한 정의·정리 대조 필요).

### foundations-015 — P2 · pose estimation을 행렬 ‘회귀’와 동일시

- 위치/인용: `content/02-foundations/se3-geometry.md:190-191` — `"pose estimation" = regressing this matrix.`
- 문제: pose estimation은 $T\in SE(3)$를 추정하는 과제이며, 직접 회귀 외에도 대응점 기반 PnP, 최적화, 필터링, 확률분포 추정 등이 가능하다. 과제·출력과 해결 방법을 동일시하면 논문의 method 역할을 잘못 분류한다.
- 제안: “pose estimation은 이 $T$를 추정하는 과제다. 직접 행렬/회전 표현을 회귀할 수도 있고 기하 최적화나 대응점 풀이로 얻을 수도 있다”로 교체한다.
- 근거 신뢰도: **본문 확인**.

### foundations-016 — P2 · ML 학습 레시피의 영문·국문이 핵심 조건에서 어긋남

- 위치/인용: `content/02-foundations/ml-practice.md:179` — cosine decay가 “usually to ~10% of peak rather than to zero”; 한국어 `:374` — “그다음 0을 향한 cosine decay”. 또 영문 `:181`은 gradient accumulation이 per-example 분해 손실에서만 큰 배치를 재현하고 contrastive loss에는 안 된다고 설명하지만, 한국어 `:376`은 “큰 배치를 흉내”라고만 정의한다.
- 문제: 같은 독자가 언어에 따라 반대되는 최종 학습률과, 대조학습에서 가장 중요한 비동등성 여부를 다르게 배운다. 이는 재현 설정과 batch-size 주장을 읽는 능력에 직접 영향을 준다.
- 제안: 양쪽 모두 “최소 학습률은 레시피의 설정값이며 0 또는 비영 값일 수 있다”로 통일한다. 영문의 ‘보통 10%’도 독립 검증 없이 표준으로 승격하지 않는다. gradient accumulation에는 “예제별 분해 손실·같은 optimizer step 등 필요한 조건에서 큰 배치와 대응하며, 대조 손실의 negatives·배치 통계·확률 연산까지 항상 같지는 않다”는 단서를 양언어로 붙인다. warmup의 ‘아예 학습되지 않는다’도 영문의 특정 post-norm 사례로 한정한다.
- 근거 신뢰도: **본문 확인**(언어판 직접 대조; 수치·빈도 일반화는 **추가검증 필요**).

### foundations-017 — P1 · 동역학 파라미터를 sim-to-real 실패의 보편적 주원인으로 단정

- 위치/인용: `content/02-foundations/manipulator-kinematics-dynamics.md:282-285` — “**This equation is the sim-to-real gap.** … the mismatch is usually not in the perception”; 한국어 `:595-597` — “**이 방정식이 곧 sim-to-real 격차다.** … 불일치는 대개 인식이 아니라 이 파라미터들에 있다.”
- 문제: 조작 sim-to-real 실패는 시각·촉각 관측, 지연, 제어 인터페이스, 접촉/마찰, 액추에이터, 과제 분포가 함께 만들 수 있다. 동역학 페이지의 중요한 메시지를 전체 분야의 원인 순위로 확대해, 실패 분석에서 인식 가설을 성급히 배제하게 한다.
- 제안: §7의 세 번째 항을 “이 파라미터 불일치는 **동역학 쪽의 주요 sim-to-real 원인 중 하나**다. 어떤 층이 지배적인지는 동기화 로그와 절제로 분리한다”로 바꾸고 `failure-analysis-system-evaluation.md`의 최초 실패 절로 연결한다.
- 근거 신뢰도: **본문 확인**(같은 감사 범위의 다층 실패 분석과도 충돌); 원인 빈도 순위는 **추가검증 필요**.

### foundations-018 — P2 · 위치 명령 로봇의 컴플라이언스 주장을 ‘대부분 무의미’로 처리

- 위치/인용: `content/02-foundations/manipulator-kinematics-dynamics.md:296-299` — “Most claims about compliance are meaningless in the second case”; 한국어 `:607-610` 동일 취지.
- 문제: 외부 힘 루프·어드미턴스 제어도 벤더 위치 루프의 대역폭·강성·지연을 포함해 유효한 시스템 주장을 할 수 있다. 자가점검 답(`:341`, 한국어 `:652`)은 바로 이 조건부 가능성을 더 정확히 설명하므로 본문과 톤이 어긋난다.
- 제안: 질문 항목을 “위치 인터페이스라면 내측 루프의 강성·대역폭·지연과 환경 강성을 포함한 **전체 폐루프**에서 컴플라이언스 주장을 평가해야 한다”로 교체한다.
- 근거 신뢰도: **본문 확인**.

### foundations-019 — P2 · peer-review 계산 예제의 한국어판에 출처 없는 실험 조건이 추가됨

- 위치/인용: `content/06-research-practice/scientific-writing-peer-review.md:143-148`은 장면당 `17/20, 16/20, 16/20`과 이항 SE만 제시하지만, 한국어 `:333-338`은 추가로 “(각 20회, 시드 3개 ±1 std)”를 삽입한다.
- 문제: 시행 20회와 시드 3개의 계층·집계 관계가 정의되지 않았고 `±1 std`의 대상도 없다. 재현 가능한 응답문을 가르치는 예제가 언어에 따라 다른 설계를 보고한다.
- 제안: 한국어의 추가 괄호를 삭제해 영문과 맞추거나, 양쪽 모두에 “각 시드당/전체 몇 회인지, SE가 어떤 단위에서 계산됐는지”를 명시한다. “5%p 차이가 잡음 안”도 검정 결론 대신 “이 표본만으로 장면 차이를 분리하기 어렵다”로 쓴다.
- 근거 신뢰도: **본문 확인**.

### foundations-020 — P1 · 저널 확장 정책을 ‘추가 실험은 확장이 아니다’로 과도하게 축약

- 위치/인용: `content/06-research-practice/venue-strategy.md:188-196` — 원 정책 요약은 “mere extension”과 “additional experiments”만으로는 부족하다고 한 뒤 “**More experiments is not an extension**”이라 결론 낸다; 한국어 `:448-455` — “**실험을 더 하는 것은 확장이 아니다.**”
- 문제: 본문 자체가 인용한 기준은 ‘추가 실험이라는 형식’의 금지가 아니라 실질적 새 결과·의의의 부재다. 새 연구 질문과 실질적 결과를 만드는 실험까지 불가능하다고 오독하면 학생의 제출 전략을 잘못 제한한다.
- 제안: 굵은 문장을 “**같은 주장을 뒷받침하는 실험을 더하는 것만으로는 실질적 확장이 아니다.** 새 질문·방법·결과의 연구 의의를 목표 저널 지침에 맞춰 설명해야 한다”로 바꾼다.
- 근거 신뢰도: **본문 확인**(페이지가 바로 위에 옮긴 정책 문구와 결론의 범위 비교); 정책의 최신성은 행동 전 **추가검증 필요**.

### foundations-021 — P2 · 임팩트 ‘사다리’가 독립 사용과 현장 현실성을 한 축에 놓고 한국어에서는 단서도 누락

- 위치/인용: `content/06-research-practice/real-world-impact.md:62-69` — 영문 SVG는 “used by someone else sits on a different axis”라고 단서를 달면서도 곧 이를 “top rung”, “strongest impact evidence”라 한다. 한국어 SVG `:253-259`에는 다른 축이라는 문장이 없고 그대로 “맨 위 단계”라 한다.
- 문제: 다른 연구실의 시뮬레이션 재현과 단 한 번의 실제 현장 운용은 서로 다른 질문에 답해 완전한 서열이 아니다. 한국어 독자는 저자가 알고 있는 2축 구조조차 보지 못한다.
- 제안: 선형 사다리를 (a) 환경 현실성: sim→lab→mock-up→site, (b) 독립성/채택: 자체 실행→독립 재현→독립 사용의 2축 표로 바꾸거나, 최소한 한국어에도 동일 단서를 번역하고 ‘최상단’ 표현을 제거한다.
- 근거 신뢰도: **본문 확인**.

### foundations-022 — P2 · ‘존재하지 않는다’는 핵심 연구 공백에 재검증 가능한 검색 경계가 부족

- 위치/인용: `content/06-research-practice/simulators-benchmarks-datasets.md:134-145` — “No simulator has a documented model…”, `:193-199` — “no benchmark…”, `:316-335` — “No shared dataset…”; 한국어 `:552-562`, `:608-613`, `:720-738` 동일.
- 문제: 도구 선택에는 매우 유용한 결론이지만, 부재 주장은 데이터베이스·검색어·포함 기준에 따라 바뀐다. 출처 절의 “official pages were checked”만으로는 후속 독자가 공백을 재검증하거나 새 반례를 판정하기 어렵다.
- 제안: §5–§8 앞에 작은 ‘부재 판정 범위’ 상자(검색일, 확인한 공식 카탈로그/논문 DB, `shared`·`on-site`·`contact-rich`의 포함 기준, 알려진 근접 반례)를 둔다. 새 과목을 늘리지 않고 현재 조사 결과의 경계만 보존한다.
- 근거 신뢰도: **추가검증 필요**(본문은 2026-08-22 확인을 주장하나 이번 감사에서 외부 전수 검색하지 않음).

### foundations-023 — P2 · JND를 계산할 과제·관례가 불명확

- 위치/인용: `content/06-research-practice/psychophysics-human-measurement.md:60-65` — “the JND read between the 25% and 75% points”; 한국어 `:286-290` — “JND는 25%와 75% 지점 사이에서 읽는다.”
- 문제: ‘사이에서 읽는다’는 표현만으로 저자가 두 점의 차이 전체를 JND로 정의했다고 확정할 수는 없다. 다만 과제와 계산 관례가 없어서 초보자가 직접 수치를 계산하기 어렵다. 강제선택 과제의 정답률과 비교 과제의 응답비율도 같은 축이 아니다.
- 제안: 채택한 비교 과제·응답곡선·JND 관례를 먼저 명시한다. 예를 들어 대칭적인 비교 응답곡선과 반사분위 범위 관례를 가정한다면 $x_{25}=0.8$, $x_{75}=1.2$에서 JND=$(1.2-0.8)/2=0.2$를 보일 수 있다. 이 식을 yes/no detection이나 모든 2AFC의 보편 정의로 쓰지 않는다.
- 근거 신뢰도: **추가검증 필요**(절차별 정의를 표준 심리물리 교재와 대조 필요; 본문의 산술 규칙 누락은 본문 확인).

### foundations-024 — P1 · 지각 JND를 운동 의도·생성 능력의 경계로 전용

- 위치/인용: `content/06-research-practice/psychophysics-human-measurement.md:108-115` — variation below what the operator perceives “is not intent; it is noise”, “under ~0.14 N cannot be attributed to deliberate modulation”; 한국어 `:325-333` 동일.
- 문제: JND는 특정 조건에서 두 자극을 **변별**하는 능력을 재는 값이지, 시각 단서·피드포워드 운동·학습된 제어로 더 작은 힘 변화를 의도적으로 생성할 수 없다는 경계가 아니다. 떨림/마찰과 의도를 가르는 데는 명령·과제 사건·반복성·별도 조작 검증이 필요하다. 바로 뒤 `:117-119`의 단서는 앞의 절대 결론을 충분히 회수하지 못한다.
- 제안: 첫 문장을 “JND 아래 변동만으로는 촉각적으로 유도된 의도를 **입증할 수 없다**”로 낮추고, 0.14 N은 배제 기준이 아니라 screening reference라고 표시한다. 이어 현재 §4 후반의 동기화 명령/사건 비교를 필수 판정 절차로 올린다.
- 근거 신뢰도: **본문 확인**(측정 construct와 결론 construct의 불일치); 정량 역치는 과제·장치별 **추가검증 필요**.

### foundations-025 — P2 · 연구 프로그램의 HRI 선수 경로가 사람 측정 전용 페이지를 누락

- 위치/인용: `content/07-research-program/index.md:163`은 HRI의 Foundation을 `ML Practice (study design and statistics)` 하나로 두고, Paper 1도 `content/07-research-program/paper-arc.md:78`에서 ML Practice만 “study design and error bars”로 연결한다.
- 문제: 같은 감사 범위의 `psychophysics-human-measurement.md:15-19`는 자신을 ‘측정 대상이 사람인 특수 사례’의 도구함으로 정의한다. Paper 1이 worker perception/intent/HRI를 다루는데 이 링크가 빠져 독자가 ML seed·trial 통계를 사람 대상 측정에 그대로 적용할 수 있다.
- 제안: Research Program §6 HRI 행과 Paper Arc 1편의 “Leans on”에 `Experimental Design` 및, 지각/인터페이스 주장을 할 때 선택적으로 `Psychophysics & Human Measurement`를 추가한다. 전 HRI 프로젝트의 필수 신규 과목으로 만들지 말고 주장 유형에 따라 조건화한다.
- 근거 신뢰도: **본문 확인**.

## 읽은 파일 전체 목록과 상태

| 파일 | 상태 | 발견 ID |
|---|---|---|
| `content/02-foundations/index.md` | 완료·경로/사실 문제 | foundations-001, 002 |
| `content/02-foundations/overview.md` | 완료·게이트 불일치 | foundations-003 |
| `content/02-foundations/engineering-math.md` | 완료·대체로 양호 | — |
| `content/02-foundations/neural-network-basics.md` | 완료·깊이 계약/부분 과장 | foundations-009, 013 |
| `content/02-foundations/linear-algebra.md` | 완료·대체로 양호 | — |
| `content/02-foundations/calculus-backprop.md` | 완료·대체로 양호 | — |
| `content/02-foundations/probability.md` | 완료·자가점검 사실 오류 | foundations-004 |
| `content/02-foundations/optimization.md` | 완료·조건/솔버 과장 | foundations-005, 006, 010 |
| `content/02-foundations/information-theory.md` | 완료·대체로 양호 | — |
| `content/02-foundations/signal-processing.md` | 완료·조건 보강 필요 | foundations-011 |
| `content/02-foundations/rl-basics.md` | 완료·수렴/실무/최신 주장 문제 | foundations-007, 008, 012 |
| `content/02-foundations/se3-geometry.md` | 완료·표현 정리 조건/과제-방법 구별 필요 | foundations-014, 015 |
| `content/02-foundations/ml-practice.md` | 완료·영문/국문 핵심 불일치 | foundations-016 |
| `content/02-foundations/manipulator-kinematics-dynamics.md` | 완료·동역학 다리는 강함, 범위 과장 | foundations-017, 018 |
| `content/06-research-practice/index.md` | 완료·순서와 역할 구분 양호 | — |
| `content/06-research-practice/research-questions-claims.md` | 완료·질문→주장→증거 연결 우수 | — |
| `content/06-research-practice/experimental-design-reproducibility.md` | 완료·실험 단위/불확실성/산출물 우수 | — |
| `content/06-research-practice/failure-analysis-system-evaluation.md` | 완료·최초 실패/전파/노출 구분 우수 | — |
| `content/06-research-practice/scientific-writing-peer-review.md` | 완료·언어판 예제 불일치 | foundations-019 |
| `content/06-research-practice/venue-strategy.md` | 완료·운영 정보 유용, 정책 결론 과도 | foundations-020 |
| `content/06-research-practice/real-world-impact.md` | 완료·주장 경계 유용, 사다리 축 혼합 | foundations-021 |
| `content/06-research-practice/simulators-benchmarks-datasets.md` | 완료·도구의 부재/한계 지도 강함 | foundations-022 |
| `content/06-research-practice/psychophysics-human-measurement.md` | 완료·선택 경로 가치 높으나 JND 오용 | foundations-023, 024 |
| `content/07-research-program/index.md` | 완료·범위 통제 명료, HRI 경로 누락 | foundations-025 |
| `content/07-research-program/paper-arc.md` | 완료·의존/미룸 구조와 실패 신호 양호 | foundations-025 |

## 만족한 부분

- `engineering-math.md`, `linear-algebra.md`, `calculus-backprop.md`는 공업수학 경험을 논문 독법으로 전환한다. 행렬 곱 순서·shape, 잔차의 기하, transpose와 inverse 구분, 분기 그래디언트 합은 초보자가 실제 수식을 점검할 수 있는 수준이다.
- `probability.md`의 기저율 예제, `information-theory.md`의 KL/ELBO 역할 분리, `signal-processing.md`의 aliasing·타임스탬프·필터 이력은 용어 정의에서 측정 가정까지 이어진다. DDPM 해설 한 곳을 고치면 좋은 축이다.
- `manipulator-kinematics-dynamics.md`의 2R 질량행렬과 $\Lambda=(JM^{-1}J^\top)^{-1}$ 계산은 식의 물리 역할을 수치로 연결하며, `wiki-support: Working`과 외부 Mastery 경계를 명시한 점도 모범적이다.
- Research Practice의 연구 질문→실험 단위/비교→최초 실패/전파→글쓰기 흐름은 실제 방법·실험·가정 문해력을 만든다. 특히 “프레임 수≠독립 시행 수”, oracle의 역할, 개입/리셋 분리, 결과와 기전 해석 분리는 바로 적용 가능한 Working 수준이다.
- Research Program은 세 기둥을 동등한 전공으로 만들지 않고 조작 중심으로 제한하며, 각 논문이 무엇에 기대고 무엇을 미루는지 적게 한다. 고정 커리큘럼이 아니라 첫 baseline/실패 뒤 수정하는 결정 기록이라고 밝힌 점이 과도한 과목 확장을 막는다.

## 우선 수정 순서

1. 학습 경로 계약: foundations-001~003, 013, 025.
2. 직접 오개념을 만드는 문장/해설: foundations-004~008, 017, 020, 024.
3. 적용 조건·언어판 정렬: foundations-009~012, 014~016, 018, 019, 021~023.
