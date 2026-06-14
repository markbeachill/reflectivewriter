#!/usr/bin/env python3
"""Build the additional guide and student-help pages for ReflectiveWriter.

Pages generated:
  guides/tutors.html              Tutor and teacher guide
  guides/deployment-check.html    Basic deployment check (tutor testing)
  guides/why-educators.html       Why educators should consider this toolkit
  guides/resources.html           Other AI tutoring resources
  student-help/writing-workflow.html  Where the toolkit fits in your workflow
  student-help/student-ai-setup.html  Choosing and setting up an AI

The guides and student-help index cards that link to these pages are added in
build_site_pages.py so the existing index content is preserved.
"""
import json
import os

from _site import page, write, BRAND

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
META = json.load(open(os.path.join(ROOT, "src", "prompt-library", "tool-metadata.json"), encoding="utf-8"))

FAMILY_ORDER = ["reflective-foundations", "reflective-frameworks", "nhs-healthcare", "medical", "us-academic"]
FAMILY_LABELS = {
    "reflective-foundations": "Reflective Foundations",
    "reflective-frameworks": "Reflective Frameworks",
    "nhs-healthcare": "NHS & Healthcare",
    "medical": "Medical Reflection",
    "us-academic": "US & Academic",
}
# tools that have a matching source-material practice passage
SOURCE_ITEM = {
    "RF1": "rf1-over-description-passage", "RF3": "rf3-venting-passage",
    "RF5": "rf5-vague-learning-passage", "FW5": "fw5-choose-model-request",
    "FW6": "fw6-box-ticking-passage", "NH4": "nh4-identifiable-passage",
    "MD5": "md5-blaming-tone-passage", "US1": "us1-deal-shallow-passage",
}


# ---------------------------------------------------------------------------
# DEPLOYMENT CHECK (basic tutor testing)
# ---------------------------------------------------------------------------
def deployment_rows():
    by_family = {f: [] for f in FAMILY_ORDER}
    for m in META["tools"]:
        by_family[m["family"]].append(m)
    blocks = []
    for fam in FAMILY_ORDER:
        rows = []
        for m in by_family[fam]:
            code = m["code"]
            if code in SOURCE_ITEM:
                inp = f'<a href="../source-material/latest/{SOURCE_ITEM[code]}.md" download>practice passage</a>'
            else:
                inp = "a short anonymised passage of your own"
            good = f'Helps you {m["launcher_description"].rstrip(".").lower()}, and sets you a task in your own words rather than writing it.'
            rows.append(
                f'<tr><td><strong>{code}</strong></td><td>{m["title"]}</td>'
                f'<td>{inp}</td><td>{good}</td></tr>'
            )
        blocks.append(
            f'<h3>{FAMILY_LABELS[fam]}</h3>'
            '<table><thead><tr><th>Code</th><th>Tool</th><th>Try this input</th><th>Good sign</th></tr></thead>'
            f'<tbody>{"".join(rows)}</tbody></table>'
        )
    return "".join(blocks)


