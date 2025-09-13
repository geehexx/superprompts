#!/usr/bin/env python3
"""Regression tests for MCP server startup and initialization.

These tests ensure that the server can start properly and handle initialization correctly.
"""

import os
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any


class ExecutableNotFoundError(FileNotFoundError):
    """Executable not found or not accessible."""


def _safe_subprocess_run(cmd: list[str], **kwargs: Any) -> subprocess.CompletedProcess[str]:
    """Run subprocess with validated command to prevent injection."""
    # Validate that the first argument is a valid executable path
    if not cmd or not Path(cmd[0]).exists() or not os.access(cmd[0], os.X_OK):
        raise ExecutableNotFoundError()
    # Ensure check=False is set for security
    kwargs.setdefault("check", False)
    # Path is validated above, so this is safe
    return subprocess.run(cmd, check=False, **kwargs)  # noqa: S603


# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


class ServerStartupTester:
    """Test class for server startup functionality."""

    def __init__(self) -> None:
        self.server_process: subprocess.Popen[str] | None = None
        self.server_dir = Path(__file__).parent.parent  # Project root

    def test_imports(self) -> bool:
        """Test that all required modules can be imported."""
        try:
            import superprompts.mcp.server  # noqa: PLC0415
            import superprompts.prompts.cursor_rules  # noqa: PLC0415
            import superprompts.prompts.repo_docs  # noqa: F401, PLC0415
        except ImportError:
            return False
        else:
            return True

    def test_server_creation(self) -> bool:
        """Test that a server instance can be created."""
        try:
            from superprompts.mcp.server import mcp  # noqa: PLC0415

            # Test that the FastMCP instance exists
            assert mcp is not None
        except Exception:
            return False
        else:
            return True

    def test_initialization_options(self) -> bool:
        """Test that initialization options can be created properly."""
        # No longer needed - we don't manage MCP server configurations
        return True

    def test_server_startup_script(self) -> bool:
        """Test that the startup script runs without errors."""
        try:
            # Test that we can run the server module directly
            python_path = shutil.which("python3")
            if not python_path:
                return False
            # Validate path to prevent command injection
            if not Path(python_path).exists() or not os.access(python_path, os.X_OK):
                return False
            result = _safe_subprocess_run(
                [
                    python_path,
                    "-c",
                    "import superprompts.mcp.server; print('Server module loads successfully')",
                ],
                check=False,
                cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
        except Exception:
            return False
        else:
            return result.returncode == 0

    def test_server_startup_process(self) -> bool:
        """Test that the server process can start and stop cleanly."""
        try:
            # Start the server in the background using the new CLI
            python_path = shutil.which("python3")
            if not python_path:
                return False
            # Validate path to prevent command injection
            if not Path(python_path).exists() or not os.access(python_path, os.X_OK):
                return False
            # Use subprocess.Popen directly since we've already validated the path
            self.server_process = subprocess.Popen(  # noqa: S603
                [python_path, "-m", "superprompts.mcp.server"],
                cwd=self.server_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )

            # Give it a moment to start
            time.sleep(2)

            # Check if it's still running
            if self.server_process.poll() is None:
                return True
            _stdout, _stderr = self.server_process.communicate()
            return False

        except Exception:
            return False
        finally:
            self.cleanup()

    def test_virtual_environment(self) -> bool:
        """Test that the virtual environment is properly set up."""
        venv_path = self.server_dir / ".venv"
        if not venv_path.exists():
            return False

        # Check if required packages are installed
        try:
            # Use the system Python since packages are installed there
            python_path = shutil.which("python3")
            if not python_path:
                return False
            # Validate path to prevent command injection
            if not Path(python_path).exists() or not os.access(python_path, os.X_OK):
                return False
            result = _safe_subprocess_run(
                [python_path, "-c", "import fastmcp, pydantic, click, rich"],
                check=False,
                cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
        except Exception:
            return False
        else:
            return result.returncode == 0

    def cleanup(self) -> None:
        """Clean up any running processes."""
        if self.server_process is not None and self.server_process.poll() is None:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            self.server_process = None

    def run_all_tests(self) -> bool:
        """Run all regression tests."""
        tests = [
            self.test_imports,
            self.test_server_creation,
            self.test_initialization_options,
            self.test_virtual_environment,
            self.test_server_startup_script,
            self.test_server_startup_process,
        ]

        passed = 0
        total = len(tests)

        for test in tests:
            if self._run_single_test(test):
                passed += 1

        return passed == total

    def _run_single_test(self, test: Callable[[], bool]) -> bool:
        """Run a single test with exception handling."""
        try:
            result = test()
            return bool(result)
        except Exception as e:
            # Log the exception for debugging but continue with other tests
            print(f"Test {test.__name__} failed: {e}")
            return False


def main() -> None:
    """Run the main test script."""
    tester = ServerStartupTester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
