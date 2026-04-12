#!/usr/bin/env python3
"""
Unity-Claude onboarding script.

Handles all deterministic onboarding steps: file creation, git init, Unity project
creation, package installation, directory scaffolding, and template rendering.
Claude invokes this after gathering project info from the developer.
"""

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.request

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")

UNITY_GITIGNORE_URL = (
    "https://raw.githubusercontent.com/github/gitignore/main/Unity.gitignore"
)

MINIMAL_GITIGNORE = """\
# Unity
[Ll]ibrary/
[Tt]emp/
[Oo]bj/
[Bb]uild/
[Bb]uilds/
[Ll]ogs/
[Uu]ser[Ss]ettings/
*.csproj
*.sln
*.suo
*.tmp
*.user
*.userprefs
*.pidb
*.booproj
*.svd
*.pdb
*.mdb
*.opendb
*.VC.db
*.pidb.meta
*.pdb.meta
*.mdb.meta
sysinfo.txt
crashlytics-build.properties
"""

# macOS Unity Hub path
UNITY_HUB_PATH = "/Applications/Unity Hub.app/Contents/MacOS/Unity Hub"

EXIT_SUCCESS = 0
EXIT_ARGS = 1
EXIT_ALREADY_ONBOARDED = 2
EXIT_STEP_FAILURE = 3

# Convention skills list (always the same set, conditionals handled by template engine)
CONVENTIONS_ALWAYS = [
    ("unity-coding-conventions", "Writing C# code"),
    ("unity-architecture-conventions", "Dependency direction, orchestration, event patterns"),
    ("unity-performance", "Allocations, hot paths, GC pressure"),
    ("unity-folder-conventions", "Creating files or folders"),
    ("unity-mcp-tools", "Interacting with Unity Editor via MCP"),
    ("unity-ugui-development", "Writing UGUI code"),
]

CONVENTIONS_ZENJECT = [
    ("zenject-conventions", "Writing Zenject code"),
]

CONVENTIONS_CONTEXT = [
    ("unity-context-system", "Reading or navigating project code"),
]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class OnboardError(Exception):
    """Raised when a step fails."""

    def __init__(self, step: str, message: str):
        self.step = step
        self.message = message
        super().__init__(f"[{step}] {message}")


# ---------------------------------------------------------------------------
# Template Engine
# ---------------------------------------------------------------------------


def build_conventions_list(zenject: bool, context_system: str) -> str:
    """Build the markdown conventions list."""
    lines = []
    for name, trigger in CONVENTIONS_ALWAYS:
        lines.append(f"- `{name}` — {trigger}")
    if zenject:
        for name, trigger in CONVENTIONS_ZENJECT:
            lines.append(f"- `{name}` — {trigger}")
    if context_system != "none":
        for name, trigger in CONVENTIONS_CONTEXT:
            lines.append(f"- `{name}` — {trigger}")
    return "\n".join(lines)


def _eval_condition(var: str, op: str, val: str, variables: dict) -> bool:
    """Evaluate a single [If] condition."""
    actual = variables.get(var, "")
    return (actual == val) if op == "=" else (actual != val)


def _process_inline_conditionals(line: str, variables: dict) -> str | None:
    """
    Process all inline [If VAR = VALUE]:rest on a single line.
    Returns the processed line, or None if the entire line should be removed.

    Two inline forms:
    - [If X = Y]:text[/If]  → bounded: only 'text' is conditional, rest continues
    - [If X = Y]:text        → unbounded: 'text' runs to next '[' or end of line

    If condition true, replace marker with text. If false, remove that segment.
    If removing a segment leaves the line empty/whitespace-only, remove the whole line.
    """
    # First pass: bounded conditionals [If ...]:text[/If]
    bounded = re.compile(r"\[If\s+(\w+)\s*(=|!=)\s*(\w+)\]:(.*?)\[/If\]")

    def bounded_replacer(m):
        var, op, val, text = m.groups()
        if _eval_condition(var, op, val, variables):
            return text
        return ""

    line = bounded.sub(bounded_replacer, line)

    # Second pass: unbounded conditionals [If ...]:text (to next [ or EOL)
    unbounded = re.compile(r"\[If\s+(\w+)\s*(=|!=)\s*(\w+)\]:([^\[]*)")

    def unbounded_replacer(m):
        var, op, val, text = m.groups()
        if _eval_condition(var, op, val, variables):
            return text
        return ""

    result = unbounded.sub(unbounded_replacer, line)

    # If the line became empty or whitespace-only after processing, remove it
    if not result.strip() and line.strip():
        return None
    return result


