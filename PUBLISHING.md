# Publishing Guide for Rinse Programming Language

## Prerequisites

1. Install build tools:
```bash
pip install build twine pyinstaller
```

## Building Distributions

### 1. Build PyPI Package

```bash
python setup.py sdist bdist_wheel
```

This creates:
- `dist/rinse-programming-language-0.1.0.tar.gz` (source distribution)  
- `dist/rinse_programming_language-0.1.0-py3-none-any.whl` (wheel)

### 2. Build Standalone Executable

```bash
pyinstaller --onefile --name rinsec-standalone rinsec_standalone.py
```

This creates:
- `dist/rinsec-standalone` (64MB standalone executable)

## Publishing to PyPI

### Test Upload (recommended first)

```bash
# Upload to TestPyPI first
twine upload --repository testpypi dist/*.whl dist/*.tar.gz

# Test installation from TestPyPI
pip install --index-url https://test.pypi.org/simple/ rinse-programming-language
```

### Production Upload

```bash
twine upload dist/*.whl dist/*.tar.gz
```

## Verifying Installation

After publishing, users can install with:

```bash
pip install rinse-programming-language
```

And use with:

```bash
rinsec hello.rn
```

## Package Contents

- **Source**: All Python modules in `rinse/` package
- **Entry Point**: `rinsec` command points to `rinse.rinsec:main`
- **Dependencies**: `llvmlite>=0.37.0`
- **License**: MIT
- **Executable**: Standalone binary for Windows/Linux/macOS

The package is now ready for distribution on PyPI and can be used by installing with pip!