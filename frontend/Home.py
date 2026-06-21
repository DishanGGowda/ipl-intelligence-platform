import streamlit as st

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="IPL Intelligence Platform",
    page_icon="🏏",
    layout="wide"
)

# =====================================================
# HIDE DEFAULT STREAMLIT ELEMENTS
# =====================================================

st.markdown("""
<style>

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

header {
    visibility: hidden;
}

.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# HERO IMAGE
# =====================================================

st.image(
    "frontend/assets/home_hero.png",
    width="stretch"
)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# PLATFORM STATUS
# =====================================================

st.subheader("🚀 Platform Status")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.success("PostgreSQL Online")

with c2:
    st.success("MinIO Online")

with c3:
    st.success("Airflow Online")

with c4:
    st.success("FastAPI Online")

st.divider()

# =====================================================
# ABOUT PLATFORM
# =====================================================

st.subheader("📊 About Platform")

st.markdown("""
The IPL Intelligence Platform is an end-to-end cricket analytics ecosystem built using modern Data Engineering and Analytics Engineering practices.

### Core Technologies

- Python
- PostgreSQL
- MinIO Data Lake
- Apache Airflow
- dbt
- FastAPI
- Streamlit
- Docker

### Dataset Coverage

- Seasons: 19
- Players: 736
- Venues: 40
- Matches: 1,244
- Matchups: 31,353
""")

st.divider()

# =====================================================
# NAVIGATION
# =====================================================

st.subheader("🎯 Available Analytics")

col1, col2 = st.columns(2)

with col1:

    st.page_link(
        "pages/1_Player_Explorer.py",
        label="👤 Player Explorer",
        icon="👤"
    )

    st.markdown(
        "Career statistics, season trends, strike rates and player intelligence."
    )

    st.markdown("---")

    st.page_link(
        "pages/2_Bowler_Explorer.py",
        label="🎯 Bowler Explorer",
        icon="🎯"
    )

    st.markdown(
        "Top wicket takers, economy leaders and bowling analytics."
    )

    st.markdown("---")

    st.page_link(
        "pages/3_Matchup_Intelligence.py",
        label="⚔️ Matchup Intelligence",
        icon="⚔️"
    )

    st.markdown(
        "Batter vs bowler rivalries, dismissals and matchup intelligence."
    )

with col2:

    st.page_link(
        "pages/4_Venue_Intelligence.py",
        label="🏟️ Venue Intelligence",
        icon="🏟️"
    )

    st.markdown(
        "Venue scoring patterns, ground comparisons and historical trends."
    )

    st.markdown("---")

    st.page_link(
        "pages/5_Season_Analytics.py",
        label="📈 Season Analytics",
        icon="📈"
    )

    st.markdown(
        "Run trends, season evolution and historical IPL analysis."
    )

st.divider()

# =====================================================
# QUICK START
# =====================================================

st.info(
    "Select any analytics module above to start exploring IPL data."
)
