import pandas as pd
import requests
import datetime

import pytz

client_id = '08e2f604ed0f49baabd07bccf43cc9b3'
token = 'BQAkeq8tlxn2QGbSELJNfnc9ymbLq72FVbl8wROZnFJ6TUvck5XLKNl1OLD4oVNmzG9i9z6b2x4fVXUlcF6Nu8RcEgMJ97Y1AxpQJMMwAdUjG15yCSeIABwKl3Gp1AdmkZV5slHVqBLh24DwUhx0zNyqlQOArAn3ReCXD9ITR-WYRfH6PB4YZxhHTfgSgNYItRcNnM1jf4o'

def return_dataframe():
    input_variables = {
        'Authorization':'Bearer {token}'.format(token=token),
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    unix = int(yesterday.timestamp())*1000
    
    r = requests.get('https://api.spotify.com/v1/me/player/recently-played?limit=50&before{time}'
                     .format(time=unix), headers=input_variables)
    
    data = r.json()
    artis_name = []
    album_name = []
    song_name = []
    played_at = []
    release = []
    
    for song in data['items']:
        artis_name.append(song['track']['album']['artists'][0]['name'])
        album_name.append(song['track']['album']['name'])
        song_name.append(song['track']['name'])
        played_at.append(song['played_at'])
        release.append(song['track']['album']["release_date"])
    
    df_dict = {
        'song_name':song_name,
        'artis_name':artis_name,
        'album_name':album_name,
        'release':release,
        'played_at':played_at
    }

    df = pd.DataFrame(df_dict, columns=['song_name','artis_name','album_name','release','played_at'])

    df['release'] = df['release'].apply(lambda x : x[:4])
    df['release'] = pd.to_datetime(df['release'])
    df['release'] = df['release'].dt.year

    df['played_at'] = pd.to_datetime(df['played_at']).dt.tz_convert('Etc/GMT-7')
    df['played_at'] = df['played_at'].dt.strftime('%Y-%m-%d %H:%M:%S') # trả về object
    df['played_at'] = pd.to_datetime(df['played_at'])

    return df


def spotify_etl():
    load_df = return_dataframe()
    print(load_df)
    return load_df

spotify_etl()