import matplotlib
import networkx as nx
# Create a directed graph
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('TkAgg')
# Add edges and nodes to your graph
# (Replace this with your graph creation logic)

def wcc_scc(G):
    wcc = list(nx.weakly_connected_components(G))

    # Find strongly connected components
    scc = list(nx.strongly_connected_components(G))
    print(len(wcc))
    print(len(scc))

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, font_weight='bold')
    plt.title('Graph with Weakly Connected Components')
    plt.savefig("wcc.png")


    # Print information about weakly connected components
    print("Weakly Connected Components:")
    for i, component in enumerate(wcc, 1):
        print(f"Component {i}: {component}")

    # Plot the graph and highlight strongly connected components with a new layout
    plt.figure()
    pos_scc = nx.spring_layout(G.reverse())  # Reverse the graph for SCC layout
    nx.draw(G, pos_scc, with_labels=True, font_weight='bold')
    plt.savefig("scc.png")
    plt.title('Graph with Strongly Connected Components')

    # Print information about strongly connected components
    print("Strongly Connected Components:")
    for i, component in enumerate(scc, 1):
        print(f"Component {i}: {component}")

#dataset/BitcoinOTC/soc-sign-bitcoinotc.csv
#dataset/BitcoinAlpha/bitcoinalpha.csv
#dataset/Epinion/soc-sign-epinions.txt
address='../dataset/BitcoinOTC/soc-sign-bitcoinotc.csv'

df = pd.read_csv(address)
#df=df.sort_values(by=['TIME'])
G = nx.from_pandas_edgelist(df, source='SOURCE', target='TARGET', edge_attr=['RATING'], create_using=nx.DiGraph())


wcc_scc(G)
exit()

# Check if the graph is weakly connected
is_weakly_connected = nx.is_weakly_connected(G)

# Check if the graph is strongly connected
is_strongly_connected = nx.is_strongly_connected(G)

# Calculate the percentage of nodes in the largest weakly connected component
if is_weakly_connected:
    wcc = max(nx.weakly_connected_components(G), key=len)
    wcc_percentage = len(wcc) / len(G.nodes()) * 100
    print(f"Largest Weakly Connected Component: {wcc_percentage:.2f}%")

# Calculate the percentage of nodes in the largest strongly connected component
if is_strongly_connected:
    scc = max(nx.strongly_connected_components(G), key=len)
    scc_percentage = len(scc) / len(G.nodes()) * 100
    print(f"Largest Strongly Connected Component: {scc_percentage:.2f}%")