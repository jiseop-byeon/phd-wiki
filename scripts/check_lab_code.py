#!/usr/bin/env python3
"""Run every runnable ```python block in the wiki and report the ones that fail.

A page is treated like a notebook: its blocks run in order, in one namespace, in a
fresh subprocess, so a later block may use a function an earlier block defined.
Each block's failure is reported with the page and line where the block starts.

Skipped on purpose:
  - `?`-blank templates (the Do item of a Tier A problem set). Python has no `?`
    operator, so a `?` left after strings and comments are stripped marks a blank.
  - ROS 2 code: blocks importing rclpy, launch, message packages and the like.
    They need a ROS installation and are checked by hand on the ROS 2 pages.
  - A block whose first line is `# not-run: <reason>` (an intentional error, a
    fragment that only makes sense inside a larger program).

Usage: python3 scripts/check_lab_code.py [-v] [--timeout SECONDS] [paths...]
Exit status is 1 if any block fails, 0 otherwise. CI runs it after the content gate.
"""
import argparse
import glob
import io
import json
import os
import re
import subprocess
import sys
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

FENCE = re.compile(r"^((?:> ?)*)```python[^\n]*\n(.*?)^\1```", re.M | re.S)
# Modules that need ROS 2 or a package built in a ROS workspace.
ROS_MODULES = {
    "rclpy", "launch", "launch_ros", "launch_testing", "ament_index_python",
    "std_msgs", "geometry_msgs", "sensor_msgs", "nav_msgs", "shape_msgs",
    "moveit", "moveit_msgs", "tf2_ros", "tf2_geometry_msgs", "turtlesim",
    "example_interfaces", "rcl_interfaces", "nav2_simple_commander",
    "builtin_interfaces", "action_msgs", "visualization_msgs", "trajectory_msgs",
    "control_msgs", "diagnostic_msgs", "rosbag2_py", "ros2cli",
}
# Packages the wiki's own ROS pages ask the reader to create.
ROS_LOCAL = re.compile(r"_interfaces$|^my_pkg$|^cart_")
IMPORT = re.compile(r"^\s*(?:from\s+([\w.]+)\s+import|import\s+([\w., ]+))", re.M)
NOT_RUN = re.compile(r"^\s*#\s*not-run\b")
# ROS fragments often omit their imports (a launch-file excerpt, a node's method).
ROS_NAMES = re.compile(r"\b(LaunchDescription|IncludeLaunchDescription|DeclareLaunchArgument|"
                       r"LaunchConfiguration|PythonLaunchDescriptionSource|get_package_share_directory|"
                       r"create_publisher|create_subscription|create_service|create_client|"
                       r"declare_parameter|get_logger|ament_python|rclpy)\b"
                       r"|\bNode\(\s*(package|executable|name)\s*=|\(Node\):")
# On a ROS 2 page, a one-line excerpt of a node or a setup.py is still ROS code.
ROS_PAGE_NAMES = re.compile(r"\bself\.|\bNode\(|\bsetup\(|\bpackage_name\b|\bDuration\(|\bTime\(")


def has_blank(code):
    """True if a `?` survives outside strings and comments (a template blank)."""
    try:
        toks = tokenize.generate_tokens(io.StringIO(code).readline)
        return any(t.string == "?" and t.type in (tokenize.OP, tokenize.ERRORTOKEN) for t in toks)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return "?" in re.sub(r"#.*|'[^'\n]*'|\"[^\"\n]*\"", "", code)


def modules(code):
    out = set()
    for m in IMPORT.finditer(code):
        names = m.group(1) or m.group(2)
        for n in names.split(","):
            n = n.strip().split(" ")[0]
            if n:
                out.add(n.split(".")[0])
    return out


def blocks(path):
    """Yield (line, code, skip_reason) for each ```python block on the page."""
    text = open(path, encoding="utf-8").read()
    for m in FENCE.finditer(text):
        prefix = m.group(1)
        line = text.count("\n", 0, m.start()) + 1
        body = m.group(2)
        if prefix:
            body = "\n".join(l[len(prefix):] if l.startswith(prefix) else l.lstrip("> ")
                             for l in body.split("\n"))
        first = body.lstrip("\n").split("\n", 1)[0]
        mods = modules(body)
        if NOT_RUN.match(first):
            yield line, body, "marked not-run"
        elif (mods & ROS_MODULES or any(ROS_LOCAL.search(x) for x in mods)
              or ROS_NAMES.search(body)
              or ("/ros2/" in path and ROS_PAGE_NAMES.search(body))):
            yield line, body, "ROS 2 code"
        elif has_blank(body):
            yield line, body, "template with ? blanks"
        else:
            yield line, body, None


RUNNER = r"""
import json, sys, traceback, io, contextlib, os
os.environ.setdefault("MPLBACKEND", "Agg")
blocks = json.load(sys.stdin)
ns = {"__name__": "__main__"}
results = []
for line, code in blocks:
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            exec(compile(code, f"<block@{line}>", "exec"), ns)
        results.append([line, None, buf.getvalue()[-2000:]])
    except SystemExit:
        results.append([line, None, buf.getvalue()[-2000:]])
    except BaseException:
        results.append([line, traceback.format_exc(limit=3)[-1500:], buf.getvalue()[-500:]])
print("@@RESULTS@@" + json.dumps(results))
"""


def run_page(path, runnable, timeout):
    """Run a page's runnable blocks in order in one subprocess; return per-block results."""
    try:
        proc = subprocess.run([sys.executable, "-c", RUNNER], input=json.dumps(runnable),
                              capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return [[runnable[0][0], f"page timed out after {timeout}s", ""]]
    marker = proc.stdout.rfind("@@RESULTS@@")
    if marker < 0:
        return [[runnable[0][0], "runner crashed:\n" + proc.stderr[-1500:], ""]]
    return json.loads(proc.stdout[marker + len("@@RESULTS@@"):])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("-v", "--verbose", action="store_true")
    ap.add_argument("--timeout", type=int, default=120)
    args = ap.parse_args()
    paths = args.paths or sorted(glob.glob("content/**/*.md", recursive=True))
    paths = [p for p in paths if "/templates/" not in p]
    counts = {"ran": 0, "failed": 0}
    skipped = {}
    failures = []
    for path in paths:
        runnable = []
        for line, code, why in blocks(path):
            if why:
                skipped[why] = skipped.get(why, 0) + 1
                if args.verbose:
                    print(f"  skip {path}:{line} ({why})")
            else:
                runnable.append([line, code])
        if not runnable:
            continue
        for line, err, out in run_page(path, runnable, args.timeout):
            counts["ran"] += 1
            if err:
                counts["failed"] += 1
                failures.append((path, line, err))
            elif args.verbose:
                print(f"  ok   {path}:{line}")
    for path, line, err in failures:
        print(f"FAIL {path}:{line}\n    " + err.strip().replace("\n", "\n    "))
    skip_txt = ", ".join(f"{n} {why}" for why, n in sorted(skipped.items()))
    print(f"\n{counts['ran']} block(s) run, {counts['failed']} failed; skipped: {skip_txt or 'none'}.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
