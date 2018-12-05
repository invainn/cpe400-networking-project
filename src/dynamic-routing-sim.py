# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
# AUTHORS:
# Aaron Mcanerney
# Nikkolas Irwin
# Anthony Bennett
#
# DESCRIPTION: Simulates a mesh network where nodes and links may fail. Nodes and links may fail intermittently.
# As an input to the simulation, each node and link will have a certain probability to fail. When such failure occurs,
# the network adapts and re-routes to avoid the faulty link/node(s). This program accomplishes the simulation by using
# Dijkstra's algorithm to solve the All Pairs Shortest Path problem by varying the source node among all nodes in the
# graph (except node 1, the source node) and recovering the path itself, not just the cost of the path.
#
# GETTING STARTED:
# 1. Download and install Python 3.7.1 or greater Link: https://www.python.org/
# 2. Download and install Pip 18.1 Link: https://pypi.org/project/pip/
# 3. Download and install NetworkX 2.2 Link: https://networkx.github.io/
# 4. Download and install matplotlib 3.0.2 Link: https://matplotlib.org/users/installing.html
#
# TO RUN THE PROGRAM: Type 'python dynamic-routing-sim.py' without the single quotes.
#
# OUTPUT:
# -Displays the nodes that fail at every interval
# -Displays Dijkstra's Shortest Path (if a path exists) from  the source node (node 1) to the
# destination node (node 25).
# -Displays the number of hops (if a path exists) or 'Destination unreachable' (if a path does not exist).
#
# ABOUT THE GUI SIMULATION:
# -Green nodes display Dijkstra's Shortest Path from the source node (node 1) to the destination node (node 25) if
# a path exists.
# -Blue nodes indicate nodes that are online but are not included in the shortest path from the source node (node 1) to
# the destination node (node 25).
# -Red nodes indicate nodes that have failed, become faulty, and are currently offline. The faulty nodes recover on
# the next interval and are avoided for the current interval if a path from the source node (node 1) to the destination
# node (node 25) exists.
# -Each interval is 9000 milliseconds (9 seconds) long.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

# Import Statements.
import networkx as nx
import matplotlib.pyplot as plt
import random
import matplotlib.animation
import copy
import itertools

# NetworkX graph object to be used by the whole file.
G = nx.Graph()
nodes = [x for x in range(1, 26)]
G.add_nodes_from(nodes)
pos = nx.spring_layout(G)

# Set initial node color.
node_colors = ['blue' for x in range(1, 26)]

# Build the plot.
fig, ax = plt.subplots(figsize=(8, 6))

# Holds the node activity for the log-file.
outputFile = open('../log/activity-log.txt', 'w')


# Graph edge init function.
def edgeInit(edges):
    G.add_edges_from(edges) 


# Create color list for all nodes in graph.
def initNodeColor():
    return 


# Initialize the NetworkX graph.
def initGraph():
    outputFile.write('dynamic-routing-sim' + '\n')
    outputFile.write('-------------------' + '\n')
    edges = readEdgesFromFile()
    edgeInit(edges)


# Read edges from a file.
def readEdgesFromFile():
    edges = [tuple(map(int, line.rstrip('\n').split(' '))) for line in open('../app-data/edges.txt')]
    return edges


# Calculate how many nodes will fail for a given interval.
def calculateFailurePercentage():
    return random.randint(1, 5)


