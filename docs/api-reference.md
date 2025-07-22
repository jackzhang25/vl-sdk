# API Reference

Complete reference for all Visual Layer SDK classes and methods.

## VisualLayerClient

The main client class for interacting with the Visual Layer API.

### Constructor

```python
VisualLayerClient(api_key: str, api_secret: str)
```

**Parameters:**
- `api_key` (str): Your Visual Layer API key
- `api_secret` (str): Your Visual Layer API secret

**Example:**
```python
client = VisualLayerClient(api_key="your_key", api_secret="your_secret")
```

---

### Health & Connection Methods

#### `healthcheck() -> dict`

Check the health status of the Visual Layer API.

**Returns:**
- `dict`: Health status response

**Example:**
```python
health = client.healthcheck()
print(health)  # {'status': 'healthy'}
```

---

### Dataset Listing Methods

#### `get_sample_datasets() -> list`

Get sample datasets available for testing and exploration.

**Returns:**
- `list`: List of sample dataset dictionaries

**Example:**
```python
samples = client.get_sample_datasets()
for sample in samples:
    print(f"Sample: {sample['display_name']}")
```

#### `get_all_datasets() -> pd.DataFrame`

Get all datasets accessible to your account as a pandas DataFrame.

**Returns:**
- `pd.DataFrame`: DataFrame with dataset information including:
  - `id`: Dataset unique identifier
  - `created_by`: Creator user ID  
  - `source_dataset_id`: Source dataset reference
  - `owned_by`: Owner user ID
  - `display_name`: Human-readable dataset name
  - `description`: Dataset description
  - `preview_uri`: Preview image URL
  - `source_type`: Type of data source
  - `source_uri`: Source location URI
  - `created_at`: Creation timestamp
  - `updated_at`: Last update timestamp
  - `filename`: Original filename
  - `sample`: Whether this is a sample dataset
  - `status`: Processing status
  - `n_images`: Number of images in dataset

**Example:**
```python
datasets_df = client.get_all_datasets()
print(f"Found {len(datasets_df)} datasets")
print(datasets_df[['display_name', 'status', 'n_images']].head())
```

#### `get_dataset(dataset_id: str) -> pd.DataFrame`

Get dataset details as a pandas DataFrame for a specific dataset ID.

**Parameters:**
- `dataset_id` (str): The unique identifier of the dataset

**Returns:**
- `pd.DataFrame`: Single-row DataFrame with dataset details

**Example:**
```python
dataset_df = client.get_dataset("dataset-123")
print(dataset_df.iloc[0]['display_name'])
```

#### `get_dataset_object(dataset_id: str) -> Dataset`

Get a Dataset object for advanced operations like search, export, and deletion.

**Parameters:**
- `dataset_id` (str): The unique identifier of the dataset

**Returns:**
- `Dataset`: Dataset object for performing operations

**Example:**
```python
dataset = client.get_dataset_object("dataset-123")
stats = dataset.get_stats()
```

---

### Dataset Creation Methods

#### `create_dataset_from_s3_bucket(s3_bucket_path: str, dataset_name: str, pipeline_type: str = None) -> Dataset`

Create a dataset from files stored in an S3 bucket.

**Parameters:**
- `s3_bucket_path` (str): S3 bucket path (without `s3://` prefix)
- `dataset_name` (str): Name for the new dataset
- `pipeline_type` (str, optional): Processing pipeline type

**Returns:**
- `Dataset`: Dataset object for the created dataset

**Raises:**
- `ValueError`: If required parameters are missing
- `requests.exceptions.RequestException`: If the API request fails

**Example:**
```python
dataset = client.create_dataset_from_s3_bucket(
    s3_bucket_path="my-bucket/images/",
    dataset_name="My S3 Dataset",
    pipeline_type="image_processing"
)
print(f"Created dataset ID: {dataset.dataset_id}")
```

#### `create_dataset_from_local_folder(file_path: str, filename: str, dataset_name: str, pipeline_type: str = None) -> Dataset`

Create a dataset from a local zip file.

**Parameters:**
- `file_path` (str): Full path to the zip file
- `filename` (str): Name of the zip file
- `dataset_name` (str): Name for the new dataset  
- `pipeline_type` (str, optional): Processing pipeline type

**Returns:**
- `Dataset`: Dataset object for the created dataset

**Raises:**
- `ValueError`: If file doesn't exist or parameters are invalid
- `requests.exceptions.RequestException`: If the API request fails

**Example:**
```python
dataset = client.create_dataset_from_local_folder(
    file_path="/path/to/images.zip",
    filename="images.zip",
    dataset_name="Local Dataset",
    pipeline_type="image_processing"
)
print(f"Created dataset ID: {dataset.dataset_id}")
```

---

## Dataset

The Dataset class provides methods for working with individual datasets.

### Constructor

```python
Dataset(client: VisualLayerClient, dataset_id: str)
```

**Parameters:**
- `client`: VisualLayerClient instance
- `dataset_id` (str): The unique identifier of the dataset

**Note:** Usually created via `client.get_dataset_object()` rather than directly.

---

### Dataset Information Methods

#### `get_details() -> dict`

Get detailed information about the dataset.

**Returns:**
- `dict`: Dataset details with filtered fields including:
  - `id`, `created_by`, `owned_by`, `display_name`, `description`
  - `preview_uri`, `source_type`, `source_uri` 
  - `created_at`, `updated_at`, `filename`, `sample`, `status`

**Example:**
```python
details = dataset.get_details()
print(f"Dataset: {details['display_name']}")
print(f"Status: {details['status']}")
```

#### `get_stats() -> dict`

Get comprehensive statistics for the dataset.

**Returns:**
- `dict`: Dataset statistics and metrics

**Example:**
```python
stats = dataset.get_stats()
print(f"Dataset statistics: {stats}")
```

#### `get_status() -> str`

Get the current processing status of the dataset.

**Returns:**
- `str`: Dataset status (e.g., "READY", "PROCESSING", "ERROR")

**Example:**
```python
status = dataset.get_status()
if status == "READY":
    print("Dataset is ready for operations")
else:
    print(f"Dataset status: {status}")
```

#### `get_image_info(image_id: str) -> dict`

Get detailed information about a specific image in the dataset.

**Parameters:**
- `image_id` (str): The unique identifier of the image

**Returns:**
- `dict`: Image information including URI and metadata

**Example:**
```python
image_info = dataset.get_image_info("image-123")
image_url = image_info['image_uri']
```

---

### Dataset Exploration Methods

#### `explore() -> pd.DataFrame`

Explore the dataset and return previews as a DataFrame.

**Returns:**
- `pd.DataFrame`: DataFrame containing preview items from the first cluster

**Example:**
```python
previews_df = dataset.explore()
print(f"Found {len(previews_df)} preview items")
print(previews_df.columns.tolist())
```

---

### Search Methods

#### `search_by_labels(labels: List[str]) -> pd.DataFrame`

Search dataset by labels and return matching images as a DataFrame.

**Parameters:**
- `labels` (List[str]): List of labels to search for (e.g., ["cat", "dog"])

**Returns:**
- `pd.DataFrame`: DataFrame containing all images from matching clusters

**Example:**
```python
results_df = dataset.search_by_labels(["angular_leaf_spot", "bean_rust"])
print(f"Found {len(results_df)} images with specified labels")
```

#### `search_by_captions(caption_text: str, similarity_threshold: float = 0.83) -> pd.DataFrame`

Search dataset by AI-generated captions using semantic similarity.

**Parameters:**
- `caption_text` (str): Text to search for in captions
- `similarity_threshold` (float): Threshold for semantic search (default: 0.83)

**Returns:**
- `pd.DataFrame`: DataFrame containing all images from matching clusters

**Example:**
```python
results_df = dataset.search_by_captions("person holding leaf")
print(f"Found {len(results_df)} images matching caption")
```

#### `search_by_labels_async(labels: List[str]) -> dict`

Start an asynchronous search by labels and return the export task status.

**Parameters:**
- `labels` (List[str]): List of labels to search for

**Returns:**
- `dict`: Export status response with task ID and progress information

**Example:**
```python
status = dataset.search_by_labels_async(["cat", "dog"])
task_id = status.get("id")
download_uri = status.get("download_uri")
```

#### `search_by_labels_async_to_dataframe(labels: List[str], poll_interval: int = 10, timeout: int = 300) -> pd.DataFrame`

Search dataset by labels asynchronously, poll until ready, and return results as DataFrame.

**Parameters:**
- `labels` (List[str]): List of labels to search for
- `poll_interval` (int): Seconds between status polls (default: 10)
- `timeout` (int): Maximum seconds to wait (default: 300)

**Returns:**
- `pd.DataFrame`: DataFrame with search results, or empty if timeout/error

