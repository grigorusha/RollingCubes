# Импортируем библиотеку pygame
import pygame
from pygame import *
import random

from tkinter import Tk
from tkinter import filedialog as fd
import os

# Объявляем базовые переменные
SIZE_X_START = 3
SIZE_Y_START = 3
CUBE_SIZE = 100
BORDER = 5
TILE = 10
SHIFT = 3
PANEL_SIZE = 120
BACKGROUND_COLOR = "#000000"
GRAY_COLOR = "#808080"
GRAY_COLOR2 = "#A0A0A0"

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

def check_button(place, y, x):
    if (x >= place.left) and (x <= place.right) and (y >= place.top) and (y <= place.bottom):
        return True
    return False

def read_file():
    dir = os.path.abspath(os.curdir)
    filetypes = (("Текстовый файл", "*.txt"),("Любой", "*"))
    filename = fd.askopenfilename(title="Open Level", initialdir=dir,filetypes=filetypes)
    if filename=="":
        return ""

    x = y = 0
    level = []
    with open(filename,'r') as f:
        lines = f.readlines()
        for str in lines:
            str_mas = []
            str = str.replace('\n','')
            while len(str)>=2:
                sim1 = str[0]
                sim2 = str[1]
                str = str[3:]
                str_mas.append([sim1,sim2])
            level.append(str_mas)
            y += 1
            x = max(x,len(str_mas))
    return level, y, x

def save_file(level):
    dir = os.path.abspath(os.curdir)
    filetypes = (("Текстовый файл", "*.txt"),("Любой", "*"))
    filename = fd.asksaveasfile("w", title="Save Level as...", initialdir=dir,filetypes=filetypes)
    if filename==None:
        return ""

    with open(filename.name, 'w') as f:
        for str in level:
            line = ""
            for cube in str:
                line += cube[0]+cube[1]+" "
            f.write(line+"\n")

