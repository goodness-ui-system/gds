# Goodness — a UI design system

Goodness (short name: gds) is the design-system companion to the Honest software
methodology: the methodology keeps the code honest; the design system keeps the
interface honest.

A best-of-breed UI design system for professional, data-dense B2B applications,
built from scratch — inspired by the visual language of the current generation of
AI-native professional tools — and native to the Honest
stack: FastAPI + Jinja2 + HTMX + domx + CSS custom properties. No client-side framework,
zero JavaScript, system-first theming — dark and light as exact equals, led by the
OS preference and overridable per user.

Design once here; applications adopt the system whole. Product identity is a brand skin
(re-pointed tokens), never a fork. The system is standalone: built and proven in
isolation, then propagated into applications.

Current status: a catalog, not a verdict. Wherever several ways of doing the same
thing exist — record-form styles, dashboard figure sizes, table-editing models —
every credible option is documented and rendered side by side in the specimen, so
the final system can be selected by looking at real examples. The selection pass
comes later; until then, nothing on display is final.

## Start here
- `whitepaper.html` — open it in a browser. The flagship: every design question
  explained in plain language with the options, the live example right after,
  the recommendation, and a decision status. Written for any reader.
- `specimen.html` — the same catalog with no words: a pure visual reference.
  The two evolve in parallel by standing rule.
- `AGENTS.md` — the operating manual. Read every session before touching UI.
- `tokens.css` — the single source of truth for every design decision.
- `enforcement/` — the lint + Gherkin spec that make the rules self-defending:
  `python3 enforcement/lint_design.py` must always exit clean.
- `research/deep-analysis.md` — the expert briefing: the enduring ideas this stands
  on, the aesthetic study, and the mapping onto Honest.

## Principles
1. Systematic + finite — one definition per element, a known option set, no snowflakes.
2. Tokens are CSS custom properties; components are Jinja partials + BEM; behaviour
   is HTMX/domx attributes — zero JavaScript, even for ⌘K.
3. Customization is server-rendered config — users compose their own dashboards,
   tables, and filters; "my view" is a DB row, not client state (DATAOS).
4. Design once, skin many — themes and brands are re-pointed semantic tokens.
5. Enforced, not remembered — lint + contrast checks fail the build on drift.
