import numpy as np
import scipy as sc
import re
from numpy.linalg import norm
from scipy.spatial import distance

f = open('/Users/denmak/Documents/MLfromMIPT/ASSESMENTS/Week2/Sentences.txt','r')

lines = []
statmatrix = []
globalmatrix = []
globalwords = {}


def wordcount(line,word):
	i = 0
	for wd in line:
		if wd == word:
			i = i+1
	return i

def getWords(strings):
	words={}
	lines = []
	matrix = []
	indexW = 0
	indexS = 0
	for str in strings:
		str = re.split('[^a-z]', str.lower().replace(',','').replace('.','').replace('-',''))
		for word in str:
			ind = 0
			if words.has_key(word) and word!='' and word!=' ' and len(word)>0:
				ind = words[word]
				matrix.append([indexS, ind, wordcount(str, word), word])
			elif word != '' and word!=' ' and len(word)>0:
				words[word] = indexW
				ind = indexW
				indexW = indexW + 1
				matrix.append([indexS, ind, wordcount(str, word), word])



		lines.append(str)
		indexS =indexS + 1

	return words,matrix,lines



globalwords,globalmatrix,lines = getWords(f)

statmatrix = [[0] * len(globalwords.keys()) for i in range( len(lines) )]



print globalwords.items()
print len(globalwords.keys())
#print lines
#print globalmatrix
#print statmatrix


for line in globalmatrix:
	statmatrix[line[0]][line[1]] = line[2]
	print line[0],line[1],line[2],line[3]




#print statmatrix
cos_angles=[]
cos_dist = []

for s in statmatrix:
	cos_angles.append([statmatrix.index(s),np.dot(statmatrix[0], s) / norm(statmatrix[0]) / norm(s)])
print cos_angles

i=0
for s in statmatrix:
	d = [i,distance.cosine(s,statmatrix[0])]
	print 'row: ',str(i),' :', s
	print 'dist from:',str(i),' to 0 =',d
	cos_dist.append(d)
	i=i+1
print cos_dist



cl = sorted(cos_dist, key=lambda sp: sp[1])
print cl[:3]
#[[0, 1.0], [6, 0.32433748657040123], [21, 0.31524416249564025]]

submission1 = open('/Users/denmak/Documents/MLfromMIPT/ASSESMENTS/Week2/submission-1.txt','w')
submission1.write(''+str(cl[1][0])+' '+str(cl[2][0]))

print ''+str(cl[1][0])+' '+str(cl[2][0])
print len(cl)
print cl


#-----------------------------------------------------------------------------------------------

f = open('/Users/denmak/Documents/MLfromMIPT/ASSESMENTS/Week2/submission-2.txt','w')
f.write('4.36 -1.30  0.19 -0.01')
f.close()



