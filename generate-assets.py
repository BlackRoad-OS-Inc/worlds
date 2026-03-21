#!/usr/bin/env python3
"""Generate BlackRoad branded SVG assets for every repo in the World Library."""

import os
import html

WORLDS = "/Users/alexa/worlds"

# Official BlackRoad Design System colors
BRAND = {
    "orange": "#FF6B2B",
    "pink": "#FF2255",
    "magenta": "#CC00AA",
    "purple": "#8844FF",
    "blue": "#4488FF",
    "cyan": "#00D4FF",
    "black": "#000",
    "surface": "#0a0a0a",
    "elevated": "#111",
    "border": "#222",
    "muted": "#444",
    "white": "#fff",
}

# Category color pairs (from the brand gradient spectrum)
CATEGORIES = {
    "agents": {"c1": "#CC00AA", "c2": "#8844FF", "label": "AGENT"},
    "worlds": {"c1": "#FF6B2B", "c2": "#FF2255", "label": "WORLD"},
    "tools": {"c1": "#4488FF", "c2": "#00D4FF", "label": "TOOL"},
    "reference": {"c1": "#FF2255", "c2": "#CC00AA", "label": "REFERENCE"},
}

# Per-repo accent override (unique identity within category)
REPO_COLORS = {
    # agents
    "openclaw": ("#CC00AA", "#8844FF"),
    "pi-mono": ("#8844FF", "#4488FF"),
    "hindsight": ("#FF2255", "#CC00AA"),
    "agency-agents": ("#FF6B2B", "#FF2255"),
    "superpowers": ("#CC00AA", "#FF2255"),
    "rowboat": ("#4488FF", "#00D4FF"),
    "OpenViking": ("#FF6B2B", "#CC00AA"),
    "OpenSandbox": ("#8844FF", "#00D4FF"),
    "skills": ("#00D4FF", "#4488FF"),
    "agent-monitor": ("#FF2255", "#8844FF"),
    "sgpt": ("#4488FF", "#8844FF"),
    # worlds
    "pixel-agents": ("#FF6B2B", "#FF2255"),
    "claude-office": ("#FF2255", "#CC00AA"),
    "GameBoyWorlds": ("#CC00AA", "#8844FF"),
    "isometric-nyc": ("#4488FF", "#00D4FF"),
    "tiny-world": ("#00D4FF", "#4488FF"),
    "SanAndreasUnity": ("#FF6B2B", "#CC00AA"),
    "BitNet": ("#8844FF", "#00D4FF"),
    # tools
    "A2UI": ("#4488FF", "#00D4FF"),
    "PDF4QT": ("#00D4FF", "#8844FF"),
    "alfred-calendly": ("#4488FF", "#FF2255"),
    "openapi-generator": ("#8844FF", "#4488FF"),
    "algorithms": ("#00D4FF", "#CC00AA"),
    # reference
    "learn-claude-code": ("#FF2255", "#CC00AA"),
    "book.git-scm.com": ("#CC00AA", "#8844FF"),
    "the-book-of-secret-knowledge": ("#FF6B2B", "#FF2255"),
}


def get_description(repo_dir):
    for readme in ["README.md", "README.rst", "README", "readme.md"]:
        path = os.path.join(repo_dir, readme)
        if os.path.isfile(path):
            with open(path, "r", errors="ignore") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and not line.startswith("!") and not line.startswith("[") and not line.startswith("<") and not line.startswith("---"):
                        return line[:90]
    return "BlackRoad World Library"


