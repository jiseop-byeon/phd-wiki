#!/usr/bin/env python3
"""Assign the wiki-wide study-depth profile to substantive content pages.

★/◐/○ describes how much of a paper to read. These fields describe how well a
construction-Physical-AI researcher should be able to use the knowledge.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"

WORKING_PAPERS = {
    # Reusable deep-learning backbone and optimization knowledge.
    "adam", "batch-norm", "attention-is-all-you-need", "resnet", "vit", "lora",
    "ppo", "sac",
    # Perception and geometry used directly by field robots.
    "yolo", "detr", "sam", "dino", "depth-anything", "pointnet", "nerf",
    "3d-gaussian-splatting", "vggt",
    # Multimodal and robot-learning interfaces.
    "clip", "qwen-vl", "act", "diffusion-policy", "gr00t-n1", "octo",
    "open-x-embodiment", "openvla", "pi0", "rt-1", "rt-2", "saycan",
    # Generative control and world-model tools.
    "dreamer", "vae", "ddpm", "ddim", "classifier-free-guidance",
    "flow-matching", "dit", "latent-diffusion",
    # Domain papers used to formulate construction-robotics research.
    "aes", "bim-digital-twin", "dry-stone-wall", "ext", "heap",
    "stentz-excavator", "vision-guided-assembly", "wheel-loader-rl",
}


def profile(path: Path) -> tuple[str, str, str] | None:
    rel = path.relative_to(CONTENT)
    parts = rel.parts
    stem = path.stem

    if rel.as_posix() in {"index.md", "study-log.md", "08-research-radar/index.md"}:
        return None
    if parts[0] == "templates":
        return None

    if "notes" in parts and stem != "index":
        if stem in WORKING_PAPERS:
            return (
                "Working",
                "Read the method and evaluation closely enough to select, adapt, or diagnose it.",
                "Raise to Mastery only when this method or its assumptions become part of the thesis contribution.",
            )
        return (
            "Literacy",
            "Explain the problem, inputs and outputs, central claim, evidence, and one limitation.",
            "Raise to Working when the paper becomes a baseline, dependency, or implementation choice.",
        )

    if parts[0] == "02-foundations":
        if stem in {"overview", "information-theory"}:
            return (
                "Literacy",
                "Read the notation and recurring ideas accurately; return for deeper derivations when a paper requires them.",
                "Raise to Working or Mastery when the thesis objective depends directly on these formulations.",
            )
        return (
            "Working",
            "Use the notation, equations, and diagnostic ideas while reading methods and designing experiments.",
            "Raise to Mastery only for the mathematical or estimation component that carries the thesis novelty.",
        )

    if parts[0] == "03-deep-learning":
        return (
            "Literacy",
            "Use the map to locate a method historically and explain how neighboring research streams connect.",
            "Raise the specific downstream method pages—not the whole map—to Working or Mastery.",
        )

    if parts[0] == "04-robotics":
        if stem in {"index", "modern-robotics-book"}:
            return (
                "Literacy",
                "Understand the track structure and identify which robotics tool a paper assumes.",
                "Raise the chapters and tools used by the thesis to Working; master only the contribution-bearing subsystem.",
            )
        if stem == "convex-mpc-legged":
            return (
                "Literacy",
                "Read the MPC formulation and recognize its assumptions and role in a complete robot system.",
                "Raise to Working or Mastery when legged control or MPC design is used directly.",
            )
        return (
            "Working",
            "Follow the formulation, frames, assumptions, and failure modes well enough to use or evaluate the tool.",
            "Raise to Mastery when this subsystem is modified, defended, or claimed as a thesis contribution.",
        )

    if parts[0] == "05-construction-robotics":
        if stem in {"index", "lineage", "labs", "industry-deployment"}:
            return (
                "Literacy",
                "Explain the domain landscape, research lineage, actors, and deployment constraints.",
                "Raise the chosen construction task and system layer to Working or Mastery.",
            )
        return (
            "Working",
            "Use the task taxonomy, system assumptions, and evaluation criteria to formulate construction-robotics research.",
            "Raise to Mastery when this task stream or deployment layer is the thesis contribution.",
        )

    if parts[0] == "06-research-practice":
        if stem == "index":
            return (
                "Literacy",
                "Use this page to navigate the research workflow and its completion criteria.",
                "Apply the individual practice pages at Working level throughout the project.",
            )
        return (
            "Working",
            "Apply the procedure when forming claims, running experiments, analyzing failure, and writing.",
            "Mastery means consistently producing defensible work, not memorizing the page.",
        )

    if rel.as_posix() == "glossary.md":
        return (
            "Literacy",
            "Distinguish neighboring terms and read them consistently across papers.",
            "Raise a term to Working through its linked concept or method page when it enters daily use.",
        )

    if parts[0] == "01-canonical-papers":
        return (
            "Literacy",
            "Use this map or guide to choose reading order, reading volume, and evidence checks.",
            "Working and Mastery are assigned on the individual concept or paper pages.",
        )

    return None


def update_frontmatter(path: Path, values: tuple[str, str, str]) -> bool:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---", text, re.S)
    if not match:
        return False
    frontmatter = match.group(1)
    for key in ("study-depth", "depth-goal", "mastery-when"):
        frontmatter = re.sub(rf"^{re.escape(key)}:.*\n?", "", frontmatter, flags=re.M)
    depth, goal, mastery = values
    additions = "\n".join(
        [
            f"study-depth: {depth}",
            f"depth-goal: {json.dumps(goal, ensure_ascii=False)}",
            f"mastery-when: {json.dumps(mastery, ensure_ascii=False)}",
        ]
    )
    frontmatter = frontmatter.rstrip() + "\n" + additions
    updated = text[: match.start(1)] + frontmatter + text[match.end(1) :]
    if updated == text:
        return False
    path.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    assigned = changed = 0
    for path in sorted(CONTENT.rglob("*.md")):
        values = profile(path)
        if values is None:
            continue
        assigned += 1
        changed += update_frontmatter(path, values)
    print(f"Study-depth profile assigned to {assigned} pages; {changed} files changed.")


if __name__ == "__main__":
    main()
