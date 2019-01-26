import os
import pygame

from settings import Settings, Sidebar, Textbox
from cards import Deck
import game_functions as gf

#create relative paths to make it easier to access the repositories within the folder
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')

class Button(pygame.sprite.Sprite, Sidebar):

	def __init__(self, screen, image, x, y):
	
		self.screen = screen
		
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(image_path, (str(image) +'.png')))
		self.rect = self.image.get_rect()
		
		self.rect.left = x 
		self.rect.top = y
	
	def blitme(self):
		"""draw the card at its current location"""
		self.screen.blit(self.image, self.rect)

class dealButton(Button):
	""" Button that deals cards """
        
	def __init__(self, screen, image, x, y):
	
		Button.__init__(self, screen, image, x, y)
		self.rect = self.image.get_rect()
	
		self.rect.left = x 
		self.rect.top = y
		
	def update(self, mouse_X, mouse_Y, deck, discard_pile, player, dealer, round_over, round_counter):
		"""runs an update check to see if player hit the button and to do the necessary items when hit"""
		
		if self.rect.collidepoint(int(mouse_X), int(mouse_Y)) == 1 and  round_over == 1:
			#print("deal button hit successfully")
			
			#reset counters
			round_over = 0
			round_counter += 1
			
			#make a new deck and distribute cards
			deck = Deck.createDeck()
			deck, discard_pile, player, dealer = Deck.deal(deck, discard_pile)
			
		return round_over, round_counter, deck, discard_pile, player, dealer
		
		
class doubleButton(Button):
	""" Button to stand on current hand """
        
	def __init__(self, screen, image, x, y):
	
		Button.__init__(self, screen, image, x, y)
		self.rect = self.image.get_rect()
	
		self.rect.left = x #make value of self.rect.left match the left side of the button to whatever position given
		self.rect.top = y
	
	def update(self, mouse_X, mouse_Y, deck, discard_pile, player_hand, dealer_hand, round_over, text, wins, losses):
		"""respond to user request to double down"""
		
		winner = text
		
		if self.rect.collidepoint(int(mouse_X), int(mouse_Y)) == 1 and round_over == 0 and len(player_hand) == 2:
			#round is over, distribute card to user and see who wins
			round_over = 1
			
			deck, discard_pile, player_hand = Deck.hit(deck, discard_pile, player_hand)
			
			player_value = gf.checkValue(player_hand)
			dealer_value = gf.checkValue(dealer_hand)
			
			if player_value > 21:
				winner = "player bust"
				losses += 1
			else:
				if dealer_value < 17:
					deck, discard_pile, dealer_hand = Deck.hit(deck, discard_pile, dealer_hand)
					dealer_value = gf.checkValue(dealer_hand)
				
				#check for a bust on dealer
				if dealer_value > 21:
					winner = "dealer bust"
					wins += 1
				elif player_value > dealer_value:
					winner = "player"
					wins += 1
				elif player_value < dealer_value:
					winner = "dealer"
					losses += 1
				elif player_value == dealer_value:
					winner = "push"
				
				
	
		return deck, discard_pile, player_hand, dealer_hand, round_over, winner, wins, losses
		
class hitButton(Button):
	"""generates the hit button sprite to be used within game"""

	def __init__(self, screen, image, x, y):
	
		Button.__init__(self, screen, image, x, y)
		self.rect = self.image.get_rect()
	
		self.rect.left = x #make value of self.rect.left match the left side of the button to whatever position given
		self.rect.top = y
	

	def update(self, mouse_X, mouse_Y, deck, discard_pile, player, round_over, text, losses):
		"""respons to the users request to to hit"""
		
		winner = text
		
		if self.rect.collidepoint(int(mouse_X), int(mouse_Y)) == 1 and round_over == 0:
			deck, discard_pile, player = Deck.hit(deck, discard_pile, player)
			
			hand_total = gf.checkValue(player)
			
			#check for a bust
			if hand_total > 21:
				round_over = 1
				losses += 1
				winner = "player bust"
			
		return deck, discard_pile, player, round_over, winner, losses

class standButton(Button):
	"""geenrates the stand button"""

	def __init__(self, screen, image, x, y):
	
		Button.__init__(self, screen, image, x, y)
		self.rect = self.image.get_rect()
	
		self.rect.left = x 
		self.rect.top = y
		
	def update(self, mouse_X, mouse_Y, round_over, playerHand, dealerHand, text, deck, discard_pile, wins, losses):
		"""runs an update check to see if player hit the button and stand/end round if hit"""
		
		winner = text
		
		if self.rect.collidepoint(int(mouse_X), int(mouse_Y)) == 1 and round_over == 0:
			
			#if round isn't over set to end of round
			if round_over == 0:
				round_over = 1
				
				#determine current totals in each hand
				player_total = gf.checkValue(playerHand)
				dealer_total = gf.checkValue(dealerHand)
				
				#if dealer is under 17, hit until he is at 17+
				while dealer_total < 17:
					deck, discard_pile, dealerHand = Deck.hit(deck, discard_pile, dealerHand)
					dealer_total = gf.checkValue(dealerHand)
					
				#if dealer hit pushes over 21 then he loses, otherwise, determine winner
				if dealer_total > 21:
					winner = "dealer bust"
					wins += 1
				else:
					winner, wins, losses = gf.determineWinner(player_total, dealer_total, wins, losses)
			
		return round_over, winner, deck, discard_pile, dealerHand, playerHand, wins, losses

		