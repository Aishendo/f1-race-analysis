"""Streamlit presentation of the Monza 2024 race analysis."""

import matplotlib.pyplot as plt
import streamlit as st

from analysis import match_laps_to_stints, prepare_pace_laps, summarise_pace
from data_io import load_race_table
from plots import (
    plot_all_lap_times,
    plot_hard_tyre_pace,
    plot_lap_time_distributions,
    plot_race_pace,
    plot_teammate_pace,
    plot_tyre_strategies,
)


FOCUS_DRIVERS = [16, 4, 81]
COMPARISON_DRIVERS = [16, 55, 4, 81, 1, 44, 63]
TEAM_PAIRS = {
    "Ferrari": [16, 55],
    "McLaren": [4, 81],
    "Mercedes": [44, 63],
    "Red Bull": [1, 11],
}
COLORS = {
    16: "crimson",
    55: "saddlebrown",
    4: "darkorange",
    81: "royalblue",
    44: "seagreen",
    63: "darkgoldenrod",
    1: "purple",
    11: "slategray",
}


@st.cache_data
def load_inputs():
    """Read the saved OpenF1 tables for the presentation."""
    drivers = load_race_table("drivers")
    drivers["full_name"] = drivers["full_name"].str.title()
    return (
        drivers,
        load_race_table("laps"),
        load_race_table("stints"),
        load_race_table("session_result"),
        load_race_table("race_control"),
    )


def show_plot(plot, *args, caption):
    """Display a figure from plots.py and close it after rendering."""
    fig, _ = plot(*args)
    try:
        st.pyplot(fig)
    finally:
        plt.close(fig)
    st.caption(caption)


def show_table(table, filename):
    """Show rounded values and offer a full-precision CSV."""
    st.dataframe(table.round(3), hide_index=True)
    st.download_button(
        "Download CSV",
        table.to_csv(index=False),
        file_name=filename,
        mime="text/csv",
    )


def show_pace(selected, drivers, names, laps, pace, total_laps):
    st.header("Race pace")
    raw_selected = laps.loc[laps["driver_number"].isin(selected)]
    pace_selected = pace.loc[pace["driver_number"].isin(selected)]

    show_plot(
        plot_all_lap_times, raw_selected, selected, names, COLORS,
        caption="Recorded lap times include the standing start and pit-related laps.",
    )
    show_plot(
        plot_race_pace, pace_selected, drivers, selected, total_laps, COLORS,
        caption="Compare drivers at the same race lap. Gaps show excluded laps.",
    )
    show_plot(
        plot_lap_time_distributions, pace_selected, selected, names, COLORS,
        caption="The box spans the middle 50% of lap times. The line marks the "
        "median and the triangle marks the mean.",
    )


def show_tyres(selected, drivers, names, stints, pace, total_laps):
    st.header("Tyre strategies")
    selected_stints = stints.loc[stints["driver_number"].isin(selected)]
    selected_pace = pace.loc[pace["driver_number"].isin(selected)]

    show_plot(
        plot_tyre_strategies, stints, drivers, selected, total_laps,
        caption="Each bar is a tyre stint. Colour indicates the compound and "
        "bar length shows how many laps the driver completed on that set.",
    )

    stint_table = selected_stints.assign(
        driver=selected_stints["driver_number"].map(names),
        stint_laps=selected_stints["lap_end"] - selected_stints["lap_start"] + 1,
    ).sort_values(["driver", "stint_number"])
    st.dataframe(
        stint_table[[
            "driver", "stint_number", "compound", "lap_start", "lap_end",
            "stint_laps", "tyre_age_at_start",
        ]],
        hide_index=True,
    )

    matched = match_laps_to_stints(selected_pace, selected_stints)
    hard_laps = matched.loc[matched["compound"].eq("HARD")]
    if hard_laps.empty:
        st.info("No filtered laps on Hard tyres for the selected drivers.")
        return

    show_plot(
        plot_hard_tyre_pace, hard_laps, selected, names, COLORS,
        caption="Each line shows one Hard-tyre stint. The horizontal axis is "
        "tyre age at the start of the lap. Traffic and fuel load also affect lap times.",
    )


def show_teammates(drivers, names, pace, total_laps):
    st.header("Driver and teammate comparisons")
    show_plot(
        plot_race_pace, pace, drivers, COMPARISON_DRIVERS, total_laps, COLORS,
        caption="Filtered race pace for seven drivers across four teams.",
    )
    show_plot(
        plot_teammate_pace, pace, TEAM_PAIRS, names, total_laps, COLORS,
        caption="Each panel compares two teammates. The same vertical scale "
        "is used across all four teams.",
    )


