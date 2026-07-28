# Table rows — hairlines, zebra stripes, and how the eye crosses a wide table

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic. Live
renderings of every candidate discussed here are in the white paper's chapter
on rows and in the specimen.

## The question

Look at the record name in the first column of a wide table, then read the
number in the fifteenth. Somewhere in the crossing, the eye slips a row — and
the wider the screen, the longer the tightrope. Row delimitation is the set of
devices that keep the eye on its lane: the hairline between rows, the
alternating background (zebra striping), bare whitespace, the hover highlight,
and the pinned identity column. Each has a published record, and the oldest
evidence predates the screen entirely.

## The oldest answer — ruled and banded paper

Accountants solved this before software existed. Ledger paper ships ruled —
every row a printed line — and the wide-format tradition went further: the
continuous "green-bar" paper that line printers fed for decades alternates
pale green and white bands precisely so a reader can follow one record across
a yard-wide printout without slipping. Zebra striping is not a web fashion; it
is the banded ledger, digitized. That is also the honest frame for its
purpose: **bands exist for horizontal tracking**, and their value grows with
table width. A four-column table has no tracking problem to solve; a
twenty-column grid has little else.

## The measured record

The best-known controlled studies of zebra striping are Jessica Enders' two
experiments, published at A List Apart ("Zebra Striping: Does it Really
Help?", 2008, and "Zebra Striping: More Data for the Case"). The honest
summary of the findings: task speed and accuracy improved only modestly with
striping — mostly within the noise on narrow tables — but the gains grew with
table width, users made somewhat fewer row-slip errors on striped wide
tables, and participants clearly preferred striping. The author's own verdict
was on the order of "it can't hurt, and it may help." Nielsen Norman Group's
data-table guidance reaches the same posture from heuristics: zebra striping
or row borders are recommended for dense and wide tables, hover highlighting
for pointer users, and generous alignment discipline (numerals right-aligned,
in a tabular figure font) so columns read as columns.

The design systems split exactly along this line. IBM's Carbon ships zebra as
an off-by-default option on its data table; the US federal system offers a
striped variant with the same posture; GOV.UK's tables stay plain — hairlines
only — consistent with its minimal-ink doctrine and its typically narrow
tables; the major commercial systems (Salesforce, Material) default to
hairline dividers plus a hover state. Nobody makes stripes mandatory;
everybody with wide-table users makes them available.

## The trade — line against band

The hairline's case: it is the crispest possible row edge, it costs almost no
ink, it never collides with a state color, and it carries no suspicion of
meaning. Its limit: a line is a fence, not a lane. It separates neighbors,
but it gives the crossing eye nothing to ride — at fifteen columns the reader
is counting fences.

The band's case: a band is a lane. The eye rides a continuous ground from the
first column to the last, which is the one thing the hairline cannot offer,
and the thing the green-bar tradition proves at printout scale. The costs are
real and specific:

- **Meaning-suspicion.** Shading elsewhere in an interface means state —
  selected, disabled, highlighted. A first-time reader may pause on whether
  the shaded rows are special. The mitigation is subtlety and consistency:
  one quiet stripe everywhere, never a strong one somewhere.
- **A second ground to solve.** Every text color, status color, and mark must
  hold its contrast floor on both the base and the stripe. The stripe joins
  the contrast checker's jurisdiction or it silently breaks the floors.
- **State collisions.** Stripe, hover, selected, and edited are four
  backgrounds on one row. They must remain a strict ladder — stripe quietest,
  hover above it, selection unmistakably strongest — or states vanish on
  even rows.
- **Group parity.** In a grouped table the stripe restarts arbitrarily at
  each group break, and a two-row group reads as one shaded pair. Bands fit
  flat grids better than grouped ones.

Whitespace alone — no lines, no bands, rhythm from padding — is the calmest
of the three and the first to fail: it holds for a handful of columns of
prose and collapses exactly where the tracking problem begins. The published
guidance treats it as a narrow-table nicety, not a wide-table answer.

## The companions the question implies

Two devices answer the fifteenth-column problem more directly than any row
treatment, and both are native CSS:

- **The hover lane.** A row highlight under the pointer is the strongest
  tracking aid of all — a lane that follows the reader. Its limit is reach:
  it serves pointer users only, and it cannot help a printed or glanced-at
  table. It complements bands; it does not replace them.
- **The pinned identity column.** The first column — the record's name — stays
  put while the columns scroll beneath it (sticky positioning on the scroll
  container). The reader never loses *which row* because the answer never
  leaves the screen. This is the spreadsheet tradition's frozen column, and
  for wide grids it removes the return trip entirely.

## Recommendation

Hairlines remain the resting default — every table keeps its row borders and
its hover highlight. The band becomes a sanctioned variant for wide, flat,
dense grids: one quiet stripe derived from the theme's own ground colors (a
half-step between canvas and surface, so it re-solves itself in every theme
and family), decorative only, never carrying meaning, sitting strictly below
hover and selection in the background ladder. Wide grids additionally pin
the identity column. Grouped tables skip the stripe — the group headers
already band the table at a coarser rhythm.

Sources: Jessica Enders' zebra-striping experiments, published at A List
Apart ("Zebra Striping: Does it Really Help?"; "Zebra Striping: More Data
for the Case") · Nielsen Norman Group's data-table design guidance · the
green-bar continuous-form paper tradition and ruled ledger stationery · IBM
Carbon's data table (optional zebra) · the US federal design system's striped
table variant · GOV.UK's plain table doctrine · WCAG 2.2 — contrast minimums
apply on every ground, and color alone may not carry meaning · CSS sticky
positioning for frozen columns.
