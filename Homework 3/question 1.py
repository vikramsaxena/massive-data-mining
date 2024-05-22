import numpy as np
import networkx as nx

G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
G.add_edges_from([("A","B"), ("A","C"), ("A","D"), ("A", "G"), ("B","C"), ("B","D"), ("C","D"), ("E","F"), ("E","G"), ("F","G"), ("G","H")])
nx.draw(G, with_labels = True)

#1(a)
partition = [{"A", "B", "C", "D"}, {"E", "F", "G", "H"}]
G_remove_AG = nx.Graph(G)
G_remove_AG.remove_edge("A", "G")
Q_remove_AG = nx.community.modularity(G_remove_AG, partition)
print("Modularity after removing link between nodes A and G: ", Q_remove_AG)
nx.draw(G_remove_AG, with_labels = True)

#1(b)
G_add_EH = nx.Graph(G)
G_add_EH.add_edge("E", "H")
Q_add_EH = nx.community.modularity(G_add_EH, partition)
Q = nx.community.modularity(G, partition)
print("Modularity of original graph: ", Q)
print("Modularity after adding link between nodes E and H: ", Q_add_EH)
nx.draw(G_add_EH, with_labels = True)

#1(c)
G_add_FA = nx.Graph(G)
G_add_FA.add_edge("F", "A")
Q_add_FA = nx.community.modularity(G_add_FA, partition)
print("Modularity of original graph: ", Q)
print("Modularity after adding link between nodes F and A: ", Q_add_FA)
nx.draw(G_add_FA, with_labels = True)
