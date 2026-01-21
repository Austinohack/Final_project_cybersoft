def render_sidebar(st):
    with st.sidebar:
        st.page_link("app.py", label="Trang chủ", icon="🏠")
        st.page_link("pages/genre_dashboard.py", label="Genre Management")
        st.page_link("pages/Movie_Management.py", label="Movie CRUD", icon="🎬")


