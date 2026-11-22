import matplotlib.pyplot as plt
import pandas as pd


def plot_race_pace(
    pace_laps: pd.DataFrame,
    drivers: pd.DataFrame,
    driver_numbers: list[int],
    total_laps: int,
):
    """Plot filtered lap times for selected drivers.

    Args:
        pace_laps: Filtered data with driver_number, lap_number
            and lap_duration.
        drivers: Driver information with driver_number and full_name.
        driver_numbers: Driver numbers to include.
        total_laps: Number of laps shown on the horizontal axis.

    Returns:
        The Matplotlib figure and axes.
    """
    names = drivers.set_index("driver_number")["full_name"].to_dict()
    fig, ax = plt.subplots(figsize=(12, 5))

    for number in driver_numbers:
        driver_data = pace_laps.loc[
            pace_laps["driver_number"].eq(number)
        ].sort_values("lap_number")

        lap_times = (
            driver_data.set_index("lap_number")["lap_duration"]
            .reindex(range(1, total_laps + 1))
        )

        ax.plot(
            lap_times.index,
            lap_times,
            label=names[number],
            linewidth=1.5,
        )

    ax.set_title(
        "Monza 2024 — Race pace\n"
        "Start and pit-related laps excluded"
    )
    ax.set_xlabel("Race lap")
    ax.set_ylabel("Lap time (seconds)")
    ax.legend(bbox_to_anchor=(1.02, 1), loc="upper left")
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig, ax

def plot_tyre_strategies(
    stints: pd.DataFrame,
    drivers: pd.DataFrame,
    driver_numbers: list[int],
    total_laps: int,
):
    """Plot tyre stints for selected drivers.

    Args:
        stints: Data with driver_number, compound, stint_number,
            lap_start and lap_end.
        drivers: Driver information with driver_number and full_name.
        driver_numbers: Driver numbers to include.
        total_laps: Number of race laps.

    Returns:
        The Matplotlib figure and axes.
    """
    names = drivers.set_index("driver_number")["full_name"].to_dict()
    tyre_colors = {
        "SOFT": "#e63946",
        "MEDIUM": "#ffd166",
        "HARD": "#d9d9d9",
        "INTERMEDIATE": "#43aa8b",
        "WET": "#4895ef",
    }

    fig, ax = plt.subplots(
        figsize=(12, max(3, len(driver_numbers) * 1.2))
    )

    for row, number in enumerate(driver_numbers):
        driver_stints = stints.loc[
            stints["driver_number"].eq(number)
        ].sort_values("stint_number")

        for _, stint in driver_stints.iterrows():
            start = int(stint["lap_start"])
            end = int(stint["lap_end"])
            length = end - start + 1

            ax.barh(
                row,
                width=length,
                left=start - 0.5,
                height=0.5,
                color=tyre_colors.get(stint["compound"], "lightblue"),
                edgecolor="black",
            )

            ax.text(
                (start + end) / 2,
                row,
                f"{stint['compound']}\n{length} laps",
                ha="center",
                va="center",
                fontsize=9,
            )

    ax.set_yticks(range(len(driver_numbers)))
    ax.set_yticklabels([names[n] for n in driver_numbers])
    ax.invert_yaxis()
    ax.set_xlim(0.5, total_laps + 0.5)
    ax.set_xlabel("Race lap")
    ax.set_title("Monza 2024 — Tyre strategies")
    ax.set_axisbelow(True)
    ax.grid(axis="x", alpha=0.2)

    fig.tight_layout()
    return fig, ax

def plot_all_lap_times(
    laps: pd.DataFrame,
    driver_numbers: list[int],
    driver_names: dict[int, str],
    colors: dict[int, str],
):
    """Plot all recorded lap times for the selected drivers."""
    fig, ax = plt.subplots(figsize=(12, 5))

    for number in driver_numbers:
        driver_laps = laps.loc[
            laps["driver_number"].eq(number)
        ].sort_values("lap_number")

        ax.plot(
            driver_laps["lap_number"],
            driver_laps["lap_duration"],
            label=driver_names[number],
            color=colors[number],
            linewidth=1.5,
        )

    ax.set_title("Monza 2024 — Lap times (all laps)")
    ax.set_xlabel("Lap number")
    ax.set_ylabel("Lap time (seconds)")
    ax.legend()
    ax.grid(alpha=0.3)

    fig.tight_layout()
    return fig, ax