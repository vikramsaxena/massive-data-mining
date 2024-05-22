#!/usr/bin/env python
# coding: utf-8

# In[1]:


from collections import defaultdict
import itertools


# In[2]:


#support s
s = 100


# In[3]:


#function to split the file contents
def generate_itemset(file):
    f = open(file)
    i_set = []
    for line in f:
        item = set(line.split())
        i_set.append(item)
    return i_set


# In[4]:


#function to generate single item set
def generate_single_item_set(item_set):
    single_item_set = defaultdict(int)
    for item in item_set:
        for i in item:
            key = frozenset({i})
            if key not in single_item_set:
                single_item_set[key] = 1
            else:
                single_item_set[key] += 1
    return single_item_set


# In[5]:


#function to generate item set of size 2
def generate_size_two_item_set(item_set, single_item_set):
    size_two_item_set = defaultdict(int)
    for item in item_set:
        for i, j in itertools.combinations(item, 2):
            if s <= single_item_set[frozenset({i})] and s <= single_item_set[frozenset({j})]:
                key = frozenset({i, j})
                if key not in size_two_item_set:
                    size_two_item_set[key] = 1
                else:
                    size_two_item_set[key] += 1
    return size_two_item_set


# In[6]:


#function to generate item set of size 3
def generate_size_three_item_set(item_set, size_two_item_set):
    size_three_item_set = {}
    for item in item_set:
        for i, j, k in itertools.combinations(item, 3):
            if s <= size_two_item_set.get(frozenset({i, j}), 0) and s <= size_two_item_set.get(frozenset({j, k}), 0) and s <= size_two_item_set.get(frozenset({k, i}), 0):
                key = frozenset({i, j, k})
                if key not in size_three_item_set:
                    size_three_item_set[key] = 1
                else:
                    size_three_item_set[key] += 1
    return size_three_item_set


# In[7]:


#function to compute confidence scores
def compute_confidence_scores(item_set_one, item_set_two, size):
    confidence_scores = []
    for key,val in item_set_two.items():
        if s <= val:
            for item in itertools.combinations(key, size):
                conf = val / item_set_one[frozenset(item)]
                confidence_scores.append((set(item), (set(key) - set(item)).pop(), conf))
        else:
            continue
    return confidence_scores


# In[8]:


#generating different itemsets
item_set = generate_itemset('browsing.txt')
single_item_set = generate_single_item_set(item_set)
size_two_item_set = generate_size_two_item_set(item_set, single_item_set)
size_three_item_set = generate_size_three_item_set(item_set, size_two_item_set)


# In[9]:


#Top 5 rules for pairs of items (X, Y) having at least 100 support
confidence_scores = compute_confidence_scores(single_item_set, size_two_item_set, 1)
confidence_scores = [(tuple(c[0]), c[1], c[2]) for c in confidence_scores]
confidence_scores.sort(key = lambda c : c[0])
confidence_scores.reverse()
confidence_scores.sort(key = lambda c : c[2])
confidence_scores.reverse()
confidence_scores[:5]


# In[10]:


#Top 5 rules for item triples (X, Y, Z) having at least 100 support
confidence_scores = compute_confidence_scores(size_two_item_set, size_three_item_set, 2)
confidence_scores = [(tuple(sorted(c[0])), c[1], c[2]) for c in confidence_scores]
confidence_scores.sort(key = lambda c : c[0])
confidence_scores.reverse()
confidence_scores.sort(key = lambda c : c[2])
confidence_scores.reverse()
confidence_scores[:5]


# In[ ]:




