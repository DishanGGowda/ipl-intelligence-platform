import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import (
    get_top_runs,
    get_top_strike_rates,
    get_player_career,
    get_player_seasons
)

st.title("🏏 Player Explorer")

# ----------------------------------
# Player Search
# ----------------------------------

st.subheader("Player Search")

player_name = st.text_input(
    "Enter Player Name",
    value="V Kohli"
)

if st.button("Search Player"):

    try:

        career = get_player_career(player_name)

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Runs",
            int(career["career_runs"])
        )

        col2.metric(
            "Strike Rate",
            float(career["strike_rate"])
        )

        col3.metric(
            "Highest Score",
            int(career["highest_score"])
        )

        col4.metric(
            "Innings",
            int(career["innings_played"])
        )

        season_df = pd.DataFrame(
            get_player_seasons(player_name)
        )

        fig = px.line(
            season_df,
            x="season_year",
            y="runs",
            markers=True,
            title=f"{player_name} Season Runs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    except Exception:
        st.error("Player not found")

st.divider()

# ----------------------------------
# Top Run Scorers
# ----------------------------------

st.subheader("Top Run Scorers")

runs_df = pd.DataFrame(
    get_top_runs()
)

fig2 = px.bar(
    runs_df.head(10),
    x="player_name",
    y="career_runs"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# ----------------------------------
# Strike Rates
# ----------------------------------

st.subheader("Best Strike Rates")

sr_df = pd.DataFrame(
    get_top_strike_rates()
)

fig3 = px.bar(
    sr_df.head(10),
    x="player_name",
    y="strike_rate"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)