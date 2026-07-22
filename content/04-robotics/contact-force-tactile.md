---
title: 9. Contact, Force & Tactile Interaction
tags: [robotics, contact, manipulation, tactile]
---

## English

Once a robot touches the world, geometry alone is insufficient. Contact introduces forces, friction, impacts, changing modes, deformation, and uncertainty. These effects are central to grasping, assembly, excavation, wiping, drilling, and handling flexible materials.

> [!info] Depth target
> Read contact-rich manipulation papers by identifying the contact model, sensing, control mode, material assumptions, and evaluation. Detailed complementarity solvers and continuum mechanics remain optional working/mastery topics.

> [!note] Prerequisites
> [[02-foundations/linear-algebra|Linear Algebra]] · [[02-foundations/optimization|Optimization]] · [[04-robotics/modern-robotics/ch05-velocity-kinematics|Statics and Jacobians]] · [[04-robotics/modern-robotics/ch08-dynamics|Dynamics]] · [[04-robotics/modern-robotics/ch12-grasping|Grasping]]

### 1. Why contact changes the problem

A contact is typically **unilateral**: objects may push but do not pull through an ordinary surface. Motion can switch among separation, impact, sticking, and sliding. This makes the dynamics hybrid and often nonsmooth.

For a gap $\phi(q)\ge 0$ and normal force $f_n\ge 0$, ideal rigid contact is summarized by

$$\phi(q)f_n=0$$

If separated, force is zero; if normal force is positive, the gap is closed. This complementarity is an idealized model, not a literal description of material deformation.

### 2. Normal force and friction

Coulomb friction is commonly approximated by

$$\lVert f_t\rVert\le \mu f_n$$

where $f_n$ is normal force, $f_t$ tangential force, and $\mu$ the friction coefficient. Forces inside the friction cone can be consistent with sticking; boundary or exceeded conditions indicate impending or actual slip under the model. Real friction depends on material, speed, pressure, wear, and surface state.

### 3. Rigid and compliant models

| Model | Useful when | Main limitation |
|---|---|---|
| Rigid contact | deformation is small relative to task scale | impacts and mode switches are nonsmooth |
| Penalty/compliant contact | simulation needs continuous penetration forces | stiffness and damping are hard to identify |
| Learned/residual model | repeatable mismatch remains in data | extrapolation and physical consistency |

Simulator contact parameters are often numerical compromises. Success under one simulator setting is not evidence of robustness to real material variation.

### 4. Grasp and wrench language

A contact force produces a force and moment—a **wrench**—on the object. The grasp map combines contact forces into an object wrench. **Form closure** immobilizes an object through geometry under a specified contact model; **force closure** uses admissible contact forces, commonly including friction, to resist arbitrary external wrenches. Required contact counts depend on dimension, friction and contact assumptions, and general-position conditions.

### 5. Position, force, impedance, and admittance

| Mode | What is regulated |
|---|---|
| Position control | pose or trajectory error |
| Force control | measured contact force |
| Impedance control | desired relationship from motion error to force |
| Admittance control | desired motion response to measured force |

Impedance does not simply “control both position and force.” It shapes interaction behavior, often as a virtual mass–spring–damper. Admittance is useful when a stiff, accurate position-controlled robot can convert measured force into a compliant motion command.

### 6. Worked example: cleaning a wall

A pure position controller commands the tool 2 cm beyond an estimated wall. A 1 cm wall-location error can cause very different force because contact stiffness is high. An impedance controller instead permits pose error while shaping the restoring force; a force controller regulates normal force directly but still needs tangential motion and stability handling. The best architecture depends on actuator bandwidth, sensing, surface variation, and safety limits.

### 7. Force, tactile, and material state

- Wrist force/torque sensing measures net wrench but not the full pressure distribution.
- Tactile arrays can estimate contact location, pressure, shear, and slip cues.
- Proprioception observes the robot internally; exteroception senses the external world.
- Vision can observe global geometry while tactile sensing resolves local contact ambiguity.

Rope, cloth, soil, wet concrete, cables, and bulk material have high-dimensional, changing state. Their behavior depends on history and unobserved material properties, making representation and prediction difficult.

### 8. Learning and sim-to-real

Learning may estimate residual dynamics, contact state, friction/material properties, grasp scores, or a tactile-conditioned policy. Domain randomization can broaden training conditions, but the chosen randomization distribution defines what variation was covered. Privileged simulator state can aid training while being unavailable at deployment; check how the policy replaces it at test time.

### 9. Evaluation and paper language

Measure task success, peak/mean force, force-tracking error, slip/drop rate, object or surface damage, recovery, safety violations, and robustness across materials and friction. “Contact-rich,” “compliant,” and “robust” require explicit task and perturbation definitions.

> [!warning] Reading the claim
> A higher task success rate does not identify whether the gain came from tactile sensing, better control, safer force limits, or easier contact conditions. Look for matched baselines and ablations across sensing, controller, material, and initialization.

### After reading

- Explain unilateral contact and complementarity qualitatively.
- Interpret the friction-cone inequality and its assumptions.
- Distinguish form closure from force closure.
- Compare force, impedance, and admittance control.
- Identify what tactile sensing adds beyond wrist force and vision.
- Audit material variation and contact-related failure metrics.

### Self-check

1. Why can increasing position gain be dangerous during contact?
2. A tangential force is 6 N, normal force 10 N, and $\mu=0.5$. Is sticking allowed by the simple cone?
3. Why may a policy trained with one friction coefficient fail even with perfect perception?
4. What should a tactile-policy ablation hold constant?

> [!tip]- Answers
> 1. Small pose/model errors can generate large forces and instability. 2. No: $6>0.5\times10=5$ N. 3. Feasible forces, slip transitions, and dynamics change. 4. Demonstrations, architecture capacity, controller, initialization, materials, and evaluation protocol; remove or replace tactile information without making the rest easier.

### Sources

- [Modern Robotics, Chapter 12](http://modernrobotics.org)
- [MIT Manipulation](https://manipulation.csail.mit.edu/)

## 한국어

로봇이 세계와 닿는 순간 기하만으로는 부족하다. 접촉에는 힘, 마찰, 충격, sticking/sliding/separation 모드 전환, 변형과 불확실성이 들어온다. 이는 파지뿐 아니라 조립, 굴착, 닦기, 천공과 유연 물체 취급의 핵심이다.

$\phi(q)f_n=0$은 떨어져 있으면 접촉력이 0이고 접촉력이 있으면 gap이 닫힌다는 이상적 rigid-contact 논리다. $\lVert f_t\rVert\le\mu f_n$은 Coulomb friction cone의 기본 표현이며 실제 마찰은 재료·속도·압력·마모에 따라 달라진다.

Position control은 pose, force control은 접촉력, impedance control은 motion error와 force의 관계, admittance control은 측정 힘에 대한 motion response를 조절한다. “Impedance가 위치와 힘을 동시에 제어한다”로 단순화하지 말고 어떤 interaction dynamics를 만들었는지 확인해야 한다.

Form closure와 force closure의 조건은 차원, 마찰과 contact model에 의존한다. Tactile policy 논문에서는 성공률뿐 아니라 force, slip, damage, recovery와 재료 변화, privileged information, simulator contact 설정을 확인하라.

위 영어 절의 예제·After reading·Self-check로 접촉 모델과 sensing/control/evaluation의 관계를 점검하라.
