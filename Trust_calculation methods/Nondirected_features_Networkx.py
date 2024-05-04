import csv
import networkx as nx
import pandas as pd

# 35 attributed for each node of non directed


def general_attribute(net):
    bb = nx.betweenness_centrality(net)
    # betweenness
    nx.set_node_attributes(net, bb, "betweenness")
    # degree
    degree = dict(nx.degree(net))
    nx.set_node_attributes(net, degree, "degree")
    # degree centrality
    degree_cent = nx.degree_centrality(net)
    nx.set_node_attributes(net, degree_cent, "degree_centrality")

    # average neighbor degree
    avg_neigh = nx.average_neighbor_degree(net)
    nx.set_node_attributes(net, avg_neigh, "avg_neigh_degree")
    # closeness_centrality
    closeness = nx.closeness_centrality(net)
    nx.set_node_attributes(net, closeness, "closeness")
    # triangles
    triangle = nx.triangles(net)
    nx.set_node_attributes(net, triangle, "triangles")
    # pagerank
    pr = nx.pagerank(net, alpha=0.9)
    nx.set_node_attributes(net, pr, "prank")

    # clustering coefficient for nodes.
    cluster = nx.clustering(net)
    nx.set_node_attributes(net, cluster, "clusterCo")

    # Returns the core number for each vertex
    k_core = nx.core_number(net)
    nx.set_node_attributes(net, k_core, "k_core")

    # eccentricity
    eccent = nx.eccentricity(net)
    nx.set_node_attributes(net, eccent, "eccent")
    return net


def local_attribute(AnomaSbg, net):
    # closeness_centrality Local
    closeness_loc = nx.closeness_centrality(AnomaSbg)
    nx.set_node_attributes(net, closeness_loc, "Loc_closeness")

    bb_loc = nx.betweenness_centrality(AnomaSbg)
    # betweenness Local
    nx.set_node_attributes(net, bb_loc, "Loc_betweenness")
    # degree Local
    degree_loc = dict(nx.degree(AnomaSbg))
    nx.set_node_attributes(net, degree_loc, "Loc_degree")
    # degree centrality Local
    degree_cent_loc = nx.degree_centrality(AnomaSbg)
    nx.set_node_attributes(net, degree_cent_loc, "Loc_degree_centrality")
    # closeness_centrality Local
    closeness_loc = nx.closeness_centrality(AnomaSbg)
    nx.set_node_attributes(net, closeness_loc, "Loc_closeness")

    # clustering coefficient for nodes Local
    cluster_loc = nx.clustering(AnomaSbg)
    nx.set_node_attributes(net, cluster_loc, "Loc_clusterCo")

    # Square clustering coeficient
    sq_cluster_loc = nx.square_clustering(AnomaSbg)
    nx.set_node_attributes(net, cluster_loc, "Loc_sq_clusterCo")

    # Returns the core number for each vertex local
    k_core_loc = nx.core_number(AnomaSbg)
    nx.set_node_attributes(net, k_core_loc, "Loc_k_core")
    return AnomaSbg, net


net = nx.read_graphml("dataset/Enron/Enron.graphml")
anomalies = pd.read_csv("dataset/Enron/Enron.true", index_col=0, sep=";", header=None)
net = net.to_undirected()
AnomalousNode = []
NormalNode = []

# Returns a list of cliques containing the given node.
# Appending anomalies to the node attributes


net = general_attribute(net)
for n in net.nodes():
    # Returns the size of the largest maximal clique containing each given node.
    MClique = dict(nx.node_clique_number(net, nodes=None))
    nx.set_node_attributes(net, MClique, "maximalCliques")
    # number of cliques this node belong to
    net.nodes[n]["cliques"] = len(
        nx.cliques_containing_node(net, nodes=n, cliques=None)
    )
    net.nodes[n]["anomaly"] = anomalies.loc[int(n)][1]
net = nx.convert_node_labels_to_integers(net, ordering="sorted", first_label=0)


# Assotitavity
assotitavity = nx.attribute_assortativity_coefficient(net, "anomaly")
nx.set_node_attributes(net, assotitavity, "assotitavity")

for (p, d) in net.nodes(data=True):
    if d["anomaly"] == 1:
        AnomalousNode.append(p)
    else:
        NormalNode.append(p)

# Local attributes for anomalous subgraph
AnomaSbg = nx.subgraph(net, nbunch=AnomalousNode)
AnomaSbg, net = local_attribute(AnomaSbg, net)

# Local attributes for Normal subgraph
NormSbg = nx.subgraph(net, nbunch=NormalNode)
NormSbg, net = local_attribute(NormSbg, net)

count = 0
list_node = []
for n, d in net.nodes(data=True):
    if count == 0:
        list_node = list(d.keys())
        count += 1
        continue
    break

with open(".\dataset\Enron\EnronNode.csv", "w", newline="") as csvfile:
    fieldnames = list_node
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for n, d in net.nodes(data=True):
        writer.writerow(d)
print("done!")
