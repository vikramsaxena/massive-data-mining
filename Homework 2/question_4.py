pip install pyspark

# Importing required libraries
from pyspark import SparkConf, SparkContext
from functools import reduce
import re
import sys
import matplotlib.pyplot as plt

#read centroid file data
def read_centroid_files(file_name):
    centroid_set = []
    with open(file_name) as f:
        for line in f:
            if not line:
                continue
            centroid_set.append(list(map(float, line.split())))
    return centroid_set

#calculate eucledian distance
def euclidean_distance(x, y):
    difference = [(x[i] - y[i])**2 for i in range(len(x))]
    return reduce(lambda x, y: x + abs(y), difference, 0)

#find nearest centroid to the given point and calculate the cost
def findCentroid(p, centroids, euc_dist, cost):
    min_dist_i = None
    min_dist = float('inf')
    for i, c in enumerate(centroids.value):
        euc_distance = euc_dist(p, c)
        if  min_dist > euc_distance:
            min_dist = euc_distance
            min_dist_i = i
    cost += min_dist
    return min_dist_i, p

#helper method for iterative k means function
def a_xy(cumulative, p):
    cumulative_p, cumulative_centroid = cumulative
    for i in range(len(p)):
        cumulative_p[i] += p[i]
    return cumulative_p, cumulative_centroid + 1

#helper method for iterative k means function
def a_xx(x, y):
    p_x, centroid_x = x
    p_y, centroid_y = y
    for i in range(len(p_x)):
        p_x[i] += p_y[i]
    return p_x, centroid_x + centroid_y

#iterative k means algorithm
def iterative_k_means(centroids, c):
  for i in range(MAX_ITER):
    #assign centroid
    ip = rdd_data.map(lambda point: findCentroid(point, centroids, euclidean_distance, c))

    #new centroid
    ic = ip.aggregateByKey((COLS * [0], 0), a_xy, a_xx)
    ic = ic.collect()
    new_centroids = k * [None]
    for i, sumcentroid in ic:
        sum, centroid = sumcentroid
        new_centroids[i] = [sum[j] / centroid for j in range(len(sum))]
    assert not any([centroid is None for centroid in new_centroids])

    #cost
    if c == c1:
      all_c1.append(c.value)
    else:
      all_c2.append(c.value)
    c.value = 0
    centroids.unpersist()
    centroids = sc.broadcast(new_centroids)

  if c == c1:
    return all_c1
  else:
    return all_c2

#determine change in cost
def change(cost):
    return ((cost[0] - cost[9]) / cost[0])*100

#plot graph
def plot_cost_vs_iteration(all_c1, all_c2):
  X = range(1, MAX_ITER + 1)
  Y1 = all_c1
  Y2 = all_c2
  legend1 = 'c1.txt'
  legend2 = 'c2.txt'

  plt.figure(figsize=(12,6))
  plt.xlabel('iteration')
  plt.ylabel('cost')
  plt.title('cost vs. iteration')
  plt.xticks(X)
  plt.plot(X, Y1, label = legend1)
  plt.plot(X, Y2, label = legend2)
  plt.legend(loc = 'upper right')
  plt.show()

sc = SparkContext.getOrCreate();
# load data
data = sc.textFile('data.txt')
rdd_data = data.map(lambda l: list(map(float, l.split())))
# costs
c1 = sc.accumulator(0)
c2 = sc.accumulator(0)
all_c1 = []
all_c2 = []

#parameters
MAX_ITER = 20
k = 10
COLS = 58

centroids_1 = read_centroid_files('c1.txt')
centroids_1 = sc.broadcast(centroids_1)

centroids_2 = read_centroid_files('c2.txt')
centroids_2 = sc.broadcast(centroids_2)

#perform iterative k-means
all_c1 = iterative_k_means(centroids_1, c1)
all_c2 = iterative_k_means(centroids_2, c2)

print('The change in cost after 10 iterations for c1.txt', change(all_c1))
print('The change in cost after 10 iterations for c2.txt', change(all_c2))

plot_cost_vs_iteration(all_c1, all_c2)

