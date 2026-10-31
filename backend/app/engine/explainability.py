from __future__ import annotations
import uuid
import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from .facts import Fact, FactValue
from .rules import Conclusion, Rule
from .forward_chaining import RuleFiringRecord, RuleSkippedRecord

class GraphNodeData(BaseModel):
    label: str
    sublabel: Optional[str] = None
    node_type: str                   # "FACT" | "RULE" | "CONCLUSION" | "SAFETY" | "MISSING_INFO"
    state: str                       # "ACTIVE" | "INACTIVE" | "FIRED" | "SKIPPED" | "EMERGENCY"
    metadata: Dict[str, Any] = Field(default_factory=dict)
    step: int = 0

class GraphNode(BaseModel):
    id: str
    type: str                        # "factNode" | "ruleNode" | "conclusionNode" | "safetyNode" | "missingInfoNode"
    position: Dict[str, float]       # {"x": ..., "y": ...}
    data: GraphNodeData

class GraphEdgeData(BaseModel):
    relationship: str                # "SUPPORTED_BY" | "TRIGGERS" | "DERIVED_FROM" | "CONFLICTS_WITH" | "ASKS_FOR"
    label: Optional[str] = None
    animated: bool = False
    step: int = 0

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    type: str = "supportedByEdge"    # "supportedByEdge" | "triggersEdge" | "conflictsWithEdge" | "asksForEdge"
    data: GraphEdgeData
    animated: bool = False

class GraphPayload(BaseModel):
    graph_id: str
    assessment_id: str
    kb_version: str
    nodes: List[GraphNode]
    edges: List[GraphEdge]
    total_steps: int = 0

class InferenceTrace(BaseModel):
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    assessment_id: str
    kb_version: str
    created_at: str = Field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    initial_facts: List[Dict[str, Any]]
    derived_facts: List[Dict[str, Any]]
    fired_rules: List[RuleFiringRecord]
    skipped_rules: List[RuleSkippedRecord]
    final_conclusions: List[Dict[str, Any]]
    emergency_flagged: bool
    iterations_run: int
    execution_time_ms: float
    graph_payload: GraphPayload

