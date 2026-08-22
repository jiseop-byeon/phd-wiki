---
title: 9. Study Log
tags: [log]
---

무엇을 읽고 공부했는지 기록하는 일지. 일주일에 한 번이라도 좋으니 꾸준히 남긴다.
나중에 다시 보면 "그때 내가 뭘 몰랐는지"가 보여서 복습 지점을 찾기 좋다.

## 2026-08

### 2026-08-21 (4) 촉각·파지·건설 조작, 그리고 Radar 3배 확장

**[[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱]].** 촉각을 쓰는 근거를 "비전보다
풍부해서"가 아니라 **결정적 변수가 접촉 안에 있어서**로 좁혔다. 제대로 물린 볼트와 나사산이
어긋난 볼트는 파지 바깥에서 똑같아 보이고, 기대어 있는 패널과 안착한 패널은 카메라 깊이
잡음보다 작은 차이다. 센서는 변환 원리가 아니라 **무엇을 출력하는가**로 묶었다 — 손목 F/T는
정직한 뉴턴이지만 어디서 왔는지 모르고, 광학 촉각(GelSight·DIGIT)은 **기하를 재고 힘은
추론한다**. 13번의 시간 규모와 이어 붙이면 결론이 하나 나온다: 광학 촉각은 카메라 주기로
도는데 단단한 접촉 천이는 1~2 ms에 끝나므로, **촉각은 충격에서 살아남는 기제가 아니라 다음에
무엇을 할지 정하는 기제다.** 폐루프 힘 조절에 쓴다는 논문은 훨씬 강한 하드웨어 주장을 하는 것.

**[[04-robotics/grasping|15. 파지]].** 마찰 원뿔 → antipodal 조건 → closure → $\epsilon$ 지표 →
그 이론이 학습 파이프라인의 **라벨 생성기**로 옮겨간 경위. 검증에서 **널리 퍼진 오류 하나를
잡았다**: 3D에서 마찰 있는 force closure는 손가락 **넷**(Markenscoff·Ni·Papadimitriou 1990이
자기 초록에서 말한다)이고, 흔히 인용되는 **일곱**은 *마찰 없는 form closure* 개수다. 둘은 다른
정리인데 2차 출처가 어김없이 뒤섞는다. Ferrari & Canny도 1992년인데 *Springer Handbook*의
참고문헌이 1986으로 잘못 적고 있다. 건설과의 접점은 §6: **$\mu$는 §2~§4 전체의 입력인데 현장에서
아무도 그것을 재지 않는다.** 0.6을 가정한 계획기가 실제 0.3인 표면에서는 자기가 가졌다고 믿는
원뿔의 절반만 가진 것이다.

**[[05-construction-robotics/construction-manipulation|9. 건설 매니퓰레이션]]** — 이 위키의 고유
교차점. 건설 작업 10개를 조작 원시동작·결정적 센싱·제어 모드·가장 어려운 불확실성으로 분해했다.
조적과 대부분의 놓기 작업이 **접촉이 많지 않다**고 말하는 것도 요점의 일부다.

그리고 이 페이지가 만들어진 이유가 된 발견: 드릴링·드라이월·철근·파사드·목재·용접을 겨냥해
찾아본 결과, **가동 중인 건설 현장에 매니퓰레이터를 올린 논문이 둘뿐**이다 — Feng 등(2024,
철근 결속, 선양 훈난 4기)과 Yu 등(2007, 커튼월). 나머지는 전부 실험실이나 목업이고, "on-site"를
제목에 단 여러 논문이 본문에서는 통제된 실험실이라고 밝힌다. 가장 강한 천장 드릴링 결과조차
실제 현장 실증이 향후 과제라고 말한다. 이것을 기회로 읽되 단계를 건너뛸 허가로 읽지 않는 것이
이 페이지의 결론이다. 함정 둘도 기록했다: **보도 시연이 결과로 인용되는 것**(드라이월 휴머노이드의
심사 논문은 *관절 설계*에 관한 것이고 드라이월 시연은 보도 영상이다)과 **상용 시스템에는 논문이
없다는 것**(Jaibot·TyBot·Canvas·Okibo의 생산성 수치는 마케팅이다).

**[[02-foundations/rl-basics|RL 기초 §6]]에 정량 논증 추가.** 별도의 모방학습 페이지를 만들려다
그만두었다 — §6이 이미 BC·공변량 이동·DAgger·다봉성·행동 청킹·오프라인 RL을 다 다루고 있어서
중복 페이지는 이 위키가 이미 겪은 표류(교훈 2번)를 다시 부를 뿐이었다. 대신 빠져 있던 숫자를
넣었다: 스텝당 오류율 $\epsilon$이면 $T$스텝 과제가 $(1-\epsilon)^T$로 살아남으므로,
**100스텝에 1번 틀리는 정책이 50스텝 과제는 60%, 500스텝 과제는 0.7%로만 깨끗하게 끝낸다.**
독립 가정은 정리가 아니라 예시라고 명시하고, 실제 정리(Ross 등 2011: BC는 $O(\epsilon T^2)$,
DAgger는 $O(\epsilon T)$)를 옆에 붙였다. 행동 청킹이 이 곡선의 지평 축을 왼쪽으로 되돌리는
싼 방법이라는 것도.

**Research Radar 확장.** IROS·RSS·RA-L·T-RO를 추가했다. **로보틱스 커버리지가 7,846 → 23,604편
(3.0배), 전체가 58,439 → 76,701편.** 작업 중 스크립트 버그 둘을 고쳤다: DBLP가 NeurIPS 파일을
`nips{연도}`에서 `neurips{연도}`로 개명해서 **5년치가 통째로 404였고**(다음 재빌드 때 조용히
사라졌을 것이다), 끊긴 연결(`RemoteDisconnected`)이 재시도 예외에 안 잡혀 페치 전체가 크래시했다.
Radar 페이지의 "IROS·RSS·RA-L·T-RO는 아직 색인되지 않았다"는 경고도 사실이 아니게 되어 고쳤고,
**재빌드 이전 값과 이후 값을 비교하지 말라**는 경고로 대체했다.

용어집 179항목(+10: antipodal, 마찰 원뿔, grasp wrench space, 초기 미끄러짐, 접촉 상태 추정,
RCC, 선택 행렬, 택셀, visuotactile, wedging/jamming).

### 2026-08-21 (3) 힘·컴플라이언스 제어 — 매니퓰레이션 트랙의 기여 층

[[04-robotics/force-compliance-control|13. 힘·컴플라이언스 제어]]. 기초 10번과 함께 Mastery로
올린 쌍이다. 접촉 다량 조작의 모든 주장이 결국 이 제어기들 중 하나에 관한 주장이기 때문이다.

이 페이지에서 실제로 배운 것 셋:

- **뻣뻣한 로봇이야말로 단단한 벽을 감당하지 못한다.** 소박한 예상과 정반대다. 어드미턴스
  제어(힘을 재고, 뻣뻣한 내부 위치 루프에 운동을 명령)는 무른 환경에 맞고, 임피던스 제어(운동을
  재고 힘을 명령, 역구동 가능한 팔 필요)가 단단한 환경에 맞는다. 강판에서 마이크로미터의 운동이
  큰 힘을 만들면 어드미턴스의 실효 루프 게인이 폭발하고 지연이 그것을 진동으로 바꾼다. **논문
  읽기에 직접 쓰이는 결론**: 손목 힘 센서를 단 산업용 팔의 "힘 제어"는 어드미턴스이고, 벤더의
  위치 루프가 환경과 직렬로 끼어 있으므로 폼에서 보인 결과는 강철에 대해 아무것도 말하지 않는다.
- **접촉 천이의 산수가 이 페이지의 중심이다.** $\Lambda = 2$ kg가 $v = 5$ cm/s로 강성 $K$인
  면을 만나면 $F_{\max} = v\sqrt{\Lambda K}$, $t = \pi\sqrt{\Lambda/K}$다. 맨 공구가 단단한
  구조물($10^7$ N/m)에 닿으면 **224 N이 1.4 ms 만에** 지나가고, 1 kHz 제어기는 그중 샘플 하나를
  — 그마저 정점 뒤에 — 본다. 어떤 제어 법칙도 이것을 고치지 못한다. 정보가 사건 뒤에 오기
  때문이다. 유연 손목($10^4$ N/m)을 직렬로 넣으면 **7.1 N이 44 ms에 걸쳐** 오고 샘플 44개가
  들어온다. 힘과 지속 시간이 **둘 다 $\sqrt{K}$로 가므로** 1000배 무르게 하면 각각 정확히
  $\sqrt{1000} \approx 32$배를 산다. 그래서 **수동 컴플라이언스는 능동 제어의 값싼 대체품이
  아니라 접촉 대역폭에서 작동하는 유일한 것**이다.
- **학습된 정책이 앉는 자리가 이 산수에서 곧바로 나온다.** 정책은 어떤 컴플라이언스를 요구할지를
  10~50 Hz에서 고르고, 고전 제어기가 500~1000 Hz에서 실현하고, 수동 컴플라이언스가 아무도
  샘플링할 수 없는 그 밀리초를 맡는다. 뻣뻣한 벤더 루프에 위치를 내보내는 정책은 세 층 모두에서
  빠져나온 것이다 — 그래서 조작 정책 논문에서 **행동 공간을 가장 먼저 확인해야 한다.**

Mason의 자연/인공 제약(같은 방향에서 위치와 힘을 동시에 제어할 수 없는 이유), Raibert & Craig의
선택 행렬, Khatib의 작업 공간 제어(여유 자유도 해소가 영공간 투영이 되는 것 — 사람이 있는 현장에서
이것은 덤이 아니라 기제다), Whitney의 wedging/jamming과 RCC, Colgate & Hogan의 수동성 조건(제어기가
안정하게 구현할 수 있는 강성에 **한계가 있다**)까지.

**인용 검증에서 내 기억이 틀린 것을 하나 잡았다**: Raibert & Craig 1981은 ASME JDSMC **vol. 103**
이지 102가 아니다(102가 2차 서지에 널리 퍼져 있다). Khatib은 "IEEE Journal **on** Robotics and
Automation"이고 "of"가 아니다 — 기초 10번의 인용도 권·호·쪽까지 보강했다. RCC 자체의 정본
출처(Drake 1977 학위논문, Whitney & Nevins 1979)는 DOI 시대 이전이라 **확인하지 못했고**, 그
사실을 페이지에 명시해 두었다.

