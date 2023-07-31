import sys

import pygame
import random
import time
import threading

import DBname.DBsession
from DBname import DBsession
from DBname.CreatingTag import add_time_game, add_stand_game
from DBname.Stand_game import StandGame
from DBname.Time_game import timeGame

# Инициализация Pygame
pygame.init()

DBsession.global_init("db/game.db")

# Размеры окна
WIDTH = 450
HEIGHT = 900

# Размеры игрового поля
GRID_SIZE = 30
NUM_ROWS = 30
NUM_COLS = 10

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Определение фигур
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]]
]

# Инициализация окна игры и шрифта
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тетрис")
font = pygame.font.SysFont(None, 40)
font1 = pygame.font.SysFont(None, 34)
paused = False
global sound_on
sound_on = True

timer_start = 0
time_limit = 360

pygame.mixer.init()

composition1 = pygame.mixer.Sound("sound/8 Bit Music - Action Man (Mega Man Style Chiptune) [TubeRipper.com].wav")
composition2 = pygame.mixer.Sound("sound/8Bit Boss Chiptune - Boss Theme - Sawsquarenoise Free Copyright-Safe Music [TubeRipper.com].wav")
composition3 = pygame.mixer.Sound("sound/Run As Fast As You Can [TubeRipper.com].wav")
destroyline = pygame.mixer.Sound("sound/destroyline.wav")
movesound = pygame.mixer.Sound("sound/move.wav")
endsound = pygame.mixer.Sound("sound/end.wav")
compositions = [composition1, composition2, composition3]


# def play_music():
#     sound = sound_on
#     if sound:
#         while True:
#             random_composition = random.choice(compositions)
#             random_composition.play()
#             pygame.time.wait(int(random_composition.get_length() * 1000))
#             random_composition.stop()
#     else:
#         pygame.mixer.stop()
#
#
# music_thread = threading.Thread(target=play_music)
# music_thread.start()


def draw_rating_menu():
    menu_text = font.render("рейтинг", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - 50, 100))

    global timerating_button
    global standartrating_button
    global allrating_button
    global menu_button

    timerating_button = pygame.Rect(0, 200, 100, 50)
    pygame.draw.rect(screen, WHITE, timerating_button)
    ratingtime_text = font.render("время", True, BLACK)
    screen.blit(ratingtime_text, (0, 210))


    standartrating_button = pygame.Rect(0, 300, 130, 50)
    pygame.draw.rect(screen, WHITE, standartrating_button)
    standardrat_text = font.render("Стандарт", True, BLACK)
    screen.blit(standardrat_text, (0, 310))

    allrating_button = pygame.Rect(0, 400, 100, 50)
    pygame.draw.rect(screen, WHITE, allrating_button)
    allrat_text = font.render("Общий", True, BLACK)
    screen.blit(allrat_text, (0, 410))

    menu_button = pygame.Rect(0, 850, 100, 50)
    pygame.draw.rect(screen, WHITE, menu_button)
    menurat_text = font.render("Меню", True, BLACK)
    screen.blit(menurat_text, (0, 860))


