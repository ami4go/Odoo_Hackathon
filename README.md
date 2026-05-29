# Understanding the Previous BTP Report
### *"Design and Development of Electronic Systems – Drone"*
**By:** Aarehant Jain & Shashank Mishra | **Advisor:** Dr. Anuj Grover | **Date:** April 2026

---

## What Is This Project About? (In Simple Words)

Imagine you want a small drone to fly **inside a room** (like a warehouse or tunnel) **all by itself** — no human with a remote control. The drone needs to:

1. **See** what is around it (walls, obstacles, people)
2. **Think** about what it sees (is that a wall? how far is it?)
3. **Decide** where to fly next (avoid the wall, take a safe path)

The previous team built the **brain and eyes** for this drone using cheap, tiny computer chips (microcontrollers). They worked on **three big pieces**:

---

## The Three Big Pieces

### Piece 1: The "Eyes" — Ultrasonic Radar (Chapters 1 & 5)

**What it is:** A small radar system that sends out sound waves (like a bat!) and listens for the echo to measure distance to objects.

**How it works (simple version):**
1. The chip generates a **chirp** — a sound that sweeps from 35 kHz to 45 kHz (too high for humans to hear)
2. The chirp bounces off a wall and comes back
3. The chip measures **how long** the echo took to return
4. Using basic math: `distance = speed x time / 2`, it calculates how far the wall is

**Hardware used:**
- **STM32G071** microcontroller (a tiny chip with only 32 KB of RAM!)
- **Murata MA40S4S** ultrasonic speakers/microphones
- Analog amplifiers and filters on a breadboard

**What they achieved:**
- Detects objects up to **1 meter** away
- Resolution of about **4.3 cm** (can tell apart two objects that are 4.3 cm apart)
- Later upgraded to **4 sensors** (front, back, left, right) running simultaneously using a second chip (**STM32F303RE**)

**Problems they ran into:**
- Sensors interfered with each other (crosstalk) — solved by clever timer-based triggering
- Timer channel conflicts on the chip — solved by reassigning hardware timers

---

### Piece 2: The "Brain" — Memory-Efficient CNN (Chapters 2, 3 & 4)

**What it is:** A way to run a neural network (AI) on a tiny chip that has almost no memory.

**Why it matters:** Normal AI models need gigabytes of RAM. Their chip has only **32 KB**. They figured out how to squeeze a neural network into this tiny space.

**How they did it (simple version):**
1. They modeled the neural network as a **graph** (boxes connected by arrows)
2. Each box (layer) needs some memory to store its temporary results
3. They figured out the **optimal order** to run the layers so that memory usage stays as low as possible
4. Key trick: **reuse memory buffers** — when one layer is done, its memory can be given to the next layer

**Techniques used:**
- **Stripe streaming:** Process the image in small horizontal strips instead of all at once
- **Knapsack optimization:** Choose which layers to recompute vs. store (like a packing problem)
- **Topological sorting:** Run layers in the correct dependency order

**Results:**
- Reduced peak memory usage by **30-50%** compared to naive execution
- Made it possible to run CNNs that would otherwise be impossible on 32 KB RAM

---

### Piece 3: The "Navigation System" — ROS + Gazebo Simulation (Chapters 6, 7 & 8)

**What it is:** The software pipeline that takes sensor data and makes the drone fly autonomously in a simulated room.

**The pipeline (step by step):**

Depth Camera -> Point Cloud -> OctoMap (3D Map) -> Path Planner -> PX4 -> Drone Moves

**Step 1 — Depth Camera (Chapter 6):**
- A simulated camera in Gazebo that gives depth (distance) for every pixel
- Output format: **PointCloud2** (a list of thousands of 3D points representing the room)
- They applied filters to clean up noisy data:
  - **Statistical outlier removal** — removes random wrong points
  - **Voxel grid filtering** — simplifies the point cloud by averaging nearby points into cubes

**Step 2 — 3D Mapping with OctoMap (Chapter 7):**
- Takes the point cloud and builds a **3D map** of the room
- Uses an **octree** data structure (divides space into smaller and smaller cubes)
- Very memory-efficient — only stores cubes that actually contain obstacles
- Uses **ray casting** to determine which space is free vs. occupied

**Step 3 — Path Planning with DWA (Chapter 8):**
- **DWA = Dynamic Window Approach** — a local path planner
- The drone samples many possible paths (different speeds and turn rates)
- Each path is scored by a **cost function**: cost = a x heading + b x distance + c x velocity
  - Heading: is the path pointing toward the goal?
  - Distance: does the path stay far from obstacles?
  - Velocity: does the path maintain good speed?