**그림에서 새로 배운 실수**: 2차 베지에의 실제 정점은 제어점이 아니라 **양 끝점과 제어점의
가중 평균**(끝점 0.25씩 + 제어점 0.5)이다. 제어점을 y=44에 두고 라벨을 그 높이에 붙였더니 곡선은
y=97까지밖에 안 올라와 라벨이 허공에 떠 있었다. 3차 베지에로 바꾸고(끝점 0.125씩 + 제어점 0.375씩)
정점을 역산해서 다시 그렸다. 접촉 그림은 아예 **두 축 모두 실제 비례**로 다시 그렸다 — 바늘 같은
스파이크와, 같은 힘 축에서 거의 보이지 않는 넓은 봉우리, 그 아래 1 kHz 눈금자. 논증이 그림 자체가
되었다.

### 2026-08-21 (2) 전문화 층 첫 페이지: 원격조작

전수 조사에서 가장 큰 공백이었던 항목 — 코퍼스 16개 파일이 원격조작을 *언급*하는데 전용 절이
**0개**였다 — 을 채웠다. [[04-robotics/teleoperation-demonstration|12. 원격조작과 시연 수집]].

핵심 재프레이밍은 노트 §7의 것이다: **원격조작은 데이터 생성 도구다.** 그러면 평가 기준이
바뀐다 — 사람이 로봇을 얼마나 잘 모는가가 아니라, 만들어낸 데이터의 품질·양·비용, 그리고
사람이 손을 놓았을 때 그 데이터로 학습한 정책이 작동하는가. 조작자에게 아름다운 힘 피드백을
주지만 세션마다 10분 셋업이 필요한 인터페이스는, 하루에 에피소드 천 개를 모으는 조잡한
인터페이스에 진다.

기술적으로 이 페이지가 실제로 가르치는 것:
- **2포트 모델과 투명성.** 조작자가 느끼는 임피던스 = 팔로워가 닿는 환경의 임피던스. Lawrence의
  4채널 분석(1993)이 이것을 직관에서 설계 목표로 바꾸었고, 동시에 이 분야의 근본적 트레이드오프
  — 투명성 대 견고한 안정성 — 를 지명한다. 둘 중 하나만 보고하는 논문은 결과의 절반만 보고한 것.
- **지연이 왜 "그냥 느린 것"이 아닌가.** 스프링·질량·감쇠기는 전부 수동적이라 연결해도 안정한데,
  지연이 그 수동성을 깬다: $T$초 전 위치로 계산된 힘이 그사이 움직인 리더에 가해지면서 시스템
  *안으로* 에너지를 넣는다. 그래서 게인을 낮추는 것이 해결책이 아니다. Niemeyer & Slotine(1991)의
  wave variable이 구조적 처방이다 — 일률이 $\tfrac12(u^2-v^2)$가 되어 채널이 저장만 할 뿐
  만들어내지 못하므로 임의의 상수 지연에서 수동적이다. 대가는 투명성이고, 그래서 §2의
  트레이드오프가 튜닝 손잡이가 아니라 정리의 형태로 되돌아온다.
- **인터페이스 스펙트럼**을 충실도 대 시간당 수집 비용 두 축에 배치했다. 기구학이 같은 리더 암이
  왜 두 문제를 한꺼번에 없애는지(역기구학 + 리타게팅), 휴대형 그리퍼가 무엇을 대가로 치르는지
  (embodiment 격차)를 그 축 위에서 읽는다.
- **리타게팅**이 시연을 조용히 비현실적으로 만드는 지점이라는 점. 사상이 사람으로 하여금 로봇이
  작업 공간 가장자리에서만 닿는 자세를 명령하게 두면 데이터셋이 특이점 근처로 가득 차고 정책이
  그것을 물려받는다 — MR 5장의 가조작성 점검은 분석이 아니라 수집 파이프라인 안에 있어야 한다.
- **좋은 시연 데이터**의 네 축(조작자 숙련도와 일관성, 다봉성, 복구의 포함 여부, 상태-행동
  일관성)과 논문에서 뽑아낼 일곱 항목.

**인용은 전부 1차 출처로 검증했다.** 아홉 건의 추정이 모두 맞았지만 함정 둘을 찾았다:
(1) Niemeyer & Slotine의 실제 제목은 "Stable adaptive teleoperation"이고 "wave variables"가
아니며, 일부 서지가 *IEEE Trans. Automatic Control*로 잘못 분류한다(실제로는 *IEEE J. Oceanic
Engineering* 16(1):152–162). (2) **ALOHA·GELLO·Mobile ALOHA·UMI는 전부 제목이나 평판에
"low-cost"를 달고 있지만 어느 것도 초록에 가격을 적지 않는다** — 떠도는 금액은 본문·프로젝트
사이트·언론에서 온 것이므로, 인용하려면 그 출처를 명시해야 한다. 페이지에 경고 박스로 남겼다.

용어집 +14(동역학 6 + 원격조작 7 + 혼동 쌍 1), 총 169항목. 정렬 규칙(대소문자 무시 알파벳순)이
삽입으로 깨졌던 것을 절별 재정렬로 복구했다 — 기존 항목의 상대 순서는 그대로다.

**그림 두 개 모두 첫 판이 틀렸다.** 2포트 도식은 상자 안 부제목이 상자보다 넓어 "what the human
moves"가 "hat the human move"로 잘렸고, 인터페이스 산점도는 캡션이 viewBox를 넘어갔으며 햅틱
장치 라벨이 자기 점에서 멀리 떨어져 있었다. 브라우저에서 눈으로 보고 나서야 발견했다 — bbox
검사기는 통과시켰는데, 텍스트가 *부모 상자*보다 넓은 것은 viewBox 밖으로 나가는 것이 아니라서다.

### 2026-08-21 (방향 전환: Construction Physical AI — 매니퓰레이션 중심)

연구 방향이 좁혀졌다. **접촉이 많은 건설 조작(contact-rich construction manipulation)** 이
핵심이고, 내비게이션과 HRI는 그것을 실제로 돌아가게 하는 보조 기둥이다. 위키는 "physical AI
전 분야 문해력"으로 완성돼 있었고, 그 목표는 바꾸지 않는다 — 그 위에 **전문화 층**을 얹는다.
공통 커리큘럼(기초 0~9 → how-to-read → 논문 리스트)은 그대로다.

- **[[07-research-program/index|7. Research Program]] 신설**. 연구 정체성 한 문장, 세 기둥과
  그 위계(조작이 주, 내비·HRI가 보조), 학위논문 질문, 기여 비중(50~60 / 20~25 / 20~25),
  조작 중심 스택과 언어→수정 루프 그림, 그리고 **어느 위키 페이지가 어느 기둥을 받치는지의
  지도** — 이 표가 위키를 노트 더미가 아니라 하나의 프로그램으로 묶는다. 범위 통제 규칙도
  명시했다: 새 주제의 입장 시험은 "이것이 건설 조작 연구 질문을 직접 개선하는가"이고,
  정직한 답이 "흥미로울 것 같다"면 답은 아니오다.
- **[[07-research-program/paper-arc|7.1 Paper Arc]] 신설**. 5편 arc(작업자 인지 → 내비/모바일
  조작 → 핵심 건설 조작 → 접촉 다량·학습 조작 → 통합)와 각 편이 기대는 위키 페이지·앵커 논문.
  3편의 작업을 고르는 다섯 기준(접촉이 본질적일 것, 공차가 실재할 것, 사람이 지금 하고 있을 것,
  실험실에서 반복 가능할 것, 실패가 파국적이지 않을 것)이 실제로 쓰는 부분이다 — 이 기준으로
  "로봇 스프레이 도장"은 탈락한다(접촉이 부수적이고 성공을 눈으로 판정한다).
- **[[00-study-depth-guide|Depth Guide]]에 "프로파일: 건설 매니퓰레이션" 추가** + T자 그림.
  중요한 절제: **Mastery를 "매니퓰레이션 전체"로 올리지 않았다.** 기구학·역기구학·궤적 생성은
  Working에 남는다 — 유창하게 *써야 하는* 선수 지식이지 *방어할* 주장이 아니다. Mastery는
  접촉을 지는 핵심(접촉 다량 조작·힘/임피던스/어드미턴스 제어·파지·조작용 모방학습)으로 한정했다.
- **[[02-foundations/manipulator-kinematics-dynamics|기초 10. 매니퓰레이터 기구학·동역학]] 신설**
  — 기구학·동역학이 더 필요한가라는 질문의 답. 답은 "기구학은 이미 충분하고, **동역학 절반과
  작업 공간으로 넘어가는 다리가 통째로 비어 있었다**"였다. MR 4~5장은 FK와 야코비안, $\tau = J^\top\mathcal{F}$까지
  잘 가르치지만 거기서 멈추고, 힘 제어는 그 너머에서 시작한다. 그래서 이 페이지는 FK/IK를
  다시 가르치지 않고 빈 곳만 채운다: 매니퓰레이터 방정식, 코리올리 결합, 역동역학·계산 토크,
  그리고 작업 공간 관성 $\Lambda = (JM^{-1}J^\top)^{-1}$.
  세 숫자가 이 페이지를 진다 — 같은 2 kg 팔인데 **곧게 뻗으면 1번 관절 관성이 접었을 때의 5배**
  (제자세마다 게인이 달라져야 하는 이유), 1번 관절을 **정지시켜 두어도** 2번이 2 rad/s로
  휘두르면 $-4$ N·m가 필요하고 속도를 두 배 하면 $-16$ N·m가 되는 것(저속 실험이 모델 오차를
  숨기는 이유), 그리고 $\theta=(0°,90°)$에서 **끝점이 옆으로는 1 kg, 위로는 2 kg처럼 거동**
  하는 것(같은 강성 게인이 모든 방향에서 옳을 수 없는 이유, 충격력이 방향에 의존하는 이유).
  겉보기 질량 타원의 긴 축이 *어려운* 방향이라는 것 — MR 5장 가조작성 타원과 정확히 반대로
  읽는다 — 도 명시했다. 모든 수치는 넘파이로 재계산했고, 질량 행렬은 운동 에너지에서 수치
  미분으로 독립 검증했다.
