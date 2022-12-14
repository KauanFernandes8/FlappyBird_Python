import pygame
import random
from pygame.locals import *
import os
import time
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(17, GPIO.OUT)
#GPIO.cleanup()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 800
SPEED = 10
GRAVIDADE = 1
VELOCIDADE_JOGO = 5

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 200

BLACK = (0, 0, 0)


class Passaro(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.MovimentoPassaro = [pygame.image.load('bluebird-upflap.png').convert_alpha(),
                       pygame.image.load(
                           'bluebird-midflap.png').convert_alpha(),
                       pygame.image.load('bluebird-downflap.png').convert_alpha()]

        self.velocidade = SPEED #velocidade passaro

        self.atualizaImage = 0#variavel que controla o "movimento"

        self.image = pygame.image.load('bluebird-upflap.png').convert_alpha()#recortando a imagem
        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 2 #determinando tamanho jogo
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.atualizaImage = (self.atualizaImage + 1) % 3 #metodo responsavel por fazer acontecer o bater das asas
        self.image = self.MovimentoPassaro[self.atualizaImage]

        self.velocidade += GRAVIDADE
        self.rect[1] += self.velocidade

    def pulo(self):
        self.velocidade = -SPEED


class Cano(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('pipe-red.png').convert_alpha()
        # self.image = pygame.image.load('./pipe-red.png').convert_alpha() #para rodar no raspberry
        self.image = pygame.transform.scale(
            self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= VELOCIDADE_JOGO


class Chao(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('base.png').convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= VELOCIDADE_JOGO


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Cano(False, xpos, size)
    pipe_inverted = Cano(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return (pipe, pipe_inverted)


pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

BACKGROUND = pygame.image.load('background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_group = pygame.sprite.Group()
passarinho = Passaro()
bird_group.add(passarinho)

chao_group = pygame.sprite.Group()
for i in range(2):
    ground = Chao(GROUND_WIDTH * i)
    chao_group.add(ground)

cano_group = pygame.sprite.Group()
for i in range(2):
    canos = get_random_pipes(SCREEN_WIDTH * i + 800)
    cano_group.add(canos[0])
    cano_group.add(canos[1])


clock = pygame.time.Clock()

pontuacao = 0
while True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                passarinho.velocidade = -SPEED
                pontuacao += 1
                GPIO.output(17, GPIO.HIGH)
                time.sleep(0.2)
                GPIO.output(17, GPIO.LOW)

    screen.blit(BACKGROUND, (0, 0))
    BACKGROUND = pygame.image.load('background-day.png')
    BACKGROUND = pygame.transform.scale(
        BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))

    if is_off_screen(chao_group.sprites()[0]):
        chao_group.remove(chao_group.sprites()[0])

        new_ground = Chao(GROUND_WIDTH - 20)
        chao_group.add(new_ground)

    if is_off_screen(cano_group.sprites()[0]):
        cano_group.remove(cano_group.sprites()[0])
        cano_group.remove(cano_group.sprites()[0])

        canos = get_random_pipes(SCREEN_WIDTH * 2)

        cano_group.add(canos[0])
        cano_group.add(canos[1])

    bird_group.update()
    chao_group.update()
    cano_group.update()

    bird_group.draw(screen)
    cano_group.draw(screen)
    chao_group.draw(screen)

    pygame.display.update()

    # placar de pontuação
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    text_surface = my_font.render(
        "Pontos: " + str(pontuacao), False, (0, 0, 0))
    BACKGROUND.blit(text_surface, (0, 0))

    if (pygame.sprite.groupcollide(bird_group, chao_group, False, False, pygame.sprite.collide_mask) or
       pygame.sprite.groupcollide(bird_group, cano_group, False, False, pygame.sprite.collide_mask)):
        # Game over

        pygame.quit()
        os.system('menu.py')
        # os.system('python3 menu.py') #para rodar no raspber
