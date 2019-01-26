#uses the system tools
import sys
import random
import os

import pygame

from settings import Settings, Sidebar, Textbox, Card_Table, Draw_Background_Pieces
from cards import Card, DealerCard, PlayerCard, Deck
import game_functions as gf
import sprites as sp

#create the font settings for later
font_preferences = [ 
	"Helvetica",
	"Cambria",
	"Garamond",
	"Comic Sans MS"
	]
textbox_font_size = 16
font_color = (255, 255, 255)

#create an instance of settings superclass that is used to draw the screen and later called by the other objects
ai_settings = Settings()
screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
pygame.display.set_caption("Blackjack")	

#create the instances that will contain the needed attributes to draw the individual screen pieces
sidebar_settings = Sidebar()
textbox_settings = Textbox()
table_settings = Card_Table()
screen_pieces = Draw_Background_Pieces(screen, sidebar_settings, textbox_settings)

#card spacing settings
table_offset = table_settings.table_width*.40

#variable to define printed text and keep active within loop
click = 0
space_offset = 5

#generate button sprites for later
dealButton = sp.dealButton(screen, "deal", 920, 300)
doubleButton = sp.doubleButton(screen, "double", 920, 400)
standButton = sp.standButton(screen, "stand", 920, 500)
upArrow = sp.upArrow(screen, "up", 1060, 300)
downArrow = sp.downArrow(screen, "down", 1060, 400)
hitButton = sp.hitButton(screen, "hit", 1060, 500)

dealButtonGray = sp.dealButton(screen, "deal_gray", 920, 300)
doubleButtonGray = sp.doubleButton(screen, "double_gray", 920, 400)
standButtonGray = sp.standButton(screen, "stand_gray", 920, 500)
hitButtonGray = sp.hitButton(screen, "hit_gray", 1060, 500)

#create a sprite group for the buttons
in_round_buttons_DbAllow = pygame.sprite.Group(dealButtonGray, doubleButton, standButton, upArrow, downArrow, hitButton)
in_round_buttons_DbDeny = pygame.sprite.Group(dealButtonGray, doubleButtonGray, standButton, upArrow, downArrow, hitButton)
out_of_round_buttons = pygame.sprite.Group(dealButton, doubleButtonGray, standButtonGray, upArrow, downArrow, hitButtonGray)

def run_game():
	#Initialize pygame screen and font modules
	pygame.init()
	pygame.font.init()
	
	#variables to determine round and statistics
	round_over = 0
	round_counter = 1
	wins = 0
	losses = 0
	#ratio = wins // losses
	
	#create the title
	title = gf.create_text("Blackjack", font_preferences, 42, font_color)
	
	#create lists to be used later in the game
	discard_pile = []
	deck = []
	player = []
	dealer = []
		
	#generate card elements and variables, then generate list
	deck_icon = Deck(screen, (table_settings.table_width // 2), (table_settings.table_height // 2) - 10)
	deck = Deck.createDeck()
	deck, discard_pile, player, dealer = Deck.deal(deck, discard_pile)
	
	#variable to define printed text and keep active within loop
	text = None
	text_placement = textbox_settings.y_pos + 5
	
	# Start the main loop for the game
	while True:
	
		#variables for mouse coordinates
		mouse_X = 0
		mouse_Y = 0

		#redraw the screen with elements during each pass through the loop
		screen.fill(ai_settings.bg_color)
		screen_pieces.draw()
		screen.blit(title, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 20))
		deck_icon.blitme()
		
		#generate statistic text
		round = gf.create_text("Round: " + str(round_counter), font_preferences, 28, font_color)
		screen.blit(round, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 80))
		stats = gf.create_text("Wins: " + str(wins) + " | " + "Losses: " + str(losses), font_preferences, 24, font_color)
		screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 120))
		
		if round_counter != 1 and losses != 0:
			ratio = 100 * float(wins)/float(losses)
			stats = gf.create_text("W/L Ratio: " + str("{0:.2f}".format(ratio)) + " %", font_preferences, 24, font_color)
			screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 150))	
		
		#draw the cards for the dealer and player
		Deck.drawCurrentHand(screen, player, dealer, table_offset, table_settings.y_pos, table_settings.table_height, round_over)	

		#print message to user on current status
		gf.textbox_message(screen, round_over, text, font_preferences, textbox_font_size, font_color, space_offset, text_placement, player)
		
		#check events for exit signal
		message = gf.check_events()
		
		#retrieve and keep text on screen of last event
		if message != None:
			#set click to 1 (used in next elif) and grabs the x and y coordinates pressed
			click = 1
			mouse_X, mouse_Y = message.split('|')
			
		#detect and respond if there is blackjack on start of round
		if len(player) == 2 and len(dealer) == 2 and round_over == 0:	
			text, round_over, wins, losses = gf.blackjack(player, dealer, text, round_over, wins, losses)
			
		
		#responds when user hits the double button
		deck, discard_pile, player, dealer, round_over, text, wins, losses = doubleButton.update(mouse_X, mouse_Y, deck, discard_pile, player, dealer, round_over, text, wins, losses)
		
		#responds when user hits the stand button
		round_over, text, deck, discard_pile, dealer, player, wins, losses = standButton.update(mouse_X, mouse_Y, round_over, player, dealer, text, deck, discard_pile, wins, losses)
		
		#responds when user hits the hit button
		deck, discard_pile, player, round_over, text, losses = hitButton.update(mouse_X, mouse_Y, deck, discard_pile, player, round_over, text, losses)
		
		#responds when user hits the deal button
		round_over, round_counter, deck, discard_pile, player, dealer = dealButton.update(mouse_X, mouse_Y, deck, discard_pile, player, dealer, round_over, round_counter)
		
		#draw start of round buttons to screen
		if round_over == 0 and len(player) == 2:
			in_round_buttons_DbAllow.draw(screen)
		#draw buttons after first hit
		elif round_over == 0 and len(player) > 2:
			in_round_buttons_DbDeny.draw(screen)
		#draw buttons for end of round
		else:
			out_of_round_buttons.draw(screen)
		
		# Make the most recently drawn screen visible
		pygame.display.flip()
	

#start the game
run_game()