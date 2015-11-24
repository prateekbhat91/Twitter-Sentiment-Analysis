import tweepy
import time
import sys
from tweepy import models as m
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import csv
import pandas
import codecs

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Creation of the actual interface, using authenticationt
try:
    api = tweepy.API(auth)
except ValueError:
    print "Error in authentication"


class listener(StreamListener):

    def on_data(self, data):
        try:
            decoded = json.loads(data)

            if decoded['place']and decoded['user']['location'] != None:
                saveTup = (decoded['text'].encode('ascii', 'ignore')+" ** " + decoded['place']['full_name'].encode('ascii', 'ignore') + " ** " + decoded['user']['location'].encode('ascii', 'ignore'))
                #print saveTup
            elif decoded['place'] == None and decoded['user']['location']!=None:
                saveTup = decoded['text'].encode('ascii', 'ignore')+" ** " + str(decoded['place']) + " ** " + decoded['user']['location'].encode('ascii', 'ignore')
                #print saveTup
            elif decoded['place'] != None and decoded['user']['location']==None:
                saveTup = (decoded['text'].encode('ascii', 'ignore')+" ** " + decoded['place']['full_name'].encode('ascii', 'ignore') + " ** " + str(decoded['user']['location']))
                #print saveTup

            else:
                saveTup=(decoded['text'].encode('ascii', 'ignore')+" ** " + str(decoded['place']) + " ** " + str(decoded['user']['location']))

            file = open("BernieSanders", "a+")
            file.write(saveTup)
            file.write("\n")
            file.close()


        except BaseException,e:
            print 'Failed',str(e)
            time.sleep(5)
            return True

    def on_error(self, status):
        print status

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["#FeelTheBern", "BernieSanders", "Bernie2016", "@BernieSanders"])


