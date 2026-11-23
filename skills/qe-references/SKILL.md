---
name: qe-references
description: "Reference step for a QE report or thesis question list, run after the user has finalized Pass B: find references per main question with sub-agents, de-duplicate them, check the metadata with scripts, read every paper in full against the sub-questions (a Sonnet-class reader first, an Opus-class re-check when the reader reports that a paper cannot answer), match every quote against the PDF text, and produce the bibliography, the per-reference notes and the claims table that the question list and the evidence page rely on. Use when the user says 找 reference, 文献, reference check, full-text check, 复核, 核对引用, asks to add a reference or a sub-question after the reference step, asks whether a drafted answer is supported by its sources, or asks what is still unverified in the bibliography."
---

# QE references

A question list says what every sentence or two of the report has to answer. This skill finds out which of those answers the literature supports, and leaves a record precise enough that nobody has to trust memory: for every sub-question that needs literature, which paper answers it, in which words, on which page.

It is the third step of the user's workflow, between `qe-question-list` (the passes) and `qe-slide-assets` / `qe-evidence-page` (what the supervisor sees). Read `references/project-notes.md` first: it holds this user's folder, naming and numbering conventions and the state of the collection.

## Before starting

- **Pass B must be final for the chapters in scope, and the user is the one who says so.** If it is not, say which chapter is missing and stop. References found for coarse or moving questions do not line up with the sentences later, and the search has to be redone.
- The units of all work below are the sub-questions. Give each a stable ID in order of appearance (`B001`, `B002`, …) and keep one row per sub-question in a working table for the whole step.

## What this step produces

| File | Content |
|---|---|
| bibliography (`.bib`) | One entry per work. Key: first author's surname + year + first content word of the title, lower case. New entries are appended; existing numbers and keys never change. |
| verification table (`.csv`) | `key, source, status, detail, cleared` from the metadata check. |
| claims table (`.csv`) | One row per sub-question and reference: `sub_id, main_question, sub_question, key, verdict, claim, quote, page, reader, recheck, quote_check`. |
| reference notes (`.md`) | Per reference: the citation, a DOI or arXiv link, what was read (full text, pages, or abstract only), three to six sentences on what the paper establishes for the questions that cite it, and its caveats. `qe-evidence-page` treats these notes as its trusted source of facts. |
| tags in the question list | On each sub-question: `[refs: key, key]`, `[refs: none — own work]` or `[refs: none — structural]`; where needed `[check: caveat]`, `[check: own framing]`, `[no references yet: …]`. |
| PDFs and page-marked texts | One PDF per reference in the reference folder, and one text file per key with a `===== page N =====` line before each page. |

## Step 1 — Sort the sub-questions

Put every sub-question into one of three kinds: it needs literature; it is answered by the user's own work (papers, experiments); it needs no reference (structure, the report's own definitions). Only the first kind goes on. Tags that already sit on lines from an earlier survey are a pool: re-sort them onto the sub-questions they support before searching for anything new.

## Step 2 — Discovery, clustered by main question

- **One sub-agent per main question.** It sees that main question and all of its sub-questions, with the ones that need literature marked. Main questions of the same sub-section may share one sub-agent when they draw on the same literature; say which ones were grouped.
- Every sub-agent also gets the current bibliography (keys and titles) and must reuse an existing entry before proposing a new one. Cap what it may add (two or three new references per sub-question is usually enough) and ask for the record to be verified at its source, not recalled.
- Task text and output schema: `references/subagent-tasks.md`, "Discovery". Sub-agents run under the general agent profile. They may stop on a network-approval card that only the user can answer; tell the user when that happens.
- Afterwards merge the results, run `qe_dedupe` on the merged entries, keep the earlier key of each duplicate group, and report: how many sub-questions are covered by existing entries, how many new entries, how many still have nothing.

## Step 3 — Metadata check, and the human checks

- Run `qe_check_metadata(bib_path, out_csv)`. It compares title, first author, year and venue with Crossref (entries with a DOI) or with arXiv (entries with an arXiv id). Statuses: `verified`; `mismatch` (the detail names the field); `human check` (no DOI or arXiv id, or a venue that an arXiv record cannot confirm).
- Fix a mismatch from the record, never from memory, and run the check again on those keys.
- What the script cannot check stays with a human: venues of papers that exist only on arXiv, entries without identifiers, page ranges, and whether a local PDF is the published version or a preprint or proof.
- **Every item a human still has to check is repeated to the user at the end of every reply until the user clears it.** Build the block with `qe_open_checks(verification_csv, extra=[...])`; `extra` carries items that are not metadata (a PDF that is missing, a paper read from its abstract only, a reference that had a single read). When the user clears an item, write the date and how it was cleared into the `cleared` column. Never clear an item yourself.
- Crossref takes an optional contact address. Pass `email=` only with the address returned by `host.get_user_email()`; if that call fails, leave it out.

