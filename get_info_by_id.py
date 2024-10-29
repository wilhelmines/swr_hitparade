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
    spotipy,
):
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Initialize Spotify client
    client_credentials_manager = SpotifyClientCredentials(
        client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    return client_credentials_manager, sp


@app.cell
def __(logging, pd, sp, time):
    def get_spotify_data_by_id(track_id):
        logging.info(f"Fetching Spotify data for track ID '{track_id}'")
        track = sp.track(track_id)
        audio_features = sp.audio_features(track_id)[0]

        return extract_data(track, audio_features)


    def get_spotify_data_by_search(artist, title):
        logging.info(f"Searching Spotify for '{title}' by '{artist}'")
        query = f"artist:{artist} track:{title}"
        results = sp.search(q=query, type='track', limit=1)

        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            track_id = track['id']
            audio_features = sp.audio_features(track_id)[0]
            return extract_data(track, audio_features)

        logging.warning(f"No results found for '{title}' by '{artist}'.")
        return None


    def extract_data(track, audio_features):
        album = track['album']
        artist = track['artists'][0]

        # Extract relevant data
        return {
            "track_name": track['name'],
            "track_id": track['id'],
            "popularity": track['popularity'],
            "duration": track['duration_ms'],
            "explicit": track['explicit'],
            "preview_url": track.get('preview_url'),
            "external_urls_track": track['external_urls']['spotify'],
            "album_name": album['name'],
            "album_id": album['id'],
            "album_release_date": album['release_date'],
            "album_type": album['album_type'],
            "total_tracks": album['total_tracks'],
            "album_images": album['images'],
            "album_external_url": album['external_urls']['spotify'],
            "artist_name": artist['name'],
            "artist_id": artist['id'],
            "artist_external_url": artist['external_urls']['spotify'],
            "danceability": audio_features['danceability'],
            "energy": audio_features['energy'],
            "key": audio_features['key'],
            "loudness": audio_features['loudness'],
            "mode": audio_features['mode'],
            "speechiness": audio_features['speechiness'],
            "acousticness": audio_features['acousticness'],
            "instrumentalness": audio_features['instrumentalness'],
            "liveness": audio_features['liveness'],
            "valence": audio_features['valence'],
            "tempo": audio_features['tempo'],
            "time_signature": audio_features['time_signature']
        }


    def main(input_csv, output_csv):
        # Read the input CSV with existing columns
        df = pd.read_csv(input_csv)

        # Define a mapping from the Spotify data dictionary to the column names in the CSV
        column_mapping = {
            "track_name": "Spotify Track Name",
            "track_id": "Spotify Track ID",
            "popularity": "Spotify Popularity",
            "duration": "Spotify Duration (ms)",
            "explicit": "Spotify Explicit",
            "preview_url": "Spotify Preview URL",
            "external_urls_track": "Spotify External Track URL",
            "album_name": "Spotify Album Name",
            "album_id": "Spotify Album ID",
            "album_release_date": "Spotify Album Release Date",
            "album_type": "Spotify Album Type",
            "total_tracks": "Spotify Total Tracks",
            "album_images": "Spotify Album Images",
            "album_external_url": "Spotify Album External URL",
            "artist_name": "Spotify Artist Name",
            "artist_id": "Spotify Artist ID",
            "artist_external_url": "Spotify Artist External URL",
            "danceability": "Spotify Danceability",
            "energy": "Spotify Energy",
            "key": "Spotify Key",
            "loudness": "Spotify Loudness",
            "mode": "Spotify Mode",
            "speechiness": "Spotify Speechiness",
            "acousticness": "Spotify Acousticness",
            "instrumentalness": "Spotify Instrumentalness",
            "liveness": "Spotify Liveness",
            "valence": "Spotify Valence",
            "tempo": "Spotify Tempo",
            "time_signature": "Spotify Time Signature"
        }

        # Iterate over rows in the DataFrame
        for index, row in df.iterrows():
            artist = row['Artist']
            title = row['Title']
            track_id = row.get('Spotify Track ID')  # Assume track IDs are pre-loaded in input

            # Fetch data from Spotify, either by ID or by search
            spotify_data = get_spotify_data_by_id(track_id) if pd.notna(track_id) else get_spotify_data_by_search(artist, title)

            if spotify_data:
                # Assign values to columns only if they exist in the mapping and the DataFrame
                for key, value in spotify_data.items():
                    if key in column_mapping:
                        col_name = column_mapping[key]
                        # Convert lists (e.g., album_images) to strings
                        if isinstance(value, list):
                            value = str(value)
                        # Set the value in the appropriate column
                        if col_name in df.columns:
                            df.at[index, col_name] = value

            # Sleep to avoid rate limits
            time.sleep(0.1)

        # Save to output CSV with the same columns
        df.to_csv(output_csv, index=False)

    if __name__ == "__main__":
        input_csv = 'swr_is_null_spotify_data.csv'  # Input CSV file
        output_csv = 'swr_is_null_spotify_data_2.csv'  # Output CSV file
        main(input_csv, output_csv)
    return (
        extract_data,
        get_spotify_data_by_id,
        get_spotify_data_by_search,
        input_csv,
        main,
        output_csv,
    )


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
