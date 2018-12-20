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
myClock = time.Clock()
running = True

mode = 'menu'
offsetX = offsetY = 0

class Player:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.image = Surface((50, 50))
		self.rect = self.image.get_rect()
		self.rect.center = self.x, self.y

	def update(self):
		self.rect.center = self.x, self.y

	def draw(self, surf):
		draw.rect(surf, GREEN, self.rect)

ox = oy = mx = my = 0

# Actual Game Stuff
particles = []
gravPoints = []
gravPoints.append([width/2, height/2, 50])
rad = 5
player = Player(width/2, height/2)

# Menu Stuff
titleFont = font.SysFont("Poor Richard", 76)

while running:
	mouseDown = mouseUp = False
	for evt in event.get():
		if evt.type == QUIT:
			running = False
		elif evt.type == KEYDOWN:
			if evt.key == K_ESCAPE:
				running = False
		elif evt.type == MOUSEBUTTONDOWN:
			if evt.button == 1:
				mouseDown = True
				ox, oy = mx, my
			if evt.button == 4:
				# Mouse Wheel Up
				rad += 1
			if evt.button == 5:
				# Mouse Wheel DOWN
				rad -= 1

		elif evt.type == MOUSEBUTTONUP:
			if evt.button == 1:
				mouseUp = True

	# Updates
	mx, my = mouse.get_pos()
	mb = mouse.get_pressed()

	screen.fill(WHITE)
	if mb[0]:
		draw.circle(screen, BLACK, (ox, oy), 5)
		draw.line(screen, BLACK, (mx, my), (ox, oy))

	if mouseUp:
		dx = ox - mx
		dy = oy - my
		vx = dx / 10
		vy = dy / 10
		particles.append([ox, oy, vx, vy, 0, 0, rad])

	for g in gravPoints:
		draw.circle(screen, RED, (int(g[0]), int(g[1])), g[2])

	for i in range(len(particles)-1, -1, -1):
		p = particles[i]
		for g in gravPoints:
			dx = p[0] - g[0]
			dy = p[1] - g[1]
			dist = hypot(dx, dy)
			ang = atan2(dy, dx) - radians(180)
			f = (10 * g[2] * p[6]) / max(1, dist)**2
			p[4] = f*cos(ang)
			p[5] = f*sin(ang)
		p[2] += p[4]
		p[3] += p[5]
		p[0] += p[2]
		p[1] += p[3]
		draw.circle(screen, BLACK, (int(p[0]), int(p[1])), 5)

		if not (-100 < p[0] < width+100 and -100 < p[1] < height+100):
			del particles[i]
			print("GONE")

	display.flip()
	myClock.tick(60)

quit()