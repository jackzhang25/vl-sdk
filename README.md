# Visual Layer SDK

A Python SDK for interacting with the Visual Layer API, providing easy access to dataset management, creation, and analysis capabilities.

## Features

- 🔐 **JWT Authentication** - Secure API access with automatic token generation
- 📊 **Dataset Management** - Create, explore, and manage datasets
- 🗂️ **Multiple Data Sources** - Support for S3 buckets and local files
- 📈 **Data Analysis** - Get statistics and explore dataset contents
- 🚀 **Easy Integration** - Simple, intuitive API design
- 📋 **Pandas Integration** - Native DataFrame support for data analysis

## Installation

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your API credentials:
```
VISUAL_LAYER_API_KEY=your_api_key_here
VISUAL_LAYER_API_SECRET=your_api_secret_here
```

## Quick Start

```python
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
```

## API Reference

### VisualLayerClient

The main client class for interacting with the Visual Layer API.

#### Initialization

- **Production (default):**

```python
client = VisualLayerClient(api_key="your_api_key", api_secret="your_api_secret")
```

- **Custom URL:**

```python
client = VisualLayerClient(api_key="your_api_key", api_secret="your_api_secret", url="https://app.staging-visual-layer.link/api/v1")
```

**Parameters:**
- `api_key` (str): Your Visual Layer API key
- `api_secret` (str): Your Visual Layer API secret
- `url` (str): API base URL. Defaults to production URL: "https://app.visual-layer.com/api/v1"

**Note:** The client automatically performs a healthcheck during initialization to validate the provided URL. If the healthcheck fails, an "Invalid URL" error will be raised.

#### Core Methods

##### `healthcheck() -> dict`
Check the health of the Visual Layer API.

```python
health = client.healthcheck()
```

##### `get_sample_datasets() -> list`
Get sample datasets available for testing.

```python
sample_datasets = client.get_sample_datasets()
```

##### `get_all_datasets() -> list`
Retrieve all datasets accessible to your account.

```python
all_datasets = client.get_all_datasets()
```

##### `get_dataset(dataset_id: str) -> pd.DataFrame`
Get dataset details as a pandas DataFrame.

```python
dataset_df = client.get_dataset("your_dataset_id")
```

**Returns:** DataFrame with dataset information including:
- id, created_by, owned_by, display_name
- description, preview_uri, source_type, source_uri
- created_at, updated_at, filename, sample, status, n_images

##### `get_dataset_object(dataset_id: str) -> Dataset`
Get a Dataset object for advanced operations.

```python
dataset = client.get_dataset_object("your_dataset_id")
```

##### `add_searchable(searchable_id: str, searchable: Searchable) -> None`
Add a Searchable object to the client's storage dictionary.

```python
# This is automatically called when Searchable objects are created
# You can also manually add searchables if needed
client.add_searchable("searchable_123", searchable_object)
```

**Parameters:**
- `searchable_id` (str): The unique ID of the Searchable object
- `searchable`: The Searchable object to store

##### `get_searchable(searchable_id: str) -> Searchable`
Get a Searchable object from the client's storage by ID.

```python
# Retrieve a previously stored searchable
searchable = client.get_searchable("searchable_123")
if searchable:
    results = searchable.get_results()
```

**Parameters:**
- `searchable_id` (str): The unique ID of the Searchable object

**Returns:** The stored Searchable object, or None if not found

##### `get_all_searchables() -> list`
Get all Searchable objects stored in the client.

```python
# Get all stored searchables
all_searchables = client.get_all_searchables()
print(f"Client has {len(all_searchables)} stored searchables")
```

**Returns:** List of all stored Searchable objects

#### Dataset Creation

##### `create_dataset_from_s3_bucket(s3_bucket_path: str, dataset_name: str, pipeline_type: str = None) -> dict`
Create a dataset from files stored in an S3 bucket.
####  `make sure to not include s3:// in the front it is already added`
```python
result = client.create_dataset_from_s3_bucket(
    s3_bucket_path="my-bucket/images/",
    dataset_name="My Image Dataset",
    pipeline_type="image_processing"
)
```

