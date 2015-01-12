# Copyright 2006-2014 Coppelia Robotics GmbH. All rights reserved. 
# marc@coppeliarobotics.com
# www.coppeliarobotics.com
# 
# -------------------------------------------------------------------
# THIS FILE IS DISTRIBUTED "AS IS", WITHOUT ANY EXPRESS OR IMPLIED
# WARRANTY. THE USER WILL USE IT AT HIS/HER OWN RISK. THE ORIGINAL
# AUTHORS AND COPPELIA ROBOTICS GMBH WILL NOT BE LIABLE FOR DATA LOSS,
# DAMAGES, LOSS OF PROFITS OR ANY OTHER KIND OF LOSS WHILE USING OR
# MISUSING THIS SOFTWARE.
# 
# You are free to use/modify/distribute this file for whatever purpose!
# -------------------------------------------------------------------
#
# This file was automatically created for V-REP release V3.1.3 on Sept. 30th 2014

# Make sure to have the server side running in V-REP: 
# in a child script of a V-REP scene, add following command
# to be executed just once, at simulation start:
#
# simExtRemoteApiStart(19999)
#
# then start simulation, and run this program.
#
# IMPORTANT: for each successful call to simxStart, there
# should be a corresponding call to simxFinish at the end!

import vrep
import vrepConst

print 'IAC Algorithm'
vrep.simxFinish(-1) # just in case, close all opened connections
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5)
if clientID!=-1:
	print 'Connected to remote API server'
	res,objs=vrep.simxGetObjects(clientID,vrep.sim_handle_all,vrep.simx_opmode_oneshot_wait)
	if res==vrep.simx_return_ok:
		print 'Number of objects in the scene: ',len(objs)
	else:
		print 'Remote API function call returned with error code: ',res
	err_world, worldHandle = vrep.simxGetObjectHandle(clientID,"world", vrep.simx_opmode_oneshot_wait)
	err_epuck, epuckHandle = vrep.simxGetObjectHandle(clientID,"ePuck", vrep.simx_opmode_oneshot_wait)
	err_sphere, sphereHandle = vrep.simxGetObjectHandle(clientID,"Sphere", vrep.simx_opmode_oneshot_wait)
	err_left,leftHandle = vrep.simxGetObjectHandle(clientID,"ePuck_leftJoint",vrep.simx_opmode_oneshot_wait)
	err_right,rightHandle = vrep.simxGetObjectHandle(clientID,"ePuck_rightJoint",vrep.simx_opmode_oneshot_wait)
	# Get ePuck position relative to ref_handle object
	#err,epuck_position = simxGetObjectPosition(clientID, epuckHandle, epuckHandle, vrep.simx_opmode_buffer)
	# Non reconnu ...

	while True:
		vrep.simxSetJointTargetVelocity(clientID,leftHandle,0,vrep.simx_opmode_oneshot)
		vrep.simxSetJointTargetVelocity(clientID,rightHandle,0,vrep.simx_opmode_oneshot)
		# Sets Sphere position to ePuck's position ...
		vrep.simxSetObjectPosition(clientID,sphereHandle,epuckHandle,[0.0,0.0,0.1],vrep.simx_opmode_oneshot)
	vrep.simxFinish(clientID)
else:
	print 'Failed connecting to remote API server'
print 'Program ended'
