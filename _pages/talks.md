---
layout: page
permalink: /talks/
title: Talks
nav: true
nav_order: 4
description: Where I have talked about my work, at conferences and as an invited speaker.
---

{% assign talks = site.data.talks | sort: "date" | reverse %}
{% assign years = talks | group_by_exp: "t", "t.date | date: '%Y'" %}
{% for y in years %}
<h2 class="year">{{ y.name }}</h2>
<ol class="cv-list">
{% for t in y.items %}
{% assign badge2 = nil %}
{% if t.kind contains 'invited' %}{% assign badge2 = 'Invited' %}{% endif %}
{% if t.type == 'Seminar' %}{% assign title = t.title %}{% assign sub = t.location %}{% assign badge2 = 'Invited' %}{% else %}{% assign title = t.event %}{% capture sub %}{{ t.location }}{% if t.title %} — <em>{{ t.title }}</em>{% endif %}{% endcapture %}{% endif %}
{% include cv_entry.liquid badge=t.type badge2=badge2 dates=t.dates title=title url=t.url sub=sub %}
{% endfor %}
</ol>
{% endfor %}
