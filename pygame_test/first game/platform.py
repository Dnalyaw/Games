import pygame

#always do pygame.init() before anything if you want to make something using pygame
pygame.init()

#making the width and height of the window (has to be in a tuple) : pygame.display.set_mode((500, 500))
win = pygame.display.set_mode((500, 480))

# This sets up all he images in use; see how all of the images use image.load and are in a list
walkRight = [pygame.image.load('D:/Character Sprites/First Game/R1.png'), pygame.image.load('D:/Character Sprites/First Game/R2.png'), pygame.image.load('D:/Character Sprites/First Game/R3.png'), pygame.image.load('D:/Character Sprites/First Game/R4.png'), pygame.image.load('D:/Character Sprites/First Game/R5.png'), pygame.image.load('D:/Character Sprites/First Game/R6.png'), pygame.image.load('D:/Character Sprites/First Game/R7.png'), pygame.image.load('D:/Character Sprites/First Game/R8.png'), pygame.image.load('D:/Character Sprites/First Game/R9.png')]
walkLeft = [pygame.image.load('D:/Character Sprites/First Game/L1.png'), pygame.image.load('D:/Character Sprites/First Game/L2.png'), pygame.image.load('D:/Character Sprites/First Game/L3.png'), pygame.image.load('D:/Character Sprites/First Game/L4.png'), pygame.image.load('D:/Character Sprites/First Game/L5.png'), pygame.image.load('D:/Character Sprites/First Game/L6.png'), pygame.image.load('D:/Character Sprites/First Game/L7.png'), pygame.image.load('D:/Character Sprites/First Game/L8.png'), pygame.image.load('D:/Character Sprites/First Game/L9.png')]
bg = pygame.image.load('D:/Character Sprites/First Game/bg.jpg')
char = pygame.image.load('D:/Character Sprites/First Game/standing.png')

pygame.display.set_caption("Character")

#making an inner clock for fps of game
clock = pygame.time.Clock()

#play sounds/music
bulletSound = pygame.mixer.Sound('D:/Character Sprites/First Game/Game_bullet.mp3')
hitSound = pygame.mixer.Sound('D:/Character Sprites/First Game/Game_hit.mp3')
pygame.mixer.Sound.set_volume(bulletSound, 0.1)
pygame.mixer.Sound.set_volume(hitSound, 0.1)


music = 'D:/Character Sprites/First Game/sweden_audio.mp3'
pygame.mixer.music.load(music)
pygame.mixer.music.set_volume(0.05)
#plays music (-1 plays it on loop)
pygame.mixer.music.play(-1)


class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.isJump = False
        self.jumpCount = 10
        self.left = False
        self.right = False
        self.walkCount = 0
        self.standing = True
        self.hitbox = (self.x + 17, self.y + 11, 28, 52)
    def draw(self, win):
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not(self.standing):
            if self.left:
                # if walk count is at 4, the sprite will choose 1, until walkcount goes over all of the images so then it restarts again
                win.blit(walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            elif self.right:
                win.blit(walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
        else:
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))
            else:
                win.blit(walkLeft[0], (self.x, self.y))
        #this hitbox is a rectangle that will move with the player
        self.hitbox = (self.x + 17, self.y + 11, 28, 52)
        #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)

    def hit (self):
        #the reason we set the jump variables here because when hit and jumping, the character is still jumping when it respawns,
        self.isJump = False
        self.jumpCount = 10
        self.x = 50
        self.y = 405
        self.walkCount = 0
        #placing minus score if player is hit
        font1 = pygame.font.SysFont('arial', 100)
        text = font1.render('-5', 1, (255, 0, 0))
        #you want to pt it in the middle of screen, so middle minus half of the text should be center aligned
        win.blit(text, (250 - (text.get_width()/2), 240 - (text.get_height()/2)))
        pygame.display.update()
        i = 0
        #delays 10 miliseconds 300 times, so 3 seconds
        while i < 150:
            pygame.time.delay(10)
            i += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    i = 301
                    pygame.quit()



