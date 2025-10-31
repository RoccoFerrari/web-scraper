from utils import _save_as_csv, _save_as_json
from typing import Callable, Dict, List, Any

# Dispatcher dictionary
# Mapping data formats to their respective functions
# Format: Dict[str, function]
SAVER_REGISTRY: Dict[str, Callable[[List[List[Any]], str], None]] = {
    'csv': _save_as_csv,
    'json': _save_as_json,
}