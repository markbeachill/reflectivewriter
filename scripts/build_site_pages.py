#!/usr/bin/env python3
"""Generate the remaining Reflective Report Writing Tutor pages.

about, examples, student-help, guides (index + frameworks + anonymisation +
teaching-approach), changelog, and the .nojekyll marker.
"""
import os
from _site import page, write, BRAND, VERSION, LAST_UPDATED, DOCS

PL = "prompt-libraries/latest"

# ---------------------------------------------------------------------------
# ABOUT
# ---------------------------------------------------------------------------
about_body = """<main>
<article class="reading"><header class="page-intro"><p class="kicker">About</p><h1>About this site</h1><p class="lead">Background on the Reflective Report Writing Tutor, who made it, and where the project files live.</p></header>
<section>
<h2>Creator</h2>
<p>This toolkit was created by <a href="https://www.linkedin.com/in/markbeachill/" rel="noopener noreferrer" target="_blank">Dr Mark Beachill</a>. It is part of the same family as the <a href="https://markbeachill.github.io/tutorprompts/" rel="noopener noreferrer" target="_blank">AI Personal Tutor Toolkit</a> and follows the same tutor-not-ghost-writer design.</p>
</section><section>
<h2>Repository and discussion</h2>
<p>The GitHub repository is at <a href="https://github.com/markbeachill/reflectivewriter" rel="noopener noreferrer" target="_blank">github.com/markbeachill/reflectivewriter</a>. Use the repository's Discussions area for comments, questions or suggestions.</p>
</section><section>
<h2>What this site is for</h2>
<p>Reflective writing is a standard requirement across nursing, medicine, teaching, social work, higher education and professional development. Students and practitioners are often asked to reflect but rarely taught how, and general AI tools make it easy to generate a plausible-sounding reflection that contains no actual reflection at all.</p>
<p>This toolkit takes a different route. It turns an ordinary AI tool into a tutor that questions you, explains the moves, shows worked examples on unrelated content, and reviews what you write — without supplying your experience, your feelings, your insight or your learning. The honest path is made the easy one.</p>
</section><section>
<h2>Specialist libraries</h2>
<p>Alongside two general libraries, the toolkit includes specialist libraries that build a professional standard into the tutor: NHS and healthcare reflection around NMC revalidation, medical reflection around UK reflective-practice guidance, and US academic reflection around the DEAL model. Because the standard is built in, these libraries ask fewer setup questions before they can help.</p>
</section><section>
<h2>For developers and departments</h2>
<p>The public files are designed to be used as they are. Departments who want a smaller or locally tailored version can edit the master library, removing tools they do not need and adding local rules carefully. The repository's developer notes explain where the prompt files live and how to rebuild them without weakening the core design.</p>
</section><section>
<h2>Important limits</h2>
<p>This site is not affiliated with the NMC, GMC, any medical royal college, or any university. It summarises publicly available guidance to help you write your own reflection; it does not replace your course, placement, employer or regulator's own rules. Always check those, especially on confidentiality and anonymisation.</p>
</section></article>
</main>"""
write("about.html", page(f"About | {BRAND}", about_body, body_class="reference"))


