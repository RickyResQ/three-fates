# Plan v4.1 — De-slop pass on the Three Fates page

**Status:** BUILT AND LIVE 2026-09-27 ~23:25 MST. Commit 146b949, pushed, live URL verified 200 with all markers present.
**Date:** 2026-09-27 ~23:15 MST

## Eric's review decisions (his words: "Cream background is not very sexy. Proceed with your call.")

- Background: KEEP the warm cream `#FFF1E5`. His own verdict tonight is that warm paper reads human; the "sexy" has to come from typography and confident color use, not a background swap. No background color change (also preserves the contrast-gate tuning).
- Open question 1 (FX shading as stepped area + axis + legend): YES, proceed.
- Open question 2 (all giant numerals to charcoal): YES, all of them.
- Open question 3 (approve/cut): approved as written, all 9 items.
**Trigger:** Reddit commenter called the page's "background shading" AI slop; Eric agreed and asked for a fix. Consult with the Muse improvement ideas side chat returned a ranked audit (read-only, nothing changed).

## What the audit found

The obvious suspects are already clean: no dark backgrounds, no mono fonts, no purple/blue gradients, no emoji bullets, no stock photos. The "dark full-bleed bridge section" was stale description — it renders on the same cream `#FFF1E5` as everything else. What remains are subtler template signatures, ranked below by impact.

## What stays (reads as human, do not touch)

- Verdict headlines per section, obit prose, the "Mesa, Arizona" dateline
- Specific methodology bullets, the colophon
- Double-rule and 3px ink section rules (genuine newsprint idiom)
- All chart accessibility work: colorblind-safe Okabe-Ito palette, dash patterns, keyboard-accessible charts, reduced-motion support

## Ranked fixes

### 1. Delete the film-grain overlay
The `<svg class="grain">` with feTurbulence fractalNoise covers the whole page (opacity .03, multiply blend). It's fake analog warmth; the paper feel already comes from the cream background. Delete the SVG block and its CSS rule. Zero data impact.

### 2. Kill the tracked-uppercase eyebrow labels (keep one)
~20 tracked-uppercase sans eyebrow labels scream template. Keep exactly one: the masthead `.kicker`. Convert the rest:
- `.obit h3` → Georgia italic, 16px, normal case, ink
- `.pullquote .attr` → Georgia italic, 14px, muted, no tracking
- Fold `.secnum` into the showmeta line or delete it
- Drop letter-spacing on `.badge` / `.mnum` to `.02em`

### 3. Giant numerals to ink
Giant stat numerals in five different colors (vermilion `#D55E00` for -87%, blue `#0072B2` for 4.0, gold `#B37400` for 7.3x, magenta `#A24D7E` for 9x) are the last color-discipline holdout. Set `.giantstat .n` and `.secstat-num` to `--ink` charcoal (~12.6:1 on cream). Show colors stay ONLY inside the SVG chart lines/dots.

### 4. Collapse the two parallel numbering schemes
Scrollytelling ACT I/II/III plus section I./II./III. reads as template scaffolding. Delete the Roman-numeral `.secnum` divs; replace ACT labels in the scrolly with plain serif-italic kickers ("The death", "The coronation"). Keep the moments-list 1/2/3 (those are functional links).

### 5. Quiz restyle: from widget to printed ballot
The quiz buttons are the generic "AI quiz widget" pattern (big rounded cards). Restyle as a printed ballot: block layout, max-width 560px, ink-bordered 4px-radius options, A/B/C rendered by a CSS counter in a 52px gutter.

### 6. Make the FX-research background shading an explicit data layer
The 14 background-shading rects (alpha 0.04–0.15) read as a decorative gradient wash even though they're real data (211 to 599 series) — this is very likely what the Redditor meant by "background shading." Make it honest: flat stepped area at ~0.16 alpha, plus a right-hand axis labeled "US scripted series" and a legend swatch. All data preserved.

### 7. Systematize border-radius
Current radius system reads generic-SaaS. New system: 4px for interactive controls/inputs, 6px for tooltip/scrubcard, 50% only for tiny legend dots.

### 8. Declutter hairline dividers
Delete the `.chartwrap` top/bottom borders and `.vizhead` border-bottom. Keep the 3px ink section rules and the moments-list hairlines.

### 9. Enlarge chart legend circles (public commitment 2026-09-27 ~23:12 MST)
u/Pirkale asked in the thread that the color-circle legend on the site be made as large as possible so it doesn't blend into the background. OP reply committed to it publicly. Bump legend dot size (keep 50% radius per fix #7) and verify the larger dots don't collide with labels at 390px.

## Hard constraints

- Single-file static page; no structural JS changes beyond deleting the grain SVG
- Every replacement color at 3:1 or better on cream `#FFF1E5`
- All data, charts, quiz, tap-to-spotlight, dash patterns, and reduced-motion behavior preserved
- Build from `build_page4.py` (or successor), commit + push, verify 200 + markers live

## Verification checklist (before Eric looks at it)

1. Contrast re-check: all text/accents ≥3:1 on cream (build-time gate)
2. Keyboard pass: chart markers, quiz options, tap-to-spotlight all operable
3. Reduced-motion pass: no animation, instant jumps
4. Mobile 390px read: no overlap, ballot options tappable
5. Stats check unchanged (twd_loss=87, bb_mult=7.3, got_finale_imdb=4.0, hotd_mult=9)
6. `node --check` on page JS

## Open questions for Eric

1. Fix #6 changes how the FX-research shading looks — okay to make it a flat stepped area with its own axis?
2. Fix #3 puts all giant numerals in charcoal — any stat you want to keep colored?
3. Approve the plan as written, or cut/adjust items?
