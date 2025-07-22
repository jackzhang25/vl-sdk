# Getting Started

This guide will help you get up and running with the Visual Layer SDK quickly.

## Authentication

The Visual Layer SDK uses JWT-based authentication. You'll need API credentials from your Visual Layer account.

### Getting API Credentials

1. Log in to your Visual Layer account
2. Navigate to Settings → API Keys  
3. Generate a new API key pair
4. Save your `API_KEY` and `API_SECRET` securely

### Setting Up Environment Variables

Create a `.env` file in your project directory:

```bash
VISUAL_LAYER_API_KEY=your_api_key_here
VISUAL_LAYER_API_SECRET=your_api_secret_here
```

### Client Initialization

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
```

## Your First API Call

Test your connection with a health check:

```python
# Check API health
health = client.healthcheck()
print(f"API Status: {health}")
# Output: API Status: {'status': 'healthy'}
```

## Basic Operations

### 1. List All Datasets

```python
# Get all datasets as a DataFrame
datasets_df = client.get_all_datasets()
print(f"Found {len(datasets_df)} datasets")
print(datasets_df.head())
```

### 2. Get Dataset Details

```python
# Get a specific dataset
if len(datasets_df) > 0:
    dataset_id = datasets_df.iloc[0]['id']
    dataset = client.get_dataset_object(dataset_id)
    
    # Get dataset details
    details = dataset.get_details()
    print(details)
```

### 3. Explore Dataset Content

```python
# Explore dataset previews
previews_df = dataset.explore()
print(f"Found {len(previews_df)} preview items")
print(previews_df.columns.tolist())
```

### 4. Export Dataset

```python
# Export full dataset to DataFrame
if dataset.get_status() in ["READY", "completed"]:
    media_df = dataset.export_to_dataframe()
    print(f"Exported {len(media_df)} media items")
    
    # Save to CSV
    media_df.to_csv("exported_dataset.csv", index=False)
    print("Dataset saved to exported_dataset.csv")
else:
    print(f"Dataset not ready for export. Current status: {dataset.get_status()}")
```

## Working with Sample Datasets

Use sample datasets to test functionality:

```python
# Get sample datasets
sample_datasets = client.get_sample_datasets()
print(f"Available sample datasets: {len(sample_datasets)}")

for sample in sample_datasets:
    print(f"- {sample['display_name']} (ID: {sample['id']})")
```

## Creating Your First Dataset

### From S3 Bucket

```python
# Create dataset from S3 bucket
dataset = client.create_dataset_from_s3_bucket(
    s3_bucket_path="my-bucket/images/",  # Don't include s3:// prefix
    dataset_name="My Image Dataset",
    pipeline_type="image_processing"  # Optional
)

print(f"✅ Dataset created with ID: {dataset.dataset_id}")
```

### From Local Files

```python
# Create dataset from local zip file
dataset = client.create_dataset_from_local_folder(
    file_path="/path/to/images.zip",
    filename="images.zip",
    dataset_name="Local Image Dataset",
    pipeline_type="image_processing"  # Optional
)

print(f"✅ Dataset created with ID: {dataset.dataset_id}")
```

## Logging and Debugging

Enable verbose logging to see detailed API interactions:

```python
from visual_layer_sdk.logger import set_verbose

# Enable verbose logging
set_verbose(True)

# Now all API calls will show detailed information
client.get_all_datasets()
```
## Next Steps

Now that you have the basics down, explore these advanced features:

- {doc}`Search & Filtering <search-filtering>` - Advanced dataset search capabilities
- {doc}`API Reference <api-reference>` - Complete method documentation
- {doc}`Logging <logging>` - Configure logging for your needs