import collections
import math
from collections import Counter
import random as rand

import networkx as nx
import numpy as np
import pandas as pd
import csv

from matplotlib import pyplot as plt

TimeList = []
dict_node = {}
rank_node_dict = {}
unlabeled_rank = {}
unlabeled_weight = {}
weight_node_dict = {}
time_node_dict = {}
Allnode = set()


def find_avg_intensity(k):

    avg = sum(k) / len(k)
    if round(avg) == 0:
        return round(avg) - 1
    return round(avg)


def dice_throw_avg(k):
    sequence = [-1, -2, -3, 4, 5, 6]
    rand_idx = rand.randrange(len(sequence))
    avg = sum(k) / len(k)
    x = sequence[rand_idx]
    if round(avg) == 0:
        if x > 0:
            return round(avg) + 1
        else:
            return round(avg) - 1
    return round(avg)
    # Declaring the sequence


def biased_regression_avg(address):
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
                dict_node[int(row[1])].append(int(row[2]))
            except:
                dict_node[int(row[1])] = [int(row[2])]

        for k, v in dict_node.items():

            if len(set(v)) > 1:
                z = find_avg_intensity(v)
                rank_node_dict[int(k)] = z

            else:
                rank_node_dict[int(k)] = v[0]

    return rank_node_dict


def unbiased_regression_avg(address):
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
                dict_node[int(row[1])].append(int(row[2]))
            except:
                dict_node[int(row[1])] = [int(row[2])]

        for k, v in dict_node.items():

            if len(set(v)) > 1:
                z = dice_throw_avg(v)
                rank_node_dict[int(k)] = int(z)

            else:
                rank_node_dict[int(k)] = int(v[0])

    return rank_node_dict


# dataset/BitcoinAlpha/bitcoinalpha.csv
# dataset/BitcoinOTC/soc-sign-bitcoinotc.csv
address = "dataset/BitcoinOTC/soc-sign-bitcoinotc.csv"
df = pd.read_csv(address)
df = df.sort_values(by=["TIME"])
# writing into the file
G = nx.from_pandas_edgelist(
    df,
    source="SOURCE",
    target="TARGET",
    edge_attr=["RATING", "TIME"],
    create_using=nx.MultiDiGraph(),
)

rank = biased_regression_avg(address)
# rank= biased_regression_avg(address)

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
    if int(k) < 0:
        neg += int(v)
    else:
        pos += int(v)
# print(neg/pos * 100)
print(neg / (neg + pos) * 100)
print(neg)

nx.set_node_attributes(G, rank, "rank")


unlabeled_nodes = list(Allnode.difference(set(dict_node.keys())))
print(len(set(Allnode)))
print(len(unlabeled_nodes))


"""
with open( "dataset/BitcoinOTC/OTC_node_order.txt", 'w') as f:
    f.write('\n'.join(TimeList))
    f.write('\n') # newline at the end of file

#rank zero means unknown
for items in unlabeled_nodes:
    unlabeled_rank[int(items)]=0
nx.set_node_attributes(G, unlabeled_rank,'rank')
"""
# dataset/BitcoinOTC/soc-sign-bitcoinotc.csv/RegressionBitcoinOTC.graphml
nx.write_graphml_lxml(
    G, "dataset/BitcoinOTC/regression_biased/OTC_regression_biased.graphml"
)
