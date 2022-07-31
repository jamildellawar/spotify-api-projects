import helper_functions as hf
import random as r
from datetime import datetime
import main

def find_time_left(end_hour, end_minute):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S").split(":")
    # Time left in seconds
    time_left = 0

    # Turn hours to minutes
    hours_left = end_hour - int(current_time[0])
    time_left += hours_left * 60

    # Turn minutes into seconds
    minutes_left = end_minute - int(current_time[1])
    time_left += minutes_left
    time_left *= 60

    time_left -= int(current_time[2])

    # To give a 15 second buffer
    time_left += 15
    return time_left


def findBestTracklist(tracks, sum):
    # To store current sum and
    # max sum of subarrays
    curr_sum = tracks[0][0]
    curr_tracks = [tracks[0][1]]
    best_tracklist = []
    max_sum = 0
    start = 0

    # To find max_sum less than sum
    for i in range(len(tracks)):
         
        # Update max_sum if it becomes
        # greater than curr_sum
        if (curr_sum <= sum):
            if max_sum <= curr_sum:
                max_sum = curr_sum
                best_tracklist = []
                for _ in curr_tracks:
                    best_tracklist.append(_)

        # If curr_sum becomes greater than sum
        # subtract starting elements of array
        while (curr_sum + tracks[i][0] > sum and start < i):
            curr_sum -= tracks[start][0]
            curr_tracks.remove(tracks[start][1])
            start += 1

        # Add elements to curr_sum
        curr_sum += tracks[i][0]
        curr_tracks.append(tracks[i][1])
 

    # Adding an extra check for last subarray
    if (curr_sum <= sum):
        if max_sum <= curr_sum:
            max_sum = curr_sum
            for _ in curr_tracks:
                best_tracklist.append(_)
    return (max_sum, best_tracklist)


temp_now = datetime.now()
current_time = temp_now.strftime("%H:%M:%S")
current_time_split = current_time.split(":")
print(current_time)

# Time until the alarm
end_time = input("What time do you want to stop music? ")
hour_seconds = end_time.split(":")
hour = int(hour_seconds[0])
if int(current_time_split[0]) > 12:
    hour += 12
minute = int(float(hour_seconds[1]))


time_left = find_time_left(hour, minute)
chosen_end_track = main.sp.track('https://open.spotify.com/track/3zuK7lJhlrXyuDcLsYMNeo?si=02b64af3fea344dc')
end_song_uri = chosen_end_track['uri']
end_song_length = chosen_end_track['duration_ms']/1000
playlist_tracks = main.sp.playlist("https://open.spotify.com/playlist/4pCotpAODf5rW3CFYOSMUn?si=6f0dd61e18f14462")['tracks']['items']
r.shuffle(playlist_tracks)
playlist_track_lengths = []

for song in playlist_tracks:
    if song['track']['uri'] != end_song_uri:
        playlist_track_lengths.append([song['track']['duration_ms']/1000, song['track']['uri']])

print("Seconds left: " + str(time_left))

best = findBestTracklist(playlist_track_lengths, time_left-end_song_length)

best[1].append(end_song_uri)
print(best)
total = 0
for song in best[1]:
    total += main.sp.track(song)['duration_ms']/1000

print(total)
total=0

for uri in best[1]:
    total += main.sp.track(uri)['duration_ms']/1000
    main.sp.add_to_queue(uri)

main.sp.pause_playback()
main.sp.volume(100)
main.sp.next_track()
print(total)


