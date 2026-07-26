"""
Design-system lint — the enforcement layer for AGENTS.md.

Honest-shaped: every check is a pure function (text in, violations out);
the only I/O is in main(), at the boundary.

Rules enforced (see enforcement/design-enforcement.feature):
  R1  no raw hex colors in CSS outside tokens.css
  R2  no style= attributes in HTML
  R3  no !important
  R4  no box-shadow outside tokens.css unless the value is var(--shadow-overlay) or none
  R5  no px literals outside tokens.css except 0px / 1px (hairline) / 2px (emphasis line)
  R6  every CSS class selector is BEM: block / block__element / block--modifier
  R7  no imperative JS in HTML: <script>, addEventListener, querySelector,
      innerHTML, fetch(  — behaviour belongs to HTMX/domx attributes
  R8  impersonal voice in documents: no we / our / ours / us / let's
      (URLs, inline code, and fenced code blocks are exempt)
  R9  no named entities: identity names are banned everywhere; benchmark
      product names are banned outside research/ (citations live there)
  R10 the palette contract: every family in tokens.css defines the
      identical set of named steps — neutral ramps match step-for-step,
      accent ramps match step-for-step; a missing or extra step fails

Run:  python3 enforcement/lint_design.py [root]
Exit: 0 clean, 1 violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

TOKENS_FILE = "tokens.css"

BEM_RE = re.compile(
    r"^[a-z][a-z0-9]*(?:-[a-z0-9]+)*"      # block (kebab)
    r"(?:__[a-z0-9]+(?:-[a-z0-9]+)*)?"     # optional __element
    r"(?:--[a-z0-9]+(?:-[a-z0-9]+)*)?$"    # optional --modifier
)
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")
PX_RE = re.compile(r"(?<![\w-])(\d+(?:\.\d+)?)px\b")
CLASS_SEL_RE = re.compile(r"\.([A-Za-z_][A-Za-z0-9_-]*)")
STYLE_ATTR_RE = re.compile(r"\bstyle\s*=", re.IGNORECASE)
JS_MARKERS = ("<script", "addEventListener", "querySelector", "innerHTML", "fetch(")
ALLOWED_PX = {"0", "1", "2"}


def line_of(text: str, index: int) -> int:
    """Pure. 1-based line number of a character index."""
    return text.count("\n", 0, index) + 1


def strip_css_comments(css: str) -> str:
    """Pure. Blank out /* … */ comments, preserving newlines for line numbers."""
    return re.sub(
        r"/\*.*?\*/",
        lambda m: re.sub(r"[^\n]", " ", m.group(0)),
        css,
        flags=re.DOTALL,
    )


def css_contexts(name: str, text: str) -> list[tuple[str, int]]:
    """Pure. Return (css_text, char_offset) chunks: whole file for .css,
    <style> blocks for .html. Comments blanked."""
    if name.endswith(".css"):
        return [(strip_css_comments(text), 0)]
    chunks = []
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.DOTALL | re.IGNORECASE):
        chunks.append((strip_css_comments(m.group(1)), m.start(1)))
    return chunks


def check_hex(name: str, text: str) -> list[dict]:
    """R1. Pure."""
    if name == TOKENS_FILE:
        return []
    out = []
    for css, off in css_contexts(name, text):
        for m in HEX_RE.finditer(css):
            out.append({"rule": "R1-raw-hex", "line": line_of(text, off + m.start()),
                        "detail": m.group(0)})
    return out


def check_px(name: str, text: str) -> list[dict]:
    """R5. Pure."""
    if name == TOKENS_FILE:
        return []
    out = []
    for css, off in css_contexts(name, text):
        for m in PX_RE.finditer(css):
            if m.group(1) not in ALLOWED_PX:
                out.append({"rule": "R5-raw-px", "line": line_of(text, off + m.start()),
                            "detail": m.group(0)})
    return out


def check_important(name: str, text: str) -> list[dict]:
    """R3. Pure."""
    out = []
    for css, off in css_contexts(name, text):
        for m in re.finditer(r"!important", css):
            out.append({"rule": "R3-important", "line": line_of(text, off + m.start()),
                        "detail": "!important"})
    return out


def check_box_shadow(name: str, text: str) -> list[dict]:
    """R4. Pure."""
    if name == TOKENS_FILE:
        return []
    out = []
    for css, off in css_contexts(name, text):
        for m in re.finditer(r"box-shadow\s*:\s*([^;}]+)", css):
            value = m.group(1).strip()
            if value not in ("var(--shadow-overlay)", "none"):
                out.append({"rule": "R4-shadow", "line": line_of(text, off + m.start()),
                            "detail": value[:60]})
    return out


def check_bem(name: str, text: str) -> list[dict]:
    """R6. Pure."""
    out = []
    for css, off in css_contexts(name, text):
        for m in CLASS_SEL_RE.finditer(css):
            cls = m.group(1)
            if not BEM_RE.match(cls):
                out.append({"rule": "R6-bem", "line": line_of(text, off + m.start()),
                            "detail": "." + cls})
    return out


def check_style_attr(name: str, text: str) -> list[dict]:
    """R2. Pure."""
    if not name.endswith(".html"):
        return []
    out = []
    for m in STYLE_ATTR_RE.finditer(text):
        out.append({"rule": "R2-style-attr", "line": line_of(text, m.start()),
                    "detail": "style="})
    return out


def check_js(name: str, text: str) -> list[dict]:
    """R7. Pure."""
    if not name.endswith(".html"):
        return []
    out = []
    for marker in JS_MARKERS:
        for m in re.finditer(re.escape(marker), text):
            if marker == "<script" and "htmx" in text[m.start():m.start() + 200]:
                continue  # app shells load the htmx/domx libraries themselves
            out.append({"rule": "R7-imperative-js", "line": line_of(text, m.start()),
                        "detail": marker})
    return out


CHECKS = (check_hex, check_px, check_important, check_box_shadow,
          check_bem, check_style_attr, check_js)

PROSE_SUFFIXES = (".md", ".feature", ".html")
FIRST_PERSON_RE = re.compile(r"\b(?:[Ww]e|[Oo]urs?|[Ll]et's)\b|\bus\b")
IDENTITY_NAMES = ("Vincent", "Guyaux", "Monkbeast", "Buckler", "Brac3r",
                  "Bracer", "OpenVRM", "Segouro", "Embrase",
                  "TD Bank", "CIBC", "Vanguard")
BENCHMARK_NAMES = ("Airtable", "Notion", "Figma", "Retool", "Anthropic",
                   "Claude", "Conductor", "Omnigent", "Raycast", "Vercel")


def prose_text(name: str, text: str) -> str:
    """Pure. Strip the zones exempt from prose rules: fenced code, inline
    code, URLs, and <style> blocks — preserving newlines for line numbers."""
    blank = lambda m: re.sub(r"[^\n]", " ", m.group(0))
    if name.endswith((".md", ".feature")):
        text = re.sub(r"```.*?```", blank, text, flags=re.DOTALL)
        text = re.sub(r"`[^`\n]+`", blank, text)
    if name.endswith(".html"):
        text = re.sub(r"<style[^>]*>.*?</style>", blank, text,
                      flags=re.DOTALL | re.IGNORECASE)
    return re.sub(r"https?://\S+", blank, text)


def check_first_person(name: str, text: str) -> list[dict]:
    """R8. Pure."""
    if not name.endswith(PROSE_SUFFIXES):
        return []
    stripped = prose_text(name, text)
    return [{"rule": "R8-first-person", "line": line_of(stripped, m.start()),
             "detail": m.group(0)} for m in FIRST_PERSON_RE.finditer(stripped)]


def check_named_entities(name: str, text: str, in_research: bool = False) -> list[dict]:
    """R9. Pure."""
    if not name.endswith(PROSE_SUFFIXES):
        return []
    stripped = prose_text(name, text)
    banned = IDENTITY_NAMES if in_research else IDENTITY_NAMES + BENCHMARK_NAMES
    out = []
    for word in banned:
        for m in re.finditer(r"\b" + re.escape(word) + r"\b", stripped):
            out.append({"rule": "R9-named-entity",
                        "line": line_of(stripped, m.start()), "detail": word})
    return out


PALETTE_FAMILIES = {"neutral": ("neutral", "cool", "gray"),
                    "accent": ("clay", "azure", "ink")}


def check_palette_contract(name: str, text: str) -> list[dict]:
    """R10. Pure. Every family defines the identical set of named steps."""
    if name != TOKENS_FILE:
        return []
    out = []
    for kind, ramps in PALETTE_FAMILIES.items():
        steps = {r: set(re.findall(r"--" + r + r"-(\d+)\s*:", text)) for r in ramps}
        reference = steps[ramps[0]]
        for ramp in ramps[1:]:
            for missing in sorted(reference - steps[ramp], key=int):
                out.append({"rule": "R10-palette-contract", "line": 1,
                            "detail": f"--{ramp}-{missing} missing ({kind} step exists in {ramps[0]})"})
            for extra in sorted(steps[ramp] - reference, key=int):
                out.append({"rule": "R10-palette-contract", "line": 1,
                            "detail": f"--{ramp}-{extra} has no {ramps[0]} counterpart"})
    return out


def find_violations(name: str, text: str, in_research: bool = False) -> list[dict]:
    """Pure. All violations for one file."""
    found = [v for check in CHECKS for v in check(name, text)]
    found += check_first_person(name, text)
    found += check_named_entities(name, text, in_research)
    found += check_palette_contract(name, text)
    return found


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    files = [p for p in sorted(root.rglob("*"))
             if p.suffix in (".css", ".html", ".md", ".feature")
             and not any(part.startswith(".") for part in p.parts)]
    total = 0
    for path in files:
        in_research = "research" in path.parts
        violations = find_violations(path.name, path.read_text(encoding="utf-8"),
                                     in_research)
        for v in violations:
            total += 1
            print(f"{path.relative_to(root)}:{v['line']}  {v['rule']}  {v['detail']}")
    print(f"\ndesign-lint: {len(files)} file(s) scanned, {total} violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
