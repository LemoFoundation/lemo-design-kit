# LEMO / Encore — the design system

Everything you need to make something look like it came from LEMO. Two halves: the **universal
discipline** (type, spacing, shadow, accent — constant on every piece) and the **brand surface**
(the fonts and colours that make it LEMO or Encore specifically).

Source of truth for the brand surface: the *"BRAND COLORS & FONTS (current)"* sheet, 2026-07-27.

---

# Part 1 — Universal discipline

These are not preferences. They're what makes a layout read as *designed* rather than assembled,
and they hold for every piece regardless of sub-brand or medium.

## Type: the golden-ratio ladder

Base **42px**, every step ×/÷ 1.618:

```
16  ·  26  ·  42  ·  68  ·  110  ·  178
```

**Any two sizes in one lockup must be rungs on this ladder.** Never pick an in-between size to
make something fit — drop a rung instead. Using sizes from one ladder is the single biggest reason
hierarchy reads as intentional.

**On PRINT boards, convert to points before trusting the ladder.** At 300 DPI, `pt = px / 300 × 72`:

| rung | points at 300 DPI | use on print |
|---|---|---|
| 16 | 3.8pt | too small — don't |
| 26 | 6.2pt | fine print, labels, captions only |
| 42 | **10pt** | **the floor for anything meant to be read** |
| 68 | 16pt | subheads, deck |
| 110 | 26pt | headline |
| 178 | 43pt | display |

Setting a trust/credentials block at 26 makes the one paragraph that has to persuade into the
smallest type on the sheet. *(Learned on the LEMO tutoring flyer, 2026-07-27.)*

## Spacing: the 8-point grid

Every gap, margin and grouping distance is a multiple of 8. Even spacing is what separates a
designed lockup from an eyeballed one.

**One icon gutter per board.** When several stacked blocks pair an icon with text, any drift in
icon size or gutter produces text edges a few pixels apart — `160 / 162 / 166` in one real case.
Near-identical edges read as a *mistake* much faster than obviously different ones do. Fix the icon
box and gutter once, then verify mechanically:

```js
[...new Set(texts.map(t => t.x))].sort()   // near-duplicates in this list are the bug
```

**Rows that don't share column edges should be BANDS, not columns.** A 3-up row and a 2-up row can
sit on the same module and still not align at their edges. Rather than forcing a shared grid,
separate them with a hairline — as stripes, cross-row alignment stops being a question the eye
asks.

## Shadow: soft and wide, never an outline

A shadow's darkness concentrates at the glyph edge, so a tight or medium radius reads as a black
rim. Use **only large-radius blur** so it diffuses into an aura.

```js
shape.shadows = [{ style:"drop-shadow", offsetX:0, offsetY:2, blur:30, spread:0,
  hidden:false, color:{ color:"#000000", opacity:0.35 } }];
```

**Legibility over imagery is a scrim or a shadow — never a stroke.** Strokes belong on frames,
graphic marks and speech-bubble edges only. And if a gradient scrim already makes the text pop,
don't *also* shadow it.

## The accent

The accent colour is the one per-piece flex, and it lives on **graphic marks** — rules, bars,
panels, labels, icons — **never on body copy**. Coloured body text loses contrast against
unpredictable grounds and is the fastest way to make a piece look amateur.

For this brand the accent barely flexes at all: **the orange IS the identity** (it's the period in
both wordmarks).

## Photography

**A photo is either a SUBJECT or it isn't there. There is no useful middle.** Suppress a photo much
below ~50% visibility and it pays the full cost of a photo — a busy ground, constant legibility
management, several scrim layers — for none of the benefit. Either commit to it at full strength
and **build the layout around that specific frame's composition** (its bright band becomes the type
well), or drop it and use a flat ground.

If you're dimming a photo to make something else work, that's the signal to *remove* it, not to dim
it further.

## Safe areas (screen pieces)

