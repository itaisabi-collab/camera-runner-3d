"""
Generate Google Play Store assets for RUN! 3D - Camera Runner
- 512x512 app icon
- 2x phone screenshots (1080x1920)
"""
from PIL import Image, ImageDraw, ImageFont
import math, os

out = os.path.dirname(os.path.abspath(__file__))

# Helper: find a bold font
def get_font(size, bold=True):
    paths = [
        'C:/Windows/Fonts/arialbd.ttf',
        'C:/Windows/Fonts/arial.ttf',
        'C:/Windows/Fonts/Impact.ttf',
    ]
    if not bold:
        paths = ['C:/Windows/Fonts/arial.ttf'] + paths
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def get_impact(size):
    p = 'C:/Windows/Fonts/impact.ttf'
    if os.path.exists(p):
        return ImageFont.truetype(p, size)
    return get_font(size)

# Gradient helper
def gradient(draw, w, h, c1, c2):
    for y in range(h):
        r = int(c1[0] + (c2[0]-c1[0])*y/h)
        g = int(c1[1] + (c2[1]-c1[1])*y/h)
        b = int(c1[2] + (c2[2]-c1[2])*y/h)
        draw.line([(0,y),(w,y)], fill=(r,g,b))

def draw_runner(d, cx, cy, scale=1.0, color=(255,255,255)):
    """Draw a running figure silhouette"""
    s = scale
    # Head
    d.ellipse([cx-12*s, cy-65*s, cx+12*s, cy-40*s], fill=color)
    # Body
    d.line([(cx, cy-40*s), (cx-5*s, cy+10*s)], fill=color, width=int(8*s))
    # Front leg (extended)
    d.line([(cx-5*s, cy+10*s), (cx+25*s, cy+5*s)], fill=color, width=int(7*s))
    d.line([(cx+25*s, cy+5*s), (cx+30*s, cy+25*s)], fill=color, width=int(6*s))
    # Back leg (bent back)
    d.line([(cx-5*s, cy+10*s), (cx-25*s, cy+30*s)], fill=color, width=int(7*s))
    d.line([(cx-25*s, cy+30*s), (cx-15*s, cy+10*s)], fill=color, width=int(6*s))
    # Front arm
    d.line([(cx, cy-30*s), (cx-25*s, cy-10*s)], fill=color, width=int(6*s))
    # Back arm
    d.line([(cx, cy-30*s), (cx+20*s, cy-15*s)], fill=color, width=int(6*s))

# ============================================================
# 1. APP ICON 512x512
# ============================================================
print("Creating app icon...")
icon = Image.new('RGBA', (512, 512), (0,0,0,0))
bg = Image.new('RGB', (512, 512))
d = ImageDraw.Draw(bg)

# Vibrant blue-to-purple gradient
gradient(d, 512, 512, (30, 100, 255), (160, 30, 220))

# Decorative glow circles
overlay = Image.new('RGBA', (512,512), (0,0,0,0))
od = ImageDraw.Draw(overlay)
for cx, cy, rad, alpha in [(400,100,80,40),(100,420,60,30),(450,400,50,25),(60,80,40,20)]:
    od.ellipse([cx-rad, cy-rad, cx+rad, cy+rad], fill=(255,255,255,alpha))
bg = Image.alpha_composite(bg.convert('RGBA'), overlay).convert('RGB')

d = ImageDraw.Draw(bg)

# Speed lines behind runner position
for i in range(8):
    y = 270 + i * 25
    x_start = 50 + i*12
    x_end = 140 + i*8
    d.line([(x_start, y), (x_end, y)], fill=(255,255,255), width=3)

# Draw running figure
draw_runner(d, 220, 340, scale=2.2, color=(255,255,255))

# "RUN!" text
font_big = get_impact(150)
text = 'RUN!'
bbox = d.textbbox((0,0), text, font=font_big)
tw = bbox[2] - bbox[0]
tx = (512 - tw) // 2 + 50
ty = 30

# Black outline
for ox in range(-5, 6):
    for oy in range(-5, 6):
        if abs(ox) + abs(oy) > 0:
            d.text((tx+ox, ty+oy), text, fill=(0,0,0), font=font_big)
# Yellow/gold text
d.text((tx, ty), text, fill=(255, 230, 50), font=font_big)

