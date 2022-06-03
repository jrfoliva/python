import pygame.font
class Scoreboard():
	"""Uma classe para mostrar informações sobre pontuação."""
	
	def __init__(self, ai_settings, stats, screen):
		"""Inicializa os atributos da pontuação."""
		self.screen = screen
		self.screen_rect = screen.get_rect()
		self.ai_settings = ai_settings
		self.stats = stats
		
		#Configuração de fonte para as informações de pontuação
		self.text_color = (0, 255, 0)
		self.font = pygame.font.SysFont('comicsansms', 22, bold=True, italic=False)
		
		#Prepara as imagens para as pontuações iniciais
		self.prep_score()
		self.prep_high_score()
		self.prep_level()
		self.prep_ships()
		
	def prep_score(self):
		"""Transforma a pontuação em uma imagem renderizada."""
		rounded_score =  int(round(self.stats.score, -1))
		score_str = "Pontos: {:,}".format(rounded_score)
		self.score_image = self.font.render(score_str, True,
			self.text_color,(0,0,0))
	
		#Exibe a pontuação na parte superior esquerdo da tela
		self.score_rect = self.score_image.get_rect()
		self.score_rect.right = self.screen_rect.right - 5
		self.score_rect.top = self.screen_rect.top + 2
		
		#Exibe comandos no lado superior esquerdo
		self.comands_img = self.font.render("Para sair 'Q'", True,
		 (255,255,255), (0,0,0))	
		self.comands_img_rect = self.comands_img.get_rect()
		self.comands_img_rect.left = self.screen_rect.left + 5
		self.comands_img_rect.top = self.screen_rect.top + 2 
		
		#Exibe comando pause ou continue
		self.pause_img = self.font.render("Pausar/Continuar 'P'", True,
		 (255,255,255), (0,0,0))	
		self.pause_img_rect = self.pause_img.get_rect()
		self.pause_img_rect.left = self.screen_rect.left + 5
		self.pause_img_rect.top = self.comands_img_rect.bottom + 5 

	def prep_high_score(self):
		"""Transforma a maior pontuação em uma imagem renderizada."""
		high_score = int(round(self.stats.high_score, -1))
		high_score_str = "Recorde: {:,}".format(high_score)
		self.high_score_image = self.font.render(high_score_str, True,
			self.text_color, (0,0,0))
		
		#Centraliza a pontuação máxima no top da tela
		self.high_score_rect = self.high_score_image.get_rect()
		self.high_score_rect.centerx = self.screen_rect.centerx
		self.high_score_rect.top = self.score_rect.top

	def prep_level(self):
		"""Transforma o nível em uma imagem renderizada."""
		self.level_image = self.font.render("Nível: "+str(self.stats.level),
		True, self.text_color, (0,0,0))
		
		#Posiciona o nível abaixo da pontuação
		self.level_rect = self.level_image.get_rect()
		self.level_rect.right = self.score_rect.right
		self.level_rect.top = self.score_rect.bottom + 5	
		
	def prep_ships(self):
		"""Mostra quantas naves restam."""
		self.ship_left_image = self.font.render("Nave: " + str
			(self.stats.ships_left), True, self.text_color, (0,0,0))
		
		#Posiciona abaixo de level
		self.ship_left_rect = self.ship_left_image.get_rect()
		self.ship_left_rect.right = self.level_rect.right
		self.ship_left_rect.top = self.level_rect.bottom + 5
		
	def draw_status_damage(self, col, damage=0):
		"""Exibe 3 rectangulos indicando danos na ship."""
		width, height = 100, 20
		self.col, lin = col, 15
		green = (0,255,0)
		yellow = (255,255,0)
		red = (255,0,0)
		white = (255,255,255)
		pygame.draw.rect(self.screen, white, [self.col-2, lin-2, width+4, height+4],3)
		if damage == 0:
			pygame.draw.rect(self.screen, green, [self.col, lin, width, height]) 
		elif damage == 1:
			pygame.draw.rect(self.screen, yellow, [self.col, lin, (width/2), height]) 
		elif damage == 2:
			pygame.draw.rect(self.screen, red, [self.col, lin, (width/3), height])
		elif damage == 3:
			pygame.draw.rect(self.screen, red, [self.col, lin, (width/4), height])
		elif damage == 4:
			pygame.draw.rect(self.screen, red, [self.col, lin, (width/5), height])
		else:
			pygame.draw.rect(self.screen, red, [self.col-2, lin-2, width+4, height+4],3)
			
	def show_score(self):
		"""Exibe a pontuação na tela."""
		self.screen.blit(self.score_image, self.score_rect)
		self.screen.blit(self.comands_img, self.comands_img_rect)
		self.screen.blit(self.pause_img, self.pause_img_rect)
		self.screen.blit(self.high_score_image, self.high_score_rect)
		self.screen.blit(self.level_image, self.level_rect)
		self.screen.blit(self.ship_left_image, self.ship_left_rect)
