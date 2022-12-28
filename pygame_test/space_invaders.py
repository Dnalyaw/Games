import pygame
import random
pygame.font.init()


#make window screen
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
icon = pygame.image.load('D:/Character Sprites/Space Invaders/standing.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Space Invaders")

#Load all images
RED_SPACE_SHIP = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_ship_red_small.png')
GREEN_SPACE_SHIP = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_ship_green_small.png')
BLUE_SPACE_SHIP = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_ship_blue_small.png')

#player's ship
YELLOW_SPACE_SHIP = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_ship_yellow.png')

#Lasers
RED_LASER = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_laser_red.png')
GREEN_LASER = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_laser_green.png')
BLUE_LASER = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_laser_blue.png')
YELLOW_LASER = pygame.image.load('D:/Character Sprites/Space Invaders/pixel_laser_yellow.png')

#Powerups
HEART = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Space Invaders/pixel-heart.png"), (75, 75))
RAPID_FIRE = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Space Invaders/rapid_fire.png"), (75, 75))
LASER_GUN = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Space Invaders/laser_gun.png"), (75, 55))
SPEED_ICON = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Space Invaders/speed_icon.png"), (60, 60))
ONE_UP = pygame.transform.scale(pygame.image.load("D:/Character Sprites/Space Invaders/one_up.png"), (65, 65))

#Background; scaled by doing pygame.transform.scale, then put the dimensions of the scale
BG = pygame.transform.scale(pygame.image.load('D:/Character Sprites/Space Invaders/background-black.png'), (WIDTH, HEIGHT))

class Powerup:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
        self.visible = True
        #picks numbers 1-5 randomly
        self.pick = random.randrange(1, 6, 1)
        self.pick_2 = random.randrange(6, 11, 1)
        self.pick_3 = random.randrange(11, 16, 1)
        self.pick_4 = random.randrange(16, 21, 1)
    def draw(self, window):
        if self.visible == True:
            window.blit(self.img, (self.x, self.y))
    def collision(self, obj):
        return collide(self, obj)

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel
    def off_screen(self, height):
        return not (self.y <= height and self.y >= 0)
    def collision(self, obj):
        return collide(self, obj)

class Ship:
    COOLDOWN = 30

    #health is an optional class that is defaulted at 100, but can be changed
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        #if the cooldown ahs reached the counter, it can shoot again
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1
    def shoot(self):
        #when no cooldown, create laser, add to laser list, and set the cooldown counter
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()

#because of inheritance, any variables initialized in the init will also be initialized using Player
class Player(Ship):
    def __init__(self, x, y, health=100):
        #inheriting the (super)/variables in the ship
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    def draw(self, window):
        super().draw(window)
        self.healthbar(window)

    def healthbar(self, window):
        #rectangle for healthbar
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0, 255, 0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))

