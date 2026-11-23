---
name: "qe-evidence-page"
description: "Build or revise the supervisor-facing evidence page for a thesis or QE question list: one card per main question, evidence folded under each Pass B sub-question, thesis-ready conclusion sentences, own timelines and tables, per-card references. Use whenever the user wants to visualize a question list, slide assets or literature evidence for their supervisor, asks to add, move, check or re-split evidence on such a page, or says things like 证据页, 给老板看的页面, More evidence, Pass B 对不上. On first use it asks for the files it needs before building anything."
---

# QE evidence page

Turn a chapter-by-chapter question list and its collected figures into a page a supervisor can read: for every main question, what evidence exists and what it lets the student conclude. The page is a review tool for the question list, not the thesis and not a slide deck.

Reply to the user in their language (usually Simplified Chinese). Everything on the page is US English academic prose.

## First use: ask for the files before building

The page is only as good as its sources, and a page built on guessed inputs has to be rebuilt. So before any layout, figure or sentence, find out whether this is a first use or a continuation.

**It is a continuation** when a `page_build/` folder (build script and maps) or an existing evidence page is found in the user's connected folders, their artifacts, or earlier in the conversation. Then skip the intake, load that build, and ask only for whatever the current request needs that is not there.

**It is a first use** when neither is found. Look once through the attachments and connected folders for the files below, then send the user ONE message, in their language, that lists what was found (by file name, so they can confirm it is the right version) and asks for what is missing. Do not start building in the same turn, and do not ask file by file across several turns.

Required; without all three there is nothing to build:

1. **The question list** (markdown), with main questions and Pass B sub-questions. If there are several versions, ask which one is current.
2. **The evidence assets**: the slide-assets CSV and the folder of cropped figures and tables it points to.
3. **The reference notes** (markdown): one note per reference written from the full text, with DOI or arXiv link.

Needed for full quality; say what is lost without each one and go on if the user does not have it:

4. **The reference PDFs.** Without them, numbers cannot be checked and new crops cannot be made, so conclusions stay qualitative wherever the notes give no number.
5. **A folder to save the build into** (scripts, maps, figures, new crops). Without it the work cannot be continued in a later conversation.

Ask in the same message, since the answers change what gets built:

- Which chapters or sections this page should cover.
- Who will read it and how it will be shared (a link for the supervisor, a meeting walkthrough).
- Any figures of their own (their papers, earlier slides) that should appear as evidence.

If the files live on the user's computer and no folder is connected, say how to provide them: attach them here, or connect the folder that holds them. A whole folder of PDFs and crops is better connected than attached.

When the files arrive, check them before building and report in a few lines: number of main questions and sub-questions, number of CSV rows, how many crop files the CSV points to that exist, how many reference keys in the question list have a note and a PDF, and any main question in the CSV that does not match the question list. Fix nothing silently; a mismatch here usually means an old version of one of the files.

## What each input looks like

- **Question list** (markdown). A bold line is a main question (Pass A); indented lines under it are sub-questions (Pass B). Sub-questions carry `[refs: bibkey, ...]`, or `[refs: none - own work]` / `[refs: none - structural]`. Its Terms and Pass notes hold the user's decisions: read them before proposing structure changes.
- **Slide-assets CSV**: one row per figure or table, with section, main question, reference key, label (Figure 2, Table 1), caption, a short note on use, `slide_use` (`show` = main figure, `backup` = folded evidence), and the path of the cropped image. Rows marked as own figures have no reference.
- **Reference notes** (markdown): per reference, a note written after reading the full text, plus DOI or arXiv link. Treat these notes as the trusted source of facts.
- **Reference PDFs and crops** in the user's folder.
- **An existing build**: if a `page_build/` folder exists (build script, keyword and conclusion maps, extras, fixes, sub-question maps) and a `figures/` folder with a figure generator, continue from them. Do not rebuild from scratch.

## What the page shows

One page (artboard) per section; split a section when it gets long. Each page has a section nav and an "Expand all evidence" control at the top.

Each main question is a card, numbered Chapter-Index exactly as in the question list (1-1, 2-6). A card contains, in order:

1. **Main figures**: the `show` rows and the student's own figures, each with a highlighted keyword and one or two sentences.
2. **More evidence**, split by Pass B sub-question. The sub-question is a small red heading, in question-list order, and the folded items that answer it sit under it. When a card has more than about twelve items, make each sub-question a collapsible group with an item count. Sub-questions with nothing to show are left out; a sub-question answered by the student's own framing can carry a short note instead of items when the user supplies the text.
3. **References** for that card only; the exact form is under "References and links" below.

A folded item is: highlighted keyword, source label (Figure 3, Table 2, or Text), citation number, the cropped figure, and one conclusion.

## Rules the user set

These came from repeated corrections; the reason is given so they can be applied to new cases.

- **Evidence only.** Never show gaps, counts of missing items, to-dos, or bookkeeping ("PDF not saved", author-order notes, "Own figure; years are...", "from memory"). The supervisor is judging the argument, and such notes read as unfinished work. Put caveats in the chat reply instead.
- **Own figures are evidence, already drawn.** Do not ask the supervisor whether to draw something. Draw it and present it.
- **Conclusions, not captions.** The sentence in a fold is what the student could paste into the thesis: a claim that stands without the figure, answers the sub-question it sits under, and never says "the figure shows". One or two sentences, no em dashes.
- **No invented facts.** Numbers come from the full-text notes or from a table you actually looked at or text you searched in the PDF. Where neither gives a number, write a qualitative conclusion. Say in the reply which sentences rest on memory or on a caption alone.
- **Emphasis must look like emphasis**: keywords are bold with a highlight, not plain bold.
- **Crop the paper's own caption** ("Figure 3: ...") out of every screenshot.
- **Lower the density.** Replace lists of text with a timeline, a table, or a small interactive element. Group long evidence lists and fold them.
- **Each item belongs where it answers the question.** Check for: figures that only repeat a later section; the student's own paper filed under "previous work"; technical detail sitting under an overview question. Remove duplicates across cards unless a sub-question needs the figure again, and then give it a different sentence.
- **Do not embed or redistribute the PDFs.** Link to the publisher or arXiv page.
- **Follow an edit brief literally.** When the user sends a list of changes with wording, use that wording, add no facts, touch nothing else, and end with a list of what changed and what deviates from the brief.
- **Sharing.** The page starts private. When the user is ready to send it, remind them to share it with the reader first, and that the reader can comment on the page directly.

## Visual conventions

The user settled these one correction at a time. Keep them the same on every page so that a colour always means the same thing; a new colour needs a new meaning.

| Element | Convention |
|---|---|
| Page | Background #FAFAFB, white cards with a 1px #E3E6EB border and 14px radius; text #16181D, secondary text #545B67 |
| Type | Inter for body, Space Grotesk bold for page title, section headings and question titles |
| Question number | White on blue #1D4ED8, a small rounded tag left of the question title |
| Keyword emphasis | Bold on a yellow highlight #FDE68A. Plain bold is not enough; the user could not tell it from body text |
| Pass B sub-question | Dark red #B91C1C, small and semibold. Red is reserved for sub-questions and used for nothing else |
| Links and reference numbers | Blue #1D4ED8, underlined |
| Fold groups | Light grey #F6F7F9 with the same border; the summary line shows the sub-question and an item count |

- **Click to enlarge.** Every image enlarges to full card width on click and shrinks on a second click; small crops are unreadable otherwise.
- **Expand all evidence** at the top of each page opens every fold on that page.
- **Sub-question order** follows the question list. Reordering or rewording a sub-question on the page is a proposal: say so and keep the page in step with the question list once the user decides.
- **One term, one wording.** When the user renames a concept ("no tokenizer" became "no vector quantization"), change it everywhere on the page, in own figures and tables as well, then search the built pages and confirm it is gone. A paper's own title keeps its wording.
- **Placeholders.** Where the user said to wait for their source, the page shows "[TBD: source needed]" and nothing invented in its place. Remove the marker when the text arrives.
- **Opening view.** Set the canvas to open on the first chapter's page, not on the overview of all artboards.

## References and links

