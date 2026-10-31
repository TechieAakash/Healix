from __future__ import annotations
from typing import Dict, List, Any, Set, Tuple
from pydantic import BaseModel, Field

class BayesQueryResponse(BaseModel):
    query_variable: str
    evidence: Dict[str, bool]
    posterior_distribution: Dict[str, float]
    cpt_explanation: str

class DempsterShaferResult(BaseModel):
    frame_of_discernment: List[str]
    mass_1: Dict[str, float]
    mass_2: Dict[str, float]
    conflict_k: float
    combined_mass: Dict[str, float]
    belief_intervals: Dict[str, Dict[str, float]]  # {Hypothesis: {"bel": ..., "pl": ...}}

class FuzzyMembership(BaseModel):
    input_value: float
    memberships: Dict[str, float]
    linguistic_summary: str

class UncertaintyEngine:
    """
    Implements Unit 4: Bayesian Networks, Dempster-Shafer Theory, and Fuzzy Logic.
    """

    @classmethod
    def bayesian_network_query(cls, query_var: str = "Flu", evidence: Optional[Dict[str, bool]] = None) -> BayesQueryResponse:
        """
        Clinical Network: Flu (Prior: 0.1)
        Flu -> Fever: P(Fever | Flu) = 0.85, P(Fever | ~Flu) = 0.05
        Flu -> Fatigue: P(Fatigue | Flu) = 0.90, P(Fatigue | ~Flu) = 0.15
        Fever -> Chills: P(Chills | Fever) = 0.75, P(Chills | ~Fever) = 0.02
        """
        if evidence is None:
            evidence = {"Fever": True, "Fatigue": True}

        # Exact calculation using Bayes Rule
        p_flu_true = 0.10
        p_flu_false = 0.90

        # Conditional probabilities
        p_fever_given_flu = 0.85 if evidence.get("Fever") is True else 0.15
        p_fever_given_not_flu = 0.05 if evidence.get("Fever") is True else 0.95

        p_fatigue_given_flu = 0.90 if evidence.get("Fatigue") is True else 0.10
        p_fatigue_given_not_flu = 0.15 if evidence.get("Fatigue") is True else 0.85

        # Likelihood P(Evidence | Flu = True)
        likelihood_true = p_fever_given_flu * p_fatigue_given_flu
        # Likelihood P(Evidence | Flu = False)
        likelihood_false = p_fever_given_not_flu * p_fatigue_given_not_flu

        unnormalized_true = likelihood_true * p_flu_true
        unnormalized_false = likelihood_false * p_flu_false
        normalizer = unnormalized_true + unnormalized_false

        post_true = round(unnormalized_true / normalizer, 4)
        post_false = round(unnormalized_false / normalizer, 4)

        return BayesQueryResponse(
            query_variable=query_var,
            evidence=evidence,
            posterior_distribution={"True": post_true, "False": post_false},
            cpt_explanation=f"Given evidence {evidence}, P({query_var}=True) updated from prior 0.10 to posterior {post_true}."
        )

    @classmethod
    def dempster_shafer_combine(
        cls,
        mass_1: Optional[Dict[str, float]] = None,
        mass_2: Optional[Dict[str, float]] = None
    ) -> DempsterShaferResult:
        """
        Frame: {Migraine, Meningitis, Tension}
        Combines two independent sensor/expert belief assignments m1 and m2 using Dempster's Rule of Combination.
        """
        frame = ["Migraine", "Meningitis", "Tension"]

        if mass_1 is None:
            # Expert 1: Moderate belief in Migraine, some uncertainty
            mass_1 = {"Migraine": 0.60, "Migraine,Tension": 0.20, "Theta": 0.20}
        if mass_2 is None:
            # Expert 2: Strong belief in Benign Cephalea (Migraine or Tension)
            mass_2 = {"Migraine,Tension": 0.70, "Theta": 0.30}

        def parse_focal(s: str) -> Set[str]:
            if s == "Theta":
                return set(frame)
            return set(x.strip() for x in s.split(","))

        # Calculate conflict factor K
        conflict_k = 0.0
        combined: Dict[str, float] = {}

        for set1_str, m1 in mass_1.items():
            f1 = parse_focal(set1_str)
            for set2_str, m2 in mass_2.items():
                f2 = parse_focal(set2_str)
                intersection = f1.intersection(f2)
                product = m1 * m2

                if len(intersection) == 0:
                    conflict_k += product
                else:
                    sorted_inter = ",".join(sorted(list(intersection)))
                    if set(intersection) == set(frame):
                        sorted_inter = "Theta"
                    combined[sorted_inter] = combined.get(sorted_inter, 0.0) + product

        # Normalize by (1 - K)
        denominator = 1.0 - conflict_k
        if denominator <= 0:
            denominator = 1e-6

        normalized_mass = {k: round(v / denominator, 4) for k, v in combined.items()}

        # Compute Belief Bel(A) and Plausibility Pl(A) for singleton hypotheses
        intervals: Dict[str, Dict[str, float]] = {}
        for h in frame:
            bel = 0.0
            pl = 0.0
            for focal_str, m_val in normalized_mass.items():
                f_set = parse_focal(focal_str)
                if f_set.issubset({h}):
                    bel += m_val
                if len(f_set.intersection({h})) > 0:
                    pl += m_val
            intervals[h] = {"belief": round(bel, 4), "plausibility": round(pl, 4)}

        return DempsterShaferResult(
            frame_of_discernment=frame,
            mass_1=mass_1,
            mass_2=mass_2,
            conflict_k=round(conflict_k, 4),
            combined_mass=normalized_mass,
            belief_intervals=intervals
        )

    @classmethod
    def evaluate_fuzzy_temperature(cls, temp_celsius: float) -> FuzzyMembership:
        """
        Fuzzy membership for body temperature in Celsius.
        Normal: [36.0, 36.6, 37.2]
        Low-Grade Fever: [37.0, 37.8, 38.4]
        High Fever: [38.2, 39.0, 41.0]
        """
        def tri_mf(x: float, a: float, b: float, c: float) -> float:
            if x <= a or x >= c:
                return 0.0
            elif a < x <= b:
                return (x - a) / (b - a)
            else:
                return (c - x) / (c - b)

        def trap_right(x: float, a: float, b: float) -> float:
            if x <= a:
                return 0.0
            elif a < x < b:
                return (x - a) / (b - a)
            return 1.0

        def trap_left(x: float, a: float, b: float) -> float:
            if x <= a:
                return 1.0
            elif a < x < b:
                return (b - x) / (b - a)
            return 0.0

        mu_normal = trap_left(temp_celsius, 36.5, 37.2)
        mu_low_grade = tri_mf(temp_celsius, 37.0, 37.8, 38.5)
        mu_high_fever = trap_right(temp_celsius, 38.2, 39.2)

        memberships = {
            "Normal (Afebrile)": round(mu_normal, 3),
            "Low-Grade Pyrexia": round(mu_low_grade, 3),
            "High Pyrexia": round(mu_high_fever, 3)
        }

        dominant = max(memberships.items(), key=lambda item: item[1])
        summary = f"Temperature {temp_celsius}°C primarily belongs to '{dominant[0]}' with μ={dominant[1]}."

        return FuzzyMembership(
            input_value=temp_celsius,
            memberships=memberships,
            linguistic_summary=summary
        )

