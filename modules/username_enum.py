"""
Username enumeration: checks whether a username exists on a curated list of
public platforms by requesting each site's public profile URL and reading
the HTTP status / page markers. This only queries information the sites
already serve publicly to any visitor — it does not log in, bypass auth,
or access private data.
"""
import asyncio
import httpx
from core.module_base import BaseModule
from core.models import Target, Finding, TargetType, Confidence
from core.config import settings

# name -> (profile url template, marker that indicates "not found" even on HTTP 200)
SITES = {
    "GitHub":      ("https://github.com/{u}", None),
    "GitLab":      ("https://gitlab.com/{u}", None),
    "Reddit":      ("https://www.reddit.com/user/{u}/about.json", None),
    "HackerNews":  ("https://news.ycombinator.com/user?id={u}", "No such user"),
    "Instagram":   ("https://www.instagram.com/{u}/", None),
    "X/Twitter":   ("https://x.com/{u}", None),
    "Medium":      ("https://medium.com/@{u}", None),
    "DevTo":       ("https://dev.to/{u}", None),
    "Keybase":     ("https://keybase.io/{u}", None),
    "Pinterest":   ("https://www.pinterest.com/{u}/", None),
}


class UsernameEnumModule(BaseModule):
    name = "username_enum"
    description = "Checks public profile existence for a username across common platforms"
    accepts = (TargetType.USERNAME,)

    async def run(self, target: Target) -> list[Finding]:
        findings: list[Finding] = []
        sem = asyncio.Semaphore(settings.max_concurrent_requests)

        async with httpx.AsyncClient(
            headers={"User-Agent": settings.user_agent},
            timeout=settings.http_timeout,
            follow_redirects=True,
        ) as client:

            async def check(site, template_marker):
                template, not_found_marker = template_marker
                url = template.format(u=target.value)
                async with sem:
                    try:
                        resp = await client.get(url)
                    except Exception:
                        return None
                exists = resp.status_code == 200
                if exists and not_found_marker and not_found_marker in resp.text:
                    exists = False
                return (site, url, exists, resp.status_code)

            results = await asyncio.gather(*[
                check(site, tm) for site, tm in SITES.items()
            ])

        hits = [r for r in results if r and r[2]]
        if hits:
            findings.append(Finding(
                module=self.name, target_id=target.id,
                label=f"Username found on {len(hits)} platform(s)",
                data={"matches": [{"site": s, "url": u} for s, u, _, _ in hits]},
                confidence=Confidence.MEDIUM,
            ))
        for s, u, exists, code in results:
            if exists:
                findings.append(Finding(
                    module=self.name, target_id=target.id,
                    label=f"Profile on {s}",
                    data={"url": u, "status_code": code},
                    confidence=Confidence.MEDIUM,
                ))
        return findings
