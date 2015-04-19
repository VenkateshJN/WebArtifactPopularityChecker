import MySQLdb as mdb
import sys
import urllib2

f=open('output/indexResults_Twitter.txt')
d=f.readlines()

f1=open('output/Tweets_likes.txt')
d1=f1.readlines()

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()

		for i in d:
			p=i.split(',')
			if p[0].endswith('\n'):
				p[0]=p[0][:-1]
			number=int(p[0][1:])
			features=d1[number-1].split(" ")
			for xc in range(1,len(p),2):
				ids=int(p[xc])
				if p[2].endswith('\n'):
					p[2]=p[2][:-1]
				maxvalue=float(p[2])
				if p[xc+1].endswith('\n'):
					p[xc+1]=p[xc+1][:-1]
				weight=float(p[xc+1])
				cur.execute("SELECT id,likes,comment,share FROM Index_Score where artifact_id='%d'" %ids)
				rows = cur.fetchall()
				for r in rows:
					ids=int(r[0])
					likes=int(float(weight/maxvalue)*int(features[0]))+int(r[1])	#heuristics	
					comment=int(r[2])
					if features[1].endswith('\n'):
						features[1]=features[1][:-1]
					share=int(float(weight/maxvalue)*int(features[1]))+int(r[3])
					cur.execute("UPDATE Index_Score SET likes = %d, comment=%d, share=%d WHERE artifact_id = %d" %(likes,comment,share,ids))  

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close
