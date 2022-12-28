import pygame, sys
import random

pygame.init()
clock = pygame.time.Clock()


#Setting up main window
WIDTH, HEIGHT = 1280, 960
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')

FPS = 60

rect_length = 140

#game rectangles(x, y, width, height)
ball = pygame.Rect(WIDTH/2 - 15, HEIGHT/2 - 15, 30, 30)
opponent = pygame.Rect(WIDTH - 20, HEIGHT/2 - 70, 10, rect_length)
player = pygame.Rect(10, HEIGHT/2 - 70, 10, rect_length)

bg_color = pygame.Color('grey12')

#game variables
ball_vel_x = 6 * random.choice((1, -1))
ball_vel_y = 6 * random.choice((1, -1))

player_speed = 7
opponent_speed = 7

#making text
player_score = 0
opponent_score = 0
game_font = pygame.font.Font("freesansbold.ttf", 32)

#score timer
score_time = True

def ball_animation():
    global ball_vel_x, ball_vel_y
    global opponent_score, player_score
    global score_time
    global rect_length

    ball.x += ball_vel_x
    ball.y += ball_vel_y

    # makes it so it bounces off walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_vel_y *= -1
    if ball.left <= 0 or ball.right >= WIDTH:
        if ball.left <= 0:
            opponent_score += 1
            score_time = pygame.time.get_ticks()
        elif ball.right >= WIDTH:
            player_score += 1
            score_time = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_vel_x < 0:
        ball_vel_x *= -1
        rect_length -= 20
    if ball.colliderect(opponent) and ball_vel_x > 0:
        ball_vel_x *= -1
        rect_length -= 20

#variables x, y, top, bottom, left, right, and center are all premade by pygame and can only be used by rectangles

def opponent_ai():
    #opponent
    if opponent.top < ball.y:
        opponent.y += opponent_speed
    if opponent.top > ball.y:
        opponent.y -= opponent_speed
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= HEIGHT - 5:
        opponent.bottom = HEIGHT - 5

def ball_restart():
    global ball_vel_x, ball_vel_y
    global score_time

    current_time = pygame.time.get_ticks()
    ball.center = (WIDTH/2, HEIGHT/2)

    if current_time - score_time < 700:
        number_three = game_font.render("3", False, (200, 200, 200))
        WIN.blit(number_three, (WIDTH/2 - 10, HEIGHT/2 + 20))
    if 700 < current_time - score_time < 1400:
        number_two = game_font.render("2", False, (200, 200, 200))
        WIN.blit(number_two, (WIDTH/2 - 10, HEIGHT/2 + 20))
    if 1400 < current_time - score_time < 2100:
        number_one = game_font.render("1", False, (200, 200, 200))
        WIN.blit(number_one, (WIDTH/2 - 10, HEIGHT/2 + 20))

    if current_time - score_time < 2100:
        ball_vel_x, ball_vel_y = 0, 0
    else:
        ball_vel_y = 7 * random.choice((1, -1))
        ball_vel_x = 7 * random.choice((1, -1))
        score_time = None


while True:
    #Handling input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN] and player.bottom + 5 < HEIGHT:
        player.y += player_speed
    if keys[pygame.K_UP] and player.top > 5:
        player.y -= player_speed

    ball_animation()

    opponent_ai()

    #visuals
    WIN.fill(bg_color)
    pygame.draw.rect(WIN, (200, 200, 200), player)
    pygame.draw.rect(WIN, (200, 200, 200), opponent)
    #elipse is the same as rect, just that with the rectangle it can curve it into a ball
    pygame.draw.ellipse(WIN, (200, 200, 200), ball)
    #an aaline is a straight line, drawing a start point and an end point
    pygame.draw.aaline(WIN, (200, 200, 200), (WIDTH/2, 0), (WIDTH/2, HEIGHT))

    if score_time:
        ball_restart()


    #putting text onto screen
    player_text = game_font.render(f"{player_score}", False, (200, 200, 200))
    opponent_text = game_font.render(f"{opponent_score}", False, (200, 200, 200))
    WIN.blit(player_text, (600, 25))
    WIN.blit(opponent_text, (660, 25))

    #Updating window
    clock.tick(FPS)
    pygame.display.flip()