def render_template(template_text: str, variables: dict) -> str:
    """
    Two-pass template rendering.

    Pass 1: Process conditionals.
      - Inline: [If X = Y]:rest  → if true, output rest; if false, remove segment
      - Block: [If X = Y] on its own line → gates lines until [EndIf]
      - [EndIf] on its own line → ends the current block

    Pass 2: Replace [PLACEHOLDER] with values.
    """
    lines = template_text.split("\n")
    result = []
    skip_depth = 0  # How many nested false-blocks we're inside

    # Pass 1: Conditionals
    for line in lines:
        stripped = line.strip()

        # Check for [EndIf]
        if stripped == "[EndIf]":
            if skip_depth > 0:
                skip_depth -= 1
            continue

        # Check for standalone [If VAR = VALUE] (block opener)
        m = re.match(r"^\s*\[If\s+(\w+)\s*(=|!=)\s*(\w+)\]\s*$", line)
        if m:
            if skip_depth > 0:
                # Already inside a false block — nest deeper
                skip_depth += 1
            else:
                var, op, val = m.groups()
                if not _eval_condition(var, op, val, variables):
                    skip_depth = 1
            continue

        # If inside a false block, skip this line
        if skip_depth > 0:
            continue

        # Process inline conditionals
        processed = _process_inline_conditionals(line, variables)
        if processed is not None:
            result.append(processed)

    text = "\n".join(result)

    # Pass 2: Variable substitution
    for key, value in variables.items():
        text = text.replace(f"[{key}]", value)

    return text


def load_template(name: str) -> str:
    """Load a template file by name from the templates directory."""
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r") as f:
        return f.read()


def render_template_file(name: str, variables: dict) -> str:
    """Load and render a template."""
    return render_template(load_template(name), variables)


# ---------------------------------------------------------------------------
# Asmdef Zenject Handling
# ---------------------------------------------------------------------------


def filter_asmdef_zenject(content: str, zenject: bool) -> str:
    """
    If zenject is false, parse the asmdef JSON, remove Zenject references,
    and re-serialize.
    """
    if zenject:
        return content

    data = json.loads(content)
    zenject_refs = {"Zenject", "Zenject.TestFramework"}
    if "references" in data:
        data["references"] = [
            r for r in data["references"] if r not in zenject_refs
        ]
    return json.dumps(data, indent=4) + "\n"


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------


def run_cmd(
    cmd: list,
    step: str,
    cwd: str | None = None,
    fatal: bool = True,
    timeout: int = 120,
    capture: bool = True,
) -> subprocess.CompletedProcess | None:
    """Run a command, optionally fatal on failure."""
    try:
        result = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=capture,
            text=True,
            timeout=timeout,
        )
        if result.returncode != 0 and fatal:
            stderr = result.stderr.strip() if result.stderr else ""
            raise OnboardError(step, f"Command failed: {' '.join(cmd)}\n{stderr}")
        return result
    except FileNotFoundError:
        if fatal:
            raise OnboardError(step, f"Command not found: {cmd[0]}")
        print(f"  WARNING: {cmd[0]} not found, skipping")
        return None
    except subprocess.TimeoutExpired:
        if fatal:
            raise OnboardError(step, f"Command timed out after {timeout}s: {' '.join(cmd)}")
        print(f"  WARNING: Command timed out: {' '.join(cmd)}")
        return None


