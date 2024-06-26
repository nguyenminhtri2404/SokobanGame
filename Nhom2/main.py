# ***********************************************************************************#
#------------------------------------------------------------------------------------#
#*********************  WELCOME TO SOKOBAN GAME MAKE BY TEAM 2  *********************#
#                Authors: 2001216232 - TRUONG LE BAO TRAN (LEADER)                   #
#                         2001216237 - NGUYEN MINH TRI                               #
#                         2001210747 - LE VIET TUAN KHAI                             #
#------------------------------------------------------------------------------------#
# ***********************************************************************************#



# Import thư viện
import pygame
from enum import Enum
import random
import sys
import time
from pygame.locals import *
import os
import psutil
from queue import Queue
from copy import copy, deepcopy
from datetime import datetime
import math
from sortedcontainers import SortedList
import numpy as np
from scipy.optimize import linear_sum_assignment


# Tạo màn hình game
pygame.init()
FPS = 60
WIDTH = 1280
HEIGHT = 720
clock = pygame.time.Clock()
pygame.display.set_caption("Nhóm 2 - Game đẩy thùng")
pygame.display.set_icon(pygame.image.load("Assets/textures/icon_game.png"))
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Tạo các màu
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_LIGHT = (231, 231, 231)
ORANGE = '#ff631c'
BLUE_LIGHT = (40, 53, 88)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
YELLOW_LIGHT = (255, 255, 51)
BROWN = (210, 105, 30)
PINK = (204, 0, 255)
GREEN_LIGHT = (0, 255, 140)
GREEN = (0, 255, 0)
GREEN_DARK = (0, 255, 0)


# Tạo các biến cần thiết
running = True
numsRow = 10
numsCol = 20
numsUnit = max(numsRow, numsCol) # Lấy số dòng hoặc số cột lớn nhất nhằm tạo ra ô vuông luôn có kích thước bằng nhau
lengthSquare = int(WIDTH/numsUnit) # Chiều dài của mỗi ô vuông

offsetX = (WIDTH - lengthSquare * numsCol) / 2 # Tọa độ X của màn hình game
offsetY = ((HEIGHT - lengthSquare * numsRow) / 2)+40 # Tọa độ Y của màn hình game

map_index = 0
level = 0
character = 0
box_selected = 0
goal_selected = 0
mode = 0
win = 0
step = 1
timeTook = 0
pushed = 0
startTime = 0
stepNode = 0
visualized = 0
moves = []
name = ''
actions = []
ptr = -1
VOCUC = 1e9
# Load các assets cần thiết
background = pygame.image.load("Assets/textures/bg_mainmenu.jpg")
background = pygame.transform.scale(background, (WIDTH, HEIGHT)) 

background_game = pygame.image.load("Assets/textures/bg_game.jpg")
background_game = pygame.transform.scale(background_game, (WIDTH, HEIGHT))

background_choose = pygame.image.load("Assets/textures/bg_choose.jpg")
background_choose = pygame.transform.scale(background_choose, (WIDTH, HEIGHT))

wall = pygame.image.load("Assets/textures/wall.jpg")
wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))

list_box = {
    0 : pygame.image.load("Assets/textures/box1.png"),
    1 : pygame.image.load("Assets/textures/box2.png"),
}

box = list_box[box_selected]
box = pygame.transform.scale(box, (lengthSquare, lengthSquare)) 

list_goal = {
    0 : pygame.image.load("Assets/textures/goal1.png"),
    1 : pygame.image.load("Assets/textures/goal2.png"),
}

goal = list_goal[goal_selected]
goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

path_test = pygame.image.load("Assets/textures/path.png")
path_test = pygame.transform.scale(path_test, (lengthSquare, lengthSquare))

list_player = {
    0: pygame.image.load("Assets/textures/player1.png"),
    1: pygame.image.load("Assets/textures/player2.png"),
    2: pygame.image.load("Assets/textures/player3.png")
}

pause = pygame.image.load("Assets/textures/pause.png")
pause = pygame.transform.scale(pause, (40, 40))

player_ = list_player[character]
player_size = (lengthSquare, lengthSquare)

board_credit = pygame.image.load("Assets/textures/board_credit.png")
board_credit = pygame.transform.scale(board_credit, (WIDTH/2, HEIGHT/2+60))

exit = pygame.image.load("Assets/textures/exit.png")
exit = pygame.transform.scale(exit, (lengthSquare, lengthSquare))

child_title = pygame.image.load("Assets/textures/accept.png")
child_title = pygame.transform.scale(child_title, (WIDTH/4, 100))

undo_img = pygame.image.load("Assets/textures/undo.png")
undo_img = pygame.transform.scale(undo_img, (40, 40))

redo_img = pygame.image.load("Assets/textures/redo.png")
redo_img = pygame.transform.scale(redo_img, (40, 40))

