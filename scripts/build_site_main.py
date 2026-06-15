#!/usr/bin/env python3
"""Generate the Reflective Report Writing Tutor website (docs/) - home + tools."""
from _site import page, write, BRAND, TAGLINE, VERSION

PL = "prompt-libraries/latest"

# ---------------------------------------------------------------------------
# HOME
# ---------------------------------------------------------------------------
home_body = f"""<main><section class="hero"><div class="container hero-grid"><div><p class="kicker">Purpose</p><h1>Write your own reflection. Use AI as a tutor.</h1><p class="lead">These toolkit files turn an ordinary AI tool into a reflective-writing tutor. It helps you move from describing what happened to working out what it meant — without writing the reflection for you. Your experience, your feelings, your learning stay yours.</p><div class="btn-row"><a class="button" download="" href="{PL}/reflective_writing_tutor_mini_libraries.zip">Download all mini libraries</a><a class="button secondary" download="" href="{PL}/reflective_writing_tutor_master_library.md">Download master library</a><a class="button secondary" href="try-it/">Try it online</a></div></div><div class="panel"><span class="tag">How it works</span><h2>Choose the help you need.</h2><p>Download a library, upload it to an AI tool, then type <code>prompt</code> to see the menu. Choose a tool and paste a passage of your own reflective writing.</p><p>If you get stuck at any point, say "I'm stuck" and the tutor will take a step back to help you find a manageable next move.</p><p>Not sure where to start? Try the Reflective Foundations library.</p></div></div></section>
<div class="container"><section class="panel notice"><span class="tag">Try it online</span><h2>No download needed</h2><p>Prefer to just start typing? Open a hosted version of the tutor in ChatGPT or Gemini. Read the short privacy note on the page first, and never paste anything that could identify a real person.</p><div class="btn-row"><a class="button" href="try-it/">Try it in ChatGPT or Gemini</a></div></section></div>
<div class="container"><section class="panel" id="downloads"><h2>Choose a library</h2><p>Use a mini library for free plans or focused work. Use the master library if you want everything in one file. Specialist libraries build in a professional standard, so they ask you fewer setup questions.</p><p class="small-note">Current toolkit version: <strong>Reflective Writer v{VERSION}</strong>.</p><div class="grid"><article class="card"><h3>Reflective Foundations</h3><p>The core skills for any reflection: trimming description, the "so what", handling feelings, depth, and turning learning into action.</p><div class="actions"><a class="button" download="" href="{PL}/01_reflective_foundations_library.md">Download library</a><a class="button secondary" href="tools/reflective-foundations.html">Explore</a></div></article><article class="card"><h3>Reflective Frameworks</h3><p>Apply a named model: Gibbs; What? So What? Now What?; Kolb; Brookfield. Plus help choosing one and avoiding box-ticking.</p><div class="actions"><a class="button" download="" href="{PL}/02_reflective_frameworks_library.md">Download library</a><a class="button secondary" href="tools/reflective-frameworks.html">Explore</a></div></article><article class="card"><h3>NHS &amp; Healthcare</h3><p>NMC revalidation accounts, placement reflections, significant events, linking to the Code, and a careful anonymisation check.</p><div class="actions"><a class="button" download="" href="{PL}/03_nhs_healthcare_reflection_library.md">Download library</a><a class="button secondary" href="tools/nhs-healthcare.html">Explore</a></div></article><article class="card"><h3>Medical Reflection</h3><p>Insight-focused portfolio and appraisal entries in line with UK reflective-practice guidance, with anonymisation and tone checks.</p><div class="actions"><a class="button" download="" href="{PL}/04_medical_reflection_library.md">Download library</a><a class="button secondary" href="tools/medical.html">Explore</a></div></article><article class="card"><h3>US &amp; Academic</h3><p>The DEAL model, service-learning, reflective journals, ePortfolio statements, and linking reflection to course outcomes.</p><div class="actions"><a class="button" download="" href="{PL}/05_us_academic_reflection_library.md">Download library</a><a class="button secondary" href="tools/us-academic.html">Explore</a></div></article><article class="card notice"><span class="tag">Start here</span><h3>New to reflective writing?</h3><p>Read the short student guide on what reflective writing is, and why AI should not write it for you.</p><div class="actions"><a class="button" href="student-help/">Student help</a><a class="button secondary" href="guides/frameworks.html">See the frameworks</a></div></article></div></section>
<section class="panel notice"><span class="tag">Important</span><h2>Privacy comes first in reflective writing</h2><p>Reflective reports usually involve other people — patients, service users, clients, pupils, colleagues. Do not paste or upload anything that could identify a real person into a public AI tool unless you have checked your course, placement, employer, regulator and data-protection rules.</p><p>Removing a name is often not enough: a small set of ordinary details together can still identify someone. The anonymisation tools (NH4, MD3) and the <a href="guides/anonymisation.html">anonymisation guide</a> can help.</p></section>
<section class="panel"><h2>Why "reflect for yourself"?</h2><p>The value of a reflective report is the understanding you reach by working through your own experience honestly. If an AI invents your feelings, your insight or your learning, the report is no longer reflection — and in professional contexts it can be misleading or against the rules.</p><p>So this toolkit draws a hard line: it will question you, explain the moves, show made-up examples on other content, and review your attempts. It will not write your experience, feelings, insight or learning for you. That boundary is the point, not a limitation.</p></section>
<section class="panel"><h2>What this toolkit can and cannot do</h2><p>It gives you structured prompts for honest, learning-focused reflection: deepening the "so what", applying a model, meeting a professional standard, and checking anonymity and tone.</p><p>It cannot guarantee anonymity, replace your tutor, supervisor or regulator's guidance, or stop someone who wants AI to write their reflection. Its value is making the honest path the easy one.</p><div class="btn-row"><a class="button secondary" href="student-help/">Student help</a><a class="button secondary" href="guides/">Guides</a><a class="button secondary" href="changelog/">Version history</a></div></section></div></main>"""
write("index.html", page(BRAND, home_body, body_class="home"))

