"""
Preprocessing for TRIPs analysis


"""

import pandas as pd
import numpy as np
from pathlib import Path
import logger

logger = logging.getLogger(__name__)  # __name__ will be 'trips.preprocessing'


def remove_rRNA(counts_df:pd.DataFrame, ref_rna:str) -> pd.DataFrame:

    """
    Remove all rRNA features.

    Parameters
    ----------
    counts_df : pd.DataFrame
        Dataframe containing counts
    ref_rna : str
        rRNA reference text file

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
        logger.error(f"rRNA reference file not found: {ref_rna}")
        raise FileNotFoundError(f"rRNA reference file not found: {ref_rna}")

        # Read rRNA gene names from file
    with open(ref_path, 'r') as f:
        rRNA_genes = [line.strip() for line in f if line.strip()]

    if not rRNA_genes:
        logger.error(f"No rRNA genes found in {ref_rna}")
        raise ValueError(f"No rRNA genes found in reference file: {ref_rna}")

    # Check how many rRNA genes are actually in the count matrix
    rRNA_in_data = [gene for gene in rRNA_genes if gene in counts_df.columns]

    if not rRNA_in_data:
        logger.warning(f"No rRNA genes from reference found in count matrix. "
                      f"Returning unchanged matrix.")
        return counts_df
    # Filter out rRNA genes
    n_features_before = counts_df.shape[1]
    counts_filtered = counts_df.loc[:, ~counts_df.columns.isin(rRNA_genes)]
    n_features_after = counts_filtered.shape[1]
    n_removed = n_features_before - n_features_after

    logger.debug(f"Removed rRNA genes: {rRNA_in_data}")  # Only shows with --verbose
    logger.info(f"Removed {n_removed} rRNA features...")  # Always shows
    return counts_filtered


def filter_samples_by_bc1(
    counts_df: pd.DataFrame,
    bc1_mapping: dict,
    samples_to_keep: list[str]
) -> pd.DataFrame:
    """
    Filter count matrix to keep only specified sample types based on bc1 indices.

    Parameters
    ----------
    counts_df : pd.DataFrame
        Count matrix with cell barcodes as index
    bc1_mapping : dict
        Mapping of bc1 ranges to sample names, e.g.,
        {(1, 36): 'WT', (37, 72): 'sigB_KO', (73, 96): 'saeQRS_KO'}
    samples_to_keep : list[str]
        Sample names to keep, e.g., ['WT']

    Returns
    -------
    pd.DataFrame
        Filtered count matrix containing only specified samples
    """

    # Extract bc1 indices from cell barcodes
    # Parse based on PETRI-seq naming convention

    # creates list like: ['WT', 'WT', ..., 'sigB_KO', 'sigB_KO', ..., 'saeQRS_KO', ...]
    bc1_lookup = list(bc1_mapping.keys())

    # Extract the bc1 indices from the cell barcode names
    bc1 = counts_df.index.str.replace('D5_lib\d_bc1_', '', regex=True).\
        str.replace('_bc2_.*', '', regex=True).astype(int)

    # Convert bc1 to sample and quantify indices per sample
    sample_label = pd.Series(bc1_lookup[bc1.to_numpy() - 1], index=counts_df.index)
    sample_label.value_counts()

    counts = counts.loc[sample_label == 'WT']
    counts.to_csv('outputs/tsb_raw_counts.txt.gz',
                index=True, index_label='CellBarcode', sep="\t"
                )