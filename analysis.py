import pandas as pd


def prepare_pace_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Prepare lap data for descriptive race pace comparisons.

    Exclude first laps, pit-out laps, presumed pit-in laps,
    and missing or non-positive lap times.

    Args:
        laps: Lap data containing driver_number, lap_number,
            lap_duration and is_pit_out_lap.

    Returns:
        A sorted, filtered copy with an is_pit_in_lap column.
        Safety car periods and traffic are not filtered.
    """
    prepared = laps.sort_values(
        ["driver_number", "lap_number"]
    ).copy()

    grouped = prepared.groupby("driver_number")

    next_is_pit_out = (
        grouped["is_pit_out_lap"].shift(-1).eq(True)
    )
    next_lap_number = grouped["lap_number"].shift(-1)

    prepared["is_pit_in_lap"] = (
        next_is_pit_out
        & next_lap_number.eq(prepared["lap_number"] + 1)
    )

    keep = (
        prepared["lap_number"].gt(1)
        & prepared["lap_duration"].gt(0)
        & ~prepared["is_pit_out_lap"].eq(True)
        & ~prepared["is_pit_in_lap"]
    )

    return prepared.loc[keep].copy()

def summarise_pace(pace_laps: pd.DataFrame) -> pd.DataFrame:
    """Calculate descriptive lap-time statistics for each driver.

    Args:
        pace_laps: Filtered lap data containing driver_number
            and lap_duration.

    Returns:
        A DataFrame indexed by driver_number with lap counts,
        median, standard deviation and fastest lap time.
    """
    return pace_laps.groupby("driver_number").agg(
        laps=("lap_duration", "size"),
        median_seconds=("lap_duration", "median"),
        std_seconds=("lap_duration", "std"),
        fastest_seconds=("lap_duration", "min"),
    )

def match_laps_to_stints(
    laps: pd.DataFrame, stints: pd.DataFrame
) -> pd.DataFrame:
    """Match laps to tyre stints and calculate tyre age at each lap start."""
    lap_stints = laps.merge(
        stints[[
            "driver_number",
            "stint_number",
            "compound",
            "lap_start",
            "lap_end",
            "tyre_age_at_start",
        ]],
        on="driver_number",
        how="left",
    )

    in_stint = lap_stints["lap_number"].between(
        lap_stints["lap_start"], lap_stints["lap_end"]
    )
    lap_stints = lap_stints.loc[in_stint].copy()

    lap_stints["tyre_age_start_of_lap"] = (
        lap_stints["tyre_age_at_start"]
        + lap_stints["lap_number"]
        - lap_stints["lap_start"]
    )
    return lap_stints