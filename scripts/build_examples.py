#!/usr/bin/env python3
"""Generate real worked example pages for every tool, styled with css/aichat.css.

Each tool gets docs/examples/example-<code>.html showing a short but genuine chat
exchange: the writer pastes anonymised text, the tutor diagnoses and sets a task
without ever writing the reflection. docs/examples/index.html lists them all,
grouped by library.

The example content lives in EXAMPLES below, keyed by tool id. Every tutor turn
respects the toolkit ethic: it questions, diagnoses and teaches, but never
invents the writer's experience, feelings, insight or learning.
"""
import json
import os

from _site import page, write, BRAND, DOCS  # reuse the shared page template

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
META = json.load(open(os.path.join(ROOT, "src", "prompt-library", "tool-metadata.json"), encoding="utf-8"))

FAMILY_LABELS = {
    "reflective-foundations": "Reflective Foundations",
    "reflective-frameworks": "Reflective Frameworks",
    "nhs-healthcare": "NHS & Healthcare",
    "medical": "Medical Reflection",
    "us-academic": "US & Academic",
}
FAMILY_ORDER = ["reflective-foundations", "reflective-frameworks", "nhs-healthcare", "medical", "us-academic"]


def bot(html):
    return ("chatbot", html)


def user(html):
    return ("user", html)


