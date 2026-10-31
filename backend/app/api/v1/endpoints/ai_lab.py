from typing import Dict, Any
from fastapi import APIRouter
from ....ai_lab.search import SearchEngine
from ....ai_lab.logic import LogicEngine
from ....ai_lab.uncertainty import UncertaintyEngine
from ....ai_lab.games import GameEngine
from ....ai_lab.planning import GoalStackPlanner
from ....ai_lab.learning import ID3Learner
from ....schemas.all_schemas import (
    SearchRequest, UnificationRequest, ResolutionRequest,
    BayesRequest, FuzzyRequest
)

router = APIRouter(prefix="/ai-lab", tags=["NSUT AI Lab"])

@router.post("/search/run")
async def run_search(req: SearchRequest):
    if req.algorithm.upper() == "HILL_CLIMBING":
        return SearchEngine.hill_climbing(start=req.start_node, goal=req.goal_node)
    elif req.algorithm.upper() == "SIMULATED_ANNEALING":
        return SearchEngine.simulated_annealing()
    else:
        return SearchEngine.a_star_search(start=req.start_node, goal=req.goal_node)

@router.post("/logic/unify")
async def run_unification(req: UnificationRequest):
    return LogicEngine.run_unification(req.term1, req.term2)

@router.post("/logic/resolve")
async def run_resolution(req: ResolutionRequest):
    return LogicEngine.resolution_refutation(req.clauses)

@router.post("/uncertainty/bayes")
async def run_bayes(req: BayesRequest):
    return UncertaintyEngine.bayesian_network_query(req.query_variable, req.evidence)

@router.get("/uncertainty/dempster-shafer")
async def run_dempster_shafer():
    return UncertaintyEngine.dempster_shafer_combine()

@router.post("/uncertainty/fuzzy")
async def run_fuzzy(req: FuzzyRequest):
    return UncertaintyEngine.evaluate_fuzzy_temperature(req.temperature_celsius)

@router.get("/games/alpha-beta")
async def run_alpha_beta():
    return GameEngine.run_alpha_beta_demo()

@router.get("/planning/blocks-world")
async def run_planning():
    return GoalStackPlanner.run_demo_plan()

@router.get("/learning/decision-tree")
async def run_decision_tree():
    return ID3Learner.train_clinical_demo()

