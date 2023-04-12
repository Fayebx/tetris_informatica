#!/bin/python3
#
#
#source: https://github.com/StanislavPetrovV/Python-Tetris
#source: https://github.com/jjengo/tetris/tree/master/sounds
#source: https://stackoverflow.com/questions/59778780/adding-menu-with-buttons-to-pygame
#source: https://stackoverflow.com/questions/30720665/countdown-timer-in-pygame
#
import pygame
from copy import deepcopy
from random import choice, randrange
#
from pygame import mixer
#
# starting the mixer
mixer.init()
mixer.music.set_volume(0.9)

# constants (UPPER_CASE_NAMES)
BLACK = (  0,  0,  0) #RGB KLEUR CODES
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
W, H = 10, 20
TILE = 35
GAME_RES = W * TILE, H * TILE
RES = 750, 940 #RESOLUTIE
FPS = 60

# initialize pygame
pygame.init()

# set the timer
timer_event = pygame.USEREVENT+1

# variables
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# tetris figures
figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for j in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

bg = pygame.image.load('images/black.jpg').convert()
game_bg = pygame.image.load('images/black.jpg').convert()

main_font = pygame.font.SysFont('menlo', 65) #pygame.font.Font('font/font.ttf', 65)
font = pygame.font.SysFont('menlo', 35) #pygame.font.Font('font/font.ttf', 45)
instruction_font = pygame.font.SysFont('menlo', 25) #pygame.font.Font('font/font.ttf', 65)
countdowntimer_font = pygame.font.SysFont('menlo', 65) #pygame.font.Font('font/font.ttf', 65)

title_score = font.render('score', True, pygame.Color('red'))
title_record = font.render('record', True, pygame.Color('green'))

get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

score, lines = 0, 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

stage = 'menu'
running = True

# functie: maak de buttons
def button_create(text, rect, inactive_color, active_color, action):
    font = pygame.font.Font(None, 40)
    button_rect = pygame.Rect(rect)
    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    return [text, text_rect, button_rect, inactive_color, active_color, action, False]


# functie: controleer buttons
def button_check(info, event):
    text, text_rect, rect, inactive_color, active_color, action, hover = info
    if event.type == pygame.MOUSEMOTION:
        # hover = True/False
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:
            action()


# functie: teken biuttons
def button_draw(screen, info):
    text, text_rect, rect, inactive_color, active_color, action, hover = info
    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)

# functie: geklikt op start button
def on_click_button_start():
    global stage
    stage = 'countdown'


# functie: geklikt op exit button
def on_click_button_exit():
    global stage
    global running
    stage = 'exit'
    running = False


# functie afspelen geluid
def play_sound(sound):
    s = mixer.Sound("sounds/"+sound+".wav")
    s.play()


# functie:
def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


# functie: inlezen highscore
def get_record():
    try:
        with open('record') as f:
            return f.readline()
    except FileNotFoundError:
        with open('record', 'w') as f:
            f.write('0')


# functie: opslaan highscore
def set_record(record, score):
    rec = max(int(record), score)
    with open('record', 'w') as f:
        f.write(str(rec))


# functie: reset countdown timer
def reset_countdown():
    global counter, countdownTimer
    counter = 3
    countdownTimer = 99
    timer_event = pygame.USEREVENT+1
    pygame.time.set_timer(timer_event, 1000)


#####################
### HOOFD ROUTUNE ###
#####################
button_start = button_create("START", (260, 670, 100, 50), RED, GREEN, on_click_button_start)
button_exit = button_create("QUIT", (400, 670, 100, 50), RED, GREEN, on_click_button_exit)

# reset the countdown timer
reset_countdown()

