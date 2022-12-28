import random

import pygame

pygame.font.init()

WIN_WIDTH = 1100
WIN_HEIGHT = 600
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
dino_run_1 = pygame.image.load("D:/Character Sprites/Dino Game/Dino/DinoRun1.png")
dino_run_2 = pygame.image.load("D:/Character Sprites/Dino Game/Dino/DinoRun2.png")
dino_duck_1 = pygame.image.load("D:/Character Sprites/Dino Game/Dino/DinoDuck1.png")
dino_duck_2 = pygame.image.load("D:/Character Sprites/Dino Game/Dino/DinoDuck2.png")
small_cactus_1 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/SmallCactus1.png")
small_cactus_2 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/SmallCactus2.png")
small_cactus_3 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/SmallCactus3.png")
large_cactus_1 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/LargeCactus1.png")
large_cactus_2 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/LargeCactus2.png")
large_cactus_3 = pygame.image.load("D:/Character Sprites/Dino Game/Cactus/LargeCactus3.png")
bird_1 = pygame.image.load("D:/Character Sprites/Dino Game/Bird/Bird1.png")
bird_2 = pygame.image.load("D:/Character Sprites/Dino Game/Bird/Bird2.png")

dino_dead = pygame.image.load(("D:/Character Sprites/Dino Game/Dino/DinoDead.png"))

dino_jumping = pygame.image.load("D:/Character Sprites/Dino Game/Dino/DinoJump.png")
dino_running = [dino_run_1, dino_run_2]
dino_ducking = [dino_duck_1, dino_duck_2]
small_cactus_imgs = [small_cactus_1, small_cactus_2, small_cactus_3]
large_cactus_imgs = [large_cactus_1, large_cactus_2, large_cactus_3]
bird_imgs = [bird_1, bird_2]
cloud_img = pygame.image.load("D:/Character Sprites/Dino Game/Other/Cloud.png")
track_img = pygame.image.load("D:/Character Sprites/Dino Game/Other/Track.png")
game_over_img = pygame.image.load("D:/Character Sprites/Dino Game/Other/GameOver.png")

obstacles = [small_cactus_imgs, large_cactus_imgs, bird_imgs]

pygame.display.set_caption("Dino Game")

class Dinosaur:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.duck_img = dino_ducking
        self.run_img = dino_running
        self.jump_img = dino_jumping
        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False

        self.run_count = 0
        self.img = self.run_img[0]
        self.mask = pygame.mask.from_surface(self.img)

        self.duck_pos = 340
        self.jump_vel = 9#8.5
        self.visible = True
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


    def update(self, obstacle):
        if self.visible:
            if self.dino_run:
                self.img = self.run_img[self.run_count // 5]
                self.run_count += 1
                if self.run_count >= 10:
                    self.run_count = 0
            if self.dino_jump:
                self.img = self.jump_img
                self.y -= self.jump_vel * 4
                self.jump_vel -= 1#0.8
                if self.jump_vel < -9: #-8.5:
                    self.dino_jump = False
                    self.jump_vel = 9#8.5
            if self.dino_duck:
                self.y = self.duck_pos
                self.img = self.duck_img[self.run_count // 5]
                self.run_count += 1
                if self.run_count >= 10:
                    self.run_count = 0
            elif not self.dino_duck and not self.dino_jump:
                self.y = 310
        else:
            self.img = dino_dead

class Track:
    WIDTH = track_img.get_width()
    IMG = track_img

    def __init__(self, y, vel):
        self.VEL = vel
        self.y = y
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

class Cloud:
    WIDTH = track_img.get_width()

    def __init__(self, vel):
        self.VEL = vel
        self.x = random.randint(800, 1000)
        self.y = random.randint(50, 100)
        self.image = cloud_img
    def draw(self, win):
        win.blit(self.image, (self.x, self.y))
        self.x -= self.VEL
        if self.x < -self.image.get_width():
            self.x = random.randint(2500, 3000)
            self.y = random.randint(50, 100)

class Obstacles:
    def __init__(self, vel):
        self.VEL = vel
        self.x = 700
        self.y = 0
        self.images = random.choice(obstacles)
        self.image = random.choice(self.images)
        self.flyCount = 0
        self.mask = pygame.mask.from_surface(self.image)

    def draw(self, win):
        self.x -= self.VEL
        if self.images == small_cactus_imgs:
            self.y = 330
            win.blit(self.image, (self.x, self.y))
        elif self.images == large_cactus_imgs:
            if self.image == large_cactus_3:
                self.y = 300
                win.blit(self.image, (self.x, self.y))
            else:
                self.y = 310
                win.blit(self.image, (self.x, self.y))
        elif self.images == bird_imgs:
            self.y = 240
            win.blit(self.images[self.flyCount // 5], (self.x, self.y))
            self.flyCount += 1
            if self.flyCount >= 10:
                self.flyCount = 0

        if self.x < -self.image.get_width():
            self.images = random.choice(obstacles)
            self.image = random.choice(self.images)
            self.x = random.randint(1000, 1500)


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    #tldr; if the mask of object 2 collides with the mak of object 1, this will return a true or false depending on the overlap
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #(x, y)

def lost(win, player):
#    font = pygame.font.SysFont("comicsans", 60, bold=True)
 #   label = font.render("YOU LOST! Score: " + str(score), False, (0, 0, 0))
  #  win.blit(label, WIN_WIDTH / 2 - (label.get_width() / 2), WIN_HEIGHT / 2 - (label.get_height() / 2))
    player.img = dino_dead
    win.blit(player.img, (player.x, player.y))
    win.blit(game_over_img, (WIN_WIDTH / 2 - (game_over_img.get_width() / 2), WIN_HEIGHT / 2 - (game_over_img.get_height() / 2)))
    pygame.display.update()
    player.visible = False

def redrawWindow(surface, player, track, cloud, score, obstacle):
    player.update(obstacle)
    surface.fill((255, 255, 255))

    font = pygame.font.SysFont('freesansbold.ttf', 30)
    text = font.render("Score: " + str(score), False, (0, 0, 0))
    surface.blit(text, (WIN_WIDTH - 20 - text.get_width(), 20))

    player.draw(surface)
    track.draw(surface)
    cloud.draw(surface)
    obstacle.draw(surface)
    pygame.display.update()

def main():
    VEL = 20
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    player = Dinosaur(80, 310)
    cloud = Cloud(VEL)
    track = Track(380, VEL)
    obstacle = Obstacles(VEL)
    score = 0
    player.visible = True

    run = True
    while run:
        clock.tick(30)
        score += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and not player.dino_jump:
            player.dino_duck = False
            player.dino_run = False
            player.dino_jump = True
        elif keys[pygame.K_DOWN] and not player.dino_duck:
            player.dino_duck = True
            player.dino_run = False
            player.dino_jump = False
        elif not keys[pygame.K_DOWN] and not keys[pygame.K_UP]:
            player.dino_duck = False
            player.dino_run = True


        if score % 100 == 0:
            VEL += 1
        if collide(player, obstacle):
            lost(win, player)
            pygame.time.delay(2000)
            run = False
            main()
        track.move()
        redrawWindow(win, player, track, cloud, score, obstacle)

main()