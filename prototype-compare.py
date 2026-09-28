#!/usr/bin/env python3
"""Build the v4 comparison-chart legibility prototype (approval gate, not the full page).

Steps:
  1. Contrast gate: every show accent vs #FFF1E5 must be >= 3:1 (WCAG non-text).
     Fails with nonzero exit and writes NO html.
  2. Label de-collision simulation at 375px and 1280px (same greedy 2D algorithm
     the page runs in JS: labels sit just past each line's end, min 16px vertical
     gap where x-ranges overlap). Fails on any overlap or edge clipping.
  3. Writes ~/workspace/three-fates/prototype-compare.html.
"""
import json, sys

BG = '#FFF1E5'
SHOWS = [
    ('The Walking Dead', '#D55E00', ''),
    ('Game of Thrones', '#0072B2', '12,6'),
    ('Breaking Bad', '#B37400', '3,3'),
    ('House of the Dragon', '#A24D7E', '16,5,3,5'),
    ('Better Call Saul', '#8C564B', '2,2'),
    ('Lost', '#007A5E', '10,4'),
]
OUT = '/home/hatch/workspace/three-fates/prototype-compare.html'
DATA = '/home/hatch/workspace/three-fates/data.json'
YMAX = 24.0

# ---- 1. contrast gate ----
def lum(h):
    h = h.lstrip('#')
    r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)

