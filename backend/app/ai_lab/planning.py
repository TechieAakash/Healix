from __future__ import annotations
from typing import List, Dict, Set, Any
from pydantic import BaseModel, Field

class PlanAction(BaseModel):
    action_name: str
    preconditions: List[str]
    add_list: List[str]
    delete_list: List[str]

class PlanningStep(BaseModel):
    step_num: int
    executed_action: str
    current_state: List[str]
    goal_stack: List[str]

class PlanningResult(BaseModel):
    initial_state: List[str]
    goal_state: List[str]
    plan_actions: List[str]
    steps: List[PlanningStep]
    success: bool

class GoalStackPlanner:
    """
    Implements Unit 5: STRIPS Goal Stack Planning for Blocks World.
    Blocks: A, B, C
    Predicates: ON(x, y), ONTABLE(x), CLEAR(x), HOLDING(x), ARMEMPTY
    """

    @classmethod
    def run_demo_plan(cls) -> PlanningResult:
        """
        Initial state: ONTABLE(A), ONTABLE(B), CLEAR(A), CLEAR(B), ARMEMPTY
        Goal state: ON(A, B), ONTABLE(B)
        """
        initial_state = {"ONTABLE(A)", "ONTABLE(B)", "CLEAR(A)", "CLEAR(B)", "ARMEMPTY"}
        goal_state = {"ON(A, B)", "ONTABLE(B)"}

        # Simulated Goal Stack execution steps
        steps = [
            PlanningStep(
                step_num=1,
                executed_action="INITIALIZE",
                current_state=sorted(list(initial_state)),
                goal_stack=["ON(A, B)"]
            ),
            PlanningStep(
                step_num=2,
                executed_action="PICKUP(A)",
                current_state=["CLEAR(B)", "HOLDING(A)", "ONTABLE(B)"],
                goal_stack=["STACK(A, B)"]
            ),
            PlanningStep(
                step_num=3,
                executed_action="STACK(A, B)",
                current_state=["ARMEMPTY", "CLEAR(A)", "ON(A, B)", "ONTABLE(B)"],
                goal_stack=[]
            )
        ]

        return PlanningResult(
            initial_state=sorted(list(initial_state)),
            goal_state=sorted(list(goal_state)),
            plan_actions=["PICKUP(A)", "STACK(A, B)"],
            steps=steps,
            success=True
        )

