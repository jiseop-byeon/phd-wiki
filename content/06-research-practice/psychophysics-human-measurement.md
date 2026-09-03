---
title: 8. Psychophysics & Human Measurement
tags: [research, human-subjects, psychophysics, haptics]
study-depth: Working
depth-goal: "Choose the right threshold procedure for a stated question, turn a perceptual threshold into a hardware spec or a data-validity check, and tell a perception study from a performance study when reading a haptic evaluation."
mastery-when: "Raise to Mastery when a human-subjects evaluation is itself the claim — an operator study, an interface comparison, or a perceptual validation of a collected corpus."
---

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to pick a threshold procedure, use published thresholds as design
> numbers, and read a human-subjects evaluation without mistaking workload for perception.
> **Working** — 임계값 측정 절차를 고르고, 발표된 임계값을 설계 수치로 쓰고, 작업부하
> 연구를 지각 연구로 혼동하지 않고 인간 대상 평가를 읽을 수 있는 수준.

> [!note] Prerequisites · 선수 지식
> [[06-research-practice/experimental-design-reproducibility|2. Experimental Design & Reproducibility]] first — this page
> is that page's toolbox for the special case where the measured system is a person.
> [[06-research-practice/experimental-design-reproducibility|2. 실험 설계와 재현성]]을 먼저 —
> 이 페이지는 측정 대상이 사람인 특수 사례를 위한 그 페이지의 공구함이다.

## English

A robot that works with or for people eventually makes a claim about a person: the
operator *felt* the contact, the worker *noticed* the alert, the interface *reduced*
difficulty. Psychophysics is the branch of experimental psychology that puts numbers on
"felt" and "noticed," and it is old enough — Weber's law dates to 1834 — that its
procedures are standardized. Using them badly is a reviewable offense; not knowing them
means hardware specs and data-validity arguments get made by guesswork.

### 1. Two thresholds

Everything downstream rests on two quantities:

- **Absolute (detection) threshold** — the smallest stimulus a person can detect at all.
  Operationally: the intensity detected on 50% of trials, read off a fitted psychometric
  function.
- **Difference threshold (JND)** — the smallest *change* in a stimulus a person can
  detect. **Weber's law** says the JND is roughly proportional to the reference
  intensity: $\Delta I / I = c$, a constant *Weber fraction*, over the useful middle of
  the range (it degrades near threshold and at extremes).

Weber fractions worth memorizing for force interaction, all from the classical
literature: **force magnitude ≈ 7–10%** (Jones 1989; Tan et al. 1994), **stiffness
≈ 23%** (Jones & Hunter 1990). Vibrotactile detection is sharpest near **250 Hz**, where
displacement thresholds fall below a micrometer under ideal conditions (Bolanowski et
al. 1988). These few numbers do a surprising amount of engineering work in §3–§4.

### 2. The classical procedures

Four procedures measure the same thresholds with different bias/cost tradeoffs:

- **Method of limits.** Present ascending then descending series; the subject reports
  when the sensation appears/disappears; the threshold is the average transition point.
  Fast, but habituation and expectation bias the transitions — subjects keep saying
  "yes" on a descending run and "no" on an ascending one.
- **Method of adjustment.** The subject tunes the stimulus themselves until it is just
  perceptible (absolute) or matches a reference (difference). Fastest and most engaging;
  highest variance; the mean gives the point of subjective equality (PSE) and the
  standard deviation estimates the difference threshold.
- **Method of constant stimuli.** Fix 5–9 intensities spanning the threshold, present
  each many times in random order, record yes/no. Fitting the percent-yes curve gives
  the **psychometric function** — typically sigmoid — with the absolute threshold at
  50% and the JND read between the 25% and 75% points. Least biased (the subject cannot
  predict the next level), most trials, and the only procedure that hands you the whole
  curve rather than a point.
- **Staircase (adaptive) methods.** A transformed up-down rule (Levitt 1971) drives the
  stimulus toward the threshold and oscillates around it; averaging the reversal points
  estimates the threshold at a fraction of constant-stimuli cost. The workhorse of
  modern haptics studies; variants (step-size schedules, double staircases,
  two-interval forced choice) control where on the psychometric function the procedure
  converges.

