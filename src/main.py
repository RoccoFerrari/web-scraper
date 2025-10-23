# run: ../venv/bin/python main.py
import requests
import scraper_logic as sl

if __name__ == "__main__":
    url = input("Insert URL: ")

    guard = True
    selectors_tmp = []
    print("\n--- Insert CSS selectors one by one. Type 'END' to finish ---")
    while guard:
        selector = input("Insert CSS selector: ")
        if selector.upper() == "END":
            guard = False
        else:
            selectors_tmp.append(selector)

    selectors = sl.Selector(*selectors_tmp)

    try:
        html_content = sl.fetch_page(url)
        print(f"\n--- Fetching data from {url} using selectors {selectors.get_selectors()} ---")

        soup = sl.soupify(html_content)
        element_list = sl.select_elements(soup, selectors)

        print("\n--- Results ---")
        for result in sl.format_results(element_list):
            print(": ".join(result))

            
    except requests.exceptions.RequestException as e:
        print("\n --- Connection Error ---")
        print(f"An error occurred while trying to fetch the URL: {e}")
    except Exception as e:
        print("\n --- Error ---")
        print(f"An unexpected error occurred: {e}")
        print("Please check your CSS selectors and try again (es. 'h3 > a', 'p.price_color').")
    

