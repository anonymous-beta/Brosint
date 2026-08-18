#!/usr/bin/env python3
"""
BROsint entry point.

    python brosint.py --tui              launch the terminal UI (default)
    python brosint.py --web              launch the web UI at http://127.0.0.1:8000
    python brosint.py --domain X.com     run a one-off scan straight from the CLI
    python brosint.py --email a@b.com
    python brosint.py --username foo
    python brosint.py --ip 1.2.3.4
"""
import argparse
import asyncio
import json
import sys


def main():
    parser = argparse.ArgumentParser(description="BROsint — standalone OSINT framework")
    parser.add_argument("--tui", action="store_true", help="Launch terminal UI")
    parser.add_argument("--web", action="store_true", help="Launch web UI (FastAPI + browser graph)")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--domain")
    parser.add_argument("--email")
    parser.add_argument("--username")
    parser.add_argument("--ip")
    args = parser.parse_args()

    if args.web:
        import uvicorn
        print(f"[BROsint] Web UI starting → http://127.0.0.1:{args.port}")
        uvicorn.run("webapp.backend.main:app", host="127.0.0.1", port=args.port, reload=False)
        return

    one_off = args.domain or args.email or args.username or args.ip
    if one_off:
        from core.models import Target, TargetType
        from core.engine import Engine
        from modules import MODULE_REGISTRY

        if args.domain:
            target = Target(value=args.domain, type=TargetType.DOMAIN)
        elif args.email:
            target = Target(value=args.email, type=TargetType.EMAIL)
        elif args.username:
            target = Target(value=args.username, type=TargetType.USERNAME)
        else:
            target = Target(value=args.ip, type=TargetType.IP)

        engine = Engine(MODULE_REGISTRY)
        result = asyncio.run(engine.scan(target))
        print(json.dumps(result.to_dict(), indent=2, default=str))
        return

    # default: TUI
    from tui.app import main as tui_main
    tui_main()


if __name__ == "__main__":
    sys.exit(main() or 0)