Two cautions transfer straight from [[06-research-practice/experimental-design-reproducibility|2. Experimental Design §1]]:
the experimental unit is the **participant**, not the trial — a thousand staircase
trials from three people is n = 3 — and yes/no procedures confound sensitivity with
response bias, which is why forced-choice designs ("which interval contained it?")
are preferred when the claim matters.

### 3. Thresholds are hardware specs

A haptic or teleoperation interface displays forces to a person, so human thresholds
bound its useful resolution from below and its required fidelity from above. Two rules:

- A force artifact **below** the detection threshold and below the JND at operating
  force is invisible — money spent removing it buys nothing perceptible.
- A force artifact **above** the JND is part of what the operator feels — friction,
  cogging, and quantization at that scale are not implementation details, they are the
  displayed signal.

> [!example] Worked example · 계산 예제
> **When does encoder quantization become perceptible?** A 1-DoF capstan-drive device:
> motor pulley radius $r_p = 5$ mm, sector radius $r_s = 75$ mm (transmission ratio
> $R = 15$), handle lever $r_h = 70$ mm, encoder resolution $0.25°$ per count at the
> motor. Sector resolution is $0.25°/15 \approx 0.0167°$, so handle position resolves to
> $\Delta x = r_h \cdot \Delta\theta = 0.070 \times (0.0167 \cdot \pi/180) \approx
> \mathbf{0.02\ mm}$.
>
> Rendering a $k = 500$ N/m virtual surface, force steps in increments of
> $k\,\Delta x = 0.01$ N — at a 1 N contact that is 1%, far under the 7% force JND:
> the surface feels continuous. Render a "concrete-like" $k = 10^4$ N/m instead and the
> step becomes $0.2$ N — **20% of a light 1 N touch, nearly three JNDs**: the wall
> feels gritty. Same encoder, same math; the perceptual threshold is what decides which
> stiffness this hardware may honestly render. The device-side half of this chain lives
> in [[04-robotics/teleoperation-demonstration|12. Teleoperation §4.5]].

### 4. Thresholds validate data

The same numbers police a demonstration corpus. If a dataset's stated value is that
operators *modulated force with intent* — the premise of a force-bearing corpus — then
recorded force variation smaller than what the operator could perceive or reliably
produce is not intent; it is noise wearing intent's clothing. Concretely: at a 2 N task
force with a 7% JND, variations under ~0.14 N cannot be attributed to deliberate
modulation, and a policy trained to imitate them is imitating tremor and friction.
This check belongs in the collection pipeline next to the manipulability check of
[[04-robotics/teleoperation-demonstration|12. Teleoperation §5]], not in the rebuttal.

The practical reason to check thresholds is to avoid giving sensor detail a stronger interpretation than the experiment supports. For example, in wall wiping, small recorded force fluctuations could reflect pad friction, involuntary motion, or purposeful correction driven by another cue. A published perceptual threshold is a screening reference, not proof of which mechanism generated an individual sample.

**The reading this gives you.** Ask whether deliberate modulation was independently validated under the actual interface and task conditions. Compare synchronized commands, task events, and perceptual evidence before labeling a force channel as intention. Preserve the raw signal, but distinguish measured variation from an inferred human purpose.

### 5. Perception on a construction site

Lab thresholds assume a bare, rested fingertip. A site removes every one of those
assumptions, and each removal is a design fact for worker-facing interfaces
([[05-construction-robotics/hrc-worker-centered|6. HRC & Worker-Centered Robotics]]):

| Channel (afferent) | Band | Carries | On site |
|---|---|---|---|
| Merkel (SA I) | 0.3–3 Hz | fine form, texture | blocked by gloves |
| Meissner (RA I) | 3–40 Hz | slip, grip events | strongly attenuated by gloves |
| Pacinian (PC) | 10–500 Hz, peak ≈ 250 Hz | vibration | passes through material |
| Ruffini (SA II) | sustained | skin stretch, lateral force | partly preserved |

(The four-afferent account is Johansson & Flanagan 2009; the channel psychophysics is
Bolanowski et al. 1988.)

- **Gloves gate by frequency, not uniformly.** Spatial detail dies; vibration in the PC
  band transmits through material — which is why a phone vibrating in a pocket is felt.
  A vibrotactile alert is therefore the one cutaneous channel a gloved worker keeps.
  The exception is engineered against you: anti-vibration gloves are certified (ISO
  10819) precisely by how much they attenuate that band.
