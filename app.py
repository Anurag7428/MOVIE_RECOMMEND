
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c7ec19ffdd3279641fb606d19ceb9bb1&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=Error"

movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies['title'].values

st.header("🎬 Movie Recommendation System")
st.subheader("Popular Picks")

# Fallback static posters using known TMDB IDs
static_ids = [603, 245891, 27205, 155, 157336]
imageUrls = [fetch_poster(i) for i in static_ids]

cols = st.columns(5)
for idx, col in enumerate(cols):
    if idx < len(imageUrls):
        col.image(imageUrls[idx])

selectvalue = st.selectbox("Select a movie", movies_list)

def recommend(movie):
    if movie not in movies['title'].values:
        raise ValueError(f"Movie '{movie}' not found in dataset.")
    
    index = movies[movies['title'] == movie].index[0]
    distance = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    
    recommended_movies = []
    recommended_posters = []

    for i in distance[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
        
    return recommended_movies, recommended_posters

