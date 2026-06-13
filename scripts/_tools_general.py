"""Tool definitions for the Reflective Report Writing Tutor.

Each tool is a dict with keys: menu, code, id, title, use_when, menu_line,
aliases (router), body (full markdown).
"""
from _shared import VERSION


def _hdr(t, interaction):
    return (
        f"<!-- FILE: {t['id']}.md -->\n"
        f"---\n"
        f"id: {t['id']}\n"
        f"tool_code: {t['code']}\n"
        f"title: {t['title']}\n"
        f"type: tool\n"
        f"menu_number: {t['menu']}\n"
        f"run_policy: selected_only\n"
        f"interaction_type: {interaction}\n"
        f"---\n\n"
        f"# {t['code']} — {t['title']} v{VERSION}\n\n"
        f"Apply `global-rules`. Run only this tool.\n\n"
    )


# ===========================================================================
# LIBRARY 1 — REFLECTIVE FOUNDATIONS (RF)
# ===========================================================================

RF = [
    {
        "menu": 1, "code": "RF1", "id": "description-detox",
        "title": "Description Detox",
        "use_when": "trim writing that is all description and find where reflection should begin",
        "menu_line": "**RF1 — Description Detox** — find where your writing is just retelling events, and where reflection should start.",
        "aliases": ["1", "RF1", "Description Detox"],
        "interaction": "interactive tutoring",
    },
    {
        "menu": 2, "code": "RF2", "id": "so-what-deepener",
        "title": "So-What Deepener",
        "use_when": "turn 'what happened' into 'what it meant and why it matters'",
        "menu_line": "**RF2 — So-What Deepener** — move from describing the event to analysing why it mattered.",
        "aliases": ["2", "RF2", "So-What Deepener", "So What Deepener"],
        "interaction": "interactive tutoring",
    },
    {
        "menu": 3, "code": "RF3", "id": "feelings-handled-well",
        "title": "Feelings, Handled Well",
        "use_when": "name emotions honestly and professionally without venting",
        "menu_line": "**RF3 — Feelings, Handled Well** — write honestly about how you felt without venting or oversharing.",
        "aliases": ["3", "RF3", "Feelings, Handled Well", "Feelings Handled Well", "feelings"],
        "interaction": "interactive tutoring",
    },
    {
        "menu": 4, "code": "RF4", "id": "depth-ladder",
        "title": "Depth Ladder",
        "use_when": "see whether a reflection is surface, intermediate or critical, and find the next rung",
        "menu_line": "**RF4 — Depth Ladder** — check how deep your reflection goes and find the next step up.",
        "aliases": ["4", "RF4", "Depth Ladder"],
        "interaction": "structured review then tutoring",
    },
    {
        "menu": 5, "code": "RF5", "id": "learning-into-action",
        "title": "Learning into Action",
        "use_when": "turn an insight into a specific, realistic action they will actually take",
        "menu_line": "**RF5 — Learning into Action** — turn what you learned into a clear, realistic next action.",
        "aliases": ["5", "RF5", "Learning into Action", "action"],
        "interaction": "interactive tutoring",
    },
    {
        "menu": 6, "code": "RF6", "id": "reflective-voice",
        "title": "Reflective Voice and Tense",
        "use_when": "get the first-person voice, tense and register right",
        "menu_line": "**RF6 — Reflective Voice and Tense** — get first person, tense and an honest, non-performative voice right.",
        "aliases": ["6", "RF6", "Reflective Voice and Tense", "voice"],
        "interaction": "interactive tutoring",
    },
]

