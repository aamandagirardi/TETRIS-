import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
largura_tela = 495
altura_tela = 581
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption('Tela Inicial')

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)

# Carrega a imagem de fundo
imagem_fundo = pygame.image.load('Imagem_inicio.png')

# Função para desenhar botões
def desenhar_botao(texto, x, y, largura, altura, cor):
    pygame.draw.rect(tela, cor, (x, y, largura, altura))
    fonte = pygame.font.Font(None, 36)
    texto_surface = fonte.render(texto, True, branco)
    texto_rect = texto_surface.get_rect(center=(x + largura // 2, y + altura // 2))
    tela.blit(texto_surface, texto_rect)

# Coordenadas dos botões
largura_botao = 200
altura_botao = 50
espaco = 1 # Espaço entre os botões

# Calcula a posição dos botões
y_jogar = (altura_tela // 2) - (altura_botao + espaco)  # Botão "Jogar"
y_highscore = (altura_tela // 2)  # Botão "Highscore"
y_sair = (altura_tela // 2) + (altura_botao + espaco)  # Botão "Sair"

# Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if (largura_tela // 2 - largura_botao // 2 <= event.pos[0] <= largura_tela // 2 + largura_botao // 2 and
                y_jogar <= event.pos[1] <= y_jogar + altura_botao):  # Botão Jogar
                import tetris  # Importa o arquivo do jogo Tetris
                tetris.main()  # Chama a função principal do jogo

            elif (largura_tela // 2 - largura_botao // 2 <= event.pos[0] <= largura_tela // 2 + largura_botao // 2 and
                  y_highscore <= event.pos[1] <= y_highscore + altura_botao):  # Botão Highscore
                pass  # Não faz nada por enquanto

            elif (largura_tela // 2 - largura_botao // 2 <= event.pos[0] <= largura_tela // 2 + largura_botao // 2 and
                  y_sair <= event.pos[1] <= y_sair + altura_botao):  # Botão Sair
                pygame.quit()
                sys.exit()

    # Desenha a imagem de fundo
    tela.blit(imagem_fundo, (0, 0))

    # Desenha os botões
    desenhar_botao('Jogar', largura_tela // 2 - largura_botao // 2, y_jogar, largura_botao, altura_botao, preto)
    desenhar_botao('Sair', largura_tela // 2 - largura_botao // 2, y_sair, largura_botao, altura_botao, preto)

    pygame.display.flip()
