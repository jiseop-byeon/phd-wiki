# Papers to fetch through the library

Claims the wiki makes that no openly accessible source could confirm. Each line names
the paper and the one thing to look for. Everything here is currently marked in the wiki
as unverified rather than deleted, so nothing depends on it silently.

Sci-Hub and similar sites were not used. These are the residue of an open-access-only pass.

## Construction and field robotics

| Paper | Identifier | What to check |
|---|---|---|
| Johns et al., 2023 — *A framework for robotic excavation and dry stone construction using on-site materials* | 10.1126/scirobotics.abp9758 | Does the paper say stone grasping and placement are **force-controlled** rather than position-controlled? Find the sentence in the manipulation or execution section that names the control mode. |
| Johns et al., 2023 — same paper | 10.1126/scirobotics.abp9758 | Does the per-stone reconstruction estimate **mass or inertial properties**, or only geometry? The abstract says only "robotic grasping and textured 3D scanning". |
| Lundeen, Kamat, Menassa & McGee, 2019 — *Autonomous motion planning and task execution in geometrically adaptive robotized construction work* | 10.1016/j.autcon.2018.12.020 | Was the joint-filling case study run on a **laboratory testbed or an active site**? The wiki builds its Michigan-line framing on "testbed, not a site" and the abstract never states the venue. |
| Liang, Kamat, Menassa & McGee, 2022 — *Trajectory-Based Skill Learning for Overhead Construction Robots Using Generalized Cylinders with Orientation* | 10.1061/(ASCE)CP.1943-5487.0001004 | Confirm **82.0% against 71.3%**, and what the 71.3% baseline actually is. |
| Davila Delgado et al., 2019 — *Robotics and automated systems in construction: Understanding industry-specific challenges for adoption* | 10.1016/j.jobe.2019.100868 | Does the item-level ranking put **high initial capital investment first overall**? And are the body's four technology categories named as the wiki lists them? |
| Zhang et al., 2021 — *An autonomous excavator system for material loading tasks* | 10.1126/scirobotics.abc3164 | Does the body state a machine-size range up to **49 t**? The abstract says only "compact and standard excavators". |
| Egli, Gaschen, Kerscher, Jud & Hutter, 2022 — *Soil-Adaptive Excavation Using Reinforcement Learning* | 10.1109/LRA.2022.3189834 | Does the method adapt **without ever identifying the soil**, and over what randomized soil-parameter ranges was it trained? |

## Control and optimization

| Paper | Identifier | What to check |
|---|---|---|
| Dietrich, Ott & Albu-Schäffer, 2015 — *An overview of null space projections for redundant, torque-controlled robots* | 10.1177/0278364914566516 | Confirm that a Moore-Penrose null-space projector is already **statically** consistent, and that only the dynamically consistent inverse satisfies $JM^{-1}N^\top = 0$. |
| Axehill & Morari, 2012 — *An alternative use of the Riccati recursion for efficient optimization* | 10.1016/j.sysconle.2011.09.018 | Does the paper state a **flop count quadratic in the horizon** for its Cholesky factorization of the condensed Hessian? Nothing openly accessible gives a rate. |
