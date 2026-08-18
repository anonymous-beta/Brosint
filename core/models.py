"""
BROsint Core Data Models
-------------------------
Everything a module produces is a Finding. Findings reference a Target and
optionally other Findings they were derived from — that's what lets the
correlator build a node graph instead of a flat list.
"""
from __future__ import annotations
import time
import uuid
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Any, Optional


class TargetType(str, Enum):
    EMAIL = "email"
    USERNAME = "username"
    DOMAIN = "domain"
    IP = "ip"
    PHONE = "phone"
    FILE = "file"


class Confidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CONFIRMED = "confirmed"


@dataclass
class Target:
    value: str
    type: TargetType
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])


@dataclass
class Finding:
    """A single piece of evidence produced by a module."""
    module: str
    target_id: str
    label: str                     # short human-readable summary, e.g. "MX records"
    data: dict[str, Any]           # structured payload
    confidence: Confidence = Confidence.MEDIUM
    derived_from: Optional[str] = None   # id of another Finding, if chained
    id: str = field(default_factory=lambda: uuid.uuid4().hex[:10])
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict:
        d = asdict(self)
        d["confidence"] = self.confidence.value
        return d


@dataclass
class ScanResult:
    target: Target
    findings: list[Finding] = field(default_factory=list)
    errors: list[dict] = field(default_factory=list)

    def add(self, finding: Finding):
        self.findings.append(finding)

    def add_error(self, module: str, message: str):
        self.errors.append({"module": module, "message": message, "ts": time.time()})

    def to_dict(self) -> dict:
        return {
            "target": asdict(self.target) | {"type": self.target.type.value},
            "findings": [f.to_dict() for f in self.findings],
            "errors": self.errors,
}