- 홈에 **5번 경로(매니퓰레이션 우선)** 추가 — 2번을 대신하는 것이 아니라 그다음에 타는 경로.
  기초 인덱스에는 10번을 "전문화 트랙"으로 분리해 두었다: 공통 커리큘럼은 여전히 0~9다.

**부수적으로 찾은 버그**: EN/KR 그림 개수 파리티를 전 코퍼스에서 처음 검사했더니 **중복 그림
세 개**가 나왔다(MR 4장·5장의 SVG, RL 기초의 mermaid). 이전 중복 제거가 놓친 이유는 사본들이
완전히 같지 않았기 때문이다 — 타원 반지름이 5% 다르거나 캡션 줄바꿈이 다르거나 라벨 한 줄의
표현이 달랐다. 즉 부분 쓰기 뒤 재시도가 남긴 흔적이고, 정확 일치 비교로는 안 잡힌다. 그중
하나는 mermaid 라벨 안에 이스케이프되지 않은 `|`까지 들고 있었다(`p(s'|s,a)`). 파리티 검사를
앞으로의 QA에 포함한다.


### 2026-08-19 (전수 읽기 감사 후속 — 남은 6개 항목 전부 집행)

전수 읽기에서 뽑은 목록을 추천 순서(1 → 3 → 4 → 5 → 6 → 2)대로 전부 끝냈다.

- **논문 노트 86편 전부에 수학 on-ramp 신설** (71편에 없었다). 기초 트랙과 논문을 잇는 다리가
  정작 논문 쪽에서 끊겨 있었다. 각 노트가 자기가 기대는 **구체적인 절**과 거기서 무엇을 만나게
  되는지를 말한다 — ResNet은 그것을 떠받치는 미적분 §5의 한 줄을, CLIP은 코사인 유사도 + 4억
  쌍 검색이 가능한 고차원 기하 + 상호정보량 하한으로서의 InfoNCE를, Diffusion Policy는 회귀
  헤드가 타당한 두 행동을 무효한 하나로 평균 내는 RL 기초 §6의 다봉성을, ExACT는 주장 수준을
  정하는 배치 사다리를. 기존 15편은 한국어만 있어서 영어를 추가 — 86편 전부 이중언어.
- **[[01-canonical-papers/how-to-read|논문 읽는 법]]에 §4.5 시범 신설**: 2~4절의 도구 셋을
  RT-1 하나에 순서대로 실제로 돌렸다. 초록 해독이 수식 하나 보기 전에 질문 셋을 만들고, 그
  셋이 결국 논문 자신의 결과 표 축과 일치한다. 수식 5질문에서 3번("기댓값의 대상")이 값을
  한다: "시연자의 상태 위에서 잡힌다"가 곧 복합 오차 문제이고, 논문이 아니라 수식이 알려준다.
  그다음 주장 체크리스트가 물 곳이 생긴다 — 97%/76% 격차가 일반화 주장의 정직한 내용이고,
  논문이 두 분할을 따로 보고했기 때문에만 존재한다.
- **[[02-foundations/overview|기초 Overview]]에 통과 점검 신설**: 페이지별 자가점검은 한
  페이지씩만 검사했고, 트랙 전체가 끝났는지 판정하는 것이 없었다. 최소 두 페이지를 엮는 누적
  12문항(층 모양+비선형성 / 그래디언트 부호와 크기 / 고유분해+PSD 판정 / 이차형식+공분산이
  PSD인 이유 / 나트 단위 교차 엔트로피 / KL / 기저율 / 칼만 융합 / 극점과 그 이산 상 /
  에일리어싱 / 유효 지평 / 10회 90% 읽기), 9개 이상이면 통과. 모든 숫자 검산 완료. 홈과
  기초 인덱스에서 링크.
- **용어집 12개 추가** — 노트에서 반복해 쓰는데 정의가 없던 것: cross-attention(25회),
  in-context learning(16), pooling(15), NMS(14), denoising(14), FLOPs(12), residual
  connection, receptive field, reparameterization trick, adapter, throughput vs latency,
  CLIP score.
- **페이지별 잔여 공백 정리**: PMF/PDF/CDF 풀어쓰기(밀도는 확률이 아니라는 함정 포함), 주사위
  분산 근거, 임피던스 법칙과 단위 + 1 cm 오차가 $10^4$ N/m에서 100 N인 계산, 반공간 투영의
  숫자 예제, 표준편차 vs 표준오차($n=4$면 2배 차이 — 오차 막대가 좁아 보이는 이유), 점 셋
  최소제곱과 직교성 10초 검산, 연쇄 법칙의 전치와 끝의 1, SLAM의 시그마 포인트·파티클 고갈·
  게이지 자유도. **그림 4개** 추가(가우시안, 스테레오 2패널, RRT 트리, 자율성 스펙트럼) +
  연결 지도에 SE(3)·ML 실무 노드.
- **★ 논문 17편 전부에 그림** (EN·KR 각각, 총 34개). 각각 그 논문이 유명한 *메커니즘*을
  보인다: 어텐션의 모양 연쇄(정사각형은 T×T 표 하나뿐 — 이차 비용), CLIP 유사도 행렬(N개
  정답 대 N²−N개 음성), 회귀 헤드가 두 시연을 평균 내 장애물에 정통으로 박는 그림, ACT 청킹의
  결정 21회 대 5회, DDPM의 고정 순방향/학습 역방향 두 사슬, 휜 경로 대 곧은 경로의 적분 스텝,
  RT-2의 공유 어휘, π0의 두 전문가, GR00T의 10 Hz/120 Hz 2단, Dreamer의 상상 루프, SAM의
  무거운 절반/가벼운 절반 분할, VGGT의 루프 대 순방향 한 번, HEAP의 고전 스택(+힘 궤적을
  계획하는 이유), AES의 모듈형 스택, ExT의 **화살표 굵기**(실기계 검증은 사전학습 정책뿐,
  파인튜닝은 시뮬레이션), 비전 유도 조립의 지그 대체, 건식 석벽의 닫힌 루프.

**검증**: 그림 총 94개(인라인 SVG) + mermaid 69블록. 브라우저에서 **텍스트만이 아니라 모든
그리기 요소**를 `getBBox()`로 재측정 — 잘림 0, 겹침 0. 작업 중 세 그림이 틀려서 다시 그렸다:
가우시안의 좁은 곡선이 viewBox 밖으로 잘려 있었고(텍스트만 보던 이전 검사가 놓쳤다), 스테레오의
"가까운 점"이 가깝게 보이지 않았으며, RRT 트리가 "충돌 없으면 뻗는다"는 캡션과 달리 장애물을
관통했다. 검사기에 경로-장애물 교차 판정을 추가했다. QA 159파일 0문제, KaTeX 오류 0,
렌더 안 된 굵은 글씨 0.


### 2026-08-07 (남은 목록 소진 — MR 3~5장, 배치, 연구 실무, 건설 트랙)

지난 항목에서 "다음 세션"으로 미뤄둔 목록을 전부 끝냈다. 도형 총 56개.

- **MR 3~5장** — 기하 챕터인데 그림이 0개였다. 텍스트는 이미 계산 예제가 있었으므로 **그림만**
  보강: 3장에 space/body 프레임 그림(같은 화살표, 두 벌의 숫자 — [Ad_T]에 R과 p가 둘 다
  필요한 이유), 4장에 2R 팔의 home/90-90 그림(PoE와 기하 두 경로가 같은 끝점에 도달;
  어긋나면 스크류 축이나 home이 틀린 것), 5장에 가조작성 타원 두 개
  ($\theta_2 = 90°$일 때 $\sigma$ = 1.62/0.62 비 2.6 vs $20°$일 때 2.20/0.16 비 14 —
  펴질수록 납작해지고 $0°$에서 직선으로 붕괴).
- **[[04-robotics/robot-systems-deployment|로봇 시스템·배치]]** — 70 ms 지연 예산을 **실제
  비율의 막대**로. 추론 40 ms가 예산의 절반을 넘는 것이 눈에 보인다. "30 Hz로 돈다"가 "그
  프레임이 얼마나 낡았나"와 다른 질문이라는 요점을 그림이 대신 말한다.
- **[[06-research-practice/experimental-design-reproducibility|실험 설계]]** — 시행 횟수 대
  불확실성 곡선(로그 축): $1/\sqrt n$이 10회에서 ±32%p, 100회에서 ±10%p, 1000회에서 ±3%p.
  rule of three($3/n$)도 함께 그려 "실패 0회"가 무엇을 보장하지 *않는지* 보이게.
- **건설 트랙** — 판단대로 유도가 아니라 **구조를 보이는 그림**으로: 디지털 트윈 4단 사다리
  (각 단이 명사가 아니라 *경로 하나*를 더한다는 것 + 각 단에 아직 없는 것), 그리고 HRC의
  감지→추론→결정→소통→작업자 폐루프 mermaid(1~2단계만 있으면 작업자 *센싱*이고, 2→3 화살표가
  있어야 작업자 중심 *로보틱스*가 된다는 페이지의 핵심 주장을 그림이 직접 보여준다).

**검증**: 브라우저에서 56개 도형 전체의 텍스트를 `getBBox()`로 재측정 — viewBox 이탈 0,
텍스트 겹침 0, 상자 넘침 0(작업 중 digital-twin 사다리에서 8건, MR 3개 그림에서 6건,
지연 예산에서 1건을 잡아 고쳤다). SVG 텍스트 안에 마크다운 문법이 남은 것 0건(ch03에서 1건
발견 — SVG는 마크다운을 파싱하지 않으므로 별표가 그대로 보였다). KaTeX 오류 0.

### 2026-08-07 (이차형식 $x^\top A x$ + foundations 기준을 로보틱스 트랙으로)

