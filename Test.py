#Super programme python
import vrep
import kppv
import tree
import random
import sphere
from math import sqrt
import time

import matplotlib.pyplot as plt

def superPlot(Pbdd):
	if Pbdd.dimCutVal == -1:
		plt.plot(Pbdd.LE)
	else:
		superPlot(Pbdd.n1)
		superPlot(Pbdd.n2)
		pass
	pass



print("Salut je suis un programme Python !\n")

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

def moyenneMobile(list,x_n,delay,t):
	moy = x_n
	for i in range(1,delay+1):
		moy += list[t-i]
		pass
	moy /= delay + 1
	return moy


vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)


def getTheGoodLE(Pbdd,action):
	#print type(Pbdd),type(Pbdd.cutval),type(Pbdd.dimCutVal),type(Pbdd.data),type(Pbdd.n1),type(Pbdd.n2),type(Pbdd.LE),type(Pbdd.LEM)################
	if Pbdd.dimCutVal == -1:
		return Pbdd.LE
	else:
		if action[Pbdd.dimCutVal] < Pbdd.cutval:
			return getTheGoodLE(Pbdd.n1,action)
			pass
		else:
			return getTheGoodLE(Pbdd.n2,action)
			pass
		pass
	pass


def getTheGoodLEM(Pbdd,i,action):
	if Pbdd.dimCutVal == -1:
		return Pbdd.LEM[i]
	else:
		if action[Pbdd.dimCutVal] < Pbdd.cutval:
			return getTheGoodLEM(Pbdd.n1,i,action)
			pass
		else:
			return getTheGoodLEM(Pbdd.n2,i,action)
			pass
		pass
	pass


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


def C2_criterion(BDD):
	dim = 0
	cutValue = 0
	var = -100000
	medianes = median(BDD.data)
	#print 'medianes =',medianes########################
	for x in range(0,len(medianes)):
		v = variance(BDD.data, x, medianes[x])
		if(v > var):
			var = v
			dim = x
			cutValue = medianes[x]
		pass
	#print 'var =',var,'dim =',dim,'cutValue =',cutValue#####################
	return [cutValue, dim]

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
		#if dimension ==3:
		#	print data[x][dimension]
		#	pass

	#print 'm_1 =',m_1,'m_2 =',m_2,'count_1 =',count_1,'count_2 =',count_2,'separator =',separator################
	m_1/=count_1
	m_2/=count_2
	m /= len(data)
	return (1/2.0)*((m_1 - m)**2 + (m_2 - m)**2)

def splitBDD(BDD):
	if len(BDD.data) > 249:
		#print type(BDD),type(BDD.cutval),type(BDD.dimCutVal),type(BDD.data),type(BDD.n1),type(BDD.n2),type(BDD.LE),type(BDD.LEM)################
		cutVals = C2_criterion(BDD)
		BDD.n1 = tree.node(-1,-1,[],None,None,[],[])
		BDD.n2 = tree.node(-1,-1,[],None,None,[],[])
		for x in range(0,249):
			if(BDD.data[x][cutVals[1]] > cutVals[0]):
				BDD.n1.data.append(BDD.data[x])
			else:
				BDD.n2.data.append(BDD.data[x])
				pass
			pass
		BDD.cutval = cutVals[0]
		BDD.dimCutVal = cutVals[1]

		BDD.n1.LE = BDD.LE
		BDD.n1.LEM = BDD.LEM
		BDD.n2.LE = BDD.LE
		BDD.n2.LEM = BDD.LEM

		#supp de DATA LE et LEM du pere
		BDD.LE = []
		BDD.LEM = []
		BDD.DATA = []
	else:
		pass



t=0
delay = 150
nbExemple = 20

err_world, worldHandle = vrep.simxGetObjectHandle(clientID,"world", vrep.simx_opmode_oneshot_wait)
err_epuck, epuckHandle = vrep.simxGetObjectHandle(clientID,"ePuck", vrep.simx_opmode_oneshot_wait)
err_sphere, sphereHandle = vrep.simxGetObjectHandle(clientID,"Sphere", vrep.simx_opmode_oneshot_wait)
err_left,leftHandle = vrep.simxGetObjectHandle(clientID,"ePuck_leftJoint",vrep.simx_opmode_oneshot_wait)
err_right,rightHandle = vrep.simxGetObjectHandle(clientID,"ePuck_rightJoint",vrep.simx_opmode_oneshot_wait)



Pbdd = tree.node(-1,-1,[],None,None,[],[])

MPbdd = []


