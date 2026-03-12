import networkx as nx


def optimize_route(G, start, end):

    """
    Compute optimal route using weighted shortest path
    """

    try:

        route = nx.shortest_path(
            G,
            source=start,
            target=end,
            weight="weight"
        )

        total_time = 0

        for i in range(len(route)-1):

            total_time += G[route[i]][route[i+1]]["weight"]

        return route, total_time

    except:

        return [], 0