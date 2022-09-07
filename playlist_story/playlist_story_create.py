import main
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
    try:
        counter = 0
        while True:
            searches = main.sp.search(word, type="track", market="US", offset=counter, limit=50)['tracks']['items']
            counter += 50
            for track in searches:
                trackName = track['name'].replace("'","'").replace(".", "").replace(",", "")
                if trackName == word:
                    return (track['name'], track['uri'])
    except exceptions.SpotifyException:
        try:
            counter = 0
            while True:
                searches = main.sp.search(f"track:{word}", type="track", market="US", offset=counter, limit=50)['tracks']['items']
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
    foundWords = {}
    pointer = 0
    while pointer < len(words):
        if len(previousWords) == 5:
            pointer -= 4
            lostWords.append(previousWords[0])
            previousWords = []
            playlistSongs.append(" ")
        previousWords.append(words[pointer])
        phraseToSearch = " ".join(previousWords)
        print(phraseToSearch)
        if phraseToSearch not in foundWords.keys():
            searchedWord = search_for_word(phraseToSearch)
        else:
            searchedWord = foundWords[phraseToSearch]
        if searchedWord:
            playlistSongs.append(searchedWord[1])
            print("found")
            previousWords = []
            foundWords[searchedWord[0]] = searchedWord
        else:
            print("not found")
        pointer += 1

    lostSongCounter = 0
    for song in playlistSongs:
        if song == " ":
            if lostWords[lostSongCounter] not in foundWords.keys():
                songURL = input(f"We couldn't find the word \"{lostWords[lostSongCounter]}\". Please enter a song url for this word. \n")
                tempSongURI = main.sp.track(songURL)['uri']
                tempIndex = playlistSongs.index(song)
                playlistSongs[tempIndex] = tempSongURI
                foundWords[lostWords[lostSongCounter]] = tempSongURI
                lostSongCounter += 1
            else:
                tempIndex = playlistSongs.index(song)
                tempSongURI = foundWords[lostWords[lostSongCounter]]
                playlistSongs[tempIndex] = tempSongURI
                lostSongCounter += 1

    create_playlist(playlistSongs)



create_playlist_story()