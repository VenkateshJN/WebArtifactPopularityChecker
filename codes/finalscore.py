import MySQLdb as mdb
import sys
import urllib2

f=open('output/FinalArtifacts.txt')
d=f.readlines()

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()

		for i in range(1,len(d)+1):
			cur.execute("SELECT id,likes,comment,share FROM Index_Score where artifact_id=%d" %i)
			rows = cur.fetchall()
			for r in rows:
				print r[0],r[1],r[2],r[3]
				ids=int(r[0])
				likes=int(r[1])
				comment=int(r[2])
				share=int(r[3])
				score=likes+(2*comment)+(5*share)
				cur.execute("UPDATE Index_Score SET score=%f WHERE id = %d" %(score,ids))  
			
			cur.execute("SELECT id,likes,comment,share FROM Cluster_Score where artifact_id=%d" %ids)
			rows = cur.fetchall()
			for r in rows:
				print r[0],r[1],r[2]
				ids=int(r[0])
				likes=int(r[1])
				comment=int(r[2])
				share=int(r[3])
				score=likes+(2*comment)+(5*share)
				cur.execute("UPDATE Cluster_Score SET score=%f WHERE id=%d" %(score,ids))   
			
			

		


except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close
