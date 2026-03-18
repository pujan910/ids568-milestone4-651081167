# IDS 568 Milestone 4

## Overview
This project is about building a distributed feature engineering pipeline using Ray. The goal was to generate a large synthetic dataset (10M+ rows) and compare local vs distributed execution. Everything is reproducible using a fixed seed.

## Setup

Clone repo:
git clone https://github.com/pujan910/ids568-milestone4-651081167.git
cd ids568-milestone4-651081167

Create env:
python -m venv .venv
source .venv/bin/activate

Install deps:
pip install -r requirements.txt

## Data Generation

python generate_data.py --rows 10000000 --seed 42 --output data.parquet

- uses seed so same data every time
- stored as parquet for faster read

## Run Pipeline

Local:
python pipeline.py --mode local

Distributed:
python pipeline.py --mode distributed --chunks 4

## What it does

- reads dataset
- creates feature: amount_squared
- groups by transaction_type
- computes mean

Distributed:
- splits data into chunks
- runs in parallel using Ray
- combines results using sum + count (so its correct)

## Reproducibility

- seed = 42 used
- same outputs every run
- requirements.txt has all packages
- no hardcoded paths

## Results

Local:
~0.4 sec

Distributed:
~2.9 sec

local is faster here coz overhead of ray is high for this size

## Notes

- ray has startup overhead
- distributed is slower for smaller datasets
- but scales better for large data or multiple machines
- both modes give same results

## Files

pipeline.py → main pipeline
generate_data.py → data generation
REPORT.md → analysis
requirements.txt → dependencies

## Final

Project can be reproduced easily using above steps.