def social_card(name, desc, category, c1, c2, label):
    desc_escaped = html.escape(desc)
    name_escaped = html.escape(name)
    badge_w = len(label) * 11 + 32
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#000"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="glow" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="{c1}" stop-opacity="0.12"/>
      <stop offset="50%" stop-color="{c2}" stop-opacity="0.06"/>
      <stop offset="100%" stop-color="#000" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="spectrum" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6B2B"/>
      <stop offset="20%" stop-color="#FF2255"/>
      <stop offset="40%" stop-color="#CC00AA"/>
      <stop offset="60%" stop-color="#8844FF"/>
      <stop offset="80%" stop-color="#4488FF"/>
      <stop offset="100%" stop-color="#00D4FF"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="640" fill="url(#bg)"/>
  <rect width="1280" height="640" fill="url(#glow)"/>
  <!-- Top spectrum bar -->
  <rect x="0" y="0" width="1280" height="3" fill="url(#spectrum)"/>
  <!-- Category badge -->
  <rect x="80" y="80" width="{badge_w}" height="32" rx="4" fill="url(#accent)" opacity="0.9"/>
  <text x="{80 + badge_w // 2}" y="101" font-family="JetBrains Mono, monospace" font-size="13" font-weight="700" fill="#fff" text-anchor="middle" letter-spacing="2">{label}</text>
  <!-- BR mark -->
  <circle cx="1160" cy="110" r="40" fill="none" stroke="url(#accent)" stroke-width="1.5" opacity="0.5"/>
  <text x="1160" y="120" font-family="Space Grotesk, sans-serif" font-size="26" font-weight="700" fill="{c1}" text-anchor="middle" opacity="0.8">BR</text>
  <!-- Project name -->
  <text x="80" y="260" font-family="Space Grotesk, sans-serif" font-size="56" font-weight="700" fill="#fff">{name_escaped}</text>
  <!-- Accent underline -->
  <rect x="80" y="278" width="200" height="2" rx="1" fill="url(#accent)" opacity="0.6"/>
  <!-- Description -->
  <text x="80" y="340" font-family="JetBrains Mono, monospace" font-size="18" fill="#fff" opacity="0.5">{desc_escaped}</text>
  <!-- Road dashes -->
  <g opacity="0.4">
    <rect x="80" y="400" width="48" height="2" rx="1" fill="{c1}"/>
    <rect x="148" y="400" width="48" height="2" rx="1" fill="{c1}" opacity="0.7"/>
    <rect x="216" y="400" width="48" height="2" rx="1" fill="{c2}" opacity="0.5"/>
    <rect x="284" y="400" width="48" height="2" rx="1" fill="{c2}" opacity="0.3"/>
    <rect x="352" y="400" width="48" height="2" rx="1" fill="{c2}" opacity="0.1"/>
  </g>
  <!-- Footer -->
  <rect x="0" y="556" width="1280" height="84" fill="#000" opacity="0.6"/>
  <text x="80" y="604" font-family="JetBrains Mono, monospace" font-size="14" fill="#fff" opacity="0.3" letter-spacing="1">BLACKROAD WORLD LIBRARY</text>
  <text x="560" y="604" font-family="JetBrains Mono, monospace" font-size="14" fill="#fff" opacity="0.2">{category}</text>
  <text x="1200" y="604" font-family="Space Grotesk, sans-serif" font-size="16" font-weight="600" fill="{c1}" text-anchor="end" opacity="0.7">blackroad.io</text>
  <!-- Bottom spectrum bar -->
  <rect x="0" y="637" width="1280" height="3" fill="url(#spectrum)"/>
</svg>'''


def banner(name, desc, category, c1, c2, label):
    desc_escaped = html.escape(desc)
    name_escaped = html.escape(name)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#000"/>
      <stop offset="100%" stop-color="#0a0a0a"/>
    </linearGradient>
    <linearGradient id="a2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="{c1}"/>
      <stop offset="100%" stop-color="{c2}"/>
    </linearGradient>
    <linearGradient id="sp2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="#FF6B2B"/>
      <stop offset="20%" stop-color="#FF2255"/>
      <stop offset="40%" stop-color="#CC00AA"/>
      <stop offset="60%" stop-color="#8844FF"/>
      <stop offset="80%" stop-color="#4488FF"/>
      <stop offset="100%" stop-color="#00D4FF"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="320" fill="url(#bg2)"/>
  <rect x="0" y="0" width="1280" height="3" fill="url(#sp2)"/>
  <text x="640" y="120" font-family="Space Grotesk, sans-serif" font-size="48" font-weight="700" fill="#fff" text-anchor="middle">{name_escaped}</text>
  <rect x="540" y="136" width="200" height="2" rx="1" fill="url(#a2)" opacity="0.5"/>
  <text x="640" y="180" font-family="JetBrains Mono, monospace" font-size="16" fill="#fff" opacity="0.4" text-anchor="middle">{desc_escaped}</text>
  <!-- Road dashes -->
  <g opacity="0.3">
    <rect x="480" y="210" width="32" height="2" rx="1" fill="{c1}"/>
    <rect x="528" y="210" width="32" height="2" rx="1" fill="{c1}" opacity="0.7"/>
    <rect x="576" y="210" width="32" height="2" rx="1" fill="{c2}" opacity="0.5"/>
    <rect x="624" y="210" width="32" height="2" rx="1" fill="{c2}" opacity="0.35"/>
    <rect x="672" y="210" width="32" height="2" rx="1" fill="{c2}" opacity="0.2"/>
    <rect x="720" y="210" width="32" height="2" rx="1" fill="{c2}" opacity="0.1"/>
  </g>
  <text x="640" y="280" font-family="JetBrains Mono, monospace" font-size="12" fill="#fff" opacity="0.25" text-anchor="middle" letter-spacing="2">BLACKROAD WORLD LIBRARY · {label} · PAVE TOMORROW</text>
  <rect x="0" y="317" width="1280" height="3" fill="url(#sp2)"/>
</svg>'''


