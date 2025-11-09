# 🔴 Disk Space Issue - Installation Cannot Complete

## Problem
Your C: drive is **completely full** (0 bytes free), which prevents `cq-agent` from installing. Even though we:
- ✅ Cleared pip cache (freed ~1.3 GB)
- ✅ Created virtual environment on E: drive
- ✅ Set pip cache to E: drive

The installation still fails because Python needs temporary space on C: drive during installation.

## ✅ Solutions (Choose One)

### Solution 1: Free Up Space on C: Drive (Recommended)

**Free at least 5-10 GB on C: drive**, then retry installation:

```powershell
# Navigate to Code-Quality-Agent directory
cd E:\Code-Quality-Agent

# Activate virtual environment (if using it)
E:\cq-agent-env\Scripts\Activate.ps1

# Install
python -m pip install --upgrade --force-reinstall .
```

**Ways to free up space:**
1. **Empty Recycle Bin**
2. **Run Disk Cleanup**: `cleanmgr` in Run dialog
3. **Delete temporary files**: `%TEMP%` and `%TMP%` folders
4. **Uninstall unused programs**
5. **Move large files to E: drive**
6. **Clear browser caches**
7. **Delete old Windows Update files** (requires admin)

### Solution 2: Install Minimal Dependencies Only

If you can't free up space, install only the core package without all dependencies:

```powershell
cd E:\Code-Quality-Agent
python -m pip install --no-deps .
```

**Note**: This will install `cq-agent` but you'll need to install dependencies manually as needed.

### Solution 3: Use Portable Python on E: Drive

1. Download portable Python from [python.org](https://www.python.org/downloads/)
2. Extract to `E:\Python311` (or similar)
3. Use that Python for installation:

```powershell
E:\Python311\python.exe -m pip install --upgrade --force-reinstall E:\Code-Quality-Agent
```

## 🔍 Check Current Disk Space

```powershell
Get-PSDrive C | Select-Object Used,Free
```

You need at least **5-10 GB free** for a successful installation.

## 📝 After Freeing Space

Once you have free space, run:

```powershell
cd E:\Code-Quality-Agent
python -m pip install --upgrade --force-reinstall .
cq-agent --help  # Verify installation
```

## ⚠️ Important Notes

- The virtual environment on E: drive (`E:\cq-agent-env`) is ready to use once you have space
- After installation, you'll need to activate the venv each time:
  ```powershell
  E:\cq-agent-env\Scripts\Activate.ps1
  cq-agent analyze .
  ```

## 🆘 Still Having Issues?

If you continue to have problems after freeing space:
1. Check Python version: `python --version` (needs 3.11+)
2. Try installing in smaller chunks (install dependencies separately)
3. Consider using a different Python installation location

