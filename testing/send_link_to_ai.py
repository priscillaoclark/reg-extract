from testing.llm_summary import get_ai_summaries
import requests
from bs4 import BeautifulSoup

def link_to_ai(link):
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')
        html_content = soup.prettify()
        for a in soup.find_all('a'):
            a.decompose()
        text_content = soup.get_text()
        tokens = text_content.split()
        text_content = ' '.join(tokens)
        
        ai_summary = get_ai_summaries(text_content)
        ai_summary_short, ai_summary_long = ai_summary
        
        return ai_summary_short
    
# example usage
# result = link_to_ai('https://www.federalreserve.gov/newsevents/pressreleases/enforcement20241010a.htm')
# print(result)