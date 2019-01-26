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
	"Cambria",
	"Garamond",
	"Comic Sans MS",
	"Wingdings"
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
dealButton = sp.dealButton(screen, "deal", 1060, 400)
doubleButton = sp.doubleButton(screen, "double", 920, 400)
standButton = sp.standButton(screen, "stand", 920, 500)
hitButton = sp.hitButton(screen, "hit", 1060, 500)

dealButtonGray = sp.dealButton(screen, "deal_gray", 1060, 400)
doubleButtonGray = sp.doubleButton(screen, "double_gray", 920, 400)
standButtonGray = sp.standButton(screen, "stand_gray", 920, 500)
hitButtonGray = sp.hitButton(screen, "hit_gray", 1060, 500)

#create a sprite group for the buttons
in_round_buttons_DbAllow = pygame.sprite.Group(dealButtonGray, doubleButton, standButton, hitButton)
in_round_buttons_DbDeny = pygame.sprite.Group(dealButtonGray, doubleButtonGray, standButton, hitButton)
out_of_round_buttons = pygame.sprite.Group(dealButton, doubleButtonGray, standButtonGray, hitButtonGray)

def run_game():
	#Initialize pygame screen and font modules
	pygame.init()
	pygame.font.init()
	
	#variables to determine round and statistics
	round_over = 0
	round_counter = 1
	wins = 0
	losses = 0
	
	#create the title
	title = gf.create_text("Blackjack", font_preferences, 42, font_color)
	author = gf.create_text("By: Cole Lehman", font_preferences, 20, font_color)
	
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

		#draw background and base static elements first through each pass
		screen.fill(ai_settings.bg_color)
		screen_pieces.draw()
		screen.blit(title, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 20))
		screen.blit(author, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 70))
		deck_icon.blitme()
		
		#print current stats to screen
		gf.print_screen_stats(screen, font_preferences, font_color, round_counter, wins, losses)
		
		#draw the cards for the dealer and player
		Deck.drawCurrentHand(screen, player, dealer, table_offset, table_settings.y_pos, table_settings.table_height, round_over)	

		#print messages to user on status of the game (result of round)
		gf.textbox_message(screen, round_over, text, font_preferences, textbox_font_size, font_color, space_offset, text_placement, player)
		
		#check events for exit signal and mouse button presses
		message = gf.check_events()
		
		#retrieve mouse output (formatted as string since check events cannot return multiple variables) and splice the output to retrieve mouse X & Y coord.
		if message != None:
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