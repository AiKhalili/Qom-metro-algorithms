"""main.py - unified workflow for the Qom Metro Algorithms project."""

import builtins
import os
import re
import sys

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(PROJECT_ROOT, "src")
for path in (PROJECT_ROOT, SRC_DIR):
    if path not in sys.path:
        sys.path.insert(0, path)

try:
    import arabic_reshaper
    from bidi.algorithm import get_display

    _BIDI_AVAILABLE = True
except ImportError:
    _BIDI_AVAILABLE = False

try:
    import termios
    import tty

    _POSIX = True
except ImportError:
    _POSIX = False

try:
    import msvcrt

    _WINDOWS = True
except ImportError:
    _WINDOWS = False

_RTL_PATTERN = re.compile(r"[\u0600-\u06FF\u200C\u200F]")
_builtin_print = builtins.print
_builtin_input = builtins.input


def _fix_rtl(text):
    if not _BIDI_AVAILABLE or not _RTL_PATTERN.search(text):
        return text
    return get_display(arabic_reshaper.reshape(text))


def _patched_print(*args, **kwargs):
    fixed_args = [_fix_rtl(a) if isinstance(a, str) else a for a in args]
    _builtin_print(*fixed_args, **kwargs)


def _redraw_line(prompt, buffer):
    """Clear the current terminal line and redraw prompt+typed text, shaped."""
    text = "".join(buffer)
    fixed = _fix_rtl(prompt + text)
    # \r -> back to column 0, \033[K -> clear from cursor to end of line
    sys.stdout.write("\r\033[K" + fixed)
    sys.stdout.flush()


def _posix_raw_input(prompt):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    new_settings = termios.tcgetattr(fd)
    # Turn off canonical mode (line buffering) AND local echo, so nothing
    # reaches the screen except what we explicitly write ourselves.
    new_settings[3] = new_settings[3] & ~(termios.ICANON | termios.ECHO)
    buffer = []
    try:
        termios.tcsetattr(fd, termios.TCSANOW, new_settings)
        sys.stdout.write(_fix_rtl(prompt) + "\n")
        sys.stdout.flush()
        _redraw_line("", buffer)
        while True:
            ch = sys.stdin.read(1)
            if ch in ("\r", "\n"):
                sys.stdout.write("\n")
                sys.stdout.flush()
                break
            elif ch in ("\x7f", "\b"):  # Backspace / Delete
                if buffer:
                    buffer.pop()
                    _redraw_line("", buffer)
            elif ch == "\x03":  # Ctrl-C
                sys.stdout.write("\n")
                raise KeyboardInterrupt
            elif ch == "\x04":  # Ctrl-D
                if not buffer:
                    sys.stdout.write("\n")
                    raise EOFError
            elif ch == "\x1b":  # start of an arrow-key/escape sequence: ignore it
                sys.stdin.read(2)
            else:
                buffer.append(ch)
                _redraw_line("", buffer)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return "".join(buffer)


def _windows_raw_input(prompt):
    buffer = []
    sys.stdout.write(_fix_rtl(prompt) + "\n")
    sys.stdout.flush()
    _redraw_line("", buffer)
    while True:
        ch = msvcrt.getwch()
        if ch in ("\r", "\n"):
            print()
            break
        elif ch == "\x08":  # Backspace
            if buffer:
                buffer.pop()
                _redraw_line("", buffer)
        elif ch == "\x03":  # Ctrl-C
            raise KeyboardInterrupt
        elif ch in ("\x00", "\xe0"):  # arrow-key/function-key prefix: ignore
            msvcrt.getwch()
        else:
            buffer.append(ch)
            _redraw_line("", buffer)
    return "".join(buffer)


def _patched_input(prompt=""):
    # Only take over the terminal when we're actually attached to one and
    # the platform is supported; otherwise fall back to the normal input()
    # (e.g. when input is piped/redirected, or bidi libs aren't installed).
    if _BIDI_AVAILABLE and sys.stdin.isatty() and sys.stdout.isatty():
        try:
            if _POSIX:
                return _posix_raw_input(prompt)
            elif _WINDOWS:
                return _windows_raw_input(prompt)
        except Exception:
            pass  # fall through to the plain built-in input below
    if prompt:
        _builtin_print(_fix_rtl(prompt))
    return _builtin_input()


builtins.print = _patched_print
builtins.input = _patched_input
print = _patched_print
input = _patched_input


from graph.graph import Graph
from data.qom_metro_data import STATIONS, CONNECTIONS

from algorithms.reachability import Reachability
from algorithms.shortest_path import ShortestPath

from algorithms.mst import MinimumSpanningTree
from algorithms.kruskal import KruskalMST
from algorithms.dag_shortest_path import DAGShortestPath
from algorithms.express_line import build_express_line
from algorithms.bellman_ford import BellmanFord
from algorithms.incentive_network import (
    build_incentive_network,
    build_incentive_network_with_negative_cycle,
)

