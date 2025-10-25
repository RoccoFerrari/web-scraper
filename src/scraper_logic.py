from urllib.parse import urljoin
import requests
from class_selectors import *

# Interface: AbstractSelector
# Implementations: TagSelector, AttributeSelector

def fetch_page(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response

def soupify(html_content):
    # html_content: response.content
    return BeautifulSoup(html_content, "html.parser")

def select_elements(soup: BeautifulSoup, column_jobs: List[AbstractSelector]) -> List[List[Tag]]:
    element_lists = []
    for job in column_jobs:
        # Every job knows how to find its elements
        elements = job.find_elements(soup)
        element_lists.append(elements)
        
    return element_lists

def format_results(element_lists: List[List[Tag]], column_jobs: List[AbstractSelector], base_url: str) -> List[List[Any]]:
    # zip(*element_lists) transforms [ [a,b], [c,d] ] in zip([a,b], [c,d])
    zipped_tags = zip(*element_lists)
    
    results = []
    for tag_group in zipped_tags:
        cleaned_group = []
        
        for tag, job in zip(tag_group, column_jobs):
            cleaned_data = job.extract(tag)

            if isinstance(job, AttributeSelector) and \
                job.attribute_name in ('href', 'src') and \
                cleaned_data:
                cleaned_data = urljoin(base_url, cleaned_data)

            cleaned_group.append(cleaned_data)
            
        results.append(cleaned_group)
    
    return results