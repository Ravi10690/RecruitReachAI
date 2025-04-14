#!/usr/bin/env python3
"""
Run script for RecruitReach2.

This script provides a simple way to run the RecruitReach2 application.
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(project_root))

# Import the main function from the main module
from main import main

if __name__ == "__main__":
    # Run the application
    main()
