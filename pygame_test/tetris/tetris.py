import pygame
import random

pygame.init()

# creating the data structure for pieces
# setting up global vars
# functions
# - create_grid
# - draw_grid
# - draw_window
# - rotating shape in main
# - setting up the main

"""
10 x 20 square grid
shapes: S, Z, I, O, J, L, T
represented in order by 0 - 6
"""

icon = pygame.image.load('D:/Character Sprites/Tetris/tetris_icon.png')
pygame.display.set_icon(icon)

music = 'D:/Character Sprites/Tetris/tetris.mp3'
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.0)
#plays music (-1 plays it on loop)
pygame.mixer.music.play(-1)


pygame.font.init()

# GLOBALS VARS
s_width = 800
s_height = 700
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


# index 0 - 6 represent shape


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0

def create_grid(locked_positions={}):
    #making grid for tetris
    grid = [[(0, 0, 0) for _ in range(10)] for _ in range(20)]

    #for each row, then for each column for that row(square)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #locked position is a dictionary that corresponds coordinates to colors
            if (j, i) in locked_positions:
                #find that position
                c = locked_positions[(j, i)]
                #change the color to that position
                grid[i][j] = c
    return grid

def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            #for every row in a current line
            if column == '0':
                #if it passes a 0 in the list, puts it in x and y value; getting spot by using x + column, y + row
                positions.append((shape.x + j, shape.y + i))
    for i, pos in enumerate(positions):
        #sice using periods makes the position a bit off, change the look to match the box perfectly
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    #all the available squares if in accepted position and the squares are black
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    #gets rid of useless sublists
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    #what this line of code is saying is that for the positions that are not accepted, if the y value is greater than negative 1, it will return false
    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True

    return False


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    #drawing a grid s0 you can see the blocks
    for i in range(len(grid)):
        #drawing a line every row from the left to the right of the box
        pygame.draw.line(surface, (128,128,128), (sx, sy + i*block_size), (sx+play_width, sy + i*block_size))
        for j in range(len(grid[i])):
            #drawing a line for every column, top to bottom
            pygame.draw.line(surface, (128, 128, 128), (sx + j*block_size, sy), (sx + j*block_size, sy + play_height))


def clear_rows(grid, locked):
    inc = 0
    #loops through the grid backwards
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        #if not black squares are in row, it is filled, so delete row
        if (0, 0, 0) not in row:
            inc += 1
            ind = i
            #delete row by finding the y coordinates for each and deleting the ones in that coordinate
            for j in range(len(row)):
                try:
                    del locked[(j, i)]
                except:
                    continue

    #shifting rows
    if inc > 0:
        #this makes it so the bottom rows movve down first; this is important because of overlappig that might occur
        for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
            x, y = key
            #if above the index of the row removed
            if y < ind:
                #make a new key that increments in down
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)
    return inc


def draw_next_shape(shape, surface):
    #will show you the next shape
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Next Shape:", 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    #drawing the shape in the next shape area of the window
    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    surface.blit(label, (sx + 10, sy - 30))

def update_score(nscore):
    score = max_score()
    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    # putting some text onto the screen
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render("Tetris", 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    #current_score
    font = pygame.font.SysFont("comicsans", 30)
    label = font.render("Score: " + str(score), 1, (255, 255, 255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 30, sy + 160))

    #last score
    high_score_label = font.render("High Score: " + str(last_score), 1, (255, 255, 255))

    sx = top_left_x + play_width - 550
    sy = top_left_y + play_height/2 - 100

    surface.blit(high_score_label, (sx + 30, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            #for every spot on the grid, draw a rectangle; for the x and y positions, just put top left of the grid and the amount of blocks multiplied by the block size will bring you to the right block
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 4)
    draw_grid(surface, grid)

def main(win):
    last_score = max_score()
    locked_positions = {}
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    muted = False
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.35
    level_time = 0
    score = 0

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if fall_speed > .12:
                fall_speed -= 0.005

        #if the timer counts to the number, the piece will fall at that time
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            #if it is not a valid position, move the piece back like nothing ever happened
            #in this scenario, if we did not move left or right and we came to an invalid position, that means we went down
            if not (valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                current_piece.x -= 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x += 1
            if keys[pygame.K_RIGHT]:
                current_piece.x += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.x -= 1
            if keys[pygame.K_DOWN]:
                current_piece.y += 1
                if not(valid_space(current_piece, grid)):
                    current_piece.y -= 1
            if keys[pygame.K_UP]:
                current_piece.rotation += 1
                if not (valid_space(current_piece, grid)):
                    current_piece.rotation -= 1
            if keys[pygame.K_SPACE]:
                #current_piece.y += 20
                while (valid_space(current_piece, grid)):
                        current_piece.y += 1
                current_piece.y -= 1
            if keys[pygame.K_m]:
                if muted == True:
                    pygame.mixer.music.set_volume(0.5)
                    muted = False
                elif muted == False:
                    pygame.mixer.music.set_volume(0.0)
                    muted = True


                    #current_piece.y -= 20
        shape_pos = convert_shape_format(current_piece)

        for i in range(len(shape_pos)):
            x, y = shape_pos[i]
            if y > -1:
                #if not above the screen, draw color for corresponding piece
                grid[y][x] = current_piece.color

        #once the piece is locked, the current piece changes, and the next piece will go
        if change_piece:
            score += 1
            for pos in shape_pos:
                #locked positions is a dictionary with coordinates on one side and a color on the other
                #what this is doing is saying that if the position of a square is in a locked position, keep it there
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10


        draw_window(win, grid, score, last_score)
        draw_next_shape(next_piece, win)
        pygame.display.update()
        if check_lost(locked_positions):
            draw_text_middle(win, "YOU LOST", 80, (255, 255, 255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)

def main_menu(win):
    run = True
    while run:
        draw_text_middle(win, 'Press Any Key To Play', 60, (255, 255, 255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()


win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')
main_menu(win)  # start game