# Logging

The Visual Layer SDK includes a comprehensive logging system that provides natural, user-friendly output messages for all operations.

## Features

- 📝 **Natural Language Messages**: Human-readable output with emojis and clear descriptions
- 📊 **Multiple Log Levels**: INFO, DEBUG, WARNING, ERROR, and SUCCESS levels
- 🔧 **Specialized Methods**: Dedicated logging methods for common operations
- ⚙️ **Configurable Verbosity**: Easy to enable/disable detailed logging
- 📤 **Multiple Output Destinations**: Console, file, stderr, or combinations
- 🎯 **Consistent Formatting**: Uniform message format across all SDK operations

## Quick Start

```python
from visual_layer_sdk import VisualLayerClient
from visual_layer_sdk.logger import set_verbose

# Initialize client (logger is automatically created)
client = VisualLayerClient(api_key="your_key", api_secret="your_secret")

# Enable verbose logging for debugging
set_verbose(True)

# All SDK operations will now show detailed logs
datasets = client.get_all_datasets()
```

## Output Destinations

By default, all logging output goes to **stdout** (console/terminal). You can configure different destinations:

### Console Only (Default)
```python
from visual_layer_sdk.logger import log_to_console_only

log_to_console_only()
```

### File Only
```python
from visual_layer_sdk.logger import log_to_file_only

log_to_file_only("my_app.log")
```

### Console and File
```python
from visual_layer_sdk.logger import log_to_console_and_file

log_to_console_and_file("my_app.log")
```

### Error Stream
```python
from visual_layer_sdk.logger import log_to_stderr

log_to_stderr()
```

## Log Levels

### Basic Logging
```python
from visual_layer_sdk.logger import get_logger

logger = get_logger()

# Info messages (default)
logger.info("Starting dataset creation...")

# Success messages (with ✅ emoji)
logger.success("Dataset created successfully!")

# Warning messages (with ⚠️ emoji)
logger.warning("Dataset is not ready for export")

# Error messages (with ❌ emoji)
logger.error("Failed to connect to API")

# Debug messages (only shown in verbose mode)
logger.debug("Making API request to /dataset/123")
```