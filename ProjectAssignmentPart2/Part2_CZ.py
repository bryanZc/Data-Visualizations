#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  5 18:13:23 2018

@author: chengzhong
"""

from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt
from sklearn.manifold import MDS
from mpl_toolkits.mplot3d import Axes3D
from scipy.cluster.hierarchy import ward, dendrogram
import random

'''
###Ways to count the word "house" in Emma (file 0 in the list of files)
house_idx = list(vocab).index('house') #index of "house" 
print(dtm[0, house_idx])
##There are 95 occurrences of “house” in Emma
##Counting "house" in Pride and Prejudice (107 in Pride) 
print(dtm[1,house_idx])
print(list(vocab)[house_idx]) #this will print “house” 
print(dtm) #prints the doc term matrix

##Create a table of word counts to compare Emma and Pride and Prejudice
columns=["BookName", "house","and","almost"] 
MyList=["Emma"]
MyList2=["Pride"]
MyList3=["Sense"]
for someword in ["house","and", "almost"]:
	EmmaWord = (dtm[0, list(vocab).index(someword)]) 
	MyList.append(EmmaWord)
	PrideWord = (dtm[1, list(vocab).index(someword)]) 
	MyList2.append(PrideWord)
	SenseWord = (dtm[2, list(vocab).index(someword)]) 
	MyList3.append(SenseWord)
##print(MyList)
##print(MyList2)
df2=pd.DataFrame([columns, MyList,MyList2, MyList3]) 
print(df2)


#Euclidean Distance
dist = euclidean_distances(dtm)

#print(np.round(dist,0))
#The dist between Emma and Pride is 3856
##Cosine Similarity
cosdist = 1 - cosine_similarity(dtm)
#print(np.round(cosdist,3)) #cos dist should be .02
'''
def plot_2D(cosdist,names):
    ## This type of visualization is called multidimensional scaling (MDS)
    mds = MDS(n_components=2, dissimilarity="precomputed", random_state=1) ## "precomputed" means we will give the dist (as cosine sim)
    pos = mds.fit_transform(cosdist) # shape (n_components, n_samples)
    xs, ys = pos[:, 0], pos[:, 1]
    
    plt.figure(figsize=(10,8))
    for x, y, name in zip(xs, ys, names):
        plt.scatter(x, y)
        plt.text(x+0.0009,y+0.001,name)
    plt.title('2D Distribution of books by distance',fontweight='bold',fontsize=14,verticalalignment='bottom')
    plt.savefig("2D_plot.jpg")
    plt.show()

def plot_3D(cosdist,names): 
    mds = MDS(n_components=3, dissimilarity="precomputed", random_state=1) 
    pos = mds.fit_transform(cosdist)
    fig = plt.figure(figsize=(12,10))
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(pos[:, 0], pos[:, 1], pos[:, 2],c=pos[:,2])
    for x, y, z, s in zip(pos[:, 0], pos[:, 1], pos[:, 2], names):
        ax.text(x+0.001, y, z+.001, s)
    lower_x = round(min(pos[:,0]),3)
    lower_y = round(min(pos[:,1]),3)
    lower_z = round(min(pos[:,2]),3)
    upper_x = round(max(pos[:,0]),3)
    upper_y = round(max(pos[:,1]),3)
    upper_z = round(max(pos[:,2]),3)
    ax.set_xlim3d(lower_x,upper_x) #stretch out the x axis 
    ax.set_ylim3d(lower_y,upper_y) #stretch out the x axis 
    ax.set_zlim3d(lower_z,upper_z) #stretch out the z axis 
    ax.set_title("3D Distribution of books by distance",fontsize=18,verticalalignment='bottom',fontweight='bold')
    plt.savefig("3D_plot.jpg")
    plt.show()

def cluster_plot(cosdist,names):
    linkage_matrix = ward(cosdist)
    plt.figure(figsize=(10,8))
    dendrogram(linkage_matrix, orientation="right", labels=names)#,leaf_font_size=6) 
    
    plt.title('Hierarchical Cluster of books',fontweight='bold',fontsize=20,verticalalignment='bottom')
    plt.tight_layout()
    plt.savefig("cluster_plot.jpg")
    plt.show()

def main(filenames,names):    
    vectorizer = CountVectorizer(input='filename')
    dtm = vectorizer.fit_transform(filenames) 
    print(type(dtm)) #vocab is a vocabulary list of each word that appears 
    #vocab = vectorizer.get_feature_names() # change to a list 
    #print(vocab)
    dtm = dtm.toarray() # convert to a regular array 
    #print(list(vocab)[500:550])
    cosdist = 1 - cosine_similarity(dtm)
    plot_2D(cosdist,names)
    plot_3D(cosdist,names)
    cluster_plot(cosdist,names)

if __name__ == "__main__":
    #input the name of books
    names=['Austen_Emma','Austen_Pride','Austen_Sense',
    'CBronte_Jane','CBronte_Professor','CBronte_Villette',
    'Dickens_Bleak','Dickens_David','Dickens_Hard',
    'EBronte_Wuthering',
    'Eliot_Adam','Eliot_Middlemarch','Eliot_Mill']
    path = 'Novels_Corpus/' 
    #choose how many books want to compare
    mynames = random.sample(names,13)
    filenames = []
    for filename in mynames:
        file = path+filename+'.txt'
        filenames.append(file)
    main(filenames,mynames) 
    
    









