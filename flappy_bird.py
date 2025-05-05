import pygame
import random
pygame.init()

# Configuración de la pantalla del juego
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
CLOCK = pygame.time.Clock()

# Carga de imágenes
BG = pygame.transform.scale(pygame.image.load("bg.png"), (400, 500))
GROUND = pygame.transform.scale(pygame.image.load("ground.png"), (435, 100))
BIRD = pygame.image.load("bird1.png")
DOWN_PIPE = pygame.transform.scale(pygame.image.load("pipe.png"), (50, 300))
TOP_PIPE = pygame.transform.rotate(DOWN_PIPE, 180)

# Fuente para texto
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 60)

def draw_text(text, size, x, y, color=(255,255,255), center=True):
    f = pygame.font.SysFont(None, size)
    t = f.render(text, True, color)
    rect = t.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    SCREEN.blit(t, rect)

def start_screen():
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(GROUND, (0, 500))
    draw_text("Flappy Bird", 60, WIDTH // 2, HEIGHT // 2 - 50)
    draw_text("Presiona ESPACIO para empezar", 30, WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()
    wait_for_space()

def game_over_screen(score):
    SCREEN.blit(BG, (0, 0))
    SCREEN.blit(GROUND, (0, 500))
    draw_text("¡Game Over!", 60, WIDTH // 2, HEIGHT // 2 - 60)
    draw_text(f"Puntaje: {score}", 40, WIDTH // 2, HEIGHT // 2)
    draw_text("Presiona ESPACIO para reiniciar", 30, WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()
    wait_for_space()

def wait_for_space():
    waiting = True
    while waiting:
        CLOCK.tick(15)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_loop():
    # Posición y físicas
    bird_x, bird_y = 50, 250
    bird_speed_y = 3
    bird_acceleration = 0.5
    bird_speed_jump = -6

    # Suelo
    ground_x = 0
    ground_speed_x = -4

    # Tuberías
    pipes = []
    pipe_speed_x = -4
    pipe_gap = 120
    pipe_width = 50
    pipe_height = 300

    # Puntuación
    score = 0

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_speed_y = bird_speed_jump

        bird_speed_y += bird_acceleration 
        bird_y += bird_speed_y

        if bird_y <= 0 or bird_y >= 500 - BIRD.get_height():
            run = False

        ground_x += ground_speed_x
        if ground_x <= -35:
            ground_x = 0

        if len(pipes) == 0 or pipes[-1][0] < 200:
            center = random.randint(150, 350)
            pipes.append([WIDTH, center])

        SCREEN.blit(BG, (0, 0))
        new_pipes = []
        bird_rect = pygame.Rect(bird_x, bird_y, BIRD.get_width(), BIRD.get_height())

        for pipe in pipes:
            pipe[0] += pipe_speed_x
            if pipe[0] > -pipe_width:
                new_pipes.append(pipe)

                top_y = pipe[1] - pipe_gap // 2 - pipe_height
                bottom_y = pipe[1] + pipe_gap // 2

                top_rect = pygame.Rect(pipe[0], top_y, pipe_width, pipe_height)
                bottom_rect = pygame.Rect(pipe[0], bottom_y, pipe_width, pipe_height)

                SCREEN.blit(TOP_PIPE, (pipe[0], top_y))
                SCREEN.blit(DOWN_PIPE, (pipe[0], bottom_y))

                if bird_rect.colliderect(top_rect) or bird_rect.colliderect(bottom_rect):
                    run = False

                if pipe[0] + pipe_width < bird_x and 'scored' not in pipe:
                    score += 1
                    pipe.append('scored')

        pipes = new_pipes

        SCREEN.blit(GROUND, (ground_x, 500))
        SCREEN.blit(BIRD, (bird_x, bird_y))
        draw_text(f"Score: {score}", 30, 10, 10, center=False)

        pygame.display.flip()
        CLOCK.tick(60)

    return score

# --- EJECUCIÓN DEL JUEGO ---
while True:
    start_screen()
    final_score = game_loop()
    game_over_screen(final_score)