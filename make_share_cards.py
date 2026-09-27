"""Render v3 paper-style share cards from the real dataset."""
import json, datetime
from PIL import Image, ImageDraw, ImageFont

BASE = '/home/hatch/workspace/three-fates'
PAPER = (255, 241, 229)
INK = (51, 48, 46)
MUTED = (138, 123, 102)
LINE = (229, 214, 190)
CLARET = (153, 15, 61)
SHOWS = [('The Walking Dead', (194, 59, 34)),
         ('Game of Thrones', (154, 122, 26)),
         ('Breaking Bad', (30, 122, 76))]
SHORT = {'The Walking Dead': 'TWD', 'Game of Thrones': 'GoT', 'Breaking Bad': 'BB'}

SERIF = '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf'
SERIFB = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
SANS = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

d = json.load(open(f'{BASE}/data.json'))
by = {s['show']: s for s in d['shows']}
T0 = datetime.date(2008, 1, 1).toordinal()
T1 = datetime.date(2023, 6, 1).toordinal()

def pts(show, x0, x1, y0, y1, vmax=18):
    out = []
    for ep in by[show]['episodes']:
        t = datetime.date.fromisoformat(ep['air']).toordinal()
        x = x0 + (t - T0) / (T1 - T0) * (x1 - x0)
        y = y1 - (ep['viewers'] / vmax) * (y1 - y0)
        out.append((x, y))
    return out

def tracked(draw, xy, text, font, fill, track=3):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x

def chart(draw, x0, y0, x1, y1, lw, years=True):
    # horizontal gridlines only, like the page
    grid_f = ImageFont.truetype(SANS, 22 if lw > 3 else 20)
    for v in (0, 5, 10, 15):
        y = y1 - (v / 18) * (y1 - y0)
        draw.line([(x0, y), (x1, y)], fill=LINE, width=2)
        draw.text((x0 - 14, y - 14), f'{v}M', font=grid_f, fill=MUTED, anchor='ra')
    if years:
        yr_f = ImageFont.truetype(SANS, 22 if lw > 3 else 20)
        for yr in range(2008, 2023, 2):
            t = datetime.date(yr, 1, 1).toordinal()
            x = x0 + (t - T0) / (T1 - T0) * (x1 - x0)
            draw.text((x, y1 + 12), str(yr), font=yr_f, fill=MUTED, anchor='ma')
    for name, color in SHOWS:
        draw.line(pts(name, x0, x1, y0, y1), fill=color, width=lw, joint='curve')

# ---------- 1. og-image.png (1200x630) ----------
W, H = 1200, 630
im = Image.new('RGB', (W, H), PAPER)
dr = ImageDraw.Draw(im)
M = 64
dr.line([(M, 56), (M + 72, 56)], fill=CLARET, width=5)
tracked(dr, (M, 72), 'THREE FATES', ImageFont.truetype(SERIFB, 34), INK, track=8)
dr.text((M, 128), 'One died. One was crowned. One climbed.',
        font=ImageFont.truetype(SERIF, 52), fill=INK)
# legend
lx = M
leg_f = ImageFont.truetype(SANS, 24)
for name, color in SHOWS:
    dr.ellipse([lx, 208, lx + 18, 226], fill=color)
    lx += 28
    dr.text((lx, 200), name, font=leg_f, fill=MUTED)
    lx += dr.textlength(name, font=leg_f) + 36
chart(dr, M + 44, 268, W - M, 540, 5, years=False)
dr.text((M, 566), 'Per-episode Nielsen ratings  \u00b7  rickyresq.github.io/three-fates',
        font=ImageFont.truetype(SANS, 22), fill=MUTED)
im.save(f'{BASE}/share/og-image.png')
print('wrote share/og-image.png')

# ---------- 2. reddit-versus.png (1600x1000) ----------
W, H = 1600, 1000
im = Image.new('RGB', (W, H), PAPER)
dr = ImageDraw.Draw(im)
M = 80
dr.line([(M, 64), (M + 84, 64)], fill=CLARET, width=6)
tracked(dr, (M, 82), 'THREE FATES', ImageFont.truetype(SERIFB, 38), INK, track=9)
dr.text((M, 140), 'Three shows, three fates',
        font=ImageFont.truetype(SERIFB, 72), fill=INK)
dr.text((M, 232), 'Per-episode Nielsen linear viewership, 2008\u20132022 (millions of US viewers)',
        font=ImageFont.truetype(SERIF, 34), fill=MUTED)
lx = M
leg_f = ImageFont.truetype(SANS, 28)
for name, color in SHOWS:
    dr.ellipse([lx, 300, lx + 20, 320], fill=color)
    lx += 32
    dr.text((lx, 292), name, font=leg_f, fill=INK)
    lx += dr.textlength(name, font=leg_f) + 44
chart(dr, M + 56, 380, W - M, 860, 6, years=True)
dr.text((M, 912), 'Sources: TV by the Numbers / ShowBuzzDaily via Wikipedia episode lists.',
        font=ImageFont.truetype(SANS, 24), fill=MUTED)
dr.text((W - M, 912), 'OC', font=ImageFont.truetype(SANS, 24), fill=MUTED, anchor='ra')
im.save(f'{BASE}/share/reddit-versus.png')
print('wrote share/reddit-versus.png')
