# Installation Guide

This guide will help you install and set up the Alanube Python API client.

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- An Alanube API token

## Installation Methods

### Method 1: Install from PyPI (Recommended)

The easiest way to install the library is using pip:

```bash
pip install alanube
```

### Method 2: Install from Source

If you want to install the latest development version or contribute to the project:

1. Clone the repository:
```bash
git clone https://github.com/wilmerm/alanube-python-api.git
cd alanube-python-api
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Install in editable mode:
```bash
pip install -e .
```

## Verification

To verify the installation, run Python and try importing the library:

```python
from alanube.do import Alanube
print("Alanube library imported successfully!")
```

## Getting Your API Token

1. Visit the [Alanube website](https://www.alanube.co/)
2. Sign up for an account
3. Navigate to your dashboard
4. Generate an API token
5. Keep your token secure and never share it publicly

## Environment Setup

For development, you can use environment variables to store your API token:

1. Create a `.env` file in your project root:
```bash
ALANUBE_TOKEN=your_api_token_here
ALANUBE_DEVELOPER_MODE=true
```

2. Load environment variables in your code:
```python
import os
from dotenv import load_dotenv
from alanube.do import Alanube

load_dotenv()

token = os.getenv('ALANUBE_TOKEN')
developer_mode = os.getenv('ALANUBE_DEVELOPER_MODE', 'false').lower() == 'true'

Alanube.connect(token, developer_mode=developer_mode)
```

## Next Steps

- Read the [Usage Examples](usage.md) to learn how to use the library
- Check the [API Reference](api-reference.md) for detailed method documentation
- Explore [Country Support](countries.md) to see what features are available

## Troubleshooting

### Common Issues

**Import Error: No module named 'alanube'**
- Make sure you've installed the package correctly
- Verify you're using the correct Python environment
- Try reinstalling: `pip install --force-reinstall alanube`

**Authentication Error**
- Verify your API token is correct
- Check if your token has the necessary permissions
- Ensure you're using the correct environment (production vs sandbox)

**Network Issues**
- Check your internet connection
- Verify firewall settings
- Try using a different network if available

For more help, see our [troubleshooting guide](troubleshooting.md) or [open an issue](https://github.com/wilmerm/alanube-python-api/issues) on GitHub. 