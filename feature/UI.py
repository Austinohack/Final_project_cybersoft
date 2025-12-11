def render_sidebar(st):
    with st.sidebar:
        st.page_link("app.py", label="Trang chủ", icon="🏠")
        st.page_link("pages/add_product.py", label="Thêm sản phẩm")
