"""
Web Search Utilities for RecruitReach.

This module provides utilities for web search operations.
"""

import os
import requests
from typing import Optional, Dict, Any, List
from Recruiter.prompts.company_research_prompts import OPENAI_WEB_SERACH_PROMPT
try:
    from bs4 import BeautifulSoup
    from googlesearch import search
except ImportError:
    pass

try:
    from agents import Agent, Runner, WebSearchTool
except ImportError:
    pass


def get_company_info_bs4(company_name: str) -> Optional[str]:
    """
    Get company information using BeautifulSoup and googlesearch.
    
    Args:
        company_name: Name of the company to research.
        
    Returns:
        Company information as text, or None if an error occurred.
    """
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
        
        return company_info['description']
    except Exception as e:
        print(f"Error during research: {e}")
        return None


def get_company_info_agent(company_name: str, api_key: Optional[str] = None) -> Optional[str]:
    """
    Get company information using Agent with WebSearchTool.
    
    Args:
        company_name: Name of the company to research.
        api_key: OpenAI API key. If provided, will be used for the search.
        
    Returns:
        Company information as text, or None if an error occurred.
    """
    try:
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key
            
        agent = Agent(
            name="Assistant",
            instructions=OPENAI_WEB_SERACH_PROMPT,
            tools=[
                WebSearchTool(),
            ],
        )
        
        messages = Runner.run_sync(agent, company_name)
        return messages.final_output
    except Exception as e:
        print(f"Error during research: {e}")
        return None
