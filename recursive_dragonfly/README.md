# Recursive Dragonfly (RDF) Network Simulator

This repository contains a Python-based simulation suite for the **Recursive Dragonfly (RDF)** topology. RDF extends the standard Dragonfly hierarchy by applying a recursive construction, enabling the network to scale to an extreme number of nodes while maintaining low diameter and efficient routing.

Detailed:https://ieeexplore.ieee.org/document/10391640

## 🚀 Overview

The Recursive Dragonfly topology uses a base Dragonfly structure as a building block and tiles it recursively. This simulator models the complex group-to-group mappings and the hierarchical routing required to navigate multiple levels of recursion.

### Key Features
* **Recursive Structure Support**: Implements group ID and router ID calculations based on the number of recursions (`N`).
* **Hierarchical Routing**: Features a multi-level routing algorithm that resolves destinations by climbing up and down the recursive layers.
* **Packet Dropping Algorithm**: Simulates network congestion by dropping packets when target switch buffers exceed the `max_p` threshold.
* **Scalability Metrics**: Evaluates performance (Latency, Throughput, Loss) as a function of recursive depth and injection rate ($\lambda$).

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `latency.py` | **Core Simulator**: The main engine for cycle-accurate simulation. Implements the recursive packet-moving logic and data collection. |
| `RDF_dict.py` | **Topology Generator**: Contains the recursive `group_id` calculation and the `dct` function to map the multi-level switch hierarchy. |

---

## ⚙️ Configuration & Parameters

You can customize the network scale in the `if __name__ == "__main__":` block of `latency.py`:

* **`N`**: The number of **recursive levels** (e.g., `N=2` means a dragonfly within a dragonfly).
* **`M`**: Number of routers in the base group.
* **`K`**: Number of compute nodes connected to each router.
* **`L`**: Number of global links per router.
* **`max_p`**: Buffer capacity (default: 16). 
* **`lam` ($\lambda$)**: Traffic load (injection rate).

---

## 🔍 Recursive Routing & Drop Logic

### Routing Mechanism
The `routing` and `drouting` functions handle the recursive pathfinding:
1.  **Identity Check**: The algorithm identifies which recursive level the current group and destination group diverge at.
2.  **Level Resolution**: Packets are routed to the specific gateway router that connects the current recursive level to the next, until the destination group is reached.
3.  **Local Delivery**: Once the packet reaches the target group at the lowest level, it is delivered to the target router and compute node.
4.  **lossless routing**: You can comment the marked codes to execute a lossless simulation.

### Dropping Mechanism
To prevent infinite queuing and model realistic high-load behavior:
* **Buffer Check**: Before every hop, the simulator queries the `dct` for the target switch's current occupancy.
* **Drop Condition**: If the current packet does not reach its destination node on the scheduled hops(thr), the packet is removed from the network.
* **Metrics**: The `u` array tracks the total number of dropped packets to calculate the **Drop Packet Ratio**.

---

## 📊 Performance Metrics

The simulation tracks four primary data points for each load level:
1.  **Average Latency**: Cycles taken for successfully received packets.
2.  **Throughput**: Total successful deliveries per cycle.
3.  **Received Ratio**: The fraction of total injected packets that were successful.
4.  **Drop Ratio**: The fraction of packets lost rate.

---

## 🏃 Quick Start

1.  **Prerequisites**:
    ```bash
    pip install numpy
    ```

2.  **Run Simulation**:
    ```bash
    python latency.py
    ```

3.  **Output Analysis**:
    The script prints results in the format: `lam, Latency, Throughput, Received_Ratio, Drop_Ratio`. You can capture this output or uncomment the plotting code to generate visual graphs.