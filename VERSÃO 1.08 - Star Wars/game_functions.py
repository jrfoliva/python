import sys, pygame, json
from alien import Alien
from boss import Boss
from time import sleep
from random import randint
import pygame.font
from pygame.sprite import Group

def check_keydown_events(event, ai_settings, screen, stats, ship,
	sound):
	"""Responde a pressionamentos de tecla."""
	pused = False
	if event.key == pygame.K_RIGHT:
		ship.moving_right = True
	elif event.key == pygame.K_LEFT:
		ship.moving_left = True
	elif event.key == pygame.K_UP:
		ship.moving_up = True
	elif event.key == pygame.K_DOWN:
		ship.moving_down = True
	elif event.key == pygame.K_SPACE:
		ship.fire_bullet()
	elif event.key == pygame.K_d:
		sound.track_darth.play(loops=0)
	elif event.key == pygame.K_r:
		sound.track_r2d2.play(loops=0)
	elif event.key == pygame.K_c:
		sound.track_chewbacca.play(loops=0)				
	elif event.key == pygame.K_p:
		paused = True
		call_pause(paused, sound)
	elif event.key == pygame.K_q:
		high_score = get_stored_number()
		if stats.high_score > high_score:
			store_high_score(stats)
		sys.exit()
		
def call_pause(paused, sound):
	"""Função para controle do pause."""
	sound.track_combat.stop()
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p:
					paused = False
					sound.track_combat.play(loops=-1)
					break
				else:
					paused = True
					pygame.time.wait(100)				
						
def check_keyup_events(event, ship):
	"""Responde as solturas das teclas."""
	if event.key == pygame.K_RIGHT:
		ship.moving_right = False
	elif event.key == pygame.K_LEFT:
		ship.moving_left = False
	
def check_play_button(ai_settings, screen, stats, sb, ship, aliens,
	play_button, mouse_x, mouse_y, sound):
	"""Inicia um jogo quando um jogador clicar em play."""
	button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
	if button_clicked and not stats.game_active:
		pygame.mouse.set_visible(False) #Desabilita mouse sobre o jogo
		#Reinicia os dados estatísticos do jogo
		ai_settings.initialize_dynamic_settings()
		ship.bullet_damage = 0 #Zera painel de danos da ship
		stats.reset_stats()
		stats.game_active = True
		#Reinicia as imagens do painel de pontuação e som
		sound.track_main.stop()
		sound.track_combat.play(loops=-1)
		sb.prep_score()
		sb.prep_high_score()
		sb.prep_level()
		sb.prep_ships()
		ship.image = ai_settings.ship_img
		#Limpa bullets da tela
		clear_bullets_screen(ship, aliens)
		#Cria uma nova frota e centraliza a ship
		create_fleet(ai_settings, screen, ship, aliens, sound, stats)
		ship.center_ship()

def clear_bullets_screen(ship, aliens):
	"""Limpa a tela após fim de jogo."""
	#Limpa bullets de ship da tela
	ship.bullets.empty()

	#Limpa bullets de aliens da tela
	for alien in aliens.sprites():
		alien.bullets.empty()
			
def get_stored_number():
	"""Tenta recuperar o número armazenado no arquivo."""
	try:
		with open('record.json') as f_obj:
			number = json.load(f_obj)
	except FileNotFoundError:
		return 0
	else:
		return number

def store_high_score(stats):
	"""Armazena a pontuação recorde em arquivo."""
	with open('record.json', 'w') as f_obj:
		json.dump(stats.high_score, f_obj)		
		
def check_events(ai_settings, stats, screen, sb, ship, aliens,
	play_button, sound):
	"""Responde a eventos de pressionamentos de teclas e de mouse."""
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			high_score = get_stored_number()
			if stats.high_score > high_score:
				store_high_score(stats)
			sys.exit()
		elif event.type == pygame.MOUSEBUTTONDOWN:
			mouse_x, mouse_y = pygame.mouse.get_pos()
			#Verifica o botão play
			check_play_button(ai_settings, screen, stats, sb, ship,
			 aliens, play_button, mouse_x, mouse_y, sound)			
		elif event.type == pygame.KEYDOWN:
			check_keydown_events(event, ai_settings, screen, stats,
			 ship, sound)
		elif event.type == pygame.KEYUP:
			check_keyup_events(event, ship)
			