# "3D" subtitle
font_sub = get_impact(55)
sub = '3D'
bbox2 = d.textbbox((0,0), sub, font=font_sub)
sw = bbox2[2] - bbox2[0]
sx = tx + tw + 5
sy = ty + 90

for ox in range(-3, 4):
    for oy in range(-3, 4):
        if abs(ox) + abs(oy) > 0:
            d.text((sx+ox, sy+oy), sub, fill=(0,0,0), font=font_sub)
d.text((sx, sy), sub, fill=(0,255,200), font=font_sub)

# Rounded corners mask
mask = Image.new('L', (512,512), 0)
md = ImageDraw.Draw(mask)
md.rounded_rectangle([0,0,511,511], radius=90, fill=255)

icon = bg.convert('RGBA')
icon.putalpha(mask)
icon.save(os.path.join(out, 'icon-512.png'))
print('  -> icon-512.png saved!')


# ============================================================
# 2. SCREENSHOT 1 - "Play with your BODY!" (1080x1920)
# ============================================================
print("Creating screenshot 1...")
ss1 = Image.new('RGB', (1080, 1920))
d1 = ImageDraw.Draw(ss1)

# Dark blue to purple gradient
gradient(d1, 1080, 1920, (20, 10, 80), (80, 10, 120))

# Glow circles
overlay = Image.new('RGBA', (1080,1920), (0,0,0,0))
od = ImageDraw.Draw(overlay)
for cx,cy,rad,al in [(540,500,300,25),(200,1400,200,20),(900,300,150,20),(540,1200,250,15)]:
    od.ellipse([cx-rad,cy-rad,cx+rad,cy+rad], fill=(100,50,255,al))
ss1 = Image.alpha_composite(ss1.convert('RGBA'), overlay).convert('RGB')
d1 = ImageDraw.Draw(ss1)

# Title: "PLAY WITH YOUR"
font_title = get_impact(90)
font_title2 = get_impact(120)

title1 = 'PLAY WITH YOUR'
bbox = d1.textbbox((0,0), title1, font=font_title)
tw = bbox[2]-bbox[0]
tx = (1080-tw)//2
ty = 140

for ox in range(-3,4):
    for oy in range(-3,4):
        if abs(ox)+abs(oy)>0:
            d1.text((tx+ox,ty+oy), title1, fill=(0,0,0), font=font_title)
d1.text((tx,ty), title1, fill=(255,255,255), font=font_title)

# "BODY!"
title2 = 'BODY!'
bbox = d1.textbbox((0,0), title2, font=font_title2)
tw = bbox[2]-bbox[0]
tx = (1080-tw)//2
ty2 = ty + 100

for ox in range(-4,5):
    for oy in range(-4,5):
        if abs(ox)+abs(oy)>0:
            d1.text((tx+ox,ty2+oy), title2, fill=(0,0,0), font=font_title2)
d1.text((tx,ty2), title2, fill=(0,255,200), font=font_title2)

# Camera lens graphic
cx, cy = 540, 650
d1.ellipse([cx-180, cy-180, cx+180, cy+180], fill=(40,40,60), outline=(100,100,140), width=8)
d1.ellipse([cx-140, cy-140, cx+140, cy+140], fill=(20,20,40), outline=(60,60,100), width=4)
d1.ellipse([cx-100, cy-100, cx+100, cy+100], fill=(30,30,60), outline=(80,80,120), width=3)
# Center lens glow
for r in range(70, 0, -2):
    c_val = int(150*(70-r)/70)
    col = (50 + c_val, 100 + int(100*(70-r)/70), 255)
    d1.ellipse([cx-r, cy-r, cx+r, cy+r], fill=col)
# Lens highlight
d1.ellipse([cx-30, cy-50, cx+10, cy-20], fill=(200,220,255))

# Person silhouette below camera
pcx, pcy = 540, 960
# Glow behind person
for r in range(150, 0, -3):
    c = int(40 * r / 150)
    d1.ellipse([pcx-r, pcy-r+20, pcx+r, pcy+r+20], fill=(c, c, c+30))

draw_runner(d1, pcx, pcy, scale=3.0, color=(0,255,200))

# Direction arrows
font_arrow = get_impact(120)
d1.text((120, 900), '<', fill=(255,230,50), font=font_arrow)
d1.text((820, 900), '>', fill=(255,230,50), font=font_arrow)

