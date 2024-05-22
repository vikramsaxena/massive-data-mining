# In[1]:


import numpy as np


# In[2]:


#number of nodes
n = 100
#Matrix M
M = np.zeros((n, n))
#one vector
one = np.ones((n, 1))
#rank vector
r = np.zeros((n, 1))
#number of iterations
iterations = 40
#beta
beta = 0.8


# In[3]:


#reading the dataset and creating the matrix M
def create_matrix_M():
    with open('graph.txt') as f:
        line = f.readline()
        while line:
            nodes = line.strip().split()
            tgt_node = int(nodes[1])
            src_node = int(nodes[0])
            M[tgt_node - 1][src_node - 1] += 1
            line = f.readline()
    
    deg = np.sum(M, axis = 0)

    for i in range(n):
        M[:, i] = np.true_divide(M[:, i], deg[i])
    return M


# In[4]:


#compute PageRank and determine r vector
def compute_page_rank(M):
    r = one / n
    product_one = np.multiply(one, 1 - beta) / n
    # calculating the rank
    for i in range(iterations):
        product_two = np.matmul(beta * M, r)
        r = product_one + product_two

    r_vector = np.transpose(r)
    page_rank = r_vector.argsort()
    return page_rank, r_vector


# In[5]:


#determine the top 5 node IDs with the highest PageRank scores
def top_5_node(page_rank, r_vector):
    top_5_node_IDs = np.flip(page_rank[0][-5:]) + 1
    print("Top 5 node IDs with the highest PageRank scores:")
    print("------------------------------------------------")
    print("\nNode ID:\t Page rank")
    for i in top_5_node_IDs:
        print(i, ":\t", r_vector[0][i - 1])


# In[6]:


#determine the bottom 5 node IDs with the lowest PageRank scores
def bottom_5_node(page_rank, r_vector):
    bottom_5_node_IDs = page_rank[0][:5] + 1
    print("Bottom 5 node IDs with the lowest PageRank scores: ")
    print("--------------------------------------------------")
    print("\nNode ID:\t Page rank")
    for i in bottom_5_node_IDs:
        print(i, ":\t", r_vector[0][i - 1])


# In[7]:


M = create_matrix_M()
page_rank, r_vector = compute_page_rank(M)


# In[8]:


#List the top 5 node IDs with the highest PageRank scores
top_5_node(page_rank, r_vector)


# In[9]:


#List the bottom 5 node IDs with the lowest PageRank scores
bottom_5_node(page_rank, r_vector)


# In[ ]:




