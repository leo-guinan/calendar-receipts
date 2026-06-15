from pathlib import Path

from scripts.build_static_site import build_static_site


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


def test_static_site_renders_project_markdown_to_shareable_html(tmp_path):
    write(
        tmp_path / "views" / "projects" / "semantic-axis.md",
        """# semantic-axis project view

Current status: RED

## Current initiative — 2026-W25

- [ ] saved-report-permalink-ux-artifact-captured
- [x] existing-receipt
""",
    )

    output_dir = build_static_site(root=tmp_path)

    page = output_dir / "projects" / "semantic-axis" / "index.html"
    assert page.exists()
    html = page.read_text()
    assert "semantic-axis project view" in html
    assert "Current status: RED" in html
    assert "saved-report-permalink-ux-artifact-captured" in html
    assert "class=\"status status-red\"" in html
    assert "views/projects/semantic-axis.md" in html

    index = (output_dir / "index.html").read_text()
    assert "Semantic Axis" in index
    assert "projects/semantic-axis/" in index
