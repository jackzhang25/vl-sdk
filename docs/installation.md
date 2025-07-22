# Installation

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

## Install from Source

Since the package is currently in development, install directly from the source code:

If you want to install from the source code:

1. Clone the repository:
```bash
git clone https://github.com/jackzhang25/vl-package.git
cd vl-package
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package:
```bash
pip install -e .
```

## Development Installation

For development, install with additional development dependencies:

```bash
pip install -e ".[dev]"
```

This includes:
- `black` - Code formatting
- `ruff` - Linting and code analysis
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting

## Dependencies

The SDK has the following core dependencies:

| Package | Version | Purpose |
|---------|---------|---------|
| `requests` | >=2.31.0 | HTTP client for API calls |
| `python-dotenv` | >=1.0.0 | Environment variable management |
| `PyJWT` | >=2.8.0 | JWT token generation and validation |
| `pandas` | >=2.2.0 | Data manipulation and analysis |

## Environment Setup

After installation, create a `.env` file in your project directory with your API credentials:

```bash
# .env
VISUAL_LAYER_API_KEY=your_api_key_here
VISUAL_LAYER_API_SECRET=your_api_secret_here
```

## Verify Installation

Test your installation with a simple script:

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

# Test connection
try:
    health = client.healthcheck()
    print(f"✅ Connection successful: {health}")
except Exception as e:
    print(f"❌ Connection failed: {e}")
```

### System-Specific Instructions

#### Windows
```bash
# Clone repository
git clone https://github.com/jackzhang25/vl-package.git
cd vl-package

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install package
pip install -e .
```

#### macOS/Linux
```bash
# Clone repository
git clone https://github.com/jackzhang25/vl-package.git
cd vl-package

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install package
pip install -e .
```

#### Using conda
```bash
# Clone repository
git clone https://github.com/jackzhang25/vl-package.git
cd vl-package

# Create environment
conda create -n visual-layer python=3.9
conda activate visual-layer

# Install package
pip install -e .
```

## Next Steps

Once installed, check out the [Getting Started](getting-started) guide to begin using the SDK.