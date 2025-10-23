import requests
from bs4 import BeautifulSoup

# Class to wrap CSS selectors
class Selector:
    def __init__(self, *args):
        self.selectors = args
        self.count = len(args)

    def get_selectors(self):
        return self.selectors
    
    def get_item(self, index):
        return self.selectors[index]
    
    def get_count(self):
        return self.count
    

def fetch_page(url: str):
    response = requests.get(url)
    response.raise_for_status()
    return response.content

def soupify(html_content):
    # html_content: response.content
    return BeautifulSoup(html_content, "html.parser")

def select_elements(soup, selector_set: Selector):
    elements = []
    for i in range(selector_set.get_count()):
        selected = soup.select(selector_set.get_item(i))
        elements.append(selected)
    return elements

def format_results(element_list):
    # zip(*element_lists) transforms [ [a,b], [c,d] ] in zip([a,b], [c,d])
    # into (a, c), (b, d)
    zipped_tags = zip(*element_list)
    
    results = []
    for group in zipped_tags:
        # group is a Tag tuple, es: (<tag_name>, <tag_price>)
        cleaned_group = [tag.text.strip() for tag in group]
        results.append(cleaned_group)
    
    return results