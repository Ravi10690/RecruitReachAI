from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv(override=True)

def get_llm(model_name="gpt-4o-mini", temperature=0.2):
    """
    # Load the model from the Hugging Face model hub
    """
    llm = ChatOpenAI(model=model_name, temperature=temperature)
    return llm