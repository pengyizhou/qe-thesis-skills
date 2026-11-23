---
name: qe-question-list
description: Five-stage guided discussion that turns a PhD Qualifying Examination (QE) report or thesis into a chapter-by-chapter "question list", built in two passes per chapter — first a short set of abstract questions that carry the argument (never one question per sentence), then a detailed list that expands each abstract question into sub-questions, each answered by one to two sentences of the report. Use whenever the user wants to work out the research problems, storyline, or writing plan of their QE / thesis / confirmation report chapter by chapter (abstract, introduction, literature review, one chapter per research task), or says things like "QE question list", "帮我过一下 chapter X 的 research problem", "下一阶段", "继续 Stage 2", "Pass B", "展开细化问题", or asks to revise, check, extend, or expand an existing question list. Also trigger when the user shares a thesis outline or another student's question list and wants their own built in the same style.
---

# QE Question List

A QE report (and later the thesis) is easiest to write when every sentence or two is the answer to one explicit question, and every such question sits under a larger question that says what that part of the chapter is arguing. A question list is therefore not a checklist of topics — it is the plan of the whole document at two resolutions, written as questions. This skill builds that plan with the user over five stages, one chapter at a time, and inside each chapter in two passes: abstract questions first, detailed questions second. The research problems are discussed before any question is written.

## Where this skill sits

Before any report text is written, the user's workflow has five steps. This skill covers the first two and the question-list side of the fourth.

| Step | What happens | Skill |
|---|---|---|
| 1 | Pass A: the logical flow and the main questions are discussed and fixed | this skill |
| 2 | Pass B: the grain is agreed, the sub-questions are written, overlaps are merged, the user finalizes | this skill |
| 3 | References: discovery per main question, metadata check, full-text reading, quote check | `qe-references` |
| 4 | Consolidation: reference tags on the sub-questions; findings that change a sub-question come back here, and the user decides each | `qe-references`, then this skill |
| 5 | Slide assets and the page the supervisor reads | `qe-slide-assets`, `qe-evidence-page` |

The user decides when a pass is final, and reports when the supervisor has approved something. Do not add an approval gate of your own; record what the user reports in the stage status.

## Why questions, not headings

A heading ("3.3 Proposed Framework") says *where* a paragraph goes; a question ("How is the neutral reference bank constructed?") says *what the paragraph must deliver*. Questions expose weak spots immediately: if the user cannot answer a question in a sentence or two during the discussion, that part of the chapter is not ready to be written, and that is exactly what the discussion is for. Questions also make the storyline auditable — the abstract, introduction, contributions and task chapters all have to answer the *same* questions at different depths, so inconsistencies between them show up as contradictions between question lists.

## Two passes per chapter: abstract, then detailed

Every chapter's list is written twice, at two resolutions, and the first must be approved before the second is started.

- **Pass A — abstract questions.** A short list of high-level questions, one per *argumentative move* of the chapter (typically what one paragraph, or a tight group of paragraphs, has to establish). They are deliberately coarse: an abstract question is never the question behind a single sentence of the content. The test for Pass A is that a reader who answers only the abstract questions, in order, still gets the chapter's whole argument. In practice this is paragraph level in every chapter, a long literature review and the task chapters included: about one abstract question per paragraph of the eventual text, cut along the paragraph structure of the source paper when a chapter is built on one. A coarser cut (one question per sub-section) leaves each abstract question with far more than eight children at Pass B; in a long section, turn the sub-section-level questions into `###` headings and keep the paragraph-level questions as Pass A. In the working file a Pass A question is a **bold** depth-1 bullet, and it is short: one clause. How coarse the main questions are is the user's choice: when `references/storyline-context.md` records a density (main questions per page), count a draft against it before showing it. The second half of a compound question, parenthetical examples and enumerations are sub-question material.
- **Pass B — detailed questions.** Each approved abstract question is expanded into several sub-questions that belong to it and to nothing else (typically three to six). By default each sub-question is answered by about one to two sentences of the report; how fine the sub-questions are is agreed with the user before the expansion starts (see move 4), because it decides how many there will be. The test for Pass B is that answering an abstract question's children in order, at the agreed grain, produces the text that answers the parent — nothing missing, nothing that belongs under a different parent. In the working file the sub-questions are indented under their bold main question. The user may write the first sub-lines himself, sometimes as short notes on the answer; Pass B is complete when every main question has its full set of sub-questions, each phrased as a question.

The split exists because the two passes catch different errors. Pass A exposes problems of argument — a missing step, two moves in the wrong order, a claim with no home — while the list is still short enough to read in a minute and cheap to reorder. Pass B exposes problems of content — a step the user cannot actually fill, a number that is not yet available. Expanding first and restructuring later means rewriting dozens of detailed questions, so do not show Pass B material until the user has said yes to Pass A for that chapter.