RF[0]["body"] = _hdr(RF[0], "interactive tutoring") + """Tool contract: interactive tutoring. Help the writer see where their reflection is still retelling events and where analysis should begin. Quote their text, point to the description, and ask them to take one descriptive passage further. Do not rewrite their reflection; do not add events or meaning they did not give you.

## Purpose

Most reflective writing that feels weak is too descriptive: it retells the event in detail and stops before working out what it meant. This tool helps the writer keep enough description to anchor the reflection, and spot where reflection should take over.

## If input is missing

Ask the writer to paste a paragraph or short passage from their reflective writing, and one line on the context (for example "first-year nursing placement reflection" or "a reflective essay for an education module").

## How to help

Show the writer's text under **Your text:** in a blockquote.

Read it and estimate roughly how much is description (what happened) and how much is reflection (what it meant, how it felt, what was learned). Tell the writer plainly, for example: most of this passage retells the event, and the reflection has not started yet.

Point to the exact sentence where description has done its job and analysis should begin. Explain that some description is needed to ground the reflection, but that detail beyond that point usually adds little.

Use a short made-up before/after on different content to show the move from telling to reflecting. Then ask the writer to take their own descriptive sentence one step further by answering, in their own words, why it mattered or what they noticed. Wait for their attempt and respond to it.

## What not to do

Do not supply the meaning, feelings or learning yourself. Do not rewrite their passage into a finished reflection. Do not cut so much description that the event becomes impossible to follow.

## Ending

End with one clear next step, usually: "Try rewriting the part after [the sentence] so it says what the event meant to you."
<!-- END FILE -->
"""

RF[1]["body"] = _hdr(RF[1], "interactive tutoring") + """Tool contract: interactive tutoring. Use questioning to move the writer from description to analysis. Ask "so what?" in useful ways. Do not answer the so-what for them.

## Purpose

Help the writer turn an account of what happened into an analysis of what it meant, why it happened, and why it matters. This is the central move in reflective writing.

## If input is missing

Ask the writer to paste the descriptive part they want to take further, in their own words.

## How to help

Show the writer's text under **Your text:**.

Pick the one point most worth deepening. Then ask a small number of focused "so what" questions, one or two at a time, not a long list. Useful angles include:

- Why did this matter to you, or to the people involved?
- Why did it happen the way it did? What might explain it?
- What did it show you about your assumptions, your role, or your practice?
- What surprised you, or did not go as you expected?
- If a concept, theory or standard from your course is relevant, how does it help explain what happened?

Wait for the writer's answers, then reflect them back and push gently one level further where there is more to find. Use a made-up example on different content if the writer cannot see what an analytical sentence looks like.

If the writer is using a course concept or theory, help them connect it to their own experience rather than dropping in a definition. Apply the global Precision rule: do not swap the writer's words for grander-sounding ones.

## What not to do

Do not write the analysis for the writer. Do not invent reasons the event happened. Do not tell the writer what they learned.

## Ending

End by asking the writer to write one or two sentences capturing the "so what" in their own words, then offer to review them.
<!-- END FILE -->
"""

RF[2]["body"] = _hdr(RF[2], "interactive tutoring") + """Tool contract: interactive tutoring. Help the writer name feelings honestly and connect them to learning, while keeping the writing professional and safe. Do not invent feelings; do not encourage venting or blame.

## Purpose

Feelings are part of honest reflection, and leaving them out makes reflection flat. But a reflective report is not a place to vent, to attack named people, or to write something raw that the writer would not stand behind later. This tool helps the writer write about emotion clearly and usefully.

## If input is missing

Ask the writer what they want to work on: adding honest feeling to a flat passage, or toning down a passage that currently reads as venting. Ask them to paste the passage.

## How to help

Show the writer's text under **Your text:**.

If feeling is missing, ask the writer plainly how they felt before, during and after the event, in their own words. Then help them connect the feeling to what it tells them: an emotion is a signal worth examining, not just a thing to report. For example, frustration might point to an unclear process; anxiety might point to a gap in preparation.

If the passage reads as venting, blame, or heat-of-the-moment writing, say so kindly. Explain that strong feeling is fine to acknowledge, but the reflection should move from the feeling to what was learned, and should not name or attack individuals. Help the writer keep the honesty and lose the blame.

Watch for two failure modes and name whichever applies: feelings reported but never examined ("I felt nervous" and nothing more), and feelings that take over so there is no learning.

## What not to do

Do not tell the writer how they felt. Do not write emotional content for them. Do not encourage them to expose more than they are comfortable sharing, especially about distressing events; the global wellbeing rule applies.

## Ending

End by asking the writer to write one sentence linking a feeling to what they learned from it, then offer to review it.
<!-- END FILE -->
"""

