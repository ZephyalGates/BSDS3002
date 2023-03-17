import os
import base64
import requests
from requests import post, get
import json
from tqdm import tqdm
import pandas as pd

def get_token():
    client_id = '7727b6a6602f4dcf99d337ee11f0983e'
    client_secret = '6b4958253cb544aaae1b0bf4858726ee'
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    json_result = json.loads(response.content)

    if "access_token" in json_result:
        token = json_result["access_token"]
        return token
    else:
        print("Error: Failed to get access token")
        print(json_result)
        return None

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def get_artist_id(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    response = requests.get(query_url, headers=headers)
    json_result = json.loads(response.content)

    if "artists" in json_result and "items" in json_result["artists"] and len(json_result["artists"]["items"]) > 0:
        artist = json_result["artists"]["items"][0]
        artist_id = artist.get("id", None)
        return artist_id
    else:
        return None, None, None

token = get_token()


df = pd.read_parquet("data_similarity_larger_than_93.parquet")

df["Spotify ID"] = None

with tqdm(total=len(df)) as pbar:
    for i, artist_name in enumerate(df["Spotify Name"]):
        pbar.set_description(f"Processing artist {i+1} of {len(df)}: {artist_name}")
        # token = get_token()
        if token:
            spotify_id = get_artist_id(token, artist_name)
            if spotify_id:
              df.at[i, "Spotify ID"] = spotify_id

        pbar.update(1)

df["Spotify ID"] = df["Spotify ID"].apply(lambda x: str(x).encode() if x is not None else None)
# df.head(10)
df.to_parquet("data_similarity_larger_than_93_with_id.parquet")