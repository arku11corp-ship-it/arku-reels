"""Render a 1080x1920 reel from a JSON spec: segments of images (letterboxed on black) with optional text, synced to beats."""
import sys, json, subprocess, numpy as np, librosa
from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H, FPS = 1080, 1920, 30
FONT = "/usr/share/fonts/opentype/inter/InterDisplay-Medium.otf"
spec = json.load(open(sys.argv[1])); out = sys.argv[2]

def fit(img):
    img = img.convert('RGB'); w, h = img.size
    s = W / w; nh = int(h * s)
    if nh > H: s = H / h
    return img.resize((int(w * s), int(h * s)), Image.LANCZOS)

def text_layer(lines, size, cy):
    lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    f = ImageFont.truetype(FONT, size); lh = int(size * 1.25)
    y0 = cy - lh * len(lines) // 2
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    for i, ln in enumerate(lines):
        tw = d.textlength(ln, font=f); x = (W - tw) / 2; y = y0 + i * lh
        ds.text((x, y + 2), ln, font=f, fill=(0, 0, 0, 255), stroke_width=6, stroke_fill=(0, 0, 0, 255))
        d.text((x, y), ln, font=f, fill=(255, 255, 255, 255), stroke_width=2, stroke_fill=(20, 20, 20, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(9)); sh.putalpha(sh.getchannel('A').point(lambda a: min(255, int(a * 1.1))))
    return Image.alpha_composite(sh, lay)

# audio + beat grid
y, sr = librosa.load(spec['audio'], sr=22050, offset=spec.get('audio_start', 0), duration=40)
_, bf = librosa.beat.beat_track(y=y, sr=sr); beats = list(librosa.frames_to_time(bf, sr=sr))
# segment boundaries: each segment lasts n beats (or fixed seconds if 'sec')
if spec.get('start_on_beat') and beats:
    off = beats[0]; spec['audio_start'] = spec.get('audio_start', 0) + off; beats = [b - off for b in beats]
t = 0.0; bounds = []
bi = 0
for seg in spec['segments']:
    if 'sec' in seg: end = t + seg['sec']
    else:
        while bi < len(beats) and beats[bi] <= t + 0.05: bi += 1
        bi2 = min(bi + seg['beats'] - 1, len(beats) - 1); end = beats[bi2]; bi = bi2
    bounds.append((t, end)); t = end
total = t
frames = []
p = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
    '-ss', str(spec.get('audio_start', 0)), '-i', spec['audio'], '-t', f'{total:.3f}',
    '-af', f"afade=t=out:st={max(total-0.35,0):.3f}:d=0.35", '-map', '0:v', '-map', '1:a',
    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '19', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '160k', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
cache = {}
cta = text_layer([spec['cta']], spec.get('cta_size', 50), spec.get('cta_y', 1800)) if spec.get('cta') else None
for (t0, t1), seg in zip(bounds, spec['segments']):
    n = max(1, round((t1 - t0) * FPS))
    if seg.get('image'):
        if seg['image'] not in cache: cache[seg['image']] = fit(Image.open(seg['image']))
        art = cache[seg['image']]
    else: art = None
    tl = text_layer(seg['text'], seg.get('size', 62), seg.get('text_y', 0)) if seg.get('text') else None
    z0, z1 = seg.get('zoom', (1.0, 1.0))
    for k in range(n):
        fr = Image.new('RGB', (W, H), (0, 0, 0))
        if art is not None:
            z = z0 + (z1 - z0) * k / max(n - 1, 1); aw, ah = art.size
            a = art if z == 1 else art.resize((int(aw * z), int(ah * z)), Image.BILINEAR).crop((int(aw*(z-1)/2), int(ah*(z-1)/2), int(aw*(z-1)/2)+aw, int(ah*(z-1)/2)+ah))
            fr.paste(a, ((W - aw) // 2, (H - ah) // 2))
        if tl is not None: fr.paste(tl, (0, 0), tl)
        if cta is not None and not seg.get('no_cta'): fr.paste(cta, (0, 0), cta)
        p.stdin.write(fr.tobytes())
p.stdin.close(); p.wait()
print(out, f"{total:.2f}s", [f"{a:.2f}-{b:.2f}" for a, b in bounds])
