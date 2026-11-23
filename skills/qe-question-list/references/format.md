# Question list format

The working file is one Markdown file, `question-list.md`, holding every chapter at both resolutions. Each pass of each stage replaces its own chapter block and leaves the others alone.

## File skeleton

```markdown
# <Thesis title> — Question List

## Terms
- paralinguistic information: <the definition fixed in Stage 0/1>
- Task 1: <one-line name>  (chapter 3)
- Task 2: <one-line name>  (chapter 4)
- <method names, key metrics, representation names>

## Stage status
| Stage | Chapter | Pass A (abstract) | Pass B (detailed) |
|---|---|---|---|
| 0 | Abstract | approved | done |
| 1 | Introduction | approved | — |
| 2 | Literature Review | drafted, awaiting approval | — |
| 3 | Task 1 chapter | — | — |
| 4 | Task 2 chapter | — | — |
| 5 | Conclusion and Future Work (optional) | — | — |

---
## 0. Abstract (1 pg)
...

---
# 1. Introduction (4.5 pg)
...
```

Pass A status is one of `—`, `drafted, awaiting approval`, `approved`. Pass B is `—`, `partial (§x.y–§x.z)`, or `done`. Pass B is never started on a chapter whose Pass A is not `approved`.

## Chapter block format

- Chapter title line carries the total page budget: `# 3. <Title> (16.5 pg)`.
- Each section heading carries its own budget: `## 3.3 Proposed <Method> Framework (5 pg)`.
- A `### Chapter opening (0.5 pg)` line sits under every chapter title, unless the chapter structure fixed with the user folds the opening into the first question of its first section.
- In a section longer than about four pages, group the abstract questions under `###` sub-section headings (`### 2.3.2 Data sources and annotation`). Headings are not questions; a question that only names the sub-section's topic belongs in the heading, not in the list.
- Questions are nested bullets with a fixed meaning per depth:
  - **Depth 1 = main (abstract) question, Pass A — written in bold:** `- **How is speech represented for the LLM?**`. One argumentative move, in one short clause. After Pass A the chapter block contains only bold depth-1 bullets.
  - **Depth 2 = sub-question (detailed question), Pass B — indented under its main question, not bold.** One to two sentences of the report. Added under its parent in Pass B, in the order the sentences will appear. The second half of a compound question ("…, and why …?"), parenthetical examples and enumerations belong here, not in the main question.
  - Depth 3 only when a detailed question has an internal enumeration that the report will list item by item (e.g. three calibration paths, four datasets).
- The abstract (Stage 0) is one page, so its abstract questions are fewer and its detailed questions map to single sentences; the same two depths apply.
- Every question ends with `?`. If something must be *stated* rather than argued (a definition, a fact), phrase it as a sub-question under the main question it serves ("What does <term> mean here, and why is that the right scope?"). The user's own first sub-lines may be short notes on the answer ("SSL-based, TDNN, etc."); keep them as they are in the user's draft, and when Pass B is completed turn each into a question, with the note kept in brackets if it helps.
- `Starter:` (or `Starter/background:`) in front of a main question marks the opening question of a section; `Connector:` in front of a sub-question marks the lead-in to the next part. They replace chapter-style bridges; a literature-review section has no closing question.
- Unresolved items: `- How does the retrieval mechanism select candidates? [TBD: user has not decided between similarity threshold and top-k]`
- Abstract questions carried over from an earlier chapter (abstract ↔ contributions ↔ task chapter intro) are marked with `↔ §x.y` at the end so the mirroring is visible and easy to check. Mirroring is tracked at depth 1; detailed questions are not expected to repeat across chapters, because each chapter answers the shared question at a different depth.
- A figure the user plans for a section is recorded on its heading: `### 2.3.1 Evolution  [figure planned by the user: timeline tree of TTS systems]`. The questions under the heading explain the figure. Figures are not counted in the page budget.
- References are attached only after the user has finalized Pass B, by the `qe-references` skill, which defines the tags (`[refs: key1, key2]`, `[refs: none — own work]`, `[refs: none — structural]`, `[check: caveat]`, `[check: own framing]`). Do not write or edit them here. Tags that an earlier survey left on a main question stay where they are until then. Keep these tags word for word when the question is moved, and add `(was <old ID>)` when its position changes, so that it can still be matched to the reference list.
- A change proposed by the coach that the user has not yet confirmed is tagged on the line: `[reworded … — confirm]`, `[new … — confirm; references to be attached]`. Remove the tag when the user confirms; wording that comes from the user's own edited copy needs no tag. `[TBD: premise to be checked at the reference step]` marks a question whose premise about the literature has not been checked; it is not checked while Pass A or Pass B is being written. A sub-question added by the coach in Pass B is tagged `[Pass B, added by the coach — confirm]` until the user approves it.
- Tags may sit on a main question or on a sub-question: when an earlier main question becomes a sub-question, its `[refs: …]`, `[check: …]` and `(was X)` move with it.
- A literature-review section has no `(closing)` question by default (see `chapter-probes.md`, Stage 2).

