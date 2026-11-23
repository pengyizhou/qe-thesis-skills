---
name: qe-slide-assets
description: "Build the slide-assets table for a QE report or thesis question list: choose, for each main question, the figures, tables and input/output samples from the reference PDFs that a supervisor needs to see, crop them from the PDFs as vector PDF plus PNG with their captions, review the crops, and write the CSV (with slide_use and file paths) that the qe-evidence-page skill reads. Use when the user says slide assets, 素材, 截图, 裁图, extract figures or tables from the references, says there are too many figures, asks which sub-questions need a figure and which can be said in a sentence, or wants the hand-off bundle for the evidence page."
---

# QE slide assets

The supervisor judges the writing plan from a page of evidence, not from the question list. This skill prepares the visual part of that evidence: which figure or table stands behind which main question, cropped from the reference PDFs and listed in one table. It does not build the page; `qe-evidence-page` does, from the files this skill leaves.

It is the last step before the hand-off. It needs a question list whose reference step is done (`qe-references`): sub-questions with `[refs: …]` tags, the reference notes, the claims table, the PDFs and their page-marked texts. Read `references/project-notes.md` for this user's folders and for what already exists.

## The table

One CSV, one row per asset, with these columns. `qe-evidence-page` reads them by name.

| Column | Content |
|---|---|
| `section`, `main_question` | Where the asset belongs, copied word for word from the question list. |
| `asset_type` | `architecture_figure`, `results_table`, `data_table`, `input_output_sample`, `taxonomy_figure`, `timeline`, or `own figure or table`. |
| `source` | `reference`, or `to be drawn` for a figure or table the user plans to make. |
| `ref`, `pdf_number`, `label`, `page` | BibTeX key, number of the PDF, the label as printed (`Figure 2`, `Table II`), and the 1-based page of the local PDF. |
| `caption` | First sentence of the printed caption. |
| `use_on_slide` | One line: what the asset shows for this question, or which sub-question it was found for. |
| `slide_use` | `show`, `backup`, `base for own …`, or `not needed` (see the triage). |
| `asset_pdf_path`, `asset_png_path` | Absolute paths of the crop; empty for rows without a file. |
| `asset_note` | Why there is no file, or what is unusual (two tables stacked, a manual clip, a proof copy). |

## Step 1 — Candidates

For each main question, collect candidates from the references cited under its sub-questions. The claims table says which paper answers what; the captions say what a figure shows. Find captions by searching the page-marked texts for lines that start with `Figure N`, `Fig. N`, `Table N`. Three to eight candidates per main question are enough; note for each which sub-question it serves. Add a `to be drawn` row for every figure or table the question list plans as the user's own (a timeline tree, a summary table of corpora, a comparison of architectures).

## Step 2 — Triage: what the supervisor must see

A long candidate list is a pool, not a slide plan. Mark each row:

- `show` — the supervisor needs to see it to judge the plan. Aim for about one per main question, and none where a sentence does the job.
- `backup` — kept as folded evidence under a sub-question.
- `base for own …` — a published figure or table the user's own version will be built from.
- `not needed` — a `to be drawn` placeholder that turned out unnecessary.

Content that is said in one or two sentences and gets no `show` asset:

1. definitions and motivation;
2. single systems in an evolution section — they are nodes of the timeline, each with a phrase;
3. a claim that rests on one number — give the number and the citation;
4. general methods that are background (keep one figure only for a method the thesis builds on);
5. metric definitions — one small table of the user's own;
6. details of single corpora — they go into the summary table.

Tell the user the count before and after the triage, list the main questions that end up with text only, and let the user move rows between `show` and `backup`.

## Step 3 — Crop

For each row with a reference, crop the float with its caption:

```python
r = qe_crop_asset(pdf_path, "Figure 2", base, hint_page=4)   # base = folder/NNN_key_Figure2 (no extension)
```

It writes `base.pdf` (a vector crop) and `base.png` (400 dpi) and returns the page, the clip, and `status` (`ok`, `manual`, `not found`). File names: `NNN_key_Label` with the label stripped of spaces and punctuation. Write each file once.

The automatic crop is a first guess. In testing, on 207 hand-reviewed crops, it agreed with the reviewed crop within 10 points in 137 cases, within 25 points in a further 24, was clearly wrong in 40 and found nothing in 6. Expect to correct about one crop in four.

Labels the function does not handle and that need a manual clip from the start: two floats under one label (`Tables 2-3`), a part of a figure (`Figure 1 (panel c)` returns the whole figure), and text that is not a float (a prompt in an appendix).

## Step 4 — Review every crop

1. Build contact sheets of twelve crops with `qe_contact_sheet(items, out_jpg)` and look at every sheet. Typical faults: a running header or a section heading inside the crop; a neighbouring table or the title block included; rows of a table cut off; the caption cut short; the wrong side of the caption taken.
2. For each faulty crop, render the page with `qe_page_grid(pdf_path, page, out_jpg)`, read the rectangle off the 50-point grid, and export it with `qe_crop_asset(pdf_path, label, base, clip=[x0, y0, x1, y1], page=N)`. Trying `direction="up"` or `"down"`, or another `max_gap` in `qe_locate_float`, is quicker when only the side or the extent is wrong.
3. Look at the corrected crops again. A crop that was not viewed is not finished; say in the report how many were viewed and how many were corrected by hand.

## Step 5 — Write the paths and hand off

- Fill `asset_pdf_path`, `asset_png_path` and `asset_note` for every row; rows that share a reference and label share a file. A row whose PDF is not on disk gets the reason in `asset_note` and goes to the open checks of `qe-references`.
- Note in `asset_note` when the local PDF is a preprint or a proof and the asset carries numbers.
- The bundle for `qe-evidence-page` is: the question list with its tags, this CSV, the crops, the reference notes, and the reference PDFs. Check that every `main_question` in the CSV still matches the question list word for word; a question that was reworded since is reported, not silently re-mapped.

## Working with the page afterwards

- The published page cannot be read from its link or from a browser's "save page as" copy. To review it, ask for screenshots, a PDF print, or the page's source.
- When the user wants the page changed, write a prompt for the agent that maintains it: name the cards in scope, give the exact wording of questions, say which file goes where, use only text that was checked against the sources, mark anything unchecked `[TBD: source needed]`, and ask for a list of what was changed.

## Helpers loaded with this skill

`qe_crop_asset`, `qe_locate_float`, `qe_find_caption`, `qe_table_caption_side`, `qe_export_crop`, `qe_contact_sheet`, `qe_page_grid` (and `qe_label_pattern`, `qe_page_lines`, `qe_float_sides` they use). They need PyMuPDF (`pymupdf`) and Pillow in the environment. Coordinates are PDF points; pages are 1-based in every argument a caller passes.

## Files

- `references/project-notes.md` — this user's folders, the existing assets table and crops, and what is still missing.
