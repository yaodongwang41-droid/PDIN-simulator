# Mirrored k-ary n-tree (MiKANT) Network Simulator

This project implements a cycle-accurate simulation for **Mirrored k-ary n-tree (MiKANT)** topologies. It is designed to evaluate network performance—specifically latency, throughput, and packet delivery ratios—under varying traffic loads and routing conditions.

Detailed:https://ieeexplore.ieee.org/document/8560259


## 🚀 Features

- **Topology Support**: Implements the Mirrored k-ary n-tree structure, a hierarchical network specialized for high-performance interconnects.
- **Hierarchical Routing**: Models the distinctive **Upward phase** (towards the root) and **Downward phase** (towards the leaf nodes) of tree-based networks.
- **Flow Control**: Simulates buffer capacity and congestion using a Virtual Channel (VC) style logic with a configurable `max_p` threshold.
- **Performance Metrics**:
    - **Latency**: Average cycles per packet delivery.
    - **Throughput**: Effective data rate under specific injection rates.
    - **Received Ratio**: Efficiency of the network in delivering injected packets.

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `lantency_mikant.py` | The main simulation engine. Contains the `routing_la` function which handles the complex upward/downward logic and cycle-by-cycle state updates. |
| `switch_dict.py` | Utility script for managing the network's logical structure. Includes k-ary conversion, switch/node dictionary generation, and random traffic configuration. |

---

## ⚙️ Key Parameters

You can customize the network scale and simulation intensity in the `if __name__ == "__main__":` block of `lantency_mikant.py`:

* **`k`**: The arity of the tree (number of children per node).
* **`n`**: The height/levels of the tree.
* **`max_p`**: Buffer size (maximum packets per switch) to simulate congestion and back-pressure.
* **`lam` ($\lambda$)**: Traffic load (packet injection rate). The simulation typically iterates through a range of `lam` to find the saturation point.
* **`num`**: Number of simulation repetitions to calculate a statistically significant average.

---

## 🔍 Routing Logic (MiKANT)

The simulator uses a `mark` state machine to track each packet's journey:
1. **Upward Phase**: Packets climb the tree to reach a common ancestor or the root level (`sl` increases).
2. **Turnaround**: Once the highest necessary point is reached, the packet switches to the downward phase.
3. **Downward Phase**: Packets descend towards the specific target group (`sg`) and destination node (`sl` decreases).
4. **Flow Control**: If the target switch buffer is full (`>= max_p`), the packet is held in the current switch, simulating network back-pressure.

---

## 📊 Outputs

The simulation generates data points printed to the console and stored in arrays (`y`, `z`, `w`), which can be used to plot:
- **Latency vs. Traffic Load**
- **Throughput vs. Traffic Load**
- **Delivery Success Ratio**

---

## 🏃 Quick Start

1. **Prerequisites**:
   ```bash
   pip install numpy matplotlib