#!/usr/bin/env python3
"""Draw the three figures of content/physical-ai-map.md from one table of pages.

The map is the picture each course page's "Why this matters" callout points to:
the stack of 7. Research Program §5 drawn as bands of page chips, with the three
floors beneath it (tools, mathematics, physics), research practice beside it and
the dissertation path of §8 marked on it. The table below is the single source of
truth for the page's figures; the prose around them is written by hand.

    python3 scripts/build_physical_ai_map.py          # redraw the figures in the page
    python3 scripts/build_physical_ai_map.py --check  # exit 1 if the page is stale

Before it draws anything it compares the table with the wiki and stops with exit
status 2 when they disagree:

  * a slug that is not a page: content/<slug>.md, or content/<slug>index.md for a
    folder link, which is written with a trailing "/";
  * a chip whose number is not the number its page's own title carries, so a
    renumbered page cannot keep its old chip;
  * a block whose Working or Literacy count is not the one in the table of 7 §8,
    or totals that are not the ones §8's "Reading the table" states — when §8
    changes, BLOCKS and TOTALS below are the one place to update;
  * a week-2/week-3 split of block 2 that is not where 5. Control Theory starts in
    the robotics schedule.

It also estimates the width of every label (Arial advances, a Hangul syllable at
one em; both are wider than the site's Source Sans Pro) and stops with exit status
3 when a label would overflow the box drawn for it. It rewrites only the lines
between <!-- MAP:figN:LANG:BEGIN --> and <!-- MAP:figN:LANG:END -->, and it names
any course page that has no chip yet. Standard library only.
"""
import os
import re
import sys
from collections import Counter, namedtuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
PAGE = os.path.join(CONTENT, "physical-ai-map.md")
PROGRAM_PAGE = os.path.join(CONTENT, "07-research-program", "index.md")
ROBOTICS_PAGE = os.path.join(CONTENT, "04-robotics", "index.md")


# =============================================================================
# THE TABLE
# =============================================================================

# Where you are now: a week of the four-week improvement plan (WEEKS, below).
# Figure 1 pins the band that holds most of that week's pages, figure 2 its row,
# figure 3 the first bar the week prepares. Move it when the week changes.
YOU_ARE_HERE = 2

# One chip per page: (key, label, slug, on_path, block)
#   key      how STEPS and WEEKS name the chip: a track tag, a colon, the number
#   label    the page's number as its own title writes it ("MR 12" for "MR Ch.12");
#            a chip drawn outside its own track carries the track ("DL 1.4")
#   slug     the path under content/ without ".md"; a folder link ends in "/"
#            and opens that folder's index.md
#   on_path  True when 7. Research Program §8 puts the page on the dissertation
#            path, and block is then its block there (1-7); otherwise None.
#            Read off §8's table and the track schedules it cites: robotics
#            sessions 1-104, deep learning 1-3, 11-13, 35-44, research practice
#            4-6 and 14, construction 3-6, 12-15, 21-25, 30, 33, 37-47.

# The goal: construction, the track everything below exists for.
GOAL = (
    ("c:1", "1", "05-construction-robotics/lineage", False, None),
    ("c:2", "2", "05-construction-robotics/labs", False, None),
    ("c:2.5", "2.5", "05-construction-robotics/site-engineering", True, 6),
    ("c:3", "3", "05-construction-robotics/earthmoving-heavy-machinery", False, None),
    ("c:4", "4", "05-construction-robotics/assembly-fabrication", True, 6),
    ("c:5", "5", "05-construction-robotics/site-perception", False, None),
    ("c:6", "6", "05-construction-robotics/hrc-worker-centered", True, 6),
    ("c:7", "7", "05-construction-robotics/digital-twin-workflows", False, None),
    ("c:7.5", "7.5", "05-construction-robotics/sim-to-real", True, 6),
    ("c:8", "8", "05-construction-robotics/industry-deployment", False, None),
    ("c:9", "9", "05-construction-robotics/construction-manipulation", True, 6),
    ("c:10", "10", "05-construction-robotics/imitating-contact", True, 7),
)
PROGRAM = (
    ("p:7", "7", "07-research-program/", False, None),
)

# Learning and adaptation: the deep-learning track (1.4 sits on the tools floor).
LEARNING = (
    ("d:1", "1", "03-deep-learning/foundations/", True, 4),
    ("d:1.1", "1.1", "03-deep-learning/foundations/sequence-models", False, None),
    ("d:1.2", "1.2", "03-deep-learning/foundations/attention-transformer", False, None),
    ("d:1.3", "1.3", "03-deep-learning/foundations/training-at-scale", False, None),
    ("d:2", "2", "03-deep-learning/computer-vision/", True, 4),
    ("d:3", "3", "03-deep-learning/vlm/", True, 4),
    ("d:4", "4", "03-deep-learning/vla/", True, 4),
    ("d:5", "5", "03-deep-learning/world-models/", False, None),
    ("d:6", "6", "03-deep-learning/diffusion/", False, None),
    ("d:6.1", "6.1", "03-deep-learning/diffusion/vae-gan", False, None),
)

# The robot stack: the layers of 7 §5, drawn top to bottom, so its flow
# perception -> scene -> grasping -> planning -> manipulation -> contact runs up.
MR = "04-robotics/modern-robotics/"
STACK = (
    ("loop", "the loop, closed", "닫힌 루프", (
        ("r:26", "26", "04-robotics/capstone-panel-contact", True, 2),
    )),
    ("contact", "contact and force", "접촉과 힘", (
        ("r:9", "9", "04-robotics/contact-force-tactile", True, 2),
        ("r:13", "13", "04-robotics/force-compliance-control", True, 3),
        ("r:14", "14", "04-robotics/tactile-visuotactile", False, None),
        ("r:24", "24", "04-robotics/haptics-teleoperation/", False, None),
    )),
    ("manipulation", "manipulation", "조작", (
        ("r:1", "1", "04-robotics/modern-robotics-book", True, 2),
        ("r:2", "2", MR, True, 2),
        ("mr:3", "MR 3", MR + "ch03-rigid-body-motions", True, 2),
        ("mr:4", "MR 4", MR + "ch04-forward-kinematics", True, 2),
        ("mr:5", "MR 5", MR + "ch05-velocity-kinematics", True, 2),
        ("mr:6", "MR 6", MR + "ch06-inverse-kinematics", True, 2),
        ("mr:8", "MR 8", MR + "ch08-dynamics", True, 2),
        ("r:12", "12", "04-robotics/teleoperation-demonstration", True, 3),
    )),
    ("planning", "planning", "계획", (
        ("mr:2", "MR 2", MR + "ch02-configuration-space", True, 2),
        ("r:4", "4", "04-robotics/planning-decision-making", True, 2),
        ("mr:9", "MR 9", MR + "ch09-trajectory-generation", True, 2),
        ("mr:10", "MR 10", MR + "ch10-motion-planning", True, 2),
        ("r:16", "16", "04-robotics/navigation-mobile-manipulation", False, None),
        ("r:19", "19", "04-robotics/semantic-language-navigation", False, None),
        ("mr:13", "MR 13", MR + "ch13-wheeled-mobile-robots", False, None),
    )),
    ("grasping", "grasping", "파지", (
        ("r:15", "15", "04-robotics/grasping", True, 3),
        ("mr:12", "MR 12", MR + "ch12-grasping", True, 3),
    )),
    ("scene", "scene and state", "장면과 상태", (
        ("r:3", "3", "04-robotics/state-estimation-slam", True, 2),
        ("r:17", "17", "04-robotics/traversability-off-road", False, None),
        ("r:23", "23", "04-robotics/human-intent-prediction", False, None),
    )),
    ("perception", "perception", "인식", (
        ("r:3.2", "3.2", "04-robotics/sensor-models", True, 2),
        ("r:3.5", "3.5", "04-robotics/geometric-perception-calibration", True, 2),
        ("r:3.6", "3.6", "04-robotics/perception-sensors-rigs", True, 2),
        ("r:20", "20", "04-robotics/video-action-understanding", False, None),
        ("r:21", "21", "04-robotics/human-pose-gaze", False, None),
        ("r:22", "22", "04-robotics/egocentric-perception", False, None),
        ("r:23.5", "23.5", "04-robotics/xr-human-robot-collaboration", False, None),
    )),
)
LOOP_NOTE = ("capstone: the classical baseline a learned policy must beat",
             "캡스톤: 학습된 정책이 이겨야 할 고전 기준선")
