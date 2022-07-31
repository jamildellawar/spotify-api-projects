import main as m
import helper_functions as hf
import random as r
import time

playlist_id = hf.playlist_to_id('https://open.spotify.com/playlist/7KPDLvwpjgQdeqhn68GzoM?si=178ef4ab815342aa')
name = m.sp.current_user()['display_name']

# DO BUNCHES
tracks_info = m.sp.playlist_tracks(playlist_id=playlist_id)
total = tracks_info['total']
temp_total = total
tracks = tracks_info['items']
offset = 0
while temp_total > 100:
    offset += 100
    temp_tracks = m.sp.playlist_tracks(playlist_id=playlist_id, offset=offset,limit=100)
    for temp_track in temp_tracks['items']:
        tracks.append(temp_track)
    temp_total -= 100

# Pick the Valentines track
rand_track = tracks_info['items'][r.randint(0, total-1)]['track']
track_name = rand_track['name']
track_id = [rand_track['id']]
genre = ['romance']

# Have artists' names typed out
artists_typed = ""
artist_ids = []
for artist in rand_track['artists']:
    artist_ids.append(artist['id'])
if len(artist_ids) > 3:
    artist_ids = artist_ids[:2]
if len(rand_track['artists']) == 1:
    artists_typed = rand_track['artists'][0]['name']
elif len(rand_track['artists']) == 2:
    artists_typed = rand_track['artists'][0]['name'] + " and " + rand_track['artists'][1]['name']
else:
    for artist in rand_track['artists'][:-1]:
        artists_typed += artist['name'] + ', ' 
    artists_typed += "and " + artist['name'][-1]
chosen_track_uri = rand_track['uri']


# Rolling animation in terminal
for i in range(50):
    temp_rand_track = tracks_info['items'][r.randint(0, total-1)]['track']
    print(temp_rand_track['name'])
    if i < 16:
        time.sleep(.03)
    elif i < 25:
        time.sleep(.05)
    elif i < 40:
        time.sleep(.15)
    elif i < 48:
        time.sleep(.25)
    if i == 48:
        time.sleep(.5)
    if i == 49:
        time.sleep(1)
    if i == 50:
        time.sleep(2)

print("The track chosen is... ")
time.sleep(1)
print("...")
time.sleep(1)
print(track_name + " by " + artists_typed + "!")

# Get 50 songs to recommend based on track and romance genre
rec_tracks_info = m.sp.recommendations(seed_tracks=track_id, seed_genres=genre, seed_artists=artist_ids, limit=50, country="US")
rec_tracks = rec_tracks_info['tracks']
rec_tracks_uri = []
for track in rec_tracks:
    rec_tracks_uri.append(track['uri'])

# Create playlist with recommendations and first track as chosen track
m.sp.user_playlist_create(m.user_id, f'{name}\'s Valentine\'s Playlist', description=f'The song {track_name} sums up your Valentines. I hope that\'s what you wanted!',)
new_playlist_id = m.sp.user_playlists(user=m.user_id)['items'][0]['id']
m.sp.user_playlist_add_tracks(m.user_id, new_playlist_id, [chosen_track_uri])
m.sp.user_playlist_add_tracks(m.user_id, new_playlist_id, rec_tracks_uri)
time.sleep(1)
print("Check out your new playlist!")
print("(You may need to reload Spotify for it to show up.)")