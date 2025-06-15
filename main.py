import pygame, random, pyttsx3, threading
import tkinter as tk
import speech_recognition as sr
from datetime import datetime
from tkinter import messagebox
from recursos.funcoes import contagemRegressiva
from recursos.funcoes import falarTexto
engine=pyttsx3.init()
pygame.init()
largura, altura = (1000,700)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( (largura, altura) )
pygame.display.set_caption("Cowboy Maluco")
corCaixa = (253, 193, 127)
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
branco = (255,255,255)
bege = (198, 129, 40)
corS = (243, 146, 85)
preto = (0, 0 ,0 )
cowboy = pygame.transform.smoothscale(pygame.image.load("recursos/cowboy.png"), (90, 80))
Zumbi = pygame.transform.smoothscale(pygame.image.load("recursos/Zumbi.png").convert_alpha(), (45, 65))
Zumbi2 = pygame.transform.smoothscale(pygame.image.load("recursos/Zumbi2.png").convert_alpha(), (45, 65))
cowboyChorando = pygame.image.load("recursos/cowboyChorando.png")
cabecaZumbi = pygame.image.load("recursos/cabeçaZumbi.png")
fundoInicio = pygame.image.load("recursos/fundoInicio.png")
projetil = pygame.image.load("recursos/projetil.png")
icone = pygame.image.load("recursos/icone.png")
fundo = pygame.image.load("recursos/fundo.png")
nuvem = pygame.image.load("recursos/nuvem.png")
coracao = pygame.transform.smoothscale(pygame.image.load("recursos/coração.png"), (30, 30))
pygame.display.set_icon(icone)
somTiro = pygame.mixer.Sound("recursos/somTiro.mp3")
somZumbi = pygame.mixer.Sound("recursos/somZumbi1.mp3")
somZumbi2 = pygame.mixer.Sound("recursos/somZumbi2.mp3")
fonteInicio = pygame.font.SysFont("comicsans",25)
fonteExplicacao = pygame.font.SysFont("comicsans",18)
fonteInstrucao = pygame.font.SysFont("comicsans",20)
fontePause = pygame.font.SysFont("comicsans", 100)
Pause = pygame.font.SysFont("comicsans", 20)
fonteTitulo = pygame.font.Font("recursos/FonteInicio.ttf",150)
pontosMensagem = pygame.font.SysFont("comicsans", 30)
mensagemPause = Pause.render("Pressione Espaço para pausar ", True, preto )
pause = fontePause.render("PAUSE", True, preto)
derrotaMensagem = fonteTitulo.render("VOCE PERDEU!", True, corCaixa)
startTitulo = fonteTitulo.render("BEM-VINDO", True, bege)
startTexto = fonteInicio.render("Jogar", True, preto)
pauseRect = pause.get_rect(center=((largura, altura)[0]//2, (largura, altura)[1]//2))
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

zumbiCabeca = pygame.transform.smoothscale(pygame.image.load("recursos/cabeçaZumbi.png"), (40, 35))
zumbiCabecaRect = zumbiCabeca.get_rect()

zumbiCabecaRect.x = random.randint(0, (largura, altura)[0] - zumbiCabecaRect.width)
zumbiCabecaRect.y = random.randint(0, (largura, altura)[1] - zumbiCabecaRect.height)

velocidadeCabeca = 0.3

direcaoX = random.randint(-10, 10)
direcaoY = random.randint(-10, 10)

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
alturaJanela = 110
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
    dano = False
    maximoVidas = 5
    vida = maximoVidas
    dano = False
    alpha = 0
    alphaVermelho = 0
    pontos = 0
    jogoPausado = False
    solX, solY = 1000, 5  
    raio = 20
    raioMinimo = 30
    raioMaximo = 40
    crescendo = True  
    velocidadePulso = 0.1 
    tempoDirecao = 0
    intervaloTroca = 2000
    posicaoXCowboy = 420
    posicaoYCowboy = 600
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
            nonlocal vida, dano, alpha, pontos
            self.y += self.velocidade
            if self.y > 700:
                self.y = random.randint(250, 450)
                faixa = random.choice(faixasPosicaoX)
                self.x = random.randint(faixa[0], faixa[1] - self.largura)
                self.imagem, self.som = random.choice(zumbisComSons)
                self.som.play()
                pontos = max(0, pontos - 20)

        def desenhar(self):
            tela.blit(self.imagem, (self.x, self.y))

    NUM_INIMIGOS = 6
    inimigos = [Inimigo() for _ in range(NUM_INIMIGOS)]
    zumbisMortos = 0
    zumbisSpawns = 10

    class Projetil:
        def __init__(self, x, y, img):
            self.imagem = pygame.transform.scale(projetil, (13,13))
            self.x = x
            self.y = y
            self.img = img
            self.velocidade = -14
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
                pygame.quit()
                exit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXCowboy = 7
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXCowboy = -7
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXCowboy = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXCowboy = 0
            if not jogoPausado:   
                if evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                    projetilX = posicaoXCowboy + 68
                    projetilY = posicaoYCowboy + 2
                    projeteis.append(Projetil(projetilX, projetilY, projetil))
                    somTiro.play()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    jogoPausado = not jogoPausado
                    if jogoPausado:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        if jogoPausado:
            instrucaoPause = fonteInstrucao.render("Press SPACE to Unpause Game", True, preto)
        else:
            instrucaoPause = fonteInstrucao.render("Press SPACE to Pause Game", True, preto)

        if jogoPausado:
            tela.blit(fundo, (0, 0))
            Pontos = pontosMensagem.render(f"Pontos: {pontos}", True, preto)
            tela.blit(Pontos, (10, 0))
            tela.blit(pause, pauseRect)
            tela.blit(instrucaoPause, (150, 10))
            pygame.display.update()
            

        if not jogoPausado:

            tempoPassado = relogio.tick(60)
            tempoDirecao += tempoPassado
            
            if tempoDirecao >= intervaloTroca:
                direcaoX = random.randint(-10, 10)
                direcaoY = random.randint(-10, 10)
                tempoDirecao = 0

            zumbiCabecaRect.x += direcaoX * velocidadeCabeca
            zumbiCabecaRect.y += direcaoY * velocidadeCabeca

            if zumbiCabecaRect.left <= 0 or zumbiCabecaRect.right >= (largura, altura)[0]:
                direcaoX = -direcaoX 
            if zumbiCabecaRect.top <= 0 or zumbiCabecaRect.bottom >= (largura, altura)[1]:
                direcaoY = -direcaoY 

            if crescendo:
                raio += velocidadePulso
                if raio >= raioMaximo:
                    crescendo = False
            else:
                raio -= velocidadePulso
                if raio <= raioMinimo:
                    crescendo = True
                
            if posicaoXCowboy < 150 :
                posicaoXCowboy = 150
            elif posicaoXCowboy > 670:
                posicaoXCowboy = 670

            posicaoXCowboy = posicaoXCowboy + movimentoXCowboy 

            for inimigo in inimigos:
                inimigo.reaparecer()

                    
            tela.blit(fundo, (0, 0))
            tela.blit(zumbiCabeca, zumbiCabecaRect)
            pygame.draw.circle(tela, amarelo, (solX, solY), int(raio))

            for p in projeteis[:]:
                p.mover()
                p.desenhar()
                if p.limiteProjetil():
                    projeteis.remove(p)
                    
            for inimigo in inimigos:
                inimigo.desenhar()

            inimigosRemover = []
            projeteisRemover = []
            inimigosAdicionar = []

            for p in projeteis:
                projetilRect = pygame.Rect(p.x, p.y, p.imagem.get_width(), p.imagem.get_height())
                for i in inimigos:
                    inimigoRect = pygame.Rect(i.x, i.y, i.imagem.get_width(), i.imagem.get_height())
                    if projetilRect.colliderect(inimigoRect):
                        if p not in projeteisRemover:
                            projeteisRemover.append(p)
                        if i not in inimigosRemover:
                            inimigosRemover.append(i)
                        inimigosAdicionar.append(Inimigo())
                        pontos += 1
                        zumbisMortos += 1

                        if zumbisMortos >= zumbisSpawns:
                            inimigosAdicionar.append(Inimigo())
                            zumbisSpawns += 10
                            zumbisMortos = 0

                        break 

            for p in projeteisRemover:
                if p in projeteis:
                    projeteis.remove(p)
            for i in inimigosRemover:
                if i in inimigos:
                    inimigos.remove(i)
                    
            for novo in inimigosAdicionar:
                inimigos.append(novo)

            cowboyRect = pygame.Rect(posicaoXCowboy, posicaoYCowboy, cowboy.get_width(), cowboy.get_height())
            inimigosColisao = []

            for inimigo in inimigos:
                inimigoRect = pygame.Rect(inimigo.x, inimigo.y, inimigo.largura, inimigo.altura)
                if cowboyRect.colliderect(inimigoRect):
                    dano = True
                    vida -= 1
                    alpha = 150
                    inimigosColisao.append(inimigo)

                    if vida <= 0:
                        vida = 0
                        registrarDerrrota()
                        dead()
                        
                if vida < maximoVidas:
                    alphaVermelho = int((1 - (vida / maximoVidas)) * 30)
                    overlayVermelho = pygame.Surface((largura, altura))
                    overlayVermelho.set_alpha(alphaVermelho)
                    overlayVermelho.fill(vermelho)
                    tela.blit(overlayVermelho, (0, 0))

                if dano:
                    overlay = pygame.Surface((largura, altura))
                    overlay.set_alpha(alpha)
                    overlay.fill(vermelho)
                    tela.blit(overlay, (0, 0))
                    alpha -= 7

                    if alpha <= 0:
                        dano = False
                        alpha = 0

            for inimigo in inimigosColisao:
                if inimigo in inimigos:
                    inimigos.remove(inimigo)
                    inimigos.append(Inimigo())
                
            tela.blit(cowboy, (posicaoXCowboy, posicaoYCowboy))
            tela.blit(instrucaoPause, (175, 4))
            Pontos = pontosMensagem.render(f"Pontos: {pontos}", True, preto)
            tela.blit(Pontos, (5, -5))
            for i in range(vida):
                tela.blit(coracao, (10 + i * 35, 50))
            pygame.display.update()

            def registrarDerrrota():
                registro = datetime.now()
                dataHora = registro.strftime("%Y-%m-%d %H:%M:%S")

                with open("log.dat.", "a", encoding="utf-8") as arquivo:
                    arquivo.write(f"Derrrota registrada em: {dataHora} | Pontos: {pontos}\n")
            
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
        playerName = fonteExplicacao.render(f"Nickname: {nome}", True, preto)
        explicacoes = [
        "O objetivo do jogo é matar os zumbis antes que eles cheguem ao",
        "fim da tela, se isso acontecer você perde uma vida. Você terá 5",
        "vidas. Para movimentar o personagem use as setas Direita e Es-",
        "querda e para atirar use a tecla S ."
        ]   
        for i in range(len(explicacoes)):
            linhaRenderizada = fonteExplicacao.render(explicacoes[i], True, preto)
            tela.blit(linhaRenderizada, (235, 360 + i * 30))
        tela.blit(playerName, (440, 324))
        tela.blit(startTitulo, (265, 20))
        tela.blit(startTexto, (466, 487))

        pygame.display.update()
        relogio.tick(60)   

def dead():
    pygame.mixer.music.stop() 
    
    try:
        with open("log.dat", "r", encoding="utf-8") as arquivo:
            linhas = arquivo.readlines()

    except FileNotFoundError:
        linhas = ["Nenhum registro de partida encontrado."]

    quantidadeLinhas = linhas[-5:]
    inicioHistorico = 440

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()

        tela.blit(cowboyChorando, (0, 0))
        tela.blit(derrotaMensagem, (220, 20))
        caixaTexto = pygame.draw.rect(tela, corCaixa, pygame.Rect (85, 440, 855, 210), border_radius=15)
        
        y = inicioHistorico
        for linha in quantidadeLinhas:
            linhaFormatada = linha.strip()
            historico = pontosMensagem.render(linhaFormatada, True, preto)
            tela.blit(historico, (100, y))
            y += 40

        pygame.display.update()
        relogio.tick(60) 
start()