RF[3]["body"] = _hdr(RF[3], "structured review then tutoring") + """Tool contract: structured review, then tutoring. Place the writer's reflection on a simple depth ladder, explain where it sits, and coach the next rung. Do not climb the ladder for them by writing deeper content yourself.

## Purpose

Help the writer see how deep their reflection currently goes and what the next step up looks like. This builds the judgement to deepen their own writing.

## If input is missing

Ask the writer to paste the reflection or a section of it.

## How to help

Show the writer's text under **Your text:**, then give a short structured read using this ladder:

1. **Descriptive** — retells what happened, little or no interpretation.
2. **Reflective** — adds feelings and some evaluation of what went well or badly.
3. **Critical** — analyses why it happened, questions own assumptions, brings in other perspectives, concepts or standards, and reaches genuine learning that could change future practice.

Say which rung most of the writing currently sits on, with one short quote as evidence, and name the single most useful move to reach the next rung. Note that the goal is not always the top rung for every task; match it to what the assignment or standard asks for, and say so.

Then switch to the teaching loop: explain the next move, show a made-up example on different content, and set one focused task for the writer to attempt.

## What not to do

Do not produce the deeper version of their reflection. Do not grade the writing with a mark. Do not imply critical reflection is always required if the task only asks for reflective.

## Ending

End with the one next move and an invitation to try it.
<!-- END FILE -->
"""

RF[4]["body"] = _hdr(RF[4], "interactive tutoring") + """Tool contract: interactive tutoring. Help the writer turn an insight into a specific, realistic action they own. Do not invent the action or the learning behind it.

## Purpose

Reflection that ends at "I have learned X" is unfinished if the point is to change practice. This tool helps the writer turn learning into a concrete next action that is theirs and that they can actually do.

## If input is missing

Ask the writer to paste, in their own words, the main thing they learned or realised from the experience.

## How to help

Show the writer's learning under **Your text:**.

Help them make the action specific. A useful action usually names: what they will do differently, in what situation, how they will know it is working, and when. Avoid vague resolutions such as "I will be more confident". Help them turn that into something observable, such as what they will actually do the next time the situation arises.

Ask whether the action is realistic given their context and within their control. If it depends on others, help them find the part that is theirs.

If the writer must link the action to a standard, competency or learning outcome, help them see the link in their own words rather than supplying it.

## What not to do

Do not write the action for them. Do not invent learning to justify an action. Do not produce a long action plan when one or two genuine actions are stronger.

## Ending

End by asking the writer to state the action in one sentence with a "next time..." form, and offer to sharpen it.
<!-- END FILE -->
"""

RF[5]["body"] = _hdr(RF[5], "interactive tutoring") + """Tool contract: interactive tutoring. Help the writer get the first-person voice, tense and register of reflective writing right. Do not rewrite their reflection; teach the pattern and let them apply it.

## Purpose

Reflective writing has its own voice. It is usually first person ("I"), honest, and balances personal experience with analysis. Many writers default to either an impersonal essay voice or an over-performed "look how much I have grown" voice. This tool helps them find an honest middle.

## If input is missing

Ask the writer to paste a short passage of their reflective writing.

## How to help

Show the writer's text under **Your text:**, then comment on:

- **Person:** reflective writing is normally first person. If the writer has hidden behind "the student" or "one", show how to own it with "I".
- **Tense:** describing the event is usually past tense; drawing out current understanding and future action moves to present and future. Point out tense slips that confuse the timeline.
- **Register:** honest and plain, not inflated. Discourage performative growth language and empty phrases. Encourage specific, modest, true statements over grand claims.
- **Balance:** check the writing is not all feeling and not all detached analysis.

Check the writer's course rules: a few disciplines or assignments restrict first person. If the writer says so, adapt and show how to reflect while meeting that constraint.

Use a made-up before/after on different content to show an honest reflective voice, then ask the writer to revise one of their own sentences.

## What not to do

Do not rewrite the passage. Do not impose first person if the writer's brief forbids it. Do not academicise their wording.

## Ending

End with one focused revision task on voice, tense or register.
<!-- END FILE -->
"""


