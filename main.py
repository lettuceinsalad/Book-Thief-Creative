import pygame
from pygame import mixer
import time
import random
import sys
import time

# Samuel Zhang
# Jan 12, 2022

pygame.init()

# colours
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (255, 0, 0)
green = (157, 216, 89)
darkGreen = (148, 210, 82)
backgroundGreen = (142, 201, 35)
blue = (38, 118, 232)
lightBlue = (0, 200, 225)

width = 450
height = 450

win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake')

clock = pygame.time.Clock()

# set size of each snake block and its speed
snakeSize = 30
global snakeSpeed
snakeSpeed = 5

fontPath = 'Emulogic-zrEw.ttf'
font = pygame.font.Font(fontPath, 20)

global musicPlaying
musicPlaying = True

global timeNow
timeNow = 0

# function to display text


def blitText(text, colour, x, y, win, fontSize):
    font = pygame.font.Font(fontPath, fontSize)
    message = font.render(text, True, colour)
    win.blit(message, [x, y])


# function for the main menu screen
def mainMenu():

    # set variables, images, and music
    global musicPlaying
    click = False
    snakeImage = pygame.image.load(
        'snakeimagelarge.png')
    volumeImage = pygame.image.load(
        'volumeon.png')
    muteImage = pygame.image.load('volumeoff.png')
    if musicPlaying:
        mixer.music.load('terrariajungle.mp3')
        pygame.mixer.music.set_volume(0.1)
        mixer.music.play(-1)

    # game loop
    while True:

        # get time from starting the menu
        global startTime
        startTime = pygame.time.get_ticks()

        win.fill(backgroundGreen)

        # get mouse position
        mx, my = pygame.mouse.get_pos()

        # make rects for the buttons
        playButton = pygame.Rect(22, 325, 125, 100)
        diffButton = pygame.Rect(162, 325, 125, 100)
        quitButton = pygame.Rect(302, 325, 125, 100)
        volumeControl = pygame.Rect(5, 5, 36, 36)

        # check if the mouse has clicked on the buttons, and if so then run the appropriate action
        if playButton.collidepoint((mx, my)):
            if click:
                gameLoop()
        if diffButton.collidepoint((mx, my)):
            if click:
                diffMenu()
        if quitButton.collidepoint((mx, my)):
            if click:
                pygame.quit()
        if volumeControl.collidepoint((mx, my)):
            if click:
                if musicPlaying == True:
                    pygame.mixer.music.stop()
                    musicPlaying = False
                else:
                    mixer.music.load(
                        'terrariajungle.mp3')
                    pygame.mixer.music.set_volume(0.1)
                    mixer.music.play(-1)
                    musicPlaying = True

        # draw the rects and text and image
        pygame.draw.rect(win, black, playButton)
        pygame.draw.rect(win, black, diffButton)
        pygame.draw.rect(win, black, quitButton)
        pygame.draw.rect(win, backgroundGreen, volumeControl)
        blitText("PLAY", white, 42, 360, win, 20)
        blitText("DIFFI", white, 172, 347, win, 20)
        blitText("CULTY", white, 172, 372, win, 20)
        blitText("QUIT", white, 322, 360, win, 20)
        win.blit(snakeImage, (5, 5))

        # draw the volume icon on top left
        if musicPlaying:
            win.blit(volumeImage, (5, 5))
        else:
            win.blit(muteImage, (5, 5))

        # check for user input
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# function for the difficulty menu
def diffMenu():
    click = False
    snakeImage = pygame.image.load(
        'snakeimage.png')

    # game loop
    while True:
        win.fill(backgroundGreen)

        # get mouse location
        mx, my = pygame.mouse.get_pos()

        # make rects for the buttons
        easyButton = pygame.Rect(22, 265, 125, 100)
        medButton = pygame.Rect(162, 265, 125, 100)
        hardButton = pygame.Rect(302, 265, 125, 100)
        backButton = pygame.Rect(162, 385, 125, 45)
        backLine = pygame.Rect(0, 160, 450, 75)

        # check if the mouse has clicked any of the button options and adjust the snakeSpeed accordingly
        if easyButton.collidepoint((mx, my)):
            if click:
                global snakeSpeed
                snakeSpeed = 5
        if medButton.collidepoint((mx, my)):
            if click:
                snakeSpeed = 10
        if hardButton.collidepoint((mx, my)):
            if click:
                snakeSpeed = 15
        if backButton.collidepoint((mx, my)):
            if click:
                mainMenu()

        # draw rectangles and text and image
        pygame.draw.rect(win, black, easyButton)
        pygame.draw.rect(win, black, medButton)
        pygame.draw.rect(win, black, hardButton)
        pygame.draw.rect(win, black, backButton)
        pygame.draw.rect(win, (125, 184, 18), backLine)
        blitText("EASY", white, 42, 300, win, 20)
        blitText("MEDIUM", white, 172, 302, win, 17)
        blitText("HARD", white, 322, 300, win, 20)
        blitText("BACK", white, 182, 392, win, 20)
        blitText("DIFFICULTY", white, 20, 170, win, 40)
        win.blit(snakeImage, (117, 0))

        # take user input
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pygame.display.update()
        clock.tick(60)