- **$x^\top A x$ 해설 신설** — "스칼라로 치면 $ax^2$ 같은데 전치가 붙어 있어 직관이 안 온다"는
  질문. 답: 정확히 그것이 맞고 전치는 부기다. 모양으로 설명($1{\times}n)(n{\times}n)(n{\times}1)$
  = 숫자 하나이므로 $x$가 양쪽에 필요), 풀어쓰면 $\sum_i\sum_j A_{ij}x_ix_j$라 항마다 좌표
  둘의 곱 = "이차", 대각 $A$는 독립 포물선 / 비대각은 그릇을 기울이는 교차항 / PSD가 아닌 예는
  안장. 그리고 두 정의가 같은 이유를 유도: $A = Q\Lambda Q^\top$, $y = Q^\top x$로 두면
  $x^\top A x = \sum_i \lambda_i y_i^2$ — 제곱의 가중합이므로 모든 $x$에서 $\ge 0$인 것과 모든
  $\lambda_i \ge 0$이 같은 말. 만나는 자리 둘: 테일러 2차항 $\tfrac12\delta^\top H\delta$(어느
  방향으로도 위로 휨 = 지역 최솟값), 그리고 $\text{Var}(w^\top x) = w^\top\Sigma w \ge 0$ —
  분산이 음수일 수 없다는 것이 **공분산이 PSD인 이유** 그 자체다.
  **그림 추가**: 그릇 / 바닥이 평평한 골짜기 / 안장 세 패널.
- **비-foundations 페이지 전수 감사** — 42개 교육 페이지의 단어 수·숫자 수·그림 수를 스크립트로
  뽑았다. 500단어 넘는데 구체적 숫자가 3개 미만인 페이지 12개, 그림이 0인 페이지 다수.
- **[[04-robotics/lqr-lqg|6. LQR/LQG]] §3 전면 재작성** (883단어에 숫자 1개였다) — 이중 적분기의
  리카티를 **손으로 푼다**: $P$를 대입해 스칼라 방정식 셋 → $p_{12} = \sqrt{qr}$ →
  $k_1 = \sqrt\rho$, $k_2 = \sqrt2\rho^{1/4}$. 여기서 사실 셋이 한꺼번에 떨어진다: ① 비만
  의미가 있다(1행과 4행 이득이 동일 — 자가점검 2번의 답) ② **감쇠는 고를 수 없다** — 어떤
  가중치에서도 $\zeta = 0.707$이고, 제어 이론 §7이 손으로 놓은 $\zeta=0.7$과 사실상 같은 자리다
  ③ **속도는 네제곱근** — 두 배 빠르게 하려면 $q/r$을 16배, 열 배면 $10^4$배. 4행 표와
  계단 응답 그림 추가.
- **[[04-robotics/mpc|7. MPC]] §2에 크기 계산** — stacked vs condensed를 형용사가 아니라 숫자로:
  사족보행 centroidal MPC($n_x{=}13$, $n_u{=}12$, $N{=}10$)에서 stacked 263변수·띠 구조 vs
  condensed 120변수·밀집($120^2 = 14{,}400$). 지평을 두 배로 하면 stacked는 2배, condensed는
  4배. 그리고 50 Hz면 전체가 20 ms 안에 끝나야 한다.

**남은 것** (다음 세션): MR 3~5장(기하 챕터인데 그림 0개), robot-systems-deployment의 지연
예산 숫자, 06-research-practice의 통계 주장, 05-construction 트랙의 그림. 05는 상당수가
Literacy 수준 서베이 페이지라 유도가 아니라 **논문에서 온 구체적 숫자와 그림**을 넣는 것이 맞다.

### 2026-08-07 (foundations 전 페이지 — 결론만 있던 자리에 계산을 넣기)

"$G(s) = 1/(s-a)$ 같은 것도 유도를 다 쓰고, 예시가 너무 구체적이지 않다. engineering math뿐
아니라 foundation 전부를 보강하라." 기초 트랙 11페이지를 절 단위로 스크립트 감사해 **구체적
숫자가 하나도 없는 절**을 뽑았다. 감사 시점에 73개 절 중 47개가 그랬다. 결과: 실제 숫자를 지고
있는 절이 20% → 43%로. (남은 것은 표기법 사전, 지표 표, "이 위키 어디에 나오나" 같은 목록형 절.)

**0.5 공업수학** — 지적받은 네 곳 전부:
- §9 **$G(s)$ 유도** 추가: 양변 라플라스 → $x(0)=0$ 규약 명시 → $sX = aX + U$ → $(s-a)X = U$.
  "미분방정식이 나눗셈이 되었다"와, 그 나눗셈을 깨뜨리는 $s = a$가 곧 8절의 지수라는 연결까지.
- §9 **"주파수 응답 = $G(j\omega)$"** 해설: $s = j\omega$는 7절의 순수 회전 = 영원히 진동하는
  입력, 답의 크기는 증폭률, 각도는 지연. + **"이 절은 예고편이지 목적지가 아니다"** 콜아웃 —
  실제로 가르치는 곳은 제어 이론 §5와 신호처리 §5임을 명시(질문에 대한 직접 답).
- §2 **테일러**: $\sqrt{4.1}$을 차수별로 계산하는 표(오차 $2.5\times10^{-2}$ → $1.5\times10^{-4}$
  → $1.9\times10^{-6}$). 뉴턴법 논쟁이 이 표라는 것과, 논문이 말없이 쓰는 $e^\delta \approx 1+\delta$.
- §3 **적분·기댓값**: 주사위 $E[X] = 3.5$(가중합이 말 그대로), 균등분포 손 계산($E[X^2] = 1/3$과
  $(E[X])^2 = 1/4$의 차이가 곧 분산), 그리고 코드에서는 언제나 샘플 평균.
- §4 **행렬 연산 전면 재작성**: 성분 하나를 천천히 계산 → $AB$는 열이, $BA$는 행이 바뀐다는
  것을 **눈으로** 보여 순서 문제 설명 → 역행렬을 숫자로($\det = -2$, 검산까지) → 특이 행렬
  $\begin{pmatrix}1&2\\2&4\end{pmatrix}$로 "풀랭크가 배제하는 것" → 배치 $(32\times512)$ 모양 검사.
- §1 도함수 예제를 $(2,1)$에서 실제로 평가($\nabla f = (-2,-4)$)하고 부호와 크기를 해석.

**나머지 기초 10페이지**:
- **선형대수**: $2\times2$ 고유값 분해 전 과정($\lambda = 3, 1$, 고유벡터가 수직으로 나오는 이유),
  조건수의 대가를 숫자로($\kappa = 10$, 20스텝 뒤 $(0.012, 0.019)$), 특이 행렬의 SVD($\sigma = 5, 0$).
- **미적분·역전파**: "손으로 하는 계산 예제"가 정작 기호뿐이었다 → 0.7과 *같은* 신경망에 실제
  숫자를 넣은 역전파 표 5줄 + 읽는 법 셋(부호가 방향을 말한다 / 큰 활성값이 큰 그래디언트 /
  모양이 안 맞으면 버그). 순방향 vs 역방향 모드 비용에 숫자($10^7$배).
- **확률**: 선형성에 "독립 불필요"가 왜 단서인지를 주사위 분산으로($5.83$ vs $11.67$),
  MLE를 실제 측정값 5개로(그리고 라플라스 잡음이면 중앙값이 된다는 대비), 칼만 이득 스칼라
  예제($K = 0.8$, 새 분산이 두 입력 어느 쪽보다 작다).
- **정보이론**: $H(p) = 1.157$, $H(p,q) = 1.280$을 비트로 계산하고 그 차 $0.123$이 §3에서 KL과
  정확히 일치함을 보임. 상호정보량을 균열 감지기로($0.037$ / $0.081$비트 = 46%).
- **최적화**: 경사 하강 vs 뉴턴법을 산수 한 줄로(10스텝 vs 1스텝, 그리고 왜 신경망엔 못 쓰는지).
- **신호처리**: $N=4$ DFT를 손으로($X[0]=0$이 DC 없음, $k=1$과 거울상 $k=3$), 지수 평활기를
  스텝별로 추적(90%까지 22샘플 = 100 Hz에서 0.22초 지연).
- **RL 기초**: 종이에서 푸는 2-상태 MDP($V(B)=10$이 0.5 §5의 기하급수 합, $V(A)=9$, 선택이
  없으면 어드밴티지가 0).
- **SE(3)**: 회전 순서를 숫자로($R_zR_x$는 z축, $R_xR_z$는 y축), 회전 행렬 검증법($\det=-1$이면
  반사 = 실제 버그), $T_{AB}T_{BC}$ 합성을 숫자로(오프셋을 먼저 회전시켜야 하는 이유).
- **ML 실무**: 불균형 데이터 혼동행렬 예제 — 정확도 97%인데 "전부 정상"이라 답해도 94%,
  정밀도 0.80 / 재현율 0.67(균열 20개 놓침) / F1 0.727. 건설에서 이 비대칭이 왜 실제인지까지.

### 2026-08-07 (0.5 공업수학 §6~7 정밀 보강 — 질문 5개에서 나온 것)

읽다가 막힌 지점 다섯을 그대로 받아 고쳤다. 전부 0.5와 2. 미적분 안에서 해결했고 새 페이지는
만들지 않았다.

- **"$\ln$은 밑이 10인가 e인가"** — 위키가 $\log$와 $\ln$을 밑을 밝히지 않고 섞어 쓰고 있었다.
  이제 명시: $\ln$은 언제나 밑 $e$(natural log의 n), $\log_2$는 밑 2, 밑 없는 $\log$는 이 위키와
  대부분의 ML 논문에서 밑 $e$이되 **정보이론에서만 비트라서 밑 2**. 그리고 밑을 바꿔도 상수배일
  뿐이라 최솟값 위치가 안 바뀐다는 점까지. $\log_b x = \ln x/\ln b$의 유도($y = \log_b x$ ⇒
  $b^y = x$ ⇒ 양변에 $\ln$)와 1 나트 $\approx$ 1.44 비트도 추가.
- **"log-sum-exp가 다른 페이지에 자세히 있나"** — 없었다. 0.5 §6이 "[[02-foundations/calculus-backprop|2. 미적분 §4]] 참조"라 했는데
  정작 거기엔 "log-sum-exp로 안정화" 한 줄뿐이라 서로 미루고 있었다. 상세 설명은 0.5 §6에
  두고(이미 유도해 둠), 미적분 §4가 그쪽을 가리키도록 방향을 바로잡았다.
