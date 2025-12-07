"""
ABIA Traffic Accident Forecaster - Launch Script

Simple launcher to run the Streamlit application.
Usage: python run.py
"""

import subprocess
import sys
from pathlib import Path

# Get the project root directory
PROJECT_ROOT = Path(__file__).parent
STREAMLIT_APP = PROJECT_ROOT / 'streamlit_app' / 'main.py'

if __name__ == '__main__':
    print("🚦 Launching ABIA Traffic Accident Forecaster...")
    print(f"   App location: {STREAMLIT_APP}")
    print()
    
    # Run streamlit with the app
    subprocess.run([
        sys.executable, '-m', 'streamlit', 'run',
        str(STREAMLIT_APP),
        '--server.headless', 'false'
    ])
