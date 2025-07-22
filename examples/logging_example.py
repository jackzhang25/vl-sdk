#!/usr/bin/env python3
"""
Example script demonstrating the Visual Layer SDK logging system.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual_layer_sdk.client import VisualLayerClient
from visual_layer_sdk.logger import get_logger, set_verbose, set_log_level
import logging


def main():
    """Demonstrate the logging system with different scenarios."""

    # Load environment variables
    load_dotenv()

    # Get API credentials
    API_KEY = os.getenv("VISUAL_LAYER_API_KEY")
    API_SECRET = os.getenv("VISUAL_LAYER_API_SECRET")

    if not API_KEY or not API_SECRET:
        print("❌ Error: API credentials not found in environment variables")
        print("Please set VISUAL_LAYER_API_KEY and VISUAL_LAYER_API_SECRET in your .env file")
        return

    # Initialize client
    print("🚀 Initializing Visual Layer client...")
    client = VisualLayerClient(API_KEY, API_SECRET)

    # Example 1: Normal logging (INFO level)
    print("\n" + "=" * 50)
    print("EXAMPLE 1: Normal Logging (INFO level)")
    print("=" * 50)

    try:
        # Health check
        health_status = client.healthcheck()
        client.logger.api_health_check(health_status)

        # Get sample datasets
        sample_datasets = client.get_sample_datasets()
        client.logger.success(f"Retrieved {len(sample_datasets)} sample datasets")

    except Exception as e:
        client.logger.error(f"Error in normal logging example: {str(e)}")

    # Example 2: Verbose logging (DEBUG level)
    print("\n" + "=" * 50)
    print("EXAMPLE 2: Verbose Logging (DEBUG level)")
    print("=" * 50)

    # Enable verbose logging
    set_verbose(True)

    try:
        # This will now show detailed request information
        client.logger.info("Making a request with verbose logging enabled...")
        health_status = client.healthcheck()
        client.logger.api_health_check(health_status)

    except Exception as e:
        client.logger.error(f"Error in verbose logging example: {str(e)}")

    # Example 3: Dataset operations with natural messages
    print("\n" + "=" * 50)
    print("EXAMPLE 3: Dataset Operations")
    print("=" * 50)

    # Reset to normal logging
    set_verbose(False)

    try:
        # Simulate dataset creation process
        client.logger.info("Creating a new dataset...")
        client.logger.dataset_created("test-dataset-123", "My Test Dataset")

        # Simulate upload process
        client.logger.dataset_uploading("My Test Dataset")
        client.logger.dataset_uploaded("My Test Dataset")

        # Simulate processing
        client.logger.dataset_processing("My Test Dataset")
        client.logger.dataset_ready("My Test Dataset")

        # Simulate search operations
        client.logger.search_started("labels", "cat")
        client.logger.search_completed(42, "labels", "cat")

        client.logger.search_started("captions", "people")
        client.logger.search_completed(0, "captions", "people")

        # Simulate export operations
        client.logger.export_started("test-dataset-123")
        client.logger.export_completed("test-dataset-123", 150)

    except Exception as e:
        client.logger.error(f"Error in dataset operations example: {str(e)}")

    # Example 4: Error handling
    print("\n" + "=" * 50)
    print("EXAMPLE 4: Error Handling")
    print("=" * 50)

    try:
        # Simulate various error scenarios
        client.logger.warning("Dataset is not ready for export")
        client.logger.dataset_not_ready("test-dataset-456", "processing")

        client.logger.error("Failed to connect to API")
        client.logger.request_error("Connection timeout")

        client.logger.export_failed("test-dataset-789", "Dataset not found")

    except Exception as e:
        client.logger.error(f"Error in error handling example: {str(e)}")

    print("\n" + "=" * 50)
    print("✅ Logging Examples Complete!")
    print("=" * 50)

    print("\n📝 Summary of logging features:")
    print("• Natural, user-friendly messages with emojis")
    print("• Different log levels (INFO, DEBUG, WARNING, ERROR)")
    print("• Specialized methods for common operations")
    print("• Easy to enable/disable verbose logging")
    print("• Consistent formatting across all SDK operations")


if __name__ == "__main__":
    main()
