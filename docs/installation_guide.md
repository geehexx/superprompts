# Installation Guide

Complete installation instructions for SuperPrompts across different platforms and environments.

## System Requirements

- **Python**: 3.10 or higher
- **Operating System**: Linux, macOS, Windows (WSL2 recommended for Windows)
- **Memory**: 512MB RAM minimum, 1GB recommended
- **Disk Space**: 100MB for installation, 500MB for development

## Installation Methods

### Method 1: From Source (Recommended)

This method gives you the latest features and development tools.

#### 1. Install uv (Dependency Manager)

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

**Windows (PowerShell):**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative (pip):**
```bash
pip install uv
```

#### 2. Clone and Install
```bash
# Clone the repository
git clone https://github.com/geehexx/superprompts.git
cd superprompts

# Install dependencies
uv sync --dev

# Verify installation
uv run superprompts --help
```

### Method 2: From PyPI (When Available)

```bash
# Using pip
pip install superprompts

# Using uv
uv add superprompts
```

### Method 3: Development Installation

For contributors and advanced users:

```bash
# Clone repository
git clone https://github.com/geehexx/superprompts.git
cd superprompts

# Install with development dependencies
uv sync --dev

# Install pre-commit hooks
uv run pre-commit install

# Run complete setup
uv run invoke setup

# Verify everything works
uv run invoke status
```

## Platform-Specific Instructions

### Linux

#### Ubuntu/Debian
```bash
# Update package list
sudo apt update

# Install Python 3.10+ if not available
sudo apt install python3.10 python3.10-venv python3.10-dev

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install SuperPrompts
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

#### CentOS/RHEL/Fedora
```bash
# Install Python 3.10+ if not available
sudo dnf install python3.10 python3.10-devel

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install SuperPrompts
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

#### Arch Linux
```bash
# Install Python 3.10+ if not available
sudo pacman -S python

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Install SuperPrompts
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

### macOS

#### Using Homebrew
```bash
# Install Python 3.10+
brew install python@3.10

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install SuperPrompts
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

#### Using MacPorts
```bash
# Install Python 3.10+
sudo port install python310

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Install SuperPrompts
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

### Windows

#### Using WSL2 (Recommended)
```bash
# In WSL2 terminal
curl -LsSf https://astral.sh/uv/install.sh | sh
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

#### Using PowerShell
```powershell
# Install Python 3.10+ from python.org
# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Add to PATH
$env:PATH += ";$env:USERPROFILE\.local\bin"

# Clone and install
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

#### Using Chocolatey
```powershell
# Install Python 3.10+
choco install python --version=3.10.0

# Install uv
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Clone and install
git clone https://github.com/geehexx/superprompts.git
cd superprompts
uv sync --dev
```

## Docker Installation

### Using Dockerfile
```dockerfile
FROM python:3.10-slim

# Install uv
RUN pip install uv

# Clone and install SuperPrompts
RUN git clone https://github.com/geehexx/superprompts.git /app
WORKDIR /app
RUN uv sync --dev

# Set entrypoint
ENTRYPOINT ["uv", "run", "superprompts"]
```

### Using Docker Compose
```yaml
version: '3.8'
services:
  superprompts:
    build: .
    volumes:
      - ./your-project:/workspace
    working_dir: /workspace
    command: ["uv", "run", "superprompts", "list-prompts"]
```

### Using Pre-built Image (When Available)
```bash
# Pull and run pre-built image
docker run -it --rm superprompts/superprompts:latest

# Or with volume mount
docker run -it --rm -v $(pwd):/workspace superprompts/superprompts:latest
```

## Verification

### Basic Verification
```bash
# Check installation
uv run superprompts --version

# List available prompts
uv run superprompts list-prompts

# Test a prompt
uv run superprompts get-prompt repo_docs
```

### Advanced Verification
```bash
# Run all tests
uv run invoke test

# Check code quality
uv run invoke check-all

