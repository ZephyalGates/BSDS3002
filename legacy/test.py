import os
import base64
import requests
from requests import post, get
import json
from tqdm import tqdm
import pandas as pd

df = pd.read_parquet("latest_edges.parquet")

print(len(df))