# Up arrow (jump)
d1.polygon([(540,1120),(490,1180),(590,1180)], fill=(255,230,50))
# Down arrow (duck)
d1.polygon([(540,1260),(490,1200),(590,1200)], fill=(255,100,100))

# Labels
font_label = get_impact(45)
d1.text((80, 1030), 'MOVE', fill=(255,255,255), font=font_label)
d1.text((810, 1030), 'MOVE', fill=(255,255,255), font=font_label)

font_sm = get_impact(38)
d1.text((460, 1090), 'JUMP!', fill=(255,230,50), font=font_sm)
d1.text((460, 1270), 'DUCK!', fill=(255,100,100), font=font_sm)

# Bottom text
font_bot = get_impact(60)
bot_text = 'NO CONTROLLER NEEDED'
bbox = d1.textbbox((0,0), bot_text, font=font_bot)
tw = bbox[2]-bbox[0]
d1.text(((1080-tw)//2, 1500), bot_text, fill=(255,230,50), font=font_bot)

bot2 = 'USE YOUR CAMERA!'
bbox = d1.textbbox((0,0), bot2, font=font_bot)
tw = bbox[2]-bbox[0]
d1.text(((1080-tw)//2, 1580), bot2, fill=(255,255,255), font=font_bot)

# App name at bottom
font_app = get_impact(55)
app = 'RUN! 3D'
bbox = d1.textbbox((0,0), app, font=font_app)
tw = bbox[2]-bbox[0]
for ox in range(-2,3):
    for oy in range(-2,3):
        if abs(ox)+abs(oy)>0:
            d1.text(((1080-tw)//2+ox, 1780+oy), app, fill=(0,0,0), font=font_app)
d1.text(((1080-tw)//2, 1780), app, fill=(0,255,200), font=font_app)

ss1.save(os.path.join(out, 'screenshot1.png'))
print('  -> screenshot1.png saved!')


# ============================================================
# 3. SCREENSHOT 2 - "8 Meme Characters!" (1080x1920)
# ============================================================
print("Creating screenshot 2...")
ss2 = Image.new('RGB', (1080, 1920))
d2 = ImageDraw.Draw(ss2)

# Purple to pink gradient
gradient(d2, 1080, 1920, (60, 10, 100), (150, 20, 80))

# Glow
overlay2 = Image.new('RGBA', (1080,1920), (0,0,0,0))
od2 = ImageDraw.Draw(overlay2)
for cx2,cy2,rad,al in [(540,400,300,20),(300,1000,200,15),(800,1300,200,15)]:
    od2.ellipse([cx2-rad,cy2-rad,cx2+rad,cy2+rad], fill=(255,50,150,al))
ss2 = Image.alpha_composite(ss2.convert('RGBA'), overlay2).convert('RGB')
d2 = ImageDraw.Draw(ss2)

# Title: "8 MEME"
font_t1 = get_impact(100)
font_t2 = get_impact(120)

t1 = '8 MEME'
bbox = d2.textbbox((0,0), t1, font=font_t1)
tw = bbox[2]-bbox[0]
tx = (1080-tw)//2
ty = 100
for ox in range(-3,4):
    for oy in range(-3,4):
        if abs(ox)+abs(oy)>0:
            d2.text((tx+ox,ty+oy), t1, fill=(0,0,0), font=font_t1)
d2.text((tx,ty), t1, fill=(255,230,50), font=font_t1)

# "CHARACTERS!"
t2 = 'CHARACTERS!'
bbox = d2.textbbox((0,0), t2, font=font_t2)
tw = bbox[2]-bbox[0]
tx = (1080-tw)//2
ty2 = ty + 110
for ox in range(-4,5):
    for oy in range(-4,5):
        if abs(ox)+abs(oy)>0:
            d2.text((tx+ox,ty2+oy), t2, fill=(0,0,0), font=font_t2)
d2.text((tx,ty2), t2, fill=(255,255,255), font=font_t2)

# Character grid - 2 rows of 4
char_colors = [
    ((255,80,80), 'RAGE'),
    ((50,200,255), 'DOGE'),
    ((255,200,50), 'TROLL'),
    ((100,255,100), 'PEPE'),
    ((255,150,50), 'NYAN'),
    ((200,100,255), 'CHAD'),
    ((255,100,200), 'AMOGUS'),
    ((150,150,255), 'STONKS'),
]

font_char = get_impact(28)
box_size = 200
gap = 40
start_x = (1080 - (4*box_size + 3*gap)) // 2
start_y = 420

for i, (color, name) in enumerate(char_colors):
    row = i // 4
    col = i % 4
    x = start_x + col * (box_size + gap)
    y = start_y + row * (box_size + gap + 50)

    # Character card background
    d2.rounded_rectangle([x, y, x+box_size, y+box_size], radius=25, fill=(30,20,50), outline=color, width=4)

    # Character body
    ccx = x + box_size//2
    ccy = y + box_size//2 - 10

    # Body
    d2.rounded_rectangle([ccx-35, ccy-10, ccx+35, ccy+55], radius=15, fill=color)
    # Head
    d2.ellipse([ccx-30, ccy-55, ccx+30, ccy+5], fill=color)
    # Eyes (white)
    d2.ellipse([ccx-18, ccy-38, ccx-6, ccy-22], fill=(255,255,255))
    d2.ellipse([ccx+6, ccy-38, ccx+18, ccy-22], fill=(255,255,255))
    # Pupils
    d2.ellipse([ccx-14, ccy-34, ccx-8, ccy-26], fill=(0,0,0))
    d2.ellipse([ccx+8, ccy-34, ccx+14, ccy-26], fill=(0,0,0))
    # Mouth (smile)
    d2.arc([ccx-12, ccy-18, ccx+12, ccy-2], start=0, end=180, fill=(0,0,0), width=2)
    # Legs
    d2.rounded_rectangle([ccx-25, ccy+50, ccx-10, ccy+75], radius=5, fill=color)
    d2.rounded_rectangle([ccx+10, ccy+50, ccx+25, ccy+75], radius=5, fill=color)

    # Name below card
    bbox = d2.textbbox((0,0), name, font=font_char)
    nw = bbox[2]-bbox[0]
    d2.text((x + (box_size-nw)//2, y+box_size+8), name, fill=color, font=font_char)

# "COLLECT COINS" text
font_unlock = get_impact(55)
unlock = 'COLLECT COINS'
bbox = d2.textbbox((0,0), unlock, font=font_unlock)
tw = bbox[2]-bbox[0]
d2.text(((1080-tw)//2, 1200), unlock, fill=(255,230,50), font=font_unlock)

unlock2 = 'TO UNLOCK THEM ALL!'
bbox = d2.textbbox((0,0), unlock2, font=font_unlock)
tw = bbox[2]-bbox[0]
d2.text(((1080-tw)//2, 1270), unlock2, fill=(255,255,255), font=font_unlock)

# Coin graphic
coin_y = 1430
coin_x = 540
# Outer glow
for r in range(70, 60, -1):
    d2.ellipse([coin_x-r, coin_y-r, coin_x+r, coin_y+r], fill=(200,150,0))
# Main coin
d2.ellipse([coin_x-55, coin_y-55, coin_x+55, coin_y+55], fill=(255,220,50))
d2.ellipse([coin_x-45, coin_y-45, coin_x+45, coin_y+45], fill=(255,200,30))
# Dollar sign
font_coin = get_impact(65)
bbox = d2.textbbox((0,0), '$', font=font_coin)
dw = bbox[2]-bbox[0]
dh = bbox[3]-bbox[1]
d2.text((coin_x-dw//2, coin_y-dh//2-5), '$', fill=(180,130,0), font=font_coin)

# Watch ads hint
font_hint = get_impact(40)
hint = 'OR WATCH ADS FOR FREE COINS!'
bbox = d2.textbbox((0,0), hint, font=font_hint)
tw = bbox[2]-bbox[0]
d2.text(((1080-tw)//2, 1550), hint, fill=(200,200,200), font=font_hint)

# App name at bottom
font_app = get_impact(55)
app = 'RUN! 3D'
bbox = d2.textbbox((0,0), app, font=font_app)
tw = bbox[2]-bbox[0]
for ox in range(-2,3):
    for oy in range(-2,3):
        if abs(ox)+abs(oy)>0:
            d2.text(((1080-tw)//2+ox, 1780+oy), app, fill=(0,0,0), font=font_app)
d2.text(((1080-tw)//2, 1780), app, fill=(0,255,200), font=font_app)

ss2.save(os.path.join(out, 'screenshot2.png'))
print('  -> screenshot2.png saved!')

print('\nAll store assets created successfully!')
print(f'Output directory: {out}')