left = pygame.image.load("Assets/textures/left.png")
left = pygame.transform.scale(left, (30, 30))

right = pygame.image.load("Assets/textures/right.png")
right = pygame.transform.scale(right, (30, 30))

# Hàm lấy font
def get_font(size):
    return pygame.font.Font("Assets/font/font_menu.ttf", size)

def get_font_game(size):
    return pygame.font.Font("Assets/font/font_game.ttf", size)


levelFont = get_font(25)
buttonFont = get_font(25)
menuFont = get_font(55)
gameFont = get_font_game(25)


# Class Buttons
class Button():
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

# Cac nut trong game
START_BTN= Button(image=child_title, pos=(WIDTH/2, HEIGHT/2-50), text_input="Start", font=menuFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
CREDIT_BTN = Button(image=child_title, pos=(WIDTH/2, HEIGHT/2+100), text_input="Credits", font=menuFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
QUIT_BTN = Button(image=child_title, pos=(WIDTH/2, HEIGHT/2+250), text_input="Quit", font=menuFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
ACCEPT_BTN = Button(image=child_title, pos=(WIDTH/2, HEIGHT/2+200), text_input="Accept", font=menuFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
LEFT_BTN = Button(image=left, pos=(WIDTH/2-60, HEIGHT/2+92), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
RIGHT_BTN = Button(image=right, pos=(WIDTH/2+60, HEIGHT/2+92), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
BACK_BTN = Button(image=exit,pos=(WIDTH/2, HEIGHT/2+180),text_input="",font=get_font(30),base_color=(255,255,255),hovering_color=(255,0,0))


#Xử lí các nút
def check_one_digit(n):
    if len(str(n)) == 1:
        return True
    return False

def undo():
    global player, boxes, ptr, stepNode, pushed
    if ptr > -1:
        move = actions[ptr]
        boxes = set(boxes)
        if move[1] == 1:
            pushed -= 1
            boxes.remove((player[0] + move[0].vector[0], player[1] + move[0].vector[1]))
            boxes.add(player)
        boxes = tuple(boxes)
        player = (player[0] - move[0].vector[0], player[1] - move[0].vector[1])
        stepNode -= 1
        ptr -= 1

def redo():
    global player, boxes, ptr, stepNode, pushed
    if ptr < len(actions) - 1:
        _, is_pushed, player, boxes = move(player, boxes, actions[ptr + 1][0])
        ptr += 1
        stepNode += 1
        pushed += is_pushed

#=========================PHẦN THỰC HIỆN TRÒ CHƠI=========================
class Direction:

    def __init__(self, vector, char):
        self.vector = vector
        self.char = char

    def get_char(self):
        return self.char

L = Direction((-1, 0), 'L')
R = Direction((1, 0), 'R')
U = Direction((0, -1), 'U')
D = Direction((0, 1), 'D')
directions = [U, L, D, R] 


def is_win(goals, boxes):
    return goals.issubset(boxes)


def reset_data():
    global numsCol, numsRow, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player_, walls, goals, boxes, paths, player, name, distanceToGoal, listDeadPoint, actions, ptr
    
    wall = pygame.image.load('Assets/textures/wall.jpg')
    goal = list_goal[goal_selected]
    player_ = list_player[character]
    box = list_box[box_selected]
    name = "./Testcases/{}.txt".format(level+1)
    walls, goals, boxes, paths, player, numsRow, numsCol = readFile(name)
    distanceToGoal, listDeadPoint = set_distanceToGoals()
    actions = []
    ptr = -1

    numsRow = 10
    numsCol = 20

    numsUnit = max(numsCol, numsRow)
    lengthSquare = int(WIDTH/numsUnit)

    offsetX = (WIDTH - lengthSquare * numsCol)/2
    offsetY = ((HEIGHT - lengthSquare * numsRow)/2)+40

    wall = pygame.transform.scale(wall, (lengthSquare, lengthSquare))
    box = pygame.transform.scale(box, (lengthSquare, lengthSquare))
    goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))
    player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

def init_data():
    global move, win, step, timeTook, pushed, startTime, stepNode, level, board, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY, visualized, actions,mode
    mode = 1
    win = 0
    step = 2
    timeTook = 0
    pushed = 0
    startTime = 0
    stepNode = 0
    visualized = 0
    actions = []
    reset_data()


def readFile(filename):
    walls = set()
    goals = set()
    boxes = []
    paths = set()
    player = None
    x = 0
    y = 0
    with open(filename, 'r') as f:
        read_data = f.read()
        lines = read_data.split('\n')	
        for line in lines:
            x = 0
            for char in line:
                if char == '#': # Wall
                    walls.add((x,y))
                elif char == 'x': # Box
                    boxes.append((x,y))
                    paths.add((x,y))
                elif char == '?': # Goal
                    goals.add((x,y))
                    paths.add((x,y))
                elif char == '@': # Player
                    player = (x,y)
                    paths.add((x,y))
                elif char == '-': # Player and Goal
                    goals.add((x,y))
                    player = (x,y)
                    paths.add((x,y))
                elif char == '+': # Box and Goal
                    goals.add((x,y))
                    boxes.append((x,y))
                    paths.add((x,y))
                elif char == '.': # Path
                    paths.add((x,y))
                x += 1
            y += 1
    return walls, goals, tuple(boxes), paths, player, x, y

def set_distanceToGoals():
    distanceToGoal = dict()
    listDeadPoints = set()
    for goal in goals:
        distanceToGoal[goal] = dict()
        for path in paths:
            distanceToGoal[goal][path] = VOCUC
    queue = Queue()
    for goal in goals:
        distanceToGoal[goal][goal] = 0
        queue.put(goal)
        while not queue.empty():
            position = queue.get()
            for direction in directions:
                boxPos = (position[0] + direction.vector[0], position[1] + direction.vector[1])
                playerPos = (position[0] + 2*direction.vector[0], position[1] + 2*direction.vector[1])
                if (boxPos in paths) and (playerPos not in walls) and (distanceToGoal[goal][boxPos] == VOCUC) :  #nếu chưa tính k/c thì thực hiện tính
                    distanceToGoal[goal][boxPos] = distanceToGoal[goal][position] + 1
                    queue.put(boxPos)
    # Add dead point
    for path in paths:
        is_deadPoint = True
        for goal in goals:	
            if distanceToGoal[goal][path] != VOCUC:
                is_deadPoint = False
                break
        if is_deadPoint == True:
            listDeadPoints.add(path)
    return distanceToGoal, listDeadPoints


def available_direction(player, boxes): 
    available_moves = []
    for direction in directions:
        if (player[0] + direction.vector[0], player[1] + direction.vector[1]) not in walls: # phía trước có thể là đường trống hoặc thùng
            if (player[0] + direction.vector[0], player[1] + direction.vector[1]) in boxes: # xét phía trước là thùng --> và trước thùng đó phải là đường trống
                if ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in walls) and ((player[0] + 2*direction.vector[0], player[1] + 2*direction.vector[1]) not in boxes):
                    available_moves.append(direction)
            else: # xét phía trước là đường trống
                available_moves.append(direction)
    return available_moves

def move(player, boxes, direction):
    temp = (player[0] + direction.vector[0], player[1] + direction.vector[1])
    pushed = 0
    flag = True #đánh dấu đường đi hợp lệ
    boxes = set(boxes)
    
    if temp in boxes:
        pushed = 1
        boxes.remove(temp)
        new_box = (player[0] + 2 * direction.vector[0], player[1] + 2 * direction.vector[1])
        boxes.add(new_box)
        
        if new_box in listDeadPoint:
            flag = False

    boxes = tuple(sorted(boxes)) #sắp xếp các thùng để duy trì thứ tự trong danh sách
    
    player = temp
    return flag, pushed, player, boxes

#=========================PHẦN THUẬT TOÁN=========================

def bfs(current_player, current_boxes):
    global win, timeTook, startTime
    listState = Queue()
    visited = set()
    listState.put((current_player, current_boxes, 0, 0, []))
    visited.add((current_player, current_boxes))
    startTime = time.time()
    while True:
        if listState.empty():
            return ( 0, 0, [])

        (now_player, now_boxes, numOfsteps, numOfpush, listMoves) = listState.get()
        moves = available_direction(now_player,now_boxes)
        for m in moves:
            flag, pushed, new_player, new_boxes = move(now_player, now_boxes, m)
            if (new_player, new_boxes) not in visited and flag == True: #flag là cờ đánh dấu đường đi hợp lệ
                visited.add((new_player, new_boxes))
                if is_win(goals, new_boxes):							
                    timeTook = time.time() - startTime
                    win = 1
                    return ( numOfsteps + 1, timeTook, listMoves + [(m,pushed)])
                listState.put((new_player, new_boxes, numOfsteps+1, numOfpush + pushed, listMoves + [(m,pushed)]))


def heuristic( boxes):
    temp = []
    for goal in goals:
        for box in boxes:
            temp.append(distanceToGoal[goal][box])

    arr = np.array(temp)
    cost = arr.reshape(len(goals), len(boxes))
    row_ind, col_ind = linear_sum_assignment(cost) # Hungarian Algorithm
    return cost[row_ind, col_ind].sum()

def cost_Fn(step, boxes):
    return heuristic(boxes) + step # f(n) = g(n) + h(n)
               
def A_star(current_player, current_boxes):
	global win, timeTook, startTime
	listState = SortedList(key=lambda x: cost_Fn(x[2], x[1])) #x[1] là boxes và x[2] là numOfsteps
	visited = set()
	listState.add((current_player, current_boxes, 0, 0, [])) #(player, boxes, numOfsteps, numOfpush, listMoves=[(direction, pushed)])
	visited.add((current_player, current_boxes))
	startTime = time.time()
	while True:
		if len(listState) == 0:
			return ( 0, 0, [])

		(now_player, now_boxes, numOfsteps, numOfpush, listMoves) = listState.pop(0)
		print(f"Trang thai dang xet: Player={now_player}")
		listDirection = available_direction(now_player,now_boxes)
		for d in listDirection:
			flag, pushed, new_player, new_boxes = move(now_player, now_boxes, d)
			if (new_player, new_boxes) not in visited and flag == True: #flag là cờ đánh dấu đường đi hợp lệ
				visited.add((new_player, new_boxes))
				if is_win(goals, new_boxes):
					timeTook = time.time() - startTime
					win = 1
					return (numOfsteps + 1, timeTook, listMoves + [(d,pushed)])
				listState.add((new_player, new_boxes, numOfsteps + 1, numOfpush + pushed, listMoves + [(d,pushed)]))


def Hill_climbing(curr_player, curr_boxes):
    global win, timeTook, startTime  
    visited = set()
    now_state = (curr_player, curr_boxes, 0, 0, [])
    visited.add((curr_player, curr_boxes))
    startTime = time.time()
    while True:
        if not any(now_state): #GAME OVER
            return ( 0, 0, [])
        (now_player, now_boxes, numOfsteps, numOfpush, listMoves) = now_state #trạng thái đang xét
        print(" Trang thai dang xet player=:", {now_player})
        
        best_state= now_state #gán tt htai là tt tốt nhất
        best_heuristic = heuristic(now_boxes) #gán heuristiu của tt htai là heuristic tốt nhất

        listDirection = available_direction(now_player, now_boxes) #tìm các hướng trạng thái kế tiếp
        for d in reversed(listDirection):
            flag, pushed, new_player, new_boxes = move(now_player, now_boxes, d) #tính toạ độ của từng láng giềng
            if (new_player, new_boxes) not in visited and flag == True: #nếu chưa xét và không phải vật cản
                if heuristic(new_boxes) <= best_heuristic:
                    best_heuristic= heuristic(new_boxes)
                    best_state= (new_player, new_boxes, numOfsteps + 1, numOfpush + pushed, listMoves + [(d, pushed)])

        visited.add((best_state[0], best_state[1]))
        if is_win(goals, best_state[1]): #WIN
            timeTook = time.time() - startTime
            win = 1
            return (best_state[2], timeTook, best_state[4])
        now_state = best_state




#=========================PHẦN GIAO DIỆN=========================

snow = []

for i in range(100):
    x = random.randrange(0,1280)
    y = random.randrange(0,720)
    snow.append([x,y])


#---MÀN HÌNH CHÍNH
def draw_main_menu():
    screen.blit(background, (0, 0))

    for ice in range(len(snow)): 
            pygame.draw.circle(screen, 'white', snow[ice],3)
            snow[ice][1]+=1 
            if snow[ice][1]>720:  
        
                snow[ice][1] = random.randrange(-50,-10)
                snow[ice][0] = random.randrange(0,1280)

    MENU_TEXT = get_font(75).render("SOKOBAN GAME", True, YELLOW)
    MENU_TEXT_RECT = MENU_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-200))
    screen.blit(MENU_TEXT, MENU_TEXT_RECT)
    
    START_BTN.changeColor(pygame.mouse.get_pos())
    START_BTN.update(screen)
    
    CREDIT_BTN.changeColor(pygame.mouse.get_pos())
    CREDIT_BTN.update(screen)
    
    QUIT_BTN.changeColor(pygame.mouse.get_pos())
    QUIT_BTN.update(screen)

    COPYRIGHT_TEXT = get_font(20).render("© 2023 - NHOM 2 - TTK", True, YELLOW)
    COPYRIGHT_TEXT_RECT = COPYRIGHT_TEXT.get_rect(center=(offsetX+200, HEIGHT/2+245))
    screen.blit(COPYRIGHT_TEXT, COPYRIGHT_TEXT_RECT)

#-------MÀN HÌNH CREDITS-------
def draw_credits():
    run= True
    while run:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()
        screen.blit(background, (0, 0))

        for ice in range(len(snow)): 
            pygame.draw.circle(screen, 'white', snow[ice],3)
            snow[ice][1]+=1 
            if snow[ice][1]>720:  
                snow[ice][1] = random.randrange(-50,-10)
                snow[ice][0] = random.randrange(0,1280)

        CREDITS_BACK = Button(image=exit,pos=(WIDTH/2, HEIGHT/2+180),text_input="",font=get_font(30),base_color=(255,255,255),hovering_color=(255,0,0))
        CREDITS_BACK.update(screen)
        screen.blit(board_credit, (WIDTH/2-320, HEIGHT/2-320))

        CREDITS_TEXT = get_font(48).render("CREDITS", True, WHITE)
        CREDITS_TEXT_RECT = CREDITS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-298))
        screen.blit(CREDITS_TEXT, CREDITS_TEXT_RECT)

        CREDITS_NAME = get_font(40).render("TEAM 2", True, RED)
        CREDITS_NAME_RECT = CREDITS_NAME.get_rect(center=(WIDTH/2, HEIGHT/2-250))
        screen.blit(CREDITS_NAME, CREDITS_NAME_RECT)

        CREDITS_NAME = get_font(25).render("2001216232 - Truong Le Bao Tran (Leader)", True, BLACK)
        CREDITS_NAME_RECT = CREDITS_NAME.get_rect(center=(WIDTH/2, HEIGHT/2-200))
        screen.blit(CREDITS_NAME, CREDITS_NAME_RECT)

        CREDITS_NAME = get_font(25).render("2001216237 - Nguyen Minh Tri", True, BLACK)
        CREDITS_NAME_RECT = CREDITS_NAME.get_rect(center=(WIDTH/2, HEIGHT/2-150))
        screen.blit(CREDITS_NAME, CREDITS_NAME_RECT)

        CREDITS_NAME = get_font(25).render("2001210747 - Le Viet Tuan Khai", True, BLACK)
        CREDITS_NAME_RECT = CREDITS_NAME.get_rect(center=(WIDTH/2, HEIGHT/2-100))
        screen.blit(CREDITS_NAME, CREDITS_NAME_RECT)

        CREDITS_TEXT = get_font(35).render("THANK YOU FOR PLAYING GAME!", True, RED)
        CREDITS_TEXT_RECT = CREDITS_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2))
        screen.blit(CREDITS_TEXT, CREDITS_TEXT_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                    if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                        run = False
                        print("Back")
                        draw_main_menu()
        pygame.display.update()

#-------MÀN HÌNH CHỌN LEVEL VÀ NHÂN VẬT-------
def draw_set_choose():
    run = True
    global level, character, step, mode, box_selected, goal_selected
    while run:
        # screen.fill((0, 0, 0))
        screen.blit(background_choose, (0, 0))

        for ice in range(len(snow)): 
            pygame.draw.circle(screen, 'white', snow[ice],3)
            snow[ice][1]+=1 
            if snow[ice][1]>720:  
        
                snow[ice][1] = random.randrange(-50,-10)
                snow[ice][0] = random.randrange(0,1280)

        SET_CHOOSE_TEXT = get_font(65).render("SET CHOOSE", True, WHITE)
        SET_CHOOSE_TEXT_RECT = SET_CHOOSE_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-310))
        screen.blit(SET_CHOOSE_TEXT, SET_CHOOSE_TEXT_RECT)

        title_board = pygame.image.load("Assets/textures/accept.png")
        title_board = pygame.transform.scale(title_board, (WIDTH/3, 60))
        screen.blit(title_board, (WIDTH/2-206, HEIGHT/2-260))
        TITLE_TEXT = get_font(32).render("Choose character", True, WHITE)
        TITLE_TEXT_RECT = TITLE_TEXT.get_rect(center=(WIDTH/2+8, HEIGHT/2-235))
        screen.blit(TITLE_TEXT, TITLE_TEXT_RECT)
        
        player1_thum = pygame.image.load("Assets/textures/player1.png")
        player1_thum = pygame.transform.scale(player1_thum, (150, 150))
        player1_btn = Button(image=player1_thum, pos=(WIDTH/2-200, HEIGHT/2-100), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
        player1_btn.update(screen)

        player2_thum = pygame.image.load("Assets/textures/player2.png")
        player2_thum = pygame.transform.scale(player2_thum, (150, 150))
        player2_btn = Button(image=player2_thum, pos=(WIDTH/2, HEIGHT/2-100), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
        player2_btn.update(screen)

        player3_thum = pygame.image.load("Assets/textures/player3.png")
        player3_thum = pygame.transform.scale(player3_thum, (150, 150))
        player3_btn = Button(image=player3_thum, pos=(WIDTH/2+200, HEIGHT/2-100), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GRAY_LIGHT)
        player3_btn.update(screen)


        title_board = pygame.image.load("Assets/textures/accept.png")
        title_board = pygame.transform.scale(title_board, (WIDTH/3, 60))
        screen.blit(title_board, (WIDTH/2-206, HEIGHT/2))
        TITLE_TEXT = get_font(32).render("Choose level", True, WHITE)
        TITLE_TEXT_RECT = TITLE_TEXT.get_rect(center=(WIDTH/2+8, HEIGHT/2+26))
        screen.blit(TITLE_TEXT, TITLE_TEXT_RECT)

        LEVEL_TEXT = get_font(40).render(f"{level+1}", True, WHITE)
        if check_one_digit(level):
            LEVEL_TEXT_RECT = LEVEL_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2+90))
        else:
            LEVEL_TEXT_RECT = LEVEL_TEXT.get_rect(center=(WIDTH/2+2, HEIGHT/2+90))
        screen.blit(LEVEL_TEXT, LEVEL_TEXT_RECT)

        

        LEFT_BTN.update(screen)
        RIGHT_BTN.update(screen)

        ACCEPT_BTN.changeColor(pygame.mouse.get_pos())
        ACCEPT_BTN.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    draw_main_menu()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if step == 1:
                    if LEFT_BTN.checkForInput(pygame.mouse.get_pos()):
                        level = (level+9)%10
                        print("Left")
                        print(level)
                    if RIGHT_BTN.checkForInput(pygame.mouse.get_pos()):
                        level = (level+1)%10
                        print("Right")
                        print(level)
                    if player1_btn.checkForInput(pygame.mouse.get_pos()):
                        character = 0
                        box_selected
                        print("Player 1")
                        print(character)
                    if player2_btn.checkForInput(pygame.mouse.get_pos()):
                        character = 1
                        box_selected = 1
                        goal_selected = 1
                        print("Player 2")
                        print(character)
                    if player3_btn.checkForInput(pygame.mouse.get_pos()):
                        character = 2
                        box_selected = 0
                        print("Player 3")
                        print(character)
                    if ACCEPT_BTN.checkForInput(pygame.mouse.get_pos()):
                        run = False
                        print("Accept")
                        step = 2
                        mode = 1
                        draw_game(character, level, box_selected, goal_selected)
        pygame.display.update()
        
