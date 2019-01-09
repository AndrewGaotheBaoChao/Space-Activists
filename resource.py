from pygame import *

init()
font.init()

# font, text, width
def mul_lines(f, t, wid, f_color=(0,0,0)):
	lines = []
	while f.size(t)[0] > wid:
		pos = len(t)
		while f.size(t[0:pos])[0] > wid:
			pos = t.rfind(' ', 0, pos)
			if pos == -1:
				continue
		lines.append(t[0:pos])
		t = t[pos+1:]
	lines.append(t)

	totHeight = f.size(lines[0])[1] * len(lines)
	surf = Surface((wid, totHeight), SRCALPHA)
	surf.fill((0,0,0,0))
	for p in range(len(lines)):
		lineFont = f.render(lines[p], True, f_color)
		lineFontRect = lineFont.get_rect()
		lineFontRect.topleft = 0, p * lineFont.get_height()
		surf.blit(lineFont, lineFontRect)
	return surf

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

fonts = []
fonts.append(font.Font("fonts/sao.ttf", 60))
fonts.append(font.Font("fonts/sao.ttf", 46))
fonts.append(font.Font("fonts/sao.ttf", 36))
fonts.append(font.Font("fonts/sao.ttf", 20))

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

scale(playerImages, 0.18)

npcImages = [[]]

npcSheet = image.load('images/npcs/c1.png')
npc1 = []
npc1.append(get_image(npcSheet, [7, 34, 18, 31]))
npc1.append(get_image(npcSheet, [7, 2, 18, 31]))
npc1.append(get_image(npcSheet, [7, 66, 18, 31]))
npc1.append(get_image(npcSheet, [7, 98, 18, 31]))

scale(npc1, 3)
npcImages.append(npc1)

npcSheet = image.load('images/npcs/c2.png')
npc2 = []
npc2.append(get_image(npcSheet, [70, 5, 20, 27]))
npc2.append(get_image(npcSheet, [6, 5, 20, 27]))
npc2.append(get_image(npcSheet, [6, 37, 20, 27]))
npc2.append(transform.flip(npc2[2], True, False))

scale(npc2, 3)
npcImages.append(npc2)
