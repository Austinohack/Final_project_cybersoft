import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Audience Engagement", layout="wide")
st.title("🎥 Audience Engagement")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# Safety cleanup
df = df.dropna(subset=["genre", "rating", "score"])
df["genre"] = df["genre"].astype(str)
df["rating"] = df["rating"].astype(str)




col1, col2 = st.columns(2)

with col1:
# =========================
# AVERAGE SCORE BY GENRE
# =========================
    if {"genre", "score"}.issubset(df.columns):

        score_genre = (
                df.groupby("genre")["score"]
                .mean()
                .reset_index()
                .sort_values("score")
            )

    st.altair_chart(
            alt.Chart(score_genre)
            .mark_bar()
            .encode(
                y=alt.Y("genre:N", sort="-x", title="Genre"),
                x=alt.X("score:Q", title="Average Score"),
                tooltip=[
                    alt.Tooltip("genre:N", title="Genre"),
                    alt.Tooltip("score:Q", title="Average Score", format=".2f")
                ]
            )
            .properties(title="Average Score by Genre", height=400)
            .interactive(),
            use_container_width=True
        )

    # =========================
    # AVERAGE SCORE BY RATING
    # =========================
    if {"rating", "score"}.issubset(df.columns):

        score_rating = (
            df.groupby("rating")["score"]
            .mean()
            .reset_index()
        )

        st.altair_chart(
            alt.Chart(score_rating)
            .mark_bar()
            .encode(
                x=alt.X("rating:N", title="Rating"),
                y=alt.Y("score:Q", title="Average Score"),
                tooltip=[
                    alt.Tooltip("rating:N", title="Rating"),
                    alt.Tooltip("score:Q", title="Average Score", format=".2f")
                ]
            )
            .properties(title="Average Score by Rating", height=400)
            .interactive(),
            use_container_width=True
        )


# =========================
# LOAD DATA (if not already loaded)
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# Safety cleanup
df = df.dropna(subset=["votes", "score", "genre"])
df["votes"] = pd.to_numeric(df["votes"], errors="coerce")
df["score"] = pd.to_numeric(df["score"], errors="coerce")
df["genre"] = df["genre"].astype(str)

with col2:
    # =========================
    # VOTES vs SCORE (SCATTER)
    # =========================
    if {"votes", "score"}.issubset(df.columns):

        scatter_chart = (
            alt.Chart(df)
            .mark_circle(opacity=0.4)
            .encode(
                x=alt.X("votes:Q", title="Votes", scale=alt.Scale(type="log")),
                y=alt.Y("score:Q", title="Score"),
                tooltip=[
                    alt.Tooltip("votes:Q", title="Votes", format=","),
                    alt.Tooltip("score:Q", title="Score", format=".2f"),
                    alt.Tooltip("genre:N", title="Genre")
                ]
            )
            .properties(
                title="Votes vs Score",
                height=400
            )
            .interactive()
        )

        st.altair_chart(scatter_chart, use_container_width=True)

    # =========================
    # TOTAL VOTES BY GENRE (BARH)
    # =========================
    if {"genre", "votes"}.issubset(df.columns):

        votes_genre = (
            df.groupby("genre")["votes"]
            .sum()
            .reset_index()
            .sort_values("votes")
        )

        votes_genre_chart = (
            alt.Chart(votes_genre)
            .mark_bar()
            .encode(
                y=alt.Y("genre:N", sort="-x", title="Genre"),
                x=alt.X("votes:Q", title="Total Votes"),
                tooltip=[
                    alt.Tooltip("genre:N", title="Genre"),
                    alt.Tooltip("votes:Q", title="Total Votes", format=",")
                ]
            )
            .properties(
                title="Total Votes by Genre",
                height=400
            )
            .interactive()
        )

        st.altair_chart(votes_genre_chart, use_container_width=True)

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
if "ROI" in df.columns:
    df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce")

if "gross" in df.columns:
    df["gross"] = pd.to_numeric(df["gross"], errors="coerce")

df = df.dropna(subset=["ROI", "gross"], how="all")

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
if "ROI" in df.columns:
    df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce")

if "gross" in df.columns:
    df["gross"] = pd.to_numeric(df["gross"], errors="coerce")

df = df.dropna(subset=["ROI", "gross"], how="all")

import streamlit as st
import pandas as pd

st.title("🎬 Director & ⭐ Star Impact")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# =========================
# SAFETY CLEANUP
# =========================
if "ROI" in df.columns:
    df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce")

if "gross" in df.columns:
    df["gross"] = pd.to_numeric(df["gross"], errors="coerce")

# =========================
# DIRECTOR IMPACT (AVG ROI)
# =========================
if {"director", "ROI"}.issubset(df.columns):

    director_roi = (
        df.groupby("director")["ROI"]
        .mean()
        .reset_index()
        .sort_values("ROI", ascending=False)
        .head(10)
    )

    st.subheader("Top 10 Directors by Average ROI")
    st.dataframe(
        director_roi,
        use_container_width=True,
        hide_index=True
    )

# =========================
# STAR IMPACT (AVG GROSS)
# =========================
if {"star", "gross"}.issubset(df.columns):

    star_gross = (
        df.groupby("star")["gross"]
        .mean()
        .reset_index()
        .sort_values("gross", ascending=False)
        .head(10)
    )

    st.subheader("Top 10 Stars by Average Gross")
    st.dataframe(
        star_gross,
        use_container_width=True,
        hide_index=True
    )


