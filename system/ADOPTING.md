# Adopting Goodness (gds) — drop-in manual for a consuming application

Copy this file into the root of an application that adopts the system, named
`CLAUDE.md` or `AGENTS.md`, and edit only the two marked lines. Any coding
agent working in that repository reads it automatically and inherits the
system's rules without being told them again in every prompt.

Adoption means the application inherits the system whole. Per-product
identity is a brand skin — a palette family, a wordmark, an icon — never a
fork of the components. A rule that does not fit is reported back so the
system can change; it is not overridden locally, because a local override is
invisible to every other application and to the next person here.

---

## Where the rules live

- Catalog, the component contracts: <https://goodness-ui-system.github.io/gds/pages/system/components-catalog.html>
- White paper, the reasoning: <https://goodness-ui-system.github.io/gds/system/whitepaper.html>
- Specimen, everything rendered: <https://goodness-ui-system.github.io/gds/system/specimen.html>
- Source: <https://github.com/goodness-ui-system/gds> — `system/components.md` is
  the catalog's source and the file to read when a page is not to hand.

Cloning the system beside the application is worth the disk: an agent that can
read `system/components.md` and `system/ui.css` locally will follow them far
more closely than one working from a summary.

---

## The instruction that matters

Before changing any part of the interface, read the catalog section that
governs it. The catalog is written to be read in pieces — a single section
answers a single question, and most of the rules exist because something went
wrong once in a way that was expensive to find.

Never invent a component that the catalog already names. Where the catalog is
silent, build to its principles, then report the gap.

---

## The rules most often broken

These are the ones a fresh agent gets wrong. Each has a section in the
catalog; this list is a reminder, not a substitute.

1. **One hairline weight per object.** Every rule inside a table — the frame,
   the rail under a tab row, the head's bottom, the row separators — is the
   same 1px in the ordinary border token. A second weight inside one object
   reads as a hierarchy that is not there. Strength escalates only where a
   rule carries a boundary alone.
2. **Two devices never claim one job.** A filled header band does not also
   need a heavy rule beneath it. A gap that already separates does not also
   need a divider. When two devices claim one job, drop the one that carries
   no information the other cannot.
3. **Air belongs between sections, not inside lists.** Navigation items are a
   list; they stack at the row pitch with no added gap. Adding air inside a
   list costs twice — the rail stops being scannable, and the space meant to
   mark a real break stops marking anything.
4. **A caption hugs its object.** A full step above a label, a quarter step
   below it. Equal-ish gaps leave the label floating between two things and
   belonging to whichever the reader guesses.
5. **Status colour tracks the action demanded, not the state named.** A
   finished state is quiet; only an exception earns a filled ground. A green
   badge on completed work puts the loudest mark on the rows that need
   nothing.
6. **Door against dial.** A control that opens something is not boxed and owes
   a hover ground. A control that holds a value and shows it at rest wears its
   label and its value. Icon-only is for doors and actions, never for dials.
7. **The navigation marks the route, never the record.** Nothing relocates a
   reader as a side effect of data. The application may offer a change of
   context; it may never perform one.
8. **A label inherits the meaning of its neighbours.** A relationship fact
   placed among attribute facts will be read as an attribute. Attribute the
   group once rather than prefixing every label, and never with a possessive
   in a product where the reader may be viewing someone else's data.
9. **The browser's own popups never render.** `window.confirm`, `alert`,
   `prompt`, and the default rendering of `hx-confirm` all interrupt in
   system chrome that carries none of the application's identity. Keep
   `hx-confirm` as the trigger vocabulary, intercept `htmx:confirm`
   globally, and render the Dialog (§2.11) — default-deny: only the
   explicit confirm button proceeds.

---

## Verifying a change

Two habits catch nearly everything, and both take a minute.

**Assert geometry, do not look at it.** Where two things are meant to align,
measure both bounding boxes and print the difference. It is zero or it is a
bug. A near-miss of a few pixels is worse than either exact agreement or an
obvious difference, because the eye registers it without being able to name
it.

**Read pixels, not stylesheets.** Computed styles report what the CSS says;
only a screenshot reports what shipped. Scan a column of pixels through a
region and print each colour run with its height — a rule that comes back two
pixels tall is a doubled border, and one with a different value is the wrong
token. This habit has caught bugs that every other check reported as clean,
including a checker that agreed with itself instead of with the screen.

Check both themes and the narrowest supported width, every time.

---

## Reporting back

The system improves from what its applications discover. When a rule does not
fit, or a screen needs something the catalog does not name, write down what
was needed and why the existing rule failed, and raise it against the system
repository. A finding phrased as a rule with its reasoning is worth more than
a fix, because the fix helps one screen and the rule helps every application
that adopts the system afterwards.

---

<!-- EDIT THESE TWO LINES FOR THE APPLICATION -->
Application: `<name>`
Palette family: `<warm | cool | mono | goodness>` — set on the root element as
`data-palette`, with `data-theme` left to the reader's preference.
