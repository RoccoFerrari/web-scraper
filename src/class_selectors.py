# Abstract Base Class
from abc import ABC, abstractmethod
from bs4.element import Tag
from bs4 import BeautifulSoup
from typing import List, Any, Optional

class AbstractSelector(ABC):
    """
    Abstract base class for all selectors.
    """

    def __init__(self, *selector_queries: str):
        """
        Initialize the selector with one or more CSS selector queries.
        """
        if not selector_queries:
            raise ValueError("At least one selector query must be provided.")
        self._selectors = list(selector_queries)

    def find_elements(self, soup: BeautifulSoup) -> List[Tag]:
        """
        Find and return elements from the soup based on the selector queries.
        """
        for query in self._selectors:
            elements = soup.select(query)
            if elements:
                return elements
        return []

    @abstractmethod
    def extract(self, element: Tag) -> Optional[str]:
        """
        Extract data from the given HTML element (text or attribute).
        """
        pass

    def get_item(self, index: int):
        return self._selectors[index]

    def get_count(self):
        return len(self._selectors)
    

# Concrete Implementation
class TagSelector(AbstractSelector):
    """
    Concrete implementation of BaseSelector for HTML tag selection.
    """

    def extract(self, element: Tag) -> Optional[str]:
        """Extract the text content from the HTML element."""
        if element:
            return element.get_text(strip=True)
        return None

    
class AttributeSelector(AbstractSelector):
    """
    Concrete implementation of BaseSelector for HTML attribute selection.
    """

    def __init__(self, attribute_name: str, *selector_queries: str):
        """
        Initialize the selector with an attribute name and one or more CSS selector queries.
        """
        super().__init__(*selector_queries)
        self.attribute_name = attribute_name

    def extract(self, element: Tag) -> Optional[str]:
        """Extract the specified attribute's value from the HTML element."""
        if element:
            return element.get(self.attribute_name)
        return None