import json, math, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
repo = sys.argv[1]
d = json.load(open(f'{repo}/data/collisions.json'))
F = '/usr/share/fonts/opentype/inter/'
BG = (236, 237, 239)
x0, x1, y0, y1 = 19.3, 28.4, 34.7, 41.9
k = math.cos(math.radians(38.3))

def draw_map(img, box, blur=5, gain=9):
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
    img.paste(Image.new('RGB', (W, H), (255, 107, 61)), (0, 0), glow)
    img.paste(Image.new('RGB', (W, H), (122, 21, 0)), (0, 0), core)

# share card 1200x630
W, H = 1200, 630
img = Image.new('RGB', (W, H), BG)
draw_map(img, (630, 24, 1176, 606))
dr = ImageDraw.Draw(img)
dr.rounded_rectangle((40, 40, 600, 590), radius=28, fill=(22, 27, 34))
title = ImageFont.truetype(F + 'Inter-Bold.otf', 72)
sub = ImageFont.truetype(F + 'Inter-Regular.otf', 32)
stat = ImageFont.truetype(F + 'Inter-SemiBold.otf', 30)
small = ImageFont.truetype(F + 'Inter-Regular.otf', 21)
dr.text((84, 86), 'Δεν είναι', font=title, fill=(232, 236, 241))
dr.text((84, 166), 'ατύχημα', font=title, fill=(255, 210, 63))
for i, line in enumerate(['Τροχαίες συγκρούσεις και', 'διακομιδές στην Ελλάδα,', '2020–2025']):
    dr.text((84, 276 + 42 * i), line, font=sub, fill=(185, 196, 210))
dr.line((84, 424, 556, 424), fill=(42, 49, 60), width=2)
dr.text((84, 444), '84.331 συγκρούσεις', font=stat, fill=(255, 107, 61))
dr.text((84, 484), '119.897 διακομιδές', font=stat, fill=(76, 194, 255))
dr.text((84, 548), 'Πηγή: accidents.maps.gov.gr', font=small, fill=(120, 130, 142))
img.save(f'{repo}/og.png', optimize=True)

# square icon: map only
ic = Image.new('RGB', (512, 512), BG)
draw_map(ic, (28, 28, 484, 484), blur=4, gain=10)
ic.save(f'{repo}/icon-512.png', optimize=True)
ic.resize((180, 180), Image.LANCZOS).save(f'{repo}/apple-touch-icon.png', optimize=True)
ic.resize((32, 32), Image.LANCZOS).save(f'{repo}/favicon.png', optimize=True)
print('ok')
