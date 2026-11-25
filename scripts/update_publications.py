#!/usr/bin/env python3
"""Refresh _bibliography/papers.bib from INSPIRE.

Downloads every paper of the INSPIRE author below and adds to each BibTeX entry:

  category      first | coauthor | collaboration  (the sections of /publications/)
  abbr          journal badge, e.g. JCAP
  inspirehep_id INSPIRE record number
  citations     citation count on the day the script ran

It also restores the full author list of short-author papers, which INSPIRE's
BibTeX cuts at ten names, and applies _data/publication_overrides.yml.

Run it by hand with  python3 scripts/update_publications.py
GitHub runs it every Monday (.github/workflows/update-publications.yml).
Needs only Python 3 and PyYAML.
"""

import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

AUTHOR = "A.Cozzumbo.1"  # INSPIRE author identifier
LAST_NAME = "Cozzumbo"

# Papers with a collaboration, or with more authors than this, are listed under
# "Collaboration papers".
MAX_SHORT_AUTHORS = 20

REPO_ROOT = Path(__file__).resolve().parent.parent
BIB = REPO_ROOT / "_bibliography" / "papers.bib"
OVERRIDES = REPO_ROOT / "_data" / "publication_overrides.yml"
API = "https://inspirehep.net/api/literature"

JOURNAL_ABBR = {
    "Phys. Rev. D": "PRD",
    "Phys. Rev. Lett.": "PRL",
    "Phys. Rev. X": "PRX",
    "JCAP": "JCAP",
    "JHEP": "JHEP",
    "Astrophys. J.": "ApJ",
    "Astrophys. J. Lett.": "ApJL",
    "Astrophys. J. Suppl.": "ApJS",
    "Astron. Astrophys.": "A&A",
    "Mon. Not. Roy. Astron. Soc.": "MNRAS",
    "Class. Quant. Grav.": "CQG",
    "Eur. Phys. J. C": "EPJC",
    "Phys. Dark Univ.": "PDU",
    "Phys. Lett. B": "PLB",
    "Phil. Trans. Roy. Soc. Lond. A": "PTRSA",
}


def fetch(**params):
    url = f"{API}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url, timeout=90) as response:
        return response.read().decode("utf-8")


def fetch_records(query, fields):
    body = fetch(q=query, size=250, fields=fields)
    return [hit["metadata"] for hit in json.loads(body)["hits"]["hits"]]


def category(record, entry):
    if "collaboration =" in entry or record.get("author_count", 0) > MAX_SHORT_AUTHORS:
        return "collaboration"
    first = re.search(r'author\s*=\s*"([^"]*)"', entry)
    return "first" if first and first.group(1).startswith(LAST_NAME + ",") else "coauthor"


def enrich(entry, records, authors, overrides):
    key = re.match(r"@\w+\{([^,]+),", entry).group(1).strip()
    record = records.get(key)
    if record is None:
        sys.exit(f"INSPIRE returned BibTeX for {key} but no record: try again later")

    if key in authors:
        names = " and ".join(authors[key])
        entry = re.sub(r'(author\s*=\s*)"[^"]*"', lambda m: f'{m.group(1)}"{names}"', entry, count=1)

    eprint = re.search(r'eprint\s*=\s*"([^"]+)"', entry)
    for field, value in (overrides.get(eprint.group(1)) or {} if eprint else {}).items():
        entry = re.sub(rf'(\b{field}\s*=\s*)"[^"]*"', lambda m: f'{m.group(1)}"{{{value}}}"', entry, count=1)

    extra = {
        "category": category(record, entry),
        "inspirehep_id": record["control_number"],
        "citations": record.get("citation_count", 0),
    }
    journal = re.search(r'journal\s*=\s*"([^"]+)"', entry)
    if journal and journal.group(1) in JOURNAL_ABBR:
        extra["abbr"] = JOURNAL_ABBR[journal.group(1)]
    lines = "".join(f"    {name} = {{{value}}},\n" for name, value in extra.items())
    return re.sub(r"(@\w+\{[^,]+,\n)", lambda m: m.group(1) + lines, entry, count=1)


def main():
    query = f"a {AUTHOR}"
    bib = fetch(q=query, sort="mostrecent", size=250, format="bibtex")
    entries = [e.strip() for e in re.split(r"(?m)^(?=@\w+\{)", bib) if e.strip()]

    records = {}
    for record in fetch_records(query, "texkeys,control_number,author_count,citation_count"):
        for key in record.get("texkeys", []):
            records[key] = record

    authors = {}
    short = f"{query} and ac 1->{MAX_SHORT_AUTHORS}"
    for record in fetch_records(short, "texkeys,authors.full_name"):
        names = [a["full_name"] for a in record.get("authors", [])]
        for key in record.get("texkeys", []):
            authors[key] = names

    # Never replace the list with something suspiciously short (INSPIRE hiccup).
    previous = BIB.read_text(encoding="utf-8").count("\n@") if BIB.exists() else 0
    if not entries or len(entries) < 0.8 * previous:
        sys.exit(f"INSPIRE returned {len(entries)} papers, the current list has {previous}: not updating")

    overrides = {}
    if OVERRIDES.exists():
        overrides = yaml.safe_load(OVERRIDES.read_text(encoding="utf-8")) or {}

    enriched = [enrich(e, records, authors, overrides) for e in entries]
    header = "% Written by scripts/update_publications.py from INSPIRE -- do not edit by hand.\n% Corrections go in _data/publication_overrides.yml.\n\n"
    BIB.write_text(header + "\n\n".join(enriched) + "\n", encoding="utf-8")

    counts = {c: sum(f"category = {{{c}}}" in e for e in enriched) for c in ("first", "coauthor", "collaboration")}
    print(f"{len(enriched)} papers: {counts}")


if __name__ == "__main__":
    main()
