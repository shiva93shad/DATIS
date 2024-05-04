import collections
import csv
from collections import Counter

import networkx as nx
import numpy as np
import pandas as pd

G = nx.DiGraph()
DG = nx.DiGraph()
Allnode = set()
import matplotlib.pyplot as plt

dict_node = {}
rank_node_dict = {}
unlabeled_rank = {}
unlabeled_weight = {}
weight_node_dict = {}
time_node_dict = {}
TimeList = []


def find_majority_voting(k):
    myMap = {}
    maximum = ("", 0)  # (occurring element, occurrences)
    for n in k:
        if n in myMap:
            myMap[n] += 1
        else:
            myMap[n] = 1

        # Keep track of maximum on the go
        if myMap[n] > maximum[1]:
            maximum = [int(n), myMap[n]]

    return maximum


def majority_vote_node(address):
    c = 0
    with open(address) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        for row in csv_reader:
            if c == 0:
                c += 1
                continue
            Allnode.add(row[0])
            Allnode.add(row[1])
            TimeList.append(row[0])
            TimeList.append(row[1])
            try:
                # otc_bitcoin
                dict_node[row[1]].append(0 if int(row[2]) > 0 else 1)
                # alpha_bitcoin
                # dict_node[row[1]].append(row[2])
            except:
                # otc_bitcoin
                dict_node[row[1]] = [0 if int(row[2]) > 0 else 1]
            # alpha_bitcoin
            # dict_node[row[1]]=[row[2]]

        count = 0
        node_c = 0
        for k, v in dict_node.items():

            node_c += 1
            if len(set(v)) > 1:
                z = find_majority_voting(v)
                rank_node_dict[int(k)] = int(z[0])
                weight_node_dict[int(k)] = z[1]

            else:
                rank_node_dict[int(k)] = int(v[0])
                weight_node_dict[int(k)] = len(v)
                count += 1

    return (rank_node_dict, weight_node_dict)


address = "dataset/BitcoinAlpha/bitcoinalpha.csv"
rank, weight = majority_vote_node(address)

list_item = []
neg = 0
pos = 0

for k, v in rank.items():
    list_item.append(v)
counts = Counter(list_item)
z = collections.OrderedDict(sorted(counts.items()))
print(z)
for k, v in dict(z).items():
    print(k)
    if int(k) == 1:
        neg += int(v)
    else:
        pos += int(v)
# print(neg/pos * 100)
print(neg / (neg + pos) * 100)
print(neg)
exit()


df = pd.read_csv("dataset/BitcoinAlpha/bitcoinalpha.csv")
df["RATING"] = np.where(df["RATING"] >= 1, 0, 1)
df = df.sort_values(by=["TIME"])

print(df)
# writing into the file
# df.to_csv(".\dataset\BitcoinAlpha\processed_bitcoinalpha.csv", index=False)
G = nx.from_pandas_edgelist(
    df,
    source="SOURCE",
    target="TARGET",
    edge_attr=["RATING", "TIME"],
    create_using=nx.MultiDiGraph(),
)


with open("dataset/BitcoinAlpha/node_order.txt", "w") as f:
    f.write("\n".join(TimeList))
    f.write("\n")  # newline at the end of file

nx.set_node_attributes(G, rank, "rank")
nx.set_node_attributes(G, weight, "weight")

unlabeled_nodes = list(Allnode.difference(set(dict_node.keys())))


for items in unlabeled_nodes:
    unlabeled_rank[int(items)] = 2
    unlabeled_weight[int(items)] = 0

nx.set_node_attributes(G, unlabeled_rank, "rank")
nx.set_node_attributes(G, unlabeled_weight, "weight")

nx.write_graphml_lxml(G, ".\dataset\BitcoinAlpha\majorityBitcoinAlpha.graphml")
for nodes in G.nodes(data=True):
    print(nodes)
