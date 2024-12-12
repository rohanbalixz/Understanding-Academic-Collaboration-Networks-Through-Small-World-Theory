import networkx as nx
import matplotlib.pyplot as plt

# Calculate the probability p for G(n, p) using the empirical graph
n = G.number_of_nodes()
m = G.number_of_edges()
p = (2 * m) / (n * (n - 1)) if n > 1 else 0  # Ensure valid p

# Generate G(n, p) random graph
random_graph = nx.erdos_renyi_graph(n, p, seed=42)

# Metrics for the random graph
random_global_clustering = nx.transitivity(random_graph)
random_avg_path_length = (
    nx.average_shortest_path_length(random_graph) if nx.is_connected(random_graph) else None
)

# Metrics for the real co-authorship network
real_global_clustering = nx.transitivity(G)
real_avg_path_length = (
    nx.average_shortest_path_length(G) if nx.is_connected(G) else None
)

# Plot the comparison bar chart
metrics = ["Clustering Coefficient", "Avg Path Length"]
real_metrics = [real_global_clustering, real_avg_path_length]
random_metrics = [random_global_clustering, random_avg_path_length]

plt.figure(figsize=(8, 6))
x = range(len(metrics))

plt.bar(x, real_metrics, width=0.4, label="Real Network", color="blue", alpha=0.7)
plt.bar([i + 0.4 for i in x], random_metrics, width=0.4, label="Random Network", color="orange", alpha=0.7)

# Add labels, title, and legend
plt.xticks([i + 0.2 for i in x], metrics)
plt.ylabel("Metric Value")
plt.title("Comparison of Real Co-Authorship Network vs Random G(n, p) Network")
plt.legend()
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.show()
