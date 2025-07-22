#!/usr/bin/env python3
"""
Example script demonstrating how to use VQL (Visual Query Language) for different types of searches.
This shows both the existing VQL methods and the new VQL methods for labels and captions.
"""

import os
import sys
from dotenv import load_dotenv

# Add the src directory to the path so we can import the SDK
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from visual_layer_sdk.client import VisualLayerClient
from visual_layer_sdk.dataset import Dataset


def demo_vql_issue_search(client, dataset_id):
    """Demo: Search by issues using VQL (already implemented)"""
    print("\n" + "=" * 60)
    print("DEMO: VQL Issue Search")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for blurry images using VQL
    print("🔍 Searching for blurry images using VQL...")
    try:
        df_blur = dataset.search_by_issues_to_dataframe(issue_types=["blur"])
        print(f"✅ Found {len(df_blur)} blurry images using VQL")
        if len(df_blur) > 0:
            print(f"Sample results: {df_blur.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Search for multiple issue types using VQL
    print("\n🔍 Searching for multiple issue types using VQL...")
    try:
        df_multiple = dataset.search_by_issues_to_dataframe(issue_types=["blur", "dark", "outliers"])
        print(f"✅ Found {len(df_multiple)} images with multiple issues using VQL")
        if len(df_multiple) > 0:
            print(f"Sample results: {df_multiple.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def demo_vql_visual_similarity_search(client, dataset_id):
    """Demo: Search by visual similarity using VQL (already implemented)"""
    print("\n" + "=" * 60)
    print("DEMO: VQL Visual Similarity Search")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Note: You need a valid media_id for this to work
    # This is just an example - replace with a real media_id from your dataset
    example_media_id = "example_media_id_123"  # Replace with actual media_id

    print("🔍 Searching for visually similar images using VQL...")
    print(f"⚠️  Note: Using example media_id '{example_media_id}' - replace with real media_id")

    try:
        # This will likely fail with the example media_id, but shows the VQL usage
        df_similar = dataset.search_by_visual_similarity_to_dataframe(media_id=example_media_id, threshold=0.5)
        print(f"✅ Found {len(df_similar)} similar images using VQL")
        if len(df_similar) > 0:
            print(f"Sample results: {df_similar.head(3)}")
    except Exception as e:
        print(f"❌ Error (expected with example media_id): {str(e)}")


def demo_vql_label_search(client, dataset_id):
    """Demo: Search by labels using VQL (new implementation)"""
    print("\n" + "=" * 60)
    print("DEMO: VQL Label Search")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for images with specific labels using VQL
    print("🔍 Searching for images with 'cat' label using VQL...")
    try:
        df_cat = dataset.search_by_labels_vql_to_dataframe(labels=["cat"])
        print(f"✅ Found {len(df_cat)} images with 'cat' label using VQL")
        if len(df_cat) > 0:
            print(f"Sample results: {df_cat.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Search for images with multiple labels using VQL
    print("\n🔍 Searching for images with multiple labels using VQL...")
    try:
        df_multiple = dataset.search_by_labels_vql_to_dataframe(labels=["cat", "dog", "person"])
        print(f"✅ Found {len(df_multiple)} images with multiple labels using VQL")
        if len(df_multiple) > 0:
            print(f"Sample results: {df_multiple.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Compare with non-VQL method
    print("\n🔍 Comparing with non-VQL label search...")
    try:
        df_non_vql = dataset.search_by_labels_to_dataframe(labels=["cat"])
        print(f"✅ Found {len(df_non_vql)} images with 'cat' label using non-VQL method")
        if len(df_non_vql) > 0:
            print(f"Sample results: {df_non_vql.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def demo_vql_caption_search(client, dataset_id):
    """Demo: Search by captions using VQL (new implementation)"""
    print("\n" + "=" * 60)
    print("DEMO: VQL Caption Search")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    # Search for images with specific caption text using VQL
    print("🔍 Searching for images with 'cat' in captions using VQL...")
    try:
        df_cat = dataset.search_by_captions_vql_to_dataframe(caption_text="cat")
        print(f"✅ Found {len(df_cat)} images with 'cat' in captions using VQL")
        if len(df_cat) > 0:
            print(f"Sample results: {df_cat.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Search for images with more complex caption text using VQL
    print("\n🔍 Searching for images with 'sitting outdoors' in captions using VQL...")
    try:
        df_complex = dataset.search_by_captions_vql_to_dataframe(caption_text="sitting outdoors")
        print(f"✅ Found {len(df_complex)} images with 'sitting outdoors' in captions using VQL")
        if len(df_complex) > 0:
            print(f"Sample results: {df_complex.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Compare with non-VQL method
    print("\n🔍 Comparing with non-VQL caption search...")
    try:
        df_non_vql = dataset.search_by_captions_to_dataframe(caption_text=["cat"])
        print(f"✅ Found {len(df_non_vql)} images with 'cat' in captions using non-VQL method")
        if len(df_non_vql) > 0:
            print(f"Sample results: {df_non_vql.head(3)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")


def demo_advanced_vql_queries(client, dataset_id):
    """Demo: Advanced VQL query examples"""
    print("\n" + "=" * 60)
    print("DEMO: Advanced VQL Queries")
    print("=" * 60)

    dataset = Dataset(client, dataset_id)

    print("🔍 Advanced VQL Query Examples:")
    print("• These examples show the VQL structure used internally")
    print("• You can modify the VQL directly for more complex queries")

    # Example 1: Issue search VQL structure
    print("\n📋 Example 1: Issue Search VQL Structure")
    issue_vql = [{"issues": {"op": "issue", "value": "blur", "confidence_min": 0.8, "confidence_max": 1.0, "mode": "in"}}]
    print(f"VQL for blur issues: {issue_vql}")

    # Example 2: Visual similarity VQL structure
    print("\n📋 Example 2: Visual Similarity VQL Structure")
    similarity_vql = [{"similarity": {"op": "upload", "value": "media_id_123", "threshold": 0.5}}]
    print(f"VQL for visual similarity: {similarity_vql}")

    # Example 3: Label search VQL structure
    print("\n📋 Example 3: Label Search VQL Structure")
    label_vql = [{"labels": {"op": "in", "value": ["cat", "dog"]}}]
    print(f"VQL for label search: {label_vql}")

    # Example 4: Caption search VQL structure
    print("\n📋 Example 4: Caption Search VQL Structure")
    caption_vql = [{"captions": {"op": "contains", "value": "cat sitting"}}]
    print(f"VQL for caption search: {caption_vql}")


def demo_vql_parameter_comparison():
    """Demo: Compare VQL vs non-VQL parameters"""
    print("\n" + "=" * 60)
    print("DEMO: VQL vs Non-VQL Parameter Comparison")
    print("=" * 60)

    print("📊 Parameter Comparison:")
    print("\n🔍 Label Search:")
    print("• Non-VQL: Uses 'labels' parameter with JSON array")
    print("• VQL: Uses 'vql' parameter with structured query")
    print("  - More flexible and extensible")
    print("  - Supports complex query operations")

    print("\n🔍 Caption Search:")
    print("• Non-VQL: Uses 'caption_only_filter' parameter with string")
    print("• VQL: Uses 'vql' parameter with structured query")
    print("  - More precise control over search operations")
    print("  - Supports different operators (contains, equals, etc.)")

    print("\n🔍 Issue Search:")
    print("• Non-VQL: Not available")
    print("• VQL: Uses 'vql' parameter with structured query")
    print("  - Only available through VQL")
    print("  - Supports confidence thresholds and multiple issue types")

    print("\n🔍 Visual Similarity Search:")
    print("• Non-VQL: Not available")
    print("• VQL: Uses 'vql' parameter with structured query")
    print("  - Only available through VQL")
    print("  - Supports different anchor types and thresholds")


def main():
    """Run all VQL search demos"""

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
        demo_vql_issue_search(client, test_dataset_id)
        demo_vql_visual_similarity_search(client, test_dataset_id)
        demo_vql_label_search(client, test_dataset_id)
        demo_vql_caption_search(client, test_dataset_id)
        demo_advanced_vql_queries(client, test_dataset_id)
        demo_vql_parameter_comparison()

    except Exception as e:
        print(f"❌ Error during demo: {str(e)}")
        import traceback

        print(f"Full error: {traceback.format_exc()}")

    print("\n" + "=" * 60)
    print("📝 SUMMARY OF VQL SEARCH FEATURES")
    print("=" * 60)

    print("\n🎯 VQL Search Methods:")
    print("• search_by_issues_to_dataframe() - Issue search using VQL")
    print("• search_by_visual_similarity_to_dataframe() - Visual similarity using VQL")
    print("• search_by_labels_vql_to_dataframe() - Label search using VQL (NEW)")
    print("• search_by_captions_vql_to_dataframe() - Caption search using VQL (NEW)")

    print("\n🔧 VQL Advantages:")
    print("• More flexible and extensible query language")
    print("• Supports complex query operations")
    print("• Consistent parameter structure across all search types")
    print("• Better control over search operators and thresholds")
    print("• Future-proof for advanced query features")

    print("\n💡 Use Cases:")
    print("• Complex multi-condition searches")
    print("• Advanced filtering with confidence thresholds")
    print("• Consistent query structure across different search types")
    print("• Future extensibility for new search operators")

    print("\n✅ Demo Complete!")
    print("VQL provides a powerful and flexible way to search your datasets with consistent syntax.")


if __name__ == "__main__":
    main()
