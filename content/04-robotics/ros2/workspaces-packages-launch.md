---
title: "25.4 Workspaces, Packages, Builds and Launch"
tags: [robotics, ros2, systems]
study-depth: Working
wiki-support: Working
depth-goal: "Build a two-package workspace with colcon, start both nodes from one launch file with parameters loaded from YAML, and prove which copy of your code a running node is actually executing."
mastery-when: "Go deeper when you are packaging for release, writing CMake for a library other people link against, or building cross-compiled or containerised workspaces for a fleet."
---

## English

> [!abstract] Depth target · 깊이 목표
> **Working** — enough to run the daily edit–build–source–launch loop without losing an afternoon to it, and to diagnose the two failures it produces. Not enough to package for a ROS distribution release.
> **Working** — 매일 반복하는 편집–빌드–source–launch 루프를 반나절 잃지 않고 돌리고, 그 과정에서 나오는 두 가지 고장을 진단할 정도. 배포판 릴리스용 패키징까지는 아니다.

> [!note] Prerequisites · 선수 지식
> A machine running **ROS 2 Jazzy Jalisco on Ubuntu 24.04** with the environment set up as in [[04-robotics/ros2/index|25. ROS 2]], and nodes you can already write and run, as in [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]. Parameters are used here as a thing to configure; what they are is [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]].
> **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 환경, 그리고 이미 노드를 쓰고 실행할 수 있는 상태. 파라미터는 여기서 "설정하는 대상"으로만 쓴다.

### 1. Why a build step exists at all

Python does not need to be compiled. So a reasonable first question is why a Python ROS 2 node cannot just be run with `python3 my_node.py`.

It can, for one file in one terminal. What it will not do is let `ros2 run` find the executable by package name, let a launch file in another package refer to it, let `rosdep` know what to install, let a C++ node find the message type it publishes, or let anyone else build it from a clone.

All of that comes from one idea: a **package** declares what it is and what it needs, and a **build** turns that declaration into a fixed directory layout that the ROS 2 tooling knows how to search. The cost is that there is now a copy of your code somewhere other than where you edit it. Section 13 is about the day that copy goes stale.

### 2. The workspace: `src`, `build`, `install`, `log`

A workspace is a directory containing ROS 2 packages. You create it by hand — there is no `ros2 workspace create`:

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

Packages go in `src`, one directory each, never nested inside one another. After the first build you have four directories:

| Directory | Written by | What is in it | Safe to delete |
|---|---|---|---|
| `src` | you | the only thing you edit; the only thing in version control | no |
| `build` | colcon | per-package intermediate artefacts — CMake caches, object files, `.egg-info` | yes |
| `install` | colcon | the result: executables, Python modules, `share/` data, and the setup files you source | yes |
| `log` | colcon | the full output of every build, including the one whose errors scrolled past | yes |

Two habits follow. Put `build/`, `install/` and `log/` in `.gitignore`; and when a build behaves impossibly, `rm -rf build install log` and rebuild — it is cheap and removes an entire class of question.

`log` is the one beginners ignore. `colcon build` prints a summary, not compiler output; the full output per package is under `log/latest_build/<package>/`. Or use `colcon build --event-handlers console_direct+`, which streams it to the terminal.

### 3. What `colcon build` actually does

`colcon` is the build *tool*. Run from the workspace root:

```bash
cd ~/ros2_ws
colcon build
```

```text
Starting >>> temp_sim
Finished <<< temp_sim [1.21s]
Starting >>> temp_filter
Finished <<< temp_filter [4.87s]

Summary: 2 packages finished [6.20s]
```

Four things happened, in this order:

1. **Discovery.** colcon walked `src` looking for `package.xml` files. A directory containing a `COLCON_IGNORE` file is skipped — which is how repositories ship packages you are not meant to build.
2. **Ordering.** It read the dependency tags in each `package.xml` and built a graph. Unrelated packages build in parallel; a package waits for the ones it depends on. This is the first practical reason to declare dependencies honestly: undeclared ones make the build order luck, and luck that holds on your machine fails on a colleague's parallel build.
3. **Per-package build**, dispatched by the package's declared build type — CMake for `ament_cmake`, setuptools for `ament_python`.
4. **Install.** Each package's artefacts are copied into `install/<package_name>/`, and colcon generates the environment setup files alongside them.

Note step 4. By default, **install means copy**. The file the node runs is not the file you edited.

### 4. ament, and the two build types

`ament` is the build *system* — the CMake macros and Python conventions that say where a package's outputs go; colcon is the tool that invokes it. colcon decides *what* and *when*, ament decides *where*. Two build types are officially supported:

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 temp_sim
ros2 pkg create --build-type ament_cmake  --license Apache-2.0 temp_filter
```

An `ament_python` package is a setuptools package with ROS metadata bolted on. Its minimum contents are `package.xml`, `setup.py`, `setup.cfg`, `resource/<package_name>` (a marker file that makes the package discoverable through the ament index), and a directory named after the package containing `__init__.py`. Executables come from `entry_points`:

```python
entry_points={
    'console_scripts': [
        'sensor = temp_sim.sensor:main',
    ],
},
```

and `setup.cfg` is what makes `ros2 run` able to find them, because it redirects the generated scripts into the place ament looks:

```ini
[develop]
script_dir=$base/lib/temp_sim
[install]
install_scripts=$base/lib/temp_sim
```

An `ament_cmake` package is a CMake project. Its minimum contents are `package.xml`, `CMakeLists.txt`, `src/`, and `include/<package_name>/`. The executable and its install rule are explicit:

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(filter src/filter.cpp)
ament_target_dependencies(filter rclcpp std_msgs)

install(TARGETS filter DESTINATION lib/${PROJECT_NAME})

ament_package()
```

`DESTINATION lib/${PROJECT_NAME}` is the same location `setup.cfg` pointed at above. That is the convention `ros2 run <package> <executable>` searches, and it is why both languages are addressed identically from the command line.

**When a package needs both.** Message, service and action definitions can currently only be generated from a CMake package: `rosidl_generate_interfaces()` is a CMake macro. So a package that defines its own interfaces *and* contains Python nodes cannot be `ament_python`. The documented way out is an `ament_cmake` package that also calls `ament_cmake_python`, whose `ament_python_install_package()` macro installs a Python package from CMake. The other way out — and the one worth preferring — is two packages: `my_robot_interfaces` (`ament_cmake`, definitions only) and `my_robot_nodes` (`ament_python`). Interface packages that contain nothing but definitions are cheap for other people to depend on.

### 5. `package.xml`, dependency tags, and rosdep

`package.xml` is the declaration. It carries the name, version, maintainer, licence, the build type in an `<export>` block, and the dependencies. The dependency entries are called **rosdep keys** and there is a specific tag for each phase of a package's life:

| Tag | Meaning | Typical use |
|---|---|---|
| `<depend>` | needed at both build and run time | C++ dependencies, when in doubt |
| `<build_depend>` | needed only to build | a header-only tool used during compilation |
| `<build_export_depend>` | needed by packages that build against yours | your public header includes theirs |
| `<exec_depend>` | needed only at run time | Python dependencies, launch files, message runtime |
| `<test_depend>` | needed only by tests | linters, `python3-pytest` |

The distinction that beginners get wrong: a pure Python package has no build phase, so it should use `<exec_depend>`, not `<depend>`. A C++ package almost always wants `<depend>`.

A key is either the name of a package released into the ROS ecosystem (`rclpy`, `std_msgs`, `nav2_bt_navigator`) or a system-library key from the rosdistro index — `rosdep/base.yaml` for apt packages, `rosdep/python.yaml` for Python ones. `doxygen` is a key; `libdoxygen-dev` is not.

Those keys are what this command consumes, run once from the workspace root before a build:

```bash
rosdep install --from-paths src --ignore-src -r -y
```

It walks every `package.xml` under `src`, resolves each key to a package name for this operating system, and installs the missing ones with `apt`. The flags, individually:

