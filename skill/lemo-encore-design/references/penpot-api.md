# Penpot API — operating manual & gotchas

Every item below was paid for by a failed build. Read it before writing non-trivial
`execute_code`. The companion helper library ([`penpot-helpers.js`](penpot-helpers.js)) wraps the
common patterns — load it into `storage` first thing each session.

## Running code & seeing results

- **`execute_code`** — runs JS in the Penpot plugin context. Globals: `penpot` (the API),
  `penpotUtils`, and **`storage`** (a persistent object — stash intermediates and functions here to
  reuse across calls, e.g. `storage.gd`, `storage.manifest`). The body is a function: `return`
  whatever you want back (objects are fine, no `JSON.stringify`). `console.*` output comes back
  separately — **don't log data you're also returning** (you'll get it twice).
- **~30s timeout.** Keep calls bounded; don't sweep hundreds of shapes with heavy work in one go.
- **Oversized returns auto-save to disk** and come back as a file path. Read that file rather than
  expecting inline data.
- **`export_shape`** — PNG/SVG of a shape *as it appears* (`mode:"shape"`, includes descendants) or
  its raw image fill (`mode:"fill"`). Needs a **FULL** shape id. Special ids: `"selection"`,
  `"page"`. **Group and full-page exports time out** — export individual boards by id.

## When calls hang

Penpot's tools split into two families that fail differently:

| Tool | Served by | If broken |
|---|---|---|
| `high_level_overview`, `penpot_api_info` | the MCP **server** (static text) | still answers instantly |
| `execute_code`, `export_shape` | **relayed to the browser tab** | hangs to timeout |

So `high_level_overview` succeeding proves nothing about the connection — it returns static text
regardless. **The only real test is a relayed call: `return 42;`.**

If the relayed calls hang while the server-served ones answer, the token and transport are fine and
the browser side isn't bound. Have the user open their Penpot tab with the MCP toggle on and reload
it, then retry. See step 0 in `SKILL.md`.

**A malformed request body hangs identically to a dead connection** — the server frequently
swallows a bad call rather than erroring. So before blaming Penpot or the user's setup, run the
`return 42;` control through your own code path.

## DANGER — calls that corrupt the file

**`penpot.createShapeFromSvg()` fed `generateMarkup()` output produces shapes the SERVER rejects.**
This is the worst failure mode in the API because *it looks like it worked*:

1. The call returns valid shape ids and the shapes appear on canvas.
2. On the next sync, `update-file` returns **400 `:referential-integrity`** — `:invalid-geometry`,
   `:parent-not-found`, `:frame-not-found`, `:not-head-main-not-allowed`.
3. The client runs `:persistence/discard-persistence-state` and **throws away the whole commit.**
   Everything you built in that call is gone.
4. The plugin dies, so the *next* call fails with *"No Penpot instance connected for user token"* —
   which points at the token and is **not** a token problem.

The user sees a full-page **Internal Error** and can download a `report.txt`. That report is the
fastest diagnosis available — ask for it rather than guessing.

**Do this instead: `shape.clone()`.** Native, safe, and it carries fills and children faithfully.
The catch: **`clone()` cannot cross pages**, so build beside the assets you need to copy rather than
on a separate page.

**Corollary — verify persistence after any large build.** Re-query the ids in a *separate* call. A
build that returned ids but whose shapes are absent on the next call was rolled back.

## Exports and image fills

`mode:"shape"` renders image fills fine, including whole boards full of photos. You *can* visually
QA a composite that includes photography. What's actually true:

- **A blank export is usually a TRANSIENT LOAD RACE — retry before concluding anything.** A large
  source image (e.g. 2667×4000) can export blank several times in a row and then render perfectly
  once the browser has it cached. Its `fills[0].fillImage` looks valid throughout, so inspecting the
  fill tells you nothing.
  **Do NOT tell the user their upload is corrupt, and do NOT ask them to re-upload**, on the
  strength of a few blank exports. Instead:
  1. **Ask whether they can see it in Penpot.** Canvas is the source of truth; this export path is
     not. If they see it, the asset is good and only your view is broken.
  2. Retry a few times, and again after other calls have touched the file.
  3. Only if it's *also* invisible on their canvas is the upload actually bad.
- **`mode:"fill"` fails on large source images**, erroring `session expired`. It exports the *raw*
  image at full resolution, so display size doesn't help. Prefer `mode:"shape"`, which renders at
  the shape's display size.
- Exports time out intermittently under load. A bare retry usually succeeds — don't re-diagnose the
  connection over one timeout.

## Resizing an image fill to the wrong aspect ratio CROPS it (silently)

Image fills default to `keepAspectRatio: true`, so `shape.resize(w, h)` at a ratio that doesn't
match the source **fills and clips** — it does not letterbox and does not distort. Nothing errors;
you just get a photo with its subject cut off.

**Always derive one dimension from the source ratio:**

```js
const f = s.fills[0].fillImage, ar = f.width / f.height;
s.resize(W, Math.round(W / ar));           // never hand-pick both
```

Bottom-align a row of mixed-ratio images to a shared baseline rather than forcing equal heights.

## Blend modes: work in Penpot, DEAD in `export_shape`

`shape.blendMode` accepts and stores every CSS mode, and Penpot's **canvas and its own UI exporter
composite them correctly**. But **`export_shape` does not composite a blend mode against the layers
beneath it** — it blends against an empty backdrop:

| mode | via `export_shape` | via Penpot UI |
|---|---|---|
| `multiply` / `overlay` / `soft-light` / `color` | pure **black** | correct |
| `screen` / `luminosity` | flat **grey** | correct |
| `normal` + alpha | correct | correct |

Consequence: a design using blend modes is **unverifiable from this side** — every check has to
route through the user. Treat that as a real cost, not a footnote.

Stick to **alpha scrims and linear gradients** (`normal` blend). Those composite correctly
everywhere. If you suspect a blend-mode artifact, lay swatches of each mode side by side over a
photo and export — black/grey columns mean the export path, not your geometry.

## Text — traps

- **`fontId` ALONE DOES NOT SET THE WEIGHT — you must set `fontVariantId`.** Assigning only
  `t.fontId = 'gfont-montserrat'` renders **regular**, so a headline specified as Montserrat 800
  comes out visibly light while every other property looks correct. Nothing errors. Set both
  defensively, since which one takes depends on the build:
  ```js
  t.fontId = 'gfont-montserrat';
  try{ t.fontVariantId = '800'; }catch(e){}
  try{ t.fontWeight    = '800'; }catch(e){}
  ```
  When rebuilding an existing design, **read the source's `fontVariantId` first** — it isn't
  returned by a casual property dump, so it silently defaults and you ship the wrong weight.
- **`await penpot.openPage(p)` DOES NOT PERSIST BETWEEN CALLS.** Each `execute_code` starts on
  whatever page the *user* is on, so a second call that assumes the page you opened last time
  silently reads the wrong one — typically surfacing as `Cannot read properties of undefined` when
  a find-by-name returns nothing. Call `openPage` inside **every** call that touches a non-current
  page.
- **`letterSpacing` rejects negative values** (`Value not valid: -0.91`). No optical tightening on
  display type; clamp to `>= 0`.
- **`growType:'auto-height'` with a huge fixed width still wraps.** For a single-line ticker set
  `growType='auto-width'` and skip `resize()`. Its `width` reads back as `1` until a later call —
  measure it in the *next* `execute_code`, not inline.
- **A text box carries dead leading BELOW the glyphs — never bottom-anchor by the box.** At
  `fontSize:288 / lineHeight:0.86` the box ran ~40px past the last glyph row (~14% of the font size;
  it scales). Placing the box bottom on a 64px margin leaves a ~110px optical gap that reads as a
  mistake. Place by the *glyph* bottom:
  `y = targetGlyphBottom + deadLeading − boxHeight`. Same on the left — a display glyph sits ~2px
  inside its box. **Measure the exported PNG** rather than guessing.
- **TRACKED TEXT OVERFLOWS A BOX SIZED TO THE GLYPH RUN.** `letterSpacing` is applied *after* the
  text measures, so a box wide enough for the characters still wraps once tracking is on. Budget
  roughly **`chars × tracking`** of extra width — a 24-char line at `size:42` measures ~605px but
  needs ~653px at `track:2`, so in a 640px box it silently becomes two lines and wrecks the vertical
  rhythm below it. **The failure is silent.** Either oversize the box or use `growType:'auto-width'`
  and position by `x`.

## Fills — hex + opacity, NOT rgba

A fill is an object with a **hex** colour and a **separate** opacity. Passing rgba or a bad shape
throws `Value not valid ... Code: :fills`.

```js
shape.fills = [{ fillColor:"#FE5700", fillOpacity:0.9 }];
```

**Gradients: BOTH linear and radial require a `width` field.** Omitting it gives the same `:fills`
error, which names every stop and looks like a stop problem. Stops are `{offset, color, opacity}`;
`opacity:0` is legal.

```js
// linear — note width:1
shape.fills = [{ fillColorGradient:{ type:"linear", width:1, startX:0.5,startY:0, endX:0.5,endY:1,
  stops:[{offset:0,color:"#000000",opacity:0.6},{offset:1,color:"#000000",opacity:0}] } }];
// radial — note width:1
shape.fills = [{ fillColorGradient:{ type:"radial", startX:0.5,startY:0.5, endX:0.5,endY:0,
  width:1, stops:[{offset:0,color:"#FFFFFF",opacity:0.5},{offset:1,color:"#FFFFFF",opacity:0}] } }];
```

Also rejected: a `fillOpacity` key alongside `fillColorGradient` on the same fill object. Put the
alpha in the stops.

**A scrim rect's own EDGE renders as a visible hard line, even where its gradient is at
`opacity:0`.** Don't build a scrim stack out of partial-height rects — three of them
(top/bottom/right) produced two black lines across a photo board that the user spotted immediately.
**Single-source it: one full-board rect per axis**, with the fade expressed as interior stops.

```js
// one full-board vertical scrim: dark top, clear middle, dark bottom — no internal edges
s.fills=[{fillColorGradient:{type:'linear',width:1,startX:0.5,startY:0,endX:0.5,endY:1,stops:[
  {offset:0,color:INK,opacity:0.55},{offset:0.24,color:INK,opacity:0.04},
  {offset:0.44,color:INK,opacity:0},  {offset:0.66,color:INK,opacity:0.48},
  {offset:1,color:INK,opacity:0.96}]}}];
```

## Shadows

Array of shadow objects. `= []` removes; `= [{...}]` sets. Use **large blur** so it reads as a soft
aura, not a black rim (see `brand.md`).

```js
shape.shadows = [{ style:"drop-shadow", offsetX:0, offsetY:2, blur:30, spread:0,
  hidden:false, color:{ color:"#000000", opacity:0.35 } }];
```

## Strokes

```js
shape.strokes = [{ strokeColor:"#FFFFFF", strokeOpacity:1, strokeWidth:3,
  strokeAlignment:"center", strokeStyle:"solid" }];
```

Frames, graphic marks and speech-bubble edges only — never body text.

## Traversal — there is no `currentPage.children`

`penpot.currentPage` has only `{id, name, background, flows, rulerGuides}` — **no `.children`**.
Get shapes with **`penpot.currentPage.findShapes()`** (the FLAT list of every shape). To walk the
tree, recurse on `.children` (present on boards and groups, absent on leaves):

```js
const all = penpot.currentPage.findShapes();          // flat, everything
const kids = n => (n && n.children) ? n.children : [];
const board = all.find(s => s.type==='board' && s.name==='FLYER_v1');
(function walk(n){ kids(n).forEach(c => { /* ... */ walk(c); }); })(board);
```

## Reading a page you're not on

A non-current `Page` object exposes only `{id, name, background, flows, rulerGuides}` —
`page.root.children` is `undefined` and `page.findShapes()` returns `[]`. Page contents are only
readable once that page is open (`await penpot.openPage(page)`). `openPage` itself is safe.

## Boards, z-order, hierarchy

- **Board children move WITH the board** when you set `board.x`. **So NEVER also shift the children
  yourself.** Doing both applies the delta twice and throws every child outside the board's clip,
  leaving a board that renders as a solid colour block with its contents apparently gone (they're
  intact, just at `2×delta`). To relocate a board, set `board.x`/`board.y` and touch nothing else.
  The tell for a double-move: the children's coords sit exactly one delta beyond the board's own.
- **`board.appendChild(shape)` adds to the top of the stack AND reorders** an existing child to
  top — this is how you set **z-order** (append in back-to-front order). There is no z-index
  property.
- **`shape.clone()`** duplicates; **`shape.remove()`** deletes. To copy an asset into a board:
  `const c = src.clone(); board.appendChild(c); c.x = ...; c.y = ...`.

## Positioning rotated shapes

`shape.bounds` is in **absolute page coordinates**, so computing an offset from `bounds` places the
shape relative to the *page*, not its board — on a board at x=6900 the shape silently lands near
x=0 and vanishes from the export. After setting `rotation`, always place with
**`penpotUtils.setParentXY(shape, localX, localY)`**, which is rotation-safe.

## Transform

- `shape.rotation` is in **degrees**.
- To resize freely, **set `shape.proportionLock = false` first**, then `shape.resize(w, h)`.

## Creating shapes

`penpot.createRectangle()`, `createText(str)`, `createEllipse()`, `createBoard()`. New shapes land
at the page root — `board.appendChild()` them, then set `x`/`y` (board-local coords once parented).

**`createShapeFromSvg()` is on the danger list above — prefer `clone()`.**