# Beside the stack: control, and the systems that keep every layer on time and safe.
CONTROL = (
    ("r:5", "5", "04-robotics/control-theory-ce397", True, 2),
    ("r:5.5", "5.5", "04-robotics/system-identification", True, 2),
    ("mr:11", "MR 11", MR + "ch11-robot-control", True, 2),
    ("r:6", "6", "04-robotics/lqr-lqg", True, 2),
    ("r:7", "7", "04-robotics/mpc", True, 2),
    ("r:8", "8", "04-robotics/convex-mpc-legged", True, 2),
    ("r:18", "18", "04-robotics/legged-locomotion", False, None),
)
SYSTEMS = (
    ("r:10", "10", "04-robotics/robot-systems-deployment", True, 2),
    ("r:10.5", "10.5", "04-robotics/actuators-drives", True, 2),
    ("r:11", "11", "04-robotics/hri-safety", True, 2),
    ("r:25", "25", "04-robotics/ros2/", False, None),
)

# The three floors, top to bottom: physics, mathematics, tools.
PHYSICS = (
    ("f:0.6.1", "0.6.1", "02-foundations/basic-mechanics", False, None),
    ("f:0.6.2", "0.6.2", "02-foundations/basic-circuits-electronics", False, None),
    ("f:0.6.3", "0.6.3", "02-foundations/fluid-power", False, None),
)
MATH = (   # the path starts at the gate of 0. Overview, which checks 0.5-9
    ("f:0", "0", "02-foundations/overview", True, 1),
    ("f:0.5", "0.5", "02-foundations/engineering-math", False, None),
    ("f:0.8", "0.8", "02-foundations/neural-network-basics", False, None),
    ("f:1", "1", "02-foundations/linear-algebra", False, None),
    ("f:2", "2", "02-foundations/calculus-backprop", False, None),
    ("f:3", "3", "02-foundations/probability", False, None),
    ("f:4", "4", "02-foundations/optimization", False, None),
    ("f:5", "5", "02-foundations/information-theory", False, None),
    ("f:6", "6", "02-foundations/signal-processing", False, None),
    ("f:7", "7", "02-foundations/rl-basics", False, None),
    ("f:7.5", "7.5", "02-foundations/rl-robot-learning", True, 4),
    ("f:8", "8", "02-foundations/se3-geometry", False, None),
    ("f:9", "9", "02-foundations/ml-practice", False, None),
    ("f:10", "10", "02-foundations/manipulator-kinematics-dynamics", True, 1),
)
TOOLS = (
    ("t:11", "11", "02-foundations/algorithms/", False, None),
    ("t:12", "12", "02-foundations/tools/", False, None),
    ("t:12.1", "12.1", "02-foundations/tools/linux-shell", False, None),
    ("t:12.2", "12.2", "02-foundations/tools/git-research-code", False, None),
    ("t:12.3", "12.3", "02-foundations/tools/python-research-code", False, None),
    ("t:12.4", "12.4", "02-foundations/tools/config-data-formats", False, None),
    ("t:12.5", "12.5", "02-foundations/tools/computer-networks", False, None),
    ("t:12.6", "12.6", "02-foundations/tools/latex-figures-references", False, None),
    ("t:12.7", "12.7", "02-foundations/tools/gpu-clusters", False, None),
    ("t:12.8", "12.8", "02-foundations/tools/concurrency", False, None),
    ("t:12.9", "12.9", "02-foundations/tools/mechanical-design-fabrication", False, None),
    ("t:25.0", "25.0", "04-robotics/ros2/cpp-for-robot-code", False, None),
    ("t:1.4", "DL 1.4", "03-deep-learning/foundations/gpu-computing", False, None),
)

# Research practice, beside every layer. 2 and 4's worked case are block 5; the
# rest is block 8 of §8, which runs alongside the path rather than on it.
PRACTICE = (
    ("rp:1", "1", "06-research-practice/research-questions-claims", False, None),
    ("rp:2", "2", "06-research-practice/experimental-design-reproducibility", True, 5),
    ("rp:3", "3", "06-research-practice/failure-analysis-system-evaluation", False, None),
    ("rp:4", "4", "06-research-practice/scientific-writing-peer-review", True, 5),
    ("rp:5", "5", "06-research-practice/venue-strategy", False, None),
    ("rp:6", "6", "06-research-practice/real-world-impact", False, None),
    ("rp:7", "7", "06-research-practice/simulators-benchmarks-datasets", False, None),
    ("rp:8", "8", "06-research-practice/psychophysics-human-measurement", False, None),
)

# Band names: (name, track, why the layer is needed), English then Korean.
BANDS = {
    "goal": (("the goal", "“install that panel on the frame”",
              "what everything below is for"),
             ("목표", "“저 패널을 프레임에 설치해”", "아래의 모든 것이 향하는 곳")),
    "learning": (("learning and adaptation", "deep learning",
                  "improves the policy from data and demonstrations"),
                 ("학습과 적응", "딥러닝", "데이터와 시연으로 정책을 개선한다")),
    "stack": (("the robot stack", "robotics, with Modern Robotics (MR)",
               "each layer hands its result to the one above it"),
              ("로봇 스택", "로보틱스와 Modern Robotics(MR)", "각 층이 결과를 위의 층에 넘긴다")),
    "physics": (("physics floor", "foundations 0.6.1–0.6.3",
                 "what the robot's body, its drives and the panel obey"),
                ("물리 바닥", "기초 0.6.1–0.6.3", "로봇의 몸과 구동계, 그리고 패널이 따르는 법칙")),
    "math": (("mathematics floor", "foundations 0–10",
              "the language every layer is written in"),
             ("수학 바닥", "기초 0–10", "모든 층이 쓰이는 언어")),
    "tools": (("tools floor", "foundations 11–12, 25.0 C++, DL 1.4 GPU",
               "what every layer runs on, and how its results are kept"),
              ("도구 바닥", "기초 11–12, 25.0 C++, DL 1.4 GPU", "모든 층이 도는 바탕, 그리고 결과를 남기는 법")),
    "practice": (("research", "practice", "alongside"), ("연구", "실무", "나란히")),
}
GROUPS = {
    "goal": ((("construction", "건설"), GOAL), (("program", "연구 프로그램"), PROGRAM)),
    "learning": ((None, LEARNING),),
    "physics": ((None, PHYSICS),),
    "math": ((None, MATH),),
    "tools": ((None, TOOLS),),
}
SIDE = ((("control", "제어"), CONTROL), (("systems", "시스템"), SYSTEMS))

# Figure 2: the eight steps of 7 §5's worked instance, "Install that panel on the
# frame": (step, its layer, the chips that power it), English lines then Korean.
# A chip lands in the row of its band, so the column reads down to the floors.
# Where a page's own "Why this matters" callout names its steps, the column follows
# it (12.6 names none: it carries the evidence about the steps to a reader).
STEPS = (
    (("resolve the", "instruction"), ("지시를", "해석"),
     ("learning and", "adaptation"), ("학습과", "적응"),
     ("d:3", "d:1.2", "r:19", "f:5", "f:0.8", "t:1.4")),
    (("identify", "panel and", "frame"), ("패널과", "프레임을", "식별"),
     ("perception,", "scene, state"), ("인식,", "장면과 상태"),
     ("c:5", "c:7", "d:2", "r:3", "r:3.2", "r:3.5", "r:3.6", "f:8", "f:1", "f:3",
      "f:6", "f:4", "t:12.5", "t:12.8", "t:12.9")),
    (("decompose", "the job"), ("작업을", "분해"),
     ("planning:", "the task"), ("계획:", "과제"),
     ("c:2.5", "c:7", "d:4", "r:4", "f:4", "f:7", "t:11")),
    (("plan a", "grasp"), ("파지를", "계획"),
     ("grasping",), ("파지",),
     ("mr:12", "r:15", "r:16", "f:0.6.1", "f:0.6.3", "f:4", "f:8")),
    (("move the", "component"), ("부재를", "옮김"),
     ("planning,", "manipulation"), ("계획,", "조작"),
     ("mr:2", "mr:3", "mr:4", "mr:5", "mr:6", "mr:8", "mr:9", "r:4", "mr:10", "r:5",
      "mr:11", "r:10.5", "f:0.6.1", "f:0.6.2", "f:0.6.3", "f:2", "f:8", "f:10", "f:4",
      "f:0.5", "f:1", "t:25.0", "t:12.1", "t:12.8", "t:12.5")),
    (("detect", "contact"), ("접촉을", "감지"),
     ("contact and", "force"), ("접촉과 힘",),
     ("mr:3", "mr:5", "r:3.2", "r:9", "r:14", "f:0.6.1", "f:0.6.2", "f:6", "f:3",
      "f:10", "f:0.5", "t:12.3", "t:25.0", "t:12.1", "t:12.8")),
    (("perform the", "fitting"), ("끼움을", "수행"),
     ("contact,", "learning"), ("접촉,", "학습"),
     ("c:4", "c:9", "c:10", "c:7.5", "d:4", "mr:5", "r:3.5", "r:3.6", "r:12", "r:13",
      "rp:7", "f:0.6.1", "f:7.5", "f:10", "f:0.5", "f:2", "f:7", "t:12.7", "t:12.4",
      "t:25.0", "t:12.9")),
    (("verify", "completion"), ("완료를", "검증"),
     ("task", "completion"), ("작업 완료",),
     ("c:2.5", "c:5", "c:6", "rp:2", "rp:3", "f:3", "f:9", "f:7.5", "t:12.2", "t:12.3",
      "t:12.4")),
)

