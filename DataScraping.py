from pyalex import Works
import csv

# Initialize an empty list to hold data
data = []

# Set up the search and pagination parameters
pager = Works().search_filter(title="")  # A search filter with an empty title for all works

# Loop through pages and collect data
for page in pager.paginate(per_page=100):  # Set the number of results per page
    for work in page:
        work_title = work.get("title", "N/A")
        authors = work.get("authorships", [])
        
        # Collect author names
        author_names = ", ".join(author["author"]["display_name"] for author in authors if author.get("author"))
        
        # Append to data list
        data.append([author_names, work_title])
        
        # Stop if we reach the desired number of rows
        if len(data) >= 1000:
            break
    if len(data) >= 1000:
        break

# Write the collected data to a CSV file
with open("works_authors.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Authors", "Works"])  # Write header
    writer.writerows(data)  # Write data

print("CSV file created: works_authors.csv")
