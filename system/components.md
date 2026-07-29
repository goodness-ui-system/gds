# Components Catalog

The complete list of components in the UI Design System. One entry per component:
what it is, its finite options, an example in the system's idiom (Jinja + BEM + HTMX),
and notes on the Honest mapping. `specimen.html` renders the visual reference;
`AGENTS.md` §5 holds the variant-matrix vocabulary; this file is the catalog.

Status: a catalog of candidates, not a verdict. Wherever several ways of doing the
same thing exist (form presentation styles, figure sizes, table-editing models),
every credible option is documented and rendered side by side in the specimen, so
the final system can be chosen by looking at real examples rather than imagining
them. Entries marked as options are on display pending selection. Explanations aim
at plain language: any term of art is defined where it first appears.

How to read an entry
- *Options* are the finite set — variants × states × sizes. Anything not listed does
  not exist; a new need adds a row here, never a one-off style.
- Shared state vocabulary: `default · hover · focus-visible · active · disabled ·
  loading · selected · error` (only the applicable ones are noted).
- Every example consumes semantic tokens only and declares behaviour with `hx-*`
  attributes. Zero JavaScript.
- View configuration (filters, sorts, visible fields…) is always server-side state:
  a row in a `views` table, reflected in the URL, rendered to HTML (DATAOS).
- Every part explained: where an entry embodies a decision or offers an option,
  each part is named with the reason it exists and the reason it sits where it
  sits. §4.3 (field visibility panel) is the model.

---

## 1 · Atoms

### 1.1 Button
The single action element. Options: `primary` (clay pill — the only pill, one per
screen region) · `secondary` · `ghost` · `danger` · `link`; icon-only; states default /
hover / focus-visible / disabled / loading.
```html
<button class="button button--primary" hx-post="/reports" hx-target="#list">
  Run analysis</button>
<button class="button button--secondary" disabled>Export</button>
```
Loading is declarative: `hx-indicator` toggles a `.spinner` inside the button.

### 1.2 Input / Textarea
Single- and multi-line text entry. Options: `default · invalid`; validation is
declared (`type`, `required`, `min`, `pattern`) — browser + server enforce (P11).
```html
<input class="input" type="email" name="email" required placeholder="you@company.com">
<input class="input input--invalid" type="text" aria-describedby="err-name">
```

### 1.3 Select
Native `<select>`, restyled by tokens. Options: `default · invalid`. Multi-select
is not a variant — it's the Chip-bar molecule fed by repeated params.

### 1.4 Checkbox / Radio
Two drawing options are on display (whitepaper, Selection controls chapter;
decision pending). Option A: native inputs, `accent-color: var(--color-action)`.
Option B: custom-drawn (`.checkbox--drawn` / `.radio--drawn`, `appearance: none`,
state drawn from semantic tokens — identical in every browser, styleable disabled
and mixed states). Either way, always wrapped in a `.choice` label for a full-size
click target ≥ `--target-min`.
```html
<label class="choice"><input class="checkbox checkbox--drawn" type="checkbox"
  name="notify" checked> Notify on change</label>
```
The mixed state (a parent checkbox over a partly-selected set) is server-rendered as
`class="checkbox--mixed"` — a visual state only. The platform's mixed flag is
script-only, and `aria-checked` is forbidden on a native checkbox (ARIA in HTML;
the native state wins and some readers double-announce), so where the mixed reading
must reach assistive technology the control is a server-rendered select-all button,
not a tri-state checkbox. Checkbox = deferred form data, submitted later. A checkbox
group is the many-of-many control; a lone checkbox is the opt-in control. Submission
contract: an unchecked checkbox submits nothing at all — the server treats an absent
name as false, always; no hidden-input companions.

### 1.5 Switch
An on/off control whose effect applies immediately (`.switch`, a checkbox carrying
`role="switch"` — the pattern the major component vendors converged on: current
screen readers announce a true switch, and the failure mode is a correctly-stated
checkbox — plus HTML's emerging native `switch` attribute for browsers that know
it; the checked state stays native, never restated with `aria-checked`).
Options: `md · sm`; label trailing, or the
`.switch-row` settings-list presentation (title + description left, switch right).
Never inside a form that ends in a Save button — that job belongs to Checkbox.
The flip is one request with honest feedback: never move the thumb before the
server confirms. State words inside the track are rejected (localization, and the
state-vs-action ambiguity); a separate localizable state word beside the control
is a permitted variant where research shows confusion.
```html
<label class="switch"><input class="switch__track" type="checkbox" switch role="switch"
  name="visible" value="status" checked hx-post="/views/current/fields"
  hx-target="#table"> Auto-refresh</label>
```

### 1.6 Badge
Status at a glance: dot + label, hairline border, tinted field. Options: `neutral ·
success · warning · danger · info · accent`.
```html
<span class="badge badge--danger"><span class="badge__dot"></span> Overdue</span>
```

### 1.7 Chip (removable)
An applied token — an active filter, a selected value. Options: with/without key
prefix; removable.
```html
<span class="chip"><span class="chip__key">priority:</span> critical
  <button class="chip__remove" hx-get="/items?tier=" hx-target="#list"
          hx-push-url="true" aria-label="Remove filter">✕</button></span>
```

### 1.8 Avatar
Identity mark, initials fallback. Options: `sm · md · lg`.

### 1.9 Icon
One set only: Lucide, inlined SVG, `stroke="currentColor"`, stroke-width 1.5.
No icon fonts, no CDN, no second set.

### 1.10 Spinner / Skeleton
Loading affordances. Spinner pairs with `hx-indicator`; Skeleton (`line · block`)
fills a fragment target while `hx-trigger="load"` content arrives.

### 1.11 Kbd
Keyboard hint in mono (`⌘K`, `↵`) inside menus and the palette. Never decorative.

