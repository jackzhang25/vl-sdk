"""
Visual Layer SDK

A Python SDK for interacting with the Visual Layer API.
"""

from .client import VisualLayerClient
from .dataset import Dataset, SearchOperator, IssueType
from .exceptions import VisualLayerException

__version__ = "0.1.14"
__all__ = [
    "VisualLayerClient",
    "Dataset",
    "SearchOperator",
    "IssueType",
]