class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
    }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        #ship img and laser based off of color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        #makes a mask of the surface of the img
        self.mask = pygame.mask.from_surface(self.ship_img)
    def move(self, vel):
        self.y += vel
    def shoot(self):
        #when no cooldown, create laser, add to laser list, and set the cooldown counter
        if self.cool_down_counter == 0:
            laser = Laser(self.x - 20, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    #tldr; if the mask of object 2 collides with the mak of object 1, this will return a true or false depending on the overlap
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None #(x, y)


player = Player(300, 630)

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5

    enemies = []
    wave_length = 5
    enemy_vel = 1
    laser_vel = 4

    player_vel = 5

    lost = False
    lost_count = 0

    heart = Powerup(random.randrange(50, WIDTH - 100, 1), random.randrange(10, WIDTH - 100, 1), HEART)
    rapid_fire = Powerup(random.randrange(50, WIDTH - 100, 1), random.randrange(10, WIDTH - 100, 1), RAPID_FIRE)
    laser_gun = Powerup(random.randrange(50, WIDTH - 100, 1), random.randrange(10, WIDTH - 100, 1), LASER_GUN)
    speed_icon = Powerup(random.randrange(50, WIDTH - 100, 1), random.randrange(10, WIDTH - 100, 1), SPEED_ICON)
    one_up = Powerup(random.randrange(50, WIDTH - 100, 1), random.randrange(10, WIDTH - 100, 1), ONE_UP)

    clock = pygame.time.Clock()
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    #redraw_window is important because if there is anything wrong with a drawing, it's probably gonna be in redraw window
    def redraw_window():
        WIN.blit(BG, (0, 0))

        #draw text
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 255, 255))
        level_label = main_font.render(f"Level: {level}", 1, (255, 255, 255))
        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        #refreshing powerups
        if level == heart.pick + 1 or level == heart.pick_2 + 1 or level == heart.pick_3 + 1 or level == heart.pick_4 + 1:
            heart.visible = True
        if level == rapid_fire.pick + 1 or level == rapid_fire.pick_2 + 1 or level == rapid_fire.pick_3 + 1 or level == rapid_fire.pick_4 + 1:
            rapid_fire.visible = True
        if level == laser_gun.pick + 1 or level == laser_gun.pick_2 + 1 or level == laser_gun.pick_3 + 1 or level == laser_gun.pick_4 + 1:
            laser_gun.visible = True
        if level == speed_icon.pick + 1 or level == speed_icon.pick_2 + 1 or level == speed_icon.pick_3 + 1 or level == speed_icon.pick_4 + 1:
            speed_icon.visible = True
        if level == one_up.pick + 1 or level == one_up.pick_2 + 1 or level == one_up.pick_3 + 1 or level == one_up.pick_4 + 1:
            one_up.visible = True

        #draw powerups if on screen
        if level == heart.pick or level == heart.pick_2 or level == heart.pick_3 or level == heart.pick_4:
            heart.draw(WIN)
        if level == rapid_fire.pick or level == rapid_fire.pick_2 or level == rapid_fire.pick_3 or level == rapid_fire.pick_4:
            rapid_fire.draw(WIN)
        if level == laser_gun.pick or level == laser_gun.pick_2 or level == laser_gun.pick_3 or level == laser_gun.pick_4:
            laser_gun.draw(WIN)
        if level == speed_icon.pick or level == speed_icon.pick_2 or level == speed_icon.pick_3 or level == speed_icon.pick_4:
            speed_icon.draw(WIN)
        if level == one_up.pick or level == one_up.pick_2 or one_up == speed_icon.pick_3 or one_up == speed_icon.pick_4:
            one_up.draw(WIN)


        if lost:
            lost_label = lost_font.render("You Lost!!", 1, (255,255,255))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))



        pygame.display.flip()


    while run:
        clock.tick(FPS)
        redraw_window()

        if lives <= 0 or player.health <= 0:
            lost = True
            lost_count += 1
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        if len(enemies) == 0:
            level += 1
            wave_length += 5
            for i in range(wave_length):
                #depending on the amount of i in wavelength, it will spawn enemies in a random spot on the top of the screen
                enemy = Enemy(random.randrange(50, WIDTH - 100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player.x - player_vel > 0: #left
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel + player.get_width() < WIDTH:  # right
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0: #up
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel + player.get_height() + 15 < HEIGHT: #down
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()

        if level == heart.pick or level == heart.pick_2 or level == heart.pick_3 or level == heart.pick_4:
            if collide(player, heart) and heart.visible == True:
                heart.visible = False
                if player.health <= 75:
                    player.health += 25
                else:
                    player.health = 100

        if level == rapid_fire.pick or level == rapid_fire.pick_2 or level == rapid_fire.pick_3 or level == rapid_fire.pick_4:
            if collide(player, rapid_fire) and rapid_fire.visible == True:
                rapid_fire.visible = False
                if Ship.COOLDOWN >= 10:
                    Ship.COOLDOWN -= 5
                else:
                    Ship.COOLDOWN = 10

        if level == laser_gun.pick or level == laser_gun.pick_2 or level == laser_gun.pick_3 or level == laser_gun.pick_4:
            if collide(player, laser_gun) and laser_gun.visible == True:
                laser_gun.visible = False
                Ship.COOLDOWN = 0
        if Ship.COOLDOWN != 0:
            laser_gun_cooldown = Ship.COOLDOWN
        if level == laser_gun.pick + 1 or level == laser_gun.pick_2 + 1 or level == laser_gun.pick_3 + 1 or level == laser_gun.pick_4 + 1:
            if Ship.COOLDOWN == 0:
                Ship.COOLDOWN = laser_gun_cooldown

        if level == speed_icon.pick or level == speed_icon.pick_2 or level == speed_icon.pick_3 or level == speed_icon.pick_4:
            if collide(player, speed_icon) and speed_icon.visible == True:
                speed_icon.visible = False
                player_vel += 1

        if level == one_up.pick or level == one_up.pick_2 or level == one_up.pick_3 or level == one_up.pick_4:
            if collide(player, one_up) and one_up.visible == True:
                one_up.visible = False
                lives += 1



        for enemy in enemies[:]:
            #every iteration move the enemy's lasers and move the enemy
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)

            #shoot randomly
            if random.randrange(0, 5 * 60) == 1:
                enemy.shoot()
            #if the player and the enemy hit each other, the enemy dies but you lose health
            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)
            #if the enemy reaches the end, you lose a life
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)

        player.move_lasers(-laser_vel, enemies)

def main_menu():
    title_font = pygame.font.SysFont("comicsans", 100)
    rules_font = pygame.font.SysFont("comicsans", 40)
    run = True
    while run:
        WIN.blit(BG, (0, 0))
        title_label = title_font.render("Left-Click to begin...", 1, (255, 255, 255))
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 200))
        rules_label = rules_font.render("Movement - WASD, Shoot - Space", 1, (255, 255, 255))
        WIN.blit(rules_label, (WIDTH / 2 - rules_label.get_width() / 2, 350))
        rules_label_2 = rules_font.render("Pause - X on top right, Exit - X on top right x2 ", 1, (255, 255, 255))
        WIN.blit(rules_label_2, (WIDTH / 2 - rules_label_2.get_width() / 2, 400))

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                main()
    pygame.quit()



main_menu()