- **Machinery masks the alert band.** Powered tools and heavy equipment put broadband
  vibration exactly into PC territory. A wrist-worn alert competing with a breaker in
  the same hands is signal against noise in one channel — masking and adaptation, not
  volume, are why site alert wearables fail quietly.
- **The population's thresholds are shifted.** Prolonged vibration exposure produces
  elevated vibrotactile thresholds — the sensorineural component of hand-arm vibration
  syndrome (Brammer, Taylor & Lundborg 1987; exposure metrics in ISO 5349-1). A
  detection threshold measured on students does not transfer to a crew of drillers;
  measure on the population the claim is about, or say so.

### 6. Beyond thresholds — performance and workload

Not every haptic experiment is psychophysical. Three families answer different
questions, and papers routinely blur them:

- **Perception**: can the person detect/discriminate it? (this page's §1–§2)
- **Performance**: does the interface change task outcomes? The classical instrument is
  **Fitts' law** — movement time grows with the index of difficulty
  $ID = \log_2(2D/W)$ for target distance $D$ and width $W$ — so "the haptic condition
  reduced difficulty" has a standard operationalization (Fitts 1954).
- **Workload / experience**: what did it cost the person? NASA-TLX (Hart & Staveland
  1988) and its kin are self-report; they measure something real that is not
  perception and not task time.

A claim of the form "haptic feedback improved teleoperation" should say which of the
three it measured. One that measured workload and concludes perception has changed
lanes mid-paper — the reviewer's phrase is *construct validity*, and
[[06-research-practice/research-questions-claims|1. Research Questions & Claims]] is
where that vocabulary lives.

### After reading

- [ ] Define absolute threshold, JND, Weber fraction, PSE, psychometric function.
- [ ] Pick between limits, adjustment, constant stimuli, and staircase for a stated
  question and budget, and name each procedure's characteristic bias.
- [ ] Turn a Weber fraction into a hardware spec (quantization, friction floor) and
  into a corpus-validity bound.
- [ ] Name the three site effects — glove frequency-gating, machinery masking in the PC
  band, HAVS-shifted thresholds — and what each does to an alert design.
- [ ] Classify a haptic evaluation as perception, performance, or workload.

### Self-check

1. Why does the method of constant stimuli resist the habituation/expectation biases
   that affect the method of limits?
2. A staircase run yields 40 trials from each of 3 participants. What is n, and why?
3. A device's friction band is 0.05 N and the task force is 2 N. Is the friction
   perceptible mid-task (force JND 7%)? Near force reversals at ~0.3 N?
4. An alert wristband works in the lab and fails on site. Give two channel-level
   explanations before blaming the electronics.
5. A paper reports NASA-TLX improved with haptic feedback and concludes operators
   "perceived contact better." What is wrong?

> [!tip]- Answers
> 1. Because the subject cannot predict the next level: intensities are presented many times
> in *random order*, so there is no ascending or descending run to habituate to or anticipate.
> The methods of limits and adjustment both have a direction of travel, and the bias rides on
> it. The price is trial count — randomness costs data.
> 2. $n = 3$. The experimental unit is the participant, not the trial
> ([[06-research-practice/experimental-design-reproducibility|2. §1]]): the 40 trials within
> one staircase are made by the same nervous system on the same day and are not independent —
> they exist to estimate that *one* person's threshold well, not to be counted as 40 samples.
> 3. Mid-task, no: the JND at 2 N is $0.07 \times 2 = 0.14$ N, and 0.05 N of friction sits
> well below it. Near reversals, yes: at 0.3 N the JND is $0.07 \times 0.3 = 0.021$ N, and the
> same 0.05 N is now more than twice the detectable change. One friction spec is imperceptible
> and salient *in the same task*, which is why Weber's law makes "is it good enough" a question
> about the operating point, not the device.
> 4. From §5's channel table: **masking** — the tool in the same hands drives broadband
> vibration into the very Pacinian band the alert uses, so the signal competes with noise in
> one channel; and **gating/attenuation** — gloves (anti-vibration gloves by design, ISO 10819)
> attenuate the band the wristband transmits on. Both predict lab success and site failure with
> fully working electronics.
> 5. It measured workload and concluded perception. NASA-TLX is a self-report *cost* measure —
> §6's third family — and can improve while detection is unchanged (less effort, same
> percept) or even worsen while detection improves. A perception claim needs a psychophysical
> measurement: detection or discrimination performance, ideally forced-choice.

