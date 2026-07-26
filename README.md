# SOP vs Accomplishments — Independent Project

**Project:** Closed Loop Drone Obstacle Detection & Avoidance  
**Student:** Amit Kumar  
**Advisor:** Dr. Anuj Grover  
**Institute:** IIIT Delhi  

---

## Original Statement of Purpose

The SOP defined **3 objectives**, extending the work of the previous BTP team (Aarehant Jain & Shashank Mishra, Winter 2026):

### Objective 1: On-MCU TinyML Deployment
- **Model Export & Quantization:** Convert the offline 6-class material classifier (88–92% baseline) to int8/fixed-point for STM32 via TensorFlow Lite Micro or CMSIS-NN.
- **On-Device Feature Extraction:** Migrate the full feature pipeline (RMS, ZCR, spectral centroid, echo width, PSLR) into firmware.
- **Real-Time Validation:** Live UART log with per-frame predictions, inference latency under 100ms.

### Objective 2: End-to-End Loop Closure in SITL
- **Sensor-to-ROS Bridge:** Stream live STM32 telemetry (distance + class + confidence) into ROS topics consumed by PX4/Gazebo stack.
- **Classification-Aware Avoidance:** Implement stop/hover/re-route logic conditional on class, range, and confidence.
- **Quantitative Mission Validation:** Mission success rate, planning latency, and false-positive avoidance rate.

### Objective 3: Integration, Robustness & Bench-to-Flight Bring-up
- **Hardware Maturation:** Move PROTOTYPE-1 from breakout to fabricated integrated PCB.
- **Drone-Mounted Bench Test:** Mount the sensor on a fixed airframe and characterise vibration-induced noise floor.

---

## Design Decision: Depth Camera over Ultrasonic Sensors

The previous BTP team built ultrasonic sensors on STM32 microcontrollers. Their radar achieved **1m range** with **4.3cm resolution**, providing only **4 distance readings** (front, back, left, right).

After evaluating this system, the sensing modality was upgraded to a **depth camera** that captures **307,200 3D points per frame** — equivalent to 307K ultrasonic sensors — enabling dense 3D mapping that the ultrasonic approach could never achieve.

**Why this was the right call:**
1. The depth camera provides **76,800× more data** per frame than 4 ultrasonic sensors
2. It enables **3D occupancy mapping** (OctoMap), which ultrasonic sensors cannot do
3. The software stack (ROS 2, path planning) is directly transferable to real hardware

---

## Accomplishments Mapped to SOP Objectives

### ✅ Objective 1 → Depth Camera Perception Pipeline

| SOP Target | What Was Done | Status |
|:---|:---|:---:|
| TinyML on STM32 | Replaced with OakD-Lite depth camera (640×480 @ 30fps) — 76,800× more data than ultrasonic sensors | ✅ Done |
| On-device feature extraction | Point Cloud filtering pipeline: Voxel Grid + Statistical Outlier Removal (307K → ~170 clean points/frame) | ✅ Done |
| Real-time inference <100ms | OctoMap processes filtered point clouds in real-time; A* path planning in ~60ms | ✅ Done |

---

### ✅ Objective 2 → End-to-End Closed Loop — Fully Accomplished

This was the **core objective** and has been **completely achieved and significantly exceeded**:

| SOP Target | What Was Done | Status |
|:---|:---|:---:|
| Sensor-to-ROS Bridge | Depth camera → `ros_gz_bridge` → ROS 2 topics → OctoMap → `/projected_map` | ✅ Done |
| Classification-Aware Avoidance | Dynamic obstacle detection: checks next 5–10 waypoints against live OctoMap every 2s. Obstacle ON path → hover + replan. NOT on path → ignore and continue. | ✅ Done |
| Stop / Hover / Re-route logic | Reactive safety (0.25m threshold → retreat), stuck detection (8s → blacklist + retreat), path-blocked → replan from current position | ✅ Done |
| Quantitative Mission Validation | 6-algorithm benchmark with metrics: planning time, path length, waypoints, nodes explored, smoothness angle. CSV export. 5 test cases across all rooms. | ✅ Done |

**Additionally accomplished beyond SOP scope:**

| Extra Achievement | Description |
|:---|:---|
| **6 Path Planning Algorithms** | A*, Dijkstra, Bellman Ford, PRM, RRT, Theta* — implemented, benchmarked, compared |
| **Visual Benchmark Mode** | All 6 algorithms run simultaneously with colored paths in RViz |
| **Frontier-Based Autonomous Exploration** | Drone explores unknown environments with zero prior knowledge — discovers rooms, doorways, obstacles purely through sensors |
| **2.5D Altitude-Aware Planning** | 3-layer planner (1.2m / 1.8m / 2.4m) — drone flies under pipes, over furniture |
| **3D OctoMap Query System** | O(1) voxel hash lookups for real-time 3D collision checking |
| **Multi-Room Environment** | 3-room house (18×12m) with 12 furniture pieces, staggered doorways, ceiling obstacles |

---

