import pygame 
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800

class Passaro(pygame.sprite.Sprite):
    
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FUNDO = pygame.image.load('fundo3.png')#plano de fundo
FUNDO = pygame.transform.scale(FUNDO,(SCREEN_WIDTH, SCREEN_HEIGHT))#enquadrando a imagem ao tamanho da tela

while True:

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
    screen.blit(FUNDO, (0, 0))
    
    pygame.display.update()