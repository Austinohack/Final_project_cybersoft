import streamlit as st
from feature.utils import load_movies, create_movie, update_movie, delete_movie

st.title("🎬 Movie CRUD Management")

df = load_movies()

# =========================
# CREATE
# =========================
st.header("➕ Create Movie")

with st.form("create_movie"):
    title = st.text_input("Title")
    rating = st.text_input("Rating (PG, R, PG-13)")
    genre = st.text_input("Genre")
    year = st.number_input("Year", 1900, 2100)
    released = st.text_input("Released (YYYY-MM-DD)")
    score = st.number_input("Score", 0.0, 10.0)
    votes = st.number_input("Votes", 0)
    director = st.text_input("Director")
    writer = st.text_input("Writer")
    star = st.text_input("Star")
    country = st.text_input("Country")
    budget = st.number_input("Budget", 0)
    gross = st.number_input("Gross", 0)
    company = st.text_input("Company")
    runtime = st.number_input("Runtime (min)", 0)
    segment = st.text_input("Segment")

    submit = st.form_submit_button("Create")

if submit:
    try:
        create_movie({
            "title": title,
            "rating": rating,
            "genre": genre,
            "year": year,
            "released": released,
            "score": score,
            "votes": votes,
            "director": director,
            "writer": writer,
            "star": star,
            "country": country,
            "budget": budget,
            "gross": gross,
            "company": company,
            "runtime": runtime,
            "segment": segment,
        })
        st.success("Movie created 🎉")
        

    except ValueError as e:
        st.error(str(e))


# =========================
# UPDATE
# =========================
st.header("✏️ Update Movie")

df = load_movies()

# this creates idx
idx = st.selectbox(
    "Select movie to update",
    df.index.tolist(),
    format_func=lambda i: df.loc[i, "title"]
)


with st.form("update_movie"):
    title = st.text_input("Title", df.loc[idx, "title"])
    rating = st.text_input("Rating", df.loc[idx, "rating"])
    genre = st.text_input("Genre", df.loc[idx, "genre"])
    year = st.number_input("Year", value=int(df.loc[idx, "year"]))
    released = st.text_input("Released", df.loc[idx, "released"])
    score = st.number_input("Score", 0.0, 10.0, value=float(df.loc[idx, "score"]))
    votes = st.number_input("Votes", value=int(df.loc[idx, "votes"]))
    director = st.text_input("Director", df.loc[idx, "director"])
    writer = st.text_input("Writer", df.loc[idx, "writer"])
    star = st.text_input("Star", df.loc[idx, "star"])
    country = st.text_input("Country", df.loc[idx, "country"])
    budget = st.number_input("Budget", value=int(df.loc[idx, "budget"]))
    gross = st.number_input("Gross", value=int(df.loc[idx, "gross"]))
    company = st.text_input("Company", df.loc[idx, "company"])
    runtime = st.number_input("Runtime", value=int(df.loc[idx, "runtime"]))
    segment = st.text_input("Segment", df.loc[idx, "segment"])

    update_clicked = st.form_submit_button("Update")

    if update_clicked:
        update_movie(
            idx,
            {
                "title": title,
                "rating": rating,
                "genre": genre,
                "year": year,
                "released": released,
                "score": score,
                "votes": votes,
                "director": director,
                "writer": writer,
                "star": star,
                "country": country,
                "budget": budget,
                "gross": gross,
                "company": company,
                "runtime": runtime,
                "segment": segment,
            }
        )
        st.success("Movie updated correctly ✅")
        

# =========================
# DELETE
# =========================
st.divider()
st.header("🗑 Delete Movie")

del_idx = st.selectbox(
    "Select movie to delete",
    df.index,
    format_func=lambda i: df.loc[i, "title"],
    key="delete"
)

if st.button("Delete"):
    delete_movie(del_idx)
    st.warning("Movie deleted!")
    
