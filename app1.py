import streamlit as st
import pickle
import pandas as pd
import requests

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

import gzip
# Load the original file
with open('similarity.pkl', 'rb') as f:
    data = pickle.load(f)

# Compress the file
with gzip.open('similarity.pkl.gz', 'wb') as f:
    pickle.dump(data, f)


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=0b41dc6c757f51c76654c32f78b5169e&language=en-US'
        .format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1: 6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Select Movie:",
    movies['title'].values
)

if st.button('Recommend'):
    name, poster = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.write(name[i])
            st.image(poster[i])
