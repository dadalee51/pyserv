#MR LEE's pygame test
import pygame
import sys
from random import randint as ri
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
while True:
    screen.fill(WHITE)
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        speedY-=1
    else:
        speedY+=gravity
    if keys[pygame.K_RIGHT]:
        speedX+=1 #pass for Chloe
    if keys[pygame.K_LEFT]:
        speedX-=1 #pass for Chloe
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    drawBackground(screen,0,0)
    drawCloud(screen,cloudX,cloudY)
    drawCar(screen,carX,carY)
    carX+=speedX
    carY+=speedY
    speedX+=1#for Chloe
    speedY-=1#for Chloe
    print(speedX)
    if carX > 400:
        carX=400
        cloudX-=speedX
    if cloudX < -20:
        cloudX=1000
        cloudY=ri(0,400)
    clock.tick(10)
    pygame.display.flip()