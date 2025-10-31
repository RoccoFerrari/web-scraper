import csv
import json
from typing import List, Any

# private functions for specific data formats
def _save_as_csv(results: List[List[Any]], filepath: str):
    """Writes data to a CSV file."""
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(results)

def _save_as_json(results: List[List[Any]], filepath: str):
    """Writes data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)