### Sources

- G. A. Gescheider, *Psychophysics: The Fundamentals*, 3rd ed., Erlbaum, 1997 — the
  standard procedures text.
- H. Levitt, "Transformed Up-Down Methods in Psychoacoustics," *JASA* 49(2):467–477,
  1971. DOI 10.1121/1.1912375 — the staircase rules.
- L. A. Jones, "Matching forces: constant errors and differential thresholds,"
  *Perception* 18(5):681–687, 1989 — force JND ≈ 7%.
- H. Z. Tan, M. A. Srinivasan, B. Eberman, B. Cheng, "Human factors for the design of
  force-reflecting haptic interfaces," *ASME DSC* 55-1, pp. 353–359, 1994 — design
  tables for force interaction.
- L. A. Jones, I. W. Hunter, "A perceptual analysis of stiffness," *Exp. Brain Res.*
  79:150–156, 1990 — stiffness JND ≈ 23%.
- S. J. Bolanowski, G. A. Gescheider, R. T. Verrillo, C. M. Checkosky, "Four channels
  mediate the mechanical aspects of touch," *JASA* 84(5):1680–1694, 1988 — channel
  bands and the 250 Hz sensitivity peak.
- R. S. Johansson, J. R. Flanagan, "Coding and use of tactile signals from the
  fingertips in object manipulation tasks," *Nat. Rev. Neurosci.* 10:345–359, 2009.
  DOI 10.1038/nrn2621 — the four-afferent account (also cited in
  [[04-robotics/tactile-visuotactile|14. Tactile & Visuotactile Sensing]]).
- P. M. Fitts, "The information capacity of the human motor system in controlling the
  amplitude of movement," *J. Exp. Psychol.* 47(6):381–391, 1954.
- S. G. Hart, L. E. Staveland, "Development of NASA-TLX (Task Load Index)," *Advances
  in Psychology* 52:139–183, 1988.
- A. J. Brammer, W. Taylor, G. Lundborg, "Sensorineural stages of the hand-arm
  vibration syndrome," *Scand. J. Work Environ. Health* 13(4):279–283, 1987.
- ISO 5349-1:2001, hand-transmitted vibration exposure; ISO 10819, anti-vibration
  glove transmissibility.
- K. E. MacLean, "Haptic interaction design for everyday interfaces," *Reviews of
  Human Factors and Ergonomics* 4:149–194, 2008 — when haptic feedback is worth using
  at all.

## 한국어

사람과 함께, 혹은 사람을 위해 일하는 로봇은 결국 사람에 대한 주장을 하게 된다: 조작자가
접촉을 *느꼈다*, 작업자가 알림을 *알아챘다*, 인터페이스가 난이도를 *낮췄다*. 심리물리학은
"느꼈다"와 "알아챘다"에 숫자를 붙이는 실험심리학의 분과이고, Weber의 법칙이 1834년으로
거슬러 올라갈 만큼 오래되어 절차가 표준화되어 있다. 이 절차를 잘못 쓰면 심사에서 걸리고,
모르면 하드웨어 사양과 데이터 타당성 논증을 어림짐작으로 하게 된다.

### 1. 두 개의 임계값

이후의 모든 것이 두 양 위에 선다:

- **절대(검출) 임계값** — 사람이 검출할 수 있는 가장 작은 자극. 조작적으로는: 적합된
  심리측정 함수에서 읽은, 시행의 50%에서 검출되는 강도.
- **차이 임계값(JND)** — 사람이 검출할 수 있는 가장 작은 자극의 *변화*. **Weber의
  법칙**은 JND가 기준 강도에 대략 비례한다고 말한다: $\Delta I / I = c$, 일정한 *Weber
  분율* — 유효 범위의 중간 대역에서 성립하고 임계값 근처와 양 극단에서는 무너진다.

힘 상호작용에서 외워둘 가치가 있는 Weber 분율, 모두 고전 문헌에서: **힘 크기 ≈ 7–10%**
(Jones 1989; Tan et al. 1994), **강성 ≈ 23%**(Jones & Hunter 1990). 진동촉각 검출은
**250 Hz** 근처에서 가장 예민하고, 이상적인 조건에서 변위 임계값이 1마이크로미터 아래로
내려간다(Bolanowski et al. 1988). 이 몇 개의 숫자가 §3–§4에서 놀랄 만큼 많은 공학적 일을
한다.

