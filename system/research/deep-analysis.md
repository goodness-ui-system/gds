# Deep Analysis — The Ideas a Best-of-Breed UI System Stands On

> Research briefing. Sources — the products, systems, and methodologies studied —
> are cited inline where claims are made and listed at the end.

> The expert briefing behind this design system. Read once to understand *why* the
> rules in `AGENTS.md` are what they are. `AGENTS.md` is the operating manual; this
> is the reasoning and the references.
>
> Scope: a single master UI system, built from scratch, for professional, data-dense
> B2B applications built on the Honest stack (FastAPI + Jinja2 + HTMX + domx +
> CSS custom properties, DOM-as-state, no client framework). Applications adopt the
> system whole; product identity is a brand skin, never a fork.

---

## 0. The problem this kills

Multiple applications, hand-styled screen by screen, drift apart. Feedback fixes one
place and not the others. "Consistent look and feel" becomes impossible because nothing
is a *system* — every screen is a snowflake. The cure is not more taste applied more often.
The cure is to encode the decisions once, as data and named parts, so that "the
button" is one definition with a finite set of options, used everywhere, changed in one
place. Everything below serves that single goal.

---

## Part 1 — The enduring ideas (proven over time)

These are the concepts that have survived a decade-plus of industry churn because each
one durably solves a real problem. They are the load-bearing walls.

### 1.1 Atomic Design — a vocabulary for composition
Brad Frost, 2013 (blog) → 2016 (book). Decompose every UI into a five-stage hierarchy:
atoms (button, input, label, badge) → molecules (a labelled search field) →
organisms (a table toolbar, a header) → templates (page skeletons) → pages
(real content). It survives because it forces "build systems, not pages" and gives
everyone one shared word for each part. It maps cleanly onto a component library — and,
here, onto Jinja partials/macros.

### 1.2 Design Tokens — decisions stored as data
Coined at Salesforce (Jina Anne & Jon Levine, ~2014) for the Lightning Design System.
A token is a named, platform-agnostic key–value pair — `color-action = #d97757` — that
stores a *design decision* decoupled from where it's used. Style Dictionary (Danny
Banks / Amazon, open-sourced ~2016) built them; the W3C Design Tokens Community Group
(2019) standardised a portable format. Tokens survive because they turn "rebrand the app"
from a find-and-replace nightmare into a single data edit.

The discipline that makes tokens work is tiering:

| Tier | Purpose | Example |
|---|---|---|
| Primitive / global | Raw values. The palette. Named by what they *are*. | `--clay-400: #d97757` |
| Semantic / alias | Intent. Named by what they're *for*. Components use only these. | `--color-action: var(--clay-400)` |
| Component | Optional. A component's own hook, pointing at a semantic. | `--button-bg: var(--color-action)` |

Components never touch raw values — only semantic aliases. This one rule is what lets
a single system skin many apps and flip light/dark (see 1.6).

### 1.3 The reference systems — and the one thing each proved
The lessons are borrowed, not the look. Each of these earned its place:

| System | Signature contribution taken |
|---|---|
| IBM Carbon | The gold standard for data-dense enterprise UI: rigorous DataTable, grid, deep accessibility. The closest cousin to this system. |
| Salesforce Lightning | Birthplace of design tokens and enterprise/CRM pattern discipline. |
| Google Material | Codified elevation, motion, and the 8dp grid — a full physics of UI. |
| Apple HIG | Clarity / deference / depth; rigorous targets & typography. |
| Atlassian | Practical token adoption across many products; strong empty states. |
| Shopify Polaris | Best-in-class UX writing and exhaustive component-state docs. |
| Adobe Spectrum | Token-driven multi-scale theming (density as a first-class axis). |
| Ant Design | The richest enterprise tables / forms / filters out of the box. |
| USWDS | Proof a system can be an accessibility & plain-language instrument. |

### 1.4 The 8-point grid — a finite, memorable spatial system
Space, size, and layout snap to multiples of 8px, with a 4px sub-grid for fine work.
Popularised by Material; adopted everywhere because 8 divides cleanly across screen
densities and replaces an infinity of arbitrary paddings with one small, memorable scale
(4, 8, 12, 16, 24, 32, 48…). Fewer choices → more consistency.