#-------MÀN HÌNH VẼ MÀN CHƠI-------
def draw_board(player_,box,goal):
    # Trích xuât điểm của map
    all_points = walls.union(paths).union(goals).union(boxes).union({player})
    
    # Tính toán size của map
    max_row = max(point[1] for point in all_points)
    max_col = max(point[0] for point in all_points)

    numsRow = max_row + 1
    numsCol = max_col + 1

    # Tính toán tâm màn hình
    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    # Tính điểm bắt đầu vẽ
    start_x = center_x - (lengthSquare * numsCol) / 2
    start_y = center_y - (lengthSquare * numsRow) / 2 + 40

    for point in walls:
        screen.blit(wall, [start_x + lengthSquare * point[0], start_y + lengthSquare * point[1]])

    for point in paths:
        screen.blit(path_test,[start_x + lengthSquare * point[0], start_y + lengthSquare * point[1], lengthSquare, lengthSquare])

    for point in goals:
        screen.blit(goal, [start_x + lengthSquare * point[0], start_y + lengthSquare * point[1]])

    screen.blit(player_, [start_x + lengthSquare * player[0], start_y + lengthSquare * player[1]])

    for point in boxes:
        screen.blit(box, [start_x + lengthSquare * point[0], start_y + lengthSquare * point[1]])

    pygame.display.flip()


