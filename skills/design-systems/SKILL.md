---
name: design-systems
description: Use when building, styling, theming, or refactoring a web UI, page, component, or landing/marketing site in the visual style of a known brand or product (Stripe, Linear, Apple, Notion, Vercel, Tesla, Spotify, Airbnb, Figma, Shopify, Supabase, etc.) — also use when the user says "look like X", "design like X", "X-inspired", "in the style of X", or copies a screenshot/URL from one of the 70 catalogued brands. Provides the brand's full design spec (colors, typography, components, spacing, do's/don'ts) from a curated local library.
---

# Design Systems

## Overview

Local mirror of [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) — 70 `DESIGN.md` files extracted from real brand sites. Each one is a complete design system spec (colors, type scale, component states, spacing, do's/don'ts) ready for an agent to apply.

When the user invokes a brand for visual reference, **read the matching `DESIGN.md` and let it drive your styling decisions** instead of guessing.

## How to Use

1. **Identify the brand.** User says "like Stripe" / "Linear-style" / "make it feel like Apple". Look it up in the catalogue below.
2. **Read the DESIGN.md.** Path: `~/.claude/skills/design-systems/library/design-md/<slug>/DESIGN.md`. Use the Read tool — do NOT try to summarize from memory.
3. **Apply the spec.** Use the exact hex values, font stacks, spacing scale, and component states from the file. Quote the file when justifying a choice ("Stripe's DESIGN.md specifies `#533afd` for primary actions").
4. **Cite the source** in PR descriptions or commit messages: "Styling adapted from awesome-design-md / <brand>".

## Multi-brand or unlisted brands

- **Mixing two brands** (e.g. "Linear's layout with Notion's warmth") → read both DESIGN.md files, then explicitly declare which tokens come from which.
- **Brand not in the catalogue** → say so. Do NOT fabricate a DESIGN.md. Offer to (a) pick the closest brand from the list, or (b) do a brief design pass without a reference.

## Catalogue (70 brands)

Folder slugs are listed when they differ from the obvious brand name.

### AI & LLM Platforms
`claude` · `cohere` · `elevenlabs` · `minimax` · `mistral.ai` · `ollama` · `opencode.ai` · `replicate` · `runwayml` · `together.ai` · `voltagent` · `x.ai`

### Developer Tools & IDEs
`cursor` · `expo` · `lovable` · `raycast` · `superhuman` · `vercel` · `warp`

### Backend / Database / DevOps
`clickhouse` · `composio` · `hashicorp` · `mongodb` · `posthog` · `sanity` · `sentry` · `supabase`

### Productivity & SaaS
`cal` *(Cal.com)* · `intercom` · `linear.app` · `mintlify` · `notion` · `resend` · `zapier`

### Design & Creative Tools
`airtable` · `clay` · `figma` · `framer` · `miro` · `webflow`

### Fintech & Crypto
`binance` · `coinbase` · `kraken` · `mastercard` · `revolut` · `stripe` · `wise`

### E-commerce & Retail
`airbnb` · `meta` · `nike` · `shopify` · `starbucks`

### Media & Consumer Tech
`apple` · `ibm` · `nvidia` · `pinterest` · `playstation` · `spacex` · `spotify` · `theverge` · `uber` · `vodafone` · `wired`

### Automotive
`bmw` · `bmw-m` · `bugatti` · `ferrari` · `lamborghini` · `renault` · `tesla`

## Slug-resolution quick rules

| User says | Slug |
|---|---|
| Linear | `linear.app` |
| xAI / X | `x.ai` |
| Mistral | `mistral.ai` |
| Together AI | `together.ai` |
| OpenCode | `opencode.ai` |
| Cal.com | `cal` |
| BMW (regular) | `bmw` |
| BMW M (motorsport) | `bmw-m` |
| The Verge | `theverge` |

For everything else: lowercase brand name. If unsure, run `ls ~/.claude/skills/design-systems/library/design-md/`.

## What each DESIGN.md contains

Every file follows the [Stitch DESIGN.md format](https://stitch.withgoogle.com/docs/design-md/format/):

1. Visual theme & atmosphere
2. Color palette & roles (semantic name + hex + function)
3. Typography rules (full hierarchy)
4. Component stylings (buttons, cards, inputs, nav — with states)
5. Layout principles (spacing, grid, whitespace)
6. Depth & elevation (shadows)
7. Do's and Don'ts
8. Responsive behavior
9. Agent prompt guide (quick color reference)

## Updating the library

Library is a shallow git clone. To pull new brands or fixes:

```bash
cd ~/.claude/skills/design-systems/library && git pull
```

## What this skill is NOT

- Not for theological, sermon, or pastor-AI work — those have their own skills.
- Not a UI generator — it provides the spec; you write the code.
- Not a substitute for actual brand assets (logos, fonts under license). Use design tokens, not trademarked material.