def color_theme_json(name, c1, c2, category):
    """Generate a BlackRoad color theme config for pixel projects."""
    return f'''{{"name": "{name}",
  "category": "{category}",
  "brand": {{
    "primary": "{c1}",
    "secondary": "{c2}",
    "accent": "#FF6B2B",
    "surface": "#0a0a0a",
    "elevated": "#111111",
    "border": "#222222",
    "text": "#ffffff",
    "textMuted": "rgba(255,255,255,0.5)",
    "gradient": "linear-gradient(90deg, #FF6B2B, #FF2255, #CC00AA, #8844FF, #4488FF, #00D4FF)"
  }},
  "office": {{
    "floor": {{"h": 0, "s": 0, "b": -60, "c": 10, "colorize": true}},
    "floorAlt": {{"h": 270, "s": 8, "b": -65, "c": 5, "colorize": true}},
    "wall": {{"h": 0, "s": 0, "b": -75, "c": 0, "colorize": true}},
    "desk": "#111111",
    "deskTop": "#1a1a1a",
    "chair": "#0a0a0a",
    "computer": "#222222",
    "plant": "#00D4FF",
    "accentGlow": "{c1}"
  }},
  "agents": {{
    "palette0": "{c1}",
    "palette1": "{c2}",
    "palette2": "#FF6B2B",
    "palette3": "#FF2255",
    "palette4": "#4488FF",
    "palette5": "#00D4FF"
  }},
  "fonts": {{
    "display": "Space Grotesk",
    "mono": "JetBrains Mono",
    "weights": [400, 600, 700]
  }}
}}'''


def main():
    print("━" * 52)
    print("  BlackRoad Asset Generator — World Library")
    print("━" * 52)
    print()

    total = 0
    for category in ["agents", "worlds", "tools", "reference"]:
        cat_dir = os.path.join(WORLDS, category)
        if not os.path.isdir(cat_dir):
            continue
        cat_cfg = CATEGORIES[category]
        print(f"[{category}] {cat_cfg['c1']} → {cat_cfg['c2']}")

        for name in sorted(os.listdir(cat_dir)):
            repo_dir = os.path.join(cat_dir, name)
            if not os.path.isdir(repo_dir) or name.startswith("."):
                continue

            c1, c2 = REPO_COLORS.get(name, (cat_cfg["c1"], cat_cfg["c2"]))
            label = cat_cfg["label"]
            desc = get_description(repo_dir)

            br_dir = os.path.join(repo_dir, ".blackroad")
            os.makedirs(br_dir, exist_ok=True)

            # Social card
            with open(os.path.join(br_dir, "social-card.svg"), "w") as f:
                f.write(social_card(name, desc, category, c1, c2, label))

            # Banner
            with open(os.path.join(br_dir, "banner.svg"), "w") as f:
                f.write(banner(name, desc, category, c1, c2, label))

            # Color theme config
            with open(os.path.join(br_dir, "theme.json"), "w") as f:
                f.write(color_theme_json(name, c1, c2, category))

            total += 1
            print(f"  [{c1}→{c2}] {name}")

        print()

    print("━" * 52)
    print(f"  Done. {total} repos × 3 assets = {total * 3} files generated.")
    print("  Assets: social-card.svg, banner.svg, theme.json")
    print("━" * 52)


if __name__ == "__main__":
    main()