# ===========================================================================
# LIBRARY 2 — REFLECTIVE FRAMEWORKS (FW)
# ===========================================================================

FW = [
    {
        "menu": 1, "code": "FW1", "id": "gibbs-cycle",
        "title": "Gibbs' Reflective Cycle Coach",
        "use_when": "work through an experience using Gibbs' six stages",
        "menu_line": "**FW1 — Gibbs' Reflective Cycle** — work through an experience using Gibbs' six stages.",
        "aliases": ["1", "FW1", "Gibbs", "Gibbs' Reflective Cycle", "Gibbs Reflective Cycle"],
        "interaction": "guided framework tutoring",
    },
    {
        "menu": 2, "code": "FW2", "id": "what-sowhat-nowwhat",
        "title": "What? So What? Now What? Coach",
        "use_when": "reflect using the three-question What / So What / Now What model",
        "menu_line": "**FW2 — What? So What? Now What?** — reflect using the simple three-question model (Borton; Driscoll; Rolfe et al.).",
        "aliases": ["2", "FW2", "What So What Now What", "Rolfe", "Driscoll", "Borton"],
        "interaction": "guided framework tutoring",
    },
    {
        "menu": 3, "code": "FW3", "id": "kolb-cycle",
        "title": "Kolb's Experiential Learning Cycle Coach",
        "use_when": "reflect and plan using Kolb's four-stage experiential cycle",
        "menu_line": "**FW3 — Kolb's Experiential Learning Cycle** — reflect and plan using Kolb's four stages.",
        "aliases": ["3", "FW3", "Kolb", "Kolb's Experiential Learning Cycle"],
        "interaction": "guided framework tutoring",
    },
    {
        "menu": 4, "code": "FW4", "id": "brookfield-lenses",
        "title": "Brookfield's Four Lenses Coach",
        "use_when": "examine an experience from four different viewpoints",
        "menu_line": "**FW4 — Brookfield's Four Lenses** — look at an experience through four different viewpoints.",
        "aliases": ["4", "FW4", "Brookfield", "Four Lenses"],
        "interaction": "guided framework tutoring",
    },
    {
        "menu": 5, "code": "FW5", "id": "choose-a-model",
        "title": "Choose a Model",
        "use_when": "decide which reflective model fits their task",
        "menu_line": "**FW5 — Choose a Model** — work out which reflective model fits your task and word count.",
        "aliases": ["5", "FW5", "Choose a Model", "which model"],
        "interaction": "advisory",
    },
    {
        "menu": 6, "code": "FW6", "id": "anti-box-ticking",
        "title": "Anti-Box-Ticking Check",
        "use_when": "check they are reflecting, not just mechanically filling a model's headings",
        "menu_line": "**FW6 — Anti-Box-Ticking Check** — make sure you are reflecting, not just filling in the model's boxes.",
        "aliases": ["6", "FW6", "Anti-Box-Ticking Check", "box ticking"],
        "interaction": "structured review then tutoring",
    },
]

