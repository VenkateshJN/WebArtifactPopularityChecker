import json
import ast
import urllib2
import urlmarker
import re
import sys
import csv
import nltk

sl={}	#stores the paging details for likes
sc={}	#stores the paging deatils for comments

d = []

bv = sys.argv[1]

#f1=open('artifacts'+bv[-1]+'_like.txt','w+')
f1=open('output/Posts.txt','w+')
f2=open('output/Posts_like.txt','w+')
f3=open('output/FbArtifacts_like.txt','w+')
f4=open('output/FbArtifacts.txt','w+')

json_data=open(bv)



with open(bv) as json_data:
	d = json_data.readlines()#each line corresponds to one post
	for i in d:

		l={}
		data=[]
		countlikes=0		#stores the number of likes
		countcomment=0		#stores the number of comments	
		countshare=0		#stores the number of shares
		l = ast.literal_eval(i)

		
		
		if 'likes' in l:
			countlikes= len(l['likes']['data'])
			if 'next' in l['likes']['paging']:
				za=l['likes']['paging']['next']
				pe=za.split('?')
				sts=pe[0]+'?summary=1&'+pe[1]
				pl=urllib2.urlopen(sts).read()
				sl= json.loads(pl)
				if 'summary' in sc:
					countlikes=sl['summary']['total_count']

		#------------------------------------------------
		if 'comments' in l:
			countcomment=len(l['comments']['data'])
			if 'next' in l['comments']['paging']:
				za=l['comments']['paging']['next']
				pe=za.split('?')
				sts=pe[0]+'?summary=1&'+pe[1]
				pl=urllib2.urlopen(sts).read()
				sc= json.loads(pl)
				if 'summary' in sc:
					countcomment=sc['summary']['total_count']

		#-------------------------------------------------
		data.append(l['id'])

		z=[]
		
					

			#shares
		if 'shares' in l:
			countshare=l['shares']['count']

			#likes
		
		if l['type']=='link':
			z.append(l['link'])
		if 'message' in l:
				stri = l['message'].encode('utf8')
				z=re.findall(urlmarker.URL_REGEX,stri)	#getting the url of artifacts in expanded form

		if 'message' in l and len(z)==0:
			stp=stri.replace('\n',' ')
			f1.write(str(stp))
			f1.write("\n")
			f2.write(str(countlikes))
			f2.write(" ")
			f2.write(str(countcomment))
			f2.write(" ")
			f2.write(str(countshare))
			f2.write('\n')
			f1.flush()
			f2.flush()
		else:
			for ou in z:
#try
				if 'http:' not in ou:
					ou='http://'+ou
				try:
					a=urllib2.urlopen(ou)
					sg=a.url
					if sg.endswith('/'):
						sg=sg[:-1]

					f3.write(sg)
					f3.write(" ")
					f4.write(sg)
					f4.write("\n")
#print "-----------------------"+sg
					f3.write(str(countlikes))
					f3.write(" ")
					f3.write(str(countcomment))
					f3.write(" ")
					f3.write(str(countshare))
					f3.write("\n")
					f3.flush()
					f4.flush()
				except:
					continue
json_data.close()
f1.close()
f2.close()
f3.close()
f4.close()
