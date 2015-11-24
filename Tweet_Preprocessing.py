import re
import sqlite3
from collections import defaultdict

# conn = sqlite3.connect('FinalTweet.db')
# c = conn.cursor()
# c.execute("CREATE TABLE FinalTweet(key INT, candidates TEXT, tweets TEXT, TweetLocation TEXT, PersonLocation TEXT, Label TEXT)")

## Load the data from text file. ##
def load_data(tweet_dict):
  filename = open("BernieSanders")
  pattern = re.compile('\*\* \w+ \*\* \w+')
  s=""
  for line in filename.readlines():
    s= "".join((s,line))
    n = pattern.findall(s)
    if not n:
      continue
    tweet_dict[len(tweet_dict)+1] = s
    s=""
  filename.close()
  print len(tweet_dict)

## Clean the tweets ##
def clean_dict(tweet_dict):
  for key in tweet_dict.keys():
    data = tweet_dict[key].lower()
    data = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',data)
    twee = data.split("**")
    if len(twee[0]) > 5:
      data_lst = twee[0].split()
      if data_lst:
        if data_lst[0] == "rt":
            data_lst.remove(data_lst[0])
        new_data = ' '.join(data_lst)
        new_data = " **".join((new_data, twee[1], twee[2]))
        tweet_dict[key] = new_data
      else:
        del tweet_dict[key]
        continue
    else:
        del tweet_dict[key]
  print len(tweet_dict)


tweet_map=defaultdict(dict)

def calculate(text):
  mytext = text
  count = 0
  count_sum = 0
  for i in mytext:
    if i >= 'a' and i <= 'z':
      count_sum += ((2**count)*ord(i))%(7**7)
      count += 1
  return count_sum%(7**7)

def assign(text,tweet_map,hashval):
  text_dict = tweet_map[hashval]
  if len(tweet_map[hashval])== 0:
    tweet_map[hashval][0]= 1
  elif tweet_map[hashval][0] > 0:
    for key in text_dict.keys():
        if key > 0:
            matchtext = tweet_map[hashval][key]
            #print matchtext
            if text in matchtext :
                return True
    tweet_map[hashval][0] += 1
  tweet_map[hashval][tweet_map[hashval][0]]= text
  return False

def process_dict(tweet_dict):
  global tweet_map
  length = len(tweet_dict)
  for i in range(length):
    if i in tweet_dict.keys():
      data = tweet_dict[i]
      text_two = data.split('**')
      text = text_two[0]
      words = text.split()
      if len(words) < 3:
        del tweet_dict[i]
        continue

      hashval = calculate(text)
      if True == assign(text,tweet_map,hashval):
        del tweet_dict[i]


def preprocessing():
  tweet_dict = {}
  load_data(tweet_dict)
  clean_dict(tweet_dict)
  process_dict(tweet_dict)
  print len(tweet_dict)
  # for key in tweet_dict:
  #   split_data = tweet_dict[key].split("**")
  #   c.execute("INSERT INTO FinalTweet values (?, 'BernieSanders', ?, ?, ?, NULL);", (key, split_data[0], split_data[1], split_data[2]))
  #   conn.commit()
    #print (tweet_dict[key])



if __name__ == "__main__":
  preprocessing()
