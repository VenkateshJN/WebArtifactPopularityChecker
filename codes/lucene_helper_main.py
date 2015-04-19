# -*- coding: utf-8 -*-
#!/usr/bin/python
import os
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
    
def makeDirectoryStructure(path):
    directory = path + 'Raw_Data/'  # this folder contatins text of each artifact in each file
    if not os.path.exists(directory):
        os.makedirs(directory)
    tokens_file = open(path+'AllArtifacts_Tokens.txt', 'r').readlines()
    idx = 0
    for i in range(len(tokens_file)):
        idx += 1
        line = tokens_file[i]
        raw_tokens = line.split()
        if len(raw_tokens) > 0:
            #string = str(idx) + ':=' + url
            f = open(directory+str(idx)+'.txt', 'w')
            f.write(line)
            f.close()

def prepareNonArtifacts(path):
    stop_words = {} #loadStopWords(path)
    stemmer = nltk.stem.porter.PorterStemmer()
    twitter_file = open(path+'Twitter_NonArtifacts.txt', 'r')
    twitter_output = open(path+'Cleaned_Twitter_NonArtifacts_Tokens.txt', 'w')
    i = 0
    for line in twitter_file:
        if i % 4 == 0:
            string = tokenize(line, stop_words, stemmer)
            twitter_output.write(string + '\n')
        i += 1
    twitter_file.close()
    twitter_output.close()
    facebook_file = open(path+'Facebook_NonArtifacts.txt', 'r')
    facebook_output = open(path+'Cleaned_Facebook_NonArtifacts_Tokens.txt', 'w')
    for line in facebook_file:
        string = tokenize(line, stop_words, stemmer)
        facebook_output.write(string + '\n')
    facebook_file.close()
    facebook_output.close()
 
def main():
    #path = 'D:/IIIT-H course datasets/major_project/'
    #path = '/media/payne/Shared/IIIT-H course datasets/major_project/'
    #user_input = raw_input("Enter path for main folder: ")
    #path = user_input
    path = './dataset/'
    
    makeDirectoryStructure(path)
    prepareNonArtifacts(path)            
 
 
if __name__ == '__main__':
    main()