**Parameters:**
- `s3_bucket_path` (str): S3 bucket path containing the files
- `dataset_name` (str): Name for the new dataset
- `pipeline_type` (str, optional): Processing pipeline type

##### `create_dataset_from_local_folder(file_path: str, filename: str, dataset_name: str, pipeline_type: str = None) -> dict`
Create a dataset from a local zip file.

```python
result = client.create_dataset_from_local_folder(
    file_path="/path/to/images.zip",
    filename="images.zip",
    dataset_name="Local Image Dataset",
    pipeline_type="image_processing"
)
```

**Parameters:**
- `file_path` (str): Full path to the zip file
- `filename` (str): Name of the zip file
- `dataset_name` (str): Name for the new dataset
- `pipeline_type` (str, optional): Processing pipeline type

### Dataset

The Dataset class provides methods for working with individual datasets.

#### Initialization

```python
dataset = Dataset(client: VisualLayerClient, dataset_id: str)
```

#### Core Methods

##### `get_stats() -> dict`
Get comprehensive statistics for the dataset.

```python
stats = dataset.get_stats()
```

##### `get_details() -> dict`
Get detailed information about the dataset.

```python
details = dataset.get_details()
```

##### `get_status() -> str`
Get the current status of the dataset.

```python
status = dataset.get_status()
# Returns: "READY", "PROCESSING", "ERROR", etc.
```

##### `explore() -> pd.DataFrame`
Explore the dataset and return previews as a DataFrame.

```python
previews_df = dataset.explore()
```

**Returns:** DataFrame containing dataset previews from the first cluster.

##### `export() -> dict`
Export the dataset in JSON format.

```python
export_data = dataset.export()
```

**Note:** Dataset must be in "READY" or "completed" status to export.

##### `export_to_dataframe() -> pd.DataFrame`
Export the dataset and convert media items to a DataFrame.

```python
media_items_df = dataset.export_to_dataframe()
```

**Returns:** DataFrame containing media items (excluding metadata_items).

##### `delete() -> dict`
Delete the dataset permanently.

```python
result = dataset.delete()
```

##### `search() -> Searchable`
Get a Searchable object for building complex search queries.

```python
# Get searchable object
searchable = dataset.search()

# Use the searchable object to build and execute searches
results = searchable.search_by_labels(["cat"]).get_results()
```

**Returns:** A Searchable object that can be used to chain multiple search criteria together.

##### `search_by_vql(vql: List[dict], entity_type: str = "IMAGES") -> pd.DataFrame`
Search the dataset using custom VQL (Visual Query Language) asynchronously, poll until export is ready, download the results, and return as a DataFrame.

```python
# Label search
vql = [{"id": "label_filter", "labels": {"op": "one_of", "value": ["cat", "dog"]}}]
df = dataset.search_by_vql(vql)

# Caption search
vql = [{"text": {"op": "fts", "value": "cat sitting"}}]
df = dataset.search_by_vql(vql)

# Issue search
vql = [{"issues": {"op": "issue", "value": "outliers", "confidence_min": 0.8, "confidence_max": 1.0, "mode": "in"}}]
df = dataset.search_by_vql(vql)

# Visual similarity search
vql = [{"id": "similarity_search", "similarity": {"op": "upload", "value": "media_id"}}]
df = dataset.search_by_vql(vql)
```

- `vql` (List[dict]): VQL query structure as a list of filter objects
- `entity_type` (str): Entity type to search ("IMAGES" or "OBJECTS", default: "IMAGES")

**Returns:** DataFrame containing the search results, or empty if not ready or no matches found.

##### `IssueType` Enum
The `issue_type` parameter uses the `IssueType` enum:

```python
from visual_layer_sdk.dataset import IssueType

IssueType.MISLABELS      # "mislabels" - Mislabeled items
IssueType.OUTLIERS       # "outliers" - Statistical outliers
IssueType.DUPLICATES     # "duplicates" - Duplicate images
IssueType.BLUR           # "blur" - Blurry images
IssueType.DARK           # "dark" - Dark/underexposed images
IssueType.BRIGHT         # "bright" - Bright/overexposed images
IssueType.NORMAL         # "normal" - Normal images (no issues)
IssueType.LABEL_OUTLIER  # "label_outlier" - Label outliers
```

