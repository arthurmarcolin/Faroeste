import os
import pygame

pygame.init()
tamanho = (1000,700)
cowboyTamanho = (110, 100)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho )
pygame.display.set_caption("Velho Oeste")
branco = (255,255,255)
preto = (0, 0 ,0 )
cowboy = pygame.image.load("recursos/cowboy.png")
cabecaZumbi = pygame.image.load("recursos/cabeçaZumbi.png")
fundoInicio = pygame.image.load("recursos/fundoInicio.png")
fundo = pygame.image.load("recursos/fundo.png")
icone = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
nuvem = pygame.image.load("recursos/nuvem.png")
projetil = pygame.image.load("recursos/projetil.png")
zumbi = pygame.image.load("recursos/Zumbi.png")
zumbi2 =pygame.image.load("recursos/Zumbi2.png")
musicaInicio = pygame.mixer.music.load("recursos/musicaInicio.mp3")
musicaJogo = pygame.mixer.music.load("recursos/musicaJogo.mp3")
somTiro = pygame.mixer.Sound("recursos/somTiro.mp3")
somZumbi = pygame.mixer.Sound("recursos/somZumbi1.mp3")
somZumbi2 = pygame.mixer.Sound("recursos/somZumbi2.mp3")
fonteInicio = pygame.font.SysFont("lucidaconsole",18)
fonteTitulo = pygame.font.Font("recursos/FonteInicio.ttf")

posicaoXCowboy = 420
posicaoYCowboy = 600
movimentoXCowboy = 0
redimencaoCowboy = pygame.transform.smoothscale(cowboy, cowboyTamanho)

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            quit()
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
            movimentoXCowboy = 7
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
            movimentoXCowboy = -7
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
            movimentoXCowboy = 0
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
            movimentoXCowboy = 0
    
    posicaoXCowboy = posicaoXCowboy + movimentoXCowboy                    
            
    if posicaoXCowboy < 150 :
        posicaoXCowboy = 150
    elif posicaoXCowboy > 670:
        posicaoXCowboy = 670

    tela.blit(fundo, (0,0)) 
    tela.blit( redimencaoCowboy, (posicaoXCowboy, posicaoYCowboy) )      
            
    pygame.display.update()
    relogio.tick(60)