- **"softmax·교차 엔트로피가 요즘도 중요한가"** — 위키가 답을 안 하고 있었다. 명시: 지금도
  모든 LLM의 학습 손실(다음 토큰 = 어휘 전체 softmax + 교차 엔트로피), 모든 분류 헤드,
  어텐션 내부의 연산 자체이고, [[01-canonical-papers/notes/4-vla/rt-1|RT-1]]처럼 행동을 256구간으로 이산화하면 로봇 제어도 분류 문제가 된다.
  예외도 함께: 연속값 출력(회귀 헤드, 디퓨전·플로우 매칭 정책)은 제곱 오차로 학습한다.
- **"atan2가 뭔데"** / **"loses the quadrant가 무슨 뜻"** — 정의도 이유도 없이 "atan2를 써라"만
  있었다. 이제 atan2의 정의(두 좌표를 따로 받아 원 전체 각도를 반환)와, $(1,1)$과 $(-1,-1)$이
  둘 다 $b/a = 1$이라 $\arctan$이 똑같이 $45°$를 주는 구체적 반례, $a = 0$에서 깨지는 이유,
  역기구학이 atan2만 쓰는 이유까지. **그림 추가**: 원점을 지나는 한 점선 위의 두 점과 $45°$·$225°$ 호.
- **"사인파로 분해 = 회전에 투영이 이해가 안 된다"** — 한 문장으로 압축돼 있었다. 3단계로 폈다:
  ① 사인파는 회전을 옆에서 본 것(실수부 = 가로 그림자) ② "주파수 $\omega$가 얼마나 들었나"는
  $e^{-j\omega t}$로 **반대로 돌려서 평균**내면 나온다 — 있으면 회전이 상쇄돼 값이 남고, 없으면
  모든 방향을 고르게 훑어 0이 된다 ③ 그 "곱하고 평균"이 곧 내적이고, 그것이 투영이다.
  그래서 DFT $X[k] = \sum_n x[n]e^{-j2\pi kn/N}$에는 숨은 내용이 없다. **그림 추가**: 단위원 위의
  점과 그 그림자가 그리는 코사인.

### 2026-08-07 (한 줄로 압축한 유도 5곳 펼치기)

"$\gamma S = S - 1$이 왜 나왔는지 모르겠다"는 지적. 결론만 있고 **중간 단계가 없는** 곳을
같은 기준으로 훑어 5곳을 펼쳤다. 새 페이지를 만들지 않고 원래 자리에서 늘렸다.

- **기하급수 합** (0.5 §5) — "두 줄 증명"이라 써놓고 실제로는 결론만 있었다. 이제:
  $S$에 이름 붙이기 → 양변에 $\gamma$ 곱하기 → 두 줄을 나란히 놓으면 아래 줄이 위 줄에서
  맨 앞의 $1$만 뺀 것임을 보이기 → 그래서 $\gamma S = S - 1$ → 대수 4단계. 요령이 "곱해도
  같은 무한 꼬리가 재현되므로 무한이 스스로 상쇄된다"는 것임을 명시. $\gamma = 0.5$ 검산과
  논문이 실제로 쓰는 유한 합 $\frac{1-\gamma^n}{1-\gamma}$도 추가.
- **유효 지평이 왜 $1/(1-\gamma)$인가** — 이것도 그냥 단정하고 있었다. 두 방향으로 설명:
  ① 에이전트가 평생 모을 수 있는 가중치의 총합이 정확히 그 합이다 ② $0.99^{100} \approx 0.37$.
  [[02-foundations/rl-basics|RL 기초]]에서 0.5 §5로 역참조 추가.
- **Log-sum-exp** (0.5 §6) — 안정화 식만 있고 유도도 이유도 없었다. 가장 큰 항을 묶어내는
  단계, 근사가 아니라 정확한 항등식이라는 점, 그리고 왜 오버플로가 사라지는지(모든 지수가
  $\le 0$이 되고 최대항이 정확히 $1$이라 언더플로도 안 난다)를 추가.
- **$\dot x = ax$의 해** (0.5 §8) — 풀지 말고 *대입해서 확인*하면 된다는 것을 보였다
  (미분하면 $a\,x(t)$, $t=0$에서 $x(0)$). 6절의 "$e$는 자기 도함수" 한 줄과 연결.
- **연속/이산 안정 조건** (0.5 §8) — "한 이야기의 두 반쪽"이라고만 하고 다리를 안 놓았다.
  $a_d = e^{a\Delta t}$이고 $|e^{a\Delta t}| = e^{\text{Re}(a)\Delta t}$이므로 좌반평면이 단위원
  안으로 사상된다는 계산을 명시.
- **베이즈 정리** (3. 확률 §1) — "연쇄 법칙의 두 순서에서 한 줄로 유도"라고 써놓고 그 한 줄이
  없었다. 두 분해를 나란히 쓰고 같다고 놓고 $P(x)$로 나누는 과정을 실제로 보였다.

### 2026-08-07 (전제된 용어 풀어쓰기 + 굵은 글씨 렌더링 버그 수정)

"full rank", "continuum limit" 같은 용어가 설명 없이 쓰이고 있다는 지적을 받아, 기초 트랙 전체를
읽는 순서대로 훑으며 **처음 등장할 때 정의가 없는 용어**를 전수로 뽑았다(후보 100여 개를 스크립트로
첫 등장 위치와 함께 출력해 하나씩 판정).

- **풀어쓴 용어 20개**(EN·KR 양쪽, 모두 한 문장 안에 삽입 — 별도 박스를 만들지 않았다):
  연속 극한, 풀랭크, 열공간과 span, 직교행렬, 외적, 닫힘 성질, 편향·분산, $A \succeq 0$(양의 준정부호),
  탭(tap), SNR·dB, DC, 자기상관, 정상성/WSS, 군(group), 잠재변수, 변분 추론, support(지지집합),
  온폴리시/오프폴리시, 위상 여유, 종단 집합의 불변성, A*의 admissibility/consistency.
- **0.5 공업수학 표기법 사전**에 $A^\top$, $\det A$, $A \succeq 0$ 세 줄 추가 — 앞 페이지에서 이미 쓰던
  기호인데 사전에 없었다.
- **[[glossary|용어집]]에 16개 항목 신설** — 본문에서 푼 용어를 나중에 다시 찾을 수 있도록.
- **렌더링 버그 발견·수정 (12개 페이지)** — `**용어(term)**이` 형태가 CommonMark의 right-flanking
  규칙 때문에 굵게 처리되지 않고 별표가 그대로 보이고 있었다(닫는 `**` 앞이 문장부호 `)`, 뒤가 한글이면
  닫히지 않는다). 오늘 넣은 것뿐 아니라 rt-2, jepa, 신경망 기초, ml-practice, RL 기초, SE(3),
  접촉·촉각, HRI 안전 페이지에 **이전부터 있던 것들**이었다. 전부 `**용어**(term)` 형태로 고쳤고,
  같은 실수가 다시 들어오지 못하도록 `scripts/verify_content.py`에 **검사 10번**으로 추가했다.
  (이 검사가 곧바로 내가 놓친 1건을 더 잡았다.)

### 2026-08-07 (시각 자료 전면 도입 — 그림 36개 + 다이어그램)

"나는 visual 학습이 유리하다"는 요청에 따라 전 페이지를 다시 읽고, 글로만 설명하던 개념 중
그림이 실제로 이해를 바꾸는 곳을 골라 채웠다. 감사 결과 157페이지 중 145페이지에 도형이 0개였다.

- **원칙**: 장식용 그림은 넣지 않는다. 본문의 *계산 예제 숫자를 그대로 지고 있는* 그림만 넣는다.
  모든 도형은 인라인 SVG로 `currentColor`를 쓰므로 라이트/다크 테마를 자동으로 따라간다.
- **추가한 SVG 18종 (EN·KR 각각, 총 36개)**:
  역전파 순전파/역전파 흐름(δ가 전치를 타고 흐르고 가중치 그래디언트는 외적),
  $H(p,q)=H(p)+\mathrm{KL}$ 누적 막대, 볼록 vs 비볼록 지형, 에일리어싱(200 Hz로 찍은 170 Hz가 30 Hz로 보이는 그림 — 두 곡선이 8개 샘플을 **모두** 지나감),
  과적합 학습·검증 곡선과 조기 종료, SE(3) 프레임 합성($T_{AC}=T_{AB}T_{BC}$에서 B가 약분),
  s-평면 극점 지도, 계단 응답 극점 배치 전후(44%·8초 → 4.6%·1.4초, 실제 수식으로 그림),
  MPC receding horizon, 마찰 원뿔, 핀홀 투영(작고 가까운 물체와 크고 먼 물체가 **같은 픽셀**에 맺힘),
  작업 공간 vs 배위 공간 장애물 팽창, PPO 클리핑 목적함수(좋은 행동/나쁜 행동 두 패널),
  보상 항 균형(+0.02 vs −0.50을 실제 비율로), 깊이 사다리(★◐○ vs L/W/M이 독립임을 두 칸으로),
  SVD 회전→스케일→회전, 가제어/비가제어 도달 방향, 2-3-1 신경망 계산 예제.
- **추가한 mermaid 다이어그램**: 칼만 예측→보정 루프, MDP 에이전트-환경 루프, RL 방법 계보
  (모델 프리/기반 → 가치·정책 그래디언트 → 액터-크리틱), 제어 피드백 블록도, 학습 루프.
- **작업 중 잡은 내용 오류 3건** — 그림을 그리다 글이 틀렸거나 그림이 글과 어긋난 곳이 드러났다:
  ① 과적합 그림의 검증 곡선이 올라가지 않고 계속 내려가고 있었다(그림이 과적합을 안 보여줌),
  ② 에일리어싱 그림의 샘플 점이 실제 신호 곡선 위에 있지 않아 "같은 샘플을 공유한다"는 요점이 무너져 있었다,
  ③ 핀홀 그림이 캡션과 반대로 두 점을 **다른** 픽셀에 보내고 있었다. 셋 다 수식으로 다시 생성해 교정.
