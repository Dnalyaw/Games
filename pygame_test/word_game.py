import random
import pygame

#pygame.init()
pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 800



pygame.display.set_caption("Some Game")


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


    run = True
    while run:



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:

        if keys[pygame.K_RIGHT]:

        if keys[pygame.K_UP] and player.y - player.vel > 0:

        if keys[pygame.K_DOWN] and player.y + player.vel + 50 < WIN_HEIGHT:

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

        draw_window()

        win.fill((255, 255, 255))

    pygame.quit()
    quit()

main()