# Infinite loop
while running:
    # get highscore
    record = get_record()
    #
    dx, rotate = 0, False
    sc.blit(bg, (0, 0))
    sc.fill(pygame.Color('black'))
    sc.blit(game_sc, (20, 20))
    game_sc.fill(pygame.Color('black'))

    for i in range(lines):
        pygame.time.wait(200)

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == timer_event and stage == "countdown":
                counter -= 1
                text = font.render(str(counter), True, (0, 128, 0))
                if counter == -2:
                    pygame.time.set_timer(timer_event, 0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
                play_sound("lateralmove")
            elif event.key == pygame.K_RIGHT:
                dx = 1
                play_sound("lateralmove")
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
                play_sound("drop")
            elif event.key == pygame.K_UP:
                rotate = True

        # check buttons
        button_check(button_start, event)
        button_check(button_exit, event)

    # draws
    button_draw(sc, button_exit)

    # countdown timer
    if stage == "countdown":
        sc.fill((255, 255, 255))
        text = str(counter)
        #
        # play count down sound
        if counter != countdownTimer:
            if counter > 0:
                play_sound("countDown")
            if counter == 0:
                play_sound("countDownLetsGo")
        #
        countdownTimer = counter
        #
        if counter == 0 or counter == -1:
            text = "Lets Go!"

        # end of countdown timer. Start game
        if counter == -2:
            stage = "game"
            mixer.music.load("sounds/tetrismusic.wav")
            mixer.music.play(-1, 0.0)

        sc.fill(pygame.Color('black'))
        title_countdown_timer = countdowntimer_font.render(text, True, pygame.Color('white'))
        text_rect = title_countdown_timer.get_rect(center=sc.get_rect().center)
        sc.blit(title_countdown_timer, text_rect)

    if stage == "menu":
        button_draw(sc, button_start)

        # display instructions for game
        title = pygame.image.load('images/tetris.jpg')
        title = pygame.transform.scale(title, (750, 200))
        sc.blit(title, (0, 20))
        arrow_keys = pygame.image.load('images/arrowkeys.png')
        arrow_keys = pygame.transform.scale(arrow_keys, (150, 85))
        sc.blit(arrow_keys, (295, 400))

        #instruction text
        text_rotate = instruction_font.render('ROTATE', True, pygame.Color('purple'))
        sc.blit(text_rotate, (325, 360))
        text_rotate = instruction_font.render('DROP', True, pygame.Color('purple'))
        sc.blit(text_rotate, (340, 500))
        text_rotate = instruction_font.render('LEFT', True, pygame.Color('purple'))
        sc.blit(text_rotate, (220, 450))
        text_rotate = instruction_font.render('RIGHT', True, pygame.Color('purple'))
        sc.blit(text_rotate, (470, 450))

    elif stage == "game":
        # move x
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].x += dx
            if not check_borders():
                figure = deepcopy(figure_old)
                break
        # move y
        anim_count += anim_speed
        if anim_count > anim_limit:
            anim_count = 0
            figure_old = deepcopy(figure)
            for i in range(4):
                figure[i].y += 1
                if not check_borders():
                    for i in range(4):
                        field[figure_old[i].y][figure_old[i].x] = color
                    figure, color = next_figure, next_color
                    next_figure, next_color = deepcopy(choice(figures)), get_color()
                    anim_limit = 2000
                    break
        # rotate
        center = figure[0]
        figure_old = deepcopy(figure)
        if rotate:
            play_sound("rotate")
            for i in range(4):
                x = figure[i].y - center.y
                y = figure[i].x - center.x
                figure[i].x = center.x - x
                figure[i].y = center.y + y
                if not check_borders():
                    figure = deepcopy(figure_old)
                    break
        # check lines
        line, lines = H - 1, 0
        for row in range(H - 1, -1, -1):
            count = 0
            for i in range(W):
                if field[row][i]:
                    count += 1
                field[line][i] = field[row][i]
            if count < W:
                line -= 1
            else:
                # Next level, speed up animation
                play_sound("levelup")
                anim_speed += 20
                lines += 1
        # compute score
        score += scores[lines]
        # draw grid
        [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
        # draw figure
        for i in range(4):
            figure_rect.x = figure[i].x * TILE
            figure_rect.y = figure[i].y * TILE
            pygame.draw.rect(game_sc, color, figure_rect)
        # draw field
        for y, raw in enumerate(field):
            for x, col in enumerate(raw):
                if col:
                    figure_rect.x, figure_rect.y = x * TILE, y * TILE
                    pygame.draw.rect(game_sc, col, figure_rect)
        # draw next figure
        for i in range(4):
            figure_rect.x = next_figure[i].x * TILE + 380
            figure_rect.y = next_figure[i].y * TILE + 185
            pygame.draw.rect(sc, next_color, figure_rect)
        # draw titles
        title = pygame.image.load('images/tetris.jpg')
        title = pygame.transform.scale(title, (350, 120))
        sc.blit(title, (400, 0))

        sc.blit(title_score, (535, 630))
        sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 680))
        sc.blit(title_record, (525, 500))
        sc.blit(font.render(record, True, pygame.Color('gold')), (550, 550))
        # game over
        for i in range(W):
            if field[0][i]:
                # save record
                set_record(record, score)
                field = [[0 for i in range(W)] for i in range(H)]
                anim_count, anim_speed, anim_limit = 0, 60, 2000
                score = 0
                play_sound("gameover")
                for i_rect in grid:
                    pygame.draw.rect(game_sc, get_color(), i_rect)
                    sc.blit(game_sc, (20, 20))
                    pygame.display.flip()
                    clock.tick(200)
                #
                # start countdown timer
                stage = "countdown"
                reset_countdown()

    pygame.display.flip()
    clock.tick(FPS)