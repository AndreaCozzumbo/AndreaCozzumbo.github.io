#!/usr/bin/env python3
"""Write the LaTeX bodies of the CV and of the publication list.

Reads   _data/curriculum/*.yml, _data/talks.yml, _bibliography/papers.bib
Writes  cv-latex/generated/{header,cv,publications}.tex

The website reads the same files directly, so the page and the PDFs always agree.
Values are plain text: accents, dashes and Greek letters can be typed as they are.
Needs only Python 3 and PyYAML.
"""

import re
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA = REPO_ROOT / "_data"
OUT = REPO_ROOT / "cv-latex" / "generated"
LAST_NAME = "Cozzumbo"

SPECIAL = {
    "\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
    "–": "--", "—": "---", "’": "'", "“": "``", "”": "''",
}
GREEK = {"Λ": r"\Lambda", "γ": r"\gamma", "α": r"\alpha", "β": r"\beta", "σ": r"\sigma", "Ω": r"\Omega", "μ": r"\mu", "ν": r"\nu"}
SPECIAL.update({ch: rf"\ensuremath{{{macro}}}" for ch, macro in GREEK.items()})


def tex(text):
    """Plain text -> LaTeX."""
    out = "".join(SPECIAL.get(ch, ch) for ch in str(text or ""))
    return out.replace("LaTeX", r"\LaTeX")


def url(address):
    return address.replace("%", r"\%").replace("#", r"\#")


def link(text, address=None):
    return rf"\href{{{url(address)}}}{{{text}}}" if address else text


def load(name):
    return yaml.safe_load((DATA / name).read_text(encoding="utf-8")) or []


def section(title, level="section"):
    return rf"\{level}{{\textcolor{{myCustomColor}}{{{tex(title)}}}}}"


def row(left, right):
    """One line: text on the left (may wrap), date on the right."""
    return rf"\datedline{{{left}}}{{{tex(right)}}}"


def entry(title, dates, description, address=None):
    return rf"\cvblock{{{link(tex(title), address)}}}{{{tex(dates)}}}{{{description}}}"


# --------------------------------------------------------------------- CV ---


def cv_body():
    out = [section("Education")]
    for e in load("curriculum/education.yml"):
        grade = f", {tex(e['grade'])}" if e.get("grade") else ""
        plural = "s" if "," in e["supervisors"] else ""
        out.append(
            rf"\cvdegree{{{tex(e['field'])}}}{{{tex(e['dates'])}}}{{{tex(e['degree'])}}}{{{tex(e['institution'])}{grade}}}"
            rf"{{{tex(e['thesis_label'])}: \textit{{{tex(e['thesis'])}}}\\ Supervisor{plural}: {tex(e['supervisors'])}}}"
        )

    out += [section("Professional experience"), section("Working and visit experience", "subsection")]
    for e in load("curriculum/experience.yml"):
        out.append(entry(e["title"], e["dates"], tex(e["description"]), e.get("url")))

    out.append(section("Thesis supervisor", "subsection"))
    for e in load("curriculum/supervision.yml"):
        out.append(entry(e["title"], e["dates"], rf"\textit{{{tex(e['thesis'])}}} by {tex(e['student'])}."))

    out.append(section("Outreach experience", "subsection"))
    for e in load("curriculum/outreach.yml"):
        out.append(entry(e["title"], e["dates"], tex(e["description"]), e.get("url")))

    out.append(section("Conference organization"))
    for e in load("curriculum/organization.yml"):
        title = link(rf"\textbf{{{tex(e['title'])}}}", e.get("url"))
        out.append(row(f"{title} -- {tex(e['role'])}", e["dates"]))

    talks = sorted(load("talks.yml"), key=lambda t: str(t["date"]), reverse=True)
    out.append(section("Talks at international conferences and workshops"))
    for t in talks:
        if t["type"] == "Conference":
            title = link(rf"\textbf{{{tex(t['event'])}}}", t.get("url"))
            out.append(row(rf"{title}, {tex(t['location'])}, \textit{{{tex(t['kind'])}}}", t["dates"]))

    out.append(section("Invited seminars"))
    for t in talks:
        if t["type"] == "Seminar":
            out.append(row(rf"\textbf{{{tex(t['title'])}}}, {tex(t['location'])}", t["dates"]))

    out.append(section("Participation at international conferences, workshops and schools"))
    for e in load("curriculum/participation.yml"):
        out.append(row(link(rf"\textbf{{{tex(e['title'])}}}", e.get("url")), e["dates"]))

    skills = load("curriculum/skills.yml")
    out.append(section("Technical skills"))
    for s in skills["technical"]:
        out.append(rf"\cvitem{{{tex(s['label'])}}}{{{', '.join(tex(x) for x in s['levels'])}}}")
    out.append(section("Languages"))
    for lang in skills["languages"]:
        out.append(rf"\cvitemwithcomment{{{tex(lang['language'])}}}{{{tex(lang['level'])}}}{{{tex(lang['note'])}}}")
    return "\n\n".join(out) + "\n"


