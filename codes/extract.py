#writes texts for each artifact

import nltk
import sys
from boilerpipe.extract import Extractor

fin=open(sys.argv[1])

d=fin.readlines()
#q=sys.argv[1].split('.')

fout=open('output/Tokens.txt','w+')

for i in d: 
	try:
		extractor = Extractor(extractor='ArticleExtractor', url=i)
		extracted_text=extractor.getText()


		l=extracted_text.split('\n');
		s=[]

		for j in range(0,len(l)):
			p=nltk.word_tokenize(l[j])
			for k in p:
				s.append(k)
		for j in s:
			print>>fout, j.encode('utf8'),
		print>>fout
	except:
	  	print>>fout
	 

fin.close()
fout.close()


