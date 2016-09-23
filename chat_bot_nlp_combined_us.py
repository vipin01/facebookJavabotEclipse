# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 17:10:50 2016

@author: Vipin
"""

from nltk import word_tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn

from collections import Counter
from math import sqrt,ceil
import re

import csv
import sys
import pickle

sent=[]
#ifile  = open('/opt/bitnami/pyfiles/ques_us.csv', "r", encoding = "ISO-8859-1")
ifile  = open('C:/Users/Vipin/Desktop/chatBot/ques_us.csv', "r", encoding = "ISO-8859-1")
read = csv.reader(ifile)
for row in read :
    sent.append(row[0])
ifile.close()

ans=[]
#ifile  = open('/opt/bitnami/pyfiles/ans_us.csv', "r", encoding = "ISO-8859-1")
ifile  = open('C:/Users/Vipin/Desktop/chatBot/ans_us.csv', "r", encoding = "ISO-8859-1")
read = csv.reader(ifile)
for row in read :
    ans.append(row[0])
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
            
    if not results: return False
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
  

# read keyword dictionary from disk
key_words_list= pickle.load(open("C:/Users/Vipin/Desktop/chatBot/usKeywordsPickle",'rb'))
#key_words_list= pickle.load(open("/opt/bitnami/pyfiles/usKeywordsPickle",'rb'))

keywordsDict = pickle.load(open("C:/Users/Vipin/Desktop/chatBot/usKeywordsDict",'rb'))

# input string
input_str= sys.argv[1]
#input_str= "How can I get cash from my card if I need it?"

# extract all important tokens from the input
input_tokens=filter_tokens(input_str)

for i in range(len(input_tokens)):
    if input_tokens[i] not in keywordsDict: 
        for j in keywordsDict:
            if(sim(input_tokens[i],j)): input_tokens[i]= j

score_it_kw=[]
max_score_it_kw=[]
score=[]
for key_words_list_index in range(len(key_words_list)):
    for key_words in key_words_list[key_words_list_index]:
        for input_tokens_word in input_tokens:
            va=word2vec(input_tokens_word)
            vb=word2vec(key_words)
            score_it_kw.append(ceil(cosdis(va,vb)*100)/100)
        max_score_it_kw.append(max(score_it_kw))
        score_it_kw=[]
    score.append(sum(max_score_it_kw)/len(key_words_list[key_words_list_index]))
    max_score_it_kw=[]
              
if max(score)>=0.85 :
    print("If you are looking for '"+sent[score.index(max(score))]+"', please visit "+ans[score.index(max(score))])
    #print(ans[score.index(max(score))])
else :
    print("Not found in the database")
