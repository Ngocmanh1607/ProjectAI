import numpy as np
import os
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import astar
import DFS
import time
TIME_OUT = 1800

path_board = os.getcwd() + '/Testcases'
path_checkpoint = os.getcwd() + '/Checkpoints'
assets_path = os.getcwd() + '/images'


def get_boards():
    os.chdir(path_board)
    list_boards = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_board}/{file}"
            board = get_board(file_path)
            list_boards.append(board)
    return list_boards


def get_check_points():
    os.chdir(path_checkpoint)
    list_check_point = []
    for file in os.listdir():
        if file.endswith(".txt"):
            file_path = f"{path_checkpoint}/{file}"
            check_point = get_pair(file_path)
            list_check_point.append(check_point)
    return list_check_point


def format_check_points(check_points):
    result = []
    for check_point in check_points:
        result.append((check_point[0], check_point[1]))
    return result


def get_board(path):
    # Load testcase file and apply formatting
    filepath = f"{path}"
    result = np.loadtxt(filepath, dtype=str, delimiter=',')
    return result


def get_pair(path):
    # Load checkpoint file and return coordinate pair
    # (Convert f-string to regular string)
    filepath = f"{path}"
    result = np.loadtxt(filepath, dtype=int, delimiter=',')
    return result


maps = get_boards()
check_points = get_check_points()
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 640))
pygame.display.set_caption('Sokoban')
clock = pygame.time.Clock()
BACKGROUND = (0, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
'''
GET SOME ASSETS
'''
os.chdir(assets_path)
player = pygame.image.load(os.getcwd() + '/player.png')
player = pygame.transform.scale(player, (40, 40))
wall = pygame.image.load(os.getcwd() + '/wall.png')
box = pygame.image.load(os.getcwd() + '/box0.png')
box = pygame.transform.scale(box, (32, 32))
point = pygame.image.load(os.getcwd() + '/target.png')
point = pygame.transform.scale(point, (32, 32))
space = pygame.image.load(os.getcwd() + '/space.png')
space = pygame.transform.scale(space, (32, 32))
arrow_left = pygame.image.load(os.getcwd() + '/arrow_left.png')
arrow_right = pygame.image.load(os.getcwd() + '/arrow_right.png')
init_background = pygame.image.load(os.getcwd() + '/floor.png')
# scale
init_background = pygame.transform.scale(init_background, (640, 640))
'''
RENDER THE MAP FOR GAMEPLAY
'''


def renderMap(board):
    width = len(board[0])
    height = len(board)
    indent = (640 - width * 32) / 2.0
    for i in range(height):
        for j in range(width):
            screen.blit(space, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == '1':
                screen.blit(wall, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == 'b':
                screen.blit(box, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == 't':
                screen.blit(point, (j * 32 + indent, i * 32 + 250))
            if board[i][j] == 'p':
                screen.blit(player, (j * 32 + indent, i * 32 + 250))


# Map level
mapNumber = 0
# Algorithm to solve the game
algorithm = "Depth First Search"

sceneState = "init"
loading = False

''' SOKOBAN FUNCTION '''


def find_position_player(board):
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == 'p':
                return (i, j)
    return None


def find_path(board):
    path = []
    i = 0
    for i in range(len(board)):
        path.append(find_position_player(board[i]))
    return path


def move(path):
    position_player = find_position_player(maps[mapNumber])
    x = position_player[0]
    y = position_player[1]

    move_list = []
    for i in range(len(path)):
        cur_x = path[i][0]
        cur_y = path[i][1]

        if cur_x < x:
            move_list.append("up")
        elif cur_x > x:
            move_list.append("down")
        elif cur_y < y:
            move_list.append("left")
        elif cur_y > y:
            move_list.append("right")
        x = cur_x
        y = cur_y

    return move_list


def renderMoveList(move_list, max_display_lines, move_list_scroll):
    move_font = pygame.font.Font('gameFont.ttf', 20)
    move_text = move_font.render("Move List:", True, WHITE)
    move_rect = move_text.get_rect(topright=(600, 10))
    screen.blit(move_text, move_rect)

    move_list_font = pygame.font.Font('gameFont.ttf', 20)
    move_list_y = 40  # Điểm bắt đầu để hiển thị danh sách di chuyển

    # Tính toán chỉ số cuối cùng mà có thể hiển thị trên màn hình
    end_index = min(move_list_scroll + max_display_lines, len(move_list))

    for i in range(move_list_scroll, end_index):
        move = move_list[i]
        move_text = move_list_font.render(move, True, WHITE)
        move_rect = move_text.get_rect(topright=(600, move_list_y))
        screen.blit(move_text, move_rect)
        move_list_y += 20  # Khoảng cách giữa các mục trong danh sách

    pygame.display.flip()


def sokoban():
    running = True
    global sceneState
    global loading
    global algorithm
    global list_board
    global mapNumber
    stateLenght = 0
    currentState = 0
    found = True
    move_list = []
    # Khởi tạo biến move_list_scroll
    max_display_lines = 10
    while running:
        screen.blit(init_background, (0, 0))
        if sceneState == "init":
            # Choose map and display
            initGame(maps[mapNumber])
        if sceneState == "executing":
            move_list_scroll = -1
            path = []
            # Choose map
            list_check_point = check_points[mapNumber]
            if algorithm == "Depth First Search":
                time_start = time.time()
                print("DFS")
                list_board = DFS.DFS_search(maps[mapNumber], list_check_point)
                time_end = time.time()
                rounded_time = round(time_end - time_start, 3)
                print("Thời gian thực thi:", rounded_time, "giây")
            else:
                time_start = time.time()
                print("AStar")
                list_board = astar.AStar_Search(
                    maps[mapNumber], list_check_point)
                time_end = time.time()
                rounded_time = round(time_end - time_start, 3)
                print("Thời gian thực thi:", rounded_time, "giây")
            path = find_path(list_board[0])
            move_list = move(path)
            if len(list_board) > 0:
                sceneState = "playing"
                stateLenght = len(list_board[0])
                print(stateLenght)
                currentState = 0
            else:
                sceneState = "end"
                found = False

        if sceneState == "loading":
            loadingGame()
            sceneState = "executing"
        if sceneState == "end":
            if found:
                foundGame(list_board[0][stateLenght - 1])
            else:
                notfoundGame()
        if sceneState == "playing":

            mapSize = pygame.font.Font('gameFont.ttf', 30)
            mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
            mapRect = mapText.get_rect(center=(320, 100))
            screen.blit(mapText, mapRect)
            algorithmSize = pygame.font.Font('gameFont.ttf', 30)
            algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
            algorithmRect = algorithmText.get_rect(center=(320, 600))
            screen.blit(algorithmText, algorithmRect)

            clock.tick(2)
            renderMap(list_board[0][currentState])
            # In danh sách di chuyển lên màn hình
            if move_list_scroll < len(move_list) - max_display_lines:
                move_list_scroll += 1
                renderMoveList(move_list, max_display_lines,
                               move_list_scroll)

            currentState = currentState + 1
            if currentState == stateLenght:
                sceneState = "end"
                found = True
        # Check event when you press key board
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:

                # Press arrow key board to change level map
                if event.key == pygame.K_RIGHT and sceneState == "init":
                    if mapNumber < len(maps) - 1:
                        mapNumber = mapNumber + 1
                if event.key == pygame.K_LEFT and sceneState == "init":
                    if mapNumber > 0:
                        mapNumber = mapNumber - 1
                # Press ENTER key board to select level map and algorithm
                if event.key == pygame.K_RETURN:
                    if sceneState == "init":
                        sceneState = "loading"
                    if sceneState == "end":
                        sceneState = "init"
                # Press SPACE key board to switch algorithm
                if event.key == pygame.K_SPACE and sceneState == "init":
                    if algorithm == "Depth First Search":
                        algorithm = "A Star Search"
                    else:
                        algorithm = "Depth First Search"
        pygame.display.flip()
    pygame.quit()


''' DISPLAY MAIN SCENE '''
# DISPLAY INITIAL SCENE


def initGame(map):
    titleSize = pygame.font.Font('gameFont.ttf', 60)
    titleText = titleSize.render('sokoban', True, WHITE)
    titleRect = titleText.get_rect(center=(320, 80))
    screen.blit(titleText, titleRect)

    desSize = pygame.font.Font('gameFont.ttf', 20)
    desText = desSize.render('Now, select your map!!!', True, WHITE)
    desRect = desText.get_rect(center=(320, 140))
    screen.blit(desText, desRect)

    mapSize = pygame.font.Font('gameFont.ttf', 30)
    mapText = mapSize.render("Lv." + str(mapNumber + 1), True, WHITE)
    mapRect = mapText.get_rect(center=(320, 200))
    screen.blit(mapText, mapRect)

    screen.blit(arrow_left, (246, 188))
    screen.blit(arrow_right, (370, 188))

    algorithmSize = pygame.font.Font('gameFont.ttf', 30)
    algorithmText = algorithmSize.render(str(algorithm), True, WHITE)
    algorithmRect = algorithmText.get_rect(center=(320, 600))
    screen.blit(algorithmText, algorithmRect)
    renderMap(map)


def loadingGame():
    fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = fontLoading_2.render(
        'Loading game', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 100))
    screen.blit(text_2, text_rect_2)


def foundGame(map):

    font_1 = pygame.font.Font('gameFont.ttf', 30)
    text_1 = font_1.render('The problem is solved!!!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 600))
    screen.blit(text_2, text_rect_2)

    renderMap(map)


def notfoundGame():

    font_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = font_1.render('Oh no, I tried my best :(', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 100))
    screen.blit(text_1, text_rect_1)

    font_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = font_2.render('Press Enter to continue.', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 600))
    screen.blit(text_2, text_rect_2)


if __name__ == "__main__":
    sokoban()
