"""
Preprocessing for TRIPs analysis.

This module contains functions for initial data preprocessing including:
- Removing rRNA features
- Filtering samples by barcode indices
"""

import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def remove_rRNA(counts_df: pd.DataFrame, ref_rna: str) -> pd.DataFrame:
    """
    Remove all rRNA features from count matrix.

    Parameters
    ----------
    counts_df : pd.DataFrame
        Count matrix with cells as rows and genes as columns.
    ref_rna : str
        Path to rRNA reference text file (one gene per line).

    Returns
    -------
    pd.DataFrame
        Count matrix with rRNA features removed.

    Raises
    ------
    FileNotFoundError
        If rRNA file does not exist.
    ValueError
        If no rRNA genes are found in the reference file.
    """
    # Convert to Path object and validate
    ref_path = Path(ref_rna)

    if not ref_path.is_file():
        raise FileNotFoundError(f"rRNA reference file not found: {ref_rna}")

    # Read rRNA gene names from file
    with open(ref_path, 'r') as f:
        rRNA_genes = [line.strip() for line in f if line.strip()]

    if not rRNA_genes:
        raise ValueError(f"No rRNA genes found in reference file: {ref_rna}")

    logger.info(f"Loaded {len(rRNA_genes)} rRNA genes from reference")

    # Check how many rRNA genes are actually in the count matrix
    rRNA_in_data = [gene for gene in rRNA_genes if gene in counts_df.columns]

    if not rRNA_in_data:
        logger.warning(
            f"No rRNA genes from reference found in count matrix. "
            f"Returning unchanged matrix."
        )
        return counts_df

    # Filter out rRNA genes
    n_features_before = counts_df.shape[1]
    counts_filtered = counts_df.loc[:, ~counts_df.columns.isin(rRNA_genes)]
    n_features_after = counts_filtered.shape[1]
    n_removed = n_features_before - n_features_after

    logger.info(
        f"Removed {n_removed} rRNA features "
        f"({n_features_before} → {n_features_after} total features)"
    )

    return counts_filtered


def filter_samples_by_barcode(
    counts_df: pd.DataFrame,
    barcode_mapping: dict,
    samples_to_keep: list[str],
    barcode_pattern: str = 'D5_lib\d_bc1_',
    output_path: str = None
) -> pd.DataFrame:
    """
    Filter count matrix to keep only specified sample types based on barcode indices.

    Parameters
    ----------
    counts_df : pd.DataFrame
        Count matrix with cell barcodes as index.
    barcode_mapping : dict
        Mapping of barcode ranges to sample names, e.g.,
        {(1, 36): 'WT', (37, 72): 'sigB_KO', (73, 96): 'saeQRS_KO'}
    samples_to_keep : list[str]
        Sample names to keep, e.g., ['WT']
    barcode_pattern : str, optional
        Regex pattern for dataset-specific barcode format.
        Default is 'D5_lib\d_bc1_' for Saureus dataset.
        Use 'D1_lib\d_bc1_' for Ecoli dataset.
    output_path : str, optional
        Path to save filtered counts as tab-separated file.
        If None, file is not saved.

    Returns
    -------
    pd.DataFrame
        Filtered count matrix containing only specified samples.

    Raises
    ------
    ValueError
        If no samples match the samples_to_keep list.
    """
    # Create barcode lookup array from the mapping
    max_barcode = max(end for start, end in barcode_mapping.keys())
    barcode_lookup = [''] * max_barcode

    for (start, end), sample_name in barcode_mapping.items():
        for i in range(start - 1, end):  # -1 for 0-indexing
            barcode_lookup[i] = sample_name

    barcode_lookup = np.array(barcode_lookup)

    # Extract barcode indices from cell barcodes
    barcode = counts_df.index.str.replace(barcode_pattern, '', regex=True).\
        str.replace('_bc2_.*', '', regex=True).astype(int)

    # Map barcode to sample labels
    sample_label = pd.Series(barcode_lookup[barcode.to_numpy() - 1], index=counts_df.index)

    logger.info(f"Sample distribution:\n{sample_label.value_counts()}")

    # Filter to keep only specified samples
    mask = sample_label.isin(samples_to_keep)

    if not mask.any():
        raise ValueError(
            f"No samples found matching: {samples_to_keep}. "
            f"Available samples: {sample_label.unique().tolist()}"
        )

    counts_filtered = counts_df.loc[mask]

    # Set index name for consistency with saved files
    counts_filtered.index.name = 'CellBarcode'  # ← Add this line

    n_kept = mask.sum()
    n_total = len(counts_df)
    logger.info(f"Kept {n_kept}/{n_total} cells from samples: {samples_to_keep}")

    # Save to file if path provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        counts_filtered.to_csv(
            output_path,
            index=True,
            index_label='CellBarcode',
            sep="\t"
        )
        logger.info(f"Saved filtered counts to {output_path}")

    return counts_filtered