### 1.12 Segmented control (candidate)
One-of-few, every option visible, as adjacent buttons — a radio group in button
clothing (`.segmented`: visually hidden radio inputs + styled labels, zero JS).
For picking a value or a data scope (interval, filter facet), never for switching
views — that is Tabs. Options: raised segment (neutral) or tinted accent
(`.segmented--accent`); optional mono counts (`.segmented__count`); 2–5 segments.
Keyboard note: arrow keys check radios as they move, so a request fires per arrow
press — permitted only when the swap is an inline, non-context-changing update
(a tile re-render, never navigation or focus loss); anything heavier gets an
explicit Apply button per WCAG 3.2.2.
```html
<div class="segmented">
  <input class="segmented__input" type="radio" name="interval" id="i-d" checked
         hx-get="/dash?interval=day" hx-target="#tiles" hx-push-url="true">
  <label class="segmented__btn" for="i-d">Day</label>
  <input class="segmented__input" type="radio" name="interval" id="i-w"
         hx-get="/dash?interval=week" hx-target="#tiles" hx-push-url="true">
  <label class="segmented__btn" for="i-w">Week</label>
</div>
```

### 1.13 Toggle button (candidate)
A button that stays pressed (`.toggle-btn`, state = `aria-pressed`, server-rendered).
For repeated-action states: watch/unwatch, formatting marks. Options: labeled;
icon-only (`.toggle-btn--icon`, always with `aria-label`). The pressed state must
survive grayscale — border + fill change together, never color alone. The label
and icon never change with the state (stable name, state carries the answer);
a name-flipping pair (start/stop) is a different control and takes no
`aria-pressed` — never both at once.

### 1.14 Choice chip (candidate)
Many-of-many as compact pills (`.chip-choice`: hidden checkbox + pill face with a
check mark when selected). The horizontal, space-tight form of the checkbox group —
filter facets above a table. Distinct from Chip (1.7), which shows an applied value
and removes; the choice chip toggles membership in place.

### 1.15 Option tile (candidate)
A radio dressed as a small card (`.option-tile`) for one-of-few choices that need a
description line — a plan, a sync mode, a placement. The tile keeps a visible radio
dot: without it, a bordered card does not read as a single choice in a group. One
interactive element per tile — never a link or button nested inside the label.

---

### 1.16 Digits in columns (rule)
Any component presenting digits in columns — numeric table cells, count
columns, meter and ratio number pairs, stacked deltas, pagination status —
either uses the mono face (tabular by construction) or declares
`font-variant-numeric: tabular-nums`. Single display numbers (a KPI headline,
a ratio percent) keep proportional figures: the rule triggers on columns, not
on numbers. Font contract, the palette contract's idea applied to type: a
sans face qualifies for the system only if it ships a `tnum` feature with
uniform-width alternates; `enforcement/check_figures.py` opens the shipped
binaries and verifies — a face missing the step is a bug, not a preference.

### 1.17 Clearing the group (rule)
Deselecting K active options costs K clicks; the empty state must cost one.
The device depends on the group's role:

- Filter group (empty means "everything"): a leading exclusive `All` option —
  radio-like inside the checkbox group. Selecting All deselects every
  specific; selecting a specific turns All off; deselecting the last specific
  snaps All back on, so the group is never blank and the empty set is always
  labeled.
- Any group with 2+ active options: a clear action (`.toggle-clear`) at the
  group's end — the universal escape hatch.
- Form group (empty means "none chosen"): the exclusive "None of the above"
  option where none is a legitimate answer; the clear action otherwise.
  Never a fake All — a filter word has no place in data entry.
- Long lists (table selection, field pickers): the tri-state select-all
  parent (1.4) and the hide-all arithmetic (§4.3).

Refused: All as an ordinary member that can sit active beside specifics —
"All + Documents" is unanswerable. Exclusivity is server logic: every press
is one `hx-get` carrying the next parameter set; the server renders the next
true state. Full record: the Selection Controls research note.

## 2 · Molecules

### 2.1 Form field
Label + control + hint + error, stacked. Options: required marker; `invalid` state
renders a server fragment error under the control.
```html
<div class="field">
  <label class="field__label field__label--required" for="f-name">Account name</label>
  <input class="input" id="f-name" name="name" type="text" required>
  <span class="field__hint">Legal entity name, as registered.</span>
</div>
```

### 2.2 Search field
Input + leading icon; instant results server-side.
```html
<span class="search-field">
  <span class="search-field__icon">…svg…</span>
  <input class="input search-field__input" type="search" name="q"
         hx-get="/accounts" hx-trigger="input changed delay:200ms"
         hx-target="#list" hx-push-url="true" hx-include="[name='sort']">
</span>
```

### 2.3 Dropdown menu
Button-opened action list; the fragment arrives from the server open.
Options: items, `--danger` item, dividers, kbd hints. Carries `--shadow-overlay`.

The consequential-action rule (applies to every action list in the system —
dropdown menus, the view menu, context menus, bulk-actions bars, palette action
groups): the most critical or destructive choice is never visually equal to its
neighbors. Three markers, always together: it renders in the danger color
(`--color-danger`), it sits last in the list, and a divider separates it from the
routine actions. The eye locates it instantly when it is wanted and cannot slide
into it by accident when it is not. One consequential action per list — if two
items are colored, neither stands out; when a list genuinely carries several
destructive choices, they share the final divider-separated group. Color alone
never carries the risk: destructive actions still confirm (`hx-confirm` or a
Dialog) before executing.
```html
<div class="menu" role="menu">
  <button class="menu__item" role="menuitem">Duplicate <span class="menu__kbd">⌘D</span></button>
  <hr class="menu__divider">
  <button class="menu__item menu__item--danger" hx-delete="/views/{{ view.id }}"
          hx-confirm="Delete this view?" role="menuitem">Delete view</button>
</div>
```

### 2.4 Alert
Inline callout: 2px accent bar + title + text. Options: `success · warning ·
danger · info`.

### 2.5 Toast
Transient confirmation in an `aria-live="polite"` region the server swaps into.
Same variants as Alert; auto-dismiss via a CSS animation, not JS.

### 2.6 Tabs
In-page section switch; the active tab comes from the URL, not client state.
```html
<div role="tablist" class="tabs">
  <a class="tabs__tab" role="tab" aria-selected="true" href="?tab=overview">Overview</a>
  <a class="tabs__tab" role="tab" aria-selected="false" href="?tab=history">History</a>
</div>
```

### 2.7 Card — by intent, not by default
Surface + hairline container: title, body, actions. Cards are not forbidden — they
are scoped. They were the most overused container of the past design-system decade
(systems built by people who never shipped an app), but the fix is knowing the
duality, not banning the part.