- The path with the **lowest cost** wins and the drone follows it

**Software stack they used:**
- **ROS 1 Noetic** — robot middleware
- **Gazebo Classic 11** — 3D physics simulator
- **MAVROS** — bridge between ROS and PX4
- **PX4 v1.13** — flight controller firmware

---

## The Overall System Architecture

This is the most important diagram from the report (Figure 8.3, Page 31):

```
SENSORS (Depth Camera, LiDAR, Sonar)
        |
        v
PointCloud Generator
(Convert sensor data to 3D point cloud)
        |
        v
Local Planner Node (Obstacle avoidance logic)
  - Histogram Builder (2D obstacle map)
  - Cost Calculator (Score paths)
        |
        v
STAR Planner (Path search)
        |
        v
Avoidance Setpoint Publisher
(Publishes /trajectory /setpoint)
        |
        v
MAVROS Node (ROS to PX4 Bridge)
        |
        v
PX4 Flight Stack (Flight Controller)
        |
        v
DRONE MOVES
```

---

## What Has Already Been Done vs. What We Need To Do

| **Already Done (by previous team)** | **Our Job (carry forward)** |
|---|---|
| Built FMCW ultrasonic radar on STM32 | Set up the simulation environment (Done in Week 0) |
| Multi-sensor simultaneous sensing (4 directions) | Upgrade the software stack from ROS 1 to ROS 2 (Done) |
| Memory-efficient CNN execution planner | Replace MAVROS with XRCE-DDS bridge (Done) |
| PointCloud processing pipeline in simulation | Integrate real sensor data into the new ROS 2 pipeline |
| OctoMap-based 3D mapping | Re-implement OctoMap in ROS 2 ecosystem |
| DWA path planning with cost function | Test and validate path planning in our indoor world |
| Ran everything in ROS 1 + Gazebo Classic | Migrate the full pipeline to ROS 2 + Gazebo Sim |

---

## What We Have Done So Far (Week 0)

We set up the **foundation** for carrying this project forward:

1. **Installed Ubuntu 22.04** with ROS 2 Humble (replacing ROS 1 Noetic)
2. **Compiled PX4 v1.14** in SITL (Software-In-The-Loop) mode
3. **Built Micro-XRCE-DDS Agent** (replacing MAVROS) — verified the bridge connection
4. **Created a custom 10x8x3m indoor world** in Gazebo Sim with wireframe walls
5. **Verified sensor topics** — IMU running at 248.5 Hz (expected ~250 Hz)
6. **Recorded baseline flight data** — 60-second hover test with 11,807 odometry samples
7. **Measured position hold accuracy** — horizontal drift only 0.04m (very stable)

---

## How We Plan To Carry This Forward

### Phase 1: Perception (Weeks 1-2)
- Add a **simulated depth camera** to our Gazebo drone model
- Write a ROS 2 node that converts depth images to PointCloud2
- Apply the same **statistical outlier removal** and **voxel grid filtering** from the report

### Phase 2: Mapping (Weeks 3-4)
- Integrate **OctoMap** with ROS 2 to build a 3D map of our indoor room
- Visualize the occupancy grid in RViz2

### Phase 3: Planning (Weeks 5-6)
- Implement the **DWA local planner** as a ROS 2 node
- Use the cost function from the report to score and select safe trajectories
- Test obstacle avoidance in the 10x8x3m room

### Phase 4: Integration (Weeks 7-8)
- Connect the full pipeline: Camera -> PointCloud -> OctoMap -> DWA -> PX4
- Run end-to-end autonomous navigation in simulation
- Compare results with the previous team's findings

---

## Key Terms Cheat Sheet (for the meeting)

| Term | What It Means |
|---|---|
| **FMCW Radar** | A type of radar that uses a sweeping frequency chirp to measure distance |
| **STM32** | A family of cheap, low-power microcontroller chips |
| **CNN** | Convolutional Neural Network — an AI model that recognizes patterns in images |
| **SRAM** | The tiny amount of working memory on a microcontroller (32 KB here) |
| **PointCloud2** | A ROS data format — a collection of thousands of 3D points representing objects |
| **OctoMap** | A 3D mapping library that represents space as occupied/free using octrees |
| **Octree** | A tree data structure that recursively divides 3D space into 8 smaller cubes |
| **DWA** | Dynamic Window Approach — a real-time path planning algorithm |
| **PX4** | Open-source flight controller software that runs on drone hardware |
| **SITL** | Software-In-The-Loop — running PX4 in simulation instead of on real hardware |
| **ROS** | Robot Operating System — middleware that connects robot software components |
| **MAVROS** | Old bridge between ROS 1 and PX4 (uses MAVLink protocol) |
| **XRCE-DDS** | New bridge between ROS 2 and PX4 (uses DDS protocol, faster) |
| **Gazebo** | A 3D physics simulator where we test the drone virtually |