def write_file(path: str, content: str, dry_run: bool = False) -> None:
    """Write content to a file, creating parent directories."""
    if dry_run:
        print(f"  WRITE {path} ({len(content)} bytes)")
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
    print(f"  Created {path}")


def make_dirs(path: str, dry_run: bool = False) -> None:
    """Create a directory tree."""
    if dry_run:
        print(f"  MKDIR {path}")
        return
    os.makedirs(path, exist_ok=True)


# ---------------------------------------------------------------------------
# Unity Editor Discovery
# ---------------------------------------------------------------------------


def find_unity_editor(editor_version: str | None, step: str) -> str:
    """Find the Unity editor binary path."""
    if not os.path.exists(UNITY_HUB_PATH):
        raise OnboardError(step, "Unity Hub not found at expected path. Install Unity Hub first.")

    result = run_cmd(
        [UNITY_HUB_PATH, "--", "--headless", "editors", "--installed"],
        step,
        fatal=True,
    )
    if not result or not result.stdout.strip():
        raise OnboardError(step, "No Unity editors installed. Install one via Unity Hub.")

    # Parse output: lines like "6000.3.6f1  (Apple silicon) installed at /path/to/Unity.app"
    editors = {}
    for line in result.stdout.strip().split("\n"):
        line = line.strip()
        if not line or "installed at" not in line:
            continue
        # Extract version (first token) and path (after "installed at")
        version = line.split()[0].strip()
        m = re.search(r"installed at\s+(.+)", line)
        if m:
            app_path = m.group(1).strip()
            # Unity.app → Unity.app/Contents/MacOS/Unity
            if app_path.endswith(".app"):
                app_path = os.path.join(app_path, "Contents", "MacOS", "Unity")
            editors[version] = app_path

    if not editors:
        raise OnboardError(step, f"Could not parse installed editors from:\n{result.stdout}")

    if editor_version:
        if editor_version in editors:
            return editors[editor_version]
        raise OnboardError(
            step,
            f"Editor version {editor_version} not found. Available: {', '.join(editors.keys())}",
        )

    # Use the latest (last in the dict, or sort by version)
    version = sorted(editors.keys())[-1]
    print(f"  Using Unity {version}")
    return editors[version]


# ---------------------------------------------------------------------------
# Step Functions
# ---------------------------------------------------------------------------


def step_prechecks(project_dir: str, state: str) -> None:
    """Check if already onboarded."""
    constants_path = os.path.join(project_dir, ".claude", "State", "Constants.md")
    if os.path.exists(constants_path):
        raise OnboardError("pre-checks", "Project already onboarded (Constants.md exists)")

    if state == "greenfield":
        assets_path = os.path.join(project_dir, "Assets")
        if os.path.exists(assets_path):
            raise OnboardError(
                "pre-checks",
                "Assets/ already exists but state=greenfield. Use --state existing for existing projects.",
            )


def step_constants(project_dir: str, variables: dict, state: str, dry_run: bool) -> None:
    """Create Constants.md from template."""
    template_name = "constants-existing.md.template" if state == "existing" else "constants.md.template"
    content = render_template_file(template_name, variables)
    write_file(
        os.path.join(project_dir, ".claude", "State", "Constants.md"),
        content,
        dry_run,
    )


def step_git_init(project_dir: str, dry_run: bool) -> None:
    """Initialize git repo and .gitignore."""
    if dry_run:
        print("  RUN git init")
        print("  DOWNLOAD .gitignore")
        print("  APPEND Claude Code entries to .gitignore")
        return

    run_cmd(["git", "init"], "git-init", cwd=project_dir)

    # Download Unity .gitignore
    gitignore_path = os.path.join(project_dir, ".gitignore")
    try:
        req = urllib.request.Request(UNITY_GITIGNORE_URL)
        with urllib.request.urlopen(req, timeout=10) as resp:
            gitignore_content = resp.read().decode("utf-8")
    except Exception:
        print("  WARNING: Could not download Unity .gitignore, using minimal fallback")
        gitignore_content = MINIMAL_GITIGNORE

    # Append Claude Code entries
    claude_append = load_template("gitignore-append.template")
    gitignore_content += claude_append

    with open(gitignore_path, "w") as f:
        f.write(gitignore_content)
    print("  Created .gitignore")


