from pygame import *

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