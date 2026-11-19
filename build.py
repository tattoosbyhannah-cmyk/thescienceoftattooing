#!/usr/bin/env python3
"""Builds the static thescienceoftattooing.com site into ./public.
Edit the CONFIG and page content below, then run: python3 build.py"""
import json, os, html, datetime

# ---------------- CONFIG ----------------
SITE = "https://www.thescienceoftattooing.com"
APP_URL = "https://the-science-of-tattooing-dfec8.web.app/"   # change if the app moves to app.thescienceoftattooing.com
AMAZON_URL = "https://www.amazon.com/dp/B0838N9L43"
EMAIL = "thescienceoftattooing@gmail.com"
FACEBOOK = "https://www.facebook.com/thescienceoftattooing"
YOUTUBE_ID = "8qkqU4m7kkY"
FOUNDER = "Hannah Wolf"
TODAY = datetime.date.today().isoformat()
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public")

LOGO_SVG = ('<svg viewBox="0 0 40 40" aria-hidden="true"><g stroke="#ff5610" stroke-width="3" stroke-linecap="round">'
            '<line x1="20" y1="22" x2="32" y2="9"/><line x1="20" y1="22" x2="8" y2="15"/><line x1="20" y1="22" x2="27" y2="34"/></g>'
            '<g fill="#ff5610"><circle cx="20" cy="22" r="7"/><circle cx="32" cy="9" r="4.5"/><circle cx="8" cy="15" r="3.5"/><circle cx="27" cy="34" r="3.5"/></g></svg>')

NAV = [("/ink/", "Ink ingredients"), ("/book/", "Book"), ("/app/", "App"), ("/regulators/", "For regulators"), ("/about/", "About"), ("/contact/", "Contact")]

ORG = {
    "@type": "EducationalOrganization", "@id": SITE + "/#org", "name": "The Science of Tattooing",
    "url": SITE + "/", "logo": SITE + "/icon-512.png", "email": EMAIL, "foundingDate": "2018",
    "founder": {"@id": SITE + "/#founder"}, "sameAs": [FACEBOOK],
    "description": "Education on the science of tattooing: tattoo ink chemistry, skin physiology, complications and safety, for artists, clients and regulators.",
}
FOUNDER_LD = {"@type": "Person", "@id": SITE + "/#founder", "name": FOUNDER, "jobTitle": "Tattoo artist, educator and author",
              "url": SITE + "/about/", "worksFor": {"@id": SITE + "/#org"}}


def page(path, title, desc, body, ld=None, crumbs=None, og_type="website"):
    url = SITE + path
    graph = [ORG]
    if path == "/":
        graph += [{"@type": "WebSite", "@id": SITE + "/#site", "url": SITE + "/", "name": "The Science of Tattooing",
                   "publisher": {"@id": SITE + "/#org"}, "inLanguage": "en-US"}, FOUNDER_LD]
    if crumbs:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
            {"@type": "ListItem", "position": 2, "name": crumbs, "item": url}]})
    graph += ld or []
    navhtml = "".join(f'<a href="{h}"{" aria-current=page" if h == path else ""}>{t}</a>' for h, t in NAV)
    crumb_html = f'<nav class="wrap crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / {html.escape(crumbs)}</nav>' if crumbs else ""
    doc = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#f6f3ec" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#14130f" media="(prefers-color-scheme: dark)">