def step_github_repo(project_dir: str, repo_name: str, dry_run: bool) -> None:
    """Create GitHub repo (non-fatal)."""
    if dry_run:
        print(f"  RUN gh repo create {repo_name} --private --source . --push")
        return

    run_cmd(
        ["gh", "repo", "create", repo_name, "--private", "--source", ".", "--push"],
        "github-repo",
        cwd=project_dir,
        fatal=False,
    )


def step_git_commit(project_dir: str, message: str, dry_run: bool) -> None:
    """Stage all and commit."""
    if dry_run:
        print(f"  RUN git add -A && git commit -m '{message}'")
        return

    run_cmd(["git", "add", "-A"], "git-commit", cwd=project_dir)
    # Check if there's anything to commit
    result = run_cmd(
        ["git", "diff", "--cached", "--quiet"],
        "git-commit",
        cwd=project_dir,
        fatal=False,
    )
    if result and result.returncode == 0:
        print(f"  Nothing to commit for: {message}")
        return
    run_cmd(["git", "commit", "-m", message], "git-commit", cwd=project_dir)


def step_git_push(project_dir: str, dry_run: bool) -> None:
    """Push to remote if one exists (non-fatal)."""
    if dry_run:
        print("  RUN git push")
        return

    # Check if remote exists
    result = run_cmd(
        ["git", "remote"],
        "git-push",
        cwd=project_dir,
        fatal=False,
    )
    if not result or not result.stdout.strip():
        return

    run_cmd(["git", "push"], "git-push", cwd=project_dir, fatal=False)


def step_unity_create(
    project_dir: str, editor_version: str | None, dry_run: bool
) -> None:
    """Create Unity project via editor binary."""
    if dry_run:
        print("  DISCOVER Unity editor")
        print(f"  RUN <editor> -createProject {project_dir} -quit -batchmode")
        return

    editor_path = find_unity_editor(editor_version, "unity-create")

    print("  Creating Unity project (this may take a few minutes)...")
    run_cmd(
        [editor_path, "-createProject", project_dir, "-quit", "-batchmode"],
        "unity-create",
        timeout=300,
    )

    # Verify
    if not os.path.exists(os.path.join(project_dir, "Assets")):
        raise OnboardError("unity-create", "Unity project creation failed — Assets/ not found")

    print("  Unity project created successfully")