def update_screen(ai_settings, stats, screen, sb, ship, aliens,
	play_button):
	"""Atualiza as imagens na tela e alterna para nova tela."""
	
	#Redesenha a tela a cada passagem pelo laço
	screen.blit(ai_settings.image, ai_settings.img_coord)
	
	#Redesenha todos os projéteis atrás da espaçonave e dos alienígenas
	for bullet in ship.bullets.sprites():
		bullet.draw_bullet()	
	
	for alien in aliens.sprites():
		for bullet in alien.bullets.sprites():
			bullet.draw_bullet()
	
	#Chama o método que desenha a espaçonave	
	ship.blitme()
	aliens.draw(screen)
	
	#Desenha a informações sobre as pontuações
	sb.show_score()
	#Desenha o status de danos da ship
	sb.draw_status_damage(900, ship.bullet_damage)
	
	#Checa rota entre projétil e alien e desenha graf. danos alien
	check_route_bullet_alien(screen, sb, ship, aliens)
			
	#Desenha o botão play se o jogo estiver inativo
	if not stats.game_active:
		play_button.draw_button()
		
	#Deixa a tela mais recente visível
	pygame.display.flip()
	

def check_route_bullet_alien(screen, sb, ship, aliens):
	"""Checa rota de colisão entre projétil e alien, para
	desenhar gráfico de dano."""
	for alien in aliens.sprites():
		for bullet in ship.bullets.sprites():
			if bullet.rect.top - alien.rect.bottom <= 5 and bullet.rect.top - alien.rect.bottom > 0:
				sb.draw_status_damage(300, alien.bullet_damage)
				break
		
def check_bullet_alien_collisions(ai_settings, screen, stats, ship, sb,
	aliens, sound):
	"""Verifica se alien foi atingido por bullet."""
	# Em caso afirmativo, livra-se do projétil e do alienígena
	for bullet in ship.bullets.sprites():
		for alien in aliens.sprites():
			collision = pygame.sprite.collide_rect(alien, bullet)
			if collision:
				alien.bullet_damage += 1				
				stats.score += ai_settings.alien_points
				sb.prep_score()
				sb.prep_high_score()				
				sb.show_score()
				ship.bullets.remove(bullet)
				if alien.bullet_damage == ai_settings.bullet_damage:
					alien.change_image()
					aliens.remove(alien)
					count = 0
				else:
					alien.change_image(image=ai_settings.short_explosion)
				pygame.display.flip()
				pygame.time.delay(5)				
		check_high_score(stats, sb)
	if len(aliens) == 0 :
		clear_bullets_screen(ship, aliens) #Destrói projéteis existentes.
		show_message_screen(screen)
		#Aumenta o nível 
		if stats.level % 3 == 0:
			stats.ships_left += 1
			show_fast_message(screen, sound)
			sb.prep_ships()
			ai_settings.bullets_screen_limit += 1
		if stats.level in ai_settings.decrease_level_list:
			#Volta as velocidades normais do jogo
			ai_settings.decrease_speed()
		else:
			#Aumenta a velocidade do jogo e cria uma nova frota
			ai_settings.increase_speed()
		stats.level += 1
		sb.prep_level()
		create_fleet(ai_settings, screen, ship, aliens, sound, stats)
		ship.center_ship()
		ship.bullet_damage = 0
	
def check_bullet_ship_collision(ai_settings, screen, stats, ship, sb,
	aliens, sound):
	"""Verifica se houve colisão entre bullet alien contra a ship."""
	for alien in aliens.sprites():
		for bullet in alien.bullets.sprites():
			collision = pygame.sprite.collide_rect(ship, bullet)
			if collision:
				ship.bullet_damage += 1
				if ship.bullet_damage == ai_settings.ship_bullet_damage:
					alien.bullets.remove(bullet)
					ship_hit(ai_settings, stats, screen, sb, ship, aliens, sound)
				else:
					alien.bullets.remove(bullet)
					ship.change_image(image=ai_settings.short_explosion)
					pygame.display.flip()
					pygame.time.delay(5)
	