def ratingscreen():
    screen.fill(BLACK)
    db_sess = DBsession.create_session()
    all_list = []
    time_game = db_sess.query(timeGame).all()
    all_list.extend(time_game)
    stand_game = db_sess.query(StandGame).all()
    all_list.extend(stand_game)
    all_list = sorted(all_list, key=lambda x: x.create_data, reverse=True)
    db_sess.close()

    rat = True
    while rat:
        x = 0
        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rat = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rat = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if timerating_button.collidepoint(pygame.mouse.get_pos()):
                    time_game = sorted(time_game, key=lambda x: x.create_data, reverse=True)
                    screen.fill(BLACK)
                    draw_rating_menu()
                    for el in time_game[:15]:
                        text = font1.render(f'{"На время"} | {el.score} | {el.timeingame} | {el.level}', True, WHITE)
                        screen.blit(text, (150, 160 + x))
                        x += 50
                elif standartrating_button.collidepoint(pygame.mouse.get_pos()):
                    stand_game = sorted(stand_game, key=lambda x: x.create_data, reverse=True)
                    screen.fill(BLACK)
                    draw_rating_menu()
                    for el in stand_game[:15]:
                        text = font1.render(f'{"Стандарт"} | {el.score} | {el.level}', True, WHITE)
                        screen.blit(text, (150, 160 + x))
                        x += 50
                elif allrating_button.collidepoint(pygame.mouse.get_pos()):
                    screen.fill(BLACK)
                    draw_rating_menu()
                    for el in all_list[:15]:
                        text = font1.render(f'{"На время" if "timeGame" in el.__class__.__name__ else "Стандарт"} | {el.score} | {el.timeingame if "timeGame" in el.__class__.__name__ else "None"} | {el.level}', True, WHITE)
                        screen.blit(text, (150, 160 + x))
                        x += 50
                elif menu_button.collidepoint(pygame.mouse.get_pos()):
                    rat = False

        draw_rating_menu()

        pygame.display.flip()


