import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 400
HEIGHT = 600
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flap and Score")

clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game variables
gravity = 0.5
bird_movement = 0
score = 0
high_score = 0

# Load images
background_img = pygame.image.load("background.png").convert()
bird_img = pygame.image.load("bird.png").convert_alpha()
pipe_img = pygame.image.load("pipe.png").convert_alpha()

# Resize images
bird_img = pygame.transform.scale(bird_img, (50, 50))
pipe_img = pygame.transform.scale(pipe_img, (70, 400))

# Bird rectangle
bird_rect = bird_img.get_rect(center=(100, HEIGHT // 2))

# Pipe rectangles
pipe_heights = [200, 300, 400]
pipe_width = 70
pipe_gap = 200
pipe_x = WIDTH

# Game over text
game_over_font = pygame.font.Font(None, 50)

# Functions
def draw_score():
    score_surface = game_font.render(str(int(score)), True, WHITE)
    score_rect = score_surface.get_rect(center=(WIDTH // 2, 100))
    screen.blit(score_surface, score_rect)

def draw_high_score():
    high_score_surface = game_font.render("High Score: " + str(int(high_score)), True, WHITE)
    high_score_rect = high_score_surface.get_rect(center=(WIDTH // 2, 50))
    screen.blit(high_score_surface, high_score_rect)

def show_game_over():
    game_over_surface = game_over_font.render("Game Over", True, WHITE)
    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(game_over_surface, game_over_rect)

def create_pipe():
    random_height = random.choice(pipe_heights)
    bottom_pipe = pipe_img.get_rect(midtop=(pipe_x, random_height))
    top_pipe = pipe_img.get_rect(midbottom=(pipe_x, random_height - pipe_gap))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]
    return visible_pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= HEIGHT:
            screen.blit(pipe_img, pipe)
        else:
            flipped_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flipped_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

# Game loop
running = True
game_active = True
pipes = []

# Game font
game_font = pygame.font.Font(None, 36)

# Game main loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8
            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                pipes.clear()
                bird_rect.center = (100, HEIGHT // 2)
                bird_movement = 0
                score = 0

    if game_active:
        # Bird movement
        bird_movement += gravity
        bird_rect.centery += bird_movement

        # Draw background
        screen.blit(background_img, (0, 0))

        # Pipes
        if len(pipes) == 0:
            pipes.extend(create_pipe())
        pipes = move_pipes(pipes)
        draw_pipes(pipes)

        # Bird
        screen.blit(bird_img, bird_rect)

        # Collision detection
        if check_collision(pipes):
            game_active = False
            if score > high_score:
                high_score = score

        # Score
        score += 0.01
        draw_score()

    else:
        show_game_over()
        draw_high_score()

    # Update the display
    pygame.display.flip()

    # Set the frames per second
    clock.tick(FPS)

# Quit the game
pygame.quit()
