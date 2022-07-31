import spotipy
from spotipy.oauth2 import SpotifyAuthBase, SpotifyClientCredentials, SpotifyOAuth
import os
# pip install python-dotenv
from dotenv import load_dotenv

load_dotenv()

SPOTIPY_CLIENT_ID = os.getenv('CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('CLIENT_SECRET')
# sudo apachectl start
# if error:
# sudo apachectl stop
# or
# npx kill-port <PORT>

# Just getting all of the scopes so I don't have to worry about switching
# between it for different projects
SCOPE_LIST = [
                'user-modify-playback-state', 
                'ugc-image-upload', 
                'user-read-playback-state', 
                'user-read-private', 
                'user-follow-modify', 
                'user-follow-read', 
                'user-library-modify', 
                'user-library-read', 
                'streaming', 
                'user-read-playback-position', 
                'playlist-modify-private', 
                'playlist-read-collaborative', 
                'app-remote-control', 
                'user-read-email', 
                'playlist-read-private', 
                'user-top-read', 
                'playlist-modify-public', 
                'user-read-currently-playing', 
                'user-read-recently-played'
                ]

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope=SCOPE_LIST))

user_id = sp.current_user()['id']

# # Testing (Make sure to be playing something on your Spotify Account)
# current = sp.current_playback()
# print("Currently playing " + current['item']['name'] + " from the album " + current['item']['album']['name'] + " by " + current['item']['album']['artists'][0]['name'])



