"""Entry point for running cq-agent as a module: python -m cq_agent"""
import sys

def main():
	"""Main entry point that handles import errors gracefully."""
	try:
		from cq_agent.cli.main import main as cli_main
		return cli_main()
	except ModuleNotFoundError as e:
		if "cq_agent" in str(e):
			print("=" * 70, file=sys.stderr)
			print("ERROR: cq_agent module not found!", file=sys.stderr)
			print("=" * 70, file=sys.stderr)
			print("\nThe package is not properly installed.", file=sys.stderr)
			print("\nTo fix this, please install the package:", file=sys.stderr)
			print("\n  1. Navigate to the Code-Quality-Agent directory", file=sys.stderr)
			print("  2. Run: pip install -e .", file=sys.stderr)
			print("     OR: pip install .", file=sys.stderr)
			print("\nIf you're in a virtual environment, make sure it's activated.", file=sys.stderr)
			print("If you installed globally, try: pip install --upgrade --force-reinstall .", file=sys.stderr)
			print("=" * 70, file=sys.stderr)
			return 1
		raise

if __name__ == "__main__":
	sys.exit(main())

