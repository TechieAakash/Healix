from __future__ import annotations
from typing import Dict, Any, Optional, List, Tuple
from pydantic import BaseModel, Field

class Term:
    def __init__(self, name: str, args: Optional[List[Term]] = None, is_var: bool = False):
        self.name = name
        self.args = args or []
        self.is_var = is_var or name.startswith("?")

    def is_variable(self) -> bool:
        return self.is_var

    def is_constant(self) -> bool:
        return not self.is_var and len(self.args) == 0

    def is_compound(self) -> bool:
        return len(self.args) > 0

    def __repr__(self) -> str:
        if self.is_compound():
            args_str = ", ".join(str(a) for a in self.args)
            return f"{self.name}({args_str})"
        return self.name

    def __eq__(self, other) -> bool:
        if not isinstance(other, Term):
            return False
        return (
            self.name == other.name and
            self.is_var == other.is_var and
            self.args == other.args
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "is_var": self.is_var,
            "args": [a.to_dict() for a in self.args]
        }

def parse_term(s: str) -> Term:
    """Parses strings like '?x', 'John', 'AllergicTo(?x, Penicillin)' into Term tree."""
    s = s.strip()
    if "(" not in s:
        return Term(s, is_var=s.startswith("?"))

    name = s[:s.index("(")].strip()
    rest = s[s.index("(") + 1 : -1].strip()

    # Split args respecting nested parens
    args = []
    depth = 0
    curr = []
    for char in rest:
        if char == "(":
            depth += 1
            curr.append(char)
        elif char == ")":
            depth -= 1
            curr.append(char)
        elif char == "," and depth == 0:
            args.append(parse_term("".join(curr)))
            curr = []
        else:
            curr.append(char)
    if curr:
        args.append(parse_term("".join(curr)))

    return Term(name, args=args, is_var=False)

class UnificationStep(BaseModel):
    step_num: int
    action: str
    term1: str
    term2: str
    current_subst: Dict[str, str]
    message: str

class UnificationResult(BaseModel):
    success: bool
    mgu: Optional[Dict[str, str]] = None
    steps: List[UnificationStep] = Field(default_factory=list)
    failure_reason: Optional[str] = None

class Unifier:
    """
    Implements Robinson's First-Order Logic Unification Algorithm with Occurs-Check.
    """

    def __init__(self):
        self.steps: List[UnificationStep] = []
        self.step_counter = 0

    def _record_step(self, action: str, t1: Term, t2: Term, subst: Dict[str, Term], message: str):
        self.step_counter += 1
        readable_subst = {k: str(v) for k, v in subst.items()}
        self.steps.append(
            UnificationStep(
                step_num=self.step_counter,
                action=action,
                term1=str(t1),
                term2=str(t2),
                current_subst=readable_subst,
                message=message
            )
        )

    def occurs_check(self, var: Term, term: Term, subst: Dict[str, Term]) -> bool:
        """Checks if variable 'var' occurs anywhere inside 'term' (under substitution)."""
        if var == term:
            return True
        if term.is_variable() and term.name in subst:
            return self.occurs_check(var, subst[term.name], subst)
        if term.is_compound():
            return any(self.occurs_check(var, arg, subst) for arg in term.args)
        return False

    def unify_var(self, var: Term, term: Term, subst: Dict[str, Term]) -> Optional[Dict[str, Term]]:
        if var.name in subst:
            return self.unify(subst[var.name], term, subst)
        elif term.is_variable() and term.name in subst:
            return self.unify(var, subst[term.name], subst)
        elif self.occurs_check(var, term, subst):
            self._record_step(
                "OCCURS_CHECK_FAILURE",
                var,
                term,
                subst,
                f"Variable {var} occurs inside {term}; infinite term prevented."
            )
            return None
        else:
            new_subst = dict(subst)
            new_subst[var.name] = term
            self._record_step(
                "BIND_VARIABLE",
                var,
                term,
                new_subst,
                f"Bound {var} -> {term}"
            )
            return new_subst

    def unify(self, t1: Term, t2: Term, subst: Optional[Dict[str, Term]] = None) -> Optional[Dict[str, Term]]:
        if subst is None:
            subst = {}

        self._record_step("EXAMINE", t1, t2, subst, f"Attempting to unify {t1} with {t2}")

        if t1 == t2:
            self._record_step("IDENTICAL", t1, t2, subst, f"Terms are identical: {t1}")
            return subst

        if t1.is_variable():
            return self.unify_var(t1, t2, subst)

        if t2.is_variable():
            return self.unify_var(t2, t1, subst)

        if t1.is_compound() and t2.is_compound():
            if t1.name != t2.name:
                self._record_step("CLASH", t1, t2, subst, f"Predicate symbol mismatch: {t1.name} != {t2.name}")
                return None
            if len(t1.args) != len(t2.args):
                self._record_step("ARITY_MISMATCH", t1, t2, subst, f"Arity mismatch: {len(t1.args)} != {len(t2.args)}")
                return None

            curr = subst
            for a1, a2 in zip(t1.args, t2.args):
                curr = self.unify(a1, a2, curr)
                if curr is None:
                    return None
            return curr

        self._record_step("CLASH", t1, t2, subst, f"Constant mismatch: {t1} != {t2}")
        return None

    def unify_strings(self, expr1: str, expr2: str) -> UnificationResult:
        self.steps = []
        self.step_counter = 0

        try:
            t1 = parse_term(expr1)
            t2 = parse_term(expr2)
            res = self.unify(t1, t2, {})
            if res is not None:
                mgu_dict = {k: str(v) for k, v in res.items()}
                return UnificationResult(success=True, mgu=mgu_dict, steps=self.steps)
            else:
                last_step = self.steps[-1].message if self.steps else "Unification failed"
                return UnificationResult(success=False, steps=self.steps, failure_reason=last_step)
        except Exception as e:
            return UnificationResult(success=False, steps=self.steps, failure_reason=str(e))