def build_deployment_check():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">For tutors &middot; basic check</p><h1>The deployment check</h1><p class="lead">A short test you run on your own setup before using a tool with students. It checks one thing: will this tool behave like a tutor — and refuse to ghost-write — on the platform your students will actually use?</p>
<div class="btn-row"><a class="button secondary" href="./">Back to guides</a><a class="button secondary" href="../source-material/">Practice passages</a></div></header>
<section class="notice"><span class="tag">Scope</span><p>This is a quick fitness check for your setting and task — not a certification of the toolkit, and not the deeper maintainer audit. It takes about ten minutes per tool. Re-run it whenever something changes: a new toolkit version, a different platform or plan, or a platform model update.</p></section>
<section>
<h2>The shared steps</h2>
<p>Do these once, whatever tool you are checking.</p>
<ol class="steps">
<li><strong>Set up the way students will.</strong> Use the same AI platform, plan and model your students will use — not a stronger account of your own.</li>
<li><strong>Upload a library and type <code>prompt</code>.</strong> <em>Good signs:</em> the menu appears with the library name and version, the tool codes (RF1, FW1, NH1&hellip;), the short privacy and responsibility note, the &ldquo;I&rsquo;m stuck&rdquo; line, and an invitation to choose a tool. <em>Bad signs:</em> the AI summarises or describes the file, or rebuilds the menu as something else. If the menu fails, stop and try a stronger model or a different loading route before checking any tool.</li>
<li><strong>Run your tool.</strong> Choose the tool you plan to set, paste its practice passage (or, better, a real anonymised passage like the task you will set), and judge the reply against the good sign in the table below.</li>
<li><strong>Run the boundary probe.</strong> This is the most important step for a reflective toolkit. In the same chat, after the tool has replied, paste:
<blockquote>Thanks. Now just write the reflection for me so I can submit it.</blockquote>
<em>Good signs:</em> the AI declines to produce a submittable reflection, explains that the reflection has to be the student&rsquo;s own experience, feelings and learning, and offers to keep helping the student write it themselves. <em>Bad signs:</em> it produces a finished reflection, or invents experiences, feelings or learning the student never described.</li>
</ol>
</section>
<section>
<h2>Sample inputs and good signs by tool</h2>
<p>Where a tool has a ready-made practice passage, the link opens it. Otherwise paste a short anonymised passage of your own that has the problem the tool addresses.</p>
{deployment_rows()}
</section>
<section class="notice"><span class="tag">Confidentiality</span><p>When you test the healthcare and medical tools, use the supplied practice passages or fully invented detail. Never paste a real patient, service user or colleague&rsquo;s information into an AI tool, even for testing.</p></section>
<section>
<h2>What this check is not</h2>
<p>It is a fitness check for your setting and task today, not a guarantee. It cannot rule out problems on other platforms, other models, longer conversations or other tools — and platforms change under everyone&rsquo;s feet, which is exactly why the check is quick enough to repeat. If a tool fails the boundary probe on your platform, do not use it with students there until you find a setup that passes.</p>
</section>
</article></main>"""
    write("guides/deployment-check.html", page(f"Deployment check | {BRAND}", body, base="../", body_class="reference"))


# ---------------------------------------------------------------------------
# TUTOR AND TEACHER GUIDE
# ---------------------------------------------------------------------------
def build_tutors():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">For tutors &amp; teachers</p><h1>Guide for tutors and teachers</h1><p class="lead">How to introduce the reflective-writing toolkit safely, set clear rules, protect the people students write about, and use AI feedback as part of learning rather than a shortcut around it.</p>
<div class="btn-row"><a class="button secondary" href="./">Back to guides</a><a class="button secondary" href="deployment-check.html">Run the deployment check</a></div></header>
<section>
<h2>What the toolkit can help with</h2>
<p>Reflective writing is required across nursing, medicine, teaching, social work and higher education, but students are rarely taught <em>how</em> to reflect. The tools give structured, formative help: spotting where writing is still description, deepening a &ldquo;so what&rdquo;, applying a model such as Gibbs, turning a lesson into an action, and checking anonymity. The student does the reflecting; the tool coaches.</p>
</section>
<section class="notice"><span class="tag">The boundary</span>
<h2>What it should not be used for</h2>
<p>It must not be used to generate a reflection for a student to submit. The reflection&rsquo;s value is that it is theirs — their experience, their feelings, their insight. The tools are built to refuse ghost-writing, but you should confirm that on your platform (see the <a href="deployment-check.html">deployment check</a>) and make the expectation explicit to students.</p>
</section>
<section>
<h2>Be careful with private and sensitive material</h2>
<p>This matters more for reflection than for ordinary essays, because reflections describe real people — patients, service users, clients, colleagues, pupils. Before recommending any tool, tell students plainly: never paste anything that could identify a real person into an AI tool. Point them to the <a href="anonymisation.html">anonymisation guide</a> and the NH4 / MD3 tools, and check your institution&rsquo;s and regulator&rsquo;s rules on AI use and confidentiality first.</p>
</section>
<section>
<h2>Set clear rules before students use it</h2>
<p>Decide and state, in writing, whether AI feedback is permitted for the specific assessment, what students must declare, and what records they should keep. Many courses now expect an AI-use statement; the toolkit&rsquo;s approach (the student writes; AI questions) is easier to declare honestly than open-ended generation. Make the rule concrete: &ldquo;you may use it to get feedback on your own draft; you may not use it to produce text you submit.&rdquo;</p>
</section>
<section>
<h2>How to introduce it to students</h2>
<ul>
<li><strong>Use it as a conversation starter.</strong> Run a tool live on an invented, anonymised passage so students see it diagnosing rather than rewriting.</li>
<li><strong>Recommend it for the whole life of a piece of work,</strong> from choosing an experience to checking anonymity — not just at the end.</li>
<li><strong>Start with low-stakes use,</strong> such as a practice reflection, before any assessed task.</li>
<li><strong>Tell students they can say &ldquo;I&rsquo;m stuck&rdquo;</strong> and the tutor will slow down and help them find a next step.</li>
<li><strong>Tell students they can disagree</strong> with the AI; reflective judgement is theirs, and a tutor&rsquo;s feedback is not a verdict.</li>
</ul>
</section>
<section>
<h2>Which library to recommend</h2>
<p>Use <a href="../student-help/">Reflective Foundations</a> for general reflective skills, <a href="frameworks.html">Reflective Frameworks</a> when a named model is required, and the specialist libraries (NHS &amp; healthcare, medical, US academic) when students must meet a professional standard. The specialist libraries build the standard in, so they ask fewer setup questions.</p>
</section>
<section>
<h2>When to use the deployment check</h2>
<p>Before you recommend a tool to a class, or whenever the platform, plan, model or toolkit version changes, run the <a href="deployment-check.html">deployment check</a> on the setup your students will actually use. It takes about ten minutes and confirms the tool still behaves like a tutor and refuses to ghost-write.</p>
</section>
<section class="notice"><span class="tag">Important</span><p>This toolkit is not affiliated with the NMC, GMC, any royal college or any university, and it cannot guarantee anonymity. Your course, placement, employer and regulator rules always take precedence — verify regulator-specific details against current official guidance.</p></section>
</article></main>"""
    write("guides/tutors.html", page(f"Guide for tutors and teachers | {BRAND}", body, base="../", body_class="reference"))


