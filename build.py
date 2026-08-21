#!/usr/bin/env python3
"""Build the LEMO / Encore design kit. Runs on macOS, Linux and Windows.

    python build.py              package build/lemo-encore-design.zip
    python build.py --assets     ALSO regenerate the bundled logo artwork from the masters
    python build.py --check      verify an existing zip without rebuilding

Packaging needs nothing but the standard library. Only --assets needs Pillow
(`pip install pillow`), and only whoever changes the logo masters ever needs to run it.

Why this is Python and not a shell script: the zip must use FORWARD SLASHES in its entry paths.
The ZIP spec (4.4.17.1) requires it, and extractors that honour the spec read a backslash entry
like "lemo-encore-design\\SKILL.md" as one flat filename instead of a folder, so the skill silently
fails to load. Windows PowerShell 5.1's Compress-Archive gets this wrong. Python's zipfile always
normalises to forward slashes, so the bug is impossible here rather than merely avoided.

Output is gitignored - attach it to a GitHub release rather than committing it.
"""

import argparse
import base64
import io
import json
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.abspath(__file__))
NAME = "lemo-encore-design"
SRC = os.path.join(ROOT, "skill")
OUT = os.path.join(ROOT, "build", NAME + ".zip")

MASTERS = os.path.join(ROOT, "assets", "logos")
BUNDLED = os.path.join(SRC, NAME, "assets", "logos")

# Downscale target for the bundled artwork.
#
# The masters are 5000x5000. Base64 travels through an execute_code call as literal tokens, so a
# master costs ~39k tokens to upload - more than the rest of a session. At 1500px the VISIBLE
# wordmark lands ~1080px wide (3.6in at 300dpi), which covers flyer use, for ~7-10k tokens.
# Raising this raises the per-session cost for every user.
LOGO_PX = 1500

# (master filename, output filename, Penpot group name, Penpot shape name)
#
# The group and shape names are LOAD-BEARING: SKILL.md creates the shapes with these names and
# brand.md places each mark by looking them up. Renaming anything here silently breaks every build
# for everyone who has already installed the skill.
VARIANTS = [
    ("LEMO (black).png",      "lemo-black.png",   "Lemo Logos",   "Logo / Black"),
    ("LEMO (white).png",      "lemo-white.png",   "Lemo Logos",   "Logo / White"),
    ("Encore Navy Logo.png",  "encore-navy.png",  "Encore Logos", "Logo / Navy"),
    ("Encore Red Logo.png",   "encore-red.png",   "Encore Logos", "Logo / Red"),
    ("Encore White Logo.png", "encore-white.png", "Encore Logos", "Logo / White"),
]


