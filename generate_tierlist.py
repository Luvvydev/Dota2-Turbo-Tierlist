from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Dict, List, Tuple

from PIL import Image, ImageDraw, ImageFont

# Repository layout:
# generate_tierlist.py
# assets/dota2-css-hero-sprites/assets/images/minimap_hero_sheet.png
# assets/dota2-css-hero-sprites/assets/stylesheets/dota2minimapheroes.css
BASE_DIR = Path(__file__).resolve().parent
ASSET_ROOT = BASE_DIR / "assets" / "dota2-css-hero-sprites"
SPRITE_PATH = ASSET_ROOT / "assets" / "images" / "minimap_hero_sheet.png"
CSS_PATH = ASSET_ROOT / "assets" / "stylesheets" / "dota2minimapheroes.css"
OUTPUT_PATH = BASE_DIR / "dota2_turbo_tier_list.png"

for required_path in (SPRITE_PATH, CSS_PATH):
    if not required_path.exists():
        raise FileNotFoundError(
            f"Missing required asset: {required_path}\n"
            "Place the dota2-css-hero-sprites package under "
            "assets/dota2-css-hero-sprites/."
        )

tiers: Dict[str, List[str]] = {
    "SUPERSONIC RACING": [
        "Ancient Apparition", "Dark Willow", "Earth Spirit", "Ember Spirit",
        "Nature’s Prophet", "Nyx Assassin", "Snapfire", "Storm Spirit",
        "Void Spirit", "Witch Doctor",
    ],
    "TURBOCHARGED": [
        "Axe", "Bane", "Bloodseeker", "Bounty Hunter", "Centaur Warrunner",
        "Chaos Knight", "Clinkz", "Crystal Maiden", "Dawnbreaker",
        "Drow Ranger", "Earthshaker", "Hoodwink", "Jakiro", "Kez",
        "Legion Commander", "Leshrac", "Lifestealer", "Lion", "Lone Druid",
        "Mars", "Medusa", "Mirana", "Monkey King", "Morphling", "Muerta",
        "Necrophos", "Ogre Magi", "Outworld Destroyer", "Pangolier",
        "Phantom Assassin", "Primal Beast", "Puck", "Pugna", "Razor", "Riki",
        "Sand King", "Shadow Fiend", "Shadow Shaman", "Slardar", "Slark",
        "Sniper", "Spirit Breaker", "Tidehunter", "Tiny", "Troll Warlord",
        "Ursa", "Vengeful Spirit", "Warlock", "Weaver",
    ],
    "SAME SAME BUT DIFFERENT": [
        "Anti Mage", "Batrider", "Brewmaster", "Bristleback", "Clockwerk",
        "Dazzle", "Death Prophet", "Dragon Knight", "Grimstroke", "Huskar",
        "Invoker", "Kunkka", "Largo", "Lich", "Lina", "Magnus", "Marci",
        "Phantom Lancer", "Pudge", "Rubick", "Silencer", "Skywrath Mage",
        "Sven", "Templar Assassin", "Timbersaw", "Tusk", "Underlord",
        "Undying", "Viper", "Visage", "Windranger",
    ],
    "NOT SO GOOD": [
        "Alchemist", "Arc Warden", "Beastmaster", "Broodmother", "Dark Seer",
        "Disruptor", "Elder Titan", "Enchantress", "Faceless Void",
        "Gyrocopter", "Juggernaut", "Keeper of the Light", "Luna", "Lycan",
        "Meepo", "Naga Siren", "Omniknight", "Phoenix", "Queen of Pain",
        "Ringmaster", "Shadow Demon", "Techies", "Tinker", "Treant Protector",
        "Venomancer", "Winter Wyvern", "Wraith King", "Zeus",
    ],
    "GO BACK TO RANKED": [
        "Abaddon", "Chen", "Doom", "Enigma", "Io", "Night Stalker", "Oracle",
        "Spectre", "Terrorblade",
    ],
}

