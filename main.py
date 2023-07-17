
# Importing important libraries

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

# Variables

date = input("Which Year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
endpoint = f"https://www.billboard.com/charts/hot-100/{date}/"

spotify_client_id = os.environ.get("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.environ.get("SPOTIFY_CLIENT_SECRET")

# -------------------x-------------web scraping top 100 songs ----------x----------------x------------------x--------
response = requests.get(url=endpoint)
website = response.text


soup = BeautifulSoup(website, "html.parser")
title = soup.select(selector="li h3", class_="c-title")
song_name = list()
for i in title:
    song_name.append(i.getText().strip())
for i in range(108, 99, -1):
    song_name.remove(song_name[i])




# ------------x------------------authenticationg spotify-------------x----------------------x---------------------x--


auth_manager = SpotifyOAuth(scope="playlist-modify-private", redirect_uri="https://www.google.com", client_id=spotify_client_id, client_secret=spotify_client_secret, show_dialog=True, cache_path="token.txt", username="Aditya Singh")
sp = spotipy.Spotify(auth_manager=auth_manager)
user_id = sp.current_user()["id"]

# ------------x----------------changing songs to corresponding song URI-------------x--------------x------------x------

year = date.split("-")[0]
song_uris = list()
for song in song_name:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"song is not available, skipped")

# creating playlist


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)



# Adding songs to playlist


sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
