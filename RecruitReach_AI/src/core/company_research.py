import requests
from bs4 import BeautifulSoup
from googlesearch import search
from RecruitReach_AI.src.models.llm_manager import get_llm

def research_company(company_name):
    try:
        # Search for company information using Google
        search_results = search(f"{company_name} company overview", num_results=2)
    
        # Extract relevant information from the search results
        company_info = {}
        for result in search_results:
            # Fetch the webpage content
            response = requests.get(result)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract relevant text from the webpage
            company_info['description'] = soup.get_text()
            company_info['name'] = company_name
            break  # For now, just use the first result
        
        llm = get_llm()
        # Use LLM to summarize or extract specific information if needed
        summary = llm.invoke(f"summarize this : {company_info['description']}")
        return summary.content
    except Exception as e:
        print(f"Error researching company: {e}")
        return None
    

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    info = research_company(company_name)
    if info:
        print(f"Company Name: {info['name']}")
        print(f"Description: {info['description']}")
    else:
        print("Failed to retrieve company information.")
