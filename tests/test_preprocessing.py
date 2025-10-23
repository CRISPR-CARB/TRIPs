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
from pathlib import Path
from trips.preprocessing import (
    remove_rRNA,
    # ... other functions you're testing
)

def test_remove_rRNA():
    return