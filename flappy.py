from turtle import speed
import pygame 
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SPEED = 1000

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.MovimentoPassaro = [pygame.image.load('asaCentro.png').convert_alpha(),#vetor que simula o movimento do passaro 
                                pygame.image.load('asaAlta.png').convert_alpha(), #baseado na troca rapida de imagens
                                pygame.image.load('asaBaixa.png').convert_alpha()]

        self.atualizaImage = 0 #variavel que controla o "movimento"
        self.image = pygame.image.load('asaCentro.png').convert_alpha() #recortando a imagem

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH/2
        self.rect[1] = SCREEN_HEIGHT/2
    
    def update(self):
        self.atualizaImage = (self.atualizaImage+1) %3#metodo responsavel por fazer acontecer o bater das asas
        self.image = self.MovimentoPassaro[self.atualizaImage]

        #atualiando altura do passarinho
        #self.rect[1] += SPEED

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FUNDO = pygame.image.load('noite.png')#plano de fundo
FUNDO = pygame.transform.scale(FUNDO,(SCREEN_WIDTH, SCREEN_HEIGHT))#enquadrando a imagem ao tamanho da tela

bird_group =pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

clock = pygame.time.Clock() #vai controlar a velocidade do bater de asas

while True:
    clock.tick()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

    screen.blit(FUNDO, (0, 0))
    
    bird_group.update()

    bird_group.draw(screen)

    pygame.display.update()