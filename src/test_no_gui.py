# Non-GUI test for scraper_logic.execute_scraping
from queue import Queue
import scraper_logic as sl
from class_selectors import GUIRef, TagSelector, AttributeSelector

# Prepare a fake HTML page
HTML = b"""
<html>
  <body>
    <a href="/relative/path">A link</a>
    <p class="content">Paragraph text</p>
  </body>
</html>
"""

class FakeResponse:
    def __init__(self, content, url):
        self.content = content
        self.url = url

# Monkeypatch fetch_page to avoid network
def fake_fetch_page(url: str):
    return FakeResponse(HTML, url)

sl.fetch_page = fake_fetch_page

# Build GUIRef-like object
selectors = [TagSelector('p.content'), AttributeSelector('href', 'a')]
# Note: AttributeSelector(attribute_name, selector_query)

gui_ref = GUIRef(url='http://example.com/base/', format='csv', selectors=selectors)

q = Queue()

# Run the scraping function (synchronous call)
sl.execute_scraping(gui_ref, q)

# Get and print result
result = q.get()
if isinstance(result, Exception):
    print('ERROR:', result)
else:
    print('RESULTS:')
    for row in result:
        print(row)
