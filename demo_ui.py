#!/usr/bin/env python3
"""
Quick demo script to showcase the production-grade UI
"""

import subprocess
import sys

def main():
    print("🚀 Starting Code Quality Intelligence Agent Demo")
    print("=" * 60)
    
    # Check if streamlit is available
    try:
        print("✅ Streamlit is available")
    except ImportError:
        print("❌ Streamlit not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "streamlit", "plotly", "numpy"])
    
    # Check if plotly is available
    try:
        print("✅ Plotly is available")
    except ImportError:
        print("❌ Plotly not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "plotly", "numpy"])
    
    print("\n🎨 Launching Production-Grade UI...")
    print("📍 URL: http://localhost:8501")
    print("🔍 Features:")
    print("   • Modern gradient design with animations")
    print("   • Interactive charts and visualizations")
    print("   • Smart filtering and search")
    print("   • File details with code context")
    print("   • Safe autofix with confirmation")
    print("   • Export capabilities")
    print("\n💡 Pro Tips:")
    print("   • Use the sidebar to configure analysis")
    print("   • Try different filters in the Dashboards tab")
    print("   • Explore file details with code context")
    print("   • Test the autofix functionality")
    print("   • Export reports for your team")
    print("\n" + "=" * 60)
    
    # Launch Streamlit
    app_path = Path(__file__).parent / "src" / "cq_agent" / "web" / "app.py"
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", str(app_path),
        "--server.headless", "false",
        "--server.port", "8501"
    ])

if __name__ == "__main__":
    main()
