# LEMO / Encore Design Kit

Make on-brand LEMO and Encore graphics — flyers, posters, social posts, TV slides, postcards,
banners — by chatting with Claude. Claude builds them in Penpot, shows you a picture, and you tell
it what to change.

**You do not need to know how to design, and you do not need to write any code.**

---

## What you need first

| | |
|---|---|
| **A Claude account** | Pro, Max, or Team. (Custom connectors aren't available on the free plan.) |
| **A Penpot account** | Free. You'll make your own at [penpot.app](https://penpot.app). |
| **A browser** | Penpot has to stay open in a tab while you work. |

Setup takes about ten minutes and you only do it once.

---

## Setup

### 1. Download the two files you need

From this repo's **Releases** page:

- **`lemo-encore-design.zip`** — the design skill
- **`lemo-brand-assets.zip`** — the LEMO and Encore logos

Save both somewhere you can find them again.

### 2. Make a Penpot account and import the logos

1. Go to [penpot.app](https://penpot.app) and sign up.
2. From the dashboard, click **Import file** and select `lemo-brand-assets.zip`.
3. That adds a page containing both the LEMO and Encore logo sets. Claude needs these — it will
   refuse to build without them rather than fake a logo.

### 3. Get your Penpot key

1. In Penpot, click your avatar (top right) → **Settings**.
2. Find the **MCP** section and turn it **on**.
3. Generate a key and **copy it**. It's a long string of letters and numbers.

> **Keep this private.** It's a password to your Penpot account. Don't paste it into Slack, email,
> or a shared doc. If it ever leaks, come back here and generate a new one.

### 4. Connect Penpot to Claude

1. Go to [claude.ai](https://claude.ai) → your initials (bottom left) → **Settings** →
   **Connectors**.
2. Click **Add custom connector**.
3. Name it `Penpot`.
4. For the URL, paste this — replacing `YOUR_KEY_HERE` with the key you just copied:

   ```
   https://design.penpot.app/mcp/stream?userToken=YOUR_KEY_HERE
   ```

5. Save. Penpot should now appear in your connector list.

### 5. Add the design skill

1. In Claude, go to **Settings** → **Capabilities** → **Skills**.
2. Click **Upload skill** and pick `lemo-encore-design.zip`.

That's it. You're set up.

---

## Using it

**Every time, before you start a chat:**

1. Open your Penpot file in a browser tab.
2. Make sure the **MCP toggle is on**.
3. **Leave that tab open.** Claude works through it — if you close it, Claude loses its hands.

Then start a new chat in Claude and describe what you want.

### What to say

Describe the piece the way you'd describe it to a person. The more of this you include, the fewer
questions Claude has to ask:

- **LEMO or Encore** — they have different colours and fonts
- **What it is and where people will see it** — "a flyer we're printing", "an Instagram story",
  "a slide for the lobby TV". You don't need to know pixel sizes; Claude works that out.
- **The actual words** — dates, times, prices, location, contact, and what it should say
- **Anything that must be on it** — a logo, a QR code, a sponsor, a deadline

**A good first message looks like this:**

> Make me a print flyer for Encore volleyball tryouts, 8.5x11.
> Tryouts are Saturday March 14, 9am-12pm at Lincoln High School gym.
> Ages 12-18. $25 to register. Sign up at encorevb.com/tryouts.
> Headline should say "TRYOUTS ARE HERE". Needs the Encore logo.

Claude will ask about anything it still needs, build a first version, and show you a picture.

### Claude will not make up facts

If you don't give it a date, a price, or a location, it puts `[DATE TBD]` on the page instead of
inventing something. That's on purpose — a made-up date that *looks* right is how a whole print run
gets wasted. If you see a placeholder in your design, that's Claude telling you it needs that
information from you.

### Getting changes made

This is the part that matters — **you can revise it yourself, as many times as you want.** Just say
what's wrong in plain language:

- "Make the headline bigger"
- "The date is hard to read"
- "Move the logo to the bottom"
- "Can we try it on a dark background"
- "The price should be $30, not $25"
- "It feels cramped"
- "Go back to the previous version"

Claude makes the change, exports a new picture, and shows you. Keep going until it's right.

### When it's done

Ask Claude to export the final file, or download it yourself from Penpot (**File → Export**). For
print, ask for a PDF; for screen, a PNG.

---

## Fonts (optional)

**You don't need to install anything.** Montserrat is a real LEMO and Encore brand font and it's
already in Penpot for everyone. Both logos are placed as artwork rather than typed text, so you can
make a fully on-brand piece with no font setup at all.

If you want the display faces — **Pirulen** for LEMO headlines, **NFLMinnesota Vikings** for Encore
— you have to add them yourself:

1. Get the font files (see `assets/fonts/`).
2. In Penpot, go to your **Dashboard → Fonts** and upload them.
3. Tell Claude you've installed them, otherwise it will stay on Montserrat.

---

## If something goes wrong

**"Penpot isn't talking to me" / Claude says it can't connect**

In this order:

1. Is your Penpot file open in a browser tab? Open it.
2. Is the MCP toggle on? Turn it on.
3. Reload the Penpot tab.
4. Tell Claude to try again.

This is almost never a problem with your key — **don't generate a new one**, that usually makes it
worse. The tab just needs to be live first.

**Claude says it can't find the logos**

You skipped step 2, or you're in a different Penpot file from the one you imported them into.
Import the brand assets from the dashboard.

**Claude shows me a blank image**

Usually a big photo that hasn't loaded yet. Ask it to try the export again. If the design looks
fine to you in Penpot, the file is fine.

**Penpot shows a full-page "Internal Error"**

Download the `report.txt` it offers and paste it to Claude — it says exactly what went wrong. Then
reload the tab and carry on. Your design is recoverable.

**It made something ugly or off-brand**

Say so, specifically. "That doesn't look like our stuff" is less useful than "the orange looks wrong
next to the navy" or "the text is too small to read". Claude has the full brand book and will
usually know which rule it broke.

---

## What's in this repo

```
skill/lemo-encore-design/   the skill source
  SKILL.md                  how Claude behaves as the designer
  references/
    brand.md                the LEMO/Encore brand book - type, colour, logos, rules
    formats.md              sizes, DPI and safe areas for every kind of piece
    penpot-api.md           how to drive Penpot without breaking things
    penpot-helpers.js       helper code Claude loads at the start of each session
assets/                     logo artwork and font notes
build.ps1                   packages the skill zip for a release
```

Maintaining this? See [MAINTAINING.md](MAINTAINING.md).
