"""
Tests for io module.

"""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
from trips.io import (
    remove_rRNA,
    # ... other functions you're testing
)

def test_load_count_matrix()