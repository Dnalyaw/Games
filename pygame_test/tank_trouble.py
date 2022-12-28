import pygame
import random

#pygame.init()
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800

tank_img = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/player_tank.png"), (50, 50))
tank_img_2 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/player_tank_left.png"), (50, 50))
tank_img_3 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/player_tank_right.png"), (50, 50))
tank_img_4 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/player_tank_down.png"), (50, 50))
enemy_tank_img = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/enemy_tank.png"), (50, 50))
enemy_tank_img_2 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/enemy_tank_left.png"), (50, 50))
enemy_tank_img_3 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/enemy_tank_right.png"), (50, 50))
enemy_tank_img_4 = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/enemy_tank_down.png"), (50, 50))
BULLET = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/bullet.png"), (12, 12))
bg = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Tank Game/bg_2.png"), (800, 800))

pygame.display.set_caption("Tanks")
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 2
        self.imgs = [tank_img, tank_img_2, tank_img_3, tank_img_4]
        self.img = tank_img_4
        self.mask = pygame.mask.from_surface(self.img)
        self.left = False
        self.right = False
        self.up = False
        self.down = True
        self.hitbox = (self.x, self.y, 50, 50)
        self.visible = True
    #def move(self, vel):
    def draw(self, win):
        if self.visible:
            win.blit(self.img, (self.x, self.y))
            self.hitbox = (self.x, self.y, 50, 50)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 2
        self.imgs = [tank_img, tank_img_2, tank_img_3, tank_img_4]
        self.img = enemy_tank_img
        self.mask = pygame.mask.from_surface(self.img)
        self.left = False
        self.right = False
        self.up = True
        self.down = False
        self.hitbox = (self.x, self.y, 50, 50)
        self.visible = True
    #def move(self, vel):
    def draw(self, win):
        if self.visible:
            win.blit(self.img, (self.x, self.y))
            self.hitbox = (self.x, self.y, 50, 50)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
class Background:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.img = bg
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))
class projectile(object):
    def __init__(self, x, y, x_facing, y_facing):
        self.x = x
        self.y = y
        self.img = BULLET
        self.mask = pygame.mask.from_surface(self.img)
        self.x_facing = x_facing
        self.x_vel = 8 * x_facing
        self.y_facing = y_facing
        self.y_vel = 8 * y_facing
        self.hitbox = (self.x, self.y, 6, 6)
    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    #tldr; if the mask of object 2 collides with the mak of object 1, this will return a true or false depending on the overlap
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #(x, y)

def draw_window(win, player, enemy, bullets, player_bullets, blue_score, red_score, background):
    background.draw(win)
    player.draw(win)
    enemy.draw(win)
    font = pygame.font.SysFont('comicsans', 30)
    text = font.render("Blue Score: " + str(blue_score), 1, (0, 0, 0))
    text_2 = font.render("Red Score: " + str(red_score), 1, (0, 0, 0))
    win.blit(text, (10, 10))
    win.blit(text_2, (10, WIN_HEIGHT - 30))

    for bullet in bullets:
        # after a bullet is added (by clicking space), the bullet is drawn using the draw function in projectile
        #also, since it was appended as a projectile
        bullet.draw(win)
    for bullet in player_bullets:
        bullet.draw(win)
    pygame.display.update()

