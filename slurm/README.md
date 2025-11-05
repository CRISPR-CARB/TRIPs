# SLURM

These scripts were written to run on the [sciCORE](https://scicore.unibas.ch/) cluster's [SLURM](https://slurm.schedmd.com/) workload scheduler. You may need to modify them to run on your HPC system. However, you can still look into them to have an idea of the resource allocation needed for the program they are calling. As a rule of thumb, each of the shell scripts here will be named for the program in [scripts](../scripts) that they are calling.

These SLURM scripts are intended to be called from the root of the repository. The usage pattern is:

```sh
sbatch --account=<account> --mail-user=<email> slurm/<script_name>.sh
```

The flags `--account` and `--mail-user` may or may not be needed depending on your HPC system. They are not set by default via `#SBATCH` in the scripts themselves to avoid hardcoding potentially sensitive information.
