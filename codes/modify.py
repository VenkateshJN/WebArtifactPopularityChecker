import sys

f=open('Tweets.txt')
f1=open('Tweets_likes.txt','w+')

d=f.readlines()
print len(d)

for i in range(1,len(d),4):
	print>>f1, d[i][:-1],d[i+1][:-1]
f1.close()

