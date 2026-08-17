# LEMO / Encore Design Kit

Make on-brand LEMO and Encore graphics — flyers, posters, TV slides, social posts — by chatting
with Claude. Claude builds them in Penpot, shows you a picture, and you tell it what to change.

**You do not need to know how to design, and you do not need to write any code.**

---

## What you need first

| | |
|---|---|
| **A Claude account** | Pro, Max, or Team. (Custom connectors aren't available on the free plan.) |
| **A Penpot account** | With access to the shared LEMO design file. |
| **A browser** | Penpot has to stay open in a tab while you work. |

Setup takes about ten minutes and you only do it once.

---

## Setup

### 1. Get your Penpot key

1. Open [Penpot](https://design.penpot.app) and sign in.
2. Click your avatar (top right) → **Settings**.
3. Find the **MCP** section and turn it **on**.
4. Generate a key and **copy it**. It's a long string of letters and numbers.

> **Keep this private.** It's a password to your Penpot account. Don't paste it into Slack, email,
> or a shared doc. If it ever leaks, come back here and generate a new one.

### 2. Connect Penpot to Claude

1. Go to [claude.ai](https://claude.ai) → your initials (bottom left) → **Settings** →
   **Connectors**.
2. Click **Add custom connector**.
3. Name it `Penpot`.
4. For the URL, paste this — replacing `YOUR_KEY_HERE` with the key you copied in step 1:

   ```
   https://design.penpot.app/mcp/stream?userToken=YOUR_KEY_HERE
   ```

5. Save. You should see Penpot appear in your connector list.

### 3. Add the design skill

1. Download **`lemo-design.zip`** from this repo (it's in the `dist` folder — click it, then click
   **Download**).
2. In Claude, go to **Settings** → **Capabilities** → **Skills**.
3. Click **Upload skill** and pick the zip file.

That's it. You're set up.

---

## Using it

**Every single time, before you start a chat:**

1. Open your LEMO design file in Penpot, in a browser tab.
2. Make sure the **MCP toggle is on**.
3. **Leave that tab open.** Claude works through it — if you close it, Claude loses its hands.

Then start a new chat in Claude and describe what you want.

### What to say

You don't need special wording. Just describe the piece the way you'd describe it to a person.
The more of these you include, the fewer questions Claude has to ask:

- **What it is** — "a flyer", "a TV slide for the lobby", "an Instagram story"
- **LEMO or Encore** — they have different colours and fonts
- **Print or screen** — this changes the colours and the minimum text size
- **The actual words** — dates, times, prices, location, contact, and what you want it to say
- **Anything that must be on it** — a logo, a QR code, a sponsor, a deadline

**A good first message looks like this:**

> Make me a print flyer for Encore volleyball tryouts. 8.5x11.
> Tryouts are Saturday March 14, 9am–12pm at Lincoln High School gym.
> Ages 12–18. $25 to register. Sign up at encorevb.com/tryouts.
> Headline should say "TRYOUTS ARE HERE". Needs the Encore logo.

Claude will ask about anything it still needs, build a first version, and show you a picture.

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

Claude will make the change, export a new picture, and show you. Keep going until it's right.

### When it's done

Ask Claude to export the final file, or just download it yourself from Penpot
(**File → Export**). For print, ask for a PDF; for screen, a PNG.

---

## If something goes wrong

**"Penpot isn't talking to me" / Claude says it can't connect**

The usual fix, in this order:

1. Is your Penpot design open in a browser tab? Open it.
2. Is the MCP toggle on? Turn it on.
3. Reload the Penpot tab.
4. Tell Claude to try again.

This is almost never a problem with your key — **don't generate a new one**, that usually makes it
worse. The tab just needs to be live first.

**Claude shows me a blank image**

Usually a big photo that hasn't loaded yet. Ask Claude to try the export again. If you can see the
design fine in Penpot, the file is fine.

**Penpot shows a full-page "Internal Error"**

Download the `report.txt` it offers and paste it to Claude — it says exactly what went wrong.
Then reload the tab and carry on. Your design is recoverable.

**It made something ugly / off-brand**

Tell it so, specifically. "That doesn't look like our stuff" is less useful than "the orange looks
wrong next to the navy" or "the text is too small to read". Claude has the full brand book and will
usually know the rule it broke.

---

## What's in this repo

```
skill/lemo-design/          the skill source — edit here
  SKILL.md                  how Claude behaves as the designer
  references/
    brand.md                the LEMO/Encore brand book (type, colour, logos, rules)
    penpot-api.md           how to drive Penpot without breaking things
    penpot-helpers.js       helper code Claude loads at the start of each session
dist/lemo-design.zip        the packaged skill — this is what you upload to Claude
```

If you're maintaining this, see [MAINTAINING.md](MAINTAINING.md).
