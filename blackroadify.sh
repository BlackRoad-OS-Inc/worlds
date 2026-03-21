#!/bin/bash
# BlackRoadify — stamp all world library repos with BlackRoad branding
# Preserves original LICENSE, adds BLACKROAD.md with attribution + branding

set -e

WORLDS="/Users/alexa/worlds"
LOGO_URL="https://images.blackroad.io/brand/br-circle-256.png"
DATE=$(date +%Y-%m-%d)

blackroadify() {
  local dir="$1"
  local category="$2"
  local repo_name=$(basename "$dir")

  # Get original license type
  local license="Unknown"
  if [ -f "$dir/LICENSE" ]; then
    if grep -qi "MIT" "$dir/LICENSE" 2>/dev/null; then license="MIT"
    elif grep -qi "Apache" "$dir/LICENSE" 2>/dev/null; then license="Apache-2.0"
    fi
  elif [ -f "$dir/LICENSE.md" ]; then
    if grep -qi "MIT" "$dir/LICENSE.md" 2>/dev/null; then license="MIT"
    elif grep -qi "Apache" "$dir/LICENSE.md" 2>/dev/null; then license="Apache-2.0"
    fi
  elif [ -f "$dir/LICENSE.txt" ]; then
    if grep -qi "MIT" "$dir/LICENSE.txt" 2>/dev/null; then license="MIT"
    elif grep -qi "Apache" "$dir/LICENSE.txt" 2>/dev/null; then license="Apache-2.0"
    fi
  fi

  # Get upstream from git remote
  local upstream=$(cd "$dir" && git remote get-url upstream 2>/dev/null | sed 's|https://github.com/||' | sed 's|\.git$||')
  [ -z "$upstream" ] && upstream="unknown"

  # Get description from first line of README
  local description=""
  for readme in README.md README.rst README readme.md; do
    if [ -f "$dir/$readme" ]; then
      description=$(head -5 "$dir/$readme" | grep -v '^#' | grep -v '^$' | head -1 | sed 's/^[[:space:]]*//')
      break
    fi
  done
  [ -z "$description" ] && description="A BlackRoad World Library component"

  # Write BLACKROAD.md
  cat > "$dir/BLACKROAD.md" << BREOF
<p align="center">
  <img src="${LOGO_URL}" width="128" alt="BlackRoad OS" />
</p>

<h3 align="center">BlackRoad World Library</h3>
<p align="center"><strong>${repo_name}</strong> — ${category}</p>
<p align="center"><em>Pave Tomorrow.</em></p>

---

## Attribution

This project is a fork of [${upstream}](https://github.com/${upstream}), licensed under **${license}**.

All original code remains under its original license. New code, modifications, and BlackRoad-specific additions are Copyright (c) 2024-2026 BlackRoad OS, Inc. All rights reserved.

## BlackRoad Integration

| Field | Value |
|-------|-------|
| **Library** | World Library |
| **Category** | ${category} |
| **Upstream** | [${upstream}](https://github.com/${upstream}) |
| **License** | ${license} (original) |
| **Added** | ${DATE} |
| **Status** | Integrated |

## About BlackRoad OS

BlackRoad OS is sovereign AI infrastructure — local-first, privacy-respecting, community-owned.

- Website: [blackroad.io](https://blackroad.io)
- GitHub: [github.com/blackboxprogramming](https://github.com/blackboxprogramming)

---

*BlackRoad OS, Inc. — Pave Tomorrow.*
BREOF

  echo "  [OK] $repo_name ($license, upstream: $upstream)"
}

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  BlackRoadify — World Library Builder"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

for category in agents worlds tools reference; do
  echo "[$category]"
  if [ -d "$WORLDS/$category" ]; then
    for repo_dir in "$WORLDS/$category"/*/; do
      [ -d "$repo_dir" ] && blackroadify "$repo_dir" "$category"
    done
  fi
  echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Done. All repos BlackRoadified."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