# main loop
def gameLoop():

    # check if the music is turned off or not
    global musicPlaying
    if musicPlaying:
        pygame.mixer.music.fadeout(1000)
        mixer.music.load('terraria_day.mp3')
        pygame.mixer.music.set_volume(0.1)
        mixer.music.play(-1, 0, 3000)

    # set variables
    gameOver = False
    gameClose = False

    x1 = width / 3
    y1 = height / 3

    x1Change = 0
    y1Change = 0

    snakeList = []
    snakeLen = 1
    direction = ''

    # set food x and y coords
    foodx = round(random.randrange(0, width - snakeSize) / 30.0) * 30.0
    foody = round(random.randrange(0, height - snakeSize) / 30.0) * 30.0

    while not gameOver:
        while gameClose == True:

            # display text when you lose
            win.fill(black)
            blitText("Press R to Play Again", red,
                     width / 30, height / 4, win, 20)
            blitText("ESC to Return to Menu", red,
                     width / 30, height / 3, win, 20)
            blitText("You Lived For:", white, width / 4, height / 2, win, 20)
            score = str(snakeLen - 1)
            blitText(score, white, width / 2.2, height / 1.7, win, 20)
            blitText("You Played for", red,
                     width / 30, 350, win, 20)
            blitText(timeNow, blue,
                     width / 1.4, 350, win, 20)
            blitText("sec", red,
                     width / 1.24, 350, win, 20)

            pygame.mixer.music.fadeout(2000)
            pygame.display.update()

            # when you lose, if r then restart the loop
            # if esc close the tab
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mainMenu()
                    if event.key == pygame.K_r:
                        gameLoop()

        # loop through movement
        # direction variable stops snake from moving into itself
        # space bar adds one segment to the snake
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    mainMenu()
                if direction != 'R':
                    if event.key == pygame.K_LEFT:
                        x1Change = -30
                        y1Change = 0
                        direction = 'L'
                if direction != 'L':
                    if event.key == pygame.K_RIGHT:
                        x1Change = 30
                        y1Change = 0
                        direction = 'R'
                if direction != 'D':
                    if event.key == pygame.K_UP:
                        y1Change = -30
                        x1Change = 0
                        direction = 'U'
                if direction != 'U':
                    if event.key == pygame.K_DOWN:
                        y1Change = 30
                        x1Change = 0
                        direction = 'D'
                if event.key == pygame.K_SPACE:
                    snakeLen += 1

        # lose if the snake goes out of the screen
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            gameClose = True

        # update snake location
        x1 += x1Change
        y1 += y1Change

        # draw the green and dark green background
        win.fill(green)
        for row in range(30):
            for col in range(row % 2, 30, 2):
                pygame.draw.rect(
                    win, darkGreen, (row * snakeSize, col * snakeSize, snakeSize, snakeSize))

        # draw the food
        pygame.draw.rect(win, red, [foodx, foody, snakeSize, snakeSize])

        # update snake head location
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snakeList.append(snakeHead)

        # delete old snake body
        if len(snakeList) > snakeLen:
            del snakeList[0]

        # if the snake head hits its body close the game
        for x in snakeList[:-1]:
            if x == snakeHead:
                gameClose = True

        # draw the snake body and snake head
        for i in snakeList:
            pygame.draw.rect(win, lightBlue, [
                             i[0], i[1], snakeSize, snakeSize])
            pygame.draw.rect(
                win, blue, [snakeHead[0], snakeHead[1], snakeSize, snakeSize])

        # display the score on top left
        value = str(snakeLen - 1)
        blitText(value, white, 15, 15, win, 20)

        # display the time on the top right
        timeNow = str((pygame.time.get_ticks() - startTime) // 1000)
        blitText(timeNow, white, 405, 15, win, 20)
        pygame.display.update()

        # if the snake hits the food make new food coords, add to the size of the snake, and play sound effect
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snakeSize) / 30.0) * 30.0
            foody = round(random.randrange(
                0, height - snakeSize) / 30.0) * 30.0
            snakeLen += 1
            munchSound = mixer.Sound(
                'munchsound.mp3')
            munchSound.set_volume(0.3)
            munchSound.play()

        # set how fast the game runs
        clock.tick(snakeSpeed)


mainMenu()
