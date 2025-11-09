#!/usr/bin/env python3
"""Quick script to verify cq-agent installation."""
import sys

def main():
    try:
        import cq_agent
        print("✓ cq_agent package is installed")
        
        try:
            from cq_agent.cli.main import main
            print("✓ CLI module can be imported")
            print("\nInstallation looks good! You can use 'cq-agent' command.")
            return 0
        except ImportError as e:
            print(f"✗ CLI module import failed: {e}")
            return 1
    except ImportError:
        print("✗ cq_agent package is NOT installed")
        print("\nTo install:")
        print("  1. Navigate to the Code-Quality-Agent directory")
        print("  2. Run: pip install -e .")
        print("     OR: pip install .")
        return 1

if __name__ == "__main__":
    sys.exit(main())

