from pygame import *

def get_image(sheet, pos):
	img = Surface((pos[2],pos[3]), SRCALPHA)
	img.fill((255,255,255,0))
	img.blit(sheet, img.get_rect(), pos)
	return img

def load():
	global playerSheet, playerImages
	playerSheet = image.load('images/character.png')
	playerImages = []
	playerImages.append(get_image(playerSheet, [25, 100, 351, 451]))
	playerImages.append(get_image(playerSheet, [448, 100, 351, 451]))
	playerImages.append(get_image(playerSheet, [823, 100, 351, 451]))
	playerImages.append(get_image(playerSheet, [1123, 100, 351, 451]))