- **Per card.** Each card has its own list, numbered in order of first use on that card. Adding an item in the middle renumbers the later entries of that card; mention this in the report so the user is not surprised.
- **Entry form**: authors (first author "et al."), year, title, venue, then a "Cited by" line with the keywords of the items that cite it. A reference that only appears inside an own table or a note is listed too, cited by that table or note.
- **Venue.** Give the published venue when there is one, even if the PDF on file is the arXiv copy. For a preprint or technical report the venue is the identifier, written "arXiv:2509.24650".
- **Jump to the paper.** The reference number, both in the list and beside each item, links to the DOI page, or to the arXiv abstract page when there is no DOI, and opens in a new window. Link to the landing page, never to a PDF file, and never embed the PDF: the page is shared, and the papers are not the user's to redistribute.
- **Item source line**: label and citation number, for example "Table 3 · [22]"; "Text" when the item has no figure.
- **New references the user supplies** go into the build's reference file with exactly the details given. If only "Zhou et al." was given, write that and offer to complete the names from the PDF.

## Own figures

The own figures are for reading on the page. The user does not consider them thesis-ready, so do not present them as final thesis figures; keep the content (the categories, the flow, which system belongs where) easy to redraw in another style.

Generate them as SVG from a script and rasterize; keep the script so figures can be regenerated.

- **Colours inside figures**: slate text (#0F172A titles, #64748B secondary) on white; one colour per line of work or per route, used the same way in every figure. No colour carries meaning on its own: each coloured group also has a text label.
- **Tables**: a title and one-line subtitle, a pale header row, the first column bold with the citation in small grey under it, short cells, thin row rules. If a first-column name wraps, both lines stay bold.
- **A table per comparison question.** When a card compares several corpora, benchmarks or systems, put one own table at the top of the card (name, language, size, categories, how it was built or scored) and keep the folds for the detail.

- **Timeline**: survey style. A curved axis through the middle (time is not linear), year markers on it, works above and below with name and releasing group, colour by line of work, optional era brackets. Use the year of first public release and verify it against the paper where possible. Split crowded recent years into halves rather than stacking more than two items per side.
- **Comparison table**: families or systems as rows, a few short columns.
- **Structure comparison**: side-by-side blocks with the systems that use each design named on the figure.
- **Pipelines**: straight left to right, no bends.
- Do not fetch or draw company logos; show the organization as text.
- One figure can serve two adjacent questions: show it once and add a one-line pointer on the other card.

## Workflow

1. **Run the first-use intake** above if no build exists yet; otherwise load the existing build. Then map every CSV row to its main question and report mismatches between the CSV and the current question list.
2. **Agree on the layout** in a short description before building, if no page exists yet.
3. **Draw the own figures** first and show them; then build the page.
4. **Write conclusions** card by card from the full-text notes. View the crop when a sentence depends on what a table says.
5. **Assign each folded item to a sub-question**, then run the strict coverage check below.
6. **Publish**, then report: what changed, what was checked against a PDF, what rests on memory, and anything that could not be made to fit.

### Strict coverage check

A reference appearing under a question does not mean the question is answered. For every sub-question that needs literature, judge whether a conclusion on the page directly answers it: yes, partly, or no. For large lists, give independent subagents one group of questions each, with the sub-questions, the items and their sentences, and the reference notes, and have them return a verdict and one fix per gap. Fixes, cheapest first:

- reword the sentence of an item already under the question;
- reuse a figure shown elsewhere on the page, with a new sentence;
- add a text-only item citing one reference;
- crop a new figure from the PDF.

Also collect items that answer nothing under their question and move or drop them. Tell the user when a sub-question's premise is not supported by the notes, rather than writing around it.

## Page-only changes

The CSV and the question list belong to the user. Record removals, moves, added items, reworded sentences, sub-question assignments and display order in the build's own maps, and say so. Offer to write changes back to the question list only when the user asks; reordering or rewording sub-questions on the page is a proposal until then.

## Building and publishing

- Build the page as a Design-type canvas artifact when that type is available: one artboard per section page, images uploaded as assets, pages regenerated by the build script and published as a patch. Read the type's own instructions before the first edit.
- Folding, click-to-enlarge and expand-all can be done with plain HTML and CSS (details elements, a hidden checkbox with `:has`), which avoids scripting inside the artboard.
- Before publishing, check the live version. If it changed since the last publish, compare before overwriting, and edit shared index files from the live copy.
- Do not render or screenshot the result unless the user asks; say that it was not visually checked and what to look at.
- Save the build scripts, maps, new crops and figures back to the user's folder after each round so the work can continue in a new conversation.