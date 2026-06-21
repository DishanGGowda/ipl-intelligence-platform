import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import (
    get_top_wickets,
    get_best_economy
)

st.title("🎯 Bowler Explorer")

# -----------------------------
# Top Wicket Takers
# -----------------------------

st.subheader("Top Wicket Takers")

wickets_data = get_top_wickets()

wickets_df = pd.DataFrame(wickets_data)

st.dataframe(
    wickets_df,
    use_container_width=True
)

# KPI Cards

if not wickets_df.empty:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Most Wickets",
            wickets_df.iloc[0]["total_wickets"]
        )

    with c2:
        st.metric(
            "Top Bowler",
            wickets_df.iloc[0]["player_name"]
        )

    with c3:
        st.metric(
            "Spells Bowled",
            wickets_df.iloc[0]["spells_bowled"]
        )

# Chart

fig = px.bar(
    wickets_df.head(10),
    x="player_name",
    y="total_wickets",
    title="Top 10 Wicket Takers"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Best Economy
# -----------------------------

st.subheader("Best Economy Bowlers")

economy_data = get_best_economy()

economy_df = pd.DataFrame(economy_data)

st.dataframe(
    economy_df,
    use_container_width=True
)

fig2 = px.bar(
    economy_df.head(10),
    x="player_name",
    y="economy",
    title="Best Economy Bowlers"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)