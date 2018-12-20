from pygame import *
from math import *
from random import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

init()

width, height = 960, 540
screen = display.set_mode((width, height))
running = True

while running:
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		elif evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False

	screen.fill(WHITE)

	display.flip()

quit()