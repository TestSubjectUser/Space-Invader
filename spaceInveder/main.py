# PNGs are from www.flaticon.com
import pygame
import random
import math
from pygame import mixer

pygame.init()  # initialize the pygame
screen = pygame.display.set_mode((800, 600))  # width,height
# Background
bg = pygame.image.load('background.png')

# Vackground music
mixer.music.load('background.wav')
mixer.music.play(-1)            # plays infinitely, -1

# title and icon
pygame.display.set_caption("Space Inveder")
icon = pygame.image.load('player.png')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('player.png')
playerX_pos = 370
playerY_pos = 480
playerX_pos_change = 0

# enemy, for the multiple enemy's we are creating list(we have to use append method instead of = ) out of it
enemyimg = []
enemyX_pos = []
enemyY_pos = []
enemyX_pos_change = []
enemyY_pos_change = []
num_of_enemy = 6

for i in range(num_of_enemy):
    enemyimg.append(pygame.image.load('enemy.png'))
    enemyX_pos.append(random.randint(0, 736))
    enemyY_pos.append(random.randint(50, 150))
    enemyX_pos_change.append(3)                         # this are constants its okay if we don't make them list, but for the sake of simplisity we doing it.
    enemyY_pos_change.append(40)

#For single enemy
# enemyimg = pygame.image.load('enemy.png')
#     enemyX_pos = random.randint(0, 736)
#     enemyY_pos = random.randint(50, 150)
#     enemyX_pos_change = 3
#     enemyY_pos_change = 40

# Bullet
bulletimg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480  # top of the space
bulletX_pos_change = 0
bulletY_pos_change = 5
bullet_state = "ready"  # ready - can't see bullet on screeen, fire - currently moving

# score = 0
# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)         # freesansbold.ttf - only font is inside pygame(download ttf font file and place that file imside this spaceinveder dict and name it)

textX = 10
textY = 10

#game over text
game_font = pygame.font.Font('freesansbold.ttf', 64)

def showScore(x, y):
    # we using render (first we have to render than blit)
    score = font.render("Score : " + str(score_value), True, (255,255,255))
    screen.blit(score, (x, y))
def game_over_text():
    game_over_font = game_font.render("GAME OVER", True, (255,255,255))
    screen.blit(game_over_font, (200, 250))

def player(X, Y):
    # blit means draw(for this we can say that we are drawing this image of player in this window using blit method)
    screen.blit(playerImg, (X, Y))


def enemy(X, Y, i):
    screen.blit(enemyimg[i], (X, Y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x + 16, y + 10))  # center of space ship change acording our img
    # screen.blit(bulletimg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))  # https://www.mathplanet.com/education/algebra-2/conic-sections/distance-between-two-points-and-the-midpoint
    if distance < 27:
        return True
    else:
        return False


# game loop
running = True
while running:
    # an event is anything that is happening inside our game window, any kind of input control.
    # only closes when close button touched
    screen.fill((25, 40, 65))
    # Background image
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # whenever we press any key stroke on our keyboard, it is a key stroke event
        # KEYDOWN and pygame. KEYUP events respectively. For example, if we want to detect if a key was pressed, we will track if any event of pygame. KEYDOWN occurred or not and, accordingly, we will get to know if any key was pressed or not.
        # KEYDOWN - pressing key, KEYUP - releasing key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print('LEFT arrow is pressed.')
                playerX_pos_change = -4
            if event.key == pygame.K_RIGHT:
                # print('RIGHT arrow is pressed.')
                playerX_pos_change = 4

            if event.key == pygame.K_SPACE:  # it is called when we click space bar so it's disappearing
                if bullet_state is "ready":
                    bullet_sound = mixer.Sound('laser.wav')         #for short sound
                    bullet_sound.play()                             #want to play in loop so
                    bulletX = playerX_pos  # where the spaceship is
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                # print('keystroke has been released!!')
                playerX_pos_change = 0

    # playerX_pos += 0.1
    # playerY_pos -= 0.1

    playerX_pos += playerX_pos_change
    if playerX_pos <= 0:
        playerX_pos = 0
    elif playerX_pos >= 736:  # 64*64 png size
        playerX_pos = 736  # 800 - 64 = 736

    # enemy movement
    for i in range(num_of_enemy):

        # Game Over
        if(enemyY_pos[i] > 440):
            for j in range(num_of_enemy):
                enemyY_pos[i] = 2000
            game_over_text()
            break

        enemyX_pos[i] += enemyX_pos_change[i]
        if enemyX_pos[i] <= 0:
            enemyX_pos_change[i] = 3
            enemyY_pos[i] += enemyY_pos_change[i]
        elif enemyX_pos[i] >= 736:
            enemyX_pos_change[i] = -3
            enemyY_pos[i] += enemyY_pos_change[i]

        # Collision
        collision = isCollision(enemyX_pos[i], enemyY_pos[i], bulletX, bulletY)
        if collision:
            explosion_sound = mixer.Sound('explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            # print(score)
            enemyX_pos[i] = random.randint(0, 736)
            enemyY_pos[i] = random.randint(50, 150)

        enemy(enemyX_pos[i], enemyY_pos[i], i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if (bullet_state is "fire"):
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_pos_change

    player(playerX_pos, playerY_pos)  # make sure this line is after fill methd otherwise it want show up
    # enemy(enemyX_pos, enemyY_pos)
    showScore(textX, textY)
    pygame.display.update()  # if we dont write it screen wont be updates
