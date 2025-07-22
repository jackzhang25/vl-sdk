#!/usr/bin/env python3
"""
Demo script showing how to use the issue search functionality in the Visual Layer SDK.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual_layer_sdk.client import VisualLayerClient
from visual_layer_sdk.dataset import Dataset


def demo_issue_type_mapping():
    """Demo: Show issue type ID to name mapping"""
    print("🚀 Visual Layer SDK - Issue Search Demo")
    print("=" * 60)

    print("📋 Issue Type ID to Name Mapping:")
    print("-" * 50)

    issue_mapping = Dataset.list_available_issue_types()
    print("| ID | Issue Type Name | Description | Severity |")
    print("|----|-----------------|-------------|----------|")

    for issue_id, info in issue_mapping.items():
        severity_name = {0: "High", 1: "Medium", 2: "Low"}[info["severity"]]
        print(f"| {issue_id} | {info['name']:<15} | {info['description']:<11} | {severity_name:<8} |")

    print("\n💡 Severity Levels:")
    print("• 0: High severity (mislabels, outliers, duplicates, normal, label_outlier)")
    print("• 1: Medium severity (blur, dark)")
    print("• 2: Low severity (bright)")


def demo_issue_search_by_ids(client, dataset_id):
    """Demo: Search by issue type IDs"""
    print("\n" + "=" * 60)
    print("DEMO: Search by Issue Type IDs")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for high-severity issues (IDs 0, 1, 2, 6, 7)
    print("🔍 Searching for high-severity issues (IDs: 0, 1, 2, 6, 7)...")
    high_severity_results = dataset.search_by_issues(issue_types=[0, 1, 2, 6, 7])
    print(f"✅ Found {len(high_severity_results)} images with high-severity issues")

    # Search for image quality issues (IDs 3, 4, 5)
    print("\n🔍 Searching for image quality issues (IDs: 3, 4, 5)...")
    quality_results = dataset.search_by_issues(issue_types=[3, 4, 5])
    print(f"✅ Found {len(quality_results)} images with quality issues")

    # Search for specific issue types
    print("\n🔍 Searching for blurry images (ID: 3)...")
    blur_results = dataset.search_by_issues(issue_types=[3])
    print(f"✅ Found {len(blur_results)} blurry images")

    print("\n🔍 Searching for duplicate images (ID: 2)...")
    duplicate_results = dataset.search_by_issues(issue_types=[2])
    print(f"✅ Found {len(duplicate_results)} duplicate images")


def demo_issue_search_by_names(client, dataset_id):
    """Demo: Search by issue type names"""
    print("\n" + "=" * 60)
    print("DEMO: Search by Issue Type Names")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for blurry images by name
    print("🔍 Searching for blurry images by name...")
    blur_results = dataset.search_by_issues(issue_types=["blur"])
    print(f"✅ Found {len(blur_results)} blurry images")

    # Search for multiple issue types by name
    print("\n🔍 Searching for dark and bright images...")
    lighting_results = dataset.search_by_issues(issue_types=["dark", "bright"])
    print(f"✅ Found {len(lighting_results)} images with lighting issues")

    # Search for outliers and mislabels
    print("\n🔍 Searching for outliers and mislabels...")
    data_quality_results = dataset.search_by_issues(issue_types=["outliers", "mislabels"])
    print(f"✅ Found {len(data_quality_results)} images with data quality issues")


def demo_vql_search(client, dataset_id):
    """Demo: Search using VQL (Visual Query Language)"""
    print("\n" + "=" * 60)
    print("DEMO: Search using VQL (Visual Query Language)")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # VQL query for high-severity issues
    print("🔍 Searching with VQL for high-severity issues...")
    vql_query = '{"issue_type": ["mislabels", "outliers", "duplicates"], "severity": [0]}'
    vql_results = dataset.search_by_issues(issue_types=vql_query)
    print(f"✅ Found {len(vql_results)} images with high-severity issues using VQL")

    # VQL query for image quality issues with confidence threshold
    print("\n🔍 Searching with VQL for quality issues with confidence > 0.8...")
    quality_vql = '{"issue_type": ["blur", "dark", "bright"], "confidence": {"min": 0.8}}'
    quality_results = dataset.search_by_issues(issue_types=quality_vql)
    print(f"✅ Found {len(quality_results)} images with quality issues (confidence > 0.8)")


def demo_severity_filtering(client, dataset_id):
    """Demo: Filter by severity levels"""
    print("\n" + "=" * 60)
    print("DEMO: Filter by Severity Levels")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for high-severity issues only
    print("🔍 Searching for high-severity issues only...")
    high_severity = dataset.search_by_issues(severity_levels=[0])
    print(f"✅ Found {len(high_severity)} images with high-severity issues")

    # Search for medium and low severity issues
    print("\n🔍 Searching for medium and low severity issues...")
    medium_low = dataset.search_by_issues(severity_levels=[1, 2])
    print(f"✅ Found {len(medium_low)} images with medium/low severity issues")

    # Search for all severity levels
    print("\n🔍 Searching for all severity levels...")
    all_severities = dataset.search_by_issues(severity_levels=[0, 1, 2])
    print(f"✅ Found {len(all_severities)} images with any severity issues")


def demo_confidence_filtering(client, dataset_id):
    """Demo: Filter by confidence threshold"""
    print("\n" + "=" * 60)
    print("DEMO: Filter by Confidence Threshold")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search with high confidence threshold
    print("🔍 Searching for issues with confidence > 0.9...")
    high_confidence = dataset.search_by_issues(confidence_threshold=0.9)
    print(f"✅ Found {len(high_confidence)} images with high-confidence issues")

    # Search with medium confidence threshold
    print("\n🔍 Searching for issues with confidence > 0.7...")
    medium_confidence = dataset.search_by_issues(confidence_threshold=0.7)
    print(f"✅ Found {len(medium_confidence)} images with medium-confidence issues")


def demo_combined_filters(client, dataset_id):
    """Demo: Combine multiple filters"""
    print("\n" + "=" * 60)
    print("DEMO: Combined Filters")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Combine issue types with severity and confidence
    print("🔍 Searching for high-severity blur/dark issues with confidence > 0.8...")
    combined_results = dataset.search_by_issues(issue_types=["blur", "dark"], severity_levels=[1], confidence_threshold=0.8)
    print(f"✅ Found {len(combined_results)} images matching combined criteria")

    # Combine with additional filters
    print("\n🔍 Searching with additional filters...")
    additional_filters = {"labels": ["cat", "dog"], "origins": ["VL"]}  # Only images with cat or dog labels  # Only Visual Layer generated images
    filtered_results = dataset.search_by_issues(issue_types=["mislabels", "outliers"], additional_filters=additional_filters)
    print(f"✅ Found {len(filtered_results)} images with data quality issues in cat/dog images")


def demo_issue_management(client, dataset_id):
    """Demo: Issue management functions"""
    print("\n" + "=" * 60)
    print("DEMO: Issue Management Functions")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Get available issue types for this dataset
    print("📋 Getting available issue types for this dataset...")
    try:
        issue_types = dataset.get_issue_types()
        print(f"✅ Found {len(issue_types)} available issue types")
        for issue_type in issue_types:
            print(f"  • {issue_type}")
    except Exception as e:
        print(f"⚠️  Could not retrieve issue types: {str(e)}")

    # Get dataset issues
    print("\n📊 Getting dataset issues...")
    try:
        dataset_issues = dataset.get_dataset_issues(filter_by={"issue_type_id": [0, 1, 2]}, sort_by="severity")  # High severity issues
        print(f"✅ Found {len(dataset_issues)} dataset issues")
    except Exception as e:
        print(f"⚠️  Could not retrieve dataset issues: {str(e)}")


def demo_issue_info_utilities():
    """Demo: Issue information utility functions"""
    print("\n" + "=" * 60)
    print("DEMO: Issue Information Utilities")
    print("=" * 60)

    # Get information about specific issue types
    print("🔍 Getting information about specific issue types...")

    # By ID
    blur_info = Dataset.get_issue_type_info(issue_id=3)
    print(f"Issue ID 3: {blur_info}")

    # By name
    duplicate_info = Dataset.get_issue_type_info(issue_name="duplicates")
    print(f"Issue name 'duplicates': {duplicate_info}")

    # Get all available issue types
    print("\n📋 All available issue types:")
    all_issues = Dataset.list_available_issue_types()
    for issue_id, info in all_issues.items():
        print(f"  {issue_id}: {info['name']} - {info['description']} (Severity: {info['severity']})")


def main():
    """Run all issue search demos"""

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

    # Test dataset ID (you can change this to a real dataset ID)
    test_dataset_id = "5db7f426-4fdf-11ef-8d8b-5e82a4538d0f"

    try:
        # Run all demos
        demo_issue_type_mapping()
        demo_issue_search_by_ids(client, test_dataset_id)
        demo_issue_search_by_names(client, test_dataset_id)
        demo_vql_search(client, test_dataset_id)
        demo_severity_filtering(client, test_dataset_id)
        demo_confidence_filtering(client, test_dataset_id)
        demo_combined_filters(client, test_dataset_id)
        demo_issue_management(client, test_dataset_id)
        demo_issue_info_utilities()

    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")

    print("\n" + "=" * 60)
    print("📝 SUMMARY OF ISSUE SEARCH FEATURES")
    print("=" * 60)

    print("\n🎯 Search Methods:")
    print("• Search by issue type IDs (0-7)")
    print("• Search by issue type names (mislabels, outliers, etc.)")
    print("• Search using VQL (Visual Query Language)")
    print("• Filter by severity levels (0=High, 1=Medium, 2=Low)")
    print("• Filter by confidence threshold")
    print("• Combine multiple filters")

    print("\n🔧 Management Functions:")
    print("• Get available issue types for dataset")
    print("• Get dataset issues with filtering")
    print("• Get cluster-specific issues")
    print("• Get image-specific issues")
    print("• Get issue type information")

    print("\n💡 Use Cases:")
    print("• Find problematic images for review")
    print("• Identify data quality issues")
    print("• Filter by confidence for reliable results")
    print("• Combine with other filters for targeted search")
    print("• Export issue data for analysis")

    print("\n✅ Demo Complete!")
    print("The issue search functionality provides comprehensive tools for finding and managing data quality issues.")


if __name__ == "__main__":
    main()
