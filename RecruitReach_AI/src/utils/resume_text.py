from langchain_community.document_loaders import PyPDFLoader
from file_paths import RESUME_PATH
from pathlib import Path

def load_resume():
    loader = PyPDFLoader(str(Path(RESUME_PATH).resolve()))
    docs = loader.load()
    return docs

if __name__ == "__main__":
    resume_docs = load_resume()
    print(resume_docs)
