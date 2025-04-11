from bs4 import BeautifulSoup
from googlesearch import search

def get_company_info(company_name):
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