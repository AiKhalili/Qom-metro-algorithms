# Qom Metro Algorithms

**Algorithm Design Course — Final Project | Bu-Ali Sina University | Spring 2026 (1405)**

A complete, unified implementation of the graph algorithms behind a full metro-network design, optimization, and operations pipeline, built for the *"From Qom to New York"* case study: a fictional technical hiring track run by **UrbanPulse Dynamics**, applied to the real single-line metro network of Qom, Iran. All five project rounds — from basic graph modeling to advanced routing algorithms — are implemented on **one shared graph** and **one cohesive object-oriented codebase**.

> **Course instructor:** Dr. Mohammad Javad Davari
> **Team Members:** Zeinab Khalili, Fatemeh Shabani

---

## Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Data Model — The Qom Metro Graph](#data-model--the-qom-metro-graph)
- [Round 1 — Initial Acceptance](#round-1--initial-acceptance)
- [Round 2 — Infrastructure Design](#round-2--infrastructure-design)
- [Round 3 — Daily Metro Operations](#round-3--daily-metro-operations)
- [Round 4 — Network Performance Analysis](#round-4--network-performance-analysis)
- [Round 5 — Innovation (Bonus)](#round-5--innovation-bonus)
- [Algorithms & Complexity Reference](#algorithms--complexity-reference)
- [Testing](#testing)
- [Design Decisions & SOLID Principles](#design-decisions--solid-principles)

---

## Overview

Per the project brief, the engineering team must design and implement the full algorithmic backbone of the Qom metro system — from basic graph modeling to simultaneously managing hundreds of trains, capacity analysis, and fuzzy station search — on the **real single line currently under construction in Qom** (20 stations). This repository's approach:

- **One shared graph** (`Graph` in `src/graph/graph.py`) reused across all five rounds — no isolated, per-task graph implementations, as explicitly required by the project brief.
- **Modular, object-oriented architecture**: every algorithm lives in its own class under `src/algorithms/`, depending only on the `Graph` interface — never on data sources or UI code.
- **A single unified entry point** (`main.py`) with an interactive menu exposing the complete workflow of all five rounds.
- **Full right-to-left (RTL) rendering support** for Persian station names in the terminal (optional, via `arabic-reshaper` and `python-bidi`).

---

## Project Structure

```
Qom-metro-algorithms/
├── main.py                          # Entry point; interactive 5-round menu
├── pytest.ini                       # pytest config (pythonpath = src)
├── src/
│   ├── graph/
│   │   ├── edge.py                  # Edge class: destination, distance, time, weight, capacity
│   │   └── graph.py                 # Graph class: adjacency list + node/edge management
│   ├── data/
│   │   ├── qom_metro_data.py        # STATIONS and CONNECTIONS extracted from the project brief
│   │   └── qom_metro_capacity_data.py  # Per-edge capacity for T4.2 (Max-Flow)
│   ├── data_structures/
│   │   ├── union_find.py            # Disjoint Set with path compression + union by rank
│   │   ├── train.py                 # Train entity (time interval + priority)
│   │   ├── trip_record.py           # Passenger trip record for operational analytics
│   │   └── passenger.py             # Passenger entity for gate-queue simulation
│   ├── algorithms/
│   │   ├── reachability.py          # T1.2 — BFS
│   │   ├── shortest_path.py         # T1.3 — Dijkstra
│   │   ├── mst.py                   # T2.1 — Prim
│   │   ├── kruskal.py               # T2.1/T2.2 — Kruskal + Union-Find
│   │   ├── dag_shortest_path.py     # T2.3 — Shortest path on a DAG
│   │   ├── express_line.py          # Builder for the directed express-line graph
│   │   ├── bellman_ford.py          # T2.4 — Bellman-Ford + negative-cycle detection
│   │   ├── incentive_network.py     # Builder for the negative-weight incentive graph
│   │   ├── platform_scheduling.py   # T3.1 — Interval Scheduling
│   │   ├── dispatch_queue.py        # T3.2 — Priority queue (min-heap)
│   │   ├── operational_analytics.py # T3.3 — Daily trip averages + k-th busiest station
│   │   ├── passenger_simulation.py  # T3.4 — Random passenger-arrival simulation
│   │   ├── floyd_warshall.py        # T4.1 — All-pairs shortest paths
│   │   ├── max_flow.py              # T4.2 — Edmonds-Karp
│   │   ├── critical_stations.py     # T4.3 — Articulation points and bridges (Tarjan / DFS)
│   │   ├── relief_deployment.py     # T4.4 — Approximate + exact Dominating Set
│   │   ├── fuzzy_search.py          # T4.5 — Levenshtein edit distance
│   │   └── bidirectional_dijkstra.py # Round 5 — Bidirectional Dijkstra vs. Dijkstra
│   └── demos/
│       ├── operations_demo.py       # Integrated demo for T3.1–T3.4
│       └── max_flow_demo.py         # Capacity-graph builder + T4.2 demo
└── tests/
    ├── test_platform_scheduling.py
    ├── test_dispatch_queue.py
    ├── test_operational_analytics.py
    └── test_passenger_simulation.py
```

---

## Getting Started

### Prerequisites

- Python **3.10+**
- No mandatory third-party dependencies — every algorithm is built on the Python standard library (`heapq`, `collections`, `itertools`, etc.).

### Optional dependency (correct RTL rendering of Persian station names)

`main.py` attempts to reshape Persian station names with `arabic_reshaper` and `python-bidi` for correct terminal display. These are **optional**; if missing, the program still runs fine (terminal output for Persian text may just not be visually reordered on some terminals).

```bash
pip install arabic-reshaper python-bidi
```

### Run the application

```bash
git clone <repository-url>
cd Qom-metro-algorithms
python main.py
```

You'll see the following menu:

```
1) Round 1 - Initial Acceptance (graph / BFS / Dijkstra)
2) Round 2 - Infrastructure Design (MST / DAG / Bellman-Ford)
3) Round 3 - Daily Metro Operations
4) Round 4 - Network Performance Analysis
5) Round 5 - Innovation (bonus)
0) Run all rounds in order
q) Quit
```

Selecting an option runs that round's scenario on the shared Qom graph. Some tasks (T1.2/T1.3, and Round 5) prompt for a start/end station or a routing criterion (distance/time); leaving the prompt empty falls back to a sensible default.

---

## Usage

### Running a specific task programmatically

```python
from graph.graph import Graph
from data.qom_metro_data import STATIONS, CONNECTIONS
from algorithms.shortest_path import ShortestPath

graph = Graph()
for station in STATIONS:
    graph.add_station(station)
for origin, destination, distance, time in CONNECTIONS:
    graph.add_connection(origin, destination, distance, time)

engine = ShortestPath(graph)
path, cost = engine.find_shortest_path(
    "ایستگاه ترمینال مسافربری قم",
    "ایستگاه حرم مطهر حضرت معصومه (س)",
    criterion="distance",   # or "time"
)
print(path, cost)
```

### Running the standalone demos

```bash
cd src
python -m demos.operations_demo   # T3.1–T3.4 walkthrough
python -m demos.max_flow_demo     # T4.2 (Max-Flow) demo
```

---

## Data Model — The Qom Metro Graph

Per task **T1.1**, the network is modeled as an **adjacency list** (`dict[station] -> list[Edge]`) inside the `Graph` class. This choice is justified by the fact that the Qom network is **sparse** (20 stations, 21 edges): an adjacency list gives O(V + E) memory versus O(V²) for an adjacency matrix, and neighbor traversal (needed by BFS/Dijkstra/DFS) is more efficient.

Each `Edge` stores:

| Field | Description |
|---|---|
| `destination` | Target station |
| `distance` | Distance in kilometers |
| `time` | Approximate travel time in minutes |
| `weight` | Generic weight (defaults to `distance`; made negative for incentive edges in Round 2) |
| `capacity` | Passenger capacity per unit time (used by T4.2) |

Raw data (20 stations, 21 connections) was extracted directly from the "Graph Nodes (Stations)" and "Edges (Routes)" tables in the project brief and lives in `src/data/qom_metro_data.py`.

---

## Round 1 — Initial Acceptance

| Code | Task | Algorithm | File |
|---|---|---|---|
| T1.1 | Model the Qom map as a graph | Graph data structure (adjacency list) | `graph/graph.py` |
| T1.2 | Check reachability between two stations | BFS | `algorithms/reachability.py` |
| T1.3 | Core routing engine (shortest path) | Dijkstra with a min-heap; selectable criterion (distance/time) | `algorithms/shortest_path.py` |
| T1.4 | Time/space complexity analysis | — | Documented in code and in the app menu |

**Complexity:** BFS runs in O(V + E); Dijkstra with a heap-based priority queue runs in O((V + E) log V).

---

## Round 2 — Infrastructure Design

| Code | Task | Algorithm | File |
|---|---|---|---|
| T2.1 | Design the lowest-cost network (MST) | Prim (min-heap) vs. Kruskal | `algorithms/mst.py`, `algorithms/kruskal.py` |
| T2.2 | Efficient Kruskal implementation | Union-Find with path compression + union by rank | `data_structures/union_find.py` |
| T2.3 | Build a one-way express line (DAG) | Topological sort + edge relaxation | `algorithms/dag_shortest_path.py`, `algorithms/express_line.py` |
| T2.4 | Detect negative cycles (incentive edges) | Bellman-Ford | `algorithms/bellman_ford.py`, `algorithms/incentive_network.py` |

- **Prim vs. Kruskal:** both run on the shared graph and their total cost is compared. Prim suits dense graphs where fast neighbor access matters (O(E log V) with a binary heap); Kruskal, sorting edges and using Union-Find, is simpler for sparse graphs — O(E log E) here.
- **Express line:** a **separate directed graph** (`build_express_line`) is built because DAG-shortest-path is only meaningful on an acyclic graph — running it on the main (undirected) graph raises a cycle error, exactly the constraint highlighted in the project brief.
- **Negative cycles:** a dedicated negative-weight graph (`build_incentive_network`) and a deliberately cyclic sample (`build_incentive_network_with_negative_cycle`) are both provided to exercise both outcomes.

---

## Round 3 — Daily Metro Operations

| Code | Task | Algorithm | File |
|---|---|---|---|
| T3.1 | Assign the maximum number of trains to a shared platform | Greedy Interval Scheduling (sorted by departure time) | `algorithms/platform_scheduling.py` |
| T3.2 | Manage the train dispatch queue by priority | Min-heap with lazy deletion / priority update | `algorithms/dispatch_queue.py` |
| T3.3 | Analyze operational data (daily trip average, k-th busiest station) | `Counter` + top-k selection | `algorithms/operational_analytics.py` |
| T3.4 | Simulate random passenger arrivals and gate queues | Heap-based event queue + a random-arrival model | `algorithms/passenger_simulation.py` |

All four capabilities operate on the same shared entities (`Train`, `TripRecord`, `Passenger`) and are chained into one continuous scenario in `demos/operations_demo.py` — not four disconnected scripts — matching the brief's requirement of "system-wide integration."

---

## Round 4 — Network Performance Analysis

| Code | Task | Algorithm | File |
|---|---|---|---|
| T4.1 | Precompute the full shortest-path matrix between all stations | Floyd-Warshall | `algorithms/floyd_warshall.py` |
| T4.2 | Peak-hour capacity analysis (maximize passenger flow) | Max-Flow (Edmonds-Karp; Ford-Fulkerson with BFS) | `algorithms/max_flow.py`, `demos/max_flow_demo.py` |
| T4.3 | Identify critical stations (articulation points and bridges) | DFS via Tarjan's low-link method | `algorithms/critical_stations.py` |
| T4.4 | Optimal relief-team placement (bonus, NP-Hard) | Greedy Dominating Set approximation + exact search for comparison | `algorithms/relief_deployment.py` |
| T4.5/T4.6 | Typo-tolerant station name search | Levenshtein edit distance | `algorithms/fuzzy_search.py` |

- **T4.3** outputs the exact set of articulation points and bridges.
- **T4.4** first establishes that the problem is equivalent to **Dominating Set** and is `NP-Hard`; a greedy approximation is then implemented and compared against an exact brute-force solution, with the resulting **approximation ratio** reported.

---

## Round 5 — Innovation (Bonus)

**Chosen track: Track A — apply an advanced algorithm outside the standard syllabus**

Implementation of **Bidirectional Dijkstra** (`algorithms/bidirectional_dijkstra.py`): a simultaneous search from both the start and end station that terminates when the two search frontiers meet. Its performance is benchmarked against standard Dijkstra on the real Qom graph, reporting the **percentage reduction in nodes expanded** — exactly the comparison metric requested by the project brief for this technique.

> The brief's other optional techniques (A\*, ALT, Contraction Hierarchies, metaheuristics, ACO, Fibonacci Heap, Hopcroft–Karp for T3.5, FFT) are **not implemented** in this version — this round is entirely bonus, and the brief asks teams to pick just one of the two available tracks.

---

## Algorithms & Complexity Reference

| Algorithm | Used for | Time Complexity | Space Complexity |
|---|---|---|---|
| BFS | T1.2 reachability | O(V + E) | O(V) |
| Dijkstra (min-heap) | T1.3 shortest path | O((V + E) log V) | O(V) |
| Prim (min-heap) | T2.1 MST | O(E log V) | O(V + E) |
| Kruskal + Union-Find | T2.1/T2.2 MST | O(E log E) | O(V + E) |
| Topological sort + relaxation | T2.3 DAG shortest path | O(V + E) | O(V) |
| Bellman-Ford | T2.4 negative cycles | O(V·E) | O(V) |
| Greedy Interval Scheduling | T3.1 platform assignment | O(n log n) | O(n) |
| Min-heap (priority queue) | T3.2 dispatch queue | O(log n) per operation | O(n) |
| Counter / top-k | T3.3 operational analytics | O(n) / O(n log k) | O(V) |
| Event-driven simulation | T3.4 passenger arrivals | O(n log n) | O(n) |
| Floyd-Warshall | T4.1 all-pairs shortest paths | O(V³) | O(V²) |
| Edmonds-Karp | T4.2 max flow | O(V·E²) | O(V + E) |
| DFS (Tarjan low-link) | T4.3 articulation points/bridges | O(V + E) | O(V) |
| Greedy Dominating Set | T4.4 relief deployment | ~O(V·E) | O(V) |
| Exact Dominating Set | T4.4 baseline for comparison | Exponential — O(2ᵛ) | O(V) |
| Levenshtein distance | T4.5 fuzzy search | O(m·n) per comparison | O(m·n) |
| Bidirectional Dijkstra | Round 5 — innovation | O((V + E) log V), smaller practical constant | O(V) |

*(m and n are the lengths of the two compared strings; V and E are the number of stations and edges, respectively.)*

---

## Testing

Current test coverage focuses on Round 3's four core modules (`pytest`, configured via `pytest.ini` with `pythonpath = src`):

| Test file | Coverage |
|---|---|
| `test_platform_scheduling.py` | Correctness of the maximum-train selection, completeness of the rejected set, edge cases (empty/single input) |
| `test_dispatch_queue.py` | Priority-based dispatch order, non-destructive `peek`, priority updates, train removal, empty-queue behavior |
| `test_operational_analytics.py` | Total/average daily trips, per-station visit counts, k-th busiest station (and out-of-range k), empty-state behavior |
| `test_passenger_simulation.py` | Reproducibility with a fixed seed, valid gate assignment for every passenger, gate-count vs. wait-time relationship, per-gate utilization stats, zero-passenger edge case |

Run the full suite:

```bash
pip install pytest
pytest
```
---

## Design Decisions & SOLID Principles

- **Single Responsibility:** each algorithm class (`ShortestPath`, `MinimumSpanningTree`, `BellmanFord`, etc.) has exactly one responsibility and depends only on `Graph` — never on the data source or the UI layer.
- **Open/Closed:** the `Graph`/`Edge` structures are general-purpose and extensible (directed edges, weights, capacities) without modifying existing code when new algorithms are added.
- **Dependency direction:** the `algorithms` layer depends on `graph` and `data_structures`, never the reverse; raw data (`data/`) is fully decoupled from algorithmic logic.
- **One graph, one data source:** as explicitly required at the end of every round in the project brief ("avoid creating independent implementations for each task"), every round reuses the same `STATIONS`/`CONNECTIONS` and the same `Graph` class; task-specific graphs (express line, incentive network, capacity graph) are simply separate *instances* of that same class, not parallel implementations.
- **Single unified workflow:** `main.py` provides one entry point and one menu for all five rounds; no scattered scripts are needed to run individual tasks (the demos under `src/demos` also draw from the same shared graph and data).

---
## License

This project was developed as coursework for the Algorithm Design course at Bu-Ali Sina University and is intended for educational purposes.