## Step 4 — Full texts

- Fetch each PDF from its open source (arXiv, the publisher's open copy, `fetch_article_fulltext`). If a host is blocked or the paper is behind a paywall, do not look for mirrors or other copies: add the paper to the missing-texts list, ask the user to download it into the reference folder, and keep it in the open checks.
- Save each PDF once, under the naming of `references/project-notes.md`. Then write its text with `qe_pdf_to_text(pdf, "<texts>/<key>.txt")`.
- A reference whose full text was never read is marked "abstract only" in its note and stays in the open checks.

## Step 5 — Reading in two tiers, then the quote check

1. **Reader, Sonnet-class, one sub-agent per paper.** It gets the page-marked text and the sub-questions that cite the paper, reads the whole paper, and returns for each sub-question a verdict (`supported`, `partly`, `cannot answer`), the claim in one sentence of its own, a verbatim quote of at most 40 words and its page. It also reports errors in the bibliographic record and any pages it did not read. Task text: `references/subagent-tasks.md`, "Reader".
2. **Re-check, Opus-class, only where the reader says a paper cannot answer or answers partly.** An independent sub-agent gets the sub-question, the reader's finding and the same text, and confirms or overturns the finding with its own quote. Only confirmed findings are applied. Task text: "Re-check".
3. **Quote check, by script, on every row.** Run `qe_match_quotes(claims_csv, texts_dir, out_csv)`. A `supported` row passes only if its quote is `exact` on the stated page. `other page N`: correct the page. `not found`: the reader supplies the quote again; if it is still not found, the row counts as `cannot answer` and goes to the re-check. This is the guard against a wrong "supported", which the re-check alone never sees.

Resolve model ids at run time (`host.list_models()`); never write a model id into a task or a file. Record in the reading log which tier read which paper, and what was not read.

## Step 6 — Consolidate with the user

- Write the tags onto the sub-questions. All citing rows supported: `[refs: …]` only. A paper supports part of the premise: `[check: caveat]`, with what is and is not supported in the claims table. The facts are supported but the comparison or framing is the thesis's own: `[check: own framing]`. Nothing found: `[no references yet: …]`.
- Labels and scope statements are checked here against the papers' own wording: the name of a family of methods, what a system is said to lack, why the thesis follows one line of work. A label the papers do not support is a finding like any other.
- **Show the user every sub-question whose premise the reading did not support, each with the smallest fix**: reword, split, mark as own framing, or drop. These findings change Pass B, so the user decides each one; apply nothing without that decision, and keep the undecided ones in the open checks.
- Update the reference notes and the claims table, and report the totals. The question list, the claims table, the notes and the PDFs are then ready for `qe-slide-assets` and `qe-evidence-page`.

## Later additions and answer checks

- **A sub-question or a reference added after this step** goes through the same steps on a small scale: one discovery sub-agent for its main question, the metadata check for the new keys, the two-tier reading and the quote check. If the user asks for a single read instead, do that, and list the entry in the open checks as "single read".
- **The user drafts the answer to a sub-question.** Check it clause by clause against the page-marked texts of the cited papers. Report each clause as supported, attributed differently in the source, or not found, with pages; propose the smallest rewording; and record on the sub-question that it was checked, with the date and the pages.
- A claim made in a contribution chapter is judged against the work that existed when its paper was written. Later and concurrent work is acknowledged, never used to call the claim wrong.

## Helpers loaded with this skill

`qe_parse_bib`, `qe_dedupe`, `qe_check_entry`, `qe_check_metadata`, `qe_open_checks`, `qe_pdf_to_text`, `qe_match_quotes` (and the small `qe_norm_title`, `qe_arxiv_id`, `qe_norm_quote` they use). `qe_pdf_to_text` needs PyMuPDF; install `pymupdf` in the environment if the import fails. Each function's docstring states its inputs and outputs.

## Files

- `references/subagent-tasks.md` — task texts and output schemas for the discovery, reader and re-check sub-agents.
- `references/project-notes.md` — this user's reference folder, file naming, numbering, model choice, and the state of the collection. Update it, with the user's agreement, when a convention changes.
