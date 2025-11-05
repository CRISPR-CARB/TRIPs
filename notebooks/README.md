# Notebooks

The `notebooks/` folder contains notebooks demonstrating `TRIPs`-capabilities and running through specific analysis pipelines.

## Running notebooks

You can launch Jupyter Lab from the command line by running:


```bash
uv run --with jupyter jupyter lab
```


If your Jupyter Lab instance is launched outside the project environment (e.g. on Open OnDemand), you may need to make this project's ipykernel available to Jupyter Lab. To
do this, run the following command in the terminal:


```bash
uv run python -m ipykernel install --user --name=TRIPs --display-name "Python [uv env: TRIPs]"
```


Restart Jupyter Lab and you should now be able to see "Python [uv env: TRIPs]" as an option in the kernel selection menu in the top right corner of the notebook interface.