##### `SemanticRelevance` Enum
The `relevance` parameter uses the `SemanticRelevance` enum:

```python
from visual_layer_sdk.dataset import SemanticRelevance

SemanticRelevance.LOW_RELEVANCE     # 0.9 - High threshold, more precise results
SemanticRelevance.MEDIUM_RELEVANCE  # 0.8 - Default threshold, balanced results
SemanticRelevance.HIGH_RELEVANCE    # 0.7 - Low threshold, more inclusive results
```

##### `get_available_models() -> list`
Get available models for enrichment for this dataset.

```python
models = dataset.get_available_models()
print(f"Available models: {models}")
```

**Returns:** List containing available models for enrichment.

##### `enrich_dataset(enrichment_models: dict) -> dict`
Enrich the dataset with specified models.

```python
# Enrich with caption and object detection
result = dataset.enrich_dataset({
    "CAPTION_IMAGES": "vl_image_captioner_v00",
    "OBJECT_DETECTION": "vl_object_detector_v00"
})

# Enrich with semantic search
result = dataset.enrich_dataset({
    "MULTIMODEL_IMAGE_ENCODING": "DFN5B-CLIP-ViT-H-14-384-images"
})
```

- `enrichment_models` (dict): Dictionary mapping enrichment types to model names

**Returns:** Dictionary response from the enrichment API.

##### `check_enrichment_progress(enrichment_context_id: str) -> dict`
Check enrichment progress with percentage.

```python
# First get the enrichment context
context_url = f"{client.base_url}/enrichment/{dataset_id}/context"
context_response = client.session.get(context_url, headers=client._get_headers())
context_data = context_response.json()
context_id = context_data.get('context_id')

# Then check progress
progress = dataset.check_enrichment_progress(context_id)
print(f"Status: {progress['status']}")
print(f"Progress: {progress['progress']}%")
```

- `enrichment_context_id` (str): The enrichment context ID from the enrichment API

**Returns:** Dictionary containing enrichment status and progress information.

**Note:** This method also prints status and progress to the console for easy monitoring.

## Displaying Images

The SDK provides several ways to display images using the `image_uri` field returned in search results.

### Basic Image Display

```python
import requests
from PIL import Image
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from IPython.display import display, Image as IPImage

# Get search results
df = dataset.search_by_labels(["cat", "dog"])

# Method 1: Display using PIL (Python Imaging Library)
def display_image_pil(image_uri):
    """Display image using PIL"""
    response = requests.get(image_uri)
    img = Image.open(BytesIO(response.content))
    img.show()  # Opens in default image viewer

# Method 2: Display using matplotlib
def display_image_matplotlib(image_uri):
    """Display image using matplotlib"""
    response = requests.get(image_uri)
    img = mpimg.imread(BytesIO(response.content))
    plt.figure(figsize=(8, 6))
    plt.imshow(img)
    plt.axis('off')
    plt.show()

# Method 3: Display in Jupyter notebook
def display_image_jupyter(image_uri):
    """Display image in Jupyter notebook"""
    display(IPImage(url=image_uri))

# Display first 3 images from search results
for idx, row in df.head(3).iterrows():
    print(f"Image {idx}: {row['image_uri']}")
    print(f"Labels: {row.get('image_labels', 'N/A')}")
    display_image_matplotlib(row['image_uri'])
    print("---")
```

### Advanced Image Display with Information

