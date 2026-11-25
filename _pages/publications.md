---
layout: page
permalink: /publications/
title: Publications
nav: true
nav_order: 2
---

<div class="pubs-top">
<p>Here are the papers I wrote or contributed to. You can also find them on
<span class="icon-links"><a class="icon-link" href="https://inspirehep.net/authors/{{ site.data.socials.inspirehep_id }}" aria-label="INSPIRE" title="INSPIRE"><i class="ai ai-inspire"></i></a> and
<a class="icon-link" href="https://orcid.org/{{ site.data.socials.orcid_id }}" aria-label="ORCID" title="ORCID"><i class="fa-brands fa-orcid"></i></a></span>.
Click on BibTeX to copy a citation, or take the <a href="{{ '/assets/pdf/PubList.pdf' | relative_url }}">whole list as a PDF</a>.</p>
{% include bib_search.liquid %}
</div>

<div class="publications">

<section class="pub-group" id="first-author">
<h2 class="pub-section">First author</h2>
{% bibliography --group_by none --query @*[category=first] %}
</section>

<section class="pub-group" id="co-author">
<h2 class="pub-section">Co-author</h2>
{% bibliography --group_by none --query @*[category=coauthor] %}
</section>

<section class="pub-group" id="collaboration-papers">
<h2 class="pub-section">Collaboration papers</h2>
{% bibliography --query @*[category=collaboration] %}
</section>

</div>
