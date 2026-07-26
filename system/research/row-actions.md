# Row actions — visible icons vs. the overflow menu

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic.

## The question

A table row usually offers several actions: open, edit, duplicate, archive,
delete. Should they sit on the row as visible icon buttons, or behind a single
⋯ button (the overflow menu — a button that opens a longer menu of choices)?

## What the evidence says

Three problems with an icon per action per row:

1. Repetition destroys the signal. An affordance — the visual hint that
   something is clickable — works by contrast with its surroundings. Repeat the
   same icon on forty rows and it stops contrasting with anything; it reads as
   texture, like a ruled line, and the eye skips it. The Nielsen Norman Group's
   icon research adds the second half of the problem: outside a small set of
   universal symbols (search, print, play), users routinely misread bare icons,
   so every additional icon column adds guessing rather than speed.
2. Danger proximity. A destructive icon repeated down a column places an
   irreversible action one accidental click away from every record on screen.
   Mature systems bury destructive actions instead of surfacing them.
3. Clutter compounds. Two icons per row across forty rows is eighty competing
   click targets; data-dense screens lose the very scannability the table
   exists to provide.

The overflow menu's own weakness, from the same research: everything inside it
is invisible until clicked. The Nielsen Norman Group's contextual-menu
guidelines are direct about the consequence — contextual menus must never be
the only way to reach an action people need constantly, and their contents
must stay consistent from row to row.

## The convergent industry rule: a frequency budget

The large design systems reconcile the two findings the same way. IBM's Carbon
data-table guidance puts row actions in an overflow menu in the last column,
optionally revealed on hover, and GitHub's Primer action bar collapses anything
beyond a small number of frequent actions into overflow. The shared shape:

- At most one — occasionally two — actions earn a visible spot on the row,
  and only if they are used constantly, harmless if misclicked, and drawn with
  a universally understood symbol.
- Everything else goes into one ⋯ menu, always in the same (last) column,
  always with the same contents for the same record type.
- Destructive actions never appear as bare row icons; inside the menu they
  take the danger color, the last position, and a divider above (the
  consequential-action rule).
- The quiet variant — row actions hidden until hover — is legitimate only if
  keyboard focus also reveals them (`:focus-within`), so keyboard and
  assistive-technology users are never locked out. Carbon added hover-reveal to
  its data table for exactly this clutter reason.

## Fit with this system

The default table already uses one ghost ⋯ per row. The catalog in the
specimen renders the full option set: A (⋯ only, the default), B (one earned
icon plus ⋯), C (hover/focus-revealed ⋯), and the rejected anti-pattern (a
destructive icon per row) shown for contrast. The rule as encoded: default is
A; B is an exception argued per case against the three tests; C is a styling
variant of A or B; the anti-pattern is forbidden.

## Sources

- Nielsen Norman Group — Designing Effective Contextual Menus:
  https://www.nngroup.com/articles/contextual-menus-guidelines/
- Nielsen Norman Group — Contextual Menus: Delivering Relevant Tools:
  https://www.nngroup.com/articles/contextual-menus/
- Nielsen Norman Group — icon usability research:
  https://www.nngroup.com/topic/icons/
- IBM Carbon Design System — Overflow menu usage:
  https://carbondesignsystem.com/components/overflow-menu/usage/
- Carbon data table — overflow visible on hover (design discussion):
  https://github.com/carbon-design-system/carbon/issues/5804
- GitHub Primer — Action bar:
  https://primer.style/components/action-bar
