import collections

import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import pandas as pd
import numpy as np
import matplotlib.colors as mcolors
#dataset/BitcoinOTC/soc-sign-bitcoinotc.csv
#dataset/BitcoinAlpha/bitcoinalpha.csv
data = pd.read_csv('../dataset/BitcoinAlpha/bitcoinalpha.csv', header=None,
                       names=['SOURCE', 'TARGET', 'RANK', 'TIME'], skiprows=1)
# Create a directed graph from the dataset
G = nx.DiGraph()
for _, row in data.iterrows():
    G.add_edge(row['SOURCE'], row['TARGET'], weight=row['RANK'], timestamp=row['TIME'])

# Convert timestamps to seconds
timestamps = data['TIME']

# Define time windows in seconds (2 weeks)
window_size = 4 * 7 * 24 * 60 * 60  # 4 weeks in seconds

# Create a directed graph from the dataset
# Create a dictionary to store temporal edge weight data
nodes = list(G.nodes())
temporal_edge_weights = {node: {} for node in nodes}

# Calculate temporal edge weights for each node and time window
start_time = min(timestamps)
end_time = max(timestamps)
current_time = start_time
num_windows = 0

# Calculate positive and negative ranks for each node in each time window
temporal_positive_ranks = collections.defaultdict(dict)
temporal_negative_ranks = collections.defaultdict(dict)

while current_time < end_time:
    window_start = current_time
    window_end = current_time + window_size
    window_edge_weights = {}

    for node in nodes:
        positive_rank = 0
        negative_rank = 0

        total_weight = 0
        for _, _, d in G.in_edges(node, data=True):
            if window_start <= d['timestamp'] <= window_end:
                total_weight += d['weight']

                if d['weight'] > 0:
                    positive_rank += d['weight']
                if d['weight'] < 0:
                    negative_rank += d['weight']
                    #print('yes')
        window_edge_weights[node] = total_weight
        '''
             Calculate positive and negative ranks based on your criteria and store in temporal_positive_ranks and temporal_negative_ranks
        '''
        temporal_positive_ranks[num_windows][node] = positive_rank
        temporal_negative_ranks[num_windows][node] = negative_rank

    temporal_edge_weights[num_windows] = window_edge_weights

    current_time += window_size
    num_windows += 1

'''
for k,v in temporal_negative_ranks.items():
    for ke,va in v.items():
        if va<0:
            print(va)
'''

# Calculate correlation matrices for positive and negative ranks
positive_corr_matrix = np.zeros((num_windows, num_windows))
negative_corr_matrix = np.zeros((num_windows, num_windows))


for window1 in range(num_windows):
    for window2 in range(num_windows):
        # Calculate pearson correlation between positive ranks for window1 and window2
        # Store the correlation value in positive_corr_matrix
        positive_ranks_window1 = [temporal_positive_ranks[window1][node] for node in nodes]
        positive_ranks_window2 = [temporal_positive_ranks[window2][node] for node in nodes]
        positive_corr = np.corrcoef(positive_ranks_window1, positive_ranks_window2)[0, 1]
        #print(positive_corr)
        positive_corr_matrix[window1, window2] = positive_corr

        # Calculate pearson correlation between negative ranks for window1 and window2
        # Store the correlation value in negative_corr_matrix
        negative_ranks_window1 = [temporal_negative_ranks[window1][node] for node in nodes]
        negative_ranks_window2 = [temporal_negative_ranks[window2][node] for node in nodes]
        negative_corr = np.corrcoef(negative_ranks_window1, negative_ranks_window2)[0, 1]
        print(negative_corr)
        negative_corr_matrix[window1, window2] = negative_corr


# Create a figure and axes
#fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

# Create two separate figures and axes

# Create two separate figures and axes with specified sizes
fig1, ax1 = plt.subplots(figsize=(7, 7))
fig2, ax2 = plt.subplots(figsize=(7, 7))

# Plot the correlation heatmaps for positive and negative ranks
cmap = plt.cm.coolwarm  # You can choose a different colormap

positive_corr_heatmap = ax1.imshow(positive_corr_matrix, cmap=cmap, vmin=-1, vmax=1)
negative_corr_heatmap = ax2.imshow(negative_corr_matrix, cmap=cmap, vmin=-1, vmax=1)

# Add colorbars
cbar_positive = fig1.colorbar(positive_corr_heatmap, ax=ax1)
cbar_negative = fig2.colorbar(negative_corr_heatmap, ax=ax2)

# Set axis labels
ax1.set_xlabel('Window Number', fontsize=12)
ax1.set_ylabel('Window Number', fontsize=12)
ax2.set_xlabel('Window Number', fontsize=12)
ax2.set_ylabel('Window Number', fontsize=12)

# Set titles
ax1.set_title('Positive Rank Correlation Heatmap', fontsize=14)
ax2.set_title('Negative Rank Correlation Heatmap', fontsize=14)