| | Card | Section (3.0) |
|---|---|---|
| Strengths | Self-contained and glanceable; rearrangeable and user-composable; handles heterogeneous content; reads well from across the room | Denser; calmer; one shared separator per pair; preserves vertical scanning and cross-item comparison |
| Weaknesses | Spatially expensive (edge + gap + edge); busier for the eye; breaks scanning across items; invites decoration | Less separable — items read as one flow; not rearrangeable as units |
| Use for | Senior-management / executive dashboards, KPI walls, monitoring & control environments, user-composed widget grids | Day-to-day operational screens: data tables, lists, forms, record details, database views |

The test in one line: if the user reads across items — comparing rows, scanning a
column — use Sections; if each item stands alone at a glance, a Card is
legitimate. An executive dashboard is card territory; three levels deep in the
day-to-day app, it isn't.

### 2.8 KPI tile
Label + mono value + delta (`--up/--down`) + sparkline SVG. Dashboard atom.

Figure-size options (all three rendered in the specimen, pending selection):
- A · Display — the number at 2xl. Works like signage: readable before the eye
  focuses, from across a room. Costs space, and every big number claims to be
  the headline — past five or six tiles, none is. For the few numbers a team
  steers by.
- B · Mid — the number at heading size (lg). Still leads the tile but stops
  dominating the screen; more tiles fit per row; delta and sparkline gain
  relative weight. For working dashboards someone sits in front of.
- C · Stat list — all numbers at body size, one metric per row, values
  right-aligned in mono so digits line up. Nothing shouts; the form is for
  comparing many metrics, not glancing at one. Scales to a dozen rows.

One size per row, never mixed — a mixed row reads as a hierarchy nobody intended.

### 2.9 Pagination
Prev/next + mono status (`1–50 of 248`); `hx-get` + `hx-push-url` so every page is
a bookmarkable URL. Server-side "load more" is the infinite-scroll variant.
One of three scroll models — see 3.12 for the full menu and the recommendation.

### 2.10 Breadcrumbs
Path context for deep hierarchies: `Workspaces / Templates / Reports`. Links all the
way up; current item is plain text with `aria-current="page"`.

### 2.11 Dialog
Native `<dialog>` for confirmations and small focused tasks, served as a fragment.
For row-level confirmation prefer `hx-confirm`; Dialog is for anything richer.
Carries `--shadow-overlay`.

### 2.12 Chip-bar
The row of currently-applied filter Chips above a table, each removable, with a
"Clear all" ghost button when 2+ are active. The visible summary of filter state.

### 2.13 Ratio tile & meter
The "20 of 200 reviewed · 10%" figure — a number against a total. Options:
percent-led tile (share is the story), count-led tile (the quantity is the
story), delta variant (the movement is the story), meter row (the list form),
and segmented meter (the total splits into states). The meter is the native
`<progress>` element — declarative, zero JS — themed by tokens; the unfilled
track is a lighter step of the same hue so the bar reads as one object, and
length carries the value, never color. The big value is sans semibold
(display-size numbers use proportional figures; mono is for the `20 / 200`
count pair and for columns). Segmented meters use a one-hue opacity ladder
with 2px surface gaps between parts and a legend with counts; widths come from
a finite step scale rendered server-side.

Adjacency rules — the multiple-tiles-side-by-side case: one variant per row,
never mixed; one quiet hue across every tile; identical number formats
(integer percents, mono count pairs); meters always span the full tile width
so lengths compare at a glance. A semantic color enters a meter only when a
threshold genuinely means something (a breach, an overdue state) and then
always with a word or icon, per the compound-signal rule. Past four or five
metrics, tiles stop scanning — switch to stacked meter rows, where the label
column does the work.

Figure-size options mirror the KPI tile's (§2.8): display percent (glance-first),
mid percent (heading size; bar and number share the weight), small percent
(body size; the bar becomes the primary signal — the halfway house before meter
rows). All three are rendered in the specimen, pending selection.

### 2.14 Keyboard conventions — what Enter means
Enter is the most overloaded key in modern software: in one product it sends, in
another it makes a new line, in a third it activates a menu item — and users
carry each habit into the next application, where it misfires. The rule here
removes the guessing by making the control decide, never the application. Every
part of the convention, and why:

- Menus, lists, palettes: Enter activates the highlighted item; Esc closes.
  The oldest and least disputed meaning — a choice surface has exactly one
  sensible thing for Enter to do.
- Single-line field in a form: Enter submits. This is implicit submission,
  built into the web platform itself — it is why Enter works in every search
  and login box — and it is kept, never suppressed. It requires the form to
  have a real submit button.
- Multi-line text box: Enter makes a new line, always. A text box that accepts
  paragraphs is a writing surface, and these applications hold notes and
  descriptions, not chat messages. The two failure modes are not symmetric: a
  surprise submit can fire a half-written record (bad, sometimes irreversible),
  while a newline that did not submit costs one extra keystroke. The safe
  meaning wins.
- Cmd/Ctrl+Enter: the one universal accelerator meaning "save or submit from
  anywhere in the form", including from inside a text box. One combination,
  identical in every screen of every application on the system.
- The interface teaches the accelerator in place: while a multi-line text box
  has focus, the form's primary button shows the ⌘↵ hint beside its label —
  the convention is learned exactly where it is needed, not from a manual.
- Shift+Enter is accepted as a newline synonym. Users arriving from chat
  applications press it out of habit; it produces the same newline, so the
  habit is harmless and is not fought.
- Grid editing: Enter starts and commits a cell edit, Esc cancels, Tab commits
  and advances (§3.6, option E). The same principle — a grid cell is a
  different control, so Enter means something different there, and it means it
  consistently.
- The only place Enter-to-send would be correct is a true chat surface, where
  the chat convention is the learned rule. No such surface exists in the
  system today; if one is ever added, it follows chat convention and nothing
  else does.

Evidence and the history of the confusion: research/enter-key.md. Live
examples: the specimen's keyboard-conventions section.

### 2.15 Appearance control — System · Light · Dark
The visible half of system-first theming (principle 3): one button in the
header opens a menu with exactly three choices. Every part, and why:

- Three options, not two. System is a first-class choice, always one click
  away — never buried behind "advanced". The site opens in System.
- The menu, not a cycle. A single icon that cycles modes must answer "what
  mode am I in?" and "what happens if I click?" with one symbol; it cannot.
  The menu is what-you-see-is-what-you-get: all options visible, the active
  one checked. The cycling toggle is rejected.
