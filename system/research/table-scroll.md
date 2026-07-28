# Table scroll — how the table meets the bottom of the screen

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic. Live
renderings of every candidate discussed here are in the white paper's chapter
on the scroll question and in the specimen.

## The question

A data table holding two hundred and forty-eight rows cannot show them all at
once, so something has to give: either the table is cut into pages and the
reader clicks through them, or the rows keep coming and the reader scrolls.
That one decision ripples outward — it decides whether a Next button exists,
whether anything may sit at the bottom of the screen, where the summary
numbers and bulk actions live, and how much the browser has to hold in memory.
Three models answer it, and each has a published record.

## Option one — pages

The classic: a fixed number of rows, a footer with "1–15 of 248", Prev and
Next. Nobody's favorite — the click tax is real, and the published usability
literature has measured it: Nielsen Norman Group's write-ups on pagination
record that users often stop at the first page and that clicking through
pages is slower and more effortful than scrolling the same content. Yet the
model survives everywhere for honest reasons. It is the only model where the
reader has a stable address — "page 3, sorted by score" is a bookmarkable,
sharable, back-button-safe place — and the only one where the server does
bounded work per request no matter how large the table grows. E-commerce
research from Baymard Institute keeps finding pagination appropriate for
goal-directed searching, where the reader needs to know where they are in the
result set and how much remains. For a server-rendered system it is also the
zero-risk baseline: plain links, no script, nothing to restore.

The verdict on pages is not "wrong" but "chosen deliberately": right where
position-in-set matters (search results, audit logs read to a date), wrong as
the default for a working grid someone lives in all day.

## Option two — the page scrolls, and the bottom edge belongs to the rows

The second model lets the document itself grow: rows continue as the reader
scrolls, more arrive when the scroll approaches the end, and with a thousand
rows the reader simply keeps going. The published record on infinite scroll
is rich and mostly cautionary, and the cautions convert directly into rules.

The famous failure is the unreachable bottom: anything placed below an
infinite list — a footer, a summary, actions — recedes forever as new rows
push it down. Nielsen Norman Group documented the pattern years ago
(footers fleeing from readers who chase them). The honest conclusion is the
rule this system adopts: **in the scrolling-page model, nothing may sit at
the bottom of the screen.** The bottom edge belongs to the last row that
happens to be visible, and to nothing else. Everything the paged model kept
in a footer — the selected count, the bulk actions, the summary numbers, the
result total — moves above the table, into the toolbar region, where it is
always reachable.

The other recorded costs, each with its mitigation: the scrollbar lies
(its size and position change as content arrives — tolerable when the
toolbar states the true total); the back button must return to the same
place (browsers restore scroll for real navigations, so a server-rendered
list that grows by real fragments keeps this working); keyboard and
assistive-technology users need the arriving content announced (the ARIA
feed pattern exists for exactly this); and deep scrolling accumulates
thousands of live rows in the document (the point where the third model, or
windowing, takes over). The mechanism itself is native to the system's
stack: an HTMX request triggered when a sentinel row is revealed appends the
next fragment — no custom script, degrading gracefully to a plain "more"
link when scripting is absent.

## Option three — the grid owns the scroll, the chrome keeps its place

The third model changes what scrolls. The table's box stretches to fill the
height of the screen; the rows scroll inside it, endlessly, fed the same way
as option two; the column header stays pinned at the top of the box, group
headers stick below it as their group passes, and the chrome — toolbar
above, bulk actions and summary below — never moves. There is no Next
button, and there is nothing dishonest about the bottom of the screen: the
summary row pinned there is not fleeing from anyone, because the scrolling
happens inside the frame above it.

This is the application-grid tradition, and it is what every
spreadsheet-database product ships: Airtable's grid, Notion's table views,
and every desktop spreadsheet before them scroll the rows inside a fixed
viewport with the controls at rest. The pattern's demands are real but
well-mapped: the box must genuinely fit the viewport (a page that scrolls
*and* a grid that scrolls is the notorious double-scrollbar trap, so the
shell must hand the grid its height honestly); the sticky header and sticky
group rows are native CSS on the scroll container, no script; and at very
large depths the document-size cost returns, answered in mature grids by
windowing — rendering only the visible slice — which is an implementation
detail behind the same appearance.

The scrollbar-position problem softens here too: the grid can state "showing
1–40 of 248, more arriving as you scroll" in the summary row that never
moves.

## What the schools agree on

Across the literature, three points repeat. First, the choice is by task,
not by taste: browsing and monitoring favor scrolling, position-aware
retrieval favors pages — which is why the catalog keeps all three models on
display rather than deleting two. Second, hybrid "load more" buttons —
Baymard's recommended compromise for product lists — are a variant of option
two with an explicit gesture replacing the automatic one; the same
bottom-of-screen rule applies. Third, whichever model is chosen, the total
must stay visible somewhere fixed: readers tolerate not seeing all rows, but
not losing how many there are.

## Recommendation

The contained scroll — option three — as the default for working grids: it
is the only model that keeps every piece of chrome honest and reachable
while still abolishing the Next button, and it matches the tool tradition
this system's tables come from. The scrolling page — option two — where the
table *is* the page (a feed, a log), with its bottom-of-screen rule enforced
strictly. Pages — option one — where position in the set is part of the
task. All three stay in the catalog, rendered side by side.

Sources: Nielsen Norman Group on infinite scrolling and its costs, and on
pagination; Baymard Institute's e-commerce testing of pagination, "load
more", and infinite scrolling; the W3C ARIA Authoring Practices feed
pattern; CSS positioning specifications for sticky headers inside scroll
containers; HTMX documentation on the revealed trigger for incremental
loading; the shipped grids of Airtable and Notion as the application-grid
precedent.
