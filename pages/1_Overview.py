import streamlit as st
from feature.utils import load_movies_data
from constants import DATA_URL

df = load_movies_data("data/clean/movies_clean.csv")

# ===============================
# Section – Business Objectives (Slide 3)
# ===============================
st.header("🎯 Business Objectives")

st.markdown(
    """
    This analysis is designed to answer key business questions using historical movie data:

    - Identify **factors driving movie success**
    - Compare **ROI across genres and countries**
    
    All insights are **data-driven**, focusing on measurable performance indicators.
    """
)

st.divider()


# ===============================
# Section – Dataset Overview (Slide 4)
# ===============================
st.header("🗂️ Dataset Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Movies", f"{len(df)}")

with col2:
    st.metric("Year range:", f"{df["year"].min()} - {df["year"].max()} ")

with col3:
    st.metric("Dimensions", "Genre, Rating, Country")

st.markdown(
    """
    **Key metric groups used throughout the analysis:**

    - **Audience & Quality:** score, votes  
    - **Financial:** budget, gross, ROI  
    - **Marketing & Engagement:** CPM, engagement  

    """
)

st.success(
    "The dataset has been **cleaned, standardized, and structured** into thematic folders"
    "to support both exploratory analysis and dashboard visualization."
)




