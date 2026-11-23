# Chapter probes and question skeletons

For each stage: (a) the probes to raise in the discussion *before* drafting — pick the ones the user has not already answered; (b) the generic skeleton the chapter's question list usually follows. The skeleton is a starting shape, not a form to fill; the specific sub-questions come from the discussion. The skeletons predate the two-pass format, so their nesting is not the Pass A / Pass B split: use the granularity guide in `format.md` to decide which lines are abstract questions for the section's page budget (in a one-page abstract the top-level lines are the abstract questions; in a multi-page section the nested, paragraph-sized lines are). Pass B detailed questions are never taken from a skeleton — they come from the discussion.

---

## Stage 0 — Abstract (≈1 pg)

### Probes
- In one sentence, what is the research topic? (If the user needs two sentences, the topic is not yet fixed.)
- Why does the system or community *need* this? What goes wrong without it — a concrete failure, not "better performance".
- What does prior work represent, assume or optimize that is the root of the limitation? Name the representation (categorical labels? pooled embeddings? text transcripts?) — the gap usually lives in the representation.
- How many research tasks, and what is the one-line question of each?
- For each task: method in one clause, result in one clause (a number or a qualitative gain, and on what).
- What is the overall contribution when the tasks are put together? This is not the sum of the tasks; it is what the thesis *enables*.
- Scope: what does the thesis explicitly not cover? (Needed later to keep contributions narrow.)

### Skeleton
- What is the research topic of this thesis?
- Why is <paralinguistic / X> information important for <system>?
- What are the key limitations of previous work?
  - How is <X> typically represented, and what does that representation miss?
  - <second limitation, if any>
- What research tasks are investigated to address these limitations?
  - Task 1 — <name>
    - What methodological approach is proposed, and how does it address the limitation?
    - What improvements are achieved?
  - Task 2 — <name>
    - (same two)
- What overall contribution does this thesis make towards <goal>?

---

## Stage 1 — Introduction (≈4.5 pg: opening 0.5, Motivation 1, Research Problem & Objectives 1, Contributions 1, Outline 0.5)

### Probes
- Motivation: what can current systems already do well? (Students skip this and the gap then looks like a strawman.) What role does <X> play in the human version of the task? Why is the dominant signal (e.g. lexical content) insufficient on its own — give a two-line example of an utterance that is misread without <X>.
- What makes <X> *hard*, as opposed to merely *missing*? Usually two kinds of hardness: representational (cannot be categorised cleanly) and distributional (varies across speakers / contexts / languages). Which apply here?
- Where exactly do existing approaches fall short — representation, modelling, training objective, or evaluation? Map each shortfall to a challenge.
- Research question: one sentence, starting with "How can …". Each task must be a sub-question of it.
- Contributions: for each, what is the *mechanism* (not the name of the method) and what does it let the system do that it could not before? Does the supervisor want contributions stated narrowly? If so, each contribution maps to exactly one paper / one chapter.
- Does the order of tasks in §1.2 match the order of chapters? (Perception before generation, recognition before response, etc.)

### Skeleton
- §1.1 Motivation
  - Why is <X> important for <system>?
    - What is <system>, and what can current ones already do?
    - What role does <X> play in <the human communicative act>?
    - Why is <dominant signal> alone insufficient?
  - What makes <X> understanding / generation challenging?
    - <representational hardness>
    - <distributional hardness>
  - Where do existing approaches fall short?
  - What challenges follow, and what research tasks do they motivate?
- §1.2 Research Problem and Objectives
  - What limitations remain in current <systems>?
  - How has previous work incorporated <X>? (representation; modelling; what each misses)
  - What key challenges remain unresolved? (one per task)
  - What main research question follows?
  - What research tasks are formulated? (Task 1 — how can …? Task 2 — how can …?)
- §1.3 Contributions
  - What methodological contributions address the two tasks?
  - How does contribution 1 <mechanism → capability>?
  - How does contribution 2 <mechanism → capability>?
  - How do the two together advance <goal>?
- §1.4 Report Outline
  - What does each chapter contain?

---

## Stage 2 — Literature Review (≈18–25 pg; one section per line of work of the thesis)

