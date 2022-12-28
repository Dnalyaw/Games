import pygame

#always do pygame.init() before anything if you want to make something using pygame
pygame.init()

#making the width and height of the window (has to be in a tuple) : pygame.display.set_mode((500, 500))
win = pygame.display.set_mode((500, 500))


pygame.display.set_caption("First Game")

def main():
    x = 0
    y = 0
    width = 40
    height = 60
    vel = 5

    isJump = False
    jumpCount = 10


    #pygame's window will close immediately after the code has been processed, so you have to make a while loop run forever in order to keep it running
    run = True
    while run:
        #time delay
        pygame.time.delay(100)

        # event is every move the user inputs into pygame, like a button click or a cursor move
        # pygame.event.get() will get thee events that happened
        for event in pygame.event.get():
            #this just makes it so if you hit the x on the top right, the program finishes
            if event.type == pygame.QUIT:
                run = False

        #finds which keys gets pressed, this is a list
        keys = pygame.key.get_pressed()
        #in the list, we can tell pygame what to do if we push down on a key
        if keys[pygame.K_LEFT] and x > vel:
            #one important thing is that (0,0) in coordinates is on the top left, and (500, 500) is on the bottom right
            x -= vel
        if keys[pygame.K_RIGHT] and x < 500 - width:
            x += vel
        if not(isJump):
            if keys[pygame.K_UP] and y > vel:
                y -= vel
            if keys[pygame.K_DOWN] and y < 500 - height - vel:
                y += vel
            if keys[pygame.K_SPACE]:
                isJump = True
        else:
            #making jumping function
            if jumpCount >= -10:
                neg = 1
                #when the jumpCount reaches 0 from 10, it will go down
                if jumpCount < 0:
                    neg = -1
                # y-= makes the square go up, and the velocity will keep going down as a parabola because the velocity will start at 100, and the velocity will go decrease to 81, 64, 49 abd so on
                y -= (jumpCount ** 2) * 0.5 * neg
                jumpCount -= 1
            else:
                isJump = False
                jumpCount = 10




        #fill fills the background with a color; this is good for deleting if you can see multiple of something
        win.fill((0, 0, 0))
        #the top left of the area is the actual coordinate of the thing
        pygame.draw.rect(win, (200, 23, 255), (x, y, width, height))
        #after making something, you have to display it using pygame.display.update()
        pygame.display.update()

if __name__ == "__main__":
    main()

pygame.quit()