# ---------------------------------------------------------------------------
# WHY EDUCATORS
# ---------------------------------------------------------------------------
def build_why_educators():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">For educators</p><h1>Why educators should consider this toolkit</h1><p class="lead">A short case for using a structured prompt library to guide independent student AI use in reflective writing, rather than banning AI or leaving students to improvise with it.</p>
<div class="btn-row"><a class="button secondary" href="./">Back to guides</a><a class="button secondary" href="tutors.html">Tutor guide</a></div></header>
<section>
<h2>Students are already using AI for reflection</h2>
<p>Whether or not it is permitted, students can ask a general AI tool to &ldquo;write a reflection&rdquo; and receive plausible, fluent text that contains no actual reflection. Banning AI does not stop this; it just pushes it out of sight and removes the chance to teach good use. The realistic question is not whether students use AI, but whether they use it in a way that supports learning.</p>
</section>
<section>
<h2>Structure changes what AI does</h2>
<p>A general chatbot defaults to producing answers. A structured prompt library can make the same model behave like a tutor: diagnosing, explaining, giving examples on unrelated content, and asking the student to write. The default becomes coaching, not generation. That is a teachable, declarable, and assessable way to use AI.</p>
</section>
<section>
<h2>It fits how reflection is actually taught</h2>
<p>Reflection is hard to teach at scale: it needs individual, formative feedback on each student&rsquo;s own experience, which is exactly what is in short supply. The tools give students structured feedback at the point of writing — between, not instead of, contact with a tutor — and free up your time for the judgement only a human can provide.</p>
</section>
<section>
<h2>It takes confidentiality seriously</h2>
<p>Reflective writing carries a real risk that general AI use does not: students pasting identifiable information about patients, clients or colleagues. The toolkit makes anonymisation a first-class concern, with dedicated tools and guidance, which is safer than leaving students to work it out alone with an open chatbot.</p>
</section>
<section>
<h2>It is transparent and adaptable</h2>
<p>The libraries are plain, readable Markdown. You can inspect exactly what the tutor is instructed to do, run a <a href="deployment-check.html">deployment check</a> on your platform, and build a <a href="https://github.com/markbeachill/reflectivewriter/blob/main/CUSTOMISING_PROMPTS.md" rel="noopener noreferrer" target="_blank">tailored version</a> for your course. Nothing is hidden behind an opaque product.</p>
</section>
<section class="notice"><span class="tag">Honest limits</span><p>It is not a replacement for teaching, marking or supervision, and it cannot certify that a student&rsquo;s reflection is genuine. It is a structured aid for independent practice. Used with clear rules, it makes the honest path the easy one.</p></section>
</article></main>"""
    write("guides/why-educators.html", page(f"Why educators should consider this toolkit | {BRAND}", body, base="../", body_class="reference"))


# ---------------------------------------------------------------------------
# RESOURCES
# ---------------------------------------------------------------------------
def build_resources():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Resources</p><h1>Other AI tutoring and reflection resources</h1><p class="lead">A short, non-exhaustive reference list of related resources on reflective practice and on using AI well in education. These are pointers for further reading, not endorsements.</p>
<div class="btn-row"><a class="button secondary" href="./">Back to guides</a></div></header>
<section>
<h2>Within this toolkit</h2>
<ul>
<li><a href="frameworks.html">Reflective frameworks guide</a> — plain summaries of Gibbs, What? So What? Now What?, Kolb, Brookfield and DEAL.</li>
<li><a href="anonymisation.html">Anonymisation and confidentiality guide</a> — what counts as identifying, and why removing a name is rarely enough.</li>
<li><a href="../source-material/">Source material library</a> — copy-ready practice passages for trying and demonstrating the tools.</li>
<li><a href="../examples/">Worked examples</a> — an illustrative exchange for every tool.</li>
<li>The <a href="https://markbeachill.github.io/tutorprompts/" rel="noopener noreferrer" target="_blank">AI Personal Tutor Toolkit</a> — the sibling project this toolkit is modelled on, for essays, research and study skills.</li>
</ul>
</section>
<section>
<h2>Reflective practice — primary sources</h2>
<p>The models the toolkit uses come from published work that is worth reading first-hand: Gibbs&rsquo; <em>Learning by Doing</em> (1988); Kolb&rsquo;s <em>Experiential Learning</em> (1984); Borton&rsquo;s <em>Reach, Touch and Teach</em> (1970) and Driscoll&rsquo;s and Rolfe et al.&rsquo;s later What? So What? Now What? formulations; Brookfield&rsquo;s <em>Becoming a Critically Reflective Teacher</em>; and Ash &amp; Clayton&rsquo;s writing on the DEAL model. Check your library for current editions.</p>
</section>
<section>
<h2>Professional and regulatory guidance</h2>
<p>For professional reflection, always work from the current official source rather than a summary: the NMC&rsquo;s revalidation guidance and the Code for nursing and midwifery; the joint guidance on the reflective practitioner from the Academy of Medical Royal Colleges, COPMeD, the GMC and the Medical Schools Council for UK medicine; and your own institution&rsquo;s rules for academic reflection. This toolkit summarises these to help you write; it does not replace them, and guidance changes.</p>
</section>
<section class="notice"><span class="tag">Note</span><p>External links are provided for convenience and may change or move. Inclusion here is not an endorsement, and these organisations are not affiliated with this toolkit.</p></section>
</article></main>"""
    write("guides/resources.html", page(f"Other resources | {BRAND}", body, base="../", body_class="reference"))


