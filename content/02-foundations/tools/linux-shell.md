---
title: "12.1 Linux and the Shell"
tags: [foundations, tools, linux]
study-depth: Working
wiki-support: Working
depth-goal: "On P6's robot computer, name a file by an absolute or relative path and predict what the shell will pass to a program; read a process's exit status as the signal that ended it; set and read a permission in octal and say which of the three classes applies; say which processes an environment variable reaches and why a new terminal needs source; write a script with set -euo pipefail that fails for the right reason; copy a day's bags with rsync and keep a run alive in tmux; give a USB device a stable name and start a stack at boot with systemd; and price one day of logging — its bytes, its disk, its copy — and a clock offset against a latency budget."
mastery-when: "Raise when the thesis runs its own fleet of robot computers, a real-time kernel, containers on the robot, or a site network that you administer."
---

> [!note] Prerequisites · 선수 지식
> [[02-foundations/lab-plants|0.6 Lab Plants]] (**P6**: the 200 Hz controller, the 50 Hz vision node and the 70 ms budget) and [[02-foundations/probability|3. Probability §2]] (the Poisson count and the exponential waiting time, used in §8 and the Worked case). Nothing else: no programming beyond typing a command. The ROS 2 pages this page points to come later in study order; each is linked where it is used and never assumed.
> [[02-foundations/lab-plants|0.6 Lab Plants]](**P6**: 200 Hz 제어기, 50 Hz 비전 노드, 70 ms 예산)와 [[02-foundations/probability|3. Probability §2]](포아송 횟수와 지수 대기 시간. §8과 계산 절에서 쓴다). 그 밖에는 없다. 명령을 입력할 줄 알면 되고 프로그래밍은 가정하지 않는다. 이 페이지가 가리키는 ROS 2 페이지들은 학습 순서상 뒤에 오므로, 쓰이는 자리에서 링크할 뿐 안다고 가정하지 않는다.

## English

*Stands on [[02-foundations/lab-plants|0.6 Lab Plants]], whose **P6** is a cart with a 200 Hz controller, a 50 Hz vision node and a 70 ms budget from camera to force. This page is about the computer that runs it — an Ubuntu machine on the cart, reached from a workstation over Ethernet — and about the shell you type into to start, watch, fix and copy from it. The ROS 2 track, [[04-robotics/ros2/index|25. ROS 2]], assumes all of this and teaches none of it.*

> [!note] Why this matters · 왜 배우는가
> This page is the floor beneath the whole physical-AI stack of [[07-research-program/index|research program §5]]: every layer from perception to task completion runs as a process on a Linux robot computer, and in that section's worked instance, "Install that panel on the frame", it is what keeps the controller that moves the component and detects contact running, stoppable and recorded (its place is marked on the [[physical-ai-map|Physical AI Map]]). Without it a trial day is lost in ways no log explains — a recording hung up with a dropped ssh session, a controller that opened the IMU instead of the encoder after a reboot, a nightly check that reported "0 errors" because it read nothing — and the demonstrations a policy like [[05-construction-robotics/imitating-contact|10. Imitating Contact]]'s learns from are exactly such recordings. The ROS 2 build track leans on this page from [[04-robotics/ros2/what-ros2-is|25.1 §7]] to [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]; the page sits outside the seven blocks of the dissertation path ([[07-research-program/index|research program §8]]), so take it when the first need arrives — before you first log in to a robot computer, and at the latest when the build track starts for the rig, ahead of block 7. After it you can run, watch, stop and copy a day of robot recording without losing it, and price that day in bytes, hours and clock offset.

> [!note] First pass · 처음이라면
> Two sessions of about 75 minutes each. **Session 1:** the Running object and the picture, then §1–§3 — how files are named, what the shell does to a line before anything runs, and how a program starts, stops and reports how it ended. End with Self-check 2 and 3. **Session 2:** §4–§6 — permissions, the environment, pipes and scripts — then Worked case steps 1–5 with a calculator. End with Self-check 4, 5 and 6. After that: §8 (and step 6 of the Worked case) before you next work on the robot over ssh, §7 and §9–§11 on the day you set up the robot computer itself, and the problem set last, because its Interpret item uses every section.

### Running object · 이 페이지의 대상

**P6** from [[02-foundations/lab-plants|0.6 Lab Plants]], seen from its computer. The controller samples the encoder and commands the motor at 200 Hz and publishes `/cmd`; the vision node publishes a goal on `/goal` at 50 Hz from a camera running at the same rate; a recorder writes both topics and the compressed camera stream to a bag, the directory of recorded messages that [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]] defines. All three run on one Ubuntu 24.04 computer on the cart, called `p6-cart` here, which you reach from a workstation over a direct Ethernet cable. The catalog fixes the two rates and the budget; everything else in the table is this page's own, frozen here as course numbers chosen for clean arithmetic — not measurements of any machine and not product specifications.

| Symbol | Value | What it is here |
|---|---:|---|
| $f_c$, $f_v$ | 200 Hz, 50 Hz | controller and vision rates (catalog) |
| $s$ | 64 bytes | payload of one `/cmd` or `/goal` message, the illustrative size [[04-robotics/ros2/debugging-data-reproducibility\|25.10]] also uses |
| $s_{\text{img}}$ | 40,000 bytes | one compressed camera frame, recorded at $f_v$ |
| $F$ | 120 GB $=120\times10^9$ bytes | free space for bags on the cart's disk at 08:00 |
| $R$ | 1 Gbit/s | the Ethernet link between cart and workstation, nominal |
| $\eta$ | 0.8 | the fraction of $R$ a bulk copy achieves, so a copy runs at $\eta R/8=100$ MB/s |
| $T$ | 8 h | one shift, 08:00 to 16:00 |
| $\lambda$ | 0.1 per hour | how often the workstation's ssh session to the cart drops — a laptop lid, a cable, a timeout |
| addresses | `192.168.10.1`, `192.168.10.2` | workstation and cart on the direct link |
| account, device | user `robot`; encoder board at `/dev/ttyACM0` | the account the stack runs as, and the USB serial device the controller reads |

Every command on this page was run on a macOS 26.6 laptop (arm64) under bash 3.2 unless its block says otherwise, and every output shown is what that run printed, trimmed where marked. The cart runs Ubuntu 24.04 with bash 5.2.21 and the GNU tools; where the two differ, the page says which system printed an output, and a Linux-only command is marked *from the manual, not run here* — checked against the documentation in Sources, not executed.

*Scope: this page teaches the Linux a researcher uses every day on any machine — files and paths, what the shell does to a line, processes and signals, permissions, the environment, pipes and scripts, installing software, remote work, devices and services, and the clock and the network as a shell user meets them — each applied to P6's computer. It does not teach ROS 2 itself: sourcing a workspace is [[04-robotics/ros2/what-ros2-is|25.1 §7]] and [[04-robotics/ros2/workspaces-packages-launch|25.4 §6]], recording a bag [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]. Python environments, Git, file formats and networking are this track's other pages ([[02-foundations/tools/python-research-code|12.3]], [[02-foundations/tools/git-research-code|12.2]], [[02-foundations/tools/config-data-formats|12.4]], [[02-foundations/tools/computer-networks|12.5]]); §12 lists the rest and where it lives.*

### The picture · 그림으로 먼저 보기

<svg viewBox="0 0 560 560" style="max-width:100%;height:auto" role="img" aria-label="Three panels. A: a workstation at 192.168.10.1 reaches the robot computer p6-cart at 192.168.10.2 over 1 Gbit/s Ethernet that copies about 100 MB/s; on the cart, systemd starts the controller at 200 Hz, the vision node at 50 Hz and the recorder at 7.26 GB/h; the controller reads the encoder through /dev/p6-encoder, a stable name for ttyACM0, whose mode crw-rw---- root dialout is 660; the recorder writes to 120 GB of free disk. B: one day of recording to scale, a straight line from 08:00 rising 7.26 GB per hour, 58.1 GB at the end of the shift at 16:00, the disk full at 00:32. C: grep on a missing log exits 2, wc exits 0, the pipeline reports 0 unless pipefail is set, then 2.">
  <defs><marker id="lsh-arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" font-weight="600" fill="currentColor">A · P6's robot computer and its link</text>
  <rect x="12" y="52" width="120" height="84" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="20" y="68" font-size="11" font-weight="600" fill="currentColor">workstation</text>
  <text x="20" y="84" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">192.168.10.1</text>
  <text x="20" y="100" font-size="11" fill="currentColor">ssh p6, then tmux</text>
  <text x="20" y="116" font-size="11" fill="currentColor">rsync pulls bags</text>
  <line x1="132" y1="94" x2="196" y2="94" stroke="currentColor" stroke-width="2"/>
  <text x="164" y="86" font-size="10" text-anchor="middle" fill="currentColor">Ethernet</text>
  <text x="164" y="108" font-size="10" text-anchor="middle" fill="currentColor">1 Gbit/s</text>
  <text x="164" y="120" font-size="10" text-anchor="middle" fill="currentColor">≈100 MB/s</text>
  <rect x="196" y="28" width="352" height="176" rx="4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="204" y="44" font-size="11" font-weight="600" fill="currentColor">p6-cart · Ubuntu 24.04 · <tspan font-family="ui-monospace,monospace" font-weight="400">192.168.10.2</tspan></text>
  <rect x="292" y="52" width="160" height="20" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.85"/>
  <text x="372" y="66" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">p6-stack.service</text>
  <text x="286" y="66" font-size="10" text-anchor="end" fill="currentColor" fill-opacity="0.8">systemd</text>
  <line x1="372" y1="72" x2="262" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arr)"/>
  <line x1="372" y1="72" x2="372" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arr)"/>
  <line x1="372" y1="72" x2="482" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arr)"/>
  <rect x="208" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="260" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">controller</text>
  <text x="260" y="118" font-size="10" text-anchor="middle" fill="currentColor">200 Hz → /cmd</text>
  <rect x="320" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="372" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">vision</text>
  <text x="372" y="118" font-size="10" text-anchor="middle" fill="currentColor">50 Hz → /goal</text>
  <rect x="432" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="484" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">recorder</text>
  <text x="484" y="118" font-size="10" text-anchor="middle" fill="currentColor">7.26 GB/h</text>
  <line x1="260" y1="124" x2="260" y2="144" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arr)"/>
  <line x1="484" y1="124" x2="484" y2="144" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arr)"/>
  <rect x="208" y="146" width="216" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.85"/>
  <text x="214" y="160" font-size="10" font-family="ui-monospace,monospace" fill="currentColor">/dev/p6-encoder → ttyACM0</text>
  <text x="214" y="174" font-size="10" font-family="ui-monospace,monospace" fill="currentColor">crw-rw---- root dialout</text>
  <text x="214" y="188" font-size="10" fill="currentColor">mode 660: robot must be in dialout</text>
  <rect x="432" y="146" width="104" height="50" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="484" y="162" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">SSD</text>
  <text x="484" y="176" font-size="10" text-anchor="middle" fill="currentColor">120 GB free</text>
  <text x="484" y="189" font-size="10" text-anchor="middle" fill="currentColor">at 08:00</text>
  <line x1="8" y1="214" x2="552" y2="214" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="12" y="234" font-size="12" font-weight="600" fill="currentColor">B · one day of recording, to scale</text>
  <line x1="60" y1="392" x2="540" y2="392" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="60" y1="392" x2="60" y2="262" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="60" y1="272" x2="540" y2="272" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3" stroke-dasharray="3 3"/>
  <line x1="60" y1="332" x2="540" y2="332" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.15"/>
  <text x="54" y="396" font-size="10" text-anchor="end" fill="currentColor">0</text>
  <text x="54" y="336" font-size="10" text-anchor="end" fill="currentColor">60</text>
  <text x="54" y="276" font-size="10" text-anchor="end" fill="currentColor">120</text>
  <text x="54" y="256" font-size="10" text-anchor="end" fill="currentColor">GB used</text>
  <g font-size="10" text-anchor="middle" fill="currentColor"><text x="60" y="406">08:00</text><text x="140" y="406">12:00</text><text x="220" y="406">16:00</text><text x="300" y="406">20:00</text><text x="380" y="406">00:00</text><text x="460" y="406">04:00</text><text x="540" y="406">08:00</text></g>
  <text x="300" y="420" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">time of day; the recorder starts at 08:00 and nobody stops it</text>
  <line x1="60" y1="392" x2="390.69" y2="272" stroke="currentColor" stroke-width="2.2"/>
  <line x1="390.69" y1="272" x2="540" y2="272" stroke="currentColor" stroke-width="1.6" stroke-dasharray="6 4"/>
  <line x1="220" y1="392" x2="220" y2="333.94" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <circle cx="220" cy="333.94" r="3.6" fill="currentColor"/>
  <circle cx="390.69" cy="272" r="3.6" fill="currentColor"/>
  <text x="70" y="298" font-size="11" font-weight="600" fill="currentColor">7.26 GB/h</text>
  <text x="70" y="312" font-size="10" fill="currentColor">camera 99.2%, /cmd and /goal 0.8%</text>
  <text x="228" y="350" font-size="10" font-weight="600" fill="currentColor">16:00 · 58.1 GB · shift ends</text>
  <text x="228" y="363" font-size="10" fill="currentColor">copy to the workstation: 9 min 41 s</text>
  <text x="398" y="290" font-size="10" font-weight="600" fill="currentColor">00:32 · 120 GB · disk full</text>
  <text x="398" y="303" font-size="10" fill="currentColor">16 h 32 min after the start</text>
  <line x1="8" y1="432" x2="552" y2="432" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="12" y="452" font-size="12" font-weight="600" fill="currentColor">C · the nightly check when the log is missing</text>
  <rect x="12" y="462" width="236" height="40" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="20" y="478" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">grep ERROR p6_day2.log</text>
  <text x="20" y="494" font-size="10" fill="currentColor">status 2: no such file</text>
  <text x="258" y="488" font-size="12" font-weight="600" font-family="ui-monospace,monospace" fill="currentColor">|</text>
  <rect x="272" y="462" width="128" height="40" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="280" y="478" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">wc -l</text>
  <text x="280" y="494" font-size="10" fill="currentColor">prints 0, status 0</text>
  <text x="12" y="524" font-size="11" fill="currentColor">default: the pipeline's status is the last command's, <tspan font-weight="600">0</tspan>, and the report says "0 errors"</text>
  <text x="12" y="542" font-size="11" fill="currentColor">with set -o pipefail: the status is <tspan font-weight="600">2</tspan>, and set -e stops the script</text>
</svg>

P6's computer as this page sees it: a workstation reaches `p6-cart` over a 1 Gbit/s link that copies about 100 MB/s, systemd starts the three programs at boot, and the controller reads its encoder through `/dev/p6-encoder`, a stable name for `ttyACM0`, whose mode `crw-rw----` (660, group `dialout`) is why the user `robot` must be in that group. Panel B draws the recorder's 7.26 GB/h to scale: the shift ends at 16:00 with 58.1 GB, a 9 min 41 s copy, and a recorder nobody stopped fills the 120 GB at 00:32. Panel C is a nightly check reading a log that does not exist: `grep` fails with status 2, yet the pipeline reports 0 unless `pipefail` is set.

### 1. Files, paths and the filesystem tree

*In one sentence:* everything on the machine hangs from one tree rooted at `/`, a path names a place in it from the root or from the working directory of whoever reads it, and `df` and `du` say how full it is.

The first puzzles on a new machine are usually a file that one program finds and another does not, and a disk that fills up overnight; both are questions about the filesystem. A **shell** is the program that reads the line you type, rewrites it by rules of its own (§2) and starts the programs it names; the window around it is only a terminal. The scripts on this page begin with `#!/bin/bash`, so bash runs them on the cart whatever shell you happen to type into. Everything a Linux machine keeps — programs, configuration, data and even its devices — hangs from one tree of directories whose root is `/`. The places that matter on `p6-cart`, with what the manual page hier(7) says each is for:

| Directory | What it holds, and what lives there on `p6-cart` |
|---|---|
| `/home/robot` | the home directory of the account `robot`: the workspace, the bags, `~/.ssh`, `~/.bashrc` |
| `/etc` | configuration local to this machine: udev rules (§9), systemd units (§10), the network (§11) |
| `/opt/ros/jazzy` | add-on packages: ROS 2, put there by apt (§7) |
| `/usr/bin` | the primary directory of programs: `bash`, `grep`, `rsync`, `ssh` |
| `/dev` | device files that refer to hardware: `/dev/ttyACM0` (§9) |
| `/var/log`, `/tmp` | log files; temporary files that may be deleted without notice, for instance at boot |

Every process carries a **working directory** — the directory it is "in"; `pwd` prints the shell's, `cd` changes it — and a new process starts in its parent's. Paths are read against it, which is where most "it works when I run it" puzzles begin.

A **path** names a file by the route to it through that tree: its components are the names between the `/` characters, each looked up inside the directory reached so far, and every directory passed on the way must grant search permission (§4). A path that begins with `/` is **absolute** and the lookup starts at the root; any other path is **relative** and starts at the working directory of the process that uses it. So an absolute path names the same file for every process, and a relative path names a different file for each working directory it is read from. `.` and `..` are the directory reached so far and its parent (`/..` is `/`), while `~` is not part of the rule at all: the shell replaces it with the home directory before any program sees the path (§2). The recorder that writes to `bags/day1`, started by `robot` in `/home/robot`, writes to `/home/robot/bags/day1` — about 3.6 GB per half-hour file on P6 (Worked case).

The trap is a program started from somewhere else. A systemd service starts in `/` unless told otherwise (§10), so a relative path that worked in your terminal breaks at boot; anything a machine starts for you — a script, a launch file, a service — should name its files by absolute path or set its working directory explicitly. §6's log check, saved as `path_demo.sh` and run with bash on the laptop, first from the log's directory and then from `/` (`$OLDPWD` is the directory `cd` just left):

```bash
#!/bin/bash
./p6_check_log.sh p6_day1.log
cd / && "$OLDPWD"/p6_check_log.sh p6_day1.log
echo "status $?"
```

```text
p6_day1.log: 3 errors, 56 warnings
grep: p6_day1.log: No such file or directory
status 1
```

**How full is the disk.** Two commands answer it, and they measure different things. `df -h` reports each *filesystem* — its size, what is used, what is free — while `du -sh DIR` adds up what one *directory tree* occupies. With `-h` both count in powers of 1024 — their "G" is $2^{30}$ bytes, not $10^9$ — so the 120 GB of free space frozen above, $120\times10^9$ bytes, appears in `df -h` as about 111.8G. When a size on the robot and a size in a paper disagree by 7%, this is usually the reason: $10^9/2^{30}=0.931$.

> [!note]- Deeper · 더 깊이
> GNU `df -H` and `du --si` count in powers of 1000 instead. `du` also counts the disk blocks a file occupies rather than its exact length, and `-h` rounds up. A mock bag directory of three 1,000,000-byte split files and a 42-byte `metadata.yaml` (the one §8 copies) holds 3,000,042 bytes, 2.86 of the 1,048,576-byte units `du -h` calls "M", and on the laptop it prints as 2.9M:
>
> ```bash
> du -sh bags/day1
> ```
>
> ```text
> 2.9M	bags/day1
> ```

**Where the documentation is.** Every command and file format on this page has a manual page, `man NAME`. The number in `chmod(1)` or `systemd.service(5)` is the section: 1 for user commands, 5 for file formats and configuration files, 7 for overviews such as hier(7), 8 for system-management commands. `man 5 systemd.service` opens the file format rather than a command of the same name.

### 2. What the shell does to a line: expansion and quoting

*In one sentence:* bash rewrites every line — variables, word splitting, file-name patterns — before the program sees it, and quoting decides which of those rewrites happen.

Most surprises in shell scripts — a file reported missing that is there, one argument split into two, a deletion that reaches further than meant — come from not knowing what bash does to a line before the program sees it. Before any program runs, bash turns your line into a list of words, and the program sees only that list — never the quotes, the `$` or the `*` you typed. The rule is three rewrites, in the order the Bash manual gives, and one switch that turns them off: quoting. Inside single quotes every character is literal; inside double quotes a variable still expands, but its value is neither cut apart nor matched against file names. For example, with `dir` set to `day 1`, the line `ls $dir/*.mcap` hands `ls` two words, `day` and `1/*.mcap`, not one path — before `ls` has even started; the demonstration below prints exactly such lists.

> **Shell expansion, defined.** **Shell expansion** is the *rewriting bash applies to a command line before running anything*: a property of the line and of the shell's variables, never of the program, which receives only the result. Three conditions define that result. Unquoted words are **expanded** — `~` to the home directory, `$name` to a variable's value, `$(command)` to a command's output. The unquoted results are **split** into separate words at spaces, tabs and newlines. And each unquoted word containing `*`, `?` or `[` is a **pattern**, replaced by the sorted names of the existing files it matches, or left exactly as typed if it matches none. Double quotes stop the second and third steps; single quotes stop all three.
>
> $$n_{\text{args}}(\pi)=\max(m_\pi,\,1)$$
>
> where $\pi$ is one unquoted pattern word and $m_\pi$ the number of existing names it matches, so a pattern hands the program as many arguments as it matched, or its own literal text when it matched none, and a double-quoted `"$d"` hands over exactly one argument whatever `$d` contains.
>
> - **Example**: `"$dir"/*.mcap` with `dir="day 1"` and two split files in that directory gives $m=2$: two arguments, both real files (below).
> - **Non-example**: the same line without the quotes. The value `day 1` is split first, so the program receives `day` and `1/*.mcap` — the second a pattern that matched nothing and was passed through as literal text. No error is raised; the program simply receives a name that is not a file.
> - **Why it matters**: bag directories, calibration files and dataset folders acquire spaces and dates in their names. A script that quotes every `"$variable"` behaves the same for all of them.

The rules, saved as `quote_demo.sh` and run with bash on the laptop, in a directory holding `day 1/run_0.mcap`, `day 1/run_1.mcap` and an empty directory `empty`. `printf '[%s]\n'` prints each argument it receives between brackets, so it shows exactly what a program would get:

```bash
#!/bin/bash
dir="day 1"
printf '[%s]\n' $dir/*.mcap
echo "--- quoted"
printf '[%s]\n' "$dir"/*.mcap
echo "--- a pattern that matches nothing"
printf '[%s]\n' empty/*.mcap
echo "--- an empty variable in front of /*"
bagdir=""
printf '[%s]\n' $bagdir/* | head -3
echo "--- the same with \${bagdir:?}"
printf '[%s]\n' "${bagdir:?is empty}"/*
echo "not reached"
```

```text
[day]
[1/*.mcap]
--- quoted
[day 1/run_0.mcap]
[day 1/run_1.mcap]
--- a pattern that matches nothing
[empty/*.mcap]
--- an empty variable in front of /*
[/Applications]
[/Library]
[/System]
--- the same with ${bagdir:?}
quote_demo.sh: line 12: bagdir: is empty
```

The fourth case is the one that destroys data. With `bagdir` empty, `$bagdir/*` becomes `/*`, every entry at the root — `/Applications`, `/Library` and `/System` on this Mac, `/bin`, `/boot`, `/etc` on the cart — so `rm -rf $bagdir/*` would try to delete the machine. `${bagdir:?message}` refuses to expand an empty or unset variable: the script prints the message and stops, and `not reached` never runs. `set -u` (§6) is weaker than it looks, because it objects only to a variable that was never set, not to one set to the empty string (`nounset_demo.sh`):

```bash
#!/bin/bash
set -u
bagdir=""
echo "empty is allowed: [$bagdir]"
echo "unset is not: [$bag_dir]"
echo "not reached"
```

```text
empty is allowed: []
nounset_demo.sh: line 5: bag_dir: unbound variable
```

The misspelling `bag_dir` is caught; the empty `bagdir` is not. Quote every variable, guard the ones that must not be empty with `:?`, and the whole class of accident is closed.

### 3. Processes, signals and jobs

*In one sentence:* a running program is a process with a number, a parent and an exit status, and signals — from the terminal, from `kill`, from systemd — are how it is stopped, cleanly or not.

When the robot misbehaves you need to find its programs, stop them, and read how each one ended — and the way you stop them decides whether the controller gets to command zero before it exits. A **process** is one running instance of a program. It has a number (PID), a parent (PPID), a user and groups (§4), an environment (§5), a working directory (§1) and three open streams (§6). `ps -ef` lists every process on the machine; `pgrep -af controller` lists those whose *full command line* contains `controller`. Without `-f`, pgrep matches only the process name, which the kernel cuts to 15 characters — a node executable called `vision_goal_publisher` is `vision_goal_pub` there — and which is `python3` for a script started as `python3 script.py`. `top` shows them live. A process is started by another process and returns an **exit status** to it when it ends: 0 for success, 1–255 for failure. Bash reports 127 for a command it could not find and 126 for a file it found but could not execute (§4).

A command followed by `&` runs as a **background job**, and the shell returns at once. `jobs` lists the shell's jobs, `fg` brings one to the foreground, Ctrl-Z stops the foreground job and `bg` lets it continue in the background. This bookkeeping is **job control**: an interactive shell gives each job a process group of its own, so that Ctrl-C, Ctrl-Z, `fg` and `bg` act on one job at a time. A script has job control off unless `set -m` turns it on, and this section's last trap comes from that. In `ps` or `top`, a state letter says what each process is doing: `S` is interruptible sleep — a node blocked waiting for its next message looks like this — `D` uninterruptible sleep (usually disk or device I/O), `T` stopped, and `Z` a zombie whose parent never collected its exit status.

> [!note]- Deeper · 더 깊이
> One sleeping job, listed on the laptop (`jobs_demo.sh`):
>
> ```bash
> #!/bin/bash
> set -m                       # job control on, as in an interactive shell
> sleep 100 &
> sleep 1
> ps -o pid,ppid,stat,etime,command -p $!
> jobs
> kill %1
> ```
>
> ```text
>   PID  PPID STAT ELAPSED COMMAND
> 96448 96447 S      00:01 sleep 100
> [1]+  Running                 sleep 100 &
> ```

The controls that stop a process are **signals**.

> **Signal, defined.** A **signal** is a *small numbered notification that the kernel delivers to a process* — no payload, and not an order the process must obey, with two exceptions. Four conditions define it. Each signal has a **number and a default action**: SIGHUP 1, SIGINT 2, SIGKILL 9 and SIGTERM 15 all terminate the process unless it arranged otherwise, and these four numbers are the same on every Linux architecture. A process may **catch** a signal with a handler of its own or **ignore** it — except SIGKILL and SIGSTOP, which can be neither caught, blocked nor ignored. Signals have **three kinds of sender**: the terminal (Ctrl-C sends SIGINT to the processes of the foreground job, Ctrl-Z sends SIGTSTP), another process (`kill`, which sends SIGTERM unless told otherwise; systemd stopping a service, §10), and the kernel itself. And a process that **dies from** a signal leaves the signal's number in the status its parent reads.
>
> $$s=128+n$$
>
> where $n$ is the number of the signal that killed the process and $s$ the exit status bash reports, so 130 means SIGINT, 143 SIGTERM and 137 SIGKILL; Python's subprocess machinery, which `ros2 launch` uses, reports the same death as $-n$ instead.
>
> - **Example**: three `sleep` processes on the laptop, each sent one signal: statuses 130, 143 and 137 (below), which is how you read a line such as `process has died [pid 4242, exit code -2, ...]` in a launch log — SIGINT, not a crash.
> - **Non-example**: an exit status of 0 or 1 after you pressed Ctrl-C. A program that *catches* SIGINT and shuts down cleanly exits with whatever status it chooses; $128+n$ describes only a process the signal killed. And status 1 is never a signal: it is the program reporting a failure of its own.
> - **Why it matters**: the stop path of a robot is a sequence of signals — Ctrl-C, then `ros2 launch`'s escalation, then systemd's timeout — and only a process that handles them can stop its motor and close its files before it goes.

The three deaths, run on the laptop (`signals_demo.sh`):

```bash
#!/bin/bash
set -m                       # job control on, so the background job keeps SIGINT
for sig in INT TERM KILL; do
  sleep 100 &
  pid=$!
  kill -s "$sig" "$pid"
  wait "$pid"
  echo "SIG$sig -> status $?"
done
```

```text
[1]+  Interrupt: 2            sleep 100
SIGINT -> status 130
signals_demo.sh: line 7: 96455 Terminated: 15          sleep 100
SIGTERM -> status 143
signals_demo.sh: line 7: 96456 Killed: 9               sleep 100
SIGKILL -> status 137
```

