# run: ../venv/bin/python main.py
import scraper_logic as sl
import requests
import sys

if __name__ == "__main__":
    
    columns_to_extract = []
    print("--- Scraper Builder ---")
    print("Define the data 'columns' you want to extract.")

    while True:
        print(f"\n--- Defining Column {len(columns_to_extract) + 1} ---")
        
        # Ask for the extraction TYPE
        prompt = (
            "What type of data do you want to extract?\n"
            " (1) Tag's Text Content\n"
            " (2) An Attribute (e.g., 'href' or 'src')\n"
            "Choice: "
        )
        choice = input(prompt)
        
        attribute_name = None
        if choice == '1':
            pass # It's a TagSelector
        elif choice == '2':
            attribute_name = input("Enter the attribute name (e.g., href): ")
            if not attribute_name:
                print("Invalid attribute name. Please try again.")
                continue
        else:
            print("Invalid choice. Please try again.")
            continue
            
        # Ask for the CSS QUERIES for this column (with fallback)
        selectors_tmp = []
        print("Enter one or more CSS queries for this column (the first one that works will be used).")
        print("Type 'END' when you are finished with THIS column.")
        
        while True:
            selector = input(f"CSS Query for Column {len(columns_to_extract) + 1}: ")
            if selector.upper() == "END":
                if not selectors_tmp:
                    print("Error: You must enter at least one CSS query for this column.")
                else:
                    break # Finished entering queries for this column
            else:
                selectors_tmp.append(selector)
        
        # Create the correct Job object and add it to the list
        if choice == '1':
            job = sl.TagSelector(*selectors_tmp)
            columns_to_extract.append(job)
        elif choice == '2' and attribute_name:
            job = sl.AttributeSelector(attribute_name, *selectors_tmp)
            columns_to_extract.append(job)
            
        print(f"--- Column {len(columns_to_extract)} added ---")
        
        # Ask if they want to add more columns
        keep_going = input("Do you want to add another column? (y/n): ")
        if keep_going.lower() != 'y':
            break 

    if not columns_to_extract:
        print("No columns defined. Exiting.")
        sys.exit(0)

    # --- Execute Scraping ---

    url = input("\nEnter the URL to scrape data from: ")

    try:
        response = sl.fetch_page(url)
        html_content = response.content
        base_url = response.url

        print(f"\n--- Fetching data from {url} ---")
        print(f"--- Number of columns to extract: {len(columns_to_extract)} ---")

        soup = sl.soupify(html_content)
        
        # Find all the lists of Tags
        tag_lists = sl.select_elements(soup, columns_to_extract)

        # Extract data (text or attribute) and format
        # We pass both the tag lists AND the jobs for extraction
        final_results = sl.format_results(tag_lists, columns_to_extract, base_url)

        print("\n--- Results ---")
        # Iterate over results and print them robustly
        for row in final_results:
            # Convert each item to a string (handling None)
            cleaned_row = [str(item) if item is not None else "N/A" for item in row]
            print(" : ".join(cleaned_row))

            
    except requests.exceptions.RequestException as e:
        print("\n --- Connection Error ---")
        print(f"An error occurred while trying to fetch the URL: {e}")
    except Exception as e:
        print(f"\n --- Error ---")
        print(f"An unexpected error occurred: {e}")
        print("Please check your CSS selectors and try again (e.g., 'h3 > a', 'p.price_color').")