For IG stories / Reels / TikTok, keep text clear of the **right action rail** and the **bottom
caption + username band**. For a lobby TV, keep everything inside a ~5% inset — TVs overscan.

---

# Part 2 — The brand surface

## One account, two sub-brands

LEMO and Encore Volleyball Club are **one brand pack with two surfaces**. Both wordmarks are the
same construction — a geometric sans closed by a period, with the period set in the same orange.
That orange is the shared identity. They share Montserrat and Futura; they differ only in display
face and palette temperature, which is exactly what a sub-brand is.

| | **LEMO** | **Encore** |
|---|---|---|
| Role | the service / organisation | the volleyball club |
| Display face | **Pirulen** | **NFLMinnesota Vikings** |
| Shared faces | Montserrat, Futura, Futura Book | Montserrat, Futura, Futura Book |
| Ink | black `#000000` | navy `#09162B` |
| Secondary | navy `#00264B`, gray `#545454` | red `#D60000` |
| Accent | orange `#FE5700` | orange (borrowed — it's the wordmark's period) |

**Ask which one the piece is for.** It changes almost every colour on the page.

## Fonts — read this before setting type

**Montserrat is a genuine brand face for both sub-brands**, not a substitute. It's the only brand
face **already installed in Penpot** (weights 100–900), so it can carry body, deck, label and even
headline work without compromise.

**Not available in Penpot — must be uploaded as custom fonts first:** Pirulen,
NFLMinnesota Vikings, Futura, Futura Book.

This is usually a non-issue, because **both wordmarks ship as logo artwork, not live type** — a
piece can be fully on-brand without the display faces. Only reach for them when a headline
genuinely needs the LEMO/Encore voice, and get them uploaded first.

**Setting weight is a two-step trap:** `fontId` alone renders regular. You must also set
`fontVariantId`. See `penpot-api.md`.

## Colour — pick the orange by substrate

The single most important rule in this brand. There are **three** LEMO oranges and they are not
interchangeable:

| Orange | Hex | Use |
|---|---|---|
| Digital | `#FE5700` | screens — TV slides, social, web, video |
| Print on white | `#F26122` | printed on white — paper flyers, light merch |
| Print on black | `#EC5524` | printed on black merch |

> **Do NOT "unify" these across a screen piece and a print piece — they are already the same
> colour.** Measured: `#FE5700` is L\* 59.8, `#F26122` is L\* 59.5 — a 0.3 difference, far below
> the visible threshold. They differ by ~6° of hue, invisible unless the pieces sit side by side.
> They are one ink rendered for two reproduction systems: `#FE5700` is outside CMYK gamut, so a
> press clips it toward roughly `#F26122` whether you specify it or not. Sending the print value to
> a screen throws away gamut; sending the digital value to a press just lets the *printer* choose
> the substitute instead of LEMO.
>
> **Exception:** if a print piece and a screen piece will be shown side by side *on a screen* (a
> deck, a social post), make a screen-only variant of the print piece using `#FE5700`.

The two navies are also distinct — LEMO `#00264B` is warmer and lighter than Encore `#09162B`.
Don't merge them.

## Do NOT put orange on saturated navy at scale

The most useful colour rule this brand has, learned the hard way:

> **LEMO orange and LEMO navy are near-complementary and both fully saturated.** Orange `#FE5700`
> is hue **21° / 100% S**; navy `#00264B` is hue **210° / 100% S** — **192° apart.**

At small areas (navy body text, an orange rule) that's fine and on-brand. But give **both** sides a
large area — an orange CTA block on a navy field — and the shared edge produces
**simultaneous-contrast vibration**. It reads as cheap, and no amount of type or layout work fixes
it. Complementary schemes stay calm only when one side is a small accent (60/30/10) **or** one side
is desaturated.

**The fix: keep the navy hue, collapse it to a neutral ramp, and let orange be the only chromatic
voice.** Every step below sits at ~210° with saturation stepped down:

| Role | Hex | Use |
|---|---|---|
| ground (dark) | `#0F1720` | screen backgrounds — a rich near-black, not flat `#000` |
| surface | `#1B2733` | raised panels on dark |
| line (dark) | `#2C3B4B` | hairlines on dark |
| muted (dark) | `#93A3B3` | footnotes on dark |
| tint (light) | `#F4F7FA` | section panels on white — structure at almost no toner |
| muted (light) | `#5A6B7C` | footnotes on white — **use instead of the `#545454` gray** |

Measured contrast: white on `#0F1720` **18.1:1**; muted **7.0:1**; orange **5.65:1**.

## Type on an orange field: set it WHITE

Two reasons, and the second decides it:

1. White knockout is the conventional CTA/button treatment, so an orange block with white type
   simply *reads* as a button.
2. **Saturated orange + near-black is the Halloween palette.** That association is a real brand
   cost on a piece aimed at parents, and it outweighs the contrast margin.

White-on-orange measures **3.19:1** — that clears WCAG's 3:1 floor for **large** text, so it's
correct for display lines. Ink-on-orange measures higher at 5.65:1, but optimising for that number
is what produced the Halloween look. **Set any small text on orange at weight 700**, and never run
long body copy on an orange field.

**Orange on white is 3.4:1** — large display type and graphic marks only. Never body copy, never
small labels.

## Choose the ground per medium — don't force a match

- **Print → white ground.** The printer's ~0.2in unprintable border disappears and toner stays low.
- **Screen → dark ground.** It's free, and the accent pops.

## Logo artwork geometry

The logo files are **squares with large transparent padding**, so placing art by its square
misaligns the wordmark. Measured content boxes (alpha extent, 2026-07-27):

| Mark | x range | y range | content aspect |
|---|---|---|---|
| LEMO | `15.70% – 87.90%` | `43.70% – 56.50%` | 5.641 |
| Encore | `4.20% – 96.10%` | `37.50% – 60.30%` | 4.031 |

Place by the **visible** box and back-solve the square:

```js
// want the visible wordmark W wide at (px, py), for LEMO:
const fx0=0.1570, fx1=0.8790, fy0=0.4370, fy1=0.5650;
const squareW = W / (fx1 - fx0);
const squareH = squareW;                      // the artwork is square
img.resize(squareW, squareH);
img.x = px - fx0 * squareW;
img.y = py - fy0 * squareH;
```

In Penpot the logos live on **Page 1** as `Lemo Logos` and `Encore Logos`, with children named
`Logo / <Variant>` (`Black` / `White` for LEMO; `Navy` / `Red` / `White` for Encore). **Anchor on
those names, not ids** — and clone them into your board rather than moving the originals. Note that
`clone()` cannot cross pages, so build on the page where the logos live, or copy them over first.

**These only exist if the person imported the brand-assets file** — every account is separate and a
fresh Penpot file has no logos. If the groups are missing, stop and get them imported; never
improvise a wordmark in live type. See step 3 of `SKILL.md`.

## Texture, if a piece reads flat

Texture should **reference how the object is actually made**. On merch graphics, screen-print
misregistration (an offset colour copy behind a block), halftone dots, and registration marks work
because screen printing genuinely does those things. Generic grain or noise is decoration.

Test before adding any texture: *does this reference how the thing is made?* If not, cut it. Keep
it behind the type at low opacity — if you read the texture before the headline, it's too loud.

---

## Still undefined

- **No CMYK build is documented for paper.** `#F26122` is specified for *merch* on a white
  substrate and is being used as the closest documented intent for white paper. If a real CMYK spec
  exists, add it here.
- **Voice and tone are not captured.** Get copy from the person requesting the piece; don't invent
  a house voice.
- The source sheet is labelled *"current"*, implying a revision may be planned. Re-confirm before a
  large print run.