# ---------------------------------------------------------------------------
# TOOLS INDEX
# ---------------------------------------------------------------------------
tools_index_body = f"""<main><article class="reading"><header class="page-intro"><p class="kicker">Libraries</p><h1>Five libraries, thirty tools</h1><p class="lead">Each library is a downloadable Markdown file. Upload one to an AI tool, type <code>prompt</code>, and choose a tool. General libraries suit any reflection; specialist libraries build in a professional standard so they need less setup.</p></header>
<section><h2>General</h2>
<p><strong><a href="reflective-foundations.html">Reflective Foundations</a></strong> — the core skills for any reflective report: Description Detox, So-What Deepener, Feelings Handled Well, Depth Ladder, Learning into Action, Reflective Voice and Tense.</p>
<p><strong><a href="reflective-frameworks.html">Reflective Frameworks</a></strong> — apply a model to your own experience: Gibbs' Reflective Cycle; What? So What? Now What?; Kolb's Experiential Learning Cycle; Brookfield's Four Lenses; Choose a Model; Anti-Box-Ticking Check.</p>
</section>
<section><h2>Specialist formats</h2><p>These reduce the questions the tutor needs to ask, because the standard is built in.</p>
<p><strong><a href="nhs-healthcare.html">NHS &amp; Healthcare (NMC)</a></strong> — NMC revalidation accounts, placement reflections, significant events, anonymisation, linking to the Code, and reflective-discussion prep.</p>
<p><strong><a href="medical.html">Medical Reflection (GMC / AoMRC)</a></strong> — insight-focused portfolio and appraisal entries, anonymisation and disclosure awareness, significant events and feedback, tone and safety, capability linkage.</p>
<p><strong><a href="us-academic.html">US &amp; Academic</a></strong> — the DEAL model, service-learning, reflective journals, learning-outcome linkage, ePortfolio statements, and critical-incident reflection.</p>
</section>
<section><h2>Everything in one file</h2><p>The master library contains all thirty tools. It is larger, so use a mini library on a free AI plan.</p><div class="btn-row"><a class="button" download="" href="../{PL}/reflective_writing_tutor_master_library.md">Download master library</a><a class="button secondary" download="" href="../{PL}/reflective_writing_tutor_mini_libraries.zip">Download all mini libraries (zip)</a></div></section></article></main>"""
write("tools/index.html", page(f"Tools | {BRAND}", tools_index_body, css="style.css", base="../", body_class="reference"))


# Helper for a tool-library explore page
def tool_page(slug, kicker, h1, lead, file_name, rows, example):
    rows_html = "".join(
        f"<tr><td><strong>{c}</strong></td><td>{name}</td><td>{when}</td><td>{get}</td></tr>"
        for c, name, when, get in rows
    )
    body = f"""<main><article class="reading"><header class="page-intro"><p class="kicker">{kicker}</p><h1>{h1}</h1><p class="lead">{lead}</p><div class="btn-row"><a class="button" download="" href="../{PL}/{file_name}">Download this library</a><a class="button secondary" href="../examples/">See examples</a><a class="button secondary" href="./">Back to tools</a></div></header>
<section><h2>Tools included</h2>
<table><thead><tr><th aria-label="Tool code"></th><th>Tool</th><th>Use it when...</th><th>What you get</th></tr></thead><tbody>{rows_html}</tbody></table></section>
<section><h2>Mini example</h2>{example}<p class="small">This is a short illustration. Real exchanges are interactive: the tutor asks, you answer, and it responds to what you actually wrote.</p></section></article></main>"""
    write(f"tools/{slug}.html", page(f"{h1} | {BRAND}", body, css="style.css", base="../", body_class="reference"))