**How a node should react.** Both ROS 2 client libraries install handlers for SIGINT and SIGTERM by default: `rclcpp::init` and `rclpy.init` catch the two signals and shut down the node's context, which makes `spin` return. That is the moment a controller should command zero, close its serial port and let the recorder close its bag. When `ros2 launch` shuts down, every process it started is stopped in three steps: SIGINT (on Ctrl-C it comes straight from the terminal, otherwise from launch), then SIGTERM from launch to any process still running 5 s later, then SIGKILL 5 s after that. A node that needs longer than 5 s to stop is therefore killed mid-cleanup, and SIGKILL gives no process a chance to write the end of a file. The motor's safe state cannot depend on this chain at all; it lives in the drive and the stop circuit ([[04-robotics/ros2/from-simulation-to-hardware|25.11 §6]]).

**The background job that ignores Ctrl-C.** In a script, job control is off, and bash starts every background job with SIGINT and SIGQUIT *ignored*. A start-up script that launches the recorder with `&` and later tries to stop it the way Ctrl-C would, with `kill -INT`, leaves it running. On the laptop (`bg_sigint.sh`):

```bash
#!/bin/bash
# no job control (the default in a script): a background job ignores SIGINT
sleep 5 &
pid=$!
sleep 1                      # let the child start: a signal sent before it has set SIGINT to ignored still kills it
kill -s INT "$pid"
sleep 1
kill -0 "$pid" && echo "after SIGINT: still running"
kill -s TERM "$pid"
wait "$pid"
echo "after SIGTERM: status $?"
```

```text
after SIGINT: still running
bg_sigint.sh: line 10: 96459 Terminated: 15          sleep 5
after SIGTERM: status 143
```

`kill -0` sends no signal; it only tests that the process exists. Stop a script's background jobs with SIGTERM, which is `kill`'s default — or, better, let systemd own them (§10).

### 4. Users, groups and permissions

*In one sentence:* every file has an owner, a group and nine permission bits, exactly one class of which applies to a given process, and a serial device is opened through its group.

The first thing that fails on a new robot computer is usually a permission: the controller cannot open its serial port, and the error says only *Permission denied*. Every process runs as a **user** with a numeric ID, one primary **group** and a list of supplementary groups; `id` prints all three for your shell. The user `root`, ID 0, bypasses the permission checks below — except that even root can execute a file only if at least one of its execute bits is set. `sudo COMMAND` runs one command as root if the machine's sudoers policy allows your account, and it runs it in a *reset* environment containing only a few variables such as `PATH`, `HOME` and `USER` — so of what `source` (§5) put into your terminal's environment, at most `PATH` reaches the command, and `sudo ros2 …` fails.

Every file carries an owner, a group and nine permission bits: read, write and execute for the owner (`u`), the group (`g`) and everyone else (`o`). `ls -l` shows them after a type letter: `-` a regular file, `d` a directory, `l` a symbolic link, `c` a character device such as a serial port. On a directory, read lists the names, write creates and deletes entries, and execute is *search*: the right to pass through it on a path (§1).

> **Permission mode, defined.** A file's **permission mode** is *nine bits in three classes of three* — owner, group, others, each with read, write and execute — written as three octal digits; it belongs to the file, not to the user. Three conditions decide an access. The kernel picks **exactly one class** for the process: the owner class if the process's user owns the file, else the group class if the file's group is the process's group or one of its supplementary groups, else the others class — the first match wins, even when a later class would allow more. It then checks **only that class's three bits** against the access asked for. And the digits are **sums of bits**, read = 4, write = 2, execute = 1, so each digit from 0 to 7 names one combination.
>
> $$m=(d_u\,d_g\,d_o)_8=64\,d_u+8\,d_g+d_o,\qquad d=4r+2w+x$$
>
> where $r,w,x\in\{0,1\}$ are one class's bits and $d_u,d_g,d_o$ the three digits, so `rw-` is $4+2=6$, `r-x` is $5$, and `rw-rw----` is 660 in octal, 432 in decimal; files are created with the mode the program asks for, usually 666, minus the bits in the shell's `umask`, usually 022, which is why new files appear as 644.
>
> - **Example**: the encoder board. Ubuntu's udev rules give every `ttyACM` device the group `dialout`, and udev's default for a device node with a group is 0660, so `/dev/ttyACM0` shows `crw-rw---- root dialout`. The user `robot` is not `root`, so the owner class does not apply; if `robot` is in `dialout`, the group digit 6 grants read and write; if not, the others digit 0 grants nothing, and the controller's `open()` fails with *Permission denied*.
> - **Non-example**: `sudo chmod 666 /dev/ttyACM0`. It works until the board is unplugged or the cart reboots, because udev creates the node afresh each time with its rules' mode; the fix is the group, not the mode.
> - **Why it matters**: "Permission denied" on a robot is almost never solved by root. Find the class that applies, and change the group or the mode that answers it.

The bits, set and read back on the laptop (`perm_demo.sh`). macOS's `stat -f "%Sp %Lp"` prints the mode as letters and octal; on the cart the GNU form is `stat -c "%A %a" FILE` (from the manual, not run here):

```bash
#!/bin/bash
umask
touch encoder_stub
stat -f "%Sp %Lp  %N" encoder_stub
chmod 660 encoder_stub
stat -f "%Sp %Lp  %N" encoder_stub
chmod u=rw,g=r,o= encoder_stub
stat -f "%Sp %Lp  %N" encoder_stub
chmod 000 encoder_stub
cat encoder_stub; echo "cat status: $?"
```

```text
0022
-rw-r--r-- 644  encoder_stub
-rw-rw---- 660  encoder_stub
-rw-r----- 640  encoder_stub
cat: encoder_stub: Permission denied
cat status: 1
```

**Joining the group that owns the device.** On the cart, from the manual, not run here:

```bash
sudo usermod -aG dialout robot     # -a appends; without it, -G replaces robot's groups
```

Then log out and back in. A login — an ssh session, for one — reads the account's groups from the group database, and every process started afterwards inherits that list unchanged; so the terminal you ran `usermod` in, and every node it starts, still lacks `dialout`. `id` in a new ssh session shows it. Leaving out `-a` is its own disaster: `usermod -G dialout robot` makes `dialout` the account's *only* supplementary group and removes it from every other, `sudo` included.

**The execute bit.** A script runs as `./p6_check.sh` only if its `x` bit is set; `bash p6_check.sh` runs it regardless, because then bash reads the file as data. On the laptop (`exec_bit.sh`):

```bash
#!/bin/bash
printf '#!/bin/bash\necho "p6 check ok"\n' > p6_check.sh
./p6_check.sh; echo "status: $?"
bash p6_check.sh; echo "status: $?"
chmod +x p6_check.sh
stat -f "%Sp %Lp  %N" p6_check.sh
./p6_check.sh; echo "status: $?"
```

```text
exec_bit.sh: line 3: ./p6_check.sh: Permission denied
status: 126
p6 check ok
status: 0
-rwxr-xr-x 755  p6_check.sh
p6 check ok
status: 0
```

Status 126 is bash's "found, but not executable". `chmod +x` with no class letter adds execute for all three classes except where the `umask` forbids it, giving 755 here.

### 5. The environment, `PATH` and `source`

*In one sentence:* environment variables flow from a process to the processes it starts and never back, which is why a terminal needs `source`, and why an ssh command, `sudo` and a service each need their own.

A command that works in one terminal but not in another — or at the keyboard but not over ssh or at boot — is almost always the environment. An **environment variable** is a `NAME=value` string that a process carries and hands to the processes it starts. `printenv` lists your shell's environment and `echo "$HOME"` prints one variable. A shell variable enters the environment only when it is exported (`export NAME=value`), and `NAME=value command` sets one variable for one command.

The variable that decides what runs is `PATH`: a colon-separated list of directories. When you type a name without a `/`, bash tries each directory in order and runs the first executable file of that name it finds; if none has it, the result is `command not found` and status 127. `type -a NAME` lists every match in order, `command -v NAME` the one that will run.

> **Environment variable, defined.** An **environment variable** is a *name–value string in a process's environment*, a list the kernel hands each new program at start — a property of one process, not of the machine or the terminal. Three conditions define how far it reaches. A child **receives a copy** of its parent's exported variables when it is created. Changes afterwards **flow only downward**: a child can change its own copy, never its parent's, so a script run as a program cannot alter the shell that ran it. And a variable reaches a process **only along the chain that started it**: two terminals, a systemd service and a `sudo` command are four separate chains.
>
> $$c\ \longmapsto\ d_k/c,\qquad k=\min\{\,i:\ d_i/c\ \text{is an executable file}\,\},\qquad \texttt{PATH}=d_1{:}d_2{:}\cdots$$
>
> where $c$ is a command name with no `/` and $d_i$ the directories of `PATH` in order, so the first directory that holds a program of that name wins; prepending a directory makes its programs override everything after it, which is exactly what sourcing a ROS 2 setup file does.
>
> - **Example**: `source /opt/ros/jazzy/setup.bash` prepends `/opt/ros/jazzy/bin` to `PATH` in this shell, so `ros2` resolves there, and exports the other variables ROS 2 reads; every node started from this shell inherits them.
> - **Non-example**: `bash setup.bash`. It runs the file in a *child* shell, which sets every variable in its own copy and then exits, so the terminal you typed it in is unchanged — `command not found` one line later (below).
> - **Why it matters**: nearly every "works in one terminal, not in another" on a robot is a variable that reached one chain of processes and not the other.

`source FILE` — or `. FILE` — reads the file's commands into the *current* shell, which is the only way a file can change your terminal's environment. A stand-in for a workspace's setup file, whose `bin` directory holds a one-line program `p6_status`:

```bash
# fake_ws/setup.bash: a stand-in for a workspace's install/setup.bash
export P6_WS="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PATH="$P6_WS/bin:$PATH"
```

run and then sourced, on the laptop (`env_demo.sh`):

```bash
#!/bin/bash
bash fake_ws/setup.bash
echo "after bash setup.bash:   P6_WS=${P6_WS:-<unset>}"
p6_status
source fake_ws/setup.bash
echo "after source setup.bash: P6_WS set: $([ -n "$P6_WS" ] && echo yes)"
p6_status
```

```text
after bash setup.bash:   P6_WS=<unset>
env_demo.sh: line 4: p6_status: command not found
after source setup.bash: P6_WS set: yes
p6_status: controller up
```