```python
import pandas as pd
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def display_search_results_with_info(df, max_images=5):
    """Display search results with image and metadata"""
    fig, axes = plt.subplots(1, min(max_images, len(df)), figsize=(15, 5))
    if len(df) == 1:
        axes = [axes]
    
    for idx, (_, row) in enumerate(df.head(max_images).iterrows()):
        # Download and display image
        response = requests.get(row['image_uri'])
        img = mpimg.imread(BytesIO(response.content))
        
        axes[idx].imshow(img)
        axes[idx].axis('off')
        
        # Add title with metadata
        title = f"Image {idx}\n"
        if row.get('image_labels'):
            title += f"Labels: {row['image_labels'][:30]}...\n"
        if row.get('captions'):
            title += f"Caption: {row['captions'][:30]}...\n"
        if row.get('issues'):
            title += f"Issues: {row['issues'][:30]}..."
            
        axes[idx].set_title(title, fontsize=10)
    
    plt.tight_layout()
    plt.show()

# Display search results
df = dataset.search_by_labels(["cat"])
display_search_results_with_info(df, max_images=3)
```

### Image Grid Display

```python
import math

def display_image_grid(df, cols=4, figsize=(20, 15)):
    """Display images in a grid layout"""
    rows = math.ceil(len(df) / cols)
    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    
    if rows == 1:
        axes = axes.reshape(1, -1)
    elif cols == 1:
        axes = axes.reshape(-1, 1)
    
    for idx, (_, row) in enumerate(df.iterrows()):
        row_idx = idx // cols
        col_idx = idx % cols
        
        try:
            response = requests.get(row['image_uri'])
            img = mpimg.imread(BytesIO(response.content))
            axes[row_idx, col_idx].imshow(img)
            axes[row_idx, col_idx].axis('off')
            
            # Add labels as title
            labels = row.get('image_labels', '')[:20]
            axes[row_idx, col_idx].set_title(f"Labels: {labels}...", fontsize=8)
            
        except Exception as e:
            axes[row_idx, col_idx].text(0.5, 0.5, f"Error: {str(e)}", 
                                       ha='center', va='center')
            axes[row_idx, col_idx].axis('off')
    
    # Hide empty subplots
    for idx in range(len(df), rows * cols):
        row_idx = idx // cols
        col_idx = idx % cols
        axes[row_idx, col_idx].axis('off')
    
    plt.tight_layout()
    plt.show()

# Display all search results in a grid
df = dataset.search_by_labels(["cat", "dog"])
display_image_grid(df, cols=3)
```

### Interactive Image Browser

```python
import ipywidgets as widgets
from IPython.display import display, clear_output

def create_image_browser(df):
    """Create an interactive image browser"""
    if len(df) == 0:
        print("No images to display")
        return
    
    # Create widgets
    image_index = widgets.IntSlider(
        value=0, min=0, max=len(df)-1, step=1,
        description='Image:'
    )
    
    image_output = widgets.Output()
    
    def update_image(change):
        with image_output:
            clear_output(wait=True)
            idx = change['new']
            row = df.iloc[idx]
            
            # Display image
            display(IPImage(url=row['image_uri']))
            
            # Display metadata
            print(f"Image {idx + 1} of {len(df)}")
            print(f"Media ID: {row.get('media_id', 'N/A')}")
            print(f"Labels: {row.get('image_labels', 'N/A')}")
            print(f"Captions: {row.get('captions', 'N/A')}")
            print(f"Object Labels: {row.get('object_labels', 'N/A')}")
            print(f"Issues: {row.get('issues', 'N/A')}")
    
    image_index.observe(update_image, names='value')
    
    # Display initial image
    update_image({'new': 0})
    
    # Display widgets
    display(widgets.VBox([image_index, image_output]))

# Create interactive browser for search results
df = dataset.search_by_issues_to_dataframe(issue_type="blur")
create_image_browser(df)
```

### Saving Images Locally

```python
import os
from urllib.parse import urlparse

def save_images_locally(df, output_dir="downloaded_images"):
    """Save images from search results to local directory"""
    os.makedirs(output_dir, exist_ok=True)
    
    for idx, row in df.iterrows():
        try:
            # Download image
            response = requests.get(row['image_uri'])
            response.raise_for_status()
            
            # Generate filename
            media_id = row.get('media_id', f'image_{idx}')
            filename = f"{media_id}.jpg"
            filepath = os.path.join(output_dir, filename)
            
            # Save image
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"Saved: {filepath}")
            
        except Exception as e:
            print(f"Failed to save image {idx}: {e}")
    
    print(f"Saved {len(df)} images to {output_dir}/")

# Save search results locally
df = dataset.search_by_labels(["cat"])
save_images_locally(df, "cat_images")
```

