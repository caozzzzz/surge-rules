from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'icons' / 'source'
OUT = ROOT / 'icons'
SIZE = 256
CONTENT_SIZE = 208
NAMES = (
    'airport', 'united-states', 'hong-kong', 'singapore', 'taiwan',
    'proxy', 'final', 'netflix', 'telegram', 'x', 'tiktok', 'ai',
    'spotify', 'youtube', 'youtube-music', 'apple-ai', 'apple', 'adblock',
)
# Preserve URLs used by older downloaded configurations.
ALIASES = {
    'netflix': ('netflix-v3',),
    'x': ('x-v3',),
    'apple': ('apple-v3', 'apple-v4', 'apple-v5', 'apple-v6'),
    'apple-ai': ('apple-ai-v4', 'apple-ai-v5', 'apple-ai-v6'),
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name in NAMES:
        with Image.open(SOURCE / f'{name}.png') as source:
            artwork = source.convert('RGBA')
        bounds = artwork.getchannel('A').getbbox()
        if bounds is None:
            raise ValueError(f'Empty icon source: {name}')
        artwork = artwork.crop(bounds)
        artwork.thumbnail((CONTENT_SIZE, CONTENT_SIZE), Image.Resampling.LANCZOS)
        image = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
        image.alpha_composite(artwork, ((SIZE - artwork.width) // 2, (SIZE - artwork.height) // 2))
        for filename in (name, *ALIASES.get(name, ())):
            image.save(OUT / f'{filename}.png', optimize=True)
    print(f'Generated {len(NAMES)} Essential icons and compatibility aliases')


if __name__ == '__main__':
    main()