def check_bullets_collision(ship, aliens):
	"""Checa colisão entre bullets."""
	for bullet_ship in ship.bullets.sprites():
		for alien in aliens.sprites():
			for bullet_alien in alien.bullets.sprites():
				collision = pygame.sprite.collide_rect(bullet_alien, bullet_ship)
				if collision:
					alien.bullets.remove(bullet_alien)
					ship.bullets.remove(bullet_ship)

def update_bullets(ai_settings, screen, stats, ship, sb, aliens, sound):
	"""Atualiza a posição dos projéteis e se livra dos projéteis
		antigos."""
	# Atualiza as posições dos projéteis
	ship.bullets.update()
	#Remove os projéteis que ultrapassam a tela do jogo, para
	#não ocupar memória desnecessáriamente.
	screen_rect = screen.get_rect()
	for bullet in ship.bullets.copy():
		if bullet.rect.bottom <= screen_rect.top + 100:
			ship.bullets.remove(bullet)
	check_bullet_alien_collisions(ai_settings, screen, stats, ship, sb,
	 aliens, sound)
	 
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		for bullet in alien.bullets.copy():
			alien.bullets.update()
			if bullet.rect.bottom >= screen_rect.bottom:
				alien.bullets.remove(bullet)
	
	check_bullet_ship_collision(ai_settings, screen, stats, ship, sb,
	aliens, sound)
	check_bullets_collision(ship, aliens)
				
def get_number_aliens_x(ai_settings, alien_width):
	"""Determina o número de alienígena que cabem em uma linha."""
	available_space_x = ai_settings.screen_width - 2 * alien_width
	number_aliens_x = int(available_space_x / (2 * alien_width))
	return number_aliens_x

def create_fleet(ai_settings, screen, ship, aliens, sound, stats):
	"""Cria uma frota completa de alienígenas."""
	# Cria um alienígena e calcula o número de alienígenas em uma linha
	# O espaçamento entre os alienígenas é igual à largura de um alienígena
	if stats.level %ai_settings.boss_level == 0:
		alien = Boss(ai_settings, screen, sound)
		ai_settings.initialize_boss_settings()
		sound.track_darth.play(loops=1)
	else:
		alien = Alien(ai_settings, screen, sound)
	number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
	number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
		
	#cria a primeira linha de alienígenas
	for row_number in range(number_rows):
		for alien_number in range(number_aliens_x):
			#Cria um alienígena e o posiciona na tela
			create_alien(ai_settings, screen, aliens, alien_number, row_number, sound, stats)

def get_number_rows(ai_settings, ship_height, alien_height):
	"""Determina o número de linha com alienígenas que cabem na tela."""
	available_space_y = (ai_settings.screen_height -(3 * alien_height) - ship_height)
	number_rows = int(available_space_y / (2 * alien_height))
	return number_rows

def create_alien(ai_settings, screen, aliens, alien_number, row_number, sound, stats):
	"""Cria um alienígena e o posiciona na tela."""
	if stats.level %ai_settings.boss_level == 0:
		alien = Boss(ai_settings, screen, sound)
	else:
		alien = Alien(ai_settings, screen, sound)
	alien_width = alien.rect.width
	alien.x = alien_width + 2 * alien_width * alien_number
	alien.rect.x = alien.x
	alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
	aliens.add(alien)
	
def change_fleet_direction(ai_settings, aliens):
	"""Faz toda sua froata descer e mudar de direção."""
	for alien in aliens.sprites():
		alien.rect.y += ai_settings.fleet_drop_speed
	ai_settings.fleet_direction *= -1
	
def check_fleet_edges(ai_settings, aliens):
	"""Responde apropriadamente se um alienígena alcançou uma das bordas."""
	for alien in aliens.sprites():
		if alien.check_edges():
			change_fleet_direction(ai_settings, aliens)
			break

def alien_fire_bullet(ai_settings, stats, aliens):
	"""Dispara bullet dos aliens a partir do level 2."""
	if stats.level > 1:
		count_bullets = 0
		for alien in aliens.sprites():
			count_bullets += len(alien.bullets)
		if count_bullets < ai_settings.bullets_screen_limit:
			rand = randint(0, len(aliens)-1)
			alienlist = aliens.sprites()
			alien = alienlist[rand]
			if len(alien.bullets) < alien.bullets_allowed:
				alien.fire_bullet()
	
