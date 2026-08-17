# Maintaining this kit

Notes for whoever owns the kit (currently Austin). Everyone else wants [README.md](README.md).

## Where this came from

Ported out of the `VideoProjects` repo, where the same capability runs as the `graphic-design`
skill under Claude Code. That version resolves the brand pack from the filesystem
(`_tools/brands/lemo-encore/`) and layers it over a universal `STYLE.md`. **This kit is
self-contained instead** — `references/brand.md` is the universal discipline and the lemo-encore
pack flattened into one file, because there's no filesystem on claude.ai.

Deliberately left behind: the carousel format layer, the travel-diary recipe, the Python helpers
(`align-cutout.py`, `image-treat.py`), the PowerShell fallback runner, and the whole brand-pack
resolution mechanism. None of them survive the move to a web session, and none are needed for
flyers.

## Rebuilding the zip

After editing anything under `skill/`:

```powershell
.\build.ps1
```

**Don't use `Compress-Archive`.** Windows PowerShell 5.1 writes entry paths with backslashes
(`lemo-design\SKILL.md`), which the ZIP spec forbids — some extractors then read that as one flat
filename instead of a folder and the skill won't load. `build.ps1` writes forward slashes.

The zip must contain the `lemo-design/` folder with `SKILL.md` at its root. Re-upload it in
Claude → Settings → Capabilities → Skills (replace the existing one).

Anyone who already uploaded the old version keeps running it until they re-upload. **There's no
push mechanism** — when you ship a meaningful brand change, tell the team to grab the new zip.

## Keeping it in sync with VideoProjects

The two copies will drift. When a real lesson gets learned on either side:

- **Brand decisions** (a colour rule, a type gotcha, a logo measurement) → update *both*
  `_tools/brands/lemo-encore/STYLE.md` in VideoProjects and `references/brand.md` here.
- **Penpot API gotchas** → `references/penpot-api.md` in both. These are usually copy-paste
  identical; the kit's version just has the repo-local paths stripped.
- **Method / workflow changes** → likely diverge. The VideoProjects skill assumes a designer
  driving it; this one assumes a non-designer. Don't blindly copy `SKILL.md` across.

Record brand decisions with a dated line in the "Changelog" section of the VideoProjects pack, the
way that repo already does — this kit's `brand.md` intentionally has no changelog, to keep it
readable for non-designers.

## Things to watch

- **Plan gating.** Custom connectors need Pro/Max/Team. A free-tier coworker cannot use this at
  all, and the failure will look like "the connector page has no Add button."
- **The tab-open requirement is the #1 support call.** Penpot's MCP is browser-relayed, so
  Penpot must be open with MCP on *before* the chat starts. The README leads with it and the
  skill's step 0 handles it, but expect to explain it in person during the demo.
- **Each person needs their own Penpot key.** Never distribute yours. A key is account-scoped, so
  a shared one would let anyone act as you in Penpot.
- **Fonts.** Only Montserrat is installed in Penpot. Pirulen, NFLMinnesota Vikings, Futura and
  Futura Book have to be uploaded to the Penpot file before anyone can set type in them. If the
  team will need display type, upload them to the shared file once rather than making each person
  do it.

## Demo suggestion

The pitch lands better if they watch a revision, not a build. Have a flyer already made, then let
someone from the team ask for three changes live — a wrong date, a bigger headline, a dark
version. The point isn't that Claude can design; it's that they stop waiting on you for round two.