# The four-week plan that improves the pages just ahead of the owner's study.
WEEKS = {
    1: ("foundations and the gate", "기초와 통과 점검",
        ("f:0", "f:0.5", "f:0.8", "f:1", "f:2", "f:3", "f:4", "f:5", "f:6", "f:7", "f:7.5",
         "f:8", "f:9", "f:10")),
    2: ("robotics common, first half", "로보틱스 공통 앞 절반",
        ("r:1", "r:2", "mr:2", "mr:3", "mr:4", "mr:5", "mr:6", "mr:8", "mr:9", "r:3",
         "r:3.2", "r:3.5", "r:3.6", "r:4", "mr:10")),
    3: ("robotics common, second half, and deep learning 1–4",
        "로보틱스 공통 뒤 절반과 딥러닝 1–4",
        ("r:5", "r:5.5", "mr:11", "r:6", "r:7", "r:8", "r:9", "r:10", "r:10.5", "r:11",
         "r:26", "d:1", "d:2", "d:3", "d:4")),
    4: ("manipulation, construction and research practice", "매니퓰레이션, 건설, 연구 실무",
        ("r:12", "r:13", "r:15", "mr:12", "c:2.5", "c:4", "c:6", "c:9", "c:10", "rp:2",
         "rp:4")),
}

# Figure 3: the blocks of 7 §8, with Working and Literacy exactly as §8's table
# writes them, and the bar cut into (sessions, week of the plan that prepares
# them). Block 1 is "1 + 6", the gate and 10; block 2's cut is where 5. Control
# Theory starts in the robotics schedule; block 4 is "3 + 16", 7.5 and then deep
# learning 1-4; in block 6 the two 7.5 sessions (construction 30 and 33) lie
# between 6 and 9 and are not in the plan.
BLOCKS = (
    (1, "the gate, then 10", "통과 점검, 그다음 10", "1 + 6", "1 + 1", ((1, 1), (6, 1))),
    (2, "robotics common, to the capstone", "캡스톤까지 로보틱스 공통", "104", "41",
     ((60, 2), (44, 3))),
    (3, "12, 13 and 15, with MR 12", "12, 13, 15와 MR 12장", "about 20", "4", ((20, 4),)),
    (4, "7.5 RL §1, §4, then deep learning 1–4",
     "7.5 RL §1·§4, 그다음 딥러닝 1–4", "3 + 16", "1 + 8", ((3, 1), (16, 3))),
    (5, "research practice 2, and 4's worked case", "연구 실무 2와 4의 끝까지 계산",
     "4", "4", ((4, 4),)),
    (6, "construction 2.5, 4, 6, 9, with 7.5 §7–§8",
     "건설 2.5, 4, 6, 9와 7.5 §7–§8", "20", "9", ((13, 4), (2, None), (5, 4))),
    (7, "10. Imitating Contact", "10. 접촉 모방", "6", "2", ((6, 4),)),
    (8, "the rest of research practice", "연구 실무의 나머지", "32", "16", ()),
)
# §8's "Reading the table": blocks 1-7 at Working and Literacy, block 8, all, and
# the weeks each pass takes at two course sessions a week.
TOTALS = dict(working=180, literacy=71, alongside=32, all=212, weeks_working=90,
              weeks_literacy=36)


# =============================================================================
# Checking the table against the wiki
# =============================================================================

Chip = namedtuple("Chip", "key label slug on_path block band")
TITLES = {}


def _registry():
    chips, dup = {}, []

    def put(rows, band):
        for key, label, slug, on_path, block in rows:
            if key in chips:
                dup.append(key)
            chips[key] = Chip(key, label, slug, on_path, block, band)

    put(GOAL, "goal")
    put(PROGRAM, "goal")
    put(LEARNING, "learning")
    for _rid, _en, _ko, rows in STACK:
        put(rows, "stack")
    for _name, rows in SIDE:
        put(rows, "stack")
    put(PHYSICS, "physics")
    put(MATH, "math")
    put(TOOLS, "tools")
    put(PRACTICE, "practice")
    return chips, dup


CHIPS, DUPLICATE_KEYS = _registry()


def page_file(slug):
    if slug.endswith("/"):
        return os.path.join(CONTENT, slug, "index.md")
    return os.path.join(CONTENT, slug + ".md")


def href(slug):
    return "./" + slug


def read_title(path):
    with open(path, encoding="utf-8") as fh:
        head = fh.read(6000)
    m = re.match(r"---\n(.*?)\n---", head, re.S)
    t = m and re.search(r"^title:\s*(.+?)\s*$", m.group(1), re.M)
    if not t:
        return None
    s = t.group(1)
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        s = s[1:-1]
    return s


def title_number(title):
    m = re.match(r"MR Ch\.0*(\d+)\b", title)
    if m:
        return "MR " + m.group(1)
    m = re.match(r"(\d+(?:\.\d+)*)\.?\s", title)
    return m.group(1) if m else None


def label_number(label):
    return label[3:] if label.startswith("DL ") else label


def count(cell):
    """Sessions a §8 cell stands for: '1 + 6' -> 7, 'about 20' -> 20."""
    return sum(int(n) for n in re.findall(r"\d+", cell))


def _halves(text):
    m = re.search(r"^## 한국어\s*$", text, re.M)
    return (text[:m.start()], text[m.start():]) if m else (text, "")


def _section8(half):
    m = re.search(r"^### 8\. .*?(?=^### 9\. )", half, re.M | re.S)
    return m.group(0) if m else ""


def _table_rows(section):
    rows = {}
    for line in section.splitlines():
        if re.match(r"^\| \d+ \|", line):
            cells = [c.strip() for c in line.replace("\\|", "\x00").strip().strip("|").split("|")]
            rows[int(cells[0])] = cells
    return rows


