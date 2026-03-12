import pandas as pd


def route_to_dataframe(G, route):

    rows = []

    for node in route:

        rows.append({
            "latitude": G.nodes[node]["lat"],
            "longitude": G.nodes[node]["lon"],
            "name": G.nodes[node]["name"]
        })

    return pd.DataFrame(rows)