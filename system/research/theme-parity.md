# Theme Parity — System-First Dark and Light

> Research briefing. Sources are cited inline where claims are made and listed at
> the end. The doctrine below is encoded in the operating documentation and in
> `tokens.css`.

## The doctrine: system-first, two equal citizens

Most applications ship one good mode and one afterthought — and users trapped in
the weaker mode meet unreadable sections, text too close to its background, and
washed-out controls. The position taken here is different: the operating system's
preference leads (`prefers-color-scheme`), an explicit user choice overrides it,
and dark and light are exact equals. There is no "primary" mode and no "derived"
mode. People differ — some prefer dark, some light, many follow ambient light
through the day, letting the OS switch at sunset — and a system that respects
users respects that choice at every level. Every component, every token pair, and
every screen must be excellent in both modes, verified in both modes.

The preference cascade has three levels: the OS setting is the default; a stored
per-user choice (a preferences row, rendered server-side as `data-theme` — no
flash of the wrong theme on load, because the server already knows) overrides the
OS; and nothing else does. Best practice is unambiguous that users must keep
control of the toggle (Uxcel, principle 12).

## Why parity requires re-solving, not inverting

Simply flipping a light palette produces a broken dark one; contrast does not
survive inversion (Uxcel; Atmos). Dark mode is a second design problem sharing
the same structure, which is exactly what the palette contract provides: the same
named steps, re-pointed per theme, with every text and UI pair contrast-solved
per mode. The semantic hues already follow this rule — different steps per theme,
each individually verified — and any new family must too.

## The craft rules, both directions

Dark mode has failure modes of its own, and the research is consistent about
them:

1. Never pure white text on dark. Bright white on a dark field glows — the halo
   effect (halation) — and the full expert evidence is laid out in the dedicated
   section below. The remedy is an off-white: the system's dark-mode text is a
   light gray, never `#ffffff`.
2. Never pure black canvas. White-on-black contrast is harsh enough to hurt;
   published guidance recommends a dark gray in place of true black — the widely
   cited reference value is `#121212` (Material Design, via Uxcel and Atmos).
   The system's canvases sit near-black, never at `#000000`.
3. Desaturate on dark. Saturated colors optically vibrate on dark fields and
   often fail the 4.5:1 contrast test there; guidance suggests roughly 20 points
   lower saturation in dark mode (Atmos). The semantic hues here are desaturated
   by design and re-solved per theme.
4. Elevation is lightness, not shadow. On dark surfaces, shadows disappear;
   depth comes from a surface ladder where raised is lighter and sunken is
   darker (Uxcel; Atmos) — the ladder this system uses in both modes, which is
   one reason its dark and light can be true equals.
5. Light mode has its own version of rule 1: pure black text on pure white is
   needlessly harsh at high brightness; near-black ink on a soft off-white
   canvas reads longer with less fatigue.
6. Contrast law is mode-independent. WCAG thresholds (4.5:1 text, 3:1 UI) apply
   identically in both modes; each mode is verified separately, never assumed
   from the other.
7. Focus must survive both modes. The focus ring color is re-pointed per theme
   so keyboard visibility never degrades in either.
8. Test where users live: low light and bright light, high brightness and low,
   both modes (Uxcel). A mode that is only comfortable in the lighting it was
   designed in is half finished.

## Deep dive: text color on dark — the halo problem

The complaint is common and real: white text on a dark screen appears to glow,
with a halo bleeding around each letter, and reading becomes tiring — worse at
high screen brightness. The expert record on this is unusually consistent, from
the platform specifications to the researcher behind the next-generation
contrast standard.

The mechanism. In dark mode there is less overall light, so the pupil dilates;
a wider pupil makes the eye more susceptible to optical aberrations, so bright
glyphs scatter and blur (Nielsen Norman Group). For people with astigmatism the
effect is stronger: the widely cited statement from a University of British
Columbia perception researcher holds that roughly half the population has some
measurable astigmatism, and for them white-on-black text visibly fuzzes because
the dilated pupil lets the lens deformation dominate focus (Harrison, via
Oddie, 2008). The APCA work adds that severity varies with eye age, display
technology, ambient adaptation, and — often overlooked — sheer monitor
luminance (Somers).