def build_assets():
    """Regenerate the bundled logo artwork, .b64 sidecars and manifest.json from the masters."""
    try:
        from PIL import Image
    except ImportError:
        sys.exit("--assets needs Pillow:  pip install pillow")

    os.makedirs(BUNDLED, exist_ok=True)
    manifest = []

    for src, out, group, shape in VARIANTS:
        path = os.path.join(MASTERS, src)
        if not os.path.exists(path):
            sys.exit("missing master: %s" % path)

        im = Image.open(path).convert("RGBA")
        if im.width != im.height:
            sys.exit("%s is %dx%d - masters must be square, the placement maths assumes it"
                     % (src, im.width, im.height))

        small = im.resize((LOGO_PX, LOGO_PX), Image.LANCZOS)
        buf = io.BytesIO()
        small.save(buf, "PNG", optimize=True)
        png = buf.getvalue()

        with open(os.path.join(BUNDLED, out), "wb") as f:
            f.write(png)
        b64 = base64.b64encode(png).decode()
        # No trailing newline: this is pasted verbatim into an execute_code call.
        with open(os.path.join(BUNDLED, out + ".b64"), "w", newline="") as f:
            f.write(b64)

        # Measure alpha extent on the DOWNSCALED file, not the master. Resampling spreads alpha a
        # fraction of a percent into the transparent margin, and this copy is the one that actually
        # gets placed, so it is the honest source of truth.
        bbox = small.getchannel("A").getbbox()
        if bbox is None:
            sys.exit("%s is fully transparent" % src)
        x0, y0, x1, y1 = bbox

        manifest.append({
            "file": out, "group": group, "shape": shape, "square": LOGO_PX,
            "x0": round(x0 / LOGO_PX, 4), "x1": round(x1 / LOGO_PX, 4),
            "y0": round(y0 / LOGO_PX, 4), "y1": round(y1 / LOGO_PX, 4),
            "contentAspect": round((x1 - x0) / (y1 - y0), 3),
            "b64Bytes": len(b64),
        })
        print("  %-18s %6.1fKB png  %6.1fKB b64  ~%5d tokens"
              % (out, len(png) / 1024, len(b64) / 1024, len(b64) // 4))

    with open(os.path.join(BUNDLED, "manifest.json"), "w", newline="\n") as f:
        f.write(json.dumps(manifest, indent=2) + "\n")

    print("\n  manifest.json:")
    for m in manifest:
        print("    %-16s %-14s x %.4f-%.4f  y %.4f-%.4f  ar %.3f"
              % (m["shape"], m["group"], m["x0"], m["x1"], m["y0"], m["y1"], m["contentAspect"]))


def build_zip():
    """Package skill/<NAME>/ into build/<NAME>.zip with forward-slash entry paths."""
    skill_dir = os.path.join(SRC, NAME)
    if not os.path.isdir(skill_dir):
        sys.exit("missing %s" % skill_dir)

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    if os.path.exists(OUT):
        os.remove(OUT)

    files = []
    for dirpath, dirnames, filenames in os.walk(skill_dir):
        dirnames.sort()
        for fn in sorted(filenames):
            full = os.path.join(dirpath, fn)
            # Sorted, relative, forward-slash - deterministic across machines.
            rel = os.path.relpath(full, SRC).replace(os.sep, "/")
            files.append((full, rel))
    files.sort(key=lambda p: p[1])

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for full, rel in files:
            z.write(full, rel)
            print("  + %s" % rel)

    print("\nBuilt %s" % OUT)


def check_zip():
    """Verify the packaged zip is well formed and its base64 payloads decode."""
    if not os.path.exists(OUT):
        sys.exit("no zip at %s - run: python build.py" % OUT)

    ok = True
    with zipfile.ZipFile(OUT) as z:
        names = z.namelist()
        bad = [n for n in names if "\\" in n]
        print("entries: %d | backslash entries: %d" % (len(names), len(bad)))
        if bad:
            print("  FAIL - these break folder structure on spec-compliant extractors:")
            for n in bad:
                print("    %s" % n)
            ok = False

        root_skill = "%s/SKILL.md" % NAME
        if root_skill not in names:
            print("  FAIL - %s missing; the skill will not load" % root_skill)
            ok = False

        man_path = "%s/assets/logos/manifest.json" % NAME
        if man_path not in names:
            print("  FAIL - %s missing" % man_path)
            return finish(False)

        for m in json.loads(z.read(man_path)):
            b64 = z.read("%s/assets/logos/%s.b64" % (NAME, m["file"])).decode()
            raw = base64.b64decode(b64)
            matches = raw == z.read("%s/assets/logos/%s" % (NAME, m["file"]))
            # PNG magic - proves atob() + Uint8Array will hand Penpot a real image.
            is_png = raw[:8] == b"\x89PNG\r\n\x1a\n"
            print("  %-16s b64 decodes to PNG: %-5s  matches bundled file: %s"
                  % (m["shape"], is_png, matches))
            ok = ok and is_png and matches

    return finish(ok)


def finish(ok):
    print("\n%s" % ("ALL CHECKS PASS" if ok else "CHECKS FAILED"))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Build the LEMO / Encore design kit.")
    ap.add_argument("--assets", action="store_true",
                    help="regenerate bundled logo artwork from assets/logos/ masters (needs Pillow)")
    ap.add_argument("--check", action="store_true",
                    help="verify the existing zip instead of rebuilding")
    args = ap.parse_args()

    if args.check:
        return check_zip()

    if args.assets:
        print("Regenerating logo artwork:")
        build_assets()
        print()

    build_zip()
    print()
    return check_zip()


if __name__ == "__main__":
    sys.exit(main())