def main():
    player_shootLoop = 0
    enemy_shootLoop = 0
    background = Background(0, 0)
    player = Player(WIN_WIDTH//2, 15)
    enemy = Enemy(WIN_WIDTH//2, 735)
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    bullets = []
    player_bullets = []
    blue_score = 0
    red_score = 0

    run = True
    while run:
        clock.tick(60)

        if player_shootLoop > 0:
            player_shootLoop += 1
        if player_shootLoop > 24:
            player_shootLoop = 0
        if enemy_shootLoop > 0:
            enemy_shootLoop += 1
        if enemy_shootLoop > 24:
            enemy_shootLoop = 0

        # if the bullet is on the screen, it will move a velocity
        for bullet in bullets:
            if bullet.x < WIN_WIDTH and bullet.x > 0:
                bullet.x += bullet.x_vel
            else:
                # deletes the bullet in bullets list
                bullets.pop(bullets.index(bullet))
            if bullet.y < WIN_HEIGHT and bullet.y > 0:
                bullet.y += bullet.y_vel
            else:
                # deletes the bullet in bullets list
                bullets.pop(bullets.index(bullet))
            if collide(bullet, background):
                bullets.pop(bullets.index(bullet))
            # if the top of the bullet is above the bottom of the goblin's hitbox and the bottom of the bullet is below the top:
            if collide(bullet, player):
                red_score += 1
                bullets.pop(bullets.index(bullet))
                player.visible = False
                player = Player(random.randrange(1, WIN_WIDTH - 50), random.randrange(1, WIN_HEIGHT - 50))


        for bullet in player_bullets:
            if bullet.x < WIN_WIDTH and bullet.x > 0:
                bullet.x += bullet.x_vel
            else:
                # deletes the bullet in bullets list
                player_bullets.pop(player_bullets.index(bullet))
            if bullet.y < WIN_HEIGHT and bullet.y > 0:
                bullet.y += bullet.y_vel
            else:
                # deletes the bullet in bullets list
                player_bullets.pop(player_bullets.index(bullet))
            if collide(bullet, background):
                player_bullets.pop(player_bullets.index(bullet))
            if collide(bullet, enemy):
                    blue_score += 1
                    player_bullets.pop(player_bullets.index(bullet))
                    enemy.visible = False
                    enemy = Enemy(random.randrange(1, WIN_WIDTH - 50), random.randrange(1, WIN_HEIGHT - 50))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - player.vel > 0:
            player.x -= player.vel
            player.img = tank_img_2
            player.left = True
            player.right = False
            player.up = False
            player.down = False
        if keys[pygame.K_RIGHT] and player.x + player.vel + 50 < WIN_WIDTH:
            player.x += player.vel
            player.img = tank_img_3
            player.left = False
            player.right = True
            player.up = False
            player.down = False
        if keys[pygame.K_UP] and player.y - player.vel > 0:
            player.y -= player.vel
            player.img = tank_img
            player.left = False
            player.right = False
            player.up = True
            player.down = False
        if keys[pygame.K_DOWN] and player.y + player.vel + 50 < WIN_HEIGHT:
            player.y += player.vel
            player.img = tank_img_4
            player.left = False
            player.right = False
            player.up = False
            player.down = True
        if keys[pygame.K_PERIOD] and player_shootLoop == 0:
            # the x direction will change based off of if the the person is facing left or right
            if player.right:
                player.x_facing = 1
                player.y_facing = 0
            elif player.left:
                player.x_facing = -1
                player.y_facing = 0
            elif player.up:
                player.x_facing = 0
                player.y_facing = -1
            elif player.down:
                player.x_facing = 0
                player.y_facing = 1
            if len(player_bullets) < 5:
                # adds a projectile to the list everytime space is pressed
                # the parameters make sure that the bullet is shooting from the middle of the man
                player_bullets.append(projectile(round(player.x + 50 // 2), round(player.y + 50 // 2), player.x_facing, player.y_facing))
            player_shootLoop = 1
        if keys[pygame.K_a] and enemy.x - enemy.vel > 0:
            enemy.x -= enemy.vel
            enemy.img = enemy_tank_img_2
            enemy.left = True
            enemy.right = False
            enemy.up = False
            enemy.down = False
        if keys[pygame.K_d] and enemy.x + enemy.vel + 50 < WIN_WIDTH:
            enemy.x += player.vel
            enemy.img = enemy_tank_img_3
            enemy.left = False
            enemy.right = True
            enemy.up = False
            enemy.down = False
        if keys[pygame.K_w] and enemy.y - enemy.vel > 0:
            enemy.y -= player.vel
            enemy.img = enemy_tank_img
            enemy.left = False
            enemy.right = False
            enemy.up = True
            enemy.down = False
        if keys[pygame.K_s] and enemy.y + enemy.vel + 50 < WIN_HEIGHT:
            enemy.y += enemy.vel
            enemy.img = enemy_tank_img_4
            enemy.left = False
            enemy.right = False
            enemy.up = False
            enemy.down = True
        if keys[pygame.K_SPACE] and enemy_shootLoop == 0:
            # the x direction will change based off of if the the person is facing left or right
            if enemy.right:
                enemy.x_facing = 1
                enemy.y_facing = 0
            elif enemy.left:
                enemy.x_facing = -1
                enemy.y_facing = 0
            elif enemy.up:
                enemy.x_facing = 0
                enemy.y_facing = -1
            elif enemy.down:
                enemy.x_facing = 0
                enemy.y_facing = 1
            if len(bullets) < 5:
                # adds a projectile to the list everytime space is pressed
                # the parameters make sure that the bullet is shooting from the middle of the man
                bullets.append(projectile(round(enemy.x + 50 // 2), round(enemy.y + 50 // 2), enemy.x_facing, enemy.y_facing))
            enemy_shootLoop = 1

        if collide(player, enemy):
            player.visible = False
            enemy.visible = False
            player = Player(random.randrange(1, WIN_WIDTH - 50), random.randrange(1, WIN_HEIGHT - 50))
            enemy = Enemy(random.randrange(1, WIN_WIDTH - 50), random.randrange(1, WIN_HEIGHT - 50))
        if keys[pygame.K_DOWN] and collide(background, player):
            player.vel = 0
        elif keys[pygame.K_UP] and collide(background, player):
            player.vel = 0
        elif keys[pygame.K_LEFT] and collide(background, player):
            player.vel = 0
        elif keys[pygame.K_RIGHT] and collide(background, player):
            player.vel = 0
        else:
            player.vel = 2


        if keys[pygame.K_w] and collide(background, enemy):
            enemy.vel = 0
        elif keys[pygame.K_s] and collide(background, enemy):
            enemy.vel = 0
        elif keys[pygame.K_a] and collide(background, enemy):
            enemy.vel = 0
        elif keys[pygame.K_d] and collide(background, enemy):
            enemy.vel = 0
        else:
            enemy.vel = 2

        draw_window(win, player, enemy, bullets, player_bullets, blue_score, red_score, background)

        win.fill((255, 255, 255))

    pygame.quit()
    quit()

main()