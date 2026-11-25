---
layout: page
permalink: /theses/
title: Theses
nav: true
nav_order: 5
description: Here are the longer works I wrote during my studies.
---

<ol class="cv-list">
{% assign theses = site.data.curriculum.education | sort: "date" | reverse %}
{% for e in theses %}
{% capture sub %}{{ e.institution }}, {{ e.field }}{% endcapture %}
{% capture note %}Supervisor{% if e.supervisors contains ',' %}s{% endif %}: {{ e.supervisors }}{% endcapture %}
{% include cv_entry.liquid badge=e.badge dates=e.dates title=e.thesis sub=sub note=note pdf=e.pdf %}
{% endfor %}
</ol>
