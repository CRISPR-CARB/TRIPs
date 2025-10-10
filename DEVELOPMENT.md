# TRIPs Package Refactoring: Convert to Installable Package with CLI and Workflow Support

## Overview
This PR refactors the TRIPs analysis notebooks into a well-structured, installable Python package with both a command-line interface (CLI) and Snakemake workflow support. The goal is to make TRIPs more accessible, reproducible, and maintainable while preserving all current functionality.

## Motivation
Currently, TRIPs consists of Jupyter notebooks that must be run sequentially with manual parameter adjustments. This refactoring will:
- Make the analysis pipeline easier to run and reproduce
- Provide clear interfaces for both interactive and automated use
- Enable better testing and validation
- Improve code maintainability and extensibility
- Lower the barrier to entry for new users

## Proposed Changes

### 1. Package Structure
- [ ] Create proper Python package structure with `src/trips/` layout
- [ ] Set up `pyproject.toml` with dependencies and package metadata
- [ ] Organize code into logical modules:
  - `preprocessing.py` - Data import, filtering, scVI denoising
  - `cycle_analysis.py` - Cell cycle analysis, angle assignment
  - `promoter_analysis.py` - TSS distance relationship analysis
  - `trip_analysis.py` - TRIP definition and clustering
  - `utils.py` - Shared utility functions
  - `io.py` - File I/O operations
  - `visualization.py` - Plotting functions
- [ ] Extract notebook code into functions with clear inputs/outputs
- [ ] Add `__init__.py` files with public API exports

### 2. Command-Line Interface (CLI)
- [ ] Implement Click-based CLI with subcommands:
  - `trips preprocess` - Run initial processing and scVI denoising
  - `trips cycle-analysis` - Perform cell cycle analysis
  - `trips promoter-analysis` - Analyze promoter distance relationships
  - `trips trip-analysis` - Define and cluster TRIPs
  - `trips run-all` - Run complete pipeline
- [ ] Add `--help` documentation for all commands and parameters
- [ ] Implement verbose/quiet logging options
- [ ] Add `--config` option to load parameters from YAML/JSON file
- [ ] Include `--dry-run` flag for validation without execution

### 3. Configuration Management
- [ ] Create configuration schema (YAML format)
- [ ] Provide example config files for E. coli and S. aureus datasets
- [ ] Document all configurable parameters with descriptions and defaults
- [ ] Implement parameter validation with helpful error messages
- [ ] Support parameter overrides via CLI flags

### 4. Snakemake Workflow
- [ ] Create `Snakefile` that orchestrates the full pipeline
- [ ] Define rules for each analysis step
- [ ] Set up proper input/output dependencies
- [ ] Create `config.yaml` template for workflow parameters
- [ ] Add example workflow configurations for provided datasets
- [ ] Document workflow usage in separate `WORKFLOW.md`

### 5. Code Quality & Best Practices
- [ ] Replace print statements with proper logging (using Python `logging` module)
- [ ] Add type hints to all functions
- [ ] Implement input validation with clear error messages
- [ ] Add docstrings to all public functions (Google or NumPy style)
- [ ] Set up code formatting (Black) and linting (Ruff/Flake8)
- [ ] Ensure consistent naming conventions

### 6. Testing
- [ ] Set up pytest testing framework
- [ ] Add unit tests for utility functions
- [ ] Add integration tests using example datasets
- [ ] Test CLI commands with various parameter combinations
- [ ] Validate Snakemake workflow execution
- [ ] Set up CI/CD for automated testing (GitHub Actions)

### 7. Documentation
- [ ] Create comprehensive `README.md` with:
  - Installation instructions
  - Quick start guide
  - CLI usage examples
  - Configuration file format
- [ ] Add `INSTALLATION.md` with detailed setup instructions
- [ ] Create `WORKFLOW.md` for Snakemake usage
- [ ] Convert existing notebooks to tutorial/example notebooks
- [ ] Add inline code documentation
- [ ] Create API documentation (consider Sphinx or MkDocs)

### 8. Backwards Compatibility
- [ ] Keep original notebooks functional as examples/tutorials
- [ ] Ensure new package produces identical results to notebooks
- [ ] Document any behavioral changes or improvements
- [ ] Provide migration guide from notebooks to package/CLI

### 9. Dependencies & Environment
- [ ] Pin dependency versions in `pyproject.toml`
- [ ] Create `environment.yml` for conda users
- [ ] Document minimum Python version requirement
- [ ] Address R script dependency (`origin_angle_circular_model.R`):
  - Option A: Keep as external dependency with clear instructions
  - Option B: Investigate Python alternatives (needs discussion)
  - Option C: Wrap R script with rpy2 for seamless integration

### 10. Additional Improvements (Future Considerations)
- [ ] Add progress bars for long-running operations
- [ ] Implement checkpointing/resume capability
- [ ] Add data validation checks at pipeline entry points
- [ ] Create output summary reports
- [ ] Consider containerization (Docker) for reproducibility

## Implementation Plan

### Phase 1: Foundation (Weeks 1-2)
- Set up package structure
- Extract core functions from `initial_processing.ipynb`
- Implement basic CLI for preprocessing step
- Set up testing framework

### Phase 2: Core Functionality (Weeks 3-4)
- Extract remaining notebook code into modules
- Complete CLI for all analysis steps
- Implement configuration system
- Add comprehensive logging

### Phase 3: Workflow & Documentation (Weeks 5-6)
- Create Snakemake workflow
- Write documentation
- Add tests and validation
- Set up CI/CD

### Phase 4: Polish & Review (Week 7)
- Code review and refactoring
- Performance optimization if needed
- Final testing with both example datasets
- Documentation review

## Questions for Discussion
1. **Target users**: Should we optimize for bioinformaticians familiar with command line, or make it accessible to wet lab researchers?
2. **R dependency**: What's the preferred approach for handling `origin_angle_circular_model.R`?
3. **Output formats**: Should we standardize output formats or maintain current structure?
4. **Testing data**: Are there additional datasets beyond Ecoli_D1 and Saureus_D5 we should test with?
5. **Version numbering**: What should the first release version be? (suggest v1.0.0)

## Testing Plan
- Run full pipeline on both example datasets
- Compare outputs to original notebook results (ensure numerical equivalence)
- Test various parameter configurations
- Validate error handling with malformed inputs
- Benchmark performance against original notebooks

## Breaking Changes
None expected - this is additive functionality. Original notebooks will remain functional.

## Related Issues
- (Link any relevant GitHub issues here)

---

**CC:** @jeremy (replace with actual GitHub username)

**Timeline:** ~7 weeks estimated

**Status:** Draft for feedback - please review and comment!