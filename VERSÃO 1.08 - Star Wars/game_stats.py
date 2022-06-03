import json
class GameStats():
	"""Armazena os dados estatísticos do jogo."""
	def __init__(self, ai_settings):
		"""Inicializa os dados estatísticos."""
		self.ai_settings = ai_settings
		#Armazena a maior pontuação gravado no arquivo
		self.get_stored_high_score() 
		#Inicia o jogo em um estado inativo
		self.game_active = False
		self.reset_stats()
		
	def reset_stats(self):
		"""Inicializam os dados estatísticos que podem mudar durante
		 o jogo."""
		self.ships_left = self.ai_settings.ship_limit
		self.score = 0
		self.level = 1		
					
	def get_stored_high_score(self):
		"""Tenta recuperar o número armazenado no arquivo."""
		try:
			with open('record.json') as f_obj:
				self.high_score = json.load(f_obj)
		except:
			#print("Algum problema com o arquivo! Corrigindo...")
			self.high_score = 0
			with open('record.json', 'w') as f_obj:
				json.dump(self.high_score, f_obj)