#-------VẼ MÀN HÌNH GAME------
def draw_game(character, level, box_selected, goal_selected):
    run = True
    show_BFS_btn = True
    show_A_STAR_btn = True
    show_HILL_CLIMBING_btn = True
    show_RUN_btn = False
    pygame.mixer_music.load("Assets/sounds/playsong.mp3")
    pygame.mixer_music.play(-1)
    global mode, win, step, timeTook, pushed, startTime, stepNode, visualized, moves, actions, ptr, clock, itemMemory,walls, goals, boxes, paths, player, numsRow, numsCol, numsUnit, lengthSquare, offsetX, offsetY, wall, box, goal, player_, distanceToGoal, listDeadPoint
    player_ = list_player[character]
    player_ = pygame.transform.scale(player_, (lengthSquare, lengthSquare))

    box = list_box[box_selected]
    box = pygame.transform.scale(box, (lengthSquare, lengthSquare)) 

    goal = list_goal[goal_selected]
    goal = pygame.transform.scale(goal, (lengthSquare, lengthSquare))

    name = "./Testcases/{}.txt".format(level+1)
    walls, goals, boxes, paths, player, numsRow, numsCol = readFile(name)
    distanceToGoal, listDeadPoint = set_distanceToGoals()

    while run:
        clock.tick(FPS)
        screen.fill((0, 0, 0))
        screen.blit(background_game, (0, offsetY))
        for ice in range(len(snow)): 
            pygame.draw.circle(screen, 'white', snow[ice],3)
            snow[ice][1]+=1 
            if snow[ice][1]>720:  
        
                snow[ice][1] = random.randrange(-50,-10)
                snow[ice][0] = random.randrange(0,1280)

        if not (mode >= 2 and win == 0):
            time_Title = levelFont.render("Time: ", True, WHITE)
            screen.blit(time_Title, (offsetX+20, offsetY-80))
            if (timeTook < 60):
                time_text = gameFont.render("{:0.4f} s".format(timeTook), True, WHITE)
            else:
                time_text = gameFont.render("{:0.4f} s".format(timeTook), True, RED)
            screen.blit(time_text, (offsetX+110, offsetY-73))
                
            step_Title = levelFont.render("Step: ", True, WHITE)
            screen.blit(step_Title, (offsetX+20, offsetY-40))
            step_text = gameFont.render(f"{stepNode}", True, WHITE)
            screen.blit(step_text, (offsetX+110, offsetY-33))

            pushed_Title = levelFont.render("Pushed: ", True, WHITE)
            screen.blit(pushed_Title, (offsetX+230, offsetY-80))
            pushed_text = gameFont.render(f"{pushed}", True, WHITE)
            screen.blit(pushed_text, (offsetX+350, offsetY-73))

        level_Title = levelFont.render("Level: ", True, WHITE)
        screen.blit(level_Title, (offsetX+230, offsetY-40))
        level_text = gameFont.render(f"{level+1}", True, WHITE)
        screen.blit(level_text, (offsetX+350, offsetY-33))
        #--- Nền button
        title_board = pygame.image.load("Assets/textures/accept.png")
        title_board = pygame.transform.scale(title_board, (100, 40))

        title_board2 = pygame.image.load("Assets/textures/accept.png")
        title_board2 = pygame.transform.scale(title_board2, (130, 40))

        title_board3 = pygame.image.load("Assets/textures/accept.png")
        title_board3 = pygame.transform.scale(title_board, (80, 35))


    #--- CÁC NÚT TRONG GAME
        BFS_BTN = Button(image=title_board, pos=(offsetX+450, offsetY-60), text_input="BFS", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        BFS_BTN.changeColor(pygame.mouse.get_pos())
        if show_BFS_btn == True:
            BFS_BTN.update(screen)
  

        A_STAR_BTN = Button(image=title_board, pos=(offsetX+570, offsetY-60), text_input="A*", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        A_STAR_BTN.changeColor(pygame.mouse.get_pos())
        if show_A_STAR_btn == True:
            A_STAR_BTN.update(screen)


        HILL_CLIMBING_BTN = Button(image=title_board, pos=(offsetX+690, offsetY-60), text_input="Hill", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        HILL_CLIMBING_BTN.changeColor(pygame.mouse.get_pos())
        if show_HILL_CLIMBING_btn == True:
            HILL_CLIMBING_BTN.update(screen)


        RUN_BTN = Button(image=title_board3, pos=(offsetX+570, offsetY-20), text_input="Run", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        RUN_BTN.changeColor(pygame.mouse.get_pos())
        if show_RUN_btn == True:
            RUN_BTN.update(screen)

        UNDO_BTN = Button(image=undo_img, pos=(offsetX+980, offsetY-40), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        UNDO_BTN.update(screen)

        RESTART_BTN = Button(image=title_board2, pos=(offsetX+1080, offsetY-40), text_input="Restart", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        RESTART_BTN.changeColor(pygame.mouse.get_pos())
        RESTART_BTN.update(screen)

        REDO_BTN = Button(image=redo_img, pos=(offsetX+1180, offsetY-40), text_input="", font=buttonFont, base_color=WHITE, hovering_color=GREEN_DARK)
        REDO_BTN.update(screen)
        
        SLOVING_TEXT = get_font(20).render("WAITING", True, WHITE)
        SLOVING_TEXT_RECT = SLOVING_TEXT.get_rect(center=(WIDTH/2-65, HEIGHT/2-300))

        #-- Xử lý game---
        if is_win(goals, boxes) == True and mode == 1:
            win = 1
            WIN_TEXT = get_font(75).render("YOU WIN", True, YELLOW)
            WIN_TEXT_RECT = WIN_TEXT.get_rect(center=(WIDTH/2, HEIGHT/2-330))
            screen.blit(WIN_TEXT, WIN_TEXT_RECT)
            pygame.mixer_music.stop()

        #-- Các chế độ chơi
        if step == 3 and win == 0 and mode == 1: # Chế độ tự chơi
            timeTook = time.time() - startTime
        
        #--- Các thuật toán
        if step == 3 and mode == 2 and win == 0:
            (steps, times, moves) = bfs(player, boxes) #BFS

        if step == 3 and mode == 3 and win == 0:
            (steps, times, moves) = A_star(player, boxes) #A STAR
        
        if step == 3 and mode == 4 and win == 0:
            ( steps, times, moves) = Hill_climbing(player, boxes) #LEO ĐỒI DỐC ĐỨNG

        if len(moves) > 0 and visualized == 1:
            (_, is_pushed, player, boxes) = move(player, boxes, moves[0][0])
            actions.append(moves[0])
            moves.pop(0)
            stepNode += 1
            pushed += is_pushed
            ptr += 1
            time.sleep(0.3) # Delay 0.3s

        for event in pygame.event.get():
            keys_pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT or keys_pressed[pygame.K_q]:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    draw_set_choose()
    
            if step == 2:
                if event.type == KEYDOWN:
                    step = 3
                    show_BFS_btn = False
                    show_A_STAR_btn = False
                    show_HILL_CLIMBING_btn = False
                    startTime = time.time()
            mouse = pygame.mouse.get_pos()
            x = mouse[0]
            y = mouse[1]
    
    #-----CHẾ ĐỘ THUẬT TOÁN-----
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("x: ", x,"-", " y: ", y)
                if step == 2:
                    if BFS_BTN.checkForInput(pygame.mouse.get_pos()): 
                        mode = 2
                        step = 3
                        print("BFS")
                        print("Mode: ", mode)
                        print("Step: ", step)
                        show_A_STAR_btn = False
                        show_HILL_CLIMBING_btn = False
                        show_RUN_btn = True
                        screen.blit(SLOVING_TEXT, SLOVING_TEXT_RECT)
                        continue

                    if A_STAR_BTN.checkForInput(pygame.mouse.get_pos()): 
                        mode = 3
                        step = 3
                        show_BFS_btn = False
                        show_HILL_CLIMBING_btn = False
                        show_RUN_btn = True
                        screen.blit(SLOVING_TEXT, SLOVING_TEXT_RECT)
                        continue

                    if HILL_CLIMBING_BTN.checkForInput(pygame.mouse.get_pos()):
                        mode = 4
                        step = 3
                        show_BFS_btn = False
                        show_A_STAR_btn = False
                        show_RUN_btn = True
                        screen.blit(SLOVING_TEXT, SLOVING_TEXT_RECT)
                        continue
                    
                if step == 3:
                    if mode == 1:
                        if RESTART_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Restart")
                            init_data()
                            draw_game(character, level, box_selected, goal_selected)
                        if UNDO_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Undo")
                            undo()
                        if REDO_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Redo")
                            redo()
                    if mode == 2:
                        if RESTART_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Restart")
                            init_data()
                            draw_game(character, level, box_selected, goal_selected)
                        if win == 1:
                            if visualized == 0:
                                if RUN_BTN.checkForInput(pygame.mouse.get_pos()):
                                    visualized = 1
                                    print("Run")
                                else:
                                    if UNDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Undo")
                                        undo()
                                    if REDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Redo")
                                        redo()
                    if mode == 3:
                        if RESTART_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Restart")
                            init_data()
                            draw_game(character, level, box_selected, goal_selected)
                        if win == 1:
                            if visualized == 0:
                                if RUN_BTN.checkForInput(pygame.mouse.get_pos()):
                                    visualized = 1
                                    print("Run")
                                else:
                                    if UNDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Undo")
                                        undo()
                                    if REDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Redo")
                                        redo()
                    if mode == 4:
                        if RESTART_BTN.checkForInput(pygame.mouse.get_pos()):
                            print("Restart")
                            init_data()
                            draw_game(character, level, box_selected, goal_selected)
                        if win == 1:
                            if visualized == 0:
                                if RUN_BTN.checkForInput(pygame.mouse.get_pos()):
                                    visualized = 1
                                    print("Run")
                                else:
                                    if UNDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Undo")
                                        undo()
                                    if REDO_BTN.checkForInput(pygame.mouse.get_pos()):
                                        print("Redo")
                                        redo()
                    
            
    #--- CHẾ ĐỘ TỰ CHƠI---
            if event.type == pygame.KEYDOWN:        
                if step == 3:
                    if mode == 1 and win == 0:
                        if event.key == pygame.K_w or event.key == pygame.K_UP:
                            if U in available_direction(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr+1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, U)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((U, is_pushed))
                        elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                            if D in available_direction(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr+1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, D)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((D, is_pushed))
                        elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                            if L in available_direction(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr+1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, L)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((L, is_pushed))
                        elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                            if R in available_direction(player, boxes):
                                if ptr + 1 < len(actions):
                                    actions = actions[0:(ptr+1)]
                                (_, is_pushed, player, boxes) = move(player, boxes, R)
                                stepNode += 1
                                pushed += is_pushed
                                ptr += 1
                                actions.append((R, is_pushed))

        draw_board(player_,box,goal)
        pygame.display.update()

# Main
if __name__ == '__main__':
    pygame.mixer_music.load("Assets/sounds/themesong.mp3")
    pygame.mixer_music.play(-1)
    while running:
        clock.tick(FPS)
        draw_main_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if START_BTN.checkForInput(pygame.mouse.get_pos()):
                    print("Start")
                    draw_set_choose()
                if CREDIT_BTN.checkForInput(pygame.mouse.get_pos()):
                    print("Credit")
                    draw_credits()
                if QUIT_BTN.checkForInput(pygame.mouse.get_pos()):
                    running = False
                    print("Quit")
                    sys.exit()
        pygame.display.update()