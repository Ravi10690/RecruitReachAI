from langchain_openai import ChatOpenAI
from RecruitReach_AI.utils.toml_parser import TomlParser
OPENAI_API_KEY = TomlParser().get_value("openai", "OPENAI_API_KEY")

def get_llm(model_name="gpt-4o-mini", temperature=0.2):
    """
    # Load the model from the Hugging Face model hub
    """
    llm = ChatOpenAI(model=model_name, temperature=temperature, api_key=OPENAI_API_KEY)
    return llm


if __name__ == "__main__":
    # Example usage
    llm = get_llm()
    print(llm.invoke("hi"))
    print("LLM loaded successfully.")
    # You can now use the `llm` object for further processing