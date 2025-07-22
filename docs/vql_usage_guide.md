# VQL (Visual Query Language) Usage Guide

This guide explains how to use VQL (Visual Query Language) for different types of searches in the Visual Layer SDK.

## What is VQL?

VQL (Visual Query Language) is a structured query language that provides a consistent and flexible way to search datasets. It offers more advanced querying capabilities compared to simple parameter-based searches.

## VQL vs Non-VQL Search Methods

### Current Implementation Status

| Search Type | Non-VQL Method | VQL Method | Status |
|-------------|----------------|------------|---------|
| **Labels** | `search_by_labels()` | `search_by_labels_vql()` | ✅ Both Available |
| **Captions** | `search_by_captions()` | `search_by_captions_vql()` | ✅ Both Available |
| **Issues** | Not Available | `search_by_issues()` | ✅ VQL Only |
| **Visual Similarity** | Not Available | `search_by_visual_similarity()` | ✅ VQL Only |

## VQL Search Methods

### 1. Label Search with VQL

```python
from visual_layer_sdk.dataset import Dataset

# Initialize dataset
dataset = Dataset(client, dataset_id)

# Search for images with specific labels using VQL
df = dataset.search_by_labels_vql(labels=["cat", "dog"])

# Parameters:
# - labels: List of label strings to search for
# - entity_type: "IMAGES" or "OBJECTS" (default: "IMAGES")
# - poll_interval: Seconds between status polls (default: 10)
# - timeout: Maximum seconds to wait (default: 300)
```

**VQL Structure:**
```json
[{"labels": {"op": "in", "value": ["cat", "dog"]}}]
```

### 2. Caption Search with VQL

```python
# Search for images with specific caption text using VQL
df = dataset.search_by_captions_vql(captions="cat sitting")

# Parameters:
# - captions: String to search in captions
# - entity_type: "IMAGES" or "OBJECTS" (default: "IMAGES")
# - poll_interval: Seconds between status polls (default: 10)
# - timeout: Maximum seconds to wait (default: 300)
```

**VQL Structure:**
```json
[{"captions": {"op": "contains", "value": "cat sitting"}}]
```

### 3. Issue Search with VQL

```python
# Search for images with specific issues using VQL
df = dataset.search_by_issues(issue_types=["blur", "dark"])

# Parameters:
# - issue_types: List of issue type strings
# - entity_type: "IMAGES" or "OBJECTS" (default: "IMAGES")
# - confidence_min: Minimum confidence threshold (default: 0.8)
# - confidence_max: Maximum confidence threshold (default: 1.0)
# - poll_interval: Seconds between status polls (default: 10)
# - timeout: Maximum seconds to wait (default: 300)
```

**VQL Structure:**
```json
[{"issues": {"op": "issue", "value": "blur", "confidence_min": 0.8, "confidence_max": 1.0, "mode": "in"}}]
```

### 4. Visual Similarity Search with VQL

```python
# Search for visually similar images using VQL
df = dataset.search_by_visual_similarity(
    media_id="your_media_id",
    threshold=0.5
)

# Parameters:
# - media_id: The anchor media ID to search for similar images
# - threshold: Similarity threshold (default: 0.5)
# - anchor_type: Anchor type (default: "UPLOAD")
# - entity_type: "IMAGES" or "OBJECTS" (default: "IMAGES")
# - poll_interval: Seconds between status polls (default: 10)
# - timeout: Maximum seconds to wait (default: 300)
```

**VQL Structure:**
```json
[{"similarity": {"op": "upload", "value": "your_media_id", "threshold": 0.5}}]
```

## VQL Operators

### Label Search Operators
- `"in"`: Search for images that have any of the specified labels
- `"not_in"`: Search for images that don't have any of the specified labels
- `"all"`: Search for images that have all of the specified labels

### Caption Search Operators
- `"contains"`: Search for images with captions containing the specified text
- `"equals"`: Search for images with captions exactly matching the specified text
- `"starts_with"`: Search for images with captions starting with the specified text
- `"ends_with"`: Search for images with captions ending with the specified text

### Issue Search Operators
- `"issue"`: Search for images with specific issue types
- `"confidence_min"`: Minimum confidence threshold for issue detection
- `"confidence_max"`: Maximum confidence threshold for issue detection
- `"mode"`: Search mode ("in" for any of the specified issues)

### Visual Similarity Operators
- `"upload"`: Use uploaded images as anchor
- `"threshold"`: Similarity threshold (0.0 to 1.0)

## Advanced VQL Examples

### Complex Label Search
```python
# Search for images with multiple label conditions
# This would require custom VQL construction
vql = [
    {"labels": {"op": "in", "value": ["cat", "dog"]}},
    {"labels": {"op": "not_in", "value": ["person"]}}
]
```

