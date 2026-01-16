import streamlit as st
from feature.utils import load_movies_data
from constants import DATA_URL

st.set_page_config(
    page_title="Movie Performance Dashboard",
    layout="wide"
)
df = load_movies_data("data/clean/movies_clean.csv")

# ===============================
# Header – Slide 1
# ===============================
st.title("🎬 Movie Performance & Market Analysis")
st.subheader("Financial, Audience & Marketing Insights")

st.markdown(
    f"""
    **Data source:** {DATA_URL}  
    **Scope:** Financial performance, audience quality, marketing effectiveness  
    """
)

st.divider()

# ===============================
# Section – Agenda (Slide 2)
# ===============================
st.header("📌 Agenda & Analysis Flow")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        1. Business objectives  
        2. Dataset overview  
        3. Audience & quality  
        4. Financial performance  
        """
    )

with col2:
    st.markdown(
        """
        5. Marketing & engagement  
        6. People & production companies  
        7. Time trends  
        8. Key takeaways & recommendations  
        """
    )

st.info(
    "Each section is presented on a dedicated, standalone page, enabling both detailed exploration and quick insight discovery."
)

st.divider()
