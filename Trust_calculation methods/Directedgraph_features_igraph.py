import csv
import networkx as nx
from igraph import Graph
import pandas as pd


def general_attribute(net):
    # betweenness
    net.vs["betweenness"] = Graph.betweenness(net)
    print("done")
    # degree
    net.vs["degree"] = Graph.degree(net)
    # degree_centrality
    print("done")
    # centrality
    net.vs["eig_center"] = Graph.eigenvector_centrality(net)
    print("done")
    net.vs["har_center"] = Graph.harmonic_centrality(net)
    # average neighbor degree
    # net.vs["avg_neigh_degree"]= Graph.knn(net)
    # closeness_centrality
    net.vs["closeness"] = Graph.closeness(net)

    # pagerank
    net.vs["pgrank"] = Graph.pagerank(net)
    net.vs["weig_pgrank"] = Graph.pagerank(net)
    # hubs and authority
    net.vs["auth"] = Graph.authority_score(net)
    net.vs["hub"] = Graph.hub_score(net)
    # clustering coefficient for nodes.
    # Returns the core number for each vertex
    # coreness
    net.vs["coreness"] = Graph.coreness(net)
    # eccentricity
    net.vs["eccentricity"] = Graph.eccentricity(net)
    # assortivity
    # net.vs["assortivity"] = Graph.assortativity(net)
    # net.vs['deg_assort'] = Graph.assortativity_degree(net)
    # strength
    net.vs["strength"] = Graph.strength(net)
    # transitivity
    # net.vs['transitivity'] =Graph.transitivity_local_undirected(net)

    return net


def local_attribute(AnomaSbg, net1):
    # betweenness
    net1.vs["loc_betweenness"] = Graph.betweenness(AnomaSbg)
    print("done")
    # degree
    net1.vs["loc_degree"] = Graph.degree(AnomaSbg)
    # degree_centrality
    print("done")
    # centrality
    net1.vs["loc_eig_center"] = Graph.eigenvector_centrality(AnomaSbg)
    print("done")
    net1.vs["loc_har_center"] = Graph.harmonic_centrality(AnomaSbg)
    # average neighbor degree
    # net.vs["avg_neigh_degree"]= Graph.knn(net)
    # closeness_centrality
    net1.vs["loc_closeness"] = Graph.closeness(AnomaSbg)

    # pagerank
    net1.vs["loc_pgrank"] = Graph.pagerank(AnomaSbg)
    net1.vs["loc_weig_pgrank"] = Graph.pagerank(AnomaSbg)
    # hubs and authority
    net1.vs["loc_auth"] = Graph.authority_score(AnomaSbg)
    net1.vs["loc_hub"] = Graph.hub_score(AnomaSbg)
    # clustering coefficient for nodes.
    # Returns the core number for each vertex
    # coreness
    # net1.vs["loc_coreness"] = Graph.coreness(AnomaSbg)
    # eccentricity
    net1.vs["loc_eccentricity"] = Graph.eccentricity(AnomaSbg)
    # assortivity
    # net.vs["assortivity"] = Graph.assortativity(net)
    # net.vs['deg_assort'] = Graph.assortativity_degree(net)
    # strength
    net1.vs["loc_strength"] = Graph.strength(AnomaSbg)
    # transitivity
    # net1.vs['loc_transitivity'] = Graph.transitivity_local_undirected(AnomaSbg)
    return AnomaSbg, net1


# net = nx.read_graphml('dataset/Enron/Enron.graphml')
# dataset/BitcoinOTC/regression_biased/OTC_regression_biased.graphml
net = nx.read_graphml("dataset/BitcoinOTC/bias_deserve/OTC_bias_deserve.graphml")
# net = nx.convert_node_labels_to_integers(net, ordering='sorted', first_label=0)
# anomalies = pd.read_csv('dataset/Enron/Enron.true', index_col=0, sep=';', header=None)

"""
AnomalousNode= []
NormalNode=[]
for n in net.nodes():
    net.nodes[n]['anomaly'] = anomalies.loc[int(n)][1]
"""


netw = Graph.from_networkx(net)
print("dataset converted")
netw = general_attribute(netw)
# print(netw.summary())
# print(netw.vs['rank'])
i = 0
for item in netw.vs["bias"]:
    # print(netw.vs['rank'][i])
    if item is None:
        netw.vs[i]["bias"] = -1
        # print(netw.vs['rank'][i])
    i += 1
i = 0
for item in netw.vs["deserve"]:
    # print(netw.vs['rank'][i])
    if item is None:
        netw.vs[i]["deserve"] = 0
        # print(netw.vs['rank'][i])
    i += 1

anomalous = netw.vs.select(lambda x: x["deserve"] < 0)
# drop_node= netw.vs.select(label_eq=1)
# anomalous= netw.vs.select(rank_lt=0)

subgraph_drop = Graph.subgraph(netw, anomalous)

non_anomalous = netw.vs.select(deserve_gt=0)
# non_anomalous= netw.vs.select(lambda x:x['rank'] > 0)
subgraph_nondrop = Graph.subgraph(netw, non_anomalous)


# general_attribute(netw)
local_attribute(subgraph_drop, netw)
local_attribute(subgraph_nondrop, netw)

print("loaded dataset!")
netw.write_graphml("dataset/1.graphml")
G = nx.read_graphml("dataset/1.graphml")
print("done")
count = 0
list_node = []
for n, d in G.nodes(data=True):

    if count == 0:
        list_node = ["node_id"] + list(d.keys())
        count += 1
        break

# Returns a list of cliques containing the given node.
# Appending anomalies to the node attributes

with open(
    "dataset/BitcoinOTC/bias_deserve/OTC_bias_deserve.csv", "w", newline=""
) as csvfile:
    fieldnames = list_node
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for n, d in G.nodes(data=True):
        d["node_id"] = n
        writer.writerow(d)
print("done!")
