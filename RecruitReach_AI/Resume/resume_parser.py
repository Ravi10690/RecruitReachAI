import os
from langchain_community.document_loaders import PyPDFLoader
from RecruitReach_AI.config.file_paths import RESUME_PATH
from pathlib import Path

def load_resume():
    if not os.path.isfile(RESUME_PATH):
        raise FileNotFoundError(f"Resume not found at: {RESUME_PATH}")
    loader = PyPDFLoader(RESUME_PATH)
    docs = loader.load()
    return docs[0].page_content

if __name__ == "__main__":
    resume_docs = load_resume()
    print(resume_docs)
