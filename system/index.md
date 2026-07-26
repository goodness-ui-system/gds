# Goodness (gds) — Index

Map of content, grouped by audience. Read `AGENTS.md` first in any session.

_Last updated: 2026-07-26_

Status: catalogs of candidates pending a selection pass. The system is named
Goodness (short: gds), companion to the Honest software methodology.
Standing rule: `specimen.html` and `whitepaper.html` evolve in parallel — every
example change lands in both, in the same commit.

## For every reader — the flagship
- [whitepaper.html](whitepaper.html) — the living white paper: 26 chapters, each with the explanation in plain language, the options, the live rendered example right after the words that describe it, the recommendation, a decision-status badge (adopted / recommendation pending / options on display), and per-chapter sources. Built from the system's own tokens, so every example updates itself when a token changes. CSS-only family, theme, and density switches in the header.

## For every reader — orientation
- [README.md](README.md) — what this project is and its current status.
- [index.md](index.md) — this map.

## For the reviewer — the visual reference
- [specimen.html](specimen.html) — the pure rendered catalog: the same examples as the white paper, no prose, titles and option labels only. Order: color families → typography → buttons → inputs → badges → alerts → sections-not-cards → navigation → dashboard (three figure sizes) → progress & ratio → data table → row actions → table editing vs. form editing → record forms (styles, then workflows) → keyboard conventions → filter builder → view system → command palette → empty state.

## For AI agents — the rulebook
- [AGENTS.md](AGENTS.md) — the operating manual read at session start: principles 1–11, token architecture, taxonomy, workflow, the dual-document rule, forbidden patterns, definition of done, and the document map.
- [enforcement/lint_design.py](enforcement/lint_design.py) — design lint R1–R10. `python3 enforcement/lint_design.py` → exit 0 required.
- [enforcement/check_contrast.py](enforcement/check_contrast.py) — every family × theme mapping: WCAG AA floors + dark-mode halation ceilings. `python3 enforcement/check_contrast.py` → exit 0 required.
- [enforcement/design-enforcement.feature](enforcement/design-enforcement.feature) — the same rules as Gherkin; binds to pytest-bdd at app integration.

## For developers — the technical reference
- [components.md](components.md) — the catalog: every atom/molecule/organism with options, states, and code idioms (Jinja + BEM + HTMX), the View System, and the gaps list.
- [tokens.css](tokens.css) — the single source of truth for every value: primitives → semantic aliases, three palette families under one contract, system-first theming, three-step density.
- [ui.css](ui.css) — shared component styles consumed by both rendered documents; token references only.

## Workbench — investigations in progress (not for readers)
Research files hold named sources while an investigation is under way, then their
content graduates into a white-paper chapter.
- [research/record-forms.md](research/record-forms.md) — record-form evidence (graduation into chapter 19 pending).
- [research/table-inline-editing.md](research/table-inline-editing.md) — graduated into chapter 18.
- [research/row-actions.md](research/row-actions.md) — graduated into chapter 17.
- [research/enter-key.md](research/enter-key.md) — graduated into chapter 23.
- [research/theme-parity.md](research/theme-parity.md) — graduated into chapter 3 (full record retained here).
- [research/brand-color-vs-semantics.md](research/brand-color-vs-semantics.md) — graduation into chapter 25 pending.
- [research/deep-analysis.md](research/deep-analysis.md) — the founding briefing; source material for several chapters.

## Scope
One master system for professional, data-dense B2B applications on the Honest
stack. Per-product identity via `[data-brand]` token skins. Standalone until
proven, then propagated into applications.
