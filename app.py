import streamlit as st
import pickle
import pandas as pd
import requests
import gdown
import os

import certifi
import time

import urllib.parse

file_id = "1Cn4c397mIDmhYtonPlwP1WWCX2hq8Dkp"  
output = "similarity.pkl"

if not os.path.exists(output):
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output, quiet=False)

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=9c9e19b7173dd408b9a4cf451147857e&language=en-US"
        response = requests.get(url, timeout=5)
        response.raise_for_status()

        data = response.json()

        if data.get('poster_path'):
            return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except Exception as e:
        print("Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"
    
    
def recommend(movie):
  index = movies[movies['title'] == movie].index[0]
  distances=similarity[index]
  movies_list=sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]


  recommended_movie_names = []
  recommended_movie_posters = []  
  for i in movies_list:
      movie_id = movies.iloc[i[0]].movie_id
      print(movie_id)
      recommended_movie_names.append(movies.iloc[i[0]].title)
    
      recommended_movie_posters.append(fetch_poster(movie_id))
  return recommended_movie_names,recommended_movie_posters  



movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies=pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))
st.title('Movie Recommender System')


selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies['title'].values
)


if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])


