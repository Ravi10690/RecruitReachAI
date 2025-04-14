"""
Main entry point for RecruitReach2.

This module provides the main entry point for the RecruitReach2 application.
"""

import os
import sys
import streamlit.web.cli as stcli
from pathlib import Path


def main():
    """
    Main entry point for the application.
    
    This function sets up the environment and launches the Streamlit application.
    """
    # Get the directory of the current file
    current_dir = Path(__file__).resolve().parent
    
    # Add the current directory to the Python path
    sys.path.insert(0, str(current_dir))
    
    # Path to the Streamlit app
    app_path = current_dir /"Recruiter" / "app" / "web" / "app.py"
    
    # Check if the app file exists
    if not app_path.exists():
        print(f"Error: App file not found at {app_path}")
        sys.exit(1)
    
    # Launch the Streamlit app
    sys.argv = ["streamlit", "run", str(app_path), "--browser.serverAddress=localhost", "--server.port=8501"]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
