from fuzzywuzzy import fuzz
import pandas as pd
import re

df = pd.read_parquet("artists_with_infos.parquet")

def compute_similarity(s1, s2):
    if s1 is None or s2 is None:
        return 0
    else:
        return fuzz.ratio(s1.lower(), s2.lower())

# Compute the similarity score and add it to a new column
df["Similarity"] = df.apply(lambda row: compute_similarity(row["Artist"], row["Spotify Name"]), axis=1)

print(df.head())

num_similar = (df["Similarity"] > 93).sum()

df_filtered = df[df["Similarity"] > 93]

print(num_similar)

df_filtered.to_parquet("data_similarity_larger_than_93.parquet", index=False)

df_filtered2 = pd.read_parquet("data_similarity_less_than_95.parquet")

def preprocess_string(s):

    if isinstance(s, str):

        s = re.sub(r'[^\w\s]', '', s)

        s = s.replace("the", "")

        s = s.replace("&", "and")

        s = s.lower()

        return s
    else:

        return ""

df_filtered2.loc[:, "Artist2"] = df_filtered2.loc[:, "Artist"].apply(preprocess_string)
df_filtered2.loc[:, "Spotify Name2"] = df_filtered2.loc[:, "Spotify Name"].apply(preprocess_string)
df_filtered2["Similarity2"] = df_filtered2.apply(lambda row: compute_similarity(row["Artist"], row["Spotify Name"]), axis=1)

df_filtered2.to_csv("data_similarity_less_than_95_filtered.csv", index=False)