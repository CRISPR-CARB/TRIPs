#!/bin/bash
#SBATCH --job-name=hello
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=0:05:00
#SBATCH --qos=30min
#SBATCH --output=logs/hello.o
#SBATCH --error=logs/hello.e
#SBATCH --mail-type=END,FAIL,TIME_LIMIT


uv run "src/TRIPs/hello.py"

