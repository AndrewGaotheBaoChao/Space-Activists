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
screen_copy = screen.copy()

clock = time.Clock() # FPS Clock
currentScreen = "menu" # Keeps track of which screen the user is on
running = True
tick = 0 # Global game tick

class Game:
	def __init__(self):
		# Setup
		self.title = "English Project"
		display.set_caption(self.title)
		self.load_files("level/map.tmx")

	def load_files(self, map_file):
		self.map = TiledMap(map_file)
		self.camera = Camera(self.map.width, self.map.height)
		self.npcs = []
		self.walls = []
		self.portals = []

		for n in self.map.npcs:
			self.npcs.append(NPC(n))
		for p in self.map.portals:
			self.portals.append(Portal(p))
		self.player = Player(self)

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
		if not self.player.talking:
			for n in self.npcs:
				n.update(self)
			self.camera.update(self.player, self.map.small)

	def draw_game(self):
		screen.fill((50,50,50))
		if self.player.talking and self.player.talking_to != None:
			screen.blit(self.player.background, (0, 0))
			self.player.talking_to.talk()
			# draw.rect(screen, GREEN, self.camera.apply_rect(self.player.talking_to.rect), 5)
		else:
			r = Rect(-(self.camera.camera.x), -(self.camera.camera.y), width, height)
			mapimg = self.map.make_map(r)
			maprect = mapimg.get_rect()
			screen.blit(mapimg, self.camera.apply_rect(maprect))
			for n in self.npcs:
				screen.blit(n.image, self.camera.apply_rect(n.rect))
			# for p in self.portals:
			# 	draw.rect(screen, BLUE, self.camera.apply_rect(p.rect), 2)

			screen.blit(self.player.image, self.camera.apply(self.player))
			# for w in self.map.walls:
			# 	draw.rect(screen, BLACK, self.camera.apply_rect(w), 1)

class Player:
	def __init__(self, g):
		self.index = 0 # keeps track of what image to blit in animation
		self.images = playerImages
		self.image = self.images[self.index] # holds actual image for animation
		self.rect = self.image.get_rect()
		self.rect.center = g.map.player_spawn
		self.dir = "down"
		self.mode = "moving"
		self.x, self.y = g.map.player_spawn
		self.vx, self.vy = 0, 0
		self.talking = False
		self.talking_to = None

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

		if not self.talking:
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
		if not self.talking:
			for n in g.npcs:
				if self.rect.colliderect(n.rect) and interact:
					self.background = screen_copy
					self.talking = True
					self.talking_to = n
			for p in g.portals:
				if self.rect.colliderect(p.rect):
					g.load_files(p.path)
					if p.co:
						g.player.x = p.co[0]
						g.player.y = p.co[1]

		self.determine_image()

	def draw(self):
		screen.blit(self.image, self.rect)

