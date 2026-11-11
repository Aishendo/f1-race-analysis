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