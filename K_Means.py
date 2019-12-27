#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 15 15:03:48 2019

@author: Sandeep Reddy Gopu
"""

import sys
import json
import re
import copy
import math

regex_string = [
    r'<[^>]+>',
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',
    r'(?:(?:\d+,?)+(?:\.?\d+)?)',
    r"(?:[a-z][a-z'\-_]+[a-z])",
    r'(?:[\w_]+)',
]

text_re = re.compile(r'(' + '|'.join(regex_string) + ')', re.VERBOSE | re.IGNORECASE)

def text(s):
    return text_re.findall(s)


def preprocess(s, lowercase=True):
    data = text(s)
    if lowercase:
        data = [character.lower() for character in data]
    return data

def jaccard(a, b):
    intersection = list(set(a) & set(b))
    I = len(intersection)
    union = list(set(a) | set(b))
    U = len(union)
    return round(1 - (float(I) / U), 4)

def kmeans(centroid_index, tweet_data, l, k):
    #count = 0
    for h in range(k):
        #count = count + 1
        centroid_txt = [tweet_data[x] for x in centroid_index]
        cluster = []
        for i in range(l):
            d = [jaccard(tweet_data[i], centroid_txt[j]) for j in range(k)]
            ans = d.index(min(d))
            cluster.append(ans)
        centroid1 = up_date(cluster, tweet_data, l, k)
        sum = 0;
        for i in range(k):
            if(centroid1[i] == centroid_index[i]):
                sum = sum + 1
            if (sum == k):
                break
            centroid_index = copy.deepcopy(centroid1)
    #output(cluster, k, terms_all)
    print("For k  :  ", k)
    sse(cluster, centroid_index, tweet_data, k, l)
    output(cluster, k, tweet_data)

def output(cluster, k, tweet_data):
    final = []
    for i in range(k):
        final.append([j for j, u in enumerate(cluster) if u == i])
        t = [x for x in final[i]]
        print("Cluster [",i+1,"] : ", len([tweet_data[x] for x in t]), " tweets. ")

def up_date(cluster, tweet_data, l, k):
    indices = []
    new_centxt_index = []
    for i in range(k):
        indices.append([j for j, u in enumerate(cluster) if u == i])
        m = indices[i]
        if (len(m) != 0):
            txt = [tweet_data[p] for p in m]
            sim = [[jaccard(txt[i], txt[j]) for j in range(len(m))] for i in range(len(m))]
            f1 = [sum(i) for i in sim]
        new_centxt_index.append(
            m[(f1.index(min([sum(i) for i in sim])))])
    return new_centxt_index

def sse(cluster, centroid_index, tweet_data, k, l):
    indices1 = []
    centroid_txt = [tweet_data[x] for x in centroid_index]
    sum = 0
    for i in range(k):
        indices1.append([j for j, u in enumerate(cluster) if u == i])
        t = [tweet_data[x] for x in indices1[i]]
        for j in range(len(indices1[i])):
            sum = sum + math.pow(jaccard(t[j], centroid_txt[i]), 2)
    print('SSE', sum)

tweet_data = []
with open("usnewshealth.txt", "r") as f:
    for line in f:
        line1 = re.sub(r'http\S+', '', line)
        line2 = re.sub(r'(?:@[\w_]+)', '', line1)
        tweet = line2
        tokens = preprocess(tweet)
        tweet_data.append([text for text in tokens])

for i in range(len(tweet_data)):
    tweet_data[i] = tweet_data[i][9:]

centroid_index = []
for i in range(0, len(tweet_data), 280):
    centroid_index.append(i)


l = len(tweet_data)
k = 5
kmeans(centroid_index, tweet_data, l, k)
#print(len(centroid_index))
#55, 26
#70, 20
#95, 15
#150,10
#280, 5
