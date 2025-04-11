
from RecruitReach_AI.models.llm_manager import get_llm
from RecruitReach_AI.Company_Reserch.ResearchMehtods.openi_web_search import get_company_info as get_company_info_openi
from RecruitReach_AI.Comapny_Reserch.ResearchMehtods.google_search import get_company_info as get_company_info_google
def research_company(company_name, method ='openai'):
    try:
        if method == 'google':
            company_info = get_company_info_google(company_name)
            llm = get_llm()
            # Use LLM to summarize or extract specific information if needed
            summary = llm.invoke(f"summarize this : {company_info['description']}")
            return summary.content
        elif method == "openai":
            company_info = get_company_info_openi(company_name)
            return company_info
    except Exception as e:
        print(f"Error researching company: {e}")
        return None
    

if __name__ == "__main__":
    company_name = input("Enter the company name: ")
    info = research_company(company_name)
    if info:    
        print(info)
    else:
        print("Failed to retrieve company information.")
