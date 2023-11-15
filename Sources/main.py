import numpy as np
import os
from copy import deepcopy
import pygame
from pygame.constants import KEYDOWN
import astar

''' TIME OUT FOR ALL ALGORITHM : 30 MIN ~ 1800 SECONDS '''
TIME_OUT = 1800
''' GET THE TESTCASES AND CHECKPOINTS PATH FOLDERS '''
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


''' READ A SINGLE CHECKPOINT TXT FILE '''


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
algorithm = "A STAR"

sceneState = "init"
loading = False

''' SOKOBAN FUNCTION '''


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

    while running:
        screen.blit(init_background, (0, 0))
        if sceneState == "init":
            # Choose map and display
            initGame(maps[mapNumber])

        if sceneState == "executing":
            # Choose map
            list_check_point = check_points[mapNumber]
            print("AStar")
            list_board = astar.AStart_Search(
                maps[mapNumber], list_check_point)
            if len(list_board) > 0:
                sceneState = "playing"
                stateLenght = len(list_board[0])
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
            clock.tick(2)
            renderMap(list_board[0][currentState])
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
                    algorithm = "A Star Search"
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
    fontLoading_1 = pygame.font.Font('gameFont.ttf', 40)
    text_1 = fontLoading_1.render('SHHHHHHH!', True, WHITE)
    text_rect_1 = text_1.get_rect(center=(320, 60))
    screen.blit(text_1, text_rect_1)

    fontLoading_2 = pygame.font.Font('gameFont.ttf', 20)
    text_2 = fontLoading_2.render(
        'The problem is being solved, stay right there!', True, WHITE)
    text_rect_2 = text_2.get_rect(center=(320, 100))
    screen.blit(text_2, text_rect_2)


def foundGame(map):

    font_1 = pygame.font.Font('gameFont.ttf', 30)
    text_1 = font_1.render('Yeah! The problem is solved!!!', True, WHITE)
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