# Test MCP server
uv run superprompts-server &
uv run superprompts list-prompts
```

## Troubleshooting

### Common Issues

#### 1. Python Version Issues
```bash
# Check Python version
python3 --version

# If version is too old, install Python 3.10+
# Ubuntu/Debian:
sudo apt install python3.10

# macOS:
brew install python@3.10

# Windows:
# Download from python.org
```

#### 2. uv Not Found
```bash
# Add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### 3. Permission Issues
```bash
# Fix permissions
chmod +x ~/.local/bin/uv

# Or install with --user flag
pip install --user uv
```

#### 4. Network Issues
```bash
# Use alternative package index
uv sync --dev --index-url https://pypi.org/simple/

# Or configure proxy
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

#### 5. Virtual Environment Issues
```bash
# Recreate virtual environment
uv venv --force
uv sync --dev

# Or clear cache and reinstall
uv cache clean
uv sync --dev
```

### Platform-Specific Issues

#### Linux Issues
```bash
# Missing build tools
sudo apt install build-essential python3-dev

# Missing SSL certificates
sudo apt install ca-certificates

# Permission denied
sudo chown -R $USER:$USER ~/.local
```

#### macOS Issues
```bash
# Xcode command line tools
xcode-select --install

# Homebrew issues
brew update && brew upgrade

# Permission issues
sudo chown -R $(whoami) /usr/local
```

#### Windows Issues
```powershell
# PowerShell execution policy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Long path support
# Enable in Group Policy or registry
```

### Getting Help

- **Documentation**: Check the [docs/](docs/) directory
- **Issues**: Report problems on [GitHub Issues](https://github.com/geehexx/superprompts/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/geehexx/superprompts/discussions)

## Uninstallation

### Remove from Source Installation
```bash
# Remove the directory
rm -rf /path/to/superprompts

# Remove uv (optional)
rm -rf ~/.local/bin/uv
```

### Remove from PyPI Installation
```bash
# Using pip
pip uninstall superprompts

# Using uv
uv remove superprompts
```

### Remove Docker Installation
```bash
# Remove container
docker rm superprompts

# Remove image
docker rmi superprompts/superprompts

# Remove volumes
docker volume prune
```

## Next Steps

After successful installation:

1. **Read the [Getting Started Guide](getting_started.md)**
2. **Explore [Available Prompts](available_prompts.md)**
3. **Learn [AI Prompting Best Practices](ai_prompting_best_practices.md)**
4. **Set up [MCP Configuration](mcp_configuration.md)** for Cursor IDE

## Development Setup

For contributors:

1. **Follow the [Development Guide](development.md)**
2. **Read the [Contributing Guide](contributing_guide.md)**
3. **Set up [Pre-commit Hooks](pre_commit.md)**
4. **Configure [Testing Environment](testing.md)**

## Environment Variables

Useful environment variables for configuration:

```bash
# Set logging level
export SUPERPROMPTS_LOG_LEVEL=DEBUG

# Set custom config path
export SUPERPROMPTS_CONFIG_PATH=/path/to/config

# Set Python path
export PYTHONPATH=/path/to/superprompts
```

## Performance Optimization

### For Large Projects
```bash
# Use faster dependency resolution
uv sync --dev --no-cache

# Parallel installation
uv sync --dev --jobs 4
```

### For CI/CD
```bash
# Minimal installation
uv sync --dev --no-dev

# Cache dependencies
uv sync --dev --cache-dir /tmp/uv-cache
```

## Security Considerations

### Best Practices
- Use virtual environments for isolation
- Keep dependencies updated
- Use HTTPS for all downloads
- Verify package integrity

### Network Security
```bash
# Use trusted package indexes
uv sync --dev --index-url https://pypi.org/simple/

# Verify SSL certificates
export SSL_VERIFY=true
```

That's it! You should now have SuperPrompts installed and ready to use. If you encounter any issues, check the [Troubleshooting Guide](troubleshooting.md) or reach out to the community for help.
