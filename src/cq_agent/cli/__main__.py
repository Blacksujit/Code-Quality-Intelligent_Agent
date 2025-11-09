"""Entry point wrapper for cq-agent CLI that handles import errors gracefully."""
import sys
import os


def _show_installation_error():
	"""Show helpful error message when package is not installed."""
	print("=" * 70, file=sys.stderr)
	print("ERROR: cq_agent module not found!", file=sys.stderr)
	print("=" * 70, file=sys.stderr)
	print("\nThe package is not properly installed.", file=sys.stderr)
	print("\n📦 TO INSTALL (from Code-Quality-Agent directory):", file=sys.stderr)
	print("\n  Option 1: Use the installation script", file=sys.stderr)
	print("    cd E:\\Code-Quality-Agent", file=sys.stderr)
	print("    python install_global.py", file=sys.stderr)
	print("\n  Option 2: Manual installation", file=sys.stderr)
	print("    cd E:\\Code-Quality-Agent", file=sys.stderr)
	print("    pip install -e .", file=sys.stderr)
	print("    # OR: pip install .", file=sys.stderr)
	print("\n  Option 3: Force reinstall (if already installed)", file=sys.stderr)
	print("    cd E:\\Code-Quality-Agent", file=sys.stderr)
	print("    pip install --upgrade --force-reinstall .", file=sys.stderr)
	print("\n⚠️  IMPORTANT:", file=sys.stderr)
	print("  - Install from Code-Quality-Agent directory, NOT your project directory!", file=sys.stderr)
	print("  - If using a virtual environment, make sure it's activated", file=sys.stderr)
	print("  - After installation, you can use 'cq-agent' from ANY directory", file=sys.stderr)
	print("\n📖 See INSTALL.md for detailed instructions", file=sys.stderr)
	print("\nCurrent Python path:", file=sys.stderr)
	for p in sys.path:
		print(f"  - {p}", file=sys.stderr)
	print("=" * 70, file=sys.stderr)


def main():
	"""Main entry point that handles import errors gracefully."""
	try:
		# Try to import the actual main function
		from cq_agent.cli.main import main as cli_main
		return cli_main()
	except (ModuleNotFoundError, ImportError) as e:
		error_msg = str(e)
		if "cq_agent" in error_msg or "No module named 'cq_agent'" in error_msg:
			_show_installation_error()
			return 1
		# Re-raise if it's a different import error
		raise


if __name__ == "__main__":
	sys.exit(main())