### 2. 고전적 절차들

네 절차가 같은 임계값을 서로 다른 편향/비용 절충으로 잰다:

- **극한법(method of limits).** 상승 계열과 하강 계열을 제시하고, 감각이
  나타나는/사라지는 지점을 보고받아 전이점의 평균을 임계값으로 삼는다. 빠르지만 습관화와
  기대가 전이점을 편향시킨다 — 피험자는 하강 계열에서는 "예"를, 상승 계열에서는
  "아니오"를 계속 말하는 경향이 있다.
- **조정법(method of adjustment).** 피험자가 직접 자극을 조절해 겨우 지각되게(절대)
  하거나 기준과 일치시킨다(차이). 가장 빠르고 몰입되지만 분산이 가장 크다. 평균이 주관적
  동등점(PSE), 표준편차가 차이 임계값의 추정치다.
- **항상자극법(method of constant stimuli).** 임계값을 걸치는 5–9개 강도를 고정하고
  각각을 무작위 순서로 여러 번 제시해 예/아니오를 기록한다. 긍정 응답 비율 곡선을
  적합하면 — 보통 S자형인 — **심리측정 함수**가 나오고, 절대 임계값은 50% 지점, JND는
  25%와 75% 지점 사이에서 읽는다. 편향이 가장 적고(다음 강도를 예측할 수 없다) 시행이
  가장 많으며, 점이 아니라 곡선 전체를 주는 유일한 절차다.
- **계단법(staircase, 적응적 방법).** 변형 상하법(Levitt 1971)이 자극을 임계값 쪽으로
  몰아 그 주위에서 진동하게 하고, 반전점들의 평균으로 임계값을 추정한다 — 항상자극법
  비용의 몇 분의 일로. 현대 햅틱 연구의 주력 절차이고, 변형들(스텝 크기 스케줄, 이중
  계단, 2구간 강제선택)이 심리측정 함수의 어느 지점으로 수렴할지를 통제한다.

[[06-research-practice/experimental-design-reproducibility|2. 실험 설계 §1]]에서 두
경고가 그대로 넘어온다: 실험 단위는 시행이 아니라 **참가자**다 — 세 명에게서 나온 계단법
시행 천 번은 n = 3이다 — 그리고 예/아니오 절차는 민감도와 응답 편향을 뒤섞으므로, 주장이
중요할수록 강제선택 설계("어느 구간에 있었는가?")를 쓴다.

### 3. 임계값은 하드웨어 사양이다

햅틱·원격조작 인터페이스는 사람에게 힘을 전시하므로, 인간의 임계값이 유용한 분해능을
아래에서, 요구 충실도를 위에서 경계 짓는다. 두 규칙:

- 검출 임계값 **아래**, 그리고 작동 힘에서의 JND 아래에 있는 힘 인공물은 보이지 않는다 —
  그것을 없애는 데 쓴 돈은 지각 가능한 어떤 것도 사지 못한다.
- JND **위**의 힘 인공물은 조작자가 느끼는 것의 일부다 — 그 크기의 마찰, 코깅, 양자화는
  구현 세부가 아니라 전시되는 신호다.

> [!example] Worked example · 계산 예제
> **엔코더 양자화는 언제 지각되는가?** 1자유도 캡스턴 구동 장치: 모터 풀리 반지름
> $r_p = 5$ mm, 섹터 반지름 $r_s = 75$ mm(전동비 $R = 15$), 핸들 레버 $r_h = 70$ mm,
> 모터 엔코더 분해능 카운트당 $0.25°$. 섹터 분해능은 $0.25°/15 \approx 0.0167°$, 핸들
> 위치 분해능은 $\Delta x = r_h \cdot \Delta\theta = 0.070 \times (0.0167 \cdot
> \pi/180) \approx \mathbf{0.02\ mm}$.
>
> $k = 500$ N/m 가상 표면을 렌더링하면 힘은 $k\,\Delta x = 0.01$ N 단위로 계단진다 —
> 1 N 접촉에서 1%로, 7% 힘 JND에 한참 못 미친다: 표면이 연속으로 느껴진다. 대신
> "콘크리트 같은" $k = 10^4$ N/m을 렌더링하면 계단이 $0.2$ N이 된다 — **가벼운 1 N
> 터치의 20%, JND의 약 세 배**: 벽이 껄끄럽게 느껴진다. 같은 엔코더, 같은 수식이지만,
> 이 하드웨어가 정직하게 렌더링할 수 있는 강성을 정하는 것은 지각 임계값이다. 이 사슬의
> 장치 쪽 절반은 [[04-robotics/teleoperation-demonstration|12. 원격조작 §4.5]]에 있다.

