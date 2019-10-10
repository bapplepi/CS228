import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../LeapSDK/lib/')
import pickle
import Leap
import numpy as np
from Leap import Finger
from constants import pygameWindowWidth, pygameWindowDepth

controller = Leap.Controller()

from pygameWindow import PYGAME_WINDOW
import random

x = 500
y = 400
xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

pygameWindow = PYGAME_WINDOW()

clf = pickle.load( open('userData/classifier.p','rb') )
testData = np.zeros((1,30),dtype='f')

def CenterData(testData):
	xTotal = 0.0
	yTotal = 0.0
	zTotal = 0.0
	for i in range(0,10):
		xTotal = xTotal + testData[0,i]
		yTotal = yTotal + testData[0,i+1]
		zTotal = zTotal + testData[0,i+2]
	xTotal = xTotal/10.0
	yTotal = yTotal/10.0
	zTotal = zTotal/10.0
	for i in range(0,10):
		testData[0,i] = testData[0,i] - xTotal
		testData[0,i+1] = testData[0,i+1] - yTotal
		testData[0,i+2] = testData[0,i+2] - zTotal



def Scale(x, oldMin, oldMax, newMin, newMax):
	if oldMin == oldMax:
		newX = float(newMax - newMin)/2
	else:
		newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)

	return newX

def Handle_Vector_From_Leap(v):
	global xMin,xMax,yMin,yMax
	vX = int(v[0])
	vY = int(v[1])

	if vX < xMin:
		xMin = vX
	elif vX > xMax:
		xMax = vX
	if vY < yMin:
		yMin = vY
	elif vY > yMax:
		yMax = vY

	pygameX = Scale(vX, xMin, xMax, 0, pygameWindowWidth)
	pygameY = Scale(vY, yMin, yMax, pygameWindowDepth, 0)
		
	return (pygameX,pygameY)


def Handle_Bone(bone, b):
	global k, testData
	base = bone.prev_joint
	tip = bone.next_joint
	baseCoords = Handle_Vector_From_Leap(base)
	tipCoords = Handle_Vector_From_Leap(tip)
	if((b==0) or (b==3)):
		#print "+ 3"
		testData[0,k] = tip[0]
		testData[0,k+1] = tip[1]
		testData[0,k+2] = tip[2]
		k = k + 3
	pygameWindow.Draw_Black_Line(baseCoords, tipCoords, 4-b)

def Handle_Finger(finger):
	for b in range(0,4):
		#print "for bone " + str(b)
		Handle_Bone(finger.bone(b), b)

def Handle_Frame(frame):
	global x, y, xMin, xMax, yMin, yMax
	hand = frame.hands[0]
	fingers = hand.fingers
	for finger in fingers:
		#print "for finger " + str(finger)
		Handle_Finger(finger)

k = 0

def loop():
	global k
	pygameWindow.Prepare()
	frame = controller.frame()
	if len(frame.hands) > 0:
		k = 0
		Handle_Frame(frame)
		CenterData(testData)
		predictedClass = clf.Predict(testData)
		print(predictedClass)
	pygameWindow.Reveal()


while True:
	loop()