import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

def search(artist_list):
    edges = []




    for i, a in tqdm(enumerate(artist_list), total=len(artist_list), position=0, desc="Processing artists"):

        aa = a.replace(" ", "+")
        url = f'https://inflooenz.com/?artist={aa}&submit=Search'
        try:
            page = requests.get(url)
            page.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Error: {a} not found")
            continue

        soup = BeautifulSoup(page.content, 'html.parser')

        followers_list = soup.find('ul', attrs={'class':'influences-list', 'id':'followers-list'})
        if followers_list:
            print('F1')
            for follower in followers_list.find_all('li')[:-1]:
                if follower.text != "":
                    edges.append([follower.text, a, 'follower'])
        else:
            print('F0')  
        influencers_list = soup.find('ul', attrs={'class':'influences-list', 'id':'influencers-list'})
        if influencers_list:
            print('I1')
            for influencer in influencers_list.find_all('li')[:-1]:
                if influencer.text != "":
                    edges.append([a, influencer.text, 'influencer'])
        else:
            print('I0')                


    return edges

artist_list = ["Simon and Garfunkel"]

edges = search(artist_list)

print(len(edges))

edges_df = pd.DataFrame(edges, columns=['source', 'target', 'type'])

previous_df = pd.read_parquet("latest_edges.parquet")

print(len(previous_df))

combined = pd.concat([previous_df, edges_df])

print(len(combined))
print(combined.head(-5))

combined.to_parquet('latest_edges.parquet')