from __future__ import annotations
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class GameTreeNode(BaseModel):
    id: str
    name: str
    is_maximizer: bool
    alpha: float
    beta: float
    value: Optional[float] = None
    pruned: bool = False
    children: List[GameTreeNode] = Field(default_factory=list)

class AlphaBetaStep(BaseModel):
    step_num: int
    node_id: str
    action: str
    alpha: float
    beta: float
    value: Optional[float]
    message: str

class AlphaBetaResult(BaseModel):
    root_value: float
    best_move: str
    pruned_nodes_count: int
    total_nodes_visited: int
    tree: GameTreeNode
    steps: List[AlphaBetaStep]

class GameEngine:
    """
    Implements Unit 4: Minimax Algorithm with Alpha-Beta Pruning.
    """

    @classmethod
    def run_alpha_beta_demo(cls) -> AlphaBetaResult:
        """
        Runs Alpha-Beta search on a canonical 3-ply game tree to demonstrate optimal pruning.
        Leaves: [3, 5, 6, 9, 1, 2, 0, -1]
        """
        steps: List[AlphaBetaStep] = []
        step_counter = [0]
        pruned_counter = [0]
        visited_counter = [0]

        def record(node_id: str, action: str, alpha: float, beta: float, val: Optional[float], msg: str):
            step_counter[0] += 1
            steps.append(
                AlphaBetaStep(
                    step_num=step_counter[0],
                    node_id=node_id,
                    action=action,
                    alpha=round(alpha, 2),
                    beta=round(beta, 2),
                    value=round(val, 2) if val is not None else None,
                    message=msg
                )
            )

        # Predefined canonical tree structure
        # Root (Max) -> A (Min), B (Min)
        # A -> A1 (Max), A2 (Max) -> Leaves: [3, 5], [6, 9]
        # B -> B1 (Max), B2 (Max) -> Leaves: [1, 2], [0, -1]

        raw_leaves = {
            "L1": 3.0, "L2": 5.0,
            "L3": 6.0, "L4": 9.0,
            "L5": 1.0, "L6": 2.0,
            "L7": 0.0, "L8": -1.0
        }

        def build_and_evaluate(
            node_id: str,
            depth: int,
            is_max: bool,
            alpha: float,
            beta: float
        ) -> GameTreeNode:
            visited_counter[0] += 1
            node = GameTreeNode(id=node_id, name=node_id, is_maximizer=is_max, alpha=alpha, beta=beta)

            # Base case: leaves at depth 3
            if node_id in raw_leaves:
                val = raw_leaves[node_id]
                node.value = val
                record(node_id, "EVALUATE_LEAF", alpha, beta, val, f"Evaluated leaf {node_id} = {val}")
                return node

            record(node_id, "ENTER_NODE", alpha, beta, None, f"Entered {'MAX' if is_max else 'MIN'} node {node_id}")

            # Define child mappings
            child_map = {
                "Root": ["A", "B"],
                "A": ["A1", "A2"],
                "B": ["B1", "B2"],
                "A1": ["L1", "L2"],
                "A2": ["L3", "L4"],
                "B1": ["L5", "L6"],
                "B2": ["L7", "L8"]
            }

            children_ids = child_map.get(node_id, [])

            if is_max:
                v = -float("inf")
                for cid in children_ids:
                    child_node = build_and_evaluate(cid, depth + 1, False, alpha, beta)
                    node.children.append(child_node)
                    v = max(v, child_node.value if child_node.value is not None else -float("inf"))
                    alpha = max(alpha, v)
                    node.alpha = alpha
                    node.beta = beta

                    if beta <= alpha:
                        pruned_counter[0] += (len(children_ids) - len(node.children))
                        record(node_id, "PRUNE", alpha, beta, v, f"Beta cutoff at {node_id} (Beta={beta} <= Alpha={alpha})")
                        break
                node.value = v
                record(node_id, "RESOLVE_MAX", alpha, beta, v, f"MAX node {node_id} resolved value = {v}")
                return node
            else:
                v = float("inf")
                for cid in children_ids:
                    child_node = build_and_evaluate(cid, depth + 1, True, alpha, beta)
                    node.children.append(child_node)
                    v = min(v, child_node.value if child_node.value is not None else float("inf"))
                    beta = min(beta, v)
                    node.alpha = alpha
                    node.beta = beta

                    if beta <= alpha:
                        pruned_counter[0] += (len(children_ids) - len(node.children))
                        record(node_id, "PRUNE", alpha, beta, v, f"Alpha cutoff at {node_id} (Beta={beta} <= Alpha={alpha})")
                        break
                node.value = v
                record(node_id, "RESOLVE_MIN", alpha, beta, v, f"MIN node {node_id} resolved value = {v}")
                return node

        tree_root = build_and_evaluate("Root", 0, True, -float("inf"), float("inf"))
        best_child = tree_root.children[0].name if tree_root.children else "None"

        return AlphaBetaResult(
            root_value=tree_root.value or 0.0,
            best_move=f"Branch -> {best_child}",
            pruned_nodes_count=pruned_counter[0],
            total_nodes_visited=visited_counter[0],
            tree=tree_root,
            steps=steps
        )