def validate():
    problems = []
    for key in DUPLICATE_KEYS:
        problems.append(f"chip key {key} is used twice")
    slugs = Counter(c.slug for c in CHIPS.values())
    for slug, n in slugs.items():
        if n > 1:
            problems.append(f"{slug} has {n} chips; a page is drawn once")
    for c in CHIPS.values():
        path = page_file(c.slug)
        if not os.path.exists(path):
            problems.append(f"chip {c.label} ({c.key}): no page at {os.path.relpath(path, ROOT)}")
            continue
        title = read_title(path)
        if not title:
            problems.append(f"chip {c.label}: {os.path.relpath(path, ROOT)} has no title")
            continue
        TITLES[c.slug] = title
        if title_number(title) != label_number(c.label):
            problems.append(f"chip {c.label} ({c.slug}): the page's title is {title!r}, "
                            f"so its number is {title_number(title)!r}")
        if c.on_path != (c.block in range(1, 8)):
            problems.append(f"chip {c.label} ({c.key}): on_path={c.on_path} but block={c.block}")
    for i, step in enumerate(STEPS, 1):
        for key in step[4]:
            if key not in CHIPS:
                problems.append(f"step {i} names {key}, which is not a chip")
    for week, (_en, _ko, keys) in WEEKS.items():
        for key in keys:
            if key not in CHIPS:
                problems.append(f"week {week} names {key}, which is not a chip")
    if YOU_ARE_HERE not in WEEKS:
        problems.append(f"YOU_ARE_HERE = {YOU_ARE_HERE!r} is not a week of WEEKS")

    # the path's numbers against 7 §8
    try:
        program = open(PROGRAM_PAGE, encoding="utf-8").read()
    except OSError:
        return problems + [f"missing {PROGRAM_PAGE}: the path's numbers cannot be checked"]
    en_half, ko_half = _halves(program)
    sec_en, sec_ko = _section8(en_half), _section8(ko_half)
    rows_en, rows_ko = _table_rows(sec_en), _table_rows(sec_ko)
    if not rows_en or not rows_ko:
        problems.append("7 §8's table not found in one of the halves: update _section8/_table_rows")
    for n, _e, _k, w_cell, l_cell, segs in BLOCKS:
        if n in rows_en:
            got = (rows_en[n][2], rows_en[n][3])
            if got != (w_cell, l_cell):
                problems.append(f"block {n}: 7 §8 writes Working {got[0]!r} and Literacy {got[1]!r}, "
                                f"the table here {w_cell!r} and {l_cell!r} - update BLOCKS")
        elif rows_en:
            problems.append(f"block {n} is not a row of 7 §8's table")
        if n in rows_ko:
            got = (re.findall(r"\d+", rows_ko[n][2]), re.findall(r"\d+", rows_ko[n][3]))
            if got != (re.findall(r"\d+", w_cell), re.findall(r"\d+", l_cell)):
                problems.append(f"block {n}: the Korean table of 7 §8 has {rows_ko[n][2]!r} / "
                                f"{rows_ko[n][3]!r}")
        if segs and sum(s for s, _w in segs) != count(w_cell):
            problems.append(f"block {n}: its bar is cut into {sum(s for s, _w in segs)} sessions, "
                            f"not {count(w_cell)}")
    if rows_en and set(rows_en) != {b[0] for b in BLOCKS}:
        problems.append(f"7 §8's table has blocks {sorted(rows_en)}; BLOCKS has "
                        f"{sorted(b[0] for b in BLOCKS)}")
    claims = (
        (r"Blocks 1–7 come to about (\d+) sessions at Working and (\d+) at Literacy",
         (TOTALS["working"], TOTALS["literacy"])),
        (r"block 8 adds (\d+) beside it, about (\d+) in all", (TOTALS["alongside"], TOTALS["all"])),
        (r"(\d+) sessions is about (\d+) weeks", (TOTALS["working"], TOTALS["weeks_working"])),
        (r"(\d+) sessions, about (\d+) weeks at that pace",
         (TOTALS["literacy"], TOTALS["weeks_literacy"])),
    )
    for pattern, expect in claims:
        m = re.search(pattern, sec_en)
        if not m:
            problems.append(f"7 §8 no longer says {pattern!r}: re-read §8, then update TOTALS "
                            f"and this pattern")
        elif tuple(int(g) for g in m.groups()) != expect:
            problems.append(f"7 §8 says {m.group(0)!r}; TOTALS has {expect}")
    path = [b for b in BLOCKS if b[0] <= 7]
    if sum(count(b[3]) for b in path) != TOTALS["working"]:
        problems.append("the Working counts of blocks 1-7 do not add up to TOTALS['working']")
    if sum(count(b[4]) for b in path) != TOTALS["literacy"]:
        problems.append("the Literacy counts of blocks 1-7 do not add up to TOTALS['literacy']")
    if TOTALS["working"] + TOTALS["alongside"] != TOTALS["all"]:
        problems.append("TOTALS: working + alongside is not all")

    # block 2's cut: week 3 starts where 5. Control Theory starts
    try:
        robotics = _halves(open(ROBOTICS_PAGE, encoding="utf-8").read())[0]
    except OSError:
        return problems + [f"missing {ROBOTICS_PAGE}"]
    sessions = []
    for line in robotics.splitlines():
        m = re.match(r"^\| (?:\*\*)?(\d+)(?:\*\*)? \|", line)
        if m:
            sessions.append((int(m.group(1)), line))
    block2 = next(b for b in BLOCKS if b[0] == 2)
    if len(sessions) != count(block2[3]):
        problems.append(f"the robotics schedule has {len(sessions)} sessions; block 2 counts "
                        f"{count(block2[3])}")
    first = next((n for n, line in sessions if "04-robotics/control-theory-ce397" in line), None)
    if first is None:
        problems.append("no session of the robotics schedule links 5. Control Theory, so the "
                        "week-2/week-3 cut of block 2 cannot be checked")
    elif first - 1 != block2[5][0][0]:
        problems.append(f"5. Control Theory starts at robotics session {first}, so week 2 covers "
                        f"{first - 1} sessions of block 2, not {block2[5][0][0]} - update BLOCKS")
    return problems


# Pages the map leaves out on purpose, and folders a group chip stands for.
NOT_ON_MAP = (
    "02-foundations/index", "02-foundations/lab-plants", "02-foundations/lab-kernel",
    "02-foundations/algorithms/", "03-deep-learning/index", "03-deep-learning/lab-objects",
    "03-deep-learning/lineage", "03-deep-learning/physical-ai-ecosystem", "04-robotics/index",
    "04-robotics/haptics-teleoperation/", "04-robotics/ros2/", "05-construction-robotics/index",
    "06-research-practice/index",
)
COURSE_TRACKS = ("02-foundations", "03-deep-learning", "04-robotics", "05-construction-robotics",
                 "06-research-practice")


def uncovered():
    drawn = {os.path.normpath(page_file(c.slug)) for c in CHIPS.values()}
    out = []
    for track in COURSE_TRACKS:
        for dirpath, _dirs, files in os.walk(os.path.join(CONTENT, track)):
            for fn in files:
                p = os.path.normpath(os.path.join(dirpath, fn))
                if not fn.endswith(".md") or p in drawn:
                    continue
                rel = os.path.relpath(p, CONTENT)[:-3].replace(os.sep, "/")
                if any(rel == x or (x.endswith("/") and rel.startswith(x)) for x in NOT_ON_MAP):
                    continue
                out.append(rel)
    return sorted(out)


# =============================================================================
# Drawing
# =============================================================================

ACCENT = "var(--secondary,currentColor)"
HIGHLIGHT = "var(--highlight,rgba(143,159,169,0.15))"

# Arial advance widths in thousandths of an em (the site's Source Sans Pro is
# narrower, so a label that fits here fits there).
_ADV = {}
for _chars, _w in (("'", 191), ("ijl", 222), ("|", 260), (" !,./:;I[\\]ft", 278),
                   ("()-r`", 333), ("{}", 334), ('"', 355), ("*", 389), ("^", 469),
                   ("Jcksvxyz", 500), ("0123456789#$?L_abdeghnopqu", 556),
                   ("+<=>~", 584), ("FTZ", 611), ("&ABEKPSVXY", 667), ("CDHNRUw", 722),
                   ("GOQ", 778), ("Mm", 833), ("%", 889), ("W", 944), ("@", 1015),
                   ("·", 278), ("–§", 556), ("“”", 333),
                   ("’", 222), ("—→↑≈", 1000)):
    for _c in _chars:
        _ADV[_c] = _w


def text_w(s, size, bold=False):
    total = 0.0
    for ch in s:
        if "가" <= ch <= "힣":
            total += 1000
        else:
            total += _ADV.get(ch, 600) * (1.06 if bold else 1.0)
    return total * size / 1000.0


def num(v):
    s = f"{v:.1f}"
    return s[:-2] if s.endswith(".0") else s


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def pack(widths, x0, x1, gap):
    """Greedy lines of (index, x); a line wraps before an item that would pass x1."""
    lines, cur, x = [], [], x0
    for i, w in enumerate(widths):
        if cur and x + w > x1 + 0.01:
            lines.append(cur)
            cur, x = [], x0
        cur.append((i, x))
        x += w + gap
    if cur:
        lines.append(cur)
    return lines


def chip_w(label, size, pad=4.0):
    return max(1.75 * size, text_w(label, size, bold=True) + 2 * pad)


class Fig:
    def __init__(self, n, lang, aria):
        self.n, self.lang, self.aria = n, lang, aria
        self.en = lang == "en"
        self.mid = f"pmap{n}a" + ("" if self.en else "k")
        self.out, self.problems = [], []
        self.add(f'<defs><marker id="{self.mid}" viewBox="0 0 10 10" refX="9" refY="5" '
                 f'markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" '
                 f'fill="currentColor"/></marker></defs>')

    def add(self, s):
        self.out.append(s)

    def fits(self, what, s, size, room, bold=False):
        w = text_w(s, size, bold)
        if w > room + 0.01:
            self.problems.append(f"figure {self.n} ({self.lang}): {what} {s!r} needs "
                                 f"{w:.0f} units, {room:.0f} available")
        return w

    def text(self, x, y, s, size, anchor=None, weight=None, opacity=None, italic=False,
             accent=False):
        a = [f'x="{num(x)}"', f'y="{num(y)}"', f'font-size="{size}"']
        if anchor:
            a.append(f'text-anchor="{anchor}"')
        if weight:
            a.append(f'font-weight="{weight}"')
        if italic:
            a.append('font-style="italic"')
        if opacity is not None:
            a.append(f'opacity="{opacity}"')
        if accent:
            a.append(f'style="fill:{ACCENT}"')
        self.add(f'<text {" ".join(a)}>{esc(s)}</text>')

    def arrow(self, x1, y1, x2, y2, width=1.3, opacity=None):
        op = f' stroke-opacity="{opacity}"' if opacity is not None else ""
        self.add(f'<line x1="{num(x1)}" y1="{num(y1)}" x2="{num(x2)}" y2="{num(y2)}" '
                 f'stroke="currentColor" stroke-width="{width}"{op} marker-end="url(#{self.mid})"/>')

    def svg(self, height):
        head = (f'<svg viewBox="0 0 560 {num(height)}" style="max-width:100%;height:auto" '
                f'role="img" aria-label="{esc(self.aria)}">')
        return "\n".join((head, '<g fill="currentColor">', *self.out, "</g>", "</svg>"))