# Each entry: id -> (intro_lead, [turns]).  Turns are (role, inner_html).
EXAMPLES = {
    # ---- Reflective Foundations -------------------------------------------
    "description-detox": ("How RF1 separates retelling from reflection.", [
        bot("<h2>RF1 — Description Detox</h2><p>Paste a passage of your own reflective writing and I'll show you where it's still describing and where reflection should begin.</p>"),
        user("<p>During my placement I was asked to lead the morning handover. I read out each case, answered a few questions, and then the shift started. It took about fifteen minutes. Afterwards my supervisor said it went fine.</p>"),
        bot("<p><strong>Your text:</strong></p><blockquote>During my placement I was asked to lead the morning handover&hellip; my supervisor said it went fine.</blockquote>"
            "<p>This is almost entirely description: a clear, accurate account of what happened, but the reflection hasn't started yet. The reader knows the sequence of events but not what any of it <em>meant</em> to you.</p>"
            "<p>The richest moment is probably the handover itself — leading it for the first time. <strong>Try this:</strong> write two or three sentences answering only this: what was going on for you while you were leading it? Not what you did — what you noticed, felt, or found harder or easier than expected. I'll work from whatever you write.</p>"),
    ]),
    "so-what-deepener": ("How RF2 moves writing from event to meaning.", [
        bot("<h2>RF2 — So-What Deepener</h2><p>Paste a sentence or short passage where you can describe what happened but feel it hasn't gone anywhere yet.</p>"),
        user("<p>We had a difficult team meeting about the new rota. I said my bit and then it ended. I felt annoyed.</p>"),
        bot("<p>Good — there's a real feeling here to work with. \u201cAnnoyed\u201d is the start, not the end.</p>"
            "<p>So what was underneath it: not being heard, a fairness issue, worry about the workload, something else? I'm not going to guess which, because the honest answer is yours. <strong>Finish this sentence in your own words:</strong> \u201cIt mattered to me because&hellip;\u201d Then we'll turn that into the analysis the passage is missing.</p>"),
    ]),
    "feelings-handled-well": ("How RF3 turns venting into usable reflection.", [
        bot("<h2>RF3 — Feelings, Handled Well</h2><p>Paste the part where you write about how you felt.</p>"),
        user("<p>Honestly the whole thing was a disaster and the other student didn't pull their weight at all, which was so frustrating and typical.</p>"),
        bot("<p>The feeling is clear and it's fine to name frustration. Two things to adjust so this works as reflection rather than venting.</p>"
            "<p>First, it currently aims outward at the other person (\u201cdidn't pull their weight&hellip; typical\u201d). Reflection works better when it stays with your own experience. Second, \u201cdisaster\u201d names a verdict, not a feeling.</p>"
            "<p><strong>Try this:</strong> rewrite one sentence that names what <em>you</em> felt at a specific moment, and what that feeling tells you. Keep the other person anonymous and avoid character judgements. Paste it and I'll review.</p>"),
    ]),
    "depth-ladder": ("How RF4 locates the depth of a reflection.", [
        bot("<h2>RF4 — Depth Ladder</h2><p>Paste a short passage and I'll show you where it sits: descriptive, reflective, or critical — and the next rung up.</p>"),
        user("<p>I realised I find it hard to ask for help. I think this comes from wanting to seem capable. Next time I'll try to ask earlier.</p>"),
        bot("<p>This is already on the <strong>reflective</strong> rung: you've named a pattern and a possible reason, not just events. That's good work.</p>"
            "<p>The next rung is <strong>critical</strong>: testing that explanation rather than accepting it. <strong>Try this:</strong> ask yourself whether \u201cwanting to seem capable\u201d fully explains it, or whether something about the specific situation (the people, the stakes, past experience) also shaped it. Write one sentence that complicates your first explanation.</p>"),
    ]),
    "learning-into-action": ("How RF5 turns a lesson into a real action.", [
        bot("<h2>RF5 — Learning into Action</h2><p>Paste the part where your reflection says what you learned.</p>"),
        user("<p>In conclusion, I have learned that communication is really important and I will improve my communication skills in future.</p>"),
        bot("<p>That conclusion would fit almost any reflection, which is the sign it's too general to act on. \u201cImprove my communication\u201d isn't yet something you could actually do on Monday.</p>"
            "<p><strong>Try this:</strong> name the specific situation where your communication fell short, then one concrete thing you'd do differently next time it arises — something you own and could actually do. For example, a when-then: \u201cwhen X happens, I will&hellip;\u201d Write yours and I'll check it's specific enough.</p>"),
    ]),
    "reflective-voice": ("How RF6 fixes voice and tense.", [
        bot("<h2>RF6 — Reflective Voice and Tense</h2><p>Paste a passage and I'll check the voice, person and tense.</p>"),
        user("<p>One enters the ward and one observes that the patient is anxious. It is then realised that reassurance should be provided.</p>"),
        bot("<p>The meaning is fine, but the voice is doing the opposite of what reflection needs. \u201cOne enters&hellip; it is then realised\u201d removes <em>you</em> from your own account, and reflection is supposed to be first-person.</p>"
            "<p><strong>Try this:</strong> rewrite those sentences in the first person and past tense — \u201cI went onto the ward and noticed&hellip;\u201d — keeping it honest rather than formal. Paste your version and I'll look at the tense consistency next.</p>"),
    ]),

    # ---- Reflective Frameworks --------------------------------------------
    "gibbs-cycle": ("How FW1 coaches the analysis stage of Gibbs.", [
        bot("<h2>FW1 — Gibbs' Reflective Cycle Coach</h2><p>Tell me the experience you want to reflect on (anonymised), and which stage you're on. I'll guide you through the six stages without writing them for you.</p>"),
        user("<p>I'm on the Analysis stage. I wrote: the presentation went badly because I was nervous.</p>"),
        bot("<p>That sentence is still really <em>evaluation</em> — it judges how it went. Gibbs' <strong>Analysis</strong> asks <em>why</em>, and it's where the reflection earns its keep.</p>"
            "<p>Why were you nervous, specifically: under-prepared, an unfamiliar format, a high-stakes audience, something else? And why did the nerves affect the delivery the way they did? <strong>Pick the most honest reason</strong> and write one sentence starting \u201cI think this happened because&hellip;\u201d. I'll help you push it further from there.</p>"),
    ]),
    "what-sowhat-nowwhat": ("How FW2 keeps a short reflection balanced.", [
        bot("<h2>FW2 — What? So What? Now What? Coach</h2><p>Good for short or fast-paced reflections. Tell me your situation in anonymised terms.</p>"),
        user("<p>What: a service user raised their voice at me at the desk. So what: it was stressful. Now what: I'll be more careful.</p>"),
        bot("<p>You've got all three parts, which is the hard bit. But \u201cSo what\u201d and \u201cNow what\u201d are each only one step deep.</p>"
            "<p><strong>So what</strong> should reach meaning, not just restate the feeling. Stressful in what way — did it touch your confidence, your sense of safety, your role? <strong>Now what</strong> should be concrete: \u201cmore careful\u201d isn't yet an action. <strong>Try this:</strong> write one fuller \u201cSo what\u201d sentence, and one \u201cNow what\u201d that names a specific thing you'd do. I'll review both.</p>"),
    ]),
    "kolb-cycle": ("How FW3 links experience to a general principle.", [
        bot("<h2>FW3 — Kolb's Experiential Learning Cycle Coach</h2><p>Tell me the concrete experience you're starting from.</p>"),
        user("<p>I tried a new way of structuring my notes during a lecture and it worked much better. I'm at the Abstract Conceptualisation stage.</p>"),
        bot("<p>Nice — you've got a clear Concrete Experience and you've reflected on it. <strong>Abstract Conceptualisation</strong> is where you turn this single success into a general principle you could reuse.</p>"
            "<p>The trap is staying specific (\u201cthis note method worked in this lecture\u201d). <strong>Try this:</strong> finish the sentence \u201cWhat this suggests more generally is that I learn better when&hellip;\u201d — aiming for something that would also apply beyond note-taking. Then we'll plan how to test it (Active Experimentation).</p>"),
    ]),
    "brookfield-lenses": ("How FW4 surfaces an assumption through another lens.", [
        bot("<h2>FW4 — Brookfield's Four Lenses Coach</h2><p>We'll look at one experience through four viewpoints. Which lens would you like to start with?</p>"),
        user("<p>The students' lens. I taught a session and I think it went well.</p>"),
        bot("<p>The <strong>learners' lens</strong> is a good challenge here, because \u201cI think it went well\u201d is the autobiographical view — your own. This lens asks how it looked from <em>their</em> side, which can differ sharply.</p>"
            "<p><strong>Try this:</strong> name one piece of actual evidence about how the learners experienced it — a question they asked, their faces, something they did afterwards, feedback. Then say whether it confirms or complicates your \u201cit went well\u201d. I won't supply their view; the point is to ground it in what you actually observed.</p>"),
    ]),
    "choose-a-model": ("How FW5 recommends a framework for your task.", [
        bot("<h2>FW5 — Choose a Model</h2><p>Tell me about the reflection you need to write and I'll recommend a model and say why.</p>"),
        user("<p>It's a 300-word reflection for a nursing module on a single shift. No model is specified.</p>"),
        bot("<p>For 300 words on a single event, <strong>What? So What? Now What?</strong> usually fits best: three clear moves, no stage left underdeveloped, and it suits short healthcare reflections.</p>"
            "<p><strong>Gibbs</strong> is the main alternative if feelings are central, but at 300 words its six stages can leave each one thin. My suggestion: draft with What/So What/Now What, and borrow Gibbs' \u201cFeelings\u201d prompt if emotion is important. Want me to set you up with FW2 next? First, though — does your brief truly not name a model? Always check, because many do.</p>"),
    ]),
    "anti-box-ticking": ("How FW6 catches mechanical model-filling.", [
        bot("<h2>FW6 — Anti-Box-Ticking Check</h2><p>Paste a reflection where you've filled in a model's headings but it feels mechanical.</p>"),
        user("<p>Description: it happened. Feelings: I felt fine. Evaluation: it was okay. Analysis: it went okay because I did my best.</p>"),
        bot("<p>You've spotted it yourself — the headings are present but each one is a placeholder. \u201cAnalysis: it went okay because I did my best\u201d restates the evaluation rather than explaining anything.</p>"
            "<p>The model isn't the problem; the boxes just haven't been used to think yet. <strong>Try this:</strong> pick the single heading where you have the most to say honestly, and write three real sentences under it. We'll get one box genuinely working before worrying about the rest.</p>"),
    ]),

    # ---- NHS & Healthcare --------------------------------------------------
    "nmc-revalidation-account": ("How NH1 shapes an NMC revalidation account.", [
        bot("<h2>NH1 — NMC Revalidation Reflective Account</h2><p>We'll work through one of your five accounts, mirroring the NMC form, and link it to the Code. Describe the CPD, feedback or event in anonymised terms.</p>"),
        user("<p>I attended training on recognising sepsis early and it changed how I escalate concerns.</p>"),
        bot("<p>That's a strong basis for an account — a clear piece of CPD with a practice change attached, which is exactly what the form wants.</p>"
            "<p>The NMC account asks what you learned and <em>how your practice changed</em>. \u201cChanged how I escalate\u201d is promising but general. <strong>Try this:</strong> write two sentences — one naming something specific you now do differently when you suspect sepsis, and one on what difference that makes for patients. Keep everything anonymised. Then we'll link it to the relevant theme of the Code (likely <em>Preserve safety</em>).</p>"),
    ]),
    "placement-reflection": ("How NH2 focuses a placement reflection on development.", [
        bot("<h2>NH2 — Practice Placement Reflection</h2><p>Tell me about the placement experience (anonymised) you'd like to reflect on.</p>"),
        user("<p>I shadowed a wound dressing and then did one myself with my supervisor watching.</p>"),
        bot("<p>Good choice — a moment where you moved from watching to doing is rich for a placement reflection, which should centre on <em>your development</em> rather than the procedure.</p>"
            "<p><strong>Try this:</strong> write about the shift from shadowing to doing it yourself. What felt different when it was your hands? What did you find you could already do, and what did you realise you still need to practise? Anonymise the patient throughout. I'll help you link it to your proficiencies afterwards.</p>"),
    ]),
    "significant-event": ("How NH3 keeps a significant event constructive.", [
        bot("<h2>NH3 — Significant Event Reflection</h2><p>Describe the event in anonymised terms. We'll keep this constructive and learning-focused.</p>"),
        user("<p>A medication was nearly given to the wrong patient but it was caught in time.</p>"),
        bot("<p>A near miss is a valuable thing to reflect on, and the fact it was caught matters. Before we go further: make sure nothing here identifies the patient, staff, ward or date.</p>"
            "<p>The aim is learning, not blame — yours or anyone's. <strong>Try this:</strong> describe the point at which the error was caught, and what allowed it to be caught. Then we'll look at what the event shows about the checks in place and your own part in them, written as learning rather than fault.</p>"),
    ]),
    "anonymisation-check": ("How NH4 finds identifying detail before you share.", [
        bot("<h2>NH4 — Anonymisation and Confidentiality Check</h2><p>Paste your reflection and I'll flag anything that could identify a real person — before it goes anywhere.</p>"),
        user("<p>On 3 March on Ward 7 at St Elsewhere's I cared for Mr J, an 82-year-old man with motor neurone disease, who&hellip;</p>"),
        bot("<p>Several details here could identify someone, even in one sentence: the <strong>exact date</strong>, the <strong>ward and hospital name</strong>, the patient's <strong>initial and age</strong>, and a <strong>specific condition</strong>. Together those could point to one person, so removing the name alone would not be enough.</p>"
            "<p><strong>Try this:</strong> \u201cI cared for an older man with a life-limiting neurological condition.\u201d Keep the date and place out entirely. Rewrite your opening that way and paste it back, and I'll check the rest of the passage.</p>"),
    ]),
    "link-to-code": ("How NH5 links a reflection to the NMC Code.", [
        bot("<h2>NH5 — Link to the Code</h2><p>Paste your reflection and tell me if you already have a theme in mind. The four themes are Prioritise people, Practise effectively, Preserve safety, and Promote professionalism and trust.</p>"),
        user("<p>My reflection is about taking time to explain a procedure to a frightened patient until they understood and consented.</p>"),
        bot("<p>This connects most naturally to <strong>Prioritise people</strong> — acting in partnership, respecting the person's right to be involved in decisions about their care — and arguably <strong>Practise effectively</strong> through clear communication.</p>"
            "<p>The link only counts if it's genuine and in your words, not a label bolted on. <strong>Try this:</strong> write one sentence that states, from your own account, how what you did reflects \u201cprioritising people\u201d. I'll check it reads as a real connection rather than a tick-box.</p>"),
    ]),
    "reflective-discussion-prep": ("How NH6 prepares you for the reflective discussion.", [
        bot("<h2>NH6 — Reflective Discussion Prep</h2><p>The reflective discussion is a conversation with another registrant about your accounts. Tell me which account you'd like to practise talking through.</p>"),
        user("<p>The sepsis training one. I'm worried I'll just read it out.</p>"),
        bot("<p>That worry is common and easy to work on. The discussion isn't a reading test; it's you talking about what you learned.</p>"
            "<p><strong>Try this:</strong> without looking at your written account, say out loud (or type) in two or three sentences what changed in your practice and why it mattered. Paste roughly what you'd say. I'll then ask you the kind of follow-up a colleague might — \u201ccan you give an example?\u201d — so it feels like a conversation, not a recital.</p>"),
    ]),

    # ---- Medical -----------------------------------------------------------
    "reflective-practitioner-entry": ("How MD1 leads with insight, not narrative.", [
        bot("<h2>MD1 — Reflective Practitioner Entry</h2><p>For a portfolio, appraisal or training reflection. Describe the event or learning point in anonymised terms.</p>"),
        user("<p>I want to reflect on a clinic where I ran very late and several patients were unhappy.</p>"),
        bot("<p>Useful material. UK reflective-practice guidance is clear that the entry should foreground <em>insight and learning</em>, not a minute-by-minute narrative, and should be anonymised.</p>"
            "<p><strong>Try this:</strong> skip the blow-by-blow and write straight to the insight — what running late and the patients' response showed you about how you prioritise, communicate delays, or manage clinic flow. One or two honest sentences. We'll add a focused action after that.</p>"),
    ]),
    "insight-builder": ("How MD2 pushes past a generic lesson.", [
        bot("<h2>MD2 — Insight Builder</h2><p>Paste the part of your entry that's meant to show insight.</p>"),
        user("<p>I missed the deteriorating obs on a patient because I was busy. Lesson learned, I'll be more careful.</p>"),
        bot("<p>\u201cI'll be more careful\u201d is a resolution, not yet insight — and assessors notice the difference.</p>"
            "<p>What did this show you about how you prioritise and escalate when you're stretched? And what specifically would you do when the workload spikes again — a check at set points, a handover habit, asking for help earlier? <strong>Try this:</strong> write the insight as something you now understand about your own practice, then one action that follows from it.</p>"),
    ]),
    "anonymisation-disclosure": ("How MD3 checks anonymity and gives calm context.", [
        bot("<h2>MD3 — Anonymisation and Disclosure Awareness</h2><p>Paste your reflective note and I'll check anonymity, then give accurate context on how such notes are handled.</p>"),
        user("<p>Should I leave out the date and the fact it was a cardiac arrest? Also can my reflection be used against me?</p>"),
        bot("<p>On anonymisation: yes, keep the exact date out, and avoid combinations that could identify the patient or colleagues — removing the name alone is rarely enough. A specific event plus a place and date can identify someone.</p>"
            "<p>On your second question: reflective notes should focus on learning, and UK guidance encourages writing them. They can in principle be requested by a court, but a regulator doesn't ask for them to investigate a doctor. The practical protection is to write reflectively and anonymously, focusing on insight rather than a detailed factual record. Paste your note and I'll flag anything identifying.</p>"),
    ]),
    "significant-event-analysis": ("How MD4 reflects on feedback or a complaint.", [
        bot("<h2>MD4 — Significant Event and Feedback Reflection</h2><p>Describe the event, complaint or compliment in anonymised terms.</p>"),
        user("<p>I received a complaint that I seemed dismissive. I don't think I was, but it stuck with me.</p>"),
        bot("<p>That it stuck with you is exactly why it's worth reflecting on, and you can do that honestly without either accepting or rejecting the complaint wholesale.</p>"
            "<p><strong>Try this:</strong> set aside whether the label \u201cdismissive\u201d is fair, and write about what the patient might have experienced that led them to feel that way — pace, eye contact, time pressure, wording. Then one thing you could do to reduce that risk. Keep it learning-focused and free of any detail that identifies the complainant.</p>"),
    ]),
    "tone-safety-check": ("How MD5 catches blame and venting in tone.", [
        bot("<h2>MD5 — Tone and Safety Check</h2><p>Paste your draft entry and I'll flag any tone that could read as blame or heat-of-the-moment venting.</p>"),
        user("<p>The whole thing was the nursing staff's fault for not bleeping me sooner, and the system is a joke.</p>"),
        bot("<p>Two flags. First, <strong>blame of named or identifiable colleagues</strong> (\u201cthe nursing staff's fault\u201d) — reflective writing isn't the place to attribute fault to others, and it can read poorly later. Second, <strong>heat-of-the-moment framing</strong> (\u201ca joke\u201d) that adds feeling but no learning.</p>"
            "<p><strong>Try this:</strong> rewrite to focus on the system or process and on your own part in it — for example, what would have helped the concern reach you sooner, and what you'd do differently. Paste the rewrite and I'll re-check the tone.</p>"),
    ]),
    "capability-linkage": ("How MD6 links a reflection to a curriculum capability.", [
        bot("<h2>MD6 — Capability and Curriculum Linkage</h2><p>Tell me the capability or outcome you're mapping to, and paste the relevant reflection.</p>"),
        user("<p>I want to link my reflection on breaking bad news to a communication capability.</p>"),
        bot("<p>That's a sound match in principle. The linkage is only convincing when your account actually evidences the capability, rather than just naming it.</p>"
            "<p><strong>Try this:</strong> point to the specific thing in your reflection that demonstrates the capability — what you did or learned about communicating in that conversation. Write one sentence of the form \u201cThis shows [capability] because I&hellip;\u201d. I'll check it's evidenced, and remind you to confirm the exact wording with your supervisor.</p>"),
    ]),

    # ---- US & Academic -----------------------------------------------------
    "deal-model": ("How US1 deepens the Examine step of DEAL.", [
        bot("<h2>US1 — DEAL Model Coach</h2><p>We'll work through Describe, Examine, and Articulate Learning. Tell me which step you're on and paste your draft. (US English by default.)</p>"),
        user("<p>Examine step. I wrote: at the food bank I learned that poverty is bad and we should help people.</p>"),
        bot("<p>That's a general statement you could have written before you ever went — which is the signal that the <strong>Examine</strong> step hasn't done its work yet. Examine asks you to connect this specific experience to course material and to test an assumption you brought with you.</p>"
            "<p><strong>Try this:</strong> name one concrete thing you actually observed that surprised you or challenged an assumption, and one course concept that helps explain it. Answer with that observation and concept, and we'll build the Examine step from there.</p>"),
    ]),
    "service-learning": ("How US2 separates the three kinds of learning.", [
        bot("<h2>US2 — Service-Learning Reflection</h2><p>Service-learning reflections usually cover academic, personal, and civic learning. Tell me about your placement.</p>"),
        user("<p>I tutored kids at an after-school program. I learned I'm patient and it felt good to help.</p>"),
        bot("<p>That's genuine <strong>personal</strong> learning. A strong service-learning reflection also reaches the <strong>academic</strong> and <strong>civic</strong> dimensions, which are missing so far.</p>"
            "<p><strong>Try this:</strong> add one sentence each. Academic: a concept from your course that the tutoring illuminated or complicated. Civic: something the experience showed you about the community, the program, or the wider issue it addresses. I won't fill these in — they're yours — but I'll help you sharpen them once they're down.</p>"),
    ]),
    "reflective-journal": ("How US3 deepens a journal entry and spots patterns.", [
        bot("<h2>US3 — Reflective Journal Coach</h2><p>Paste a recent entry. I can also help you notice patterns across entries over time.</p>"),
        user("<p>Today was busy. Lots going on in the project. Felt tired but okay. More tomorrow.</p>"),
        bot("<p>That's a log more than a reflection — it records the day but doesn't yet think about it. Journals get their value when one small thing is examined.</p>"
            "<p><strong>Try this:</strong> pick a single moment from \u201clots going on\u201d and write three sentences: what happened, what you made of it, and what you'll carry into tomorrow. Over a few entries I can then help you spot recurring themes — but only from what you actually write.</p>"),
    ]),
    "link-to-outcomes": ("How US4 makes an outcome link specific.", [
        bot("<h2>US4 — Link to Learning Outcomes</h2><p>Paste the outcome from your rubric and the relevant reflection.</p>"),
        user("<p>Outcome: \u201cdemonstrate critical thinking.\u201d My reflection: I thought hard about the project and considered different ideas.</p>"),
        bot("<p>\u201cThought hard\u201d and \u201cconsidered different ideas\u201d assert the outcome rather than demonstrating it — a grader can't see the critical thinking yet.</p>"
            "<p><strong>Try this:</strong> point to the moment where you actually weighed one idea against another and changed or sharpened your view. Write \u201cI demonstrated critical thinking when I&hellip;\u201d and finish it with that specific instance. I'll check it shows the outcome rather than naming it, and that it's pitched at the right level.</p>"),
    ]),
    "eportfolio-statement": ("How US5 frames a portfolio piece honestly.", [
        bot("<h2>US5 — ePortfolio Reflective Statement</h2><p>Tell me which piece of work you're framing and what you want the statement to show.</p>"),
        user("<p>It's my best essay. I want to say it shows I'm a strong writer.</p>"),
        bot("<p>A portfolio statement is more convincing when it shows growth or specific strengths than when it claims a general label like \u201cstrong writer.\u201d</p>"
            "<p><strong>Try this:</strong> name one specific thing this essay demonstrates — a skill you developed, a problem you solved, a piece of feedback you acted on — and what it shows about you as a writer. Write that, honestly, and I'll help you phrase it so it stands on the evidence rather than on the claim.</p>"),
    ]),
    "aha-moment": ("How US6 reflects on a turning point.", [
        bot("<h2>US6 — Critical Incident Reflection</h2><p>Tell me about the moment or turning point you want to reflect on (anonymised where it involves others).</p>"),
        user("<p>There was a moment in a group project where I realized I'd been wrong about the whole approach.</p>"),
        bot("<p>That's a real critical incident — a moment that shifted your thinking. The value is in unpacking the shift, not just reporting it.</p>"
            "<p><strong>Try this:</strong> write what you believed <em>before</em> the moment, what specifically triggered the realization, and what you understood <em>after</em>. Three short sentences. Keep the others in the group anonymous. Once it's down, we'll look at what the change tells you about how you work and decide.</p>"),
    ]),
}


