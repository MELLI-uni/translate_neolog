#!/bin/bash
#
#SBATCH --job-name=scraper
#SBATCH --output=/zooper2/jiyoon.pyo/translate_neolog/output.out
#SBATCH --gres=gpu:2
#SBATCH --ntasks=1
#SBATCH --gres-flags=enforce-binding
#SBATCH --nodes=1-1
#SBATCH --mem=20gb

export LD_LIBRARY_PATH=/usr/local/cuda/lib64/

cd translate_neolog
python tweet_scraper.py
