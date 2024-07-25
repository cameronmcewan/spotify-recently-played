import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

# load env variables from .env file
load_dotenv()

# Spotify API Credentials
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')


# Scope required to read recnelty played tracks
scope = 'user-read-recently-played'

#Set up Spotify authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=scope
))

st.title("Spotify Recently Played Tracks")

if st.button("Get Recently Played Tracks"):
    results = sp.current_user_recently_played(limit=10)
    if results is not None:
        num_columns = 5
        cols = st.columns(num_columns)

        for idx, item in enumerate(results['items']):
            track = item['track']
            track_name = track['name']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            album_art = track['album']['images'][0]['url']
            played_at = item['played_at']

            with cols[idx % num_columns]:
                st.image(album_art, use_column_width=True)
                st.write(f"**Track {idx+1}:**")
                st.write(f"**Name:** {track_name}")
                st.write(f"**Artist:** {artist_name}")
                st.write(f"**Album:** {album_name}")
                st.write(f"**Played at:** {played_at}")
                st.write("---")
    else:
        st.write("Failed to fetch recently played tracks.")     

st.write("Click the button above to fetch your recently played tracks from your Spotify account.")
       
