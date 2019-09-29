import Leap
from Leap import Finger
from constants import pygameWindowWidth, pygameWindowDepth
from pygameWindow_Del03 import PYGAME_WINDOW
import random
import numpy as np
import pickle
import os
import shutil

class DELIVERABLE:
	def __init__(self):
		self.Clear_Directory()
		self.controller = Leap.Controller()
		self.x = 500
		self.y = 400
		self.xMin = 1000.0
		self.xMax = -1000.0
		self.yMin = 1000.0
		self.yMax = -1000.0
		self.previousNumberOfHands = 0
		self.currentNumberOfHands = 0
		self.gestureData = np.zeros((5,4,6),dtype='f')
		self.numGestures = 0
		self.pygameWindow = PYGAME_WINDOW()


	def Clear_Directory(self):
		shutil.rmtree("userData")
		os.mkdir("userData")


	def Scale(self, x, oldMin, oldMax, newMin, newMax):
		if oldMin == oldMax:
			newX = float(newMax - newMin)/2
		else:
			newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)

		return newX


	def Save_Gesture(self):
		pickleOut = open("userData/gesture" + str(self.numGestures) + ".p","wb")
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

		if self.Recording_Is_Ending():
			self.gestureData[i,j,0] = bone.prev_joint[0]
			self.gestureData[i,j,1] = bone.prev_joint[1]
			self.gestureData[i,j,2] = bone.prev_joint[2]
			self.gestureData[i,j,3] = bone.next_joint[0]
			self.gestureData[i,j,4] = bone.next_joint[1]
			self.gestureData[i,j,5] = bone.next_joint[2]

		baseCoords = self.Handle_Vector_From_Leap(base)
		tipCoords = self.Handle_Vector_From_Leap(tip)
		if self.currentNumberOfHands == 1:
			self.pygameWindow.Draw_Line(baseCoords, tipCoords, 4-j, "green")
		else:
			self.pygameWindow.Draw_Line(baseCoords, tipCoords, 4-j, "red")
		

	def Handle_Finger(self, finger, i):
		for j in range(0,4):
			self.Handle_Bone(finger.bone(j), i, j)


	def Handle_Frame(self, frame):
		global x, y, xMin, xMax, yMin, yMax
		hand = frame.hands[0]
		fingers = hand.fingers
		for i in range(0,5):
			self.Handle_Finger(fingers[i], i)
		if self.Recording_Is_Ending():
			print(self.gestureData)
			self.Save_Gesture()

	def Recording_Is_Ending(self):
		if self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2:
			return True


	def Run_Once(self):
		self.pygameWindow.Prepare()
		frame = self.controller.frame()
		if len(frame.hands) > 0:
			self.Handle_Frame(frame)
		self.previousNumberOfHands = self.currentNumberOfHands
		self.currentNumberOfHands = len(frame.hands)
		self.pygameWindow.Reveal()


	def Run_Forever(self):
		while True:
			self.Run_Once()