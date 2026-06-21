import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import get_high_scoring_venues

st.title("🏟️ Venue Intelligence")

venue_data = get_high_scoring_venues()

venue_df = pd.DataFrame(venue_data)

# -----------------------------
# KPI Cards
# -----------------------------

if not venue_df.empty:

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Highest Scoring Venue",
            venue_df.iloc[0]["venue_name"]
        )

    with c2:
        st.metric(
            "Average Runs",
            round(
                venue_df.iloc[0]["avg_runs_per_match"],
                2
            )
        )

    with c3:
        st.metric(
            "Matches Played",
            venue_df.iloc[0]["matches_played"]
        )

# -----------------------------
# Table
# -----------------------------

st.subheader("Highest Scoring IPL Venues")

st.dataframe(
    venue_df,
    use_container_width=True,
    hide_index=True
)

# -----------------------------
# Average Runs Chart
# -----------------------------

fig = px.bar(
    venue_df,
    x="venue_name",
    y="avg_runs_per_match",
    color="city",
    title="Average Runs Per Match"
)

fig.update_layout(
    xaxis_title="Venue",
    yaxis_title="Average Runs"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Total Runs Chart
# -----------------------------

fig2 = px.scatter(
    venue_df,
    x="matches_played",
    y="total_runs",
    size="avg_runs_per_match",
    hover_name="venue_name",
    title="Venue Scoring Landscape"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)