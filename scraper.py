import requests
from bs4 import BeautifulSoup

url = input("Insert URL: ")

primary_selector = input("Insert primary CSS selector: ")
secondary_selector = input("Insert secondary CSS selector: ")

print(f"Fetching data from {url} using selectors '{primary_selector}' and '{secondary_selector}'")

try:
    response = requests.get(url)
    response.raise_for_status()  # Controlla che la richiesta sia andata a buon fine

    # 2. Analisi: Diamo l'HTML a BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    element_1 = soup.select(primary_selector)
    element_2 = soup.select(secondary_selector)

    print("--- Results ---")

    if not element_1 or not element_2:
        print("No elements found with the provided selectors.")

    if len(element_1) != len(element_2):
        print("Warning: The number of elements found with the primary selector does not match the number found with the secondary selector.")

    # Using zip to pair elements from both selectors
    for el_1, el_2 in zip(element_1, element_2):
        # Strip removes leading/trailing whitespace
        print(f"{el_1.text.strip()}: {el_2.text.strip()}")

except requests.exceptions.RequestException as e:
    print("\n --- Connection Error ---")
    print(f"An error occurred while trying to fetch the URL: {e}")

except Exception as e:
    print("\n --- Error ---")
    print(f"An unexpected error occurred: {e}")
    print("Please check your CSS selectors and try again (es. 'h3 > a', 'p.price_color').")