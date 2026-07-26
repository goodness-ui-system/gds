# Table inline editing — why some products allow it, why many refuse

Research note. Named products and sources are cited here because this folder is the
one place citations are allowed; operating documents stay generic.

## The question

Some applications let a value be changed directly in a table cell, the way a
spreadsheet does. Others make every change go through the record form that opens
when a row is clicked. Is the second group just lazier — or is there a real reason
to refuse inline editing?

## Plain-language glossary

A few words this note leans on, defined once:

- Affordance — the visual hint that tells a reader something is interactive.
  A button looks pressable; an underlined word looks clickable. A table cell that
  can be edited but looks identical to one that cannot has a missing affordance.
- Commit — the moment a change is actually written to the database. Everything
  before the commit can still be thrown away safely.
- Draft (or pending changeset) — a set of changes that have been made on screen
  but not committed yet. The draft can be reviewed, corrected, or discarded as a
  whole before anything is written.
- Validation — the checks a value must pass before it is accepted: is the date
  real, is the number in range, is the field allowed to be empty.
- Cross-field validation — checks that involve more than one field at once:
  "the end date must be after the start date", "if status is Closed, a reason is
  required". A single cell cannot show this kind of error well, because the error
  belongs to the combination, not to one cell.
- Maker-checker (also called dual control or four-eyes) — a rule used in
  regulated work: the person who makes a change cannot be the one who approves it.
  A second person must review before the commit.
- Optimistic update — showing a change as done before the server has confirmed
  it, and quietly rolling it back if the server refuses. Feels fast; can lie.

## Why many serious products refuse inline editing

The refusal is usually a decision, not a gap. Four reasons come up in every
serious treatment of the subject:

1. Validation has nowhere to live. A form has room next to each field for a
   label, help text, and an error message. A table cell has room for a value. The
   moment a rule fails — especially a cross-field rule — the cell cannot explain
   itself, and the error ends up in a toast the reader has already stopped watching.
2. The commit moment becomes invisible. In a form, Save is the commit; everyone
   understands nothing happened until it was pressed. A grid that writes on every
   cell exit commits dozens of times behind the reader's back. An accidental key
   press becomes a silent write to the record.
3. Governance breaks. Under maker-checker rules a change must be reviewed before
   it lands. Cell-by-cell instant writes are the exact opposite of that; only a
   draft that is submitted as a batch can be routed through an approval.
4. Accessibility is hard to retrofit. A grid where cells morph into inputs
   needs the full keyboard grammar (see below) and careful screen-reader wiring;
   the W3C publishes a dedicated pattern for it precisely because ad-hoc attempts
   fail. Screen readers announce a plain table well; a half-editable one, badly.

## Why some products embrace it anyway

Repetitive correction across many rows is genuinely miserable in a form: open
record, change one field, save, back, next record, forty times. Products whose
daily work looks like that — spreadsheets, project trackers, data platforms —
invest in grid editing because the productivity gain is real. The best of them all
converged on the same shape.

## The pattern the industry converged on: draft plus save bar

Salesforce's Lightning Design System is the clearest statement of it: entering
edit mode marks the grid; every edited cell is visually tinted and held as a
draft; a bar counts the unsaved changes and offers one Save and one Cancel for
the whole batch. Nothing commits until Save. GitHub's Primer design system draws
the same line from the other direction, separating "declarative" commits (an
explicit Save button) from "imperative" ones (saving as a side effect) and warning
about the latter. The W3C ARIA Authoring Practices grid pattern supplies the
keys: Enter or F2 begins editing, Escape cancels and restores, Tab commits and
moves on, arrow keys travel the grid.

The batch draft solves each refusal above: validation runs server-side on the
whole batch and returns per-cell errors while nothing is yet written; the commit
moment is one visible button; the submitted draft is exactly the artifact a
maker-checker review needs; and the keyboard grammar is standardized rather than
invented.

## Fit with this system's architecture

The server-rendered stack keeps state in the DOM and on the server, which makes
the draft pattern unusually natural: edited cells post to a server-side pending
changeset, the save bar is a fragment that re-renders with the current count, and
Save submits the changeset — the same object the review/diff form already
displays. What the stack does not do well is spreadsheet fluency (instant
cell-to-cell typing with zero round trips); that is the honest boundary, and the
reason instant per-cell commit stays reserved for single pickers with an Undo.

## The catalog of options (all on display in the specimen)

- A. Read-only table + form editing — the safe default.
- B. Edit mode with draft + save bar — for repetitive multi-row correction.
- C. Per-cell instant commit — pickers only, always with Undo.
- D. Editable-field whitelist — inline rights granted per column, not per table.
- E. The shared keyboard grammar — Enter/F2, Esc, Tab, arrows.

Open decisions, deliberately left to selection: whether option C exists at all
before an undo toast ships, and whether records under approval rules always force
option B's draft mode.

## Sources

- Salesforce Lightning Design System — Data Table / inline edit blueprint:
  https://www.lightningdesignsystem.com/components/data-tables/
- GitHub Primer — Saving patterns (declarative vs imperative):
  https://primer.style/ui-patterns/saving
- W3C ARIA Authoring Practices Guide — Grid (interactive tabular data) pattern:
  https://www.w3.org/WAI/ARIA/apg/patterns/grid/
- Nielsen Norman Group — Data tables and inline editing usability writing:
  https://www.nngroup.com/articles/data-tables/
