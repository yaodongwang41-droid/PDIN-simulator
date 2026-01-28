# Dimension Extended Dragonfly (EDD) Network Simulator

This repository contains a Python-based simulation suite for the **Dimension Extended Dragonfly (EDD)** topology. EDD enhances the standard Dragonfly by introducing a multi-dimensional structure within each group, further optimizing local routing and network scalability.

Detailed:https://onlinelibrary.wiley.com/doi/10.1002/cpe.8286


## 🚀 Overview

The EDD topology organizes routers into groups, but unlike the basic Dragonfly, routers within a group are connected via a multi-dimensional (n-dimensional) mesh/torus-like structure. This simulator tracks packet movements through these dimensions, managing inter-group global links and intra-group local links.

### Key Features
* **N-Dimensional Intra-group Routing**: Supports multi-dimensional router layouts within each group (defined by parameters `M` and `N`).
* **Packet Dropping Algorithm**: Models realistic network behavior by dropping packets when they encounter buffer saturation (`max_p`).
* **Cycle-Accurate Simulation**: Tracks latency, throughput, and packet loss across various traffic injection rates ($\lambda$).
* **Flexible Scale**: Easily adjustable dimensionality, group size, and link density.

---

## 🛠 File Structure

| File | Description |
| :--- | :--- |
| `latency.py` | **Core Simulator**: Executes the performance test, tracks packet states, and calculates metrics. |
| `basic_routing.py` | **Routing Demo**: Provides a hop-by-hop path demonstration and calculates shortest-path lengths for EDD. |
| `EDD_dict.py` | **Topology Generator**: Creates the router/node mapping for the dimension-extended structure. |

---

## ⚙️ Configuration & Parameters

You can customize the simulation in the `if __name__ == "__main__":` block of `latency.py`:

* **`N`**: The dimension of each group (e.g., `N=3`).
* **`M`**: The number of routers in each dimension of a group.
* **`K`**: The number of compute nodes connected to each router.
* **`L`**: The number of global links per router.
* **`max_p`**: Buffer capacity (default: 12). If the target buffer exceeds this value.
* **`lam` ($\lambda$)**: Offered traffic load range (injection rate).

---

## 🔍 Routing & Drop Logic

### Routing Phases
1.  **Injection (`ind=0`)**: The packet enters the network at the source router.
2.  **Inter-Group Phase**: If the destination is in a different group, the packet routes through the internal dimensions of the current group to find the specific router with a global link to the target group.
3.  **Intra-Group Phase**: Once in the target group, the packet uses n-dimensional routing to reach the target router.
4.  **Reception (`ind=-1`)**: Packet delivered to the compute node.

### Dropping Mechanism
This simulation implements a "Drop-Packets" policy:
* Before moving a packet to any router, the simulator checks the target router's occupancy.
* If the current packet does not reach its destination node on the scheduled hops(thr), the packet is removed from the network.
* This is quantified as the **Drop Ratio** in the simulation results.

---

## 📊 Performance Indicators

The script outputs data for each load point ($\lambda$):
- **Latency**: Average cycles for delivered packets.
- **Throughput**: Rate of packets successfully reaching their destination.
- **Received Ratio**: Percentage of offered load delivered.
- **Drop Ratio**: Percentage of offered load dropped due to congestion.

---

## 🏃 How to Run

1.  **Run a Routing Path Demo**:
    ```bash
    python basic_routing.py
    ```

2.  **Run the Full Performance Simulation**:
    ```bash
    python latency.py
    ```

3.  **Visualization**:
    You can uncomment the `matplotlib` section at the end of `latency.py` to plot the result curves.