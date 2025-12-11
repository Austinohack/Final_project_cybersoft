# app.py
import streamlit as st
from datetime import date, timedelta
from constants import revenue_daily, revenue_6m, top_products
from feature.utils import check_session, vnd, fmt_table, filter_products
from feature.UI import render_sidebar

# =========================
# CẤU HÌNH & DỮ LIỆU GIẢ
# =========================
st.set_page_config(
    page_title="Bảng điều khiển doanh thu cửa hàng", layout="wide")
st.markdown("""
<style>
div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

check_session()
tong_doanh_thu = 856_000_000
so_don_hang = 1_254
khach_moi = 327
so_sp_ban_ra = 15_430


# 14 ngày gần nhất
days = [date.today() - timedelta(days=13 - i) for i in range(14)]
days_lbl = [d.strftime("%d/%m") for d in days]

revenue_daily = [x * 1_000_000 for x in revenue_daily]


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
months_lbl = [f"{m:02d}/{y}" for (y, m) in ym]
revenue_6m = [x * 1_000_000 for x in revenue_6m]

# =========================
# UI
# =========================
st.title("📊 BẢNG ĐIỀU KHIỂN DOANH THU CỬA HÀNG")
st.caption("Theo dõi doanh thu, đơn hàng, khách hàng và sản phẩm bán chạy.")

render_sidebar(st)

# Thẻ số liệu
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.subheader("Doanh thu tháng này")
    st.metric(label="", value=vnd(tong_doanh_thu), delta="+2.1%")
    st.link_button("Xem chi tiết doanh thu", "#")
with c2:
    st.subheader("Đơn hàng")
    st.metric(label="", value=f"{so_don_hang:,}".replace(",", "."))
    st.link_button("Xem chi tiết đơn hàng", "#")
with c3:
    st.subheader("Khách hàng mới")
    st.metric(label="", value=f"{khach_moi:,}".replace(",", "."), delta="+5%")
    st.link_button("Xem chi tiết KH", "#")
with c4:
    st.subheader("Sản phẩm bán ra")
    st.metric(label="", value=f"{so_sp_ban_ra:,}".replace(",", "."))
    st.link_button("Xem sản phẩm chi tiết", "#")

st.divider()

c1, c2 = st.columns(2)
with c1:
    # Biểu đồ doanh thu theo ngày (Vega-Lite – có sẵn trong Streamlit)
    st.subheader("📈 Biểu đồ doanh thu theo ngày")
    data_daily = [{"Ngày": d, "Doanh thu": v}
                  for d, v in zip(days_lbl, revenue_daily)]
    st.vega_lite_chart(
        data_daily,
        {
            "mark": "area",
            "encoding": {
                "x": {"field": "Ngày", "type": "nominal", "axis": {"labelAngle": 0}},
                "y": {
                    "field": "Doanh thu",
                    "type": "quantitative",
                    "axis": {"title": "VND"},
                },
                "tooltip": [
                    {"field": "Ngày", "type": "nominal"},
                    {"field": "Doanh thu", "type": "quantitative", "format": ",.0f"},
                ],
            },
            "height": 280,
        },
        use_container_width=True,
    )
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