while t < 700:



	actions = []

	if t==0:
		err,epuck_position = vrep.simxGetObjectPosition(clientID, epuckHandle, -1, vrep.simx_opmode_streaming)
	else:
		err,epuck_position = vrep.simxGetObjectPosition(clientID, epuckHandle, -1, vrep.simx_opmode_buffer)
		pass


	#creation des actions
	for i in range(0,nbExemple):
		actions.append( [random.uniform(-5,5) , random.uniform(-5,5) , random.uniform(0,1)] )
		pass

	if t<delay:
		#Action random
		actionChoisie = actions[0]
		pass
	else:
		#Calcul LPi pour chaque action
		Ep = []
		Emtplusun = []
		LP = []
		for x in range(0,nbExemple):

			Ep.append( kppv.kppv(actions[x], MPbdd,1) ) #### probleme de taille entre actions[x] et la base de MPbdd

			Emtplusun.append(moyenneMobile(getTheGoodLE(Pbdd,actions[x]),Ep[x],delay,t) )

			LP.append( [-(Emtplusun[x] - getTheGoodLEM(Pbdd,t-delay,actions[x]) ) , x] )
			pass

		LP.sort()

		if random.randint(0,100)<10:
			#Action random
			actionChoisie = actions[0]
			pass
		else:
			actionChoisie = actions[LP[len(LP)-1][1]]
			pass
		pass

	#On a choisi l'action

	# Estimation de S(t+1)
	T= getTheGoodTree(Pbdd,actionChoisie)


	if len(T.data) > 2:
		S_predicted = kppv.kppv(actionChoisie,T.data,2)
	else:
		S_predicted = 0
		pass
	# On realise l'action
	vrep.simxSetJointTargetVelocity(clientID,leftHandle,actionChoisie[0],vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID,rightHandle,actionChoisie[1],vrep.simx_opmode_oneshot)
	vec = sphere.sphere_controller(actionChoisie[2],epuck_position)



	if isinstance(vec,type([])) and len(vec)!=0:
		vrep.simxSetObjectPosition(clientID,sphereHandle,-1,vec,vrep.simx_opmode_oneshot)
		pass


	# On calcule E(t)
	if t ==0:
		err_sphere, spherePosition = vrep.simxGetObjectPosition(clientID,sphereHandle, -1, vrep.simx_opmode_streaming)
	else:
		err_sphere, spherePosition = vrep.simxGetObjectPosition(clientID,sphereHandle, -1, vrep.simx_opmode_buffer)


	S_calculated = sqrt((epuck_position[0] - spherePosition[0])**2 + (epuck_position[1] - spherePosition[1])**2)
	E = abs(S_predicted - S_calculated);
	#ajout a la base de donnees de MP
	actionChoisie.append(E)
	MPbdd.append( actionChoisie )

	#print 'f =',actionChoisie[2],'S_calculated =',S_calculated###################################

	# On ajoute E(t) a LE
	T.LE.append(E)
	# On calcul Em(t) et ajout a LEM
	if t>delay:
		Em = moyenneMobile(T.LE,0,delay,t)
	else:
		Em = moyenneMobile(T.LE,0,t,t)
	T.LEM.append(Em)

	#print 'actionChoisie = ',actionChoisie #################
	# ajout dans la base de donnees de P
	actionChoisie.pop()
	actionChoisie.append(S_calculated)
	T.data.append(actionChoisie)

	#print 'actionChoisie = ',actionChoisie##################

	splitBDD(T)

	print 't =',t##########################
	t+=1
	#time.sleep(1)
	pass

tree.status(Pbdd,0)

#superPlot(Pbdd)

#plt.show()

vrep.simxFinish(clientID)

'''
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
	print 'Connected to remote API server'
	res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait)
	if res==vrep.simx_return_ok:
		print 'Number of objects in the scene: ',len(objs)
	else:
		print 'Remote API function call returned with error code: ',res



	err,leftMotor=vrep.simxGetObjectHandle(clientID,'ePuck_leftJoint',vrep.simx_opmode_oneshot_wait)
	err,rightMotor=vrep.simxGetObjectHandle(clientID,'ePuck_rightJoint',vrep.simx_opmode_oneshot_wait)
	err,sensor2 = vrep.simxGetObjectHandle(clientID,'ePuck_proxSensor2',vrep.simx_opmode_oneshot_wait)
	err,sensor3 = vrep.simxGetObjectHandle(clientID,'ePuck_proxSensor3',vrep.simx_opmode_oneshot_wait)
	err,sensor4 = vrep.simxGetObjectHandle(clientID,'ePuck_proxSensor4',vrep.simx_opmode_oneshot_wait)
	err,sensor5 = vrep.simxGetObjectHandle(clientID,'ePuck_proxSensor5',vrep.simx_opmode_oneshot_wait)

	first = True

	while True :
		if first :
			dist2=vrep.simxReadProximitySensor(clientID,sensor2,vrep.simx_opmode_streaming)
			dist3=vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_streaming)
			dist4=vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_streaming)
			dist5=vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_streaming)
		else:
			dist2=vrep.simxReadProximitySensor(clientID,sensor2,vrep.simx_opmode_buffer)
			dist3=vrep.simxReadProximitySensor(clientID,sensor3,vrep.simx_opmode_buffer)
			dist4=vrep.simxReadProximitySensor(clientID,sensor4,vrep.simx_opmode_buffer)
			dist5=vrep.simxReadProximitySensor(clientID,sensor5,vrep.simx_opmode_buffer)

		if dist3[1] == True | dist2[1] == True:
			vrep.simxSetJointTargetVelocity(clientID,leftMotor,2,vrep.simx_opmode_oneshot)
			vrep.simxSetJointTargetVelocity(clientID,rightMotor,-2,vrep.simx_opmode_oneshot)
		else:
			#if dist4 == True:
			#	vrep.simxSetJointTargetVelocity(clientID,leftMotor,-1,vrep.simx_opmode_oneshot)
			#	vrep.simxSetJointTargetVelocity(clientID,rightMotor,1,vrep.simx_opmode_oneshot)
			#else:
			vrep.simxSetJointTargetVelocity(clientID,leftMotor,2,vrep.simx_opmode_oneshot)
			vrep.simxSetJointTargetVelocity(clientID,rightMotor,2.1,vrep.simx_opmode_oneshot)



	vrep.simxFinish(clientID)
else:
	print 'Failed connecting to remote API server'
print 'Program ended'

'''

