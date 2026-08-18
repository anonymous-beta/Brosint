"""
BROsint Module Base
--------------------
Every OSINT module is a small, self-contained class. To add a new module:

    1. Subclass BaseModule
    2. Set `name`, `accepts` (which TargetTypes it can run against)
    3. Implement `run(target) -> list[Finding]`
    4. Register it in modules/__init__.py's MODULE_REGISTRY

The engine handles concurrency, timeouts, and error isolation — a module
raising an exception never crashes the scan, it just gets logged as an
error and the rest of the scan continues.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from core.models import Target, Finding, TargetType


class BaseModule(ABC):
    name: str = "base"
    description: str = ""
    accepts: tuple[TargetType, ...] = ()
    requires_key: str | None = None   # env var name, if this module needs one

    def supports(self, target: Target) -> bool:
        return target.type in self.accepts

    @abstractmethod
    async def run(self, target: Target) -> list[Finding]:
        """Perform the lookup and return a list of Finding objects."""
        raise NotImplementedError

    def is_available(self) -> bool:
        """Modules that need an optional key report themselves unavailable
        instead of failing loudly, so the framework stays standalone by default."""
        if self.requires_key is None:
            return True
        from core.config import settings
        return settings.get_secret(self.requires_key) is not None
