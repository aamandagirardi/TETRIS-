import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),
    (100, 179, 179),
    (80, 34, 22),
    (80, 134, 22),
    (180, 34, 22),
    (180, 34, 122),
]

class Figure:
    x = 0
    y = 0

    figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # O
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # T
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # S
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # Z
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # J
        [[1, 2, 5, 6]],  # L
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.figures) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def image(self):
        return self.figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.figures[self.type])


class Tetris:
    def __init__(self, height, width):
        self.level = 2
        self.score = 0
        self.lines = 0
        self.state = "start"
        self.field = []
        self.height = height
        self.width = width
        self.x = 27
        self.y = 90
        self.zoom = 26
        self.figure = None
        self.next_figure = Figure(0, 0)  # Inicializa a próxima peça
        self.hold = None  # Peça guardada
        self.hold_used = False  # Controle para evitar múltiplas trocas
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_figure(self):
        self.figure = self.next_figure
        self.next_figure = Figure(0, 0)  # Gera uma nova próxima peça
        self.hold_used = False  # Reset ao criar nova peça
        if self.intersects():  # Verifica se a nova peça já colide ao ser criada
            self.state = "gameover"

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    if i + self.figure.y > self.height - 1 or \
                            j + self.figure.x > self.width - 1 or \
                            j + self.figure.x < 0 or \
                            self.field[i + self.figure.y][j + self.figure.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]
        self.score += lines ** 2
        self.lines += lines

    def go_space(self):
        while not self.intersects():
            self.figure.y += 1
        self.figure.y -= 1
        self.freeze()

    def go_down(self):
        self.figure.y += 1
        if self.intersects():
            self.figure.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.figure.image():
                    self.field[i + self.figure.y][j + self.figure.x] = self.figure.color
        self.break_lines()
        self.new_figure()  # Aqui a nova peça é gerada e imediatamente verificada se colide
        if self.intersects():
            self.state = "gameover"

    def go_side(self, dx):
        old_x = self.figure.x
        self.figure.x += dx
        if self.intersects():
            self.figure.x = old_x

    def rotate(self):
        old_rotation = self.figure.rotation
        self.figure.rotate()
        if self.intersects():
            self.figure.rotation = old_rotation

    def hold_figure(self):
        if not self.hold_used:  # Permite trocar a peça apenas uma vez por ciclo
            if self.hold is None:  # Guarda a peça atual, se não houver nenhuma guardada
                self.hold = self.figure
                self.new_figure()
            else:  # Troca a peça guardada pela peça atual
                self.hold, self.figure = self.figure, self.hold
                self.figure.x = 3  # Reseta a posição da peça trocada
                self.figure.y = 0
            self.hold_used = True


pygame.init()

background = pygame.image.load('imagem_fundo.png')

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

size = (background.get_width(), background.get_height())
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(17, 10)  # Altura ajustada
counter = 0

pressing_down = False
paused = False  # Variável para controlar pausa

while not done:
    if game.figure is None:
        game.new_figure()

    counter += 1
    if counter > 100000:
        counter = 0

    if game.state == "start" and not paused:
        if counter % (fps // game.level // 2) == 0 or pressing_down:
            game.go_down()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Pausa e despausa o jogo
                paused = not paused

            if not paused:
                if game.state == "start":
                    if event.key == pygame.K_UP:
                        game.rotate()
                    if event.key == pygame.K_DOWN:
                        pressing_down = True
                    if event.key == pygame.K_LEFT:
                        game.go_side(-1)
                    if event.key == pygame.K_RIGHT:
                        game.go_side(1)
                    if event.key == pygame.K_SPACE:
                        game.go_space()
                    if event.key == pygame.K_c:  # Tecla para guardar a peça
                        game.hold_figure()
                if event.key == pygame.K_ESCAPE:
                    game.__init__(17, 10)  # Reinicia o jogo

                if game.state == "gameover" and event.key == pygame.K_RETURN:
                    game.__init__(17, 10)  # Reinicia o jogo

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_DOWN:
            pressing_down = False

    screen.blit(background, (0, 0))

    if game.state == "gameover":
        font = pygame.font.SysFont('Calibri', 65, True, False)
        text_game_over = font.render("GAME OVER", True, (255, 125, 0))
        screen.blit(text_game_over, [96, 250])
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text_restart = font.render("Pressione Enter para reiniciar", True, (255, 255, 255))
        screen.blit(text_restart, [110, 320])
    elif paused:
        overlay = pygame.Surface(size)
        overlay.set_alpha(128)  # Define a transparência (0 a 255)
        overlay.fill((128, 128, 128))  # Cor cinza
        screen.blit(overlay, (0, 0))

        font = pygame.font.SysFont('Calibri', 65, True, False)
        text_pause = font.render("JOGO PAUSADO", True, (255, 255, 255))
        screen.blit(text_pause, [45, 250])
        font = pygame.font.SysFont('Calibri', 25, True, False)
        text_resume = font.render("Aperte P para voltar ao jogo", True, (255, 255, 255))
        screen.blit(text_resume, [100, 320])
    else:
        for i in range(game.height):
            for j in range(game.width):
                pygame.draw.rect(screen, BLACK, [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
                if game.field[i][j] > 0:
                    pygame.draw.rect(screen, colors[game.field[i][j]],
                                     [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1, game.zoom - 2, game.zoom - 1])

        if game.figure is not None:
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.figure.image():
                        pygame.draw.rect(screen, colors[game.figure.color],
                                         [game.x + game.zoom * (j + game.figure.x) + 1,
                                          game.y + game.zoom * (i + game.figure.y) + 1,
                                          game.zoom - 2, game.zoom - 2])

        font = pygame.font.SysFont('Calibri', 25, True, False)
        text_next = font.render("Próxima Peça:", True, WHITE)
        screen.blit(text_next, [330, 50])

        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.next_figure.image():
                    pygame.draw.rect(screen, colors[game.next_figure.color],
                                     [350 + game.zoom * j, 80 + game.zoom * i,
                                      game.zoom - 2, game.zoom - 2])

        font1 = pygame.font.SysFont('Calibri', 17, True, False)
        if game.hold is None:
            text_hold_empty = font1.render("Aperte C para", True, WHITE)
            text_hold_empty2 = font1.render("guardar a peça", True, WHITE)
            screen.blit(text_hold_empty, [328, 280])
            screen.blit(text_hold_empty2, [326, 300])
        else:
            scale_factor = 0.6
            for i in range(4):
                for j in range(4):
                    p = i * 4 + j
                    if p in game.hold.image():
                        pygame.draw.rect(screen, colors[game.hold.color],
                                         [350 + int(game.zoom * j * scale_factor), 280 + int(game.zoom * i * scale_factor),
                                          int(game.zoom * scale_factor) - 2, int(game.zoom * scale_factor) - 2])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
