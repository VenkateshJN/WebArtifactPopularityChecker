# -*- coding: utf-8 -*-
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.neighbors import NearestNeighbors
import time
import sys
import re
import nltk

def loadStopWords(path):
    file_input = open(path+'stop-words_combined_en.txt', 'r')
    stop_words = {}
    for word in file_input:
        word = re.sub(r'\W+', '', word)
        stop_words[word] = 1
    return stop_words

def tokenize(text, stop_words, stemmer):
    raw_tokens = text.split()
    array = ''
    for token in raw_tokens:
        if len(token) > 1:
            word = token.lower()
            try:
                dummy = stop_words[word]
            except KeyError:
                word = re.sub(r'\W+', '', word)
                word = stemmer.stem(word)
                array += word + ' '
    array =  array[:-1]
    return array

def parseFromFile(tokens_file, stop_words, stemmer):
    train_samples = []
    train_labels = []
    for i in range(len(tokens_file)):
        line = tokens_file[i]
        raw_tokens = line.split()
        if len(raw_tokens) > 0:
            sample = tokenize(line, stop_words, stemmer)
            label = i + 1
            train_samples.append(sample)
            train_labels.append(label)
    return train_samples, train_labels
    
def parseFromFileTest(path):
    stop_words = loadStopWords(path)
    stemmer = nltk.stem.porter.PorterStemmer()
    twitter_file = open(path+'Twitter_NonArtifacts.txt', 'r')
    twitter_lines = []
    i = 0
    for line in twitter_file:
        if i % 4 == 0:
            string = tokenize(line, stop_words, stemmer)
            twitter_lines.append(string)
        i += 1
    twitter_file.close()
    facebook_file = open(path+'Facebook_NonArtifacts.txt', 'r')
    facebook_lines = []
    for line in facebook_file:
        string = tokenize(line, stop_words, stemmer)
        facebook_lines.append(string)
    facebook_file.close()
    return facebook_lines, twitter_lines
    
def featurePipeline(data):
    count_vect = CountVectorizer()
    X_train_counts = count_vect.fit_transform(data)
    tfidf_transformer = TfidfTransformer()
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    return X_train_tfidf, count_vect

def testPipeline(data, count_vect):
    X_test_counts = count_vect.transform(data)
    tfidf_transformer = TfidfTransformer()
    X_test_tfidf = tfidf_transformer.fit_transform(X_test_counts)
    return X_test_tfidf

def cluster(path, X_train_tfidf, train_labels, fb_tfidf, tw_tfidf):
    nbrs = NearestNeighbors(n_neighbors=10, algorithm='ball_tree').fit(X_train_tfidf)
    fb_distances, fb_indices = nbrs.kneighbors(fb_tfidf)
    tw_distances, tw_indices = nbrs.kneighbors(tw_tfidf)
 
    outputpath='./output/'	   
    out_file = open(outputpath+'kNNResults_Facebook.txt', 'w')
    for j in range(len(fb_indices)):
        l = fb_indices[j]
        string = 'fb' + str(j + 1) + ','
        for i in range(len(l)):
            new = train_labels[l[i]]
            score = fb_distances[j][i]
            string += str(new) + ',' + str(score) + ','
        string = string[:-1]
        string += '\n'
        out_file.write(string)
    out_file.close()
    
    out_file = open(outputpath+'kNNResults_Twitter.txt', 'w')
    for j in range(len(tw_indices)):
        l = tw_indices[j]
        string = 'tw' + str(j + 1) + ','
        for i in range(len(l)):
            new = train_labels[l[i]]
            score = tw_distances[j][i]
            string += str(new) + ',' + str(score) + ','
        string = string[:-1]
        string += '\n'
        out_file.write(string)
    out_file.close()

def generateData(path):
    tokens_file = open(path+'AllArtifacts_Tokens.txt', 'r').readlines()
    stop_words = loadStopWords(path)
    stemmer = nltk.stem.porter.PorterStemmer()
    train_samples, train_labels = parseFromFile(tokens_file, stop_words, stemmer)
    X_train_tfidf, count_vect = featurePipeline(train_samples)
    return X_train_tfidf, count_vect, train_labels

def main():
    #path = 'D:/IIIT-H course datasets/major_project/'
    #path = '/media/payne/Shared/IIIT-H course datasets/major_project/'
    #user_input = raw_input("Enter path for main folder: ")
    #path = user_input
    path = './dataset/'
    
    t1 = time.time()
    X_train_tfidf, count_vect, train_labels = generateData(path)
    t2 = time.time()
    print 'Load and Prepare Train data', t2 - t1
    fb_test, tw_test = parseFromFileTest(path)
    fb_tfidf = testPipeline(fb_test, count_vect)
    tw_tfidf = testPipeline(tw_test, count_vect)
    t3 = time.time()
    print 'Load and Prepare Test data', t3 - t2
    
    #print X_train_tfidf.shape[0]
    #print max(train_labels)
    cluster(path, X_train_tfidf, train_labels, fb_tfidf, tw_tfidf)
    t4 = time.time()
    print 'Classification + Writing output', t4 - t3
    #evaluate(path, train_map, fb_map, tw_map)   
        

if __name__ == '__main__':
    main()