- **검증**: 브라우저에서 36개 도형의 모든 텍스트에 대해 (a) viewBox 밖으로 나가는지 (b) 서로 겹치는지
  (c) 상자 밖으로 흘러나오는지를 `getBBox()`로 전수 측정 — 최종 0건. 라이트/다크 양쪽 육안 확인.
  한국어 절에 영어 캡션이 남은 그림 0건, 영어 절에 한국어가 섞인 그림 0건(스크립트 검사).

### 2026-08-02 (진입 장벽 낮추기 + 실전 RL 층 + 언어 정비 + 읽은 기록)

- **[[02-foundations/neural-network-basics|0.7 신경망이란 무엇인가]] 신설** — 위키가 "층", "손실",
  "에폭"을 정의 없이 쓰고 있었다. 신경망 = 행렬곱 쌓기, 비선형성이 필요한 이유, 2→3→1 순전파
  손 계산, 파라미터 세기, 배치·에폭·이터레이션 산수, 파라미터 vs 하이퍼파라미터 표.
  foundations 각 페이지에 **입장 조건**(이 페이지를 열기 전에 갖춰야 할 것)을 명시.
- **[[02-foundations/rl-basics|RL 기초]]에 §7–§10 추가** — 논문을 읽는 데 실제로 필요한데 빠져 있던 층:
  보상 설계(가중합 표 + 퇴화 해 산수), 탐색과 커리큘럼, 실기계 위의 RL(RLFT·KL 정규화·안전 옵션 4종),
  RL 실험 절 읽는 법(2e9 스텝 ÷ 4,096 환경 ÷ 50 Hz = 시뮬 2.7시간 vs 실기계 한 대로 **1.3년**).
  [[glossary|용어집]]에 관련 용어 대량 추가.
- **언어 전수 점검** — 영국식 철자 16건(전부 내가 그날 넣은 것) 정규화, 수·시제 불일치와 어색한
  한국어 표현 교정.
- **읽은 기록 위젯** — 페이지마다 +/− 로 읽은 날짜와 회차를 남기는 로컬 플러그인
  (`plugins/read-log`). localStorage에 페이지별로 저장, SPA 이동 후에도 다시 그린다.

## 2026-07

### 2026-07-26 (교차 검증 수리 + 제어 트랙 자립화 + 이중언어 완결)

전 페이지 정독 평가에서 나온 항목을 전부 반영했다.

- **개념 페이지가 자기 논문 노트를 반박하던 3건 교정** — 위키 방법론의 신뢰성 문제라 최우선:
  [[05-construction-robotics/earthmoving-heavy-machinery|토공]]의 ExT "~100시간"을 논문 검증값(과제당 15만 에피소드 ≈ 실기계 30일, RTX 3090 2시간 생성, 실기계 전이는 *사전학습* 정책)으로,
  [[05-construction-robotics/hrc-worker-centered|HRC]]의 Lasota & Shah "실제 자동차 조립 라인 배치"를 "BMW *테스트 환경*(저자가 실제 공장 배치를 대표하지 않는다고 명시)"으로,
  토공 §5의 근거 없는 운용 묘사("지오펜스·공공 통행 없음·직원 감독")를 논문이 실제로 말하는 범위로.
- **[[04-robotics/control-theory-ce397|5. 제어 이론]] 전면 재작성** — 외부 패킷 목차였던 페이지를 자체 완결 가이드로: 피드백이 사는 것/지불하는 것, 상태공간 변환, 모드와 행렬 지수, 연속·이산 안정성, 전달함수·극점과 $\zeta,\omega_n$에서 정착 시간·오버슈트 뽑기, 가제어성·가관측성 랭크 검정(가제어/불가제어 예제 각 1), 극점 배치 계산 예제, PID와 와인드업, 관측기·분리 원리, 선형화·게인 스케줄링·포화, 제어 주장 읽기 표, 자가점검 5문 + 정답. 공업수학을 한 번 본 독학자 기준으로 외부 자료 없이 통과 가능.
- **제어 서브트랙 5~8번에 선수지식 콜아웃 신설** (로보틱스·건설 22페이지 중 유일하게 없던 묶음): control→LQR→MPC→convex MPC가 서로를 명시적으로 가리키도록.
- **고아 챕터 3개 해소** — MR 6장(IK)·9장(궤적 생성)·13장(바퀴 로봇)은 코퍼스 전체에서 인바운드 링크가 0이었다. 계획·로봇 시스템·상태 추정·현장 인식·SE(3)에서 역링크를 걸어 전 페이지 인바운드 ≥ 1.
- **이중언어 완결**: foundations 6페이지에 EN 정답 추가, MR 11장 전부의 "시작 전 점검"·자가점검·정답 병기, [[03-deep-learning/lineage|DL 계보]] 영어 절 신설(홈 4번 진입 경로), [[glossary|용어집]] 전 항목 영어 병기, canonical list 서문 영어, **논문 노트 86편의 exit-test 체크리스트 전량과 claim box 전량 병기**.
- 잔여 정리: 8-construction 인덱스 frontmatter 보강, 공업수학 §8–9 → 제어 이론 본문 링크(제목 안 위키링크 금지 규약 준수).
- **완료 확인 중 추가 발견 2건** (전수 스크립트가 잡음): [[00-study-depth-guide|깊이 가이드]]와 [[08-research-radar/index|Research Radar]]의 영어 절이 `## English`로 감싸이지 않아 하위 절이 `## 한국어`의 형제로 앉아 있었고, Radar는 **영어 Methodology가 한국어 절 뒤에** 통째로 붙어 있어 한국어 독자가 번역 안 된 절로 끝나고 있었다. 둘 다 감싸고 h3로 강등, Radar에 `### 사용법`·`### 방법론` 미러 추가 → 코퍼스 전역 "한쪽 언어만 있는 페이지" 0.
- `resource` 태그 정리: 포인터 스텁이던 시절에 붙은 라벨을 [[04-robotics/lqr-lqg|LQR/LQG]]·[[04-robotics/mpc|MPC]]에서 제거(둘 다 이제 자체 완결 가이드). 실제 외부 자료 포인터인 [[04-robotics/convex-mpc-legged|convex MPC]]·[[04-robotics/modern-robotics-book|MR 책 가이드]]에는 유지. 태그를 소비하는 코드가 없음을 확인한 뒤 라벨만 수정.

**검증 방법 메모** — 이번에 실제로 문제를 잡아낸 것은 눈이 아니라 스크립트다: ① 위키링크 in/out-degree 계산(고아 3개 발견) ② 논문 노트별 claim box·체크리스트의 언어 판정(31 + 약 300건 발견) ③ `## English`/`## 한국어` 짝 검사(위의 2건 발견). 다음 감사 때도 이 셋을 먼저 돌릴 것.

### 2026-07-24 (독학의 벽 9곳 낮추기)

교육 평가가 "외부 자료 없이는 못 넘는다"고 지목한 지점 — 주변 페이지가 유도를 기대하도록 훈련시켜 놓고 결과만 단정하던 곳 — 을 EN·KR 양쪽에서 메웠다.

- **정보이론 §5 ELBO**: 숨어 있던 대수를 노출 — $\log\frac{p(x|z)p(z)}{q}$를 재구성항 + (−KL)로 항별 분할해 우변이 허공에서 나오지 않도록
- **선형대수 §5 가제어성**: 랭크 조건을 단정 대신 직관으로 구축(입력이 $B$ 열 방향으로 밀고, 동역학이 도달 범위를 $AB$, $A^2B$로 회전)
- **공업수학 §8–9**: 가장 어려운 절에 자가점검이 0개였던 것 → ODE 안정성·극점/반평면 문제 2개와 정답 추가
- **RL 기초 §6**: 모방학습 7개 밀집 불릿을 3개 라벨 묶음으로(목적함수+covariate shift / 데이터셋 읽기 / 표현력 헤드가 존재하는 이유)
- **DDIM**: core 디퓨전 노트 중 유일하게 램프가 없던 것 → 결정론적 단계를 구체적으로(노이즈 예측 → 함의된 $x_0$ 읽기 → 낮은 수준으로 재노이즈)와 왜 허용되는지(손실이 marginal만 제약)
- **미적분·역전파**: "위의 각 단계가 곧 VJP 하나다" 연결문으로 손 계산 예제와 §2 추상 정의를 융합
- **최적화 §4**: "왜 제약을 목적함수에 더하나" — 최적점에서 $\nabla f$가 $\nabla g$와 반평행 → $\nabla(f+\lambda g)=0$
- **SE(3) §4**: 반대칭 형태 유도($R^\top R=I$ 미분 → $\dot R+\dot R^\top=0$)
- **MR 8장**: 진자 1링크로 $M/c/g$ 접지($\tau=ml^2\ddot\theta+mgl\sin\theta$), 왜 1링크는 코리올리가 0이고 2링크에서 켜지는지

### 2026-07-23 (최종 편집 3종 — 깊이 정직화·핵심 보강·정밀 교정)

- **깊이 표시 2층 분리**: `study-depth`(권장 목표) vs `wiki-support`(페이지 자체 제공 깊이) — [[00-study-depth-guide|가이드]]에 규약 문서화, MR 8~12장·제어이론 등 격차 페이지에 `wiki-support: Literacy` 표시
- **핵심 Working 페이지 4개 심층 보강**: [[04-robotics/mpc|MPC]](QP 볼록성 조건, stacked/condensed, infeasibility·softening·warm start, 모델 불일치, 선형/NMPC/접촉), [[04-robotics/lqr-lqg|LQR/LQG]](리카티 구조 읽기, 안정화 가능성·검출 가능성, Q/R 예제, LQG 무여유), [[01-canonical-papers/notes/8-construction/heap|HEAP]](구동 개조·센싱·소프트웨어 스택·증거 성격·공백 4종), [[01-canonical-papers/notes/8-construction/ext|ExT]](시연 생성 3소스·사전학습·SFT/RLFT·전이 증거)
- **절대 표현 정밀 교정 6건**: Transformer "essentially all"→지배적+예외 명시, CLIP 개념 학습 단정→해석+경쟁 설명, FM 직선 경로→가능 조건(보장 아님), "objective of choice"→지배적 목적함수 중 하나, 고차원 직교성→검색 가능성의 한 이유(관련쌍 점수는 학습의 성질), 칼만 vs 저역통과→모델 조건부
- MR 책 가이드의 "챕터 노트 추가 예정" 잔재 제거

