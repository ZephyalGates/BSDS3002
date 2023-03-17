import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm

def search(artist_list, checkpoint_interval=1000):
    edges = []
    checkpoint_dir = 'checkpoints'
    os.makedirs(checkpoint_dir, exist_ok=True)
    checkpoint_file = os.path.join(checkpoint_dir, 'checkpoint.pkl')
    start_index = 0

    if os.path.exists(checkpoint_file):
        checkpoint = pd.read_pickle(checkpoint_file)
        edges = checkpoint['edges']
        start_index = checkpoint['index']
        print(f"Resuming from checkpoint: {start_index}")

    for i, a in tqdm(enumerate(artist_list[start_index:]), total=len(artist_list[start_index:]), position=0, desc="Processing artists"):
        index = i + start_index

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
        if index > 0 and index % checkpoint_interval == 0:
            checkpoint = {'edges': edges, 'index': index}
            pd.to_pickle(checkpoint, checkpoint_file)

        # print(edges)    
        print(len(edges))
    checkpoint = {'edges': edges, 'index': index}
    pd.to_pickle(checkpoint, checkpoint_file)


    return edges

artists_df = pd.read_parquet('artists.parquet')

artist_list = artists_df['artist'].tolist()

edges = search(artist_list, checkpoint_interval=10)

# print(edges)

edges_df = pd.DataFrame(edges, columns=['source', 'target', 'type'])

edges_df.to_parquet('edges.parquet')