def chip(fig, c, x, y, w, h, size, ring=False):
    """A page chip: a link to the page, its title on hover, heavier when on the path."""
    title = TITLES[c.slug]
    if c.on_path:
        title += (f" — on the dissertation path, block {c.block}" if fig.en
                  else f" — 학위논문 경로, 블록 {c.block}")
    if ring:
        fig.add(f'<rect x="{num(x - 2.5)}" y="{num(y - 2.5)}" width="{num(w + 5)}" '
                f'height="{num(h + 5)}" rx="4.5" fill="none" stroke-width="1.3" '
                f'stroke-dasharray="2.5 1.5" style="stroke:{ACCENT}"/>')
    look = ('fill-opacity="0.22" stroke-width="1.8"' if c.on_path
            else 'fill-opacity="0.05" stroke-width="0.8" stroke-opacity="0.8"')
    fig.add(f'<a href="{href(c.slug)}" data-no-popover="true"><title>{esc(title)}</title>'
            f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{h}" rx="3" '
            f'fill="currentColor" stroke="currentColor" {look}/>'
            f'<text x="{num(x + w / 2)}" y="{num(y + h / 2 + size * 0.36)}" font-size="{size}" '
            f'text-anchor="middle">{esc(c.label)}</text></a>')


def sample_chip(fig, x, y, label, heavy, size=10.5, h=16):
    """A chip drawn for the legend only: the look of a link chip, no link."""
    w = chip_w(label, size)
    look = ('fill-opacity="0.22" stroke-width="1.8"' if heavy
            else 'fill-opacity="0.05" stroke-width="0.8" stroke-opacity="0.8"')
    fig.add(f'<g style="color:{ACCENT}"><rect x="{num(x)}" y="{num(y)}" width="{num(w)}" '
            f'height="{h}" rx="3" fill="currentColor" stroke="currentColor" {look}/>'
            f'<text x="{num(x + w / 2)}" y="{num(y + h / 2 + size * 0.36)}" font-size="{size}" '
            f'font-weight="600" text-anchor="middle">{esc(label)}</text></g>')
    return w


def badge(fig, cx, cy, n, dashed=False):
    """A block of the path: a numbered circle in the path chips' style."""
    look = ('fill-opacity="0.06" stroke-width="1.1" stroke-dasharray="2 1.5"' if dashed
            else 'fill-opacity="0.22" stroke-width="1.5"')
    fig.add(f'<g style="color:{ACCENT}"><circle cx="{num(cx)}" cy="{num(cy)}" r="7.5" '
            f'fill="currentColor" stroke="currentColor" {look}/>'
            f'<text x="{num(cx)}" y="{num(cy + 3.6)}" font-size="10" font-weight="600" '
            f'text-anchor="middle">{n}</text></g>')


def pin(fig, x, y, label, size=11, lift=1):
    """A map pin whose point sits at (x, y), with its label to the right, lifted by `lift`."""
    fig.add(f'<path fill-rule="evenodd" d="M{num(x)} {num(y)}L{num(x - 4.3)} {num(y - 6.2)}'
            f'A4.9 4.9 0 1 1 {num(x + 4.3)} {num(y - 6.2)}ZM{num(x + 1.7)} {num(y - 8.6)}'
            f'a1.7 1.7 0 1 0 -3.4 0a1.7 1.7 0 1 0 3.4 0Z" style="fill:{ACCENT}"/>')
    if label:
        fig.text(x + 8, y - lift, label, size, weight=600, accent=True)
    return x + 8 + (text_w(label, size, True) if label else 0)


def here_label(fig):
    return "you are here" if fig.en else "지금 여기"


def here_info():
    keys = set(WEEKS[YOU_ARE_HERE][2])
    bands = Counter(CHIPS[k].band for k in keys)
    band = bands.most_common(1)[0][0]
    whole = len(bands) == 1
    return keys, band, whole, (set() if whole else keys)


def band_rect(fig, x, y, w, h, here=False, rx=7):
    if here:
        fig.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" '
                f'stroke-width="1.8" style="fill:{HIGHLIGHT};stroke:{ACCENT}"/>')
    else:
        fig.add(f'<rect x="{num(x)}" y="{num(y)}" width="{num(w)}" height="{num(h)}" rx="{rx}" '
                f'fill="currentColor" fill-opacity="0.035" stroke="currentColor" '
                f'stroke-opacity="0.4"/>')


def band_header(fig, bid, x0, x1, y, blocks, pinned):
    name, track, why = BANDS[bid][0 if fig.en else 1]
    right = x1 - 8
    if pinned:
        s = here_label(fig)
        right -= text_w(s, 11, True) + 8
        pin(fig, right, y + 16, s)
        right -= 12
    if blocks:
        lab = "path" if fig.en else "경로"
        cx = right - 7.5 - 18.5 * (len(blocks) - 1)
        for i, b in enumerate(blocks):
            badge(fig, cx + 18.5 * i, y + 11.5, b)
        right = cx - 7.5 - 4 - text_w(lab, 10)
        fig.text(right, y + 15, lab, 10, opacity=0.8)
        right -= 8
    tx = x0 + 8
    need = text_w(name, 11, True) + text_w(" · " + track, 11)
    if need > right - tx:
        fig.problems.append(f"figure 1 ({fig.lang}): band title {name!r} needs {need:.0f} "
                            f"units, {right - tx:.0f} available")
    fig.add(f'<text x="{num(tx)}" y="{num(y + 15)}" font-size="11"><tspan font-weight="600">'
            f'{esc(name)}</tspan> · {esc(track)}</text>')
    fig.fits("band note", why, 10, x1 - 8 - tx)
    fig.text(tx, y + 28, why, 10, italic=True, opacity=0.8)


def band_chips(bid):
    if bid == "stack":
        out = [CHIPS[r[0]] for _i, _e, _k, rows in STACK for r in rows]
        return out + [CHIPS[r[0]] for _n, rows in SIDE for r in rows]
    return [CHIPS[r[0]] for _g, rows in GROUPS[bid] for r in rows]


def path_blocks(bid):
    return sorted({c.block for c in band_chips(bid) if c.on_path})


def simple_band(fig, bid, x0, x1, y, here):
    _keys, band, whole, ring = here
    size, h_chip, line_h, top = 10.5, 16, 21, 36
    items = []
    for glabel, rows in GROUPS[bid]:
        if glabel:
            s = glabel[0] if fig.en else glabel[1]
            items.append(("label", s, text_w(s, 10) + 1))
        for r in rows:
            c = CHIPS[r[0]]
            items.append(("chip", c, chip_w(c.label, size)))
    lines = pack([w for _k, _p, w in items], x0 + 8, x1 - 8, 4.5)
    h = top + line_h * len(lines) + 1
    band_rect(fig, x0, y, x1 - x0, h, here=(bid == band and whole))
    band_header(fig, bid, x0, x1, y, path_blocks(bid), pinned=(bid == band))
    for li, line in enumerate(lines):
        ly = y + top + line_h * li
        for i, x in line:
            kind, p, w = items[i]
            if kind == "label":
                fig.text(x, ly + 11.8, p, 10, italic=True, opacity=0.8)
            else:
                chip(fig, p, x, ly, w, h_chip, size, ring=p.key in ring)
    return h


