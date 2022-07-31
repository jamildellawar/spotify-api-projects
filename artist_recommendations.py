from helper_functions import *
import main

def get_artist_recommendations():
    """
    Will run through 100 recommendation seeds of 100 tracks each that take
    in the top four tracks and the artist wanted. From there, it will create
    a playlist of songs given artist.
    """
    target_artist = [artist_to_id(input("Put artist URL: "))]
    # target_artist = [artist_to_id('https://open.spotify.com/artist/0Y4inQK6OespitzD6ijMwb?si=RZLyTxkXTCurV8db55jR1w')]

    target_artist_name = main.sp.artist(target_artist[0])['name']
    # print(target_artist_name)

    top_twenty_songs = main.sp.current_user_top_tracks()
    top_num_songs_id = []
    for i in range(4):
        top_num_songs_id.append(top_twenty_songs['items'][i]['id'])
    # print(top_num_songs_id)
    # top_five_songs_id = ['52eYVUkFTOVozbVFIaFrnV']

    country = "US"
    limit = 100

    playlist_songs = []

    for x in range(100):
        recommendations = main.sp.recommendations(seed_artists=target_artist, seed_genres=None, seed_tracks=top_num_songs_id, limit=limit, country=country)

        for i in range(100):
            targeted = False
            # print(i)
            for artist in recommendations['tracks'][i]['artists']:
                # print(artist['name'])
                if artist['name'] == target_artist_name:
                    targeted = True
            if targeted and recommendations['tracks'][i] not in playlist_songs:
                playlist_songs.append(recommendations['tracks'][i])




    print("Playlist Songs: \n \n")
    for item in playlist_songs: 
        print(item['name'])

    # Create the new playlist
    main.sp.user_playlist_create(main.user_id, f'Getting to Know {target_artist_name}', description=f'Songs you might like by {target_artist_name} based on your top songs. Created by Jamil Dellawar @jamildellawar on Instagram.')

    # Get that playlist id
    new_playlist_id = main.sp.user_playlists(user=main.user_id)['items'][0]['id']

    playlist_songs_id = []
    # Get all of the IDs of the tracks
    for song in playlist_songs:
        playlist_songs_id.append(song['id'])

    # Add the tracks
    main.sp.user_playlist_add_tracks(main.user_id, new_playlist_id, playlist_songs_id)


get_artist_recommendations()