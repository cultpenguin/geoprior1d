"""
geoprior1d: 1D Geological Prior Generator

A Python package for generating stochastic realizations of subsurface
lithology and resistivity models based on geological constraints.
"""

__version__ = "1.0.0"
__author__ = "Your Name"

# Import main API functions
from .core import prior_generator
from .io import extract_prior_info
from .sampling import get_prior_sample
from .colormaps import flj_log

# Alias for more Pythonic naming
generate_prior = prior_generator

# Define public API
__all__ = [
    "prior_generator",
    "generate_prior",
    "extract_prior_info",
    "get_prior_sample",
    "flj_log",
]