def stack_band(fig, x0, x1, y, here):
    _keys, band, whole, ring = here
    size, h_chip, line_h, top = 10.5, 16, 21, 38
    ladder_x, label_x = x0 + 14, x0 + 24
    ch_x0 = x0 + 114
    ct_x0, ct_x1 = x1 - 88, x1 - 8
    rows, ry = [], y + top
    for rid, en, ko, rs in STACK:
        cs = [CHIPS[r[0]] for r in rs]
        end = x1 - 8 if rid == "loop" else ct_x0 - 8
        lines = pack([chip_w(c.label, size) for c in cs], ch_x0, end, 4.5)
        rh = line_h * len(lines) + 5
        rows.append(dict(id=rid, name=en if fig.en else ko, cs=cs, lines=lines, y=ry, h=rh))
        ry += rh
    side = []
    for (s_en, s_ko), rs in SIDE:
        cs = [CHIPS[r[0]] for r in rs]
        side.append((s_en if fig.en else s_ko, cs,
                     pack([chip_w(c.label, size) for c in cs], ct_x0 + 6, ct_x1 - 6, 4)))
    layer_top = rows[1]["y"]
    need = sum(16 + line_h * len(lines) for _t, _c, lines in side) + 8
    if need > ry - layer_top:
        rows[-1]["h"] += need - (ry - layer_top)
        ry = layer_top + need
    h = ry - y + 5
    band_rect(fig, x0, y, x1 - x0, h, here=(band == "stack" and whole))
    band_header(fig, "stack", x0, x1, y, path_blocks("stack"), pinned=(band == "stack"))
    # the control and systems column, beside the six layers
    fig.add(f'<rect x="{num(ct_x0)}" y="{num(layer_top + 3)}" width="{num(ct_x1 - ct_x0)}" '
            f'height="{num(ry - layer_top - 5)}" rx="5" fill="currentColor" fill-opacity="0.04" '
            f'stroke="currentColor" stroke-opacity="0.3"/>')
    sy = layer_top + 3
    for title, cs, lines in side:
        fig.fits("side title", title, 10.5, ct_x1 - ct_x0 - 12, bold=True)
        fig.text(ct_x0 + 6, sy + 13, title, 10.5, weight=600)
        sy += 17
        for li, line in enumerate(lines):
            for i, x in line:
                c = cs[i]
                chip(fig, c, x, sy + line_h * li, chip_w(c.label, size), h_chip, size,
                     ring=c.key in ring)
        sy += line_h * len(lines) + 2
    # the layers: separators, names, the ladder of 7 §5, chips
    for k, r in enumerate(rows):
        if k:
            end = x1 - 8 if k == 1 else ct_x0 - 6
            fig.add(f'<line x1="{num(x0 + 8)}" y1="{num(r["y"])}" x2="{num(end)}" y2="{num(r["y"])}" '
                    f'stroke="currentColor" stroke-opacity="0.22"/>')
        mid = r["y"] + r["h"] / 2
        lx = x0 + 8 if r["id"] == "loop" else label_x
        fig.fits("layer name", r["name"], 10.5, ch_x0 - 6 - lx)
        fig.text(lx, mid + 3.8, r["name"], 10.5)
        for li, line in enumerate(r["lines"]):
            for i, x in line:
                c = r["cs"][i]
                cy = r["y"] + 3 + line_h * li + (r["h"] - 5 - line_h * len(r["lines"])) / 2
                chip(fig, c, x, cy, chip_w(c.label, size), h_chip, size, ring=c.key in ring)
        if r["id"] == "loop":
            last = r["lines"][-1][-1]
            nx = last[1] + chip_w(r["cs"][last[0]].label, size) + 8
            note = LOOP_NOTE[0 if fig.en else 1]
            fig.fits("loop note", note, 10, x1 - 8 - nx)
            fig.text(nx, mid + 3.5, note, 10, italic=True, opacity=0.8)
    for lower, upper in zip(rows[:0:-1], rows[-2:0:-1]):
        fig.arrow(ladder_x, lower["y"] + lower["h"] / 2 - 4, ladder_x,
                  upper["y"] + upper["h"] / 2 + 3, width=1.1, opacity=0.7)
    return h


def practice_column(fig, x0, x1, top, bottom, ring):
    l1, l2, note = BANDS["practice"][0 if fig.en else 1]
    band_rect(fig, x0, top, x1 - x0, bottom - top)
    cx = (x0 + x1) / 2
    for i, s in enumerate((l1, l2)):
        fig.fits("column title", s, 10.5, x1 - x0 - 6, bold=True)
        fig.text(cx, top + 15 + 13 * i, s, 10.5, anchor="middle", weight=600)
    blocks = sorted({c.block for c in (CHIPS[r[0]] for r in PRACTICE) if c.on_path})
    for i, b in enumerate(blocks):
        badge(fig, cx + 18.5 * (i - (len(blocks) - 1) / 2), top + 45, b)
    fig.fits("column note", note, 10, x1 - x0 - 6)
    fig.text(cx, bottom - 8, note, 10, anchor="middle", italic=True, opacity=0.8)
    first, last = top + 64, bottom - 36
    step = (last - first) / (len(PRACTICE) - 1)
    for i, r in enumerate(PRACTICE):
        c = CHIPS[r[0]]
        w = chip_w(c.label, 10.5)
        chip(fig, c, cx - w / 2, first + step * i, w, 16, 10.5, ring=c.key in ring)


def flow(fig, x0, x1, y, items, gap=16, line_h=22):
    """Legend items (width, draw(x, y)) laid left to right, wrapping at x1."""
    lines = pack([w for w, _d in items], x0, x1, gap)
    for li, line in enumerate(lines):
        for i, x in line:
            items[i][1](x, y + line_h * li)
    return y + line_h * len(lines)


def legend_text_item(fig, sample_w, sample, s, size=10):
    w = sample_w + 5 + text_w(s, size)

    def draw(x, y):
        sample(x, y)
        fig.text(x + sample_w + 5, y + 11.8, s, size)
    return (w, draw)


def fig_map(lang):
    week_keys, band, whole, ring = here_info()
    en = lang == "en"
    names = {b: BANDS[b][0 if en else 1][0] for b in ("goal", "learning", "stack", "physics",
                                                        "math", "tools")}
    if en:
        aria = ("Physical AI map. Top: the goal, install that panel on the frame, in construction. "
                "Below it learning and adaptation, then the robot stack of perception, scene and "
                "state, grasping, planning, manipulation and contact and force, with control and "
                "systems beside it, then the physics, mathematics and tools floors. Research "
                "practice runs alongside. Every chip is a page; heavy chips are on the "
                f"dissertation path; the {names[band]} is marked you are here.")
    else:
        aria = ("피지컬 AI 지도. 맨 위는 건설의 목표, 저 패널을 프레임에 설치해. 그 아래 학습과 적응, "
                "그 아래 인식, 장면과 상태, 파지, 계획, 조작, 접촉과 힘의 로봇 스택과 곁의 제어와 시스템, "
                "맨 아래 물리, 수학, 도구 바닥. 연구 실무가 나란히 간다. 칩마다 페이지이고, 굵은 칩은 "
                f"학위논문 경로 위에 있으며, {names[band]}에 지금 여기 표시가 있다.")
    fig = Fig(1, lang, aria)
    here = (week_keys, band, whole, ring)
    X0, X1, RX0, RX1 = 10.0, 494.0, 504.0, 554.0
    ext, y = {}, 8.0
    for bid in ("goal", "learning"):
        h = simple_band(fig, bid, X0, X1, y, here)
        ext[bid] = (y, y + h)
        y += h + 18
    h = stack_band(fig, X0, X1, y, here)
    ext["stack"] = (y, y + h)
    y += h + 22
    floors_top = y - 5
    for bid in ("physics", "math", "tools"):
        h = simple_band(fig, bid, X0, X1, y, here)
        ext[bid] = (y, y + h)
        y += h + 6
    floors_bottom = y - 1
    fig.add(f'<rect x="{num(X0 - 5)}" y="{num(floors_top)}" width="{num(X1 - X0 + 10)}" '
            f'height="{num(floors_bottom - floors_top)}" rx="10" fill="none" stroke="currentColor" '
            f'stroke-opacity="0.45" stroke-dasharray="4 3"/>')
    for lower_top, upper_bottom in ((ext["learning"][0], ext["goal"][1]),
                                    (ext["stack"][0], ext["learning"][1]),
                                    (floors_top, ext["stack"][1])):
        for fx in (0.2, 0.5, 0.8):
            x = X0 + (X1 - X0) * fx
            fig.arrow(x, lower_top - 1.5, x, upper_bottom + 2.5)
    practice_column(fig, RX0, RX1, ext["goal"][0], floors_bottom, ring)
    # legend
    items = [
        legend_text_item(fig, chip_w("3.5", 10.5), lambda x, y: sample_chip(fig, x, y, "3.5", False),
                         "a page: click to open, hover for its title" if en
                         else "페이지: 누르면 열리고, 포인터를 올리면 제목"),
        legend_text_item(fig, chip_w("3.5", 10.5), lambda x, y: sample_chip(fig, x, y, "3.5", True),
                         "on the dissertation path of 7 §8" if en else "7 §8의 학위논문 경로 위"),
        legend_text_item(fig, 15, lambda x, y: badge(fig, x + 7.5, y + 8, 2),
                         "its block of the path" if en else "그 경로 블록"),
        legend_text_item(fig, 10, lambda x, y: fig.arrow(x + 5, y + 16, x + 5, y + 1, width=1.3),
                         "stands on what is below it" if en else "아래에 있는 것 위에 선다"),
    ]
    if ring:
        items.append(legend_text_item(
            fig, 22, lambda x, y: fig.add(
                f'<rect x="{num(x)}" y="{num(y)}" width="22" height="16" rx="4.5" fill="none" '
                f'stroke-width="1.3" stroke-dasharray="2.5 1.5" style="stroke:{ACCENT}"/>'),
            "this week's pages" if en else "이번 주의 페이지"))
    wk = (f"you are here: week {YOU_ARE_HERE} of the four-week plan, {WEEKS[YOU_ARE_HERE][0]}"
          if en else f"지금 여기: 4주 계획의 {YOU_ARE_HERE}주차, {WEEKS[YOU_ARE_HERE][1]}")
    items.append((12 + text_w(wk, 10.5, True), lambda x, y: (
        pin(fig, x + 5, y + 14, ""), fig.text(x + 13, y + 12, wk, 10.5, weight=600, accent=True))))
    end = flow(fig, X0, RX1, floors_bottom + 14, items)
    return fig, fig.svg(end + 2)


