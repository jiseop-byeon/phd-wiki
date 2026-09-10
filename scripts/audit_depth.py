#!/usr/bin/env python3
"""Depth-assignment conformance — a page sitting deeper than the study guide
allows for its area.

Imported by verify_content.py as check 14, and runnable on its own.

The 2026-09-09 full-wiki evaluation reported that `study-depth` had drifted:
136 Working / 72 Literacy / 7 Mastery, with the worry that "Working has become
the default, which blunts the filter".  That worry is decidable, because the
guide states its own defaults in two tables:

  * the generic area table in `00-study-depth-guide.md` ("Area | Default | …"),
    which prescribes Working for nine of its twelve rows, so a Working majority
    is what the table produces, not evidence against it;
  * the sharper "Profile: construction manipulation" table, whose last row
    sends broader RL theory, generic VLM topics, world models, diffusion
    internals, and autonomy topics outside manipulation to Literacy.

This check reads both tables out of the guide and fails when a page sits
*above* the depth its area allows.  Sitting below is never an error — Literacy
where the guide would permit Working is the conservative direction, and 40
pages currently do that.

Like check 12, it also fails if a table row's wording changes, so the check
cannot be silently retired by editing the guide.

    python3 scripts/audit_depth.py        # from the repo root
"""
import os, re, sys, glob

ORDER = {"Literacy": 0, "Working": 1, "Mastery": 2}
GUIDE = os.path.join("content", "00-study-depth-guide.md")

# Area rows of the generic table, each mapped to the paths it governs.  The
# guide names areas in prose; only this repo knows which files they are, so the
# mapping lives here and the *defaults* are read from the guide.
AREA_PATHS = {
    "Engineering math, linear algebra, calculus, probability, optimization": (
        "02-foundations/engineering-math", "02-foundations/linear-algebra",
        "02-foundations/calculus-backprop", "02-foundations/probability",
        "02-foundations/optimization"),
    "Information theory": ("02-foundations/information-theory",),
    "Signal processing, state estimation, calibration, SE(3)": (
        "02-foundations/signal-processing", "02-foundations/se3-geometry",
        "04-robotics/state-estimation-slam",
        "04-robotics/geometric-perception-calibration"),
    "Deep-learning history and ecosystem maps": ("03-deep-learning/",),
    "VLM": ("notes/3-vlm/",),
    "Diffusion, flow matching, world models": (
        "notes/6-diffusion/", "notes/5-world-models/"),
    "Construction lineage, labs, industry map": (
        "05-construction-robotics/lineage", "05-construction-robotics/labs",
        "05-construction-robotics/industry-deployment"),
    "Research practice": ("06-research-practice/",),
}

# The profile table's Literacy row, which is stricter than the generic table
# for these files.  Navigation itself is Working by the profile's own Working
# row, so only the topics with no manipulation path are listed.
PROFILE_LITERACY_PATHS = (
    "notes/5-world-models/", "notes/6-diffusion/", "notes/3-vlm/",
)

# Deliberate promotions above the area default, each with the reason the guide
# or the research program gives.  A page may only exceed its default if it is
# named here.
PROMOTED = {
    "notes/6-diffusion/ddpm": "the objective Diffusion Policy runs on",
    "notes/6-diffusion/ddim": "the sampler Diffusion Policy runs on",
    "notes/6-diffusion/classifier-free-guidance": "conditioning used by the manipulation policies",
    "notes/6-diffusion/flow-matching": "the objective pi-0 runs on",
    "notes/6-diffusion/dit": "the backbone the VLA notes assume",
    "notes/6-diffusion/vae": "latent action spaces in the VLA track",
    "notes/3-vlm/clip": "the encoder row the guide sends to Working",
    "notes/3-vlm/qwen-vl": "the encoder row the guide sends to Working",
}


def _table_defaults(text):
    """Read the generic area table; return {area: default cell}."""
    rows = {}
    for line in text.splitlines():
        m = re.match(r"^\|\s*([^|]+?)\s*\|\s*(Literacy|Working)([^|]*)\|", line)
        if m and m.group(1) not in ("Area", "Depth"):
            rows[m.group(1)] = (m.group(2) + m.group(3)).strip()
    return rows


def _profile_literacy_row(text):
    for line in text.splitlines():
        if line.startswith("| **Literacy, raised to Working on demand**"):
            return line
    return None


def audit():
    problems = []
    try:
        guide = open(GUIDE, encoding="utf-8").read()
    except OSError:
        return [(GUIDE, "missing: depth conformance cannot be checked")]

    defaults = _table_defaults(guide)
    for area in AREA_PATHS:
        if area not in defaults:
            problems.append((GUIDE, f"area row {area!r} not found — the table wording "
                                    f"changed, so its check no longer applies. "
                                    f"Update AREA_PATHS in scripts/audit_depth.py"))
    if _profile_literacy_row(guide) is None:
        problems.append((GUIDE, "the profile table's Literacy row not found — update "
                                "PROFILE_LITERACY_PATHS in scripts/audit_depth.py"))
    if problems:
        return problems

    ceiling = {}          # path fragment -> (allowed depth, area name)
    for area, frags in AREA_PATHS.items():
        cell = defaults[area]
        # "Literacy; selected encoders at Working" and "Literacy broadly;
        # directly used methods at Working" both cap at Literacy plus a named
        # exception list, which PROMOTED carries.
        allowed = "Literacy" if cell.startswith("Literacy") else "Working"
        for f in frags:
            ceiling[f] = (allowed, area)
    for f in PROFILE_LITERACY_PATHS:
        ceiling[f] = ("Literacy", "profile table, Literacy row")

    for p in sorted(glob.glob("content/**/*.md", recursive=True)):
        body = open(p, encoding="utf-8").read()
        m = re.search(r"^study-depth:\s*(\S+)", body, re.M)
        if not m:
            continue
        depth = m.group(1)
        if depth not in ORDER:
            problems.append((p, f"study-depth: {depth} is not one of Literacy/Working/Mastery"))
            continue
        rel = p.replace(os.sep, "/")
        for frag, (allowed, area) in ceiling.items():
            if frag not in rel:
                continue
            if ORDER[depth] <= ORDER[allowed]:
                continue
            if any(k in rel for k in PROMOTED):
                continue
            problems.append((p, f"study-depth: {depth} sits above the guide's default "
                                f"({allowed}) for {area!r}, and the page is not in the "
                                f"documented PROMOTED set"))
    return problems


if __name__ == "__main__":
    found = audit()
    for f, msg in found:
        print(f" - {f}: {msg}")
    print(f"\n{len(found)} page(s) deeper than the study guide allows.")
    sys.exit(1 if found else 0)
