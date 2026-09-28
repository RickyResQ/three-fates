# Three Fates v2 Plan — "Three Eras of the Sitcom"

Status: SHIPPED 2026-09-27 ~17:15 MST. Live at https://rickyresq.github.io/three-fates/ (commit 126533d).
Date: 2026-09-27

## Decisions (his delegation, my calls)

1. Framing: "Three Eras of the Sitcom." It was the commenter's own phrase and it mirrors the Three Fates concept.
2. Mini-obituaries: INCLUDED. Jeeves drafts all three in his voice (v1 obituaries are the style reference); Eric does one quick voice pass. Timeline assumes 24h turnaround from him.
3. v3: BCS + Lost, unless the thread keeps demanding something else — then follow the demand.

## Why this, why now

The r/dataisbeautiful thread (his #2 post of all time, 400+ upvotes, 159K views) produced two direct requests for Seinfeld / The Office / Friends as "three eras of the sitcom." That is the v2 content: it converts commenters into return visitors ("you asked, we built it"). Data verified available 2026-09-27: all three have per-episode Nielsen tables on Wikipedia.

BCS + Lost stay benched for v3.

## Content: the sitcom set

- Seinfeld (1989-1998, 180 eps): Wikipedia "List of Seinfeld episodes" has a full per-episode U.S. viewers grid. One TBD cell in S4 to resolve or mark null.
- Friends (1994-2004, 236 eps): per-episode "US viewers (millions)" tables on Wikipedia.
- The Office (2005-2013, 201 eps): per-episode tables on Wikipedia; OfficeTally (TV by the Numbers) as backup.

Same methodology as v1: Nielsen linear first-airing figures in millions. Same honesty bar: every headline figure verified against the source before it ships; nulls marked, never interpolated. Killer-stat pull-quotes for the trio (e.g. the finales: Seinfeld 76.3M, Friends 52.5M, Office 5.7M — the decline of monoculture in three numbers).

## Structure

v1's drama scrollytelling stays untouched. v2 adds a show-set switcher at the chart: Dramas | Sitcoms. Each set gets its own lines, same interactions. The sitcom set gets a short intro line, not full obituaries — data first, prose later. Per-show legend toggles double as the "head-to-head mode" (pick any two lines, overlay them).

## Features (thread-promised = must-ship)

1. Season/episode x-axis toggle (promised to Criplor).
2. Dots-only toggle (promised to foursaken — discrete per-episode data).
3. Dash-pattern line styles as second encoding on top of color (promised to FVCKEDINTHAHEAD; helps colorblind readers beyond the palette fix).
4. Per-show legend toggles (= head-to-head mode).

Deferred to v3: season report cards, TWD spinoff autopsy, BCS + Lost set.

## Build notes

- Data pipeline mirrors v1: scrape Wikipedia tables → data.json gains a "sitcoms" set → same verification pass (8 headline figures re-verified clean before ship).
- Chart code extends, not rewrites: set switcher, x-axis mode, point rendering mode, dash patterns.
- GoatCounter already live; v2 adds a per-set view count so we learn which set pulls.
- Email capture stays as-is.

## Timeline

Data pull + verification: 2-3 days. Build: 2-3 days. Target: ship within a week, while the thread's afterglow is still warm. A "you asked for it" reply dropped in the thread on launch day doubles as the marketing.

## Open questions for Eric

1. Ship the sitcom set as "Three Eras of the Sitcom" framing, or keep it neutral ("The Sitcoms")?
2. Mini-obituaries for the three sitcoms in his voice (like v1), or data-only for speed?
3. v3 next: BCS + Lost, or something else the thread asks for?