### 4. 임계값은 데이터를 검증한다

같은 숫자가 시연 코퍼스를 감시한다. 데이터셋의 선언된 가치가 조작자가 *의도를 갖고 힘을
조절했다*는 것이라면 — force-bearing 코퍼스의 전제 — 조작자가 지각하거나 신뢰성 있게
만들어낼 수 있는 것보다 작은 힘 변동은 의도가 아니다. 의도의 옷을 입은 잡음이다.
구체적으로: 2 N 작업 힘에서 JND 7%면 약 0.14 N 아래의 변동은 의도적 조절로 볼 수 없고,
그것을 모사하도록 학습된 정책은 떨림과 마찰을 모사하고 있는 것이다. 이 점검은
[[04-robotics/teleoperation-demonstration|12. 원격조작 §5]]의 가조작성 점검 옆, 수집
파이프라인 안에 있어야 한다 — 리버틀에 있어서는 안 된다.

임계값을 확인하는 실무적 이유는 센서 세부에 실험이 지지하는 것보다 강한 뜻을 붙이지 않기 위해서다. 벽 닦기의 작은 힘 변동은 패드 마찰, 비자발적 움직임, 다른 단서에 따른 의도적 보정에서 올 수 있다. 발표된 지각 임계값은 선별 기준이지 개별 표본의 생성 기전을 증명하지는 않는다.

**여기서 얻는 독법.** 실제 인터페이스와 과제 조건에서 의도적 조절을 독립 검증했는지 묻는다. 힘 채널을 의도로 부르기 전에 동기화된 명령, 과제 사건, 지각 증거를 비교한다. 원신호는 보존하되 측정된 변동과 추론한 사람의 목적을 구분한다.

### 5. 건설 현장에서의 지각

실험실 임계값은 맨손의, 쉬고 있는 손끝을 가정한다. 현장은 그 가정을 하나씩 전부
제거하고, 각 제거는 작업자 대면 인터페이스의 설계 사실이 된다
([[05-construction-robotics/hrc-worker-centered|6. HRC와 작업자 중심 로보틱스]]):

| 채널(구심신경) | 대역 | 나르는 것 | 현장에서 |
|---|---|---|---|
| Merkel (SA I) | 0.3–3 Hz | 미세 형태, 질감 | 장갑에 차단됨 |
| Meissner (RA I) | 3–40 Hz | 미끄러짐, 그립 사건 | 장갑에 크게 감쇠 |
| Pacinian (PC) | 10–500 Hz, 피크 ≈ 250 Hz | 진동 | 재료를 통과함 |
| Ruffini (SA II) | 지속 | 피부 늘림, 측면 힘 | 부분 보존 |

(네 구심신경 체계는 Johansson & Flanagan 2009, 채널 심리물리는 Bolanowski et al. 1988.)

- **장갑은 균일하게가 아니라 주파수로 거른다.** 공간적 세부는 죽는다. PC 대역의 진동은
  재료를 타고 전달된다 — 주머니 속 휴대폰 진동이 느껴지는 이유다. 그러므로 진동촉각
  알림은 장갑 낀 작업자에게 남는 유일한 피부 채널이다. 예외는 당신에게 불리하게 설계되어
  있다: 방진 장갑은 정확히 그 대역을 얼마나 감쇠하는가로 인증받는다(ISO 10819).
- **기계가 알림 대역을 마스킹한다.** 동력 공구와 중장비는 광대역 진동을 정확히 PC 영역에
  넣는다. 브레이커를 쥔 같은 손의 손목에 찬 알림은 한 채널 안에서 신호 대 잡음 싸움이다 —
  현장 알림 웨어러블이 조용히 실패하는 이유는 음량이 아니라 마스킹과 순응이다.
