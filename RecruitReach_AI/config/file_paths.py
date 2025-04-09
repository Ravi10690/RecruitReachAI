import os
from pathlib import Path
ROOT_DIR = Path(__file__).resolve(strict=True).parent.parent

# Path to the resume file
RESUME_PATH = os.path.join(ROOT_DIR, "data", "Ravi_Ahuja_Resume.pdf")
TOML_PATH = os.path.join(ROOT_DIR, "config", "config.toml")
# RESUME_PATH = "C://Users//ravia//OneDrive//Documents//Resume//Ravi_Ahuja_Resume.pdf"
