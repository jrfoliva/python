import pygame
from pygame.sprite import Sprite
from pygame.sprite import Group
from bullet2 import Bullet2

class Boss(Sprite):
	"""Classe que representa um alienígena."""
	
	def __init__(self, ai_settings, screen, sound):
		"""Inicializa um alienígena e define sua posição inicial."""
		super(Boss, self).__init__()
		self.screen = screen
		self.ai_settings = ai_settings
		self.sound = sound
		
		#Carrega a imagem do alienígena e define seu atributo rect
		self.image = ai_settings.boss_img
		self.rect = self.image.get_rect()
		
		#Inicia cada novo alienígena próximo ao lado esquerdo
		#e parte superior da tela
		self.rect.x = self.rect.width
		self.rect.y = self.rect.height
		
		#Armazena a posição exata do alienígena
		self.x = float(self.rect.x)
		
		#Armazena a quantidade de alienígenas na tela
		self.count_alien = 0
		
		#Bullet Group
		self.bullets = Group()
		
		#Armazena bullets permitidos
		self.bullets_allowed = 2
		
		#Define qual a quantidade de projéteis suporta
		self.bullet_damage = 0
		
	def blitme(self):
		"""Desenha o alienígena em sua posição atual."""
		self.screen.blit(self.image, self.rect)
		self.count_alien += 1

	def draw_alien(self):
		"""Desenha o alienígena na tela."""
		pygame.draw.rect(self.screen, self.color, self.rect)

	def update(self):
		"""Move o alienígena para a direita."""
		self.x += (self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction)
		self.rect.x = self.x

	def check_edges(self):
		"""Devolve True se o alienígena estiver em uma das bordas da tela."""
		screen_rect = self.screen.get_rect()
		if self.rect.right >= screen_rect.right:
			return True
		elif self.rect.left <= 0 :
			return True
			
	def change_image(self, image=None):
		"""Troca a imagem do alien por explosão se atingido."""
		if not image:
			image = self.ai_settings.explosion
			self.sound.track_explosion.play(loops=0)
		image_rect = image.get_rect()
		image_rect.center = self.rect.center
		self.screen.blit(image, image_rect)

	def fire_bullet(self):
		"""Dispara um projétil se o limite ainda não foi alcançado."""
		if len(self.bullets) < self.ai_settings.bullets_allowed:
			self.sound.track_imp_laser.play(loops=0)
			new_bullet = Bullet2(self.ai_settings, self.screen, self.rect)
			self.bullets.add(new_bullet)
