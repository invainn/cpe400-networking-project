# cpe400-networking-project

* AUTHORS: Aaron Mcanerney, Nikkolas Irwin, and Anthony Bennett

* DESCRIPTION: Simulates a mesh network where nodes and links may fail. Nodes and links may fail intermittently. As an input to the simulation, each node and link will have a certain probability to fail. When such failure occurs, the network adapts and re-routes to avoid the faulty link/node(s). This program accomplishes the simulation by using Dijkstra's algorithm to solve the All Pairs Shortest Path problem by varying the source node among all nodes in the graph (except node 1, the source node) and recovering the path itself, not just the cost of the path.

* GETTING STARTED:
1. Download and install Python 3.7.1 or greater
	Link: https://www.python.org/
2. Download and install Pip 18.1
	Link: https://pypi.org/project/pip/
3. Download and install NetworkX 2.2
	Link: https://networkx.github.io/
3. Download and install matplotlib 3.0.2
	Link: https://matplotlib.org/users/installing.html

* TO RUN THE PROGRAM: Type 'python dynamic-routing-sim.py' without the single quotes.