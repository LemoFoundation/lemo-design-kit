// penpot-helpers.js — load ONCE per session into Penpot `storage` via execute_code.
// Paste this whole file as the code of one execute_code call. It installs `storage.gd` with the
// tree/query/edit helpers so you don't re-derive them every turn.
// Then use e.g. `storage.gd.board('FLYER_v1')`, `storage.gd.setFill(s,'#FE5700',0.9)`.
//
// Rationale for each helper is in penpot-api.md. Nothing here mutates the design — it's just
// query + safe setters. Re-run it any time (it just reinstalls the object).

storage.gd = (function () {
  const kids = n => (n && n.children) ? n.children : [];

  // walk(fn, root?) — depth-first over the whole page (or a subtree). fn gets (node).
  function walk(fn, root) {
    const roots = root ? [root] : penpot.currentPage.findShapes().filter(s => !s.parent || s.parent.type === 'page');
    // simplest robust walk: iterate the flat list when no root given
    if (!root) { penpot.currentPage.findShapes().forEach(fn); return; }
    (function rec(n) { kids(n).forEach(c => { fn(c); rec(c); }); })(root);
  }

  const all = () => penpot.currentPage.findShapes();

  // board(name) — a board by exact name (top-level slide/artboard).
  const board = name => all().find(s => s.type === 'board' && s.name === name) || null;

  // byName(name, root?) — first shape with this name (optionally within a board/group).
  function byName(name, root) {
    let hit = null;
    if (root) { walk(n => { if (!hit && n.name === name) hit = n; }, root); return hit; }
    return all().find(s => s.name === name) || null;
  }

  // byId4(k) — shape whose id ends with these 4 chars. WARN: last-4 can collide on big
  // files; prefer byName/full id. Returns the first match.
  const byId4 = k => all().find(s => s.id.slice(-4) === k) || null;

  // children(board) — light inventory of a board's direct children (for manifests / probing).
  function children(b) {
    return kids(b).map(c => {
      const o = { id4: c.id.slice(-4), id: c.id, name: c.name, type: c.type,
        x: Math.round(c.x), y: Math.round(c.y), w: Math.round(c.width), h: Math.round(c.height) };
      if (c.type === 'text') { o.text = c.characters; o.fontId = c.fontId; o.fontSize = c.fontSize; o.grow = c.growType; }
      return o;
    });
  }

  // cloneInto(src, dest, x, y) — copy an asset (e.g. from a library group) into a board at
  // board-local x,y, placed on top. NEVER mutates src (that's the "don't move originals" rule).
  function cloneInto(src, dest, x, y) {
    const c = src.clone();
    dest.appendChild(c);            // parents it AND puts it on top
    if (x != null) c.x = x;
    if (y != null) c.y = y;
    return c;
  }

  // bringToTop(board, shape) — restack to front (append reorders an existing child).
  const bringToTop = (b, s) => b.appendChild(s);

  // setFill(shape, hex, opacity?) — hex + separate opacity (NOT rgba).
  const setFill = (s, hex, opacity) => { s.fills = [{ fillColor: hex, fillOpacity: opacity == null ? 1 : opacity }]; return s; };

  // setShadow(shape, {ox,oy,blur,spread,color,opacity}) — soft aura defaults. []=remove.
  function setShadow(s, o) {
    o = o || {};
    s.shadows = [{ style: 'drop-shadow', offsetX: o.ox ?? 0, offsetY: o.oy ?? 2,
      blur: o.blur ?? 30, spread: o.spread ?? 0, hidden: false,
      color: { color: o.color ?? '#000000', opacity: o.opacity ?? 0.35 } }];
    return s;
  }
  const clearShadow = s => { s.shadows = []; return s; };

  // setStroke(shape, {color,opacity,width,align,style}) — frames/marks only, not body text.
  function setStroke(s, o) {
    o = o || {};
    s.strokes = [{ strokeColor: o.color ?? '#FFFFFF', strokeOpacity: o.opacity ?? 1,
      strokeWidth: o.width ?? 3, strokeAlignment: o.align ?? 'center', strokeStyle: o.style ?? 'solid' }];
    return s;
  }

  // setText(shape, chars) / setAlign(shape, a) — align set defensively across aliases.
  const setText = (s, chars) => { s.characters = chars; return s; };
  function setAlign(s, a) { ['align', 'textAlign', 'horizontalAlign'].forEach(p => { try { s[p] = a; } catch (e) {} }); return s; }

  // borrowFont(fromShape, toShape) — copy a working fontId off an existing text shape
  // (more reliable than resolving via penpot.fonts.all).
  const borrowFont = (from, to) => { to.fontId = from.fontId; return to; };

  return { kids, walk, all, board, byName, byId4, children, cloneInto, bringToTop,
    setFill, setShadow, clearShadow, setStroke, setText, setAlign, borrowFont };
})();

// confirmation (not logged — returned once)
return { installed: Object.keys(storage.gd), boards: storage.gd.all().filter(s => s.type === 'board').map(b => b.name).sort() };
