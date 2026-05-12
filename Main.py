from sys import setswitchinterval
import copy
from OTN1 import OTN1
from OTN2 import OTN2
from Link import Link
from Service import Service
import networkx as nx
import matplotlib.pyplot as plt
import random
import pandas as pd
from math import ceil


# Set seed for reproducibility
random.seed(32) 

# Initialize nodes for the national network (assuming 10-15 nodes)
num_nodes = random.randint(10, 15)
nodes = [OTN2() for _ in range(num_nodes)]
nodes_1 = [OTN1() for _ in range(num_nodes)]

# Create graph
national_graph = nx.Graph()

# Add nodes to the graph
national_graph.add_nodes_from(nodes)

# Define a maximum of 15,20 links with distances between 50 and 400 km
num_links = random.randint(15, 20)
links = []
links_full = []
added_edges = set()

while len(links) < num_links:
    # Randomly select two distinct nodes
    node_a, node_b = random.sample(nodes, 2)

    # Ensure no duplicate links
    if (node_a, node_b) in added_edges or (node_b, node_a) in added_edges:
        continue

    # Generate a random link length between 50 km and 400 km
    distance = random.randint(50, 400) 

    # Create and store the Link object
    link = Link(starting_node=node_a, ending_node=node_b)
    links_full.append(link)

    # Add the link to the nodes in both directions
    node_a.add_link(link)
    node_b.add_link(link)

    links.append((node_a, node_b, distance))
    added_edges.add((node_a, node_b))

# Add weighted edges to the graph
national_graph.add_weighted_edges_from(links)

# Convert nodes to their `_node_id` for labeling
node_labels = {node: node._node_id for node in nodes}

# Display the generated national network graph details
df = pd.DataFrame([(l[0]._node_id, l[1]._node_id, l[2]) for l in links], columns=["Node A", "Node B", "Distance (km)"])
print(df)

# Use Kamada-Kawai layout for better spacing
pos = nx.kamada_kawai_layout(national_graph)

# Draw the graph with node IDs
plt.figure(figsize=(10, 6))
nx.draw(national_graph, pos, labels=node_labels, with_labels=True, node_size=500, node_color="lightblue", edge_color="gray", font_size=10)

# Draw edge labels with distances
edge_labels = {(u, v): f"{w} km" for u, v, w in links}
nx.draw_networkx_edge_labels(national_graph, pos, edge_labels=edge_labels, font_size=8)

# Show the graph
plt.title("National Network Graph")
plt.show()



shortest_path = []
shortest_edge = []


for node1 in nodes:
  for node2 in nodes:
    # Select two random nodes for shortest path calculation
    source_node = None
    target_node = None

    if node1 != node2:
      source_node = node1
      target_node = node2

    if source_node and target_node:
      # Compute shortest path using Dijkstra's algorithm (weighted by distance)
      shortest_path1 = nx.shortest_path(national_graph, source=source_node, target=target_node, weight='weight')

      # Convert path edges to Link objects
      shortest_path_edges = []
      for u, v in zip(shortest_path1[:-1], shortest_path1[1:]):
          # Find the correct Link object
          for link in u.links:
              if (link.starting_node == u and link.ending_node == v) or (link.starting_node == v and link.ending_node == u):
                  shortest_path_edges.append(link)
                  break
      shortest_edge.append(shortest_path_edges)
      shortest_path.append(shortest_path1)

      # Display results
      print("Shortest path nodes:", [node._node_id for node in shortest_path1])
      print("Shortest path edges:", [f"Link({link.starting_node._node_id}, {link.ending_node._node_id})" for link in shortest_path_edges])


for path in shortest_path:
  path.insert(0, nodes_1[path[0]._node_id - 1])


groom = False #for changing granularity (true for 10g and false for 100g)
OTN2.grooming = groom
Link.grooming = groom

random.seed(None)

flag = True
i = 1
j = 0
total_serv = []
transponders = []
total_cap = []
total_light = []
serv = 0

capacity = []
lightpath = []
num_tran = []

