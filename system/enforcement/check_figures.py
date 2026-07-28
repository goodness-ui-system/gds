"""
Tabular-figures check — the type half of the palette contract.

The rule (components.md §1.16): any component presenting digits in columns
uses the mono face or declares tabular figures. That rule is only honest if
the shipped faces can keep it, so this check opens the font binaries:

  - every digit advance in each mono face must be uniform
    (tabular by construction);
  - each sans face must carry a `tnum` OpenType feature whose alternate
    digit glyphs are uniform-width.

A face that fails is a bug, not a preference — the palette contract's idea
applied to type.

Honest-shaped: measurement functions are pure over parsed font data; the
only I/O is in main(). Where no faces ship (this repository serves its demo
pages from a font CDN), the check reports and exits clean — the binding
moment is app integration, where faces are self-hosted per AGENTS.md §2.

Run:  python3 enforcement/check_figures.py [root]
Exit: 0 clean or nothing to check, 1 on any violation.
"""

from __future__ import annotations

import sys
from pathlib import Path

FONT_SUFFIXES = (".woff2", ".woff", ".ttf", ".otf")
DIGITS = "0123456789"


def digit_advances(font) -> dict[str, int]:
    """Pure over a parsed font. Advance width per digit, via the best cmap."""
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    out = {}
    for ch in DIGITS:
        glyph = cmap.get(ord(ch))
        if glyph:
            out[ch] = hmtx[glyph][0]
    return out


def tnum_advances(font) -> dict[str, int] | None:
    """Pure over a parsed font. Advance width per digit after applying the
    tnum single-substitution lookups; None when the face has no tnum."""
    if "GSUB" not in font:
        return None
    gsub = font["GSUB"].table
    if not gsub.FeatureList:
        return None
    lookup_indexes: list[int] = []
    for record in gsub.FeatureList.FeatureRecord:
        if record.FeatureTag == "tnum":
            lookup_indexes.extend(record.Feature.LookupListIndex)
    if not lookup_indexes:
        return None
    substitutions: dict[str, str] = {}
    for i in lookup_indexes:
        lookup = gsub.LookupList.Lookup[i]
        for sub in lookup.SubTable:
            mapping = getattr(sub, "mapping", None)
            if mapping:
                substitutions.update(mapping)
    cmap = font.getBestCmap()
    hmtx = font["hmtx"]
    out = {}
    for ch in DIGITS:
        glyph = cmap.get(ord(ch))
        if glyph:
            out[ch] = hmtx[substitutions.get(glyph, glyph)][0]
    return out


def check_face(path: Path, font) -> list[str]:
    """Pure over a parsed font. Violations for one face."""
    name = path.name
    is_mono = "mono" in name.lower()
    base = digit_advances(font)
    if not base:
        return [f"{name}: no digit glyphs resolved — wrong subset shipped?"]
    if is_mono:
        if len(set(base.values())) != 1:
            return [f"{name}: mono face with non-uniform digit advances {sorted(set(base.values()))}"]
        return []
    tab = tnum_advances(font)
    if tab is None:
        return [f"{name}: sans face ships no tnum feature — does not qualify for the system"]
    if len(set(tab.values())) != 1:
        return [f"{name}: tnum alternates are not uniform-width {sorted(set(tab.values()))}"]
    return []


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent
    faces = [p for p in sorted(root.rglob("*")) if p.suffix in FONT_SUFFIXES
             and not any(part.startswith(".") for part in p.parts)]
    if not faces:
        print("figures-check: no shipped font binaries found — nothing to verify here; "
              "the check binds at app integration, where faces are self-hosted.")
        return 0
    try:
        from fontTools.ttLib import TTFont
    except ImportError:
        print("figures-check: fontTools is required to open the shipped faces "
              "(pip install fonttools). Faces present but unverified — failing.")
        return 1
    total = 0
    for path in faces:
        for violation in check_face(path, TTFont(str(path))):
            total += 1
            print(violation)
    print(f"\nfigures-check: {len(faces)} face(s) opened, {total} violation(s)")
    return 1 if total else 0


if __name__ == "__main__":
    raise SystemExit(main())
