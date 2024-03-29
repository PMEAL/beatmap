import streamlit as st
from matplotlib import rcParams
from static import altair_plots as plots
from static import texts, utils

import beatmap as bt

state = st.session_state
st.set_page_config(
    page_title="BEaTmap Analysis",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto"
)
rcParams["axes.formatter.limits"] = 0, 0
rcParams["font.sans-serif"] = [
    "Lucida Sans Unicode",
    "Lucida Grande",
    "DejaVu Sans",
    "Tahoma"
]


def main():
    utils.fill_sidebar()

    st.markdown("# BEaTmap Analysis")

    # Bypass calculations if no data is found
    if "bet_results" not in state:
        st.error("You need to upload isotherm data first!")
        return

    st.markdown("## BET model assumptions")
    with st.expander("Click to expand!"):
        if "checks" in state:
            state.check_values = [value for value in state.checks]
        else:
            state.check_values = [True, True, True, False, True]
        state.checks = [
            st.checkbox(label=texts.checks[i], value=state.check_values[i])
            for i in range(5)
        ]
        label = "Minimum number of points"
        if "min_num_points" not in state:
            state.min_num_points = 5
        st.slider(label=label, min_value=2, max_value=27, key="min_num_points")

        state.mask_results = bt.core.rouq_mask(
            intercept=state.bet_results.intercept,
            iso_df=state.bet_results.iso_df,
            nm=state.bet_results.nm,
            slope=state.bet_results.slope,
            enforce_y_intercept_positive=state.checks[0],
            enforce_pressure_increasing=state.checks[1],
            enforce_absorbed_amount=state.checks[2],
            enforce_relative_pressure=state.checks[3],
            enforce_enough_datapoints=state.checks[4],
            min_num_points=state.min_num_points,
        )

        if state.mask_results.mask.all():
            msg = "Relative pressure ranges not valid. Adjust settings to proceed."
            st.error(msg)
            return

    st.markdown("## Analysis results")
    tabs = st.tabs(["SSA Heatmap", "SSA Error Heatmap"])

    with tabs[0]:
        # st.markdown(r"BET Specific Surface Area \[$\frac{m^2}{g}$\]")
        # st.markdown(r"## Specific surface area heatmap")
        st.markdown(texts.ssa_instruction)
        plots.plot_ssa_heatmap(state.bet_results, state.mask_results)

    with tabs[1]:
        st.markdown(texts.err_instruction)
        plots.plot_err_heatmap(state.bet_results, state.mask_results)

    # Track if BET has been performed
    state.bet_analysis = True


if __name__ == "__main__":
    main()
