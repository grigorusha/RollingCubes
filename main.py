# Импортируем библиотеку pygame
import pygame
from pygame import *
import random

# Объявляем переменные
SIZE_X_START = 3
SIZE_Y_START = 3
CUBE_SIZE = 100
BORDER = 5
TILE = 10
PANEL_SIZE = 70
BACKGROUND_COLOR = "#000000"

CUBE_COLOR = [("W","#FFFFFF"),("R","#FF0000"),("B","#0000FF"),
              ("Y","#FFFF00"),("P","#800080"),("G","#008000")]
level = []

def init_level(y,x):
    level = []
    for ny in range(y):
        str = []
        for nx in range(x):
            str.append(["W", "B"])
        level.append(str)

    ny = y // 2
    nx = x // 2
    level[ny][nx] = [" "," "]

    return level

def next_cubes(top, face):
    for face_ind, COLOR_ONE in enumerate(CUBE_COLOR):
        if COLOR_ONE[0] == face:
            break
    for top_ind, COLOR_ONE in enumerate(CUBE_COLOR):
        if COLOR_ONE[0] == top:
            break

    back_ind = (top_ind + 3)%6
    vek = 1-(top_ind % 2)*2

    face_set = CUBE_COLOR.copy()
    face1 = min(top_ind, back_ind)
    face_set.pop(face1)
    face_set.pop(face1+2)

    if vek < 0:
        face_set.reverse()

    while face_set[0][0]!=face:
        elem = face_set.pop(0)
        face_set.append(elem)

    return face_set

