import marimo

__generated_with = "0.9.1"
app = marimo.App(width="medium")


@app.cell
def __():
    import pandas as pd
    import spotipy
    from spotipy.oauth2 import SpotifyClientCredentials
    import time
    import logging
    return SpotifyClientCredentials, logging, pd, spotipy, time


app._unparsable_cell(
    r"""
    SPOTIPY_CLIENT_ID = #Use your own
    SPOTIPY_CLIENT_SECRET = #Use your own
    """,
    name="__"
)


@app.cell
def __(
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SpotifyClientCredentials,
    logging,
    pd,
    spotipy,
    time,
):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_spotify_data(artist, title):
        logging.info(f"Searching Spotify for '{title}' by '{artist}'")
        query = f"artist:{artist} track:{title}"
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            album = track['album']
            artist = track['artists'][0]

            # Track details
            track_name = track['name']
            track_id = track['id']
            popularity = track['popularity']
            duration = track['duration_ms']
            explicit = track['explicit']
            preview_url = track['preview_url']
            external_urls_track = track['external_urls']['spotify']

            # Album details
            album_name = album['name']
            album_id = album['id']
            album_release_date = album['release_date']
            album_type = album['album_type']
            total_tracks = album['total_tracks']
            album_images = album['images']
            album_external_url = album['external_urls']['spotify']

            # Artist details
            artist_name = artist['name']
            artist_id = artist['id']
            #artist_popularity = artist['popularity']
            #artist_genres = artist['genres']
            artist_external_url = artist['external_urls']['spotify']

            # Fetch audio features
            audio_features = sp.audio_features(track_id)[0]  # Get audio features for the track
            danceability = audio_features['danceability']
            energy = audio_features['energy']
            key = audio_features['key']
            loudness = audio_features['loudness']
            mode = audio_features['mode']
            speechiness = audio_features['speechiness']
            acousticness = audio_features['acousticness']
            instrumentalness = audio_features['instrumentalness']
            liveness = audio_features['liveness']
            valence = audio_features['valence']
            tempo = audio_features['tempo']
            time_signature = audio_features['time_signature']

            logging.info(f"Found data for '{title}': Track: {track_name}, Album: {album_name}, Artist: {artist_name}")

            return {
                "track_name": track_name,
                "track_id": track_id,
                "popularity": popularity,
                "duration": duration,
                "explicit": explicit,
                "preview_url": preview_url,
                "external_urls_track": external_urls_track,
                "album_name": album_name,
                "album_id": album_id,
                "album_release_date": album_release_date,
                "album_type": album_type,
                "total_tracks": total_tracks,
                "album_images": album_images,
                "album_external_url": album_external_url,
                "artist_name": artist_name,
                "artist_id": artist_id,
                #"artist_popularity": artist_popularity,
                #"artist_genres": artist_genres,
                "artist_external_url": artist_external_url,
                "danceability": danceability,
                "energy": energy,
                "key": key,
                "loudness": loudness,
                "mode": mode,
                "speechiness": speechiness,
                "acousticness": acousticness,
                "instrumentalness": instrumentalness,
                "liveness": liveness,
                "valence": valence,
                "tempo": tempo,
                "time_signature": time_signature
            }

        logging.warning(f"No results found for '{title}' by '{artist}'.")
        return None

    def main(input_csv, output_csv):
        # Read input CSV
        df = pd.read_csv(input_csv)

        # Create new columns for output data
        df['Spotify Track Name'] = None
        df['Spotify Track ID'] = None
        df['Spotify Popularity'] = None
        df['Spotify Duration (ms)'] = None
        df['Spotify Explicit'] = None
        df['Spotify Preview URL'] = None
        df['Spotify External Track URL'] = None
        df['Spotify Album Name'] = None
        df['Spotify Album ID'] = None
        df['Spotify Album Release Date'] = None
        df['Spotify Album Type'] = None
        df['Spotify Total Tracks'] = None
        df['Spotify Album Images'] = None
        df['Spotify Album External URL'] = None
        df['Spotify Artist Name'] = None
        df['Spotify Artist ID'] = None
        df['Spotify Artist External URL'] = None
        df['Spotify Danceability'] = None
        df['Spotify Energy'] = None
        df['Spotify Key'] = None
        df['Spotify Loudness'] = None
        df['Spotify Mode'] = None
        df['Spotify Speechiness'] = None
        df['Spotify Acousticness'] = None
        df['Spotify Instrumentalness'] = None
        df['Spotify Liveness'] = None
        df['Spotify Valence'] = None
        df['Spotify Tempo'] = None
        df['Spotify Time Signature'] = None

        for index, row in df.iterrows():
            artist = row['Artist']
            title = row['Title']

            # Fetch data from Spotify
            spotify_data = get_spotify_data(artist, title)

            if spotify_data:
                # Unpack Spotify data
                df.at[index, 'Spotify Track Name'] = spotify_data['track_name']
                df.at[index, 'Spotify Track ID'] = spotify_data['track_id']
                df.at[index, 'Spotify Popularity'] = spotify_data['popularity']
                df.at[index, 'Spotify Duration (ms)'] = spotify_data['duration']
                df.at[index, 'Spotify Explicit'] = spotify_data['explicit']
                df.at[index, 'Spotify Preview URL'] = spotify_data['preview_url']
                df.at[index, 'Spotify External Track URL'] = spotify_data['external_urls_track']
                df.at[index, 'Spotify Album Name'] = spotify_data['album_name']
                df.at[index, 'Spotify Album ID'] = spotify_data['album_id']
                df.at[index, 'Spotify Album Release Date'] = spotify_data['album_release_date']
                df.at[index, 'Spotify Album Type'] = spotify_data['album_type']
                df.at[index, 'Spotify Total Tracks'] = spotify_data['total_tracks']
                df.at[index, 'Spotify Album Images'] = spotify_data['album_images']
                df.at[index, 'Spotify Album External URL'] = spotify_data['album_external_url']
                df.at[index, 'Spotify Artist Name'] = spotify_data['artist_name']
                df.at[index, 'Spotify Artist ID'] = spotify_data['artist_id']
                #df.at[index, 'Spotify Artist Popularity'] = spotify_data['artist_popularity']
                #df.at[index, 'Spotify Artist Genres'] = spotify_data['artist_genres']
                df.at[index, 'Spotify Artist External URL'] = spotify_data['artist_external_url']
                df.at[index, 'Spotify Danceability'] = spotify_data['danceability']
                df.at[index, 'Spotify Energy'] = spotify_data['energy']
                df.at[index, 'Spotify Key'] = spotify_data['key']
                df.at[index, 'Spotify Loudness'] = spotify_data['loudness']
                df.at[index, 'Spotify Mode'] = spotify_data['mode']
                df.at[index, 'Spotify Speechiness'] = spotify_data['speechiness']
                df.at[index, 'Spotify Acousticness'] = spotify_data['acousticness']
                df.at[index, 'Spotify Instrumentalness'] = spotify_data['instrumentalness']
                df.at[index, 'Spotify Liveness'] = spotify_data['liveness']
                df.at[index, 'Spotify Valence'] = spotify_data['valence']
                df.at[index, 'Spotify Tempo'] = spotify_data['tempo']
                df.at[index, 'Spotify Time Signature'] = spotify_data['time_signature']

            # Sleep to avoid rate limits
            time.sleep(0.1)

        # Save to output CSV
        df.to_csv(output_csv, index=False)

    if __name__ == "__main__":
        input_csv = 'swr_is_null.csv'  # Input CSV file
        output_csv = 'swr_is_null_spotify_data.csv'  # Output CSV file
        main(input_csv, output_csv)
    return (
        client_credentials_manager,
        get_spotify_data,
        input_csv,
        main,
        output_csv,
        sp,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
