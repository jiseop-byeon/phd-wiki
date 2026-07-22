---
title: 6. Signal Processing
tags: [foundations]
---

> [[02-foundations/overview|0. Overview]] — 이 페이지에 필요한 사전 수학과 다른 지식과의 연결 지도 · prerequisites & connection map

## English

Every sensor a construction robot carries — camera, LiDAR, IMU, encoder — hands you a
sampled, noisy signal. Course-depth treatment: convolution worked by hand, the sampling
theorem with its math, DFT/FFT, filter design basics, and the bridge to control's transfer
functions.

### 1. Signals, systems, and convolution

- A system is **LTI** (linear, time-invariant) ⟺ completely characterized by its impulse
  response $h$; the output is **convolution**:
  $$y[n] = (x * h)[n] = \sum_k x[k]\, h[n-k]$$
- Worked example: $x = [1, 2, 3]$, $h = [1, 1]$ (a running sum):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — flip, slide, multiply, accumulate.
  Length: $N_x + N_h - 1$.
- A CNN layer is exactly a *learned bank* of such $h$'s in 2D (plus nonlinearity) —
  [[01-canonical-papers/notes/alexnet|AlexNet]] onward; "padding/stride" are the boundary and
  sampling choices of this same operation.
- Key properties: commutative, associative (cascaded LTI systems = one convolved $h$),
  and the delta $\delta[n]$ is the identity.

### 2. Sampling — the contract between continuous and digital

- **Nyquist–Shannon**: a signal with no content above $B$ Hz is *perfectly* recoverable
  from samples at $f_s > 2B$. Above $f_s/2$, content **aliases**: frequency $f$ appears at
  $|f - kf_s|$ — wheels spin backwards on camera; a 60 Hz vibration sampled at 50 Hz
  masquerades as 10 Hz.
- Therefore: **anti-alias filter before downsampling**, always (this includes decimating
  IMU logs in software).
- Engineering corollary: pick sensor rates from the fastest dynamics you must *observe*,
  with margin — a 10 Hz perception loop cannot even see, let alone damp, a 50 Hz vibration.
- Quantization: finite bits add ~uniform noise (~6 dB SNR per bit) — the *other* half of
  digitization.

### 3. Frequency domain — the diagonalizing basis

- Fourier's claim: signals = sums of sinusoids. Deeper claim: **complex exponentials are
  the eigenfunctions of LTI systems** ([[02-foundations/linear-algebra|eigen-thinking]]) —
  a sinusoid in gives the same sinusoid out, scaled by $H(f)$. That is why frequency
  analysis diagonalizes filtering.
- **DFT**: $X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j2\pi kn/N}$ — correlation of the signal
  with each basis frequency; **FFT** computes all $N$ in $O(N\log N)$.
- **Convolution theorem**: $x * h \leftrightarrow X \cdot H$ — filtering is multiplication
  in frequency; also the lens for neural nets' spectral bias (they fit low frequencies first).
