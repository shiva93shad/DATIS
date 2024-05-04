import collections
import math
from collections import Counter
import random as rand

import networkx as nx
import numpy as np
import pandas as pd
import csv

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
    # Declaring the sequence


def quadritic_regression(address):
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
                z = quadritic_voting(v)
                rank_node_dict[int(k)] = z

            else:
                rank_node_dict[int(k)] = v[0]

    return rank_node_dict


def quadritic_voting(k):
    sequence = [-1, -2, -3, 4, 5, 6]
    rand_idx = rand.randrange(len(sequence))
    x = sequence[rand_idx]
    total = 0
    pos = 0
    neg = 0
    for i in k:
        if i < 0:
            neg += 1
        else:
            pos += 1

    if (
        len(k) == pos or len(k) == neg
    ):  # this means if all votes are either positive or negative, then find avg
        total = find_avg_intensity(k)
    else:
        for i in k:
            if i < 0:
                total += i
            else:
                total += math.ceil(math.sqrt(i))
        total = total / len(k)
        if round(total) == 0:
            if round(total) == 0:
                if x > 0:
                    return round(total) + 1
                else:
                    return round(total) - 1
    return round(total)


# dataset/BitcoinAlpha/bitcoinalpha.csv
address = "dataset/BitcoinAlpha/bitcoinalpha.csv"
df = pd.read_csv(address)
df = df.sort_values(by=["TIME"])
# writing into the file
G = nx.from_pandas_edgelist(
    df,
    source="SOURCE",
    target="TARGET",
    edge_attr=["RATING"],
    create_using=nx.MultiDiGraph(),
)

field_names = ["pagerank"]
"""
with open('Names.csv', 'w',newline='') as csvfile:
    writer = csv.writer(csvfile)
    for key, value in weighted_pagerank.items():
        writer.writerow([key, value])
"""
# rank= biased_regression_avg(address)
list_item = []
rank = quadritic_regression(address)
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
    if k < 0:
        neg += v
    else:
        pos += v
# print(neg/pos * 100)
print(neg / (neg + pos) * 100)
print(neg)

nx.set_node_attributes(G, rank, "rank")


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
    G, "dataset/BitcoinAlpha/quadritic_regression/Alpha_quadritic_regression.graphml"
)
