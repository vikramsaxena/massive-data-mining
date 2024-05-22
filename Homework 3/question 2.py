import numpy as np
import networkx as nx

G = nx.Graph()
G.add_nodes_from(["A", "B", "C", "D", "E", "F", "G", "H"])
G.add_edges_from([("A", "B"), ("A", "C"), ("A", "D"), ("A", "G"), ("B", "C"), ("B", "D"), ("C", "D"), ("E", "F"), ("E", "G"), ("F", "G"), ("G", "H")])
nx.draw(G, with_labels = True)

#2(a)
A = nx.adjacency_matrix(G)
A = A.toarray()
print("Adjacency matrix A:\n", A)

D = G.degree()
print("\nDegree matrix D:\n", D)

L = nx.laplacian_matrix(G)
L = L.toarray()
print("\nLaplacian matrix L:\n",L)

#2(b)
eigen_values, eigen_vectors = np.linalg.eig(L)
print("Eigen values of the Laplacian matrix:\n", eigen_values)
print("\nEigen vectors of the Laplacian matrix:\n", eigen_vectors)

#2(c)
sort_eigen_values = np.argsort(eigen_values)
second_smallest_eigen_vector = eigen_vectors[ : , sort_eigen_values[1]]
print("Eigen vector corresponding to the second smallest eigen values:\n", second_smallest_eigen_vector)