def chat_block(turns):
    rows = []
    for role, html in turns:
        label = "User" if role == "user" else "Chatbot"
        rows.append(
            f'      <section class="ai-chat-turn ai-chat-{role} ai-chat-turn--{role}">\n'
            f'        <div class="ai-chat-role">{label}</div>\n'
            f'        <div class="ai-chat-bubble">{html}</div>\n'
            f'      </section>'
        )
    inner = "\n".join(rows)
    return (
        '<section class="ai-chat-page" aria-label="Example chat">\n'
        '  <div class="ai-chat-window">\n'
        '    <div class="ai-chat-log">\n'
        f'{inner}\n'
        '    </div>\n'
        '  </div>\n'
        '</section>'
    )


def example_page(meta):
    code = meta["code"]
    title = meta["title"]
    ex = EXAMPLES[meta["id"]]
    lead, turns = ex
    body = (
        f'<main>\n<article class="reading"><header class="page-intro">'
        f'<p class="kicker">Example</p><h1>{code} — {title}</h1>'
        f'<p class="lead">{lead} This is one short exchange; real sessions continue interactively, responding to what you actually write.</p>'
        f'<div class="btn-row"><a class="button secondary" href="./">All examples</a>'
        f'<a class="button secondary" href="../tools/">Browse tools</a></div></header></article>\n'
        f'{chat_block(turns)}\n'
        f'<div class="container"><p class="small-note">The tutor questions, diagnoses and teaches, but never writes your experience, feelings, insight or learning. That boundary is the whole point.</p></div>\n'
        f'</main>'
    )
    css_extra = '<link href="../css/aichat.css" rel="stylesheet"/>'
    html = page(f"{code} {title} example | {BRAND}", body, base="../", body_class="reference")
    # inject the aichat stylesheet right after the main stylesheet link
    html = html.replace('<link href="../style.css" rel="stylesheet"/>',
                        '<link href="../style.css" rel="stylesheet"/>\n' + css_extra)
    return f"examples/example-{code.lower()}.html", html