**Example:**
```python
results_df = dataset.search_by_labels_async_to_dataframe(
    labels=["bean_rust", "angular_leaf_spot"],
    poll_interval=5,
    timeout=600
)
print(f"Async search found {len(results_df)} images")
```

#### `search_by_captions_async(caption_text: str, similarity_threshold: float = 0.83) -> dict`

Start an asynchronous search by captions using the export_context_async endpoint.

**Parameters:**
- `caption_text` (str): Text to search for in captions  
- `similarity_threshold` (float): Threshold for semantic search (default: 0.83)

**Returns:**
- `dict`: Export task response with task ID for polling

**Example:**
```python
task_response = dataset.search_by_captions_async("blue nail")
task_id = task_response.get("id")
```

---

### Export Methods

#### `export() -> dict`

Export the dataset in JSON format.

**Returns:**
- `dict`: Complete dataset export data

**Raises:**
- `RuntimeError`: If dataset is not ready for export

**Example:**
```python
if dataset.get_status() in ["READY", "completed"]:
    export_data = dataset.export()
    media_items = export_data["media_items"]
else:
    print("Dataset not ready for export")
```

#### `export_to_dataframe() -> pd.DataFrame`

Export the dataset and convert media items to a pandas DataFrame.

**Returns:**
- `pd.DataFrame`: DataFrame containing media items (metadata_items excluded)

**Example:**
```python
media_df = dataset.export_to_dataframe()
print(f"Exported {len(media_df)} media items")
print(media_df.columns.tolist())

# Save to CSV
media_df.to_csv("dataset_export.csv", index=False)
```

---

### Utility Methods

#### `download_export_results(download_uri: str) -> dict`

Download export results from a provided URI. Handles both ZIP and JSON responses.

**Parameters:**
- `download_uri` (str): The download URI from an export status response

**Returns:**
- `dict`: Downloaded and parsed export data

**Example:**
```python
# Usually used internally, but can be called directly
export_data = dataset.download_export_results(download_uri)
media_items = export_data.get("media_items", [])
```

#### `process_export_download_to_dataframe(download_uri: str) -> pd.DataFrame`

Download export results and flatten to a DataFrame with processed metadata.

**Parameters:**
- `download_uri` (str): The download URI from export status

**Returns:**
- `pd.DataFrame`: Processed DataFrame with flattened metadata columns:
  - `captions`: AI-generated captions (semicolon-separated)
  - `image_labels`: Image classification labels with source
  - `object_labels`: Object detection labels with bounding boxes  
  - `issues`: Detected quality issues with confidence scores

**Example:**
```python
results_df = dataset.process_export_download_to_dataframe(download_uri)
print(results_df[['captions', 'image_labels', 'issues']].head())
```

#### `delete() -> dict`

Permanently delete the dataset.

**Returns:**
- `dict`: Deletion confirmation response

**Warning:** This operation is irreversible.

**Example:**
```python
# Be very careful with this operation!
result = dataset.delete()
print(f"Dataset deleted: {result}")
```

---

## Error Handling

The SDK raises standard Python exceptions for different error conditions:

### Common Exceptions

#### `ValueError`
Raised for invalid input parameters:
```python
try:
    client.create_dataset_from_s3_bucket("", "")  # Empty parameters
except ValueError as e:
    print(f"Invalid parameters: {e}")
```

#### `requests.exceptions.RequestException`
Raised for API request failures:
```python
try:
    datasets = client.get_all_datasets()
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
```

#### `requests.exceptions.HTTPError`
Raised for HTTP status errors (4xx, 5xx):
```python
try:
    dataset = client.get_dataset_object("invalid-id")
    details = dataset.get_details()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 404:
        print("Dataset not found")
    elif e.response.status_code == 401:
        print("Authentication failed")
```

#### `RuntimeError`
Raised for operation-specific errors:
```python
try:
    export_data = dataset.export()
except RuntimeError as e:
    print(f"Export failed: {e}")
    # Usually means dataset is not ready
```

---

## Type Hints

The SDK uses Python type hints for better development experience:

```python
from typing import List, Dict, Optional
import pandas as pd

# Method signatures include type hints
def search_by_labels(self, labels: List[str]) -> pd.DataFrame:
    pass

def create_dataset_from_s3_bucket(
    self, 
    s3_bucket_path: str, 
    dataset_name: str, 
    pipeline_type: Optional[str] = None
) -> 'Dataset':
    pass
```

This enables better IDE support, code completion, and static type checking with tools like `mypy`.