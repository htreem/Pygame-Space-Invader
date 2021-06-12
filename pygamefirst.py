import pygame
import random
import math
import time

pygame.init() #initialise pygame

#creates an empty window
screen = pygame.display.set_mode((800,600))

#Background
background = pygame.image.load('background01.jpg')

#Title and Icon
pygame.display.set_caption("Game")
icon = pygame.image.load('planet.png')
pygame.display.set_icon(icon)

#Player
playerImg = pygame.image.load('player.png')
playerX = 90
playerY = 300
playerX_change = 0
playerY_change = 0

#Enemy (pt. 2 creating multiple ones)
#LIST FUNCTIONS
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 12

for i in range (num_of_enemies):
    enemyImg.append(pygame.image.load('Enemy.png'))
    enemyX.append(random.randint(500,730))
    enemyY.append(random.randint(60,530))
    enemyX_change.append(-50)
    enemyY_change.append(5)

#Bullet (at ready state, you cannot see bullet on the screen. At fire state, bullet is moving)
bulletImg = pygame.image.load('bullet.png')
bulletX = 90
bulletY = 0
bulletX_change = 23
bulletY_change = 0
bullet_state = "ready"

#Score counter
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)
textX = 10
textY = 10
def show_score(x,y):
    score = font.render("Score: " + str(score_value), True, (255,255,255)) #typecasting
    screen.blit(score, (x, y))

#Game over text
go = False
over_font = pygame.font.Font("freesansbold.ttf",64)
def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255,255,255))
    screen.blit(over_text, (200, 250))

def player(x,y):
    screen.blit(playerImg, (x, y)) #drawing the player on the screen

def enemy(x,y,i):
    screen.blit(enemyImg[i], (x, y)) #drawing the enemy on the screen

def fire_bullet(x,y):
    global bullet_state #ensures bullet_state is also registered/accessible inside the function
    bullet_state = "fire"
    screen.blit(bulletImg, (x+16,y+10)) #this ensures bullet appears at centre of the robot


#distance between bullet and enemy using pythagoras
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance < 27:
        return True
    else:
        return False


#loop so that window doesn't appear and go away suddenly; events happen each loop eg. keyboard presses
running = True
while running:
    # background colour (using 3 values of rgb) + background image
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0)) #where background image appears from

    for event in pygame.event.get():
        if event.type == pygame.QUIT: #this line asks if the red button in the corner has been pressed/if the window is closed
            running = False

        #if keystroke pressed/is down, check which one it is
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                ###print("Left arrow is pressed")
                playerX_change = -5
            if event.key == pygame.K_d:
                ####print("Right arrow is pressed")
                playerX_change = 5
            if event.key == pygame.K_w:
                playerY_change = -5
            if event.key == pygame.K_s:
                playerY_change = 5
            if event.key == pygame.K_RIGHT:
                if bullet_state == "ready": #this ensures the bullets do not teleport after being shot
                    bulletY = playerY  # ensures bullet doesn't stay with spaceship // saves playerY coord into bulletY parameter
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)  # spawns bullet
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s:
                #print("Keystroke has been released")
                playerX_change = 0
                playerY_change = 0

    #player position = player position + change
    playerX += playerX_change
    playerY += playerY_change

    #setting boundaries
    if playerX <= 0:
        playerX =0
    elif playerX >= 736: #not 800 (full size of window) to account for size of the sprite/spaceship
        playerX = 736
    if playerY <= 0:
        playerY = 0
    elif playerY >= 536:
        playerY = 536

    #Enemy movement
    #DO THE EXACT Same thing with the enemy, only make it change direction when it hits the edge and make it move forward as well
    #PT 2 THROW IN LIST
    for i in range (num_of_enemies):

        enemyY[i] += enemyY_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0
        #elif enemyX[i] >= 736:
           # enemyX[i] = 736
        if enemyY[i] <= 0:
            enemyY_change[i] = 5
            enemyX[i] += enemyX_change[i]
        elif enemyY[i] >= 536:
            enemyY_change[i] = -5
            enemyX[i] += enemyX_change[i]


    #Bullet movement (make sure it stays on the screen and reset bullet state when it hits the end)
    if bulletX >= 800:
        bulletX = 90
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change


    #collision (PT 2 LISTS)
    for i in range (num_of_enemies):
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletX = 0
            bullet_state = "ready"
            score_value += 1
            #print(score_value)
            enemyX[i] = random.randint(500, 730)
            enemyY[i] = random.randint(60, 530)

        enemy(enemyX[i], enemyY[i],i)  #was meant to be below outside of for loop but it has to be moved here because of the list. NOTE THE i THROWN IN AT THE END

    # Game over
    for i in range (num_of_enemies):

        if enemyX[i] < 64:
            for j in range(num_of_enemies):
                enemyX[j] = 2000 #pushes enemies off the screen
            playerImg = pygame.image.load('flame.png')
            go = True
            break

        collision = isCollision(enemyX[i], enemyY[i], playerX, playerY)
        if collision:
            for j in range(num_of_enemies):
                enemyX[j] = 2000 #pushes enemies off the screen
            playerImg = pygame.image.load('flame.png')
            go = True
            break

    #this ensures the player stays on the screen and runs the function which moves it
    player(playerX,playerY)
    #showing score counter
    show_score(textX,textY)
    if go == True:
        game_over_text()
    #ensure game updates to deal with new information after each loop
    pygame.display.update()