#!/usr/bin/env python3
"""Render the manual site's generated pages from the manifests.

    python3 tools/site/gen_pages.py

Writes the generated pages (gitignored, so the deploy builds them fresh):

  manual/<remix>/...   the manual of each published remix (gen_manual.py)
  _remix-<name>.md     the module table of each published remix's overview page

Only the remixes in release.REMIXES are published. The pages are rendered at
deploy time (the Pages workflow on main; the site job of ci.yml on a PR), so
the site and the manifests cannot drift. Stdlib only, like the rest of the
tools. The registry execs the manifests, so the author submodules must be
checked out first (git submodule update --init).

Links to the repository are written as full https URLs; no literal
repository path appears in this file on purpose: tools/verify/doclinks.py
scans it too, and every path it finds must exist.
"""

import html
import pathlib
import json
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / pathlib.Path("docs") / "site" / "reference"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1])); import toolpath  # noqa: E402,F401  (every tools/ dir on sys.path)

from remix import index, registry  # noqa: E402
from remix.schema import CATEGORY_TITLE, Category  # noqa: E402

GH_UPSTREAM = "https://github.com/sambanks/octabam"
GH_FORK = "https://github.com/ilia-murzinov/octabam"
# Back-compat for any leftover GH uses in this file / tests.
GH = GH_UPSTREAM

_SMALL = {"a", "an", "and", "as", "at", "but", "by", "for", "from", "in", "of", "on", "or", "the", "to", "with", "over"}
_UPPER = {"os", "din", "dj", "eq", "bd", "usb", "midi", "cc", "cpu", "dsp", "cf", "lfo", "ata", "txtr", "amf",
          "fx1", "fx2", "lofi2", "brain", "ui", "id", "sd"}


def title_case(text: str) -> str:
    """Title Case for headings and nav labels. Tokens that already carry capitals
    or digits (device labels, acronyms) and links/code are kept as written."""
    out, started, after_colon = [], False, False
    for tok in text.replace("octabam-", "octabam ").split(" "):
        word = tok.strip(":,()")
        if re.fullmatch(r"[a-z]+(-[a-z]+)+", word):
            tok = tok.replace(word, "-".join(x.upper() if x in _UPPER else x.capitalize() for x in word.split("-")), 1)
            out.append(tok)
            started = True
            continue
        if not re.fullmatch(r"[a-z][a-z']*", word):
            out.append(tok)
            started = started or bool(re.search(r"[A-Za-z]", tok))
            after_colon = tok.endswith(":")
            continue
        if word in _UPPER:
            new = word.upper()
        elif word in _SMALL and started and not after_colon:
            new = word
        else:
            new = word.capitalize()
        out.append(tok.replace(word, new, 1))
        started = True
        after_colon = tok.endswith(":")
    return " ".join(out)


def _label(m) -> str:
    """Readable headings; manifest keys and device labels keep their spelling."""
    names = {
        "analog-bassdrum": "Analog BD",
        "ata-write-guard": "ATA write guard",
        "bbd": "BBD delay",
        "blackpyramids-303": "BlackPyramids 303",
        "character-txtr": "Character TXTR",
        "cxosc": "Complex oscillator",
        "devilish": "dEVILish",
        "dlcopy": "Effect loader (copier)",
        "dlpump": "Effect loader (sender)",
        "direct-jump-kyoti": "Direct jump (Kyoti)",
        "distorx": "DisTorX",
        "lofi-amf-fix": "Lo-Fi AMF fix",
        "octa303": "OCTA-303",
        "wavecf": "WAVE",
        "plocks-p2": "Page 2 parameter locks",
        "rec-cs1-skip": "Recorder CS1 skip",
        "rec-trig-mute": "Recorder trig mute",
        "rlen-plen": "RLEN PLEN",
        "rnd-name": "Random naming",
        "scenes-p2": "Page 2 scene locks",
        "stems": "Stem recording",
        "tempo-bus": "Tempo controls",
    }
    if m.name in names:
        return title_case(names[m.name])
    acronyms = {"USB", "MIDI", "CC", "FX1", "FX2", "DSP", "CPU", "CF", "LFO", "LOFI2", "BRAIN"}
    words = m.key.replace("_", " ").split()
    return title_case(" ".join(word if word in acronyms else word.lower() for word in words))


def _author(m) -> str:
    if m.is_stock:
        return "stock"
    return f"[{m.author}]({m.author_url})" if m.author_url else (m.author or "?")


def _site_keys():
    import release
    return set(getattr(release, "SITE_MODULES", ()) or ())


def _records(m) -> dict:
    path = OUT.parent / "screenshots.json"
    records = json.loads(path.read_text()) if path.exists() else {}
    return records.get(m.name, {})


