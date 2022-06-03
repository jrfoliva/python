import pygame
from button import Button

class Banner():
	"""Classe que trata a imgagem de um banner para apresentação."""
	def __init__(self, image, screen):		
		"""Inicializa a imagem e pega seu retângulo."""
		self.image = image
		self.image_rect = self.image.get_rect()
		
		#Captura o retângulo da tela
		self.screen = screen
		self.screen_rect = screen.get_rect()
		
		#posiciona a imagem do banner no centro da tela
		self.image_rect.center = self.screen_rect.center
				
		#Flag para controle de visualização
		self.banner_view = False
	
	def show_banner(self):
		"""Exibe o banner conforme posicionado."""
		self.screen.blit(self.image, self.image_rect)
	
		
	