# ---------------------------------------------------------------------------
# STUDENT HELP
# ---------------------------------------------------------------------------
student_body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Student help</p><h1>How to use the toolkit</h1><p class="lead">Everything you need to get started, plus the one rule that matters most: the tutor helps you write your reflection — it does not write it for you.</p></header>
<section>
<h2>Getting started in four steps</h2>
<ol class="steps">
<li><strong>Download a library.</strong> Start with <a href="../{PL}/01_reflective_foundations_library.md" download>Reflective Foundations</a> if you are new, or a specialist library if you have a set standard to meet (NHS, medical, US academic).</li>
<li><strong>Upload it to an AI tool.</strong> Attach the Markdown file to a conversation in a tool that accepts file uploads, or paste its contents in.</li>
<li><strong>Type <code>prompt</code>.</strong> This shows the menu of tools. Pick one by number or name.</li>
<li><strong>Paste a passage of your own writing,</strong> or describe your situation, and work through the questions. Type <code>prompt</code> at any time to return to the menu.</li>
</ol>
</section><section class="notice">
<span class="tag">The main rule</span>
<h2>This is not a first-draft generator</h2>
<p>The tutor will not invent what happened to you, how you felt, what you realised, or what you learned. Those are the parts that make a reflection yours, and in professional contexts inventing them can be dishonest or against the rules.</p>
<p>What it <em>will</em> do is ask good questions, explain the difference between description and reflection, show you worked examples on unrelated situations, and review what you write. If that feels like more work than getting an AI to "just write it" — that is the point. The work is the reflection.</p>
</section><section>
<h2>If you get stuck</h2>
<p>Say <strong>"I'm stuck"</strong> at any point. The tutor will take a step back, make the task smaller, and offer a more manageable next move. You can also ask it to explain why it is asking something, or to give another example.</p>
</section><section class="warning">
<h2>Protect real people</h2>
<p>Reflective reports usually involve others — patients, service users, clients, pupils, colleagues. Before you paste anything into a public AI tool, check your course, placement, employer, regulator and data-protection rules. Do not include anything that could identify a real person.</p>
<p>Removing a name is often not enough: a handful of ordinary details together can still point to one person. Use the anonymisation tools (NH4 for healthcare, MD3 for medical) and read the <a href="../guides/anonymisation.html">anonymisation guide</a> before you share or save.</p>
</section><section>
<h2>Free AI plans</h2>
<p>On a free plan, prefer a single <strong>mini library</strong> rather than the master file — the master contains all thirty tools and is large. One mini library is usually well within limits and keeps the tutor focused.</p>
</section><section>
<h2>Which library should I use?</h2>
<ul class="list-clean">
<li><strong>New to reflection, or any subject:</strong> Reflective Foundations.</li>
<li><strong>Told to use a named model:</strong> Reflective Frameworks (Gibbs, What/So What/Now What, Kolb, Brookfield).</li>
<li><strong>Nursing or midwifery (NMC):</strong> NHS &amp; Healthcare.</li>
<li><strong>Medicine, PA or AA (UK):</strong> Medical Reflection.</li>
<li><strong>US higher education, service-learning:</strong> US &amp; Academic.</li>
</ul>
<div class="btn-row"><a class="button" href="../tools/">See all libraries</a><a class="button secondary" href="../examples/">See example sessions</a></div>
</section></article>
</main>"""
write("student-help/index.html", page(f"Student Help | {BRAND}", student_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# GUIDES INDEX
# ---------------------------------------------------------------------------
guides_body = """<main>
<article class="reading"><header class="page-intro"><p class="kicker">Guides</p><h1>Guides and references</h1><p class="lead">Background reading to help you reflect well and use the toolkit safely.</p></header>
<section><div class="grid">
<article class="guide-card"><span class="guide-label">Reference</span><h3>Reflective frameworks</h3><p>Plain summaries of the models the toolkit uses: Gibbs, What? So What? Now What?, Kolb, Brookfield's lenses and the DEAL model — and how to choose.</p><div class="actions"><a class="button" href="frameworks.html">Read the frameworks guide</a></div></article>
<article class="guide-card"><span class="guide-label">Safety</span><h3>Anonymisation and confidentiality</h3><p>Why removing a name is rarely enough, what counts as identifying, and how to write about real people responsibly in a reflection.</p><div class="actions"><a class="button" href="anonymisation.html">Read the anonymisation guide</a></div></article>
<article class="guide-card"><span class="guide-label">Approach</span><h3>The teaching approach</h3><p>How the tutor works, why it refuses to ghost-write, and the pedagogy behind the questions it asks.</p><div class="actions"><a class="button" href="teaching-approach.html">Read about the approach</a></div></article>
</div></section></article>
</main>"""
write("guides/index.html", page(f"Guides | {BRAND}", guides_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# GUIDES: FRAMEWORKS
# ---------------------------------------------------------------------------
frameworks_body = """<main>
<article class="reading"><header class="page-intro"><p class="kicker">Reference</p><h1>Reflective frameworks</h1><p class="lead">A reflective framework is a set of prompts that moves you from "what happened" to "what it meant" and "what I will do". No model is compulsory; the best one is the one that helps you think honestly. Here are the models the toolkit supports.</p></header>
<section>
<h2>Gibbs' Reflective Cycle (1988)</h2>
<p>A widely used six-stage cycle, popular where feelings matter and a full structure helps: <strong>Description</strong> (what happened), <strong>Feelings</strong> (what you thought and felt), <strong>Evaluation</strong> (what was good and bad), <strong>Analysis</strong> (why — making sense of it), <strong>Conclusion</strong> (what else you could have done, what you now understand), and <strong>Action Plan</strong> (what you would do next time).</p>
<p class="muted">Best for: detailed reflections where the emotional dimension is important. Watch out for: stopping at evaluation and never reaching analysis.</p>
</section><section>
<h2>What? So What? Now What?</h2>
<p>A compact three-question model, useful for short reflections and fast-paced practice. <strong>What?</strong> describes the situation; <strong>So what?</strong> works out why it mattered and what it means; <strong>Now what?</strong> decides what you will do differently. The framing originates with Borton (1970), was developed as trigger questions by Driscoll (1994), and expanded by Rolfe, Freshwater and Jasper (2001).</p>
<p class="muted">Best for: tight word counts, journals, healthcare reflections. Watch out for: spending too long on "What?" and rushing the other two.</p>
</section><section>
<h2>Kolb's Experiential Learning Cycle (1984)</h2>
<p>A learning-focused cycle: <strong>Concrete Experience</strong> (having the experience), <strong>Reflective Observation</strong> (reviewing it), <strong>Abstract Conceptualisation</strong> (drawing a general lesson or linking to theory), and <strong>Active Experimentation</strong> (trying the new approach). It is strong when you want to connect a specific experience to a general principle.</p>
<p class="muted">Best for: linking practice to theory. Watch out for: jumping to a "lesson" without genuine observation first.</p>
</section><section>
<h2>Brookfield's Four Lenses (1995)</h2>
<p>Rather than stages, Brookfield offers four viewpoints to examine the same experience: your own <strong>autobiographical</strong> view; the <strong>students' or service-users'</strong> eyes; your <strong>colleagues' or peers'</strong> perspectives; and the <strong>theoretical or literature</strong> lens. Looking through all four surfaces assumptions a single viewpoint hides.</p>
<p class="muted">Best for: testing assumptions, teaching and practice reflection. Watch out for: treating it as four boxes rather than genuinely shifting viewpoint.</p>
</section><section>
<h2>The DEAL model (Ash &amp; Clayton, 2009)</h2>
<p>A critical-reflection model common in US higher education and service-learning: <strong>Describe</strong> the experience objectively; <strong>Examine</strong> it across academic, personal and civic categories; and <strong>Articulate Learning</strong> — what you learned, how, why it matters, and what you will do next. It is designed to push beyond surface description toward demonstrable learning.</p>
<p class="muted">Best for: experiential, civic and service-learning in US courses. Watch out for: examining only the personal category and neglecting the academic and civic.</p>
</section><section>
<h2>Choosing a model</h2>
<p>If feelings are central and you have room, Gibbs. If you are short on words, What? So What? Now What?. If you want to connect experience to theory, Kolb. If you want to challenge your assumptions, Brookfield. For US experiential and service-learning, DEAL. If a course or regulator names a model, use that one. The toolkit's <strong>Choose a Model</strong> tool (FW5) can recommend one for your specific task.</p>
<div class="btn-row"><a class="button" href="../tools/reflective-frameworks.html">Frameworks library</a><a class="button secondary" href="../tools/">All tools</a></div>
</section></article>
</main>"""
write("guides/frameworks.html", page(f"Reflective frameworks | {BRAND}", frameworks_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# GUIDES: ANONYMISATION
# ---------------------------------------------------------------------------
anon_body = """<main>
<article class="reading"><header class="page-intro"><p class="kicker">Safety</p><h1>Anonymisation and confidentiality</h1><p class="lead">Reflective reports almost always involve other people. Writing about them honestly while protecting their privacy is a skill in itself — and a professional and legal requirement. This guide explains the essentials. It is general information, not legal advice; always follow your own course, employer and regulator rules.</p></header>
<section class="warning">
<h2>The core message</h2>
<p>Removing someone's name is usually <strong>not</strong> enough to anonymise them. A small set of ordinary details — a date, a place, an age, a role, an unusual condition or event — can together identify a person even with no name at all. Before you write, and again before you share or save, ask: could anyone who was there, or who knows the people involved, work out who this is?</p>
</section><section>
<h2>What can identify someone</h2>
<p>Identifying information is not only names. Watch for combinations of:</p>
<ul class="list-clean">
<li>Dates, shifts or times, and specific locations (ward, school, team, hospital, clinic).</li>
<li>Job titles or roles, especially where few people hold them.</li>
<li>Ages, particularly exact ages of children, or unusual age-plus-condition combinations.</li>
<li>Rare conditions, rare events, or distinctive circumstances.</li>
<li>Bed numbers, case numbers, room numbers, or other reference details.</li>
<li>Your own identifying details, which can locate everyone else by association.</li>
</ul>
<p>The data-protection point is that anonymisation has to be judged on the whole picture. UK guidance and the Information Commissioner's Office treat information as identifying if a person could be singled out from it, directly or indirectly — so stripping the name while leaving the rest is not anonymisation.</p>
</section><section>
<h2>How to write about people safely</h2>
<ul class="list-clean">
<li>Refer to people by role, not name: "a patient", "my practice supervisor", "a colleague", "a pupil".</li>
<li>Generalise specifics: "an older adult" rather than an exact age; "a long-term condition" rather than a rare named one, unless the condition is essential and cannot identify.</li>
<li>Remove dates, shifts, bed and case numbers, and place names unless genuinely necessary.</li>
<li>Keep the focus on <em>your</em> learning and actions, which rarely need identifying detail to make sense.</li>
<li>If a detail is essential to the reflection but identifying, consider whether you can reflect on the same learning using a less specific framing.</li>
</ul>
</section><section>
<h2>Professional context</h2>
<p>In nursing, the NMC requires reflective accounts for revalidation to be written so that no patient, service user, colleague or other person can be identified. In medicine, UK guidance from the Academy of Medical Royal Colleges and others is clear that reflective notes should be anonymised as far as possible and should focus on learning rather than a blow-by-blow record. Across professions, the principle is the same: reflect openly about yourself, protect everyone else.</p>
</section><section class="notice">
<h2>Before you paste anything into an AI tool</h2>
<p>A public AI tool is not a private notebook. Anonymise <em>before</em> you paste, not after. If you are unsure whether a passage is safe, the toolkit's anonymisation tools — <strong>NH4</strong> (NHS &amp; Healthcare) and <strong>MD3</strong> (Medical) — will flag risky details and explain why, so you can fix them before the reflection goes anywhere.</p>
<div class="btn-row"><a class="button" href="../tools/nhs-healthcare.html">NHS anonymisation tool</a><a class="button secondary" href="../tools/medical.html">Medical anonymisation tool</a></div>
</section></article>
</main>"""
write("guides/anonymisation.html", page(f"Anonymisation and confidentiality | {BRAND}", anon_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# GUIDES: TEACHING APPROACH
# ---------------------------------------------------------------------------
teaching_body = """<main>
<article class="reading"><header class="page-intro"><p class="kicker">Approach</p><h1>The teaching approach</h1><p class="lead">Why this toolkit asks questions instead of producing answers, and how each tool is designed to teach rather than to write.</p></header>
<section>
<h2>Writing is thinking</h2>
<p>The value of a reflective report is not the text on the page; it is the understanding you reach by working through your own experience honestly. If something else does that thinking, you get a document but not the learning the document is supposed to represent. So the toolkit's first principle is simple: it helps you reflect; it does not reflect for you.</p>
</section><section>
<h2>What every tool will and will not do</h2>
<p>Each tool runs the same kind of loop: it <strong>diagnoses</strong> where your writing is (often still description), <strong>explains</strong> the move you need to make, shows a <strong>worked example on unrelated content</strong> so you can see the move without copying it, asks you to <strong>attempt</strong> it on your own material, and then <strong>reviews</strong> what you wrote and points to the next step.</p>
<p>It will <strong>not</strong> invent your experiences, your feelings, your insight or your learning, and it will not produce a finished reflection for you to hand in. That boundary is deliberate and applies even if you ask it directly.</p>
</section><section>
<h2>Specialist libraries reduce the quizzing</h2>
<p>General tools have to ask about your context before they can help. Specialist libraries build a standard in — NMC revalidation, UK medical reflective practice, the US DEAL model — so the tutor already knows the shape of what you are writing and the rules it must respect. That means fewer setup questions and faster, more relevant help, while the no-ghost-writing rule stays exactly the same.</p>
</section><section>
<h2>Honesty, not performance</h2>
<p>Reflective writing is sometimes assessed, which tempts people to perform insight rather than have it. The tutor pushes the other way: it values a small, true, specific realisation over an impressive-sounding general one, and it will gently call out conclusions that could have been written about any situation.</p>
</section><section>
<h2>Care and limits</h2>
<p>Reflection can touch on difficult experiences. The tutor keeps a supportive, non-judgemental tone, lets you set the pace, and offers a smaller next step whenever you say you are stuck. It is a writing tutor, not a counsellor or a regulator: it cannot guarantee anonymity, replace your supervisor's guidance, or make a professional judgement for you. Its job is to make the honest, thoughtful path the easy one.</p>
<div class="btn-row"><a class="button" href="../tools/">Browse the tools</a><a class="button secondary" href="../student-help/">Student help</a></div>
</section></article>
</main>"""
write("guides/teaching-approach.html", page(f"The teaching approach | {BRAND}", teaching_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# CHANGELOG
# ---------------------------------------------------------------------------
changelog_body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Changelog</p><h1>Version history</h1><p class="lead">A record of releases of the Reflective Report Writing Tutor toolkit.</p></header>
<section>
<h2>v{VERSION} &mdash; {LAST_UPDATED}</h2>
<p>First public release.</p>
<ul class="list-clean">
<li>Two general libraries: Reflective Foundations and Reflective Frameworks.</li>
<li>Three specialist libraries: NHS &amp; Healthcare (NMC), Medical (GMC / AoMRC), and US &amp; Academic (DEAL).</li>
<li>Thirty tools in total, plus a combined master library.</li>
<li>Strengthened no-ghost-writing rule: the tutor never invents the writer's experience, feelings, insight or learning.</li>
<li>Anonymisation and confidentiality checks built into the healthcare and medical libraries, with a dedicated safety guide.</li>
<li>Worked example pages for every tool, shown as chat transcripts using a separate chat stylesheet.</li>
<li>File-based prompt source under <code>src/</code>: one Markdown file per tool, with pack manifests compiled by the build script.</li>
</ul>
<p class="small-note">Downloads: <a href="../{PL}/reflective_writing_tutor_mini_libraries.zip" download>all mini libraries (zip)</a> &middot; <a href="../{PL}/reflective_writing_tutor_master_library.md" download>master library</a>.</p>
</section></article>
</main>"""
write("changelog/index.html", page(f"Changelog | {BRAND}", changelog_body, base="../", body_class="reference"))

# ---------------------------------------------------------------------------
# .nojekyll
# ---------------------------------------------------------------------------
with open(os.path.join(DOCS, ".nojekyll"), "w", encoding="utf-8") as f:
    f.write("")
print("wrote .nojekyll")

print("pages done")
