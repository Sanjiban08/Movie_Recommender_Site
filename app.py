import pandas as pd
import streamlit as st
import pickle
import requests


# Function to fetch movie poster URL
def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=7e611464901216c79325a6542e626897&language=en-US'.format(
            movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


# Function to recommend movies
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


# Load movie data and similarity matrix
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Set the title and page configuration
st.set_page_config(page_title='Movie Recommender', page_icon='🎬', layout='wide')

# Set a background color for the entire app
st.markdown(
    """
    <style>
        body {
            background-color: #ffffff;  /* White background color */
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Set the title with a bit of color
st.title('Movie Recommender System 🍿')

# Select a movie from the dropdown
selected_movie_name = st.selectbox('Enter a Movie:', movies['title'].values)

# Display the recommendation button
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create columns for recommended movies
    col1, col2, col3, col4, col5 = st.columns(5)

    # Display recommended movies with styling
    with col1:
        st.image(posters[0], use_column_width=True)
        st.markdown(f"<h2 style='text-align: center; color: #800080; font-size: 20px;'>{names[0]}</h2>",
                    unsafe_allow_html=True)
    with col2:
        st.image(posters[1], use_column_width=True)
        st.markdown(f"<h2 style='text-align: center; color: #800080; font-size: 20px;'>{names[1]}</h2>",
                    unsafe_allow_html=True)
    with col3:
        st.image(posters[2], use_column_width=True)
        st.markdown(f"<h2 style='text-align: center; color: #800080; font-size: 20px;'>{names[2]}</h2>",
                    unsafe_allow_html=True)
    with col4:
        st.image(posters[3], use_column_width=True)
        st.markdown(f"<h2 style='text-align: center; color: #800080; font-size: 20px;'>{names[3]}</h2>",
                    unsafe_allow_html=True)
    with col5:
        st.image(posters[4], use_column_width=True)
        st.markdown(f"<h2 style='text-align: center; color: #800080; font-size: 20px;'>{names[4]}</h2>",
                    unsafe_allow_html=True)
