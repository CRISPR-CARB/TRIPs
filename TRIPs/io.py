"""
Input/Output operations for TRIPs analysis.

This module centralizes all file reading and writing operations, including:
- Loading count matrices and AnnData objects
- Reading gene annotation files
- Saving analysis results and processed data
- Managing output directory structure

All I/O functions include proper error handling and path validation.
"""

import pandas as pd
from anndata import AnnData
import scanpy as sc
from pathlib import Path

# ============================================================================
# Input functions
# ============================================================================

def load_count_matrix(...):
    ...

def load_gene_annotations(...):
    ...


# ============================================================================
# Output functions
# ============================================================================

def save_anndata(...):
    ...