### 2026-07-23 (건설 트랙 완성 — 코퍼스 기반 확충 마무리)

- 5클러스터 조사(미시간·UIUC 디아스포라·GT/TAMU/CMU·유럽·로보틱스史+산업)의 잔여 작업 완료:
- **신규 논문 노트 12편**: [[01-canonical-papers/notes/8-construction/exact-2024|ExACT]](Baidu, sim 검증), [[01-canonical-papers/notes/8-construction/egli-rl|Egli RL 굴착]], [[01-canonical-papers/notes/8-construction/cho-slam|Cho SLAM 2018]], [[01-canonical-papers/notes/8-construction/han-welding|Han 용접]], [[01-canonical-papers/notes/8-construction/aerial-am-2022|Nature 공중 AM]], [[01-canonical-papers/notes/8-construction/liang-hrc-survey|Liang HRC 서베이]], [[01-canonical-papers/notes/8-construction/liu-jebelli-bci|BCI 원격조작]], [[01-canonical-papers/notes/8-construction/lasota-shah|Lasota & Shah]], [[01-canonical-papers/notes/8-construction/park-nl|Park NL]], [[01-canonical-papers/notes/8-construction/yu-imitation|Yu 모방학습]], [[01-canonical-papers/notes/8-construction/lundeen-2019|Lundeen]], [[01-canonical-papers/notes/8-construction/liang-lfd|Liang LfD]] — 8-construction 총 22노트
- 기존 6노트(AES·돌담·Feng·Stentz·Wang DT·휠로더) 하우스 스타일 승격: 완전 한국어 병기, 연결, 수치 심층화
- 스트림 5페이지(조립·인식·HRC·DT·sim-to-real)에 Depth target·자가 점검·KR 다이어그램 복원 + 전 스트림↔노트 양방향 링크
- 선행 노트 4편(PPO·SAC·PointNet·SayCan) 완전 통합: opener·위키링크·RL 기초 §4 on-ramp·GAE 단락
- 오류 수정: Tang DOI(2010), ext.md 구식 스트림 참조, Radar 빈 캐시 가드, iframe 높이, LDM 깊이(Literacy)


### 2026-07-23 (전역 학습 깊이 + 다중 범위 Research Radar)

- Study intent를 Radar의 임시 필터에서 제거하고 [[00-study-depth-guide|0. Study Depth Guide]]와 모든 실질 학습 페이지의 `study-depth`·`depth-goal`·`mastery-when` 속성으로 이동
- 140개 foundations·개념·논문·로보틱스·건설·research-practice 페이지에 Literacy/Working 기본 목표와 Mastery 승격 조건을 명시; 템플릿과 배포 QA에도 강제
- Radar 온톨로지를 59개 토픽·10개 겹치는 연구 관점으로 확장: Deep Learning, Computer Vision, Generative Models, Multimodal, Physical AI, World Models, VLM & VLA, Robot Learning, Robotics, Construction Physical AI
- 단일 폴더 분류를 폐기하고 Diffusion Policy처럼 여러 분야의 합류점이 복수 관점에 동시에 나타나는 multi-label 구조 채택
- 건설 신호는 `construction robotics` 검색이 아니라 작업·장비·자산·재료·현장 맥락 × 로봇·자율성·인식·계획·제어·HRI의 교차 조건으로 검출; Automation in Construction와 Construction Robotics의 Crossref 메타데이터 추가
- 2021–2025 출판 논문 58,439편, 59개 토픽으로 재집계; SLAM의 일반 `localization` 오탐과 건물 설계 RL의 embodied 오탐을 제거하고 대표 표본·필터·캐시 갱신을 브라우저에서 검증

### 2026-07-23 (Research Radar 초기판)

- 문해력 획득 이후 연구 문제를 고르는 단계의 의사결정 도구 [[08-research-radar/index|Research Radar]] 신설
- 2021–2025 NeurIPS·ICML·ICLR·CVPR·ICRA·CoRL 정식 proceedings 55,642편을 DBLP 서지 메타데이터로 수집; arXiv·워크숍 제외
- 규모×상승속도 사분면, 절대 규모/Fast Rising/Early Signals 순위, scope·학습 깊이·signal 필터, 연도별 추세, 대표 논문·근거 패널 구현
- 제목 기반 다중 태그 taxonomy, 연도별 전체 논문 수 정규화, momentum·burst·venue breadth·small-sample shrinkage 적용
- OpenAlex의 연도별 conference-source 분할이 가짜 추세를 만들 수 있어 집계 소스로 사용하지 않고, DBLP 연도별 proceedings를 로컬 캐시 후 분석하는 보수적 경로 채택
- 현재 제한: 제목에 방법명이 없는 논문은 누락될 수 있고 기관 정규화·기술적 논쟁 자동 후보는 후속 검증 대상; 화면에 audit와 confidence 공개

### 2026-07-23 (건설로봇 코퍼스·계보 재구성)

- 기술·학술·시스템의 세 계보로 분야를 재구성하고 미시간/UIUC 디아스포라, ETH 패브리케이션·굴착 나무, CMU 중장비 기원, 연구→산업 연결을 검증
- 희망적 주제 목록을 코퍼스에서 도출한 5개 연구 스트림+2개 횡단층으로 교체; 토공, 조립, 현장 인식, 작업자 중심 HRC, 디지털 트윈, sim-to-real, 산업 배치의 이중언어 개념 페이지 추가
- canonical 8번을 18편의 앵커·supporting 문헌으로 확장하고 CMU 트럭 적재, Baidu AES, 휠로더 RL, 비전 유도 조립, 돌담, BIM 디지털 트윈의 상세 노트 추가
- ExT·건설 physical AI의 누락 선행 재료 PPO, SAC, PointNet/PointNet++, SayCan을 추가

### 2026-07-23 (7종 전수 감사 + 프로필 기준 티어 조정)

- 건설로봇 제외 전 콘텐츠를 7개 영역으로 병렬 전수 감사 (탐색 계층 / foundations / 논문 노트 2조 / 로보틱스 / research practice / 커리큘럼 적합성)
- BLOCKING 2건 수정: softmax를 [[02-foundations/engineering-math|0.5 §10]]에 정의(12곳에서 정의 없이 사용되던 것), 로보틱스 한국어 인덱스에 3.5 기하 인식 추가
- 사실 교정: ViT 88.55%는 H/14(L/16은 87.8), Bahdanau는 미지단어 제외 부분집합에서만 SMT 대등, I3D 원 논문은 71–75%, Qwen2-VL은 2B/7B/72B, Genie 학습 데이터는 ~24.4만 시간 크롤 중 ~3만 시간 필터
- 탐색 수리: 섹션 인덱스 2곳이 자기 하위 페이지 링크, canonical list 영어 범례 추가·study guide를 트랙 순서로 재배열, π0→Flow Matching 직결(Score SDE 우회 제거), 전방 참조 선수지식 2건 완화
- 교육 보강: ELBO의 곱하고-나누기 단계 명시, 시행 수 가늠 도구(±1/√n, rule of three), 리뷰어 응답 예문, PaliGemma 기구·한계 보강, VGGT에 기하 인식 on-ramp
- **프로필 기준 티어 조정** (미국 상위 공대 건설 physical AI 대학원생 기준): BERT·GPT-3·InstructGPT·I3D·PlaNet·Score-SDE·LDM ◐→○, Cosmos ★→◐ — 로봇 논문에서 한 줄 조상 인용 수준인 항목들의 읽기 부담 축소
- 예정: PPO(◐)·SAC(○)·PointNet/++(○)·SayCan(○) 노트와 sim-to-real 학습 가이드를 건설로봇 확충과 함께 추가 (ExT 계열 읽기의 선행 재료)

### 2026-07-23 (공통 커리큘럼 공백 보완)

- 외부 점검(달성도 ~92%)이 지목한 세 공백을 보완:
- [[04-robotics/geometric-perception-calibration|3.5 Geometric Perception & Calibration]] 신설 — 핀홀 모델·intrinsics/extrinsics·깊이 복원(스테레오 계산 예제)·포인트 클라우드·registration/ICP·보정 5종·reprojection error·기하+딥 인식의 역할 구분
- [[04-robotics/robot-systems-deployment|Robot Systems]] §6 행동 오케스트레이션 추가 — FSM·behavior tree·precondition/postcondition·timeout/retry/fallback·action server; "로봇이 회복했다"가 어느 계층의 일인지 읽는 법
- [[02-foundations/rl-basics|RL 기초]] §6을 모방 학습 도구 상자로 확장 — BC 목적함수, covariate shift와 오차 누적, DAgger, 시연 수집과 동기화, 행동 청킹, 다봉 시연, 데이터 큐레이션, 오프라인 RL과의 구분; VLA 노트 진입 사슬 연결
- 용어집 확충 — Intrinsics/Extrinsics·Geometric/Deep perception·State machine/Behavior tree (혼동 쌍), ICP·Reprojection error·Behavior tree (사전)

### 2026-07-23 (robot systems literacy와 research practice 확장)

- **4. Robotics & Control**을 **4. Robotics & Physical Systems**로 확장
- State Estimation/Localization/SLAM, Planning & Decision-Making, Contact/Force/Tactile Interaction, Robot Systems/Embodiment/Deployment, HRI & Safety의 다섯 literacy guide 추가
- **6. Research Practice** 신설: Research Questions & Claims, Experimental Design & Reproducibility, Failure Analysis & System Evaluation, Scientific Writing & Peer Review
- Foundations 이후 학습 구조를 AI model literacy와 robot systems literacy의 병렬 경로로 나누고 Physical AI·Construction Robotics에서 합류하도록 연결
- Probability, Optimization, Signal Processing, RL, SE(3), ML Practice, Modern Robotics, LQG, MPC에 직접 교차 링크를 추가하고 glossary를 estimation·planning·contact·systems·safety·reproducibility까지 확장
- 새 상세 페이지 9개에 English/한국어, After reading, Self-check가 유지되는지 deployment QA에서 자동 검사

