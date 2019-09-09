import sys
sys.path.insert(0, '../LeapSDK/lib/')
import Leap
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

print(pygameWindow)

def Perturb_Circle_Position():
	global x, y
	fourSidedDieRoll = random.randint(1, 4)
	if fourSidedDieRoll == 1:
		x -= 1
	elif fourSidedDieRoll == 2:
		x += 1
	elif fourSidedDieRoll == 3:
		y -= 1
	else:
		y += 1

def Scale(x, oldMin, oldMax, newMin, newMax):
	if oldMin == oldMax:
		newX = float(newMax - newMin)/2
	else:
		newX = float(newMin) + float(newMax - newMin) * float(x - oldMin)/float(oldMax - oldMin)


	return newX

def Handle_Frame(frame):
	global x, y, xMin, xMax, yMin, yMax
	hand = frame.hands[0]
	fingers = hand.fingers
	indexFingerList = fingers.finger_type(Finger.TYPE_INDEX)
	indexFinger = indexFingerList[0]
	distalPhalanx = indexFinger.bone(3)
	tip = distalPhalanx.next_joint
	x = int(tip[0])
	y = int(tip[1])
	if x < xMin:
		xMin = x
	elif x > xMax:
		xMax = x
	if y < yMin:
		yMin = y
	elif y > yMax:
		yMax = y

while True:
	pygameWindow.Prepare()
	frame = controller.frame()
	if len(frame.hands) > 0:
		Handle_Frame(frame)
		pygameX = Scale(x, xMin, xMax, 0, pygameWindowWidth)
		pygameY = Scale(y, yMin, yMax, pygameWindowDepth, 0)
		pygameWindow.Draw_Black_Circle(int(pygameX), int(pygameY))
	pygameWindow.Reveal()
	"""Perturb_Circle_Position()
	pygameWindow.Draw_Black_Circle(x,y)"""