### Complex Caption Search
```python
# Search for images with specific caption patterns
# This would require custom VQL construction
vql = [
    {"captions": {"op": "contains", "value": "cat"}},
    {"captions": {"op": "contains", "value": "outdoors"}}
]
```

### Combined Search
```python
# Search for images with both specific labels and captions
# This would require custom VQL construction
vql = [
    {"labels": {"op": "in", "value": ["cat"]}},
    {"captions": {"op": "contains", "value": "sitting"}}
]
```

## Comparison: VQL vs Non-VQL Methods

### Label Search Comparison

**Non-VQL Method:**
```python
# Uses 'labels' parameter
params = {"export_format": "json", "include_images": False, "labels": json.dumps(labels)}
```

**VQL Method:**
```python
# Uses 'vql' parameter with structured query
vql = [{"labels": {"op": "in", "value": labels}}]
params = {"export_format": "json", "include_images": False, "entity_type": entity_type, "vql": json.dumps(vql)}
```

### Caption Search Comparison

**Non-VQL Method:**
```python
# Uses 'caption_only_filter' parameter
params = {"export_format": "json", "include_images": False, "caption_only_filter": captions}
```

**VQL Method:**
```python
# Uses 'vql' parameter with structured query
vql = [{"captions": {"op": "contains", "value": captions}}]
params = {"export_format": "json", "include_images": False, "entity_type": entity_type, "vql": json.dumps(vql)}
```

## VQL Advantages

1. **Consistency**: All search types use the same parameter structure
2. **Flexibility**: Supports complex query operations and combinations
3. **Extensibility**: Easy to add new operators and search types
4. **Precision**: Better control over search operators and thresholds
5. **Future-proof**: Designed for advanced query features

## Error Handling

VQL methods include comprehensive error handling:

```python
try:
    df = dataset.search_by_labels_vql(labels=["cat"])
    if len(df) > 0:
        print(f"Found {len(df)} images")
    else:
        print("No images found matching criteria")
except ValueError as e:
    print(f"Invalid parameters: {e}")
except Exception as e:
    print(f"Search failed: {e}")
```

## Performance Considerations

- VQL searches are asynchronous and may take time to complete
- Use appropriate `poll_interval` and `timeout` values
- Monitor search progress through logging
- Consider dataset size when setting timeout values

## Best Practices

1. **Start Simple**: Begin with basic VQL queries before moving to complex ones
2. **Test Parameters**: Verify your search parameters with small datasets first
3. **Monitor Logs**: Use the logging system to track search progress
4. **Handle Errors**: Always include proper error handling for production use
5. **Optimize Timeouts**: Set appropriate timeout values based on dataset size

## Complete Example

```python
import os
from dotenv import load_dotenv
from visual_layer_sdk import VisualLayerClient

# Load environment variables
load_dotenv()

# Initialize client
client = VisualLayerClient(
    api_key=os.getenv("VISUAL_LAYER_API_KEY"),
    api_secret=os.getenv("VISUAL_LAYER_API_SECRET")
)

# Get dataset
dataset = client.get_dataset_object("your_dataset_id")

# VQL Label Search
print("🔍 Searching for cat images using VQL...")
df_cats = dataset.search_by_labels_vql(labels=["cat"])
print(f"Found {len(df_cats)} cat images")

# VQL Caption Search
print("🔍 Searching for images with 'sitting' in captions using VQL...")
df_sitting = dataset.search_by_captions_vql(captions="sitting")
print(f"Found {len(df_sitting)} images with 'sitting' in captions")

# VQL Issue Search
print("🔍 Searching for blurry images using VQL...")
df_blur = dataset.search_by_issues(issue_types=["blur"])
print(f"Found {len(df_blur)} blurry images")

# Save results
df_cats.to_csv("cat_images_vql.csv", index=False)
df_sitting.to_csv("sitting_images_vql.csv", index=False)
df_blur.to_csv("blurry_images_vql.csv", index=False)
```

## Troubleshooting

### Common Issues

1. **No Results Found**: Check if your search criteria are too specific
2. **Timeout Errors**: Increase timeout value for large datasets
3. **Invalid Parameters**: Verify parameter types and values
4. **API Errors**: Check API credentials and network connectivity

### Debug Tips

1. Enable verbose logging to see detailed request/response information
2. Test with simple queries before complex ones
3. Check dataset status before searching
4. Monitor API rate limits

## Conclusion

VQL provides a powerful and flexible way to search your Visual Layer datasets. While the non-VQL methods are simpler for basic searches, VQL offers more advanced capabilities and consistency across different search types. Choose the method that best fits your use case and complexity requirements. 