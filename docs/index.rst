Visual Layer SDK Documentation
==============================

A Python SDK for interacting with the Visual Layer API, providing easy access to dataset management, creation, and analysis capabilities.

.. image:: https://img.shields.io/badge/version-0.1.5-blue
   :alt: Version 0.1.5

.. image:: https://img.shields.io/badge/python-3.8%2B-blue
   :alt: Python 3.8+

.. image:: https://img.shields.io/badge/license-MIT-green
   :alt: MIT License

🌟 Features
-----------

- 📊 **Dataset Management** - Create, explore, and manage datasets
- 🔍 **Advanced Search** - Search by labels, captions, visual similarity, and issues
- 📋 **Pandas Integration** - Native DataFrame support for data analysis

🚀 Quick Start
--------------

.. code-block:: python

   from visual_layer_sdk import VisualLayerClient

   # Initialize client
   client = VisualLayerClient(api_key="your_api_key", api_secret="your_api_secret")

   # Check API health
   health = client.healthcheck()
   print(f"API Status: {health}")

   # Get all datasets
   datasets = client.get_all_datasets()
   print(f"Found {len(datasets)} datasets")

   # Get a specific dataset
   dataset = client.get_dataset_object("your_dataset_id")
   stats = dataset.get_stats()
   print(f"Dataset stats: {stats}")

📚 Documentation
----------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   installation.md
   getting-started.md

.. toctree::
   :maxdepth: 2
   :caption: User Guide

   search-filtering.md
   logging.md

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api-reference.md

🔗 Quick Links
--------------

- `GitHub Repository <https://github.com/jackzhang25/vl-package>`_
- :doc:`Installation Guide <installation>`
- :doc:`API Documentation <api-reference>`

💡 Need Help?
-------------

- Review the :doc:`api-reference` for detailed method documentation
- See :doc:`getting-started` for troubleshooting tips

----

*Visual Layer SDK - Making visual data analysis simple and powerful.*