### 1.5 Type ramps & the base-16 rule
A modular scale derives sizes from a base and a ratio, giving harmonious steps instead
of random pixel values. The base-16 approach keeps the root at the browser default
(16px) and expresses type and space in `rem`, so user zoom and accessibility settings
scale the whole UI proportionally. Harmony *and* accessibility from one decision.

### 1.6 Theming by indirection — the mechanism that skins many apps
Multi-brand and light/dark are not separate stylesheets. A theme is just a different
mapping of semantic → primitive. Because components reference only semantic aliases,
you re-point the aliases under a selector (`:root`, `[data-theme="light"]`,
`[data-brand="acme"]`) and every component re-skins with zero component edits. This is
the technical core of "design once, use everywhere," and CSS custom properties do it
natively — no build step required.

### 1.7 Variant taxonomy — the "options and differences," made finite
A mature component is an explicit, finite option set: variants (primary /
secondary / ghost / danger), states (default, hover, focus, active, disabled,
loading, selected, error), and sizes (sm / md / lg). Polaris, Carbon, and Ant each
document this matrix exhaustively — every cell gets a spec and a token. This is precisely
the system's goal: *define each element and the differences between its options so
they're easy to use.* A finite matrix prevents one-off snowflakes and makes components
predictable and testable.

### 1.8 Accessibility as a structural constraint, not a review
WCAG 2.2 (W3C Recommendation, Oct 2023) is encoded into tokens and defaults, not
checked at the end: text contrast ≥ 4.5:1, large text / UI components ≥ 3:1,
always-visible focus, full keyboard operability, target size ≥ 24×24px. When
the tokens ship contrast-safe pairs and components ship focus rings and min hit-areas by
default, compliance is structural.

### 1.9 CSS methodology for a no-framework, pure-custom-properties stack
The stack has no Tailwind and no CSS-in-JS. Three proven methods combine:
- BEM (`.block__element--modifier`; Yandex, ~2010) — flat, low-specificity,
  self-documenting class names. The Honest architecture already mandates it.
- ITCSS (Harry Roberts) — orders the stylesheet by reach (Settings → Tools → Generic
  → Elements → Objects → Components → Utilities) to prevent specificity wars.
- CUBE CSS (Andy Bell, 2020) — Composition, Utility, Block, Exception; embraces the
  cascade and pairs naturally with tokens + BEM.

Together: ITCSS orders the file, tokens hold the values, BEM names the parts, CUBE
reconciles with the cascade.

---

## Part 2 — The aesthetic: the AI agent-harness visual language

The direction: build from scratch, inspired by the current AI agent-harness apps —
Claude (Code / Cowork / claude.ai), Conductor, Omnigent, and the wider class
(Cursor, Warp, Raycast, Linear, Vercel/Geist, Zed). Studied directly, they share a
coherent visual DNA.

### 2.1 The shared DNA
1. Dark is canonical for the work surface; light is derived by inverting the same
   ramp — not a second palette. (Claude is the interesting inversion: a *warm cream*
   light canvas with dark reserved for code/model cards.)
2. Depth from a surface-colour ladder + 1px hairline borders, not drop shadows.
   Linear, Raycast, and Zed reject shadows in chrome outright. Vercel allows only
   whisper-soft layered shadows plus an inset hairline ring.
3. One restrained accent carries the brand voice — Anthropic clay/terracotta, Linear
   lavender, Vercel blue — reserved for the primary action and the active/selected state.
4. Semantic colours are desaturated so they survive on a low-chroma neutral field.
5. Sans for UI, mono for meaning — code, IDs, timestamps, run labels, numeric table
   cells. Mono is a *functional signal*, not decoration.
6. ~8px grid, tight radii (6–10px), pills for CTAs only. Negative letter-tracking on
   display sizes; weights capped around 600.
7. Agent-tool motifs: run/task cards, per-agent panes, status dots, diff views,
   streaming output, keyboard-first affordances, monospace labels. Motion is highly
   restrained — streaming text is the primary animation.