while flag:
    service_map = {}  # Dictionary to store services by path index

    for idx, path in enumerate(shortest_path):
        a = random.randint(0, 1)
        rate = 10 if a == 0 else 100

        service = Service(
            rate=rate,
            sd_pair=(path[0]._node_id, path[-1]._node_id),
            path_nodes=path,
            path_edges=[link._link_id for link in shortest_edge[idx]]
        )


        service_map[idx] = service  # Store service for this path
        path[0].add_service(service)

        # Check for capacity issues
        for node in nodes:
            if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                flag = False
                fail = node
                break

        if not flag:
            break

    if not flag:
        break


    # Assign services to links
    for idx, (path, edge_path) in enumerate(zip(shortest_path, shortest_edge)):
        for link in edge_path:
            link.add_service(service_map[idx])
            #j += 1

            # Check for capacity issues
            for node in nodes:
                if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                    flag = False
                    fail = node
                    break

            if not flag:
                break

        #j -= len(edge_path) - 1
        j += 1

        if not flag:
            break

    j -= len(path) - 1
    if j >= i*50:
      i += 1

      tran = 0
      for node in nodes:
        tran += node.num_transponders
      num_tran.append(tran)

      node_cap = 0
      for node in nodes:
        if node.used_capacity >= node.max_capacity:
          node_cap += node.max_capacity
        else:
          node_cap += node.used_capacity
      capacity.append(node_cap)


      light = 0
      for link in links_full:
        light += ceil(link.used_odus/5)
      lightpath.append(light)


    if not flag:
        break

    # Assign services to intermediate nodes
    for idx, path in enumerate(shortest_path):
        for node in path[1:]:  # Skip first node since it's already assigned
            node.add_service(service_map[idx])

            # Check for capacity issues
            for node in nodes:
                if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                    flag = False
                    fail = node
                    break

            if not flag:
                break

        if not flag:
            break

    if not flag:
        break




serv += j
total_serv.append(serv)



tran = 0
for node in nodes:
  tran += node.num_transponders

transponders.append(tran)

node_cap = 0

for node in nodes:
  if node.used_capacity >= node.max_capacity:
    node_cap += node.max_capacity
  else:
    node_cap += node.used_capacity

total_cap.append(node_cap)


light = 0
for link in links_full:
  light += ceil(link.used_odus/5)
total_light.append(light)



# Create deep copies of nodes, links, and edges to avoid modifying the original lists
nodes1 = nodes.copy()
links1 = links.copy()
added_edges1 = added_edges.copy()

# Remove the failed node from the node list
nodes1.remove(fail)

# Remove links that include the failed node
links1 = [link for link in links if fail not in link]

# Remove added edges that include the failed node
added_edges1 = [edge for edge in added_edges if fail not in edge]