def check_alien_ship_collision(ai_settings, stats, screen, sb, ship, aliens,
	sound):
	"""Verifica colisão entre ship e aliens."""
	for alien in aliens.sprites():
		if pygame.sprite.collide_rect(alien, ship):
			alien.change_image()
			ship.bullet_damage = 3
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, sound)
			
def update_aliens(ai_settings, stats, screen, sb, ship, aliens, sound):
	"""Atualiza a posição de todos os alienígenas da froata;
	verifica aliens na bordas, e atualiza posição de cada.
	"""
	check_fleet_edges(ai_settings, aliens)
	#Verifica se alien chegou na parte inferior da tela
	check_alien_screen_bottom(ai_settings, stats, screen, sb, ship, aliens, sound)
	aliens.update()
	if stats.game_active: 
		alien_fire_bullet(ai_settings, stats, aliens)
	#Verifica se houve colisões entre alienígenas e a espaçonave
	check_alien_ship_collision(ai_settings, stats, screen, sb, ship, aliens,
	sound)
	#Verifica se alien chegaram na parte inferior da tela
	check_alien_screen_bottom(ai_settings, stats, screen, sb, ship, aliens, sound)

	
def ship_hit(ai_settings, stats, screen, sb, ship, aliens, sound):
	"""Responde ao fato de a espaçonave ter sido atingida por um
	alienígena ou bullet."""
	#Troca a image da ship e alien por explosão e atualiza estatítisca
	if stats.ships_left > 0:
		#Decrementa ships_left
		stats.ships_left -= 1
		sb.prep_ships()
		ship.change_image()#ship.image = ai_settings.explosion
		show_message_screen(screen, "Tente novamente!")
		ship.change_image(image=ai_settings.ship_img)#ship.image = ai_settings.ship_img
		#Limpa bullets e aliens da tela
		aliens.empty() 
		clear_bullets_screen(ship, aliens)	
		#Cria uma nova frota e centraliza a ship
		create_fleet(ai_settings, screen, ship, aliens, sound, stats)
		ship.center_ship()
		ship.bullet_damage = 0
	elif stats.ships_left == 0:
		sb.prep_ships()
		ship.change_image()
		sound.track_combat.stop()
		show_message_screen(screen, 'Fim de jogo!')
		clear_bullets_screen(ship, aliens)
		aliens.empty()
		sound.track_main.play(loops=1)
		stats.game_active = False
		pygame.mouse.set_visible(True)

def check_alien_screen_bottom(ai_settings, stats, screen, sb, ship, aliens, sound):
	"""Verifica se a frota está chegando na parte inferior da tela."""
	screen_rect = screen.get_rect()
	for alien in aliens.sprites():
		if alien.rect.bottom > screen_rect.bottom - 5:
			ship_hit(ai_settings, stats, screen, sb, ship, aliens, sound)
			break
	
def check_high_score(stats, sb):
	"""Verifica se há uma nova pontuação máxima."""
	if stats.score > stats.high_score:
		stats.high_score = stats.score
		sb.prep_high_score()
		
def show_message_screen(screen, msg='Missão cumprida!'):
	"""A cada fim de combate apresenta mensagem."""
	font = pygame.font.SysFont('calibri', 48, bold=True, italic=False)
	msg_image = font.render(msg, True, (255,255,255),
		(0,255,0))
	msg_image_rect = msg_image.get_rect()
	screen_rect = screen.get_rect()
	msg_image_rect.center = screen_rect.center
	screen.blit(msg_image, msg_image_rect)
	pygame.display.flip()
	pygame.time.delay(3000)

def show_fast_message(screen, sound, msg='Conquista: 1 Nave Extra!'):
	"""A cada fim de combate apresenta mensagem."""
	font = pygame.font.SysFont('calibri', 48, bold=True, italic=True)
	msg_image = font.render(msg, True, (0,0,255),
		(255,255,0))
	msg_image_rect = msg_image.get_rect()
	screen_rect = screen.get_rect()
	msg_image_rect.center = screen_rect.center
	screen.blit(msg_image, msg_image_rect)
	pygame.display.flip()
	pygame.time.delay(1500)
	sound.track_r2d2.play(loops=0)
