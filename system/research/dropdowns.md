# Dropdowns — one word, three components, and the rules for each

Research note. Named products and sources are cited here because this folder
is the one place citations are allowed; operating documents stay generic.

## The question

"Dropdown" covers at least three different things: a menu of commands, a
picker for one option, and a picker for several. What are the rules for each,
when is a dropdown the wrong control entirely, and what belongs inside the
floating box besides the options?

## Finding 1 — dropdowns are overused, and the count decides

The most-quoted line in the literature is Luke Wroblewski's: dropdowns should
be the interface of last resort. The reasoning is mechanical, not aesthetic:
a dropdown hides its options behind a click, costs at least two interactions,
and gives no overview of what is available. The practical thresholds that
fall out of the research and the large design systems:

- Fewer than ~5 options, room on screen → show them: radio buttons or a
  segmented control. Nothing to open, nothing hidden.
- ~5 to ~10 options → a plain dropdown is fine; scanning a short list works.
- More than ~10–15 options → the list needs a search/filter field (the
  combobox pattern — an input that filters the list as it is typed). The US
  government design systems ship a dedicated combo box for exactly this case.
- Known-format values (a date, a quantity) → often better typed than picked.

## Finding 2 — the three kinds must not be confused

The Nielsen Norman Group's comparison of listboxes and dropdown lists draws
the structural line: a dropdown list is for one choice and closes on pick; a
listbox — visible checkboxes, multiple selection — is for several, and must
behave differently. Folding both into one look is what confuses readers.

- Action menu (commands): verbs that act on a record. Closes on fire. The
  gravest command is visually set apart — danger color, last position,
  divider (the consequential-action rule).
- Single-select: the current choice carries a visible check before anything
  is clicked (state first, action second); the menu closes on pick because
  the job is complete.
- Multi-select: checkboxes as the affordance (the square box is the learned
  signal for "several allowed"); the panel STAYS OPEN while ticking — a
  panel that closes per tick forces one reopen per choice; a selection count
  and a Clear are always visible; search sits first when the list is long.
  Selected values echo outside the closed control (chips or a count on the
  trigger), so the state survives the menu closing.

## Finding 3 — what else may live in the box

Depending on context the floating box legitimately carries more than bare
options: a label header naming the set; a search field (long lists); kbd
hints (action menus); a divider-plus-danger group (the consequential rule);
a footer with count and Clear (multi-select). Each addition must serve the
kind — a search field in a three-item menu is noise, a missing search in a
forty-item one is friction.

## Findings offered for review (not yet encoded)

- Group headers inside long single-select lists (like the palette's grouped
  results) — worth adopting once a real >20-item picker exists.
- "Recently used" or pinned-first ordering for pickers used constantly
  (owner pickers in triage tools) — powerful, but adds state to explain.
- Create-in-place ("+ Add new tag" as the last row of a multi-select) —
  saves a round trip to settings; needs validation rules.
- Async loading for very large sets (search queries the server instead of
  filtering a shipped list) — the natural Honest fit past a few hundred
  rows, since the menu is a server fragment anyway.
- Apply-button multi-selects (batch the filter change instead of applying
  per tick) — matches the draft + save bar logic when each tick is an
  expensive re-query; live-apply feels better when re-query is cheap.

## Sources

- Luke Wroblewski — Dropdowns Should be the UI of Last Resort:
  https://www.lukew.com/ff/entry.asp?1950
- Nielsen Norman Group — Listboxes vs. Dropdown Lists:
  https://www.nngroup.com/articles/listbox-dropdown/
- Balsamiq — Dropdown menu (combo box) guidelines:
  https://balsamiq.com/learn/dropdown-menus/
- CMS design system — Dropdown guidance (thresholds, when not to use):
  https://design.cms.gov/components/dropdown
- Cancer.gov design system — Combo box (search past ~15 options):
  https://designsystem.cancer.gov/components/combo-box
- Eleken — Dropdown menu UI patterns and examples:
  https://www.eleken.co/blog-posts/dropdown-menu-ui