### Requirements for Image Display

To use the image display examples above, install the required packages:

```bash
pip install Pillow matplotlib requests ipywidgets
```

For Jupyter notebook support:
```bash
pip install ipython
```

## Search Functionality

The SDK provides a powerful, chainable search interface through the `Searchable` class. This allows you to build complex queries by chaining multiple search criteria together.

### Basic Search Usage

```python
# Get a searchable object from the dataset
searchable = dataset.search()

# Perform searches and chain them together
results = searchable.search_by_labels(["cat", "dog"])\
                    .search_by_issues([IssueType.BLUR])\
                    .search_by_captions(["outdoors"])\
                    .get_results()

print(f"Found {len(results)} images matching all criteria")
```

### Search Methods

#### `search_by_labels(labels, search_operator)`
Search by image labels with support for different operators.

```python
from visual_layer_sdk.dataset import SearchOperator

# Search for images with specific labels
results = dataset.search().search_by_labels(["cat", "dog"]).get_results()

# Use different search operators
results = dataset.search().search_by_labels(
    ["cat", "dog"], 
    search_operator=SearchOperator.IS_ONE_OF
).get_results()

# Exclude certain labels
results = dataset.search().search_by_labels(
    ["blur", "dark"], 
    search_operator=SearchOperator.IS_NOT
).get_results()
```

#### `search_by_captions(captions, search_operator)`
Search by image captions with full-text search capabilities.

```python
# Search for images with specific captions
results = dataset.search().search_by_captions(["cat sitting", "outdoors"]).get_results()

# Use different search operators
results = dataset.search().search_by_captions(
    ["cat", "dog"], 
    search_operator=SearchOperator.IS_ONE_OF
).get_results()
```

#### `search_by_issues(issue_types, search_operator, confidence_min, confidence_max)`
Search by image quality issues with confidence thresholds.

```python
from visual_layer_sdk.dataset import IssueType, SearchOperator

# Search for images with specific issues
results = dataset.search().search_by_issues([IssueType.BLUR, IssueType.DARK]).get_results()

# Set confidence thresholds
results = dataset.search().search_by_issues(
    [IssueType.OUTLIERS], 
    confidence_min=0.7, 
    confidence_max=0.9
).get_results()

# Exclude certain issues
results = dataset.search().search_by_issues(
    [IssueType.BLUR], 
    search_operator=SearchOperator.IS_NOT
).get_results()
```

#### `search_by_semantic(text, relevance)`
Search by semantic similarity using natural language.

```python
from visual_layer_sdk.dataset import SemanticRelevance

# Search for semantically similar images
results = dataset.search().search_by_semantic("people walking on the beach").get_results()

# Adjust relevance threshold
results = dataset.search().search_by_semantic(
    "healthy plant leaves", 
    relevance=SemanticRelevance.HIGH_RELEVANCE
).get_results()
```

#### `search_by_visual_similarity(image_path, threshold, search_operator)`
Search by visual similarity using a reference image.

```python
# Search for visually similar images
results = dataset.search().search_by_visual_similarity(
    "/path/to/reference_image.jpg", 
    threshold=0.7
).get_results()

# Adjust threshold for more/less restrictive results
# Lower threshold = more restrictive (fewer results)
# Higher threshold = less restrictive (more results)
# Recommended range: 0.2-0.8
```

### Chaining Multiple Search Criteria

The power of the Searchable class comes from its ability to chain multiple search criteria together. Results are combined using intersection (AND logic) - only images that match ALL criteria are returned.

```python
# Complex search combining multiple criteria
searchable = dataset.search()

# Start with label search
searchable = searchable.search_by_labels(["cat", "dog"])

# Add issue filtering
searchable = searchable.search_by_issues([IssueType.BLUR])

# Add caption search
searchable = searchable.search_by_captions(["outdoors"])

# Add semantic search
searchable = searchable.search_by_semantic("pet animals")

# Get final results
results = searchable.get_results()
print(f"Found {len(results)} images matching all criteria")
```

