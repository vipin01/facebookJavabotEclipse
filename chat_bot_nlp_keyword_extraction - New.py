# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 15:58:39 2016

@author: Vipin
"""

import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

from collections import Counter
from math import sqrt
import re

import csv
import pickle


sent=[]
#ifile  = open('/opt/bitnami/pyfiles/ques_uk.csv', "r", encoding = "ISO-8859-1")
ifile  = open('C:/Users/Vipin/Desktop/chatBot/ques_us.csv', "r")
read = csv.reader(ifile)
for row in read :
    sent.append(row[0])
ifile.close()


def sim(word1, word2, lch_threshold=3):
    results = []
    for net1 in wn.synsets(word1):
        for net2 in wn.synsets(word2):
            try:
                lch = net1.lch_similarity(net2)
            except:
                continue
           
            try:
                if lch >= lch_threshold:
                    results.append((net1, net2))
            except:
                continue
            
    if not results:
        return False
    return True
 

def filter_tokens(input):
    # replace all apostrophe with blank
    tokens=re.sub('[^A-Za-z0-9]+'," ",input)    
    # tokenize the string    
    tokens=word_tokenize(tokens)
    # convert every character to lower case
    tokens=[word.lower() for word in tokens]
    # get the part of speech of each token
    tokens=pos_tag(tokens)
    # keep only nouns, adverb, adjective and verb tokens
    tokens=[word for word,pos in tokens if pos == 'NN' or pos=='NNS' or 
              pos=='NNP' or pos=='NNPS'or pos=='VBN' or pos=='VB' or pos=='VBD'
              or pos=='VBG' or pos=='VBP' or pos=='VBZ' or pos=='JJ' or pos=='RB']
    # remove stop words
    s=set(stopwords.words('english'))
    s.update(['please','help'])
    tokens = [word for word in tokens if word not in s]
    # lemmatize all tokens into its present form
    lmtzr = WordNetLemmatizer()
    tokens=[lmtzr.lemmatize(word,'v') for word in tokens]
    # remove all tokens having less than 2 characters
    tokens=[word for word in tokens if len(word) > 1]
    
    for i in range(len(tokens)):
        if tokens[i] in keywordsDict: continue
        else:
            for j in keywordsDict:
                if(sim(tokens[i],j)):
                    tokens[i]= j
            if tokens[i] not in keywordsDict:
                keywordsDict.append(tokens[i])
    
    return tokens


def word2vec(word):
    # count the characters in word
    cw = Counter(word)
    # precomputes a set of the different characters
    sw = set(cw)
    # precomputes the "length" of the word vector
    lw = sqrt(sum(c*c for c in cw.values()))
    # return a tuple
    return cw, sw, lw

def cosdis(v1, v2):
    # which characters are common to the two words?
    common = v1[1].intersection(v2[1])
    # by definition of cosine distance we have
    return sum(v1[0][ch]*v2[0][ch] for ch in common)/v1[2]/v2[2]    
  
      
# build keyword dictionary with the existing data
keywordsDict=[]
key_words_list=[filter_tokens(test) for test in sent]


# open the file for writing
fileObject = open("C:/Users/Vipin/Desktop/chatBot/usKeywordsPickle",'wb')

pickle.dump(key_words_list,fileObject)   
# here we close the fileObject
fileObject.close()

# open the file for writing
fileObject = open("C:/Users/Vipin/Desktop/chatBot/usKeywordsDict",'wb')

pickle.dump(keywordsDict,fileObject)   
# here we close the fileObject
fileObject.close()

# we open the file for reading
b = pickle.load(open("C:/Users/Vipin/Desktop/chatBot/usKeywordsPickle",'rb'))
c = pickle.load(open("C:/Users/Vipin/Desktop/chatBot/usKeywordsDict",'rb'))

