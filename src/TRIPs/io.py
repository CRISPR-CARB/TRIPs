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
import os

# ============================================================================
# Input functions
# ============================================================================

def load_count_matrix(counts_dir: str) -> pd.DataFrame:
    """
    Load and concatenate count matrices from multiple library files.

    Reads all count files (ending in '_counts.txt.gz') from the specified
    directory, concatenates them into a single DataFrame, and cleans the
    gene labels by removing chromosome prefixes.

    Parameters
    ----------
    counts_dir : str
        Path to directory containing count matrix files.
        Files must be named with pattern '*_counts.txt.gz'.

    Returns
    -------
    pd.DataFrame
        Concatenated count matrix with cells as rows and genes as columns.
        Missing gene counts across libraries are filled with zeros.
        Gene names have chromosome prefixes (e.g., 'NC_.*:') removed.

    Raises
    ------
    FileNotFoundError
        If the specified directory does not exist.
    ValueError
        If no count files matching the pattern are found in the directory.

    Notes
    -----
    - Files are expected to be tab-separated with gene names as columns
    - If different libraries have different genes, missing values are filled with 0
    - Chromosome naming pattern 'NC_.*:' is removed from all gene labels

    Examples
    --------
    >>> counts = load_count_matrix('count_matrices/Ecoli_D1/')
    >>> counts.shape
    (5000, 4321)  # 5000 cells, 4321 genes
    """
    # Convert to Path object and validate
    counts_path = Path(counts_dir)

    if not counts_path.exists():
        raise FileNotFoundError(f"Directory not found: {counts_dir}")

    if not counts_path.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {counts_dir}")

    # Find all count files
    file_paths = list(counts_path.glob('*_counts.txt.gz'))

    if not file_paths:
        raise ValueError(
            f"No count files (*_counts.txt.gz) found in directory: {counts_dir}"
        )

    # Log the files being loaded (useful for debugging)
    print(f"Loading {len(file_paths)} count file(s) from {counts_dir}")

    # Import counts as individual libraries that are then concatenated together
    # (if there are mismatches between libraries in terms of genes, these are filled in with zeros)
    count_dfs = []
    for file_path in file_paths:
        try:
            df = pd.read_table(file_path, sep="\t", index_col=0)
            count_dfs.append(df)
        except Exception as e:
            raise ValueError(f"Error reading file {file_path}: {e}")

    counts_df = pd.concat(count_dfs, axis=0).fillna(0)

    # Remove chromosome names from gene labels
    counts_df.columns = counts_df.columns.str.replace("^NC_.*:", "", regex=True)

    return counts_df


def load_gene_annotations(...):
    ...


# ============================================================================
# Output functions
# ============================================================================

def save_anndata(...):
    ...