### 2.2 The from-scratch direction (professional, data-dense)
- System-first theming: the OS preference leads, a stored user choice overrides,
  and dark and light are exact equals re-pointed from the same ramp — a deliberate
  departure from the dark-canonical habit of the studied tools (see
  `theme-parity.md`).
- A slightly warm neutral ramp (a touch of Anthropic's taupe) — approachable and
  distinctive against the sea of cool blue-grays, without Claude's full cream commitment.
  A 10-step functional ramp: 1–3 backgrounds/surfaces, 4–6 borders, 7–8 hover/active,
  9–10 text.
- Surface layering: canvas → raised panel (one step up) → sunken well (one step down);
  depth from the ladder + 1px hairlines. No drop shadows in app chrome. Exactly one
  soft shadow token, reserved for floating overlays (command palette, menus, popovers).
- A single warm accent — terracotta/clay (`~#d97757`) — reads distinctive and
  non-generic against ubiquitous SaaS blue. Primary action + active/selected only.
- Type pairing: a humanist/grotesque sans for UI + a mono for code, IDs, timestamps,
  and numeric columns. A serif display face is optional if an editorial voice is wanted
  (Claude's signature move); default is sans display with tight tracking.
- Density: compact-but-breathable — 4px base grid, 8px rhythm. Dense tables breathe
  via line-height, hairline row dividers, and mono numerals rather than extra padding.
  Density is a token-switchable axis (`[data-density]`), à la Spectrum.
- Radius: 6–8px default, 4px for chips/inputs, pill for the primary CTA and status
  badges.

Concrete token values live in `tokens.css` — the single source of truth — with every
text/UI pair contrast-verified programmatically in both themes (WCAG 2.2 AA).

---

## Part 3 — The synthesis: this system inside the Honest medium

The single most important realisation: on the Honest stack, a design system is not a
component library you import — it is three native layers. Nothing here fights the
sixteen principles; it expresses them.

| Design-system concept | Honest-native form |
|---|---|
| Design tokens (tiered) | CSS custom properties in `:root`, primitive → semantic → component |
| Theming / multi-brand / dark mode | Re-pointed aliases under `[data-theme]` / `[data-brand]` — pure CSS |
| Atomic components | Jinja partials & macros (atoms → organisms); fragment partials (`_row.html`) are molecules/organisms |
| Variants × states × sizes | BEM modifiers + macro parameters; states via `:hover` / `:focus-visible` / `[aria-selected]` |
| Interaction / behaviour | HTMX attributes (`hx-get/post/put/delete`, `hx-target`, `hx-swap`, `hx-trigger`, `hx-push-url`, `hx-include`) — never hand-written JS |
| Loading / async states | `hx-indicator` + a CSS class — no JS spinners wired by hand |
| Validation states | Native browser (`type=email`, `required`, `min`) per P11 + server-rendered error partials |

### 3.1 The customization insight — DATAOS *is* the feature
The headline product goal — users build their own dashboards, tables, filters, and
screens — is where the Honest stack stops being a constraint and becomes the advantage.

In a React app, "my saved view" is a client-side state problem (stores, effects, local
persistence). Under DOM-as-State (P06) it is the opposite and far simpler: a user's
custom view is server-side state — a row in a `views` / `preferences` table — rendered to
HTML and swapped in by HTMX. Column show/hide, saved filters, dashboard tile layout,
density preference: all of it is *server-rendered configuration*, not a client widget.
The filter/search example already in `items/page.html` (`hx-get` + `hx-push-url="true"`)
is the seed of the entire pattern — bookmarkable, shareable, no client store. The design
system's job is to give these configurable primitives a consistent skin and a finite set
of options.

### 3.2 The command palette (Cmd-K) — zero JavaScript after all
Every best-of-breed tool in this class has a command palette. Initially assessed as
needing one sliver of JS for the key binding — verification against the htmx
documentation proved otherwise: trigger event filters cover it declaratively
(`hx-trigger="keydown[(metaKey||ctrlKey)&&key=='k'] from:body"`). Contents are
server-rendered fragments fetched with `hx-get`; typeahead is `hx-trigger="input changed
delay:150ms"`. The system therefore ships with zero JavaScript — no exceptions.
Where DOM state must be *collected or persisted* (e.g. capturing a user's current view
arrangement), domx — the DATAOS companion library (collect / apply / observe /
persist via a declarative manifest, as an htmx extension) — is the sanctioned tool,
never hand-written JS.

---

## Part 4 — The five primitives, best-of-breed → Honest

Five primitives matter most: tables, menus, dashboards, filters, search. For
each: the proven pattern, the finite options, and the Honest expression.

Tables / data grids. The core primitive of data-dense professional work. Options:
density mode (comfortable/compact), sticky header (+ sticky first column), per-column
sort / resize / reorder / show-hide, row selection (checkbox + shift-range), inline or
overflow-menu row actions, pagination vs. server-side "load more," and saved views
(named column/sort/filter presets per user). Honest form: native `<table>`, server-sorted
and server-filtered, rows as `_row.html` fragments, sort/paginate via `hx-get` +
`hx-push-url`, saved views persisted server-side. Virtualisation is deliberately *not*
needed — the server sends only the current page. (Reference bar: AG Grid, Linear, Airtable.)

Menus / navigation. Collapsible left sidebar for deep hierarchies, topbar for
shallow apps, plus a command palette (Cmd-K) for navigation *and* actions
(the Sublime → VS Code → Superhuman/Linear lineage). Options: collapsed/expanded, nested
accordion sections, active-state indication. Honest form: server-rendered nav, active
state from the request path, `hx-boost` for instant transitions.

Dashboards. A widget/card grid users can add, remove, resize, and rearrange —
"build your own dashboard" (Datadog/Grafana/Retool). Options: KPI tiles (big number +
delta + sparkline) up top, richer cards below; per-user persisted layout; designed
empty states that teach first-run rather than dead-end. Honest form: layout is a
server-side config row; each widget is a fragment fetched with `hx-get hx-trigger="load"`.

Filters. Escalating sophistication: filter bar (quick chips/dropdowns) → filter
builder (stacked field / operator / value rows, AND/OR) → faceted (counts per
value). Options: saved named filters, URL-encoded state so any filtered view is
bookmarkable and shareable — essential for collaborative audit trails. Honest form:
exactly the `items` search pattern, generalised: inputs drive `hx-get` with
`hx-push-url="true"` and `hx-include` to combine controls.

Search. Instant/typeahead (debounced), scoped (per entity type), and unified
command-palette search (nav + records + actions in one Cmd-K surface). Options:
grouped results, highlighted matches, keyboard nav, recent/suggested on empty query.
Honest form: `hx-trigger="input changed delay:150ms"` → server-rendered results fragment.

---

## Sources

Aesthetic (agent-harness study):
- Anthropic brand / Claude tokens — https://geist.co/work/anthropic ; https://github.com/anthropics/skills/blob/main/skills/brand-guidelines/SKILL.md
- Claude design notes — https://github.com/voltagent/awesome-design-md/blob/main/design-md/claude/DESIGN.md
- Conductor — https://www.conductor.build/
- Omnigent — https://omnigent.ai/ ; https://www.databricks.com/blog/introducing-omnigent-meta-harness-combine-control-and-share-your-agents
- Linear tokens — https://github.com/voltagent/awesome-design-md/blob/main/design-md/linear.app/DESIGN.md
- Vercel/Geist — https://vercel.com/geist/colors
- Raycast — https://github.com/VoltAgent/awesome-design-md/blob/main/design-md/raycast/DESIGN.md
- Warp themes — https://www.warp.dev/blog/how-we-designed-themes-for-the-terminal-a-peek-into-our-process

Methodology & patterns:
- Atomic Design — https://atomicdesign.bradfrost.com/chapter-2/
- Design Tokens history — https://www.designsystemscollective.com/the-incomplete-history-of-design-tokens-61581c573e5d ; https://www.w3.org/community/design-tokens/
- Style Dictionary — https://didoo.medium.com/how-to-manage-your-design-tokens-with-style-dictionary-98c795b938aa
- WCAG 2.2 target size — https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- CUBE CSS — https://cube.fyi/
- Command palettes — https://blog.superhuman.com/how-to-build-a-remarkable-command-palette/ ; https://retool.com/blog/designing-the-command-palette
