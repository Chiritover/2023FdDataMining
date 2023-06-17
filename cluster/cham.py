import pandas as pd
import itertools
from graphs import *
import matplotlib.pyplot as plt

def knn_graph(df, k):
    points = [p[1:] for p in df.itertuples()]
    g = nx.Graph()
    for i in range(0, len(points)):
        g.add_node(i)
    iterpoints = enumerate(points)
    for i, p in iterpoints:
        distances = list(map(lambda x: euclidean_distance(p, x), points))
        closests = np.argsort(distances)[1:k+1]  #  kth closest
        for c in closests:
            g.add_edge(i, c, weight=1.0 / distances[c], similarity=int(
                1.0 / max(1e-7, distances[c]) * 1e4))
        g._node[i]['pos'] = p
    g.graph['edge_weight_attr'] = 'similarity'
    return g

def part(graph, k, df=None):
    clusters = 0
    for i, p in enumerate(graph.nodes()):
        graph._node[p]['cluster'] = 0
    cnts = {}
    cnts[0] = len(graph.nodes())

    while clusters < k - 1:
        maxc = -1
        max_count = 0
        for key, val in cnts.items():
            if val > max_count:
                max_count = val
                maxc = key
        s_nodes = [n for n in graph._node if graph._node[n]['cluster'] == maxc]
        s_graph = graph.subgraph(s_nodes)
        edgecuts, parts = metis.part_graph(s_graph, 2, objtype='cut', ufactor=250)
        new = 0
        for i, p in enumerate(s_graph.nodes()):
            if parts[i] == 1:
                graph._node[p]['cluster'] = clusters + 1
                new = new + 1
        cnts[maxc] = cnts[maxc] - new
        cnts[clusters + 1] = new
        clusters = clusters + 1
    edgecuts, parts = metis.part_graph(graph, k)
    if df is not None:
        df['cluster'] = nx.get_node_attributes(graph, 'cluster').values()
    return graph

def merge(graph, df, a, k):
    clusters = np.unique(df['cluster'])
    while len(clusters) > k:
        class1 = -1
        class2 = -2
        optimal = 0
        for combination in itertools.combinations(clusters, 2):
            i, j = combination
            gi = [n for n in graph._node if graph._node[n]['cluster'] in [i]]
            gj = [n for n in graph._node if graph._node[n]['cluster'] in [j]]
            edges = []
            for a in gi:
                for b in gj:
                    if a in graph:
                        if b in graph[a]:
                            edges.append((a, b))
            if not edges:
                continue
            result = get_connectivity(graph, gi, gj, a)
            if result > optimal:
                optimal = result
                class1, class2 = i, j
        if optimal > 0:
            df.loc[df['cluster'] == class2, 'cluster'] = class1
            for i, p in enumerate(graph.nodes()):
                if graph._node[p]['cluster'] == class2:
                    graph._node[p]['cluster'] = class1
        else:
            return

def get_labels(df):
    ans = df.copy()
    clusters = list(pd.DataFrame(df['cluster'].value_counts()).index)
    c = 1
    for i in clusters:
        ans.loc[df['cluster'] == i, 'cluster'] = c
        c = c + 1
    return ans

df = pd.read_csv('./datasets/3MC.csv', sep=',',
                     header=None)
df.drop(df.columns[[-1,]], axis=1, inplace=True)
# print(df)
n = 8
pre_k = 20
k = 4
graph = knn_graph(df, n)
graph = part(graph, pre_k, df)
merge(graph, df, 2.0, k)
if (len(df.columns) > 3):
    print("Plot Waring: more than 2-Dimensions!")
df.plot(kind='scatter', c=df['cluster'], cmap='gist_rainbow', x=0, y=1)
plt.savefig("ans2.png")