def header():
    p = load("curriculum/profile.yml")
    name = {k: rf"\textcolor{{myCustomColor}}{{{tex(p[k])}}}" for k in ("first_name", "last_name")}
    return "\n".join([
        rf"\name{{{name['first_name']}}}{{{name['last_name']}}}",
        rf"\email{{{p['email']}}}",
        rf"\extrainfo{{\href{{https://orcid.org/{p['orcid']}}}{{ORCID {p['orcid']}}}"
        rf"~~~\href{{{url(p['webpage'])}}}{{{tex(p['webpage'].split('://')[-1])}}}}}",
    ]) + "\n"


# ------------------------------------------------------------ publications ---


def parse_bib(text):
    """Entries of papers.bib as dicts. Values keep their LaTeX."""
    entries = []
    for chunk in re.split(r"(?m)^(?=@\w+\{)", text):
        if not chunk.startswith("@"):
            continue
        fields = {}
        for m in re.finditer(r'(?ms)^\s+(\w+)\s*=\s*(?:"(.*?)"|\{(.*?)\}),?\s*$', chunk):
            fields[m.group(1)] = m.group(2) if m.group(2) is not None else m.group(3)
        if not {"title", "author", "category"} <= fields.keys():
            sys.exit(f"papers.bib: incomplete entry {chunk.splitlines()[0]!r}")
        entries.append(fields)
    return entries


def bib_text(value):
    """LaTeX from INSPIRE, made safe for pdflatex."""
    value = re.sub(r"^\{(.*)\}$", r"\1", value.strip())
    value = re.sub(r"(?<!\\)&", r"\\&", value)
    for ch, macro in {**GREEK, "⊙": r"\odot"}.items():
        value = value.replace(ch, rf"\ensuremath{{{macro}}}")
    return value.replace("–", "--").replace("’", "'")


def authors(fields):
    names = []
    for person in fields["author"].split(" and "):
        if person.strip() == "others":
            return ", ".join(names) + r" \textbf{et al.}"
        last, _, first = person.partition(", ")
        initials = " ".join(f"{part[0]}." for part in re.split(r"[\s.]+", first) if part)
        name = bib_text(f"{initials} {last}".strip())
        names.append(rf"\textbf{{{name}}}" if last == LAST_NAME else name)
    return ", ".join(names)


COLLABORATIONS = {"LIGO Scientific": "LIGO Scientific", "VIRGO": "Virgo", "Virgo": "Virgo", "KAGRA": "KAGRA", "ET": "ET"}


def collaboration(fields):
    names = [COLLABORATIONS[c] for c in fields.get("collaboration", "").split(", ") if c in COLLABORATIONS]
    names.sort(key=list(COLLABORATIONS.values()).index)
    if not names:
        return ""
    return " and ".join(names) + f" Collaboration{'s' if len(names) > 1 else ''}: "


def publication(fields):
    refs = [rf"\href{{https://arxiv.org/abs/{fields['eprint']}}}{{arXiv:{fields['eprint']}}}"] if "eprint" in fields else []
    if "doi" in fields:
        refs.append(rf"doi: \href{{https://doi.org/{url(fields['doi'])}}}{{{tex(fields['doi'])}}}")
    lines = [collaboration(fields) + authors(fields), rf"\textit{{{bib_text(fields['title'])}}}", ", ".join(refs)]
    return r"\cvpub{" + r", \newline ".join(line for line in lines if line) + "}"


def publications_body():
    bib = parse_bib((REPO_ROOT / "_bibliography" / "papers.bib").read_text(encoding="utf-8"))
    out = [section("List of publications")]

    def add(title, key):
        out.append(section(title, "subsection"))
        out.extend(publication(f) for f in bib if f["category"] == key)

    add("First author", "first")
    add("Co-author", "coauthor")
    add("Collaboration papers", "collaboration")
    return "\n\n".join(out) + "\n"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, body in (("header", header()), ("cv", cv_body()), ("publications", publications_body())):
        (OUT / f"{name}.tex").write_text(body, encoding="utf-8")
        print(f"wrote cv-latex/generated/{name}.tex")


if __name__ == "__main__":
    main()
