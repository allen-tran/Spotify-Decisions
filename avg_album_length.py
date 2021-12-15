import spotipy
import boto3
import csv
from datetime import datetime

from config.playlists import personal_playlists
from tools.playlists import get_artist_from_playlist

spotipy_object = spotipy.Spotify(client_credentials_manager = spotipy.oauth2.SpotifyClientCredentials())
final_data_dictionary = {
    'Year Released': [],
    'Album Length': [],
    'Album Name': [],
    'Artist': []
}

PLAYLIST = "itll_be_january_before_you_know_it"

def gather_data_local():
    with open("personal_albums.csv", 'w') as file:
        header = list(final_data_dictionary.keys())
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        albums_obtained = []
        
        artists = get_artist_from_playlist(personal_playlists()[PLAYLIST])
        
        for artist in list(artists.keys()):
            print(artist)
            artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit = 50)
            for album in artists_albums['items']:
                if 'US' in album['available_markets']:
                    key = album['name'] + album['artists'][0]['name'] + album['release_date'][:4]
                    if key not in albums_obtained:
                        albums_obtained.append(key)
                        album_data = spotipy_object.album(album['uri'])
                        # For every song in the album
                        album_length_ms = 0
                        for song in album_data['tracks']['items']:
                            album_length_ms = song['duration_ms'] + album_length_ms
                        writer.writerow({'Year Released': album_data['release_date'][:4],
                                         'Album Length': album_length_ms,
                                         'Album Name': album_data['name'],
                                         'Artist': album_data['artists'][0]['name']})
                        final_data_dictionary['Year Released'].append(album_data['release_date'][:4])
                        final_data_dictionary['Album Length'].append(album_length_ms)
                        final_data_dictionary['Album Name'].append(album_data['name'])
                        final_data_dictionary['Artist'].append(album_data['artists'][0]['name'])

    return final_data_dictionary

def gather_data():
    # For every artist we're looking for
    with open("/tmp/personal_albums.csv", 'w') as file:
        header = ['Year Released', 'Album Length', 'Album Name', 'Artist']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        artists = get_artist_from_playlist(spotify_playlists()[PLAYLIST])
        for artist in artists.keys():
            artists_albums = spotipy_object.artist_albums(artist, album_type='album', limit=50)
            # For all of their albums
            for album in artists_albums['items']:
                if 'GB' in artists_albums['items'][0]['available_markets']:
                    album_data = spotipy_object.album(album['uri'])
                    # For every song in the album
                    album_length_ms = 0
                    for song in album_data['tracks']['items']:
                        # TODO consider album popularity
                        album_length_ms = song['duration_ms'] + album_length_ms
                    writer.writerow({'Year Released': album_data['release_date'][:4],
                                     'Album Length': album_length_ms,
                                     'Album Name': album_data['name'],
                                     'Artist': album_data['artists'][0]['name']})

if __name__ == "__main__":
    data = gather_data_local()