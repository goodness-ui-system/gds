# Selection controls — checkbox, radio, switch, and the wider choice family

Research note. Named products and sources are cited here because this folder is
the one place citations are allowed; operating documents stay generic. Live
renderings of every candidate discussed here are in the white paper's Selection
controls chapter and in the specimen.

## The question

Every screen asks its reader to choose: which rows, which options, on or off,
this scope or that one. A small family of controls answers those questions —
checkbox, radio button, switch, segmented control, toggle button, chips, tiles,
dropdowns — and every design authority draws the lines between them a little
differently. What are the real rules, where do the authorities genuinely
disagree, and what should a server-rendered, zero-JavaScript system adopt?

## Two axes organize the family

Almost every rule in this domain falls out of two questions:

1. The shape of the choice — exactly one of a set, zero-or-more of a set, or a
   single yes/no.
2. The moment of effect — does the choice act the instant it is made, or is it
   collected now and applied when a form is saved?

One-of-a-set maps to the radio family (radio group, segmented control, select,
option tiles); zero-or-more maps to the checkbox family (checkbox group, choice
chips, multi-select); a lone on/off maps to the checkbox when deferred and the
switch when immediate. Most documented misuses are a control sitting in the
wrong cell of that grid — above all the switch inside a form that ends in a
Save button.

## The checkbox

The checkbox predates computing — it descends from paper forms and ballots —
and its screen meaning has been stable since the first graphical interfaces:
each box is an independent yes/no, so a group of them means choose any number.
Jakob Nielsen codified the web version of the rule in 2004: checkboxes for
zero-or-more, radio buttons for exactly-one, and no mixing of the two jobs.

The submission contract matters for a server-rendered system: an unchecked
native checkbox submits nothing at all. The server must treat an absent name as
false, always; the alternative workaround (a hidden companion input) creates
two sources of truth for one answer.

A lone checkbox is the opt-in control, and it carries a wording rule every
authority repeats: label it positively. A checkbox reading "Do not send
notifications" forces the reader through a double negative to work out what
unchecking means. The sharper test comes from the US Web Design System: the
label must make both states obvious — what checked means and what unchecked
means. Sara Soueidan's analysis of the yes/no question adds the deciding
factor: when the negative answer is itself information that must be recorded
(declarations, eligibility), an unchecked box is indistinguishable from "did
not answer", so the question needs two radio buttons instead — three states
(yes, no, unanswered) instead of two.

The mixed state — the dash in a parent checkbox standing over a partly-selected
set — turns out to be one of the least honest corners of the web platform. The
native flag for it is reachable only from script: there is no HTML attribute,
and the checkbox still submits as simply checked or unchecked. Worse, the
tempting server-side shortcut — writing the checked-state ARIA attribute onto a
native checkbox — is explicitly forbidden by the W3C's ARIA-in-HTML rules: the
native state wins, and some screen readers announce the state twice. The
consequence for a zero-script system: a mixed checkbox can be drawn as a visual
state, but where "partly checked" must genuinely reach assistive technology,
the honest control is a server-rendered select-all button, not a tri-state
checkbox.

## The radio button

The radio button is named after mechanical car-radio preset buttons — pressing
one physically released the previous one — and shipped with the earliest
graphical interfaces. Its contract: exactly one of a visible set, and choosing
one releases the others.

It carries an asymmetry that shapes the biggest debate about it: once any
option is chosen, the group cannot be returned to "no answer" — there is no
un-choose. From that asymmetry two schools grew:

- Always pre-select. Nielsen Norman Group's long-standing position: a radio
  group should ship with a default chosen, because an empty group is a state
  the control was never meant to have, defaults are demonstrably sticky
  (observational research finds most users keep them), and a preselected group
  can never fail validation.
- Never pre-select. The GOV.UK Design System and its family (NHS, ONS, UK
  Parliament): a preselected answer gets submitted unread and silently becomes
  wrong data, and the no-un-choose asymmetry makes a mistaken preselection
  unrecoverable. Government services testing found exactly this failure. For
  consent specifically, the law settles it: the European Court of Justice ruled
  in Planet49 (2019) that pre-ticked consent is not consent.
