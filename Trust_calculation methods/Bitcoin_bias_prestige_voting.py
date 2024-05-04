import collections
from collections import Counter
import networkx as nx
import pandas as pd
import csv

edgelist = []
all_node = []
bias = {}
deserve = {}
x_kj = 0
d_o = {}
d_i = {}


def prestige_deserve(sum, length):
    d = (1 / length) * sum
    return d


def bias_trust(sum, length):
    b = (1 / (2 * length)) * sum
    return b


def X_kj(bias, weight):
    x = bias * weight
    return x


count = 0
# dataset/BitcoinOTC/soc-sign-bitcoinotc.csv
# dataset/BitcoinAlpha/bitcoinalpha.csv
# dataset/Epinion/soc-sign-epinions.txt
address = "dataset/BitcoinOTC/soc-sign-bitcoinotc.csv"
df = pd.read_csv(address)
df = df.sort_values(by=["TIME"])
G = nx.from_pandas_edgelist(
    df,
    source="SOURCE",
    target="TARGET",
    edge_attr=["RATING", "TIME"],
    create_using=nx.MultiDiGraph(),
)

with open(address, "r") as file:
    for line in file.readlines():
        # print(line.strip().split(',')[2])
        if count == 0:
            count += 1
            continue

        from_node = int(line.strip().split(",")[0])
        to_node = int(line.strip().split(",")[1])
        weight = float(line.strip().split(",")[2])
        edgelist.append([from_node, to_node, weight])
        all_node.append(from_node)
        all_node.append(to_node)

        bias[from_node] = -1
        bias[to_node] = -1

        deserve[from_node] = -1
        deserve[to_node] = -1
        try:
            d_o[from_node].append([to_node, weight])
        except:
            d_o[from_node] = [[to_node, weight]]

        try:
            d_i[to_node].append([from_node, weight])
        except:
            d_i[to_node] = [[from_node, weight]]

# print(d_o[3])
final_dict = {x: d_o[x] for x in d_o if x in d_i}
print(final_dict.keys())
print(len(set(d_i) - set(final_dict)))

i = 1
all = list(set(all_node))
while i < 100:  # go on 5 iteration
    for node in all:
        sum = 0
        sum1 = 0
        try:
            for income in d_i[node]:  # for each edge [node,out,weight]
                w = income[1] / 10
                if X_kj(bias[income[0]], w) <= 0:
                    x_kj = 0
                else:
                    x_kj = abs(bias[income[0]])
                sum += w * (1 - x_kj)
            deserve[node] = prestige_deserve(sum, len(d_i[node]))
            # print(len(d_i[node]))
        except:
            continue

        try:
            for outgo in d_o[node]:

                w1 = outgo[1] / 10
                sum1 += w1 - deserve[outgo[0]]

            bias[node] = bias_trust(sum1, len(d_o[node]))
        except:
            continue
        # print(len(d_o[node]))

    i += 1
    print("iteration passed!")

# pd.DataFrame(d.items(), columns=['Date', 'DateValue'])
bias.update((x, y * 10) for x, y in bias.items())
deserve.update((x, y * 10) for x, y in deserve.items())
d = dict((k, v) for k, v in deserve.items() if v > 1)
# print(deserve)
print(len(d))
count = 0
for k, v in deserve.items():
    if v < -2:
        count += 1
print(count)
nx.set_node_attributes(G, bias, "bias")
nx.set_node_attributes(G, deserve, "deserve")

nx.write_graphml_lxml(G, "dataset/BitcoinOTC/bias_deserve/OTC_bias_deserve.graphml")


# convert the dataset to df and then to the networkx graph and then apply igraph on it.
# dataset/BitcoinOTC/bias_deserve
# dataset/BitcoinAlpha/bias_deserve
