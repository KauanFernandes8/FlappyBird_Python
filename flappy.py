import pygame 
from pygame.locals import *

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 800
SPEED = 10
GRAVITY = 1
VELOCIDADE_JOGO = 10

#chão
LARGURA_CHAO = 2* SCREEN_WIDTH
ALTURA_CHAO = 100   

#canos
LARGURA_CANO = 80
ALTURA_CANO = 500
CANO_TAMANHO = 80

class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.MovimentoPassaro = [pygame.image.load('asaCentro.png').convert_alpha(),#vetor que simula o movimento do passaro 
                                pygame.image.load('asaAlta.png').convert_alpha(), #baseado na troca rapida de imagens
                                pygame.image.load('asaBaixa.png').convert_alpha()]

        self.velocidade = SPEED #velocidade jogo

        self.atualizaImage = 0 #variavel que controla o "movimento"

        self.image = pygame.image.load('asaCentro.png').convert_alpha() #recortando a imagem
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH/2
        self.rect[1] = SCREEN_HEIGHT/2
    
    def update(self):
        
        self.atualizaImage = (self.atualizaImage+1) %3#metodo responsavel por fazer acontecer o bater das asas
        self.image = self.MovimentoPassaro[self.atualizaImage]

        self.velocidade += GRAVITY

        #atualiando altura do passarinho
        self.rect[1] += self.velocidade

    def pulo(self): 
        self.velocidade = -SPEED

class Cano(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('cano_grande.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(LARGURA_CANO, ALTURA_CANO))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] =- (self.rect[3] -ysize)
        else:
                self.rect[1] = SCREEN_HEIGHT - ysize


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

FUNDO = pygame.image.load('noite.png')#plano de fundo
FUNDO = pygame.transform.scale(FUNDO,(SCREEN_WIDTH, SCREEN_HEIGHT))#enquadrando a imagem ao tamanho da tela

bird_group =pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

clock = pygame.time.Clock() #vai controlar a velocidade do bater de asas

while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                bird.pulo()

    screen.blit(FUNDO, (0, 0))
    
    bird_group.update()

    bird_group.draw(screen)

    pygame.display.update()