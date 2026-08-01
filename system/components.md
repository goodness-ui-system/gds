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
Status at a glance: label, hairline border, tinted field. Options: `neutral ·
success · warning · danger · info · accent`.
```html
<span class="badge badge--danger">Overdue</span>
```
No dot. The label is the accessible signal (never color alone — the word does
that job), the tinted text and border are the color layer, and a dot beside a
static word is a third coding carrying nothing — in a twenty-row status
column it is twenty circles meaning nothing. The dot (`badge__dot`) survives
as one reserved variant: liveness — a state happening right now ("recording",
"running") — which the static word cannot say.

State pairs — a progress vocabulary, not a severity scale. Where a column
carries two states of one piece of work ("to review" and "reviewed"), give
the pair two independent cues rather than one, so it survives grayscale,
printing, and colour blindness: hue and field, never hue alone.

- The settled state takes the fill. A terminal good state is `success` — a
  completed review is a success, which is what the colour means. Where colour
  is unwanted, `.badge--solid` gives the same settled reading in neutral.
- The open state recedes: `.badge--quiet`, outline only, muted. It is not a
  warning and not an error — it is work outstanding, and it is usually the
  majority. Marking the majority produces a wall of badges, the badge-dot
  mistake at larger size; the mark belongs on the exception.
- Reserve the meaning colours for what they mean. `warning` is for overdue,
  `danger` for failed — never for "not started", or the two states that
  matter later have no colours left. Design the whole scale when the second
  state appears, not the pair.

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
icon-only (`.toggle-btn--icon`, always with `aria-label`).

The lens toggle — a named use. An orthogonal record flag (a favorite, a
watched item) worn as one earned icon beside the scopes: left side of the
toolbar, after the scope group. A lens composes rather than partitions — it
combines with any scope, filter, and sort — so it is never a member of a
scope row (a favorite can belong to any type; adding it breaks the row's
one-facet grammar), never only inside the filter builder (a daily flip
cannot cost a panel-open), and not only a saved view (a view swaps the whole
configuration; the lens narrows the current one). Pressed state tinted;
count at rest permitted (the star wearing the favorites count in the current
scope); state URL-reflected like every part of the view. A personal saved
view may bake the same flag in — the same server state, worn two ways.

Favorites are the fully specified use of the lens — see 3.13.

The pressed state must
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

### 1.18 Every control clears itself (rule)
A control that can be set carries its own way to unset it, positioned so its
scope needs no explanation:

- Search field — an X inside the box (`.search-field__clear`), present only
  when there is something to clear. Pure CSS on `:not(:placeholder-shown)`,
  so it appears the instant a character is typed with no round trip; the
  platform's own search-cancel button is suppressed, since it ships in some
  engines and not others and would otherwise sit beside this one. Honest
  mapping: the X is a link or `hx-get` to the same list with the query
  parameter dropped — the request the server already understands.
- Chip — its own remove (1.7). Scope group — its leading All (1.17).
  Filter panel — clears its own conditions (4.4). Favourites lens — turns
  itself off (3.13). Bulk selection — its Clear in the bulk bar (3.9).

