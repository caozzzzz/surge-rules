from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import math

SIZE = 256
OUT = Path(__file__).resolve().parents[1] / "icons"
OUT.mkdir(parents=True, exist_ok=True)


def font(size: int):
    candidates = [
        "C:/Windows/Fonts/seguisb.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            pass
    return ImageFont.load_default()


def canvas(top, bottom):
    image = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    gradient = Image.new("RGBA", (SIZE, SIZE))
    pixels = gradient.load()
    for y in range(SIZE):
        t = y / (SIZE - 1)
        color = tuple(round(top[i] * (1 - t) + bottom[i] * t) for i in range(3)) + (255,)
        for x in range(SIZE):
            pixels[x, y] = color
    mask = Image.new("L", (SIZE, SIZE), 0)
    ImageDraw.Draw(mask).rounded_rectangle((8, 8, 248, 248), radius=58, fill=255)
    image.paste(gradient, (0, 0), mask)
    return image, ImageDraw.Draw(image)


def centered(draw, text, size=86, y=126):
    f = font(size)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((SIZE - (box[2] - box[0])) / 2, y - (box[3] - box[1]) / 2 - box[1]), text, font=f, fill="white")


def save(name, colors, painter):
    image, draw = canvas(*colors)
    painter(draw)
    image.save(OUT / f"{name}.png", optimize=True)


def plane(draw):
    draw.polygon([(45, 126), (211, 52), (161, 207), (123, 151), (84, 176), (93, 139)], fill="white")
    draw.polygon([(93, 139), (177, 83), (123, 151)], fill=(210, 230, 255))


def rocket(draw):
    draw.ellipse((94, 42, 186, 170), fill="white")
    draw.polygon([(95, 126), (61, 178), (104, 169)], fill="white")
    draw.polygon([(177, 126), (202, 185), (163, 169)], fill="white")
    draw.ellipse((120, 73, 158, 111), fill=(54, 105, 255))
    draw.polygon([(117, 166), (154, 166), (136, 222)], fill=(255, 199, 52))


def play(draw, music=False):
    if music:
        draw.ellipse((46, 46, 210, 210), outline="white", width=17)
        draw.ellipse((76, 76, 180, 180), fill="white")
        draw.polygon([(119, 102), (119, 158), (163, 130)], fill=(229, 22, 54))
    else:
        draw.rounded_rectangle((43, 72, 213, 184), radius=34, fill="white")
        draw.polygon([(113, 100), (113, 156), (164, 128)], fill=(255, 34, 45))


def spotify(draw):
    for i, width in enumerate((15, 13, 11)):
        y = 91 + i * 35
        points = []
        for x in range(65, 196, 4):
            arc = math.sin((x - 65) / 130 * math.pi) * (18 - i * 3)
            points.append((x, y - arc))
        draw.line(points, fill="white", width=width)


def sparkle(draw):
    draw.polygon([(128, 42), (144, 103), (205, 128), (144, 145), (128, 210), (111, 145), (50, 128), (111, 103)], fill="white")
    draw.ellipse((178, 48, 204, 74), fill=(202, 244, 255))


def shield(draw):
    draw.polygon([(128, 39), (205, 70), (194, 158), (128, 215), (62, 158), (51, 70)], fill="white")
    draw.line((91, 91, 165, 165), fill=(231, 56, 70), width=20)
    draw.line((165, 91, 91, 165), fill=(231, 56, 70), width=20)


def apple(draw, ai=False):
    draw.ellipse((72, 88, 142, 187), fill="white")
    draw.ellipse((113, 88, 184, 187), fill="white")
    draw.polygon([(92, 170), (164, 170), (145, 211), (111, 211)], fill="white")
    draw.ellipse((134, 48, 169, 78), fill="white")
    if ai:
        draw.polygon([(185, 44), (193, 66), (215, 74), (193, 82), (185, 104), (177, 82), (155, 74), (177, 66)], fill=(255, 220, 61))


def tiktok(draw):
    draw.line((135, 68, 135, 161), fill=(37, 244, 238), width=28)
    draw.line((135, 75, 188, 99), fill=(37, 244, 238), width=22)
    draw.ellipse((69, 143, 139, 213), fill=(37, 244, 238))
    draw.line((143, 62, 143, 155), fill="white", width=22)
    draw.line((143, 69, 194, 92), fill="white", width=17)
    draw.ellipse((77, 137, 143, 203), fill="white")


save("airport", ((60, 112, 255), (77, 67, 220)), plane)
save("united-states", ((42, 83, 180), (214, 49, 62)), lambda d: centered(d, "US", 82))
save("hong-kong", ((226, 35, 57), (166, 18, 42)), lambda d: centered(d, "HK", 78))
save("singapore", ((238, 50, 69), (177, 20, 53)), lambda d: centered(d, "SG", 78))
save("taiwan", ((46, 88, 190), (220, 43, 58)), lambda d: centered(d, "TW", 78))
save("proxy", ((91, 66, 245), (45, 151, 255)), rocket)
save("final", ((30, 184, 134), (14, 128, 108)), lambda d: (d.line((68, 132, 112, 176), fill="white", width=24), d.line((112, 176, 192, 82), fill="white", width=24)))
save("netflix", ((32, 32, 38), (5, 5, 8)), lambda d: centered(d, "N", 130))
save("telegram", ((54, 174, 238), (29, 122, 205)), plane)
save("x", ((38, 38, 42), (4, 4, 5)), lambda d: centered(d, "X", 120))
save("tiktok", ((38, 38, 45), (8, 8, 12)), tiktok)
save("ai", ((123, 61, 242), (21, 186, 213)), sparkle)
save("spotify", ((30, 215, 96), (15, 135, 66)), spotify)
save("youtube", ((255, 62, 62), (210, 9, 34)), lambda d: play(d, False))
save("youtube-music", ((246, 46, 66), (172, 8, 38)), lambda d: play(d, True))
save("apple-ai", ((95, 73, 230), (30, 190, 205)), lambda d: apple(d, True))
save("apple", ((83, 88, 101), (28, 30, 36)), lambda d: apple(d, False))
save("adblock", ((244, 74, 84), (181, 27, 52)), shield)

print(f"Generated 18 icons in {OUT}")