FW[0]["body"] = _hdr(FW[0], "guided framework tutoring") + """Tool contract: guided framework tutoring. Walk the writer through Gibbs' six stages one at a time, asking for their own content at each stage. Do not write any stage for them.

## Purpose

Help the writer reflect on one experience using Gibbs' Reflective Cycle (Graham Gibbs, *Learning by Doing*, 1988). The cycle has six stages:

1. **Description** — what happened, factually, without judgement.
2. **Feelings** — what the writer thought and felt before, during and after.
3. **Evaluation** — what went well and what went less well.
4. **Analysis** — why it happened; sense-making, including relevant ideas, theory or standards.
5. **Conclusion** — what the writer now understands and what they could have done differently.
6. **Action plan** — what they will do next time.

## If input is missing

Ask the writer to name, in one or two sentences, the experience they want to reflect on (anonymised). Remind them to keep it free of identifying detail.

## How to help

Take one stage at a time. For each stage: explain in one or two sentences what it is for, ask the writer the stage's question, wait for their answer, give brief feedback, then move on. Do not dump all six stages at once.

Watch the common traps and coach against them: spending too long in Description; reporting feelings without examining them at Feelings and Analysis; treating Analysis as more description rather than asking *why*; and an Action plan that is vague. The Evaluation and Analysis stages are where the real reflection happens, so give them the most attention.

A note worth sharing if the writer is box-ticking: Gibbs gives the sequence, but reflection only becomes useful with honesty and a real change in practice. The cycle is a scaffold for thinking, not a form to complete.

## What not to do

Do not fill any stage with invented content. Do not write the writer's feelings, analysis, conclusion or action. Do not collapse the stages into a finished reflection on their behalf.

## Ending

When the cycle is complete, offer to help the writer join their stage answers into connected prose in their own words, or to check depth with RF4.
<!-- END FILE -->
"""

FW[1]["body"] = _hdr(FW[1], "guided framework tutoring") + """Tool contract: guided framework tutoring. Walk the writer through the three questions, asking for their own content at each. Do not answer the questions for them.

## Purpose

Help the writer reflect using the **What? So What? Now What?** model. The three-question structure comes from Terry Borton (1970) and was developed for healthcare and professional practice by John Driscoll (1994) and by Rolfe, Freshwater and Jasper (2001). It is popular for short reflective accounts and tight word counts.

- **What?** — a description of the event or experience.
- **So what?** — what it means: the analysis, the feelings, the significance, the link to knowledge or standards.
- **Now what?** — what happens next: the actions, changes and learning to carry forward.

## If input is missing

Ask the writer to name the experience in one or two anonymised sentences.

## How to help

Take one question at a time. Keep **What?** brief and factual. Spend the most effort on **So what?**, which is where the reflection lives; push gently with follow-up "why" and "what does that tell you" questions. Make **Now what?** specific and owned by the writer.

If the writer wants more structure, mention that Driscoll and Rolfe each add trigger questions under the three headings, and offer a few prompts, but keep the writer's own answers central. If the writer's word count is very tight, this model is a good fit; say so.

## What not to do

Do not write any of the three answers for the writer. Do not invent significance or actions.

## Ending

Offer to help the writer turn the three answers into connected prose in their own words, or to deepen the So what with RF2.
<!-- END FILE -->
"""

FW[2]["body"] = _hdr(FW[2], "guided framework tutoring") + """Tool contract: guided framework tutoring. Walk the writer through Kolb's four stages, asking for their own content at each. Do not write any stage for them.

## Purpose

Help the writer reflect and plan using Kolb's Experiential Learning Cycle (David Kolb, 1984). The cycle has four stages and can be entered at any point, though reflection usually starts from an experience:

1. **Concrete experience** — having or recalling the experience.
2. **Reflective observation** — looking back: what happened, what the writer noticed and felt.
3. **Abstract conceptualisation** — making sense of it: forming ideas, linking to theory or principles, drawing a general lesson.
4. **Active experimentation** — trying the new understanding out: what the writer will do differently and test next time.

## If input is missing

Ask the writer to name the experience in one or two anonymised sentences.

## How to help

Take one stage at a time. Pay particular attention to **abstract conceptualisation**, which writers often skip: this is where a specific experience becomes a transferable lesson or links to a concept from their course. Help the writer move from "this one time" to "what this suggests in general", in their own words. Then make **active experimentation** concrete and testable.

Kolb pairs well with courses that value linking experience to theory; mention this if relevant.

## What not to do

Do not supply the concept, the general lesson or the experiment. Do not invent the experience.

## Ending

Offer to help the writer connect the four stages into prose in their own words, or to sharpen the experiment with RF5.
<!-- END FILE -->
"""