**The ROS 2 case.** A shell that has not sourced ROS 2's setup file can reach neither its commands nor its packages, which is why every new terminal needs `source /opt/ros/jazzy/setup.bash`, or that line in `~/.bashrc` — the file bash reads for every interactive shell that is not a login shell; an ssh login is a login shell, and Ubuntu's default `~/.profile`, which it reads, reads `~/.bashrc` in turn. `printenv | grep -i ROS` should then show `ROS_VERSION=2`, `ROS_PYTHON_VERSION=3` and `ROS_DISTRO=jazzy`. What the setup file puts in the environment, and why a workspace is sourced *after* the installation, is the underlay–overlay rule of [[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]; the terminal that was never sourced is the failure drilled in [[04-robotics/ros2/what-ros2-is|25.1 §11]].

**The ssh command that finds no ROS.** `ssh p6` gives you an interactive shell, and `ros2` works in it. `ssh p6 'ros2 topic list'` answers `ros2: command not found`. Bash does read `~/.bashrc` when sshd starts it to run a single command, but Ubuntu's default `~/.bashrc` begins by returning at once from any shell that is not interactive, so the `source` line that the ROS 2 instructions append at the *end* of the file never runs. On the laptop, a file whose first lines are those of Ubuntu 24.04's default `~/.bashrc`, with a stand-in for the ROS 2 line at its end, sets the stand-in when an interactive bash reads it and not when a non-interactive one does (`interactive: yes`, `non-interactive: no`; the script is in the callout).

> [!note]- Deeper · 더 깊이
> `bashrc_demo.sh`: `--rcfile … -i` starts an interactive bash that reads the file, and `BASH_ENV` makes a non-interactive bash read it — standing in for the read that sshd's non-interactive bash makes of `~/.bashrc`:
>
> ```bash
> #!/bin/bash
> cat > ubuntu_like_bashrc <<'END'
> # If not running interactively, don't do anything
> case $- in
>     *i*) ;;
>       *) return;;
> esac
> # ... the rest of Ubuntu's default ~/.bashrc ...
> export P6_ROS_SOURCED=yes      # stands for: source /opt/ros/jazzy/setup.bash, appended at the end
> END
> echo "interactive:     $(bash --rcfile ./ubuntu_like_bashrc -i -c 'echo ${P6_ROS_SOURCED:-no}' 2>/dev/null)"
> echo "non-interactive: $(BASH_ENV=./ubuntu_like_bashrc bash -c 'echo ${P6_ROS_SOURCED:-no}')"
> ```
>
> ```text
> interactive:     yes
> non-interactive: no
> ```

Source explicitly in the command itself — `ssh p6 'source /opt/ros/jazzy/setup.bash && ros2 topic list'` — and never rely on a file being read. The same rule covers the two other chains that do not pass through your terminal: `sudo`, whose reset environment drops the ROS variables (§4), and a systemd service, which reads no shell start-up file at all (§10).

### 6. Pipes, redirection and scripts

*In one sentence:* every process has three streams that `>`, `2>` and `|` rewire, a pipeline reports a single exit status, and `set -euo pipefail` makes a script stop on real failures only once you say which statuses are answers.

A robot writes logs faster than anyone reads them. Pipes turn a log into a few numbers and scripts run those pipes every night — and both are worth having only if a failure cannot hide in them. Every process starts with three open streams: standard input (0), standard output (1) and standard error (2). A program writes its results to standard output and its complaints to standard error, and both appear in your terminal until you redirect them:

| Syntax | Effect |
|---|---|
| `cmd > f`, `cmd >> f` | standard output into file `f`, replacing it or appending |
| `cmd 2> f` | standard error into `f` |
| `cmd > f 2>&1` | both into `f`: first 1 goes to `f`, then 2 goes where 1 now goes |
| `cmd < f` | standard input from `f` |
| `a \| b` | `a`'s standard output into `b`'s standard input; `a`'s standard error still goes to the terminal |

Redirections are applied left to right, so order matters. `2>&1 > f` points 2 at the terminal (where 1 was *then*) and only afterwards moves 1 to `f`. The demonstrations below use a stand-in for a node, which writes two log lines to standard error as a ROS 2 node does:

```python
# fake_node.py: a stand-in for a ROS 2 node, which writes its log lines to standard error
import sys
print("[INFO] [1790150400.000000000] [controller]: control loop started at 200 Hz", file=sys.stderr)
print("[WARN] [1790150460.000000000] [controller]: goal older than 70 ms", file=sys.stderr)
```

Both orders, on the laptop (`redirect_demo.sh`):

```bash
#!/bin/bash
python3 fake_node.py > both.log 2>&1
echo "both.log has $(wc -l < both.log) lines"
python3 fake_node.py 2>&1 > only_stdout.log
echo "only_stdout.log has $(wc -l < only_stdout.log) lines"
```

```text
both.log has        2 lines
[INFO] [1790150400.000000000] [controller]: control loop started at 200 Hz
[WARN] [1790150460.000000000] [controller]: goal older than 70 ms
only_stdout.log has        0 lines
```

(macOS's `wc` pads its count with spaces, as above; a script should read the count as a number and never rely on its spacing.)

**Why `| grep` misses a node's warnings.** ROS 2 nodes write their log lines to the console on *standard error*, in the default format `[SEVERITY] [time] [node]: message`. A pipe carries standard output only, so `ros2 run … | grep WARN` lets every log line through to the terminal untouched while `grep` reads nothing. On the laptop, with the same stand-in (`stderr_pipe.sh`):

```bash
#!/bin/bash
python3 fake_node.py | grep -c WARN
python3 fake_node.py 2>&1 | grep -c WARN
```

```text
[INFO] [1790150400.000000000] [controller]: control loop started at 200 Hz
[WARN] [1790150460.000000000] [controller]: goal older than 70 ms
0
1
```

Write `2>&1 |`. Bash 5.2 on the cart also accepts `|&` as a shorthand for it; the laptop's bash 3.2 rejects `|&` as a syntax error.

**A day's log, filtered.** Pipes are how a 76-line log — or a 76,000-line one — becomes three numbers. The log below is synthetic: one 8-hour shift of P6's three nodes in ROS 2's console format, written for this page by this script (it writes a file, so CI does not run it):

```python
# not-run: writes p6_day1.log into the working directory (the synthetic log of §6, made on the laptop)
t0 = 1790150400  # 2026-09-23 08:00:00 UTC
events = (
    [((i + 1) * 1800, "INFO", "recorder", "bag split written") for i in range(16)]
    + [(60 + i * 600, "WARN", "vision", "frame dropped: exposure timeout") for i in range(46)]
    + [(300 + i * 2700, "WARN", "controller", "goal older than 70 ms") for i in range(10)]
    + [(9000 + i * 7, "ERROR", "controller", "encoder read failed: device not found") for i in range(3)]
)
events.sort()
with open("p6_day1.log", "w") as f:
    f.write("[INFO] [%d.000000000] [controller]: control loop started at 200 Hz\n" % t0)
    for dt, sev, node, msg in events:
        f.write("[%s] [%d.000000000] [%s]: %s\n" % (sev, t0 + dt, node, msg))
```

Its first four lines:

```text
[INFO] [1790150400.000000000] [controller]: control loop started at 200 Hz
[WARN] [1790150460.000000000] [vision]: frame dropped: exposure timeout
[WARN] [1790150700.000000000] [controller]: goal older than 70 ms
[WARN] [1790151060.000000000] [vision]: frame dropped: exposure timeout
```

Warnings and errors per node, busiest first — `grep -E` keeps the lines that begin with either severity, `cut` keeps fields 1 and 3 (severity and node), `sort` brings equal lines together, `uniq -c` counts each run of equal lines, and `sort -rn` orders by count:

```bash
grep -E '^\[(WARN|ERROR)\]' p6_day1.log | cut -d' ' -f1,3 | sort | uniq -c | sort -rn
```

```text
  46 [WARN] [vision]:
  10 [WARN] [controller]:
   3 [ERROR] [controller]:
```

`uniq` merges only *adjacent* equal lines, so the first `sort` is not optional.

**Exit statuses of a pipeline.** Each command in a pipeline runs as its own process and returns its own status, and `grep` uses three: 0 when it selected a line, 1 when it selected none, 2 when something went wrong, such as a missing file. The shell reports one number for the whole pipeline.

> **Pipeline exit status, defined.** The **exit status of a pipeline** is *the single number bash records in `$?` for a chain `c₁ | c₂ | … | cₙ`* — a property of the pipeline under the shell's options, not of any one command. Three conditions define it. Each $c_k$ runs as a **separate process** with its own status $s_k$, all of which bash keeps in the array `PIPESTATUS`. **By default** the pipeline's status is the last command's, $s_n$, whatever happened before it. With **`set -o pipefail`** it is the status of the rightmost command that failed, or 0 if none did.
>
> $$s_{\text{pipe}}=\begin{cases}s_n & \text{pipefail off}\\ s_{k^\ast},\ k^\ast=\max\{k:\ s_k\neq 0\} & \text{pipefail on, } 0 \text{ if no } s_k\neq0\end{cases}$$
>
> where $s_k$ is the status of the $k$-th command, so without `pipefail` a failure anywhere but in the last command disappears, and with it the pipeline fails whenever any stage does.
>
> - **Example**: `grep ERROR p6_day2.log | wc -l` when the day-2 log was never written. `grep` exits 2, `wc` prints 0 and exits 0: $(s_1,s_2)=(2,0)$, so $s_{\text{pipe}}=0$ by default and 2 under `pipefail` (below, and the picture's panel C).
> - **Non-example**: `grep ERROR p6_clean.log | wc -l` on a log with no errors. $(s_1,s_2)=(1,0)$, and under `pipefail` the pipeline "fails" with 1 although nothing went wrong — `grep`'s 1 means *no line selected*, not *error*. A script that also has `set -e` stops right there, silently (below).
> - **Why it matters**: a check that reports "0 errors" because it read nothing is worse than no check; the status of every stage is the difference between the two.

The example, on the laptop (`pipefail_demo.sh`; there is no `p6_day2.log`):

```bash
#!/bin/bash
grep ERROR p6_day2.log | wc -l
echo "status without pipefail: $?"
set -o pipefail
grep ERROR p6_day2.log | wc -l
echo "status with pipefail: $?"
```

```text
grep: p6_day2.log: No such file or directory
       0
status without pipefail: 0
grep: p6_day2.log: No such file or directory
       0
status with pipefail: 2
```

**Scripts.** A script is a file of commands with `#!/bin/bash` as its first line and its execute bit set (§4). Start every script with `set -euo pipefail`: `-e` stops the script when a command fails — except in the places bash exempts, such as the test of an `if` and every command of an `&&` or `||` list but the last; `-u` stops it at the first variable that was never set (§2); and `pipefail` makes a failure anywhere in a pipeline count. The three together have one trap, the non-example above. A log check whose only mistake is finding nothing (`strict_demo.sh`):

```bash
#!/bin/bash
set -euo pipefail
n=$(grep ERROR p6_clean.log | wc -l)
echo "errors: $n"
```

prints nothing at all and exits with status 1 on the laptop, because `grep`'s "no line selected" ended the script. The cure is to say which statuses are answers. `p6_check_log.sh`, the check this page uses, accepts `grep`'s 1 and nothing else:

```bash
#!/bin/bash
# p6_check_log.sh: count errors and warnings in one day's node log
set -euo pipefail
log="${1:?usage: p6_check_log.sh LOGFILE}"
# grep -c exits 1 when it counts zero lines; that is an answer, not a failure
errors=$(grep -c '^\[ERROR\]' "$log" || test $? -eq 1)
warnings=$(grep -c '^\[WARN\]' "$log" || test $? -eq 1)
echo "$log: $errors errors, $warnings warnings"
```

Run on the laptop against the day-1 log, a clean log of two `INFO` lines, a log that does not exist, and no argument at all:

```bash
#!/bin/bash
for log in p6_day1.log p6_clean.log p6_day2.log; do
  ./p6_check_log.sh "$log"; echo "status $?"
done
./p6_check_log.sh; echo "status $?"
```

```text
p6_day1.log: 3 errors, 56 warnings
status 0
p6_clean.log: 0 errors, 0 warnings
status 0
grep: p6_day2.log: No such file or directory
status 1
./p6_check_log.sh: line 4: 1: usage: p6_check_log.sh LOGFILE
status 1
```

The missing log now fails loudly, and the clean log passes. `|| true` would also have silenced the clean case — and the missing file with it.

### 7. Installing software: apt, pip or a container

*In one sentence:* apt owns the system, pip owns a virtual environment you made, a container owns its image, and each piece of software should come from the one tool that owns the place it goes.

One package installed the wrong way can break ROS 2's own tools for every account on the machine, so choosing an installer is choosing who owns which files. Software reaches the cart by three routes, and each one owns a different part of the disk.

**apt** installs Ubuntu's packages, and ROS 2's, which come from the ROS project's own apt repository. `sudo apt update` refreshes the list of what is available; `sudo apt install ros-jazzy-ros-base` installs a package and everything it depends on, for every account on the machine, under `/usr` and — for ROS 2 — `/opt/ros/jazzy`. It needs root, and it installs one version of each package for the whole machine. Type `apt` at the keyboard and use `apt-get` in scripts, because APT does not promise to keep `apt`'s command line stable between versions. A ROS 2 workspace names its system dependencies as keys in `package.xml`, and `rosdep` turns those keys into apt packages ([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]).

**pip** installs Python packages from the Python Package Index. On Ubuntu 24.04 it refuses to install into the system Python at all: the file `/usr/lib/python3.12/EXTERNALLY-MANAGED` marks that interpreter as apt's, and pip stops with an error that says so, before it overwrites anything apt installed. The error is the protection working. `sudo pip install --break-system-packages …` goes around it, and puts the package where every Python program on the machine — apt's tools, ROS 2's nodes and command-line tools — may import it instead of the version they were built against. ROS 2's own guide lists the routes in the same order — rosdep, then a package manager, then a virtual environment — with a warning that the Python interpreter must be the one the ROS 2 binaries were built for. Python packages for your own analysis and learning code go into a virtual environment you create, which is this track's Python page ([[02-foundations/tools/python-research-code|12.3 §1]]).

**A container** carries a whole Ubuntu userspace in an image — another release, another ROS distribution, a pinned set of versions — and runs it isolated from the rest of the machine. It is the right tool when the environment must differ from the cart's, or must be frozen so that a result can be rerun later ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]). Its price on a robot is that nothing from the host enters by default: the encoder board must be passed in by name, as `docker run --device=/dev/ttyACM0 …`, and so must everything else the container is to see.

| You need | Install with | Because |
|---|---|---|
| ROS 2, drivers, system libraries | apt, through rosdep in a workspace | one version for the whole machine, shared by every program |
| a Python package for your own code | pip, inside a virtual environment | it never touches the interpreter that apt and ROS 2 use |
| another Ubuntu or ROS release, or a frozen environment for a result | a container | the whole userspace travels in the image |

The rule behind the table: **let exactly one tool write each place on the disk** — apt the system, pip the environment you made, the container its image — and never use `sudo` to make one tool write where another is in charge. Every failure in this section is two tools sharing one directory.

### 8. Working on another machine: ssh, rsync and tmux

*In one sentence:* ssh with a key reaches the cart, rsync copies only what changed, and tmux keeps a run alive when the connection drops — which otherwise hangs up every job of the ssh shell.

You rarely sit at the robot. You log in to it from a workstation, copy each day's data off it, and leave runs going while you are away; ssh, rsync and tmux do those three jobs.

**ssh** gives you a shell on another machine over an encrypted connection: `ssh robot@192.168.10.2`, or with a host alias, `ssh p6`. An alias is an entry in `~/.ssh/config`; P6's is

```text
Host p6
    HostName 192.168.10.2
    User robot
    IdentityFile ~/.ssh/id_ed25519
    ServerAliveInterval 15
    ServerAliveCountMax 4
```

and `ssh -G p6` prints what a name resolves to without connecting — the fastest way to find out why `ssh p6` goes somewhere unexpected. The two `ServerAlive` lines make a dead connection *visible*: when the cart stops answering, ssh asks every 15 s and gives up after 4 unanswered requests, so a dropped link ends the session after about $15\times4=60$ s instead of leaving a frozen terminal. They do not keep anything alive on the cart — that is tmux's job, below.

> [!note]- Deeper · 더 깊이
> The entry saved as `ssh_config_p6` and resolved on the laptop with `-F` (read this file instead of `~/.ssh/config`), the output filtered by `grep` to the lines the entry sets (run from a terminal):
>
> ```bash
> ssh -G -F ./ssh_config_p6 p6 | grep -E '^(hostname|user|port|identityfile|serveraliveinterval|serveralivecountmax) '
> ```
>
> ```text
> user robot
> hostname 192.168.10.2
> port 22
> serveralivecountmax 4
> serveraliveinterval 15
> identityfile ~/.ssh/id_ed25519
> ```

**Keys instead of passwords.** `ssh-keygen -t ed25519` makes a key pair: a private key that never leaves your workstation and a `.pub` public key; `ssh-copy-id p6` appends the public key to the cart's `~/.ssh/authorized_keys`, after which `ssh p6` logs in with the key instead of the account's password. Both ends check permissions (§4). ssh refuses a private key that anyone else can read — a throwaway key made on the laptop, its mode changed to 644 and read back (`key_demo.sh`; output trimmed to the lines that teach):

```bash
#!/bin/bash
ssh-keygen -t ed25519 -C robot-demo -N '' -f ./demo_key -q
stat -f "%Sp %Lp  %N" demo_key demo_key.pub
chmod 644 demo_key
ssh-keygen -y -f ./demo_key > /dev/null; echo "ssh-keygen -y status: $?"
```

```text
-rw------- 600  demo_key
-rw-r--r-- 644  demo_key.pub
Permissions 0644 for './demo_key' are too open.
This private key will be ignored.
ssh-keygen -y status: 255
```

The cart's ssh server checks its end too: with its default `StrictModes yes` it inspects the modes and ownership of `robot`'s files and home directory before accepting a login, so a home directory or `~/.ssh` that other users can write to is enough to make key login fail.

**Copying.** `scp FILE p6:DIR/` copies one file over the same connection. For a directory of bags, `rsync -a SRC/ DEST/` is better, for three reasons in its manual: it runs over ssh by default; it skips every file whose size and modification time already match at the destination, so the same command run twice copies only what is new; and it deletes a partially transferred file when interrupted (unless given `--partial`), so a re-run never mistakes half a file for a whole one. On the laptop, a mock bag directory of two split files copied, copied again, and copied after the recorder wrote a third (`rsync_demo.sh`):

```bash
#!/bin/bash
rsync -a --itemize-changes bags/day1/ ws/day1/
echo "== same command again"
rsync -a --itemize-changes bags/day1/ ws/day1/
echo "== after the recorder writes a third split file"
head -c 1000000 /dev/urandom > bags/day1/day1_2.mcap
rsync -a --itemize-changes bags/day1/ ws/day1/
```

```text
cd+++++++ ./
>f+++++++ day1_0.mcap
>f+++++++ day1_1.mcap
>f+++++++ metadata.yaml
== same command again
== after the recorder writes a third split file
.d..t.... ./
>f+++++++ day1_2.mcap
```

Each output line is one item rsync acted on: `>f+++++++` a file received and newly created, `cd+++++++` a directory created, `.d..t....` a directory whose modification time changed. The second run lists nothing because nothing differed, and the third sends only the new file. The trailing slash on the source is part of the meaning: `bags/day1/` copies the directory's *contents*, `bags/day1` copies the directory itself and creates `DEST/day1/` inside the destination. Between the two machines the same command, run on the workstation, reads `rsync -a p6:bags/day1/ ~/p6_bags/day1/`.

**Keeping a run alive: tmux.** A program started from an ssh shell belongs to that shell, and dies with it when the connection drops (below). tmux is a terminal multiplexer: its sessions are held by a tmux server on the cart and, in its manual's words, survive accidental disconnection such as an ssh timeout. The routine, from the tmux manual and rosbag2's README, not run here (tmux is not installed on the laptop):

```bash
ssh p6
tmux new -s day1              # a new session named day1, on the cart
ros2 bag record --topics /cmd /goal /camera/image/compressed -d 1800 -o bags/day1
# press C-b then d to detach; the recording keeps running
tmux ls                       # later, from any new ssh session: list the sessions
tmux attach -t day1           # and reattach to this one
```

`-d 1800` splits the bag every 30 minutes, the unit an interrupted `rsync` re-sends.

What kills the run is a **hangup**. When an ssh connection drops, the terminal it provided disappears and the kernel sends SIGHUP to the shell that owned it. An interactive bash then resends SIGHUP to every job it started, running or stopped, before it exits, and each job dies from it unless it ignores SIGHUP — as a command started under `nohup` does — or was removed from the shell's job table with `disown`. A process that is not a job of that shell, such as one inside a tmux session or one started by systemd, never receives it. The trap is "I started it with `&`, so it runs in the background and is safe": a background job is still a job of the ssh shell.

How often that costs a day follows from probability. If connection drops arrive independently at a rate $\lambda$ per hour, a run of $T$ hours survives as a job of the ssh shell with probability $e^{-\lambda T}$ — the chance that a Poisson process has no event in $T$ hours ([[02-foundations/probability|3. Probability §2]]) — and with probability 1 inside tmux or under systemd, where a drop costs only a reconnection. P6's 8-hour recording at $\lambda=0.1$ per hour survives with $e^{-0.8}=0.449$ as a job of the ssh shell: fewer than half of such days are recorded to the end (Worked case, step 6), and the lost recording is found the next morning with nothing in any log to say why — the programs did not crash, they were hung up on.

The mechanism, reproduced on the laptop without a network: an interactive bash on a pseudo-terminal is given two background jobs — one plain, one under `nohup` — and then its terminal is closed the way a dropped ssh connection closes it. What survives:

```text
plain  job: gone
nohup  job: still running
```

> [!note]- Deeper · 더 깊이
> The script, run by hand as `hangup_demo.py` (not in CI, because it starts processes):
>
> ```python
> # not-run: starts an interactive bash on a pseudo-terminal and two sleep processes (run by hand as hangup_demo.py)
> import os, pty, time, subprocess
> pid, fd = pty.fork()
> if pid == 0:
>     os.execvp("bash", ["bash", "--norc", "--noprofile", "-i"])
> def send(s):
>     os.write(fd, s.encode()); time.sleep(0.5)
>     try:
>         os.read(fd, 65536)
>     except OSError:
>         pass
> send("sleep 300 & echo $! > plain.pid\n")
> send("nohup sleep 301 > /dev/null 2>&1 & echo $! > nohup.pid\n")
> time.sleep(0.5)
> os.close(fd)                      # the terminal goes away
> time.sleep(1.5)
> for name in ("plain", "nohup"):
>     p = open(name + ".pid").read().strip()
>     alive = subprocess.run(["kill", "-0", p], capture_output=True).returncode == 0
>     print("%-6s job: %s" % (name, "still running" if alive else "gone"))
>     if alive:
>         subprocess.run(["kill", p])
> ```

`nohup` saves the process but not your view of it: its output goes to a file and there is no terminal to come back to. tmux keeps the terminal. Anything that must run unattended, restart after a crash or start at boot belongs to systemd (§10).

### 9. Devices and stable names: `/dev` and udev

*In one sentence:* the kernel numbers devices in the order it meets them, so give each device a name from what it is — a udev rule — and open that name.

Once the cart has two USB serial boards, the name the controller opens can point at a different board after each reboot — and the controller then reads the wrong bytes without any error. `/dev` holds a **device file** for each device the kernel knows, and a program reaches the hardware by opening that file. In `ls -l`, character devices (`c`) move a stream of bytes — serial ports, the encoder board — and block devices (`b`) hold filesystems — disks. A USB board that speaks serial appears as `/dev/ttyACM0` or `/dev/ttyUSB0`, and the number is an ordinal: the kernel's list of device numbers calls `ttyACM0` the *first* ACM modem and `ttyACM1` the *second*. The number says which board the kernel met first, not which board it is.

Give P6's cart a second USB serial device — say its single-axis IMU of [[04-robotics/sensor-models|3.2 Sensor Models & Noise]] hangs on USB too. Whichever board the kernel meets first after a reboot becomes `ttyACM0`, so a controller configured with `/dev/ttyACM0` opens the encoder on some mornings and the IMU on others. It is the same fault as a relative path (§1): a name that depends on something other than the thing named.

**udev** is the service that acts every time the kernel reports a device: it creates the node's name links and sets the node's group and mode by **rules**. Ubuntu already ships one stable name per USB serial device: a link under `/dev/serial/by-id/`, named from the bus, the identity the device itself reports (udev's `ID_SERIAL` property) and the interface number. For a short name of your own, you write a rule. First read what you can match — the device and every parent device above it, with their attributes — then write one line. On the cart, from the manuals, not run here; the two IDs are placeholders for what `udevadm info` prints for your board:

```bash
udevadm info -a -n /dev/ttyACM0 | less      # attributes of the device and its parents
```

```text
# /etc/udev/rules.d/99-p6-encoder.rules
SUBSYSTEM=="tty", ATTRS{idVendor}=="1a2b", ATTRS{idProduct}=="3c4d", SYMLINK+="p6-encoder", GROUP="dialout", MODE="0660"
```

```bash
sudo udevadm control --reload               # re-read the rules files
sudo udevadm trigger                        # replay device events, so existing devices get the new rules
ls -l /dev/p6-encoder                       # the link, pointing at whichever ttyACM the board got
```

`--reload` alone changes nothing for a device that already exists; the rules apply at the next event, which `trigger` replays and a replug or a reboot also produces. `GROUP` and `MODE` restate Ubuntu's default for `ttyACM` devices (§4), so the rule also records the permission the controller relies on.

> **udev rule, defined.** A **udev rule** is *one line of a rules file that udev evaluates for every device event* — a match and a set of actions, applied each time a device appears, not a command run once. Three conditions define it. Its **match keys**, written `==`, must all hold for the event's device: `SUBSYSTEM`, `KERNEL` for the kernel's name, and `ATTRS{…}`, which searches the device *and its parent devices* for a sysfs attribute (a property the kernel publishes as a file under `/sys`) — a USB board's `idVendor` and `idProduct`, hexadecimal IDs, sit on its USB parent, not on the tty. Its **assignment keys**, `=` and `+=`, then act: `SYMLINK+=` adds a name under `/dev`, `GROUP=` and `MODE=` set the node's permissions. And rules files are **read from four directories** — `/usr/lib/udev/rules.d`, `/usr/local/lib/udev/rules.d`, `/run/udev/rules.d` and `/etc/udev/rules.d` — and applied together in the lexical order of their names, a file in `/etc` taking priority over one of the same name elsewhere; so a local rule is a file in `/etc/udev/rules.d/` whose number places it after the defaults.
>
> $$\text{kernel name}=\texttt{ttyACM}\,k,\ \ k=\text{its rank in detection order};\qquad \text{rule name}=f(\texttt{idVendor},\,\texttt{idProduct},\,\ldots)$$
>
> where $k$ depends on which devices the kernel met before this one, and $f$ only on attributes the board carries, so the rule's name is the same after every reboot and in every USB port, and the kernel's is not.
>
> - **Example**: the rule above. Whichever number the encoder board receives, `/dev/p6-encoder` points at it; the controller's port parameter says `/dev/p6-encoder`, and the node's mode stays `crw-rw----` with group `dialout`.
> - **Non-example**: `KERNEL=="ttyACM0", SYMLINK+="p6-encoder"`. It matches whichever board was met first — after the reboot that swaps the two, `/dev/p6-encoder` names the IMU. A stable name for an unstable fact.
> - **Non-example**: two identical encoder boards on two carts' spares shelf. Their vendor and product IDs are the same, so the rule matches both; the `/dev/serial/by-id/` name, built from each board's own identity, is the one that tells them apart.
> - **Why it matters**: a controller that opens the wrong serial port does not fail — it reads bytes, and misreads them.

### 10. Services and logs: systemd and journalctl

*In one sentence:* a systemd unit file says how to start, restart and stop one program — at boot, without a shell — and `journalctl` reads what it printed.

A stack started by hand from a terminal stops when you log out, stays down after a crash, and is not running when you arrive in the morning. **systemd** is the program that starts Ubuntu's services at boot, supervises them while they run and stops them at shutdown. Each service is described by a **unit file**, and anything that must run on the cart without you — the P6 stack, a nightly copy — should be one. P6's, on the cart, from the manuals, not run here:

```ini
# /etc/systemd/system/p6-stack.service
[Unit]
Description=P6 cart stack: controller, vision node and recorder
Wants=network-online.target
After=network-online.target

[Service]
Type=exec
User=robot
WorkingDirectory=~
ExecStart=/bin/bash -c 'source /opt/ros/jazzy/setup.bash && source /home/robot/p6_ws/install/setup.bash && exec ros2 launch p6_bringup p6.launch.py'
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Its lines answer, one by one, failures of earlier sections. `ExecStart=` runs *no shell*: systemd splits the line into words itself and supports none of the shell's pipes, redirections, `&` or builtins, so there is no `source` unless the line starts `bash -c` explicitly; and no `~/.bashrc` is read either, so the setup files are sourced right there (§5); `exec` in front of `ros2 launch` makes it replace that shell instead of running as its child, so the launch process is the service's main process. `User=robot` runs the stack as `robot`, with the supplementary groups the group database gives that account — `dialout` included, so the encoder opens (§4). `WorkingDirectory=~` replaces systemd's default of `/`, under which every relative path of §1 would point at the root. `WantedBy=multi-user.target` is what `systemctl enable` turns into a start at every boot (a *target* is a named stage of the boot, and `multi-user.target` is the normal system without a desktop), and `Wants=`/`After=network-online.target` hold the start until the network is configured, which a stack talking to the workstation needs. The daily commands, from the manuals, not run here:

```bash
sudo systemctl daemon-reload                      # re-read unit files after an edit
sudo systemctl enable --now p6-stack.service      # start at every boot, and start now
systemctl status p6-stack.service                 # state, main PID and the latest log lines
journalctl -u p6-stack.service -b -f              # this boot's log of the unit, following new lines
journalctl -u p6-stack.service -b -1 -p warning   # the previous boot, warnings and worse
sudo systemctl reset-failed p6-stack.service      # clear the failed state and the start counter
```

A service's standard output and standard error go to the **journal**, systemd's log, so the node's `[WARN]` lines on standard error (§6) are there without redirection; `journalctl -u` reads one unit's share of it, `-b` limits it to this boot, `-b -1` asks for the boot before, and `-p warning` shows that level and everything more severe.

> **systemd service, defined.** A **service** is *a unit that systemd starts, supervises and stops according to a unit file* — a declaration of how to run one program, not a script that runs it. Four conditions define its behaviour. **What runs**: `ExecStart=` names a program — by absolute path, to be safe — and runs it without a shell, as `User=` with that user's groups, in `WorkingDirectory=`, default `/`. **When**: `WantedBy=multi-user.target` and `systemctl enable` start it at every boot, after whatever `After=` names. **Restart**: with `Restart=on-failure` an unclean exit or an unclean signal starts it again after `RestartSec=` — 100 ms unless set — while an exit by SIGTERM, SIGINT, SIGHUP or SIGPIPE counts as clean; and a unit started more than `StartLimitBurst=` times (5) within `StartLimitIntervalSec=` (10 s) is not started again. **Stop**: `systemctl stop` sends SIGTERM to every process of the unit, then waits up to `TimeoutStopSec=` — 90 s unless set — and sends SIGKILL to whatever is left.
>
> $$\text{given up}\iff B\,c<I,\qquad c=t_{\text{run}}+\texttt{RestartSec}$$
>
> where $t_{\text{run}}$ is how long each attempt lives before it fails, $c$ the time from one start to the next, $B=5$ and $I=10$ s, so the sixth start falls inside the interval — and is refused — exactly when five cycles are shorter than it.
>
> - **Example**: at boot the stack starts before the encoder board has appeared, and it exits with an error 0.4 s after each start (its launch file ends the launch when the controller cannot open its port). With the default 100 ms, $c=0.5$ s and $Bc=2.5$ s $<10$ s: the sixth start, 2.5 s after the first, is refused, and the cart sits idle although the board arrived a second later. With `RestartSec=3`, as in the unit above, $c=3.4$ s and $Bc=17$ s $>10$ s: systemd keeps retrying until the board is there.
> - **Non-example**: `ExecStart=source /opt/ros/jazzy/setup.bash && ros2 launch p6_bringup p6.launch.py`. `source` is a builtin of the shell, not a program, and `&&` is shell syntax; without `bash -c` there is no shell to understand either, and the unit fails at its first start.
> - **Why it matters**: a robot that must be working when you arrive is a start order, a restart policy and a stop timeout — three numbers in a file you can read.

### 11. Time and the network

*In one sentence:* check addresses, round trips and listening ports with `ip`, `ping` and `ss`, and never compare timestamps from two machines whose clocks nobody synchronised.

Once the stack spans two machines, three new things can fail without an error message: the machines cannot reach each other, a port is closed, or their clocks disagree — and the last one silently corrupts every latency you measure across them.

**Addresses.** On the direct link the workstation is `192.168.10.1` and the cart `192.168.10.2`, both with the suffix `/24`: the first 24 bits, `192.168.10`, name the network, so the two machines are on one link and reach each other directly. These are private addresses, from the `192.168.0.0/16` block that RFC 1918 reserves for networks inside an organisation. On the cart, `ip -br addr` lists every interface with its addresses (from the manual, not run here), and a fixed address is written into a netplan file under `/etc/netplan/` and applied with `sudo netplan apply`. `ping` measures the round trip: it sends ICMP echo requests (ICMP is the network's own control-message protocol) and prints each reply's time. On the laptop, to its own loopback address (output trimmed to the first reply and the summary):

```bash
ping -c 3 127.0.0.1
```

```text
PING 127.0.0.1 (127.0.0.1): 56 data bytes
64 bytes from 127.0.0.1: icmp_seq=0 ttl=64 time=0.069 ms
--- 127.0.0.1 ping statistics ---
3 packets transmitted, 3 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 0.069/0.088/0.100/0.014 ms
```

From the workstation, `ping -c 3 192.168.10.2` is the first test of the link, before anything in ROS 2 is blamed.

**Ports.** A program that serves the network listens on a numbered port: the ssh server on 22 by default. `ss -tlnp` on the cart lists the listening TCP sockets with numeric ports and the process holding each (from the manual, not run here). ROS 2's middleware chooses its own UDP ports from `ROS_DOMAIN_ID`, which must match on every machine of one ROS 2 system; it is introduced in [[04-robotics/ros2/what-ros2-is|25.1 §5]], and its port arithmetic and multicast test are in [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]].

**Clocks.** Every computer keeps its own clock, and no two run at exactly the same rate, so two clocks set equal drift apart unless something steers them. Ubuntu 24.04 does the steering with systemd-timesyncd by default; Ubuntu's own documentation says chrony became the default from 25.10. `timedatectl status` says whether the clock is synchronised and whether the time service is active; `timedatectl timesync-status` shows timesyncd's server and current offset; with chrony, `chronyc tracking` reports the system clock's offset from chrony's estimate of true time (all from the manuals, not run here).

> **Clock offset, defined.** The **clock offset** $\theta$ between two machines is *the difference between their clocks' readings at the same instant* — a property of a pair of clocks at a moment, not of either machine, and not a constant. Three conditions define what it does. Each machine **keeps its own clock**, and a timestamp is a reading of the clock of the machine that wrote it. A time difference computed from **two stamps of different clocks** contains $\theta$, one for one. And without synchronisation $\theta$ **grows**, at the rate $\delta$ by which one clock runs faster than the other, in seconds per second.
>
> $$\hat L=t^{B}_{\text{recv}}-t^{A}_{\text{stamp}}=L+\theta(t),\qquad \theta(t)=\theta_0+\delta\,t$$
>
> where $L$ is the true latency, $t^{A}_{\text{stamp}}$ the send time read on A's clock, $t^{B}_{\text{recv}}$ the receive time read on B's clock and $\hat L$ what B computes, so every latency measured across two machines is wrong by exactly the offset at that moment.
>
> - **Example**: the vision node moves to the workstation, where the GPU is; the controller on the cart computes each goal's age. Clocks set equal at 08:00 and never synchronised, with $\delta=20$ ppm — a course number, 20 µs per second — are $\theta=20\times10^{-6}\times3600=72$ ms apart at 09:00: a goal 10 ms old reads as 82 ms and "breaks" the 70 ms budget, or, with the sign the other way, a goal 100 ms late reads as 28 ms and passes. The offset crosses the whole budget after $0.070/(20\times10^{-6})=3{,}500$ s, under an hour.
> - **Non-example**: two nodes on the cart itself. Both stamps come from one clock, so $\theta=0$ whatever that clock's error against the rest of the world; synchronising a single machine changes none of its internal latencies.
> - **Why it matters**: P6's 70 ms budget ([[04-robotics/robot-systems-deployment|10. Robot Systems §3]]) can be checked across two machines only if $|\theta|$ is small against it, and kept small — which is why [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]] asks for chrony on both machines against one source, verified rather than assumed. How close NTP and PTP get is this track's networking page ([[02-foundations/tools/computer-networks|12.5 §10]]).

### Worked case · 대상으로 한 번 끝까지

One shift of P6's logging, 08:00 to 16:00, priced from the frozen numbers — each step a rule, its substitution and a number with its unit. It uses §1, §4, §6 and §8.

**Step 1 — bytes per second into the bag.** A bag's payload grows as each recorded topic's rate times its message size ([[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), and the three topics are recorded side by side, so the recorder writes

$$r=f_c\,s+f_v\,s+f_v\,s_{\text{img}}=200\cdot64+50\cdot64+50\cdot40{,}000=12{,}800+3{,}200+2{,}000{,}000=2{,}016{,}000\ \text{B/s}$$

because each term is one topic's messages per second times its bytes per message. That is 7.2576 GB per hour, and the camera is 99.21% of it: the 200 Hz control topic that P6's whole budget is about costs 46 MB an hour. What the page counts is payload; the bag file adds a little per message on top.

**Step 2 — when the disk fills.** The disk holds $F$ bytes and fills at $r$, so

$$t_{\text{full}}=\frac{F}{r}=\frac{120\times10^{9}\ \text{B}}{2{,}016{,}000\ \text{B/s}}=59{,}523.8\ \text{s}=16.53\ \text{h}$$

since nothing else competes for the space. The shift itself uses $rT=58.06$ GB, 48.4% of it: two shifts fit, with 3.9 GB to spare, and a third does not — so the bags must leave the cart at least every second day. A recorder started at 08:00 and never stopped fills the disk 16 h 32 min later, at 00:32, and from then on it — and anything else writing to that disk — fails. `df -h /home` each morning is the check (§1); in its powers of 1024 the 120 GB read as about 111.8.

**Step 3 — the copy to the workstation.** A byte is 8 bits and the copy achieves the fraction $\eta$ of the link, so

$$t_{\text{copy}}=\frac{rT}{\eta R/8}=\frac{58.06\times10^{9}\ \text{B}}{0.8\times10^{9}/8\ \text{B/s}}=580.6\ \text{s}=9\ \text{min}\ 41\ \text{s}$$

for the whole shift. With `rsync -a` (§8), an interrupted copy costs at most the file in flight: the recorder splits at `-d 1800`, so each file holds $r\cdot1800=3.63$ GB, and a re-run re-sends at most one of them, 36.3 s, because rsync removes a partial file and skips every file already complete.

**Step 4 — the serial device's mode.** `crw-rw---- root dialout` is, class by class, $d_u=4+2+0=6$, $d_g=4+2+0=6$, $d_o=0$, so

$$m=(660)_8=6\cdot64+6\cdot8+0=432$$

because each octal digit is one class's three bits. The controller runs as `robot`, which is not the owner `root`, so the group class decides: in `dialout`, digit 6 — read and write; not in it, the others' digit 0 — `Permission denied`. The fix is `usermod -aG dialout robot` and a new login, not a new mode (§4).

**Step 5 — the nightly check.** `grep ERROR p6_day2.log | wc -l` on a day whose log was never written gives statuses $(s_1,s_2)=(2,0)$: `grep` found no file, `wc` counted nothing. Without `pipefail` the pipeline reports $s_2=0$ and the check prints "0 errors"; with it, $s_1=2$ and `set -e` stops the script (§6, panel C). On the laptop, `p6_check_log.sh` exits 1 on the missing file and 0 on a clean log.

**Step 6 — will the recording survive the shift.** Connection drops arrive at $\lambda=0.1$ per hour, independently, so for $T=8$ h

$$P(\text{no drop})=e^{-\lambda T}=e^{-0.8}=0.4493$$

since the chance that a Poisson process has no event in $T$ hours is the tail of the exponential waiting time ([[02-foundations/probability|3. Probability §2]]). A recorder started as a job of a plain ssh shell records the whole shift on 45% of days; inside tmux, or as the systemd service of §10, a drop costs a reconnection and nothing else (§8).

The whole case in a few lines of Python (run in CI; the numbers above are its output):

```python
# One day of P6's logging, from this page's course numbers (Worked case, steps 1-6).
import math

f_c, f_v, s, s_img = 200, 50, 64, 40_000        # Hz, Hz, bytes per /cmd or /goal, bytes per frame
F, R, eta, T, lam = 120e9, 1e9, 0.8, 8, 0.1     # free bytes, link bit/s, copy fraction, shift h, drops/h

r = f_c * s + f_v * s + f_v * s_img             # bytes per second into the bag
t_full = F / r                                  # seconds from 08:00 until the disk is full
day = r * T * 3600                              # bytes recorded in one shift
t_copy = day / (eta * R / 8)                    # seconds to copy the shift to the workstation
split = r * 1800                                # bytes in one 30-minute bag file

print(f"rate       {r:,} B/s = {r * 3600 / 1e9:.4f} GB/h; camera {100 * f_v * s_img / r:.2f}% of it")
print(f"disk full  {t_full:,.1f} s = {t_full / 3600:.4f} h after 08:00")
print(f"shift      {day / 1e9:.4f} GB = {100 * day / F:.1f}% of the free space")
print(f"copy       {t_copy:.1f} s = {t_copy / 60:.2f} min; one split file {split / 1e9:.3f} GB = {split / (eta * R / 8):.1f} s")
print(f"mode 660   = {0o660} = 6*64 + 6*8 + 0 = {6 * 64 + 6 * 8 + 0}")
print(f"P(no ssh drop in {T} h) = exp(-{lam * T:.1f}) = {math.exp(-lam * T):.4f}")
```

```text
rate       2,016,000 B/s = 7.2576 GB/h; camera 99.21% of it
disk full  59,523.8 s = 16.5344 h after 08:00
shift      58.0608 GB = 48.4% of the free space
copy       580.6 s = 9.68 min; one split file 3.629 GB = 36.3 s
mode 660   = 432 = 6*64 + 6*8 + 0 = 432
P(no ssh drop in 8 h) = exp(-0.8) = 0.4493
```

### 12. What this page does not cover

This page stops where a researcher's daily Linux stops. ROS 2 itself — what the setup file exports, workspaces, overlays, bags and launch files — is the ROS 2 track, starting at [[04-robotics/ros2/what-ros2-is|25.1 §7]]; virtual environments, `pip` and pinned requirements are this track's Python page ([[02-foundations/tools/python-research-code|12.3]]); Git is [[02-foundations/tools/git-research-code|12.2]]; configuration and data formats, YAML and MCAP among them, are [[02-foundations/tools/config-data-formats|12.4]]; TCP, UDP, DDS on the wire, PTP and site networks are [[02-foundations/tools/computer-networks|12.5]]; compiling C++ is [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]]; threads inside one process, and the races they allow, are [[02-foundations/tools/concurrency|12.8]]; running a job on a shared GPU cluster is [[02-foundations/tools/gpu-clusters|12.7]]; and GPU drivers and CUDA are [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing for Robot Learning]]. Not covered anywhere in the wiki: administering a multi-user server or a fleet (user management, backups, firewalls, `sudoers` policy), shell programming beyond short scripts (arrays, functions, `trap`), editors, the kernel and its drivers, and a real-time kernel, whose limits [[04-robotics/ros2/from-simulation-to-hardware|25.11 §6]] states. Each tool's manual page (§1) is the next step.

### After reading

- [ ] Name a file by absolute and relative path, and say which working directory a terminal, a script and a systemd service each start in.
- [ ] Predict the arguments a program receives from a line with variables, quotes and a glob, and guard a variable that must not be empty.
- [ ] Read an exit status as success, a program's own failure, "not found", "not executable" or a signal, and say what a node should do on SIGINT and SIGTERM.
- [ ] Read a mode in letters and octal, say which class applies to a process, and fix *Permission denied* on a serial device with a group, not with `chmod`.
- [ ] Say which processes an environment variable reaches, why a terminal needs `source`, and why `ssh p6 'ros2 …'`, `sudo ros2 …` and a service do not see it.
- [ ] Redirect standard output and standard error, filter a node's log with a pipeline, and write a script with `set -euo pipefail` that fails for the right reasons.
- [ ] Choose apt, pip in a virtual environment, or a container for a given piece of software, and say why `sudo pip install` is refused on Ubuntu 24.04.
- [ ] Log in with a key, copy a day's bags with `rsync`, and keep a run alive in tmux, and say who receives SIGHUP when a connection drops.
- [ ] Give a USB device a stable name with a udev rule, and write, enable and read the log of a systemd service.
- [ ] Price a day of logging in bytes, disk time and copy time, and a clock offset against a latency budget.

### Self-check

1. A unit file for a nightly copy has `ExecStart=/usr/bin/rsync -a bags/ ws:p6_bags/` and no `WorkingDirectory=`. Which directory does `bags/` name, and what are two fixes?
2. `bagdir` is empty. What do `rm -rf $bagdir/*` and `rm -rf "${bagdir:?}"/*` each do, and why does `set -u` not help?
3. A launch log says `process has died [pid 5120, exit code -9, …]`, and a script's `$?` after the same kind of death is 137. What happened, and who is a likely sender?
4. `ls -l /dev/ttyACM0` shows `crw-rw---- 1 root dialout`, and the controller logs *Permission denied*. Which class applied to it, what is the fix, and why does the fix not take effect in the terminal you typed it in?
5. `ssh p6` followed by `ros2 topic list` works; `ssh p6 'ros2 topic list'` says `ros2: command not found`. Why, and what is the one-line fix?
6. `ros2 run p6_control controller | grep WARN` prints every log line, warnings and all. Why, and what do you type instead?
7. You run `sudo systemctl stop p6-stack.service`. What is sent, to which processes, and what happens if the recorder has not exited 90 s later?

> [!tip]- Answers
> 1. `/bags/`: a system service's working directory is `/` unless `WorkingDirectory=` sets it, and a relative path is read from there. Write the absolute path, `/home/robot/bags/`, or add `WorkingDirectory=~` together with `User=robot`.
> 2. The first expands to `rm -rf /*` — every entry at the root. The second stops with an error before `rm` runs, because `:?` refuses a variable that is empty or unset. `set -u` objects only to a variable that was never set; an empty one passes it.
> 3. The process was killed by SIGKILL, signal 9: Python's subprocess machinery reports it as −9, bash as $128+9=137. SIGKILL cannot be caught, so the program had no chance to clean up. A likely sender is `ros2 launch` itself, 10 s into a shutdown the node did not finish, or systemd after its 90 s stop timeout.
> 4. The owner is `root` and the controller runs as `robot`, so the owner class does not apply; `robot` is not in `dialout`, so the others class applies, digit 0, no access. The fix is `sudo usermod -aG dialout robot` and a new login. A process's groups are fixed when it starts and inherited by everything it starts, so the terminal you typed `usermod` in, and any node started from it, keeps the old list; a new ssh session reads the new one.
> 5. `ssh p6 'command'` runs a non-interactive bash, and Ubuntu's default `~/.bashrc` returns at its first lines from any non-interactive shell, so the `source /opt/ros/jazzy/setup.bash` line at its end never runs. Source it in the command: `ssh p6 'source /opt/ros/jazzy/setup.bash && ros2 topic list'`.
> 6. ROS 2 writes log lines to standard error and a pipe carries standard output only, so the lines bypass `grep` and reach the terminal unfiltered. Type `ros2 run p6_control controller 2>&1 | grep WARN` (or `|&` in bash 4 and later, as on the cart).
> 7. SIGTERM, followed by SIGCONT, to every process of the unit — the launch process and each node it started. Nodes that handle SIGTERM shut down; whatever is still running after `TimeoutStopSec=`, 90 s by default, receives SIGKILL, and a recorder killed that way leaves an unfinished file.

### Problem set · 과제

Tier B. Using only this page, its prerequisites and **P6** from [[02-foundations/lab-plants|0.6 Lab Plants]]. The object is the same computer; every problem changes a knob — the frame size, the disk, the link, a group list, a restart delay, a clock's rate — so no number of the page can be copied.

1. **Draw.** The picture for a changed day. The camera stream is compressed less, $s_{\text{img}}=60{,}000$ bytes; the cart has $F=200$ GB free at 08:00; and the copy goes over the site's Wi-Fi at an effective 20 MB/s instead of the Ethernet. Redraw panel A's link and recorder labels and panel B to scale — the rate, the shift's bytes at 16:00 and the time the disk fills — and write both copy times on it, over Wi-Fi and over the page's Ethernet. Does one shift still fit, and does its copy fit in a 45-minute lunch break?
2. **Derive.** (a) A second board appears as `/dev/ttyUSB0` with `crw-rw---- root dialout`, and `robot`'s groups are `robot` and `video`. Which class applies to the controller, and what does its `open()` for reading and writing return? Write in letters, octal and decimal the mode that lets the owner read and write, the group only read and others nothing, and say why `sudo chmod` is not a lasting fix. (b) Give the status each pipeline reports without and with `pipefail`: (i) `grep -c ERROR p6_day1.log | sort` on the page's day-1 log; (ii) `grep ERROR p6_clean.log | wc -l` on a log without errors; (iii) `grep ERROR p6_day2.log | grep -c controller` when `p6_day2.log` does not exist. Which of the three does `pipefail` get wrong, and why? (c) The workstation is moved onto the site's Wi-Fi, $\lambda=0.25$ drops per hour, and the recording runs 12 h as a job of the ssh shell. What is the chance it survives, and the mean time to the first drop? (d) The stack now exits 1.2 s after each start while the board is missing. With the default `RestartSec=`, when does systemd give up? What is the smallest `RestartSec=` for which it never does? (e) Two machines' clocks are set equal and never synchronised, with $\delta=50$ ppm. When does their offset exceed P6's 70 ms budget, and what age does the cart compute, 2 h later, for a goal that is truly 30 ms old?
3. **Interpret.** A lab-mate's start-up script, run by hand after each reboot from an ssh session on the workstation (`ssh robot@192.168.10.2`, then `./start_p6.sh`). It is for reading, not running, and was not run here. Name every mistake, the symptom it produces on the cart and the fix, citing the section that explains it.

```text
#!/bin/bash
# start_p6.sh: bring up P6 for the day and write a report at the end
sudo pip install pyserial
bash ~/p6_ws/install/setup.bash
ros2 bag record --topics /cmd /goal /camera/image/compressed -o ~/bags/day1 &
ros2 launch p6_bringup p6.launch.py encoder_port:=/dev/ttyACM0 &
sleep 28800
grep ERROR ~/p6_logs/day1.log | wc -l > ~/p6_report.txt
```

> [!note]- How to draw it · 그리는 법
> - **Panel A is the machine, not the network.** Draw the cart as one box holding systemd, the three programs and the two things they touch — the device file with its mode, owner and group, and the disk with its free space — and the workstation outside it, joined by one link labelled with its nominal rate and the rate a copy achieves.
> - **Label the device by both names**, the stable one the controller opens and the kernel's one it points at, and write the mode in letters and octal. The permission is part of the picture because it is the first thing that fails.
> - **Panel B is a straight line drawn to scale.** Put time of day on the horizontal axis from the start of recording to the same time next day, at a fixed number of pixels per hour, and gigabytes used on the vertical axis up to the free space. The line's slope is $r$ in GB/h; it meets the top at $F/r$, which is where the disk is full.
> - **Mark the end of the shift on the line** with its gigabytes, and write the copy time beside it — the one derived number the day owes before anyone goes home. With a different link, only that label changes.
> - **Draw the line flat after the disk fills, dashed**, and label the time of day. A recorder left running is the default outcome, not an accident.
> - **Panel C is a pipeline with a status under every stage** and the two readings of `$?` beneath it. In this problem set it does not change; redraw it only if you change the command.

> [!tip]- Solutions
> 1. $r=12{,}800+3{,}200+50\cdot60{,}000=3{,}016{,}000$ B/s $=10.8576$ GB/h, the camera 99.47% of it. The shift writes $10.8576\times8=86.86$ GB, 43.4% of 200 GB, so one shift fits easily; two fit too ($173.7$ GB) and a third does not. The disk fills after $200\times10^9/3{,}016{,}000=66{,}313$ s $=18.42$ h, at 02:25 the next morning. The copy takes $86.86\times10^9/(20\times10^6)=4{,}343$ s $=72.4$ min over Wi-Fi — longer than lunch — and $868.6$ s $=14.5$ min over the Ethernet at 100 MB/s. On a 20 px per hour, 1 px per GB drawing, the line rises 10.86 px per hour and reaches the 200 GB level at $x=18.42\times20=368$ px from the start.
> 2. (a) The owner is `root`, not `robot`; the group `dialout` is not among `robot` and `video`; so the others class applies, digit 0, and `open()` fails with *Permission denied*. The mode is `rw-r-----`, $(640)_8=6\cdot64+4\cdot8+0=416$. `chmod` changes a node that udev creates afresh, with its rules' mode, at the next boot or replug; the lasting fix is `robot` in `dialout`, or a rule's `GROUP=`/`MODE=`. (b) (i) $(0,0)$: 0 and 0 — `grep` counted 3. (ii) $(1,0)$: 0 without, 1 with `pipefail` — a false alarm, since `grep`'s 1 means only "no line selected". (iii) $(2,1)$: the second `grep` read nothing and selected nothing, so it exits 1; the pipeline reports 1 without `pipefail` (the last command) and 1 with it (the rightmost failure), and the missing file's 2 is hidden either way. `pipefail` reports *a* failure, not *the* failure; run on the laptop, `PIPESTATUS` printed `0 0`, `1 0` and `2 1`. (c) $e^{-0.25\times12}=e^{-3}=0.0498$: one such run in twenty survives, and the first drop comes after $1/\lambda=4$ h on average. (d) $c=1.2+0.1=1.3$ s and $5c=6.5$ s $<10$ s: the sixth start, 6.5 s after the first, is refused. It never gives up when $5c\ge10$ s, that is $c\ge2$ s and `RestartSec` $\ge0.8$ s; take 1 s or more to stay clear of the boundary. (e) $0.070/(50\times10^{-6})=1{,}400$ s $=23.3$ min. After 2 h, $\theta=50\times10^{-6}\times7{,}200=0.36$ s, so the goal reads $30+360=390$ ms old — or, with the opposite sign, $30-360=-330$ ms: a goal from the future, an age that no pair of synchronised clocks can produce.
> 3. *Line 3*, `sudo pip install pyserial`: Ubuntu 24.04 marks its Python as externally managed, so pip refuses with an error; forced with `--break-system-packages` it would put the package where apt's and ROS 2's Python import from. Fix: declare the dependency for rosdep and install it with apt (§7), or use a virtual environment for non-ROS code ([[02-foundations/tools/python-research-code|12.3]]). *Line 4*, `bash …/setup.bash`: the setup runs in a child shell that exits, so the workspace is never sourced — line 6 cannot find `p6_bringup`, and if the ssh shell never sourced ROS 2 either, lines 5 and 6 both print `ros2: command not found`. Fix: `source` (§5). *Lines 5–6*, `&` jobs of a script run from the ssh session: when the workstation sleeps or its connection drops, the whole script is hung up and the recording ends mid-shift, with no error anywhere (§8); and the jobs ignore SIGINT, so stopping them with `kill -INT` does nothing (§3). Fix: a systemd service (§10), or at least tmux. *Line 6*, `encoder_port:=/dev/ttyACM0`: a kernel name, so on the morning the IMU is met first the controller opens the IMU. Fix: a udev rule and `/dev/p6-encoder` (§9). *Line 8*: no `set -euo pipefail`, and the nodes log to standard error and to ROS 2's own log files, not to `~/p6_logs/day1.log`; `grep` exits 2, `wc` writes 0, and the report says 0 errors every day. Fix: `set -euo pipefail`, capture the stack's standard error or read the journal of the service, and count with the `p6_check_log.sh` pattern (§6). Also missing: nothing stops the recorder at the end, so the disk fills at 00:32 (Worked case, step 2).

### Sources

- GNU Bash Reference Manual ([gnu.org](https://www.gnu.org/software/bash/manual/html_node/index.html)) — expansions and quoting, `${var:?}`, exit statuses (126, 127, $128+n$), pipelines and `pipefail`, `set -e`/`-u`, signals in scripts, SIGHUP resent to jobs.
- bash(1) ([man7.org](https://man7.org/linux/man-pages/man1/bash.1.html)), Ubuntu 24.04's bash 5.2.21 ([packages.ubuntu.com](https://packages.ubuntu.com/noble/bash)) and its default `~/.bashrc` ([skel.bashrc](https://git.launchpad.net/ubuntu/+source/bash/tree/debian/skel.bashrc?h=ubuntu/noble)) — start-up files, including for sshd; the early return from non-interactive shells.
- POSIX Shell Command Language ([pubs.opengroup.org](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html)) and the [jobs](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/jobs.html), [fg](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/fg.html), [bg](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/bg.html) and [ls](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/ls.html) utilities — redirection order, `exec`, `export`, job control, file-type letters.
- GNU Coreutils, [Mode Structure](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html) — read, write and execute on files and directories.
- Linux man pages ([man7.org](https://man7.org/linux/man-pages/)) — signal(7), termios(3), credentials(7), initgroups(3), path_resolution(7), umask(2), hier(7), man-pages(7), usermod(8), proc_pid_comm(5), ps(1), pgrep(1), kill(1), nohup(1), chmod(1), stat(1), df(1), du(1), grep(1), sort(1), uniq(1), wc(1), stdin(3), ip(8), ss(8), ping(8), timedatectl(1): the command and kernel facts of §1–§6 and §11.
- systemd man pages ([man7.org](https://man7.org/linux/man-pages/)) — systemd.service(5), systemd.unit(5), systemd.exec(5), systemd.kill(5), systemd-system.conf(5), systemd.special(7), systemctl(1), journalctl(1), journald.conf(5), systemd-journald.service(8), udev(7), udevadm(8): §9's rules and §10's start, restart, stop and journal.
- systemd source ([github.com/systemd/systemd](https://github.com/systemd/systemd)) — [50-udev-default.rules.in](https://github.com/systemd/systemd/blob/main/rules.d/50-udev-default.rules.in) (`dialout` for serial devices), [60-serial.rules](https://github.com/systemd/systemd/blob/v255/rules.d/60-serial.rules) (`/dev/serial/by-id`), [udev-node.c](https://github.com/systemd/systemd/blob/v255/src/udev/udev-node.c) (0660 when a group is set); Ubuntu 24.04 ships systemd 255.4 ([packages.ubuntu.com](https://packages.ubuntu.com/noble/systemd)).
- Linux kernel documentation — [devices.txt](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/devices.txt) (`ttyACM0` the first ACM modem) and [sysfs-bus-usb](https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-bus-usb) (`idVendor`, `idProduct`).
- OpenSSH manuals ([man.openbsd.org](https://man.openbsd.org/)) — ssh(1) `-G`, ssh_config(5) `ServerAlive*`, sshd_config(5) `StrictModes`, scp(1); ssh-copy-id(1) and [session.c](https://github.com/openssh/openssh-portable/blob/master/session.c) (groups read at login).
- tmux(1) ([man.openbsd.org](https://man.openbsd.org/tmux.1)) — sessions that survive an ssh timeout; `new -s`, `attach -t`, `C-b d`.
- rsync(1) ([download.samba.org](https://download.samba.org/pub/rsync/rsync.1)) — the trailing slash, the quick check, partial files removed.
- sudoers(5) ([sudo.ws](https://www.sudo.ws/docs/man/sudoers.man/)) — `env_reset`, `secure_path`.
- apt(8) ([manpages.debian.org](https://manpages.debian.org/bookworm/apt/apt.8.en.html)) — `apt-get` in scripts; PEP 668 ([peps.python.org](https://peps.python.org/pep-0668/)) and Ubuntu's [libpython3.12-stdlib file list](https://packages.ubuntu.com/noble/amd64/libpython3.12-stdlib/filelist) — the `EXTERNALLY-MANAGED` marker; Docker run reference ([docs.docker.com](https://docs.docker.com/reference/cli/docker/container/run/)) — `--device`.
- Python documentation — [subprocess](https://docs.python.org/3/library/subprocess.html) and [asyncio subprocesses](https://docs.python.org/3/library/asyncio-subprocess.html): return code $-N$ for death by signal $N$.
- ROS 2 documentation, jazzy ([github.com/ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — configuring the environment, installation on Ubuntu, console logging on standard error and its format, installing Python packages.
- ROS 2 source, jazzy — [rclcpp utilities.hpp](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/utilities.hpp) and [rclpy `__init__.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/__init__.py) (SIGINT and SIGTERM handlers), [launch execute_local.py](https://github.com/ros2/launch/blob/jazzy/launch/launch/actions/execute_local.py) and [osrf_pycommon](https://github.com/osrf/osrf_pycommon) (the 5 s + 5 s shutdown; "process has died"), [rosbag2 README](https://github.com/ros2/rosbag2/blob/jazzy/README.md) (`--topics`, `-d`, MCAP).
- Ubuntu Server, [About time synchronisation](https://ubuntu.com/server/docs/explanation/networking/about-time-synchronisation/) — timesyncd, chrony from 25.10; [chronyc(1)](https://chrony-project.org/doc/4.6/chronyc.html) — `tracking`; [Netplan](https://netplan.readthedocs.io/en/stable/using-static-ip-addresses/) — static addresses; RFC 1918 ([rfc-editor.org](https://www.rfc-editor.org/rfc/rfc1918.html)) — private addresses.

## 한국어

*[[02-foundations/lab-plants|0.6 Lab Plants]] 위에 선다. 그 페이지의 **P6**은 200 Hz 제어기, 50 Hz 비전 노드, 카메라에서 힘까지 70 ms의 예산을 가진 카트다. 이 페이지는 그것을 돌리는 컴퓨터 — 카트에 실린 Ubuntu 기계로, 워크스테이션에서 이더넷으로 접속한다 — 와, 그 컴퓨터에서 프로그램을 띄우고, 지켜보고, 고치고, 데이터를 복사해 오려고 입력하는 셸을 다룬다. ROS 2 트랙([[04-robotics/ros2/index|25. ROS 2]])은 이 모두를 안다고 가정하고 하나도 가르치지 않는다.*

> [!note] 왜 배우는가 · Why this matters
> 이 페이지는 [[07-research-program/index|연구 프로그램 §5]]의 물리 AI 스택 전체 아래의 바닥이다([[physical-ai-map|피지컬 AI 지도]]에 그 자리가 표시되어 있다). 인식부터 작업 완료까지 모든 층이 리눅스 로봇 컴퓨터 위의 프로세스로 돌고, 그 절의 예 "저 패널을 프레임에 설치해"에서 이 페이지는 부재를 옮기고 접촉을 감지하는 제어기가 돌고, 멈출 수 있고, 기록되게 지킨다. 이것이 없으면 시행하는 하루가 어느 로그도 설명하지 못하는 식으로 날아간다 — 끊긴 ssh 세션과 함께 죽은 녹화, 재부팅 뒤 엔코더 대신 IMU를 연 제어기, 아무것도 읽지 못해 "오류 0건"이라고 보고한 야간 점검 — 그리고 [[05-construction-robotics/imitating-contact|10. 접촉 모방]] 같은 정책이 배우는 시연이 바로 그런 녹화다. ROS 2 만드는 트랙은 [[04-robotics/ros2/what-ros2-is|25.1 §7]]부터 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]까지 이 페이지에 기대고, 이 페이지는 [[07-research-program/index|학위논문 경로(연구 프로그램 §8)]]의 일곱 블록 밖에 있으므로 처음 필요해질 때 — 로봇 컴퓨터에 처음 로그인하기 전, 늦어도 블록 7에 앞서 장비를 위해 만드는 트랙을 시작할 때 — 읽는다. 다 읽으면 로봇의 하루치 녹화를 잃지 않고 돌리고, 지켜보고, 멈추고, 복사할 수 있고, 그 하루에 바이트, 시간, 시계 오프셋으로 값을 매길 수 있다.

> [!note] 처음이라면 · First pass
> 75분 안팎의 두 회차로 읽는다. **1회차:** 이 페이지의 대상과 그림, 그다음 1–3절 — 파일에 이름을 붙이는 법, 무엇이든 실행되기 전에 셸이 한 줄에 하는 일, 프로그램이 시작하고 멈추고 어떻게 끝났는지 알리는 법. 스스로 점검 2와 3으로 마친다. **2회차:** 4–6절 — 권한, 환경, 파이프와 스크립트 — 그다음 계산기를 들고 계산 절의 1–5단계. 스스로 점검 4, 5, 6으로 마친다. 그 뒤로는 ssh로 로봇에서 일하기 전에 8절(과 계산 절의 6단계)을, 로봇 컴퓨터 자체를 설정하는 날에 7절과 9–11절을 읽고, 과제는 맨 마지막에 푼다. 해석 문항이 모든 절을 쓰기 때문이다.

### 이 페이지의 대상 · Running object

[[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**을 그 컴퓨터 쪽에서 본다. 제어기는 200 Hz로 엔코더를 샘플하고 모터를 명령하며 `/cmd`를 발행한다. 비전 노드는 같은 속도로 도는 카메라로부터 50 Hz로 `/goal`에 목표를 발행한다. 녹화기는 두 토픽과 압축된 카메라 스트림을 bag에 쓴다. bag은 녹화된 메시지의 디렉터리로, [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]이 정의한다. 셋은 모두 카트에 실린 Ubuntu 24.04 컴퓨터 한 대에서 돌고, 이 페이지는 그것을 `p6-cart`라 부른다. 워크스테이션에서 이더넷 케이블 한 가닥으로 직접 접속한다. 카탈로그가 고정하는 것은 두 속도와 예산이다. 표의 나머지는 모두 이 페이지가 스스로 여기서 고정하는 값이고, 하나하나가 산수가 깔끔하도록 고른 교과용 숫자다. 어떤 기계를 잰 값도, 어떤 제품의 사양도 아니다.

| 기호 | 값 | 여기서 무엇인가 |
|---|---:|---|
| $f_c$, $f_v$ | 200 Hz, 50 Hz | 제어기와 비전의 속도(카탈로그) |
| $s$ | 64바이트 | `/cmd`나 `/goal` 메시지 하나의 페이로드. [[04-robotics/ros2/debugging-data-reproducibility\|25.10]]도 쓰는 설명용 크기 |
| $s_{\text{img}}$ | 40,000바이트 | 압축된 카메라 프레임 하나. $f_v$로 녹화 |
| $F$ | 120 GB $=120\times10^9$바이트 | 08:00에 카트 디스크에 남은 bag용 여유 공간 |
| $R$ | 1 Gbit/s | 카트와 워크스테이션 사이 이더넷 링크, 공칭값 |
| $\eta$ | 0.8 | 대량 복사가 내는 $R$의 비율. 그래서 복사는 $\eta R/8=100$ MB/s |
| $T$ | 8시간 | 교대 한 번, 08:00부터 16:00까지 |
| $\lambda$ | 시간당 0.1 | 워크스테이션에서 카트로 연 ssh 세션이 끊기는 빈도 — 노트북 덮개, 케이블, 시간 초과 |
| 주소 | `192.168.10.1`, `192.168.10.2` | 직결 링크 위의 워크스테이션과 카트 |
| 계정, 장치 | 사용자 `robot`, `/dev/ttyACM0`의 엔코더 보드 | 스택이 도는 계정과, 제어기가 읽는 USB 시리얼 장치 |

이 페이지의 모든 명령은 블록에 따로 적지 않은 한 macOS 26.6 노트북(arm64)의 bash 3.2에서 실행했고, 보이는 출력은 모두 그 실행이 찍은 그대로이며 줄인 곳은 표시했다. 카트는 bash 5.2.21과 GNU 도구를 갖춘 Ubuntu 24.04다. 두 시스템이 다른 곳에서는 어느 쪽이 찍은 출력인지 밝히고, 리눅스에서만 되는 명령이나 파일에는 *매뉴얼에서 가져옴, 여기서 실행하지 않음*이라고 적었다. 출처에 적은 공식 문서와 대조했을 뿐 실행하지는 않았다는 뜻이다.

*범위: 이 페이지는 연구자가 어느 기계에서든 매일 쓰는 리눅스를 가르친다. 파일과 경로, 셸이 한 줄에 하는 일, 프로세스와 시그널, 권한, 환경, 파이프와 스크립트, 소프트웨어 설치, 원격 작업, 장치와 서비스, 그리고 셸 사용자가 만나는 만큼의 시계와 네트워크이고, 각각을 P6의 컴퓨터에 적용한다. ROS 2 자체는 가르치지 않는다. 워크스페이스를 source하는 일은 [[04-robotics/ros2/what-ros2-is|25.1 §7]]과 [[04-robotics/ros2/workspaces-packages-launch|25.4 §6]], bag 녹화는 [[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]이다. Python 환경, Git, 파일 형식, 네트워크는 이 트랙의 다른 페이지([[02-foundations/tools/python-research-code|12.3]], [[02-foundations/tools/git-research-code|12.2]], [[02-foundations/tools/config-data-formats|12.4]], [[02-foundations/tools/computer-networks|12.5]])가 맡고, 나머지와 그것이 사는 곳은 12절이 적는다.*

### 그림으로 먼저 보기 · The picture

<svg viewBox="0 0 560 560" style="max-width:100%;height:auto" role="img" aria-label="패널 셋. A: 192.168.10.1의 워크스테이션이 약 100 MB/s로 복사하는 1 Gbit/s 이더넷으로 192.168.10.2의 로봇 컴퓨터 p6-cart에 닿는다. 카트에서는 systemd가 200 Hz 제어기, 50 Hz 비전 노드, 7.26 GB/h 녹화기를 띄운다. 제어기는 ttyACM0의 고정 이름인 /dev/p6-encoder로 엔코더를 읽고, 그 모드 crw-rw---- root dialout은 660이다. 녹화기는 여유 120 GB 디스크에 쓴다. B: 같은 척도로 그린 하루치 녹화. 08:00에서 시간당 7.26 GB씩 오르는 직선이 교대가 끝나는 16:00에 58.1 GB, 00:32에 디스크 가득. C: 없는 로그에 grep은 2, wc는 0으로 끝나고, 파이프라인은 pipefail이 없으면 0, 있으면 2를 보고한다.">
  <defs><marker id="lsh-arrk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs>
  <text x="12" y="18" font-size="12" font-weight="600" fill="currentColor">A · P6의 로봇 컴퓨터와 링크</text>
  <rect x="12" y="52" width="120" height="84" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.7"/>
  <text x="20" y="68" font-size="11" font-weight="600" fill="currentColor">워크스테이션</text>
  <text x="20" y="84" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">192.168.10.1</text>
  <text x="20" y="100" font-size="11" fill="currentColor">ssh p6 뒤 tmux</text>
  <text x="20" y="116" font-size="11" fill="currentColor">rsync로 bag 복사</text>
  <line x1="132" y1="94" x2="196" y2="94" stroke="currentColor" stroke-width="2"/>
  <text x="164" y="86" font-size="10" text-anchor="middle" fill="currentColor">이더넷</text>
  <text x="164" y="108" font-size="10" text-anchor="middle" fill="currentColor">1 Gbit/s</text>
  <text x="164" y="120" font-size="10" text-anchor="middle" fill="currentColor">≈100 MB/s</text>
  <rect x="196" y="28" width="352" height="176" rx="4" fill="none" stroke="currentColor" stroke-width="1.3" stroke-opacity="0.85"/>
  <text x="204" y="44" font-size="11" font-weight="600" fill="currentColor">p6-cart · Ubuntu 24.04 · <tspan font-family="ui-monospace,monospace" font-weight="400">192.168.10.2</tspan></text>
  <rect x="292" y="52" width="160" height="20" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.85"/>
  <text x="372" y="66" font-size="11" text-anchor="middle" font-family="ui-monospace,monospace" fill="currentColor">p6-stack.service</text>
  <text x="286" y="66" font-size="10" text-anchor="end" fill="currentColor" fill-opacity="0.8">systemd</text>
  <line x1="372" y1="72" x2="262" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arrk)"/>
  <line x1="372" y1="72" x2="372" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arrk)"/>
  <line x1="372" y1="72" x2="482" y2="88" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arrk)"/>
  <rect x="208" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="260" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">controller</text>
  <text x="260" y="118" font-size="10" text-anchor="middle" fill="currentColor">200 Hz → /cmd</text>
  <rect x="320" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="372" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">vision</text>
  <text x="372" y="118" font-size="10" text-anchor="middle" fill="currentColor">50 Hz → /goal</text>
  <rect x="432" y="90" width="104" height="34" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="484" y="104" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">recorder</text>
  <text x="484" y="118" font-size="10" text-anchor="middle" fill="currentColor">7.26 GB/h</text>
  <line x1="260" y1="124" x2="260" y2="144" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arrk)"/>
  <line x1="484" y1="124" x2="484" y2="144" stroke="currentColor" stroke-width="1" marker-end="url(#lsh-arrk)"/>
  <rect x="208" y="146" width="216" height="50" rx="3" fill="currentColor" fill-opacity="0.12" stroke="currentColor" stroke-width="1" stroke-opacity="0.85"/>
  <text x="214" y="160" font-size="10" font-family="ui-monospace,monospace" fill="currentColor">/dev/p6-encoder → ttyACM0</text>
  <text x="214" y="174" font-size="10" font-family="ui-monospace,monospace" fill="currentColor">crw-rw---- root dialout</text>
  <text x="214" y="188" font-size="10" fill="currentColor">모드 660: robot이 dialout에 있어야 함</text>
  <rect x="432" y="146" width="104" height="50" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="484" y="162" font-size="11" text-anchor="middle" font-weight="600" fill="currentColor">SSD</text>
  <text x="484" y="176" font-size="10" text-anchor="middle" fill="currentColor">여유 120 GB</text>
  <text x="484" y="189" font-size="10" text-anchor="middle" fill="currentColor">08:00 기준</text>
  <line x1="8" y1="214" x2="552" y2="214" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="12" y="234" font-size="12" font-weight="600" fill="currentColor">B · 하루치 녹화, 같은 척도로</text>
  <line x1="60" y1="392" x2="540" y2="392" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="60" y1="392" x2="60" y2="262" stroke="currentColor" stroke-width="1" stroke-opacity="0.6"/>
  <line x1="60" y1="272" x2="540" y2="272" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.3" stroke-dasharray="3 3"/>
  <line x1="60" y1="332" x2="540" y2="332" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.15"/>
  <text x="54" y="396" font-size="10" text-anchor="end" fill="currentColor">0</text>
  <text x="54" y="336" font-size="10" text-anchor="end" fill="currentColor">60</text>
  <text x="54" y="276" font-size="10" text-anchor="end" fill="currentColor">120</text>
  <text x="54" y="256" font-size="10" text-anchor="end" fill="currentColor">사용 GB</text>
  <g font-size="10" text-anchor="middle" fill="currentColor"><text x="60" y="406">08:00</text><text x="140" y="406">12:00</text><text x="220" y="406">16:00</text><text x="300" y="406">20:00</text><text x="380" y="406">00:00</text><text x="460" y="406">04:00</text><text x="540" y="406">08:00</text></g>
  <text x="300" y="420" font-size="10" text-anchor="middle" fill="currentColor" fill-opacity="0.8">시각. 녹화기는 08:00에 시작하고 아무도 멈추지 않는다</text>
  <line x1="60" y1="392" x2="390.69" y2="272" stroke="currentColor" stroke-width="2.2"/>
  <line x1="390.69" y1="272" x2="540" y2="272" stroke="currentColor" stroke-width="1.6" stroke-dasharray="6 4"/>
  <line x1="220" y1="392" x2="220" y2="333.94" stroke="currentColor" stroke-width="0.9" stroke-opacity="0.6" stroke-dasharray="3 3"/>
  <circle cx="220" cy="333.94" r="3.6" fill="currentColor"/>
  <circle cx="390.69" cy="272" r="3.6" fill="currentColor"/>
  <text x="70" y="298" font-size="11" font-weight="600" fill="currentColor">7.26 GB/h</text>
  <text x="70" y="312" font-size="10" fill="currentColor">카메라 99.2%, /cmd와 /goal 0.8%</text>
  <text x="228" y="350" font-size="10" font-weight="600" fill="currentColor">16:00 · 58.1 GB · 교대 끝</text>
  <text x="228" y="363" font-size="10" fill="currentColor">워크스테이션으로 복사: 9분 41초</text>
  <text x="398" y="290" font-size="10" font-weight="600" fill="currentColor">00:32 · 120 GB · 디스크 가득</text>
  <text x="398" y="303" font-size="10" fill="currentColor">시작 16시간 32분 뒤</text>
  <line x1="8" y1="432" x2="552" y2="432" stroke="currentColor" stroke-width="0.8" stroke-opacity="0.25"/>
  <text x="12" y="452" font-size="12" font-weight="600" fill="currentColor">C · 로그가 없을 때의 야간 점검</text>
  <rect x="12" y="462" width="236" height="40" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="20" y="478" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">grep ERROR p6_day2.log</text>
  <text x="20" y="494" font-size="10" fill="currentColor">상태 2: 파일 없음</text>
  <text x="258" y="488" font-size="12" font-weight="600" font-family="ui-monospace,monospace" fill="currentColor">|</text>
  <rect x="272" y="462" width="128" height="40" rx="3" fill="currentColor" fill-opacity="0.05" stroke="currentColor" stroke-width="1" stroke-opacity="0.8"/>
  <text x="280" y="478" font-size="11" font-family="ui-monospace,monospace" fill="currentColor">wc -l</text>
  <text x="280" y="494" font-size="10" fill="currentColor">0 출력, 상태 0</text>
  <text x="12" y="524" font-size="11" fill="currentColor">기본값: 파이프라인 상태는 마지막 명령의 것인 <tspan font-weight="600">0</tspan>, 보고서는 "오류 0건"</text>
  <text x="12" y="542" font-size="11" fill="currentColor">set -o pipefail이면: 상태는 <tspan font-weight="600">2</tspan>, set -e가 스크립트를 멈춘다</text>
</svg>

이 페이지가 보는 P6의 컴퓨터다. 워크스테이션은 약 100 MB/s로 복사하는 1 Gbit/s 링크로 `p6-cart`에 닿고, systemd가 부팅 때 세 프로그램을 띄우며, 제어기는 `ttyACM0`의 고정 이름인 `/dev/p6-encoder`로 엔코더를 읽는다. 그 모드 `crw-rw----`(660, 그룹 `dialout`)가 사용자 `robot`이 그 그룹에 있어야 하는 이유다. 패널 B는 녹화기의 7.26 GB/h를 같은 척도로 그린다. 교대는 16:00에 58.1 GB로 끝나 복사에 9분 41초가 걸리고, 아무도 멈추지 않은 녹화기는 00:32에 120 GB를 채운다. 패널 C는 없는 로그를 읽는 야간 점검이다. `grep`은 상태 2로 실패하는데도 `pipefail`이 없으면 파이프라인은 0을 보고한다.

### 1. 파일, 경로, 파일시스템 트리

*한 문장으로:* 기계의 모든 것은 `/`에서 시작하는 트리 하나에 매달려 있고, 경로는 그 안의 한 곳을 루트로부터 또는 읽는 쪽의 작업 디렉터리로부터 가리키며, `df`와 `du`가 얼마나 찼는지 말해 준다.

새 기계에서 처음 만나는 수수께끼는 대개 한 프로그램은 찾는 파일을 다른 프로그램은 못 찾는 일, 그리고 밤사이 차 버린 디스크다. 둘 다 파일시스템의 문제다. **셸**(shell)은 입력한 줄을 읽어 자기 규칙대로 고쳐 쓰고(2절) 거기 적힌 프로그램을 띄우는 프로그램이다. 그것을 둘러싼 창은 터미널일 뿐이다. 이 페이지의 스크립트는 `#!/bin/bash`로 시작하므로, 어떤 셸에 입력하든 카트에서 bash가 돌린다. 리눅스 기계가 가진 모든 것 — 프로그램, 설정, 데이터, 심지어 장치까지 — 은 `/`를 뿌리로 하는 디렉터리 트리 하나에 매달린다. `p6-cart`에서 중요한 자리와, 매뉴얼 페이지 hier(7)가 각각에 붙인 용도는 다음과 같다.

| 디렉터리 | 담는 것, 그리고 `p6-cart`에서 거기 사는 것 |
|---|---|
| `/home/robot` | 계정 `robot`의 홈 디렉터리. 워크스페이스, bag, `~/.ssh`, `~/.bashrc` |
| `/etc` | 이 기계에만 해당하는 설정. udev 규칙(9절), systemd 유닛(10절), 네트워크(11절) |
| `/opt/ros/jazzy` | 추가 패키지. apt가 설치한 ROS 2(7절) |
| `/usr/bin` | 프로그램의 기본 디렉터리. `bash`, `grep`, `rsync`, `ssh` |
| `/dev` | 하드웨어를 가리키는 장치 파일. `/dev/ttyACM0`(9절) |
| `/var/log`, `/tmp` | 로그 파일. 예고 없이, 이를테면 부팅 때 지워질 수 있는 임시 파일 |

모든 프로세스는 **작업 디렉터리** — 그 프로세스가 "들어가 있는" 디렉터리 — 를 지닌다. `pwd`는 셸의 작업 디렉터리를 찍고 `cd`는 그것을 바꾸며, 새 프로세스는 부모의 작업 디렉터리에서 시작한다. 경로는 그것을 기준으로 읽히고, "내가 돌리면 되는데" 류의 수수께끼 대부분이 여기서 시작한다.

**경로**(path)는 그 트리를 따라가는 길로 파일에 이름을 붙인다. `/` 사이의 구성 요소 하나하나를 지금까지 도달한 디렉터리 안에서 찾고, 지나가는 모든 디렉터리가 탐색 권한(4절)을 주어야 한다. `/`로 시작하는 경로는 **절대** 경로이고 찾기는 루트에서 시작한다. 그 밖의 경로는 **상대** 경로이고 그것을 쓰는 프로세스의 작업 디렉터리에서 시작한다. 그래서 절대 경로는 모든 프로세스에게 같은 파일을 가리키고, 상대 경로는 어느 작업 디렉터리에서 읽느냐에 따라 다른 파일을 가리킨다. `.`와 `..`는 지금까지 도달한 디렉터리와 그 부모이고(`/..`는 `/`), `~`는 이 규칙에 들어 있지 않다. 어떤 프로그램이 경로를 보기 전에 셸이 홈 디렉터리로 바꿔 놓기 때문이다(2절). `bags/day1`에 쓰는 녹화기를 `robot`이 `/home/robot`에서 띄우면 그것은 `/home/robot/bags/day1`이고, P6에서는 반 시간짜리 파일 하나에 약 3.6 GB가 쌓인다(계산 절).

함정은 다른 곳에서 띄운 프로그램이다. systemd 서비스는 따로 정하지 않으면 `/`에서 시작하므로(10절), 터미널에서 되던 상대 경로가 부팅 때 깨진다. 기계가 대신 띄워 주는 것 — 스크립트, launch 파일, 서비스 — 은 무엇이든 파일을 절대 경로로 부르거나 작업 디렉터리를 명시해야 한다. 영어 절의 `path_demo.sh`가 6절의 로그 점검으로 이 함정을 노트북에서 보여 준다. 로그가 있는 디렉터리에서는 `p6_day1.log: 3 errors, 56 warnings`가 나오고, `cd /` 뒤에 같은 스크립트를 부르면 `grep: p6_day1.log: No such file or directory`와 상태 1이 나온다.

**디스크가 얼마나 찼나.** 두 명령이 답하고, 둘은 다른 것을 잰다. `df -h`는 *파일시스템*마다 크기, 사용량, 여유를 보고하고, `du -sh DIR`는 *디렉터리 트리* 하나가 차지한 양을 더한다. `-h`를 주면 둘 다 1024의 거듭제곱으로 센다 — 그 "G"는 $10^9$이 아니라 $2^{30}$바이트다 — 그래서 위에서 고정한 여유 120 GB, 곧 $120\times10^9$바이트는 `df -h`에서 약 111.8G로 보인다. 로봇의 크기와 논문의 크기가 7% 어긋나면 대개 이것이 이유다. $10^9/2^{30}=0.931$.

> [!note]- 더 깊이 · Deeper
> GNU의 `df -H`와 `du --si`는 대신 1000의 거듭제곱으로 센다. 또 `du`는 파일의 정확한 길이가 아니라 파일이 차지한 디스크 블록을 세고, `-h`는 올림한다. 1,000,000바이트짜리 분할 파일 셋과 42바이트짜리 `metadata.yaml`로 만든 가짜 bag 디렉터리(8절이 복사하는 그것)는 3,000,042바이트, 곧 `du -h`가 "M"이라 부르는 1,048,576바이트 단위로 2.86이고, 노트북에서 영어 절의 `du -sh bags/day1`은 `2.9M`을 찍는다.

**문서는 어디 있나.** 이 페이지의 모든 명령과 파일 형식에는 매뉴얼 페이지가 있다. `man NAME`. `chmod(1)`이나 `systemd.service(5)`의 숫자는 섹션이다. 1은 사용자 명령, 5는 파일 형식과 설정 파일, 7은 hier(7) 같은 개관, 8은 시스템 관리 명령. `man 5 systemd.service`는 같은 이름의 명령이 아니라 파일 형식을 연다.

### 2. 셸이 한 줄에 하는 일: 확장과 인용

*한 문장으로:* bash는 프로그램이 보기 전에 모든 줄을 고쳐 쓴다 — 변수, 단어 분리, 파일 이름 패턴 — 그리고 인용이 그 가운데 무엇이 일어날지 정한다.

셸 스크립트의 놀라움 대부분 — 있는 파일이 없다고 나오고, 인수 하나가 둘로 쪼개지고, 지우기가 뜻한 것보다 멀리 미치는 일 — 은 프로그램이 보기 전에 bash가 한 줄에 무엇을 하는지 모르는 데서 온다. 어떤 프로그램이 돌기 전에 bash는 입력한 줄을 단어 목록으로 바꾸고, 프로그램은 그 목록만 본다. 입력한 따옴표도, `$`도, `*`도 보지 못한다. 규칙은 Bash 매뉴얼이 주는 순서대로의 고쳐 쓰기 셋과, 그것을 끄는 스위치 하나, 곧 인용이다. 작은따옴표 안에서는 모든 문자가 글자 그대로이고, 큰따옴표 안에서는 변수가 여전히 확장되지만 그 값이 쪼개지거나 파일 이름과 맞춰지지는 않는다. 예를 들어 `dir`이 `day 1`이면, `ls $dir/*.mcap`이라는 줄은 `ls`가 시작하기도 전에 경로 하나가 아니라 단어 둘, `day`와 `1/*.mcap`을 넘긴다. 아래 시연이 바로 그런 목록을 찍는다.

> **셸 확장의 정의.** **셸 확장**(shell expansion)은 *무엇이든 실행하기 전에 bash가 명령 줄에 가하는 고쳐 쓰기*다. 줄과 셸 변수의 성질이지 프로그램의 성질이 아니며, 프로그램은 결과만 받는다. 그 결과를 세 조건이 정한다. 인용되지 않은 단어는 **확장**된다. `~`는 홈 디렉터리로, `$name`은 변수 값으로, `$(command)`는 명령의 출력으로. 인용되지 않은 결과는 공백·탭·줄바꿈에서 **분리**되어 별개의 단어가 된다. 그리고 `*`, `?`, `[`를 담은 인용되지 않은 단어는 **패턴**이어서, 그것이 맞는 기존 파일들의 정렬된 이름으로 바뀌거나, 하나도 맞지 않으면 입력한 그대로 남는다. 큰따옴표는 둘째와 셋째 단계를 막고, 작은따옴표는 셋 모두를 막는다.
>
> $$n_{\text{args}}(\pi)=\max(m_\pi,\,1)$$
>
> $\pi$는 인용되지 않은 패턴 단어 하나, $m_\pi$는 그것이 맞는 기존 이름의 수다. 그래서 패턴은 맞춘 만큼의 인수를 프로그램에 넘기고, 하나도 맞추지 못하면 자기 글자를 그대로 넘기며, 큰따옴표 안의 `"$d"`는 `$d`에 무엇이 들었든 인수를 정확히 하나 넘긴다.
>
> - **예**: `dir="day 1"`이고 그 디렉터리에 분할 파일이 둘 있을 때의 `"$dir"/*.mcap`은 $m=2$. 둘 다 진짜 파일인 인수 둘이다(아래).
> - **비예**: 같은 줄에서 따옴표를 뺀 경우. 값 `day 1`이 먼저 분리되어 프로그램은 `day`와 `1/*.mcap`을 받는다. 둘째는 아무것도 맞추지 못해 글자 그대로 넘어간 패턴이다. 오류는 없다. 프로그램은 그저 파일이 아닌 이름을 받는다.
> - **왜 중요한가**: bag 디렉터리, 캘리브레이션 파일, 데이터셋 폴더는 이름에 공백과 날짜를 얻게 된다. 모든 `"$변수"`를 인용하는 스크립트는 그 모두에 같게 동작한다.

영어 절의 `quote_demo.sh`가 이 규칙을 노트북에서 돌린다. `printf '[%s]\n'`은 받은 인수 하나하나를 대괄호 안에 찍으므로 프로그램이 받을 것을 그대로 보여 준다. 따옴표 없이는 `[day]`와 `[1/*.mcap]`, 따옴표를 치면 `[day 1/run_0.mcap]`과 `[day 1/run_1.mcap]`, 아무것도 맞지 않는 패턴은 `[empty/*.mcap]` 그대로다. 넷째 경우가 데이터를 지우는 경우다. `bagdir`가 비어 있으면 `$bagdir/*`는 `/*`, 곧 루트의 모든 항목이 된다 — 이 Mac에서는 `/Applications`, `/Library`, `/System`, 카트에서는 `/bin`, `/boot`, `/etc` — 그래서 `rm -rf $bagdir/*`는 기계를 지우려 든다. `${bagdir:?메시지}`는 비었거나 설정되지 않은 변수의 확장을 거부한다. 스크립트는 메시지를 찍고(`quote_demo.sh: line 12: bagdir: is empty`) 멈추며, `not reached`는 끝내 돌지 않는다.

`set -u`(6절)는 보기보다 약하다. 한 번도 설정되지 않은 변수에만 반대하고, 빈 문자열로 설정된 변수는 통과시킨다. 영어 절의 `nounset_demo.sh`에서 오타 `bag_dir`는 `unbound variable`로 잡히지만 비어 있는 `bagdir`는 잡히지 않는다. 모든 변수를 인용하고, 비면 안 되는 변수는 `:?`로 지키면 이런 사고 전체가 막힌다.

### 3. 프로세스, 시그널, 작업

*한 문장으로:* 돌고 있는 프로그램은 번호, 부모, 종료 상태를 가진 프로세스이고, 시그널 — 터미널에서, `kill`에서, systemd에서 오는 — 이 그것을 깨끗하게든 아니든 멈추는 수단이다.

로봇이 이상하게 굴면 그 프로그램들을 찾고, 멈추고, 각각이 어떻게 끝났는지 읽어야 한다. 그리고 어떻게 멈추느냐가 제어기가 끝나기 전에 0을 명령할 기회를 얻는지를 정한다. **프로세스**(process)는 프로그램 하나가 실행 중인 인스턴스다. 번호(PID), 부모(PPID), 사용자와 그룹(4절), 환경(5절), 작업 디렉터리(1절), 그리고 열린 스트림 셋(6절)을 가진다. `ps -ef`는 기계의 모든 프로세스를 나열하고, `pgrep -af controller`는 *전체 명령 줄*에 `controller`가 든 것을 나열한다. `-f`가 없으면 pgrep은 프로세스 이름에만 맞추는데, 커널은 그 이름을 15자로 자른다. `vision_goal_publisher`라는 노드 실행 파일은 거기서 `vision_goal_pub`이 되고, `python3 script.py`로 띄운 스크립트의 이름은 `python3`이다. `top`은 프로세스를 실시간으로 보여 준다. 프로세스는 다른 프로세스가 띄우고, 끝날 때 그 부모에게 **종료 상태**(exit status)를 돌려준다. 성공은 0, 실패는 1–255. bash는 찾지 못한 명령에 127을, 찾았지만 실행할 수 없는 파일에 126을 보고한다(4절).

명령 뒤에 `&`를 붙이면 **백그라운드 작업**으로 돌고 셸은 바로 돌아온다. `jobs`는 셸의 작업을 나열하고, `fg`는 작업 하나를 포그라운드로 가져오며, Ctrl-Z는 포그라운드 작업을 멈추고 `bg`는 그것을 백그라운드에서 이어 가게 한다. 이 관리가 **작업 제어**(job control)다. 대화형 셸은 작업마다 따로 프로세스 그룹을 주어, Ctrl-C, Ctrl-Z, `fg`, `bg`가 한 번에 작업 하나에만 작용하게 한다. 스크립트에서는 `set -m`으로 켜지 않는 한 작업 제어가 꺼져 있고, 이 절의 마지막 함정이 거기서 나온다. `ps`나 `top`에서는 상태 글자가 각 프로세스가 무엇을 하는지 말한다. `S`는 인터럽트 가능한 잠이다 — 다음 메시지를 기다리며 막혀 있는 노드가 이렇게 보인다 — `D`는 인터럽트 불가능한 잠(대개 디스크나 장치 입출력), `T`는 멈춤, `Z`는 부모가 종료 상태를 거두지 않은 좀비다.

> [!note]- 더 깊이 · Deeper
> 영어 절의 `jobs_demo.sh`는 `set -m`으로 작업 제어를 켜고 잠든 작업 하나를 `ps`로 나열한다. 노트북에서 그 작업은 상태 `S`, 경과 시간 `00:01`로 보이고, `jobs`는 `[1]+  Running  sleep 100 &`을 찍는다.

프로세스를 멈추는 제어 수단이 **시그널**이다.

> **시그널의 정의.** **시그널**(signal)은 *커널이 프로세스에 전달하는 작은 번호 붙은 알림*이다. 실어 나르는 내용이 없고, 두 예외를 빼면 프로세스가 따라야 하는 명령도 아니다. 네 조건이 정의한다. 시그널마다 **번호와 기본 동작**이 있다. SIGHUP 1, SIGINT 2, SIGKILL 9, SIGTERM 15는 프로세스가 따로 손쓰지 않으면 모두 프로세스를 끝내고, 이 네 번호는 모든 리눅스 아키텍처에서 같다. 프로세스는 시그널을 제 핸들러로 **잡거나**(catch) **무시**할 수 있다 — SIGKILL과 SIGSTOP은 예외로, 잡을 수도 막을 수도 무시할 수도 없다. 시그널을 보내는 쪽은 **세 종류**다. 터미널(Ctrl-C는 포그라운드 작업의 프로세스들에 SIGINT를, Ctrl-Z는 SIGTSTP를 보낸다), 다른 프로세스(따로 말하지 않으면 SIGTERM을 보내는 `kill`, 서비스를 멈추는 systemd, 10절), 그리고 커널 자신. 그리고 시그널 때문에 **죽은** 프로세스는 부모가 읽는 상태에 그 시그널의 번호를 남긴다.
>
> $$s=128+n$$
>
> $n$은 프로세스를 죽인 시그널의 번호, $s$는 bash가 보고하는 종료 상태다. 그래서 130은 SIGINT, 143은 SIGTERM, 137은 SIGKILL이다. `ros2 launch`가 쓰는 Python의 subprocess 기구는 같은 죽음을 대신 $-n$으로 보고한다.
>
> - **예**: 노트북에서 `sleep` 프로세스 셋에 시그널을 하나씩 보내면 상태가 130, 143, 137이다(아래). launch 로그의 `process has died [pid 4242, exit code -2, ...]` 같은 줄도 이렇게 읽는다 — 충돌이 아니라 SIGINT다.
> - **비예**: Ctrl-C를 누른 뒤의 종료 상태 0이나 1. SIGINT를 *잡아* 깨끗하게 끝나는 프로그램은 자기가 고른 상태로 끝난다. $128+n$은 시그널이 죽인 프로세스만 설명한다. 그리고 상태 1은 결코 시그널이 아니다. 프로그램이 스스로 실패를 보고한 것이다.
> - **왜 중요한가**: 로봇을 멈추는 길은 시그널의 연쇄다 — Ctrl-C, 이어서 `ros2 launch`의 단계적 강화, 이어서 systemd의 시간 제한 — 그리고 그것을 처리하는 프로세스만 떠나기 전에 모터를 세우고 파일을 닫을 수 있다.

영어 절의 `signals_demo.sh`가 세 가지 죽음을 노트북에서 보여 준다. SIGINT는 상태 130, SIGTERM은 143, SIGKILL은 137이고, bash는 각 죽음을 `Interrupt: 2`, `Terminated: 15`, `Killed: 9`로 알린다.

**노드는 어떻게 반응해야 하나.** 두 ROS 2 클라이언트 라이브러리는 기본값으로 SIGINT와 SIGTERM에 핸들러를 설치한다. `rclcpp::init`과 `rclpy.init`이 두 시그널을 잡아 노드의 컨텍스트를 끝내고, 그러면 `spin`이 돌아온다. 제어기가 0을 명령하고, 시리얼 포트를 닫고, 녹화기가 bag을 닫게 하는 순간이 그때다. `ros2 launch`가 종료될 때 그것이 띄운 모든 프로세스는 세 단계로 멈춘다. 먼저 SIGINT(Ctrl-C라면 터미널이 곧바로 보내고, 그 밖에는 launch가 보낸다), 5초 뒤에도 돌고 있는 것에는 launch가 SIGTERM, 다시 5초 뒤에 SIGKILL. 그러니 멈추는 데 5초보다 오래 걸리는 노드는 정리 도중에 죽고, SIGKILL은 어떤 프로세스에게도 파일의 끝을 쓸 기회를 주지 않는다. 모터의 안전 상태는 이 연쇄에 전혀 기대면 안 된다. 그것은 드라이브와 정지 회로에 산다([[04-robotics/ros2/from-simulation-to-hardware|25.11 §6]]).

**Ctrl-C를 무시하는 백그라운드 작업.** 스크립트에서는 작업 제어가 꺼져 있고, bash는 모든 백그라운드 작업을 SIGINT와 SIGQUIT가 *무시된* 채로 띄운다. 녹화기를 `&`로 띄워 두고 나중에 Ctrl-C처럼 `kill -INT`로 멈추려는 시작 스크립트는 녹화기를 그대로 둔다. 영어 절의 `bg_sigint.sh`에서 SIGINT 뒤의 `sleep`은 여전히 돌고(`after SIGINT: still running`), SIGTERM이 상태 143으로 끝낸다. `kill -0`은 시그널을 보내지 않고 프로세스가 있는지만 시험한다. 스크립트의 `sleep 1`은 자식이 SIGINT를 무시로 설정할 틈을 준다. 그 전에 보낸 시그널은 여전히 자식을 죽인다. 스크립트의 백그라운드 작업은 `kill`의 기본값인 SIGTERM으로 멈추거나, 더 낫게는 systemd에 맡긴다(10절).

### 4. 사용자, 그룹, 권한

*한 문장으로:* 모든 파일은 소유자, 그룹, 권한 비트 아홉 개를 가지며, 한 프로세스에는 그중 정확히 한 부류만 적용되고, 시리얼 장치는 그 그룹을 통해 열린다.

새 로봇 컴퓨터에서 가장 먼저 실패하는 것은 대개 권한이다. 제어기가 시리얼 포트를 열지 못하고, 오류는 *Permission denied*라고만 말한다. 모든 프로세스는 숫자 ID를 가진 **사용자**, 주 **그룹** 하나, 보조 그룹 목록으로 돈다. `id`는 셸의 이 셋을 모두 찍는다. ID가 0인 사용자 `root`는 아래의 권한 검사를 건너뛴다. 다만 root라도 파일을 실행하려면 그 실행 비트가 적어도 하나는 켜져 있어야 한다. `sudo COMMAND`는 기계의 sudoers 정책이 계정에 허락하면 명령 하나를 root로 돌리는데, *초기화된* 환경, 곧 `PATH`, `HOME`, `USER` 같은 몇몇 변수만 남은 환경에서 돌린다. 그래서 `source`(5절)가 터미널 환경에 넣은 것 가운데 그 명령까지 가는 것은 많아야 `PATH`뿐이고, `sudo ros2 …`는 실패한다.

모든 파일은 소유자, 그룹, 권한 비트 아홉 개를 지닌다. 소유자(`u`), 그룹(`g`), 그 밖의 모두(`o`) 각각의 읽기, 쓰기, 실행이다. `ls -l`은 종류 글자 뒤에 그것을 보여 준다. `-`는 일반 파일, `d`는 디렉터리, `l`은 심볼릭 링크, `c`는 시리얼 포트 같은 문자 장치다. 디렉터리에서 읽기는 이름을 나열하고, 쓰기는 항목을 만들고 지우며, 실행은 *탐색*, 곧 경로 위에서 그 디렉터리를 지나갈 권리다(1절).

> **권한 모드의 정의.** 파일의 **권한 모드**(permission mode)는 *세 부류 × 세 비트, 곧 비트 아홉 개*다. 소유자, 그룹, 기타 사용자 각각의 읽기, 쓰기, 실행이며, 8진수 세 자리로 쓴다. 사용자가 아니라 파일에 속한다. 접근 하나를 세 조건이 결정한다. 커널은 프로세스에 **정확히 한 부류**를 고른다. 프로세스의 사용자가 파일을 소유하면 소유자 부류, 아니면 파일의 그룹이 프로세스의 그룹이거나 보조 그룹 중 하나이면 그룹 부류, 아니면 기타 부류 — 처음 맞는 것이 이기고, 뒤 부류가 더 많이 허락하더라도 그렇다. 그다음 **그 부류의 세 비트만** 요청된 접근과 대조한다. 그리고 각 자리는 **비트의 합**이다. 읽기 = 4, 쓰기 = 2, 실행 = 1이라서, 0부터 7까지의 각 숫자가 조합 하나를 가리킨다.
>
> $$m=(d_u\,d_g\,d_o)_8=64\,d_u+8\,d_g+d_o,\qquad d=4r+2w+x$$
>
> $r,w,x\in\{0,1\}$은 한 부류의 비트, $d_u,d_g,d_o$는 세 자리다. 그래서 `rw-`는 $4+2=6$, `r-x`는 5이고, `rw-rw----`는 8진수로 660, 10진수로 432다. 파일은 프로그램이 요청한 모드, 보통 666에서 셸의 `umask`, 보통 022에 든 비트를 뺀 모드로 만들어지고, 그래서 새 파일은 644로 나타난다.
>
> - **예**: 엔코더 보드. Ubuntu의 udev 규칙은 모든 `ttyACM` 장치에 그룹 `dialout`을 주고, 그룹이 있는 장치 노드에 대한 udev의 기본 모드는 0660이므로 `/dev/ttyACM0`은 `crw-rw---- root dialout`으로 보인다. 사용자 `robot`은 `root`가 아니므로 소유자 부류는 해당하지 않는다. `robot`이 `dialout`에 있으면 그룹 자리 6이 읽기와 쓰기를 주고, 없으면 기타 자리 0이 아무것도 주지 않아 제어기의 `open()`이 *Permission denied*로 실패한다.
> - **비예**: `sudo chmod 666 /dev/ttyACM0`. 보드를 뽑거나 카트가 재부팅할 때까지만 통한다. udev가 매번 노드를 새로 만들며 규칙의 모드를 주기 때문이다. 고칠 것은 모드가 아니라 그룹이다.
> - **왜 중요한가**: 로봇의 "Permission denied"는 root로 풀리는 일이 거의 없다. 해당하는 부류를 찾고, 그것에 답하는 그룹이나 모드를 바꾼다.

영어 절의 `perm_demo.sh`는 비트를 설정하고 다시 읽는다. `umask`는 `0022`, 새 파일은 `-rw-r--r-- 644`, `chmod 660` 뒤에는 `-rw-rw---- 660`, `chmod u=rw,g=r,o=` 뒤에는 `-rw-r----- 640`이고, `chmod 000` 뒤의 `cat`은 `Permission denied`와 상태 1로 끝난다. macOS의 `stat -f "%Sp %Lp"`가 모드를 글자와 8진수로 찍는다. 카트에서의 GNU 형태는 `stat -c "%A %a" FILE`이다(매뉴얼에서 가져옴, 여기서 실행하지 않음).

**장치를 가진 그룹에 들어가기.** 카트에서는 `sudo usermod -aG dialout robot`이다(매뉴얼에서 가져옴, 여기서 실행하지 않음). `-a`는 덧붙이고, 그것이 없으면 `-G`는 `robot`의 그룹들을 갈아 치운다. 그다음 로그아웃했다가 다시 로그인한다. 로그인 — 이를테면 ssh 세션 — 은 계정의 그룹을 그룹 데이터베이스에서 읽고, 그 뒤에 띄운 모든 프로세스는 그 목록을 그대로 물려받는다. 그래서 `usermod`를 입력한 터미널과, 거기서 띄운 모든 노드에는 여전히 `dialout`이 없다. 새 ssh 세션의 `id`가 그것을 보여 준다. `-a`를 빼먹는 것은 그것대로 재앙이다. `usermod -G dialout robot`은 `dialout`을 계정의 *유일한* 보조 그룹으로 만들어, `sudo`를 비롯한 다른 모든 그룹에서 빼 버린다.

**실행 비트.** 스크립트는 `x` 비트가 설정되어 있어야 `./p6_check.sh`로 돈다. `bash p6_check.sh`는 상관없이 돈다. 그때는 bash가 파일을 데이터로 읽기 때문이다. 영어 절의 `exec_bit.sh`에서 `x` 없는 `./p6_check.sh`는 `Permission denied`와 상태 126, `bash p6_check.sh`는 `p6 check ok`와 상태 0이고, `chmod +x` 뒤에는 모드가 `-rwxr-xr-x 755`가 되어 `./p6_check.sh`도 돈다. 상태 126은 bash의 "찾았지만 실행할 수 없음"이다. 부류 글자 없는 `chmod +x`는 `umask`가 막는 곳을 빼고 세 부류 모두에 실행을 더하므로, 여기서는 755가 된다.

### 5. 환경, `PATH`, `source`

*한 문장으로:* 환경 변수는 프로세스에서 그것이 띄운 프로세스로만 흐르고 거꾸로는 흐르지 않는다. 그래서 터미널에는 `source`가 필요하고, ssh 명령과 `sudo`와 서비스는 저마다 따로 필요하다.

한 터미널에서는 되는데 다른 터미널에서는 안 되는 명령 — 또는 키보드에서는 되는데 ssh나 부팅 때는 안 되는 명령 — 은 거의 언제나 환경 탓이다. **환경 변수**(environment variable)는 프로세스가 지니고 다니다가 자기가 띄우는 프로세스에 넘겨주는 `NAME=value` 문자열이다. `printenv`는 셸의 환경을 나열하고 `echo "$HOME"`은 변수 하나를 찍는다. 셸 변수는 내보내야(`export NAME=value`) 환경에 들어가고, `NAME=value command`는 명령 하나에만 변수 하나를 설정한다.

무엇이 실행될지 정하는 변수는 `PATH`다. 콜론으로 구분한 디렉터리 목록이다. `/` 없는 이름을 입력하면 bash는 디렉터리를 차례로 시도해, 그 이름을 가진 실행 파일을 처음 찾은 곳에서 돌린다. 어디에도 없으면 결과는 `command not found`와 상태 127이다. `type -a NAME`은 맞는 것을 순서대로 모두, `command -v NAME`은 실제로 돌 하나를 보여 준다.

> **환경 변수의 정의.** **환경 변수**는 *프로세스의 환경, 곧 커널이 새 프로그램이 시작할 때 넘겨주는 목록 안의 이름–값 문자열*이다. 한 프로세스의 성질이지 기계나 터미널의 성질이 아니다. 그것이 어디까지 닿는지를 세 조건이 정한다. 자식은 만들어질 때 부모가 내보낸 변수의 **사본을 받는다**. 그 뒤의 변화는 **아래로만 흐른다**. 자식은 제 사본을 바꿀 수 있어도 부모의 것은 결코 못 바꾸므로, 프로그램으로 실행된 스크립트는 자기를 실행한 셸을 바꿀 수 없다. 그리고 변수는 **자기를 띄운 사슬을 따라서만** 프로세스에 닿는다. 터미널 둘, systemd 서비스 하나, `sudo` 명령 하나는 서로 다른 사슬 넷이다.
>
> $$c\ \longmapsto\ d_k/c,\qquad k=\min\{\,i:\ d_i/c\ \text{is an executable file}\,\},\qquad \texttt{PATH}=d_1{:}d_2{:}\cdots$$
>
> $c$는 `/`가 없는 명령 이름, $d_i$는 `PATH`의 디렉터리들을 순서대로 늘어놓은 것이다. 그래서 그 이름의 프로그램을 가진 첫 디렉터리가 이기고, 디렉터리를 앞에 붙이면 그 안의 프로그램이 뒤의 모든 것을 가린다. ROS 2 setup 파일을 source하는 일이 정확히 이것이다.
>
> - **예**: `source /opt/ros/jazzy/setup.bash`는 이 셸의 `PATH` 앞에 `/opt/ros/jazzy/bin`을 붙여 `ros2`가 거기서 풀리게 하고, ROS 2가 읽는 다른 변수들을 내보낸다. 이 셸에서 띄운 모든 노드가 그것을 물려받는다.
> - **비예**: `bash setup.bash`. 파일을 *자식* 셸에서 돌리므로, 자식이 제 사본에 모든 변수를 설정하고는 끝나 버리고, 그것을 입력한 터미널은 그대로다 — 한 줄 뒤에 `command not found`(아래).
> - **왜 중요한가**: 로봇에서 "이 터미널에서는 되는데 저기서는 안 된다"는 거의 모두, 한 프로세스 사슬에는 닿고 다른 사슬에는 닿지 않은 변수다.

`source FILE` — 또는 `. FILE` — 은 파일의 명령을 *현재* 셸로 읽어 들이고, 파일이 터미널의 환경을 바꾸는 방법은 이것뿐이다. 영어 절은 워크스페이스 setup 파일의 대역인 `fake_ws/setup.bash`(자기 `bin` 디렉터리를 `PATH` 앞에 붙인다)를 먼저 `bash`로 돌리고 다음에 `source`한다(`env_demo.sh`). 돌렸을 때는 `P6_WS=<unset>`이고 `p6_status: command not found`가 나오며, source한 뒤에는 변수가 설정되고 `p6_status: controller up`이 나온다.

**ROS 2의 경우.** ROS 2의 setup 파일을 source하지 않은 셸에서는 그 명령에도 패키지에도 닿지 못한다. 그래서 새 터미널마다 `source /opt/ros/jazzy/setup.bash`가 필요하고, 아니면 그 줄을 `~/.bashrc` — bash가 로그인 셸이 아닌 모든 대화형 셸에서 읽는 파일 — 에 둔다. ssh 로그인은 로그인 셸이고, 그것이 읽는 Ubuntu의 기본 `~/.profile`이 다시 `~/.bashrc`를 읽는다. 그러면 `printenv | grep -i ROS`에 `ROS_VERSION=2`, `ROS_PYTHON_VERSION=3`, `ROS_DISTRO=jazzy`가 보여야 한다. setup 파일이 환경에 무엇을 넣는지, 그리고 워크스페이스를 왜 설치본 *다음에* source하는지는 [[04-robotics/ros2/workspaces-packages-launch|25.4 §6]]의 언더레이–오버레이 규칙이고, 한 번도 source하지 않은 터미널이라는 고장은 [[04-robotics/ros2/what-ros2-is|25.1 §11]]이 연습시킨다.

**ROS를 못 찾는 ssh 명령.** `ssh p6`는 대화형 셸을 주고, 그 안에서 `ros2`는 된다. `ssh p6 'ros2 topic list'`는 `ros2: command not found`로 답한다. sshd가 명령 하나를 돌리려고 bash를 띄울 때도 bash는 `~/.bashrc`를 읽지만, Ubuntu의 기본 `~/.bashrc`는 대화형이 아닌 셸이면 첫머리에서 바로 돌아가 버린다. 그래서 ROS 2 설치 안내가 파일 *끝*에 덧붙이는 `source` 줄은 끝내 돌지 않는다. 노트북에서, 첫 줄들이 Ubuntu 24.04의 기본 `~/.bashrc`와 같고 끝에 ROS 2 줄의 대역을 둔 파일은 대화형 bash가 읽으면 대역을 설정하고 비대화형 bash가 읽으면 설정하지 않는다(`interactive: yes`, `non-interactive: no`. 스크립트는 콜아웃에 있다).

> [!note]- 더 깊이 · Deeper
> 영어 절의 `bashrc_demo.sh`에서 `--rcfile … -i`는 그 파일을 읽는 대화형 bash를 띄우고, `BASH_ENV`는 비대화형 bash가 그 파일을 읽게 한다. sshd의 비대화형 bash가 `~/.bashrc`를 읽는 것의 대역이다.

명령 안에서 직접 source하고 — `ssh p6 'source /opt/ros/jazzy/setup.bash && ros2 topic list'` — 어떤 파일이 읽히리라고 기대지 않는다. 터미널을 거치지 않는 다른 두 사슬에도 같은 규칙이 적용된다. 초기화된 환경이 ROS 변수를 떨어뜨리는 `sudo`(4절), 그리고 셸 시작 파일을 전혀 읽지 않는 systemd 서비스(10절).

### 6. 파이프, 리디렉션, 스크립트

*한 문장으로:* 모든 프로세스는 `>`, `2>`, `|`가 다시 잇는 스트림 셋을 갖고, 파이프라인은 종료 상태 하나를 보고하며, `set -euo pipefail`은 어떤 상태가 답인지 말해 주어야 비로소 진짜 실패에서만 스크립트를 멈춘다.

로봇은 누가 읽는 것보다 빨리 로그를 쓴다. 파이프는 로그를 숫자 몇 개로 바꾸고 스크립트는 그 파이프를 매일 밤 돌린다 — 그리고 둘 다 실패가 그 안에 숨을 수 없을 때에만 쓸모가 있다. 모든 프로세스는 열린 스트림 셋으로 시작한다. 표준 입력(0), 표준 출력(1), 표준 오류(2). 프로그램은 결과를 표준 출력에, 불평을 표준 오류에 쓰고, 둘 다 리디렉션하기 전까지는 터미널에 나타난다.

| 문법 | 효과 |
|---|---|
| `cmd > f`, `cmd >> f` | 표준 출력을 파일 `f`로. 덮어쓰기 또는 덧붙이기 |
| `cmd 2> f` | 표준 오류를 `f`로 |
| `cmd > f 2>&1` | 둘 다 `f`로. 먼저 1이 `f`로 가고, 다음에 2가 1이 지금 가는 곳으로 간다 |
| `cmd < f` | 표준 입력을 `f`에서 |
| `a \| b` | `a`의 표준 출력을 `b`의 표준 입력으로. `a`의 표준 오류는 여전히 터미널로 |

리디렉션은 왼쪽에서 오른쪽으로 적용되므로 순서가 중요하다. `2>&1 > f`는 2를 (1이 *그때* 있던) 터미널로 향하게 한 뒤에야 1을 `f`로 옮긴다. 영어 절의 시연은 ROS 2 노드처럼 로그 두 줄을 표준 오류에 쓰는 노드 대역 `fake_node.py`를 쓴다. `redirect_demo.sh`에서 `> both.log 2>&1`은 두 줄을 모두 파일에 담고, `2>&1 > only_stdout.log`는 두 줄을 터미널에 흘리고 파일을 비워 둔다(0줄). macOS의 `wc`는 위처럼 숫자 앞을 공백으로 채운다. 스크립트는 그 수를 숫자로 읽어야 하고, 공백의 모양에 기대면 안 된다.

**`| grep`이 노드의 경고를 놓치는 이유.** ROS 2 노드는 로그 줄을 기본 형식 `[SEVERITY] [time] [node]: message`로 콘솔의 *표준 오류*에 쓴다. 파이프는 표준 출력만 나르므로, `ros2 run … | grep WARN`은 모든 로그 줄을 손대지 않은 채 터미널로 흘리고 `grep`은 아무것도 읽지 못한다. 영어 절의 `stderr_pipe.sh`에서 `|`만 쓰면 두 줄이 그대로 찍히고 `grep -c`는 0, `2>&1 |`을 쓰면 1이다. `2>&1 |`로 쓴다. 카트의 bash 5.2는 그것의 약칭 `|&`도 받지만, 노트북의 bash 3.2는 `|&`를 문법 오류로 거부한다.

**하루치 로그 걸러 내기.** 76줄 — 또는 76,000줄 — 짜리 로그가 숫자 셋이 되는 것이 파이프다. 영어 절의 로그는 합성한 것이다. P6 세 노드의 8시간 교대 하루를 ROS 2 콘솔 형식으로, 이 페이지를 위해 스크립트로 썼다(파일을 쓰므로 CI는 돌리지 않는다). 노드별 경고와 오류를 많은 것부터 세는 한 줄 — `grep -E`가 두 심각도 중 하나로 시작하는 줄을 남기고, `cut`이 1번과 3번 필드(심각도와 노드)를 남기고, `sort`가 같은 줄을 모으고, `uniq -c`가 같은 줄의 연속을 세고, `sort -rn`이 개수로 정렬한다 — 은 노트북에서 vision의 WARN 46, controller의 WARN 10, controller의 ERROR 3을 준다. `uniq`는 *이웃한* 같은 줄만 합치므로 첫 `sort`는 생략할 수 없다.

**파이프라인의 종료 상태.** 파이프라인의 각 명령은 제 프로세스로 돌며 제 상태를 돌려주고, `grep`은 셋을 쓴다. 줄을 골랐으면 0, 하나도 못 골랐으면 1, 파일이 없는 것처럼 무언가 잘못됐으면 2. 셸은 파이프라인 전체에 숫자 하나를 보고한다.

> **파이프라인 종료 상태의 정의.** **파이프라인의 종료 상태**는 *사슬 `c₁ | c₂ | … | cₙ`에 대해 bash가 `$?`에 기록하는 숫자 하나*다. 어느 한 명령의 성질이 아니라 셸 옵션 아래 파이프라인 전체의 성질이다. 세 조건이 정의한다. 각 $c_k$는 제 상태 $s_k$를 가진 **별도의 프로세스**로 돌고, bash는 그 모두를 배열 `PIPESTATUS`에 둔다. **기본값에서는** 앞에서 무슨 일이 있었든 파이프라인의 상태가 마지막 명령의 상태 $s_n$이다. **`set -o pipefail`** 아래에서는 실패한 명령 가운데 가장 오른쪽 것의 상태이고, 실패한 것이 없으면 0이다.
>
> $$s_{\text{pipe}}=\begin{cases}s_n & \text{pipefail off}\\ s_{k^\ast},\ k^\ast=\max\{k:\ s_k\neq 0\} & \text{pipefail on, } 0 \text{ if no } s_k\neq0\end{cases}$$
>
> $s_k$는 $k$번째 명령의 상태다. 그래서 `pipefail`이 없으면 마지막 명령이 아닌 곳의 실패는 사라지고, 있으면 어느 단계든 실패하는 순간 파이프라인이 실패한다.
>
> - **예**: 2일째 로그가 한 번도 쓰이지 않은 날의 `grep ERROR p6_day2.log | wc -l`. `grep`은 2로 끝나고 `wc`는 0을 찍고 0으로 끝난다. $(s_1,s_2)=(2,0)$이므로 기본값에서 $s_{\text{pipe}}=0$, `pipefail` 아래에서 2다(영어 절의 `pipefail_demo.sh`, 그리고 그림의 패널 C).
> - **비예**: 오류가 없는 로그의 `grep ERROR p6_clean.log | wc -l`. $(s_1,s_2)=(1,0)$이고, `pipefail` 아래에서 파이프라인은 잘못된 것이 없는데도 1로 "실패"한다. `grep`의 1은 *오류*가 아니라 *고른 줄 없음*이다. `set -e`까지 켠 스크립트는 거기서 소리 없이 멈춘다(아래).
> - **왜 중요한가**: 아무것도 읽지 못해서 "오류 0건"이라고 보고하는 점검은 점검이 없는 것보다 나쁘다. 모든 단계의 상태가 그 둘을 가른다.

**스크립트.** 스크립트는 첫 줄이 `#!/bin/bash`이고 실행 비트(4절)가 켜진 명령 파일이다. 모든 스크립트를 `set -euo pipefail`로 시작한다. `-e`는 명령이 실패하면 스크립트를 멈춘다 — `if`의 조건, 그리고 `&&`·`||` 목록에서 마지막을 뺀 모든 명령처럼 bash가 면제하는 자리는 빼고. `-u`는 한 번도 설정되지 않은 첫 변수에서 멈춘다(2절). `pipefail`은 파이프라인 어디서든 난 실패를 센다. 셋을 함께 쓰면 함정이 하나 있고, 위의 비예가 그것이다. 영어 절의 `strict_demo.sh` — 유일한 잘못이 아무것도 못 찾은 것인 로그 점검 — 는 노트북에서 아무것도 찍지 않고 상태 1로 끝난다. `grep`의 "고른 줄 없음"이 스크립트를 끝냈기 때문이다. 처방은 어떤 상태가 답인지 말해 주는 것이다. 이 페이지가 쓰는 점검 `p6_check_log.sh`(영어 절)는 `grep`의 1은 받아들이고 그 밖의 것은 받아들이지 않는다(`|| test $? -eq 1`). 노트북에서 1일째 로그에는 `3 errors, 56 warnings`와 상태 0, `INFO` 두 줄짜리 깨끗한 로그에는 `0 errors, 0 warnings`와 상태 0, 없는 로그에는 `grep`의 오류와 상태 1, 인수가 없으면 사용법 메시지와 상태 1이다. 없는 로그는 이제 크게 실패하고 깨끗한 로그는 통과한다. `|| true`였다면 깨끗한 경우를 조용히 넘겼겠지만 — 없는 파일도 함께 넘겼을 것이다.

### 7. 소프트웨어 설치: apt, pip, 또는 컨테이너

*한 문장으로:* apt는 시스템을, pip는 직접 만든 가상 환경을, 컨테이너는 제 이미지를 소유하고, 모든 소프트웨어는 그것이 갈 자리를 소유한 단 하나의 도구로 들여야 한다.

패키지 하나를 잘못 설치하면 기계의 모든 계정에서 ROS 2 자신의 도구가 망가질 수 있다. 그러니 설치 도구를 고르는 일은 어느 파일을 누가 소유할지 고르는 일이다. 소프트웨어가 카트에 들어오는 길은 셋이고, 각각이 디스크의 다른 부분을 소유한다.

**apt**는 Ubuntu의 패키지와, ROS 프로젝트 자체의 apt 저장소에서 오는 ROS 2의 패키지를 설치한다. `sudo apt update`는 받을 수 있는 목록을 새로 고치고, `sudo apt install ros-jazzy-ros-base`는 패키지 하나와 그것이 의존하는 모든 것을 기계의 모든 계정을 위해 `/usr` 아래, 그리고 ROS 2라면 `/opt/ros/jazzy` 아래 설치한다. root가 필요하고, 패키지마다 기계 전체에 한 버전을 설치한다. 키보드에서는 `apt`를 치고 스크립트에서는 `apt-get`을 쓴다. APT가 `apt`의 명령 줄을 버전 사이에 안정되게 지키겠다고 약속하지 않기 때문이다. ROS 2 워크스페이스는 시스템 의존성을 `package.xml`의 키로 적고, `rosdep`이 그 키를 apt 패키지로 바꾼다([[04-robotics/ros2/workspaces-packages-launch|25.4 §5]]).

**pip**는 Python Package Index에서 Python 패키지를 설치한다. Ubuntu 24.04에서는 시스템 Python에 설치하기를 아예 거부한다. 파일 `/usr/lib/python3.12/EXTERNALLY-MANAGED`가 그 인터프리터를 apt의 것으로 표시하고, pip는 apt가 설치한 무언가를 덮어쓰기 전에 그렇다고 말하는 오류를 내고 멈춘다. 그 오류는 보호 장치가 제대로 도는 것이다. `sudo pip install --break-system-packages …`는 그것을 돌아가서, 기계의 모든 Python 프로그램 — apt의 도구, ROS 2의 노드와 명령 줄 도구 — 이 그것들이 대고 빌드된 버전 대신 가져다 쓸 수도 있는 자리에 패키지를 넣는다. ROS 2 자체의 안내도 길을 같은 순서로 늘어놓는다 — rosdep, 패키지 관리자, 가상 환경 — 그리고 Python 인터프리터는 ROS 2 바이너리가 빌드된 그것이어야 한다고 경고한다. 자기 분석 코드와 학습 코드를 위한 Python 패키지는 직접 만든 가상 환경에 들어가고, 그것은 이 트랙의 Python 페이지([[02-foundations/tools/python-research-code|12.3 §1]])다.

**컨테이너**는 Ubuntu 사용자 공간 전체 — 다른 릴리스, 다른 ROS 배포판, 고정한 버전들 — 를 이미지에 담아 기계의 나머지와 격리해 돌린다. 환경이 카트와 달라야 할 때, 또는 결과를 나중에 다시 돌릴 수 있도록 얼려 두어야 할 때 맞는 도구다([[04-robotics/ros2/debugging-data-reproducibility|25.10 §13]]). 로봇에서 치르는 값은 호스트의 어떤 것도 기본값으로는 들어오지 않는다는 것이다. 엔코더 보드는 `docker run --device=/dev/ttyACM0 …`처럼 이름으로 넘겨야 하고, 컨테이너가 볼 다른 모든 것도 마찬가지다.

| 필요한 것 | 설치 도구 | 이유 |
|---|---|---|
| ROS 2, 드라이버, 시스템 라이브러리 | apt, 워크스페이스에서는 rosdep을 통해 | 기계 전체에 한 버전, 모든 프로그램이 나눠 쓴다 |
| 내 코드를 위한 Python 패키지 | 가상 환경 안의 pip | apt와 ROS 2가 쓰는 인터프리터를 절대 건드리지 않는다 |
| 다른 Ubuntu나 ROS 릴리스, 또는 결과를 위해 얼린 환경 | 컨테이너 | 사용자 공간 전체가 이미지에 담겨 옮겨 다닌다 |

표 뒤의 규칙: **디스크의 각 자리는 정확히 한 도구만 쓰게 한다** — 시스템은 apt, 직접 만든 환경은 pip, 이미지는 컨테이너 — 그리고 `sudo`로 한 도구가 다른 도구의 자리에 쓰게 만들지 않는다. 이 절의 모든 고장은 두 도구가 한 디렉터리를 나눠 쓴 것이다.

### 8. 다른 기계에서 일하기: ssh, rsync, tmux

*한 문장으로:* 키를 쓴 ssh가 카트에 닿고, rsync는 바뀐 것만 복사하며, tmux는 연결이 끊겨도 실행을 살려 둔다 — 그러지 않으면 끊김이 ssh 셸의 모든 작업을 죽인다.

로봇 앞에 앉아 있는 일은 드물다. 워크스테이션에서 로봇에 로그인하고, 날마다 데이터를 복사해 오고, 자리를 비운 동안에도 실행을 걸어 둔다. ssh, rsync, tmux가 그 세 일을 맡는다.

**ssh**는 암호화된 연결로 다른 기계의 셸을 준다. `ssh robot@192.168.10.2`, 또는 호스트 별칭으로 `ssh p6`. 별칭은 `~/.ssh/config`의 항목이고, 영어 절에 실린 P6의 항목은 호스트 이름 `192.168.10.2`, 사용자 `robot`, 신원 파일 `~/.ssh/id_ed25519`, 그리고 `ServerAliveInterval 15`와 `ServerAliveCountMax 4`를 적는다. `ssh -G p6`는 연결하지 않고 이름이 무엇으로 풀리는지 찍는다. `ssh p6`가 엉뚱한 곳으로 가는 이유를 찾는 가장 빠른 길이다. `ServerAlive` 두 줄은 죽은 연결을 *보이게* 한다. 카트가 답을 멈추면 ssh는 15초마다 묻고 답 없는 요청 4번 뒤에 포기하므로, 끊긴 링크는 멈춘 터미널로 남는 대신 약 $15\times4=60$초 뒤에 세션을 끝낸다. 카트에서 무언가를 살려 두지는 않는다 — 그것은 아래의 tmux가 할 일이다.

> [!note]- 더 깊이 · Deeper
> 영어 절은 그 항목을 `ssh_config_p6`에 저장하고 노트북에서 `-F`(`~/.ssh/config` 대신 이 파일을 읽음)로 풀어, 항목이 정한 줄들만 `grep`으로 걸러 보인다. 사용자 `robot`, 호스트 이름 `192.168.10.2`, 포트 22, `serveralivecountmax 4`, `serveraliveinterval 15`, 신원 파일 `~/.ssh/id_ed25519`.

**비밀번호 대신 키.** `ssh-keygen -t ed25519`는 키 쌍을 만든다. 워크스테이션을 결코 떠나지 않는 개인 키와 `.pub` 공개 키다. `ssh-copy-id p6`는 공개 키를 카트의 `~/.ssh/authorized_keys`에 덧붙이고, 그 뒤로 `ssh p6`는 계정 비밀번호 대신 키로 로그인한다. 양쪽 끝이 모두 권한을 검사한다(4절). ssh는 다른 누가 읽을 수 있는 개인 키를 거부한다. 영어 절의 `key_demo.sh`는 노트북에서 쓰고 버릴 키를 만들고(개인 키 `-rw------- 600`, 공개 키 `-rw-r--r-- 644`), 개인 키의 모드를 644로 바꾼 뒤 다시 읽는다(출력은 가르치는 줄만 남겼다). ssh-keygen은 `Permissions 0644 for './demo_key' are too open.`을 찍고 키를 무시하며 상태 255로 끝난다. 카트의 ssh 서버도 제 쪽을 검사한다. 기본값 `StrictModes yes`로 로그인을 받기 전에 `robot`의 파일과 홈 디렉터리의 모드와 소유권을 검사한다. 그래서 다른 사용자가 쓸 수 있는 홈 디렉터리나 `~/.ssh` 하나로 키 로그인이 실패한다.

**복사.** `scp FILE p6:DIR/`은 같은 연결로 파일 하나를 복사한다. bag 디렉터리에는 `rsync -a SRC/ DEST/`가 낫고, 그 이유 셋이 rsync의 매뉴얼에 있다. 기본값으로 ssh 위에서 돈다. 목적지에 크기와 수정 시각이 이미 같은 파일은 모두 건너뛰므로, 같은 명령을 두 번 돌리면 새것만 복사한다. 그리고 중단되면 (`--partial`을 주지 않는 한) 전송하다 만 파일을 지우므로, 다시 돌려도 반쪽 파일을 온전한 파일로 착각하지 않는다. 영어 절의 `rsync_demo.sh`는 노트북에서 분할 파일 둘인 가짜 bag 디렉터리를 복사하고, 다시 복사하고, 녹화기가 셋째를 쓴 뒤에 또 복사한다. 출력의 한 줄은 rsync가 다룬 항목 하나다. `>f+++++++`는 받아서 새로 만든 파일, `cd+++++++`는 만든 디렉터리, `.d..t....`는 수정 시각이 바뀐 디렉터리다. 첫 실행은 디렉터리와 파일 셋을 새로 만들고, 둘째 실행은 달라진 것이 없어 아무것도 나열하지 않으며, 셋째 실행은 새 파일 `day1_2.mcap` 하나만 보낸다. 원본의 끝 빗금은 뜻의 일부다. `bags/day1/`는 디렉터리의 *내용*을, `bags/day1`은 디렉터리 자체를 복사해 목적지 안에 `DEST/day1/`을 만든다. 두 기계 사이에서는 같은 명령을 워크스테이션에서 `rsync -a p6:bags/day1/ ~/p6_bags/day1/`로 돌린다.

**실행 살려 두기: tmux.** ssh 셸에서 띄운 프로그램은 그 셸에 속하고, 연결이 끊기면 셸과 함께 죽는다(아래). tmux는 터미널 멀티플렉서다. 그 세션은 카트의 tmux 서버가 붙들고 있고, 매뉴얼의 말대로 ssh 시간 초과 같은 뜻밖의 끊김에도 살아남는다. 영어 절이 tmux 매뉴얼과 rosbag2의 README에서 가져와 적은 절차(노트북에는 tmux가 없어 여기서 실행하지 않음)는 이렇다. `ssh p6`로 들어가 `tmux new -s day1`로 `day1`이라는 세션을 열고, 그 안에서 `ros2 bag record … -d 1800 -o bags/day1`로 녹화를 시작하고, `C-b` 다음 `d`로 떼어 낸다. 녹화는 계속된다. 나중에 아무 새 ssh 세션에서 `tmux ls`로 세션을 보고 `tmux attach -t day1`로 다시 붙는다. `-d 1800`은 bag을 30분마다 나누고, 그것이 중단된 `rsync`가 다시 보내는 단위다.

실행을 죽이는 것은 **끊김**(hangup)이다. ssh 연결이 끊기면 그것이 제공하던 터미널이 사라지고, 커널이 그 터미널을 가졌던 셸에 SIGHUP을 보낸다. 대화형 bash는 끝나기 전에 자기가 띄운 모든 작업에, 돌고 있든 멈춰 있든, SIGHUP을 다시 보내고, 각 작업은 SIGHUP을 무시하지 않는 한 — `nohup`으로 띄운 명령처럼 — 또는 `disown`으로 셸의 작업 표에서 빠지지 않은 한 그것 때문에 죽는다. tmux 세션 안의 프로세스나 systemd가 띄운 프로세스처럼 그 셸의 작업이 아닌 프로세스는 SIGHUP을 받지 않는다. 함정은 "`&`로 띄웠으니 백그라운드에서 돌고 안전하다"는 생각이다. 백그라운드 작업도 여전히 ssh 셸의 작업이다.

그것이 얼마나 자주 하루를 날리는지는 확률이 말한다. 연결 끊김이 시간당 $\lambda$의 비율로 서로 독립적으로 온다면, ssh 셸의 작업인 $T$시간짜리 실행이 살아남을 확률은 $e^{-\lambda T}$ — 포아송 과정이 $T$시간 동안 사건을 하나도 내지 않을 확률([[02-foundations/probability|3. Probability §2]]) — 이고, 끊김이 다시 접속하는 수고만 드는 tmux 안이나 systemd 아래에서는 1이다. 시간당 $\lambda=0.1$에서 P6의 8시간 녹화는 ssh 셸의 작업일 때 $e^{-0.8}=0.449$의 확률로 살아남는다. 그런 날의 절반도 안 되는 날만 끝까지 녹화되고(계산 절, 6단계), 잃어버린 녹화는 다음 날 아침에야 드러나며 어느 로그에도 이유가 없다. 프로그램은 충돌하지 않았다. 끊겨서 죽었다.

네트워크 없이 노트북에서 이 메커니즘을 재현한다. 가상 터미널의 대화형 bash에 백그라운드 작업 둘 — 하나는 그냥, 하나는 `nohup`으로 — 을 주고, ssh 연결이 끊길 때처럼 터미널을 닫는다. 그냥 띄운 작업은 사라지고(`gone`), `nohup` 작업은 아직 돈다(`still running`).

> [!note]- 더 깊이 · Deeper
> 그 스크립트(영어 절의 `hangup_demo.py`)는 손으로 돌린다. 프로세스를 띄우므로 CI는 돌리지 않는다.

`nohup`은 프로세스를 구하지만 그것을 보는 창은 구하지 못한다. 출력은 파일로 가고 돌아올 터미널이 없다. tmux는 터미널을 지킨다. 사람 없이 돌아야 하는 것, 충돌 뒤에 다시 떠야 하는 것, 부팅 때 떠야 하는 것은 systemd의 몫이다(10절).

### 9. 장치와 고정 이름: `/dev`와 udev

*한 문장으로:* 커널은 장치를 만나는 순서대로 번호를 매기므로, 장치마다 그것이 무엇인지로부터 이름을 주고 — udev 규칙 — 그 이름을 연다.

카트에 USB 시리얼 보드가 둘이 되면, 제어기가 여는 이름이 재부팅할 때마다 다른 보드를 가리킬 수 있다 — 그리고 제어기는 아무 오류 없이 엉뚱한 바이트를 읽는다. `/dev`에는 커널이 아는 장치마다 **장치 파일**이 하나씩 있고, 프로그램은 그 파일을 열어 하드웨어에 닿는다. `ls -l`에서 문자 장치(`c`)는 시리얼 포트나 엔코더 보드처럼 바이트의 흐름을 나르고, 블록 장치(`b`)는 디스크처럼 파일시스템을 담는다. 시리얼로 말하는 USB 보드는 `/dev/ttyACM0`이나 `/dev/ttyUSB0`으로 나타나고, 그 번호는 서수다. 커널의 장치 번호 목록은 `ttyACM0`을 *첫째* ACM 모뎀, `ttyACM1`을 *둘째*라 부른다. 번호는 커널이 어느 보드를 먼저 만났는지를 말할 뿐, 그것이 어느 보드인지를 말하지 않는다.

P6의 카트에 USB 시리얼 장치를 하나 더 달아 보자. [[04-robotics/sensor-models|3.2 Sensor Models & Noise]]의 단축 IMU도 USB에 걸려 있다고 하자. 재부팅 뒤 커널이 먼저 만나는 보드가 `ttyACM0`이 되므로, `/dev/ttyACM0`으로 설정한 제어기는 어떤 아침에는 엔코더를, 어떤 아침에는 IMU를 연다. 상대 경로(1절)와 같은 결함이다. 이름이 이름 붙인 대상이 아닌 다른 무언가에 달려 있다.

**udev**는 커널이 장치를 알릴 때마다 움직이는 서비스로, 노드의 이름 링크를 만들고 노드의 그룹과 모드를 **규칙**에 따라 정한다. Ubuntu는 USB 시리얼 장치마다 고정 이름 하나를 이미 준다. `/dev/serial/by-id/` 아래의 링크로, 버스, 장치가 스스로 알리는 신원(udev의 `ID_SERIAL` 속성), 인터페이스 번호로 이름을 짓는다. 짧은 제 이름을 원하면 규칙을 쓴다. 먼저 맞출 수 있는 것 — 장치와 그 위의 모든 부모 장치, 그리고 그 속성들 — 을 읽고(`udevadm info -a -n /dev/ttyACM0`), 그다음 한 줄을 쓴다. 영어 절의 `/etc/udev/rules.d/99-p6-encoder.rules`(매뉴얼에서 가져옴, 여기서 실행하지 않음. 두 ID는 보드에 대해 `udevadm info`가 찍는 값의 자리표시다)는 `SUBSYSTEM=="tty"`이고 부모에 정해진 `idVendor`와 `idProduct`를 가진 장치에 링크 `p6-encoder`를 더하고, 그룹 `dialout`과 모드 `0660`을 준다. 이어서 `sudo udevadm control --reload`로 규칙 파일을 다시 읽고, `sudo udevadm trigger`로 장치 이벤트를 다시 재생하며, `ls -l /dev/p6-encoder`로 보드가 받은 `ttyACM`을 가리키는 링크를 확인한다. `--reload`만으로는 이미 있는 장치에 아무것도 바뀌지 않는다. 규칙은 다음 이벤트에 적용되고, 그것을 `trigger`가 재생하며, 다시 꽂기나 재부팅도 만들어 낸다. `GROUP`과 `MODE`는 Ubuntu가 `ttyACM` 장치에 주는 기본값(4절)을 다시 적은 것이어서, 규칙이 제어기가 기대는 권한까지 기록한다.

> **udev 규칙의 정의.** **udev 규칙**은 *udev가 모든 장치 이벤트마다 평가하는 규칙 파일의 한 줄*이다. 한 번 돌리는 명령이 아니라, 장치가 나타날 때마다 적용되는 맞춤 조건과 동작의 묶음이다. 세 조건이 정의한다. `==`로 쓰는 **맞춤 키**는 이벤트의 장치에 대해 모두 성립해야 한다. `SUBSYSTEM`, 커널의 이름인 `KERNEL`, 그리고 sysfs 속성(커널이 `/sys` 아래 파일로 내놓는 장치의 성질)을 *장치와 그 부모 장치들*에서 찾는 `ATTRS{…}` — USB 보드의 16진 ID인 `idVendor`와 `idProduct`는 tty가 아니라 그 USB 부모에 붙어 있다. 그다음 `=`와 `+=`로 쓰는 **할당 키**가 움직인다. `SYMLINK+=`는 `/dev` 아래에 이름을 더하고, `GROUP=`과 `MODE=`는 노드의 권한을 정한다. 그리고 규칙 파일은 **네 디렉터리에서 읽힌다** — `/usr/lib/udev/rules.d`, `/usr/local/lib/udev/rules.d`, `/run/udev/rules.d`, `/etc/udev/rules.d` — 그리고 이름의 사전순으로 함께 적용되며, `/etc`의 파일이 다른 곳의 같은 이름 파일보다 우선한다. 그래서 로컬 규칙은 기본값들 뒤에 오도록 번호를 붙인 `/etc/udev/rules.d/`의 파일이다.
>
> $$\text{kernel name}=\texttt{ttyACM}\,k,\ \ k=\text{its rank in detection order};\qquad \text{rule name}=f(\texttt{idVendor},\,\texttt{idProduct},\,\ldots)$$
>
> $k$는 커널이 이 장치보다 먼저 만난 장치들에 달려 있고, $f$는 보드가 지닌 속성에만 달려 있다. 그래서 규칙의 이름은 재부팅마다, 어느 USB 포트에서나 같고, 커널의 이름은 그렇지 않다.
>
> - **예**: 위의 규칙. 엔코더 보드가 어느 번호를 받든 `/dev/p6-encoder`가 그것을 가리킨다. 제어기의 포트 파라미터는 `/dev/p6-encoder`라고 적고, 노드의 모드는 그룹 `dialout`과 함께 `crw-rw----`로 남는다.
> - **비예**: `KERNEL=="ttyACM0", SYMLINK+="p6-encoder"`. 먼저 만난 보드 아무것에나 맞으므로, 둘의 순서가 바뀌는 재부팅 뒤에는 `/dev/p6-encoder`가 IMU를 가리킨다. 불안정한 사실에 붙인 고정 이름이다.
> - **비예**: 카트 두 대의 예비품 선반에 있는 똑같은 엔코더 보드 둘. 제조사 ID와 제품 ID가 같으니 규칙은 둘 다에 맞는다. 둘을 가르는 것은 각 보드 자신의 신원으로 짓는 `/dev/serial/by-id/` 이름이다.
> - **왜 중요한가**: 엉뚱한 시리얼 포트를 연 제어기는 실패하지 않는다. 바이트를 읽고, 잘못 읽는다.

### 10. 서비스와 로그: systemd와 journalctl

*한 문장으로:* systemd 유닛 파일은 프로그램 하나를 셸 없이, 부팅 때 어떻게 띄우고 다시 띄우고 멈출지를 적고, `journalctl`은 그것이 찍은 것을 읽는다.

터미널에서 손으로 띄운 스택은 로그아웃하면 멈추고, 충돌하면 그대로 죽어 있으며, 아침에 도착했을 때 돌고 있지 않다. **systemd**는 Ubuntu의 서비스를 부팅 때 띄우고, 도는 동안 감독하고, 종료 때 멈추는 프로그램이다. 서비스마다 **유닛 파일** 하나가 그것을 기술하고, 사람 없이 카트에서 돌아야 하는 것 — P6 스택, 야간 복사 — 은 무엇이든 유닛이어야 한다. 영어 절의 `/etc/systemd/system/p6-stack.service`(매뉴얼에서 가져옴, 여기서 실행하지 않음)가 P6의 것이다.

그 안의 줄들이 앞 절들의 고장에 하나씩 답한다. `ExecStart=`는 *셸 없이* 돈다. systemd가 줄을 스스로 단어로 나누고, 셸의 파이프, 리디렉션, `&`, 내장 명령은 하나도 지원하지 않으므로, 줄이 명시적으로 `bash -c`로 시작하지 않으면 `source`가 없다. `~/.bashrc`도 읽히지 않으므로 setup 파일을 바로 그 줄에서 source한다(5절). `ros2 launch` 앞의 `exec`는 그것이 자식으로 도는 대신 그 셸을 대체하게 하므로, launch 프로세스가 서비스의 주 프로세스가 된다. `User=robot`은 스택을 `robot`으로 돌리고, 그룹 데이터베이스가 그 계정에 주는 보조 그룹을 — `dialout`을 포함해 — 함께 주므로 엔코더가 열린다(4절). `WorkingDirectory=~`는 systemd의 기본값 `/`를 바꾼다. 그 아래에서는 1절의 모든 상대 경로가 루트를 가리킬 것이다. `WantedBy=multi-user.target`은 `systemctl enable`이 매 부팅의 시작으로 바꿔 놓는 줄이고(*타깃*(target)은 이름 붙은 부팅 단계이고, `multi-user.target`은 데스크톱 없는 보통의 시스템이다), `Wants=`/`After=network-online.target`은 네트워크가 설정될 때까지 시작을 잡아 둔다. 워크스테이션과 말하는 스택에 필요한 것이다. 영어 절의 일상 명령(매뉴얼에서 가져옴, 여기서 실행하지 않음)은 편집 뒤에 유닛 파일을 다시 읽는 `sudo systemctl daemon-reload`, 매 부팅과 지금 바로 시작하는 `sudo systemctl enable --now p6-stack.service`, 상태·주 PID·최근 로그를 보는 `systemctl status`, 이번 부팅의 유닛 로그를 따라가는 `journalctl -u p6-stack.service -b -f`, 이전 부팅의 경고 이상만 보는 `journalctl -u p6-stack.service -b -1 -p warning`, 실패 상태와 시작 계수를 지우는 `sudo systemctl reset-failed`다.

서비스의 표준 출력과 표준 오류는 systemd의 로그인 **저널**로 가므로, 표준 오류에 찍히는 노드의 `[WARN]` 줄(6절)이 리디렉션 없이 거기 있다. `journalctl -u`는 유닛 하나의 몫을 읽고, `-b`는 이번 부팅으로 제한하며, `-b -1`은 그 앞 부팅을 묻고, `-p warning`은 그 수준과 그보다 심각한 모든 것을 보여 준다.

> **systemd 서비스의 정의.** **서비스**(service)는 *systemd가 유닛 파일에 따라 띄우고, 감독하고, 멈추는 유닛*이다. 프로그램 하나를 어떻게 돌릴지의 선언이지, 그것을 돌리는 스크립트가 아니다. 네 조건이 그 동작을 정한다. **무엇이 도는가**: `ExecStart=`는 프로그램을 — 안전하게는 절대 경로로 — 부르고, 셸 없이, `User=`로, 그 사용자의 그룹과 함께, `WorkingDirectory=`(기본값 `/`)에서 돌린다. **언제**: `WantedBy=multi-user.target`과 `systemctl enable`이 매 부팅 때, `After=`가 이름 댄 것 뒤에 띄운다. **다시 띄우기**: `Restart=on-failure`면 깨끗하지 않은 종료나 깨끗하지 않은 시그널 뒤에 `RestartSec=` — 정하지 않으면 100 ms — 만큼 기다려 다시 띄우고, SIGTERM, SIGINT, SIGHUP, SIGPIPE로 끝난 것은 깨끗한 종료로 친다. 그리고 `StartLimitIntervalSec=`(10초) 안에 `StartLimitBurst=`(5번)보다 많이 시작된 유닛은 더는 시작되지 않는다. **멈추기**: `systemctl stop`은 유닛의 모든 프로세스에 SIGTERM을 보내고, `TimeoutStopSec=` — 정하지 않으면 90초 — 까지 기다린 뒤 남은 것에 SIGKILL을 보낸다.
>
> $$\text{given up}\iff B\,c<I,\qquad c=t_{\text{run}}+\texttt{RestartSec}$$
>
> $t_{\text{run}}$은 매 시도가 실패하기 전에 사는 시간, $c$는 한 시작에서 다음 시작까지의 시간, $B=5$, $I=10$초다. 그래서 다섯 주기가 간격보다 짧을 때 정확히 여섯째 시작이 간격 안에 떨어져 거부된다.
>
> - **예**: 부팅 때 스택이 엔코더 보드가 나타나기 전에 시작되고, 시작할 때마다 0.4초 뒤 오류로 끝난다(launch 파일이 제어기가 포트를 열지 못하면 launch를 끝내도록 되어 있다). 기본값 100 ms면 $c=0.5$초, $Bc=2.5$초 $<10$초. 첫 시작 2.5초 뒤의 여섯째 시작이 거부되고, 보드가 1초 뒤에 도착했는데도 카트는 놀고 있다. 위 유닛처럼 `RestartSec=3`이면 $c=3.4$초, $Bc=17$초 $>10$초. systemd는 보드가 올 때까지 계속 다시 시도한다.
> - **비예**: `ExecStart=source /opt/ros/jazzy/setup.bash && ros2 launch p6_bringup p6.launch.py`. `source`는 프로그램이 아니라 셸의 내장 명령이고 `&&`는 셸 문법이다. `bash -c`가 없으면 둘 중 어느 것도 알아들을 셸이 없고, 유닛은 첫 시작에서 실패한다.
> - **왜 중요한가**: 도착했을 때 일하고 있어야 하는 로봇은 시작 순서, 다시 띄우기 정책, 멈춤 시간 제한 — 읽을 수 있는 파일 속의 숫자 셋 — 이다.

### 11. 시간과 네트워크

*한 문장으로:* 주소, 왕복 시간, 열린 포트는 `ip`, `ping`, `ss`로 확인하고, 아무도 시계를 맞추지 않은 두 기계의 타임스탬프는 절대 비교하지 않는다.

스택이 기계 둘에 걸치면 오류 메시지 없이 실패할 수 있는 것이 셋 새로 생긴다. 두 기계가 서로 닿지 않거나, 포트가 닫혀 있거나, 시계가 어긋난다 — 그리고 마지막 것은 두 기계에 걸쳐 재는 모든 지연을 소리 없이 망가뜨린다.

**주소.** 직결 링크에서 워크스테이션은 `192.168.10.1`, 카트는 `192.168.10.2`이고 둘 다 접미사 `/24`를 단다. 앞의 24비트, `192.168.10`이 네트워크를 가리키므로 두 기계는 한 링크 위에 있고 서로 바로 닿는다. RFC 1918이 조직 내부 네트워크용으로 떼어 둔 `192.168.0.0/16` 블록의 사설 주소다. 카트에서 `ip -br addr`는 모든 인터페이스를 주소와 함께 나열하고(매뉴얼에서 가져옴, 여기서 실행하지 않음), 고정 주소는 `/etc/netplan/` 아래 netplan 파일에 적어 `sudo netplan apply`로 적용한다. `ping`은 왕복 시간을 잰다. ICMP(네트워크 자체의 제어 메시지 프로토콜) 에코 요청을 보내고 응답마다 시간을 찍는다. 영어 절은 노트북의 루프백 주소로 `ping -c 3 127.0.0.1`을 돌린다. 첫 응답이 0.069 ms이고 요약은 `min/avg/max/stddev = 0.069/0.088/0.100/0.014 ms`다(출력은 첫 응답과 요약만 남겼다). 워크스테이션에서의 `ping -c 3 192.168.10.2`가, ROS 2의 무엇을 탓하기 전에 링크를 시험하는 첫 명령이다.

**포트.** 네트워크에 봉사하는 프로그램은 번호 붙은 포트에서 기다린다. ssh 서버는 기본값으로 22번이다. 카트에서 `ss -tlnp`는 기다리는 TCP 소켓을 숫자 포트와 그것을 쥔 프로세스와 함께 나열한다(매뉴얼에서 가져옴, 여기서 실행하지 않음). ROS 2의 미들웨어는 자기 UDP 포트를 `ROS_DOMAIN_ID`로부터 고르고, 그것은 ROS 2 시스템 하나를 이루는 모든 기계에서 같아야 한다. 도입은 [[04-robotics/ros2/what-ros2-is|25.1 §5]]이고, 포트 계산과 멀티캐스트 시험은 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]에 있다.

**시계.** 모든 컴퓨터는 제 시계를 가지고, 어느 두 시계도 정확히 같은 속도로 가지 않으므로, 같게 맞춘 두 시계는 무언가가 조정하지 않는 한 벌어진다. Ubuntu 24.04는 기본값으로 systemd-timesyncd로 조정한다. Ubuntu 자체의 문서는 25.10부터 chrony가 기본값이 되었다고 적는다. `timedatectl status`는 시계가 동기화됐는지와 시간 서비스가 켜져 있는지를 말하고, `timedatectl timesync-status`는 timesyncd의 서버와 현재 오프셋을 보여 주며, chrony라면 `chronyc tracking`이 chrony가 추정한 참 시간에 대한 시스템 시계의 오프셋을 보고한다(모두 매뉴얼에서 가져옴, 여기서 실행하지 않음).

> **시계 오프셋의 정의.** 두 기계 사이의 **시계 오프셋**(clock offset) $\theta$는 *같은 순간에 두 시계가 읽는 값의 차이*다. 한 순간의 시계 한 쌍의 성질이지 어느 한 기계의 성질이 아니고, 상수도 아니다. 그것이 무엇을 하는지를 세 조건이 정한다. 기계마다 **제 시계를 가지며**, 타임스탬프는 그것을 쓴 기계의 시계를 읽은 값이다. **서로 다른 시계의 두 타임스탬프**로 계산한 시간 차이에는 $\theta$가 하나 대 하나로 들어 있다. 그리고 동기화가 없으면 $\theta$는 한 시계가 다른 시계보다 빨리 가는 비율 $\delta$(초당 초)로 **자란다**.
>
> $$\hat L=t^{B}_{\text{recv}}-t^{A}_{\text{stamp}}=L+\theta(t),\qquad \theta(t)=\theta_0+\delta\,t$$
>
> $L$은 참 지연, $t^{A}_{\text{stamp}}$는 A의 시계로 읽은 보낸 시각, $t^{B}_{\text{recv}}$는 B의 시계로 읽은 받은 시각, $\hat L$은 B가 계산하는 값이다. 그래서 두 기계에 걸쳐 잰 모든 지연은 그 순간의 오프셋만큼 정확히 틀린다.
>
> - **예**: 비전 노드가 GPU가 있는 워크스테이션으로 옮겨 가고, 카트의 제어기가 목표마다 나이를 계산한다. 08:00에 같게 맞추고 한 번도 동기화하지 않은 시계가 $\delta=20$ ppm — 교과용 숫자, 초당 20 µs — 이면 09:00에 $\theta=20\times10^{-6}\times3600=72$ ms 벌어진다. 10 ms 된 목표가 82 ms로 읽혀 70 ms 예산을 "깨고", 부호가 반대면 100 ms 늦은 목표가 28 ms로 읽혀 통과한다. 오프셋은 $0.070/(20\times10^{-6})=3{,}500$초, 한 시간이 안 되어 예산 전체를 넘는다.
> - **비예**: 카트 안의 두 노드. 두 타임스탬프가 한 시계에서 나오므로, 그 시계가 바깥 세계에 대해 얼마나 틀렸든 $\theta=0$이다. 기계 한 대를 동기화해도 그 안의 지연은 하나도 바뀌지 않는다.
> - **왜 중요한가**: P6의 70 ms 예산([[04-robotics/robot-systems-deployment|10. Robot Systems §3]])은 $|\theta|$가 그에 비해 작고 작게 유지될 때에만 두 기계에 걸쳐 확인할 수 있다. 그래서 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §5]]는 두 기계 모두에 같은 원천을 보는 chrony를 두고, 가정하지 말고 확인하라고 요구한다. NTP와 PTP가 얼마나 가까워지는지는 이 트랙의 네트워크 페이지([[02-foundations/tools/computer-networks|12.5 §10]])다.

### 대상으로 한 번 끝까지 · Worked case

P6의 로깅 교대 하루, 08:00부터 16:00까지를 고정된 숫자로 값을 매긴다. 각 단계가 규칙, 대입, 단위 붙은 숫자다. 1, 4, 6, 8절을 쓴다.

**1단계 — bag에 들어가는 초당 바이트.** bag의 페이로드는 녹화하는 토픽마다 속도 곱하기 메시지 크기로 자라고([[04-robotics/ros2/debugging-data-reproducibility|25.10 §6]]), 세 토픽이 나란히 녹화되므로 녹화기가 쓰는 양은

$$r=f_c\,s+f_v\,s+f_v\,s_{\text{img}}=200\cdot64+50\cdot64+50\cdot40{,}000=12{,}800+3{,}200+2{,}000{,}000=2{,}016{,}000\ \text{B/s}$$

각 항이 토픽 하나의 초당 메시지 수 곱하기 메시지당 바이트이기 때문이다. 시간당 7.2576 GB이고 그중 99.21%가 카메라다. P6의 예산 전체가 걸린 200 Hz 제어 토픽은 시간당 46 MB다. 이 페이지가 세는 것은 페이로드이고, bag 파일은 메시지마다 조금을 더 얹는다.

**2단계 — 디스크가 차는 때.** 디스크는 $F$바이트를 담고 $r$로 차므로

$$t_{\text{full}}=\frac{F}{r}=\frac{120\times10^{9}\ \text{B}}{2{,}016{,}000\ \text{B/s}}=59{,}523.8\ \text{s}=16.53\ \text{h}$$

다른 무엇도 그 공간을 다투지 않기 때문이다. 교대 자체는 $rT=58.06$ GB, 그 48.4%를 쓴다. 교대 둘은 3.9 GB를 남기고 들어가고 셋째는 안 들어간다 — 그러니 bag은 적어도 이틀에 한 번은 카트를 떠나야 한다. 08:00에 시작해 아무도 멈추지 않은 녹화기는 16시간 32분 뒤인 00:32에 디스크를 채우고, 그때부터 녹화기와 그 디스크에 쓰는 다른 모든 것이 실패한다. 아침마다의 점검은 `df -h /home`이다(1절). 그 1024의 거듭제곱으로 120 GB는 약 111.8로 읽힌다.

**3단계 — 워크스테이션으로의 복사.** 바이트는 8비트이고 복사는 링크의 $\eta$만큼을 내므로

$$t_{\text{copy}}=\frac{rT}{\eta R/8}=\frac{58.06\times10^{9}\ \text{B}}{0.8\times10^{9}/8\ \text{B/s}}=580.6\ \text{s}=9\ \text{min}\ 41\ \text{s}$$

교대 하루 전체에 대해서다. `rsync -a`(8절)라면 중단된 복사는 기껏해야 날아가던 파일 하나만큼 손해다. 녹화기가 `-d 1800`으로 나누므로 파일마다 $r\cdot1800=3.63$ GB이고, 다시 돌리면 그중 많아야 하나, 36.3초를 다시 보낸다. rsync가 반쪽 파일을 지우고 이미 끝난 파일을 모두 건너뛰기 때문이다.

**4단계 — 시리얼 장치의 모드.** `crw-rw---- root dialout`은 부류별로 $d_u=4+2+0=6$, $d_g=4+2+0=6$, $d_o=0$이므로

$$m=(660)_8=6\cdot64+6\cdot8+0=432$$

8진수 한 자리가 한 부류의 세 비트이기 때문이다. 제어기는 소유자 `root`가 아닌 `robot`으로 돌므로 그룹 부류가 결정한다. `dialout`에 있으면 자리 6, 읽기와 쓰기. 없으면 기타 사용자의 자리 0, `Permission denied`. 고칠 것은 새 모드가 아니라 `usermod -aG dialout robot`과 새 로그인이다(4절).

**5단계 — 야간 점검.** 로그가 한 번도 쓰이지 않은 날의 `grep ERROR p6_day2.log | wc -l`은 상태 $(s_1,s_2)=(2,0)$을 준다. `grep`은 파일을 못 찾았고 `wc`는 아무것도 세지 못했다. `pipefail`이 없으면 파이프라인은 $s_2=0$을 보고하고 점검은 "오류 0건"을 찍는다. 있으면 $s_1=2$이고 `set -e`가 스크립트를 멈춘다(6절, 패널 C). 노트북에서 `p6_check_log.sh`는 없는 파일에 1, 깨끗한 로그에 0으로 끝난다.

**6단계 — 녹화가 교대를 버틸까.** 연결 끊김은 시간당 $\lambda=0.1$로 서로 독립적으로 오므로 $T=8$시간에 대해

$$P(\text{no drop})=e^{-\lambda T}=e^{-0.8}=0.4493$$

포아송 과정이 $T$시간 동안 사건을 내지 않을 확률은 지수 대기 시간의 꼬리이기 때문이다([[02-foundations/probability|3. Probability §2]]). 그냥 ssh 셸의 작업으로 띄운 녹화기는 날의 45%만 교대 전체를 녹화한다. tmux 안에서, 또는 10절의 systemd 서비스로 띄우면 끊김은 다시 접속하는 수고 말고는 아무것도 치르게 하지 않는다(8절).

영어 절의 Python 몇 줄(CI에서 돈다)이 이 계산 전체를 다시 하고, 위의 숫자들이 그 출력이다. 초당 2,016,000바이트 = 시간당 7.2576 GB(카메라 99.21%), 08:00 뒤 59,523.8초 = 16.5344시간에 디스크 가득, 교대 58.0608 GB = 여유 공간의 48.4%, 복사 580.6초 = 9.68분, 분할 파일 하나 3.629 GB = 36.3초, 모드 660 = 432, 8시간 동안 ssh가 한 번도 끊기지 않을 확률 $e^{-0.8}=0.4493$.

### 12. 이 페이지가 다루지 않는 것

이 페이지는 연구자의 일상 리눅스가 멈추는 곳에서 멈춘다. ROS 2 자체 — setup 파일이 내보내는 것, 워크스페이스, 오버레이, bag, launch 파일 — 는 ROS 2 트랙이고, [[04-robotics/ros2/what-ros2-is|25.1 §7]]에서 시작한다. 가상 환경, `pip`, 고정한 요구 사항은 이 트랙의 Python 페이지([[02-foundations/tools/python-research-code|12.3]]), Git은 [[02-foundations/tools/git-research-code|12.2]], YAML과 MCAP을 비롯한 설정·데이터 형식은 [[02-foundations/tools/config-data-formats|12.4]], TCP·UDP·전선 위의 DDS·PTP·현장 네트워크는 [[02-foundations/tools/computer-networks|12.5]], C++ 컴파일은 [[04-robotics/ros2/cpp-for-robot-code|25.0 C++ for Robot Code]], 한 프로세스 안의 스레드와 그것이 허락하는 경쟁은 [[02-foundations/tools/concurrency|12.8]], 공유 GPU 클러스터에서 작업을 돌리는 법은 [[02-foundations/tools/gpu-clusters|12.7]], GPU 드라이버와 CUDA는 [[03-deep-learning/foundations/gpu-computing|1.4 GPU Computing for Robot Learning]]이다. 위키 어디에서도 다루지 않는 것: 다중 사용자 서버나 로봇 여러 대의 관리(사용자 관리, 백업, 방화벽, `sudoers` 정책), 짧은 스크립트를 넘는 셸 프로그래밍(배열, 함수, `trap`), 편집기, 커널과 드라이버, 그리고 실시간 커널. 실시간 커널의 한계는 [[04-robotics/ros2/from-simulation-to-hardware|25.11 §6]]이 적는다. 다음 걸음은 각 도구의 매뉴얼 페이지(1절)다.

### 읽고 나면

- [ ] 파일을 절대 경로와 상대 경로로 부르고, 터미널, 스크립트, systemd 서비스가 각각 어느 작업 디렉터리에서 시작하는지 말한다.
- [ ] 변수, 따옴표, 글롭이 든 줄에서 프로그램이 받을 인수를 예측하고, 비면 안 되는 변수를 지킨다.
- [ ] 종료 상태를 성공, 프로그램 자신의 실패, "찾지 못함", "실행 불가", 시그널로 읽고, 노드가 SIGINT와 SIGTERM에 무엇을 해야 하는지 말한다.
- [ ] 모드를 글자와 8진수로 읽고, 프로세스에 어느 부류가 적용되는지 말하고, 시리얼 장치의 *Permission denied*를 `chmod`가 아니라 그룹으로 고친다.
- [ ] 환경 변수가 어느 프로세스에 닿는지, 터미널에 왜 `source`가 필요한지, `ssh p6 'ros2 …'`, `sudo ros2 …`, 서비스는 왜 그것을 보지 못하는지 말한다.
- [ ] 표준 출력과 표준 오류를 리디렉션하고, 파이프라인으로 노드의 로그를 거르고, 옳은 이유로 실패하는 `set -euo pipefail` 스크립트를 쓴다.
- [ ] 주어진 소프트웨어에 apt, 가상 환경 안의 pip, 컨테이너 중 무엇을 쓸지 고르고, Ubuntu 24.04에서 `sudo pip install`이 왜 거부되는지 말한다.
- [ ] 키로 로그인하고, 하루치 bag을 `rsync`로 복사하고, tmux로 실행을 살려 두며, 연결이 끊기면 누가 SIGHUP을 받는지 말한다.
- [ ] udev 규칙으로 USB 장치에 고정 이름을 주고, systemd 서비스를 쓰고, 켜고, 그 로그를 읽는다.
- [ ] 하루치 로깅에 바이트, 디스크 시간, 복사 시간으로 값을 매기고, 시계 오프셋을 지연 예산과 견준다.

### 스스로 점검

1. 야간 복사용 유닛 파일에 `ExecStart=/usr/bin/rsync -a bags/ ws:p6_bags/`가 있고 `WorkingDirectory=`는 없다. `bags/`는 어느 디렉터리를 가리키며, 고치는 법 둘은 무엇인가?
2. `bagdir`가 비어 있다. `rm -rf $bagdir/*`와 `rm -rf "${bagdir:?}"/*`는 각각 무엇을 하며, `set -u`는 왜 도움이 안 되는가?
3. launch 로그가 `process has died [pid 5120, exit code -9, …]`라고 하고, 같은 종류의 죽음 뒤 스크립트의 `$?`는 137이다. 무슨 일이 있었고, 보낸 쪽은 누구일 법한가?
4. `ls -l /dev/ttyACM0`이 `crw-rw---- 1 root dialout`을 보이고 제어기는 *Permission denied*를 기록한다. 어느 부류가 적용됐고, 고치는 법은 무엇이며, 그것을 입력한 터미널에서는 왜 효과가 없는가?
5. `ssh p6` 다음의 `ros2 topic list`는 되는데 `ssh p6 'ros2 topic list'`는 `ros2: command not found`라고 한다. 왜이며, 한 줄짜리 처방은 무엇인가?
6. `ros2 run p6_control controller | grep WARN`이 경고만이 아니라 모든 로그 줄을 찍는다. 왜이며, 대신 무엇을 입력하는가?
7. `sudo systemctl stop p6-stack.service`를 돌린다. 무엇이 어느 프로세스에 가고, 90초 뒤에도 녹화기가 끝나지 않았으면 무슨 일이 일어나는가?

> [!tip]- 스스로 점검 정답 · Answers
> 1. `/bags/`다. 시스템 서비스의 작업 디렉터리는 `WorkingDirectory=`가 정하지 않는 한 `/`이고, 상대 경로는 거기서 읽힌다. 절대 경로 `/home/robot/bags/`를 쓰거나, `User=robot`과 함께 `WorkingDirectory=~`를 더한다.
> 2. 첫째는 `rm -rf /*`, 곧 루트의 모든 항목으로 확장된다. 둘째는 `rm`이 돌기 전에 오류를 내고 멈춘다. `:?`가 비었거나 설정되지 않은 변수를 거부하기 때문이다. `set -u`는 한 번도 설정되지 않은 변수에만 반대하고, 빈 변수는 통과시킨다.
> 3. 프로세스가 SIGKILL, 시그널 9로 죽었다. Python의 subprocess 기구는 그것을 −9로, bash는 $128+9=137$로 보고한다. SIGKILL은 잡을 수 없으므로 프로그램은 정리할 기회가 없었다. 보낸 쪽으로는 노드가 끝내지 못한 종료가 10초째에 이른 `ros2 launch` 자신, 또는 90초의 멈춤 시간 제한 뒤의 systemd가 그럴 법하다.
> 4. 소유자는 `root`이고 제어기는 `robot`으로 돌므로 소유자 부류는 해당하지 않는다. `robot`은 `dialout`에 없으므로 기타 부류, 자리 0, 접근 불가가 적용된다. 처방은 `sudo usermod -aG dialout robot`과 새 로그인이다. 프로세스의 그룹은 시작할 때 정해지고 그것이 띄우는 모든 것이 물려받으므로, `usermod`를 입력한 터미널과 거기서 띄운 노드는 옛 목록을 지닌다. 새 ssh 세션이 새 목록을 읽는다.
> 5. `ssh p6 'command'`는 비대화형 bash를 돌리고, Ubuntu의 기본 `~/.bashrc`는 비대화형 셸이면 첫 줄들에서 돌아가 버리므로, 끝에 있는 `source /opt/ros/jazzy/setup.bash` 줄은 끝내 돌지 않는다. 명령 안에서 source한다. `ssh p6 'source /opt/ros/jazzy/setup.bash && ros2 topic list'`.
> 6. ROS 2는 로그 줄을 표준 오류에 쓰고 파이프는 표준 출력만 나르므로, 줄들이 `grep`을 비켜 걸러지지 않은 채 터미널에 닿는다. `ros2 run p6_control controller 2>&1 | grep WARN`을 입력한다(카트처럼 bash 4 이상이면 `|&`).
> 7. 유닛의 모든 프로세스 — launch 프로세스와 그것이 띄운 노드 하나하나 — 에 SIGTERM과 이어서 SIGCONT가 간다. SIGTERM을 처리하는 노드는 스스로 끝난다. `TimeoutStopSec=`, 기본값 90초 뒤에도 돌고 있는 것은 SIGKILL을 받고, 그렇게 죽은 녹화기는 끝나지 않은 파일을 남긴다.

### 과제 · Problem set

Tier B. 이 페이지와 선수 지식, [[02-foundations/lab-plants|0.6 Lab Plants]]의 **P6**만 쓴다. 대상은 같은 컴퓨터이고, 모든 문제가 손잡이 하나 — 프레임 크기, 디스크, 링크, 그룹 목록, 다시 띄우기 지연, 시계의 속도 — 를 바꾸므로 페이지의 어떤 숫자도 그대로 옮길 수 없다.

1. **그리기.** 바뀐 하루의 그림. 카메라 스트림을 덜 압축해 $s_{\text{img}}=60{,}000$바이트, 카트는 08:00에 $F=200$ GB가 비어 있고, 복사는 이더넷 대신 현장 Wi-Fi로 실효 20 MB/s다. 패널 A의 링크와 녹화기 라벨, 그리고 패널 B를 같은 척도로 다시 그린다 — 속도, 16:00의 교대 바이트, 디스크가 차는 시각 — 그리고 Wi-Fi와 이 페이지의 이더넷 두 경우의 복사 시간을 적는다. 교대 하루가 여전히 들어가는가, 그 복사가 45분 점심시간 안에 끝나는가?
2. **유도.** (a) 두 번째 보드가 `crw-rw---- root dialout`인 `/dev/ttyUSB0`으로 나타나고, `robot`의 그룹은 `robot`과 `video`다. 제어기에 어느 부류가 적용되고, 읽기·쓰기용 `open()`은 무엇을 돌려주는가? 소유자는 읽고 쓰고, 그룹은 읽기만 하고, 나머지는 아무것도 못 하는 모드를 글자, 8진수, 10진수로 쓰고, `sudo chmod`가 오래가는 처방이 아닌 이유를 말하라. (b) 각 파이프라인이 `pipefail` 없이와 있을 때 보고하는 상태를 대라. (i) 이 페이지의 1일째 로그에 대한 `grep -c ERROR p6_day1.log | sort`, (ii) 오류 없는 로그에 대한 `grep ERROR p6_clean.log | wc -l`, (iii) `p6_day2.log`가 없을 때의 `grep ERROR p6_day2.log | grep -c controller`. 셋 중 `pipefail`이 틀리게 보고하는 것은 무엇이며 왜인가? (c) 워크스테이션이 현장 Wi-Fi로 옮겨 가 시간당 $\lambda=0.25$로 끊기고, 녹화는 ssh 셸의 작업으로 12시간 돈다. 살아남을 확률과 첫 끊김까지의 평균 시간은? (d) 이제 보드가 없는 동안 스택이 시작할 때마다 1.2초 뒤에 끝난다. 기본 `RestartSec=`이면 systemd는 언제 포기하는가? 결코 포기하지 않게 하는 가장 작은 `RestartSec=`은? (e) 두 기계의 시계를 같게 맞추고 한 번도 동기화하지 않았으며 $\delta=50$ ppm이다. 오프셋은 언제 P6의 70 ms 예산을 넘고, 2시간 뒤 참 나이가 30 ms인 목표에 카트는 어떤 나이를 계산하는가?
3. **해석.** 동료의 시작 스크립트다. 재부팅할 때마다 워크스테이션의 ssh 세션에서 손으로 돌린다(`ssh robot@192.168.10.2` 다음 `./start_p6.sh`). 영어 절에 실린 `start_p6.sh`는 읽으라고 둔 것이지 돌리라고 둔 것이 아니며, 여기서 실행하지 않았다. 모든 실수를 대고, 그것이 카트에서 낳는 증상과 처방을, 그것을 설명하는 절과 함께 말하라.

> [!note]- 그리는 법 · How to draw it
> - **패널 A는 네트워크가 아니라 기계다.** 카트를 systemd, 세 프로그램, 그리고 그것들이 만지는 두 가지 — 모드·소유자·그룹을 단 장치 파일, 여유 공간을 단 디스크 — 를 담은 상자 하나로 그리고, 워크스테이션은 그 밖에 두어, 공칭 속도와 복사가 내는 속도를 적은 링크 하나로 잇는다.
> - **장치에는 두 이름을 모두 단다.** 제어기가 여는 고정 이름과 그것이 가리키는 커널의 이름이다. 모드는 글자와 8진수로 쓴다. 가장 먼저 실패하는 것이 권한이므로 권한이 그림의 일부다.
> - **패널 B는 같은 척도로 그린 직선이다.** 가로축은 녹화 시작부터 다음 날 같은 시각까지의 시각을 시간당 일정한 픽셀로, 세로축은 여유 공간까지의 사용 GB로 둔다. 직선의 기울기는 GB/h 단위의 $r$이고, 맨 위에 $F/r$에서 닿으며 그곳에서 디스크가 가득 찬다.
> - **교대가 끝나는 곳을 직선 위에 표시하고** 그 GB를 적은 뒤, 곁에 복사 시간을 쓴다. 누가 집에 가기 전에 그날이 치러야 할 유도 숫자 하나다. 링크가 바뀌면 그 라벨만 바뀐다.
> - **디스크가 찬 뒤에는 직선을 점선으로 평평하게 긋고** 그 시각을 적는다. 켜 둔 채 잊힌 녹화기는 사고가 아니라 기본 결과다.
> - **패널 C는 단계마다 아래에 상태를 적은 파이프라인이고**, 그 밑에 `$?`의 두 읽기를 적는다. 이 과제에서는 바뀌지 않는다. 명령을 바꿀 때만 다시 그린다.

> [!tip]- 정답 · Solutions
> 1. $r=12{,}800+3{,}200+50\cdot60{,}000=3{,}016{,}000$ B/s $=10.8576$ GB/h이고 그중 99.47%가 카메라다. 교대는 $10.8576\times8=86.86$ GB, 200 GB의 43.4%를 쓰므로 교대 하나는 넉넉히 들어가고, 둘도 들어가며($173.7$ GB), 셋째는 안 들어간다. 디스크는 $200\times10^9/3{,}016{,}000=66{,}313$초 $=18.42$시간 뒤, 다음 날 02:25에 찬다. 복사는 Wi-Fi로 $86.86\times10^9/(20\times10^6)=4{,}343$초 $=72.4$분 — 점심시간보다 길다 — 이고, 100 MB/s의 이더넷으로는 $868.6$초 $=14.5$분이다. 시간당 20 px, GB당 1 px의 그림에서 직선은 시간당 10.86 px씩 오르고, 시작에서 $x=18.42\times20=368$ px 떨어진 곳에서 200 GB 높이에 닿는다.
> 2. (a) 소유자는 `robot`이 아닌 `root`이고, 그룹 `dialout`은 `robot`과 `video` 사이에 없으므로 기타 부류, 자리 0이 적용되어 `open()`은 *Permission denied*로 실패한다. 모드는 `rw-r-----`, $(640)_8=6\cdot64+4\cdot8+0=416$이다. `chmod`가 바꾼 노드는 다음 부팅이나 다시 꽂기 때 udev가 규칙의 모드로 새로 만든다. 오래가는 처방은 `dialout`에 든 `robot`, 또는 규칙의 `GROUP=`/`MODE=`다. (b) (i) $(0,0)$. 둘 다 0 — `grep`은 3을 셌다. (ii) $(1,0)$. 없으면 0, `pipefail`이면 1 — `grep`의 1은 "고른 줄 없음"일 뿐이니 헛경보다. (iii) $(2,1)$. 둘째 `grep`은 아무것도 읽지 못해 아무것도 고르지 못했으므로 1로 끝난다. 파이프라인은 `pipefail` 없이 1(마지막 명령), 있어도 1(가장 오른쪽 실패)을 보고하고, 없는 파일의 2는 어느 쪽으로도 가려진다. `pipefail`은 *그* 실패가 아니라 *어떤* 실패를 보고한다. 노트북에서 돌린 `PIPESTATUS`는 `0 0`, `1 0`, `2 1`이었다. (c) $e^{-0.25\times12}=e^{-3}=0.0498$. 스무 번에 한 번꼴로만 살아남고, 첫 끊김은 평균 $1/\lambda=4$시간 뒤에 온다. (d) $c=1.2+0.1=1.3$초, $5c=6.5$초 $<10$초. 첫 시작 6.5초 뒤의 여섯째 시작이 거부된다. $5c\ge10$초, 곧 $c\ge2$초이고 `RestartSec`$\ge0.8$초면 결코 포기하지 않는다. 경계에서 멀도록 1초 이상을 잡는다. (e) $0.070/(50\times10^{-6})=1{,}400$초 $=23.3$분. 2시간 뒤 $\theta=50\times10^{-6}\times7{,}200=0.36$초이므로 목표는 $30+360=390$ ms 된 것으로 읽힌다 — 부호가 반대면 $30-360=-330$ ms, 동기화된 시계 한 쌍이라면 결코 만들 수 없는 나이, 미래에서 온 목표다.
> 3. *3번째 줄* `sudo pip install pyserial`: Ubuntu 24.04는 제 Python을 외부 관리로 표시하므로 pip가 오류를 내며 거부한다. `--break-system-packages`로 강행하면 apt와 ROS 2의 Python이 가져다 쓰는 자리에 패키지를 넣는다. 처방: 의존성을 rosdep에 선언하고 apt로 설치한다(7절). ROS가 아닌 코드라면 가상 환경([[02-foundations/tools/python-research-code|12.3]]). *4번째 줄* `bash …/setup.bash`: setup이 끝나 버리는 자식 셸에서 돌므로 워크스페이스는 끝내 source되지 않는다. 6번째 줄은 `p6_bringup`을 찾지 못하고, ssh 셸도 ROS 2를 source하지 않았다면 5–6번째 줄이 모두 `ros2: command not found`를 찍는다. 처방: `source`(5절). *5–6번째 줄*, ssh 세션에서 돌린 스크립트의 `&` 작업: 워크스테이션이 잠들거나 연결이 끊기면 스크립트 전체가 끊겨 녹화가 교대 도중에 끝나고, 어디에도 오류가 없다(8절). 그리고 그 작업들은 SIGINT를 무시하므로 `kill -INT`로 멈추려 해도 아무 일이 없다(3절). 처방: systemd 서비스(10절), 적어도 tmux. *6번째 줄* `encoder_port:=/dev/ttyACM0`: 커널의 이름이므로 IMU를 먼저 만난 아침에 제어기가 IMU를 연다. 처방: udev 규칙과 `/dev/p6-encoder`(9절). *8번째 줄*: `set -euo pipefail`이 없고, 노드는 로그를 `~/p6_logs/day1.log`가 아니라 표준 오류와 ROS 2 자신의 로그 파일에 쓴다. `grep`은 2로 끝나고 `wc`는 0을 쓰며, 보고서는 날마다 오류 0건이라고 말한다. 처방: `set -euo pipefail`, 스택의 표준 오류를 붙잡거나 서비스의 저널을 읽고, `p6_check_log.sh`의 방식으로 센다(6절). 그리고 빠진 것: 끝에 녹화기를 멈추는 것이 없으므로 디스크가 00:32에 찬다(계산 절, 2단계).

### 출처

영어 절의 출처 목록과 같다.

- GNU Bash 참조 매뉴얼([gnu.org](https://www.gnu.org/software/bash/manual/html_node/index.html)) — 확장과 인용, `${var:?}`, 종료 상태(126, 127, $128+n$), 파이프라인과 `pipefail`, `set -e`/`-u`, 스크립트의 시그널, 작업들에 다시 보내는 SIGHUP.
- bash(1)([man7.org](https://man7.org/linux/man-pages/man1/bash.1.html)), Ubuntu 24.04의 bash 5.2.21([packages.ubuntu.com](https://packages.ubuntu.com/noble/bash))과 기본 `~/.bashrc`([skel.bashrc](https://git.launchpad.net/ubuntu/+source/bash/tree/debian/skel.bashrc?h=ubuntu/noble)) — sshd가 띄운 셸을 포함한 시작 파일, 비대화형 셸에서 바로 돌아가는 첫 줄.
- POSIX 셸 명령 언어([pubs.opengroup.org](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/V3_chap02.html))와 유틸리티 [jobs](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/jobs.html), [fg](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/fg.html), [bg](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/bg.html), [ls](https://pubs.opengroup.org/onlinepubs/9799919799/utilities/ls.html) — 리디렉션 순서, `exec`, `export`, 작업 제어, 파일 종류 글자.
- GNU Coreutils의 [Mode Structure](https://www.gnu.org/software/coreutils/manual/html_node/Mode-Structure.html) — 파일과 디렉터리에서의 읽기, 쓰기, 실행.
- 리눅스 매뉴얼 페이지([man7.org](https://man7.org/linux/man-pages/)) — signal(7), termios(3), credentials(7), initgroups(3), path_resolution(7), umask(2), hier(7), man-pages(7), usermod(8), proc_pid_comm(5), ps(1), pgrep(1), kill(1), nohup(1), chmod(1), stat(1), df(1), du(1), grep(1), sort(1), uniq(1), wc(1), stdin(3), ip(8), ss(8), ping(8), timedatectl(1). 1–6절과 11절의 명령과 커널 사실.
- systemd 매뉴얼 페이지([man7.org](https://man7.org/linux/man-pages/)) — systemd.service(5), systemd.unit(5), systemd.exec(5), systemd.kill(5), systemd-system.conf(5), systemd.special(7), systemctl(1), journalctl(1), journald.conf(5), systemd-journald.service(8), udev(7), udevadm(8). 9절의 규칙과 10절의 시작·다시 띄우기·멈추기·저널.
- systemd 소스([github.com/systemd/systemd](https://github.com/systemd/systemd)) — [50-udev-default.rules.in](https://github.com/systemd/systemd/blob/main/rules.d/50-udev-default.rules.in)(시리얼 장치의 `dialout`), [60-serial.rules](https://github.com/systemd/systemd/blob/v255/rules.d/60-serial.rules)(`/dev/serial/by-id`), [udev-node.c](https://github.com/systemd/systemd/blob/v255/src/udev/udev-node.c)(그룹이 있으면 0660). Ubuntu 24.04는 systemd 255.4를 싣는다([packages.ubuntu.com](https://packages.ubuntu.com/noble/systemd)).
- 리눅스 커널 문서 — [devices.txt](https://github.com/torvalds/linux/blob/master/Documentation/admin-guide/devices.txt)(`ttyACM0`은 첫째 ACM 모뎀), [sysfs-bus-usb](https://github.com/torvalds/linux/blob/master/Documentation/ABI/testing/sysfs-bus-usb)(`idVendor`, `idProduct`).
- OpenSSH 매뉴얼([man.openbsd.org](https://man.openbsd.org/)) — ssh(1)의 `-G`, ssh_config(5)의 `ServerAlive*`, sshd_config(5)의 `StrictModes`, scp(1). ssh-copy-id(1)와 [session.c](https://github.com/openssh/openssh-portable/blob/master/session.c)(로그인 때 그룹을 읽음).
- tmux(1)([man.openbsd.org](https://man.openbsd.org/tmux.1)) — ssh 시간 초과를 견디는 세션, `new -s`, `attach -t`, `C-b d`.
- rsync(1)([download.samba.org](https://download.samba.org/pub/rsync/rsync.1)) — 끝 빗금, 빠른 검사, 지워지는 반쪽 파일.
- sudoers(5)([sudo.ws](https://www.sudo.ws/docs/man/sudoers.man/)) — `env_reset`, `secure_path`.
- apt(8)([manpages.debian.org](https://manpages.debian.org/bookworm/apt/apt.8.en.html)) — 스크립트에는 `apt-get`. PEP 668([peps.python.org](https://peps.python.org/pep-0668/))과 Ubuntu의 [libpython3.12-stdlib 파일 목록](https://packages.ubuntu.com/noble/amd64/libpython3.12-stdlib/filelist) — `EXTERNALLY-MANAGED` 표시 파일. Docker run 참조([docs.docker.com](https://docs.docker.com/reference/cli/docker/container/run/)) — `--device`.
- Python 문서 — [subprocess](https://docs.python.org/3/library/subprocess.html)와 [asyncio 서브프로세스](https://docs.python.org/3/library/asyncio-subprocess.html). 시그널 $N$으로 죽으면 반환 코드 $-N$.
- ROS 2 문서, jazzy([github.com/ros2/ros2_documentation](https://github.com/ros2/ros2_documentation/tree/jazzy)) — 환경 설정, Ubuntu 설치, 표준 오류로 가는 콘솔 로그와 그 형식, Python 패키지 설치.
- ROS 2 소스, jazzy — [rclcpp utilities.hpp](https://github.com/ros2/rclcpp/blob/jazzy/rclcpp/include/rclcpp/utilities.hpp)와 [rclpy `__init__.py`](https://github.com/ros2/rclpy/blob/jazzy/rclpy/rclpy/__init__.py)(SIGINT·SIGTERM 핸들러), [launch execute_local.py](https://github.com/ros2/launch/blob/jazzy/launch/launch/actions/execute_local.py)와 [osrf_pycommon](https://github.com/osrf/osrf_pycommon)(5초 + 5초 종료, "process has died"), [rosbag2 README](https://github.com/ros2/rosbag2/blob/jazzy/README.md)(`--topics`, `-d`, MCAP).
- Ubuntu Server의 [About time synchronisation](https://ubuntu.com/server/docs/explanation/networking/about-time-synchronisation/) — timesyncd, 25.10부터 chrony. [chronyc(1)](https://chrony-project.org/doc/4.6/chronyc.html) — `tracking`. [Netplan](https://netplan.readthedocs.io/en/stable/using-static-ip-addresses/) — 고정 주소. RFC 1918([rfc-editor.org](https://www.rfc-editor.org/rfc/rfc1918.html)) — 사설 주소.
