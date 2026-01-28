# Torus Network Routing & Latency Simulator

This project is a Python-based simulation environment designed to evaluate the performance of **k-ary n-cube (Torus)** networks. It simulates packet latency, throughput, and received ratios under different routing strategies and traffic loads.

Detailed:https://ieeexplore.ieee.org/document/10062614 

## 🚀 Overview

The simulator models packet movement across a Torus topology, accounting for node distance, buffer constraints, and varying routing algorithms. It uses a cycle-accurate approach to track how packets progress from source to destination.

### Key Features
* **Topology Support**: Flexible k-ary n-cube configuration (e.g., 3D Torus).
* **Routing Algorithms**:
    * **Fixed/Deterministic**: Dimension-order routing.
    * **Randomized**: Randomly selects dimensions to balance load and avoid hotspots.
    * **Congestion-Aware (RC)**: Uses relative congestion logic and packet lifetime markers to manage flow.
* **Performance Metrics**: Automatically calculates Latency (Cycles), Throughput, and Received Ratio.

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `latency.py` /  | Main simulation scripts using **Deterministic Routing** (Dimension-Order). |
|`lat.py`|  Simulation using **Random Walk** routing to distribute traffic. |
| `RW.py` | Implements **Waiting-Time**-based routing logic. |
| `RC.py` | Implements **Cycle-Check**-based routing logic. |
| `torus_dict.py` | Core utility for k-ary conversion, topology mapping, and distance calculation. |
| `torus_rf.py` | Independent routing functions for pathfinding verification. |

---

## ⚙️ Configuration

You can adjust the simulation parameters in the `if __name__ == "__main__":` block of each script:

* **`n`**: Number of nodes in a single dimension (e.g., `n = 9`).
* **`dimension`**: Dimensionality of the torus (e.g., `3` for 3D).
* **`lam` ($\lambda$)**: Traffic load intensity, ranging from 0.05 to 1.0.
* **`max_p`**: Maximum buffer capacity per node (default: 8).
* **`num`**: Number of iterations per simulation point to ensure statistical stability.

---

## 📊 Data Output

The scripts generate `.txt` files containing the results for each routing method:

* `cycles_*.txt`: Average clock cycles per traffic load point.
* `Throughput_*.txt`: Measured network throughput.
* `Received_*.txt`: The ratio of packets successfully delivered vs. injected.

---

## 🏃 Quick Start

1.  **Requirements**:
    * Python 3.x
    * NumPy
    * Matplotlib (optional for visualization)

2.  **Execution**:
    Clone the repository and run any routing simulation:
    ```bash
    python RC.py
    ```

3.  **Visualization**:
    To view the graphs, uncomment the `plt.plot(...)` and `plt.show()` sections at the bottom of the script.

---

## 🔍 Routing Logic Details

The scripts utilize a state-based `mark` system to manage packet status during each cycle:
* `mark = 0`: Packet is at the source node.
* `mark = 1`: Packet is currently traversing the network.
* `mark = 2`: Packet has reached the destination.
* `mark = -1`: Packet transmission complete.
* `mark = -2`: Congestion-based wait/drop signal.