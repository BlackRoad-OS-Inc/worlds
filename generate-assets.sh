#!/bin/bash
# Generate BlackRoad branded SVG social cards + banners for every repo
# Uses BlackRoad gradient colors per category

set -e

WORLDS="/Users/alexa/worlds"
DATE=$(date +%Y-%m-%d)

# BlackRoad gradient colors by category
declare -A CAT_COLOR1 CAT_COLOR2 CAT_ICON
CAT_COLOR1[agents]="#FF006B"   # Hot Pink
CAT_COLOR2[agents]="#7700FF"   # Vivid Purple
CAT_ICON[agents]="Agent"

CAT_COLOR1[worlds]="#FF6B00"   # Warm Orange
CAT_COLOR2[worlds]="#FF0066"   # Hot Pink
CAT_ICON[worlds]="World"

CAT_COLOR1[tools]="#0066FF"    # Cyber Blue
CAT_COLOR2[tools]="#7700FF"    # Vivid Purple
CAT_ICON[tools]="Tool"

CAT_COLOR1[reference]="#D600AA" # Deep Magenta
CAT_COLOR2[reference]="#0066FF" # Cyber Blue
CAT_ICON[reference]="Ref"

generate_social_card() {
  local dir="$1"
  local category="$2"
  local name=$(basename "$dir")
  local c1="${CAT_COLOR1[$category]}"
  local c2="${CAT_COLOR2[$category]}"
  local label="${CAT_ICON[$category]}"

  # Get short description from README
  local desc=""
  for readme in README.md README.rst README readme.md; do
    if [ -f "$dir/$readme" ]; then
      desc=$(head -10 "$dir/$readme" | grep -v '^#' | grep -v '^!' | grep -v '^\[' | grep -v '^$' | grep -v '^<' | head -1 | sed 's/^[[:space:]]*//' | cut -c1-80)
      break
    fi
  done
  [ -z "$desc" ] && desc="BlackRoad World Library"

  # Escape XML special chars
  desc=$(echo "$desc" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g; s/"/\&quot;/g')
  local safe_name=$(echo "$name" | sed 's/&/\&amp;/g; s/</\&lt;/g; s/>/\&gt;/g')

  mkdir -p "$dir/.blackroad"

  # Social card (1280x640 — GitHub og:image size)
  cat > "$dir/.blackroad/social-card.svg" << SVGEOF
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="640" viewBox="0 0 1280 640">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a0a"/>
      <stop offset="100%" stop-color="#1a1a1a"/>
    </linearGradient>
    <linearGradient id="accent" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${c1}"/>
      <stop offset="100%" stop-color="${c2}"/>
    </linearGradient>
    <linearGradient id="road" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="${c1}" stop-opacity="0.15"/>
      <stop offset="50%" stop-color="${c2}" stop-opacity="0.08"/>
      <stop offset="100%" stop-color="#0a0a0a" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="640" fill="url(#bg)"/>
  <rect width="1280" height="640" fill="url(#road)"/>
  <!-- Top gradient bar -->
  <rect x="0" y="0" width="1280" height="4" fill="url(#accent)"/>
  <!-- Category badge -->
  <rect x="80" y="80" width="${#label * 16 + 40}" height="36" rx="18" fill="url(#accent)" opacity="0.9"/>
  <text x="100" y="104" font-family="monospace" font-size="16" font-weight="bold" fill="#fff">${label}</text>
  <!-- Logo circle -->
  <circle cx="1160" cy="120" r="48" fill="none" stroke="url(#accent)" stroke-width="2" opacity="0.6"/>
  <text x="1160" y="130" font-family="monospace" font-size="28" font-weight="bold" fill="url(#accent)" text-anchor="middle">BR</text>
  <!-- Project name -->
  <text x="80" y="260" font-family="monospace" font-size="64" font-weight="bold" fill="#ffffff">${safe_name}</text>
  <!-- Description -->
  <text x="80" y="320" font-family="sans-serif" font-size="24" fill="#a0a0a0">${desc}</text>
  <!-- Bottom bar -->
  <rect x="0" y="560" width="1280" height="80" fill="#0a0a0a" opacity="0.8"/>
  <text x="80" y="608" font-family="monospace" font-size="20" fill="#666">BlackRoad World Library</text>
  <text x="640" y="608" font-family="monospace" font-size="20" fill="#666" text-anchor="middle">${category}</text>
  <text x="1200" y="608" font-family="monospace" font-size="18" fill="url(#accent)" text-anchor="end">blackroad.io</text>
  <!-- Bottom gradient bar -->
  <rect x="0" y="636" width="1280" height="4" fill="url(#accent)"/>
  <!-- Road dashes (decorative) -->
  <rect x="80" y="380" width="60" height="3" rx="1.5" fill="${c1}" opacity="0.4"/>
  <rect x="160" y="380" width="60" height="3" rx="1.5" fill="${c1}" opacity="0.3"/>
  <rect x="240" y="380" width="60" height="3" rx="1.5" fill="${c2}" opacity="0.2"/>
  <rect x="320" y="380" width="60" height="3" rx="1.5" fill="${c2}" opacity="0.1"/>
</svg>
SVGEOF

  # Banner (1280x320)
  cat > "$dir/.blackroad/banner.svg" << SVGEOF
<svg xmlns="http://www.w3.org/2000/svg" width="1280" height="320" viewBox="0 0 1280 320">
  <defs>
    <linearGradient id="bg2" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#0a0a0a"/>
      <stop offset="100%" stop-color="#1a1a1a"/>
    </linearGradient>
    <linearGradient id="accent2" x1="0%" y1="0%" x2="100%" y2="0%">
      <stop offset="0%" stop-color="${c1}"/>
      <stop offset="100%" stop-color="${c2}"/>
    </linearGradient>
  </defs>
  <rect width="1280" height="320" fill="url(#bg2)"/>
  <rect x="0" y="0" width="1280" height="3" fill="url(#accent2)"/>
  <text x="640" y="140" font-family="monospace" font-size="52" font-weight="bold" fill="#ffffff" text-anchor="middle">${safe_name}</text>
  <text x="640" y="190" font-family="sans-serif" font-size="22" fill="#808080" text-anchor="middle">${desc}</text>
  <text x="640" y="270" font-family="monospace" font-size="16" fill="url(#accent2)" text-anchor="middle">BlackRoad World Library — ${category} — Pave Tomorrow.</text>
  <rect x="0" y="317" width="1280" height="3" fill="url(#accent2)"/>
  <!-- Road dashes -->
  <rect x="440" y="220" width="40" height="2" rx="1" fill="${c1}" opacity="0.3"/>
  <rect x="500" y="220" width="40" height="2" rx="1" fill="${c1}" opacity="0.25"/>
  <rect x="560" y="220" width="40" height="2" rx="1" fill="${c2}" opacity="0.2"/>
  <rect x="620" y="220" width="40" height="2" rx="1" fill="${c2}" opacity="0.15"/>
  <rect x="680" y="220" width="40" height="2" rx="1" fill="${c2}" opacity="0.1"/>
  <rect x="740" y="220" width="40" height="2" rx="1" fill="${c2}" opacity="0.05"/>
</svg>
SVGEOF

  echo "  [OK] $name — social-card.svg + banner.svg"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  BlackRoad Asset Generator — World Library"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for category in agents worlds tools reference; do
  echo "[$category] (${CAT_COLOR1[$category]} → ${CAT_COLOR2[$category]})"
  if [ -d "$WORLDS/$category" ]; then
    for repo_dir in "$WORLDS/$category"/*/; do
      [ -d "$repo_dir" ] && generate_social_card "$repo_dir" "$category"
    done
  fi
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done. Assets generated for all repos."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
