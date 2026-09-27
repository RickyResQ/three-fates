#!/usr/bin/env python3
"""Transform build_page2.py -> build_page3.py: the paper editorial redesign.
Every replacement is asserted; the script fails loudly if a pattern drifts."""
import re

BASE = '/home/hatch/workspace/three-fates'
src = open(f'{BASE}/build_page2.py').read()

REPS = [
# ---------- palette ----------
("""  --bg:#0d0b08; --ink:#ece4d2; --muted:#a89d86; --faint:#6f6350; --line:#2b2419;
  --twd:#ff6f5c; --got:#e6b93d; --bb:#43b581; --hotd:#b48ce8;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,"Times New Roman",serif;""",
 """  --bg:#FFF1E5; --ink:#33302E; --muted:#5c564d; --faint:#8d867a; --line:#e0d3ba;
  --twd:#C23B22; --got:#9A7A1A; --bb:#1E7A4C; --hotd:#6C4FA1;
  --accent:#990F3D;
  --serif:Georgia,"Iowan Old Style","Palatino Linotype",Palatino,"Times New Roman",serif;"""),
("::selection{background:#3a2f1c;color:#fff}",
 "::selection{background:#990F3D;color:#fff}"),
("opacity:.055;mix-blend-mode:overlay", "opacity:.03;mix-blend-mode:multiply"),
# ---------- masthead ----------
(".kicker{font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--muted)}",
 ".kicker{font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--accent);font-weight:700}"),
(".lede{font-size:clamp(16px,2.2vw,20px);color:var(--muted);max-width:62ch;margin:18px 0 0}",
 ".lede{font-family:var(--serif);font-style:italic;font-size:clamp(17px,2.3vw,21px);color:var(--muted);max-width:62ch;margin:18px 0 0}"),
(".rule-double{border:0;border-top:3px solid var(--line);border-bottom:1px solid var(--line);height:7px;margin:34px 0 0;padding:0}",
 ".rule-double{border:0;border-top:2.5px solid var(--ink);border-bottom:1px solid var(--ink);height:7px;margin:34px 0 0;padding:0}"),
# ---------- scrolly steps: serif body ----------
(".stepnum{font-family:var(--serif);font-size:15px;color:var(--faint);letter-spacing:.2em;margin-bottom:10px}",
 ".stepnum{font-family:var(--sans);font-weight:700;font-size:12px;color:var(--accent);letter-spacing:.24em;margin-bottom:10px}"),
(".step p{color:var(--muted);font-size:16px;margin:0 0 .9em;max-width:44ch}",
 ".step p{font-family:var(--serif);color:var(--ink);font-size:17.5px;line-height:1.65;margin:0 0 .9em;max-width:44ch}"),
(".step p strong{color:var(--ink);font-weight:600}", ".step p strong{font-weight:700}"),
# ---------- quiz ----------
(".quiz{margin:90px 0 0;max-width:720px;border-top:3px solid var(--line);padding-top:30px}",
 ".quiz{margin:90px 0 0;max-width:720px;border-top:3px solid var(--ink);padding-top:30px}"),
(".quizbtn.right{border-color:var(--twd);color:var(--twd);opacity:1}",
 ".quizbtn.right{border-color:var(--accent);color:var(--accent);opacity:1}"),
("#quizanswer .payoff strong{color:var(--twd);font-weight:400}",
 "#quizanswer .payoff strong{color:var(--accent);font-weight:400}"),
# ---------- show sections ----------
(".showsec{margin-top:96px;border-top:3px solid var(--line);padding-top:26px}",
 ".showsec{margin-top:96px;border-top:3px solid var(--ink);padding-top:26px}"),
(".secnum{font-family:var(--serif);font-size:15px;letter-spacing:.25em;color:var(--faint);margin-bottom:8px}",
 ".secnum{font-family:var(--sans);font-weight:700;font-size:12px;letter-spacing:.26em;color:var(--accent);margin-bottom:8px}"),
(".badge.ongoing{color:#0d0b08;background:var(--hotd);border-color:var(--hotd);font-weight:700}",
 ".badge.ongoing{color:#fff;background:var(--hotd);border-color:var(--hotd);font-weight:700}"),
(".secstat-num{font-family:var(--serif);font-size:clamp(54px,7vw,84px);line-height:1}",
 ".secstat-num{font-family:var(--serif);font-size:clamp(54px,7vw,84px);line-height:1;letter-spacing:-.01em}"),
# ---------- obit: serif body, kicker subhead, no drop cap, pull quote ----------
(".obit{margin-top:34px;max-width:72ch}", ".obit{margin-top:34px;max-width:68ch}"),
(".obit h3{font-family:var(--serif);font-style:italic;font-weight:400;font-size:30px;margin:0 0 14px}",
 ".obit h3{font-family:var(--sans);font-style:normal;font-weight:700;font-size:13px;letter-spacing:.24em;text-transform:uppercase;color:var(--accent);margin:0 0 16px}"),
(".obit p{color:#cfc7b4;font-size:16.5px;margin:0 0 1.05em}",
 ".obit p{font-family:var(--serif);color:var(--ink);font-size:18px;line-height:1.72;margin:0 0 1.1em}"),
(".obit p:first-of-type::first-letter{font-family:var(--serif);font-size:3.6em;float:left;line-height:.82;padding:4px 10px 0 0;color:var(--ink)}",
 """.pullquote{border-top:1.5px solid var(--ink);border-bottom:1.5px solid var(--ink);padding:22px 0;margin:32px 0;max-width:68ch}
.pullquote p{font-family:var(--serif);font-style:italic;font-size:clamp(22px,3vw,27px);line-height:1.42;color:var(--ink);margin:0}
.pullquote .attr{font-family:var(--sans);font-style:normal;font-size:11.5px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--faint);margin-top:12px}"""),
# ---------- moments: footnote style ----------
(".moments{list-style:none;margin:26px 0 0;padding:0;max-width:860px}",
 ".moments{list-style:none;margin:26px 0 0;padding:0;max-width:68ch}"),
(".moments strong{color:var(--ink);font-weight:600}",
 ".moments strong{color:var(--ink);font-weight:400;font-family:var(--serif);font-style:italic}"),
(".mnum{font-family:var(--serif);font-size:21px;color:var(--ink);line-height:1.4}",
 ".mnum{font-family:var(--sans);font-weight:700;font-size:13px;color:var(--accent);line-height:1.7}"),
(".cap{color:var(--faint);font-size:12.5px;margin:8px 0 0;max-width:70ch}",
 ".cap{color:var(--faint);font-size:12.5px;margin:8px 0 0;max-width:70ch}\n.caphead{display:block;font-family:var(--serif);font-size:17px;line-height:1.45;color:var(--ink);margin-bottom:5px;max-width:62ch}"),
# ---------- method / email / footer ----------
(".method{margin-top:96px;border-top:3px solid var(--line);padding-top:26px;max-width:860px}",
 ".method{margin-top:96px;border-top:3px solid var(--ink);padding-top:26px;max-width:860px}"),
(".emailbox input[type=email]{background:#0d0b08;border:1px solid var(--line);border-radius:8px;color:var(--ink);padding:13px 16px;font-size:15px;width:min(320px,80vw);font-family:var(--sans)}",
 ".emailbox input[type=email]{background:#fffdf8;border:1px solid #c9b78f;border-radius:8px;color:var(--ink);padding:13px 16px;font-size:15px;width:min(320px,80vw);font-family:var(--sans)}"),
(".emailbox button{background:#ece4d2;color:#0d0b08;border:0;border-radius:8px;padding:13px 26px;font-size:15px;font-weight:700;cursor:pointer;font-family:var(--sans)}",
 ".emailbox button{background:#990F3D;color:#fff;border:0;border-radius:8px;padding:13px 26px;font-size:15px;font-weight:700;cursor:pointer;font-family:var(--sans)}"),
(".emailbox button:hover{background:#fff}", ".emailbox button:hover{background:#7a0c31}"),
('Set in Iowan Old Style &amp; the system grotesque. Printed on 100% recycled pixels.',
 'Set in Georgia &amp; the system grotesque. Printed on 100% recycled pixels.'),
# ---------- tooltip / scrubber ----------
("#tip{position:fixed;pointer-events:none;background:#1d1812;border:1px solid #4a3d28;border-radius:10px;padding:10px 13px;font-size:13px;max-width:270px;display:none;z-index:95;box-shadow:0 8px 30px rgba(0,0,0,.55);color:var(--ink)}",
 "#tip{position:fixed;pointer-events:none;background:#fffdf8;border:1px solid #d9c9a8;border-radius:10px;padding:10px 13px;font-size:13px;max-width:270px;display:none;z-index:95;box-shadow:0 10px 28px rgba(74,52,20,.20);color:var(--ink)}"),
("#tip .r{color:#ffd479}", "#tip .r{color:var(--accent);font-weight:700}"),
(".scrub{width:100%;accent-color:#ece4d2}", ".scrub{width:100%;accent-color:#990F3D}"),
(".scrubcard{background:#14110c;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:14px;margin-top:8px;min-height:74px}",
 ".scrubcard{background:#fffdf8;border:1px solid var(--line);border-radius:10px;padding:12px 14px;font-size:14px;margin-top:8px;min-height:74px}"),
(".scrubcard .r{color:#ffd479}", ".scrubcard .r{color:var(--accent);font-weight:700}"),
("  .obit p{font-size:16px}", "  .obit p{font-size:17px}"),
# ---------- BODY: viz headline states the conclusion ----------
('<div class="vtitle">The versus <em>&mdash; three shows, three fates</em></div>',
 '<div class="vtitle">One died. One was crowned. One climbed. <em>three shows, three fates</em></div>'),
("<p>Scroll. The lines will draw themselves &mdash; one fate at a time.</p>",
 "<p>Scroll. The lines will draw themselves, one fate at a time.</p>"),
("peaked at 17.29 million viewers in October 2014 &mdash; the biggest scripted audience of the decade &mdash; then bled for eight straight years.",
 "peaked at 17.29 million viewers in October 2014, the biggest scripted audience of the decade, then bled for eight straight years."),
("of its peak audience gone by the finale &mdash; 17.29M &rarr; 2.27M viewers.",
 "of its peak audience gone by the finale &middot; 17.29M &rarr; 2.27M viewers."),
("grew every single season &mdash; a climb so steady it looks drawn with a ruler.",
 "grew every single season, a climb so steady it looks drawn with a ruler."),
("It fragmented &mdash; and these three were the last shows big enough to be measured dying.",
 "It fragmented, and these three were the last shows big enough to be measured dying."),
("Below: the full record &mdash; every episode, every viewer &mdash; and four obituaries.",
 "Below: the full record, every episode and every viewer, and four obituaries."),
("17.29 million at the peak, 2.27 million at the end &mdash; the biggest rise and the longest fall ever measured on cable.",
 "17.29 million at the peak, 2.27 million at the end, the biggest rise and the longest fall ever measured on cable."),
("<h2>Methodology</h2>", "<h2>Data and Methods</h2>"),
# ---------- python: paper-safe palette, pull quotes, conclusion captions ----------
('"""Build three-fates.html v2 — de-slopped editorial redesign + scrollytelling.',
 '"""Build three-fates.html v3 — paper editorial redesign (FT/Pudding/Reuters patterns).'),
("""SECSTAT = {
    'The Walking Dead': None,  # giant -87% already lives in the scrolly step""",
 """PCOL = {'The Walking Dead': '#C23B22', 'Game of Thrones': '#9A7A1A',
        'Breaking Bad': '#1E7A4C', 'House of the Dragon': '#6C4FA1'}
CHART_CAPS = {
    'The Walking Dead': 'Every episode, 2010 to 2022: the longest, steadiest bleed ever measured on cable.',
    'Game of Thrones': 'Every episode, 2011 to 2019: eight seasons, every one bigger than the last.',
    'Breaking Bad': 'Every episode, 2008 to 2013: the only ascent on this page.',
    'House of the Dragon': 'Every episode, 2022 to 2026, linear only. The real audience is somewhere the old ruler cannot reach.',
}
PULLQUOTES = {
    'The Walking Dead': ('The conditions that drew this curve will never exist again.', 'From \\u201cThe Death,\\u201d below'),
    'Game of Thrones': ('The tombstone reads 4.0.', 'From \\u201cThe Coronation,\\u201d below'),
    'Breaking Bad': ('The data says the ascent may never happen again.', 'From \\u201cThe Ascent,\\u201d below'),
    'House of the Dragon': ('The old charts now describe the audience the way a shadow describes a person.', 'From \\u201cThe Heir,\\u201d below'),
}
SECSTAT = {
    'The Walking Dead': None,  # giant -87% already lives in the scrolly step"""),
("""    paras_html = ''.join(f'<p>{p}</p>' for p in paras)""",
 """    pq, pqattr = PULLQUOTES[name]
    paras_html = ''
    for j, p in enumerate(paras):
        paras_html += f'<p>{p}</p>'
        if j == 1:
            paras_html += (f'<aside class="pullquote"><p>\\u201c{pq}\\u201d</p>'
                           f'<div class="attr">{pqattr}</div></aside>')"""),
("""    <span class="cdot" style="background:{show['color']}"></span>""",
 """    <span class="cdot" style="background:{PCOL[name]}"></span>"""),
("""                     f' style="color:{show["color"]}">""",
 """                     f' style="color:{PCOL[name]}">"""),
("""  <div class="cap">Nielsen linear first-airing figures, millions of US viewers. Dots: episodes. Bold line: season average. Hover or tap a dot.</div>""",
 """  <div class="cap"><span class="caphead">{CHART_CAPS[name]}</span>Nielsen linear first-airing figures, millions of US viewers. Dots: episodes. Bold line: season average. Hover or tap a dot.</div>"""),
# ---------- JS: chart furniture for paper ----------
("const VSHOWS=[['The Walking Dead','#ff6f5c','twd'],['Game of Thrones','#e6b93d','got'],['Breaking Bad','#43b581','bb']];",
 "const VSHOWS=[['The Walking Dead','#C23B22','twd'],['Game of Thrones','#9A7A1A','got'],['Breaking Bad','#1E7A4C','bb']];\n"
 "const PCOL={'The Walking Dead':'#C23B22','Game of Thrones':'#9A7A1A','Breaking Bad':'#1E7A4C','House of the Dragon':'#6C4FA1'};"),
("[['#ff6f5c','2014-10-12',17.29,'Peak of cable: 17.29M',18,-14,'start'],\n               ['#43b581','2013-09-29',10.28,'Felina: 10.28M',-8,30,'middle'],\n               ['#e6b93d','2019-05-19',13.61,'Finale: 13.61M',10,-30,'start']]",
 "[['#C23B22','2014-10-12',17.29,'Peak of cable: 17.29M',18,-14,'start'],\n               ['#1E7A4C','2013-09-29',10.28,'Felina: 10.28M',-8,30,'middle'],\n               ['#9A7A1A','2019-05-19',13.61,'Finale: 13.61M',10,-30,'start']]"),
("stroke:'#0d0b08','stroke-width':2},gNotes", "stroke:'#FFF1E5','stroke-width':2},gNotes"),
("stroke:'#ece4d2','stroke-width':1.5,opacity:.85,visibility:'hidden'", "stroke:'#33302E','stroke-width':1.5,opacity:.85,visibility:'hidden'"),
("fill:'#ece4d2','font-size':13,'font-weight':700,'text-anchor':'middle'", "fill:'#33302E','font-size':13,'font-weight':700,'text-anchor':'middle'"),
("stroke:'#ece4d2','stroke-width':1.5,opacity:.9", "stroke:'#33302E','stroke-width':1.5,opacity:.9"),
("stroke:'#ece4d2','stroke-width':1.5,opacity:.8", "stroke:'#33302E','stroke-width':1.5,opacity:.8"),
("stroke:'#1d1812','stroke-width':1", "stroke:'#e6d9bd','stroke-width':1"),
("stroke:s.color,'stroke-width':5", "stroke:PCOL[s.show],'stroke-width':5"),
("stroke:s.color,'stroke-width':1.6", "stroke:PCOL[s.show],'stroke-width':1.6"),
("r:3,fill:s.color,opacity:.92", "r:3,fill:PCOL[s.show],opacity:.92"),
("Not that one \\u2014 try again.", "Not that one. Try again."),
]

COUNTS = {"stroke:'#241e14'": 2, "fill:'#6f6350'": 4, "fill:'#8a7c60'": 1}

for old, new in REPS:
    assert src.count(old) == 1, f'NOT FOUND or MULTIPLE ({src.count(old)}): {old[:70]!r}'
    src = src.replace(old, new)

for old, n in COUNTS.items():
    assert src.count(old) == n, f'COUNT DRIFT ({src.count(old)} != {n}): {old!r}'
new_map = {"stroke:'#241e14'": "stroke:'#e6d9bd'", "fill:'#6f6350'": "fill:'#8d867a'", "fill:'#8a7c60'": "fill:'#a89d86'"}
for old, new in new_map.items():
    src = src.replace(old, new)

# sanity: no dark-theme leftovers
for bad in ['#0d0b08', '#ece4d2', '#ff6f5c', '#e6b93d', '#43b581', '#b48ce8', '#ffd479', '#1d1812', '#241e14']:
    assert bad not in src, f'leftover dark-theme color: {bad}'

open(f'{BASE}/build_page3.py', 'w').write(src)
print('wrote build_page3.py,', len(src), 'bytes')
