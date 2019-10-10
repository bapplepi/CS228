import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../../LeapSDK/lib/')

import Leap
from Leap import Finger
from constants import pygameWindowWidth, pygameWindowDepth
from pygameWindow_Del03 import PYGAME_WINDOW
import random
import numpy as np
import pickle
import os
import shutil

class RECORDER:
	def __init__(self):
		self.controller = Leap.Controller()
		self.clf = pickle.load( open('userData/classifier.p','rb') )
		self.x = 500
		self.y = 400
		self.xMin = 1000.0
		self.xMax = -1000.0
		self.yMin = 1000.0
		self.yMax = -1000.0
		self.numberOfGestures = 1000
		self.gestureIndex = 0
		self.previousNumberOfHands = 0
		self.currentNumberOfHands = 0
		self.gestureData = np.zeros((5,4,6,self.numberOfGestures),dtype='f')
		self.numGestures = 0
		self.k = 0
		self.pygameWindow = PYGAME_WINDOW()
		self.testData = np.zeros((1,30),dtype='f')


	def CenterData(self):
		allXCoordinates = self.testData[0,::3]
		meanValue = allXCoordinates.mean()
		self.testData[0,::3] = allXCoordinates - meanValue

		allYCoordinates = self.testData[0,1::3]
		meanValue = allYCoordinates.mean()
		self.testData[0,1::3] = allYCoordinates - meanValue

		allZCoordinates = self.testData[0,2::3]
		meanValue = allZCoordinates.mean()
		self.testData[0,2::3] = allZCoordinates - meanValue

			#print "centered coordinates: " + str(self.testData[0,i]) + ", " + str(self.testData[0,i+1]) + ", " + str(self.testData[0,i+2])


	def Scale(self, x, oldMin, oldMax, newMin, newMax):
		if oldMin == oldMax:
			newX = float(newMax - newMin)/2
		else:
			newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)

		return newX


	def Save_Gesture(self):
		pickleOut = open("userData/gesture.p","wb")
		pickle.dump(self.gestureData, pickleOut)
		pickleOut.close()
		self.numGestures += 1


	def Handle_Vector_From_Leap(self, v):
		global xMin,xMax,yMin,yMax
		vX = int(v[0])
		vY = -int(v[2])

		if vX < self.xMin:
			self.xMin = vX
		elif vX > self.xMax:
			self.xMax = vX
		if vY < self.yMin:
			self.yMin = vY
		elif vY > self.yMax:
			self.yMax = vY

		pygameX = self.Scale(vX, self.xMin, self.xMax, 0, pygameWindowWidth)
		pygameY = self.Scale(vY, self.yMin, self.yMax, pygameWindowDepth, 0)
			
		return (pygameX,pygameY)


	def Handle_Bone(self, bone, i, j):
		base = bone.prev_joint
		tip = bone.next_joint

		baseCoords = self.Handle_Vector_From_Leap(base)
		tipCoords = self.Handle_Vector_From_Leap(tip)
		if((j==0) or (j==3)):
			#print "+ 3"
			self.testData[0,self.k] = tip[0]
			self.testData[0,self.k+1] = tip[1]
			self.testData[0,self.k+2] = tip[2]
			self.k = self.k + 3

		if self.currentNumberOfHands == 1:
			self.pygameWindow.Draw_Line(baseCoords, tipCoords, 4-j, "green")
		

	def Handle_Finger(self, finger, i):
		for j in range(0,4):
			self.Handle_Bone(finger.bone(j), i, j)


	def Handle_Frame(self, frame):
		global x, y, xMin, xMax, yMin, yMax
		hand = frame.hands[0]
		fingers = hand.fingers
		for i in range(0,5):
			self.Handle_Finger(fingers[i], i)


	def Recording_Is_Ending(self):
		if self.currentNumberOfHands == 2:
			return True


	def Run_Once(self):
		self.pygameWindow.Prepare()
		frame = self.controller.frame()
		if len(frame.hands) > 0:
			self.Handle_Frame(frame)
			self.CenterData()
			predictedClass = self.clf.Predict(self.testData)
			print(predictedClass)
		self.k = 0
		self.currentNumberOfHands = len(frame.hands)
		self.pygameWindow.Reveal()


	def Run_Forever(self):

		while True:
			self.Run_Once()