def draw_main_menu(sound=True):
    screen.fill(BLACK)
    menu_text = font.render("Главное меню", True, WHITE)
    screen.blit(menu_text, (WIDTH // 2 - 100, 100))

    global rating_button
    global standard_button
    global timed_button
    global sound_button

    # Кнопка "Рейтинг"
    rating_button = pygame.Rect(WIDTH // 2 - 75, 200, 150, 50)
    pygame.draw.rect(screen, WHITE, rating_button)
    rating_text = font.render("Рейтинг", True, BLACK)
    screen.blit(rating_text, (WIDTH // 2 - 50, 210))

    # Кнопка "Стандартная игра"
    standard_button = pygame.Rect(WIDTH // 2 - 150, 300, 300, 50)
    pygame.draw.rect(screen, WHITE, standard_button)
    standard_text = font.render("Стандартная игра", True, BLACK)
    screen.blit(standard_text, (WIDTH // 2 - 125, 310))

    # Кнопка "Игра на время"
    timed_button = pygame.Rect(WIDTH // 2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, WHITE, timed_button)
    timed_text = font.render("Игра на время", True, BLACK)
    screen.blit(timed_text, (WIDTH // 2 - 93, 410))

    sound_button = pygame.Rect(WIDTH // 2 - 75, 840, 150, 50)
    pygame.draw.rect(screen, WHITE, sound_button)
    soundON_text = font.render("Включить", True, BLACK)
    soundOFF_text = font.render("Выключить", True,BLACK)
    if sound == True:
        screen.blit(soundOFF_text, (WIDTH // 2 - 75, 850))
    else:
        screen.blit(soundON_text, (WIDTH // 2 - 70, 850))


def end_game(Win=None):
    end = True
    if Win is not None:
        screen.fill(BLACK)
        end_text = font.render("Win", True, WHITE)
        screen.blit(end_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
    else:
        screen.fill(BLACK)
        end_text = font.render("Game Over", True, WHITE)
        screen.blit(end_text, (WIDTH // 2 - 80, HEIGHT // 2))
        pygame.display.flip()
    while end:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                end = False
            if event.type == pygame.KEYDOWN:
                end = False
            pygame.display.flip()


def draw_grid():
    for row in range(NUM_ROWS):
        pygame.draw.line(screen, WHITE, (0, row * GRID_SIZE), (WIDTH, row * GRID_SIZE))
    for col in range(NUM_COLS + 1):
        pygame.draw.line(screen, WHITE, (col * GRID_SIZE, 0), (col * GRID_SIZE, HEIGHT))


def draw_score(score, time_left=None, level=0):
    score_text = font.render("Счет: " + str(score), True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 32))
    score_text = font.render("Уровень: " + str(level), True, WHITE)
    screen.blit(score_text, (WIDTH - 150, 130))

    if paused:
        paused_text = font.render("Пауза", True, WHITE)
        screen.blit(paused_text, (WIDTH - 150, 64))
    if time_left is not None:
        time_text = font.render(str(int(time_left)) + " сек", True, WHITE)
        screen.blit(time_text, (WIDTH - 150, 98))


def draw_shape(shape, row, col):
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c]:
                pygame.draw.rect(screen, WHITE, ((col + c) * GRID_SIZE, (row + r) * GRID_SIZE, GRID_SIZE, GRID_SIZE))


def check_collision(shape, row, col):
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c]:
                if (row + r >= NUM_ROWS or col + c < 0 or col + c >= NUM_COLS) or (row + r >= 0 and board[row + r][col + c] == 1):
                    return True
    return False


def merge_shape(shape, row, col):
    if sound_on:
        endsound.play()
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c]:
                board[row + r][col + c] = 1


def remove_rows():
    full_rows = []
    for row in range(NUM_ROWS):
        if all(board[row]):
            full_rows.append(row)
    for row in full_rows:
        del board[row]
        board.insert(0, [0] * NUM_COLS)
    if sound_on:
        destroyline.play()
    return len(full_rows)


def generate_shape():
    shape_index = random.randint(0, len(SHAPES) - 1)
    return SHAPES[shape_index]


def play_standard_game():
    global paused
    global running
    global board
    global level

    # Инициализация параметров игры
    board = [[0] * NUM_COLS for _ in range(NUM_ROWS)]
    current_shape = generate_shape()
    current_row = 0
    current_col = NUM_COLS // 2 - len(current_shape[0]) // 2
    score = 0
    level = 0

    # Главный игровой цикл

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                add_stand_game(score, level)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused

        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if not check_collision(current_shape, current_row, current_col - 1):
                    if sound_on:
                        movesound.play()
                    current_col -= 1
            if keys[pygame.K_RIGHT]:
                if not check_collision(current_shape, current_row, current_col + 1):
                    if sound_on:
                        movesound.play()
                    current_col += 1
            if keys[pygame.K_DOWN]:
                if not check_collision(current_shape, current_row + 1, current_col):
                    if sound_on:
                        movesound.play()
                    current_row += 1
            if keys[pygame.K_UP]:
                rotated_shape = list(zip(*current_shape[::-1]))
                if not check_collision(rotated_shape, current_row, current_col):
                    if sound_on:
                        movesound.play()
                    current_shape = rotated_shape
            if keys[pygame.K_SPACE]:
                while current_row < NUM_ROWS - len(current_shape) and not check_collision(current_shape, current_row + 1, current_col):
                    if sound_on:
                        movesound.play()
                    current_row += 1
            if keys[pygame.K_ESCAPE]:
                add_stand_game(score, level)
                running = False

        # Опускание фигуры вниз каждый кадр (пропускается при коллизии)
            if not check_collision(current_shape, current_row + 1, current_col):
                current_row += 1
            else:
                merge_shape(current_shape, current_row, current_col)
                score += remove_rows()
                current_shape = generate_shape()
                current_row = 0
                current_col = NUM_COLS // 2 - len(current_shape[0]) // 2
                if score >= (level * 10) + 11:
                    if level == 11:
                        end_game(1)
                        add_stand_game(score, level)
                        running = False
                    else:
                        level += 1


            # Проверка на завершение игры
                if check_collision(current_shape, current_row, current_col):
                    end_game()
                    add_stand_game(score, level)
                    running = False

        # Очистка экрана
        screen.fill(BLACK)

        # Отрисовка игрового поля
        draw_grid()

        # Отрисовка текущей фигуры
        draw_shape(current_shape, current_row, current_col)

        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if board[r][c] != 0:
                    pygame.draw.rect(screen, WHITE, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Отрисовка счета
        draw_score(score, None, level)

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(5 + level)


def play_time_game():
    global paused
    global running
    global timer_start
    global board
    global level
    global timer

    paused = False
    timer_start = time.time()
    # Инициализация параметров игры
    board = [[0] * NUM_COLS for _ in range(NUM_ROWS)]
    current_shape = generate_shape()
    current_row = 0
    current_col = NUM_COLS // 2 - len(current_shape[0]) // 2
    score = 0
    level = 0

    # Главный игровой цикл

    clock = pygame.time.Clock()
    running = True
    while running:

        timer = int(time.time() - timer_start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                add_time_game(score, level, timer)
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused


        if not paused:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                if not check_collision(current_shape, current_row, current_col - 1):
                    if sound_on:
                        movesound.play()
                    current_col -= 1
            if keys[pygame.K_RIGHT]:
                if not check_collision(current_shape, current_row, current_col + 1):
                    if sound_on:
                        movesound.play()
                    current_col += 1
            if keys[pygame.K_DOWN]:
                if not check_collision(current_shape, current_row + 1, current_col):
                    if sound_on:
                        movesound.play()
                    current_row += 1
            if keys[pygame.K_UP]:
                rotated_shape = list(zip(*current_shape[::-1]))
                if not check_collision(rotated_shape, current_row, current_col):
                    if sound_on:
                        movesound.play()
                    current_shape = rotated_shape
            if keys[pygame.K_SPACE]:
                while current_row < NUM_ROWS - len(current_shape) and not check_collision(current_shape, current_row + 1, current_col):
                    if sound_on:
                        movesound.play()
                    current_row += 1
            if keys[pygame.K_ESCAPE]:
                add_time_game(score, level, timer)
                print(str(timer) + "привет")
                running = False

        # Опускание фигуры вниз каждый кадр (пропускается при коллизии)
            if not check_collision(current_shape, current_row + 1, current_col):
                current_row += 1
            else:
                merge_shape(current_shape, current_row, current_col)
                score += remove_rows()
                current_shape = generate_shape()
                current_row = 0
                current_col = NUM_COLS // 2 - len(current_shape[0]) // 2
                if score >= (level * 10) + 11:
                    level += 1
                    if level == 7:
                        end_game(1)
                        add_time_game(score, level, timer)
                        running = False
                    else:
                        level += 1

            # Проверка на завершение игры
                if check_collision(current_shape, current_row, current_col):
                    end_game()
                    add_time_game(score, level, timer)
                    running = False

            time_left = time_limit - (time.time() - timer_start)

        if time.time() - timer_start >= time_limit:
            end_game()
            add_time_game(score, level, timer)
            running = False

        # Очистка экрана
        screen.fill(BLACK)

        # Отрисовка игрового поля
        draw_grid()

        # Отрисовка текущей фигуры
        draw_shape(current_shape, current_row, current_col)

        for r in range(NUM_ROWS):
            for c in range(NUM_COLS):
                if board[r][c] != 0:
                    pygame.draw.rect(screen, WHITE, (c * GRID_SIZE, r * GRID_SIZE, GRID_SIZE, GRID_SIZE))

        # Отрисовка счета
        draw_score(score, time_left, level)

        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(5 + level)


main = True
while main:

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                main = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if standard_button.collidepoint(pygame.mouse.get_pos()):
                play_standard_game()
            elif timed_button.collidepoint(pygame.mouse.get_pos()):
                play_time_game()
            elif sound_button.collidepoint(pygame.mouse.get_pos()):
                sound_on = not sound_on
                if sound_on:
                    pygame.mixer.unpause()
                else:
                    pygame.mixer.pause()
            elif rating_button.collidepoint(pygame.mouse.get_pos()):
                ratingscreen()


    # Отрисовка главного меню
    draw_main_menu(sound_on)

    pygame.display.flip()

# Закрытие Pygame
pygame.quit()
sys.exit