Pass A may run ahead of Pass B: if the user wants to settle the abstract questions for several chapters (or the whole report) before expanding any of them, do that, and record per chapter which passes are done.

## Questions first; references are a separate step

The order for every chapter is: Pass A → consistency check of Pass A → Pass B → the user finalizes Pass B. Everything about references happens after that, with the `qe-references` skill.

- **Neither pass carries reference work.** No literature search and no `[refs: …]` tags while a pass is being drafted: a reference supports a sentence, and only a final Pass B says what the sentences are. Write the questions from the discussion, the user's papers and what the user states. A premise about the literature that nobody has checked keeps its question and gets `[TBD: premise to be checked at the reference step]`; a reason the report gives for its own scope is such a premise whenever it says something about other work.
- **The check before Pass B.** When Pass A is settled, run the consistency checks on it and report. Fix what the user agrees to fix, then expand.
- **Tags that already exist stay.** `[refs: …]` and `[check: …]` tags from a reference step stay on their lines and move with them; `qe-references` defines them. When that step finds that a sub-question's premise is not supported, the proposed rewording, split or cut comes back here, and the user decides each one.

## The five stages

| Stage | Chapter | What the discussion must settle |
|---|---|---|
| 0 | Abstract | The one-paragraph version of the whole story: topic → why it matters → what prior work misses → the research tasks → method + result per task → overall contribution |
| 1 | Introduction | Motivation, research problem and objectives, contributions, outline. The place where the *gap → challenge → task* chain is argued, not just stated |
| 2 | Literature Review | One section per line of work of the thesis, each going from the task family as a whole to the model class and then to the specific task (approaches, corpora, evaluation). It surveys what is done, how, and why it is done that way; it does not argue for the thesis |
| 3 | Task 1 chapter | Introduction, background, proposed method, experimental setup, results |
| 4 | Task 2 chapter | Same structure as Stage 3 |
| 5 (optional) | Conclusion and Future Work | What the tasks showed together, the limitations they share, and the future-work plan. Short by default (2–3 pages) |

If the thesis has more than two tasks, add a stage per task; if it has one, Stage 4 is dropped. Ask once at the start how many task chapters there are, then keep that fixed. Ask at the same time whether the report must carry a future-work plan (a QE report usually must): if so, a closing Conclusion and Future Work chapter is the last stage, and its future-work questions have to agree with what the contributions section declared out of scope.

Stages run in order the first time through because each later chapter *depends on* decisions made earlier (the abstract fixes the tasks; the introduction fixes the challenges each task answers; the literature review sections mirror the task chapters). After the first pass, the user may jump to any stage to revise it, and a revision to an early stage should trigger a consistency re-check of later ones (see "Consistency checks").

## Running a stage

Each stage has the same five moves. Do not skip the discussion — writing questions before the research problem is settled produces a list that looks complete and says nothing — and do not merge moves 3 and 4.

### 1. Locate and recap

Find the working file (default `question-list.md` in the working directory; the user may keep it in a Project doc instead — if a Project is attached, check there first). Read it. State in two or three lines which stages are done (and for each, whether Pass A only or Pass A and B), which stage and pass you are starting, and the decisions from earlier stages that constrain this one (for Stage 3: "Task 1 was defined in Stage 1 as …; the chapter must deliver that"). If no file exists, this is Stage 0: ask for the storyline, the research tasks, and the papers each task is built on. Read `references/storyline-context.md` if it exists for standing context about this user's thesis; its chapter-structure section and the Terms block of `question-list.md` override the generic skeletons in `chapter-probes.md`.

### 2. Discuss the research problem (before any questions)

Hold a short, focused conversation about *what this chapter has to argue*. Ask two to four questions at a time, not a wall; wait for answers; push back where the answer is vague. Reference `references/chapter-probes.md` for the probes that matter for each chapter — but select, don't recite. The probes exist to surface the things students most often leave implicit:

- the **gap**: what prior work represents or assumes that is wrong or too coarse for this problem
- the **challenge**: why the gap is hard (not just "nobody did it")
- the **task**: a one-sentence research question that the chapter answers
- the **claim**: what the method does that addresses the challenge, and what evidence will show it
- the **boundary**: what is explicitly *out* of scope (a supervisor often wants a broad introduction but narrow contributions — respect that split when the user states it)

