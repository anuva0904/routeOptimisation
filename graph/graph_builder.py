import networkx as nx
import numpy as np
import random


def distance(lat1, lon1, lat2, lon2):

    return np.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)


def build_graph(df, edges_df):

    G = nx.DiGraph()

    stops = df[['stop_id','stop_name','stop_lat','stop_lon']].drop_duplicates()

    for _, row in stops.iterrows():

        G.add_node(
            row['stop_id'],
            name=row['stop_name'],
            lat=row['stop_lat'],
            lon=row['stop_lon']
        )

    for _, row in edges_df.iterrows():

        weight = row['travel_time'] * random.uniform(0.9,1.2)

        G.add_edge(
            row['from_stop'],
            row['to_stop'],
            weight=weight
        )

    stop_list = stops.to_dict("records")

    for i in range(len(stop_list)):

        for j in range(i+1,len(stop_list)):

            s1 = stop_list[i]
            s2 = stop_list[j]

            dist = distance(
                s1["stop_lat"],
                s1["stop_lon"],
                s2["stop_lat"],
                s2["stop_lon"]
            )

            if dist < 0.02:

                travel_time = dist * 10000
                travel_time = travel_time * random.uniform(0.9,1.2)

                G.add_edge(s1["stop_id"], s2["stop_id"], weight=travel_time)
                G.add_edge(s2["stop_id"], s1["stop_id"], weight=travel_time)

    return G