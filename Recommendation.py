import pandas as pd
from sklearn.cluster import KMeans
from sklearn.utils import shuffle

def Suggestion(url):
    tracks = pd.read_csv('result.csv')

    favorites = tracks[tracks.Url_youtube.isin(url)]

    cluster_numbers = list(favorites['type'])
    clusters = {}
    for num in cluster_numbers:
        clusters[num] = cluster_numbers.count(num)

    user_favorite_cluster = [(k, v) for k, v in sorted(clusters.items(), key=lambda item: item[1])][0][0]


    suggestions = tracks[tracks.type == user_favorite_cluster]

    df = shuffle(suggestions)
    new_url=df['Url_youtube']
    new_url_str=new_url.iloc[0]
    return new_url_str