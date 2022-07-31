import main
from helper_functions import *
import heapq
# Find popularity of artist and then popularity of track


def get_popularity(tracks, type, playlist_total):
    """
    Get the list of popularities of the tracks or artists in the playlist.

    Args:
        tracks (List<Spotify Tracks>): The list of tracks based on Spotify API Documentation
        type (str): What 
        playlist_total (int): Number of tracks

    Returns:
        popularity (List<Int>): List of popularities of each track or artist
    """
    popularity = []
    if type == 'artist':
        for i in range(playlist_total):
            artists = tracks[i]['track']['artists']
            artists_for_track = []
            for artist in artists:
                artist_id = artist['id']
                artists_for_track.append(main.sp.artist(artist_id)['popularity'])
            popularity.append(artists_for_track)
    elif type == 'track':
        for i in range(playlist_total):
            track = tracks[i]['track']
            popularity.append(track['popularity'])
    return popularity


def sort_by_popularity(pop_type = 'track', sample = None):
    """
    Creates a new playlist with the popularities of the tracks or artists.

    Args:
        pop_type (str, optional): _description_. Defaults to 'track'.
        sample (str, optional): Spotify playlist link parameter allowing for easier testing
    """
    # See if testing playlist URL is set. Otherwise prompt for URL
    if sample == None:
        playlist_id = playlist_to_id(input("Put Playlist URL: "))
    else:
        playlist_id = playlist_to_id(sample)

    playlist_info = main.sp.playlist(playlist_id)
    playlist_name = playlist_info['name']
    playlist_total = playlist_info['tracks']['total']
    temp_total = playlist_total

    # Get all tracks with bunches
    playlist_tracks = []
    counter = 0
    while temp_total > 0:
        playlist_track_info = main.sp.playlist_tracks(playlist_id, limit=100, offset = 100 * counter)
        for track in playlist_track_info['items']:
            playlist_tracks.append(track)
        temp_total -= 100
        counter += 1
    
    popularity = get_popularity(playlist_tracks, pop_type, playlist_total)

    popularity_to_track = {}
    heap_pop = []
    # Create Dict for popularity to link to item
    if pop_type == 'track':
        for i in range(playlist_total):
            if popularity[i] in popularity_to_track.keys():
                popularity_to_track[popularity[i]].append(playlist_tracks[i]['track']['uri'])
            else:
                print(popularity[i])
                popularity_to_track[popularity[i]] = [playlist_tracks[i]['track']['uri']]
            heap_pop.append(popularity[i])
    elif pop_type == 'artist':
        for i in range(playlist_total):
            if max(popularity[i]) in popularity_to_track.keys():
                # print(max(popularity[i]))
                popularity_to_track[max(popularity[i])].append(playlist_tracks[i]['track']['uri'])
            else:
                # print(max(popularity[i]))
                popularity_to_track[max(popularity[i])] = [playlist_tracks[i]['track']['uri']]
            heap_pop.append(max(popularity[i]))
    print(heap_pop)

    # Create Heap
    heapq._heapify_max(heap_pop) 

    sorted_playlist = []
    
    # Items in Order from min to max
    # print("printing max_pop")
    for i in range(playlist_total):
        temp_pop = heapq._heappop_max(heap_pop)
        
        # print(temp_pop)
        max_pop = popularity_to_track[temp_pop].pop()
        sorted_playlist.append(max_pop)
        print(temp_pop)
        print(main.sp.track(max_pop)['name'])

    # Split into batches of 100
    counter = 0
    batched_sorted_playlists = [[]]
    for i in range(playlist_total):
        if i%100 == 0 and i != 0:
            counter +=1
            batched_sorted_playlists.append([sorted_playlist[i]])
        else:
            batched_sorted_playlists[counter].append(sorted_playlist[i])
    # for i in range(len(batched_sorted_playlists)):
    #     print(batched_sorted_playlists[i])
    #     print(len(batched_sorted_playlists[i]))

    # Create New Playlist 
    main.sp.user_playlist_create(main.user_id, f'{playlist_name} Sorted', description=f'Songs from {playlist_name} sorted by popularity of the {pop_type}s.')
    new_playlist_id = main.sp.user_playlists(user=main.user_id)['items'][0]['id']
    for i in range(len(batched_sorted_playlists)):
        # print(batched_sorted_playlists[i])
        main.sp.user_playlist_add_tracks(main.user_id, new_playlist_id, batched_sorted_playlists[i])

# To sort by artist
sort_by_popularity('artist')

# To sort by track
sort_by_popularity('track')
# sort_by_popularity()