"""
Graph builder: converts one or more ScanResults into a generic node/edge
graph structure that both the TUI (as a tree) and the web frontend (as a
force-directed graph via vis-network) can render.

Node kinds: "target" and "finding". Edges connect a target to each of its
findings, and connect a finding to another finding when it was explicitly
marked as `derived_from` (chained discovery).
"""
from __future__ import annotations
from core.models import ScanResult


def build_graph(results: list[ScanResult]) -> dict:
    nodes = []
    edges = []
    seen_targets = set()

    for result in results:
        t = result.target
        if t.id not in seen_targets:
            nodes.append({
                "id": t.id,
                "label": t.value,
                "group": "target",
                "type": t.type.value,
            })
            seen_targets.add(t.id)

        for f in result.findings:
            nodes.append({
                "id": f.id,
                "label": f.label,
                "group": "finding",
                "module": f.module,
                "confidence": f.confidence.value,
                "data": f.data,
            })
            source = f.derived_from or f.target_id
            edges.append({"from": source, "to": f.id})

    return {"nodes": nodes, "edges": edges}
