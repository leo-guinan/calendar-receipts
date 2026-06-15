#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from calendar_receipts.project_view import build_project_view


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a stakeholder project view from calendar receipts")
    parser.add_argument("--project", required=True, help="Project slug, e.g. semantic-axis")
    parser.add_argument("--current-period", required=True, help="Weekly period, e.g. 2026-W25")
    parser.add_argument("--weeks-ahead", type=int, default=4, help="Number of weekly columns/sections including current")
    parser.add_argument("--output", help="Markdown output path. Defaults to views/projects/<project>.md")
    args = parser.parse_args()

    markdown = build_project_view(
        project=args.project,
        current_period=args.current_period,
        root=ROOT,
        weeks_ahead=args.weeks_ahead,
    )

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = ROOT / output_path
    else:
        output_path = ROOT / "views" / "projects" / f"{args.project}.md"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
