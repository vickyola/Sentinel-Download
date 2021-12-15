#!/bin/bash

#SBATCH --mem-per-cpu=1gb
#SBATCH --job-name=download_crop_model_data_test
#SBATCH --output=/work/%u/%x-%j.out
#SBATCH --time=0-00:01:00   


python download_sentinel.py

