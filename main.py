import os, json, pygame, random, pyttsx3, threading
import tkinter as tk
import speech_recognition as sr
from tkinter import messagebox
from recursos.funcoes import inicializarBancoDeDados
from recursos.funcoes import contagemRegressiva
from recursos.funcoes import escreverDados
from recursos.funcoes import aguarde
from recursos.funcoes import falarTexto
engine=pyttsx3.init()
pygame.init()
inicializarBancoDeDados()
tamanho = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho )
pygame.display.set_caption("Forasteiro Maluko")
branco = (255,255,255)
preto = (0, 0 ,0 )
bege = (198, 129, 40)
corCaixa = (253, 193, 127)
corS = (243, 146, 85)
cowboy = pygame.transform.smoothscale(pygame.image.load("recursos/cowboy.png"), (110, 100))
cabecaZumbi = pygame.image.load("recursos/cabeçaZumbi.png")
fundoInicio = pygame.image.load("recursos/fundoInicio.png")
fundo = pygame.image.load("recursos/fundo.png")
icone = pygame.image.load("recursos/icone.png")
pygame.display.set_icon(icone)
nuvem = pygame.image.load("recursos/nuvem.png")
projetil = pygame.image.load("recursos/projetil.png")
Zumbi = pygame.transform.smoothscale(pygame.image.load("recursos/Zumbi.png").convert_alpha(), (60, 80))
Zumbi2 = pygame.transform.smoothscale(pygame.image.load("recursos/Zumbi2.png").convert_alpha(), (60, 80))
somTiro = pygame.mixer.Sound("recursos/somTiro.mp3")
somZumbi = pygame.mixer.Sound("recursos/somZumbi1.mp3")
somZumbi2 = pygame.mixer.Sound("recursos/somZumbi2.mp3")
fonteInicio = pygame.font.SysFont("comicsans",25)
fonteTitulo = pygame.font.Font("recursos/FonteInicio.ttf",150)
fonteExplicacao = pygame.font.SysFont("comicsans",18)
zumbisComSons = [
    (Zumbi, somZumbi),
    (Zumbi2, somZumbi2),  
]
faixasPosicaoX = [
    (424, 584), 
    (410, 598),  
    (350, 670),
    (230, 690),
]

def reconhecerFala():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            label_status.after(0, lambda: label_status.config(text="Ouvindo..."))

            audio = recognizer.listen(source, timeout=5)

            label_status.after(0, lambda: label_status.config(text="Reconhecendo..."))

            texto = recognizer.recognize_google(audio, language='pt-BR')

            entry_nome.after(0, lambda: entry_nome.insert(tk.END, texto))
            label_status.after(0, lambda: label_status.config(text="Texto adicionado!"))

        except sr.UnknownValueError:
            label_status.after(0, lambda: label_status.config(text="Não entendi o que você disse."))
        except sr.RequestError:
            label_status.after(0, lambda: label_status.config(text="Erro ao acessar o serviço de reconhecimento."))
        except sr.WaitTimeoutError:
            label_status.after(0, lambda: label_status.config(text="Tempo de escuta acabou."))


def iniciarVozEreconhecimento():
    
    falarTexto("Fale seu nickname em voz alta para começar.")
   
    reconhecerFala()

def iniciarThreadVoz():
    thread = threading.Thread(target=iniciarVozEreconhecimento)
    thread.start()

def obter_nome():
    global nome
    nome = entry_nome.get()
    if not nome:
        messagebox.showwarning("Aviso", "Por favor, diga ou digite seu nome!")
    else:
        root.destroy()

root = tk.Tk()
larguraJanela = 400
alturaJanela = 100
larguraTela = root.winfo_screenwidth()
alturaTela = root.winfo_screenheight()
pos_x = (larguraTela - larguraJanela) // 2
pos_y = (alturaTela - alturaJanela) // 2
root.geometry(f"{larguraJanela}x{alturaJanela}+{pos_x}+{pos_y}")
root.title("Diga seu Nick")
root.protocol("WM_DELETE_WINDOW", obter_nome)

entry_nome = tk.Entry(root, font=("Arial", 14))
entry_nome.pack(pady=10)

botao = tk.Button(root, text="Confirmar", command=obter_nome)
botao.pack(pady=5)

label_status = tk.Label(root, text="")
label_status.pack(pady=5)

root.after(1000, iniciarThreadVoz)

root.mainloop()

