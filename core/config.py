"""
BROsint Core Config
--------------------
Central place for framework-wide settings. No API keys are hardcoded here —
if a module needs a key (e.g. an optional breach-database lookup you own
credentials for), it reads it from the environment so the framework stays
standalone and nothing is baked into the repo.
"""
import os
from dataclasses import dataclass, field


@dataclass
class Settings:
    app_name: str = "BROsint"
    version: str = "2.0.0"
    http_timeout: int = 8
    user_agent: str = "BROsint/2.0 (+https://github.com/anonymous-beta/Brosint)"
    max_concurrent_requests: int = 20
    output_dir: str = os.environ.get("BROSINT_OUTPUT_DIR", "./output")
    env: dict = field(default_factory=lambda: dict(os.environ))

    def get_secret(self, key: str) -> str | None:
        """Read an optional API key/secret from the environment only.
        Modules must degrade gracefully (skip themselves) if this is None.
        """
        return os.environ.get(key)


settings = Settings()
os.makedirs(settings.output_dir, exist_ok=True)
