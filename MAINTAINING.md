# Maintaining this kit

Notes for whoever owns the kit. Everyone else wants [README.md](README.md).

## Where this came from

Ported out of the personal `VideoProjects` repo, where the same capability runs as the
`graphic-design` skill under Claude Code. That version resolves a brand pack from the filesystem
(`_tools/brands/lemo-encore/`) and layers it over a universal `STYLE.md`. **This kit is
self-contained instead** — `references/brand.md` is the universal discipline and the lemo-encore
pack flattened into one file, because a claude.ai session has no filesystem.

Deliberately left behind: the carousel format layer, the travel-diary recipe, the Python helpers,
the PowerShell fallback runner, and the brand-pack resolution mechanism. None survive the move to a
web session, and none are needed here.

## Shipping a change

1. Edit under `skill/lemo-encore-design/`.
2. Run `.\build.ps1` — writes `build/lemo-encore-design.zip` (gitignored).
3. Commit the source change.
4. Cut a GitHub release and attach `lemo-encore-design.zip` plus the current
   `lemo-brand-assets.zip`.
5. Tell the team to re-download. **There is no push mechanism** — whoever uploaded v1 keeps running
   v1 forever until they upload a new one.

**Don't use `Compress-Archive`.** Windows PowerShell 5.1 writes entry paths with backslashes, which
the ZIP spec forbids; extractors that honour the spec read `lemo-encore-design\SKILL.md` as a flat
filename rather than a folder, and the skill won't load. `build.ps1` writes forward slashes.

The zip must contain the `lemo-encore-design/` folder with `SKILL.md` at its root.

## Brand assets

`assets/logos/` holds the source logo artwork. The **Penpot import file** (`lemo-brand-assets.zip`)
is built by hand from Penpot's own export, not by a script:

- Build a Penpot file with one page containing both logo sets
- Groups named exactly `Lemo Logos` and `Encore Logos`
- Children named `Logo / Black`, `Logo / White` (LEMO) and `Logo / Navy`, `Logo / Red`,
  `Logo / White` (Encore)
- Export it from the Penpot dashboard and attach to the release

**Those names are load-bearing.** `brand.md` documents the measured alpha-extent geometry for
placing the marks, and `SKILL.md` blocks the build if the groups are absent. Rename anything in
Penpot and both break.

## Fonts and licensing

Only Montserrat is assumed. It's a Google font, ships with Penpot, and per the brand book is a
genuine brand face for both sub-brands — so the kit works with zero font installation.

**Before putting font binaries in this repo, check what you're allowed to redistribute:**

- Display faces derived from sports-team wordmarks carry trademark considerations separate from
  any font licence; check both before adding one.
- **Futura** — commercial under every cut (Linotype, Paratype, Bitstream). Redistribution is not
  permitted.
- **Pirulen** — a Larabie face; free for personal use, commercial use typically needs a licence.

Safest is to keep `assets/fonts/` as instructions on where to obtain each one, and let people
install them into their own Penpot account. Flagged 2026-08-20; the call is LEMO's.

## Keeping it in sync with VideoProjects

The two copies will drift. When a real lesson gets learned on either side:

- **Brand decisions** (a colour rule, a type gotcha, a logo measurement) → update *both*
  `_tools/brands/lemo-encore/STYLE.md` in VideoProjects and `references/brand.md` here.
- **Penpot API gotchas** → `references/penpot-api.md` in both. Usually copy-paste identical; this
  version just has repo-local paths stripped.
- **Method / workflow changes** → likely diverge. The VideoProjects skill assumes a designer
  driving it; this one assumes a non-designer with nobody reviewing the output. Don't blindly copy
  `SKILL.md` across.

Record brand decisions with a dated line in the changelog of the VideoProjects pack, the way that
repo already does. This kit's `brand.md` intentionally has no changelog, to stay readable for
non-designers.

## Things to watch

- **Plan gating.** Custom connectors need Pro/Max/Team. A free-tier teammate can't use this at all,
  and it looks like "the connector page has no Add button."
- **The tab-open requirement is the #1 support call.** Penpot's MCP is browser-relayed, so Penpot
  must be open with MCP on *before* the chat starts.
- **Everyone needs their own Penpot key.** Never distribute yours — a key is account-scoped.
- **The empty-file problem.** New accounts have no logos, which is why `SKILL.md` step 3 blocks the
  build. If someone reports "it won't design anything," check they imported the assets.

## Demo suggestion

The pitch lands better if they watch a **revision**, not a build. Have a flyer already made, then
let someone ask for three changes live — a wrong date, a bigger headline, a dark version. The point
isn't that Claude can design; it's that they stop waiting on you for round two.
