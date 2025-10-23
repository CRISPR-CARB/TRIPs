"""
Tests for preprocessing module.

This module contains unit and integration tests for the preprocessing functions
in trips.preprocessing, including:
- Removing rRNA features
- Filtering samples by bc1 indices
- Data validation and error handling

Tests use example datasets from the TRIPs repository (Ecoli_D1 and Saureus_D5)
or generate synthetic test data where appropriate.
"""

import pytest
import pandas as pd
import numpy as np
import TRIPs
from pathlib import Path
from TRIPs.preprocessing import (
    remove_rRNA,
    filter_samples_by_bc1
    # ... other functions you're testing
)


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def sample_counts_df():
    """Create a sample count matrix for testing."""
    return pd.DataFrame({
        'gene1': [10, 20, 30],
        'gene2': [5, 15, 25],
        'rRNA_16S': [100, 200, 300],
        'rRNA_23S': [150, 250, 350],
        'gene3': [8, 18, 28],
    }, index=['cell1', 'cell2', 'cell3'])


@pytest.fixture
def rRNA_reference_file(tmp_path):
    """Create a temporary rRNA reference file."""
    ref_file = tmp_path / "rRNA_genes.txt"
    ref_file.write_text("rRNA_16S\nrRNA_23S\n")
    return str(ref_file)


@pytest.fixture
def empty_rRNA_file(tmp_path):
    """Create an empty rRNA reference file."""
    ref_file = tmp_path / "empty_rRNA.txt"
    ref_file.write_text("")
    return str(ref_file)


@pytest.fixture
def rRNA_file_with_whitespace(tmp_path):
    """Create rRNA file with extra whitespace and blank lines."""
    ref_file = tmp_path / "rRNA_whitespace.txt"
    ref_file.write_text("rRNA_16S\n\n  rRNA_23S  \n\n")
    return str(ref_file)

@pytest.fixture
def sample_counts_with_barcodes():
    """Create a count matrix with PETRI-seq style barcodes."""
    # Create barcodes that match the PETRI-seq format
    # bc1 values: 1-5 will be WT, 6-10 will be knockout
    barcodes = [
        'D5_lib1_bc1_1_bc2_100',
        'D5_lib1_bc1_2_bc2_101',
        'D5_lib1_bc1_3_bc2_102',
        'D5_lib2_bc1_4_bc2_103',
        'D5_lib2_bc1_5_bc2_104',
        'D5_lib1_bc1_6_bc2_105',
        'D5_lib1_bc1_7_bc2_106',
        'D5_lib2_bc1_8_bc2_107',
        'D5_lib2_bc1_9_bc2_108',
        'D5_lib1_bc1_10_bc2_109',
    ]

    return pd.DataFrame({
        'gene1': np.random.randint(0, 100, 10),
        'gene2': np.random.randint(0, 100, 10),
        'gene3': np.random.randint(0, 100, 10),
    }, index=barcodes)


@pytest.fixture
def simple_bc1_mapping():
    """Simple bc1 mapping for testing."""
    return {
        (1, 5): 'WT',
        (6, 10): 'knockout'
    }


@pytest.fixture
def complex_bc1_mapping():
    """More complex bc1 mapping with 3 conditions."""
    return {
        (1, 36): 'WT',
        (37, 72): 'sigB_KO',
        (73, 96): 'saeQRS_KO'
    }


# ============================================================================
# Unit Tests (using synthetic data)
# ============================================================================
def test_remove_rRNA_basic(sample_counts_df, rRNA_reference_file):
    """Test basic rRNA removal."""
    result = remove_rRNA(sample_counts_df, rRNA_reference_file)

    # Check that rRNA genes were removed
    assert 'rRNA_16S' not in result.columns
    assert 'rRNA_23S' not in result.columns

    # Check that other genes remain
    assert 'gene1' in result.columns
    assert 'gene2' in result.columns
    assert 'gene3' in result.columns

    # Check shape
    assert result.shape == (3, 3)  # 3 cells, 3 non-rRNA genes

    # Check data integrity (values unchanged for remaining genes)
    pd.testing.assert_series_equal(result['gene1'], sample_counts_df['gene1'])


def test_remove_rRNA_preserves_index(sample_counts_df, rRNA_reference_file):
    """Test that cell indices are preserved after filtering."""
    result = remove_rRNA(sample_counts_df, rRNA_reference_file)

    pd.testing.assert_index_equal(result.index, sample_counts_df.index)


def test_remove_rRNA_file_not_found(sample_counts_df):
    """Test error when rRNA reference file doesn't exist."""
    with pytest.raises(FileNotFoundError, match="rRNA reference file not found"):
        remove_rRNA(sample_counts_df, "nonexistent_file.txt")


