import pygame.mixer

class GameSounds():
	def __init__(self, ai_settings):
		"""Inicializa os atributos de som do jogo."""
		self.main = ai_settings.main
		self.combat = ai_settings.combat
		self.laser = ai_settings.laser
		self.imp_laser = ai_settings.imp_laser
		self.darth = ai_settings.darth
		self.r2d2 = ai_settings.r2d2
		self.chewbacca = ai_settings.chewbacca
		self.explosion = ai_settings.explosion_sound
		#Inicializa mixer
		mixer = pygame.mixer
		mixer.init()
		
		#Inicia a trilha coma o arquivo wav
		self.track_main = mixer.Sound(self.main)
		self.track_combat = mixer.Sound(self.combat)
		self.track_laser = mixer.Sound(self.laser)
		self.track_imp_laser = mixer.Sound(self.imp_laser)	
		self.track_darth = mixer.Sound(self.darth)
		self.track_r2d2 = mixer.Sound(self.r2d2)
		self.track_chewbacca = mixer.Sound(self.chewbacca)
		self.track_explosion = mixer.Sound(self.explosion)
