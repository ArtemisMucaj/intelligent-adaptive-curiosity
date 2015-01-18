# Copyright 2015,  Jean-Baptiste Assouad et Artemis Mucaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
def kppv(exemple,base,k):
	dis = []
	for i in range(0,len(base)):
		dis.append( [distance(exemple,base[i]) , i] )
		pass
	dis.sort()
	#moyenne sur le dernier terme de chaque exemple de la base
	moy = 0.0
	for i in range(0,k):
		moy += base[dis[i][1]][len(exemple)-1]
		pass
	moy /= k
	return moy


def distance(u1,u2):
	res = 0
	for i in range(0,len(u1)-1):
		res += (u1[i] - u2[i])**2
		pass
	return res

'''
exemple = [1,1,3]
base = [ [1,2,2] , [2,3,-2] , [5,6,1] , [-1,0,2] ]
print kppv(exemple,base,2)
'''