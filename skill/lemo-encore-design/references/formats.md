# Formats — resolving what to actually build

The person asking for a design usually knows **where it will be seen**, not what size it should
be. Never ask them for an aspect ratio, a pixel dimension, or a DPI — those are yours to derive.

Ask at most two things:

1. **Where will people see this?** (on their phone, printed in hand, on a wall, on the lobby TV,
   in a slide deck, worn)
2. **How big is it physically?** — only for print or signage.

Then resolve everything else from the tables below.

## Presets — the frequent work

If what they describe matches one of these, use it and don't ask further.

### Screen

| Preset | Pixels | Notes |
|---|---|---|
| Instagram post (square) | 1080 × 1080 | |
| Instagram post (portrait) | 1080 × 1350 | preferred — takes more feed height |
| Instagram story / Reel cover | 1080 × 1920 | mind the safe zones below |
| Facebook / event cover | 1200 × 630 | |
| Lobby TV slide | 1920 × 1080 | keep everything inside a 5% inset |
| Email header | 1200 × 400 | |
| Slide for a deck | 1920 × 1080 | |
| Virtual background | 1920 × 1080 | |

**All screen pieces:** dark ground (`#0F1720`), orange `#FE5700`.

### Print — 300 DPI

`pixels = inches × 300`

| Preset | Inches | Pixels |
|---|---|---|
| Flyer | 8.5 × 11 | 2550 × 3300 |
| Half-sheet flyer | 8.5 × 5.5 | 2550 × 1650 |
| Sign-up sheet | 8.5 × 11 | 2550 × 3300 |
| Poster | 11 × 17 | 3300 × 5100 |
| Postcard | 6 × 4 | 1800 × 1200 |
| Business card | 3.5 × 2 | 1050 × 600 |

**All print pieces:** white ground, orange `#F26122` (or `#EC5524` if it prints on black),
**42px type floor** for anything meant to be read (that's 10pt — see `brand.md`).

### Large format — 150 DPI

Anything over ~24 inches on its long edge. At that size 300 DPI produces files too big to work
with, and nobody views a yard sign from 12 inches away.

`pixels = inches × 150`

| Preset | Inches | Pixels |
|---|---|---|
| Yard sign | 24 × 18 | 3600 × 2700 |
| Retractable banner | 33 × 80 | 4950 × 12000 |
| Table throw front | 72 × 30 | 10800 × 4500 |

Scale the type ladder up proportionally — the px floor is meaningless here; judge by viewing
distance. A yard sign is read from ~15 feet, a banner from ~10.

## Anything not on the list

Nonprofit work throws up formats no table covers. Derive it:

1. **Screen?** Use the destination's native pixel size. If they don't know it, ask what device or
   platform and look it up rather than guessing. Dark ground, `#FE5700`.
2. **Print?** Get the physical size in inches. `px = in × 300` (or × 150 above ~24in). White
   ground, `#F26122`. Type floor 42.
3. **Bleed** — if any colour or image runs off the edge, add **0.125in on every side** and tell
   them the piece has bleed so they order it that way. An 8.5 × 11 flyer with bleed is
   8.75 × 11.25 → 2625 × 3375. If nothing touches the edge, skip bleed.
4. **Margins** — keep content at least **0.25in** off the trim on print. Home and office printers
   have an unprintable border of roughly 0.2in; anything closer may be shaved off.

## Safe areas

- **Instagram story / Reel** — keep text clear of the **right action rail** and the **bottom
  caption and username band**. Roughly: 250px off the bottom, 150px off the right.
- **Lobby TV** — inset everything 5%. TVs overscan and will crop the edges.
- **Print** — 0.25in minimum off the trim, more if it will be held in a folder or stapled.

## Sanity check before building

- Is this **LEMO or Encore**? It changes the palette and the display face.
- Is this **print or screen**? It changes the ground, the orange, and the type floor.
- Does anything **run off the edge**? That decides bleed.
- Will it be read or scanned? That decides whether 42 is a floor or a starting point.
