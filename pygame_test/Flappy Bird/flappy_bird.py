import pygame
import neat
import time
import os
import random

pygame.init()
pygame.font.init()

WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/bird1.png")), pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/bird2.png")), pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/bird3.png"))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/pipe.png"))
BASE_IMG = pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/base.png"))
BG_IMG = pygame.transform.scale2x(pygame.image.load("D:/Character Sprites/flappy_bird/imgs/bg.png"))

STAT_FONT = pygame.font.SysFont('comicsans', 50)

icon = pygame.image.load("D:/Character Sprites/flappy_bird/imgs/bird1.png")
pygame.display.set_icon(icon)
pygame.display.set_caption('Flappy Bird')

jump = pygame.mixer.Sound('D:/Character Sprites/flappy_bird/jump_2.mp3')
point = pygame.mixer.Sound('D:/Character Sprites/flappy_bird/point.mp3')
lost = pygame.mixer.Sound('D:/Character Sprites/flappy_bird/lost.mp3')
#pygame.mixer.Sound.set_volume(bulletSound, 0.1)
#pygame.mixer.Sound.set_volume(hitSound, 0.1)

class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        #what this line does is because the tick count resets every jump, every frame the jump becomes less and less until the bird starts going down
        #ex: -10.5 + 1.5 = -9, then tick count goes up, -7, -3, -1,  1, 4, and so on
        d = self.vel*self.tick_count + 1.5*self.tick_count**2

        #makes d not surpass 16 pixels
        if d >= 16:
            d = 16
        #fine tuning to make the jump nicer
        if d < 0:
            d -= 2

        #changing y
        self.y += d

        #tilting bird upwards
        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            #makes it so it nose dives but doesn't flip all the way around
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        self.img_count += 1

        #goes through a pattern that makes the bird flap its wings
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        #makes the bird level when taking a nose dive
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2

        #rotates the image around the center
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft=(self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)

class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x):
        self.x = x
        self.height = 0

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        #the top height is the top left hand corner - the height to get the bottom of the top pipe
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        #the pipe moves to the left a little bit because the bird doesn't move
        self.x -= self.VEL

    def draw(self, win):
        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
    def collide(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface((self.PIPE_TOP))
        bottom_mask = pygame.mask.from_surface((self.PIPE_BOTTOM))

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        #if collide, will return none, else returns something
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True

        return False

class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y =y
        self.x1 = 0
        self.x2 = self.WIDTH
    def move(self):
        #what this will do is it will have two of the same image, one starting from the left side and another off the screen to the right
        # this code makes it so these photos move to the left side, and if the imgae goes off the screen, move it to the right side
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

def update_score(nscore):
    score = max_score()
    with open('high_score.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))

def max_score():
    with open('high_score.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()
    return score

def draw_window(win, bird, pipes, base, score, last_score = 0):
    win.blit(BG_IMG, (0, 0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: "+ str(score), 1, (255, 255, 255))
    high_score_text = STAT_FONT.render("High Score: " + str(last_score), 1, (255, 255, 255))
    win.blit(high_score_text, (10, 10))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    base.draw(win)


    bird.draw(win)
    pygame.display.update()

def main():
    last_score = max_score()
    bird = Bird(230, 350)
    base = Base(730)
    pipes = [Pipe(700)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                if bird.y >= 0:
                    jump.play()
                    bird.jump()

        bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            #since pipes is a list, we can append another pipe everytime the bird passes the pipe and doesn't get killed
            if pipe.collide(bird) or bird.y >= 685:
                lost.play()
                font = pygame.font.SysFont("comicsans", 60, bold=True)
                label = font.render("YOU LOST! Score: " + str(score), False, (255, 255, 255))
                win.blit(label, (WIN_WIDTH/2 - (label.get_width()/2), WIN_HEIGHT/2 - (label.get_height()/2)))
                pygame.display.update()
                pygame.time.delay(1500)
                update_score(score)
                main()
                #run = False

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
            if not pipe.passed and pipe.x < bird.x:
                point.play()
                #if the pie was passed and it was not declared as passed, declare as passed
                pipe.passed = True
                add_pipe = True
            pipe.move()
        if add_pipe:
            score += 1
            pipes.append(Pipe(600))

        for r in rem:
            #removing pipe when offscreen
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= 730:
            pass

        base.move()
        draw_window(win, bird, pipes, base, score, last_score)


    pygame.quit()
    quit()

main()