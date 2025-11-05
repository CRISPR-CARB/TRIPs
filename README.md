# TRIPs

This repo contains code for pre-processing, cycle analysis, promoter distance analysis, and trip analysis for bacterium.

[![project-badge](https://img.shields.io/badge/project%20status-ongoing-green)][repository]
[![docs-badge](https://img.shields.io/badge/docs-pages-blue)][docs]
[![license-badge](https://img.shields.io/badge/open--source-green)](LICENSE)
[![python-versions-badge](https://img.shields.io/badge/python-3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)][project-config]

Version: 0.1.0

### Dependencies
Analysis was done with Python v3.8.6 with the following libraries:
- numpy v1.23.3
- pandas v1.3.3
- scanpy v1.7.1 (https://scanpy.readthedocs.io)
- scvi v0.9.0 (https://scvi-tools.org/)

Code has been tested only on these library versions. No non-standard hardware is required and installation only takes minutes. We recommend using conda to create an specific environment - here all installations were done using anaconda3 (https://www.anaconda.com/download).

### Guide to notebooks
There are two example workflows (see Table S1 from the manuscript for details):
- Ecoli_D1: *E. coli* MG1655 grown in LB
- Saureus_D5: *S. aureus* USA300 LAC grown in TSB

For each of these we have the following notebooks:
- `initial_processing.ipynb`: Code for doing initial data import, filtering, and scVI denoising. This also has the code to generate global correlation patterns. The whole workbook takes ~1 hr to run.
- `cycle_analysis.ipynb`: Code for doing cell cycle analysis including assigning cell and gene angles, finding cycle variable genes, and aligning cell angle by the predicted point of replication. All analysis takes ~10 min to run (with additional time for `origin_angle_circular_model.R` (see below).
- `promoter_distance_analysis.ipynb`: Determining relationships between expression patterns and distance from the transcriptional start site (see Figure 4 in the manuscript). Takes <5 min to run.
- `trip_analysis.ipynb`: Defining Transcription-Replication Interaction Profiles (TRIPs) and performing clustering on these. Takes <5 min to run.

In addition there is the `origin_angle_circular_model.R` file. This is a script that must be run separately in RStudio as part of the `cycle_analysis.ipynb` workflow (see notebook for details). This takes ~5 min to run.

  There are also the following folders:
  - `count_matrices`: Raw count matrices for each library as output of the PETRI-seq processing pipeline (https://tavazoielab.c2b2.columbia.edu/PETRI-seq/).
  - `outputs`: Output files from the scripts above.
  - `samples`: Actual files used within the analysis presented for the manuscript. These are frequently used as inputs in the Jupyter notebooks to aid comparison to manuscript figures.
  - `reference`: Gene annotation files.

In order to make the analysis work, you **must run the initial steps of the `initial_processing.ipynb` notebook** to generate the AnnData file (`*_adata.h5ad`). This file was too large to upload directly to Github (>500 MB), so you'll need to generate it yourself. Please contact the lab if you have any issues doing so. Once you have done this, you should be able to run the notebooks individually without issues.

### Considerations for running this analysis on new data
We have not yet fully automated the analysis pipeline. As such, there are a number of parameters that may need to be varied in this workflow for working with new data:
- scVI hyperparameters: We stick with the same ones throughout but it should be considered whether these are right for your dataset or a further hyperparameter search is warranted.
- UMAP chromosome bin size (see `cycle_analysis.ipynb`): The size of chromosome bins used may need to be varied based on species and data quality. We have done 100 kb for *E. coli* and 50 kb for *S. aureus, which given the differing genome sizes is ~50 bins for each chromosome. For lower quality datasets, the bin size may need to increase.
- Angle orientation: As explained in the `cycle_analysis.ipynb`, the initial directionality of the cell angles/gene angles is arbitrary and may need to be reversed. See notebook for details.
- Chain selection in Rstan model fit: The cyclical regression model tends to hit a lot of local minima. However, we run eight chains (eight independent fits) with the HMC sampling, allowing us to clearly identify the chains that fit correctly. See `origin_angle_circular_model.R` for details.

## Usage

The notebooks in [`notebooks`][notebooks] are meant to highlight package functionality while answering specific questions within the context of the project. You can see these notebooks as an examples gallery, usually going from more basic to more advanced topics, hence the numeration. Thus, examples of how to load and display data are usually found in the first notebooks, while more advanced scientific questions are addressed in the later ones.

## Documentation

The documentation for this project is available at [jeremy.zucker.gitlab.io/TRIPs/][docs].

## Contributing

Contributions are very much welcomed, see [CONTRIBUTING][contributing] for instructions.

## Authors and acknowledgment

This repository was initialized from the [ceda-project-copier][ceda-project-copier] template.

## Citing

If you find this work useful or inspiring in your research, consider citing our work:

```bibtex

```

## License

See [LICENSE][license].

[ceda-project-copier]: https://ceda-unibas.gitlab.io/ceda-project-copier/
[docs]: https://jeremy.zucker.gitlab.io/TRIPs/
[contributing]: CONTRIBUTING.md
[research-group]: https://www.unibas.ch/
[license]: LICENSE
[repository]: https://gitlab.com/jeremy.zucker/TRIPs
[notebooks]: https://gitlab.com/jeremy.zucker/TRIPs/-/tree/main/notebooks
[scripts]: https://gitlab.com/jeremy.zucker/TRIPs/-/tree/main/scripts
[project-config]: https://gitlab.com/jeremy.zucker/TRIPs/-/blob/main/pyproject.toml
