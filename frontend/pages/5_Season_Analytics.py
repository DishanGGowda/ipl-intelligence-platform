import streamlit as st
import pandas as pd
import plotly.express as px
import requests

BASE_URL = "http://localhost:8001/api/v1"

st.title("📈 Season Analytics")

# ----------------------------------
# Load Data
# ----------------------------------

highest_scoring = requests.get(
    f"{BASE_URL}/seasons/highest-scoring"
).json()

run_trends = requests.get(
    f"{BASE_URL}/seasons/run-trends"
).json()

highest_df = pd.DataFrame(highest_scoring)
trends_df = pd.DataFrame(run_trends)

# ----------------------------------
# KPI Cards
# ----------------------------------

if not highest_df.empty:

    top_season = highest_df.iloc[0]

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Highest Scoring Season",
            int(top_season["season_year"])
        )

    with c2:
        st.metric(
            "Total Runs",
            int(top_season["total_runs"])
        )

    with c3:
        st.metric(
            "Avg Runs / Match",
            round(
                float(top_season["avg_runs_per_match"]),
                2
            )
        )

# ----------------------------------
# Highest Scoring Seasons
# ----------------------------------

st.subheader("Highest Scoring IPL Seasons")

st.dataframe(
    highest_df,
    use_container_width=True,
    hide_index=True
)

fig1 = px.bar(
    highest_df,
    x="season_year",
    y="total_runs",
    title="Highest Scoring Seasons"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ----------------------------------
# Run Trends
# ----------------------------------

st.subheader("Season Run Trends")

fig2 = px.line(
    trends_df,
    x="season_year",
    y="total_runs",
    markers=True,
    title="IPL Run Trends Over Time"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ----------------------------------
# Season Lookup
# ----------------------------------

st.subheader("Season Lookup")

season_year = st.number_input(
    "Enter Season Year",
    min_value=2008,
    max_value=2026,
    value=2026,
    step=1
)

if st.button("Get Season Summary"):

    season = requests.get(
        f"{BASE_URL}/seasons/{season_year}"
    ).json()

    if "message" not in season:

        c1, c2, c3 = st.columns(3)

        with c1:
            st.metric(
                "Matches Played",
                season["matches_played"]
            )

        with c2:
            st.metric(
                "Total Runs",
                int(season["total_runs"])
            )

        with c3:
            st.metric(
                "Avg Runs / Match",
                round(
                    float(season["avg_runs_per_match"]),
                    2
                )
            )

    else:
        st.error("Season not found")