import json
import streamlit as st
from recommend import df, recommend_movies
from omdb_utils import get_movie_details
from preprocess import tfidf_matrix
from get_for_you_recommendations import get_for_you_recommendations

config = json.load(open("config.json"))
OMDB_API_KEY = config["OMDB_API_KEY"]

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

st.title("🎬 Movie Recommender")

movie_list = sorted(df['title'].dropna().unique())
selected_movie = st.selectbox("🎬 Select a movie:", movie_list)

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("🚀 Recommend Similar Movies"):
    st.session_state.history.append(selected_movie)
    with st.spinner("Finding similar movies..."):
        recommendations = recommend_movies(selected_movie)
        if recommendations is None or recommendations.empty:
            st.warning("Sorry, no recommendations found.")
        else:
            st.success("Top similar movies:")
            for _, row in recommendations.iterrows():
                movie_title = row['title']
                plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

                with st.container():
                    col1, col2 = st.columns([1, 3])
                    with col1:
                        if poster != "N/A":
                            st.image(poster, width=100)
                        else:
                            st.write("❌ No Poster Found")
                    with col2:
                        st.markdown(f"### {movie_title}")
                        st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")

    # ✅ FOR YOU RECOMMENDATIONS — show AFTER a search
    st.subheader("🎯 For You Recommendations")
    for_you = get_for_you_recommendations(df, tfidf_matrix)
    if for_you is None or for_you.empty:
        st.warning("No personalized recommendations yet. Keep exploring movies!")
    else:
        st.success("Movies you might like:")
        for _, row in for_you.iterrows():
            movie_title = row['title']
            plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if poster != "N/A":
                        st.image(poster, width=100)
                    else:
                        st.write("❌ No Poster Found")
                with col2:
                    st.markdown(f"### {movie_title}")
                    st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")



else:
    if st.session_state.history:
        st.subheader("🎯 For You Recommendations")
        for_you = get_for_you_recommendations(df, tfidf_matrix)
        if for_you is None or for_you.empty:
            st.warning("No personalized recommendations yet. Keep exploring movies!")
        else:
            st.success("Movies you might like:")
        for _, row in for_you.iterrows():
            movie_title = row['title']
            plot, poster = get_movie_details(movie_title, OMDB_API_KEY)

            with st.container():
                col1, col2 = st.columns([1, 3])
                with col1:
                    if poster != "N/A":
                        st.image(poster, width=100)
                    else:
                        st.write("❌ No Poster Found")
                with col2:
                    st.markdown(f"### {movie_title}")
                    st.markdown(f"*{plot}*" if plot != "N/A" else "_Plot not available_")