### Probes
- Which lines of work does the thesis have? A common shape is one section per side of the thesis (e.g. understanding; generation), each going from the task family as a whole, to the model class the thesis uses, to the specific task. Ask the user for the outline; do not default to "system class → modelling → task technology" if the thesis is not about that system.
- For each section: what is the historical arc, and does the user plan a timeline figure for it? Which model class does the thesis use, and how is it built and adapted? Which general methods are used across tasks of this field? For the specific task: which approaches exist (conventional; LLM-based), which corpora, metrics and benchmarks — and does the user want a summary table?
- Scope (ask these for the user's outline before drafting): for each section, which task chapter does it lead to? For each sub-section, which question of that chapter would be harder to read without it (reliance)? If none: is it one step more general than what the task chapter needs — the task family, the history behind the model class, the alternative families (distance) — or a neighbouring topic that can go? A sub-section that passes neither test is cut or becomes one acknowledging sentence. Tell the user what share of the review's pages no task-chapter question points to, and let the user judge it. What the thesis's own experiments show belongs in the task chapter.
- What must *not* be in the literature review: (a) the closer, narrower prior work a method directly competes with — that goes in the task chapter's introduction; (b) any argument for the thesis — why a topic matters, why these tasks, why something is out of scope, what remains unsolved; (c) questions about why something has not been done. The literature review asks what is done, how, and why it is done that way. Everything else is a Stage 1 question.

### Skeleton (per section; no closing question unless the user asks for one)
- **Starter: which tasks / demands make up <task family>?**
  - Connector: how does the section go from them to <the specific task>?
- Evolution (often explained around a timeline figure)
  - **How was <task family> built before <model class>?**
  - **How did <model class> come to handle it?** (ends on what <model class> gained: the ground on which a task chapter builds on it)
- Architectures of <model class>
  - **How is <input> represented and aligned with <backbone>?**
  - **Which general methods are used to adapt or improve these models?**
- The specific task
  - **How do conventional approaches handle <task>?**
  - **How do <model class> approaches handle it?**
  - **Which corpora exist, and how is the task evaluated (metrics, benchmarks)?**

---

## Stages 3 / 4 — Task chapter (≈16.5 pg: opening 0.5, Intro 1.5, Background 4, Method 5, Setup 2, Results 3–3.5)

### Probes
- Re-state the task question from §1.2. Does the chapter answer *that* question, or has it drifted (common when the chapter is adapted from a paper with a different framing)?
- Intro: why is this sub-problem important *on its own*, and what is the chapter's objective in one or two "how can" sentences?
- Background: group the directly competing prior work into 2–4 families. For each family: what does it do, what does it assume, what does it lose? What is the shared limitation across families? (That shared limitation is the sentence the method answers.)
- Method: the overall architecture in one figure's worth of description, then one sub-section per component. For each component: inputs, outputs, and the one design decision that distinguishes it from the obvious alternative. Which component carries the main novelty?
- Training: how many stages, what is frozen, what objective at each stage, how are objectives balanced?
- Setup: which datasets, and why *these* for *this* task's claim; which metrics; which baselines (must include the strongest competing family from Background); which settings (zero-shot / fine-tuned / model sizes); what implementation details reviewers will ask for.
- Results: list the chapter's claims (from the intro) and make sure there is one results question per claim. Then: ablations (one per component), generalization (across datasets / backbones / sizes), and qualitative examples if the task's output is open-ended.
- What is the chapter's limitation, stated honestly? (One paragraph; often asked in QE.)

### Skeleton
- Chapter opening — what does this chapter do and which §1.2 challenge does it answer?
- §x.1 Introduction
  - Why is <sub-problem> important?
    - <mechanism of the difficulty, 2–3 leaves>
  - What is the main research objective of this chapter?
    - How can <capability 1>?
    - How can <capability 2>?
- §x.2 Background
  - How have previous studies addressed <sub-problem>?
    - <family 1>: how does it work and what does it lose?
    - <family 2>
    - <family 3>
  - What limitations do existing approaches share?
- §x.3 Proposed <Method>
  - What is the overall architecture?
  - How does <component A> work?
    - <inputs/outputs>
    - <key design decision>
  - How does <component B> work?
  - How is the model trained?
    - <stage 1>
    - <stage 2>
    - How are the objectives balanced?
- §x.4 Experimental Setup
  - Which datasets, metrics, baselines, settings, and implementation details?
- §x.5 Results and Discussion
  - How does <method> perform against existing approaches? (one leaf per claim)
  - How does each component contribute? (ablations)
  - How well does it generalize? (datasets / backbones / sizes)
  - What do qualitative examples reveal? (if applicable)
  - What are the remaining limitations?

---

## Stage 5 — Conclusion and Future Work (optional, ≈2–3 pg)

### Probes
- Does the report need a future-work plan, and how long may the chapter be? Keep it short unless the user asks otherwise, and ask whether a timeline is required rather than assuming one.
- What did the tasks show *together* that neither shows alone? This re-answers the main research question of §1.2; it does not repeat the task results one by one.
- Which limitations do the tasks share? Consolidate them from each task chapter's own limitations paragraph.
- For each future-work direction: what does the thesis leave open that it addresses, is it ongoing or planned, and what will it enable? Use the user's own list; do not add directions.
- Does the list agree with what the contributions section declared out of scope? If the two differ, reconcile them with the user.

### Skeleton
- §5.1 Conclusion
  - What question did the thesis set out to answer, and how do the tasks together answer it?
  - What did each task show about <the shared challenge>?
  - What limitations do the tasks share, and what do they leave open?
- §5.2 Future Work
  - What does the thesis leave open, and which work is planned to address it?
  - How will <direction> address <open point>? (one per direction)