- The resolves-to line. The System row states what it currently means —
  "Match device — currently Dark" — so nobody picks System blind. Rendered
  with zero script: two prewritten spans, one shown by a
  `prefers-color-scheme` media query.
- Trigger options: sun/moon (reports the current appearance — sun when
  light, moon when dark; the icon reports, the menu chooses) or the neutral
  contrast circle ◐. Sun/moon is the recommended default.
- Honest-stack mapping: the menu is a server-rendered overlay; choosing posts
  to the preferences endpoint and the server re-renders with `data-theme`
  set (or absent, for System) — no flash of the wrong theme, no client
  state.

Open decision: override persistence. Session-scoped (device stays the source
of truth; every visit greets in System) vs. stored per user (a decision made
once holds). May legitimately differ between public sites and signed-in
applications. Evidence and named prior art: research/theme-control.md.

---

## 3 · Organisms
### 3.0 Section & separator — the default layout unit
The default layout unit for working screens: full-bleed rectangular sections that
touch, with a single 1px hairline shared between neighbors. Two cards side by side
cost the eye three elements — edge, gap, edge; two sections cost one. Denser,
calmer, and how the pane-and-divider layouts of today's leading professional tools. The Card (2.7) remains the right tool where content is glanceable
and independent — the duality table there says when to pick which.
Options: stacked (horizontal separators) · side-by-side panes (vertical
separators) · optional section header row (title + actions) · optional `--well`
section (sunken content like code or logs).
```html
<div class="section-stack">
  <section class="section-stack__section">
    <h3 class="section-stack__title">Coverage</h3> …content…
  </section>
  <section class="section-stack__section">…content…</section>   <!-- one shared line -->
</div>
```
```css
.section-stack__section + .section-stack__section { border-top: 1px solid var(--color-border); }
.pane-row__pane + .pane-row__pane            { border-left: 1px solid var(--color-border); }
```
The adjacent-sibling selector *is* the principle: the separator belongs to the pair,
not to either section. No margins between sections; rhythm comes from internal
padding (`--space-4/5`), not gaps.

**The air rule (R11).** Everywhere outside a fused section-stack, the opposite
law applies: nothing begins flush against the end of the block before it. Any
element that opens a new block after another block — a paragraph after a demo
frame, a label after a table, a panel after a paragraph — carries vertical air
above it: base rhythm `var(--space-4)`, and `var(--space-6)` for a label that
opens a group. The only sanctioned tight pairs are a caption with the object
it captions (label, heading, legend) and a component's own internal anatomy.
The rule is enforced by rendering, not by trust: `enforcement/check_rhythm.mjs`
measures every adjacent pair on every page and fails on any flush pair.

### 3.1 App shell
Sidebar + topbar + main. Options: sidebar expanded/collapsed (a `preferences`
row); active item via `aria-current="page"` from the request path; `hx-boost` for
instant transitions.

### 3.2 Sidebar nav
Anatomy options on display (whitepaper, Navigation chapter; decision pending):

- Group label: uppercase eyebrow (`.sidenav__section`) · sentence case
  (`.sidenav__section--sentence`). Static text, never a link.
- Item casing: title case · sentence case — one is chosen per application,
  never mixed.
- Icons: none · small (`.sidenav__icon`, 1rem — matches the text) · large
  (`.sidenav--icons-lg`, 1.25rem — leads the row). All-or-none per menu;
  Lucide only; the word is always present.
- Active item: tinted pill (default) · solid ink pill (`.sidenav--active-solid`)
  · left accent bar (`.sidenav--active-bar`). Never color alone.
- Separators: titled group when the group has a name; bare hairline
  (`.sidenav__divider`) when it does not; never both between the same neighbors.
- Submenus: always-open with connector line (`.sidenav__item--sub`) ·
  collapsible native `<details>` group (`.sidenav__group` +
  `.sidenav__group-summary`, chevron right→down, zero JS; server renders
  frequent groups `open`) · second column (`.sidenav--secondary`) when a parent
  has dozens of children — the drill-in. One level of nesting; a parent either
  navigates or toggles, never both.
- Items may carry mono counts (`.sidenav__count`).

Not a card: the sidebar is a flat rail sitting directly on the page background,
separated from the content by a single vertical hairline — the sections-not-cards
rule turned sideways. No box, no rounded border, no fill behind the rail; the only
filled shape is the current item's selection pill. Floating menus that open from
the rail are overlays and keep their edge and shadow (that is a requirement of
floating above other content, not a card by choice).

Nav density rule: navigation and menu rows use `--menu-pad-y`, a tighter rhythm
than data rows (`--row-pad-y`). A nav item is targeted, not read — menu-heavy
business applications burn sidebar space fast, and the reference tools run their
sidebars at roughly 32–36px of row pitch. The floor is `--target-min` (24px);
tight density tightens one step further. Applies to sidebar items, dropdown
and view menus, panel rows, and palette items alike.


Utility controls — a finite option set. Real deployments grow shell
conveniences; without a catalog entry they live as per-application forks,
exactly what the system exists to prevent. An application adopts any subset
of `hide/peek · move-side · collapse-all/expand-all · resize` and invents
nothing beyond it:

- Hide / pin — three states, two of them stored. Pinned (default): the rail
  occupies its column. Click: the rail disappears entirely, content takes the
  full width, the stored preference becomes hidden. While hidden, the screen's
  left edge peeks the rail back as a temporary overlay (pure CSS, `:hover` on
  a fixed edge zone) — leaving lets it slide away, and peeking never changes
  the stored state. Clicking the same control while peeked re-pins the rail.
  The peek is the recovery path: the button is never unreachable. Only the
  two clicks touch the server — one preference flip each.
- Move side — the whole rail, with its second column when open, mirrors to
  the other screen edge.
- Collapse all / expand all — two stateless chevrons acting on every nav
  group at once (the native `<details>` groups, acted on server-side).
- Resize — a drag handle on the rail edge; double-click resets the default
  width. The one control that must capture live DOM state (the dragged
  width): domx territory, posting the final value — never hand-written JS.

