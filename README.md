# Monza 2024: Race Pace and Tyre Strategies

Python project for the Coding for Data Science and Data Management
course, academic year 2026/2027.

## Objective

Explore differences in race pace, tyre strategies and final results
at the 2024 Italian Grand Prix.

The project includes an overview of all 20 participants, detailed
analysis of Charles Leclerc, Lando Norris and Oscar Piastri,
and teammate comparisons for Ferrari, McLaren, Mercedes and Red Bull.

## Research questions

1. How did lap times vary between drivers throughout the race?
2. How did tyre strategies and stint lengths differ?
3. How did filtered race pace compare with final race results?

## Data source

Data was originally downloaded from the
[OpenF1 API](https://openf1.org/docs/).

Race: 2024 Italian Grand Prix, Monza.
Session key: `9590`.

### Original OpenF1 requests

The race session key was found with
`GET https://api.openf1.org/v1/sessions?year=2024&session_name=Race`.
The Monza race has session key `9590`.

| Snapshot in `data/raw/` | Original GET request |
| --- | --- |
| `monza_2024_drivers.csv` | `https://api.openf1.org/v1/drivers?session_key=9590` |
| `monza_2024_laps.csv` | `https://api.openf1.org/v1/laps?session_key=9590` |
| `monza_2024_stints.csv` | `https://api.openf1.org/v1/stints?session_key=9590` |
| `monza_2024_race_control.csv` | `https://api.openf1.org/v1/race_control?session_key=9590` |
| `monza_2024_session_result.csv` | `https://api.openf1.org/v1/session_result?session_key=9590` |

The API responses were read as JSON, converted to pandas DataFrames,
and saved as CSV files.

The notebook reads the snapshots from `data/raw/`.
After dependencies are installed, running the analysis does not
require internet access.

OpenF1 is an independent community project, not an official
Formula 1 or FIA data service.

## Project files

| File or folder | Purpose |
|---|---|
| `race_analysis.ipynb` | Analysis, visualisations and conclusions |
| `data_io.py` | Loading saved CSV tables |
| `analysis.py` | Lap filtering and descriptive pace statistics |
| `plots.py` | Reusable race pace and tyre strategy plots |
| `data/raw/` | Downloaded source snapshots |
| `data/processed/` | Exported analysis tables |
| `requirements.txt` | Python dependencies and installed versions |
| `.gitignore` | Files excluded from version control |

## Setup on Windows

Python 3.12 is used for this project.

Clone the repository and enter its folder:

```powershell
git clone https://github.com/Aishendo/f1-race-analysis.git
cd f1-race-analysis
```

Create a virtual environment and install dependencies:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Start JupyterLab from the project folder:

```powershell
.\.venv\Scripts\python.exe -m jupyterlab
```

Open `race_analysis.ipynb` and run all cells in order.

Alternatively, open the project in VS Code, install the Microsoft
Python and Jupyter extensions, and select the `.venv` notebook kernel.

A private repository requires GitHub access to clone.

## Run the Streamlit app

After installing the dependencies in **Setup on Windows**, run this
command from the project folder:

```powershell
.\.venv\Scripts\python.exe -m streamlit run streamlit_app.py
```

Open the **Local URL** printed in the terminal. Use the sidebar to
navigate between Race overview, Race pace, Tyre strategies, Teammates
and Conclusions. The app reads the included OpenF1 snapshots directly
from `data/raw/` and can run independently of the notebook.

## Libraries

- pandas: loading, filtering, joining and summarising tables
- Matplotlib: visualisations
- JupyterLab and ipykernel: notebook execution

The notebook also imports NumPy. Requests was used during the
initial API data collection.

## Method

Original snapshots are preserved. Pace statistics use a separate
filtered table that excludes:
- The first race lap
- Pit-out laps marked by OpenF1
- Presumed pit-in laps immediately preceding a pit-out lap,
  when lap numbers are consecutive
- Missing or non-positive lap times

Statistics include lap count, median lap time, sample standard
deviation and fastest retained lap.

For tyre analysis, laps are matched to stint boundaries.
Tyre age at the start of a lap is calculated from the initial
tyre age and the lap's position within the stint.

## Main findings

Among the three main drivers, Piastri had the lowest median
filtered lap time: 83.468 seconds. Norris recorded 83.591 seconds
and Leclerc 83.716 seconds.

Leclerc nevertheless won, finishing 2.664 seconds ahead of
Piastri and 6.153 seconds ahead of Norris.

Leclerc used one stop, while Norris and Piastri used two.
Leclerc's final Hard stint covered 38 laps.

These results illustrate why filtered median pace alone
does not determine the final race result.

## Limitations

This is a descriptive study of one race, not a causal model
or an estimate of the optimal strategy.

Traffic, fuel load, weather and local yellow flags are not
controlled for. Tyre-age plots also reflect other changes
throughout the race and do not isolate tyre degradation.

Drivers who retired or were lapped covered different race
distances, limiting direct comparisons of their summary statistics.

No Safety Car, VSC or red-flag messages were found by the filter
applied to the downloaded race control data.

## Outputs

Running the notebook exports:
- `data/processed/monza_2024_pace_vs_results.csv`
- `data/processed/monza_2024_all_drivers_overview.csv`