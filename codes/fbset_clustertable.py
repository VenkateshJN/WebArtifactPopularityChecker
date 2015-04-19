## updates cluster table for fb artifacts

import MySQLdb as mdb
import sys
import urllib2

f=open('output/kNNResults_Facebook.txt')
d=f.readlines()

f1=open('output/Posts_like.txt')
d1=f1.readlines()

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()

		for i in d:
			p=i.split(',')
			number=p[0][2:]
			if number.endswith('\n'):
				number=number[:-1]
			number=int(number)
			features=d1[number-1].split(" ")
			for xc in range(1,len(p),2):
				ids=int(p[xc])
				if p[-1].endswith("\n"):
					p[-1]=p[-1][:-1]
				maxvalue=float(p[-1])
				if p[xc+1].endswith('\n'):
					p[xc+1]=p[xc+1][:-1]
				weight=float(p[xc+1])
				cur.execute("SELECT id,likes,comment,share FROM Cluster_Score where artifact_id='%d'" %ids)
				rows = cur.fetchall()
				for r in rows:
					ids=int(r[0])
					likes=int(float(weight/maxvalue)*int(features[0]))+int(r[1])
					comment=int(float(weight/maxvalue)*int(features[1]))+int(r[2])
					if features[2].endswith('\n'):
						features[2]=features[2][:-1]
					share=int(float(weight/maxvalue)*int(features[2]))+int(r[3])
					cur.execute("UPDATE Cluster_Score SET likes = %d, comment=%d, share=%d WHERE artifact_id = %d" %(likes,comment,share,ids))  

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close