class ExplainabilityEngine:
    @staticmethod
    def build_graph_and_trace(
        assessment_id: str,
        kb_version: str,
        initial_facts: List[Fact],
        working_memory: Dict[str, Fact],
        fired_rules: List[RuleFiringRecord],
        skipped_rules: List[RuleSkippedRecord],
        final_conclusions: List[Conclusion],
        emergency_flagged: bool,
        iterations_run: int,
        execution_time_ms: float
    ) -> InferenceTrace:
        nodes: List[GraphNode] = []
        edges: List[GraphEdge] = []
        node_ids: set = set()

        # Layout tracking (layer X, row Y)
        col_facts_x = 80.0
        col_rules_x = 420.0
        col_conclusions_x = 780.0

        fact_y = 60.0
        rule_y = 60.0
        conc_y = 60.0
        y_spacing = 110.0

        fact_node_map: Dict[str, str] = {}

        # 1. Add Initial User Facts (Col 1)
        for fact in initial_facts:
            nid = f"fact_{fact.name}"
            if nid not in node_ids:
                node_ids.add(nid)
                fact_node_map[fact.name] = nid
                is_emergency_attr = "red_flag" in fact.name.lower() or "chest_pain" in fact.name.lower()
                
                label_clean = fact.name.replace("symptom.", "").replace("_", " ").title()
                val_str = fact.value.value if fact.value else "UNKNOWN"
                
                nodes.append(
                    GraphNode(
                        id=nid,
                        type="factNode",
                        position={"x": col_facts_x, "y": fact_y},
                        data=GraphNodeData(
                            label=label_clean,
                            sublabel=f"Value: {val_str}",
                            node_type="FACT",
                            state="ACTIVE" if fact.value == FactValue.TRUE else "INACTIVE",
                            metadata={
                                "fact_name": fact.name,
                                "value": val_str,
                                "source": fact.source,
                                "raw_value": fact.raw_value
                            },
                            step=0
                        )
                    )
                )
                fact_y += y_spacing

        # 2. Add Fired Rules (Col 2) and Edges
        rule_node_map: Dict[str, str] = {}
        for r_rec in fired_rules:
            rnid = f"rule_{r_rec.rule_id}"
            if rnid not in node_ids:
                node_ids.add(rnid)
                rule_node_map[r_rec.rule_id] = rnid

                is_red = (r_rec.category == "EMERGENCY_RED_FLAG")
                nodes.append(
                    GraphNode(
                        id=rnid,
                        type="safetyNode" if is_red else "ruleNode",
                        position={"x": col_rules_x, "y": rule_y},
                        data=GraphNodeData(
                            label=r_rec.rule_name,
                            sublabel=f"Priority: {r_rec.priority} | Iteration: {r_rec.iteration}",
                            node_type="SAFETY" if is_red else "RULE",
                            state="EMERGENCY" if is_red else "FIRED",
                            metadata={
                                "rule_id": r_rec.rule_id,
                                "category": r_rec.category,
                                "priority": r_rec.priority,
                                "duration_ms": r_rec.execution_duration_ms
                            },
                            step=r_rec.iteration
                        )
                    )
                )
                rule_y += y_spacing

            # Connect matched facts to this fired rule (SUPPORTED_BY)
            for m_fact in r_rec.matched_facts:
                fname = m_fact.get("name")
                if fname and fname in fact_node_map:
                    fnid = fact_node_map[fname]
                    eid = f"edge_{fnid}_{rnid}"
                    edges.append(
                        GraphEdge(
                            id=eid,
                            source=fnid,
                            target=rnid,
                            type="supportedByEdge",
                            animated=True,
                            data=GraphEdgeData(
                                relationship="SUPPORTED_BY",
                                label="Satisfies",
                                animated=True,
                                step=r_rec.iteration
                            )
                        )
                    )

        # 3. Add Conclusions (Col 3) and link with Triggers
        for idx, conc in enumerate(final_conclusions):
            cnid = f"conc_{conc.id}_{idx}"
            if cnid not in node_ids:
                node_ids.add(cnid)
                is_emergency = (conc.recommendation_tier.value == "EMERGENCY")

                nodes.append(
                    GraphNode(
                        id=cnid,
                        type="safetyNode" if is_emergency else "conclusionNode",
                        position={"x": col_conclusions_x, "y": conc_y},
                        data=GraphNodeData(
                            label=conc.summary,
                            sublabel=f"Tier: {conc.recommendation_tier.value} (Conf: {int(conc.confidence * 100)}%)",
                            node_type="CONCLUSION",
                            state="EMERGENCY" if is_emergency else "CONFIRMED",
                            metadata={
                                "conclusion_id": conc.id,
                                "tier": conc.recommendation_tier.value,
                                "confidence": conc.confidence,
                                "detailed_explanation": conc.detailed_explanation,
                                "actionable_steps": conc.actionable_steps
                            },
                            step=idx + 1
                        )
                    )
                )
                conc_y += y_spacing

                # Find the rule that triggered this conclusion
                # Look in fired_rules
                for r_rec in fired_rules:
                    concs = r_rec.asserted_conclusions
                    if any(c.get("id") == conc.id or c.get("fact_name") == conc.fact_name for c in concs):
                        rnid = rule_node_map.get(r_rec.rule_id)
                        if rnid:
                            eid = f"edge_{rnid}_{cnid}"
                            edges.append(
                                GraphEdge(
                                    id=eid,
                                    source=rnid,
                                    target=cnid,
                                    type="triggersEdge",
                                    animated=True,
                                    data=GraphEdgeData(
                                        relationship="TRIGGERS",
                                        label="Concludes",
                                        animated=True,
                                        step=r_rec.iteration
                                    )
                                )
                            )

        # 4. Include a representative sample of Skipped Rules for "Why Not" inspection
        skipped_count = 0
        for s_rec in skipped_rules[:4]:  # Top 4 most relevant skipped rules
            snid = f"skipped_{s_rec.rule_id}"
            if snid not in node_ids:
                node_ids.add(snid)
                nodes.append(
                    GraphNode(
                        id=snid,
                        type="ruleNode",
                        position={"x": col_rules_x, "y": rule_y},
                        data=GraphNodeData(
                            label=s_rec.rule_name,
                            sublabel="Status: Did Not Fire (Unsatisfied)",
                            node_type="RULE",
                            state="SKIPPED",
                            metadata={
                                "rule_id": s_rec.rule_id,
                                "unsatisfied_conditions": s_rec.unsatisfied_conditions,
                                "missing_facts": s_rec.missing_facts
                            },
                            step=0
                        )
                    )
                )
                rule_y += y_spacing
                skipped_count += 1

        graph_payload = GraphPayload(
            graph_id=str(uuid.uuid4()),
            assessment_id=assessment_id,
            kb_version=kb_version,
            nodes=nodes,
            edges=edges,
            total_steps=iterations_run + 1
        )

        derived_facts = [
            f.model_dump(mode="json")
            for f in working_memory.values()
            if f.source == "DERIVED"
        ]

        return InferenceTrace(
            assessment_id=assessment_id,
            kb_version=kb_version,
            initial_facts=[f.model_dump(mode="json") for f in initial_facts],
            derived_facts=derived_facts,
            fired_rules=fired_rules,
            skipped_rules=skipped_rules,
            final_conclusions=[c.model_dump(mode="json") for c in final_conclusions],
            emergency_flagged=emergency_flagged,
            iterations_run=iterations_run,
            execution_time_ms=execution_time_ms,
            graph_payload=graph_payload
        )

