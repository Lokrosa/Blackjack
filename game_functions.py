import sys

import pygame
from settings import Settings, Sidebar, Textbox, Card_Table


textbox_settings = Textbox()
sidebar_settings = Sidebar() 

"""next three functions found on nerdparadise.com as part of pygame tutorials"""
def make_font(fonts, size):
	#gets a list of lowercase spaceless font names
	available = pygame.font.get_fonts()
	
	#lambdas are one line functions , e.g. lambda argument: manipulate(argument)
	choices = map(lambda x:x.lower().replace(' ', ''), fonts)
	#loop through possible choices given by user against available fonts, if a match then take that font
	for choice in choices:
		if choice in available:
			return pygame.font.SysFont(choice, size)
	return pygame.font.Font(None, size)

#cache font choices in a dictionary on initialization call to uses easy later when repeatedly called
_cached_fonts = {}
def get_font(font_preferences, size):
	global _cached_fonts
	#creates a delimited string for series of font preferences and size given
	key = str(font_preferences) + '|' + str(size)
	font = _cached_fonts.get(key, None)
	#store font in dictinary if none exists and return font
	if font == None:
		font = make_font(font_preferences, size)
		_cached_fonts[key] = font
	return font
	
#cache font choices in a dictionary on initialization call to uses easy later when repeatedly called
_cached_text = {}
def create_text(text, fonts, size, color):
	global _cached_text
	#join all settings (font, size, color, text) as a string
	key = '|'.join(map(str, (fonts, size, color, text)))
	#try to get current cached text from the dictionary and if not return none
	image = _cached_text.get(key, None)
	#if no text is given earlier (none) then run the get font and render the text as an image then store in dictionary 
	if image == None:
		font = get_font(fonts, size)
		image = font.render(text, True, color)
		_cached_text[key] = image
	return image		

def check_events():
	
	#Watch for keyboard and mouse events
	for event in pygame.event.get():
			
		#if the exit button is hit close the game screen and exit pygame
		if event.type == pygame.QUIT:
			pygame.display.quit()
			#its not running anymore so shut down the game and exit interpreter - this is for my development (macro to run is set to keep shell open on close of game)
			print("\n Please type exit() to close shell\n")
			sys.exit()
		elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
			pygame.display.quit()
			print("\n Please type exit() to close shell\n")
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				mouse_X, mouse_Y = pygame.mouse.get_pos()
				message = str(mouse_X) + "|" + str(mouse_Y)
				return message
		elif event.type == pygame.MOUSEBUTTONUP:
			#variables for mouse coordinates
			mouse_X = 0
			mouse_Y = 0

def checkValue(hand):
	""" Checks the value of the cards in a hand """

	hand_total = 0

	for card in hand:
		value = card[1:]

		# face cards worth 10 and ace worth 11 or 1 depending on situation  
		if value == 'j' or value == 'q' or value == 'k': value = 10
		elif value == 'a': 
			if hand_total <= 10: value = 11
			else: value = 1
		else: value = int(value)

		hand_total += value
	
	return hand_total
		
def determineWinner(player_value, dealer_value, wins, losses):
	"""determines the winner of the round"""
	
	#return the winner status
	if player_value > dealer_value:
		wins += 1
		return "player", wins, losses
	elif player_value < dealer_value:
		losses += 1
		return "dealer", wins, losses
	else:
		return "push", wins, losses

def blackjack(player_hand, dealer_hand, text, round_over, wins, losses):
	"""determines if play or dealer has blackjack or if a blackjack tie has occurred"""
	
	message = text
	
	if round_over == 0:
	
		player_value = checkValue(player_hand)
		dealer_value = checkValue(dealer_hand)
		
		if player_value == 21 and dealer_value != 21:
			round_over = 1
			wins += 1
			message = "player blackjack"
		elif player_value != 21 and dealer_value == 21:
			round_over = 1
			losses += 1
			message = "dealer blackjack"
		elif player_value == 21 and dealer_value == 21:
			round_over = 1
			message = "push"
		else:
			round_over = 0
		
	return message, round_over, wins, losses
	
	
def textbox_message(screen, round_over, text, font_preferences, textbox_font_size, font_color, space_offset, text_placement, player):
	"""this function is the logic loop by using text keywords to determine what to print to the user console"""

	if round_over == 1:
		if text != None:
			if text == "player" or text == "dealer" or text == "push":
				if text == "player" or text == "dealer":
					text_message = "The winner is the " + text
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))
				else:
					text_message = "The round is a push (tie)"
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))
			elif "bust" in text:
				if text == "player bust":
					text_message = "Dealer wins - you bust..."
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))
				elif text == "dealer bust":
					text_message = "Dealer busts - you win!"
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))
			elif "blackjack" in text:
				if text == "player blackjack":
					text_message = "Blackjack! You won the round!"
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))
				else:
					text_message = "Dealer won with blackjack..."
					textbox_message = create_text(text_message, font_preferences, textbox_font_size, font_color)
					screen.blit(textbox_message, (space_offset, text_placement))			
	#[COMMENTED FEATURE] uncomment to print to console the current total of the users hand at any point during the a set
	#else:
		#if text != None:
			#text = "The player currently holds " + str(checkValue(player))
			#textbox_message = create_text(text, font_preferences, textbox_font_size, font_color)
			#screen.blit(textbox_message, (space_offset, text_placement))
			
def print_screen_stats(screen, font_preferences, font_color, round_counter, wins, losses):
	"""function to print the statistics to screen"""

	#generate wins and losses to print to screen
	round = create_text("Round: " + str(round_counter), font_preferences, 24, font_color)
	screen.blit(round, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 140))
	stats = create_text("Wins: " + str(wins) + " | " + "Losses: " + str(losses), font_preferences, 24, font_color)
	screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 20, 200))
	
	#generate W/L ratio to print to screen
	if round_counter != 1 and losses != 0:
		ratio = 100 * float(wins)/float(losses)
		stats = create_text("W/L Ratio: " + str("{0:.2f}".format(ratio)) + " %", font_preferences, 24, font_color)
		screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 24, 260))
	elif round_counter != 1 and wins != 0:
		stats = create_text("W/L Ratio: " + str("{0:.2f}".format(100)) + " %", font_preferences, 24, font_color)
		screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 24, 260))
	elif round_counter != 1 and wins >= losses:
		stats = create_text("W/L Ratio: " + str("{0:.2f}".format(100)) + " %", font_preferences, 24, font_color)
		screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 24, 260))
	else:
		stats = create_text("W/L Ratio: " + str("{0:.2f}".format(0)) + " %", font_preferences, 24, font_color)
		screen.blit(stats, ((sidebar_settings.x_pos + sidebar_settings.sidebar_quartered) - 24, 260))
			
