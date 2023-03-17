import pandas as pd
from fuzzywuzzy import fuzz

df = pd.read_parquet(r"Z:\BSDS3002_GP_GIT\BSDS3002\Part1 - inflooenz\artists_in_edges.parquet")

top100 = ["Talking Heads", "Carl Perkins", "Curtis Mayfield", "R.E.M.", "Diana Ross and the Supremes", "Lynyrd Skynyrd", "Nine Inch Nails", "Booker T. and the MGs", "Guns n' Roses", "Tom Petty", "Carlos Santana", "The Yardbirds", "Jay-Z", "Gram Parsons", "Tupac Shakur", "Black Sabbath", "James Taylor", "Eminem", "Creedence Clearwater Revival", "The Drifters", "Elvis Costello", "The Four Tops", "The Stooges", "Beastie Boys", "The Shirelles", "Eagles", "Hank Williams", "Radiohead", "AC/DC", "Frank Zappa", "The Police", "Jackie Wilson", "The Temptations", "Cream", "Al Green", "The Kinks", "Phil Spector", "Tina Turner", "Joni Mitchell", "Metallica", "The Sex Pistols", "Aerosmith", "Parliament and Funkadelic", "Grateful Dead", "Dr. Dre", "Eric Clapton", "Howlin' Wolf", "The Allman Brothers Band", "Queen", "Pink Floyd", "The Band", "Elton John", "Run-DMC", "Patti Smith", "Janis Joplin", "The Byrds", "Public Enemy", "Sly and the Family Stone", "Van Morrison", "The Doors", "Simon and Garfunkel", "David Bowie", "John Lennon", "Roy Orbison", "Madonna", "Michael Jackson", "Neil Young", "The Everly Brothers", "Smokey Robinson and the Miracles", "Johnny Cash", "Nirvana", "The Who", "The Clash", "Prince", "The Ramones", "Fats Domino", "Jerry Lee Lewis", "Bruce Springsteen", "U2", "Otis Redding", "Bo Diddley", "The Velvet Underground", "Marvin Gaye", "Muddy Waters", "Sam Cooke", "Stevie Wonder", "Led Zeppelin", "Buddy Holly", "The Beach Boys", "Bob Marley", "Ray Charles", "Aretha Franklin", "Little Richard", "James Brown", "Jimi Hendrix", "Chuck Berry", "The Rolling Stones", "Elvis Presley", "Bob Dylan", "The Beatles"]

threshold = 95

# create a set of the elements in the dataframe columns
df_elements = set(df['Artist'].values.flatten())

# initialize an empty list to store the elements that are not included
not_included = []

# check if all elements in the list are included in the dataframe columns
for e in top100:
    if not any(fuzz.partial_ratio(e, d) >= threshold for d in df_elements):
        not_included.append(e)

# print the elements that are not included
print("Elements not included in the DataFrame columns with a fuzzy matching similarity of at least 95%:")
print(not_included)