Placement: one controls row directly under the brand slot — icon-only
buttons at muted color, targets ≥ `--target-min`, every button with an
`aria-label` and tooltip. Icon-only is permitted here: a small fixed set of
universal symbols used once, not repeated per row (consistent with the
row-actions repetition rule, §3.4). Collapse-all / expand-all sit at the
row's end so they align vertically with the per-group chevrons they command
— the lever sits over the thing it moves. Keyboard: every control tabbable;
the resize handle is a button (arrow keys nudge by one spacing step, Home
resets) so the pointer drag is never the sole path. Persistence: a
`preferences` row rendered server-side — the shell arrives with
`data-menu="hidden"` / `data-menu-side="right"` / the width already applied,
never flashing into place. Client storage is the named anti-pattern: it is
client state, and it desynchronizes across devices. A fifth control enters
by the standard workflow (AGENTS.md §11), never as a private feature.

### 3.3 Dashboard grid
User-composed widget grid. Layout is a `views` row (`{"tiles":[{"w":…}]}`); each
tile is a fragment loaded with `hx-get hx-trigger="load"`; add/remove/rearrange
posts the new layout. Ships with a designed Empty state.

### 3.4 Data table
The core primitive. Options: density (token switch) · sticky header · sortable
columns · selectable rows · numeric mono columns · row actions (ghost ⋯ menu) ·
footer with Pagination. Server-sorted, server-filtered; rows are `_row.html`
fragments.

Row delimitation — how the eye crosses a wide table. Hairlines
(`border-bottom` per row) and the hover lane are the resting default on every
table. The quiet stripe (`.data-table--zebra`) is the sanctioned variant for
wide, flat, dense grids: even rows take `--color-row-alt`, a half-step
between canvas and surface derived from the ground aliases (defined once,
re-solves in every theme and family), decorative only, never meaning. The
background ladder is strict — stripe < hover < selected — enforced by
exclusion in the selector. Wide grids additionally pin the identity column
(`.data-table--pin-first`, sticky first column). Whitespace-only
(`.data-table--airy`) is a narrow-table nicety. Grouped tables always skip
the stripe: group headers already band the table, and stripe parity restarts
at each break. Full record and citations: the Table Rows research note.
```html
<th><a class="data-table__sort data-table__sort--active"
       href="?sort=name&dir=desc" hx-get="/accounts?sort=name&dir=desc"
       hx-target="#table" hx-push-url="true">Account ▲</a></th>
```

Row actions — visible icons vs. the overflow menu. Every row carries actions;
the question is how many deserve to be visible. Three findings drive the rule:

- Repetition kills affordance. An icon repeated on every row stops reading as
  a button and becomes texture — the eye tunes out repeated decoration, so
  forty delete icons are less findable than one menu, not more.
- Icons alone are misread. Beyond a handful of universal symbols (search,
  print, play), readers guess at bare icons; each extra icon column adds
  guessing, not speed.
- Danger proximity. A destructive icon on every row puts an irreversible
  action one accidental click from everything on screen.

Against that, the overflow menu (⋯) has one cost: everything inside is
invisible until clicked, so an action people need constantly should not live
there. The reconciliation is a frequency budget, and it is the rule:

- Default: ⋯ only — one per row, always the last column, same menu everywhere.
  Inside it the consequential-action rule applies (danger color, last position,
  divider above, one per menu).
- Exception, argued per case: at most one — rarely two — visible actions on
  the row, and only when all three tests pass: used constantly · harmless if
  misclicked · a symbol everyone reads the same way.
- Never: a destructive action as a bare row icon. Delete lives inside the ⋯.
- Optional quiet variant: the ⋯ hidden until the row is hovered or holds
  keyboard focus (`:hover` / `:focus-within` — CSS only). Reveal on focus is
  mandatory, so keyboard users are never locked out.

All four states are rendered in the specimen (options A–C plus the rejected
anti-pattern). Evidence and sources: research/row-actions.md.

### 3.5 Table toolbar
The table's control strip and the view's cockpit. Left to right: Search field ·
Chip-bar (applied filters) · the five view controls · primary action. Everything
mutates the same URL-backed view state, and each control wears its active count
at rest (`Filter · 2`), so the view's configuration is readable without opening
anything; a control with nothing active shows its bare name.

The elements, and what a click opens:

- View button — first in the row, the one control whose resting label
  changes: `View ▾` before any view exists, the view's name once one is
  selected (the control states which view, as every neighbor states its
  count). Click opens the view panel (4.1–4.2): one popover, two panes,
  one shared hairline.
- Hide fields → the field visibility panel (4.3): one switch per field,
  show-all/hide-all first (the thirty-fields-three-wanted arithmetic).
- Filter → the filter builder (4.4): condition rows, add-condition,
  add-group.
- Group → the group menu: one grouping field + direction. Group headers band
  the table — which is why grouped tables skip the zebra stripe (3.4).
- Sort → the ordered sort list: several sorts stacked, direction per field.
- Row height → the compact-to-roomy control: the three density steps
  (tight · normal · loose) applied per view (§4.7) — one crowded review view
  packs rows while a presentation view breathes; stored like every other
  part of the view.

Deliberately absent: a color button. Painting rows from the toolbar puts
meaning into decoration; meaning belongs to the semantic colors — badges,
marks, and a rule the view declares in its description line (see the
brand-vs-meaning chapter). Order rule: the five controls keep this order in
every application; a sixth control enters by the standard workflow
(AGENTS.md §11), never ad hoc.

### 3.6 Table editing vs. form editing — the options catalog
Where should a value change: in the table cell itself, or in the record form the
row opens? Every option is on display in the specimen, pending selection; a real
screen usually combines two or three. Evidence and sources:
research/table-inline-editing.md.

- A · Read-only table + form editing — the safe default. The table finds and
  compares; the form changes. Right whenever fields carry help text, interact
  with each other, or need review before landing.
- B · Edit mode with a draft and a save bar — an Edit button flips the grid into
  a spreadsheet-like mode; edited cells are tinted and held as a draft (nothing
  written yet); a bar counts unsaved changes and offers one Save and one Cancel
  for the whole batch. The server checks the batch together and returns per-cell
  errors. Right for repetitive corrections across many rows.
- C · Per-cell instant commit — one field saved the moment it changes, confirmed
  by a toast with Undo. Reserved for single pickers (status, owner): nothing to
  validate against other fields, one click to reverse. Never typed text/numbers.
