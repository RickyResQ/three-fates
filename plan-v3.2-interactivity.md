# Plan: v3.2 per-show page interactivity (annotations, line animation, inflection callouts)

Date: 2026-09-27. Status: BUILT AND LIVE 2026-09-27 ~21:33 MST (commit d297c31). Eric reviewed plan and approved build; council 4/4 BUILD.
Council cost: $0.17 of the $25 cap (~$8.34/month spent).
Site: https://rickyresq.github.io/three-fates/ — static single file, GitHub Pages, no backend.
Build: ~/workspace/three-fates/build_page3.py -> index.html. Data: data.json (unchanged by this plan).

## Goal
Make the per-show pages feel like a story you experience, not a chart you look at. Three features from the Muse improvement ideas consult (Eric picked 1 + 3 + 4).

## Feature A: Clickable story annotations on key-moment markers
Current state: numbered circles on the chart (1, 2, 3) correspond to an ordered list below the chart with narrative text (MOMENTS dict, already written).
Change: tapping or clicking a numbered marker scrolls to its matching list item, highlights it briefly, and expands it. Clicking a list item highlights the matching marker on the chart. Keyboard accessible (markers become <button>-like focusable elements).
Why: closes the loop between chart and story; the thread's liveliest debates are about causes, not numbers.
Effort: small. No new copy needed — reuses existing MOMENTS text.
Council fixes folded in: one-way scroll flag so a gesture does not bounce back and forth; keyboard focus moves to the list item on activation; highlight uses outline/weight, not color alone; stable IDs per moment (e.g. #bb-moment-2) so moments are shareable; never hide the already-visible list text just to create an interaction; reduced-motion fallback for smooth scroll.

## Feature B: Animated line draw
Current state: chart renders fully on page load.
Change: a small "Play" button per chart (text button, editorial style, no icon fonts) animates the episode polyline drawing left to right via stroke-dashoffset over ~4 seconds, with a live readout of the episode being drawn (title, viewers). Also triggers once on scroll into view if the user has not played it. Respects prefers-reduced-motion (renders static).
Why: watching the fall happen lands harder than seeing the finished slope; cheapest possible motion.
Effort: small. JS requestAnimationFrame drives both the draw and the readout (keeps them in sync — CSS alone cannot).
Council fixes folded in: changing a toggle mid-animation cancels cleanly and renders static — replay only on request, never auto-replay on toggle; readout line is fixed-height so the chart does not jump as titles change; scroll-trigger fires once per page via IntersectionObserver at ~50% visibility, only the most-visible chart if several enter together; readout is not announced per-episode to screen readers; completed chart stays visible by default — nothing hidden waiting for a scroll trigger.

## Feature C: Auto inflection callouts
Current state: nothing labels the biggest week-to-week moves.
Change: at build time, compute per show the 3 largest single-episode drops and 3 largest gains (viewers[i] - viewers[i-1], consecutive episodes only). Render small serif labels directly on the chart at those points, e.g. "-3.1M" / "+2.4M", in the show's accent color at reduced opacity. Skip callouts that would overlap a numbered moment marker (moment wins). Hovering a callout shows the two episode titles.
Why: answers "when did it jump the shark" without the visitor hunting — the Reddit debate in one feature.
Effort: small. Computed at build time from existing data, zero runtime cost.
Council fixes folded in: deltas computed WITHIN seasons only — a premiere vs. the prior finale is a gap, not a week-to-week move; missing viewer points are skipped, never treated as zero; gains and drops ranked separately on unrounded values; labels checked against moment markers, each other, and chart edges in BOTH linear and log scales; episode-pair titles available on tap/focus, not hover alone; true minus sign (−); build-time assertion recomputes one known delta per show.

## Design constraints (his standing rules)
- Zero AI slop: no gradients, no generic illustrations, no emoji bullets. Serif labels, hairlines, restrained accents only.
- Static site: HTML/CSS/JS only, no backend, no new dependencies.
- Mobile-first: tap targets, no hover-only functionality (Feature A works on tap; Feature C callouts are visible labels, not hover secrets).
- prefers-reduced-motion honored for Feature B.

## Cost
~$0 for build. No council spend needed for the build itself (council only for this review).

## Verification before ship
1. Build passes stats check (existing: twd_loss=87, bb_mult=7.3, got_finale_imdb=4.0, hotd_mult=9).
2. curl the live URL, confirm 200 and new features render (spot-check one show's page: marker click, play button, callout labels).
3. Link verification rule: any public URL posted about this update gets loaded first.

## Open questions for Eric
1. Feature B trigger: play button per chart, auto-play on scroll into view, or both? Council split — one seat says button only (reader control), three say both (button + scroll-once, reduced-motion disables autoplay). My lean: both.
2. Feature C count: 3 drops + 3 gains, or 2+2? Council lean: 3+3 on desktop, hide rank-3 on mobile via CSS (2+2). My lean: 3+3 desktop / 2+2 mobile.

## Council verdicts
- grok: BUILD all three. Flags: scroll-bounce flag, live-readout layout shift, absolute (not percent) deltas stated in a build comment.
- gpt: BUILD A; BUILD B and C with guardrails. Button-only for v1, 2+2 callouts, curl verifies delivery not behavior — add browser checks on narrow and wide screens.
- gemini: BUILD all three. rAF over CSS for readout sync; IntersectionObserver at 0.8 threshold; 2+2 callouts.
- anthropic: BUILD all three. Season-boundary exclusion for deltas; mixed-metric check; stable shareable moment IDs; 3+3 desktop / 2+2 mobile via CSS.
