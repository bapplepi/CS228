from pygameWindow import PYGAME_WINDOW
import random

x = 500
y = 400

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

while True:
	Perturb_Circle_Position()
	pygameWindow.Prepare()
	pygameWindow.Draw_Black_Circle(x,y)
	pygameWindow.Reveal()