<meta property="og:site_name" content="The Science of Tattooing">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/og-image.png">
<meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{SITE}/og-image.png">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/icon-512.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@800&family=IBM+Plex+Mono:wght@500&family=IBM+Plex+Sans:wght@400;500&display=swap">
<link rel="stylesheet" href="/styles.css">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="wrap">
<a class="brand" href="/" aria-label="The Science of Tattooing — home">{LOGO_SVG}<span>The Science of Tattooing</span></a>
<nav class="nav" aria-label="Main">{navhtml}<a class="btn btn-app" href="{APP_URL}" rel="noopener">Play the app</a></nav>
</div></header>
{crumb_html}
<main id="main">
{body}
</main>
<footer class="site-footer"><div class="wrap">
<div class="foot-grid">
<div><h2>The Science of Tattooing</h2><p>Shedding light on the mysterious side of tattooing. Founded in 2018 by tattoo artist {FOUNDER}.</p>
<a class="btn btn-app" href="{APP_URL}" rel="noopener">Play the app</a></div>
<div><h2>Explore</h2><ul>
<li><a href="/book/">The book</a></li><li><a href="/app/">The learning app</a></li>
<li><a href="/regulators/">For regulators</a></li><li><a href="/about/">About</a></li></ul></div>
<div><h2>Connect</h2><ul>
<li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{FACEBOOK}" rel="noopener">Facebook</a></li>
<li><a href="{AMAZON_URL}" rel="noopener">Book on Amazon</a></li></ul></div>
</div>
<p class="fine">© {datetime.date.today().year} The Science of Tattooing. Educational content only — not medical or legal advice.</p>
</div></footer>
<script>
document.querySelectorAll('.video button').forEach(b=>b.addEventListener('click',()=>{{
 const f=document.createElement('iframe');f.src='https://www.youtube-nocookie.com/embed/'+b.dataset.id+'?autoplay=1';
 f.title=b.dataset.title;f.allow='autoplay; encrypted-media; picture-in-picture';f.allowFullscreen=true;b.replaceWith(f);}}));