---
---

# 🎯 OUR FOCUS: Objective 2 — End-to-End Loop Closure in SITL

> The previous team built the sensor, the AI model, and the simulation — but **never connected them**. The sensor data never actually reached the drone's flight controller. Our job is to **close this loop**.

```
STM32 Sensor → [??? GAP ???] → ROS Topics → Planner → PX4 → Drone Moves
```
**The "???" is our job.**

---

## Our 3 Specific Tasks

### Task A: Sensor-to-ROS Bridge
Stream live STM32 data into ROS topics that PX4 can consume.

**Plan:**
1. STM32 sends data via UART: `{distance: 0.45, class: "glass", confidence: 0.91}`
2. We write a ROS 2 node that reads serial, parses it, and publishes:
   - `/sensor/distance` (Float32)
   - `/sensor/material_class` (String)
   - `/sensor/confidence` (Float32)
3. In SITL, we **mock** this data using a virtual sensor until real hardware is ready

---

### Task B: Classification-Aware Avoidance
Make the drone **react differently** based on what the sensor reports.

| Sensor Input | Drone Reaction |
|---|---|
| Any obstacle < 0.3m | **Emergency stop** — hover immediately |
| Hard surface (metal/concrete) at 0.3-0.8m | **Reroute** — plan alternative path |
| Soft surface (fabric/foam) at 0.3-0.8m | **Slow down** — proceed cautiously |
| Low confidence (< 70%) | **Hover** — wait for more readings |
| No obstacle detected | **Continue** — follow planned trajectory |

**Implementation:** A ROS 2 avoidance node subscribes to sensor topics and publishes modified trajectory setpoints to `/fmu/in/trajectory_setpoint` or emergency commands to `/fmu/in/vehicle_command`.

---

### Task C: Quantitative Mission Validation
Run test scenarios and measure performance with hard numbers.

| Metric | What It Measures | Target |
|---|---|---|
| **Mission Success Rate** | % of runs where drone reaches goal without crashing | > 90% |
| **Planning Latency** | Time from detection to avoidance maneuver | < 200ms |
| **False-Positive Rate** | How often drone avoids a phantom obstacle | < 5% |
| **False-Negative Rate** | How often drone misses a real obstacle | 0% |

**Test scenarios:** (1) Straight flight toward wall, (2) Corridor navigation, (3) Multi-obstacle room, (4) Material-dependent (glass vs. curtain)

---

## Week-by-Week Plan

| Week | Focus | Deliverable |
|---|---|---|
| **Week 0** | Environment setup & baseline | Verified toolchain, hover data (DONE) |
| **Week 1** | Add depth camera to Gazebo drone | Simulated sensor publishing PointCloud2 |
| **Week 2** | Build Sensor-to-ROS bridge node | Mock STM32 data as ROS 2 topics |
| **Week 3** | Implement avoidance decision logic | Drone stops when obstacle detected |
| **Week 4** | Add material-aware behavior | Different reactions per material type |
| **Week 5** | Build test scenarios in Gazebo | 4 structured mission scenarios |
| **Week 6** | Quantitative validation | Success rate, latency, false-positive rate |
| **Week 7** | Connect real STM32 (from Team 1) | Live UART data into ROS 2 |
| **Week 8** | Final integration & report | End-to-end demo + documentation |

---

## What To Tell The Tutor

> "The previous team built the sensor hardware (ultrasonic FMCW radar) and the AI classifier, and set up a ROS/Gazebo simulation with a path planner. However, these components were never connected — the sensor data never reached the drone's control system. Our objective is to **close this loop** by building a Sensor-to-ROS bridge, implementing classification-aware avoidance logic, and validating everything with quantitative metrics in SITL. In Week 0, we have set up the entire simulation toolchain using ROS 2 Humble, PX4 v1.14, and Gazebo Sim, and verified that the baseline environment is working correctly."