- **모집단의 임계값이 이동해 있다.** 장기 진동 노출은 진동촉각 임계값을 올린다 —
  수부진동증후군의 감각신경 성분이다(Brammer, Taylor & Lundborg 1987; 노출 지표는 ISO
  5349-1). 학생에게서 잰 검출 임계값은 착암 작업조에 이전되지 않는다. 주장의 대상인
  모집단에서 재거나, 재지 않았다고 말하라.

### 6. 임계값 너머 — 성능과 작업부하

모든 햅틱 실험이 심리물리 실험은 아니다. 세 계열이 서로 다른 질문에 답하고, 논문은 이를
자주 흐린다:

- **지각**: 사람이 그것을 검출/변별할 수 있는가? (이 페이지의 §1–§2)
- **성능**: 인터페이스가 과제 결과를 바꾸는가? 고전적 도구는 **Fitts의 법칙** — 이동
  시간은 목표 거리 $D$와 폭 $W$에 대한 난이도 지수 $ID = \log_2(2D/W)$와 함께 증가한다 —
  이라서 "햅틱 조건이 난이도를 낮췄다"에는 표준적 조작화가 있다(Fitts 1954).
- **작업부하/경험**: 그것이 사람에게 얼마의 비용이었는가? NASA-TLX(Hart & Staveland
  1988) 계열은 자기보고다. 지각도 과제 시간도 아닌, 실재하는 무언가를 잰다.

"햅틱 피드백이 원격조작을 개선했다" 형태의 주장은 셋 중 무엇을 쟀는지 말해야 한다.
작업부하를 재고 지각을 결론 내린 논문은 중간에 차선을 바꾼 것이다 — 심사자의 용어로는
*구성 타당도*이고, 그 어휘는
[[06-research-practice/research-questions-claims|1. 연구 질문과 주장]]에 있다.

### 읽고 나면 말할 수 있어야 하는 것

- [ ] 절대 임계값, JND, Weber 분율, PSE, 심리측정 함수를 정의한다.
- [ ] 주어진 질문과 예산에 대해 극한법·조정법·항상자극법·계단법 중 하나를 고르고, 각
  절차의 특징적 편향을 말한다.
- [ ] Weber 분율을 하드웨어 사양(양자화, 마찰 바닥)과 코퍼스 타당성 경계로 바꾼다.
- [ ] 세 가지 현장 효과 — 장갑의 주파수 거름, PC 대역의 기계 마스킹, HAVS로 이동한
  임계값 — 와 각각이 알림 설계에 하는 일을 말한다.
- [ ] 햅틱 평가를 지각·성능·작업부하로 분류한다.

### 스스로 점검

1. 항상자극법은 왜 극한법을 괴롭히는 습관화/기대 편향에 강한가?
2. 세 참가자에게서 계단법 시행이 각 40번 나왔다. n은 얼마이고, 왜인가?
3. 장치의 마찰 대역이 0.05 N이고 작업 힘이 2 N이다. 과제 중간에 마찰이 지각되는가(힘
   JND 7%)? 약 0.3 N의 힘 반전 근처에서는?
4. 알림 손목밴드가 실험실에서는 되고 현장에서는 안 된다. 전자회로를 탓하기 전에 채널
   수준의 설명 둘을 대라.
5. 논문이 햅틱 피드백으로 NASA-TLX가 개선됐다고 보고하고 조작자가 "접촉을 더 잘
   지각했다"고 결론 내린다. 무엇이 잘못인가?

