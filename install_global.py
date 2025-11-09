#!/usr/bin/env python3
"""
Global Installation Script for cq-agent

This script installs cq-agent globally so you can use it from any directory.

Usage:
    python install_global.py

After installation, you can use 'cq-agent' command from any directory.
"""
import subprocess
import sys
import os
import platform
from pathlib import Path
import shutil

def get_python_scripts_dir():
    """Get the Python Scripts directory where console scripts are installed."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "show", "-f", "pip"],
            capture_output=True,
            text=True,
            check=True
        )
        # Try to find Scripts directory from pip location
        import site
        scripts_dir = site.getusersitepackages()
        if scripts_dir:
            # Convert site-packages to Scripts
            scripts_dir = str(Path(scripts_dir).parent / "Scripts")
            if Path(scripts_dir).exists():
                return scripts_dir
        
        # Fallback: use site.USER_BASE
        user_base = site.getuserbase()
        if user_base:
            scripts_dir = str(Path(user_base) / "Scripts")
            if Path(scripts_dir).exists():
                return scripts_dir
        
        # Try common locations
        python_exe = Path(sys.executable)
        scripts_dir = python_exe.parent / "Scripts"
        if scripts_dir.exists():
            return str(scripts_dir)
            
    except Exception:
        pass
    
    # Default fallback
    python_exe = Path(sys.executable)
    return str(python_exe.parent / "Scripts")

def check_path_includes_scripts():
    """Check if Python Scripts directory is in PATH."""
    scripts_dir = get_python_scripts_dir()
    path_env = os.environ.get("PATH", "").split(os.pathsep)
    return scripts_dir in path_env or any(scripts_dir.lower() == p.lower() for p in path_env)

def check_command_available():
    """Check if cq-agent command is available."""
    return shutil.which("cq-agent") is not None

def main():
    print("=" * 70)
    print("cq-agent Global Installation")
    print("=" * 70)
    print()
    
    # Check if we're in the right directory
    if not (Path("setup.py").exists() or Path("pyproject.toml").exists()):
        print("ERROR: This script must be run from the Code-Quality-Agent directory!")
        print("\nPlease:")
        print("  1. Navigate to the Code-Quality-Agent directory")
        print("  2. Run: python install_global.py")
        return 1
    
    print("Installing cq-agent globally...")
    print("This will make 'cq-agent' available from any directory.\n")
    
    try:
        # Install in editable mode for development, or regular install for production
        install_mode = os.getenv("CQ_AGENT_DEV", "").lower()
        if install_mode in ("1", "true"):
            print("Installing in development mode (-e)...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "-e", "."],
                check=True,
                capture_output=False
            )
        else:
            print("Installing in production mode...")
            result = subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "--force-reinstall", "."],
                check=True,
                capture_output=False
            )
        
        print("\n" + "=" * 70)
        print("✓ Package installation successful!")
        print("=" * 70)
        
        # Check if command is available
        scripts_dir = get_python_scripts_dir()
        is_windows = platform.system() == "Windows"
        
        print(f"\n📁 Scripts directory: {scripts_dir}")
        
        if check_command_available():
            print("✓ 'cq-agent' command is available in PATH")
            print("\nYou can now use 'cq-agent' from any directory:")
            print("  cq-agent analyze .")
            print("  cq-agent qa .")
        else:
            print("\n⚠️  WARNING: 'cq-agent' command not found in PATH!")
            print("\nThis usually happens on Windows when Python Scripts directory")
            print("is not in your PATH environment variable.")
            print("\n" + "=" * 70)
            print("🔧 SOLUTIONS:")
            print("=" * 70)
            
            if is_windows:
                print("\nOption 1: Add Scripts to PATH (Recommended)")
                print(f"  1. Add this directory to your PATH:")
                print(f"     {scripts_dir}")
                print("  2. Restart your terminal/PowerShell")
                print("\n  To add to PATH:")
                print("    - Press Win + X, select 'System'")
                print("    - Click 'Advanced system settings'")
                print("    - Click 'Environment Variables'")
                print("    - Edit 'Path' under 'User variables'")
                print(f"    - Add: {scripts_dir}")
                
                print("\nOption 2: Use Python module syntax (Works immediately)")
                print("  Instead of: cq-agent analyze .")
                print("  Use:        python -m cq_agent.cli.main analyze .")
                print("  Or:         python -m cq_agent analyze .")
                
                print("\nOption 3: Use full path")
                cq_agent_exe = Path(scripts_dir) / "cq-agent.exe"
                if cq_agent_exe.exists():
                    print(f"  Use: {cq_agent_exe} analyze .")
            else:
                print("\nOption 1: Add Scripts to PATH")
                print(f"  Add to ~/.bashrc or ~/.zshrc:")
                print(f"  export PATH=\"$PATH:{scripts_dir}\"")
                print("\nOption 2: Use Python module syntax")
                print("  python -m cq_agent.cli.main analyze .")
        
        print("\n" + "=" * 70)
        print("To verify installation, run:")
        print("  python verify_installation.py")
        print("=" * 70)
        return 0
        
    except subprocess.CalledProcessError as e:
        print("\n" + "=" * 70)
        print("✗ Installation failed!")
        print("=" * 70)
        print(f"\nError: {e}")
        print("\nPlease check:")
        print("  1. You have pip installed")
        print("  2. You have write permissions")
        print("  3. If using a virtual environment, make sure it's activated")
        return 1
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

