import os
from Recruiter.utils.config.config_manager import ConfigManager
from Recruiter.core.company_research.company_researcher import CompanyResearcher

def test_company_research():
    # Load configuration
    config_manager = ConfigManager()
    api_key = config_manager.get_value('openai', 'OPENAI_API_KEY')
    
    company_name = "OpenAI"
    
    # Test with BS4 method
    print("\n=== Testing with BS4 method ===")
    researcher_bs4 = CompanyResearcher(api_key=api_key, search_method='bs4')
    info_bs4 = researcher_bs4.research_company(company_name)
    print(f"Company Info for {company_name} (BS4): {info_bs4[:200]}...")
    
    # Test with Agent method
    print("\n=== Testing with Agent method ===")
    researcher_agent = CompanyResearcher(api_key=api_key, search_method='agent')
    info_agent = researcher_agent.research_company(company_name)
    print(f"Company Info for {company_name} (Agent): {info_agent[:200] if info_agent else 'None'}...")
    
    # Test with LLM method
    print("\n=== Testing with LLM method ===")
    researcher_llm = CompanyResearcher(api_key=api_key, search_method='llm')
    info_llm = researcher_llm.research_company(company_name)
    print(f"Company Info for {company_name} (LLM): {info_llm[:200]}...")

if __name__ == "__main__":
    test_company_research()