# Add window numbers as tick labels every 5 items
window_numbers = np.arange(0, num_windows, 5)
ax1.set_xticks(window_numbers)
ax1.set_yticks(window_numbers)
ax2.set_xticks(window_numbers)
ax2.set_yticks(window_numbers)
ax1.set_xticklabels(window_numbers, fontsize=10)
ax1.set_yticklabels(window_numbers, fontsize=10)
ax2.set_xticklabels(window_numbers, fontsize=10)
ax2.set_yticklabels(window_numbers, fontsize=10)

# Rotate tick labels for better visibility
plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

# Adjust the layout to minimize white space
fig1.tight_layout()
fig2.tight_layout()

# Display the plots
plt.show()

'''
fig1, ax1 = plt.subplots(figsize=(7, 7))
fig2, ax2 = plt.subplots(figsize=(7, 7))

# Plot the correlation heatmaps for positive and negative ranks
cmap = plt.cm.coolwarm  # You can choose a different colormap

#cmap_with_nan = mcolors.ListedColormap(['green'] + [cmap(i) for i in range(cmap.N)])
cmap.set_bad(color='white')

positive_corr_heatmap = ax1.imshow(positive_corr_matrix, cmap=cmap, vmin=-1, vmax=1)
negative_corr_heatmap = ax2.imshow(negative_corr_matrix, cmap=cmap, vmin=-1, vmax=1)

# Add colorbars
cbar_positive = fig1.colorbar(positive_corr_heatmap, ax=ax1)
cbar_negative = fig2.colorbar(negative_corr_heatmap, ax=ax2)

# Set axis labels
ax1.set_xlabel('Window Number', fontsize=12)
ax1.set_ylabel('Window Number', fontsize=12)
ax2.set_xlabel('Window Number', fontsize=12)
ax2.set_ylabel('Window Number', fontsize=12)

# Set titles
ax1.set_title('Positive Rank Correlation Heatmap', fontsize=14)
ax2.set_title('Negative Rank Correlation Heatmap', fontsize=14)

# Add window numbers as tick labels every 5 items
window_numbers = np.arange(num_windows)
ax1.set_xticks(np.arange(0, num_windows, 5))
ax1.set_yticks(np.arange(0, num_windows, 5))
ax2.set_xticks(np.arange(0, num_windows, 5))
ax2.set_yticks(np.arange(0, num_windows, 5))
ax1.set_xticklabels(window_numbers[::5], fontsize=10)
ax2.set_xticklabels(window_numbers[::5], fontsize=10)
ax1.set_yticklabels(window_numbers[::5], fontsize=10)
ax2.set_yticklabels(window_numbers[::5], fontsize=10)

# Rotate tick labels for better visibility
plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")
plt.setp(ax2.get_xticklabels(), rotation=45, ha="right")

# Adjust tight layout parameters to minimize white space
plt.tight_layout(pad=1, h_pad=0.5, w_pad=0.5)

# Display the plot
plt.show()
'''
'''
# Set axis labels
ax1.set_xlabel('Window Number')
ax1.set_ylabel('Window Number')
ax2.set_xlabel('Window Number')
ax2.set_ylabel('Window Number')

# Set titles
ax1.set_title('Positive Rank Correlation Heatmap')
ax2.set_title('Negative Rank Correlation Heatmap')

# Add window numbers as tick labels
window_numbers = np.arange(num_windows)
ax1.set_xticks(np.arange(num_windows))
ax1.set_yticks(np.arange(num_windows))
ax2.set_xticks(np.arange(num_windows))
ax2.set_yticks(np.arange(num_windows))
ax1.set_xticklabels(window_numbers)
ax2.set_xticklabels(window_numbers)

ax1.set_yticklabels(window_numbers,fontsize=5)
ax2.set_yticklabels(window_numbers,fontsize=5)

# Rotate tick labels for better visibility
plt.setp(ax1.get_xticklabels(), rotation=90, ha="right",fontsize=5)
plt.setp(ax2.get_xticklabels(), rotation=90, ha="right",fontsize=5)

# Display the plot
plt.tight_layout()
plt.show()

'''


'''
# Create correlation heatmaps
plt.figure(figsize=(14, 7))

plt.subplot(1, 2, 1)
sns.heatmap(positive_corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', xticklabels=num_windows, yticklabels=num_windows)
plt.title('Correlation Heatmap for Positive Ranks')
plt.xlabel('Time Windows')
plt.ylabel('Time Windows')

plt.subplot(1, 2, 2)
sns.heatmap(negative_corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', xticklabels=num_windows, yticklabels=num_windows)
plt.title('Correlation Heatmap for Negative Ranks')
plt.xlabel('Time Windows')
plt.ylabel('Time Windows')

plt.tight_layout()
plt.show()
'''