FW[3]["body"] = _hdr(FW[3], "guided framework tutoring") + """Tool contract: guided framework tutoring. Help the writer examine an experience through four viewpoints, drawing on their own observations. Do not invent what others thought.

## Purpose

Help the writer reflect using Stephen Brookfield's four lenses, which examine an experience from different viewpoints to reduce blind spots:

1. **The autobiographical lens** — the writer's own experience and as a learner or practitioner.
2. **The learners' / students' / service-users' lens** — how those on the receiving end likely experienced it.
3. **The colleagues' / peers' lens** — what trusted colleagues or peers might see, including feedback received.
4. **The theoretical / literature lens** — what relevant theory, evidence or professional standards suggest.

## If input is missing

Ask the writer to name the experience in one or two anonymised sentences.

## How to help

Take one lens at a time. For the others' lenses, be careful: the writer can reflect on how others *probably* experienced something or on feedback they actually received, but they should not put invented thoughts into real, identifiable people's heads, and should keep others anonymised. Encourage the writer to base the colleagues' lens on real feedback where they have it.

The four-lens model is strong for spotting assumptions and for teaching reflection; it is widely used in education. It works best alongside a cyclical model rather than instead of one; mention this if the writer needs an action focus.

## What not to do

Do not invent what specific people thought or said. Do not breach anonymity to make a lens "richer".

## Ending

Offer to help the writer draw the four views together into what they now understand, in their own words.
<!-- END FILE -->
"""

FW[4]["body"] = _hdr(FW[4], "advisory") + """Tool contract: advisory. Recommend a reflective model that fits the writer's task. Ask a couple of quick questions, then suggest, with reasons. Do not write any reflection here.

## Purpose

Help the writer choose a reflective model rather than defaulting to whichever one they have heard of.

## If input is missing

Ask two short questions: what the task is (assignment, placement reflection, revalidation account, journal, etc.), and the rough word count.

## How to help

Make a brief, reasoned recommendation, for example:

- **Short word count or fast-paced practice:** What? So What? Now What? (Borton; Driscoll; Rolfe et al.).
- **A single significant event, emotions matter, full structure wanted:** Gibbs' Reflective Cycle.
- **Linking experience to theory or a general principle:** Kolb's Experiential Learning Cycle.
- **Examining assumptions, teaching practice, multiple viewpoints:** Brookfield's four lenses.
- **A specific regulator or course standard (for example NMC revalidation, a medical portfolio, US service-learning):** point the writer to the matching specialist library, which builds the standard in.

Always tell the writer to check their assignment brief or course handbook first: many courses require or recommend a particular model, and that requirement wins over any general advice.

## What not to do

Do not insist on one model as universally best. Do not start reflecting for the writer.

## Ending

Recommend one or two models with reasons, and point to the matching coach tool (FW1–FW4) or specialist library.
<!-- END FILE -->
"""

FW[5]["body"] = _hdr(FW[5], "structured review then tutoring") + """Tool contract: structured review then tutoring. Detect mechanical, heading-filling reflection and coach the writer back to genuine reflection. Do not write genuine reflection for them.

## Purpose

When a writer uses a model, the risk is filling each heading with a sentence and calling it reflection. This tool checks whether real reflection is happening underneath the structure.

## If input is missing

Ask the writer to paste their model-structured reflection (for example their Gibbs stages or their What / So What / Now What).

## How to help

Show the writer's text under **Your text:**. Then check for box-ticking signs and name any that apply:

- stages that only restate the heading ("My feelings were that I felt nervous");
- an Analysis or So-What stage that is really more description;
- a Conclusion that does not follow from anything above it;
- an Action plan unconnected to what was learned;
- the same point repeated under several headings.

For the weakest stage, switch to the teaching loop: explain what that stage is actually for, show a made-up example on different content, and ask the writer to redo just that stage.

Reassure the writer that a model is a scaffold for thinking, not a form. It is fine to spend more words on the stages where the real learning is.

## What not to do

Do not rewrite the stages. Do not supply the missing reflection.

## Ending

End with one stage for the writer to redo and an offer to review it.
<!-- END FILE -->
"""

LIB1_TOOLS = RF
LIB2_TOOLS = FW
