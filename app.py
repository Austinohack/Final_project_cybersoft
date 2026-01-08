# app.py
import streamlit as st
from datetime import date, timedelta
from constants import revenue_daily, revenue_6m, top_products
from feature.utils import check_session, vnd, fmt_table, filter_products
from feature.UI import render_sidebar
import pandas as pd
import os
import glob
import shutil




# ===================
# CẤU HÌNH & DỮ LIỆU 
# ===================
st.set_page_config(
    page_title="Sell dashboard movies", layout="wide")
st.markdown("""
<style>
div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)
url = "https://raw.githubusercontent.com/riodev1310/rio_datasets/main/movies.csv"

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

selected_genre = genre_list[0]

# Map selected genre to absolute path
selected_index = genre_list.index(selected_genre)
file_path = found_files[selected_index]

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



# 14 ngày gần nhất
days = []
days_lbl = []

revenue_daily = []


def prev_months(n: int):
    anchor = date.today().replace(day=1)
    out = []
    y, m = anchor.year, anchor.month
    for _ in range(n):
        out.append((y, m))
        m -= 1
        if m == 0:
            m = 12
            y -= 1
    return list(reversed(out))


ym = prev_months(9)
months_lbl = []
revenue_6m = []

# =========================
# UI
# =========================
st.title("📊 SELL DASHBOARD MOVIES")

# ---------------- AUTO YEAR RANGE ----------------

year_min, year_max = None, None

if "year" in df.columns:
    # Force numeric (handles strings, None, NaN)
    year_series = pd.to_numeric(df["year"], errors="coerce")

    if year_series.notna().any():
        year_min = int(year_series.min())
        year_max = int(year_series.max())


if year_min is not None and year_max is not None:
    st.caption(f"From {year_min} to {year_max}")
else:
    st.caption("Year range unavailable")


render_sidebar(st)

# Thẻ số liệu
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.subheader("Doanh thu tháng này")
    # st.metric(label="", value=vnd(tong_doanh_thu), delta="+2.1%")
    st.link_button("Xem chi tiết doanh thu", "#")
with c2:
    st.subheader("Đơn hàng")
    st.link_button("Xem chi tiết đơn hàng", "#")
with c3:
    st.subheader("Khách hàng mới")
    st.link_button("Xem chi tiết KH", "#")
with c4:
    st.subheader("Sản phẩm bán ra")
    st.link_button("Xem sản phẩm chi tiết", "#")

st.divider()

c1, c2 = st.columns(2)
with c1:
    st.subheader("📊 Summary Statistics")
# ---------- ROI by Country ----------
    if "country" in df.columns and "ROI" in df.columns:
        roi_country = (
            df.groupby("country", as_index=False)["ROI"]
            .mean()
            .sort_values("ROI", ascending=False)
        )

        st.markdown("### 🌍 Average ROI by Country")
        st.bar_chart(
            roi_country.set_index("country")["ROI"],y_label= "ROI"
        )
    else:
        st.warning("Country or ROI column not found.")
        
with c2:
    # Biểu đồ doanh thu 6 tháng
    st.subheader("📊 Doanh thu 6 tháng gần nhất")
    data_6m = [{"Tháng": m, "Doanh thu": v}
               for m, v in zip(months_lbl, revenue_6m)]
    st.vega_lite_chart(
        data_6m,
        {
            "mark": "bar",
            "encoding": {
                "x": {"field": "Tháng", "type": "nominal", "axis": {"labelAngle": 0}},
                "y": {"field": "Doanh thu", "type": "quantitative", "axis": {"title": "VND"}},
                "tooltip": [
                    {"field": "Tháng", "type": "nominal"},
                    {"field": "Doanh thu", "type": "quantitative", "format": ",.0f"},
                ],
            },
            "height": 280,
        },
        use_container_width=True,
    )

st.divider()

# Bảng top sản phẩm + ô tìm kiếm
st.subheader("🔥 TOP 5 SẢN PHẨM BÁN CHẠY NHẤT")
keyword = st.text_input("🔎 Tìm sản phẩm:")

filtered = filter_products(top_products, keyword)
st.table(fmt_table(filtered))