### 2026-07-22 (교육 설계 개편 — research-literacy curriculum)

- 사이트 목표를 명문화: **연구 문해력**(용어 친숙 + 논문의 문장·수식·주장·실험을 과장 없이 읽기)이 목표이며, 균일한 기술 숙달이 아님 — 홈에 목표 선언 추가
- [[01-canonical-papers/how-to-read|0. How to Read Papers]] 신설: 4단계 읽기 깊이(인지/독해/실무/숙달), 논문 문장의 문법(보장하지 않는 것 표), 수식 5질문, 회의주의자 체크리스트, 퇴장 시험
- 읽기 깊이 체계 도입: 핵심 논문 리스트 전체에 ★(원문 정독)·◐(노트+훑기)·○(계보용) 표시 — 이 기호는 권장 읽기 분량이지 숙련 수준이 아님
- 전체 63개 논문 노트에 "읽고 나면 말할 수 있어야 하는 것" 점검 추가; ★ 15편에는 "핵심 주장 읽는 법" 박스(제목의 주장을 어디까지 믿을지)와 수학 on-ramp 추가
- foundations에 선수 지식 박스·접이식 정답·계산 예제 보강; [[02-foundations/ml-practice|ML 실무]]에 평가 함정 섹션(체리피킹, 개루프/폐루프, 시드 분산 등) 추가
- [[05-construction-robotics/index|건설로봇]]에 11축 논문 읽기 틀 추가 (작업·신체·인식·표현·계획제어·자율·배포안전·평가 현실성·sim-to-real·실패 분석·생산성 비교)
- 정밀 편집 패스: 용어집 정의 교정(조건수·VLM/VLA·IL·Diffusion/FM·LQR), foundations 단정 완화(atan2, MLE 범위, ResNet 완화 표현, 민감도/정확도 구분), MR 12·13장 가정 명시, 계보도 실선 의미 완화, [[01-canonical-papers/notes/3-vlm/paligemma|PaliGemma]] 노트 신설(○)

### 2026-07-22 (초기 구축)

- 위키 개설: Obsidian + Quartz + GitHub Pages 구축
- 첫 논문 노트 작성: [[01-canonical-papers/notes/1-foundations/attention-is-all-you-need|Attention Is All You Need]]
- 기초 1차 배치 (2012→2016 연대순): [[01-canonical-papers/notes/1-foundations/alexnet|AlexNet]], [[01-canonical-papers/notes/1-foundations/vgg|VGG]], [[01-canonical-papers/notes/1-foundations/bahdanau-attention|Bahdanau Attention]], [[01-canonical-papers/notes/1-foundations/resnet|ResNet]]
- 계보도에 2012–2017 구간 추가 (CNN 갈래 + RNN 갈래 → Transformer 합류)
- 다음 읽을 것: Adam, BatchNorm, seq2seq, LSTM 또는 바로 ViT/CLIP
- 기초 섹션 완주 + Transformer 이후 진출 (총 12편 추가):
  기초 마무리 — [[01-canonical-papers/notes/1-foundations/lstm|LSTM]], [[01-canonical-papers/notes/1-foundations/seq2seq|seq2seq]], [[01-canonical-papers/notes/1-foundations/adam|Adam]], [[01-canonical-papers/notes/1-foundations/batch-norm|BatchNorm]]
  Transformer 이후 — [[01-canonical-papers/notes/1-foundations/bert|BERT]], [[01-canonical-papers/notes/1-foundations/gpt-3|GPT-3]], [[01-canonical-papers/notes/1-foundations/scaling-laws|Scaling Laws+Chinchilla]], [[01-canonical-papers/notes/1-foundations/vit|ViT]], [[01-canonical-papers/notes/1-foundations/mae|MAE]], [[01-canonical-papers/notes/1-foundations/lora|LoRA]], [[01-canonical-papers/notes/1-foundations/instructgpt|InstructGPT]], [[01-canonical-papers/notes/3-vlm/clip|CLIP]]
- VGGT(CVPR 2025 Best Paper) 확인 후 CV 섹션에 추가
- 다음: VLM 계열 (Flamingo, BLIP-2, LLaVA) 또는 디퓨전 계열 (VAE, GAN, DDPM)
- 노트 형식 개선: 모든 노트 첫 줄에 "저자, 학회 연도 — arXiv·PDF·Code" 표기; 폴더명 `01-canonical-papers`로 변경
- VLM 배치 완료: [[01-canonical-papers/notes/3-vlm/flamingo|Flamingo]], [[01-canonical-papers/notes/3-vlm/blip-2|BLIP-2]], [[01-canonical-papers/notes/3-vlm/llava|LLaVA]] — CLIP→연결자 설계 경쟁→지시 튜닝의 흐름; 다음은 VLA로 가는 관문 통과
- 다음: 디퓨전 계열 (VAE, GAN, DDPM, Score SDE) 또는 바로 VLA (RT-1, RT-2, Diffusion Policy)
- 기초 정리 페이지 3편 (reference 자료를 내 언어로 재구성): [[02-foundations/optimization|최적화]], [[02-foundations/probability|확률과 랜덤 프로세스]], [[02-foundations/signal-processing|신호처리]]
- 디퓨전 기초 배치: [[01-canonical-papers/notes/6-diffusion/vae|VAE]], [[01-canonical-papers/notes/6-diffusion/gan|GAN]], [[01-canonical-papers/notes/6-diffusion/ddpm|DDPM]], [[01-canonical-papers/notes/6-diffusion/score-sde|Score SDE]] — VAE(안정·흐릿) vs GAN(선명·불안정)의 긴장을 DDPM이 해소하고 Score SDE가 이론으로 통합
- 다음: VLA 진입 (RT-1, RT-2, Diffusion Policy, ACT) — 디퓨전 수학 준비 완료
- VLA 1차 배치: [[01-canonical-papers/notes/4-vla/rt-1|RT-1]], [[01-canonical-papers/notes/4-vla/rt-2|RT-2]], [[01-canonical-papers/notes/4-vla/diffusion-policy|Diffusion Policy]], [[01-canonical-papers/notes/4-vla/act|ACT/ALOHA]] — 로봇 데이터 스케일링(RT-1) → 웹 지식 전이(RT-2) → 다봉 행동 분포(DP) → 행동 청킹(ACT)
- 다음: VLA 2차 (Open X-Embodiment, Octo, OpenVLA, π0, GR00T N1)로 VLA 섹션 완주
- 기초 섹션 확장 (4편 추가, 총 7편 체계 완성): [[02-foundations/linear-algebra|선형대수]], [[02-foundations/calculus-backprop|미적분과 역전파]], [[02-foundations/information-theory|정보이론]], [[02-foundations/rl-basics|강화학습 기초]] — 위키의 모든 논문을 읽기에 충분한 배경 세트
- VLA 섹션 완주 (5편): [[01-canonical-papers/notes/4-vla/open-x-embodiment|OXE]], [[01-canonical-papers/notes/4-vla/octo|Octo]], [[01-canonical-papers/notes/4-vla/openvla|OpenVLA]], [[01-canonical-papers/notes/4-vla/pi0|π0]], [[01-canonical-papers/notes/4-vla/gr00t-n1|GR00T N1]] — 데이터 풀링 → 오픈 모듈식 정책 → 오픈 VLA → flow matching 융합 → 휴머노이드 데이터 피라미드
- 다음: 월드모델 섹션 (World Models, PlaNet, Dreamer, JEPA, Genie, Sora, Cosmos)
- sudoremove.com 점검: 내용 상충 없음 확인; 배울 점으로 생태계 카탈로그 채택 → [[03-deep-learning/physical-ai-ecosystem|Physical AI Ecosystem]] 페이지 신설
- 선형대수 페이지에 제어이론 연결 섹션 추가 (상태공간, 고유값=안정성, 가제어성 랭크 조건)
- 월드모델 섹션 완주 (7편): [[01-canonical-papers/notes/5-world-models/world-models|World Models]], [[01-canonical-papers/notes/5-world-models/planet|PlaNet]], [[01-canonical-papers/notes/5-world-models/dreamer|Dreamer v1–3]], [[01-canonical-papers/notes/5-world-models/jepa|JEPA 계열]], [[01-canonical-papers/notes/5-world-models/genie|Genie]], [[01-canonical-papers/notes/5-world-models/sora|Sora]], [[01-canonical-papers/notes/5-world-models/cosmos|Cosmos]] — 꿈속 훈련 → RSSM → 상상 속 actor-critic → 표현 공간 예측(반대 진영) → 인터넷 비디오에서 행동 발견 → 시뮬레이터 가설 → 인프라화
- 다음 후보: CV 나머지 (U-Net~VGGT) 또는 디퓨전 나머지 (DDIM, CFG, LDM, ControlNet, DiT, Flow Matching) 또는 건설로봇 서베이 수집
- CV 섹션 완주 (12편): U-Net, Faster R-CNN, YOLO, I3D/SlowFast, DETR, NeRF, Swin, DINO/DINOv2, SAM, 3DGS, Depth Anything, VGGT
- 디퓨전 섹션 완주 (6편): DDIM, CFG, Latent Diffusion, ControlNet, DiT, Flow Matching — 딥러닝 파트(섹션 1~6) 논문 노트 전부 완료 (총 58편)
- 방침: foundations 페이지들을 제어이론 교재 수준의 깊이로 증보하기로 함 (다음 작업)
- 남은 큰 덩어리: ① foundations 심화 증보 ② 건설로봇 서베이 수집(섹션 8) ③ 로보틱스/제어 노트(섹션 7)
- foundations 심화 증보 완료: 7개 페이지 전부 교재 수준으로 — 유도(정규방정식, KL 비음수성, 벨만, 정책 그래디언트), 계산 예제(2층 역전파, 합성곱, 베이즈 진단, KKT 투영, MPC-QP 정식화), 스스로 점검 문제 추가
- 남은 큰 덩어리: ① 건설로봇 서베이 수집(섹션 8) ② 로보틱스/제어 노트(섹션 7: Modern Robotics 챕터, LQR, MPC)
