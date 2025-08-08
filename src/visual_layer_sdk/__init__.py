"""
Visual Layer SDK

A Python SDK for interacting with the Visual Layer API.
"""

from .client import VisualLayerClient
from .dataset import Dataset, IssueType, SearchOperator
from .exceptions import VisualLayerException

__version__ = "0.1.27"
__all__ = [
    "VisualLayerClient",
    "Dataset",
    "SearchOperator",
    "IssueType",
    "VisualLayerException",
    "SearchableDataset",
]
