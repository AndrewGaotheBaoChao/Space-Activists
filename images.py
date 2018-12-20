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
	playerImages.append(get_image(playerSheet, [450, 100, 351, 451]))
	playerImages.append(get_image(playerSheet, [825, 100, 351, 451]))
	playerImages.append(get_image(playerSheet, [1125, 100, 351, 451]))

	playerImages.append(get_image(playerSheet, [25, 700, 351, 451]))
	playerImages.append(get_image(playerSheet, [450, 700, 351, 451]))
	playerImages.append(get_image(playerSheet, [825, 700, 351, 451]))
	playerImages.append(get_image(playerSheet, [1125, 700, 351, 451]))

	playerImages.append(get_image(playerSheet, [25, 1275, 351, 451]))
	playerImages.append(get_image(playerSheet, [450, 1275, 351, 451]))
	playerImages.append(get_image(playerSheet, [825, 1275, 351, 451]))
	playerImages.append(get_image(playerSheet, [1125, 1275, 351, 451]))
