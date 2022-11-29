import pygame 
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('aviao.jpg').convert_alpha() #recortando a imagem
        self.rect = self.image.get_rect()
        print(self.rect)
    
    def update(self):
        pass

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FUNDO = pygame.image.load('fundo3.png')#plano de fundo
FUNDO = pygame.transform.scale(FUNDO,(SCREEN_WIDTH, SCREEN_HEIGHT))#enquadrando a imagem ao tamanho da tela

bird_group =pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.blit(FUNDO, (0, 0))
    
    bird_group.update()

    bird_group.draw(screen)

    pygame.display.update()