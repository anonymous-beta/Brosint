"""
Domain recon: WHOIS registration data + DNS record enumeration.
Uses public WHOIS/DNS protocols only — no third-party paid API.
"""
import asyncio
from core.module_base import BaseModule
from core.models import Target, Finding, TargetType, Confidence


class DomainReconModule(BaseModule):
    name = "domain_recon"
    description = "WHOIS registration + DNS record lookup for a domain"
    accepts = (TargetType.DOMAIN,)

    async def run(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []
        loop = asyncio.get_event_loop()

        # --- WHOIS ---
        try:
            import whois  # python-whois
            w = await loop.run_in_executor(None, whois.whois, target.value)
            data = {
                "registrar": _s(w.get("registrar")),
                "creation_date": _s(w.get("creation_date")),
                "expiration_date": _s(w.get("expiration_date")),
                "name_servers": _s(w.get("name_servers")),
                "org": _s(w.get("org")),
                "country": _s(w.get("country")),
            }
            findings.append(Finding(
                module=self.name, target_id=target.id, label="WHOIS record",
                data=data, confidence=Confidence.HIGH,
            ))
        except Exception as e:
            pass  # engine records this in ScanResult.errors via the runner

        # --- DNS records ---
        try:
            import dns.resolver
            records = {}
            for rtype in ("A", "AAAA", "MX", "TXT", "NS", "CNAME"):
                try:
                    answers = await loop.run_in_executor(
                        None, dns.resolver.resolve, target.value, rtype
                    )
                    records[rtype] = [r.to_text() for r in answers]
                except Exception:
                    continue
            if records:
                findings.append(Finding(
                    module=self.name, target_id=target.id, label="DNS records",
                    data=records, confidence=Confidence.HIGH,
                ))
                # SPF/DMARC presence is a useful derived signal
                txt_joined = " ".join(records.get("TXT", []))
                if "v=spf1" in txt_joined:
                    findings.append(Finding(
                        module=self.name, target_id=target.id,
                        label="SPF policy detected", data={"raw": txt_joined},
                        confidence=Confidence.MEDIUM,
                    ))
        except Exception:
            pass

        return findings


def _s(v):
    if isinstance(v, list):
        return [str(x) for x in v]
    return str(v) if v is not None else None
