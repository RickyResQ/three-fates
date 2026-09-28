# Three Fates v3 Update Plan — for Eric's review, then council

## Context
The r/dataisbeautiful thread (1.1k upvotes, 406K views) produced a full comment sweep. Top asks: new shows (Better Call Saul, Lost, The Wire, The Sopranos, Parks and Rec, Buffy, M*A*S*H), a colorblind-safe palette (top-voted single comment, 98 upvotes), dashed/dotted line patterns, and a season/episode x-axis toggle. Seinfeld, Friends, and The Office were requested too, but the site already has them (955 episodes, 7 shows across dramas + sitcoms sets).

## Proposed scope: Phase A (ship this week, while the thread is warm)
1. Accessibility overhaul: switch all series to the Okabe-Ito colorblind-safe palette, add dashed/dotted/solid line patterns per series, and distinct point shapes. This answers the single most-upvoted comment in the thread.
2. Add Better Call Saul (62 episodes, AMC 2015-2022): per-episode Nielsen linear figures from Wikipedia episode tables. Pairs with Breaking Bad; the thread already discussed it.
3. Add Lost (121 episodes, ABC 2004-2010): per-episode Nielsen figures from Wikipedia episode tables. Directly answers u/1RedOne's request.
4. Season/episode x-axis toggle: align every series to S1E1 so viewers can compare trajectories show-to-show, alongside the existing release-date axis.
5. Methodology honesty note: a short "what this leaves out" section addressing the thread's critiques — streaming not counted, piracy undercounts GoT, Nielsen misses viewing parties, linear-only. This strengthens credibility with the exact critics who raised it.

## Deferred to Phase B (later, not this week)
- More shows: The Wire, The Sopranos, Parks and Rec, Buffy, M*A*S*H.
- Head-to-head comparison mode and season report cards (were v2 ideas).

## Why BCS + Lost first, not all seven requested shows
- Each new show needs per-episode Nielsen data verified against Wikipedia tables; quality beats quantity, and the 404 incident taught us every public claim gets checked.
- BCS and Lost were the two most-discussed in the thread (BCS debated at length; Lost explicitly requested).
- Shipping two good shows this week beats shipping seven rushed ones next month while the thread cools.

## What this costs Eric
Nothing but review. Agent collects the data, verifies figures, rebuilds the page, loads the live URL and confirms 200 before telling you.

## Verification rules before shipping
- Every per-episode figure checked against its Wikipedia source table.
- Live page loaded and confirmed 200, not just built locally.
- No invented data anywhere.
