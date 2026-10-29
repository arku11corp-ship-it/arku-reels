import sys
from PIL import Image, ImageDraw
im = Image.open(sys.argv[1]).convert('RGBA'); ov = Image.new('RGBA', im.size, (0,0,0,0)); d = ImageDraw.Draw(ov)
R = (255, 0, 0, 90)
d.rectangle([0, 0, 1080, 240], fill=R); d.rectangle([0, 1470, 1080, 1920], fill=R)   # top UI / feed crop, bottom caption UI
d.rectangle([0, 0, 35, 1920], fill=R); d.rectangle([1045, 0, 1080, 1920], fill=R); d.rectangle([945, 1220, 1045, 1470], fill=R)
Image.alpha_composite(im, ov).convert('RGB').resize((360, 640)).save(sys.argv[2])