> [!tip]- 정답 · Answers
> 1. 피험자가 다음 자극 수준을 예측할 수 없기 때문이다. 강도들을 *무작위 순서*로 여러 번
> 제시하므로 습관화하거나 기대할 상승·하강 진행이 없다. 극한법과 조정법에는 진행 방향이
> 있고, 편향은 그 방향에 올라탄다. 대가는 시행 수다 — 무작위성은 데이터로 값을 치른다.
> 2. $n = 3$. 실험 단위는 시행이 아니라 참가자다
> ([[06-research-practice/experimental-design-reproducibility|2. §1]]). 한 계단법 안의 40번
> 시행은 같은 신경계가 같은 날 만든 것이라 독립이 아니다 — 그 *한 사람*의 임계값을 잘
> 추정하기 위해 존재하는 것이지 표본 40개로 세라고 있는 것이 아니다.
> 3. 과제 중간에는 아니다: 2 N에서의 JND는 $0.07 \times 2 = 0.14$ N이고 마찰 0.05 N은 그보다
> 한참 아래다. 힘 반전 근처에서는 지각된다: 0.3 N에서의 JND는 $0.07 \times 0.3 = 0.021$ N이고
> 같은 0.05 N이 이제 감지 가능한 변화의 두 배가 넘는다. 마찰 사양 하나가 *같은 과제 안에서*
> 지각 불가능하기도 하고 두드러지기도 하다 — 베버 법칙이 "충분히 좋은가"를 장치가 아니라
> 동작점에 대한 질문으로 만드는 이유다.
> 4. §5의 채널 표에서: **차폐(masking)** — 같은 손에 든 공구가 광대역 진동을 알림이 쓰는 바로
> 그 파치니 대역에 밀어 넣으므로, 신호가 한 채널 안에서 잡음과 경쟁한다. 그리고
> **차단/감쇠** — 장갑(방진 장갑은 설계상, ISO 10819)이 손목밴드가 송신하는 그 대역을
> 감쇠시킨다. 둘 다 전자회로가 멀쩡한 채로 실험실 성공과 현장 실패를 예측한다.
> 5. 작업부하를 재고 지각을 결론 냈다. NASA-TLX는 자기보고식 *비용* 측정 — §6의 세 번째
> 계열 — 이라, 탐지가 그대로인데도 좋아질 수 있고(덜 힘들고 지각은 같음) 탐지가 좋아지는데도
> 나빠질 수 있다. 지각 주장에는 심리물리 측정이 필요하다: 탐지나 변별 성능, 이상적으로는
> 강제선택.

### 출처

- G. A. Gescheider, *Psychophysics: The Fundamentals*, 3rd ed., Erlbaum, 1997 — 절차의
  표준 교과서.
- H. Levitt, "Transformed Up-Down Methods in Psychoacoustics," *JASA* 49(2):467–477,
  1971. DOI 10.1121/1.1912375 — 계단법 규칙.
- L. A. Jones, "Matching forces: constant errors and differential thresholds,"
  *Perception* 18(5):681–687, 1989 — 힘 JND ≈ 7%.
- H. Z. Tan, M. A. Srinivasan, B. Eberman, B. Cheng, "Human factors for the design of
  force-reflecting haptic interfaces," *ASME DSC* 55-1, pp. 353–359, 1994 — 힘
  상호작용 설계 표.
- L. A. Jones, I. W. Hunter, "A perceptual analysis of stiffness," *Exp. Brain Res.*
  79:150–156, 1990 — 강성 JND ≈ 23%.
- S. J. Bolanowski, G. A. Gescheider, R. T. Verrillo, C. M. Checkosky, "Four channels
  mediate the mechanical aspects of touch," *JASA* 84(5):1680–1694, 1988 — 채널 대역과
  250 Hz 민감도 피크.
- R. S. Johansson, J. R. Flanagan, "Coding and use of tactile signals from the
  fingertips in object manipulation tasks," *Nat. Rev. Neurosci.* 10:345–359, 2009.
  DOI 10.1038/nrn2621 — 네 구심신경 체계
  ([[04-robotics/tactile-visuotactile|14. 촉각·시촉각 센싱]]에도 인용됨).
- P. M. Fitts, "The information capacity of the human motor system in controlling the
  amplitude of movement," *J. Exp. Psychol.* 47(6):381–391, 1954.
- S. G. Hart, L. E. Staveland, "Development of NASA-TLX (Task Load Index)," *Advances
  in Psychology* 52:139–183, 1988.
- A. J. Brammer, W. Taylor, G. Lundborg, "Sensorineural stages of the hand-arm
  vibration syndrome," *Scand. J. Work Environ. Health* 13(4):279–283, 1987.
- ISO 5349-1:2001, 손 전달 진동 노출; ISO 10819, 방진 장갑 전달률.
- K. E. MacLean, "Haptic interaction design for everyday interfaces," *Reviews of
  Human Factors and Ergonomics* 4:149–194, 2008 — 애초에 햅틱 피드백이 쓸 가치가 있는
  경우.
