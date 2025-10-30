from queue import Queue
import scraper_logic as sl
from class_selectors import GUIRef, TagSelector

selectors = [TagSelector('h3')]

gui_ref = GUIRef(url='https://books.toscrape.com/', format='csv', selectors=selectors)
q = Queue()

sl.execute_scraping(gui_ref, q)

res = q.get()
print(type(res))
if isinstance(res, Exception):
    print('ERROR:', res)
else:
    print('LEN:', len(res))
    for row in res[:10]:
        print(row)
