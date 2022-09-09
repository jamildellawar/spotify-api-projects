import main
from spotipy import exceptions


def get_phrase():
    """
    Cleans the phrase so that it can be searched properly.

    Returns:
        phrase (String): cleaned phrased removed of punctuation for searching
    """
    phrase = input("Please type what you'd like the playlist to say: \n").\
        replace("'","'").\
        replace(".", "").\
        replace(",", "").lower()
    return phrase

def create_playlist(playlistSongs):
    """
    Creates a playlist with a list of song URIs

    Args:
        playlistSongs (List<String>): list of song URI strings
    """
    main.sp.user_playlist_create(main.user_id, "Playlist Story", public=False, description="Created by @jamildellawar on Instagram.")
    newPlaylistId = main.sp.user_playlists(user=main.user_id)['items'][0]['id']
    main.sp.playlist_add_items(newPlaylistId, playlistSongs)

def search_for_word(word):
    """
    Searches for a word with Spotify API

    Args:
        word (string): word to be searched

    Returns:
        (songName, songURI) (tuple): returns a tuple of the song name and URI if the word is found. Otherwise it returns None
    """
    try:
        counter = 0
        while True:
            searches = main.sp.search(word, type="track", market="US", offset=counter, limit=50)['tracks']['items']
            counter += 50
            for track in searches:
                trackName = track['name'].replace("'","'").replace(".", "").replace(",", "").lower()
                if trackName == word:
                    return (track['name'], track['uri'])
    except exceptions.SpotifyException:
        try:
            counter = 0
            while True:
                searches = main.sp.search(f"track:{word}", type="track", market="US", offset=counter, limit=50)['tracks']['items']
                counter += 50
                for track in searches:
                    trackName = track['name'].replace("'","'").replace(".", "").replace(",", "").lower()
                    if trackName == word:
                        return (track['name'], track['uri'])
        except exceptions.SpotifyException:
            return None

def create_playlist_story():
    """
    Creates a playlist with song names being a message that you want to type.
    Example: 
    """
    phrase = get_phrase()
    words = phrase.split(" ")
    playlistSongs = []
    previousWords = []
    lostWords = []
    foundWords = {}
    skippedWords = []
    pointer = 0
    while pointer < len(words):
        skip = False
        if len(previousWords) == 5:
            pointer -= 4
            lostWords.append(previousWords[0])
            previousWords = []
            playlistSongs.append(" ")
        previousWords.append(words[pointer])
        phraseToSearch = " ".join(previousWords)
        print(phraseToSearch)

        # Check if the word has been seen before
        if phraseToSearch in foundWords.keys():
            searchedWord = foundWords[phraseToSearch]
        elif phraseToSearch in skippedWords:
            skip = True
        else:
            searchedWord = search_for_word(phraseToSearch)

        
        if searchedWord:
            playlistSongs.append(searchedWord[1])
            print("found")
            previousWords = []
            foundWords[searchedWord[0]] = searchedWord
        elif skip:
            print("not found before")
        else:
            print("not found")
        pointer += 1

    for word in previousWords:
        playlistSongs.append(" ")
        lostWords.append(word)

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
