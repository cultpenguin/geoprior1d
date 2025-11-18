# geoprior1d

1D geological prior generator for stochastic lithology and resistivity modeling.

## Installation

### From source
```bash
cd geoprior1d

# Basic installation
pip install .

# Development installation (editable mode)
pip install -e .

# With development tools
pip install -e ".[dev]"
```

### From PyPI (after publishing)
```bash
pip install geoprior1d
```

## Quick Start

### Command Line

```bash
geoprior1d input.xlsx -n 10000 -d 90 --plot
```

### Python API

```python
from geoprior1d import generate_prior

# Generate priors
filename, flags = generate_prior(
    input_data="daugaard_matlab.xlsx",
    Nreals=10000,
    dmax=90,
    dz=1,
    doPlot=1
)

print(f"Output saved to: {filename}")
```

## Input File Format

See [CLAUDE.md](CLAUDE.md) for detailed format specification.

## Development

### Install development dependencies
```bash
pip install -e ".[dev]"
# or
pip install -r requirements-dev.txt
```

### Run tests
```bash
pytest
pytest --cov=geoprior1d  # With coverage
```

### Code formatting
```bash
black geoprior1d/
isort geoprior1d/
flake8 geoprior1d/
```

## Project Structure

This project uses modern Python packaging with `pyproject.toml`. See [MODERN_PACKAGING.md](MODERN_PACKAGING.md) for details.

## Documentation

- [CLAUDE.md](CLAUDE.md) - Code architecture and usage
- [MODERN_PACKAGING.md](MODERN_PACKAGING.md) - Packaging guide
- [CONVERSION_SUMMARY.md](CONVERSION_SUMMARY.md) - Conversion details

## License

MIT License
