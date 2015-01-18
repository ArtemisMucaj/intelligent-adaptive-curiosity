# Copyright 2015,  Jean-Baptiste Assouad et Artemis Mucaj
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

from copy import copy
import tree
import matplotlib.pyplot as plt
###################################

# Plot l'erreur moyenne en prediction
def superPlot(Pbdd):
	if Pbdd.dimCutVal == -1:
		plt.plot(Pbdd.LEM)
	else:
		superPlot(Pbdd.n1)
		superPlot(Pbdd.n2)
		pass
	pass

# Calcul la liste des valeures medianes du
# vecteur data
def median(data):
	listTmp = []
	med = []
	for i in range(0,len(data[0])):

		for x in range(0,len(data)):
			listTmp.append(data[x][i])
			pass
		listTmp.sort()
		med.append(listTmp[len(listTmp)/2])
		pass
	return med

# Moyenne mobile entre les elements de list ainsi que
# x_n sur delay valeures
def moyenneMobile(list,x_n,delay):
	moy = x_n
	for i in range(1,delay+1):
		moy += list[len(list)-i]
		pass
	moy /= delay + 1
	return moy

# Retournes la liste d'erreurs de l'expert associe a l'action
def getTheGoodLE(Pbdd,action):
	if Pbdd.dimCutVal == -1:
		return Pbdd.LE
	else:
		#print 'dimCutVal =',Pbdd.dimCutVal,'action =',action##########
		if action[Pbdd.dimCutVal] < Pbdd.cutval:
			return getTheGoodLE(Pbdd.n1,action)
			pass
		else:
			return getTheGoodLE(Pbdd.n2,action)
			pass
		pass
	pass

# Retournes l'erreure de prediction de l'element i de l'expert
# associe a action
def getTheGoodLEM(Pbdd,i,action):
	if Pbdd.dimCutVal == -1:
		return Pbdd.LEM[len(Pbdd.LE)-(i+1)]
	else:
		if action[Pbdd.dimCutVal] < Pbdd.cutval:
			return getTheGoodLEM(Pbdd.n1,i,action)
			pass
		else:
			return getTheGoodLEM(Pbdd.n2,i,action)
			pass
		pass
	pass

# Retournes le sous arbre de l'expert correspondant a l'action
def getTheGoodTree(Pbdd,action):
	if Pbdd.dimCutVal == -1:
		return Pbdd
	else:
		if action[Pbdd.dimCutVal] < Pbdd.cutval:
			return getTheGoodTree(Pbdd.n1,action)
			pass
		else:
			return getTheGoodTree(Pbdd.n2,action)
			pass
		pass
	pass

# Calcul de la variance suivant une dimension en utilisant
# separator pour distinguer deux classes
def variance(data, dimension, separator):
	m = 0
	m_1 = 0
	m_2 = 0
	count_1 = 0
	count_2 = 0
	for x in range(0,len(data)):
		m += data[x][dimension]
		if data[x][dimension] > separator:
			m_1 += data[x][dimension]
			count_1 += 1
			pass
		else:
			m_2 += data[x][dimension]
			count_2 +=1
			pass

	if count_1 == 0 or count_2 == 0:
		return 100000
		pass
	m_1/=count_1
	m_2/=count_2
	m /= len(data)
	return (1/2.0)*((m_1 - m)**2 + (m_2 - m)**2)

# Critere C2, retournes la dimension ainsi que la valeure de
# separation des donnees, dimension minimisant la variance
# interclasse (cutvalue = mediane)
def C2_criterion(BDD):
	dim = 0
	cutValue = 0
	var = 100000
	medianes = median(BDD.data)
	#print 'medianes =',medianes########################
	for x in range(0,len(medianes)):
		v = variance(BDD.data, x, medianes[x])
		if(v < var):
			var = v
			dim = x
			cutValue = medianes[x]
		pass
	#print 'var =',var,'dim =',dim,'cutValue =',cutValue#####################
	return [cutValue, dim]

# Separes la base de donnee en deux selon deux criteres, C1 et C2
def splitBDD(BDD,c1):
	if len(BDD.data) > c1-1:
		#print type(BDD),type(BDD.cutval),type(BDD.dimCutVal),type(BDD.data),type(BDD.n1),type(BDD.n2),type(BDD.LE),type(BDD.LEM)################
		cutVals = C2_criterion(BDD)
		BDD.n1 = tree.node(-1,-1,[],None,None,[],[])
		BDD.n2 = tree.node(-1,-1,[],None,None,[],[])
		for x in range(0,c1-1):
			if(BDD.data[x][cutVals[1]] <= cutVals[0]):
				BDD.n1.data.append(BDD.data[x])
			else:
				BDD.n2.data.append(BDD.data[x])
				pass
			pass
		BDD.cutval = cutVals[0]
		BDD.dimCutVal = cutVals[1]

		BDD.n1.LE = copy(BDD.LE)
		BDD.n1.LEM = copy(BDD.LEM)
		BDD.n2.LE = copy(BDD.LE)
		BDD.n2.LEM = copy(BDD.LEM)

		#supp de DATA LE et LEM du pere
		BDD.LE = []
		BDD.LEM = []
		BDD.data = []
	else:
		pass
