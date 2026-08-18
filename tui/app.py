"""
BROsint TUI — run with: python -m tui.app

A terminal-native interface: pick a target type, enter a value, watch
modules run live, browse findings in a tree. This is the "standalone,
no browser needed" way to use BROsint.
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Input, Select, Button, Tree, Log, Static
from textual.reactive import reactive

from core.models import Target, TargetType
from core.engine import Engine
from modules import MODULE_REGISTRY


class BrosintTUI(App):
    CSS = """
    Screen {
        background: #05080d;
    }
    #sidebar {
        width: 34;
        border: round #1fd6c0;
        padding: 1;
    }
    #main {
        border: round #1fd6c0;
    }
    #log {
        height: 10;
        border: round #7a3cff;
    }
    Button {
        background: #10151f;
        color: #1fd6c0;
        border: round #1fd6c0;
    }
    Input {
        border: round #7a3cff;
    }
    Tree {
        background: #05080d;
    }
    """
    TITLE = "BROsint // terminal recon console"
    BINDINGS = [("q", "quit", "Quit")]

    def __init__(self):
        super().__init__()
        self.engine = Engine(MODULE_REGISTRY)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Horizontal():
            with Vertical(id="sidebar"):
                yield Static("TARGET TYPE", classes="label")
                yield Select(
                    [(t.value, t.value) for t in TargetType],
                    id="target_type", value=TargetType.DOMAIN.value,
                )
                yield Static("VALUE", classes="label")
                yield Input(placeholder="e.g. example.com", id="target_value")
                yield Button("Run Scan", id="run_btn", variant="success")
            with Vertical(id="main"):
                yield Tree("Results", id="results_tree")
                yield Log(id="log")
        yield Footer()

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id != "run_btn":
            return
        value = self.query_one("#target_value", Input).value.strip()
        ttype = self.query_one("#target_type", Select).value
        log = self.query_one("#log", Log)
        tree = self.query_one("#results_tree", Tree)
        tree.clear()
        tree.root.label = f"Results: {value}"

        if not value:
            log.write_line("[!] Enter a target value first.")
            return

        target = Target(value=value, type=TargetType(ttype))
        applicable = self.engine.applicable_modules(target)
        log.write_line(f"[*] Running {len(applicable)} module(s): "
                        f"{', '.join(m.name for m in applicable)}")

        def on_done(module_name, count, findings):
            if count < 0:
                log.write_line(f"[x] {module_name} errored")
                return
            log.write_line(f"[+] {module_name}: {count} finding(s)")
            branch = tree.root.add(f"{module_name} ({count})", expand=True)
            for f in findings:
                node = branch.add_leaf(f.label)

        result = await self.engine.scan(target, on_module_done=on_done)
        log.write_line(f"[✓] Scan complete — {len(result.findings)} total findings, "
                        f"{len(result.errors)} error(s).")


def main():
    BrosintTUI().run()


if __name__ == "__main__":
    main()
