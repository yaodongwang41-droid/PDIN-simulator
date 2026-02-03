# Multi-Topology Network Performance Simulation Suite

This repository provides a comprehensive simulation framework for evaluating and comparing various high-performance network topologies. It implements cycle-accurate packet-level simulations to analyze latency, throughput, and reliability across different interconnection strategies.

## 🌟 Key Simulation Characteristics

* **Traffic Pattern**: All simulations are conducted under **Uniform Traffic Load**. Sources and destinations are distributed uniformly across the entire network to evaluate baseline performance.
* **Buffer Model**: Routers/Switches are designed with **Multi-Queue (Virtual Channels)** support. Congestion management is handled via a configurable `max_p` threshold, simulating realistic back-pressure and buffer saturation.
* **Flow Control**: Depending on the topology, the suite uses either **Lossless Flow Control** (back-pressure) or **Packet Dropping Algorithms** to manage network overflow.

---

## 🏗 Supported Topologies

This suite covers a wide spectrum of network architectures, from classical direct networks to advanced hierarchical structures:

### 1. Classical Direct Networks
* **Torus (k-ary n-cube)**: A multi-dimensional grid with wrap-around links. Supports deterministic and randomized dimension-order routing.
* **Hypercube (n-cube)**: A specialized case of the torus where each dimension has a size of 2, offering high bisection bandwidth and low diameter.

### 2. Hierarchical Tree Topologies
* **k-ary n-tree (Fat-Tree)**: A standard multi-stage tree topology using **Nearest Common Ancestor (NCA)** routing with adaptive upward path selection.
* **Mirrored k-ary n-tree (MiKANT)**: An optimized tree structure that effectively reduced average distance and cost through mirror structure.

### 3. High-Radix Dragonfly Variants
* **Dragonfly**: A cost-effective high-radix topology utilizing groups of fully connected routers with sparse global inter-group connectivity.
* **Dimension Extended Dragonfly (DED)**: Enhances local group connectivity by replacing the internal cliques with n-dimensional meshes/tori.
* **Recursive Dragonfly (RDF)**: A highly scalable version of Dragonfly that tiles base groups recursively to support exascale system requirements.



---

## 🛠 Project Structure

Each topology is organized into its own set of scripts:

| Topology Group | Core Logic | Dictionary/Map | Simulation Entry |
| :--- | :--- | :--- | :--- |
| **Torus** | `BC.py`, `RW.py`, `RC.py` | `torus_dict.py` | `lat.py` |
| **Hypercube** | `BC.py`, `RW.py`, `RC.py` | `cube_dict.py` | `hypercube_latency.py` |
| **MiKANT** | `lantency_mikant.py` | `switch_dict.py` | `lantency_mikant.py` |
| **Fat-Tree** | `kant_routing.py` | `kant_dict.py` | `latency.py` |
| **Dragonfly** | `dragonfly.py` | `DF_dict.py` | `latency.py` |
| **DED / RDF** | `basic_routing.py` | `EDD_dict.py` / `RDF_dict.py` | `latency.py` |

---

## ⚙️ Global Configuration

Common parameters across all simulations:

* **`lam` ($\lambda$)**: Injection rate per node (offered load).
* **`max_p`**: Buffer capacity(packets).
* **`num`**: Number of simulation iterations to ensure statistical convergence.

---

## 🔍 Performance Metrics

The suite evaluates the following key performance indicators (KPIs):

1.  **Average Latency**: The mean number of clock cycles required for a packet to travel from source to destination.
2.  **Throughput**: The total number of packets successfully delivered per clock cycle.
3.  **Received Ratio**: The efficiency of the network (Delivered Packets / Injected Packets).
4.  **Drop Ratio** (Dragonfly variants): The percentage of packets discarded due to congestion.

---

## 🏃 Quick Start

To run a simulation for a specific topology (e.g., Dragonfly):

1.  Navigate to the directory.
2.  Execute the latency script:
    ```bash
    python latency.py
    ```
3.  The results will be written to the current directory as `Latency, Throughput, Received_Ratio, Drop_Ratio`.

---

