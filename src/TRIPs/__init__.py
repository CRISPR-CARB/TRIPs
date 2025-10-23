"""
TRIPs - Transcription-Replication Interaction Profiles

A package for analyzing bacterial single-cell RNA-seq data to understand
transcription-replication interactions during the cell cycle.
"""

__version__ = "0.1.0"

# Import main modules to make them accessible
from . import preprocessing
from . import io

# Optionally expose commonly used functions at package level
from .preprocessing import remove_rRNA, filter_samples_by_bc1
from .io import load_count_matrix

__all__ = [
    "preprocessing",
    "io",
    "remove_rRNA",
    "filter_samples_by_bc1",
    "load_count_matrix",
]