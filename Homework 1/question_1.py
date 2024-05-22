# -*- coding: utf-8 -*-

pip install pyspark

from pyspark import SparkConf
from pyspark import SparkContext

#Setting Spark config and loading the text file data
conf = SparkConf()
sc = SparkContext(conf=conf)
data = sc.textFile('soc-LiveJournal1Adj.txt')

#function to generate tuples containing the user and their list of friends
def generate_user_friend_tuples(line):
    user, friends = line.split('\t')
    if '' == friends:
        friend_list = []
    else:
        friend_list = friends.split(',')
    return (user, friend_list)

#function to generate all the pairs of friends for a user
def generate_user_friend_pairs(line):
    user_id = line[0]
    friend_list = line[1]
    friend_pairs = []
    for friend_id in friend_list:
        pair = (user_id, friend_id)
        if friend_id < user_id:
            pair = (friend_id, user_id)
        friend_pairs.append((pair, 0))
    for i in range(len(friend_list) - 1):
        for j in range(i + 1, len(friend_list)):
            pair = (friend_list[i], friend_list[j])
            if friend_list[j] < friend_list[i] :
                pair = (friend_list[j], friend_list[i])
            friend_pairs.append((pair, 1))
    return friend_pairs

#generating tuples and filtering the data 
tuples = data.map(lambda line : generate_user_friend_tuples(line))
pairs = tuples.flatMap(lambda line : generate_user_friend_pairs(line))
mutual_filter = pairs.groupByKey().filter(lambda pair : 0 not in pair[1]).flatMapValues(lambda x : x)

#generating recommended user data
reduce_mutual_filter = mutual_filter.reduceByKey(lambda x, y : x + y)
recommended_users = reduce_mutual_filter.flatMap(lambda pair: [(pair[0][0], (pair[0][1], pair[1])), (pair[0][1], (pair[0][0], pair[1]))]).groupByKey().mapValues(list) 
sorted_recommendation = recommended_users.map(lambda user: (user[0], sorted(user[1], key = lambda x : (-x[1], int(x[0])))))
recommended_user_data = sorted_recommendation.collect()

#printing the result
user_ids = ['924', '8941', '8942', '9019', '9020', '9021', '9022', '9990', '9992', '9993']
for user_id in user_ids:
    for line in recommended_user_data:
        id, result = line
        if user_id == id:
            recommended_user_id = []
            for i in result:
                recommended_user_id.append(i[0])
            print(user_id, recommended_user_id)
