# Helpers for the qe-references skill. Loading this file only defines functions.
import csv
import difflib
import json
import os
import re
import time
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET


def qe_parse_bib(path):
    """Parse a .bib file into a list of dicts: key, type, and one item per field (lower-case names)."""
    text = open(path, encoding="utf8").read()
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,", text):
        if m.group(1).lower() in ("comment", "string", "preamble"):
            continue
        depth, i = 1, m.end()
        while i < len(text) and depth:
            depth += {"{": 1, "}": -1}.get(text[i], 0)
            i += 1
        body = text[m.end():i - 1]
        entry = {"key": m.group(2), "type": m.group(1).lower()}
        for f in re.finditer(r"(\w+)\s*=\s*", body):
            j = f.end()
            if j >= len(body):
                continue
            if body[j] == "{":
                d, k = 1, j + 1
                while k < len(body) and d:
                    d += {"{": 1, "}": -1}.get(body[k], 0)
                    k += 1
                val = body[j + 1:k - 1]
            elif body[j] == '"':
                k = body.find('"', j + 1)
                val = body[j + 1:k]
            else:
                val = re.match(r"[^,\n]*", body[j:]).group(0)
            name = f.group(1).lower()
            if name not in entry:
                entry[name] = re.sub(r"\s+", " ", val).strip()
        entries.append(entry)
    return entries


def qe_norm_title(title):
    """Lower-case, strip TeX braces, accents and punctuation: the form used to compare titles."""
    t = re.sub(r"\\[`'\"^~=.]\s*", "", title or "")
    t = re.sub(r"\\[a-zA-Z]+\s*|[{}$]", "", t)
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", t.lower()).strip()


def qe_arxiv_id(entry):
    """arXiv identifier of a bib entry (from eprint, url, journal or note), or ''."""
    blob = " ".join(entry.get(k, "") for k in ("eprint", "url", "journal", "note", "doi"))
    m = re.search(r"(\d{4}\.\d{4,5})(v\d+)?", blob)
    return m.group(1) if m and ("arxiv" in blob.lower() or entry.get("eprint")) else ""


def qe_dedupe(entries):
    """Groups of bib keys that are the same work (same DOI, same arXiv id, or same normalized title)."""
    seen, groups = {}, {}
    for e in entries:
        ids = [("doi", e.get("doi", "").lower()), ("arxiv", qe_arxiv_id(e)), ("title", qe_norm_title(e.get("title", "")))]
        hit = next((seen[i] for i in ids if i[1] and i in seen), None)
        root = hit or e["key"]
        groups.setdefault(root, []).append(e["key"])
        for i in ids:
            if i[1]:
                seen.setdefault(i, root)
    return [g for g in groups.values() if len(g) > 1]


def qe_fetch_json(url, timeout=25):
    with urllib.request.urlopen(url, timeout=timeout) as r:
        return json.loads(r.read().decode("utf8"))


def qe_first_family(author_field):
    first = re.split(r"\s+and\s+", author_field or "")[0]
    fam = first.split(",")[0] if "," in first else (first.split() or [""])[-1]
    return qe_norm_title(fam)


def qe_check_entry(entry, email=None):
    """Compare one bib entry with Crossref (by DOI) or arXiv (by id). Returns a dict with status:
    'verified', 'mismatch' (see detail) or 'human check' (nothing to compare against, or a venue
    that the arXiv record cannot confirm). Pass email only if host.get_user_email() returned one."""
    out = {"key": entry["key"], "source": "", "status": "human check", "detail": ""}
    title, fam, year = qe_norm_title(entry.get("title", "")), qe_first_family(entry.get("author", "")), entry.get("year", "")
    venue = entry.get("booktitle") or entry.get("journal") or ""
    problems = []
    try:
        if entry.get("doi"):
            url = "https://api.crossref.org/works/" + urllib.parse.quote(entry["doi"])
            if email:
                url += "?mailto=" + urllib.parse.quote(email)
            w = qe_fetch_json(url)["message"]
            out["source"] = "crossref"
            r_title = qe_norm_title(" ".join(w.get("title") or []))
            r_fam = qe_norm_title((w.get("author") or [{}])[0].get("family", ""))
            parts = (w.get("issued") or {}).get("date-parts") or [[None]]
            r_year = str(parts[0][0] or "")
            r_venue = " ".join(w.get("container-title") or [])
            if difflib.SequenceMatcher(None, title, r_title).ratio() < 0.9:
                problems.append("title: record has '%s'" % " ".join(w.get("title") or [])[:120])
            if fam and r_fam and difflib.SequenceMatcher(None, fam, r_fam).ratio() < 0.8:
                problems.append("first author: record has '%s'" % r_fam)
            if year and r_year and abs(int(year) - int(r_year)) > 1:
                problems.append("year: record has %s" % r_year)
            if venue and r_venue and difflib.SequenceMatcher(None, qe_norm_title(venue), qe_norm_title(r_venue)).ratio() < 0.5 \
                    and qe_norm_title(r_venue) not in qe_norm_title(venue) and qe_norm_title(venue) not in qe_norm_title(r_venue):
                problems.append("venue: record has '%s'" % r_venue[:100])
        elif qe_arxiv_id(entry):
            url = "http://export.arxiv.org/api/query?id_list=" + qe_arxiv_id(entry)
            with urllib.request.urlopen(url, timeout=25) as r:
                root = ET.fromstring(r.read())
            ns = {"a": "http://www.w3.org/2005/Atom", "x": "http://arxiv.org/schemas/atom"}
            e = root.find("a:entry", ns)
            out["source"] = "arxiv"
            if e is None or e.find("a:title", ns) is None:
                problems.append("arXiv id not found")
            else:
                r_title = qe_norm_title(e.find("a:title", ns).text)
                r_fam = qe_norm_title((e.find("a:author/a:name", ns).text or "").split()[-1])
                if difflib.SequenceMatcher(None, title, r_title).ratio() < 0.9:
                    problems.append("title: record has '%s'" % re.sub(r"\s+", " ", e.find("a:title", ns).text)[:120])
                if fam and r_fam and difflib.SequenceMatcher(None, fam, r_fam).ratio() < 0.8:
                    problems.append("first author: record has '%s'" % r_fam)
                jref = e.find("x:journal_ref", ns)
                if venue and "arxiv" not in venue.lower():
                    out["status"] = "human check"
                    out["detail"] = "venue '%s' cannot be confirmed from the arXiv record%s" % (
                        venue[:80], " (journal_ref: %s)" % jref.text if jref is not None else "")
                    if problems:
                        out["status"], out["detail"] = "mismatch", "; ".join(problems) + "; " + out["detail"]
                    return out
        else:
            out["detail"] = "no DOI and no arXiv id in the entry"
            return out
    except Exception as ex:  # network or record errors are reported, never guessed around
        out["detail"] = "lookup failed: %s" % str(ex)[:150]
        return out
    out["status"] = "mismatch" if problems else "verified"
    out["detail"] = "; ".join(problems)
    return out


