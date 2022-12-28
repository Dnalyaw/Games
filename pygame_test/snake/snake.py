import pygame
import math
import random
import tkinter as tk
from tkinter import messagebox

pygame.init()

pygame.display.set_caption("Snake")

class cube(object):
    rows = 20
    w = 500

    def __init__(self, start, dirnx=1, dirny=0, color=(0, 255, 0)):
        self.pos = start
        self.dirnx = 1
        self.dirny = 0
        self.color = color

    def move(self, dirnx, dirny):
        self.dirnx = dirnx
        self.dirny = dirny
        self.pos = (self.pos[0] + self.dirnx, self.pos[1] + self.dirny)#changing position

    def draw(self, surface, eyes=False):
        dis = self.w // self.rows#length and width of cube to one cube length
        i = self.pos[0]#current row
        j = self.pos[1]#current column

        pygame.draw.rect(surface, self.color, (i*dis+1, j*dis+1, dis-2, dis-2))#draws apple as rectangle, but changed to be a bit smaller so can see grid
        if eyes:  # Draws the eyes
            centre = dis // 2
            radius = 3
            circleMiddle = (i * dis + centre - radius, j * dis + 8)
            circleMiddle2 = (i * dis + dis - radius * 2, j * dis + 8)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle, radius)
            pygame.draw.circle(surface, (0, 0, 0), circleMiddle2, radius)

class Snake(object):
    body = []
    turns = {}
    def __init__(self, color, pos):
        self.color = color
        self.head = cube(pos)
        self.body.append(self.head)
        self.dirnx = 0
        self.dirny = 1
        self.left = False
        self.right = True
        self.up = False
        self.down = False

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_LEFT]:
                    print("hi")
                    self.dirnx = -1#x goes down by one when going left
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]#self.head.pos is the current position of the head of the snake. The line says that we have a full turn at dirnx and dirny
                elif keys[pygame.K_RIGHT]:
                    self.dirnx = 1  # x goes down by one when going left
                    self.dirny = 0
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]#adding turns that happen into a turn list
                elif keys[pygame.K_UP]:
                    self.dirnx = 0  # x goes down by one when going left
                    self.dirny = -1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
                elif keys[pygame.K_DOWN]:
                    self.dirnx = 0  # x goes down by one when going left
                    self.dirny = 1
                    self.turns[self.head.pos[:]] = [self.dirnx, self.dirny]
        #this is so each cube turns in a direction when the input tells it to turn
        for i, c in enumerate(self.body):#for all squares, turn on that square; i,c is index, cube
            p = c.pos[:]# [:] makes a copy so it's not actually changing the original; p is the cube's position
            if p in self.turns:#for every cube in the snake's body, if that cube's position is in the turn list
                turn = self.turns[p]#gets the direction that we should turn
                c.move(turn[0], turn[1])#move in that turn for that position
                if i == len(self.body)-1:#once that move reaches the end of the snake, then remove that turn
                    self.turns.pop(p)
            else:  # If we are not turning the cube
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0:
                    c.pos = (c.rows - 1, c.pos[1])
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    c.pos = (0, c.pos[1])
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    c.pos = (c.pos[0], 0)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    c.pos = (c.pos[0], c.rows - 1)
                else:
                    c.move(c.dirnx, c.dirny)  # If we haven't reached the edge just move in our current direction


    def reset(self, pos):
        self.head = cube(pos)
        self.body = []
        self.body.append(self.head)
        self.turns = {}
        self.dirnx = 0
        self.dirny = 1
        s.right = True
        s.left = False
        s.up = False
        s.down = False

    def addCube(self):
        tail = self.body[-1]
        dx, dy = tail.dirnx, tail.dirny
        if dx == 1 and dy == 0:# if moving left right up or down, wherever the tail is at should add one more cube behind it
            self.body.append(cube((tail.pos[0] - 1, tail.pos[1])))
        elif dx == -1 and dy == 0:
            self.body.append(cube((tail.pos[0] + 1, tail.pos[1])))
        elif dx == 0 and dy == 1:
            self.body.append(cube((tail.pos[0], tail.pos[1] - 1)))
        elif dx == 0 and dy == -1:
            self.body.append(cube((tail.pos[0], tail.pos[1] + 1)))

        self.body[-1].dirnx = dx#if we only used the code up top, the cube would just stay there, so this should attach the tail
        self.body[-1].dirny = dy

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i == 0:#if index is 0, aka the cube is the first one
                c.draw(surface, True)#true should draw eyes, telling us where the front of the snake is
            else:
                c.draw(surface)#else, draw a cube




def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0

    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255,255,255), (x, 0), (x,w))#draw a line starting at the left and ending at the right
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))#draw a line starting from the top and ending at the bottom

