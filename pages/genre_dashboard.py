import streamlit as st
import pandas as pd
import glob
import os
import shutil
from feature.UI import render_sidebar
import matplotlib.ticker as mticker
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import altair as alt

st.set_page_config(page_title="Genres Dashboard", layout="wide")
st.title("🎬 Movie Genres Dashboard")

st.success("Dashboard loaded successfully!")

render_sidebar(st)

st.markdown("""
<style>
div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# Paths / diagnostics
script_path = os.path.abspath(__file__)            # path to this script
script_dir = os.path.dirname(script_path)          # .../pages
parent_dir = os.path.dirname(script_dir)           # project root (likely)
cwd = os.path.abspath(os.getcwd())



# Where to look for .xlsx files (search these folders recursively)
search_dirs = [
    script_dir,       # same folder as dashboard (pages/)
    parent_dir,       # project root (one level up)
    cwd               # where Streamlit was started from (could be different)
]

found_files = []
for d in search_dirs:
    if os.path.isdir(d):
        pattern = os.path.join(d, "**", "*.xlsx")
        found_files.extend(glob.glob(pattern, recursive=True))

# Deduplicate and sort
found_files = sorted(list(dict.fromkeys(found_files)))

if not found_files:
    st.error("No .xlsx files were found in the usual locations.")
    st.info("Diagnostics shown in the sidebar. Common fixes below:")
    st.markdown("""
    - Make sure your `Action.xlsx`, etc. are in the project folder or the `pages/` folder.  
    - Ensure filenames end with `.xlsx` (not `.xls` or `.XLSX` with weird characters).  
    - Run Streamlit from the project root: `streamlit run pages/genre_dashboard.py`.  
    - Check file permissions — you should be able to open the file in Excel or a text editor.
    """)
    # show directories listing for extra help
    for d in search_dirs:
        try:
            st.write(f"Contents of `{d}` (top 20):")
            items = os.listdir(d)[:20]
            st.write(items)
        except Exception as e:
            st.write(f"Could not list `{d}`: {e}")
    st.stop()



# Build genre list from filenames (basename without ext)
genre_list = [os.path.splitext(os.path.basename(p))[0] for p in found_files]

selected_genre = st.sidebar.selectbox("Select Genre", genre_list)

# Map selected genre to absolute path
selected_index = genre_list.index(selected_genre)
file_path = found_files[selected_index]


# Try to load the Excel file with robust error reporting
try:
    df = pd.read_excel(file_path)
except Exception as e:
    st.error("Failed to read the Excel file. See details below.")
    st.exception(e)
    # Offer to copy the file into the script directory for testing
    st.markdown("---")
    st.write("If you'd like to copy this file into the `pages/` folder for testing, click below:")
    dest = os.path.join(script_dir, os.path.basename(file_path))
    if os.path.exists(dest):
        st.write(f"`{dest}` already exists.")
    else:
        if st.button("Copy file into pages/ for testing"):
            try:
                shutil.copy2(file_path, dest)
                st.success(f"Copied to `{dest}`. Please refresh the app.")
            except Exception as e2:
                st.error(f"Copy failed: {e2}")
    st.stop()






# ---- Normal dashboard UI ----
st.header(f"📂 {selected_genre} Movies")
st.write(f"`{os.path.basename(file_path)}` (rows: {len(df)})")
st.subheader("📈 Numeric Column Distributions")

c1, c2= st.columns(2)
with c1:
# --- Only 3 visualization options ---
    options = [
        "ROI by year",
        "CPM by year",
        "Engagement by year"
    ]


    choice = st.selectbox("Choose a metric to visualize:", options)

    # Map user choice → actual dataframe column
    metric_map = {
        "ROI by year": "ROI",
        "CPM by year": "CPM",
        "Engagement by year": "Engagement"
    }

    metric_column = metric_map[choice]

    # --- Plot the selected metric ---
    if "year" in df.columns:
        chart_data = df.groupby("year")[metric_column].mean().reset_index()

        st.line_chart(
            chart_data,
            x="year",
            y=metric_column
        )
    else:
        st.error("Column 'year' not found in dataset.")

with c2:
    chart = (
        alt.Chart(df)
        .mark_circle(size=60)
        .encode(
            x=alt.X("score", title="Score"),
            y=alt.Y("budget", title="Budget (VND)"),
            tooltip=[
                alt.Tooltip("name", title="name"),
                alt.Tooltip("score", title="Score"),
                alt.Tooltip("budget", title="Budget (VND)", format=",.0f")  # 👈 format budget nicely
            ]

        )
        .properties(
            title="Correlation Between Budget and Score",
            height=500
        )
        .interactive()
    )

    st.altair_chart(chart, use_container_width=True)

# Infer genre from filename
df["genre"] = selected_genre

st.subheader("📊 ROI Comparison")

# ---------- ROI by Genre (current dataset) ----------
if "ROI" in df.columns:
    roi_genre = (
        df.groupby("genre", as_index=False)["ROI"]
        .mean()
        .sort_values("ROI", ascending=False)
    )

    st.metric(
    label="🎭 Average ROI (This Genre)",
    value=f"{df['ROI'].mean():.2f}"
)
else:
    st.warning("ROI column not found.")





    # plt.show()

st.subheader("📊 Summary Statistics")

num_cols = df.select_dtypes(include="number")
cat_cols = df.select_dtypes(exclude="number")

# --- Numeric Summary ---
st.markdown("### 🔢 Numeric Columns")
if not num_cols.empty:
    st.dataframe(
        num_cols.describe().T,
        use_container_width=True
    )
else:
    st.info("No numeric columns available.")

# --- Categorical Summary ---
st.markdown("### 🏷 Categorical Columns")
if not cat_cols.empty:
    cat_summary = pd.DataFrame({
        "Unique values": cat_cols.nunique(),
        "Most frequent": cat_cols.mode().iloc[0],
        "Missing values": cat_cols.isna().sum()
    })
    st.dataframe(
        cat_summary,
        use_container_width=True
    )
else:
    st.info("No categorical columns available.")



# st.subheader("📋 Data Preview")
st.dataframe(df.head(), hide_index=True)



# Download options
st.subheader("⬇ Download Options")
csv_data = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label=f"Download {selected_genre} as CSV",
    data=csv_data,
    file_name=f"{selected_genre}.csv",
    mime="text/csv"
)
with open(file_path, "rb") as f:
    st.download_button(
        label=f"Download {selected_genre}.xlsx",
        data=f,
        file_name=os.path.basename(file_path),
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )









