import random
from math import sqrt

def sphere_controller(frequency, pos_robot):
	# Computes the next toy position depending on the robot fractions
	# returns [x, y ,z] coordinates of the toy
	# action = [motorLeft, motorRight, frequency]
	if frequency >= 0 and frequency <= 0.33:
		# toy moves randomly inside the map
		# Map is 10x10 ... (depends on the map used)
		return generate_random_position(10,10,pos_robot,0.5)
	elif frequency > 0.33 and frequency <= 0.66:
		# stops moving
		return 0
	elif frequency > 0.66 and frequency <= 1:
		# toy jumps on robot position (y axis is vertical axis)
		return [pos_robot[0], 0.5 , pos_robot[1]]
	else:
		# frequency out of widthband
		return 0

def generate_random_position(max_width, max_length, pos_robot, radius):
	while True:
		generated_pos=[random.uniform(0,max_width), 0.5, random.uniform(0,max_length)]
		if(isCollision(generated_pos, pos_robot, radius) == False):
			return generated_pos

def isCollision(generated_pos, pos_robot, radius):
	if sqrt((generated_pos[0] - pos_robot[0])**2 + (generated_pos[2] - pos_robot[1])**2) <= radius:
		return True
	else:
		return False

def unitTest():
	frequency = 0.1
	output = sphere_controller(frequency, [1.5,0.5,2.5]);
	print "frequency :", frequency, ", robot position : ", [1.5,0.5,2.5]
	print "output is", output
	return
