"""
IP geolocation via ip-api.com's free public endpoint (no key required,
rate-limited to 45 req/min per their terms). Swap in your own provider
by editing the URL below if you have one.
"""
import httpx
from core.module_base import BaseModule
from core.models import Target, Finding, TargetType, Confidence
from core.config import settings


class IPGeolocationModule(BaseModule):
    name = "ip_geolocation"
    description = "Approximate geolocation and ASN info for an IP address"
    accepts = (TargetType.IP,)

    async def run(self, target: Target) -> list[Finding]:
        url = f"http://ip-api.com/json/{target.value}?fields=status,message,country,regionName,city,isp,org,as,lat,lon,query"
        async with httpx.AsyncClient(
            headers={"User-Agent": settings.user_agent}, timeout=settings.http_timeout
        ) as client:
            resp = await client.get(url)
            data = resp.json()

        if data.get("status") != "success":
            return [Finding(
                module=self.name, target_id=target.id, label="Geolocation lookup failed",
                data={"message": data.get("message", "unknown error")},
                confidence=Confidence.LOW,
            )]

        return [Finding(
            module=self.name, target_id=target.id, label="IP geolocation",
            data={
                "country": data.get("country"),
                "region": data.get("regionName"),
                "city": data.get("city"),
                "isp": data.get("isp"),
                "org": data.get("org"),
                "asn": data.get("as"),
                "lat": data.get("lat"),
                "lon": data.get("lon"),
            },
            confidence=Confidence.MEDIUM,
        )]