# Updates the function for graph animations.
# Runs Dijkstra's Shortest Path on the graph after failure and updates the animation accordingly.
def updateGraph(num):
    # Clear the figure.
    ax.clear()

    # Calculate how many nodes will fail on a given iteration.
    number_of_failures = calculateFailurePercentage()
    failures = {random.randint(2, 25) for x in range(0, number_of_failures)}

    # Store the edges in a list.
    edges = []
    # Make a copy of the edges to be reinserted.
    for failure in failures:
        edges.append(copy.deepcopy(list(G.edges(failure))))

    # Flatten the list.
    all_edges = list(itertools.chain(*edges))

    # Remove the node(s) from the graph.
    G.remove_nodes_from(failures)

    # Generate a shortest path from node 1 to all others.
    path = dict(nx.all_pairs_shortest_path(G))

    # Create edges of path for coloring.
    path_edges = createEdgesFromPath(path)

    # Add node(s) into graph.
    G.add_nodes_from(failures)

    # Show node failure(s).
    for x in range(len(node_colors) - number_of_failures, len(node_colors)):
        node_colors[x] = 'red'

    # Add a title to the top of the figure that displays the node failure(s) for a given interval.
    title = "Node Failure(s): " + ''.join(str(node) + ' ' for node in sorted(failures))

    # Keep a running list of node failures in the console.
    print(title)

    # Write the node activity to an output file.
    outputFile.write('\n' + title + '\n')

    # Use a try-except block to calculates the shortest path and number of hops based on the available nodes.
    # Starting at from the source node (node 1) to the destination node (node 25).
    try:
        # Store Dijkstra's Shortest Path
        d_path = nx.dijkstra_path(G, 1, 25)

        # Display Dijkstra's Shortest Path and write the results to the output file.
        print("Dijkstra Shortest Path:" + str(d_path))
        outputFile.write("Dijkstra Shortest Path:" + str(d_path) + "\n")

        # Display the number of hops and write the results to the output file.
        print("Number of Hops: " + str(len(d_path) - 1))
        outputFile.write("Number of Hops: " + str(len(d_path) - 1) + "\n")

        # Calculate the edges used for Dijkstra's Shortest Path for a given interval.
        djisktra_edges = createEdgesDijsktras(d_path)

        # Update the graph.
        nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, width=4, alpha=0.2, edge_color='b')
        nx.draw_networkx_edges(G, pos=pos, edgelist=all_edges, width=2, alpha=0.3, edge_color='r')
        nx.draw_networkx_edges(G, pos=pos, edgelist=djisktra_edges, width=4, alpha=0.8, edge_color='g')

    # If no path exists from the source node (node 1) to the destination node (node 25) then handle the
    # error gracefully by updating the GUI to show no path and print a message to the console and output file.
    except nx.exception.NetworkXNoPath:
        # Print to the console if no path exists.
        print("No available path from [source]: node (1) to [destination]: node (25)")
        outputFile.write("No available path from [source]: node (1) to [destination]: node (25)\n")

        # Prompt the user that the destination could not be reached and write the result to the output file.
        print("Destination unreachable.")
        outputFile.write("Destination unreachable.\n")

        # Update the graph.
        nx.draw_networkx_edges(G, pos=pos, edgelist=path_edges, width=4, alpha=0.2, edge_color='b')
        nx.draw_networkx_edges(G, pos=pos, edgelist=all_edges, width=2, alpha=0.3, edge_color='r')

    # Draw the updated graph.
    nx.draw(G, pos=pos, node_color=node_colors, with_labels=True, alpha=.8, font_weight='bold', ax=ax)

    # Set the figure title.
    ax.set_title(title, fontsize="8", fontweight="bold")

    # Reset the node(s) for next iteration
    for x in range(len(node_colors) - number_of_failures, len(node_colors)):
        node_colors[x] = 'blue'
        
    # Put the edges back into graph for next iteration.
    G.add_edges_from(all_edges)
    # Add a line of space between intervals.
    print()


# Create edges from the single source Dijkstra's Shortest Path.
def createEdgesFromPath(path):
    all_edges = set()

    for key in path.keys():
        shortest = path[key]
        paths = shortest.values()

        for l in paths:
            if len(l) > 1:
                edges = [(x, y) for x, y in zip(l, l[1:])]

                for edge in edges:
                    all_edges.add(edge)

    return all_edges


def createEdgesDijsktras(path):
    edges = [(x, y) for x, y in zip(path, path[1:])]
    return edges


# Create the initial network graph.
initGraph()

# Produce the animation.
ani = matplotlib.animation.FuncAnimation(fig, updateGraph, frames=30, interval=9000, repeat=True)
plt.show()

# Close the output file when the program ends to save the logged data from the simulation.
print('Data written to log/activity-log.txt')
