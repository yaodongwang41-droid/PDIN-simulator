# Dragonfly Network Topology & Latency Simulator

This repository contains a Python simulation suite for the **Dragonfly** interconnect topology. It evaluates network performance by modeling packet traversal across local and global links, including a specific implementation of packet-dropping algorithms to handle extreme congestion.

Detailed:https://ieeexplore.ieee.org/document/4556717

[Image of Dragonfly network topology]


## 🚀 Overview

Dragonfly is a high-radix topology that reduces network diameter by organizing routers into fully connected groups. This simulator tracks packets as they move between nodes, routers, and groups, providing a cycle-accurate analysis of latency and throughput.

### Key Features
* **Packet Dropping Logic**: Unlike simple back-pressure models, this simulator calculates a **Drop Packet Ratio**, allowing analysis of network reliability under heavy loads.
* **Basic Routing**: Implements basic routing across local (intra-group) and global (inter-group) links.
* **Comprehensive Metrics**: Tracks Latency, Throughput, Received Ratio, and Drop Ratio.

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `latency.py` | The main simulation engine. Runs the cycle-accurate simulation across a range of traffic loads ($\lambda$). |
| `dragonfly.py` | **Routing Demo & Logic**: Contains the core routing function and a utility to calculate the hop-by-hop path length between nodes. |
| `DF_dict.py` | **Topology Generator**: Handles the mapping of Group/Router/Node IDs and generates the initial network configuration. |

---

## ⚙️ Configuration & Parameters

You can adjust the network scale in the `if __name__ == "__main__":` block of `latency.py`:

* **`K`**: Number of compute nodes connected to each router.
* **`M`**: Number of routers in each group.
* **`L`**: Number of global links per router (connecting to other groups).
* **`max_p`**: Buffer capacity per router (default: 12).
* **`lam` ($\lambda$)**: Injection rate, simulated from 0.05 to 0.9.
* **`num`**: Number of simulation iterations per data point.

---

## 🔍 Routing & Dropping Logic

The simulation follows a specific state machine (`ind`):
1.  **Injection (`ind=0`)**: Packet attempts to enter the source router.
2.  **Traversing (`ind=1`)**:
    * If destination is in a **different group**: The packet moves to the specific router that holds the global link to the target group.
    * If destination is in the **same group**: The packet moves directly to the target router.
3.  **Dropping**: If the current packet does not reach its destination node on the scheduled hops(thr), the packet is removed from the network.
4.  **Reception (`ind=-1`)**: Successful delivery to the destination node.
5.  **lossless routing**: You can comment the marked codes to execute a lossless simulation.
---

## 📊 Performance Indicators

The script outputs five key values per simulation step:
1.  **$\lambda$**: Traffic Load.
2.  **Average Latency**: Average clock cycles per successful delivery.
3.  **Throughput**: Total packets delivered per cycle.
4.  **Received Ratio**: Percentage of injected packets delivered.
5.  **Drop Ratio**: Percentage of injected packets dropped due to congestion.

---

## 🏃 Quick Start

1.  **Prerequisites**:
    ```bash
    pip install numpy
    ```

2.  **Run a Path Test**:
    To see the routing logic and hop count between two random nodes:
    ```bash
    python dragonfly.py
    ```

3.  **Run Full Simulation**:
    To generate performance data across various traffic loads:
    ```bash
    python latency.py
    ```