slug_map: Dict[str, str] = {
    "Abaddon": "abaddon",
    "Alchemist": "alchemist",
    "Ancient Apparition": "ancient_apparition",
    "Anti Mage": "antimage",
    "Arc Warden": "arc_warden",
    "Axe": "axe",
    "Bane": "bane",
    "Batrider": "batrider",
    "Beastmaster": "beastmaster",
    "Bloodseeker": "bloodseeker",
    "Bounty Hunter": "bounty_hunter",
    "Brewmaster": "brewmaster",
    "Bristleback": "bristleback",
    "Broodmother": "broodmother",
    "Centaur Warrunner": "centaur",
    "Chaos Knight": "chaos_knight",
    "Chen": "chen",
    "Clinkz": "clinkz",
    "Clockwerk": "rattletrap",
    "Crystal Maiden": "crystal_maiden",
    "Dark Seer": "dark_seer",
    "Dark Willow": "dark_willow",
    "Dawnbreaker": "dawnbreaker",
    "Dazzle": "dazzle",
    "Death Prophet": "death_prophet",
    "Disruptor": "disruptor",
    "Doom": "doom_bringer",
    "Dragon Knight": "dragon_knight",
    "Drow Ranger": "drow_ranger",
    "Earth Spirit": "earth_spirit",
    "Earthshaker": "earthshaker",
    "Elder Titan": "elder_titan",
    "Ember Spirit": "ember_spirit",
    "Enchantress": "enchantress",
    "Enigma": "enigma",
    "Faceless Void": "faceless_void",
    "Grimstroke": "grimstroke",
    "Gyrocopter": "gyrocopter",
    "Hoodwink": "hoodwink",
    "Huskar": "huskar",
    "Invoker": "invoker",
    "Io": "wisp",
    "Jakiro": "jakiro",
    "Juggernaut": "juggernaut",
    "Keeper of the Light": "keeper_of_the_light",
    "Kez": "kez",
    "Kunkka": "kunkka",
    "Largo": "largo",
    "Legion Commander": "legion_commander",
    "Leshrac": "leshrac",
    "Lich": "lich",
    "Lifestealer": "life_stealer",
    "Lina": "lina",
    "Lion": "lion",
    "Lone Druid": "lone_druid",
    "Luna": "luna",
    "Lycan": "lycan",
    "Magnus": "magnataur",
    "Marci": "marci",
    "Mars": "mars",
    "Medusa": "medusa",
    "Meepo": "meepo",
    "Mirana": "mirana",
    "Monkey King": "monkey_king",
    "Morphling": "morphling",
    "Muerta": "muerta",
    "Naga Siren": "naga_siren",
    "Nature’s Prophet": "furion",
    "Necrophos": "necrolyte",
    "Night Stalker": "night_stalker",
    "Nyx Assassin": "nyx_assassin",
    "Ogre Magi": "ogre_magi",
    "Omniknight": "omniknight",
    "Oracle": "oracle",
    "Outworld Destroyer": "obsidian_destroyer",
    "Pangolier": "pangolier",
    "Phantom Assassin": "phantom_assassin",
    "Phantom Lancer": "phantom_lancer",
    "Phoenix": "phoenix",
    "Primal Beast": "primal_beast",
    "Puck": "puck",
    "Pudge": "pudge",
    "Pugna": "pugna",
    "Queen of Pain": "queenofpain",
    "Razor": "razor",
    "Riki": "riki",
    "Ringmaster": "ringmaster",
    "Rubick": "rubick",
    "Sand King": "sand_king",
    "Shadow Demon": "shadow_demon",
    "Shadow Fiend": "nevermore",
    "Shadow Shaman": "shadow_shaman",
    "Silencer": "silencer",
    "Skywrath Mage": "skywrath_mage",
    "Slardar": "slardar",
    "Slark": "slark",
    "Snapfire": "snapfire",
    "Sniper": "sniper",
    "Spectre": "spectre",
    "Spirit Breaker": "spirit_breaker",
    "Storm Spirit": "storm_spirit",
    "Sven": "sven",
    "Techies": "techies",
    "Templar Assassin": "templar_assassin",
    "Terrorblade": "terrorblade",
    "Tidehunter": "tidehunter",
    "Timbersaw": "shredder",
    "Tinker": "tinker",
    "Tiny": "tiny",
    "Treant Protector": "treant",
    "Troll Warlord": "troll_warlord",
    "Tusk": "tusk",
    "Underlord": "abyssal_underlord",
    "Undying": "undying",
    "Ursa": "ursa",
    "Vengeful Spirit": "vengefulspirit",
    "Venomancer": "venomancer",
    "Viper": "viper",
    "Visage": "visage",
    "Void Spirit": "void_spirit",
    "Warlock": "warlock",
    "Weaver": "weaver",
    "Windranger": "windrunner",
    "Winter Wyvern": "winter_wyvern",
    "Witch Doctor": "witch_doctor",
    "Wraith King": "skeleton_king",
    "Zeus": "zuus",
}

def load_positions(css_path: Path) -> Dict[str, Tuple[int, int]]:
    css = css_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"\.d2mh\.([a-z0-9_]+)[^{]*\{\s*"
        r"background-position:\s*-(\d+)px\s*-(\d+)px;",
        flags=re.MULTILINE,
    )
    positions: Dict[str, Tuple[int, int]] = {}
    for slug, x, y in pattern.findall(css):
        positions[slug] = (int(x), int(y))
    return positions

