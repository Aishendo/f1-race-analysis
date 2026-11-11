# F1 Race Analysis — Monza 2024

Python project for the Coding for Data Science and Data Management
course, academic year 2026/2027.

## Objective

Explore race pace and tyre strategies of Charles Leclerc,
Lando Norris and Oscar Piastri at the 2024 Italian Grand Prix.

## Data source

OpenF1 API: https://openf1.org/

Session key: 9590.
Downloaded CSV snapshots are stored in data/raw/.

## Current progress

- Loaded driver, lap, stint and race control data.
- Checked missing lap times and duplicate laps.
- Visualised lap times and tyre strategies.
- Calculated preliminary race pace statistics.

The analysis is in progress.

## Setup and run on Windows

Run these commands from the project folder:

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt
    .\.venv\Scripts\python.exe -m jupyterlab

Open race_analysis.ipynb and run the cells in order.
The notebook loads the included CSV snapshots from data/raw/.
No internet connection is required to run the analysis after installing the dependencies.