### Search Operators

The SDK provides several search operators for different types of searches:

```python
from visual_layer_sdk.dataset import SearchOperator

SearchOperator.IS              # Items must have ALL specified values
SearchOperator.IS_NOT          # Items must NOT have ALL specified values together
SearchOperator.IS_ONE_OF       # Items must have AT LEAST ONE of the specified values
SearchOperator.IS_NOT_ONE_OF   # Items must have NONE of the specified values
```

### Issue Types

Available issue types for quality filtering:

```python
from visual_layer_sdk.dataset import IssueType

IssueType.MISLABELS      # Mislabeled items
IssueType.OUTLIERS       # Statistical outliers
IssueType.DUPLICATES     # Duplicate images
IssueType.BLUR           # Blurry images
IssueType.DARK           # Dark/underexposed images
IssueType.BRIGHT         # Bright/overexposed images
IssueType.NORMAL         # Normal images (no issues)
IssueType.LABEL_OUTLIER  # Label outliers
```

### Semantic Relevance Levels

Control the precision of semantic search:

```python
from visual_layer_sdk.dataset import SemanticRelevance

SemanticRelevance.LOW_RELEVANCE     # 0.9 - High threshold, more precise results
SemanticRelevance.MEDIUM_RELEVANCE  # 0.8 - Default threshold, balanced results
SemanticRelevance.HIGH_RELEVANCE    # 0.7 - Low threshold, more inclusive results
```

### Getting Results

#### `get_results(entity_type="IMAGES")`
Execute the accumulated search query and return results as a DataFrame.

```python
# Execute the search and get results
results = searchable.get_results()

# Specify entity type
results = searchable.get_results(entity_type="OBJECTS")  # For object detection results
```

#### `count(entity_type="IMAGES")`
Get the count of results without constructing a DataFrame (more efficient).

```python
# Get count of results
count = searchable.count()
print(f"Found {count} matching images")

# Both methods share the same cache, so calling count() after get_results() is instant
```

### Resetting and Managing Queries

#### `reset()`
Clear all search criteria and return to the original dataset.

```python
# Reset to original dataset
searchable.reset()

# Now get_results() will return all images in the dataset
all_images = searchable.get_results()
```

#### `get_query()`
Get the current VQL query structure.

```python
# View current query
current_query = searchable.get_query()
print(f"Current query: {current_query}")
```

### Advanced Search Patterns

#### Combining Multiple Searchable Objects

```python
# Create separate searchable objects
label_search = dataset.search().search_by_labels(["cat"])
issue_search = dataset.search().search_by_issues([IssueType.BLUR])

# Chain them together
combined_search = label_search.chain_filters(issue_search)
results = combined_search.get_results()
```

#### Conditional Search Building

```python
searchable = dataset.search()

# Build search conditionally
if include_cats:
    searchable = searchable.search_by_labels(["cat"])

if exclude_blur:
    searchable = searchable.search_by_issues([IssueType.BLUR])

if search_text:
    searchable = searchable.search_by_semantic(search_text)

# Execute final search
results = searchable.get_results()
```

### Performance Tips

1. **Use count() for quick checks**: If you only need the number of results, use `count()` instead of `get_results()`
2. **Cache results**: Both `count()` and `get_results()` share the same cache, so subsequent calls are instant
3. **Chain efficiently**: Build your search query step by step, then execute once at the end
4. **Reset when needed**: Use `reset()` to clear previous search criteria when starting a new search

### Complete Search Example

```python
from visual_layer_sdk.dataset import IssueType, SearchOperator, SemanticRelevance

# Initialize search
searchable = dataset.search()

# Build complex search query
searchable = searchable.search_by_labels(["cat", "dog"], SearchOperator.IS_ONE_OF)\
                      .search_by_issues([IssueType.BLUR, IssueType.DARK], confidence_min=0.7)\
                      .search_by_captions(["outdoors", "park"])\
                      .search_by_semantic("pets playing outside", SemanticRelevance.MEDIUM_RELEVANCE)

# Get results
results = searchable.get_results()
print(f"Found {len(results)} images matching all criteria")

# Display sample results
for idx, row in results.head(3).iterrows():
    print(f"Image {idx}: {row.get('image_labels', 'N/A')} - {row.get('captions', 'N/A')}")

# Get count for verification
count = searchable.count()
print(f"Count verification: {count}")

# Reset for new search
searchable.reset()
new_results = searchable.search_by_labels(["bird"]).get_results()
print(f"New search found {len(new_results)} bird images")
```