def main():
    SIZE_X = SIZE_X_START
    SIZE_Y = SIZE_Y_START

    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    timer = pygame.time.Clock()

    while True:
        WIN_WIDTH = SIZE_X * CUBE_SIZE  # Ширина создаваемого окна
        WIN_HEIGHT = SIZE_Y * CUBE_SIZE + PANEL_SIZE  # Высота
        DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

        level = init_level(SIZE_Y, SIZE_X)
        moves = 0

        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Rolling Cubes")  # Пишем в шапку
        screen.fill(BACKGROUND_COLOR) # Заливаем поверхность сплошным цветом

        button_y1 = CUBE_SIZE * SIZE_Y + BORDER + 10
        button_reset = font.render('Reset', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_reset_place = button_reset.get_rect(topleft=(10, button_y1))
        button_scramble = font.render('Scramble', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_scramble_place = button_scramble.get_rect(topleft=(button_reset_place.right+10, button_y1))

        button_y2 = button_reset_place.bottom + 5
        button_minusx = font.render('-', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_minusx_place = button_minusx.get_rect(topleft=(10, button_y2))
        textx = font.render(str(SIZE_X), True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        textx_place = textx.get_rect(topleft=(button_minusx_place.right+3, button_y2))
        button_plusx = font.render('+', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_plusx_place = button_plusx.get_rect(topleft=(textx_place.right+3, button_y2))

        button_minusy = font.render('-', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_minusy_place = button_minusy.get_rect(topleft=(button_plusx_place.right+10, button_y2))
        texty = font.render(str(SIZE_Y), True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        texty_place = texty.get_rect(topleft=(button_minusy_place.right+3, button_y2))
        button_plusy = font.render('+', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_plusy_place = button_plusy.get_rect(topleft=(texty_place.right+3, button_y2))

        scramble_move = 0
        solved = True

        while True:  # Основной цикл программы
            vek = mouse_x = mouse_y = 0

            if scramble_move == 0:
                timer.tick(10)
                # menu
                pf_black = Surface((CUBE_SIZE*SIZE_X, PANEL_SIZE))
                pf_black.fill(Color("#000000"))
                screen.blit(pf_black, (0, CUBE_SIZE*SIZE_Y))
                pf = Surface((CUBE_SIZE*SIZE_X, 5))
                pf.fill(Color("#B88800"))
                screen.blit(pf, (0, CUBE_SIZE*SIZE_Y+BORDER))
                if solved:
                    text_solved = font.render('Solved', True, CUBE_COLOR[4][1])
                else:
                    text_solved = font.render('not solved', True, CUBE_COLOR[5][1])
                text_solved_place = text_solved.get_rect(topleft=(button_scramble_place.right + 10, button_y1))
                screen.blit(text_solved, text_solved_place)
                text_moves = font.render('Moves: ' + str(moves), True, CUBE_COLOR[1][1])
                text_moves_place = text_moves.get_rect(topleft=(button_plusy_place.right + 10, button_y2))
                screen.blit(text_moves, text_moves_place)

                # button
                screen.blit(button_reset, button_reset_place)
                screen.blit(button_scramble, button_scramble_place)
                screen.blit(button_minusx, button_minusx_place)
                screen.blit(textx, textx_place)
                screen.blit(button_plusx, button_plusx_place)
                screen.blit(button_minusy, button_minusy_place)
                screen.blit(texty, texty_place)
                screen.blit(button_plusy, button_plusy_place)

                for ev in pygame.event.get():  # Обрабатываем события
                    if (ev.type == QUIT) or (ev.type == KEYDOWN and ev.key == K_ESCAPE):
                        return SystemExit, "QUIT"
                    if ev.type == KEYDOWN and ev.key == K_UP:
                        vek = 1
                    if ev.type == KEYDOWN and ev.key == K_LEFT:
                        vek = 2
                    if ev.type == KEYDOWN and ev.key == K_DOWN:
                        vek = 3
                    if ev.type == KEYDOWN and ev.key == K_RIGHT:
                        vek = 4
                    if ev.type == MOUSEBUTTONDOWN and ev.button == 1:
                        mouse_x = ev.pos[0]
                        mouse_y = ev.pos[1]
            else:
                vek = random.randint(1,4)

            if mouse_x+mouse_y > 0:
                if mouse_y<CUBE_SIZE*SIZE_Y+BORDER:
                    xx = mouse_x // CUBE_SIZE
                    xx2 = mouse_x % CUBE_SIZE
                    if xx2>0:
                        xx += 1
                    yy = mouse_y // CUBE_SIZE
                    yy2 = mouse_y % CUBE_SIZE
                    if yy2>0:
                        yy += 1

                    xx -= 1
                    yy -= 1
                    cube = level[yy][xx]
                    if cube[0] != " ":
                        if xx != 0:
                            cube_test = level[yy][xx-1]
                            if cube_test[0] == " ":
                                vek = 2
                        if xx != SIZE_X-1:
                            cube_test = level[yy][xx+1]
                            if cube_test[0] == " ":
                                vek = 4
                        if yy != 0:
                            cube_test = level[yy-1][xx]
                            if cube_test[0] == " ":
                                vek = 1
                        if yy != SIZE_Y-1:
                            cube_test = level[yy+1][xx]
                            if cube_test[0] == " ":
                                vek = 3
                else:
                    if (mouse_x>=button_reset_place.left)and(mouse_x<=button_reset_place.right) and (mouse_y>=button_reset_place.top)and(mouse_y<=button_reset_place.bottom):
                        # reset
                        break
                    elif (mouse_x>=button_scramble_place.left)and(mouse_x<=button_scramble_place.right) and (mouse_y>=button_scramble_place.top)and(mouse_y<=button_scramble_place.bottom):
                        # scramble
                        scramble_move = SIZE_X*SIZE_Y*100
                    elif (mouse_x>=button_minusx_place.left)and(mouse_x<=button_minusx_place.right) and (mouse_y>=button_minusx_place.top)and(mouse_y<=button_minusx_place.bottom):
                        # scramble
                        if SIZE_X>2:
                            SIZE_X -= 1
                        break
                    elif (mouse_x>=button_plusx_place.left)and(mouse_x<=button_plusx_place.right) and (mouse_y>=button_plusx_place.top)and(mouse_y<=button_plusx_place.bottom):
                        # scramble
                        if SIZE_X<10:
                            SIZE_X += 1
                        break
                    elif (mouse_x>=button_minusy_place.left)and(mouse_x<=button_minusy_place.right) and (mouse_y>=button_minusy_place.top)and(mouse_y<=button_minusy_place.bottom):
                        # scramble
                        if SIZE_Y>2:
                            SIZE_Y -= 1
                        break
                    elif (mouse_x>=button_plusy_place.left)and(mouse_x<=button_plusy_place.right) and (mouse_y>=button_plusy_place.top)and(mouse_y<=button_plusy_place.bottom):
                        # scramble
                        if SIZE_Y<10:
                            SIZE_Y += 1
                        break

            if vek!=0:
                fl = False
                for ny in range(SIZE_Y):
                    for nx in range(SIZE_X):
                        cube = level[ny][nx]
                        if cube[0] == " ":
                            fl = True
                            break
                    if fl:
                        break
                nyp = ny
                nxp = nx

                fl = True
                if vek==1:
                    if ny==SIZE_Y-1:
                        fl = False
                    ny += 1
                elif vek == 3:
                    if ny == 0:
                        fl = False
                    ny -= 1
                elif vek == 2:
                    if nx == SIZE_X - 1:
                        fl = False
                    nx += 1
                elif vek==4:
                    if nx==0:
                        fl = False
                    nx -= 1

                if fl:
                    cube = level[ny][nx]

                    face_set = next_cubes(cube[0], cube[1])
                    face_set2 = next_cubes(face_set[4-vek][0], cube[0])
                    if vek == 1: # UP
                        cube = [face_set2[3][0], face_set2[2][0]]
                    elif vek == 3:  # DOWN
                        cube = [face_set2[3][0], face_set2[0][0]]
                    elif vek == 2:  # LEFT
                        cube = [face_set2[3][0], cube[1]]
                    elif vek == 4: # RIGHT
                        cube = [face_set2[3][0] , cube[1]]

                    level[ny][nx] = [" ", " "]
                    level[nyp][nxp] = cube

                    moves += 1

            if scramble_move != 0:
                scramble_move -= 1
                moves = 0
                continue

            solved = True
            x = y = 0  # координаты
            for row in level:  # вся строка
                for cube in row:  # каждый куб
                    if cube[0]==" ":
                        pf = Surface((CUBE_SIZE, CUBE_SIZE))
                        pf.fill(Color(BACKGROUND_COLOR))
                        screen.blit(pf, (x, y))
                    else:
                        if (cube[0]!="W")or(cube[1]!="B"):
                            solved = False

                        # верхняя плитка
                        pf = Surface((CUBE_SIZE-BORDER*2-TILE*2, CUBE_SIZE-BORDER*2-TILE*2))
                        for up,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==cube[0]:
                                pf.fill(Color(COLOR_ONE[1]))
                                break
                        screen.blit(pf, (x+BORDER+TILE, y+BORDER+TILE))

                        face_set = next_cubes(cube[0],cube[1])

                        # передняя плитка
                        pf = Surface((CUBE_SIZE-BORDER*2-TILE*2, TILE))
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[0][0]:
                                pf.fill(Color(COLOR_ONE[1]))
                                break
                        screen.blit(pf, (x+BORDER+TILE, y+CUBE_SIZE-BORDER-TILE))

                        # левая плитка
                        pf = Surface((TILE, CUBE_SIZE-BORDER*2-TILE*2))
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[1][0]:
                                pf.fill(Color(COLOR_ONE[1]))
                                break
                        screen.blit(pf, (x+BORDER, y+BORDER+TILE))

                        # задняя плитка
                        pf = Surface((CUBE_SIZE-BORDER*2-TILE*2, TILE))
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[2][0]:
                                pf.fill(Color(COLOR_ONE[1]))
                                break
                        screen.blit(pf, (x+BORDER+TILE, y+BORDER))

                        # правая плитка
                        pf = Surface((TILE, CUBE_SIZE-BORDER*2-TILE*2))
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[3][0]:
                                pf.fill(Color(COLOR_ONE[1]))
                                break
                        screen.blit(pf, (x+CUBE_SIZE-BORDER-TILE, y+BORDER+TILE))

                    x += CUBE_SIZE  # блоки платформы ставятся на ширине блоков
                y += CUBE_SIZE  # то же самое и с высотой
                x = 0  # на каждой новой строчке начинаем с нуля

            pygame.display.update()  # обновление и вывод всех изменений на экран

main()