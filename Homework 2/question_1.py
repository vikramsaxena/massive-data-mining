
# In[1]:


import numpy as np
from scipy.linalg import svd
from numpy.linalg import eigh


# In[2]:


#SVD decomposition
M = np.array([[1, 2],[2, 1], [3, 4], [4, 3]])
U, S, V_T = svd(M, full_matrices = False)


# In[3]:


print("U:")
print(U)
print("")
print("S:")
print(S)
print("")
print("V^T:")
print(V_T)


# In[4]:


#Eigenvalue decomposition
M_TM = np.matmul(M.transpose(), M)
Evals, Evecs = eigh(M_TM)


# In[5]:


print("Evals:")
print(Evals)
print("")
print("Evecs:")
print(Evecs)
print("")

