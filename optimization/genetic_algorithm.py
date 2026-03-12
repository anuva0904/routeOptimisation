import random
import networkx as nx

def random_route(graph,start,end):

    try:
        return nx.shortest_path(graph,start,end,weight="weight")
    except:
        return []


def genetic_route(graph,start,end,pop_size=20):

    population = [random_route(graph,start,end) for _ in range(pop_size)]

    best = min(population,key=len)

    return best
