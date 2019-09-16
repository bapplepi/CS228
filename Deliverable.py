import Leap
from Leap import Finger
from constants import pygameWindowWidth, pygameWindowDepth
from pygameWindow_Del03 import PYGAME_WINDOW
import random

class DELIVERABLE:
	def __init__(self):
		self.controller = Leap.Controller()
		self.x = 500
		self.y = 400
		self.xMin = 1000.0
		self.xMax = -1000.0
		self.yMin = 1000.0
		self.yMax = -1000.0
		self.pygameWindow = PYGAME_WINDOW()


	def Scale(self, x, oldMin, oldMax, newMin, newMax):
		if oldMin == oldMax:
			newX = float(newMax - newMin)/2
		else:
			newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)

		return newX


	def Handle_Vector_From_Leap(self, v):
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


	def Handle_Bone(self, bone, b):
		base = bone.prev_joint
		tip = bone.next_joint
		baseCoords = Handle_Vector_From_Leap(base)
		tipCoords = Handle_Vector_From_Leap(tip)
		pygameWindow.Draw_Black_Line(baseCoords, tipCoords, 4-b)


	def Handle_Finger(self, finger):
		for b in range(0,3):
			Handle_Bone(finger.bone(b), b)


	def Handle_Frame(self, frame):
		global x, y, xMin, xMax, yMin, yMax
		hand = frame.hands[0]
		fingers = hand.fingers
		for finger in fingers:
			Handle_Finger(finger)


	def Run_Once(self):
		self.pygameWindow.Prepare()
		frame = self.controller.frame()
		if len(frame.hands) > 0:
			Handle_Frame(frame)
		self.pygameWindow.Reveal()

	def Run_Forever(self):
		while True:
			Run_Once(self)