- `--from-paths src` — the directory to scan for `package.xml` files.
- `--ignore-src` — do not try to install a dependency that is itself a package in this workspace. Without it, rosdep would install the released binary of a package you are about to build from source, and you would then have two of it.
- `-r` — continue despite errors instead of stopping on the first key that fails to resolve. Useful, and also a way to hide a real problem: check the output for unresolved keys rather than trusting the exit code.
- `-y` — answer yes to apt.

rosdep is not a package manager; it is a mapping from a platform-independent key to whatever apt calls that thing on Ubuntu 24.04. It needs `sudo rosdep init` and `rosdep update` once before first use.

### 6. Underlay, overlay, and sourcing order

Your ROS 2 installation at `/opt/ros/jazzy` is a workspace too. When you source your own workspace on top of it, yours is the **overlay** and the installation is the **underlay**. The rule is:

> Your underlay must contain the dependencies of all the packages in your overlay, and packages in your overlay override packages in the underlay.

Sourcing order follows from that: underlay first, overlay second.

```bash
source /opt/ros/jazzy/setup.bash      # underlay
source ~/ros2_ws/install/setup.bash   # overlay
```

There are two setup files in an install directory and the difference matters. `local_setup.bash` adds only the packages in *this* workspace. `setup.bash` adds this workspace *and* the underlay it was built against. So sourcing `/opt/ros/jazzy/setup.bash` followed by the workspace's `local_setup.bash` is equivalent to sourcing the workspace's `setup.bash` alone.

Two rules that are not obvious and cost real time:

- **Do not build in a terminal that has an overlay sourced, and do not source an overlay in the terminal you built in.** The official tutorial is explicit that this creates complex problems. The mechanism is that a build inherits an environment that already points at its own previous output, so a package can be built against a stale copy of itself. Use one terminal to build and other terminals to run.
- **Overriding a package that other packages depend on is a trap.** Packages in the underlay were compiled against the underlay's version and will be run against yours; if the override changes an ABI, the failure is a crash with no sensible message. Overlays are safest on leaf packages.

To ask which one won, use:

```bash
ros2 pkg prefix temp_sim
```

```text
/home/you/ros2_ws/install/temp_sim
```

If that prints `/opt/ros/jazzy`, the shell is not seeing your workspace, and nothing you do to your source will change what runs.

### 7. `--symlink-install`, and exactly what it buys

```bash
colcon build --symlink-install
```

The flag tells colcon to use symlinks instead of copying files from the source and build directories *where possible*. For an `ament_python` package, colcon runs setuptools' `develop` step rather than `install`, so the installed module resolves back to the file in `src`. Edit the Python file, restart the node, and the change is live — no rebuild.

What it does not do:

- **It does not help compiled C++.** A symlink to a `.cpp` file is not an executable. The artefact that runs is the binary, and producing a new binary means compiling. `--symlink-install` on an `ament_cmake` package still symlinks *installed data files* — launch files, YAML, URDF, RViz configs installed with `install(DIRECTORY ...)` — which is genuinely useful, but the C++ itself needs `colcon build` every time.
- **It does not cover structural changes, in any language.** A new entry point in `setup.py`, a new file added to `data_files`, a renamed module, a new dependency in `package.xml`: all of those change what gets installed, and all of them need a rebuild. The symlink only keeps an *existing* installed path pointing at a live file.
- **It is not a mode you can half-apply.** Alternating between `colcon build` and `colcon build --symlink-install` in one workspace leaves a mix of copies and symlinks. Pick one per workspace; if you switch, delete `build` and `install` first.

The mental model worth keeping: without the flag, `install/` is a photograph of `src/`. With it, and for Python only, `install/` is a window onto `src/`.

### 8. Building less than everything

A full `colcon build` on a workspace containing Nav2 or MoveIt takes long enough to break your concentration. Two selection flags:

```bash
colcon build --packages-select temp_filter            # exactly this package, nothing else
colcon build --packages-up-to temp_filter             # this package and its recursive dependencies
```

`--packages-select` is what you want during a tight edit loop on one package whose dependencies have not changed. `--packages-up-to` is what you want after pulling someone else's changes, or the first time you build a package that depends on others in the same workspace.

The failure mode of `--packages-select` is silent staleness: you changed a message definition in package A, rebuilt only B, and B is still compiled against the old definition. When the symptom is a type or serialisation error that makes no sense given the source, drop the flag. Related: `--continue-on-error` keeps building unrelated packages after one fails, turning a 20-package build into one list of errors instead of a sequence of one-at-a-time discoveries.

### 9. Why launch files exist

Starting nodes by hand does not scale past about three, for specific reasons:

1. **Arity.** A real system is ten to fifty processes. Ten terminals is not a user interface.
2. **Configuration.** Each node needs parameters, remappings and a namespace; typing those as `--ros-args` flags is error-prone and unrecorded.
3. **Reproducibility.** The command you typed at 2am is not in version control. A launch file is.
4. **Supervision.** The launch system monitors the processes it started and reacts when one dies. A pile of terminals does not.

A launch file is a *description* of a system, executed by the `launch` framework with ROS-specific actions from `launch_ros`. It can be written in Python, XML or YAML; the three are functionally equivalent. Python is used here because it is the only one in which you can compute something.

### 10. A Python launch file: description, actions, substitutions

Three concepts, and they map onto three things in the file.

A **launch description** is what the file returns: a function named `generate_launch_description()` returning a `LaunchDescription` object. The launch system imports the file and calls that function; nothing else in the file is special.

**Actions** are the entries in the list — things to do. `Node` (from `launch_ros.actions`) starts a ROS node. `DeclareLaunchArgument` declares an argument the file accepts. `IncludeLaunchDescription` pulls in another launch file. `GroupAction` scopes a set of actions.

**Substitutions** are values resolved at execution rather than when the file is written. This is the part that surprises people: a launch file is evaluated in two phases, so ordinary Python string operations do not work on a launch argument. `LaunchConfiguration('target_frame')` is not a string, it is an object that will become one; `FindPackageShare('temp_sim')` resolves to that package's `share` directory in whichever workspace won, and `PathJoinSubstitution([...])` joins paths made of such objects.

The minimal shape:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim',
        ),
    ])
```

`package` and `executable` are what `ros2 run` would take. `name` overrides the node name it was given in code, and `namespace` prefixes it. Launch it with:

```bash
ros2 launch <package_name> <launch_file_name>
```

Two flags worth knowing before you need them: `ros2 launch -s <pkg> <file>` prints the arguments the launch file accepts, and `ros2 launch -p <pkg> <file>` prints the launch description without running it.

### 11. Parameters, namespaces, remapping and includes

**Parameters from a dict**, useful for one or two values:

```python
Node(
    package='turtlesim',
    executable='turtlesim_node',
    name='sim',
    parameters=[{'background_r': LaunchConfiguration('background_r')}],
)
```

**Parameters from YAML**, which is what you want past a handful:

```python
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

Node(
    package='turtlesim',
    executable='turtlesim_node',
    namespace='turtlesim2',
    name='sim',
    parameters=[PathJoinSubstitution([
        FindPackageShare('launch_tutorial'), 'config', 'turtlesim.yaml'])
    ],
)
```

The YAML file is **not** a launch file. It is a parameter file, and its structure is the thing people get wrong:

```yaml
/turtlesim2/sim:
  ros__parameters:
    background_b: 255
    background_g: 86
    background_r: 150
