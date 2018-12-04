#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 16:07:47 2018

@author: chengzhong
"""

###Packages-----------------------
import tweepy
from tweepy import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
###-----------------------------------------


## Create all the keys and secrets that you get
## from using the Twitter API-------------------------------------
consumer_key = '4MWgWR3lihW1dNkbBW86rKXbw'
consumer_secret = 'FcUlbKoLQdry2I1i4HFJd8frk2uXeALCgVDlwJq4ZlnPyHyA0o'
access_token = '1162187700-5XDSKprKzklAstPBASwfNun7PZjX2ag9vCH4RBW'
access_secret = 'PDq8yEFL2stZ0384ILXn7TpoRqyadc9xlXc4wVbkgrHPy'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

hashname = input("Please Enter the hashtag name start with hashtag (eg.#Stockmarket): ")
if hashname[0] == "#":
    keyword = hashname[1:]
else:
    hashname = "#"+hashname
    keyword = hashname[1:]
    
num_tweets = eval(input("Please enter the number of tweets you want (maximum 30): "))
if int(num_tweets) > 30:
    print("Will Collect Maximum 30 Tweets.")
    num_tweets = 30
else:
    num_tweets = int(num_tweets)

class Listener(StreamListener):
    print("In Listener...") 
    tweet_number=0
    #__init__ runs as soon as an instance of the class is created
    def __init__(self, max_tweets, hfilename, rawfile):
        self.max_tweets=max_tweets
        print(self.max_tweets)     
    #on_data() is a function of StreamListener as is on_error and on_status    
    def on_data(self, data):
        self.tweet_number+=1 
        print("In on_data", self.tweet_number)
        try:
            print("In on_data in try")
            with open(hfilename, 'a') as f:
                with open(rawfile, 'a') as g:
                    tweet=json.loads(data)
                    tweet_text=tweet["text"]
                    print(tweet_text,"\n")
                    f.write(tweet_text) # the text from the tweet
                    json.dump(tweet, g)  #write the raw tweet
        except BaseException:
            print("NOPE")
            pass
        if self.tweet_number>=self.max_tweets:
            sys.exit('Limit of '+str(self.max_tweets)+' tweets reached.')
    #method for on_error()
    def on_error(self, status):
        print("ERROR")
        if(status==420):
            print("Error ", status, "rate limited")
            return False

#Create a file for any hash mine    
hfilename="file_"+keyword+".txt"
rawfile="file_rawtweets_"+keyword+".txt"
twitter_stream = Stream(auth, Listener(num_tweets, hfilename, rawfile))
twitter_stream.filter(track=[hashname])                                                                  

 
