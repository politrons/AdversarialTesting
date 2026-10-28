"""Launch the real Promptfoo CLI using the active Python environment."""

import os
import shutil
import subprocess
import sys

from adversarial_testing import PROJECT_ROOT


def evaluate() -> int:
    promptfoo_executable = PROJECT_ROOT / "node_modules" / ".bin" / "promptfoo"
    if not promptfoo_executable.is_file() or shutil.which("node") is None:
        print("Install Node.js >=22.22.0 and run npm ci first.", file=sys.stderr)
        return 2

    environment = create_environment()
    # Prepare promptfoo command pointing to config/promptfooconfig.yaml to know
    # which providers needs to be executed and which test case use.
    promptfoo_command = [
        str(promptfoo_executable), "eval", "--config", "config/promptfooconfig.yaml",
        "--no-cache", "--no-share", "--max-concurrency", "1",
        "--table-cell-max-length", "300",
    ]
    result = subprocess.run(
        promptfoo_command, cwd=PROJECT_ROOT, env=environment, check=False
    )
    return result.returncode


def create_environment() -> dict[str, str]:
    """
    Create the environment for the promptfoo
    """
    environment = os.environ.copy()
    environment.update(
        PROMPTFOO_PYTHON=sys.executable,
        PROMPTFOO_CONFIG_DIR=str(PROJECT_ROOT / ".promptfoo"),
        PROMPTFOO_DISABLE_TELEMETRY="1",
        PROMPTFOO_DISABLE_UPDATE="1",
    )
    source_path = str(PROJECT_ROOT / "src")
    environment["PYTHONPATH"] = os.pathsep.join(
        filter(None, [source_path, environment.get("PYTHONPATH")])
    )
    return environment
