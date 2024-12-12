import csv
import networkx as nx
import matplotlib.pyplot as plt
import random  # For generating random colors
import pandas as pd  # For handling degree count
import powerlaw  # For power law fitting and comparison
from pyalex import Works

# Function to create the collaboration network graph
def create_collaboration_network(max_authors=40000):
    G = nx.Graph()
    pager = Works().search_filter(title="")  # Search filter with an empty title for all works

    # Variables to track works and authors
    author_work_mapping = {}
    work_to_authors = {}
    unique_id = 0

    # Collect data from OpenAlex
    for page in pager.paginate(per_page=100):  # Fetch 100 works per page
        for work in page:
            work_title = work.get("title", "N/A")
            authors = work.get("authorships", [])
            
            # Track authors for this specific work
            current_authors = []
            for author in authors:
                if author.get("author"):
                    author_name = author["author"]["display_name"]
                    
                    # Assign unique ID if author is new
                    if author_name not in author_work_mapping:
                        author_work_mapping[author_name] = unique_id
                        unique_id += 1
                    
                    # Track the author ID for this work
                    current_authors.append(author_work_mapping[author_name])

            # Map work to authors
            work_to_authors[work_title] = current_authors

            # Stop if max authors limit is reached
            if len(author_work_mapping) >= max_authors:
                break
        if len(author_work_mapping) >= max_authors:
            break

    # Create edges by connecting authors with the same work
    for work, authors in work_to_authors.items():
        for i in range(len(authors)):
            for j in range(i + 1, len(authors)):
                G.add_edge(authors[i], authors[j])

    # Remove nodes with degree = 100
    nodes_to_remove = [node for node, degree in G.degree() if degree == 100]
    G.remove_nodes_from(nodes_to_remove)
    
    return G

# Function to create a regular lattice network
def create_regular_lattice_network(n, k):
    # Create a regular lattice network where each node is connected to k neighbors
    lattice = nx.watts_strogatz_graph(n, k, 0)  # Regular lattice: rewiring probability = 0
    return lattice

# Function to compare degree distributions with Power Law
def compare_with_powerlaw(graph):
    # Calculate degree sequence for the co-authorship network
    deg_sequence = [d for _, d in graph.degree()]
    fit = powerlaw.Fit(deg_sequence, discrete=True)
    print("Co-Authorship Network:")
    print(f"  Alpha (Power-Law Exponent): {fit.alpha:.2f}")
    print(f"  KS Distance: {fit.D:.2f}")

    # Generate a random graph G(n, p)
    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()
    p = 2 * total_edges / (total_nodes * (total_nodes - 1))  # Probability for G(n, p)
    random_graph = nx.erdos_renyi_graph(total_nodes, p)

    # Calculate degree sequence for the random graph
    random_deg_sequence = [d for _, d in random_graph.degree()]
    random_fit = powerlaw.Fit(random_deg_sequence, discrete=True)
    print("Random Graph G(n, p):")
    print(f"  Alpha (Power-Law Exponent): {random_fit.alpha:.2f}")
    print(f"  KS Distance: {random_fit.D:.2f}")

    # Create a regular lattice network with the same number of nodes and edges
    avg_degree = int(2 * total_edges / total_nodes)  # Calculate average degree
    regular_lattice = create_regular_lattice_network(total_nodes, avg_degree)

    # Calculate degree sequence for the regular lattice
    lattice_deg_sequence = [d for _, d in regular_lattice.degree()]
    if len(lattice_deg_sequence) > 0:  # Only fit if degree sequence is non-empty
        lattice_fit = powerlaw.Fit(lattice_deg_sequence, discrete=True)
        print("Regular Lattice Network:")
        print(f"  Alpha (Power-Law Exponent): {lattice_fit.alpha:.2f}")
        print(f"  KS Distance: {lattice_fit.D:.2f}")

    # Plot the degree distributions
    plt.figure(figsize=(12, 8))
    
    # Co-authorship network
    fit.power_law.plot_pdf(label="Co-Authorship Network (Power Law)", linestyle='-', color='b')
    
    # Random graph
    random_fit.power_law.plot_pdf(label="Random Graph G(n, p) (Power Law)", linestyle='--', color='r')
    
    # Regular lattice
    if len(lattice_deg_sequence) > 0:
        plt.hist(lattice_deg_sequence, bins=range(min(lattice_deg_sequence), max(lattice_deg_sequence) + 1),
                 density=True, label="Regular Lattice Network", color='g', alpha=0.6)

    plt.xlabel('Degree', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Degree Distribution: Power Law Comparison', fontsize=16)
    plt.legend(fontsize=12)
    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Main execution
if __name__ == "__main__":
    # Create the collaboration network graph
    collaboration_graph = create_collaboration_network(max_authors=40000)

    # Analyze and compare with Power Law
    compare_with_powerlaw(collaboration_graph)