def step_unity_open(
    project_dir: str, editor_version: str | None, dry_run: bool
) -> None:
    """Open Unity editor (background, non-blocking)."""
    if dry_run:
        print(f"  RUN <editor> -projectPath {project_dir} (background)")
        return

    editor_path = find_unity_editor(editor_version, "unity-open")

    subprocess.Popen(
        [editor_path, "-projectPath", project_dir],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    print("  Unity editor opening in background")


def step_packages(project_dir: str, zenject: bool, dry_run: bool) -> None:
    """Install OpenUPM packages."""
    if dry_run:
        print("  RUN openupm add com.ivanmurzak.unity.mcp")
        print("  RUN openupm add com.cysharp.unitask")
        if zenject:
            print("  RUN openupm add com.svermeulen.extenject")
        return

    # Check openupm
    result = run_cmd(["openupm", "--version"], "packages", fatal=False)
    if not result or result.returncode != 0:
        # Try to install via npm
        print("  OpenUPM CLI not found, installing via npm...")
        run_cmd(["npm", "install", "-g", "openupm-cli"], "packages", fatal=True)

    packages = [
        "com.ivanmurzak.unity.mcp",
        "com.cysharp.unitask",
    ]
    if zenject:
        packages.append("com.svermeulen.extenject")

    for pkg in packages:
        print(f"  Installing {pkg}...")
        run_cmd(["openupm", "add", pkg], "packages", cwd=project_dir, fatal=False)


def step_directories(project_dir: str, project_name: str, tests: bool, dry_run: bool) -> None:
    """Create the Assets directory structure."""
    dirs = [
        os.path.join(project_dir, "Assets", "Plugins"),
        os.path.join(project_dir, "Assets", f"_{project_name}", "Shared", "Scripts"),
        os.path.join(project_dir, "Assets", "_Core", "Editor", "Scripts", "AutomationHelpers"),
        os.path.join(project_dir, "Assets", "_Core", "Shared", "Scripts"),
        os.path.join(project_dir, "Assets", "Settings"),
    ]
    if tests:
        dirs.extend([
            os.path.join(project_dir, "Assets", f"_{project_name}", "Tests", "Editor"),
            os.path.join(project_dir, "Assets", f"_{project_name}", "Tests", "Runtime"),
        ])

    for d in dirs:
        make_dirs(d, dry_run)


def step_asmdefs(
    project_dir: str, variables: dict, zenject: bool, tests: bool, dry_run: bool
) -> None:
    """Create assembly definition files."""
    project_name = variables["ProjectName"]

    asmdef_map = {
        "asmdef/Core.asmdef.template": os.path.join(
            project_dir, "Assets", "_Core", "Core.asmdef"
        ),
        "asmdef/Core.Editor.asmdef.template": os.path.join(
            project_dir, "Assets", "_Core", "Editor", "Core.Editor.asmdef"
        ),
        "asmdef/Project.asmdef.template": os.path.join(
            project_dir, "Assets", f"_{project_name}", f"{project_name}.asmdef"
        ),
    }

    if tests:
        asmdef_map["asmdef/Project.Tests.Editor.asmdef.template"] = os.path.join(
            project_dir,
            "Assets",
            f"_{project_name}",
            "Tests",
            "Editor",
            f"{project_name}.Tests.Editor.asmdef",
        )
        asmdef_map["asmdef/Project.Tests.Runtime.asmdef.template"] = os.path.join(
            project_dir,
            "Assets",
            f"_{project_name}",
            "Tests",
            "Runtime",
            f"{project_name}.Tests.Runtime.asmdef",
        )

    for template_name, output_path in asmdef_map.items():
        content = render_template_file(template_name, variables)
        content = filter_asmdef_zenject(content, zenject)
        write_file(output_path, content, dry_run)


def step_core_scripts(project_dir: str, variables: dict, dry_run: bool) -> None:
    """Create ContextInfo.cs and ScriptExecutor.cs."""
    scripts = {
        "contextinfo.cs.template": os.path.join(
            project_dir, "Assets", "_Core", "Shared", "Scripts", "ContextInfo.cs"
        ),
        "scriptexecutor.cs.template": os.path.join(
            project_dir,
            "Assets",
            "_Core",
            "Editor",
            "Scripts",
            "AutomationHelpers",
            "ScriptExecutor.cs",
        ),
    }

    for template_name, output_path in scripts.items():
        content = render_template_file(template_name, variables)
        write_file(output_path, content, dry_run)


def step_aiflow(project_dir: str, workflow: str, variables: dict, dry_run: bool) -> None:
    """Generate AIFlow.md from the workflow-specific template."""
    template_map = {
        "driven": "aiflow-driven.md.template",
        "assisted": "aiflow-assisted.md.template",
        "limited": "aiflow-limited.md.template",
    }
    template_name = template_map[workflow]
    content = render_template_file(template_name, variables)
    write_file(
        os.path.join(project_dir, ".claude", "AIFlow.md"),
        content,
        dry_run,
    )


def step_claudemd(project_dir: str, variables: dict, dry_run: bool) -> None:
    """Generate CLAUDE.md from template."""
    content = render_template_file("claudemd.md.template", variables)
    write_file(
        os.path.join(project_dir, ".claude", "CLAUDE.md"),
        content,
        dry_run,
    )


def step_planning_stubs(project_dir: str, dry_run: bool) -> None:
    """Create empty planning files for driven mode."""
    planning_dir = os.path.join(project_dir, ".claude", "Planning")
    history_dir = os.path.join(planning_dir, "History")

    make_dirs(history_dir, dry_run)

    stubs = {
        os.path.join(planning_dir, "ProjectPlan.md"): "# Project Plan\n",
        os.path.join(planning_dir, "CurrentIteration.md"): "# Current Iteration\n",
        os.path.join(planning_dir, "IterationHistory.md"): "# Iteration History\n",
    }

    for path, content in stubs.items():
        write_file(path, content, dry_run)


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


def run_greenfield(args, variables: dict) -> None:
    """Execute greenfield onboarding flow."""
    project_dir = args.project_dir
    dry_run = args.dry_run

    # Pre-checks
    print("Step: Pre-checks")
    step_prechecks(project_dir, "greenfield")

    # Constants.md
    print("Step: Constants.md")
    step_constants(project_dir, variables, "greenfield", dry_run)

    # Git init
    if not args.skip_git:
        print("Step: Git init")
        step_git_init(project_dir, dry_run)

        print("Step: Initial commit")
        step_git_commit(project_dir, "[Pipeline] Initialize project", dry_run)

        # Create GitHub repo after initial commit so --push has something to push
        repo_name = os.path.basename(os.path.abspath(project_dir))
        print("Step: GitHub repo")
        step_github_repo(project_dir, repo_name, dry_run)

    # Unity project creation
    if not args.skip_unity_create:
        print("Step: Create Unity project")
        step_unity_create(project_dir, args.editor_version, dry_run)

        print("Step: Open Unity")
        step_unity_open(project_dir, args.editor_version, dry_run)

        if not args.skip_git:
            print("Step: Commit Unity project")
            step_git_commit(project_dir, "[Pipeline] Create Unity project", dry_run)

    # Packages
    if not args.skip_packages:
        print("Step: Install packages")
        step_packages(project_dir, args.zenject, dry_run)

        if not args.skip_git:
            print("Step: Commit packages")
            step_git_commit(project_dir, "[Pipeline] Install packages", dry_run)

    # Scaffold
    print("Step: Create directories")
    step_directories(project_dir, args.name, args.tests, dry_run)

    print("Step: Create assembly definitions")
    step_asmdefs(project_dir, variables, args.zenject, args.tests, dry_run)

    print("Step: Create core scripts")
    step_core_scripts(project_dir, variables, dry_run)

    # AIFlow.md
    print("Step: Generate AIFlow.md")
    step_aiflow(project_dir, args.workflow, variables, dry_run)

    # CLAUDE.md
    print("Step: Generate CLAUDE.md")
    step_claudemd(project_dir, variables, dry_run)

    # Planning stubs (driven only)
    if args.workflow == "driven":
        print("Step: Create planning stubs")
        step_planning_stubs(project_dir, dry_run)

    # Final scaffold commit + push everything
    if not args.skip_git:
        print("Step: Commit scaffold")
        step_git_commit(project_dir, "[Pipeline] Scaffold project", dry_run)

        print("Step: Push")
        step_git_push(project_dir, dry_run)

    print("\nOnboarding (script portion) complete.")


def run_existing(args, variables: dict) -> None:
    """Execute existing project onboarding flow."""
    project_dir = args.project_dir
    dry_run = args.dry_run

    # Pre-checks
    print("Step: Pre-checks")
    constants_path = os.path.join(project_dir, ".claude", "State", "Constants.md")
    if os.path.exists(constants_path):
        raise OnboardError("pre-checks", "Project already onboarded (Constants.md exists)")

    # Constants.md
    print("Step: Constants.md")
    step_constants(project_dir, variables, "existing", dry_run)

    # AIFlow.md
    print("Step: Generate AIFlow.md")
    step_aiflow(project_dir, "limited", variables, dry_run)

    # CLAUDE.md
    print("Step: Generate CLAUDE.md")
    step_claudemd(project_dir, variables, dry_run)

    # Commit
    if not args.skip_git:
        print("Step: Commit")
        step_git_commit(
            project_dir,
            "[Pipeline] Onboard existing project (limited mode)",
            dry_run,
        )

    print("\nOnboarding (script portion) complete.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_bool(value: str) -> bool:
    """Parse a boolean string."""
    if value.lower() in ("true", "1", "yes"):
        return True
    if value.lower() in ("false", "0", "no"):
        return False
    raise argparse.ArgumentTypeError(f"Invalid boolean value: {value}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Unity-Claude onboarding: deterministic project setup.",
    )

    # Required
    parser.add_argument("--project-dir", required=True, help="Path to project directory")
    parser.add_argument("--name", required=True, help="Project name (PascalCase)")
    parser.add_argument("--company", required=True, help="Company/username for namespaces")
    parser.add_argument(
        "--scope",
        required=True,
        choices=["prototype", "small", "medium", "large", "very-large", "unknown"],
    )
    parser.add_argument(
        "--state", required=True, choices=["greenfield", "existing"]
    )
    parser.add_argument(
        "--ownership",
        required=True,
        choices=["solo", "team-owner", "team-ai-driven", "team"],
    )
    parser.add_argument(
        "--workflow", required=True, choices=["driven", "assisted", "limited"]
    )

    # Conditionally required (greenfield)
    parser.add_argument("--tests", type=parse_bool, default=None)
    parser.add_argument(
        "--context-system", choices=["inline", "none"], default=None
    )

    # Optional
    parser.add_argument("--zenject", type=parse_bool, default=False)
    parser.add_argument("--description", default="")
    parser.add_argument("--editor-version", default=None)

    # Flags
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--skip-unity-create", action="store_true")
    parser.add_argument("--skip-packages", action="store_true")
    parser.add_argument("--dry-run", action="store_true", help="Print actions without executing")

    args = parser.parse_args()

    # Validate conditionally required args for greenfield
    if args.state == "greenfield":
        if args.tests is None:
            parser.error("--tests is required for greenfield projects")
        if args.context_system is None:
            parser.error("--context-system is required for greenfield projects")

    # Defaults for existing
    if args.state == "existing":
        if args.tests is None:
            args.tests = False
        if args.context_system is None:
            args.context_system = "none"

    # Resolve project dir to absolute
    args.project_dir = os.path.abspath(args.project_dir)

    return args


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main() -> int:
    args = parse_args()

    # Build template variables
    conventions_list = build_conventions_list(args.zenject, args.context_system)
    variables = {
        "ProjectName": args.name,
        "CompanyName": args.company,
        "PROJECT_NAME": args.name,
        "PROJECT_DESCRIPTION": args.description if args.description else "[PROJECT_DESCRIPTION]",
        "SCOPE": args.scope,
        "OWNERSHIP": args.ownership,
        "WORKFLOW": args.workflow,
        "CONTEXT_SYSTEM": args.context_system or "none",
        "TESTS": str(args.tests).lower(),
        "ZENJECT": str(args.zenject).lower(),
        "CONVENTIONS_LIST": conventions_list,
    }

    if args.dry_run:
        print("=== DRY RUN ===")
        print(f"Project: {args.name} ({args.state})")
        print(f"Directory: {args.project_dir}")
        print(f"Workflow: {args.workflow}")
        print()

    try:
        if args.state == "existing":
            run_existing(args, variables)
        else:
            run_greenfield(args, variables)
    except OnboardError as e:
        print(f"\nERROR [{e.step}]: {e.message}", file=sys.stderr)
        if "already onboarded" in e.message:
            return EXIT_ALREADY_ONBOARDED
        return EXIT_STEP_FAILURE

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
