from pyalex import Works
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

# Function to fetch data from OpenAlex and create a graph
def fetch_graph_from_openalex(max_works=1000):
    G = nx.Graph()
    pager = Works().search_filter(title="")  # Search filter with an empty title for all works
    
    # Collect works and authors
    for page in pager.paginate(per_page=100):  # Fetch 100 works per page
        for work in page:
            authors = work.get("authorships", [])
            
            # Add edges between co-authors for each work
            author_ids = []
            for author in authors:
                if author.get("author"):
                    author_id = author["author"]["id"]
                    author_ids.append(author_id)
            
            # Create edges for co-authors
            for i in range(len(author_ids)):
                for j in range(i + 1, len(author_ids)):
                    G.add_edge(author_ids[i], author_ids[j])
            
            # Stop if the number of works exceeds the limit
            if len(G.nodes) >= max_works:
                break
        if len(G.nodes) >= max_works:
            break
    
    # Remove nodes with exactly 100 degrees
    nodes_to_remove = [node for node, degree in G.degree() if degree == 100]
    G.remove_nodes_from(nodes_to_remove)
    
    return G

# Function to compare degree distribution with G(n, p) and plot the graph
def compare_with_random_graph(graph):
    total_nodes = graph.number_of_nodes()
    total_edges = graph.number_of_edges()
    
    if total_nodes <= 1 or total_edges == 0:
        print("Graph is too small to proceed. Please check the data.")
        return

    # Degree sequence for our graph
    deg_sequence = [d for _, d in graph.degree()]
    
    # Calculate degree distribution for the input graph
    deg_count = pd.Series(deg_sequence).value_counts().sort_index()

    # Generate a G(n, p) random graph
    p = 2 * total_edges / (total_nodes * (total_nodes - 1))  # Probability for G(n, p)
    random_graph = nx.erdos_renyi_graph(total_nodes, p)
    
    # Degree sequence for the random graph
    random_deg_sequence = [d for _, d in random_graph.degree()]
    random_deg_count = pd.Series(random_deg_sequence).value_counts().sort_index()

    # Plot the degree distribution comparison
    plt.figure(figsize=(12, 8))  # Set the figure size for better scaling

    # Plot the degree distribution of the input graph
    deg_count.plot(kind='line', label="Co-Authorship Network", color='b')

    # Plot the degree distribution of the random graph
    random_deg_count.plot(kind='line', label="Random Graph G(n, p)", color='r')

    # Set plot labels and title
    plt.xlabel('Degree', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Degree Distribution Comparison', fontsize=16)

    # Customize tick parameters for better scaling
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)

    # Add a legend
    plt.legend(fontsize=12)

    # Add grid for better readability
    plt.grid(visible=True, which='both', linestyle='--', linewidth=0.5)

    # Show the plot
    plt.tight_layout()  # Adjust layout to prevent clipping
    plt.show()

# Main execution
if __name__ == "__main__":
    # Fetch graph data from OpenAlex
    G = fetch_graph_from_openalex(max_works=1000)

    # Compare degree distribution with G(n, p)
    compare_with_random_graph(G)