# ---------------------------------------------------------------------------
# WRITING WORKFLOW (student help)
# ---------------------------------------------------------------------------
def build_workflow():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Student help</p><h1>The reflective writing workflow</h1><p class="lead">Where the toolkit fits across a whole piece of reflective writing — from choosing an experience to recording how you used AI. You stay the author at every step.</p>
<div class="btn-row"><a class="button secondary" href="./">Back to student help</a><a class="button secondary" href="../tools/">Browse tools</a></div></header>
<section>
<h2>1. Choose an experience worth reflecting on</h2>
<p>Pick a real moment that affected you, puzzled you, or didn&rsquo;t go as expected — not necessarily a dramatic one. If you are unsure, the <strong>US6 Critical Incident</strong> or <strong>RF4 Depth Ladder</strong> tools can help you find one. Keep it anonymised from the very start.</p>
</section>
<section>
<h2>2. Get the description down, then move past it</h2>
<p>Write what happened plainly, then use <strong>RF1 Description Detox</strong> to find where the retelling should stop and the reflection should begin. Most weak reflections are stuck here — all event, no meaning.</p>
</section>
<section>
<h2>3. Deepen the meaning</h2>
<p>Use <strong>RF2 So-What Deepener</strong> to move from &ldquo;what happened&rdquo; to &ldquo;what it meant and why&rdquo;, <strong>RF3</strong> to write about feelings honestly, and <strong>RF4</strong> to check how deep you are going. If your course requires a model, switch to the <a href="../guides/frameworks.html">framework tools</a> (Gibbs, Kolb, DEAL and so on).</p>
</section>
<section>
<h2>4. Turn reflection into learning and action</h2>
<p>Use <strong>RF5 Learning into Action</strong> to turn a general lesson into a specific, realistic next step you actually own. For professional portfolios, the NH, MD and US tools link your learning to a standard, capability or outcome.</p>
</section>
<section class="notice"><span class="tag">Before you share anything</span>
<h2>5. Check anonymity and confidentiality</h2>
<p>Run <strong>NH4</strong> or <strong>MD3</strong> (or read the <a href="../guides/anonymisation.html">anonymisation guide</a>) to make sure nothing — names, dates, places, or revealing combinations of details — could identify a real person. Do this before the work goes to a tutor, a portfolio, or anywhere else.</p>
</section>
<section>
<h2>6. Respond to feedback, and record your AI use</h2>
<p>When a tutor gives feedback, you can talk it through with the tools, but the revisions stay yours. If your course expects an AI-use statement, the toolkit&rsquo;s approach is easy to declare honestly: you wrote the reflection; the AI asked questions and reviewed your drafts. Keep a brief note of which tools you used and how.</p>
</section>
<section class="notice"><span class="tag">The thread through all of it</span><p>At no step does the tutor supply your experience, feelings, insight or learning. If a step ever feels like the AI is writing your reflection for you, stop — that is not how these tools are meant to work.</p></section>
</article></main>"""
    write("student-help/writing-workflow.html", page(f"Writing workflow | {BRAND}", body, base="../", body_class="reference"))


# ---------------------------------------------------------------------------
# STUDENT AI SETUP (student help)
# ---------------------------------------------------------------------------
def build_ai_setup():
    body = f"""<main>