**Ask for the flow before proposing one.** This is a required part of every Pass A discussion, and it is separate from the details. For the chapter, and then for each section, ask the user in what order they want to show things: which move comes first and what it leads to, which figure or table anchors the section, and what the reader should have concluded by its end. Do not offer a structure of your own until the user has described theirs; a structure proposed early tends to be generic and is re-cut later. If the user asks for a proposal, give two orderings and say what each puts in front.

End the discussion with a brief summary of what was decided, in the user's own terms, including the agreed flow in one line per section, and get a yes before drafting. The discussion itself is in whatever language the user is writing in; the question list is in academic US English because it will be the skeleton of the English report.

### 3. Pass A — draft the abstract questions

Write the chapter's abstract questions in the format in `references/format.md` (section headings with page budgets, one line per abstract question, no children yet). The rules that make Pass A usable:

- **One abstract question per argumentative move, not per sentence.** If an abstract question could be answered in one or two sentences, it is a detailed question that has lost its parent — find the move it serves and ask that instead. If answering it would take more than about a page, it is hiding two moves — split it.
- **The abstract questions alone must carry the argument.** Read them top to bottom without their sections' headings: if the chain gap → challenge → task → method → evidence is not visible, a move is missing or out of order.
- **Ask "how" and "why", not "what is".** "What is an SDS?" invites a definition; "What can current LLM-driven SDSs already do, and what do they miss?" invites an argument. Definitions are Pass B material under an argumentative parent.
- **Mirror structure across chapters deliberately.** Every task chapter has the same five sections, and their introductions re-ask (at chapter depth) the task question that Stage 1 posed. The abstract and the contributions section ask the same abstract questions as the task chapters. Keep the wording parallel so the mirroring is visible.
- **Page budgets are planning tools, not padding targets.** Put a budget on each section (e.g. `## 3.3 Proposed Framework (5 pg)`) derived from the user's total page limit, and use the granularity guide in `references/format.md` for how many abstract questions that budget supports. If the questions outrun the budget, the section is over-scoped — say so. Budgets count text only: ask once whether the user's page numbers include figures and tables, and if they do, subtract the expected floats before using the guide.
- **Chapter opening** paragraphs (0.5 pg) get one abstract question: "What does this chapter do, and how does it connect to the previous one?"
- **A literature review surveys; it does not argue.** Its questions ask what is done, how, and why it is done that way. It never asks why something has *not* been done, and never why the thesis does something: motivation, the choice of tasks, scope decisions, gap statements and "what remains unsolved" are asked in the introduction and in each task chapter's introduction. Its sections have no closing question unless the user asks for one, and need no logical bridge to one another; a "Connector" sub-question inside a section's starter is enough. Follow the user's outline for its sections — a common shape is one section per side of the thesis, each going from the task family as a whole (often an "evolution" sub-section explained around a timeline figure), to the model class, to the specific task with its approaches, corpora, metrics and benchmarks (often one summary table). What the thesis's own experiments show is said in the task chapter. Put a method that is general to a field with the general model class, not under the application the thesis uses it for. Argue importance from the phenomenon itself, never from the fact that benchmarks test it. Record planned figures and tables on the heading. When an evolution sub-section is followed by an architecture sub-section, divide them by *what it is* and *how it works*: the evolution part names each step and says what it is in a sentence or two; the architecture part explains the mechanism of the line of work the thesis uses. A system or a figure has one home. When the evolution ends in a set of families of current methods, give each family a sub-question of its own, then one sub-question that compares them (it holds the summary table), then one that says which family the rest of the chapter follows and why; narrow the title of the next sub-section to that family.
- **A literature review leads to the task chapters; it is not a survey of the field.** Each section leads to one task chapter. A sub-section or a main question is kept only if it passes one of two tests. *Reliance*: a question in a task chapter needs this content; name that question and give it a cross-reference mark that points to the lowest-level sub-section of the review. *Distance*: no task-chapter question needs it directly, but it is one step more general than what a task chapter needs: the task family the task belongs to, the history that explains why the field adopted the model class the thesis works with, or the alternative families that show where the thesis's choice sits. Such content gets less space the farther it is from the task. An evolution sub-section passes on distance. It should end on what the current model class gained; the review states this as fact, and the task chapter's question about its own model is where the thesis draws on it. Content that passes neither test (a neighbouring field, a use of the model class that the thesis does not study, a family of methods it does not use) is cut or becomes one acknowledging sentence. The opposite failure counts too: a review organized by the thesis's own contributions, or one that leaves out background a task chapter relies on. The user's outline decides the sections: apply the two tests to it, and do not propose broader sections than the user asked for.
- For task chapters, the Results section must have at least one abstract question per claim made in the chapter introduction — otherwise a claim goes unsupported. Check this explicitly.

