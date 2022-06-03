import pygame
from bullet import Bullet
from pygame.sprite import Group

class Ship():
	
	def __init__(self, ai_settings, screen, sound):
		"""Inicializa a spaçonave e define sua posição na tela inicial."""

		self.screen = screen
		self.ai_settings = ai_settings
		self.sound = sound
		#Carrega a imagem da espaçonave e obtém seu rect
		self.image = self.ai_settings.ship_img
		self.rect = self.image.get_rect()
		self.screen_rect = screen.get_rect()
		
		#Inicia cada nova espaçonave na parte inferior central da tela
		self.rect.centerx = self.screen_rect.centerx
		self.rect.bottom = self.screen_rect.bottom
		
		#Armazena um valor decimal para o centro da espaçonave
		self.center = float(self.rect.centerx)
			
		#Flag de movimento
		self.moving_right = False
		self.moving_left = False
	
		#Define o quanto de dano suporta
		self.bullet_damage = 0
		
		#Grupo de bullet
		self.bullets = Group()
		
	def blitme(self):
		"""Desenha a espaçonave na sua posição atual."""
		self.screen.blit(self.image, self.rect)

	def update(self):
		"""Atualiza a posição da espaçonave de acordo com a flag de 
			movimento."""
		if self.moving_right and self.rect.right < self.screen_rect.right:
			self.center += self.ai_settings.ship_speed_factor
		if self.moving_left and self.rect.left > 0:
			self.center -= self.ai_settings.ship_speed_factor
		
		#Atualiza o objeto rect conforme self.center
		self.rect.centerx = self.center
	
	def center_ship(self):
		"""Centraliza a ship na tela."""
		self.center = self.screen_rect.centerx

	def change_image(self, image=None):
		"""Troca a imagem do alien por explosão se atingido.
		Se image passado por parâmetro"""
		if not image:
			image = self.ai_settings.explosion
			self.sound.track_explosion.play(loops=0)
		image_rect = image.get_rect()
		image_rect.center = self.rect.center
		self.screen.blit(image, image_rect)
			
	def fire_bullet(self):
		"""Dispara um projétil se o limite ainda não foi alcançado."""
		if len(self.bullets) < self.ai_settings.bullets_allowed:
			self.sound.track_laser.play(loops=0)
			new_bullet = Bullet(self.ai_settings, self.screen, self.rect)
			self.bullets.add(new_bullet)
