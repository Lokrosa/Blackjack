'''
As the game expands, new settings will be introduced as well. Creating a module will allow the settings to be stored in one place.

Potential Ideas:
revisiting sublasses as when new variables are defined for older ones the older atttributes sit unused
	
'''

import pygame

class Settings():
	"""a class to store all the initialization draw settings for Blackjack screen"""
	
	def __init__(self):
		"""Initialize the game's settings"""
		
		#screen settings
		self.screen_width = 1200
		self.screen_height = 600
	
		#light blue background color for the game table
		self.bg_color = (108, 207, 192)
		
class Sidebar(Settings):
	"""a class to store all the settings for the sidebar that will hold the interactive pieces and text"""
	
	def __init__(self):
		"""initializes the sidebar settings"""
		
		#pull variables from parent class settings that draws the full game screen
		Settings.__init__(self)
		
		#take the variables of the screen settings and change as necessary to make the box
		self.modified_width = int(self.screen_width * .25) #change this value to change how space the box takes up of the screen
		self.sidebar_width = self.modified_width # 25% the width of the full screen
		self.sidebar_height = self.screen_height
		self.sidebar_quartered = self.modified_width // 4 # pixel width quartered for button/text positioning
		
		# starting position of box within screen
		self.x_pos = self.screen_width - self.modified_width
		self.y_pos = 0
		
		# color the background of menu black
		self.bg_color = (0, 0, 0)

class Textbox(Settings):
	"""a class to store the settings for the bottom text box that will be where results are printed and questions asked"""
	
	def __init__(self):
		"""initialze the instance settings for the text box"""
	
		#pull variables from parent class settings that draws the full game screen
		Settings.__init__(self)
		
		#take the variables of the screen settings and change as necessary to make the box
		self.modified_height = int(self.screen_height * .05) #change this value to change how space the box takes up of the screen
		self.textbox_width = (self.screen_width * .75) #text box width is reaches from lefthand side of screen to the beginning of the sidebar box
		self.textbox_height = self.modified_height #15% of the height  of the full screen
		
		# starting position of box within screen
		self.x_pos = 0
		self.y_pos = self.screen_height - self.modified_height
		
		# color background of menu black
		self.bg_color = (0, 0, 0)
		
class Card_Table(Settings):
	"""a class to store the dimension settings of the card table area"""

	def __init__(self):
		"""initialze the instance settings for the text box"""

		#pull variables from parent class settings that draws the full game screen
		Settings.__init__(self)
		
		#take the variables of the screen settings to determine the ending width and height of the table area
		self.table_x_start = int(self.screen_width * .01)
		self.table_y_start = int(self.screen_height * .01)
		self.table_width = int(self.screen_width * .74) #giving 1% offset for the card placement
		self.table_height = int(self.screen_height * .94) #giving 1% offset for the card placement 
		
		# starting position of box within screen
		self.x_pos = self.table_x_start
		self.y_pos = self.table_y_start
		
class Draw_Background_Pieces():
	"""This takes in all the draw settings and makes it callable as one function for refactoring"""
	
	def __init__(self, screen, sidebar_settings, textbox_settings):
		"""initializes the instance settings for the drawing"""
		
		#screen settings
		self.screen = screen
		
		#define the sidebar rectangle draw settings from the settings grabbed by the instances passed into the class
		self.sidebar_color = sidebar_settings.bg_color
		self.sidebar_xpos = sidebar_settings.x_pos
		self.sidebar_ypos = sidebar_settings.y_pos
		self.sidebar_width = sidebar_settings.sidebar_width
		self.sidebar_height = sidebar_settings.sidebar_height
		self.sidebar_edge_thickness = 0 #this determines the thickness to draw outer edge, 0 means rectangle will be filled
		
		#define the textbox rectangle draw settings from the settings grabbed by the instances passed into the class
		self.textbox_color = textbox_settings.bg_color
		self.textbox_xpos = textbox_settings.x_pos
		self.textbox_ypos = textbox_settings.y_pos
		self.textbox_width = textbox_settings.textbox_width
		self.textbox_height = textbox_settings.textbox_height
		self.textbox_edge_thickness = 0 #this determines the thickness to draw outer edge, 0 means rectangle will be filled
		
	def draw(self):
		"""draw the sidebar and textbox elements to the screen"""
		pygame.draw.rect(self.screen, self.sidebar_color, (self.sidebar_xpos, self.sidebar_ypos, self.sidebar_width, self.sidebar_height), self.sidebar_edge_thickness)
		pygame.draw.rect(self.screen, self.textbox_color, (self.textbox_xpos, self.textbox_ypos, self.textbox_width, self.textbox_height), self.textbox_edge_thickness)
		