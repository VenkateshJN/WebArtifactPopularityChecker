#!/bin/bash

python ./codes/Parser.py $1 	#parsing fb data
python ./codes/Tweets.py $2	#parsing twitter data
python ./codes/Artifact.py $2 #parsing twitter data

#Combining facebook and twitter artifacts

cat ./output/FbArtifacts.txt ./output/TwArtifact.txt >> ./output/Artifacts.txt #combined artifacts
sort ./output/Artifacts.txt >> ./output/artifacts.txt
rm ./output/Artifacts.txt
cat ./output/artifacts.txt | uniq >> ./output/FinalArtifacts.txt
rm ./output/artifacts.txt

python ./codes/extract.py ./output/FinalArtifacts.txt

python ./codes/knn_main.py 			##Clustering
python ./codes/lucene_helper_main.py

java -jar ./codes/Lucene_IndexingFB.jar		##Indexing
java -jar ./codes/Lucene_IndexingTW.jar

## To execute the following one need to install mysql username:root password:iiit123 database_name:popularity 

python ./codes/create_database.py
python ./codes/fbpopulate_database.py
python ./codes/twpopulate_database.py
python ./codes/fbset_indextable.py
python ./codes/fbset_clustertable.py
python ./codes/modify.py
python ./codes/twset_indextable.py
python ./codes/twset_clustertable.py
python ./codes/finalscore.py
python ./codes/indexscore.py
python ./codes/knnscores.py
