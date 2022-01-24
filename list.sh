#!/bin/bash

#SBATCH --mem-per-cpu=1gb
#SBATCH --job-name=download_in_work_test
#SBATCH --output=/work/%u/%x-%j.out
#SBATCH --time=0-0:05:00   

python list_files.py
