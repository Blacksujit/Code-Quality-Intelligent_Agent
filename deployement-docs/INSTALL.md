# 📦 Installation Guide for cq-agent

This guide will help you install `cq-agent` globally so you can use it from any project directory.

## 🎯 Quick Installation

### Step 1: Navigate to Code-Quality-Agent Directory

```bash
cd E:\Code-Quality-Agent
```

**Important**: You must run the installation from the `Code-Quality-Agent` directory, NOT from your project directory!

### Step 2: Install the Package

#### Option A: Using the Installation Script (Recommended)

```bash
python install_global.py
```

#### Option B: Manual Installation

```bash
# For development (editable install)
pip install -e .

# OR for production (regular install)
pip install .
```

#### Option C: Force Reinstall (if you have issues)

```bash
pip install --upgrade --force-reinstall .
```

### Step 3: Verify Installation

```bash
# From the Code-Quality-Agent directory
python verify_installation.py

# Or test the command directly
cq-agent --help
```

### Step 4: Use from Any Directory

Once installed, you can use `cq-agent` from **any project directory**:

```bash
# Navigate to your project
cd E:\Gamified\python-flask-E-learning-platform

# Run analysis
cq-agent analyze .

# Or use Q&A
cq-agent qa .
```

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'cq_agent'"

**Solution**: The package is not installed. Make sure you:

1. ✅ Installed from the `Code-Quality-Agent` directory (not your project directory)
2. ✅ Used the correct Python environment (check with `python --version`)
3. ✅ If using a virtual environment, make sure it's activated
4. ✅ Reinstalled after making changes: `pip install --upgrade --force-reinstall .`

### Issue: "ERROR: Directory '.' is not installable"

**Solution**: You're trying to install from the wrong directory. 

- ❌ **Wrong**: Running `pip install .` from `E:\Gamified\python-flask-E-learning-platform`
- ✅ **Correct**: Running `pip install .` from `E:\Code-Quality-Agent`

### Issue: "cq-agent: command not recognized" or "The term 'cq-agent' is not recognized"

**This is a PATH issue on Windows!** The `cq-agent` command is installed, but Windows can't find it.

#### **Solution 1: Add Python Scripts to PATH (Recommended for permanent fix)**

1. **Find your Python Scripts directory:**
   ```powershell
   python -c "import site; import os; from pathlib import Path; print(Path(site.getuserbase()) / 'Scripts')"
   ```
   Or check common locations:
   - `C:\Users\YOUR_USERNAME\AppData\Local\Programs\Python\Python311\Scripts`
   - `C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python311\Scripts`

2. **Add to PATH:**
   - Press `Win + X`, select **"System"**
   - Click **"Advanced system settings"**
   - Click **"Environment Variables"**
   - Under **"User variables"**, select **"Path"** and click **"Edit"**
   - Click **"New"** and add the Scripts directory path
   - Click **"OK"** on all dialogs
   - **Restart your terminal/PowerShell** (important!)

3. **Verify:**
   ```powershell
   # Close and reopen PowerShell, then:
   cq-agent --help
   ```

#### **Solution 2: Use Python Module Syntax (Works immediately, no PATH needed)**

Instead of `cq-agent`, use:

```powershell
# Full module path
python -m cq_agent.cli.main analyze .

# Or shorter (if __main__.py is set up)
python -m cq_agent analyze .
```

This works from any directory and doesn't require PATH configuration!

#### **Solution 3: Use Full Path to Executable**

```powershell
# Find the executable
python -c "import site; from pathlib import Path; print(Path(site.getuserbase()) / 'Scripts' / 'cq-agent.exe')"

# Then use the full path
C:\Users\YOUR_USERNAME\AppData\Roaming\Python\Python311\Scripts\cq-agent.exe analyze .
```

#### **Solution 4: Check Installation Location**

1. Check if the script was installed:
   ```powershell
   python -m pip show cq-agent
   ```

2. Check where scripts are installed:
   ```powershell
   python -m pip show -f cq-agent | Select-String "cq-agent"
   ```

3. If not found, reinstall:
   ```powershell
   pip install --upgrade --force-reinstall .
   ```

### Issue: Works in one terminal but not another

**Solution**: You might be using different Python environments. Make sure:

1. The same Python environment is active in both terminals
2. If using virtual environments, activate the same one
3. Check which Python is being used: `where python` (Windows) or `which python` (Linux/Mac)

## 🌍 Global vs Local Installation

### Global Installation (Recommended)

Installs `cq-agent` system-wide or in your user Python environment. You can use it from any directory.

```bash
# From Code-Quality-Agent directory
pip install .
```

### Development Installation (Editable)

Installs in editable mode - changes to the code are immediately available.

```bash
# From Code-Quality-Agent directory
pip install -e .
```

### Virtual Environment Installation

If you prefer to keep it isolated:

```bash
# Create virtual environment
python -m venv cq-agent-env

# Activate it
# Windows:
cq-agent-env\Scripts\activate
# Linux/Mac:
source cq-agent-env/bin/activate

# Install
pip install -e .
```

**Note**: You'll need to activate the virtual environment each time you want to use `cq-agent`.

## ✅ Verification Checklist

After installation, verify everything works:

- [ ] `python verify_installation.py` runs successfully
- [ ] `cq-agent --help` shows the help message
- [ ] `cq-agent analyze .` works from a test project directory
- [ ] No "ModuleNotFoundError" messages appear


## 🆘 Still Having Issues?

1. Check Python version: `python --version` (needs 3.11+)
2. Check pip version: `pip --version`
3. Try upgrading pip: `python -m pip install --upgrade pip`
4. Check installation location: `python -m pip show cq-agent`
5. Verify entry points: `python -m pip show -f cq-agent | findstr cq-agent`

