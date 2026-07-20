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


def centered(draw, text, size=86, y=126, fill="white"):
    f = font(size)
    box = draw.textbbox((0, 0), text, font=f)
    draw.text(((SIZE - (box[2] - box[0])) / 2, y - (box[3] - box[1]) / 2 - box[1]), text, font=f, fill=fill)


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


def flag_frame(draw):
    draw.rounded_rectangle((36, 67, 220, 189), radius=13, fill=(255, 255, 255, 70), outline="white", width=5)


def flag_us(draw):
    flag_frame(draw)
    for i in range(7):
        y = 72 + i * 16
        draw.rectangle((41, y, 215, y + 8), fill=(214, 35, 53))
    draw.rectangle((41, 72, 119, 132), fill=(30, 67, 138))
    for row in range(3):
        for col in range(4):
            x, y = 52 + col * 18, 82 + row * 18
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="white")


def flag_hk(draw):
    flag_frame(draw)
    draw.rounded_rectangle((41, 72, 215, 184), radius=8, fill=(222, 35, 55))
    for angle in range(0, 360, 72):
        a = math.radians(angle - 90)
        cx, cy = 128 + math.cos(a) * 25, 128 + math.sin(a) * 25
        draw.ellipse((cx - 10, cy - 20, cx + 10, cy + 10), fill="white")
    draw.ellipse((123, 123, 133, 133), fill=(222, 35, 55))


def flag_sg(draw):
    flag_frame(draw)
    draw.rounded_rectangle((41, 72, 215, 184), radius=8, fill="white")
    draw.rounded_rectangle((41, 72, 215, 130), radius=8, fill=(237, 41, 57))
    draw.rectangle((41, 121, 215, 130), fill=(237, 41, 57))
    draw.ellipse((56, 81, 94, 119), fill="white")
    draw.ellipse((67, 81, 99, 113), fill=(237, 41, 57))
    for x, y in ((107, 88), (118, 96), (114, 110), (100, 110), (96, 96)):
        draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill="white")


def flag_tw(draw):
    flag_frame(draw)
    draw.rounded_rectangle((41, 72, 215, 184), radius=8, fill=(221, 40, 48))
    draw.rectangle((41, 72, 125, 130), fill=(18, 57, 125))
    draw.ellipse((72, 84, 104, 116), fill="white")
    draw.ellipse((80, 92, 96, 108), fill=(18, 57, 125))


def cycle(draw):
    draw.arc((52, 54, 204, 202), 205, 350, fill="white", width=22)
    draw.arc((52, 54, 204, 202), 25, 170, fill="white", width=22)
    draw.polygon([(197, 80), (217, 119), (172, 116)], fill="white")
    draw.polygon([(59, 176), (39, 137), (84, 140)], fill="white")


def x_logo(draw):
    # Official X-inspired asymmetric crossed ribbons.
    draw.polygon([(59, 55), (93, 55), (198, 201), (164, 201)], fill="white")
    draw.polygon([(170, 55), (198, 55), (84, 201), (56, 201)], fill="white")


def netflix_logo(draw):
    # Three-ribbon construction remains legible even at Surge's small icon size.
    draw.rectangle((70, 52, 101, 204), fill=(181, 0, 17))
    draw.rectangle((155, 52, 186, 204), fill=(181, 0, 17))
    draw.polygon([(70, 52), (101, 52), (186, 204), (155, 204)], fill=(229, 9, 20))


def shield(draw):
    draw.polygon([(128, 39), (205, 70), (194, 158), (128, 215), (62, 158), (51, 70)], fill="white")
    draw.line((91, 91, 165, 165), fill=(231, 56, 70), width=20)
    draw.line((165, 91, 91, 165), fill=(231, 56, 70), width=20)


def apple(draw, ai=False):
    # Recognizable Apple-inspired silhouette: twin shoulders, lower lobes, leaf and bite.
    draw.ellipse((58, 86, 145, 180), fill="white")
    draw.ellipse((105, 80, 190, 180), fill="white")
    draw.polygon([(66, 132), (185, 128), (174, 178), (151, 211), (123, 214), (94, 190)], fill="white")
    draw.ellipse((135, 43, 173, 76), fill="white")
    # Match the local gradient so the bite reads as a cut-out instead of a dark dot.
    draw.ellipse((169, 91, 205, 127), fill=(63, 123, 194) if ai else (60, 63, 74))
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
save("united-states", ((42, 83, 180), (214, 49, 62)), flag_us)
save("hong-kong", ((226, 35, 57), (166, 18, 42)), flag_hk)
save("singapore", ((238, 50, 69), (177, 20, 53)), flag_sg)
save("taiwan", ((46, 88, 190), (220, 43, 58)), flag_tw)
save("proxy", ((91, 66, 245), (45, 151, 255)), rocket)
save("final", ((30, 184, 134), (14, 128, 108)), cycle)
save("netflix-v3", ((40, 40, 46), (4, 4, 7)), netflix_logo)
save("telegram", ((54, 174, 238), (29, 122, 205)), plane)
save("x-v3", ((54, 58, 68), (8, 9, 12)), x_logo)
save("tiktok", ((38, 38, 45), (8, 8, 12)), tiktok)
save("ai", ((123, 61, 242), (21, 186, 213)), sparkle)
save("spotify", ((30, 215, 96), (15, 135, 66)), spotify)
save("youtube", ((255, 62, 62), (210, 9, 34)), lambda d: play(d, False))
save("youtube-music", ((246, 46, 66), (172, 8, 38)), lambda d: play(d, True))
save("apple-ai-v4", ((95, 73, 230), (30, 190, 205)), lambda d: apple(d, True))
save("apple-v4", ((83, 88, 101), (28, 30, 36)), lambda d: apple(d, False))
save("adblock", ((244, 74, 84), (181, 27, 52)), shield)

print(f"Generated 18 icons in {OUT}")
