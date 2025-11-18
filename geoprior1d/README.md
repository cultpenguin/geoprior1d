# geoprior1d

1D geological prior generator for stochastic lithology and resistivity modeling.

## Installation

### From source
```bash
cd geoprior1d
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
    n_realizations=10000,
    depth_max=90,
    depth_step=1,
    plot=True
)

print(f"Output saved to: {filename}")
```

## Input File Format

See [MODULE_CONVERSION_PLAN.md](MODULE_CONVERSION_PLAN.md) for detailed format specification.

## License

MIT License