ROWS2 = (
    ("goal", ("goal:", "construction"), ("목표:", "건설")),
    ("learning", ("learning and", "adaptation"), ("학습과", "적응")),
    ("stack", ("robot stack", "and control"), ("로봇 스택과", "제어")),
    ("practice", ("research", "practice"), ("연구 실무",)),
    ("physics", ("physics", "floor"), ("물리 바닥",)),
    ("math", ("mathematics", "floor"), ("수학 바닥",)),
    ("tools", ("tools", "floor"), ("도구 바닥",)),
)


def fig_task(lang):
    en = lang == "en"
    _keys, band, whole, ring = here_info()
    aria = ("The eight steps of installing a panel on a frame, left to right: resolve the "
            "instruction, identify panel and frame, decompose the job, plan a grasp, move the "
            "component, detect contact, perform the fitting, verify completion. Under each, its "
            "layer and the page chips that power it, down to the physics, mathematics and tools "
            "floors it stands on." if en else
            "패널을 프레임에 설치하는 여덟 단계를 왼쪽에서 오른쪽으로: 지시 해석, 패널과 프레임 식별, "
            "작업 분해, 파지 계획, 부재 이동, 접촉 감지, 끼움 수행, 완료 검증. 단계마다 속한 층과 "
            "그 단계를 움직이는 페이지 칩, 그리고 그 단계가 딛는 물리·수학·도구 바닥까지.")
    fig = Fig(2, lang, aria)
    lx, cx0, cx1 = 5.0, 75.0, 557.0
    n = len(STEPS)
    cw = (cx1 - cx0) / n
    size, h_chip, line_h = 10, 15, 19
    lead = 12.5   # between stacked label lines; Noto Sans KR's line box is tall

    def cx(i):
        return cx0 + cw * (i + 0.5)

    cy = 18.0
    fig.text(lx, cy + 4, "the task" if en else "과제", 10.5, weight=600)
    for i in range(n - 1):
        fig.arrow(cx(i) + 10, cy, cx(i + 1) - 11, cy, width=1.1)
    for i in range(n):
        fig.add(f'<circle cx="{num(cx(i))}" cy="{num(cy)}" r="9" fill="currentColor" '
                f'fill-opacity="0.1" stroke="currentColor" stroke-width="1.2"/>')
        fig.text(cx(i), cy + 3.6, str(i + 1), 10, anchor="middle", weight=600)
    ly = cy + 24
    step_lines = [st[0] if en else st[1] for st in STEPS]
    for i, lines in enumerate(step_lines):
        for j, s in enumerate(lines):
            fig.fits("step", s, 10, cw - 3)
            fig.text(cx(i), ly + lead * j, s, 10, anchor="middle")
    yl = ly + lead * max(len(x) for x in step_lines) + 5
    fig.text(lx, yl, "its layer" if en else "속한 층", 10, italic=True, opacity=0.8)
    layer_lines = [st[2] if en else st[3] for st in STEPS]
    for i, lines in enumerate(layer_lines):
        for j, s in enumerate(lines):
            fig.fits("layer", s, 10, cw - 3)
            fig.text(cx(i), yl + lead * j, s, 10, anchor="middle", italic=True, opacity=0.85)
    gy = yl + lead * (max(len(x) for x in layer_lines) - 1) + 10
    for bid, en_l, ko_l in ROWS2:
        if bid == "physics":
            fig.add(f'<line x1="{num(lx)}" y1="{num(gy + 2)}" x2="{num(cx1)}" y2="{num(gy + 2)}" '
                    f'stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="4 3"/>')
            gy += 7
        cells = []
        for i, st in enumerate(STEPS):
            cs = [CHIPS[k] for k in st[4] if CHIPS[k].band == bid]
            ws = [chip_w(c.label, size, pad=3) for c in cs]
            cells.append((cs, ws, pack(ws, cx(i) - cw / 2 + 2, cx(i) + cw / 2 - 2, 2.5)))
            for w in ws:
                if w > cw - 4:
                    fig.problems.append(f"figure 2 ({lang}): a chip of width {w:.0f} does not fit "
                                        f"a column of {cw - 4:.0f}")
        here_row = bid == band and whole
        labels = list(en_l if en else ko_l)
        nl = max(1, max(len(lines) for _c, _w, lines in cells))
        rh = max(line_h * nl + 6, lead * len(labels) + (19 if here_row else 8))
        if here_row:
            fig.add(f'<rect x="{num(lx - 3)}" y="{num(gy)}" width="{num(cx1 - lx + 3)}" '
                    f'height="{num(rh)}" rx="4" stroke-width="1.6" '
                    f'style="fill:{HIGHLIGHT};stroke:{ACCENT}"/>')
        else:
            fig.add(f'<rect x="{num(lx - 3)}" y="{num(gy)}" width="{num(cx1 - lx + 3)}" '
                    f'height="{num(rh)}" rx="4" fill="currentColor" fill-opacity="0.04"/>')
        block_h = lead * len(labels) + (13 if here_row else 0)
        ty = gy + (rh - block_h) / 2 + 8.5
        for j, s in enumerate(labels):
            fig.fits("row label", s, 10, cx0 - lx - 4, bold=j == 0)
            fig.text(lx, ty + lead * j, s, 10, weight=600 if j == 0 else None)
        if here_row:
            s = "you are here" if en else "지금 여기"
            fig.fits("row pin", s, 10, cx0 - lx - 10, bold=True)
            pin(fig, lx + 3, ty + lead * len(labels) + 3, "")
            fig.text(lx + 9, ty + lead * len(labels) + 2, s, 10, weight=600, accent=True)
        for i, (cs, ws, lines) in enumerate(cells):
            off = (rh - line_h * len(lines)) / 2 + 2
            for li, line in enumerate(lines):
                lw = sum(ws[k] for k, _x in line) + 2.5 * (len(line) - 1)
                x = cx(i) - lw / 2
                for k, _x in line:
                    chip(fig, cs[k], x, gy + off + line_h * li, ws[k], h_chip, size,
                         ring=cs[k].key in ring)
                    x += ws[k] + 2.5
        gy += rh + 3
    for i in range(1, n):
        x = cx0 + cw * i
        fig.add(f'<line x1="{num(x)}" y1="{num(cy + 12)}" x2="{num(x)}" y2="{num(gy - 3)}" '
                f'stroke="currentColor" stroke-opacity="0.22" stroke-dasharray="2 3"/>')
    note = ("read down a column: the pages that power the step, then the floors it stands on"
            if en else "열을 따라 내려가며 읽는다: 단계를 움직이는 페이지, 그리고 그 단계가 딛는 바닥")
    fig.fits("note", note, 10, cx1 - lx)
    fig.text(lx, gy + 11, note, 10, italic=True, opacity=0.8)
    return fig, fig.svg(gy + 18)


