import streamlit as st
from feature.utils import check_session, vnd, filter_products, fmt_table
from feature.UI import render_sidebar


st.set_page_config(page_title="Thêm mặt hàng", layout="wide")
st.title("Add product")
st.markdown("""
<style>
div[data-testid="stSidebarNav"] { display: none; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DỮ LIỆU & TRỢ GIÚP
# -----------------------------
check_session()


render_sidebar(st)
# -----------------------------
# HEADER
# -----------------------------
st.subheader("🔥 TOP 5 SẢN PHẨM BÁN CHẠY NHẤT")

# -----------------------------
# FORM THÊM HÀNG (trong expander)
# -----------------------------
with st.expander("➕ Thêm mặt hàng mới", expanded=True):
    name = st.text_input("Tên sản phẩm mới", placeholder="Nhập tên…")
    qty = st.number_input("Số lượng bán", min_value=0, step=1, value=0)
    category = st.selectbox(
        "Danh mục", ["Quần áo", "Giày dép", "Phụ kiện", "Điện tử", "Khác"])
    price = st.number_input("Giá bán (VND)", min_value=0,
                            step=1000, value=250_000, help="Ví dụ: 250000 VND")
    status = st.selectbox(
        "Tình trạng", ["Còn hàng", "Sắp hết hàng", "Hết hàng"])

    col_btn = st.columns([1, 6])[0]
    with col_btn:
        if st.button("Thêm mặt hàng", type="primary", use_container_width=True, disabled=(not name or price <= 0)):
            item = {
                "Tên sản phẩm": name.strip(),
                "Số lượng bán": int(qty),
                "Danh mục": category,
                "Giá bán (VND)": int(price),
                "Tình trạng": status,
            }
            st.session_state.products.append(item)
            st.success(
                f"Đã thêm: **{item['Tên sản phẩm']}** — {vnd(item['Giá bán (VND)'])}")

# -----------------------------
# TÌM KIẾM + BẢNG
# -----------------------------
st.text_input("🔎 Tìm sản phẩm:", key="search_product",
              placeholder="Nhập tên sản phẩm…")

filtered = filter_products(st.session_state.products,
                           st.session_state.search_product)
st.table(fmt_table(filtered))
