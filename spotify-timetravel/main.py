import requests
from bs4 import BeautifulSoup
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

'''
SCOPE (PUBLIC/PRIVATE)
- changing to private/public - scope - 'playlist-modify-<state>'
- new token gets generated when you change scope
- playlist that is created as private can't be changed to public.
- user_playlist_create 'Public' param must be equivlent to scope
'''

sp = spotipy.Spotify(
	auth_manager=SpotifyOAuth(
		scope="playlist-modify-public",
		redirect_uri="http://example.com",
		client_id=os.environ["SPOTIPY_CLIENT_ID"],
		client_secret=os.environ["SPOTIPY_CLIENT_SECRET"],
		show_dialog=True,
		cache_path="token.txt"
	)
)
user_id = sp.current_user()["id"]

date = input("Which date do you want to travel to? (YYYY-MM-DD): ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
bb_webpage = response.text
soup = BeautifulSoup(bb_webpage, 'html.parser')

billboard = soup.find_all(name="h3", class_="a-truncate-ellipsis")
song_titles = [song.getText() for song in billboard]
# print(song_titles)

song_uris = []
year = date.split("-")[0]
for song in song_titles:
	result = sp.search(q=f"track:{song} year:{year}", type="track")
	try:
		uri = result["tracks"]["items"][0]["uri"]
		song_uris.append(uri)
	except IndexError:
		print(f"{song} doesn't exist in Spotify. Skipped.")


playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=True)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
