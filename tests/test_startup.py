#!/usr/bin/env python3
"""Regression tests for MCP server startup and initialization.

These tests ensure that the server can start properly and handle initialization correctly.
"""

import subprocess
import sys
import time
from pathlib import Path

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
            import superprompts.mcp.config
            import superprompts.mcp.server
            import superprompts.prompts.cursor_rules
            import superprompts.prompts.repo_docs

            return True
        except ImportError:
            return False

    def test_server_creation(self) -> bool:
        """Test that a server instance can be created."""
        try:
            from superprompts.mcp.server import mcp

            # Test that the FastMCP instance exists
            assert mcp is not None
            return True
        except Exception:
            return False

    def test_initialization_options(self) -> bool:
        """Test that initialization options can be created properly."""
        try:
            from superprompts.mcp.config import MCPServerConfig

            # Test creating a server config
            config = MCPServerConfig(name="test_server", command="python", args=["-m", "test.server"])
            assert config.name == "test_server"
            return True
        except Exception:
            return False

    def test_server_startup_script(self) -> bool:
        """Test that the startup script runs without errors."""
        try:
            # Test that we can run the server module directly
            result = subprocess.run(
                [
                    "python3",
                    "-c",
                    "import superprompts.mcp.server; print('Server module loads successfully')",
                ],
                check=False,
                cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

    def test_server_startup_process(self) -> bool:
        """Test that the server process can start and stop cleanly."""
        try:
            # Start the server in the background using the new CLI
            self.server_process = subprocess.Popen(
                ["python3", "-m", "superprompts.mcp.server"],
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
            result = subprocess.run(
                ["python3", "-c", "import fastmcp, pydantic, click, rich"],
                check=False,
                cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
            return result.returncode == 0
        except Exception:
            return False

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
            try:
                if test():
                    passed += 1
            except Exception:
                pass

        return passed == total


def main() -> None:
    """Main entry point for the test script."""
    tester = ServerStartupTester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
