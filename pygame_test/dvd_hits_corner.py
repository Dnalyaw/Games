import random

import pygame

WIDTH, HEIGHT = 1500, 1250

pygame.display.set_caption("Will it hit the corner?")
win = pygame.display.set_mode((WIDTH, HEIGHT))
red = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_red.png'), (250, 250))
orange = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_orange.png'), (250, 250))
yellow = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_yellow.png'), (250, 250))
green = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_green.png'), (250, 250))
blue = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_blue.png'), (250, 250))
purple = pygame.transform.scale(pygame.image.load('D:/Character Sprites/dvd_logos/dvd_logo_purple.png'), (250, 250))

logos = [red, orange, yellow, green, blue, purple]
logo = logos[0]
icon = pygame.image.load("D:/Character Sprites/dvd_logos/dvd_logo_red.png")
pygame.display.set_icon(icon)

class dvd():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = 20
        self.y_vel = 20
        self.pick = 0
        self.logo = logo

    def draw(self, win, color):
        win.blit(color, (self.x, self.y))
    def move(self):
        DVD.draw(win, self.logo)
        self.x += self.x_vel
        self.y += self.y_vel
        if self.y + 50 <= 0 or self.y + 193 >= HEIGHT:
            self.y_vel *= -1
            self.pick += 1
            if self.pick > 5:
                self.pick = 0
            self.logo = logos[self.pick]
        if self.x <= 0 + 10 or self.x + 260 >= WIDTH:
            self.x_vel *= -1
            self.pick += 1
            if self.pick > 5:
                self.pick = 0
            self.logo = logos[self.pick]



DVD = dvd(250, 300)


def main():
    #pygame's window will close immediately after the code has been processed, so you have to make a while loop run forever in order to keep it running
    run = True
    while run:
        clock = pygame.time.Clock()
        clock.tick(60)


        #time delay
        pygame.time.delay(100)

        # event is every move the user inputs into pygame, like a button click or a cursor move
        # pygame.event.get() will get thee events that happened
        for event in pygame.event.get():
            #this just makes it so if you hit the x on the top right, the program finishes
            if event.type == pygame.QUIT:
                run = False



        #fill fills the background with a color; this is good for deleting if you can see multiple of something
        win.fill((0, 0, 0))

        DVD.move()

        #after making something, you have to display it using pygame.display.update()
        pygame.display.update()

main()