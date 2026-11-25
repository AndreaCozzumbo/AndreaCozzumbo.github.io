---
layout: page
permalink: /cv/
title: Curriculum vitae
nav_title: CV
nav: true
nav_order: 3
description: Here is my curriculum vitae. You can also download it as a PDF.
toc:
  sidebar: left
---

{% assign cv = site.data.curriculum %}
{% assign talks = site.data.talks | sort: "date" | reverse %}

<p class="cv-downloads">
<a class="pub-btn" href="{{ '/assets/pdf/CV.pdf' | relative_url }}">CV (PDF)</a>
<a class="pub-btn" href="{{ '/assets/pdf/PubList.pdf' | relative_url }}">Publication list (PDF)</a>
<a class="pub-btn" href="{{ '/assets/pdf/CV_full.pdf' | relative_url }}">CV + publications (PDF)</a>
<a class="pub-btn pub-btn-bib" href="{{ '/assets/pdf/cv_latex.zip' | relative_url }}">LaTeX source</a>
</p>

<h2 class="cv-h2" id="education">Education</h2>
<ol class="cv-list">
{% for e in cv.education %}
{% capture title %}{{ e.degree }} in {{ e.field }}{% endcapture %}
{% capture sub %}{{ e.institution }}{% if e.grade != blank and e.grade != '' %}, {{ e.grade }}{% endif %}{% endcapture %}
{% capture note %}{{ e.thesis_label }}: <em>{{ e.thesis }}</em><br>Supervisor{% if e.supervisors contains ',' %}s{% endif %}: {{ e.supervisors }}{% endcapture %}
{% include cv_entry.liquid badge=e.badge dates=e.dates title=title sub=sub note=note pdf=e.pdf %}
{% endfor %}
</ol>

<h2 class="cv-h2" id="experience">Working and visit experience</h2>
<ol class="cv-list">
{% for e in cv.experience %}{% include cv_entry.liquid badge=e.badge dates=e.dates title=e.title url=e.url note=e.description %}{% endfor %}
</ol>

<h2 class="cv-h2" id="publications">Publications</h2>
<p>First- and co-author papers; the complete list, with collaboration papers, is on the <a href="{{ '/publications/' | relative_url }}">publications page</a>.</p>
<div class="publications">
{% bibliography --group_by none --query @*[category=first] %}
{% bibliography --group_by none --query @*[category=coauthor] %}
</div>

<h2 class="cv-h2" id="talks">Talks at international conferences and workshops</h2>
<ol class="cv-list">
{% for t in talks %}{% if t.type == 'Conference' %}
{% assign badge2 = nil %}{% if t.kind contains 'invited' %}{% assign badge2 = 'Invited' %}{% endif %}
{% capture sub %}{{ t.location }}, <em>{{ t.kind }}</em>{% endcapture %}
{% include cv_entry.liquid badge=badge2 dates=t.dates title=t.event url=t.url sub=sub %}
{% endif %}{% endfor %}
</ol>

<h2 class="cv-h2" id="seminars">Invited seminars</h2>
<ol class="cv-list">
{% for t in talks %}{% if t.type == 'Seminar' %}{% include cv_entry.liquid dates=t.dates title=t.title url=t.url sub=t.location %}{% endif %}{% endfor %}
</ol>

<h2 class="cv-h2" id="participation">Conferences, workshops and schools attended</h2>
<ol class="cv-list">
{% for e in cv.participation %}{% include cv_entry.liquid dates=e.dates title=e.title url=e.url %}{% endfor %}
</ol>

<h2 class="cv-h2" id="organization">Conference organization</h2>
<ol class="cv-list">
{% for e in cv.organization %}{% include cv_entry.liquid badge="LOC" dates=e.dates title=e.title url=e.url sub=e.role %}{% endfor %}
</ol>

<h2 class="cv-h2" id="supervision">Thesis supervisor</h2>
<ol class="cv-list">
{% for e in cv.supervision %}
{% capture note %}<em>{{ e.thesis }}</em> by {{ e.student }}{% endcapture %}
{% include cv_entry.liquid badge="Thesis" dates=e.dates title=e.title note=note %}
{% endfor %}
</ol>

<h2 class="cv-h2" id="outreach">Outreach experience</h2>
<ol class="cv-list">
{% for e in cv.outreach %}{% include cv_entry.liquid badge="Outreach" dates=e.dates title=e.title url=e.url note=e.description %}{% endfor %}
</ol>

<h2 class="cv-h2" id="skills">Technical skills</h2>
<ul class="cv-skills">
{% for s in cv.skills.technical %}<li><strong>{{ s.label }}</strong> {{ s.levels | join: '; ' }}</li>{% endfor %}
</ul>

<h2 class="cv-h2" id="languages">Languages</h2>
<ul class="cv-skills">
{% for l in cv.skills.languages %}<li><strong>{{ l.language }}</strong> {{ l.level }}{% if l.note != '' %} ({{ l.note }}){% endif %}</li>{% endfor %}
</ul>