```

The top-level key is the node's *fully qualified name* — namespace and all — and the parameters sit under a literal `ros__parameters` key (two underscores). Get either wrong and the file loads without complaint and sets nothing: a node launched into the `turtlesim3` namespace does not match the block above, so it runs with its defaults.

When the same parameters should reach several nodes regardless of name or namespace, use the wildcard:

```yaml
/**:
  ros__parameters:
    background_b: 255
```

`/**` matches every node at any namespace depth — the right tool for `use_sim_time`, the wrong one for anything a node-specific value would state more clearly.

**Namespaces.** Setting `namespace=` on every `Node` gets tedious. `PushROSNamespace` sets it for everything that follows in a group — and it must be the *first* action in the list, or the actions before it escape the namespace:

```python
from launch.actions import GroupAction
from launch_ros.actions import PushROSNamespace

GroupAction(actions=[
    PushROSNamespace('turtlesim2'),
    IncludeLaunchDescription(PathJoinSubstitution([launch_dir, 'turtlesim_world_2_launch.py'])),
])
```

**Remapping** rewires a node's topic names from outside, without touching its source:

```python
Node(
    package='turtlesim',
    executable='mimic',
    name='mimic',
    remappings=[
        ('/input/pose', '/turtle2/pose'),
        ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
    ],
)
```

This is why generic topic names in node code (`/input/pose`) are a feature rather than laziness: the node is reusable because the wiring lives in the launch file.

**Including one launch file from another**, with an argument passed down:

```python
IncludeLaunchDescription(
    PathJoinSubstitution([launch_dir, 'broadcaster_listener_launch.py']),
    launch_arguments={'target_frame': 'carrot1'}.items()
)
```

and in the included file, the argument is declared with a default so it also runs standalone:

```python
DeclareLaunchArgument(
    'target_frame', default_value='turtle1',
    description='Target frame name.',
),
```

A declared argument is also settable from the command line: `ros2 launch pkg file.py target_frame:=carrot1`. The documentation recommends one small top-level launch file that includes subsystem launch files and sets the handful of parameters that change often.

Launch files and YAML config only work if they are installed. For `ament_python`, add them to `data_files` in `setup.py`:

```python
import os
from glob import glob

data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
],
```

For `ament_cmake`, a single install rule in `CMakeLists.txt`:

```cmake
install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})
```

A launch file that is not installed produces `file ... was not found` from `ros2 launch`, and the cause is almost always a forgotten `data_files` entry or a forgotten rebuild after adding one.

### 12. Exercise: two packages, one launch file

One sitting. Reuse the node code from [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]; the point here is the packaging, not the callbacks.

1. Create the workspace and two packages:

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name sensor temp_sim
ros2 pkg create --build-type ament_cmake  --license Apache-2.0 --node-name filter temp_filter
```

2. Make `sensor` publish a `std_msgs/msg/Float64` on `raw` at a rate taken from a declared parameter `publish_hz`, and `filter` subscribe to `raw`, apply an exponential filter with a declared parameter `alpha`, and publish `filtered`. Declare the dependencies honestly: `<exec_depend>rclpy</exec_depend>` and `<exec_depend>std_msgs</exec_depend>` in the Python package, `<depend>rclcpp</depend>` and `<depend>std_msgs</depend>` in the C++ one.

3. In `temp_sim`, create `config/params.yaml`:

```yaml
/demo/sensor:
  ros__parameters:
    publish_hz: 20.0
/demo/filter:
  ros__parameters:
    alpha: 0.1
```

4. In `temp_sim`, create `launch/bringup_launch.py` that declares a `namespace` argument defaulting to `demo`, pushes that namespace, and starts both nodes with `parameters=[PathJoinSubstitution([FindPackageShare('temp_sim'), 'config', 'params.yaml'])]` **and `name='sensor'` / `name='filter'` on the two `Node` actions**. Those names matter: `sensor` and `filter` are the *executable* names you passed to `--node-name`, while the node name comes from the string in `super().__init__(...)`. Without the `name=` override the graph shows whatever the code calls itself, the YAML keys above match nothing, and step 6 fails for a reason unrelated to the one it is meant to teach. Add the `launch/` and `config/` entries to `data_files` in `setup.py`.

5. Resolve, build, source in a *new* terminal, run:

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch temp_sim bringup_launch.py
```

6. From a third terminal, verify — and this is the part that counts, because a launch file that starts two processes is not evidence that either one was configured:

```bash
ros2 node list
```

```text
/demo/filter
/demo/sensor
```

```bash
ros2 param get /demo/sensor publish_hz
ros2 param get /demo/filter alpha
```

You are done when `ros2 param get` returns the YAML values and not the defaults compiled into the nodes. Then break it on purpose: change the top-level key in `params.yaml` from `/demo/sensor` to `/sensor`, rebuild, relaunch. The launch still succeeds, `ros2 node list` is unchanged, and `ros2 param get` returns the default. That silence is the most common parameter bug in ROS 2, and now you have seen it.

### 13. The failure to diagnose: the edit that did nothing

The symptom: you change a line in a Python node — add a log message, change a constant — rebuild, relaunch, and the behaviour is identical. You read the file again. The edit is there.

The cause is section 3, step 4: `colcon build` **copied** your file into `install/`, and the running node is loading a copy that is not the one you think. Do not debug the code. Establish which file is executing, in three commands.

First, which workspace is answering at all:

```bash
ros2 pkg prefix temp_sim
```

If this is `/opt/ros/jazzy` rather than `~/ros2_ws/install/temp_sim`, you are running an installed binary of a package you also have in source, and no amount of rebuilding will change it. That happens when the package was installed with apt — often pulled in by rosdep without `--ignore-src` — and the workspace was never sourced.

Second, which file the Python interpreter resolves, in the same shell the node runs in:

```bash
python3 -c "import temp_sim.sensor as m; print(m.__file__)"
```

```text
/home/you/ros2_ws/install/temp_sim/lib/python3.12/site-packages/temp_sim/sensor.py
```

A path under `install/` is a **copy**. A path under `build/` means the symlink install is in effect: colcon runs `setup.py develop` in the build space on purpose — its own comment reads "invoke `setup.py develop` step in build space / to avoid placing any files in the source space" — and symlinks your module there, so the path is `build/<pkg>/<pkg>/...` and your edits are live. Compare it against the file you edited; `diff` settles the argument in one line:

```bash
diff ~/ros2_ws/src/temp_sim/temp_sim/sensor.py \
     ~/ros2_ws/install/temp_sim/lib/python3.12/site-packages/temp_sim/sensor.py
```

Non-empty output is the whole diagnosis: the build did not run, ran on a different workspace, was restricted by `--packages-select` to a package you were not editing, or failed and you read the summary line instead of `log/latest_build/`.

Third, for a node that is already running, ask the process rather than the filesystem:

```bash
pgrep -af sensor
tr '\0' '\n' < /proc/<pid>/cmdline
```

The command line shows the console-script wrapper the node was launched from — `install/temp_sim/lib/temp_sim/sensor` — and `cat` on it shows which module it imports. If that path is under a workspace you forgot you had sourced, you have found it.

The fix for the ordinary case is one flag:

```bash
rm -rf build install log
colcon build --symlink-install
```

Rerun the `python3 -c` check and the path now points into `build/`, not `src/`, because that is where colcon puts the development install. The file there is a symlink to your source, so edit, restart the node, and the change takes effect with no build at all.

**And now the asymmetry.** Do the same experiment with the C++ node in `temp_filter`. Change a constant in `src/filter.cpp`, restart the node without rebuilding, and nothing happens — correctly. `--symlink-install` changed nothing for it, because what runs is `install/temp_filter/lib/temp_filter/filter`, an ELF binary produced by the compiler, not a link to a source file. Confirm it directly:

```bash
ls -l $(ros2 pkg prefix temp_filter)/lib/temp_filter/filter
file $(ros2 pkg prefix temp_filter)/lib/temp_filter/filter
```

It is a symlink, pointing into `build/` — `ament_cmake` reimplements `install(TARGETS)` to symlink rather than copy, as its own header says: *"Reimplement CMake install(TARGETS) command to use symlinks instead of copying resources."* So the symlink is there; what it points at is a **compiled artefact**, and no amount of symlinking recompiles it. Editing `filter.cpp` still requires `colcon build`, while editing `params.yaml` in the same package takes effect on relaunch. That is the rule in one sentence: **`--symlink-install` makes installed files track their sources, and a binary tracks its object code, not the `.cpp` you edited.**

The C++ loop is therefore `colcon build --packages-select temp_filter` every time, and that is why the selective-build flags in section 8 matter more to C++ developers than to Python ones.

### 14. What this page does not cover

Writing the nodes themselves is [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]], and declaring and validating the parameters that the YAML here sets is [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]. Launch-time event handlers, conditional actions, composable-node containers and lifecycle-aware launch are beyond this page; the launch documentation covers them, and lifecycle nodes appear in 25.3. Capturing what a launched system did, replaying it, and pinning a workspace so a colleague gets the same build are [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]. Releasing a package into a ROS distribution — `bloom`, the rosdistro pull request, the buildfarm — is not covered anywhere in this track. Where the rest of the stack sits is [[04-robotics/ros2/index|25. ROS 2]].

### Sources

- ROS 2 Jazzy documentation — Tutorials: Creating a workspace; Creating a package; Managing Dependencies with rosdep; Creating a launch file; Managing large projects.
- ROS 2 Jazzy documentation — Tutorials: Implementing custom interfaces (interfaces require a CMake package; `ament_cmake_python` for Python in CMake packages).
- ROS 2 Jazzy documentation — How-to guides: Using ros2 param; Launch file different formats.
- colcon documentation — build verb (`--symlink-install`, `--merge-install`, `--continue-on-error`); Package selection arguments (`--packages-select`, `--packages-up-to`); What is a Workspace?; Overriding Packages.
- `ament_cmake_python` README — `ament_python_install_package`, `ament_python_install_module`.
- `rosdep` command-line options (`--from-paths`, `--ignore-src`, `-r`, `-y`).
- REP-149 — package format 3 dependency tags.

> [!question]- Self-check · Answer
> **1. You edit a Python node, run `colcon build`, relaunch, and nothing changes. Name three causes and the single command that distinguishes them.** The build did not cover this package (`--packages-select` on the wrong one), the shell is resolving the package from `/opt/ros/jazzy` rather than your workspace, or the build failed and you read only the summary. `python3 -c "import <pkg>.<module> as m; print(m.__file__)"` in the running shell tells you which file is actually loaded; `ros2 pkg prefix <pkg>` tells you which workspace won.
> **2. Why does `--symlink-install` fix the Python case but not the C++ case?** For an `ament_python` package colcon runs setuptools' `develop` step, so the installed module path resolves back into `src/`. A C++ package's installed artefact is a compiled binary; there is no source file for it to point at, so a new binary requires a compile. Data files installed by a CMake package — launch, YAML, URDF — *are* symlinked and do track their sources.
> **3. Your YAML parameter file loads without error and no parameter is set. What are the two things to check first?** The top-level key must be the node's fully qualified name including its namespace (`/demo/sensor`, not `/sensor`), and the parameters must sit under `ros__parameters` with two underscores. Both mistakes are silent. `/**` as the top-level key sidesteps the first one when the parameters really are meant for every node.
> **4. Why should a pure Python package use `<exec_depend>` rather than `<depend>`?** `<depend>` declares a dependency needed at both build and run time, and a pure Python package has no build phase. Declaring build-time dependencies it does not have makes the workspace build order more constrained than it needs to be and misrepresents what an installed binary of the package actually requires.

## 한국어

> [!abstract] 깊이 목표 · Depth target
> **Working** — 편집–빌드–source–launch 루프를 매일 돌리고, 그 루프가 만들어 내는 두 가지 고장을 진단할 정도. 배포판 릴리스용 패키징은 아니다.
> **Working** — enough to run the daily loop and diagnose its two failures, not to package for a distribution release.

> [!note] 선수 지식 · Prerequisites
> **Ubuntu 24.04 위의 ROS 2 Jazzy Jalisco** 환경([[04-robotics/ros2/index|25. ROS 2]]), 그리고 이미 노드를 쓰고 실행할 수 있는 상태([[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]). 파라미터는 여기서 "설정하는 대상"으로만 쓴다. 파라미터 자체는 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]].
> ROS 2 Jazzy on Ubuntu 24.04, plus the ability to write and run a node.

### 1. 빌드 단계가 왜 존재하는가

Python은 컴파일이 필요 없다. 그러면 왜 Python 노드를 `python3 my_node.py`로 그냥 돌리면 안 되는가.

파일 하나, 터미널 하나라면 돌아간다. 다만 이런 것들은 되지 않는다. `ros2 run`이 패키지 이름으로 실행 파일을 찾는 것, 다른 패키지의 launch 파일이 그 노드를 가리키는 것, `rosdep`이 무엇을 설치할지 아는 것, C++ 노드가 그 메시지 타입을 찾는 것, 남이 clone해서 빌드하는 것.

전부 하나의 발상에서 나온다. **패키지**가 자기가 무엇이고 무엇을 필요로 하는지 선언하고, **빌드**가 그 선언을 ROS 2 도구가 탐색할 줄 아는 고정된 디렉터리 구조로 바꾼다. 대가는, 편집하는 곳이 아닌 다른 곳에 코드 사본이 생긴다는 것이다. 13절은 그 사본이 낡는 날에 관한 것이다.

### 2. 워크스페이스: `src`, `build`, `install`, `log`

워크스페이스는 ROS 2 패키지가 들어 있는 디렉터리다. 직접 만든다 — `ros2 workspace create` 같은 것은 없다.

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
```

패키지는 `src` 안에 하나씩, 절대 서로 중첩하지 않는다. 첫 빌드 후 디렉터리는 넷이다.

| 디렉터리 | 만드는 주체 | 내용 | 지워도 되나 |
|---|---|---|---|
| `src` | 당신 | 편집하는 유일한 것, 버전 관리에 들어가는 유일한 것 | 아니오 |
| `build` | colcon | 패키지별 중간 산출물 — CMake 캐시, 오브젝트 파일, `.egg-info` | 예 |
| `install` | colcon | 결과물: 실행 파일, Python 모듈, `share/` 데이터, source할 setup 파일 | 예 |
| `log` | colcon | 모든 빌드의 전체 출력. 화면 위로 지나가 버린 그 에러 포함 | 예 |

습관 둘이 나온다. `build/`, `install/`, `log/`를 `.gitignore`에 넣는다. 빌드가 말이 안 되게 굴면 `rm -rf build install log` 후 다시 빌드한다 — 싸고, 질문 한 부류를 통째로 없앤다.

초보가 무시하는 것은 `log`다. `colcon build`는 요약만 찍고 컴파일러 출력은 찍지 않는다. 패키지별 전체 출력은 `log/latest_build/<package>/`에 있다. 또는 `colcon build --event-handlers console_direct+`로 터미널에 흘려보낸다.

### 3. `colcon build`가 실제로 하는 일

`colcon`은 빌드 *도구*다. 워크스페이스 루트에서 실행한다.

```bash
cd ~/ros2_ws
colcon build
```

```text
Starting >>> temp_sim
Finished <<< temp_sim [1.21s]
Starting >>> temp_filter
Finished <<< temp_filter [4.87s]

Summary: 2 packages finished [6.20s]
```

이 순서로 네 가지가 일어났다.

1. **탐색.** colcon이 `src`를 걸으며 `package.xml`을 찾는다. `COLCON_IGNORE` 파일이 있는 디렉터리는 건너뛴다 — 저장소가 "빌드하면 안 되는 패키지"를 배포하는 방식이다.
2. **순서 결정.** 각 `package.xml`의 의존 태그를 읽어 그래프를 만든다. 서로 무관한 패키지는 병렬로, 의존하는 패키지는 기다렸다 빌드한다. 의존성을 정직하게 선언해야 하는 첫 번째 실용적 이유가 이것이다. 선언하지 않은 의존성은 빌드 순서를 운에 맡기는 것이고, 내 머신에서 통하던 운은 동료의 병렬 빌드에서 깨진다.
3. **패키지별 빌드.** 선언된 build type에 따라 분기한다 — `ament_cmake`면 CMake, `ament_python`이면 setuptools.
4. **설치.** 각 패키지의 산출물을 `install/<package_name>/`으로 복사하고, 그 옆에 환경 setup 파일을 생성한다.

4번을 보라. 기본값에서 **설치는 복사**다. 노드가 실행하는 파일은 당신이 편집한 파일이 아니다.

### 4. ament, 그리고 두 가지 build type

`ament`는 빌드 *시스템*이다 — 산출물이 어디로 가는지 정하는 CMake 매크로와 Python 관례. colcon은 그것을 호출하는 도구다. colcon은 *무엇을 언제*, ament는 *어디에*를 정한다. 공식 지원 build type은 둘이다.

```bash
cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 temp_sim
ros2 pkg create --build-type ament_cmake  --license Apache-2.0 temp_filter
```

`ament_python` 패키지는 ROS 메타데이터를 붙인 setuptools 패키지다. 최소 구성은 `package.xml`, `setup.py`, `setup.cfg`, `resource/<package_name>`(ament 인덱스에서 패키지를 찾게 해 주는 마커 파일), 그리고 패키지와 같은 이름에 `__init__.py`가 든 디렉터리. 실행 파일은 `entry_points`에서 나온다.

```python
entry_points={
    'console_scripts': [
        'sensor = temp_sim.sensor:main',
    ],
},
```

그리고 `ros2 run`이 그것을 찾을 수 있게 하는 것이 `setup.cfg`다. 생성되는 스크립트를 ament가 보는 위치로 돌린다.

```ini
[develop]
script_dir=$base/lib/temp_sim
[install]
install_scripts=$base/lib/temp_sim
```

`ament_cmake` 패키지는 CMake 프로젝트다. 최소 구성은 `package.xml`, `CMakeLists.txt`, `src/`, `include/<package_name>/`. 실행 파일과 설치 규칙은 명시적이다.

```cmake
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(filter src/filter.cpp)
ament_target_dependencies(filter rclcpp std_msgs)

install(TARGETS filter DESTINATION lib/${PROJECT_NAME})

ament_package()
```

`DESTINATION lib/${PROJECT_NAME}`은 위 `setup.cfg`가 가리킨 것과 같은 위치다. `ros2 run <package> <executable>`이 뒤지는 관례가 이것이고, 그래서 두 언어를 커맨드라인에서 똑같이 다룰 수 있다.

**둘 다 필요한 경우.** 메시지·서비스·액션 정의는 현재 CMake 패키지에서만 생성할 수 있다. `rosidl_generate_interfaces()`가 CMake 매크로이기 때문이다. 따라서 자기 인터페이스를 정의하면서 Python 노드도 담는 패키지는 `ament_python`이 될 수 없다. 문서가 제시하는 길은 `ament_cmake` 패키지에서 `ament_cmake_python`을 함께 쓰는 것이다. 그 `ament_python_install_package()` 매크로가 CMake에서 Python 패키지를 설치한다. 다른 길은 — 그리고 이쪽이 낫다 — 패키지를 둘로 쪼개는 것이다. `my_robot_interfaces`(`ament_cmake`, 정의만)와 `my_robot_nodes`(`ament_python`). 정의만 든 인터페이스 패키지는 남이 의존하기에 싸다.

### 5. `package.xml`, 의존 태그, rosdep

`package.xml`이 선언이다. 이름, 버전, 관리자, 라이선스, `<export>` 블록의 build type, 그리고 의존성이 들어간다. 의존 항목은 **rosdep key**라 부르고, 패키지 생애의 각 국면마다 전용 태그가 있다.

| 태그 | 의미 | 전형적 용도 |
|---|---|---|
| `<depend>` | 빌드 시점과 실행 시점 모두 필요 | C++ 의존성, 애매하면 이것 |
| `<build_depend>` | 빌드에만 필요 | 컴파일 중에만 쓰는 도구 |
| `<build_export_depend>` | 내 패키지에 빌드 의존하는 쪽이 필요로 함 | 공개 헤더가 남의 헤더를 include할 때 |
| `<exec_depend>` | 실행 시점에만 필요 | Python 의존성, launch 파일, 메시지 런타임 |
| `<test_depend>` | 테스트에만 필요 | 린터, `python3-pytest` |

초보가 틀리는 구분: 순수 Python 패키지는 빌드 국면이 없으므로 `<depend>`가 아니라 `<exec_depend>`를 써야 한다. C++ 패키지는 거의 항상 `<depend>`다.

key는 ROS 생태계에 릴리스된 패키지 이름(`rclpy`, `std_msgs`, `nav2_bt_navigator`)이거나, rosdistro 인덱스의 시스템 라이브러리 key다 — apt는 `rosdep/base.yaml`, Python은 `rosdep/python.yaml`. `doxygen`은 key이고 `libdoxygen-dev`는 아니다.

그 key들을 소비하는 명령이 이것이다. 빌드 전에 워크스페이스 루트에서 한 번 돌린다.

```bash
rosdep install --from-paths src --ignore-src -r -y
```

`src` 아래 모든 `package.xml`을 걸으며 각 key를 이 운영체제의 패키지 이름으로 해석하고, 빠진 것을 `apt`로 설치한다. 플래그를 하나씩 보면,

- `--from-paths src` — `package.xml`을 찾을 디렉터리.
- `--ignore-src` — 이 워크스페이스 안에 있는 패키지는 의존성으로 설치하지 않는다. 없으면 rosdep이 곧 소스로 빌드할 패키지의 릴리스 바이너리를 설치해 버리고, 같은 것이 둘이 된다.
- `-r` — 해석에 실패한 key가 있어도 멈추지 않고 계속한다. 유용하고, 동시에 진짜 문제를 가리는 방법이기도 하다. 종료 코드를 믿지 말고 출력에서 미해결 key를 확인하라.
- `-y` — apt에 yes로 답한다.

rosdep은 패키지 관리자가 아니다. 플랫폼 독립적인 key를, Ubuntu 24.04에서 apt가 그것을 뭐라고 부르는지로 옮기는 사상(mapping)이다. 첫 사용 전에 `sudo rosdep init`과 `rosdep update`가 한 번 필요하다.

### 6. 언더레이, 오버레이, source 순서

`/opt/ros/jazzy`의 ROS 2 설치본도 워크스페이스다. 내 워크스페이스를 그 위에 얹어 source하면 내 것이 **오버레이**, 설치본이 **언더레이**다. 규칙은 이렇다.

> 언더레이는 오버레이에 있는 모든 패키지의 의존성을 담고 있어야 하며, 오버레이의 패키지는 언더레이의 패키지를 덮어쓴다.

source 순서는 여기서 따라 나온다. 언더레이 먼저, 오버레이 나중.

```bash
source /opt/ros/jazzy/setup.bash      # 언더레이
source ~/ros2_ws/install/setup.bash   # 오버레이
```

install 디렉터리에는 setup 파일이 둘이고 차이가 중요하다. `local_setup.bash`는 *이* 워크스페이스의 패키지만 추가한다. `setup.bash`는 이 워크스페이스와 *그것이 빌드된 언더레이*까지 추가한다. 그래서 `/opt/ros/jazzy/setup.bash` 다음에 워크스페이스의 `local_setup.bash`를 하는 것은 워크스페이스의 `setup.bash` 하나만 하는 것과 같다.

당연해 보이지 않으면서 실제로 시간을 잡아먹는 규칙 둘.

- **오버레이가 source된 터미널에서 빌드하지 말고, 빌드한 터미널에서 오버레이를 source하지 말라.** 공식 튜토리얼이 복잡한 문제를 만든다고 명시한다. 원리는, 빌드가 이미 자기 이전 출력을 가리키는 환경을 물려받아, 패키지가 자기 자신의 낡은 사본에 대해 빌드될 수 있다는 것이다. 빌드용 터미널 하나, 실행용 터미널 따로.
- **다른 패키지가 의존하는 패키지를 덮어쓰는 것은 함정이다.** 언더레이의 패키지들은 언더레이 버전에 대해 컴파일되었는데 실행은 당신 버전과 하게 된다. ABI가 바뀌면 결과는 아무 말도 안 되는 크래시다. 오버레이는 leaf 패키지에 가장 안전하다.

어느 쪽이 이겼는지는 이렇게 묻는다.

```bash
ros2 pkg prefix temp_sim
```

```text
/home/you/ros2_ws/install/temp_sim
```

여기서 `/opt/ros/jazzy`가 찍히면 그 셸은 당신 워크스페이스를 보고 있지 않고, 소스를 어떻게 고쳐도 실행되는 것은 바뀌지 않는다.

### 7. `--symlink-install`이 정확히 무엇을 사 주는가

```bash
colcon build --symlink-install
```

*가능한 곳에서* 소스·빌드 디렉터리의 파일을 복사하는 대신 심볼릭 링크를 쓰라는 플래그다. `ament_python` 패키지에서는 colcon이 setuptools의 `install` 대신 `develop` 단계를 돌리므로, 설치된 모듈이 `src`의 파일로 되돌아 해석된다. Python 파일을 고치고 노드를 재시작하면 즉시 반영된다 — 빌드 없이.

하지 않는 일:

- **컴파일된 C++에는 도움이 되지 않는다.** `.cpp` 파일로 가는 심볼릭 링크는 실행 파일이 아니다. 실행되는 산출물은 바이너리이고, 새 바이너리를 얻으려면 컴파일해야 한다. `ament_cmake` 패키지라도 `install(DIRECTORY ...)`로 설치되는 *데이터 파일* — launch 파일, YAML, URDF, RViz 설정 — 은 여전히 링크된다. 그건 진짜로 유용하다. 하지만 C++ 자체는 매번 `colcon build`다.
- **구조 변경은 어떤 언어에서도 덮지 못한다.** `setup.py`의 새 entry point, `data_files`에 추가한 새 파일, 이름을 바꾼 모듈, `package.xml`의 새 의존성 — 전부 설치되는 내용 자체를 바꾸므로 재빌드가 필요하다. 링크는 *이미 있는* 설치 경로가 살아 있는 파일을 가리키게 유지할 뿐이다.
- **절반만 적용할 수 있는 모드가 아니다.** 한 워크스페이스에서 `colcon build`와 `colcon build --symlink-install`을 오가면 사본과 링크가 섞인다. 워크스페이스당 하나를 골라라. 바꿀 거면 `build`와 `install`을 먼저 지워라.

기억할 그림: 플래그가 없으면 `install/`은 `src/`의 사진이다. 플래그가 있으면, 그리고 Python에 한해, `install/`은 `src/`로 난 창이다.

### 8. 전부보다 적게 빌드하기

Nav2나 MoveIt이 들어 있는 워크스페이스의 전체 `colcon build`는 집중이 끊길 만큼 걸린다. 선택 플래그 둘.

```bash
colcon build --packages-select temp_filter            # 정확히 이 패키지만
colcon build --packages-up-to temp_filter             # 이 패키지와 그 재귀적 의존성
```

`--packages-select`는 의존성이 바뀌지 않은 한 패키지를 빡빡하게 고칠 때 쓴다. `--packages-up-to`는 남의 변경을 pull한 뒤, 또는 같은 워크스페이스의 다른 패키지에 의존하는 패키지를 처음 빌드할 때 쓴다.

`--packages-select`의 고장 방식은 조용한 낡음이다. 패키지 A의 메시지 정의를 고치고 B만 다시 빌드하면 B는 여전히 옛 정의에 대해 컴파일된 상태다. 소스를 보면 말이 안 되는 타입·직렬화 에러가 증상이면 플래그를 빼라. 곁들여 `--continue-on-error`는 한 패키지가 실패해도 무관한 패키지를 계속 빌드해, 20개짜리 빌드를 에러 목록 하나로 바꿔 준다.

### 9. launch 파일이 존재하는 이유

노드를 손으로 띄우는 방식은 세 개쯤에서 한계가 온다. 이유는 구체적이다.

1. **개수.** 실제 시스템은 프로세스 10~50개다. 터미널 10개는 사용자 인터페이스가 아니다.
2. **설정.** 각 노드에 파라미터, 리매핑, 네임스페이스가 필요하다. `--ros-args` 플래그로 타이핑하는 것은 틀리기 쉽고 기록에 남지 않는다.
3. **재현성.** 새벽 2시에 친 명령은 버전 관리에 없다. launch 파일은 있다.
4. **감시.** launch 시스템은 자기가 띄운 프로세스를 감시하고, 하나가 죽으면 보고하거나 반응한다. 터미널 무더기는 그러지 않는다.

launch 파일은 시스템의 *기술(description)*이고, `launch_ros`의 ROS 전용 액션과 함께 `launch` 프레임워크가 실행한다. Python, XML, YAML로 쓸 수 있고 셋은 기능적으로 동등하다. 여기서 Python을 쓰는 이유는 셋 중 유일하게 무언가를 계산할 수 있기 때문이다.

### 10. Python launch 파일: description, action, substitution

개념 셋이 파일의 세 요소에 대응한다.

**launch description**은 파일이 돌려주는 것이다. `generate_launch_description()`이라는 함수가 `LaunchDescription` 객체를 반환한다. launch 시스템은 파일을 import해서 그 함수를 호출한다. 파일의 나머지에 특별한 것은 없다.

**액션**(action)은 그 리스트의 항목, 즉 할 일이다. `Node`(`launch_ros.actions`)는 ROS 노드를 띄운다. `DeclareLaunchArgument`는 이 파일이 받는 인자를 선언한다. `IncludeLaunchDescription`은 다른 launch 파일을 끌어온다. `GroupAction`은 액션 묶음의 범위를 정한다.

**치환**(substitution)은 파일을 쓸 때가 아니라 실행할 때 결정되는 값이다. launch 파일은 두 국면으로 평가되므로 launch 인자에 평범한 Python 문자열 연산을 쓸 수 없다. `LaunchConfiguration('target_frame')`은 문자열이 아니라 나중에 문자열이 될 객체다. `FindPackageShare('temp_sim')`은 이긴 워크스페이스에서 그 패키지의 `share` 디렉터리로 해석되고, `PathJoinSubstitution([...])`은 그런 객체들로 된 경로를 잇는다.

최소 형태:

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlesim',
            namespace='turtlesim1',
            executable='turtlesim_node',
            name='sim',
        ),
    ])
```

`package`와 `executable`은 `ros2 run`에 줄 것과 같다. `name`은 코드에서 준 노드 이름을 덮어쓰고 `namespace`는 앞에 붙인다. 실행은 이렇게 한다.

```bash
ros2 launch <package_name> <launch_file_name>
```

필요해지기 전에 알아 둘 플래그 둘: `ros2 launch -s <pkg> <file>`은 그 launch 파일이 받는 인자를 찍고, `ros2 launch -p <pkg> <file>`은 실행하지 않고 launch description을 찍는다.

### 11. 파라미터, 네임스페이스, 리매핑, include

**dict으로 주는 파라미터**, 한두 개일 때 쓴다.

```python
Node(
    package='turtlesim',
    executable='turtlesim_node',
    name='sim',
    parameters=[{'background_r': LaunchConfiguration('background_r')}],
)
```

**YAML에서 읽는 파라미터**, 몇 개를 넘어가면 이쪽이다.

```python
from launch.substitutions import PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare

Node(
    package='turtlesim',
    executable='turtlesim_node',
    namespace='turtlesim2',
    name='sim',
    parameters=[PathJoinSubstitution([
        FindPackageShare('launch_tutorial'), 'config', 'turtlesim.yaml'])
    ],
)
```

이 YAML 파일은 launch 파일이 **아니다**. 파라미터 파일이고, 사람들이 틀리는 지점은 그 구조다.

```yaml
/turtlesim2/sim:
  ros__parameters:
    background_b: 255
    background_g: 86
    background_r: 150
```

최상위 키는 노드의 *완전 수식 이름*, 즉 네임스페이스까지 포함한 이름이고, 파라미터는 문자 그대로 `ros__parameters`(밑줄 두 개) 키 아래에 놓인다. 둘 중 하나만 틀려도 파일은 불평 없이 로드되고 아무것도 설정되지 않는다. `turtlesim3` 네임스페이스로 띄운 노드는 위 블록과 맞지 않아 기본값으로 돈다.

같은 파라미터를 이름·네임스페이스와 무관하게 여러 노드에 주려면 와일드카드를 쓴다.

```yaml
/**:
  ros__parameters:
    background_b: 255
```

`/**`는 어떤 네임스페이스 깊이의 모든 노드에 매치된다. `use_sim_time`에는 맞는 도구이고, 노드별 값이 더 분명한 것에는 틀린 도구다.

**네임스페이스.** `Node`마다 `namespace=`를 다는 것은 지겹다. `PushROSNamespace`는 그룹 안에서 뒤따르는 모든 것에 네임스페이스를 건다 — 그리고 리스트의 *첫* 액션이어야 한다. 아니면 그 앞의 액션들이 네임스페이스를 벗어난다.

```python
from launch.actions import GroupAction
from launch_ros.actions import PushROSNamespace

GroupAction(actions=[
    PushROSNamespace('turtlesim2'),
    IncludeLaunchDescription(PathJoinSubstitution([launch_dir, 'turtlesim_world_2_launch.py'])),
])
```

**리매핑**은 노드의 소스를 건드리지 않고 바깥에서 토픽 이름을 다시 배선한다.

```python
Node(
    package='turtlesim',
    executable='mimic',
    name='mimic',
    remappings=[
        ('/input/pose', '/turtle2/pose'),
        ('/output/cmd_vel', '/turtlesim2/turtle1/cmd_vel'),
    ],
)
```

노드 코드의 일반적인 토픽 이름(`/input/pose`)이 게으름이 아니라 기능인 이유가 이것이다. 배선이 launch 파일에 사니까 노드가 재사용 가능해진다.

**다른 launch 파일 include**, 인자를 내려보내면서:

```python
IncludeLaunchDescription(
    PathJoinSubstitution([launch_dir, 'broadcaster_listener_launch.py']),
    launch_arguments={'target_frame': 'carrot1'}.items()
)
```

include되는 쪽에서는 기본값과 함께 인자를 선언해 두어 단독 실행도 되게 한다.

```python
DeclareLaunchArgument(
    'target_frame', default_value='turtle1',
    description='Target frame name.',
),
```

선언된 인자는 커맨드라인에서도 준다. `ros2 launch pkg file.py target_frame:=carrot1`. 문서가 권하는 구조는, 하위 시스템 launch 파일들을 include하고 자주 바뀌는 파라미터 몇 개만 담는 짧은 최상위 launch 파일이다.

launch 파일과 YAML 설정은 설치되어야 동작한다. `ament_python`이면 `setup.py`의 `data_files`에 넣는다.

```python
import os
from glob import glob

data_files=[
    ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
    ('share/' + package_name, ['package.xml']),
    (os.path.join('share', package_name, 'launch'), glob('launch/*')),
    (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
],
```

`ament_cmake`면 `CMakeLists.txt`에 설치 규칙 한 줄이다.

```cmake
install(DIRECTORY launch config DESTINATION share/${PROJECT_NAME})
```

설치되지 않은 launch 파일은 `ros2 launch`에서 `file ... was not found`를 낸다. 원인은 거의 항상 `data_files` 항목을 빠뜨렸거나, 넣고 나서 다시 빌드하지 않은 것이다.

### 12. 실습: 패키지 둘, launch 파일 하나

한 자리에서 끝난다. 노드 코드는 [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]의 것을 재사용하라. 여기의 핵심은 콜백이 아니라 패키징이다.

1. 워크스페이스와 패키지 둘을 만든다.

```bash
mkdir -p ~/ros2_ws/src && cd ~/ros2_ws/src
ros2 pkg create --build-type ament_python --license Apache-2.0 --node-name sensor temp_sim
ros2 pkg create --build-type ament_cmake  --license Apache-2.0 --node-name filter temp_filter
```

2. `sensor`는 선언된 파라미터 `publish_hz`의 주기로 `raw`에 `std_msgs/msg/Float64`를 publish하게, `filter`는 `raw`를 구독해 선언된 파라미터 `alpha`의 지수 필터를 적용하고 `filtered`를 publish하게 만든다. 의존성은 정직하게 선언한다. Python 패키지에는 `<exec_depend>rclpy</exec_depend>`와 `<exec_depend>std_msgs</exec_depend>`, C++ 패키지에는 `<depend>rclcpp</depend>`와 `<depend>std_msgs</depend>`.

3. `temp_sim`에 `config/params.yaml`을 만든다.

```yaml
/demo/sensor:
  ros__parameters:
    publish_hz: 20.0
/demo/filter:
  ros__parameters:
    alpha: 0.1
```

4. `temp_sim`에 `launch/bringup_launch.py`를 만든다. 기본값 `demo`인 `namespace` 인자를 선언하고, 그 네임스페이스를 push하고, 두 노드를 `parameters=[PathJoinSubstitution([FindPackageShare('temp_sim'), 'config', 'params.yaml'])]`와 함께 **두 `Node` 액션에 `name='sensor'`, `name='filter'`를 붙여** 띄운다. 이 이름이 중요하다. `sensor`와 `filter`는 `--node-name`에 넘긴 *실행 파일* 이름이고, 노드 이름은 `super().__init__(...)`의 문자열에서 온다. `name=` 덮어쓰기가 없으면 그래프에는 코드가 스스로를 부르는 이름이 뜨고, 위 YAML 키는 아무것도 맞히지 못하며, 6단계가 가르치려는 것과 무관한 이유로 실패한다. `setup.py`의 `data_files`에 `launch/`와 `config/` 항목을 추가한다.

5. 해결하고, 빌드하고, *새* 터미널에서 source하고, 실행한다.

```bash
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build
```

```bash
source /opt/ros/jazzy/setup.bash
source ~/ros2_ws/install/setup.bash
ros2 launch temp_sim bringup_launch.py
```

6. 세 번째 터미널에서 검증한다. 여기가 핵심이다. 프로세스 둘이 떴다는 사실은 둘 중 어느 것도 설정되었다는 증거가 아니기 때문이다.

```bash
ros2 node list
```

```text
/demo/filter
/demo/sensor
```

```bash
ros2 param get /demo/sensor publish_hz
ros2 param get /demo/filter alpha
```

`ros2 param get`이 노드에 박힌 기본값이 아니라 YAML 값을 돌려주면 끝이다. 그다음 일부러 깨 보라. `params.yaml`의 최상위 키를 `/demo/sensor`에서 `/sensor`로 바꾸고, 다시 빌드하고, 다시 launch한다. launch는 여전히 성공하고 `ros2 node list`도 그대로이며 `ros2 param get`은 기본값을 돌려준다. 그 침묵이 ROS 2에서 가장 흔한 파라미터 버그이고, 이제 당신은 그것을 본 적이 있다.

### 13. 진단할 고장: 아무 일도 하지 않은 편집

증상. Python 노드의 한 줄을 고치고 — 로그 한 줄 추가, 상수 변경 — 다시 빌드하고 다시 launch했는데 동작이 똑같다. 파일을 다시 읽는다. 편집은 거기 있다.

원인은 3절의 4단계다. `colcon build`가 파일을 `install/`로 **복사했고**, 실행 중인 노드가 당신이 생각하는 것과 다른 사본을 읽고 있다. 코드를 디버깅하지 말라. 어느 파일이 실행 중인지를 명령 세 개로 확정하라.

첫째, 애초에 어느 워크스페이스가 답하고 있는가.

```bash
ros2 pkg prefix temp_sim
```

이것이 `~/ros2_ws/install/temp_sim`이 아니라 `/opt/ros/jazzy`면, 소스로도 갖고 있는 패키지의 설치된 바이너리를 돌리고 있는 것이고 아무리 다시 빌드해도 바뀌지 않는다. apt로 설치되고(`--ignore-src` 없이 rosdep이 끌어온 경우가 흔하다) 워크스페이스를 source하지 않았을 때 그렇게 된다.

둘째, Python 인터프리터가 어느 파일로 해석하는가. 노드가 도는 것과 같은 셸에서,

```bash
python3 -c "import temp_sim.sensor as m; print(m.__file__)"
```

```text
/home/you/ros2_ws/install/temp_sim/lib/python3.12/site-packages/temp_sim/sensor.py
```

`install/` 아래 경로면 **사본**이다. `build/` 아래 경로면 symlink 설치가 걸려 있다는 뜻이다. colcon은 `setup.py develop`을 일부러 build space에서 돌린다. 자기 주석이 "invoke `setup.py develop` step in build space / to avoid placing any files in the source space"라고 적고 있다. 모듈을 그쪽에 심볼릭 링크로 걸어 두므로 경로는 `build/<패키지>/<패키지>/...`가 되고 편집이 살아 있다. 편집한 파일과 비교하라. `diff` 한 줄이면 논쟁이 끝난다.

```bash
diff ~/ros2_ws/src/temp_sim/temp_sim/sensor.py \
     ~/ros2_ws/install/temp_sim/lib/python3.12/site-packages/temp_sim/sensor.py
```

출력이 비어 있지 않으면 그것이 진단 전부다. 빌드가 안 돌았거나, 다른 워크스페이스에서 돌았거나, `--packages-select`가 편집 중인 패키지를 빼놓았거나, 실패했는데 `log/latest_build/` 대신 요약 줄만 읽은 것이다.

셋째, 이미 돌고 있는 노드라면 파일 시스템이 아니라 프로세스에 물어라.

```bash
pgrep -af sensor
tr '\0' '\n' < /proc/<pid>/cmdline
```

명령줄에 노드가 띄워진 console-script 래퍼가 보인다 — `install/temp_sim/lib/temp_sim/sensor` — 그리고 그 파일을 `cat`하면 어느 모듈을 import하는지 나온다. 그 경로가 source한 줄도 몰랐던 워크스페이스 아래라면 범인을 찾은 것이다.

평범한 경우의 해법은 플래그 하나다.

```bash
rm -rf build install log
colcon build --symlink-install
```

`python3 -c` 확인을 다시 하면 경로가 `src/`가 아니라 `build/`를 가리킨다. colcon이 개발용 설치를 거기에 두기 때문이다. 그 파일이 소스를 가리키는 심볼릭 링크이므로, 고치고 노드만 재시작하면 빌드 없이 반영된다.

**그리고 여기서 비대칭이 나온다.** `temp_filter`의 C++ 노드로 같은 실험을 해 보라. `src/filter.cpp`의 상수를 고치고 다시 빌드하지 않은 채 노드를 재시작하면 아무 일도 일어나지 않는다 — 그게 맞다. `--symlink-install`은 그쪽에 아무것도 바꾸지 않았다. 실행되는 것은 `install/temp_filter/lib/temp_filter/filter`, 컴파일러가 만든 ELF 바이너리이지 소스 파일로 가는 링크가 아니기 때문이다. 직접 확인하라.

```bash
ls -l $(ros2 pkg prefix temp_filter)/lib/temp_filter/filter
file $(ros2 pkg prefix temp_filter)/lib/temp_filter/filter
```

심볼릭 링크이고 `build/` 안을 가리킨다. `ament_cmake`가 `install(TARGETS)`를 복사 대신 심볼릭 링크로 다시 구현하기 때문이다. 그 헤더가 *"Reimplement CMake install(TARGETS) command to use symlinks instead of copying resources."* 라고 적고 있다. 즉 링크는 걸려 있고, 그 링크가 가리키는 것이 **컴파일 산출물**이다. 심볼릭 링크를 아무리 걸어도 그것이 다시 컴파일되지는 않는다. `filter.cpp`를 고치면 여전히 `colcon build`가 필요하고, 같은 패키지의 `params.yaml`은 다시 launch하면 반영된다. 한 문장으로 된 규칙: **`--symlink-install`은 설치된 파일이 자기 소스를 따라가게 만들지만, 바이너리가 따라가는 것은 목적 코드이지 당신이 고친 `.cpp`가 아니다.**

따라서 C++ 루프는 매번 `colcon build --packages-select temp_filter`이고, 8절의 선택 빌드 플래그가 Python 개발자보다 C++ 개발자에게 더 중요한 이유가 이것이다.

### 14. 이 페이지가 다루지 않는 것

노드 자체를 쓰는 것은 [[04-robotics/ros2/nodes-topics-messages|25.2 Nodes, Topics and Messages]]이고, 여기의 YAML이 설정하는 파라미터를 선언하고 검증하는 것은 [[04-robotics/ros2/services-actions-parameters|25.3 Services, Actions, Parameters and Lifecycle]]이다. launch 시점의 이벤트 핸들러, 조건부 액션, composable node 컨테이너, lifecycle을 아는 launch는 이 페이지 밖이다. launch 문서가 다루고 lifecycle 노드는 25.3에 나온다. launch된 시스템이 무엇을 했는지 기록하고 다시 재생하고, 동료가 같은 빌드를 얻도록 워크스페이스를 고정하는 것은 [[04-robotics/ros2/debugging-data-reproducibility|25.10 Debugging, Data and Reproducibility]]다. 패키지를 ROS 배포판에 릴리스하는 것 — `bloom`, rosdistro 풀 리퀘스트, 빌드팜 — 은 이 트랙 어디서도 다루지 않는다. 나머지 스택의 위치는 [[04-robotics/ros2/index|25. ROS 2]].

### 출처

- ROS 2 Jazzy 문서 — Tutorials: Creating a workspace; Creating a package; Managing Dependencies with rosdep; Creating a launch file; Managing large projects.
- ROS 2 Jazzy 문서 — Tutorials: Implementing custom interfaces(인터페이스는 CMake 패키지에서만 정의 가능, CMake 패키지의 Python은 `ament_cmake_python`).
- ROS 2 Jazzy 문서 — How-to guides: Using ros2 param; Launch file different formats.
- colcon 문서 — build verb(`--symlink-install`, `--merge-install`, `--continue-on-error`); Package selection arguments(`--packages-select`, `--packages-up-to`); What is a Workspace?; Overriding Packages.
- `ament_cmake_python` README — `ament_python_install_package`, `ament_python_install_module`.
- `rosdep` 커맨드라인 옵션(`--from-paths`, `--ignore-src`, `-r`, `-y`).
- REP-149 — package format 3 의존 태그.

> [!question]- 스스로 점검 · 정답
> **1. Python 노드를 고치고 `colcon build` 후 다시 launch했는데 아무것도 안 바뀐다. 원인 셋과, 그것들을 가르는 명령 하나를 대라.** 빌드가 이 패키지를 포함하지 않았거나(`--packages-select`를 다른 패키지에 걸었거나), 셸이 워크스페이스가 아니라 `/opt/ros/jazzy`에서 패키지를 해석하고 있거나, 빌드가 실패했는데 요약 줄만 읽었다. 실행 셸에서 `python3 -c "import <pkg>.<module> as m; print(m.__file__)"`가 실제로 로드되는 파일을 알려 주고, `ros2 pkg prefix <pkg>`가 어느 워크스페이스가 이겼는지 알려 준다.
> **2. `--symlink-install`은 왜 Python은 고치고 C++은 못 고치나?** `ament_python` 패키지에서는 colcon이 setuptools의 `develop` 단계를 돌리므로 설치된 모듈 경로가 `src/`로 되돌아 해석된다. C++ 패키지의 설치 산출물은 컴파일된 바이너리이고, 가리킬 소스 파일이 없으므로 새 바이너리에는 컴파일이 필요하다. CMake 패키지가 설치하는 데이터 파일 — launch, YAML, URDF — 은 링크되고 소스를 따라간다.
> **3. YAML 파라미터 파일이 에러 없이 로드되는데 아무 파라미터도 설정되지 않는다. 먼저 확인할 두 가지는?** 최상위 키가 네임스페이스를 포함한 노드의 완전 수식 이름이어야 한다(`/sensor`가 아니라 `/demo/sensor`), 그리고 파라미터가 밑줄 두 개짜리 `ros__parameters` 아래에 있어야 한다. 둘 다 조용히 실패한다. 파라미터가 정말 모든 노드용이면 최상위 키 `/**`가 첫 번째 문제를 비켜 간다.
> **4. 순수 Python 패키지는 왜 `<depend>`가 아니라 `<exec_depend>`를 써야 하나?** `<depend>`는 빌드와 실행 양쪽에 필요한 의존성을 선언하는데, 순수 Python 패키지에는 빌드 국면이 없다. 없는 빌드 의존성을 선언하면 워크스페이스 빌드 순서가 필요 이상으로 제약되고, 설치된 패키지가 실제로 무엇을 요구하는지도 잘못 표현한다.