- The middle: Microsoft's Windows guidelines — preselect the safest, most
  private option; when no default is defensible for safety, security, or legal
  reasons, ship the group empty and enforce with validation.

Much of the war dissolves on one distinction: an edit screen re-rendering the
saved value is displaying state, not preselecting — every school accepts it.
The debate only genuinely applies to first-time questions.

Secondary radio rules with unusually broad agreement: stack options vertically
(a horizontal row makes it ambiguous which label belongs to which control —
strong expert consensus, though the often-cited "scanning studies" turn out to
be thinner than folklore suggests); order options logically rather than
alphabetically (alphabetical order changes under translation); and when no
option may truthfully apply, add an explicit escape — "None of these" — last,
after a divider, because GOV.UK research found users unsure whether leaving
everything unchosen was allowed.

Where the set gets long, authorities agree a dropdown takes over but disagree
on the number: Shopify Polaris says consider a select from four options;
Baymard's e-commerce testing says radios under five; Nielsen Norman Group and
the US Web Design System say radios under about seven; Microsoft's older
guidance says up to seven or eight; GOV.UK refuses a number and calls the
select a last resort at any count. The honest reading: two to five is always
safe for radios, six to eight is contested, nine-plus is never radios.

## The switch

The switch descends from the physical light switch by way of the iPhone's
skeuomorphic settings screens, and it carries the family's one extra promise:
the effect happens the moment it flips. On that promise there is remarkable
consensus — at least nine major authorities state it in near-identical words
(Nielsen Norman Group, Apple, Google's Material Design, Microsoft, IBM Carbon,
GitLab, GitHub, Adobe Spectrum, the UK Intelligence Community system):
a switch acts immediately, needs no Save, and therefore never belongs inside a
form that ends in a submit button. Microsoft's phrasing is the cleanest — the
checkbox is for status, the switch is for action. A switch beside a Save button
misleads twice at once, and it is the single most-cited anti-pattern in this
domain; a well-known code-review platform had to retro-fix production settings
pages from switches back to checkboxes.

Around that consensus, four genuine disputes:

1. The abolitionists. Adam Silver, Axess Lab, and (by omission) GOV.UK and the
   US Web Design System argue the switch should not exist on the web: its
   state-versus-action ambiguity ("is this on, or does pressing turn it on?")
   is unfixable, observed user testing shows people pausing to ask exactly that
   question, and an honest immediate-effect control quietly mandates scripting
   and network calls with failure modes a form never has. The strongest
   counter-evidence comes from inside government itself: a UK video-appointment
   service ran five rounds of user research on live camera and microphone
   controls and found toggles beat buttons and radios for users with low
   digital confidence — yet the component remains unpublished in GOV.UK's
   system, gated on its no-JavaScript doctrine.

2. The labeling schism. Everyone agrees the label names the thing being
   switched and never changes with state; the split is over state words. One
   school (Apple, GitHub, the majority of systems surveyed — 70% put no words
   inside the control) bans embedded ON/OFF entirely: the words collide with
   the state-versus-action ambiguity and break under translation. The other
   (Microsoft, the UK Intelligence Community system) recommends a separate
   state word beside the control, precisely because thumb position and fill
   alone fail users who never learned the convention. Both agree on the floor:
   state is never conveyed by color alone.