- D · Editable-field whitelist — inline rights granted per column, not per
  table. Low-risk fields earn the pencil affordance; calculated fields,
  identifiers, and anything governance depends on stay read-only in the grid.
- E · Keyboard grammar (shared by B, C, D) — Enter or F2 edits the focused
  cell, Esc cancels and restores, Tab commits and advances, arrows travel the
  grid. One convention, learned from the spreadsheet.

Mapping: edited cells post to a server-side pending changeset; the save bar is a
fragment re-rendered with the current count; Save submits the changeset — the
same object the review/diff workflow already displays, which is how option B
feeds an approval (maker-checker) flow unchanged. Open decisions: whether C
exists before an undo toast ships; whether records under approval rules always
force B's draft mode.

### 3.7 Record form — presentation styles and workflows, two axes
The screen behind a clicked row. The industry habit — a card per field or per
field-group — is rejected; both layouts are built from full-bleed sections
sharing hairlines. The evidence (research/record-forms.md) splits by task:
entry wants top labels and a single column; reading wants a left label column
to scan. So the system ships presentation styles and, separately, workflows — a style is the UI of the fields; a workflow is the process around them; they compose freely.

Style 1 — stacked form. For creating a record, or an explicit edit mode
when fields are interdependent. Options: top-aligned regular-weight labels
(never floating or placeholder labels), strict single column with one
exception (short conceptual pairs — city/postal, date parts — share a line),
hairline sections with small headers, sticky footer with Cancel left of a
verb-named primary (Save changes), no reset button, explicit save, validation
on blur plus a submit summary that repeats field messages.
```html
<form class="section-stack record-form" hx-put="/accounts/42" hx-target="#detail">
  <section class="section-stack__section"> …fields, single column… </section>
  <section class="section-stack__section form-actions">
    <button class="button button--ghost" type="button">Cancel</button>
    <button class="button button--primary" type="submit">Save changes</button>
  </section>
</form>
```

Style 2 — property sheet. The read-first default: identity header (title +
mono key facts), then label:value rows sharing hairlines — fixed muted label
column left, value right, numbers in mono. Whole row is the edit target; hover
reveals the affordance. Commit rules: pickers (status, owner, enums, dates)
save instantly on selection via `hx-put`; free text opens in place with
adjacent confirm/cancel; interdependent edits escalate to Style 1 in a
Dialog. No save footer — nothing is ever pending. Record-level actions live in
the header menu under the consequential-action rule.
```html
<div class="prop" hx-get="/accounts/42/edit/owner" hx-target="this" hx-swap="outerHTML">
  <span class="prop__label">Owner</span>
  <span class="prop__value"><span class="avatar avatar--sm">KL</span> K. Lane</span>
  <span class="prop__edit-hint">✎</span>
</div>
```
The two are a system: the sheet is where records live; the form is where
records are born and where complex edits go.

Field presentation styles — a separate axis from workflow. Layouts A and B are
two of six graphical treatments of the same fields, all rendered in the
specimen pending selection: stacked top-label (A), read-first property sheet
(B), the ledger form (the form as a table — label cells and input cells
sharing grid hairlines, borderless inputs filling the cell), left-label inputs
(the property sheet's editable twin — boxed inputs beside a fixed label
column), two-column dense (top labels in twin columns — for review-heavy
contexts, since entry evidence favors a single column), and the print style
(no input boxes; caption labels over values sitting on a baseline rule —
quiet, document-like, at home in the mono family). Presentation style and
workflow compose freely: any style can appear in any placement and any
workflow.

Workflow candidates, rendered in their own specimen section pending selection:
the document hybrid (editable title and prose body over a property strip — for
records whose heart is text); the wizard (sequential creation with a
visible step path, for long or consequential records); grid entry
(the table as the form — bulk cell editing, tab advances); the
conversational form (one question at a time — intake and AI-assisted creation
where a described record arrives pre-filled for review); the placement axis
(any form or sheet opens as side panel, dialog, or full page — one component,
three containers); the settings pattern (summary rows drilling into small edit
forms, for rarely-touched configuration); the review/diff form (old value
struck, proposed value beside it, approve or reject — maker-checker
workflows); and the user-composed form (the layout itself is a saved
configuration row: fields toggled, ordered, and sectioned per team or user —
the saved-view idea applied to forms).

---

### 3.8 Detail panel
Row → side panel: click a row, `hx-get` the record fragment into a right-hand
panel (`.detail-panel`, surface + hairline, no shadow). Deep-linkable
(`hx-push-url="/accounts/42"`). The alternative to leaving the table.

### 3.9 Bulk-actions bar
Appears when rows are selected: mono count + actions (Export, Assign, Archive).
Server renders it into the table fragment when `selected` params are present.

### 3.10 Command palette
⌘K — opened by a pure HTMX trigger, contents server-rendered, grouped, keyboard-
navigable. The only element (with menus/dialogs) casting `--shadow-overlay`.
```html
<div hx-get="/palette" hx-target="#overlay"
     hx-trigger="keydown[(metaKey||ctrlKey)&&key=='k'] from:body"></div>
```

### 3.11 Empty state
First-run teacher: icon, title, one sentence, one primary action. Every list,
table, and dashboard has one designed — never a bare "No results."

### 3.12 Table scroll — how the table meets the bottom of the screen
Three models, all in the catalog; the choice is by task, not by taste.

- **Pages** — fixed row count, prev/next footer. The only model with a stable
  address (bookmarkable, back-button-safe) and bounded server work. Right when
  position in the set is part of the task; wrong as the working-grid default.
- **Scrolling page** — the document grows; rows arrive as the scroll nears the
  end (`hx-trigger="revealed"` on a sentinel row, degrading to a "more" link).
  **Rule: nothing may sit at the bottom of the screen.** The bottom edge
  belongs to the last visible row; selected count, bulk actions, and summary
  all move above the table, and the toolbar states the true total.
- **Contained scroll (recommended)** — the grid's box fills the viewport
  height and rows scroll inside it; sticky column header at the box top;
  toolbar above and bulk bar + summary below never move; no next button.
  One demand: the shell hands the grid its height exactly — a page that
  scrolls and a grid that scrolls is the double-scrollbar trap.

## 4 · The View System

