# Runway Crosswind Trainer

A frontend-only, Cessna-inspired educational wind-component trainer deployed on GitHub Pages.

**Live website:** https://rianamalhotra.github.io/runway-crosswind-calculator/

## Experience

1. Start in a simplified cockpit taxi scene with an animated windsock.
2. Select **Analyze crosswind** to open the instrument display.
3. Adjust runway heading, wind-from direction, sustained wind and gust speed.
4. Review crosswind/headwind/tailwind components, vector decomposition and a configurable reference threshold.
5. Select **Cockpit** to return to the taxi view.

The vector diagram uses **runway-up orientation** (not north-up) so the component breakdown remains readable. Crosswind positive means wind from the right; negative means from the left. Negative headwind indicates tailwind.

## Calculations

With relative wind angle θ = wind-from direction − runway heading:

- Headwind = wind speed × cos(θ)
- Crosswind = wind speed × sin(θ)

The same calculations are applied to gust speed. The interface requires gust speed to be at least sustained wind speed.

## Run locally

Open `index.html` in a modern browser. No installation or backend is required.

## Automated tests

Requires Node.js 18+:

```bash
node --test tests/*.test.js
```

Tests cover direct headwind, tailwind, left/right crosswind, 30-degree decomposition, gusts, wraparound headings, zero wind and invalid inputs. GitHub Actions runs the tests on pushes to `main` and pull requests.

## Deploy

GitHub Pages → **Deploy from a branch** → `main` → `/(root)`. Commits to main automatically redeploy the site.

## Safety and scope

**For education only; not for operational flight planning or go/no-go decisions.** The default 15 kt threshold is a user-adjustable comparison value, not a certified Cessna 172 operating limit. Actual aircraft guidance varies by model and conditions. Use runway heading and wind direction in the same magnetic or true reference. Runway numbers are rounded and do not necessarily equal the precise published runway heading.
