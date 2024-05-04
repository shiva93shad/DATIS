import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import numpy as np

#../dataset/BitcoinOTC/soc-sign-bitcoinotc.csv
#../dataset/BitcoinOTC/bias_deserve/OTC_bias_deserve.csv

#../dataset/BitcoinAlpha/bitcoinalpha.csv
#../dataset/BitcoinAlpha/bias_deserve/Alpha_bias_deserve.csv
def merger():
    data = pd.read_csv('../dataset/BitcoinOTC/soc-sign-bitcoinotc.csv', header=None,
                       names=['SOURCE', 'TARGET', 'RANK', 'TIME'], skiprows=1)
    data2 = pd.read_csv('../dataset/BitcoinOTC/bias_deserve/OTC_bias_deserve.csv',
                        usecols=['_nx_name', 'bias', 'deserve'])
    data2.rename(columns={'TARGET': '_nx_name'}, inplace=True)
    print(
        data2.rename(columns={'_nx_name': 'TARGET'}, inplace=True))
    data2['deserve'] = data2['deserve'].apply(lambda x: x * 10)
    merger_df = pd.merge(data, data2, on='TARGET')
    return data,merger_df


data, merger_df=merger()
pos_df = merger_df[merger_df['deserve'] >0]
neg_df = merger_df[merger_df['deserve'] <0]
# Create a directed graph from the dataset
G = nx.DiGraph()
for _, row in neg_df.iterrows():
    G.add_edge(row['SOURCE'], row['TARGET'], weight=row['RANK'], timestamp=row['TIME'])

# Convert timestamps to seconds
timestamps = neg_df['TIME']

# Define time windows in seconds (2 weeks)
window_size = 4 * 7 * 24 * 60 * 60  # 4 weeks in seconds

# Create a dictionary to store temporal edge weight data
nodes = list(G.nodes())
temporal_edge_weights = {node: {} for node in nodes}

# Calculate temporal edge weights for each node and time window
start_time = min(timestamps)
end_time = max(timestamps)
current_time = start_time
num_windows = 0

while current_time < end_time:
    window_start = current_time
    window_end = current_time + window_size
    window_edge_weights = {}

    for node in nodes:
        total_weight = 0
        for _, _, d in G.in_edges(node, data=True):
            if window_start <= d['timestamp'] <= window_end:
                total_weight += d['weight']
        window_edge_weights[node] = total_weight

    temporal_edge_weights[num_windows] = window_edge_weights

    current_time += window_size
    num_windows += 1


# ... (previous code remains unchanged)

# Create a stacked bar chart
fig, ax = plt.subplots(figsize=(14, 8))  # Increase the figure size

bottom = np.zeros(num_windows)  # Initialize the bottom of each bar

for node in nodes:
    edge_weights = [temporal_edge_weights[window][node] for window in range(num_windows)]
    ax.bar(range(num_windows), edge_weights, bottom=bottom, label=f'Node {node}')

    bottom += edge_weights  # Update the bottom for the next iteration

ax.set_xlabel('Time Window', fontsize=16)  # Increase x-axis label font size
ax.set_ylabel('Cumulative Edge Weights', fontsize=16)  # Increase y-axis label font size

# Set x-axis ticks every five items
ax.set_xticks(range(0, num_windows, 5))
ax.set_xticklabels(['{}'.format(i + 1) for i in range(0, num_windows, 5)], rotation=90, fontsize=12)

# Set y-axis font size
ax.tick_params(axis='y', labelsize=12)

# Position legend below the chart
#ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5, fontsize=12)  # Adjust the position as needed
fig.tight_layout()

# Save the figure as a PDF in the 'output' folder
#OTC_neg_node_stackedbar.png
#OTC_pos_node_stackedbar.png
#Alfa_neg_node_stackedBar.png
#Alfa_pos_node_stackedBar.png
plt.savefig('./pic/OTC_neg_node_stackedbar.png', bbox_inches='tight')

plt.show()


'''
# Create a stacked bar chart
plt.figure(figsize=(10, 6))
bottom = np.zeros(num_windows)  # Initialize the bottom of each bar

for node in nodes:
    edge_weights = [temporal_edge_weights[window][node] for window in range(num_windows)]
    plt.bar(range(num_windows), edge_weights, bottom=bottom, label=f'Node {node}')
    bottom += edge_weights  # Update the bottom for the next iteration

#plt.title('Stacked Bar Chart of received ranks for negative ranked nodes in Bitcoin OTC Dataset (4-Week Windows)')
plt.xlabel('Time Window')
plt.ylabel('Cumulative Edge Weights')
plt.xticks(range(num_windows), ['{}'.format(i + 1) for i in range(num_windows)], rotation=90,fontsize=6)

# Position legend below the chart
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=5)  # Adjust the position as needed

plt.tight_layout()
plt.show()
'''