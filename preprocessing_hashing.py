import re
import sqlite3
#import sklearn
from collections import defaultdict


conn = sqlite3.connect('example.db')
c = conn.cursor()
#clf = sklearn.svm.SVC()

def load_data(tweet_dict):
  filename = open('BernieSanders')
  pattern = re.compile('\*\* \w+ \*\* \w+')
  s=""
  for line in filename.readlines():
    s= "".join((s,line))
    n = pattern.findall(s)
    if not n:
      continue
##    print ("Value of s", s, "test", s.split()[21])
    tweet_dict[len(tweet_dict)+1] = s
    s=""
  filename.close()

def clean_dict(tweet_dict):
  for key in tweet_dict:
    data = tweet_dict[key]
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data)
    data_lst = data.split()
    if len(urls) > 0:
      for item in urls:
        try: 
          data_lst.remove(item)
        except ValueError:
          continue
    elif data_lst[0].lower() == "rt":
      data_lst.remove(data_lst[0])
    new_data = ' '.join(data_lst)
    tweet_dict[key] = new_data
  print len(tweet_dict)


tweet_map=defaultdict(dict)

def calculate(text):
  mytext = text.lower()
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
            print matchtext
            if text in matchtext :
                return True
    tweet_map[hashval][0] += 1
  tweet_map[hashval][tweet_map[hashval][0]]= text.lower()
  return False

def process_dict(tweet_dict):
  global tweet_map
  length = len(tweet_dict)
  for i in range(length):
    if i in tweet_dict.keys():
      data = tweet_dict[i]
      text_two = data.split('**')
      text = text_two[0]
      text = text.lower()
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
  print (len(tweet_dict))


if __name__ == "__main__":
  preprocessing()
