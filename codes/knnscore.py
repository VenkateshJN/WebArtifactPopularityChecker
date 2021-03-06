#Prints the score of clustering to a file

import MySQLdb as mdb
import sys
import urllib2

f=open('output/Knn_Score.txt','w+')

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()
		cur.execute("SELECT a.id, a.artifact, b.score FROM Artifact_Likes a, Cluster_Score b WHERE a.id = b.artifact_id order by b.score DESC;")
		rows = cur.fetchall()
		for r in rows:
			print>>f, str(r[1]),
			print>>f, str(r[2]),
			print>>f

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		f.close()
		con.close
