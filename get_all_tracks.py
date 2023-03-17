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

def get_all_albums_by_artist(token, artist_id):
    headers = get_auth_header(token)
    albums = []

    url = f"https://api.spotify.com/v1/artists/{artist_id}/albums?limit=50"
    while url:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"Failed to get albums for artist with ID {artist_id}.")
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.content}")
            break

        json_result = json.loads(response.content)
        artist_albums = json_result.get("items", [])
        albums.extend(artist_albums)
        url = json_result.get("next")

    return albums

token = get_token()

print(get_all_albums_by_artist(token, '0nmQIMXWTXfhgOBdNzhGOs'))