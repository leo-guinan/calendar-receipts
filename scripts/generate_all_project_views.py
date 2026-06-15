#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from calendar_receipts.project_view import build_project_view


def generate_all_project_views(root: Path = ROOT) -> list[Path]:
    config_path = root / "views" / "projects.yaml"
    config = yaml.safe_load(config_path.read_text()) if config_path.exists() else {"projects": []}
    written: list[Path] = []
    for item in config.get("projects", []):
        project = item["project"]
        current_period = item["current_period"]
        weeks_ahead = int(item.get("weeks_ahead", 4))
        markdown = build_project_view(
            project=project,
            current_period=current_period,
            root=root,
            weeks_ahead=weeks_ahead,
        )
        output_path = root / "views" / "projects" / f"{project}.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown)
        written.append(output_path)
    return written


def main() -> int:
    written = generate_all_project_views(ROOT)
    for path in written:
        print(f"Wrote {path}")
    if not written:
        print("No projects configured in views/projects.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
