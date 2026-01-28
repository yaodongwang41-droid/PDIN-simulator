# k-ary n-tree (Fat-Tree) Network Simulator

This repository contains a Python-based simulation suite for **k-ary n-tree** (often referred to as Fat-Tree) network topologies. It models packet latency, throughput, and delivery success rates, incorporating Virtual Channel (VC) buffer management and randomized adaptive routing.

Detailed:https://ieeexplore.ieee.org/document/580853

## 🚀 Key Features

- **Topology Configuration**: Supports customizable `k` (arity) and `n` (height) to simulate various scales of Fat-Tree networks.
- **NCA Routing**: Implements the **Nearest Common Ancestor** routing logic, consisting of:
    - **Upward Phase**: Packets climb to a switch that can reach the destination.
    - **Downward Phase**: Packets descend through a specific deterministic path to the target node.
- **Congestion Modeling**: Uses a `max_p` threshold to simulate buffer limits and back-pressure flow control.
- **Interactive Demonstration**: Includes a dedicated script to visualize the hop-by-hop routing path.

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `latency.py` | The core performance simulator. Runs cycle-accurate tests over various traffic loads ($\lambda$). |
| `kant_routing.py` | **Routing Demo**: A simplified script that prints the step-by-step switch IDs a packet traverses from source to destination. |
| `kant_dict.py` | Utility library for generating k-ary representations, switch/node dictionaries, and traffic patterns. |

---

## ⚙️ Simulation Parameters

In `latency.py`, you can tune the network environment:

* **`k`**: The number of ports/children per switch (e.g., `k=4`).
* **`n`**: The number of stages/levels in the tree.
* **`max_p`**: Buffer capacity per switch (default: 8).
* **`lam` ($\lambda$)**: Packet injection rate range (simulated via `np.arange`).
* **`num`**: Number of simulation iterations per data point to ensure accuracy.

---

## 🔍 Routing Logic Overview

The simulation handles packets based on their `mark` state:

1. **Source Injection (`mark=0`)**: Checks if the source switch has available buffer space.
2. **Upward Routing**: If the current switch cannot reach the destination directly, it moves up to a higher level. In this implementation, the upward path is **randomly selected** among available parents to balance load.
3. **NCA Reach**: Once the Nearest Common Ancestor is reached, the packet enters the **Downward Phase (`mark=1`)**.
4. **Downward Routing**: The path becomes deterministic, moving down through specific switches to the target.
5. **Flow Control**: Packets are only moved if the target switch buffer is below `max_p`.

---

## 📈 Outputs

The simulation tracks and outputs:
- **Average Latency**: Measured in clock cycles.
- **Throughput**: Successfully delivered packets per cycle.
- **Received Ratio**: The percentage of injected packets that reached their destination.

---

## 🏃 How to Run

### 1. View a Routing Path Example
To see how a packet moves through the switch levels:
```bash
python kant_routing.py