from demos.operations_demo import (
    demo_platform_scheduling,
    demo_dispatch_queue,
    demo_operational_analytics,
    demo_passenger_simulation,
)

from algorithms.floyd_warshall import AllPairsShortestPath
from algorithms.fuzzy_search import FuzzyStationSearch
from demos.max_flow_demo import build_capacity_graph, demo_max_flow
from algorithms.critical_stations import CriticalStations
from algorithms.relief_deployment import ReliefDeployment

from algorithms.bidirectional_dijkstra import compare_with_dijkstra


def build_shared_graph():
    graph = Graph()
    for station in STATIONS:
        graph.add_station(station)
    for origin, destination, distance, time in CONNECTIONS:
        graph.add_connection(origin, destination, distance, time)
    return graph


DEFAULT_START = "ایستگاه ترمینال مسافربری قم"
DEFAULT_END = "ایستگاه حرم مطهر حضرت معصومه (س)"


def _print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def _ask_station(graph, prompt, default):
    value = input(f"{prompt} [Enter = {default}]: ").strip()
    if not value:
        value = default
    if not graph.has_station(value):
        print(f"  ! Station '{value}' not found, using default.")
        value = default
    return value


def round1_menu(graph):
    _print_header("Round 1: Initial Acceptance (Graph Basics + Routing)")

    print(
        f"T1.1 - Graph model: {graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections (adjacency list)."
    )

    start = _ask_station(graph, "Start station", DEFAULT_START)
    end = _ask_station(graph, "End station", DEFAULT_END)

    print("\n--- T1.2: Reachability check (BFS) ---")
    reach = Reachability(graph)
    path = reach.find_path(start, end)
    if path is None:
        print(f"No path found between '{start}' and '{end}'.")
    else:
        print(f"Path found ({len(path) - 1} hops): {' -> '.join(path)}")

    print("\n--- T1.3: Main routing engine (Dijkstra) ---")
    criterion = (
        input("Criterion (distance / time) [Enter = distance]: ").strip() or "distance"
    )
    engine = ShortestPath(graph)
    sp_path, cost = engine.find_shortest_path(start, end, criterion=criterion)
    if sp_path is None:
        print("No path found.")
    else:
        unit = "km" if criterion == "distance" else "min"
        print(f"Shortest path ({criterion}): {' -> '.join(sp_path)}")
        print(f"Total cost: {cost} {unit}")

    print("\n--- T1.4: Time/space complexity ---")
    print("BFS (T1.2):      O(V + E) time, O(V) space")
    print("Dijkstra (T1.3): O((V + E) log V) with a min-heap, O(V) space")


def round2_menu(graph):
    _print_header("Round 2: Infrastructure Design (MST / DAG / Bellman-Ford)")

    print("--- T2.1 & T2.2: Prim vs. Kruskal (Union-Find) ---")
    mst = MinimumSpanningTree(graph)
    prim_edges, prim_cost = mst.prim()
    print(f"Prim    -> {len(prim_edges)} edges, total cost = {prim_cost}")

    kruskal = KruskalMST(graph)
    kruskal_edges, kruskal_cost = kruskal.kruskal()
    print(f"Kruskal -> {len(kruskal_edges)} edges, total cost = {kruskal_cost}")

    print("\n--- T2.3: Express line (DAG shortest path) ---")
    express_graph = build_express_line()
    dag = DAGShortestPath(express_graph)
    express_start = "ایستگاه ترمینال مسافربری قم"
    express_end = "ایستگاه ارگ سالاریه"
    dag_path, dag_cost = dag.shortest_path(express_start, express_end, criterion="time")
    if dag_path is None:
        print(
            f"No path between '{express_start}' and '{express_end}' on the express graph."
        )
    else:
        print(f"Shortest express path: {' -> '.join(dag_path)} (time = {dag_cost} min)")

    print("\n--- T2.4: Negative-cycle check (Bellman-Ford) ---")
    incentive_graph = build_incentive_network()
    bf = BellmanFord(incentive_graph)
    if bf.has_negative_cycle(criterion="weight"):
        print("Negative cycle detected in the incentive network!")
    else:
        print("No negative cycle; shortest paths are valid.")
        path, cost = bf.shortest_path(DEFAULT_START, DEFAULT_END, criterion="weight")
        if path:
            print(f"Shortest path (weight): {' -> '.join(path)} (cost = {cost})")

    print("\n  Testing a graph that contains a negative cycle (A-B-C):")
    negative_cycle_graph = build_incentive_network_with_negative_cycle()
    bf_cycle = BellmanFord(negative_cycle_graph)
    if bf_cycle.has_negative_cycle(criterion="weight"):
        cycle = bf_cycle.find_negative_cycle(criterion="weight")
        print(f"  Negative cycle found: {' -> '.join(cycle)}")


