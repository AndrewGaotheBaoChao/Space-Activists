from pygame import *
from math import *
from random import *
from resource import *
from tilemap import *
from settings import *
import sys

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

sys.stderr = open('errorlog.txt', 'w') # making a txt file to record all errors
init()
screen = display.set_mode((width, height))

clock = time.Clock() # FPS Clock
currentScreen = "menu" # Keeps track of which screen the user is on
running = True
tick = 0 # Global game tick

class Game:
	def __init__(self):
		# Setup
		self.title = "English Project"
		display.set_caption(self.title)
		self.load_files()
		self.player = Player(self)

		# Game Stuff
		self.walls = []

	def load_files(self):
		self.map = TiledMap("level/map.tmx") 
		self.camera = Camera(self.map.width, self.map.height)
		self.npcs = []

		for n in self.map.npcs:
			self.npcs.append(NPC(n[0], n[1], n[2]))

	def update_menu(self):
		pass

	def draw_menu(self):
		screen.blit(menu, (0, 0))
		screen.blit(playB, (389, 349))
		screen.blit(helpB, (389, 416))
		screen.blit(creditsB, (389, 483))

	def draw_help(self):
		screen.blit(helpS, (0, 0))
		screen.blit(backB, (650, 483))

	def draw_credits(self):
		screen.blit(creditsS, (0, 0))
		screen.blit(backB, (650, 483))

	def update_pause(self):
		pass

	def draw_pause(self):
		screen.fill((100,100,100))
		p = fonts[1].render("Paused", True, WHITE)
		pr = p.get_rect()
		pr.center = width/2, height/2
		screen.blit(p, pr)

	def update_game(self):
		self.player.update()
		self.camera.update(self.player)

	def draw_game(self):
		screen.fill((50,50,50))
		mapimg = self.map.make_map(self.camera.camera)
		maprect = mapimg.get_rect()
		screen.blit(mapimg, self.camera.apply_rect(maprect))
		for n in self.npcs:
			x, y = n.rect.topleft
			x += self.camera.camera.x
			y += self.camera.camera.y
			screen.blit(n.image, (x, y))
		screen.blit(self.player.image, self.camera.apply(self.player))
		for w in self.map.walls:
			draw.rect(screen, BLACK, self.camera.apply_rect(w), 1)

class Player:
	def __init__(self, g):
		self.index = 0 # keeps track of what image to blit in animation
		self.images = playerImages
		self.image = self.images[self.index] # holds actual image for animation
		self.rect = self.image.get_rect()
		self.rect.center = g.map.player_spawn
		self.dir = "down"
		self.x, self.y = g.map.player_spawn
		self.vx, self.vy = 0, 0

	def determine_image(self):
		if self.dir in ["up", "down"]:
			if self.vy > 0:
				self.index = 0
			elif self.vy < 0:
				self.index = 4
		elif self.dir in ["right", "left"]:
			if self.vx > 0:
				self.index = 12
			elif self.vx < 0:
				self.index = 8

		if self.vx == self.vy == 0:
			d = ["down","up","left","right"]
			i = d.index(self.dir) * 4
			if i == 12: i+=1
			self.image = self.images[i]
		else:
			self.image = self.images[self.index + (int(tick/5) % 4)]

	def update(self):
		self.vx, self.vy = 0, 0
		kp = key.get_pressed()
		if kp[K_LSHIFT]: s = 16
		else: s = 8

		if kp[K_RIGHT] or kp[K_d]:
			self.dir = "right"
			self.vx = s
		elif kp[K_LEFT] or kp[K_a]:
			self.dir = "left"
			self.vx = -s
		elif kp[K_DOWN] or kp[K_s]:
			self.dir = "down"
			self.vy = s
		elif kp[K_UP] or kp[K_w]:
			self.dir = "up"
			self.vy = -s

		self.x += self.vx
		self.y += self.vy
		self.rect.center = self.x, self.y

		### COLLISIONS ###
		for w in g.map.walls:
			if self.rect.colliderect(w):
				if abs(self.vx) != 0:
					if self.vx > 0:
						self.rect.right = w[0]
					else:
						self.rect.left = w[0] + w[2]
					self.x = self.rect.centerx
				if abs(self.vy) != 0:
					if self.vy > 0:
						self.rect.bottom = w[1]
					else:
						self.rect.top = w[1] + w[3]
					self.y = self.rect.centery

		self.determine_image()

	def draw(self):
		screen.blit(self.image, self.rect)

class NPC:
	def __init__(self, x, y, t):
		# Get the right skins for the type (t)
		self.images = npcImages[t]
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.center = x, y

	def update(self):
		# Rotate towards the player
		pass

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
				if currentScreen == "menu": running = False
				elif currentScreen == "pause": running = False
				elif currentScreen == "game": currentScreen = "pause"
			if evt.key == K_SPACE:
				if currentScreen == "pause": currentScreen = "game"

		elif evt.type == KEYUP:
			pass

		# If mouse button is released
		if evt.type == MOUSEBUTTONUP:
			if evt.button == 1:
				click = True

	if currentScreen == "menu": # When user is on main menu screen
		g.update_menu()
		g.draw_menu()

		if playR.collidepoint(mx, my): # Checks mouse collision with button
			draw.rect(screen, WHITE, playR, 2)

			if click:
				currentScreen = "game"

		if helpR.collidepoint(mx, my):
			if click:
				currentScreen = "help"
			draw.rect(screen, WHITE, helpR, 2)

		if creditsR.collidepoint(mx, my):
			if click:
				currentScreen = "credits"
			draw.rect(screen, WHITE, creditsR, 2)

	elif currentScreen == "help":
		g.draw_help()
		if backR.collidepoint(mx, my):
			draw.rect(screen, WHITE, backR, 2)
			if click:
				currentScreen = "menu"

	elif currentScreen == "credits":
		g.draw_credits()
		if backR.collidepoint(mx, my):
			draw.rect(screen, WHITE, backR, 2)
			if click:
				currentScreen = "menu"

	elif currentScreen == "pause":
		g.update_pause()
		g.draw_pause()

	elif currentScreen == "game":
		g.update_game()
		g.draw_game()

	display.flip()
	clock.tick(60) # FPS
	tick = (tick + 1) % (60*120) # global game tick counter, resetting after 120 seconds

sys.stderr.close()
sys.stderr = sys.__stderr__
quit()
