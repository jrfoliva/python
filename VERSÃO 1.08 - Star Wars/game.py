# game.py

import pygame
import random

from pygame.locals import *
import background

class Game(object):
    
    def __init__(self, size):
        pygame.init()
        flags = DOUBLEBUF
        self.screen = pygame.display.set_mode(size, flags)
        self.screen_size = self.screen.get_size()
        
        pygame.mouse.set_visible(False)
        pygame.display.set_caption('Meu Primeiro Jogo em Python')
        
        self.run = True
        self.list = {
            'player': pygame.sprite.RenderPlain(),
            'enemy': pygame.sprite.RenderPlain(),
            'fire': pygame.sprite.RenderPlain(),
            'enemy_fire': pygame.sprite.RenderPlain(),
        }
        self.player = None
        self.background = background.Background()
    
    def update_actors(self):
        if self.background is not None:
            self.background.update()
        
        for actor in self.list.values():
            actor.update()
    
    def draw_actors(self):
        if self.background is not None:
            self.background.draw(self.screen)
        else:
            self.screen.fill(0)
        
        for actor in self.list.values():
            actor.draw(self.screen)
    
    def act_actors(self):
        pass
    
    def manage(self):
        pass
    
    def handle_events(self):
        player = self.player
        for event in pygame.event.get():
            t = event.type
            
            if t in (KEYDOWN, KEYUP):
                k = event.key
            
            if t == QUIT:
                self.run = False
            elif t == KEYDOWN and k == K_ESCAPE:
                self.run = False
            elif t == KEYUP:
                pass
    
    def loop(self):
        clock = pygame.time.Clock()
        
        while self.run:
            clock.tick(1000)
            
            self.handle_events()
            self.manage()
            
            self.act_actors()
            self.update_actors()
            self.draw_actors()
            
            pygame.display.flip()

if __name__ == '__main__':
    game = Game( (640, 480) )
    game.loop()
