"""
Contrast checker — the color-math enforcement layer for AGENTS.md.

Honest-shaped: pure functions throughout; the only I/O is in main().

Verifies every palette family in every theme (all combinations declared in
tokens.css) against two kinds of law:

  FLOORS (WCAG 2.2 AA — apply in both modes, no exceptions):
    text, muted, action, and every semantic hue ≥ 4.5:1 on canvas and surface;
    on-action ≥ 4.5:1 on the action color.

  CEILINGS (halation — dark themes; see research/theme-parity.md):
    body text is never pure white and never brighter than #EBEBEB effective;
    the canvas is never pure black. Bright white on dark glows (halation) —
    per the Material dark-theme spec, APCA guidance, and the astigmatism
    evidence; contrast has a ceiling in dark mode, but never a basement.

Run:  python3 enforcement/check_contrast.py [tokens.css]
Exit: 0 clean, 1 violations found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FLOOR = 4.5
TEXT_CEILING_HEX = "#ebebeb"   # top of the recommended dark-mode text band
CANVAS_FLOOR_HEX = "#0a0a0a"   # darkest sanctioned canvas (never #000000)

TEXT_ROLES = ("text", "text-muted", "action", "success", "warning", "danger", "info")


def luminance(hexcolor: str) -> float:
    """Pure. WCAG relative luminance of a #rrggbb color."""
    h = hexcolor.lstrip("#")
    channels = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
              for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def ratio(a: str, b: str) -> float:
    """Pure. WCAG contrast ratio between two hex colors."""
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def parse_primitives(css: str) -> dict:
    """Pure. Every --name: #hex declaration in the file."""
    return {m.group(1): m.group(2).lower()
            for m in re.finditer(r"--([\w-]+)\s*:\s*(#[0-9a-fA-F]{6})\b", css)}


def parse_block(css: str, selector_re: str) -> dict:
    """Pure. Alias → primitive-name across ALL blocks matching the selector
    (tokens.css uses several :root blocks); var() references only."""
    merged = {}
    for m in re.finditer(selector_re + r"\s*\{(.*?)\}", css, re.DOTALL):
        for a in re.finditer(r"--color-([\w-]+)\s*:\s*var\(--([\w-]+)\)",
                             m.group(1)):
            merged[a.group(1)] = a.group(2)
    return merged


def resolve_mappings(css: str) -> dict:
    """Pure. (family, theme) → {role: hex} for every declared combination,
    emulating the cascade: root → light → family → family+light."""
    prim = parse_primitives(css)
    root = parse_block(css, r":root")
    light = parse_block(css, r'\[data-theme="light"\]')
    combos = {("warm", "dark"): [root], ("warm", "light"): [root, light]}
    for fam in ("cool", "mono"):
        fam_block = parse_block(css, r'\[data-palette="' + fam + r'"\]')
        both = parse_block(
            css, r'\[data-palette="' + fam + r'"\]\[data-theme="light"\]')
        if fam_block:
            combos[(fam, "dark")] = [root, fam_block]
            combos[(fam, "light")] = [root, light, fam_block, both]
    out = {}
    for key, layers in combos.items():
        merged = {}
        for layer in layers:
            merged.update(layer)
        out[key] = {role: prim[name] for role, name in merged.items()
                    if name in prim}
    return out


def check_mapping(family: str, theme: str, colors: dict) -> list[str]:
    """Pure. All violations for one family+theme mapping."""
    problems = []
    for surface in ("canvas", "surface"):
        bg = colors.get(surface)
        if not bg:
            continue
        for role in TEXT_ROLES:
            fg = colors.get(role)
            if fg and ratio(fg, bg) < FLOOR:
                problems.append(
                    f"{family}/{theme}: {role} {fg} on {surface} {bg} = "
                    f"{ratio(fg, bg):.2f}:1 (floor {FLOOR}:1)")
    if colors.get("on-action") and colors.get("action"):
        r = ratio(colors["on-action"], colors["action"])
        if r < FLOOR:
            problems.append(
                f"{family}/{theme}: on-action on action = {r:.2f}:1 "
                f"(floor {FLOOR}:1)")
    if theme == "dark":
        text, canvas = colors.get("text"), colors.get("canvas")
        if text and (text == "#ffffff"
                     or luminance(text) > luminance(TEXT_CEILING_HEX)):
            problems.append(
                f"{family}/dark: text {text} exceeds the halation ceiling "
                f"({TEXT_CEILING_HEX}) — bright white glows on dark")
        if canvas and (canvas == "#000000"
                       or luminance(canvas) < luminance(CANVAS_FLOOR_HEX)):
            problems.append(
                f"{family}/dark: canvas {canvas} below the sanctioned floor "
                f"({CANVAS_FLOOR_HEX}) — never pure black")
    return problems


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else \
        Path(__file__).resolve().parent.parent / "tokens.css"
    css = path.read_text(encoding="utf-8")
    mappings = resolve_mappings(css)
    total = 0
    for (family, theme), colors in sorted(mappings.items()):
        problems = check_mapping(family, theme, colors)
        checked = sum(1 for r in TEXT_ROLES for srf in ("canvas", "surface")
                      if colors.get(r) and colors.get(srf))
        status = "FAIL" if problems else "pass"
        print(f"{status}  {family}/{theme}: {checked} pairs checked, "
              f"{len(problems)} problem(s)")
        for p in problems:
            print("      " + p)
        total += len(problems)
    print(f"\ncontrast-check: {len(mappings)} mappings, {total} violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
