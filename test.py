import os
import base64
import requests
from requests import post, get
import json
from tqdm import tqdm
import pandas as pd

df = pd.read_parquet("edges.parquet")

print(df.head(-5))

# rows_with_none = df[df["Spotify ID"] == 'None']
# print(rows_with_none)