## Questions-only export

When the user asks for a clean version, write a separate file (`question-list_vN.md`) with the requested chapters: headings with page budgets, main questions in bold, sub-questions indented, and planned figures or tables in the heading as `(includes a timeline tree)`. Strip `[refs: …]`, `[check: …]`, confirm tags, `(was X)`, `↔` marks and `[TBD]`s. The export is for the user to read and edit by hand; the working file keeps the tags. A second kind of export holds Pass A only: the headings with their page budgets (with an estimate per sub-section when the user asks for one) and the bold main questions, without sub-questions. It is what the user takes to the supervisor before Pass B. When the user sends an edited copy back, compare it with the working file line by line, sync the working file to the user's wording and structure, re-attach the tags to the lines that carry the earlier questions, and report what changed.

## Granularity guide

A planning guide, not a quota. A density of main questions or a grain of sub-questions that the user has set takes precedence over the table below. It assumes roughly 500 words, or about 20 sentences, per page; rescale if the user's template is denser or sparser. The budgets are text pages: figures and tables are not counted. If the user's page limit includes floats, estimate them per section (a task chapter built on a paper usually inherits all of that paper's figures and tables) and subtract them before reading the table.

| Section budget | Abstract questions (Pass A) | Detailed questions (Pass B) |
|---|---|---|
| 0.5 pg | 1–2 | 4–8 |
| 1 pg | 2–4 | 8–15 |
| 2 pg | 4–7 | 16–30 |
| 4 pg | 8–12 | 35–60 |
| 5 pg | 10–15 | 45–75 |

Reading the table: an abstract question covers about a paragraph (sometimes two short ones); a detailed question covers one to two sentences; so each abstract question has about three to six children. Signs the granularity is off:

- An abstract question that one sentence would answer → it is a detailed question; find its parent.
- An abstract question with one child, or with more than about eight → merge it, or split it into two moves.
- A detailed question that needs a whole paragraph → it is an abstract question; promote it and expand it.
- A Pass A list as long as the Pass B guide for that budget → Pass A has been written at sentence level; collapse it.

## Worked example (one task chapter)

The chapter below is fictional; it shows the format, not a real thesis.

### After Pass A — main questions only (bold)

```markdown
# 3. Site-Robust Bird Sound Classification via Habitat-Aware Background Modelling (16.5 pg)

### Chapter opening (0.5 pg)
- **What does this chapter do, and which challenge from §1.2 does it answer?**  ↔ §1.2 Task 1

## 3.1 Introduction (1.5 pg)
- **Why is site-robust bird sound classification important, and why do models trained on curated recordings fail in the field?**
- **Where do existing ways of handling recording conditions leave the problem open?**
- **What is the main research objective of this chapter?**  ↔ §1.2 Task 1
- **What does the chapter propose, and what does it claim to show?**  ↔ §0, §1.3

## 3.2 Background (4 pg)
- **How do data-augmentation methods simulate field conditions, and which conditions do they miss?**
- **How do domain-adaptation methods align curated and field recordings, and why do they need unlabelled recordings from every site?**
- **How do noise-reduction front ends clean the input, and why do they remove faint calls with the noise?**
- **What limitations do existing approaches share when the habitat changes?**

## 3.3 Proposed HABM Framework (5 pg)
- **What is the overall architecture of HABM, and how do background modelling and classification fit into one framework?**
- **How is the habitat background bank built?**
- **How does background matching find the closest habitat for a new recording?**
- **How does background-conditioned classification separate the call from the matched background?**

## 3.4 Experimental Setup (2 pg)
- **Which datasets and metrics are used, and why do they test robustness to a change of site?**
- **Which baselines and evaluation settings (unseen sites, few-shot adaptation) are compared, and how is the model trained?**

## 3.5 Results and Discussion (3 pg)
- **How does HABM perform compared with existing approaches?**  ↔ §0, §1.3
- **How does each proposed component contribute?**
- **How well does HABM generalize across sites and model architectures?**
```

The user approves (or edits) this list before anything below is written.

### After Pass B — the same block with §3.1 and §3.5 expanded

```markdown
## 3.1 Introduction (1.5 pg)
- **Why is site-robust bird sound classification important, and why do models trained on curated recordings fail in the field?**
  - Where are bird sound classifiers deployed such that they must work at sites they were never trained on?
  - How do wind, insects, water and other species change what a call sounds like in a field recording?
  - What does a model get wrong when it reads a habitat's background as part of the call?
  - Why are models trained on curated recordings therefore unreliable in the field?
- **Where do existing ways of handling recording conditions leave the problem open?**
  - What do augmentation, domain adaptation and noise reduction each assume about the field?
  - Which of those assumptions fails at a new site with no labelled recordings?
  - What property would a method need in order to avoid that failure?
- **What is the main research objective of this chapter?**  ↔ §1.2 Task 1
  - How can a call be separated from the habitat background it was recorded in?
  - How can a classifier stay accurate at unseen sites without per-site labels?
- **What does the chapter propose, and what does it claim to show?**  ↔ §0, §1.3
  - What is HABM in one sentence?
  - What are its two components, and what does each contribute?
  - Which claims does the chapter make, each to be supported in §3.5?
  - How is the rest of the chapter organized?

## 3.5 Results and Discussion (3 pg)
- **How does HABM perform compared with existing approaches?**  ↔ §0, §1.3
  - Which table reports the main comparison, and on which datasets and metrics?
  - What improvement is achieved at unseen sites, and against which strongest baseline?
  - What improvement is achieved with few-shot adaptation?
  - What do these two results together say about the Task 1 question?
- **How does each proposed component contribute?**
  - How do matched habitat backgrounds compare with random backgrounds or none?
  - How do the matching strategies compare?
  - How does background-conditioned classification compare with subtracting the background before classifying?
  - Which component accounts for most of the gain, and why is that expected from §3.3?
- **How well does HABM generalize across sites and model architectures?**
  - Which cross-site and cross-architecture results are reported?
  - Where does the gain shrink or disappear?  [TBD: failure cases not yet analysed]
  - What limitation of the method do those cases point to?
```

Things to notice:

- The bold depth-1 questions are word for word the approved Pass A list; Pass B only added the indented children.
- Each child is something one to two sentences can answer, and the children of one parent read in order as the paragraph.
- §3.5's first abstract question mirrors a claim in the abstract and contributions (`↔ §0, §1.3`), and §3.1's objective re-asks the Task 1 question from §1.2. Mirroring marks sit on abstract questions only.
- Every claim named under §3.1's last abstract question has an abstract question in §3.5, and each of those has a child naming the evidence.
