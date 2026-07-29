"""
Catalog renderer — keeps the site's Components Catalog page in lockstep
with the catalog source.

`components.md` is the specification; `pages/system/components-catalog.html`
is its rendering on the site. The two evolve in parallel by rule (AGENTS.md
§11), and a hand-maintained rendering drifts — entries added to the source
silently never reach the site. This script makes the rendering mechanical:
run it after any change to `components.md`.

Run:  python3 enforcement/render_catalog.py
Exit: 0 on success (the page is rewritten in place).
"""

from __future__ import annotations

from pathlib import Path

import markdown

REPO = Path(__file__).resolve().parents[2]
SOURCE = REPO / "system" / "components.md"
TARGET = REPO / "pages" / "system" / "components-catalog.html"

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Components Catalog · Goodness UI</title>
<link rel="stylesheet" href="../../assets/css/doc.css">
</head>
<body>
<div class="wrap">
  <p class="eyebrow">The System · Components Catalog</p>
  <h1>Components catalog<span class="d">.</span></h1>
  <p class="lede">Every atom, molecule, and organism in the system: what it is, its finite options, an example in the system's idiom, and the reasoning behind each part. The specimen and the white paper render these; this is the specification.</p>
"""

FOOT = """</div>
</body>
</html>
"""


def render(source_md: str) -> str:
    """Pure. The page body for the catalog source."""
    body = source_md.split("\n", 1)[1] if source_md.startswith("# ") else source_md
    html = markdown.markdown(body, extensions=["fenced_code", "tables"])
    return HEAD + html + "\n" + FOOT


def main() -> int:
    TARGET.write_text(render(SOURCE.read_text(encoding="utf-8")), encoding="utf-8")
    print(f"catalog-render: {TARGET.relative_to(REPO)} rewritten from "
          f"{SOURCE.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