def _module_url(m) -> str:
    """Canonical tree for the module: fork for SITE_MODULES, upstream otherwise."""
    d = pathlib.Path("modules") / m.name
    base = GH_FORK if m.key in _site_keys() else GH_UPSTREAM
    if (ROOT / d / "README.md").exists():
        return f"{base}/blob/main/{d}/README.md"
    return f"{base}/tree/main/{d}"


def _figure(record: dict) -> list[str]:
    caption = record["caption"]
    return [f"![{caption}](../../img/{record['image']})", "", f"*{caption}*", ""]


def _hero_key(m) -> str | None:
    """The screenshot shown under the title: `main` where captured, else the first."""
    recs = _records(m)
    return "main" if "main" in recs else next(iter(recs), None)


def hero(m) -> list[str]:
    key = _hero_key(m)
    return _figure(_records(m)[key]) if key else []


def screen_reference(m) -> list[str]:
    notes_path = OUT.parent / "screen-notes.json"
    notes = json.loads(notes_path.read_text()) if notes_path.exists() else {}
    hero_key = _hero_key(m)
    rest = [r for k, r in _records(m).items() if k != hero_key]
    lines = []
    if rest:
        lines += ["## Screen reference", ""]
        for record in rest:
            lines += _figure(record)
    if m.name in notes:
        lines += ["## Display behaviour", "", notes[m.name], ""]
    return lines


def directory_page(mods, manual_page: dict) -> str:
    """Directory of Ilia's modules documented on this site."""
    site_keys = _site_keys()
    lines = ["# Modules", "",
             "Modules developed on this fork, with usage notes on this site. "
             "The rest of each `base*` / `cx*` image is credited on "
             "[Home](../index.md#credits). "
             "Build an image on [Build and Install](../web-builder.md).", ""]
    for cat, ms in index.by_category(mods).items():
        ms = [m for m in ms if m.key in site_keys]
        if not ms:
            continue
        lines += [f"### {CATEGORY_TITLE[cat]}", "", "| Feature | Author |", "|---|---|"]
        lines += [f"| [{_label(m)}](modules/{m.name}.md) | {_author(m)} |" for m in ms] + [""]
    return "\n".join(lines) + "\n"


def _display_author(m) -> tuple[str, str]:
    """(sort_key, markdown author cell) — normalize known author spellings."""
    if m.is_stock:
        return ("Elektron", "Elektron (stock)")
    raw = (m.author or "?").strip()
    url = (m.author_url or "").strip()
    # Collapse alternate spellings used across manifests.
    aliases = {
        "sambanks": ("Sam Banks", "https://github.com/sambanks"),
        "Sam Banks": ("Sam Banks", "https://github.com/sambanks"),
        "iliamurzinov": ("ilia-murzinov", "https://github.com/ilia-murzinov"),
        "ilia-murzinov": ("ilia-murzinov", "https://github.com/ilia-murzinov"),
        "timhastie/octatrick-modules": (
            "Tim Hastie (octatrick)", "https://github.com/timhastie/octatrick-modules"),
        "Zac Kyoti": ("Zac Kyoti", "https://github.com/Zac-Kyoti"),
        "markandrus/octemu": ("markandrus", "https://github.com/markandrus/octemu"),
        "bkkbrls-del/midisc": ("bkkbrls-del", "https://github.com/bkkbrls-del/midisc"),
        "bryantysinger/octa-bt-pt": (
            "bryantysinger", "https://github.com/bryantysinger/octa-bt-pt"),
        "sanderlegit": ("sanderlegit", "https://github.com/sanderlegit"),
        "radiohagen": ("radiohagen", "https://github.com/radiohagen"),
        "yvesrosius": ("yvesrosius", "https://github.com/yvesrosius"),
    }
    name, href = aliases.get(raw, (raw, url))
    if href:
        return (name, f"[{name}]({href})")
    return (name, name)


def shipped_credits_page(mods) -> str:
    """Author → modules as plain linked lists for BUILDER_REMIXES (+ SITE_MODULES)."""
    import release
    keys = set(getattr(release, "SITE_MODULES", ()) or ())
    for n in getattr(release, "BUILDER_REMIXES", ()) or ():
        keys |= set(registry.remix(n).modules)
    by: dict[str, list] = {}
    author_md: dict[str, str] = {}
    for key in keys:
        m = mods[key]
        sort_name, md = _display_author(m)
        author_md[sort_name] = md
        by.setdefault(sort_name, []).append(m)
    lines = [
        "<!-- generated by tools/site/gen_pages.py — do not edit -->",
        "",
    ]
    site_keys = _site_keys()
    for author in sorted(by, key=lambda a: (a == "Elektron", a.lower())):
        ms = sorted(by[author], key=lambda m: _label(m).lower())
        items = []
        for m in ms:
            name = _label(m)
            if m.is_stock:
                items.append(name)
            elif m.key in site_keys:
                # Paths are from docs/site/ (index.md includes this fragment).
                items.append(f"[{name}](reference/modules/{m.name}.md)")
            else:
                items.append(f"[{name}]({_module_url(m)})")
        lines += [f"**{author_md[author]}** — {', '.join(items)}.", ""]
    return "\n".join(lines) + "\n"


