#MR LEE's pygame test
import pygame
import sys
from random import randint as ri
pygame.init()
try:
    pygame.mixer.music.load('MariobrosPhase1.mid')
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play()
except:
    pass
screen = pygame.display.set_mode((800,600))
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
clock=pygame.time.Clock()
carX=100
carY=400
cloudX=100
cloudY=100
speedX=1
speedY=0
gravity=3
#MR Lee's code
def drawCar(screen, x, y):
    pygame.draw.circle(screen, BLACK, [x,y],30)
    pygame.draw.circle(screen, BLACK, [x+100,y],30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
    pygame.draw.rect(screen,BLUE,[x,y-200,800,600])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def test_keys(k):
    time=pygame.time.get_ticks()
    k=list(pygame.key.get_pressed())
    if time in range(0,1000):
        k[pygame.K_UP]=1
    if time in range(5000,7000):
        k[pygame.K_RIGHT]=1
    #print(k)
    return k
while True:
    screen.fill(WHITE)
    keys=pygame.key.get_pressed()
    keys=test_keys(keys)
    if keys[pygame.K_UP]:
        speedY-=1
    else:
        speedY+=gravity
    if keys[pygame.K_RIGHT]:
        speedX+=1 
    if keys[pygame.K_LEFT]:
        speedX-=1 
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    drawBackground(screen,0,0)
    drawCloud(screen,cloudX,cloudY)
    drawCar(screen,carX,carY)
    carX+=speedX
    carY+=speedY
    if carX > 400:
        carX=400
        cloudX-=speedX
    if cloudX < -20:
        cloudX=1000
        cloudY=ri(0,400)
    if carY>400:
        carY=400
        speedY=0
    clock.tick(30)
    pygame.display.flip()