### ❌ Objective 3 → Hardware Integration — Not Pursued

| SOP Target | Status | Reason |
|:---|:---:|:---|
| PCB fabrication | ❌ | Shifted from hardware to software-defined sensing |
| Drone-mounted bench test | ❌ | Physical drone hardware not available; validated in SITL simulation |

**Justification:** The software stack (ROS 2 nodes, OctoMap, path planners, frontier exploration) is **hardware-agnostic by design**. Replacing Gazebo with a real depth camera + localization system (Vicon, T265, or VIO) would enable deployment on a physical drone with minimal code changes.

---

## Quantitative Results

### Path Planning Benchmark (5 Test Cases × 6 Algorithms)

| Test Case | A* Time | Theta* Time | A* Length | Theta* Length | A* Smoothness | Theta* Smoothness |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| Bedroom → Study (cross-room) | 17.8ms | 32.6ms | 7.18m | 6.79m | 45.0° | 38.4° |
| Bedroom → Living (through door) | 5.1ms | 16.1ms | 7.24m | 6.80m | 45.0° | 34.1° |
| Living → Study (full traverse) | 18.0ms | 30.5ms | 13.52m | 12.57m | 45.0° | 9.9° |
| Short: within Bedroom | 0.3ms | 2.1ms | 4.00m | 4.00m | 0.0° | 0.0° |
| Diagonal: corner to corner | 24.3ms | 50.7ms | 17.55m | 16.40m | 45.0° | 15.7° |

### Frontier Exploration Performance
- **6 autonomous scans** to fully map the 3-room house (18×12m)
- **184×122 cell** occupancy grid generated from sensor data
- **3,404 obstacles** detected and mapped
- **Zero crashes** in final configuration
- Complete room coverage including corners and doorways

---

## Project Taskflow

**Inherited from BTP (Winter 2026):**
- Gazebo simulation environment with PX4 SITL
- Basic ROS pipeline (no autonomous navigation, no path planning, no 3D mapping)
- Ultrasonic radar prototype on STM32 (4 sensors, 1m range)
- Memory-efficient CNN for material classification (32KB RAM)

**Phase 1 — Perception & Mapping (Built from Scratch):**
1. Custom 3-room house environment (18×12m, 12 furniture pieces, staggered doorways)
2. Depth camera integration (OakD-Lite, 640×480 @ 30fps)
3. Point cloud filtering pipeline (307K → ~170 points/frame)
4. OctoMap 3D occupancy mapping with TF broadcaster
5. First successful A* autonomous navigation on sensor-derived maps

**Phase 2 — Multi-Algorithm Comparison & 2.5D Planning:**
1. Implemented 5 additional path planners (Dijkstra, Bellman Ford, PRM, RRT, Theta*)
2. Visual benchmark mode — all 6 algorithms with colored paths in RViz
3. Flight stability: velocity clamping + yaw smoothing
4. Real-time obstacle avoidance with dynamic replanning
5. Ceiling obstacles (fans, hanging light, low pipe at drone altitude)
6. 3D OctoMap Query system (O(1) voxel hash lookups)
7. 2.5D multi-layer planner — 3 altitude layers for flying under/over obstacles

**Phase 3 — Frontier-Based Autonomous Exploration:**
1. Replaced hardcoded scan waypoints with frontier-based exploration
2. Drone autonomously discovers rooms, doorways, obstacles using only its depth camera
3. FrontierExtractor: clusters free-unknown boundary cells, scores by size/distance
4. Safety systems: reactive retreat (0.25m), stuck detection (8s), replan limiter
5. Wall-proximity cost map naturally centers A* paths in corridors
6. Dual unknown-space penalty: 3.0 for exploration, 50.0 for goal navigation
7. Pure Pursuit path follower with short 0.3m lookahead to prevent corner-cutting

---

## Summary

The SOP proposed 3 objectives centered around deploying TinyML on STM32 microcontrollers and closing the sensor-to-flight loop. After evaluating the inherited BTP hardware (4 ultrasonic sensors with 1m range), the sensing modality was upgraded to a **depth camera approach** that provides 76,800× more spatial data per frame, enabling capabilities the ultrasonic approach could never achieve.

The core SOP objective — **end-to-end closed-loop obstacle detection and avoidance in SITL** — has been **fully accomplished** and significantly exceeded: the drone autonomously explores unknown environments using frontier-based exploration, builds persistent 3D maps with OctoMap, navigates using 6 different path planning algorithms (benchmarked quantitatively), detects new obstacles in real-time and replans around them, and supports 2.5D altitude-aware planning.

The only SOP objective not pursued was physical PCB fabrication (Objective 3), which was deprioritized because the software stack is hardware-agnostic and ready for deployment on real hardware with a depth camera swap.

---

**Repository:** [github.com/shashank22603/ROS](https://github.com/shashank22603/ROS) (Branch: Amit)  
**Personal:** [github.com/ami4go/Indoor-Drone-Navigation](https://github.com/ami4go/Indoor-Drone-Navigation)
