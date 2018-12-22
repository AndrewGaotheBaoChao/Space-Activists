from pygame import *

init()
font.init()

def get_image(sheet, pos):
	img = Surface((pos[2],pos[3]), SRCALPHA)
	img.fill((255,255,255,0))
	img.blit(sheet, img.get_rect(), pos)
	return img

def scale(pics, scale):
	for i in range(len(pics)):
		r = pics[i].get_rect()
		pics[i] = transform.scale(pics[i], (int(r.width*scale), int(r.height*scale)))

# Menu background and buttons images
menu = image.load("images/menu/menu.png")
playB = image.load("images/menu/play.png")
helpB = image.load("images/menu/help.png")
creditsB = image.load("images/menu/credits.png")
backB = image.load("images/menu/back.png")
helpS = image.load("images/menu/helpS.png")
creditsS = image.load("images/menu/creditsS.png")

# Button rects
playR = Rect(389, 349, 502, 58)
helpR = Rect(389, 416, 502, 58)
creditsR = Rect(389, 483, 502, 58)
backR = Rect(650, 483, 502, 58)

playerSheet = image.load('images/character_alpha.png')
playerImages = []
playerImages.append(get_image(playerSheet, [25, 100, 351, 451]))
playerImages.append(get_image(playerSheet, [425, 100, 351, 451]))
playerImages.append(get_image(playerSheet, [825, 100, 351, 451]))
playerImages.append(get_image(playerSheet, [1225, 100, 351, 451]))

playerImages.append(get_image(playerSheet, [25, 700, 351, 451]))
playerImages.append(get_image(playerSheet, [425, 700, 351, 451]))
playerImages.append(get_image(playerSheet, [825, 700, 351, 451]))
playerImages.append(get_image(playerSheet, [1225, 700, 351, 451]))

playerImages.append(get_image(playerSheet, [25, 1275, 351, 451]))
playerImages.append(get_image(playerSheet, [425, 1275, 351, 451]))
playerImages.append(get_image(playerSheet, [825, 1275, 351, 451]))
playerImages.append(get_image(playerSheet, [1225, 1275, 351, 451]))

playerImages.append(get_image(playerSheet, [25, 1875, 351, 451]))
playerImages.append(get_image(playerSheet, [425, 1875, 351, 451]))
playerImages.append(get_image(playerSheet, [825, 1875, 351, 451]))
playerImages.append(get_image(playerSheet, [1225, 1875, 351, 451]))

scale(playerImages, 0.25)

fonts = []
fonts.append(font.Font("fonts/sao.ttf", 46))
fonts.append(font.Font("fonts/sao.ttf", 60))
