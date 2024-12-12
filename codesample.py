from pyalex import Works
import csv
import networkx as nx
import matplotlib.pyplot as plt

# Initialize variables
data = []
unique_id = 0  # Start unique identifier from 0
author_work_mapping = {}  # To map authors to their unique IDs and works
work_to_authors = {}  # To map works to their respective authors

# Set up the search and pagination parameters
pager = Works().search_filter(title="")  # Search filter with an empty title for all works

# Loop through pages and collect data
for page in pager.paginate(per_page=100):  # Set the number of results per page
    for work in page:
        work_title = work.get("title", "N/A")
        authors = work.get("authorships", [])
        
        # Track authors for this specific work
        current_authors = []
        
        for author in authors:
            if author.get("author"):
                author_name = author["author"]["display_name"]
                
                # Assign a unique ID if the author is new
                if author_name not in author_work_mapping:
                    author_work_mapping[author_name] = {
                        "id": unique_id,
                        "works": []
                    }
                    unique_id += 1
                
                # Add the author to the current work's authors
                current_authors.append(author_work_mapping[author_name]["id"])
                
                # Add the work to the author's list of works
                author_work_mapping[author_name]["works"].append(work_title)
        
        # Map the current work to its authors
        work_to_authors[work_title] = current_authors
        
        # Stop if we reach the desired number of rows
        if len(author_work_mapping) >= 100000:
            break
    if len(author_work_mapping) >= 100000:
        break

# Generate edges for the graph by connecting authors with the same work
edges = []
for work, authors in work_to_authors.items():
    for i in range(len(authors)):
        for j in range(i + 1, len(authors)):
            edges.append((authors[i], authors[j]))

# Create the graph
G = nx.Graph()
G.add_edges_from(edges)

# Analyze graph properties (Optional)
print(f"Number of nodes: {G.number_of_nodes()}")
print(f"Number of edges: {G.number_of_edges()}")

# Plot the graph
plt.figure(figsize=(10, 10))
nx.draw_spring(G, node_size=100, node_color="blue", with_labels=True, font_size=8)
plt.title("Co-Authorship Network (Shared Works)")
plt.show()

# Save the graph
nx.write_edgelist(G, "co_authorship_graph.edgelist")
print("Graph created and saved as 'co_authorship_graph.edgelist'.")

# Save author-work data to CSV
with open("authors_works_unique.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Unique ID", "Author", "Work Title"])  # Write header
    for author, details in author_work_mapping.items():
        for work in details["works"]:
            writer.writerow([details["id"], author, work])

print("CSV file created: authors_works_unique.csv")
