"""
Email analysis: syntax validation + domain deliverability signals (MX
records, disposable-domain heuristic). Deliberately does NOT attempt to
verify individual mailbox existence (SMTP probing) or query breach
databases without the user's own API key — see breach_lookup.py for the
opt-in version of that.
"""
import asyncio
import re
from core.module_base import BaseModule
from core.models import Target, Finding, TargetType, Confidence

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# small illustrative set — not exhaustive, meant as a heuristic signal only
DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com",
    "tempmail.com", "yopmail.com", "trashmail.com",
}


class EmailAnalysisModule(BaseModule):
    name = "email_analysis"
    description = "Validates email format and checks domain mail configuration"
    accepts = (TargetType.EMAIL,)

    async def run(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []
        valid_format = bool(EMAIL_RE.match(target.value))
        local, _, domain = target.value.partition("@")

        findings.append(Finding(
            module=self.name, target_id=target.id, label="Format check",
            data={"valid_format": valid_format, "local_part": local, "domain": domain},
            confidence=Confidence.HIGH,
        ))

        if not valid_format or not domain:
            return findings

        if domain.lower() in DISPOSABLE_DOMAINS:
            findings.append(Finding(
                module=self.name, target_id=target.id,
                label="Disposable email domain",
                data={"domain": domain}, confidence=Confidence.MEDIUM,
            ))

        try:
            import dns.resolver
            loop = asyncio.get_event_loop()
            answers = await loop.run_in_executor(None, dns.resolver.resolve, domain, "MX")
            mx_hosts = sorted(r.exchange.to_text() for r in answers)
            findings.append(Finding(
                module=self.name, target_id=target.id, label="MX records",
                data={"mx_hosts": mx_hosts, "has_mail_server": len(mx_hosts) > 0},
                confidence=Confidence.HIGH,
            ))
        except Exception:
            findings.append(Finding(
                module=self.name, target_id=target.id, label="MX records",
                data={"mx_hosts": [], "has_mail_server": False},
                confidence=Confidence.MEDIUM,
            ))

        return findings
