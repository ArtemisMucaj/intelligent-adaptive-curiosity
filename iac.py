# Implementation algorithme IAC
# vrep api utilities
import vrep
# iac utilities
import kppv
import tree
import toy
import utilities
# math utilities
import random
from math import sqrt
import time
# Plotter
import matplotlib.pyplot as plt

t=0
delay = 150
nbExemple = 20
duree = 1000 #1500
c1 = 300
varKppv = 10
vitRobot = 1

# Start IAC
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)

err_epuck, epuckHandle = vrep.simxGetObjectHandle(clientID,"ePuck", vrep.simx_opmode_oneshot_wait)
err_toy, toyHandle = vrep.simxGetObjectHandle(clientID,"Sphere", vrep.simx_opmode_oneshot_wait)
err_left,leftHandle = vrep.simxGetObjectHandle(clientID,"ePuck_leftJoint",vrep.simx_opmode_oneshot_wait)
err_right,rightHandle = vrep.simxGetObjectHandle(clientID,"ePuck_rightJoint",vrep.simx_opmode_oneshot_wait)

# Prediction machine P (arbre d'experts) qui apprends a predire la
# distance au jouet
Pbdd = tree.node(-1,-1,[],None,None,[],[])
# Meta learning machine (apprends a predire l'erreure)
MPbdd = []
S_calculated = 0

# Debut de la simulation
while t < duree:
	# Vecteur d'actions possibles
	actions = []
	if t==0:
		err,epuck_position = vrep.simxGetObjectPosition(clientID, epuckHandle, -1, vrep.simx_opmode_streaming)
	else:
		err,epuck_position = vrep.simxGetObjectPosition(clientID, epuckHandle, -1, vrep.simx_opmode_buffer)
		pass

	# Creation des actions aleatoires
	for i in range(0,nbExemple):
		actions.append( [random.uniform(-vitRobot,vitRobot) , random.uniform(-vitRobot,vitRobot) , random.uniform(0,1), S_calculated] )
		pass

	if t<delay:
		# Action random
		actionChoisie = actions[0]
		pass
	else:
		#Calcul du learning progress LPi pour chaque action
		# Ep = erreur de prediction de la learning machine P
		Ep = []
		# Erreure moyenne de l'expert associe a l'action
		Emtplusun = []
		LP = []
		# Calcul de LP pour chaque action aleatoire tiree
		for x in range(0,nbExemple):
			# Prediction de l'erreur de prediction de la meta learning-machine MP
			Ep.append( kppv.kppv(actions[x], MPbdd,varKppv) ) #### probleme de taille entre actions[x] et la base de MPbdd
			# Calcul de la moyenne Em(t+1)
			Emtplusun.append(utilities.moyenneMobile(utilities.getTheGoodLE(Pbdd,actions[x]),Ep[x],delay) )
			# Calcul de LP
			LP.append( [-(Emtplusun[x] - utilities.getTheGoodLEM(Pbdd,delay,actions[x]) ) , x] )
			pass
		# Tri du tableau contenant les LPi
		LP.sort()
		# 10% de chances de realiser une action random
		if random.randint(0,100)<10:
			#Action random
			actionChoisie = actions[0]
			pass
		else:
			# Selection de l'action ayant le LP le plus eleve
			actionChoisie = actions[LP[len(LP)-1][1]]
			pass
		pass

	#On a choisi l'action
	# Estimation de S(t+1) avec la learning machine P
	# Choix de l'expert associe a l'action choisie
	T= utilities.getTheGoodTree(Pbdd,actionChoisie)

	if len(T.data) > varKppv:
		S_predicted = kppv.kppv(actionChoisie,T.data,varKppv)
	else:
		S_predicted = 0
		pass

	# On realise l'action dans VREP
	vrep.simxSetJointTargetVelocity(clientID,leftHandle,actionChoisie[0],vrep.simx_opmode_oneshot)
	vrep.simxSetJointTargetVelocity(clientID,rightHandle,actionChoisie[1],vrep.simx_opmode_oneshot)
	vec = toy.toy_controller(actionChoisie[2],epuck_position)

	if isinstance(vec,type([])) and len(vec)!=0:
		vrep.simxSetObjectPosition(clientID,toyHandle,-1,vec,vrep.simx_opmode_oneshot)
		pass

	# On calcule E(t)
	if t ==0:
		err_toy, toyPosition = vrep.simxGetObjectPosition(clientID,toyHandle, -1, vrep.simx_opmode_streaming)
	else:
		err_toy, toyPosition = vrep.simxGetObjectPosition(clientID,toyHandle, -1, vrep.simx_opmode_buffer)

	# Calcul de l'erreur de prediction
	S_calculated = sqrt((epuck_position[0] - toyPosition[0])**2 + (epuck_position[1] - toyPosition[1])**2)
	E = abs(S_predicted - S_calculated)

	# Ajout a la base de donnees de MP
	#    Retires S(t) du vecteur actionChoisie
	actionChoisie.pop()
	#    Ajoutes l'erreur de prediction
	actionChoisie.append(E)
	MPbdd.append( actionChoisie )

	#print 'f =',actionChoisie[2],'S_calculated =',S_calculated###################################

	# On ajoute E(t) a LE (liste d'erreures de l'expert associe)
	T.LE.append(E)
	# On calcul Em(t) et ajout a LEM (liste des moyennes d'erreures)
	if t>delay:
		Em = utilities.moyenneMobile(T.LE,0,delay)
	else:
		Em = utilities.moyenneMobile(T.LE,0,t)
	T.LEM.append(Em)

	# Ajout dans la base de donnees de P
	actionChoisie.pop()
	actionChoisie.append(S_calculated)
	T.data.append(actionChoisie)

	# Separation pour creer deux experts
	utilities.splitBDD(T,c1)

	print 't =',t #
	t+=1
	#time.sleep(1)
	pass

if 1:
	print 'Try me'
	pass
# Stops robot
vrep.simxSetJointTargetVelocity(clientID,leftHandle,0,vrep.simx_opmode_oneshot)
vrep.simxSetJointTargetVelocity(clientID,rightHandle,0,vrep.simx_opmode_oneshot)

# Affichage de l'arbre d'experts
tree.status(Pbdd,0)  ###########
# Affichage de la moyenne d'erreur par expert
utilities.superPlot(Pbdd)
plt.show()

# Fin de la simulation
vrep.simxFinish(clientID)



