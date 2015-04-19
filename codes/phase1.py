import MySQLdb as mdb
import sys
import urllib2

f=open('output/Phase1.txt','w+')

try:
	con=mdb.connect('localhost','root','iiit123','popularity');
	with con:

		cur=con.cursor()
		cur.execute("SELECT artifact, likes,comment,share FROM Artifacts_Likes;")
		rows = cur.fetchall()
		for r in rows:
			score = int(r[1])+(2*int(r[2]))+(5*int(r[3]))
			print>>f, str(r[0]),
			print>>f, score,
			print>>f

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		f.close()
		con.close