- Signal fingerprints: white noise = flat spectrum; drift/bias = spike near DC; rotating
  machinery = sharp peaks at harmonics (an excavator's engine band is a notch-filter target).

### 4. Filtering — design basics

- **FIR** (finite impulse response, $y = \sum b_k x[n-k]$): always stable, exactly linear
  phase possible (no waveform distortion), needs more taps. The moving average is the
  simplest FIR; its frequency response $|H(f)| = |\sin(\pi f M)/(M\sin \pi f)|$ shows the
  tradeoff: longer window ⇒ narrower passband *and* more delay.
- **IIR** (feedback, e.g., $y[n] = \alpha y[n-1] + (1-\alpha)x[n]$ — the exponential
  smoother): cheap and sharp, but can ring and go unstable; phase is nonlinear.
- Choosing: low-pass for sensor noise, high-pass for drift removal, notch at known
  vibration harmonics, complementary filters to fuse IMU accel (low-passed) + gyro
  (high-passed).
- **Phase lag is the price of causal smoothing**: every causal low-pass delays the signal —
  aggressive filtering *fights your controller* (a lagged velocity estimate destabilizes a
  D-term). This is the practical reason to prefer model-based estimation:
  the **Kalman filter** ([[02-foundations/probability|derived here]]) is the optimal
  time-varying filter once signal + noise are written as a state-space model.

### 5. Bridge to control: transforms

- The Laplace transform (continuous) / **Z-transform** (discrete) generalize Fourier:
  convolution ↦ multiplication by a *transfer function* $H(s)$ or $H(z)$.
- Poles of $H$ = eigenvalues of the state-space $A$
  ([[02-foundations/linear-algebra|control connection]]): stability = poles in the left
  half-plane (continuous) / inside the unit circle (discrete). Filters, plants, and
  controllers all speak this one language — which is why the control-theory course packet
  and this page are two views of the same object.

### 6. Sensor-pipeline habits (field-tested)

- Log **raw**, filter later; never filter twice implicitly (driver + your code).
- Timestamp at the sensor, synchronize clocks before fusing (extrinsics *and* time offsets
  for camera-LiDAR-IMU).
- Check the spectrum before choosing a filter: name the noise before you fight it.

### Self-check

1. Convolve $x = [1, 0, -1]$ with $h = [1, 2, 1]$ by hand, and give the output length.
2. An IMU samples at 200 Hz; a motor vibrates at 170 Hz. Where does the vibration appear
   in the data, and what should have been done?
3. Derive the frequency response of the 2-point moving average and find the frequency it
   nulls completely.
4. Why does a Kalman filter typically beat a hand-tuned low-pass for velocity estimation
   in a control loop? (Two reasons: one about lag, one about models.)

## 한국어

건설로봇이 싣고 다니는 모든 센서 — 카메라, LiDAR, IMU, 엔코더 — 는 샘플링된, 노이즈 낀
신호를 건네준다. 교재 수준의 서술: 손으로 푸는 합성곱, 수식이 있는 샘플링 정리, DFT/FFT,
필터 설계 기초, 그리고 제어의 전달함수로 가는 다리.

### 1. 신호, 시스템, 합성곱

- **LTI**(선형 시불변) 시스템 ⟺ 임펄스 응답 $h$로 완전히 특성화; 출력은 **합성곱**:
  $$y[n] = (x * h)[n] = \sum_k x[k]\, h[n-k]$$
- 계산 예제: $x = [1, 2, 3]$, $h = [1, 1]$(연속 합):
  $y = [1,\ 1{+}2,\ 2{+}3,\ 3] = [1, 3, 5, 3]$ — 뒤집고, 밀고, 곱하고, 누적한다.
  길이: $N_x + N_h - 1$.
- CNN 층은 정확히 이런 $h$들의 *학습된 2D 묶음*(+ 비선형성)이다 —
  [[01-canonical-papers/notes/alexnet|AlexNet]] 이후 전부; "패딩/스트라이드"는 같은 연산의
  경계·샘플링 선택지다.
- 핵심 성질: 교환·결합 법칙(직렬 LTI = 합성곱된 $h$ 하나), $\delta[n]$이 항등원.

### 2. 샘플링 — 연속과 디지털 사이의 계약

- **나이퀴스트–섀넌**: $B$ Hz 위 성분이 없는 신호는 $f_s > 2B$ 샘플에서 *완벽히* 복원된다.
  $f_s/2$ 위의 성분은 **에일리어싱**된다: 주파수 $f$가 $|f - kf_s|$에 나타난다 —
  카메라 속 바퀴가 거꾸로 돌고, 50 Hz로 샘플링한 60 Hz 진동은 10 Hz로 위장한다.
- 따라서: **다운샘플링 전 안티에일리어스 필터**, 항상 (소프트웨어에서 IMU 로그를 솎아낼
  때도 포함).
- 공학적 따름정리: *관측해야 할* 가장 빠른 동역학에서 여유를 두고 센서 주기를 정하라 —
  10 Hz 인식 루프는 50 Hz 진동을 감쇠는커녕 보지도 못한다.
- 양자화: 유한 비트는 거의 균일한 노이즈를 더한다(비트당 약 6 dB SNR) — 디지털화의
  나머지 절반.

### 3. 주파수 영역 — 대각화하는 기저

- 푸리에의 주장: 신호 = 사인파들의 합. 더 깊은 주장: **복소 지수함수는 LTI 시스템의
  고유함수다** ([[02-foundations/linear-algebra|고유값적 사고]]) — 사인파가 들어가면 같은
  사인파가 $H(f)$배 되어 나온다. 주파수 분석이 필터링을 대각화하는 이유가 이것이다.
- **DFT**: $X[k] = \sum_{n=0}^{N-1} x[n]\, e^{-j2\pi kn/N}$ — 신호와 각 기저 주파수의
  상관; **FFT**가 $N$개 전부를 $O(N\log N)$에 계산.
- **합성곱 정리**: $x * h \leftrightarrow X \cdot H$ — 필터링은 주파수 영역의 곱;
  신경망의 스펙트럼 편향(저주파부터 맞춘다)을 이해하는 렌즈이기도 하다.
- 신호의 지문: 백색 잡음 = 평평한 스펙트럼; 드리프트/바이어스 = DC 근처 스파이크;
  회전 기계 = 고조파의 날카로운 피크 (굴착기 엔진 대역은 노치 필터의 표적).

### 4. 필터링 — 설계 기초

- **FIR** (유한 임펄스 응답, $y = \sum b_k x[n-k]$): 항상 안정, 정확한 선형 위상
  가능(파형 왜곡 없음), 대신 탭이 많이 필요. 이동 평균이 가장 단순한 FIR; 그 주파수 응답
  $|H(f)| = |\sin(\pi f M)/(M\sin \pi f)|$이 트레이드오프를 보여준다: 창이 길수록 통과
  대역이 좁아지고 *그리고* 지연이 커진다.
- **IIR** (피드백, 예: $y[n] = \alpha y[n-1] + (1-\alpha)x[n]$ — 지수 평활기): 싸고
  날카롭지만 링잉·불안정 가능; 위상이 비선형.
- 선택: 센서 노이즈엔 저역통과, 드리프트 제거엔 고역통과, 알려진 진동 고조파엔 노치,
  IMU 융합엔 상보 필터(가속도 저역 + 자이로 고역).
- **위상 지연은 인과적 평활화의 대가다**: 모든 인과적 저역통과는 신호를 늦춘다 — 과한
  필터링은 *제어기와 싸운다*(지연된 속도 추정이 D항을 불안정하게 만든다). 모델 기반
  추정을 선호하는 실전적 이유가 이것이다: 신호+노이즈를 상태공간 모델로 쓰면
  **칼만 필터**([[02-foundations/probability|여기서 유도]])가 최적 시변 필터다.

### 5. 제어로 가는 다리: 변환

- 라플라스 변환(연속) / **Z-변환**(이산)은 푸리에의 일반화: 합성곱 ↦ *전달함수*
  $H(s)$ 또는 $H(z)$와의 곱.
- $H$의 극점 = 상태공간 $A$의 고유값
  ([[02-foundations/linear-algebra|제어 연결]]): 안정성 = 극점이 좌반평면(연속) /
  단위원 안(이산). 필터, 플랜트, 제어기가 전부 이 하나의 언어를 쓴다 — 제어이론 교재와
  이 페이지가 같은 대상의 두 시점인 이유다.

### 6. 센서 파이프라인 습관 (현장 검증됨)

- **원시** 데이터로 기록하고 필터링은 나중에; 암묵적 이중 필터링(드라이버 + 내 코드) 금지.
- 센서에서 타임스탬프를 찍고, 융합 전에 시계를 동기화(카메라-LiDAR-IMU의 외부 파라미터
  *그리고* 시간 오프셋).
- 필터를 고르기 전에 스펙트럼부터 봐라: 싸울 노이즈의 이름부터 알아내라.

### 스스로 점검

1. $x = [1, 0, -1]$과 $h = [1, 2, 1]$을 손으로 합성곱하고 출력 길이를 말하라.
2. IMU가 200 Hz로 샘플링하는데 모터가 170 Hz로 진동한다. 진동은 데이터의 어디에
   나타나고, 무엇을 했어야 하는가?
3. 2점 이동 평균의 주파수 응답을 유도하고, 완전히 소거되는 주파수를 찾아라.
4. 제어 루프의 속도 추정에서 칼만 필터가 손튜닝 저역통과를 보통 이기는 이유는?
   (두 가지: 하나는 지연, 하나는 모델에 관한 것.)
