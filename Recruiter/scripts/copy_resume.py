"""
Script to copy the resume from the original project to the new project structure.

This script copies the resume file from the original RecruitReach_AI project
to the new RecruitReach2 project structure.
"""

import os
import shutil
from pathlib import Path


def copy_resume():
    """
    Copy the resume file from the original project to the new project structure.
    
    This function copies the resume file from RecruitReach_AI/data/Ravi_Ahuja_Resume.pdf
    to RecruitReach2/data/resume.pdf.
    """
    # Get the current directory (should be the project root)
    current_dir = Path(__file__).resolve().parent.parent
    
    # Define source and destination paths
    source_path = Path(current_dir.parent, "RecruitReach_AI", "data", "Ravi_Ahuja_Resume.pdf")
    dest_path = Path(current_dir, "data", "resume.pdf")
    
    # Create the data directory if it doesn't exist
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Copy the file
    if os.path.exists(source_path):
        shutil.copy2(source_path, dest_path)
        print(f"Resume copied from {source_path} to {dest_path}")
    else:
        print(f"Source resume file not found at {source_path}")


if __name__ == "__main__":
    copy_resume()
