from collections import defaultdict
import nltk
# nltk.download()
from nltk.tokenize import word_tokenize as wt
from nltk.probability import FreqDist as freq
import numpy as np
from numpy import array, arange, zeros, hstack, argsort
from itertools import  izip
import xlrd
import codecs
import sys
from sklearn.cross_validation import StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import  SVC
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score


n_jobs = 25

book = xlrd.open_workbook('Final_tweets.xlsx')

sheet = book.sheets()[0]



class Tweet(object):
    def __init__(self,tweet):
        self.id = tweet['id']
        self.tweet = tweet['tweet']
        self.tweetlocation = tweet['tweet_location']
        self.geolocation = tweet['geo_location']
        self.label =tweet['label']

class Candidate(object):
    def __init__(self,name):
        self.candidate = name
        self.positive = defaultdict()
        self.negative = defaultdict()
        self.neutral = defaultdict()

    def insertTweet(self,tweet):
        myobject = Tweet(tweet)
        if tweet['label'] == "positive":
            self.positive[len(self.positive)]= myobject
        elif tweet['label'] == "negative":
            self.negative[len(self.negative)]= myobject
        else:
            self.neutral[len(self.neutral)] = myobject

    def getTweets(self,label):
        if label == "positive":
            data = self.positive
        elif label == "negative":
            data = self.negative
        else:
            data = self.neutral
        tweetlist= []
        for key in data:
            text = data[key].tweet
            tweetlist.append(text)
        return tweetlist

CandidateList = []

Hillary = Candidate("Hillary")
CandidateList.append(Hillary)
Bernie = Candidate("Bernie")
CandidateList.append(Bernie)
Trump = Candidate("Trump")
CandidateList.append(Trump)
Martin= Candidate("Martin")
CandidateList.append(Martin)
Ben= Candidate("Ben")
CandidateList.append(Ben)
Marco= Candidate("Marco")
CandidateList.append(Marco)
Carley= Candidate("Carley")
CandidateList.append(Carley)



def get_data():
    count = 1
    total = 39692
    sentiment = ['positive','negative','neutral']
    for ind in range(1,total):
        curr_tweet = defaultdict()
        if sheet.row_values(ind)[5].lower() not in sentiment:
            continue
        curr_tweet['id']=sheet.row_values(ind)[0]
        curr_tweet['candidate']=sheet.row_values(ind)[1]
        curr_tweet['tweet']= "".join(sheet.row_values(ind)[2]).encode("utf-8")
        curr_tweet['tweet_location']=sheet.row_values(ind)[3]
        curr_tweet['geo_location']=sheet.row_values(ind)[4]
        curr_tweet['label']=sheet.row_values(ind)[5].lower()

        if curr_tweet['candidate'] == 'Hillary':
            Hillary.insertTweet(curr_tweet)
        elif curr_tweet['candidate'] == 'Bernie':
            Bernie.insertTweet(curr_tweet)
        elif curr_tweet['candidate'] == 'Trump':
            Trump.insertTweet(curr_tweet)
        elif curr_tweet['candidate'] == 'Ben':
            Ben.insertTweet(curr_tweet)
        elif curr_tweet['candidate'] == 'Martin':
            Martin.insertTweet(curr_tweet)
        elif curr_tweet['candidate'] == 'Marco':
            Marco.insertTweet(curr_tweet)
        else:
            Carley.insertTweet(curr_tweet)

get_data()






def prepareData(CandidateList):
    positiveText = ""
    negativeText = ""
    neutralText = ""

    vectors = []
    labels = []

    for candidate in CandidateList:
        positiveDict = candidate.positive
        for item  in positiveDict:
            text = positiveDict[item].tweet
            positiveText += text
            vec = text.split()
            vectors.append(vec)
            labels.append("positive")
    for candidate in CandidateList:
        negativeDict = candidate.negative
        for item  in negativeDict:
            text = negativeDict[item].tweet
            negativeText += text
            vectors.append(vec)
            labels.append("negative")
    for candidate in CandidateList:
        neutralDict = candidate.neutral
        for item  in neutralDict:
            text = neutralDict[item].tweet
            neutralText += text
            vectors.append(vec)
            labels.append("neutral")
    positiveTokens = wt(positiveText)
    negativeTokens = wt(negativeText)
    neutralTokens = wt(neutralText)

    positiveDist = freq(positiveTokens)
    negativeDist = freq(negativeTokens)
    neutralDist = freq(neutralTokens)

    tempVector = defaultdict()

    mostCount = 30
    mostPositive = positiveDist.most_common(mostCount)
    mostNegative = negativeDist.most_common(mostCount)
    mostNeutral = neutralDist.most_common(mostCount)




    for mytuple in positiveDist.items():
        if mytuple not in mostPositive and mytuple[1] > 1:
            tempVector[len(tempVector)] = mytuple[0]
    for mytuple in negativeDist.items():
        if mytuple not in mostNegative and mytuple[1] > 1:
            tempVector[len(tempVector)] = mytuple[0]
    for mytuple in neutralDist.items():
        if mytuple not in mostNeutral and mytuple[1] > 1:
            tempVector[len(tempVector)] = mytuple[0]

    print len(tempVector)
    tempvector = {tempVector[w]: w for w in tempVector}
    print len(tempvector)
    return (vectors,labels,tempvector)

(vectors,labels,temp)=prepareData(CandidateList)

def svmVector(vectors,labels,svmvector):
    trainvector = []
    trainlabel = []
    for (data,label) in izip(vectors,labels):
        vec = np.zeros((len(svmvector)))
        for word in data:
            try:
                vec[svmvector[word]] = 1
            except:
                continue
        trainvector.append(vec)
        trainlabel.append(label)

    skvectors = array(trainvector)
    sklabels = array(trainlabel)

    return skvectors, sklabels

(skvector, sklabel)=svmVector(vectors,labels,temp)

def SVM_gridSearch(trainVectors, trainLabels, kernel):
    C_range = 10.0 ** arange(-2, 2)
    gamma_range = 10.0 ** arange(-2, 2)
    param_grid = dict(gamma=gamma_range, C=C_range)
    cv = StratifiedKFold(y=trainLabels, n_folds=2)
    grid = GridSearchCV(SVC(kernel=kernel), param_grid=param_grid, cv=cv, n_jobs=n_jobs) #GridSearchCV(SVC(kernel=kernel, class_weight='auto')
    grid.fit(trainVectors, trainLabels)

    ## Estimated best parameters
    C = grid.best_estimator_.C
    gamma = grid.best_estimator_.gamma
    return C, gamma
#######################################

def getCAndGamma(skvectors, sklabels, kernel = 'rbf'):
    C, gamma = SVM_gridSearch(skvectors, sklabels, kernel)
    print C
    print gamma
    return C, gamma

C,gamma = getCAndGamma(skvector,sklabel)
clf = OneVsRestClassifier(SVC(C=C, kernel='linear', gamma= gamma,verbose= False, probability= False))
testvector = skvector
clf.fit(skvector,sklabel)
predicted = clf.predict(testvector)

print "classification reports: ", classification_report(sklabel,predicted)
print "Accuracy score: ", round(accuracy_score(sklabel,predicted),2)


