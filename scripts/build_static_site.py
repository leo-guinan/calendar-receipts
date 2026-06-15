#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

STYLE = """
:root {
  color-scheme: dark;
  --bg: #08111f;
  --panel: #0f1b2e;
  --panel-2: #142238;
  --text: #eaf0f8;
  --muted: #9fb0c6;
  --border: #27415f;
  --red: #ff6b6b;
  --green: #4ade80;
  --amber: #fbbf24;
  --link: #7dd3fc;
}
* { box-sizing: border-box; }
body {
  margin: 0;
  background: radial-gradient(circle at top left, #14233a 0, var(--bg) 38rem);
  color: var(--text);
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}
a { color: var(--link); }
.page {
  width: min(1040px, calc(100% - 32px));
  margin: 0 auto;
  padding: 42px 0 64px;
}
header {
  border: 1px solid var(--border);
  border-radius: 24px;
  background: rgba(15, 27, 46, 0.86);
  padding: 28px;
  box-shadow: 0 24px 80px rgba(0, 0, 0, 0.28);
}
main {
  margin-top: 24px;
  border: 1px solid var(--border);
  border-radius: 24px;
  background: rgba(15, 27, 46, 0.78);
  overflow: hidden;
}
.content { padding: 28px; }
h1 { margin: 0 0 10px; font-size: clamp(2rem, 5vw, 4rem); letter-spacing: -0.05em; }
h2 { margin: 34px 0 14px; padding-top: 20px; border-top: 1px solid var(--border); }
h3 { margin: 24px 0 10px; color: #d9e7ff; }
p { color: var(--muted); }
ul { padding-left: 1.3rem; }
li { margin: 0.45rem 0; }
.code, code {
  background: #07101d;
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.15rem 0.35rem;
}
.task {
  list-style: none;
  margin-left: -1.3rem;
  border: 1px solid var(--border);
  background: rgba(20, 34, 56, 0.66);
  border-radius: 12px;
  padding: 10px 12px;
}
.task.done { border-color: rgba(74, 222, 128, 0.45); }
.task.open { border-color: rgba(255, 107, 107, 0.42); }
.status {
  display: inline-block;
  margin-left: 0.5rem;
  padding: 0.18rem 0.55rem;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
}
.status-red { background: rgba(255, 107, 107, 0.14); color: var(--red); border: 1px solid rgba(255, 107, 107, 0.45); }
.status-green { background: rgba(74, 222, 128, 0.14); color: var(--green); border: 1px solid rgba(74, 222, 128, 0.45); }
.status-partial { background: rgba(251, 191, 36, 0.14); color: var(--amber); border: 1px solid rgba(251, 191, 36, 0.45); }
.grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(260px, 1fr)); gap: 16px; margin-top: 24px; }
.card { display: block; text-decoration: none; color: var(--text); padding: 20px; border: 1px solid var(--border); border-radius: 18px; background: rgba(20, 34, 56, 0.7); }
.card:hover { border-color: var(--link); }
.meta { color: var(--muted); font-size: 0.92rem; }
.footer { margin-top: 24px; color: var(--muted); font-size: 0.9rem; }
""".strip()


def titleize_project(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.replace("_", "-").split("-"))


def slug_from_project_md(path: Path) -> str:
    return path.stem


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r'<code>\1</code>', escaped)
    return escaped


def markdown_to_html(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    in_ul = False

    def close_ul() -> None:
        nonlocal in_ul
        if in_ul:
            out.append("</ul>")
            in_ul = False

    for raw in lines:
        line = raw.rstrip()
        if not line:
            close_ul()
            continue
        if line.startswith("### "):
            close_ul()
            out.append(f"<h3>{inline_markdown(line[4:])}</h3>")
        elif line.startswith("## "):
            close_ul()
            out.append(f"<h2>{inline_markdown(line[3:])}</h2>")
        elif line.startswith("# "):
            close_ul()
            title = inline_markdown(line[2:])
            out.append(f"<h1>{title}</h1>")
        elif line.startswith("- [ ] ") or line.startswith("- [x] "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            done = line.startswith("- [x] ")
            body = line[6:]
            symbol = "✓" if done else "×"
            cls = "done" if done else "open"
            out.append(f'<li class="task {cls}"><strong>{symbol}</strong> {inline_markdown(body)}</li>')
        elif line.startswith("- "):
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_markdown(line[2:])}</li>")
        else:
            close_ul()
            rendered = inline_markdown(line)
            rendered = rendered.replace("Current status: RED", 'Current status: RED <span class="status status-red">RED</span>')
            rendered = rendered.replace("Current status: GREEN", 'Current status: GREEN <span class="status status-green">GREEN</span>')
            rendered = rendered.replace("Current status: PARTIAL", 'Current status: PARTIAL <span class="status status-partial">PARTIAL</span>')
            out.append(f"<p>{rendered}</p>")
    close_ul()
    return "\n".join(out)


def page_template(title: str, body: str, source_href: str | None = None) -> str:
    source = f'<p class="meta">Source: <a href="{html.escape(source_href)}">{html.escape(source_href)}</a></p>' if source_href else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>{STYLE}</style>
</head>
<body>
  <div class="page">
    <header>
      <div class="meta">Calendar Receipts stakeholder view</div>
      <h1>{html.escape(title)}</h1>
      <p>Generated from expectations and receipts. If the receipts are missing, the view stays red. Grim, but useful.</p>
      {source}
    </header>
    <main><div class="content">
{body}
    </div></main>
    <div class="footer">Receipt-driven project view. No hand-edited dashboard state.</div>
  </div>
</body>
</html>
"""


def build_index(root: Path, output_dir: Path, project_files: list[Path]) -> None:
    cards = []
    for md_path in sorted(project_files):
        slug = slug_from_project_md(md_path)
        text = md_path.read_text()
        status = "RED" if "Current status: RED" in text else "GREEN" if "Current status: GREEN" in text else "PARTIAL" if "Current status: PARTIAL" in text else "UNKNOWN"
        cards.append(
            f'<a class="card" href="projects/{html.escape(slug)}/">'
            f'<h3>{html.escape(titleize_project(slug))}</h3>'
            f'<div class="meta">Status: {html.escape(status)}</div>'
            '</a>'
        )
    body = '<h2>Project views</h2>\n<div class="grid">' + "\n".join(cards) + "</div>"
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(page_template("Calendar Receipts", body))


def build_static_site(root: Path | None = None) -> Path:
    root = root or ROOT
    output_dir = root / "site"
    projects_dir = root / "views" / "projects"
    project_files = sorted(projects_dir.glob("*.md")) if projects_dir.exists() else []

    output_dir.mkdir(parents=True, exist_ok=True)
    build_index(root, output_dir, project_files)

    for md_path in project_files:
        slug = slug_from_project_md(md_path)
        source_rel = md_path.relative_to(root).as_posix()
        html_body = markdown_to_html(md_path.read_text())
        page = page_template(titleize_project(slug), html_body, source_href=f"https://github.com/leo-guinan/calendar-receipts/blob/main/{source_rel}")
        target = output_dir / "projects" / slug / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page)

    return output_dir


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static stakeholder pages from project views")
    parser.add_argument("--root", default=str(ROOT))
    args = parser.parse_args()
    output = build_static_site(Path(args.root))
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
