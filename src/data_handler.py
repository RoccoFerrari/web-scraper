from config import SAVER_REGISTRY
from typing import List, Any

# Dispatcher dictionary (in config.py)

def save_data(results: List[List[Any]], format: str, filepath: str):
    """
    Save results to a file in the specified format.
    """
    if not results: 
        raise ValueError("No data.") 

    # Search for the appropriate saving function
    saver_function = SAVER_REGISTRY.get(format)
    
    # Check if the format is supported
    if not saver_function:
        raise ValueError(f"Format not supported: {format}")

    # Run the saving function
    try:
        saver_function(results, filepath)
    except IOError as e:
        raise Exception(f"Error during writing: {e}")
