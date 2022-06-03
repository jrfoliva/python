import pygame, os
from game_stats import GameStats as gs

class Settings():
	"""Classe que armazena todas as configurações do jogo
		Alien Invasion."""
	
	def __init__(self):
		"""Inicializa as configurações estáticas do jogo."""
		#Configurações da tela
		self.screen_width = 1280
		self.screen_height = 680
		
		#Configuraçao dos caminhos para carga de arquivos
		current_path = os.path.dirname(__file__)
		image_path = os.path.join(current_path, 'images')
		sounds_path = os.path.join(current_path, 'sounds')
		
		
		self.image = pygame.image.load(os.path.join(image_path, 'starofdeath.jpg'))
		self.img_coord = (0, 0)
		
		#Configura imagem de agradecimento.
		self.birthday = pygame.image.load(os.path.join(image_path, 'logo StarWars2.jpg'))
		
		#Configuração da espaçonave
		self.ship_limit = 2
		self.ship_img = pygame.image.load(os.path.join(image_path, 'nave_luke.png'))

		#Imagem de explosão
		self.explosion = pygame.image.load(os.path.join(image_path, 'explosion.png'))
		self.short_explosion = pygame.image.load(os.path.join(image_path, 'short_explosion.png'))
		
		#Configura o som do jogo
		self.main = os.path.join(sounds_path, 'starwars_theme.wav')	
		self.laser = os.path.join(sounds_path, 'ship_laser.wav')
		self.imp_laser = os.path.join(sounds_path, 'imp_laser.wav')
		self.combat = os.path.join(sounds_path, 'imperial.wav')
		self.darth = os.path.join(sounds_path, 'darth.wav')
		self.r2d2 = os.path.join(sounds_path, 'r2d2.wav')
		self.chewbacca = os.path.join(sounds_path, 'chewbacca.wav')
		self.explosion_sound = os.path.join(sounds_path,'explosion.wav')
		
		#Configuração dos projéteis
		self.bullet_width = 3
		self.bullet_height = 20
		self.bullet_color = 0, 0, 230	
		self.bullet2_color = 230, 0, 0
				
		#Configuração dos alienígenas
		self.alien_img = pygame.image.load(os.path.join(image_path, 'new_nave_rebel.png'))
		
		#configuração daa nave chefe
		self.boss_img = pygame.image.load(os.path.join(image_path, 'boss_ship.png'))
		
		#Define os níveis que deverá enfrentar os chefões
		self.boss_level = 5

		#Define uma lista onde deverá ser decrementado 
		self.decrease_level_list = [5,10,15,20,25,30,35,40,45,50]
		
		#A taxa com que a velocidade do jogo aumenta
		self.speedup_scale = 1.1 #padrão 1.1
		#A taxa com que aumenta a pontuação 
		self.score_scale = 1.2
		#A taxa com que aumenta os projéteis
		self.score_bullets = 1
		
		self.initialize_dynamic_settings()
		
		self.initialize_boss_settings()

	def initialize_dynamic_settings(self):
		"""Inicializa as configuração que mudarão durante o jogo."""
		#Padrões iniciais
		self.bullets_allowed = 3
		self.bullets2_allowed = 1
		self.bullet_damage = 1
		self.ship_bullet_damage = 3 
		self.ship_speed_factor = 3 #5
		self.bullet_speed_factor = 3 #5
		self.bullets_screen_limit = 1
		self.bullets2_allowed = 1
		self.alien_speed_factor = 2
		self.fleet_drop_speed = 5 #Padrão 5
		self.fleet_direction = 1 # = 1 representa direita; -1 esquerda
		self.alien_points = 10 #Pontuação por alien destruídos
				
	def initialize_boss_settings(self):
		"""Inicializa as configuração que mudarão durante o jogo."""
		#Padrões iniciais
		self.bullet_damage += 4 #Danos suportados pela nave chefe
		self.bullets2_allowed += 1  #Disparos permitidos
		self.alien_speed_factor = 2
		self.fleet_drop_speed = 5
		self.fleet_direction = 1 # = 1 representa direita; -1 esquerda
		#Pontuação por alien destruídos
		self.alien_points = 50
		
	def increase_speed(self):
		"""Aumenta as configurações de velocidade."""
		self.ship_speed_factor *= self.speedup_scale
		self.bullet_speed_factor *= self.speedup_scale
		self.alien_speed_factor *= self.speedup_scale
		self.alien_points = int(self.alien_points * self.score_scale)
		self.fleet_drop_speed *= self.speedup_scale

	def decrease_speed(self):
		"""Inicializa as configuração que mudarão durante o jogo."""
		#Padrões iniciais
		self.bullet_damage -= 3 #Danos suportados pela nave chefe
		self.bullets2_allowed -= 1 #Disparos permitidos
		self.alien_speed_factor *= 1.8
		self.fleet_drop_speed += 2
		self.fleet_direction = 1 # = 1 representa direita; -1 esquerda
		#Pontuação por alien destruídos
		self.alien_points = 10