def fig_route(lang):
    en = lang == "en"
    week = YOU_ARE_HERE
    path = [b for b in BLOCKS if b[0] <= 7]
    total = sum(count(b[3]) for b in path)
    aria = (f"The dissertation path of 7 section 8 as a timeline: seven blocks, about "
            f"{TOTALS['working']} sessions at Working and {TOTALS['literacy']} at Literacy, "
            f"block 8 alongside, each bar tagged with the week of the four-week plan that "
            f"prepares it, and a marker at week {week}." if en else
            f"7 §8의 학위논문 경로를 시간 순서로: 일곱 블록, Working 약 {TOTALS['working']}회와 "
            f"Literacy {TOTALS['literacy']}회, 곁에서 나란히 가는 8 블록, 막대마다 그것을 준비하는 "
            f"4주 계획의 주차, 그리고 {week}주차의 지금 여기 표시.")
    fig = Fig(3, lang, aria)
    lx, nx, cx0, cx1 = 8.0, 32.0, 252.0, 548.0
    sc = (cx1 - cx0) / total

    def X(s):
        return cx0 + s * sc

    def tag(w):
        return f"week {w}" if en else f"{w}주차"

    fig.text(lx, 15, "the path of 7 §8, block by block" if en else "7 §8의 경로, 블록별로",
             10.5, weight=600)
    y0, rh = 26.0, 34.0
    start, here_at = 0, None
    for r, (n, e, k, w_cell, l_cell, segs) in enumerate(BLOCKS):
        yc = y0 + rh * r + rh / 2
        badge(fig, lx + 8, yc - 3, n, dashed=n > 7)
        name = e if en else k
        fig.fits("block name", name, 10.5, cx0 - 8 - nx)
        fig.text(nx, yc - 0.5, name, 10.5)
        wd = w_cell.replace("about ", "≈ " if en else "약 ")
        fig.text(nx, yc + 11.5, f"W {wd} · L {l_cell}", 10, opacity=0.8)
        by, bh = yc - 10, 11
        if n > 7:
            fig.add(f'<rect x="{num(X(0))}" y="{num(by)}" width="{num(X(total) - X(0))}" '
                    f'height="{bh}" rx="2" fill="currentColor" fill-opacity="0.05" '
                    f'stroke="currentColor" stroke-opacity="0.8" stroke-dasharray="4 3"/>')
            s = "alongside the whole path" if en else "경로 전체와 나란히"
            fig.fits("block 8 note", s, 10, X(total) - X(0) - 8)
            fig.text((X(0) + X(total)) / 2, by + 9, s, 10, anchor="middle", italic=True)
            continue
        wn, ln = count(w_cell), count(l_cell)
        s0 = start
        for ss, wk in segs:
            xa, xb = X(s0), X(s0 + ss)
            if wk == week:
                fig.add(f'<rect x="{num(xa)}" y="{num(by)}" width="{num(xb - xa)}" height="{bh}" '
                        f'style="fill:{HIGHLIGHT}"/>')
                if here_at is None:
                    here_at = (xa, by)
            else:
                op = "0.16" if wk is not None else "0.05"
                fig.add(f'<rect x="{num(xa)}" y="{num(by)}" width="{num(xb - xa)}" height="{bh}" '
                        f'fill="currentColor" fill-opacity="{op}"/>')
            s0 += ss
        fig.add(f'<rect x="{num(X(start))}" y="{num(by)}" width="{num(X(start + wn) - X(start))}" '
                f'height="{bh}" fill="none" stroke="currentColor" stroke-width="1.1"/>')
        s0 = start
        for ss, wk in segs:
            xa, xb = X(s0), X(s0 + ss)
            if wk == week:
                fig.add(f'<rect x="{num(xa)}" y="{num(by)}" width="{num(xb - xa)}" height="{bh}" '
                        f'fill="none" stroke-width="2" style="stroke:{ACCENT}"/>')
            s0 += ss
            if s0 < start + wn:
                fig.add(f'<line x1="{num(xb)}" y1="{num(by)}" x2="{num(xb)}" y2="{num(by + bh)}" '
                        f'stroke="currentColor" stroke-width="0.9"/>')
        fig.add(f'<rect x="{num(X(start))}" y="{num(by + bh + 2)}" width="{num(ln * sc)}" '
                f'height="3.5" fill="currentColor" fill-opacity="0.75"/>')
        # week tags: inside each piece if every piece has room, else one tag beside the bar
        weeks = [wk for _s, wk in segs if wk is not None]
        pieces, s0, inside = [], start, True
        for ss, wk in segs:
            if wk is not None:
                pieces.append((X(s0), X(s0 + ss), wk))
                inside &= X(s0 + ss) - X(s0) >= text_w(tag(wk), 10) + 8
            s0 += ss
        if pieces and inside:
            for xa, xb, wk in pieces:
                fig.text((xa + xb) / 2, by + 8.8, tag(wk), 10, anchor="middle",
                         weight=600 if wk == week else None, accent=wk == week)
        elif weeks:
            uniq = sorted(set(weeks), key=weeks.index)
            s = (tag(uniq[0]) if len(uniq) == 1 else
                 ("weeks " + " and ".join(map(str, uniq)) if en else
                  "·".join(map(str, uniq)) + "주차"))
            tw = text_w(s, 10, week in uniq)
            if X(start) - 6 - tw >= cx0:
                tx, anchor = X(start) - 6, "end"
            elif X(start + wn) + 6 + tw <= cx1:
                tx, anchor = X(start + wn) + 6, None
            else:
                fig.problems.append(f"figure 3 ({lang}): no room for the tag {s!r} of block {n}")
                tx, anchor = X(start + wn) + 6, None
            fig.text(tx, by + 8.8, s, 10, anchor=anchor, weight=600 if week in uniq else None,
                     accent=week in uniq)
        start += wn
    ya = y0 + rh * len(BLOCKS) + 4
    fig.add(f'<line x1="{num(cx0)}" y1="{num(ya)}" x2="{num(cx1)}" y2="{num(ya)}" '
            f'stroke="currentColor" stroke-opacity="0.7"/>')
    ticks = [t for t in range(0, total, 50) if total - t >= 15] + [total]
    for t in ticks:
        fig.add(f'<line x1="{num(X(t))}" y1="{num(ya)}" x2="{num(X(t))}" y2="{num(ya + 4)}" '
                f'stroke="currentColor" stroke-opacity="0.7"/>')
        fig.text(X(t), ya + 14, str(t), 10, anchor="middle", opacity=0.85)
    axis = "sessions at Working" if en else "Working 회차"
    fig.fits("axis", axis, 10, cx0 - 8 - nx)
    fig.text(cx0 - 8, ya + 4, axis, 10, anchor="end", italic=True, opacity=0.8)
    t = TOTALS
    lines = (
        (f"blocks 1–7: about {t['working']} sessions at Working (≈ {t['weeks_working']} weeks "
         f"at two a week) and {t['literacy']} at Literacy (≈ {t['weeks_literacy']} weeks)") if en else
        (f"1–7 블록: Working 약 {t['working']}회(주 2회로 약 {t['weeks_working']}주), Literacy "
         f"{t['literacy']}회(약 {t['weeks_literacy']}주)"),
        (f"block 8 adds {t['alongside']} alongside: about {t['all']} sessions in all" if en
         else f"8 블록이 곁에서 {t['alongside']}회를 더해 모두 약 {t['all']}회"),
        ("thick bar: every row of a block (Working) · thin bar: its bold rows (Literacy)" if en
         else "굵은 막대: 블록의 모든 행(Working) · 가는 막대: 굵은 행(Literacy)"),
        ("week n: the week of the four-week plan that improves those pages ahead of your study"
         if en else "n주차: 공부 바로 앞에서 그 페이지들을 다듬는 4주 계획의 주"),
    )
    y = ya + 32
    for j, s in enumerate(lines):
        fig.fits("route note", s, 10, 552 - lx)
        fig.text(lx, y + 13 * j, s, 10, weight=600 if j < 2 else None,
                 italic=j > 1, opacity=None if j < 2 else 0.8)
    if here_at:
        px, py = here_at[0] + 5, here_at[1] - 1.5
        label = here_label(fig)
        if px + 8 + text_w(label, 11, True) > cx1:
            fig.problems.append(f"figure 3 ({lang}): no room for the pin's label at x={px:.0f}")
        pin(fig, px, py, label, lift=5)
    return fig, fig.svg(y + 13 * (len(lines) - 1) + 8)


# =============================================================================
# Writing the page
# =============================================================================

def splice(text, figures):
    for (n, lang), svg in figures.items():
        begin, end = f"<!-- MAP:fig{n}:{lang}:BEGIN -->", f"<!-- MAP:fig{n}:{lang}:END -->"
        i, j = text.find(begin), text.find(end)
        if i < 0 or j < i:
            sys.exit(f"{os.path.relpath(PAGE, ROOT)}: marker {begin} ... {end} not found")
        text = text[:i + len(begin)] + "\n" + svg + "\n" + text[j:]
    return text


def main():
    problems = validate()
    if problems:
        print(f"The table disagrees with the wiki ({len(problems)}):")
        for p in problems:
            print(" -", p)
        sys.exit(2)
    figures, layout = {}, []
    for lang in ("en", "ko"):
        for n, build in ((1, fig_map), (2, fig_task), (3, fig_route)):
            fig, svg = build(lang)
            layout += fig.problems
            figures[(n, lang)] = svg
    if layout:
        print(f"A label would overflow its box ({len(layout)}):")
        for p in layout:
            print(" -", p)
        sys.exit(3)
    for rel in uncovered():
        print(f"note: {rel} has no chip on the map - add it to the table")
    old = open(PAGE, encoding="utf-8").read()
    new = splice(old, figures)
    on_path = sum(c.on_path for c in CHIPS.values())
    summary = (f"{len(CHIPS)} chips ({on_path} on the path) in 7 bands, {len(STEPS)} steps, "
               f"{len(BLOCKS)} blocks; you are here: week {YOU_ARE_HERE}")
    if "--check" in sys.argv:
        if new != old:
            print("physical-ai-map.md is stale: run python3 scripts/build_physical_ai_map.py")
            sys.exit(1)
        print(f"physical-ai-map.md up to date ({summary})")
        return
    if new != old:
        with open(PAGE, "w", encoding="utf-8") as fh:
            fh.write(new)
        print(f"wrote {os.path.relpath(PAGE, ROOT)} ({summary})")
    else:
        print(f"physical-ai-map.md already up to date ({summary})")


if __name__ == "__main__":
    main()
