import collections
from collections import Counter
import networkx as nx
import pandas as pd
import csv

TimeList = []
dict_node = {}
rank_node_dict = {}
weight_node_dict = {}
indegree_nodes = {}
time_node_dict = {}
Allnode = set()
All_node_ranks = []


def normalizing(min_x, max_x, x):
    x_prime = 0
    # x_prime =(2 * (x - min_x)/(max_x - min_x))-1
    x_prime = (20 * (x - min_x) / (max_x - min_x)) - 10
    # x_prime = (x - min_x) / (max_x - min_x)
    return x_prime


def compute_rank(weighted_list, pr_dict):
    rank_avg = 0
    rank_sum = 0
    for items in weighted_list:
        # print(pr_dict[items[0]])
        rank_sum += pr_dict[items[0]] * items[1]
    rank_avg = rank_sum / len(weighted_list)
    All_node_ranks.append(rank_avg)
    return rank_avg


# dataset/BitcoinAlpha/bitcoinalpha.csv
address = "dataset/BitcoinAlpha/bitcoinalpha.csv"
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
pr = nx.pagerank(G, alpha=0.85)
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
            indegree_nodes[int(row[1])].append([int(row[0]), int(row[2])])
        except:
            dict_node[int(row[1])] = [int(row[2])]
            indegree_nodes[int(row[1])] = [[int(row[0]), int(row[2])]]

    for k, v in indegree_nodes.items():
        # pr_dict[v] page rank of node v (indegree nodes)
        z = compute_rank(v, pr)
        rank_node_dict[int(k)] = z

# Normalizing between [-1, 1] x′′=(2*(x−minx)/(maxx−minx))-1
min_x = min(All_node_ranks)
max_x = max(All_node_ranks)

for k, v in rank_node_dict.items():
    rank_node_dict[k] = normalizing(min_x, max_x, v)

list_item = []
neg = 0
pos = 0
for k, v in rank_node_dict.items():
    list_item.append(v)
counts = Counter(list_item)
z = collections.OrderedDict(sorted(counts.items()))
print(z)
for k, v in dict(z).items():

    if int(k) < 0:
        neg += int(v)
    else:
        pos += int(v)
# print(neg/pos * 100)
print(neg / (neg + pos) * 100)
exit()


# rank zero means unknown
"""
for items in unlabeled_nodes:
    unlabeled_rank[int(items)]=0
nx.set_node_attributes(G, unlabeled_rank,'rank')
"""
