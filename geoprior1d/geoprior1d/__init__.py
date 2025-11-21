"""
geoprior1d: 1D Geological Prior Generator

A Python package for generating stochastic realizations of subsurface
lithology and resistivity models based on geological constraints.
"""

__version__ = "0.9.0"

# Import main API functions
from .core import geoprior1d, generate_prior_realizations, save_prior_to_hdf5
from .io import extract_prior_info
from .sampling import get_prior_sample
from .colormaps import flj_log

# Define public API
__all__ = [
    "geoprior1d",
    "generate_prior_realizations",
    "save_prior_to_hdf5",
    "extract_prior_info",
    "get_prior_sample",
    "flj_log",
]