class NPC:
	def __init__(self, obj):
		# Get the right skins for the type (t)
		self.images = npcImages[int(obj.type)]
		self.image = self.images[0]
		self.rect = self.image.get_rect()
		self.rect.center = obj.x, obj.y

		# Just in case we forget to add npc_name in map file
		try: self.name = obj.npc_name
		except: self.name = "UNKNOWN"

		try: self.dialogue = obj.dialogue.split(" # ")
		except: self.dialogue = []

		for i in range(len(self.dialogue)):
			if self.dialogue[i][0] == "\\":
				self.dialogue[i] = "ME: " + self.dialogue[i][1:]
			else:
				self.dialogue[i] = self.name.upper() + ": " + self.dialogue[i]
		self.index = 0
		self.page = 0
		self.delay = 0
		self.delayMax = 2
		self.dir = "down"

	def update(self, g):
		dx = g.player.rect.centerx - self.rect.centerx
		dy = g.player.rect.centery - self.rect.centery
		ang = degrees(atan2(dy, dx))
		if ang < 0: ang += 360
		if 45 <= ang < 135:
			self.dir = "down"
		elif 135 <= ang < 225:
			self.dir = "left"
		elif 225 <= ang < 315:
			self.dir = "up"
		else:
			self.dir = "right"
		self.image = self.images["down up left right".split(" ").index(self.dir)]

	def talk(self):
		if not self.dialogue:
			g.player.talking = False
			return

		# Continue scrolling as there us still text to be revealed
		if self.index < len(self.dialogue[self.page]) - 1:
			self.delay += 1

		# If user clicks space
		if advance:
			# if there is still text to be revealed, reveal if all
			if self.index < len(self.dialogue[self.page]) - 1:
				self.index = len(self.dialogue[self.page]) - 1
			# otherwise, go to next page / exit if last page
			else:
				self.delay, self.index = 0, 0
				if self.page < len(self.dialogue) - 1:
					self.page += 1
				else:
					self.page = 0
					g.player.talking = False
					return
		if self.delay >= self.delayMax:
			self.delay = 0
			self.index += 1

		# the text so far (srolled)
		txt = self.dialogue[self.page][0:self.index+1]
		# width for the speech box at the bottom of the screen
		w = width-100
		# Speech box
		boxR = Rect((width-w)/2, height - 200, w, 190)

		# Drawing the box
		screen.blit(textbox, (0, 0))

		pos = boxR.x + 20, boxR.y + 20
		text_render = mul_lines(fonts[1], txt, w - 40, align="left")
		screen.blit(text_render, pos)

		# If the page is done
		if self.index >= len(self.dialogue[self.page]) - 1:
			if (tick%20) / 10 < 1:
				i = fonts[1].render("-->", True, BLACK)
				r = i.get_rect()
				r.bottomright = boxR.right - 20, boxR.bottom - 20
				screen.blit(i, r)

class Portal:
	def __init__(self, obj):
		self.rect = Rect(obj.x, obj.y, obj.width, obj.height)
		self.path = "level/" + obj.location + ".tmx"
		try:
			self.co = obj.co.split(",")
			self.co = [int(self.co[0]), int(self.co[1])]
		except: self.co = []
interact = False
click = False
advance = False
g = Game()

introText = "One night, you go to sleep, thinking it's just a normal night # You wake up the next morning, realising something is wrong # So you go outside...".split(" # ")
introCounter = 0

while running:
	mx, my = mouse.get_pos()  # Mouse location
	mb = mouse.get_pressed()  # Mouse click status
	click = False  # Resets mouse click so that it only counts as one click
	interact = False
	advance = False

	for evt in event.get():
		if evt.type == QUIT:
			running = False
		
		elif evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				if currentScreen in ["menu", "intro"]: running = False
				elif currentScreen == "pause": currentScreen = "game"
				elif currentScreen == "game": currentScreen = "pause"
			if evt.key == K_SPACE:
				if currentScreen == "pause": running = False
				elif currentScreen == "intro":
					introCounter = 0
					currentScreen = "game"

		elif evt.type == KEYUP:
			if evt.key == K_e:
				interact = True
			elif evt.key == K_SPACE:
				advance = True

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
				currentScreen = "intro"

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

	elif currentScreen == "intro":
		screen.fill(BLACK)
		# The length of time (in ticks) for each sentence of the intro
		# 60 = 1 second
		length = 180
		introCounter += 1
		page = int(introCounter / length)
		if page < len(introText):
			i = introCounter % length
			c = 255
			if i < length/4:
				c = i/(length/4) * 255
			elif length-i < length/4:
				c = (length-i)/(length/4) * 255
			txt = introText[page]
			txtImg = fonts[0].render(txt, True, (c, c, c))
			txtRect = txtImg.get_rect()
			txtRect.center = width/2, height/2
			screen.blit(txtImg, txtRect)
		else:
			currentScreen = "game"

	display.flip()
	screen_copy = screen.copy()
	clock.tick(60) # FPS
	tick = (tick + 1) % (60*120) # global game tick counter, resetting after 120 seconds

sys.stderr.close()
sys.stderr = sys.__stderr__
quit()
