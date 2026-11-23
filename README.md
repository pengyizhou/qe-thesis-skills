# qe-thesis-skills

Four agent skills for working out the writing plan of a PhD Qualifying Examination (QE) report or a thesis together with an AI agent, from the first discussion of a chapter to an evidence page your supervisor can review.

> **What these skills are, and what they are not.**
> They are skills for *discussing* the writing plan of a QE report or thesis with an AI agent. They are **not** skills that write a QE report or thesis for you.
> You take part in every step and you make every decision: what each chapter argues, which questions stay, when a pass is final, which references hold, which figures your supervisor sees. The agent only carries out the time-consuming work in between — searching for references, checking metadata and quotes against the sources, proofreading the question list for consistency, cropping figures and tables — and reports back so that you can decide.
>
> **这套 skill 是什么、不是什么。** 它是用来和 AI agent 讨论 QE / Thesis 写作方案的 skill，不是帮人写 QE / Thesis 的 skill。全程需要人深度参与，所有决定都由人来做；AI agent 只帮忙执行耗时的检索、确认、校对、裁切等工作，做完报告给人，由人决定。

## Workflow and gates

**[Open the interactive workflow map →](https://pengyizhou.github.io/qe-thesis-skills/)** (中文 / English)

The map shows the six steps, the 22 gates between them, who passes each gate (you, the agent's own check, a script, or an independent sub-agent), and where a failed gate sends the work back. It also has a tutorial on the constraints for the literature-review chapter. Writing the report itself is not part of the workflow.

| Step | Skill | What it leaves |
|---|---|---|
| 1. Pass A: main questions per chapter, after a discussion of the flow | `qe-question-list` | main questions per chapter, approved by you |
| 2. Pass B: sub-questions at an agreed grain, overlaps merged | `qe-question-list` | the question list, finalized by you |
| 3. References: discovery per main question, metadata check, two-tier full-text reading, quote check | `qe-references` | bibliography, verification table, claims table, reference notes |
| 4. Consolidation: you decide every sub-question whose premise the reading did not support | `qe-references` → `qe-question-list` | final question list with reference tags |
| 5. Slide assets: figures and tables behind each main question | `qe-slide-assets` | assets CSV and crops |
| 6. Evidence page for your supervisor | `qe-evidence-page` | the page |

## Before anything goes to your supervisor

Run an automatic check first: [supervisor-agent](https://github.com/FabianRitter/supervisor-agent) by Fabian Ritter Gutierrez simulates supervisor feedback, calibrated on Prof. Chng Eng Siong's six-step thesis writing method. Its `list-of-questions` skill reviews a chapter-by-chapter question list with page budgets, which is what steps 1–2 here produce, for the structural points a supervisor raises: sections that go from broad to narrow, page budgets that add up, an explicit mapping from the literature review to the contribution chapters, and one-clause questions. Use it on the Pass A export before you show it to your supervisor (M1 on the map), and on the finalized list. See its README for setup.

## What is in this repository

| Path | What it is |
|---|---|
| `skills/qe-question-list/` | Five-stage discussion that turns a report into a chapter-by-chapter question list, in two passes (main questions, then sub-questions). `references/` holds the output format with a fictional worked example, discussion probes per chapter type, and a template for your own storyline. |
| `skills/qe-references/` | The reference step: discovery with sub-agents, de-duplication, metadata check against Crossref and arXiv, full-text reading in two tiers, quote matching against the PDF text, open checks that only you can clear. `kernel.py` holds the helper functions. |
| `skills/qe-slide-assets/` | Chooses, crops and reviews the figures and tables a supervisor needs for each main question, and writes the assets CSV. `kernel.py` holds the cropping helpers. |
| `skills/qe-evidence-page/` | Builds the supervisor-facing evidence page: one card per main question, evidence folded under each sub-question, references per card. |
| `agent-profile/QE_QUESTION_LIST.md` | Description and instructions for a dedicated question-list coach agent. |
| `docs/index.html` | The interactive workflow map, published with GitHub Pages. |

### Files you fill in yourself

Three files ship as templates. The skills read them and, with your agreement, write what you decide into them as you go; they hold your own thesis's context and state, not rules of the skills.

- `skills/qe-question-list/references/storyline-context.md` — your storyline, tasks, chapter structure, fixed terms and supervisor guidance.
- `skills/qe-references/references/project-notes.md` — your reference folder, naming, numbering and the state of your collection.
- `skills/qe-slide-assets/references/project-notes.md` — your asset folders and the state of the assets table.

Optionally, a complete question list from a peer (used with their permission) can be saved as `skills/qe-question-list/references/example-question-list.md` as a standard for granularity. None is included here.

## Installing

Each folder under `skills/` is one skill; keep the folder name as the skill name and keep `kernel.py` at the skill's root.

- **Claude Science**: open **Capabilities → Skills**, click **Add skill**, and choose one of:
  - **Import from GitHub** — add the skills from this repository (`pengyizhou/qe-thesis-skills`).
  - **Upload a skill** — zip one folder under `skills/` (for example `skills/qe-references/`, with its `kernel.py` and `references/`) and drop the `.zip`; repeat for each of the four skills. Uploading `SKILL.md` alone would leave out the helper code and reference files.

  After adding them, check that the four `qe-` skills are switched on in the Skills list. If you work with a restricted specialist (such as the question-list coach in `agent-profile/`), attach the skills to it under **Specialists** as well.
- **Claude Code**: copy the four folders into `~/.claude/skills/` (or a project's `.claude/skills/`).
- **Other agent workspaces**: give the folders to an agent there and ask it to create each skill from its folder. A restricted agent profile needs each skill attached before it can load it.

The `kernel.py` helpers need PyMuPDF (`pymupdf`), Pillow and pandas in the Python environment.

## State of testing

- `qe-question-list`: in regular use since November 2026.
- `qe-references`: helpers tested on a 197-entry bibliography (parsing), a 14-entry metadata sample, and quote matching on real page-marked texts. Not yet run end to end; the sub-agent task texts have not been used as written.
- `qe-slide-assets`: the automatic crop agreed with 207 hand-reviewed crops within 10 points in 137 cases, within 25 points in 24, was clearly wrong in 40 and found nothing in 6. Every crop still has to be viewed.
- `qe-evidence-page`: in use for one report.

## License

Released under the NANYANG TECHNOLOGICAL UNIVERSITY - NTUITIVE PTE LTD Dual License Agreement: free for non-commercial use (teaching, academic research, personal experimentation); commercial use needs a separate license. See [`LICENSE`](LICENSE). For a commercial license, contact yizhou004@e.ntu.edu.sg.
