/*
 * Vertical-rhythm check — the enforcement for the air rule (R11).
 *
 * The rule: nothing begins flush against the end of the block before it.
 * Any element that starts a new block after another block must have air
 * above it (the base rhythm); the only sanctioned tight pairs are a
 * caption with the object it captions (a label, a heading, a legend) and
 * a component's own internal anatomy.
 *
 * Static lint cannot see rendered geometry, so this check renders every
 * page of the site and measures every adjacent sibling pair:
 *
 *   flagged  = vertically stacked, visible, closer than MIN_GAP px
 *   exempt   = inside a <table>; side-by-side or gap-managed flex/grid;
 *              a caption-ish first element (heading, label, legend);
 *              two elements of the block their parent owns (BEM anatomy —
 *              .scroll-study__chrome above .scroll-study__body is the
 *              component's own skeleton, not document flow)
 *
 * Run:  node enforcement/check_rhythm.mjs   (from system/, or repo root)
 * Exit: 0 clean, 1 any flush pair found.
 */

import { chromium } from "playwright";
import { fileURLToPath } from "url";
import { dirname, resolve } from "path";
import { readdirSync } from "fs";

const root =
  process.env.GDS_ROOT ||
  resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const MIN_GAP = 12;

/* Scope: the flowing documents of the linked site. The standalone plates
 * (logo studies, geometry plates, node explorations) are fixed compositions
 * where flush placement is the design — the air rule governs document flow,
 * not artwork. */
const pages = [
  "system/specimen.html",
  "system/whitepaper.html",
  "pages/hero.html",
  ...readdirSync(resolve(root, "pages/system"))
    .filter((f) => f.endsWith(".html"))
    .map((f) => "pages/system/" + f),
];

const walk = (minGap) => {
  const out = [];
  const blockOf = (el) => {
    const c = (el.classList && el.classList[0]) || "";
    return c.split("__")[0].split("--")[0];
  };
  const captionish = (el) =>
    /^H[1-6]$|^SUMMARY$|^LEGEND$|^DT$/.test(el.tagName) ||
    /(__label|__title|__key|__legend|__size|__sub|__hint|__error|eyebrow)/.test(el.className || "");
  const sel = (el) => {
    const c = (el.classList && el.classList[0]) || el.tagName.toLowerCase();
    const t = (el.textContent || "").trim().slice(0, 32).replace(/\s+/g, " ");
    return `${c} “${t}”`;
  };
  for (const el of document.body.querySelectorAll("*")) {
    const prev = el.previousElementSibling;
    if (!prev) continue;
    if (el.closest("table") || el.closest("svg")) continue;
    // items of one list are the list's own anatomy, not adjacent blocks
    if (/^(LI|DT|DD|OPTION|TR)$/.test(el.tagName)) continue;
    // form controls and their hints/errors are field anatomy, not blocks
    if (/^(INPUT|SELECT|TEXTAREA|BUTTON|LABEL)$/.test(prev.tagName)) continue;
    // a docked pair shares one line on purpose — the tab rail is the table's
    // top edge (components.md 2.6), the same sanctioned fusion as a section
    // stack rather than two blocks that forgot their air
    if (el.parentElement.classList && el.parentElement.classList.contains("tab-dock")) continue;
    // a run of the same component repeated is a designed fused stack
    // (switch-row after switch-row: the section law — flush, sharing a hairline)
    if (blockOf(prev) && blockOf(prev) === blockOf(el)) continue;
    // a classless run of one tag (stacked code chips) is one exhibit, not blocks
    if (prev.tagName === el.tagName && !el.classList.length && !prev.classList.length) continue;
    // when either side belongs to the parent's own block, the pair is that
    // component's anatomy (a brand slot above the sidenav's items)
    const pb = blockOf(el.parentElement);
    if (pb && (blockOf(el) === pb || blockOf(prev) === pb)) continue;
    // captions under their object (a size figure below a mark)
    if (captionish(el)) continue;
    // anything inside a drawn component frame (border or surface between the
    // pair and the document flow) is that component's interior, not flow
    let anc = el.parentElement, interior = false;
    while (anc && anc !== document.body) {
      if (/specimen__section|specimen__main|\bwrap\b/.test(anc.className || "")) break;
      const as = getComputedStyle(anc);
      if (parseFloat(as.borderTopWidth) > 0 || parseFloat(as.borderLeftWidth) > 0 ||
          (as.backgroundColor !== "rgba(0, 0, 0, 0)" && as.backgroundColor !== "transparent")) {
        interior = true; break;
      }
      anc = anc.parentElement;
    }
    if (interior) continue;
    const a = prev.getBoundingClientRect();
    const b = el.getBoundingClientRect();
    if (a.height === 0 || b.height === 0 || a.width === 0 || b.width === 0) continue;
    const ps = getComputedStyle(el.parentElement);
    if (/flex|grid/.test(ps.display)) {
      const gap = parseFloat(ps.rowGap) || 0;
      if (gap >= 8) continue;
      if (/^row/.test(ps.flexDirection) && ps.display.includes("flex")) continue;
    }
    const es = getComputedStyle(el);
    if (es.position === "absolute" || es.position === "fixed") continue;
    // inline-level elements are text flow wrapping across lines, not blocks
    if (es.display.startsWith("inline") || getComputedStyle(prev).display.startsWith("inline")) continue;
    // vertically stacked with horizontal overlap
    if (b.top < a.bottom - 2) continue;
    if (Math.min(a.right, b.right) - Math.max(a.left, b.left) <= 0) continue;
    const parentBlock = blockOf(el.parentElement);
    if (parentBlock && blockOf(prev) === parentBlock && blockOf(el) === parentBlock) continue;
    if (captionish(prev)) continue;
    const gap = b.top - a.bottom;
    if (gap < minGap) out.push({ prev: sel(prev), next: sel(el), gap: Math.round(gap) });
  }
  return out;
};

const browser = await chromium.launch({
  executablePath: process.env.RHYTHM_BROWSER || "/opt/pw-browsers/chromium",
});
const page = await browser.newPage({ viewport: { width: 1400, height: 1000 } });
let total = 0;
for (const rel of pages) {
  // domcontentloaded: geometry needs the stylesheet, not remote fonts —
  // a page importing web fonts must not stall the check behind the network
  await page.goto("file://" + resolve(root, rel), { waitUntil: "domcontentloaded" });
  await page.waitForTimeout(250);
  const flags = await page.evaluate(walk, MIN_GAP);
  for (const f of flags) {
    total += 1;
    console.log(`${rel}  gap ${f.gap}px  ${f.prev}  →  ${f.next}`);
  }
}
await browser.close();
console.log(`\nrhythm-check: ${pages.length} page(s) rendered, ${total} flush pair(s)`);
process.exit(total ? 1 : 0);