def main():
    # основные константы
    SIZE_X = SIZE_X_START
    SIZE_Y = SIZE_Y_START
    file_ext = False

    # основная инициализация
    random.seed()
    pygame.init()  # Инициация PyGame
    font = pygame.font.SysFont('Verdana', 18)
    timer = pygame.time.Clock()
    Tk().withdraw()

    ################################################################################
    ################################################################################
    # перезапуск программы при смене параметров
    while True:
        # дополнительные константы
        WIN_WIDTH = SIZE_X * CUBE_SIZE  # Ширина создаваемого окна
        WIN_HEIGHT = SIZE_Y * CUBE_SIZE + PANEL_SIZE  # Высота
        DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную

        if file_ext:
            file_ext = False
        else:
            level = init_level(SIZE_Y, SIZE_X)
        moves_stack = []
        moves = 0
        scramble_move = 0
        solved = True
        edit_mode = False
        square = 0

        # инициализация окна
        screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
        pygame.display.set_caption("Rolling Cubes")  # Пишем в шапку
        pygame.display.set_icon(pygame.image.load('RollingCubes.ico'))
        screen.fill(BACKGROUND_COLOR) # Заливаем поверхность сплошным цветом

        # инициализация всех кнопок
        button_y1 = CUBE_SIZE * SIZE_Y + BORDER + 10
        button_reset = font.render('Reset', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_reset_place = button_reset.get_rect(topleft=(10, button_y1))
        button_scramble = font.render('Scramble', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_scramble_place = button_scramble.get_rect(topleft=(button_reset_place.right+10, button_y1))
        button_undo = font.render('Undo', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_undo_place = button_undo.get_rect(topleft=(button_scramble_place.right+10, button_y1))

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
        button_open = font.render('Open', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_open_place = button_open.get_rect(topleft=(button_plusy_place.right+10, button_y2))
        button_save = font.render('Save', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
        button_save_place = button_save.get_rect(topleft=(button_open_place.right+10, button_y2))

        button_y3 = button_minusx_place.bottom + 5

        ################################################################################
        ################################################################################
        # Основной цикл программы
        while True:
            vek = mouse_x = mouse_y = cube_pos_x = cube_pos_y = 0
            undo = False

            ################################################################################
            ################################################################################
            # отрисовка элементов меню и кнопок

            if scramble_move == 0:

                # menu
                pf_black = Surface((CUBE_SIZE*SIZE_X, PANEL_SIZE))
                pf_black.fill(Color("#000000"))
                screen.blit(pf_black, (0, CUBE_SIZE*SIZE_Y))
                pf = Surface((CUBE_SIZE*SIZE_X, 5))
                pf.fill(Color("#B88800"))
                screen.blit(pf, (0, CUBE_SIZE*SIZE_Y+BORDER))

                if edit_mode:
                    button_edit = font.render('Edit', True, CUBE_COLOR[2][1], CUBE_COLOR[0][1])
                else:
                    button_edit = font.render('Edit', True, CUBE_COLOR[2][1], CUBE_COLOR[5][1])
                button_edit_place = button_edit.get_rect(topleft=(10, button_y3))
                button_y4 = button_edit_place.bottom + 5

                # text
                text_moves = font.render('Moves: ' + str(moves), True, CUBE_COLOR[1][1])
                text_moves_place = text_moves.get_rect(topleft=(10, button_y4))
                screen.blit(text_moves, text_moves_place)
                if solved:
                    text_solved = font.render('Solved', True, CUBE_COLOR[0][1])
                else:
                    text_solved = font.render('not solved', True, CUBE_COLOR[5][1])
                text_solved_place = text_solved.get_rect(topleft=(text_moves_place.right + 10, button_y4))
                screen.blit(text_solved, text_solved_place)

                # button
                screen.blit(button_reset, button_reset_place)
                screen.blit(button_scramble, button_scramble_place)
                screen.blit(button_undo, button_undo_place)
                screen.blit(button_minusx, button_minusx_place)
                screen.blit(textx, textx_place)
                screen.blit(button_plusx, button_plusx_place)
                screen.blit(button_minusy, button_minusy_place)
                screen.blit(texty, texty_place)
                screen.blit(button_plusy, button_plusy_place)
                screen.blit(button_open, button_open_place)
                screen.blit(button_save, button_save_place)
                screen.blit(button_edit, button_edit_place)

                # edit button - WRB,YPG
                draw.polygon(screen, CUBE_COLOR[0][1], [[button_edit_place.right + 5+4, button_edit_place.top+4],
                                                        [button_edit_place.right + 5 + button_edit_place.height-4, button_edit_place.top+4],
                                                        [button_edit_place.right + 5 + button_edit_place.height-4, button_edit_place.bottom-4],
                                                        [button_edit_place.right + 5+4, button_edit_place.bottom-4]])
                draw.line(screen,CUBE_COLOR[1][1],[button_edit_place.right + 5 + button_edit_place.height-3, button_edit_place.top+4],
                                                  [button_edit_place.right + 5 + button_edit_place.height-3, button_edit_place.bottom-4],3)
                draw.line(screen,CUBE_COLOR[2][1],[button_edit_place.right + 5 + button_edit_place.height-4, button_edit_place.bottom-3],
                                                  [button_edit_place.right + 5+4, button_edit_place.bottom-3],3)
                draw.line(screen,CUBE_COLOR[4][1],[button_edit_place.right + 5+3, button_edit_place.top+4],
                                                  [button_edit_place.right + 5+3, button_edit_place.bottom-4],3)
                draw.line(screen,CUBE_COLOR[5][1],[button_edit_place.right + 5+4, button_edit_place.top+3],
                                                  [button_edit_place.right + 5 + button_edit_place.height-4, button_edit_place.top+3],3)
                draw.polygon(screen,GRAY_COLOR,[[button_edit_place.right + button_edit_place.height + 5+4, button_edit_place.top+3],[button_edit_place.right + 5 + button_edit_place.height*2 - 2, button_edit_place.top+3],
                                                [button_edit_place.right + 5 + button_edit_place.height*2 - 2, button_edit_place.bottom-3],[button_edit_place.right + button_edit_place.height + 5+4, button_edit_place.bottom-3]])
                draw.line(screen,GRAY_COLOR2,[button_edit_place.right + button_edit_place.height + 5+4+3, button_edit_place.top+3+3],
                                                  [button_edit_place.right + 5 + button_edit_place.height*2 - 2-3, button_edit_place.bottom-3-3],2)
                draw.line(screen,GRAY_COLOR2,[button_edit_place.right + 5 + button_edit_place.height*2 - 2-3, button_edit_place.top+3+3],
                                                  [button_edit_place.right + button_edit_place.height + 5+4+3, button_edit_place.bottom-3-3],2)
                draw.polygon(screen,GRAY_COLOR,[[button_edit_place.right + button_edit_place.height*2 + 5+4, button_edit_place.top+3],[button_edit_place.right + 5 + button_edit_place.height*3 - 2, button_edit_place.top+3],
                                                [button_edit_place.right + 5 + button_edit_place.height*3 - 2, button_edit_place.bottom-3],[button_edit_place.right + button_edit_place.height*2 + 5+4, button_edit_place.bottom-3]],2)
                if square == 1:
                    draw.polygon(screen, CUBE_COLOR[3][1],
                                 [[button_edit_place.right + 5, button_edit_place.top],
                                  [button_edit_place.right + 4 + button_edit_place.height,button_edit_place.top],
                                  [button_edit_place.right + 4 + button_edit_place.height,button_edit_place.bottom - 1],
                                  [button_edit_place.right + 5, button_edit_place.bottom - 1]], 2)
                elif square == 2:
                    draw.polygon(screen, CUBE_COLOR[3][1], [
                        [button_edit_place.right + button_edit_place.height + 5 + 2, button_edit_place.top+1],
                        [button_edit_place.right + 5 -1 + button_edit_place.height * 2, button_edit_place.top+1],
                        [button_edit_place.right + 5 -1 + button_edit_place.height * 2, button_edit_place.bottom-2],
                        [button_edit_place.right + button_edit_place.height + 5 +2, button_edit_place.bottom-2]],2)
                elif square == 3:
                    draw.polygon(screen, CUBE_COLOR[3][1], [
                        [button_edit_place.right + button_edit_place.height * 2 + 5 + 2, button_edit_place.top + 1],
                        [button_edit_place.right + 5 + button_edit_place.height * 3 , button_edit_place.top + 1],
                        [button_edit_place.right + 5 + button_edit_place.height * 3 , button_edit_place.bottom - 1],
                        [button_edit_place.right + button_edit_place.height * 2 + 5 + 2, button_edit_place.bottom - 1]],2)


            ################################################################################
            ################################################################################
            # обработка событий

            if scramble_move == 0:
                timer.tick(10)

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
                    if ev.type == MOUSEBUTTONDOWN and ev.button == 5:
                        mouse_x = button_undo_place.right
                        mouse_y = button_undo_place.top
            else:
                cube_pos_x = random.randint(0,SIZE_X-1)
                cube_pos_y = random.randint(0,SIZE_Y-1)

                cube = level[cube_pos_y][cube_pos_x]
                if (cube[0] != " ") and (cube[0] != "X"):
                    vek = random.randint(1,4)
                    mouse_x = mouse_y = 1

            ################################################################################
            ################################################################################
            # обработка нажатия на кнопки

            if mouse_x+mouse_y > 0 and scramble_move == 0:
                if mouse_y>CUBE_SIZE*SIZE_Y+BORDER:
                    if check_button(button_reset_place, mouse_y, mouse_x): # reset
                        break
                    elif check_button(button_scramble_place, mouse_y, mouse_x) and not edit_mode:  # scramble
                        scramble_move = SIZE_X * SIZE_Y * 1000
                    elif check_button(button_undo_place, mouse_y, mouse_x) and not edit_mode:  # undo
                        if len(moves_stack) > 0:
                            vek,cube_pos_y,cube_pos_x = moves_stack.pop()
                            vek = (vek + 1) % 4 + 1
                            moves -= 1
                            undo = True
                    elif check_button(button_open_place, mouse_y, mouse_x):  # open
                        fil = read_file()
                        if fil!="":
                            level, SIZE_Y, SIZE_X = fil
                            file_ext = True
                            break
                    elif check_button(button_save_place, mouse_y, mouse_x):  # save
                        save_file(level)
                    elif check_button(button_edit_place, mouse_y, mouse_x):  # edit
                        edit_mode = not edit_mode
                        if edit_mode:
                            square = 1
                        else:
                            square = 0
                        moves_stack = []
                        moves = 0
                    elif edit_mode and(mouse_x>button_edit_place.right+5)and(mouse_x<button_edit_place.right+button_edit_place.height+5)and(mouse_y>button_edit_place.top)and(mouse_y<button_edit_place.bottom):
                        square = 1
                        moves_stack = []
                        moves = 0
                    elif edit_mode and(mouse_x>button_edit_place.right+button_edit_place.height+5)and(mouse_x<button_edit_place.right+button_edit_place.height*2+5)and(mouse_y>button_edit_place.top)and(mouse_y<button_edit_place.bottom):
                        square = 2
                        moves_stack = []
                        moves = 0
                    elif edit_mode and(mouse_x>button_edit_place.right+button_edit_place.height*2+5)and(mouse_x<button_edit_place.right+button_edit_place.height*3+5)and(mouse_y>button_edit_place.top)and(mouse_y<button_edit_place.bottom):
                        square = 3
                        moves_stack = []
                        moves = 0
                    elif check_button(button_minusx_place, mouse_y, mouse_x):
                        if SIZE_X > 2:
                            SIZE_X -= 1
                        break
                    elif check_button(button_plusx_place, mouse_y, mouse_x):
                        if SIZE_X < 10:
                            SIZE_X += 1
                        break
                    elif check_button(button_minusy_place, mouse_y, mouse_x):
                        if SIZE_Y > 2:
                            SIZE_Y -= 1
                            pos = pygame.mouse.get_pos()
                            pygame.mouse.set_pos(pos[0], pos[1] - CUBE_SIZE)
                        break
                    elif check_button(button_plusy_place, mouse_y, mouse_x):
                        if SIZE_Y < 10:
                            SIZE_Y += 1
                            pos = pygame.mouse.get_pos()
                            pygame.mouse.set_pos(pos[0], pos[1]+CUBE_SIZE)
                        break


                ################################################################################
                ################################################################################
                # обработка нажатия на кубики в игровом поле

                else:
                    # определим координаты кубика
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

                    cube_pos_x = xx
                    cube_pos_y = yy

                    # определим сторону на которую нажали
                    nn1 = xx2>yy2
                    nn2 = (CUBE_SIZE-xx2)>yy2
                    if nn1 and nn2:
                        vek2 = 1
                    elif (not nn1) and nn2:
                        vek2 = 2
                    elif (not nn1) and (not nn2):
                        vek2 = 3
                    elif nn1 and (not nn2):
                        vek2 = 4

                    if not edit_mode:
                        cube = level[yy][xx]
                        if (cube[0] != " ")and(cube[0] != "X"):

                            # определим количество пустых клеток вокруг кубика (num)
                            # если пустая клетка одна, то направление перекатывания однозначное.
                            # если несколько, то надо учитывать сторону кубика для выбора направления

                            num = 0
                            if yy != 0:
                                cube_test = level[yy-1][xx]
                                if cube_test[0] == " ":
                                    vek = 1
                                    num += 1
                            if xx != 0:
                                cube_test = level[yy][xx-1]
                                if cube_test[0] == " ":
                                    vek = 2
                                    num += 1
                            if yy != SIZE_Y-1:
                                cube_test = level[yy+1][xx]
                                if cube_test[0] == " ":
                                    vek = 3
                                    num += 1
                            if xx != SIZE_X-1:
                                cube_test = level[yy][xx+1]
                                if cube_test[0] == " ":
                                    vek = 4
                                    num += 1

                            # пустых клеток несколько
                            if num>1:
                                vek = 0
                                if vek2==1:
                                    if yy != 0:
                                        cube_test = level[yy - 1][xx]
                                        if cube_test[0] == " ":
                                            vek = 1
                                if vek2==2:
                                    if xx != 0:
                                        cube_test = level[yy][xx - 1]
                                        if cube_test[0] == " ":
                                            vek = 2
                                if vek2==3:
                                    if yy != SIZE_Y - 1:
                                        cube_test = level[yy + 1][xx]
                                        if cube_test[0] == " ":
                                            vek = 3
                                if vek2==4:
                                    if xx != SIZE_X - 1:
                                        cube_test = level[yy][xx + 1]
                                        if cube_test[0] == " ":
                                            vek = 4
                    else:
                        # режим редактора игрового поля
                        if square==1:
                            level[yy][xx] = ["W","B"]
                        elif square == 2:
                            level[yy][xx] = ["X", "X"]
                        elif square==3:
                            level[yy][xx] = [" "," "]


            ################################################################################
            ################################################################################
            # логика игры - выполнение перемещений кубиков

            if vek!=0:
                if mouse_x+mouse_y == 0:
                    # играем с клавиатуры
                    fl = False
                    for ny in range(SIZE_Y):
                        for nx in range(SIZE_X):
                            cube = level[ny][nx]
                            if cube[0] == " ":
                                fl = True
                                break
                        if fl:
                            break
                    # нашли позицию пустой ячейки
                    nyp = ny
                    nxp = nx

                    # найдем позицию кубика, который перекатываем
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
                else:
                    # играем мышкой, координаты уже знаем
                    nxp = nx = cube_pos_x
                    nyp = ny = cube_pos_y

                    # найдем позицию пустой ячейки
                    fl = True
                    if vek==1:
                        if nyp==0:
                            fl = False
                        nyp -= 1
                    elif vek == 3:
                        if nyp == SIZE_Y-1:
                            fl = False
                        nyp += 1
                    elif vek == 2:
                        if nxp == 0:
                            fl = False
                        nxp -= 1
                    elif vek==4:
                        if nxp==SIZE_X - 1:
                            fl = False
                        nxp += 1

                # само вращение кубика
                if fl:
                    cube = level[ny][nx]
                    cube0 = level[nyp][nxp]

                    if cube[0]!="X" and cube0[0]==" ":
                        face_set = next_cubes(cube[0], cube[1])
                        face_set2 = next_cubes(face_set[4-vek][0], cube[0])
                        if vek == 1: # UP
                            cube = [face_set2[3][0], face_set2[2][0]]
                        elif vek == 3:  # DOWN
                            cube = [face_set2[3][0], face_set2[0][0]]
                        elif vek == 2:  # LEFT
                            cube = [face_set2[3][0], cube[1]]
                        elif vek == 4: # RIGHT
                            cube = [face_set2[3][0], cube[1]]

                        level[ny][nx] = [" ", " "]
                        level[nyp][nxp] = cube

                        if not undo:
                            moves += 1
                            moves_stack.append([vek,nyp,nxp])

            if scramble_move != 0:
                scramble_move -= 1
                moves_stack = []
                moves = 0
                continue

            ################################################################################
            ################################################################################
            # отрисовка кубиков на игровом поле

            solved = True
            x = y = 0  # координаты
            for row in level:  # вся строка
                for cube in row:  # каждый куб
                    if cube[0]==" ":
                        # пусто
                        pf = Surface((CUBE_SIZE, CUBE_SIZE))
                        pf.fill(Color(BACKGROUND_COLOR))
                        screen.blit(pf, (x, y))
                    elif cube[0]=="X":
                        # блок
                        pf = Surface((CUBE_SIZE-BORDER*2+2, CUBE_SIZE-BORDER*2+2))
                        pf.fill(Color(GRAY_COLOR))
                        screen.blit(pf, (x+BORDER, y+BORDER))
                        draw.line(screen, GRAY_COLOR2,(x+BORDER+TILE, y+BORDER+TILE),(x+BORDER+CUBE_SIZE-BORDER*2-TILE, y+BORDER+CUBE_SIZE-BORDER*2-TILE), 10)
                        draw.line(screen, GRAY_COLOR2,(x+BORDER+CUBE_SIZE-BORDER*2-TILE, y+BORDER+TILE),(x+BORDER+TILE, y+BORDER+CUBE_SIZE-BORDER*2-TILE), 10)

                    else:
                        # кубик
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
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[0][0]:
                                draw.polygon(screen,COLOR_ONE[1], [[x+BORDER+TILE, y+CUBE_SIZE-BORDER-TILE],
                                                                   [x+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2, y+CUBE_SIZE-BORDER-TILE],
                                                                   [x+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2-SHIFT, y+CUBE_SIZE-BORDER-TILE+TILE],
                                                                   [x+BORDER+TILE+SHIFT, y+CUBE_SIZE-BORDER-TILE+TILE]] )
                                break

                        # левая плитка
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[1][0]:
                                draw.polygon(screen,COLOR_ONE[1], [[x+BORDER, y+BORDER+TILE+SHIFT],
                                                                   [x+BORDER+TILE, y+BORDER+TILE],
                                                                   [x+BORDER+TILE, y+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2],
                                                                   [x+BORDER, y+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2-SHIFT]] )
                                break

                        # задняя плитка
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[2][0]:
                                draw.polygon(screen,COLOR_ONE[1], [[x+BORDER+TILE+SHIFT, y+BORDER],
                                                                   [x+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2-SHIFT, y+BORDER],
                                                                   [x+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2, y+BORDER+TILE],
                                                                   [x+BORDER+TILE, y+BORDER+TILE]] )
                                break

                        # правая плитка
                        for nn,COLOR_ONE in enumerate(CUBE_COLOR):
                            if COLOR_ONE[0]==face_set[3][0]:
                                draw.polygon(screen,COLOR_ONE[1], [[x+CUBE_SIZE-BORDER-TILE, y+BORDER+TILE],
                                                                   [x+CUBE_SIZE-BORDER-TILE+TILE, y+BORDER+TILE+SHIFT],
                                                                   [x+CUBE_SIZE-BORDER-TILE+TILE, y+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2-SHIFT],
                                                                   [x+CUBE_SIZE-BORDER-TILE, y+BORDER+TILE+CUBE_SIZE-BORDER*2-TILE*2]] )
                                break

                    x += CUBE_SIZE
                y += CUBE_SIZE
                x = 0

            pygame.display.update()  # обновление и вывод всех изменений на экран

main()