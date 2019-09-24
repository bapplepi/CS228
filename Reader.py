
from pygameWindow_Del03 import PYGAME_WINDOW
import os
import pickle
from constants import pygameWindowWidth, pygameWindowDepth, xMin, xMax, yMin, yMax
import time

class READER:
	def __init__(self):
		self.pygameWindow = PYGAME_WINDOW()
		self.Count_Gestures()

	def Print_Gestures(self, numGestures):
		for i in range(0, numGestures):
			gesture = pickle.load(open("userData/gesture" + str(i) + ".p", "rb"))
			print(gesture.read())

	def Count_Gestures(self):
		path, dirs, files = next(os.walk("userData"))
		self.numGestures = len(files)

	def Scale(self, x, oldMin, oldMax, newMin, newMax):
		if oldMin == oldMax:
			newX = float(newMax - newMin)/2
		else:
			newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)
		return newX

	def Draw_Gesture(self, i):
		global xMin, yMin, xMax, yMax
		self.pygameWindow.Prepare()
		gesture = pickle.load(open("userData/gesture" + str(i) + ".p", "rb"))
		for i in range(0,5):
			for j in range(0,4):
				currentBone = gesture[i,j,:]
				xBaseNotYetScaled = currentBone[0]
				xBase = self.Scale(xBaseNotYetScaled, xMin, xMax, 0, pygameWindowWidth)
				yBaseNotYetScaled = -currentBone[2]
				yBase = self.Scale(yBaseNotYetScaled, yMin, yMax, pygameWindowDepth, 0)
				xTipNotYetScaled = currentBone[3]
				xTip = self.Scale(xTipNotYetScaled, xMin, xMax, 0, pygameWindowWidth)
				yTipNotYetScaled = -currentBone[5]
				yTip = self.Scale(yTipNotYetScaled, yMin, yMax, pygameWindowDepth, 0)
				self.pygameWindow.Draw_Line((xBase, yBase), (xTip, yTip), 2, "blue")
		self.pygameWindow.Reveal()
		time.sleep(0.5)

	def Draw_Each_Gesture_Once(self):
		for i in range(0, self.numGestures):
			self.Draw_Gesture(i)

	def Draw_Gestures(self):
		while True:
			self.Draw_Each_Gesture_Once()