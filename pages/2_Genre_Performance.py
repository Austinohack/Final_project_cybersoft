import streamlit as st
import pandas as pd
import altair as alt

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="Movies Rating Dashboard",
    layout="wide"
)

st.title("🎬 Movie Ratings Dashboard")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# Safety cleanup
df = df.dropna(subset=["genre", "rating"])
df["genre"] = df["genre"].astype(str)
df["rating"] = df["rating"].astype(str)

# =========================
# PREPARE DATA
# =========================
genre_rating_counts = (
    df.groupby(["genre", "rating"])
      .size()
      .reset_index(name="count")
)

rating_counts = (
    df["rating"]
      .value_counts()
      .reset_index()
)
rating_counts.columns = ["rating", "count"]

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns(2)

# =========================
# GENRE vs RATING (INTERACTIVE STACKED)
# =========================
with col1:
    st.subheader("🎭 Genre vs Rating")

    genre_rating_chart = (
        alt.Chart(genre_rating_counts)
        .mark_bar()
        .encode(
            x=alt.X("genre:N", title="Genre", sort="-y"),
            y=alt.Y("count:Q", title="Count"),
            color=alt.Color("rating:N", title="Rating"),
            tooltip=[
                alt.Tooltip("genre:N", title="Genre"),
                alt.Tooltip("rating:N", title="Rating"),
                alt.Tooltip("count:Q", title="Count")
            ]
        )
        .properties(
            width="container",
            height=400
        )
        .interactive()   # zoom + pan
    )

    st.altair_chart(genre_rating_chart, use_container_width=True)

# =========================
# RATING DISTRIBUTION (INTERACTIVE)
# =========================
with col2:
    st.subheader("📊 Rating Distribution")

    rating_dist_chart = (
        alt.Chart(rating_counts)
        .mark_bar()
        .encode(
            x=alt.X("rating:N", title="Rating", sort="-y"),
            y=alt.Y("count:Q", title="Count"),
            tooltip=[
                alt.Tooltip("rating:N", title="Rating"),
                alt.Tooltip("count:Q", title="Count")
            ]
        )
        .properties(
            width="container",
            height=400
        )
        .interactive()
    )

    st.altair_chart(rating_dist_chart, use_container_width=True)

import streamlit as st
import pandas as pd
import altair as alt

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# =========================
# SAFETY CLEANUP
# =========================
df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce")
df["genre"] = df["genre"].astype(str)

if "rating" in df.columns:
    df["rating"] = df["rating"].astype(str)

df = df.dropna(subset=["ROI", "genre"])

# =========================
# ROI BY GENRE
# =========================
st.subheader("📊 Average ROI by Genre")

roi_genre = (
    df.groupby("genre")["ROI"]
    .mean()
    .reset_index()
    .sort_values("ROI")
)

roi_genre_chart = (
    alt.Chart(roi_genre)
    .mark_bar()
    .encode(
        y=alt.Y("genre:N", sort="-x", title="Genre"),
        x=alt.X("ROI:Q", title="Average ROI"),
        tooltip=[
            alt.Tooltip("genre:N", title="Genre"),
            alt.Tooltip("ROI:Q", title="Average ROI", format=".2f")
        ]
    )
    .properties(height=400)
    .interactive()
)

st.altair_chart(roi_genre_chart, use_container_width=True)

# =========================
# ROI BY RATING
# =========================
if "rating" in df.columns:
    st.subheader("⭐ Average ROI by Rating")

    roi_rating = (
        df.groupby("rating")["ROI"]
        .mean()
        .reset_index()
    )

    roi_rating_chart = (
        alt.Chart(roi_rating)
        .mark_bar()
        .encode(
            x=alt.X("rating:N", title="Rating"),
            y=alt.Y("ROI:Q", title="Average ROI"),
            tooltip=[
                alt.Tooltip("rating:N", title="Rating"),
                alt.Tooltip("ROI:Q", title="Average ROI", format=".2f")
            ]
        )
        .properties(height=400)
        .interactive()
    )

    st.altair_chart(roi_rating_chart, use_container_width=True)
