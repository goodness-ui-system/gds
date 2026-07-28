# Menus — the side menu's anatomy, its options, and the schools behind them

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic. Live
renderings of every candidate discussed here are in the white paper's
Navigation chapter and in the specimen.

## The question

A side menu looks like the simplest thing in an application — a column of
links — yet every part of it is a decision: how a group announces itself, how
the items are written, whether they carry icons and at what size, how the
current item is marked, what separates one run of items from the next, how a
group folds, and what happens when a group outgrows the column. The major
design systems answer these questions differently, and a few of the answers
have actual user research behind them.

## First, what a side menu is — and is not

One question in this domain is genuinely settled. A navigation menu is a list
of links, not a "menu" in the widget sense that assistive technology
understands from desktop applications. The ARIA menu roles exist for
application menus (a right-click menu, a menu bar) and drag in a heavy
keyboard contract; putting them on site navigation breaks expectations, and
the W3C's own authoring guidance now says so on its example pages — the
disclosure pattern, plain links with an expand/collapse button, "is better
suited for most web sites". The practitioners who drove this consensus
(Adrian Roselli's "Don't use ARIA menu roles for site nav", Heydon
Pickering's "navigation menus are not menus; they're lists of links") won the
argument completely. For this system the consequence is already native: a nav
landmark with a label, lists of links, the current page marked with the
standard current-page attribute rendered by the server — which can never
drift from the truth, because the server knows the route.

## The group label

The small heading above a run of items comes in three schools. The uppercase
eyebrow — small, letterspaced, muted — is prescribed verbatim by Shopify's
system ("use all caps for section labels") and is the admin-template
tradition. The regular-case label — small bold text, no transform — is what
Salesforce, GitHub, HashiCorp, and Atlassian ship, and it has the readability
argument on its side: IBM's content guidance records that all-caps text is
measurably slower to read because word shapes disappear, and GOV.UK bans
block capitals outright. The third school has no labels at all: IBM's own
application shell groups by collapsible parents and thin dividers instead,
on the argument that a label costs a row without being clickable.

Two rules survive every school. The label is static text, never a link — the
thing that expands is a different element with its own affordance. And if the
uppercase look is chosen, the transform belongs to the stylesheet, never
typed into the content, so the copy itself stays in sentence case and the
style can change later without touching a word.

## Item casing

Title case against sentence case is a genuine two-camp debate with a lopsided
roster. Title case — every main word capitalized — is Apple's tradition,
applied consistently across its platform menus, and one large email product's
style guide uses it for top-level navigation specifically. Sentence case is
prescribed by Google, Microsoft, IBM, GOV.UK, Shopify, and Atlassian, and the
arguments are practical: it is the only rule writers apply consistently
without a referee ("title case is difficult to implement consistently across
an organization" — IBM), it keeps proper nouns distinguishable, and it
survives translation — most languages have no title-case convention at all,
so a title-case interface desynchronizes from its own localizations. The
catalog shows both; the honest summary is that title case reads as polish and
sentence case reads as pragmatism, and a system picks one and never mixes.

## Icons

No surveyed system requires icons on every menu item; the strongest stated
rule is all-or-none within a group — GitHub's guidance says it verbatim
("ideally all items have a leading visual, or no items have them"), because
one icon-less row in an icon'd menu misaligns the labels and implies a
hierarchy that does not exist. HashiCorp adds a level rule: icons on the top
level only, never on children. Everyone treats menu icons as decorative for
assistive technology — the word is always present and carries the meaning.

Sizes cluster tightly across systems: 16 pixels in dense 32-pixel rows
(IBM), 20 pixels in mid-density navs (Shopify, Microsoft), 24 in touch-first
drawers (Google). That maps exactly onto the two candidates on display: the
small icon that matches the text size and reads as part of the line, and the
large icon that leads the row. The icon-only collapsed rail — icons with no
labels — is contested territory: Microsoft's web system refuses to support
it, Google ships it with label-reveal modes, and for a zero-script system it
is out of reach anyway, because accessible tooltips cannot be delivered
without script. The defensible position is to skip it.

## The active item, hover, and metrics

The systems mark the current item with two or three cues stacked together,
drawn from a small taxonomy: a left keyline bar at the panel edge (IBM 4px,
Salesforce 4px, Shopify 3px), a short rounded indicator (Microsoft's small
bar), a full filled pill (Google — the strongest figure-ground, the most
vertical cost), or bold text alone on the quietest government systems. Every
system pairs the shape with a weight change, and none relies on color alone;
the current-page attribute is the programmatic equivalent. Hover is always
one step quieter than selected. Item heights run from 28 pixels (Shopify
desktop) through 32 (IBM, the proven data-dense setting) to 56 (Google,
touch-first); labels clamp to one line and truncate rather than wrap
(Google: "maximum lines per item is 1"); counts and badges are sanctioned
but bounded — one trailing count, not a decoration parade.

## Separators

Dividers are the semantically light alternative to titled groups — GitHub's
guidance frames the choice exactly that way: sections with labels when the
groups have names, thin rules when they do not. Google auto-inserts hairline
dividers between drawer groups. The classic divider case is the pinned
bottom run — settings and help — separated from the scrolling body.

## Submenus — the folding question

Three live schools, and a fourth that retired itself.

Show everything. Navigation is a table of contents; hiding items taxes
discoverability more than length taxes scanning. This is the school with the
strongest research behind it: the published hidden-navigation studies found
discoverability roughly halved when navigation is hidden, with longer task
times. The UK justice department's side navigation is the pure form — a flat
list with section headings, nothing collapsible. The school fails only when
the list outgrows the viewport.

User-controlled folding. Groups collapse behind a parent row with a chevron;
the reader, not the route, decides. IBM, GitHub, Microsoft, and Adobe all
ship this. Within the school, independent toggles are the norm — no surveyed
system forces an accordion where opening one group closes another, the
accordion spec itself makes exclusivity optional, and an open question stands
in the W3C's own tracker about whether auto-closing panels harms
accessibility. The chevron facts are worth recording precisely: in published
icon testing the caret was the only symbol users preferentially tapped over
the label, a plain right-arrow is ambiguous because it can also mean
"navigates elsewhere", and placement splits the evidence from the
convention — measured task times favor a leading chevron (one consistent
click position), while the product-system convention is overwhelmingly
trailing. Either way the entire row is the toggle target, never just the
icon.

Route-expansion. The server decides: the group containing the current page
renders open, the others closed — Shopify, Amazon's console system, and the
US federal system all work this way. For a server-rendered system this is
the purest zero-script mechanism of all: the state derives from the URL,
nothing needs storing, and back-and-forward are correct by construction.

The retired fourth school is the drill-down, where a child list slides in
and replaces the parent list; its best-known adopter deprecated it, because
it hides all sibling context.

The split-target trap has a settled resolution set: a parent that has no
page of its own is a toggle and nothing else; a parent that is a real page
is a link, with expansion following the route; and only when readers must
peek without navigating does a separate, separately-named disclosure button
sit beside the link. Never one element that both navigates and toggles.

Depth is capped at two levels by strong consensus (IBM says it flatly: the
panel does not support three tiers — promote the third level to tabs in the
page). Children indent by one step, about sixteen pixels beyond the parent.
A connector line beside the children, as one candidate on display draws, is
honestly labeled: it is a tree-view convention imported for its looks; no
surveyed sidebar ships it.

## The zero-script mechanics

The native disclosure element is the only true script-free collapsible
group, and it is production-proven at scale — GitHub built years of its
interface on it. Its known edges: the default triangle marker needs the
standard two-part reset before drawing a custom chevron; the summary row
should hold plain text only (no links, no headings inside); and screen
readers vary in what they call it (a button, a disclosure triangle, or just
the text) — degraded polish, not a failure. One recent platform change turns
a former caveat into a feature: as of the current interop cycle, every
engine auto-expands a closed disclosure when find-in-page matches inside it,
so a reader's search always finds items hidden in a collapsed group — and
styling must therefore never assume the server-rendered state is the only
one. Where folding state should persist, the precedents store it server-side
(a cookie or a per-user preference read at render time), never restored by
client script after paint.

On this stack the choice between the disclosure element and a server
round-trip per toggle is genuinely open: the disclosure element costs
nothing and works offline in the page; the round-trip keeps all state
server-side, matches the authoring-guidance pattern exactly (state carried
in the expanded attribute the server renders), and persists for free. Both
candidates are legitimate; route-expansion underneath either is the
foundation.

## Submenu overflow — the second column

When a group's children number in the dozens — a document's sections, a
deep settings tree — folding and indentation both fail: the fold still
scrolls, and the indent stops reading as structure. The overflow answer is
the second column: the parent stays one item on the rail, and its children
move into a column of their own beside it, one hairline away, with its own
quiet title. This differs from the retired drill-down in the decisive way:
the parent list stays visible, so sibling context is never lost. The
documentation site of this very system uses the pattern for its specimen
sections. The rule of thumb the catalog records: fold a handful of children
under a parent; give a parent with dozens its own column.

## What the evidence is worth

Genuinely research-backed: the hidden-navigation discoverability studies
(hiding roughly halves discoverability); the accordion-icon testing (the
caret preferred over every alternative, the right-arrow ambiguous); the
timed leading-versus-trailing icon comparison; the government accordion
research that led to pairing the chevron with visible show/hide text; and
the readability findings against all-caps text. Convention presented as
law: the trailing-chevron placement, the two-level depth cap, every icon
size, and the item-height bands. The casing debate is values, not evidence —
consistency and localization against polish — which is exactly why it needs
an explicit house decision rather than a silent habit.

## What this system takes from it

The white paper's Navigation chapter renders the candidates and keeps the
decision open. In brief: the rail principle stands; group labels are static
and come in eyebrow or sentence-case styles; item casing is a one-time house
decision between title and sentence case; icons are all-or-none per menu at
one of two sizes, top level only, never load-bearing; the active item keeps
a shape plus weight, never color alone; titled groups and bare dividers
split the separator job; submenus offer always-open, collapsible-disclosure,
and route-expanded candidates with depth capped at two; and the second
column is the recorded answer to a group that outgrows the rail.

## Sources

Standards and the menu-role question:

- W3C ARIA Authoring Practices — disclosure navigation pattern and examples:
  https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/
- W3C APG — menubar navigation example (the anti-menubar caution):
  https://www.w3.org/WAI/ARIA/apg/patterns/menubar/examples/menubar-navigation/
- W3C APG — accordion pattern (exclusivity optional):
  https://www.w3.org/WAI/ARIA/apg/patterns/accordion/
- W3C — open question on auto-closing panels:
  https://github.com/w3c/aria-practices/issues/3391
- W3C WCAG — technique ARIA26 (aria-current="page"):
  https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA26
- Adrian Roselli — Don't Use ARIA Menu Roles for Site Nav:
  https://adrianroselli.com/2017/10/dont-use-aria-menu-roles-for-site-nav.html
- Adrian Roselli — Link + Disclosure Widget Navigation:
  https://adrianroselli.com/2019/06/link-disclosure-widget-navigation.html
- Heydon Pickering — Inclusive Components, Menus and Menu Buttons:
  https://inclusive-components.design/menus-menu-buttons/

The systems surveyed:

- IBM Carbon — UI shell left panel (usage, style, metrics):
  https://carbondesignsystem.com/components/UI-shell-left-panel/usage/
- IBM Carbon — writing style (the all-caps and title-case objections):
  https://carbondesignsystem.com/guidelines/content/writing-style/
- GitHub Primer — NavList (groups, all-or-none visuals, depth warning):
  https://primer.style/components/nav-list
- Shopify Polaris — Navigation (all-caps section labels, route-expanded
  children, one-line clamp):
  https://polaris.shopify.com/components/deprecated/navigation
- Microsoft Fluent 2 — Nav (categories as accordions, no icon-only layout,
  fixed chevron placement):
  https://fluent2.microsoft.design/components/web/react/core/nav/usage
- Salesforce Lightning — vertical navigation (regular-case section titles,
  keyline active state): https://github.com/salesforce-ux/design-system
- Google Material — navigation drawer and rail:
  https://github.com/material-components/material-components-android/blob/master/docs/components/NavigationDrawer.md
- Adobe Spectrum — side navigation (headers vs multi-level):
  https://spectrum.adobe.com/page/side-navigation/
- HashiCorp Helios — side nav (icons top-level only):
  https://helios.hashicorp.design/components/side-nav
- Atlassian — navigation system and the deprecated drill-down:
  https://atlassian.design/components/side-navigation
- AWS Cloudscape — side navigation (route-expansion):
  https://cloudscape.design/patterns/general/service-navigation/side-navigation/
- USWDS — side navigation: https://designsystem.digital.gov/components/side-navigation/
- Ministry of Justice — side navigation (the flat always-open form):
  https://design-patterns.service.justice.gov.uk/components/side-navigation/

Casing and content style:

- Microsoft Style Guide — sentence-style capitalization:
  https://github.com/MicrosoftDocs/microsoft-style-guide/blob/main/styleguide/capitalization.md
- Google Material 3 — UX writing best practices:
  https://m3.material.io/foundations/content-design/style-guide/ux-writing-best-practices
- GOV.UK style guide — capitalisation:
  https://www.gov.uk/guidance/style-guide/a-to-z-of-gov-uk-style
- Apple Style Guide — title-style capitalization:
  https://support.apple.com/guide/applestyleguide/
- Mailchimp content style guide — title case for main navigation:
  https://github.com/mailchimp/content-style-guide

The research record:

- Nielsen Norman Group — Hamburger Menus and Hidden Navigation Hurt UX
  Metrics: https://www.nngroup.com/articles/hamburger-menus/
- Nielsen Norman Group — Left-Side Vertical Navigation:
  https://www.nngroup.com/articles/vertical-nav/
- Nielsen Norman Group — Accordion Icons (the caret finding):
  https://www.nngroup.com/articles/accordion-icons/
- UX Movement — Where to Place Your Accordion Menu Icons (leading beats
  trailing in task time):
  https://uxmovement.com/navigation/where-to-place-your-accordion-menu-icons/
- GitLab Design System — accordion (leading icon for a constant click
  position): https://design.gitlab.com/components/accordion
- Inside GOV.UK — making the accordion more accessible (chevron plus
  visible text):
  https://insidegovuk.blog.gov.uk/2021/10/29/how-we-made-the-gov-uk-accordion-component-more-accessible

Zero-script mechanics:

- GitHub — details-menu element (production disclosure on details):
  https://github.com/github/details-menu-element
- GitHub Primer CSS — the details reset:
  https://github.com/primer/css/blob/main/src/utilities/details.scss
- Scott O'Hara — details and summary, the accessibility profile:
  https://www.scottohara.me/blog/2022/09/12/details-summary.html
- Interop 2025 — find-in-page auto-expands details in every engine:
  https://github.com/web-platform-tests/interop/issues/491
- GitLab — sidebar collapse state stored in a cookie:
  https://gitlab.com/gitlab-org/gitlab/-/merge_requests/110868