def ratio(a, b):
    l1, l2 = sorted((lum(a), lum(b)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

print('contrast vs', BG)
for name, col, _ in SHOWS:
    r = ratio(col, BG)
    print(f'  {name:20s} {col}  {r:.2f}:1')
    if r < 3.0:
        print(f'  !! {name} below 3:1 — gate failed')
        sys.exit(1)

# ---- data ----
data = json.load(open(DATA))
by_name = {s['show']: s for s in data['shows']}
series = {}
for name, col, dash in SHOWS:
    pts = [(i, e['viewers']) for i, e in enumerate(by_name[name]['episodes'])
           if e['viewers'] is not None]
    series[name] = pts
total_eps = sum(len(v) for v in series.values())
x_max = max(p[0] for v in series.values() for p in v)

# label width estimate (px): name chars + pattern sample + gaps (+ dot on mobile)
def label_w(name, mobile):
    per = 6.2 if mobile else 6.8
    extra = (18 + 7 + 14) if mobile else (26 + 14)
    return len(name) * per + extra

def geom(W):
    mobile = W <= 480
    L = 42 if mobile else 46
    R = 170 if mobile else 190
    T, B = 16, 38
    H = 360 if mobile else 440
    return dict(L=L, R=R, T=T, B=B, H=H, mobile=mobile,
                pw=W - L - R, ph=H - T - B, W=W)

# ---- 2. simulation ----
for W in (375, 1280):
    g = geom(W)
    X = lambda x: g['L'] + x / x_max * g['pw']
    Y = lambda v: g['T'] + g['ph'] - v / YMAX * g['ph']
    items = []
    for name, _, _ in SHOWS:
        ex, ev = series[name][-1]
        x0 = X(ex) + 8
        items.append({'name': name, 'x0': x0, 'x1': x0 + label_w(name, g['mobile']),
                      'y': Y(ev), 'ex': X(ex), 'ey': Y(ev)})
    items.sort(key=lambda d: d['y'])
    # greedy 2D placement: separate x-overlapping labels (16px), then global
    # shifts to respect plot bounds (shifts preserve gaps, so this converges)
    n = len(items)
    ys = [it['y'] for it in items]
    xov = lambda a, b: not (items[a]['x1'] < items[b]['x0'] or items[b]['x1'] < items[a]['x0'])
    for _ in range(60):
        changed = False
        for i in range(1, n):
            for j in range(i):
                if xov(i, j) and ys[i] - ys[j] < 16:
                    ys[i] = ys[j] + 16
                    changed = True
        over = max(ys) - (g['T'] + g['ph'])
        if over > 0:
            ys = [y - over for y in ys]
            changed = True
        under = g['T'] - min(ys)
        if under > 0:
            ys = [y + under for y in ys]
            changed = True
        if not changed:
            break
    placed_x0 = [it['x0'] for it in items]
    placed_x1 = [it['x1'] for it in items]
    for i in range(len(ys)):
        for j in range(i + 1, len(ys)):
            xover = not (items[i]['x1'] < items[j]['x0'] or items[j]['x1'] < items[i]['x0'])
            if xover:
                assert abs(ys[i] - ys[j]) >= 15.99, f'label overlap at {W}px: {items[i]["name"]} vs {items[j]["name"]}'
    assert all(g['T'] <= y <= g['T'] + g['ph'] for y in ys), f'out of bounds at {W}px'
    assert all(it['x1'] <= W - 4 for it in items), f'clipped at {W}px'
    gaps = [ys[i+1] - ys[i] for i in range(len(ys) - 1)]
    print(f'de-collision {W}px: {len(ys)} labels, min vertical gap {min(gaps):.1f}px, in bounds, no clipping — OK')

# ---- 3. write html ----
js_data = {name: [[x, v] for x, v in pts] for name, pts in series.items()}
js_shows = [{'name': n, 'color': c, 'dash': d} for n, c, d in SHOWS]

html = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Prototype — comparison chart legibility gate</title>
<style>
  :root{
    --bg:#FFF1E5; --ink:#33302E; --muted:#5c564d; --faint:#8d867a; --line:#e0d3ba;
    --serif: Georgia, 'Times New Roman', serif;
    --sans: -apple-system, 'Helvetica Neue', Arial, sans-serif;
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);
       -webkit-font-smoothing:antialiased}
  .wrap{max-width:1200px;margin:0 auto;padding:40px 20px 80px}
  .kicker{font-size:12px;letter-spacing:.26em;text-transform:uppercase;
          color:var(--faint);font-weight:700;margin-bottom:14px}
  h1{font-family:var(--serif);font-weight:400;font-size:clamp(30px,4.6vw,52px);
     line-height:1.08;margin:0 0 12px;letter-spacing:-.01em;
     font-variant-numeric:oldstyle-nums}
  h1 em{font-style:italic}
  .sub{font-size:15.5px;color:var(--muted);max-width:62ch;margin:0 0 34px;line-height:1.6}
  #stage{position:relative;width:100%}
  #stage svg{display:block;width:100%;height:auto}
  .tick{font-family:var(--sans);font-size:11px;fill:var(--faint)}
  .grid{stroke:var(--line);stroke-width:1}
  .axis{stroke:#b9a983;stroke-width:1}
  .leader{stroke:#b9a983;stroke-width:1}
  .slabel{position:absolute;transform:translateY(-50%);display:flex;align-items:center;
          gap:7px;background:transparent;border:0;padding:5px 4px;cursor:pointer;
          font-family:var(--sans);font-size:13px;font-weight:600;white-space:nowrap;
          border-radius:6px;text-align:left}
  .slabel:focus-visible{outline:2px solid var(--ink);outline-offset:2px}
  .slabel.dim{opacity:.35}
  .slabel .dot{display:none;width:7px;height:7px;border-radius:50%;flex:0 0 auto}
  .cap{margin-top:14px;font-size:12.5px;color:var(--faint);max-width:70ch;line-height:1.55}
  .hint{margin-top:10px;font-size:13px;color:var(--muted)}
  @media (max-width:480px){
    .wrap{padding:28px 14px 60px}
    .slabel{font-size:12px;color:var(--muted);font-weight:500}
    .slabel .dot{display:block}
    .slabel .sw{width:18px}
  }
</style>
</head>
<body>
<div class="wrap">
  <div class="kicker">Prototype &middot; legibility gate</div>
  <h1>Six premieres, <em>__TOTAL__ episodes</em>, one chart.</h1>
  <p class="sub">Every episode of six landmark series, plotted from its own S1E1 &mdash; so you can watch audiences arrive, peak, and leave on the same clock. Tap a show to isolate it.</p>
  <div id="stage"></div>
  <p class="hint" id="hint">Tap a show name or line to focus it. Tap again, press Esc, or tap the background to reset.</p>
  <p class="cap">Nielsen linear first-airing figures, millions of US viewers. Each line keeps its own dash pattern, so every show is identifiable without color. No legend &mdash; each label sits at its line&rsquo;s right edge.</p>
</div>
<script>
const SHOWS = __SHOWS__;
const DATA = __DATA__;
const XMAX = __XMAX__, YMAX = 24;
const FADE = '#d8cfbd';
const NS = 'http://www.w3.org/2000/svg';
const stage = document.getElementById('stage');
let focused = null;
const reg = {};

function labelW(name, mobile){
  const per = mobile ? 6.2 : 6.8;
  const extra = mobile ? (18 + 7 + 14) : (26 + 14);
  return name.length * per + extra;
}

function geom(W){
  const mobile = W <= 480;
  const L = mobile ? 42 : 46, R = mobile ? 170 : 190, T = 16, B = 38;
  const H = mobile ? 360 : 440;
  const pw = W - L - R, ph = H - T - B;
  return {L,R,T,B,H,pw,ph,mobile,
    X: x => L + x / XMAX * pw,
    Y: v => T + ph - v / YMAX * ph};
}

function el(tag, attrs, parent){
  const n = document.createElementNS(NS, tag);
  for (const k in attrs) n.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(n);
  return n;
}

function toggle(name){ setFocus(focused === name ? null : name); }
function setFocus(name){ focused = name; applyFocus(); }

function applyFocus(){
  SHOWS.forEach(s => {
    const rec = reg[s.name];
    if (!rec || !rec.btn) return;
    const on = !focused || focused === s.name;
    rec.pl.setAttribute('stroke', on ? s.color : FADE);
    rec.pl.setAttribute('opacity', on ? '1' : '.55');
    rec.btn.classList.toggle('dim', !on);
    rec.btn.setAttribute('aria-pressed', focused === s.name ? 'true' : 'false');
  });
  document.getElementById('hint').textContent = focused
    ? 'Showing ' + focused + ' \u2014 others faded. Tap again, press Esc, or tap the background to reset.'
    : 'Tap a show name or line to focus it. Tap again, press Esc, or tap the background to reset.';
}

function build(){
  const W = stage.clientWidth;
  const g = geom(W);
  stage.innerHTML = '';
  for (const k in reg) delete reg[k];
  const svg = el('svg', {width: W, height: g.H, role: 'img',
    'aria-label': 'Per-episode viewership, all six shows from their premieres'}, stage);

  for (let v = 0; v <= YMAX; v += 6){
    const y = g.Y(v);
    el('line', {x1: g.L, x2: g.L + g.pw, y1: y, y2: y, class: 'grid'}, svg);
    const t = el('text', {x: g.L - 8, y: y + 4, 'text-anchor': 'end', class: 'tick'}, svg);
    t.textContent = v === 0 ? '0' : v + 'M';
  }
  el('line', {x1: g.L, x2: g.L, y1: g.T, y2: g.T + g.ph, class: 'axis'}, svg);
  el('line', {x1: g.L, x2: g.L + g.pw, y1: g.T + g.ph, y2: g.T + g.ph, class: 'axis'}, svg);
  const xl = el('text', {x: g.L + g.pw, y: g.H - 8, 'text-anchor': 'end', class: 'tick'}, svg);
  xl.textContent = 'episode number from each show\u2019s premiere';

  SHOWS.forEach(s => {
    const pts = DATA[s.name].map(p => [g.X(p[0]), g.Y(p[1])]);
    const str = pts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ');
    const grp = el('g', {}, svg);
    const hit = el('polyline', {points: str, fill: 'none', stroke: 'rgba(0,0,0,0)',
      'stroke-width': 20, style: 'cursor:pointer'}, grp);
    const pl = el('polyline', {points: str, fill: 'none', stroke: s.color,
      'stroke-width': 2.2, 'stroke-linejoin': 'round', 'stroke-linecap': 'round'}, grp);
    if (s.dash) pl.setAttribute('stroke-dasharray', s.dash);
    hit.addEventListener('click', ev => { ev.stopPropagation(); toggle(s.name); });
    const ex = pts[pts.length-1][0], ey = pts[pts.length-1][1];
    reg[s.name] = {pl, show: s, ex, ey};
  });

  // labels at each line's right edge, greedy 2D de-collision:
  // separate x-overlapping labels to a 16px min vertical gap, then global
  // shifts to respect plot bounds (shifts preserve gaps, so this converges)
  const items = SHOWS.map(s => {
    const r = reg[s.name];
    const x0 = r.ex + 8;
    return {name: s.name, x0, x1: x0 + labelW(s.name, g.mobile), y: r.ey};
  }).sort((a, b) => a.y - b.y);
  const n = items.length;
  const ys = items.map(it => it.y);
  const xov = (a, b) => !(items[a].x1 < items[b].x0 || items[b].x1 < items[a].x0);
  for (let iter = 0; iter < 60; iter++){
    let changed = false;
    for (let i = 1; i < n; i++)
      for (let j = 0; j < i; j++)
        if (xov(i, j) && ys[i] - ys[j] < 16){ ys[i] = ys[j] + 16; changed = true; }
    const over = Math.max(...ys) - (g.T + g.ph);
    if (over > 0){ for (let i = 0; i < n; i++) ys[i] -= over; changed = true; }
    const under = g.T - Math.min(...ys);
    if (under > 0){ for (let i = 0; i < n; i++) ys[i] += under; changed = true; }
    if (!changed) break;
  }
  items.forEach((it, i) => { it.ly = ys[i]; });

  items.forEach(it => {
    const s = SHOWS.find(x => x.name === it.name);
    const r = reg[s.name];
    if (Math.abs(it.ly - r.ey) > 4)
      el('line', {x1: r.ex, x2: it.x0 - 4, y1: r.ey, y2: it.ly, class: 'leader'}, svg);
    const b = document.createElement('button');
    b.className = 'slabel'; b.type = 'button';
    b.style.left = it.x0 + 'px';
    b.style.top = it.ly + 'px';
    if (!g.mobile) b.style.color = s.color;
    b.setAttribute('aria-pressed', 'false');
    b.setAttribute('aria-label', 'Focus ' + s.name);
    const sw = document.createElementNS(NS, 'svg');
    sw.setAttribute('width', g.mobile ? '18' : '26');
    sw.setAttribute('height', '6'); sw.setAttribute('aria-hidden', 'true');
    sw.classList.add('sw');
    const samp = document.createElementNS(NS, 'line');
    samp.setAttribute('x1', '0'); samp.setAttribute('x2', g.mobile ? '18' : '26');
    samp.setAttribute('y1', '3'); samp.setAttribute('y2', '3');
    samp.setAttribute('stroke', s.color); samp.setAttribute('stroke-width', '2.4');
    if (s.dash) samp.setAttribute('stroke-dasharray', s.dash);
    sw.appendChild(samp);
    const dot = document.createElement('span');
    dot.className = 'dot'; dot.style.background = s.color; dot.setAttribute('aria-hidden', 'true');
    const nm = document.createElement('span'); nm.textContent = s.name;
    b.append(sw, dot, nm);
    b.addEventListener('click', ev => { ev.stopPropagation(); toggle(s.name); });
    stage.appendChild(b);
    r.btn = b;
  });

  svg.addEventListener('click', () => setFocus(null));
  applyFocus();
}

document.addEventListener('keydown', e => { if (e.key === 'Escape') setFocus(null); });
let rT;
window.addEventListener('resize', () => { clearTimeout(rT); rT = setTimeout(build, 150); });
build();
</script>
</body>
</html>'''

html = (html
        .replace('__TOTAL__', str(total_eps))
        .replace('__SHOWS__', json.dumps(js_shows))
        .replace('__DATA__', json.dumps(js_data))
        .replace('__XMAX__', str(x_max)))

open(OUT, 'w').write(html)
print('wrote', OUT, f'({total_eps} episodes, xmax={x_max})')
