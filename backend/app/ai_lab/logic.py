from __future__ import annotations
from typing import List, Set, Tuple, Dict, Any, Optional
from pydantic import BaseModel, Field
from ..engine.unification import Unifier, UnificationResult

class ResolutionStep(BaseModel):
    step_num: int
    clause1: List[str]
    clause2: List[str]
    resolvent: List[str]
    resolved_literal: str
    is_empty_clause: bool

class ResolutionProofResult(BaseModel):
    proved: bool
    clauses: List[List[str]]
    steps: List[ResolutionStep]
    explanation: str

class LogicEngine:
    """
    Implements Unit 3: Propositional Resolution Refutation and First-Order Unification.
    """

    @classmethod
    def run_unification(cls, term1: str, term2: str) -> UnificationResult:
        unifier = Unifier()
        return unifier.unify_strings(term1, term2)

    @classmethod
    def resolution_refutation(cls, initial_clauses: List[List[str]]) -> ResolutionProofResult:
        """
        Propositional Resolution Theorem Prover.
        Clauses are represented as lists of literals, e.g.:
        [["P", "Q"], ["~P", "R"], ["~Q"], ["~R"]]
        Proves whether the clause set is unsatisfiable (deriving empty clause []).
        """
        # Normalize literals as sets of frozen strings
        clauses = [frozenset(c) for c in initial_clauses]
        seen_clauses = set(clauses)
        steps: List[ResolutionStep] = []
        step_counter = 0

        while True:
            new_clauses = set()
            clause_list = list(seen_clauses)
            pair_resolved = False

            for i in range(len(clause_list)):
                for j in range(i + 1, len(clause_list)):
                    c1 = clause_list[i]
                    c2 = clause_list[j]

                    # Look for complementary pairs: L in c1 and ~L in c2 (or vice versa)
                    for lit in c1:
                        neg_lit = lit[1:] if lit.startswith("~") else f"~{lit}"
                        if neg_lit in c2:
                            # Resolvent is (c1 \ {lit}) U (c2 \ {neg_lit})
                            resolvent = (c1 - {lit}) | (c2 - {neg_lit})
                            step_counter += 1

                            is_empty = (len(resolvent) == 0)
                            steps.append(
                                ResolutionStep(
                                    step_num=step_counter,
                                    clause1=sorted(list(c1)),
                                    clause2=sorted(list(c2)),
                                    resolvent=sorted(list(resolvent)),
                                    resolved_literal=lit,
                                    is_empty_clause=is_empty
                                )
                            )

                            if is_empty:
                                return ResolutionProofResult(
                                    proved=True,
                                    clauses=initial_clauses,
                                    steps=steps,
                                    explanation="Contradiction derived! Empty clause (BOX) reached via resolution refutation."
                                )

                            if resolvent not in seen_clauses:
                                new_clauses.add(resolvent)
                                pair_resolved = True

            if not new_clauses.issubset(seen_clauses) and pair_resolved:
                seen_clauses.update(new_clauses)
            else:
                # No new clauses generated
                break

        return ResolutionProofResult(
            proved=False,
            clauses=initial_clauses,
            steps=steps,
            explanation="No contradiction found. The knowledge base is consistent / satisfiable."
        )

