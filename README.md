# WebArtifactPopularityChecker

Prerequisites: 
Install MySql (configure it as username:'root',password:'iiit123',database:'popularity')


Run as:
In the directory Team3 just type

./run.sh *fb_json_file* *twitter_json_file*

Example: ./run_sh dataset/Facebook_dataset dataset/Twitter_dataset.json



Output will be stored in the output folder in files named:

Index_Score - Scores based on Indexing Results
Knn_Score - Scores based on KNN Results
popularity.sql - MySQL dump


Introductory Video : https://www.youtube.com/watch?v=ZfFu4NTXMjU&feature=youtu.be

Slideshare: http://www.slideshare.net/tutulive/computing-social-score-of-web-aritfacts

