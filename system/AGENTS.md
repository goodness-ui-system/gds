# Goodness (gds) — Agent Operating Manual

This project is a best-of-breed UI design system for professional, data-dense B2B
applications built on the Honest stack.
Design once here; applications adopt the system and inherit it whole — per-product
identity is a brand skin, never a fork. Read this file first, every session, before
designing or changing any UI.

Companions:
- `tokens.css` — the single source of truth for every design decision (§4).
- `specimen.html` — the whole system, rendered. Open it in a browser.
- `enforcement/` — the lint + Gherkin spec that make the rules self-defending (§9).
- `research/deep-analysis.md` — the *why* and the references behind these rules.

**Machine-mode.** Durable fix over patch. Concise. "go" means execute. Say when something
is wrong and propose the correct path.

**Documentation style.** These documents are written for publication: any reader,
anywhere, with no knowledge of the author. Four rules, enforced by the prose lint:

1. No bold inside paragraphs — bold is reserved for titles and headings. Readers
   find what matters in a sentence themselves; mid-sentence bolding disrupts reading
   and steals attention from everything not bolded. Italics sparingly.
2. Impersonal voice. Never `we`, `our`, `us`, or `let's` — no implied speaker,
   seller, or team. Write about the situation, the market, and the method: "a
   company whose brand color is red…", "best practice suggests…", "the system
   supports…". Recommendations are attributed to the method or to best practice,
   never to a narrator.
3. No named entities as examples. No companies, products, people, or industries as
   hypothetical actors — "a green-brand enterprise" says everything a real name
   would. Nothing in any document may reveal what sector the author works in or
   who the author is. Fictional placeholder names in demo data are fine.
4. Citations are welcome, and are the one place names belong: public standards,
   methodologies, and published systems may be cited inline where a claim is made,
   and listed under a Sources heading at the end of the file.
