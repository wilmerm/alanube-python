# Contributing Guide

Thank you for your interest in contributing to the Alanube Python API! This guide will help you get started with contributing to the project.

## Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)
- [Pull Request Process](#pull-request-process)
- [Issue Reporting](#issue-reporting)
- [Code of Conduct](#code-of-conduct)

## Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- pip
- Virtual environment (recommended)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone https://github.com/your-username/alanube-python-api.git
   cd alanube-python-api
   ```

3. Add the upstream repository:
   ```bash
   git remote add upstream https://github.com/wilmerm/alanube-python-api.git
   ```

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install the package in editable mode
pip install -e .
```

### 3. Verify Installation

```bash
python -c "from alanube.do import Alanube; print('Setup successful!')"
```

## Code Style

We follow PEP 8 style guidelines and use several tools to maintain code quality.

### Code Formatting

We use `black` for code formatting:

```bash
# Format all Python files
black alanube/

# Check formatting without making changes
black --check alanube/
```

### Linting

We use `flake8` for linting:

```bash
# Run flake8
flake8 alanube/

# Run with specific configuration
flake8 alanube/ --max-line-length=88 --extend-ignore=E203,W503
```

### Type Checking

We use `mypy` for type checking:

```bash
# Run type checking
mypy alanube/
```

### Import Sorting

We use `isort` for import sorting:

```bash
# Sort imports
isort alanube/

# Check import sorting
isort --check-only alanube/
```

### Pre-commit Hooks

Install pre-commit hooks to automatically run these checks:

```bash
# Install pre-commit
pip install pre-commit

# Install the git hook scripts
pre-commit install

# Run against all files
pre-commit run --all-files
```

## Testing

### Running Tests

```bash
# Run all tests
python -m unittest discover -s alanube/tests -p "*.py"

# Run specific test file
python -m unittest alanube.tests.test_api

# Run specific test method
python -m unittest alanube.tests.test_api.TestAlanubeAPI.test_send_fiscal_invoice

# Run with verbose output
python -m unittest discover -s alanube/tests -p "*.py" -v
```

### Test Coverage

```bash
# Install coverage
pip install coverage

# Run tests with coverage
coverage run -m unittest discover -s alanube/tests -p "*.py"

# Generate coverage report
coverage report

# Generate HTML coverage report
coverage html
```

### Writing Tests

When writing tests, follow these guidelines:

1. **Test Structure**
   ```python
   import unittest
   from unittest.mock import patch, MagicMock
   from alanube.do import Alanube
   from alanube.do.exceptions import AlanubeException
   
   class TestAlanubeAPI(unittest.TestCase):
       def setUp(self):
           """Set up test fixtures."""
           self.api_token = "test_token"
           Alanube.connect(self.api_token, developer_mode=True)
       
       def tearDown(self):
           """Clean up after tests."""
           pass
       
       def test_send_fiscal_invoice_success(self):
           """Test successful fiscal invoice sending."""
           # Test implementation
           pass
       
       def test_send_fiscal_invoice_invalid_payload(self):
           """Test fiscal invoice with invalid payload."""
           # Test implementation
           pass
   ```

2. **Mocking External Dependencies**
   ```python
   @patch('alanube.do.api.requests.post')
   def test_api_call(self, mock_post):
       # Mock the response
       mock_response = MagicMock()
       mock_response.status_code = 200
       mock_response.json.return_value = {"id": "test_id"}
       mock_post.return_value = mock_response
       
       # Test the method
       result = Alanube.send_document(encf_type=31, payload={})
       
       # Assertions
       self.assertEqual(result["id"], "test_id")
       mock_post.assert_called_once()
   ```

3. **Test Naming**
   - Use descriptive test method names
   - Follow the pattern: `test_method_name_scenario`
   - Include docstrings explaining what the test does

4. **Test Coverage**
   - Test both success and failure scenarios
   - Test edge cases and boundary conditions
   - Test error handling and exceptions
   - Aim for at least 80% code coverage

## Documentation

### Code Documentation

All public methods should have docstrings following Google style:

```python
def send_document(self, encf_type: int, payload: dict) -> dict:
    """Send an electronic document of the specified type.
    
    Args:
        encf_type (int): The type of the eNCF document.
        payload (dict): The data required to send the document.
        
    Returns:
        dict: The response from the Alanube API containing document information.
        
    Raises:
        ValidationError: If the payload is invalid.
        AuthenticationError: If authentication fails.
        AlanubeException: For other API errors.
        
    Example:
        >>> payload = {"company_id": "123", "customer": {...}}
        >>> response = Alanube.send_document(31, payload)
        >>> print(response["document_number"])
        'B0100000001'
    """
    pass
```

### Documentation Updates

When adding new features or changing existing ones:

1. **Update docstrings** for all modified methods
2. **Update README.md** if adding new features
3. **Update API reference** in `docs/api-reference.md`
4. **Add usage examples** in `docs/usage.md`
5. **Update installation guide** if needed

### Building Documentation

```bash
# Install documentation dependencies
pip install mkdocs mkdocs-material

# Build documentation
mkdocs build

# Serve documentation locally
mkdocs serve
```

## Pull Request Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Your Changes

```bash
# Add your changes
git add .

# Commit with a descriptive message
git commit -m "feat: add support for new document type

- Add new document type 48 for special invoices
- Implement validation for new type
- Add tests for new functionality
- Update documentation with new type"
```

### 4. Push to Your Fork

```bash
git push origin feature/your-feature-name
```

### 5. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the pull request template
5. Submit the pull request

### Pull Request Template

```markdown
## Description
Brief description of the changes made.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## Testing
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Manual testing completed

## Checklist
- [ ] Code follows the style guidelines
- [ ] Self-review of code completed
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added and passing

## Related Issues
Closes #(issue number)
```

## Issue Reporting

### Before Reporting an Issue

1. Check if the issue has already been reported
2. Try to reproduce the issue with the latest version
3. Check the documentation for solutions
4. Search existing issues and pull requests

### Issue Template

```markdown
## Bug Report

### Environment
- Python version: 3.10.0
- Alanube version: 1.0.0
- Operating system: Windows 10
- Country: Dominican Republic

### Description
Clear and concise description of the bug.

### Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

### Expected Behavior
What you expected to happen.

### Actual Behavior
What actually happened.

### Error Messages
```
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  ...
```

### Additional Context
Add any other context about the problem here.
```

## Code of Conduct

### Our Standards

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- The use of sexualized language or imagery
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate

### Enforcement

Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project team. All complaints will be reviewed and investigated and will result in a response that is deemed necessary and appropriate to the circumstances.

## Getting Help

If you need help with contributing:

1. **Check the documentation** - Start with the README and API reference
2. **Search existing issues** - Your question might already be answered
3. **Create a new issue** - Use the appropriate template
4. **Join discussions** - Participate in existing discussions

## Recognition

Contributors will be recognized in:

- The project README
- Release notes
- Contributor hall of fame
- GitHub contributors page

Thank you for contributing to the Alanube Python API! 🚀 