A single global reset that reaches into all of them is a control whose scope
cannot be seen: placed after the favourites star it appears to clear
favourites too, and a reader who has to guess will not press it. Where a
global reset genuinely exists it names its scope ("Reset view", "Clear all
filters"), sits with the controls it clears rather than beside ones it does
not, and never becomes the only way to clear something that could clear
itself.

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
One row, two jobs, two named contracts — distinguished by label grammar,
never by a visual fork. The active tab always comes from the URL, not client
state, and every tab is a real link with the current one marked
(`aria-current="page"`) — the tab-role widget belongs to client-side swaps
this system does not ship (the accessibility record's navigation-styled-as-
tabs guidance; citations in the Tabs research note).

- Scope tabs — subsets of one collection ("All · In review · Reviewed").
  All first, with the exclusive-All arithmetic (1.17); counts ride the
  labels (`.tabs__count`) so the row doubles as a status summary; a switch
  changes only the rows — toolbar, columns, sort, selection survive. Few,
  stable, near-exhaustive subsets; a dozen volatile ones is a saved-view
  problem (§4), not a tab row.

  Count formatting — one numeric reading per tab. The count is mono,
  tabular (a re-render must not shift the labels beside it), one type step
  down, and one step quieter than its label — muted even on the active tab,
  because the label carries the emphasis and a count competing with it makes
  the row a scoreboard. No filled counter pill: a tinted chip is
  notification grammar, and this row already has its baseline. Zero renders
  as `0`, never hidden — a missing number reads as unknown, not as none.
  Large counts cap (`999+`) so the row never reflows. And no second number:
  a count-plus-percent pair per tab triples the row's numeric load and
  states twice what one figure already says, since every share is derivable
  from the All total. Where completion is the story, the percentage belongs
  to a ratio tile or meter (2.13) beside or above the table — one place,
  one reading, and the meter shows progress at a glance in a way a digit
  in a tab label cannot.
- Section tabs — panels of one record ("Score · Files · Due diligence").
  Noun labels naming different content of one parent; no All; counts only
  where a section is a countable collection; the section is in the URL, so
  deep links land and the back button walks tab history.

Docking (`.tab-dock`). A scope row belongs to the table it filters, so it
attaches to it: the rail runs the full width and becomes the table's top
edge, the table loses its top radius and pulls up one pixel to share that
line, and the active tab's accent interrupts the rail rather than hanging
under nothing. A tab row with no rail is the floating-tabs defect — the
active underline reads as a stray dash and the other tabs attach to
nothing. Spacing is asymmetric by rule: air above toward the toolbar, none
below, so proximity alone says which object the row belongs to. The dock
also separates two scope rows that would otherwise compete — toolbar pills
above and a docked rail below are different kinds of object, where two
stacked pill rows each beginning with "All" read as two versions of one
control.

Boundary rules: one row never mixes jobs; nesting in one order only (a scope
row may sit inside a section, never the reverse); the segmented control
(1.12) re-renders the same panel with a different parameter, tabs change
which thing is on screen; steps with an order are a workflow (3.7), never
tabs. Across an application the two jobs coexist freely — a list page
scopes, a record page sections — under two conditions: one solution per
page type (every list page scopes the same way, every record page sections
the same way — never the same kind of page solving the same problem two
ways), and when both rows share a page they never sit adjacent: section
tabs on the page's top boundary, the scope row down inside its section
above the list, content between them, so a reader always knows which level
a click switches.
```html
<nav class="tabs" aria-label="List scopes">
  <a class="tabs__tab" aria-current="page" href="?scope=all">All <span class="tabs__count">248</span></a>
  <a class="tabs__tab" href="?scope=review">In review <span class="tabs__count">34</span></a>
</nav>
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

### 2.15 Display control — appearance and density behind one door
Every setting about *how the application looks* opens from one button in the
header, beside the account. Not one button per setting: appearance and
density are both per-person comfort choices — set once, then forgotten — and
a permanent slot in the chrome for each spends scarce header room on
decisions almost nobody revisits, while a reader thinking "I want this
bigger" has to guess which of several small icons owns that. One door,
labelled Display, holding two named groups separated by a divider.

It lives in the app header, never in a table toolbar. A toolbar configures
its table; this configures the reader's experience of every table.

**Appearance group — System · Light · Dark.** The visible half of
system-first theming (principle 3):

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

**Density group — tight · normal · loose.** The three steps of the one
density axis (whitepaper ch. 6), the active one checked. No System row:
the platform publishes no density preference to read.

**Density is per-user, not per-view.** Merging the control settles a scope
question the system had left open. Density set inside a table's toolbar
would be a property of *that table* — saved with the view, inherited by
whoever opens it. Density set here is a property of *the reader* — it
follows that person across every table in the application and belongs to
nobody else. The system takes the second reading: stored with the account,
server-rendered, and it does **not** travel inside a saved view. A view
carries what the data looks like — columns, filters, sort, grouping. It does
not carry how tall someone else likes their rows. A screen that genuinely
needs a table-local override must earn the exception; it is not the shape.

**The trigger reports the scope.** When the menu holds appearance alone,
sun/moon is the honest glyph — it reports the current appearance while the
menu chooses, so the two jobs never collide — and the contrast circle ◐ is
the neutral alternative that names appearance without picking a side. Once
density joins the menu, both of those lie by omission: they name one of the
two settings inside. The trigger becomes a pair of sliders — not "theme",
not "density", but "adjust how this looks", which is the menu's actual
scope. Rule: the trigger must not name a subset of what the menu holds.

Honest-stack mapping: the menu is a server-rendered overlay; choosing posts
to the preferences endpoint and the server re-renders with `data-theme` and
`data-density` set (or `data-theme` absent, for System) — no flash of the
wrong theme, no client state.

Open decision: appearance-override persistence. Session-scoped (device stays
the source of truth; every visit greets in System) vs. stored per user (a
decision made once holds). May legitimately differ between public sites and
signed-in applications. Density has no such question — a comfort setting
that resets every visit is not a setting. Evidence and named prior art:
research/theme-control.md.

---

### 2.16 Popover height — fill, then scroll (rule)
Any popover opened from a control — the dropdown menu (2.3), the view panel
(4.1–4.2), the sort list, the group menu, the field visibility panel (4.3) —
sizes itself to its content and grows downward until it stops one gutter
short of the window's bottom edge (`--popover-gutter`, ≈100px); only past
that point does its list scroll internally. A taller window shows more
items with no scrolling; a short window scrolls sooner; no popover caps
itself at an arbitrary item count while the screen below it sits empty.
Where the space beneath the anchor is too shallow, the box opens upward
under the same gutter. Implementation: `max-height` from the viewport
height minus the anchor's offset and the gutter; pinned parts (a pane
title, bulk actions) stay put while the list scrolls. Exception: the
command palette (3.10) sizes from the center of the screen by its own rule.

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

### 3.0b Page head — title, meta, status, primary action
The row a page title anchors. Options, and the choice belongs to the
application (white paper chapter 14 argues both sides):

- List page, no display title — the rail names the page; the pane starts at
  the toolbar. The `<h1>` still exists, visually hidden, because readers
  navigating by headings need one.
- List page, name in the toolbar row (`.page-head__name`) — visible, costs no
  extra row, modest rather than display size. Preferred where the shell lets
  the rail hide, since the rail's marker can be absent, and where the name can
  carry something the rail cannot (a count).
- Record page (`.page-head`) — title, meta line, status, and primary action in
  one row. Always prominent: no navigation lists every record, so the title
  carries information nothing else on screen carries.

Fixed regardless of option: exactly one first-level heading per page, and the
document `<title>` always set. Failure modes: a display-size heading that only
echoes the rail, and a title kept beside a breadcrumb (2.10) ending in the
same word — the third statement of one fact.

### 3.0c Chrome stack — the rhythm above the data
Everything between the page's top edge and its first record, spaced as a
ladder rather than a rhythm. Proximity is the only grouping signal a stack
of chrome has, and equal gaps spend it on nothing: four evenly spaced bands
read as four unrelated strata, leaving the reader to work out which parts
belong together.

The steps halve, and each halving states a relationship:

| Gap | Step | What it says |
|---|---|---|
| Page title → toolbar | `--space-6` | The title is a separate stratum |
| Toolbar → scope rail | `--space-4` | These are one control assembly |
| Scope rail → table | `0` (shared line) | The rail is the table's own top edge (2.6) |

Two consequences worth stating. The ladder is what makes the assembly
legible without adding a single divider — dividers are ink spent on what
spacing already says. And it pays for itself in rows: a header region
laddered this way runs roughly a third shorter than one spaced uniformly,
and on a dense list every pixel returned is another record visible before
the first scroll. Where the title area grows (a description, a status), a
hairline beneath it is the honest divider — but only once the ladder alone
stops carrying the grouping.

### 3.1 App shell
Sidebar + topbar + main. Options: sidebar expanded/collapsed (a `preferences`
row); active item via `aria-current="page"` from the request path; `hx-boost` for
instant transitions.

### 3.1a The two-column agreement
A rail and a content column are two documents unless they agree on
something, and two shared lines are enough (`.app-frame`):

- The rail's brand row sits on the page title's baseline. Both columns'
  heads take one height and one bottom edge, so the line is exact rather
  than near — a three-pixel miss reads worse than either agreement or a
  clear difference.
- The first nav item starts where the first control starts. With the heads
  equal and both columns running the same first step, this falls out for
  free.

Everything below those two lines may differ freely. Four rules hold them:

1. The shell's own controls ride in the brand row — chrome beside chrome —
   rather than taking a band of their own to hold one icon, which is what
   pushes the nav out of agreement in the first place (3.2 utility
   controls).
2. The rail runs the same halving ladder as the content (3.0c): a full step
   down to the first group, half a step between groups, a quarter from a
   label to the items it names.
3. One left margin governs the rail — the item icon aligns with the mark
   above it, and the active pill's background is free to bleed left of that
   line. A background may pass the text margin; text may not.
4. The gutter is symmetric about the divider, so the line sits in its own
   channel rather than hugging the rail.

Type ratio across the divider. The two heads sit on one line, so their
sizes are compared whether or not that was intended, and the ratio states
which name outranks which. The rule: **the wordmark is never smaller than
the page title.** An application's identity outranks the name of any one
page inside it; a title set two steps above the mark inverts the hierarchy
and reads as though the page were the product. Both take the same step
(`--text-lg`) unless the brand is a drawn wordmark that earns more. The
subtitle under each — the product line under the mark, the record count
under the title — takes the small muted step, matching across the divider
too.

And the formatting rule the layout implies: the rail recedes. It is chrome
while the table is the work, so navigation never sets larger than body text
and only the current item stands at full strength — the rest one step down,
as the submenu children do. A rail that outshouts its data has the
hierarchy backwards.

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

Submenu style. Four parts, and each answers why it looks the way it does.
The rail is one continuous hairline on the children's container, never a
border per child — a per-item border breaks at every row gap and reads as
unrelated fragments instead of a branch. It descends from the centre of the
parent's icon (`calc(var(--space-3) + var(--sidenav-icon) / 2)`), so the
children hang from the row that owns them rather than from the panel edge.
Children are muted at rest, because the parent carries the group's weight;
hover restores full text colour. Children take no icons — icons mark the top
level only, so a child row can never be mistaken for a parent, and the
indent plus the rail already say where it sits. The active child marks the
rail (a 2px accent segment) rather than filling a pill, so position inside
the branch reads without competing with the active top-level item, which
does fill. Depth stops at two levels; a third is promoted to tabs in the
page (menus research).

### 3.3 Dashboard grid
User-composed widget grid. Layout is a `views` row (`{"tiles":[{"w":…}]}`); each
tile is a fragment loaded with `hx-get hx-trigger="load"`; add/remove/rearrange
posts the new layout. Ships with a designed Empty state.

### 3.4 Data table
The core primitive. Options: density (token switch) · sticky header · sortable
columns · selectable rows · numeric mono columns · row actions (ghost ⋯ menu) ·
footer with Pagination. Server-sorted, server-filtered; rows are `_row.html`
fragments.

A status column that duplicates a date column. Where every "reviewed" row
carries a date and every "to review" row carries a dash, the two columns
encode one fact, and one of them is width spent on nothing (the badge-dot
logic applied to a column). If the vocabulary is genuinely binary, the date
column alone says it. Keep both only when the status vocabulary is larger
than the date can express — overdue, in progress, waiting — in which case
design the whole scale rather than the pair.

Column alignment. One master rule generates the rest: a header always takes
its column's alignment, so the label and the values it names share an edge.
Alignment follows what a value means, not what it is made of — the test is
whether anyone would ever compare or total the column.

| Column kind | Alignment | Notes |
|---|---|---|
| Text (names, descriptions) | Left | Clip to one line rather than wrap, so rows keep one height and column edges stay straight |
| Pills, badges, marks, avatars | Centre (`--center`) | Short fixed tokens only — never prose, which is unreadable centred |
| Numbers, currency, scores | Right (`--num`) | Mono, tabular figures, one decimal precision for the whole column; the unit lives in the header, never repeated per row |
| Fixed-format dates | Right (`--num`) | Ordinal, so they compare like magnitudes and mono makes the column exact. Relative dates ("2 days ago") are text — left |
| Identifiers and codes | Left (`--mono`) | Mono but never right: a code is read left to right, not compared. Digits alone do not make a number — postal codes, phone numbers, and account numbers are identifiers |
| Selection checkbox | Centre (`--check`) | First, fixed narrow; the header holds select-all |
| Row actions | Right (`--actions`) | Last, fixed narrow, never hideable (4.3) |

Two rules the table above implies. Empty headers are still named: a column
whose header shows nothing on screen — selection, favourites, actions —
carries a `.visually-hidden` label, because a screen reader announcing
"blank" is a column with no name. And a placeholder for a missing value
takes its column's alignment, never an exception: a missing number sits
right where the number would have been.

One craft trap in the first column. A leading mark inside a text cell — an
avatar, a status dot, a favourite star — pushes the text right while the
header stays at the cell edge, so the label and its data start at different
places and the eye notices without being able to name it. Either the mark
sits in its own narrow column, or the cell uses `.data-table__cell--marked`
so the mark and the label share one left edge with the header above them.

Header anatomy. The head is a different stratum from the data, and it
differentiates by treatment rather than by volume — making the labels darker
or heavier puts them in competition with the values they name, and the values
are the point. Four parts:

- A band behind the head (`--color-well`), which does most of the separating
  without adding a unit of text contrast.
- The label one step quieter than its data: muted, medium weight. Optional
  micro-label variant (`.data-table--head-label`): uppercase and
  letterspaced, so the head stops reading as data at all — all-caps is
  measurably slower to read, an acceptable trade for a handful of fixed
  words learned once, never for content. One treatment per application.
- The strongest rule in the table beneath it (2px `--color-border-strong`),
  so the head/body split outranks every row separator. Never a box around
  the head — that makes it a floating card (3.0).
- Sticky. An unlabeled column at row fifty is the real complaint behind
  "the header is hard to see".

The head keeps one height in every density step (`--row-pad-y-head`, which
density never re-points). Density exists to fit more records on screen;
compressing the head buys a single row once and costs the legibility of the
labels that orient the whole table. It would also move the table's top edge
on every density change — the one line that should stay put while the rows
beneath it breathe.

Alignment and marking: numeric columns right-align, header included, while
the header label itself stays sans — mono is for the figures, not for the
word naming them. Identifier columns use `.data-table__cell--mono`,
left-aligned, because a code is read rather than compared. The sorted column
carries its direction in the header (`.data-table__sort--active` plus
`.data-table__sort-dir`): a toolbar claiming "Sort · 1" while no column is
marked is a claim the table never confirms.

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
Chip-bar (applied filters) · the four view controls · primary action. Everything
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
  State-honest label: `Hide fields` while nothing is hidden; `Hidden
  fields · N` once N are — the count names what is already hidden, and
  an action verb beside it would misread as an instruction.
- Filter → the filter builder (4.4): condition rows, add-condition,
  add-group.
- Group → the group menu: one grouping field + direction. Group headers band
  the table — which is why grouped tables skip the zebra stripe (3.4).
- Sort → the ordered sort list: several sorts stacked, direction per field.

Deliberately absent, first: a row-height button. Density is per-user, not
per-view — it lives once in the Display control in the app header (§2.15).
A toolbar copy would offer to save someone else's comfort setting into a
shared view. A screen that truly needs a table-local override earns the
exception and states why.

Deliberately absent, second: a color button. Painting rows from the toolbar puts
meaning into decoration; meaning belongs to the semantic colors — badges,
marks, and a rule the view declares in its description line (see the
brand-vs-meaning chapter). Order rule: the four controls keep this order in
every application; a fifth control enters by the standard workflow
(AGENTS.md §11), never ad hoc.

Control treatment — when a control is boxed. The toolbar carries two kinds
of control, and the treatment says which is which rather than decorating
either:

- A control that holds a value is boxed. A text field needs its box to show
  where typing goes; a toggle needs an outline because an unfilled box is
  what makes "off" legible; the lens is the same. Box = something lives
  here.
- A control that opens something is not boxed (`.button--ghost`). A door has
  no state to display at rest, so a container around it describes nothing,
  and nine contours in one row is ink spent saying nothing nine times.
  Hover must give these a background — borderless is a weaker affordance at
  rest, and the hover ground is what repays it. Without it the criticism of
  flat controls lands fairly.
- A borderless control announces state with a fill, never by growing a
  border (`Sort · 1`, `Hidden fields · 3`). Fill is the stronger signal on
  an unbordered control, and it keeps "has a value" reading the same way
  across the whole group.

Icon-only qualifies twice over. It is permitted where the symbol is genuinely
universal and the control either performs an action or opens a menu — the
row-actions ellipsis, the Display trigger in the app header (§2.15) — and it
always carries an `aria-label` and a tooltip. It is not permitted for a
control that holds a value *and shows it at rest*: such a control has a
state to state, so it takes a label and its value (`Sort · 1`,
`Hidden fields · 3`) like every neighbour. The line is not icon vs. label,
it is door vs. dial: a door has nothing to report until it opens, a dial
must report or it is lying by silence. And an action sitting among
configuration controls takes a separator (`.table-toolbar__sep`), because
adjacency implies membership — the same hairline that separates the lens
from the scope pills it composes with.

Deliberately absent, third: a download button. Export is a view-level
operation — it exports *this* configuration of columns, filters and sort —
so it lives in the view menu beside duplicate and delete (§4.2), where its
scope is unambiguous. In the toolbar it would read as "export the table",
scope unstated, and it would take a permanent slot for something almost
nobody does daily. The frequency budget that governs row actions governs
the toolbar too: a permanent slot is earned by daily use, not by
importance.

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
- **The foot of a scrolling list** (`.list-foot`) — three states in one slot,
  and both scrolling models owe it. More coming: spinner plus a word, where
  the next rows will appear. The end: a hairline and the total stated
  ("End of list — all 248 accounts shown"), because a bare end-of-list
  leaves the reader counting while a number converts the worry into a fact,
  and it answers the second question at the same time — a list that ends
  this way has no page two to look for. Nothing: a list that fits on screen
  shows neither, since an ending announced under six rows is ceremony. The
  marker is flow content, never pinned furniture, so it satisfies the
  scrolling-page rule that nothing may sit at the bottom of the screen — it
  is only ever seen at the true end. Carries `role="status"` so the ending
  is announced, and it is the natural home for a back-to-top link.
- **Contained scroll (recommended)** — the grid's box fills the viewport
  height and rows scroll inside it; sticky column header at the box top;
  toolbar above and bulk bar + summary below never move; no next button.
  One demand: the shell hands the grid its height exactly — a page that
  scrolls and a grid that scrolls is the double-scrollbar trap.

### 3.13 Favorites
A personal collection flag, and the reference case for the lens toggle
(1.13). Five parts, each answering a question a reader asks:

1. Marker column (`.data-table__cell--fav`) — a star in the leading position
   beside the identity column, pinned with it on wide grids (3.4). Filled
   with the accent on favorites; on unmarked rows drawn only on hover or
   keyboard focus — transparent but still clickable, and still ≥
   `--target-min` — because a column of hollow stars is the badge-dot
   mistake repeated (1.6). Leading, not trailing: the star is primarily a
   state marker, and markers belong where the eye scans, at the row's start.
   A trailing star beside the row menu is a permitted variant only on narrow
   tables where the whole row fits on screen; on a wide grid it sits past
   the horizontal scroll, invisible exactly when the reader is reading the
   name (the tracking problem of the rows chapter).
2. The marker is the toggle — one click in place, no menu round trip. The
   repeated-icon caution (3.4) does not apply: this icon is primarily a state
   marker that happens to be clickable, the action is trivially reversible,
   and no destructive action sits nearby.
3. Overflow-menu entry — the discoverable, keyboard-obvious path, with a
   state-honest label pair (`Add to favorites` / `Remove from favorites`,
   matching the row's current state) and the same star glyph as the marker.
   Dual entry is deliberate: the menu is for discovery, the inline star for
   frequency. Where the row's actions cluster in a trailing column, that
   column is fixed — always last, never hideable or reorderable in the field
   visibility panel (4.3), because a reader must not be able to hide the
   only route to a row's actions.
4. Emptying the collection — and it depends on what the table has. Two
   tiers, because the composed path presupposes components a table may not
   ship:

   - A table with row selection: the bulk-actions bar (3.9) gains add and
     remove, so emptying is lens + select-all + remove — three clicks,
     three existing components composing, no new control. This is the
     primary path wherever selection exists, and a `Clear all favorites`
     entry in the view panel's actions pane is its optional discoverable
     twin (the dual-entry logic of the row star and its menu: menu for
     discovery, direct gesture for frequency).
   - A table without row selection: there is no bulk bar to hold the pair,
     so the row star is the only per-record path (fine for a handful) and
     the `Clear all favorites` entry becomes required rather than optional
     — it is the single action that needs no selection, and without it a
     reader who starred forty rows has no way back except forty clicks.
     Never substitute a standing clear-all button in the toolbar: an
     unbounded erasure one click from everything is the shape being
     avoided, whether or not selection exists.

   Both tiers route through one confirm, and it is the same confirm: when
   the action covers the whole collection it states the count — "Remove all
   47 favorites?", the count in the question and the verb on the button
   (2.11, and the confirm-copy rule) — so the scale of an erasure is never
   discovered afterwards. Prescribing the composed path without checking
   for selection is the general trap: a path may only be prescribed where
   its components are present, and the catalog names the fallback where
   they are not.
5. Empty lens — the empty state (3.11) when the lens is on and nothing is
   starred: teach the gesture in one sentence, never a bare grid.

Semantics: favorites are always personal — per user, server-side, synced
across devices; a colleague's star never moves a reader's (contrast views,
which may be collaborative). The filled star takes the accent (a
user-selected state), never the warning color (a favorite is not a warning).
Favorites never auto-sort to the top: silently reordering breaks the sort the
toolbar claims — the lens is the honest way to see them together.

The lens itself (1.13) is part six's other half: the toolbar star that
narrows any view to the collection, composing with every scope, filter, and
sort. Its finite rules:

- Count visibility. The count always shows, pressed or resting, including
  zero. A withheld zero reads as unknown rather than as none — the same
  reasoning as the scope-tab count (2.6), so counts-at-rest is one rule
  across the system rather than a rule with an exception. `★ 0` at rest is
  also the honest invitation: it says the collection exists and is empty,
  which is what teaches the gesture.
- What the count counts. Favorites within the current filter set, not within
  the whole book: the number must predict the click. A resting `12` that
  yields four rows because a status filter is on has lied, and every other
  count in the system (`Filter · 2`, `All 248`) describes the configuration
  in force.
- URL. Only the flag travels (`?favorites=1`, omitted when off) — never the
  favorite ids. The set is per-user server state read at render time (a
  server-read cookie is an acceptable first implementation; browser storage
  restored after paint is not — it is client state and it desynchronizes).
- Empty states, two cases with different primary actions. Lens on, no other
  filters, nothing starred: title "No favorites in this view", one sentence
  teaching the row star and the menu, and the primary action turns the lens
  off — the collection is empty, so clearing filters would change nothing.
  Lens on with other filters, no matches: "No favorites match these
  filters", primary action clears the filters, secondary turns off the lens
  — the collection exists, the filters are what hid it. Both teach; neither
  is a dead end.

Live renderings: the specimen's Favorites section and the white paper's
Favorites chapter.

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
The pane fills the window before it scrolls (2.16); on narrow screens the
two panes stack.
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
The reference product puts four heights — short to extra-tall — plus wrap
headers in the view, persisted per view. The system diverges: row height *is*
density, density is one axis of three steps, and it belongs to the reader,
not to the view (§2.15). The control lives once, in the Display menu in the
app header; it is not repeated in the toolbar and is not written into a
saved view. What stays view-owned here is the part that really is about the
data: wrap headers on/off (a table modifier), and tall rows meaning
line-clamped multi-line cells — a decision about the *content* a column
shows, which travels with the view legitimately.

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
- A casing lint for navigation: §3.2 rules one casing per application; a
  pure-function classifier over rendered nav labels (title case vs sentence
  case, fail on mixture) moves the rule from prose to machinery.
