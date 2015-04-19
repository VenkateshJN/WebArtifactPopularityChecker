import MySQLdb as mdb
import sys
import urllib2

f=open('output/FinalArtifacts.txt')
d=f.readlines()
print len(d)
f1=open('output/TwArtifacts_like.txt')
d1=f1.readlines()
print len(d)

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()


		for i in d1:
			p=i.split(' ')
			cur.execute("SELECT id,likes,comment,share FROM Artifact_Likes where artifact='%s'" %p[0])
			rows = cur.fetchall()
			for r in rows:
				ids=int(r[0])
				likes=int(p[1])+int(r[1])
				comment=int(r[2])
				if p[2].endswith('\n'):
					p[2]=p[2][:-1]
				share=int(p[2])+int(r[3])
				cur.execute("UPDATE Artifact_Likes SET likes = %d, comment=%d, share=%d WHERE Id = %d" %(likes,comment,share,ids))  
				print "done"
				cur.execute("SELECT likes,comment,share FROM Index_Score where artifact_id='%d'" %ids)
				row = cur.fetchall()
				print "hi"
				for st in row:
					likes=int(p[1])+int(st[0])
					comment=int(st[1])
					if p[2].endswith('\n'):
						p[2]=p[2][:-1]
					share=int(p[2])+int(st[2])
					cur.execute("UPDATE Index_Score SET likes = %d, comment=%d, share=%d WHERE artifact_id = %d" %(likes,comment,share,ids))   
			
				cur.execute("SELECT likes,comment,share FROM Cluster_Score where artifact_id='%d'" %ids)
				row = cur.fetchall()
				print "byee"
				for st in row:
					likes=int(p[1])+int(st[0])
					comment=int(st[1])
					if p[2].endswith('\n'):
						p[2]=p[2][:-1]
					share=int(p[2])+int(st[2])
					cur.execute("UPDATE Cluster_Score SET likes = %d, comment=%d, share=%d WHERE artifact_id = %d" %(likes,comment,share,ids))   
			

		

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close