Best-of-breed reference: the leading spreadsheet-database platforms, studied from
their live UIs and documentation. What makes them the benchmark: *every* aspect of a table's presentation (visible
fields, filters, grouping, sort, row height, color) is stored per named view,
views are first-class shareable objects with ownership levels, and filter state can
even travel in a URL. That model maps one-to-one onto DATAOS: a view is a row —
`views(id, resource, owner_id, name, kind, is_personal, config JSONB)` — the URL
carries the live overrides, and the server renders the result. Below, each
component of the family; together they land in the Table toolbar and view sidebar.

### 4.1 View panel — pane one: every view
The View button (first in the toolbar, 3.5) opens one popover of two panes
sharing one vertical hairline — the pane law applied to a menu. Pane one is
every view: create new, find-a-view search, typed icons per view kind, the
named-view list with the current view highlighted.
Options: view kinds (`table` now; `dashboard`, others later) · find-a-view
(typeahead over view names) · create new · personal section vs shared section.
The list scrolls internally past about six views; on narrow screens the two
panes stack.
```html
<nav class="view-switcher">
  <button class="view-switcher__new" hx-post="/views?resource=accounts">+ Create new…</button>
  <input class="input" type="search" placeholder="Find a view"
         hx-get="/views?resource=accounts" hx-trigger="input changed delay:150ms"
         hx-target="#view-list">
  <div id="view-list">
    <a class="view-switcher__item" aria-current="page"
       href="/accounts?view=high-priority">High-priority, active</a>
    <a class="view-switcher__item" href="/accounts?view=enterprise-only">Enterprise only</a>
  </div>
</nav>
```

### 4.2 View panel — pane two: this view
Per-view management, as the second pane of the same popover: rename, edit
description, duplicate, copy another view's configuration, export CSV, delete
(last, danger color, divider above — the consequential-action rule). The pane
is titled with the current view's name so its target is never ambiguous, and
it acts on the current view only — acting on another view means switching to
it first; no per-row menus in pane one. Plus the ownership levels
worth adopting outright: *collaborative* (team-editable), *personal* (only the
owner edits its config), *locked* (config frozen — audit-friendly).
Options: the seven actions above · ownership level · view description.
All are one-line handlers: duplicate = copy the `config` JSON; export = the same
query rendered as CSV instead of HTML.

### 4.3 Field visibility panel
The panel that decides which columns a table shows. Every part, and why it is
there:

- Find-a-field search (top). Tables can carry dozens of possible columns;
  scrolling a long switch list is slower than typing three letters. The search
  filters the list as it is typed.
- Show all / Hide all (directly under the search, above the list). Bulk
  actions for the two extreme starting points. Show all answers "what else is
  there?" in one click. Hide all serves the opposite and more common power
  move: when only three of thirty fields matter, it is far faster to hide
  everything and switch the three wanted ones back on than to turn off
  twenty-seven switches one by one. Placed above the list, not in a footer,
  because they act on the list that follows — the reader meets the lever
  before the thing it moves. A hairline under the pair separates bulk actions
  from per-field rows.
- One switch per field. A switch, not a checkbox, because the change applies
  immediately — the table re-renders on toggle; there is no Apply step.
- Drag handle (⋮⋮, row end). Column order is part of the same mental model as
  column visibility, so reordering lives in the same panel.
- Field-type icon (production version). Tells fields with similar names apart
  at a glance.

Options: per-field on/off · order · show-all/hide-all.
```html
<div class="field-panel">
  <input class="input" type="search" placeholder="Find a field"
         hx-get="/views/{{ view.id }}/fields" hx-trigger="input changed delay:150ms"
         hx-target="#field-list">
  <div class="field-panel__bulk">
    <button class="field-panel__bulk-btn" type="button"
            hx-post="/views/{{ view.id }}/fields/show-all" hx-target="#table">Show all</button>
    <button class="field-panel__bulk-btn" type="button"
            hx-post="/views/{{ view.id }}/fields/hide-all" hx-target="#table">Hide all</button>
  </div>
  <label class="field-panel__row">
    <input class="control-switch__box" type="checkbox" name="visible" value="status"
           checked hx-post="/views/{{ view.id }}/fields" hx-target="#table">
    <span class="field-panel__icon">…type icon…</span> Status
  </label>
</div>
```
The server re-renders the table with the new column set; the choice persists in
`config.fields`. Hide all keeps at least one column visible (the primary field)
so the table never renders empty.

### 4.4 Filter builder
The heart of the system. Stacked condition rows
(field / operator / value), conjunction dropdown (`and`/`or`), and condition
groups — a bracketed sub-list with its own conjunction, nestable one level.
Operators are typed per field: text (contains, is, is empty…), select (is any
of, has none of…), number/date (=, <, >, range), checkbox (is checked).
Options: add/remove condition · add group · per-field operator sets ·
conjunctions · copy from another view · saved with the view.
```html
<div class="filter-row">
  <select class="select" name="f0.field"><option>Priority</option>…</select>
  <select class="select" name="f0.op"><option>has none of</option>…</select>
  <select class="select" name="f0.value" multiple>…</select>
  <button class="button button--ghost" hx-delete="/views/{{ view.id }}/filters/0"
          hx-target="#table" aria-label="Remove condition">✕</button>
</div>
```
Layout rule: each condition renders as one segmented control — field, operator,
value, and row actions share hairline borders (the section-separator principle at
control scale), with radius only at the ends, and rows stack at the tightest
spacing step. Ten conditions cost barely more height than two; the list stays
scannable as it grows. Every change fires `hx-get` with `hx-push-url="true"` — filters live in the URL
(best-in-class tools ship this as URL filter params: `filterContains_Field=value`,
`filterConjunction=or`; the operator-in-param idea carries over directly) and persist to
`config.filters` when saved.

The AI row. The newest benchmark UIs put a natural-language box above the builder —
"Describe what you want to see." For AI-era apps this is the differentiator worth
copying: the sentence goes to the server, an LLM translates it into the same typed
filter JSON, and the builder renders *populated* — inspectable, correctable,
honest. One `hx-post="/views/{id}/filters/from-text"`; no client magic.

### 4.5 Group-by panel
Pick a field → the table renders grouped: a group header row (value + mono count +
collapse via `<details>`), rows beneath, optional per-group summary. Options:
group field (groupable types only) · sub-group (one level) · collapsed state
per user · copy from view.

