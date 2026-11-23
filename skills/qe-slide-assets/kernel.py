# Helpers for the qe-slide-assets skill. Loading this file only defines functions.
# They need PyMuPDF (import name fitz) and Pillow; both are imported inside the functions.
import os
import re

ROMAN = ("", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X", "XI", "XII", "XIII", "XIV", "XV")
IN_TEXT = r"(shows?|reports?|presents?|lists?|summari[sz]es?|compares?|illustrates?|gives?|provides?|depicts?|plots?|displays?|contains?|is|are|and|we|also|further|\(|,)\b"


def qe_label_pattern(label):
    """(kind, compiled regex) for a caption that starts a line: 'Figure 2', 'Fig. 2.1', 'Table II', 'Algorithm 1'.
    A parenthetical such as '(panel c)' is ignored. Returns (None, None) for labels this cannot parse."""
    m = re.match(r"\s*\[?\s*(fig(?:ure)?\.?|tab(?:le)?\.?|alg(?:orithm)?\.?)\s*([0-9]+(?:\.[0-9]+)?|[IVXLC]+)\b", label, re.I)
    if not m:
        return None, None
    word, num = m.group(1).lower(), m.group(2)
    kind = "figure" if word.startswith("fig") else "table" if word.startswith("tab") else "algorithm"
    names = {"figure": r"(?:Figure|FIGURE|Fig\.?|FIG\.?)", "table": r"(?:Table|TABLE|Tab\.?)", "algorithm": r"(?:Algorithm|ALGORITHM|Alg\.?)"}[kind]
    nums = [re.escape(num)]
    if num.isdigit() and int(num) < len(ROMAN):
        nums.append(ROMAN[int(num)])
    elif num.upper() in ROMAN:
        nums.append(str(ROMAN.index(num.upper())))
    return kind, re.compile(r"^\s*\[?\s*%s\s*(?:%s)(?![0-9A-Za-z]|\.[0-9])" % (names, "|".join(nums)))


def qe_page_lines(page):
    """Text lines of a page as dicts: text, bbox (fitz.Rect), block index, size."""
    import fitz
    out = []
    for bi, b in enumerate(page.get_text("dict")["blocks"]):
        for ln in b.get("lines", []):
            txt = "".join(s["text"] for s in ln["spans"])
            if txt.strip():
                out.append({"text": txt, "bbox": fitz.Rect(ln["bbox"]), "block": bi,
                            "size": max(s["size"] for s in ln["spans"])})
    return out


def qe_find_caption(doc, label, hint_page=None):
    """Best caption line for `label`: (page index, fitz.Rect of the whole caption, caption text) or None.
    hint_page is 1-based. In-text mentions that start a line ('Table 3 shows ...') score lower."""
    import fitz
    kind, rx = qe_label_pattern(label)
    if rx is None:
        return None
    best = None
    for pno in range(len(doc)):
        lines = qe_page_lines(doc[pno])
        for i, ln in enumerate(lines):
            m = rx.match(ln["text"])
            if not m:
                continue
            rest = ln["text"][m.end():].lstrip(" ]")
            score = 2 if (not rest or rest[0] in ":.|") else 0
            score -= 3 if re.match(IN_TEXT, rest.lstrip(":. "), re.I) and not (rest[:1] in ":.") else 0
            if hint_page is not None:
                score += 3 if pno == hint_page - 1 else 1 if abs(pno - (hint_page - 1)) <= 2 else 0
            if best is None or score > best[0]:
                rect, text, j = fitz.Rect(ln["bbox"]), ln["text"], i + 1
                while j < len(lines) and lines[j]["block"] == ln["block"] and j - i < 14:
                    rect |= lines[j]["bbox"]
                    text += " " + lines[j]["text"]
                    j += 1
                best = (score, pno, rect, re.sub(r"\s+", " ", text).strip())
    return None if best is None else best[1:]


def qe_float_sides(page, cap, graphics=True):
    """Layout around a caption rectangle: column range, the stop lines above and below (prose, headings,
    other captions, page margins) and the content rectangles between the caption and each stop."""
    import fitz
    W, H = page.rect.width, page.rect.height
    blocks = [b for b in page.get_text("dict")["blocks"] if b.get("lines")]
    body = [fitz.Rect(b["bbox"]) for b in blocks if len(b["lines"]) >= 3 and 0.07 * H < b["bbox"][1] < 0.93 * H]
    X0 = min([r.x0 for r in body] + [cap.x0])
    X1 = max([r.x1 for r in body] + [cap.x1])
    mid = (X0 + X1) / 2
    narrow = [r for r in body if r.width < 0.55 * (X1 - X0)]
    two_col = len(narrow) >= 2 and any(r.x1 < mid + 5 for r in narrow) and any(r.x0 > mid - 5 for r in narrow)
    cx = (cap.x0 + cap.x1) / 2
    if two_col and cap.width < 0.6 * (X1 - X0) and abs(cx - mid) > 0.08 * (X1 - X0):
        xa, xb = (X0, mid - 4) if cx < mid else (mid + 4, X1)
    else:
        xa, xb = X0, X1
    colw = xb - xa

    def in_cols(r):
        return r.width > 0 and min(r.x1, xb) - max(r.x0, xa) > 0.5 * min(r.width, colw)

    cap_re = re.compile(r"^\s*\[?\s*(?:Figure|FIGURE|Fig\.?|FIG\.?|Table|TABLE|Algorithm)\s*(?:[0-9]+|[IVXLC]+)\b")
    head_re = re.compile(r"^\s*(?:[0-9]{1,2}(?:\.[0-9]{1,2}){0,3}\.?|[IVX]{1,4}\.|[A-H]\.)\s+[A-Z][A-Za-z ,:&/\-]{2,70}$")
    sizes = sorted(s["size"] for b in blocks if len(b["lines"]) >= 3 for ln in b["lines"] for s in ln["spans"])
    body_size = sizes[len(sizes) // 2] if sizes else 10.0
    stops, content = [], []
    for b in blocks:
        r = fitz.Rect(b["bbox"])
        if not in_cols(r) or (r & cap).get_area() > 0.5 * r.get_area():
            continue
        text = " ".join("".join(s["text"] for s in ln["spans"]) for ln in b["lines"])
        widths = [fitz.Rect(ln["bbox"]).width for ln in b["lines"]]
        toks = text.split()
        wordy = sum(1 for t in toks if re.fullmatch(r"[A-Za-z][A-Za-z'\-]+[,.;:)]?", t)) / max(1, len(toks))
        prose = (len(b["lines"]) >= 3 and len(toks) >= 25 and wordy > 0.8 and r.width > 0.35 * (X1 - X0)
                 and sorted(widths)[len(widths) // 2] > 0.8 * r.width)
        spans = [s for ln in b["lines"] for s in ln["spans"] if s["text"].strip()]
        strong = bool(spans) and (min(s["size"] for s in spans) > body_size + 0.4 or all(s["flags"] & 16 for s in spans))
        heading = len(b["lines"]) == 1 and len(toks) <= 12 and bool(head_re.match(text)) and strong
        if prose or cap_re.match(text) or heading or r.y1 < 0.07 * H or r.y0 > 0.93 * H:
            stops.append(r)
        else:
            content.append(r)
    if graphics:
        for info in page.get_image_info():
            r = fitz.Rect(info["bbox"])
            if in_cols(r) and r.get_area() < 0.9 * W * H:
                content.append(r)
        for d in page.get_drawings():
            r = fitz.Rect(d["rect"])
            if in_cols(r) and r.get_area() < 0.9 * W * H and (r.width > 2 or r.height > 2):
                content.append(r)
    top = max([s.y1 for s in stops if s.y1 <= cap.y0 + 1] + [0.06 * H])
    bottom = min([s.y0 for s in stops if s.y0 >= cap.y1 - 1] + [0.94 * H])
    above = [r for r in content if r.y0 >= top - 1 and r.y1 <= cap.y0 + 2]
    below = [r for r in content if r.y1 <= bottom + 1 and r.y0 >= cap.y1 - 2]
    return {"xa": xa, "xb": xb, "top": top, "bottom": bottom, "above": above, "below": below}


def qe_table_caption_side(doc, max_gap=22):
    """'up' if the tables of this document sit above their captions, 'down' if below, None if unclear.
    Votes come from the table captions that have table text on one side only."""
    import fitz
    rx = re.compile(r"^\s*\[?\s*(?:Table|TABLE|Tab\.)\s*(?:[0-9]+|[IVXLC]+)\s*\]?\s*[:.|]")
    votes = {"up": 0, "down": 0}
    for page in doc:
        lines = qe_page_lines(page)
        for i, ln in enumerate(lines):
            if not rx.match(ln["text"]):
                continue
            cap, j = fitz.Rect(ln["bbox"]), i + 1
            while j < len(lines) and lines[j]["block"] == ln["block"] and j - i < 14:
                cap |= lines[j]["bbox"]
                j += 1
            s = qe_float_sides(page, cap, graphics=False)
            up = any(cap.y0 - r.y1 <= max_gap for r in s["above"])
            down = any(r.y0 - cap.y1 <= max_gap for r in s["below"])
            if up != down:
                votes["up" if up else "down"] += 1
    if votes["up"] == votes["down"]:
        return None
    return "up" if votes["up"] > votes["down"] else "down"


def qe_locate_float(doc, label, hint_page=None, direction=None, pad=4, max_gap=22, table_side=None):
    """Clip rectangle of a figure, table or algorithm with its caption.
    Returns {'page': index, 'clip': fitz.Rect, 'direction': 'up'|'down', 'caption': text, 'debug': {...}} or None.
    'up' means the content sits above the caption. For tables the side is taken from the content next to
    the caption and, when both sides have content, from the document's other tables (pass table_side to
    reuse the result of qe_table_caption_side). The result is a first guess: view every crop before use."""
    import fitz
    found = qe_find_caption(doc, label, hint_page)
    if found is None:
        return None
    pno, cap, cap_text = found
    kind, rx = qe_label_pattern(label)
    page = doc[pno]
    W, H = page.rect.width, page.rect.height
    s = qe_float_sides(page, cap)
    xa, xb, top, bottom, above, below = s["xa"], s["xb"], s["top"], s["bottom"], s["above"], s["below"]
    gap_up = min([cap.y0 - r.y1 for r in above] + [9e9])
    gap_dn = min([r.y0 - cap.y1 for r in below] + [9e9])
    if direction is None:
        near_up, near_dn = gap_up <= max_gap, gap_dn <= max_gap
        if kind == "figure":
            direction = "up" if near_up or not below else "down"
        elif near_up != near_dn:
            direction = "up" if near_up else "down"
        else:
            side = table_side or qe_table_caption_side(doc, max_gap)
            direction = side or ("up" if gap_up + 4 < gap_dn else "down")
    clip = fitz.Rect(cap)
    pool = sorted(above, key=lambda r: -r.y1) if direction == "up" else sorted(below, key=lambda r: r.y0)
    for r in pool:
        gap = (clip.y0 - r.y1) if direction == "up" else (r.y0 - clip.y1)
        if gap > max_gap:
            break
        clip |= r
    clip = fitz.Rect(max(clip.x0 - pad, xa - pad, 0), max(clip.y0 - pad, top if direction == "up" else 0),
                     min(clip.x1 + pad, xb + pad, W), min(clip.y1 + pad, bottom if direction == "down" else H))
    return {"page": pno, "clip": clip, "direction": direction, "caption": cap_text,
            "debug": {"caption_rect": [round(v) for v in cap], "columns": [round(xa), round(xb)], "top": round(top),
                      "bottom": round(bottom), "n_above": len(above), "n_below": len(below)}}


def qe_export_crop(pdf_path, page_index, clip, base, dpi=400):
    """Write base.pdf (vector crop of one page region) and base.png. clip is [x0, y0, x1, y1] in PDF points.
    The PDF keeps the rest of the page hidden inside the file. Returns the two paths."""
    import fitz
    src = fitz.open(pdf_path)
    c = fitz.Rect(clip) & src[page_index].rect
    out = fitz.open()
    pg = out.new_page(width=c.width, height=c.height)
    pg.show_pdf_page(pg.rect, src, page_index, clip=c)
    out.save(base + ".pdf", garbage=4, deflate=True)
    z = min(dpi / 72, 6000 / max(c.width, c.height))
    pg.get_pixmap(matrix=fitz.Matrix(z, z), alpha=False).save(base + ".png")
    out.close()
    return base + ".pdf", base + ".png"


def qe_crop_asset(pdf_path, label, base, hint_page=None, clip=None, page=None, direction=None):
    """Locate and export one asset. With clip and page (1-based) given, nothing is detected: the stated
    region is exported (the per-item override). Returns a dict with status 'ok', 'manual' or 'not found'."""
    import fitz
    if clip is not None and page is not None:
        qe_export_crop(pdf_path, page - 1, clip, base)
        return {"status": "manual", "page": page, "clip": [round(v, 1) for v in clip], "base": base}
    doc = fitz.open(pdf_path)
    loc = qe_locate_float(doc, label, hint_page, direction)
    if loc is None or loc["clip"].height < 25 or loc["clip"].width < 40:
        return {"status": "not found", "base": base}
    qe_export_crop(pdf_path, loc["page"], loc["clip"], base)
    return {"status": "ok", "page": loc["page"] + 1, "clip": [round(v, 1) for v in loc["clip"]],
            "direction": loc["direction"], "caption": loc["caption"][:160], "base": base}


def qe_contact_sheet(items, out_jpg, cols=4, tile=(520, 430)):
    """One JPEG with a tile per crop, for visual review. items: list of (title, png_path)."""
    from PIL import Image, ImageDraw
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile[0], rows * tile[1]), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (title, png) in enumerate(items):
        x, y = (i % cols) * tile[0], (i // cols) * tile[1]
        draw.rectangle([x, y, x + tile[0] - 1, y + tile[1] - 1], outline=(180, 0, 0))
        draw.text((x + 6, y + 4), title[:80], fill=(0, 0, 160))
        if os.path.exists(png):
            im = Image.open(png).convert("RGB")
            im.thumbnail((tile[0] - 12, tile[1] - 30))
            sheet.paste(im, (x + 6, y + 22))
    sheet.save(out_jpg, quality=82)
    return out_jpg


def qe_page_grid(pdf_path, page, out_jpg, width=1000, clip=None):
    """Render one page (1-based) with a 50-point grid labelled in PDF points, to read off a manual clip."""
    import fitz
    from PIL import Image, ImageDraw
    pg = fitz.open(pdf_path)[page - 1]
    z = width / pg.rect.width
    pm = pg.get_pixmap(matrix=fitz.Matrix(z, z))
    im = Image.frombytes("RGB", (pm.width, pm.height), pm.samples)
    draw = ImageDraw.Draw(im)
    for x in range(0, int(pg.rect.width) + 1, 50):
        draw.line([(x * z, 0), (x * z, im.height)], fill=(255, 0, 0) if x % 100 == 0 else (255, 180, 180))
        if x % 100 == 0:
            draw.text((x * z + 2, 2), str(x), fill=(200, 0, 0))
    for y in range(0, int(pg.rect.height) + 1, 50):
        draw.line([(0, y * z), (im.width, y * z)], fill=(0, 0, 255) if y % 100 == 0 else (180, 180, 255))
        draw.text((2, y * z + 1), str(y), fill=(0, 0, 200))
    if clip is not None:
        draw.rectangle([clip[0] * z, clip[1] * z, clip[2] * z, clip[3] * z], outline=(0, 160, 0), width=3)
    im.save(out_jpg, quality=82)
    return out_jpg
