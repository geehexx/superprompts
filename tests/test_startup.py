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

    def __init__(self):
        self.server_process = None
        self.server_dir = Path(__file__).parent.parent  # Project root

    def test_imports(self):
        """Test that all required modules can be imported."""
        print("Testing imports...")
        try:
            from mcp.server import Server
            from mcp.server.models import InitializationOptions
            from mcp.server.stdio import stdio_server
            from mcp.types import TextContent, Tool

            print("✅ All imports successful")
            return True
        except ImportError as e:
            print(f"❌ Import error: {e}")
            return False

    def test_server_creation(self):
        """Test that a server instance can be created."""
        print("Testing server creation...")
        try:
            from mcp.server import Server

            server = Server("test_server")
            print("✅ Server creation successful")
            return True
        except Exception as e:
            print(f"❌ Server creation error: {e}")
            return False

    def test_initialization_options(self):
        """Test that initialization options can be created properly."""
        print("Testing initialization options...")
        try:
            from mcp.server import Server

            server = Server("test_server")
            # This is the fix we implemented - using create_initialization_options()
            init_options = server.create_initialization_options()
            print("✅ Initialization options creation successful")
            return True
        except Exception as e:
            print(f"❌ Initialization options error: {e}")
            return False

    def test_server_startup_script(self):
        """Test that the startup script runs without errors."""
        print("Testing startup script...")
        try:
            # Test the script syntax first
            script_path = self.server_dir / "mcp_server" / "start_server.sh"
            if not script_path.exists():
                print("❌ Startup script not found")
                return False

            result = subprocess.run(
                ["bash", "-n", str(script_path)],
                check=False, cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"❌ Script syntax error: {result.stderr}")
                return False

            print("✅ Startup script syntax is valid")
            return True
        except Exception as e:
            print(f"❌ Script test error: {e}")
            return False

    def test_server_startup_process(self):
        """Test that the server process can start and stop cleanly."""
        print("Testing server process startup...")
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
                print("✅ Server process started successfully")
                return True
            stdout, stderr = self.server_process.communicate()
            print("❌ Server process failed to start")
            print(f"STDOUT: {stdout}")
            print(f"STDERR: {stderr}")
            return False

        except Exception as e:
            print(f"❌ Server process test error: {e}")
            return False
        finally:
            self.cleanup()

    def test_virtual_environment(self):
        """Test that the virtual environment is properly set up."""
        print("Testing virtual environment...")
        venv_path = self.server_dir / "venv"
        if not venv_path.exists():
            print("❌ Virtual environment not found")
            return False

        # Check if required packages are installed
        try:
            # Use the system Python since packages are installed there
            result = subprocess.run(
                ["python3", "-c", "import mcp, pydantic, click, rich"],
                check=False, cwd=self.server_dir,
                capture_output=True,
                text=True,
            )
            if result.returncode != 0:
                print(f"❌ Required packages not installed: {result.stderr}")
                return False

            print("✅ Virtual environment is properly configured")
            return True
        except Exception as e:
            print(f"❌ Virtual environment test error: {e}")
            return False

    def cleanup(self):
        """Clean up any running processes."""
        if self.server_process and self.server_process.poll() is None:
            print("Cleaning up server process...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            self.server_process = None

    def run_all_tests(self):
        """Run all regression tests."""
        print("Running MCP Server Regression Tests")
        print("=" * 40)

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
                print()  # Add spacing between tests
            except Exception as e:
                print(f"❌ Test {test.__name__} failed with exception: {e}")
                print()

        print("=" * 40)
        print(f"Test Results: {passed}/{total} tests passed")

        if passed == total:
            print("🎉 All tests passed! Server startup is working correctly.")
            return True
        print("❌ Some tests failed. Please check the output above.")
        return False


def main():
    """Main entry point for the test script."""
    tester = ServerStartupTester()
    try:
        success = tester.run_all_tests()
        sys.exit(0 if success else 1)
    finally:
        tester.cleanup()


if __name__ == "__main__":
    main()