def test_remove_rRNA_empty_file(sample_counts_df, empty_rRNA_file):
    """Test error when rRNA reference file is empty."""
    with pytest.raises(ValueError, match="No rRNA genes found in reference file"):
        remove_rRNA(sample_counts_df, empty_rRNA_file)


def test_remove_rRNA_whitespace_handling(sample_counts_df, rRNA_file_with_whitespace):
    """Test that whitespace and blank lines are handled correctly."""
    result = remove_rRNA(sample_counts_df, rRNA_file_with_whitespace)

    # Should still remove the rRNA genes despite whitespace
    assert 'rRNA_16S' not in result.columns
    assert 'rRNA_23S' not in result.columns
    assert result.shape == (3, 3)


def test_remove_rRNA_no_overlap(sample_counts_df, tmp_path):
    """Test when rRNA genes don't exist in count matrix."""
    # Create reference with genes not in the data
    ref_file = tmp_path / "other_rRNA.txt"
    ref_file.write_text("rRNA_5S\nrRNA_18S\n")

    result = remove_rRNA(sample_counts_df, str(ref_file))

    # Should return unchanged matrix
    pd.testing.assert_frame_equal(result, sample_counts_df)


def test_remove_rRNA_partial_overlap(sample_counts_df, tmp_path):
    """Test when only some rRNA genes exist in count matrix."""
    # Reference has one gene that exists and one that doesn't
    ref_file = tmp_path / "partial_rRNA.txt"
    ref_file.write_text("rRNA_16S\nrRNA_5S\n")

    result = remove_rRNA(sample_counts_df, str(ref_file))

    # Should remove only the gene that exists
    assert 'rRNA_16S' not in result.columns
    assert 'rRNA_23S' in result.columns  # This wasn't in reference
    assert result.shape == (3, 4)


def test_remove_rRNA_all_genes_are_rRNA(tmp_path):
    """Test when all genes in matrix are rRNA."""
    counts = pd.DataFrame({
        'rRNA_16S': [100, 200],
        'rRNA_23S': [150, 250],
    }, index=['cell1', 'cell2'])

    ref_file = tmp_path / "all_rRNA.txt"
    ref_file.write_text("rRNA_16S\nrRNA_23S\n")

    result = remove_rRNA(counts, str(ref_file))

    # Should return empty DataFrame with same index
    assert result.shape == (2, 0)
    pd.testing.assert_index_equal(result.index, counts.index)


def test_remove_rRNA_empty_counts_df(rRNA_reference_file):
    """Test with empty count matrix."""
    empty_counts = pd.DataFrame()

    result = remove_rRNA(empty_counts, rRNA_reference_file)

    # Should handle gracefully
    assert result.shape == (0, 0)


def test_remove_rRNA_case_sensitive(tmp_path):
    """Test that gene matching is case-sensitive."""
    counts = pd.DataFrame({
        'rRNA_16S': [100, 200],
        'rrna_16s': [50, 100],  # Different case
        'gene1': [10, 20],
    }, index=['cell1', 'cell2'])

    ref_file = tmp_path / "case_test.txt"
    ref_file.write_text("rRNA_16S\n")  # Only exact match

    result = remove_rRNA(counts, str(ref_file))

    # Should only remove exact match
    assert 'rRNA_16S' not in result.columns
    assert 'rrna_16s' in result.columns  # Different case should remain
    assert result.shape == (2, 2)


def test_remove_rRNA_returns_copy(sample_counts_df, rRNA_reference_file):
    """Test that function returns a new DataFrame, not modifying original."""
    original_shape = sample_counts_df.shape
    original_columns = sample_counts_df.columns.tolist()

    result = remove_rRNA(sample_counts_df, rRNA_reference_file)

    # Original should be unchanged
    assert sample_counts_df.shape == original_shape
    assert sample_counts_df.columns.tolist() == original_columns

    # Result should be different
    assert result.shape != sample_counts_df.shape

def test_filter_samples_basic(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test basic sample filtering keeping only WT."""
    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT']
    )

    # Should keep only cells with bc1 1-5 (5 cells)
    assert result.shape[0] == 5
    assert result.shape[1] == 3  # Same number of genes

    # Check that correct barcodes are kept
    for barcode in result.index:
        bc1 = int(barcode.split('_bc1_')[1].split('_bc2_')[0])
        assert 1 <= bc1 <= 5


def test_filter_samples_keep_knockout(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test filtering to keep only knockout samples."""
    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['knockout']
    )

    # Should keep only cells with bc1 6-10 (5 cells)
    assert result.shape[0] == 5

    # Check that correct barcodes are kept
    for barcode in result.index:
        bc1 = int(barcode.split('_bc1_')[1].split('_bc2_')[0])
        assert 6 <= bc1 <= 10