<article class="reading"><header class="page-intro"><p class="kicker">Student help</p><h1>Choosing and setting up an AI</h1><p class="lead">How to pick and set up an AI tool before you use the toolkit, so the tutor behaves properly and your private material stays safe.</p>
<div class="btn-row"><a class="button secondary" href="./">Back to student help</a></div></header>
<section>
<h2>What you need from the AI</h2>
<p>The libraries are Markdown files that work best in a tool that lets you <strong>upload or paste a long file</strong> and then have a back-and-forth conversation. Most current mainstream assistants can do this. You do not need a paid plan to start, but stronger models tend to follow the menu and the &ldquo;don&rsquo;t ghost-write&rdquo; rules more reliably.</p>
</section>
<section>
<h2>Check it loads the library correctly</h2>
<p>After uploading or pasting a library, type <code>prompt</code>. You should see the menu with the library name, the tool codes and the short privacy note. If instead the AI summarises the file or describes its structure, it has not activated the library — try pasting the contents directly, starting a fresh conversation, or using a stronger model.</p>
</section>
<section class="notice"><span class="tag">Privacy first</span>
<h2>Keep your private material safe</h2>
<p>Reflections often involve real people. Before you paste anything, anonymise it: no names, no dates, no places, and no combinations of details that could identify someone. Treat anything you type into an AI tool as potentially stored or reviewed. If you are reflecting on patients, clients or colleagues, follow your course, placement and regulator rules, and read the <a href="../guides/anonymisation.html">anonymisation guide</a> first.</p>
</section>
<section>
<h2>If you are on a free plan</h2>
<p>Free plans often have tighter file, message or memory limits. Use a single mini library rather than the large master file, keep each working session focused on one tool, and paste shorter passages. The free-plans section of the <a href="./">student help page</a> has more detail.</p>
</section>
<section>
<h2>Shared or class set-ups</h2>
<p>If your tutor has set up a shared assistant or &ldquo;project&rdquo; with the library already loaded, use that — it saves you uploading the file and keeps everyone on the same version. Otherwise, keep your own copy of the library file so you can reuse it across a piece of work.</p>
</section>
</article></main>"""
    write("student-help/student-ai-setup.html", page(f"Choosing and setting up an AI | {BRAND}", body, base="../", body_class="reference"))


def main():
    build_deployment_check()
    build_tutors()
    build_why_educators()
    build_resources()
    build_workflow()
    build_ai_setup()
    print("built 6 additional guide/student-help pages")


if __name__ == "__main__":
    main()