tool_page(
    "reflective-foundations", "General library", "Reflective Foundations",
    "The core skills behind any good reflective report: keeping description in check, finding the meaning, handling feelings well, judging depth, and turning learning into action.",
    "01_reflective_foundations_library.md",
    [
        ("RF1", "Description Detox", "Your writing retells events and stops before reflecting.", "Where description ends and reflection should begin."),
        ("RF2", "So-What Deepener", "You can describe it but not say why it mattered.", "Questions that move you from event to meaning."),
        ("RF3", "Feelings, Handled Well", "Feelings are missing, or the passage reads as venting.", "Honest, professional emotional writing tied to learning."),
        ("RF4", "Depth Ladder", "You are unsure how deep your reflection goes.", "Where it sits: descriptive, reflective or critical, and the next rung."),
        ("RF5", "Learning into Action", "Your reflection ends at \u201cI have learned X\u201d.", "A specific, realistic action you actually own."),
        ("RF6", "Reflective Voice and Tense", "The voice feels like an essay, or over-performed.", "First person, consistent tense, an honest register."),
    ],
    """<p class="example-label">Writer input</p><blockquote>The patient was upset and I didn't know what to say, so I just got the nurse. Then I went to lunch.</blockquote><p class="example-label">Typical tutor response (RF2)</p><div class="sample-output"><p>That tells me what you did. The reflection hasn't started yet. The interesting bit is the moment you didn't know what to say. So what was going on there for you — did you feel out of your depth, worried about saying the wrong thing, unsure of your role? Write one sentence about why that moment mattered, and we'll build from it.</p></div><p class="example-label">What this shows</p><p>The tutor does not supply the feeling or the lesson. It points to where reflection should begin and asks the writer to do it.</p>""",
)

tool_page(
    "reflective-frameworks", "General library", "Reflective Frameworks",
    "Apply a recognised reflective model to your own experience. The tutor guides you through each stage and asks for your content; it never fills the stages in for you.",
    "02_reflective_frameworks_library.md",
    [
        ("FW1", "Gibbs' Reflective Cycle", "You want full structure and emotions matter.", "A guided walk through the six stages."),
        ("FW2", "What? So What? Now What?", "You have a tight word count or fast-paced practice.", "A guided walk through the three questions."),
        ("FW3", "Kolb's Experiential Learning Cycle", "You want to link experience to a general lesson or theory.", "A guided walk through the four stages."),
        ("FW4", "Brookfield's Four Lenses", "You want to test your assumptions from several viewpoints.", "A guided walk through the four lenses."),
        ("FW5", "Choose a Model", "You don't know which model to use.", "A reasoned recommendation for your task."),
        ("FW6", "Anti-Box-Ticking Check", "You filled in the headings but it feels mechanical.", "A check that real reflection is happening underneath."),
    ],
    """<p class="example-label">Writer input</p><blockquote>I'm using Gibbs. For \u201cAnalysis\u201d I wrote: the presentation went badly because I was nervous.</blockquote><p class="example-label">Typical tutor response (FW1)</p><div class="sample-output"><p>That's still close to evaluation — it names what went wrong. Analysis asks <em>why</em>. Why were you nervous: under-prepared, unfamiliar format, a tough audience, high stakes? And why did nerves affect the delivery the way they did? Pick the most honest reason and write a sentence starting \u201cI think this happened because\u2026\u201d.</p></div><p class="example-label">What this shows</p><p>The tutor coaches the difference between evaluation and analysis, and asks the writer to supply the real reason.</p>""",
)

