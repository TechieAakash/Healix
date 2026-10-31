from __future__ import annotations
import math
import heapq
import random
from typing import List, Dict, Any, Optional, Tuple
from pydantic import BaseModel, Field

class SearchStep(BaseModel):
    step_num: int
    current_node: str
    open_list: List[Dict[str, Any]]
    closed_list: List[str]
    g_cost: float
    h_cost: float
    f_cost: float
    description: str

class SearchResult(BaseModel):
    algorithm: str
    start_node: str
    goal_node: str
    path: List[str]
    total_cost: float
    nodes_expanded: int
    steps: List[SearchStep]
    time_complexity: str
    space_complexity: str
    is_optimal: bool

class SearchEngine:
    """
    Implements Unit 2 algorithms: A*, AO*, Hill Climbing, Simulated Annealing.
    """

    @staticmethod
    def get_sample_graph() -> Tuple[Dict[str, Dict[str, float]], Dict[str, float]]:
        # Graph nodes represent clinical triage pathways from Triage Check -> Specialist
        graph = {
            "Triage": {"Headache_Branch": 2.0, "Chest_Branch": 5.0, "Vitals_Branch": 1.5},
            "Headache_Branch": {"Neuro_Assess": 3.0, "Vascular_Screen": 4.0},
            "Chest_Branch": {"ECG_Station": 2.5, "Troponin_Lab": 3.5},
            "Vitals_Branch": {"Hydration_Check": 2.0, "Infection_Screen": 2.5},
            "Neuro_Assess": {"Specialist_Neurology": 2.0},
            "Vascular_Screen": {"Specialist_Neurology": 3.0, "Emergency_ICU": 4.0},
            "ECG_Station": {"Specialist_Cardiology": 1.5, "Emergency_ICU": 2.0},
            "Troponin_Lab": {"Specialist_Cardiology": 1.0},
            "Hydration_Check": {"Discharge_SelfCare": 1.0},
            "Infection_Screen": {"General_Medicine": 2.0},
            "Specialist_Neurology": {},
            "Specialist_Cardiology": {},
            "Emergency_ICU": {},
            "Discharge_SelfCare": {},
            "General_Medicine": {}
        }
        # Admissible heuristic estimates to Specialist_Neurology
        heuristics_to_neuro = {
            "Triage": 6.0,
            "Headache_Branch": 4.0,
            "Chest_Branch": 9.0,
            "Vitals_Branch": 7.0,
            "Neuro_Assess": 2.0,
            "Vascular_Screen": 2.5,
            "ECG_Station": 8.0,
            "Troponin_Lab": 8.5,
            "Hydration_Check": 8.0,
            "Infection_Screen": 6.5,
            "Specialist_Neurology": 0.0,
            "Specialist_Cardiology": 7.0,
            "Emergency_ICU": 5.0,
            "Discharge_SelfCare": 9.0,
            "General_Medicine": 6.0
        }
        return graph, heuristics_to_neuro

    @classmethod
    def a_star_search(
        cls,
        graph: Optional[Dict[str, Dict[str, float]]] = None,
        heuristics: Optional[Dict[str, float]] = None,
        start: str = "Triage",
        goal: str = "Specialist_Neurology"
    ) -> SearchResult:
        if graph is None or heuristics is None:
            graph, heuristics = cls.get_sample_graph()

        pq: List[Tuple[float, float, str, List[str]]] = []  # (f, g, node, path)
        h_start = heuristics.get(start, 0.0)
        heapq.heappush(pq, (h_start, 0.0, start, [start]))

        g_costs: Dict[str, float] = {start: 0.0}
        closed_set = set()
        steps: List[SearchStep] = []
        step_counter = 0

        while pq:
            f, g, current, path = heapq.heappop(pq)

            if current in closed_set:
                continue

            closed_set.add(current)
            step_counter += 1

            open_snapshot = [
                {"node": item[2], "f": round(item[0], 2), "g": round(item[1], 2), "h": round(item[0] - item[1], 2)}
                for item in sorted(pq, key=lambda x: x[0])
            ]

            steps.append(
                SearchStep(
                    step_num=step_counter,
                    current_node=current,
                    open_list=open_snapshot,
                    closed_list=list(closed_set),
                    g_cost=round(g, 2),
                    h_cost=round(heuristics.get(current, 0.0), 2),
                    f_cost=round(f, 2),
                    description=f"Expanded node '{current}' with f(n) = {round(g,2)} + {round(heuristics.get(current, 0.0),2)} = {round(f,2)}"
                )
            )

            if current == goal:
                return SearchResult(
                    algorithm="A* Heuristic Search",
                    start_node=start,
                    goal_node=goal,
                    path=path,
                    total_cost=round(g, 2),
                    nodes_expanded=len(closed_set),
                    steps=steps,
                    time_complexity="O(b^d)",
                    space_complexity="O(b^d)",
                    is_optimal=True
                )

            for neighbor, edge_cost in graph.get(current, {}).items():
                new_g = g + edge_cost
                if neighbor not in g_costs or new_g < g_costs[neighbor]:
                    g_costs[neighbor] = new_g
                    h = heuristics.get(neighbor, 0.0)
                    new_f = new_g + h
                    heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

        return SearchResult(
            algorithm="A* Heuristic Search",
            start_node=start,
            goal_node=goal,
            path=[],
            total_cost=0.0,
            nodes_expanded=len(closed_set),
            steps=steps,
            time_complexity="O(b^d)",
            space_complexity="O(b^d)",
            is_optimal=False
        )

    @classmethod
    def hill_climbing(
        cls,
        graph: Optional[Dict[str, Dict[str, float]]] = None,
        heuristics: Optional[Dict[str, float]] = None,
        start: str = "Triage",
        goal: str = "Specialist_Neurology"
    ) -> SearchResult:
        if graph is None or heuristics is None:
            graph, heuristics = cls.get_sample_graph()

        current = start
        path = [current]
        total_cost = 0.0
        steps = []
        step_counter = 0

        while current != goal:
            step_counter += 1
            curr_h = heuristics.get(current, 999.0)
            neighbors = graph.get(current, {})

            if not neighbors:
                steps.append(
                    SearchStep(
                        step_num=step_counter,
                        current_node=current,
                        open_list=[],
                        closed_list=list(path),
                        g_cost=round(total_cost, 2),
                        h_cost=curr_h,
                        f_cost=curr_h,
                        description=f"Local peak / Dead end reached at '{current}'."
                    )
                )
                break

            # Find neighbor with lowest h (steepest descent towards goal)
            best_neighbor = None
            best_h = curr_h
            best_edge_cost = 0.0

            neighbor_stats = []
            for n, edge_cost in neighbors.items():
                nh = heuristics.get(n, 999.0)
                neighbor_stats.append({"node": n, "h": nh})
                if nh < best_h:
                    best_h = nh
                    best_neighbor = n
                    best_edge_cost = edge_cost

            steps.append(
                SearchStep(
                    step_num=step_counter,
                    current_node=current,
                    open_list=neighbor_stats,
                    closed_list=list(path),
                    g_cost=round(total_cost, 2),
                    h_cost=curr_h,
                    f_cost=curr_h,
                    description=f"Inspecting neighbors of '{current}'. Best next step: {best_neighbor} with h={best_h}"
                )
            )

            if best_neighbor is None:
                # Local maximum reached
                break

            current = best_neighbor
            path.append(current)
            total_cost += best_edge_cost

        return SearchResult(
            algorithm="Hill Climbing (Steepest Ascent)",
            start_node=start,
            goal_node=goal,
            path=path,
            total_cost=round(total_cost, 2),
            nodes_expanded=len(path),
            steps=steps,
            time_complexity="O(b * m)",
            space_complexity="O(1)",
            is_optimal=(path[-1] == goal)
        )

    @classmethod
    def simulated_annealing(
        cls,
        initial_temp: float = 100.0,
        cooling_rate: float = 0.85,
        min_temp: float = 1.0
    ) -> Dict[str, Any]:
        """
        Demonstrates Simulated Annealing optimization for avoiding local minima.
        Objective: Minimize clinical triage allocation latency function f(x) = (x-4)^2 + 3*sin(2x).
        """
        def objective(x: float) -> float:
            return (x - 4.0) ** 2 + 3.0 * math.sin(2.0 * x)

        curr_x = 0.0
        curr_e = objective(curr_x)
        temp = initial_temp
        history = []
        iteration = 0

        while temp > min_temp and iteration < 50:
            iteration += 1
            # Random neighbor perturbation
            next_x = curr_x + random.uniform(-1.5, 1.5)
            next_e = objective(next_x)
            delta_e = next_e - curr_e

            accepted = False
            if delta_e < 0:
                # Better solution: always accept
                curr_x = next_x
                curr_e = next_e
                accepted = True
            else:
                # Worse solution: accept with Metropolis probability P = exp(-delta_e / T)
                prob = math.exp(-delta_e / max(temp, 1e-5))
                if random.random() < prob:
                    curr_x = next_x
                    curr_e = next_e
                    accepted = True

            history.append({
                "iteration": iteration,
                "temperature": round(temp, 2),
                "current_x": round(curr_x, 3),
                "energy": round(curr_e, 3),
                "accepted": accepted
            })
            temp *= cooling_rate

        return {
            "algorithm": "Simulated Annealing",
            "optimal_x": round(curr_x, 3),
            "minimal_energy": round(curr_e, 3),
            "iterations": iteration,
            "history": history
        }

