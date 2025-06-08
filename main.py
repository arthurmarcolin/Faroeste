import os
import pygame
import random
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
import json

pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
cowboyTamanho = (110, 100)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho )
pygame.display.set_caption("Velho Oeste")
branco = (255,255,255)
preto = (0, 0 ,0 )
bege = (198, 129, 40)
corCaixa = (253, 193, 127)
corS = (243, 146, 85)
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
somTiro = pygame.mixer.Sound("recursos/somTiro.mp3")
somZumbi = pygame.mixer.Sound("recursos/somZumbi1.mp3")
somZumbi2 = pygame.mixer.Sound("recursos/somZumbi2.mp3")
fonteInicio = pygame.font.SysFont("comicsans",25)
fonteTitulo = pygame.font.Font("recursos/FonteInicio.ttf",150)
fonteExplicacao = pygame.font.SysFont("comicsans",18)
largura_janela = 300
altura_janela = 50
def obter_nome():
    global nome
    nome = entry_nome.get() 
    if not nome: 
        messagebox.showwarning("Aviso", "Por favor, digite seu nome!")
    else:
            
        root.destroy() 
    
root = tk.Tk()
largura_tela = root.winfo_screenwidth()
altura_tela = root.winfo_screenheight()
pos_x = (largura_tela - largura_janela) // 2
pos_y = (altura_tela - altura_janela) // 2
root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
root.title("Digite seu Nick")
root.protocol("WM_DELETE_WINDOW", obter_nome)

entry_nome = tk.Entry(root)
entry_nome.pack()

botao = tk.Button(root, text="Confirmar", command=obter_nome)
botao.pack()

root.mainloop()

def jogar():
    posicaoXCowboy = 420
    posicaoYCowboy = 600
    movimentoXCowboy = 0
    redimencaoCowboy = pygame.transform.smoothscale(cowboy, cowboyTamanho)
    pygame.mixer.music.stop()
    pygame.mixer.music.load("recursos/musicaJogo.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.play(-1)

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

def start():     
    larguraBotaoStart = 100
    alturaBotaoStart  = 35
    larguraCaixaTexto = 550
    alturaCaixaTexto = 220
    alturaS = 28
    larguraS = 20
    pygame.mixer.music.load("recursos/musicaInicio.mp3")
    pygame.mixer.music.play()
    pygame.mixer.music.play(-1)
    
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startBotao.collidepoint(evento.pos):
                    larguraBotaoStart = 147
                    alturaBotaoStart  = 37
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startBotao.collidepoint(evento.pos):
                    jogar()
                                
        tela.fill(branco)
        tela.blit(fundoInicio, (0,0) )
        caixaTexto = pygame.draw.rect(tela, corCaixa, pygame.Rect (225, 320, larguraCaixaTexto, alturaCaixaTexto), border_radius=15)
        detalheS = pygame.draw.rect(tela, corS , pygame.Rect (498, 450, larguraS, alturaS), border_radius=5)
        startBotao = pygame.draw.rect(tela, corS, (450,490, larguraBotaoStart, alturaBotaoStart), border_radius=10)
        startTitulo = fonteTitulo.render("BEM-VINDO", True, bege)
        startTexto = fonteInicio.render("Jogar", True, preto)
        playerName = fonteExplicacao.render(f"Nickname: {nome}", True, preto)
        textoExplicacao = fonteExplicacao.render("O objetivo do jogo é matar os zumbis antes que eles cheguem ao", True, preto)
        textoExplicacao2 = fonteExplicacao.render("fim da tela, se isso acontecer você perde uma vida. Você terá 5", True, preto)
        textoExplicacao3 = fonteExplicacao.render("vidas. Para movimentar o personagem use as setas Direita e Es-", True, preto)
        textoExplicacao4 = fonteExplicacao.render("querda e para atirar use a tecla S .", True, preto)
        tela.blit(textoExplicacao, (235, 360))
        tela.blit(textoExplicacao2, (235, 390))
        tela.blit(textoExplicacao3, (235, 420))
        tela.blit(textoExplicacao4, (235, 450))
        tela.blit(playerName, (440, 324))
        tela.blit(startTitulo, (265, 20))
        tela.blit(startTexto, (466, 487))

        pygame.display.update()
        relogio.tick(60)    
start()