import numpy as np
import networkx as nx
from tqdm import tqdm
import metis

def euclidean_distance(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))

def part_graph(graph, k, df=None):
    edgecuts, parts = metis.part_graph(
        graph, 2, objtype='cut', ufactor=250)
    for i, p in enumerate(graph.nodes()):
        graph._node[p]['cluster'] = parts[i]
    if df is not None:
        df['cluster'] = nx.get_node_attributes(graph, 'cluster').values()
    return graph

def internal_interconnectivity(graph, cluster):
    return np.sum(bisection_weights(graph, cluster))

def relative_interconnectivity(graph, cluster_i, cluster_j):
    edges = get_edgs((cluster_i, cluster_j), graph)
    EC = np.sum(get_weights(graph, edges))
    ECci, ECcj = internal_interconnectivity(
        graph, cluster_i), internal_interconnectivity(graph, cluster_j)
    return EC / ((ECci + ECcj) / 2.0)

def internal_closeness(graph, cluster):
    cluster = graph.subgraph(cluster)
    edges = cluster.edges()
    weights = get_weights(cluster, edges)
    return np.sum(weights)

def relative_closeness(graph, cluster_i, cluster_j):
    edges = get_edgs((cluster_i, cluster_j), graph)
    if not edges:
        return 0.0
    else:
        SEC = np.mean(get_weights(graph, edges))
    Ci, Cj = internal_closeness(
        graph, cluster_i), internal_closeness(graph, cluster_j)
    SECci, SECcj = np.mean(bisection_weights(graph, cluster_i)), np.mean(
        bisection_weights(graph, cluster_j))
    return SEC / ((Ci / (Ci + Cj) * SECci) + (Cj / (Ci + Cj) * SECcj))

def get_connectivity(g, ci, cj, a):
    return relative_interconnectivity(g, ci, cj) * np.power(relative_closeness(g, ci, cj), a)

def get_cluster(graph, clusters):
    nodes = [n for n in graph._node if graph._node[n]['cluster'] in clusters]
    return nodes

def get_edgs(partitions, graph):
    cut_set = []
    for a in partitions[0]:
        for b in partitions[1]:
            if a in graph:
                if b in graph[a]:
                    cut_set.append((a, b))
    return cut_set

def min_cut_bisector(graph):
    graph = graph.copy()
    graph = part_graph(graph, 2)
    partitions = get_cluster(graph, [0]), get_cluster(graph, [1])
    return get_edgs(partitions, graph)

def get_weights(graph, edges):
    return [graph[edge[0]][edge[1]]['weight'] for edge in edges]

def bisection_weights(graph, cluster):
    cluster = graph.subgraph(cluster)
    edges = min_cut_bisector(cluster)
    weights = get_weights(cluster, edges)
    return weights