## Error Handling

The SDK provides comprehensive error handling:

```python
from visual_layer_sdk import VisualLayerException

try:
    dataset = client.get_dataset_object("invalid_id")
    stats = dataset.get_stats()
except VisualLayerException as e:
    print(f"API Error: {e}")
except requests.exceptions.RequestException as e:
    print(f"Network Error: {e}")
except ValueError as e:
    print(f"Validation Error: {e}")
```

## Logging Configuration

The SDK provides comprehensive logging capabilities with multiple configuration options.

### Basic Log Level Setting

```python
from visual_layer_sdk.logger import set_log_level, set_verbose
import logging

# Set specific log level
set_log_level(logging.DEBUG)    # Most verbose
set_log_level(logging.INFO)     # Default level
set_log_level(logging.WARNING)  # Only warnings and errors
set_log_level(logging.ERROR)    # Only errors

# Quick verbose mode toggle
set_verbose(True)   # Sets to DEBUG level
set_verbose(False)  # Sets to INFO level
```

### Logging Destinations

```python
from visual_layer_sdk.logger import configure_logging, log_to_console_only, log_to_file_only, log_to_console_and_file

# Console only (default)
log_to_console_only()

# File only
log_to_file_only()  # Uses default log directory
log_to_file_only("/path/to/custom.log")  # Custom log file

# Both console and file
log_to_console_and_file()  # Uses default log directory
log_to_console_and_file("/path/to/custom.log")  # Custom log file

# Advanced configuration
configure_logging(
    output_destinations=["stdout", "file"],
    log_file="/path/to/custom.log",
    level=logging.DEBUG,
    log_dir="/custom/log/directory"
)
```

### Log File Management

```python
from visual_layer_sdk.logger import get_log_file_path, get_default_log_directory, list_log_files, show_log_directory_info

# Get current log file path
current_log = get_log_file_path()
print(f"Current log file: {current_log}")

# Get default log directory
log_dir = get_default_log_directory()
print(f"Default log directory: {log_dir}")

# List all log files
log_files = list_log_files()
for log_file in log_files:
    print(f"Log file: {log_file}")

# Show log directory information
show_log_directory_info()
```

### Log Levels Explained

- **DEBUG**: Most verbose - shows all API requests, responses, and internal operations
- **INFO**: Default level - shows important operations like dataset creation, exports, searches
- **WARNING**: Shows warnings and errors only
- **ERROR**: Shows only errors

### Example: Debug Mode for Troubleshooting

```python
from visual_layer_sdk.logger import set_verbose, log_to_console_and_file

# Enable debug logging to both console and file
set_verbose(True)
log_to_console_and_file("debug_session.log")

# Now all SDK operations will show detailed debug information
client = VisualLayerClient(api_key, api_secret)
dataset = client.get_dataset_object("your_dataset_id")
df = dataset.search_by_labels_to_dataframe(["cat", "dog"])
```

### Default Log Locations

- **Windows**: `%APPDATA%/VisualLayer/logs/`
- **macOS/Linux**: `~/.local/share/visual-layer/logs/`

Log files are named with timestamps: `visual_layer_sdk_YYYY-MM-DD.log`

## Requirements

- Python 3.8+
- requests
- python-dotenv
- PyJWT
- pandas

## Development

### Running Tests
```bash
pytest tests/ --cov=src/visual_layer_sdk
```

### Code Formatting
```bash
black src/ tests/
ruff check --fix src/ tests/
```

### Installing in Development Mode
```bash
pip install -e ".[dev]"
```

## License

MIT License - see LICENSE file for details.

## Support

For support and questions, please refer to the Visual Layer documentation or contact the development team. 