def qe_check_metadata(bib_path, out_csv, keys=None, email=None, pause=0.3):
    """Run qe_check_entry over a .bib file (or over `keys` only) and write out_csv
    (key, source, status, detail). Returns counts per status."""
    rows = []
    for e in qe_parse_bib(bib_path):
        if keys is not None and e["key"] not in keys:
            continue
        rows.append(qe_check_entry(e, email=email))
        time.sleep(pause)
    with open(out_csv, "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=["key", "source", "status", "detail"])
        w.writeheader()
        w.writerows(rows)
    counts = {}
    for r in rows:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    return counts


def qe_open_checks(verification_csv, extra=None):
    """Text block of every item a human still has to check: rows of the verification CSV whose
    status is not 'verified' and whose 'cleared' column (if present) is empty, plus `extra` lines.
    Repeat this block at the end of every reply until it is empty."""
    lines = []
    with open(verification_csv, encoding="utf8") as f:
        for r in csv.DictReader(f):
            if r.get("status") != "verified" and not (r.get("cleared") or "").strip():
                lines.append("- %s: %s (%s)" % (r["key"], r.get("detail") or r.get("status"), r.get("status")))
    lines += ["- " + x for x in (extra or [])]
    return "Open checks (%d):\n%s" % (len(lines), "\n".join(lines)) if lines else "Open checks: none"


def qe_pdf_to_text(pdf_path, out_txt):
    """Write the text of a PDF with a '===== page N =====' line before each page (N is 1-based)."""
    import fitz
    doc = fitz.open(pdf_path)
    with open(out_txt, "w", encoding="utf8") as f:
        for i, page in enumerate(doc):
            f.write("===== page %d =====\n%s\n" % (i + 1, page.get_text()))
    return len(doc)


def qe_norm_quote(s):
    s = unicodedata.normalize("NFKC", s or "").replace("\ufffe", "").replace("\u00ad", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s).strip().lower()


def qe_match_quotes(claims_csv, text_dir, out_csv=None):
    """Check every quote of a claims table against the page text of its paper.
    claims_csv needs columns key, page, quote; text_dir holds <key>.txt files from qe_pdf_to_text.
    Adds quote_check: 'exact' (on the stated page), 'other page N', 'near (ratio)', 'not found',
    'no text file' or 'no quote'. Returns counts per result."""
    rows = list(csv.DictReader(open(claims_csv, encoding="utf8")))
    cache, counts = {}, {}
    for r in rows:
        key, quote = r.get("key", ""), qe_norm_quote(r.get("quote", ""))
        path = os.path.join(text_dir, key + ".txt")
        if not quote:
            res = "no quote"
        elif not os.path.exists(path):
            res = "no text file"
        else:
            if key not in cache:
                parts = re.split(r"===== page (\d+) =====\n", open(path, encoding="utf8").read())
                cache[key] = {int(parts[i]): qe_norm_quote(parts[i + 1]) for i in range(1, len(parts) - 1, 2)}
            pages = cache[key]
            try:
                stated = int(float(r.get("page") or 0))
            except ValueError:
                stated = 0
            if quote in pages.get(stated, ""):
                res = "exact"
            else:
                other = [p for p, t in pages.items() if quote in t]
                if other:
                    res = "other page %d" % other[0]
                else:
                    best = 0.0
                    for t in pages.values():
                        sm = difflib.SequenceMatcher(None, quote, t, autojunk=False)
                        blk = sm.find_longest_match(0, len(quote), 0, len(t))
                        best = max(best, blk.size / max(1, len(quote)))
                    res = "near (%.2f)" % best if best >= 0.6 else "not found"
        r["quote_check"] = res
        counts[res.split(" ")[0]] = counts.get(res.split(" ")[0], 0) + 1
    if out_csv:
        with open(out_csv, "w", newline="", encoding="utf8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
            w.writeheader()
            w.writerows(rows)
    return counts