def test_filter_samples_keep_multiple(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test keeping multiple sample types."""
    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT', 'knockout']
    )

    # Should keep all cells
    assert result.shape[0] == 10


def test_filter_samples_preserves_data(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test that gene expression data is preserved correctly."""
    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT']
    )

    # Check that values match for a specific barcode
    test_barcode = 'D5_lib1_bc1_1_bc2_100'
    pd.testing.assert_series_equal(
        result.loc[test_barcode],
        sample_counts_with_barcodes.loc[test_barcode]
    )
def test_filter_samples_ecoli_pattern():
    """Test with Ecoli (D1) barcode pattern."""
    barcodes = [
        'D1_lib1_bc1_1_bc2_100',
        'D1_lib1_bc1_2_bc2_101',
        'D1_lib1_bc1_6_bc2_102',
    ]

    counts = pd.DataFrame({
        'gene1': [10, 20, 30],
        'gene2': [15, 25, 35],
    }, index=barcodes)

    bc1_mapping = {(1, 5): 'WT', (6, 10): 'knockout'}

    result = filter_samples_by_bc1(
        counts,
        bc1_mapping,
        samples_to_keep=['WT'],
        barcode_pattern="D1_lib\d_bc1_"  # Ecoli pattern
    )

    assert result.shape[0] == 2  # First two barcodes


def test_filter_samples_wrong_pattern_raises_error():
    """Test that using wrong barcode pattern causes issues."""
    barcodes = ['D1_lib1_bc1_1_bc2_100']  # D1 format
    counts = pd.DataFrame({'gene1': [10]}, index=barcodes)
    bc1_mapping = {(1, 5): 'WT'}

    # Using D5 pattern on D1 data should fail to parse
    with pytest.raises((ValueError, TypeError)):
        filter_samples_by_bc1(
            counts,
            bc1_mapping,
            samples_to_keep=['WT'],
            barcode_pattern="D5_lib\d_bc1_"  # Wrong pattern!
        )
def test_filter_samples_no_matching_samples(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test error when no samples match the filter."""
    with pytest.raises(ValueError, match="No samples found matching"):
        filter_samples_by_bc1(
            sample_counts_with_barcodes,
            simple_bc1_mapping,
            samples_to_keep=['nonexistent_sample']
        )


def test_filter_samples_empty_samples_list(sample_counts_with_barcodes, simple_bc1_mapping):
    """Test with empty samples_to_keep list."""
    with pytest.raises(ValueError, match="No samples found matching"):
        filter_samples_by_bc1(
            sample_counts_with_barcodes,
            simple_bc1_mapping,
            samples_to_keep=[]
        )


def test_filter_samples_invalid_bc1_mapping():
    """Test with invalid bc1_mapping structure."""
    barcodes = ['D5_lib1_bc1_1_bc2_100']
    counts = pd.DataFrame({'gene1': [10]}, index=barcodes)

    # Invalid mapping (not dict of tuples)
    invalid_mapping = {'WT': [1, 5]}

    with pytest.raises((KeyError, TypeError, ValueError)):
        filter_samples_by_bc1(
            counts,
            invalid_mapping,
            samples_to_keep=['WT']
        )

def test_filter_samples_saves_to_file(sample_counts_with_barcodes, simple_bc1_mapping, tmp_path):
    """Test that filtered data is saved correctly when output_path provided."""
    output_file = tmp_path / "filtered_counts.tsv"

    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT'],
        output_path=str(output_file)
    )

    # Check file was created
    assert output_file.exists()

    # Read back and verify
    saved_data = pd.read_csv(output_file, sep='\t', index_col='CellBarcode')
    pd.testing.assert_frame_equal(result, saved_data)


def test_filter_samples_creates_output_directory(sample_counts_with_barcodes, simple_bc1_mapping, tmp_path):
    """Test that output directory is created if it doesn't exist."""
    output_file = tmp_path / "nested" / "dir" / "filtered_counts.tsv"

    filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT'],
        output_path=str(output_file)
    )

    # Check nested directory was created
    assert output_file.parent.exists()
    assert output_file.exists()


def test_filter_samples_no_output_file(sample_counts_with_barcodes, simple_bc1_mapping, tmp_path):
    """Test that no file is saved when output_path is None."""
    result = filter_samples_by_bc1(
        sample_counts_with_barcodes,
        simple_bc1_mapping,
        samples_to_keep=['WT'],
        output_path=None
    )

    # Should return DataFrame but not save anything
    assert isinstance(result, pd.DataFrame)
    assert len(list(tmp_path.iterdir())) == 0  # tmp_path should be empty


# ============================================================================
# Integration Tests (using real reference file)
# ============================================================================

