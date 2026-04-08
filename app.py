import streamlit as st
import pickle
import pandas as pd
import requests
import time

# -------------------------------
# 🔄 Load Data (Cached)
# -------------------------------
@st.cache_data
def load_data():
    movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)

    top50 = pickle.load(open('top50.pkl', 'rb'))
    return movies, top50

movies, top50 = load_data()

# -------------------------------
# 🎬 Fetch Poster (Cached)
# -------------------------------
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"

    for _ in range(3):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            if data.get('poster_path'):
                return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
            else:
                return "https://via.placeholder.com/500x750?text=No+Image"

        except Exception:
            time.sleep(1)

    return "https://via.placeholder.com/500x750?text=Error"

# -------------------------------
# 🎯 Recommendation Function
# -------------------------------
def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    index = movies[movies['title'] == movie].index[0]

    # Get top 5 from precomputed top50
    similar_movies = top50.get(index, [])[:5]

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in similar_movies:
        movie_id = movies.iloc[i].movie_id
        recommended_movie_names.append(movies.iloc[i].title)
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

# -------------------------------
# 🎨 Streamlit UI
# -------------------------------
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Type or select a movie",
    movies['title'].values
)

if st.button('Show Recommendation'):
    names, posters = recommend(selected_movie)

    if len(names) == 0:
        st.error("Movie not found!")
    else:
        cols = st.columns(5)

        for i in range(len(names)):
            with cols[i]:
                st.image(posters[i])
                st.caption(names[i])