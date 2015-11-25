from collections import defaultdict
import nltk
import numpy as np
from numpy import array, arange, zeros, hstack, argsort
from itertools import  izip

class Tweet(object):
    def __init__(self,tweet):
        self.id =
        self.tweet =
        self.tweetlocation =
        self.geolocation =
        self.label =

class Candidate(object):
    def __init__(self,name):
        self.candidate = name
        self.positive = defaultdict()
        self.negative = defaultdict()
        self.neutral = defaultdict()

    def insertTweet(self,tweet):
        myobject = Tweet(tweet)
        if tweet.label == "Positive":
            self.positive[len(self.positive)]= myobject
        elif tweet.label == "Negative":
            self.negative[len(self.negative)]= myobject
        else:
            self.neutral[len(self.neutral)] = myobject

    def getTweets(self,label):
        if label == "Positive":
            data = self.positive
        elif label == "Negative":
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
    positiveTokens = nltk.word_tokenize(positiveText)
    negativeTokens = nltk.word_tokenize(negativeText)
    neutralTokens = nltk.word_tokenize(neutralText)

    positiveDist = nltk.FreqDist(positiveTokens)
    negativeDist = nltk.FreqDist(negativeTokens)
    neutralDist = nltk.FreqDist(neutralTokens)

    tempVector = {}

    mostCount = 50
    mostPositive = positiveDist.most_common(mostCount)
    mostNegative = negativeDist.most_common(mostCount)
    mostNeutral = neutralDist.most_common(mostCount)

    for mytuple in positiveDist:
        if mytuple not in mostPositive and mytuple[1] > 4:
            tempVector[len(tempVector)] = mytuple[0]
    for mytuple in negativeDist:
        if mytuple not in mostNegative and mytuple[1] > 4:
            tempVector[len(tempVector)] = mytuple[0]
    for mytuple in neutralDist:
        if mytuple not in mostNeutral and mytuple[1] > 4:
            tempVector[len(tempVector)] = mytuple[0]

    tempvector = {tempVector[w]: w for w in tempVector}
    return (vectors,labels,tempvector)

def svmVector(vectors,labels,svmvector):
    trainvector = []
    trainlabel = []
    for (data,label) in izip(vectors,labels):
        vec = np.zeroes((len(svmvector)))
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