tool_page(
    "nhs-healthcare", "Specialist library", "NHS &amp; Healthcare Reflection",
    "For nurses, midwives, nursing associates and healthcare students. Built around NMC revalidation and UK practice, so it asks fewer setup questions. It will not write your account, and it helps you keep it anonymous.",
    "03_nhs_healthcare_reflection_library.md",
    [
        ("NH1", "NMC Revalidation Reflective Account", "Writing one of your five revalidation accounts.", "A guided account mirroring the NMC form, linked to the Code."),
        ("NH2", "Practice Placement Reflection", "Reflecting on a placement as a student.", "A reflection focused on your development."),
        ("NH3", "Significant Event Reflection", "Reflecting on a critical incident.", "Constructive, anonymised, learning-focused reflection."),
        ("NH4", "Anonymisation and Confidentiality Check", "Before you save or share any reflection.", "A flag of anything that could identify a person, with fixes."),
        ("NH5", "Link to the Code", "You need to connect a reflection to the Code.", "A genuine link to the four Code themes, in your words."),
        ("NH6", "Reflective Discussion Prep", "Getting ready for the reflective discussion.", "Practice talking through your accounts."),
    ],
    """<p class="example-label">Writer input (pasted into NH4)</p><blockquote>On 3 March on Ward 7 at St Elsewhere's, I cared for Mr J, an 82-year-old man with motor neurone disease, who\u2026</blockquote><p class="example-label">Typical tutor response (NH4)</p><div class="sample-output"><p>A few things here could identify someone, even though it's just one sentence: the exact date, the ward and hospital name, the patient's initial and age, and a specific condition. Together those could point to one person. Try: \u201cI cared for an older man with a life-limiting neurological condition.\u201d Keep the date and place out. Removing the name alone wouldn't be enough.</p></div><p class="example-label">What this shows</p><p>The check protects real people, and explains <em>why</em> each detail is a risk so the writer learns to anonymise themselves.</p>""",
)

tool_page(
    "medical", "Specialist library", "Medical Reflection",
    "For doctors, medical students, physician associates and anaesthesia associates. Built around UK reflective-practice guidance (AoMRC, COPMeD, GMC and the Medical Schools Council), with insight, anonymisation and tone at its centre.",
    "04_medical_reflection_library.md",
    [
        ("MD1", "Reflective Practitioner Entry", "Writing a portfolio, appraisal or training reflection.", "An insight-first entry, learning and actions foregrounded."),
        ("MD2", "Insight Builder", "Your entry is still mostly description.", "Questions that draw out genuine insight in your words."),
        ("MD3", "Anonymisation and Disclosure Awareness", "Before you save a reflective note.", "An anonymity check plus accurate, calm context on how notes may be used."),
        ("MD4", "Significant Event and Feedback Reflection", "Reflecting on an event, complaint or compliment.", "Constructive, anonymised reflection focused on learning."),
        ("MD5", "Tone and Safety Check", "You want to be sure the tone is right.", "A flag of blame, venting or heat-of-the-moment framing."),
        ("MD6", "Capability and Curriculum Linkage", "Linking a reflection to a curriculum capability.", "A genuine link in your own words to confirm with your supervisor."),
    ],
    """<p class="example-label">Writer input (pasted into MD2)</p><blockquote>I missed the deteriorating obs on a patient because I was busy. Lesson learned, I'll be more careful.</blockquote><p class="example-label">Typical tutor response (MD2)</p><div class="sample-output"><p>\u201cI'll be more careful\u201d is a resolution, not yet insight. What did this show you about how you prioritise and escalate when you're stretched? What specifically would you do differently next time the workload spikes — a check at set points, handover, asking for help earlier? Write the insight as something you now understand about your own practice.</p></div><p class="example-label">What this shows</p><p>The tutor pushes past a generic lesson toward demonstrable insight, which the writer must articulate themselves.</p>""",
)

tool_page(
    "us-academic", "Specialist library", "US &amp; Academic Reflection",
    "For students in US higher education reflecting on experiential, civic and service-learning. Uses the DEAL model and defaults to US English. It ties reflection to course outcomes without writing it for you.",
    "05_us_academic_reflection_library.md",
    [
        ("US1", "DEAL Model", "You want a structured critical-reflection model.", "A guided walk through Describe, Examine, Articulate Learning."),
        ("US2", "Service-Learning Reflection", "Reflecting on community-engaged work.", "Reflection on academic, personal and civic learning."),
        ("US3", "Reflective Journal", "Keeping a journal that deepens over time.", "A repeatable prompt and pattern-spotting across entries."),
        ("US4", "Link to Learning Outcomes", "A rubric asks you to connect to outcomes.", "A specific link in your own words, pitched at the right level."),
        ("US5", "ePortfolio Reflective Statement", "Framing a piece of work in a portfolio.", "An honest statement of what the work shows."),
        ("US6", "Critical Incident Reflection", "Reflecting on a turning point.", "A focused reflection on what changed and why."),
    ],
    """<p class="example-label">Writer input (Examine step, pasted into US1)</p><blockquote>At the food bank I learned that poverty is bad and we should help people.</blockquote><p class="example-label">Typical tutor response (US1)</p><div class="sample-output"><p>That's a general statement you could have written before going. The Examine step asks you to connect this specific experience to course material and to test your assumptions. What did you actually observe that surprised you or challenged an assumption you arrived with? Which concept from the course helps explain it? Answer with one concrete observation and the concept it connects to.</p></div><p class="example-label">What this shows</p><p>The tutor moves the writer from a platitude to evidence-based examination, in their own words.</p>""",
)

print("tool pages done")
