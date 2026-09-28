# Three Fates v4 — UI Redesign Plan

Date: 2026-09-27. Status: PLAN WRITTEN — pending council review, then Eric's review. NO BUILD until both.

## Why
Eric's verdict on the live page: "Colors make this hard to see" and "Is this what Muse improvement pointed you to for amazing UI?" Standing rule now encoded: outstanding only, never average. v3.2 added features; the visual design never got a review pass. This plan is that pass.

Research brief (design study of Pudding, NYT Upshot, Reuters, IIB winners, fable-index): in subagent handoff 2026-09-27.

## Design thesis
The page is a long-form editorial data story, not a dashboard. The best in the world (Upshot, Pudding, fable-index) share four moves we don't fully make: (1) type carries the page — two voices, giant hero numbers, everything else a whisper; (2) color encodes exactly one thing — the show — and never touches UI chrome; (3) rhythm over templates — varied pacing, not six identical sections; (4) annotations live on the data — labels inline on the chart, not in a list below.

## What changes (concrete)

1. **Typography discipline.** Two typefaces only: expressive serif (headlines, hero numbers, pull quotes — with true italics and oldstyle figures) and one quiet grotesque (labels, captions, UI). Giant stat numbers go bigger (up to ~140px, line-height 0.9), one number per mobile screen. Kill every third-voice style on the page.

2. **Color discipline.** Show accents (darkened 2026-09-27: TWD #D55E00, GoT #0072B2, BB #B37400, HotD #A24D7E, BCS #8C564B, Lost #9A7200) appear ONLY on data ink: lines, hero numerals, swatches, moment dots. All chart chrome (axes, gridlines, tick labels) goes quiet neutral. Audit and remove every place an accent leaked onto UI chrome.

3. **Rhythm over templates.** Break the six-identical-sections pattern. Promote each show's one-line verdict (we have them: "It did not die of quality...") to the section headline under the roman numeral. Alternate layouts: number-first for two shows, chart-first for two, so scrolling has a beat. Full-bleed comparison chart as a bridge between the three fates.

4. **Annotations on the data.** Inline the top 2 moments per chart as small numbered dots with hairline leader lines and 12px quiet labels (collision-checked against the v3.2 inflection callouts; moment markers win ties). Keep the full moments list below as a dated timeline; numbers match the chart. Clickable linking (v3.2) stays.

5. **Comparison chart.** Direct-label each line at its right edge; kill the legend. Tapping a show grays the other five (focus + context). Keep the dashed/dotted colorblind patterns — accessibility craft is a differentiator.

6. **Quiz.** Restyle as oversized tappable cards: serif question, instant payoff revealing a mini-chart instead of text-only.

## What does NOT change
All data, all v3.2 features (play animation, tooltips, toggles, callouts), single static file, no frameworks, no gradients, no emoji, no new dependencies. Stats check must still print twd_loss=87 bb_mult=7.3 got_finale_imdb=4.0 hotd_mult=9.

## Council review (2026-09-27) — 3 BUILD, 1 NO-BUILD-pending-proof. All fixes folded below.
- Grok: contrast gate before layout work — every accent ≥3:1 on the real background for data strokes, ≥4.5:1 for 12px labels. 12px labels that fail go quiet neutral, accent only on the dot/stroke.
- GPT: comparison-chart legibility is the hardest test and was missing from verification. Fix: build a real-size comparison-chart prototype (375px + desktop) as an approval gate — readable non-overlapping labels, all six series identifiable without color or tapping — Eric approves the artifact before full build.
- Gemini: alternating rhythm via CSS ONLY (flex-direction / grid-template-areas on nth-child(even)), DOM identical across all six sections, so v3.2 JS bindings can't regress.
- Anthropic: BB (#B37400) and Lost (#9A7200) are nearly the same hue — they blur together and the dash patterns don't help on numerals/dots/swatches. Fix: give Lost a distinct hue from the same Okabe-Ito family — darkened bluish-green #007A5E (checked clear of GoT #0072B2). Add a build-time contrast gate that fails the build if any show color is below 3:1 on the page background, plus a vision-deficiency (deuteranopia/protanopia) screenshot check on the comparison chart.

## Build verification
Build clean, stats check unchanged, node --check on extracted JS, contrast gate prints every accent's ratio and fails below 3:1, curl 200 + marker grep on the live URL, then a real mobile-viewport browser screenshot pass on the Lost and TWD sections AND the comparison chart (normal + vision-deficiency simulation) before calling it done.

## Open question for Eric
Scope guardrail: this is a visual redesign of the existing page. New content (new shows, head-to-head mode, report cards) stays parked for Phase B.
