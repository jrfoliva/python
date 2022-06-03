import pygame
import pygame.font

class Button():
	def __init__(self, screen, msg, position):
		"""Inicializa os atributos do botão."""
		self.screen = screen
		self.screen_rect = self.screen.get_rect()
		
		# Define as dimensões e as propriedades do botão
		self.width, self.height = 200, 50
		self.button_color = (0, 255, 0)
		self.text_color = (255, 255, 255)
		self.font = pygame.font.SysFont('calibri', 48, bold=True)

		# Constrói o objeto rect do botão e o centraliza conforme argumento
		self.rect = pygame.Rect(0, 0, self.width, self.height)
		if position == 'center':
			self.rect.center = self.screen_rect.center
		elif position == 'bottom':
			self.rect.bottom = self.screen_rect.bottom - 50
			self.rect.centerx = self.screen_rect.centerx
			
		# A mensagem do botão deve ser preparada apena uma vez
		self.prep_msg(msg)
				 
	def prep_msg(self, msg):
		"""Transforma msg em imagem renderizada e centraliza o texto no
		botão."""
		self.msg_image = self.font.render(msg, True, self.text_color,
			self.button_color)
		self.msg_image_rect = self.msg_image.get_rect()
		self.msg_image_rect.center = self.rect.center
				
	def draw_button(self):
		"""Desenha um botão em branco, e em seguida, desenha a mensagem."""
		self.screen.fill(self.button_color, self.rect)
		self.screen.blit(self.msg_image, self.msg_image_rect)
