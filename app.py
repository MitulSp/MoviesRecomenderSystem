import requests
import streamlit as st
import pickle
import pandas as pd
import requests

def recommend(movie):
    movie_index = moviesDF[moviesDF['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_poster = []

    for i in movies_list:
        movieID = moviesDF.iloc[i[0]].movie_id
        # getting poster from TMDB API
        recommended_movies.append(moviesDF.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movieID))

    return recommended_movies, recommended_movies_poster


def fetch_poster(byMovieID):
    response = requests.get('https://api.themoviedb.org/3/movie/{'
                 '}?api_key="Your_API_KEY"&language=en-US'.format(byMovieID))
    data = response.json()

    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

movies_dict = pickle.load(open('movie_dict.pkl','rb'))
moviesDF = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl','rb'))

st.title('Movie Recommender System')

selectedMovie = st.selectbox(
    'Select movie',
    (moviesDF['title'].values)
)

if st.button('Recommend'):
    names, posters = recommend(selectedMovie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.text(names[0])
    with col2:
        st.image(posters[1])
        st.text(names[1])
    with col3:
        st.image(posters[2])
        st.text(names[2])
    with col4:
        st.image(posters[3])
        st.text(names[3])
    with col5:
        st.image(posters[4])
        st.text(names[4])