3. The role dispute — and how the evidence moved. The ARIA switch role exists
   so assistive technology can announce a switch instead of a checkbox, and
   the influential 2021 testing rounds (Adrian Roselli, Scott O'Hara) found
   support inconsistent enough that practitioners recommended a plain styled
   checkbox. The picture has changed since: the largest holdout screen reader
   fixed its handling in its 2023.1 release (it now genuinely says "switch,
   on/off"), and the major component vendors — Microsoft's Fluent, Google's
   Material, Adobe's React Aria — have all converged on exactly one markup: a
   native checkbox carrying the switch role, with the checked state left
   native (writing the checked-state ARIA attribute alongside is both
   forbidden and harmful). The worst remaining failure mode is a correctly-
   stated checkbox. The native switch attribute HTML has been growing
   (shipped in one browser engine, still unmerged in the standard, with no
   formal accessibility mapping yet) is the eventual clean answer and is
   harmless to include alongside the role today — but alone it would leave
   most screen readers hearing a checkbox. One meta-finding deserves record:
   the public per-pairing evidence here is thin and dated — the community
   support-tracking site has never published switch-role test data, so the
   freshest public utterance matrices are a personal test page from 2021 and
   a 2025 retest of the pressed-button pattern.

4. The reversal. Shopify's B2B design system spent a decade refusing a switch
   (its maintainers' rule: dirty state needs a checkbox and a Save; instant
   persistence earns a toggle), shipped a button-based "setting toggle"
   pattern instead, deprecated it, and then shipped a real switch in its next
   platform — evidence that even mature systems flip on this question, and
   that the underlying tension (honest form semantics versus glanceable
   instant state) does not fully resolve.

Regulators have also entered: the US FTC's dark-patterns report flags
confusing toggle settings that lead users into unintended privacy choices, and
pre-enabled consent switches are invalid under European law. A system's usage
policy can reasonably ban: default-on consent switches, negated labels where
off looks protective but is not, and any switch whose flip is not actually
persisted immediately.

## The segmented control

The segmented control — one-of-few as adjacent buttons — was born on the Mac
as "a compact alternative to a group of radio buttons" and became canonical in
iOS. Its central discipline is the tabs rule, stated independently by Apple,
IBM, Workday, and others: tabs switch views; a segmented control changes a
value or how the same data is presented. Dressing one as the other teaches
readers the wrong reflex. A corollary from GitHub's system: if each option has
its own URL, it is navigation — render links.

Count rules converge: two to five segments (Apple allows up to seven on wide
desktop layouts; GitHub allows six icon-only), noun labels of one to three
words, all text or all icons but never mixed, and a single-select segmented
control always has a value — if "nothing selected" is meaningful, the control
is a radio group in a form, not a segmented control.

Under the hood, four schools disagree about what the control is:

- A radio group in button clothing (Apple's original framing, Google's web
  implementation, Adobe's React Aria): real radio semantics, arrow keys move
  the selection. This is the only school compatible with zero scripting —
  hidden native radio inputs, styled labels — and the one adopted for the
  candidate on display.
- Toggle buttons (pressed-state buttons): the only model that extends to
  multi-select, at the cost of hiding the one-of-N relationship from
  assistive technology.
- Tabs (IBM's "content switcher" is literally tab markup): honest when
  segments genuinely swap a panel, a semantics lie otherwise.
- A plain list of buttons (GitHub): no borrowed pattern at all, every segment
  its own tab stop, on the argument that all three borrowed grammars mislead
  someone.

One hazard follows from radio semantics and matters to this stack: arrow keys
select as they move, so a segmented control that fires a server request on
every change fires on every arrow press. Accessibility guidance (the W3C's
documented failure F37, echoed by the US Web Design System's "avoid
auto-submission" warning) allows change-triggered updates only when they are
inline and non-disruptive — anything heavier needs an explicit Apply.

The empirical record favors the radio implementation strongly: community test
data shows native radio groups are the one composite in this family with a
flawless score — every tested screen reader announces the role, the state, and
the position in the group ("2 of 3"), and every tested voice-control tool
activates them by their visible label. The pressed-button implementation
announces independent buttons with no group relationship at all, and the tab
implementation needs scripting by construction.

The pattern's health is worth recording: Google deprecated its segmented
button in the 2025 Material update in favor of a renamed equivalent, and a
ride-hailing company's design-system audit famously found fourteen divergent
segmented-control implementations across ten products — evidence that one
visual pattern serving values, views, filters, and actions breeds drift unless
the system splits the jobs by name, which is what the tabs rule does.

## The toggle button

A toggle button is a button that stays pressed — on/off wearing a button's
clothes: watch this view, bold this text, show archived. Its state is the
pressed attribute, which a server can render without any script, and it comes
with the family's subtlest rule, stated by the W3C pattern and backed by Sarah
Higley's cross-screen-reader testing: the accessible name never changes while
the state flips. "Watch, pressed" is announced reliably; a button that flips
both its word and its state at once leaves the listener unsure which was
announced. Nielsen Norman Group publishes the opposite advice for two-state
action buttons (change the label: Start recording / Stop recording) — the
reconciliation, due to Heydon Pickering, is that those are two different
controls: a state control keeps its name and takes the pressed attribute; an
action pair changes its name and must not claim a pressed state; never both at
once. The icon-only toggle inherits the star problem — does a filled star mean
"starred" or "press to star"? — which is why the labeled form is preferred
where space allows, and why the pressed look must change more than color.

The pressed-button pattern's reputation as the safest toggle semantics also
needs a current-day asterisk: a 2025 community retest found one major desktop
screen reader announcing nothing at all when a pressed state changes under its
standard activation command — the on-paper-safest pattern currently carries
the worst live state-change defect. One large platform's design system moved
its switch from the switch role to the pressed button in 2023 on accessibility
advice; the 2025 data complicates that trade rather than settling it. The
honest conclusion: state vocabularies differ by screen reader (pressed, on,
selected, checked), so a label must read correctly under any of them, and
support claims need a last-verified date.

## The wider relatives

The dropdown select. The sharpest school split in the family. GOV.UK, on
recorded user research (users unable to close the list, typing into it,
confusing focus with selection, missing scrollable options — the "Burn your
select tags" findings), calls the select a last resort and tells teams to
restructure the question first. The pragmatists (Shopify, Apple, Microsoft,
IBM) treat a defaulted dropdown as a legitimate space tool for four-to-fifteen
options. Both are right about their own users: the research base behind the
ban is infrequent, low-digital-confidence citizens; a data-dense professional
tool serves experts who amortize the learning cost, and screen space is a
first-order constraint there. Two points are uncontested: never a select for
two or three options, and the multiple-selection variant of the native select
is broken everywhere — GOV.UK bans it citing Sarah Higley's assistive-
technology testing; the replacement is a checkbox group (or, past roughly
fifteen options, a scripted filterable multi-select, which a zero-script
system defers).

Choice chips. Google's Material system positions chip sets as replacements for
checkbox lists and even radio groups in filter bars: horizontally compact,
selection doubling as an applied-filters summary, a checkmark carrying the
selected state beyond color. Its own guidance concedes the weakness — single-
and multi-select chip sets are indistinguishable to the eye, so they must
never mix on a page. GOV.UK conspicuously solves the same dense-filter problem
with small checkboxes instead, precisely to keep the signifier honest. Built
as real checkbox inputs under pill faces (as in the candidate on display),
chips keep native semantics and the argument reduces to the visual trade-off.

Option tiles. When each option needs a description, systems formalize the
radio-as-card: Salesforce's visual picker, IBM's selectable tile, the US Web
Design System's tile variants. Two safety rules follow the pattern everywhere.
The tile keeps a visible radio dot, because a bordered card alone does not
read as one-of-a-set. And nothing else interactive lives inside the selectable
surface — the automated accessibility rule against nested interactive
elements treats it as a serious failure; IBM's formulation is the workable
one: an inner link is acceptable only as its own separate click target, never
inside the label.

None-of-the-above. GOV.UK's researched pattern for checkbox groups: an
explicit exclusive "none" option, last, after an "or" divider, with its label
restating the question. Its scripted convenience (auto-unchecking the others)
degrades honestly: without script, the server validates that "none" and a real
option were not both submitted. The same research found users unsure whether
leaving all boxes empty was permitted — the explicit option removes the
ambiguity.

Table row selection. The enterprise systems agree: a leading checkbox column;
a header select-all whose third, mixed state means "some rows"; a bulk-actions
bar that appears with selection; a radio column when exactly one row may be
chosen. Adobe's React Aria documents the two interaction models — explicit
checkbox toggling versus desktop-style replace-with-modifier-keys — and the
pagination honesty rule: a header checkbox selects the page, and "select all
N matching" across pages is a separate, explicit act the server owns. Three
details from the deeper survey earn house-rule status. Every row checkbox
needs the row's identity in its accessible name ("Select Acme Corp", never a
hundred identical "Select row"s — the default in at least one major system).
The cross-page escalation ("All 50 on this page selected — select all 3,000
matching this filter") is the one pattern in this domain where a server-
rendered system is structurally stronger than a client-rendered one, because
the selection is already server state; the classic server-rendered admin
interfaces implement it with plain links and a live-region count. And the
header checkbox's mixed state hits the same platform wall as the parent
checkbox everywhere else — the honest degradations are a visible "12 of 50
selected" count beside an unchecked header box, or explicit select-all and
clear buttons in the toolbar instead of a header checkbox at all.

Read-only and disabled — the view-mode question. Record screens spend most of
their life in a non-editable view, and the platform is full of traps there.
The read-only attribute does not apply to checkboxes and radios at all — a
spec-level no-op. A disabled checkbox is skipped by the keyboard, exempted
from contrast requirements (audit tools deliberately never flag an unreadable
disabled control), and — the sharpest trap — submits nothing even when
checked, so a naive server that treats absent-as-unchecked silently wipes the
value. Three camps answer view mode. The discoverability camp keeps controls
focusable with advisory attributes — which, without script, leaves a control
that looks off but still operates: a lie. The read-only-as-first-class camp
(IBM's system, Adobe's) renders a full-contrast, keyboard-reachable,
non-operable field — but every shipping implementation achieves the
non-operability with script. The content camp (GOV.UK, research-backed)
never renders a dead control at all: in view mode the value is content — "
Notifications: on" in a summary list with a Change link. For a zero-script
system the content camp is the only fully honest default, with the disabled
control reserved for temporarily-unavailable options inside active forms,
paired with the server-side rule that a disabled field's value is never
inferred from its absence.

## Drawing the controls — the implementation schools

Three schools exist for making native inputs look like the system:

1. Tint the native widget: the accent-color property (universally supported
   since 2022) recolors the browser's own checkbox and radio with one
   declaration. Near-zero code and zero accessibility risk — high-contrast
   modes, print, zoom, and right-to-left rendering all keep working because
   nothing was overridden. The cost: no control over shape, border, glyph, or
   size ratio, and each browser draws its own version.
2. Draw on the input itself: strip the native rendering (appearance: none) and
   draw box, border, and glyph in CSS directly on the input element. Scott
   O'Hara's 2021 verdict made this the modern default over the older
   hidden-input-plus-styled-span technique, which is now understood as a
   legacy-browser fallback. Full visual control with intact native semantics —
   and full responsibility: high-contrast mode strips author backgrounds (a
   documented real-world failure took a major CMS's checkboxes invisible
   there), print drops backgrounds by default, and every state must be
   re-verified. The candidates on display carry the corresponding safety net:
   a forced-colors rule hands the drawn inputs back to the browser and carries
   selected states on system colors.
3. Hidden input under a drawn face: still the only technique for composite
   controls whose visuals genuinely are not the input's own box — the switch
   track, segmented labels, chip faces, tiles. Sara Soueidan's finding governs
   the hiding: the input must sit invisibly on top of its visual replacement,
   not off-screen, so touch-exploring screen-reader users find it where it
   appears to be.

Cross-cutting floors, all encoded in the tokens or the candidates: visible
focus on the styled face when the hidden input has keyboard focus; targets of
at least 24 pixels (with the GOV.UK observation that users click the box, not
the label — so the visible control itself stays generous); state changes never
by color alone; thumb and glyph motion wrapped in the reduced-motion media
query; and the validation pseudo-classes that fire only after interaction
(user-invalid) noted as a progressive nicety that never replaces the
server-rendered error.

## What the evidence is worth

Genuinely research-backed: GOV.UK's select failure modes and oversized
controls (recorded usability sessions); the video-service toggle research
(five rounds, pro-switch for live device controls); Sarah Higley's
assistive-technology testing of selects and of state announcements; Adrian
Roselli's and Scott O'Hara's switch-role support matrices; the community
per-pairing utterance data on native checkboxes and radios (flawless) and
pressed buttons (currently defective on one major pairing); GOV.UK's
none-checkbox research; the DWP finding that batch filtering beats live
filtering for caseworker screens; default-stickiness observations behind the
preselection debate. A freshness caveat belongs on the record: the public
switch-role evidence base has not been systematically retested since 2021,
and the community support site's switch entry is an empty stub.

Convention presented as law: every numeric threshold (radios-to-select at
five, seven, or eight; segment caps), the vertical-stacking "studies", and the
immediacy rule for switches itself — nine authorities state it, none cites a
controlled study. Convention this strong is still worth adopting; it should
just be documented as convention, which this note does.

## Clearing the group

A many-of-many group has a cost the family's catalog did not price: undoing.
Deselecting K active options costs K clicks, and the empty state is reachable
only by hunting each option down. The filter-usability record treats this as
a real defect — Baymard's e-commerce testing keeps finding that users need an
obvious way to reset applied filters and abandon interfaces where clearing is
manual labor, and Nielsen Norman Group's applied-filters guidance makes the
same demand: visible current state, one-gesture removal.

The remedy splits by the group's role. In a filter group, the empty set
already means "everything" — so the group gains a leading exclusive All
option, radio-like inside the checkbox group: selecting All deselects every
specific in one click, selecting any specific turns All off, and deselecting
the last specific snaps All back on, so the group is never blank and the
empty set is always labeled. This is the filter-chip convention across the
major platforms, and its form-side twin is documented research: GOV.UK's
checkboxes guidance ships the "None of the above" exclusive option for
exactly the same reason — a group whose none-state must be an explicit,
one-click answer. In a form group, where empty means "none chosen" rather
than "everything", the exclusive none option is the honest device where none
is a legitimate answer; a clear action covers the rest. And any group with
two or more active options exposes a clear action at its end — the universal
escape hatch. The long-list case (a table's selection column, a field
picker) already has its device: the tri-state select-all parent, with the
field panel's hide-all arithmetic as the reasoning on record.

One shape is rejected: All as an ordinary member that can sit active beside
specifics. "All + Documents" is unanswerable — everything, or just these? —
and every surveyed implementation makes the exclusivity strict. On a
zero-script stack the exclusivity is server logic by construction: each
press is one request carrying the next parameter set, and the server renders
the next true state.

## What this system takes from it

The white paper's Selection controls chapter renders the candidates and
records the working recommendation; the decision remains open until the
selection pass. In brief: the two axes decide the control; the switch exists
under the strict contract (immediate, standalone, never beside Save; a native
checkbox with the switch role plus the emerging native switch attribute, and
never a restated checked-state attribute); checkbox and radio ship in one of two
drawing options (native accent-color or custom-drawn — one to be chosen, not
both); the segmented control is hidden radios with the tabs rule and the
arrow-key caveat; the toggle button keeps a stable name; chips and tiles are
real inputs under styled faces; the mixed checkbox is visual-only with the
select-all button as the honest alternative; and the select stays the control
of last resort for one-of-many, with its multiple variant banned outright.
Group clearing is role-driven: filters get the leading exclusive All, forms
get the exclusive none where none is an answer, any group with two or more
active options gets a clear action, and All-beside-specifics is refused.

## Sources

Standards and platform:

- W3C ARIA Authoring Practices Guide — Checkbox, Radio Group, Switch, Button,
  Listbox patterns: https://www.w3.org/WAI/ARIA/apg/patterns/
- W3C — Using ARIA (First Rule of ARIA): https://www.w3.org/TR/using-aria/
- W3C — ARIA in HTML (aria-checked forbidden on native checkbox):
  https://www.w3.org/TR/html-aria/
- WCAG 2.2 Understanding — Non-text Contrast (1.4.11), Target Size (2.5.8),
  On Input (3.2.2, failure F37):
  https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html,
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html,
  https://www.w3.org/TR/WCAG20-TECHS/F37.html
- MDN — indeterminate is script-only:
  https://developer.mozilla.org/en-US/docs/Web/API/HTMLInputElement/indeterminate
- WebKit — An HTML Switch Control (the checkbox switch attribute):
  https://webkit.org/blog/15054/an-html-switch-control/
- WHATWG — switch attribute pull request:
  https://github.com/whatwg/html/pull/9546
- Open UI — Switch explainer: https://open-ui.org/components/switch.explainer/

The switch debate:

- Nielsen Norman Group — Toggle-Switch Guidelines:
  https://www.nngroup.com/articles/toggle-switch-guidelines/
- Adam Silver — Why toggle switches suck (and what to do instead):
  https://adamsilver.io/blog/why-toggle-switches-suck-and-what-to-do-instead/
- Axess Lab — Toggles suck!: https://axesslab.com/toggles-suck/
- Adrian Roselli — Switch Role Support:
  https://adrianroselli.com/2021/10/switch-role-support.html
- Adrian Roselli — Under-Engineered Toggles:
  https://adrianroselli.com/2019/03/under-engineered-toggles.html
- Scott O'Hara — aria-switch-control test results:
  https://github.com/scottaohara/aria-switch-control
- Sara Soueidan — On Designing and Building Toggle Switches:
  https://www.sarasoueidan.com/blog/toggle-switch-design/
- GOV.UK backlog — Toggle switch component (the five-round video-service
  research): https://github.com/alphagov/govuk-design-system-backlog/issues/244
- USWDS — toggle discussion ("intended usage is a single checkbox"):
  https://github.com/uswds/uswds/issues/3229
- Shopify Polaris — why no switch, and the reversal:
  https://github.com/Shopify/polaris-react/discussions/7297,
  https://shopify.dev/docs/api/app-home/polaris-web-components/forms/switch
- FTC — dark-patterns report (confusing toggle settings):
  https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers

Checkbox and radio:

- Jakob Nielsen — Checkboxes vs. Radio Buttons (2004):
  https://www.nngroup.com/articles/checkboxes-vs-radio-buttons/
- Kara Pernice — Radio Buttons: Always Select One?:
  https://www.nngroup.com/articles/radio-buttons-default-selection/
- GOV.UK Design System — Radios, Checkboxes, Select:
  https://design-system.service.gov.uk/components/radios/,
  https://design-system.service.gov.uk/components/checkboxes/,
  https://design-system.service.gov.uk/components/select/
- Microsoft Win32 UX Guide — Radio Buttons (the safety-conditional middle):
  https://learn.microsoft.com/en-gb/windows/win32/uxguide/ctrl-radio-buttons
- Sara Soueidan — One Checkbox vs Two Radio Buttons:
  https://www.sarasoueidan.com/blog/one-checkbox-or-two-radio-buttons/
- GDS design notes — updated radios and checkboxes (users click the box):
  https://designnotes.blog.gov.uk/2016/11/30/weve-updated-the-radios-and-checkboxes-on-gov-uk/
- GDS design notes — letting users tick a "none" checkbox:
  https://designnotes.blog.gov.uk/2021/11/15/letting-users-tick-a-none-checkbox/
- Bird & Bird — Planet49: pre-ticked boxes are not consent:
  https://www.twobirds.com/en/insights/2019/global/planet49-cjeu-rules-on-cookie-consent
- Baymard Institute — Drop-Down Usability:
  https://baymard.com/blog/drop-down-usability
- Luke Wroblewski — Dropdowns Should be the UI of Last Resort:
  https://www.lukew.com/ff/entry.asp?1950=
- Alice Bartlett — Burn Your Select Tags (EpicFEL 2014):
  https://www.youtube.com/watch?v=CUkMCQR4TpY
- Sarah Higley — Select your poison (assistive-technology testing):
  https://www.24a11y.com/2019/select-your-poison/

Segmented controls and toggle buttons:

- Apple HIG — Segmented Controls, Toggles:
  https://developer.apple.com/design/human-interface-guidelines/segmented-controls,
  https://developer.apple.com/design/human-interface-guidelines/toggles
- GitHub Primer — Segmented Control (the plain-buttons school):
  https://primer.style/product/components/segmented-control
- IBM Carbon — Content Switcher (the tabs school), Toggle, Data Table:
  https://carbondesignsystem.com/components/content-switcher/usage/,
  https://carbondesignsystem.com/components/toggle/usage/,
  https://carbondesignsystem.com/components/data-table/usage/
- Material — segmented-button deprecation:
  https://github.com/material-components/material-components-android/blob/master/docs/components/ToggleButtonGroup.md
- Adobe React Aria — ToggleButtonGroup, selection models:
  https://react-spectrum.adobe.com/react-aria/ToggleButtonGroup.html
- Runi Goswami (Lyft) — A better segmented control (the fourteen-variants
  audit): https://medium.com/tap-to-dismiss/a-better-segmented-control-9e662de2ef57
- Sarah Higley — Playing with state (state beats name-change in testing):
  https://sarahmhigley.com/writing/playing-with-state/
- Heydon Pickering — Building Inclusive Toggle Buttons:
  https://www.smashingmagazine.com/2017/09/building-inclusive-toggle-buttons/
- Nielsen Norman Group — State-Switch Controls (the mute-button case):
  https://www.nngroup.com/articles/state-switch-buttons/

Relatives and implementation:

- Material Design 3 — Chips guidelines:
  https://m3.material.io/components/chips/guidelines
- Salesforce SLDS — Visual Picker (radio-cards on real inputs):
  https://github.com/salesforce-ux/design-system (visual-picker docs)
- Deque axe-core — nested-interactive rule:
  https://github.com/dequelabs/axe-core/blob/develop/doc/rule-descriptions.md
- Adam Silver — Form Design Patterns, filter chapter (material honesty,
  batch vs live filtering): https://github.com/adamsilver/fdpb
- DWP Design System — filters research (batch beats live for caseworkers):
  https://design-system.dwp.gov.uk/research/filters
- web.dev — CSS accent-color: https://web.dev/articles/accent-color
- Stephanie Eckles — Pure CSS Custom Checkbox Style:
  https://moderncss.dev/pure-css-custom-checkbox-style/
- Scott O'Hara — One last time: custom styling radio buttons and checkboxes:
  https://www.scottohara.me/blog/2021/09/24/custom-radio-checkbox-again.html
- Sara Soueidan — Inclusively Hiding and Styling Checkboxes and Radio Buttons:
  https://www.sarasoueidan.com/blog/inclusively-hiding-and-styling-checkboxes-and-radio-buttons/
- Drupal — Claro checkboxes unusable in forced-colors mode (the cautionary
  case): https://www.drupal.org/project/drupal/issues/3271305
- USWDS — Select ("avoid auto-submission"), checkbox wording rules:
  https://designsystem.digital.gov/components/select/,
  https://designsystem.digital.gov/components/checkbox/

Assistive-technology evidence, tables, and view mode:

- a11ysupport.io test data (native checkbox/radio flawless; pressed-button
  2025 retest; switch entry an empty stub):
  https://github.com/accessibilitysupported/a11ysupport.io
- NVDA 2023.1 changelog — switch role finally reported:
  https://github.com/nvaccess/nvda/issues/11310
- GitHub Primer — the 2023 move from switch role to pressed button:
  https://github.com/primer/react/pull/3510
- Scott O'Hara — per-pairing switch utterance tests:
  https://github.com/scottaohara/a11y_styled_form_controls
- MDN browser-compat-data — the switch attribute is single-engine,
  off standards track: https://github.com/mdn/browser-compat-data
- Carbon — data-table selection (tri-state header, batch bar):
  https://carbondesignsystem.com/components/data-table/usage/
- Shopify Polaris — selection across pages, bulk-action strings:
  https://polaris.shopify.com/components/tables/index-table
- Django admin — the server-rendered cross-page select-all:
  https://github.com/django/django (admin actions templates)
- Ministry of Justice frontend — progressive-enhancement multi-select:
  https://github.com/ministryofjustice/moj-frontend
- HTMX — bulk-update example (the zero-script table form):
  https://htmx.org/examples/bulk-update/
- WHATWG HTML — disabled and readonly applicability, entry-list
  construction: https://html.spec.whatwg.org/multipage/input.html
- Carbon — read-only states pattern (read-only is not disabled):
  https://carbondesignsystem.com/patterns/read-only-states-pattern/
- GOV.UK — check your answers pattern (view mode as content):
  https://design-system.service.gov.uk/patterns/check-answers/
