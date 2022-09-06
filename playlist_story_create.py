from xml.sax import ContentHandler
import main
import helper_functions as hf
import time
from spotipy import exceptions


def get_phrase():
    phrase = input("Please type what you'd like the playlist to say: \n").\
        replace("'","'").\
        replace(".", "").\
        replace(",", "")
    return phrase

def create_playlist(playlistSongs):
    main.sp.user_playlist_create(main.user_id, "Playlist Story", public=False, description="Created by @jamildellawar on Instagram.")
    newPlaylistId = main.sp.user_playlists(user=main.user_id)['items'][0]['id']
    main.sp.playlist_add_items(newPlaylistId, playlistSongs)

def search_for_word(word):
    counter = 0
    try:
        while True:
            searches = main.sp.search(word, type="track", market="US", offset=counter, limit=50)['tracks']['items']
            counter += 50
            for track in searches:
                trackName = track['name'].replace("'","'").replace(".", "").replace(",", "")
                if trackName == word:
                    return (track['name'], track['uri'])
    except exceptions.SpotifyException:
        return None

def create_playlist_story():
    phrase = get_phrase()
    words = phrase.split(" ")
    playlistSongs = []
    previousWords = []
    lostWords = []
    pointer = 0
    while pointer < len(words):
        if len(previousWords) == 5:
            pointer -= 3
            lostWords.append(previousWords[0])
            previousWords = []
            playlistSongs.append(" ")
        previousWords.append(words[pointer])
        phraseToSearch = " ".join(previousWords)
        print(phraseToSearch)
        searchedWord = search_for_word(phraseToSearch)
        if searchedWord:
            playlistSongs.append(searchedWord[1])
            print("found")
            previousWords = []
        else:
            print("not found")
        pointer += 1

    lostSongCounter = 0
    for song in playlistSongs:
        if song == " ":
            songURL = input(f"We couldn't find the word \"{lostWords[lostSongCounter]}\". Please enter a song url for this word.")
            lostSongCounter += 1
            tempSongURI = main.sp.track(songURL)['uri']
            playlistSongs.append(tempSongURI)

    create_playlist(playlistSongs)



create_playlist_story()