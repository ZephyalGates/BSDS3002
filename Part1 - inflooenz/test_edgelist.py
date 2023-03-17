import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

artists_df = pd.read_parquet(r"Z:\BSDS3002_GP_GIT\BSDS3002\Part1 - inflooenz\artists.parquet")
edges_df = pd.read_parquet(r"Z:\BSDS3002_GP_GIT\BSDS3002\Part1 - inflooenz\edges.parquet")

print(len(edges_df))

all_artists = set(artists_df['artist'])

artists_in_edges = set(edges_df['source']).union(set(edges_df['target']))

percent_in_edges = len(artists_in_edges) / len(all_artists) * 100

artists_not_in_edges = all_artists - artists_in_edges
print(len(artists_in_edges))
print(f"{len(artists_not_in_edges)} artists not in edge list")
print(f"{percent_in_edges:.2f}% of artists in edge list")

artists_in_edges_df = pd.DataFrame(list(artists_in_edges), columns=['Artist'])
print(artists_in_edges_df.head())
artists_in_edges_df.to_parquet(r"Z:\BSDS3002_GP_GIT\BSDS3002\Part1 - inflooenz\artists_in_edges.parquet")