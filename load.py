from pygame import *

# Menu background and buttons images
menu = image.load("images/menu/menu.png")
play = image.load("images/menu/play.png")
helpB = image.load("images/menu/help.png")
creditsB = image.load("images/menu/credits.png")

# Menu button rects
playR = Rect(389, 349, 502, 58)
helpR = Rect(389, 416, 502, 58)
creditsR = Rect(389, 483, 502, 58)