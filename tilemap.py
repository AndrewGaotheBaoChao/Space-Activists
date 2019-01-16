from pygame import *
import pytmx
from settings import *

class Map:
	def __init__(self, filename):
		self.data = []
		with open(filename, 'rt') as f:
			for line in f:
				self.data.append(line.strip())

		self.tilewidth = len(self.data[0])
		self.tileheight = len(self.data)
		self.width = self.tilewidth * ts
		self.height = self.tileheight * ts

class TiledMap:
	def __init__(self, filename):
		tm = pytmx.load_pygame(filename, pixelalpha = True)
		self.width = tm.width * tm.tilewidth
		self.height = tm.height * tm.tileheight
		self.tmxdata = tm
		try: self.small = bool(int(tm.small))
		except: self.small = False

		self.walls = []
		self.player_spawn = [0, 0]
		self.npcs = []
		self.portals = []

		for t in tm.visible_layers:
			if isinstance(t, pytmx.TiledObjectGroup):
				for obj in t:
					if obj.visible:
						if obj.name == "wall":
							self.walls.append(Rect(obj.x, obj.y, obj.width, obj.height))
						elif obj.name == "spawn":
							self.player_spawn = [obj.x, obj.y]
						elif obj.name == "npc":
							self.npcs.append(obj)
						elif obj.name == "portal":
							self.portals.append(obj)

	def render_area(self, surface, rect):
		ti = self.tmxdata.get_tile_image_by_gid
		tw, th = self.tmxdata.tilewidth, self.tmxdata.tileheight
		for layer in self.tmxdata.visible_layers:
			if isinstance(layer, pytmx.TiledTileLayer):
				for x, y, gid in layer:
					r = Rect(x*tw, y*th, tw, th)
					if rect.colliderect(r):
						tile = ti(gid)
						if tile:
							surface.blit(tile, (x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

	def render(self, surface):
		self.render_area(surface, Rect(0, 0, self.width, self.height))

	def make_map(self, rect):
		temp_surface = Surface((self.width, self.height))
		self.render_area(temp_surface, rect)
		return temp_surface

class Camera:
	def __init__(self, width, height):
		self.camera = Rect(0, 0, width, height)
		self.width = width
		self.height = height

	def apply(self, entity):
		return entity.rect.move(self.camera.topleft)

	def apply_rect(self, rect):
		return rect.move(self.camera.topleft)

	def update(self, target, small):
		x = -target.rect.centerx + int(width / 2)
		y = -target.rect.centery + int(height / 2)

		if not small:
			# limit scrolling to map size
			x = min(0, x)  # left
			y = min(0, y)  # top
			x = max(-(self.width - width), x)  # right
			y = max(-(self.height - height), y)  # bottom
		self.camera = Rect(x, y, self.width, self.height)