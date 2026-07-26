# Goodness UI Design System

> The honest foundation for your interface.

The public site + living documentation for **Goodness UI** — a design system whose
identity is built around the **Node monogram**: a “G” traced as a connected network,
constructed on a blueprint and kept honest by a single, fixed geometry.

This repository is a **static, no-build website**. Open `index.html` in a browser and
it runs — there is nothing to compile. It hosts for free on GitHub Pages.

## What’s inside

A persistent left-hand navigation frames a hero home page and every design document
produced so far:

| Section | Page | What it is |
| --- | --- | --- |
| Home | `pages/hero.html` | Animated hero — the G building itself on a blueprint, on a loop |
| Logo Guidelines | `pages/logo-guidelines.html` | Master geometry, avatar, logo on black/white, clear space, sizing, palette |
| Logo Exploration | `pages/logo-exploration.html` | The 5 original logo directions |
| Node Explorations | `pages/node-explorations.html` | 20 variations of the Node direction |
| Geometry Study | `pages/geometry-study.html` | Monochrome sweep of line weight & dot size |
| Midpoint · node 9 | `pages/geometry-midpoint.html` | The chosen final geometry (stroke 5 · node 9) |
| Blueprint Plate | `pages/blueprint-plate.html` | The 20 studies drawn as dimensioned construction plates |

## Locked decisions

- **Master mark geometry:** stroke `5`, node ⌀ `9` (18px), round caps, 8-node “G”, derived on `R62`.
- **Tagline:** *The honest foundation for your interface.*
- **Token prefix:** default `--gds-`, configurable, may be set empty in fully-owned codebases.
- **Logo color:** monochrome — one ink per ground (ink `#12253F` on light, `#FFFFFF` on dark).

## Palette

| Token | Value | Use |
| --- | --- | --- |
| Ink | `#12253F` | Logo on light |
| Paper | `#FFFFFF` | Logo on dark |
| Blueprint | `#0A2247` | Ground |
| Furniture | `#6BA8DE` | Construction guides |
| Linework | `#EAF3FF` | Blueprint marks |

## Run locally

```bash
# any static server works; e.g.
python3 -m http.server 8080
# then open http://localhost:8080
```

## Deploy

Pushing to `main` triggers `.github/workflows/pages.yml`, which publishes the site to
GitHub Pages. In the repo: **Settings → Pages → Build and deployment → Source: GitHub Actions.**

## Structure

```
gds/
├── index.html              # site shell (sidebar + hash router)
├── assets/
│   ├── css/app.css         # shell styles (blueprint theme)
│   ├── js/app.js           # tiny hash router, no dependencies
│   └── favicon.svg         # the mark
├── pages/                  # each design document (self-contained HTML)
└── .github/workflows/      # GitHub Pages deploy
```

---

© 2026 Goodness UI. All marks are vector.