def build_index(tools_by_family):
    rows = []
    for fam in FAMILY_ORDER:
        rows.append(f'<tr><th colspan="3">{FAMILY_LABELS[fam]}</th></tr>')
        for m in tools_by_family[fam]:
            code = m["code"]
            rows.append(
                f'<tr><td><strong>{code}</strong></td><td>{m["title"]}</td>'
                f'<td><a href="example-{code.lower()}.html">Open example</a></td></tr>'
            )
    table = "\n".join(rows)
    body = f"""<main><article class="reading"><header class="page-intro"><p class="kicker">Examples</p><h1>Worked examples for every tool</h1><p class="lead">Each page shows a real exchange: anonymised writing pasted in, and the tutor's reply. The tutor diagnoses, teaches and sets a task — it never writes the reflection. Examples are rendered in a chat style using a separate stylesheet (<code>css/aichat.css</code>).</p></header>
<section>
<table><thead><tr><th aria-label="Tool code"></th><th>Tool</th><th>Example</th></tr></thead><tbody>
{table}
</tbody></table>
</section>
<section><h2>Ready to try one yourself?</h2><div class="btn-row"><a class="button" href="../student-help/">Go to student help</a><a class="button secondary" href="../tools/">Browse all tools</a><a class="button secondary" href="../index.html#downloads">Download a library</a></div></section>
</article></main>"""
    html = page(f"Examples | {BRAND}", body, base="../", body_class="reference")
    html = html.replace('<link href="../style.css" rel="stylesheet"/>',
                        '<link href="../style.css" rel="stylesheet"/>\n<link href="../css/aichat.css" rel="stylesheet"/>')
    return "examples/index.html", html


def main():
    tools = META["tools"]
    by_family = {f: [] for f in FAMILY_ORDER}
    for m in tools:
        by_family[m["family"]].append(m)

    missing = [m["id"] for m in tools if m["id"] not in EXAMPLES]
    if missing:
        raise SystemExit(f"Missing example content for: {', '.join(missing)}")

    for m in tools:
        rel, html = example_page(m)
        write(rel, html)

    rel, html = build_index(by_family)
    write(rel, html)
    print(f"built {len(tools)} example pages + index")


if __name__ == "__main__":
    main()
