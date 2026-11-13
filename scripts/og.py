import json, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
repo = sys.argv[1]
d = json.load(open(f'{repo}/data/collisions.json'))
F = '/usr/share/fonts/opentype/inter/'
BG = (236, 237, 239)
x0, x1, y0, y1 = 19.3, 28.4, 34.7, 41.9
k = math.cos(math.radians(38.3))

def draw_map(img, box, blur=5, gain=9, glow_c=(255, 107, 61), core_c=(122, 21, 0)):
    W, H = img.size
    mw, mh = (x1 - x0) * k, (y1 - y0)
    s = min((box[2] - box[0]) / mw, (box[3] - box[1]) / mh)
    ox = box[0] + ((box[2] - box[0]) - mw * s) / 2
    oy = box[1] + ((box[3] - box[1]) - mh * s) / 2
    heat = Image.new('L', (W, H), 0)
    hd = ImageDraw.Draw(heat)
    for x, y in zip(d['x'], d['y']):
        hd.point((ox + (x / 1e5 - x0) * k * s, oy + (y1 - y / 1e5) * s), fill=255)
    glow = heat.filter(ImageFilter.GaussianBlur(blur)).point(lambda v: min(255, int(v * gain * 0.55)))
    core = heat.filter(ImageFilter.GaussianBlur(max(0.8, blur / 4))).point(lambda v: min(255, v * 5))
    img.paste(Image.new('RGB', (W, H), glow_c), (0, 0), glow)
    img.paste(Image.new('RGB', (W, H), core_c), (0, 0), core)

# share card 1200x630; everything sits in the central 600px so side-cropped previews keep it
W, H = 1200, 630
DARK = (22, 27, 34)
img = Image.new('RGB', (W, H), BG)
draw_map(img, (425, 196, 775, 548), blur=4, gain=10, glow_c=(200, 20, 20), core_c=(110, 0, 0))   # blood red
dr = ImageDraw.Draw(img)
title = ImageFont.truetype(F + 'Inter-Bold.otf', 62)
sub = ImageFont.truetype(F + 'Inter-Regular.otf', 26)
stat = ImageFont.truetype(F + 'Inter-SemiBold.otf', 24)
small = ImageFont.truetype(F + 'Inter-Regular.otf', 18)
cx = W // 2
tw1 = dr.textlength('Δεν είναι ', font=title); tw2 = dr.textlength('ατύχημα', font=title)
x = cx - (tw1 + tw2) / 2
dr.text((x, 40), 'Δεν είναι ', font=title, fill=(22, 27, 34))
dr.text((x + tw1, 40), 'ατύχημα', font=title, fill=(138, 3, 3))
dr.text((cx, 120), 'Τροχαίες συγκρούσεις και διακομιδές', font=sub, fill=(70, 78, 90), anchor='mt')
dr.text((cx, 154), 'στην Ελλάδα, 2020–2025', font=sub, fill=(70, 78, 90), anchor='mt')
a, b = '84.331 συγκρούσεις', '119.897 διακομιδές'
gap = 28
wa, wb = dr.textlength(a, font=stat), dr.textlength(b, font=stat)
x = cx - (wa + gap + wb) / 2
dr.text((x, 568), a, font=stat, fill=(138, 3, 3))
dr.text((x + wa + gap, 568), b, font=stat, fill=(0, 92, 150))
dr.text((cx, 606), 'Πηγή: accidents.maps.gov.gr', font=small, fill=(110, 118, 128), anchor='mt')
img.save(f'{repo}/og.png', optimize=True)

# square icon: map only
ic = Image.new('RGB', (512, 512), BG)
draw_map(ic, (28, 28, 484, 484), blur=4, gain=10, glow_c=(200, 20, 20), core_c=(110, 0, 0))
ic.save(f'{repo}/icon-512.png', optimize=True)
ic.resize((180, 180), Image.LANCZOS).save(f'{repo}/apple-touch-icon.png', optimize=True)
ic.resize((32, 32), Image.LANCZOS).save(f'{repo}/favicon.png', optimize=True)
print('ok')
