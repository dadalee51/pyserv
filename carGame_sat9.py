#MR LEE's code - as at saturday morning 5/9 
#todo: add gravity 
import pygame
import sys
from random import randint as ri
screen = pygame.display.set_mode((800,600))
BLACK=(0,0,0)
WHITE=(255,255,255)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
BLUE=(120,120,250)
clock=pygame.time.Clock()
carX=100
carY=400
cloudX=300
cloudY=200
speedX=1
signXList=[0,200,400,600,800]
#MR LEE's code
def drawCar(screen,x,y):
    pygame.draw.circle(screen,BLACK,[x,y],30)
    pygame.draw.circle(screen,BLACK,[x+100,y],30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def drawRoadSign(screen,x,y):
    pygame.draw.rect(screen,WHITE,[x,y,50,15])
#MR LEE's code
while True:
    screen.fill(WHITE)
    carX+=speedX
    #speedX+=1
    drawBackground(screen,0,0)
    if carX > 400:
        carX=400
        for i,xs in enumerate(signXList):
            if xs<=-200:
                xs+=1100
            drawRoadSign(screen,xs,500)
            xs-=speedX
            signXList[i]=xs
    else:#when car has not reached 400 yet
        for xs in signXList:
            drawRoadSign(screen,xs,500)
    if carX>399:
        cloudX-=speedX
    if cloudX < -20:
        cloudX=1000
        cloudY=ri(0,200)
    if speedX > 40:
        speedX = 40
    #print(carX,speedX)
    #handle keys here -MR LEE
    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pass #try to do whatever here
    elif keys[pygame.K_LEFT]:
        speedX-=1
    elif keys[pygame.K_RIGHT]:
        speedX+=1
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit() #remember to import sys
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    drawCloud(screen,cloudX,cloudY)
    drawCar(screen,carX,carY)
    clock.tick(30)
    pygame.display.flip()