def build_overview(results, drivers, pace):
    """Join final classification, driver identities and pace statistics."""
    summary = summarise_pace(pace).rename(columns={"laps": "analysed_laps"})
    return (
        results.merge(
            drivers[["driver_number", "full_name", "team_name"]],
            on="driver_number",
            how="left",
            validate="one_to_one",
        )
        .merge(summary, on="driver_number", how="left", validate="one_to_one")
        .sort_values("position")
    )


def show_overview(overview, laps, pace):
    st.header("Race overview")
    driver_metric, lap_metric, kept_metric = st.columns(3)
    driver_metric.metric("Drivers", len(overview))
    lap_metric.metric("Recorded laps", len(laps))
    kept_metric.metric("Laps retained for pace", len(pace))

    st.subheader("Final classification and filtered pace")
    st.caption("Analysed laps are the laps retained after filtering. Times are in seconds.")
    show_table(
        overview[[
            "position", "full_name", "team_name", "number_of_laps",
            "analysed_laps", "median_seconds", "std_seconds", "fastest_seconds",
            "gap_to_leader", "dnf", "dns", "dsq",
        ]],
        "monza_2024_all_drivers_overview.csv",
    )


def show_findings(overview, race_control):
    st.header("Results and conclusions")
    focus = overview.loc[overview["driver_number"].isin(FOCUS_DRIVERS)]
    show_table(
        focus[[
            "position", "full_name", "number_of_laps", "duration",
            "gap_to_leader", "median_seconds", "fastest_seconds",
        ]],
        "monza_2024_pace_vs_results.csv",
    )

    st.markdown(
        "Piastri had the quickest median filtered lap (**83.468 s**), "
        "followed by Norris (**83.591 s**) and Leclerc (**83.716 s**). "
        "Leclerc won with one stop and a **38-lap final stint on Hard tyres**. "
        "Piastri and Norris stopped twice and finished 2.664 s and 6.153 s behind him."
    )
    st.markdown(
        "The filtered median describes typical lap pace. The final result "
        "includes the start and time spent in the pits. This single-race analysis "
        "cannot establish which strategy was optimal."
    )

    with st.expander("Method, limitations and race control"):
        st.markdown(
            "- Data source: [OpenF1](https://openf1.org/docs/), session `9590`.\n"
            "- The pace filter excludes lap one, pit-out laps, consecutive "
            "laps immediately before a pit-out lap, and missing or non-positive times.\n"
            "- Laps are matched to tyre stints by driver and lap boundaries. "
            "Tyre age is the initial stint age plus laps completed within that stint.\n"
            "- Traffic, fuel load and different completed race distances limit comparisons."
        )

        relevant = (
            race_control["category"].eq("SafetyCar")
            | race_control["message"].str.contains(
                r"\b(?:SAFETY CAR|VSC|RED FLAG)\b", case=False, na=False
            )
            | race_control["flag"].eq("RED")
        )
        events = race_control.loc[
            relevant, ["date", "lap_number", "category", "flag", "message"]
        ].sort_values("date")
        if events.empty:
            st.caption("The filter found no Safety Car, VSC or red-flag messages.")
        else:
            st.dataframe(events, hide_index=True)


def main():
    st.set_page_config(page_title="Monza 2024 | Race Analysis", layout="wide")
    st.title("Monza 2024")
    st.caption("Italian Grand Prix · Race pace and tyre strategies")
    section = st.sidebar.radio(
        "Analysis",
        ["Race overview", "Race pace", "Tyre strategies", "Teammates", "Conclusions"],
    )

    try:
        drivers, laps, stints, results, race_control = load_inputs()
    except FileNotFoundError as exc:
        st.error(str(exc))
        return

    names = drivers.set_index("driver_number")["full_name"].to_dict()
    pace = prepare_pace_laps(laps)
    total_laps = int(laps["lap_number"].max())

    if section == "Race overview":
        show_overview(build_overview(results, drivers, pace), laps, pace)
    elif section == "Conclusions":
        show_findings(build_overview(results, drivers, pace), race_control)
    elif section == "Teammates":
        show_teammates(drivers, names, pace, total_laps)
    else:
        selected = st.sidebar.multiselect(
            "Drivers",
            FOCUS_DRIVERS,
            default=FOCUS_DRIVERS,
            format_func=names.__getitem__,
            key="focus_drivers",
        )
        if not selected:
            st.info("Select at least one driver to show the analysis.")
        elif section == "Race pace":
            show_pace(selected, drivers, names, laps, pace, total_laps)
        else:
            show_tyres(selected, drivers, names, stints, pace, total_laps)


if __name__ == "__main__":
    main()