engine.say(f"Seja Bem Vindo {nome} ")
engine.runAndWait()
def jogar():
    posicaoXCowboy = 420
    posicaoYCowboy = 600
    cowboyTamanho = (110, 100)
    movimentoXCowboy = 0
    projeteis = []
    pygame.mixer.music.stop()
    pygame.mixer.music.load("recursos/musicaJogo.mp3")
    pygame.mixer.music.set_volume(0.30)
    pygame.mixer.music.play()
    pygame.mixer.music.play(-1)

    class Inimigo:
        def __init__(self):
            self.imagem, self.som = random.choice(zumbisComSons)
            self.largura = self.imagem.get_width()
            self.altura = self.imagem.get_height()
            faixa = random.choice(faixasPosicaoX)
            self.x = random.randint(faixa[0], faixa[1] - self.largura)
            self.y = random.randint(290, 420)
            self.velocidade = random.uniform(0.1, 1)
            self.som.play()

        def reaparecer(self):
            self.y += self.velocidade
            if self.y > 700:
                self.y = random.randint(250, 450)
                faixa = random.choice(faixasPosicaoX)
                self.x = random.randint(faixa[0], faixa[1] - self.largura)
                self.imagem, self.som = random.choice(zumbisComSons)
                self.som.play()

        def desenhar(self):
            tela.blit(self.imagem, (self.x, self.y))

    NUM_INIMIGOS = 2
    inimigos = [Inimigo() for _ in range(NUM_INIMIGOS)]

    class Projetil:
        def __init__(self, x, y, img):
            self.imagem = pygame.transform.scale(projetil, (13,13))
            self.x = x
            self.y = y
            self.img = img
            self.velocidade = -10
            self.limiteSuperior = 350

        def mover(self):
            self.y += self.velocidade
        
        def desenhar (self):
            tela.blit(self.imagem, (self.x, self.y))

        def limiteProjetil(self):
            return self.y < self.limiteSuperior
        

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
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                x_projetil = posicaoXCowboy + 82
                y_projetil = posicaoYCowboy + 7
                projeteis.append(Projetil(x_projetil, y_projetil, projetil))
                somTiro.play()                  
            
        if posicaoXCowboy < 150 :
            posicaoXCowboy = 150
        elif posicaoXCowboy > 670:
            posicaoXCowboy = 670

        for inimigo in inimigos:
            inimigo.reaparecer()

                
        tela.blit(fundo, (0, 0))

        for p in projeteis[:]:
            p.mover()
            p.desenhar()
            if p.limiteProjetil():
                projeteis.remove(p)
                
        for inimigo in inimigos:
            inimigo.desenhar()

        for p in projeteis[:]:
            projetilRect = pygame.Rect(p.x, p.y, p.imagem.get_width(), p.imagem.get_height())
            for i in inimigos[:]:
                inimigoRect = pygame.Rect(i.x, i.y, i.imagem.get_width(), i.imagem.get_height())
                if projetilRect.colliderect(inimigoRect):
                    projeteis.remove(p)
                    inimigos.remove(i)
                    inimigos.append(Inimigo())
                    break

        

        tela.blit(cowboy, (posicaoXCowboy, posicaoYCowboy))
        tela.blit(nuvem, (450, 100))

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
                    larguraBotaoStart = 96
                    alturaBotaoStart  =31
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startBotao.collidepoint(evento.pos):
                    contagemRegressiva()
                    jogar()
                                          
        tela.fill(branco)
        tela.blit(fundoInicio, (0,0) )
        caixaTexto = pygame.draw.rect(tela, corCaixa, pygame.Rect (225, 320, larguraCaixaTexto, alturaCaixaTexto), border_radius=15)
        detalheS = pygame.draw.rect(tela, corS , pygame.Rect (498, 450, larguraS, alturaS), border_radius=5)
        startBotao = pygame.draw.rect(tela, corS, (450,490, larguraBotaoStart, alturaBotaoStart), border_radius=10)
        startTitulo = fonteTitulo.render("BEM-VINDO", True, bege)
        startTexto = fonteInicio.render("Jogar", True, preto)
        playerName = fonteExplicacao.render(f"Nickname: {nome}", True, preto)
        explicacoes = [
        "O objetivo do jogo é matar os zumbis antes que eles cheguem ao",
        "fim da tela, se isso acontecer você perde uma vida. Você terá 5",
        "vidas. Para movimentar o personagem use as setas Direita e Es-",
        "querda e para atirar use a tecla S ."
        ]   
        for i in range(len(explicacoes)):
            linha_renderizada = fonteExplicacao.render(explicacoes[i], True, preto)
            tela.blit(linha_renderizada, (235, 360 + i * 30))
        tela.blit(playerName, (440, 324))
        tela.blit(startTitulo, (265, 20))
        tela.blit(startTexto, (466, 487))

        pygame.display.update()
        relogio.tick(60)    

start()