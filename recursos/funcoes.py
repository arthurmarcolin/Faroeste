import os, time
import json
from datetime import datetime
import pygame
tamanho = (1000, 700)
branco = (255,255,255)
tela = pygame.display.set_mode( tamanho )
preto = (0, 0 ,0 )
fundo = pygame.image.load("recursos/fundo.png")
cowboy = pygame.transform.smoothscale(pygame.image.load("recursos/cowboy.png"), (110, 100))
def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    
    try:
        banco = open("base.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("base.atitus","w")
    
def escreverDados(nome, pontos):
    
    banco = open("base.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
    data_br = datetime.now().strftime("%d/%m/%Y")
    dadosDict[nome] = (pontos, data_br)
    
    banco = open("base.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
def contagemRegressiva():
    fonte_contagem = pygame.font.SysFont("comicsans",100)
    for i in range(3, 0, -1):
        tela.blit(fundo,(0,0))
        tela.blit(cowboy, (420, 600))
        texto = fonte_contagem.render(str(i), True, preto)
        
        texto_rect = texto.get_rect(center=(tamanho[0]//2, tamanho[1]//2))
        tela.blit(texto, texto_rect)
        pygame.display.flip()
        pygame.time.delay(1000)  
    
    tela.blit(fundo,(0,0))
    tela.blit(cowboy, (420, 600))
    texto = fonte_contagem.render("Começou!", True, preto)
    texto_rect = texto.get_rect(center=(tamanho[0]//2, tamanho[1]//2))
    tela.blit(texto, texto_rect)
    pygame.display.flip()
    pygame.time.delay(1000)