</script>
</body>
</html>
"""
    dest = os.path.join(OUT, path.strip("/"), "index.html") if path != "/" else os.path.join(OUT, "index.html")
    if path.endswith(".html"):
        dest = os.path.join(OUT, path.strip("/"))
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(doc)


SUBJECTS = [("01", "Ph", "Physiology", "c1"), ("02", "Ch", "Chemistry", "c2"), ("03", "Co", "Complications", ""),
            ("04", "Hi", "History", ""), ("05", "Py", "Physics", "c3"), ("06", "So", "Sociology", "")]
ELEMENTS = '<div class="elements" role="list" aria-label="Six subjects in the app">' + "".join(
    f'<div class="el {c}" role="listitem"><span class="n">{n}</span><span class="sym" aria-hidden="true">{s}</span><span class="nm">{nm}</span></div>'
    for n, s, nm, c in SUBJECTS) + "</div>"

VIDEO = f'''<div class="video"><button data-id="{YOUTUBE_ID}" data-title="The Science of Tattooing video" aria-label="Play video: The Science of Tattooing">
<img src="https://i.ytimg.com/vi/{YOUTUBE_ID}/hqdefault.jpg" alt="Video thumbnail for The Science of Tattooing" loading="lazy" width="480" height="360"><span class="play">▶ Watch now</span></button></div>'''

BOOK_COVER = ('<picture><source srcset="/images/the-science-of-tattooing-book-cover.webp" type="image/webp">'
              '<img class="book-img" src="/images/the-science-of-tattooing-book-cover.jpg" width="600" height="900" loading="lazy" '
              f'alt="Cover of The Science of Tattooing by {FOUNDER}: an artist sketching anatomical tattoo designs, with the title on an orange band"></picture>')

FAQ = [
    ("What is in tattoo ink?", "Tattoo ink is a suspension of pigments (the particles that create color) in a carrier liquid, often with additives such as binders, thickeners and preservatives. Pigments may be organic or inorganic, and formulations vary widely by brand. The book and app explain each component and why it matters."),
    ("Do I need to download the app?", "No. The Science of Tattooing app runs in your web browser. Open it on any phone or computer and start a lesson right away — no download required."),
    ("Who is The Science of Tattooing for?", "Tattoo artists and apprentices who want a scientific foundation for their craft, clients and collectors who want to understand what goes into their skin, and regulators and lawmakers who write and enforce tattoo safety rules."),
    ("Is this medical advice?", "No. The Science of Tattooing shares published research and fundamentals for education. For a specific medical condition, talk with a physician before getting tattooed."),
    ("How does laser tattoo removal work?", "Laser removal delivers very short pulses of light that shatter ink particles into smaller fragments, which the body's immune system then gradually clears. The book covers the physics and physiology behind it."),
]
FAQ_HTML = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in FAQ)
FAQ_LD = {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}

APP_LD = {"@type": "WebApplication", "@id": SITE + "/app/#app", "name": "The Science of Tattooing app", "url": APP_URL,
          "applicationCategory": "EducationalApplication", "operatingSystem": "Any (web browser)",
          "description": "Gamified tattoo-science lessons and quizzes across physiology, chemistry, complications, history, physics and sociology.",
          "publisher": {"@id": SITE + "/#org"}, "educationalUse": "Self-study", "inLanguage": "en"}
BOOK_LD = {"@type": "Book", "@id": SITE + "/book/#book", "name": "The Science of Tattooing", "author": {"@id": SITE + "/#founder"},
           "publisher": {"@id": SITE + "/#org"}, "bookEdition": "First edition", "image": SITE + "/images/the-science-of-tattooing-book-cover.jpg", "datePublished": "2020", "inLanguage": "en",
           "about": ["Tattoo ink", "Tattooing", "Skin physiology", "Laser tattoo removal"], "url": SITE + "/book/",
           "sameAs": [AMAZON_URL],
           "description": "A fundamental-level guide to the science of tattooing: chemistry, physiology and medical topics including tattoo ink ingredients, laser removal and pain."}

# ---------------- PAGES ----------------
page("/", "The Science of Tattooing — Tattoo Ink, Skin & Safety Education",
     "Learn the science behind tattooing: what's in tattoo ink, how skin heals, laser removal and safety. Read the book and play the web learning app.",
     f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="label">Tattoo education · Est. 2018</span>
<h1>The science behind every tattoo</h1>
<p class="lead">What's in tattoo ink? How does skin heal around pigment? How does laser removal work? We make the research behind tattooing clear for artists, clients and regulators. <a href="/ink/">Start with what's in tattoo ink</a>.</p>
<div class="actions"><a class="btn btn-app" href="{APP_URL}" rel="noopener">Play the learning app</a><a class="btn btn-ghost" href="/book/">Get the book</a></div></div>
{ELEMENTS}
</div></section>

<section class="band"><div class="wrap">
<span class="label">Who it's for</span><h2>One body of knowledge, three audiences</h2>
<div class="grid grid-3" style="margin-top:var(--s4)">
<article class="card"><span class="label">01 · Artists</span><h3>Tattoo artists &amp; apprentices</h3><p>Ground your craft in chemistry, skin physiology and infection control — knowledge most apprenticeships skip.</p><a href="/app/">Start learning</a></article>
<article class="card"><span class="label">02 · Clients</span><h3>Clients &amp; collectors</h3><p>Understand what goes into your skin, how healing works and what questions to ask before your next session.</p><a href="/book/">Read the book</a></article>
<article class="card"><span class="label">03 · Regulators</span><h3>Regulators &amp; lawmakers</h3><p>Evidence-based context for tattoo safety rules, offered in a cooperative spirit.</p><a href="/regulators/">Work with us</a></article>
</div></div></section>

<section><div class="wrap split">
<div><span class="label">The app</span><h2>Gamified tattoo science you can play in a browser</h2>
<p>183 lessons across six subjects — physiology, chemistry, complications, history, physics and sociology — with quizzes and awards that keep you coming back.</p>
<ul class="stats"><li><b>183</b><span>lessons</span></li><li><b>6</b><span>subjects</span></li><li><b>0</b><span>downloads needed</span></li></ul>
<div class="actions"><a class="btn btn-app" href="{APP_URL}" rel="noopener">Play now</a><a class="btn btn-ghost" href="/app/">What's inside</a></div></div>
{VIDEO}
</div></section>

<section class="band"><div class="wrap split">
{BOOK_COVER}
<div><span class="label">The book</span><h2>The Science of Tattooing, first edition</h2>
<p>A comprehensive guide to the fundamental scientific terms behind tattooing — chemistry, physiology and medical topics. It answers questions like what's in tattoo ink, how laser removal works and what pain actually is.</p>
<p>Written by veteran tattoo artist {FOUNDER} with input from PhDs and MDs. Every purchase funds the project.</p>
<div class="actions"><a class="btn btn-primary" href="{AMAZON_URL}" rel="noopener">Buy on Amazon</a><a class="btn btn-ghost" href="/book/">About the book</a></div></div>
</div></section>

<section><div class="wrap">
<span class="label">Questions</span><h2>Frequently asked questions</h2>
<div class="prose" style="margin-top:var(--s4)">{FAQ_HTML}</div>
</div></section>

<section class="band"><div class="wrap split">
<blockquote>“Great things are done by a series of small things brought together.”<cite>Vincent van Gogh</cite></blockquote>
<div><h2>Get in touch</h2><p>Questions about the book, the app, speaking or regulatory education? We'd love to hear from you.</p>
<a class="btn btn-primary" href="mailto:{EMAIL}">Email us</a></div>
</div></section>
''', ld=[FAQ_LD, APP_LD, BOOK_LD])

page("/book/", "The Science of Tattooing Book — Tattoo Ink Chemistry & Skin Science",
     "The Science of Tattooing book explains tattoo ink ingredients, skin physiology, laser removal and pain in plain language. By tattoo artist Hannah Wolf. Buy on Amazon.",
     f'''
<section class="hero"><div class="wrap split">
<div><span class="label">The book · First edition</span><h1>The Science of Tattooing</h1>
<p class="lead">A fundamental-level guide to the chemistry, physiology and medicine behind tattooing — written by a tattoo artist, reviewed with scientists.</p>
<div class="actions"><a class="btn btn-primary" href="{AMAZON_URL}" rel="noopener">Buy on Amazon</a><a class="btn btn-app" href="{APP_URL}" rel="noopener">Practice in the app</a></div></div>
{BOOK_COVER}
</div></section>
<section class="band"><div class="wrap">
<span class="label">Inside</span><h2>Questions the book answers</h2>
<div class="grid grid-3" style="margin-top:var(--s4)">
<article class="card"><span class="label">Chemistry</span><h3>What's in tattoo ink?</h3><p>Pigments, carriers and additives — what each one does and why formulations differ.</p></article>
<article class="card"><span class="label">Physics</span><h3>How does laser removal work?</h3><p>How light pulses fragment pigment and how the body clears what's left.</p></article>
<article class="card"><span class="label">Physiology</span><h3>What is pain?</h3><p>How skin and nerves respond to the needle, and what healing looks like underneath.</p></article>
</div></div></section>
<section><div class="wrap prose">
<h2>Why this book exists</h2>
<p>In 2017, tattoo artist {FOUNDER} began working with PhDs and MDs to write a textbook on tattoo materials. Tattooing is one of the oldest art forms, yet much of its science has gone under-researched or unshared. This book gathers existing research into one place, encourages further study and supports better procedure standards — particularly for clients with medical conditions.</p>
<p>It is the first in a planned series for operators, lawmakers and consumers.</p>
<p><a class="btn btn-primary" href="{AMAZON_URL}" rel="noopener">Buy the book on Amazon</a></p>
</div></section>
''', ld=[BOOK_LD, FOUNDER_LD], crumbs="Book", og_type="book")

page("/app/", "Tattoo Science Learning App — 183 Lessons | The Science of Tattooing",
     "Play The Science of Tattooing web app: 183 gamified lessons and quizzes on tattoo physiology, ink chemistry, complications, history, physics and sociology.",
     f'''
<section class="hero"><div class="wrap hero-grid">
<div><span class="label">The app · Plays in your browser</span><h1>Learn tattoo science one lesson at a time</h1>
<p class="lead">Short lessons, quizzes and awards across six subjects. Built for apprentices, working artists and curious clients — on any phone or computer.</p>
<div class="actions"><a class="btn btn-app" href="{APP_URL}" rel="noopener">Play now</a></div>
<ul class="stats"><li><b>183</b><span>lessons</span></li><li><b>6</b><span>subjects</span></li></ul></div>
{ELEMENTS}
</div></section>
<section class="band"><div class="wrap">
<span class="label">Subjects</span><h2>What you'll learn</h2>
<div class="grid grid-3" style="margin-top:var(--s4)">
<article class="card"><span class="label">01 · Ph</span><h3>Physiology</h3><p>Skin layers, wound healing and how the body responds to pigment.</p></article>
<article class="card"><span class="label">02 · Ch</span><h3>Chemistry</h3><p>Pigments, carriers, preservatives and what's really in the bottle.</p></article>
<article class="card"><span class="label">03 · Co</span><h3>Complications</h3><p>Reactions, infections and when to refer a client to a doctor.</p></article>
<article class="card"><span class="label">04 · Hi</span><h3>History</h3><p>Tattooing traditions and milestones across cultures and centuries.</p></article>
<article class="card"><span class="label">05 · Py</span><h3>Physics</h3><p>Needles, machines, light and laser removal.</p></article>
<article class="card"><span class="label">06 · So</span><h3>Sociology</h3><p>Tattooing, identity, regulation and the culture around the craft.</p></article>
</div>
<div class="actions"><a class="btn btn-app" href="{APP_URL}" rel="noopener">Start your first lesson</a></div>
</div></section>
<section><div class="wrap split"><div><h2>See it in action</h2><p>Watch a quick look at The Science of Tattooing, then jump into the app.</p></div>{VIDEO}</div></section>
''', ld=[APP_LD], crumbs="App")

page("/regulators/", "Tattoo Safety Education for Regulators & Lawmakers | The Science of Tattooing",
     "Evidence-based tattoo safety education for health departments, inspectors and lawmakers — tattoo ink, infection control and procedure standards from an experienced artist.",
     f'''
<section class="hero"><div class="wrap prose">
<span class="label">For regulators</span><h1>Better tattoo rules start with shared knowledge</h1>
<p class="lead">We work with regulators in a cooperative way to educate lawmakers and enforcement agencies about how tattooing actually works.</p>
<div class="actions"><a class="btn btn-primary" href="mailto:{EMAIL}?subject=Regulatory%20education">Get in touch</a></div>
</div></section>
<section class="band"><div class="wrap">
<h2>How we can help</h2>
<div class="grid grid-3" style="margin-top:var(--s4)">
<article class="card"><h3>Briefings &amp; training</h3><p>Plain-language sessions for health departments and inspectors on tattoo materials, procedures and aftercare.</p></article>
<article class="card"><h3>Research context</h3><p>What published studies say about tattoo ink and safety — and where evidence is still thin.</p></article>
<article class="card"><h3>Practitioner perspective</h3><p>Two decades of studio experience to help rules work in real shops.</p></article>
</div></div></section>
''', crumbs="For regulators")

page("/about/", "About Hannah Wolf & The Science of Tattooing",
     "The Science of Tattooing was founded in 2018 by Hannah Wolf, a tattoo artist with 20+ years of experience, to bring research and understanding to tattooing.",
     f'''
<section class="hero"><div class="wrap prose">
<span class="label">About</span><h1>Shedding light on the mysterious side of tattooing</h1>
<p class="lead">The Science of Tattooing was established by {FOUNDER} to bring awareness and understanding to under-researched areas of tattooing.</p>
<h2>At a glance</h2>
<p>{FOUNDER} is a veteran tattoo artist with more than twenty years behind the machine. In 2017 she began working with PhDs and MDs on a textbook about tattoo materials, and in 2018 founded The Science of Tattooing to share that knowledge.</p>
<p>The project's goals are to share existing research, encourage further study and support better procedure standards — especially for clients with medical conditions.</p>
<h2>What we make</h2>
<ul><li><a href="/book/">The Science of Tattooing</a>, the first book in a planned series for operators, lawmakers and consumers.</li>
<li><a href="/app/">A gamified learning app</a> with 183 lessons across six subjects.</li>
<li><a href="/regulators/">Education for regulators</a> and enforcement agencies.</li></ul>
<div class="actions"><a class="btn btn-app" href="{APP_URL}" rel="noopener">Play the app</a><a class="btn btn-ghost" href="/contact/">Contact</a></div>
</div></section>
''', ld=[FOUNDER_LD, {"@type": "AboutPage", "url": SITE + "/about/", "mainEntity": {"@id": SITE + "/#org"}}], crumbs="About")

page("/contact/", "Contact The Science of Tattooing",
     "Contact The Science of Tattooing about the book, the learning app, speaking, partnerships or regulatory education.",
     f'''
<section class="hero"><div class="wrap prose">
<span class="label">Contact</span><h1>Get in touch</h1>
<p class="lead">Questions about the book, the app, speaking, research partnerships or regulatory education? Email us and we'll get back to you.</p>
<div class="actions"><a class="btn btn-primary" href="mailto:{EMAIL}">{EMAIL}</a><a class="btn btn-ghost" href="{FACEBOOK}" rel="noopener">Facebook</a></div>
<h2>Tattoo appointments</h2>
<p>This site is for education. For tattoo bookings with {FOUNDER}, visit <a href="https://tattoosbyhannah.com" rel="noopener">tattoosbyhannah.com</a>.</p>
</div></section>
''', ld=[{"@type": "ContactPage", "url": SITE + "/contact/"}], crumbs="Contact")

page("/ink/", "What's in Tattoo Ink? Pigments, Carriers & Additives Explained",
     "What is tattoo ink made of? Learn about tattoo pigments, carriers, preservatives and metals, how ink is regulated in the US, and how to read an ink's safety data sheet.",
     f'''
<section class="hero"><div class="wrap prose">
<span class="label">Ink ingredients</span><h1>What's in tattoo ink?</h1>
<p class="lead">Every tattoo ink is a mix of pigment particles suspended in a carrier, plus additives that keep it stable. Here is what each part does — and how to find out what's in a specific bottle.</p>
<h2>The three main components</h2>
<ul><li><b>Pigments</b> — the insoluble particles that stay in the skin and create color. They may be organic (carbon-based, such as many bright reds and yellows) or inorganic (mineral, such as titanium dioxide whites and iron oxides).</li>
<li><b>Carrier</b> — the liquid that holds pigment evenly and carries it into the skin, commonly water with ingredients such as glycerin, alcohols or witch hazel.</li>
<li><b>Additives</b> — binders, thickeners, surfactants and preservatives that control flow, shelf life and consistency.</li></ul>
<h2>How to read an ink label or safety data sheet</h2>
<p>Pigments are usually identified by a Colour Index name and number (for example "Pigment Red 254, CI 56110") and a CAS number. Looking those up tells you the actual chemical — including whether it contains metals.</p>
<h2>How tattoo ink is regulated in the US</h2>
<p>Tattoo inks are regulated by the FDA as cosmetics. The Modernization of Cosmetics Regulation Act of 2022 (MoCRA) added new requirements for manufacturers, including facility registration and product listing.</p>
<div class="card" style="margin-top:var(--s5)"><span class="label">Coming soon</span><h3>Ink ingredient lookup &amp; chat</h3>
<p>We're building a searchable database of tattoo inks by brand, product and material — plus a chat assistant you can ask about what's in a pigment.</p>
<a class="btn btn-primary" href="mailto:{EMAIL}?subject=Ink%20database%20updates">Get notified at launch</a></div>
<p style="margin-top:var(--s4)">Want the full picture? <a href="/book/">The book</a> covers ink chemistry in depth, and the <a href="/app/">app's Chemistry lessons</a> let you practice it.</p>
</div></section>
''', ld=[{"@type": "Article", "headline": "What's in tattoo ink?", "author": {"@id": SITE + "/#founder"}, "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": SITE + "/ink/", "image": SITE + "/og-image.png", "dateModified": TODAY}], crumbs="Ink ingredients", og_type="article")

page("/404.html", "Page not found | The Science of Tattooing", "This page could not be found.",
     '''<section class="hero"><div class="wrap prose"><span class="label">Error 404</span><h1>That page isn't here</h1>
<p class="lead">It may have moved when we rebuilt the site.</p><div class="actions"><a class="btn btn-primary" href="/">Go home</a><a class="btn btn-ghost" href="/app/">Try the app</a></div></div></section>''')
# keep 404 out of the index
p404 = os.path.join(OUT, "404.html")
s = open(p404).read().replace('content="index, follow, max-image-preview:large"', 'content="noindex"').replace(f'<link rel="canonical" href="{SITE}/404.html">\n', "")
open(p404, "w").write(s)

# ---------------- sitemap / robots ----------------
urls = [("/", "1.0"), ("/ink/", "0.9"), ("/app/", "0.9"), ("/book/", "0.9"), ("/regulators/", "0.7"), ("/about/", "0.6"), ("/contact/", "0.5")]
with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u, p in urls:
        f.write(f"  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><priority>{p}</priority></url>\n")
    f.write("</urlset>\n")
with open(os.path.join(OUT, "robots.txt"), "w") as f:
    f.write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
with open(os.path.join(OUT, "favicon.svg"), "w") as f:
    f.write(LOGO_SVG.replace('<svg viewBox', '<svg xmlns="http://www.w3.org/2000/svg" viewBox').replace(' aria-hidden="true"', ""))
print("built", OUT)
