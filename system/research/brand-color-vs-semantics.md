# Brand Color vs. Semantic Color — the red/green problem

> Research briefing. Sources are cited inline where claims are made and listed at
> the end. The recommendation at the close is pending adoption into the operating
> documentation.

## The question

A company adopting a design system may bring a brand color that is exactly one of
the meaning-carrying hues. A green-brand enterprise collides with success; a
red-brand enterprise collides with danger and destructive actions. When an
application is skinned in an adopter's brand, what happens to "red means danger,
green means success"? Two options present themselves: find a new way to present success and danger and free those hues for
branding, or protect the semantic hues and refuse them as brand colors.

## Why this is a real problem

In this system color is a language with three separate jobs. The neutrals carry the
surfaces, the accent carries interactivity (the primary action and the
active/selected state), and the semantic set carries outcome (success, warning,
danger, info). The whole design holds together because each job has its own lane.
A brand color entering the app takes the accent lane — and when that brand hue is
red or green, two lanes suddenly speak the same word. A red primary button reads as
destructive; a green "Save" button reads as "already succeeded"; a red active-nav
state reads as an error the user should investigate. In dense analytical
screens this is worse than cosmetic: users scan tables by color, and a false
danger signal has a real cost in attention.

## The fact that settles most of the argument

About 8% of men (and ~0.5% of women) have red-green color vision deficiency — the
most common form of colorblindness. For them, brand-red and danger-red were never
distinguishable from each other, and neither was red from green. This is why WCAG
SC 1.4.1 (Use of Color) exists: color must never be the only carrier of meaning.
Any system that lets a bare patch of red or green carry the message is already
broken for one user in twelve, brand collision or not. The consequence: in this
system, semantics are always a compound signal — a shape (badge, alert bar, edge
marker), an icon or dot, and a word, with color as reinforcement. Once that rule is
absolute, the collision loses most of its teeth, because meaning survives even
where hue is ambiguous.

## Option A — reinvent success/danger, free the hues for brand

Present outcomes without relying on red/green at all: neutral badges with strong
icons and words, position and weight doing the work, perhaps blue/orange as the
outcome pair (as some trading platforms do for colorblind modes). Strengths: the
brand gets its color everywhere with zero ambiguity; one less constraint in sales
conversations. Weaknesses: it fights forty years of interface convention — users
arrive trained; green-check and red-alert are read pre-attentively, and giving that
up measurably slows scanning in dense tables; every competitor's app will still
speak the convention; and the system becomes harder to reason about, because
"danger" now looks different from everything the user knows. This is a high price
paid on every screen to solve a problem that exists only for some brands.

## Option B — protect the semantic hues, constrain the brand

Keep green=success and red=danger untouchable, and refuse red/green brand accents
(offer the brand a secondary from its palette instead). Strengths: maximum clarity,
zero retraining, simplest system. Weaknesses: it is commercially naive — an
enterprise whose identity is red will not accept a blue product; buyers expect
their brand in the chrome, and a forbidden brand color is a hard constraint to
defend in a sales cycle. The market itself disproves the necessity: widely used
red-branded applications still present red error states, and display negative
figures in red beside red chrome. They survive because of role separation, not
hue exclusivity.

## The recommendation — a third path: role separation plus hue distancing

Keep the convention and admit the brand, but make the collision structurally
harmless. Concretely, four rules. First, semantics are always compound (the rule
above): success/warning/danger/info ship only as badge, alert, or edge-marker
shapes with icon-or-dot plus word — a bare colored word or fill is forbidden, so
meaning never depends on telling two reds apart. Second, hue distancing: the brand
accent and the semantic hue near it must be tuned apart in lightness and chroma —
a red brand accent sits as the adopter's exact identity red while danger uses the system's
contrast-solved danger steps (different lightness, different saturation), and the
palette contract's per-theme steps make this a solvable, checkable math problem,
not taste. Third, role placement: the accent appears only in interactive positions
(primary pill, active nav, selection) and semantics only in outcome positions
(badges, alerts, markers, edge bars) — position alone disambiguates "red button =
the brand's main action" from "red badge = overdue". Fourth, the destructive-action
exception: when the brand accent is red, the danger button variant must not be a
solid red fill (it would impersonate the primary); it becomes outline + icon + word,
and the confirmation dialog carries the weight. One extra note for financial data:
gain/loss coloring in tables is a fifth lane; pair it with sign and directional
glyphs (+/−, ▲▼) so a green or red brand never corrupts a P&L column, and remember
some markets (East Asia) invert the red/green market convention entirely — one more
reason numbers never rely on hue.

In token terms this costs almost nothing: a brand skin re-points only
`--color-action` (and its hover/active/focus companions); the semantic aliases are
untouchable by brand skins; the lint can enforce that a `[data-brand]` block
touches no `--color-success/warning/danger/info` alias. The duality then becomes a
strength of the method: a system built this way accepts any brand color, including red
and green, because meaning in the interface is never carried by color alone.

## Sources

- Nathan Curtis, Color in Design Systems (EightShapes) — feedback-color sets as a
  deliberate, separate lane: https://medium.com/eightshapes-llc/color-in-design-systems-a1c80f65fa3
- Cieden, How to choose system colors — red/green brands can coexist with semantic
  colors; conventions are defaults, not laws: https://cieden.com/book/sub-atomic/color/system-colors
- W3C WCAG SC 1.4.1 Use of Color — color must not be the sole visual means of
  conveying information: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- PaletteRx, Designing error/warning/success colors: https://paletterx.com/blog/color-for-error-and-success-states
- UXPin, Color consistency in design systems: https://www.uxpin.com/studio/blog/color-consistency-design-systems/
