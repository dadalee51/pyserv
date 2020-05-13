#Expected by end of Today MR LEE
#adding key and event handling
#MR Lee's pygame
import pygame
import sys
from random import randint as ri
screen=pygame.display.set_mode((800,600))
BLACK=(0,0,0)
WHITE=(255,255,255)
BLUE=(120,120,250)
GREEN=(0,255,0)
RED=(255,0,0)
GREY=(170,170,170)
clock=pygame.time.Clock()
carX=100
carY=400
cloudX=300
cloudY=200
signXList=[0,100,200,300,400,500,600,700,800,900,1000]
accelX=0
#MR LEE's code
def drawCar(screen,x,y):
    pygame.draw.circle(screen,BLACK, [x,y], 30)
    pygame.draw.circle(screen,BLACK, [x+100,y], 30)
    pygame.draw.rect(screen,GREEN,[x,y,100,-50])
def drawBackground(screen,x,y):
    pygame.draw.rect(screen,GREY,[x,y+400,800,200])
    pygame.draw.rect(screen,BLUE,[x,y,800,400])
def drawCloud(screen,x,y):
    pygame.draw.ellipse(screen,WHITE,[x,y,50,20])
    pygame.draw.ellipse(screen,WHITE,[x-25,y+15,50,20])
def drawRoadSign(screen,x,y):
    pygame.draw.rect(screen,WHITE,[x,y,50,15])
#MR LEE's code
while True:
    screen.fill(WHITE)
    carX+=accelX
    
    if carX > 400:
        carX=400
    elif carX < 0:
        carX=0
        accelX=0
    if accelX > 40:
        accelX=40
    if carX>399:
        cloudX-=accelX
    if cloudX <= -20:
        cloudX=1000
        cloudY=ri(0,200)
    
    #handle keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        pass
    elif keys[pygame.K_RIGHT]:
        accelX+=1
    elif keys[pygame.K_LEFT]:
        accelX-=1
    elif keys[pygame.K_q]:
        pygame.quit()
        sys.exit()
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    drawBackground(screen,0,0)
    drawCloud(screen,cloudX,cloudY)
    drawCar(screen,carX,carY)
    if carX >= 400:
        for i,xs in enumerate(signXList):
            if xs<=-200:
                xs+=1100
            drawRoadSign(screen,xs,500)
            xs-=accelX
            signXList[i]=xs
    else:
        for xs in signXList:
            drawRoadSign(screen,xs,500)
        
    pygame.display.flip()
    clock.tick(30)