def module_page(m, mods, manual_page: dict) -> str:
    """One page per contributed module: the usage fragment (docs/site/usage/<name>.md) when one is written,
    else the manifest's line, then where the module is and its facts."""
    fragment = OUT.parent / pathlib.Path("usage") / f"{m.name}.md"
    who = html.escape(m.author or "?")
    if m.author_url:
        who = f'<a href="{html.escape(m.author_url)}">{who}</a>'
    lines = ["---", "not_in_nav: true", "---", "", f"# {_label(m)}", "", f'<p class="byline">By {who}</p>', ""]
    import release
    builder = getattr(release, "BUILDER_REMIXES", ()) or ()
    in_builder = sorted(
        n for n in builder
        if m.key in set(registry.remix(n).modules))
    if in_builder:
        listed = ", ".join(f"`{n}`" for n in in_builder)
        lines += [f"Ships in: {listed}.", ""]
    # Usage that leads with architecture diagrams: prose + path first, LCD
    # shots under ## Screens. Everyone else keeps a hero screen under the title.
    _DIAGRAM_FIRST = frozenset({"cxosc", "void", "resonator", "shatter", "stuttr"})
    if m.name in _DIAGRAM_FIRST and fragment.is_file():
        lines += [f'--8<-- "usage/{m.name}.md"', ""]
        recs = _records(m)
        if recs:
            lines += ["## Screens", ""]
            for record in recs.values():
                lines += _figure(record)
        notes_path = OUT.parent / "screen-notes.json"
        notes = json.loads(notes_path.read_text()) if notes_path.exists() else {}
        if m.name in notes:
            lines += ["## Display behaviour", "", notes[m.name], ""]
    else:
        lines += hero(m)
        if fragment.is_file():
            lines += [f'--8<-- "usage/{m.name}.md"', ""]
        else:
            lines += [m.doc, ""]
        lines += screen_reference(m)
    return "\n".join(lines) + "\n"


def _ensure_site_stock_stub() -> pathlib.Path | None:
    """Tim manifests call stock_guard at import; Pages CI has no MAIN OS.

    If the recon section is missing, write an ephemeral zero stub so the
    registry can load author metadata for credits. Returns the path when
    this process created the stub (caller must delete it afterward) so a
    later acceptance harvest does not treat zeros as stock.
    """
    section = ROOT / "out" / "raw" / "section_3_MAIN_OS.bin"
    if section.exists():
        return None
    section.parent.mkdir(parents=True, exist_ok=True)
    section.write_bytes(b"\0" * (8 * 1024 * 1024))
    print("gen_pages: no MAIN OS section; wrote ephemeral stock_guard stub "
          "(site/credits only)", file=sys.stderr)
    return section


def main(quiet: bool = False) -> int:
    import gen_manual
    import release
    import shutil
    stub = _ensure_site_stock_stub()
    try:
        mods = registry.modules()
        official = [(n, registry.remix(n)) for n in release.REMIXES]
        if OUT.exists():
            shutil.rmtree(OUT)
        OUT.mkdir(parents=True, exist_ok=True)
        jobs = {}
        manual_page = gen_manual.published_pages(mods, official)
        site_keys = _site_keys()
        jobs["modules.md"] = directory_page(mods, manual_page)
        jobs["_credits-shipped.md"] = shipped_credits_page(mods)
        for m in mods.values():
            if m.key not in site_keys:
                continue
            jobs[f"modules/{m.name}.md"] = module_page(m, mods, manual_page)
        for name, r in official:
            jobs[f"_remix-{name}.md"] = "\n".join(gen_manual.remix_table(name, r, mods)) + "\n"
        if official:
            jobs.update(gen_manual.main(mods, official))
        for name, text in sorted(jobs.items()):
            (OUT / name).parent.mkdir(parents=True, exist_ok=True)
            (OUT / name).write_text(text)
            if not quiet:
                print(f"wrote docs/site/reference/{name}")
    finally:
        if stub is not None and stub.exists():
            stub.unlink()
            print("gen_pages: removed ephemeral stock_guard stub", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
