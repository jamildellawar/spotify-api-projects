def playlist_to_id(playlistURL):
    """
    Parameters:
    playlistURL: playlist URL as a String from Spotify

    Returns:
    playlistID: playlist ID as a String from given URL
    """
    playlistID = playlistURL.split("/")[4].split("?")[0]
    # print(playlistID)
    return playlistID


def user_to_id(userURL):
    """
    Parameters:
    userURL: user URL as a String from Spotify

    Returns:
    userID: user ID as a String from given URL
    """
    userID = userURL.split("/")[4].split("=")[1].split("&")[0]
    # print(userID)
    return userID
    
def artist_to_id(artistURL):
    """
    Parameters:
    artistURL: artist URL as a String from Spotify

    Returns:
    artistID: artist ID as a String from given URL
    """
    artistID = artistURL.split("/")[4].split("?")[0]
    # print(artistID)
    return artistID

def get_item_name(item):
    """
    Returns:
    item_name: item name given the item's data structure (Dictionary)
    """
    item_name = item['name']
    return item_name

def get_all_key(original, key):
    """
    Get all 50 items from a Spotify Playlist.

    Parameters:
    original: Dictionary will data
    key: item needed within the Dictionary ('name', 'track', etc.)

    Returns:
    temp: List of needed key items
    """
    temp = []
    for i in range(50):
        temp.append(original[i][key])
    return temp

def print_all(tracks_or_artists, key=None, one=False):
    """
    Used to test what is list of the data set of the API.
    Parameters:
    tracks_or_artists: List of data (tracks or artists info)
    key: if only one specific item is needed to be scene within each index
    one: if only one example is needed
    """
    if one:
        if key == None:
            print(tracks_or_artists[0])
        else:
            print(tracks_or_artists[0][key])
    else:
        if key == None:
            for i in range(50):
                print(tracks_or_artists[i])
        else:
            for i in range(50):
                print(tracks_or_artists[i][key])



# Testing helper functions    
# user_to_id("https://open.spotify.com/user/tkddude0511?si=d6875f6f3a8a4b60&nd=1")
# playlist_to_id("https://open.spotify.com/playlist/5iRCwoD6KS1OrVcH1ZJVxb?si=d7360cd7ca0249fa")
# artist_to_id('https://open.spotify.com/artist/0Y4inQK6OespitzD6ijMwb?si=RZLyTxkXTCurV8db55jR1w')