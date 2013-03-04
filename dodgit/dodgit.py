import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 600
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 0, 0)
FPS = 40
ENEMYMINSIZE = 10
ENEMYMAXSIZE = 40
ENEMYMINSPEED = 1
ENEMYMAXSPEED = 8
ADDNEWENEMYRATE = 6
PLAYERMOVERATE = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # quit if escape key is pressed
                    terminate()
                return

def playerHasHitEnemy(playerRect,enemies):
    for e in enemies:
        if playerRect.colliderect(e['rect']):
            return True
    return False


def drawText (text, font, surface, x, y):
    textobj = font.render(text,1,TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj, textrect)


pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
pygame.display.set_caption('Dodgit')
pygame.mouse.set_visible(False)          # making the cursor invisible

font = pygame.font.Sysfont(None,40)

gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')


playerImage = pygame.image.load('player.jpg')
playerRect = playerImage.get_rect()
enemyImage = pygame.image.load('enemy.jpg')

drawText('Dodgit!!',font,windowSurface,(WINDOWWIDTH/3)+20,(WINDOWHEIGHT/3))
drawText('Press any key to start.',font, windowSurface,(WINDOWWIDTH/3)-40,(WINDOWHEIGHT/3)+60)
pygame.display.update()
waitForPlayerToPressKey()

topscore = 0

while True:
    enemies = []
    score = 0
    playerRect.topleft = (WINDOWWIDTH/2,WINDOWHEIGHT - 50)

    moveUp = moveDown = moveLeft = moveRight = False
    enemyAddCounter = 0

    pygame.mixer.music.play(-1,0.0)

    while True:
        score += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = True
                    moveRight = False

                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = True
                    moveLeft = False

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = True
                    moveDown = False

                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = True
                    moveUp = False

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False

                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False

                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False

                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

            if event.type == MOUSEMOTION:
                playerRect.move_ip(event.pos[0] - playerRect.centerx,event.pos[1]-playerRect.centery)


        enemyAddCounter += 1

        if enemyAddCounter == ADDNEWENEMYRATE:
            enemyAddCounter = 0

            enemySize = random.randint(ENEMYMINSIZE,ENEMYMAXSIZE)
            newEnemy = {'rect':pygame.Rect(random.randint(0,WINDOWWIDTH - enemySize), 0 - enemySize, enemySize, enemySize),
                        'speed':random.randint(ENEMYMINSIZE,ENEMYMAXSIZE),
                        'surface': pygame.transform.scale(enemyImage,(enemySize,enemySize))
                        }

            enemies.append(newEnemy)


        # Motion of the Player
        if moveLeft and playerRect.left>0:
            playerRect.move_ip(-1*PLAYERMOVERATE,0)

        if moveRight and playerRect.right < WINDOWWIDTH:
            playerRect.move_ip(PLAYERMOVERATE,0)

        if moveUp and playerRect.top > 0:
            playerRect.move_ip(0, -1*PLAYERMOVERATE)

        if moveDown and playerRect.bottom < WINDOWHEIGHT:
            playerRect.move_ip(0,PLAYERMOVERATE)


        # Making the cursor follow the player
        pygame.mouse.set_pos(playerRect.centerx,playerRect.centery)


        # Motion of Enemies
        for e in enemies:
            e['rect'].move_ip(0,e['speed'])


        # Removing Enemies
        for e in enemies:
            if e['rect'].top > WINDOWHEIGHT:
                enemies.remove(e)


        # Drawing game world on the window
        windowSurface.fill(BACKGROUNDCOLOR)


        # Drawing the score and Top Score
        drawText('Score: %s' % (score), font, windowSurface,10,0)
        drawText('Top Score: %s' %(topscore),font, windowSurface,10,40)


        # Drawing the player's rectangle
        windowSurface.blit(playerImage, playerRect)


        # Drawing enemies
        for e in enemies:
            windowSurface.blit(e['surface'],e['rect'])

        pygame.display.update()


        # Check whether any of the enemies have hit the player.
        if playerHasHitEnemy(playerRect,enemies):
            if score > topscore:
                topscore = score
            break

        mainClock.tick(FPS)


        # "Game Over" screen
    pygame.mixer.music.stop()
    gameOverSound.play()


    drawText('GAME OVER',font,windowSurface,(WINDOWWIDTH/3),(WINDOWHEIGHT/3))
    drawText('Press any key to play again.',font,windowSurface,(WINDOWWIDTH/3) - 80,(WINDOWHEIGHT/3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()





















































                





















































































