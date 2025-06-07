import os
import pygame
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import escreverDados
from recursos.funcoes import aguarde
import json

inicializarBancoDeDados()
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
fonteTitulo = pygame.font.Font("recursos/fonteTitulo.ttf")

def jogar():
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


def start():     
    larguraBotaoStart = 150
    alturaBotaoStart  = 40
    
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

        startBotao = pygame.draw.rect(tela, branco, (10,10, larguraBotaoStart, alturaBotaoStart), border_radius=15)
        startTexto = fonteInicio.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (18,20))
        
        pygame.display.update()
        relogio.tick(60)
start()