class projectile(object):
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 8 * facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    walkRight = [pygame.image.load('D:/Character Sprites/First Game/R1E.png'), pygame.image.load('D:/Character Sprites/First Game/R2E.png'), pygame.image.load('D:/Character Sprites/First Game/R3E.png'), pygame.image.load('D:/Character Sprites/First Game/R4E.png'), pygame.image.load('D:/Character Sprites/First Game/R5E.png'), pygame.image.load('D:/Character Sprites/First Game/R6E.png'), pygame.image.load('D:/Character Sprites/First Game/R7E.png'), pygame.image.load('D:/Character Sprites/First Game/R8E.png'), pygame.image.load('D:/Character Sprites/First Game/R9E.png'), pygame.image.load('D:/Character Sprites/First Game/R10E.png'), pygame.image.load('D:/Character Sprites/First Game/R11E.png')]
    walkLeft = [pygame.image.load('D:/Character Sprites/First Game/L1E.png'), pygame.image.load('D:/Character Sprites/First Game/L2E.png'), pygame.image.load('D:/Character Sprites/First Game/L3E.png'), pygame.image.load('D:/Character Sprites/First Game/L4E.png'), pygame.image.load('D:/Character Sprites/First Game/L5E.png'), pygame.image.load('D:/Character Sprites/First Game/L6E.png'), pygame.image.load('D:/Character Sprites/First Game/L7E.png'), pygame.image.load('D:/Character Sprites/First Game/L8E.png'), pygame.image.load('D:/Character Sprites/First Game/L9E.png'), pygame.image.load('D:/Character Sprites/First Game/L10E.png'), pygame.image.load('D:/Character Sprites/First Game/L11E.png')]

    def __init__(self, x, y, width, height, end):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.end = end
        #keeps path of alien
        self.path = [self.x, self.end]
        self.walkCount = 0
        self.vel = 3
        self.hitbox = (self.x + 17, self.y + 2, 31, 57)
        self.health = 10
        self.visible = True
    def draw(self, win):
        if self.visible:
            #the enemy will be moved first, then it will be drawn
            self.move()
            #once the list of images is done, restart
            if self.walkCount + 1 >= 33:
                self.walkCount = 0

            if self.vel > 0:
                #the reason that it's divided by 3 is because it looks normal
                win.blit(self.walkRight[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1
            else:
                win.blit(self.walkLeft[self.walkCount // 3], (self.x, self.y))
                self.walkCount += 1

            #behind the green box, there will be a red box
            pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0], self.hitbox[1] - 20, 50, 10))
            # the next line just makes it so that the width of the rectangle will shrink by 10 percent every time hit() happens
            pygame.draw.rect(win, (0, 130, 0), (self.hitbox[0], self.hitbox[1] - 20, 50 - ((50/10) * (10 - self.health)), 10))

            self.hitbox = (self.x + 17, self.y + 2, 31, 57)
            #pygame.draw.rect(win, (255, 0, 0), self.hitbox, 2)
    def hit(self):
        #if character is hit, health loses by one
        if self.health > 1:
            self.health -= 1
        else:
            self.visible = False

    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                #saying that if the starting point plus the velocity moving right is less than the end point, keep running right
                self.x += self.vel
            else:
                #otherwise, move in opposite direction
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            #if the starting point  moving left hits the end of the path
            if self.x - self.vel > self.path[0]:
                #you would think since its the opposite, it should be going negative, but the velocity is already negative
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0

def redrawGameWindow():
    win.blit(bg, (0,0))
    #text step 2: render the text and make the words, 1 (for some reason), and color RGB
    text = font.render("Score: " + str(score), 1, (0, 0, 0))
    #text step 3: place it onto the screen
    win.blit(text, (10, 10))
    man.draw(win)   #draws person onto window
    goblin.draw(win)
    for bullet in bullets:
        # after a bullet is added (by clicking space), the bullet is drawn using the draw function in projectile
        #also, since it was appended as a projectile
        bullet.draw(win)
    pygame.display.update()


#mainloop
#text step 1: make the font, size, and bold
font = pygame.font.SysFont('arial', 30, True)
man = player(50, 405, 64, 64)  #man will call to the class and give all the parameters to be used as variables. You can also use the functions
goblin = enemy(100, 410, 64, 64, 450)
shootLoop = 0
score = 0
times_killed = 0
bullets = []
run = True
while run:

    #27 frames per second
    clock.tick(27)

    #makes no collision box if not visible
    if goblin.visible == True:
        # if the top of the man is above the bottom of the goblin's hitbox and the bottom of the man is below the top:
        if man.hitbox[1] < goblin.hitbox[1] + goblin.hitbox[3] and man.hitbox[1] + man.hitbox[3] > goblin.hitbox[1]:
            # if the man is to the right of the left side and is to the left of the right side (x + width will give the x of the other side
            if man.hitbox[0] + man.hitbox[2] > goblin.hitbox[0] and man.hitbox[0] < goblin.hitbox[0] + goblin.hitbox[2]:
                man.hit()
                score -= 5
    else:
        times_killed -= .1
        goblin = enemy(100, 410 - times_killed, 64, 64, 450)

    #what shoot loop will do is it will give a pause so that multiple shots are not happening at one click. The while loop will not allow you to click space until the shoot loop is 0, and the reason the while loop needs to run at least 4 is to calibrate the correct time
    if shootLoop > 0:
        shootLoop += 1
    if shootLoop > 3:
        shootLoop = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #if the bullet is on the screen, it will move a velocity
    for bullet in bullets:
        #if the top of the bullet is above the bottom of the goblin's hitbox and the bottom of the bullet is below the top:
        if bullet.y - bullet.radius < goblin.hitbox[1] + goblin.hitbox[3] and bullet.y + bullet.radius > goblin.hitbox[1]:
            #if the bullet is to the right of the left side and is to the left of the right side (x + width will give the x of the other side
            if bullet.x + bullet.radius > goblin.hitbox[0] and bullet.x - bullet.radius < goblin.hitbox[0] + goblin.hitbox[2]:
                hitSound.play()
                goblin.hit()
                score += 1
                bullets.pop(bullets.index(bullet))
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            #deletes the bullet in bullets list
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and shootLoop == 0:
        bulletSound.play()
        #the x direction will change based off of if the the person is facing left or right
        if man.right:
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            #adds a projectile to the list everytime space is pressed
            #the parameters make sure that the bullet is shooting from the middle of the man
            bullets.append(projectile(round(man.x + man.width //2), round(man.y + man.height //2), 6, (0, 0, 0), facing))
        shootLoop = 1

    if keys[pygame.K_LEFT] and man.x > man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else:
        man.standing = True
        man.walkCount = 0


    if not(man.isJump):
        if keys[pygame.K_UP]:
            man.isJump = True
            #man.right = False
            #man.left = False
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1
            man.y -= (man.jumpCount ** 2) * 0.5 * neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10

    redrawGameWindow()
pygame.quit()