Save the Pass A list into the working file, show it to the user in full, and ask for approval or changes. Stop here. Do not draft Pass B in the same turn, and do not attach "preview" sub-questions to the Pass A list. Do not look for references either (see "Questions first").

### 4. Pass B — expand each abstract question into detailed questions

Once the user has approved Pass A for the chapter (or for the sections they name), expand it:

- **Agree on the grain first.** Before writing any sub-question, ask the user how detailed the sub-questions should be: how many sentences of the report one sub-question stands for, or how many sub-questions a main question should have. Work out what that means for the chapter (text pages × about 20 sentences ÷ sentences per sub-question) and tell the user the total before drafting. When the user has set a density of main questions, one main question covers many sentences, so either the sub-questions are coarser than one to two sentences or there are many of them; the user chooses. Record the agreed grain in the working file.
- **Several sub-questions per abstract question, each at the agreed grain** (one to two sentences of the report unless the user chose otherwise). Three to six children is typical at that default. One child means the abstract question was already detailed — merge it into a neighbour or reopen Pass A for it. More than about eight means it is two moves.
- **Every sub-question has exactly one parent.** A sub-question that fits under no abstract question is evidence that Pass A is missing a move; say so and propose the abstract question rather than parking the orphan under the nearest parent.
- **Order the children as the sentences will appear.** The children of one parent, answered in sequence, should read as the paragraph(s). Typical sequences: claim → reason → evidence → consequence; or setup → mechanism → inputs/outputs → why this design.
- **Be concrete where Pass A was general.** This is where definitions, named datasets, metrics, baselines, numbers, and the specific table or figure that carries a result belong. For each Results claim, at least one child names the evidence (which comparison, which metric, on what data).
- **Do not rewrite the parents.** Pass B adds children; the approved abstract questions stay word for word. If expansion shows that a parent is wrong, flag it and ask before changing it.
- **Mark gaps instead of guessing.** When the discussion did not settle something, write the question anyway and tag it `[TBD: …]` with what is missing. A question the user cannot yet answer is more useful than a plausible one you invented. Detailed questions are where most `[TBD]`s appear; that is expected.

- **Check for overlap, then merge (required).** When a section has been expanded, compare every sub-question with the other main questions of the chapter and with their sub-questions. Where two cover the same content — one system explained twice, a definition asked in two places, a history question and a mechanism question that both describe the same model — stop and discuss the flow with the user: which main question owns the content, and what the other one keeps. Then merge the duplicates, and report what was merged and where each piece went.

If expanding a section raises points the discussion never covered, ask about them (two to four questions at a time) before writing the children — Pass B is not licence to fill gaps with assumptions.

Pass B is final when the user says so. Only then does the reference step start, with `qe-references`.

### 5. Check, save, hand off

Run the consistency checks below against the stages already written. Save the chapter's list into the working file (replace that chapter's section; leave the others untouched) and update the stage status with the pass reached. Then show the user the new material in full, flag every `[TBD]`, and ask whether to refine it or move on (to Pass B of this chapter, or to the next stage). Do not start the next pass or stage on your own.

## Consistency checks

The storyline threads through all chapters; these are the threads to pull after each stage.

- **Tasks**: the tasks named in the abstract (Stage 0), in §1.2 (Stage 1), in the contributions (Stage 1) and the task chapter titles (Stages 3–4) must be the same tasks in the same order with parallel wording.
- **Gap → challenge → task → method → result**: each task's chain must be stated once in the abstract (one clause each), argued in the introduction, and delivered in its chapter. If the chapter's results questions answer something the introduction never asked, either add the question to Stage 1 or drop it.
- **Literature review coverage, both ways**: (a) every background topic that a task chapter relies on has a home in Stage 2, and the task chapter goes *deeper* instead of repeating it; (b) every lowest-level sub-section of Stage 2 passes the reliance or the distance test of Pass A. For (b), list the pairs (sub-section of the review, task-chapter questions that point to it) and report the share of the review's pages that lies in sub-sections no task-chapter question points to. Report it after Pass A of the review, after Pass A of each task chapter, and whenever a section of the review is restructured. The share is an indicator for the user to judge, not a limit; a sub-section that passes neither test is reported as a finding, and so is a task-chapter question about the thesis's model or task that has no sub-section of the review to point to. When the user cuts a topic, record where its content goes instead (a sub-question, one acknowledging sentence, or a task chapter). Check also that no Stage 2 question argues for the thesis ("why does this thesis …", "what remains unsolved for Task N"); such questions belong to Stage 1.
- **Terminology**: the key terms (how the paralinguistic or affective information is represented, what the method is called, what the metric is) must be used identically across stages. Keep a short "Terms" block at the top of the working file and update it.
- **Scope**: nothing in the contributions or task chapters may be broader than what the discussion fixed as the boundary.
- **Definitions against structure**: when a taxonomy is added or a section title is narrowed, read the Terms block again. A term that is defined more narrowly than the taxonomy uses it, or a title that only repeats the definition, is a conflict; propose either widening the definition or keeping the title, and let the user choose.
- **One home**: no system, definition or figure is explained under two main questions. Adjacent sub-sections (evolution and architecture, method and setup) are where this fails.
- **Scope sentences**: a sentence that says why the report follows one line of work states what the thesis's methods act on. It does not claim what the other lines cannot do unless that claim has been checked; until then it carries a `[TBD]`.
- **Two-pass integrity**: every detailed question has exactly one abstract parent; every expanded abstract question has at least two children; no abstract question is answerable in a single sentence; and the abstract questions of a chapter, read alone, still state its argument. Cross-chapter checks (tasks, chain, mirroring) are run on the abstract questions; the detailed questions are checked for terminology and for evidence behind each claim.

