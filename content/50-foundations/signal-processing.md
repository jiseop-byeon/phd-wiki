---
title: Signal Processing · 신호처리
tags: [foundations]
---

## English

Every sensor a construction robot carries — camera, LiDAR, IMU, encoder — hands you a
sampled, noisy signal. This page is the minimum theory to handle them honestly, plus the
places it secretly reappears inside deep learning.

### 1. Signals & LTI systems

- A system is **LTI** (linear, time-invariant) ⇒ completely characterized by its impulse
  response $h$; output is **convolution** $y = x * h$.
- Convolution intuition: slide, weight, accumulate — a learned bank of small $h$'s is
  exactly a CNN layer ([[canonical-papers/notes/alexnet|AlexNet]] onward).

### 2. Sampling

- **Nyquist–Shannon**: sampling at $f_s$ captures content below $f_s/2$; anything above
  folds back as **aliasing** (why wheels spin backwards on camera, why IMUs need
  anti-alias filtering before downsampling).
- Practical corollary: choose sensor rates from the dynamics you must observe — a 10 Hz
  perception loop cannot stabilize a 50 Hz vibration.

### 3. Frequency domain

- Fourier: any signal = sum of sinusoids; the **DFT** computes it on samples, the **FFT**
  makes it $O(N\log N)$.
- Convolution in time = multiplication in frequency — the reason filtering is cheap and the
  lens for understanding "low-frequency bias" of neural networks.
- Spectra of common signals: white noise (flat), drift (low-frequency), vibration (peaks).

### 4. Filtering

- FIR (moving average — always stable, linear phase) vs IIR (cheap, sharper, can ring).
- Low-pass to suppress sensor noise, high-pass to remove drift, notch for known vibration
  frequencies (e.g., excavator engine bands).
- The Kalman filter is the *optimal* time-varying filter once you write signal + noise as a
  state-space model — the bridge from this page to [[50-foundations/probability|probability]]
  and [[20-robotics/index|control]].

### 5. Sensor-pipeline habits

- Log raw, filter later; never filter twice implicitly (driver + your code).
- Beware phase lag: every causal low-pass delays the signal — aggressive smoothing fights
  the controller.
- Synchronize clocks before fusing (camera-LiDAR-IMU extrinsics *and* time offsets).

### 6. Where it appears in this wiki

- CNN = learned convolution filters ([[canonical-papers/notes/alexnet|AlexNet]], [[canonical-papers/notes/vgg|VGG]])
- Diffusion noise schedules = shaping the spectrum of injected Gaussian noise
- IMU/LiDAR preprocessing for site perception ([[30-construction-robotics/index|construction robotics]])

## 한국어

건설로봇이 싣고 다니는 모든 센서 — 카메라, LiDAR, IMU, 엔코더 — 는 샘플링된, 노이즈 낀
신호를 건네준다. 이 페이지는 그것들을 정직하게 다루기 위한 최소 이론과, 그 이론이
딥러닝 안에서 몰래 재등장하는 지점들이다.

### 1. 신호와 LTI 시스템

- **LTI**(선형 시불변) 시스템 ⇒ 임펄스 응답 $h$로 완전히 특성화되고, 출력은 **합성곱** $y = x * h$
- 합성곱의 직관: 밀고, 가중하고, 누적한다 — 작은 $h$들의 학습된 묶음이 정확히 CNN 층이다
  ([[canonical-papers/notes/alexnet|AlexNet]] 이후 전부).

### 2. 샘플링

- **나이퀴스트–섀넌**: $f_s$로 샘플링하면 $f_s/2$ 아래 성분만 담긴다; 그 위의 성분은
  **에일리어싱**으로 접혀 들어온다 (카메라에 바퀴가 거꾸로 도는 이유, IMU를 다운샘플링
  전에 안티에일리어스 필터링해야 하는 이유).
- 실전 따름정리: 관측해야 할 동역학에서 센서 주기를 정하라 — 10 Hz 인식 루프로는
  50 Hz 진동을 안정화할 수 없다.

### 3. 주파수 영역

- 푸리에: 모든 신호 = 사인파의 합; 샘플에서는 **DFT**가 계산하고 **FFT**가 $O(N\log N)$으로 만든다.
- 시간 영역의 합성곱 = 주파수 영역의 곱 — 필터링이 싼 이유이자, 신경망의 "저주파 편향"을
  이해하는 렌즈.
- 흔한 신호의 스펙트럼: 백색 잡음(평평), 드리프트(저주파), 진동(피크).

### 4. 필터링

- FIR(이동 평균 — 항상 안정, 선형 위상) vs IIR(저렴, 날카롭지만 링잉 가능).
- 센서 노이즈엔 저역통과, 드리프트 제거엔 고역통과, 알려진 진동 주파수(굴착기 엔진 대역 등)엔 노치.
- 신호+노이즈를 상태공간 모델로 쓰면 칼만 필터가 *최적* 시변 필터가 된다 — 이 페이지와
  [[50-foundations/probability|확률]], [[20-robotics/index|제어]]를 잇는 다리.

### 5. 센서 파이프라인 습관

- 원시 데이터로 기록하고 필터링은 나중에; 암묵적 이중 필터링(드라이버 + 내 코드) 금지.
- 위상 지연 주의: 모든 인과적 저역통과는 신호를 늦춘다 — 과한 평활화는 제어기와 싸운다.
- 융합 전에 시계부터 동기화 (카메라-LiDAR-IMU의 외부 파라미터 *그리고* 시간 오프셋).

### 6. 이 위키에서 등장하는 곳

- CNN = 학습된 합성곱 필터 ([[canonical-papers/notes/alexnet|AlexNet]], [[canonical-papers/notes/vgg|VGG]])
- 디퓨전 노이즈 스케줄 = 주입되는 가우시안 노이즈의 스펙트럼 성형
- 현장 인식을 위한 IMU/LiDAR 전처리 ([[30-construction-robotics/index|건설로봇]])
