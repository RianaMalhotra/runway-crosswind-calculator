# Runway Crosswind Calculator

A responsive, frontend-only aviation tool that calculates headwind, tailwind, and left/right crosswind components from runway heading and wind direction/speed.

## Live website

https://rianamalhotra.github.io/runway-crosswind-calculator/ (available after GitHub Pages is enabled)

## Features

- Instant wind component calculations
- Interactive runway and wind visualization
- Input validation and mobile-friendly layout
- No dependencies, server, or API required

## Run locally

Open `index.html` in any modern browser.

## Formula

With wind speed `V` and relative angle `θ = wind direction - runway heading`:

- Headwind component: `V × cos(θ)` (negative means tailwind)
- Crosswind component: `V × sin(θ)` (positive means wind from right)

For runway heading 270°, wind from 300° at 20 kt: headwind ≈ 17.3 kt, crosswind ≈ 10.0 kt from right.

## Deployment

GitHub repository **Settings → Pages → Build and deployment → Deploy from a branch → main → /(root) → Save**.

> Educational demonstration only. Not for operational flight planning. Runway heading and wind direction must use the same magnetic/true reference. Runway numbers are rounded and are not precise published headings.
