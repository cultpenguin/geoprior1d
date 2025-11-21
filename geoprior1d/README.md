# geoprior1d

1D geological prior generator for stochastic lithology and resistivity modeling.

## Installation

### From PyPI
```bash
pip install geoprior1d
```

### From source
```bash
cd geoprior1d

# Basic installation
pip install .

# Development installation (editable mode)
pip install -e .
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

See [CLAUDE.md](CLAUDE.md) for detailed format specification and code architecture.

## Requirements

- Python >= 3.8
- numpy >= 1.20.0
- h5py >= 3.0.0
- matplotlib >= 3.3.0
- pandas >= 1.2.0
- scipy >= 1.6.0
- tqdm >= 4.60.0

All dependencies are automatically installed via pip.

## License

MIT License