def redrawWindow(surface):
    global rows, width, s
    last_score = max_score()
    surface.fill((0, 0, 0))
    s.draw(surface)
    snack.draw(surface)
    drawGrid(width, rows, surface)
    STAT_FONT = pygame.font.SysFont('comicsans', 40)
    text = STAT_FONT.render("Score: " + str(len(s.body)), 1, (255, 255, 255))
    surface.blit(text, (width - 10 - text.get_width(), 0))
    high_score_text = STAT_FONT.render("High Score: " + str(last_score), 1, (255, 255, 255))
    surface.blit(high_score_text, (10, 0))

    pygame.display.update()


def randomSnack(rows, item):
    positions = item.body
    while True:#generate random positions until occupied
        x = random.randrange(rows)
        y = random.randrange(rows)
        if len(list(filter(lambda z:z.pos == (x, y), positions))) > 0:# i just found this thing online where if the the apple position is the same as a position where the snake is at, find another random until it does not
            continue#if zed.position is = to (x,y), do it again
        else:
            break
    return (x, y)

def lost(win):
    update_score(str(len(s.body)))
    font = pygame.font.SysFont("comicsans", 60, bold=True)
    label = font.render("YOU LOST! Score: " + str(len(s.body)), False, (255, 255, 255))
    win.blit(label, (width / 2 - (label.get_width() / 2), width / 2 - (label.get_height() / 2)))
    pygame.display.update()
    pygame.time.delay(1500)
    s.reset((1, 10))

def update_score(nscore):
    score = max_score()
    with open('C:/Users/richa/PycharmProjects/Games/pygame_test/snake/highest_score.txt', 'w') as f:
        if int(score) > int(nscore):
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('C:/Users/richa/PycharmProjects/Games/pygame_test/snake/highest_score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def main():
    global rows, width, s, snack
    width = 500
    rows = 20
    win = pygame.display.set_mode((width, width))
    s = Snake((0, 255, 0), (1, 10))
    snack = cube(randomSnack(rows, s), color=(255, 0, 0))
    clock = pygame.time.Clock()

    run = True
    while run:
        pygame.time.delay(75)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not s.right:
            s.dirnx = -1  # x goes down by one when going left
            s.dirny = 0
            s.right = False
            s.left = True
            s.up = False
            s.down = False
            s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]  # self.head.pos is the current position of the head of the snake. The line says that we have a full turn at dirnx and dirny
        elif keys[pygame.K_RIGHT] and not s.left:
            s.dirnx = 1  # x goes down by one when going left
            s.dirny = 0
            s.right = True
            s.left = False
            s.up = False
            s.down = False
            s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]  # adding turns that happen into a turn list
        elif keys[pygame.K_UP] and not s.down:
            s.dirnx = 0  # x goes down by one when going left
            s.dirny = -1
            s.right = False
            s.left = False
            s.up = True
            s.down = False
            s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
        elif keys[pygame.K_DOWN] and not s.up:
            s.dirnx = 0  # x goes down by one when going left
            s.dirny = 1
            s.right = False
            s.left = False
            s.up = False
            s.down = True
            s.turns[s.head.pos[:]] = [s.dirnx, s.dirny]
        # this is so each cube turns in a direction when the input tells it to turn
        for i, c in enumerate(s.body):  # for all squares, turn on that square; i,c is index, cube
            p = c.pos[:]  # [:] makes a copy so it's not actually changing the original; p is the cube's position
            if p in s.turns:  # for every cube in the snake's body, if that cube's position is in the turn list
                turn = s.turns[p]  # gets the direction that we should turn
                c.move(turn[0], turn[1])  # move in that turn for that position
                if i == len(s.body) - 1:  # once that move reaches the end of the snake, then remove that turn
                    s.turns.pop(p)
            else:  # If we are not turning the cube
                # If the cube reaches the edge of the screen we will make it appear on the opposite side
                if c.dirnx == -1 and c.pos[0] <= 0:
                    lost(win)
                elif c.dirnx == 1 and c.pos[0] >= c.rows - 1:
                    lost(win)
                elif c.dirny == 1 and c.pos[1] >= c.rows - 1:
                    lost(win)
                elif c.dirny == -1 and c.pos[1] <= 0:
                    lost(win)
                else:
                    c.move(c.dirnx, c.dirny)  # If we haven't reached the edge just move in our current direction
        if s.body[0].pos == snack.pos:
            s.addCube()
            snack = cube(randomSnack(rows, s), color=(255, 0, 0))

        for x in range(len(s.body)):
            if s.body[x].pos in list(map(lambda z:z.pos, s.body[x + 1:])):#checks if the head has hit the body
                lost(win)
                break
        redrawWindow(win)


main()