positions = load_positions(CSS_PATH)
sprite = Image.open(SPRITE_PATH).convert("RGBA")

missing = [
    hero
    for heroes in tiers.values()
    for hero in heroes
    if slug_map[hero] not in positions
]
if missing:
    raise RuntimeError(f"Missing sprite entries: {missing}")

# Layout
canvas_width = 2400
outer_margin = 38
header_height = 158
footer_height = 54
tier_gap = 10
label_width = 310
content_padding = 18

columns = 14
tile_width = 142
tile_height = 126
icon_size = 88

row_counts = {
    tier: math.ceil(len(heroes) / columns)
    for tier, heroes in tiers.items()
}
tier_heights = {
    tier: (rows * tile_height) + (content_padding * 2)
    for tier, rows in row_counts.items()
}
canvas_height = (
    outer_margin
    + header_height
    + sum(tier_heights.values())
    + tier_gap * (len(tiers) - 1)
    + footer_height
    + outer_margin
)

image = Image.new("RGB", (canvas_width, canvas_height), (14, 17, 22))
draw = ImageDraw.Draw(image)

def load_font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    """Load a readable font on Linux, macOS, or Windows."""
    bold_candidates = [
        "InterDisplay-Bold.otf",
        "Inter-Bold.ttf",
        "DejaVuSans-Bold.ttf",
        "/usr/share/fonts/opentype/inter/InterDisplay-Bold.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/Library/Fonts/Arial Bold.ttf",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/seguisb.ttf",
    ]
    regular_candidates = [
        "InterDisplay-Regular.otf",
        "Inter-Regular.ttf",
        "DejaVuSans.ttf",
        "/usr/share/fonts/opentype/inter/InterDisplay-Regular.otf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ]

    for candidate in bold_candidates if bold else regular_candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue

    return ImageFont.load_default()


title_font = load_font(64, bold=True)
subtitle_font = load_font(24)
tier_font = load_font(30, bold=True)
count_font = load_font(20)
hero_font = load_font(17)
footer_font = load_font(17)

# Header
header_top = outer_margin
draw.rounded_rectangle(
    (outer_margin, header_top, canvas_width - outer_margin, header_top + header_height - 12),
    radius=24,
    fill=(24, 28, 35),
    outline=(65, 72, 84),
    width=2,
)
draw.text(
    (outer_margin + 36, header_top + 24),
    "DOTA 2 TURBO HERO TIER LIST",
    font=title_font,
    fill=(244, 246, 249),
)
draw.text(
    (outer_margin + 40, header_top + 102),
    "127 heroes ranked by how their kits translate to Turbo mode",
    font=subtitle_font,
    fill=(166, 175, 190),
)

tier_styles = {
    "SUPERSONIC RACING": ((197, 58, 72), (86, 25, 34)),
    "TURBOCHARGED": ((232, 129, 55), (91, 48, 23)),
    "SAME SAME BUT DIFFERENT": ((224, 188, 73), (88, 72, 27)),
    "NOT SO GOOD": ((93, 137, 176), (34, 52, 70)),
    "GO BACK TO RANKED": ((88, 93, 105), (35, 38, 45)),
}

def fit_centered_text(
    draw_context: ImageDraw.ImageDraw,
    box: Tuple[int, int, int, int],
    lines: List[str],
    font: ImageFont.FreeTypeFont,
    fill: Tuple[int, int, int],
    spacing: int = 6,
) -> None:
    x1, y1, x2, y2 = box
    line_boxes = [draw_context.textbbox((0, 0), line, font=font) for line in lines]
    widths = [b[2] - b[0] for b in line_boxes]
    heights = [b[3] - b[1] for b in line_boxes]
    total_height = sum(heights) + spacing * (len(lines) - 1)
    current_y = y1 + (y2 - y1 - total_height) // 2
    for line, width, height in zip(lines, widths, heights):
        draw_context.text(
            (x1 + (x2 - x1 - width) // 2, current_y),
            line,
            font=font,
            fill=fill,
        )
        current_y += height + spacing

def split_hero_name(name: str) -> List[str]:
    if len(name) <= 14:
        return [name]
    words = name.split()
    if len(words) == 1:
        return [name]
    best: Tuple[str, str] | None = None
    best_diff = 999
    for i in range(1, len(words)):
        left = " ".join(words[:i])
        right = " ".join(words[i:])
        diff = abs(len(left) - len(right))
        if diff < best_diff:
            best = (left, right)
            best_diff = diff
    return list(best) if best else [name]

y = outer_margin + header_height

for tier_name, heroes in tiers.items():
    tier_height = tier_heights[tier_name]
    bright, dark = tier_styles[tier_name]

    # Full row panel
    draw.rounded_rectangle(
        (outer_margin, y, canvas_width - outer_margin, y + tier_height),
        radius=20,
        fill=(25, 29, 36),
        outline=(61, 68, 80),
        width=2,
    )

    # Tier label panel
    draw.rounded_rectangle(
        (outer_margin, y, outer_margin + label_width, y + tier_height),
        radius=20,
        fill=dark,
    )
    # Square the right corners so the label joins cleanly to the content.
    draw.rectangle(
        (outer_margin + label_width - 20, y, outer_margin + label_width, y + tier_height),
        fill=dark,
    )
    draw.rectangle(
        (outer_margin + label_width, y, outer_margin + label_width + 6, y + tier_height),
        fill=bright,
    )

    label_lines = {
        "SUPERSONIC RACING": ["SUPERSONIC", "RACING"],
        "TURBOCHARGED": ["TURBOCHARGED"],
        "SAME SAME BUT DIFFERENT": ["SAME SAME", "BUT DIFFERENT"],
        "NOT SO GOOD": ["NOT SO GOOD"],
        "GO BACK TO RANKED": ["GO BACK", "TO RANKED"],
    }[tier_name]

    label_box = (
        outer_margin + 18,
        y + 18,
        outer_margin + label_width - 18,
        y + tier_height - 48,
    )
    fit_centered_text(draw, label_box, label_lines, tier_font, (248, 248, 250))
    count_text = f"{len(heroes)} HEROES"
    count_bbox = draw.textbbox((0, 0), count_text, font=count_font)
    count_width = count_bbox[2] - count_bbox[0]
    draw.text(
        (
            outer_margin + (label_width - count_width) // 2,
            y + tier_height - 38,
        ),
        count_text,
        font=count_font,
        fill=(215, 219, 226),
    )

    start_x = outer_margin + label_width + 26
    start_y = y + content_padding

    for index, hero in enumerate(heroes):
        col = index % columns
        row = index // columns
        tile_x = start_x + col * tile_width
        tile_y = start_y + row * tile_height

        # Card
        card_x2 = tile_x + tile_width - 10
        card_y2 = tile_y + tile_height - 8
        draw.rounded_rectangle(
            (tile_x, tile_y, card_x2, card_y2),
            radius=13,
            fill=(18, 21, 27),
            outline=(55, 61, 72),
            width=2,
        )

        slug = slug_map[hero]
        sx, sy = positions[slug]
        icon = sprite.crop((sx, sy, sx + 32, sy + 32))
        icon = icon.resize((icon_size, icon_size), Image.Resampling.NEAREST)

        icon_x = tile_x + ((tile_width - 10 - icon_size) // 2)
        icon_y = tile_y + 8
        image.paste(icon, (icon_x, icon_y), icon)

        lines = split_hero_name(hero)
        text_area_top = tile_y + 96
        if len(lines) == 1:
            bbox = draw.textbbox((0, 0), lines[0], font=hero_font)
            text_width = bbox[2] - bbox[0]
            draw.text(
                (tile_x + (tile_width - 10 - text_width) // 2, text_area_top + 3),
                lines[0],
                font=hero_font,
                fill=(231, 234, 239),
            )
        else:
            for line_index, line in enumerate(lines[:2]):
                bbox = draw.textbbox((0, 0), line, font=hero_font)
                text_width = bbox[2] - bbox[0]
                draw.text(
                    (
                        tile_x + (tile_width - 10 - text_width) // 2,
                        text_area_top - 4 + line_index * 18,
                    ),
                    line,
                    font=hero_font,
                    fill=(231, 234, 239),
                )

    y += tier_height + tier_gap

footer_y = canvas_height - outer_margin - footer_height + 8
draw.text(
    (outer_margin + 4, footer_y),
    "Hero icons: Valve Dota 2 minimap artwork via dota2-css-hero-sprites 2.6.2",
    font=footer_font,
    fill=(133, 142, 156),
)
right_footer = "Generated from the supplied video transcript"
right_bbox = draw.textbbox((0, 0), right_footer, font=footer_font)
draw.text(
    (canvas_width - outer_margin - (right_bbox[2] - right_bbox[0]) - 4, footer_y),
    right_footer,
    font=footer_font,
    fill=(133, 142, 156),
)

image.save(OUTPUT_PATH, "PNG", optimize=True)

print(f"Created: {OUTPUT_PATH}")
print(f"Dimensions: {canvas_width} x {canvas_height}")
print(f"Heroes included: {sum(len(heroes) for heroes in tiers.values())}")
