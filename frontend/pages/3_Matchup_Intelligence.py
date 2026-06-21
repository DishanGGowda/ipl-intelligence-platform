import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import (
    get_top_rivalries,
    get_matchup
)

st.title("⚔️ Matchup Intelligence")

# -----------------------------
# Rivalries Table
# -----------------------------

rivalries = get_top_rivalries()

rivalries_df = pd.DataFrame(rivalries)

st.subheader("Top Batter vs Bowler Rivalries")

st.dataframe(
    rivalries_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Rivalries Chart
# -----------------------------

fig = px.bar(
    rivalries_df.head(10),
    x="batter_name",
    y="runs_scored",
    color="bowler_name",
    title="Top Rivalries By Runs Scored"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Matchup Search
# -----------------------------

st.divider()

st.subheader("Search Matchup")

col1, col2 = st.columns(2)

with col1:
    batter_name = st.text_input(
        "Batter Name",
        value="V Kohli"
    )

with col2:
    bowler_name = st.text_input(
        "Bowler Name",
        value="R Ashwin"
    )

if st.button("Search Matchup"):

    try:

        matchup = get_matchup(
            batter_name,
            bowler_name
        )

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.metric(
                "Runs",
                matchup["runs_scored"]
            )

        with c2:
            st.metric(
                "Balls",
                matchup["balls_faced"]
            )

        with c3:
            st.metric(
                "Dismissals",
                matchup["dismissals"]
            )

        with c4:
            st.metric(
                "Strike Rate",
                matchup["strike_rate"]
            )

        st.success(
            f"{matchup['batter_name']} vs {matchup['bowler_name']}"
        )

    except:

        st.error("Matchup not found")