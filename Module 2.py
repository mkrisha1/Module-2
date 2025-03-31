# Module 2

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import re

df = pd.read_csv("imdb_movies.csv", encoding="latin1")
df.columns = df.columns.str.lower()

# Drop unnecessary fields
df_clean = df.drop(columns=['overview', 'orig_title', 'status', 'orig_lang', 'country'])
print(df_clean.columns)

# Drop rows with missing data
print(df.isnull().sum())
df = df.dropna()
print(df.isnull().sum())

def contains_sqrt(text):
    if isinstance(text, str):
        return 'square root' in text.lower()  # Case-insensitive check
    return False

# Drop rows with unrecognizable data
def has_unrecognizable_characters(text):
    pattern = re.compile('[^\x00-\x7F]+')  # Non-ASCII characters
    return bool(pattern.search(text))

df_clean = df[~df['names'].apply(has_unrecognizable_characters)]
df_clean = df[~df['crew'].apply(has_unrecognizable_characters)]
df_clean = df_clean[df_clean['crew'].notna() & (df_clean['crew'] != '')]
df_clean = df[~df['genre'].apply(has_unrecognizable_characters)]
df_clean = df[~df.map(contains_sqrt).any(axis=1)]


g = nx.Graph()
df.head()

for index, row in df_clean.iterrows():
    # Check if 'Crew' is a valid string before attempting to split
    if isinstance(row['crew'], str):
        crew_members = row['crew'].split(',')  
        for actor in crew_members:
            # Add actor to the graph if they don't exist yet
            if actor not in g:
                g.add_node(actor)
            # Create edges between each pair of actors in the same movie
            for co_actor in crew_members:
                if actor != co_actor:  # Prevent self-links
                    g.add_edge(actor, co_actor)

degree_centrality = nx.degree_centrality(g)

important_actors = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]

print("Top 5 Important Actors:")
for actor, centrality in important_actors:
    print(f"Actor: {actor}, Degree Centrality: {centrality:.4f}")

# Visualize the network
plt.figure(figsize=(15, 6))
nx.draw_networkx(g, with_labels=True, node_size=50, font_size=10, node_color="skyblue", alpha=0.7)
plt.title("Movie Actor Network")
plt.tight_layout()
plt.show()





