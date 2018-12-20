from pygame import *
from math import *
from random import *
import images
from load import *

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

init()
images.load()
width, height = 1280, 720
screen = display.set_mode((width, height))

clock = time.Clock() # FPS Clock
currentScreen = "menu" # Keeps track of which screen the user is on
running = True
tick = 0

class Game:
	def __init__(self):
		self.title = "English Project"
		display.set_caption(self.title)
		self.player = Player()

		self.offset = [0, 0]

	def update_menu(self):
		pass

	def draw_menu(self):
		screen.fill((50,50,50))
		screen.blit(menu, (0, 0))
		screen.blit(play, (389, 349))
		screen.blit(helpB, (389, 416))
		screen.blit(creditsB, (389, 483))

	def update_game(self):
		self.player.update()

	def draw_game(self):
		screen.fill((50,50,50))
		self.player.draw()

class Player:
	def __init__(self):
		self.index = 0 # keeps track of what image to blit in animation
		self.image = images.playerImages[self.index] # holds actual image for animation
		self.rect = self.image.get_rect()
		self.rect.center = width/2, height/2
		self.x, self.y = self.rect.midbottom
		self.dir = 'down'

		self.vx, self.vy = 0, 0

	def determine_image(self):
		if self.dir in ['up', 'down']:
			if self.vy > 0:
				self.index = 0
			elif self.vy < 0:
				self.index = 4
		elif self.dir in ['right', 'left']:
			if self.vx > 0:
				self.index = 12
			elif self.vx < 0:
				self.index = 8

		if self.vx == self.vy == 0:
			d = ['down','up','left','right']
			i = d.index(self.dir) * 4
			if i == 12: i+=1
			self.image = images.playerImages[i]
		else:
			self.image = images.playerImages[self.index + (int(tick/5) % 4)]

	def update(self):
		self.vx , self.vy = 0, 0
		kp = key.get_pressed()
		if kp[K_RIGHT] or kp[K_d]:
			self.dir = 'right'
			self.vx = 5
		if kp[K_LEFT] or kp[K_a]:
			self.dir = 'left'
			self.vx = -5
		if kp[K_DOWN] or kp[K_s]:
			self.dir = 'down'
			self.vy = 5
		if kp[K_UP] or kp[K_w]:
			self.dir = 'up'
			self.vy = -5

		self.determine_image()

	def draw(self):
		screen.blit(self.image, self.rect)

g = Game()

while running:
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
		if evt.type == MOUSEBUTTONUP:
			if evt.button == 1:
				click = True
				print(click)

	if currentScreen == "menu": # When user is on main menu screen
		g.update_menu()
		g.draw_menu()

		if playR.collidepoint(mx, my): # Checks mouse collision with button
			draw.rect(screen, WHITE, playR, 2)

		if helpR.collidepoint(mx, my):
			draw.rect(screen, WHITE, helpR, 2)

		if creditsR.collidepoint(mx, my):
			draw.rect(screen, WHITE, creditsR, 2)

	elif currentScreen == "game":
		g.update_game()
		g.draw_game()

	display.flip()
	clock.tick(60) # FPS
	tick = (tick + 1) % (60*120)

quit()