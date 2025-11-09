# 🚀 Quick Start Guide

## The Problem You're Experiencing

You're trying to use `cq-agent` from your project directory (`E:\Gamified\python-flask-E-learning-platform`), but getting:

```
ModuleNotFoundError: No module named 'cq_agent'
```

This happens because the package isn't installed in your Python environment yet.

## ✅ The Solution (3 Simple Steps)

### Step 1: Go to Code-Quality-Agent Directory

```powershell
cd E:\Code-Quality-Agent
```

**⚠️ CRITICAL**: You MUST install from the `Code-Quality-Agent` directory, NOT from your project directory!

### Step 2: Install the Package

```powershell
# Option A: Use the installation script (easiest)
python install_global.py

# Option B: Manual installation
pip install -e .
```

### Step 3: Use from Any Directory

```powershell
# Now go to your project
cd E:\Gamified\python-flask-E-learning-platform

# Use cq-agent - it will work now!
cq-agent analyze .
```

## 🎯 That's It!

After Step 2, `cq-agent` is installed globally and you can use it from **any directory** on your system.

## ⚠️ Windows PATH Issue?

If you get **"cq-agent: command not recognized"** on Windows, this is a PATH issue. You have 3 options:

### Option 1: Fix PATH (Recommended)
```powershell
# Run the PATH fix script
.\fix_path_windows.ps1

# Then restart your terminal and use:
cq-agent analyze .
```

### Option 2: Use Python Module Syntax (Works immediately!)
```powershell
# Instead of: cq-agent analyze .
# Use this (no PATH needed):
python -m cq_agent.cli.main analyze .
python -m cq_agent analyze .  # Shorter version
```

### Option 3: Add to PATH Manually
1. Find your Scripts directory:
   ```powershell
   python -c "import site; from pathlib import Path; print(Path(site.getuserbase()) / 'Scripts')"
   ```
2. Add that directory to your PATH (see [INSTALL.md](INSTALL.md) for detailed steps)
3. Restart terminal

## 🔍 Verify Installation

From the Code-Quality-Agent directory:

```powershell
python verify_installation.py
```

You should see:
```
✓ cq_agent package is installed
✓ CLI module can be imported

Installation looks good! You can use 'cq-agent' command.
```

## ❓ Common Mistakes

### ❌ Wrong: Installing from project directory
```powershell
cd E:\Gamified\python-flask-E-learning-platform
pip install .  # ERROR: No setup.py here!
```

### ✅ Correct: Installing from Code-Quality-Agent directory
```powershell
cd E:\Code-Quality-Agent
pip install .  # SUCCESS!
```

## 📖 Need More Help?

- **Detailed Installation Guide**: See [INSTALL.md](INSTALL.md)
- **Troubleshooting**: See [INSTALL.md#troubleshooting](INSTALL.md#-troubleshooting)
- **Full Documentation**: See [README.md](README.md)

