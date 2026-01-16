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
for col in ["budget", "gross"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["budget", "gross"])

# =========================
# FINANCIAL OVERVIEW
# =========================
st.subheader("💰 Budget Distribution")

budget_hist = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X(
            "budget:Q",
            bin=alt.Bin(maxbins=50),
            title="Budget"
        ),
        y=alt.Y("count()", title="Number of Movies"),
        tooltip=[
            alt.Tooltip("count()", title="Movies")
        ]
    )
    .properties(height=400)
    .interactive()
)

st.altair_chart(budget_hist, use_container_width=True)

# =========================
# BUDGET vs GROSS
# =========================
st.subheader("📈 Budget vs Gross")

budget_gross_scatter = (
    alt.Chart(df)
    .mark_circle(opacity=0.35, size=60)
    .encode(
        x=alt.X("budget:Q", title="Budget"),
        y=alt.Y("gross:Q", title="Gross"),
        tooltip=[
            alt.Tooltip("budget:Q", title="Budget", format=","),
            alt.Tooltip("gross:Q", title="Gross", format=",")
        ]
    )
    .properties(height=400)
    .interactive()
)

st.altair_chart(budget_gross_scatter, use_container_width=True)

import streamlit as st
import pandas as pd

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# =========================
# SAFETY CLEANUP
# =========================
for col in ["ROI", "budget", "gross"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["genre"] = df["genre"].astype(str)
df = df.dropna(subset=["ROI"])

# =========================
# TOP & BOTTOM ROI MOVIES
# =========================

col1, col2 = st.columns(2)

with col1:
    st.subheader("🏆 Top 10 ROI Movies")

    top10 = df.sort_values("ROI", ascending=False).head(10)

    st.dataframe(
        top10[["title", "genre", "ROI", "budget", "gross"]],
        use_container_width=True
    )
with col2:
    st.subheader("💀 Bottom 10 ROI Movies")

    bottom10 = df.sort_values("ROI").head(10)

    st.dataframe(
        bottom10[["title", "genre", "ROI", "budget", "gross"]],
        use_container_width=True
    )

import streamlit as st
import pandas as pd

st.title("🏢 Production Company Performance")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# =========================
# SAFETY CLEANUP
# =========================
if "ROI" in df.columns:
    df["ROI"] = pd.to_numeric(df["ROI"], errors="coerce")

# =========================
# PRODUCTION COMPANY PERFORMANCE
# =========================
if {"company", "ROI", "title"}.issubset(df.columns):

    company_perf = (
        df.groupby("company")
        .agg(
            avg_ROI=("ROI", "mean"),
            movie_count=("title", "count")
        )
        .reset_index()
        .sort_values("avg_ROI", ascending=False)
        .head(10)
    )

    st.dataframe(
        company_perf,
        use_container_width=True,
        hide_index=True
    )

