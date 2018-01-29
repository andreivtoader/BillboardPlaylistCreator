from gmusicapi import Mobileclient
import billboard
import sys

mobileclient = Mobileclient()
email = sys.argv[1]
password = sys.argv[2]

mobile_loggedin = mobileclient.login(email, password, Mobileclient.FROM_MAC_ADDRESS)

print "Mobile Interface login: " + str(mobile_loggedin)

################# Get Billboard Alternative && Adult Alternative playlist ID's #################

playlists = mobileclient.get_all_playlists()

alternative_playlist_ID = None
adult_alternative_ID = None

for playlist in playlists:
	if playlist['name'] == "Billboard Alternative":
		alternative_playlist_ID = playlist['id']
	if playlist['name'] == "Billboard Adult Alternative":
		adult_alternative_ID = playlist['id']

################# Get Billboard Alternative && Adult Alternative current charts and IDs to add #################

print("Getting Billboard Alternative && Adult Alternative current charts and IDs...")

alternative = billboard.ChartData('alternative-songs')
triple_a = billboard.ChartData('triple-a')

alternative_chart = []
for track in alternative:
    alternative_chart.append(track.artist + ' ' + track.title)

triple_a_chart = []
for track in triple_a:
    triple_a_chart.append(track.artist + ' ' + track.title)

alternative_songsToAdd = []
for track in alternative_chart:
    song = mobileclient.search(track)
    if len(song.get('song_hits')) > 0:
       id = song.get('song_hits')[0].get('track').get('storeId')
       alternative_songsToAdd.append(id)

triplea_songsToAdd = []
for track in triple_a_chart:
    song = mobileclient.search(track)
    if len(song.get('song_hits')) > 0:
       id = song.get('song_hits')[0].get('track').get('storeId')
       triplea_songsToAdd.append(id)

################# Get Google Play Music required playlists contents #################

contents = mobileclient.get_all_user_playlist_contents()

current_billboard_alternative = []
current_billboard_adult_alternative = []

for content in contents:
	for track in content['tracks']:
		if track['playlistId'] == alternative_playlist_ID:
			current_billboard_alternative.append(track['trackId'])
		if track['playlistId'] == adult_alternative_ID:
			current_billboard_adult_alternative.append(track['trackId'])

################# Do the math for Alternative #################

print("Doing math for the Billboard Alternative playlist...")

alternative_songs_to_delete = list(set(current_billboard_alternative).difference(alternative_songsToAdd))
alternative_songs_to_add = list(set(alternative_songsToAdd).difference(current_billboard_alternative))

contents = mobileclient.get_all_user_playlist_contents()

current_billboard_alternative_libraryIds = []
for content in contents:
  for track in content['tracks']:
    if track['playlistId'] == alternative_playlist_ID:
      for song in alternative_songs_to_delete:
        if song == track['trackId']:
          current_billboard_alternative_libraryIds.append(track['id'])  

mobileclient.remove_entries_from_playlist(current_billboard_alternative_libraryIds)
mobileclient.add_songs_to_playlist(alternative_playlist_ID, alternative_songs_to_add)

################# Do the math for Adult Alternative #################

print("Doing math for the Billboard Adult Alternative playlist...")

triplea_songs_to_delete = list(set(current_billboard_adult_alternative).difference(triplea_songsToAdd))
triplea_songs_to_add = list(set(triplea_songsToAdd).difference(current_billboard_adult_alternative))

contents = mobileclient.get_all_user_playlist_contents()

current_billboard_triplea_libraryIds = []
for content in contents:
  for track in content['tracks']:
    if track['playlistId'] == adult_alternative_ID:
      for song in triplea_songs_to_delete:
        if song == track['trackId']:
          current_billboard_triplea_libraryIds.append(track['id'])  

mobileclient.remove_entries_from_playlist(current_billboard_triplea_libraryIds)
mobileclient.add_songs_to_playlist(adult_alternative_ID, triplea_songs_to_add)