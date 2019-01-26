import random
import os
import pygame

#create relative paths to make it easier to access the repositories within the folder
current_path = os.path.dirname(__file__)
image_path = os.path.join(current_path, 'images')
card_path = os.path.join(image_path, 'cards')

class Card():

	def __init__(self, screen, x, y):
		"""Initialize a card and set its position on screen"""
		self.screen = screen
		
		# Load a card image and get its rect
		#this returns a surface representing the card which is stored within the self.image
		self.image = pygame.image.load(os.path.join(card_path, 'back.png'))
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#put the card at the bottom center of the screen
		self.rect.centerx = x #make value of self.rect.centerx (the x-coordinate of card center) match centerx value of screen's rect
		self.rect.bottom = y #make the value of the self.rect.bottom (y-cord of card bottom) to value of screen rect's bottom attribute
		
	def blitme(self):
		"""draw the card at its current location"""
		self.screen.blit(self.image, self.rect)
		
class DealerCard(Card):
	"""a class to store the positioning details for the dealer's cards"""
	
	def __init__(self, screen, card_name, x, y):
		"""initialze the instance settings passed for the dealer card class"""

		#pull variables from the parent card class to use in positioning the dealer card
		Card.__init__(self, screen, x, y)
		
		#pull the card image from the repository located within the card images folder
		self.image = pygame.image.load(os.path.join(card_path, (card_name + '.png'))) 
		
		#put the card at the values passed into function
		self.rect.right = x #make value passed be the location of the right side of the card object
		self.rect.top = y
		
class PlayerCard(Card):
	"""a class to store the positioning details for the player's cards"""
	
	def __init__(self, screen, card_name, x, y):
		"""initialze the instance settings passed for the player card class"""

		#pull variables from the parent card class to use in positioning the plaer card
		Card.__init__(self, screen, x, y)
		
		self.image = pygame.image.load(os.path.join(card_path, (card_name + '.png'))) 
		
		#put the card at the values passed into the function
		self.rect.right = x 
		self.rect.bottom = y

class Deck(Card):
	"""a class to store the settings and important functions of the deck and how it operates in conjunction with dealer/player hands"""
	
	def __init__(self, screen, x, y):
		"""initialze the instance settings for the text box"""

		#pull variables from parent class settings that draws the full game screen
		Card.__init__(self, screen, x, y)
		
		self.image = pygame.image.load(os.path.join(card_path, 'deck.png')) 
		
		#put the card at the bottom center of the screen
		self.rect.centerx = x #make value of self.rect.centerx (the x-coordinate of card center) match centerx value of screen's rect
		self.rect.top = y
		
	def createDeck():
		""" Creates a deck with 52 cards"""
		
		#define the card titles that are not number cards
		deck = ['sj', 'sq', 'sk', 'sa', 'hj', 'hq', 'hk', 'ha', 'cj', 'cq', 'ck', 'ca', 'dj', 'dq', 'dk', 'da']
		values = range(2,11)
		#create the number value cards to the array and append
		for x in values:
			spades = "s" + str(x)
			hearts = "h" + str(x)
			clubs = "c" + str(x)
			diamonds = "d" + str(x)
			deck.append(spades)
			deck.append(hearts)
			deck.append(clubs)
			deck.append(diamonds)
		return deck
		
	def shuffle(deck):
		""" 
		shuffles deck using fisher-yates shuffle algorithm, better than using random class. Analogous to pulling out of a hat. Alg is:
			for i from n-1 to 1 do
				j <- random int such that 0 <= j <= i
				exchange a[j] and a[i]		
		"""
		n = len(deck) - 1
		while n > 0:
			j = random.randint(0, n)
			deck[j], deck[n] = deck[n], deck[j]
			n -= 1

		return deck
		
	def refreshDeck(deck, discardPile):
		"""this function allows us to reshuffle the discard pile and refresh into the deck"""
	
		print("\ndeck has " + str(len(deck)) + "cards\n" + "discard pile has " + str(len(discardPile)) + "cards\n")
		#copy all elements from the discard pile back into the deck
		for card in discardPile:
			deck.append(card)
		del discardPile[:]
		print("\ndeck now has " + str(len(deck)) + "cards\n" + "discard pile has " + str(len(discardPile)) + "cards\n")
		
		#shuffle the deck and return both the deck and discard_pile
		deck = Deck.shuffle(deck)
		return deck, discardPile
		
	def deal(deck, discardPile):
		"""function to deal to deal the cards to player and dealer"""
		
		#each new round the deck needs to be reshuffled
		deck = Deck.shuffle(deck)
		dealer, player = [], []

		cardsToDeal = 4

		while cardsToDeal > 0:
			#if deck is empty we need to refresh before proceeding
			if len(deck) == 0:
				deck, deadDeck = Deck.refreshDeck(deck, discardPile)

			# deals to player then dealer
			if cardsToDeal % 2 == 0: 
				player.append(deck[0])
			else: 
				dealer.append(deck[0])
			
			#delete element of deck deal list
			del deck[0]
			cardsToDeal -= 1
		
		#return modified deck, discard pile, player, and dealer hands
		return deck, discardPile, player, dealer
		
	def hit(deck, discardPile, hand):
		""" restores deck if no cards remain and hits with new card from deck"""

		# if the deck is empty, shuffle in the dead deck
		if len(deck) == 0:
			deck, discardPile = Deck.refreshDeck(deck, discardPile)

		hand.append(deck[0])
		discardPile.append(deck[0])
		del deck[0]

		return deck, discardPile, hand
		
	def drawCurrentHand(screen, playerHand, dealerHand, table_offset, dealer_y_pos, player_y_pos, round_over):
		"""draws the current dealer and player hands to the screen"""
		
		if round_over == 0:
			#draw the cards for the player and dealer, however keep on card face down
			for card in range(len(dealerHand)):	
				if card == (len(dealerHand) - 1): DealerCard(screen, "back", (table_offset + (25*card)), dealer_y_pos).blitme() #cant show
				else: DealerCard(screen, dealerHand[card], (table_offset + (25*card)), dealer_y_pos).blitme()
			for card in range(len(playerHand)):
				PlayerCard(screen, playerHand[card], (table_offset + (25*card)), player_y_pos).blitme()
		else:
			#show all cards for dealer and player, face up
			for card in range(len(dealerHand)):	
				DealerCard(screen, dealerHand[card], (table_offset + (25*card)), dealer_y_pos).blitme() #cant show
			for card in range(len(playerHand)):
				PlayerCard(screen, playerHand[card], (table_offset + (25*card)), player_y_pos).blitme()