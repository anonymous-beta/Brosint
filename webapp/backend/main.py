"""
BROsint web backend — run with: uvicorn webapp.backend.main:app --reload
Serves the REST API the frontend graph UI talks to, plus the static
frontend itself. Everything runs on localhost by default; nothing here
phones home anywhere else.
"""
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import uuid
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from core.models import Target, TargetType
from core.engine import Engine
from modules import MODULE_REGISTRY
from correlator.graph_builder import build_graph

app = FastAPI(title="BROsint API", version="2.0.0")
engine = Engine(MODULE_REGISTRY)

# in-memory store of scan results, keyed by scan id (swap for a real DB if you want persistence)
SCANS: dict[str, list] = {}

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "..", "frontend")


class ScanRequest(BaseModel):
    value: str
    type: str  # matches TargetType values: email, username, domain, ip, phone, file


@app.get("/api/modules")
def list_modules():
    return [
        {"name": m.name, "description": m.description,
         "accepts": [t.value for t in m.accepts], "available": m.is_available()}
        for m in MODULE_REGISTRY.values()
    ]


@app.post("/api/scan")
async def run_scan(req: ScanRequest):
    try:
        ttype = TargetType(req.type)
    except ValueError:
        raise HTTPException(400, f"Unknown target type: {req.type}")

    target = Target(value=req.value, type=ttype)
    result = await engine.scan(target)

    scan_id = uuid.uuid4().hex[:12]
    SCANS[scan_id] = [result]

    return {
        "scan_id": scan_id,
        "result": result.to_dict(),
        "graph": build_graph(SCANS[scan_id]),
    }


@app.get("/api/scan/{scan_id}/graph")
def get_graph(scan_id: str):
    if scan_id not in SCANS:
        raise HTTPException(404, "Scan not found")
    return build_graph(SCANS[scan_id])


@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


app.mount("/static", StaticFiles(directory=os.path.join(FRONTEND_DIR, "static")), name="static")