while len(nodes1) > 1:

  # Create graph
  national_graph1 = nx.Graph()


  # Add nodes to the graph
  national_graph1.add_nodes_from(nodes1)

  # Add weighted edges to the graph
  national_graph1.add_weighted_edges_from(links1)

  # Convert nodes to their `_node_id` for labeling
  node_labels = {node: node._node_id for node in nodes1}

  # Use Kamada-Kawai layout for better spacing
  pos = nx.kamada_kawai_layout(national_graph)

  shortest_path = []
  shortest_edge = []


  for node1 in nodes1:
    for node2 in nodes1:
      # Select two random nodes for shortest path calculation
      source_node = None
      target_node = None

      if node1 != node2:
        source_node = node1
        target_node = node2

      if source_node and target_node:
        # Compute shortest path using Dijkstra's algorithm (weighted by distance)
        try:
          shortest_path1 = nx.shortest_path(national_graph, source=source_node, target=target_node, weight='weight')
        except nx.NetworkXNoPath:
          continue

        # Convert path edges to Link objects
        shortest_path_edges = []
        for u, v in zip(shortest_path1[:-1], shortest_path1[1:]):
            # Find the correct Link object
            for link in u.links:
                if (link.starting_node == u and link.ending_node == v) or (link.starting_node == v and link.ending_node == u):
                    shortest_path_edges.append(link)
                    break
        shortest_edge.append(shortest_path_edges)
        shortest_path.append(shortest_path1)


  for path in shortest_path:
    path.insert(0, nodes_1[path[0]._node_id - 1])

  flag = True

  i = 0
  j = 0

  while flag:
      service_map = {}  # Dictionary to store services by path index

      for idx, path in enumerate(shortest_path):
          a = random.randint(0, 1)
          rate = 10 if a == 0 else 100

          service = Service(
              rate=rate,
              sd_pair=(path[0]._node_id, path[-1]._node_id),
              path_nodes=path,
              path_edges=[link._link_id for link in shortest_edge[idx]]
          )


          service_map[idx] = service  # Store service for this path
          path[0].add_service(service)

          # Check for capacity issues
          for node in nodes1:
              if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                  flag = False
                  fail = node
                  break

          if not flag:
              break

      if not flag:
          break



      # Assign services to links
      for idx, (path, edge_path) in enumerate(zip(shortest_path, shortest_edge)):
          for link in edge_path:
            if link.used_odus < link.max_odu:
              link.add_service(service_map[idx])
              #j += 1

              # Check for capacity issues
            for node in nodes1:
                if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                    flag = False
                    fail = node
                    break

            if not flag:
                break


          #j -= len(edge_path) - 1
          j += 1

          if not flag:
              break


      j -= len(path) - 1

      if j >= i*50:
        i += 1

        tran = 0
        for node in nodes:
          tran += node.num_transponders
        num_tran.append(tran)

        node_cap = 0
        for node in nodes:
          if node.used_capacity >= node.max_capacity:
            node_cap += node.max_capacity
          else:
            node_cap += node.used_capacity
        capacity.append(node_cap)


        light = 0
        for link in links_full:
          light += ceil(link.used_odus/5)
        lightpath.append(light)


      if not flag:
          break



      # Assign services to intermediate nodes
      for idx, path in enumerate(shortest_path):
          for node in path[1:]:  # Skip first node since it's already assigned
            if node.used_capacity < node.max_capacity and node.used_odus < node.max_odus:
              node.add_service(service_map[idx])


              # Check for capacity issues
            for node in nodes1:
                if node.used_capacity >= node.max_capacity or node.used_odus >= node.max_odus:
                    flag = False
                    fail = node
                    break

            if not flag:
                break

          if not flag:
              break

      if not flag:
          break



  serv += j
  total_serv.append(serv)

  # Remove the failed node from the node list
  nodes1.remove(fail)

  # Remove links that include the failed node
  links1 = [link for link in links1 if fail not in link]

  # Remove added edges that include the failed node
  added_edges1 = [edge for edge in added_edges1 if fail not in edge]


  tran = 0
  for node in nodes:
    tran += node.num_transponders

  transponders.append(tran)

  node_cap = 0

  for node in nodes:
    if node.used_capacity >= node.max_capacity:
      node_cap += node.max_capacity
    else:
      node_cap += node.used_capacity

  total_cap.append(node_cap)


  light = 0
  for link in links_full:
    light += ceil(link.used_odus/5)
  total_light.append(light)


x_labels = [50 + i * 50 for i in range(len(capacity))]

# Create bar charts for each dataset with updated x-axis labels and thicker bars
fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(18, 6))

bar_width = 30  # Adjust bar width for thickness

fig.suptitle("Grooming Granularity 100G", fontsize=16, fontweight='bold') #change the name based on grooming granularity

# Plot each dataset separately with thicker bars
axs[0].bar(x_labels, capacity, color='red', width=bar_width, label="Total Capacity")
axs[0].set_title("Total Capacity")
axs[0].set_xlabel("Number of Services")
axs[0].set_ylabel("Capacity")
axs[0].set_xticks(x_labels)

axs[1].bar(x_labels, lightpath, color='blue', width=bar_width, label="Number of Occupied Channels")
axs[1].set_title("Number of Occupied Channels")
axs[1].set_xlabel("Number of Services")
axs[1].set_ylabel("Occupied Channels")
axs[1].set_xticks(x_labels)

axs[2].bar(x_labels, num_tran, color='green', width=bar_width, label="Number of Transponders")
axs[2].set_title("Number of Transponders")
axs[2].set_xlabel("Number of Services")
axs[2].set_ylabel("Number of Transponders")
axs[2].set_xticks(x_labels)

# Adjust layout for better visibility
plt.tight_layout()
plt.show()


