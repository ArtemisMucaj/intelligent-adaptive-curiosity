#Super programme python
import vrep
import kppv
import tree
import random

print("Salut je suis un programme Python !\n")


def moyenneMobile(list,x_n,delay,t):
	moy = x_n
	for i in range(1,delay+1):
		moy += list[t-i]
		pass
	moy /= delay + 1
	return moy


vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)



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

while True:

	actions = []

	err,epuck_position = vrep.simxGetObjectPosition(clientID, epuckHandle, -1, vrep.simx_opmode_streaming)
	#creation des actions
	for i in range(0,nbExemple):
		########### add SM(t) a actions ###############
		actions.append( [random.uniform(-5,5) , random.uniform(-5,5) , random.uniform(0,1),epuck_position[0],epuck_position[1] ] )
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

			Ep.append( kppv.kppv([actions[x], MPbdd,1]) ) #### probleme de taille entre actions[x] et la base de MPbdd
			########## a faire ################
			Emtplusun.append( moyenneMobile(getTheGoodLE(Pbdd),Ep[x],delay,t) )

			########## a faire ################
			LP.append( [-(Emtplusun[x] - getTheGoodLEM(Pbdd,t-delay) ) , x] )
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

	########## Estimation de S(t+1) ###############

	# On realise l'action
	vrep.simxSetJointTargetVelocity(clientID,leftHandle,actionChoisie[0],vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID,rightHandle,actionChoisie[1],vrep.simx_opmode_oneshot)
	vec = sphere.sphere_controller(actionChoisie[2],epuck_position)

	if len(vec)!=0:
		vrep.simxSetObjectPosition(clientID,sphereHandle,-1,vec,vrep.simx_opmode_oneshot)
		pass

	######### On calcule E(t) ############

	#ajout a la base de donnees de MP
	actionChoisie.append(E)
	MPbdd.append( actionChoisie )

	######### On ajoute E(t) a LE ##########

	######## On calcul Em(t) et ajout a LEM #########

	####### ajout dans la base de donnees de P ###########
	pass


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
