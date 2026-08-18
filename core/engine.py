"""
BROsint Engine
--------------
Takes a Target, figures out which registered modules apply, runs them
concurrently with per-module error isolation, and hands the combined
ScanResult to the correlator to build a node/edge graph.
"""
from __future__ import annotations
import asyncio
from typing import Callable, Optional
from core.models import Target, ScanResult
from core.module_base import BaseModule


class Engine:
    def __init__(self, modules: dict[str, BaseModule]):
        self.modules = modules

    def applicable_modules(self, target: Target) -> list[BaseModule]:
        return [m for m in self.modules.values() if m.supports(target) and m.is_available()]

    async def scan(
        self,
        target: Target,
        on_module_done: Optional[Callable[[str, int, list], None]] = None,
    ) -> ScanResult:
        result = ScanResult(target=target)
        mods = self.applicable_modules(target)

        async def run_one(module: BaseModule):
            try:
                findings = await module.run(target)
                for f in findings:
                    result.add(f)
                if on_module_done:
                    on_module_done(module.name, len(findings), findings)
            except Exception as e:
                result.add_error(module.name, f"{type(e).__name__}: {e}")
                if on_module_done:
                    on_module_done(module.name, -1, [])

        await asyncio.gather(*[run_one(m) for m in mods])
        return result
