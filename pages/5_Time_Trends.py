import streamlit as st
import pandas as pd
import altair as alt

st.title("⏱️ Time Trend Analysis")

# =========================
# LOAD DATA
# =========================
df = pd.read_csv("data/clean/movies_clean.csv")

# =========================
# SAFETY CLEANUP
# =========================
for col in ["year", "budget", "gross", "ROI"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["year"])

# =========================
# AGGREGATE BY YEAR
# =========================
trend = (
    df.groupby("year")
    .agg(
        avg_budget=("budget", "mean"),
        avg_gross=("gross", "mean"),
        avg_ROI=("ROI", "mean")
    )
    .reset_index()
)

# =========================
# RESHAPE (BUDGET + GROSS)
# =========================
money_long = trend.melt(
    id_vars="year",
    value_vars=["avg_budget", "avg_gross"],
    var_name="Metric",
    value_name="Amount"
)

money_long["Metric"] = money_long["Metric"].map({
    "avg_budget": "Average Budget",
    "avg_gross": "Average Gross"
})

# =========================
# LAYOUT
# =========================
col1, col2 = st.columns([1.5, 1])

# =========================
# CHART 1: REAL MONEY SCALE
# =========================
with col1:
    money_chart = (
        alt.Chart(money_long)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y(
                "Amount:Q",
                title="USD",
                axis=alt.Axis(format="~s")  # <-- 1e6, 1e7, 1e8
            ),
            color=alt.Color("Metric:N", title="Metric"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("Metric:N", title="Metric"),
                alt.Tooltip("Amount:Q", title="Amount", format=",.0f")
            ]
        )
        .properties(
            title="Average Budget & Gross Over Time",
            height=400
        )
        .interactive()
    )

    st.altair_chart(money_chart, use_container_width=True)
with col2:
    roi_chart = (
        alt.Chart(trend)
        .mark_line(point=True)
        .encode(
            x=alt.X("year:O", title="Year"),
            y=alt.Y("avg_ROI:Q", title="Average ROI"),
            tooltip=[
                alt.Tooltip("year:O", title="Year"),
                alt.Tooltip("avg_ROI:Q", title="Avg ROI", format=".2f")
            ]
        )
        .properties(
            title="Average ROI Over Time",
            height=400
        )
        .interactive()
    )

    st.altair_chart(roi_chart, use_container_width=True)
