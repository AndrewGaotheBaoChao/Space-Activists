from pygame import *
from math import *
from random import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

init()
clock = time.Clock() # FPS Clock
currentScreen = "Menu" # Keeps track of which screen the user is on
running = True

class Game:
	def init(self):
		global window, width, height, title
		width, height = 1280, 720
		title = "English Project"
		self.screen = display.set_mode((width, height))

	def start_screen(self):
		self.screen.blit(menu, (0, 0))
		self.screen.blit(newGameB, (389, 349))
		self.screen.blit(helpB, (389, 483))
		self.screen.blit(creditsB, (389, 550))
		display.flip()

	def start_game(self):
		pass

	def events(self):
		pass

g = Game()

while running:

	clock.tick()  # Advances the clock for FPS
	mx, my = mouse.get_pos()  # Mouse location
	mb = mouse.get_pressed()  # Mouse click status
	click = False  # Resets mouse click so that it only counts as one click

	for evt in event.get():
		if evt.type == QUIT:
			running = False
		elif evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False

		# If mouse button is released
		if e.type == MOUSEBUTTONUP and e.button == 1:
			click = True
			print(click)

	if currentScreen == "Menu":
		g.start_screen()

	elif currentScreen == "Game":
		g.start_game()

	display.flip()

quit()