def round3_menu(graph):
    _print_header("Round 3: Daily Metro Operations")

    selected_trains = demo_platform_scheduling(graph)
    demo_dispatch_queue(selected_trains)
    demo_operational_analytics(graph)
    demo_passenger_simulation(graph)


def round4_menu(graph):
    _print_header("Round 4: Network Performance Analysis")

    print("--- T4.1: All-pairs shortest path (Floyd-Warshall) ---")
    apsp = AllPairsShortestPath(graph)
    apsp.precompute(criterion="distance")
    d = apsp.shortest_distance(DEFAULT_START, DEFAULT_END)
    p = apsp.shortest_path(DEFAULT_START, DEFAULT_END)
    print(f"Precomputed distance {DEFAULT_START} -> {DEFAULT_END}: {d} km")
    print(f"Path: {' -> '.join(p)}")

    print("\n--- T4.2: Peak-hour capacity (Max-Flow) ---")
    capacity_graph = build_capacity_graph()
    demo_max_flow(capacity_graph)

    print("\n--- T4.3: Critical stations (articulation points & bridges) ---")
    critical = CriticalStations(graph)
    critical.analyze()
    articulation_points = critical.get_articulation_points()
    bridges = critical.get_bridges()
    print(f"Articulation points ({len(articulation_points)}): {articulation_points}")
    print(f"Bridges ({len(bridges)}):")
    for u, v in bridges:
        print(f"  {u} <-> {v}")

    print("\n--- T4.4: Relief team deployment (approximate dominating set) ---")
    relief = ReliefDeployment(graph)
    greedy_result = relief.greedy_dominating_set()
    exact_result = relief.exact_minimum_dominating_set()
    ratio = relief.approximation_ratio(greedy_result, exact_result)
    print(f"Greedy solution ({len(greedy_result)} stations): {sorted(greedy_result)}")
    print(f"Exact solution  ({len(exact_result)} stations):  {sorted(exact_result)}")
    print(f"Approximation ratio: {ratio:.2f}")

    print("\n--- T4.5: Fuzzy station search (Levenshtein distance) ---")
    fuzzy = FuzzyStationSearch(graph)
    query = input("Station name (with typo) [Enter = 'ایستگاه دانشکاه قم']: ").strip()
    if not query:
        query = "ایستگاه دانشکاه قم"
    best_match, distance = fuzzy.closest_match(query)
    print(f"Closest match for '{query}': '{best_match}' (edit distance = {distance})")


def round5_menu(graph):
    _print_header("Round 5 (Bonus): Bidirectional Dijkstra vs. Dijkstra")

    start = _ask_station(graph, "Start station", DEFAULT_START)
    end = _ask_station(graph, "End station", "ایستگاه بوستان جنگلی غدیر")

    result = compare_with_dijkstra(graph, start, end, criterion="distance")

    print(
        f"\nDijkstra:               "
        f"cost = {result['dijkstra']['cost']}, "
        f"nodes expanded = {result['dijkstra']['nodes_expanded']}"
    )
    print(
        f"Bidirectional Dijkstra: "
        f"cost = {result['bidirectional_dijkstra']['cost']}, "
        f"nodes expanded = {result['bidirectional_dijkstra']['nodes_expanded']}"
    )
    print(f"Reduction in nodes expanded: {result['nodes_expanded_reduction_percent']}%")


def run_all(graph):
    round1_menu(graph)
    round2_menu(graph)
    round3_menu(graph)
    round4_menu(graph)
    round5_menu(graph)


def print_main_menu():
    print("\n" + "-" * 70)
    print("UrbanPulse Dynamics -- Qom Metro System")
    print("-" * 70)
    print("1) Round 1 - Initial Acceptance (graph / BFS / Dijkstra)")
    print("2) Round 2 - Infrastructure Design (MST / DAG / Bellman-Ford)")
    print("3) Round 3 - Daily Metro Operations")
    print("4) Round 4 - Network Performance Analysis")
    print("5) Round 5 - Innovation (bonus)")
    print("0) Run all rounds in order")
    print("q) Quit")


def main():
    graph = build_shared_graph()
    print(
        f"Shared graph loaded: {graph.number_of_stations()} stations, "
        f"{graph.number_of_connections()} connections."
    )

    actions = {
        "1": round1_menu,
        "2": round2_menu,
        "3": round3_menu,
        "4": round4_menu,
        "5": round5_menu,
        "0": run_all,
    }

    while True:
        print_main_menu()
        choice = input("Your choice: ").strip().lower()

        if choice == "q":
            print("Goodbye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid input. Try again.")
            continue

        try:
            action(graph)
        except Exception as exc:
            print(f"\n[Error running this section]: {exc}")


if __name__ == "__main__":
    main()

