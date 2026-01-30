# Fault-Tolerance Simulator

This repository contains a specialized simulation suite for the **Dimension Extended Dragonfly (DED)** topology, focusing on **Fault-Tolerant Routing** and **Node-Disjoint Path** algorithms. It evaluates network resilience by simulating packet delivery success rates in the presence of random router failures.



## 🚀 Overview

Dimension Extended Dragonfly (DED) improves upon the standard Dragonfly by utilizing a multi-dimensional internal group structure. This suite implements advanced algorithms to find multiple non-overlapping (disjoint) paths between nodes, ensuring connectivity even when several routers are offline.

### Key Features
* **Disjoint Path Algorithms**: Implements `neighbor_jump`, `global_jump`, and `multi_jump` to find multiple redundant paths.
* **Fault-Tolerant Simulation**: Benchmarks the **Success Rate** and **Average Path Length** against a varying percentage of faulty routers (0% to 80%).
* **Multi-Dimensional Routing**: Supports n-dimensional group configurations ($M^N$) with configurable global link density ($L$).

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `fault_tolerant_sim.py` | **Main Entry**: Runs the Monte Carlo simulation to test success rates under different failure scenarios. |
| `disjoint_path.py` | **Algorithm Core**: Contains the logic for finding multiple node-disjoint paths (Neighbor/Global/Multi Jump). |
| `ded_routing.py` | **Basic Routing**: Provides the standard dimension-order routing logic for DED. |
| `DED_dict.py` | **Topology Map**: Generates router IDs and manages the faulty router configuration. |

---

## 💡 Routing Algorithms

The simulator compares three primary routing strategies:

1.  **Basic Path**: The shortest deterministic path. Highly susceptible to failure if any node on the path is faulty.
2.  **Neighbor Jump**: Leverages local neighbors within the n-dimensional group to bypass faulty nodes before attempting global travel.
3.  **Global Jump**: An aggressive redundancy strategy that utilizes diverse global links to route through intermediate groups, enhancing the chance of reaching the destination.
4.  **Multi Jump**: This is the most powerful algorithm in the suite. It is based on the topological principles of dragonfly-like toplogies.



---

## ⚙️ Configuration & Parameters

Adjust these in `fault_tolerant_sim.py`:

* **`M`**: Number of routers per dimension (e.g., `M=4`).
* **`N`**: Number of dimensions in a group (e.g., `N=3`).
* **`L`**: Number of global links per router (e.g., `L=2`).
* **`times`**: Number of source-destination pairs to test per failure rate (default: `100,000`).
* **`epsilon`**: Convergence parameter for the Global Jump algorithm.

---

## 📈 Performance Metrics

The simulation outputs data as the failure rate $\lambda$ (percentage of faulty routers) increases:
* **Success Rate**: The probability that at least one functional disjoint path exists between a random source and destination.
* **Average Path Length**: The mean number of hops for successful deliveries (typically increases as the network routes around failures).

---

## 🏃 Quick Start

1.  **To run the fault-tolerance benchmark**:
    ```bash
    python fault_tolerant_sim.py
    ```
    The results will be saved to `success_ratio.txt` and `average_length.txt`.

2.  **To visualize a single disjoint path calculation**:
    ```bash
    python disjoint_path.py
    ```
    This will print the specific paths found between a random source and destination pair.


