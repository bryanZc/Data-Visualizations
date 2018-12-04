#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 23:44:11 2018

@author: chengzhong
"""
# Load all packages
#from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from collections import Counter
import re
from os import path
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np

linecount=0
hashcount=0
wordcount=0
BagOfWords=[]
BagOfHashes=[]
BagOfLinks=[]

### SET THE FILE NAME ###

tweetsfile="file_Trump.txt"

###################################

with open(tweetsfile, 'r') as file:
    for line in file:
        # Remove the emojis in text
        emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U0001F1F2-\U0001F1F4"  # Macau flag
        u"\U0001F1E6-\U0001F1FF"  # flags
        u"\U0001F600-\U0001F64F"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U0001F1F2"
        u"\U0001F1F4"
        u"\U0001F620"
        u"\u200d"
        u"\u2640-\u2642"
        "]+", flags=re.UNICODE)
        
        line = emoji_pattern.sub(r'', line)
        
        #tokenize the text
        WordList=TweetTokenizer(strip_handles=True, reduce_len=True).tokenize(line)
        #WordList2=word_tokenize(line)
        linecount=linecount+1
        
        #match the regular expression
        regex1=re.compile('^#.+')
        regex2=re.compile('[^\W\d]') #no numbers
        regex3=re.compile('^http*')
        regex4=re.compile('.+\..+')

        for item in WordList:
            if(len(item)>2):
                if((re.match(regex1,item))):
                    newitem=item[1:] #remove the hash
                    BagOfHashes.append(newitem)
                    hashcount=hashcount+1
                elif(re.match(regex2,item)):
                    if(re.match(regex3,item) or re.match(regex4,item)):
                        BagOfLinks.append(item)
                    else:
                        BagOfWords.append(item)
                        wordcount=wordcount+1
                else:
                    pass
            else:
                pass

BigBag=BagOfWords+BagOfHashes
#make all to lowercase
BigBag = [x.lower() for x in BigBag]
#remove all stopwords in ENglish and Spanish
stop_words = set(stopwords.words('english'))
stop_words_spanish = set(stopwords.words('spanish'))
BigBag = [w for w in BigBag if w not in stop_words]
BigBag = [w for w in BigBag if w not in stop_words_spanish]

Raw_Tweet_File=open("TwitterResultsRaw.txt","w")
Freq_Tweet_File=open("TwitterWordFrq.txt", "w")

for word in BigBag:
    w = word+" "
    Raw_Tweet_File.write(w)

c = Counter(BigBag)
for word,count in c.most_common():
    value = word + "," + str(count)+"\n"
    Freq_Tweet_File.write(value)
    print(word,count)
Raw_Tweet_File.close()
Freq_Tweet_File.close()
#generate the wordcloud
d = path.dirname(__file__)
Rawfilename="TwitterResultsRaw.txt"
twitter_mask = np.array(Image.open(path.join(d, "twitter.jpg")))
# Read the whole text.
text = open(path.join(d, Rawfilename)).read()
wordcloud = WordCloud(width=1600, height=800,background_color='white',mask = twitter_mask).generate(text)
# Open a plot of the generated image.
plt.figure( figsize=(10,6), facecolor='k')
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.savefig("Twitter_Python_Wordcloud.jpg")
plt.show()
plt.close()