5. Plain language, always. Explanations are written so a reader with no design or
   engineering background follows them: prefer the everyday word, keep sentences
   concrete, and define every term of art in ordinary words the first time it
   appears ("a draft — changes made on screen but not yet written to the
   database"). Jargon without a definition is a defect, not a shorthand.
6. Every part explained. Whenever a component embodies a decision or offers an
   option, the document names each part and gives the reason it exists and the
   reason it sits where it sits ("Hide all lives above the list because, with
   thirty fields and three wanted, hiding everything and re-enabling three beats
   flipping twenty-seven switches"). A part that cannot be justified in one plain
   sentence is a candidate for removal, not for silence.

Examples given in conversation are context for the session — they are never
transcribed into documents.

**Catalog status.** Until a selection pass happens, the documents and the specimen
are catalogs of candidates, not verdicts. Where several ways of doing the same
thing exist (form presentation styles, figure sizes, table-editing models), every
credible option is documented and rendered side by side so the final system can be
chosen by looking at real examples. New research adds options to the catalog; it
does not silently pick winners. Decisions, once made, are recorded explicitly and
losers are removed in the same change.

---

## 1. Mission

Kill visual drift. Many apps, one system. Never "here is the app, take it or leave it" —
instead give users a finite, consistent kit of parts they can compose into their own
screens, dashboards, tables, and filters. Every element is defined once, with an
explicit, finite set of options, so it's easy to pick the right one and impossible to
invent a snowflake.

Two words govern every decision: systematic (one definition, reused) and finite
(a known option set, not infinite freedom).

## 2. The medium — non-negotiable

Target applications are Honest apps: FastAPI + Jinja2 + HTMX + domx + PostgreSQL,
DOM-as-state, no client-side framework. The Honest rules (the sixteen principles,
Gherkin-first, the forbidden-patterns tables) govern here too. What that means for UI:

- Tokens = CSS custom properties in `tokens.css`. Nothing else holds a colour or size.
- Components = Jinja partials / macros + BEM classes. No React, Vue, Alpine,
  Tailwind, CSS-in-JS, or utility frameworks.
- Behaviour = HTMX attributes (`hx-get/post/put/delete`, `hx-target`, `hx-swap`,
  `hx-trigger`, `hx-push-url`, `hx-include`). No hand-written JS event wiring, no
  `fetch`, no `addEventListener`, no client state store. Zero JS — even keyboard
  shortcuts are declarative (§7).
- domx (the DATAOS companion library) is the sanctioned tool when DOM state must be
  *collected, applied, observed, or persisted* — e.g. capturing a user's current view
  configuration to send to the server. It works declaratively via a manifest and the
  `hx-ext="domx"` extension (`dx-manifest`, `dx-cache`). Reach for it instead of ever
  writing imperative JS; if neither HTMX nor domx covers a need, the route is returning
  the wrong HTML shape — fix the route.
- State lives on the server, rendered to HTML, swapped by HTMX (P06 DATAOS).
- Validation is native + declared (`type=email`, `required`, `min`, SQL constraints)
  per P11 — never imperative checks.

## 3. Design principles

1. One accent, used sparingly. The clay accent marks the primary action and the
   active/selected state. Never decorate with it. The primary button is the only pill.
2. Depth from the surface ladder + 1px hairlines. No drop shadows in app chrome. One
   shadow token exists, only for floating overlays (palette, menu, popover).
3. System-first theming. The OS preference leads (`prefers-color-scheme`); a stored
   per-user choice (`data-theme`, rendered server-side — never a flash of the wrong
   theme) overrides it. Dark and light are exact equals: neither is primary, neither
   is derived; both mappings share one ramp and are contrast-solved independently.
   The craft rules of parity (no pure white text on dark — halation; no pure black
   canvas; desaturate on dark; elevation by lightness; verify every pair in both
   modes) live in `research/theme-parity.md` and are encoded in the tokens.
   The switching UI is the appearance control (`components.md` §2.15): one
   header button opening a three-option menu — System · Light · Dark — with
   the active choice checked and the System row stating what it resolves to.
   Never a cycling toggle. Persistence of an override (session vs. stored per
   user) is an open decision.
4. Mono means something. The mono face marks code, IDs, timestamps, run labels, and
   numeric table columns — never prose.
5. Density is a setting, not a redesign. Three steps on one axis via
   `[data-density]`: tight (the most rows per screen, for heavy data review),
   normal (the default reading rhythm, no attribute), loose (extra air for touch
   use, presentations, long reading). Two options assume one kind of user; three
   cover the spectrum while staying finite. Every step keeps targets ≥
   `--target-min`.
6. Finite options. Every component is variants × states × sizes — a matrix (§5).
   A new need means a new row, not a snowflake.
7. Customization is server-rendered config. "My view" is a DB row, not client state (§6).
8. Accessibility is structural (§8) — shipped in tokens and defaults, not bolted on.
9. Sections by default, cards by intent. For the day-to-day working screens —
   lists, tables, forms, database and record views — the layout unit is the full-bleed
   section: flush rectangles sharing one hairline separator. Two adjacent cards
   cost three visual elements (edge + gap + edge); two sections cost one line. Cards
   are not forbidden — they earn their place where content is genuinely independent
   and glanceable: a senior-management dashboard, a monitoring/control environment, a
   user-composed widget grid. The test: if the user reads *across* items (comparing,
   scanning), use sections; if each item stands alone at a glance, a card is
   legitimate. The duality with strengths and weaknesses is spelled out in
   `components.md` §2.7.
10. The consequential action stands apart. In any action list — a dropdown menu, a
    view menu, a context menu, a bulk-actions bar — the most critical or
    destructive choice (delete, archive, remove) is never styled like its
    neighbors: it takes the danger color, sits last, and is separated by a
    divider, so the eye finds it instantly and never hits it by accident. The
    full rule lives in `components.md` §2.3.
11. The control decides what Enter means — never the application. In menus,
    lists, and palettes, Enter activates the highlighted item. In a single-line
    field inside a form, Enter submits (native implicit submission — kept, never
    suppressed). In every multi-line text box, Enter makes a new line, always;
    Cmd/Ctrl+Enter is the one universal accelerator for "save or submit from
    anywhere in the form", and the primary button teaches it by showing the ⌘↵
    hint while a text box has focus. Shift+Enter is accepted as a harmless
    newline synonym. In grid editing, Enter starts and commits a cell edit (the
    standard grid grammar) — the same principle applied to a different control.
    Full explanation: `components.md` §2.14; evidence: `research/enter-key.md`.

## 4. Tokens — `tokens.css` is the single source of truth

Never restate values in docs or components; edit `tokens.css`, and only `tokens.css`.
Three tiers; components consume only semantic (tier 2) aliases:

```
tier 1  primitive  →  raw palette / scales    (--clay-400, --neutral-900, --space-4)
tier 2  semantic   →  intent; component-facing (--color-action, --color-surface)
tier 3  component  →  optional per-component hook (--button-bg: var(--color-action))
```

- Theming = re-pointing tier-2 aliases under `[data-theme="light"]` — already in the
  file. A palette family is the same move one level up, selected with
  `[data-palette]`. Three families fill the contract, each with both themes: warm
  (taupe ramp + clay accent, the token-level fallback), cool (gray-blue + azure),
  and mono (pure grayscale + achromatic ink accent — the specimen's opening state).
  A brand skin re-points just the accent under `[data-brand="…"]` (commented
  example). Never edit a component to re-theme.
- The palette contract: every family defines the identical set of named steps —
  14 neutrals (0·25·50·100·200·300·400·500·600·700·800·900·950·1000) and 4 accent
  steps (300·400·500·600). Families map one-to-one; switching families can never
  leave a semantic alias without a matching step. A family missing a step is a bug;
  adding a family means filling the exact contract with new values.
- Contrast is verified, not assumed — by machinery. `enforcement/check_contrast.py`
  resolves every family × theme mapping and enforces WCAG 2.2 AA floors (text
  ≥ 4.5:1, UI ≥ 3:1) plus the dark-mode halation ceilings: body text lives in the
  `#DEDEDE`–`#EBEBEB` band, never `#ffffff`; canvas is never `#000000`
  (`research/theme-parity.md` has the expert record). Semantic hues use different
  contrast-solved steps per theme. The checker runs on every token change.
- The resting hairline `--color-border` is *intentionally* sub-3:1 — a decorative
  divider. Interactive contrast is carried by `--color-focus`, never the resting border.
- Fonts are self-hosted via `@font-face` at integration (Inter for UI, JetBrains Mono
  for data) — never a CDN `<link>`. The stacks degrade gracefully to system faces.
- Icons: one set — Lucide, copied inline as SVG (`stroke="currentColor"`,
  stroke-width 1.5). No icon fonts, no CDN, no second set.

## 5. Component taxonomy — the "options and differences"

Every component is a finite matrix: variants × states × sizes, documented as a table.
Shared state vocabulary: `default · hover · focus-visible · active · disabled · loading ·
selected · error` (not all apply to all). Sizes `sm · md · lg` where relevant. Everything
below is rendered live in `specimen.html`. The full catalog — every component with an
example and explanation, including the full View System — is `components.md`.

| Atom | Variants | Notes |
|---|---|---|
| Button | `primary · secondary · ghost · danger · link` | primary = clay pill, the only one; icon-only variant; loading via `hx-indicator` |
| Input / Textarea | `default · invalid` | native validation; server-rendered error |
| Select | `default · invalid` | native `<select>`; multiselect = chips |
| Checkbox / Radio | `native · drawn` (candidates) | wrapped in `.choice`; mixed state server-rendered (`aria-checked="mixed"`) |
| Switch | `md · sm`; row presentation | immediate effect only — never beside a Save button; checkbox + `role="switch"` (+ native `switch` attr), never `aria-checked` |
| Segmented control | `raised · accent`; counts | candidate; one-of-few values/scopes, 2–5 segments; hidden radios, zero JS |
| Toggle button | `labeled · icon-only` | candidate; `aria-pressed` server-rendered; pressed ≠ color alone |
| Choice chip | — | candidate; many-of-many filter facets; hidden checkbox + pill |
| Option tile | — | candidate; radio-as-card with visible dot; one interactive element per tile |
| Badge | `neutral · success · warning · danger · info · accent` | dot + tinted field |
| Chip (removable) | `default` | filter tokens; `hx-delete` to remove |
| Avatar | `sm · md · lg` | initials fallback |
| Icon | — | inline Lucide SVG, `currentColor` |
| Spinner / Skeleton | `line · block` | paired with `hx-indicator` |

| Molecule | Made of | Key options |
|---|---|---|
| Search field | input + icon | typeahead `hx-trigger="input changed delay:150ms"` |
| Form field | label + control + hint + error | required marker, invalid state |
| Filter row | field + operator + value | AND/OR, add/remove |
| Dropdown menu | button + list | overlay shadow; kbd hints; danger item |
| Alert | accent bar + title + text | `success · warning · danger · info` |
| Tabs | tablist + panels | active from URL/`aria-selected` |
| Card | title + body + actions | surface + hairline |
| KPI tile | label + value + delta + sparkline | mono value; delta up/down |
| Pagination | prev/next + status | `hx-get` + `hx-push-url` |

| Organism | Purpose | Customization surface |
|---|---|---|
| App shell | sidebar + topbar + main | collapsed/expanded; `aria-current` nav; menu-anatomy candidates (label style, casing, icons ×3, active ×3, separators, submenu ×3) in `components.md` §3.2 |
| Data table | the core primitive | density, columns, sort, selection, saved views |
| Table toolbar | search + chips + view controls | column show/hide, saved-view picker |
| Filter builder | stacked filter rows | saved filters, URL state |
| Dashboard grid | KPI tiles + cards | add/remove/resize/reorder; per-user layout |
| Command palette | ⌘K nav + actions + search | §7 |
| Empty state | first-run guidance | teaches, never dead-ends |

Each shipped cell gets: the BEM class, the tokens it consumes, a row in its matrix table,
a live rendering in `specimen.html`, and a Gherkin scenario for any behaviour (§10).

## 6. Customization = server-rendered config (DATAOS)

The product goal is users building their own screens — dashboards, tables, filters,
saved views. On this stack that is *simpler*, not harder: a saved view / filter set /
dashboard layout / density choice is a row in a `views` or `preferences` table,
rendered to HTML and swapped by HTMX. No client store.

Rules:
- Persist user view config server-side (per user, per resource). Render from it.
- Filter/sort/search state goes in the URL via `hx-push-url="true"` — every view is
  bookmarkable and shareable (essential for collaborative team workflows).
- Column show/hide, reorder, density, saved views, dashboard tile layout = config the
  server reads and reflects into the rendered fragment.
- Combine controls with `hx-include`; target specific `#id`s with `hx-target`.
- When the current DOM state itself must be captured (e.g. "save this arrangement"),
  collect it declaratively with domx and post it — never hand-rolled JS.

## 7. The command palette — zero JavaScript

Every best-of-breed professional tool has ⌘K. Here it needs no JS at all: htmx
trigger event-filters are the documented mechanism —

```html
<div hx-get="/palette"
     hx-trigger="keydown[(metaKey||ctrlKey)&&key=='k'] from:body"
     hx-target="#overlay" hx-swap="innerHTML"></div>
```

The panel arrives as a server-rendered fragment (`autofocus` on its input); typeahead is
`hx-trigger="input changed delay:150ms"`; results are grouped fragments, keyboard-
navigable. The palette overlay is the only element that may cast `--shadow-overlay`.

## 8. Accessibility — shipped by default

Non-negotiable, encoded in tokens and component defaults:
- Contrast: body text ≥ 4.5:1, large text & UI ≥ 3:1 — verified per §4.
- Visible focus on every interactive element: `:focus-visible` ring in
  `--color-focus`, width/offset from tokens.
- Full keyboard operability — native elements (`<button>`, `<a>`, `<table>`,
  `<details>`, `<dialog>`) over div soup; correct tab order.
- Target size ≥ `--target-min` (24px) even in tight density.
- Semantic HTML + ARIA only where native falls short (`aria-selected`, `aria-current`,
  `aria-live` for toasts).

## 9. Enforcement — the rules defend themselves

Prose rules drift; machinery doesn't. `enforcement/` carries the design equivalents of
the Honest enforcement stack:

- `enforcement/lint_design.py` — pure scanning functions, I/O only in `main()`.
  Run: `python3 enforcement/lint_design.py` (exit 1 on any violation). Rules:
  R1 no raw hex outside `tokens.css` · R2 no `style=` attributes ·
  R3 no `!important` · R4 no shadow outside `var(--shadow-overlay)`/`none` ·
  R5 no px literals outside `tokens.css` except 0/1/2px ·
  R6 every class selector is BEM · R7 no imperative JS in templates.
- `enforcement/check_contrast.py` — the color-math checker. Resolves every palette
  family in every theme from `tokens.css` and enforces the floors (every
  text-capable pair ≥ 4.5:1 on canvas and surface, on-action ≥ 4.5:1) and the
  dark-mode ceilings (body text never pure white and never brighter than `#EBEBEB`
  effective — the halation band; canvas never pure black). Run:
  `python3 enforcement/check_contrast.py` (exit 1 on any violation).
- `enforcement/design-enforcement.feature` — the same rules as Gherkin scenarios;
  binds to pytest-bdd step definitions at app integration and runs in CI.
- `specimen.html` is the living conformance proof — it renders the entire system and
  must itself pass the lint. If a component isn't in the specimen, it doesn't exist.
- At integration, add the lint as a pre-commit hook next to the app's existing hooks.

## 10. Workflow — how to add or change UI

Honest is Gherkin-first; UI behaviour is behaviour.

1. Token or component? A value change = edit `tokens.css`, run
   `python3 enforcement/check_contrast.py`, and stop. A behaviour/structure
   change = continue.
2. Write the scenario first — `.feature`, `@unit`, plain observable language.
3. Write step defs red, then the Jinja partial + BEM CSS + HTMX/domx attributes to green.
4. Semantic tokens only in component CSS.
5. Document the variant matrix (§5) and add the component to BOTH rendered
   documents: `specimen.html` (pure catalog, no prose) and `whitepaper.html`
   (the same example placed after its explanation, with options, recommendation
   and status). The two evolve in parallel — never change one without the other.
   Shared styles live in `ui.css`, so visual changes are single-sourced; the
   parallel rule applies to markup and to content.
6. Run `python3 enforcement/lint_design.py` — must exit clean.
7. Validate contrast & focus (§8) for anything colour-touching.
8. Branch + PR; a human reviews and merges (human gate).

## 11. Forbidden — design edition

| Forbidden | Honest equivalent |
|---|---|
| Raw hex / px / size inside a component | A token (`var(--…)`) — lint R1/R5 |
| A component reading a primitive token | Read a semantic alias |
| Tailwind / utility classes / CSS-in-JS | BEM + CSS custom properties — lint R6 |
| React / Vue / Alpine / any client store | Jinja partial + HTMX + server state |
| `addEventListener` / `querySelector` / `fetch` / `<script>` | HTMX attributes; domx for state capture — lint R7 |
| Hand-written JS for shortcuts, tabs, toggles | `hx-trigger` event filters, `<details>`, `aria-*` |
| `style=` attributes, `!important` | Proper BEM rule + tokens — lint R2/R3 |
| Drop shadow in app chrome | Surface ladder + 1px hairline — lint R4 |
| Accent colour as decoration | Accent = primary action + active only |
| A second stylesheet for light/dark | Re-pointed `[data-theme]` aliases |
| A one-off "just this screen" style | Add a variant to the matrix, or a token |
| Client-side saved views / filters | Server-side config row, URL state |
| CDN fonts or icon fonts | Self-hosted `@font-face`; inline Lucide SVG |

## 12. Definition of done

A UI change is done when: it uses only semantic tokens; it has a Gherkin scenario for any
behaviour; it renders in BOTH `specimen.html` and `whitepaper.html` (the
dual-document rule — the specimen shows it, the white paper explains it, and the
two change together in the same commit); the lint exits clean; it works in dark
and light from one ramp; contrast and visible focus pass; it needs zero
JavaScript; and its options are captured in the §5 matrix. If any fails, it's
not done.

**Document map — what each file is and who it is for.**

- `whitepaper.html` — the flagship, for every reader including non-technical
  ones: one chapter per topic, each with the explanation in plain language, the
  options, the live example right after the words that describe it, the
  recommendation, a decision-status badge, and that chapter's sources.
- `specimen.html` — the pure rendered catalog, no prose: the same examples as
  the white paper with titles and option labels only. A visual reference.
- `AGENTS.md` + `enforcement/` — the agent rulebook: rules and machinery only;
  each rule points to its white-paper chapter for the full story.
- `components.md` + `tokens.css` — the technical reference for developers:
  specs, option matrices, code idioms, and the single source of truth for
  values.
- `README.md` + `index.md` — orientation for any reader; the index groups
  files by audience.
- `research/` — the workbench: named sources and investigations live here
  while in progress, then graduate into white-paper chapters. Never the place
  a reader is sent to.