What the authorities prescribe. The Material Design dark-theme specification is
explicit about the cause: pure `#FFFFFF` "would visually vibrate against dark
backgrounds" and "can harm legibility since the light from that text appears to
bleed or blur against the dark background"; its remedy is white at 87% opacity
for high-emphasis text on the `#121212` surface (an effective `#E0E0E0`), 60%
for secondary (≈ `#A0A0A0`), 38% for disabled. A leading email product's design
team lands almost identically — 90% white for primary text, 65% for secondary —
naming halation and eye fatigue as the reason. Apple's system label colors tell
the same story from another platform: the secondary, tertiary, and quaternary
labels are built on an off-white base (`#EBEBF5` at falling opacities), and the
platform guidance warns that high contrast "can cause visual discomfort" for
dark-adapted eyes. The deepest technical account comes from the author of APCA,
the candidate contrast method for the next accessibility standard: the current
standard's contrast math "doesn't work in dark mode" — it over-reports
light-on-dark contrast, scoring white-on-near-black as excellent when it is
perceptually harsh — and maximum contrast is explicitly harmful ("everything
looks like it has a glow around it"); APCA is experimenting with a contrast
ceiling, not just a floor, around its Lc 85–90 band.

The resulting rule, as adopted here. Dark-mode body text lives in an off-white
band of roughly 87–92% lightness — effective values from about `#DEDEDE` to
`#EBEBEB` on a `#121212`-class surface — never pure white; brighter steps up to
about `#F5F5F5` are reserved for small accents, and `#FFFFFF` for nothing.
Secondary text sits near 60% effective lightness while staying at or above the
4.5:1 floor, which remains the non-negotiable minimum in both directions —
contrast has a ceiling in dark mode, but never a basement. The system's tokens
already conform: the four families' dark-mode text steps (`#e9e6dd`,
`#e8ebf1`, `#e8e8e8`, `#dce9f6`) sit at the upper edge of the recommended band, their
muted steps hold above the accessibility floor rather than falling to the 38%
disabled level, and the achromatic accent tops out at `#f5f5f5`. One point of
honest nuance from the record: for fully sighted readers in good light, dark
text on light still measures as more readable overall (Nielsen Norman Group) —
which is an argument for system-first parity, not for preferring either mode.

## How the tokens implement it

`tokens.css` carries one alias set and three mappings: a fallback mapping (dark),
a light mapping under `[data-theme="light"]`, and a `prefers-color-scheme: light`
media block that applies the light mapping when no explicit `data-theme` is set —
so the OS leads by default and a stored user choice wins when present. The same
pattern covers every palette family. Components never know which mode they are
in; they read semantic aliases, and the cascade does the rest.

## Sources

- Material Design dark theme specification — #121212 surface, 87/60/38% text
  opacities, the anti-pure-white rationale:
  https://m2.material.io/design/color/dark-theme.html and
  https://codelabs.developers.google.com/codelabs/design-material-darktheme
- Nielsen Norman Group, Dark Mode vs. Light Mode (Budiu, 2020) — pupil
  dilation mechanism, light-mode readability findings, recommendation to let
  users choose: https://www.nngroup.com/articles/dark-mode/
- Andrew Somers on APCA and dark mode — WCAG 2 over-reports light-on-dark;
  halation from excess contrast; experimental contrast ceiling:
  https://medium.com/@colleengratzer/how-apca-changes-accessible-contrast-with-andrew-somers-3d47627a5e16
  and https://github.com/Myndex/SAPC-APCA/discussions/74
- The astigmatism/halation statement (Harrison, UBC Sensory Perception and
  Interaction Research Group, 2008, via Oddie):
  https://tatham.blog/2008/10/13/why-light-text-on-dark-background-is-a-bad-idea/
- Apple Human Interface Guidelines — Dark Mode and Color; system label colors
  on an off-white base: https://developer.apple.com/design/human-interface-guidelines/dark-mode
- Superhuman design team — 90%/65% white text, halation and eye fatigue, OLED
  black-smear note: https://blog.superhuman.com/how-to-design-delightful-dark-themes/
- Atmos, Dark mode UI best practices — halation and astigmatism, #121212,
  ~20-point desaturation, lighter-is-higher elevation:
  https://atmos.style/blog/dark-mode-ui-best-practices
- Uxcel, 12 principles of dark mode design — no direct inversion, pure-black and
  pure-white cautions, WCAG in dark mode, user control of the toggle:
  https://uxcel.com/blog/12-principles-of-dark-mode-design-627
- W3C WCAG 2.2 — contrast minimums apply in every mode:
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- MDN, prefers-color-scheme — the system preference media feature:
  https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-color-scheme
