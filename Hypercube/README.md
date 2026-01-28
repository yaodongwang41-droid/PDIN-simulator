# n-cube (Hypercube) Network Routing & Latency Simulator

This repository provides a Python-based simulation environment for evaluating performance metrics in an **n-dimensional Hypercube (n-cube)** network topology. It calculates packet latency, throughput, and received ratios across various routing algorithms under different traffic loads ($\lambda$).

Detailed:https://ieeexplore.ieee.org/document/10062614 

---

## 🚀 Overview

The simulator models a cycle-accurate network where packets are injected into an n-cube structure. It tracks how packets traverse dimensions based on specific routing logic while respecting node buffer capacities.




## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `BC.py` | Simulation using **Basic Deterministic** routing logic. |
| `hypercube_latency.py` | Simulation using **Random Walk** routing logic.|
| `RW.py` | Implements **Waiting-Time**-based routing logic. |
| `RC.py` | Implements **Cycle-Check**-based routing logic. |
| `cube_dict.py` | Core utility for generating node mappings (bit strings), calculating Hamming distances, and configuring traffic. |

---

## ⚙️ Configuration

You can modify key parameters within the `if __name__ == "__main__":` block of each script:

* **`n`**: The dimension of the hypercube (e.g., `n = 10` results in $2^{10} = 1024$ nodes).
* **`lam` ($\lambda$)**: Traffic load intensity (packet injection rate).
* **`max_p`**: Maximum buffer capacity per node (typically set to 6).
* **`num`**: Number of simulation iterations to ensure statistical stability.

---

## 📊 Performance Tracking

The scripts utilize a state-based `mark` system to manage packet status in each cycle:
* `mark = 0`: Packet is at the source node.
* `mark = 1`: Packet is in transit through the network.
* `mark = 2`: Packet has reached the destination.
* `mark = -1`: Packet successfully received/retired.
* `mark = -2`: Transmission halted for the current cycle due to congestion.

Results are automatically saved to `.txt` files (e.g., `cycles_rrc.txt`, `Throughput_rw.txt`) for later analysis.

---

## 🏃 How to Run

1.  **Requirements**:
    * Python 3.x
    * NumPy
    * Matplotlib (optional for live graphing)

2.  **Run a specific simulation**:
    ```bash
    python BC.py
    ```

3.  **Visualization**:
    To see the performance curves, uncomment the `plt.plot(...)` and `plt.show()` sections at the bottom of the scripts.