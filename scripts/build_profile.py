"""Render an original pixel world without network calls, fonts, or API keys."""

from pathlib import Path
import math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
C = dict(bg="#11151d", panel="#19212c", line="#344050", muted="#a2afbf",
         ink="#f2f5eb", lime="#d8ff76", blue="#9dbdff", pink="#ffadce", soil="#222d3b")
# Original 5 x 7 bitmap alphabet: no OS-specific font dependency.
BITMAPS = {
    "A":"01110/10001/10001/11111/10001/10001/10001",
    "B":"11110/10001/10001/11110/10001/10001/11110",
    "C":"01111/10000/10000/10000/10000/10000/01111",
    "D":"11110/10001/10001/10001/10001/10001/11110",
    "E":"11111/10000/10000/11110/10000/10000/11111",
    "F":"11111/10000/10000/11110/10000/10000/10000",
    "G":"01111/10000/10000/10111/10001/10001/01111",
    "H":"10001/10001/10001/11111/10001/10001/10001",
    "I":"11111/00100/00100/00100/00100/00100/11111",
    "J":"00111/00010/00010/00010/10010/10010/01100",
    "K":"10001/10010/10100/11000/10100/10010/10001",
    "L":"10000/10000/10000/10000/10000/10000/11111",
    "M":"10001/11011/10101/10101/10001/10001/10001",
    "N":"10001/11001/10101/10011/10001/10001/10001",
    "O":"01110/10001/10001/10001/10001/10001/01110",
    "P":"11110/10001/10001/11110/10000/10000/10000",
    "Q":"01110/10001/10001/10001/10101/10010/01101",
    "R":"11110/10001/10001/11110/10100/10010/10001",
    "S":"01111/10000/10000/01110/00001/00001/11110",
    "T":"11111/00100/00100/00100/00100/00100/00100",
    "U":"10001/10001/10001/10001/10001/10001/01110",
    "V":"10001/10001/10001/10001/10001/01010/00100",
    "W":"10001/10001/10001/10101/10101/10101/01010",
    "X":"10001/10001/01010/00100/01010/10001/10001",
    "Y":"10001/10001/01010/00100/00100/00100/00100",
    "Z":"11111/00001/00010/00100/01000/10000/11111",
    "0":"01110/10001/10011/10101/11001/10001/01110",
    "1":"00100/01100/00100/00100/00100/00100/01110",
    "+":"00000/00100/00100/11111/00100/00100/00000",
    "/":"00001/00001/00010/00100/01000/10000/10000",
    ".":"00000/00000/00000/00000/00000/00110/00110",
    " ":"00000/00000/00000/00000/00000/00000/00000",
}


def text(draw, value, x, y, color="ink", scale=1):
    for index, char in enumerate(value):
        for row, bits in enumerate(BITMAPS[char].split("/")):
            for col, bit in enumerate(bits):
                if bit == "1":
                    px, py = x + (index * 6 + col) * scale, y + row * scale
                    draw.rectangle((px, py, px + scale - 1, py + scale - 1), fill=C[color])


def star(draw, x, y, color="lime", size=2):
    draw.line((x - size, y, x + size, y), fill=C[color])
    draw.line((x, y - size, x, y + size), fill=C[color])


def avatar(draw, x, feet, tick, facing):
    sprite = ["..HHHH..", ".HHHHHH.", ".HSSSS..", "..SSSES.",
              "...SS...", "..BBBB..", ".SBBBBS.", "..BBBB..",
              "..PPPP..", "..PPPP..", "..P..P..", ".PP..PP."]
    palette = dict(H="ink", S="pink", E="bg", B="blue", P="muted")
    for row, line in enumerate(sprite):
        for col, bit in enumerate(line[::facing]):
            if bit != ".":
                dx = tick % 2 if row >= 10 else 0
                draw.point((x + col + dx, feet - 12 + row), fill=C[palette[bit]])


MONOGRAM = (ASSETS / "monogram.txt").read_text().splitlines()


def frame(index):
    image = Image.new("RGB", (480, 208), C["bg"])
    d = ImageDraw.Draw(image)
    d.rectangle((0, 0, 479, 207), outline=C["line"])
    d.rectangle((1, 1, 478, 30), fill=C["panel"])
    star(d, 17, 15)
    text(d, "CIDLINA / WORLD 01", 28, 12)
    text(d, "PERSONAL SPACE", 378, 12, "muted")
    for row, line in enumerate(MONOGRAM):
        for col, char in enumerate(line):
            if char == "A":
                x, y = 26 + col * 3, 53 + row * 5
                d.rectangle((x, y, x + 2, y + 3), fill=C["lime"])
    text(d, "ONE IDEA LEADS TO ANOTHER.", 22, 160, "muted")
    d.line((193, 49, 193, 168), fill=C["line"])
    text(d, "PLAYER 01", 217, 47, "lime")
    text(d, "JAN", 215, 65, scale=3)
    text(d, "CIDLINA", 215, 95, scale=3)
    text(d, "DESIGN + WORDS + TECH", 217, 132, "blue")
    text(d, "MAKE IT MAKE SENSE.", 217, 148, "muted")
    for x, y, offset in [(174,47,0), (16,89,13), (172,144,29), (452,66,41)]:
        star(d, x, y, "pink" if (index + offset) % 40 < 20 else "line", 1)
    d.rectangle((1, 186, 478, 206), fill=C["soil"])
    d.line((1, 185, 478, 185), fill=C["lime"])
    for x in range(5, 478, 12):
        d.line((x, 191, x + 3, 191), fill=C["line"])
        d.point((x + 7, 201), fill=C["line"])
    text(d, "COLLECT IDEAS.", 22, 175, "muted")
    phase = index / 96
    position = 217 + round(224 * (1 - abs(2 * phase - 1)))
    jump = round(15 * max(0, 1 - abs(position - 326) / 23))
    avatar(d, position, 185 - jump, index // 3, 1 if phase < .5 else -1)
    collected = 25 <= index < 48 or 73 <= index < 96
    if not collected:
        star(d, 330, 161 + round(2 * math.sin(index * math.pi / 12)), size=3)
    if 25 <= index < 38 or 73 <= index < 86:
        text(d, "IDEA +1", 345, 163 - (index % 24) // 3, "lime")
    return image.resize((960, 416), Image.Resampling.NEAREST)


def main():
    frames = [frame(index) for index in range(96)]
    frames[0].save(ASSETS / "profile.png", optimize=True)
    palette = frames[0].quantize(colors=16, dither=Image.Dither.NONE)
    indexed = [im.quantize(palette=palette, dither=Image.Dither.NONE) for im in frames]
    indexed[0].save(ASSETS / "profile.gif", save_all=True, append_images=indexed[1:],
                    duration=100, loop=0, optimize=True, disposal=1)
    print(f"Rendered {len(frames)} frames; {(ASSETS / 'profile.gif').stat().st_size:,} bytes")


if __name__ == "__main__":
    main()
