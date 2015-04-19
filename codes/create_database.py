#Table definition for MySQl

import MySQLdb as mdb
import sys

f=open('./output/FinalArtifacts.txt')
d=f.readlines()


try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()
		cur.execute("DROP TABLE IF EXISTS Artifact_Likes CASCADE")
		cur.execute("DROP TABLE IF EXISTS Index_Score CASCADE")
		cur.execute("DROP TABLE IF EXISTS Cluster_Score CASCADE")


		cur.execute("CREATE TABLE Artifact_Likes(id INT PRIMARY KEY AUTO_INCREMENT, artifact VARCHAR(150), likes INT, comment INT, share INT)")
		print "done"
		cur.execute("CREATE TABLE Index_Score(id INT PRIMARY KEY AUTO_INCREMENT, artifact_id INT, likes INT, comment INT, share INT,score FLOAT(20,2), normalised_score FLOAT(10,8))")
		print "done2"

		cur.execute("CREATE TABLE Cluster_Score(id INT PRIMARY KEY AUTO_INCREMENT, artifact_id INT, likes INT, comment INT, share INT,score FLOAT(20,2), Normalised_Score FLOAT(10,8))")
		print "done3"
		
		for i in range(len(d)):
			if d[i].endswith('\n'):
				d[i]=d[i][:-1]
			string="INSERT INTO Artifact_Likes(artifact,likes,comment,share) VALUES('"+d[i]+"',0,0,0)"
			cur.execute(string)
			cur.execute("INSERT INTO Index_Score(artifact_id,likes,comment,share) VALUES(%d,0,0,0)" %(i+1))
			cur.execute("INSERT INTO Cluster_Score(artifact_id,likes,comment,share) VALUES(%d,0,0,0)" %(i+1))




except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close
