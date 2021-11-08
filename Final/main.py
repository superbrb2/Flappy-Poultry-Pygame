import pygame
import sys
import random


def draw_floor():
    wn.blit(floor_surface, (floor_x_pos, 800))
    wn.blit(floor_surface, (floor_x_pos + 576, 800))


def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 245))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            wn.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            wn.blit(flip_pipe, pipe)


def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            hit_sound.play()
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 800:
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
    return new_bird


def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(f'{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 150))
        wn.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 150))
        wn.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 775))
        wn.blit(high_score_surface, high_score_rect)


def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score


def score_sound(pipes):
    global pipe
    for pipe in pipes:
        if pipe.centerx == 100:
            point_sound.play()
    return pipes


pygame.init()
wn = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('sounds_n_shit/04B_19.TTF', 50)

# Game variables
gravity = 0.25
bird_movement = 0
game_active = True
score = -1
high_score = 0
death_noise = 1


bird_downflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, 1200))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 150)
pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [400, 500, 600, 700]

bg_surface = pygame.image.load('assets/background-day.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

game_over_surface = pygame.image.load('assets/message.png')
game_over_surface = pygame.transform.scale2x(game_over_surface).convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288, 475))

flap_sound = pygame.mixer.Sound('sounds_n_shit/sound/sfx_wing.wav')
point_sound = pygame.mixer.Sound('sounds_n_shit/sound/sfx_point.wav')
death_sound = pygame.mixer.Sound('sounds_n_shit/sound/sfx_die.wav')
hit_sound = pygame.mixer.Sound('sounds_n_shit/sound/sfx_hit.wav')


# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_movement = 0
                bird_movement -= 7.5
                flap_sound.play()

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = -1
                death_sound = 1

    wn.blit(bg_surface, (0, 0))

    if game_active:
        # Bird
        rotated_bird = rotate_bird(bird_surface)
        bird_movement += gravity
        wn.blit(rotated_bird, bird_rect)
        bird_rect.centery += bird_movement
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score display
        score += 0.00833

        # Score sound
        score_sound(pipe_list)

        score_display('main_game')
    else:
        wn.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

        # death sound
        if death_noise == 1:
            death_sound.play()
            death_noise += 1
    # Floor
    floor_x_pos -= 5
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)
