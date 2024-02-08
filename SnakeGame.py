import pygame, sys, time, random
from pygame.locals import *
from enum import Enum

pygame.init()
playSurface = pygame.display.set_mode((640,480))
pygame.display.set_caption("Snake Game")


class Direction(Enum):
    UP = "up"
    DOWN = "down"
    RIGHT = "right"
    LEFT = "left"


def setConfig():
    playSurface = pygame.display.set_mode((640,480))
    fpsClock = pygame.time.Clock()
    snakePosition = [100, 100]
    snakeSegments = [[100,100],[80,100],[60,100]]
    fruitPosition = [300,300]
    fruitSpawned = 1
    direction = Direction.RIGHT
    changeDirection = direction

    return playSurface, fpsClock, snakePosition, snakeSegments, fruitPosition, fruitSpawned, direction, changeDirection


def joystickConnected():
    # Xbox Controller
    global joystick
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    if joystick_count == 0:
        return False
    else:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        return True


def setBackgroundMusic():
    # Audio mixer for bg music
    pygame.mixer.init()
    pygame.mixer.music.load("bg_music/Blue Danube Strauss (No Copyright Music).mp3")
    pygame.mixer.music.set_volume(1.0)
    pygame.mixer.music.play(-1) # Continuos replay


def setColours():
    global redColour, blackColour, whiteColour, greyColour, greenColour
    redColour = pygame.Color(255, 0, 0)    
    blackColour = pygame.Color(0, 0, 0)
    whiteColour = pygame.Color(255, 255, 255)
    greyColour = pygame.Color(150, 150, 150)
    greenColour = pygame.Color(0,200,0)


def gameOver():
    gameOverFont = pygame.font.Font("freesansbold.ttf", 72)
    gameOverSurf = gameOverFont.render("Game Over", True, greyColour)
    gameOverRect = gameOverSurf.get_rect()
    gameOverRect.midtop = (320, 10)
    playSurface.blit(gameOverSurf, gameOverRect)
    pygame.display.flip()
    time.sleep(1)
    pygame.quit()
    sys.exit()


def getDPadDirection():
    d_pad = (joystick.get_hat(0)[0], joystick.get_hat(0)[1])
    if d_pad == (1, 0):
        return Direction.RIGHT
    elif d_pad == (-1, 0):
        return Direction.LEFT
    elif d_pad == (0, 1):
        return Direction.UP
    elif d_pad == (0, -1):
        return Direction.DOWN


def getKeyDirection(event):
    if event.key==K_RIGHT or event.key==ord("d"):
        return Direction.RIGHT
    if event.key==K_LEFT or event.key==ord("a"):
        return Direction.LEFT
    if event.key==K_UP or event.key==ord("w"):
        return Direction.UP
    if event.key==K_DOWN or event.key==ord("s"):
        return Direction.DOWN
    if event.key==K_ESCAPE:
        pygame.event.post(pygame.event.Event(QUIT))


def getAnalogStickDirection():
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)

    # Threshold for avoid direction detection mistakes (analogic dead zone)
    threshold = 0.3

    # Diagonal threshold
    dThreshold = 0.5

    if x_axis > threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.RIGHT
    elif x_axis < -threshold and y_axis < dThreshold and y_axis > -dThreshold:
        return Direction.LEFT
    elif y_axis > threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.DOWN
    elif y_axis < -threshold and x_axis < dThreshold and x_axis > -dThreshold:
        return Direction.UP


def main(config, joystickConnected):
    playSurface, fpsClock, snakePosition, snakeSegments, fruitPosition, fruitSpawned, direction, changeDirection = config
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                changeDirection = getKeyDirection(event)
            elif joystickConnected and (event.type == pygame.JOYHATMOTION):
                changeDirection = getDPadDirection()
            elif joystickConnected and event.type == pygame.JOYAXISMOTION:
                changeDirection = getAnalogStickDirection()
            
        if changeDirection==Direction.RIGHT and not(direction==Direction.LEFT):
                direction = changeDirection
        if changeDirection==Direction.LEFT and not(direction==Direction.RIGHT):
                direction = changeDirection
        if changeDirection==Direction.UP and not(direction==Direction.DOWN):
                direction = changeDirection
        if changeDirection==Direction.DOWN and not(direction==Direction.UP):
                direction = changeDirection
        
        if direction==Direction.RIGHT:
                snakePosition[0] += 20
        if direction==Direction.LEFT:
                snakePosition[0] -= 20
        if direction==Direction.UP:
                snakePosition[1] -= 20
        if direction==Direction.DOWN:
                snakePosition[1] += 20
        
        snakeSegments.insert(0, list(snakePosition))
        
        if snakePosition[0]==fruitPosition[0] and snakePosition[1]==fruitPosition[1]:
            fruitSpawned = 0
        else:
            snakeSegments.pop()
        
        if fruitSpawned==0:
            x = random.randrange(1,32)
            y = random.randrange(1,24)
            fruitPosition = [x*20, y*20]
            fruitSpawned=1
        
        playSurface.fill(whiteColour)
        for position in snakeSegments:
            pygame.draw.rect(playSurface, greenColour, Rect(position[0], position[1], 20, 20))
        pygame.draw.rect(playSurface, redColour, Rect(fruitPosition[0], fruitPosition[1], 20, 20))
        pygame.display.flip()
        
        if snakePosition[0]>620 or snakePosition[0]<0:
            gameOver()
        if snakePosition[1]>460 or snakePosition[1]<0:
            gameOver()
        
        for snakeBody in snakeSegments[1:]:
            if snakePosition[0]==snakeBody[0] and snakePosition[1]==snakeBody[1]:
                gameOver()
        
        fpsClock.tick(18)


setBackgroundMusic()
setColours()
configValues = setConfig()
hasJoystick = joystickConnected()
main(configValues, hasJoystick)