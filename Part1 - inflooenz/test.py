import pandas as pd

df = pd.read_parquet(r"Z:\BSDS3002_GP_GIT\BSDS3002\Part1 - inflooenz\edges.parquet")

print(df[df["target"] == "Simon & Garfunkel"])