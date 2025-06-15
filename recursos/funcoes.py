import time, pygame, pyttsx3
engine=pyttsx3.init()
tamanho = (1000, 700)
branco = (255,255,255)
preto = (0, 0 ,0 )
tela = pygame.display.set_mode( tamanho )
fundo = pygame.image.load("recursos/fundo.png")
cowboy = pygame.transform.smoothscale(pygame.image.load("recursos/cowboy.png"), (90, 80))
    
def aguarde(segundos):
    time.sleep(segundos)
    
def contagemRegressiva():
    fonteContagem = pygame.font.SysFont("comicsans",100)
    for i in range(3, 0, -1):
        tela.blit(fundo,(0,0))
        tela.blit(cowboy, (420, 600))
        texto = fonteContagem.render(str(i), True, preto)
        
        textoRect = texto.get_rect(center=(tamanho[0]//2, tamanho[1]//2))
        tela.blit(texto, textoRect)
        pygame.display.flip()
        pygame.time.delay(1000)  
    
    tela.blit(fundo,(0,0))
    tela.blit(cowboy, (420, 600))
    texto = fonteContagem.render("Começou!", True, preto)
    textoRect = texto.get_rect(center=(tamanho[0]//2, tamanho[1]//2))
    tela.blit(texto, textoRect)
    pygame.display.flip()
    pygame.time.delay(1000)

def falarTexto(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()