### 4.6 Sort panel
Multi-sort: ordered sort rows rendered as the same compact segmented control as
filter conditions, direction labels typed per field
(A→Z, 1→9, checked→unchecked), drag priority, and the *Automatically sort records*
toggle. Options: up to N sort fields · per-type direction · auto-sort on/off —
when off, order becomes manual: a `position` column the user drags, which is
DATAOS-native (the order *is* data).

### 4.7 Row-height control
Four heights — short to extra-tall — plus wrap headers. Here it is token-native:
Short/Comfortable map to `[data-density]`; Tall adds line-clamped multi-line
cells; wrap headers is a table modifier. Options: `short · comfortable ·
tall` · wrap headers on/off. Persisted per view.

### 4.8 Color rules
Record coloring, adapted to the system's restraint: conditional row edge
markers (a 2px left bar in a semantic color) driven by the same condition rows
as the Filter builder — "Score < 50 → danger". Never full-row fills; the accent
rule (§3 of AGENTS.md) holds. Options: ordered rules (first match wins) ·
semantic colors only · per view.

### 4.9 Summary row
Sticky table footer with per-column aggregates: count, sum, avg, min/max, %
checked — computed in SQL, rendered mono. Options: aggregate per column ·
none. Best-in-class grids ship this per-column; it is cheap
(one query) and high-value for dense numeric screens.

### 4.10 Shareable view URLs
Not a widget — a guarantee the whole family upholds: the URL always encodes view
+ live overrides (`/accounts?view=high-priority&filterContains_name=cloud&sort=score`).
Copy the address bar and a colleague sees exactly your screen (their permissions
permitting). The benchmark platforms document this as a feature; here it falls out of
`hx-push-url` discipline.

---

## 5 · App branding

The identity kit every application decides once at creation (whitepaper, App
branding chapter; options on display, decision pending). Not the system's
branding — the application's.

### 5.1 Brand slot
The mark in the top-left of the rail: a small square beside the application
name, optional product-area line under it, closed by the rail's own hairline
(`.brand-slot`, `.brandmark`). Mark options: ink (`.brandmark` — theme text on
theme canvas, self-inverting) · accent (`.brandmark--accent`). A drawn logo,
when one exists, replaces the letter in the same slot.

### 5.2 The two-grounds test
Every mark ships verified on both grounds — one ink on dark, one ink on light.
The letter-mark passes by construction (its colors are semantic tokens); a
drawn replacement must pass the same check before shipping.

### 5.3 Favicon
Default: first letter of the brand name on a rounded square. One vector icon
file carrying both renderings (it follows the device's dark/light preference),
plus fixed-size fallbacks: 16 · 32 · 48 (tabs, taskbars) · 180 (touch icon)
· 192/512 (web-app manifest). The letter must stay readable at 16px — the
reason the default is a letter, not a word. Self-hosted, like every asset.

**Rule — the favicon follows the system, never the app.** The favicon lives
in the browser tab, and the tab is painted by the operating system's theme,
not the application's. An application switched to dark on a light desktop
still sits in a light tab bar — an icon keyed to the in-app theme would
vanish against the chrome it actually lives in. The vector icon keys its two
renderings to the system preference alone (`prefers-color-scheme` inside the
SVG); the application's own theme switch must never touch it. Binding the
favicon to the in-app theme is a defect.

### 5.4 Avatar
The 512px square as the application's identity on external platforms, shipped
in both grounds (ink and inverse); which one is uploaded where stays a human
decision — the kit guarantees both exist and match.

## 6 · Gaps found & suggestions

Studying the benchmark tools surfaced elements the system did not yet name — added above:
Detail panel (3.8), Bulk-actions bar (3.9), Breadcrumbs (2.10), Dialog (2.11),
Toast (2.5), Chip-bar (2.12), and the whole §4 family including Color rules,
Summary row, and view ownership levels.

Worth adding next, in rough priority order:

1. Inline cell editing — click a cell, it swaps to an input, blur/⏎ saves
   (`hx-put` on the cell, fragment back). The spreadsheet-database core gesture; fits fragments
   perfectly. Needs a careful finite spec (which field types, validation display).
2. Undo toast — destructive actions answer with a Toast carrying "Undo"
   (`hx-post` a compensating action within a window). Cheaper than confirm-
   dialogs everywhere and kinder than `hx-confirm`.
3. View sections & favorites — the benchmark groups views into sections with
   favorites pinned on top; becomes valuable past ~10 views per resource.
4. Default view per user — `preferences.default_view[resource]`; the resource
   URL without `?view=` redirects to it.
5. Watch / subscribe to a view — "notify me when records enter this view";
   pairs naturally with saved filters for collaborative review workflows.
6. Further view kinds — kanban (group-by rendered as columns), calendar
   (date-field views), and list are the view kinds most relevant to B2B
   workflows; each is just another renderer over the same `views` row.
7. Keyboard-shortcut overlay — a `?`-triggered cheat-sheet dialog listing all
   `hx-trigger` bindings; keyboard-first tools owe users this map.
8. CSV import — the reverse of View menu → export; column-mapping UI on a
   staged upload.

Each of these enters the system the standard way (AGENTS.md §11): scenario first,
matrix row here, rendering in the specimen, lint clean.

Recorded from the first production adoption audit (accepted as candidates,
not yet argued in full):

- A wordmark variant for the brand slot (§5.1): a type-only brand — a live-text
  wordmark in a display face used nowhere else — occupying the slot, closed by
  the same hairline. The wordmark face is a brand asset (exempt from the UI
  face rule) but its inks must still be the semantic text/canvas pair, so the
  two-grounds test passes by construction.
- An orphan-token lint: every token defined in `tokens.css` must be consumed
  by `ui.css` or a component file, or carry an explicit `reserved:` comment.
  Exit 1 on any orphan — the audit found a dead token consumed by nothing for
  two years while the documentation still described it as rendering.
- A density-control spec (§2.16): the user-facing control for application-wide
  density — a twin of the appearance control (§2.15), three labeled options,
  the active one checked, stored per user, no System row.
- A casing lint for navigation: §3.2 rules one casing per application; a
  pure-function classifier over rendered nav labels (title case vs sentence
  case, fail on mixture) moves the rule from prose to machinery.
