# Sub-agent tasks for the reference step

Each sub-agent starts with nothing but its task text. Put every requirement in the task, hand files over as artifact markers, and ask for a structured result. Fill the `<…>` parts; keep the rules as written.

## Discovery (one per main question, or per group of main questions of one sub-section)

```
You support a PhD qualifying-examination report on <field>. Below is one main question of its
question list with its sub-questions. Each sub-question will be answered by a few sentences of the report.
Find the references those sentences need.

Main question: <text>
Sub-questions (N = needs literature; the others are listed for context only):
  <sub_id> [N] <text>
  ...

Existing bibliography (reuse these keys before proposing anything new):
  <key> — <title> (<year>)
  ...

For every sub-question marked N:
- name the existing keys that answer it, if any;
- propose at most <2-3> new references, only where the existing ones do not answer it;
- for each new reference give a BibTeX entry whose title, authors, year and venue you verified at the
  source (publisher page, proceedings, arXiv listing), and say where you verified each field.
  Key = first author's surname + year + first content word of the title, lower case.
  Year and venue are those of the published version if there is one, otherwise arXiv.
- give one line on what the reference is expected to show for that sub-question.

Rules: never state a title, author, year, venue or claim from memory; write "not found" instead.
Do not download papers from mirrors or copies when the source is blocked; report them as not fetched.
List in `deviations` every sub-question you could not cover and why.
```

Output schema: `{"sub_questions": [{"sub_id", "existing_keys": [...], "new_keys": [...], "expectation": "..."}], "new_entries": [{"key", "bibtex", "verified_where", "arxiv_id", "doi"}], "not_found": [...]}`.

## Reader (one per paper; Sonnet-class)

```
Read the attached paper in full (all pages, appendix included) and judge what it says about each of
the sub-questions below. The text has a line "===== page N =====" before each page; N is the page
number to report.

Paper: <key> — <title>
Text: <artifact marker of <key>.txt>
Sub-questions that cite this paper:
  <sub_id> <text>
  ...

For each sub-question return:
- verdict: "supported" (the paper states what the sub-question needs), "partly" (it states part of it,
  or states it for a narrower case), or "cannot answer" (it does not say this);
- claim: one sentence in your own words of what the paper establishes;
- quote: at most 40 words copied exactly from the text, the sentence that decides the verdict;
- page: the page number of the quote;
- for "partly" and "cannot answer": what exactly is missing.

Also report: any field of this record that the paper's first page contradicts
(<the bib entry>), and any page you did not read.

Rules: a quote must be an exact substring of one page. If you cannot find a sentence to quote, the
verdict is not "supported". Do not use knowledge of the paper from outside the text.
```

Output schema: `{"key", "rows": [{"sub_id", "verdict", "claim", "quote", "page", "missing"}], "record_errors": [...], "pages_not_read": [...]}`.

## Re-check (one per finding or per paper with findings; Opus-class)

```
A first reader judged that the attached paper does not, or only partly, answer the sub-question below.
Decide independently whether that judgement is right.

Paper: <key> — <title>
Text: <artifact marker of <key>.txt>
Sub-question: <sub_id> <text>
First reader's finding: <verdict> — <missing>

Read the relevant sections and search the whole text before deciding. Return:
- decision: "confirmed" (the finding stands), "overturned" (the paper does answer the sub-question),
  or "immaterial" (the gap does not change how the reference may be used);
- quote and page that decide it (exact substring, at most 40 words);
- if confirmed: the smallest change that would make the citation correct — a narrower wording of the
  sub-question, a different reference from the list below, or dropping the citation.

Other references already cited under this sub-question: <keys>
```

Output schema: `{"sub_id", "key", "decision", "quote", "page", "fix"}`.