When a check fails, say which earlier stage's question conflicts with which new one and propose the smaller fix. Only edit an earlier stage with the user's agreement.

## Resuming, revising, jumping

- "继续 / next stage / Stage N": recap from the file, then run that stage, starting at Pass A (or at Pass B if Pass A for that chapter is already approved).
- "Expand / 展开 / Pass B for chapter X": check that Pass A for that chapter is approved, then run move 4 for it.
- "Abstract questions for the whole report first": run moves 1–3 chapter by chapter without Pass B, then return for the expansions in order.
- "Revise chapter X": re-open the discussion for the points the user names, re-draft only the affected questions, and re-run the consistency checks downstream of that chapter. A change to an abstract question after Pass B invalidates only that question's children — re-expand those and leave the rest.
- "Check the list": run only the consistency checks over the whole file and report.
- "Find references / 找 reference / check the references": that is the `qe-references` skill. Check that the user has finalized Pass B for that chapter; if not, say so and finish Pass B first.
- "Restructure a section that is already settled": discuss first and change nothing until the points are agreed. Name the overlap or the gap, propose the smallest re-cut, and check it against the Terms block. If the user has reported the supervisor's approval of that part, record the change in the stage status so that it can be pointed out at the next review.
- "The supervisor approved / commented": record it in the stage status with the date. Comments on the evidence page come back as changes to Pass A or Pass B and go through the same discussion as any revision.
- "Slides / assets / 证据页": after the reference step, the asset table is built with `qe-slide-assets` and the page with `qe-evidence-page`.
- "Give me a prompt for the other agent": write it so that it can be pasted as it is — the pages or files in scope, and that nothing else may change; the exact wording of every question; which content goes where; text and numbers only from what has been checked, with `[TBD: source needed]` where it has not; and a request to list what was changed.
- "Give me a clean version / questions only": write the questions-only export described in `format.md` as a separate file; do not strip the tags from the working file.
- The user sends back an edited copy of an export: compare it with the working file, sync the working file to the user's wording and structure, re-attach the reference and check tags, and report what changed and any main question whose sub-questions no longer fit under it. The user's wording is final.
- "Is this question needed?": give a clear recommendation, say what would be lost, and where that content would go instead (another question, a sub-question, a task chapter). Apply the cut only when the user decides.
- "Turn this into an outline / write §X": the question list is the writing plan — write one to two sentences per detailed question, in order, grouped into paragraphs by abstract question, and keep each abstract question as a hidden comment above its paragraph so the user can see which question the text answers. Sections that have only Pass A cannot be written yet; expand them first.

## Files

- `references/format.md` — the exact output format for both passes, the granularity guide, and a worked example chapter shown at Pass A and (for one section) at Pass B.
- `references/chapter-probes.md` — discussion probes per chapter type, and the generic question skeleton for each. The skeletons are Pass A (abstract-question) shapes; Pass B children come from the discussion, not from a template.
- `references/example-question-list.md` (optional, not shipped) — a complete question list from a peer, saved here with their permission. If it exists, use it as the standard for Pass A granularity and cross-chapter parallelism; do not copy its content. If it does not, the granularity guide in `format.md` is the standard.
- Related skills: `qe-references` (the reference step), `qe-slide-assets` (figures and tables for the supervisor's page), `qe-evidence-page` (the page itself).
- `references/storyline-context.md` — standing context about the user's own thesis storyline, supervisor guidance and papers. Read it at Stage 0 and whenever the storyline is in question; update it (with the user's agreement) when a stage changes a decision it records.
